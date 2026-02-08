#!/usr/bin/env python3
"""
Complète le contenu des leçons du chapitre "Introduction aux investissement" (section Les bases).
- Charge le contenu existant depuis output/strapi-lessons-full.json (à générer avant avec fetch)
- Ajoute les quiz (et si besoin 1 bloc texte) manquants pour atteindre au moins 6 quiz par leçon
- Met à jour chaque leçon dans Strapi via PUT (documentId)
Usage:
  export STRAPI_URL="https://cms.finsly.org"
  export STRAPI_API_TOKEN="..."
  python scripts/update-introduction-investissement-lessons.py
"""
import os
import json
import requests
from pathlib import Path

STRAPI_URL = os.getenv("STRAPI_URL", "https://cms.finsly.org").rstrip("/")
STRAPI_TOKEN = os.getenv("STRAPI_API_TOKEN")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FULL_JSON = ROOT / "output" / "strapi-lessons-full.json"


def rt_paragraph(text: str):
    """Un paragraphe Rich Text Strapi."""
    return {"type": "paragraph", "children": [{"text": text, "type": "text"}]}


def make_quiz_block(Question: str, questionType: str, options: list, correctAnswer: str,
                    explanationcorrect: str, explanationfalse: str, points: int = 5):
    """Construit un quizz-block au format Strapi (sans id)."""
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


def supplements_for_lesson(order: int):
    """Retourne les blocs à ajouter (quiz, et éventuellement 1 text) pour cette leçon."""
    # Leçon 1: 3 quiz existants → ajouter 3 pour atteindre 6
    if order == 1:
        return [
            make_quiz_block(
                "Les intérêts composés, c'est :",
                "multiple-choice",
                ["Des intérêts que l'on paie à la banque", "Des gains qui génèrent eux-mêmes des gains au fil du temps", "Un type d'impôt", "Une prime de bienvenue"],
                "Des gains qui génèrent eux-mêmes des gains au fil du temps",
                "Parfait ! Plus tu commences tôt, plus la capitalisation a le temps de faire son effet.",
                "L'avantage principal, c'est le temps laissé aux intérêts composés.",
            ),
            make_quiz_block(
                "Une épargne de précaution correspond en général à 3 à 6 mois de dépenses.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! 3 à 6 mois de dépenses sur un support sécurisé, c'est la recommandation classique.",
                "L'épargne de précaution recommandée correspond en général à 3 à 6 mois de dépenses.",
            ),
            make_quiz_block(
                "Mieux vaut commencer à épargner avec un petit montant régulier que d'attendre une grosse somme.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! La régularité et la durée comptent souvent plus que le montant du premier versement.",
                "C'est vrai : commencer tôt avec un petit montant régulier est généralement plus utile qu'attendre une grosse somme.",
            ),
        ]
    # Leçon 2: 0 quiz → ajouter 6
    if order == 2:
        return [
            make_quiz_block(
                "En général, plus le rendement potentiel est élevé :",
                "multiple-choice",
                ["Plus le risque est faible", "Plus le risque est élevé", "Moins il faut diversifier", "Plus c'est garanti par l'État"],
                "Plus le risque est élevé",
                "Exact ! Rendement et risque vont souvent de pair.",
                "En général, un rendement potentiel plus élevé va de pair avec un risque plus élevé.",
            ),
            make_quiz_block(
                "Diversifier son épargne permet de réduire le risque sans renoncer à tout rendement.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Répartir entre plusieurs actifs limite l'impact d'une mauvaise performance.",
                "C'est vrai : la diversification permet de limiter le risque tout en conservant un potentiel de rendement.",
            ),
            make_quiz_block(
                "Pourquoi l'horizon de placement est-il important ?",
                "multiple-choice",
                ["Parce que les banques l'exigent", "Parce qu'un horizon long permet de mieux absorber les variations sans vendre au mauvais moment", "Parce que les impôts sont plus bas après 10 ans", "Parce que c'est une mode"],
                "Parce qu'un horizon long permet de mieux absorber les variations sans vendre au mauvais moment",
                "Parfait ! Avec du temps, tu peux laisser passer les baisses sans être obligé de vendre.",
                "L'horizon long permet d'absorber les variations et d'éviter de vendre en période de baisse.",
            ),
            make_quiz_block(
                "Tu dois investir en actions l'argent dont tu pourrais avoir besoin dans 1 an.",
                "true-false",
                ["Vrai", "Faux"],
                "Faux",
                "Non ! Pour un besoin à court terme, mieux vaut un placement sécurisé (livret, etc.).",
                "C'est faux : pour un horizon court, les placements risqués (actions) ne sont pas adaptés.",
            ),
            make_quiz_block(
                "Le Livret A est un placement à :",
                "multiple-choice",
                ["Risque élevé, rendement élevé", "Risque faible, rendement faible", "Risque nul, rendement très élevé", "Risque modéré, rendement modéré"],
                "Risque faible, rendement faible",
                "Exact ! Livret A = peu de risque, rendement modeste mais garanti.",
                "Le Livret A est plutôt faible risque / faible rendement.",
            ),
            make_quiz_block(
                "Choisir son niveau de risque en fonction des tendances du moment est une bonne stratégie.",
                "true-false",
                ["Vrai", "Faux"],
                "Faux",
                "Non ! Mieux vaut se baser sur ta situation, ton horizon et ta tolérance au risque.",
                "C'est faux : il vaut mieux fonder ses choix sur sa situation et son horizon que sur l'ambiance du marché.",
            ),
        ]
    # Leçon 3: 2 quiz → ajouter 4
    if order == 3:
        return [
            make_quiz_block(
                "Quelle classe d'actif est en général la plus risquée ?",
                "multiple-choice",
                ["Le livret A", "Les actions", "Les fonds euros", "Le compte courant"],
                "Les actions",
                "Exact ! Les actions sont en général la classe la plus volatile.",
                "Parmi les options, les actions sont en général la plus risquée.",
            ),
            make_quiz_block(
                "Les obligations sont des prêts à des États ou des entreprises.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Parfait ! Une obligation, c'est un prêt : tu prêtes de l'argent en échange d'intérêts.",
                "Les obligations correspondent à des prêts (État ou entreprise), pas à des parts de sociétés.",
            ),
            make_quiz_block(
                "Diversifier entre plusieurs classes d'actifs permet de lisser les variations du portefeuille.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Les classes n'évoluent pas toujours ensemble ; la diversification limite l'impact des baisses.",
                "C'est vrai : répartir entre actions, obligations, monétaire, etc. aide à lisser les variations.",
            ),
            make_quiz_block(
                "\"Ne pas mettre tous ses œufs dans le même panier\" signifie :",
                "multiple-choice",
                ["Acheter uniquement des œufs", "Diversifier entre plusieurs placements ou classes d'actifs", "Ne jamais investir", "Tout mettre sur un seul placement"],
                "Diversifier entre plusieurs placements ou classes d'actifs",
                "Exact ! C'est l'idée de diversification : répartir pour limiter le risque.",
                "L'expression signifie diversifier : répartir son épargne entre plusieurs types de placements.",
            ),
        ]
    # Leçon 4: 3 quiz → ajouter 3
    if order == 4:
        return [
            make_quiz_block(
                "Après 5 ans, les plus-values du PEA sont exonérées d'impôt sur le revenu.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Après 5 ans, exonération d'impôt sur les plus-values (les prélèvements sociaux restent dus).",
                "C'est vrai : le PEA offre cet avantage fiscal après 5 ans.",
            ),
            make_quiz_block(
                "Le PEA a un plafond de versement.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Exact ! Le plafond est de 150 000€ (pour un PEA ouvert depuis 2017).",
                "Le PEA est bien plafonné (150 000€ pour les PEA ouverts depuis 2017).",
            ),
            make_quiz_block(
                "Le PEA est adapté à un investissement :",
                "multiple-choice",
                ["À très court terme (quelques mois)", "Long terme (5 ans ou plus)", "Uniquement pour les cryptomonnaies", "Sans plafond"],
                "Long terme (5 ans ou plus)",
                "Parfait ! Le PEA est fait pour l'investissement en actions sur le long terme.",
                "Le PEA est conçu pour un horizon long terme (5 ans minimum pour l'avantage fiscal).",
            ),
        ]
    # Leçon 5: 3 quiz → ajouter 3
    if order == 5:
        return [
            make_quiz_block(
                "L'assurance-vie offre des avantages fiscaux progressifs selon la durée de détention.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Avant 8 ans = PFU 30% ; après 8 ans = abattement puis avantages.",
                "C'est vrai : les avantages fiscaux de l'assurance-vie s'améliorent avec la durée.",
            ),
            make_quiz_block(
                "L'assurance-vie peut servir au transmission du patrimoine.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Exact ! Les contrats d'assurance-vie ont un régime fiscal avantageux pour les bénéficiaires.",
                "L'assurance-vie est effectivement un outil de transmission (avantages fiscaux pour les bénéficiaires).",
            ),
            make_quiz_block(
                "Après 8 ans, l'assurance-vie permet un abattement sur les gains. Cet abattement est de :",
                "multiple-choice",
                ["1 000€", "4 600€ (9 200€ pour un couple)", "20 000€", "Aucun abattement"],
                "4 600€ (9 200€ pour un couple)",
                "Parfait ! 4 600€ (9 200€ pour un couple) après 8 ans.",
                "L'abattement après 8 ans est de 4 600€ (9 200€ pour un couple).",
            ),
        ]
    # Leçon 6: 0 quiz → ajouter 6
    if order == 6:
        return [
            make_quiz_block(
                "Un biais cognitif en investissement, c'est :",
                "multiple-choice",
                ["Une garantie de gain", "Une tendance à raisonner de façon biaisée (ex: suivre la foule, avoir peur de perdre)", "Un type de compte bancaire", "Une obligation légale"],
                "Une tendance à raisonner de façon biaisée (ex: suivre la foule, avoir peur de perdre)",
                "Exact ! Les biais nous poussent à des décisions irrationnelles (vente en panique, surréaction aux news).",
                "Les biais cognitifs sont des déformations du raisonnement, pas des produits ou des garanties.",
            ),
            make_quiz_block(
                "Vendre en panique lors d'une grosse baisse du marché est souvent un réflexe rationnel.",
                "true-false",
                ["Vrai", "Faux"],
                "Faux",
                "Non ! C'est souvent un biais : on cristallise des pertes et on rate la reprise. La discipline paie.",
                "C'est faux : vendre en panique est souvent une réaction émotionnelle qui pénalise le rendement long terme.",
            ),
            make_quiz_block(
                "Suivre l'opinion du plus grand nombre pour choisir ses investissements est une stratégie sans risque.",
                "true-false",
                ["Vrai", "Faux"],
                "Faux",
                "Non ! C'est le biais de la foule : quand tout le monde achète, les prix sont souvent déjà hauts.",
                "C'est faux : suivre la foule peut conduire à acheter au plus haut et vendre au plus bas.",
            ),
            make_quiz_block(
                "La diversification permet de limiter l'impact des biais sur ton portefeuille.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Un portefeuille diversifié et une stratégie claire aident à résister aux réactions émotionnelles.",
                "C'est vrai : diversification et discipline limitent l'impact des biais.",
            ),
            make_quiz_block(
                "Quel comportement illustre un biais de perte (aversion à la perte) ?",
                "multiple-choice",
                ["Investir régulièrement sans regarder le cours", "Vendre tout dès -10% pour \"éviter de perdre plus\" alors que l'horizon est long", "Diversifier son portefeuille", "Rester investi 10 ans"],
                "Vendre tout dès -10% pour \"éviter de perdre plus\" alors que l'horizon est long",
                "Exact ! L'aversion à la perte nous pousse à cristalliser les pertes au pire moment.",
                "Le biais de perte pousse à sur-réagir aux baisses (vendre trop tôt) plutôt qu'à rester discipliné.",
            ),
            make_quiz_block(
                "Avoir un plan d'investissement écrit t'aide à résister aux biais émotionnels.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Un plan clair (montant, fréquence, horizon) aide à ne pas réagir à chaque fluctuation.",
                "C'est vrai : un plan défini à l'avance limite les décisions impulsives.",
            ),
        ]
    # Leçon 7: 0 quiz → ajouter 6
    if order == 7:
        return [
            make_quiz_block(
                "Le PER (Plan Épargne Retraite) est un produit :",
                "multiple-choice",
                ["Réservé aux fonctionnaires", "Ouvert à tous, destiné à compléter la retraite", "Sans avantage fiscal", "Sans plafond de versement"],
                "Ouvert à tous, destiné à compléter la retraite",
                "Exact ! Le PER est ouvert à tous et permet de se constituer un complément de retraite avec avantage fiscal.",
                "Le PER est bien un dispositif ouvert à tous pour compléter sa retraite.",
            ),
            make_quiz_block(
                "Les versements sur un PER peuvent donner droit à une réduction d'impôt.",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Les versements sont déductibles du revenu imposable (dans la limite du plafond).",
                "C'est vrai : les versements PER sont déductibles, ce qui réduit l'impôt.",
            ),
            make_quiz_block(
                "À la retraite, le capital du PER est :",
                "multiple-choice",
                ["Imposé uniquement à la flat tax", "Imposé comme un revenu (après abattement pour la part en capital)", "Exonéré d'impôt", "Imposé uniquement sur les plus-values"],
                "Imposé comme un revenu (après abattement pour la part en capital)",
                "Parfait ! Au déblocage, le capital est imposé (avec abattement pour la part capital selon l'âge).",
                "Au déblocage du PER, le capital est imposé comme revenu (avec abattement selon l'âge).",
            ),
            make_quiz_block(
                "Le PER peut être débloqué avant la retraite dans certains cas (achat de résidence principale, surendettement, etc.).",
                "true-false",
                ["Vrai", "Faux"],
                "Vrai",
                "Oui ! Des déblocages anticipés sont possibles sous conditions (résidence principale, surendettement, invalidité, etc.).",
                "C'est vrai : le PER autorise des déblocages anticipés dans des situations définies par la loi.",
            ),
            make_quiz_block(
                "Le PER remplace intégralement la retraite obligatoire.",
                "true-false",
                ["Vrai", "Faux"],
                "Faux",
                "Non ! Le PER est un complément à la retraite obligatoire (régime de base + régimes complémentaires).",
                "C'est faux : le PER complète la retraite, il ne la remplace pas.",
            ),
            make_quiz_block(
                "Qui peut ouvrir un PER ?",
                "multiple-choice",
                ["Uniquement les salariés du privé", "Uniquement les plus de 50 ans", "Toute personne (salarié, indépendant, etc.)", "Uniquement les fonctionnaires"],
                "Toute personne (salarié, indépendant, etc.)",
                "Exact ! Le PER est ouvert aux salariés, indépendants, etc.",
                "Le PER est accessible à tous (salariés, indépendants, etc.).",
            ),
        ]
    return []


def main():
    if not STRAPI_TOKEN:
        print("❌ STRAPI_API_TOKEN non défini.")
        return 1
    if not FULL_JSON.exists():
        print(f"❌ Fichier non trouvé : {FULL_JSON}")
        print("   Lance d'abord le script de récupération (voir doc ou commande python qui charge les 7 leçons avec populate=*).")
        return 1
    with open(FULL_JSON, "r", encoding="utf-8") as f:
        lessons = json.load(f)
    headers = {"Authorization": f"Bearer {STRAPI_TOKEN}", "Content-Type": "application/json"}
    for L in lessons:
        if "error" in L:
            print(f"⚠️ Skip lesson error: {L.get('documentId')}")
            continue
        order = L["order"]
        title = L["title"]
        doc_id = L["documentId"]
        content = list(L.get("content") or [])
        to_add = supplements_for_lesson(order)
        if not to_add:
            print(f"  [{order}] {title}: rien à ajouter.")
            continue
        for b in to_add:
            content.append(b)
        # Strapi n'accepte pas la clé "id" dans les composants : on l'enlève partout
        def strip_id(block):
            return {k: v for k, v in block.items() if k != "id"}
        content = [strip_id(b) for b in content]
        print(f"  [{order}] {title}: +{len(to_add)} bloc(s) → PUT...")
        resp = requests.put(
            f"{STRAPI_URL}/api/lessons/{doc_id}",
            json={"data": {"content": content}},
            headers=headers,
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"     ❌ Erreur {resp.status_code}: {resp.text[:300]}")
        else:
            print(f"     ✅ Mis à jour.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
