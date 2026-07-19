#!/usr/bin/env python3
"""Prep a photo for ASCII conversion: remove bg, boost contrast, composite on white."""
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def main(photo_path: str):
    img = Image.open(photo_path)
    img_no_bg = remove(img)
    arr = np.array(img_no_bg.convert("L"))
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(arr)
    white_bg = Image.new("L", enhanced.shape[::-1], 255)
    fg = Image.fromarray(enhanced)
    mask = img_no_bg.split()[3] if len(img_no_bg.split()) == 4 else None
    white_bg.paste(fg, mask=mask)
    out = Path("data/source-prepped.png")
    white_bg.save(out)
    print(f"Saved prepped image to {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <photo.jpg>")
        sys.exit(1)
    main(sys.argv[1])