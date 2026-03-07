import os
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np

NUM_IMAGES = 6
IMAGE_DIR = "../../../dataset/v6/images"
LABEL_DIR = "../../../dataset/v6/labels"

image_files = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(('.jpg', '.png', '.jpeg'))
]

if len(image_files) == 0:
    raise FileNotFoundError(f"The directory {IMAGE_DIR} contains no image files.")

sampled_images = random.sample(image_files, min(NUM_IMAGES, len(image_files)))


def draw_polygons(image_path, label_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w, _ = img.shape

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) < 3:
                    continue

                cls = parts[0]
                coords = list(map(float, parts[1:]))

                polygon = []
                for i in range(0, len(coords), 2):
                    x = int(coords[i] * w)
                    y = int(coords[i + 1] * h)
                    polygon.append([x, y])

                polygon = np.array(polygon, np.int32).reshape((-1, 1, 2))

                cv2.polylines(img, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

                x_min, y_min = polygon[:, 0, 0].min(), polygon[:, 0, 1].min()
                cv2.putText(
                    img,
                    f"Class {cls}",
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

for ax, img_file in zip(axes, sampled_images):
    img_path = os.path.join(IMAGE_DIR, img_file)
    label_path = os.path.join(LABEL_DIR, os.path.splitext(img_file)[0] + ".txt")

    annotated_img = draw_polygons(img_path, label_path)
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

    ax.imshow(annotated_img)
    ax.set_title(img_file, fontsize=10)
    ax.axis("off")

plt.tight_layout()
plt.show()
