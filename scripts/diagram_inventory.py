#!/usr/bin/env python3
"""List source diagram images with size and color count."""

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "src" / "assets" / "diagrams"


def image_number(path: Path) -> int:
    return int(re.search(r"\d+", path.name).group())


def main() -> int:
    for path in sorted(DIAGRAMS.glob("image*.png"), key=image_number):
        result = subprocess.run(
            ["identify", "-format", "%f,%w,%h,%[colors]", str(path)],
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
