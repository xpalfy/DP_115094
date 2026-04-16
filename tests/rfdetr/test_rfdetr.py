import os
import json
import cv2
import torch
import numpy as np
from PIL import Image
import supervision as sv
from pycocotools.coco import COCO
from pycocotools import mask as mask_utils

from rfdetr import RFDETRLarge
from rfdetr import RFDETRSegSmall


# ===================================================
# CONFIG
# ===================================================

MODEL_PATH = "../../backend/runs/combined/rfdetr/detect/train_rf-detr-large/checkpoint_best_total.pth"

TEST_IMAGES = "../../dataset/v6.5_coco/test/images"
TEST_ANN = "../../dataset/v6.5_coco/test/_annotations.coco.json"

OUTPUT_DIR = "./runs/rfdetr_test_predictions"

CLASS_NAMES = [
    "a","b","c","d","e","f","g","h","i","l",
    "m","n","o","p","r","s","t","u","v","w","z"
]

THRESHOLD = 0.5
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===================================================
# MODEL
# ===================================================

def load_model():
    print("Loading model:", MODEL_PATH)

    model = RFDETRLarge(
        pretrain_weights=MODEL_PATH,
        num_classes=len(CLASS_NAMES),
        device=DEVICE
    )

    # model = RFDETRSegSmall(
    #     pretrain_weights=MODEL_PATH,
    #     num_classes=len(CLASS_NAMES),
    #     device=DEVICE
    # )

    model.optimize_for_inference()

    print("Model loaded\n")
    return model


# ===================================================
# DATA
# ===================================================

def load_dataset():
    dataset = sv.DetectionDataset.from_coco(
        images_directory_path=TEST_IMAGES,
        annotations_path=TEST_ANN
    )

    coco_gt = COCO(TEST_ANN)

    image_name_to_id = {
        img["file_name"]: img["id"]
        for img in coco_gt.dataset["images"]
    }

    print("Test images:", len(dataset))
    return dataset, image_name_to_id


# ===================================================
# HELPERS
# ===================================================

def has_masks(detections):
    return (
        hasattr(detections, "mask")
        and detections.mask is not None
        and len(detections.mask) > 0
    )


def create_labels(detections):
    return [
        f"{CLASS_NAMES[int(c)]} {float(conf):.2f}"
        for c, conf in zip(detections.class_id, detections.confidence)
    ]


def binary_mask_to_coco_rle(binary_mask):
    """ Convert binary mask to COCO RLE. """
    binary_mask = np.asfortranarray(binary_mask.astype(np.uint8))
    rle = mask_utils.encode(binary_mask)
    rle["counts"] = rle["counts"].decode("utf-8")
    return rle


# ===================================================
# PREDICTIONS
# ===================================================

def convert_to_coco_predictions(detections, image_id):
    preds = []

    segmentation_mode = has_masks(detections)

    if segmentation_mode:
        for box, conf, cls, mask in zip(
            detections.xyxy,
            detections.confidence,
            detections.class_id,
            detections.mask
        ):
            x1, y1, x2, y2 = box

            coco_rle = binary_mask_to_coco_rle(mask)

            preds.append({
                "image_id": image_id,
                "category_id": int(cls),
                "bbox": [
                    float(x1),
                    float(y1),
                    float(x2 - x1),
                    float(y2 - y1)
                ],
                "segmentation": coco_rle,
                "score": float(conf)
            })
    else:
        for box, conf, cls in zip(
            detections.xyxy,
            detections.confidence,
            detections.class_id
        ):
            x1, y1, x2, y2 = box

            preds.append({
                "image_id": image_id,
                "category_id": int(cls),
                "bbox": [
                    float(x1),
                    float(y1),
                    float(x2 - x1),
                    float(y2 - y1)
                ],
                "score": float(conf)
            })

    return preds


# ===================================================
# VISUALIZATION
# ===================================================

def annotate_image(image, detections, box_annotator, label_annotator, mask_annotator):
    labels = create_labels(detections)
    annotated = image.copy()

    if has_masks(detections):
        annotated = mask_annotator.annotate(annotated, detections)
    else:
        annotated = box_annotator.annotate(annotated, detections)

    annotated = label_annotator.annotate(annotated, detections, labels)
    return annotated


# ===================================================
# INFERENCE LOOP
# ===================================================

def run_inference(model, dataset, image_name_to_id):
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    mask_annotator = sv.MaskAnnotator()

    predictions = []

    for image_name, image, _ in dataset:
        pil_image = Image.fromarray(image)

        detections = model.predict(
            pil_image,
            threshold=THRESHOLD
        )

        file_name = os.path.basename(image_name)
        image_id = image_name_to_id[file_name]

        mode = "segmentation" if has_masks(detections) else "detection"
        print(f"{file_name} -> {mode}, detections: {len(detections)}")

        preds = convert_to_coco_predictions(detections, image_id)
        predictions.extend(preds)

        annotated = annotate_image(
            image,
            detections,
            box_annotator,
            label_annotator,
            mask_annotator
        )

        save_path = os.path.join(OUTPUT_DIR, file_name)
        cv2.imwrite(save_path, annotated)

    return predictions


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":
    model = load_model()

    dataset, image_name_to_id = load_dataset()

    predictions = run_inference(model, dataset, image_name_to_id)

    pred_file = os.path.join(OUTPUT_DIR, "predictions.json")
    with open(pred_file, "w") as f:
        json.dump(predictions, f)

    print("\nFinished testing.")
    print("Results saved to:", OUTPUT_DIR)