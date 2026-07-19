#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG."""
import os
from pathlib import Path

USERNAME = "sikander1020"
ROLE = "Software Engineer"
STACK = "Python · JavaScript · React · Node.js · AI/ML"
HIGHLIGHTS = "AI Agent Developer · API Integration · Vibe Coding · Cybersecurity Tools"
NOW = "Building an AI Cybersecurity Assistant"
PREV = "Multiple AI/ML & Full-Stack Projects"

LINE_HEIGHT = 28
PADDING_X = 24
PADDING_Y = 32
WIDTH = 490
COLORS = {
    "label": "#8b949e",
    "value": "#c9d1d9",
    "accent": "#58a6ff",
    "bg": "#0d1117",
}

def make_card():
    entries = [
        ("Now", NOW),
        ("Prev", PREV),
        ("Role", ROLE),
        ("Stack", STACK),
        ("Highlights", HIGHLIGHTS),
    ]
    height = PADDING_Y * 2 + len(entries) * LINE_HEIGHT + 40
    static = os.environ.get("STATIC") == "1"

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
           f'width="{WIDTH}" height="{height}">']
    svg.append(f'<rect width="{WIDTH}" height="{height}" rx="8" fill="{COLORS["bg"]}"/>')
    svg.append(f'<text x="{PADDING_X}" y="{PADDING_Y + 16}" font-family="monospace" '
               f'font-size="16px" fill="{COLORS["accent"]}" font-weight="bold">'
               f'{USERNAME}@github</text>')
    svg.append(f'<line x1="{PADDING_X}" y1="{PADDING_Y + 26}" '
               f'x2="{WIDTH - PADDING_X}" y2="{PADDING_Y + 26}" stroke="{COLORS["label"]}" opacity="0.3"/>')

    for i, (label, value) in enumerate(entries):
        y = PADDING_Y + 50 + i * LINE_HEIGHT
        delay = i * 200 if not static else 0
        opacity = "0" if not static else "1"
        svg.append(f'<g opacity="{opacity}">'
                   f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" '
                   f'begin="{delay}ms" fill="freeze"/>'
                   f'<text x="{PADDING_X}" y="{y}" font-family="monospace" font-size="14px">'
                   f'<tspan fill="{COLORS["label"]}">{label:>10}: </tspan>'
                   f'<tspan fill="{COLORS["value"]}">{value}</tspan>'
                   f'</text></g>')

    svg.append("</svg>")
    return "\n".join(svg)

if __name__ == "__main__":
    Path("info-card.svg").write_text(make_card())
    print("Wrote info-card.svg")