# Guide : Agent AI pour Générer des Leçons et les Créer dans Strapi

## Vue d'ensemble

Cet agent AI permet de :
1. **Lire** des documents de référence en batch (ex: `cours-bourse-v1.md`, `cours-lois-reglementations-v1.md`)
2. **Générer** automatiquement le contenu des leçons selon le format établi
3. **Créer** les entités dans Strapi CMS via l'API après validation

---

## Architecture de l'Agent

```
┌─────────────────┐
│  Documents MD   │ (cours-bourse-v1.md, etc.)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parser Agent   │ (Lit et structure les documents)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generator Agent │ (Génère le contenu selon format)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validation UI   │ (Tu valides le contenu généré)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Strapi Creator  │ (Crée les entités via API)
└─────────────────┘
```

---

## Étape 1 : Structure des Données

### Format d'Entrée (Input)

L'agent reçoit :
- **Fichiers de référence** : Documents Markdown avec la structure des cours
- **Instructions** : Section, Chapitres, Sujets principaux

### Format de Sortie (Output)

L'agent génère un JSON structuré :

```typescript
interface GeneratedContent {
  section: {
    title: string;
    description: RichTextBlock[];
    order: number;
    icon: string;
    difficulty: string;
  };
  chapters: Array<{
    title: string;
    description: RichTextBlock[];
    order: number;
    lessons: Array<{
      title: string;
      description: RichTextBlock[];
      order: number;
      content: {
        textBlocks: Array<{
          title?: string;
          content: string; // Markdown ou Rich Text
          highlight: boolean;
        }>;
        quizBlocks: Array<{
          questions: Array<{
            questionType: "multiple-choice" | "true-false" | "matching" | "slider" | "fill-in" | "drag-drop";
            question: string;
            options: any; // Dépend du type
            correctAnswer: any;
            explanationcorrect: string;
            explanationfalse: string;
            reward: number;
          }>;
        }>;
      };
      estimatedDuration: number;
      coinReward: number;
      difficulty: string;
      slug: string;
    }>;
  }>;
}
```

---

## Étape 2 : Prompt Système pour l'Agent

### Prompt Principal

```markdown
Tu es un expert en création de contenu pédagogique financier pour une application mobile.

TÂCHE :
Générer des leçons complètes selon le format établi, en te basant sur les documents de référence fournis.

FORMAT REQUIS :

1. SECTION
   - title: string
   - description: Rich Text Blocks (array)
   - order: number
   - icon: string
   - difficulty: "beginner" | "intermediate" | "advanced"
   - isActive: true

2. CHAPITRES (array)
   - title: string
   - description: Rich Text Blocks
   - order: number
   - isActive: true
   - estimatedDuration: number (somme des leçons)

3. LEÇONS (array dans chaque chapitre)
   - title: string
   - description: Rich Text Blocks (courte description)
   - order: number
   - content: {
       textBlocks: Array<{
         __component: "lesson.text-block"
         title?: string (optionnel)
         content: string (Markdown format, sera converti en Rich Text)
         highlight: boolean
       }>
       quizBlocks: Array<{
         __component: "lesson.quiz-block"
         questions: Array<{
           questionType: "multiple-choice" | "true-false" | "matching" | "slider" | "fill-in" | "drag-drop"
           question: string
           options: any (format dépend du type)
           correctAnswer: any
           explanationcorrect: string (feedback si bonne réponse)
           explanationfalse: string (feedback si mauvaise réponse)
           reward: number (10 par défaut)
         }>
       }>
     }
   - estimatedDuration: number (10-15 minutes)
   - coinReward: number (50-100)
   - difficulty: "beginner" | "intermediate"
   - slug: string (généré à partir du titre)
   - isActive: true

RÈGLES IMPORTANTES :
- Ton : "tu", "ton", accessible et humain (comme dans les exemples)
- Niveau : Débutant, explications claires
- Questions : 6-8 questions par leçon avec feedback détaillé
- Contenu : Progressif, pédagogique, avec exemples concrets
- Format Markdown : Pour le contenu des text-blocks (sera converti en Rich Text)

EXEMPLES DE RÉFÉRENCE :
[L'agent aura accès aux documents cours-bourse-v1.md et cours-lois-reglementations-v1.md]
```

---

## Étape 3 : Implémentation de l'Agent

### Option A : Script Python avec OpenAI API

```python
# scripts/generate-lessons.py

import os
import json
import openai
from pathlib import Path
from typing import Dict, List, Any
import markdown
from markdown.extensions import codehilite, fenced_code

class LessonGeneratorAgent:
    def __init__(self, api_key: str, strapi_url: str, strapi_token: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.strapi_url = strapi_url.rstrip('/api')
        self.strapi_token = strapi_token
        
    def read_reference_documents(self, doc_paths: List[str]) -> str:
        """Lit les documents de référence en batch"""
        content = ""
        for path in doc_paths:
            with open(path, 'r', encoding='utf-8') as f:
                content += f"\n\n=== DOCUMENT: {Path(path).name} ===\n\n"
                content += f.read()
        return content
    
    def generate_lessons(
        self, 
        section_title: str,
        chapters_topics: List[Dict[str, Any]],  # [{"title": "...", "lessons": [...]}]
        reference_docs: List[str]
    ) -> Dict[str, Any]:
        """Génère le contenu des leçons"""
        
        # Lire les documents de référence
        reference_content = self.read_reference_documents(reference_docs)
        
        # Construire le prompt
        prompt = f"""
Tu es un expert en création de contenu pédagogique financier.

DOCUMENTS DE RÉFÉRENCE :
{reference_content}

TÂCHE :
Générer une section complète avec chapitres et leçons pour : "{section_title}"

STRUCTURE DEMANDÉE :
{json.dumps(chapters_topics, indent=2, ensure_ascii=False)}

Génère le contenu complet au format JSON suivant :
{{
  "section": {{
    "title": "{section_title}",
    "description": [{{"type": "paragraph", "children": [{{"text": "..."}}]}}],
    "order": 1,
    "icon": "icon-name",
    "difficulty": "beginner",
    "isActive": true
  }},
  "chapters": [
    {{
      "title": "...",
      "description": [{{"type": "paragraph", "children": [{{"text": "..."}}]}}],
      "order": 1,
      "isActive": true,
      "lessons": [
        {{
          "title": "...",
          "description": [{{"type": "paragraph", "children": [{{"text": "..."}}]}}],
          "order": 1,
          "content": {{
            "textBlocks": [
              {{
                "title": "...",
                "content": "# Markdown content here",
                "highlight": false
              }}
            ],
            "quizBlocks": [
              {{
                "questions": [
                  {{
                    "questionType": "multiple-choice",
                    "question": "...",
                    "options": ["a) ...", "b) ...", "c) ...", "d) ..."],
                    "correctAnswer": "b) ...",
                    "explanationcorrect": "...",
                    "explanationfalse": "...",
                    "reward": 10
                  }}
                ]
              }}
            ]
          }},
          "estimatedDuration": 15,
          "coinReward": 50,
          "difficulty": "beginner",
          "slug": "generated-slug",
          "isActive": true
        }}
      ]
    }}
  ]
}}

IMPORTANT :
- Utilise le même ton que les documents de référence ("tu", "ton", accessible)
- 6-8 questions par leçon avec feedback détaillé
- Contenu progressif et pédagogique
- Format Markdown pour les text-blocks
"""
        
        # Appel à l'API OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",  # ou "gpt-4" selon disponibilité
            messages=[
                {"role": "system", "content": "Tu es un expert en création de contenu pédagogique financier."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}  # Force JSON
        )
        
        return json.loads(response.choices[0].message.content)
    
    def convert_markdown_to_richtext(self, markdown_text: str) -> List[Dict]:
        """Convertit Markdown en format Rich Text Blocks de Strapi"""
        # Utiliser markdown pour parser
        md = markdown.Markdown(extensions=['codehilite', 'fenced_code'])
        html = md.convert(markdown_text)
        
        # Convertir HTML en Rich Text Blocks (simplifié)
        # Strapi utilise un format spécifique, à adapter selon votre setup
        blocks = []
        
        # Parser simple (à améliorer selon besoins)
        paragraphs = markdown_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                blocks.append({
                    "type": "paragraph",
                    "children": [{"text": para.strip()}]
                })
        
        return blocks
    
    def save_generated_content(self, content: Dict, output_path: str):
        """Sauvegarde le contenu généré pour validation"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(f"✅ Contenu généré sauvegardé dans : {output_path}")
    
    def create_in_strapi(self, content: Dict) -> Dict[str, Any]:
        """Crée les entités dans Strapi via API"""
        results = {
            "section_id": None,
            "chapter_ids": [],
            "lesson_ids": []
        }
        
        # 1. Créer la Section
        section_data = {
            "data": {
                "title": content["section"]["title"],
                "description": content["section"]["description"],
                "order": content["section"]["order"],
                "icon": content["section"]["icon"],
                "difficulty": content["section"]["difficulty"],
                "isActive": content["section"]["isActive"]
            }
        }
        
        response = self._strapi_post("/api/sections", section_data)
        if response:
            results["section_id"] = response["data"]["id"]
            print(f"✅ Section créée : {results['section_id']}")
        
        # 2. Créer les Chapitres
        for chapter in content["chapters"]:
            chapter_data = {
                "data": {
                    "title": chapter["title"],
                    "description": chapter["description"],
                    "order": chapter["order"],
                    "section": results["section_id"],
                    "isActive": chapter["isActive"],
                    "estimatedDuration": sum(
                        lesson.get("estimatedDuration", 15) 
                        for lesson in chapter["lessons"]
                    )
                }
            }
            
            response = self._strapi_post("/api/chapters", chapter_data)
            if response:
                chapter_id = response["data"]["id"]
                results["chapter_ids"].append(chapter_id)
                print(f"✅ Chapitre créé : {chapter_id}")
                
                # 3. Créer les Leçons
                for lesson in chapter["lessons"]:
                    # Convertir le contenu Markdown en Rich Text
                    text_blocks = []
                    for tb in lesson["content"]["textBlocks"]:
                        text_blocks.append({
                            "__component": "lesson.text-block",
                            "title": tb.get("title"),
                            "content": self.convert_markdown_to_richtext(tb["content"]),
                            "highlight": tb.get("highlight", False)
                        })
                    
                    # Créer les quiz blocks
                    quiz_blocks = []
                    for qb in lesson["content"]["quizBlocks"]:
                        quiz_blocks.append({
                            "__component": "lesson.quiz-block",
                            "questions": qb["questions"]
                        })
                    
                    lesson_data = {
                        "data": {
                            "title": lesson["title"],
                            "description": lesson["description"],
                            "order": lesson["order"],
                            "chapter": chapter_id,
                            "lessonType": "course",
                            "content": text_blocks + quiz_blocks,
                            "isActive": lesson["isActive"],
                            "estimatedDuration": lesson["estimatedDuration"],
                            "coinReward": lesson["coinReward"],
                            "slug": lesson["slug"],
                            "difficulty": lesson["difficulty"],
                            "tags": None
                        }
                    }
                    
                    response = self._strapi_post("/api/lessons", lesson_data)
                    if response:
                        results["lesson_ids"].append(response["data"]["id"])
                        print(f"✅ Leçon créée : {response['data']['id']}")
        
        return results
    
    def _strapi_post(self, endpoint: str, data: Dict) -> Dict:
        """Helper pour les requêtes POST vers Strapi"""
        import requests
        
        url = f"{self.strapi_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.strapi_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur lors de la création : {e}")
            return None


# Exemple d'utilisation
if __name__ == "__main__":
    agent = LessonGeneratorAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        strapi_url=os.getenv("STRAPI_URL", "https://cms.finsly.org"),
        strapi_token=os.getenv("STRAPI_API_TOKEN")
    )
    
    # Définir la structure
    chapters_topics = [
        {
            "title": "Chapitre 1 : Les bases",
            "lessons": [
                {"title": "Leçon 1.1 : Introduction", "topics": ["concept A", "concept B"]},
                {"title": "Leçon 1.2 : Les fondamentaux", "topics": ["concept C", "concept D"]}
            ]
        },
        {
            "title": "Chapitre 2 : Approfondissement",
            "lessons": [
                {"title": "Leçon 2.1 : Concepts avancés", "topics": ["concept E"]}
            ]
        }
    ]
    
    # Documents de référence
    reference_docs = [
        "docs/cours-bourse-v1.md",
        "docs/cours-lois-reglementations-v1.md"
    ]
    
    # Générer le contenu
    print("🔄 Génération du contenu...")
    generated_content = agent.generate_lessons(
        section_title="Nouvelle Section",
        chapters_topics=chapters_topics,
        reference_docs=reference_docs
    )
    
    # Sauvegarder pour validation
    agent.save_generated_content(
        generated_content, 
        "output/generated-content.json"
    )
    
    # Demander validation
    print("\n📋 Contenu généré. Vérifie le fichier output/generated-content.json")
    validation = input("Valider et créer dans Strapi ? (oui/non): ")
    
    if validation.lower() == "oui":
        print("🔄 Création dans Strapi...")
        results = agent.create_in_strapi(generated_content)
        print(f"\n✅ Création terminée : {results}")
    else:
        print("❌ Création annulée. Modifie le fichier JSON et relance le script.")
```

---

## Étape 4 : Script Node.js/TypeScript (Alternative)

```typescript
// scripts/generate-lessons.ts

import OpenAI from 'openai';
import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';

interface LessonGeneratorConfig {
  openaiApiKey: string;
  strapiUrl: string;
  strapiToken: string;
}

class LessonGeneratorAgent {
  private openai: OpenAI;
  private strapiUrl: string;
  private strapiToken: string;

  constructor(config: LessonGeneratorConfig) {
    this.openai = new OpenAI({ apiKey: config.openaiApiKey });
    this.strapiUrl = config.strapiUrl.replace(/\/api$/, '');
    this.strapiToken = config.strapiToken;
  }

  async readReferenceDocuments(docPaths: string[]): Promise<string> {
    let content = '';
    for (const docPath of docPaths) {
      const fileContent = fs.readFileSync(docPath, 'utf-8');
      content += `\n\n=== DOCUMENT: ${path.basename(docPath)} ===\n\n`;
      content += fileContent;
    }
    return content;
  }

  async generateLessons(
    sectionTitle: string,
    chaptersTopics: any[],
    referenceDocs: string[]
  ): Promise<any> {
    const referenceContent = await this.readReferenceDocuments(referenceDocs);

    const prompt = `
Tu es un expert en création de contenu pédagogique financier.

DOCUMENTS DE RÉFÉRENCE :
${referenceContent}

TÂCHE :
Générer une section complète avec chapitres et leçons pour : "${sectionTitle}"

STRUCTURE DEMANDÉE :
${JSON.stringify(chaptersTopics, null, 2)}

Génère le contenu complet au format JSON. Utilise le même format que les documents de référence.
`;

    const response = await this.openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        {
          role: 'system',
          content:
            'Tu es un expert en création de contenu pédagogique financier. Tu génères toujours du JSON valide.',
        },
        { role: 'user', content: prompt },
      ],
      temperature: 0.7,
      response_format: { type: 'json_object' },
    });

    return JSON.parse(response.choices[0].message.content || '{}');
  }

  async createInStrapi(content: any): Promise<any> {
    const results = {
      section_id: null as number | null,
      chapter_ids: [] as number[],
      lesson_ids: [] as number[],
    };

    // Créer la Section
    try {
      const sectionResponse = await axios.post(
        `${this.strapiUrl}/api/sections`,
        {
          data: content.section,
        },
        {
          headers: {
            Authorization: `Bearer ${this.strapiToken}`,
            'Content-Type': 'application/json',
          },
        }
      );
      results.section_id = sectionResponse.data.data.id;
      console.log(`✅ Section créée : ${results.section_id}`);
    } catch (error) {
      console.error('❌ Erreur création section:', error);
      return results;
    }

    // Créer les Chapitres et Leçons
    for (const chapter of content.chapters) {
      try {
        const chapterResponse = await axios.post(
          `${this.strapiUrl}/api/chapters`,
          {
            data: {
              ...chapter,
              section: results.section_id,
            },
          },
          {
            headers: {
              Authorization: `Bearer ${this.strapiToken}`,
              'Content-Type': 'application/json',
            },
          }
        );
        const chapterId = chapterResponse.data.data.id;
        results.chapter_ids.push(chapterId);
        console.log(`✅ Chapitre créé : ${chapterId}`);

        // Créer les Leçons
        for (const lesson of chapter.lessons) {
          try {
            const lessonResponse = await axios.post(
              `${this.strapiUrl}/api/lessons`,
              {
                data: {
                  ...lesson,
                  chapter: chapterId,
                },
              },
              {
                headers: {
                  Authorization: `Bearer ${this.strapiToken}`,
                  'Content-Type': 'application/json',
                },
              }
            );
            results.lesson_ids.push(lessonResponse.data.data.id);
            console.log(`✅ Leçon créée : ${lessonResponse.data.data.id}`);
          } catch (error) {
            console.error(`❌ Erreur création leçon:`, error);
          }
        }
      } catch (error) {
        console.error(`❌ Erreur création chapitre:`, error);
      }
    }

    return results;
  }
}

// Exemple d'utilisation
async function main() {
  const agent = new LessonGeneratorAgent({
    openaiApiKey: process.env.OPENAI_API_KEY!,
    strapiUrl: process.env.STRAPI_URL || 'https://cms.finsly.org',
    strapiToken: process.env.STRAPI_API_TOKEN!,
  });

  const chaptersTopics = [
    {
      title: 'Chapitre 1 : Les bases',
      lessons: [
        { title: 'Leçon 1.1 : Introduction', topics: ['concept A'] },
      ],
    },
  ];

  const referenceDocs = [
    'docs/cours-bourse-v1.md',
    'docs/cours-lois-reglementations-v1.md',
  ];

  console.log('🔄 Génération du contenu...');
  const generatedContent = await agent.generateLessons(
    'Nouvelle Section',
    chaptersTopics,
    referenceDocs
  );

  // Sauvegarder pour validation
  fs.writeFileSync(
    'output/generated-content.json',
    JSON.stringify(generatedContent, null, 2)
  );
  console.log('✅ Contenu sauvegardé dans output/generated-content.json');

  // Ici, tu valides manuellement, puis :
  // const results = await agent.createInStrapi(generatedContent);
}

main();
```

---

## Étape 5 : Workflow Complet

### 1. Préparation

```bash
# Créer le dossier pour les outputs
mkdir -p output

# Installer les dépendances (Python)
pip install openai requests markdown

# Ou (Node.js)
npm install openai axios
```

### 2. Configuration

Créer un fichier `.env` :

```env
OPENAI_API_KEY=sk-...
STRAPI_URL=https://cms.finsly.org
STRAPI_API_TOKEN=your-strapi-token
```

### 3. Utilisation

```bash
# Python
python scripts/generate-lessons.py

# Node.js
npm run generate-lessons
```

### 4. Validation

1. L'agent génère le contenu dans `output/generated-content.json`
2. Tu vérifies le contenu
3. Tu valides ou demandes des modifications
4. Si validé, l'agent crée dans Strapi

---

## Étape 6 : Interface de Validation (Optionnel)

Créer une interface web simple pour valider avant création :

```html
<!-- scripts/validation-ui.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Validation Contenu Généré</title>
</head>
<body>
    <h1>Validation du Contenu Généré</h1>
    <div id="content-preview"></div>
    <button onclick="validate()">✅ Valider et Créer dans Strapi</button>
    <button onclick="reject()">❌ Rejeter</button>
    
    <script>
        // Charger le JSON généré
        fetch('output/generated-content.json')
            .then(r => r.json())
            .then(data => {
                // Afficher le contenu pour validation
                document.getElementById('content-preview').innerHTML = 
                    JSON.stringify(data, null, 2);
            });
        
        function validate() {
            // Appeler l'API pour créer dans Strapi
            fetch('/api/create-in-strapi', { method: 'POST' })
                .then(() => alert('✅ Créé dans Strapi !'));
        }
    </script>
</body>
</html>
```

---

## Points d'Attention

### 1. Conversion Markdown → Rich Text

Strapi utilise un format Rich Text spécifique. Il faut convertir le Markdown :

```typescript
function markdownToRichText(md: string): any[] {
  // Parser Markdown et convertir en format Strapi
  // Format Strapi : [{ type: "paragraph", children: [{ text: "..." }] }]
  // Utiliser une librairie comme remark ou markdown-it
}
```

### 2. Gestion des Quiz Blocks

Les quiz blocks dans Strapi ont une structure spécifique. Vérifier le format exact dans votre Strapi :

```typescript
// Format probable dans Strapi
{
  __component: "lesson.quiz-block",
  questions: [
    {
      questionType: "multiple-choice",
      question: "...",
      options: [...],
      correctAnswer: "...",
      explanationcorrect: [...], // Rich Text Blocks
      explanationfalse: [...],   // Rich Text Blocks
      reward: 10
    }
  ]
}
```

### 3. Gestion des Erreurs

Ajouter une gestion d'erreurs robuste :

```python
try:
    results = agent.create_in_strapi(generated_content)
except Exception as e:
    print(f"❌ Erreur : {e}")
    # Sauvegarder l'état pour reprendre plus tard
    save_checkpoint(results)
```

### 4. Validation Progressive

Créer section par section, chapitre par chapitre, pour éviter de tout perdre en cas d'erreur.

---

## Améliorations Futures

1. **Interface Web** : Dashboard pour gérer la génération et validation
2. **Édition** : Permettre d'éditer le contenu généré avant validation
3. **Versioning** : Sauvegarder les versions générées
4. **Batch Processing** : Générer plusieurs sections en une fois
5. **Templates** : Sauvegarder des templates de structure pour réutilisation

---

## Exemple de Commande Complète

```bash
# 1. Générer le contenu
python scripts/generate-lessons.py \
  --section "Épargne et Budget" \
  --chapters "docs/chapters-structure.json" \
  --reference "docs/cours-bourse-v1.md docs/cours-lois-reglementations-v1.md" \
  --output "output/generated-epargne.json"

# 2. Valider (manuellement ou via UI)
# 3. Créer dans Strapi
python scripts/generate-lessons.py \
  --create \
  --input "output/generated-epargne.json"
```

---

**Document créé le :** [Date]
**Version :** 1.0
**Statut :** Guide d'implémentation
