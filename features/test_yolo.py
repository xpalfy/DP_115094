from ultralytics import YOLO
import numpy as np
import os

# =========================
# CONFIG
# =========================
MODEL_PATH = "../backend/runs/french/yolo11/segment/train_yolo11l-seg/v1_yolo11l-seg/weights/best.pt"
DATA_YAML = "data.yaml"
IMG_SIZE = 1024
DEVICE = "cuda"

if __name__ == "__main__":

    if not os.path.exists(MODEL_PATH):
        print(f"Weights not found: {MODEL_PATH}")
        exit()

    print(f"\n=== Evaluating {MODEL_PATH} ===")

    model = YOLO(MODEL_PATH)

    metrics = model.val(
        data=DATA_YAML,
        split="test",
        imgsz=IMG_SIZE,
        conf=0.25,
        device=DEVICE
    )

    print("\n================ RESULTS ================\n")

    # =========================
    # BOX METRICS
    # =========================
    if hasattr(metrics, "box"):
        print("BOX METRICS")
        print(f"Precision:  {float(np.mean(metrics.box.p)):.4f}")
        print(f"Recall:     {float(np.mean(metrics.box.r)):.4f}")
        print(f"mAP@50:     {metrics.box.map50:.4f}")
        print(f"mAP@50-95:  {metrics.box.map:.4f}")
        print()

    # =========================
    # MASK METRICS (SEG MODEL)
    # =========================
    if hasattr(metrics, "seg"):
        print("MASK METRICS")
        print(f"Precision:  {float(np.mean(metrics.seg.p)):.4f}")
        print(f"Recall:     {float(np.mean(metrics.seg.r)):.4f}")
        print(f"mAP@50:     {metrics.seg.map50:.4f}")
        print(f"mAP@50-95:  {metrics.seg.map:.4f}")
        print()

    print("=========================================\n")