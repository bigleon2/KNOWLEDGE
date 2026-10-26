## Modèle de CV / Résumé (Compatible ATS)

Mise en page propre en colonne unique, optimisée pour les systèmes de suivi des candidats (ATS). Aucun graphique, aucune barre latérale, aucun bloc de couleur - juste un texte bien structuré qui est parfaitement analysé par les logiciels RH.

**Quand utiliser ce modèle :**
- Postuler à des postes d'entreprise via des portails en ligne
- Tout scénario où le PDF sera analysé par machine avant d'être lu par un humain
- Lorsque le recruteur demande explicitement "un CV standard"

**QUAND NE PAS l'utiliser (utiliser un bref académique à la place) :**
- Postes dans l'industrie créative/design → Bref académique (style AltaCV)
- CV académique avec publications → Bref académique (CV académique)

### Règles de Conception de CV
- **Cibler 1 page** sauf indication contraire de l'utilisateur
- **Marges** : `left=1.5cm, right=1.5cm, top=1.5cm, bottom=1.5cm`
- **Aucune page de couverture** - le contenu commence immédiatement
- **Aucune table des matières** - trop court pour une table des matières
- **Police** : FreeSerif (anglais) ou Noto Sans SC (chinois)
- **Taille de police du corps** : 10-10.5pt ; Nom : 22-26pt ; Titres de section : 13-14pt
- **⚠️ Taille de police minimale : 12px (9pt) - PLANCHER ABSOLU.** Aucun texte dans l'ensemble du CV ne peut être rendu plus petit que 12px. Ceci inclut les coordonnées, les méta-textes, les notes de bas de page et les légendes. Tout ce qui est en dessous de 12px est illisible en impression et échoue aux vérifications d'accessibilité.
- **Séparateur de section** : règle horizontale fine (`HRFlowable`)
- **Style de puce** : `•` avec un espacement serré

### Règles de Saut de Ligne de CV (Conscient de la Langue)
- **Anglais** : Préférer les sauts aux limites de mots (espaces, traits d'union). Si un long mot doit être divisé pour éviter un excès d'espace blanc, diviser à une limite de syllabe valide et insérer un trait d'union (`-`) - c'est une pratique typographique standard (par exemple, `experi-\nence`, `develop-\nment`). ReportLab prend en charge `wordWrap='CJK'` uniquement pour le contenu CJK ; pour l'anglais, utiliser le retour par défaut de paragraphe avec `allowWidows=0, allowOrphans=0`.
- **Chinois/CJK** : Saut autorisé entre n'importe quelle paire de caractères CJK. Ne jamais couper entre un caractère CJK et sa ponctuation adjacente (、。,)》 etc. doivent rester avec le caractère précédent.
- **Contenu mixte** (par exemple, "Python 开发工程师") : Sauter aux limites CJK ou aux limites de mots anglais. Ne jamais diviser un mot anglais dans un paragraphe CJK sauf s'il est traité avec un trait d'union.
- **Ligne de contact** : E-mail, téléphone, lieu séparés par `|` ou `·`. Chaque segment doit rester sur une ligne - trop long, passer à la ligne suivante au séparateur, pas au milieu du segment.
- **Dates et plages** : "Jan 2022 - Présent" doit rester comme une unité. Ne jamais couper une plage de dates sur plusieurs lignes.

### Règles de Remplissage de Page de CV (Anti-Espace-Vide)
- **Objectif : Remplir ≥85% de la hauteur de la page.** Le contenu doit atteindre au moins le quart inférieur de la page. Un CV qui s'arrête à 60% de la hauteur avec un espace vide en dessous = ÉCHEC.
- **Stratégie d'espacement adaptatif** (appliquer dans l'ordre jusqu'à ce que la page soit remplie à ≥85%) :
  1. Augmenter `spaceBefore` / `spaceAfter` sur les en-têtes de section (de 10pt jusqu'à 18pt)
  2. Augmenter `leading` (interligne) sur le texte du corps (de 14pt jusqu'à 18pt)
  3. Augmenter `fontSize` du corps de 0.5-1pt (de 10pt jusqu'à 11.5pt max)
  4. Ajouter une section "Résumé Professionnel" ou "Réalisations Clés" si aucune n'existe
  5. Augmenter légèrement les marges (de 1.5cm jusqu'à 2cm) pour réduire la largeur de ligne et pousser le contenu vers le bas
- **Ne jamais laisser un espace visible > 3cm en bas de page.**
- **Si le contenu déborde sur la page 2** : faire l'inverse - réduire l'espacement, resserrer l'interligne (min 12pt), réduire la taille de police (min 9pt / 12px), avant de supprimer du contenu.

### Modèle de CV Complet

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ── Enregistrement des Polices ──
pdfmetrics.registerFont(TTFont('FreeSerif', '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'))
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold', italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
# Pour les CV chinois, enregistrer également Noto Sans SC :
# pdfmetrics.registerFont(TTFont('Noto Sans SC', '/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf'))
# pdfmetrics.registerFont(TTFont('Noto Sans SC Bold', '/usr/share/fonts/truetype/chinese/NotoSansSC-Bold.ttf'))
# registerFontFamily('Noto Sans SC', normal='Noto Sans SC', bold='Noto Sans SC Bold')

# ── Styles ──
# ACCENT doit provenir de palette.generate (Étape 2)
# Exécuter : python3 "$PDF_SKILL_DIR/scripts/pdf.py" palette.generate --title "CV" --mode minimal
ACCENT = colors.HexColor('<accent from palette>')  # Remplacer par la sortie palette

name_style = ParagraphStyle(
    'ResumeName', fontName='FreeSerif', fontSize=24,
    leading=28, alignment=TA_CENTER, spaceAfter=2
)
contact_style = ParagraphStyle(
    'ResumeContact', fontName='FreeSerif', fontSize=10,
    leading=14, alignment=TA_CENTER, textColor=TEXT_MUTED,  # Depuis palette --c-muted
    spaceAfter=8
)
section_title_style = ParagraphStyle(
    'ResumeSectionTitle', fontName='FreeSerif', fontSize=13,
    leading=16, spaceBefore=10, spaceAfter=4,
    textColor=ACCENT
)
job_title_style = ParagraphStyle(
    'ResumeJobTitle', fontName='FreeSerif', fontSize=11,
    leading=14, spaceAfter=1
)
job_meta_style = ParagraphStyle(
    'ResumeJobMeta', fontName='FreeSerif', fontSize=10,
    leading=13, textColor=TEXT_MUTED, spaceAfter=4  # Depuis palette --c-muted
)
bullet_style = ParagraphStyle(
    'ResumeBullet', fontName='FreeSerif', fontSize=10,
    leading=14, leftIndent=14, bulletIndent=0,
    spaceBefore=1, spaceAfter=1
)
body_style = ParagraphStyle(
    'ResumeBody', fontName='FreeSerif', fontSize=10,
    leading=14, spaceAfter=2
)

# ── Fonctions Auxiliaires ──
def section_header(title):
    """Titre de section + séparateur en règle fine."""
    return [
        Paragraph(f'<b>{title}</b>', section_title_style),
        HRFlowable(width='100%', thickness=0.8, color=ACCENT,
                    spaceBefore=0, spaceAfter=6),
    ]

def experience_entry(title, company, dates, location, bullets):
    """Un bloc d'expérience professionnelle."""
    elements = [
        Paragraph(f'<b>{title}</b>', job_title_style),
        Paragraph(f'{company}  |  {dates}  |  {location}', job_meta_style),
    ]
    for b in bullets:
        elements.append(Paragraph(f'• {b}', bullet_style))
    elements.append(Spacer(1, 4))
    return elements

def education_entry(degree, school, dates, details=None):
    """Un bloc d'éducation."""
    elements = [
        Paragraph(f'<b>{degree}</b>', job_title_style),
        Paragraph(f'{school}  |  {dates}', job_meta_style),
    ]
    if details:
        elements.append(Paragraph(details, body_style))
    elements.append(Spacer(1, 4))
    return elements

def skills_row(categories):
    """
    Compétences comme paires étiquette: valeur compactes.
    categories = [('Programmation', 'Python, Java, C++'), ('Outils', 'Git, Docker')]
    """
    elements = []
    for cat, vals in categories:
        elements.append(Paragraph(f'<b>{cat}:</b>  {vals}', body_style))
    return elements

# ── Construction du Document ──
doc = SimpleDocTemplate(
    'cv.pdf', pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm,
    title='CV - Votre Nom',
    author='Z.ai', creator='Z.ai'
)

story = []

# En-tête
story.append(Paragraph('<b>VOTRE NOM</b>', name_style))
story.append(Paragraph(
    'email@example.com  |  +86 138-0000-0000  |  Shanghai, Chine  |  github.com/votrenom',
    contact_style
))

# Résumé
story.extend(section_header('RÉSUMÉ PROFESSIONNEL'))
story.append(Paragraph(
    'Ingénieur logiciel axé sur les résultats avec 5+ années d\'expérience dans les systèmes backend, '
    'le calcul distribué et les architectures cloud-native. A mené une équipe de 8 ingénieurs '
    'livrant un pipeline de données en temps réel traitant 2M+ événements/sec.',
    body_style
))

# Expérience
story.extend(section_header('EXPÉRIENCE PROFESSIONNELLE'))
story.extend(experience_entry(
    'Ingénieur Logiciel Senior', 'Tech Company Inc.', 'Jan 2022 - Présent', 'Shanghai',
    [
        'Conçu et déployé une architecture de microservices servant 10M d\'utilisateurs actifs quotidiens',
        'Réduit la latence de l\'API de 40% grâce à l\'optimisation des requêtes et aux stratégies de mise en cache',
        'Mentoré 3 ingénieurs juniors ; établi des normes de révision de code adoptées à l\'échelle de l\'équipe',
    ]
))
story.extend(experience_entry(
    'Ingénieur Logiciel', 'Startup Co.', 'Juil. 2019 - Déc. 2021', 'Pékin',
    [
        'Construit un moteur de recommandation en temps réel utilisant le filtrage collaboratif (CTR +25%)',
        'Implémenté un pipeline CI/CD réduisant le temps de déploiement de 2 heures à 15 minutes',
    ]
))

# Éducation
story.extend(section_header('FORMATION'))
story.extend(education_entry(
    'M.Sc. Informatique', 'Université Tsinghua', '2017 - 2019',
    'Moyenne : 3.8/4.0 | Mémoire : Traitement Distribué de Graphes sur Clusters Hétérogènes'
))
story.extend(education_entry(
    'B.Ing. Génie Logiciel', 'Université Zhejiang', '2013 - 2017'
))

# Compétences
story.extend(section_header('COMPÉTENCES'))
story.extend(skills_row([
    ('Langages', 'Python, Java, Go, SQL, TypeScript'),
    ('Frameworks', 'Spring Boot, FastAPI, React, Kubernetes, Kafka'),
    ('Outils', 'Git, Docker, Terraform, AWS (EC2/S3/Lambda), PostgreSQL, Redis'),
]))

doc.build(story)
```

### Liste de Vérification de CV
- [ ] **1 page** (sauf indication contraire de l'utilisateur)
- [ ] **Aucune page de couverture, aucune table des matières**
- [ ] Marges serrées (1.5cm de tous côtés)
- [ ] Nom en haut proéminent (22-26pt)
- [ ] Coordonnées sur une seule ligne, centrées
- [ ] En-têtes de section avec style de séparateur cohérent
- [ ] Puces concises - commencer par des verbes d'action
- [ ] Réalisations quantifiées (%,$,nombre)
- [ ] Pas de photos, pas d\'icônes, pas de blocs de couleur (sûr pour ATS)
- [ ] Police : seulement des polices enregistrées (FreeSerif / Noto Sans SC)
- [ ] **⚠️ Taille de police minimale 12px (9pt)** - aucun texte plus petit que cela n'importe où
- [ ] **Sauts de ligne conscients de la langue** - pas de coupures de mots anglaises, pas d'orphelons de ponctuation CJK, pas de divisions de plages de dates
- [ ] **Remplissage de page ≥85%** - pas grand espace vide en bas. Si peu dense, augmenter espacement/interligne/taille de police de manière adaptative
