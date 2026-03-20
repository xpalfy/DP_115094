import os
import random
import cv2
import matplotlib.pyplot as plt


# ===================================================
# CONFIG
# ===================================================

NUM_IMAGES = 5

IMAGE_DIR = "../../dataset/v6.5/train/images"
LABEL_DIR = "../../dataset/v6.5/train/labels"


# ===================================================
# HELPERS
# ===================================================

def get_image_files(directory):
    """List valid image files."""
    return [
        f for f in os.listdir(directory)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]


def get_label_path(image_file):
    """Get corresponding label file path."""
    return os.path.join(
        LABEL_DIR,
        os.path.splitext(image_file)[0] + ".txt"
    )


def yolo_to_bbox(parts, w, h):
    """Convert YOLO format → pixel bbox."""
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

    return cls, x_min, y_min, x_max, y_max


# ===================================================
# DRAWING
# ===================================================

def draw_boxes(image_path, label_path):
    """Draw YOLO bounding boxes on image."""
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Can't read image {image_path}")

    h, w, _ = img.shape

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()

                if len(parts) != 5:
                    continue

                cls, x_min, y_min, x_max, y_max = yolo_to_bbox(parts, w, h)

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


# ===================================================
# VISUALIZATION
# ===================================================

def show_samples(image_files):
    """Display random annotated images."""
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

        annotated = draw_boxes(img_path, label_path)
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        ax.imshow(annotated)
        ax.set_title(img_file, fontsize=9)
        ax.axis("off")

    plt.tight_layout()
    plt.show()


# ===================================================
# MAIN
# ===================================================

def main():
    image_files = get_image_files(IMAGE_DIR)

    if not image_files:
        raise FileNotFoundError(f"No images found in {IMAGE_DIR}")

    show_samples(image_files)

if __name__ == "__main__":
    main()
