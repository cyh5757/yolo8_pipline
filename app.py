from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os
from ultralytics import YOLO

app = FastAPI()
# train 폴더 별 사용자 지정 선택
model = YOLO('runs/detect/train3/weights/best.pt')

class DetectionResult(BaseModel):
    label: str
    confidence: float

@app.post("/predict/", response_model=dict)
async def predict(file: UploadFile = File(...)):
    # 파일 확장자 체크
    if not file.filename.endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload jpg or png images only.")

    # 파일 저장
    temp_path = "temp.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Inference with low conf threshold
        results = model(temp_path, conf=0.1)
        boxes = results[0].boxes

        detections = []
        for box in boxes:
            label_id = int(box.cls[0].item())
            label_name = results[0].names[label_id]
            conf = box.conf[0].item()
            detections.append({
                "label": label_name,
                "confidence": round(conf, 4)
            })

        return {"detections": detections}

    finally:
        # temp 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)
