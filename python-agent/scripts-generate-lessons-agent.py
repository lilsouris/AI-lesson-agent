#!/usr/bin/env python3
"""
Agent AI pour générer des leçons et les créer dans Strapi CMS

Usage:
    python scripts-generate-lessons-agent.py --section "Les bases" --chapter "Fondamentaux" --lessons lessons-input.json
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from openai import OpenAI


class LessonGeneratorAgent:
    """Agent AI pour générer des leçons pédagogiques selon le format Strapi exact"""
    
    def __init__(self, openai_api_key: str, strapi_url: str, strapi_token: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.strapi_url = strapi_url.rstrip('/api').rstrip('/')
        self.strapi_token = strapi_token
        
    def read_reference_documents(self, doc_paths: List[str]) -> str:
        """Lit les documents de référence en batch"""
        content = ""
        for path in doc_paths:
            full_path = Path(path)
            if not full_path.exists():
                print(f"⚠️  Document non trouvé : {path}")
                continue
                
            with open(full_path, 'r', encoding='utf-8') as f:
                content += f"\n\n=== DOCUMENT: {full_path.name} ===\n\n"
                content += f.read()
        return content
    
    def convert_markdown_to_richtext(self, markdown_text: str) -> List[Dict]:
        """Convertit Markdown en format Rich Text Blocks de Strapi"""
        blocks = []
        
        # Split par paragraphes (double newline)
        paragraphs = markdown_text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Détecter les titres
            if para.startswith('#'):
                level = len(para) - len(para.lstrip('#'))
                text = para.lstrip('#').strip()
                # Strapi supports heading-1 to heading-6
                heading_type = f"heading-{min(level, 6)}"
                blocks.append({
                    "type": heading_type,
                    "children": [{"text": text, "type": "text"}]
                })
            # Détecter le gras **text**
            elif '**' in para:
                # Simple parser pour le gras - on garde le texte avec bold
                text = para
                children = []
                parts = re.split(r'(\*\*[^*]+\*\*)', text)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        # Texte en gras
                        bold_text = part[2:-2]
                        children.append({"text": bold_text, "type": "text", "bold": True})
                    elif part:
                        children.append({"text": part, "type": "text"})
                blocks.append({
                    "type": "paragraph",
                    "children": children if children else [{"text": para, "type": "text"}]
                })
            else:
                # Paragraphe normal
                blocks.append({
                    "type": "paragraph",
                    "children": [{"text": para, "type": "text"}]
                })
        
        return blocks if blocks else [{"type": "paragraph", "children": [{"text": markdown_text, "type": "text"}]}]
    
    def calculate_coin_reward(self, question_count: int) -> int:
        """Calcule les coins selon le nombre de questions"""
        if question_count <= 3:
            return 150
        elif question_count <= 5:
            return 200
        elif question_count == 6:
            return 250
        elif question_count == 7:
            return 300
        elif question_count >= 8:
            return 350
        return 150  # default
    
    def generate_lessons(
        self, 
        section_title: str,
        chapter_title: str,
        lessons_input: List[Dict[str, Any]],
        reference_docs: List[str],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Génère le contenu des leçons via OpenAI"""
        
        print("📚 Lecture des documents de référence...")
        reference_content = self.read_reference_documents(reference_docs)
        
        if not reference_content:
            print("⚠️  Aucun document de référence trouvé")
        
        # Construire le prompt système
        system_prompt = """Tu es un expert en création de contenu pédagogique financier pour une application mobile Finsly.

TÂCHE :
Générer des leçons complètes selon le format Strapi exact, en te basant sur les documents de référence fournis.

FORMAT STRAPI REQUIS :
- Chaque leçon a un `title`, `description` (Rich Text Blocks array), `order`, `difficulty` ("easy"|"medium"|"hard")
- `lessonType` : TOUJOURS "quizz"
- `estimatedDuration` : en minutes (10-15 minutes par leçon)
- `coinReward` : calculé selon nombre de questions (2-3=150, 4-5=200, 6=250, 7=300, 8=350)
- `content` : array de blocks (text-blocks ET quiz-blocks mélangés)

STRUCTURE CONTENT :
- `text-blocks` : Array avec `__component: "lesson-content.text-block"`, `title` (ex: "Page 1"), `content` (Rich Text Blocks), `highlight: false`
- `quiz-blocks` : Array avec `__component: "lesson-content.quizz-block"`, `Question` (string), `questionType` (enum), `options` (Rich Text Blocks array), `correctAnswer` (string), `explanationcorrect` (Rich Text Blocks), `explanationfalse` (Rich Text Blocks), `points: 5`

RÈGLES IMPORTANTES :
- Ton : "tu", "ton", accessible et humain (comme dans les exemples)
- Niveau : Débutant, explications claires
- Questions : 6-8 questions par leçon avec feedback détaillé
- Contenu : Progressif, pédagogique, avec exemples concrets
- Format Markdown : Pour le contenu des text-blocks (sera converti en Rich Text)
- Options de quiz : Array de strings simples (sera converti en Rich Text Blocks)
- Rich Text Blocks : Format [{"type": "paragraph", "children": [{"text": "...", "type": "text"}]}]

Retourne UNIQUEMENT du JSON valide, sans markdown, sans code blocks."""
        
        # Construire le prompt utilisateur
        user_prompt = f"""
DOCUMENTS DE RÉFÉRENCE :
{reference_content[:15000]}

TÂCHE :
Générer des leçons pour la section "{section_title}", chapitre "{chapter_title}"

STRUCTURE DES LEÇONS DEMANDÉES :
{json.dumps(lessons_input, indent=2, ensure_ascii=False)}

Génère le contenu complet au format JSON suivant (exemple) :
{{
  "chapterTitle": "{chapter_title}",
  "lessons": [
    {{
      "title": "Titre de la leçon",
      "description": [
        {{"type": "paragraph", "children": [{{"text": "Description courte de la leçon", "type": "text"}}]}}
      ],
      "order": 1,
      "difficulty": "easy",
      "estimatedDuration": 12,
      "content": {{
        "textBlocks": [
          {{
            "title": "Page 1",
            "content": "# Titre\\n\\nContenu en Markdown avec **gras** et paragraphes..."
          }},
          {{
            "title": "Page 2",
            "content": "Plus de contenu..."
          }}
        ],
        "quizBlocks": [
          {{
            "Question": "Texte de la question ?",
            "questionType": "multiple-choice",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correctAnswer": "Option 2",
            "explanationcorrect": "Bonne réponse ! Explication détaillée...",
            "explanationfalse": "Mauvaise réponse. Explication...",
            "points": 5
          }}
        ]
      }}
    }}
  ]
}}

IMPORTANT :
- Utilise le même ton que les documents de référence ("tu", "ton", accessible)
- 6-8 questions par leçon avec feedback détaillé
- Contenu progressif et pédagogique
- Format Markdown pour les text-blocks (sera converti en Rich Text)
- Options de quiz : array de strings simples
- Rich Text Blocks pour descriptions et explications : format [{{"type": "paragraph", "children": [{{"text": "...", "type": "text"}}]}}]
- Génère des slugs à partir des titres (minuscules, tirets)
"""
        
        print("🤖 Génération du contenu via OpenAI...")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # ou "gpt-4" selon disponibilité
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            generated_content = json.loads(response.choices[0].message.content)
            
            # Post-process: Convert markdown to Rich Text Blocks and calculate coin rewards
            for lesson in generated_content.get("lessons", []):
                content = lesson.get("content", {})
                
                # Convert text blocks markdown to Rich Text
                for tb in content.get("textBlocks", []):
                    if isinstance(tb.get("content"), str):
                        tb["content"] = self.convert_markdown_to_richtext(tb["content"])
                
                # Convert quiz options to Rich Text Blocks
                quiz_count = 0
                for qb in content.get("quizBlocks", []):
                    quiz_count += 1
                    # Convert options array to Rich Text Blocks
                    if isinstance(qb.get("options"), list):
                        options_rt = []
                        for opt in qb["options"]:
                            if isinstance(opt, str):
                                options_rt.append({
                                    "type": "paragraph",
                                    "children": [{"text": opt, "type": "text"}]
                                })
                        qb["options"] = options_rt
                    
                    # Convert explanations to Rich Text Blocks if they're strings
                    for key in ["explanationcorrect", "explanationfalse"]:
                        if isinstance(qb.get(key), str):
                            qb[key] = self.convert_markdown_to_richtext(qb[key])
                
                # Calculate coin reward
                lesson["coinReward"] = self.calculate_coin_reward(quiz_count)
                lesson["lessonType"] = "quizz"  # Always "quizz"
                lesson["isActive"] = True
                
                # Generate slug if not present
                if "slug" not in lesson:
                    lesson["slug"] = self._generate_slug(lesson["title"])
            
            # Sauvegarder si output_path fourni
            if output_path:
                os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(generated_content, f, indent=2, ensure_ascii=False)
                print(f"✅ Contenu généré sauvegardé dans : {output_path}")
            
            return generated_content
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération : {e}")
            raise
    
    def _generate_slug(self, title: str) -> str:
        """Génère un slug à partir d'un titre"""
        slug = title.lower()
        slug = re.sub(r'[àáâãäå]', 'a', slug)
        slug = re.sub(r'[èéêë]', 'e', slug)
        slug = re.sub(r'[ìíîï]', 'i', slug)
        slug = re.sub(r'[òóôõö]', 'o', slug)
        slug = re.sub(r'[ùúûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    def find_section_by_title(self, title: str) -> Optional[Dict]:
        """Trouve une section existante par titre"""
        try:
            response = requests.get(
                f"{self.strapi_url}/api/sections",
                headers={
                    "Authorization": f"Bearer {self.strapi_token}",
                    "Content-Type": "application/json"
                },
                params={"filters[title][$eq]": title},
                timeout=30
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            return data[0] if data else None
        except Exception as e:
            print(f"⚠️  Erreur lors de la recherche de section : {e}")
            return None
    
    def find_chapter_by_title(self, title: str, section_id: int) -> Optional[Dict]:
        """Trouve un chapitre existant par titre dans une section"""
        try:
            response = requests.get(
                f"{self.strapi_url}/api/chapters",
                headers={
                    "Authorization": f"Bearer {self.strapi_token}",
                    "Content-Type": "application/json"
                },
                params={
                    "filters[title][$eq]": title,
                    "filters[section][id][$eq]": section_id
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            return data[0] if data else None
        except Exception as e:
            print(f"⚠️  Erreur lors de la recherche de chapitre : {e}")
            return None
    
    def create_in_strapi(
        self, 
        section_title: str,
        chapter_title: str,
        content: Dict,
        attach_to_existing_chapter: bool = False
    ) -> Dict[str, Any]:
        """Crée les leçons dans Strapi en les attachant à une section/chapitre existant"""
        results = {
            "section_id": None,
            "chapter_id": None,
            "lesson_ids": [],
            "errors": []
        }
        
        # 1. Trouver la section existante
        print(f"\n🔍 Recherche de la section : {section_title}")
        section = self.find_section_by_title(section_title)
        if not section:
            results["errors"].append(f"Section '{section_title}' non trouvée")
            print(f"❌ Section '{section_title}' non trouvée")
            return results
        
        results["section_id"] = section["id"]
        print(f"✅ Section trouvée : ID {results['section_id']}")
        
        # 2. Trouver ou créer le chapitre
        print(f"\n🔍 Recherche du chapitre : {chapter_title}")
        chapter = self.find_chapter_by_title(chapter_title, results["section_id"])
        
        if chapter:
            results["chapter_id"] = chapter["id"]
            print(f"✅ Chapitre existant trouvé : ID {results['chapter_id']}")
        elif not attach_to_existing_chapter:
            # Créer le chapitre
            print(f"📝 Création du chapitre : {chapter_title}")
            chapter_data = {
                "data": {
                    "title": chapter_title,
                    "description": [{"type": "paragraph", "children": [{"text": f"Chapitre : {chapter_title}", "type": "text"}]}],
                    "order": 1,  # TODO: calculer l'order correct
                    "section": results["section_id"],
                    "isActive": True,
                    "estimatedDuration": sum(
                        lesson.get("estimatedDuration", 15) 
                        for lesson in content.get("lessons", [])
                    )
                }
            }
            
            try:
                response = requests.post(
                    f"{self.strapi_url}/api/chapters",
                    json=chapter_data,
                    headers={
                        "Authorization": f"Bearer {self.strapi_token}",
                        "Content-Type": "application/json"
                    },
                    timeout=30
                )
                response.raise_for_status()
                results["chapter_id"] = response.json()["data"]["id"]
                print(f"✅ Chapitre créé : ID {results['chapter_id']}")
            except Exception as e:
                error_msg = f"Erreur création chapitre: {e}"
                results["errors"].append(error_msg)
                print(f"❌ {error_msg}")
                return results
        else:
            results["errors"].append(f"Chapitre '{chapter_title}' non trouvé et création désactivée")
            print(f"❌ Chapitre '{chapter_title}' non trouvé")
            return results
        
        # 3. Créer les leçons
        print(f"\n📚 Création des leçons...")
        for idx, lesson in enumerate(content.get("lessons", []), 1):
            print(f"  Leçon {idx}: {lesson.get('title', 'Sans titre')}")
            
            # Construire le content array (dynamic zone)
            content_blocks = []
            
            # Ajouter les text-blocks
            for tb in lesson.get("content", {}).get("textBlocks", []):
                content_blocks.append({
                    "__component": "lesson-content.text-block",
                    "title": tb.get("title", f"Page {len([b for b in content_blocks if b.get('__component') == 'lesson-content.text-block']) + 1}"),
                    "content": tb.get("content", []),
                    "highlight": tb.get("highlight", False)
                })
            
            # Ajouter les quiz-blocks
            for qb in lesson.get("content", {}).get("quizBlocks", []):
                content_blocks.append({
                    "__component": "lesson-content.quizz-block",
                    "Question": qb.get("Question", ""),
                    "questionType": qb.get("questionType", "multiple-choice"),
                    "options": qb.get("options", []),
                    "correctAnswer": qb.get("correctAnswer", ""),
                    "explanationcorrect": qb.get("explanationcorrect", []),
                    "explanationfalse": qb.get("explanationfalse", []),
                    "points": qb.get("points", 5)
                })
            
            lesson_data = {
                "data": {
                    "title": lesson["title"],
                    "description": lesson.get("description", []),
                    "order": lesson.get("order", idx),
                    "chapter": results["chapter_id"],
                    "lessonType": lesson.get("lessonType", "quizz"),
                    "content": content_blocks,
                    "isActive": lesson.get("isActive", True),
                    "estimatedDuration": lesson.get("estimatedDuration", 15),
                    "coinReward": lesson.get("coinReward", 150),
                    "slug": lesson.get("slug", self._generate_slug(lesson["title"])),
                    "difficulty": lesson.get("difficulty", "easy"),
                    "tags": lesson.get("tags")
                }
            }
            
            try:
                response = requests.post(
                    f"{self.strapi_url}/api/lessons",
                    json=lesson_data,
                    headers={
                        "Authorization": f"Bearer {self.strapi_token}",
                        "Content-Type": "application/json"
                    },
                    timeout=30
                )
                response.raise_for_status()
                lesson_id = response.json()["data"]["id"]
                results["lesson_ids"].append(lesson_id)
                print(f"    ✅ Leçon créée : ID {lesson_id}")
            except Exception as e:
                error_msg = f"Erreur création leçon '{lesson.get('title')}': {e}"
                results["errors"].append(error_msg)
                print(f"    ❌ {error_msg}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"       Response: {e.response.text[:500]}")
        
        return results


def load_lessons_input(file_path: str) -> List[Dict[str, Any]]:
    """Charge la structure des leçons depuis un fichier JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Support both direct array and object with "lessons" key
        if isinstance(data, list):
            return data
        return data.get("lessons", [])


def main():
    parser = argparse.ArgumentParser(description='Génère des leçons et les crée dans Strapi')
    parser.add_argument('--section', required=True, help='Titre de la section existante')
    parser.add_argument('--chapter', required=True, help='Titre du chapitre (existant ou à créer)')
    parser.add_argument('--lessons', required=True, help='Fichier JSON avec la structure des leçons')
    parser.add_argument('--reference', nargs='+', default=[], help='Documents de référence (Markdown)')
    parser.add_argument('--output', default='output/generated-content.json', help='Fichier de sortie')
    parser.add_argument('--create', action='store_true', help='Créer directement dans Strapi après génération')
    parser.add_argument('--input', help='Fichier JSON à charger (au lieu de générer)')
    parser.add_argument('--attach-only', action='store_true', help='Attacher uniquement à un chapitre existant (ne pas créer)')
    
    args = parser.parse_args()
    
    # Variables d'environnement
    openai_key = os.getenv("OPENAI_API_KEY")
    strapi_url = os.getenv("STRAPI_URL", "https://cms.finsly.org")
    strapi_token = os.getenv("STRAPI_API_TOKEN")
    
    if not openai_key and not args.input:
        print("❌ OPENAI_API_KEY non définie dans les variables d'environnement")
        return
    
    if not strapi_token:
        print("❌ STRAPI_API_TOKEN non définie dans les variables d'environnement")
        return
    
    # Initialiser l'agent
    agent = LessonGeneratorAgent(openai_key or "dummy", strapi_url, strapi_token)
    
    # Charger ou générer le contenu
    if args.input:
        print(f"📂 Chargement du contenu depuis : {args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            generated_content = json.load(f)
    else:
        # Charger la structure des leçons
        print(f"📂 Chargement de la structure : {args.lessons}")
        lessons_input = load_lessons_input(args.lessons)
        
        # Documents de référence par défaut
        reference_docs = args.reference if args.reference else [
            "docs/cours-bourse-v1.md",
            "docs/cours-lois-reglementations-v1.md"
        ]
        
        # Générer le contenu
        generated_content = agent.generate_lessons(
            section_title=args.section,
            chapter_title=args.chapter,
            lessons_input=lessons_input,
            reference_docs=reference_docs,
            output_path=args.output
        )
    
    # Créer dans Strapi si demandé
    if args.create:
        print("\n" + "="*50)
        print("🚀 CRÉATION DANS STRAPI")
        print("="*50)
        validation = input("\n⚠️  Valider et créer dans Strapi ? (oui/non): ")
        
        if validation.lower() in ['oui', 'o', 'yes', 'y']:
            results = agent.create_in_strapi(
                section_title=args.section,
                chapter_title=args.chapter,
                content=generated_content,
                attach_to_existing_chapter=args.attach_only
            )
            
            print("\n" + "="*50)
            print("📊 RÉSULTATS")
            print("="*50)
            print(f"Section ID: {results['section_id']}")
            print(f"Chapitre ID: {results['chapter_id']}")
            print(f"Leçons créées: {len(results['lesson_ids'])}")
            if results['errors']:
                print(f"\n⚠️  Erreurs: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"  - {error}")
        else:
            print("❌ Création annulée")
    else:
        print(f"\n✅ Contenu généré. Vérifie le fichier : {args.output}")
        print("💡 Pour créer dans Strapi, relance avec --create")


if __name__ == "__main__":
    main()
