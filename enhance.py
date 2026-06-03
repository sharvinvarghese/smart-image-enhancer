#!/usr/bin/env python

import argparse
import os
from pathlib import Path

import cv2
import numpy as np

from src.algorithms import AVAILABLE_ALGOS
from src.io_utils import load_image, save_image


def parse_args():
    parser = argparse.ArgumentParser(
        description="Smart image enhancement CLI with multiple algorithms (CLAHE, AHE, Retinex, tone mapping, etc.)."
    )
    parser.add_argument("--input", "-i", type=str, required=True, help="Input folder containing images.")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output folder to write enhanced images.")
    parser.add_argument(
        "--algo",
        "-a",
        type=str,
        default="clahe",
        choices=list(AVAILABLE_ALGOS.keys()) + ["all"],
        help="Which algorithm to apply. Use 'all' to run every available algorithm.",
    )
    parser.add_argument(
        "--auto-params",
        action="store_true",
        help="Use simple image statistics to auto-tune algorithm parameters where supported.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.is_dir():
        raise ValueError(f"Input path {input_dir} is not a directory")

    print(f"[smart-image-enhancer] Input  : {input_dir.resolve()}")
    print(f"[smart-image-enhancer] Output : {output_dir.resolve()}")
    print(f"[smart-image-enhancer] Algo   : {args.algo}")
    print(f"[smart-image-enhancer] Auto-params: {args.auto_params}")

    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

    processed = 0
    skipped = 0

    for root, _, files in os.walk(input_dir):
        for fname in files:
            ext = Path(fname).suffix.lower()
            if ext not in exts:
                print(f"  [skip] {fname} — unsupported extension '{ext}'")
                skipped += 1
                continue

            in_path = Path(root) / fname
            rel_path = in_path.relative_to(input_dir)

            print(f"  [load] {rel_path}")
            img = load_image(str(in_path))
            print(f"         shape={img.shape}, dtype={img.dtype}")

            algos_to_run = (
                list(AVAILABLE_ALGOS.keys()) if args.algo == "all" else [args.algo]
            )

            base_stem = rel_path.stem

            for algo_name in algos_to_run:
                print(f"  [algo] Running '{algo_name}' on {fname} ...")
                enhance_fn = AVAILABLE_ALGOS[algo_name]
                enhanced = enhance_fn(img, auto_params=args.auto_params)

                out_subdir = output_dir / rel_path.parent
                out_subdir.mkdir(parents=True, exist_ok=True)

                out_name = f"{base_stem}_{algo_name}{rel_path.suffix}"
                out_path = out_subdir / out_name

                save_image(str(out_path), enhanced)
                print(f"  [save] -> {out_path}")

            processed += 1

    print(f"\n[done] Processed: {processed} image(s), Skipped: {skipped} file(s).")


if __name__ == "__main__":
    main()
