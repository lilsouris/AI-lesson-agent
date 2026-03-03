Lessons fix plan – live Strapi snapshot
======================================

This file describes what I propose to change in the **current live Strapi lessons**, based on the latest snapshot in `output/strapi-lessons-full.json` (51 lessons fetched via the API), and the issues detected in `output/lessons-issues.json`.

Scope of issues
---------------

The automated audit looked for lessons that either:

- Have **no quiz blocks at all**, or
- Have **quiz blocks with `options`, `explanationcorrect` or `explanationfalse` set to `null`**.

With the current live data, this yields **4 problematic lessons**:

1. Chapter **« L'investissement dans les entreprises »**  
   - Lesson: **« L'investissement dans les startups »** (`documentId: m2rng62xfjrzp174bjvl15vw`)  
   - Text blocks: 2  
   - Quiz blocks: **0**

2. Chapter **« L'immobilier pour les jeunes »**  
   - Lesson: **« SCPI vs immobilier direct »** (`documentId: p1asmgj7n5jlcngdgv5msjzy`)  
   - Text blocks: 2  
   - Quiz blocks: **0**

3. Chapter **« Fiscalité des placements et investissements »**  
   - Lesson: **« Budget et gestion des finances personnelles »** (`documentId: n2vnjpu38vznbj5kfwyvyexe`)  
   - Text blocks: 3  
   - Quiz blocks: 2, **both incomplete** (no options, no explanations).

4. Chapter unknown (no chapter/section linked)  
   - Lesson: **« Les ETF (Exchange Traded Funds) »** (`documentId: ewzcsqnif4z08c40p43or6pl`)  
   - Text blocks: 3  
   - Quiz blocks: 1, **incomplete** (no options, no explanations).

For all other lessons (including « Les bases » and « Lois & réglementations »), the audit did **not** find missing or malformed quiz blocks.

Proposed changes by lesson
--------------------------

Below is the **content-level plan** for what to modify or add. The future fix script will:

- Read the existing `content` for each targeted lesson from Strapi (or from `strapi-lessons-full.json` as baseline).
- Preserve all existing **text-blocks**.
- Replace or append **quiz-blocks** according to the plan below, using the standard Strapi quiz format (Rich Text options + explanations).

### 1. « L'investissement dans les startups » (docId: m2rng62xfjrzp174bjvl15vw)

**Current situation**

- 2 pages de texte:
  - Page 1: introduction à l’investissement dans les startups via equity crowdfunding, potentiel de x10+.
  - Page 2: risques très élevés (90% d’échec), importance de limiter à ~5–10% du portefeuille, diversification sur 20–30 startups, critères d’analyse (équipe, marché, produit, business model).
- **Aucun quiz**.

**What I propose to add**

Ajouter **3 quiz-blocks**:

1. **Compréhension du risque et de la part du portefeuille**  
   - Type: multiple-choice.  
   - Question: « Quelle part de ton portefeuille ce type d’investissement (startups) devrait en général représenter ? »  
   - Options (ordre à préciser dans le script):  
     - « 50–60 % »  
     - « 20–30 % »  
     - « 5–10 % » (bonne réponse)  
     - « 0 % ou 100 % »  
   - Explication correcte: rappeler que l’investissement en startups est ultra-risqué → petite part du portefeuille.  

2. **Diversification en nombre de startups**  
   - Type: multiple-choice.  
   - Question: « Pour lisser le risque, combien de startups environ est-il recommandé de détenir ? »  
   - Options:  
     - « 1 ou 2 »  
     - « 5 »  
     - « 20–30 » (bonne réponse)  
     - « 100 minimum »  
   - Explication: une seule « licorne » peut compenser plusieurs échecs, mais il faut un nombre suffisant de lignes (20–30) pour lisser le risque.

3. **Identifier les bons critères d’analyse**  
   - Type: multiple-choice ou matching.  
   - Variante simple (MCQ):  
     - Question: « Quels critères sont cités dans la leçon pour analyser une startup ? »  
     - Bonne réponse: « Équipe, marché, produit, business model ».  
   - Explication: mettre en avant ces 4 axes et rappeler qu’ils sont plus importants que le “hype”.

### 2. « SCPI vs immobilier direct » (docId: p1asmgj7n5jlcngdgv5msjzy)

**Current situation**

- 2 pages de texte:
  - Page 1: comparaison immobilier direct vs SCPI (capital initial, gestion, risques).
  - Page 2: rendement des SCPI (~4–5 %), frais d’entrée élevés, absence d’effet de levier, intérêt pour les jeunes (ticket d’entrée plus faible, diversification, pas de gestion).
- **Aucun quiz**.

**What I propose to add**

Ajouter **3 quiz-blocks**:

1. **Capital minimum et effet de levier**  
   - Type: multiple-choice.  
   - Question: « Pourquoi l’immobilier direct est-il plus difficile d’accès qu’une SCPI pour un jeune ? »  
   - Bonne réponse: apport important (20–30 %) + gestion lourde, vs SCPI accessibles dès de petits montants gérés par des pros.

2. **Avantage clé des SCPI**  
   - Type: multiple-choice.  
   - Question: « Quel est l’avantage principal d’une SCPI par rapport à l’immobilier locatif direct ? »  
   - Bonne réponse: diversification sur de nombreux biens + absence de gestion quotidienne.

3. **Inconvénients des SCPI**  
   - Type: multiple-choice ou true-false.  
   - Question: « Parmi les propositions suivantes, lequel est un inconvénient des SCPI ? »  
   - Bonne réponse: frais d’entrée élevés (6–10 %) + liquidité plus faible que des titres cotés.

### 3. « Budget et gestion des finances personnelles » (docId: n2vnjpu38vznbj5kfwyvyexe)

**Current situation**

- 3 pages de texte sur la règle **50/30/20** (besoins / envies / épargne) avec exemple concret pour 2000 € nets/mois et cas particuliers (vivre chez ses parents, coût de la vie élevé).  
- 2 quiz-blocks existants, tous deux **incomplets**:
  - id 513 – Question: « Avec un salaire de 2000€ net, combien devrais-tu épargner selon la règle 50/30/20 ? » – `options: null`, explications nulles.
  - id 514 – Question: « Si tu vis chez tes parents, que peux-tu faire ? » – `options: null`, explications nulles.

**What I propose to change**

Remplacer complètement ces **2 quiz-blocks** par des versions complètes:

1. **Application chiffrée de la règle 50/30/20**  
   - Type: multiple-choice (ou drag-drop si l’on veut que l’utilisateur reconstruise 50/30/20).  
   - Question: « Avec un salaire de 2000€ net, quelle répartition correspond à la règle 50/30/20 (besoins/envies/épargne) ? »  
   - Bonne réponse: **1000€ / 600€ / 400€**.  
   - Explication: rappeler le calcul (50 % de 2000, 30 %, 20 %) et l’idée de fixer un montant d’épargne dès le départ.

2. **Cas particulier: vivre chez ses parents**  
   - Type: multiple-choice.  
   - Question: « Si tu vis chez tes parents avec peu de dépenses fixes, que conseille la leçon ? »  
   - Bonne réponse: augmenter la part épargnée (par exemple > 20 %) en profitant de charges faibles, plutôt que tout mettre dans les dépenses plaisir.  
   - Explication: c’est une opportunité pour constituer rapidement un matelas de sécurité et/ou un apport.

Optionnellement, on pourra ajouter **1–2 quiz supplémentaires** pour monter à 4 quiz au total (par exemple: identifier à quelle catégorie appartiennent certaines dépenses, ou ajuster la règle selon le coût de la vie).

### 4. « Les ETF (Exchange Traded Funds) » (docId: ewzcsqnif4z08c40p43or6pl)

**Current situation**

- 3 pages de texte:
  - Page 1: définition simple d’un ETF (acheter un panier d’actions en un clic).
  - Page 2: focus sur l’ETF **MSCI World** (plus de 1600 entreprises, diversification, frais faibles).
  - Page 3: exemples d’indices (CAC 40, S&P 500, MSCI World) et intérêt de la diversification mondiale.
- 1 quiz-block **incomplet**:
  - id 85 – Question: « Combien d'entreprises contient l'ETF MSCI World ? »  
    - `options: null`, `explanationcorrect: null`, `explanationfalse: null`,  
    - `correctAnswer: "+ 1500"`.

**What I propose to change**

Remplacer ce quiz-block par un quiz complet:

1. **Nombre d’entreprises dans l’ETF MSCI World**  
   - Type: multiple-choice.  
   - Question: « En ordre de grandeur, combien d’entreprises contient l’ETF MSCI World ? »  
   - Options suggérées:  
     - « Environ 40 »  
     - « Environ 500 »  
     - « Plus de 1 600 » (bonne réponse, cohérente avec la leçon)  
     - « Plus de 10 000 »  
   - Explication correcte: rappeler que l’ETF MSCI World regroupe plus de 1600 entreprises des pays développés, ce qui en fait un outil très diversifié.  
   - Explication fausse: corriger l’ordre de grandeur si l’utilisateur choisit une autre option.

If you agree with the above
---------------------------

The next step will be to:

1. Implement a dedicated script (e.g. `scripts/fix-lessons-strapi-live.py`) that:
   - Targets **only** the 4 lessons listed here (by `documentId`).
   - Rebuilds their `content` by:
     - Preserving all text-blocks.
     - Replacing or appending quiz-blocks as described above, in the exact Strapi format (Rich Text paragraphs for options and explanations).
   - Issues a `PUT /api/lessons/{documentId}` for each updated lesson.

2. Run that script **only after your validation** of this plan, so we don’t touch any other lessons or sections.

