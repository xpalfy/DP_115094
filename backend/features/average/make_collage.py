import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# ================= CONFIG =================

# Average image folders
DIR_V4 = "../../average_images_v4"
DIR_V5 = "../../average_images_v5"

# Temporary collages
TEMP_V4 = "collage_v4_tmp.png"
TEMP_V5 = "collage_v5_tmp.png"

# Final slide output
FINAL_OUT = "final_slide_collage.png"

# PowerPoint slide size (16:9 Full HD)
SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080

# Margins (presentation balanced)
OUTER_MARGIN = 40   # slide border spacing
CENTER_GAP = 90     # space between collages

# Collage grid config
UNIFIED_CLASSES = [
    'a','ae','b','c','d','e','f','g','h','i','j','k','l',
    'm','n','o','oe','p','q','r','s','ss','t','u','ue',
    'v','w','x','y','z'
]

COLS = 6
FIG_SCALE = 3.8

# Fonts
LABEL_FONT_SIZE = 22
TITLE_FONT_SIZE = 28

# Export quality
EXPORT_DPI = 300


# ================= LOAD AVERAGE IMAGES =================

def load_average_images(folder):
    images = {}

    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")

    for file in os.listdir(folder):
        if file.startswith("average_") and file.endswith(".png"):
            label = file.replace("average_", "").replace(".png", "")
            path = os.path.join(folder, file)

            img = cv2.imread(path)
            if img is not None:
                images[label] = img

    print(f"Loaded {len(images)} images from {folder}")
    return images


# ================= CREATE SINGLE COLLAGE =================

def create_collage(images_dict, title, output_file):

    rows = int(np.ceil(len(UNIFIED_CLASSES) / COLS))

    fig, axes = plt.subplots(
        rows,
        COLS,
        figsize=(COLS * FIG_SCALE, rows * FIG_SCALE)
    )

    axes = axes.flatten()

    # Title
    plt.suptitle(
        title,
        fontsize=TITLE_FONT_SIZE,
        fontweight="bold",
        y=0.97
    )

    plt.subplots_adjust(top=0.93)

    # Grid
    for i, letter in enumerate(UNIFIED_CLASSES):

        ax = axes[i]

        if letter in images_dict:

            img_rgb = cv2.cvtColor(images_dict[letter], cv2.COLOR_BGR2RGB)
            ax.imshow(img_rgb)

            ax.set_title(
                letter,
                fontsize=LABEL_FONT_SIZE,
                fontweight="bold"
            )

        else:
            ax.axis("off")
            continue

        ax.axis("off")

    # Remove unused cells
    for j in range(len(UNIFIED_CLASSES), len(axes)):
        axes[j].axis("off")

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save temporary collage
    plt.savefig(
        output_file,
        dpi=EXPORT_DPI,
        bbox_inches="tight",
        pad_inches=0.05
    )

    plt.close()

    print(f"Saved temp collage: {output_file}")


# ================= ASPECT RATIO SAFE RESIZE =================

def resize_to_fit(img, max_w, max_h):

    h, w, _ = img.shape

    scale = min(max_w / w, max_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(img, (new_w, new_h))


# ================= BUILD FINAL SLIDE =================

def build_slide(left_path, right_path, output_path):

    left = cv2.imread(left_path)
    right = cv2.imread(right_path)

    if left is None or right is None:
        raise RuntimeError("Temporary collage images missing")

    slide = np.ones(
        (SLIDE_HEIGHT, SLIDE_WIDTH, 3),
        dtype=np.uint8
    ) * 255

    usable_width = SLIDE_WIDTH - 2 * OUTER_MARGIN - CENTER_GAP
    usable_height = SLIDE_HEIGHT - 2 * OUTER_MARGIN

    half_width = usable_width // 2

    left_fit = resize_to_fit(left, half_width, usable_height)
    right_fit = resize_to_fit(right, half_width, usable_height)

    # Vertical centering
    ly = OUTER_MARGIN + (usable_height - left_fit.shape[0]) // 2
    ry = OUTER_MARGIN + (usable_height - right_fit.shape[0]) // 2

    # Horizontal positions
    left_x = OUTER_MARGIN
    right_x = OUTER_MARGIN + half_width + CENTER_GAP

    slide[
        ly:ly + left_fit.shape[0],
        left_x:left_x + left_fit.shape[1]
    ] = left_fit

    slide[
        ry:ry + right_fit.shape[0],
        right_x:right_x + right_fit.shape[1]
    ] = right_fit

    cv2.imwrite(output_path, slide)

    print("FINAL PPT SLIDE IMAGE SAVED:")
    print(output_path)


# ================= MAIN =================

if __name__ == "__main__":

    avg_v4 = load_average_images(DIR_V4)
    avg_v5 = load_average_images(DIR_V5)

    create_collage(avg_v4, "German Dataset (v4)", TEMP_V4)
    create_collage(avg_v5, "French Dataset (v5)", TEMP_V5)

    build_slide(TEMP_V4, TEMP_V5, FINAL_OUT)
