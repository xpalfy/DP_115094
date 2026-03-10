import os
import cv2
import random
from flask import request, jsonify, send_from_directory

ALLOWED_VERSIONS = {"v4", "v5", "v6"}

def get_dataset_dir(version: str) -> str:
    if version not in ALLOWED_VERSIONS:
        version = "v4"
    return f"./dataset/{version}"


def register_dataset_images_routes(app):

    @app.route("/dataset/images/<path:filename>")
    def serve_dataset_image(filename):
        split = request.args.get("split", "train")
        version = request.args.get("v", "v4")

        dataset_dir = get_dataset_dir(version)

        img_dir = os.path.join(dataset_dir, split, "images")
        if not os.path.exists(img_dir):
            img_dir = os.path.join(dataset_dir, "images")

        if not os.path.exists(img_dir):
            return jsonify({"error": f"Image dir not found: {img_dir}"}), 404

        return send_from_directory(img_dir, filename)

    @app.route("/sample_images", methods=["GET"])
    def get_sample_images():
        num = int(request.args.get("num", 6))
        split = request.args.get("split", "train")
        version = request.args.get("v", "v4")

        dataset_dir = get_dataset_dir(version)

        img_dir = os.path.join(dataset_dir, split, "images")
        label_dir = os.path.join(dataset_dir, split, "labels")

        if not os.path.exists(img_dir):
            img_dir = os.path.join(dataset_dir, "images")

        if not os.path.exists(label_dir):
            label_dir = os.path.join(dataset_dir, "labels")

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

        sampled = random.sample(img_files, min(len(img_files), num))
        results = []

        for file in sampled:
            img_path = os.path.join(img_dir, file)
            img = cv2.imread(img_path)
            if img is None:
                continue

            h, w, _ = img.shape
            annotations = []

            label_path = os.path.join(label_dir, os.path.splitext(file)[0] + ".txt")
            if os.path.exists(label_path):
                with open(label_path) as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) < 3:
                            continue

                        coords = list(map(float, parts[1:]))

                        polygon = []
                        for i in range(0, len(coords), 2):
                            polygon.append([
                                int(coords[i] * w),
                                int(coords[i + 1] * h)
                            ])

                        annotations.append({
                            "class": parts[0],
                            "polygon": polygon
                        })

            results.append({
                "filename": file,
                "width": w,
                "height": h,
                "image_url": f"http://localhost:5000/dataset/images/{file}?v={version}&split={split}",
                "annotations": annotations
            })

        return jsonify({
            "version": version,
            "split": split,
            "count": len(results),
            "images": results
        })