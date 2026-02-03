# Lancer l'agent pour "Lois et réglementations"

## Prérequis

1. **OPENAI_API_KEY**  
   Clé API OpenAI (pour générer le contenu).  
   [Créer une clé](https://platform.openai.com/api-keys)

2. **STRAPI_API_TOKEN**  
   Token d’API Strapi (le token temporaire fourni précédemment a **expiré**).  
   - Va sur https://cms.finsly.org/admin  
   - Connecte-toi → Settings → API Tokens  
   - Crée un token avec les permissions nécessaires (Content Manager, etc.)  
   - Copie le token

## Configuration

À la racine du projet, crée un fichier `.env` (s’il n’existe pas) :

```bash
# À la racine du projet AI-lesson-agent
OPENAI_API_KEY=sk-...
STRAPI_URL=https://cms.finsly.org
STRAPI_API_TOKEN=ton_nouveau_token_ici
```

Ou exporte les variables dans le terminal avant de lancer :

```bash
export OPENAI_API_KEY=sk-...
export STRAPI_API_TOKEN=ton_nouveau_token
```

## Option 1 : Script tout-en-un

```bash
chmod +x scripts/run-lois-reglementations.sh
./scripts/run-lois-reglementations.sh
```

Cela génère **2 nouveaux chapitres** (et leurs leçons) pour la section "Lois et réglementations", en s’appuyant sur `docs/cours-lois-reglementations-v1.md`, et écrit le résultat dans `output/lois-reglementations-chapters.json` (sans rien créer dans Strapi).

## Option 2 : Commandes manuelles

### Étape 1 : Générer le contenu (sans créer dans Strapi)

```bash
python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Lois et réglementations" \
  --generate-chapters 2 \
  --reference docs/cours-lois-reglementations-v1.md \
  --output output/lois-reglementations-chapters.json
```

Tu peux remplacer `2` par `3` (ou plus) pour générer plus de chapitres.

### Étape 2 : Vérifier le JSON

Ouvre `output/lois-reglementations-chapters.json` et vérifie titres, descriptions et leçons.

### Étape 3 : Créer dans Strapi (après validation)

```bash
python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Lois et réglementations" \
  --input output/lois-reglementations-chapters.json \
  --create
```

L’agent demandera une confirmation avant de créer les chapitres et leçons dans Strapi.

## Titre exact de la section

Dans Strapi, la section peut s’appeler exactement **"Lois et réglementations"** ou **"Lois et réglementations "** (avec un espace).  
Si la section n’est pas trouvée, ouvre l’admin Strapi et recopie le titre exact dans la commande (`--section "..."`).

## En cas d’erreur

- **"Section 'Lois et réglementations' non trouvée"**  
  Vérifier le titre de la section dans Strapi et l’utiliser tel quel dans `--section`.

- **"Token expired"**  
  Régénérer un token dans Strapi Admin et mettre à jour `STRAPI_API_TOKEN` dans `.env` ou dans le terminal.

- **"OPENAI_API_KEY non définie"**  
  Ajouter la clé dans `.env` ou faire `export OPENAI_API_KEY=sk-...` avant de lancer.
