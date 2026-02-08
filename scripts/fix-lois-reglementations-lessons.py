#!/usr/bin/env python3
"""
Section "Lois et réglementations" :
- Vérifie que chaque text-block a un titre "Page 1", "Page 2", ... et que le titre
  d'origine est bien en tête du contenu (sinon on renomme en Page N et on préfixe le contenu).
- Vérifie que chaque quiz de type "matching" a ses options en un seul bloc texte (A/1/B/2/...).
  Si options = plusieurs paragraphes, on les fusionne en un seul bloc (texte avec retours à la ligne).
Puis PUT chaque leçon (sans id dans les blocs).
"""
import os
import re
import requests
from pathlib import Path

STRAPI_URL = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
STRAPI_TOKEN = os.getenv("STRAPI_API_TOKEN")


def rt_paragraph(text: str):
    return {"type": "paragraph", "children": [{"text": text, "type": "text"}]}


def rich_text_to_plain(block) -> str:
    """Extrait le texte brut d'un bloc Rich Text (paragraph avec children)."""
    if not block:
        return ""
    if isinstance(block, str):
        return block
    children = block.get("children") or []
    return "".join(c.get("text", "") for c in children if c.get("type") == "text")


def text_block_needs_fix(block, page_index: int):
    """
    Retourne (need_fix, new_title).
    Fix si le titre n'est pas "Page N" : on veut "Page 1", "Page 2", ...
    """
    title = (block.get("title") or "").strip()
    expected = f"Page {page_index}"
    if title == expected:
        return False, None
    return True, expected


def merge_matching_options(options: list) -> list:
    """Fusionne plusieurs paragraphes d'options en un seul bloc (une seule string avec \\n)."""
    if not options or len(options) <= 1:
        return options
    lines = []
    for opt in options:
        text = rich_text_to_plain(opt).strip()
        if text:
            lines.append(text)
    if not lines:
        return options
    return [rt_paragraph("\n".join(lines))]


def strip_id(block: dict) -> dict:
    return {k: v for k, v in block.items() if k != "id"}


def main():
    if not STRAPI_TOKEN:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1
    headers = {"Authorization": f"Bearer {STRAPI_TOKEN}", "Content-Type": "application/json"}

    # Section Lois et réglementations
    r = requests.get(f"{STRAPI_URL}/api/sections", headers=headers, params={"pagination[pageSize]": 100}, timeout=30)
    r.raise_for_status()
    sections = r.json().get("data", [])
    section = next((s for s in sections if (s.get("title") or "").strip() == "Lois et réglementations"), None)
    if not section:
        print("❌ Section 'Lois et réglementations' introuvable.")
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
    chapters = r2.json().get("data", [])

    # Toutes les leçons (documentId)
    lessons_to_fetch = []
    for ch in chapters:
        r3 = requests.get(
            f"{STRAPI_URL}/api/lessons",
            headers=headers,
            params={"filters[chapter][id][$eq]": ch["id"], "pagination[pageSize]": 100, "sort": "order:asc"},
            timeout=30,
        )
        r3.raise_for_status()
        for lec in r3.json().get("data", []):
            lessons_to_fetch.append(lec.get("documentId"))

    fixed_count = 0
    for doc_id in lessons_to_fetch:
        if not doc_id:
            continue
        req = requests.get(f"{STRAPI_URL}/api/lessons/{doc_id}", headers=headers, params={"populate": "*"}, timeout=30)
        if req.status_code != 200:
            print(f"  Skip {doc_id}: GET {req.status_code}")
            continue
        d = req.json().get("data", {})
        title_lesson = d.get("title")
        content = list(d.get("content") or [])
        new_content = []
        text_index = 0
        changed = False

        for b in content:
            comp = b.get("__component")
            if comp == "lesson-content.text-block":
                text_index += 1
                need_fix, new_title = text_block_needs_fix(b, text_index)
                if need_fix and new_title:
                    # Renommer en Page N et préfixer le contenu avec l'ancien titre si pas déjà en tête
                    old_title = (b.get("title") or "").strip()
                    blocks_content = list(b.get("content") or [])
                    first_text = rich_text_to_plain(blocks_content[0]).strip() if blocks_content else ""
                    if old_title and old_title != new_title and first_text != old_title:
                        blocks_content.insert(0, rt_paragraph(old_title))
                    new_content.append(strip_id({
                        **b,
                        "title": new_title,
                        "content": blocks_content,
                    }))
                    changed = True
                else:
                    new_content.append(strip_id(b))
                continue

            if comp == "lesson-content.quizz-block":
                qtype = (b.get("questionType") or "").strip().lower()
                opts = b.get("options")
                if qtype == "matching" and isinstance(opts, list) and len(opts) > 1:
                    merged = merge_matching_options(opts)
                    new_content.append(strip_id({**b, "options": merged}))
                    changed = True
                else:
                    new_content.append(strip_id(b))
                continue

            new_content.append(strip_id(b))

        if changed:
            fixed_count += 1
            print(f"  Fix: {title_lesson} ({doc_id[:12]}...) → PUT...")
            resp = requests.put(
                f"{STRAPI_URL}/api/lessons/{doc_id}",
                json={"data": {"content": new_content}},
                headers=headers,
                timeout=30,
            )
            if resp.status_code != 200:
                print(f"     ❌ {resp.status_code}: {resp.text[:250]}")
            else:
                print(f"     ✅ Mis à jour.")
        else:
            print(f"  OK:  {title_lesson}")

    print(f"\nTotal: {fixed_count} leçon(s) corrigée(s) sur {len(lessons_to_fetch)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
