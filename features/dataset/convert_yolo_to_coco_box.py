import os
import json
import yaml
import shutil
from pathlib import Path
from PIL import Image


# ===================================================
# CONFIG
# ===================================================

DATA_YAML = "../../dataset/v7.5/data.yaml"
OUTPUT_SUFFIX = "_coco"


# ===================================================
# LOAD CONFIG
# ===================================================

def load_yaml():
    """Load dataset YAML config."""
    with open(DATA_YAML, "r") as f:
        return yaml.safe_load(f)


# ===================================================
# CONVERSIONS
# ===================================================

def yolo_to_coco_bbox(parts, width, height):
    """Convert YOLO bbox → COCO bbox."""
    class_id = int(parts[0])

    x_center = float(parts[1])
    y_center = float(parts[2])
    w = float(parts[3])
    h = float(parts[4])

    bbox_w = w * width
    bbox_h = h * height

    x_min = (x_center * width) - bbox_w / 2
    y_min = (y_center * height) - bbox_h / 2

    return class_id, x_min, y_min, bbox_w, bbox_h


# ===================================================
# SPLIT CONVERSION
# ===================================================

def convert_split(dataset_root, split_name, output_root, classes):

    input_split = Path(dataset_root) / split_name
    images_dir = input_split / "images"
    labels_dir = input_split / "labels"

    out_split = Path(output_root) / split_name
    out_images = out_split / "images"

    os.makedirs(out_images, exist_ok=True)

    images = []
    annotations = []

    image_id = 1
    ann_id = 1

    for img_file in os.listdir(images_dir):

        if not img_file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        src_img = images_dir / img_file
        dst_img = out_images / img_file

        shutil.copy2(src_img, dst_img)

        with Image.open(src_img) as im:
            width, height = im.size

        # -------------------------
        # IMAGE ENTRY
        # -------------------------
        images.append({
            "id": image_id,
            "file_name": img_file,
            "width": width,
            "height": height
        })

        # -------------------------
        # LABELS
        # -------------------------
        label_path = labels_dir / (Path(img_file).stem + ".txt")

        if label_path.exists():
            with open(label_path) as f:
                for line in f:
                    parts = line.strip().split()

                    if len(parts) < 5:
                        continue

                    class_id, x_min, y_min, bw, bh = yolo_to_coco_bbox(
                        parts, width, height
                    )

                    annotations.append({
                        "id": ann_id,
                        "image_id": image_id,
                        "category_id": class_id,
                        "bbox": [x_min, y_min, bw, bh],
                        "area": bw * bh,
                        "iscrowd": 0
                    })

                    ann_id += 1

        image_id += 1

    # -------------------------
    # CATEGORIES
    # -------------------------
    categories = [
        {"id": i, "name": name}
        for i, name in enumerate(classes)
    ]

    coco = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    with open(out_split / "annotations.json", "w") as f:
        json.dump(coco, f)

    print(f"{split_name} converted ({len(images)} images)")


# ===================================================
# MAIN
# ===================================================

def main():

    cfg = load_yaml()

    dataset_root = cfg["path"]
    classes = cfg["names"]

    output_root = dataset_root + OUTPUT_SUFFIX

    splits = [cfg[k] for k in ["train", "val", "test"] if k in cfg]

    for split in splits:
        convert_split(dataset_root, split, output_root, classes)

    print("\nDataset conversion finished.")
    print("Output:", output_root)


if __name__ == "__main__":
    main()
