import os
import glob
import yaml
from collections import Counter
import matplotlib.pyplot as plt


# ===================================================
# CONFIG
# ===================================================

DATA_YAML_PATH = "../../dataset/v6.1/data.yaml"


# ===================================================
# LOAD YAML
# ===================================================

def load_dataset_config(path):
    """Load dataset config from YAML."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"data.yaml not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_dataset_config(cfg):
    """Extract and validate dataset info."""
    base_dir = cfg.get("path")
    if base_dir is None:
        raise ValueError("'path' field missing from data.yaml")

    images_dir = os.path.join(base_dir, cfg.get("images", "images"))
    labels_dir = os.path.join(base_dir, cfg.get("labels", "labels"))

    class_names = cfg.get("names", [])
    if not class_names:
        raise ValueError("No class names found in data.yaml ('names' field missing).")

    class_map = {str(i): name for i, name in enumerate(class_names)}

    if not os.path.exists(images_dir):
        raise FileNotFoundError(f"Images directory not found: {images_dir}")

    if not os.path.exists(labels_dir):
        raise FileNotFoundError(f"Labels directory not found: {labels_dir}")

    return base_dir, images_dir, labels_dir, class_map


# ===================================================
# COUNTING
# ===================================================

def count_classes(labels_dir):
    """Count class occurrences from label files."""
    class_counts = Counter()

    for lbl_path in glob.glob(os.path.join(labels_dir, "*.txt")):
        with open(lbl_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    cls_id = parts[0]
                    class_counts[cls_id] += 1

    return class_counts


# ===================================================
# PRINTING
# ===================================================

def print_dataset_info(base_dir, images_dir, labels_dir):
    print(f"\nDataset base path: {base_dir}")
    print(f"Images directory:  {images_dir}")
    print(f"Labels directory:  {labels_dir}")


def print_class_counts(class_counts, class_map):
    print("\nClass instance count:\n")

    for cls_id in sorted(class_counts.keys(), key=lambda x: int(x)):
        class_name = class_map.get(cls_id, "UNKNOWN")
        print(f"Class {cls_id:>2} ({class_name}): {class_counts[cls_id]}")

    print("\nTotal objects:", sum(class_counts.values()))


# ===================================================
# PLOTTING
# ===================================================

def plot_class_distribution(class_counts, class_map):
    sorted_ids = sorted(class_counts.keys(), key=lambda x: int(x))

    labels = [
        f"{cid} - {class_map.get(cid, 'UNKNOWN')}"
        for cid in sorted_ids
    ]

    counts = [
        class_counts[cid]
        for cid in sorted_ids
    ]

    plt.figure(figsize=(14, 7))
    plt.bar(labels, counts)

    plt.xlabel("Class", fontsize=14, fontweight="bold")
    plt.ylabel("Count", fontsize=14, fontweight="bold")

    plt.title(
        "Object Count per Class — Combined Dataset (v6.1)",
        fontsize=18,
        fontweight="bold",
        pad=20
    )

    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)

    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


# ===================================================
# MAIN
# ===================================================
def main():
    cfg = load_dataset_config(DATA_YAML_PATH)
    BASE_DIR, IMAGES_DIR, LABEL_DIR, CLASS_MAP = parse_dataset_config(cfg)
    print_dataset_info(BASE_DIR, IMAGES_DIR, LABEL_DIR)
    class_counts = count_classes(LABEL_DIR)
    print_class_counts(class_counts, CLASS_MAP)
    plot_class_distribution(class_counts, CLASS_MAP)


if __name__ == "__main__":
    main()