#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan-versions-reelles.py — Item 3c, session B6 (Task ID 7).

Identifie les skills métier dont le frontmatter `version: 1.0.0` fut inventé
par la Phase 2 (fix-frontmatter.py : champ version absent -> 1.0.0), puis
recherche leurs VRAIES versions dans les sources structurées locales,
par priorité décroissante :

  P1  frontmatter `metadata.version`   (convention Z.AI, cf. ZAI_METADATA_SKILLS
                                        de fix-frontmatter.py — champ conserve
                                        intact par la Phase 2)
  P2  skill.json                       (manifeste auteur)
  P3  skill.yaml                       (manifeste auteur)
  P4  _meta.json / metadata.json       (recu de publication ClawHub)
  P5  CHANGELOG.md                     (premiere entree = version la plus recente)
  P6  package.json                     (version du paquet)

Le clone de reference /tmp/KNOWLEDGE_CHECK (a8ffb5f, pristine, utilise par
le test d'interactions 11b) fournit l'etat pre-Phase 2 : l'absence de champ
`version` top-level dans l'original signale la valeur inventee.

Garde-fou contrat semver (section 4 de test-coherence-interactions.py) :
un skill cible d'une dependance declaree (ex. fullstack-dev >= 1.0.0 declare
par correct-work) n'est enrichi que si la vraie version satisfait le plancher.

Modes :
  defaut       : scan + rapport, AUCUNE ecriture sur les skills
  --apply      : enrichment chirurgical — SEULE la ligne `version:` du
                 frontmatter est remplacee ; corps byte-identique garanti,
                 re-parse YAML verifie, champs requis CHECK 8 verifies.

Rapport JSON : scripts/versions-reelles-report.json
"""

import json
import re
import sys
from pathlib import Path

import yaml

SKILLS = Path("/home/z/my-project/skills")
CLONE = Path("/tmp/KNOWLEDGE_CHECK/skills")
REPORT = Path("/home/z/my-project/scripts/versions-reelles-report.json")

ECOSYSTEM = {"gen-plan", "correct-work", "clone-chat", "skills-inventory",
             "skill-creator", "autonomous-agent"}
CONTRACT_SKILLS = ["gen-plan", "correct-work", "clone-chat",
                   "agent-prompt-engineering", "autonomous-agent"]

APPLY = "--apply" in sys.argv

# ----------------------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------------------


def split_frontmatter(text):
    """(head_raw, body) ; head_raw = texte exact entre les deux '---'."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def fm_dict(head_raw):
    if head_raw is None:
        return {}
    try:
        return yaml.safe_load(head_raw) or {}
    except yaml.YAMLError:
        return {}


def norm_semver(value):
    """Normalise '1.0' / 1.0 / 'v2.0.1' / '0.1.0' -> 'X.Y.Z' ; sinon None."""
    if value is None:
        return None
    m = re.match(r"^\s*v?(\d+)\.(\d+)(?:\.(\d+))?", str(value))
    if not m:
        return None
    return f"{m.group(1)}.{m.group(2)}.{m.group(3) or '0'}"


def semver_tuple(v):
    m = re.match(r"(\d+)\.(\d+)\.(\d+)", v)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def read_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def read_yaml_file(path):
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def changelog_version(path):
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"^##\s*v?(\d+\.\d+(?:\.\d+)?)", text, re.M)
    return norm_semver(m.group(1)) if m else None


def parse_frontmatter_deps(path):
    """[(skill, version_min)] — regex identiques a la section 4 du test."""
    deps = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return deps
    head, _ = split_frontmatter(text)
    if head is None:
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
        vm = re.search(r'version:\s*"?>?=?\s*(\d+\.\d+\.\d+)', line)
        if vm and cur:
            deps.append((cur, vm.group(1)))
            cur = None
    return deps


# ----------------------------------------------------------------------------
# Planchers de contrats semver (section 4 du test d'interactions)
# ----------------------------------------------------------------------------

floors = {}
for name in CONTRACT_SKILLS:
    for dep, vmin in parse_frontmatter_deps(SKILLS / name / "SKILL.md"):
        if dep not in floors or semver_tuple(vmin) > semver_tuple(floors[dep]):
            floors[dep] = vmin

print("Contrats semver detectes (cibles hors ecosysteme seulement) :")
for dep, vmin in sorted(floors.items()):
    if dep not in ECOSYSTEM:
        print(f"  {dep} >= {vmin}")

# ----------------------------------------------------------------------------
# Scan des skills metier (enumeration identique a verify-cross CHECK 8)
# ----------------------------------------------------------------------------

PRIORITY = ("metadata.version", "skill.json", "skill.yaml",
            "_meta.json", "metadata.json", "CHANGELOG.md", "package.json")

rows = []
for d in sorted(SKILLS.iterdir()):
    if not d.is_dir() or d.name.startswith(("_", "@")) or d.name in ECOSYSTEM:
        continue
    skill_md = d / "SKILL.md"
    if not skill_md.is_file():
        continue

    text = skill_md.read_text(encoding="utf-8")
    head, _ = split_frontmatter(text)
    cur_fm = fm_dict(head)
    cur_ver = norm_semver(cur_fm.get("version"))

    # Etat pre-Phase 2 (clone de reference a8ffb5f)
    orig_fm = {}
    clone_md = CLONE / d.name / "SKILL.md"
    if clone_md.is_file():
        ohead, _ = split_frontmatter(clone_md.read_text(encoding="utf-8"))
        orig_fm = fm_dict(ohead)
    orig_ver = norm_semver(orig_fm.get("version"))
    invented = cur_ver is not None and orig_ver is None

    # Sources structurees
    sources = {}
    md = cur_fm.get("metadata")
    if isinstance(md, dict):
        v = norm_semver(md.get("version"))
        if v:
            sources["metadata.version"] = v
    for fn in ("skill.json", "skill.yaml"):
        data = read_json(d / fn) if fn.endswith(".json") else read_yaml_file(d / fn)
        if data:
            v = norm_semver(data.get("version"))
            if v:
                sources[fn] = v
    for fn in ("_meta.json", "metadata.json"):
        data = read_json(d / fn)
        if data:
            v = norm_semver(data.get("version"))
            if v:
                sources[fn] = v
    v = changelog_version(d / "CHANGELOG.md")
    if v:
        sources["CHANGELOG.md"] = v
    data = read_json(d / "package.json")
    if data:
        v = norm_semver(data.get("version"))
        if v:
            sources["package.json"] = v

    real = next((sources[k] for k in PRIORITY if k in sources), None)
    real_source = next((k for k in PRIORITY if k in sources), None)

    # Statut / action
    if not invented:
        status, action, note = "reelle-conservee", None, (
            f"version originale {orig_ver} conservee par la Phase 2")
    elif real is None:
        status, action, note = "inventee-sans-source", None, (
            "aucune version declaree dans les sources locales — 1.0.0 documente")
    elif real == cur_ver:
        status, action, note = "inventee-confirmee", None, (
            f"vraie version ({real_source}) == 1.0.0 inventee")
    else:
        floor = floors.get(d.name)
        if floor and semver_tuple(real) < semver_tuple(floor):
            status, action, note = "contrat-bloque", None, (
                f"vraie version {real} < plancher contrat >= {floor} — 1.0.0 conserve")
        else:
            status, action, note = "enrichissable", real, (
                f"source {real_source}")

    rows.append({
        "skill": d.name,
        "version_courante": cur_ver,
        "version_originale_clone": orig_ver,
        "inventee_phase2": invented,
        "sources": sources,
        "vraie_version": real,
        "source_prioritaire": real_source,
        "statut": status,
        "action": action,
        "note": note,
        "apply_status": None,
    })

# ----------------------------------------------------------------------------
# Application chirurgicale (--apply)
# ----------------------------------------------------------------------------

applied, errors = [], []
if APPLY:
    for row in rows:
        if not row["action"]:
            continue
        p = SKILLS / row["skill"] / "SKILL.md"
        text = p.read_text(encoding="utf-8")
        head, _ = split_frontmatter(text)
        new_head, n = re.subn(r"^version:.*$", f"version: {row['action']}",
                              head, count=1, flags=re.M)
        if n != 1:
            row["apply_status"] = "ERREUR : ligne version introuvable"
            errors.append(row["skill"])
            continue
        new_text = text.replace(head, new_head, 1)
        nh, nbody = split_frontmatter(new_text)
        nfm = fm_dict(nh)
        _, obody = split_frontmatter(text)
        ok = (norm_semver(nfm.get("version")) == row["action"]
              and nbody == obody
              and all(k in nfm for k in ("version", "category", "language",
                                         "tags", "dependencies")))
        if ok:
            p.write_text(new_text, encoding="utf-8")
            row["apply_status"] = "applique"
            applied.append(row["skill"])
        else:
            row["apply_status"] = "ERREUR : verification post-ecriture"
            errors.append(row["skill"])

# ----------------------------------------------------------------------------
# Rapport
# ----------------------------------------------------------------------------

def count(status):
    return sum(1 for r in rows if r["statut"] == status)

print(f"\nSkills metier scannes : {len(rows)}")
print(f"  reelle-conservee       (version originale, Phase 2/conformes) : {count('reelle-conservee')}")
print(f"  inventee-confirmee     (vraie version retrouvee == 1.0.0)     : {count('inventee-confirmee')}")
print(f"  enrichissable          (vraie version != 1.0.0)               : {count('enrichissable')}")
print(f"  contrat-bloque         (plancher semver non satisfait)        : {count('contrat-bloque')}")
print(f"  inventee-sans-source   (aucune version declaree localement)   : {count('inventee-sans-source')}")

print("\nEnrichissements (vraies versions) :")
for r in rows:
    if r["statut"] == "enrichissable":
        print(f"  {r['skill']:32s} {r['version_courante']} -> {r['action']:8s} [{r['source_prioritaire']}]"
              + (f"  ({r['apply_status']})" if r["apply_status"] else ""))
if count("enrichissable") == 0:
    print("  (aucun)")

print("\nConfirmations (vraie version == 1.0.0 inventee) :")
for r in rows:
    if r["statut"] == "inventee-confirmee":
        print(f"  {r['skill']:32s} 1.0.0 ( reel, via {r['source_prioritaire']})")

print("\nSans source (1.0.0 documente comme convention) :")
for r in rows:
    if r["statut"] == "inventee-sans-source":
        print(f"  {r['skill']}")

print("\nContrats bloques :")
for r in rows:
    if r["statut"] == "contrat-bloque":
        print(f"  {r['skill']} — {r['note']}")
if count("contrat-bloque") == 0:
    print("  (aucun)")

if APPLY:
    print(f"\nAPPLY : {len(applied)} skills enrichis, {len(errors)} erreurs")
    if errors:
        for e in errors:
            print(f"  ERREUR : {e}")

REPORT.write_text(json.dumps({
    "session": "B6 (Task ID 7, item 3c)",
    "mode": "apply" if APPLY else "scan",
    "contrats_semver_cibles_metier": {d: v for d, v in floors.items()
                                      if d not in ECOSYSTEM},
    "totaux": {s: count(s) for s in ("reelle-conservee", "inventee-confirmee",
                                     "enrichissable", "contrat-bloque",
                                     "inventee-sans-source")},
    "appliques": applied,
    "erreurs": errors,
    "skills": rows,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRapport JSON : {REPORT}")
