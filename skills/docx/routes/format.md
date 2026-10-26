# Route: Format / Mise en page

## Workflow

```
1. Lire le document actuel (pandoc pour le contenu, unpack pour la structure)
2. Identifier les exigences de formatage de l'utilisateur
3. Utiliser le tableau de conversion d'unités (voir SKILL.md)
4. Appliquer le formatage via la manipulation OOXML ou python-docx
5. Packager et vérifier
```

## Formatage rapide via python-docx

Pour les tâches de formatage simples, python-docx est souvent plus rapide que le brut XML :

```python
from docx import Document as PythonDocument
from docx.shared import Pt, Cm, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = PythonDocument("input.docx")

# Modifier le formatage de tous les paragraphes du corps
for para in doc.paragraphs:
    if para.style.name.startswith("Heading"):
        continue
    para.paragraph_format.first_line_indent = Twips(420)
    para.paragraph_format.line_spacing = 1.5
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in para.runs:
        run.font.name = "宋体"
        run.font.size = Pt(12)  # Xiao Si 小四

doc.save("output.docx")
```

## Modèles de demande de formatage courants

### Formatage de thèse universitaire

Exigences typiques pour une thèse universitaire chinoise :

```python
from docx.shared import Cm, Pt, Twips

# Marges
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)

# Polices
# Corps : SimSun 宋体 Xiao Si 小四 (12pt)
# H1 : SimHei 黑体 San Hao 三号 (16pt) centré
# H2 : SimHei 黑体 Si Hao 四号 (14pt)
# H3 : SimHei 黑体 Xiao Si 小四 (12pt)
# Anglais : Times New Roman, mêmes tailles
```

### Numéros de page commençant à partir d'une page spécifique

Utiliser une approche multi-sections :
```python
# Section 1 : Pages liminaires (chiffres romains)
# Section 2 : Contenu principal (chiffres arabes, commençant à 1)
# Cela nécessite une manipulation OOXML — voir routes/edit.md pour le workflow unpack/pack
```

En brut XML (`word/document.xml`) :
```xml
<w:sectPr>
  <w:pgNumType w:fmt="upperRoman" w:start="1"/>
</w:sectPr>
<!-- Nouvelle section -->
<w:sectPr>
  <w:pgNumType w:fmt="decimal" w:start="1"/>
</w:sectPr>
```

### En-têtes différents par section

Chaque section dans un .docx peut avoir son propre en-tête/pied de page. Voir `references/docx-js-advanced.md` pour l'approche multi-sections.

Pour les documents existants, modifier `word/document.xml` pour diviser `<w:sectPr>` et créer des fichiers `headerN.xml` séparés.

### Conversion de taille de police

Lorsque l'utilisateur demande un nom de taille de police chinoise :

| Demande | Action |
|---------|--------|
| "Changer en taille Wu Hao (5ème)" | `font.size = Pt(10.5)` ou `size: 21` dans docx-js |
| "Titre en SimHei San Hao" | `font.size = Pt(16)`, `font.name = "SimHei"` |
| "Corps en Xiao Si SimSun" | `font.size = Pt(12)`, `font.name = "SimSun"` |

### Ajustement de l'interligne

```python
from docx.shared import Twips

# Espacement 1.0x
para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
para.paragraph_format.line_spacing = 1.0

# Espacement 1.3x (notre défaut)
para.paragraph_format.line_spacing = 1.5

# Espacement fixe (ex: 28pt)
para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
para.paragraph_format.line_spacing = Pt(28)
```

## Vérification

Après les modifications de formatage :
1. Ouvrir dans LibreOffice ou convertir en PDF pour vérification visuelle
2. Extraire le texte avec pandoc pour s'assurer que le contenu est inchangé
3. Comparer les tailles de fichier (les modifications de formatage ne devraient pas changer drastiquement la taille)
