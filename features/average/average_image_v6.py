import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from tqdm import tqdm


# ===================================================
# CONFIG
# ===================================================

DATA_YAML_PATH = "../../dataset/v6/data.yaml"
TARGET_SIZE = (128, 128)
OUTPUT_DIR = "../../backend/average_images_v6"


# ===================================================
# LOAD YAML
# ===================================================

def load_dataset_config(path):
    """Load dataset configuration from YAML."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"data.yaml not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_paths(cfg):
    """Resolve dataset paths."""
    base_dir = cfg.get("path")
    if base_dir is None:
        raise ValueError("'path' field missing from data.yaml")

    image_dir = os.path.join(base_dir, cfg.get("images", "images"))
    label_dir = os.path.join(base_dir, cfg.get("labels", "labels"))

    return image_dir, label_dir


def load_classes(cfg):
    """Load class names and validate."""
    class_names = cfg.get("names", [])
    num_classes = cfg.get("nc", len(class_names))

    if not class_names or num_classes != len(class_names):
        raise ValueError("Mismatch or missing 'names' / 'nc' in data.yaml")

    return class_names, num_classes


# ===================================================
# HELPERS
# ===================================================

def get_image_files(image_dir):
    """List image files."""
    files = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not files:
        raise FileNotFoundError(f"No images found in: {image_dir}")

    return files


def load_image_and_label(image_dir, label_dir, filename):
    """Load image and label path."""
    img_path = os.path.join(image_dir, filename)
    label_path = os.path.join(label_dir, os.path.splitext(filename)[0] + ".txt")

    img = cv2.imread(img_path)

    if img is None or not os.path.exists(label_path):
        return None, None

    return img, label_path


def polygon_from_coords(coords, w, h):
    """Convert normalized coords to pixel polygon."""
    polygon = [
        [int(coords[i] * w), int(coords[i + 1] * h)]
        for i in range(0, len(coords), 2)
    ]
    return np.array(polygon, np.int32)


def extract_object(img, polygon):
    """Mask and crop object from image."""
    h, w, _ = img.shape

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 255)

    masked = cv2.bitwise_and(img, img, mask=mask)

    x_min, y_min = polygon[:, 0].min(), polygon[:, 1].min()
    x_max, y_max = polygon[:, 0].max(), polygon[:, 1].max()

    if x_max <= x_min or y_max <= y_min:
        return None

    cropped = masked[y_min:y_max, x_min:x_max]

    if cropped.size == 0:
        return None

    return cv2.resize(cropped, TARGET_SIZE)


# ===================================================
# MAIN
# ===================================================

def main():

    # ===================================================
    # LOAD DATA
    # ===================================================

    cfg = load_dataset_config(DATA_YAML_PATH)
    IMAGE_DIR, LABEL_DIR = resolve_paths(cfg)
    CLASS_NAMES, NUM_CLASSES = load_classes(cfg)

    image_files = get_image_files(IMAGE_DIR)

    class_sums = defaultdict(
        lambda: np.zeros((TARGET_SIZE[1], TARGET_SIZE[0], 3), dtype=np.float64)
    )
    class_counts = defaultdict(int)


    for img_file in tqdm(image_files, desc="Processing images"):

        img, label_path = load_image_and_label(IMAGE_DIR, LABEL_DIR, img_file)
        if img is None:
            continue

        h, w, _ = img.shape

        with open(label_path, "r") as f:
            for line in f:

                parts = line.strip().split()

                if len(parts) < 7:
                    continue

                cls = int(parts[0])
                if cls >= NUM_CLASSES:
                    continue

                coords = list(map(float, parts[1:]))
                polygon = polygon_from_coords(coords, w, h)

                resized = extract_object(img, polygon)
                if resized is None:
                    continue

                class_sums[cls] += resized.astype(np.float64)
                class_counts[cls] += 1


    # ===================================================
    # SAVE AVERAGE IMAGES
    # ===================================================

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    average_images = {}

    for cls in range(NUM_CLASSES):

        if class_counts[cls] == 0:
            continue

        avg_img = (class_sums[cls] / class_counts[cls]).astype(np.uint8)
        average_images[cls] = avg_img

        class_name = CLASS_NAMES[cls]
        save_path = os.path.join(OUTPUT_DIR, f"average_{class_name}.png")

        cv2.imwrite(save_path, avg_img)
        print(f"Saved: {save_path}")


    # ===================================================
    # VISUALIZATION
    # ===================================================

    cols = 5
    rows = int(np.ceil(NUM_CLASSES / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes = axes.flatten()

    for i in range(NUM_CLASSES):

        ax = axes[i]

        if i in average_images:
            img_rgb = cv2.cvtColor(average_images[i], cv2.COLOR_BGR2RGB)
            ax.imshow(img_rgb)
            ax.set_title(f"{CLASS_NAMES[i]} (n={class_counts[i]})", fontsize=12)
        else:
            ax.text(0.5, 0.5, "N/A", ha="center", va="center", fontsize=14)

        ax.axis("off")


    for j in range(NUM_CLASSES, len(axes)):
        axes[j].axis("off")


    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
