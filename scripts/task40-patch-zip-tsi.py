#!/usr/bin/env python3
"""Patch v1.1.0 de construire-zip-tsi.py — entrées zip à date figée (R6)."""
from pathlib import Path

P = Path("/home/z/my-project/work/knowledge-clone-fddbe94/construire-zip-tsi.py")
t = P.read_text(encoding="utf-8")

OLD_TITRE = '"""construire-zip-tsi.py — construit zip-tsi.zip (source de vérité portable).'
NEW_TITRE = (
    '"""construire-zip-tsi.py — construit zip-tsi.zip (source de vérité portable) v1.1.0.\n'
    "\n"
    "v1.1.0 (Task 40, correct-work G2) : entrées à date figée 1980-01-01 — le\n"
    "zip devient byte-identique au re-jeu indépendamment des mtime (R6). Le\n"
    "writestr horodatat le manifeste à l'heure courante : source de non-\n"
    "déterminisme attrapée par le correct-work Task 40 (re-jeus sha divergents\n"
    "masqués par la granularité 2 s du format zip).\n"
)

OLD_AJOUT = """            chemin = os.path.join(racine, f)
            relatif = os.path.join(
                prefixe, os.path.relpath(chemin, dossier))
            zf.write(chemin, relatif)
            n += 1
    return n"""
NEW_AJOUT = """            chemin = os.path.join(racine, f)
            relatif = os.path.join(
                prefixe, os.path.relpath(chemin, dossier))
            # entrées à date figée (1980-01-01) — zip déterministe
            # byte-identique au re-jeu, indépendant des mtime (R6)
            info = zipfile.ZipInfo(relatif, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, open(chemin, "rb").read())
            n += 1
    return n"""

OLD_MANIF = """        zf.writestr("zip-tsi/manifeste.json",
                    json.dumps(manifeste, ensure_ascii=False, indent=1))"""
NEW_MANIF = """        info = zipfile.ZipInfo("zip-tsi/manifeste.json",
                               date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, json.dumps(manifeste, ensure_ascii=False, indent=1))"""

OLD_AGENT = """        agent = os.path.join(RACINE_DEPOT, "tsi-agent.md")
        if os.path.isfile(agent):
            zf.write(agent, "zip-tsi/tsi-agent.md")
            compte += 1"""
NEW_AGENT = """        agent = os.path.join(RACINE_DEPOT, "tsi-agent.md")
        if os.path.isfile(agent):
            info = zipfile.ZipInfo("zip-tsi/tsi-agent.md",
                                   date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, open(agent, "rb").read())
            compte += 1"""

OLD_SKILLS = """            chemin = os.path.join(skills, nom, "SKILL.md")
            if os.path.isfile(chemin):
                zf.write(chemin, f"zip-tsi/manifestes-skills/{nom}-SKILL.md")
                compte += 1"""
NEW_SKILLS = """            chemin = os.path.join(skills, nom, "SKILL.md")
            if os.path.isfile(chemin):
                cible = f"zip-tsi/manifestes-skills/{nom}-SKILL.md"
                info = zipfile.ZipInfo(cible, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, open(chemin, "rb").read())
                compte += 1"""

for ancien, nouveau in [(OLD_TITRE, NEW_TITRE), (OLD_AJOUT, NEW_AJOUT),
                        (OLD_MANIF, NEW_MANIF), (OLD_AGENT, NEW_AGENT),
                        (OLD_SKILLS, NEW_SKILLS)]:
    assert ancien in t, f"introuvable : {ancien[:60]}…"
    t = t.replace(ancien, nouveau, 1)

P.write_text(t, encoding="utf-8")
print("construire-zip-tsi.py patché v1.1.0 (5 substitutions)")
