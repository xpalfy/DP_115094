import os
import shutil
from glob import glob
from tqdm import tqdm

BASE = "../../dataset/v4.4"
SRC1 = os.path.join(BASE, "train")
SRC2 = os.path.join(BASE, "train_synth")
DST = os.path.join(BASE, "train_full")

DST_IMG = os.path.join(DST, "images")
DST_LBL = os.path.join(DST, "labels")

os.makedirs(DST_IMG, exist_ok=True)
os.makedirs(DST_LBL, exist_ok=True)

def merge(src_dir, dst_dir):
    for path in tqdm(glob(os.path.join(src_dir, "*"))):
        shutil.copy2(path, os.path.join(dst_dir, os.path.basename(path)))

print("Merging datasets.")

merge(os.path.join(SRC1, "images"), DST_IMG)
merge(os.path.join(SRC1, "labels"), DST_LBL)
merge(os.path.join(SRC2, "images"), DST_IMG)
merge(os.path.join(SRC2, "labels"), DST_LBL)

print("Merge complete!")
