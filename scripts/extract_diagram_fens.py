#!/usr/bin/env python3
"""Draft FEN extraction from the legacy diagram PNGs.

This is intentionally conservative. It learns square templates from verified
FENs in src/diagrams/diagrams.csv and writes draft boards with '?' for any
unrecognized square.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "src" / "diagrams" / "diagrams.csv"
DIAGRAMS = ROOT / "src" / "assets" / "diagrams"
OUT = ROOT / "src" / "diagrams"


def image_number(path: Path) -> int:
    return int(re.search(r"\d+", path.name).group())


def expand_fen_board(fen: str) -> list[list[str]]:
    rows = []
    for rank in fen.split("/"):
        row: list[str] = []
        for char in rank:
            if char.isdigit():
                row.extend(["."] * int(char))
            else:
                row.append(char)
        if len(row) != 8:
            raise ValueError(f"invalid FEN rank: {rank}")
        rows.append(row)
    if len(rows) != 8:
        raise ValueError(f"invalid FEN board: {fen}")
    return rows


def compress_fen_board(rows: list[list[str]]) -> str:
    out = []
    for row in rows:
        rank = []
        empty = 0
        for char in row:
            if char == ".":
                empty += 1
            else:
                if empty:
                    rank.append(str(empty))
                    empty = 0
                rank.append(char)
        if empty:
            rank.append(str(empty))
        out.append("".join(rank))
    return "/".join(out)


def square_hash(path: Path, rank: int, file: int) -> str:
    image = Image.open(path).convert("1")
    cell = image.size[0] // 8
    crop = image.crop(
        (file * cell, rank * cell, (file + 1) * cell, (rank + 1) * cell)
    ).resize((32, 32), Image.Resampling.NEAREST)
    return hashlib.sha1(crop.tobytes()).hexdigest()


def load_verified() -> dict[int, str]:
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        return {
            int(row["id"]): row["fen"]
            for row in csv.DictReader(handle)
            if row["fen"] and row["status"] == "verified-from-moves"
        }


def learn_templates(verified: dict[int, str]) -> dict[str, str]:
    labels: defaultdict[str, set[str]] = defaultdict(set)
    for diagram_id, fen in verified.items():
        board = expand_fen_board(fen)
        path = DIAGRAMS / f"image{diagram_id}.png"
        for rank in range(8):
            for file in range(8):
                labels[square_hash(path, rank, file)].add(board[rank][file])

    conflicts = {key: value for key, value in labels.items() if len(value) > 1}
    if conflicts:
        details = ", ".join(f"{key[:8]}={sorted(value)}" for key, value in conflicts.items())
        raise SystemExit(f"template conflicts: {details}")

    return {key: next(iter(value)) for key, value in labels.items()}


def draft_board(path: Path, templates: dict[str, str]) -> tuple[str, list[str]]:
    rows: list[list[str]] = []
    unknown = []
    for rank in range(8):
        row = []
        for file in range(8):
            label = templates.get(square_hash(path, rank, file), "?")
            row.append(label)
            if label == "?":
                unknown.append(f"{chr(ord('a') + file)}{8 - rank}")
        rows.append(row)
    return compress_fen_board(rows), unknown


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    verified = load_verified()
    templates = learn_templates(verified)

    draft_path = OUT / "draft-fens.tsv"
    with draft_path.open("w", encoding="utf-8") as handle:
        handle.write("id\timage\tdraft_board\tunknown_squares\n")
        for path in sorted(DIAGRAMS.glob("image*.png"), key=image_number):
            diagram_id = image_number(path)
            board, unknown = draft_board(path, templates)
            handle.write(
                f"{diagram_id}\t{path.relative_to(ROOT)}\t{board}\t{','.join(unknown)}\n"
            )

    print(f"wrote {draft_path.relative_to(ROOT)}")
    print(f"learned {len(templates)} templates from {len(verified)} verified diagrams")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
