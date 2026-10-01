#!/usr/bin/env python3
"""Convert a prepped grayscale image to an animated ASCII-art SVG with terminal styling."""
from pathlib import Path
from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 100
ROWS = 53
FILL_COLOR = "#c9d1d9"
CHAR_W = 7
CHAR_H = 14
ROW_DELAY_MS = 80

USERNAME = "sikander1020"

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
    padding_x = 20
    padding_y = 37
    title_height = 30
    footer_height = 40
    row_step = 15
    text_width = COLS * CHAR_W
    width = padding_x + text_width + padding_x
    height = padding_y + ROWS * row_step + footer_height

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>',
        f'<line x1="0" y1="{title_height}" x2="{width}" y2="{title_height}" stroke="#30363d"/>',
        f'<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/><circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/><circle cx="52" cy="15.0" r="5" fill="#27c93f"/>',
        f'<text x="{width/2}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">{USERNAME}@github: ~$ ./portrait.sh</text>',
        f'<style>',
        f'@keyframes revealRow {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}',
        f'@keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}',
        f'</style>',
    ]

    for i, line in enumerate(lines):
        delay = i * ROW_DELAY_MS
        y = padding_y + i * row_step
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(f'<text xml:space="preserve" x="{padding_x}" y="{y + 11}" fill="{FILL_COLOR}" font-size="12.9" opacity="0" style="animation: revealRow 0.2s ease-out {delay}ms forwards;">{escaped}</text>')

    cursor_x = padding_x + text_width + 2
    svg_parts.append(f'<rect x="{cursor_x}" y="{padding_y}" width="8" height="{CHAR_H}" fill="{FILL_COLOR}" opacity="0" style="animation: revealRow 0s ease-out {ROWS * ROW_DELAY_MS}ms forwards, blink 1s step-end infinite;"/>')

    footer_y = height - 20
    svg_parts.append(f'<line x1="0" y1="{height - footer_height}" x2="{width}" y2="{height - footer_height}" stroke="#30363d"/>')
    svg_parts.append(f'<text x="{padding_x}" y="{footer_y}" fill="#7d8590" font-size="13">{USERNAME}@github:~$ whoami <tspan fill="{FILL_COLOR}">Sikander</tspan></text>')
    svg_parts.append(f'<rect x="{padding_x + 216}" y="{height - 36}" width="8" height="14" fill="{FILL_COLOR}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')
    svg_parts.append("</svg>")
    return "\n".join(svg_parts)

def main():
    lines = image_to_ascii("data/source-prepped.png")
    svg = build_svg(lines)
    Path("avi-ascii.svg").write_text(svg)
    print("Wrote avi-ascii.svg")

if __name__ == "__main__":
    main()