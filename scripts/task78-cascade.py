#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 78/79 G1 — Cascade KO-L004 périmètre gen-plan v3.41.0
(à exécuter APRÈS : task78-amendement-v3410.py + task78-delta-v3410.py
+ generer-pm-skill.py --generate gen-plan --delta + git mv PM v3.40.0).

Recalibrages mécaniques (comptages dérivés du disque — KO-L003) :
  A. skills/@historique/README.md — §5 (en-tête 57 PMs, complément Task 78,
     sceau v3.40.0) + §2 (ligne gen-plan 45 PMs, vue d'ensemble GEN-PLAN).
  B. skills/@historique/historiques-par-skill/gen-plan.md — vivante v3.41.0,
     ligne table v3.41.0, liste fichiers + v3.40.0.
  C. skills/KNOWLEDGE.md — entrée gen-plan v3.41.0 (en-tête, description
     sondage borné, Dernière calibration).
  D. skills/@mon-ecosysteme/README.md — Version 2.1.21, SHARED v1.7.36,
     révision v2.1.21, arborescence v3.41.0.
  E. pin ECO_SKILLS — scripts/check-ecosysteme-integrity.py ×2 arbres.
  F. RETRAITS_SANCTIONNES — scripts/task21-f2-rebuild-archive.py += v3.40.0.

ÉCART AU PLAN Task 78 D006 consigné (règle d'or n°5) : le plan exigeait
« SHARED et PM-INSTALL INCHANGÉS », mais le générateur KO-L004 v1.1.0 applique
le recalibrage croisé par contrat (directive 2026-10-09, 20+ précédents) —
SHARED v1.7.36 + PM-INSTALL v1.9.13 conservés (réversion = lag §6.1), tampon
§0 propagé (propagate-context ×3 passes convergé 0/0/0).

Garde-fous : idempotence (no-op si déjà appliquée) ; assert count==1 ;
ABANDON rc=2 sans écriture si un ancrage échoue (tout en mémoire avant écriture).
"""
import hashlib
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
H = Path("/home/z/my-project")  # hôte (pin)
ARCH_GP = R / "skills/@historique/prompts-maitres/gen-plan"
PM_V3400_ARCH = ARCH_GP / "PROMPT-MAITRE-GEN-PLAN-v3.40.0.md"
README_HIST = R / "skills/@historique/README.md"
HIST_GP = R / "skills/@historique/historiques-par-skill/gen-plan.md"
KB = R / "skills/KNOWLEDGE.md"
README_CORPUS = R / "skills/@mon-ecosysteme/README.md"
PIN_REPO = R / "scripts/check-ecosysteme-integrity.py"
PIN_HOST = H / "scripts/check-ecosysteme-integrity.py"
RETRAITS = R / "scripts/task21-f2-rebuild-archive.py"

SHA_V3400 = "8fa129f99892c83edcb9da5e33a7f7055bd01a9b71845416cc21e00d639c972b"


def sub(text, old, new, label, n=1):
    c = text.count(old)
    if c != n:
        print("ABANDON : ancrage [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, old[:70]))
        sys.exit(2)
    return text.replace(old, new)


def sceau(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # --- état mécanique
    sha = sceau(PM_V3400_ARCH)
    if sha != SHA_V3400:
        print("ABANDON : SHA-256 du PM v3.40.0 archivé = %s (attendu %s)" % (sha, SHA_V3400))
        return 2
    n_gp = len(list(ARCH_GP.glob("PROMPT-MAITRE-GEN-PLAN-v*.md")))
    total_4 = sum(len(list(d.glob("*.md"))) for d in
                  (R / "skills/@historique/prompts-maitres").iterdir() if d.is_dir())
    v_doc = len(re.findall(r"^\| v\d+\.\d+\.\d+ \|",
                           (R / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.41.0.md").read_text(encoding="utf-8"), re.M))
    print("[mécanique] gen-plan archivés : %d · total 4 familles : %d · versions documentées §7 PM v3.41.0 : %d"
          % (n_gp, total_4, v_doc))

    readme = README_HIST.read_text(encoding="utf-8")
    if "PROMPT-MAITRE-GEN-PLAN-v3.40.0.md | " + sha[:16] in readme:
        print("[NO-OP] cascade déjà appliquée (sceau v3.40.0 présent au README @historique)")
        return 0

    # --- A. README @historique
    a = readme
    a = sub(a, "## 5. Index des fichiers sources archivés (56 PMs — sceau SHA-256 ; comptage mécanique recalibré Task 77, label « 50 » stale résorbé)",
            "## 5. Index des fichiers sources archivés (%d PMs — sceau SHA-256 ; comptage mécanique recalibré Task 77, complément Task 78)" % total_4,
            "§5 en-tête comptage")
    a = sub(a, "Complément cascade Task 77 (2026-11-08, session web-ecef7f80 — protocole d'émission parallèle gen-plan v3.40.0, directive trace 1a1ba66f3aff26e9) : `PROMPT-MAITRE-GEN-PLAN-v3.39.0.md` archivé par `git mv` byte-identité R4 (SHA-256 scellé ci-dessous).",
            "Complément cascade Task 77 (2026-11-08, session web-ecef7f80 — protocole d'émission parallèle gen-plan v3.40.0, directive trace 1a1ba66f3aff26e9) : `PROMPT-MAITRE-GEN-PLAN-v3.39.0.md` archivé par `git mv` byte-identité R4 (SHA-256 scellé ci-dessous). "
            "Complément cascade Task 78 (2026-11-08, session web-ecef7f80 — règle de sondage borné gen-plan v3.41.0, directive trace 1a1bbf9f403a2865) : `PROMPT-MAITRE-GEN-PLAN-v3.40.0.md` archivé par `git mv` byte-identité R4 (SHA-256 scellé ci-dessous).",
            "§5 intro complément Task 78")
    a = sub(a, "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md | 918bc6925dab6b16a55f228791b039454f74b524e6984b2d9bb4f42c8fb01395 |",
            "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.40.0.md | %s |\n| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md | 918bc6925dab6b16a55f228791b039454f74b524e6984b2d9bb4f42c8fb01395 |" % sha,
            "§5 sceau v3.40.0")
    a = sub(a, "| `prompts-maitres/gen-plan/` | 44 PMs GEN-PLAN historiques (v3.6.1 → v3.39.0 — comptage mécanique Task 77, labels stalés « 40 »/« 45 » résorbés)",
            "| `prompts-maitres/gen-plan/` | %d PMs GEN-PLAN historiques (v3.6.1 → v3.40.0 — comptage mécanique Task 78)" % n_gp,
            "§2 ligne gen-plan")
    a = sub(a, "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 48 (v2.0.0 → v3.40.0) | 44 (v3.6.1 → v3.39.0) | v3.40.0 |",
            "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | %d (v2.0.0 → v3.41.0) | %d (v3.6.1 → v3.40.0) | v3.41.0 |" % (v_doc, n_gp),
            "§2 vue d'ensemble GEN-PLAN")

    # --- B. historiques-par-skill/gen-plan.md
    b = HIST_GP.read_text(encoding="utf-8")
    b = sub(b, "> **Version vivante (corpus)** : v3.40.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.40.0.md` (sa table §7 fait foi)",
            "> **Version vivante (corpus)** : v3.41.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.41.0.md` (sa table §7 fait foi)",
            "vivante")
    b = sub(b, "> **Versions archivées** : 44 PMs (v3.6.1 → v3.39.0 — comptage mécanique Task 77, label « 45 » stale résorbé)",
            "> **Versions archivées** : %d PMs (v3.6.1 → v3.40.0 — comptage mécanique Task 78)" % n_gp,
            "archivées")
    lignes_v = re.findall(r"^\| v3\.40\.0 \|[^\n]*\|$", b, re.M)
    if len(lignes_v) != 1:
        print("ABANDON : ligne table v3.40.0 trouvée %d fois (attendu 1)" % len(lignes_v))
        return 2
    nouvelle_ligne = ("| v3.41.0 | 2026-11-08 | Task 78/79 G1 (session web-ecef7f80 — directive trace 1a1bbf9f403a2865 : "
                      "« génère le plan du Task \"règle de sondage borné\" » ; origine : avertissement SG2.2 Task 77 "
                      "« Sortie trop volumineuse (en-tête SHARED très long) ») : RÈGLE DE SONDAGE BORNÉ — extension de "
                      "la lecture ciblée (E5-POIDS v3.38.0) aux inspections transverses : (1) jamais de pattern "
                      "générique sur l'arbre skills/ sans mode fichiers (-l) d'abord ; (2) greps multi-fichiers "
                      "tronqués + limite de résultats ; (3) §0/contrats jamais affichés en entier — plages ciblées ; "
                      "(4) exceptions golden-master et contrats PRE/POST (un fichier à la fois) ; mesures : « Contexte "
                      "Système » BRUT 12 207 o vs BORNÉ 3 763 o (gain ×3,2 ; re-mesure fraîche 11 068/3 168, ×3,5) ; "
                      "SKILL.md 30 697 o < 30 Kio tenu (compensation byte — description/§A inchangés, non-régression "
                      "triggers) ; intégral protocoles-detailles.md (Extension v3.41.0) ; cascade KO-L004 : PM v3.41.0 "
                      "(delta verrouillé scripts/delta-genplan-v3410.json) + SHARED v1.7.36 + PM-INSTALL v1.9.13 "
                      "(recalibrage croisé générateur — écart au plan D006 consigné règle d'or n°5) + propagation §0 "
                      "v1.7.36 (convergée 0/0/0) + PM v3.40.0 archivé R4 (sceau 8fa129f9…) + KB + pin ECO_SKILLS "
                      "3.41.0 + README corpus v2.1.21 + ULTRA ×2 (SHA 1eb7269eb078…) |")
    b = sub(b, lignes_v[0], lignes_v[0] + "\n" + nouvelle_ligne, "ligne table v3.41.0")
    b = sub(b, "v3.38.0, v3.39.0 (45 fichiers, SHA-256 au §5 — recalage mécanique Task 71 G1 : les sceaux antérieurs portaient 40 en excluant v3.37.0/v3.37.1 générés depuis)",
            "v3.38.0, v3.39.0, v3.40.0 (45 fichiers, SHA-256 au §5 — recalage mécanique Task 78 : énumération portée v3.6.1→v3.40.0, label « 45 » du Task 71 G1 résorbé)",
            "liste fichiers archivés + v3.40.0")

    # --- C. KB
    c = KB.read_text(encoding="utf-8")
    c = sub(c, "## gen-plan v3.40.0", "## gen-plan v3.41.0", "KB en-tête")
    c = sub(c, "philosophie #4 parallélisation par défaut des tâches ET des commandes (extension v3.32.0 ; protocole "
            "d'émission v3.40.0 : fan-out multi-appels + concurrence intra-commande `&`+`wait`/`xargs -P`, bornes "
            "G-RES ≤ 4/vague) + dégradation gracieuse",
            "philosophie #4 parallélisation par défaut des tâches ET des commandes (extension v3.32.0 ; protocole "
            "d'émission v3.40.0 : fan-out multi-appels + concurrence intra-commande `&`+`wait`/`xargs -P`, bornes "
            "G-RES ≤ 4/vague ; sondage borné v3.41.0 : inspection transverse TOUJOURS bornée — mode fichiers (-l) "
            "d'abord, greps multi-fichiers tronqués + limite de résultats, §0/contrats jamais en entier) + "
            "dégradation gracieuse",
            "KB description sondage borné")
    c = sub(c, "- **Dernière calibration** : montée v3.40.0 (2026-11-08, Task 77 G2 — directive trace 1a1ba66f3aff26e9 : protocole d'émission parallèle) ; précédente montée v3.39.0 (2026-11-08, Task 72 G1 — directives « Chantier R1 : re-curation",
            "- **Dernière calibration** : montée v3.41.0 (2026-11-08, Task 78/79 G1 — directive trace 1a1bbf9f403a2865 : "
            "règle de sondage borné ; SHARED v1.7.36/PM-INSTALL v1.9.13 recalibrés par le générateur — écart au plan "
            "D006 consigné) ; précédente montée v3.40.0 (2026-11-08, Task 77 G2 — directive trace 1a1ba66f3aff26e9 : protocole d'émission parallèle) ; précédente montée v3.39.0 (2026-11-08, Task 72 G1 — directives « Chantier R1 : re-curation",
            "KB dernière calibration")

    # --- D. README corpus
    d = README_CORPUS.read_text(encoding="utf-8")
    d = sub(d, "> **Version** : 2.1.20", "> **Version** : 2.1.21", "README corpus version")
    d = sub(d, "> **Architecture** : v2.2 — SHARED v1.7.35 — Contexte Système 3 niveaux",
            "> **Architecture** : v2.2 — SHARED v1.7.36 — Contexte Système 3 niveaux",
            "README corpus architecture")
    d = sub(d, "> **Révision v2.1.20",
            "> **Révision v2.1.21 (2026-11-08, Task 78/79 G1 — session web-ecef7f80, directive propriétaire trace "
            "1a1bbf9f403a2865 « génère le plan du Task \"règle de sondage borné\" »)** : gen-plan v3.40.0→v3.41.0 "
            "(RÈGLE DE SONDAGE BORNÉ — PM v3.41.0 généré mécaniquement, delta verrouillé "
            "scripts/delta-genplan-v3410.json) ; SHARED v1.7.36 (recalibrage croisé générateur — écart au plan D006 "
            "consigné) ; PM-INSTALL v1.9.13 ; propagation §0 v1.7.36 (119 skills + 185 scripts + 4 agents, convergée "
            "0/0/0) ; PM v3.40.0 archivé R4 @historique (sceau 8fa129f9…) ; KB gen-plan v3.41.0 + pin ECO_SKILLS "
            "3.41.0 ; ULTRA régénéré ×2 (SHA 1eb7269eb078…).\n> **Révision v2.1.20",
            "README corpus révision v2.1.21")
    d = sub(d, "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.40.0.md", "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.41.0.md",
            "README corpus arborescence")

    # --- E. pin ×2 arbres
    e_repo = PIN_REPO.read_text(encoding="utf-8")
    e_host = PIN_HOST.read_text(encoding="utf-8") if PIN_HOST.exists() else e_repo
    pin_old = '"gen-plan": "3.40.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 77 G2 : v3.40.0 protocole d\'émission parallèle ; précédent Task 72 G1'
    pin_new = '"gen-plan": "3.41.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 78/79 G1 : v3.41.0 règle de sondage borné ; précédent Task 77 G2 : v3.40.0 protocole d\'émission parallèle ; précédent Task 72 G1'
    e_repo = sub(e_repo, pin_old, pin_new, "pin repo")
    e_host = sub(e_host, pin_old, pin_new, "pin hôte")

    # --- F. RETRAITS_SANCTIONNES += v3.40.0
    f = RETRAITS.read_text(encoding="utf-8")
    f = sub(f, "RETRAITS_SANCTIONNES = {\n",
            'RETRAITS_SANCTIONNES = {\n'
            "    # cascade gen-plan v3.41.0 (Task 78/79 G1, session web-ecef7f80 2026-11-08 —\n"
            "    # règle de sondage borné, directive trace 1a1bbf9f403a2865) — re-scellement\n"
            "    # Task 78 : PM GEN-PLAN v3.40.0 DÉPLACÉ git mv vers\n"
            "    # skills/@historique/prompts-maitres/gen-plan/ — byte-identité vérifiée\n"
            "    # ci-dessous (garde anti-perte ; SHA 8fa129f99892…).\n"
            '    "PROMPT-MAITRE-GEN-PLAN-v3.40.0.md",\n\n',
            "RETRAITS_SANCTIONNES += v3.40.0")

    # --- écritures (tout validé en mémoire)
    README_HIST.write_text(a, encoding="utf-8")
    HIST_GP.write_text(b, encoding="utf-8")
    KB.write_text(c, encoding="utf-8")
    README_CORPUS.write_text(d, encoding="utf-8")
    PIN_REPO.write_text(e_repo, encoding="utf-8")
    if PIN_HOST.exists():
        PIN_HOST.write_text(e_host, encoding="utf-8")
    RETRAITS.write_text(f, encoding="utf-8")
    print("Cascade écrite : README @historique (§2+§5, %d PMs, sceau v3.40.0) · historiques-par-skill (v3.41.0, "
          "%d archivés) · KB (gen-plan v3.41.0) · README corpus (v2.1.21, SHARED v1.7.36) · pin ECO_SKILLS 3.41.0 "
          "×%d arbre(s) · RETRAITS_SANCTIONNES += v3.40.0"
          % (total_4, n_gp, 2 if PIN_HOST.exists() else 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
