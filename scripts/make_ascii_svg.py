#!/usr/bin/env python3
"""Convert a prepped grayscale image to an animated ASCII-art SVG."""

from html import escape
from pathlib import Path

from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 100
ROWS = 53
FILL_COLOR = "#c9d1d9"
CHAR_W = 7
CHAR_H = 14
ROW_DELAY_MS = 60


def image_to_ascii(img_path: str) -> list[str]:
    img = Image.open(img_path).convert("L").resize((COLS, ROWS), Image.LANCZOS)
    pixels = img.load()
    lines = []

    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            brightness = pixels[x, y]
            idx = int(brightness / 256 * len(RAMP))
            idx = min(idx, len(RAMP) - 1)
            row += RAMP[idx]
        lines.append(row)

    return lines


def build_svg(lines: list[str]) -> str:
    width = COLS * CHAR_W
    height = ROWS * CHAR_H
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII art">',
        '<rect width="100%" height="100%" fill="#0d1117" />',
        f'<g font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="{CHAR_H}" fill="{FILL_COLOR}" xml:space="preserve">',
    ]

    for y, line in enumerate(lines):
        begin_s = (y * ROW_DELAY_MS) / 1000
        y_pos = (y + 1) * CHAR_H
        safe_line = escape(line)
        svg_parts.append(f'<text x="0" y="{y_pos}" opacity="0">{safe_line}')
        svg_parts.append(
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin_s:.2f}s" dur="0.25s" fill="freeze" />'
        )
        svg_parts.append("</text>")

    svg_parts.append("</g>")
    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def main() -> None:
    lines = image_to_ascii("data/source-prepped.png")
    svg = build_svg(lines)
    Path("avi-ascii.svg").write_text(svg, encoding="utf-8")
    print("Wrote avi-ascii.svg")


if __name__ == "__main__":
    main()
