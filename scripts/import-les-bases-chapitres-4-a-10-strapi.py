#!/usr/bin/env python3
"""
Import des chapitres 4 à 10 "Les bases" dans Strapi.

- Supprime les anciens chapitres d'ordre 4 et 5 de la section "Les bases" et toutes leurs leçons.
- Crée les nouveaux chapitres 4 à 10 avec prérequis : ch4 → ch3, ch5 → ch4, …, ch10 → ch9.
- Crée toutes les leçons liées aux nouveaux chapitres (contenu depuis les-bases-chapitres-4-a-10.json).

Usage (depuis la racine du repo) :
  python scripts/import-les-bases-chapitres-4-a-10-strapi.py
  python scripts/import-les-bases-chapitres-4-a-10-strapi.py --dry-run   # affiche les actions sans supprimer/créer

Variables d'environnement : STRAPI_URL, STRAPI_API_TOKEN.
"""
import os
import sys
import json
import re
import argparse
import requests
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional

ROOT = Path(__file__).resolve().parent.parent
INPUT_JSON = ROOT / "output" / "les-bases-chapitres-4-a-10.json"

# Charger le module agent (nom de fichier avec tirets = pas importable directement)
_agent_path = ROOT / "python-agent" / "scripts-generate-chapters-and-lessons-agent.py"
_spec = importlib.util.spec_from_file_location("chapter_lesson_agent", _agent_path)
_agent_module = importlib.util.module_from_spec(_spec)
sys.modules["chapter_lesson_agent"] = _agent_module
_spec.loader.exec_module(_agent_module)
ChapterAndLessonGeneratorAgent = _agent_module.ChapterAndLessonGeneratorAgent
normalize_loaded_content = _agent_module.normalize_loaded_content


def _chapter_order(item: Dict) -> int:
    o = item.get("order")
    if o is not None:
        return int(o)
    return int((item.get("attributes") or {}).get("order", 0))


def _chapter_title(item: Dict) -> str:
    if item.get("title"):
        return item["title"]
    return (item.get("attributes") or {}).get("title") or ""


def delete_lessons_and_chapters(
    strapi_url: str,
    strapi_token: str,
    chapter_ids: List[int],
    dry_run: bool,
) -> List[str]:
    """Supprime les leçons de chaque chapitre puis les chapitres. Retourne la liste d'erreurs."""
    errors = []
    headers = {
        "Authorization": f"Bearer {strapi_token}",
        "Content-Type": "application/json",
    }
    base = strapi_url.rstrip("/")

    for ch_id in chapter_ids:
        # Récupérer les leçons du chapitre
        try:
            r = requests.get(
                f"{base}/api/lessons",
                headers=headers,
                params={
                    "filters[chapter][id][$eq]": ch_id,
                    "pagination[pageSize]": 100,
                },
                timeout=30,
            )
            r.raise_for_status()
            lessons = r.json().get("data", []) or []
        except Exception as e:
            errors.append(f"Erreur liste leçons chapitre {ch_id}: {e}")
            continue

        for lec in lessons:
            # Strapi v5 peut utiliser documentId pour l'URL
            doc_id = lec.get("documentId") or lec.get("id")
            if not doc_id:
                continue
            if dry_run:
                print(f"  [DRY-RUN] Suppression leçon {doc_id} ({lec.get('title', '')})")
                continue
            try:
                resp = requests.delete(
                    f"{base}/api/lessons/{doc_id}",
                    headers=headers,
                    timeout=30,
                )
                resp.raise_for_status()
                print(f"  ✅ Leçon supprimée : {doc_id}")
            except Exception as e:
                errors.append(f"Erreur suppression leçon {doc_id}: {e}")

        if dry_run:
            print(f"  [DRY-RUN] Suppression chapitre {ch_id}")
        else:
            try:
                resp = requests.delete(
                    f"{base}/api/chapters/{ch_id}",
                    headers=headers,
                    timeout=30,
                )
                resp.raise_for_status()
                print(f"✅ Chapitre supprimé : {ch_id}")
            except Exception as e:
                errors.append(f"Erreur suppression chapitre {ch_id}: {e}")

    return errors


def build_content_blocks(agent: ChapterAndLessonGeneratorAgent, lesson: Dict) -> List[Dict]:
    """Construit le tableau content (text-blocks + quiz-blocks) au format Strapi."""
    content_blocks = []
    text_blocks = lesson.get("content", {}).get("textBlocks", [])

    for page_idx, tb in enumerate(text_blocks, 1):
        block_title = (tb.get("title") or "").strip()
        if block_title and re.match(r"^Page \d+$", block_title):
            page_title = block_title
            content = tb.get("content", [])
        else:
            page_title = f"Page {page_idx}"
            original_title = block_title or ""
            content = tb.get("content", [])
            if original_title:
                if isinstance(content, list):
                    title_block = {
                        "type": "paragraph",
                        "children": [{"text": original_title, "type": "text"}],
                    }
                    content = [title_block] + content
                elif isinstance(content, str):
                    content = agent.convert_markdown_to_richtext(f"{original_title}\n\n{content}")
        if isinstance(content, str):
            content = agent.convert_markdown_to_richtext(content)
        content_blocks.append({
            "__component": "lesson-content.text-block",
            "title": page_title,
            "content": content,
            "highlight": tb.get("highlight", False),
        })

    for qb in lesson.get("content", {}).get("quizBlocks", []):
        content_blocks.append({
            "__component": "lesson-content.quizz-block",
            "Question": qb.get("Question", ""),
            "questionType": qb.get("questionType", "multiple-choice"),
            "options": qb.get("options", []),
            "correctAnswer": qb.get("correctAnswer", ""),
            "explanationcorrect": qb.get("explanationcorrect", []),
            "explanationfalse": qb.get("explanationfalse", []),
            "points": qb.get("points", 5),
        })

    return content_blocks


def create_chapters_and_lessons(
    agent: ChapterAndLessonGeneratorAgent,
    section_id: int,
    chapter_3_id: int,
    chapters_data: List[Dict],
    dry_run: bool,
) -> Dict[str, Any]:
    """Crée les chapitres 4 à 10 (prérequis ch4→ch3, ch5→ch4, …) et leurs leçons."""
    results = {"chapter_ids": [], "lesson_ids": [], "errors": []}
    base = agent.strapi_url.rstrip("/")
    headers = {
        "Authorization": f"Bearer {agent.strapi_token}",
        "Content-Type": "application/json",
    }
    # Chaîne de prérequis : pour le premier chapitre (order 4), prérequis = ch3
    previous_chapter_ids: List[int] = [chapter_3_id]

    for chapter_data in chapters_data:
        chapter_title = chapter_data.get("title", "Sans titre")
        order = chapter_data.get("order", 0)
        print(f"\n📚 Chapitre {order} : {chapter_title}")

        if dry_run:
            results["chapter_ids"].append(-order)
            for idx, lesson in enumerate(chapter_data.get("lessons", []), 1):
                print(f"  [DRY-RUN] Leçon {idx}: {lesson.get('title', '')}")
                results["lesson_ids"].append(0)
            continue

        # Créer le chapitre avec prérequis = previous_chapter_ids (un seul : le chapitre précédent)
        desc = chapter_data.get("description", f"Chapitre : {chapter_title}")
        if isinstance(desc, str):
            desc = agent.convert_markdown_to_richtext(desc)
        chapter_payload = {
            "data": {
                "title": chapter_title,
                "description": desc,
                "order": order,
                "section": section_id,
                "isActive": True,
                "estimatedDuration": sum(
                    les.get("estimatedDuration", 15) for les in chapter_data.get("lessons", [])
                ),
                "prerequisiteChapters": {"connect": list(previous_chapter_ids)},
            }
        }
        try:
            resp = requests.post(
                f"{base}/api/chapters",
                json=chapter_payload,
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            chapter_id = resp.json()["data"]["id"]
            previous_chapter_ids = [chapter_id]
            results["chapter_ids"].append(chapter_id)
            print(f"  ✅ Chapitre créé : ID {chapter_id} (prérequis: {chapter_payload['data']['prerequisiteChapters']['connect']})")
        except Exception as e:
            results["errors"].append(f"Création chapitre '{chapter_title}': {e}")
            print(f"  ❌ {e}")
            continue

        # Créer les leçons
        for idx, lesson in enumerate(chapter_data.get("lessons", []), 1):
            print(f"  📝 Leçon {idx}: {lesson.get('title', 'Sans titre')}")
            content_blocks = build_content_blocks(agent, lesson)
            lesson_payload = {
                "data": {
                    "title": lesson["title"],
                    "description": lesson.get("description", []),
                    "order": lesson.get("order", idx),
                    "chapter": chapter_id,
                    "lessonType": lesson.get("lessonType", "quizz"),
                    "content": content_blocks,
                    "isActive": lesson.get("isActive", True),
                    "estimatedDuration": lesson.get("estimatedDuration", 15),
                    "coinReward": lesson.get("coinReward", 150),
                    "slug": lesson.get("slug", agent._generate_slug(lesson["title"])),
                    "difficulty": lesson.get("difficulty", "easy"),
                    "tags": lesson.get("tags"),
                }
            }
            try:
                resp = requests.post(
                    f"{base}/api/lessons",
                    json=lesson_payload,
                    headers=headers,
                    timeout=30,
                )
                resp.raise_for_status()
                lesson_id = resp.json()["data"]["id"]
                results["lesson_ids"].append(lesson_id)
                print(f"    ✅ Leçon créée : ID {lesson_id}")
            except Exception as e:
                results["errors"].append(f"Leçon '{lesson.get('title')}': {e}")
                print(f"    ❌ {e}")
                if hasattr(e, "response") and e.response is not None:
                    print(f"       {e.response.text[:400]}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Import chapitres 4-10 Les bases dans Strapi (remplace anciens ch4 et ch5).")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les actions sans supprimer ni créer.")
    parser.add_argument("--input", default=str(INPUT_JSON), help="Fichier JSON des chapitres 4-10.")
    args = parser.parse_args()

    strapi_url = os.getenv("STRAPI_URL", "https://cms.finsly.org")
    strapi_token = os.getenv("STRAPI_API_TOKEN")
    if not strapi_token:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Fichier introuvable : {input_path}")
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    chapters_data = data.get("chapters", [])
    if not chapters_data:
        print("❌ Aucun chapitre dans le JSON.")
        return 1

    # Agent (OpenAI key non utilisée pour cet import)
    agent = ChapterAndLessonGeneratorAgent(
        openai_api_key=os.getenv("OPENAI_API_KEY", "dummy"),
        strapi_url=strapi_url,
        strapi_token=strapi_token,
    )
    normalize_loaded_content(agent, chapters_data)
    print("✅ Contenu normalisé (options RT, explications, slugs).")

    # Section "Les bases"
    section = agent.find_section_by_title("Les bases")
    if not section:
        print("❌ Section 'Les bases' introuvable.")
        return 1
    section_id = section["id"]
    print(f"✅ Section trouvée : ID {section_id}")

    existing = agent.get_existing_chapters(section_id)
    existing_sorted = sorted(existing, key=_chapter_order)
    chapter_3 = next((c for c in existing_sorted if _chapter_order(c) == 3), None)
    to_delete = [c for c in existing_sorted if _chapter_order(c) in (4, 5)]

    if not chapter_3:
        print("❌ Chapitre d'ordre 3 introuvable (prérequis du chapitre 4).")
        return 1
    chapter_3_id = chapter_3.get("id")
    print(f"✅ Chapitre 3 (prérequis) : ID {chapter_3_id} — {_chapter_title(chapter_3)}")

    if to_delete:
        print(f"\n🗑 Suppression des anciens chapitres (ordre 4 et 5) et de leurs leçons :")
        for c in to_delete:
            print(f"   - « {_chapter_title(c)} » (ID {c.get('id')}, ordre {_chapter_order(c)})")
        errs = delete_lessons_and_chapters(
            strapi_url, strapi_token, [c.get("id") for c in to_delete], args.dry_run
        )
        for e in errs:
            print(f"  ⚠️ {e}")
    else:
        print("\nℹ️ Aucun chapitre d'ordre 4 ou 5 à supprimer.")

    print("\n📤 Création des chapitres 4 à 10 et des leçons…")
    res = create_chapters_and_lessons(
        agent, section_id, chapter_3_id, chapters_data, args.dry_run
    )
    if res["errors"]:
        print("\n⚠️ Erreurs rencontrées :")
        for e in res["errors"]:
            print(f"  - {e}")
    if args.dry_run:
        print("\n[DRY-RUN] Aucune modification effectuée. Relance sans --dry-run pour appliquer.")
    else:
        print(f"\n✅ Terminé : {len(res['chapter_ids'])} chapitre(s), {len(res['lesson_ids'])} leçon(s) créé(s).")
    return 0 if not res["errors"] else 1


if __name__ == "__main__":
    exit(main())
