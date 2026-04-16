import os
import cv2
import random
from flask import request, jsonify, send_from_directory

ALLOWED_VERSIONS = {"v4", "v5", "v6", "v4.4", "v5.4", "v6.4"}
SPLIT_VERSIONS = {"v4.4", "v5.4", "v6.4"}


def get_version(version: str) -> str:
    """Return valid version or fallback to v4."""
    return version if version in ALLOWED_VERSIONS else "v4"


def get_dataset_dir(version: str) -> str:
    """Return dataset directory path."""
    return f"./dataset/{get_version(version)}"


def resolve_dir(base_dir: str, split: str, subfolder: str) -> str:
    """Try split-based directory first, fallback to root-level directory."""
    if split:
        path = os.path.join(base_dir, split, subfolder)
        if os.path.exists(path):
            return path

    return os.path.join(base_dir, subfolder)


def register_dataset_images_routes(app):

    @app.route("/dataset/images/<path:filename>")
    def serve_dataset_image(filename):
        """Serve dataset image file."""
        version = get_version(request.args.get("v", "v4"))
        raw_split = request.args.get("split")

        if version in SPLIT_VERSIONS:
            split = raw_split or "train"
        else:
            split = None

        dataset_dir = get_dataset_dir(version)
        img_dir = resolve_dir(dataset_dir, split, "images")

        if not os.path.exists(img_dir):
            return jsonify({"error": f"Image dir not found: {img_dir}"}), 404

        return send_from_directory(img_dir, filename)

    @app.route("/sample_images", methods=["GET"])
    def get_sample_images():
        """Return random sample images with annotations."""
        num = int(request.args.get("num", 6))
        version = get_version(request.args.get("v", "v4"))
        raw_split = request.args.get("split")

        if version in SPLIT_VERSIONS:
            split = raw_split or "train"
        else:
            split = None

        dataset_dir = get_dataset_dir(version)
        img_dir = resolve_dir(dataset_dir, split, "images")
        label_dir = resolve_dir(dataset_dir, split, "labels")

        if not os.path.exists(img_dir) or not os.path.exists(label_dir):
            return jsonify({
                "error": "Dataset directories not found",
                "img_dir": img_dir,
                "label_dir": label_dir
            }), 404

        img_files = [
            f for f in os.listdir(img_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if not img_files:
            return jsonify({"error": "No images found"}), 404

        sampled_files = random.sample(img_files, min(len(img_files), num))
        results = []

        for filename in sampled_files:
            img_path = os.path.join(img_dir, filename)
            img = cv2.imread(img_path)

            if img is None:
                continue

            h, w, _ = img.shape
            annotations = []

            label_path = os.path.join(
                label_dir,
                os.path.splitext(filename)[0] + ".txt"
            )

            if os.path.exists(label_path):
                with open(label_path) as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) < 3:
                            continue

                        coords = list(map(float, parts[1:]))

                        polygon = [
                            [
                                int(coords[i] * w),
                                int(coords[i + 1] * h)
                            ]
                            for i in range(0, len(coords), 2)
                        ]

                        annotations.append({
                            "class": parts[0],
                            "polygon": polygon
                        })

            image_url = f"http://localhost:5000/dataset/images/{filename}?v={version}"

            if split:
                image_url += f"&split={split}"

            results.append({
                "filename": filename,
                "width": w,
                "height": h,
                "image_url": image_url,
                "annotations": annotations
            })

        return jsonify({
            "version": version,
            "split": split,
            "count": len(results),
            "images": results
        })