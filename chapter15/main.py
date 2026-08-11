from __future__ import annotations

import gc
import io
import logging
import threading
from contextlib import asynccontextmanager
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
VALID_MODEL_SIZES = ["n", "s", "m", "l", "x"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_cache = {
    "current_model": None,
    "current_size": None,
    "lock": threading.Lock(),
}


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox


class DetectionResponse(BaseModel):
    detections: list[Detection]
    count: int
    image_size: dict[str, int]


def load_model(model_size: str) -> YOLO:
    if model_size not in VALID_MODEL_SIZES:
        raise ValueError(f"Invalid model size: {model_size}")

    with model_cache["lock"]:
        if (
            model_cache["current_size"] == model_size
            and model_cache["current_model"] is not None
        ):
            return model_cache["current_model"]

        if model_cache["current_model"] is not None:
            model_cache["current_model"] = None
            model_cache["current_size"] = None
            gc.collect()

        logger.info("Loading yolo26%s.pt", model_size)
        model = YOLO(f"yolo26{model_size}.pt")

        dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
        model(dummy_image)

        model_cache["current_model"] = model
        model_cache["current_size"] = model_size
        return model


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_model("n")
    yield


app = FastAPI(title="YOLO Detection API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def read_root():
    return {"message": "YOLO Detection API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/detect", response_model=DetectionResponse)
async def detect_objects(
    file: UploadFile = File(...),
    conf_threshold: float = Form(0.25),
    model_size: str = Form("n"),
) -> DetectionResponse:
    if model_size not in VALID_MODEL_SIZES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model_size. Must be one of {VALID_MODEL_SIZES}",
        )

    max_size = 10 * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 10MB.",
        )

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image file.",
        )

    image_np = np.array(image)
    if len(image_np.shape) == 3 and image_np.shape[2] == 3:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    try:
        model = load_model(model_size)
        results = model(image_np, conf=conf_threshold)
    except Exception as error:
        logger.exception("Detection failed")
        raise HTTPException(
            status_code=500,
            detail=f"Detection failed: {error}",
        ) from error

    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            detections.append(
                Detection(
                    class_id=class_id,
                    class_name=result.names[class_id],
                    confidence=float(box.conf[0]),
                    bbox=BoundingBox(
                        x1=float(box.xyxy[0][0]),
                        y1=float(box.xyxy[0][1]),
                        x2=float(box.xyxy[0][2]),
                        y2=float(box.xyxy[0][3]),
                    ),
                )
            )

    return DetectionResponse(
        detections=detections,
        count=len(detections),
        image_size={"width": image.width, "height": image.height},
    )
