import os
import shutil
import yaml


# =========================
# Utility Functions
# =========================

def load_yaml(yaml_path):
    """Load a YAML configuration file."""
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def create_class_mapping(old_names, common_names):
    """
    Create mapping: old_class_id -> new_class_id
    Only for classes that exist in common_names.
    """
    mapping = {}
    for old_id, name in enumerate(old_names):
        if name in common_names:
            new_id = common_names.index(name)
            mapping[old_id] = new_id
    return mapping


def find_image_file(images_dir, base_name):
    """Find image file with supported extensions."""
    for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        candidate = os.path.join(images_dir, base_name + ext)
        if os.path.exists(candidate):
            return candidate
    return None


def convert_dataset(src_root, mapping, dst_root):
    """
    Convert one dataset:
    - Remap class IDs
    - Remove objects not in common classes
    - Copy images
    """

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
        base_name = os.path.splitext(label_file)[0]

        image_file = find_image_file(images_src, base_name)
        if image_file is None:
            continue

        with open(label_path, "r") as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            old_class_id = int(parts[0])

            # Skip classes not in mapping
            if old_class_id not in mapping:
                continue

            new_class_id = mapping[old_class_id]
            new_line = str(new_class_id) + " " + " ".join(parts[1:])
            new_lines.append(new_line)

        # Only save if at least one object remains
        if new_lines:
            shutil.copy(image_file, os.path.join(images_dst, os.path.basename(image_file)))
            with open(os.path.join(labels_dst, label_file), "w") as f:
                f.write("\n".join(new_lines))


# =========================
# Main Execution
# =========================

def main():

    base_path = "../../dataset"

    v4_yaml_path = os.path.join(base_path, "v4", "data.yaml")
    v5_yaml_path = os.path.join(base_path, "v5", "data.yaml")

    v4_yaml = load_yaml(v4_yaml_path)
    v5_yaml = load_yaml(v5_yaml_path)

    v4_names = v4_yaml["names"]
    v5_names = v5_yaml["names"]

    # Compute common classes
    common_classes = sorted(list(set(v4_names).intersection(set(v5_names))))

    print("Common classes:")
    print(common_classes)
    print("Total:", len(common_classes))

    # Create mappings
    mapping_v4 = create_class_mapping(v4_names, common_classes)
    mapping_v5 = create_class_mapping(v5_names, common_classes)

    # Prepare v6 directory
    v6_root = os.path.join(base_path, "v6")

    if os.path.exists(v6_root):
        shutil.rmtree(v6_root)

    os.makedirs(v6_root, exist_ok=True)

    # Convert both datasets
    convert_dataset(os.path.join(base_path, "v4"), mapping_v4, v6_root)
    convert_dataset(os.path.join(base_path, "v5"), mapping_v5, v6_root)

    # Create new YAML config
    v6_yaml = {
        "path": v6_root,
        "images": "images",
        "labels": "labels",
        "nc": len(common_classes),
        "names": common_classes,
        "augment": True
    }

    with open(os.path.join(v6_root, "v6.yaml"), "w") as f:
        yaml.dump(v6_yaml, f, sort_keys=False)

    print("\n✅ v6 dataset successfully created.")


if __name__ == "__main__":
    main()