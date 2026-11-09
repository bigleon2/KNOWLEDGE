#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""


# -*- coding: utf-8 -*-
"""
Task 84 G3 — Cascade mécanique post-génération (inscription socle n°56, gen-plan v3.42.0).
À exécuter APRÈS : task84-socle-n56.py + generer-pm-skill.py --generate + git mv PM v3.41.0.

Recalibrages (comptages dérivés du disque — KO-L003) :
  A. SHARED — amendement de l'entrée révision v1.7.37 (couvrir §7 n°56).
  B. README @historique — §5 (58 PMs, complément Task 84, sceau v3.41.0) + §2 (46 archives).
  C. historiques-par-skill/gen-plan.md — vivante v3.42.0, ligne table v3.42.0, fichiers 46.
  D. KB — gen-plan v3.42.0 (en-tête + description n°56 + calibration) ; n°56 (mobilisation
     gen-plan déclarée + calibration pendance éteinte).
  E. README corpus — v2.1.22, SHARED v1.7.37, révision, arborescence v3.42.0.
  F. pin ECO_SKILLS — check-ecosysteme-integrity.py ×2 arbres (3.41.0→3.42.0).
  G. RETRAITS_SANCTIONNES — task21-f2-rebuild-archive.py += v3.41.0.
  H. historiques-par-skill/agent-engineering.md — ligne socle + typo « §1 ission ».

Garde-fous : idempotence (no-op si déjà appliquée) ; assert count==1 ;
ABANDON rc=2 SANS écriture si un ancrage échoue (tout en mémoire).
"""
import hashlib
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
H = Path("/home/z/my-project")
SHARED = R / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"
PM_V3410_ARCH = R / "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.41.0.md"
PM_V3420 = R / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.42.0.md"
README_HIST = R / "skills/@historique/README.md"
HIST_GP = R / "skills/@historique/historiques-par-skill/gen-plan.md"
HIST_AE = R / "skills/@historique/historiques-par-skill/agent-engineering.md"
KB = R / "skills/KNOWLEDGE.md"
README_CORPUS = R / "skills/@mon-ecosysteme/README.md"
PIN_REPO = R / "scripts/check-ecosysteme-integrity.py"
PIN_HOST = H / "scripts/check-ecosysteme-integrity.py"
RETRAITS = R / "scripts/task21-f2-rebuild-archive.py"


def sub(text, old, new, label, n=1):
    c = text.count(old)
    if c != n:
        print("ABANDON : ancrage [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, old[:70]))
        sys.exit(2)
    return text.replace(old, new)


def sceau(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sha = sceau(PM_V3410_ARCH)
    n_gp = len(list((R / "skills/@historique/prompts-maitres/gen-plan").glob("PROMPT-MAITRE-GEN-PLAN-v*.md")))
    total_4 = sum(len(list(d.glob("*.md"))) for d in
                  (R / "skills/@historique/prompts-maitres").iterdir() if d.is_dir())
    v_doc = len(re.findall(r"^\| v\d+\.\d+\.\d+ \|", PM_V3420.read_text(encoding="utf-8"), re.M))
    print("[mécanique] gen-plan archivés : %d · total 4 familles : %d · versions documentées §7 PM v3.42.0 : %d"
          % (n_gp, total_4, v_doc))

    readme = README_HIST.read_text(encoding="utf-8")
    if ("gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.41.0.md | " + sha[:16]) in readme:
        print("[NO-OP] cascade déjà appliquée (sceau v3.41.0 présent au README @historique)")
        return 0

    # --- A. SHARED — amendement révision v1.7.37 (couvrir §7 n°56)
    s = SHARED.read_text(encoding="utf-8")
    s = sub(s, "2026-11-09 (montée gen-plan v3.41.0→v3.42.0, KO-L004 v1.1.0) — **v1.7.37** : §6.1",
            "2026-11-09 (inscription discipline n°56 agent-engineering au socle + montée gen-plan v3.41.0→v3.42.0, "
            "KO-L004 v1.1.0) — **v1.7.37** : §7 — inscription de la discipline n°56 agent-engineering (ligne définition "
            "+ registre d'assignation — précédents v1.7.0 n°54 / Task 7-8 n°55 ; Task 84, pendance P1 éteinte) ; §6.1",
            "révision v1.7.37 amendée §7")

    # --- B. README @historique
    a = readme
    a = sub(a, "## 5. Index des fichiers sources archivés (57 PMs — sceau SHA-256 ; comptage mécanique recalibré Task 77, complément Task 78)",
            "## 5. Index des fichiers sources archivés (%d PMs — sceau SHA-256 ; comptage mécanique recalibré Task 77, complément Task 84)" % total_4,
            "§5 en-tête comptage")
    a = sub(a, "Complément cascade Task 78 (2026-11-08, session web-ecef7f80 — règle de sondage borné gen-plan v3.41.0, directive trace 1a1bbf9f403a2865) : `PROMPT-MAITRE-GEN-PLAN-v3.40.0.md` archivé par `git mv` byte-identité R4 (SHA-256 scellé ci-dessous).",
            "Complément cascade Task 78 (2026-11-08, session web-ecef7f80 — règle de sondage borné gen-plan v3.41.0, directive trace 1a1bbf9f403a2865) : `PROMPT-MAITRE-GEN-PLAN-v3.40.0.md` archivé par `git mv` byte-identité R4 (SHA-256 scellé ci-dessous). "
            "Complément cascade Task 84 (2026-11-09, session web-ecef7f80 — inscription socle discipline n°56, gen-plan v3.42.0, directive trace 1a1bed51ccaf78f1) : `PROMPT-MAITRE-GEN-PLAN-v3.41.0.md` archivé par `git mv` byte-identité R4 (SHA-256 scellé ci-dessous).",
            "§5 intro complément Task 84")
    a = sub(a, "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.40.0.md | 8fa129f99892c83edcb9da5e33a7f7055bd01a9b71845416cc21e00d639c972b |",
            "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.41.0.md | %s |\n| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.40.0.md | 8fa129f99892c83edcb9da5e33a7f7055bd01a9b71845416cc21e00d639c972b |" % sha,
            "§5 sceau v3.41.0")
    a = sub(a, "| `prompts-maitres/gen-plan/` | 45 PMs GEN-PLAN historiques (v3.6.1 → v3.40.0 — comptage mécanique Task 78)",
            "| `prompts-maitres/gen-plan/` | %d PMs GEN-PLAN historiques (v3.6.1 → v3.41.0 — comptage mécanique Task 84)" % n_gp,
            "§2 ligne gen-plan")
    a = sub(a, "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 49 (v2.0.0 → v3.41.0) | 45 (v3.6.1 → v3.40.0) | v3.41.0 |",
            "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | %d (v2.0.0 → v3.42.0) | %d (v3.6.1 → v3.41.0) | v3.42.0 |" % (v_doc, n_gp),
            "§2 vue d'ensemble GEN-PLAN")

    # --- C. historiques-par-skill/gen-plan.md
    b = HIST_GP.read_text(encoding="utf-8")
    b = sub(b, "> **Version vivante (corpus)** : v3.41.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.41.0.md` (sa table §7 fait foi)",
            "> **Version vivante (corpus)** : v3.42.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.42.0.md` (sa table §7 fait foi)",
            "vivante")
    b = sub(b, "> **Versions archivées** : 45 PMs (v3.6.1 → v3.40.0 — comptage mécanique Task 78)",
            "> **Versions archivées** : %d PMs (v3.6.1 → v3.41.0 — comptage mécanique Task 84)" % n_gp,
            "archivées")
    b = sub(b, "## Famille GEN-PLAN — 49 versions (skill : gen-plan)",
            "## Famille GEN-PLAN — %d versions (skill : gen-plan)" % v_doc, "en-tête famille")
    ligne_v3420 = ("| v3.42.0 | 2026-11-09 | Task 84 G3 (session web-ecef7f80 — directive trace 1a1bed51ccaf78f1 "
                   "« continue », pendance P1 Task 83) : INSCRIPTION SOCLE n°56 — agent-engineering (ABE/AE/MASE, "
                   "créée Task 83) inscrite au socle de vérité : SHARED §7 (ligne définition + registre "
                   "d'assignation, v1.7.37) + gen-plan §1.6 + §3 Relations (ajouts purs) ; MINOR, description/§A "
                   "inchangés (non-régression triggers) ; cascade KO-L004 : PM v3.42.0 (delta verrouillé "
                   "scripts/delta-genplan-v3420.json) + SHARED v1.7.37 + PM-INSTALL v1.9.14 + PM v3.41.0 archivé R4 "
                   "(sceau %s…) + KB gen-plan v3.42.0 + KB n°56 mobilisation déclarée + pin ECO_SKILLS 3.42.0 + "
                   "ULTRA régénéré + propagation §0 v1.7.37 | La discipline n°56 est lisible depuis le socle "
                   "(SHARED §7 source de vérité) — le routage des tâches d'agents (ABE/AE/MASE) s'appuie sur le "
                   "socle, plus sur la seule entrée KB |" % sha[:16])
    b = sub(b, "| v3.41.0 | 2026-11-08 |", ligne_v3420 + "\n| v3.41.0 | 2026-11-08 |", "table v3.42.0 (au-dessus v3.41.0)")
    b = sub(b, ", v3.39.0, v3.40.0 (45 fichiers, SHA-256 au §5 — recalage mécanique Task 78 : énumération portée v3.6.1→v3.40.0, label « 45 » du Task 71 G1 résorbé).",
            ", v3.39.0, v3.40.0, v3.41.0 (%d fichiers, SHA-256 au §5 — recalage mécanique Task 84 : énumération portée v3.6.1→v3.41.0)." % n_gp,
            "fichiers archivés énumération")

    # --- D. KB — gen-plan + n°56
    k = KB.read_text(encoding="utf-8")
    k = sub(k, "## gen-plan v3.41.0", "## gen-plan v3.42.0", "KB en-tête gen-plan")
    k = sub(k, " ; hook E1-RES §1.2bis (n67-1 reconstitué post-wipe : B-11 + collecte G-RES + fraîcheur du plan)",
            " ; hook E1-RES §1.2bis (n67-1 reconstitué post-wipe : B-11 + collecte G-RES + fraîcheur du plan) ; "
            "disciplines §1.6 : matérialisation n°56 agent-engineering (Task 84 — englobante ABE/AE/MASE, inscrite au "
            "socle SHARED §7 v1.7.37 — cadrage/routage des tâches d'agents, détention orchestrée registre décentralisé "
            "§8 du skill, v3.42.0)",
            "KB description gen-plan n°56")
    k = sub(k, "- **Dernière calibration** : montée v3.41.0 (2026-11-08, Task 78/79 G1 — directive trace 1a1bbf9f403a2865",
            "- **Dernière calibration** : montée v3.42.0 (2026-11-09, Task 84 G3 — directive 1a1bed51ccaf78f1 « continue » : "
            "INSCRIPTION SOCLE n°56 — SHARED §7 [définition + registre] v1.7.37 + gen-plan §1.6/§3 [pendance P1 Task 83 "
            "éteinte] ; SHARED v1.7.37/PM-INSTALL v1.9.14 recalibrés par le générateur ; PM v3.41.0 archivé R4) ; "
            "précédente montée v3.41.0 (2026-11-08, Task 78/79 G1 — directive trace 1a1bbf9f403a2865",
            "KB calibration gen-plan")
    k = sub(k, "- **Utilisé par** : tout élément consommateur d'agents (flottes, agents autonomes, fabriques — cadre n°56) ; mobilisation par le planificateur de l'écosystème à déclarer à l'inscription socle (pendance Task 83 — cf. Dernière calibration)",
            "- **Utilisé par** : tout élément consommateur d'agents (flottes, agents autonomes, fabriques — cadre n°56) ; "
            "gen-plan §1.6/§3 (mobilisation de la discipline n°56 — orchestration des tâches ABE/AE/MASE, déclarée à "
            "l'inscription socle Task 84 G3)",
            "KB n°56 Utilisé par (mobilisation déclarée)")
    k = sub(k, " ; inscription socle SHARED §7 + gen-plan §1.6 = pendance structurée (précédents v1.7.0 n°54 / Task 7-8 n°55 — tâche dédiée)",
            " ; inscription socle SHARED §7 + gen-plan §1.6 = pendance structurée ÉTEINTE Task 84 G3 (socle inscrit "
            "SHARED §7 v1.7.37 + gen-plan §1.6/§3 v3.42.0, mobilisation gen-plan déclarée — précédents v1.7.0 n°54 / "
            "Task 7-8 n°55)",
            "KB n°56 calibration pendance éteinte")

    # --- E. README corpus
    c = README_CORPUS.read_text(encoding="utf-8")
    c = sub(c, "> **Version** : 2.1.21", "> **Version** : 2.1.22", "corpus version")
    c = sub(c, "> **Architecture** : v2.2 — SHARED v1.7.36 — Contexte Système 3 niveaux",
            "> **Architecture** : v2.2 — SHARED v1.7.37 — Contexte Système 3 niveaux", "corpus architecture")
    c = sub(c, "> **Révision v2.1.21 (2026-11-08, Task 78/79 G1",
            "> **Révision v2.1.22 (2026-11-09, Task 84 G3 — session web-ecef7f80, directive propriétaire trace "
            "1a1bed51ccaf78f1 « continue »)** : gen-plan v3.41.0→v3.42.0 (INSCRIPTION SOCLE n°56 agent-engineering — "
            "SHARED §7 [définition + registre] v1.7.37 + gen-plan §1.6/§3, pendance P1 Task 83 éteinte ; PM v3.42.0 "
            "généré mécaniquement, delta verrouillé scripts/delta-genplan-v3420.json) ; SHARED v1.7.37 ; PM-INSTALL "
            "v1.9.14 ; propagation §0 v1.7.37 ; PM v3.41.0 archivé R4 @historique (sceau %s…) ; KB gen-plan v3.42.0 + "
            "KB n°56 mobilisation déclarée + pin ECO_SKILLS 3.42.0 ; ULTRA régénéré.\n"
            "> **Révision v2.1.21 (2026-11-08, Task 78/79 G1" % sha[:16],
            "corpus révision v2.1.22")
    c = sub(c, "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.41.0.md", "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.42.0.md",
            "corpus arborescence")

    # --- F. pins ECO_SKILLS ×2 arbres
    pin_new = ('"gen-plan": "3.42.0",  # KO-L004 (session web-ecef7f80 2026-11-09 — Task 84 G3 : v3.42.0 '
               'inscription socle discipline n°56 agent-engineering [SHARED §7 v1.7.37 + §1.6/§3 — pendance P1 '
               'Task 83 éteinte] ; précédent Task 78/79 G1 : v3.41.0 règle de sondage borné ; précédent Task 77 G2 :')
    pin_old = '"gen-plan": "3.41.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 78/79 G1 : v3.41.0 règle de sondage borné ; précédent Task 77 G2 :'
    p_r = PIN_REPO.read_text(encoding="utf-8")
    p_h = PIN_HOST.read_text(encoding="utf-8")
    p_r = sub(p_r, pin_old, pin_new, "pin dépôt")
    p_h = sub(p_h, pin_old, pin_new, "pin hôte")

    # --- G. RETRAITS_SANCTIONNES
    r = RETRAITS.read_text(encoding="utf-8")
    r = sub(r, '    "PROMPT-MAITRE-GEN-PLAN-v3.40.0.md",',
            '    "PROMPT-MAITRE-GEN-PLAN-v3.41.0.md",  # cascade gen-plan v3.42.0 (Task 84 G3 — inscription socle n°56)\n'
            '    "PROMPT-MAITRE-GEN-PLAN-v3.40.0.md",',
            "RETRAITS v3.41.0")

    # --- H. historiques-par-skill/agent-engineering.md — ligne socle
    # (note : le prétendu « typo §1 ission » était un artefact de transport —
    #  le fichier contient bien « §1 [mission » : liste entre crochets §1…fondements])
    h = HIST_AE.read_text(encoding="utf-8")
    h = h.rstrip("\n") + ("\n\n- **Socle inscrit** (Task 84 G3, 2026-11-09 — directive 1a1bed51ccaf78f1 « continue », "
                          "pendance P1 éteinte) : SHARED §7 (ligne définition + ligne registre d'assignation, "
                          "v1.7.37) + gen-plan §1.6/§3 (v3.42.0, mobilisation déclarée à l'entrée KB) ; PM "
                          "v3.42.0 généré (delta verrouillé scripts/delta-genplan-v3420.json), PM v3.41.0 archivé R4 "
                          "(sceau %s…).\n" % sha[:16])

    # --- écritures (tout validé en mémoire)
    SHARED.write_text(s, encoding="utf-8")
    README_HIST.write_text(a, encoding="utf-8")
    HIST_GP.write_text(b, encoding="utf-8")
    KB.write_text(k, encoding="utf-8")
    README_CORPUS.write_text(c, encoding="utf-8")
    PIN_REPO.write_text(p_r, encoding="utf-8")
    PIN_HOST.write_text(p_h, encoding="utf-8")
    RETRAITS.write_text(r, encoding="utf-8")
    HIST_AE.write_text(h, encoding="utf-8")
    print("Cascade écrite : SHARED révision §7 n°56 · README @historique (%d PMs, sceau %s…) · historiques gen-plan "
          "(vivante v3.42.0, %d versions) · KB gen-plan v3.42.0 + n°56 · README corpus v2.1.22 · pins ×2 3.42.0 · "
          "RETRAITS v3.41.0 · historique n°56 socle" % (total_4, sha[:16], v_doc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
