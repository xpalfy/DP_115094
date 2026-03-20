import os
import json
import random
import cv2
import matplotlib.pyplot as plt


# ===================================================
# CONFIG
# ===================================================

NUM_IMAGES = 5

IMAGE_DIR = "../../dataset/v6.5_coco/train/images"
ANNOTATION_FILE = "../../dataset/v6.5_coco/train/_annotations.coco.json"


# ===================================================
# LOAD COCO
# ===================================================

def load_coco(annotation_path):
    """Load COCO annotation file."""
    with open(annotation_path, "r") as f:
        coco = json.load(f)

    images = coco["images"]
    annotations = coco["annotations"]
    categories = {c["id"]: c["name"] for c in coco["categories"]}

    return images, annotations, categories


def build_annotation_map(annotations):
    """Map image_id -> annotations list."""
    ann_map = {}

    for ann in annotations:
        ann_map.setdefault(ann["image_id"], []).append(ann)

    return ann_map


# ===================================================
# DRAWING
# ===================================================

def draw_boxes(image_info, ann_map, categories):
    """Draw bounding boxes on image."""

    img_path = os.path.join(IMAGE_DIR, image_info["file_name"])
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"Can't read image {img_path}")

    image_id = image_info["id"]

    if image_id in ann_map:
        for ann in ann_map[image_id]:

            x, y, w, h = ann["bbox"]
            cls_id = ann["category_id"]
            cls_name = categories.get(cls_id, str(cls_id))

            x_min = int(x)
            y_min = int(y)
            x_max = int(x + w)
            y_max = int(y + h)

            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            cv2.putText(
                img,
                cls_name,
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
    """Display random annotated images."""

    sampled_images = random.sample(images, min(NUM_IMAGES, len(images)))

    fig, axes = plt.subplots(
        1,
        len(sampled_images),
        figsize=(4 * len(sampled_images), 5)
    )

    if len(sampled_images) == 1:
        axes = [axes]

    for ax, img_info in zip(axes, sampled_images):

        annotated_img = draw_boxes(img_info, ann_map, categories)
        annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

        ax.imshow(annotated_img)
        ax.set_title(img_info["file_name"], fontsize=9)
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
