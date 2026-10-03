# Rapport — Test robuste de fonctionnement de l'écosystème

> **Session** : web-8a7e5653 · Task 15 / Phase P4 · 2026-10-02
> **Méthode** : flotte M1 SUPERVISOR (fleet-engineering §1.6) × micro-specs SDD (M1-M5) × Graph Diamond (4 phases) — 3 agents spécialisés en parallèle, agrégation arbitrée
> **Arbitre mécanique** : `scripts/test-fonctionnement-robuste.py` (65 checks — rapports : `scripts/robust-test-report.json`, specs et rapports workers : `tmp/robust-test/`)

---

## 1. Conception du test — disciplines, techniques et protocoles mobilisés

Le test robuste exigé par la directive (« tâches en parallèle, utilisation d'agents spécialisés et utilisation du maximum des disciplines, techniques et protocoles de conception de plan d'actions ») a été conçu comme une **mission réelle de flotte** plutôt qu'un test cosmétique : l'écosystème a été mis à l'épreuve en l'utilisant pour s'auditer lui-même. Le **pattern M1 SUPERVISOR** (fleet-engineering §1.2) a été choisi et documenté avant lancement (règle §1.4-1) : un superviseur (Main, Task 15) et trois workers spécialisés indépendants, avec points de fusion clairs et arbitrage central — les cinq patterns alternatifs (FAN-OUT pur, PIPELINE, DEBATE, SWARM) étant moins adaptés à trois audits symétriques à agréger.

Le protocole complet a enchaîné : **spec-driven development** (M1 SPÉCIFIER — trois micro-specs versionnées 1.0.0 avec objectif, hors-périmètre, exigences E1-E5, critères d'acceptation mécaniques C1-C5, constitution ; M2 DÉCOMPOSER — Task IDs 15-W1/W2/W3, bornes ≤ 150 lignes par rapport, verrou mono-writer sur le worklog) ; **harness-engineering** (re-verdict G-RES du moniteur de ressources avant la vague — verdict OK, niveaux 0 ; bornes de coût et de timeout par sous-tâche ; critères de sortie = arbitres) ; **Graph Diamond** (phase 1 Décomposition avec preuve d'indépendance — trois livrables distincts, zéro écriture partagée ; phase 2 Exécution parallèle — les trois agents lancés en un seul message multi-outils ; phase 3 Synthèse ; phase 4 Vérification globale) ; **context-engineering** (prompts workers auto-contenus, budget d'attention borné) ; **memory-engineering** (État Long = specs persistées + worklog consolidé par le superviseur ; États Courts = contextes des agents, morts avec eux) ; **answer key** (décisions D001-D012 de session) ; **boucle loop-engineering E12-E13** (deux corrections d'arbitre en P1, une en P3, une en P4) ; **hooks correct-work** (verdict par worker + mode CIBLE sur les rapports + mode PROJET final) ; **knowledge-observer/Task Observer** (observation E15). Douze disciplines/protocoles au total, chacun pointant un artefact vérifiable (checklist mécanique de l'arbitre : 12/12 PASS).

## 2. Exécution — la vague parallèle

Trois agents spécialisés de type Explore (modèle GLM-5.3) ont été lancés **simultanément** dans un unique message multi-outils, chacun portant sa micro-spec, son Task ID, ses bornes et l'obligation d'un livrable au format imposé (vérifiable mécaniquement) :

| Task ID | Mission (micro-spec) | Livrable | Verdict |
|---|---|---|---|
| **15-W1** | Audit du corpus `@mon-ecosysteme/` — lignées de PMs, en-têtes, références croisées SHARED §6.1, orchestrateur ULTRA, README | `tmp/robust-test/rapport-15-W1.md` | **PASS AVEC RÉSERVES** (0 S1, 0 S2, 4 S3, 4 S4) |
| **15-W2** | Audit de l'outillage `scripts/` — compilabilité 32/32, arbitres exécutables, traçabilité PROVENANCE, manifeste d'intégrité, moniteur, garde anti-doublons | `tmp/robust-test/rapport-15-W2.md` | **PASS AVEC RÉSERVES** (0 S1, 1 S2, 1 S3, 4 S4) |
| **15-W3** | Audit du registre KB + skills installés — 21 entrées, bidirectionnalité des arêtes, cohérence versions, skills famille, évals | `tmp/robust-test/rapport-15-W3.md` | **PASS AVEC RÉSERVES** (0 S1, 0 S2, 3 S3, 1 S4) |

La vérification mécanique des livrables (SDD M4 — l'arbitre `test-fonctionnement-robuste.py`) confirme : sections obligatoires présentes 3/3, verdicts valides 3/3, constats numérotés avec sévérités 3/3, bilans en prose 3/3, tailles bornées 3/3, checklist disciplines 12/12 — **65/65 checks PASS**, rapport déterministe (idempotence prouvée : SHA identique sur deux exécutions). Aucune collision de fichier (vérifiée en phase 3 du Diamond), worklog resté mono-writer (consolidation superviseur), démobilisation complète de la flotte après agrégation (fleet §1.6.6).

## 3. Agrégation et arbitrage des constats divergents (M4 sur pièces)

L'agrégation (fleet §1.6.4) a consolidé 13 constats de workers, dont **un a été arbitré sur pièces et rejeté** :

- **W1-#4 REJETÉ (faux positif)** — W1 affirmait que `skills/loop-engineering/` et `skills/autonomous-agent/` étaient « absents du skills/ live ». Contre-preuves : (1) le listing de session montre les deux répertoires présents ; (2) la commande de contre-vérification du superviseur les confirme ; (3) W3, de son côté, relève « 21/21 répertoires présents » et « 5/5 skills famille installés ». Le constat est reclassé faux positif (métrique correct-work §2.8 : 1 faux positif / 13 constats = 7,7 % < 10 % — conforme).
- **W2-S2 ACCEPÉ (constat majeur nouveau)** — régression de la convention N27 : seuls **9/32 scripts** portent l'en-tête strict `PROVENANCE:` (contre 25 documentés à l'époque de l'audit initial) ; `certification-complete.py` en est totalement dépourvu. Les scripts des couches v2.0 (sessions Task 12-14) n'ont pas reçu l'en-tête de traçabilité. Correction recommandée : `audit-provenance.py --fix` (mode idempotent documenté) + en-têtes sur les scripts récents.
- **W3-E2 ACCEPÉ (affine l'analyse P1)** — 3 arêtes « Utilisé par » des disciplines (loop/graph/harness-engineering → correct-work) sans miroir dans le « Dépend de » de correct-work. L'analyse P1 (réciprocité des arêtes « Dépend de » : 66 OK / 0 ABSENTE) vérifiaient la réciproque dans le sens A→B ; W3 a vérifié le sens inverse (les déclarations d'usage des tiers doivent être acquittées par l'utilisateur déclaré) et trouve 3 arêtes non acquittées sur 35 — l'invariant B3 « 0 asymétrie » est donc à nuancer : vrai pour les arêtes « Dépend de », faux pour 3 déclarations « Utilisé par » des disciplines.
- **Effet de bord W2 arbitré sans dommage** — l'exécution de `certification-complete.py` par W2 (l'option `--help` est ignorée par le script, constat S3) a régénéré `scripts/certification-report.json` : le fichier régénéré est **byte-identique** à la version publiée (déterminisme des arbitres confirmé, drift zéro).

## 4. Convergences avec l'analyse P1 (cross-validation inter-méthodes)

Trois constats de l'analyse mécanique P1 (`analyse-interactions-gc.py`) sont **indépendamment confirmés** par les workers : l'écart famille/registre (F1 — W3 : « 5/5 installés, 0/5 entrée KB »), l'écart corpus CORRECT-WORK (F2 — W1, avec la précision que l'ULTRA §3 déclare bien v2.7.0 = forme installée) et les trous de lignée GEN-PLAN (F3 — W1). La convergence de trois méthodes différentes (parseur superviseur, audit corpus humain-agent, audit registre humain-agent) sur les mêmes écarts renforce leur réalité — c'est l'apport du Second Opinion multi-agents.

## 5. Constats nouveaux issus de la flotte (non détectés par P1)

1. **[S2·W2] Régression traçabilité PROVENANCE** — 9/32 scripts en-têtés stricts (convention N27), `certification-complete.py` sans marqueur. *Action : `audit-provenance.py --fix` + en-têtes scripts récents.*
2. **[S3·W1] README §2 arbre obsolète** — cite GEN-PLAN v3.12.0 comme unique PM (14 réels, max v3.18.0), 8 entrées décrites vs 24 fichiers ; la note v2.1.0 annonçait le drift §6.1 « résorbé » sans recalibrer l'arbre. *Action : recalibrage README §2 (montée v2.1.1).*
3. **[S3·W1] `verify-by-sha.py` fantôme** — référencé par le README (arbre + commandes) mais introuvable (déjà constaté S4 à l'installation Task 1 — canal R-1 historique). *Action : purge de la référence ou restauration du script.*
4. **[S3·W3] 5/21 entrées KB sans champ « Dernière calibration »** — les entrées P-H 2026-10-02 (audio-metadata, cpp-analysis, pdf-llm, resource-monitor, version-management). *Action : complétion des 5 lignes (montée registre).*
5. **[S3·W3] 3 arêtes « Utilisé par » non acquittées** — voir arbitrage §3. *Action : miroir « Dépend de » chez correct-work ou reformulation des déclarations des disciplines.*
6. **[S4×6] Mineurs** — comptages 80/84 skills divergents (README §1 vs SHARED §0), ancre résiduelle v3.12.0 dans SHARED §7, SYNC-CONTEXT « 23 fichiers » vs CORPUS_ATTENDU 24, `monitor.py` ne retourne pas d'écriture du `--state-file`, frontmatter `name: Version Management Skill` (≠ kebab-case) pour version-management, `--help` ignoré par certification-complete.py.

## 6. Verdict du test robuste

**PASS AVEC RÉSERVES** — l'écosystème **fonctionne** sous charge réelle : planification spec-first, vague parallèle de 3 agents spécialisés, livrables conformes aux micro-specs, agrégation et arbitrage documentés, douze disciplines/protocoles mobilisés chacun avec artefact vérifiable, idempotence des arbitres confirmée (y compris sous l'effet de bord W2). Les réserves sont les constats S2/S3 ci-dessus (1 S2 : régression PROVENANCE ; 4 S3 nouveaux + 2 S3 confirmés), toutes actionnables — elles alimentent les suggestions (a)/(b)/(c) du rapport d'analyse et la roadmap de session suivante. Zéro S1 : rien ne bloque le fonctionnement. La valeur démonstrative est double : le harnais multi-agents **trouve des défauts que l'analyse mono-agent a manqués** (6 constats nouveaux dont 1 S2), et les trois verdicts convergents valident la capacité de l'écosystème à s'auto-évaluer.
