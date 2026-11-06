#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.23)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""
"""Task 47 — correctif miroir Task 46 (correct-work(groupe) G2, findings F-01..F-03).
1. KB : restaure le pilier KB certifié Task 46 (extrait de l'archive scellée hôte) puis
   ré-applique les 2 edits gen-plan v3.33.0 (en-tête + calibration) — écriture IDENTIQUE
   hôte et clone (le KB du clone était en retard : entrées TSI Task 46 absentes).
2. Arbitre pilier : bump pin "gen-plan": "3.32.0" -> "3.33.0" (commentaire KO-L004 Task 47)
   dans le checker HÔTE, puis copie hôte->clone (résorbe les pins TSI en retard du clone :
   tsi-architect 1.1.0->1.2.0, midi-doc-expert 1.1.0->1.2.0, analyse-doc-s4mk2 1.2.0->1.3.0).
3. Miroir hôte->clone des 3 skills TSI Task 46 + leurs @historique/historiques-par-skill.
Substitutions verrouillées count==1. Idempotent : NO-OP si KB hôte == KB cible.
"""
import hashlib
import shutil
import sys
import zipfile

HOST = "/home/z/my-project"
CLONE = HOST + "/work/KNOWLEDGE-b75a620"


def abandon(msg, code=1):
    print("[ABANDON] %s" % msg)
    sys.exit(code)


def lire(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def sub(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        abandon("motif [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, motif[:70]))
    return text.replace(motif, remplace)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    # --- 1. KB : pilier certifié Task 46 + edits gen-plan v3.33.0 ---
    arch = HOST + "/download/mon-ecosysteme_archive.zip"
    with zipfile.ZipFile(arch) as z:
        kb46 = z.read("piliers/skills/KNOWLEDGE.md").decode("utf-8")
    if "## analyse-doc-s4mk2 v1.3.0" not in kb46 or "## tsi-architect v1.2.0" not in kb46 \
            or "## midi-doc-expert v1.2.0" not in kb46:
        abandon("le pilier KB extrait n'est pas l'état Task 46 (versions TSI absentes)")
    kb = sub(kb46, "## gen-plan v3.32.0", "## gen-plan v3.33.0", 1, "en-tête KB gen-plan")
    ancienne = ("- **Dernière calibration** : montée v3.32.0 (2026-11-02, session web-6058b3ba — "
                "préalable propriétaire avant gen-plan :")
    nouvelle = (
        "- **Dernière calibration** : montée v3.33.0 (2026-11-04, session web-6058b3ba — "
        "gen-plan(step), directive propriétaire : règle d'or n°7 « mémoire complète de la "
        "discussion — relire les clones et sauvegardes en cas d'oubli dû à une coupure » + "
        "re-génération du plan en mode STEP) : §1.5 — insertion règle d'or n°7 après n°6 (le "
        "plan couvre TOUS les éléments de la discussion à traiter : directives verbatim, "
        "tâches antérieures, livrables, pendances ; oubli post-coupure → relecture des clones "
        "et sauvegardes AVANT génération/re-génération ; reprise E1-RES = relecture première "
        "+ état disque règle d'or n°5 ; couverture vérifiable — chaque élément recensé ∈ "
        "{tâche du plan, livrable certifié, pendance consignée}, absence = dérive E13) ; "
        "description frontmatter inchangée (non-régression triggers) ; cascade KO-L004 : "
        "PM v3.33.0 généré mécaniquement (delta verrouillé scripts/delta-genplan-v3330.json) "
        "+ SHARED v1.7.19 + PM-INSTALL v1.8.13 recalibrés ; PM v3.32.0 archivé @historique "
        "R4 ; pin arbitre ECO_SKILLS 3.33.0 ; propagation §0 v1.7.19 ; rescellement archive "
        "v2.3 ; replay arbitres ×2. Précédent — montée v3.32.0 (2026-11-02, session "
        "web-6058b3ba — préalable propriétaire avant gen-plan :"
    )
    kb = sub(kb, ancienne, nouvelle, 1, "calibration KB")

    # Idempotence : KB hôte déjà cible ?
    if lire(HOST + "/skills/KNOWLEDGE.md") == kb:
        print("[NO-OP] KB hôte déjà à l'état cible")
    else:
        for cible in (HOST + "/skills/KNOWLEDGE.md", CLONE + "/skills/KNOWLEDGE.md"):
            with open(cible, "w", encoding="utf-8") as f:
                f.write(kb)
        print("[OK] KB restauré (pilier Task 46 + gen-plan v3.33.0) — hôte + clone byte-identiques")

    # --- 2. Arbitre pilier : pin gen-plan 3.33.0 (hôte) puis copie -> clone ---
    chk_hote = HOST + "/scripts/check-ecosysteme-integrity.py"
    t = lire(chk_hote)
    if '"gen-plan": "3.33.0"' in t:
        print("[NO-OP] pin arbitre hôte déjà 3.33.0")
    else:
        t = sub(t, '"gen-plan": "3.32.0",  # KO-L004 (session web-6058b3ba, 2026-11-02',
                '"gen-plan": "3.33.0",  # KO-L004 (Task 47, session web-6058b3ba 2026-11-04 — '
                'règle d\'or n°7 mémoire complète de la discussion, cascade générateur '
                'PM v3.33.0/SHARED v1.7.19/PM-INSTALL v1.8.13) ; '
                'KO-L004 (session web-6058b3ba, 2026-11-02', 1, "pin gen-plan arbitre hôte")
        with open(chk_hote, "w", encoding="utf-8") as f:
            f.write(t)
        print("[OK] pin arbitre hôte : gen-plan 3.33.0")
    shutil.copy2(chk_hote, CLONE + "/scripts/check-ecosysteme-integrity.py")
    print("[OK] arbitre pilier copié hôte -> clone (pins TSI Task 46 résorbés au clone)")

    # --- 3. Miroir hôte -> clone : 3 skills TSI + historiques ---
    paires = [
        ("skills/analyse-doc-s4mk2/SKILL.md", 1, 3, 0),
        ("skills/tsi-architect/SKILL.md", 1, 2, 0),
        ("skills/midi-doc-expert/SKILL.md", 1, 2, 0),
        ("skills/@historique/historiques-par-skill/analyse-doc-s4mk2.md", 0, 0, 0),
        ("skills/@historique/historiques-par-skill/tsi-architect.md", 0, 0, 0),
        ("skills/@historique/historiques-par-skill/midi-doc-expert.md", 0, 0, 0),
    ]
    for rel, maj, min_, patch in paires:
        src = HOST + "/" + rel
        dst = CLONE + "/" + rel
        shutil.copy2(src, dst)
        print("[OK] miroir hôte->clone : %s (sha %s…)" % (rel, sha(dst)[:12]))

    # --- Vérifications ---
    assert sha(HOST + "/skills/KNOWLEDGE.md") == sha(CLONE + "/skills/KNOWLEDGE.md")
    assert sha(chk_hote) == sha(CLONE + "/scripts/check-ecosysteme-integrity.py")
    for rel, _, _, _ in paires:
        assert sha(HOST + "/" + rel) == sha(CLONE + "/" + rel), rel
    print("Vérifications : KB + arbitre + %d miroirs byte-identiques hôte<->clone" % len(paires))
    return 0


if __name__ == "__main__":
    sys.exit(main())
