import os
import json
import cv2
import torch
from PIL import Image
import supervision as sv
from rfdetr import RFDETRBase
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


# ===================================================
# CONFIG
# ===================================================

MODEL_PATH = "../backend/runs/combined/rfdetr/detect/train_rf-detr-base/checkpoint_best_total.pth"

TEST_IMAGES = "../dataset/v6.5_coco/test/images"
TEST_ANN = "../dataset/v6.5_coco/test/_annotations.coco.json"

OUTPUT_DIR = "../backend/runs/rfdetr_test_predictions"

CLASS_NAMES = [
    "a","b","c","d","e","f","g","h","i","l",
    "m","n","o","p","r","s","t","u","v","w","z"
]

THRESHOLD = 0.25
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===================================================
# MODEL
# ===================================================

def load_model():
    """Load RF-DETR model."""
    print("Loading model:", MODEL_PATH)

    model = RFDETRBase(
        pretrain_weights=MODEL_PATH,
        num_classes=len(CLASS_NAMES),
        device=DEVICE
    )

    model.optimize_for_inference()

    print("Model loaded\n")
    return model


# ===================================================
# DATA
# ===================================================

def load_dataset():
    """Load dataset and COCO ground truth."""
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

    return dataset, coco_gt, image_name_to_id


# ===================================================
# PREDICTIONS
# ===================================================

def convert_to_coco_predictions(detections, image_id):
    """Convert model output to COCO format."""
    preds = []

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


def create_labels(detections):
    """Create text labels."""
    return [
        f"{CLASS_NAMES[int(c)]} {float(conf):.2f}"
        for c, conf in zip(detections.class_id, detections.confidence)
    ]


# ===================================================
# VISUALIZATION
# ===================================================

def annotate_image(image, detections, box_annotator, label_annotator):
    """Draw boxes and labels."""
    labels = create_labels(detections)

    annotated = box_annotator.annotate(image, detections)
    annotated = label_annotator.annotate(annotated, detections, labels)

    return annotated


# ===================================================
# INFERENCE LOOP
# ===================================================

def run_inference(model, dataset, image_name_to_id):
    """Run inference and save predictions."""

    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    predictions = []

    for image_name, image, _ in dataset:

        pil_image = Image.fromarray(image)

        detections = model.predict(
            pil_image,
            threshold=THRESHOLD
        )

        file_name = os.path.basename(image_name)
        image_id = image_name_to_id[file_name]

        print(file_name, "-> detections:", len(detections))

        # COCO predictions
        preds = convert_to_coco_predictions(detections, image_id)
        predictions.extend(preds)

        # Visualization
        annotated = annotate_image(
            image,
            detections,
            box_annotator,
            label_annotator
        )

        save_path = os.path.join(OUTPUT_DIR, file_name)
        cv2.imwrite(save_path, annotated)

    return predictions


# ===================================================
# EVALUATION
# ===================================================

def evaluate_coco(coco_gt, pred_file):
    """Run COCO evaluation."""
    print("\nRunning COCO evaluation...\n")

    coco_dt = coco_gt.loadRes(pred_file)

    coco_eval = COCOeval(coco_gt, coco_dt, "bbox")
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":

    model = load_model()

    dataset, coco_gt, image_name_to_id = load_dataset()

    predictions = run_inference(model, dataset, image_name_to_id)

    pred_file = os.path.join(OUTPUT_DIR, "predictions.json")

    with open(pred_file, "w") as f:
        json.dump(predictions, f)

    evaluate_coco(coco_gt, pred_file)

    print("\nFinished testing.")
    print("Results saved to:", OUTPUT_DIR)
