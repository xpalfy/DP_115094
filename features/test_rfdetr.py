import os
import json
import cv2
from PIL import Image
import supervision as sv
from rfdetr import RFDETRBase
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

# -------------------------
# PATHS
# -------------------------
MODEL_PATH = "../backend/runs/combined/rfdetr/detect/train_rf-detr-base/checkpoint_best_total.pth"
TEST_IMAGES = "../dataset/v6.5_coco/test/images"
TEST_ANN = "../dataset/v6.5_coco/test/_annotations.coco.json"
OUTPUT_DIR = "../backend/runs/rfdetr_test_predictions"

# -------------------------
# CLASSES
# -------------------------
CLASS_NAMES = [
    "a","b","c","d","e","f","g","h","i","l",
    "m","n","o","p","r","s","t","u","v","w","z"
]

THRESHOLD = 0.25
DEVICE = "cuda"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading model:", MODEL_PATH)

# -------------------------
# MODEL
# -------------------------
model = RFDETRBase(
    pretrain_weights=MODEL_PATH,
    num_classes=len(CLASS_NAMES),
    device=DEVICE
)

# gyorsabb inference
model.optimize_for_inference()

print("Model loaded\n")

# -------------------------
# LOAD DATASET
# -------------------------
dataset = sv.DetectionDataset.from_coco(
    images_directory_path=TEST_IMAGES,
    annotations_path=TEST_ANN
)

print("Test images:", len(dataset))

# -------------------------
# ANNOTATORS
# -------------------------
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# -------------------------
# COCO GROUND TRUTH
# -------------------------
coco_gt = COCO(TEST_ANN)

image_name_to_id = {
    img["file_name"]: img["id"]
    for img in coco_gt.dataset["images"]
}

# -------------------------
# PREDICTIONS STORAGE
# -------------------------
predictions = []

# -------------------------
# INFERENCE LOOP
# -------------------------
for image_name, image, gt_detections in dataset:

    pil_image = Image.fromarray(image)

    detections = model.predict(
        pil_image,
        threshold=THRESHOLD
    )

    file_name = os.path.basename(image_name)

    print(file_name, "-> detections:", len(detections))

    image_id = image_name_to_id[file_name]

    # -------------------------
    # SAVE COCO FORMAT PREDICTIONS
    # -------------------------
    for box, conf, cls in zip(
        detections.xyxy,
        detections.confidence,
        detections.class_id
    ):

        x1, y1, x2, y2 = box

        predictions.append({
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

    # -------------------------
    # CREATE LABELS
    # -------------------------
    labels = [
        f"{CLASS_NAMES[int(c)]} {float(conf):.2f}"
        for c, conf in zip(detections.class_id, detections.confidence)
    ]

    # -------------------------
    # DRAW DETECTIONS
    # -------------------------
    annotated = box_annotator.annotate(image, detections)
    annotated = label_annotator.annotate(annotated, detections, labels)

    # -------------------------
    # SAVE IMAGE
    # -------------------------
    save_path = os.path.join(OUTPUT_DIR, file_name)

    cv2.imwrite(save_path, annotated)

# -------------------------
# SAVE PREDICTIONS JSON
# -------------------------
pred_file = os.path.join(OUTPUT_DIR, "predictions.json")

with open(pred_file, "w") as f:
    json.dump(predictions, f)

# -------------------------
# COCO EVALUATION
# -------------------------
print("\nRunning COCO evaluation...\n")

coco_dt = coco_gt.loadRes(pred_file)

coco_eval = COCOeval(coco_gt, coco_dt, "bbox")
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()

print("\nFinished testing.")
print("Results saved to:", OUTPUT_DIR)