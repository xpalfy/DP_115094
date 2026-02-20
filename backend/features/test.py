from ultralytics import YOLO
import csv
import os

# =========================
# DATASET
# =========================
DATA_YAML = "./data.yaml"

# =========================
# MODELS TO EVALUATE
# =========================
MODELS = {
    # ================= YOLOv8 DET =================
    "yolov8n-det-v1": "../runs/train_yolov8n/v1_yolov8n/weights/best.pt",
    "yolov8n-det-v2": "../runs/train_yolov8n/v2_yolov8n/weights/best.pt",

    "yolov8s-det-v1": "../runs/train_yolov8s/v1_yolov8s/weights/best.pt",
    "yolov8s-det-v2": "../runs/train_yolov8s/v2_yolov8s/weights/best.pt",

    "yolov8m-det-v1": "../runs/train_yolov8m/v1_yolov8m/weights/best.pt",
    "yolov8m-det-v2": "../runs/train_yolov8m/v2_yolov8m/weights/best.pt",

    "yolov8l-det-v1": "../runs/train_yolov8l/v1_yolov8l/weights/best.pt",
    "yolov8l-det-v2": "../runs/train_yolov8l/v2_yolov8l/weights/best.pt",

    # ================= YOLOv8 SEG =================
    "yolov8n-seg-v1": "../runs/train_yolov8n-seg/v1_yolov8n-seg/weights/best.pt",
    "yolov8n-seg-v2": "../runs/train_yolov8n-seg/v2_yolov8n-seg/weights/best.pt",

    "yolov8s-seg-v1": "../runs/train_yolov8s-seg/v1_yolov8s-seg/weights/best.pt",
    "yolov8s-seg-v2": "../runs/train_yolov8s-seg/v2_yolov8s-seg/weights/best.pt",

    "yolov8m-seg-v1": "../runs/train_yolov8m-seg/v1_yolov8m-seg/weights/best.pt",
    "yolov8m-seg-v2": "../runs/train_yolov8m-seg/v2_yolov8m-seg/weights/best.pt",

    "yolov8l-seg-v1": "../runs/train_yolov8l-seg/v1_yolov8l-seg/weights/best.pt",
    "yolov8l-seg-v2": "../runs/train_yolov8l-seg/v2_yolov8l-seg/weights/best.pt",

    # ================= YOLO11 DET =================
    "yolo11n-det-v1": "../runs/train_yolo11n/v1_yolo11n/weights/best.pt",
    "yolo11n-det-v2": "../runs/train_yolo11n/v2_yolo11n/weights/best.pt",

    "yolo11s-det-v1": "../runs/train_yolo11s/v1_yolo11s/weights/best.pt",
    "yolo11s-det-v2": "../runs/train_yolo11s/v2_yolo11s/weights/best.pt",

    "yolo11m-det-v1": "../runs/train_yolo11m/v1_yolo11m/weights/best.pt",
    "yolo11m-det-v2": "../runs/train_yolo11m/v2_yolo11m/weights/best.pt",

    "yolo11l-det-v1": "../runs/train_yolo11l/v1_yolo11l/weights/best.pt",
    "yolo11l-det-v2": "../runs/train_yolo11l/v2_yolo11l/weights/best.pt",

    # ================= YOLO11 SEG =================
    "yolo11n-seg-v1": "../runs/train_yolo11n-seg/v1_yolo11n-seg/weights/best.pt",
    "yolo11n-seg-v2": "../runs/train_yolo11n-seg/v2_yolo11n-seg/weights/best.pt",

    "yolo11s-seg-v1": "../runs/train_yolo11s-seg/v1_yolo11s-seg/weights/best.pt",
    "yolo11s-seg-v2": "../runs/train_yolo11s-seg/v2_yolo11s-seg/weights/best.pt",

    "yolo11m-seg-v1": "../runs/train_yolo11m-seg/v1_yolo11m-seg/weights/best.pt",
    "yolo11m-seg-v2": "../runs/train_yolo11m-seg/v2_yolo11m-seg/weights/best.pt",

    "yolo11l-seg-v1": "../runs/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt",
    "yolo11l-seg-v2": "../runs/train_yolo11l-seg/v2_yolo11l-seg/weights/best.pt",

    # ================= YOLO12 DET =================
    "yolo12n-det-v1": "../runs/train_yolo12n/v1_yolo12n/weights/best.pt",
    "yolo12n-det-v2": "../runs/train_yolo12n/v2_yolo12n/weights/best.pt",

    "yolo12s-det-v1": "../runs/train_yolo12s/v1_yolo12s/weights/best.pt",
    "yolo12s-det-v2": "../runs/train_yolo12s/v2_yolo12s/weights/best.pt",

    "yolo12m-det-v1": "../runs/train_yolo12m/v1_yolo12m/weights/best.pt",
    "yolo12m-det-v2": "../runs/train_yolo12m/v2_yolo12m/weights/best.pt",

    "yolo12l-det-v1": "../runs/train_yolo12l/v1_yolo12l/weights/best.pt",
    "yolo12l-det-v2": "../runs/train_yolo12l/v2_yolo12l/weights/best.pt",
}

# =========================
# OUTPUT
# =========================
OUTPUT_CSV = "test_results.csv"

results = []

# =========================
# RUN TEST EVALUATION
# =========================
for name, weight_path in MODELS.items():
    print(f"\n=== Evaluating {name} ===")

    if not os.path.exists(weight_path):
        print(f"Weights not found: {weight_path}")
        continue

    model = YOLO(weight_path)

    metrics = model.val(
        data=DATA_YAML,
        split="test",
        imgsz=1024,
        conf=0.25,
        device=0
    )

    row = {
        "model": name,
        "mAP50_box": metrics.box.map50 if hasattr(metrics, "box") else None,
        "mAP50_95_box": metrics.box.map if hasattr(metrics, "box") else None,
        "mAP50_mask": None,
        "mAP50_95_mask": None,
    }

    if "seg" in name and hasattr(metrics, "mask"):
        row["mAP50_mask"] = metrics.mask.map50
        row["mAP50_95_mask"] = metrics.mask.map

    results.append(row)

# =========================
# SAVE RESULTS
# =========================
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "model",
            "mAP50_box",
            "mAP50_95_box",
            "mAP50_mask",
            "mAP50_95_mask",
        ]
    )
    writer.writeheader()
    writer.writerows(results)

print("\nTest evaluation finished")
print(f"Results saved to: {OUTPUT_CSV}")
