#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""Task 72 G1 SG1.2 — résumés opérationnels NOUVEAUX (module de constantes, v4 finale).

Textes INÉDITS remplaçant inline les 9 blocs déplacés R4 vers references/ (aucune
duplication — D004) ; chaque résumé conserve le(s) titre(s) de section (marqueurs de
borne du remplaçeur) et l'essentiel d'exécution (commandes, valeurs, seuils) ; le
détail intégral est chargé à la demande (progressive disclosure — étude Task 70 R1).
Budget D002 : additions nettes <= ~8,5 Kio (SKILL.md cible < 30 Kio).
"""

RESUME_JOURNAL = """### §5.6 Journal des versions (entrée courante — archive intégrale et mécanique de migration : `references/journal-versions.md`)

- **v3.39.0 (2026-11-08, session web-ecef7f80 — Task 72 G1, directives « Chantier R1 : re-curation progressive disclosure de gen-plan » + complémentaire 1a1b7b297b7b4975)** : 9 blocs déplacés R4 byte-identité vers `references/` (journal · règles d'or + KO · disciplines · protocoles) + append contingences (grille-token.md) — résumés NOUVEAUX inline, aucune duplication ; contrats certifiés baseline golden master + vérif POST (T1.1.0 — scripts/task72-baseline-verifier.py) ; lecture ciblée = état par défaut (E5-POIDS). MINOR. Cascade KO-L004 complète (SG1.4 — worklog Task 72)."""

RESUME_MODE_STEP = """### §5.5 Mode step — structure hiérarchique et état d'avancement (résumé — intégral : `references/protocoles-detailles.md`)

**Couche d'organisation transverse (v3.25.0, tous modes depuis v3.36.0 — seule différence : les portes de confirmation)** : **groupe `G<k>`** (unité de vérification — correct-work(groupe)) → **sous-groupes `SG<k>.<j>`** (lot cohérent 2-5 tâches) → **tâches `T<k>.<j>.<i>`** (unité élémentaire, tag #token). **Statuts dérivés de l'état vérifiable** (KO-L003) : `[À FAIRE]` · `[EN COURS]` · `[TERMINÉ]` · `[BLOQUÉ]` · `[REPORTÉ]` ; compteurs n/m. **Cadence** : ouverture de groupe → PLAN-AFFICHE d'évolution puis tableau du groupe (step-ok : après confirmation) ; fin de tâche → ligne + compteurs ; fin de sous-groupe → rappel ; clôture → tableau final + verdict correct-work(groupe). **Orthogonal à l'exécution** : couche de LECTURE ; Graph Diamond automatique dès preuve d'indépendance (même à travers les sous-groupes, série = exception tracée) ; groupes plats normalisés à l'ouverture (R6/R2)."""

RESUME_CONTINGENCES = """- **Coefficients de contingence (détail et preuves : `references/grille-token.md`)** : **profil frais local ×3-4** (première exécution sur profil restauré — coût de DÉCOUVERTE hors grilles calibrées, v3.28.1) ; **appels API en masse ×2-3** (429/backoff — ThreadPool 2-4 workers, throttle 1-2 s, reprise par lots, petits d'abord) ; **récupération externe bloquée ×3-4** (WAF/SPA/rate-limit — escalade WebFetch → curl → agent-browser → z-ai `page_reader`, budget propre AVANT l'étape requérante, v3.28.2)."""

RESUME_ROUTAGE = """### §1.16 Routage de découverte des skills + garde d'installation (résumé — intégral : `references/protocoles-detailles.md`)

- **É1-INSTALL — garde avec PRÉEMPTION** : à l'ouverture de session, AVANT E1 : `python3 skills/gen-plan/scripts/ensure-installed.py --check` (chemin canonique). rc=0 → no-op ; rc≠0 → suspension de toute tâche + `--reinstall` (pipeline PM-INSTALL, clone éphémère) AVANT toute autre étape ; directive post-réinstallation intégrée au plan ; idempotente. **v3.35.2** : contrôle du SKILL.md de TOUTES les entrées KB (dérivation dynamique) ; skills KB manquants → AUTO-RÉPARÉS depuis le miroir `KNOWLEDGE-repo/` (INSTALLE-REPARÉ, rc=0, trace worklog).
- **Routage (E5)** : skills-inventory en PRIORITÉ (`generate_skills_md.py --json`/`--search`/`--category`, comparaison mémorisée au KB) ; skill-finder-cn en FALLBACK si échec — contrôle `audit-provenance` AVANT adoption ; bascule unidirectionnelle."""

RESUME_LECONS = """### §1.14 Leçons knowledge-observer — économie API et arbitres (résumé — intégral : `references/regles-or.md`)

- **KO-L001 — Économie API (429)** : une seule sonde par message utilisateur, travail local 100 % entre les sondes, suites armées à QUOTA_OK (`--skip-done`) ; pas d'attente en-tour.
- **KO-L003 — Arbitres à invariants dynamisés** : invariants dérivés de l'état courant, jamais figés ; divergence → dynamiser l'arbitre + re-verdict honnête, jamais ajuster la réalité.

### §1.15 Leçons knowledge-observer — recalibrage croisé (résumé — intégral : `references/regles-or.md`)

- **KO-L004 — Recalibrage croisé + génération PM** : toute montée de version → AVANT certification : recalibrage des outils dépendants (arbitres, pre-checks, skills-meta, run-order, SYNC_MAP, miroir, archive) + génération mécanique du PM (`scripts/generer-pm-skill.py --generate <skill>`, substitutions verrouillées, anti-rétrogradation R2).
- **KO-L007 — Matérialisation d'abord** : `git sparse-checkout list` + test d'existence AVANT toute écriture et tout verdict naïf ; « non matérialisé » ≠ « échec ».

> Saut §1.8 → §1.14 intentionnel (Task 21 A7) ; provenance : `references/regles-or.md`."""

RESUME_DISCIPLINES = """### §1.6 Disciplines d'ingénierie de prompts (résumé — tables intégrales : `references/disciplines-mobilisation.md`)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED d'abord ; lecture par blocs + synthèses |
| **Loop engineering** | Boucle E10-E13 ; auto-calibration E15 |
| **Graph engineering** | KB = graphe bidirectionnel versionné ; matrice agent × skill |
| **Harness engineering** | Profils + signaux ; hook E8 + contrôle par phase ; worklog |
| **Refactoring engineering** | Discipline n°55 : opérations préservant le comportement observable ; garde-fous refactor-guard |
| **Refactoring test** | Outil n°55 (anti-auto-certification) : évaluation + blast radius, verdict OK/PRESSION/CRITIQUE |

- **Mobilisation** : tables E1-E8, n°54, n°55, E15, par déclencheur × modes — intégrales : `references/disciplines-mobilisation.md` ; socle commun (context/loop/graph/harness + PEK) à TOUT déclencheur du §A. **Hook continu E9-E14** : G-RES re-collecté à chaque checkpoint E11 et entre les vagues ; PRESSION → ECO, CRITIQUE → série/PAUSE. gen-plan = détenteur principal de la méthode prompt-engineering (SHARED §7 ; PEK v4.1 — `references/prompt-engineering-kit.md`)."""

RESUME_REGLES = """### §1.5 Règles d'or (résumé opérationnel — intégral : `references/regles-or.md` ; miroir SHARED §9)

| N° | Règle | Portée |
|----|-------|--------|
| 1 | **Adaptation autonome** | Blocage = adaptation journalisée, jamais d'arrêt implicite ; pause explicite si inatteignable. |
| 2 | **Régénération post-installation** | Écosystème installé → plan re-généré via le gen-plan installé (R2). |
| 3 | **Mise à jour à chaque demande** | E13 (extension, jamais réécriture) ; « intègre dans le plan d'actions » = extension en place ; « met à jour » = NOUVEAU plan consolidé $FACON2. |
| — | **Modes** | `step` : chaîne par groupes ; `step-ok` : + confirmation ; NULL : comportement antérieur ; autre mode → clarification (R2). |
| 4 | **Dépôt par clone** | Clone git local, jamais de lecture distante ; jeton éphémère jamais persisté ; publication = validation propriétaire. |
| 5 | **État vérifiable** | Chiffres et statuts du disque, jamais pré-écrits (KO-L003) ; dépôt = source R4. |
| 6 | **Langue française** | Tout texte de l'agent en français dès le premier mot ; dérive → correction + worklog + durcissement. |
| 7 | **Mémoire complète** | Oubli de coupure → relire clones/sauvegardes avant (re-)génération. |
| 8 | **Formes installées** | PM INSTALL installe `skills/<skill>/` uniquement ; prompts maîtres jamais installés. |
| 9 | **Vérification d'installation** | Garde mécanique à toute invocation ; rétablissement auto puis re-génération du plan. |
| KO | **KO-L005** | gen-plan modifiée et validée → re-génération du plan (arbitres → montée → L004 → E8). |
| KO | **KO-L009** | Secret exposé : jamais utiliser ; révocation immédiate ; push = propriétaire, jamais l'agent. |"""

RESUME_PHILO4 = """4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** (v3.24.0/v3.32.0) — vagues indépendantes prouvées en PARALLÈLE : Graph Diamond automatique (E9-E14), série = exception tracée ; dégradation gracieuse 429 — intégral : `references/protocoles-detailles.md` (#4)."""

RESUME_E1RES_E7DISP = """<!-- RÉSUMÉ v3.39.0 — protocoles intégraux (R4) : references/protocoles-detailles.md -->

**Hook E1-RES — ouverture de session (4 vérifications AVANT toute analyse)** : (1) lecture seule préalable B-11 (worklog/plan/arbitres) ; (2) collecte G-RES (`monitor.py --state-file tmp/resource-monitor-state.json` : OK/PRESSION/CRITIQUE → mode, journalisé) ; (3) fraîcheur du plan (gen-plan modifiée et valide → re-généré avant reprise) ; (4) garde post-coupure (règle d'or n°9 : piliers + integrity → rétablissement auto). **Reprise (v3.27.0)** : message pendant un plan en vol → worklog + fraîcheur + E13 + re-validation E8 + R5 + affichage ; l'état « en vol » dérive du DISQUE (RC3).

**Hook E7-DISP — affichage obligatoire (5 points, garde bloquante)** : (1) plan écrit `download/` ; (2) answer key >= 1 décision vérifiable ; (3) validation E8 aux horodatages COUPLÉS (toute écriture = re-validation) ; (4) worklog R5 + marqueur `PLAN-AFFICHE` ; (5) bloc récapitulatif AFFICHÉ au chat. Garde : `check_plan_protocol.py --plan <plan.md> --worklog worklog.md` (P1-P5). **Affichage REJOUABLE** (jamais présumé). **Ouverture d'étape (v3.36.0, tous modes)** : PLAN-AFFICHE au début de chaque groupe G<k> (vue d'évolution, statuts du disque) ; step-ok : après confirmation."""

ARBRE = """```
skills/gen-plan/
├── SKILL.md                          # < 30 Kio — progressive disclosure (v3.39.0)
├── scripts/
│   ├── ensure-installed.py           # É1-INSTALL — préemption (v3.35.2)
│   └── check_plan_protocol.py        # Arbitre E7-DISP — P1-P5 (v3.27.0)
├── references/
│   ├── etapes-detaillees.md          # 15 étapes + mode step
│   ├── grille-token.md               # Grille #token + contingences (v3.39.0)
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   ├── guide-selection-agent-skill.md # Arbre de décision
│   ├── prompt-engineering-kit.md     # PEK v4.1
│   ├── patterns-avances-qwen.md      # 5 patterns (N19)
│   ├── answer-key-b12.md             # Registre réel (N19)
│   ├── answer-key-template.md        # Schéma Answer Key (N20)
│   ├── graph-diamond-pattern.md      # Parallélisation par défaut
│   ├── observation-patterns.md       # Task Observer (N20)
│   ├── regles-or.md                  # Règles d'or + KO — intégraux (v3.39.0)
│   ├── disciplines-mobilisation.md   # Tables de mobilisation (v3.39.0)
│   ├── protocoles-detailles.md       # E1-RES/E7-DISP/§1.16/§5.5/#4 (v3.39.0)
│   └── journal-versions.md           # Journal — archive (v3.39.0)
└── evals/
    ├── evals.json                    # 9 evals
    └── trigger_evals.json            # 15 cas
```"""
