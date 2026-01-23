#!/bin/bash
# Exemple : Génération automatique de chapitres

echo "🚀 Exemple : Génération automatique de 2 chapitres pour la section 'Les bases'"
echo ""

# Générer 2 nouveaux chapitres avec leurs leçons
python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 2 \
  --output output/auto-generated-chapters.json

echo ""
echo "✅ Chapitres générés ! Vérifie le fichier : output/auto-generated-chapters.json"
echo ""
echo "💡 Pour créer dans Strapi, relance avec --create :"
echo "   python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \\"
echo "     --section 'Les bases' \\"
echo "     --input output/auto-generated-chapters.json \\"
echo "     --create"
