# Ultralyticsの公式イメージを使用
FROM ultralytics/ultralytics:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 作業ディレクトリの設定
WORKDIR /app

# FastAPI関連のパッケージを追加インストール
COPY requirements-web.txt ./requirements-web.txt
RUN python -m pip install --no-cache-dir -r requirements-web.txt

# アプリケーションのコードをコピー
COPY main.py .
COPY static ./static

# ポート8000を公開
EXPOSE 8000

# FastAPIサーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
