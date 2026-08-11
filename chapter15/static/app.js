const imageInput = document.getElementById('imageInput');
const fileName = document.getElementById('fileName');
const detectButton = document.getElementById('detectButton');
const loading = document.getElementById('loading');
const resultSection = document.getElementById('resultSection');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const detectionInfo = document.getElementById('detectionInfo');
const confThreshold = document.getElementById('confThreshold');
const confValue = document.getElementById('confValue');

let selectedImage = null;

// スライダーの値が変更されたときの処理
confThreshold.addEventListener('input', function(e) {
    confValue.textContent = e.target.value;
});

// 画像選択時の処理
imageInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        detectButton.disabled = false;

        // 画像を読み込んでメモリに保持
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                selectedImage = img;
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);

        resultSection.style.display = 'none';
    }
});

detectButton.addEventListener('click', async function() {
    if (!imageInput.files[0] || !selectedImage) return;

    const selectedModel = document.querySelector('input[name="modelSize"]:checked').value;
    detectButton.disabled = true;
    loading.textContent = '処理中...';
    loading.style.display = 'block';

    try {
        // FormDataを作成
        const formData = new FormData();
        formData.append('file', imageInput.files[0]);
        formData.append('conf_threshold', confThreshold.value);
        formData.append('model_size', selectedModel);

        // APIリクエスト
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // キャンバスのサイズを設定して結果セクションを表示
        canvas.width = selectedImage.width;
        canvas.height = selectedImage.height;
        resultSection.style.display = 'block';

        // 結果を描画
        drawDetections(result);

    } catch (error) {
        alert('エラーが発生しました: ' + error.message);
        console.error('Error:', error);
    } finally {
        detectButton.disabled = false;
        loading.style.display = 'none';
    }
});

function drawDetections(result) {
    // 元の画像を再描画
    ctx.drawImage(selectedImage, 0, 0);

    // 検出結果を描画
    result.detections.forEach(detection => {
        const bbox = detection.bbox;

        // バウンディングボックスを描画
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(
            bbox.x1,
            bbox.y1,
            bbox.x2 - bbox.x1,
            bbox.y2 - bbox.y1
        );

        // ラベルの背景
        const label = `${detection.class_name} ${(detection.confidence * 100).toFixed(1)}%`;
        ctx.font = '16px Arial';
        const textWidth = ctx.measureText(label).width;

        ctx.fillStyle = '#00ff00';
        ctx.fillRect(bbox.x1, bbox.y1 - 25, textWidth + 10, 25);

        // ラベルのテキスト
        ctx.fillStyle = '#000000';
        ctx.fillText(label, bbox.x1 + 5, bbox.y1 - 7);
    });

    // 検出情報を表示
    displayDetectionInfo(result);
}

function displayDetectionInfo(result) {
    const info = `
        <h3>検出された物体: ${result.count}個</h3>
        <ul>
            ${result.detections.map(det =>
                `<li>${det.class_name}: ${(det.confidence * 100).toFixed(1)}%</li>`
            ).join('')}
        </ul>
        <p>画像サイズ: ${result.image_size.width} × ${result.image_size.height}</p>
    `;
    detectionInfo.innerHTML = info;
}
