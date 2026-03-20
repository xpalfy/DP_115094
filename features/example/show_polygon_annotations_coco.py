import os
import random
import json
import cv2
import matplotlib.pyplot as plt
import numpy as np


# ===================================================
# CONFIG
# ===================================================

NUM_IMAGES = 6

IMAGE_DIR = "../../dataset/v6.4_coco_seg/train/images"
ANNOTATION_FILE = "../../dataset/v6.4_coco_seg/train/_annotations.coco.json"


# ===================================================
# LOAD COCO
# ===================================================

def load_coco(annotation_path):
    """Load COCO segmentation dataset."""
    with open(annotation_path, "r") as f:
        coco = json.load(f)

    images = coco["images"]
    annotations = coco["annotations"]
    categories = {c["id"]: c["name"] for c in coco["categories"]}

    return images, annotations, categories


def build_annotation_map(annotations):
    """Map image_id -> list of annotations."""
    ann_map = {}

    for ann in annotations:
        ann_map.setdefault(ann["image_id"], []).append(ann)

    return ann_map


# ===================================================
# DRAWING
# ===================================================

def draw_polygons(image_info, ann_map, categories):
    """Draw segmentation polygons on image."""

    img_path = os.path.join(IMAGE_DIR, image_info["file_name"])
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"Could not read image: {img_path}")

    anns = ann_map.get(image_info["id"], [])

    for ann in anns:
        category_name = categories.get(ann["category_id"], "unknown")

        for seg in ann["segmentation"]:
            polygon = np.array(seg).reshape(-1, 2).astype(np.int32)
            polygon = polygon.reshape((-1, 1, 2))

            cv2.polylines(img, [polygon], True, (0, 255, 0), 2)

            x_min = polygon[:, 0, 0].min()
            y_min = polygon[:, 0, 1].min()

            cv2.putText(
                img,
                category_name,
                (x_min, max(y_min - 5, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    return img


# ===================================================
# VISUALIZATION
# ===================================================

def show_samples(images, ann_map, categories):
    """Display random segmentation samples."""

    sampled = random.sample(images, min(NUM_IMAGES, len(images)))

    fig, axes = plt.subplots(
        1,
        len(sampled),
        figsize=(4 * len(sampled), 5)
    )

    if len(sampled) == 1:
        axes = [axes]

    for ax, img_info in zip(axes, sampled):

        annotated = draw_polygons(img_info, ann_map, categories)
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        ax.imshow(annotated)
        ax.set_title(img_info["file_name"], fontsize=10)
        ax.axis("off")

    plt.tight_layout()
    plt.show()


# ===================================================
# MAIN
# ===================================================

def main():
    images, annotations, categories = load_coco(ANNOTATION_FILE)
    ann_map = build_annotation_map(annotations)
    show_samples(images, ann_map, categories)

if __name__ == "__main__":
    main()
