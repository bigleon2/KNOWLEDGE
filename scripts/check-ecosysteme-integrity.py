#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Intégrité de l'écosystème Knowledge installé dans ce projet.

Recalibré Architecture v2.0 (corrige-ecosysteme, session B8) ; re-calibré B13-r5
(gen-plan v3.16.0, knowledge-observer 13e entrée, corpus 19 fichiers) ;
re-calibré B13-r6 (N25 : script-creator + script-reviewer au registre — ECO_SKILLS 15,
check 5, archive homologues v2.1 ; N27 : audit-provenance — ECO_SKILLS 16 ;
N28 : gen-plan v3.17.0 — PM v3.17.0 assemblé 1362 L, corpus 20 fichiers) ;
re-calibré 2026-10-02 (montée gen-plan v3.17.1 — propagation renommage
prompt-engineering : PM v3.17.1 assemblé, corpus 22 fichiers, SYNC_MAP 12) ;
re-calibré 2026-10-02 (fusion installateurs PM-INSTALL v1.1.0 — directive
source d'installation unique : INSTALL-ECOSYSTEME.md supprimé, miroir
skills/_prompts-maitres/ supprimé (exécution décision d'architecture v2.0),
corpus 21 fichiers, SYNC_MAP 11) ; le miroir
skills/_prompts-maitres/ est SUPPRIMÉ par décision d'architecture (KB §Décisions)
— sa vérification est remplacée par le round-trip de l'archive
download/mon-ecosysteme_archive.zip (véhicule d'intégrité v2.0) ;
re-calibré 2026-10-02 (montée gen-plan v3.17.2 — déclencheur verbatim
« intègre dans le plan d'actions » + correction E1 → PM-INSTALL v1.1.0 :
PM v3.17.2 assemblé, corpus 22 fichiers, SYNC_MAP 12) ;
re-calibré 2026-10-02 (directive « prompt ultra maître » — orchestrateur léger
généré idempotent : PROMPT-ULTRA-MAITRE-ORCHESTRATION.md ajouté au corpus via
scripts/gen-ultra-maitre.py — dérivation dynamique KO-L003, idempotence ×2
prouvée, corpus 23 fichiers, SYNC_MAP 13) ;
re-calibré 2026-10-02 (Task 14, déduplication — décision d'architecture v2.2 :
canal de fichiers download/ SUPPRIMÉ, les 14 fichiers corpus répliqués dans
download/ sont effacés, sync-download.py retiré — le check 3 devient la garde
anti-doublons : AUCUN fichier du corpus ne doit exister en copie dans download/
(l'archive d'intégrité v2.2 est l'unique voie de diffusion) ; corpus 24 fichiers
avec le clone -f, garde calibrée sur le listing réel du corpus) ;
re-calibré 2026-10-02 (Task 16, suggestions (a)/(b) — résorption F1/F2/F4 :
ECO_SKILLS 21 → 26 (5 skills famille inscrits au registre KB), CORPUS_ATTENDU
24 → 26 (PMs CORRECT-WORK v2.6.0/v2.7.0 matérialisés au corpus, méthode B1,
provenance tracée), check 5 « 26 entrées KB versionnées » ; reconstitué Task 17
session suivante — couche Task 16 récupérée via l'archive certifiée de la
discussion partagée, round-trip 26/26 byte-identique).

Vérifications (pipeline PM-INSTALL étapes 1-2, 8 — périmètre v1.3.0) :
  1. SHA-256 des fichiers du corpus canonique skills/@mon-ecosysteme/
  2. Round-trip byte-identité archive download/mon-ecosysteme_archive.zip ↔ corpus + piliers (v2.3)
  3. Garde anti-doublons download/ (décision v2.2 — 0 fichier du corpus en copie)
  4. Structure des 26 skills écosystème installés (21 + 5 skills famille Task 16)
  5. Cohérence versions SKILL.md ↔ registre KNOWLEDGE.md (26 entrées versionnées
     + section « Décisions d'architecture »)

Usage :
    python3 scripts/check-ecosysteme-integrity.py            # vérification + manifeste
    python3 scripts/check-ecosysteme-integrity.py --check    # vérification seule
"""

import hashlib
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE_DIR, "skills", "@mon-ecosysteme")
ARCHIVE = os.path.join(BASE_DIR, "download", "mon-ecosysteme_archive.zip")
DOWNLOAD = os.path.join(BASE_DIR, "download")
SKILLS = os.path.join(BASE_DIR, "skills")
KB = os.path.join(SKILLS, "KNOWLEDGE.md")
MANIFEST = os.path.join(BASE_DIR, "scripts", "ecosysteme-integrity.json")

ECO_SKILLS = {
    "gen-plan": "3.26.0",  # KO-L004 (session web-f90062ce, 2026-10-24) : leçons vérité source PM INSTALL (dégradation gracieuse philosophie #4 + règle d'or n°5 anti-aspirant) ; précédent SG7.4 Task B2 : re-matérialisation structure hiérarchique ; précédent Task 26 : parallélisation par défaut
    "knowledge-observer": "1.0.0",
    "correct-work": "2.8.0",
    "clone-chat": "2.0.2",
    "skills-inventory": "1.1.0",
    "skill-creator": "1.1.0",
    "agent-creator": "2.3.0",  # Task 22 (2026-10-23) : DÉRIVE CRITIQUE résorbée — SKILL.md re-écrit comme VRAIE fabrique d'agents (workflow F1-F5), .agent ré-écrit (capacites A2A), read_when réparé
    "script-creator": "1.1.0",
    "script-reviewer": "1.0.0",
    "audit-provenance": "1.1.0",
    "prompt-engineering": "2.3.1",
    "context-engineering": "1.2.1",
    "loop-engineering": "1.2.1",
    "graph-engineering": "1.1.1",
    "harness-engineering": "1.2.1",
    "script-mon-ecosysteme-infrastructure": "1.1.0",
    "audio-metadata": "1.1.0",
    "cpp-analysis": "1.1.0",
    "pdf-llm": "1.0.0",
    "resource-monitor": "1.1.1",
    "version-management": "1.2.0",
    "skill-finder-cn": "1.0.0",  # Task 23 : fallback §1.16 inscrit au registre
    # Skills famille (Task 16, suggestion (a) — inscription au registre, résorption F1)
    "autonomous-agent": "1.2.1",
    "correct-py": "1.1.0",
    "fleet-engineering": "1.1.1",  # KO-L004 (session web-b4d7dd19, 2026-10-11) : read_when + dependencies gen-plan — bump PATCH cascade n°54
    "memory-engineering": "1.2.1",  # KO-L004 (session web-b4d7dd19, 2026-10-11) : read_when + dependencies gen-plan — bump PATCH cascade n°54 (Task 18 : Description Optimization conservée)
    "spec-driven-development": "1.1.1",
    "refactoring-engineering": "1.1.1",  # n°55 — Task 9 (2026-10-12) : Description Optimization A2 (dérive voie M résorbée, re-mesure 7/7) ; Task 8 : seule discipline de refactoring, outil refactoring-test ; Task 12 : recalibrage doc (§5 baseline MESURÉE 7/7, plancher ref-test >=1.0.1)
    "refactor-guard": "1.8.1",
    "alias-eco": "1.2.0",  # KO-L004 Task 25bis/25ter (2026-10-23) : Description Optimization v1.1.0 + grammaire B --trigger v1.2.0 ; créé Task 18 (registre d'alias $<ALIAS> — délégation correct-work mode PROJET),  # Task 8 (fusion discussion 468a4c26) : garde-fous de refactoring — lignée externe v1.7.0, base hôte v1.2.0 portée
    "cahier-des-charges": "1.0.0",  # KO-L004 (SG7.4 Task B2, session web-f90062ce, 2026-10-24) : entrée KB restaurée — forme publiée e9a68a1 sans entrée KB (trou de synchronisation analyse B2 résorbé) ; créé v1.0.0 directive propriétaire 2026-10-23
    "agent-prompt-engineering": "1.0.1",  # KO-L004 (SG7.4 Task B2, session web-f90062ce, 2026-10-24) : entrée KB créée — forme au dépôt depuis e9a68a1 sans entrée KB (trou de synchronisation analyse B2 résorbé) ; matérialisé 2026-09-06
    "fullstack-dev": "1.0.0",  # Task 8 (fusion discussion 468a4c26 Task 27 externe) : inscrit au registre — précédent vue-upload
    "refactoring-test": "1.1.1",  # Task 8 (session web-b4d7dd19, 2026-10-12) : OUTIL de la discipline n°55 (non discipline — correction directive propriétaire) ; Task 12 : §5 baseline MESURÉE 7/7
    "vue-upload": "1.3.0",  # KO-L004 (session web-b93f42fa, 2026-10-09) : KB=registre fait foi (## vue-upload v1.3.0) — occurrence L004 résorbée, arbitre dynamisé
    "dessin-technique": "1.1.1",
    "iphone18": "1.1.0",  # Task 48 (session web-38713acd) : bump v1.1.0 extension 1944 (chemin argentique N&B années 1930-1950) ; création v1.0.0 Task 45 (R18 ouverture variable, PA-TEST-001 QC 12/12)
    "iphone19": "0.11.0",  # Task 48 (session web-38713acd) : bump v0.11.0 extension 1944 (chemin argentique N&B années 1930-1950) ; v0.10.0 pixel binning R19 (frandroid 27/03/2026) ; création v0.9.0 Task 47 (migration ANTICIPÉE)
    "iphone17": "1.1.0",  # Task 48 (session web-38713acd) : bump v1.1.0 extension 1944 (chemin argentique N&B années 1930-1950) ; création v1.0.0 Task 45 (R1-R17 d'époque, PM v2.0 scellé @historique/photos/)  # Task 12 (2026-10-18) : bump PATCH v1.1.1 — corrections findings Task 11 (ACF par latitude + garde anti-fallacieux + trou-ness) ; Task 10 : bump v1.1.0 — F4 filetage + F5 profondeur, evals T5/T6 (recalibrage KO-L004 ; création Task 8 2026-10-17, réinscription post-wipes)
}
# Convention KB_ONLY_VERSION levée (corrige-ecosysteme G-bis) : skill-creator
# porte désormais sa version dans le frontmatter (v1.0.0) comme les autres.
KB_ONLY_VERSION = set()
METIER_SKILLS = []  # P-H (2026-10-02) : les ex-métier sont versionnés et au registre — check 4bis vidé
# Recalibrage F5 (Task 8, session web-43f5b4bd, 2026-10-17) : archive v2.3 étendue aux
# piliers — l'archive embarque, sous le préfixe piliers/, les 6 fichiers critiques du
# profil (2 SKILL.md familles PM, registre KB, orchestrateur de certification, arbitre
# d'intégrité, réinstallateur) afin que la restauration autonome couvre suppression ET
# corruption sur ce périmètre ; le round-trip vérifie leur byte-identité (compatibilité
# ascendante : une archive v2.2 sans entrées piliers/ reste conforme, n_pil_ko = 0).
PILIERS_ARCHIVE = {
    "piliers/skills/gen-plan/SKILL.md": os.path.join(SKILLS, "gen-plan", "SKILL.md"),
    "piliers/skills/correct-work/SKILL.md": os.path.join(SKILLS, "correct-work", "SKILL.md"),
    "piliers/skills/KNOWLEDGE.md": KB,
    "piliers/scripts/certification-complete.py": os.path.join(BASE_DIR, "scripts", "certification-complete.py"),
    "piliers/scripts/check-ecosysteme-integrity.py": os.path.join(BASE_DIR, "scripts", "check-ecosysteme-integrity.py"),
    "piliers/scripts/install-ecosysteme-local.sh": os.path.join(BASE_DIR, "scripts", "install-ecosysteme-local.sh"),
}
# [N14-c] SYNC_MAP — HISTORIQUE : bloc supprimé Task 14 (décision v2.2, déduplication) —
# le canal de fichiers download/ n'existe plus ; le check 3 applique la garde
# anti-doublons sur le listing RÉEL du corpus (dérivation dynamique — KO-L003).
# CORPUS_ATTENDU — invariant canonique du corpus (dérivation L003) [N28]
# Recalibrage L004 (Task 56) : 20 → 21 — ajout clone -f (directive utilisateur
# « push le clone dans @mon-ecosysteme/ » ; miroir + archive alignés).
# Recalibrage L004 (Task 16, suggestion (b)) : 24 → 26 — PMs CORRECT-WORK
# v2.6.0/v2.7.0 matérialisés au corpus (méthode B1, provenance tracée).
# Recalibrage L004 (session web-b93f42fa, 2026-10-09) : 26 → 28 — corpus réel certifié
# (28 fichiers à HEAD 3eebe65 ; PMs GEN-PLAN v3.19.0/v3.20.0 recréés,
# KB Tasks 39-40) — arbitre dynamisé, jamais la réalité (KO-L003).
# Recalibrage Task 15 (session web-b93f42fa, 2026-10-10) : 28 → 27 — suppression
# propriétaire d72226a (clone-discussion-2026-09-27-…-b13-r7-f.md, UI web) —
# corpus réel certifié 27 fichiers, re-scellement archive aligné (F2 retrait
# sanctionné D002, plan-task15-decisions-restantes.md).
# Recalibrage Task 16 (session web-b93f42fa, 2026-10-11) : 27 → 8 — déduplication
# des PMs (directive propriétaire « ne garder que la dernière version ») : 19 PMs
# historiques déplacés git mv vers skills/@historique/prompts-maitres/ (byte-identité
# SHA-256 scellée contre blobs b36f177, dossier @historique/) — corpus = 3 PMs
# sources (GEN-PLAN v3.21.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0) + socle
# (SHARED, INSTALL, ULTRA, README, SYNC-CONTEXT), re-scellement archive aligné (F2).
# Recalibrage Task 9 (session web-b4d7dd19, 2026-10-12) : 8 → 9 — PM REFACTOR-GUARD
# v1.7.0 au corpus (décision D009 — 4e famille, bootstrap canonique).
CORPUS_ATTENDU = 9

results = []


def check(name, passed, detail=""):
    results.append((name, bool(passed), detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}{(' — ' + detail) if detail else ''}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    write_manifest = "--check" not in sys.argv
    manifest = {"corpus": {}, "archive": {}, "download": {}, "skills": {}}

    print("=== 1. Corpus canonique @mon-ecosysteme (SHA-256) ===")
    corpus_files = sorted(os.listdir(CORPUS)) if os.path.isdir(CORPUS) else []
    check(f"{CORPUS_ATTENDU} fichiers présents (Architecture v2.0 — N27, recalibré Task 16 b36f177: dédup PMs → @historique)", len(corpus_files) == CORPUS_ATTENDU,
          f"{len(corpus_files)} fichiers")
    for fname in corpus_files:
        digest = sha256(os.path.join(CORPUS, fname))
        manifest["corpus"][fname] = digest

    print("\n=== 2. Archive round-trip (véhicule d'intégrité v2.3 — corpus + piliers) ===")
    ok, n_ident, n_homologues, n_pil, n_pil_ko = os.path.isfile(ARCHIVE), 0, 0, 0, 0
    if ok:
        import zipfile
        with zipfile.ZipFile(ARCHIVE) as z:
            znames = [n for n in z.namelist() if not n.endswith("/")]
            for n in znames:
                if n in PILIERS_ARCHIVE:
                    # F5 (Task 8, 2026-10-17) : piliers scellés — byte-identité exigée
                    cp = PILIERS_ARCHIVE[n]
                    if os.path.isfile(cp) and hashlib.sha256(z.read(n)).hexdigest() == sha256(cp):
                        manifest["archive"][n] = sha256(cp)
                        n_pil += 1
                    else:
                        n_pil_ko += 1
                    continue
                rel = n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n
                cp = os.path.join(CORPUS, rel)
                if os.path.isfile(cp) and hashlib.sha256(z.read(n)).hexdigest() == sha256(cp):
                    manifest["archive"][rel] = sha256(cp)
                    n_ident += 1
                elif rel.startswith("homologues/"):
                    n_homologues += 1
            # v2.1 (N26, recalibrage L004) : corpus ⊆ archive byte-identique +
            # extras uniquement sous homologues/ (famille créateur/relecture).
            # v2.3 (F5, Task 8) : + piliers scellés vérifiés byte-identiques.
            extras = [n for n in znames
                      if n not in PILIERS_ARCHIVE
                      and (n.split("@mon-ecosysteme/")[-1]
                           if "@mon-ecosysteme/" in n else n) not in corpus_files]
            ok = (n_ident == len(corpus_files)
                  and n_pil_ko == 0
                  and all(e.startswith("homologues/") for e in extras)
                  and n_ident + n_pil + n_pil_ko + len(extras) == len(znames))
    check("Archive byte-identique au corpus + piliers (v2.3)", ok,
          f"corpus {n_ident}/{len(corpus_files)} · piliers {n_pil}/{len(PILIERS_ARCHIVE)} ({n_pil_ko} divergents) · {n_homologues} homologues")

    print("\n=== 3. Garde anti-doublons download/ (décision v2.2) ===")
    n_dup = 0
    for fname in sorted(corpus_files):
        d = os.path.join(DOWNLOAD, fname)
        if os.path.isfile(d):
            # Calibration Task 18 (2026-10-23, KO-L003) : détection par CONTENU —
            # un homonyme de contenu différent (ex. README.md du canal plateforme
            # hôte) n'est PAS une copie du corpus ; seule la copie byte-identique
            # (ou quasi) est un doublon sanctionné (décision v2.2).
            if sha256(d) == sha256(os.path.join(CORPUS, fname)):
                n_dup += 1
                check(f"doublon {fname}", False,
                      "copie du corpus dans download/ — à supprimer (déduplication v2.2)")
            else:
                print(f"  [NOTE] {fname} : homonyme de contenu différent dans download/ (canal partagé) — non compté")
    if n_dup == 0:
        check(f"download/ sans doublon du corpus ({len(corpus_files)} fichiers corpus absents)", True)
    if os.path.isfile(ARCHIVE):
        manifest["download"]["mon-ecosysteme_archive.zip"] = sha256(ARCHIVE)

    print("\n=== 4. Skills écosystème installés ===")
    for skill, expected_ver in ECO_SKILLS.items():
        sp = os.path.join(SKILLS, skill, "SKILL.md")
        if not os.path.isfile(sp):
            check(f"{skill}", False, "SKILL.md manquant")
            continue
        with open(sp, encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"^version:\s*[\"']?([\d.]+)", content, re.MULTILINE)
        ver = m.group(1) if m else None
        manifest["skills"][skill] = {"version": ver or "KB", "sha256": sha256(sp)}
        check(f"{skill} v{ver}", ver == expected_ver, f"attendu v{expected_ver}")

    print("\n=== 4bis. Skills métier installés ===")
    for skill in METIER_SKILLS:
        sp = os.path.join(SKILLS, skill, "SKILL.md")
        check(f"{skill}", os.path.isfile(sp))

    print("\n=== 5. Cohérence registre KNOWLEDGE.md ===")
    if os.path.isfile(KB):
        with open(KB, encoding="utf-8") as f:
            kb = f.read()
        entries = re.findall(r"^## ([\w-]+) v([\d.]+)", kb, re.MULTILINE)
        has_decisions = "## Décisions d'architecture" in kb
        # Dynamisé KO-L004 (Task 23) : l'attendu = len(ECO_SKILLS), jamais un chiffre figé
        check(f"{len(ECO_SKILLS)} entrées KB versionnées + Décisions d'architecture",
              len(entries) == len(ECO_SKILLS) and has_decisions,
              f"{len(entries)} entrées versionnées (attendu {len(ECO_SKILLS)}), Décisions={'oui' if has_decisions else 'non'}")
        for skill, expected_ver in ECO_SKILLS.items():
            match = [e for e in entries if e[0] == skill]
            check(f"KB {skill}", bool(match) and match[0][1] == expected_ver,
                  f"KB={match[0][1] if match else 'absent'} / attendu={expected_ver}")
    else:
        check("Registre KB", False, "KNOWLEDGE.md manquant")

    n_pass = sum(1 for _, p, _ in results if p)
    n_fail = len(results) - n_pass
    print(f"\n=== RESUME : {n_pass}/{len(results)} PASS, {n_fail} FAIL ===")

    if write_manifest and n_fail == 0:
        with open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Manifeste écrit : {MANIFEST}")
    elif write_manifest:
        print("Manifeste NON écrit (échecs détectés)")

    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
