import os
import shutil
from glob import glob
from tqdm import tqdm


# ===================================================
# CONFIG
# ===================================================

BASE = "../../dataset/v4.4"

SRC1 = os.path.join(BASE, "train")
SRC2 = os.path.join(BASE, "train_synth")

DST = os.path.join(BASE, "train_full")

DST_IMG = os.path.join(DST, "images")
DST_LBL = os.path.join(DST, "labels")

os.makedirs(DST_IMG, exist_ok=True)
os.makedirs(DST_LBL, exist_ok=True)


# ===================================================
# HELPERS
# ===================================================

def copy_files(src_dir, dst_dir):
    """Copy all files from src to dst."""
    files = glob(os.path.join(src_dir, "*"))

    for path in tqdm(files, desc=f"Copying {os.path.basename(src_dir)}"):
        dst_path = os.path.join(dst_dir, os.path.basename(path))
        shutil.copy2(path, dst_path)


# ===================================================
# MAIN
# ===================================================

def merge_datasets():
    print("Merging datasets...\n")

    # SRC1
    copy_files(os.path.join(SRC1, "images"), DST_IMG)
    copy_files(os.path.join(SRC1, "labels"), DST_LBL)

    # SRC2
    copy_files(os.path.join(SRC2, "images"), DST_IMG)
    copy_files(os.path.join(SRC2, "labels"), DST_LBL)

    print("\nMerge complete!")


# ===================================================
# RUN
# ===================================================

if __name__ == "__main__":
    merge_datasets()
