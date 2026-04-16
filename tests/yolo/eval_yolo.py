from ultralytics import YOLO
import torch
import numpy as np


# ===================================================
# CONFIG
# ===================================================

MODEL_PATH = "../../backend/runs/combined/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt"
DATA_YAML = "data.yaml"

IMG_SIZE = 1024
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CONF = 0.5

# ===================================================
# METRICS PRINT
# ===================================================

def print_metrics(metrics):
    print("\n================ RESULTS ================\n")

    # --------
    # --- BBOX -----------
    if hasattr(metrics, "box") and metrics.box is not None:
        print("BOX METRICS")
        print(f"Precision:  {float(np.mean(metrics.box.p)):.4f}")
        print(f"Recall:     {float(np.mean(metrics.box.r)):.4f}")
        print(f"mAP@50:     {metrics.box.map50:.4f}")
        print(f"mAP@50-95:  {metrics.box.map:.4f}")
        print()

    # ----------- SEGMENTATION -----------
    if hasattr(metrics, "seg") and metrics.seg is not None:
        print("MASK METRICS")
        print(f"Precision:  {float(np.mean(metrics.seg.p)):.4f}")
        print(f"Recall:     {float(np.mean(metrics.seg.r)):.4f}")
        print(f"mAP@50:     {metrics.seg.map50:.4f}")
        print(f"mAP@50-95:  {metrics.seg.map:.4f}")
        print()

    print("=========================================\n")


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":

    print(f"\n=== Loading model: {MODEL_PATH} ===")

    model = YOLO(MODEL_PATH)

    print("Model loaded\n")

    print("Running evaluation...\n")

    metrics = model.val(
        data=DATA_YAML,
        split="test",
        imgsz=IMG_SIZE,
        conf=CONF,
        device=DEVICE,
        verbose=True
    )

    torch.cuda.empty_cache()

    print_metrics(metrics)

    print("Finished evaluation.")