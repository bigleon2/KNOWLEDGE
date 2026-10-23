#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: Task 24 (2026-10-23, session web-fdf5963c) — cascade KO-L004 de la
# révision des §1.9bis des 16 éléments : KB (collage hérité corrigé + 13 en-têtes
# + 13 bullets Task 24 + journal), ECO_SKILLS ×13, PM REFACTOR-GUARD v1.8.1
# (génération mécanique, delta verrouillé §1.9bis révisée), archivage R4 de
# v1.8.0 (git mv byte-identité, index 27 PMs, réparation ligne v1.8.0 omise en
# Task 22), README corpus v2.1.10, SYNC-CONTEXT v1.5.2, ULTRA régénéré,
# propagate SHARED v1.7.10, rescellement archive ×2. Échec si 0 match ;
# idempotent ×2 (marqueurs par étape).
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from task24_contenu_19bis import REVISED  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SK = REPO / "skills"
CORPUS = SK / "@mon-ecosysteme"
KB = SK / "KNOWLEDGE.md"
ARB = REPO / "scripts" / "check-ecosysteme-integrity.py"
DEPOT = [s for s in REVISED if s != "agent-creator" and s not in
         {"cahier-des-charges", "inter-scripts", "agent-prompt-engineering"}]
B24 = "- **Task 24 (2026-10-23, session web-fdf5963c"


def sub1(t, old, new, label):
    n = t.count(old)
    assert n == 1, f"{label}: {n} occurrences (attendu 1)"
    return t.replace(old, new, 1)


def run(cmd, label):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    assert r.returncode == 0, f"{label}: rc={r.returncode}\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}"
    print(f"   [ok] {label}")
    return r.stdout


# ── 1. KB ────────────────────────────────────────────────────────────────
t = KB.read_text(encoding="utf-8")
glued_variants = ((")- **Task 22 (2026-10-23", ")\n- **Task 22 (2026-10-23"),
                  (")**- **Task 22 (2026-10-23", ")**\n- **Task 22 (2026-10-23"))
glued = 0
for pat_old, pat_new in glued_variants:
    n = t.count(pat_old)
    if n:
        glued += n
        t = t.replace(pat_old, pat_new)
if glued:
    KB.write_text(t, encoding="utf-8")
    print(f"KB : {glued} bullets Task 22 recollés remis sur leur propre ligne (défaut hérité corrigé)")
else:
    print("KB : collage déjà corrigé (idempotence)")
t = KB.read_text(encoding="utf-8")
residuels = [m.start() for m in re.finditer(r"\*\*Task 22 \(2026-10-23", t)
             if t[:m.start()].rsplit("\n", 1)[-1].rstrip() not in ("", "-")]
assert not residuels, f"KB: {len(residuels)} collage(s) résiduel(s) — motif non couvert"

t = KB.read_text(encoding="utf-8")
if t.count(B24) < 13:
    for skill in DEPOT + ["agent-creator"]:
        old, new = REVISED[skill][0], REVISED[skill][1]
        pat_old = re.compile(r"^(## %s v)%s(\s*)$" % (re.escape(skill), re.escape(old)), re.M)
        pat_new = re.compile(r"^## %s v%s\s*$" % (re.escape(skill), re.escape(new)), re.M)
        if pat_new.search(t):
            continue  # déjà bumpé (idempotence)
        ms = pat_old.findall(t)
        assert len(ms) == 1, f"KB heading {skill}: {len(ms)} (attendu 1)"
        t = pat_old.sub(r"\g<1>%s\g<2>" % new, t, count=1)
    KB.write_text(t, encoding="utf-8")
    print("KB : en-têtes bumpés")
else:
    print("KB : en-têtes déjà bumpés (idempotence)")

t = KB.read_text(encoding="utf-8")
if t.count(B24) < 13:
    for skill in DEPOT + ["agent-creator"]:
        new = REVISED[skill][1]
        creation = skill == "agent-creator"
        ent = re.search(r"^## %s v%s\s*$(.*?)(?=^## |\Z)" % (re.escape(skill), re.escape(new)),
                        t, re.M | re.S)
        assert ent, f"KB {skill}: entrée v{new} introuvable"
        bloc = ent.group(0)
        if "Task 24 (2026-10-23" in bloc:
            continue
        pat = re.compile(r"^- \*\*Task 22 \(2026-10-23.*$", re.M)
        ms = pat.findall(bloc)
        assert len(ms) == 1, f"KB {skill}: bullet Task 22 x{len(ms)} (attendu 1)"
        if creation:
            apport = ("§1.9bis CRÉÉE pour le 16e élément — apports de veille de la réécriture "
                      "v2.2.0 alignés au format commun des 15 autres (fabrique ≠ runtime, champ "
                      "capacites Agent Card A2A, progressive disclosure)")
            bump = f"bump v{new} MINOR"
        else:
            apport = ("révision de la §1.9bis — restructuration en bullets actionnables (chaque "
                      "apport porte son application locale explicite), bullet Sources normalisé, "
                      "note de révision ; contenu factuel Task 22 inchangé (garde anti-perte "
                      "lead-ins/sources)")
            bump = f"bump v{new} PATCH"
        bullet = (f"- **Task 24 (2026-10-23, session web-fdf5963c — directive propriétaire "
                  f"« révisez les §1.9bis des 16 éléments »)** : {apport} — {bump} "
                  f"(recalibrage KO-L004 : ECO_SKILLS + KB).\n")
        nouveau_bloc = bloc.replace(ms[0], ms[0].rstrip("\n") + "\n" + bullet.rstrip("\n"), 1)
        t = t[:ent.start()] + nouveau_bloc + t[ent.end():]
    KB.write_text(t, encoding="utf-8")
    print(f"KB : {t.count(B24)} bullets Task 24 insérés (attendu 13)")
else:
    print("KB : bullets Task 24 déjà présents (idempotence)")

t = KB.read_text(encoding="utf-8")
if "Task 24 — directive gen-plan(step) : révision des §1.9bis" not in t:
    ancre = "- **Task 22 — directive gen-plan(step) : re-mesure QUOTA"
    idx = t.find(ancre)
    assert idx > 0, "KB: ancre journal Task 22 introuvable"
    entry = (
        "- **Task 24 — directive gen-plan(step) : révision des §1.9bis des 16 éléments + "
        "intégration amont + publication GO** : directive propriétaire (session web-fdf5963c, "
        "2026-10-23 ; GO + PAT éphémère fournie — règle d'or n°2 levée). (1) **Intégration amont** : "
        "couches 18/20/22 rebasées sur origin/main (11 commits session photos web-38713acd — skills "
        "iphone17/18/19, PMs @photos, KB 33→36, worklog compacté) ; résolutions union documentées "
        "(task24-resolve-conflicts.py — KB, README @historique, worklog, manifeste) ; "
        "resynchronisation §0 SHARED v1.7.9 idempotente (3 skills + 24 scripts amont) ; certification "
        "baseline post-merge 6/6 (verify-cross 111/111 ×2, integrity 78/78, tool-routing 7/7 après "
        "citation du routage au plan §7). (2) **Révision §1.9bis ×16** : 15 sections restructurées en "
        "bullets actionnables (apport → application locale explicite, bullet Sources normalisé, note "
        "de révision — garde anti-perte mécanique lead-ins/sources) + §1.9bis CRÉÉE pour agent-creator "
        "(16e élément) ; bumps ×16 (15 PATCH + agent-creator v2.3.0 MINOR). (3) **Défaut de forme "
        "hérité corrigé** : 11 bullets Task 22 recollés à leur ligne précédente (add_kb_calibration "
        "Task 22) remis sur leur propre ligne. (4) **Cascade KO-L004** : ECO_SKILLS 13 bumps, KB 13 "
        "en-têtes + 13 bullets Task 24 + journal, PM REFACTOR-GUARD v1.8.1 généré mécaniquement (delta "
        "verrouillé §1.9bis révisée), v1.8.0 archivé @historique (git mv R4, SHA scellé, index 27 PMs, "
        "réparation ligne v1.8.0 omise en Task 22), SHARED v1.7.10 / PM-INSTALL v1.8.2 (recalibrage "
        "mécanique), SYNC-CONTEXT v1.5.2, README corpus v2.1.10, ULTRA régénéré, propagate idempotent, "
        "archive rescellée ×2.\n")
    t = t[:idx] + entry + t[idx:]
    KB.write_text(t, encoding="utf-8")
    print("KB : entrée journal Task 24 insérée")
else:
    print("KB : journal Task 24 déjà présent (idempotence)")

# ── 2. ECO_SKILLS (arbitre) ──────────────────────────────────────────────
a = ARB.read_text(encoding="utf-8")
for skill in DEPOT + ["agent-creator"]:
    old, new = REVISED[skill][0], REVISED[skill][1]
    if re.search(r'"%s":\s*"%s"' % (re.escape(skill), re.escape(new)), a):
        continue  # déjà bumpé (idempotence)
    pat = re.compile(r'("%s":\s*)"%s"' % (re.escape(skill), re.escape(old)))
    ms = pat.findall(a)
    assert len(ms) == 1, f"ECO_SKILLS {skill}: {len(ms)} (attendu 1)"
    a = pat.sub(r'\g<1>"%s"' % new, a, count=1)
ARB.write_text(a, encoding="utf-8")
print("ECO_SKILLS : 13 bumps KO-L004")

# ── 3. Delta verrouillé + génération PM v1.8.1 ───────────────────────────
pm180 = CORPUS / "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md"
pm181 = CORPUS / "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md"
TITRE = "### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)"
if not pm181.exists():
    assert pm180.exists(), "PM v1.8.0 absent du corpus"
    s180 = pm180.read_text(encoding="utf-8")
    i = s180.find(TITRE); j = s180.find("\n## §2", i)
    assert i > 0 and j > i, "PM v1.8.0: bloc §1.9bis introuvable"
    old_para = s180[i + len(TITRE):j].strip()
    sk = (SK / "refactor-guard" / "SKILL.md").read_text(encoding="utf-8")
    i2 = sk.find(TITRE); j2 = sk.find("\n## §2", i2)
    assert i2 > 0 and j2 > i2, "SKILL.md refactor-guard: bloc §1.9bis introuvable"
    new_block = sk[i2 + len(TITRE):j2].strip()
    delta = {
        "history": ("Task 24 (2026-10-23, session web-fdf5963c — directive propriétaire « révisez "
                    "les §1.9bis des 16 éléments ») : §1.9bis révisée — restructuration en bullets "
                    "actionnables (chaque apport porte son application locale explicite : golden "
                    "master AVANT -> baseline scellée avant cascade ; mutation testing léger -> "
                    "gardes anti-faux-succès + idempotence ×2 ; rollback armé -> rebase publication "
                    "réversible + 0 force-push) + bullet Sources normalisé + note de révision ; "
                    "contenu factuel Task 22 inchangé (garde anti-perte lead-ins/sources)"),
        "subs": [{"old": old_para, "new": new_block, "count": 1}],
    }
    dpath = REPO / "scripts" / "task24-delta-refactor-guard-v181.json"
    dpath.write_text(json.dumps(delta, ensure_ascii=False, indent=2), encoding="utf-8")
    out = run(["python3", "scripts/generer-pm-skill.py", "--generate", "refactor-guard",
               "--delta", "scripts/task24-delta-refactor-guard-v181.json"], "generer-pm v1.8.1")
    print("   " + out.strip().splitlines()[-1] if out.strip() else "")
else:
    print("PM v1.8.1 déjà présent (idempotence)")
assert pm181.exists(), "PM v1.8.1 absent après génération"
shared = (CORPUS / "PROMPT-MAITRE-SHARED.md").read_text(encoding="utf-8")
assert "1.7.10" in shared, "SHARED non bumpé à 1.7.10"
pi = sorted(CORPUS.glob("PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"))[-1].read_text(encoding="utf-8")
assert "1.8.2" in pi, "PM-INSTALL non bumpé à 1.8.2"
print("Recalibrage croisé : SHARED v1.7.10 + PM-INSTALL v1.8.2 (mécanique generer-pm)")

# ── 4. Archivage R4 de v1.8.0 + README @historique + historiques-par-skill ──
dest = SK / "@historique" / "prompts-maitres" / "refactor-guard" / "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md"
if pm180.exists():
    run(["git", "mv", "skills/@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md",
         "skills/@historique/prompts-maitres/refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md"],
        "git mv v1.8.0 -> @historique")
assert dest.exists() and not pm180.exists(), "archivage v1.8.0 incomplet"
sha180 = hashlib.sha256(dest.read_bytes()).hexdigest()
print(f"SHA-256 v1.8.0 archivé : {sha180[:16]}…")

rh = SK / "@historique" / "README.md"
t = rh.read_text(encoding="utf-8")
if "refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md" not in t:
    t = sub1(t, "| REFACTOR-GUARD | refactor-guard — garde-fous de refactoring (H01-H15, échelle rollout) | 3 (v1.7.0 → v1.8.0) | 2 (v1.7.0, v1.7.1) | v1.8.0 |",
             "| REFACTOR-GUARD | refactor-guard — garde-fous de refactoring (H01-H15, échelle rollout) | 4 (v1.7.0 → v1.8.1) | 3 (v1.7.0, v1.7.1, v1.8.0) | v1.8.1 |",
             "README @historique famille")
    t = sub1(t, "## 5. Index des fichiers sources archivés (26 PMs — sceau SHA-256)",
             "## 5. Index des fichiers sources archivés (27 PMs — sceau SHA-256)",
             "README @historique heading")
    t = sub1(t, "| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md | 8fceb8c1ac1dbb2848b87a8d154d9970a5b6418551898065caee56f9392de33e |",
             "| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md | 8fceb8c1ac1dbb2848b87a8d154d9970a5b6418551898065caee56f9392de33e |\n"
             "| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md | " + sha180 + " |",
             "README @historique index row")
    t = sub1(t, "Complément cascade Task 22 (2026-10-23, session web-fdf5963c — directive « disciplines/techniques »",
             "Complément cascade Task 24 (2026-10-23, session web-fdf5963c — directive « révisez les §1.9bis des 16 éléments ») : `PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md` archivé par `git mv` byte-identité (R4 — SHA-256 scellé ci-dessous ; fichier suivi au dépôt depuis le commit des couches 18/20/22). Complément cascade Task 22 (2026-10-23, session web-fdf5963c — directive « disciplines/techniques »",
             "README @historique provenance")
    rh.write_text(t, encoding="utf-8")
    print("README @historique : famille recalibrée + index 27 PMs + provenance Task 24")
else:
    print("README @historique : déjà à jour (idempotence)")

hp = SK / "@historique" / "historiques-par-skill" / "refactor-guard.md"
t = hp.read_text(encoding="utf-8")
if "| v1.8.1 |" not in t:
    ancre = re.search(r"^\| v1\.7\.1 \|.*$", t, re.M)
    assert ancre, "historiques-par-skill: ligne v1.7.1 introuvable"
    rows = (
        "| v1.8.0 | 2026-10-23 | Task 22 (session web-fdf5963c — directive « disciplines/techniques », veille 2025-2026) : §1.9bis Apports de veille — golden master AVANT (renforcement R5) + mutation testing léger en sandbox (anti faux-verts) + rollback automatique ARMÉ en canary (N5) ; PM v1.8.0 généré mécaniquement KO-L004 (delta verrouillé) ; recalibrage croisé SHARED v1.7.9 / PM-INSTALL v1.8.1 ; v1.7.1 archivé @historique (SHA scellé) | Réparation Task 24 : ligne omise en Task 22 — historique rétabli |\n"
        "| v1.8.1 | 2026-10-23 | Task 24 (session web-fdf5963c — directive « révisez les §1.9bis des 16 éléments ») : §1.9bis révisée — restructuration en bullets actionnables (apport → application locale explicite) + bullet Sources normalisé + note de révision ; contenu factuel Task 22 inchangé (garde anti-perte lead-ins/sources) ; PM v1.8.1 généré mécaniquement KO-L004 (delta verrouillé) ; recalibrage croisé SHARED v1.7.10 / PM-INSTALL v1.8.2 ; v1.8.0 archivé @historique (git mv byte-identité R4, SHA scellé) | **VERSION VIVANTE (corpus)** |\n")
    t = t[:ancre.end()] + "\n" + rows.rstrip("\n") + t[ancre.end():]
    hp.write_text(t, encoding="utf-8")
    print("historiques-par-skill : lignes v1.8.0 (réparation) + v1.8.1 insérées")
else:
    print("historiques-par-skill : déjà à jour (idempotence)")

# ── 5. README corpus + SYNC-CONTEXT ─────────────────────────────────────
rc = CORPUS / "README.md"
t = rc.read_text(encoding="utf-8")
if "Révision v2.1.10" not in t:
    t = sub1(t, "> **Révision v2.1.9 (2026-10-23, Task 22",
             "> **Révision v2.1.10 (2026-10-23, Task 24 — session web-fdf5963c, directive propriétaire « révisez les §1.9bis des 16 éléments », publication GO)** : révision §1.9bis ×16 (15 restructurées en bullets actionnables — apport → application locale explicite — + agent-creator v2.3.0 §1.9bis créée) ; PM REFACTOR-GUARD v1.8.1 généré mécaniquement KO-L004, v1.8.0 archivé @historique/prompts-maitres/refactor-guard/ (git mv R4, SHA scellé, index 27 PMs) ; SHARED v1.7.10 / PM-INSTALL v1.8.2 (recalibrage mécanique) ; intégration amont origin/main (session photos) rebasée avant cascade.\n> **Révision v2.1.9 (2026-10-23, Task 22", "README corpus rev")
    t = sub1(t, "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md  ← 4e famille (décision D009)",
             "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md  ← 4e famille (décision D009)",
             "README corpus arbo")
    rc.write_text(t, encoding="utf-8")
    print("README corpus : v2.1.10 + arbo v1.8.1")
else:
    print("README corpus : déjà à jour (idempotence)")

sc = CORPUS / "SYNC-CONTEXT.md"
t = sc.read_text(encoding="utf-8")
if "Révision v1.5.2" not in t:
    t = sub1(t, "> **Révision v1.5.1 (2026-10-23, cascade Task 22",
             "> **Révision v1.5.2 (2026-10-23, cascade Task 24 — session web-fdf5963c, KO-L004)** : état du corpus recalibré — révision §1.9bis ×16 (15 restructurées + agent-creator v2.3.0 §1.9bis créée ; garde anti-perte mécanique), PM REFACTOR-GUARD v1.8.1 généré mécaniquement (delta verrouillé), v1.8.0 archivé @historique (git mv R4, index 27 PMs, réparation ligne v1.8.0 omise en Task 22) ; SHARED v1.7.10 / PM-INSTALL v1.8.2 (recalibrage mécanique) ; intégration amont origin/main (session photos web-38713acd) rebasée + resynchronisation §0 v1.7.9 idempotente avant cascade, puis propagate v1.7.10 ; 11 bullets KB Task 22 recollés remis sur leur propre ligne (défaut de forme hérité corrigé) ; ULTRA régénéré ; archive rescellée round-trip ×2.\n> **Révision v1.5.1 (2026-10-23, cascade Task 22", "SYNC rev")
    sc.write_text(t, encoding="utf-8")
    print("SYNC-CONTEXT : v1.5.2")
else:
    print("SYNC-CONTEXT : déjà à jour (idempotence)")

# ── 6. ULTRA ─────────────────────────────────────────────────────────────
run(["python3", "scripts/gen-ultra-maitre.py"], "ULTRA régénéré")

# ── 7. propagate (constantes → v1.7.10 puis exécution) ──────────────────
pc = REPO / "scripts" / "propagate-context.py"
t = pc.read_text(encoding="utf-8")
n = t.count("(SHARED v1.7.9)")
if n:
    assert n == 4, f"propagate: {n} occurrences v1.7.9 (attendu 4)"
    pc.write_text(t.replace("(SHARED v1.7.9)", "(SHARED v1.7.10)"), encoding="utf-8")
    print("propagate-context.py : constantes recalibrées v1.7.9 → v1.7.10")
out = run(["python3", "scripts/propagate-context.py"], "propagate §0 v1.7.10")
last = out.strip().splitlines()[-1] if out.strip() else ""
print("   " + last)

# ── 8. Rescellement archive ×2 ───────────────────────────────────────────
run(["python3", "scripts/task21-f2-rebuild-archive.py"], "rescellement 1/2")
run(["python3", "scripts/task21-f2-rebuild-archive.py"], "rescellement 2/2 (idempotence)")

# ── 9. Vérifications finales ─────────────────────────────────────────────
kb = KB.read_text(encoding="utf-8")
assert kb.count(B24) == 13, f"KB: {kb.count(B24)} bullets Task 24 (attendu 13)"
assert ")- **Task 22 (2026-10-23" not in kb, "KB: collage résiduel"
for skill in DEPOT + ["agent-creator"]:
    assert re.search(r"^## %s v%s\s*$" % (re.escape(skill), REVISED[skill][1]), kb, re.M), \
        f"KB: en-tête {skill} v{REVISED[skill][1]} absent"
arb = ARB.read_text(encoding="utf-8")
for skill in DEPOT + ["agent-creator"]:
    assert f'"{skill}": "{REVISED[skill][1]}"' in arb, f"ECO_SKILLS: {skill} non bumpé"
corpus_files = sorted(p.name for p in CORPUS.glob("*.md"))
assert "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md" in corpus_files
assert "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md" not in corpus_files
print("Vérifications finales : KB 13/13, ECO_SKILLS 13/13, corpus v1.8.1 (v1.8.0 archivée) — PASS")
print("Cascade KO-L004 Task 24 : terminée.")
return_code = 0
sys.exit(return_code)
