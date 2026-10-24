#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Task 45 — correct-work(groupe C, mode CIBLE) : vérification des skills iphone18/iphone17 générés.
Cibles : skills/iphone18/, skills/iphone17/, entrées KB, recalibrage KO-L004.
Critères : D004 (projection VERBATIM du PM source, lignage byte-identique), D009 (§1→§13
opérationnels, périmètre d'époque honnête), D005 (KB 35, cross-refs bidirectionnelles),
invariant R2 (PMs @photos jamais édités)."""
import hashlib
import json
import re
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
PHOTOS = HOST / "tmp" / "KNOWLEDGE-repo" / "skills" / "@photos"
SKILLS = HOST / "skills"
KB = (SKILLS / "KNOWLEDGE.md").read_text(encoding="utf-8")
ARBITRE = (HOST / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")

# SHA-256 attendus (constatés Groupe B — source : @photos @ 1020518, identiques Task 44)
SHA_ATTENDUS = {
    "iphone18-photos.md": "2887e9e3e8cbb5b0",
    "iphone17-photos.md": "6b2846fdda56d32a",
    "iphone-photos-migration.md": "3a5e95d63979b70b",
}
SECTIONS = ["## PROMPT MAÎTRE", "## §0 — RÔLE & MISSION", "## §1 — ÉTAPE 1", "## §2 — ÉTAPE 2",
            "## §3 — ÉTAPE 3", "## §4 — ÉTAPE 4", "## §5 — ÉTAPE 5", "## §6 — VARIATIONS DE RENDU",
            "## §7 — INTÉGRATION OPÉRATIONNELLE", "## §8 — RAPPORT FINAL", "## §9 — MODE INTERACTION",
            "## §10 — MODE SÉRIE", "## §11 — AUTO-AUDIT", "## §12 — LIVRABLES", "## §13 — INTERFACE DE COMMANDES"]

results = []
def check(nom, ok, detail=""):
    results.append((nom, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {nom}" + (f" — {detail}" if detail else ""))

def corps_pm(pm_path):
    lines = Path(pm_path).read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("## PROMPT MAÎTRE"):
            return "\n".join(lines[i:]) + "\n"
    return None

print("=== A. R2 — PMs @photos intacts (byte-identité vs @ 1020518) ===")
for f, attendu in SHA_ATTENDUS.items():
    sha = hashlib.sha256((PHOTOS / f).read_bytes()).hexdigest()[:16]
    check(f"{f} SHA-256 {attendu}…", sha == attendu, sha)

for nom, pm_file in [("iphone18", "iphone18-photos.md"), ("iphone17", "iphone17-photos.md")]:
    print(f"\n=== B-F. Skill {nom} ===")
    sm = SKILLS / nom / "SKILL.md"
    text = sm.read_text(encoding="utf-8")
    # B — projection VERBATIM (corps embarqué == corps PM source, octet par octet)
    corps = corps_pm(sm)
    src = corps_pm(PHOTOS / pm_file)
    check("corps §PROMPT MAÎTRE→§13 VERBATIM (byte-identique au PM source)",
          corps is not None and corps == src,
          f"{len(corps.splitlines()) if corps else 0} lignes embarquées")
    # C — frontmatter
    fm = text.split("---", 2)[1]
    for champ in ["name: " + nom, "version: 1.0.0", "category: metier", "language: fr",
                  "description:", "dependencies:", "read_when:"]:
        check(f"frontmatter « {champ.split(':')[0]} »", champ in fm)
    deps = re.findall(r"skill: ([A-Za-z0-9-]+)", fm)
    check("dépendances (skill-creator, VLM, image-edit)", set(deps) == {"skill-creator", "VLM", "image-edit"}, ", ".join(deps))
    # D — sections opérationnelles D009
    manquantes = [s for s in SECTIONS if s not in text]
    check("§PROMPT MAÎTRE + §0→§13 présents (D009)", not manquantes, "manquantes : " + ", ".join(manquantes) if manquantes else "15/15")
    # E — Contexte Système + lignage
    check("§0 Contexte Système (SHARED v1.7.7)", "## §0 — Contexte Système (SHARED v1.7.7)" in text and "Écosystème Knowledge" in text)
    check("note de lignage (PM source + R2 byte-identité)", "Lignage — projection skill ← prompt maître source" in text and "byte-identique, jamais édité (R2)" in text and pm_file in text)
    # D009 — périmètre d'époque honnête
    if nom == "iphone18":
        check("périmètre d'époque (COURANT, R18, iphone18_max)", "R18" in text and "iphone18_max" in text)
    else:
        check("périmètre d'époque (ARCHIVÉ, supersédé iphone18)", "ARCHIVÉ" in text and "supersédé" in text and "R17" in text)
    # F — evals
    ev = json.loads((sm.parent / "evals" / "evals.json").read_text(encoding="utf-8"))
    check("evals.json (schéma écosystème, 6 cas S1/S2)",
          ev["skill"] == nom and ev["version"] == "1.0.0" and len(ev["evals"]) == 6
          and all(set(e) >= {"id", "description", "commande", "attendu", "priorite"} for e in ev["evals"])
          and {e["priorite"] for e in ev["evals"]} == {"S1", "S2"},
          f"{sum(1 for e in ev['evals'] if e['priorite']=='S1')} S1 / {sum(1 for e in ev['evals'] if e['priorite']=='S2')} S2")
    tg = json.loads((sm.parent / "evals" / "trigger_evals.json").read_text(encoding="utf-8"))
    pos = sum(1 for t in tg if t["should_trigger"]); neg = len(tg) - pos
    check("trigger_evals.json (8 cas, 2 polarités)", isinstance(tg, list) and len(tg) == 8 and pos == 6 and neg == 2,
          f"{pos} positifs / {neg} négatifs")
    check("script contournement scripts/editer-image.mjs", (sm.parent / "scripts" / "editer-image.mjs").exists())

print("\n=== G. KB — 35 entrées + cross-refs bidirectionnelles (D005) ===")
n = len(re.findall(r"^## [a-z0-9-]+ v\d+\.\d+\.\d+\s*$", KB, re.M))
check("registre 33 → 35 entrées", n == 35, f"{n} entrées")
for nom in ("iphone18", "iphone17"):
    m = re.search(rf"^## {nom} v1\.0\.0\s*$", KB, re.M)
    blk = KB[m.end():KB.find("\n## ", m.end())] if m else ""
    champs = sum(1 for c in ["**Category**", "**Description**", "**Dépend de**", "**Utilisé par**", "**Dernière calibration**", "**Statut**"] if c in blk)
    check(f"entrée KB {nom} v1.0.0 (6 champs)", m is not None and champs == 6, f"{champs}/6 champs")
check("cross-ref skill-creator « Utilisé par » += iphone18, iphone17",
      "iphone18 v1.0.0 (conventions structurelles — projection PM → SKILL.md)" in KB and "iphone17 v1.0.0 (idem)" in KB)
check("KO-L004 — ECO_SKILLS recalibré (iphone18/iphone17 1.0.0)",
      '"iphone18": "1.0.0"' in ARBITRE and '"iphone17": "1.0.0"' in ARBITRE)

print("\n═══════ RÉSUMÉ CIBLE ═══════")
ok = sum(1 for _, o, _ in results if o)
print(f"{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
