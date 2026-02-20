import os
import cv2
import pytesseract
import easyocr
import numpy as np
from flask import request, jsonify
from ultralytics import YOLO
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

# ===================================================
# OCR
# ===================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
easyocr_reader = easyocr.Reader(["en"])

# ===================================================
# YOLO MODELS
# ===================================================

# YOLOv8 detection
yolov8n_model = YOLO("runs/runs_linux/yolov8/detect/train_yolov8n/v1_yolov8n/weights/best.pt")
yolov8s_model = YOLO("runs/runs_linux/yolov8/detect/train_yolov8s/v1_yolov8s/weights/best.pt")
yolov8m_model = YOLO("runs/runs_linux/yolov8/detect/train_yolov8m/v1_yolov8m/weights/best.pt")
yolov8l_model = YOLO("runs/runs_linux/yolov8/detect/train_yolov8l/v1_yolov8l/weights/best.pt")

# YOLOv8 segmentation
yolov8n_seg_model = YOLO("runs/runs_linux/yolov8/segment/train_yolov8n-seg/v1_yolov8n-seg/weights/best.pt")
yolov8s_seg_model = YOLO("runs/runs_linux/yolov8/segment/train_yolov8s-seg/v1_yolov8s-seg/weights/best.pt")
yolov8m_seg_model = YOLO("runs/runs_linux/yolov8/segment/train_yolov8m-seg/v1_yolov8m-seg/weights/best.pt")
yolov8l_seg_model = YOLO("runs/runs_linux/yolov8/segment/train_yolov8l-seg/v1_yolov8l-seg/weights/best.pt")

# YOLO11 detection
yolo11n_model = YOLO("runs/runs_linux/yolo11/detect/train_yolo11n/v1_yolo11n/weights/best.pt")
yolo11s_model = YOLO("runs/runs_linux/yolo11/detect/train_yolo11s/v1_yolo11s/weights/best.pt")
yolo11m_model = YOLO("runs/runs_linux/yolo11/detect/train_yolo11m/v1_yolo11m/weights/best.pt")
yolo11l_model = YOLO("runs/runs_linux/yolo11/detect/train_yolo11l/v1_yolo11l/weights/best.pt")

# YOLO11 segmentation
yolo11n_seg_model = YOLO("runs/runs_linux/yolo11/segment/train_yolo11n-seg/v1_yolo11n-seg/weights/best.pt")
yolo11s_seg_model = YOLO("runs/runs_linux/yolo11/segment/train_yolo11s-seg/v1_yolo11s-seg/weights/best.pt")
yolo11m_seg_model = YOLO("runs/runs_linux/yolo11/segment/train_yolo11m-seg/v1_yolo11m-seg/weights/best.pt")
yolo11l_seg_model = YOLO("runs/runs_linux/yolo11/segment/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt")

# YOLO12 detection
yolo12n_model = YOLO("runs/runs_linux/yolo12/detect/train_yolo12n/v1_yolo12n/weights/best.pt")
yolo12s_model = YOLO("runs/runs_linux/yolo12/detect/train_yolo12s/v1_yolo12s/weights/best.pt")
yolo12m_model = YOLO("runs/runs_linux/yolo12/detect/train_yolo12m/v1_yolo12m/weights/best.pt")
yolo12l_model = YOLO("runs/runs_linux/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt")

best_model = YOLO("runs/yolo11/segment/train_yolo11l_seg/v5_yolo11l_seg/weights/best.pt")

MODEL_MAP = {
    "yolov8n": (yolov8n_model, "runs/runs_linux/yolov8/detect/train_yolov8n/v1_yolov8n/weights/best.pt", "yolov8"),
    "yolov8s": (yolov8s_model, "runs/runs_linux/yolov8/detect/train_yolov8s/v1_yolov8s/weights/best.pt", "yolov8"),
    "yolov8m": (yolov8m_model, "runs/runs_linux/yolov8/detect/train_yolov8m/v1_yolov8m/weights/best.pt", "yolov8"),
    "yolov8l": (yolov8l_model, "runs/runs_linux/yolov8/detect/train_yolov8l/v1_yolov8l/weights/best.pt", "yolov8"),

    "yolov8n-seg": (yolov8n_seg_model, "runs/runs_linux/yolov8/segment/train_yolov8n-seg/v1_yolov8n-seg/weights/best.pt", "yolov8"),
    "yolov8s-seg": (yolov8s_seg_model, "runs/runs_linux/yolov8/segment/train_yolov8s-seg/v1_yolov8s-seg/weights/best.pt", "yolov8"),
    "yolov8m-seg": (yolov8m_seg_model, "runs/runs_linux/yolov8/segment/train_yolov8m-seg/v1_yolov8m-seg/weights/best.pt", "yolov8"),
    "yolov8l-seg": (yolov8l_seg_model, "runs/runs_linux/yolov8/segment/train_yolov8l-seg/v1_yolov8l-seg/weights/best.pt", "yolov8"),

    "yolo11n": (yolo11n_model, "runs/runs_linux/yolo11/detect/train_yolo11n/v1_yolo11n/weights/best.pt", "yolov8"),
    "yolo11s": (yolo11s_model, "runs/runs_linux/yolo11/detect/train_yolo11s/v1_yolo11s/weights/best.pt", "yolov8"),
    "yolo11m": (yolo11m_model, "runs/runs_linux/yolo11/detect/train_yolo11m/v1_yolo11m/weights/best.pt", "yolov8"),
    "yolo11l": (yolo11l_model, "runs/runs_linux/yolo11/detect/train_yolo11l/v1_yolo11l/weights/best.pt", "yolov8"),

    "yolo11n-seg": (yolo11n_seg_model, "runs/runs_linux/yolo11/segment/train_yolo11n-seg/v1_yolo11n-seg/weights/best.pt", "yolov8"),
    "yolo11s-seg": (yolo11s_seg_model, "runs/runs_linux/yolo11/segment/train_yolo11s-seg/v1_yolo11s-seg/weights/best.pt", "yolov8"),
    "yolo11m-seg": (yolo11m_seg_model, "runs/runs_linux/yolo11/segment/train_yolo11m-seg/v1_yolo11m-seg/weights/best.pt", "yolov8"),
    "yolo11l-seg": (yolo11l_seg_model, "runs/runs_linux/yolo11/segment/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt", "yolov8"),

    "yolo12n": (yolo12n_model, "runs/runs_linux/yolo12/detect/train_yolo12n/v1_yolo12n/weights/best.pt", "yolov8"),
    "yolo12s": (yolo12s_model, "runs/runs_linux/yolo12/detect/train_yolo12s/v1_yolo12s/weights/best.pt", "yolov8"),
    "yolo12m": (yolo12m_model, "runs/runs_linux/yolo12/detect/train_yolo12m/v1_yolo12m/weights/best.pt", "yolov8"),
    "yolo12l": (yolo12l_model, "runs/runs_linux/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt", "yolov8"),

    "best": (best_model, "runs/yolo11/segment/train_yolo11l_seg/v5_yolo11l_seg/weights/best.pt", "yolov8"),
}

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
    detection_model = AutoDetectionModel.from_pretrained(
        model_type=model_type,
        model_path=model_path,
        confidence_threshold=conf,
        device="cuda"
    )

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

def register_detect_routes(app):

    @app.route("/detect", methods=["POST"])
    def detect_handler():
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        mode = request.form.get("mode", "yolo11n")
        use_sahi = request.form.get("useSAHI", "false").lower() == "true"
        use_polygon = request.form.get("usePolygon", "false").lower() == "true"
        confidence = float(request.form.get("confidence", 50)) / 100.0

        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # OCR
        if mode == "pytesseract":
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
            return jsonify({"mode": mode, "detections": detections})

        if mode == "easyocr":
            img = cv2.imread(filepath)
            detections = []

            for bbox, text, prob in easyocr_reader.readtext(img):
                xs = [float(p[0]) for p in bbox]
                ys = [float(p[1]) for p in bbox]

                detections.append({
                    "class": str(text),
                    "confidence": float(prob),
                    "bbox": [float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys))]
                })
            return jsonify({"mode": mode, "detections": detections})

        # YOLO
        if mode not in MODEL_MAP:
            return jsonify({"error": f"Unknown mode '{mode}'"}), 400

        model, model_path, model_type = MODEL_MAP[mode]

        if use_sahi:
            detections = run_sahi_inference(
                model_path=model_path,
                image_path=filepath,
                model_type=model_type,
                conf=confidence,
                use_polygon=use_polygon
            )
        else:
            detections = []
            results = model.predict(filepath, imgsz=1024, conf=confidence)
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

        return jsonify({
            "mode": mode,
            "useSAHI": use_sahi,
            "usePolygon": use_polygon,
            "detections": detections
        })