#!/usr/bin/env python3
"""Fetch lesson "L'inflation, ton ennemi silencieux" from Strapi (full content) and save to output/inflation-lesson.json."""
import os
import json
import requests
from pathlib import Path

STRAPI_URL = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
STRAPI_TOKEN = os.getenv("STRAPI_API_TOKEN")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "inflation-lesson.json"


def main():
    if not STRAPI_TOKEN:
        print("Set STRAPI_API_TOKEN")
        return 1
    headers = {"Authorization": f"Bearer {STRAPI_TOKEN}", "Content-Type": "application/json"}

    # Find lesson by title
    r = requests.get(
        f"{STRAPI_URL}/api/lessons",
        headers=headers,
        params={"filters[title][$containsi]": "inflation", "pagination[pageSize]": 10},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json().get("data", [])
    if not data:
        print("No lesson with 'inflation' in title found.")
        return 1
    # Prefer exact match
    lesson = next((l for l in data if (l.get("title") or "").strip() == "L'inflation, ton ennemi silencieux"), data[0])
    doc_id = lesson.get("documentId")
    if not doc_id:
        print("No documentId on lesson")
        return 1
    # Full content
    req = requests.get(
        f"{STRAPI_URL}/api/lessons/{doc_id}",
        headers=headers,
        params={"populate": "*"},
        timeout=30,
    )
    req.raise_for_status()
    full = req.json()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(full, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUT}")
    return 0


if __name__ == "__main__":
    exit(main())
