import os
import cv2
import numpy as np


# ===================================================
# CONFIG
# ===================================================

INPUT_DATASET = "../../dataset/v6.1"
OUTPUT_DATASET = "../../dataset/v6.2"

IMAGES_DIR = os.path.join(INPUT_DATASET, "images")
LABELS_DIR = os.path.join(INPUT_DATASET, "labels")

OUT_IMAGES_DIR = os.path.join(OUTPUT_DATASET, "images")
OUT_LABELS_DIR = os.path.join(OUTPUT_DATASET, "labels")

os.makedirs(OUT_IMAGES_DIR, exist_ok=True)
os.makedirs(OUT_LABELS_DIR, exist_ok=True)

# Tile config (relative to original)
TILE_RATIO = 2080 / 4160
OVERLAP_RATIO = 200 / 2080

MIN_TILE = 640
MIN_OVERLAP = 32


# ===================================================
# HELPERS
# ===================================================

def compute_steps(length, tile, overlap):
    """Compute sliding window start positions."""
    step = max(1, tile - overlap)
    steps = list(range(0, max(1, length - tile + 1), step))

    if not steps:
        steps = [0]

    if steps[-1] + tile < length:
        steps.append(length - tile)

    return steps


def load_annotations(label_path):
    """Load raw label lines."""
    if not os.path.exists(label_path):
        return []
    with open(label_path, "r") as f:
        return f.readlines()


def parse_polygon(parts, W, H):
    """Convert YOLO polygon → pixel coordinates."""
    coords = np.array(parts[1:], dtype=np.float32)

    if coords.size % 2 != 0:
        return None

    poly = coords.reshape(-1, 2)
    poly[:, 0] *= W
    poly[:, 1] *= H

    return poly


def polygon_inside_tile(poly, x1, y1, x2, y2):
    """Check if polygon fully inside tile."""
    return np.all(
        (x1 <= poly[:, 0]) & (poly[:, 0] <= x2) &
        (y1 <= poly[:, 1]) & (poly[:, 1] <= y2)
    )


def normalize_polygon(poly, x_start, y_start, tile_size):
    """Convert polygon to normalized tile coords."""
    poly[:, 0] = (poly[:, 0] - x_start) / tile_size
    poly[:, 1] = (poly[:, 1] - y_start) / tile_size
    return np.clip(poly, 0.0, 1.0)


def format_label(class_id, poly):
    """Format YOLO segmentation label."""
    flat = poly.reshape(-1)
    return f"{class_id} " + " ".join(f"{v:.6f}" for v in flat) + "\n"


# ===================================================
# MAIN
# ===================================================

def process_image(image_file):
    image_path = os.path.join(IMAGES_DIR, image_file)

    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image: {image_path}")
        return

    H, W = image.shape[:2]

    # Compute tile size
    tile_size = int(round(W * TILE_RATIO))
    tile_size = max(MIN_TILE, min(tile_size, W, H))

    overlap = int(round(tile_size * OVERLAP_RATIO))
    overlap = max(MIN_OVERLAP, min(overlap, tile_size - 1))

    x_steps = compute_steps(W, tile_size, overlap)
    y_steps = compute_steps(H, tile_size, overlap)

    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(LABELS_DIR, label_file)

    annotations = load_annotations(label_path)

    for y_idx, y_start in enumerate(y_steps):
        for x_idx, x_start in enumerate(x_steps):

            y_end = y_start + tile_size
            x_end = x_start + tile_size

            # Skip partial tiles
            if y_end > H or x_end > W:
                continue

            new_annotations = []

            for line in annotations:
                parts = line.strip().split()
                if len(parts) < 7:
                    continue

                class_id = parts[0]
                poly = parse_polygon(parts, W, H)
                if poly is None:
                    continue

                if not polygon_inside_tile(poly, x_start, y_start, x_end, y_end):
                    continue

                poly = normalize_polygon(poly, x_start, y_start, tile_size)
                new_annotations.append(format_label(class_id, poly))

            # Save only if something inside
            if new_annotations:
                cropped = image[y_start:y_end, x_start:x_end]

                stem = os.path.splitext(image_file)[0]
                suffix = f"_part{y_idx:03d}_{x_idx:03d}"

                img_name = stem + suffix + ".jpg"
                lbl_name = stem + suffix + ".txt"

                cv2.imwrite(os.path.join(OUT_IMAGES_DIR, img_name), cropped)

                with open(os.path.join(OUT_LABELS_DIR, lbl_name), "w") as f:
                    f.writelines(new_annotations)


def main():
    for image_file in os.listdir(IMAGES_DIR):
        if image_file.lower().endswith((".jpg", ".jpeg", ".png")):
            process_image(image_file)

    print("Done: v6.1 -> v6.2 slicing completed. Only annotated tiles were saved.")


if __name__ == "__main__":
    main()
