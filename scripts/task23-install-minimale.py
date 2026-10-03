#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 23 (D005) — Installation MINIMALE : fermeture mécanique de dépendances.
Pipeline PM-INSTALL v1.4.0 §2bis — l'élagage ne touche que l'arbre INSTALLÉ,
jamais le corpus @mon-ecosysteme/ ni l'archive d'intégrité (v2.2).

  (défaut)  calcule la fermeture + manifest scripts/install-profile.json + gain disque
  --apply   matérialise en plus une copie élaguée /home/z/my-project/ecosystem-minimale/
  --check   re-vérifie la fermeture (idempotence : même manifest = même empreinte)

Fermeture = {gen-plan, correct-work, skills-inventory}
          ∪ dépendances (frontmatter YAML + KB « Dépend de », transitif)
          ∪ agents {ULTRA, SHARED, SYNC-CONTEXT, INSTALL-ECOSYSTEME}
          ∪ {KNOWLEDGE.md} ∪ {scripts/}
"""
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path("/home/z/my-project/ecosystem")
MP = Path("/home/z/my-project")
MINI = MP / "ecosystem-minimale"
KB = ROOT / "skills/KNOWLEDGE.md"
SEEDS = ["gen-plan", "correct-work", "skills-inventory"]
AGENTS_OBLIGATOIRES = [
    "skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
    "skills/@mon-ecosysteme/SYNC-CONTEXT.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
]


def sh(cmd, cwd=ROOT):
    return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True).stdout


def deps_frontmatter(skill: str) -> list:
    fm = (ROOT / f"skills/{skill}/SKILL.md")
    if not fm.exists():
        return []
    txt = fm.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^dependencies:\n((?:[ \t]+.*\n?)+)", txt, re.M)
    if not m:
        return []
    deps, cur, opt = [], None, False
    for line in m.group(1).splitlines():
        it = re.match(r"\s+-\s+(.*)", line)
        if it:
            if cur and not opt:
                deps.append(cur)
            cur, opt = None, False
            nm = (re.search(r"skill:\s*([a-z0-9-]+)", it.group(1))
                  or re.match(r"([a-z0-9-]+)\s*$", it.group(1)))
            if nm:
                cur = nm.group(1)
            if re.search(r"optional:\s*true", it.group(1)):
                opt = True
        elif cur and re.search(r"optional:\s*true", line):
            opt = True
    if cur and not opt:
        deps.append(cur)
    return deps


def deps_kb(skill: str) -> list:
    kb = KB.read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"^## {re.escape(skill)} v[0-9.]+\s*$(.*?)(?=^## |\Z)", kb, re.M | re.S)
    if not m:
        return []
    d = re.search(r"\*\*Dépend de\*\*\s*:\s*(.+)", m.group(1))
    if not d:
        return []
    deps = []
    for item in split_top(d.group(1)):
        item = item.strip()
        if not item or re.match(r"^(aucune|N/A|—|–|-)", item):
            continue
        if "optionnel" in item:
            continue  # un élément optionnel n'est pas « nécessaire » (D005)
        nm = re.match(r"([a-z0-9][a-z0-9-]*)", item)
        if nm:
            deps.append(nm.group(1))
    return deps


def split_top(s: str) -> list:
    """Split sur les virgules de profondeur 0 (jamais à l'intérieur de parenthèses)."""
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


# Supplément normatif §2bis (affectations SHARED §7 + routage §1.16) : mobilisés
# par gen-plan à l'exécution sans être des dépendances YAML déclarées.
SUPPLEMENT_NORMATIF = ["skill-creator", "agent-creator", "script-creator",
                       "script-reviewer", "script-mon-ecosysteme-infrastructure",
                       "audit-provenance", "skill-finder-cn"]


def existe_skill(s: str) -> bool:
    return (ROOT / f"skills/{s}/SKILL.md").exists() or s in SEEDS


def fermeture() -> dict:
    seen, front = set(), list(SEEDS) + list(SUPPLEMENT_NORMATIF)
    liens = {}
    while front:
        s = front.pop()
        if s in seen:
            continue
        seen.add(s)
        ds = [d for d in (deps_frontmatter(s) + deps_kb(s))
              if d and existe_skill(d)]
        liens[s] = sorted(set(ds))
        front.extend(liens[s])
    return {"skills": sorted(seen), "liens": liens}


def taille(paths) -> int:
    n = 0
    for p in paths:
        if p.is_file():
            n += p.stat().st_size
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and ".next" not in f.parts and "__pycache__" not in f.parts:
                    n += f.stat().st_size
    return n


def arbre_complet():
    excl = {"(exclude).next"}
    return [ROOT / "skills", ROOT / "scripts", ROOT / "download", ROOT / "worklog.md"]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--manifest"
    cl = fermeture()
    manifest = {
        "profil": "MINIMALE",
        "defaut": "COMPLET (pipeline §2 inchangé)",
        "seeds": SEEDS,
        "fermeture_skills": cl["skills"],
        "liens_depends": cl["liens"],
        "agents": AGENTS_OBLIGATOIRES,
        "supplement_normatif_2bis": SUPPLEMENT_NORMATIF,
        "registre": "skills/KNOWLEDGE.md",
        "outillage": "scripts/ (complet — arbitres, certification, G-RES, gardes)",
        "hors_fermeture": "corpus @mon-ecosysteme/ complet + archive d'intégrité (toujours complets, v2.2)",
    }
    empreinte = hashlib.sha256(json.dumps(cl, sort_keys=True).encode()).hexdigest()[:16]
    manifest["empreinte_fermeture"] = empreinte

    # gains : arbre complet (hors .next, __pycache__, .git) vs fermeture
    t_all = sum(f.stat().st_size for f in (ROOT / "skills").rglob("*")
                if f.is_file() and ".next" not in f.parts and "__pycache__" not in f.parts)
    t_all += sum(f.stat().st_size for f in (ROOT / "scripts").rglob("*") if f.is_file())
    t_mini = sum((ROOT / f).stat().st_size for f in AGENTS_OBLIGATOIRES
                 if (ROOT / f).is_file())
    t_mini += (ROOT / "skills/KNOWLEDGE.md").stat().st_size
    t_mini += sum(f.stat().st_size for f in (ROOT / "scripts").rglob("*") if f.is_file())
    for s in cl["skills"]:
        d = ROOT / f"skills/{s}"
        if d.is_dir():
            t_mini += sum(f.stat().st_size for f in d.rglob("*")
                          if f.is_file() and "__pycache__" not in f.parts)
    manifest["gain"] = {"taille_skills_scripts_complete_mo": round(t_all / 1e6, 2),
                        "taille_minimale_mo": round(t_mini / 1e6, 2),
                        "gain_mo": round((t_all - t_mini) / 1e6, 2),
                        "gain_pct": round(100 * (t_all - t_mini) / max(1, t_all), 1)}

    out = ROOT / "scripts/install-profile.json"
    prev = json.loads(out.read_text()) if out.exists() else None
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fermeture MINIMALE : {len(cl['skills'])} skills — empreinte {empreinte}"
          f"{' (identique au précédent : idempotent)' if prev and prev.get('empreinte_fermeture') == empreinte else ''}")
    print(f"Skills : {', '.join(cl['skills'])}")
    print(f"Gain   : {manifest['gain']['gain_mo']} Mo ({manifest['gain']['gain_pct']} %) — "
          f"{manifest['gain']['taille_skills_scripts_complete_mo']} → {manifest['gain']['taille_minimale_mo']} Mo")

    if mode == "--apply":
        if MINI.exists():
            shutil.rmtree(MINI)
        MINI.mkdir(parents=True)
        for rel in AGENTS_OBLIGATOIRES:
            dst = MINI / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        shutil.copy2(KB, MINI / "skills/KNOWLEDGE.md")
        shutil.copytree(ROOT / "scripts", MINI / "scripts",
                        ignore=shutil.ignore_patterns("__pycache__", "*.json"),
                        dirs_exist_ok=True)
        for s in cl["skills"]:
            d = ROOT / f"skills/{s}"
            if d.is_dir():
                shutil.copytree(d, MINI / f"skills/{s}",
                                ignore=shutil.ignore_patterns("__pycache__"),
                                dirs_exist_ok=True)
        shutil.copy2(ROOT / "worklog.md", MINI / "worklog.md")
        print(f"Arbre élagué matérialisé : {MINI}")
    sys.exit(0)


if __name__ == "__main__":
    main()
