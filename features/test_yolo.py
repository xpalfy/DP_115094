from ultralytics import YOLO
import numpy as np
import os
import cv2
import torch

# =========================
# CONFIG
# =========================
MODEL_PATH = "../backend/runs/combined/yolo11/detect/train_yolo11m/v1_yolo11m/weights/best.pt"
DATA_YAML = "data.yaml"

TEST_IMAGES = "../dataset/v6.5/test/images"
OUTPUT_DIR = "../backend/runs/yolo_test_predictions"

IMG_SIZE = 1024
DEVICE = "cuda"
CONF = 0.5

os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":

    if not os.path.exists(MODEL_PATH):
        print(f"Weights not found: {MODEL_PATH}")
        exit()

    print(f"\n=== Loading {MODEL_PATH} ===")

    model = YOLO(MODEL_PATH)

    print("Model loaded\n")

    # =========================
    # EVALUATION (metrics)
    # =========================
    metrics = model.val(
        data=DATA_YAML,
        split="test",
        imgsz=IMG_SIZE,
        conf=CONF,
        device=DEVICE
    )

    torch.cuda.empty_cache()

    # =========================
    # PRINT RESULTS
    # =========================
    print("\n================ RESULTS ================\n")

    if hasattr(metrics, "box"):
        print("BOX METRICS")
        print(f"Precision:  {float(np.mean(metrics.box.p)):.4f}")
        print(f"Recall:     {float(np.mean(metrics.box.r)):.4f}")
        print(f"mAP@50:     {metrics.box.map50:.4f}")
        print(f"mAP@50-95:  {metrics.box.map:.4f}")
        print()

    if hasattr(metrics, "seg"):
        print("MASK METRICS")
        print(f"Precision:  {float(np.mean(metrics.seg.p)):.4f}")
        print(f"Recall:     {float(np.mean(metrics.seg.r)):.4f}")
        print(f"mAP@50:     {metrics.seg.map50:.4f}")
        print(f"mAP@50-95:  {metrics.seg.map:.4f}")
        print()

    print("=========================================\n")

    # =========================
    # SAVE PREDICTION IMAGES
    # =========================
    images = [
        f for f in os.listdir(TEST_IMAGES)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print("Saving prediction images:", len(images))

    for img_name in images:

        img_path = os.path.join(TEST_IMAGES, img_name)

        results = model.predict(
            img_path,
            imgsz=IMG_SIZE,
            conf=CONF,
            device=DEVICE,
            verbose=False
        )

        result = results[0]
        result = result.cpu()
        annotated = result.plot()

        save_path = os.path.join(OUTPUT_DIR, img_name)
        cv2.imwrite(save_path, annotated)

        print("Saved:", img_name)

    print("\nFinished testing.")
    print("Images saved to:", OUTPUT_DIR)