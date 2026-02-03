# Workflow : Générer dans Cursor Chat puis envoyer dans Strapi

L’idée : **tu utilises Cursor Chat (l’agent) pour générer le contenu des leçons**, tu valides le fichier généré, puis **tu envoies tout dans Strapi** avec le script (sans OpenAI).

## Étapes

### 1. Demander à Cursor de générer le contenu

Dans Cursor Chat, utilise un message du type (voir le template ci‑dessous) pour demander la génération de chapitres et leçons au format attendu.

L’agent va :
- s’appuyer sur `docs/cours-lois-reglementations-v1.md` (ou le doc que tu indiques),
- produire un JSON avec la structure `chapters` / `lessons` / `textBlocks` / `quizBlocks`,
- **écrire le fichier** dans `output/` (ex. `output/lois-reglementations-generated.json`).

Tu peux autoriser la création/écriture du fichier quand Cursor te le demande.

### 2. Valider le fichier généré

- Ouvre le fichier dans `output/` (ex. `output/lois-reglementations-generated.json`).
- Vérifie titres, textes, quiz et feedbacks.
- Corrige si besoin (directement dans le JSON ou en redemandant à Cursor une version corrigée).

### 3. Envoyer dans Strapi (sans OpenAI)

Une fois le contenu validé, lance le script avec **uniquement** le fichier généré et l’option de création.  
Il ne fait **pas** appel à OpenAI, seulement à l’API Strapi.

```bash
# Depuis la racine du projet
export STRAPI_URL="https://cms.finsly.org"
export STRAPI_API_TOKEN="<ton_token_strapi>"

python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Lois et réglementations" \
  --input output/lois-reglementations-generated.json \
  --create
```

- Le script charge le JSON, **normalise** le contenu (markdown → Rich Text, options en blocks, `coinReward`, etc.).
- Il crée les chapitres et leçons dans la section indiquée.
- Réponds `oui` quand il demande confirmation avant de créer.

**Note :** Pour ce push, tu n’as **pas** besoin de `OPENAI_API_KEY`, seulement `STRAPI_API_TOKEN` (et optionnellement `STRAPI_URL`).

## Format du JSON que Cursor doit générer

Le fichier doit être un JSON avec une clé `chapters` (liste de chapitres). Chaque chapitre a au minimum :

- `title` : titre du chapitre  
- `description` : courte description (texte simple ou 1–2 phrases)  
- `order` : numéro d’ordre (1, 2, 3…)  
- `lessons` : liste de leçons  

Chaque leçon doit avoir :

- `title`, `description` (texte ou array de blocs “paragraph”), `order`, `difficulty` (`"easy"` / `"medium"` / `"hard"`), `estimatedDuration` (minutes)
- `content` :
  - `textBlocks` : liste de `{ "title": "Page 1", "content": "Contenu en **markdown**...", "highlight": false }`
  - `quizBlocks` : liste de questions avec `Question`, `questionType`, `options` (liste de strings), `correctAnswer`, `explanationcorrect`, `explanationfalse` (strings), `points` (ex. 5)

Tu peux omettre : `coinReward`, `slug`, `lessonType` — le script les calcule ou complète à l’envoi.

Exemple minimal d’une leçon :

```json
{
  "title": "Comprendre l'impôt sur le revenu",
  "description": "Introduction à l'impôt sur le revenu en France.",
  "order": 1,
  "difficulty": "easy",
  "estimatedDuration": 12,
  "content": {
    "textBlocks": [
      {
        "title": "Page 1",
        "content": "**L'impôt sur le revenu, c'est quoi ?**\n\nC'est l'impôt que tu paies chaque année...",
        "highlight": false
      }
    ],
    "quizBlocks": [
      {
        "Question": "Qu'est-ce que l'impôt sur le revenu en France ?",
        "questionType": "multiple-choice",
        "options": ["Un impôt proportionnel", "Un impôt progressif", "Un impôt fixe"],
        "correctAnswer": "Un impôt progressif",
        "explanationcorrect": "Exactement ! C'est un impôt progressif...",
        "explanationfalse": "Attention ! L'impôt sur le revenu est progressif...",
        "points": 5
      }
    ]
  }
}
```

Le script convertira le markdown des `textBlocks` et les strings des options/explications en Rich Text Blocks Strapi.

## Résumé

| Étape | Où | Besoin |
|-------|-----|--------|
| 1. Générer le contenu | Cursor Chat | Toi + prompt (template ci‑dessous) |
| 2. Valider | Éditeur (fichier dans `output/`) | Toi |
| 3. Envoyer dans Strapi | Terminal (script Python) | `STRAPI_API_TOKEN` (pas d’OpenAI) |

Ainsi, **Cursor fait la génération**, et **le script ne fait que l’envoi** vers Strapi.
