#!/usr/bin/env python3
"""Fetch GitHub contribution data from the public HTML endpoint (no token needed)."""
import json
import re
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "sikander1020"

def fetch():
    url = f"https://github.com/users/{USERNAME}/contributions"
    resp = requests.get(url, headers={"User-Agent": "profile-readme-bot"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    for rect in soup.select("rect[data-date]"):
        date = rect["data-date"]
        level = int(rect.get("data-level", 0))
        count_text = rect.get("title", "")
        match = re.search(r"(\d+) contributions?", count_text)
        count = int(match.group(1)) if match else 0
        days.append({"date": date, "level": level, "count": count})

    total = sum(d["count"] for d in days)
    best_day = max(days, key=lambda d: d["count"]) if days else None

    current_streak = 0
    longest_streak = 0
    streak = 0
    for d in sorted(days, key=lambda x: x["date"]):
        if d["count"] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0
    current_streak = streak

    data = {
        "username": USERNAME,
        "days": days,
        "stats": {
            "total": total,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day,
        },
        "fetched_at": datetime.utcnow().isoformat(),
    }
    Path("data/contributions.json").write_text(json.dumps(data, indent=2))
    print(f"Fetched {len(days)} days, {total} total contributions")

if __name__ == "__main__":
    fetch()