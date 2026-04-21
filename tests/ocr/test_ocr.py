import os
import cv2
import torch
import pytesseract
import easyocr
import numpy as np

# ===================================================
# CONFIG
# ===================================================

INPUT_DIR = "../../dataset/test_ocr"
OUTPUT_DIR = "./runs/ocr_test_predictions"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
reader = easyocr.Reader(["en"], gpu=torch.cuda.is_available())

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===================================================
# IMAGE IO (UNICODE SAFE)
# ===================================================

def read_image(path):
    """Read image with unicode path support."""
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def save_image(path, img):
    """Save image with unicode path support."""
    ext = os.path.splitext(path)[1]
    _, buf = cv2.imencode(ext, img)
    buf.tofile(path)


# ===================================================
# OCR DRAW FUNCTIONS
# ===================================================

def draw_pytesseract(img):
    """Draw bounding boxes from pytesseract."""
    h = img.shape[0]

    try:
        boxes = pytesseract.image_to_boxes(img)

        for b in boxes.splitlines():
            parts = b.split()
            if len(parts) < 5:
                continue

            _, x1, y1, x2, y2 = parts[:5]

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            y1, y2 = h - y2, h - y1

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

    except Exception as e:
        print(f"[pytesseract ERROR] {e}")

    return img


def draw_easyocr(img):
    """Draw bounding boxes from EasyOCR."""
    try:
        results = reader.readtext(img)

        for bbox, _, _ in results:
            xs = [int(p[0]) for p in bbox]
            ys = [int(p[1]) for p in bbox]

            cv2.rectangle(
                img,
                (min(xs), min(ys)),
                (max(xs), max(ys)),
                (255, 0, 0),
                1
            )

    except Exception as e:
        print(f"[easyOCR ERROR] {e}")

    return img


# ===================================================
# MAIN
# ===================================================

def main():
    """Process all images in input folder."""

    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
    ]

    for f in files:
        path = os.path.join(INPUT_DIR, f)
        print("Processing:", f)

        img = read_image(path)
        if img is None:
            print("[ERROR] Cannot read image")
            continue

        base = os.path.splitext(f)[0]

        img_pytess = draw_pytesseract(img.copy())
        img_easy = draw_easyocr(img.copy())

        save_image(os.path.join(OUTPUT_DIR, f"{base}_pytesseract.jpg"), img_pytess)
        save_image(os.path.join(OUTPUT_DIR, f"{base}_easyocr.jpg"), img_easy)

    print("Done")


if __name__ == "__main__":
    main()