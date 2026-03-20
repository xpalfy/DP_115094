import os
import glob
import yaml
from collections import Counter
import matplotlib.pyplot as plt


# ===================================================
# CONFIG
# ===================================================

DATA_YAML_PATH = "../../dataset/v4.4/data.yaml"
SPLITS = ["train", "val", "test"]


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

    class_names = cfg.get("names", [])
    if not class_names:
        raise ValueError("No class names found in data.yaml")

    nc = int(cfg.get("nc", len(class_names)))

    class_map = {str(i): name for i, name in enumerate(class_names)}
    split_dirs = {s: cfg.get(s) for s in SPLITS}

    missing = [s for s in SPLITS if not split_dirs.get(s)]
    if missing:
        raise ValueError(f"Missing split paths in data.yaml: {missing}")

    return base_dir, class_names, nc, class_map, split_dirs


# ===================================================
# COUNTING
# ===================================================

def count_split_labels(base_dir, split_name, split_dirs, nc):
    """Count label occurrences for a split."""
    split_root = os.path.join(base_dir, split_dirs[split_name])
    labels_dir = os.path.join(split_root, "labels")

    if not os.path.exists(labels_dir):
        raise FileNotFoundError(
            f"Labels directory not found for split '{split_name}': {labels_dir}"
        )

    counts = Counter()

    for lbl_path in glob.glob(os.path.join(labels_dir, "*.txt")):
        with open(lbl_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue

                cls_id = parts[0]
                counts[cls_id] += 1

    full = Counter({str(i): 0 for i in range(nc)})
    full.update(counts)

    return full


def compute_all_counts(base_dir, split_dirs, nc):
    """Compute counts for all splits."""
    counts_by_split = {
        s: count_split_labels(base_dir, s, split_dirs, nc)
        for s in SPLITS
    }

    total_counts = Counter({str(i): 0 for i in range(nc)})
    for s in SPLITS:
        total_counts.update(counts_by_split[s])

    return counts_by_split, total_counts


# ===================================================
# PRINTING
# ===================================================

def print_dataset_info(base_dir, split_dirs):
    print(f"\nDataset base path: {base_dir}")
    print("Splits:")
    for s in SPLITS:
        print(f"  {s}: {split_dirs[s]}")


def print_class_distribution(counts_by_split, total_counts, class_map, nc):
    print("\nClass instance count per split:\n")

    for cid in [str(i) for i in range(nc)]:
        name = class_map.get(cid, "UNKNOWN")

        tr = counts_by_split["train"][cid]
        va = counts_by_split["val"][cid]
        te = counts_by_split["test"][cid]
        tot = total_counts[cid]

        if tot > 0:
            tr_p = tr / tot * 100
            va_p = va / tot * 100
            te_p = te / tot * 100
        else:
            tr_p = va_p = te_p = 0

        print(
            f"Class {int(cid):>2} ({name}): "
            f"train={tr} ({tr_p:.1f}%), "
            f"val={va} ({va_p:.1f}%), "
            f"test={te} ({te_p:.1f}%), "
            f"total={tot}"
        )

    print("\nTotal objects:", sum(total_counts.values()))


# ===================================================
# PLOTTING
# ===================================================

def plot_total_distribution(total_counts, class_map, nc):
    labels = [f"{i}-{class_map.get(str(i), 'UNK')}" for i in range(nc)]
    values = [total_counts[str(i)] for i in range(nc)]

    plt.figure(figsize=(14, 6))
    plt.bar(labels, values)
    plt.title("Total Distribution (v4.4)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_split_distributions(counts_by_split, class_map, nc):
    for split in SPLITS:
        split_counts = counts_by_split[split]

        labels = [f"{i}-{class_map.get(str(i), 'UNK')}" for i in range(nc)]
        values = [split_counts[str(i)] for i in range(nc)]

        plt.figure(figsize=(14, 6))
        plt.bar(labels, values)
        plt.title(f"{split.upper()} Distribution (v4.4)")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()


def plot_normalized_distributions(counts_by_split, nc):
    for split in SPLITS:
        split_counts = counts_by_split[split]
        total = sum(split_counts.values())

        labels = [f"{i}" for i in range(nc)]
        values = [split_counts[str(i)] / total for i in range(nc)]

        plt.figure(figsize=(14, 6))
        plt.bar(labels, values)
        plt.title(f"Normalized Distribution — {split.upper()} (v4.4)")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()


def plot_overlay(counts_by_split, nc):
    labels = [f"{i}" for i in range(nc)]

    train_vals = [
        counts_by_split["train"][str(i)] / sum(counts_by_split["train"].values())
        for i in range(nc)
    ]
    val_vals = [
        counts_by_split["val"][str(i)] / sum(counts_by_split["val"].values())
        for i in range(nc)
    ]
    test_vals = [
        counts_by_split["test"][str(i)] / sum(counts_by_split["test"].values())
        for i in range(nc)
    ]

    plt.figure(figsize=(14, 6))
    plt.plot(labels, train_vals, marker='o', label="Train")
    plt.plot(labels, val_vals, marker='o', label="Val")
    plt.plot(labels, test_vals, marker='o', label="Test")

    plt.title("Normalized Distribution Comparison (v4.4)")
    plt.xlabel("Class")
    plt.ylabel("Ratio")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# ===================================================
# MAIN
# ===================================================

def main():
    cfg = load_dataset_config(DATA_YAML_PATH)
    BASE_DIR, CLASS_NAMES, NC, CLASS_MAP, split_dirs = parse_dataset_config(cfg)
    print_dataset_info(BASE_DIR, split_dirs)
    counts_by_split, total_counts = compute_all_counts(BASE_DIR, split_dirs, NC)
    print_class_distribution(counts_by_split, total_counts, CLASS_MAP, NC)
    plot_total_distribution(total_counts, CLASS_MAP, NC)
    plot_split_distributions(counts_by_split, CLASS_MAP, NC)
    plot_normalized_distributions(counts_by_split, NC)
    plot_overlay(counts_by_split, NC)


if __name__ == "__main__":
    main()
