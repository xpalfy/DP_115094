import shutil
from pathlib import Path
from collections import Counter
import yaml


# ===================================================
# CONFIG
# ===================================================

SRC_DATA_YAML = Path("../../dataset/v6/data.yaml")
DST_ROOT = Path("../../dataset/v6.1")

MIN_COUNT = 100

REMAP_CLASSES = True
DRY_RUN = False
COPY_IMAGES = True
KEEP_EMPTY_LABEL_FILES = True

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"]


# ===================================================
# HELPERS
# ===================================================

def parse_seg_line(line, nc):
    """Parse one YOLO segmentation line."""
    parts = line.strip().split()

    if len(parts) < 3:
        return None, None

    try:
        cls = int(float(parts[0]))
        coords = [float(p) for p in parts[1:]]
    except:
        return None, None

    if cls < 0 or cls >= nc:
        return None, None

    if len(coords) % 2 != 0:
        return None, None

    return cls, coords


def find_image(images_dir, label_path):
    """Find corresponding image file for a label."""
    stem = label_path.stem

    for ext in IMAGE_EXTS:
        img_path = images_dir / f"{stem}{ext}"
        if img_path.exists():
            return img_path

    return None


def load_dataset(cfg):
    """Load dataset paths and metadata."""
    base = Path(cfg["path"])
    images_dir = base / cfg.get("images", "images")
    labels_dir = base / cfg.get("labels", "labels")

    names = cfg.get("names", [])
    nc = int(cfg.get("nc", len(names)))

    if not images_dir.exists():
        raise FileNotFoundError(f"Missing images dir: {images_dir}")
    if not labels_dir.exists():
        raise FileNotFoundError(f"Missing labels dir: {labels_dir}")
    if not names or nc <= 0:
        raise ValueError("Invalid data.yaml: missing names/nc")

    return base, images_dir, labels_dir, names, nc


def count_classes(label_files, nc):
    """Count instances per class."""
    counts = Counter()
    cache = {}
    invalid_lines = 0

    for lf in label_files:
        items = []

        for raw in lf.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not raw.strip():
                continue

            cls, coords = parse_seg_line(raw, nc)

            if cls is None:
                invalid_lines += 1
                items.append((None, None))
            else:
                counts[cls] += 1
                items.append((cls, coords))

        cache[lf] = items

    return counts, cache, invalid_lines


def compute_keep_drop(counts, nc):
    """Determine which classes to keep/drop."""
    to_drop = {i for i in range(nc) if counts.get(i, 0) < MIN_COUNT}
    to_keep = [i for i in range(nc) if i not in to_drop]
    return to_keep, to_drop


def build_remap(to_keep, names):
    """Build class remapping."""
    remap = {old: new for new, old in enumerate(to_keep)}
    new_names = [names[old] for old in to_keep]
    return remap, new_names


# ===================================================
# MAIN
# ===================================================

def main():

    if not SRC_DATA_YAML.exists():
        raise FileNotFoundError(f"Missing: {SRC_DATA_YAML}")

    cfg = yaml.safe_load(SRC_DATA_YAML.read_text(encoding="utf-8"))

    base, images_dir, labels_dir, names, nc = load_dataset(cfg)

    label_files = sorted(labels_dir.glob("*.txt"))
    if not label_files:
        raise FileNotFoundError(f"No label files in: {labels_dir}")

    counts, cache, invalid_lines = count_classes(label_files, nc)

    to_keep, to_drop = compute_keep_drop(counts, nc)

    # -------------------------
    # INFO
    # -------------------------
    print(f"SRC: {base}")
    print(f"Images: {images_dir}")
    print(f"Labels: {labels_dir}")
    print(f"Label files: {len(label_files)}")

    if invalid_lines:
        print(f"Invalid lines: {invalid_lines}")

    print(f"\nRule: keep classes with count >= {MIN_COUNT}")

    for i in sorted(range(nc), key=lambda x: counts.get(x, 0)):
        c = counts.get(i, 0)
        tag = " DROP" if i in to_drop else ""
        name = names[i] if i < len(names) else str(i)
        print(f"{i:2d} ({name}): {c}{tag}")

    print(f"\nDrop: {len(to_drop)} | Keep: {len(to_keep)}")

    if not to_keep:
        raise RuntimeError("No classes would remain. Lower MIN_COUNT.")

    if DRY_RUN:
        print(f"\n[DRY RUN] Nothing written. Set DRY_RUN=False to create {DST_ROOT}.")
        return

    # -------------------------
    # OUTPUT SETUP
    # -------------------------
    dst_images = DST_ROOT / "images"
    dst_labels = DST_ROOT / "labels"

    dst_images.mkdir(parents=True, exist_ok=True)
    dst_labels.mkdir(parents=True, exist_ok=True)

    if REMAP_CLASSES:
        remap, new_names = build_remap(to_keep, names)
        new_nc = len(new_names)
    else:
        remap = None
        new_names = names[:]
        new_nc = nc

    # -------------------------
    # PROCESS FILES
    # -------------------------
    written_labels = 0
    copied_images = 0
    skipped_images = 0
    emptied = 0
    removed_lines = 0

    for lf, items in cache.items():

        kept_lines = []

        for cls, coords in items:
            if cls is None or cls in to_drop:
                removed_lines += 1
                continue

            out_cls = remap[cls] if remap else cls
            kept_lines.append(
                str(out_cls) + " " + " ".join(str(x) for x in coords)
            )

        out_label = dst_labels / lf.name

        if not kept_lines:
            emptied += 1
            if KEEP_EMPTY_LABEL_FILES:
                out_label.write_text("", encoding="utf-8")
                written_labels += 1
        else:
            out_label.write_text("\n".join(kept_lines) + "\n", encoding="utf-8")
            written_labels += 1

        # Copy image
        if COPY_IMAGES:
            img = find_image(images_dir, lf)

            if img is None:
                skipped_images += 1
            else:
                shutil.copy2(img, dst_images / img.name)
                copied_images += 1

    # -------------------------
    # SAVE NEW YAML
    # -------------------------
    out_yaml = {
        "path": str(DST_ROOT),
        "images": "images",
        "labels": "labels",
        "nc": int(new_nc),
        "names": new_names,
        "augment": bool(cfg.get("augment", True)),
    }

    (DST_ROOT / "data.yaml").write_text(
        yaml.safe_dump(out_yaml, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # -------------------------
    # SUMMARY
    # -------------------------
    print("\nv6.1 dataset successfully created.")
    print(f"Written labels: {written_labels}")
    print(f"Copied images: {copied_images}")

    if skipped_images:
        print(f"Images not found: {skipped_images}")

    print(f"Emptied labels: {emptied}")
    print(f"Removed lines: {removed_lines}")
    print(f"New nc: {new_nc}")
    print("Remapped classes: yes" if REMAP_CLASSES else "Remapped classes: no")


if __name__ == "__main__":
    main()
