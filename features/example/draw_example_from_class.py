import os
import glob
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt


# ===================================================
# CONFIG
# ===================================================

BASE_DIR = "../../dataset/v6"

IMAGE_DIR = os.path.join(BASE_DIR, "images")
LABEL_DIR = os.path.join(BASE_DIR, "labels")
NOTES_PATH = os.path.join(BASE_DIR, "notes.json")


# ===================================================
# LOAD DATA
# ===================================================

def load_class_map(notes_path):
    """Load class id -> name mapping from notes.json."""
    with open(notes_path, "r", encoding="utf-8") as f:
        notes = json.load(f)

    return {str(cat["id"]): cat["name"] for cat in notes["categories"]}


# ===================================================
# HELPERS
# ===================================================

def find_image_for_label(label_path):
    """Find matching image (.jpg or .png) for a label file."""
    base = os.path.basename(label_path).replace(".txt", "")

    for ext in [".jpg", ".png"]:
        img_path = os.path.join(IMAGE_DIR, base + ext)
        if os.path.exists(img_path):
            return img_path

    return None


def get_polygon(parts):
    """Convert YOLO polygon coords to numpy array."""
    coords = list(map(float, parts[1:]))
    return np.array(coords).reshape(-1, 2)


def normalize_to_pixels(polygon, w, h):
    """Convert normalized coords → pixel coords."""
    poly_px = np.zeros_like(polygon)
    poly_px[:, 0] = polygon[:, 0] * w
    poly_px[:, 1] = polygon[:, 1] * h
    return poly_px.astype(np.int32)


def extract_object(img, polygon_px):
    """Mask + crop object from image."""
    h, w = img.shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon_px], 255)

    masked = cv2.bitwise_and(img, img, mask=mask)

    x_min, y_min = np.min(polygon_px, axis=0)
    x_max, y_max = np.max(polygon_px, axis=0)

    return masked[y_min:y_max, x_min:x_max]


# ===================================================
# EXAMPLE COLLECTION
# ===================================================

def collect_examples():
    """Collect one example per class."""
    examples = {}

    for label_path in glob.glob(os.path.join(LABEL_DIR, "*.txt")):
        with open(label_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue

                cls = parts[0]

                if cls in examples:
                    continue

                polygon = get_polygon(parts)
                img_path = find_image_for_label(label_path)

                if img_path:
                    examples[cls] = (img_path, polygon)

    return examples


# ===================================================
# VISUALIZATION
# ===================================================

def show_examples(examples, class_map):
    """Display cropped object examples."""
    for cls_id, (img_path, polygon_norm) in examples.items():

        class_name = class_map.get(cls_id, "UNKNOWN")

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w = img.shape[:2]

        polygon_px = normalize_to_pixels(polygon_norm, w, h)

        crop = extract_object(img, polygon_px)

        plt.figure(figsize=(4, 4))
        plt.imshow(crop)
        plt.title(f"Class {cls_id} - {class_name}")
        plt.axis("off")
        plt.show()


# ===================================================
# MAIN
# ===================================================

def main():
    CLASS_MAP = load_class_map(NOTES_PATH)
    examples = collect_examples()
    show_examples(examples, CLASS_MAP)

if __name__ == "__main__":
    main()
