import os
import shutil
import yaml


# ===================================================
# CONFIG
# ===================================================

BASE_PATH = "../../dataset"

V4_PATH = os.path.join(BASE_PATH, "v4")
V5_PATH = os.path.join(BASE_PATH, "v5")

OUTPUT_PATH = os.path.join(BASE_PATH, "v7")

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp"]


# ===================================================
# HELPERS
# ===================================================

def load_yaml(path):
    """Load YAML file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def create_class_mapping(old_names, common_names):
    """Map old class IDs → new class IDs."""
    return {
        old_id: common_names.index(name)
        for old_id, name in enumerate(old_names)
        if name in common_names
    }


def find_image(images_dir, base_name):
    """Find corresponding image file."""
    for ext in IMAGE_EXTS:
        img_path = os.path.join(images_dir, base_name + ext)
        if os.path.exists(img_path):
            return img_path
    return None


def process_label_file(label_path, mapping):
    """Convert one label file."""
    with open(label_path, "r") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue

        old_cls = int(parts[0])

        if old_cls not in mapping:
            continue

        new_cls = mapping[old_cls]
        new_lines.append(str(new_cls) + " " + " ".join(parts[1:]))

    return new_lines


def convert_dataset(src_root, mapping, dst_root):
    """Convert dataset and merge into destination."""
    images_src = os.path.join(src_root, "images")
    labels_src = os.path.join(src_root, "labels")

    images_dst = os.path.join(dst_root, "images")
    labels_dst = os.path.join(dst_root, "labels")

    os.makedirs(images_dst, exist_ok=True)
    os.makedirs(labels_dst, exist_ok=True)

    for label_file in os.listdir(labels_src):
        if not label_file.endswith(".txt"):
            continue

        label_path = os.path.join(labels_src, label_file)
        base = os.path.splitext(label_file)[0]

        image_path = find_image(images_src, base)
        if image_path is None:
            continue

        new_lines = process_label_file(label_path, mapping)

        # Only save if something remains
        if not new_lines:
            continue

        shutil.copy(image_path, os.path.join(images_dst, os.path.basename(image_path)))

        with open(os.path.join(labels_dst, label_file), "w") as f:
            f.write("\n".join(new_lines))


def get_common_classes(names1, names2):
    """Get sorted intersection of class names."""
    return sorted(set(names1).intersection(set(names2)))


# ===================================================
# MAIN
# ===================================================

def main():

    v4_yaml = load_yaml(os.path.join(V4_PATH, "data.yaml"))
    v5_yaml = load_yaml(os.path.join(V5_PATH, "data.yaml"))

    v4_names = v4_yaml["names"]
    v5_names = v5_yaml["names"]

    common_classes = get_common_classes(v4_names, v5_names)

    print("Common classes:")
    print(common_classes)
    print("Total:", len(common_classes))

    if not common_classes:
        raise RuntimeError("No common classes found!")

    mapping_v4 = create_class_mapping(v4_names, common_classes)
    mapping_v5 = create_class_mapping(v5_names, common_classes)

    # Reset output
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Convert datasets
    convert_dataset(V4_PATH, mapping_v4, OUTPUT_PATH)
    convert_dataset(V5_PATH, mapping_v5, OUTPUT_PATH)

    # Save new YAML
    out_yaml = {
        "path": OUTPUT_PATH,
        "images": "images",
        "labels": "labels",
        "nc": len(common_classes),
        "names": common_classes,
        "augment": True
    }

    with open(os.path.join(OUTPUT_PATH, "data.yaml"), "w") as f:
        yaml.dump(out_yaml, f, sort_keys=False)

    print("\nv7 dataset successfully created.")


if __name__ == "__main__":
    main()
