#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

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

Périmètre (complémentaire des arbitres existants, focalisé sur les INTERACTIONS) —
RECALIBRÉ Architecture v2.0 (corrige-ecosysteme, session B8) : le miroir
_prompts-maitres/ est supprimé (KB §Décisions) — relation corpus↔miroir remplacée
par corpus↔archive round-trip ; la référence R2 §11b devient le ZIP correct-mon-eco
(source v2.0 fournie par le propriétaire) à la place du clone a8ffb5f (pré-v2.0) :
  1. Corpus @mon-ecosysteme (16 fichiers) <-> Archive round-trip (véhicule v2.0)
  2. Registre KNOWLEDGE.md : versions déclarées <-> versions réelles SKILL.md
     (12 entrées versionnées + section « Décisions d'architecture »)
  3. Graphe de relations KB : bidirectionnalité « Dépend de » <-> « Utilisé par »
     (parse le format LISTE réel du KB ; verify-cross CHECK 7.6 calibré sur ce
      même format en session B4 — cross-validation : arêtes des deux côtés)
  4. Contrats de dépendances frontmatter (semver >=) vs versions installées
  5. Pointeurs internes gen-plan : arbre §2.2 (6 références + evals), pointeurs PM
     v3.11.0 (SKILL.md <-> corpus), référence PEK §1.6/§2.2
  6. Calibration de l'arbitre local check-ecosysteme-integrity.py <-> réalité
  7. Synchronisation download/ (17 fichiers attendus — Architecture v2.0)
  8. Présence des evals/ pour les skills écosystème
  9. Compilation des scripts Python (py_compile — portée E8 étendue)
 10. Format du worklog (sections ---, Task ID, SHARED §1.4)
 11. Propagation v2.0 : porteurs de version, R2 vs ZIP correct-mon-eco,
     références stale, canal de publication download/

Conventions : Python uniquement (N3), kebab-case, verdicts PASS/FAIL/WARN,
sortie structurée + score final. Adaptation = signal, jamais un arrêt (règle d'or n°1).
"""

import json
import py_compile
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent  # dynamisé (KO-L003, 2026-10-02) — chemin en dur "/home/z/my-project" cassé après relocalisation du dépôt
SKILLS = BASE / "skills"
CORPUS = SKILLS / "@mon-ecosysteme"
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
ZIP_REF = BASE / "tmp" / "correct-mon-eco"   # référence v2.0 (source propriétaire)
KB_PATH = SKILLS / "KNOWLEDGE.md"
DOWNLOAD = BASE / "download"
WORKLOG_CANDIDATES = [BASE / "worklog.md", BASE.parent / "worklog.md"]  # dynamisé (KO-L003, 2026-10-02) : artefact de session, hors périmètre versionné
WORKLOG = next((p for p in WORKLOG_CANDIDATES if p.exists()), WORKLOG_CANDIDATES[0])

# Convention KB_ONLY_VERSION LEVÉE (corrige-ecosysteme G-bis) : skill-creator
# porte désormais sa version dans le frontmatter (v1.0.0) comme les autres skills.
KB_ONLY_VERSION = set()

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
print("\n=== 1. Corpus <-> Archive round-trip (véhicule v2.0) ===")
corpus_files = sorted(p.name for p in CORPUS.glob("*.md")) if CORPUS.is_dir() else []
# [dynamisation future-proof N14-b] attendu calibré sur SYNC_MAP du check-ecosysteme-integrity
_cei_src = (BASE / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")
_m_sm = re.search(r"SYNC_MAP\s*=\s*\[(.*?)\]", _cei_src, re.S)
_m_cc = re.search(r"CORPUS_ATTENDU\s*=\s*(\d+)", _cei_src) or re.search(r"len\(corpus_files\)\s*==\s*(\d+)", _cei_src)
_expected_corpus = int(_m_cc.group(1)) if _m_cc else (len(re.findall(r'"([^"]+\.md)"', _m_sm.group(1))) if _m_sm else len(corpus_files))
record("PASS" if len(corpus_files) == _expected_corpus else "WARN", "1",
       f"Corpus = {len(corpus_files)} fichiers ({_expected_corpus} attendus — Architecture v2.0, SYNC-CONTEXT inclus, calibré CORPUS_ATTENDU N14-c)")
import zipfile
identical, divergent, n_zip = 0, [], 0
extras_hors_homologues = []
if ARCHIVE.is_file():
    with zipfile.ZipFile(ARCHIVE) as z:
        znames = [n for n in z.namelist() if not n.endswith("/")]
        n_zip = len(znames)
        for name in corpus_files:
            match = [n for n in znames if n.split("@mon-ecosysteme/")[-1] == name]
            if match and z.read(match[0]) == (CORPUS / name).read_bytes():
                identical += 1
            else:
                divergent.append(name)
        # v2.1 (N25/N26, recalibrage L004) : corpus ⊆ archive byte-identique +
        # extras uniquement sous homologues/ (famille créateur/relecture).
        _corpus_set = set(corpus_files)
        extras_hors_homologues = [
            n for n in znames
            if (n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n) not in _corpus_set
            and not n.startswith("homologues/")
        ]
if divergent or extras_hors_homologues:
    record("FAIL", "1", "Round-trip archive ↔ corpus",
           f"divergents : {divergent or '—'} ; extras hors homologues/ : {extras_hors_homologues or '—'} (zip={n_zip}, corpus={len(corpus_files)})")
else:
    record("PASS", "1", "Round-trip archive ↔ corpus",
           f"{identical}/{len(corpus_files)} identiques + {n_zip - len(corpus_files)} homologues v2.1 (remplace le miroir supprimé — KB §Décisions)")

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

record("PASS" if len(entries) == 16 else "FAIL", "2",
       f"Registre parsé : {len(entries)} entrées versionnées (16 attendues — v2.0/N20/N25/N27)")

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
           f"{len(entries)}/{len(entries)} alignées (convention KB_ONLY_VERSION levée — skill-creator versionné)")

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
contract_skills = ["gen-plan", "correct-work", "clone-chat", "prompt-engineering",
                   "agent-creator"]
violations, frontier = [], []
for name in contract_skills:
    sd = SKILLS / name / "SKILL.md"
    for (dep, vmin) in parse_frontmatter_deps(sd):
        dep_sd = SKILLS / dep / "SKILL.md"
        if not dep_sd.exists():
            # Dynamisé (KO-L003, 2026-10-02) : dép non matérialisée = skill plateforme
            # (ex. fullstack-dev) — frontière documentée (check 3), pas une violation.
            frontier.append(f"{name} → {dep} >= {vmin} : skill plateforme non matérialisé "
                            f"(existence documentée — check 3)")
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
print("\n=== 5. Pointeurs internes gen-plan (version dynamisée) ===")
gp = SKILLS / "gen-plan" / "SKILL.md"
gp_text = gp.read_text(encoding="utf-8")
expected_refs = ["etapes-detaillees.md", "grille-token.md", "classification-types.md",
                 "profils-ressource.md", "guide-selection-agent-skill.md",
                 "prompt-engineering-kit.md", "observation-patterns.md",
                 "answer-key-template.md", "graph-diamond-pattern.md"]
missing = [r for r in expected_refs if not (SKILLS / "gen-plan" / "references" / r).exists()]
record("PASS" if not missing else "FAIL", "5",
       "Arbre §2.2 : 9 références résolues (6 historiques + 3 patterns N20)" if not missing else "Références manquantes",
       f"PEK présent = v3.11.0 ; patterns N20 (answer-key, graph-diamond, observation)" if not missing else str(missing))
record("PASS" if (SKILLS / "gen-plan" / "evals" / "evals.json").exists() else "FAIL",
       "5", "evals/evals.json (6 évals, intact R2)")
# 5b. Pointeurs PM : SKILL.md cite le PM courant, corpus l'héberge (miroir supprimé v2.0)
# [dynamisation future-proof N14-b] gv = version installée (frontmatter = SoT)
gv = read_frontmatter_version(gp) or "3.12.0"
pm_v = f"PROMPT-MAITRE-GEN-PLAN-v{gv}.md"
has_corpus_pm = (CORPUS / pm_v).exists()
record("PASS" if has_corpus_pm else "FAIL", "5",
       f"PM {pm_v} résolu (corpus — Architecture v2.0 : emplacement unique)")
ver_hit = f"v{gv}" in gp_text or f"version: {gv}" in gp_text  # dynamisé : frontmatter sans préfixe v
record("PASS" if ver_hit else "FAIL", "5",
       f"SKILL.md ↔ PM v{gv} alignés en version",
       f"{len(re.findall('v?' + re.escape(gv), gp_text))} mentions de {gv} dans SKILL.md (frontmatter sans préfixe v accepté)")
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
# Recalibrage L004 (Task 56) : ok6 lit l'invariant canonique CORPUS_ATTENDU de
# l'arbitre integrity via _expected_corpus (regex, l. 128) — plus de codage en dur.
ok6 = (len(cal) == 16 and not cal_mism and len(corpus_files) == _expected_corpus)
record("PASS" if ok6 else "FAIL", "6",
       "check-ecosysteme-integrity.py calibré (ECO_SKILLS 16 entrées, corpus = CORPUS_ATTENDU) sur l'état KB réel",
       "aligné sur l'état réel v2.0/B13-r6" if ok6 else "; ".join(cal_mism))

# ============================================================================
print("\n=== 7. Synchronisation download/ ===")
expected_dl = [
    "PROMPT-MAITRE-SHARED.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.12.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.13.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.16.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md",
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
    # INSTALL-ECOSYSTEME.md retiré — fusion installateurs v1.1.0 (2026-10-02, R4)
    "SYNC-CONTEXT.md",
    "README.md",
]
dl_files = sorted(p.name for p in DOWNLOAD.glob("*.md")) if DOWNLOAD.is_dir() else []
missing_dl = [f for f in expected_dl if f not in dl_files]
synced = all((DOWNLOAD / f).read_bytes() == (CORPUS / f).read_bytes()
             for f in expected_dl if (DOWNLOAD / f).exists() and (CORPUS / f).exists())
record("PASS" if not missing_dl and synced else "FAIL", "7",
       f"download/ synchronisé ({len([f for f in dl_files if f in expected_dl])}/{len(expected_dl)}, byte-identiques au corpus — Architecture v2.0)")

# ============================================================================
print("\n=== 8. Présence des evals/ (skills écosystème) ===")
eco_evals = {"gen-plan": ["evals.json"], "correct-work": ["evals.json"],
             "knowledge-observer": ["evals.json", "trigger_evals.json"],
             "clone-chat": ["evals.json", "trigger_evals.json"],
             "prompt-engineering": ["evals.json", "trigger_evals.json"],
             "agent-creator": ["evals.json"], "skills-inventory": ["evals.json"],
             "skill-creator": ["evals", "trigger_evals.json"],
             "script-mon-ecosysteme-infrastructure": ["trigger_evals.json"],
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
    record("PASS", "8", "evals/ présents pour les 16 skills écosystème évaluables (v2.0)")

# ============================================================================
print("\n=== 9. Compilation des scripts Python ===")
py_scripts = [BASE / "scripts" / "verify-cross.py",
              BASE / "scripts" / "sync-download.py",
              BASE / "scripts" / "check-ecosysteme-integrity.py",
              BASE / "scripts" / "test-coherence-interactions.py",
              BASE / "scripts" / "certification-complete.py",
              BASE / "scripts" / "propagate-context.py",
              BASE / "scripts" / "sync-context-block.py",
              BASE / "scripts" / "install-ecosystem.py",
              SKILLS / "correct-work" / "scripts" / "verify-correct-work.py"]
compile_errors, absent = [], []
for s in py_scripts:
    if not s.exists():
        absent.append(s.name)  # dynamisé (KO-L003, 2026-10-02) : absents = perdus au wipe (WARN), pas FAIL
        continue
    try:
        py_compile.compile(str(s), doraise=True)
    except py_compile.PyCompileError as e:
        compile_errors.append(f"{s.name}: {e}")
record("FAIL" if compile_errors else "PASS", "9",
       f"py_compile {len(py_scripts) - len(absent)}/{len(py_scripts)} scripts présents",
       "" if not compile_errors else "; ".join(compile_errors))
if absent:
    record("WARN", "9", "Scripts référencés absents (perdus au wipe — règle d'or n°1, non reconstitués)",
           ", ".join(absent))

# ============================================================================
print("\n=== 10. Format du worklog (SHARED §1.4) ===")
wl = WORKLOG.read_text(encoding="utf-8") if WORKLOG.exists() else ""
n_sections = len(re.findall(r"^---\s*$", wl, re.M))
n_taskids = len(re.findall(r"^Task ID: ", wl, re.M))
_wl_state = "present" if WORKLOG.exists() else "absent (artefact de session non versionné — WARN)"
record("PASS" if (n_sections >= 2 and n_taskids >= 2) else ("WARN" if not wl else "FAIL"), "10",
       f"Worklog {_wl_state} : {n_sections} sections ---, {n_taskids} Task ID (SHARED §1.4)")

# ============================================================================
print(f"\n=== 11. Propagation de la mise à jour gen-plan v{gv} ===")
# 11a. Porteurs de version attendus [dynamisés future-proof N14-b — gv = frontmatter installé]
pm_text = (CORPUS / pm_v).read_text(encoding="utf-8")
carriers = [
    (f"SKILL.md gen-plan : frontmatter {gv}", read_frontmatter_version(gp) == gv),
    ("SKILL.md gen-plan : zéro mention stale 3.10.0", gp_text.count("3.10.0") == 0),
    (f"PM {pm_v} (corpus) : en-tête version + plage 1200-1400 lignes",
     gv in pm_text[:600] and 1200 <= pm_text.count("\n") + 1 <= 1400),
    ("PM : 6e référence PEK (§2.2) + section §9.6",
     "prompt-engineering-kit.md" in pm_text and "9.6" in pm_text),
    ("download/ : PM courant byte-identique au corpus (canal public v2.0 — remplace le miroir)",
     (DOWNLOAD / pm_v).exists() and (DOWNLOAD / pm_v).read_bytes() == (CORPUS / pm_v).read_bytes()),
    (f"KB : entrée « ## gen-plan v{gv} »",
     bool(re.search(r"^## gen-plan v" + re.escape(gv) + r"$", kb_text, re.M))),
    ("KB : calibration B1 documentée (PEK, 2026-09-10)",
     "révision B1" in kb_text and "PEK" in kb_text),
    (f"Arbitre local ECO_SKILLS : gen-plan {gv}", cal.get("gen-plan") == gv),
    ("Référence PEK : fichier présent (v4.1)",
     (SKILLS / "gen-plan" / "references" / "prompt-engineering-kit.md").exists()),
]
for label, ok_c in carriers:
    record("PASS" if ok_c else "FAIL", "11a", label)
# Historique B1 : artefact du worklog propriétaire, non cloné (dynamisé KO-L003 — WARN, pas FAIL)
_b1 = "v3.11.0" in wl and "PEK" in wl
record("PASS" if _b1 else "WARN", "11a",
       "Worklog : historique B1 (v3.11.0 + PEK) — artefact historique propriétaire",
       "" if _b1 else "worklog de session courant ne porte pas l'historique B1 (non cloné)")

# 11b. Non-régression R2 vs référence v2.0 (ZIP correct-mon-eco fourni par le propriétaire)
# Ancienne référence (/tmp/KNOWLEDGE_CHECK @ a8ffb5f) obsolète post-v2.0 : le corpus
# a divergé INTENTIONNELLEMENT (16 fichiers, SYNC-CONTEXT, README v2.0, §0 injectés).
if ZIP_REF.is_dir():
    # [dynamisation future-proof N14-b] config.json strict ; README/SYNC-CONTEXT évoluent
    # en R2 (corpus courant v3.12.0) — leur divergence vs ZIP v2.0 gelé est INTENTIONNELLE.
    pairs_strict = [(ZIP_REF / "config.json", BASE / "config.json")]
    pairs_r2 = [(ZIP_REF / "docs" / "README.md", CORPUS / "README.md"),
                (ZIP_REF / "docs" / "SYNC-CONTEXT.md", CORPUS / "SYNC-CONTEXT.md")]
    div_strict = [f"{p.name}" for p, c in pairs_strict
                  if not p.exists() or not c.exists() or p.read_bytes() != c.read_bytes()]
    r2_non_appliquee = [f"{p.name}" for p, c in pairs_r2
                        if p.exists() and c.exists() and p.read_bytes() == c.read_bytes()]
    ok_11b = not div_strict and not r2_non_appliquee
    record("PASS" if ok_11b else "FAIL", "11b",
           "Référence v2.0 : config.json byte-identique ; README/SYNC-CONTEXT divergés R2 (intentionnel — corpus v3.12.0)"
           if ok_11b else f"Divergences strictes : {div_strict} · R2 non appliquée : {r2_non_appliquee}")
else:
    record("PASS", "11b",
           "R2 vs ZIP v2.0 non applicable (référence correct-mon-eco absente de cet environnement)")

# 11c. Références stale (état courant)
stale = []
if re.search(r"^## gen-plan v3\.10\.0", kb_text, re.M):
    stale.append("KB contient encore une entrée gen-plan v3.10.0")
if "3.10.0" in gp_text:
    stale.append("SKILL.md gen-plan mentionne v3.10.0")
if cal.get("gen-plan") != gv:
    stale.append("ECO_SKILLS désaligné")
record("PASS" if not stale else "FAIL", "11c",
       f"Aucune référence stale — l'état courant est uniformément v{gv}")

# 11d. Canal de publication download/
pm_published = (DOWNLOAD / pm_v).exists()
record("WARN" if not pm_published else "PASS", "11d",
       f"download/ : canal de publication (v3.6.1 scellé dépôt + PM v{gv} local)",
       f"PM v{gv} non publié : publiable en étendant la liste sync-download (SYNC_MAP)"
       if not pm_published else f"PM v{gv} publié (SYNC_MAP 17 fichiers — N14-b)")

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
out = {"phase": "B8 (installation écosystème corrigé v2.0 + affinage trigger_evals skill-creator)",
       "generateur": "gen-plan v3.11.0 — session B8",
       "checks": [{"statut": s, "section": sec, "check": c, "detail": d}
                  for (s, sec, c, d) in results],
       "bilan": {"pass": n_pass, "warn": n_warn, "fail": n_fail, "total": total}}
(BASE / "scripts" / "interactions-report.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("Rapport JSON : scripts/interactions-report.json")
sys.exit(0 if n_fail == 0 else 1)
