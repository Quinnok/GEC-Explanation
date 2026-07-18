from __future__ import annotations

import argparse
import math
from pathlib import Path


def split(args: argparse.Namespace) -> None:
    lines = [line for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    chunk_size = max(1, math.ceil(len(lines) / args.chunks))
    for idx in range(args.chunks):
        chunk_lines = lines[idx * chunk_size : (idx + 1) * chunk_size]
        if not chunk_lines:
            continue
        (args.out_dir / f"chunk_{idx:03d}.jsonl").write_text("\n".join(chunk_lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split a JSONL file into contiguous chunks.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--chunks", type=int, default=4)
    return parser.parse_args()


if __name__ == "__main__":
    split(parse_args())
