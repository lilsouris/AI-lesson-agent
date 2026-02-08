#!/usr/bin/env python3
"""
Génère output/les-bases-chapitres-4-a-10.json : 7 chapitres (ordres 4 à 10) pour la section "Les bases".
Conçu pour NE PAS faire doublon avec le contenu déjà présent dans Strapi (voir analyse ci-dessous).

DÉJÀ COUVERT dans Strapi – à ne pas répéter :
- Ch1 : Inflation, matelas 3-6 mois, 50/30/20, premier salaire, tracking dépenses, objectifs SMART,
        intérêts simples vs composés, psychologie de l'argent (biais, automatiser).
- Ch2 : Épargne de précaution où (Livret A, LEP, LDDS), FIRE, banque tradi vs en ligne.
- Ch3 : Pourquoi épargner jeune, risque/rendement, classes d'actifs, PEA, assurance-vie, biais cognitifs, PER.
- Ch4 actuel : Intérêts simples vs composés (doublon ch1), DCA / investissement programmé.
- Ch5 actuel : Le lointain futur (transmission, retraite, pension – leçons souvent vides).

Donc les nouveaux chapitres 4-10 :
- 4 : Les frais en pratique (où les trouver, comparer courtiers/contrats – pas de long discours "ennemi silencieux").
- 5 : Ouvrir et utiliser son PEA ou AV (étapes concrètes : documents, premier virement, premier ordre).
- 6 : Quand les marchés chutent (que faire concrètement, volatilité, ne pas vendre en panique – angle crise).
- 7 : Choisir ses premiers ETF (quel type pour démarrer, frais bas – pas refaire les classes d'actifs).
- 8 : Se protéger : arnaques et promesses irréalistes.
- 9 : Retraite et long terme : où j'en suis ? (système français en bref, horizon – pas refaire le PER en détail).
- 10 : Et après ? (par où continuer : Bourse, immobilier, fiscalité – pas récap des 5 piliers).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "les-bases-chapitres-4-a-10.json"


def lesson(title, description, order, difficulty, text_blocks, quiz_blocks, duration=12):
    return {
        "title": title,
        "description": description,
        "order": order,
        "difficulty": difficulty,
        "estimatedDuration": duration,
        "content": {
            "textBlocks": text_blocks,
            "quizBlocks": quiz_blocks,
        },
    }


def text_blocks_pages(pages):
    """
    Construit les text-blocks au format Strapi : titre = "Page 1", "Page 2", ...
    et contenu = **Titre descriptif** + paragraphes (le titre d'origine est donc en tête du contenu).
    pages: liste de (titre_descriptif, contenu_markdown) ou (titre_descriptif, contenu_markdown, highlight).
    """
    out = []
    for i, p in enumerate(pages, 1):
        if len(p) == 3:
            tit, cont, highlight = p
        else:
            tit, cont = p
            highlight = False
        content_str = f"**{tit}**\n\n{cont}".strip() if tit else cont
        out.append({"title": f"Page {i}", "content": content_str, "highlight": highlight})
    return out


def q(question, qtype, options, correct, exp_c, exp_f, points=5):
    return {
        "Question": question,
        "questionType": qtype,
        "options": options,
        "correctAnswer": correct,
        "explanationcorrect": exp_c,
        "explanationfalse": exp_f,
        "points": points,
    }


def mc(question, options, correct, exp_c, exp_f):
    return q(question, "multiple-choice", options, correct, exp_c, exp_f)


def tf(question, correct, exp_c, exp_f):
    return q(question, "true-false", ["Vrai", "Faux"], correct, exp_c, exp_f)


def matching(question, options, correct_answer, exp_c, exp_f):
    """options: liste de lignes type A. ..., 1. ..., B. ..., 2. ... (sera fusionné en 1 bloc par normalize)."""
    return q(question, "matching", options, correct_answer, exp_c, exp_f)


def drag_order(question, options_random_order, correct_order_comma_separated, exp_c, exp_f):
    """options_random_order: liste des items en ordre aléatoire ; correct_order_comma_separated: même items dans l'ordre correct, séparés par des virgules."""
    return q(question, "drag-order", options_random_order, correct_order_comma_separated, exp_c, exp_f)


def drag_drop(question_with_blanks, options_words, full_sentence_answer, exp_c, exp_f):
    """question_with_blanks: phrase avec _____ ; options_words: mots à glisser ; full_sentence_answer: phrase complète."""
    return q(question_with_blanks, "drag-drop", options_words, full_sentence_answer, exp_c, exp_f)


# ---------- Chapitre 4 : Les frais en pratique (sans redire "pourquoi c'est l'ennemi" – déjà vu) ----------
CHAP4 = {
    "title": "Les frais en pratique",
    "description": "Où trouver les frais (DICI, fiches), comment comparer courtiers et contrats, et quels ordres de grandeur viser pour ne pas se faire plumer.",
    "order": 4,
    "lessons": [
        lesson(
            "Où trouver les frais d'un fonds ou d'un ETF",
            "DICI, fiches produits et documents à consulter avant d'investir.",
            1,
            "easy",
            text_blocks_pages([
                ("DICI et fiches produits", "Le **DICI** (Document d'Information Clé pour l'Investisseur) résume un fonds : objectif, risque, **frais annuels** (TER – Total Expense Ratio). Tu le trouves sur le site du gestionnaire ou de ton courtier. Pour un **ETF**, la fiche produit ou le KID (Key Information Document) indique aussi les frais. En 2 minutes tu vois si tu es à 0,1 %, 0,5 % ou 1,5 % par an. C'est la première chose à regarder avant d'acheter."),
                ("Frais de gestion, frais d'entrée, frais de transaction", "**Frais de gestion** : prélevés chaque année sur le fonds (déjà dans le TER). **Frais d'entrée** : certains contrats d'assurance-vie ou fonds en prennent (1 à 3 %) – à éviter quand tu peux. **Frais de transaction** : par ordre d'achat/vente (courtier). Pour un achat régulier, des ordres à 0 € ou 1 € sont courants. Compare le coût total (gestion + ordre) sur la durée."),
            ]),
            [
                mc("Où trouve-t-on les frais annuels (TER) d'un fonds ou d'un ETF ?", ["Dans la pub du courtier", "Dans le DICI ou la fiche produit / KID", "En appelant sa banque", "Ils ne sont pas publics"], "Dans le DICI ou la fiche produit / KID", "Exactement ! Le DICI et les fiches produits indiquent les frais. Toujours les consulter avant d'acheter.", "DICI et fiches produits (KID) : les frais annuels y figurent."),
                matching(
                    "Associe chaque document ou notion à sa définition :",
                    ["A. DICI", "1. Document qui résume un fonds (objectif, risque, frais annuels)", "B. TER", "2. Frais annuels totaux du fonds (Total Expense Ratio)", "C. KID", "3. Key Information Document – fiche d'information clé pour l'investisseur"],
                    "A → 1, B → 2, C → 3",
                    "Parfait ! DICI = doc du fonds, TER = frais annuels, KID = fiche d'information clé.",
                    "DICI résume le fonds ; TER = frais annuels ; KID = Key Information Document.",
                ),
                mc("Que signifie TER (Total Expense Ratio) ?", ["Le rendement garanti", "Les frais annuels du fonds (gestion, etc.)", "Le montant minimum d'investissement", "La durée du placement"], "Les frais annuels du fonds (gestion, etc.)", "Parfait ! Le TER résume ce que le fonds te prend chaque année. Plus il est bas, mieux c'est.", "TER = frais annuels totaux du fonds (déjà déduits du rendement)."),
                tf("Pour un achat régulier (ex. chaque mois), les frais par ordre peuvent être nuls ou très faibles selon le courtier.", "Vrai", "Oui. Beaucoup de courtiers proposent des ordres à 0 € ou 1 €. À vérifier avant d'ouvrir un compte.", "Vrai : ordres gratuits ou à 1 € sont courants pour les achats réguliers."),
            ],
        ),
        lesson(
            "Comparer courtiers et contrats",
            "Sur quels critères choisir son PEA et son assurance-vie sans se faire avoir.",
            2,
            "easy",
            text_blocks_pages([
                ("PEA : frais d'ordre, frais de garde", "En **PEA**, compare : **frais par ordre** (0 € à quelques euros), **frais de garde** (souvent 0 € en ligne), **frais de clôture**. Pour un investissement mensuel, des ordres à 0 € ou 1 € sont idéaux. Les courtiers en ligne (Boursorama, Fortuneo, Bourse Direct, etc.) sont en général moins chers que les banques en agence."),
                ("Assurance-vie : frais d'entrée, frais sur UC", "En **assurance-vie**, vérifie : **frais d'entrée** (0 % sur les contrats en ligne type Linxea, Placement-direct), **frais de gestion sur les unités de compte** (0,5 % à 1 % selon les supports). Évite les contrats « traditionnels » en agence avec 2–3 % d'entrée et des frais de gestion élevés. Pour un jeune, un contrat en ligne sans frais d'entrée est le bon choix."),
            ]),
            [
                drag_drop(
                    "Pour un PEA, _____ à 0 € ou 1 € et des ETF avec un _____ sous 0,5 % sont l'idéal.",
                    ["des ordres", "TER", "un virement", "frais", "rendement", "plafond"],
                    "Pour un PEA, des ordres à 0 € ou 1 € et des ETF avec un TER sous 0,5 % sont l'idéal.",
                    "Parfait ! Ordres pas chers + TER bas = tu gardes un maximum de rendement pour toi.",
                    "La bonne phrase : des ordres à 0 € ou 1 €, et un TER (frais annuels) sous 0,5 %.",
                ),
                mc("Quel critère est important pour un PEA quand on investit chaque mois ?", ["La couleur de l'application", "Les frais par ordre (idéalement 0 € ou très bas)", "Le nombre de marchés exotiques", "La taille de la banque"], "Les frais par ordre (idéalement 0 € ou très bas)", "Exactement ! Sur des années, des frais par ordre élevés grignotent. 0 € ou 1 € par ordre est l'idéal.", "Frais par ordre : avec un achat par mois, ça compte sur la durée."),
                tf("Les contrats d'assurance-vie en ligne (Linxea, Placement-direct) ont souvent 0 % de frais d'entrée.", "Vrai", "Oui. C'est un de leurs atouts par rapport aux contrats en agence.", "Vrai : les contrats en ligne proposent souvent 0 % de frais d'entrée."),
                mc("Quel type de contrat d'assurance-vie faut-il éviter en priorité quand on débute ?", ["Un contrat en ligne sans frais d'entrée", "Un contrat en agence avec frais d'entrée élevés et frais de gestion élevés", "Un contrat en unités de compte", "Un contrat en fonds euros"], "Un contrat en agence avec frais d'entrée élevés et frais de gestion élevés", "Parfait ! Les frais en agence te coûtent cher. En ligne, tu gardes l'essentiel du rendement.", "Éviter les contrats en agence avec 2–3 % d'entrée et frais de gestion élevés."),
                tf("Les frais de garde en PEA sont identiques chez tous les courtiers.", "Faux", "Ils varient : certains les offrent à 0 €, d'autres les facturent. À inclure dans la comparaison.", "Faux : à vérifier (souvent 0 € en ligne)."),
            ],
        ),
        lesson(
            "Quel ordre de grandeur viser ?",
            "Repères simples : ETF sous 0,5 %, contrats sans frais d'entrée.",
            3,
            "easy",
            text_blocks_pages([
                ("ETF et fonds : viser moins de 0,5 % de frais annuels", "Pour un **ETF** en PEA ou en assurance-vie, un **TER sous 0,5 %** (idéalement 0,1 % à 0,3 %) est le bon ordre de grandeur. Les ETF monde ou CAC 40 low cost sont souvent dans cette fourchette. Au-delà de 0,7–1 %, questionne-toi : y a-t-il une vraie plus-value (fonds géré activement performant) ou tu paies juste plus cher pour un résultat similaire ?"),
                ("Récap pratique", "**PEA** : courtier avec ordres pas chers ou gratuits + ETF à TER < 0,5 %. **Assurance-vie** : contrat en ligne sans frais d'entrée + supports (ETF/fonds) à frais raisonnables. Tu n'as pas besoin de chercher le 0,01 % partout : l'essentiel est d'éviter les contrats et supports très chers (entrée 2–3 %, TER > 1 %)."),
            ]),
            [
                mc("Pour un ETF, quel ordre de grandeur de frais annuels (TER) est raisonnable ?", ["2 % à 3 %", "0,1 % à 0,5 %", "10 %", "Aucun frais"], "0,1 % à 0,5 %", "Exactement ! Les ETF low cost sont souvent entre 0,1 % et 0,5 %. Au-delà, vérifie si ça vaut le coup.", "ETF low cost : souvent 0,1 % à 0,5 % de TER."),
                tf("Un contrat d'assurance-vie avec 2 % de frais d'entrée et des frais de gestion élevés est un bon choix pour démarrer.", "Faux", "Mieux vaut un contrat en ligne sans frais d'entrée et des frais de gestion raisonnables.", "Faux : privilégier 0 % d'entrée et frais de gestion bas."),
                mc("L'objectif est surtout d'éviter :", ["Tout frais", "Les contrats et supports très chers (entrée 2–3 %, TER > 1 %)", "Les ETF", "Les courtiers en ligne"], "Les contrats et supports très chers (entrée 2–3 %, TER > 1 %)", "Parfait ! Pas besoin d'optimiser au centime ; éviter les très chers suffit pour bien démarrer.", "Éviter les très chers (gros frais d'entrée, TER élevé)."),
            ],
        ),
    ],
}

# ---------- Chapitre 5 : Ouvrir et utiliser son PEA ou son assurance-vie (étapes concrètes, pas redire ce que c'est) ----------
CHAP5 = {
    "title": "Ouvrir et utiliser son PEA ou son assurance-vie",
    "description": "Les étapes concrètes : quels documents, comment faire le premier virement et passer le premier ordre, sans redire ce qu'est un PEA ou une AV.",
    "order": 5,
    "lessons": [
        lesson(
            "Documents et délais pour ouvrir un compte",
            "Ce qu'il faut préparer et combien de temps ça prend.",
            1,
            "easy",
            text_blocks_pages([
                ("Quoi préparer", "**Pièce d'identité** (CNI ou passeport), **justificatif de domicile** (facture, avis d'imposition), **RIB**. Pour un **PEA** : tu dois être résident fiscal français et ne pas avoir déjà un autre PEA (un seul par personne). Pour l'**assurance-vie** : un seul contrat suffit pour commencer. Choisis un courtier ou une banque en ligne avec des frais bas (voir chapitre précédent)."),
                ("Délais et ouverture en ligne", "Tu remplis le formulaire en ligne (identité, situation fiscale, connaissance des risques). Tu envoies les pièces. En général le compte est ouvert sous **quelques jours**. Une fois ouvert, tu fais un **virement** depuis ton compte courant vers ton PEA ou ton contrat d'assurance-vie. Pas besoin d'une grosse somme pour commencer : 100 € ou 200 € suffisent pour le premier versement."),
            ]),
            [
                mc("Combien de PEA peux-tu détenir en France ?", ["Autant que je veux", "Un seul par personne", "Deux maximum", "Un par banque"], "Un seul par personne", "Exactement ! Un PEA par personne, à vie. Choisis bien ton courtier au départ.", "Un seul PEA par personne."),
                tf("Pour ouvrir un PEA, il faut être résident fiscal français.", "Vrai", "Oui. Résidence fiscale en France obligatoire.", "Vrai : le PEA est réservé aux résidents fiscaux français."),
                mc("Quel document n'est en général pas demandé pour ouvrir un PEA ?", ["Pièce d'identité", "RIB", "Justificatif de domicile", "Relevé de compte des 5 dernières années"], "Relevé de compte des 5 dernières années", "ID, domicile et RIB suffisent en général. Pas d'historique long.", "On demande ID, domicile, RIB. Pas d'historique de compte."),
                drag_order(
                    "Classe ces étapes pour ouvrir un PEA dans le bon ordre :",
                    ["Faire un virement vers le PEA", "Remplir le formulaire en ligne et envoyer les pièces", "Choisir un courtier et aller sur son site", "Passer un ordre d'achat (ETF ou fonds)"],
                    "Choisir un courtier et aller sur son site, Remplir le formulaire en ligne et envoyer les pièces, Faire un virement vers le PEA, Passer un ordre d'achat (ETF ou fonds)",
                    "Parfait ! 1) Choisir le courtier, 2) Ouvrir le compte (formulaire + pièces), 3) Virer l'argent, 4) Acheter des parts.",
                    "L'ordre correct : choisir le courtier → ouvrir le compte (formulaire, pièces) → virement → premier ordre d'achat.",
                ),
                tf("Un premier versement de 100 ou 200 € est suffisant pour ouvrir et commencer.", "Vrai", "Pas besoin d'attendre des milliers d'euros. Ouvrir tôt fait courir la durée (ex. 5 ans pour le PEA).", "Vrai : 100–200 € pour le premier versement, c'est un bon début."),
            ],
        ),
        lesson(
            "Premier virement et premier ordre",
            "De l'argent sur le compte à l'achat de parts (ETF ou fonds).",
            2,
            "easy",
            text_blocks_pages([
                ("Du virement à l'ordre", "Une fois l'argent viré sur ton PEA ou ton assurance-vie, il est sur le **compte espèces**. Pour qu'il travaille, tu dois **acheter** un support : des parts d'ETF ou de fonds. En PEA tu passes un ordre d'achat sur un ou plusieurs ETF. En assurance-vie tu répartis entre fonds euros et unités de compte (ETF/fonds). Pour démarrer, un ETF monde ou un ETF CAC 40 est souvent recommandé."),
                ("Passer l'ordre sans stress", "Tu choisis l'ETF (ou le fonds), tu indiques le **montant** ou le **nombre de parts**, tu valides. L'ordre est exécuté au prix du marché. Pour un investissement long terme, inutile de chercher le « meilleur » jour : ce qui compte c'est d'investir régulièrement. Si tu as mis en place un virement automatique, tu peux aussi programmer un ordre automatique (investissement programmé) sur beaucoup de plateformes."),
            ]),
            [
                mc("Une fois l'argent viré sur ton PEA, où se trouve-t-il tant que tu n'as rien acheté ?", ["Nulle part", "Sur le compte espèces du PEA", "Directement en actions", "Chez ton employeur"], "Sur le compte espèces du PEA", "L'argent reste en espèces jusqu'à ce que tu passes un ordre d'achat. Pour qu'il travaille, il faut acheter des parts (ETF, etc.).", "Sur le compte espèces. Il faut passer un ordre d'achat pour investir."),
                tf("Pour un investissement long terme, il est crucial de choisir le « meilleur » jour pour acheter.", "Faux", "La régularité compte plus que le timing. Investir chaque mois est plus important que d'attendre le bon jour.", "Faux : la régularité (DCA) prime. Le « bon » jour est souvent « maintenant » puis « chaque mois »."),
                mc("Quel type de support est souvent recommandé pour un premier investissement en PEA ?", ["Une seule action d'une entreprise", "Un ETF monde ou un ETF CAC 40", "Une option", "Une cryptomonnaie"], "Un ETF monde ou un ETF CAC 40", "Un ETF diversifié (monde ou CAC 40) est simple et adapté pour démarrer.", "ETF monde ou CAC 40 : diversification simple pour un débutant."),
                tf("En assurance-vie, l'argent peut être réparti entre fonds euros et unités de compte (ETF/fonds).", "Vrai", "Fonds euros = sécurisé, UC = potentiel de rendement avec du risque. Tu peux mixer selon ton profil.", "Vrai : fonds euros + UC pour équilibrer sécurité et rendement."),
            ],
        ),
        lesson(
            "Après l'ouverture : suivre sans obsession",
            "Vérifier que tout fonctionne sans réagir à chaque mouvement du marché.",
            3,
            "easy",
            text_blocks_pages([
                ("Vérifier sans stress", "Tu peux regarder ton compte **une fois par mois ou par trimestre** pour confirmer que les virements et les ordres passent bien. Pas besoin de regarder les cours tous les jours : les marchés fluctuent, c'est normal. Sur 10 ou 20 ans, ce qui compte c'est d'avoir investi régulièrement et d'avoir gardé des frais bas."),
                ("Les pièges à éviter", "**Ne pas vendre en panique** lors d'une baisse : vendre au plus bas transforme une perte « papier » en perte réelle. **Ne pas tout mettre d'un coup** si tu as le vertige : répartir sur plusieurs mois (investissement programmé) peut te rassurer. **Ne pas oublier** de garder ton épargne de précaution à jour avant d'augmenter les versements investis."),
            ]),
            [
                mc("À quelle fréquence est-il raisonnable de regarder son PEA quand on investit pour le long terme ?", ["Plusieurs fois par jour", "Une fois par mois ou par trimestre", "Une fois par an", "Jamais"], "Une fois par mois ou par trimestre", "Suffisant pour vérifier que tout fonctionne, sans se laisser embarquer par la volatilité.", "Une fois par mois ou par trimestre suffit pour un suivi serein."),
                tf("Vendre en panique lors d'une grosse baisse du marché est souvent une mauvaise idée.", "Vrai", "Vendre au plus bas verrouille les pertes. Rester investi permet de profiter de la reprise.", "Vrai : vendre en panique verrouille les pertes. Rester investi long terme est la bonne stratégie."),
                mc("Si tu as peur de tout investir d'un coup, que faire ?", ["Ne pas investir", "Répartir tes versements sur plusieurs mois (investissement programmé)", "Attendre 10 ans", "Investir seulement en crypto"], "Répartir tes versements sur plusieurs mois (investissement programmé)", "L'investissement programmé (DCA) réduit le stress et lisse le prix d'achat moyen.", "Répartir sur plusieurs mois : ça rassure et lisse le prix d'achat."),
                tf("Il faut toujours augmenter ses versements investis même si l'épargne de précaution n'est pas complète.", "Faux", "D'abord sécurise 3 à 6 mois de dépenses (épargne de précaution), ensuite tu peux augmenter l'investissement.", "Faux : d'abord compléter l'épargne de précaution, puis augmenter l'investissement."),
            ],
        ),
    ],
}

# ---------- Chapitre 6 : Quand les marchés chutent (angle crise, pas refaire la psychologie générale) ----------
CHAP6 = {
    "title": "Quand les marchés chutent",
    "description": "Que faire concrètement lors d'une baisse ou d'un krach : pourquoi ne pas vendre en panique, et comment garder le cap.",
    "order": 6,
    "lessons": [
        lesson(
            "Les krachs font partie de l'histoire",
            "Contexte historique pour relativiser une baisse.",
            1,
            "easy",
            text_blocks_pages([
                ("Des baisses ont déjà eu lieu", "En 2008 (crise financière), 2020 (COVID), ou des corrections de -20 % à -30 % en quelques mois : les marchés ont toujours fini par repartir sur le long terme. Ça ne veut pas dire que « ça remonte toujours » à court terme – mais si tu investis pour 10 ans ou plus, une grosse baisse une année donnée n'est souvent qu'une vague dans l'historique. Les gens qui ont vendu en 2008 ou en mars 2020 ont transformé une perte temporaire en perte définitive."),
                ("Ce que ça implique pour toi", "Si ton horizon est long (retraite, projet à 10+ ans), une baisse de 20 % ou 30 % cette année n'est pas une raison de tout vendre. Au contraire : si tu continues à acheter régulièrement, tu achètes des parts moins chères pendant la baisse. Rester calme et garder le cap est souvent la meilleure réaction."),
            ]),
            [
                drag_order(
                    "Classe ces réactions lors d'une grosse baisse, de la pire à la moins mauvaise :",
                    ["Attendre 24-48 h et relire son objectif", "Ne rien changer si ton horizon est long", "Vendre tout le jour même", "Puiser dans l'épargne de précaution si urgence"],
                    "Vendre tout le jour même, Puiser dans l'épargne de précaution si urgence, Ne rien changer si ton horizon est long, Attendre 24-48 h et relire son objectif",
                    "Du pire au moins pire : vendre tout le jour même (fige la perte) → puiser dans la précaution si urgence → ne rien changer → attendre et relire son objectif (meilleure réaction).",
                    "La pire = vendre tout le jour même. Puis puiser précaution si urgence, ne rien changer, et la moins mauvaise = attendre 24-48 h et relire son objectif.",
                ),
                mc("Historiquement, après des krachs (2008, 2020), les marchés ont :", ["Disparu", "Fini par repartir sur le long terme", "Reste stables", "Baissé pour toujours"], "Fini par repartir sur le long terme", "Sur le long terme, les marchés ont repris. Vendre au plus bas, c'est figer la perte.", "Historiquement, les marchés ont repris sur 10–20 ans."),
                tf("Si ton horizon est long (10+ ans), une baisse de 20 % une année n'est pas une raison de tout vendre.", "Vrai", "C'est une vague. Rester investi et continuer à acheter régulièrement est souvent la bonne stratégie.", "Vrai : horizon long = ne pas réagir à une baisse d'une année."),
                mc("Que se passe-t-il si tu vends tout lors d'un krach ?", ["Tu sécurises ton gain", "Tu transformes une perte temporaire en perte définitive", "Tu évites de perdre plus", "Rien"], "Tu transformes une perte temporaire en perte définitive", "Vendre au plus bas = la perte devient réelle. Rester investi laisse la possibilité de la reprise.", "Vendre en panique = perte définitive. Rester = possibilité de reprise."),
                tf("Continuer à acheter pendant une baisse permet parfois d'acheter des parts moins chères.", "Vrai", "En investissant régulièrement, tu achètes aussi quand les prix sont bas. Ça lisse ton prix d'achat moyen.", "Vrai : tu achètes aussi en bas de cycle, ce qui peut être favorable."),
            ],
        ),
        lesson(
            "Que faire concrètement lors d'une grosse baisse ?",
            "Les bons réflexes : ne pas vendre sous le coup de l'émotion, revoir son plan à froid.",
            2,
            "easy",
            text_blocks_pages([
                ("Ne pas décider sous le coup de l'émotion", "Quand les titres passent au rouge et que tout le monde parle de crise, la tentation est de tout vendre « pour limiter les dégâts ». C'est souvent le pire moment : tu vends au plus bas. **Règle simple** : ne prends pas de décision de vente le jour même d'une grosse chute. Attends 24 à 48 h, relis ton objectif (horizon long ?), et demande-toi si ta situation personnelle a vraiment changé (besoin d'argent à court terme ?). Si non, ne rien faire est souvent la bonne décision."),
                ("Revoir son plan à froid", "Si tu as vraiment besoin d'argent à court terme (perte d'emploi, urgence), puise d'abord dans ton **épargne de précaution** (livret), pas dans ton PEA ou ton assurance-vie. Si ta stratégie était « j'investis pour 15 ans », une baisse ne change pas cette stratégie. Tu peux revoir ton plan une fois par an à date fixe (ex. 1er janvier), pas à chaque mouvement de marché."),
            ]),
            [
                mc("Lors d'une grosse chute du marché, que faire en premier ?", ["Tout vendre immédiatement", "Ne pas prendre de décision de vente le jour même ; attendre 24–48 h et relire son objectif", "Doubler ses achats tout de suite", "Fermer son compte"], "Ne pas prendre de décision de vente le jour même ; attendre 24–48 h et relire son objectif", "L'émotion retombe. La plupart du temps, ne rien changer est la bonne décision.", "Attendre, relire son plan. Souvent « ne rien faire » est la bonne option."),
                tf("Si tu as besoin d'argent en urgence, il vaut mieux puiser dans ton épargne de précaution (livret) que de vendre ton PEA.", "Vrai", "L'épargne de précaution est faite pour ça. Vendre le PEA en plein krach = perte figée.", "Vrai : d'abord le livret (précaution), pas le PEA en crise."),
                mc("Quand revoir son plan d'investissement ?", ["Chaque jour", "À chaque mouvement de marché", "Une fois par an à date fixe (ex. 1er janvier)", "Jamais"], "Une fois par an à date fixe (ex. 1er janvier)", "À date fixe, à froid. Pas sous le coup d'une baisse ou d'une hausse.", "1 fois par an à date fixe : décision à froid."),
                tf("Vendre tout le jour d'un krach pour « limiter les dégâts » est souvent une mauvaise idée.", "Vrai", "Tu vends au plus bas et tu figes la perte. Rester investi laisse la place à la reprise.", "Vrai : vendre au plus bas = perte définitive."),
            ],
        ),
    ],
}

# ---------- Chapitre 7 : Choisir ses premiers ETF (pas refaire les classes d'actifs – déjà ch3) ----------
CHAP7 = {
    "title": "Choisir ses premiers ETF",
    "description": "Quel type d'ETF pour démarrer (monde, Europe), pourquoi viser les frais bas, et combien de lignes garder simple.",
    "order": 7,
    "lessons": [
        lesson(
            "ETF monde ou ETF zone : quoi acheter en premier ?",
            "Un ou deux ETF pour bien démarrer sans se compliquer.",
            1,
            "easy",
            text_blocks_pages([
                ("Un ETF monde pour tout simplifier", "Un **ETF monde** (ex. répliquant le MSCI World ou un indice monde) te donne des **centaines d'actions** à travers les pays développés en un seul produit. Un seul ETF peut suffire pour démarrer : diversification géographique et sectorielle sans gérer 50 lignes. Beaucoup d'investisseurs restent avec ça pendant des années."),
                ("ETF Europe ou CAC 40 en complément", "Si tu veux ajouter une ligne « France » ou « Europe », un **ETF CAC 40** ou **Euro Stoxx 50** est simple. Ça ne remplace pas l'ETF monde pour la diversification mondiale, mais ça peut compléter. Pour commencer, **1 à 2 ETF** (monde + éventuellement Europe) suffisent. Pas besoin de 10 fonds différents."),
            ]),
            [
                drag_order(
                    "Classe ces étapes pour choisir et acheter son premier ETF dans le bon ordre :",
                    ["Passer un ordre d'achat", "Ouvrir un PEA ou une assurance-vie", "Vérifier le TER sur la fiche produit", "Choisir un ETF monde ou CAC 40"],
                    "Ouvrir un PEA ou une assurance-vie, Choisir un ETF monde ou CAC 40, Vérifier le TER sur la fiche produit, Passer un ordre d'achat",
                    "Parfait ! 1) Ouvrir le compte, 2) Choisir le type d'ETF (monde ou CAC 40), 3) Vérifier les frais (TER), 4) Passer l'ordre.",
                    "L'ordre : ouvrir PEA/AV → choisir l'ETF (monde, CAC 40) → vérifier le TER → passer l'ordre d'achat.",
                ),
                mc("Quel type d'ETF permet de détenir des centaines d'actions à travers le monde en un seul produit ?", ["Une action individuelle", "Un ETF monde (ex. MSCI World)", "Un fonds euros", "Une obligation"], "Un ETF monde (ex. MSCI World)", "Un ETF monde = diversification mondiale en un seul achat. Idéal pour démarrer.", "ETF monde = beaucoup d'actions monde en un produit."),
                tf("Pour démarrer, 1 à 2 ETF (monde + éventuellement Europe) peuvent suffire.", "Vrai", "Pas besoin de 10 lignes. Simplicité = moins d'erreurs et moins de frais.", "Vrai : 1 à 2 ETF suffisent pour bien démarrer."),
                mc("Un ETF CAC 40 ou Euro Stoxx 50 sert à :", ["Remplacer un ETF monde", "Compléter une exposition Europe/France si tu le souhaites", "Garantir un rendement", "Éviter tout risque"], "Compléter une exposition Europe/France si tu le souhaites", "Ça complète, ça ne remplace pas la diversification mondiale d'un ETF monde.", "Compléter Europe/France. Le monde reste la base."),
            ],
        ),
        lesson(
            "Frais et simplicité",
            "Pourquoi viser des ETF à faibles frais et éviter d'en avoir trop.",
            2,
            "easy",
            text_blocks_pages([
                ("Viser des frais bas (TER < 0,5 %)", "Les ETF **low cost** ont des frais annuels (TER) souvent entre 0,1 % et 0,5 %. Plus c'est bas, plus tu gardes de rendement pour toi. Vérifie le TER sur la fiche produit ou le DICI avant d'acheter. Deux ETF monde peuvent avoir des performances proches mais des frais différents : choisis le moins cher pour un même type d'indice."),
                ("Éviter d'avoir trop de lignes", "Plus tu as de lignes (ETF + fonds), plus c'est compliqué à suivre et plus tu risques de dupliquer (plusieurs ETF qui font la même chose). **Rester simple** : 1 à 3 ETF bien choisis, frais bas, et tu laisses tourner. Tu pourras affiner plus tard si tu veux (secteur, zone), mais pour les bases, la simplicité gagne."),
            ]),
            [
                mc("Quel ordre de grandeur de TER (frais annuels) viser pour un ETF ?", ["2 % à 3 %", "0,1 % à 0,5 %", "10 %", "Aucun"], "0,1 % à 0,5 %", "Les ETF low cost sont dans cette fourchette. Plus c'est bas, mieux c'est.", "0,1 % à 0,5 % : ordre de grandeur des ETF low cost."),
                tf("Avoir beaucoup de lignes (10+ ETF) est nécessaire pour bien diversifier quand on débute.", "Faux", "1 à 3 ETF suffisent. Trop de lignes = complexité et risque de doublons.", "Faux : 1 à 3 ETF suffisent. La simplicité gagne."),
                mc("Où vérifier le TER d'un ETF avant d'acheter ?", ["Dans la pub du courtier", "Sur la fiche produit ou le DICI", "En devinant", "Nulle part"], "Sur la fiche produit ou le DICI", "Fiche produit et DICI indiquent les frais. Toujours vérifier avant d'acheter.", "Fiche produit / DICI : les frais y figurent."),
            ],
        ),
    ],
}

# ---------- Chapitre 8 : Arnaques et promesses irréalistes ----------
CHAP8 = {
    "title": "Se protéger : arnaques et promesses irréalistes",
    "description": "Reconnaître les signaux d'alerte (rendements garantis, appels inconnus) et investir uniquement via des acteurs régulés.",
    "order": 8,
    "lessons": [
        lesson(
            "Les promesses irréalistes",
            "Rendement garanti, doublement en quelques mois : pourquoi c'est suspect.",
            1,
            "easy",
            text_blocks_pages([
                ("« Rendement garanti 15 % » et autres mirages", "Si quelqu'un te promet un **rendement garanti** très élevé (10 %, 15 % par an) ou de **doubler ton argent en quelques mois**, c'est soit une arnaque, soit un placement extrêmement risqué. Les vrais investissements ont du risque et des rendements variables. En bourse, sur le long terme, 6–8 % par an en moyenne est déjà un bon ordre de grandeur – et ce n'est jamais « garanti ». Plus la promesse est belle, plus il faut se méfier."),
                ("Les bons ordres de grandeur", "Un **livret** : 2–3 %. Un **fonds euros** : 1–3 %. Un **ETF actions** sur 10–20 ans : historiquement 6–8 % par an en moyenne, avec des années à -20 % ou +15 %. Si on te propose mieux que ça « sans risque » ou « garanti », pose des questions. Vérifie que l'interlocuteur et le produit sont **régulés** (banque, courtier agréé, OPCVM connus)."),
            ]),
            [
                mc("« Rendement garanti 15 % par an » est en général :", ["Une bonne opportunité", "Un signal d'alerte : promesse irréaliste ou arnaque", "La norme en bourse", "Recommandé par l'État"], "Un signal d'alerte : promesse irréaliste ou arnaque", "Les vrais placements ont du risque et des rendements variables. Les promesses trop belles cachent souvent une arnaque.", "Promesse irréaliste ou arnaque. Les vrais rendements ne sont pas « garantis » à ce niveau."),
                drag_drop(
                    "Si on te propose un rendement _____ « sans risque » ou « garanti », _____ que l'interlocuteur et le produit sont _____.",
                    ["élevé", "vérifie", "régulés", "faible", "oublie", "interdits"],
                    "Si on te propose un rendement élevé « sans risque » ou « garanti », vérifie que l'interlocuteur et le produit sont régulés.",
                    "Parfait ! Élevé + vérifie + régulés. Toujours vérifier la régulation (AMF, ACPR) en cas de promesse trop belle.",
                    "La bonne phrase : rendement élevé, vérifie, régulés. En cas de promesse belle, vérifier que l'acteur est agréé.",
                ),
                tf("Historiquement, un ETF actions sur 10–20 ans peut avoir une moyenne de 6–8 % par an, avec des années de forte hausse ou baisse.", "Vrai", "C'est un ordre de grandeur réaliste. Ce n'est jamais garanti.", "Vrai : 6–8 % par an en moyenne sur le long terme, avec de la volatilité."),
                mc("Que faire si on te propose de doubler ton argent en 6 mois ?", ["Investir tout de suite", "Se méfier et vérifier que l'interlocuteur et le produit sont régulés", "En parler à un ami", "Emprunter pour investir plus"], "Se méfier et vérifier que l'interlocuteur et le produit sont régulés", "Se méfier. Vérifier banque, courtier agréé, produit connu (OPCVM, etc.).", "Se méfier. Vérifier que tout est régulé."),
            ],
        ),
        lesson(
            "Arnaques courantes et comment s'en protéger",
            "Appels inconnus, virements vers des comptes inconnus, faux conseillers.",
            2,
            "easy",
            text_blocks_pages([
                ("Les arnaques typiques", "**Appels ou emails inconnus** te proposant un placement « exclusif » ou « réservé à quelques-uns ». **Sites ou apps** qui demandent un virement vers un compte inconnu. **Faux conseillers** qui te poussent à investir vite (« l'offre expire »). La règle : **n'investis que via des acteurs régulés** (banques, courtiers connus comme Boursorama, Fortuneo, Linxea, etc.), et **ne envoie jamais d'argent** à quelqu'un qui te contacte à l'improviste."),
                ("Concrètement", "Ouvre ton PEA ou ton assurance-vie **toi-même** sur le site officiel du courtier ou de la banque. Ne clique pas sur des liens envoyés par SMS ou email inconnus. Ne donne jamais tes identifiants bancaires ou de compte à quelqu'un qui te contacte. Si tu as un doute, vérifie sur le site officiel de l'AMF (Autorité des Marchés Financiers) ou de l'ACPR (banques/assurance) que l'acteur est bien agréé."),
            ]),
            [
                mc("Un inconnu t'appelle pour te proposer un « placement exclusif ». Que faire ?", ["Lui envoyer de l'argent", "Refuser poliment et ne jamais envoyer d'argent à quelqu'un qui te contacte à l'improviste", "Lui donner tes identifiants", "Investir la moitié pour tester"], "Refuser poliment et ne jamais envoyer d'argent à quelqu'un qui te contacte à l'improviste", "Les vrais conseillers ne t'appellent pas comme ça. Ne envoie jamais d'argent à un inconnu.", "Refuser. Ne jamais envoyer d'argent à quelqu'un qui te contacte à l'improviste."),
                tf("Investir uniquement via des acteurs régulés (banques, courtiers connus) limite le risque d'arnaque.", "Vrai", "Les acteurs régulés sont contrôlés. Les arnaques passent souvent par des inconnus ou des plateformes douteuses.", "Vrai : banques et courtiers régulés = plus de sécurité."),
                mc("Où vérifier qu'un courtier ou une banque est bien agréé ?", ["Sur un forum anonyme", "Sur le site officiel de l'AMF ou de l'ACPR", "Nulle part", "Sur les réseaux sociaux"], "Sur le site officiel de l'AMF ou de l'ACPR", "L'AMF (marchés) et l'ACPR (banques/assurance) listent les acteurs agréés. Utile en cas de doute.", "AMF (marchés), ACPR (banques/assurance) : vérifier qu'un acteur est agréé."),
                tf("Il faut ouvrir son PEA ou son assurance-vie soi-même sur le site officiel du courtier, pas via un lien envoyé par un inconnu.", "Vrai", "Ouvre toujours toi-même sur le site officiel. Ne clique pas sur des liens reçus par SMS ou email inconnus.", "Vrai : ouvrir soi-même sur le site officiel. Pas de lien inconnu."),
            ],
        ),
    ],
}

# ---------- Chapitre 9 : Retraite et long terme (système français en bref, pas refaire le PER en détail – déjà ch3) ----------
CHAP9 = {
    "title": "Retraite et long terme : où j'en suis ?",
    "description": "Comprendre en bref le système de retraite français et le rôle de l'épargne long terme (sans refaire le PER en détail, déjà vu en ch3).",
    "order": 9,
    "lessons": [
        lesson(
            "Le système de retraite en France : les bases",
            "Répartition, âge légal, et pourquoi l'épargne personnelle complète.",
            1,
            "easy",
            text_blocks_pages([
                ("Répartition et âge légal", "En France, la retraite **obligatoire** repose sur la **répartition** : les actifs cotisent pour payer les pensions des retraités. L'**âge légal** de départ (sans décote) évolue (autour de 64 ans selon ta génération). Les montants des pensions dépendent de ta carrière (années de cotisation, salaires). Beaucoup de jeunes auront une pension plus faible que le dernier salaire : d'où l'importance de **compléter** avec une épargne personnelle (PER, PEA, assurance-vie)."),
                ("Pourquoi épargner pour la retraite dès maintenant", "Plus tu commences tôt, plus ton épargne a le temps de fructifier (intérêts composés). Le **PER** (déjà vu en « Introduction aux investissements ») permet une déduction fiscale et une capitalisation sur des décennies. Le **PEA** et l'**assurance-vie** peuvent aussi servir à un objectif retraite si tu gardes l'argent jusqu'à la retraite. L'idée : ne pas compter uniquement sur la retraite obligatoire."),
            ]),
            [
                drag_drop(
                    "Plus ton _____ est long avant la retraite, plus tu peux mettre une part _____ en actions et ETF.",
                    ["horizon", "importante", "salaire", "faible", "âge", "petite"],
                    "Plus ton horizon est long avant la retraite, plus tu peux mettre une part importante en actions et ETF.",
                    "Parfait ! Horizon long + part importante en actions/ETF. Le temps lisse la volatilité.",
                    "La bonne phrase : horizon long, part importante en actions/ETF. Plus l'horizon est court, plus on sécurise (fonds euros, livret).",
                ),
                mc("En France, la retraite obligatoire repose principalement sur :", ["L'épargne personnelle", "La répartition (les actifs cotisent pour les retraités)", "Les cryptomonnaies", "Un compte à l'étranger"], "La répartition (les actifs cotisent pour les retraités)", "Les cotisations des actifs financent les pensions. D'où l'importance de compléter avec une épargne personnelle.", "Répartition : les actifs paient les pensions des retraités."),
                tf("Beaucoup de jeunes auront une pension plus faible que leur dernier salaire ; compléter avec une épargne personnelle est important.", "Vrai", "D'où l'intérêt du PER, du PEA et de l'assurance-vie pour un objectif retraite.", "Vrai : la retraite obligatoire ne suffira pas pour tous. Épargne personnelle = complément."),
                mc("Pourquoi commencer à épargner pour la retraite tôt ?", ["Pour payer moins d'impôts tout de suite", "Pour laisser le temps à l'épargne de fructifier (intérêts composés)", "Pour éviter la répartition", "Pour avoir une pension plus haute"], "Pour laisser le temps à l'épargne de fructifier (intérêts composés)", "Plus tu commences tôt, plus la capitalisation travaille pour toi.", "Le temps (intérêts composés) travaille pour toi si tu commences tôt."),
            ],
        ),
        lesson(
            "Horizon long : adapter sa stratégie",
            "Plus l'horizon est long, plus on peut accepter de volatilité (actions/ETF).",
            2,
            "easy",
            text_blocks_pages([
                ("Horizon et répartition", "Plus ton **horizon** est long (ex. 25 ans avant la retraite), plus tu peux mettre une part importante en **actions/ETF** : le temps lisse la volatilité. Plus tu te rapproches de la retraite (ex. 5 ans), plus il peut être prudent d'augmenter la part en **fonds euros** ou livrets pour sécuriser l'épargne dont tu auras besoin bientôt. C'est le principe d'**allocation selon l'âge** (déjà évoqué dans « Les différentes classes d'actifs »)."),
                ("Pas de formule magique", "Chacun a un âge, un objectif et une tolérance au risque différents. L'idée est d'avoir une stratégie cohérente : long terme = plus d'actions/ETF, court terme = plus de sécurisé. Tu peux revoir ça une fois par an (ex. à l'anniversaire du compte ou au 1er janvier) sans réagir à chaque mouvement du marché."),
            ]),
            [
                mc("Si ton horizon est long (ex. 25 ans avant la retraite), tu peux en général :", ["Tout mettre en livret", "Mettre une part plus importante en actions/ETF", "Ne rien épargner", "Tout mettre en crypto"], "Mettre une part plus importante en actions/ETF", "Le temps lisse la volatilité. Une part actions/ETF plus importante est souvent adaptée.", "Long terme = plus de marge pour la volatilité, donc plus d'actions/ETF possible."),
                tf("Plus tu te rapproches de la retraite (ex. 5 ans), augmenter la part en fonds euros ou livrets peut être prudent.", "Vrai", "Court terme = moins de temps pour absorber une baisse. Sécuriser une part limite le risque au moment du retrait.", "Vrai : court terme = plus de sécurité (fonds euros, livret)."),
                mc("Qu'est-ce qui doit influencer ta répartition (actions vs fonds euros) pour la retraite ?", ["Uniquement l'âge", "Ton horizon, ton objectif et ta tolérance au risque", "Le jour de la semaine", "La météo"], "Ton horizon, ton objectif et ta tolérance au risque", "Horizon, objectif et tolérance au risque déterminent la répartition. Pas de règle unique.", "Horizon, objectif, tolérance au risque. Chacun adapte."),
            ],
        ),
    ],
}

# ---------- Chapitre 10 : Et après ? (par où continuer, pas récap des 5 piliers) ----------
CHAP10 = {
    "title": "Et après ? Consolider et aller plus loin",
    "description": "Par où continuer ton apprentissage : Bourse, immobilier, fiscalité, sans répéter tout ce qui a été vu dans les chapitres précédents.",
    "order": 10,
    "lessons": [
        lesson(
            "Les prochaines étapes possibles",
            "Bourse, immobilier, fiscalité : quelles sections ou sujets explorer selon tes objectifs.",
            1,
            "easy",
            text_blocks_pages([
                ("Section Bourse", "Si tu veux **approfondir** les actions, les ETF, l'analyse des entreprises ou les stratégies (diversification avancée, dividendes, etc.), une section **Bourse** ou équivalent te permettra d'aller plus loin. Tu as déjà les bases : PEA, ETF, risque/rendement. La suite, c'est affiner selon ton intérêt."),
                ("Immobilier et fiscalité", "Si ton objectif est un **achat immobilier** dans quelques années, renseigne-toi sur l'épargne dédiée (horizon court = plus de fonds euros/livret pour l'apport). Si tu veux **optimiser ta fiscalité** (impôts, prélèvements sociaux, crédits d'impôt), une section **Lois et réglementations** ou **Fiscalité** t'aidera. Tu n'as pas besoin de tout faire : choisis selon tes objectifs."),
            ]),
            [
                mc("Pour approfondir les actions et les ETF, vers quelle section se diriger ?", ["Uniquement Les bases", "Une section Bourse ou équivalent", "Uniquement la crypto", "Nulle part"], "Une section Bourse ou équivalent", "Tu as les bases (PEA, ETF, risque). La section Bourse permet d'approfondir.", "Section Bourse pour aller plus loin sur actions et ETF."),
                tf("Tu dois tout apprendre (Bourse, immobilier, fiscalité) pour bien gérer ton argent.", "Faux", "Les bases suffisent pour démarrer. Tu approfondis selon tes objectifs et ton envie. Rester simple marche très bien.", "Faux : les bases suffisent. Approfondir selon objectifs et envie."),
                mc("Si tu vises un achat immobilier dans quelques années, quoi faire ?", ["Tout mettre en actions", "T'informer sur l'épargne dédiée et sécuriser l'apport (fonds euros, livret si horizon court)", "Ne rien épargner", "Tout dépenser"], "T'informer sur l'épargne dédiée et sécuriser l'apport (fonds euros, livret si horizon court)", "Objectif immo = horizon plus court. Sécuriser l'apport (fonds euros, livret) peut être pertinent.", "Épargne dédiée, apport sécurisé (fonds euros/livret si horizon court)."),
            ],
        ),
        lesson(
            "Rester simple reste gagnant",
            "Beaucoup réussissent avec peu de lignes et de la régularité. Aller plus loin est optionnel.",
            2,
            "easy",
            text_blocks_pages([
                ("La simplicité paie", "Beaucoup de gens réussissent en restant **simples** : épargne de précaution (déjà en place), virement automatique, 1 à 2 ETF dans un PEA ou une assurance-vie, et ils laissent faire 20 ans. Tu n'as pas besoin de 50 lignes ni de trader. Ce que tu as vu dans « Les bases » suffit pour **80 % du chemin**."),
                ("Aller plus loin si tu veux", "Si tu aimes ça, tu peux approfondir : analyser des entreprises, diversifier par secteur ou zone, optimiser la fiscalité, préparer un achat immobilier. Mais ce n'est **pas obligatoire**. L'essentiel est déjà là : épargner régulièrement, frais bas, rester investi long terme, ne pas vendre en panique."),
            ]),
            [
                mc("Beaucoup de gens réussissent avec :", ["50 lignes et du trading quotidien", "Épargne de précaution + virement auto + 1 à 2 ETF, en laissant faire 20 ans", "Un seul livret", "Rien"], "Épargne de précaution + virement auto + 1 à 2 ETF, en laissant faire 20 ans", "La simplicité et la régularité suffisent pour la plupart.", "Simplicité : précaution + virement auto + 1–2 ETF, long terme."),
                tf("Aller plus loin (Bourse avancée, fiscalité, immobilier) est obligatoire pour bien gérer son argent.", "Faux", "Les bases suffisent pour 80 % du chemin. Aller plus loin est optionnel selon ton intérêt.", "Faux : les bases suffisent. Le reste est optionnel."),
                mc("Quel est l'essentiel à retenir pour la suite ?", ["Trader tous les jours", "Épargner régulièrement, frais bas, rester investi long terme, ne pas vendre en panique", "Acheter 100 actions différentes", "Tout mettre en crypto"], "Épargner régulièrement, frais bas, rester investi long terme, ne pas vendre en panique", "C'est le cœur de ce que tu as vu. Le reste en découle.", "Régularité, frais bas, long terme, pas de vente en panique."),
            ],
        ),
    ],
}


def main():
    chapters = [CHAP4, CHAP5, CHAP6, CHAP7, CHAP8, CHAP9, CHAP10]
    out_data = {"chapters": chapters}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Généré : {OUT}")
    print(f"   {len(chapters)} chapitres (ordres 4 à 10), {sum(len(c['lessons']) for c in chapters)} leçons.")
    print("   Contenu conçu sans doublon avec ch1–ch3 et anciens ch4–ch5 (voir script fetch-les-bases-content.py).")


if __name__ == "__main__":
    main()
