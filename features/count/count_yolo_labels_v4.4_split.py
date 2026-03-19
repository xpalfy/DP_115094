import os
import glob
import yaml
from collections import Counter
import matplotlib.pyplot as plt

# ---- CONFIG ----
DATA_YAML_PATH = "../../dataset/v4.4/data.yaml"

# ---- LOAD YAML ----
if not os.path.exists(DATA_YAML_PATH):
    raise FileNotFoundError(f"data.yaml not found at: {DATA_YAML_PATH}")

with open(DATA_YAML_PATH, "r", encoding="utf-8") as f:
    data_cfg = yaml.safe_load(f)

BASE_DIR = data_cfg.get("path")
if BASE_DIR is None:
    raise ValueError("'path' field missing from data.yaml")

CLASS_NAMES = data_cfg.get("names", [])
if not CLASS_NAMES:
    raise ValueError("No class names found in data.yaml")

NC = int(data_cfg.get("nc", len(CLASS_NAMES)))
CLASS_MAP = {str(i): name for i, name in enumerate(CLASS_NAMES)}

SPLITS = ["train", "val", "test"]
split_dirs = {s: data_cfg.get(s) for s in SPLITS}

missing = [s for s in SPLITS if not split_dirs.get(s)]
if missing:
    raise ValueError(f"Missing split paths in data.yaml: {missing}")

# ---- COUNT FUNCTION ----
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

    full = Counter({str(i): 0 for i in range(NC)})
    full.update(counts)
    return full

# ---- PRINT INFO ----
print(f"\nDataset base path: {BASE_DIR}")
print("Splits:")
for s in SPLITS:
    print(f"  {s}: {split_dirs[s]}")

# ---- COUNT ----
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

# ---- TOTAL PLOT ----
labels = [f"{i}-{CLASS_MAP.get(str(i), 'UNK')}" for i in range(NC)]
values = [total_counts[str(i)] for i in range(NC)]

plt.figure(figsize=(14, 6))
plt.bar(labels, values)
plt.title("Total Distribution (v4.4)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# ---- PER SPLIT ----
for split in SPLITS:
    split_counts = counts_by_split[split]

    labels = [f"{i}-{CLASS_MAP.get(str(i), 'UNK')}" for i in range(NC)]
    values = [split_counts[str(i)] for i in range(NC)]

    plt.figure(figsize=(14, 6))
    plt.bar(labels, values)
    plt.title(f"{split.upper()} Distribution (v4.4)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# ---- NORMALIZED ----
for split in SPLITS:
    split_counts = counts_by_split[split]
    total = sum(split_counts.values())

    labels = [f"{i}" for i in range(NC)]
    values = [split_counts[str(i)] / total for i in range(NC)]

    plt.figure(figsize=(14, 6))
    plt.bar(labels, values)
    plt.title(f"Normalized Distribution — {split.upper()} (v4.4)")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# ---- OVERLAY (BEST) ----
labels = [f"{i}" for i in range(NC)]

train_vals = [counts_by_split["train"][str(i)] / sum(counts_by_split["train"].values()) for i in range(NC)]
val_vals   = [counts_by_split["val"][str(i)]   / sum(counts_by_split["val"].values())   for i in range(NC)]
test_vals  = [counts_by_split["test"][str(i)]  / sum(counts_by_split["test"].values())  for i in range(NC)]

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