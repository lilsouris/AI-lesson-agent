#!/usr/bin/env python3
"""
Recâble les chapitres prérequis pour les nouveaux chapitres créés dans Strapi.

Contexte :
- Les chapitres ont bien été créés, mais les appels PUT automatiques
  pour `prerequisiteChapters` renvoient 404 quand on utilise /api/chapters/{id}.
- Strapi V5 s'attend à ce que les mises à jour passent par /api/chapters/{documentId}.

Ce script :
- Retrouve, pour chaque section ciblée, les chapitres par `order`
- Met à jour les prérequis du "chapitre enfant" vers le "chapitre parent"
  via /api/chapters/{documentId} et `prerequisiteChapters.connect` (par id numérique).

Sections et mappings gérés :
- Investissement Alternatifs : order 2 (parent) -> order 3 (enfant)
- Immobilier :               order 2 (parent) -> order 3 (enfant)
- Bourse :                   order 3 (parent) -> order 4 (enfant)
- Lois et réglementations :  order 3 (parent) -> order 4 (enfant)
- Les bases :                order 11 (parent) -> order 12 (enfant)

Usage (depuis la racine du repo) :

  export STRAPI_URL="https://cms.finsly.org"
  export STRAPI_API_TOKEN="..."
  python scripts/fix-chapters-prerequisites.py --dry-run   # pour voir ce qui serait fait
  python scripts/fix-chapters-prerequisites.py             # pour appliquer réellement
"""

import os
import json
import argparse
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

import requests


@dataclass
class PrereqMapping:
    section_title: str
    parent_order: int
    child_order: int


MAPPINGS: List[PrereqMapping] = [
    PrereqMapping("Investissement Alternatifs", parent_order=2, child_order=3),
    PrereqMapping("Immobilier", parent_order=2, child_order=3),
    PrereqMapping("Bourse", parent_order=3, child_order=4),
    PrereqMapping("Lois et réglementations", parent_order=3, child_order=4),
    PrereqMapping("Les bases", parent_order=11, child_order=12),
]


def get_section_by_title(base_url: str, headers: Dict[str, str], title: str) -> Optional[Dict[str, Any]]:
    """Retourne la section Strapi (id + attributes) correspondant au titre."""
    resp = requests.get(
        f"{base_url}/api/sections",
        headers=headers,
        params={"filters[title][$eq]": title, "pagination[pageSize]": 100},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json().get("data") or []
    return data[0] if data else None


def get_chapters_for_section(base_url: str, headers: Dict[str, str], section_id: int) -> List[Dict[str, Any]]:
    """Retourne tous les chapitres d'une section (id, documentId, attributes...)."""
    chapters: List[Dict[str, Any]] = []
    page = 1
    while True:
        resp = requests.get(
            f"{base_url}/api/chapters",
            headers=headers,
            params={
                "filters[section][id][$eq]": section_id,
                "pagination[page]": page,
                "pagination[pageSize]": 100,
                "sort[0]": "order:asc",
            },
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        data = body.get("data") or []
        if not data:
            break
        chapters.extend(data)
        meta = (body.get("meta") or {}).get("pagination") or {}
        total = meta.get("total") or 0
        page_size = meta.get("pageSize") or 100
        if page * page_size >= total:
            break
        page += 1
    return chapters


def chapter_order(chapter: Dict[str, Any]) -> int:
    """Extrait le champ order, que Strapi renvoie parfois dans attributes."""
    attrs = chapter.get("attributes") or chapter
    return int(attrs.get("order") or 0)


def chapter_title(chapter: Dict[str, Any]) -> str:
    attrs = chapter.get("attributes") or chapter
    return (attrs.get("title") or "").strip()


def chapter_document_id(chapter: Dict[str, Any]) -> Optional[str]:
    attrs = chapter.get("attributes") or chapter
    return attrs.get("documentId") or chapter.get("documentId")


def chapter_numeric_id(chapter: Dict[str, Any]) -> Optional[int]:
    attrs = chapter.get("attributes") or chapter
    return attrs.get("id") or chapter.get("id")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix Strapi chapters prerequisiteChapters for new chapters.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="N'envoie pas les requêtes PUT, affiche seulement ce qui serait modifié.",
    )
    args = parser.parse_args()

    strapi_url = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
    token = os.getenv("STRAPI_API_TOKEN")
    if not token:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    base = strapi_url
    errors: List[str] = []

    for mapping in MAPPINGS:
        print(f"\n🔍 Section « {mapping.section_title} » : lier order {mapping.child_order} → prérequis order {mapping.parent_order}")
        section = get_section_by_title(base, headers, mapping.section_title)
        if not section:
            msg = f"Section '{mapping.section_title}' non trouvée."
            print(f"  ⚠️ {msg}")
            errors.append(msg)
            continue

        section_id = section.get("id")
        print(f"  ✅ Section trouvée : ID {section_id}")

        chapters = get_chapters_for_section(base, headers, section_id)
        if not chapters:
            msg = f"Aucun chapitre trouvé pour la section ID {section_id}."
            print(f"  ⚠️ {msg}")
            errors.append(msg)
            continue

        by_order = {chapter_order(c): c for c in chapters}
        parent = by_order.get(mapping.parent_order)
        child = by_order.get(mapping.child_order)

        if not parent or not child:
            msg = (
                f"Chapitres manquants pour la section '{mapping.section_title}': "
                f"parent order {mapping.parent_order} trouvé={bool(parent)}, "
                f"enfant order {mapping.child_order} trouvé={bool(child)}"
            )
            print(f"  ⚠️ {msg}")
            errors.append(msg)
            continue

        parent_id = chapter_numeric_id(parent)
        child_doc_id = chapter_document_id(child)
        print(
            f"  ➜ Parent: order={mapping.parent_order}, id={parent_id}, title={chapter_title(parent)!r}\n"
            f"  ➜ Enfant: order={mapping.child_order}, docId={child_doc_id}, title={chapter_title(child)!r}"
        )

        if not parent_id or not child_doc_id:
            msg = f"IDs manquants pour la section '{mapping.section_title}' (parent_id={parent_id}, child_doc_id={child_doc_id})."
            print(f"  ⚠️ {msg}")
            errors.append(msg)
            continue

        payload = {
            "data": {
                "prerequisiteChapters": {
                    "connect": [parent_id]
                }
            }
        }

        if args.dry_run:
            print(f"  [DRY-RUN] PUT /api/chapters/{child_doc_id} avec :")
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            continue

        try:
            resp = requests.put(f"{base}/api/chapters/{child_doc_id}", headers=headers, json=payload, timeout=30)
            if resp.status_code != 200:
                msg = f"PUT /chapters/{child_doc_id} -> {resp.status_code}: {resp.text[:300]}"
                print(f"  ❌ {msg}")
                errors.append(msg)
            else:
                print(f"  ✅ prerequisiteChapters mis à jour pour le chapitre docId={child_doc_id} (connect -> {parent_id})")
        except Exception as e:
            msg = f"Erreur lors du PUT sur /chapters/{child_doc_id}: {e}"
            print(f"  ❌ {msg}")
            errors.append(msg)

    if errors:
        print("\n⚠️ Terminé avec des erreurs :")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\n✅ Toutes les relations prerequisiteChapters ciblées ont été mises à jour (ou simulées en dry-run).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

