import os
import cv2
import glob
import math
import random
import numpy as np
from collections import defaultdict, Counter
import albumentations as A
from tqdm import tqdm

# -------------------------------
# CONFIGURATION
# -------------------------------
BASE = "../../dataset/v4.4"
SPLIT = "train"

IMG_DIR = os.path.join(BASE, SPLIT, "images")
LBL_DIR = os.path.join(BASE, SPLIT, "labels")

OUT_SPLIT = "train_synth"
OUT_IMG_DIR = os.path.join(BASE, OUT_SPLIT, "images")
OUT_LBL_DIR = os.path.join(BASE, OUT_SPLIT, "labels")

os.makedirs(OUT_IMG_DIR, exist_ok=True)
os.makedirs(OUT_LBL_DIR, exist_ok=True)

TARGET_PER_CLASS = 2200

CANVAS_W = 2080
CANVAS_H = 2080

CHARS_PER_IMG_RANGE = (120, 150)
PLACEMENT_TRIES = 60

crop_aug = A.Compose([
    A.Affine(
        scale=(0.90, 1.20),
        rotate=(-10, 10),
        translate_percent=(-0.03, 0.03),
        shear=(-4, 4),
        fit_output=True,
        p=1.0
    ),
    A.RandomBrightnessContrast(
        brightness_limit=0.12,
        contrast_limit=0.18,
        p=0.4
    ),
    A.GaussianBlur(
        blur_limit=(3, 3),
        p=0.15
    ),
    A.GaussNoise(
        var_limit=(5.0, 18.0),
        p=0.25
    ),
], keypoint_params=A.KeypointParams(format="xy", remove_invisible=False))

MIN_DIAG = 25
MAX_DIAG = 260
IMG_EXTS = (".jpg", ".jpeg", ".png")

# -------------------------------
# UTILITIES
# -------------------------------
def read_yolo_seg(path):
    objs = []
    if not os.path.exists(path):
        return objs
    with open(path, "r") as f:
        for ln in f:
            pr = ln.strip().split()
            if len(pr) < 5:
                continue
            cls = pr[0]
            coords = list(map(float, pr[1:]))
            pts = list(zip(coords[0::2], coords[1::2]))
            objs.append((cls, pts))
    return objs

def poly_norm_to_px(poly, w, h):
    return [(x * w, y * h) for x, y in poly]

def poly_px_to_norm(poly, w, h):
    return [(max(0, min(1, x / w)), max(0, min(1, y / h))) for x, y in poly]

def bbox(poly):
    xs, ys = zip(*poly)
    return int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))

def crop_char(img, poly):
    x1, y1, x2, y2 = bbox(poly)
    crop = img[y1:y2+1, x1:x2+1]
    poly_rel = [(x - x1, y - y1) for x, y in poly]
    return crop, poly_rel

def mask_from_poly(poly, shape):
    mask = np.zeros(shape, np.uint8)
    poly_int = np.array(poly, np.int32).reshape(-1, 1, 2)
    cv2.fillPoly(mask, [poly_int], 255)
    return mask

def diag(poly):
    x1, y1, x2, y2 = bbox(poly)
    return math.hypot(x2 - x1, y2 - y1)

def resize_inst(img, poly, target):
    d = diag(poly)
    if d < 1e-6:
        return img, poly
    s = target / d
    new_h = max(2, int(round(img.shape[0] * s)))
    new_w = max(2, int(round(img.shape[1] * s)))
    img2 = cv2.resize(img, (new_w, new_h))
    poly2 = [(x * s, y * s) for x, y in poly]
    return img2, poly2

def no_overlap(canvas_mask, msk, top, left):
    H, W = canvas_mask.shape
    h, w = msk.shape
    if top < 0 or left < 0 or top + h > H or left + w > W:
        return False
    region = canvas_mask[top:top + h, left:left + w]
    overlap = cv2.bitwise_and(region, msk)
    return overlap.sum() <= msk.sum() * 0.05

# -------------------------------
# LOAD INSTANCES
# -------------------------------
print("Loading character instances...")

instances = defaultdict(list)
class_counts = Counter()

for ipath in tqdm(sorted(glob.glob(os.path.join(IMG_DIR, "*")))):
    if os.path.splitext(ipath)[1].lower() not in IMG_EXTS:
        continue
    stem = os.path.splitext(os.path.basename(ipath))[0]
    lpath = os.path.join(LBL_DIR, stem + ".txt")
    objs = read_yolo_seg(lpath)
    if not objs:
        continue

    img = cv2.imread(ipath)
    if img is None:
        continue
    H, W = img.shape[:2]

    for cls, poly in objs:
        poly_px = poly_norm_to_px(poly, W, H)
        crop_img, poly_rel = crop_char(img, poly_px)
        if crop_img.size == 0:
            continue
        instances[cls].append((crop_img, poly_rel))
        class_counts[cls] += 1

print("\nOriginal objects per class:")
for c in sorted(class_counts.keys(), key=int):
    print(f"  Class {c}: {class_counts[c]}")

# -------------------------------
# COMPUTE BALANCING NEEDS
# -------------------------------
need = {c: max(0, TARGET_PER_CLASS - class_counts[c]) for c in class_counts}

print("\nRequired synthetic objects:")
for c in sorted(need.keys(), key=int):
    print(f"  Class {c}: {need[c]}")

total_needed = sum(need.values())
avg_chars = sum(CHARS_PER_IMG_RANGE) / 2
NUM_SYNTH = max(100, int(total_needed / avg_chars))

print(f"\nEstimated {NUM_SYNTH} synthetic images to generate.\n")

weights = np.array([need[c] for c in class_counts])
weights = weights / weights.sum() if weights.sum() > 0 else np.ones_like(weights) / len(weights)
classes = list(class_counts.keys())

# -------------------------------
# SYNTHETIC IMAGE GENERATION
# -------------------------------
created = Counter()
img_i = 0

for _ in tqdm(range(NUM_SYNTH)):
    canvas = np.full((CANVAS_H, CANVAS_W, 3), 255, np.uint8)
    mcanvas = np.zeros((CANVAS_H, CANVAS_W), np.uint8)
    labels_out = []

    n_chars = random.randint(*CHARS_PER_IMG_RANGE)

    for _ in range(n_chars):
        cls = np.random.choice(classes, p=weights)
        if created[cls] >= need[cls] or not instances[cls]:
            continue

        crop, poly_rel = random.choice(instances[cls])
        kps = [(float(x), float(y)) for x, y in poly_rel]

        try:
            aug = crop_aug(image=crop, keypoints=kps)
        except:
            continue

        ci, pi = aug["image"], aug["keypoints"]
        m = mask_from_poly(pi, ci.shape[:2])
        if m.sum() < 10:
            continue

        target = random.randint(MIN_DIAG, MAX_DIAG)
        ci2, pi2 = resize_inst(ci, pi, target)
        m2 = mask_from_poly(pi2, ci2.shape[:2])

        h, w = ci2.shape[:2]
        placed = False
        for _t in range(PLACEMENT_TRIES):
            top = random.randint(0, CANVAS_H - h)
            left = random.randint(0, CANVAS_W - w)
            if no_overlap(mcanvas, m2, top, left):
                roi = canvas[top:top+h, left:left+w]
                canvas[top:top+h, left:left+w] = np.where(m2[..., None] > 0, ci2, roi)
                mcanvas[top:top+h, left:left+w] |= m2
                poly_canvas = [(x + left, y + top) for x, y in pi2]
                poly_norm = poly_px_to_norm(poly_canvas, CANVAS_W, CANVAS_H)
                labels_out.append(" ".join([cls] + [f"{x:.6f} {y:.6f}" for (x, y) in poly_norm]))
                created[cls] += 1
                placed = True
                break

        if created[cls] >= need[cls]:
            continue

    if labels_out:
        img_i += 1
        stem = f"synth_{img_i:05d}"
        cv2.imwrite(os.path.join(OUT_IMG_DIR, stem + ".jpg"), canvas)
        with open(os.path.join(OUT_LBL_DIR, stem + ".txt"), "w") as f:
            f.write("\n".join(labels_out))

print("\nDone — Synthetic dataset generated.")
print("\nGenerated per class:")
for c in sorted(created.keys(), key=int):
    print(f"  Class {c}: {created[c]}")
