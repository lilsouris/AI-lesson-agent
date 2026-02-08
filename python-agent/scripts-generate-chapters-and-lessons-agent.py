#!/usr/bin/env python3
"""
Agent AI pour générer des chapitres ET des leçons et les créer dans Strapi CMS

Usage:
    # Générer des chapitres automatiquement (sans spécifier de chapitre)
    python scripts-generate-chapters-and-lessons-agent.py --section "Les bases" --generate-chapters 3

    # Générer un chapitre spécifique avec des leçons
    python scripts-generate-chapters-and-lessons-agent.py --section "Les bases" --chapter "Nouveau chapitre" --lessons lessons-input.json
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from openai import OpenAI


def _rt_paragraph(text: str) -> Dict:
    """One Rich Text paragraph block."""
    return {"type": "paragraph", "children": [{"text": text, "type": "text"}]}


def _ensure_explanation_rt(agent: "ChapterAndLessonGeneratorAgent", val: Any) -> List[Dict]:
    """Ensure explanation is always a list of Rich Text blocks (never null for Strapi)."""
    if val is None:
        return []
    if isinstance(val, str):
        return agent.convert_markdown_to_richtext(val)
    if isinstance(val, list):
        return val
    return []


class ChapterAndLessonGeneratorAgent:
    """Agent AI pour générer des chapitres et des leçons selon le format Strapi exact"""
    
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
    
    def get_existing_chapters(self, section_id: int) -> List[Dict]:
        """Récupère tous les chapitres existants d'une section"""
        try:
            response = requests.get(
                f"{self.strapi_url}/api/chapters",
                headers={
                    "Authorization": f"Bearer {self.strapi_token}",
                    "Content-Type": "application/json"
                },
                params={
                    "filters[section][id][$eq]": section_id,
                    "pagination[pageSize]": 100,
                    "sort": "order:asc"
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération des chapitres : {e}")
            return []
    
    def generate_chapter_suggestions(
        self,
        section_title: str,
        existing_chapters: List[Dict],
        num_chapters: int,
        reference_docs: List[str]
    ) -> List[Dict[str, Any]]:
        """Génère des suggestions de nouveaux chapitres en continuité avec l'existant"""
        
        print(f"🤖 Génération de {num_chapters} suggestions de chapitres...")
        
        # Construire le contexte des chapitres existants
        existing_context = ""
        if existing_chapters:
            existing_context = "CHAPITRES EXISTANTS DANS CETTE SECTION :\n"
            for i, ch in enumerate(existing_chapters, 1):
                existing_context += f"{i}. {ch['title']} (order: {ch.get('order', 'N/A')})\n"
                if ch.get('description'):
                    desc_text = ""
                    for block in ch.get('description', []):
                        if block.get('type') == 'paragraph':
                            for child in block.get('children', []):
                                if child.get('type') == 'text':
                                    desc_text += child.get('text', '')
                    if desc_text:
                        existing_context += f"   Description: {desc_text}\n"
        else:
            existing_context = "Aucun chapitre existant dans cette section.\n"
        
        # Lire les documents de référence
        reference_content = self.read_reference_documents(reference_docs)
        
        system_prompt = """Tu es un expert en création de contenu pédagogique financier pour une application mobile Finsly.

TÂCHE :
Générer des suggestions de nouveaux chapitres qui s'intègrent naturellement dans la continuité des chapitres existants d'une section.

RÈGLES :
- Les chapitres doivent suivre une progression logique
- Chaque chapitre doit avoir un titre clair et descriptif
- Chaque chapitre doit avoir une description courte (1-2 phrases)
- Les chapitres doivent être cohérents avec le thème de la section
- Propose des chapitres qui approfondissent ou complètent les chapitres existants

Retourne UNIQUEMENT du JSON valide."""
        
        user_prompt = f"""
SECTION : "{section_title}"

{existing_context}

DOCUMENTS DE RÉFÉRENCE :
{reference_content[:10000]}

TÂCHE :
Génère {num_chapters} suggestions de nouveaux chapitres qui s'intègrent naturellement dans la continuité de cette section.

Format JSON :
{{
  "chapters": [
    {{
      "title": "Titre du chapitre",
      "description": "Description courte du chapitre (1-2 phrases)",
      "order": 6,
      "suggestedLessons": [
        {{
          "title": "Titre de la leçon suggérée",
          "description": "Description courte",
          "order": 1,
          "difficulty": "easy"
        }}
      ]
    }}
  ]
}}

IMPORTANT :
- Les titres doivent être clairs et descriptifs
- Les descriptions doivent être courtes (1-2 phrases)
- L'order doit suivre logiquement les chapitres existants
- Propose 2-3 leçons suggérées par chapitre
- Les chapitres doivent être progressifs (du plus simple au plus complexe)
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,  # Plus créatif pour les suggestions
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("chapters", [])
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des suggestions : {e}")
            raise
    
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
                heading_type = f"heading-{min(level, 6)}"
                blocks.append({
                    "type": heading_type,
                    "children": [{"text": text, "type": "text"}]
                })
            # Détecter le gras **text**
            elif '**' in para:
                text = para
                children = []
                parts = re.split(r'(\*\*[^*]+\*\*)', text)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        bold_text = part[2:-2]
                        children.append({"text": bold_text, "type": "text", "bold": True})
                    elif part:
                        children.append({"text": part, "type": "text"})
                blocks.append({
                    "type": "paragraph",
                    "children": children if children else [{"text": para, "type": "text"}]
                })
            else:
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
        return 150
    
    def generate_lessons_for_chapter(
        self,
        section_title: str,
        chapter_title: str,
        chapter_description: str,
        lessons_input: List[Dict[str, Any]],
        reference_docs: List[str]
    ) -> Dict[str, Any]:
        """Génère le contenu des leçons pour un chapitre"""
        
        print(f"📚 Génération des leçons pour le chapitre : {chapter_title}")
        reference_content = self.read_reference_documents(reference_docs)
        
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
- Ton : "tu", "ton", accessible et humain
- Niveau : Débutant, explications claires
- Questions : 6-8 questions par leçon avec feedback détaillé
- Contenu : Progressif, pédagogique, avec exemples concrets
- Format Markdown : Pour le contenu des text-blocks (sera converti en Rich Text)
- Options de quiz : Array de strings simples (sera converti en Rich Text Blocks)
- Types de quiz : multiple-choice, true-false, matching, drag-order, drag-drop
  - multiple-choice / true-false : options = liste de réponses, correctAnswer = texte exact de la bonne réponse
  - matching : options = lignes A/1/B/2/C/3/..., correctAnswer = "A → 1, B → 2, C → 3, ..."
  - drag-order : options = liste des éléments à classer (ordre aléatoire), correctAnswer = même liste dans le bon ordre, séparée par des virgules
  - drag-drop (phrase à trous) : options = liste des mots à glisser (dont distracteurs), correctAnswer = phrase complète avec les trous remplis
- Rich Text Blocks : Format [{"type": "paragraph", "children": [{"text": "...", "type": "text"}]}]

Retourne UNIQUEMENT du JSON valide."""
        
        user_prompt = f"""
DOCUMENTS DE RÉFÉRENCE :
{reference_content[:15000]}

CONTEXTE :
Section : "{section_title}"
Chapitre : "{chapter_title}"
Description du chapitre : "{chapter_description}"

TÂCHE :
Générer des leçons complètes pour ce chapitre.

STRUCTURE DES LEÇONS DEMANDÉES :
{json.dumps(lessons_input, indent=2, ensure_ascii=False)}

Génère le contenu complet au format JSON suivant :
{{
  "lessons": [
    {{
      "title": "Titre de la leçon",
      "description": [
        {{"type": "paragraph", "children": [{{"text": "Description courte", "type": "text"}}]}}
      ],
      "order": 1,
      "difficulty": "easy",
      "estimatedDuration": 12,
      "content": {{
        "textBlocks": [
          {{
            "title": "Page 1",
            "content": "# Titre\\n\\nContenu en Markdown avec **gras**..."
          }}
        ],
        "quizBlocks": [
          {{
            "Question": "Texte de la question ?",
            "questionType": "multiple-choice",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correctAnswer": "Option 2",
            "explanationcorrect": "Bonne réponse ! Explication...",
            "explanationfalse": "Mauvaise réponse. Explication...",
            "points": 5
          }}
        ]
      }}
    }}
  ]
}}

IMPORTANT :
- Utilise le même ton que les documents de référence
- 6-8 questions par leçon avec feedback détaillé
- Contenu progressif et pédagogique
- Format Markdown pour les text-blocks
- Options de quiz : array de strings (une par option). Pour drag-order/drag-drop/matching, respecte le format correctAnswer indiqué dans le prompt système.
- explanationcorrect et explanationfalse : toujours des strings (sera converti en Rich Text)
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
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
                
                # Quiz blocks: format Strapi (ref. "L'inflation, ton ennemi silencieux")
                # options = Rich Text array; matching = 1 bloc avec \n; drag-order/drag-drop = 1 RT par item
                quiz_count = 0
                for qb in content.get("quizBlocks", []):
                    quiz_count += 1
                    qtype = (qb.get("questionType") or "multiple-choice").strip().lower()
                    qb["questionType"] = qtype

                    opts = qb.get("options")
                    if opts is None or not isinstance(opts, list):
                        qb["options"] = []
                    else:
                        if qtype == "matching":
                            lines = [o if isinstance(o, str) else str(o) for o in opts]
                            qb["options"] = [_rt_paragraph("\n".join(lines))]
                        else:
                            options_rt = []
                            for opt in opts:
                                if isinstance(opt, dict) and opt.get("type") == "paragraph":
                                    options_rt.append(opt)
                                else:
                                    options_rt.append(_rt_paragraph(opt if isinstance(opt, str) else str(opt)))
                            qb["options"] = options_rt

                    for key in ["explanationcorrect", "explanationfalse"]:
                        qb[key] = _ensure_explanation_rt(self, qb.get(key))
                
                lesson["coinReward"] = self.calculate_coin_reward(quiz_count)
                lesson["lessonType"] = "quizz"
                lesson["isActive"] = True
                
                if "slug" not in lesson:
                    lesson["slug"] = self._generate_slug(lesson["title"])
            
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
    
    def _section_title(self, item: Dict) -> str:
        """Extrait le titre d'une section (Strapi v4 peut mettre les champs dans attributes)."""
        if item.get("title"):
            return item["title"]
        return (item.get("attributes") or {}).get("title") or ""

    def _chapter_title(self, item: Dict) -> str:
        """Extrait le titre d'un chapitre (Strapi v4 peut mettre les champs dans attributes)."""
        if item.get("title"):
            return item["title"]
        return (item.get("attributes") or {}).get("title") or ""

    def _chapter_order(self, item: Dict) -> int:
        """Extrait l'ordre d'un chapitre pour le tri."""
        o = item.get("order")
        if o is not None:
            return int(o)
        return int((item.get("attributes") or {}).get("order", 0))

    def find_section_by_title(self, title: str) -> Optional[Dict]:
        """Trouve une section existante par titre (gère pagination et structure Strapi v4)."""
        headers = {
            "Authorization": f"Bearer {self.strapi_token}",
            "Content-Type": "application/json"
        }
        try:
            # 1) Essai avec filtre
            response = requests.get(
                f"{self.strapi_url}/api/sections",
                headers=headers,
                params={
                    "filters[title][$eq]": title,
                    "pagination[pageSize]": 100
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json().get("data") or []
            if isinstance(data, list) and data:
                return data[0]
            # 2) Fallback : récupérer toutes les sections et chercher par titre
            response = requests.get(
                f"{self.strapi_url}/api/sections",
                headers=headers,
                params={"pagination[pageSize]": 100},
                timeout=30
            )
            response.raise_for_status()
            data = response.json().get("data") or []
            if not isinstance(data, list):
                return None
            title_stripped = (title or "").strip()
            for item in data:
                if self._section_title(item).strip() == title_stripped:
                    return item
            return None
        except Exception as e:
            print(f"⚠️  Erreur lors de la recherche de section : {e}")
            return None
    
    def create_in_strapi(
        self,
        section_title: str,
        chapters_data: List[Dict],
        attach_to_existing_chapters: bool = False
    ) -> Dict[str, Any]:
        """Crée les chapitres et leçons dans Strapi"""
        results = {
            "section_id": None,
            "chapter_ids": [],
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
        
        # Chapitres existants dans la section (pour matching par titre)
        existing_chapters = self.get_existing_chapters(results["section_id"])
        # Ordre des chapitres déjà traités dans ce run (pour chaînage prerequisiteChapters)
        previous_chapter_ids_in_run: List[int] = []
        
        # 2. Créer les chapitres et leurs leçons (liens section → chapitre, chapitre → leçon, prerequisiteChapters)
        for chapter_data in chapters_data:
            chapter_title = chapter_data.get("title", "Sans titre")
            print(f"\n📚 Traitement du chapitre : {chapter_title}")
            
            existing_chapter = next(
                (c for c in existing_chapters if self._chapter_title(c).strip() == chapter_title.strip()),
                None
            )
            
            if existing_chapter and attach_to_existing_chapters:
                chapter_id = existing_chapter["id"]
                previous_chapter_ids_in_run.append(chapter_id)
                print(f"✅ Utilisation du chapitre existant : ID {chapter_id}")
            else:
                if existing_chapter:
                    print(f"⚠️  Chapitre '{chapter_title}' existe déjà, création d'un nouveau...")
                
                # prerequisiteChapters = chapitres déjà traités dans ce run (chaînage 1 → 2 → 3)
                prerequisite_ids = list(previous_chapter_ids_in_run)
                desc = chapter_data.get("description", f"Chapitre : {chapter_title}")
                if isinstance(desc, str):
                    desc = self.convert_markdown_to_richtext(desc)
                chapter_payload = {
                    "data": {
                        "title": chapter_title,
                        "description": desc,
                        "order": chapter_data.get("order", len(previous_chapter_ids_in_run) + 1),
                        "section": results["section_id"],
                        "isActive": True,
                        "estimatedDuration": sum(
                            lesson.get("estimatedDuration", 15)
                            for lesson in chapter_data.get("lessons", [])
                        ),
                    }
                }
                if prerequisite_ids:
                    chapter_payload["data"]["prerequisiteChapters"] = {"connect": prerequisite_ids}
                
                try:
                    response = requests.post(
                        f"{self.strapi_url}/api/chapters",
                        json=chapter_payload,
                        headers={
                            "Authorization": f"Bearer {self.strapi_token}",
                            "Content-Type": "application/json"
                        },
                        timeout=30
                    )
                    response.raise_for_status()
                    chapter_id = response.json()["data"]["id"]
                    previous_chapter_ids_in_run.append(chapter_id)
                    print(f"✅ Chapitre créé : ID {chapter_id}" + (f" (prérequis: {prerequisite_ids})" if prerequisite_ids else ""))
                    # Strapi n'applique souvent pas les relations sur POST : on fait un PUT pour les prérequis
                    if prerequisite_ids:
                        try:
                            put_resp = requests.put(
                                f"{self.strapi_url}/api/chapters/{chapter_id}",
                                json={
                                    "data": {
                                        "prerequisiteChapters": {"connect": prerequisite_ids}
                                    }
                                },
                                headers={
                                    "Authorization": f"Bearer {self.strapi_token}",
                                    "Content-Type": "application/json"
                                },
                                timeout=30
                            )
                            put_resp.raise_for_status()
                            print(f"    ✅ Liens prerequisiteChapters mis à jour : {prerequisite_ids}")
                        except Exception as put_e:
                            results["errors"].append(f"prerequisiteChapters (chapitre {chapter_id}): {put_e}")
                            print(f"    ⚠️  prerequisiteChapters non mis à jour : {put_e}")
                except Exception as e:
                    error_msg = f"Erreur création chapitre '{chapter_title}': {e}"
                    results["errors"].append(error_msg)
                    print(f"❌ {error_msg}")
                    continue
            
            results["chapter_ids"].append(chapter_id)
            
            # 3. Créer les leçons du chapitre
            for idx, lesson in enumerate(chapter_data.get("lessons", []), 1):
                print(f"  📝 Leçon {idx}: {lesson.get('title', 'Sans titre')}")
                
                # Construire le content array (dynamic zone)
                content_blocks = []
                text_blocks = lesson.get("content", {}).get("textBlocks", [])
                
                # Ajouter les text-blocks
                for page_idx, tb in enumerate(text_blocks, 1):
                    # Le titre affiché dans Strapi doit être "Page 1", "Page 2", ...
                    page_title = f"Page {page_idx}"
                    original_title = tb.get("title") or ""
                    content = tb.get("content", [])
                    
                    # Le titre d'origine doit être injecté dans le contenu, au début du bloc
                    if original_title:
                        if isinstance(content, list):
                            # Rich Text Blocks : on ajoute un paragraphe en tête
                            title_block = {
                                "type": "paragraph",
                                "children": [{"text": original_title, "type": "text"}]
                            }
                            content = [title_block] + content
                        elif isinstance(content, str):
                            # Fallback si jamais c'est encore du markdown brut
                            content = f"{original_title}\n\n{content}"
                    
                    content_blocks.append({
                        "__component": "lesson-content.text-block",
                        "title": page_title,
                        "content": content,
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
                
                lesson_payload = {
                    "data": {
                        "title": lesson["title"],
                        "description": lesson.get("description", []),
                        "order": lesson.get("order", idx),
                        "chapter": chapter_id,
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
                        json=lesson_payload,
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
        if isinstance(data, list):
            return data
        return data.get("lessons", [])


def normalize_loaded_content(agent: "ChapterAndLessonGeneratorAgent", chapters_data: List[Dict]) -> None:
    """
    Normalise le contenu chargé depuis un fichier (ex: généré par Cursor Chat).
    - Convertit le markdown en Rich Text Blocks dans les text-blocks
    - Convertit les options/explanation en Rich Text Blocks si ce sont des strings
    - Calcule coinReward et ajoute lessonType/slug si manquants
    """
    for chapter in chapters_data:
        for lesson in chapter.get("lessons", []):
            content = lesson.get("content", {})
            # Text blocks: convert markdown string → Rich Text Blocks
            for tb in content.get("textBlocks", []):
                if isinstance(tb.get("content"), str):
                    tb["content"] = agent.convert_markdown_to_richtext(tb["content"])
            # Quiz blocks: format Strapi (ref. leçon "L'inflation, ton ennemi silencieux")
            # - options: toujours array de Rich Text blocks (1 par option sauf matching = 1 bloc avec \n)
            # - explanationcorrect / explanationfalse: toujours array de Rich Text, jamais null
            # - drag-order: options = items en ordre aléatoire, correctAnswer = même items en ordre correct (comma-separated)
            # - drag-drop: options = mots à glisser, correctAnswer = phrase complète
            # - matching: options = 1 bloc avec lignes A/1/B/2/..., correctAnswer = "A → 1, B → 2, ..."
            quiz_count = 0
            for qb in content.get("quizBlocks", []):
                quiz_count += 1
                qtype = (qb.get("questionType") or "multiple-choice").strip().lower()
                qb["questionType"] = qtype

                opts = qb.get("options")
                if opts is None or not isinstance(opts, list):
                    qb["options"] = []
                else:
                    if qtype == "matching":
                        # Un seul bloc avec toutes les lignes (A/1/B/2/...)
                        if not opts or all(isinstance(o, dict) for o in opts):
                            pass
                        else:
                            lines: List[str] = []
                            for opt in opts:
                                if isinstance(opt, str):
                                    lines.append(opt)
                                elif isinstance(opt, dict):
                                    for child in (opt.get("children") or []):
                                        if child.get("type") == "text":
                                            lines.append(child.get("text", ""))
                            if lines:
                                qb["options"] = [_rt_paragraph("\n".join(lines))]
                    else:
                        # multiple-choice, true-false, drag-order, drag-drop: 1 option = 1 paragraphe RT
                        options_rt = []
                        for opt in opts:
                            if isinstance(opt, dict) and opt.get("type") == "paragraph":
                                options_rt.append(opt)
                            elif isinstance(opt, str):
                                options_rt.append(_rt_paragraph(opt))
                            else:
                                options_rt.append(_rt_paragraph(str(opt)))
                        qb["options"] = options_rt

                for key in ("explanationcorrect", "explanationfalse"):
                    qb[key] = _ensure_explanation_rt(agent, qb.get(key))
            lesson["coinReward"] = lesson.get("coinReward") or agent.calculate_coin_reward(quiz_count)
            lesson.setdefault("lessonType", "quizz")
            lesson.setdefault("isActive", True)
            if "slug" not in lesson:
                lesson["slug"] = agent._generate_slug(lesson["title"])
            # Description leçon : string → Rich Text Blocks
            if isinstance(lesson.get("description"), str):
                lesson["description"] = [{"type": "paragraph", "children": [{"text": lesson["description"], "type": "text"}]}]


def main():
    parser = argparse.ArgumentParser(
        description='Génère des chapitres et des leçons et les crée dans Strapi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Générer automatiquement 3 nouveaux chapitres avec leurs leçons
  python scripts-generate-chapters-and-lessons-agent.py \\
    --section "Les bases" \\
    --generate-chapters 3 \\
    --create

  # Générer un chapitre spécifique avec des leçons définies
  python scripts-generate-chapters-and-lessons-agent.py \\
    --section "Les bases" \\
    --chapter "Nouveau chapitre" \\
    --lessons input/lessons.json \\
    --create
        """
    )
    
    parser.add_argument('--section', required=True, help='Titre de la section existante dans Strapi')
    parser.add_argument('--chapter', help='Titre du chapitre spécifique (optionnel si --generate-chapters)')
    parser.add_argument('--generate-chapters', type=int, help='Nombre de chapitres à générer automatiquement')
    parser.add_argument('--lessons', help='Fichier JSON avec structure des leçons (requis si --chapter)')
    parser.add_argument('--reference', nargs='+', default=[], help='Documents de référence Markdown')
    parser.add_argument('--output', default='output/generated-content.json', help='Fichier de sortie')
    parser.add_argument('--input', help='Fichier JSON à charger (au lieu de générer)')
    parser.add_argument('--create', action='store_true', help='Créer directement dans Strapi après génération')
    parser.add_argument('--attach-only', action='store_true', help='Attacher uniquement à des chapitres existants')
    
    args = parser.parse_args()
    
    # Validation
    if not args.input and not args.generate_chapters and not args.chapter:
        parser.error("Vous devez spécifier soit --generate-chapters, soit --chapter, soit --input")
    
    if args.chapter and not args.lessons and not args.input:
        parser.error("--chapter nécessite --lessons ou --input")
    
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
    agent = ChapterAndLessonGeneratorAgent(openai_key or "dummy", strapi_url, strapi_token)
    
    # Charger ou générer le contenu
    if args.input:
        print(f"📂 Chargement du contenu depuis : {args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            generated_content = json.load(f)
        chapters_data = generated_content.get("chapters", [])
        # Normaliser le contenu (markdown → Rich Text, options string → blocks, coinReward, etc.)
        normalize_loaded_content(agent, chapters_data)
        print(f"✅ Contenu normalisé : {len(chapters_data)} chapitre(s)")
    elif args.generate_chapters:
        # Générer automatiquement des chapitres
        print(f"🤖 Génération automatique de {args.generate_chapters} chapitres...")
        
        # Trouver la section pour récupérer les chapitres existants
        section = agent.find_section_by_title(args.section)
        if not section:
            print(f"❌ Section '{args.section}' non trouvée")
            return
        
        existing_chapters = agent.get_existing_chapters(section["id"])
        print(f"📚 Chapitres existants trouvés : {len(existing_chapters)}")
        
        # Documents de référence
        reference_docs = args.reference if args.reference else [
            "docs/cours-bourse-v1.md",
            "docs/cours-lois-reglementations-v1.md"
        ]
        
        # Générer les suggestions de chapitres
        chapter_suggestions = agent.generate_chapter_suggestions(
            section_title=args.section,
            existing_chapters=existing_chapters,
            num_chapters=args.generate_chapters,
            reference_docs=reference_docs
        )
        
        print(f"\n✅ {len(chapter_suggestions)} suggestions de chapitres générées")
        
        # Pour chaque chapitre suggéré, générer les leçons complètes
        chapters_data = []
        for chapter_suggestion in chapter_suggestions:
            print(f"\n📚 Génération des leçons pour : {chapter_suggestion['title']}")
            
            # Utiliser les leçons suggérées comme base, ou générer à partir de la description
            lessons_input = chapter_suggestion.get("suggestedLessons", [])
            if not lessons_input:
                # Créer une structure basique à partir de la description
                lessons_input = [
                    {
                        "title": f"Introduction à {chapter_suggestion['title']}",
                        "description": chapter_suggestion.get("description", ""),
                        "order": 1,
                        "difficulty": "easy",
                        "topics": []
                    }
                ]
            
            # Générer le contenu complet des leçons
            lessons_content = agent.generate_lessons_for_chapter(
                section_title=args.section,
                chapter_title=chapter_suggestion["title"],
                chapter_description=chapter_suggestion.get("description", ""),
                lessons_input=lessons_input,
                reference_docs=reference_docs
            )
            
            chapters_data.append({
                "title": chapter_suggestion["title"],
                "description": chapter_suggestion.get("description", ""),
                "order": chapter_suggestion.get("order", len(chapters_data) + 1),
                "lessons": lessons_content.get("lessons", [])
            })
        
        # Sauvegarder
        generated_content = {"chapters": chapters_data}
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(generated_content, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Contenu sauvegardé dans : {args.output}")
        
    else:
        # Générer un chapitre spécifique
        lessons_input = load_lessons_input(args.lessons)
        
        reference_docs = args.reference if args.reference else [
            "docs/cours-bourse-v1.md",
            "docs/cours-lois-reglementations-v1.md"
        ]
        
        lessons_content = agent.generate_lessons_for_chapter(
            section_title=args.section,
            chapter_title=args.chapter,
            chapter_description="",
            lessons_input=lessons_input,
            reference_docs=reference_docs
        )
        
        chapters_data = [{
            "title": args.chapter,
            "description": "",
            "order": 1,
            "lessons": lessons_content.get("lessons", [])
        }]
        
        generated_content = {"chapters": chapters_data}
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(generated_content, f, indent=2, ensure_ascii=False)
        print(f"✅ Contenu sauvegardé dans : {args.output}")
    
    # Créer dans Strapi si demandé
    if args.create:
        print("\n" + "="*50)
        print("🚀 CRÉATION DANS STRAPI")
        print("="*50)
        validation = input(f"\n⚠️  Valider et créer {len(chapters_data)} chapitre(s) dans Strapi ? (oui/non): ")
        
        if validation.lower() in ['oui', 'o', 'yes', 'y']:
            results = agent.create_in_strapi(
                section_title=args.section,
                chapters_data=chapters_data,
                attach_to_existing_chapters=args.attach_only
            )
            
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
