from ultralytics import YOLO
import numpy as np
import os
import cv2
import torch

# SAHI
from sahi.predict import get_sliced_prediction
from sahi import AutoDetectionModel

# =========================
# CONFIG
# =========================
MODEL_PATH = "../backend/runs/combined/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt"
DATA_YAML = "data.yaml"

TEST_IMAGES = "../dataset/test_eugen"
OUTPUT_DIR = "../backend/runs/yolo_test_eugen"

IMG_SIZE = 1024
DEVICE = "cuda"
CONF = 0.75

USE_SAHI = True

os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":

    if not os.path.exists(MODEL_PATH):
        print(f"Weights not found: {MODEL_PATH}")
        exit()

    print(f"\n=== Loading {MODEL_PATH} ===")

    model = YOLO(MODEL_PATH)

    print("Model loaded\n")

    # =========================
    # SAHI INIT
    # =========================
    if USE_SAHI:
        print("Initializing SAHI model...")
        sahi_model = AutoDetectionModel.from_pretrained(
            model_type="ultralytics",
            model_path=MODEL_PATH,
            confidence_threshold=CONF,
            device=DEVICE
        )

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

        if USE_SAHI:
            result = get_sliced_prediction(
                img_path,
                sahi_model
            )

            image = cv2.imread(img_path)

            for obj in result.object_prediction_list:
                bbox = obj.bbox

                x1 = int(bbox.minx)
                y1 = int(bbox.miny)
                x2 = int(bbox.maxx)
                y2 = int(bbox.maxy)

                class_name = obj.category.name

                if obj.mask is not None:
                    mask = obj.mask.bool_mask.astype(bool)
                    colored_mask = np.zeros_like(image)
                    colored_mask[mask] = (0, 0, 255)
                    image = cv2.addWeighted(image, 1.0, colored_mask, 0.4, 0)

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

                (w, h), _ = cv2.getTextSize(
                    class_name,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    2
                )

                y_text = max(y1, h + 8)

                cv2.rectangle(
                    image,
                    (x1, y_text - h - 8),
                    (x1 + w, y_text),
                    (0, 0, 0),
                    -1
                )

                cv2.putText(
                    image,
                    class_name,
                    (x1, y_text - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

            save_path = os.path.join(OUTPUT_DIR, img_name)
            cv2.imwrite(save_path, image)

            print("Saved (SAHI):", img_name)

        else:
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