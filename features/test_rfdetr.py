import os
from PIL import Image
import supervision as sv
from rfdetr import RFDETRBase

# ---- PATHS ----
MODEL_PATH = "../backend/runs/combined/rfdetr/train_rf-detr-base/checkpoint_best_total.pth"
TEST_IMAGES = "../dataset/v6.5_coco/test/images"
OUTPUT_DIR = "../backend/runs/rf_detr/test_predictions"

# ---- CLASSES ----
CLASS_NAMES = [
    "a","b","c","d","e","f","g","h","i","l",
    "m","n","o","p","r","s","t","u","v","w","z"
]

THRESHOLD = 0.5
DEVICE = "cuda"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading model:", MODEL_PATH)

# ---- MODEL ----
model = RFDETRBase(
    pretrain_weights=MODEL_PATH,
    num_classes=len(CLASS_NAMES),
    device=DEVICE
)

print("Model loaded\n")

# ---- LOAD TEST IMAGES ----
images = [
    f for f in os.listdir(TEST_IMAGES)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

print("Test images:", len(images))

# ---- ANNOTATORS ----
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# ---- INFERENCE LOOP ----
for img_name in images:

    img_path = os.path.join(TEST_IMAGES, img_name)

    image = Image.open(img_path).convert("RGB")

    detections = model.predict(
        image,
        threshold=THRESHOLD
    )

    print(img_name, "-> detections:", len(detections))

    labels = [
        f"{CLASS_NAMES[int(c)]} {float(conf):.2f}"
        for c, conf in zip(detections.class_id, detections.confidence)
    ]

    annotated = box_annotator.annotate(image, detections)
    annotated = label_annotator.annotate(annotated, detections, labels)

    save_path = os.path.join(OUTPUT_DIR, img_name)

    annotated.save(save_path)

print("\nFinished testing.")
print("Results saved to:", OUTPUT_DIR)