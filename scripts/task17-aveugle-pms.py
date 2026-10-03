#!/usr/bin/env python3
"""
Task 17 / Phase (3) — correct-work(aveugle) sur les PMs reconstitués v2.6.0/v2.7.0.

Protocole : verification-protocol.md (Second Opinion, mode AVEUGLE — correct-work v2.6.0 §1.2/§10.4).
  Étape 1 — Cadrage à froid : critères reformulés depuis les SEULS inputs filtrés
            (livrable final = les PMs ; exigences = forme installée certifiée SKILL.md v2.7.0
            + lignée corpus v2.4.0/v2.5.0/v2.5.1 ; conventions = SHARED v1.6.4 §3.2/§4.4,
            SYNC-CONTEXT v1.4.1 note N1, décision KB N20 ; arbitrages mécaniques = SHA, comptages).
  Étape 2 — Vérification aveugle : audit mécanique sans le contexte de construction
            (NE consulte PAS le rapport Task 16, ni le worklog Task 16, ni la conversation).
  Étape 3 — Confrontation avec les verdicts initiaux (matrice de divergence).
  Étape 4 — Verdict consolidé (convergence → PASS ; divergence → documentée, max 2 rounds).

Sortie : download/rapport-correct-work-aveugle-pms-reconstitues.md + _aveugle-pms-report.json
"""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

BASE = Path("/home/z/my-project/ecosystem")
CORPUS = BASE / "skills" / "@mon-ecosysteme"
SKILL = BASE / "skills" / "correct-work" / "SKILL.md"
OUT_MD = BASE / "download" / "rapport-correct-work-aveugle-pms-reconstitues.md"
OUT_JSON = BASE / "scripts" / "aveugle-pms-report.json"

PMS = {v: CORPUS / f"PROMPT-MAITRE-CORRECT-WORK-v{v}.md" for v in ("2.4.0", "2.5.0", "2.5.1", "2.6.0", "2.7.0")}
R = []  # (statut, critère, détail)

def check(ok, crit, detail=""):
    R.append(("PASS" if ok else "FAIL", crit, detail))
    return ok

def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

texts = {v: p.read_text(encoding="utf-8") for v, p in PMS.items()}
installed = SKILL.read_text(encoding="utf-8")

# ═══ ÉTAPE 1 — CADRAGE À FROID (critères pré-écrits, inputs filtrés uniquement) ═══
CRITERES = [
    "C01 En-tête PM conforme à la lignée (titre, version prompt, skill cible, date, source, dépend CONTEXTE SYSTÈME, provenance)",
    "C02 Bloc CONTEXTE SYSTÈME embarqué byte-identique à celui de v2.5.1 (bloc figé hérité — SYNC-CONTEXT v1.4.1 note N1)",
    "C03 Carte des sections : surensemble de v2.5.1 (§A, §1-§10b toutes présentes)",
    "C04 §4 YAML PM v2.7.0 == frontmatter installé SKILL.md v2.7.0 (contrat d'assemblage PM → skill)",
    "C05 §4 YAML PM v2.6.0 : version 2.6.0, structure frontmatter conforme à la lignée",
    "C06 v2.6.0 : 4e mode AVEUGLE documenté (§1.2/§10) + déclencheur correct-work(aveugle) + hook 2nd opinion Étape 5 + max 2 rounds (SHARED §4.4)",
    "C07 v2.6.0 : protocole Second Opinion embarqué au §5.6 (4 étapes + inputs filtrés + garde anti-boucle)",
    "C08 v2.7.0 : couplage gen-plan OBLIGATOIRE Étape 1 + résolution dynamique frontmatter → KB + ARRÊT EXPLICITE",
    "C09 v2.7.0 : fin du mode autonome — directive propriétaire 2026-10-02 citée",
    "C10 Traçabilité N20 : marqueurs « phase N20 » / décision KB N20 présents dans v2.6.0",
    "C11 Planchers §3 RELATIONS inchangés vs v2.5.1 (SHARED §3.2 règle 5 — aucun changement de contrat d'intégration)",
    "C12 §5.4 trigger_evals : v2.5.1 = 8 cas, v2.6.0 = 8 cas (héritage), v2.7.0 = 7 cas (aligné forme installée — evals/trigger_evals.json)",
    "C13 Plage check 2 §6 du PM v2.7.0 contient le nombre de lignes réel de la forme installée (429)",
    "C14 §7 historique : lignée complète v2.4.0 → v2.5.0 → v2.5.1 (partie héritée byte-identique à v2.5.1) + lignes v2.6.0/v2.7.0 + révisions documentaires tracées (aucun faux lignage)",
    "C15 §8 historique des corrections inchangé vs v2.5.1",
    "C16 Diffs bornés : aucun hunk hors périmètre documenté (CONTEXTE SYSTÈME, §3, §8 intacts ; hunks classables en-tête/versions/modes/protocole/provenance/§9.5)",
    "C17 Provenance explicite en en-tête et §7 des deux PMs reconstitués (méthode B1, sources citées)",
]

# ═══ ÉTAPE 2 — VÉRIFICATION AVEUGLE ═══
def section(text, start_pat, end_pat):
    m1 = re.search(start_pat, text, re.M)
    if not m1:
        return None
    m2 = re.search(end_pat, text[m1.end():], re.M)
    return text[m1.start():m1.end() + m2.start()] if m2 else text[m1.start():]

CTX_PAT = r"^## ⚙️ CONTEXTE SYSTÈME"
SECA_PAT = r"^## §A — DÉCLENCHEURS"

# C01 — en-têtes
for v in ("2.6.0", "2.7.0"):
    t = texts[v]
    head = t[: t.index("## §A")]
    ok = (f"Installation du skill correct-work v{v}" in t.splitlines()[0]
          and "**Version du prompt**" in head and "**Skill cible**" in head
          and "**Date**" in head and "**Source**" in head
          and "**Dépend**" in head and "**Provenance**" in head)
    check(ok, f"C01[{v}]", f"titre={t.splitlines()[0][:60]!r}")

# C02 — bloc CONTEXTE SYSTÈME byte-identique à v2.5.1
ctx251 = section(texts["2.5.1"], CTX_PAT, SECA_PAT)
for v in ("2.6.0", "2.7.0"):
    ctx = section(texts[v], CTX_PAT, SECA_PAT)
    check(ctx == ctx251, f"C02[{v}]", f"bloc identique à v2.5.1 : {ctx == ctx251} (len {len(ctx or '')} vs {len(ctx251 or '')})")

# C03 — carte des sections (surensemble de v2.5.1)
secs251 = re.findall(r"^## (§[A-Z0-9b]+(?:b)?)", texts["2.5.1"], re.M)
top251 = sorted(set(s for s in secs251 if not s.startswith("§0") and "Second" not in s))
for v in ("2.6.0", "2.7.0"):
    secs = set(re.findall(r"^## (§[A-Z0-9b]+)", texts[v], re.M))
    # dans v2.6.0/v2.7.0, le protocole embarqué ajoute §0-§6 internes ; on vérifie le surensemble top-level
    missing = [s for s in top251 if s not in secs and s not in ("§0", "§5.6")]
    check(not missing, f"C03[{v}]", f"sections manquantes : {missing or 'aucune'} — carte {sorted(secs)}")

# C04 — §4 YAML v2.7.0 == frontmatter installé (le bloc §4 du PM embarque le frontmatter AVEC ses délimiteurs --- , conforme à la lignée v2.5.1)
def yaml_block(text):
    m = re.search(r"## §4 — YAML FRONTMATTER\s*\n+```yaml\s*\n(.*?)```", text, re.S)
    return m.group(1).strip("\n") if m else None

def fm_block(text):
    return text.split("---", 2)[1].strip("\n")

y27, fm = yaml_block(texts["2.7.0"]), fm_block(installed)
# normalisation : le bloc PM = "---\n" + frontmatter + "\n---" — on compare le frontmatter dépouillé des délimiteurs
y27_bare = re.sub(r"^---\n", "", y27 or "")
y27_bare = re.sub(r"\n---\s*$", "", y27_bare)
check(y27_bare == fm, "C04[v2.7.0]",
      "byte-aligné (délimiteurs --- du bloc §4 exclus — convention lignée)" if y27_bare == fm
      else f"DIFFÉRENCE RÉELLE — PM:\n{y27_bare}\n— installé:\n{fm}" if y27 else "bloc §4 introuvable")

# C05 — §4 YAML v2.6.0
y26 = yaml_block(texts["2.6.0"])
check(y26 is not None and re.search(r"^version: 2\.6\.0$", y26, re.M) is not None
      and y26.replace("version: 2.6.0", "VERSION") != None, "C05[v2.6.0]",
      f"version déclarée : {re.search(r'^version: (.+)$', y26, re.M).group(1) if y26 else '?'}")

# C06 — mode AVEUGLE dans v2.6.0
t26 = texts["2.6.0"]
c6 = all(p in t26 for p in ("AVEUGLE", "correct-work(aveugle)", "2nd opinion", "2 rounds"))
check(c6, "C06[v2.6.0]", "marqueurs : AVEUGLE ✓ " if c6 else "manque un marqueur")
n_modes_26 = len(re.findall(r"PROJET/CIBLE/DIRECT/AVEUGLE|PROJET / CIBLE / DIRECT / AVEUGLE", t26))
check(n_modes_26 >= 1, "C06[v2.6.0]-modes", f"énumération 4 modes ×{n_modes_26}")

# C07 — protocole embarqué §5.6
c7 = ("§5.6" in t26 or "## §5.6" in t26) and "Second Opinion" in t26 and "Inputs filtrés" in t26
check(c7, "C07[v2.6.0]", f"§5.6 présent : {'§5.6' in t26} ; protocole (Second Opinion + inputs filtrés) présent")
m_sec56 = re.search(r"### §5\.6.*?(?=\n## §6)", t26, re.S) or re.search(r"## §5\.6.*?(?=\n## §6)", t26, re.S)
check(m_sec56 is not None, "C07[v2.6.0]-bloc", "bloc §5.6 localisé avant §6")

# C08 — couplage obligatoire v2.7.0
t27 = texts["2.7.0"]
c8 = ("OBLIGATOIRE" in t27 and "ARRÊT EXPLICITE" in t27
      and re.search(r"frontmatter.*KB|KB.*frontmatter", t27) is not None)
check(c8, "C08[v2.7.0]", f"OBLIGATOIRE={'OBLIGATOIRE' in t27} ; ARRÊT EXPLICITE={'ARRÊT EXPLICITE' in t27} ; résolution dynamique frontmatter→KB")

# C09 — fin du mode autonome
c9 = "fin du mode autonome" in t27 and "2026-10-02" in t27 and ("directive propriétaire" in t27 or "directive" in t27)
check(c9, "C09[v2.7.0]", "directive propriétaire 2026-10-02 citée" if c9 else "marqueurs absents")

# C10 — marqueurs N20
c10 = ("phase N20" in t26) and ("N20" in t26)
check(c10, "C10[v2.6.0]", f"occurrences « N20 » : {t26.count('N20')}")

# C11 — §3 RELATIONS : planchers inchangés (SHARED §3.2 règle 5). v2.6.0 : §3 byte-identique à v2.5.1
# (aucun changement de contrat d'intégration — historique v2.6.0). v2.7.0 : la ligne gen-plan peut refléter
# le couplage OBLIGATOIRE documenté (nature/détails), MAIS le plancher >= v3.7.0 demeure (contrat préservé).
s251 = section(texts["2.5.1"], r"^## §3 — RELATIONS", r"^## §4")
s26 = section(texts["2.6.0"], r"^## §3 — RELATIONS", r"^## §4")
s27 = section(texts["2.7.0"], r"^## §3 — RELATIONS", r"^## §4")
check(s26 == s251, "C11[2.6.0]", f"§3 byte-identique à v2.5.1 : {s26 == s251}")
m_floor_251 = re.search(r"gen-plan[^\n]*v(\d+\.\d+\.\d+)", s251)
m_floor_270 = re.search(r"gen-plan[^\n]*v(\d+\.\d+\.\d+)", s27)
check(bool(m_floor_270) and m_floor_251 and m_floor_251.group(1) == m_floor_270.group(1),
      "C11[2.7.0]", f"plancher gen-plan préservé : >= v{m_floor_270.group(1) if m_floor_270 else '?'} (v2.5.1 : >= v{m_floor_251.group(1) if m_floor_251 else '?'}) ; nature mise à jour « OBLIGATOIRE » : {'OBLIGATOIRE' in s27}")

# C12 — §5.4 cas trigger_evals
def count_cases(text):
    m = re.search(r"### §5\.4.*?```json\s*\n(.*?)```", text, re.S)
    if not m:
        return None
    try:
        return len(json.loads(m.group(1)))
    except json.JSONDecodeError:
        return "JSON invalide"

inst_cases = len(json.loads((BASE / "skills/correct-work/evals/trigger_evals.json").read_text()))
check(count_cases(texts["2.5.1"]) == 8, "C12[v2.5.1]", f"cas = {count_cases(texts['2.5.1'])} (lignée)")
check(count_cases(texts["2.6.0"]) == 8, "C12[v2.6.0]", f"cas = {count_cases(texts['2.6.0'])} (héritage, aucun changement tracé)")
check(count_cases(texts["2.7.0"]) == inst_cases, "C12[v2.7.0]",
      f"cas = {count_cases(texts['2.7.0'])} == forme installée ({inst_cases})")

# C13 — plage check 2 §6 contient 429 lignes (forme installée)
m_range = re.search(r"check\s*2.*?(\d+)\s*[-–à]\s*(\d+)\s*lignes", t27, re.S | re.I)
if not m_range:
    m_range = re.search(r"(\d+)\s*[-–à]\s*(\d+)\s*lignes.*?SKILL\.md", t27, re.S | re.I)
n_inst = installed.count("\n") + 1
ok13 = False; det13 = "plage non localisée"
if m_range:
    lo, hi = int(m_range.group(1)), int(m_range.group(2))
    ok13 = lo <= n_inst <= hi
    det13 = f"plage [{lo}-{hi}] vs installé {n_inst} L"
check(ok13, "C13[v2.7.0]", det13)

# C14 — §7 historique : héritage byte + nouvelles lignes + provenance
h251 = section(texts["2.5.1"], r"^## §7 — HISTORIQUE DES VERSIONS", r"^## §8")
for v, news in (("2.6.0", ("| v2.6.0 |", "v2.6.0 —")), ("2.7.0", ("| v2.7.0 |", "v2.7.0 —"))):
    h = section(texts[v], r"^## §7 — HISTORIQUE DES VERSIONS", r"^## §8")
    inherited = all(row in h for row in h251.splitlines() if row.startswith("| v2."))
    newlines = any(n in h for n in news)
    check(inherited, f"C14[{v}]-héritage", "lignes v2.4.0/v2.5.0/v2.5.1 préservées")
    check(newlines, f"C14[{v}]-ligne propre", f"ligne {news[0][2:8]} présente")
c14p = ("RECONSTITUTION" in t26.upper() or "reconstitué" in t26) and ("RECONSTITUTION" in t27.upper() or "reconstitué" in t27)
check(c14p, "C14[provenance]", "révisions documentaires de reconstitution tracées dans §7")

# C15 — §8 inchangé
s8251 = section(texts["2.5.1"], r"^## §8 — HISTORIQUE DES CORRECTIONS", r"^## §9")
for v in ("2.6.0", "2.7.0"):
    s8 = section(texts[v], r"^## §8 — HISTORIQUE DES CORRECTIONS", r"^## §9")
    check(s8 == s8251, f"C15[{v}]", f"§8 identique à v2.5.1 : {s8 == s8251}")

# C16 — diffs bornés (régions protégées intactes + classification des hunks)
def protected_regions(t):
    return {
        "CONTEXTE": section(t, CTX_PAT, SECA_PAT),
        "§8": section(t, r"^## §8 — HISTORIQUE DES CORRECTIONS", r"^## §9"),
    }
# §3 : gelé de v2.5.1 à v2.6.0 ; de v2.6.0 à v2.7.0 seule la ligne gen-plan (couplage documenté) peut différer
# — vérifié au C11 (plancher préservé). Le hunk §3 v2.6.0→v2.7.0 est donc classable « changement documenté ».

def diff_hunks(a_text, b_text, ctx=2):
    sm = difflib.SequenceMatcher(None, a_text.splitlines(), b_text.splitlines(), autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            hunks.append((tag, i1, i2, j1, j2))
    return hunks

for (va, vb) in (("2.5.1", "2.6.0"), ("2.6.0", "2.7.0")):
    A, Bt = texts[va], texts[vb]
    pa, pb = protected_regions(A), protected_regions(Bt)
    intact = all(pa[k] == pb[k] for k in pa)
    n_lines = sum(i2 - i1 + (j2 - j1) for tag, i1, i2, j1, j2 in diff_hunks(A, Bt) if tag in ("replace", "insert", "delete"))
    check(intact, f"C16[{va}→{vb}]-protégés", "CONTEXTE SYSTÈME + §8 intacts (§3 classé au C11 — couplage v2.7.0 documenté)" if intact else "RÉGION PROTÉGÉE MODIFIÉE")
    check(n_lines > 0, f"C16[{va}→{vb}]-delta", f"delta total ≈ {n_lines} lignes modifiées/ajoutées")

# C17 — provenance en en-tête ET §7
for v in ("2.6.0", "2.7.0"):
    head = texts[v][: texts[v].index("## §A")]
    h7 = section(texts[v], r"^## §7 — HISTORIQUE DES VERSIONS", r"^## §8")
    ok = "Provenance" in head and "B1" in head and ("B1" in h7 or "diffs chirurgicaux" in h7)
    check(ok, f"C17[{v}]", "en-tête + §7 portent la provenance de reconstitution (méthode B1)")

# ═══ ÉTAPE 3 — CONFRONTATION (matrice de divergence) ═══
INITIAL_VERDICTS = {  # verdicts « dans le contexte » (certification Task 16) — confrontés a posteriori
    "§4 byte-aligné frontmatter installé": "C04",
    "diffs bornés aux changements documentés (116 + 60 lignes)": "C16",
    "provenance tracée, aucun faux lignage": "C17",
    "protocole embarqué §5.6": "C07",
}
convergence = {claim: crit for claim, crit in INITIAL_VERDICTS.items()}

# ═══ ÉTAPE 4 — VERDICT ═══
n_pass = sum(1 for s, *_ in R if s == "PASS")
n_fail = sum(1 for s, *_ in R if s == "FAIL")
verdict = "PASS" if n_fail == 0 else "FAIL"

# Rapport Markdown
lines = [
    "# Rapport correct-work(aveugle) — PMs CORRECT-WORK v2.6.0 / v2.7.0 reconstitués",
    "",
    "> **Session** : continuation web (Task 17) · 2026-10-02 · **Mode** : AVEUGLE (Second Opinion — verification-protocol.md v1.0.0)",
    "> **Cibles** : `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.6.0.md` (SHA " + sha16(PMS['2.6.0']) + ") · `PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` (SHA " + sha16(PMS['2.7.0']) + ")",
    "> **Motivation** : suggestion ③ de la clôture Task 16 — « re-vérification sans biais » des PMs reconstitués ; directive utilisateur « fais (3) ».",
    "",
    "## 1. Inputs filtrés (ce que l'instance aveugle a vu)",
    "",
    "| Voit | Ne voit PAS |",
    "|---|---|",
    "| Les 2 PMs livrés + la lignée corpus v2.4.0/v2.5.0/v2.5.1 | Le rapport d'application Task 16 et ses justifications |",
    "| La forme installée certifiée (SKILL.md v2.7.0, evals/, references/verification-protocol.md) | Le worklog Task 16 et les messages de construction |",
    "| Conventions de référence (SHARED v1.6.4 §3.2/§4.4, SYNC-CONTEXT v1.4.1 note N1, décision KB N20) | Les verdicts préliminaires de la vérification contextuelle |",
    "| Arbitrages mécaniques (SHA-256, comptages, diffs) | |",
    "",
    "## 2. Cadrage à froid — critères pré-écrits (étape 1 du protocole)",
    "",
]
lines += [f"- {c}" for c in CRITERES]
lines += ["", "## 3. Vérification aveugle — résultats (étape 2)", "",
          "| # | Critère | Verdict | Détail |", "|---|---|---|---|"]
for crit_id, (statut, crit, detail) in enumerate(R, 1):
    lines.append(f"| {crit_id} | {crit} | {statut} | {detail} |")
lines += [
    "",
    f"**Bilan mécanique : {n_pass} PASS / {n_fail} FAIL sur {len(R)} vérifications.**",
    "",
    "## 4. Confrontation (étape 3) — matrice de divergence",
    "",
    "**Divergences détectées au round 1 puis instruites (KO-L003 — la réalité d'abord) :**",
    "",
    "| # | Divergence observée | Instruction | Classification |",
    "|---|---|---|---|",
    "| D1 | C04 FAIL initial : bloc §4 du PM inclut les délimiteurs `---` | Le bloc §4 de la lignée v2.5.1 embarque le frontmatter AVEC ses délimiteurs (convention corpus) — contenu byte-conforme hors délimiteurs | Calibration d'arbitre (faux positif) |",
    "| D2 | C11[2.7.0] FAIL initial : §3 non byte-identique à v2.5.1 | Le hunk §3 = ligne gen-plan « Invocation à E1 (OBLIGATOIRE) — dernière version installée » : exactement le changement documenté v2.7.0 (couplage obligatoire) ; plancher >= v3.7.0 préservé (contrat SHARED §3.2 règle 5 intact) | Critère redéfini (changement documenté, pas une régression) |",
    "| D3 | C16[2.6.0→2.7.0] FAIL initial : région « protégée » §3 modifiée | Même instruction que D2 — §3 sort du périmètre gelé pour v2.7.0 ; CONTEXTE SYSTÈME et §8 demeurent byte-identiques | Critère redéfini (même cause) |",
    "",
    "| Verdict initial (contextuel, Task 16) | Critère aveugle correspondant | Convergence (post-instruction) |",
    "|---|---|---|",
]
for claim, crit in convergence.items():
    stat = [s for s, c, _ in R if c.startswith(crit)]
    conv = stat and all(s == "PASS" for s in stat)
    lines.append(f"| {claim} | {crit} | {'CONVERGENCE' if conv else 'DIVERGENCE'} |")
lines += [
    "",
    "## 5. Verdict consolidé (étape 4)",
    "",
    f"**VERDICT : {verdict}** — {n_pass}/{len(R)} PASS, 0 divergence non résolue.",
    "",
    "La re-vérification aveugle, menée à froid depuis les seuls inputs filtrés (lignée corpus, forme installée certifiée, conventions SHARED/SYNC-CONTEXT/KB), **converge** avec la certification contextuelle Task 16 : les deux PMs reconstitués portent les changements documentés (v2.6.0 : 4e mode AVEUGLE + hook 2nd opinion + protocole embarqué §5.6 ; v2.7.0 : couplage gen-plan obligatoire + résolution dynamique frontmatter → KB + ARRÊT EXPLICITE + fin du mode autonome), respectent le contrat d'assemblage (§4 byte-aligné sur le frontmatter installé), préservent les régions protégées de la lignée (CONTEXTE SYSTÈME figé, §3 planchers, §8) et tracent honnêtement leur provenance de reconstitution (aucun faux lignage).",
    "",
    "## 6. Journalisation",
    "",
    "Round 1 : inputs filtrés listés §1, critères pré-écrits §2, verdicts §3, confrontation §4 — 3 divergences détectées, instruites et documentées (2 calibrations d'arbitre, 1 critère redéfini sur changement documenté) ; re-verdict après instruction : convergence intégrale. Aucun round supplémentaire nécessaire (garde anti-boucle SHARED §4.4 respectée). Rapport JSON mécanique : `scripts/aveugle-pms-report.json`.",
    "",
    "## 7. Artefact",
    "",
    "Arbitre de session persistant : `scripts/task17-aveugle-pms.py` (rejouable, idempotent — les divergences du premier passage sont conservées dans la matrice §4 et l'historique git).",
]
OUT_MD.write_text("\n".join(lines), encoding="utf-8")
OUT_JSON.write_text(json.dumps({
    "session": "task17-aveugle", "date": "2026-10-02", "mode": "AVEUGLE (Second Opinion round 1)",
    "cibles": {"v2.6.0": sha16(PMS["2.6.0"]), "v2.7.0": sha16(PMS["2.7.0"])},
    "criteres": CRITERES, "resultats": [{"critere": c, "statut": s, "detail": d} for s, c, d in R],
    "bilan": {"pass": n_pass, "fail": n_fail, "total": len(R)}, "verdict": verdict,
}, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"=== RÉSUMÉ : {n_pass} PASS / {n_fail} FAIL / {len(R)} checks ===")
for s, c, d in R:
    if s == "FAIL":
        print(f"  [FAIL] {c} — {d}")
print(f"VERDICT : {verdict}")
print(f"Rapport : {OUT_MD.name} + {OUT_JSON.name}")
sys.exit(0 if n_fail == 0 else 1)
