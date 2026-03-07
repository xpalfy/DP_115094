import os
import random
import json
import cv2
import matplotlib.pyplot as plt
import numpy as np

NUM_IMAGES = 6

IMAGE_DIR = "../../../dataset/v6.4_coco_seg/train/images"
ANNOTATION_FILE = "../../../dataset/v6.4_coco_seg/train/annotations.json"

with open(ANNOTATION_FILE, "r") as f:
    coco = json.load(f)

images = coco["images"]
annotations = coco["annotations"]
categories = {cat["id"]: cat["name"] for cat in coco["categories"]}

image_id_to_annotations = {}
for ann in annotations:
    image_id_to_annotations.setdefault(ann["image_id"], []).append(ann)

sampled_images = random.sample(images, min(NUM_IMAGES, len(images)))


def draw_polygons(image_info):
    img_path = os.path.join(IMAGE_DIR, image_info["file_name"])
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"Could not read image: {img_path}")

    anns = image_id_to_annotations.get(image_info["id"], [])

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


fig, axes = plt.subplots(1, len(sampled_images), figsize=(4 * len(sampled_images), 5))

if len(sampled_images) == 1:
    axes = [axes]

for ax, img_info in zip(axes, sampled_images):
    annotated_img = draw_polygons(img_info)
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

    ax.imshow(annotated_img)
    ax.set_title(img_info["file_name"], fontsize=10)
    ax.axis("off")

plt.tight_layout()
plt.show()