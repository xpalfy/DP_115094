import os
import uuid
import cv2
import torch
import pytesseract
import easyocr
import numpy as np
from PIL import Image
from flask import request, jsonify
from ultralytics import YOLO
from functools import lru_cache

from rfdetr import (
    RFDETRBase, RFDETRNano, RFDETRSmall,
    RFDETRLarge, RFDETRMedium,
    RFDETRSegNano, RFDETRSegSmall
)

from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
from microservices.rfdetr_sahi import RFDETRDetectionModel


# ===================================================
# CONFIG
# ===================================================

CLASS_NAMES = [
    "a","b","c","d","e","f","g","h","i","l",
    "m","n","o","p","r","s","t","u","v","w","z"
]

# ===================================================
# OCR
# ===================================================
# Pytesseract for non-container environments
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
easyocr_reader = easyocr.Reader(["en"], gpu=torch.cuda.is_available())

# ===================================================
# MODEL MAP (UNCHANGED)
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

    "yolo26n-german": ("runs/german/yolo26/detect/train_yolo26n/v1_yolo26n/weights/best.pt", "yolov8"),
    "yolo26s-german": ("runs/german/yolo26/detect/train_yolo26s/v1_yolo26s/weights/best.pt", "yolov8"),
    "yolo26m-german": ("runs/german/yolo26/detect/train_yolo26m/v1_yolo26m/weights/best.pt", "yolov8"),
    "yolo26l-german": ("runs/german/yolo26/detect/train_yolo26l/v1_yolo26l/weights/best.pt", "yolov8"),

    "yolo26n-seg-german": ("runs/german/yolo26/segment/train_yolo26n-seg/v1_yolo26n-seg/weights/best.pt", "yolov8"),
    "yolo26s-seg-german": ("runs/german/yolo26/segment/train_yolo26s-seg/v1_yolo26s-seg/weights/best.pt", "yolov8"),
    "yolo26m-seg-german": ("runs/german/yolo26/segment/train_yolo26m-seg/v1_yolo26m-seg/weights/best.pt", "yolov8"),
    "yolo26l-seg-german": ("runs/german/yolo26/segment/train_yolo26l-seg/v1_yolo26l-seg/weights/best.pt", "yolov8"),

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

    "yolo26n-french": ("runs/french/yolo26/detect/train_yolo26n/v1_yolo26n/weights/best.pt", "yolov8"),
    "yolo26s-french": ("runs/french/yolo26/detect/train_yolo26s/v1_yolo26s/weights/best.pt", "yolov8"),
    "yolo26m-french": ("runs/french/yolo26/detect/train_yolo26m/v1_yolo26m/weights/best.pt", "yolov8"),
    "yolo26l-french": ("runs/french/yolo26/detect/train_yolo26l/v1_yolo26l/weights/best.pt", "yolov8"),

    "yolo26n-seg-french": ("runs/french/yolo26/segment/train_yolo26n-seg/v1_yolo26n-seg/weights/best.pt", "yolov8"),
    "yolo26s-seg-french": ("runs/french/yolo26/segment/train_yolo26s-seg/v1_yolo26s-seg/weights/best.pt", "yolov8"),
    "yolo26m-seg-french": ("runs/french/yolo26/segment/train_yolo26m-seg/v1_yolo26m-seg/weights/best.pt", "yolov8"),
    "yolo26l-seg-french": ("runs/french/yolo26/segment/train_yolo26l-seg/v1_yolo26l-seg/weights/best.pt", "yolov8"),

    "yolo12n-french": ("runs/french/yolo12/detect/train_yolo12n/v1_yolo12n/weights/best.pt", "yolov8"),
    "yolo12s-french": ("runs/french/yolo12/detect/train_yolo12s/v1_yolo12s/weights/best.pt", "yolov8"),
    "yolo12m-french": ("runs/french/yolo12/detect/train_yolo12m/v1_yolo12m/weights/best.pt", "yolov8"),
    "yolo12l-french": ("runs/french/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt", "yolov8"),

    # ---------------- COMBINED ----------------
    "yolov8n-combined": ("runs/combined/yolov8/detect/train_yolov8n/v1_yolov8n/weights/best.pt", "yolov8"),
    "yolov8s-combined": ("runs/combined/yolov8/detect/train_yolov8s/v1_yolov8s/weights/best.pt", "yolov8"),
    "yolov8m-combined": ("runs/combined/yolov8/detect/train_yolov8m/v1_yolov8m/weights/best.pt", "yolov8"),
    "yolov8l-combined": ("runs/combined/yolov8/detect/train_yolov8l/v1_yolov8l/weights/best.pt", "yolov8"),

    "yolov8n-seg-combined": ("runs/combined/yolov8/segment/train_yolov8n-seg/v1_yolov8n-seg/weights/best.pt", "yolov8"),
    "yolov8s-seg-combined": ("runs/combined/yolov8/segment/train_yolov8s-seg/v1_yolov8s-seg/weights/best.pt", "yolov8"),
    "yolov8m-seg-combined": ("runs/combined/yolov8/segment/train_yolov8m-seg/v1_yolov8m-seg/weights/best.pt", "yolov8"),
    "yolov8l-seg-combined": ("runs/combined/yolov8/segment/train_yolov8l-seg/v1_yolov8l-seg/weights/best.pt", "yolov8"),

    "yolo11n-combined": ("runs/combined/yolo11/detect/train_yolo11n/v1_yolo11n/weights/best.pt", "yolov8"),
    "yolo11s-combined": ("runs/combined/yolo11/detect/train_yolo11s/v1_yolo11s/weights/best.pt", "yolov8"),
    "yolo11m-combined": ("runs/combined/yolo11/detect/train_yolo11m/v1_yolo11m/weights/best.pt", "yolov8"),
    "yolo11l-combined": ("runs/combined/yolo11/detect/train_yolo11l/v1_yolo11l/weights/best.pt", "yolov8"),

    "yolo11n-seg-combined":  ("runs/combined/yolo11/segment/train_yolo11n-seg/v1_yolo11n-seg/weights/best.pt", "yolov8"),
    "yolo11s-seg-combined":  ("runs/combined/yolo11/segment/train_yolo11s-seg/v1_yolo11s-seg/weights/best.pt", "yolov8"),
    "yolo11m-seg-combined":  ("runs/combined/yolo11/segment/train_yolo11m-seg/v1_yolo11m-seg/weights/best.pt", "yolov8"),
    "yolo11l-seg-combined":  ("runs/combined/yolo11/segment/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt", "yolov8"),

    "yolo26n-combined": ("runs/combined/yolo26/detect/train_yolo26n/v1_yolo26n/weights/best.pt", "yolov8"),
    "yolo26s-combined": ("runs/combined/yolo26/detect/train_yolo26s/v1_yolo26s/weights/best.pt", "yolov8"),
    "yolo26m-combined": ("runs/combined/yolo26/detect/train_yolo26m/v1_yolo26m/weights/best.pt", "yolov8"),
    "yolo26l-combined": ("runs/combined/yolo26/detect/train_yolo26l/v1_yolo26l/weights/best.pt", "yolov8"),

    "yolo26n-seg-combined": ("runs/combined/yolo26/segment/train_yolo26n-seg/v1_yolo26n-seg/weights/best.pt", "yolov8"),
    "yolo26s-seg-combined": ("runs/combined/yolo26/segment/train_yolo26s-seg/v1_yolo26s-seg/weights/best.pt", "yolov8"),
    "yolo26m-seg-combined": ("runs/combined/yolo26/segment/train_yolo26m-seg/v1_yolo26m-seg/weights/best.pt", "yolov8"),
    "yolo26l-seg-combined": ("runs/combined/yolo26/segment/train_yolo26l-seg/v1_yolo26l-seg/weights/best.pt", "yolov8"),

    "yolo12n-combined": ("runs/combined/yolo12/detect/train_yolo12n/v1_yolo12n/weights/best.pt", "yolov8"),
    "yolo12s-combined": ("runs/combined/yolo12/detect/train_yolo12s/v1_yolo12s/weights/best.pt", "yolov8"),
    "yolo12m-combined": ("runs/combined/yolo12/detect/train_yolo12m/v1_yolo12m/weights/best.pt", "yolov8"),
    "yolo12l-combined": ("runs/combined/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt", "yolov8"),

    "rfdetr-nano-combined": ("runs/combined/rfdetr/detect/train_rf-detr-nano/checkpoint_best_total.pth", "rfdetr"),
    "rfdetr-small-combined": ("runs/combined/rfdetr/detect/train_rf-detr-small/checkpoint_best_total.pth", "rfdetr"),
    "rfdetr-base-combined": ("runs/combined/rfdetr/detect/train_rf-detr-base/checkpoint_best_total.pth", "rfdetr"),
    "rfdetr-medium-combined": ("runs/combined/rfdetr/detect/train_rf-detr-medium/checkpoint_best_total.pth", "rfdetr"),
    "rfdetr-large-combined": ("runs/combined/rfdetr/detect/train_rf-detr-large/checkpoint_best_total.pth", "rfdetr"),

    "rfdetr-nano-seg-combined": ("runs/combined/rfdetr/segment/train_rf-detr-seg-nano/checkpoint_best_total.pth", "rfdetr"),
    "rfdetr-small-seg-combined": ("runs/combined/rfdetr/segment/train_rf-detr-seg-small/checkpoint_best_total.pth", "rfdetr"),
}


# ===================================================
# MODEL SELECTION
# ===================================================

def _select_rfdetr_model(model_path: str):
    """Select RF-DETR model class from path."""
    if "seg-nano" in model_path:
        return RFDETRSegNano
    if "seg-small" in model_path:
        return RFDETRSegSmall
    if "nano" in model_path:
        return RFDETRNano
    if "small" in model_path:
        return RFDETRSmall
    if "medium" in model_path:
        return RFDETRMedium
    if "large" in model_path:
        return RFDETRLarge
    return RFDETRBase


# ===================================================
# MODEL LOADING (CACHED)
# ===================================================

@lru_cache(maxsize=4)
def get_yolo_model(model_path: str):
    """Load YOLO model."""
    return YOLO(model_path)


@lru_cache(maxsize=4)
def get_rfdetr_model(model_path: str):
    """Load RF-DETR model."""
    model_cls = _select_rfdetr_model(model_path)

    model = model_cls(
        pretrain_weights=model_path,
        num_classes=len(CLASS_NAMES),
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
    model.optimize_for_inference()
    return model


@lru_cache(maxsize=16)
def get_sahi_model(model_type: str, model_path: str):
    """Load SAHI model."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    if model_type == "rfdetr":
        mapping = {str(i): name for i, name in enumerate(CLASS_NAMES)}

        return RFDETRDetectionModel(
            model_path=model_path,
            confidence_threshold=0.5,
            device=device,
            category_mapping=mapping
        )

    return AutoDetectionModel.from_pretrained(
        model_type=model_type,
        model_path=model_path,
        device=device
    )


# ===================================================
# HELPERS
# ===================================================

def mask_to_polygon(mask, min_area=20):
    """Convert mask to polygon."""
    if mask is None:
        return None

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    best = max(contours, key=cv2.contourArea)

    if cv2.contourArea(best) < min_area:
        return None

    return best.reshape(-1, 2).astype(float).tolist()


# ===================================================
# INFERENCE FUNCTIONS
# ===================================================

def run_yolo(model, filepath, conf, use_polygon):
    """Run YOLO inference."""
    results = model.predict(filepath, imgsz=1024, conf=conf)[0]
    detections = []

    for i, box in enumerate(results.boxes):

        det = {
            "class": str(results.names[int(box.cls.item())]),
            "confidence": float(box.conf.item()),
            "bbox": list(map(float, box.xyxy[0].tolist()))
        }

        if use_polygon and results.masks is not None and i < len(results.masks.xy):
            det["polygon"] = results.masks.xy[i].tolist()

        detections.append(det)

    return detections


def run_rfdetr(model_path, filepath, conf, use_polygon):
    """Run RF-DETR inference."""
    model = get_rfdetr_model(model_path)
    image = Image.open(filepath).convert("RGB")

    preds = model.predict(image, threshold=conf)
    results = []

    masks = getattr(preds, "masks", None) or getattr(preds, "mask", None)

    for i, (xyxy, score, class_id) in enumerate(zip(
        preds.xyxy, preds.confidence, preds.class_id
    )):

        det = {
            "class": CLASS_NAMES[int(class_id)] if int(class_id) < len(CLASS_NAMES) else str(class_id),
            "confidence": float(score),
            "bbox": list(map(float, xyxy))
        }

        if use_polygon and masks is not None and i < len(masks):
            mask = (masks[i] > 0).astype(np.uint8)
            poly = mask_to_polygon(mask)
            if poly:
                det["polygon"] = poly

        results.append(det)

    return results


def run_sahi(model_path, filepath, model_type, conf, use_polygon):
    """Run SAHI inference."""
    model = get_sahi_model(model_type, model_path)
    model.confidence_threshold = conf

    result = get_sliced_prediction(filepath, model)
    detections = []

    for det in result.object_prediction_list:
        x1, y1, x2, y2 = det.bbox.to_xyxy()

        out = {
            "class": str(det.category.name),
            "confidence": float(det.score.value),
            "bbox": [float(x1), float(y1), float(x2), float(y2)]
        }

        if use_polygon and det.mask is not None:
            bool_mask = getattr(det.mask, "bool_mask", None)
            if bool_mask is not None:
                mask = (np.asarray(bool_mask, dtype=np.uint8) * 255)
                poly = mask_to_polygon(mask)
                if poly:
                    out["polygon"] = poly

        detections.append(out)

    return detections


# ===================================================
# OCR
# ===================================================

def run_pytesseract(filepath):
    """Run pytesseract OCR."""
    img = cv2.imread(filepath)
    h, _, _ = img.shape

    detections = []

    for b in pytesseract.image_to_boxes(img).splitlines():
        c, x1, y1, x2, y2 = b.split()[:5]

        detections.append({
            "class": str(c),
            "confidence": 1.0,
            "bbox": [int(x1), int(h - int(y2)), int(x2), int(h - int(y1))]
        })

    return detections


def run_easyocr(filepath):
    """Run EasyOCR."""
    img = cv2.imread(filepath)
    detections = []

    for bbox, text, prob in easyocr_reader.readtext(img):
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]

        detections.append({
            "class": str(text),
            "confidence": float(prob),
            "bbox": list(map(float, [min(xs), min(ys), max(xs), max(ys)]))
        })

    return detections


# ===================================================
# ROUTE
# ===================================================

def register_detect_routes(app):

    @app.route("/detect", methods=["POST"])
    def detect_handler():

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        mode = request.form.get("mode", "yolov8n-german")
        use_sahi = request.form.get("useSAHI", "false").lower() == "true"
        use_polygon = request.form.get("usePolygon", "false").lower() == "true"
        confidence = float(request.form.get("confidence", 50)) / 100.0

        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", f"{uuid.uuid4()}_{file.filename}")
        file.save(filepath)

        try:
            if mode == "pytesseract":
                detections = run_pytesseract(filepath)

            elif mode == "easyocr":
                detections = run_easyocr(filepath)

            else:
                if mode not in MODEL_MAP:
                    return jsonify({"error": f"Unknown mode '{mode}'"}), 400

                model_path, model_type = MODEL_MAP[mode]

                if model_type == "rfdetr" and not use_sahi:
                    detections = run_rfdetr(model_path, filepath, confidence, use_polygon)

                elif use_sahi:
                    detections = run_sahi(model_path, filepath, model_type, confidence, use_polygon)

                else:
                    model = get_yolo_model(model_path)
                    detections = run_yolo(model, filepath, confidence, use_polygon)

            return jsonify({
                "mode": mode,
                "useSAHI": use_sahi,
                "usePolygon": use_polygon,
                "detections": detections
            })

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
