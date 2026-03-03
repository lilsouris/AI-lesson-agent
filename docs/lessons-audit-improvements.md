Lessons audit – content gaps and improvement plan
=================================================

This document lists the main content issues detected in the current lessons, along with concrete suggestions for what to add or adjust. It is designed so that future scripts can systematically apply these changes via the Strapi API.

Scope
-----

The checks below are based on:

- `output/strapi-lessons-full.json` – 7 existing lessons of the chapter **« Introduction aux investissement »** (full text + quiz blocks).  
  For each lesson we inspected:
  - Number of text blocks vs quiz blocks.
  - Presence of quiz blocks with `options: null` or `explanationcorrect / explanationfalse: null`.
- Generated JSONs:
  - `output/les-bases-chapitres-4-a-10.json` (nouveaux chapitres 4–10 de « Les bases » – 7 chapitres, 16 leçons).
  - `output/lois-reglementations-generated.json` (section « Lois et réglementations » – 2 chapitres, 9 leçons).
  - `output/introduction-investissements-missing.json` (2 leçons supplémentaires proposées pour « Introduction aux investissement »).

High-level conclusion:

- **Les bases – chapitres 4–10**: toutes les leçons ont du texte structuré et plusieurs quiz complets (MCQ, Vrai/Faux, matching, drag-order, drag-drop). Aucun bloc incomplet détecté.
- **Lois et réglementations**: toutes les leçons ont des quiz complets au format cible. Pas de `options: null` ni d’explications manquantes.
- **Introduction aux investissement (7 leçons historiques dans Strapi)**: plusieurs leçons ont peu ou pas de quiz, et plusieurs quiz-blocs sont incomplets (options et explications nulles). C’est là que se concentrent les actions prioritaires.

The rest of this document focuses on the **« Introduction aux investissement »** chapter.

Introduction aux investissement – detailed issues
------------------------------------------------

Source: `output/strapi-lessons-full.json` (7 lessons already in Strapi).

For chaque leçon ci-dessous:

- **Issue**: description du problème constaté.
- **What to change/add**: suggestions concrètes de contenu à ajouter ou à remplacer (niveaux de détail suffisants pour les implémenter ensuite en quiz-blocks).

### 1. « Comprendre le risque et le rendement » (order 2)

**Issue**

- Leçon avec **2 text-blocks** (explication du couple risque/rendement, exemples Livret A / obligations / actions / immobilier).
- **Aucun quiz-block** (`quizBlocks_count: 0`).

**What to change/add**

Ajouter au moins **4 à 6 quiz** couvrant:

1. **Règle générale risque/rendement**  
   - Type: multiple-choice.  
   - Question suggérée: « En général, plus le rendement potentiel est élevé : »  
   - Options:  
     - « Plus le risque est faible »  
     - « Plus le risque est élevé » (bonne réponse)  
     - « Le risque ne change pas »  
     - « Le placement est garanti par l’État »  
   - Explications: rappeler que rendement et risque vont ensemble, et que le Livret A est faible risque / faible rendement tandis que les actions sont haut risque / haut rendement potentiel.

2. **Classement des placements par risque**  
   - Type: drag-order.  
   - Question: « Classe ces placements du moins risqué au plus risqué : »  
   - Items: Livret A, Obligations d’État, ETF actions monde, Crypto / action spéculative.  
   - Ordre correct: Livret A → Obligations d’État → ETF actions monde → Crypto / action spéculative.

3. **Horizon de temps vs niveau de risque**  
   - Type: true-false.  
   - Exemple: « Pour un projet à 2 ans, il est raisonnable d’investir 100 % en actions. » → Correct: Faux.  
   - Explication: pour un horizon court, privilégier le sans risque (livrets) plutôt que la bourse.

4. **Diversification et risque global**  
   - Type: multiple-choice.  
   - Question: « Que permet la diversification (plusieurs classes d’actifs) ? »  
   - Bonne réponse: « Réduire le risque global sans renoncer à tout rendement. »

### 2. « Les différentes classes d’actifs » (order 3)

**Issue**

- Leçon avec **3 text-blocks** et **2 quiz-blocks existants**, mais les 2 quiz suivants sont incomplets:
  - id 285 – « Comment évolue l'allocation avec l'âge ? » (`options: null`, explications nulles).
  - id 286 – « match la repartition d'actif avec l'age » (`options: null`, explications nulles).

**What to change/add**

Remplacer ces 2 quiz-blocs par des versions complètes:

1. **Allocation qui évolue avec l’âge**  
   - Type: multiple-choice.  
   - Question: « Comment l’allocation d’actifs doit-elle en général évoluer avec l’âge ? »  
   - Options:  
     - « Plus tu vieillis, plus tu peux prendre de risque »  
     - « Plus tu vieillis, plus tu réduis la part risquée (actions) au profit de supports plus sûrs » (bonne réponse)  
     - « Elle ne doit jamais changer »  
     - « Tout doit être en crypto avant la retraite »  
   - Explication: avec l’âge, horizon plus court → part plus importante en supports moins volatils.

2. **Matching âge / répartition d’actifs**  
   - Type: matching.  
   - Question: « Associe âge et répartition d’actifs typique (ordre de grandeur) : »  
   - Propositions (côté A):  
     - A. 25 ans  
     - B. 40 ans  
     - C. 60 ans  
   - Propositions (côté 1,2,3):  
     - 1. 80 % actions / 20 % oblig / cash  
     - 2. 60 % actions / 40 % oblig / cash  
     - 3. 30 % actions / 70 % oblig / cash  
   - CorrectAnswer: « A → 1, B → 2, C → 3 ».  
   - Explications: insister sur le fait que ce sont des ordres de grandeur, pas une règle absolue.

### 3. « Le PEA (Plan d’Épargne en Actions) » (order 4)

**Issue**

- Leçon avec 4 text-blocks et 3 quiz-blocks valides, mais **3 quiz-blocs supplémentaires incomplets**:
  - id 287 – « Après 5 ans, quelle est la fiscalité sur les plus-values ? » (pas d’options ni d’explications).
  - id 288 – « Que se passe-t-il si on sort avant 5 ans ? » (pas d’options ni d’explications).
  - id 289 – « Quel est le plafond du PEA ? » (pas d’options ni d’explications).

**What to change/add**

Pour chacun, remplacer par un quiz complet:

1. **Fiscalité après 5 ans**  
   - Type: multiple-choice.  
   - Question: « Après 5 ans de détention, comment sont imposées les plus-values du PEA ? »  
   - Options suggérées:  
     - « Flat tax 30 % (impôt + prélèvements sociaux) comme un compte-titres »  
     - « Exonération d’impôt sur le revenu, seuls les prélèvements sociaux restent dus » (bonne réponse)  
     - « Exonération totale d’impôts et de prélèvements sociaux »  
     - « Prélevées directement par la banque sans détail ».

2. **Sortie avant 5 ans**  
   - Type: multiple-choice.  
   - Question: « Que se passe-t-il en cas de retrait avant 5 ans sur un PEA ? »  
   - Bonne réponse à mettre en avant: clôture du plan + fiscalité moins favorable (perte de l’avantage fiscal).

3. **Plafond du PEA**  
   - Type: multiple-choice ou true-false.  
   - Exemple: « Le plafond de versement du PEA classique est d’environ 150 000€. » → Vrai.  
   - Explication: préciser qu’il s’agit du plafond de versement (hors gains) et rappeler l’existence du PEA-PME.

### 4. « L’assurance-vie moderne » (order 5)

**Issue**

- Leçon avec 3 text-blocks et 3 quiz-blocks existants, mais **les 3 quiz sont incomplets**:
  - id 290 – « D'aprés le cours, il faut éviter ... » (options/explications nulles).
  - id 291 – « Quel est l'avantage de l'assurance-vie par rapport au PEA ? » (options/explications nulles).
  - id 292 – « la fiscalité de l'assurance-vie après 8 ans est de 17,2% » (true-false sans options/explications).

**What to change/add**

Remplacer par 3 quiz complets:

1. **Contrats à éviter**  
   - Type: drag-drop ou multiple-choice.  
   - Question: « D’après le cours, il faut éviter en priorité : »  
   - Bonne réponse: « Les assurances-vie traditionnelles des banques avec frais d’entrée et de gestion élevés ».  
   - Ajouter 2–3 options incorrectes pour contraster (ex: « Les contrats en ligne sans frais », etc.).

2. **Avantage clé vs PEA**  
   - Type: multiple-choice.  
   - Question: « Quel est le principal avantage de l’assurance-vie par rapport au PEA ? »  
   - Bonne réponse: « Accéder aux marchés mondiaux (ETF monde, fonds internationaux) et à une enveloppe de transmission, pas limitée à l’Europe ».  
   - Autres options: fiscalité immédiate plus avantageuse (faux), garantie en capital totale (faux), etc.

3. **Fiscalité après 8 ans**  
   - Type: true-false.  
   - Question reformulée proprement: « Après 8 ans, la fiscalité de l’assurance-vie peut être réduite (abattement annuel + taux réduit), mais n’est pas automatiquement de 17,2 %. »  
   - Bonne réponse: Faux pour l’affirmation « la fiscalité est de 17,2 % dans tous les cas ».  
   - Explication: rappeler le mécanisme abattement + choix entre PFU et barème, et les 17,2 % correspondant aux seuls prélèvements sociaux.

### 5. « Les biais cognitifs de l’investisseur » (order 6)

**Issue**

- Leçon avec **2 text-blocks** qui détaillent plusieurs biais (confirmation, aversion aux pertes, effet de troupeau, ancrage, etc.).
- **Aucun quiz-block** (`quizBlocks_count: 0`).

**What to change/add**

Ajouter au moins **4–6 quiz** permettant de:

1. **Identifier chaque biais**  
   - Type: matching.  
   - Associer le nom du biais à sa description (ex: biais de confirmation, effet de troupeau, aversion aux pertes, biais d’ancrage).

2. **Cas pratiques**  
   - Type: multiple-choice.  
   - Présenter une situation (ex: « Tu refuses de vendre une action en forte baisse car tu veux retrouver ton prix d’achat initial ») et demander de quel biais il s’agit (ancrage).

3. **Impact sur les décisions d’investissement**  
   - Type: true-false.  
   - Exemple: « L’aversion aux pertes peut pousser un investisseur à vendre trop vite ses positions gagnantes. » → Vrai, avec explication.

4. **Stratégies pour limiter les biais**  
   - Type: multiple-choice.  
   - Question sur les solutions: avoir un plan écrit, automatiser les versements, vérifier son portefeuille moins souvent, etc.

### 6. « Le PER (Plan Épargne Retraite) » (order 7)

**Issue**

- Leçon avec **2 text-blocks** bien rédigés expliquant:
  - Avantages fiscaux à l’entrée (déduction, effet de levier fiscal).
  - Capitalisation long terme, blocage jusqu’à la retraite, cas de sortie anticipée.
- **Aucun quiz-block** (`quizBlocks_count: 0`).

**What to change/add**

Ajouter au moins **4–6 quiz** couvrant:

1. **Principe de la déduction fiscale**  
   - Type: true-false ou multiple-choice.  
   - Exemple: « Pour un contribuable imposé à 30 %, verser 1000 € sur un PER lui coûte réellement 700 €. » → Vrai, avec explication.

2. **Blocage et cas de sortie anticipée**  
   - Type: multiple-choice.  
   - Question: « Parmi les cas suivants, lesquels permettent une sortie anticipée du PER ? » (résidence principale, invalidité, surendettement, etc.).

3. **Comparaison PER vs PEA / assurance-vie**  
   - Type: multiple-choice.  
   - Interroger sur quand privilégier le PER (si imposé à 30 % ou plus, objectif retraite long terme) vs d’autres enveloppes.

4. **Risques et inconvénients**  
   - Type: true-false.  
   - Exemple: « Le principal inconvénient du PER est le blocage jusqu’à la retraite (sauf exceptions) » → Vrai.

Other sections – quick check
----------------------------

Pour mémoire:

- Les nouveaux chapitres 4–10 de **« Les bases »** ont tous:
  - Au moins 2 pages de texte par leçon.
  - Au moins 3–4 quiz par leçon, déjà structurés avec les bons types (MCQ, TF, matching, drag-order, drag-drop).
  - Aucune option ou explication nulle détectée.

- La section **« Lois et réglementations »** (2 chapitres, 9 leçons) présente:
  - Texte structuré et riche pour chaque leçon.
  - 3–6 quiz par leçon, complets et alignés avec le contenu.

À ce stade, les **actions prioritaires** pour améliorer la qualité pédagogique globale sont donc:

1. **Compléter et corriger les quiz du chapitre « Introduction aux investissement »** selon les suggestions détaillées ci-dessus.
2. **Ajouter les 2 leçons supplémentaires** prévues dans `introduction-investissements-missing.json` (portefeuille de départ + plan d’investissement régulier), une fois validées, pour renforcer la partie très pratique de ce chapitre.

Une fois ces ajustements faits, l’ensemble des sections auditées aura:

- Des leçons toutes pourvues de quiz complets et cohérents avec le texte.
- Une densité de questions suffisante (≈ 4–6 par leçon) pour un bon engagement utilisateur.
- Des formats de quiz variés, déjà compatibles avec les contraintes Strapi (Rich Text, matching en un bloc, drag-order, drag-drop).

