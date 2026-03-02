import os
import cv2
import numpy as np

# INPUT: v6.1
dataset_path = "../../../dataset/v6.1"
# OUTPUT: v6.2
output_dataset_path = "../../../dataset/v6.2"

os.makedirs(os.path.join(output_dataset_path, "images"), exist_ok=True)
os.makedirs(os.path.join(output_dataset_path, "labels"), exist_ok=True)

# Ratios from original script (4160 -> 2080 tile, 2080 -> 200 overlap)
TILE_RATIO = 2080 / 4160
OVERLAP_RATIO = 200 / 2080

MIN_TILE = 640
MIN_OVERLAP = 32

def compute_steps(length, tile, overlap):
    step = max(1, tile - overlap)
    steps = list(range(0, max(1, length - tile + 1), step))
    if not steps:
        steps = [0]
    if steps[-1] + tile < length:
        steps.append(length - tile)
    return steps

images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")
out_images_path = os.path.join(output_dataset_path, "images")
out_labels_path = os.path.join(output_dataset_path, "labels")

for image_file in os.listdir(images_path):
    if not image_file.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(images_path, image_file)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image: {image_path}")
        continue

    H, W = image.shape[:2]

    # Proportional tile and overlap
    TILE_SIZE = int(round(W * TILE_RATIO))
    TILE_SIZE = max(MIN_TILE, min(TILE_SIZE, W, H))

    OVERLAP = int(round(TILE_SIZE * OVERLAP_RATIO))
    OVERLAP = max(MIN_OVERLAP, min(OVERLAP, TILE_SIZE - 1))

    x_steps = compute_steps(W, TILE_SIZE, OVERLAP)
    y_steps = compute_steps(H, TILE_SIZE, OVERLAP)

    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(labels_path, label_file)

    annotations = []
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            annotations = f.readlines()

    for y_idx, y_start in enumerate(y_steps):
        for x_idx, x_start in enumerate(x_steps):
            y_end = y_start + TILE_SIZE
            x_end = x_start + TILE_SIZE

            # Keep only full tiles
            if y_end > H or x_end > W:
                continue

            new_annotations = []
            for line in annotations:
                parts = line.strip().split()
                if len(parts) < 1 + 6:
                    continue

                class_id = parts[0]
                coords = np.array(parts[1:], dtype=np.float32)
                if coords.size % 2 != 0:
                    continue

                poly = coords.reshape(-1, 2)

                # Normalized -> absolute pixels
                poly[:, 0] *= W
                poly[:, 1] *= H

                # Keep only polygons fully inside tile
                if np.all((x_start <= poly[:, 0]) & (poly[:, 0] <= x_end) &
                          (y_start <= poly[:, 1]) & (poly[:, 1] <= y_end)):

                    poly[:, 0] = (poly[:, 0] - x_start) / TILE_SIZE
                    poly[:, 1] = (poly[:, 1] - y_start) / TILE_SIZE

                    poly = np.clip(poly, 0.0, 1.0)

                    flat = poly.reshape(-1)
                    new_annotations.append(
                        f"{class_id} " + " ".join(f"{v:.6f}" for v in flat) + "\n"
                    )

            # Save only tiles with annotations
            if new_annotations:
                cropped = image[y_start:y_end, x_start:x_end]

                out_img_name = f"{os.path.splitext(image_file)[0]}_part{y_idx:03d}_{x_idx:03d}.jpg"
                cv2.imwrite(os.path.join(out_images_path, out_img_name), cropped)

                out_lbl_name = f"{os.path.splitext(image_file)[0]}_part{y_idx:03d}_{x_idx:03d}.txt"
                with open(os.path.join(out_labels_path, out_lbl_name), "w") as f:
                    f.writelines(new_annotations)

print("Done: v6.1 -> v6.2 slicing completed. Only annotated tiles were saved.")
