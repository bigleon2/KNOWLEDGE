#!/usr/bin/env python3
"""task82-inventaire.py — Inventaire mécanique écosystème pour l'analyse conversions (Task 82 G1).

Collecte (KO-L003 — état réel du disque, zéro étiquette) :
  - 68 skills racine : version frontmatter, poids SKILL.md, scripts/, references/, evals/,
    .agent, data/, sections #, mentions worklog (usage réel), présence KB, présence ULTRA §3,
    marqueurs tandem/projection-curée
  - agents .agent réels + gabarits
  - corpus @mon-ecosysteme + @photos + @Bibliotheque (poids)
  - historiques par skill, KB, worklog (poids)
Sortie : scripts/task82-inventaire.json + synthèse stdout triée poids/usage.
"""
import json
import os
import re
import sys

RACINE = "/home/z/my-project"
SKILLS = os.path.join(RACINE, "skills")
WORKLOG = os.path.join(RACINE, "worklog.md")
KB = os.path.join(SKILLS, "KNOWLEDGE.md")
ULTRA = os.path.join(SKILLS, "@mon-ecosysteme", "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md")

EXCLUS = {"@Bibliotheque-skills-Multi-IA", "@GHORG-ecosysteme", "@historique",
          "@mon-ecosysteme", "@photos", "@PM-SKILLS"}


def taille(p):
    return os.path.getsize(p) if os.path.isfile(p) else 0


def compte_fichiers(d):
    if not os.path.isdir(d):
        return 0
    return sum(len([f for f in fs if os.path.isfile(os.path.join(r, f))])
               for r, _, fs in os.walk(d))


def main():
    with open(WORKLOG, encoding="utf-8") as f:
        worklog_txt = f.read()
    with open(KB, encoding="utf-8") as f:
        kb_txt = f.read()
    with open(ULTRA, encoding="utf-8") as f:
        ultra_txt = f.read()

    skills = []
    for nom in sorted(os.listdir(SKILLS)):
        chemin = os.path.join(SKILLS, nom)
        if not os.path.isdir(chemin) or nom in EXCLUS or nom.startswith("."):
            continue
        p_md = os.path.join(chemin, "SKILL.md")
        if not os.path.isfile(p_md):
            continue
        with open(p_md, encoding="utf-8") as f:
            corps = f.read()
        m_v = re.search(r"^version:\s*[\"']?([\d.]+)", corps, re.MULTILINE)
        m_d = re.search(r"^description:\s*[\"']?(.{0,110})", corps, re.MULTILINE)
        agents = sorted(f for f in os.listdir(chemin) if f.endswith(".agent"))
        skills.append({
            "skill": nom,
            "version": m_v.group(1) if m_v else "?",
            "octets": len(corps.encode("utf-8")),
            "kio": round(len(corps.encode("utf-8")) / 1024, 1),
            "lignes": corps.count("\n"),
            "sections": len(re.findall(r"^#{2,3} ", corps, re.MULTILINE)),
            "scripts": compte_fichiers(os.path.join(chemin, "scripts")),
            "references": compte_fichiers(os.path.join(chemin, "references")),
            "evals": compte_fichiers(os.path.join(chemin, "evals")),
            "agents": agents,
            "data": compte_fichiers(os.path.join(chemin, "data")),
            "description": (m_d.group(1) if m_d else "")[:105],
            "usage_worklog": len(re.findall(r"(?<![\w-])" + re.escape(nom) + r"(?![\w-])", worklog_txt)),
            "kb": bool(re.search(r"^## " + re.escape(nom) + r" v[\d.]+", kb_txt, re.MULTILINE)),
            "ultra_membre": bool(re.search(r"\|`" + re.escape(nom) + r"`\||\| `" + re.escape(nom) + r"` \|", ultra_txt)),
            "tandem_marqueur": "tandem" in corps.lower(),
            "proj_curée": "projection curée" in corps.lower() or "curée" in corps.lower(),
        })

    agents_tous = []
    for nom in sorted(os.listdir(SKILLS)):
        chemin = os.path.join(SKILLS, nom)
        if not os.path.isdir(chemin) or nom in EXCLUS:
            continue
        for f in sorted(os.listdir(chemin)):
            if f.endswith(".agent"):
                agents_tous.append({"fichier": f"skills/{nom}/{f}", "octets": taille(os.path.join(chemin, f))})

    corpus = {}
    for sous in ("@mon-ecosysteme", "@photos", "@Bibliotheque-skills-Multi-IA"):
        d = os.path.join(SKILLS, sous)
        corpus[sous] = [{"fichier": f, "octets": taille(os.path.join(d, f))}
                        for f in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, f))]

    hist = []
    dh = os.path.join(SKILLS, "@historique", "historiques-par-skill")
    if os.path.isdir(dh):
        hist = [{"fichier": f, "octets": taille(os.path.join(dh, f))}
                for f in sorted(os.listdir(dh)) if os.path.isfile(os.path.join(dh, f))]

    rapport = {
        "horodatage": "2026-11-09T04:10:00Z",
        "task": "Task 82 G1 — inventaire conversions",
        "nb_skills": len(skills),
        "skills": skills,
        "agents": agents_tous,
        "corpus": corpus,
        "historiques_par_skill": hist,
        "kb_octets": taille(KB),
        "worklog_octets": taille(WORKLOG),
        "ultra_octets": taille(ULTRA),
    }
    out = os.path.join(RACINE, "scripts", "task82-inventaire.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=1)

    print(f"SKILLS: {len(skills)}  |  agents .agent: {len(agents_tous)}  |  KB {taille(KB)} o  |  worklog {taille(WORKLOG)} o")
    print("\n=== TOP 18 PAR POIDS (écosystème) ===")
    for s in sorted(skills, key=lambda x: -x["octets"])[:18]:
        print(f"{s['octets']:>7} o  v{s['version']:<8} usage:{s['usage_worklog']:>4}  refs:{s['references']:>2} scr:{s['scripts']:>2} sec:{s['sections']:>3}  agent:{len(s['agents'])}  {s['skill']}")
    print("\n=== TOP 12 PAR USAGE WORKLOG ===")
    for s in sorted(skills, key=lambda x: -x["usage_worklog"])[:12]:
        print(f"usage:{s['usage_worklog']:>5}  {s['octets']:>7} o  v{s['version']:<8}  data:{s['data']} tandem:{s['tandem_marqueur']}  {s['skill']}")
    print("\n=== AGENTS ===")
    for a in agents_tous:
        print(f"{a['octets']:>7} o  {a['fichier']}")
    print("\n=== CORPUS @mon-ecosysteme ===")
    for c in corpus["@mon-ecosysteme"]:
        print(f"{c['octets']:>7} o  {c['fichier']}")
    print("\n=== CORPUS @photos ===")
    for c in corpus["@photos"]:
        print(f"{c['octets']:>7} o  {c['fichier']}")
    print("\n=== SKILLS AVEC data/ (État Long existant) ===")
    for s in skills:
        if s["data"]:
            print(f"  {s['skill']}: data/ {s['data']} fichier(s), {s['octets']} o, usage {s['usage_worklog']}")
    print("\n=== HISTORIQUES TOP 8 ===")
    for h in sorted(hist, key=lambda x: -x["octets"])[:8]:
        print(f"{h['octets']:>7} o  {h['fichier']}")
    print(f"\nJSON: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
