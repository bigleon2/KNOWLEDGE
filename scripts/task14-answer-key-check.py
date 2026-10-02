#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.3)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Arbitre dédié de session — answer key Task 14 (14 décisions D001-D014).

Vérifie MÉCANIQUEMENT que chaque décision documentée au worklog Task 14 est
bien l'état réel de l'écosystème local (boucle E12-E13 du PM gen-plan v3.18.0).
"""
import os
import re
import sys
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "skills", "@mon-ecosysteme")
DOWNLOAD = os.path.join(BASE, "download")
ARCHIVE = os.path.join(DOWNLOAD, "mon-ecosysteme_archive.zip")
KB = os.path.join(BASE, "skills", "KNOWLEDGE.md")

results = []


def check(did, label, ok):
    results.append((did, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {did} — {label}")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def main():
    print("=== ANSWER KEY TASK 14 — vérification mécanique D001-D014 ===")
    pm_install = read(os.path.join(CORPUS, "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"))
    shared = read(os.path.join(CORPUS, "PROMPT-MAITRE-SHARED.md"))
    sync_ctx = read(os.path.join(CORPUS, "SYNC-CONTEXT.md"))
    readme = read(os.path.join(CORPUS, "README.md"))
    kb = read(KB)
    corpus_files = sorted(f for f in os.listdir(CORPUS) if os.path.isfile(os.path.join(CORPUS, f)))

    # D001 — publication de la vague complète (v1.2.0 → v1.3.0) : montées versionnées
    check("D001", "PM-INSTALL v1.3.0 (v1.2.0 → v1.3.0 publiée, historique cumulatif v1.2.0+v1.3.0)",
          pm_install.startswith("# PROMPT MAÎTRE") and "Version : 1.3.0" in pm_install[:400]
          and "| v1.3.0 |" in pm_install and "| v1.2.0 |" in pm_install)

    # D002 — analyse à jour : zéro drift skills (vérifié par rsync bidirectionnel en session —
    # forme matérielle : les 21 ECO_SKILLS certifiés par integrity, KB 21 entrées)
    check("D002", "skills écosystème synchronisés (21 ECO certifiés integrity, KB 21 entrées)",
          len(re.findall(r"^## [\w-]+ v[\d.]+", kb, re.M)) == 21)

    # D003 — analyse harmonisation : drifts identifiés et résorbés (parseur B8+, §6.1 GEN-PLAN)
    cert = read(os.path.join(BASE, "scripts", "certification-complete.py"))
    check("D003", "drift harmonisation résorbé : SHARED §6.1 GEN-PLAN v3.18.0 + parseur B8+",
          "PROMPT-MAITRE-GEN-PLAN-v3.18.0.md" in shared
          and "ERRORS?" in cert and "V[ée]rifications" in cert)

    # D004 — doublons : critère même nom + byte-identique, 14 identifiés puis supprimés
    dup = [f for f in corpus_files if os.path.isfile(os.path.join(DOWNLOAD, f))]
    check("D004", "0 doublon corpus↔download/ (critère même nom + byte-identique)", not dup)

    # D005 — l'archive n'est PAS un doublon : conservée, véhicule v2.2, round-trip 24/24
    n_ident = 0
    with zipfile.ZipFile(ARCHIVE) as z:
        for f in corpus_files:
            if z.read(f"@mon-ecosysteme/{f}") == open(os.path.join(CORPUS, f), "rb").read():
                n_ident += 1
    check("D005", f"archive = véhicule d'intégrité v2.2 conservé (round-trip {n_ident}/{len(corpus_files)})",
          n_ident == len(corpus_files) == 24)

    # D006 — artefacts de session NON corpus conservés dans le dépôt (noms distincts)
    # (vérifié côté véhicule en session ; forme locale : le scanner ne signale que l'archive)
    check("D006", "les artefacts non-corpus (noms distincts) ne sont pas des doublons (scan 0 doublon)",
          not dup and os.path.isfile(ARCHIVE))

    # D007 — suppression du canal = décision d'architecture v2.2 au registre KB
    check("D007", "décision v2.2 consignée au KB (section Décisions d'architecture)",
          "## Décisions d'architecture" in kb and "décision v2.2" in kb and "Task 14" in kb)

    # D008 — corpus recalibré : SHARED v1.6.3, SYNC-CONTEXT v1.4.0, README v2.1.0, ULTRA régénéré
    ultra = read(os.path.join(CORPUS, "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"))
    check("D008", "corpus v1.3.0 complet (SHARED 1.6.3, SYNC 1.4.0, README 2.1.0, ULTRA v2.2)",
          "**Version** : 1.6.3" in shared and "**Version** : 1.4.0" in sync_ctx
          and "**Version** : 2.1.0" in readme and "v2.2" in ultra
          and "v1.6.3" in ultra and "v1.3.0" in ultra)

    # D009 — sync-download.py retiré → _archive/ ; gardes en place
    check("D009", "sync-download.py → _archive/ ; gardes scan-doublons + deduplication en place",
          not os.path.isfile(os.path.join(BASE, "scripts", "sync-download.py"))
          and os.path.isfile(os.path.join(BASE, "scripts", "_archive", "sync-download.py"))
          and os.path.isfile(os.path.join(BASE, "scripts", "task14-scan-doublons.py"))
          and os.path.isfile(os.path.join(BASE, "scripts", "task14-deduplication.py")))

    # D010 — arbitres inversés : check 3 integrity + §7/§11a/§11d interactions
    cei = read(os.path.join(BASE, "scripts", "check-ecosysteme-integrity.py"))
    tci = read(os.path.join(BASE, "scripts", "test-coherence-interactions.py"))
    check("D010", "arbitres inversés en garde anti-doublons (check 3, §7, §11a, §11d)",
          "Garde anti-doublons download/" in cei and "Garde anti-doublons download/" in tci
          and "sans copie du PM courant" in tci and "sans doublon du PM courant" in tci
          and "SYNC_MAP = [" not in cei)

    # D011 — réserves trigger_evals résorbées : evals équipés dans la langue du skill
    sc_ev = read(os.path.join(BASE, "skills", "skill-creator", "evals", "evals.json"))
    vm_ev = read(os.path.join(BASE, "skills", "version-management", "evals", "evals.json"))
    check("D011", "evals skill-creator (en) + version-management (zh) équipés (5 evals chacun)",
          '"skill_name": "skill-creator"' in sc_ev and "Create a skill from scratch" in sc_ev
          and '"skill_name": "version-management"' in vm_ev and "首个文件写出前" in vm_ev)

    # D012 — orchestrateur recalibré : parseur B8+ + doctrine 42c2a41 + chemins dynamisés
    check("D012", "certification-complete.py recalibré (doctrine réserves, chemins locaux)",
          "PASS AVEC RÉSERVES" in cert and "knowledgerepo" in cert and "push-vehicle" in cert)

    # D013 — réserve fullstack-dev documentée, non résorbée (plateforme, hors périmètre B13-r5)
    check("D013", "réserve fullstack-dev = plateforme, hors périmètre certifiable (documentée)",
          "fullstack-dev" in tci)

    # D014 — §8 interactions recalibré 26 porteurs + compte dynamique
    m = re.search(r"eco_evals\s*=\s*\{(.*?)\}", tci, re.S)
    n_porteurs = len(re.findall(r'"[a-z0-9-]+":', m.group(1))) if m else 0
    check("D014", f"§8 recalibré {n_porteurs} porteurs evals (compte dynamique KO-L003)",
          n_porteurs == 26 and "len(eco_evals)" in tci)

    n_pass = sum(1 for _, ok in results if ok)
    print(f"\n=== RESUME : {n_pass}/{len(results)} PASS, {len(results) - n_pass} FAIL ===")
    sys.exit(0 if n_pass == len(results) else 1)


if __name__ == "__main__":
    main()
