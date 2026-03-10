import os
import yaml
from flask import request, jsonify, send_from_directory

ALLOWED_VERSIONS = {"v4", "v5", "v6"}

def get_dataset_dir(version: str) -> str:
    if version not in ALLOWED_VERSIONS:
        version = "v4"
    return f"./dataset/{version}"

def get_average_image_dir(version: str) -> str:
    if version not in ALLOWED_VERSIONS:
        version = "v4"
    return f"average_images_{version}"

def load_class_names(version: str):
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
        version = request.args.get("v", "v4")
        avg_dir = get_average_image_dir(version)

        if not os.path.exists(avg_dir):
            return jsonify({"error": f"Directory not found: {avg_dir}"}), 404

        return send_from_directory(avg_dir, filename)

    @app.route("/average_images", methods=["GET"])
    def get_average_images():
        version = request.args.get("v", "v4")
        avg_dir = get_average_image_dir(version)

        if not os.path.exists(avg_dir):
            return jsonify({"error": f"Directory not found: {avg_dir}"}), 404

        try:
            class_names = load_class_names(version)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        images = {}
        for cls in class_names:
            fname = f"average_{cls}.png"
            if os.path.exists(os.path.join(avg_dir, fname)):
                images[cls] = f"http://localhost:5000/average_images/files/{fname}?v={version}"

        return jsonify({
            "version": version,
            "nc": len(class_names),
            "count": len(images),
            "images": images
        })