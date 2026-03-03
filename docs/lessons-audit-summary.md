Lessons audit – course content overview
======================================

This document summarizes the current state of the course lessons as represented in the local JSON snapshots and generation scripts. It is meant as a reference before future automated updates via the Strapi API.

Scope and data sources
----------------------

The audit is based on the following files in the repository:

- `output/les-bases-existing-content.json`  
  Export of the existing Strapi section **« Les bases »** (before adding the new chapters 4–10). Contains:
  - **5 chapitres**, **22 leçons** (titles, brief text extracts, and quiz question headings).

- `output/les-bases-chapitres-4-a-10.json`  
  Generated content for the new chapters 4–10 of **« Les bases »**. Contains:
  - **7 chapitres**, **16 leçons**, each with text blocks and fully specified quiz blocks (MCQ, Vrai/Faux, matching, drag-order, drag-drop).

- `output/lois-reglementations-generated.json`  
  Generated content for the section **« Lois et réglementations »**. Contains:
  - **2 chapitres**, **9 leçons**, each with text blocks and quizzes (MCQ, Vrai/Faux, matching).

- `output/strapi-lessons-full.json`  
  Snapshot of the 7 leçons of the chapter **« Introduction aux investissement »** currently présentes dans Strapi, avec leur contenu complet (text-blocks et quiz-blocks).  
  - **7 leçons** totales, dont plusieurs avec quizz incomplets (options / explications nulles) ou sans quiz.

- `output/introduction-investissements-missing.json`  
  Contenu généré pour compléter le chapitre **« Introduction aux investissement »** avec 2 nouvelles leçons pratiques, pas encore poussées dans Strapi:
  - **1 chapitre**, **2 leçons** supplémentaires proposées.

In addition, the following scripts are relevant to how lessons are generated, normalised and importés dans Strapi:

- `scripts/build-les-bases-chapitres-4-a-10.py` – construit le JSON des nouveaux chapitres 4–10 de « Les bases ».
- `scripts/fetch-les-bases-content.py` – exporte depuis Strapi le contenu actuel de « Les bases » pour éviter les doublons.
- `scripts/import-les-bases-chapitres-4-a-10-strapi.py` – supprime les anciens chapitres 4–5 de « Les bases » et importe les nouveaux chapitres 4–10 avec les leçons.
- `scripts/build-lois-reglementations-json.py` – génère le JSON de la section « Lois et réglementations ».
- `scripts/fix-lois-reglementations-lessons.py` – corrige les text-blocks et quiz de cette section avant / après import.
- `python-agent/scripts-generate-chapters-and-lessons-agent.py` – agent générique pour normaliser le format Strapi (Rich Text, matching en un bloc, drag-order / drag-drop, explications non nulles) et créer chapitres + leçons via l’API.
- `scripts/fix-quiz-blocks-introduction-investissement.py` et `scripts/update-introduction-investissement-lessons.py` – scripts ciblés sur le chapitre « Introduction aux investissement » pour corriger/compléter ses quiz à partir de `strapi-lessons-full.json`.

Section « Les bases »
---------------------

### 1. Contenu existant (avant nouveaux chapitres 4–10)

Source: `les-bases-existing-content.json`

- **Chapitre 1 – Fondamentaux de l'argent et de l'épargne**  
  Leçons principales:
  - « L’inflation, ton ennemi silencieux »
  - « Ton matelas de sécurité »
  - « Ton premier salaire : que faire ? »
  - « Tracking et optimisation »
  - « Objectifs financiers et planification »
  - « La valeur du temps : intérêts simples vs composés »
  - « La psychologie de l’argent »
  - Chaque leçon a 2–3 pages de texte + plusieurs quiz (types variés: drag-drop, matching, etc.).

- **Chapitre 2 – Préparer sa stratégie d’investissement**  
  Leçons:
  - « Épargne de précaution : où ? »
  - « L’indépendance financière (mouvement FIRE) »
  - « Choisir sa banque : traditionnelle ou en ligne ? »

- **Chapitre 3 – Introduction aux investissement**  
  Leçons:
  - « Pourquoi épargner quand on est jeune ? »
  - « Comprendre le risque et le rendement »
  - « Les différentes classes d’actifs »
  - « Le PEA (Plan d’Épargne en Actions) »
  - « L’assurance-vie moderne »
  - « Les biais cognitifs de l’investisseur »
  - « Le PER (Plan Épargne Retraite) »
  - L’export Strapi montre pour chaque leçon plusieurs pages de texte. Les quiz sont complets pour certaines leçons, mais incomplets ou absents pour d’autres (voir le fichier d’améliorations).

Au total, la section « Les bases » comporte aujourd’hui **5 chapitres et 22 leçons** côté contenu existant.

### 2. Nouveaux chapitres 4–10 (conçus pour remplacer les anciens chapitres 4 et 5)

Source: `les-bases-chapitres-4-a-10.json` + import via `scripts/import-les-bases-chapitres-4-a-10-strapi.py`

- **Chapitre 4 – Les frais en pratique**  
  - 3 leçons: où trouver les frais (DICI, TER), comparer courtiers / contrats, ordres de grandeur acceptables.  
  - Quiz variés: multiple-choice, vrai/faux, matching, drag-drop.

- **Chapitre 5 – Ouvrir et utiliser son PEA ou son assurance-vie**  
  - 3 leçons: documents et délais, premier virement et premier ordre, suivi sans obsession.  
  - Inclut un quiz de type **drag-order** sur les étapes d’ouverture.

- **Chapitre 6 – Quand les marchés chutent**  
  - 2 leçons: histoire des krachs, réactions concrètes lors d’une grosse baisse.  
  - Inclut un quiz **drag-order** sur les réactions à classer du pire au moins pire.

- **Chapitre 7 – Choisir ses premiers ETF**  
  - 2 leçons: ETF monde / zone, frais et simplicité.  
  - Inclut un quiz **drag-order** sur les étapes pour choisir et acheter un ETF.

- **Chapitre 8 – Se protéger : arnaques et promesses irréalistes**  
  - 2 leçons: promesses irréalistes, arnaques courantes et signaux d’alerte.  
  - Inclut au moins un quiz **drag-drop**.

- **Chapitre 9 – Retraite et long terme : où j’en suis ?**  
  - 2 leçons: système de retraite français, adapter sa stratégie à l’horizon.  
  - Inclut un quiz **drag-drop** orienté horizon / part en actions.

- **Chapitre 10 – Et après ? Consolider et aller plus loin**  
  - 2 leçons: prochaines étapes (Bourse, immobilier, fiscalité), garder une approche simple.  
  - Quiz de consolidation et d’orientation vers d’autres sections.

Ces 7 nouveaux chapitres représentent **16 leçons** supplémentaires, importées dans Strapi avec:

- Texte structuré en **pages « Page 1 », « Page 2 », ...**, titre pédagogique en tête de contenu (au format Rich Text).
- Quiz normalisés au format attendu par Strapi (options en Rich Text, matching en un seul bloc, drag-order et drag-drop avec `correctAnswer` cohérent).
- Chaînage de prérequis: **ch4 → ch3**, puis ch5 → ch4, ..., ch10 → ch9.

Section « Lois et réglementations »
----------------------------------

Source: `lois-reglementations-generated.json` + `scripts/fix-lois-reglementations-lessons.py`

- **Chapitre 1 – Les bases de la fiscalité française**  
  - Leçons: impôt sur le revenu, tranches et quotient familial, revenus imposables, déclarations.  
  - Texte structuré en plusieurs blocs, mise en avant des règles clés et points de vigilance.  
  - Quiz: principalement multiple-choice et vrai/faux, parfois matching.

- **Chapitre 2 – Fiscalité de l’épargne et de l’investissement**  
  - Leçons: fiscalité livret / PEA / assurance-vie, prélèvements sociaux, flat tax, cas pratiques.  
  - Quiz: vérification de compréhension des taux, régimes fiscaux et cas de sortie.

Au total, cette section représente **2 chapitres et 9 leçons** dans le JSON généré, avec un format Strapi-compatible (text-blocks + quiz-blocks).

Chapitre « Introduction aux investissement »
-------------------------------------------

Sources: `les-bases-existing-content.json`, `strapi-lessons-full.json`, `introduction-investissements-missing.json`

- **État actuel dans Strapi (7 leçons)** – via `strapi-lessons-full.json`:
  - « Pourquoi épargner quand on est jeune ? » – texte + quiz complets.
  - « Comprendre le risque et le rendement » – texte présent, **0 quiz**.
  - « Les différentes classes d’actifs » – texte présent, **quelques quiz valides mais plusieurs blocs quiz avec options / explications nulles**.
  - « Le PEA (Plan d’Épargne en Actions) » – texte présent, quiz existants + **plusieurs quiz-blocs incomplets (options / explications nulles)**.
  - « L’assurance-vie moderne » – texte présent, **3 quiz-blocs incomplets** (options / explications nulles).
  - « Les biais cognitifs de l’investisseur » – texte présent, **0 quiz**.
  - « Le PER (Plan Épargne Retraite) » – texte présent, **0 quiz**.

- **Compléments prévus (non encore en production)** – via `introduction-investissements-missing.json`:
  - Leçon 8: « Construire ton premier portefeuille d’investissement » – texte + quiz complets, centrés sur profil investisseur, structure simple et erreurs à éviter.
  - Leçon 9: « Mettre en place un plan d’investissement régulier » – texte + quiz complets, centrés sur DCA, automatisation et discipline.

Scripts comme `scripts/update-introduction-investissement-lessons.py` sont prévus pour:

- Charger `strapi-lessons-full.json`.
- Compléter les leçons existantes de ce chapitre avec des quiz supplémentaires (au moins 6 par leçon).
- Pousser ces compléments dans Strapi (via PUT sur chaque `documentId`).

Résumé global
-------------

- La section **« Les bases »** est maintenant structurée en **10 chapitres**:
  - 1–3: existants, déjà en production dans Strapi (22 leçons).
  - 4–10: nouveaux, générés et importés (16 leçons).
- La section **« Lois et réglementations »** dispose de **2 chapitres, 9 leçons** au format homogène.
- Le chapitre **« Introduction aux investissement »** a **7 leçons en production**, dont plusieurs avec quiz incomplets ou manquants, et **2 leçons supplémentaires** prêtes à être ajoutées.

Les prochains ajustements se concentreront donc surtout sur:

- Compléter / corriger les quiz du chapitre « Introduction aux investissement ».
- Éventuellement enrichir encore certains quiz existants (densité / variété) si besoin, mais la structure générale (text-blocks + quiz-blocks) est en place pour toutes les sections.

