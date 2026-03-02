import os
import glob
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = "../../../dataset/v6"
IMAGE_DIR = os.path.join(BASE_DIR, "images")
LABEL_DIR = os.path.join(BASE_DIR, "labels")
NOTES_PATH = os.path.join(BASE_DIR, "notes.json")

with open(NOTES_PATH, "r", encoding="utf-8") as f:
    notes = json.load(f)

CLASS_MAP = {str(cat["id"]): cat["name"] for cat in notes["categories"]}

examples = {}

for label_path in glob.glob(os.path.join(LABEL_DIR, "*.txt")):
    with open(label_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            cls = parts[0]
            if cls in examples:
                continue  # already have example for this class

            coords = list(map(float, parts[1:]))
            polygon = np.array(coords).reshape(-1, 2)  # (x,y) pairs normalized

            img_name = os.path.basename(label_path).replace(".txt", ".jpg")
            img_path = os.path.join(IMAGE_DIR, img_name)

            if not os.path.exists(img_path):
                img_name = os.path.basename(label_path).replace(".txt", ".png")
                img_path = os.path.join(IMAGE_DIR, img_name)

            if os.path.exists(img_path):
                examples[cls] = (img_path, polygon)


for cls_id, (img_path, polygon_norm) in examples.items():
    class_name = CLASS_MAP.get(cls_id, "UNKNOWN")

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]

    # Convert normalized polygon → pixel coords
    polygon_px = np.zeros_like(polygon_norm)
    polygon_px[:, 0] = polygon_norm[:, 0] * w
    polygon_px[:, 1] = polygon_norm[:, 1] * h
    polygon_px = polygon_px.astype(np.int32)

    # Create empty mask
    mask = np.zeros((h, w), dtype=np.uint8)

    # Draw filled polygon mask
    cv2.fillPoly(mask, [polygon_px], 255)

    # Apply mask to image
    masked = cv2.bitwise_and(img, img, mask=mask)

    # Crop to polygon bounding box
    x_min, y_min = np.min(polygon_px, axis=0)
    x_max, y_max = np.max(polygon_px, axis=0)
    crop = masked[y_min:y_max, x_min:x_max]

    # Show result (only the letter)
    plt.figure(figsize=(4, 4))
    plt.imshow(crop)
    plt.title(f"Class {cls_id} - {class_name}")
    plt.axis("off")
    plt.show()
