# Gouvernance zéro-régression — principe, couches, niveaux, contrats

> Source : discussion Qwen T9-T10 (« stratégie implacable », « Refactor Control Plane »).
> Adapté à l'écosystème d72226a+ — couplage correct-work v2.7.0 (§1.5 OBLIGATOIRE) intégré.

## 1. Principe fondateur

*« Aucune modification ne doit pouvoir altérer le comportement, la stabilité ou les performances de ton écosystème tant qu'elle n'a pas été prouvée, isolée, validée, réversible et observée. »*

Cette phrase est le CRITÈRE de rejet de toute proposition de refactorisation : une modification qui ne satisfait pas les cinq propriétés (prouvée, isolée, validée, réversible, observée) est refusée, quelle que soit sa valeur apparente.

## 2. Les 5 règles absolues

1. **Aucun changement sans validation mesurable** — baseline avant, comparaison après, verdict mécanique.
2. **Feature flag par défaut** — `refactor_plan.enabled: false` à l'installation ; désactivation à tout instant.
3. **Lecture seule au départ** — le premier niveau actif est shadow (N1) : scans et scores, zéro écriture.
4. **Sandbox obligatoire** — toute exécution de transformation passe par un environnement isolé (copie, branche).
5. **Validation avec preuve** — la preuve est une mesure réelle produite par exécution (leçon T37 : « métrique inventée » = réserve bloquante ; byte-level fait foi).

## 3. Les 9 couches de sécurité

| # | Couche | Garantie |
|---|--------|----------|
| 1 | feature flags | coupure instantanée globale |
| 2 | shadow mode | aucune écriture en observation |
| 3 | recommend_only | l'agent propose, n'exécute pas |
| 4 | sandbox_required | exécution isolée uniquement |
| 5 | tests_required | aucun pas sans tests verts |
| 6 | policy_gate | arbitres mécaniques avant application |
| 7 | human_approval_required | GO explicite pour toute application réelle (N4) |
| 8 | rollback_required | plan de retour arrière testé AVANT l'application |
| 9 | audit_required | journalisation exhaustive (worklog + rapports download/) |

## 4. Échelle de déploiement (modes) et niveaux N0-N5

Modes : `disabled → shadow → recommend_only → sandbox_only → human_approved → canary → enabled`.

| Niveau | Mode(s) | Autorisations | Passage |
|--------|---------|---------------|---------|
| N0 | disabled | rien | installation (défaut) |
| N1 | shadow | scans, scores, rapports | 1 session saine + G-RES OK |
| N2 | recommend_only | recommandations écrites | N1 stable + arbitres verts |
| N3 | sandbox_only | transformations en sandbox | N2 stable + contrats respectés en shadow |
| N4 | human_approved | application réelle après GO | sandbox PASS + rollback testé + GO propriétaire |
| N5 | canary/enabled | application par petits pas armés | N4 prouvé sur ≥ 2 refactorisations |

**Rétrogradation** : immédiate et non négociable en cas de violation des contrats (§5) ou d'échec correct-work (FAIL). La rétrogradation est journalisée avec cause, mesure et décision.

## 5. Contrats de non-régression

| Contrat | Seuil | Mesure |
|---------|-------|--------|
| Latence ajoutée | < 2 % | baseline vs candidat (médiane + P95) |
| CPU ajouté | < 5 % | profilage sandbox |
| Mémoire ajoutée | < 5 % | profilage sandbox |
| Taux d'erreur | 0 | arbitres + tests |
| Comportement observable | identique | tests baseline rejoués |

Historique projet (T11) : la première intégration avait mesuré **+3.50 % latence / +5.69 % P95 — au-dessus des seuils** → verdict « VALIDÉE avec optimisations requises », puis optimisations (cache LRU, parallélisation, early-exit) ramenant l'overhead estimé v3 à ~ -2.2 % / +1.37-1.64 %. Leçon conservée : **un dépassement de contrat bloque le passage de niveau** (pas de falsification de seuil — KO-L003).

## 6. Matrice de décision par risque (H14)

| Score | Niveau | Conduite | Couches exigées |
|-------|--------|----------|-----------------|
| ≥ 10 | critique | validation humaine OBLIGATOIRE ou blocage | toutes (1-9) |
| 6-9 | moyen | spec + sandbox + maker-checker | 1,2,4,5,6,8,9 (+7 à l'application) |
| < 6 | faible | refactorisation locale simple contrôlée | 1,2,5,8,9 |

Scoring (`scripts/risk_score.py`) : complexité > 20 → +3 ; couplage > 10 → +3 ; couverture < 0.5 → +4 ; module critique → +5. Niveaux : ≥ 10 critique, ≥ 6 moyen, < 6 faible. Seuils ML (v3 projet, reportés) : {low: 3, medium: 6, high: 8, critical: 10}.

## 7. Contexte temps réel (audio/DJ)

`realtime_guard` : `pause_analysis_during_live: true` · `max_cpu_percent: 5` · `max_memory_mb: 200` · `low_priority: true`. **Aucune analyse lourde ne doit s'exécuter pendant une phase critique** (set, mixage). Le profil VIEUX PC (gen-plan §2.4) implique en outre des scripts d'analyse < 100 lignes et pas de graphiques.

## 8. Articulation avec correct-work v2.7.0

La validation d'une refactorisation passe par `correct-work (mode PROJET)` — qui, depuis v2.7.0, utilise **gen-plan à l'Étape 1 de façon OBLIGATOIRE** (§1.5 correct-work : fin du mode autonome, ARRÊT EXPLICITE si gen-plan indisponible). refactor-guard ne propose JAMAIS de validation autonome : R8 = correct-work ← gen-plan. Verdicts : PASS → clôture ; PASS AVEC RÉSERVES → réserves journalisées, continuation ; FAIL → pause, correction, re-vérification.
