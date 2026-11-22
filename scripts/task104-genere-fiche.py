#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 104 — Génération de la fiche PDF « agent engineering » (discipline n°56).

Voie Report (ReportLab) du skill pdf :
  - corps : TocDocTemplate + multiBuild (sommaire cliquable), français, A4 ;
  - couverture : Template 07 Crystal Blue déjà rendue (html2poster.js) ;
  - fusion : pypdf normalize A4 (couverture en page 0).
Palette : jeu fixe du Template 07 (typesetting/cover.md) — aucune couleur hors palette.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import hashlib
import os
import sys

PDF_SKILL_DIR = "/home/z/my-project/skills/pdf"
sys.path.insert(0, os.path.join(PDF_SKILL_DIR, "scripts"))

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, HRFlowable, KeepTogether,
                                PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts"
pdfmetrics.registerFont(TTFont("NotoSerifSC", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSerifSC-Bold", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif", f"{FONT_DIR}/truetype/freefont/FreeSerif.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Bold", f"{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Italic", f"{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-BoldItalic", f"{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", f"{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf"))
registerFontFamily("NotoSerifSC", normal="NotoSerifSC", bold="NotoSerifSC-Bold")
registerFontFamily("FreeSerif", normal="FreeSerif", bold="FreeSerif-Bold",
                   italic="FreeSerif-Italic", boldItalic="FreeSerif-BoldItalic")
registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans")

from pdf import install_font_fallback  # noqa: E402  (après enregistrement des polices)
install_font_fallback()

# ------------------------------------------- palette fixe Template 07 (corps)
PAGE_BG      = colors.HexColor("#f5f8fc")   # XL
SECTION_BG   = colors.HexColor("#edf2f9")   # XL
CARD_BG      = colors.HexColor("#e4ecf5")   # L
TABLE_STRIPE = colors.HexColor("#eef3fa")   # L
HEADER_FILL  = colors.HexColor("#1a4a7a")   # M
BORDER       = colors.HexColor("#c0d0e2")   # S
ACCENT       = colors.HexColor("#2d7ab3")   # XS
TEXT_PRIMARY = colors.HexColor("#142840")
TEXT_MUTED   = colors.HexColor("#5a7a96")

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_ROW_EVEN = colors.white
TABLE_ROW_ODD = TABLE_STRIPE

# ---------------------------------------------------------------- geometry
MARGIN = 1.0 * inch
PAGE_W, PAGE_H = A4
AVAIL_W = PAGE_W - 2 * MARGIN
AVAIL_H = PAGE_H - 2 * MARGIN
H1_THRESHOLD = AVAIL_H * 0.25
DOC_TITLE = "Agent Engineering — Fiche discipline n°56"
FOOTER_AUTHOR = "Écosystème Knowledge"

# ---------------------------------------------------------------- styles
S_BODY = ParagraphStyle("Body", fontName="FreeSerif", fontSize=10.5, leading=17,
                        alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY, spaceAfter=10)
S_H1 = ParagraphStyle("H1", fontName="FreeSerif", fontSize=21, leading=26,
                      textColor=HEADER_FILL, spaceBefore=16, spaceAfter=4)
S_H2 = ParagraphStyle("H2", fontName="FreeSerif", fontSize=14.5, leading=20,
                      textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=6)
S_H3 = ParagraphStyle("H3", fontName="FreeSerif", fontSize=11.5, leading=16,
                      textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=5)
S_BULLET = ParagraphStyle("Bullet", parent=S_BODY, alignment=TA_LEFT, leftIndent=14,
                          bulletIndent=2, spaceAfter=5)
S_NUM = ParagraphStyle("Num", parent=S_BODY, alignment=TA_LEFT, leftIndent=18,
                       firstLineIndent=-12, spaceAfter=6)
S_QUOTE = ParagraphStyle("Quote", fontName="FreeSerif-Italic", fontSize=10.5, leading=17,
                         leftIndent=24, textColor=TEXT_MUTED, spaceBefore=6, spaceAfter=10)
S_TH = ParagraphStyle("TH", fontName="FreeSerif", fontSize=9.8, leading=13,
                      textColor=colors.white, alignment=TA_LEFT)
S_TD = ParagraphStyle("TD", fontName="FreeSerif", fontSize=9.4, leading=13.5,
                      textColor=TEXT_PRIMARY, alignment=TA_LEFT)
S_TD_C = ParagraphStyle("TDC", parent=S_TD, alignment=TA_CENTER)
S_CAPTION = ParagraphStyle("Caption", fontName="FreeSerif", fontSize=8.5, leading=12,
                           textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=6)
S_STAT = ParagraphStyle("Stat", fontName="FreeSerif", fontSize=19, leading=23,
                        textColor=ACCENT, alignment=TA_CENTER)
S_STAT_LBL = ParagraphStyle("StatLbl", fontName="FreeSerif", fontSize=8.5, leading=11.5,
                            textColor=TEXT_MUTED, alignment=TA_CENTER)
S_TOC_TITLE = ParagraphStyle("TocTitle", fontName="FreeSerif", fontSize=21, leading=26,
                             textColor=HEADER_FILL, spaceAfter=14)
S_TOC0 = ParagraphStyle("TOC0", fontName="FreeSerif", fontSize=11, leading=17, leftIndent=6,
                        textColor=TEXT_PRIMARY)
S_TOC1 = ParagraphStyle("TOC1", fontName="FreeSerif", fontSize=10, leading=15, leftIndent=26,
                        textColor=TEXT_MUTED)


# ---------------------------------------------------------------- doc template
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, "bookmark_name"):
            level = getattr(flowable, "bookmark_level", 0)
            text = getattr(flowable, "bookmark_text", "")
            key = getattr(flowable, "bookmark_key", "")
            # numéro affiché = numérotation corps (sommaire = i, corps = 1..n)
            self.notify("TOCEntry", (level, text, self.page - 1, key))


def on_page(canvas, doc):
    canvas.saveState()
    # fond de page (XL tier — pont visuel avec la couverture)
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # en-tête : titre + filet accent pleine largeur
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 0.62 * inch, DOC_TITLE)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 0.70 * inch, PAGE_W - MARGIN, PAGE_H - 0.70 * inch)
    # pied de page : filet léger + auteur + numéro (i pour le sommaire, 1..n pour le corps)
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, 0.45 * inch, FOOTER_AUTHOR)
    num = "i" if doc.page == 1 else str(doc.page - 1)
    canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch, num)
    canvas.restoreState()


def heading(text, style, level=0):
    key = "h_" + hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p


def h1_block(text, first_flowable=None):
    """Titre de chapitre : CondPageBreak (règle des 25 %) + titre + filet accent."""
    parts = [heading(text, S_H1, level=0),
             HRFlowable(width="100%", color=ACCENT, thickness=1.4,
                        spaceBefore=2, spaceAfter=10)]
    if first_flowable is not None:
        parts.append(first_flowable)
    return [CondPageBreak(H1_THRESHOLD), KeepTogether(parts)]


def h2_block(text, first_flowable=None):
    parts = [heading(text, S_H2, level=1)]
    if first_flowable is not None:
        parts.append(first_flowable)
    return [KeepTogether(parts)]


def table_block(data_rows, col_ratios, header_row, caption=None, center_cols=None):
    col_widths = [r * AVAIL_W for r in col_ratios]
    assert abs(sum(col_widths) - AVAIL_W) < 1.0, "largeur de table hors cadre"
    rows = [[Paragraph("<b>%s</b>" % c, S_TH) for c in header_row]]
    for row in data_rows:
        cells = []
        for j, c in enumerate(row):
            st = S_TD_C if (center_cols and j in center_cols) else S_TD
            cells.append(Paragraph(c, st))
        rows.append(cells)
    t = Table(rows, colWidths=col_widths, hAlign="CENTER", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
    ]
    for i in range(1, len(rows)):
        style.append(("BACKGROUND", (0, i), (-1, i),
                      TABLE_ROW_ODD if i % 2 == 1 else TABLE_ROW_EVEN))
    t.setStyle(TableStyle(style))
    out = [Spacer(1, 12), t]
    if caption:
        out += [Spacer(1, 6), Paragraph(caption, S_CAPTION), Spacer(1, 10)]
    else:
        out += [Spacer(1, 12)]
    return out


def stat_row(stats):
    """Bande de trois callouts de données (règle data-to-ink)."""
    cell_w = AVAIL_W / 3.0
    cells = []
    for big, label in stats:
        cells.append([Paragraph("<b>%s</b>" % big, S_STAT), Paragraph(label, S_STAT_LBL)])
    t = Table([cells], colWidths=[cell_w] * 3, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("LINEABOVE", (0, 0), (-1, 0), 2.2, ACCENT),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [Spacer(1, 12), t, Spacer(1, 12)]


def callout(text):
    inner = Paragraph(text, ParagraphStyle("CalloutTxt", parent=S_BODY, alignment=TA_LEFT,
                                           spaceAfter=0, textColor=TEXT_PRIMARY))
    t = Table([[inner]], colWidths=[AVAIL_W], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, ACCENT),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return [Spacer(1, 8), t, Spacer(1, 10)]


# ---------------------------------------------------------------- story
story = []

# ---- sommaire (page i, non numérotée en chiffres arabes)
toc = TableOfContents()
toc.levelStyles = [S_TOC0, S_TOC1]
story.append(Paragraph("<b>Sommaire</b>", S_TOC_TITLE))
story.append(HRFlowable(width="100%", color=ACCENT, thickness=1.4, spaceBefore=0, spaceAfter=14))
story.append(toc)
story.append(PageBreak())

# ============================== 1. CARTE D'IDENTITÉ
p1 = Paragraph("La présente fiche documente la discipline <b>agent engineering</b> (n°56) "
               "sous sa forme installée, c'est-à-dire le répertoire skills/agent-engineering/ de "
               "l'écosystème Knowledge, source de vérité de tout ce qui suit. Elle répond à trois "
               "questions : à quoi sert cette discipline, comment fonctionne-t-elle en interne, et "
               "comment l'utiliser concrètement au quotidien. Chaque affirmation s'appuie sur le "
               "SKILL.md version 1.1.1 et sur sa référence de veille references/fondements-academiques.md, "
               "toutes deux versionnées dans le dépôt Knowledge et certifiées par les arbitres de "
               "l'écosystème à chaque montée de version.", S_BODY)
story += h1_block("1. Carte d'identité de la discipline", p1)
story += table_block(
    [
        ["Nom du skill", "agent-engineering (kebab-case, convention SHARED §1.3)"],
        ["Version courante", "1.1.1 (PATCH — sémantique et routage inchangés, Task 90)"],
        ["Nature", "Skill <b>discipline</b> d'ingénierie — discipline n°56 du registre SHARED §7"],
        ["Catégorie / langue", "ecosystem / français exclusif (règle d'or n°6)"],
        ["Forme installée", "skills/agent-engineering/SKILL.md (+ evals/ et references/)"],
        ["Détenteur principal", "gen-plan — mobilisation aux étapes E5 et E7 de tout plan d'actions"],
        ["Dépendances déclarées", "gen-plan >= 3.15.0 · fleet-engineering >= 1.0.1 · autonomous-agent >= 1.2.0 · agent-creator >= 2.2.0"],
        ["Tags", "#agent-engineering · #multi-agent-systems · #orchestration · #disciplines · #ecosystem"],
        ["Traçabilité", "v1.0.0 (Task 83) · v1.1.0 (Task 86) · v1.1.1 (Task 90) — session web-ecef7f80"],
    ],
    [0.28, 0.72],
    ["Champ", "Valeur"],
    caption="Tableau 1 — Carte d'identité extraite du frontmatter YAML du SKILL.md installé (v1.1.1).")
story.append(Paragraph("La discipline n°56 est dite <b>englobante</b> : elle ne détient aucune méthode "
                       "opérationnelle déjà possédée par un autre skill, et sa valeur réside dans le "
                       "routage rigoureux et dans les critères de sortie qu'elle arme, jamais dans la "
                       "duplication de méthode — c'est la règle anti-duplication R4 de l'écosystème. "
                       "Elle encadre chaque tâche relevant de trois domaines techniques (présentés au "
                       "chapitre 3), la transmet au détenteur compétent, vérifie que les critères de "
                       "sortie tiennent, puis se retire sans laisser d'état résiduel. Cette posture de "
                       "cadre la distingue des skills d'exécution : elle se juge sur la qualité des "
                       "décisions de cadrage et sur l'honnêteté des verdicts, pas sur le code produit.",
                       S_BODY))

# ============================== 2. RÔLE
p2 = Paragraph("Le rôle de la discipline n°56 tient en quatre fonctions, appliquées dans cet ordre à "
               "toute tâche touchant aux agents. Ces fonctions viennent directement de la section 1.1 "
               "du SKILL.md : elles forment le contrat de service de la discipline vis-à-vis du "
               "propriétaire de l'écosystème et de gen-plan, son détenteur orchestrateur.", S_BODY)
story += h1_block("2. Rôle : cadrer, router, outiller, veiller", p2)
story += table_block(
    [
        ["<b>CADRER</b>", "Classifier la tâche dans le bon domaine (ABE, AE ou MASE), en dériver les exigences, et décider si le système doit être agentisé — ou pas."],
        ["<b>ROUTER</b>", "Sélectionner le détenteur écosystème compétent (fleet-engineering, memory-engineering, autonomous-agent...) et lui transmettre un cadrage auto-contenu : contexte, critères, bornes — jamais de dépendance au contexte parent."],
        ["<b>OUTILLER</b>", "Armer un critère vérifiable exécutable (arbitre, baseline, seuil) AVANT l'exécution ; un livrable non validé reste « en attente », jamais « validé » (règle R3)."],
        ["<b>VEILLER</b>", "Maintenir les fondements 2026 à jour (sources vérifiées), suivre les signaux du domaine et conserver les garde-fous (gate anti-flotte, traçabilité par agent)."],
    ],
    [0.16, 0.84],
    ["Fonction", "Ce que la discipline fait concrètement"],
    caption="Tableau 2 — Les quatre fonctions du rôle (SKILL.md §1.1 et §1.6).")
story += stat_row([
    ("57 %", "des praticiens ont des agents en production — la fiabilité, pas le coût, est le premier frein (LangChain, State of Agent Engineering 2026)"),
    ("≈ 15×", "ratio de coût documenté d'un système multi-agents face à un simple dialogue (Anthropic, juin 2025) — raison d'être de la gate anti-flotte"),
    ("6/7", "score de la baseline A2 des déclencheurs de la discipline (Task 86, 21 votes réels) — mesuré, pas déclaré"),
])
story.append(Paragraph("Pourquoi un tel rôle ? Parce que les agents sont non déterministes : les "
                       "transformer en systèmes fiables exige itération rapide, évaluation systématique "
                       "et observabilité du comportement. Sans cadrage préalable, une tâche d'agents "
                       "dérive vers la complexité prématurée — le rapport Building Effective Agents "
                       "(Anthropic, décembre 2024) recommande de commencer simple et de ne complexifier "
                       "que sur preuve de besoin mesurée. Sans garde préalable, une tâche multi-agents "
                       "viole la gate anti-flotte : le ratio de coût d'environ quinze fois se paie pour "
                       "rien quand les sous-tâches sont séquentielles. La discipline n°56 existe pour "
                       "empêcher ces deux dérives avant qu'elles ne coûtent", S_BODY))
story.append(Paragraph("du temps et du budget — elle cadre d'abord, elle route ensuite, et elle ne "
                       "laisse l'exécution au détenteur que lorsqu'un critère de sortie exécutable est "
                       "armé.", S_BODY))

# ============================== 3. LES TROIS DOMAINES
p3 = Paragraph("Toute demande passe d'abord par une classification dans l'un des trois domaines du "
               "cadre. Cette classification n'est pas académique : elle détermine les exigences "
               "applicables, les détenteurs mobilisables et les critères de sortie. Le tableau ci-dessous "
               "reprend la matrice de cadrage du SKILL.md (§1.2), avec les définitions issues des "
               "fondements 2026.", S_BODY)
story += h1_block("3. Les trois domaines : ABE, AE, MASE", p3)
story += table_block(
    [
        ["<b>ABE</b> — Agent-Based Engineering",
         "Paradigme où l'agent est le bloc constitutif premier du système (ABSE, agents-as-building-blocks ; méthodologies Tropos et lignées i*).",
         "Modéliser un système en société d'agents (rôles, intentions, interactions, environnement) ; décider SI un système doit être agentisé ; structurer les rôles et le contexte partagé."],
        ["<b>AE</b> — Agent Engineering",
         "Processus itératif de transformation de LLMs en systèmes fiables (State of Agent Engineering, LangChain 2026).",
         "Prototype vers production : outillage (tool use), contexte agentique, évaluation, observabilité, contrôle des coûts, durcissement."],
        ["<b>MASE</b> — Multi-Agent Systems Engineering",
         "Ingénierie des systèmes multi-agents : orchestration, communication, coordination, émergence, sûreté inter-agents (Anthropic 2025-2026, Cognition 2025).",
         "Orchestration d'une flotte (route vers fleet-engineering n°54), handoffs typés, évaluation multi-agents, gardes coordination/collusion/sabotage."],
    ],
    [0.20, 0.40, 0.40],
    ["Domaine", "Définition (fondements)", "Tâches types"],
    caption="Tableau 3 — Cadre de classification des tâches d'agents (SKILL.md §1.2).")
story.append(Paragraph("La lecture pratique de cette matrice est simple : une demande de modélisation "
                       "structurelle relève de l'ABE, une demande de fiabilisation d'un agent existant "
                       "relève de l'AE, et toute demande impliquant plusieurs agents coordonnés relève "
                       "du MASE. En cas d'ambiguïté, la discipline tranche par la question de la valeur : "
                       "quel est le plus petit domaine qui couvre intégralement la tâche ? Ce choix "
                       "minimaliste évite l'inflation de périmètre et prépare le routage du chapitre "
                       "suivant. L'idempotence est garantie par construction : re-cadrer une même tâche "
                       "produit la même route et les mêmes critères, car les décisions sont dérivées de "
                       "l'état du disque (leçon KO-L003), jamais de l'impression du moment.", S_BODY))

# ============================== 4. FONCTIONNEMENT
p4 = Paragraph("La discipline fonctionne selon un cycle opérationnel en six étapes, répété autant de "
               "fois que nécessaire au fil d'une mission. Ce cycle est léger par conception : la "
               "discipline n'est pas un moteur d'exécution mais un cadre de gouvernance qui rend "
               "l'exécution vérifiable.", S_BODY)
story += h1_block("4. Fonctionnement : cycle et règles opérationnelles", p4)
story += table_block(
    [
        ["1", "<b>Cadrer</b>", "Classifier la tâche (ABE / AE / MASE), dériver les exigences, décider si le système doit être agentisé."],
        ["2", "<b>Router</b>", "Sélectionner le détenteur compétent et lui transmettre un cadrage auto-contenu (contexte + critères + bornes)."],
        ["3", "<b>Outiller</b>", "Armer le critère vérifiable (arbitre, baseline, seuil) AVANT l'exécution — jamais après."],
        ["4", "<b>Surveiller</b>", "Vérifier que le détenteur tient ses critères ; re-router au besoin sans changer l'objectif."],
        ["5", "<b>Consolider</b>", "Statuts dérivés du disque (KO-L003), verdicts mécaniques, écarts consignés honnêtement au worklog."],
        ["6", "<b>Se retirer</b>", "Aucun état résiduel : le système livré relève désormais de son détenteur."],
    ],
    [0.08, 0.18, 0.74],
    ["#", "Étape", "Contenu"],
    caption="Tableau 4 — Cycle opérationnel en six étapes (SKILL.md §1.6).", center_cols={0})
story.append(Paragraph("<b>Six règles opérationnelles</b> encadrent ce cycle (SKILL.md §1.4) :",
                       ParagraphStyle("lead", parent=S_BODY, spaceAfter=6)))
for i, (titre, texte) in enumerate([
    ("Simple d'abord", "pas de système multi-agents tant qu'un agent simple ou un workflow composé résout ; la complexification exige une preuve de besoin mesurée."),
    ("Gate anti-flotte avant routage MASE", "tâches séquentielles à écritures entrelacées : flotte interdite ; ratio de coût d'environ quinze fois non justifié par un périmètre parallélisable : flotte interdite."),
    ("Critère vérifiable par tâche", "chaque tâche cadrée embarque un arbitre exécutable (harness-engineering) — un livrable non validé est « en attente », jamais « validé »."),
    ("États collectifs", "l'État Long d'un système d'agents est collectif (worklog par Task ID, registre KB), jamais dans la mémoire d'un agent mort."),
    ("Journalisation qui-décide-quoi par agent", "traçabilité individuelle obligatoire dans tout système multi-agents (Anthropic, août 2026 — collusion, sabotage)."),
    ("Adaptation autonome", "l'échec d'un routage ou d'un agent est un signal de re-cadrage (domaine, détenteur, bornes), jamais un arrêt implicite."),
]):
    story.append(Paragraph("<b>%d. %s</b> — %s" % (i + 1, titre, texte), S_NUM))
story.append(Paragraph("Sur le plan de la mémoire, la discipline ne détient aucun état propre : "
                       "l'État Long est délégué au worklog (sections par Task ID), au registre KB pour "
                       "les décisions d'architecture et à l'answer key pour les décisions de "
                       "planification ; l'État Court — le contexte de cadrage — meurt avec la tâche. "
                       "Ses artefacts techniques se limitent à trois pièces : une matrice de cadrage "
                       "(tâche × domaine × détenteur × critère × bornes), une fiche de routage "
                       "auto-contenue par tâche et une trace de veille dans references/. Elle ne possède "
                       "aucun script propre : les arbitres appartiennent aux détenteurs qu'elle "
                       "mobilise.", S_BODY))

# ============================== 5. ROUTAGE
p5 = Paragraph("Le routage est la fonction première de la discipline : à chaque tâche cadrée, elle "
               "associe le détenteur écosystème qui détient réellement la méthode. Le tableau "
               "ci-dessous reproduit la table de routage du SKILL.md (§1.3) ; il est le réflexe de "
               "consultation le plus utile au quotidien.", S_BODY)
story += h1_block("5. Routage écosystème : les détenteurs", p5)
story += table_block(
    [
        ["Coordination opérationnelle de plusieurs agents (flotte)", "fleet-engineering (n°54)", "Patterns M1-M5, Task IDs, bornes, agrégation arbitrée — gen-plan E5/E7"],
        ["Mémoire d'un agent, État Court/Long, compaction", "memory-engineering", "Piliers write / select / compress / isolate"],
        ["Critères de sortie exécutables, arbitres, gardes", "harness-engineering", "Verdicts mécaniques, profils, signaux"],
        ["Contrat ou micro-spécification par sous-tâche", "spec-driven-development", "Spec AVANT code, critères d'acceptation mécaniques"],
        ["Créer un agent autonome (format .agent, cycle A-H)", "autonomous-agent", "Gabarit .agent — matérialisation vivante : knowledge-observer.agent v1.1.0"],
        ["Fabriquer un skill ou un agent réutilisable", "agent-creator / skill-creator", "Workflow F1-F5, conventions, evals"],
        ["Planifier la mission, paralléliser, arbitrer", "gen-plan", "Étapes E1-E15, Graph Diamond E9-E14, answer key"],
        ["Refactoring d'un système d'agents", "refactoring-engineering (n°55) + refactor-guard", "Zéro-régression, blast radius (refactoring-test)"],
    ],
    [0.42, 0.26, 0.32],
    ["Tâche cadrée", "Détenteur mobilisé", "Cadre apporté"],
    caption="Tableau 5 — Table de routage écosystème (SKILL.md §1.3).")
story.append(Paragraph("Une règle de routage en cinq points neutralise les conflits de périmètre : "
                       "(a) une tâche séquentielle à écritures entrelacées reste confiée à UN agent — "
                       "jamais à une flotte ; (b) une tâche parallélisable et indépendante peut ouvrir "
                       "une flotte selon les patterns M1-M5 de fleet-engineering, sous la gate "
                       "anti-flotte (périmètre large et indépendance prouvées) ; (c) les nœuds scripts "
                       "et binaires relèvent d'inter-scripts ; (d) un agent réutilisable à créer passe "
                       "par agent-creator ; (e) la discipline n°56 reste mobilisée comme cadre tant que "
                       "la tâche est vivante — elle vérifie que le détenteur tient ses critères, puis "
                       "se retire.", S_BODY))

# ============================== 6. UTILISATION
p6 = Paragraph("Concrètement, comment utiliser la discipline dans l'écosystème Knowledge ? Trois voies "
               "d'activation existent, toutes documentées dans le champ read_when du SKILL.md. La plus "
               "fréquente est implicite : elle se déclenche toute seule lorsque gen-plan détecte à "
               "l'étape E5 qu'une demande touche aux agents. Les deux autres sont explicites.", S_BODY)
story += h1_block("6. Utilisation au sein de l'écosystème", p6)
story.append(Paragraph("<b>Via gen-plan (voie implicite, la plus courante)</b> — toute directive au "
                       "format gen-plan : « ... » qui mentionne la conception, la fiabilisation ou "
                       "l'orchestration d'agents mobilise la discipline aux étapes E5 (sélection des "
                       "skills) et E7 (création du plan). La discipline nourrit alors l'answer key du "
                       "plan avec les décisions de cadrage des agents — chaque décision portant un "
                       "critère vérifiable mécaniquement.", S_BULLET))
story.append(Paragraph("<b>Par déclencheurs verbatim</b> — mentionner dans une demande : agent "
                       "engineering, ingénierie d'agents, agent-based engineering, multi-agent systems "
                       "engineering, systèmes multi-agents, concevoir / construire / évaluer un agent, "
                       "observabilité des agents, sûreté des agents, fiabiliser un agent en production, "
                       "orchestration des tâches d'agents, société d'agents, Tropos.", S_BULLET))
story.append(Paragraph("<b>En contrôle négatif assumé</b> — la discipline sait refuser : une demande "
                       "de coordination opérationnelle d'une flotte ou de création d'un skill est "
                       "routée vers fleet-engineering ou agent-creator plutôt que traitée "
                       "(contrôles A10/A14, §5 du SKILL.md).", S_BULLET))
story.append(Paragraph("Le flux d'usage complet, du besoin au livrable, suit cinq temps : "
                       "<b>(1)</b> vous décrivez une tâche d'agents dans une directive gen-plan ; "
                       "<b>(2)</b> gen-plan cadre à E5 et mobilise la discipline n°56 ; "
                       "<b>(3)</b> la discipline produit la matrice de cadrage et route vers le "
                       "détenteur compétent avec un critère de sortie exécutable ; <b>(4)</b> le "
                       "détenteur exécute sous arbitres (verdicts mécaniques) ; <b>(5)</b> la "
                       "consolidation est journalisée au worklog par Task ID, statuts dérivés du "
                       "disque. L'évaluation des déclencheurs suit le protocole SHARED §7 v2 : sept "
                       "requêtes de test (cinq positives, deux contrôles négatifs), baseline mesurée "
                       "lors de la Task 86 avec 21 votes réels — score initial 5/7 puis 6/7 après "
                       "optimisation de la description ; l'écart structurel restant (cas 6, voie "
                       "mécanique du radical « agent ») est consigné honnêtement comme proposition "
                       "future, jamais masqué.", S_BODY))
story += table_block(
    [
        ["1.0.0", "Task 83 (2026-11-09, directive 1a1beaee032b5aa5)", "Matérialisation de la discipline n°56 — forme SKILL discipline, inscription du registre §8, cascade KO-L004"],
        ["1.1.0", "Task 86 (2026-11-09, directive 1a1bed51ccaf78f1)", "Description Optimization A10/A14 — clause de contrôles négatifs en description ; baseline A2 mesurée 5/7 puis 6/7"],
        ["1.1.1", "Task 90 (2026-11-09, directive 1a1c1dde3f6d0021)", "Corrections de consistance post-test — staleness résorbé, doublon supprimé, evals alignés ; sémantique inchangée"],
    ],
    [0.14, 0.28, 0.58],
    ["Version", "Origine", "Apport"],
    caption="Tableau 6 — Historique de traçabilité (SKILL.md §6).", center_cols={0})

# ============================== 7. CINQ EXEMPLES CONCRETS
p7 = Paragraph("Les cinq exemples suivants montrent la discipline en situation réelle. Chacun est "
               "ancré dans des composants existants de l'écosystème — skills installés, arbitres "
               "exécutables, tasks journalisées au worklog — et se termine par le résultat "
               "vérifiable attendu. Ils couvrent les trois domaines du cadre : deux relèvent de l'AE, "
               "un de l'ABE et deux du MASE.", S_BODY)
story += h1_block("7. Cinq exemples concrets d'usage", p7)

story += h2_block("Exemple 1 — Matérialiser un agent autonome au format .agent",
                  Paragraph("<b>Domaine : AE · Détenteur routé : autonomous-agent.</b> Vous demandez un "
                            "agent capable d'observer les sessions et d'en tirer des leçons durables. "
                            "La discipline n°56 cadre d'abord la tâche : c'est de l'AE (transformer un "
                            "LLM en système fiable, cycle de vie complet), pas une simple fabrique de "
                            "prompt. Elle route ensuite vers autonomous-agent, détenteur du gabarit "
                            ".agent (cycle A-H, États Court et Long à deux niveaux). Le critère de "
                            "sortie est armé avant l'exécution : le fichier .agent doit exister au "
                            "chemin canonique avec ses modules internes et passer le test d'existence "
                            "(leçon KO-L007 — matérialisation d'abord). C'est exactement le chemin "
                            "suivi par knowledge-observer.agent v1.1.0 lors de la Task 82 : l'agent "
                            "d'observation tourne depuis et alimente les leçons KO-Lxxx utilisées par "
                            "tous les skills.", S_BODY))
story += h2_block("Exemple 2 — Orchestrer une flotte pour un audit massif de l'arbre skills/",
                  Paragraph("<b>Domaine : MASE · Détenteur routé : fleet-engineering (n°54).</b> "
                            "L'écosystème compte plus d'une centaine de skills à inspecter (l'arbitre "
                            "triggers-replay en évalue 101 à chaque certification). Si vous demandez "
                            "une audit agentisé de cet arbre, la discipline applique d'abord la gate "
                            "anti-flotte : des sous-tâches de lecture seule, indépendantes entre "
                            "elles, sur un périmètre large — la flotte est autorisée. Elle route "
                            "alors vers fleet-engineering, qui choisit le pattern adapté (fan-out "
                            "pour la collecte, pipeline pour les étages d'analyse), fixe les bornes "
                            "(Task IDs préfixés, agrégation arbitrée) et génère les Task IDs "
                            "traçables. Le critère de sortie : chaque sous-résultat est agrégé et "
                            "arbitré, et le ratio de coût multi-agents (environ quinze fois) est "
                            "justifié noir sur blanc par le périmètre parallélisable. Sans cette "
                            "gate, l'audit aurait coûté quinze fois plus cher pour le même "
                            "résultat.", S_BODY))
story += h2_block("Exemple 3 — Fiabiliser un agent en production (évaluation et observabilité)",
                  Paragraph("<b>Domaine : AE · Détenteurs routés : harness-engineering + loop-engineering.</b> "
                            "Un agent déjà vivant déclenche trop rarement, ou déclenche à tort. La "
                            "discipline cadre la tâche comme du durcissement AE : évaluation "
                            "systématique et observabilité avant tout réglage. Elle route vers "
                            "harness-engineering pour armer le critère — le protocole SHARED §7 v2 : "
                            "voie mécanique d'abord (stemmer et arbitre V6), puis confirmation LLM en "
                            "trois runs au quota OK — et vers loop-engineering pour la boucle "
                            "d'amélioration. C'est le cas réel de la Task 86 sur la discipline elle-même : "
                            "baseline A2 mesurée sur 21 votes réels (5/7), optimisation de la "
                            "description, re-mesure (6/7), écart structurel restant consigné au lieu "
                            "d'être maquillé. Le résultat vérifiable : trigger_evals.json versionné, "
                            "score honnête, journal de calibration.", S_BODY))
story += h2_block("Exemple 4 — Décider de NE PAS agentiser (la gate anti-flotte en action)",
                  Paragraph("<b>Domaine : ABE · Décision : refus documenté.</b> L'ABE ne sert pas "
                            "qu'à agentiser : elle sert d'abord à décider SI le système doit être "
                            "agentisé. Prenons l'installation de l'écosystème elle-même (pipeline "
                            "eco_install des Tasks 102-103) : huit étapes strictement séquentielles "
                            "à écritures entrelacées — chaque étape écrit l'état que la suivante "
                            "lit, avec codes de retour propagés et garde anti-rétrogradation. Une "
                            "flotte d'agents serait une catastrophe : écritures concurrentes sur le "
                            "même dépôt, contexte non partageable, coût multiplié. La discipline "
                            "invoque Cognition 2025 (Don't Build Multi-Agents) et le principe simple "
                            "d'abord d'Anthropic : un pipeline séquentiel unique, sans flotte. Le "
                            "résultat vérifiable : pipeline rejoué deux fois avec le même code de "
                            "retour (idempotence), zéro divergence post-installation sur les 55 "
                            "compétences installées.", S_BODY))
story += h2_block("Exemple 5 — Anti-dérive des handoffs dans une mission multi-agents",
                  Paragraph("<b>Domaine : MASE · Détenteurs routés : spec-driven-development + memory-engineering.</b> "
                            "Une mission longuette fait travailler successivement plusieurs agents "
                            "spécialisés — fabrique (agent-creator), arbitres (harness-engineering), "
                            "observation (knowledge-observer). Le risque documenté par Anthropic "
                            "(juin 2025) est la perte de contexte au handoff : chaque transfert "
                            "d'agent peut écraser des décisions. La discipline impose deux parades "
                            "avant tout lancement : des micro-spécifications auto-contenues par "
                            "sous-tâche (spec AVANT code — spec-driven-development), de sorte qu'aucun "
                            "agent ne dépend du contexte d'un autre ; et un État Long collectif — "
                            "worklog par Task ID et registre KB — jamais la mémoire vive d'un agent "
                            "mort. La journalisation qui-a-décidé-quoi par agent (Anthropic, août "
                            "2026) complète le dispositif. Résultat vérifiable dans l'écosystème : "
                            "les reprises après coupure de session réussissent sans perte — les "
                            "suites 138 à 150 du worklog ont été reconstruites depuis les clones "
                            "scellés et le dépôt, pas depuis un contexte résiduel.", S_BODY))

# ============================== 8. FONDEMENTS
p8 = Paragraph("La discipline veille sur un socle de sources 2026 vérifiées lors de sa création "
               "(Task 83) puis maintenues. Ces sources ne sont pas décoratives : chacune fonde une "
               "règle opérationnelle précise du SKILL.md, comme le montre le tableau ci-dessous.", S_BODY)
story += h1_block("8. Fondements 2026 et veille", p8)
story += table_block(
    [
        ["State of Agent Engineering (LangChain, 2026)", "Définition de l'AE comme processus itératif de fiabilisation ; 1300+ praticiens interrogés ; la fiabilité remplace le coût comme premier frein."],
        ["Building Effective Agents (Anthropic, déc. 2024)", "Principisme « simple d'abord » : blocs de base avant patterns sophistiqués — fondement de la règle opérationnelle n°1."],
        ["Agent-Based Software Engineering / Tropos (ABSE)", "Agents-as-building-blocks, modélisation en société d'agents avant implémentation — fondement du domaine ABE."],
        ["How we built our multi-agent research system (Anthropic, juin 2025)", "Orchestrateur + sous-agents, échecs de handoff, ratio de coût ≈ 15× — fondement de la gate anti-flotte."],
        ["Don't Build Multi-Agents (Cognition, 2025, reconfirmé 04/2026)", "Interdiction des flottes sur tâches séquentielles à écritures entrelacées ; artefacts de stockage plutôt que mémoire vive."],
        ["Patterns and Problems in Emerging Multi-Agent Systems (Anthropic, août 2026)", "Collusion, sabotage, traçabilité — fondement de la journalisation qui-décide-quoi par agent."],
        ["Scaling Managed Agents / Agent Teams (Anthropic, avr. 2026)", "Découplage cerveau/exécution ; team lead assigne et fusionne — pont avec fleet-engineering."],
        ["Multi-Agent Orchestration : 5 patterns (2026)", "Fan-out, pipeline, debate, supervisor, swarm — patterns détenus opérationnellement par fleet-engineering n°54."],
    ],
    [0.42, 0.58],
    ["Source (année)", "Apport à la discipline"],
    caption="Tableau 7 — Socle de fondements vérifiés (references/fondements-academiques.md).")
story.append(Paragraph("Les signaux de veille suivis par la discipline vont dans le même sens : la "
                       "fiabilité remplace le coût comme frein numéro un ; les plateformes "
                       "d'évaluation et de déploiement d'agents se multiplient ; l'ABSE académique "
                       "converge avec l'agentique LLM autour du motif agents-as-building-blocks ; les "
                       "gardes multi-agents se durcissent (collusion, sabotage) ; et la spécialisation "
                       "croisée platform / ML / skill engineering dessine des métiers distincts. Une "
                       "lecture professionnelle recommandée dans cet ordre : State of Agent Engineering "
                       "pour le cadre itératif, Building Effective Agents pour la sobriété, les gardes "
                       "MASE (Cognition 2025 puis Anthropic août 2026), enfin ABSE/Tropos pour la "
                       "modélisation structurelle.", S_BODY))

# ============================== 9. FRONTIÈRES
p9 = Paragraph("Dernier garde-fou et non le moindre : la discipline sait ce qu'elle n'est pas. Ses "
               "contrôles négatifs sont assumés et testés (évaluations A10/A14, deux contrôles "
               "négatifs dans trigger_evals.json) : elle ne se déclenche pas pour la coordination "
               "opérationnelle d'une flotte ni pour la création concrète d'un skill ou d'un agent. "
               "Cette retenue protège le propriétaire du déroutement habituel des disciplines "
               "englobantes qui, mal bornées, finissent par tout absorber.", S_BODY)
story += h1_block("9. Frontières et contrôles négatifs", p9)
story += table_block(
    [
        ["Coordonner une flotte en production", "fleet-engineering (n°54) — patterns M1-M5 et bornes"],
        ["Créer un skill ou un agent réutilisable", "agent-creator / skill-creator — workflow F1-F5"],
        ["Instancier le format .agent et son cycle A-H", "autonomous-agent — gabarit et États Court/Long"],
        ["Planifier une mission en étapes et arbitrages", "gen-plan — E1-E15, Graph Diamond, answer key"],
        ["Mémoire, gardes-fous, contrats, boucles d'un agent", "memory-, harness-, spec-, loop-engineering"],
        ["Refactoring d'un système d'agents existant", "refactoring-engineering (n°55) + refactor-guard + refactoring-test"],
    ],
    [0.52, 0.48],
    ["Type de demande (hors périmètre n°56)", "Bon détenteur"],
    caption="Tableau 8 — Frontières de la discipline et routage hors périmètre.")
story.append(Paragraph("Deux garanties de gouvernance complètent la fiche. D'une part l'idempotence : "
                       "re-cadrer une même tâche produit la même route et les mêmes critères, car "
                       "tout est dérivé de l'état du disque (leçon KO-L003) — la discipline ne "
                       "s'adapte pas au hasard, elle re-décide sur preuve. D'autre part la langue : "
                       "tous les échanges avec le propriétaire se font en français exclusif (règle "
                       "d'or n°6), y compris cette fiche. Pour aller plus loin, les sources vivantes "
                       "restent le SKILL.md installé skills/agent-engineering/SKILL.md, sa référence "
                       "references/fondements-academiques.md et le registre KB skills/KNOWLEDGE.md — "
                       "toutes trois versionnées, certifiées et toujours prioritaires sur le présent "
                       "document en cas d'évolution.", S_BODY))

# ---------------------------------------------------------------- build
BODY_PDF = "/tmp/task104-corps.pdf"
COVER_PDF = "/tmp/task104-couverture.pdf"
FINAL_PDF = "/home/z/my-project/download/fiche-agent-engineering-ecosysteme.pdf"

doc = TocDocTemplate(BODY_PDF, pagesize=A4,
                     leftMargin=MARGIN, rightMargin=MARGIN,
                     topMargin=MARGIN, bottomMargin=MARGIN,
                     title=DOC_TITLE, author="Z.ai", creator="Z.ai",
                     subject="Fiche descriptive de la discipline agent engineering (n°56) de l'écosystème Knowledge")
doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)

# ---------------------------------------------------------------- merge (couverture en page 0)
from pypdf import PdfReader, PdfWriter  # noqa: E402

A4_W, A4_H = 595.28, 841.89

def normalize_page_to_a4(page):
    box = page.mediabox
    w, h = float(box.width), float(box.height)
    if abs(w - A4_W) > 0.1 or abs(h - A4_H) > 0.1:
        page.scale_to(A4_W, A4_H)
    return page

writer = PdfWriter()
writer.add_page(normalize_page_to_a4(PdfReader(COVER_PDF).pages[0]))
for page in PdfReader(BODY_PDF).pages:
    writer.add_page(normalize_page_to_a4(page))
writer.add_metadata({
    "/Title": DOC_TITLE,
    "/Author": "Z.ai",
    "/Creator": "Z.ai",
    "/Subject": "Fiche descriptive de la discipline agent engineering (n°56) de l'écosystème Knowledge",
})
with open(FINAL_PDF, "wb") as f:
    writer.write(f)

n_pages = len(PdfReader(FINAL_PDF).pages)
print("OK —", FINAL_PDF, "pages:", n_pages)
