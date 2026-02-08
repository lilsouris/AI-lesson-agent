# Comment l'Agent Analyse la Section

## 🎯 Principe

L'agent analyse **spécifiquement la section que tu définis** avec `--section` et génère des chapitres en continuité avec **cette section uniquement**.

## 📊 Processus d'Analyse

### Étape 1 : Récupération de la Section

Quand tu lances :
```bash
python python-agent/scripts-generate-chapters-and-lessons-agent.py \
  --section "Les bases" \
  --generate-chapters 3
```

L'agent :
1. ✅ Trouve la section "Les bases" dans Strapi
2. ✅ Récupère **TOUS** les chapitres existants de cette section
3. ✅ Analyse leurs titres, descriptions, et ordre

### Étape 2 : Analyse Contextuelle

L'agent analyse :
- **Les titres des chapitres existants** → Pour comprendre le thème
- **Les descriptions** → Pour comprendre le niveau et le style
- **L'ordre** → Pour comprendre la progression logique
- **Le titre de la section** → Pour rester cohérent avec le thème global

### Étape 3 : Génération Intelligente

L'agent génère de nouveaux chapitres qui :
- ✅ Sont **cohérents avec le thème de la section**
- ✅ **Suivent la progression logique** des chapitres existants
- ✅ **Évitent les doublons** avec les chapitres existants
- ✅ **S'intègrent naturellement** dans la séquence

## 📝 Exemples Concrets

### Exemple 1 : Section "Les bases"

**Structure cible (10 chapitres pour une bonne progression débutant) :**
1. Fondamentaux de l'argent et de l'épargne
2. Préparer sa stratégie d'investissement
3. Introduction aux investissements
4. Gérer son budget et son épargne
5. Les frais : comprendre pour mieux choisir
6. Passer à l'action : ouvrir et utiliser un compte
7. Épargner régulièrement : la régularité paye
8. Rester serein et patient
9. Protéger et diversifier son épargne
10. Et après ? Consolider et aller plus loin

**Contenu pré-généré (chapitres 4 à 10) :** Le fichier `output/les-bases-chapitres-4-a-10.json` contient les 7 chapitres de remplacement/ajout (ordres 4 à 10), avec des leçons **sans doublon** avec le contenu déjà présent dans Strapi (ch1–ch3 et anciens ch4–ch5). Pour analyser le contenu existant : `python scripts/fetch-les-bases-content.py` (sauvegarde dans `output/les-bases-existing-content.json`). Génération du JSON : `python scripts/build-les-bases-chapitres-4-a-10.py`. Pour pousser vers Strapi : supprimer ou désactiver dans Strapi les anciens chapitres 4 et 5 (Les mécanismes de l'investissement, Le lointain futur), puis `--section "Les bases" --input output/les-bases-chapitres-4-a-10.json --create`.

### Exemple 2 : Section "Bourse"

**Chapitres existants :**
1. Les bases de la bourse
2. Investir intelligemment

**Chapitres générés (exemples) :**
3. Analyser une entreprise (bilan, compte de résultat)
4. Les stratégies d'investissement (value, growth, dividend)
5. La psychologie de l'investisseur

→ **Cohérent avec le thème "Bourse"** (plus avancé, spécialisé)

### Exemple 3 : Section "Lois et réglementations"

**Chapitres existants :**
1. Panorama des livrets réglementés

**Chapitres générés (exemples) :**
2. Les bases de la fiscalité française
3. Fiscalité des placements et investissements
4. Protection des épargnants et réglementation

→ **Cohérent avec le thème "Lois et réglementations"** (juridique, fiscal)

## 🔍 Code de l'Analyse

Voici comment l'agent récupère les chapitres existants :

```python
def get_existing_chapters(self, section_id: int) -> List[Dict]:
    """Récupère tous les chapitres existants d'une section"""
    response = requests.get(
        f"{self.strapi_url}/api/chapters",
        params={
            "filters[section][id][$eq]": section_id,  # ← Filtre par section
            "pagination[pageSize]": 100,
            "sort": "order:asc"
        }
    )
    return response.json().get("data", [])
```

L'agent utilise **uniquement** les chapitres de la section spécifiée, pas ceux des autres sections.

## 💡 Conseils

### 1. Choisis la bonne section

```bash
# ✅ Bon : Section cohérente
--section "Les bases" --generate-chapters 2

# ❌ Évite : Mélanger des sections différentes
--section "Bourse"  # Génère des chapitres sur la bourse
--section "Immobilier"  # Génère des chapitres sur l'immobilier
```

### 2. Plus il y a de chapitres existants, mieux c'est

Plus l'agent a de contexte, meilleures seront les suggestions :

- **1-2 chapitres existants** : L'agent doit deviner le thème
- **5+ chapitres existants** : L'agent comprend bien la progression et le style

### 3. Utilise des documents de référence pertinents

```bash
# Pour la section "Bourse"
--reference docs/cours-bourse-v1.md

# Pour la section "Lois et réglementations"
--reference docs/cours-lois-reglementations-v1.md
```

## 🎨 Personnalisation par Section

Tu peux créer des prompts différents selon la section en modifiant le code :

```python
# Dans generate_chapter_suggestions()
if section_title == "Les bases":
    # Prompt plus simple, débutant
    system_prompt = "Génère des chapitres pour débutants..."
elif section_title == "Bourse":
    # Prompt plus avancé, technique
    system_prompt = "Génère des chapitres techniques sur la bourse..."
```

## ✅ Résumé

**OUI**, l'agent fonctionne **spécifiquement** en fonction de la section que tu définis :

1. ✅ Analyse uniquement les chapitres de **cette section**
2. ✅ Génère des chapitres cohérents avec **le thème de cette section**
3. ✅ Respecte **la progression logique** de cette section
4. ✅ S'intègre naturellement dans **cette section**

C'est pour ça que tu dois toujours spécifier `--section` : c'est le contexte principal pour la génération !
