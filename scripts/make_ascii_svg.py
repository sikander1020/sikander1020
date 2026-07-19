#!/usr/bin/env python3
"""Convert a prepped grayscale image to an animated ASCII-art SVG."""
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
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="monospace" font-size="{CHAR_H}px">',
        f'<style>text {{ fill: {FILL_COLOR}; }}</style>',
    ]
    for i, line in enumerate(lines):
        delay = i * ROW_DELAY_MS
        clip_id = f"clip-row-{i}"
        y = (i + 1) * CHAR_H
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(f"""
  <defs><clipPath id="{clip_id}">
    <rect x="0" y="0" width="0" height="{height}">
      <animate attributeName="width" from="0" to="{width}" dur="0.8s"
               begin="{delay}ms" fill="freeze"/>
    </rect>
  </clipPath></defs>
  <text clip-path="url(#{clip_id})" x="0" y="{y}">{escaped}</text>""")
    svg_parts.append("</svg>")
    return "\n".join(svg_parts)

def main():
    lines = image_to_ascii("data/source-prepped.png")
    svg = build_svg(lines)
    Path("avi-ascii.svg").write_text(svg)
    print("Wrote avi-ascii.svg")

if __name__ == "__main__":
    main()