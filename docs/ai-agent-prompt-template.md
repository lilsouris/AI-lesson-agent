# Template de Prompt pour l'Agent AI

## Structure d'Entrée (Input JSON)

Crée un fichier JSON avec la structure des leçons que tu veux générer :

```json
[
  {
    "title": "Qu'est-ce que la bourse ?",
    "description": "Introduction aux concepts fondamentaux de la bourse et des marchés financiers.",
    "order": 1,
    "difficulty": "easy",
    "topics": [
      "Définition de la bourse",
      "Pourquoi les entreprises entrent en bourse",
      "Comment fonctionne le marché",
      "Les indices boursiers",
      "Pourquoi investir en bourse"
    ]
  },
  {
    "title": "Actions vs obligations : comprendre la différence",
    "description": "Apprendre à distinguer les actions des obligations et comprendre leurs caractéristiques.",
    "order": 2,
    "difficulty": "easy",
    "topics": [
      "Définition des actions",
      "Définition des obligations",
      "Comparaison concrète",
      "Le risque de défaut",
      "Quand choisir quoi",
      "Le mix actions/obligations"
    ]
  }
]
```

## Exemple de Commande

```bash
# 1. Générer le contenu
python python-agent/scripts-generate-lessons-agent.py \
  --section "Les bases" \
  --chapter "Les bases de la bourse" \
  --lessons input/lessons-bourse-ch1.json \
  --reference docs/cours-bourse-v1.md \
  --output output/generated-bourse-ch1.json

# 2. Valider le fichier output/generated-bourse-ch1.json

# 3. Créer dans Strapi
python python-agent/scripts-generate-lessons-agent.py \
  --section "Les bases" \
  --chapter "Les bases de la bourse" \
  --input output/generated-bourse-ch1.json \
  --create

# 4. Si tu veux attacher uniquement à un chapitre existant (ne pas créer de chapitre)
python python-agent/scripts-generate-lessons-agent.py \
  --section "Les bases" \
  --chapter "Les bases de la bourse" \
  --input output/generated-bourse-ch1.json \
  --create \
  --attach-only
```

## Format de Sortie Généré

L'agent génère un JSON avec cette structure :

```json
{
  "chapterTitle": "Les bases de la bourse",
  "lessons": [
    {
      "title": "Qu'est-ce que la bourse ?",
      "description": [
        {
          "type": "paragraph",
          "children": [
            {
              "text": "Introduction aux concepts fondamentaux de la bourse et des marchés financiers.",
              "type": "text"
            }
          ]
        }
      ],
      "order": 1,
      "difficulty": "easy",
      "estimatedDuration": 12,
      "coinReward": 250,
      "lessonType": "quizz",
      "isActive": true,
      "slug": "quest-ce-que-la-bourse",
      "content": {
        "textBlocks": [
          {
            "title": "Page 1",
            "content": [
              {
                "type": "paragraph",
                "children": [
                  {
                    "text": "La bourse, c'est quoi exactement ? ...",
                    "type": "text"
                  }
                ]
              }
            ],
            "highlight": false
          }
        ],
        "quizBlocks": [
          {
            "Question": "Qu'est-ce qu'une action ?",
            "questionType": "multiple-choice",
            "options": [
              {
                "type": "paragraph",
                "children": [
                  {
                    "text": "Un prêt que tu fais à une entreprise",
                    "type": "text"
                  }
                ]
              },
              {
                "type": "paragraph",
                "children": [
                  {
                    "text": "Une part de propriété d'une entreprise",
                    "type": "text"
                  }
                ]
              }
            ],
            "correctAnswer": "Une part de propriété d'une entreprise",
            "explanationcorrect": [
              {
                "type": "paragraph",
                "children": [
                  {
                    "text": "Exactement ! Une action = une part de propriété...",
                    "type": "text"
                  }
                ]
              }
            ],
            "explanationfalse": [
              {
                "type": "paragraph",
                "children": [
                  {
                    "text": "Non ! Une action, c'est une part de propriété...",
                    "type": "text"
                  }
                ]
              }
            ],
            "points": 5
          }
        ]
      }
    }
  ]
}
```

## Règles de Génération

1. **Coin Rewards** (calculés automatiquement) :
   - 2-3 questions : 150 coins
   - 4-5 questions : 200 coins
   - 6 questions : 250 coins
   - 7 questions : 300 coins
   - 8 questions : 350 coins

2. **Durée estimée** : 10-15 minutes par leçon (basé sur lecture + quiz)

3. **Structure du contenu** :
   - 2-4 text-blocks par leçon (contenu pédagogique)
   - 6-8 quiz-blocks par leçon (questions avec feedback)

4. **Types de questions supportés** :
   - `multiple-choice` : Choix multiples
   - `true-false` : Vrai/Faux
   - `matching` : Association
   - `drag-drop` : Glisser-déposer
   - `drag-order` : Ordre de classement
   - `Slider` : Question avec slider

5. **Ton** : "tu", "ton", accessible et humain (comme dans les exemples de référence)
