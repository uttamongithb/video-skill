#!/usr/bin/env python3
"""Matte the presenter PNGs: pure-white ground -> alpha, erode 1px, feather 0.8px."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = Path(__file__).resolve().parent.parent / "assets" / "presenter"
OUT = SRC / "cut"

TOL = 12          # per-channel tolerance for "this is background white"
FEATHER = 0.8


def cut(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    # distance from pure white, per pixel
    dist = np.abs(255 - a).max(axis=2)
    background = dist <= TOL
    # only background connected to the border counts
    lbl, n = ndimage.label(background)
    border = np.concatenate([lbl[0, :], lbl[-1, :], lbl[:, 0], lbl[:, -1]])
    keep = set(np.unique(border)) - {0}
    bg = np.isin(lbl, list(keep))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # erode the subject by 1 px so no white halo survives, then feather
    alpha = ndimage.binary_erosion(alpha > 0, iterations=1).astype(np.uint8) * 255
    am = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(FEATHER))
    out = im.convert("RGBA")
    out.putalpha(am)
    # trim transparent margins
    bbox = am.getbbox()
    if bbox:
        out = out.crop(bbox)
    return out


def main():
    OUT.mkdir(exist_ok=True)
    files = sorted(SRC.glob("p*.png")) + [SRC / "base_present.png"]
    for f in files:
        if not f.exists():
            continue
        im = cut(f)
        # normalise height to 1200 px so placement maths is stable across poses
        h = 1200
        w = round(im.width * h / im.height)
        im = im.resize((w, h), Image.LANCZOS)
        dst = OUT / f.name
        im.save(dst)
        # halo report: mean alpha in a 6px ring just outside the subject
        arr = np.asarray(im)[..., 3]
        print(f"{f.name:22s} {im.width}x{im.height}  opaque={100*(arr>200).mean():.1f}%")


if __name__ == "__main__":
    main()
