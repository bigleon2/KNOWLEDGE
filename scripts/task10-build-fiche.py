#!/usr/bin/env python3
"""Task 10 G2 — Génère la fiche KPS Standardized Work (conversion du standard non-KPS MO-MF-013-F).

Source canonique des valeurs : seed §4 du PM KPS-2 (validé Task 5).
Format : A4 paysage (1123x794 px), 2 pages, palette imposée PM §6.
Sortie : assets_tmp/task10/fiche-kps-standardized-work.html (+ images copiées).
Le PDF est produit ensuite par html2pdf-next.js (règle ferme du skill pdf).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import os
import shutil

BASE = "/home/z/my-project"
OUT_DIR = f"{BASE}/assets_tmp/task10"
IMG_DIR = f"{OUT_DIR}/img"
CROPS = f"{BASE}/assets_tmp/task10-crops"
os.makedirs(IMG_DIR, exist_ok=True)

IMGS = ["localisation-tank", "outillage-visses", "photo1-valve-bolt",
        "photo2-hose-clamp", "photo3-clamp-detail", "photo4-jointpipe",
        "photo5-screw-m5"]
for n in IMGS:
    shutil.copy2(f"{CROPS}/{n}.png", f"{IMG_DIR}/{n}.png")

# ---- Données canoniques (seed §4 PM KPS-2 — validé Task 5) ----
HEADER = {
    "reference": "MO-MF-013-F", "dossier": "Dossier Caractéristiques",
    "modele": "S/P/H", "numero": "TA-S-3055-020", "qa": "6-425/430",
    "operation": "Sous assemblage du tank fuel", "rev": "D",
    "date": "21/10/2024",
    "redacteur": ("Maxence DEGROOTE", "Floteur qualité", "23/09/2024"),
    "approbateur": ("Fabien BERNAERT", "Team leader", "23/09/2024"),
    "verif1": ("Camille DEBRUGNE", "Team Leader FLQ / FLQ multilignes", "18/10/2024"),
    "verif2": ("Kazumi D.", "Assistant production / Quality control (kaku S)", "21/10/2024"),
    "takt": 150, "swip": 1, "cycle": 144,
    "anomalie": ("En cas d'anomalie pièce, couple ou outil (visseuses marquage jaune P20 / "
                 "marquage blanc) : arrêter l'opération, isoler la pièce et alerter le Team Leader."),
}
NOMENCLATURE = [
    (1, "3J070-1002-", "VALVE (COOLANT)", 1),
    (2, "3J099-2737-1", "BOLT (EN 1665, M8-60, C8.8)", 3),
    (3, "3J037-3096-", "HOSE", 1),
    (4, "3J033-9475-", "CLAMP", 2),
    (5, "3S205-0552-", "JOINT PIPE", 2),
    (6, "3J037-3093-", "HOSE", 1),
    (7, "3J099-0000-3", "SCREW M5", 1),
]
STEPS = [
    {"n": 1, "img": "photo1-valve-bolt", "photo": "Photo 1", "parts": [1, 2],
     "seq": "Assembler [1] VALVE COOLANT avec [2] BOLT (x3) et serrer",
     "kp": "Visseuse 12V puis clé dynamométrique — couple 12~13,5 Nm (cible 13 Nm)",
     "raison": "Garantir le couple de serrage et éviter la défaillance de la pièce",
     "ctrl": "Couple de serrage", "flag": "QG2", "t": (38, 15, 4)},
    {"n": 2, "img": "photo2-hose-clamp", "photo": "Photo 2", "parts": [3, 4, 5],
     "seq": "Assembler [5] JOINT PIPE dans [3] HOSE et serrer avec [4] CLAMP",
     "kp": "Visseuse 12V marquage jaune (puissance 20) + douille ø 7 (distinguer de la visseuse marquage blanc) ; positionner le collier à ~0,5 cm du bord du hose",
     "raison": "Assurer l'étanchéité et le maintien mécanique du collier",
     "ctrl": "Positionnement collier et serrage", "flag": "QG2", "t": (25, 8, 3)},
    {"n": 3, "img": "photo3-clamp-detail", "photo": "Photo 3", "parts": [1, 3, 5],
     "seq": "Insérer l'ensemble [5]+[3] dans [1] VALVE COOLANT et verrouiller le clip",
     "kp": "Vérifier que le clip plastique du [5] JOINT PIPE maintient les deux parties (joint pipe + valve coolant)",
     "raison": "Éviter tout déboîtement ou fuite en service",
     "ctrl": "Verrouillage clip plastique", "flag": "QG2", "t": (12, 0, 2)},
    {"n": 4, "img": "photo4-jointpipe", "photo": "Photo 4", "parts": [4, 5, 6],
     "seq": "Assembler [5] JOINT PIPE dans [6] HOSE et serrer avec [4] CLAMP",
     "kp": "Visseuse 12V marquage jaune (P20) + douille ø 7 ; ne pas connecter sur la valve coolant (voir TA-M-3131-100)",
     "raison": "Respecter le routage du sous-assemblage avant montage final",
     "ctrl": "Routage conforme TA-M-3131-100", "flag": "Aucun", "t": (18, 6, 3)},
    {"n": 5, "img": "photo5-screw-m5", "photo": "Photo 5", "parts": [7],
     "seq": "Assembler [7] SCREW M5 et serrer",
     "kp": "Clé dynamométrique — couple 9~11 Nm (cible 10 Nm)",
     "raison": "Éviter le desserrage et détecter toute pièce oxydée (rouille / défaut d'aspect)",
     "ctrl": "Couple de serrage + contrôle aspect", "flag": "Aucun", "t": (9, 0, 1)},
]
assert sum(s["t"][0] + s["t"][1] + s["t"][2] for s in STEPS) == HEADER["cycle"], "somme temps != cycle"
pct = round(HEADER["cycle"] / HEADER["takt"] * 100)

def cn(i):
    """Chiffre cerclé — composant CSS dédié (PM §6, garantie d'affichage)."""
    return f'<span class="cn">{i}</span>'

def seq_html(seq):
    out, buf = [], ""
    for ch in seq:
        if ch == "[":
            out.append(buf); buf = ""
        elif ch == "]":
            num, buf2 = buf, ""
            out.append(cn(num)); buf = ""
        else:
            buf += ch
    out.append(buf)
    return "".join(out)

def t_cell(t):
    return (f'<td class="t-c"><b>{t[0]}</b></td><td class="t-c"><b>{t[1]}</b></td>'
            f'<td class="t-c"><b>{t[2]}</b></td><td class="t-c tot"><b>{sum(t)}</b></td>')

# ---- nomenclature rows ----
nomen_rows = "".join(
    f'<tr><td class="c">{cn(n)}</td><td class="mono">{ref}</td><td>{des}</td><td class="c"><b>{q}</b></td></tr>'
    for n, ref, des, q in NOMENCLATURE)

# ---- historique des révisions A-D (source : cartouche du standard photographié) ----
REVISIONS = [
    ("A", "23/06/2022", "Initialisation", "Bruno.W"),
    ("B", "10/01/2024", "Modification suite ECN 3597", "DEGROOTE.M"),
    ("C", "22/02/2024", "Clarification suite défaut", "DEGROOTE.M"),
    ("D", "23/09/2024", "Ajout d'informations outillage", "DEGROOTE.M"),
]
rev_rows = "".join(
    f'<tr><td class="c"><b>{r}</b></td><td class="mono">{d}</td><td>{raison}</td><td class="mono">{resp}</td></tr>'
    for r, d, raison, resp in REVISIONS)

# ---- étapes (page 2) ----
step_rows = ""
for s in STEPS:
    badge = 'qg2' if s["flag"] == "QG2" else 'qgn'
    step_rows += f'''
<div class="op">
  <div class="op-img"><img src="img/{s["img"]}.png" alt="{s["photo"]}"><span class="ph">{s["photo"]}</span></div>
  <div class="op-seq"><div class="op-n">Op. {s["n"]}</div>
    <div class="op-txt">{seq_html(s["seq"])}</div>
    <div class="op-parts">pièces : {" ".join(cn(p) for p in s["parts"])}</div></div>
  <div class="op-kp"><span class="lbl">Point clé</span> {s["kp"]}<br><span class="lbl">Raison</span> {s["raison"]}</div>
  <div class="op-ctrl"><span class="lbl">Autocontrôle</span><br>{s["ctrl"]}<br><span class="flag {badge}">{s["flag"]}</span></div>
  <table class="t"><tr><th>Man.</th><th>Mach.</th><th>Marche</th><th>Σ s</th></tr>
    <tr>{t_cell(s["t"])}</tr></table>
</div>'''

html = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Fiche KPS Standardized Work — TA-S-3055-020 (convertie depuis MO-MF-013-F)</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
@page { size: 1123px 794px; margin: 0; }
:root{
  --bg:#F8FAFC; --surface:#FFFFFF; --line:#CBD5E1; --primary:#1E40AF;
  --ok:#15803D; --warn:#B45309; --ink:#0F172A; --muted:#475569;
}
html,body{ margin:0; padding:0; width:1123px; background:var(--bg); color:var(--ink);
  font-family:'Inter','Noto Sans SC',sans-serif; font-size:12px; }
*{ box-sizing:border-box; }
.mono{ font-family:'JetBrains Mono',monospace; }
.sheet{ width:1123px; height:794px; padding:22px 30px 16px 30px; break-after:page;
  overflow:hidden; display:flex; flex-direction:column; gap:9px; position:relative; }
.sheet.p2{ break-after:auto; }

/* chiffres cerclés (composant dédié PM §6) */
.cn{ display:inline-block; width:15px; height:15px; line-height:13px; text-align:center;
  border:1.4px solid var(--primary); border-radius:50%; font-size:10px; font-weight:700;
  color:var(--primary); vertical-align:-2px; margin:0 1px; background:var(--surface); }

/* ---- cartouche ---- */
.top{ display:flex; align-items:stretch; gap:8px; }
.brand{ flex:1; border:2px solid var(--primary); border-radius:6px; padding:8px 14px; background:var(--surface); }
.brand .kicker{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:3px;
  color:var(--primary); text-transform:uppercase; }
.brand h1{ margin:2px 0 3px 0; font-size:23px; font-weight:900; color:var(--ink); }
.brand .opline{ font-size:13px; font-weight:600; color:var(--muted); }
.idbox{ border:1px solid var(--line); border-radius:6px; background:var(--surface);
  padding:6px 10px; font-size:11px; line-height:1.5; min-width:170px; }
.idbox .k{ color:var(--muted); font-size:10px; text-transform:uppercase; letter-spacing:1px; }
.idbox b{ font-size:12px; }
.revbadge{ border:2px solid var(--primary); color:var(--primary); border-radius:6px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:4px 12px; font-weight:800; background:var(--surface); }
.revbadge .v{ font-size:22px; }
.revbadge .l{ font-size:9px; font-family:'JetBrains Mono',monospace; letter-spacing:1px; }

.signs{ display:flex; gap:8px; }
.sign{ flex:1; border:1px solid var(--line); border-radius:6px; background:var(--surface); padding:5px 10px; }
.sign .r{ font-size:9.5px; text-transform:uppercase; letter-spacing:1px; color:var(--muted); }
.sign .n{ font-weight:800; font-size:12.5px; margin:1px 0; }
.sign .f{ font-size:10px; color:var(--muted); }
.sign .d{ font-family:'JetBrains Mono',monospace; font-size:9.5px; color:var(--muted); }

.kpis{ display:flex; gap:8px; }
.kpi{ flex:1; border:1px solid var(--line); border-left:4px solid var(--primary); border-radius:6px;
  background:var(--surface); padding:5px 10px; }
.kpi.ok{ border-left-color:var(--ok); }
.kpi.warn{ border-left-color:var(--warn); }
.kpi .v{ font-size:16px; font-weight:900; }
.kpi .v small{ font-size:10px; font-weight:600; color:var(--muted); }
.kpi .k{ font-size:9.5px; text-transform:uppercase; letter-spacing:1px; color:var(--muted); }

/* ---- zone médiane page 1 ---- */
.mid{ display:flex; gap:10px; flex:1; min-height:0; }
.panel{ border:1px solid var(--line); border-radius:6px; background:var(--surface); padding:8px 10px; }
.panel h3{ margin:0 0 6px 0; font-size:11px; text-transform:uppercase; letter-spacing:1.5px;
  color:var(--primary); border-bottom:2px solid var(--primary); padding-bottom:4px; }
.p-loc{ flex:0 0 300px; display:flex; flex-direction:column; }
.p-loc img{ width:100%; max-height:270px; object-fit:contain; border-radius:4px; }
.p-nom{ flex:1; }
.p-out{ flex:0 0 300px; display:flex; flex-direction:column; }
.p-out img{ width:100%; max-height:150px; object-fit:cover; border-radius:4px; }
caption-side{ }
table.nom{ width:100%; border-collapse:collapse; font-size:10.5px; }
table.nom th{ background:#EFF6FF; color:var(--primary); font-size:9.5px; text-transform:uppercase;
  letter-spacing:1px; padding:3px 6px; border:1px solid var(--line); }
table.nom td{ border:1px solid var(--line); padding:3px 6px; }
td.c{ text-align:center; }
.anomalie{ margin-top:8px; border:1.5px solid var(--warn); background:#FFFBEB;
  border-radius:6px; padding:7px 10px; font-size:10.5px; line-height:1.45; color:#7C4A03; }
.anomalie b{ color:var(--warn); text-transform:uppercase; font-size:9.5px; letter-spacing:1px; }
.cap{ font-size:9px; color:var(--muted); margin-top:4px; line-height:1.35; }

/* ---- page 2 : opérations ---- */
.h2row{ display:flex; justify-content:space-between; align-items:baseline;
  border-bottom:2px solid var(--primary); padding-bottom:5px; }
.h2row h2{ margin:0; font-size:16px; font-weight:900; }
.h2row .ref{ font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--muted); }
.ops{ display:flex; flex-direction:column; gap:7px; flex:1; min-height:0; }
.op{ display:flex; gap:9px; border:1px solid var(--line); border-radius:6px; background:var(--surface);
  padding:6px 8px; align-items:stretch; flex:1; min-height:0; }
.op-img{ flex:0 0 118px; position:relative; }
.op-img img{ width:118px; height:78px; object-fit:cover; border-radius:4px; border:1px solid var(--line); }
.op-img .ph{ position:absolute; bottom:4px; left:4px; background:rgba(15,23,42,.78); color:#fff;
  font-family:'JetBrains Mono',monospace; font-size:8.5px; padding:1px 5px; border-radius:3px; }
.op-seq{ flex:0 0 250px; }
.op-n{ font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--primary);
  font-weight:700; letter-spacing:1px; }
.op-txt{ font-size:11.5px; font-weight:600; line-height:1.4; margin-top:2px; }
.op-parts{ font-size:9.5px; color:var(--muted); margin-top:3px; }
.op-kp{ flex:1; font-size:10px; line-height:1.45; border-left:1px dashed var(--line); padding-left:9px; }
.op-ctrl{ flex:0 0 168px; font-size:10px; line-height:1.4; border-left:1px dashed var(--line); padding-left:9px; }
.lbl{ display:inline-block; font-size:8.5px; text-transform:uppercase; letter-spacing:1px;
  color:var(--primary); font-weight:700; }
.flag{ display:inline-block; margin-top:3px; font-family:'JetBrains Mono',monospace; font-size:9px;
  font-weight:700; border-radius:4px; padding:1px 7px; }
.flag.qg2{ background:#EFF6FF; color:var(--primary); border:1px solid var(--primary); }
.flag.qgn{ background:#F1F5F9; color:var(--muted); border:1px solid var(--line); }
table.t{ border-collapse:collapse; font-size:10px; align-self:center; }
table.t th{ background:#EFF6FF; color:var(--primary); font-size:8.5px; padding:2px 6px;
  border:1px solid var(--line); text-transform:uppercase; letter-spacing:.5px; }
table.t td{ border:1px solid var(--line); padding:2px 6px; text-align:center; }
table.t td.tot{ background:#F0FDF4; color:var(--ok); }
.gaugebox{ border:1px solid var(--line); border-radius:6px; background:var(--surface); padding:7px 12px; }
.gauge-head{ display:flex; justify-content:space-between; align-items:baseline; font-size:10.5px; }
.gauge-bar{ position:relative; height:16px; background:#E2E8F0; border-radius:8px; margin-top:5px; }
.gauge-fill{ position:absolute; left:0; top:0; bottom:0; width:96%; background:var(--ok);
  border-radius:8px 0 0 8px; }
.gauge-tick{ position:absolute; right:4%; top:-3px; bottom:-3px; width:2px; background:var(--ink); }
.gauge-lbl{ position:absolute; left:calc(96% - 46px); top:0; font-size:9px; font-weight:800;
  color:#fff; line-height:16px; }
.note{ font-size:9px; color:var(--muted); margin-top:4px; }
.foot{ display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace;
  font-size:9px; color:var(--muted); border-top:1px solid var(--line); padding-top:5px; }
.foot .dot{ color:var(--primary); }
</style>
</head>
<body>

<!-- ================= PAGE 1 ================= -->
<div class="sheet">
  <div class="top">
    <div class="brand">
      <div class="kicker">FICHE KPS — STANDARDIZED WORK · CONVERTIE</div>
      <h1>__OPERATION__</h1>
      <div class="opline">Modèle <b>__MODELE__</b> · N° <b>__NUMERO__</b> · Page QA <b>__QA__</b> · Référence documentaire source : <b>__REF__</b></div>
    </div>
    <div class="idbox">
      <span class="k">Dossier</span><br>__DOSSIER__<br>
      <span class="k">Date d'effet</span><br><b>__DATE__</b><br>
      <span class="k">Historique</span><br><span class="mono">A 23/06/2022 · B 10/01/2024<br>C 22/02/2024 · D 23/09/2024</span>
    </div>
    <div class="revbadge"><span class="l">RÉVISION</span><span class="v">D</span><span class="l">EN VIGUEUR</span></div>
  </div>

  <div class="signs">
    <div class="sign"><div class="r">Rédacteur</div><div class="n">__RED_N__</div><div class="f">__RED_F__</div><div class="d">__RED_D__</div></div>
    <div class="sign"><div class="r">Approbateur</div><div class="n">__APP_N__</div><div class="f">__APP_F__</div><div class="d">__APP_D__</div></div>
    <div class="sign"><div class="r">Vérificateur 1</div><div class="n">__V1_N__</div><div class="f">__V1_F__</div><div class="d">__V1_D__</div></div>
    <div class="sign"><div class="r">Vérificateur 2</div><div class="n">__V2_N__</div><div class="f">__V2_F__</div><div class="d">__V2_D__</div></div>
  </div>

  <div class="kpis">
    <div class="kpi warn"><div class="k">Takt Time <small>(démonstration)</small></div><div class="v">150 <small>s</small></div></div>
    <div class="kpi"><div class="k">SWIP (en-cours mini)</div><div class="v">1 <small>unité</small></div></div>
    <div class="kpi"><div class="k">Cycle total (5 opérations)</div><div class="v">144 <small>s</small></div></div>
    <div class="kpi ok"><div class="k">Charge Cycle / Takt</div><div class="v">96 <small>%</small></div></div>
    <div class="kpi ok"><div class="k">Audit KPS C1–C10</div><div class="v">100 <small>%</small></div></div>
  </div>

  <div class="mid">
    <div class="panel p-loc">
      <h3>Localisation d'assemblage</h3>
      <img src="img/localisation-tank.png" alt="Localisation d'assemblage sur le tank fuel">
      <div class="cap">Zone d'implantation du circuit entourée en pointillés — photo extraite du standard source MO-MF-013-F.</div>
    </div>
    <div class="panel p-nom">
      <h3>Nomenclature — 7 pièces cerclées</h3>
      <table class="nom">
        <tr><th style="width:34px">N°</th><th style="width:120px">Référence</th><th>Désignation</th><th style="width:40px">Qté</th></tr>
        __NOMEN__
      </table>
      <div class="cap">Les repères cerclés ①..⑦ renvoient aux opérations de la page 2 (composant CSS dédié, garanti sur toutes les polices d'atelier).</div>
      <h3 style="margin-top:9px">Historique des révisions</h3>
      <table class="nom">
        <tr><th style="width:38px">Rév.</th><th style="width:86px">Date</th><th>Raison</th><th style="width:92px">Resp.</th></tr>
        __REVS__
      </table>
    </div>
    <div class="panel p-out">
      <h3>Outillage marqué</h3>
      <img src="img/outillage-visses.png" alt="Visseuses marquées blanc et jaune">
      <div class="anomalie"><b>Règle d'anomalie</b><br>__ANOMALIE__</div>
    </div>
  </div>

  <div class="foot">
    <span>Conversion « standard non-KPS » <span class="dot">→</span> « standard version KPS » · source MO-MF-013-F conservée telle quelle (sha256 3d4d5109847d9f51)</span>
    <span>fiche KPS · page 1/2 · 2026-11-27</span>
  </div>
</div>

<!-- ================= PAGE 2 ================= -->
<div class="sheet p2">
  <div class="h2row">
    <h2>Séquence d'opérations — Work Sequence, Points clés &amp; Raisons, Autocontrôles</h2>
    <div class="ref">__NUMERO__ · rév D · Takt 150 s</div>
  </div>

  <div class="ops">
__STEPS__
  </div>

  <div class="gaugebox">
    <div class="gauge-head">
      <span><b>Jauge Cycle vs Takt</b> — somme des temps 144 s pour un Takt de 150 s</span>
      <span class="mono" style="color:var(--ok);font-weight:700">96 % de charge</span>
    </div>
    <div class="gauge-bar"><div class="gauge-fill"></div><div class="gauge-lbl">144 s / 150 s</div><div class="gauge-tick"></div></div>
    <div class="note">Temps manuel / machine / marche = valeurs de démonstration du convertisseur (seed §4) — à remplacer par des chronométrages terrain avant usage production. Flags QG1/QG2/Pré. = convention qualité du site, à confirmer par le service Méthodes.</div>
  </div>

  <div class="foot">
    <span>Les 5 photos « Photo n » sont extraites du standard source MO-MF-013-F · conversions d'après PM KPS-2 §4 (validé 26/26 tests)</span>
    <span>fiche KPS · page 2/2 · 2026-11-27</span>
  </div>
</div>

</body>
</html>
"""

repl = {
    "__OPERATION__": HEADER["operation"].upper(),
    "__MODELE__": HEADER["modele"], "__NUMERO__": HEADER["numero"],
    "__QA__": HEADER["qa"], "__REF__": HEADER["reference"],
    "__DOSSIER__": HEADER["dossier"], "__DATE__": HEADER["date"],
    "__ANOMALIE__": HEADER["anomalie"],
    "__RED_N__": HEADER["redacteur"][0], "__RED_F__": HEADER["redacteur"][1], "__RED_D__": HEADER["redacteur"][2],
    "__APP_N__": HEADER["approbateur"][0], "__APP_F__": HEADER["approbateur"][1], "__APP_D__": HEADER["approbateur"][2],
    "__V1_N__": HEADER["verif1"][0], "__V1_F__": HEADER["verif1"][1], "__V1_D__": HEADER["verif1"][2],
    "__V2_N__": HEADER["verif2"][0], "__V2_F__": HEADER["verif2"][1], "__V2_D__": HEADER["verif2"][2],
    "__NOMEN__": nomen_rows, "__STEPS__": step_rows, "__REVS__": rev_rows,
}
for k, v in repl.items():
    html = html.replace(k, v)

assert "__" not in html.replace("__proto__", ""), "jeton non remplacé"
out_html = f"{OUT_DIR}/fiche-kps-standardized-work.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)
print("HTML :", out_html, f"({os.path.getsize(out_html)} octets) · jauge {pct} %")
