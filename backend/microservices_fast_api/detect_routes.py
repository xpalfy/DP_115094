import os
import cv2
import pytesseract
import easyocr
import numpy as np
from functools import lru_cache
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse

from ultralytics import YOLO
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

# ===================================================
# OCR
# ===================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
easyocr_reader = easyocr.Reader(["en"])

# ===================================================
# MODEL MAP
# ===================================================

MODEL_MAP = {
    # ---------------- GERMAN ----------------
    "yolov8n-german": ("runs/german/yolov8/detect/train_yolov8n/v1_yolov8n/weights/best.pt", "yolov8"),
    "yolov8s-german": ("runs/german/yolov8/detect/train_yolov8s/v1_yolov8s/weights/best.pt", "yolov8"),
    "yolov8m-german": ("runs/german/yolov8/detect/train_yolov8m/v1_yolov8m/weights/best.pt", "yolov8"),
    "yolov8l-german": ("runs/german/yolov8/detect/train_yolov8l/v1_yolov8l/weights/best.pt", "yolov8"),

    "yolov8n-seg-german": ("runs/german/yolov8/segment/train_yolov8n-seg/v1_yolov8n-seg/weights/best.pt", "yolov8"),
    "yolov8s-seg-german": ("runs/german/yolov8/segment/train_yolov8s-seg/v1_yolov8s-seg/weights/best.pt", "yolov8"),
    "yolov8m-seg-german": ("runs/german/yolov8/segment/train_yolov8m-seg/v1_yolov8m-seg/weights/best.pt", "yolov8"),
    "yolov8l-seg-german": ("runs/german/yolov8/segment/train_yolov8l-seg/v1_yolov8l-seg/weights/best.pt", "yolov8"),

    "yolo11n-german": ("runs/german/yolo11/detect/train_yolo11n/v1_yolo11n/weights/best.pt", "yolov8"),
    "yolo11s-german": ("runs/german/yolo11/detect/train_yolo11s/v1_yolo11s/weights/best.pt", "yolov8"),
    "yolo11m-german": ("runs/german/yolo11/detect/train_yolo11m/v1_yolo11m/weights/best.pt", "yolov8"),
    "yolo11l-german": ("runs/german/yolo11/detect/train_yolo11l/v1_yolo11l/weights/best.pt", "yolov8"),

    "yolo11n-seg-german": ("runs/german/yolo11/segment/train_yolo11n-seg/v1_yolo11n-seg/weights/best.pt", "yolov8"),
    "yolo11s-seg-german": ("runs/german/yolo11/segment/train_yolo11s-seg/v1_yolo11s-seg/weights/best.pt", "yolov8"),
    "yolo11m-seg-german": ("runs/german/yolo11/segment/train_yolo11m-seg/v1_yolo11m-seg/weights/best.pt", "yolov8"),
    "yolo11l-seg-german": ("runs/german/yolo11/segment/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt", "yolov8"),

    "yolo12n-german": ("runs/german/yolo12/detect/train_yolo12n/v1_yolo12n/weights/best.pt", "yolov8"),
    "yolo12s-german": ("runs/german/yolo12/detect/train_yolo12s/v1_yolo12s/weights/best.pt", "yolov8"),
    "yolo12m-german": ("runs/german/yolo12/detect/train_yolo12m/v1_yolo12m/weights/best.pt", "yolov8"),
    "yolo12l-german": ("runs/german/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt", "yolov8"),

    # ---------------- FRENCH ----------------
    "yolov8n-french": ("runs/french/yolov8/detect/train_yolov8n/v1_yolov8n/weights/best.pt", "yolov8"),
    "yolov8s-french": ("runs/french/yolov8/detect/train_yolov8s/v1_yolov8s/weights/best.pt", "yolov8"),
    "yolov8m-french": ("runs/french/yolov8/detect/train_yolov8m/v1_yolov8m/weights/best.pt", "yolov8"),
    "yolov8l-french": ("runs/french/yolov8/detect/train_yolov8l/v1_yolov8l/weights/best.pt", "yolov8"),

    "yolov8n-seg-french": ("runs/french/yolov8/segment/train_yolov8n-seg/v1_yolov8n-seg/weights/best.pt", "yolov8"),
    "yolov8s-seg-french": ("runs/french/yolov8/segment/train_yolov8s-seg/v1_yolov8s-seg/weights/best.pt", "yolov8"),
    "yolov8m-seg-french": ("runs/french/yolov8/segment/train_yolov8m-seg/v1_yolov8m-seg/weights/best.pt", "yolov8"),
    "yolov8l-seg-french": ("runs/french/yolov8/segment/train_yolov8l-seg/v1_yolov8l-seg/weights/best.pt", "yolov8"),

    "yolo11n-french": ("runs/french/yolo11/detect/train_yolo11n/v1_yolo11n/weights/best.pt", "yolov8"),
    "yolo11s-french": ("runs/french/yolo11/detect/train_yolo11s/v1_yolo11s/weights/best.pt", "yolov8"),
    "yolo11m-french": ("runs/french/yolo11/detect/train_yolo11m/v1_yolo11m/weights/best.pt", "yolov8"),
    "yolo11l-french": ("runs/french/yolo11/detect/train_yolo11l/v1_yolo11l/weights/best.pt", "yolov8"),

    "yolo11n-seg-french": ("runs/french/yolo11/segment/train_yolo11n-seg/v1_yolo11n-seg/weights/best.pt", "yolov8"),
    "yolo11s-seg-french": ("runs/french/yolo11/segment/train_yolo11s-seg/v1_yolo11s-seg/weights/best.pt", "yolov8"),
    "yolo11m-seg-french": ("runs/french/yolo11/segment/train_yolo11m-seg/v1_yolo11m-seg/weights/best.pt", "yolov8"),
    "yolo11l-seg-french": ("runs/french/yolo11/segment/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt", "yolov8"),

    "yolo12n-french": ("runs/french/yolo12/detect/train_yolo12n/v1_yolo12n/weights/best.pt", "yolov8"),
    "yolo12s-french": ("runs/french/yolo12/detect/train_yolo12s/v1_yolo12s/weights/best.pt", "yolov8"),
    "yolo12m-french": ("runs/french/yolo12/detect/train_yolo12m/v1_yolo12m/weights/best.pt", "yolov8"),
    "yolo12l-french": ("runs/french/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt", "yolov8"),
}

# ===================================================
# LAZY LOAD + CACHE
# ===================================================

@lru_cache(maxsize=4)
def get_yolo_model(model_path: str) -> YOLO:
    return YOLO(model_path)

@lru_cache(maxsize=32)
def get_sahi_model(model_type: str, model_path: str, conf: float):
    return AutoDetectionModel.from_pretrained(
        model_type=model_type,
        model_path=model_path,
        confidence_threshold=conf,
        device="cuda"
    )

# ===================================================
# SAHI
# ===================================================

def sahi_mask_to_polygon(det, min_area=20):
    m = getattr(det, "mask", None)
    if m is None:
        return None

    bool_mask = getattr(m, "bool_mask", None)
    if bool_mask is None and hasattr(m, "to_bool_mask"):
        try:
            bool_mask = m.to_bool_mask()
        except Exception:
            return None
    if bool_mask is None:
        return None

    bm = (np.asarray(bool_mask, dtype=np.uint8) * 255)
    contours, _ = cv2.findContours(bm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    best = max(contours, key=cv2.contourArea)
    if cv2.contourArea(best) < min_area:
        return None

    return best.reshape(-1, 2).astype(float).tolist()

def run_sahi_inference(model_path, image_path, model_type="yolov8", conf=0.5, use_polygon=False):
    detection_model = get_sahi_model(model_type, model_path, conf)

    result = get_sliced_prediction(image_path, detection_model)
    detections = []

    for det in result.object_prediction_list:
        x1, y1, x2, y2 = det.bbox.to_xyxy()

        out = {
            "class": str(det.category.name),
            "confidence": float(det.score.value),
            "bbox": [float(x1), float(y1), float(x2), float(y2)]
        }

        if use_polygon:
            poly = sahi_mask_to_polygon(det)
            if poly is not None:
                out["polygon"] = poly

        detections.append(out)

    return detections

# ===================================================
# Routes
# ===================================================

def register_detect_routes(app: FastAPI):

    @app.post("/detect")
    async def detect_handler(
        file: Optional[UploadFile] = File(None),
        mode: str = Form("yolov8n-german"),
        useSAHI: str = Form("false"),
        usePolygon: str = Form("false"),
        confidence: str = Form("50")
    ):
        use_sahi = str(useSAHI).lower() == "true"
        use_polygon = str(usePolygon).lower() == "true"
        confidence_val = float(confidence) / 100.0

        if file is None:
            return JSONResponse(status_code=400, content={"error": "No file uploaded"})

        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)

        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)

        # OCR
        if mode == "pytesseract":
            img = cv2.imread(filepath)
            if img is None:
                return JSONResponse(status_code=400, content={"error": "Invalid image"})
            h, _, _ = img.shape
            detections = []

            for b in pytesseract.image_to_boxes(img).splitlines():
                c, x1, y1, x2, y2 = b.split()[:5]
                detections.append({
                    "class": str(c),
                    "confidence": 1.0,
                    "bbox": [int(x1), int(h - int(y2)), int(x2), int(h - int(y1))]
                })
            return {"mode": mode, "detections": detections}

        if mode == "easyocr":
            img = cv2.imread(filepath)
            if img is None:
                return JSONResponse(status_code=400, content={"error": "Invalid image"})
            detections = []

            for bbox, text, prob in easyocr_reader.readtext(img):
                xs = [float(p[0]) for p in bbox]
                ys = [float(p[1]) for p in bbox]
                detections.append({
                    "class": str(text),
                    "confidence": float(prob),
                    "bbox": [float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys))]
                })
            return {"mode": mode, "detections": detections}

        # YOLO / SAHI
        if mode not in MODEL_MAP:
            return JSONResponse(status_code=400, content={"error": f"Unknown mode '{mode}'"})

        model_path, model_type = MODEL_MAP[mode]

        if use_sahi:
            detections = run_sahi_inference(
                model_path=model_path,
                image_path=filepath,
                model_type=model_type,
                conf=confidence_val,
                use_polygon=use_polygon
            )
        else:
            model = get_yolo_model(model_path)
            detections = []
            results = model.predict(filepath, imgsz=1024, conf=confidence_val)
            r = results[0]

            for i, box in enumerate(r.boxes):
                det = {
                    "class": str(r.names[int(box.cls.item())]),
                    "confidence": float(box.conf.item()),
                    "bbox": [
                        float(box.xyxy[0][0].item()),
                        float(box.xyxy[0][1].item()),
                        float(box.xyxy[0][2].item()),
                        float(box.xyxy[0][3].item())
                    ]
                }

                if use_polygon and getattr(r, "masks", None) is not None and r.masks is not None:
                    if i < len(r.masks.xy) and r.masks.xy[i] is not None:
                        det["polygon"] = r.masks.xy[i].tolist()

                detections.append(det)

        return {
            "mode": mode,
            "useSAHI": use_sahi,
            "usePolygon": use_polygon,
            "detections": detections
        }