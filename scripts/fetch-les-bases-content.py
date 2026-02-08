#!/usr/bin/env python3
"""
Récupère depuis Strapi tous les chapitres et leçons de la section "Les bases"
avec titres, descriptions et résumé du contenu (premiers paragraphes des text-blocks).
Sortie : output/les-bases-existing-content.json pour analyse et éviter les doublons.
"""
import os
import json
import requests
from pathlib import Path

STRAPI_URL = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
STRAPI_TOKEN = os.getenv("STRAPI_API_TOKEN")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "les-bases-existing-content.json"


def plain_from_richtext(blocks):
    """Extrait le texte brut des blocs Rich Text (récursif sur children)."""
    if not blocks:
        return ""
    lines = []
    for b in blocks:
        if isinstance(b, dict):
            if b.get("type") == "paragraph" or b.get("type", "").startswith("heading"):
                for c in b.get("children") or []:
                    if c.get("type") == "text" and c.get("text"):
                        lines.append(c["text"].strip())
            # nested
            for c in b.get("children") or []:
                if isinstance(c, dict) and c.get("type") == "text" and c.get("text"):
                    lines.append(c["text"].strip())
    return " ".join(lines)[:500]  # premier extrait


def main():
    if not STRAPI_TOKEN:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1
    headers = {"Authorization": f"Bearer {STRAPI_TOKEN}", "Content-Type": "application/json"}

    # Sections
    r = requests.get(f"{STRAPI_URL}/api/sections", headers=headers, params={"pagination[pageSize]": 100}, timeout=30)
    r.raise_for_status()
    sections = r.json().get("data", [])
    section = next((s for s in sections if (s.get("title") or "").strip() == "Les bases"), None)
    if not section:
        print("❌ Section 'Les bases' introuvable.")
        return 1
    section_id = section["id"]

    # Chapitres
    r2 = requests.get(
        f"{STRAPI_URL}/api/chapters",
        headers=headers,
        params={"filters[section][id][$eq]": section_id, "pagination[pageSize]": 50, "sort": "order:asc"},
        timeout=30,
    )
    r2.raise_for_status()
    chapters_data = r2.json().get("data", [])

    result = {
        "section": "Les bases",
        "section_id": section_id,
        "chapters": [],
    }

    for ch in chapters_data:
        ch_id = ch.get("id")
        ch_title = ch.get("title") or (ch.get("attributes") or {}).get("title") or ""
        ch_order = ch.get("order") or (ch.get("attributes") or {}).get("order")
        ch_desc = ch.get("description") or (ch.get("attributes") or {}).get("description")
        if isinstance(ch_desc, list):
            ch_desc_plain = plain_from_richtext(ch_desc)
        else:
            ch_desc_plain = str(ch_desc or "")[:300]

        # Liste des leçons du chapitre
        r3 = requests.get(
            f"{STRAPI_URL}/api/lessons",
            headers=headers,
            params={"filters[chapter][id][$eq]": ch_id, "pagination[pageSize]": 100, "sort": "order:asc"},
            timeout=30,
        )
        r3.raise_for_status()
        lessons_list = r3.json().get("data", [])

        lessons_out = []
        for lec in lessons_list:
            doc_id = lec.get("documentId")
            title_lec = lec.get("title") or ""
            order_lec = lec.get("order")
            # Récupérer le contenu complet pour extraire les sujets
            if not doc_id:
                lessons_out.append({"title": title_lec, "order": order_lec, "content_summary": []})
                continue
            req = requests.get(
                f"{STRAPI_URL}/api/lessons/{doc_id}",
                headers=headers,
                params={"populate": "*"},
                timeout=30,
            )
            if req.status_code != 200:
                lessons_out.append({"title": title_lec, "order": order_lec, "content_summary": [], "error": req.status_code})
                continue
            full = req.json().get("data", {})
            content = full.get("content") or []
            content_summary = []
            for block in content:
                if block.get("__component") == "lesson-content.text-block":
                    title_block = block.get("title") or ""
                    rt = block.get("content") or []
                    extract = plain_from_richtext(rt)
                    content_summary.append({"title": title_block, "extract": extract})
                elif block.get("__component") == "lesson-content.quizz-block":
                    q = block.get("Question") or ""
                    if q:
                        content_summary.append({"type": "quiz", "question": q[:200]})

            lessons_out.append({
                "title": title_lec,
                "order": order_lec,
                "content_summary": content_summary,
            })

        result["chapters"].append({
            "id": ch_id,
            "title": ch_title,
            "order": ch_order,
            "description": ch_desc_plain,
            "lessons": lessons_out,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ Sauvegardé : {OUT}")
    print(f"   {len(result['chapters'])} chapitres, {sum(len(c['lessons']) for c in result['chapters'])} leçons.")
    return 0


if __name__ == "__main__":
    exit(main())
