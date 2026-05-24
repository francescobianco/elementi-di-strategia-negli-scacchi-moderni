#!/usr/bin/env python3
"""Normalize legacy diagram PNG inclusions to centered placeholder macros."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_DIRS = [ROOT / "src" / "chapters", ROOT / "src" / "appendices"]
IMAGE_RE = re.compile(
    r"\\includegraphics(?:\[[^\]]*\])?\{assets/diagrams/image(?P<num>\d+)\.png\}"
)


def caption_re(num: str) -> re.Pattern[str]:
    return re.compile(r"\\emph\{diagramma\s+" + re.escape(num) + r"(?:\s*[-–—]+[^}]*)?\}", re.S)


def normalize_text(text: str) -> tuple[str, int]:
    replacements = 0
    image_numbers = sorted({m.group("num") for m in IMAGE_RE.finditer(text)}, key=int)

    for num in image_numbers:
        image_pattern = re.compile(
            r"\\includegraphics(?:\[[^\]]*\])?\{assets/diagrams/image" + re.escape(num) + r"\.png\}"
        )
        macro = rf"\bookdiagramplaceholder{{assets/diagrams/image{num}.png}}{{{num}}}"
        text, image_count = image_pattern.subn(lambda _: macro, text)
        replacements += image_count
        text = caption_re(num).sub("", text)

    # ensure diagram macros are block separated from following prose/moves
    text = re.sub(
        r"(\\bookdiagramplaceholder(?:\[[^\]]+\])?\{[^}]+\}\{\d+\})(?=\S)",
        r"\1\n\n",
        text,
    )
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, replacements


def main() -> int:
    changed = 0
    replacements = 0
    for directory in TEX_DIRS:
        for path in sorted(directory.glob("*.tex")):
            original = path.read_text(encoding="utf-8")
            normalized, count = normalize_text(original)
            if normalized != original:
                path.write_text(normalized, encoding="utf-8")
                changed += 1
                replacements += count
                print(f"normalized {path.relative_to(ROOT)} ({count} diagrams)")
    print(f"changed {changed} files, normalized {replacements} diagram images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
