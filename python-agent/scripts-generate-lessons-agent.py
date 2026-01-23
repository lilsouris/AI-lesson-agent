#!/usr/bin/env python3
"""
Agent AI pour générer des leçons et les créer dans Strapi CMS

Usage:
    python scripts/generate-lessons-agent.py --section "Titre Section" --chapters chapters.json
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from openai import OpenAI


class LessonGeneratorAgent:
    """Agent AI pour générer des leçons pédagogiques"""
    
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
    
    def generate_lessons(
        self, 
        section_title: str,
        chapters_topics: List[Dict[str, Any]],
        reference_docs: List[str],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Génère le contenu des leçons via OpenAI"""
        
        print("📚 Lecture des documents de référence...")
        reference_content = self.read_reference_documents(reference_docs)
        
        if not reference_content:
            print("⚠️  Aucun document de référence trouvé")
        
        # Construire le prompt système
        system_prompt = """Tu es un expert en création de contenu pédagogique financier pour une application mobile.

TÂCHE :
Générer des leçons complètes selon le format établi, en te basant sur les documents de référence fournis.

FORMAT REQUIS :
- Section avec title, description (Rich Text Blocks), order, icon, difficulty
- Chapitres avec title, description, order, lessons (array)
- Leçons avec title, description, content (textBlocks + quizBlocks), estimatedDuration, coinReward, difficulty, slug

RÈGLES :
- Ton : "tu", "ton", accessible et humain
- Niveau : Débutant, explications claires
- Questions : 6-8 questions par leçon avec feedback détaillé
- Contenu : Progressif, pédagogique, avec exemples concrets
- Format Markdown : Pour le contenu des text-blocks

Retourne UNIQUEMENT du JSON valide, sans markdown, sans code blocks."""
        
        # Construire le prompt utilisateur
        user_prompt = f"""
DOCUMENTS DE RÉFÉRENCE :
{reference_content[:10000]}  # Limiter pour éviter les tokens excessifs

TÂCHE :
Générer une section complète avec chapitres et leçons pour : "{section_title}"

STRUCTURE DEMANDÉE :
{json.dumps(chapters_topics, indent=2, ensure_ascii=False)}

Génère le contenu complet au format JSON suivant (exemple) :
{{
  "section": {{
    "title": "{section_title}",
    "description": [{{"type": "paragraph", "children": [{{"text": "Description de la section"}}]}}],
    "order": 1,
    "icon": "icon-name",
    "difficulty": "beginner",
    "isActive": true
  }},
  "chapters": [
    {{
      "title": "Titre du chapitre",
      "description": [{{"type": "paragraph", "children": [{{"text": "Description"}}]}}],
      "order": 1,
      "isActive": true,
      "lessons": [
        {{
          "title": "Titre de la leçon",
          "description": [{{"type": "paragraph", "children": [{{"text": "Description courte"}}]}}],
          "order": 1,
          "content": {{
            "textBlocks": [
              {{
                "title": "Titre optionnel",
                "content": "# Contenu en Markdown\\n\\nTexte du cours...",
                "highlight": false
              }}
            ],
            "quizBlocks": [
              {{
                "questions": [
                  {{
                    "questionType": "multiple-choice",
                    "question": "Texte de la question ?",
                    "options": ["a) Option 1", "b) Option 2", "c) Option 3", "d) Option 4"],
                    "correctAnswer": "b) Option 2",
                    "explanationcorrect": "Bonne réponse ! Explication détaillée...",
                    "explanationfalse": "Mauvaise réponse. Explication...",
                    "reward": 10
                  }}
                ]
              }}
            ]
          }},
          "estimatedDuration": 15,
          "coinReward": 50,
          "difficulty": "beginner",
          "slug": "titre-lecon-slug",
          "isActive": true
        }}
      ]
    }}
  ]
}}

IMPORTANT :
- Utilise le même ton que les documents de référence
- 6-8 questions par leçon avec feedback détaillé
- Contenu progressif et pédagogique
- Format Markdown pour les text-blocks (sera converti en Rich Text)
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
    
    def convert_markdown_to_richtext(self, markdown_text: str) -> List[Dict]:
        """Convertit Markdown en format Rich Text Blocks de Strapi (simplifié)"""
        blocks = []
        
        # Parser simple par paragraphes
        paragraphs = markdown_text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Détecter les titres
            if para.startswith('#'):
                level = len(para) - len(para.lstrip('#'))
                text = para.lstrip('#').strip()
                blocks.append({
                    "type": f"heading-{min(level, 6)}",
                    "children": [{"text": text}]
                })
            else:
                blocks.append({
                    "type": "paragraph",
                    "children": [{"text": para}]
                })
        
        return blocks if blocks else [{"type": "paragraph", "children": [{"text": markdown_text}]}]
    
    def create_in_strapi(self, content: Dict) -> Dict[str, Any]:
        """Crée les entités dans Strapi via API"""
        results = {
            "section_id": None,
            "chapter_ids": [],
            "lesson_ids": [],
            "errors": []
        }
        
        # 1. Créer la Section
        print("\n📦 Création de la Section...")
        section_data = {
            "data": {
                "title": content["section"]["title"],
                "description": content["section"]["description"],
                "order": content["section"].get("order", 1),
                "icon": content["section"].get("icon", ""),
                "difficulty": content["section"].get("difficulty", "beginner"),
                "isActive": content["section"].get("isActive", True)
            }
        }
        
        try:
            response = requests.post(
                f"{self.strapi_url}/api/sections",
                json=section_data,
                headers={
                    "Authorization": f"Bearer {self.strapi_token}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            response.raise_for_status()
            results["section_id"] = response.json()["data"]["id"]
            print(f"✅ Section créée : ID {results['section_id']}")
        except Exception as e:
            error_msg = f"Erreur création section: {e}"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return results
        
        # 2. Créer les Chapitres
        print("\n📚 Création des Chapitres...")
        for idx, chapter in enumerate(content.get("chapters", []), 1):
            print(f"  Chapitre {idx}: {chapter.get('title', 'Sans titre')}")
            
            chapter_data = {
                "data": {
                    "title": chapter["title"],
                    "description": chapter.get("description", []),
                    "order": chapter.get("order", idx),
                    "section": results["section_id"],
                    "isActive": chapter.get("isActive", True),
                    "estimatedDuration": sum(
                        lesson.get("estimatedDuration", 15) 
                        for lesson in chapter.get("lessons", [])
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
                chapter_id = response.json()["data"]["id"]
                results["chapter_ids"].append(chapter_id)
                print(f"    ✅ Chapitre créé : ID {chapter_id}")
                
                # 3. Créer les Leçons
                for lesson_idx, lesson in enumerate(chapter.get("lessons", []), 1):
                    print(f"      Leçon {lesson_idx}: {lesson.get('title', 'Sans titre')}")
                    
                    # Convertir les text blocks
                    text_blocks = []
                    for tb in lesson.get("content", {}).get("textBlocks", []):
                        text_blocks.append({
                            "__component": "lesson.text-block",
                            "title": tb.get("title"),
                            "content": self.convert_markdown_to_richtext(tb.get("content", "")),
                            "highlight": tb.get("highlight", False)
                        })
                    
                    # Créer les quiz blocks
                    quiz_blocks = []
                    for qb in lesson.get("content", {}).get("quizBlocks", []):
                        quiz_blocks.append({
                            "__component": "lesson.quiz-block",
                            "questions": qb.get("questions", [])
                        })
                    
                    lesson_data = {
                        "data": {
                            "title": lesson["title"],
                            "description": lesson.get("description", []),
                            "order": lesson.get("order", lesson_idx),
                            "chapter": chapter_id,
                            "lessonType": "course",
                            "content": text_blocks + quiz_blocks,
                            "isActive": lesson.get("isActive", True),
                            "estimatedDuration": lesson.get("estimatedDuration", 15),
                            "coinReward": lesson.get("coinReward", 50),
                            "slug": lesson.get("slug", self._generate_slug(lesson["title"])),
                            "difficulty": lesson.get("difficulty", "beginner"),
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
                        print(f"        ✅ Leçon créée : ID {lesson_id}")
                    except Exception as e:
                        error_msg = f"Erreur création leçon '{lesson.get('title')}': {e}"
                        results["errors"].append(error_msg)
                        print(f"        ❌ {error_msg}")
                        
            except Exception as e:
                error_msg = f"Erreur création chapitre '{chapter.get('title')}': {e}"
                results["errors"].append(error_msg)
                print(f"    ❌ {error_msg}")
        
        return results
    
    def _generate_slug(self, title: str) -> str:
        """Génère un slug à partir d'un titre"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug


def load_chapters_from_file(file_path: str) -> List[Dict[str, Any]]:
    """Charge la structure des chapitres depuis un fichier JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Génère des leçons et les crée dans Strapi')
    parser.add_argument('--section', required=True, help='Titre de la section')
    parser.add_argument('--chapters', required=True, help='Fichier JSON avec la structure des chapitres')
    parser.add_argument('--reference', nargs='+', default=[], help='Documents de référence (Markdown)')
    parser.add_argument('--output', default='output/generated-content.json', help='Fichier de sortie')
    parser.add_argument('--create', action='store_true', help='Créer directement dans Strapi après génération')
    parser.add_argument('--input', help='Fichier JSON à charger (au lieu de générer)')
    
    args = parser.parse_args()
    
    # Variables d'environnement
    openai_key = os.getenv("OPENAI_API_KEY")
    strapi_url = os.getenv("STRAPI_URL", "https://cms.finsly.org")
    strapi_token = os.getenv("STRAPI_API_TOKEN")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY non définie dans les variables d'environnement")
        return
    
    if not strapi_token:
        print("❌ STRAPI_API_TOKEN non définie dans les variables d'environnement")
        return
    
    # Initialiser l'agent
    agent = LessonGeneratorAgent(openai_key, strapi_url, strapi_token)
    
    # Charger ou générer le contenu
    if args.input:
        print(f"📂 Chargement du contenu depuis : {args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            generated_content = json.load(f)
    else:
        # Charger la structure des chapitres
        print(f"📂 Chargement de la structure : {args.chapters}")
        chapters_topics = load_chapters_from_file(args.chapters)
        
        # Documents de référence par défaut
        reference_docs = args.reference if args.reference else [
            "docs/cours-bourse-v1.md",
            "docs/cours-lois-reglementations-v1.md"
        ]
        
        # Générer le contenu
        generated_content = agent.generate_lessons(
            section_title=args.section,
            chapters_topics=chapters_topics,
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
            results = agent.create_in_strapi(generated_content)
            
            print("\n" + "="*50)
            print("📊 RÉSULTATS")
            print("="*50)
            print(f"Section ID: {results['section_id']}")
            print(f"Chapitres créés: {len(results['chapter_ids'])}")
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
