import os
import random
import cv2
import matplotlib.pyplot as plt

NUM_IMAGES = 5
IMAGE_DIR = "../../dataset/v6.5/train/images"
LABEL_DIR = "../../dataset/v6.5/train/labels"

image_files = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

if len(image_files) == 0:
    raise FileNotFoundError(f"No images found in {IMAGE_DIR}")

sampled_images = random.sample(image_files, min(NUM_IMAGES, len(image_files)))


def draw_boxes(image_path, label_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Can't read image {image_path}")

    h, w, _ = img.shape

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                cls = parts[0]
                x_center, y_center, bw, bh = map(float, parts[1:])

                x_center *= w
                y_center *= h
                bw *= w
                bh *= h

                x_min = int(x_center - bw / 2)
                y_min = int(y_center - bh / 2)
                x_max = int(x_center + bw / 2)
                y_max = int(y_center + bh / 2)

                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

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

    annotated_img = draw_boxes(img_path, label_path)
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

    ax.imshow(annotated_img)
    ax.set_title(img_file, fontsize=9)
    ax.axis("off")

plt.tight_layout()
plt.show()
