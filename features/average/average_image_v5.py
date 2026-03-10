import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from tqdm import tqdm

# ===== Load data.yaml =====
DATA_YAML_PATH = "../../dataset/v5/data.yaml"

if not os.path.exists(DATA_YAML_PATH):
    raise FileNotFoundError(f"data.yaml not found at: {DATA_YAML_PATH}")

with open(DATA_YAML_PATH, "r", encoding="utf-8") as f:
    data_cfg = yaml.safe_load(f)

# ===== Paths from YAML =====
BASE_DIR = data_cfg.get("path")
IMAGES_DIR_NAME = data_cfg.get("images", "images")
LABELS_DIR_NAME = data_cfg.get("labels", "labels")

if BASE_DIR is None:
    raise ValueError("'path' field missing from data.yaml")

IMAGE_DIR = os.path.join(BASE_DIR, IMAGES_DIR_NAME)
LABEL_DIR = os.path.join(BASE_DIR, LABELS_DIR_NAME)

# ===== Classes from YAML =====
CLASS_NAMES = data_cfg.get("names", [])
NUM_CLASSES = data_cfg.get("nc", len(CLASS_NAMES))

if not CLASS_NAMES or NUM_CLASSES != len(CLASS_NAMES):
    raise ValueError("Mismatch or missing 'names' / 'nc' in data.yaml")

# ===== Config =====
TARGET_SIZE = (128, 128)

# ===== Accumulators =====
class_sums = defaultdict(
    lambda: np.zeros((TARGET_SIZE[1], TARGET_SIZE[0], 3), dtype=np.float64)
)
class_counts = defaultdict(int)

# ===== Image list =====
image_files = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

if not image_files:
    raise FileNotFoundError(f"No images found in: {IMAGE_DIR}")

# ===== Main loop =====
for img_file in tqdm(image_files, desc="Processing images"):
    img_path = os.path.join(IMAGE_DIR, img_file)
    label_path = os.path.join(LABEL_DIR, os.path.splitext(img_file)[0] + ".txt")

    img = cv2.imread(img_path)
    if img is None or not os.path.exists(label_path):
        continue

    h, w, _ = img.shape

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            cls = int(parts[0])
            if cls >= NUM_CLASSES:
                continue

            coords = list(map(float, parts[1:]))

            polygon = []
            for i in range(0, len(coords), 2):
                x = int(coords[i] * w)
                y = int(coords[i + 1] * h)
                polygon.append([x, y])

            polygon = np.array(polygon, np.int32)

            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.fillPoly(mask, [polygon], 255)

            masked = cv2.bitwise_and(img, img, mask=mask)

            x_min, y_min = polygon[:, 0].min(), polygon[:, 1].min()
            x_max, y_max = polygon[:, 0].max(), polygon[:, 1].max()

            if x_max <= x_min or y_max <= y_min:
                continue

            cropped = masked[y_min:y_max, x_min:x_max]
            if cropped.size == 0:
                continue

            resized = cv2.resize(cropped, TARGET_SIZE)

            class_sums[cls] += resized.astype(np.float64)
            class_counts[cls] += 1

# ===== Save average images =====
OUTPUT_DIR = "../../backend/average_images_v5"
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

# ===== Visualization =====
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
