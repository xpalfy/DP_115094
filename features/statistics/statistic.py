import os
from collections import defaultdict


# ===================================================
# CONFIG
# ===================================================

DATASETS = {
    "v4": "../../dataset/v4",
    "v5": "../../dataset/v5",
    "v6": "../../dataset/v6"
}


# ===================================================
# HELPERS
# ===================================================

def get_files(directory, extension=None):
    """List files in directory, optionally filter by extension."""
    files = os.listdir(directory)

    if extension:
        files = [f for f in files if f.endswith(extension)]

    return files


def count_instances(labels_path):
    """Count class instances from label files."""
    label_files = get_files(labels_path, ".txt")

    class_counts = defaultdict(int)
    total_instances = 0

    for label_file in label_files:
        with open(os.path.join(labels_path, label_file)) as f:
            lines = f.readlines()

        total_instances += len(lines)

        for line in lines:
            class_id = int(line.split()[0])
            class_counts[class_id] += 1

    return class_counts, total_instances


def compute_stats(class_counts, total_instances, num_images):
    """Compute dataset statistics."""
    num_classes = len(class_counts)

    avg_instances_per_image = total_instances / num_images if num_images else 0
    avg_instances_per_class = total_instances / num_classes if num_classes else 0

    return num_classes, avg_instances_per_image, avg_instances_per_class


# ===================================================
# PRINTING
# ===================================================

def print_stats(dataset_path, num_images, num_classes, total_instances,
                avg_per_image, avg_per_class, class_counts):
    """Print dataset statistics."""
    print(f"\nDataset: {dataset_path}")
    print("-------------------------")
    print(f"Images: {num_images}")
    print(f"Classes used: {num_classes}")
    print(f"Total instances: {total_instances}")
    print(f"Average instances per image: {avg_per_image:.2f}")
    print(f"Average instances per class: {avg_per_class:.2f}")

    print("\nInstances per class:")
    for cls in sorted(class_counts):
        print(f"class {cls}: {class_counts[cls]}")

    print("\nMin class instances:", min(class_counts.values()))
    print("Max class instances:", max(class_counts.values()))


# ===================================================
# MAIN ANALYSIS
# ===================================================

def analyze_dataset(dataset_path):
    """Analyze a single dataset."""

    labels_path = os.path.join(dataset_path, "labels")
    images_path = os.path.join(dataset_path, "images")

    label_files = get_files(labels_path, ".txt")
    image_files = get_files(images_path)

    class_counts, total_instances = count_instances(labels_path)

    num_images = len(image_files)

    num_classes, avg_per_image, avg_per_class = compute_stats(
        class_counts,
        total_instances,
        num_images
    )

    print_stats(
        dataset_path,
        num_images,
        num_classes,
        total_instances,
        avg_per_image,
        avg_per_class,
        class_counts
    )


# ===================================================
# RUN
# ===================================================

if __name__ == "__main__":
    for name, path in DATASETS.items():
        analyze_dataset(path)
