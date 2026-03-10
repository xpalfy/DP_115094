import os
import glob
import yaml
from collections import Counter
import matplotlib.pyplot as plt

# --- Load data.yaml ---
DATA_YAML_PATH = "../../dataset/v6/data.yaml"

if not os.path.exists(DATA_YAML_PATH):
    raise FileNotFoundError(f"data.yaml not found at: {DATA_YAML_PATH}")

with open(DATA_YAML_PATH, "r", encoding="utf-8") as f:
    data_cfg = yaml.safe_load(f)

# --- Read paths from YAML ---
BASE_DIR = data_cfg.get("path")
IMAGES_DIR_NAME = data_cfg.get("images", "images")
LABELS_DIR_NAME = data_cfg.get("labels", "labels")

if BASE_DIR is None:
    raise ValueError("'path' field missing from data.yaml")

IMAGES_DIR = os.path.join(BASE_DIR, IMAGES_DIR_NAME)
LABEL_DIR = os.path.join(BASE_DIR, LABELS_DIR_NAME)

# --- Read class names ---
CLASS_NAMES = data_cfg.get("names", [])
if not CLASS_NAMES:
    raise ValueError("No class names found in data.yaml ('names' field missing).")

# id -> class name mapping
CLASS_MAP = {str(i): name for i, name in enumerate(CLASS_NAMES)}

# --- Check directories ---
if not os.path.exists(IMAGES_DIR):
    raise FileNotFoundError(f"Images directory not found: {IMAGES_DIR}")

if not os.path.exists(LABEL_DIR):
    raise FileNotFoundError(f"Labels directory not found: {LABEL_DIR}")

print(f"\nDataset base path: {BASE_DIR}")
print(f"Images directory:  {IMAGES_DIR}")
print(f"Labels directory:  {LABEL_DIR}")

# --- Count class instances ---
class_counts = Counter()

for lbl_path in glob.glob(os.path.join(LABEL_DIR, "*.txt")):
    with open(lbl_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                cls_id = parts[0]
                class_counts[cls_id] += 1

# --- Print results ---
print("\nClass instance count:\n")
for cls_id in sorted(class_counts.keys(), key=lambda x: int(x)):
    class_name = CLASS_MAP.get(cls_id, "UNKNOWN")
    print(f"Class {cls_id:>2} ({class_name}): {class_counts[cls_id]}")

print("\nTotal objects:", sum(class_counts.values()))

# --- Prepare plot data ---
labels = [
    f"{cid} - {CLASS_MAP.get(cid, 'UNKNOWN')}"
    for cid in sorted(class_counts.keys(), key=lambda x: int(x))
]

counts = [
    class_counts[cid]
    for cid in sorted(class_counts.keys(), key=lambda x: int(x))
]

# --- Plot ---
plt.figure(figsize=(14, 7))

plt.bar(labels, counts)

# Axis labels (bigger + bold)
plt.xlabel("Class", fontsize=14, fontweight="bold")
plt.ylabel("Count", fontsize=14, fontweight="bold")

# Title (bigger + bold + margin)
plt.title(
    "Object Count per Class — Combined Dataset (v6)",
    fontsize=18,
    fontweight="bold",
    pad=20
)

# Tick labels
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(fontsize=12)

# Grid styling
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
