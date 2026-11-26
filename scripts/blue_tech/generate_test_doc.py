#!/usr/bin/env python3
"""Générateur du document test blue-tech (Task 80).

Lit le template `blue-tech.template.json` (source de vérité des tokens) et produit
`download/blue-tech-test.html` — un document de démonstration couvrant les composants
du modèle (cover, toc, part-divider, chapter-header, body, callout, stat-card, codeblock
sécable, table, checklist, steps, qa-bubble, lexicon, diagram, ending).
Pipeline : rendu passe 1 (pagedjs) -> extraction des numéros de pages réelles (PyMuPDF)
-> injection au sommaire -> rendu passe 2 -> tampon des pieds de page (pypdf+reportlab).
Idempotent : re-jeu = mêmes numéros et mêmes pieds.
"""
import io
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/home/z/my-project")
TEMPLATE = ROOT / "ecosysteme/KNOWLEDGE/templates/blue-tech/blue-tech.template.json"
HTML_OUT = ROOT / "download/blue-tech-test.html"
PDF_OUT = ROOT / "download/blue-tech-test.pdf"
RENDERER = ROOT / "skills/pdf/scripts/html2pdf-next.js"

T = json.loads(TEMPLATE.read_text(encoding="utf-8"))
C = {t["name"]: t["hex"] for t in T["design_tokens"]["colors"]}

TITLE = "Modèle Blue-Tech — Document de test"
KICKER = "MODÈLE PAR DÉFAUT · BLUE-TECH V1"

TOC_ENTRIES = [
    ("1.1", "Composants de base — corps, encadrés, statistiques", "toc-11"),
    ("1.2", "Bloc de code sécable et code en ligne", "toc-12"),
    ("1.3", "Tableaux, contrôles et procédures", "toc-13"),
    ("1.4", "Schéma, lexique et questions", "toc-14"),
]

CODE_LINES = [
    "#!/usr/bin/env python3",
    '"""Chargement d\'un manifeste d\'écosystème (exemple de bloc sécable)."""',
    "import hashlib",
    "import json",
    "from pathlib import Path",
    "",
    "",
    "def charger_manifeste(chemin: Path) -> dict:",
    '    """Lit le manifeste d\'intégrité et retourne son dictionnaire."""',
    "    brut = chemin.read_text(encoding=\"utf-8\")",
    "    donnees = json.loads(brut)",
    "    if not isinstance(donnees, dict):",
    '        raise ValueError("manifeste invalide : racine non-dictionnaire")',
    "    return donnees",
    "",
    "",
    "def empreinte(fichier: Path) -> str:",
    '    """Calcule l\'empreinte SHA-256 d\'un fichier."""',
    "    h = hashlib.sha256()",
    "    with fichier.open(\"rb\") as flux:",
    "        for bloc in iter(lambda: flux.read(65536), b\"\"):",
    "            h.update(bloc)",
    "    return h.hexdigest()",
    "",
    "",
    "def verifier(corpus: dict, racine: Path) -> list:",
    '    """Vérifie chaque entrée du corpus et retourne les dérives."""',
    "    derives = []",
    "    for nom, attendu in sorted(corpus.items()):",
    "        cible = racine / nom",
    "        if not cible.exists():",
    "            derives.append((nom, \"manquant\"))",
    "            continue",
    "        if empreinte(cible) != attendu:",
    "            derives.append((nom, \"SHA divergent\"))",
    "    return derives",
    "",
    "",
    'if __name__ == "__main__":',
    '    manifeste = charger_manifeste(Path("ecosysteme-integrity.json"))',
    '    ecarts = verifier(manifeste.get("corpus", {}), Path("skills/@mon-ecosysteme"))',
    '    print(f"{len(ecarts)} dérive(s) détectée(s)")',
]


def css() -> str:
    return f"""
@page {{
    size: {T['page']['size']};
    margin: 0 0 48px 0;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
    --dark: {C['dark']}; --dark-2: {C['dark-2']};
    --cyan: {C['cyan']}; --cyan-deep: {C['cyan-deep']};
    --violet: {C['violet']}; --green: {C['green']};
    --text: {C['text']}; --soft: {C['text-soft']};
    --muted: {C['text-muted']}; --dim: {C['text-dim']};
}}
body {{
    font-family: 'Inter', 'Liberation Sans', sans-serif;
    font-size: 15px; color: var(--soft);
    background: var(--dark);
}}
.page {{ background: var(--dark); position: relative; overflow: hidden;
    width: 210mm; min-height: calc(297mm - 48px); }}
.grid-bg {{ position: absolute; inset: 0;
    background-image: {T['page']['background_effects']['grid']};
    background-size: {T['page']['background_effects']['grid_size']}; }}
.mono {{ font-family: 'JetBrains Mono', 'Liberation Mono', monospace; }}

/* ---- couverture ---- */
.cover {{ display: flex; flex-direction: column; justify-content: center;
    padding: 70px 64px; page-break-after: always; position: relative; }}
.glow {{ position: absolute; border-radius: 50%; filter: blur(90px); pointer-events: none; }}
.glow-cyan {{ width: 420px; height: 420px; background: rgba(34,211,238,0.10); top: -60px; right: -80px; }}
.glow-violet {{ width: 460px; height: 460px; background: rgba(124,58,237,0.12); bottom: -80px; left: -100px; }}
.cover-kicker {{ font-family: 'JetBrains Mono', monospace; font-size: 12.5px;
    letter-spacing: 4px; text-transform: uppercase; color: var(--cyan); margin-bottom: 26px; }}
.cover-title {{ font-size: 62px; font-weight: 900; line-height: 1.08; color: var(--text); }}
.cover-title .accent {{ color: var(--cyan); }}
.cover-subtitle {{ font-size: 20px; font-weight: 300; line-height: 1.4;
    color: var(--soft); margin-top: 22px; }}
.cover-summary {{ margin-top: 26px; max-width: 62%; font-size: 14.5px;
    line-height: 1.65; color: var(--muted); }}
.cover-tags {{ margin-top: 30px; display: flex; gap: 10px; flex-wrap: wrap; }}
.cover-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
    letter-spacing: 1px; color: var(--violet); border: 1px solid rgba(196,181,253,0.35);
    padding: 6px 12px; border-radius: 999px; }}
.cover-footer {{ position: absolute; bottom: 48px; left: 64px; right: 64px;
    display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px; letter-spacing: 1px; color: var(--dim); }}

/* ---- sommaire ---- */
.toc-page {{ padding: 64px 58px; page-break-after: always; position: relative; }}
.toc-kicker {{ font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 3px; text-transform: uppercase; color: var(--cyan); margin-bottom: 12px; }}
.toc-title {{ font-size: 30px; font-weight: 900; color: var(--text); margin-bottom: 20px; }}
.toc-rule {{ width: 46px; height: 3px; background: var(--cyan); margin-bottom: 26px; }}
.toc-line {{ display: flex; align-items: baseline; gap: 12px; padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08); }}
.toc-line .num {{ font-family: 'JetBrains Mono', monospace; color: var(--cyan); font-size: 12px; }}
.toc-line .label {{ color: var(--soft); font-size: 14px; }}
.toc-line .dots {{ flex: 1; border-bottom: 1px dotted rgba(255,255,255,0.22); }}
.toc-line .pg {{ font-family: 'JetBrains Mono', monospace; color: var(--violet); font-size: 12px; }}
.toc-callout {{ margin-top: 22px; border-left: 3px solid var(--cyan);
    background: rgba(34,211,238,0.08); padding: 12px 16px; font-size: 12.5px;
    color: var(--muted); }}

/* ---- intercalaire ---- */
.part-divider {{ background: var(--dark); page-break-before: always;
    page-break-after: always; padding: 90px 64px; position: relative; }}
.pd-num {{ font-size: 58px; font-weight: 900; color: var(--violet);
    font-family: 'JetBrains Mono', monospace; }}
.pd-title {{ font-size: 34px; font-weight: 900; color: var(--text); margin: 14px 0 18px; }}
.pd-chapo {{ font-size: 15px; line-height: 1.65; color: var(--muted); max-width: 70%; }}
.pd-item {{ margin-top: 20px; padding: 14px 18px; background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.10); border-radius: 10px; max-width: 70%; }}
.pd-item b {{ color: var(--text); }}

/* ---- corps ---- */
.main-content {{ padding: 54px 58px; }}
.chapter-header {{ margin-bottom: 18px; padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.10); }}
.hash {{ font-family: 'JetBrains Mono', monospace; color: var(--cyan);
    font-size: 12px; letter-spacing: 2px; }}
.sec-kicker {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
    letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin: 6px 0 8px; }}
.sec-title {{ font-size: 25px; font-weight: 800; color: var(--text); }}
.body-text {{ font-size: 15px; line-height: 1.65; color: var(--soft);
    margin-bottom: 12px; text-align: left; }}
.body-text strong {{ color: var(--text); }}
.inline-code {{ font-family: 'JetBrains Mono', monospace; font-size: 12.5px;
    background: rgba(255,255,255,0.06); color: #7dd3fc; padding: 2px 7px; border-radius: 5px; }}
.callout {{ border-left: 3px solid var(--cyan); background: rgba(34,211,238,0.08);
    padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 16px 0; }}
.callout-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 10px;
    letter-spacing: 2px; text-transform: uppercase; color: var(--cyan); display: block;
    margin-bottom: 6px; }}
.callout p {{ font-size: 13px; line-height: 1.6; color: var(--soft); }}
.stats-row {{ display: flex; gap: 14px; margin: 18px 0; }}
.stat-card {{ flex: 1; background: var(--dark-2); border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px; padding: 16px 18px; }}
.stat-num {{ font-size: 26px; font-weight: 900; color: var(--cyan);
    font-family: 'JetBrains Mono', monospace; }}
.stat-label {{ font-family: 'JetBrains Mono', monospace; font-size: 10px;
    letter-spacing: 1px; text-transform: uppercase; color: var(--muted); margin-top: 6px; }}

/* ---- code ---- */
.codeblock {{ background: var(--dark); border: 1px solid rgba(34,211,238,0.25);
    border-radius: 8px; margin: 16px 0; }}
.codeblock-head {{ display: flex; justify-content: space-between; align-items: center;
    background: var(--dark-2); padding: 9px 14px; border-radius: 8px 8px 0 0;
    font-family: 'JetBrains Mono', monospace; }}
.codeblock-file {{ font-size: 11px; color: var(--soft); }}
.codeblock-lang {{ font-size: 9.5px; letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--violet); border: 1px solid rgba(196,181,253,0.35);
    padding: 2px 8px; border-radius: 999px; }}
.codeblock pre {{ font-family: 'JetBrains Mono', monospace; font-size: 12.5px;
    line-height: 1.6; color: #cbd5e1; padding: 12px 16px; }}

/* ---- table / checklist / steps / qa / lexique / schéma ---- */
table.recap {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
table.recap th {{ background: var(--dark-2); font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--cyan);
    text-align: left; padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.18); }}
table.recap td {{ padding: 10px 12px; font-size: 12.5px; color: var(--soft);
    border-bottom: 1px solid rgba(255,255,255,0.08); }}
.checklist {{ list-style: none; margin: 14px 0; }}
.checklist li {{ font-size: 13px; color: var(--soft); padding: 6px 0 6px 26px;
    position: relative; }}
.checklist li::before {{ content: ""; position: absolute; left: 0; top: 8px;
    width: 11px; height: 11px; border: 1.5px solid var(--cyan); border-radius: 3px; }}
.checklist li.ok::after {{ content: "\\2713"; position: absolute; left: 1px; top: 4px;
    color: var(--green); font-size: 11px; }}
.step {{ display: flex; gap: 12px; margin: 10px 0; }}
.step-num {{ font-family: 'JetBrains Mono', monospace; color: var(--cyan); font-size: 12px;
    min-width: 26px; height: 26px; border: 1px solid rgba(34,211,238,0.35);
    border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
.step-title {{ font-size: 13.5px; font-weight: 700; color: var(--text); }}
.step-desc {{ font-size: 12.5px; color: var(--muted); line-height: 1.55; }}
.q-bubble {{ border: 1px solid rgba(124,58,237,0.35); background: rgba(124,58,237,0.12);
    border-radius: 10px; padding: 14px 18px; margin: 16px 0; }}
.q-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 2px;
    text-transform: uppercase; color: var(--violet); display: block; margin-bottom: 6px; }}
.q-text {{ font-size: 13px; line-height: 1.6; color: var(--soft); }}
.lex-entry {{ margin: 12px 0; }}
.lex-term {{ color: #7dd3fc; font-weight: 700; }}
.lex-num {{ font-family: 'JetBrains Mono', monospace; color: var(--violet); font-size: 11px; }}
.lex-def {{ font-size: 13px; color: var(--soft); line-height: 1.6; }}
.dg-flow {{ display: flex; align-items: center; gap: 10px; margin: 16px 0; }}
.dg-node {{ flex: 1; background: var(--dark-2); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px; padding: 12px 14px; }}
.dg-node-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 9px;
    letter-spacing: 1.5px; text-transform: uppercase; color: var(--violet); }}
.dg-node-title {{ font-size: 12.5px; font-weight: 700; color: var(--text); margin: 4px 0; }}
.dg-node-desc {{ font-size: 11px; color: var(--muted); line-height: 1.5; }}
.dg-arrow {{ color: var(--cyan); font-size: 18px; font-family: 'JetBrains Mono', monospace; }}
.diagram-title {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
    letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin: 14px 0 8px; }}

/* ---- fin ---- */
.ending {{ background: var(--dark); page-break-before: always; text-align: center;
    padding: 120px 64px 90px; position: relative; }}
.ending-mark {{ font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 4px; text-transform: uppercase; color: var(--cyan); margin-bottom: 18px; }}
.ending-title {{ font-size: 34px; font-weight: 900; color: var(--text); margin-bottom: 16px; }}
.ending-text {{ font-size: 14px; line-height: 1.65; color: var(--muted);
    max-width: 60%; margin: 0 auto 34px; }}
.ending-stats {{ display: flex; justify-content: center; gap: 40px; }}
.ending-stat .v {{ font-family: 'JetBrains Mono', monospace; font-size: 22px;
    font-weight: 700; color: var(--violet); }}
.ending-stat .l {{ font-family: 'JetBrains Mono', monospace; font-size: 9.5px;
    letter-spacing: 1.5px; text-transform: uppercase; color: var(--dim); margin-top: 4px; }}
"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_html(toc_pages: dict | None = None) -> str:
    tags = "".join(f'<span class="cover-tag">{t}</span>' for t in ["template", "a4", "sombre", "16 composants"])
    toc_lines = "".join(
        f'<div class="toc-line" id="{tid}"><span class="num">{num}</span>'
        f'<span class="label">{esc(label)}</span><span class="dots"></span>'
        f'<span class="pg">{(toc_pages or {}).get(tid, "·")}</span></div>'
        for num, label, tid in TOC_ENTRIES
    )
    code_html = "".join(f"<pre>{esc(line)}</pre>" for line in CODE_LINES)
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<title>{esc(TITLE)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{css()}</style></head>
<body>
<!-- COVER -->
<div class="page cover">
  <div class="glow glow-cyan"></div><div class="glow glow-violet"></div><div class="grid-bg"></div>
  <div class="cover-kicker">{KICKER}</div>
  <div class="cover-title">Modèle <span class="accent">Blue-Tech</span></div>
  <div class="cover-subtitle">Document de test généré depuis le template JSON de l'écosystème</div>
  <div class="cover-summary">Ce document démontre l'instanciation du modèle par défaut blue-tech :
  palette sombre unifiée, composants normalisés, sommaire calé sur les pages réelles et pieds de
  page tamponnés. Il sert de preuve de génération et de référence de mise en forme.</div>
  <div class="cover-tags">{tags}</div>
  <div class="cover-footer"><span>ECOSYSTÈME KNOWLEDGE</span><span>TEMPLATE 1.0.0 · 2026-11-08</span></div>
</div>
<!-- TOC -->
<div class="page toc-page">
  <div class="toc-kicker">Sommaire</div>
  <div class="toc-title">Contenu du document test</div>
  <div class="toc-rule"></div>
  {toc_lines}
  <div class="toc-callout">Repère de lecture — les numéros de pages sont extraits du rendu réel
  (passe 2) : sommaire en « i », corps en chiffres arabes, couverture et page finale sans pied.</div>
</div>
<!-- PARTIE 1 : INTERCALAIRE -->
<div class="page part-divider">
  <div class="grid-bg"></div>
  <div class="pd-num">01</div>
  <div class="pd-title">Démonstration des composants</div>
  <p class="pd-chapo">Chaque section instancie un sous-ensemble du catalogue de composants du
  modèle, avec le contrat CSS correspondant.</p>
  <div class="pd-item"><b>Composants de base</b> — corps de texte, encadrés, statistiques.</div>
  <div class="pd-item"><b>Composants structurants</b> — code, tableaux, procédures, schémas.</div>
</div>
<!-- PARTIE 1 : CONTENU -->
<div class="page main-content" style="padding-top: 0;">
  <div class="chapter-header" id="s-11"><span class="hash">1.1&nbsp;·&nbsp;</span>
    <div class="sec-kicker">Composants de base</div>
    <div class="sec-title">Corps, encadrés et statistiques</div>
  </div>
  <p class="body-text">Le modèle <strong>blue-tech</strong> fixe une palette sombre exclusive :
  tout le document repose sur le fond <span class="inline-code">#0f172a</span> et les surfaces
  dérivées, avec deux accents — le cyan <span class="inline-code">#22d3ee</span> en principal et
  le violet <span class="inline-code">#c4b5fd</span> en secondaire. Aucun fond clair n'est admis,
  conformément à la validation V1.</p>
  <div class="callout"><span class="callout-tag">Règle de palette</span>
  <p>Les seize couleurs nommées du bloc <strong>design_tokens</strong> sont la seule source
  autorisée : un document qui introduit une couleur hors registre est non conforme.</p></div>
  <div class="stats-row">
    <div class="stat-card"><div class="stat-num">16</div><div class="stat-label">couleurs nommées</div></div>
    <div class="stat-card"><div class="stat-num">16</div><div class="stat-label">composants catalogués</div></div>
    <div class="stat-card"><div class="stat-num">10</div><div class="stat-label">validations V1-V10</div></div>
  </div>
  <div class="chapter-header" id="s-12"><span class="hash">1.2&nbsp;·&nbsp;</span>
    <div class="sec-kicker">Composants de code</div>
    <div class="sec-title">Bloc de code sécable et code en ligne</div>
  </div>
  <p class="body-text">Le composant <span class="inline-code">codeblock</span> porte un en-tête
  (fichier + badge de langage) et un corps sécable entre pages : chaque ligne est un
  <span class="inline-code">&lt;pre&gt;</span> individuel, ce qui autorise la coupure sans
  débordement.</p>
  <div class="codeblock breakable">
    <div class="codeblock-head"><span class="codeblock-file">manifeste_ecosysteme.py</span>
    <span class="codeblock-lang">python</span></div>
    {code_html}
  </div>
  <div class="chapter-header" id="s-13"><span class="hash">1.3&nbsp;·&nbsp;</span>
    <div class="sec-kicker">Composants structurants</div>
    <div class="sec-title">Tableaux, contrôles et procédures</div>
  </div>
  <table class="recap">
    <tr><th>Bloc du template</th><th>Rôle</th><th>Contrôle associé</th></tr>
    <tr><td>meta</td><td>identité du modèle</td><td>json.load + 8 blocs</td></tr>
    <tr><td>design_tokens</td><td>palette et bordures</td><td>croisement source PDF</td></tr>
    <tr><td>components</td><td>catalogue et contrats CSS</td><td>validate_doc.py</td></tr>
    <tr><td>validations</td><td>règles V1-V10</td><td>arbitres pdf_qa</td></tr>
  </table>
  <ul class="checklist">
    <li class="ok">Palette sombre exclusive appliquée à toutes les pages</li>
    <li class="ok">Sommaire calé sur les numéros de pages réels</li>
    <li class="ok">Pieds de page tamponnés hors couverture et page finale</li>
    <li>Bloc de code sécable sans débordement</li>
  </ul>
  <div class="step"><div class="step-num">1</div><div><div class="step-title">Lire le template JSON</div>
    <div class="step-desc">Source de vérité unique — ne jamais coder les tokens en dur.</div></div></div>
  <div class="step"><div class="step-num">2</div><div><div class="step-title">Instancier les champs</div>
    <div class="step-desc">Remplacer les variables de gabarit du bloc <b>fields</b>.</div></div></div>
  <div class="step"><div class="step-num">3</div><div><div class="step-title">Rendre puis tamponner</div>
    <div class="step-desc">Paged.js (2 passes si sommaire) puis tampon des pieds.</div></div></div>
  <div class="step"><div class="step-num">4</div><div><div class="step-title">Passer les arbitres</div>
    <div class="step-desc">pdf_qa + validate_doc + inspection visuelle.</div></div></div>
  <div class="chapter-header" id="s-14"><span class="hash">1.4&nbsp;·&nbsp;</span>
    <div class="sec-kicker">Composants discursifs</div>
    <div class="sec-title">Schéma, lexique et questions</div>
  </div>
  <div class="diagram-title">Schéma A — chaîne de génération blue-tech</div>
  <div class="dg-flow">
    <div class="dg-node"><div class="dg-node-tag">Entrée</div><div class="dg-node-title">Template JSON</div>
      <div class="dg-node-desc">tokens + composants + validations</div></div>
    <div class="dg-arrow">→</div>
    <div class="dg-node"><div class="dg-node-tag">Génération</div><div class="dg-node-title">HTML instancié</div>
      <div class="dg-node-desc">champs remplis, contrat CSS respecté</div></div>
    <div class="dg-arrow">→</div>
    <div class="dg-node"><div class="dg-node-tag">Sortie</div><div class="dg-node-title">PDF A4 tamponné</div>
      <div class="dg-node-desc">QA PASS + inspection visuelle</div></div>
  </div>
  <div class="lex-entry"><span class="lex-num">L1&nbsp;·&nbsp;</span><span class="lex-term">Intercalaire</span>
    <div class="lex-def">Page de rupture qui ouvre une partie : fond sombre plein, numéro mono
    violet 58px, chapo et items résumant la partie.</div></div>
  <div class="q-bubble"><span class="q-tag">Question type</span>
  <div class="q-text">Le document test couvre-t-il la totalité du catalogue de composants ?
  Oui pour les composants de contenu ; la couverture et la page finale closent le cycle.</div></div>
</div>
<!-- ENDING -->
<div class="page ending">
  <div class="glow glow-cyan"></div><div class="glow glow-violet"></div>
  <div class="ending-mark">Fin du document test</div>
  <div class="ending-title">Modèle blue-tech validé</div>
  <div class="ending-text">Ce document prouve la chaîne complète : template JSON → HTML instancié
  → rendu Paged.js en deux passes → pieds de page tamponnés → arbitres. Il sert de référence de
  non-régression pour toute évolution du modèle.</div>
  <div class="ending-stats">
    <div class="ending-stat"><div class="v">1.0.0</div><div class="l">version modèle</div></div>
    <div class="ending-stat"><div class="v">16</div><div class="l">composants</div></div>
    <div class="ending-stat"><div class="v">10</div><div class="l">validations</div></div>
  </div>
</div>
</body></html>"""


def render(out: Path) -> None:
    r = subprocess.run(["node", str(RENDERER), str(HTML_OUT), "--output", str(out)],
                       capture_output=True, text=True, timeout=300, cwd=str(ROOT))
    if r.returncode != 0:
        print(r.stdout[-1500:], r.stderr[-1500:])
        sys.exit(f"rendu KO rc={r.returncode}")


def extraire_pages(pdf: Path) -> dict:
    import fitz
    doc = fitz.open(pdf)
    pages = {}
    cibles = {tid: label for _, label, tid in TOC_ENTRIES}
    for pno in range(2, len(doc)):  # corps : à partir de la page 3 (index 2)
        texte = re.sub(r"\s+", " ", doc[pno].get_text())
        for tid, label in cibles.items():
            if tid not in pages and label.split(" — ")[0] in texte:
                pages[tid] = str(pno - 1)  # numérotation affichée = page_pdf - 2
    doc.close()
    return pages


def tampon_pieds(pdf: Path, titre: str) -> None:
    from pypdf import PdfReader, PdfWriter
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    n = len(reader.pages)
    for idx, page in enumerate(reader.pages):
        p = idx + 1
        if p == 1 or p == n:
            writer.add_page(page)
            continue
        label = "i" if p == 2 else str(p - 2)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(595.28, 841.89))
        c.setFont("Helvetica", 7.5)
        c.setFillColor(HexColor("#94a3b8"))
        c.drawString(45, 22, titre)
        c.drawRightString(595.28 - 45, 22, label)
        c.save()
        buf.seek(0)
        page.merge_page(PdfReader(io.BytesIO(buf.getvalue())).pages[0])
        writer.add_page(page)
    writer.add_metadata({
        "/Title": f"{titre} (blue-tech v{T['meta']['version']})",
        "/Author": "Z.ai — écosystème KNOWLEDGE",
        "/Creator": "blue-tech.template.json v1.0.0 + generate_test_doc.py",
        "/Subject": "Document de test du modèle par défaut blue-tech",
    })
    with pdf.open("wb") as f:
        writer.write(f)


def main() -> None:
    t0 = time.time()
    HTML_OUT.write_text(build_html(), encoding="utf-8")
    t1 = time.time()
    tmp1 = ROOT / "download/.blue-tech-test-p1.pdf"
    render(tmp1)
    t2 = time.time()
    pages = extraire_pages(tmp1)
    tmp1.unlink(missing_ok=True)
    HTML_OUT.write_text(build_html(toc_pages=pages), encoding="utf-8")
    render(PDF_OUT)
    t3 = time.time()
    tampon_pieds(PDF_OUT, TITLE)
    t4 = time.time()
    print(json.dumps({
        "html_generation_s": round(t1 - t0, 2),
        "render_p1_s": round(t2 - t1, 2),
        "toc_pages_extraites": pages,
        "render_p2_s": round(t3 - t2, 2),
        "tampon_s": round(t4 - t3, 2),
        "total_s": round(t4 - t0, 2),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
