#!/usr/bin/env python3
"""
Parcourt les leçons du chapitre "Introduction aux investissement" (section Les bases) :
- Remplace tout quiz de type "slider" par un QCM complet (même thème).
- Pour tout quiz incomplet (options ou explanationcorrect ou explanationfalse manquants) :
  remplace par un bloc complet (question, options, correctAnswer, explanationcorrect, explanationfalse).
Puis envoie un PUT par leçon (sans id dans les blocs).
"""
import os
import json
import requests
from pathlib import Path

STRAPI_URL = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
STRAPI_TOKEN = os.getenv("STRAPI_API_TOKEN")


def rt_paragraph(text: str):
    return {"type": "paragraph", "children": [{"text": text, "type": "text"}]}


def make_quiz_block(Question: str, questionType: str, options: list, correctAnswer: str,
                    explanationcorrect: str, explanationfalse: str, points: int = 5):
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


def is_slider(block):
    qtype = (block.get("questionType") or "").strip().lower()
    return qtype == "slider"


def is_incomplete(block):
    if block.get("__component") != "lesson-content.quizz-block":
        return False
    opts = block.get("options")
    has_opts = isinstance(opts, list) and len(opts) > 0
    has_ok = bool(block.get("explanationcorrect"))
    has_ko = bool(block.get("explanationfalse"))
    return not (has_opts and has_ok and has_ko)


def replacement_for_slider(block):
    """Remplace un bloc slider par un QCM sur le même thème (fiscalité PEA après 5 ans)."""
    return make_quiz_block(
        "Après 5 ans, quelle est la fiscalité sur les plus-values du PEA ?",
        "multiple-choice",
        [
            "Exonération d'impôt, uniquement prélèvements sociaux (17,2%)",
            "PFU 30% (impôt + prélèvements)",
            "Barème progressif de l'impôt sur le revenu",
            "Imposition à 45%",
        ],
        "Exonération d'impôt, uniquement prélèvements sociaux (17,2%)",
        "Exact ! Après 5 ans, plus-values et dividendes ne sont soumis qu'aux prélèvements sociaux (17,2%). C'est l'avantage majeur du PEA.",
        "Après 5 ans, le PEA n'est pas au PFU ni au barème : les plus-values sont exonérées d'impôt, seuls les prélèvements sociaux (17,2%) restent dus.",
    )


def replacement_for_incomplete(block):
    """Remplace un bloc incomplet par un bloc complet (même question/réponse si possible, sinon thème proche)."""
    q = (block.get("Question") or "").strip()
    ans = (block.get("correctAnswer") or "").strip()
    qtype = (block.get("questionType") or "multiple-choice").strip().lower()
    if qtype in ("slider", "drag-drop", "drag-order") or not qtype:
        qtype = "multiple-choice"

    # Remplacements ciblés selon la question (d'après l'analyse)
    if "allocation avec l'âge" in q or "allocation avec l'age" in q:
        return make_quiz_block(
            "Comment évolue l'allocation d'actifs avec l'âge ?",
            "multiple-choice",
            ["Plus d'actions avec l'âge", "Moins d'actions avec l'âge", "Aucun changement", "Tout en obligations après 40 ans"],
            "Moins d'actions avec l'âge",
            "Oui ! Plus on vieillit, plus on réduit la part d'actions pour privilégier la stabilité (obligations, monétaire).",
            "L'allocation évolue avec l'âge : on réduit progressivement la part d'actions pour limiter le risque.",
        )
    if "match" in q.lower() and "repartition" in q.lower():
        return make_quiz_block(
            "Quelle répartition est la plus adaptée pour un jeune de 25 ans ?",
            "multiple-choice",
            ["100% livret A", "80% actions, 20% obligations", "50% actions, 50% obligations", "100% obligations"],
            "80% actions, 20% obligations",
            "Parfait ! Un jeune peut avoir une forte part d'actions ; les obligations sécurisent un peu le portefeuille.",
            "Pour un jeune, une part importante d'actions est adaptée (horizon long). La diversification avec un peu d'obligations reste raisonnable.",
        )
    if "5 ans" in q and "fiscalité" in q and "plus-value" in q:
        return replacement_for_slider(block)
    if "sort avant 5 ans" in q or "sortir avant 5 ans" in q:
        return make_quiz_block(
            "Que se passe-t-il si on sort du PEA avant 5 ans ?",
            "multiple-choice",
            ["On garde les avantages fiscaux", "On perd les avantages et le PEA se ferme définitivement", "On paie une pénalité de 10%", "Rien de particulier"],
            "On perd les avantages et le PEA se ferme définitivement",
            "Exact ! Sortir avant 5 ans = perte des avantages fiscaux et fermeture définitive du PEA. Mieux vaut rester investi.",
            "En cas de sortie avant 5 ans, tu perds les avantages fiscaux et ton PEA est fermé définitivement. Un seul PEA par personne, à vie.",
        )
    if "plafond du PEA" in q or "plafond du pea" in q.lower():
        return make_quiz_block(
            "Quel est le plafond de versement du PEA ?",
            "multiple-choice",
            ["50 000€", "100 000€", "150 000€", "Illimité"],
            "150 000€",
            "Oui ! Le plafond du PEA est de 150 000€ (pour les PEA ouverts à partir de 2017).",
            "Le plafond du PEA est de 150 000€. Au-delà, tu peux continuer à investir via un compte-titres classique.",
        )
    if "éviter" in q or "eviter" in q:
        return make_quiz_block(
            "D'après le cours, il faut éviter :",
            "multiple-choice",
            [
                "Les contrats d'assurance-vie en ligne (Linxea, etc.)",
                "Les assurances-vie traditionnelles des banques (frais élevés, choix limités)",
                "Le PEA",
                "Les ETF",
            ],
            "Les assurances-vie traditionnelles des banques (frais élevés, choix limités)",
            "Exact ! Il vaut mieux privilégier les contrats modernes en ligne (Linxea, Placement-direct) que les assurances-vie traditionnelles des banques.",
            "Le cours recommande d'éviter les assurances-vie traditionnelles du banquier (frais élevés, choix limités) et de privilégier les contrats en ligne.",
        )
    if "avantage" in q and "assurance-vie" in q and "PEA" in q:
        return make_quiz_block(
            "Quel est l'avantage de l'assurance-vie par rapport au PEA ?",
            "multiple-choice",
            [
                "Fiscalité plus avantageuse après 5 ans",
                "Accès aux marchés mondiaux (pas seulement l'Europe)",
                "Plafond plus élevé",
                "Pas de frais",
            ],
            "Accès aux marchés mondiaux (pas seulement l'Europe)",
            "Oui ! L'assurance-vie permet d'investir sur tous les marchés mondiaux, alors que le PEA est limité à l'Europe.",
            "Le gros plus de l'assurance-vie par rapport au PEA : investir sur tous les marchés mondiaux, pas seulement l'Europe.",
        )
    if "fiscalité" in q and "8 ans" in q and "17,2" in q:
        return make_quiz_block(
            "La fiscalité de l'assurance-vie après 8 ans est uniquement de 17,2% (prélèvements sociaux).",
            "true-false",
            ["Vrai", "Faux"],
            "Faux",
            "Faux ! Après 8 ans la fiscalité est dégressive (abattement puis 7,5% dans certains cas), pas uniquement 17,2%.",
            "La fiscalité de l'assurance-vie après 8 ans n'est pas simplement 17,2% : elle est dégressive avec abattement et peut aller jusqu'à 7,5%.",
        )

    # Fallback : bloc générique pour ne pas perdre la question
    if qtype == "true-false":
        opts = ["Vrai", "Faux"]
        if ans and ans.lower() not in ("vrai", "faux", "true", "false", "wrong", "right"):
            ans = "Vrai" if ans.lower() in ("vrai", "true", "right", "correct") else "Faux"
    else:
        opts = [ans, "Autre réponse possible", "Ce n'est pas la bonne réponse", "Aucune de ces réponses"] if ans else ["Réponse A", "Réponse B", "Réponse C", "Réponse D"]
        if not ans:
            ans = opts[0]
    return make_quiz_block(
        q or "Question",
        "multiple-choice" if qtype not in ("true-false", "true - false") else "true-false",
        opts,
        ans,
        "Bonne réponse !",
        "Ce n'est pas la bonne réponse. Revois le cours.",
    )


def strip_id(block):
    return {k: v for k, v in block.items() if k != "id"}


def main():
    if not STRAPI_TOKEN:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1
    headers = {"Authorization": f"Bearer {STRAPI_TOKEN}", "Content-Type": "application/json"}
    params = {"filters[chapter][id][$eq]": 11, "pagination[pageSize]": 25, "sort": "order:asc"}
    r = requests.get(f"{STRAPI_URL}/api/lessons", headers=headers, params=params, timeout=30)
    r.raise_for_status()
    lessons_list = r.json().get("data", [])

    for lec in lessons_list:
        doc_id = lec.get("documentId")
        if not doc_id:
            continue
        req = requests.get(f"{STRAPI_URL}/api/lessons/{doc_id}", headers=headers, params={"populate": "*"}, timeout=30)
        if req.status_code != 200:
            print(f"  Skip {lec.get('title')}: GET {req.status_code}")
            continue
        d = req.json().get("data", {})
        title = d.get("title")
        content = list(d.get("content") or [])
        new_content = []
        replaced_slider = 0
        replaced_incomplete = 0
        for b in content:
            if b.get("__component") == "lesson-content.text-block":
                new_content.append(strip_id(b))
                continue
            if b.get("__component") == "lesson-content.quizz-block":
                if is_slider(b):
                    new_content.append(replacement_for_slider(b))
                    replaced_slider += 1
                elif is_incomplete(b):
                    new_content.append(replacement_for_incomplete(b))
                    replaced_incomplete += 1
                else:
                    new_content.append(strip_id(b))
                continue
            new_content.append(strip_id(b))

        if replaced_slider or replaced_incomplete:
            print(f"  [{d.get('order')}] {title}: {replaced_slider} slider(s) remplacé(s), {replaced_incomplete} bloc(s) incomplet(s) remplacé(s) → PUT...")
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
            print(f"  [{d.get('order')}] {title}: rien à corriger.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
