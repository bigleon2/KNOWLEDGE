#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""R7 — Spécialisation des agents par skills empaquetés réutilisables (Task 36, vague 2).
Construit mécaniquement la matrice agent × skill depuis le registre KB
(champs « Utilisé par » / « Dépend de ») — base de spécialisation des agents
(agent-creator). Read-only, idempotent, sortie JSON.
"""
import json, os, re, sys, time

KB = "/home/z/my-project/work_knowledge/skills/KNOWLEDGE.md"
OUT = "/home/z/my-project/work_knowledge/tmp/r7-matrice-agents-skills.json"

def main():
    with open(KB, encoding="utf-8") as f:
        txt = f.read()
    blocks = re.split(r"\n## ", txt)[1:]
    matrice, relations = {}, 0
    for b in blocks:
        m = re.match(r"([A-Za-z0-9_-]+) v([0-9.]+)", b)
        if not m:
            continue
        skill = m.group(1)
        up = re.search(r"\*\*Utilisé par\*\* : ([^\n]+)", b)
        if up:
            sans_paren = re.sub(r"\([^)]*\)", "", up.group(1))
            agents = [a.strip() for a in sans_paren.split(",") if a.strip()]
            for a in agents:
                if a in ("—", "-", "") or re.match(r"^v?\d", a) or ">=" in a:
                    continue
                matrice.setdefault(a, set()).add(skill)
                relations += 1
    agents_sorted = {a: sorted(s) for a, s in sorted(matrice.items())}
    out = {
        "regle": "R7 — les agents se spécialisent par skills empaquetés réutilisables (convention + registre KB, source de spécialisation agent-creator)",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "agents_references": len(agents_sorted),
        "relations_agent_skill": relations,
        "matrice": agents_sorted,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"R7 : {len(agents_sorted)} agents référencés, {relations} relations agent→skill "
          f"(top : {', '.join(list(agents_sorted)[:3])}…)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
