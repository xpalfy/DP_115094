import os
import shutil

SOURCE_DIR = "../dataset/v4.4"
TARGET_DIR = "../dataset/v4.4_box"
COPY_IMAGES = True

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def polygon_to_box(coords):
    xs = coords[0::2]
    ys = coords[1::2]
    return min(xs), min(ys), max(xs), max(ys)

def convert_label_file(src_path, dst_path):
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

        new_lines.append(f"{cls} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

    ensure_dir(os.path.dirname(dst_path))
    with open(dst_path, "w") as f:
        f.writelines(new_lines)

splits = ["train", "val", "test"]

for split in splits:
    src_split_dir = os.path.join(SOURCE_DIR, split)
    dst_split_dir = os.path.join(TARGET_DIR, split)

    src_label_dir = os.path.join(src_split_dir, "labels")
    src_img_dir = os.path.join(src_split_dir, "images")

    dst_label_dir = os.path.join(dst_split_dir, "labels")
    dst_img_dir = os.path.join(dst_split_dir, "images")

    ensure_dir(dst_label_dir)
    ensure_dir(dst_img_dir)

    if COPY_IMAGES:
        for file in os.listdir(src_img_dir):
            if not os.path.isfile(os.path.join(src_img_dir, file)):
                continue
            shutil.copy2(os.path.join(src_img_dir, file), os.path.join(dst_img_dir, file))

    for file in os.listdir(src_label_dir):
        if file.endswith(".txt"):
            src_file = os.path.join(src_label_dir, file)
            dst_file = os.path.join(dst_label_dir, file)
            convert_label_file(src_file, dst_file)
