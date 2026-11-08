#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 77 G2 / T2.2.2 — Cascade KO-L004 complète pour gen-plan v3.40.0
(à exécuter APRÈS : amendement v3400 + génération PM v3.40.0 + git mv v3.39.0).

Recalibrages mécaniques (comptages dérivés du disque — KO-L003) :
  A. skills/@historique/README.md — §5 (en-tête 56 PMs, complément Task 77,
     sceau v3.39.0, resorption sceaux manquants) + §2 (ligne gen-plan 44 PMs,
     vue d'ensemble GEN-PLAN + resorption lag CORRECT-WORK).
  B. skills/@historique/historiques-par-skill/gen-plan.md — vivante v3.40.0,
     archivés 44, ligne table v3.40.0, liste fichiers + v3.39.0.
  C. skills/KNOWLEDGE.md — entrée gen-plan v3.40.0 (en-tête, description,
     Dernière calibration).
  D. skills/@mon-ecosysteme/README.md — Version 2.1.20, SHARED v1.7.35,
     révision v2.1.20, arborescence v3.40.0.
  E. pin ECO_SKILLS — scripts/check-ecosysteme-integrity.py ×2 arbres.

Garde-fous : idempotence (no-op si déjà appliqué) ; assert count==1 ;
ABANDON rc=2 sans écriture si un ancrage échoue (tout en mémoire avant écriture).
"""
import hashlib
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
H = Path("/home/z/my-project")  # hôte (pin)
ARCH_GP = R / "skills/@historique/prompts-maitres/gen-plan"
PM_V3400 = R / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.40.0.md"
PM_V3390_ARCH = ARCH_GP / "PROMPT-MAITRE-GEN-PLAN-v3.39.0.md"
README_HIST = R / "skills/@historique/README.md"
HIST_GP = R / "skills/@historique/historiques-par-skill/gen-plan.md"
KB = R / "skills/KNOWLEDGE.md"
README_CORPUS = R / "skills/@mon-ecosysteme/README.md"
PIN_REPO = R / "scripts/check-ecosysteme-integrity.py"
PIN_HOST = H / "scripts/check-ecosysteme-integrity.py"

SHA_ATTENDU = "918bc6925dab6b16a55f228791b039454f74b524e6984b2d9bb4f42c8fb01395"


def sub(text, old, new, label, n=1):
    c = text.count(old)
    if c != n:
        print("ABANDON : ancrage [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, old[:70]))
        sys.exit(2)
    return text.replace(old, new)


def sceau(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def versions_table_rows(pm_text):
    return len(re.findall(r"^\| v\d+\.\d+\.\d+ \|", pm_text, re.M))


def main():
    # --- état mécanique
    sha = sceau(PM_V3390_ARCH)
    if sha != SHA_ATTENDU:
        print("ABANDON : SHA-256 du PM v3.39.0 archivé = %s (attendu %s)" % (sha, SHA_ATTENDU))
        return 2
    fichiers_gp = sorted(p.name for p in ARCH_GP.glob("PROMPT-MAITRE-GEN-PLAN-v*.md"))
    n_gp = len(fichiers_gp)
    total_4 = sum(len(list(d.glob("*.md"))) for d in
                  (R / "skills/@historique/prompts-maitres").iterdir() if d.is_dir())
    pm40 = PM_V3400.read_text(encoding="utf-8")
    v_doc = versions_table_rows(pm40)
    print("[mécanique] gen-plan archivés : %d · total 4 familles : %d · versions documentées §7 PM v3.40.0 : %d"
          % (n_gp, total_4, v_doc))

    readme = README_HIST.read_text(encoding="utf-8")
    if "PROMPT-MAITRE-GEN-PLAN-v3.39.0.md | " + sha[:16] in readme:
        print("[NO-OP] cascade déjà appliquée (sceau v3.39.0 présent au README @historique)")
        return 0

    # --- A. README @historique
    a = readme
    a = sub(a, "## 5. Index des fichiers sources archivés (50 PMs — sceau SHA-256)",
            "## 5. Index des fichiers sources archivés (%d PMs — sceau SHA-256 ; comptage mécanique "
            "recalibré Task 77, label « 50 » stale résorbé)" % total_4,
            "§5 en-tête comptage")
    a = sub(a, "archivé par `mv` byte-identité R4 (round-trip SHA-256 vérifié par scripts/task72-cascade.py ; sceau ci-dessous).",
            "archivé par `mv` byte-identité R4 (round-trip SHA-256 vérifié par scripts/task72-cascade.py ; sceau ci-dessous). "
            "Complément cascade Task 77 (2026-11-08, session web-ecef7f80 — protocole d'émission parallèle gen-plan "
            "v3.40.0, directive trace 1a1ba66f3aff26e9) : `PROMPT-MAITRE-GEN-PLAN-v3.39.0.md` archivé par `git mv` "
            "byte-identité R4 (SHA-256 scellé ci-dessous).",
            "§5 intro complément Task 77")
    a = sub(a, "| Fichier archivé | SHA-256 |\n|-----------------|---------|\n| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.38.0.md",
            "| Fichier archivé | SHA-256 |\n|-----------------|---------|\n"
            "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md | %s |\n"
            "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.38.0.md" % sha,
            "§5 sceau v3.39.0")
    a = sub(a, "40 PMs GEN-PLAN historiques (v3.6.1 → v3.37.0)",
            "%d PMs GEN-PLAN historiques (v3.6.1 → v3.39.0 — comptage mécanique Task 77, labels stalés « 40 »/« 45 » résorbés)" % n_gp,
            "§2 ligne gen-plan")
    a = sub(a, "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 48 (v2.0.0 → v3.37.1) | 40 (v3.6.1 → v3.37.0) | v3.37.1 |",
            "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | %d (v2.0.0 → v3.40.0) | %d (v3.6.1 → v3.39.0) | v3.40.0 |" % (v_doc, n_gp),
            "§2 vue d'ensemble GEN-PLAN")
    # resorption lag CORRECT-WORK (mécanique)
    d_cw = R / "skills/@historique/prompts-maitres/correct-work"
    n_cw = len(list(d_cw.glob("*.md")))
    pm_cw = (R / "skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.11.0.md")
    v_cw = versions_table_rows(pm_cw.read_text(encoding="utf-8")) if pm_cw.exists() else None
    if v_cw:
        max_cw = sorted((p.stem.split("-v")[-1] for p in d_cw.glob("*.md")),
                        key=lambda s: tuple(int(x) for x in s.split(".")))[-1]
        a = sub(a, "| CORRECT-WORK | correct-work — vérification/correction (5 étapes, 4 modes) | 12 (v1.0.0 → v2.9.0) | 6 (v2.4.0 → v2.8.0) | v2.9.0 |",
                "| CORRECT-WORK | correct-work — vérification/correction (5 étapes, 4 modes) | %d (v1.0.0 → v2.11.0) | %d (v2.4.0 → v%s) | v2.11.0 |" % (v_cw, n_cw, max_cw),
                "§2 vue d'ensemble CORRECT-WORK (lag résorbé)")
    # resorption sceaux manquants (fichiers archivés sans ligne de sceau)
    rows = set(re.findall(r"^\| ((?:gen-plan|correct-work|clone-chat|refactor-guard)/[^|]+?) \|", a, re.M))
    manquants = []
    for d in ("gen-plan", "correct-work", "clone-chat", "refactor-guard"):
        for p in sorted((R / "skills/@historique/prompts-maitres" / d).glob("*.md")):
            rel = "%s/%s" % (d, p.name)
            if rel not in rows:
                manquants.append((rel, sceau(p)))
    if manquants:
        lignes = "".join("\n| %s | %s |" % (rel, s) for rel, s in manquants)
        # insertion propre : lignes de complément après la ligne v3.39.0
        a = sub(a, "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md | %s |" % sha,
                "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md | %s |%s" % (sha, lignes),
                "sceaux manquants (complément Task 77)")
        print("[resorption] sceaux ajoutés : %s" % ", ".join(rel for rel, _ in manquants))

    # --- B. historiques-par-skill/gen-plan.md
    b = HIST_GP.read_text(encoding="utf-8")
    b = sub(b, "> **Version vivante (corpus)** : v3.39.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md` (sa table §7 fait foi)",
            "> **Version vivante (corpus)** : v3.40.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.40.0.md` (sa table §7 fait foi)",
            "vivante")
    b = sub(b, "> **Versions archivées** : 45 PMs (v3.6.1 → v3.38.0)",
            "> **Versions archivées** : %d PMs (v3.6.1 → v3.39.0 — comptage mécanique Task 77, label « 45 » stale résorbé)" % n_gp,
            "archivées")
    lignes_v = re.findall(r"^\| v3\.39\.0 \|[^\n]*\|$", b, re.M)
    if len(lignes_v) != 1:
        print("ABANDON : ligne table v3.39.0 trouvée %d fois (attendu 1)" % len(lignes_v))
        return 2
    nouvelle_ligne = ("| v3.40.0 | 2026-11-08 | Task 77 G2 (session web-ecef7f80 — directive trace 1a1ba66f3aff26e9 : "
                      "« vérifie que mon écosystème te permet de lancer 4 commandes en parallèle … fais en sorte "
                      "qu'il te permette de le faire ») : PROTOCOLE D'ÉMISSION PARALLÈLE — opérationnalisation de "
                      "la philosophie #4 (doctrine présente v3.24.0/v3.32.0, jamais appliquée : plans Tasks 70-76 "
                      "100 % série) : fan-out multi-appels (un même bloc, tous outils) + concurrence intra-commande "
                      "(`&`+`wait`/`xargs -P` ; mesure : 4×sleep 2 → 2,00 s vs 8,00 s — le shell persistant "
                      "sérialise les Bash d'un même bloc) ; bornes ≤ 4/vague (G-RES), preuve d'indépendance "
                      "légère, exceptions série inchangées, tracé worklog allégé ; SKILL.md 30 666 o < 30 Kio "
                      "(compensation byte) ; intégral protocoles-detailles.md (extension v3.40.0) + "
                      "graph-diamond-pattern.md §5 ; cascade KO-L004 : PM v3.40.0 (delta verrouillé "
                      "scripts/delta-genplan-v3400.json) + SHARED v1.7.35 + PM-INSTALL v1.9.12 + PM v3.39.0 "
                      "archivé R4 (sceau 918bc692…) + KB + pin ECO_SKILLS 3.40.0 + README corpus v2.1.20 |")
    b = sub(b, lignes_v[0], lignes_v[0] + "\n" + nouvelle_ligne, "ligne table v3.40.0")
    mliste = re.findall(r"^Fichiers archivés de la famille :[^\n]*$", b, re.M)
    if len(mliste) != 1:
        print("ABANDON : ligne « Fichiers archivés de la famille » trouvée %d fois" % len(mliste))
        return 2
    ligne_liste = mliste[0]
    if "v3.38.0" in ligne_liste and "v3.39.0" not in ligne_liste:
        idx = ligne_liste.rfind("v3.38.0")
        nouvelle_liste = ligne_liste[:idx] + "v3.38.0, v3.39.0" + ligne_liste[idx + len("v3.38.0"):]
        b = sub(b, ligne_liste, nouvelle_liste, "liste fichiers archivés + v3.39.0")

    # --- C. KB
    c = KB.read_text(encoding="utf-8")
    c = sub(c, "## gen-plan v3.39.0", "## gen-plan v3.40.0", "KB en-tête")
    c = sub(c, "philosophie #4 parallélisation par défaut des tâches ET des commandes (extension v3.32.0) + dégradation gracieuse",
            "philosophie #4 parallélisation par défaut des tâches ET des commandes (extension v3.32.0 ; protocole "
            "d'émission v3.40.0 : fan-out multi-appels + concurrence intra-commande `&`+`wait`/`xargs -P`, bornes "
            "G-RES ≤ 4/vague) + dégradation gracieuse",
            "KB description protocole")
    c = sub(c, "- **Dernière calibration** : montée v3.39.0 (2026-11-08, Task 72 G1 — directives « Chantier R1 : re-curation",
            "- **Dernière calibration** : montée v3.40.0 (2026-11-08, Task 77 G2 — directive trace 1a1ba66f3aff26e9 : "
            "protocole d'émission parallèle) ; précédente montée v3.39.0 (2026-11-08, Task 72 G1 — directives « Chantier R1 : re-curation",
            "KB dernière calibration")

    # --- D. README corpus
    d = README_CORPUS.read_text(encoding="utf-8")
    d = sub(d, "> **Version** : 2.1.18", "> **Version** : 2.1.20", "README corpus version")
    d = sub(d, "> **Architecture** : v2.2 — SHARED v1.7.34 — Contexte Système 3 niveaux",
            "> **Architecture** : v2.2 — SHARED v1.7.35 — Contexte Système 3 niveaux",
            "README corpus architecture")
    d = sub(d, "> **Révision v2.1.19",
            "> **Révision v2.1.20 (2026-11-08, Task 77 G2 — session web-ecef7f80, directive propriétaire trace "
            "1a1ba66f3aff26e9 « vérifie que mon écosystème te permet de lancer 4 commandes en parallèle »)** : "
            "gen-plan v3.39.0→v3.40.0 (PROTOCOLE D'ÉMISSION PARALLÈLE — PM v3.40.0 généré mécaniquement, delta "
            "verrouillé scripts/delta-genplan-v3400.json) ; SHARED v1.7.35 ; PM-INSTALL v1.9.12 ; PM v3.39.0 "
            "archivé R4 @historique (sceau 918bc692…) ; KB gen-plan v3.40.0 + pin ECO_SKILLS 3.40.0 ; "
            "ULTRA régénéré.\n> **Révision v2.1.19",
            "README corpus révision v2.1.20")
    d = sub(d, "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.39.0.md", "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.40.0.md",
            "README corpus arborescence")

    # --- E. pin ×2 arbres
    e_repo = PIN_REPO.read_text(encoding="utf-8")
    e_host = PIN_HOST.read_text(encoding="utf-8") if PIN_HOST.exists() else e_repo
    pin_sub_old = '"gen-plan": "3.39.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 72 G1 : v3.39.0 re-curation progressiv'
    pin_sub_new = '"gen-plan": "3.40.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 77 G2 : v3.40.0 protocole d\'émission parallèle ; précédent Task 72 G1 : v3.39.0 re-curation progressiv'
    e_repo = sub(e_repo, pin_sub_old, pin_sub_new, "pin repo")
    e_host = sub(e_host, pin_sub_old, pin_sub_new, "pin hôte")

    # --- écritures (tout validé en mémoire)
    README_HIST.write_text(a, encoding="utf-8")
    HIST_GP.write_text(b, encoding="utf-8")
    KB.write_text(c, encoding="utf-8")
    README_CORPUS.write_text(d, encoding="utf-8")
    PIN_REPO.write_text(e_repo, encoding="utf-8")
    if PIN_HOST.exists():
        PIN_HOST.write_text(e_host, encoding="utf-8")
    print("Cascade écrite : README @historique (§2+§5, %d PMs) · historiques-par-skill (v3.40.0, %d archivés) · "
          "KB (gen-plan v3.40.0) · README corpus (v2.1.20, SHARED v1.7.35) · pin ECO_SKILLS 3.40.0 ×%d arbre(s)"
          % (total_4, n_gp, 2 if PIN_HOST.exists() else 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
