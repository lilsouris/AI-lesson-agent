#!/bin/bash
# Génère de nouveaux chapitres + leçons pour la section "Lois et réglementations"
# Utilise docs/cours-lois-reglementations-v1.md comme référence

set -e
cd "$(dirname "$0")/.."

echo "📚 Section: Lois et réglementations"
echo "📄 Référence: docs/cours-lois-reglementations-v1.md"
echo ""

# Vérifier les variables d'environnement
if [ -z "$OPENAI_API_KEY" ]; then
  echo "❌ OPENAI_API_KEY n'est pas définie."
  echo "   Exporte-la ou ajoute-la dans un fichier .env à la racine du projet."
  echo "   Exemple: export OPENAI_API_KEY=sk-..."
  exit 1
fi

if [ -z "$STRAPI_API_TOKEN" ]; then
  echo "❌ STRAPI_API_TOKEN n'est pas définie."
  echo "   Récupère un nouveau token depuis https://cms.finsly.org/admin (le précédent a expiré)."
  echo "   Exemple: export STRAPI_API_TOKEN=..."
  exit 1
fi

# Charger .env si présent
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

mkdir -p output

echo "🔄 Génération de 2 nouveaux chapitres (sans création dans Strapi)..."
echo ""

python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Lois et réglementations" \
  --generate-chapters 2 \
  --reference docs/cours-lois-reglementations-v1.md \
  --output output/lois-reglementations-chapters.json

echo ""
echo "✅ Contenu généré: output/lois-reglementations-chapters.json"
echo ""
echo "📋 Prochaines étapes:"
echo "   1. Ouvre output/lois-reglementations-chapters.json et vérifie le contenu"
echo "   2. Pour créer les chapitres et leçons dans Strapi, lance:"
echo ""
echo "      python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \\"
echo "        --section \"Lois et réglementations\" \\"
echo "        --input output/lois-reglementations-chapters.json \\"
echo "        --create"
echo ""
