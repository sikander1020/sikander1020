#!/usr/bin/env python3
"""Render contribution heatmap as an animated SVG."""
import json
from datetime import datetime, timedelta
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL_SIZE = 14
CELL_GAP = 3
CORNER_RADIUS = 3
MARGIN_X = 40
MARGIN_Y = 30
LEGEND_HEIGHT = 30
STATS_HEIGHT = 25

def render():
    data = json.loads(Path("data/contributions.json").read_text())
    days = {d["date"]: d for d in data["days"]}
    stats = data["stats"]

    today = datetime.utcnow().date()
    start = today - timedelta(days=today.weekday()) - timedelta(weeks=52)
    weeks = []
    for w in range(53):
        week = []
        for d in range(7):
            date = start + timedelta(weeks=w, days=d)
            key = date.isoformat()
            entry = days.get(key, {"level": 0, "count": 0})
            week.append(entry)
        weeks.append(week)

    cols = len(weeks)
    rows = 7
    width = MARGIN_X + cols * (CELL_SIZE + CELL_GAP) + MARGIN_X
    height = MARGIN_Y + rows * (CELL_SIZE + CELL_GAP) + LEGEND_HEIGHT + STATS_HEIGHT + MARGIN_Y

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'width="{width}" height="{height}">']
    svg.append('<style>')
    svg.append('@keyframes reveal { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }')
    svg.append('</style>')
    svg.append(f'<rect width="{width}" height="{height}" rx="8" fill="#0d1117"/>')

    day_labels = ["", "Mon", "", "Wed", "", "Fri", ""]
    for i, label in enumerate(day_labels):
        if label:
            y = MARGIN_Y + i * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
            svg.append(f'<text x="4" y="{y}" font-family="monospace" font-size="10px" fill="#8b949e">{label}</text>')

    for col, week in enumerate(weeks):
        for row, entry in enumerate(week):
            x = MARGIN_X + col * (CELL_SIZE + CELL_GAP)
            y = MARGIN_Y + row * (CELL_SIZE + CELL_GAP)
            color = PALETTE[min(entry["level"], len(PALETTE) - 1)]
            delay = (col + row) * 8
            svg.append(f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                       f'rx="{CORNER_RADIUS}" fill="{color}" opacity="0" '
                       f'style="animation: reveal 0.3s ease-out {delay}ms forwards"/>')

    legend_y = MARGIN_Y + rows * (CELL_SIZE + CELL_GAP) + 10
    svg.append(f'<text x="{MARGIN_X}" y="{legend_y + 10}" font-family="monospace" '
               f'font-size="10px" fill="#8b949e">Less</text>')
    for i, color in enumerate(PALETTE):
        lx = MARGIN_X + 35 + i * (CELL_SIZE + CELL_GAP)
        svg.append(f'<rect x="{lx}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                   f'rx="{CORNER_RADIUS}" fill="{color}"/>')
    more_x = MARGIN_X + 35 + len(PALETTE) * (CELL_SIZE + CELL_GAP) + 5
    svg.append(f'<text x="{more_x}" y="{legend_y + 10}" font-family="monospace" '
               f'font-size="10px" fill="#8b949e">More</text>')

    stats_y = legend_y + LEGEND_HEIGHT + 5
    best_day_str = stats['best_day']['date'] if stats['best_day'] else 'N/A'
    stats_text = f"{stats['total']:,} contributions in the last year · {stats['current_streak']} day streak · Best: {best_day_str}"
    svg.append(f'<text x="{MARGIN_X}" y="{stats_y + 10}" font-family="monospace" '
               f'font-size="11px" fill="#c9d1d9">{stats_text}</text>')

    svg.append("</svg>")
    Path("contrib-heatmap.svg").write_text("\n".join(svg))
    print("Wrote contrib-heatmap.svg")

if __name__ == "__main__":
    render()