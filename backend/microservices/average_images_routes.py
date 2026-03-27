import os
import yaml
from flask import request, jsonify, send_from_directory

# Allowed dataset versions
ALLOWED_VERSIONS = {"v4", "v5", "v6", "v4.1", "v5.1", "v6.1"}


def get_version(version: str) -> str:
    """Return a valid version, fallback to v4 if invalid."""
    return version if version in ALLOWED_VERSIONS else "v4"


def get_dataset_dir(version: str) -> str:
    """Get dataset directory path."""
    version = get_version(version)
    return f"./dataset/{version}"


def get_average_image_dir(version: str) -> str:
    """Get average images directory path."""
    version = get_version(version)
    return f"average_images_{version}"


def load_class_names(version: str):
    """Load class names from data.yaml."""
    dataset_dir = get_dataset_dir(version)
    yaml_path = os.path.join(dataset_dir, "data.yaml")

    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"data.yaml not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    names = data.get("names")
    if not names:
        raise ValueError(f"'names' missing in {yaml_path}")

    return names


def register_average_images_routes(app):

    @app.route("/average_images/files/<path:filename>")
    def serve_average_image(filename):
        """Serve a single average image file."""
        version = get_version(request.args.get("v", "v4"))
        avg_dir = get_average_image_dir(version)

        if not os.path.exists(avg_dir):
            return jsonify({"error": f"Directory not found: {avg_dir}"}), 404

        return send_from_directory(avg_dir, filename)

    @app.route("/average_images", methods=["GET"])
    def get_average_images():
        """Return available average images grouped by class."""
        version = get_version(request.args.get("v", "v4"))
        avg_dir = get_average_image_dir(version)

        if not os.path.exists(avg_dir):
            return jsonify({"error": f"Directory not found: {avg_dir}"}), 404

        try:
            class_names = load_class_names(version)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        images = {}

        # Check which average images exist
        for cls in class_names:
            filename = f"average_{cls}.png"
            file_path = os.path.join(avg_dir, filename)

            if os.path.exists(file_path):
                images[cls] = (
                    f"http://localhost:5000/average_images/files/"
                    f"{filename}?v={version}"
                )

        return jsonify({
            "version": version,
            "nc": len(class_names),
            "count": len(images),
            "images": images
        })