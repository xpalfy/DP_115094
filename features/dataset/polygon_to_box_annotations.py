import os
import shutil


# ===================================================
# CONFIG
# ===================================================

SOURCE_DIR = "../../dataset/v6.4"
TARGET_DIR = "../../dataset/v6.5"

COPY_IMAGES = True

SPLITS = ["train", "val", "test"]


# ===================================================
# HELPERS
# ===================================================

def ensure_dir(path):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def polygon_to_box(coords):
    """Convert polygon (x1,y1,x2,y2,...) to bounding box."""
    xs = coords[0::2]
    ys = coords[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def convert_label_file(src_path, dst_path):
    """Convert one label file from polygon → YOLO bbox."""
    with open(src_path, "r") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        cls = parts[0]
        coords = list(map(float, parts[1:]))

        x_min, y_min, x_max, y_max = polygon_to_box(coords)

        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        w = x_max - x_min
        h = y_max - y_min

        new_lines.append(
            f"{cls} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n"
        )

    ensure_dir(os.path.dirname(dst_path))

    with open(dst_path, "w") as f:
        f.writelines(new_lines)


def copy_images(src_dir, dst_dir):
    """Copy all images."""
    for file in os.listdir(src_dir):
        src = os.path.join(src_dir, file)
        dst = os.path.join(dst_dir, file)

        if os.path.isfile(src):
            shutil.copy2(src, dst)


# ===================================================
# MAIN
# ===================================================

def process_split(split):
    """Process one dataset split."""
    src_split = os.path.join(SOURCE_DIR, split)
    dst_split = os.path.join(TARGET_DIR, split)

    src_img_dir = os.path.join(src_split, "images")
    src_lbl_dir = os.path.join(src_split, "labels")

    dst_img_dir = os.path.join(dst_split, "images")
    dst_lbl_dir = os.path.join(dst_split, "labels")

    ensure_dir(dst_img_dir)
    ensure_dir(dst_lbl_dir)

    if COPY_IMAGES:
        copy_images(src_img_dir, dst_img_dir)

    for file in os.listdir(src_lbl_dir):
        if not file.endswith(".txt"):
            continue

        src_file = os.path.join(src_lbl_dir, file)
        dst_file = os.path.join(dst_lbl_dir, file)

        convert_label_file(src_file, dst_file)


if __name__ == "__main__":
    for split in SPLITS:
        process_split(split)
