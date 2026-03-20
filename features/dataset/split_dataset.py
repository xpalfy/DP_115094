import os
import shutil
import random


# ===================================================
# CONFIG
# ===================================================

INPUT_DATASET = "../../dataset/v7.2"
OUTPUT_DATASET = "../../dataset/v7.4"

IMAGES_DIR = os.path.join(INPUT_DATASET, "images")
LABELS_DIR = os.path.join(INPUT_DATASET, "labels")

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SPLITS = ["train", "val", "test"]


# ===================================================
# VALIDATION
# ===================================================

assert abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) < 1e-6, \
    "Split ratios must sum to 1."


# ===================================================
# HELPERS
# ===================================================

def ensure_dirs():
    """Create output directory structure."""
    for split in SPLITS:
        os.makedirs(os.path.join(OUTPUT_DATASET, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(OUTPUT_DATASET, split, "labels"), exist_ok=True)


def get_images():
    """Collect all image files."""
    return [
        f for f in os.listdir(IMAGES_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]


def split_dataset(files):
    """Split dataset into train/val/test."""
    random.shuffle(files)

    total = len(files)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    return {
        "train": files[:train_end],
        "val": files[train_end:val_end],
        "test": files[val_end:]
    }


def copy_sample(split, img_file):
    """Copy one image + label."""
    base = os.path.splitext(img_file)[0]

    src_img = os.path.join(IMAGES_DIR, img_file)
    src_lbl = os.path.join(LABELS_DIR, base + ".txt")

    dst_img = os.path.join(OUTPUT_DATASET, split, "images", img_file)
    dst_lbl = os.path.join(OUTPUT_DATASET, split, "labels", base + ".txt")

    shutil.copy2(src_img, dst_img)

    if os.path.exists(src_lbl):
        shutil.copy2(src_lbl, dst_lbl)


def process_split(split, files):
    """Process one split."""
    print(f"\nProcessing {split} split ({len(files)} images)")

    for img_file in files:
        copy_sample(split, img_file)


# ===================================================
# MAIN
# ===================================================

def main():
    ensure_dirs()

    image_files = get_images()
    split_map = split_dataset(image_files)

    for split, files in split_map.items():
        process_split(split, files)

    print("\nDataset split completed")
    print(f"Train images: {len(split_map['train'])}")
    print(f"Validation images: {len(split_map['val'])}")
    print(f"Test images: {len(split_map['test'])}")


if __name__ == "__main__":
    main()
