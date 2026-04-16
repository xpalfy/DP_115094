from ultralytics import YOLO
import os
import cv2
import torch
import numpy as np


# ===================================================
# CONFIG
# ===================================================

MODEL_PATH = "../../backend/runs/combined/yolo12/detect/train_yolo12l/v1_yolo12l/weights/best.pt"
TEST_IMAGES = "../../dataset/v6.5/test/images"
OUTPUT_DIR = "./runs/yolo_test_predictions"

IMG_SIZE = 1024
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CONF = 0.5

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===================================================
# HELPERS
# ===================================================

def get_images(directory):
    return [
        f for f in os.listdir(directory)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]


def get_color(class_id):
    """Consistent color per class."""
    np.random.seed(class_id)
    return tuple(int(x) for x in np.random.randint(0, 255, 3))


def draw_predictions(image, result):
    img = image.copy()

    boxes = result.boxes
    masks = result.masks

    if boxes is None:
        return img

    is_segmentation = masks is not None and masks.data is not None and len(masks.data) > 0

    for i, box in enumerate(boxes):
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = get_color(cls_id)

        label = f"{result.names[cls_id]} {conf:.2f}"

        # ======================
        # SEGMENTATION
        # ======================
        if is_segmentation:
            mask = masks.data[i].cpu().numpy()
            mask = (mask > 0.5).astype(np.uint8)
            mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
            mask = mask.astype(bool)

            colored = np.zeros_like(img)
            colored[mask] = color

            img = cv2.addWeighted(img, 1.0, colored, 0.4, 0)

            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            y_text = max(y1, h + 10)

            cv2.rectangle(
                img,
                (x1, y_text - h - 8),
                (x1 + w + 4, y_text),
                color,
                -1
            )

            cv2.putText(
                img,
                label,
                (x1 + 2, y_text - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                lineType=cv2.LINE_AA
            )

        # ======================
        # DETECTION
        # ======================
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            y_text = max(y1, h + 10)

            cv2.rectangle(
                img,
                (x1, y_text - h - 8),
                (x1 + w + 4, y_text),
                color,
                -1
            )

            cv2.putText(
                img,
                label,
                (x1 + 2, y_text - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                lineType=cv2.LINE_AA
            )

    return img


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":

    if not os.path.exists(MODEL_PATH):
        print(f"Weights not found: {MODEL_PATH}")
        exit()

    print(f"\n=== Loading {MODEL_PATH} ===")

    model = YOLO(MODEL_PATH)

    print("Model loaded\n")

    images = get_images(TEST_IMAGES)
    print("Saving prediction images:", len(images))

    for img_name in images:

        img_path = os.path.join(TEST_IMAGES, img_name)

        image = cv2.imread(img_path)

        results = model.predict(
            image,
            imgsz=IMG_SIZE,
            conf=CONF,
            device=DEVICE,
            verbose=False
        )

        result = results[0].cpu()

        annotated = draw_predictions(image, result)

        save_path = os.path.join(OUTPUT_DIR, img_name)
        cv2.imwrite(save_path, annotated)

        print("Saved:", img_name)

    print("\nFinished testing.")
    print("Images saved to:", OUTPUT_DIR)