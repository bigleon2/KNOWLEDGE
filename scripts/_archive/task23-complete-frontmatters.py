#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 23 (D005/D007) — Complétion mécanique des frontmatters des skills tiers
de la couche (exigence SHARED §1.3 + arbitre N1 check-tool-routing) :
  - version  : metadata.version si présente, sinon 1.0.0 (jamais d'écrasement)
  - category : classification du scanner skills-inventory (source mécanique)
  - tags     : radicaux du NOM du skill (tags neutres — précédent Task 22 :
    les tags injectent des radicaux, donc uniquement ceux du nom lui-même)
Idempotent : second passage = 0 modification. Ne touche PAS aux 26 équipés.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path("/home/z/my-project/ecosystem")
SK = ROOT / "skills"
EXCLUDE = {"@mon-ecosysteme", "KNOWLEDGE.md"}

scan = json.loads(subprocess.run(
    "python3 skills/skills-inventory/scripts/generate_skills_md.py --json",
    cwd=ROOT, shell=True, capture_output=True, text=True).stdout or "[]")
CAT = {x["name"]: x.get("category", "Autres") for x in scan}


def radicaux(name: str) -> list:
    parts = [p for p in re.split(r"[-_]", name) if p]
    return parts[:4]


def complete(fm_text: str, name: str) -> tuple:
    lines = fm_text.splitlines()
    has = lambda k: any(l.startswith(f"{k}:") for l in lines)
    out, changed = [], False
    # version après name
    meta_v = re.search(r"version:\s*[\"']?([\d.]+)", fm_text)
    for l in lines:
        out.append(l)
        if l.startswith("name:") and not has("version"):
            v = (re.search(r"^\s*version:\s*[\"']?([\d.]+)", fm_text, re.M) or meta_v)
            out.append(f"version: \"{v.group(1) if v else '1.0.0'}\"")
            changed = True
        if (l.startswith("version:") or l.startswith("name:")) and not has("category"):
            out.append(f"category: \"{CAT.get(name, 'Autres')}\"")
            changed = True
            # re-scan : category ajoutée, vérifier tags juste après
            if not has("tags"):
                out.append("tags:")
                for t in radicaux(name):
                    out.append(f"  - {t}")
                changed = True
    # tags manquants sans ancre (cas name absent)
    if not has("tags") and not any(l.startswith("tags:") for l in out):
        out.extend(["tags:"] + [f"  - {t}" for t in radicaux(name)])
        changed = True
    return "\n".join(out) + "\n", changed


modifies = subprocess.run(
    "git diff --name-only HEAD -- ':(exclude).next'",
    cwd=ROOT, shell=True, capture_output=True, text=True).stdout.split()
n_ok = n_skip = 0
for f in sorted(set(modifies)):
    m = re.match(r"skills/([^/@][^/]*)/SKILL\.md$", f)
    if not m or m.group(1) in EXCLUDE:
        continue
    name = m.group(1)
    p = ROOT / f
    txt = p.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        n_skip += 1
        continue
    end = txt.find("\n---", 3)
    fm, body = txt[:end], txt[end:]
    if all(k in fm for k in ("version:", "category:", "tags:")):
        n_skip += 1
        continue
    new_fm, ch = complete(fm, name)
    if ch:
        p.write_text(new_fm + body, encoding="utf-8")
        n_ok += 1
print(f"frontmatters complétés : {n_ok} ; déjà conformes/ignorés : {n_skip}")
sys.exit(0)
