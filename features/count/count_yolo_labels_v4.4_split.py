import os
import glob
import yaml
from collections import Counter
import matplotlib.pyplot as plt

DATA_YAML_PATH = "../../dataset/v4.4/data.yaml"

if not os.path.exists(DATA_YAML_PATH):
    raise FileNotFoundError(f"data.yaml not found at: {DATA_YAML_PATH}")

with open(DATA_YAML_PATH, "r", encoding="utf-8") as f:
    data_cfg = yaml.safe_load(f)

BASE_DIR = data_cfg.get("path")
if BASE_DIR is None:
    raise ValueError("'path' field missing from data.yaml")

CLASS_NAMES = data_cfg.get("names", [])
if not CLASS_NAMES:
    raise ValueError("No class names found in data.yaml ('names' field missing).")

NC = int(data_cfg.get("nc", len(CLASS_NAMES)))
CLASS_MAP = {str(i): name for i, name in enumerate(CLASS_NAMES)}

SPLITS = ["train", "val", "test"]
split_dirs = {s: data_cfg.get(s) for s in SPLITS}

missing = [s for s in SPLITS if not split_dirs.get(s)]
if missing:
    raise ValueError(f"Missing split paths in data.yaml: {missing}")

def count_split_labels(split_name: str):
    split_root = os.path.join(BASE_DIR, split_dirs[split_name])

    labels_dir = os.path.join(split_root, "labels")
    if not os.path.exists(labels_dir):
        raise FileNotFoundError(f"Labels directory not found for split '{split_name}': {labels_dir}")

    counts = Counter()
    for lbl_path in glob.glob(os.path.join(labels_dir, "*.txt")):
        with open(lbl_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                cls_id = parts[0]
                counts[cls_id] += 1

    # ensure all 0..NC-1 appear (even if 0)
    full = Counter({str(i): 0 for i in range(NC)})
    full.update(counts)
    return full

print(f"\nDataset base path: {BASE_DIR}")
print("Splits:")
for s in SPLITS:
    print(f"  {s}: {split_dirs[s]}")

counts_by_split = {s: count_split_labels(s) for s in SPLITS}

total_counts = Counter({str(i): 0 for i in range(NC)})
for s in SPLITS:
    total_counts.update(counts_by_split[s])

print("\nClass instance count per split:\n")
for cid in [str(i) for i in range(NC)]:
    name = CLASS_MAP.get(cid, "UNKNOWN")
    tr = counts_by_split["train"][cid]
    va = counts_by_split["val"][cid]
    te = counts_by_split["test"][cid]
    tot = total_counts[cid]
    print(f"Class {int(cid):>2} ({name}): train={tr}, val={va}, test={te}, total={tot}")

print("\nTotal objects (all splits):", sum(total_counts.values()))

# Plot totals
plot_labels = [f"{i} - {CLASS_MAP.get(str(i), 'UNKNOWN')}" for i in range(NC)]
plot_counts = [total_counts[str(i)] for i in range(NC)]

plt.figure(figsize=(14, 7))
plt.bar(plot_labels, plot_counts)
plt.xlabel("Class", fontsize=14, fontweight="bold")
plt.ylabel("Count", fontsize=14, fontweight="bold")
plt.title("Object Count per Class — German Dataset (v4.4) [Total]", fontsize=18, fontweight="bold", pad=20)
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()