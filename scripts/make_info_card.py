#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG."""

import os
from html import escape
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


def make_card() -> str:
    entries = [
        ("Now", NOW),
        ("Prev", PREV),
        ("Role", ROLE),
        ("Stack", STACK),
        ("Highlights", HIGHLIGHTS),
    ]
    height = PADDING_Y * 2 + len(entries) * LINE_HEIGHT + 40
    static = os.environ.get("STATIC") == "1"

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Profile info card">',
        f'<rect width="100%" height="100%" rx="12" fill="{COLORS["bg"]}" />',
        f'<text x="{PADDING_X}" y="{PADDING_Y}" fill="{COLORS["accent"]}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="24" font-weight="700">{escape(USERNAME)}</text>',
    ]

    y = PADDING_Y + 40
    for i, (label, value) in enumerate(entries):
        line = (
            f'<text x="{PADDING_X}" y="{y}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" '
            f'font-size="18" fill="{COLORS["value"]}">'
            f'<tspan fill="{COLORS["label"]}">{escape(label)}:</tspan> {escape(value)}'
            "</text>"
        )
        if static:
            svg.append(line)
        else:
            begin = i * 0.12
            svg.append(line.replace('>', ' opacity="0">', 1))
            svg.append(
                f'<animate xlink:href="#line-{i}" attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.25s" fill="freeze" />'
            )
        y += LINE_HEIGHT

    if not static:
        # Rebuild animated text lines with IDs to support xlink:href targets.
        svg = svg[:3]
        y = PADDING_Y + 40
        for i, (label, value) in enumerate(entries):
            begin = i * 0.12
            svg.append(
                f'<text id="line-{i}" x="{PADDING_X}" y="{y}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" '
                f'font-size="18" fill="{COLORS["value"]}" opacity="0">'
                f'<tspan fill="{COLORS["label"]}">{escape(label)}:</tspan> {escape(value)}'
                '<animate attributeName="opacity" from="0" to="1" begin="'
                f'{begin:.2f}s" dur="0.25s" fill="freeze" /></text>'
            )
            y += LINE_HEIGHT

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    Path("info-card.svg").write_text(make_card(), encoding="utf-8")
    print("Wrote info-card.svg")
