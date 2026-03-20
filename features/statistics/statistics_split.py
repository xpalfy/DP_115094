import os
from collections import defaultdict


# ===================================================
# CONFIG
# ===================================================

DATASETS = {
    "v4.4": "../../dataset/v4.4",
    "v5.5": "../../dataset/v5.5",
    "v6.4": "../../dataset/v6.4"
}

SPLITS = ["train", "val", "test"]


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
    """Count class instances in a label directory."""
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
    """Compute statistics."""
    num_classes = len(class_counts)

    avg_per_image = total_instances / num_images if num_images else 0
    avg_per_class = total_instances / num_classes if num_classes else 0

    return num_classes, avg_per_image, avg_per_class


# ===================================================
# SPLIT ANALYSIS
# ===================================================

def analyze_split(split_path):
    """Analyze a single dataset split."""

    labels_path = os.path.join(split_path, "labels")
    images_path = os.path.join(split_path, "images")

    if not os.path.exists(labels_path) or not os.path.exists(images_path):
        return None

    image_files = get_files(images_path)

    class_counts, total_instances = count_instances(labels_path)

    num_images = len(image_files)

    num_classes, avg_img, avg_cls = compute_stats(
        class_counts,
        total_instances,
        num_images
    )

    return {
        "images": num_images,
        "classes": num_classes,
        "instances": total_instances,
        "avg_img": avg_img,
        "avg_cls": avg_cls,
        "class_counts": class_counts
    }


# ===================================================
# PRINTING
# ===================================================

def print_split_stats(split, stats):
    print(f"\n--- {split.upper()} ---")
    print(f"Images: {stats['images']}")
    print(f"Classes used: {stats['classes']}")
    print(f"Instances: {stats['instances']}")
    print(f"Avg instances / image: {stats['avg_img']:.2f}")
    print(f"Avg instances / class: {stats['avg_cls']:.2f}")


def print_total_stats(total_images, total_instances, total_classes,
                      avg_img, avg_cls, total_class_counts):

    print("\n--- TOTAL DATASET ---")
    print(f"Images: {total_images}")
    print(f"Instances: {total_instances}")
    print(f"Classes used: {total_classes}")
    print(f"Average instances per image: {avg_img:.2f}")
    print(f"Average instances per class: {avg_cls:.2f}")

    print("\nInstances per class:")
    for cls in sorted(total_class_counts):
        print(f"class {cls}: {total_class_counts[cls]}")

    if total_class_counts:
        print("\nMin class instances:", min(total_class_counts.values()))
        print("Max class instances:", max(total_class_counts.values()))


# ===================================================
# DATASET ANALYSIS
# ===================================================

def analyze_dataset(dataset_name, dataset_path):
    """Analyze full dataset (all splits)."""

    print(f"\n========== DATASET {dataset_name} ==========")

    total_class_counts = defaultdict(int)
    total_images = 0
    total_instances = 0

    for split in SPLITS:
        split_path = os.path.join(dataset_path, split)

        stats = analyze_split(split_path)
        if stats is None:
            continue

        print_split_stats(split, stats)

        for cls, count in stats["class_counts"].items():
            total_class_counts[cls] += count

        total_images += stats["images"]
        total_instances += stats["instances"]

    total_classes = len(total_class_counts)

    avg_img_total = total_instances / total_images if total_images else 0
    avg_cls_total = total_instances / total_classes if total_classes else 0

    print_total_stats(
        total_images,
        total_instances,
        total_classes,
        avg_img_total,
        avg_cls_total,
        total_class_counts
    )


# ===================================================
# RUN
# ===================================================

if __name__ == "__main__":
    for name, path in DATASETS.items():
        analyze_dataset(name, path)
