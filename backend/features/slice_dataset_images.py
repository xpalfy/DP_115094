import os
import cv2
import glob

BASE_IN = "../../dataset/v4.4"
BASE_OUT = "../../dataset/v4.5"

SPLITS = ["train", "val", "test"]

SLICE = 1040
SRC = 2080
assert SRC == SLICE * 2

OFFSETS = [
    (0,   0),
    (SLICE, 0),
    (0,   SLICE),
    (SLICE, SLICE),
]


def adjust_poly(poly, ox, oy):
    poly_px = [(x * SRC - ox, y * SRC - oy) for (x, y) in poly]
    cropped = [(x, y) for x, y in poly_px if 0 <= x < SLICE and 0 <= y < SLICE]
    if len(cropped) < 3:
        return None
    return [(x / SLICE, y / SLICE) for (x, y) in cropped]


def process_split(split):
    print(f"\nProcessing split: {split}")

    in_img = os.path.join(BASE_IN, split, "images")
    in_lbl = os.path.join(BASE_IN, split, "labels")

    out_img = os.path.join(BASE_OUT, split + "/images")
    out_lbl = os.path.join(BASE_OUT, split + "/labels")
    os.makedirs(out_img, exist_ok=True)
    os.makedirs(out_lbl, exist_ok=True)

    images = sorted(glob.glob(os.path.join(in_img, "*.jpg")))
    print(f" Found {len(images)} images")

    saved_count = 0

    for ipath in images:
        stem = os.path.splitext(os.path.basename(ipath))[0]
        lpath = os.path.join(in_lbl, stem + ".txt")

        img = cv2.imread(ipath)
        if img is None: continue

        objs = []
        if os.path.exists(lpath):
            with open(lpath, "r") as f:
                for ln in f:
                    pr = ln.strip().split()
                    cls = pr[0]
                    coords = list(map(float, pr[1:]))
                    pts = list(zip(coords[0::2], coords[1::2]))
                    objs.append((cls, pts))

        for idx, (ox, oy) in enumerate(OFFSETS):
            slice_img = img[oy:oy+SLICE, ox:ox+SLICE]
            labels_out = []

            for cls, poly in objs:
                new_poly = adjust_poly(poly, ox, oy)
                if new_poly:
                    labels_out.append((cls, new_poly))

            if not labels_out:
                continue

            out_stem = f"{stem}_p{idx:02d}"
            cv2.imwrite(os.path.join(out_img, out_stem + ".jpg"), slice_img)

            with open(os.path.join(out_lbl, out_stem + ".txt"), "w") as f:
                for cls, poly in labels_out:
                    coords = " ".join(f"{x:.6f} {y:.6f}" for x, y in poly)
                    f.write(f"{cls} {coords}\n")

            saved_count += 1

    print(f"Done: saved {saved_count} sliced samples")


if __name__ == "__main__":
    print("Starting dataset slicing v4.5...")
    for split in SPLITS:
        process_split(split)

    print("ALL DONE — v4.5 sliced dataset ready!")
    print(f"Output: {BASE_OUT}")
