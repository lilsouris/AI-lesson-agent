# AI Lesson Generator Agent for Finsly

Agent AI pour générer des leçons pédagogiques et les créer automatiquement dans Strapi CMS.

## 🎯 Fonctionnalités

- ✅ Génère des leçons complètes avec contenu pédagogique + quiz (6-8 questions)
- ✅ **NOUVEAU** : Génère automatiquement des chapitres en continuité avec l'existant
- ✅ Attache automatiquement aux sections/chapitres existants dans Strapi
- ✅ Format exact Strapi (Rich Text Blocks, dynamic zones, quiz blocks)
- ✅ Calcul automatique des coin rewards selon le nombre de questions
- ✅ Conversion Markdown → Rich Text Blocks
- ✅ Support de tous les types de questions (multiple-choice, true-false, matching, drag-drop, etc.)

## 📋 Prérequis

1. **Python 3.8+**
2. **Variables d'environnement** :
   ```bash
   export OPENAI_API_KEY="sk-..."
   export STRAPI_URL="https://cms.finsly.org"
   export STRAPI_API_TOKEN="17baf835bfcfbc48b18c5327679745d0e7c9fdc179929f392f6e13096fddb6a035a5ce153b93c7d4bf7f2f01a594ba7c79bfec9f5ec284b9d060b78622afc264614433425753ef6cd9cd62f8a15c1a332de9973e8262cf3d457674029bbb23aa31d10319d3e03c88d70d5606312af0753cd7f692003ba9a2655dc52690411070"
   ```

3. **Dépendances Python** :
   ```bash
   pip install openai requests
   ```

## 🚀 Utilisation Rapide

### Option A : Génération Automatique de Chapitres (NOUVEAU)

Génère automatiquement N nouveaux chapitres avec leurs leçons en analysant les chapitres existants :

```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 3 \
  --create
```

L'agent :
- ✅ Analyse les chapitres existants de la section
- ✅ Génère des suggestions de nouveaux chapitres en continuité
- ✅ Génère automatiquement les leçons pour chaque chapitre
- ✅ Crée tout dans Strapi

Voir `docs/chapter-generation-guide.md` pour plus de détails.

### Option B : Génération Manuelle (Chapitre Spécifique)

### Étape 1 : Créer un fichier d'entrée JSON

Crée un fichier JSON avec la structure des leçons que tu veux générer :

```json
[
  {
    "title": "Qu'est-ce que la bourse ?",
    "description": "Introduction aux concepts fondamentaux de la bourse.",
    "order": 1,
    "difficulty": "easy",
    "topics": [
      "Définition de la bourse",
      "Pourquoi les entreprises entrent en bourse",
      "Comment fonctionne le marché"
    ]
  }
]
```

Voir `scripts/example-lessons-input.json` pour un exemple complet.

### Étape 2 : Générer le contenu

**Avec le script de génération de chapitres :**
```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --chapter "Les bases de la bourse" \
  --lessons scripts/example-lessons-input.json \
  --reference docs/cours-bourse-v1.md \
  --output output/generated-content.json
```

**Ou avec l'ancien script (leçons uniquement) :**
```bash
python python-agent/scripts-generate-lessons-agent.py \
  --section "Les bases" \
  --chapter "Les bases de la bourse" \
  --lessons scripts/example-lessons-input.json \
  --reference docs/cours-bourse-v1.md \
  --output output/generated-content.json
```

### Étape 3 : Valider le contenu généré

Ouvre `output/generated-content.json` et vérifie que tout est correct.

### Étape 4 : Créer dans Strapi

```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --chapter "Les bases de la bourse" \
  --input output/generated-content.json \
  --create
```

## 📖 Options de Commande

```bash
python python-agent/scripts-generate-lessons-agent.py [OPTIONS]

Options:
  --section TEXT          Titre de la section existante dans Strapi [requis]
  --chapter TEXT          Titre du chapitre (existant ou à créer) [requis]
  --lessons FILE          Fichier JSON avec structure des leçons [requis si --input non fourni]
  --reference FILE...     Documents de référence Markdown (optionnel)
  --output FILE           Fichier de sortie JSON (défaut: output/generated-content.json)
  --input FILE            Charger un JSON généré au lieu de générer
  --create                Créer directement dans Strapi après génération
  --attach-only           Attacher uniquement à un chapitre existant (ne pas créer)
```

## 💰 Calcul des Coin Rewards

Les coin rewards sont calculés automatiquement selon le nombre de questions :

- **2-3 questions** : 150 coins
- **4-5 questions** : 200 coins
- **6 questions** : 250 coins
- **7 questions** : 300 coins
- **8 questions** : 350 coins

## 📝 Format Strapi

L'agent génère du contenu au format exact Strapi :

- **Text Blocks** : `lesson-content.text-block` avec Rich Text Blocks
- **Quiz Blocks** : `lesson-content.quizz-block` avec :
  - `Question` (string)
  - `questionType` : `"multiple-choice" | "true-false" | "matching" | "drag-drop" | "drag-order" | "Slider"`
  - `options` : Array de Rich Text Blocks
  - `correctAnswer` : String (exact match)
  - `explanationcorrect` / `explanationfalse` : Rich Text Blocks
  - `points` : 5 (par défaut)

- **Lesson** :
  - `lessonType` : Toujours `"quizz"`
  - `difficulty` : `"easy" | "medium" | "hard"`
  - `estimatedDuration` : Minutes (10-15 par défaut)
  - `coinReward` : Calculé automatiquement

## 🔍 Référence

L'agent utilise la leçon **"L'inflation, ton ennemi silencieux"** du chapitre **"Fondamentaux de l'investissement"** comme référence pour le format exact.

## 📚 Documentation

- **Génération automatique de chapitres** : `docs/chapter-generation-guide.md` ⭐ NOUVEAU
- **Template de prompt** : `docs/ai-agent-prompt-template.md`
- **Template JSON Strapi** : `docs/strapi-lesson-template.json`
- **Exemple d'entrée** : `scripts/example-lessons-input.json`

## 🔄 Deux Scripts Disponibles

1. **`scripts-generate-chapters-and-lessons-agent.py`** ⭐ RECOMMANDÉ
   - Génère des chapitres ET des leçons
   - Peut générer automatiquement des chapitres en continuité
   - Plus complet et flexible

2. **`scripts-generate-lessons-agent.py`**
   - Génère uniquement des leçons
   - Pour un chapitre spécifique existant
   - Plus simple, pour des cas d'usage spécifiques

## ⚠️ Notes Importantes

1. **Sections** : L'agent ne crée **PAS** de nouvelles sections. Il attache uniquement aux sections existantes.

2. **Chapitres** : Par défaut, l'agent crée un nouveau chapitre s'il n'existe pas. Utilise `--attach-only` pour attacher uniquement à un chapitre existant.

3. **Validation** : Toujours valider le JSON généré avant de créer dans Strapi.

4. **Documents de référence** : Utilise `docs/cours-bourse-v1.md` et `docs/cours-lois-reglementations-v1.md` comme exemples de style et de structure.

## 🐛 Dépannage

### Erreur "Section non trouvée"
- Vérifie que le titre de la section correspond exactement à celui dans Strapi
- Les titres sont sensibles à la casse

### Erreur "Chapitre non trouvé" avec `--attach-only`
- Le chapitre doit exister dans Strapi
- Retire `--attach-only` pour créer le chapitre automatiquement

### Erreur de format Rich Text Blocks
- L'agent convertit automatiquement le Markdown en Rich Text Blocks
- Si erreur, vérifie que le JSON généré a bien le format attendu

## 📄 Licence

Propriétaire - Finsly
