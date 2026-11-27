#!/usr/bin/env python3
"""Task 10 G5 — Résumé illustré PDF de la conversion (ligne creative-flow, blue-tech).

Mise en page : skill mise-en-page (M2 — règles DA-1..DA-8 pendant la génération).
Le PDF est produit par html2pdf-next.js (--nopaged : pagination native Chromium,
repli documenté du skill pdf quand pagedjs n'est pas résolu).
Sortie : assets_tmp/task10/resume-conversion-kps.html
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import os

OUT = "/home/z/my-project/assets_tmp/task10/resume-conversion-kps.html"

CSS = """
@page { size: 794px 1123px; margin: 0; }
:root{
  --bg:#111827; --surface:#1f2937; --accent:#38bdf8; --accent2:#a5b4fc;
  --text:#f8fafc; --muted:#94a3b8; --line:#334155; --fail:#fb923c; /* sémantique échec */
}
html,body{ margin:0; padding:0; width:794px; background:#111827; color:var(--text);
  font-family:'Inter','Noto Sans SC',sans-serif; }
p, td, li{ overflow-wrap:break-word; word-break:break-word; orphans:2; widows:2; }
@media screen { html{ display:flex; justify-content:center; background:#111827; }
  body{ margin:20px auto; } }
.stamp{ position:fixed; bottom:18px; left:64px; right:64px; z-index:50;
  display:flex; justify-content:space-between; align-items:center;
  font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--muted);
  border-top:1px solid var(--line); padding-top:8px; }
.stamp .dot{ color:var(--accent); }

.cover{ width:794px; height:1123px; box-sizing:border-box; break-after:page;
  overflow:hidden; position:relative; display:flex; flex-direction:column;
  justify-content:center; padding:0 70px; }
.cover .grid{ position:absolute; inset:0;
  background-image:linear-gradient(var(--line) 1px, transparent 1px),
                   linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size:64px 64px; opacity:.14; }
.cover .glow{ position:absolute; width:420px; height:420px; border-radius:50%;
  border:2px solid var(--accent); opacity:.16; right:48px; top:64px; }
.cover .glow.b{ width:260px; height:260px; right:130px; top:170px; opacity:.10; }
.cover .badge{ position:relative; font-family:'JetBrains Mono',monospace;
  font-size:12px; letter-spacing:4px; color:var(--accent); text-transform:uppercase;
  border:1px solid var(--accent); border-radius:6px; padding:6px 14px;
  display:inline-block; width:max-content; margin-bottom:34px; }
.cover h1{ position:relative; font-size:47px; font-weight:900; line-height:1.12; margin:0; }
.cover h1 .hl{ color:var(--accent); }
.cover .sub{ position:relative; font-size:16px; color:var(--muted); margin-top:22px;
  line-height:1.6; max-width:580px; }
.cover .meta{ position:relative; margin-top:46px; display:flex; gap:12px; flex-wrap:wrap; max-width:640px; }
.cover .chip{ font-family:'JetBrains Mono',monospace; font-size:11px;
  color:var(--accent2); border:1px solid var(--line); background:var(--surface);
  border-radius:6px; padding:5px 12px; }
.cover .ed{ position:absolute; bottom:60px; left:70px; right:70px;
  display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace;
  font-size:11px; color:var(--muted); padding-top:12px; border-top:1px solid var(--line); }

.toc{ padding:86px 64px 30px 64px; }
.sec-tag, .chapter-header .tag{ font-family:'JetBrains Mono',monospace;
  font-size:11px; letter-spacing:3px; color:var(--accent); text-transform:uppercase; }
.toc h2{ font-size:30px; font-weight:800; margin:8px 0 26px 0; padding-bottom:14px;
  border-bottom:2px solid var(--line); }
.toc .entry{ display:flex; align-items:baseline; gap:14px; padding:11px 0;
  border-bottom:1px dashed var(--line); }
.toc .n{ font-family:'JetBrains Mono',monospace; color:var(--accent); font-size:13px; min-width:30px; }
.toc .t{ font-size:14.5px; font-weight:600; }
.toc .p{ margin-left:auto; font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--muted); }

.main-content{ padding:74px 64px 60px 64px; }
.chapter-header{ break-after:avoid; break-inside:avoid; margin-top:26px; }
.chapter-header h2{ font-size:24px; font-weight:800; margin:6px 0 16px 0; padding-bottom:12px;
  border-bottom:2px solid var(--line); }
h3{ font-size:15px; font-weight:700; margin:18px 0 8px 0; color:var(--accent2);
  break-after:avoid; }
p.body{ font-size:12.5px; line-height:1.72; color:var(--text); margin:0 0 12px 0;
  text-align:left; }
p.body b{ color:var(--accent2); }
.lead{ font-size:13.5px; color:var(--muted); line-height:1.7; margin:0 0 14px 0; }

.fig{ break-inside:avoid; margin:14px 0 16px 0; }
.fig img{ max-width:100%; max-height:500px; height:auto; display:block;
  margin:0 auto; border:1px solid var(--line); border-radius:8px;
  background:var(--surface); padding:6px; box-sizing:border-box; object-fit:contain; }
.fig .cap{ font-size:11px; color:var(--muted); margin-top:8px; line-height:1.5; }
.fig .cap .num{ color:var(--accent); font-family:'JetBrains Mono',monospace; font-weight:700; }
.fig .cap .cr{ color:#64748b; font-size:10px; }
.figrow{ display:flex; gap:14px; flex-wrap:wrap; break-inside:avoid; margin:14px 0 16px 0; }
.figrow .fig{ flex:1 1 300px; margin:0; min-width:260px; max-width:100%; }

table.k{ width:100%; border-collapse:collapse; font-size:11px; margin:12px 0 14px 0;
  break-inside:auto; }
table.k th{ background:#0b1220; color:var(--accent); text-align:left; font-size:10px;
  text-transform:uppercase; letter-spacing:1px; padding:7px 9px; border:1px solid var(--line); }
table.k td{ border:1px solid var(--line); padding:6px 9px; vertical-align:top; line-height:1.5; }
table.k tr{ break-inside:avoid; }
.mono{ font-family:'JetBrains Mono',monospace; font-size:10.5px; }
.badge{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:9.5px;
  font-weight:700; border-radius:4px; padding:1px 7px; border:1px solid; }
.badge.pass{ color:var(--accent); border-color:var(--accent); background:rgba(56,189,248,.08); }
.badge.fail{ color:var(--fail); border-color:var(--fail); background:rgba(251,146,60,.08); }
.card{ break-inside:avoid; border:1px solid var(--line); background:var(--surface);
  border-radius:8px; padding:12px 14px; margin:12px 0 14px 0; font-size:12px;
  line-height:1.65; }
.card .t{ color:var(--accent); font-weight:700; font-size:11px; text-transform:uppercase;
  letter-spacing:1.5px; margin-bottom:6px; font-family:'JetBrains Mono',monospace; }
ul{ margin:6px 0 12px 0; padding-left:20px; }
li{ font-size:12px; line-height:1.65; margin-bottom:5px; }
.cn{ display:inline-block; width:14px; height:14px; line-height:12px; text-align:center;
  border:1.2px solid var(--accent); border-radius:50%; font-size:9.5px; font-weight:700;
  color:var(--accent); vertical-align:-2px; margin:0 1px; }

.ending{ width:794px; height:1123px; box-sizing:border-box; break-before:page;
  overflow:hidden; position:relative; display:flex; flex-direction:column;
  justify-content:center; padding:0 70px; }
.ending .grid{ position:absolute; inset:0;
  background-image:linear-gradient(var(--line) 1px, transparent 1px),
                   linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size:64px 64px; opacity:.12; }
.ending h2{ position:relative; font-size:34px; font-weight:900; margin:0 0 26px 0;
  padding-bottom:14px; border-bottom:2px solid var(--line); }
.ending .rule{ display:none; }
.ending p{ position:relative; font-size:13.5px; color:var(--muted); line-height:1.75; max-width:600px; }
.ending .src{ position:relative; margin-top:40px; font-family:'JetBrains Mono',monospace;
  font-size:10.5px; color:#64748b; line-height:1.8; }
"""

BODY = """
<div class="cover">
  <div class="grid"></div><div class="glow"></div><div class="glow b"></div>
  <div class="badge">CONVERSION STANDARD · KUBOTA PRODUCTION SYSTEM</div>
  <h1>Du standard papier<br>à la fiche <span class="hl">KPS Standardized Work</span></h1>
  <div class="sub">Analyse du « standard non-KPS » <b>MO-MF-013-F</b> — Sous assemblage du tank fuel
    (TA-S-3055-020, rév. D) photographié au poste — et résumé illustré de sa conversion
    en « standard version KPS ». Le standard d'origine est conservé tel quel.</div>
  <div class="meta">
    <span class="chip">source : photo 2479×1723 px</span>
    <span class="chip">audit source : 40 % (C1–C10)</span>
    <span class="chip">fiche convertie : 100 %</span>
    <span class="chip">cycle 144 s / takt 150 s = 96 %</span>
  </div>
  <div class="ed"><span>session web-220878ed · Task 10</span><span>2026-11-27 · mise en page : skill mise-en-page</span></div>
</div>

<div class="toc">
  <div class="sec-tag">SOMMAIRE</div>
  <h2>Six étapes, de la photo au standard converti</h2>
  <div class="entry"><span class="n">01</span><span class="t">Objet et matériau : le standard photographié</span><span class="p">2</span></div>
  <div class="entry"><span class="n">02</span><span class="t">Ce que dit le standard non-KPS — et ce qu'il ne dit pas</span><span class="p">3</span></div>
  <div class="entry"><span class="n">03</span><span class="t">La cible : la fiche KPS Standardized Work</span><span class="p">4</span></div>
  <div class="entry"><span class="n">04</span><span class="t">La conversion, donnée par donnée</span><span class="p">5</span></div>
  <div class="entry"><span class="n">05</span><span class="t">Contrôles et traçabilité</span><span class="p">6</span></div>
  <div class="entry"><span class="n">06</span><span class="t">Réserves et étapes suivantes</span><span class="p">6</span></div>
</div>

<div class="main-content">

  <div class="chapter-header">
    <div class="tag">SECTION 01</div>
    <h2>Objet et matériau : le standard photographié</h2>
  </div>
  <p class="lead">Une photo de poste, un document papier, un objectif : le faire passer du format « standard non-KPS » au format « standard version KPS » — sans jamais altérer l'original.</p>
  <p class="body">La photo reçue le 27 novembre 2026 (<span class="mono">IMG_20261127_131943.jpg</span>, 2479×1723 px) montre un
    <b>standard papier plastifié</b> affiché sur une tôle perforée d'atelier : un « Assemblage Standard »
    référencé <span class="mono">MO-MF-013-F</span>, décrivant le <b>sous-assemblage du tank fuel</b> pour les modèles
    S/P/H, pièce <span class="mono">TA-S-3055-020</span>, en révision D (tampon dateur du 21 octobre 2024). Cinq photos
    d'opération, un cartouche à quatre signataires et un tableau de cinq opérations y cohabitent en une seule
    page dense, annotée à la main par endroits.</p>
  <p class="body">Ce document n'est pas un inconnu dans le projet : c'est <b>le matériau historique du Task 5</b>
    (« Standart non-KPS du réservoir », trois photos analysées par VLM), dont il constitue le jeu de
    démonstration de l'application convertisseur. Le référentiel « KPS » du projet est explicitement le
    <b>Kubota Production System</b> (le PM KPS-2 en interdit l'amalgame avec les systèmes Kawasaki ou Volkswagen).
    La directive du jour est triple : <b>analyser</b> la photo en tant que standard non-KPS, la <b>convertir</b> en
    standard version KPS, et <b>garder</b> le standard non-KPS tel quel — condition remplie par une copie
    d'archive byte-identique, l'original d'entrée restant intact dans <span class="mono">upload/</span>.</p>

  <div class="fig">
    <img src="img/source-full.jpg" alt="Photo du standard non-KPS MO-MF-013-F">
    <div class="cap"><span class="num">Fig. 1</span> — Le standard non-KPS photographié au poste : cartouche, illustrations d'opération et tableau
      d'assemblage sur une seule page plastifiée. <span class="cr">Source : upload/IMG_20261127_131943.jpg, 21/10/2024 — conservée byte-identique (sha256 3d4d5109847d9f51…).</span></div>
  </div>

  <div class="chapter-header">
    <div class="tag">SECTION 02</div>
    <h2>Ce que dit le standard non-KPS — et ce qu'il ne dit pas</h2>
  </div>
  <p class="body">La lecture structurée du document extrait un contenu complet et exploitable :
    un cartouche d'identification (référence documentaire, dossier caractéristiques, modèle S/P/H,
    n° <span class="mono">TA-S-3055-020</span>, page QA <span class="mono">6-425/430</span>) ; quatre signataires datés
    (rédacteur Maxence DEGROOTE, approbateur Fabien BERNAERT, vérificatrices Camille DEBRUGNE et Kazumi D.) ;
    un historique de quatre révisions A→D (initialisation 2022, modification suite ECN 3597, clarification
    suite défaut, ajout d'informations outillage) ; une nomenclature de <b>7 pièces</b> référencées ; et
    <b>5 opérations</b> illustrées avec standards de couple (12–13,5 Nm à l'op. 1, 9–11 Nm à l'op. 5),
    outillage marqué (visseuse 12 V marquage blanc / marquage jaune P20, douille ø 7) et points d'attention.</p>
  <p class="body">Le document a aussi ses silences : le champ « Temps » du cartouche est <b>vide</b> ; les colonnes
    « Kaku » et « Événements » ne sont pas renseignées ; les lignes 6 et 7 du tableau sont vides ; trois opérations
    sur cinq n'ont <b>aucun point de contrôle</b> écrit ; les consignes d'anomalie sont dispersées dans des cellules
    « points d'attention » sans règle centralisée ; et deux corrections terrain (surlignage orange sur les cellules
    outillage, renvoi manuscrit <span class="mono">→ 3J09900482</span>) ne sont pas intégrées proprement. Appliqué
    à cette source, l'algorithme d'audit KPS en 10 critères du projet donne <b>40 %</b> : le fond est là, la
    structure Standardized Work n'existe pas encore.</p>

  <div class="figrow">
    <div class="fig">
      <img src="img/cartouche-source.png" alt="Cartouche du standard source">
      <div class="cap"><span class="num">Fig. 2</span> — Le cartouche source : identité, signataires datés et historique des révisions A→D.
        <span class="cr">Crop de Fig. 1, task10-crops-source.py.</span></div>
    </div>
    <div class="fig">
      <img src="img/tableau-operations.png" alt="Tableau des opérations source">
      <div class="cap"><span class="num">Fig. 3</span> — Le tableau des 5 opérations : séquences, contrôles, standards de couple, outillage, check sheet.
        <span class="cr">Crop de Fig. 1, task10-crops-source.py.</span></div>
    </div>
  </div>

  <h3>Audit KPS de la source (algorithme §6.1 du PM KPS-2 — 10 critères binaires)</h3>
  <table class="k">
    <tr><th style="width:64px">Critère</th><th>Objet</th><th style="width:76px">Source</th><th>Constat sur le standard non-KPS</th></tr>
    <tr><td class="mono">C1</td><td>En-tête (9 champs)</td><td><span class="badge pass">PASS</span></td><td>référence, modèle, n°, page QA, opération, révision, date, rédacteur, approbateur tous présents</td></tr>
    <tr><td class="mono">C2</td><td>Vérification à deux niveaux</td><td><span class="badge pass">PASS</span></td><td>vérificateur 1 et 2 renseignés (nom du second tronqué sur la photo)</td></tr>
    <tr><td class="mono">C3</td><td>Takt Time</td><td><span class="badge fail">FAIL</span></td><td>champ « Temps » vide — le rythme client n'apparaît nulle part</td></tr>
    <tr><td class="mono">C4</td><td>SWIP (en-cours minimal)</td><td><span class="badge fail">FAIL</span></td><td>concept absent du document</td></tr>
    <tr><td class="mono">C5</td><td>Règle d'anomalie</td><td><span class="badge fail">FAIL</span></td><td>consignes dispersées en cellules, aucune règle centralisée</td></tr>
    <tr><td class="mono">C6</td><td>Nomenclature</td><td><span class="badge pass">PASS</span></td><td>7 pièces avec références et quantités</td></tr>
    <tr><td class="mono">C7</td><td>Séquence d'étapes</td><td><span class="badge pass">PASS</span></td><td>5 opérations numérotées 1..5 (lignes 6-7 vides)</td></tr>
    <tr><td class="mono">C8</td><td>Temps par étape</td><td><span class="badge fail">FAIL</span></td><td>aucune décomposition manuel / machine / marche</td></tr>
    <tr><td class="mono">C9</td><td>Points clés + raisons</td><td><span class="badge fail">FAIL</span></td><td>points d'attention sur les op. 2-3 seulement, jamais de « pourquoi »</td></tr>
    <tr><td class="mono">C10</td><td>Autocontrôles systématiques</td><td><span class="badge fail">FAIL</span></td><td>« points de contrôle » vides pour les op. 2, 3 et 4</td></tr>
  </table>
  <p class="body">Score de la source : <b>4 critères PASS sur 10 = 40 %</b>. C'est exactement l'écart que la
    conversion doit combler — sans inventer ce que la source ne dit pas.</p>

  <div class="chapter-header">
    <div class="tag">SECTION 03</div>
    <h2>La cible : la fiche KPS Standardized Work</h2>
  </div>
  <p class="body">La cible de la conversion est définie une fois pour toutes par le PM KPS-2 du projet :
    une <b>fiche KPS Standardized Work</b> qui fusionne les trois feuilles classiques du travail standardisé —
    <i>Standardized Work Chart</i>, <i>Process Capacity Sheet</i>, <i>Standardized Work Combination Table</i> —
    enrichies du dossier de poste. Ce choix de fusion est assumé dans le référentiel : une seule page d'atelier
    contient l'identité, la nomenclature, la séquence, les temps, les points clés et les contrôles.</p>
  <p class="body">La fiche produite est la matérialisation imprimable du modèle de données de l'application
    <span class="mono">kps-converter</span> (Task 5) : mêmes champs, même audit, même jauge Cycle/Takt. Le document
    papier et l'application décrivent donc <b>la même réalité</b> — la fiche peut être imprimée en A4 paysage
    pour le poste, ou importée/re-importée dans l'app sans perte.</p>
  <table class="k">
    <tr><th style="width:170px">Terme Standardized Work</th><th>Définition</th><th style="width:150px">Champ de la fiche</th></tr>
    <tr><td><b>Takt Time</b></td><td>rythme imposé par la demande client (temps disponible / quantité requise)</td><td class="mono">taktTimeSec = 150 s (démonstration)</td></tr>
    <tr><td><b>Work Sequence</b></td><td>séquence d'opérations sûres et de qualité dans le Takt, pièces cerclées ①..⑦</td><td class="mono">stepOrder + workSequence</td></tr>
    <tr><td><b>Décomposition des temps</b></td><td>chaque étape en temps manuel / machine / marche</td><td class="mono">manual/machine/walkTimeSec</td></tr>
    <tr><td><b>SWIP</b></td><td>en-cours standard minimal pour un flux régulier</td><td class="mono">swipUnits = 1</td></tr>
    <tr><td><b>Points clés &amp; raisons</b></td><td>point de vigilance de chaque élément et sa justification (pratique Toyota des « points et raisons »)</td><td class="mono">keyPoint + reasonWhy</td></tr>
    <tr><td><b>Poka-yoke / traçabilité du serrage</b></td><td>anti-erreurs en ligne ; couple et nombre de boulons archivés par outillage connecté</td><td class="mono">qualityCheck + qgFlag (QG2 sur les couples)</td></tr>
  </table>

  <div class="chapter-header">
    <div class="tag">SECTION 04</div>
    <h2>La conversion, donnée par donnée</h2>
  </div>
  <p class="body">La conversion ne réinvente rien : elle <b>transpose</b> ce que la source dit vers les champs
    de la cible, et <b>signale</b> ce qu'elle ne dit pas. Les valeurs manquantes (Takt, SWIP, temps par étape,
    règle d'anomalie) proviennent du jeu de démonstration canonique du projet — le seed §4 du PM KPS-2,
    validé au Task 5 par 26/26 tests et un audit de la fiche démo à 100 % — avec la mention explicite
    « valeurs de démonstration, à remplacer par des chronométrages terrain ». Aucune valeur n'est inventée.</p>
  <table class="k">
    <tr><th style="width:200px">Donnée du standard non-KPS</th><th style="width:170px">Champ KPS cible</th><th>Valeur retenue dans la fiche</th></tr>
    <tr><td>cartouche (référence, modèle, n°, page QA)</td><td class="mono">en-tête</td><td>transposé tel quel (C1 : les 9 champs non vides)</td></tr>
    <tr><td>4 signataires datés + révisions A→D</td><td class="mono">vérification + historique</td><td>transposés ; les révisions figurent sur la page 1 de la fiche</td></tr>
    <tr><td>nomenclature 7 pièces numérotées</td><td class="mono">bomParts ①..⑦</td><td>7 pièces cerclées, composant CSS dédié garanti sur toutes les polices</td></tr>
    <tr><td>5 opérations imprimées + photos « Photo 1..5 »</td><td class="mono">workSequence + photoLabel</td><td>5 étapes avec repères cerclés et les photos d'origine recadrées</td></tr>
    <tr><td>standards de couple (12–13,5 Nm ; 9–11 Nm)</td><td class="mono">keyPoint + qualityCheck</td><td>cibles 13 Nm et 10 Nm tracées, contrôle « Couple de serrage » avec flag QG2</td></tr>
    <tr><td>outillage marqué (12 V blanc / jaune P20, douille ø 7)</td><td class="mono">keyPoint</td><td>reproduit à l'identique + zone « Outillage marqué » sur la page 1</td></tr>
    <tr><td>points d'attention dispersés</td><td class="mono">keyPoint + reasonWhy</td><td>structurés « Point clé » + « Raison » pour les 5 étapes (C9 rétabli)</td></tr>
    <tr><td>check sheet « Pré. » (op. 1, 2, 3, 5)</td><td class="mono">qgFlag</td><td>mapping seed (QG2 sur op. 1-3) — convention du site à confirmer par Méthodes</td></tr>
    <tr><td>champ « Temps » vide</td><td class="mono">manual/machine/walkTimeSec</td><td>décomposition de démonstration : 57+36+14+27+10 = <b>144 s</b></td></tr>
    <tr><td>absent de la source</td><td class="mono">taktTimeSec, swipUnits, abnormalityRule</td><td>150 s (démonstration), 1 unité, règle « arrêter / isoler / alerter le Team Leader »</td></tr>
  </table>
  <p class="body">Deux interprétations sont tracées noir sur blanc : à l'opération 2, le texte imprimé renvoie à
    un « JOINT » absent de la nomenclature — la lecture canonique validée au Task 5 retient
    <span class="cn">5</span> JOINT PIPE dans <span class="cn">3</span> HOSE serré par <span class="cn">4</span> CLAMP,
    et le renvoi manuscrit <span class="mono">3J09900482</span> reste à confirmer ; le nom du Vérificateur 2,
    tronqué sur la photo, est porté à la forme du seed (« Kazumi D. »). L'ambiguïté source est consignée dans
    l'extraction structurée, jamais effacée.</p>

  <div class="figrow">
    <div class="fig">
      <img src="img/page1-thumb.jpg" alt="Page 1 de la fiche KPS convertie">
      <div class="cap"><span class="num">Fig. 4</span> — La fiche convertie, page 1 : cartouche, signataires, KPI (Takt 150 s · SWIP 1 · cycle 144 s · 96 % · audit 100 %),
        localisation, nomenclature cerclée, révisions A→D, outillage et règle d'anomalie. <span class="cr">Fiche KPS TA-S-3055-020, Task 10.</span></div>
    </div>
    <div class="fig">
      <img src="img/page2-thumb.jpg" alt="Page 2 de la fiche KPS convertie">
      <div class="cap"><span class="num">Fig. 5</span> — La fiche convertie, page 2 : 5 opérations avec photo, séquence cerclée, point clé + raison,
        autocontrôle et temps ; jauge Cycle/Takt à 96 %. <span class="cr">Fiche KPS TA-S-3055-020, Task 10.</span></div>
    </div>
  </div>

  <div class="chapter-header">
    <div class="tag">SECTION 05</div>
    <h2>Contrôles et traçabilité</h2>
  </div>
  <p class="body">La fiche n'est pas « livrée parce qu'elle se voit bien » : elle passe les arbitres mécaniques
    de l'écosystème, et chaque affirmation de ce résumé renvoie à une preuve. Une boucle de convergence a été
    jouée (un seul round) : le panneau nomenclature de la page 1 laissait un blanc terminal — il est comblé par
    l'historique réel des révisions A→D ; les cinq opérations de la page 2 se répartissent désormais sur toute
    la hauteur utile, ce qui supprime le vide avant la jauge.</p>
  <table class="k">
    <tr><th style="width:250px">Arbitre / contrôle</th><th style="width:110px">Résultat</th><th>Preuve</th></tr>
    <tr><td>poster_validate <span class="mono">check-html</span></td><td><span class="badge pass">0 erreur</span></td><td>validation pré-rendu du HTML de la fiche (15 avertissements TINY_FONT sur folios — attendus)</td></tr>
    <tr><td>pdf_qa (mode creative)</td><td><span class="badge pass">PASS</span></td><td>10 vérifications : pas de page blanche, pas de débordement, remplissage adéquat, marges symétriques, polices embarquées</td></tr>
    <tr><td>Audit C1–C10 de la fiche convertie</td><td><span class="badge pass">100\u00a0%</span></td><td>recalcul mécanique sur le texte extrait du PDF\u00a0— les 10 critères passent</td></tr>
    <tr><td>Cohérence des temps (seed §4)</td><td><span class="badge pass">144 s / 150 s</span></td><td>somme des 5 étapes recalculée = 144 s ; 144/150 = 96 % = valeur affichée à la jauge</td></tr>
    <tr><td>Garde du standard non-KPS</td><td><span class="badge pass">byte-identique</span></td><td>sha256 de la copie d'archive = sha256 de l'original upload (3d4d5109847d9f51…)</td></tr>
    <tr><td>Propreté du texte PDF</td><td><span class="badge pass">0 défaut</span></td><td>0 caractère U+FFFD, 0 marqueur de placeholder incomplet sur la liste standard</td></tr>
    <tr><td>correct-work (bloc conversion)</td><td><span class="badge pass">10/10</span></td><td><span class="mono">scripts/cw-task10-conversion-report.json</span>\u00a0— 5 findings corrigés en vol, rapport <span class="mono">download/rapport-cw-task10-conversion.md</span></td></tr>
  </table>

  <div class="chapter-header">
    <div class="tag">SECTION 06</div>
    <h2>Réserves et étapes suivantes</h2>
  </div>
  <p class="body">La conversion est traçable et complète, mais quatre points restent des
    <b>hypothèses assumées</b> — ils figurent dans le document et dans l'extraction structurée, jamais
    dissimulés : la signification exacte des flags QG1/QG2/Pré. (convention qualité du site) ; la source du
    Takt (planning ou mesure) ; les temps par étape, qui sont des valeurs de démonstration à remplacer par des
    chronométrages terrain ; le nom complet du Vérificateur 2 et la référence manuscrite
    <span class="mono">3J09900482</span>. Le service Méthodes est le seul arbitre de ces quatre points.</p>
  <ul>
    <li><b>Faire valider la fiche par le service Méthodes</b> — c'est le passage obligé avant tout usage production (règle du projet : ne jamais inventer ce que le document source ne dit pas).</li>
    <li><b>Chronométrer les 5 opérations au poste</b> puis remplacer les temps de démonstration ; la jauge Cycle/Takt se recalcule automatiquement dans l'application.</li>
    <li><b>Reprendre les photos d'opération au poste</b> si l'on veut des vignettes plus lisibles que les crops de la source (photos imprimées sombres) ; la fiche accepte une photo par étape.</li>
    <li><b>Rejouer la fiche dans l'application</b> <span class="mono">kps-converter</span> : l'import JSON de la fiche met à jour TA-S-3055-020 sans doublon (idempotence documentée), et le panneau d'audit doit afficher 100 %.</li>
    <li><b>Conserver le standard non-KPS comme référence</b> : la conversion ne remplace rien — la source reste le document opposable, la fiche en est la version Standardized Work.</li>
  </ul>
  <div class="card">
    <div class="t">L'essentiel</div>
    Le standard non-KPS (40\u00a0%) disait <b>quoi faire</b>\u00a0; la fiche KPS (100\u00a0%) dit aussi <b>combien de temps</b>,
    <b>pourquoi</b>, et <b>quoi contrôler</b>\u00a0— avec le même contenu source, les mêmes photos, et aucune donnée
    inventée\u00a0: tout ce qui manquait est signalé comme démonstration ou hypothèse à valider.
  </div>

  <h3>Inventaire des livrables du Task 10</h3>
  <table class="k">
    <tr><th style="width:270px">Livrable</th><th>Rôle</th><th style="width:110px">Statut</th></tr>
    <tr><td class="mono">download/fiche-kps-standardized-work-TA-S-3055-020.pdf</td><td>la conversion\u00a0: fiche KPS Standardized Work 2\u00a0pages A4 paysage</td><td><span class="badge pass">livré</span></td></tr>
    <tr><td class="mono">download/extraction-standard-non-KPS-MO-MF-013-F.json</td><td>l'analyse structurée de la source (audit 40\u00a0%, hypothèses tracées)</td><td><span class="badge pass">livré</span></td></tr>
    <tr><td class="mono">download/source-standard-non-KPS-MO-MF-013-F.jpg</td><td>la garde du standard non-KPS, byte-identique à l'original</td><td><span class="badge pass">livré</span></td></tr>
    <tr><td class="mono">download/resume-conversion-kps-bluetech.pdf</td><td>le présent résumé illustré de la conversion</td><td><span class="badge pass">livré</span></td></tr>
    <tr><td class="mono">download/rapport-cw-task10-conversion.md</td><td>le rapport correct-work du bloc conversion (10/10)</td><td><span class="badge pass">livré</span></td></tr>
    <tr><td class="mono">assets_tmp/task10-crops/ (9 crops)</td><td>les illustrations recadrées du standard source (photos 1-5, localisation, outillage, cartouche, tableau)</td><td><span class="badge pass">livré</span></td></tr>
  </table>

</div>

<div class="ending">
  <div class="grid"></div>
  <h2>Un même document,<br>deux statuts</h2>
  <p>Le standard non-KPS reste la référence opposable du poste — conservé byte-identique.
     La fiche KPS Standardized Work en est la version structurée : séquence, temps, points clés,
     raisons, contrôles et Takt, prête pour le chronométrage terrain et la validation Méthodes.</p>
  <div class="src">
    Sources — upload/IMG_20261127_131943.jpg (standard non-KPS, conservé) · PM KPS-2 v2.1 §0/§4/§6 (seed canonique, validé Task 5) · analyse-photos-reservoir.json (Task 5)<br>
    Livrables — fiche-kps-standardized-work-TA-S-3055-020.pdf · extraction-standard-non-KPS-MO-MF-013-F.json · source-standard-non-KPS-MO-MF-013-F.jpg<br>
    Généré le 2026-11-27 · session web-220878ed, Task 10 · mise en page : skill mise-en-page (DA-1..DA-8) · ligne creative-flow blue-tech
  </div>
</div>
"""

html = ("<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>Conversion standard non-KPS vers KPS — résumé illustré (MO-MF-013-F)</title>\n"
        "<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900"
        "&family=JetBrains+Mono:wght@400;700&display=swap\" rel=\"stylesheet\">\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n{BODY}\n</body>\n</html>\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("HTML :", OUT, f"({os.path.getsize(OUT)} octets)")
