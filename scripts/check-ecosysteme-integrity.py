#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
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
corpus 21 fichiers, SYNC_MAP 11) : le miroir
skills/_prompts-maitres/ est SUPPRIMÉ par décision d'architecture (KB §Décisions)
— sa vérification est remplacée par le round-trip de l'archive
download/mon-ecosysteme_archive.zip (véhicule d'intégrité v2.0).

Vérifications (pipeline PM-INSTALL étapes 1-2, 8 — périmètre v1.1.0) :
  1. SHA-256 des fichiers du corpus canonique skills/@mon-ecosysteme/
  2. Round-trip byte-identité archive download/mon-ecosysteme_archive.zip ↔ corpus
  3. Synchronisation download/ (SYNC_MAP 11 fichiers — recalibré fusion v1.1.0)
  4. Structure des 16 skills écosystème + 3 skills métier installés
  5. Cohérence versions SKILL.md ↔ registre KNOWLEDGE.md (16 entrées versionnées
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
    "gen-plan": "3.17.1",
    "knowledge-observer": "1.0.0",
    "correct-work": "2.7.0",
    "clone-chat": "2.0.0",
    "skills-inventory": "1.0.0",
    "skill-creator": "1.0.0",
    "agent-creator": "2.0.0",
    "script-creator": "1.0.0",
    "script-reviewer": "1.0.0",
    "audit-provenance": "1.0.0",
    "prompt-engineering": "2.1.0",
    "context-engineering": "1.1.0",
    "loop-engineering": "1.0.1",
    "graph-engineering": "1.0.1",
    "harness-engineering": "1.0.1",
    "script-mon-ecosysteme-infrastructure": "1.1.0",
}
# Convention KB_ONLY_VERSION levée (corrige-ecosysteme G-bis) : skill-creator
# porte désormais sa version dans le frontmatter (v1.0.0) comme les autres.
KB_ONLY_VERSION = set()
METIER_SKILLS = ["audio-metadata", "cpp-analysis", "pdf-llm"]
# [N14-c] SYNC_MAP canal 8 courants — voir bloc SYNC_MAP ci-dessous
# SYNC_MAP canal Architecture v2.0 — 8 fichiers COURANTS (cible A7) ;
# CORPUS_ATTENDU — invariant canonique du corpus (dérivation L003) [N28]
# Recalibrage L004 (Task 56) : 20 → 21 — ajout clone -f (directive utilisateur
# « push le clone dans @mon-ecosysteme/ » ; miroir + archive alignés).
CORPUS_ATTENDU = 21
SYNC_MAP = [
    "PROMPT-MAITRE-SHARED.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.12.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.13.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.16.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.17.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.17.1.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md",
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
    # INSTALL-ECOSYSTEME.md retiré — fusion installateurs v1.1.0 (2026-10-02, R4)
    "SYNC-CONTEXT.md",
    "README.md",
]

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
    check(f"{CORPUS_ATTENDU} fichiers présents (Architecture v2.0 — N28, recalibré L004 Task 56)", len(corpus_files) == CORPUS_ATTENDU,
          f"{len(corpus_files)} fichiers")
    for fname in corpus_files:
        digest = sha256(os.path.join(CORPUS, fname))
        manifest["corpus"][fname] = digest

    print("\n=== 2. Archive round-trip (véhicule d'intégrité v2.1) ===")
    ok, n_ident, n_homologues = os.path.isfile(ARCHIVE), 0, 0
    if ok:
        import zipfile
        with zipfile.ZipFile(ARCHIVE) as z:
            znames = [n for n in z.namelist() if not n.endswith("/")]
            for n in znames:
                rel = n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n
                cp = os.path.join(CORPUS, rel)
                if os.path.isfile(cp) and hashlib.sha256(z.read(n)).hexdigest() == sha256(cp):
                    manifest["archive"][rel] = sha256(cp)
                    n_ident += 1
                elif rel.startswith("homologues/"):
                    n_homologues += 1
            # v2.1 (N26, recalibrage L004) : corpus ⊆ archive byte-identique +
            # extras uniquement sous homologues/ (famille créateur/relecture).
            extras = [n for n in znames
                      if (n.split("@mon-ecosysteme/")[-1]
                          if "@mon-ecosysteme/" in n else n) not in corpus_files]
            ok = (n_ident == len(corpus_files)
                  and all(e.startswith("homologues/") for e in extras)
                  and n_ident + len(extras) == len(znames))
    check("Archive byte-identique au corpus + homologues (v2.1)", ok,
          f"{n_ident}/{len(corpus_files)} + {n_homologues} homologues (N26 — recalibrage L004)")

    print("\n=== 3. Synchronisation download/ ===")
    for fname in SYNC_MAP:
        d = os.path.join(DOWNLOAD, fname)
        c = os.path.join(CORPUS, fname)
        if os.path.isfile(d) and os.path.isfile(c):
            digest = sha256(d)
            manifest["download"][fname] = digest
            check(f"sync {fname}", digest == manifest["corpus"].get(fname))
        else:
            check(f"sync {fname}", False, "fichier manquant")

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
        check("16 entrées KB versionnées + Décisions d'architecture",
              len(entries) == 16 and has_decisions,
              f"{len(entries)} entrées versionnées, Décisions={'oui' if has_decisions else 'non'}")
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
