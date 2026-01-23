# Guide : Génération Automatique de Chapitres

## 🎯 Fonctionnalité

L'agent peut maintenant **générer automatiquement des chapitres** en analysant les chapitres existants d'une section et en proposant de nouvelles idées en continuité.

## 📋 Utilisation

### Option 1 : Génération Automatique de Chapitres

Génère automatiquement N nouveaux chapitres avec leurs leçons complètes :

```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 3 \
  --create
```

**Ce que fait l'agent :**
1. ✅ Analyse les chapitres existants de la section
2. ✅ Génère des suggestions de nouveaux chapitres en continuité
3. ✅ Génère automatiquement les leçons pour chaque chapitre
4. ✅ Crée tout dans Strapi

### Option 2 : Chapitre Spécifique (comme avant)

Génère un chapitre spécifique avec des leçons définies :

```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --chapter "Nouveau chapitre" \
  --lessons scripts/example-lessons-input.json \
  --create
```

## 🔍 Comment ça marche ?

### Analyse des Chapitres Existants

L'agent récupère automatiquement :
- Les titres des chapitres existants
- Leurs descriptions
- Leur ordre
- Le contexte de la section

### Génération Intelligente

L'agent utilise ces informations pour :
- **Proposer des chapitres cohérents** avec le thème existant
- **Respecter la progression logique** (du simple au complexe)
- **Éviter les doublons** avec les chapitres existants
- **Suggérer 2-3 leçons** par chapitre

### Exemple de Continuité

Si une section "Les bases" contient :
1. Fondamentaux de l'argent et de l'épargne
2. Préparer sa stratégie d'investissement
3. Introduction aux investissements

L'agent pourrait suggérer :
4. Les mécanismes de l'investissement (déjà existant)
5. **Gérer son budget efficacement** (nouveau)
6. **Comprendre les risques financiers** (nouveau)
7. **Les outils d'investissement modernes** (nouveau)

## 📝 Format de Sortie

L'agent génère un JSON avec cette structure :

```json
{
  "chapters": [
    {
      "title": "Gérer son budget efficacement",
      "description": "Apprendre à créer et suivre un budget pour mieux gérer ses finances.",
      "order": 6,
      "lessons": [
        {
          "title": "Pourquoi faire un budget ?",
          "description": [...],
          "order": 1,
          "difficulty": "easy",
          "estimatedDuration": 12,
          "coinReward": 250,
          "lessonType": "quizz",
          "content": {
            "textBlocks": [...],
            "quizBlocks": [...]
          }
        }
      ]
    }
  ]
}
```

## ⚙️ Options Avancées

### Attacher uniquement à des chapitres existants

```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 2 \
  --attach-only \
  --create
```

⚠️ **Attention** : Avec `--attach-only`, l'agent ne créera pas de nouveaux chapitres, seulement des leçons dans les chapitres existants.

### Utiliser des documents de référence personnalisés

```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 3 \
  --reference docs/cours-bourse-v1.md docs/cours-lois-reglementations-v1.md \
  --create
```

## 🎨 Personnalisation

### Ajuster la créativité

Pour des suggestions plus créatives, modifie `temperature=0.8` dans la fonction `generate_chapter_suggestions()`.

Pour des suggestions plus conservatrices, utilise `temperature=0.6`.

### Ajuster le nombre de leçons par chapitre

Par défaut, l'agent suggère 2-3 leçons par chapitre. Tu peux modifier cela dans le prompt système.

## 📊 Exemple Complet

```bash
# 1. Générer 3 nouveaux chapitres automatiquement
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 3 \
  --output output/new-chapters.json

# 2. Vérifier le contenu généré
cat output/new-chapters.json

# 3. Créer dans Strapi
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --input output/new-chapters.json \
  --create
```

## 💡 Conseils

1. **Commence petit** : Génère 1-2 chapitres d'abord pour voir la qualité
2. **Valide toujours** : Vérifie le JSON généré avant de créer dans Strapi
3. **Utilise les références** : Plus tu donnes de documents de référence, meilleures seront les suggestions
4. **Ajuste l'ordre** : L'agent calcule l'ordre automatiquement, mais tu peux le modifier dans le JSON

## 🐛 Dépannage

### Les chapitres générés ne sont pas cohérents

- Vérifie que les documents de référence sont pertinents
- Augmente le nombre de chapitres existants analysés
- Ajuste le prompt système pour être plus spécifique

### L'agent génère des chapitres qui existent déjà

- L'agent essaie d'éviter les doublons, mais vérifie toujours
- Tu peux modifier manuellement le JSON avant de créer

### Les leçons générées ne sont pas assez détaillées

- Augmente le nombre de `topics` dans les leçons suggérées
- Utilise des documents de référence plus détaillés
- Ajuste le prompt pour demander plus de contenu
