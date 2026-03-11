import os
from collections import defaultdict

datasets = {
    "v4": "../../dataset/v4",
    "v5": "../../dataset/v5",
    "v6": "../../dataset/v6"
}

def analyze_dataset(dataset_path):

    labels_path = os.path.join(dataset_path, "labels")
    images_path = os.path.join(dataset_path, "images")

    label_files = [f for f in os.listdir(labels_path) if f.endswith(".txt")]
    image_files = [f for f in os.listdir(images_path)]

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

    print(f"\nDataset: {dataset_path}")
    print("-------------------------")
    print(f"Images: {num_images}")
    print(f"Classes used: {num_classes}")
    print(f"Total instances: {total_instances}")
    print(f"Average instances per image: {avg_instances_per_image:.2f}")
    print(f"Average instances per class: {avg_instances_per_class:.2f}")

    print("\nInstances per class:")
    for cls in sorted(class_counts):
        print(f"class {cls}: {class_counts[cls]}")

    print("\nMin class instances:", min(class_counts.values()))
    print("Max class instances:", max(class_counts.values()))


for name, path in datasets.items():
    analyze_dataset(path)