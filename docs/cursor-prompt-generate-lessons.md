# Prompt Cursor : générer des leçons pour Strapi

Copie-colle ce bloc dans **Cursor Chat** pour que l’agent génère le JSON des chapitres/leçons, puis enregistre le fichier dans `output/`.

---

## Version courte (à personnaliser)

```
Génère pour moi le contenu de chapitres et leçons pour la section Strapi "Lois et réglementations", au format JSON prêt à être envoyé avec notre script (push Strapi).

À faire :
1. Utiliser comme référence le contenu et le style de docs/cours-lois-reglementations-v1.md.
2. Générer 2 chapitres avec plusieurs leçons chacun (ex. Chapitre 1 : Les bases de la fiscalité française — au moins 2 leçons ; Chapitre 2 : un chapitre en continuité, 2 leçons).
3. Chaque leçon : 2–4 text-blocks (contenu en markdown), 6–8 quiz-blocks. Types de questions : multiple-choice, true-false, matching si pertinent. Ton "tu/ton", pédagogique.
4. Format exact : JSON avec une clé "chapters". Chaque chapitre : "title", "description", "order", "lessons". Chaque leçon : "title", "description", "order", "difficulty", "estimatedDuration", "content" avec "textBlocks" (title, content en markdown, highlight) et "quizBlocks" (Question, questionType, options en liste de strings, correctAnswer, explanationcorrect, explanationfalse, points: 5). Pas besoin de mettre coinReward, slug, lessonType — le script les gère.
5. Écrire le résultat dans output/lois-reglementations-generated.json (créer output/ si besoin).
```

---

## Version détaillée (Lois et réglementations)

```
Tu es l’agent qui génère le contenu des leçons pour l’app Finsly. Je veux que tu génères le JSON des chapitres et leçons pour la section "Lois et réglementations", puis que tu écrives ce JSON dans un fichier pour que je puisse l’envoyer dans Strapi avec notre script.

Référence : lis docs/cours-lois-reglementations-v1.md pour le style (tu/ton, pédagogique, quiz avec feedback détaillé) et pour le contenu (fiscalité, impôt sur le revenu, revenus imposables, livrets, PEA, etc.).

Contraintes :
- Section cible Strapi : "Lois et réglementations"
- Génère 2 chapitres minimum, avec au moins 2 leçons par chapitre
- Chaque leçon : 2–4 text-blocks (contenu en markdown, champs "title" et "content"), 6–8 quiz-blocks
- Types de quiz : multiple-choice, true-false, et matching si ça va bien au contenu
- Pour chaque question : Question, questionType, options (liste de strings), correctAnswer (texte exact d’une option), explanationcorrect et explanationfalse (strings), points: 5
- Ne pas remplir coinReward, slug, lessonType — le script de push les calcule ou définit

Format de sortie : un seul objet JSON avec la clé "chapters". Structure attendue par le script (voir docs/workflow-cursor-generate-then-push.md et docs/strapi-lesson-template.json).

Écris le JSON dans le fichier output/lois-reglementations-generated.json. Crée le dossier output/ s’il n’existe pas.
```

---

## Variante : un seul chapitre

Si tu veux un seul chapitre (par ex. pour tester) :

```
Génère 1 chapitre pour la section "Lois et réglementations", avec 2 leçons complètes (text-blocks + 6–8 questions chacune), en t’inspirant de docs/cours-lois-reglementations-v1.md. Format JSON comme dans docs/workflow-cursor-generate-then-push.md, clé "chapters". Écris le résultat dans output/lois-reglementations-one-chapter.json.
```

---

## Après la génération

1. Vérifier le fichier dans `output/`.
2. Lancer le push Strapi (sans OpenAI) :

```bash
export STRAPI_API_TOKEN="<ton_token>"
python3 python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Lois et réglementations" \
  --input output/lois-reglementations-generated.json \
  --create
```

Répondre `oui` à la confirmation pour créer les chapitres et leçons dans Strapi.
