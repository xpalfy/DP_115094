import os
import json
import yaml
import shutil
from pathlib import Path
from PIL import Image

DATA_YAML = "../../../dataset/v6.4/data.yaml"
OUTPUT_SUFFIX = "_coco_seg"


def load_yaml():
    with open(DATA_YAML, "r") as f:
        return yaml.safe_load(f)


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

        images.append({
            "id": image_id,
            "file_name": img_file,
            "width": width,
            "height": height
        })

        label_path = labels_dir / (Path(img_file).stem + ".txt")

        if label_path.exists():

            with open(label_path) as f:
                lines = f.readlines()

            for line in lines:

                parts = line.strip().split()

                class_id = int(parts[0])

                coords = list(map(float, parts[1:]))

                polygon = []

                xs = []
                ys = []

                for i in range(0, len(coords), 2):

                    x = coords[i] * width
                    y = coords[i + 1] * height

                    polygon.extend([x, y])

                    xs.append(x)
                    ys.append(y)

                x_min = min(xs)
                y_min = min(ys)

                bbox_w = max(xs) - x_min
                bbox_h = max(ys) - y_min

                annotations.append({
                    "id": ann_id,
                    "image_id": image_id,
                    "category_id": class_id + 1,
                    "segmentation": [polygon],
                    "bbox": [x_min, y_min, bbox_w, bbox_h],
                    "area": bbox_w * bbox_h,
                    "iscrowd": 0
                })

                ann_id += 1

        image_id += 1

    categories = [
        {"id": i + 1, "name": name}
        for i, name in enumerate(classes)
    ]

    coco = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    os.makedirs(out_split, exist_ok=True)

    with open(out_split / "annotations.json", "w") as f:
        json.dump(coco, f)

    print(f"{split_name} converted ({len(images)} images)")


def main():

    cfg = load_yaml()

    dataset_root = cfg["path"]
    classes = cfg["names"]

    output_root = dataset_root + OUTPUT_SUFFIX

    splits = []

    for key in ["train", "val", "test"]:
        if key in cfg:
            splits.append(cfg[key])

    for split in splits:
        convert_split(dataset_root, split, output_root, classes)

    print("\nPolygon dataset conversion finished.")
    print("Output:", output_root)


if __name__ == "__main__":
    main()