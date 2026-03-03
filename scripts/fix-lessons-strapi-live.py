#!/usr/bin/env python3
"""
Fixes a small set of live Strapi lessons based on docs/lessons-fix-plan-strapi-live.md.

TARGETED LESSONS ONLY (by documentId):
- m2rng62xfjrzp174bjvl15vw  -> "L'investissement dans les startups"
- p1asmgj7n5jlcngdgv5msjzy  -> "SCPI vs immobilier direct"
- n2vnjpu38vznbj5kfwyvyexe  -> "Budget et gestion des finances personnelles"
- ewzcsqnif4z08c40p43or6pl  -> "Les ETF (Exchange Traded Funds)"

What it does (when run):
- Loads the current snapshot from output/strapi-lessons-full.json as a baseline.
- For each targeted lesson:
  - Preserves all existing text-blocks.
  - Rebuilds the quiz-blocks according to the fix plan.
  - Sends a PUT /api/lessons/{documentId} with the new "content" array.

IMPORTANT:
- This script is NOT run automatically. Review docs/lessons-fix-plan-strapi-live.md first,
  then run it manually from the repo root:

    export STRAPI_URL="https://cms.finsly.org"
    export STRAPI_API_TOKEN="..."
    python scripts/fix-lessons-strapi-live.py --dry-run      # just shows payloads
    python scripts/fix-lessons-strapi-live.py                # applies fixes
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

import requests

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "output" / "strapi-lessons-full.json"


def rt_paragraph(text: str) -> Dict[str, Any]:
    """One Strapi Rich Text paragraph block."""
    return {"type": "paragraph", "children": [{"text": text, "type": "text"}]}


def make_quiz_block(
    Question: str,
    questionType: str,
    options: List[str],
    correctAnswer: str,
    explanationcorrect: str,
    explanationfalse: str,
    points: int = 5,
) -> Dict[str, Any]:
    """Build a lesson-content.quizz-block without any id."""
    opts_rt = [rt_paragraph(o) for o in options]
    return {
        "__component": "lesson-content.quizz-block",
        "Question": Question,
        "questionType": questionType,
        "options": opts_rt,
        "correctAnswer": correctAnswer,
        "explanationcorrect": [rt_paragraph(explanationcorrect)],
        "explanationfalse": [rt_paragraph(explanationfalse)],
        "points": points,
    }


def strip_id(block: Dict[str, Any]) -> Dict[str, Any]:
    """Remove Strapi component id if present."""
    return {k: v for k, v in block.items() if k != "id"}


def load_snapshot() -> List[Dict[str, Any]]:
    if not SNAPSHOT.exists():
        raise SystemExit(f"Snapshot not found: {SNAPSHOT}. Run the fetch script first.")
    with SNAPSHOT.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_lesson(snapshot: List[Dict[str, Any]], document_id: str) -> Dict[str, Any]:
    for L in snapshot:
        if L.get("documentId") == document_id:
            return L
    raise KeyError(f"Lesson with documentId={document_id} not found in snapshot.")


def build_content_startups(existing: Dict[str, Any]) -> List[Dict[str, Any]]:
    """New content for 'L'investissement dans les startups' (add 3 quizzes)."""
    content = existing.get("content") or []
    # Preserve all text-blocks
    new_content: List[Dict[str, Any]] = []
    for b in content:
        if b.get("__component") == "lesson-content.text-block":
            new_content.append(strip_id(b))

    # Quizz 1: part du portefeuille
    new_content.append(
        make_quiz_block(
            "En règle générale, quelle part de ton portefeuille l'investissement dans les startups devrait-il représenter ?",
            "multiple-choice",
            [
                "50–60 %",
                "20–30 %",
                "5–10 %",
                "0 % ou 100 %",
            ],
            "5–10 %",
            "Pour un investissement aussi risqué que les startups, on reste en général sur une petite part du portefeuille (5–10 %).",
            "Les startups sont ultra-risquées : y consacrer 50 % ou plus de ton patrimoine serait disproportionné.",
        )
    )

    # Quizz 2: nombre de lignes
    new_content.append(
        make_quiz_block(
            "Pour lisser le risque en investissant dans des startups, combien de lignes environ est-il conseillé d'avoir ?",
            "multiple-choice",
            [
                "1 ou 2",
                "5",
                "20–30",
                "100 minimum",
            ],
            "20–30",
            "Diversifier sur une vingtaine ou une trentaine de startups permet qu'une seule très grosse réussite compense plusieurs échecs.",
            "Avec 1 ou 2 startups, ton risque dépend presque entièrement d'un seul projet : c'est trop concentré.",
        )
    )

    # Quizz 3: critères d'analyse
    new_content.append(
        make_quiz_block(
            "Quels sont les principaux critères cités pour analyser une startup avant d'investir ?",
            "multiple-choice",
            [
                "Uniquement le logo et le site web",
                "Équipe, marché, produit, business model",
                "Le nombre d'abonnés sur Instagram",
                "Le fait que des amis en parlent",
            ],
            "Équipe, marché, produit, business model",
            "C'est exactement ce que la leçon met en avant : équipe, marché, produit et modèle économique.",
            "Regarder uniquement le bruit (réseaux sociaux, entourage) ne suffit pas : il faut analyser le fond du projet.",
        )
    )
    return new_content


def build_content_scpi(existing: Dict[str, Any]) -> List[Dict[str, Any]]:
    """New content for 'SCPI vs immobilier direct' (add 3 quizzes)."""
    content = existing.get("content") or []
    new_content: List[Dict[str, Any]] = []
    for b in content:
        if b.get("__component") == "lesson-content.text-block":
            new_content.append(strip_id(b))

    # Quizz 1: capital et effet de levier
    new_content.append(
        make_quiz_block(
            "Pourquoi l'immobilier direct est-il souvent plus difficile d'accès qu'une SCPI pour un jeune investisseur ?",
            "multiple-choice",
            [
                "Parce qu'il n'est pas légal avant 30 ans",
                "Parce qu'il faut un apport important et gérer le bien soi-même",
                "Parce que les SCPI rapportent toujours moins",
                "Parce qu'il faut acheter au moins 10 appartements d'un coup",
            ],
            "Parce qu'il faut un apport important et gérer le bien soi-même",
            "En immobilier direct, il faut un gros apport (souvent 20–30 %) et accepter la gestion (locataires, travaux, etc.).",
            "L'obstacle principal pour un jeune est l'apport et la gestion, pas l'âge légal.",
        )
    )

    # Quizz 2: avantage clé des SCPI
    new_content.append(
        make_quiz_block(
            "Quel est l'avantage principal des SCPI par rapport à l'immobilier locatif direct ?",
            "multiple-choice",
            [
                "Aucun apport n'est jamais nécessaire",
                "Tu peux investir de petits montants et déléguer totalement la gestion",
                "Les SCPI sont garanties en capital par l'État",
                "Les SCPI ne paient pas d'impôts",
            ],
            "Tu peux investir de petits montants et déléguer totalement la gestion",
            "Avec les SCPI, tu peux investir dès quelques centaines d'euros et des pros gèrent les biens pour toi.",
            "Les SCPI restent soumises à la fiscalité et ne sont pas garanties par l'État.",
        )
    )

    # Quizz 3: inconvénients des SCPI
    new_content.append(
        make_quiz_block(
            "Quel est un inconvénient important des SCPI mentionné dans la leçon ?",
            "multiple-choice",
            [
                "Elles ont des frais d'entrée élevés et une liquidité limitée",
                "Elles ne versent jamais de loyers",
                "Elles obligent à gérer soi-même les locataires",
                "Elles ne sont accessibles qu'aux millionnaires",
            ],
            "Elles ont des frais d'entrée élevés et une liquidité limitée",
            "Les SCPI ont souvent 6–10 % de frais d'entrée et la revente des parts peut prendre du temps.",
            "Au contraire, la gestion est déléguée et le ticket d'entrée est plutôt faible.",
        )
    )
    return new_content


def build_content_budget(existing: Dict[str, Any]) -> List[Dict[str, Any]]:
    """New content for 'Budget et gestion des finances personnelles' (replace 2 incomplete quizzes)."""
    content = existing.get("content") or []
    new_content: List[Dict[str, Any]] = []
    # Conserver tous les text-blocks, ignorer les quizz existants (incomplets)
    for b in content:
        if b.get("__component") == "lesson-content.text-block":
            new_content.append(strip_id(b))

    # Quizz 1: application de 50/30/20 sur 2000 €
    new_content.append(
        make_quiz_block(
            "Avec un salaire de 2000€ net, quelle répartition correspond à la règle 50/30/20 (besoins / envies / épargne) ?",
            "multiple-choice",
            [
                "500€ / 500€ / 1000€",
                "1000€ / 600€ / 400€",
                "800€ / 800€ / 400€",
                "1200€ / 400€ / 400€",
            ],
            "1000€ / 600€ / 400€",
            "50 % de 2000€ = 1000€ pour les besoins, 30 % = 600€ pour les envies, 20 % = 400€ pour l'épargne.",
            "La règle 50/30/20 implique 1000€ besoins / 600€ envies / 400€ épargne pour 2000€ nets.",
        )
    )

    # Quizz 2: cas particulier vivre chez ses parents
    new_content.append(
        make_quiz_block(
            "Si tu vis chez tes parents avec très peu de dépenses fixes, que conseille la leçon ?",
            "multiple-choice",
            [
                "Augmenter fortement la part consacrée aux loisirs",
                "Profiter de charges faibles pour épargner plus que 20 %",
                "Ne rien épargner tant que tu es jeune",
                "Tout investir en crypto",
            ],
            "Profiter de charges faibles pour épargner plus que 20 %",
            "C'est le moment idéal pour booster ton épargne (matelas de sécurité, futur apport, etc.).",
            "L'idée n'est pas de tout dépenser en loisirs mais de profiter de cette période pour construire ton épargne.",
        )
    )
    return new_content


def build_content_etf(existing: Dict[str, Any]) -> List[Dict[str, Any]]:
    """New content for 'Les ETF (Exchange Traded Funds)' (fix 1 incomplete quiz)."""
    content = existing.get("content") or []
    new_content: List[Dict[str, Any]] = []
    # Conserver text-blocks, ignorer le quizz existant (incomplet)
    for b in content:
        if b.get("__component") == "lesson-content.text-block":
            new_content.append(strip_id(b))

    # Quizz: nombre d'entreprises dans l'ETF MSCI World
    new_content.append(
        make_quiz_block(
            "En ordre de grandeur, combien d'entreprises contient l'ETF MSCI World ?",
            "multiple-choice",
            [
                "Environ 40",
                "Environ 500",
                "Plus de 1 600",
                "Plus de 10 000",
            ],
            "Plus de 1 600",
            "L'ETF MSCI World regroupe plus de 1600 entreprises des pays développés, ce qui offre une forte diversification.",
            "L'ordre de grandeur est bien supérieur à quelques dizaines ou centaines d'entreprises.",
        )
    )
    return new_content


FIX_TARGETS = {
    "m2rng62xfjrzp174bjvl15vw": build_content_startups,
    "p1asmgj7n5jlcngdgv5msjzy": build_content_scpi,
    "n2vnjpu38vznbj5kfwyvyexe": build_content_budget,
    "ewzcsqnif4z08c40p43or6pl": build_content_etf,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix a small set of Strapi lessons (see docs/lessons-fix-plan-strapi-live.md)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not send PUT requests, just print what would be updated.",
    )
    args = parser.parse_args()

    strapi_url = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
    strapi_token = os.getenv("STRAPI_API_TOKEN")
    if not strapi_token:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1

    headers = {
        "Authorization": f"Bearer {strapi_token}",
        "Content-Type": "application/json",
    }

    snapshot = load_snapshot()
    base = f"{strapi_url}/api/lessons"

    for doc_id, builder in FIX_TARGETS.items():
        print(f"\n🔍 Traitement de la leçon documentId={doc_id}")
        try:
            snap_lesson = find_lesson(snapshot, doc_id)
        except KeyError as e:
            print(f"  ⚠️ {e}")
            continue
        title = snap_lesson.get("title")
        print(f"  Titre: {title!r}")

        # Rebuild content (text-blocks preserved, quizzes replaced/added)
        new_content = builder(snap_lesson)
        # Remove any lingering id on components
        new_content = [strip_id(b) for b in new_content]

        payload = {"data": {"content": new_content}}

        if args.dry_run:
            print(f"  [DRY-RUN] Payload for {doc_id} (titre {title!r}):")
            print(json.dumps(payload, ensure_ascii=False, indent=2)[:2000])
            continue

        try:
            resp = requests.put(f"{base}/{doc_id}", headers=headers, json=payload, timeout=30)
            if resp.status_code != 200:
                print(f"  ❌ PUT {doc_id} -> {resp.status_code}: {resp.text[:400]}")
            else:
                print(f"  ✅ Leçon mise à jour (documentId={doc_id})")
        except Exception as e:
            print(f"  ❌ Erreur lors de la mise à jour de {doc_id}: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

