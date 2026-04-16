import json
import numpy as np
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


# ===================================================
# CONFIG
# ===================================================

GT_ANN = "../../dataset/v6.5_coco/test/_annotations.coco.json"
PRED_FILE = "./runs/rfdetr_test_predictions/predictions.json"

CLASS_NAMES = [
    "a","b","c","d","e","f","g","h","i","l",
    "m","n","o","p","r","s","t","u","v","w","z"
]

IOU_THRESHOLD = 0.5


# ===================================================
# IOU
# ===================================================

def compute_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0]+boxA[2], boxB[0]+boxB[2])
    yB = min(boxA[1]+boxA[3], boxB[1]+boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)

    areaA = boxA[2] * boxA[3]
    areaB = boxB[2] * boxB[3]

    union = areaA + areaB - inter

    return inter / union if union > 0 else 0


# ===================================================
# COCO EVAL
# ===================================================

def evaluate_coco(coco_gt, pred_file):
    print("\n=== COCO Evaluation ===\n")

    coco_dt = coco_gt.loadRes(pred_file)

    coco_eval = COCOeval(coco_gt, coco_dt, "bbox")
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()


# ===================================================
# CONFUSION MATRIX
# ===================================================

def compute_cm(coco_gt, preds):

    num_classes = len(CLASS_NAMES)
    cm = np.zeros((num_classes + 1, num_classes + 1), dtype=int)

    preds_by_image = {}
    for p in preds:
        preds_by_image.setdefault(p["image_id"], []).append(p)

    cat_ids = coco_gt.getCatIds()
    cat_id_to_index = {cat_id: i for i, cat_id in enumerate(cat_ids)}

    for img_id in coco_gt.getImgIds():

        gt_ids = coco_gt.getAnnIds(imgIds=img_id)
        gt_anns = coco_gt.loadAnns(gt_ids)

        gt_boxes = [ann["bbox"] for ann in gt_anns]
        gt_classes = [cat_id_to_index[ann["category_id"]] for ann in gt_anns]

        pred_anns = preds_by_image.get(img_id, [])

        pred_boxes = [p["bbox"] for p in pred_anns]
        pred_classes = [cat_id_to_index[p["category_id"]] for p in pred_anns]

        matched_gt = set()
        matched_pred = set()

        for i, p_box in enumerate(pred_boxes):

            best_iou = 0
            best_j = -1

            for j, g_box in enumerate(gt_boxes):

                if j in matched_gt:
                    continue

                iou = compute_iou(p_box, g_box)

                if iou > best_iou:
                    best_iou = iou
                    best_j = j

            if best_iou >= IOU_THRESHOLD:
                matched_pred.add(i)
                matched_gt.add(best_j)

                cm[gt_classes[best_j]][pred_classes[i]] += 1

        for j, g_cls in enumerate(gt_classes):
            if j not in matched_gt:
                cm[g_cls][num_classes] += 1

        for i, p_cls in enumerate(pred_classes):
            if i not in matched_pred:
                cm[num_classes][p_cls] += 1

    return cm


# ===================================================
# NORMALIZE
# ===================================================

def normalize_cm(cm):
    cm = cm.astype(float)
    row_sums = cm.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return cm / row_sums


# ===================================================
# PLOT
# ===================================================

def plot_cm(cm):

    labels = CLASS_NAMES + ["bg"]

    plt.figure(figsize=(12, 10))
    plt.imshow(cm, cmap='Blues', vmin=0, vmax=1)

    plt.title("Normalized Confusion Matrix (IoU=0.5)")
    plt.colorbar()

    ticks = np.arange(len(labels))
    plt.xticks(ticks, labels, rotation=90)
    plt.yticks(ticks, labels)

    plt.xlabel("Predicted")
    plt.ylabel("Ground Truth")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            value = cm[i, j]
            if value > 0.02:
                plt.text(
                    j, i, f"{value:.2f}",
                    ha='center', va='center',
                    fontsize=6,
                    color='black' if value < 0.5 else 'white'
                )

    plt.tight_layout()
    plt.show()


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":

    coco_gt = COCO(GT_ANN)

    with open(PRED_FILE) as f:
        preds = json.load(f)

    evaluate_coco(coco_gt, PRED_FILE)

    cm = compute_cm(coco_gt, preds)
    cm_norm = normalize_cm(cm)

    plot_cm(cm_norm)