#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

task18-cascade-historique.py — Cascade documentaire KO-L004 (Task 18, web-fdf5963c).
Re-exécutable : chaque bloc est gardé (SKIP si déjà appliqué).
Discipline sub_locked (ABANDON sans écriture pour le bloc en cours).
"""
import hashlib
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(BASE, "skills", "@historique")
CORPUS = os.path.join(BASE, "skills", "@mon-ecosysteme")


def sub_locked(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        print("ABANDON : [%s] trouvé %d fois (attendu %d)" % (label, c, n))
        sys.exit(2)
    return text.replace(motif, remplace)


def sha_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def block(path, guard, fn):
    """Applique fn(texte) sur le fichier si le guard (marqueur du nouvel état) est absent."""
    t = open(path, encoding="utf-8").read()
    if guard in t:
        print("[SKIP] %s déjà à jour" % os.path.basename(path))
        return 0
    t2 = fn(t)
    open(path, "w", encoding="utf-8").write(t2)
    print("[OK] %s" % os.path.basename(path))
    return 1


def gen_plan_edits(t):
    t = sub_locked(t,
        "> **Version vivante (corpus)** : v3.23.1 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.1.md` (sa table §7 fait foi)",
        "> **Version vivante (corpus)** : v3.23.2 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.2.md` (sa table §7 fait foi)", 1, "gp vivante")
    t = sub_locked(t,
        "> **Versions archivées** : 18 PMs (v3.6.1 → v3.22.1)",
        "> **Versions archivées** : 19 PMs (v3.6.1 → v3.23.1)", 1, "gp archivées")
    t = sub_locked(t, "## Famille GEN-PLAN — 25 versions", "## Famille GEN-PLAN — 26 versions", 1, "gp count")
    t = sub_locked(t, "| **VERSION VIVANTE (corpus)** |",
                   "| supplantée par v3.23.2 le 2026-10-23 — archivée |", 1, "gp marker")
    anchor_row_start = "| v3.23.1 | 2026-10-12 | Correction outil + fusion discussion externe 468a4c26"
    idx = t.index(anchor_row_start)
    end_of_row = t.index("\n", idx)
    new_row = ("\n| v3.23.2 | 2026-10-23 | Optimisation du système d'installation (Task 18, session web-fdf5963c — "
               "directive propriétaire « optimise le système d'installation en regénérant » + prérequis A) : note §5 "
               "mécanisme dual — installation DIRECTE des formes certifiées du dépôt par défaut (PM-INSTALL v1.8.0 §3.2, "
               "exécutant canonique eco_install_pipeline.py) ; l'assemblage §5 demeure la spécification de la forme et la "
               "voie bootstrap corpus-seul ; recalibrage croisé SHARED v1.7.8 / PM-INSTALL v1.7.2→v1.8.0 | La documentation "
               "d'installation reflète la pratique certifiée (formes du dépôt arbitrées) sans changer le comportement du "
               "skill — PATCH documentation — **VERSION VIVANTE (corpus)** |")
    t = t[:end_of_row] + new_row + t[end_of_row:]
    t = sub_locked(t,
        "v3.6.1, v3.7.0, v3.8.0, v3.8.1, v3.9.0, v3.10.0, v3.11.0, v3.12.0, v3.13.0, v3.16.0, v3.17.0, v3.17.1, v3.17.2, v3.18.0, v3.19.0, v3.21.0, v3.22.0, v3.22.1 (18 fichiers, SHA-256 au §5)",
        "v3.6.1, v3.7.0, v3.8.0, v3.8.1, v3.9.0, v3.10.0, v3.11.0, v3.12.0, v3.13.0, v3.16.0, v3.17.0, v3.17.1, v3.17.2, v3.18.0, v3.19.0, v3.21.0, v3.22.0, v3.22.1, v3.23.1 (19 fichiers, SHA-256 au §5)",
        1, "gp footer")
    return t


def correct_work_edits(t):
    t = sub_locked(t,
        "> **Version vivante (corpus)** : v2.7.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` (sa table §7 fait foi)",
        "> **Version vivante (corpus)** : v2.8.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md` (sa table §7 fait foi)", 1, "cw vivante")
    t = sub_locked(t,
        "> **Versions archivées** : 4 PMs (v2.4.0 → v2.6.0)",
        "> **Versions archivées** : 5 PMs (v2.4.0 → v2.7.0)", 1, "cw archivées")
    t = sub_locked(t, "## Famille CORRECT-WORK — 10 versions", "## Famille CORRECT-WORK — 11 versions", 1, "cw count")
    t = sub_locked(t, "**VERSION VIVANTE (corpus)** |",
                   "supplantée par v2.8.0 le 2026-10-23 — archivée |", 1, "cw marker")
    anchor_row_start = "| v2.7.0 | 2026-10-02 |"
    idx = t.index(anchor_row_start)
    end_of_row = t.index("\n", idx)
    new_row = ("\n| v2.8.0 | 2026-10-23 | Intégration alias-eco + mécanisme dual (Task 18, session web-fdf5963c — directive "
               "propriétaire : registre d'alias $<ALIAS>) : mode PROJET — délégation de la tenue du registre des phrases "
               "récurrentes à alias-eco >= v1.0.0 (§10.1 Phase 2, registre @historique/@Alias/) ; dependencies §4/§2.2 += "
               "alias-eco ; §3 Relations += alias-eco ; note §5 mécanisme dual (installation directe des formes certifiées "
               "par défaut — PM-INSTALL v1.8.0 §3.2) ; PM v2.8.0 généré mécaniquement KO-L004 (complétion agent 5 "
               "substitutions verrouillées) ; recalibrage croisé SHARED v1.7.8 / PM-INSTALL v1.7.2→v1.8.0 | La vérification "
               "PROJET tient automatiquement le registre des phrases récurrentes de la discussion analysée (délégation "
               "bidirectionnelle KB) — MINOR intégration fonctionnelle — **VERSION VIVANTE (corpus)** |")
    t = t[:end_of_row] + new_row + t[end_of_row:]
    t = sub_locked(t,
        "`prompts-maitres/correct-work/` — v2.4.0, v2.5.0, v2.5.1, v2.6.0 (4 fichiers, SHA-256 au §5)",
        "`prompts-maitres/correct-work/` — v2.4.0, v2.5.0, v2.5.1, v2.6.0, v2.7.0 (5 fichiers, SHA-256 au §5)",
        1, "cw footer")
    return t


def clone_chat_edits(t):
    t = sub_locked(t,
        "> **Version vivante (corpus)** : v2.0.1 — `skills/@mon-ecosysteme/PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md` (sa table §7 fait foi)",
        "> **Version vivante (corpus)** : v2.0.2 — `skills/@mon-ecosysteme/PROMPT-MAITRE-CLONE-CHAT-v2.0.2.md` (sa table §7 fait foi)", 1, "cc vivante")
    t = sub_locked(t,
        "> **Versions archivées** : 1 PM (v2.0.0) dans `prompts-maitres/clone-chat/` — `git mv` byte-identité R4 (Task 12, 2026-10-12)",
        "> **Versions archivées** : 2 PMs (v2.0.0, v2.0.1) dans `prompts-maitres/clone-chat/` — `git mv` byte-identité R4 (Task 12 2026-10-12, Task 18 2026-10-23)",
        1, "cc archivées")
    t = sub_locked(t, "## Famille CLONE-CHAT — 5 versions", "## Famille CLONE-CHAT — 6 versions", 1, "cc count")
    t = sub_locked(t, "**VERSION VIVANTE (corpus)** |",
                   "supplantée par v2.0.2 le 2026-10-23 — archivée |", 1, "cc marker")
    anchor_row_start = "| v2.0.1 | 2026-10-12 |"
    idx = t.index(anchor_row_start)
    end_of_row = t.index("\n", idx)
    new_row = ("\n| v2.0.2 | 2026-10-23 | Optimisation du système d'installation (Task 18, session web-fdf5963c — directive "
               "propriétaire) : note §5 mécanisme dual — installation DIRECTE des formes certifiées du dépôt par défaut "
               "(PM-INSTALL v1.8.0 §3.2) ; l'assemblage §5 demeure la spécification de la forme et la voie bootstrap "
               "corpus-seul ; PM v2.0.2 généré mécaniquement KO-L004 (complétion agent) ; recalibrage croisé SHARED v1.7.8 / "
               "PM-INSTALL v1.7.2→v1.8.0 | Documentation d'installation alignée sur la pratique certifiée — PATCH "
               "documentation — **VERSION VIVANTE (corpus)** |")
    t = t[:end_of_row] + new_row + t[end_of_row:]
    t = sub_locked(t,
        "Fichiers archivés de la famille : aucun (v2.0.0 est la version vivante depuis sa création — la lignée v1.x n'a jamais été matérialisée au corpus).",
        "Fichiers archivés de la famille : `prompts-maitres/clone-chat/` — v2.0.0, v2.0.1 (2 fichiers, SHA-256 au §5).",
        1, "cc footer")
    return t


def refactor_guard_edits(t):
    anchor_row_start = "| v1.7.0 | 2026-10-12 |"
    idx = t.index(anchor_row_start)
    end_of_row = t.index("\n", idx)
    new_row = ("\n| v1.7.1 | 2026-10-23 | Optimisation du système d'installation (Task 18, session web-fdf5963c) : note §5 "
               "mécanisme dual explicitant la cohérence de ce §5 avec PM-INSTALL v1.8.0 §3.2 (ce §5 prescrit DÉJÀ "
               "l'installation directe par copie des formes certifiées — voie par défaut ; l'assemblage depuis le corpus "
               "demeure la voie bootstrap) ; PM v1.7.1 généré mécaniquement KO-L004 (complétion agent) ; recalibrage croisé "
               "SHARED v1.7.8 / PM-INSTALL v1.7.2→v1.8.0 ; PM v1.7.0 archivé `prompts-maitres/refactor-guard/` (git mv "
               "byte-identité R4) | Première montée mécanique de la 4e famille — **VERSION VIVANTE (corpus)** |")
    return t[:end_of_row] + new_row + t[end_of_row:]


def autres_elements_edits(t):
    t = sub_locked(t, "| v1.7.4 | 2026-10-12 |",
        "| v1.7.8 | 2026-10-23 | §6.1 — référence(s) PM portée(s) aux 4 versions générées mécaniquement (gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1) + référence PM-INSTALL portée à v1.8.0 (mécanisme dual d'installation + périmètre alias-eco — Task 18, session web-fdf5963c) ; complétion de la ligne de révision |\n| v1.7.4 | 2026-10-12 |",
        1, "ae SHARED")
    t = sub_locked(t, "> **Révision v1.4.9 (2026-10-12, Task 12", "XX-NEVER-XX", 1, "ae SYNC-format") if False else t
    t = sub_locked(t, "| v1.4.7 | 2026-10-12 | Révision Task 8",
        "| v1.5.0 | 2026-10-23 | Cascade Task 18 (session web-fdf5963c, KO-L004) : 4 PMs familles régénérés mécaniquement (gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1 — note §5 mécanisme dual) ; PM-INSTALL v1.7.2→v1.8.0 ; SHARED v1.7.8 ; propagation marqueur §0 v1.7.7→v1.7.8 exécutée (100 skills + 69 scripts + 2 agents, idempotent) ; skill alias-eco v1.0.0 créé (registre @historique/@Alias/ — état vivant) ; KB 34 entrées ; ULTRA régénéré ; archive rescellée round-trip 9/9 |\n| v1.4.7 | 2026-10-12 | Révision Task 8",
        1, "ae SYNC")
    t = sub_locked(t, "| v1.1.0 | 2026-10-02 | Fusion des installateurs",
        "| v1.8.0 | 2026-10-23 | MÉCANISME DUAL d'installation (§3.2 réécrit : installation directe des formes certifiées du dépôt = voie par défaut, exécutant canonique eco_install_pipeline.py ; assemblage bootstrap corpus-seul) + intégration alias-eco (§2bis/§4/§A.3) — Task 18, session web-fdf5963c, directive propriétaire « optimise le système d'installation en regénérant » + prérequis A |\n| v1.7.2 | 2026-10-23 | Génération mécanique KO-L004 des 4 PMs familles (gen-plan v3.23.2 · correct-work v2.8.0 · clone-chat v2.0.2 · refactor-guard v1.7.1) — recalibrage croisé §2ter/§A.3 ; SHARED v1.7.8 |\n| v1.1.0 | 2026-10-02 | Fusion des installateurs",
        1, "ae PM-INSTALL")
    t = sub_locked(t, "Registre à 30 entrées — instantané des versions archivé ci-dessous (source : registre KB, instantané rafraîchi 2026-10-12 matérialisation n°55 ; le registre vivant fait foi ; les versions des 3 familles = versions de leurs PMs vivants, contrat KO-L004).",
        "Registre à 34 entrées — instantané des versions archivé ci-dessous (source : registre KB, instantané rafraîchi 2026-10-23 Task 18 — alias-eco v1.0.0 créé, 4 familles montées ; le registre vivant fait foi ; les versions des 4 familles = versions de leurs PMs vivants, contrat KO-L004).",
        1, "ae KB count")
    t = sub_locked(t, "| gen-plan | v3.23.0 | audit-provenance | v1.1.0 |",
                   "| gen-plan | v3.23.2 | audit-provenance | v1.1.0 |", 1, "ae KB gp")
    t = sub_locked(t, "| correct-work | v2.7.0 | autonomous-agent | v1.1.0 |",
                   "| correct-work | v2.8.0 | autonomous-agent | v1.1.0 |", 1, "ae KB cw")
    t = sub_locked(t, "| clone-chat | v2.0.0 | correct-py | v1.1.0 |",
                   "| clone-chat | v2.0.2 | correct-py | v1.1.0 |", 1, "ae KB cc")
    t = sub_locked(t, "| refactor-guard | v1.7.0 | fullstack-dev | v1.0.0 |",
                   "| refactor-guard | v1.7.1 | fullstack-dev | v1.0.0 |\n| alias-eco | v1.0.0 | dessin-technique | v1.1.1 |", 1, "ae KB rg+ae")
    return t


def hist_readme_edits(t):
    t = sub_locked(t, "> **Version** : 1.1.0", "> **Version** : 1.2.0", 1, "hREADME version")
    t = sub_locked(t,
        "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 25 (v2.0.0 → v3.23.0) | 18 (v3.6.1 → v3.22.1) | v3.22.1 |",
        "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 26 (v2.0.0 → v3.23.2) | 19 (v3.6.1 → v3.23.1) | v3.23.2 |",
        1, "hREADME gp")
    t = sub_locked(t,
        "| CORRECT-WORK | correct-work — vérification/correction (5 étapes, 4 modes) | 10 (v1.0.0 → v2.7.0) | 4 (v2.4.0 → v2.6.0) | v2.7.0 |",
        "| CORRECT-WORK | correct-work — vérification/correction (5 étapes, 4 modes) | 11 (v1.0.0 → v2.8.0) | 5 (v2.4.0 → v2.7.0) | v2.8.0 |",
        1, "hREADME cw")
    t = sub_locked(t,
        "| CLONE-CHAT | clone-chat — archivage de session (7+1 étapes, 8 checks) | 4 (v1.0.0 → v2.0.0) | 0 (v2.0.0 vit dès sa création) | v2.0.0 |",
        "| CLONE-CHAT | clone-chat — archivage de session (7+1 étapes, 8 checks) | 6 (v1.0.0 → v2.0.2) | 2 (v2.0.0, v2.0.1) | v2.0.2 |\n| REFACTOR-GUARD | refactor-guard — garde-fous de refactoring (H01-H15, échelle rollout) | 2 (v1.7.0 → v1.7.1) | 1 (v1.7.0) | v1.7.1 |",
        1, "hREADME cc+rg")
    t = sub_locked(t,
        "| `historique-autres-elements.md` | Historique du socle sans famille à PM :",
        "| `@Alias/aliases.json` | **Registre VIVANT** du système d'alias `$<ALIAS>` (skill alias-eco v1.0.0, Task 18 2026-10-23) — phrases récurrentes triées alphabétiquement, dédupliquées ; ÉTAT VIVANT non scellé (mis à jour à chaque scan/analyse correct-work PROJET) — les règles de conservation R2/R4 du présent dossier ne s'y appliquent PAS (il n'est pas une archive scellée) |\n| `historique-autres-elements.md` | Historique du socle sans famille à PM :",
        1, "hREADME @Alias")
    t = sub_locked(t, "## 5. Index des fichiers sources archivés (21 PMs — sceau SHA-256)",
                   "## 5. Index des fichiers sources archivés (25 PMs — sceau SHA-256)", 1, "hREADME §5 count")
    shas = []
    for fam, f in [("gen-plan", "PROMPT-MAITRE-GEN-PLAN-v3.23.1.md"),
                   ("correct-work", "PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md"),
                   ("clone-chat", "PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md"),
                   ("refactor-guard", "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md")]:
        shas.append((fam, f, sha_of(os.path.join(HIST, "prompts-maitres", fam, f))))
    anchor = "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md |"
    idx = t.index(anchor)
    new_rows = "".join("| %s/%s | %s |\n" % (fam, f, s) for fam, f, s in shas)
    return t[:idx] + new_rows + t[idx:]


def corpus_readme_edits(t):
    t = sub_locked(t, "> **Version** : 2.1.7", "> **Version** : 2.1.8", 1, "cREADME version")
    t = sub_locked(t, "> **Architecture** : v2.2 — SHARED v1.7.7 — Contexte Système 3 niveaux",
                   "> **Architecture** : v2.2 — SHARED v1.7.8 — Contexte Système 3 niveaux", 1, "cREADME arch")
    t = sub_locked(t, "> **Révision v2.1.7 (2026-10-12, Task 12",
        "> **Révision v2.1.8 (2026-10-23, Task 18 — session web-fdf5963c, directive propriétaire « optimise le système d'installation en regénérant » + skill alias-eco)** : 4 PMs familles régénérés mécaniquement KO-L004 (GEN-PLAN v3.23.2, CORRECT-WORK v2.8.0 — intégration alias-eco mode PROJET, CLONE-CHAT v2.0.2, REFACTOR-GUARD v1.7.1 — note §5 mécanisme dual) ; PM-INSTALL v1.8.0 (MÉCANISME DUAL : installation directe des formes certifiées par défaut — exécutant canonique eco_install_pipeline.py ; assemblage bootstrap ; périmètre += alias-eco §2bis/§4/§A.3) ; SHARED v1.7.8 ; skill alias-eco v1.0.0 créé (registre d'alias $<ALIAS>, déclencheurs « alias-eco »/« liste mes alias »/« alias-eco (chat) », registre @historique/@Alias/) ; KB 34 entrées ; cascade KO-L004 : propagate v1.7.8 (100 skills + 69 scripts + 2 agents), ULTRA régénéré, arbitres recalibrés, archive rescellée round-trip 9/9 ; arborescence §2 recalibrée.\n> **Révision v2.1.7 (2026-10-12, Task 12",
        1, "cREADME révision")
    t = sub_locked(t, "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.23.1.md", "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.23.2.md", 1, "cREADME gp")
    t = sub_locked(t, "│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md", "│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md", 1, "cREADME cw")
    t = sub_locked(t, "│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md", "│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.2.md", 1, "cREADME cc")
    t = sub_locked(t, "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md  ← 4e famille (décision D009)",
                   "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md  ← 4e famille (décision D009)", 1, "cREADME rg")
    t = sub_locked(t, "│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md  ← Installation (source unique v1.7.1 — pipeline 11 étapes)",
                   "│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md  ← Installation (source unique v1.8.0 — pipeline 11 étapes, mécanisme dual)", 1, "cREADME install")
    return t


def sync_context_edits(t):
    t = sub_locked(t, "> **Version** : 1.4.9", "> **Version** : 1.5.0", 1, "SC version")
    t = sub_locked(t, "> **Date** : 2026-10-12", "> **Date** : 2026-10-23", 1, "SC date")
    t = sub_locked(t, "> **Révision v1.4.9 (2026-10-12, Task 12",
        "> **Révision v1.5.0 (2026-10-23, cascade Task 18 — session web-fdf5963c, KO-L004)** : état du corpus recalibré — 4 PMs familles régénérés mécaniquement (gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1 — note §5 mécanisme dual), PMs supplantés archivés `git mv` byte-identité R4 (4 PMs : v3.23.1, v2.7.0, v2.0.1, v1.7.0) ; PM-INSTALL v1.7.2→v1.8.0 (mécanisme dual + périmètre alias-eco) ; SHARED v1.7.7→v1.7.8 ; propagation du marqueur §0 v1.7.7→v1.7.8 exécutée (100 skills + 69 scripts + 2 agents, idempotent) ; skill alias-eco v1.0.0 créé (registre @historique/@Alias/ — ÉTAT VIVANT, non-cible de la resynchronisation) ; KB 34 entrées ; ULTRA régénéré (SHA dérivé KB) ; arbitres recalibrés (ECO_SKILLS += alias-eco + 4 montées) ; archive rescellée round-trip 9/9.\n> **Révision v1.4.9 (2026-10-12, Task 12",
        1, "SC révision")
    return t


def main():
    blocks = [
        (os.path.join(HIST, "historiques-par-skill", "gen-plan.md"), "vivante (corpus)** : v3.23.2", gen_plan_edits),
        (os.path.join(HIST, "historiques-par-skill", "correct-work.md"), "vivante (corpus)** : v2.8.0", correct_work_edits),
        (os.path.join(HIST, "historiques-par-skill", "clone-chat.md"), "vivante (corpus)** : v2.0.2", clone_chat_edits),
        (os.path.join(HIST, "historiques-par-skill", "refactor-guard.md"), "| v1.7.1 | 2026-10-23 |", refactor_guard_edits),
        (os.path.join(HIST, "historique-autres-elements.md"), "Registre à 34 entrées", autres_elements_edits),
        (os.path.join(HIST, "README.md"), "> **Version** : 1.2.0", hist_readme_edits),
        (os.path.join(CORPUS, "README.md"), "> **Version** : 2.1.8", corpus_readme_edits),
        (os.path.join(CORPUS, "SYNC-CONTEXT.md"), "> **Version** : 1.5.0", sync_context_edits),
    ]
    done = 0
    for path, guard, fn in blocks:
        done += block(path, guard, fn)
    print("CASCADE HISTORIQUE OK — %d/%d blocs appliqués" % (done, len(blocks)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
