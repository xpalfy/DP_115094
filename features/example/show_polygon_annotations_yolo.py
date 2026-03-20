import os
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np


# ===================================================
# CONFIG
# ===================================================

NUM_IMAGES = 6

IMAGE_DIR = "../../dataset/v6/images"
LABEL_DIR = "../../dataset/v6/labels"


# ===================================================
# HELPERS
# ===================================================

def get_image_files(directory):
    """List valid image files."""
    return [
        f for f in os.listdir(directory)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]


def get_label_path(image_file):
    """Get corresponding label path."""
    return os.path.join(
        LABEL_DIR,
        os.path.splitext(image_file)[0] + ".txt"
    )


def yolo_polygon_to_pixels(coords, w, h):
    """Convert normalized polygon → pixel coordinates."""
    polygon = []

    for i in range(0, len(coords), 2):
        x = int(coords[i] * w)
        y = int(coords[i + 1] * h)
        polygon.append([x, y])

    return np.array(polygon, np.int32).reshape((-1, 1, 2))


# ===================================================
# DRAWING
# ===================================================

def draw_polygons(image_path, label_path):
    """Draw YOLO polygon annotations on image."""

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w, _ = img.shape

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()

                if len(parts) < 3:
                    continue

                cls = parts[0]
                coords = list(map(float, parts[1:]))

                polygon = yolo_polygon_to_pixels(coords, w, h)

                cv2.polylines(
                    img,
                    [polygon],
                    isClosed=True,
                    color=(0, 255, 0),
                    thickness=2
                )

                x_min = polygon[:, 0, 0].min()
                y_min = polygon[:, 0, 1].min()

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


# ===================================================
# VISUALIZATION
# ===================================================

def show_samples(image_files):
    """Display random polygon samples."""

    sampled = random.sample(image_files, min(NUM_IMAGES, len(image_files)))

    fig, axes = plt.subplots(
        1,
        len(sampled),
        figsize=(4 * len(sampled), 5)
    )

    if len(sampled) == 1:
        axes = [axes]

    for ax, img_file in zip(axes, sampled):

        img_path = os.path.join(IMAGE_DIR, img_file)
        label_path = get_label_path(img_file)

        annotated = draw_polygons(img_path, label_path)
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        ax.imshow(annotated)
        ax.set_title(img_file, fontsize=10)
        ax.axis("off")

    plt.tight_layout()
    plt.show()


# ===================================================
# MAIN
# ===================================================

def main():
    image_files = get_image_files(IMAGE_DIR)

    if not image_files:
        raise FileNotFoundError(f"The directory {IMAGE_DIR} contains no image files.")

    show_samples(image_files)

if __name__ == "__main__":
    main()
