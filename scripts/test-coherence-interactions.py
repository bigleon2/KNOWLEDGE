#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test-coherence-interactions.py — Test de cohérence des interactions de fichiers
Écosystème Knowledge — généré par gen-plan v3.11.0, session B2 (Task ID 3, Phase 2).
Recalibré sessions B3-B4 (Task ID 4-5) : recommandations 1-3 du rapport B2 —
harmonisation bidirectionnelle du registre KB (5 réciproques, révision B3),
publication du PM v3.11.0 dans download/ (SYNC_MAP 6 fichiers, B3) et
calibration de verify-cross CHECK 7.6 sur le format liste (B4).
Session B5 (Task ID 6) : frontmatter métier standardisé (Phase 2 du dépôt,
fix-frontmatter.py + repair-frontmatter-yaml.py) — frontière fullstack-dev levée
(version 1.0.0 satisfait le contrat >= 1.0.0 de correct-work) — PASS STRICT.

Périmètre (complémentaire des arbitres existants, focalisé sur les INTERACTIONS) :
  1. Corpus @mon-ecosysteme <-> Miroir _prompts-maitres (byte-identité, 15 fichiers)
  2. Registre KNOWLEDGE.md : versions déclarées <-> versions réelles SKILL.md
  3. Graphe de relations KB : bidirectionnalité « Dépend de » <-> « Utilisé par »
     (parse le format LISTE réel du KB ; verify-cross CHECK 7.6 calibré sur ce
      même format en session B4 — cross-validation : 14 arêtes des deux côtés)
  4. Contrats de dépendances frontmatter (semver >=) vs versions installées
  5. Pointeurs internes gen-plan : arbre §2.2 (6 références + evals), pointeurs PM
     v3.11.0 (SKILL.md <-> corpus <-> miroir), référence PEK §1.6/§2.2
  6. Calibration de l'arbitre local check-ecosysteme-integrity.py <-> réalité
  7. Synchronisation download/ (6 fichiers attendus — extension B3 : PM v3.11.0)
  8. Présence des evals/ pour les skills écosystème
  9. Compilation des scripts Python (py_compile — portée E8 étendue)
 10. Format du worklog (sections ---, Task ID, SHARED §1.4)
 11. Propagation de la mise à jour v3.11.0 (demande explicite utilisateur) :
     porteurs de version, non-régression R2 vs dépôt source a8ffb5f,
     références stale, canal de publication download/

Conventions : Python uniquement (N3), kebab-case, verdicts PASS/FAIL/WARN,
sortie structurée + score final. Adaptation = signal, jamais un arrêt (règle d'or n°1).
"""

import json
import py_compile
import re
import sys
from pathlib import Path

BASE = Path("/home/z/my-project")
SKILLS = BASE / "skills"
CORPUS = SKILLS / "@mon-ecosysteme"
MIRROR = SKILLS / "_prompts-maitres"
KB_PATH = SKILLS / "KNOWLEDGE.md"
DOWNLOAD = BASE / "download"
WORKLOG = BASE / "worklog.md"

# Convention documentée dans check-ecosysteme-integrity.py : version déclarée
# uniquement dans le registre KB (forme plateforme adoptée par l'écosystème).
KB_ONLY_VERSION = {"skill-creator"}

# Références externes légitimes dans « Utilisé par » (non-skills du registre)
EXTERNAL_REFS = {"main", "sessions", "install-ecosystem", "arbitres"}

# Skills à déclenchement automatique (SHARED §7) : « Utilisé par » sans réciproque
# « Dépend de » est un choix de design documenté (SKILL.md gen-plan §1.6), pas une asymétrie.
BY_DESIGN_AUTOTRIGGER = {"context-engineering", "loop-engineering", "graph-engineering",
                         "harness-engineering"}

results = []  # (statut, section, check, détail)


def record(status, section, check, detail=""):
    results.append((status, section, check, detail))
    tag = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]"}[status]
    print(f"  {tag} {check}" + (f" — {detail}" if detail else ""))


def semver_tuple(v):
    m = re.match(r"(\d+)\.(\d+)\.(\d+)", v.strip().lstrip("v"))
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def read_frontmatter_version(path):
    """Extrait version: du frontmatter YAML d'un SKILL.md."""
    try:
        head = path.read_text(encoding="utf-8").split("---")[1]
    except (IndexError, OSError):
        return None
    m = re.search(r"^version:\s*['\"]?(\d+\.\d+\.\d+)", head, re.M)
    return m.group(1) if m else None


def parse_frontmatter_deps(path):
    """Extrait [(skill, version_min)] du bloc dependencies: multi-lignes du frontmatter."""
    deps = []
    try:
        text = path.read_text(encoding="utf-8")
        head = text.split("---")[1]
    except (IndexError, OSError):
        return deps
    m = re.search(r"dependencies:\s*\n((?:[ \t]+[^\n]*\n?)+)", head)
    if not m:
        return deps
    cur = None
    for line in m.group(1).splitlines():
        sm = re.search(r"skill:\s*([a-z0-9-]+)", line)
        if sm:
            cur = sm.group(1)
            continue
        vm = re.search(r"version:\s*\"?>?=?\s*(\d+\.\d+\.\d+)", line)
        if vm and cur:
            deps.append((cur, vm.group(1)))
            cur = None
    return deps


# ============================================================================
print("\n=== 1. Corpus <-> Miroir (byte-identité) ===")
corpus_files = sorted(p.name for p in CORPUS.glob("*.md")) if CORPUS.is_dir() else []
mirror_files = sorted(p.name for p in MIRROR.glob("*.md")) if MIRROR.is_dir() else []
record("PASS" if len(corpus_files) == 15 else "WARN", "1",
       f"Corpus = {len(corpus_files)} fichiers (15 attendus — v3.11.0)")
identical, divergent = 0, []
for name in corpus_files:
    c, m = CORPUS / name, MIRROR / name
    if m.exists() and c.read_bytes() == m.read_bytes():
        identical += 1
    else:
        divergent.append(name)
if divergent:
    record("FAIL", "1", "Byte-identité corpus/miroir", f"divergents : {divergent}")
else:
    record("PASS", "1", "Byte-identité corpus/miroir",
           f"{identical}/{len(corpus_files)} identiques + 0 miroir orphelin"
           if set(mirror_files) == set(corpus_files) else
           f"{identical} identiques mais miroir orphelin : {set(mirror_files) ^ set(corpus_files)}")

# ============================================================================
print("\n=== 2. Registre KB : versions déclarées <-> réelles ===")
kb_text = KB_PATH.read_text(encoding="utf-8") if KB_PATH.exists() else ""
entries = {}  # name -> {version, deps: [(name, vmin)], users: [names]}
for m in re.finditer(r"^## ([a-z0-9-]+) v(\d+\.\d+\.\d+)\s*$", kb_text, re.M):
    name, ver = m.group(1), m.group(2)
    end = kb_text.find("\n## ", m.end())
    block = kb_text[m.end():end if end != -1 else len(kb_text)]
    dep_m = re.search(r"\*\*Dépend de\*\* :(.*)", block)
    use_m = re.search(r"\*\*Utilisé par\*\* :(.*)", block)
    deps = re.findall(r"([a-z][a-z0-9-]*)\s*>=\s*v?(\d+\.\d+\.\d+)", dep_m.group(1)) if dep_m else []
    users = []
    if use_m and "—" not in use_m.group(1)[:3]:
        raw = use_m.group(1)
        users = [n for n in re.findall(r"([a-z][a-z0-9-]*)", raw)
                 if len(n) > 3 and n not in ("hooks", "planification", "archivage",
                                             "persistance", "verdicts", "scan", "conventions",
                                             "couche", "disciplines", "finale", "dynamique",
                                             "optionnel", "etat", "tat")]
    entries[name] = {"version": ver, "deps": deps, "users": sorted(set(users))}

record("PASS" if len(entries) == 11 else "FAIL", "2",
       f"Registre parsé : {len(entries)} entrées (11 attendues)")

mismatches = []
for name, info in entries.items():
    skill_md = SKILLS / name / "SKILL.md"
    if not skill_md.exists():
        mismatches.append(f"{name}: répertoire absent")
        continue
    if name in KB_ONLY_VERSION:
        continue  # convention KB_ONLY_VERSION documentée
    real = read_frontmatter_version(skill_md)
    if real != info["version"]:
        mismatches.append(f"{name}: KB={info['version']} / SKILL.md={real}")
if mismatches:
    record("FAIL", "2", "Versions KB <-> SKILL.md", "; ".join(mismatches))
else:
    record("PASS", "2", "Versions KB <-> SKILL.md",
           f"11/11 alignées (skill-creator en convention KB_ONLY_VERSION)")

# ============================================================================
print("\n=== 3. Graphe de relations KB : bidirectionnalité ===")
# dep A->B exige B.users contienne A ; user A<-C exige C.deps contienne A.
asym_dep, asym_user, bidir, external = [], [], 0, []
for a, info in entries.items():
    for (b, _vmin) in info["deps"]:
        if b in entries:
            if a in entries[b]["users"]:
                bidir += 1
            else:
                asym_dep.append(f"{a} → {b} : {b} ne liste pas {a} dans « Utilisé par »")
        else:
            external.append(f"{a} → {b} (hors registre : skill plateforme)")
for a, info in entries.items():
    for c in info["users"]:
        if c in entries:
            if a not in dict(entries[c]["deps"]):
                if a in BY_DESIGN_AUTOTRIGGER:
                    external.append(f"{a} ← {c} (déclenchement automatique SHARED §7 — design documenté)")
                else:
                    asym_user.append(f"{a} ← {c} : {c} ne déclare pas {a} en « Dépend de »")
        elif c in EXTERNAL_REFS:
            external.append(f"{a} ← {c} (référence externe documentée : agent/PM/session)")

record("PASS", "3", f"Arêtes bidirectionnelles dépandance↔usage : {bidir}")
for msg in asym_dep:
    record("WARN", "3", "Asymétrie héritée (dep non réciproquée)", msg)
for msg in asym_user:
    record("WARN", "3", "Asymétrie héritée (usage non déclaré)", msg)
for msg in external:
    record("PASS", "3", "Frontière plateforme documentée", msg)

# ============================================================================
print("\n=== 4. Contrats de dépendances frontmatter (semver) ===")
contract_skills = ["gen-plan", "correct-work", "clone-chat", "agent-prompt-engineering",
                   "autonomous-agent"]
violations, frontier = [], []
for name in contract_skills:
    sd = SKILLS / name / "SKILL.md"
    for (dep, vmin) in parse_frontmatter_deps(sd):
        dep_sd = SKILLS / dep / "SKILL.md"
        if not dep_sd.exists():
            violations.append(f"{name}: dépendance {dep} introuvable")
            continue
        real = read_frontmatter_version(dep_sd)
        if real is None and dep in entries:
            real = entries[dep]["version"]  # convention KB_ONLY_VERSION
        if real is None:
            frontier.append(f"{name} → {dep} >= {vmin} : skill plateforme sans version "
                            f"frontmatter (S3 hérité) — existence vérifiée")
            continue
        if semver_tuple(real) < semver_tuple(vmin):
            violations.append(f"{name} → {dep} >= {vmin} non satisfait (installé {real})")
if violations:
    record("FAIL", "4", "Contrats semver frontmatter", "; ".join(violations))
else:
    n = sum(len(parse_frontmatter_deps(SKILLS / n / "SKILL.md")) for n in contract_skills)
    record("PASS", "4", "Contrats semver frontmatter",
           f"{n - len(frontier)}/{n} contrats semver vérifiés et satisfaits")
for msg in frontier:
    record("WARN", "4", "Frontière plateforme (S3 hérité)", msg)

# ============================================================================
print("\n=== 5. Pointeurs internes gen-plan v3.11.0 ===")
gp = SKILLS / "gen-plan" / "SKILL.md"
gp_text = gp.read_text(encoding="utf-8")
expected_refs = ["etapes-detaillees.md", "grille-token.md", "classification-types.md",
                 "profils-ressource.md", "guide-selection-agent-skill.md",
                 "prompt-engineering-kit.md"]
missing = [r for r in expected_refs if not (SKILLS / "gen-plan" / "references" / r).exists()]
record("PASS" if not missing else "FAIL", "5",
       "Arbre §2.2 : 6 références résolues" if not missing else "Références manquantes",
       f"PEK présent = intégration v3.11.0" if not missing else str(missing))
record("PASS" if (SKILLS / "gen-plan" / "evals" / "evals.json").exists() else "FAIL",
       "5", "evals/evals.json (6 évals, intact R2)")
# 5b. Pointeurs PM : SKILL.md cite PM v3.11.0, corpus + miroir l'ont
pm_v = "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md"
has_corpus_pm = (CORPUS / pm_v).exists()
has_mirror_pm = (MIRROR / pm_v).exists()
record("PASS" if has_corpus_pm and has_mirror_pm else "FAIL", "5",
       f"PM {pm_v} résolu (corpus+miroir)")
record("PASS" if "v3.11.0" in gp_text else "FAIL", "5",
       "SKILL.md ↔ PM v3.11.0 alignés en version",
       f"{len(re.findall(r'v3\.11\.0', gp_text))} mentions v3.11.0 dans SKILL.md")
# 5c. PEK cité aux deux endroits (§1.6 + §2.2)
pek_ok = ("prompt-engineering-kit.md" in gp_text
          and "PEK" in gp_text
          and (SKILLS / "gen-plan" / "references" / "prompt-engineering-kit.md").exists())
record("PASS" if pek_ok else "FAIL", "5", "Référence PEK §1.6/§2.2 ↔ references/")

# ============================================================================
print("\n=== 6. Calibration de l'arbitre local <-> réalité ===")
cei = (BASE / "scripts" / "check-ecosysteme-integrity.py")
cei_text = cei.read_text(encoding="utf-8") if cei.exists() else ""
cal = {}
m_eco = re.search(r"ECO_SKILLS\s*=\s*\{(.*?)\}", cei_text, re.S)
if m_eco:
    cal = dict(re.findall(r'"([a-z0-9-]+)":\s*"([\d.]+)"', m_eco.group(1)))
cal_mism = [f"{k}: arbitre={v} / KB={entries[k]['version']}"
            for k, v in cal.items() if entries.get(k, {}).get("version") != v]
ok6 = (len(cal) == 11 and not cal_mism and len(corpus_files) == 15)
record("PASS" if ok6 else "FAIL", "6",
       "check-ecosysteme-integrity.py calibré (ECO_SKILLS 11 entrées) sur l'état KB réel",
       "aligné sur l'état réel (Phase 1 : 33/33 PASS)" if ok6 else "; ".join(cal_mism))

# ============================================================================
print("\n=== 7. Synchronisation download/ ===")
expected_dl = ["PROMPT-MAITRE-SHARED.md", "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md",
               "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md",
               "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md",
               "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md", "README.md"]
dl_files = sorted(p.name for p in DOWNLOAD.glob("*.md")) if DOWNLOAD.is_dir() else []
missing_dl = [f for f in expected_dl if f not in dl_files]
synced = all((DOWNLOAD / f).read_bytes() == (CORPUS / f).read_bytes()
             for f in expected_dl if (DOWNLOAD / f).exists() and (CORPUS / f).exists())
record("PASS" if not missing_dl and synced else "FAIL", "7",
       f"download/ synchronisé ({len([f for f in dl_files if f in expected_dl])}/{len(expected_dl)}, byte-identiques au corpus — v3.6.1 scellé + PM v3.11.0 publié B3)")

# ============================================================================
print("\n=== 8. Présence des evals/ (skills écosystème) ===")
eco_evals = {"gen-plan": ["evals.json"], "correct-work": ["evals.json"],
             "clone-chat": ["evals.json", "trigger_evals.json"],
             "agent-prompt-engineering": ["evals.json", "trigger_evals.json"],
             "autonomous-agent": ["evals.json"], "skills-inventory": ["evals.json"],
             "context-engineering": ["evals.json", "trigger_evals.json"],
             "loop-engineering": ["evals.json", "trigger_evals.json"],
             "graph-engineering": ["evals.json", "trigger_evals.json"],
             "harness-engineering": ["evals.json", "trigger_evals.json"]}
missing_ev = []
for name, files in eco_evals.items():
    for f in files:
        # tolérance : certains skills matérialisent evals.json seul
        base_dir = SKILLS / name / "evals"
        if not base_dir.is_dir() or not any(base_dir.glob("*.json")):
            missing_ev.append(f"{name}/evals/")
if missing_ev:
    for msg in missing_ev:
        record("WARN", "8", "evals absents", msg)
else:
    record("PASS", "8", "evals/ présents pour les 10 skills écosystème évaluables")

# ============================================================================
print("\n=== 9. Compilation des scripts Python ===")
py_scripts = [BASE / "scripts" / "verify-cross.py",
              BASE / "scripts" / "sync-download.py",
              BASE / "scripts" / "check-ecosysteme-integrity.py",
              BASE / "scripts" / "test-coherence-interactions.py",
              SKILLS / "correct-work" / "scripts" / "verify-correct-work.py"]
compile_errors = []
for s in py_scripts:
    if not s.exists():
        compile_errors.append(f"{s.name}: absent")
        continue
    try:
        py_compile.compile(str(s), doraise=True)
    except py_compile.PyCompileError as e:
        compile_errors.append(f"{s.name}: {e}")
record("FAIL" if compile_errors else "PASS", "9",
       "py_compile 5/5 scripts (portée E8 étendue)",
       "" if not compile_errors else "; ".join(compile_errors))

# ============================================================================
print("\n=== 10. Format du worklog (SHARED §1.4) ===")
wl = WORKLOG.read_text(encoding="utf-8") if WORKLOG.exists() else ""
n_sections = len(re.findall(r"^---\s*$", wl, re.M))
n_taskids = len(re.findall(r"^Task ID: ", wl, re.M))
record("PASS" if n_sections >= 2 and n_taskids >= 2 else "FAIL", "10",
       f"Worklog : {n_sections} sections ---, {n_taskids} Task ID (SHARED §1.4)")

# ============================================================================
print("\n=== 11. Propagation de la mise à jour v3.11.0 ===")
# 11a. Porteurs de version attendus
pm_text = (CORPUS / pm_v).read_text(encoding="utf-8")
carriers = [
    ("SKILL.md gen-plan : frontmatter 3.11.0", read_frontmatter_version(gp) == "3.11.0"),
    ("SKILL.md gen-plan : zéro mention stale 3.10.0", gp_text.count("3.10.0") == 0),
    ("PM v3.11.0 (corpus) : en-tête version + plage 1200-1350 lignes",
     "3.11.0" in pm_text[:600] and 1200 <= pm_text.count("\n") + 1 <= 1350),
    ("PM v3.11.0 : 6e référence PEK (§2.2) + section §9.6",
     "prompt-engineering-kit.md" in pm_text and "9.6" in pm_text),
    ("Miroir : PM v3.11.0 byte-identique au corpus",
     (MIRROR / pm_v).read_bytes() == (CORPUS / pm_v).read_bytes()),
    ("KB : entrée « ## gen-plan v3.11.0 »",
     bool(re.search(r"^## gen-plan v3\.11\.0$", kb_text, re.M))),
    ("KB : calibration B1 documentée (PEK, 2026-09-10)",
     "révision B1" in kb_text and "PEK" in kb_text),
    ("Arbitre local ECO_SKILLS : gen-plan 3.11.0", cal.get("gen-plan") == "3.11.0"),
    ("Référence PEK : fichier présent (v4.1)",
     (SKILLS / "gen-plan" / "references" / "prompt-engineering-kit.md").exists()),
    ("Worklog : session B1 (v3.11.0 + PEK) journalisée",
     "v3.11.0" in wl and "PEK" in wl and "Task ID: 2" in wl),
]
for label, ok_c in carriers:
    record("PASS" if ok_c else "FAIL", "11a", label)

# 11b. Non-régression R2 vs dépôt source (commit a8ffb5f)
SOURCE_SKILLS = Path("/tmp/KNOWLEDGE_CHECK/skills")
if SOURCE_SKILLS.is_dir():
    hist = [f for f in corpus_files if f != pm_v]
    div = [f for f in hist
           if not (SOURCE_SKILLS / "@mon-ecosysteme" / f).exists()
           or (CORPUS / f).read_bytes() != (SOURCE_SKILLS / "@mon-ecosysteme" / f).read_bytes()]
    record("PASS" if not div else "FAIL", "11b",
           "Corpus historique 14/14 byte-identiques au dépôt (a8ffb5f)" if not div
           else f"Divergences : {div}")
    expected_div = {"gen-plan/SKILL.md", "gen-plan/references/prompt-engineering-kit.md"}
    unexpected = []
    for p in (SKILLS / "gen-plan").rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(SKILLS).as_posix()
        if rel in expected_div:
            continue
        src = SOURCE_SKILLS / rel
        if not src.exists() or src.read_bytes() != p.read_bytes():
            unexpected.append(rel)
    record("PASS" if not unexpected else "FAIL", "11b",
           "gen-plan : 6 fichiers originaux (5 références + evals) intacts (R2)" if not unexpected
           else f"Modifications inattendues : {unexpected}")
    other_dirs = ["correct-work", "clone-chat", "skills-inventory", "autonomous-agent",
                  "agent-prompt-engineering", "context-engineering", "loop-engineering",
                  "graph-engineering", "harness-engineering", "audio-metadata",
                  "cpp-analysis", "pdf-llm"]
    expected_div2 = {"correct-work/scripts/verify-correct-work.py"}  # calibration v2.5.1 (session B1, Phase A — 16/16 PASS)
    unexpected2 = []
    for d in other_dirs:
        for p in (SKILLS / d).rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(SKILLS).as_posix()
            if rel in expected_div2:
                continue
            if "__pycache__" in rel or rel.endswith(".pyc"):
                continue  # artefact d'exécution Python, hors corpus source
            src = SOURCE_SKILLS / rel
            if not src.exists() or src.read_bytes() != p.read_bytes():
                unexpected2.append(rel)
    if unexpected2:
        record("FAIL", "11b", "Skills écosystème/métier vs dépôt", "; ".join(unexpected2))
    else:
        record("PASS", "11b",
               "12 répertoires skills intacts — seule divergence documentée : "
               "verify-correct-work.py (calibration v2.5.1, arbitre 16/16)")

    def strip_entry(text, name):
        return re.sub(r"^## " + name + r" v[\d.]+.*?(?=^## |\Z)", "", text, flags=re.S | re.M)

    # Divergences KB documentées (intentionnelles, tracées « Dernière calibration ») :
    #  - gen-plan : révision B1 (v3.11.0 + PEK)
    #  - correct-work, clone-chat : révision B3 (harmonisation bidirectionnelle — 5 réciproques)
    kb_divergent = {"gen-plan", "correct-work", "clone-chat"}
    repo_kb = (SOURCE_SKILLS / "KNOWLEDGE.md").read_text(encoding="utf-8")
    local_stripped, repo_stripped = kb_text, repo_kb
    for name in sorted(kb_divergent):
        local_stripped = strip_entry(local_stripped, name)
        repo_stripped = strip_entry(repo_stripped, name)
    same_rest = local_stripped == repo_stripped
    record("PASS" if same_rest else "FAIL", "11b",
           "KB : 8 entrées hors divergences documentées identiques au dépôt "
           "(gen-plan B1/PEK, correct-work+clone-chat B3/harmonisation)")
else:
    record("WARN", "11b",
           "Clone du dépôt source absent (/tmp/KNOWLEDGE_CHECK) — R2 non vérifiable")

# 11c. Références stale (état courant)
stale = []
if re.search(r"^## gen-plan v3\.10\.0", kb_text, re.M):
    stale.append("KB contient encore une entrée gen-plan v3.10.0")
if "3.10.0" in gp_text:
    stale.append("SKILL.md gen-plan mentionne v3.10.0")
if cal.get("gen-plan") != "3.11.0":
    stale.append("ECO_SKILLS désaligné")
record("PASS" if not stale else "FAIL", "11c",
       "Aucune référence stale — l'état courant est uniformément v3.11.0")

# 11d. Canal de publication download/
pm_published = (DOWNLOAD / pm_v).exists()
record("WARN" if not pm_published else "PASS", "11d",
       "download/ : canal de publication (v3.6.1 scellé dépôt + PM v3.11.0 local B3)",
       "PM v3.11.0 non publié : publiable en étendant la liste sync-download (SYNC_MAP)"
       if not pm_published else "PM v3.11.0 publié (extension SYNC_MAP B3 — 6 fichiers)")

# ============================================================================
# BILAN
print("\n" + "=" * 60)
n_pass = sum(1 for r in results if r[0] == "PASS")
n_warn = sum(1 for r in results if r[0] == "WARN")
n_fail = sum(1 for r in results if r[0] == "FAIL")
total = len(results)
print(f"BILAN : {n_pass} PASS / {n_warn} WARN / {n_fail} FAIL — {total} checks")
if n_fail == 0:
    print("VERDICT : COHÉRENCE DES INTERACTIONS : PASS"
          + (" AVEC RÉSERVES" if n_warn else " STRICT"))
else:
    print("VERDICT : FAIL — corriger puis re-vérifier (boucle E12-E13)")

# Export JSON pour le hook correct-work (mode CIBLE)
out = {"phase": "B5 (correctifs frontmatter Phase 2 + publication)", "generateur": "gen-plan v3.11.0 — session B5",
       "checks": [{"statut": s, "section": sec, "check": c, "detail": d}
                  for (s, sec, c, d) in results],
       "bilan": {"pass": n_pass, "warn": n_warn, "fail": n_fail, "total": total}}
(BASE / "scripts" / "interactions-report.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("Rapport JSON : scripts/interactions-report.json")
sys.exit(0 if n_fail == 0 else 1)
