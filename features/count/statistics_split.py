import os
from collections import defaultdict

datasets = {
    "v4.4": "../../dataset/v4.4",
    "v5.5": "../../dataset/v5.5",
    "v6.4": "../../dataset/v6.4"
}

splits = ["train", "val", "test"]


def analyze_split(split_path):

    labels_path = os.path.join(split_path, "labels")
    images_path = os.path.join(split_path, "images")

    if not os.path.exists(labels_path) or not os.path.exists(images_path):
        return None

    label_files = [f for f in os.listdir(labels_path) if f.endswith(".txt")]
    image_files = os.listdir(images_path)

    class_counts = defaultdict(int)
    total_instances = 0

    for label_file in label_files:
        with open(os.path.join(labels_path, label_file)) as f:
            lines = f.readlines()

        total_instances += len(lines)

        for line in lines:
            class_id = int(line.split()[0])
            class_counts[class_id] += 1

    num_images = len(image_files)
    num_classes = len(class_counts)

    avg_instances_per_image = total_instances / num_images if num_images else 0
    avg_instances_per_class = total_instances / num_classes if num_classes else 0

    return {
        "images": num_images,
        "classes": num_classes,
        "instances": total_instances,
        "avg_img": avg_instances_per_image,
        "avg_cls": avg_instances_per_class,
        "class_counts": class_counts
    }


def analyze_dataset(dataset_name, dataset_path):

    print(f"\n========== DATASET {dataset_name} ==========")

    total_class_counts = defaultdict(int)
    total_images = 0
    total_instances = 0

    for split in splits:
        split_path = os.path.join(dataset_path, split)

        stats = analyze_split(split_path)

        if stats is None:
            continue

        print(f"\n--- {split.upper()} ---")
        print(f"Images: {stats['images']}")
        print(f"Classes used: {stats['classes']}")
        print(f"Instances: {stats['instances']}")
        print(f"Avg instances / image: {stats['avg_img']:.2f}")
        print(f"Avg instances / class: {stats['avg_cls']:.2f}")

        for cls, count in stats["class_counts"].items():
            total_class_counts[cls] += count

        total_images += stats["images"]
        total_instances += stats["instances"]

    total_classes = len(total_class_counts)
    avg_instances_per_image_total = total_instances / total_images if total_images else 0
    avg_instances_per_class_total = total_instances / total_classes if total_classes else 0

    print("\n--- TOTAL DATASET ---")
    print(f"Images: {total_images}")
    print(f"Instances: {total_instances}")
    print(f"Classes used: {total_classes}")
    print(f"Average instances per image: {avg_instances_per_image_total:.2f}")
    print(f"Average instances per class: {avg_instances_per_class_total:.2f}")

    print("\nInstances per class:")
    for cls in sorted(total_class_counts):
        print(f"class {cls}: {total_class_counts[cls]}")

    if total_class_counts:
        print("\nMin class instances:", min(total_class_counts.values()))
        print("Max class instances:", max(total_class_counts.values()))


for name, path in datasets.items():
    analyze_dataset(name, path)