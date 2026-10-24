---
name: refactor-guard
version: 1.8.1
category: ecosystem
language: fr
tags:
  - refactoring
  - zero-regression
  - risk-scoring
  - sandbox
  - governance
  - ecosystem
description: >
  Skill de refactorisation agnostique appelé par gen-plan lorsqu'un besoin de
  refactorisation est détecté (métriques, dette technique, demande explicite).
  Méthodologie applicable à toute base de code (Python/C/C++/skills) et à tout
  élément de l'écosystème : taxonomie de signaux H01-H15 (sources graph-engineering
  et fleet-engineering), score de risque pondéré (scripts/risk_score.py — stdlib),
  scan de dépendances (scripts/graph_scan.py — stdlib), spécification formelle
  (discipline spec-driven-development), sandbox obligatoire (harness-engineering),
  maker-checker (loop-engineering), gouvernance N0-N5, principe zéro-régression
  (« aucune modification ne doit altérer le comportement, la stabilité ou les
  performances tant qu'elle n'a pas été prouvée, isolée, validée, réversible et
  observée »), 9 couches de sécurité, échelle de déploiement disabled → shadow →
  recommend_only → sandbox_only → human_approved → canary → enabled (défaut :
  shadow, enabled:false), contrats de performance (latence < 2 %, CPU < 5 %,
  mémoire < 5 %, erreurs 0), validation finale par correct-work v2.7.0 (couplage
  gen-plan OBLIGATOIRE §1.5). Conçu pour la combinaison C-SAFE-1 = H02 + H04 +
  H05 + H07 + H08 + H09 + H10 + H14 + H15. Déclaré dans l'arbre canonique par la
  fusion de la discussion externe 468a4c26 (Task 8) : lignée externe certifiée v1.7.0
  (rollout enabled — échelle H15 terminale), base de contenu = hôte v1.2.0 porté
  (provenance R4). Complément triangulaire de la discipline n°55 :
  refactoring-engineering (exécutant) + refactoring-test (évaluateur) + refactor-guard
  (garde-fous).
dependencies:
  - skill: gen-plan
    version: ">=3.21.0"
    used_at: "Appel (hook), plan d'actions de refactorisation (R6), E13"
  - skill: correct-work
    version: ">=2.7.0"
    used_at: "R8 validation finale + par phase (couplage gen-plan OBLIGATOIRE §1.5)"
  - skill: resource-monitor
    version: ">=1.0.0"
    used_at: "G-RES avant tout scan/sandbox (profil NORMAL/ECO/VIEUX PC)"
  - skill: graph-engineering
    version: ">=1.0.1"
    used_at: "H02 — graphe de dépendances, centralité, cycles"
  - skill: spec-driven-development
    version: ">=1.0.0"
    used_at: "H07 — spécification de refactorisation comme contrat exécutable"
  - skill: harness-engineering
    version: ">=1.1.0"
    used_at: "H04/H09 — sandbox, arbitres, audit"
  - skill: loop-engineering
    version: ">=1.1.0"
    used_at: "H05/H08 — maker-checker, rollout itératif"
read_when:
  - Déclencher quand gen-plan détecte un besoin de refactorisation (métriques dégradées, dette technique, demande utilisateur explicite)
  - Déclencher si la demande mentionne : refactorisation, refactor, refactor-guard, restructuration de modules
  - Ne pas déclencher pour du code neuf sans base existante (pas de refactorisation possible)
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — Spécification fonctionnelle

### §1.1 Mission et principe fondateur

**Mission** : fournir à gen-plan une méthodologie **agnostique** (tout langage, toute base de code, tout skill) pour détecter, évaluer, spécifier et piloter une refactorisation **sans régression**.

**Principe fondateur (zéro-régression)** : *« Aucune modification ne doit pouvoir altérer le comportement, la stabilité ou les performances de l'écosystème tant qu'elle n'a pas été prouvée, isolée, validée, réversible et observée. »*

**5 règles absolues** :
1. Aucun changement sans validation mesurable préalable.
2. Désactivable à tout instant par feature flag (`refactor_guard.enabled: false` par défaut).
3. Lecture seule au départ (mode shadow — aucune écriture).
4. Sandbox obligatoire avant toute application réelle.
5. Validation avec preuve mesurable (baseline → comparaison → verdict).

### §1.2 Les 8 étapes (R1-R8)

| Étape | Nom | Description | Outil / discipline |
|-------|-----|-------------|---------------------|
| R1 | Réception du signal | gen-plan transmet le trigger (métriques, demande, discipline source) — formats JSON §2.4 | gen-plan (hook) |
| R2 | Scan et analyse | Graphe de dépendances, cycles, centralité, complexité, couplage — signaux externes limités à graph-engineering et fleet-engineering (décision projet : asymétrie déclencheurs/techniques) | scripts/graph_scan.py (H02) |
| R3 | Score de risque | Scoring pondéré : complexité > 20 → +3 ; couplage > 10 → +3 ; couverture < 0.5 → +4 ; module critique → +5. Niveaux : ≥ 10 critique, ≥ 6 moyen, < 6 faible | scripts/risk_score.py (H14) |
| R4 | Spécification | La refactorisation devient un CONTRAT exécutable : objectifs, invariants, seuils, critères d'acceptation mécaniques | spec-driven-development (H07) |
| R5 | Sandbox | Exécution en environnement isolé (copies, branche dédiée), comparaison baseline → candidat, arbitres mécaniques | harness-engineering (H04) |
| R6 | Plan d'actions | La refactorisation validée en sandbox devient un plan gen-plan (règle d'or n°3 — extension du plan courant, jamais réécriture destructrice) | gen-plan |
| R7 | Exécution + maker-checker | Application par petits pas réversibles, vérification systématique après chaque pas (maker ≠ checker), rollout progressif | loop-engineering (H05/H08) |
| R8 | Validation finale | correct-work (mode PROJET) sur les livrables de refactorisation — couplage gen-plan OBLIGATOIRE (correct-work §1.5) ; audit écrit (H09) ; humain dans la boucle (H15) | correct-work >= v2.7.0 |

### §1.3 Gouvernance N0-N5 et échelle de déploiement

| Niveau | Nom | Capacités activées |
|--------|-----|--------------------|
| N0 | Disabled | Aucun effet — le skill n'analyse rien (défaut à l'installation) |
| N1 | Shadow | Observation passive : scans et scores produits, AUCUNE écriture |
| N2 | Recommend_only | Recommandations émises à l'agent/utilisateur, aucune écriture |
| N3 | Sandbox_only | Exécutions limitées à la sandbox |
| N4 | Human_approved | Application réelle APRÈS validation humaine explicite (GO) |
| N5 | Canary/Enabled | Application contrôlée par petits pas avec rollback armé |

**Passage de niveau** : conditionné (stabilité constatée, tests verts, métriques dans les contrats §1.5, rollback testé, journalisation complète). **Rétrogradation immédiate** en cas de violation des contrats.

**9 couches de sécurité** (toutes actives, aucune désactivable sauf décision propriétaire) : feature flags · shadow mode · recommend_only · sandbox_required · tests_required · policy_gate · human_approval_required · rollback_required · audit_required.

### §1.4 Combinaison de signaux retenue (C-SAFE-1)

**Noyau actif C05** = H02 (graphe de dépendances) + H04 (sandbox) + H05 (maker-checker) + H07 (spécification formelle) + H10 (fitness architecturales) + H14 (score de risque) — **extension C-SAFE-1** = C05 + H09 (audit) + H15 (humain dans la boucle) + H08 (rollout progressif).

**Passifs (lecture seule uniquement)** : H01 (signaux fleet), H03 (code smells), H12 (mémoire inter-sessions). **Reportés** : H06 (DAG externe), H13 (pipeline multi-agents). **À ne jamais activer** : C12 = H01 + H03 sans H04 ni H14 ni H15 (score 2.0/10 — refactorisation non gardée). Catalogue complet : `references/catalogue-signaux-h01-h15.md`.

### §1.5 Contrats de non-régression (seuils d'acceptation)

| Contrat | Seuil | Mesure |
|---------|-------|--------|
| Latence ajoutée | < 2 % | baseline vs candidat (médiane + P95) |
| CPU ajouté | < 5 % | profilage de la sandbox |
| Mémoire ajoutée | < 5 % | profilage de la sandbox |
| Taux d'erreur | 0 | arbitres + tests |
| Comportement observable | identique | tests de non-régression baseline rejoués |

**Contexte temps réel (audio/DJ — TRAKTOR, KONTROL)** : `realtime_guard` — aucune analyse lourde pendant une phase critique (`pause_analysis_during_live: true`, `max_cpu_percent: 5`, `max_memory_mb: 200`, `low_priority: true`).

### §1.6 Matrice de décision par risque

| Score | Niveau | Conduite |
|-------|--------|----------|
| ≥ 10 | Critique | Validation humaine OBLIGATOIRE (N4) ou blocage — sandbox + spec + maker-checker requis |
| 6-9 | Moyen | Spec + sandbox + maker-checker (N3), puis N4 pour application |
| < 6 | Faible | Refactorisation locale simple, contrôlée par tests (N2→N3) |

---

### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)

- **Golden master AVANT (renforcement R5)** : avant TOUTE modification, capturer et sceller les sorties baseline (n ≥ 3 runs — entrées nominales + edge cases), puis les rejouer en sandbox ET post-vol ; la preuve comportementale (sorties identiques) remplace le simple hachage avant/après, qui ne prouve rien si les entrées varient. → *Application locale* : sorties baseline scellées avant cascade (generer-pm --check + arbitres AVANT régénération).
- **Mutation testing léger (sandbox)** : avant de considérer une validation acquise, modifier 1 opérateur/constante de la cible et exiger qu'au moins 1 test échoue — une suite qui reste verte sur une mutation prouvée est déclarée INSENSIBLE (anti faux-verts ; tests qui testent le testeur). → *Application locale* : gardes anti-faux-succès des scripts de mutation (échec si 0 match — leçon Task 17) ; re-jeu ×2 pour prouver l'idempotence.
- **Rollback armé (N5)** : en canary, la violation d'un contrat (latence/CPU/mémoire) déclenche le rollback AUTOMATIQUEMENT armé + signalement propriétaire — « rollback testé » ne suffit plus ; détection de contournement de tests dans les journaux (héritage TRACE). → *Application locale* : publication rebase = retour garanti à l'état antérieur (rebase --abort / reset --hard scellé) ; 0 force-push (Règle 0 GitHub).
- **Sources** : Rackspace/CircleCI progressive delivery 2026 · characterization tests · arXiv 2601.20103.

> **Révision Task 24** (2026-10-23, session web-fdf5963c — directive propriétaire « révisez les §1.9bis des 16 éléments ») : restructuration en bullets actionnables — chaque apport porte son application locale explicite ; bullet Sources normalisé ; contenu factuel Task 22 inchangé (garde anti-perte : lead-ins et sources préservés).

## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python 3.8+ **stdlib uniquement** (N3 — aucune dépendance externe ; networkx OPTIONNEL en local avancé, jamais requis)
- **Environnement** : `skills/refactor-guard/`
- **Scripts** : `scripts/risk_score.py` (H14, CLI JSON), `scripts/graph_scan.py` (H02, `ast`), `scripts/config.py` (Sprint 1 : seuils perf verbatim, N0, `allow_push: false`), `scripts/audit_ledger.py` (H09, journal append-only JSONL), `scripts/spec_builder.py` (H07, 9 sections obligatoires), `scripts/policy_engine.py` (H10, 5 politiques verbatim), `scripts/sandbox_runner.py` (H04, isolation + hachage avant/après), `scripts/checker.py` (H05, boucle 4 stages), `scripts/human_gate.py` (H15, matrice risque×couverture), `scripts/rollout.py` (H08, 7 modes + `can_apply_change` + 6 conditions de passage), `scripts/shadow_run.py` (N1 shadow + calibration grille #token E15 — refuse tout mode d'application, ABANDON sans écriture sur la cible)
- **Chaîne de production** : scripts écrits via script-creator → post-traitement correct-py (`correct-py-verifie.py`, CONFORME rc=0) → relecture script-reviewer (grille G1-G8 : PASS 9/9, 0 sévérité, idempotence ×2)
- **Self-tests** : **79/79 PASS idempotents ×2** (cumul réel vérifié 2026-10-10, correct-work PROJET F-1 : config 6, audit 6, spec 5, policy 9, sandbox 8, checker 6, human_gate 10, rollout 14 = 64 pour les 8 modules hypothèses ; + risk_score 8 + graph_scan 7 = 79 total cumulé ; + shadow_run 11)

### §2.2 Structure

```
skills/refactor-guard/
├── SKILL.md                              # Ce fichier
├── references/
│   ├── catalogue-signaux-h01-h15.md      # Taxonomie H01-H15, scores, combinaisons, anti-patterns
│   └── gouvernance-zero-regression.md    # Principe, 5 règles, 9 couches, N0-N5, contrats, matrice
├── scripts/
│   ├── risk_score.py                     # Scoring de risque (H14) — stdlib, déterministe, self-test
│   ├── graph_scan.py                     # Graphe d'imports + métriques de complexité (H02) — stdlib
│   ├── config.py                         # Configuration canonique Sprint 1 (seuils perf, N0) — stdlib
│   ├── audit_ledger.py                   # Journal d'audit append-only (H09) — stdlib
│   ├── spec_builder.py                   # Spécification formelle 9 sections (H07) — stdlib
│   ├── policy_engine.py                  # 5 politiques architecturales (H10) — stdlib
│   ├── sandbox_runner.py                 # Sandbox isolée + rollback (H04) — stdlib
│   ├── checker.py                        # Boucle maker-checker 4 stages (H05) — stdlib
│   ├── human_gate.py                     # Matrice risque×couverture (H15) — stdlib
│   ├── rollout.py                        # 7 modes + gate can_apply_change (H08) — stdlib
│   └── shadow_run.py                     # Exécution N1 shadow + calibration grille #token (E15) — stdlib
└── evals/
    ├── evals.json                        # Cas de test (4 evals, schéma skill-creator)
    └── trigger_evals.json                # Bare-liste canonique (décision C006)
```

### §2.3 Configuration (extrait canonique)

```yaml
refactor_plan:
  enabled: false          # N0 par défaut — jamais enabled à l'installation
  shadow_mode: true       # N1 : observation passive
  auto_apply: false       # H15 : jamais d'application sans GO
  require_human_approval: true
  realtime_guard:         # contexte audio/DJ
    pause_analysis_during_live: true
    max_cpu_percent: 5
    max_memory_mb: 200
    low_priority: true
```

### §2.4 Formats JSON (entrée/sortie)

**Entrée (trigger transmis par gen-plan)** :
```json
{"trigger": "metrics|explicit|fleet|graph", "target": "skills/<nom>/ | <chemin>",
 "reason": "<signal constaté>", "severity": "low|medium|high|critical",
 "metrics": {"cyclomatic_complexity": 0, "coupling": 0, "cohesion": 1.0,
             "test_coverage": 0.0}, "constraints": ["aucun push sans validation"]}
```

**Sortie (verdict refactor-guard)** :
```json
{"decision": "block|require_approval|sandbox_then_plan|allow_simple",
 "risk_score": 0, "risk_level": "faible|moyen|critique",
 "refactor_type": "<extraction|découpage|réorganisation>",
 "plan": ["R1..R8 — étapes détaillées"], "expected_benefits": ["…"],
 "risks": ["…"], "validation": {"sandbox": "pending|pass|fail",
 "correct_work": "pending|pass|pass_with_reserves|fail"}}
```

### §2.5 Grille #token (calibrée 2026-10-10 — recalibration E15, première exécution N1 shadow réelle)

**Deux périmètres de mesure** (ne pas confondre — cf. `scripts/shadow_run.py`) :

| Groupe | Périmètre agent-driven (v1.0.0, inchangé — contexte consommé par l'agent) | Périmètre mécanique (calibré E15, n=3 — charges utiles JSON des outils) |
|--------|---------------------------------------------------------------------------|--------------------------------------------------------------------------|
| R1-R3 (détection/scoring) | 500-1200 #token | **150-900 #token** (mesuré 180-231) |
| R4-R6 (spec/sandbox/plan) | 2000-6000 #token | **200-1000 #token** (mesuré 242-249) |
| R7-R8 (exécution/validation) | 3000-8000 #token | **30-200 #token** (mesuré 42) |

- **Mesures réelles** (shadow_run.py, mode N1, cibles vivantes : clone-chat 0 py, correct-work 1 py, gen-plan 1 py — 0 cycle, `apply: False` partout, journaux audit H09 produits) : preuves dans `download/refactor-guard-shadow-run-2026-10-10/`.
- **Heuristique E15** : 3,5 caractères/token (mix FR/code) — estimation documentée, pas un comptage tokenizer ; à affiner itérativement sur cibles multi-fichiers (n=3 à ce jour).
- **Coefficients** : profil ECO 0.7x, VIEUX PC 0.5x ; recalibration E15 itérative (prochaines exécutions N1→N2).

### §2.6 Idempotence et réversibilité (R1-R6)

R1 vérifier présence avant insertion · R2 ne jamais rétrograder le niveau de gouvernance sans cause documentée · R3 fusionner les spécifications (pas de duplication) · R4 ne jamais dupliquer un arbiter/scan · R5 journaliser chaque pas (worklog) · R6 auto-adaptation sans duplication. Chaque application réelle est précédée d'un snapshot réversible (branche `refactor-guard/<cible>` ou archive tar anti-R2) et d'un plan de rollback testé.

---

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Appelé par gen-plan (hook) | R1 reçoit le trigger ; R6 rend un plan via gen-plan ; règle d'or n°3 (extension de plan) ; version >= v3.21.0 |
| correct-work | Validation R8 + par phase | Mode PROJET — couplage gen-plan OBLIGATOIRE (correct-work §1.5, v2.7.0 : fin du mode autonome) ; verdicts PASS / PASS AVEC RÉSERVES / FAIL |
| resource-monitor | Précondition G-RES | Collecte avant tout scan/sandbox (profils NORMAL/ECO/VIEUX PC) |
| graph-engineering | Source de signaux H02 | Graphe de dépendances, cycles, centralité — déclencheur autorisé |
| fleet-engineering | Source de signaux H01 (passif) | Charge/concurrence des agents — lecture seule, jamais déclencheur seul |
| spec-driven-development | Discipline R4 (H07) | Spécification = contrat exécutable |
| harness-engineering | Discipline R5 (H04/H09) | Sandbox, arbitres, audit byte-level |
| loop-engineering | Discipline R7 (H05/H08) | Maker-checker, rollout itératif |
| context-engineering | Mobilisation | Lecture bloc par bloc des cibles volumineuses (> 500 lignes) |

---

## §4 — Conventions

- **Nommage** : kebab-case (`refactor-guard`, `catalogue-signaux-h01-h15.md`) ; versions semver (`1.0.0`)
- **N3** : scripts Python stdlib uniquement ; aucun script shell
- **N1** : chaque étape R1-R8 taguée #token ; recalibration à E15 de gen-plan
- **Sécurité** : aucun push sans validation explicite (règle d'or Z.ai n°2) ; `allow_push: false` ; toute application réelle = GO humain (N4)

## §5 — Historique

| Version | Date | Contenu |
|---------|------|---------|
| 1.0.0 | 2026-10-10 | Matérialisation initiale — continuation du projet « Skill Refactorisation Plan » (discussion Qwen T1-T46 : conception C05/C-SAFE-1, principe zéro-régression, gouvernance N0-N5) ; adaptée à l'écosystème d72226a+ (gen-plan dans sa version courante à la date — cf. historique par skill —, correct-work v2.7.0 couplage OBLIGATOIRE, KO-L003 dynamique, C006 bare-liste). Scripts stdlib testés ; evals conformes au schéma skill-creator. Réserve KO-L004 : génération du PM refactor-guard (extension generer-pm-skill.py 3→4 familles) reportée à décision propriétaire (D009). |
| 1.1.0 | 2026-10-10 | Matérialisation des 8 modules d'hypothèses C-SAFE-1 (config, audit_ledger H09, spec_builder H07, policy_engine H10, sandbox_runner H04, checker H05, human_gate H15, rollout H08) via chaîne imposée script-creator → correct-py → script-reviewer ; self-tests idempotents ×2 ; propagation versionnaire checker ECO_SKILLS + KB ; outil correct-py-verifie.py matérialisé (KO-L003) ; SKILL.md étendu via skill-creator. (Ligne d'historique complétée rétrospectivement en 1.2.0 — écart versionnaire constaté au contrôle correct-work PROJET.) |
| 1.2.0 | 2026-10-10 | Première exécution N1 shadow réelle (3 cibles vivantes) + calibration grille #token §2.5 (deux périmètres : agent-driven inchangé / mécanique calibré E15) ; ajout `scripts/shadow_run.py` (self-test 11/11 ×2, correct-py CONFORME, garde gouvernance : refuse tout mode d'application) ; correction F-1 (correct-work PROJET 2026-10-10) : comptage self-tests 72→**79/79** (cumul réel vérifié ×2) ; journaux audit H09 + rapports de calibration archivés (`download/refactor-guard-shadow-run-2026-10-10/`). |
| 1.7.0 | 2026-10-12 | CONVERGENCE de la lignée externe (fusion discussion 468a4c26 — Task 8, session web-b4d7dd19, gen-plan(step)) : l'instance source a certifié refactor-guard v1.7.0 (double-montée Tasks 23-24 — 6 PM v1.2.0→v1.7.0, rollout enabled = échelle H15 terminale, ledger N6, verif-finale-n6 réconcilié « périmées-par-conception » Task 26) ; matérialisation canonique = base mécanique v1.2.0 portée à l'identique (11 scripts stdlib + evals + references ×2) + présente calibration ; diffs intermédiaires v1.3.0→v1.6.0 non verbatim consignés par leurs preuves de discussion (R4 provenance — réserve : PMs de la lignée externe non portés, génération PM 3→4 familles = décision propriétaire D009 reportée) ; déclaration KB + ECO_SKILLS + arêtes bidirectionnelles (gen-plan hook E13, refactoring-engineering garde-fous D3/D4 — discipline n°55). |
