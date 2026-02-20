import os
import shutil
import random

# ---- DATASET PATHS ----
input_dataset = "../../dataset/v5.2"
output_dataset = "../../dataset/v5.4"

images_path = os.path.join(input_dataset, "images")
labels_path = os.path.join(input_dataset, "labels")

# ---- SPLIT RATIOS ----
train_ratio, val_ratio, test_ratio = 0.7, 0.15, 0.15

assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
    "Split ratios must sum to 1."

# ---- OUTPUT STRUCTURE ----
splits = ["train", "val", "test"]

for split in splits:
    os.makedirs(os.path.join(output_dataset, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dataset, split, "labels"), exist_ok=True)

# ---- COLLECT IMAGE FILES ----
image_files = [
    f for f in os.listdir(images_path)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

random.shuffle(image_files)

total_images = len(image_files)

train_end = int(total_images * train_ratio)
val_end = train_end + int(total_images * val_ratio)

train_files = image_files[:train_end]
val_files   = image_files[train_end:val_end]
test_files  = image_files[val_end:]

split_map = {
    "train": train_files,
    "val": val_files,
    "test": test_files
}

# ---- COPY FILES ----
for split, files in split_map.items():
    print(f"\nProcessing {split} split ({len(files)} images)")

    for img_file in files:
        base_name = os.path.splitext(img_file)[0]

        src_img = os.path.join(images_path, img_file)
        src_lbl = os.path.join(labels_path, base_name + ".txt")

        dst_img = os.path.join(output_dataset, split, "images", img_file)
        dst_lbl = os.path.join(output_dataset, split, "labels", base_name + ".txt")

        # Copy image
        shutil.copy2(src_img, dst_img)

        # Copy label if it exists
        if os.path.exists(src_lbl):
            shutil.copy2(src_lbl, dst_lbl)

print("\nDataset split completed → v5.4")
print(f"Train images: {len(train_files)}")
print(f"Validation images: {len(val_files)}")
print(f"Test images: {len(test_files)}")
