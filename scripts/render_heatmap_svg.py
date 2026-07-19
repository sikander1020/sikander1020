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


def render() -> None:
    source = Path("data/contributions.json")
    if not source.exists():
        raise SystemExit("Missing data/contributions.json. Run scripts/fetch_contributions.py first.")

    data = json.loads(source.read_text(encoding="utf-8"))
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

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Contribution heatmap">',
        '<rect width="100%" height="100%" fill="#0d1117" rx="10" />',
        '<g font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="11" fill="#8b949e">',
        f'<text x="{MARGIN_X}" y="{MARGIN_Y - 10}">Last 53 weeks</text>',
        "</g>",
    ]

    label_x = MARGIN_X - 26
    for idx, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = MARGIN_Y + idx * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
        svg.append(
            f'<text x="{label_x}" y="{y}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="10" fill="#8b949e">{label}</text>'
        )

    for w, week in enumerate(weeks):
        for d, entry in enumerate(week):
            level = int(entry.get("level", 0))
            level = min(max(level, 0), len(PALETTE) - 1)
            x = MARGIN_X + w * (CELL_SIZE + CELL_GAP)
            y = MARGIN_Y + d * (CELL_SIZE + CELL_GAP)
            count = int(entry.get("count", 0))
            begin = (w * 7 + d) * 0.004
            svg.append(
                f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{CORNER_RADIUS}" fill="{PALETTE[level]}" opacity="0">'
                f'<title>{count} contributions</title>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.3f}s" dur="0.15s" fill="freeze" />'
                "</rect>"
            )

    legend_y = MARGIN_Y + rows * (CELL_SIZE + CELL_GAP) + 18
    legend_x = MARGIN_X
    svg.append(
        f'<text x="{legend_x}" y="{legend_y}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="10" fill="#8b949e">Less</text>'
    )
    lx = legend_x + 28
    for color in PALETTE:
        svg.append(
            f'<rect x="{lx}" y="{legend_y - 10}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{CORNER_RADIUS}" fill="{color}" />'
        )
        lx += CELL_SIZE + 4
    svg.append(
        f'<text x="{lx + 4}" y="{legend_y}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="10" fill="#8b949e">More</text>'
    )

    stats_y = legend_y + 20
    best_day = stats.get("best_day") or {"date": "n/a", "count": 0}
    stats_text = (
        f'Total: {stats.get("total", 0)} · Current streak: {stats.get("current_streak", 0)} · '
        f'Longest streak: {stats.get("longest_streak", 0)} · Best day: {best_day.get("date", "n/a")} ({best_day.get("count", 0)})'
    )
    svg.append(
        f'<text x="{MARGIN_X}" y="{stats_y}" font-family="Consolas, Menlo, Monaco, \'Courier New\', monospace" font-size="10" fill="#c9d1d9">{stats_text}</text>'
    )

    svg.append("</svg>")
    Path("contrib-heatmap.svg").write_text("\n".join(svg), encoding="utf-8")
    print("Wrote contrib-heatmap.svg")


if __name__ == "__main__":
    render()
