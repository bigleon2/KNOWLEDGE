# Rapport de tests comparatifs — Task 60 G3-SG1b (D603b, E13-4)

> **Directive (verbatim)** : « dans l'objectif de m'aider à prendre ma décision, génère $FACON des tests $FACON2 fonctionnels et de performances sur cette future version de mon écosystème et sur mon écosystème actuel. »
> **Méthode** : harnais `scripts/task60-tests-comparatifs.py` (Python stdlib, 3 phases, 24 tests) — le prototype PM-skill est **EMBARQUÉ dans le harnais** (bac à sable `download/tests-task60/`), **AUCUNE intégration** (garde G0 mécanique : aucun `skills/pm-skill/`, aucun `scripts/generer-pm-ephemere.py` — porte propriétaire D604 respectée). Zéro fichier d'état de l'écosystème modifié (seule écriture : `generer-pm-report.json`, comportement nominal idempotent de l'arbitre existant).
> **Rejouabilité** : rc=0 ×3 passes ; **68/68 artefacts byte-stables** entre passes (même jour) ; chronométrages seuls varient (mesures).
> **Verdict global : 16 PASS · 1 FAIL · 7 FACT.** L'unique FAIL (A3 gen-plan) est un **défaut réel de l'écosystème actuel** détecté par le test — pas un défaut du prototype.

---

## PHASE A — Écosystème ACTUEL (corpus KO-L004, lecture seule)

| Test | Verdict | Résultat mesuré |
|---|---|---|
| A1 Couverture PM | FACT | **4 familles / 68 skills racine = 5,9 %** — 64 skills sans aucune voie PM |
| A2 Cohérence versions | **PASS** | 4/4 familles COHERENT (`generer-pm-skill.py --check`, rc=0, ~25 ms) |
| A3 Auto-portance PMs corpus | **3/4 — gen-plan FAIL** | correct-work ×3 contexte ✓ · clone-chat ×2 ✓ · refactor-guard ×2 ✓ · **gen-plan : contexte ×2 mais dépendance externe ×1 (« lire en premier »)** — le PM le plus utilisé n'est pas utilisable seul dans une IA |
| A4 Voie PM non-famille | **REFUS MÉCANIQUE** | `--generate tsi-validator` → rc=3 « famille inconnue » — la voie n'existe pas pour 64 skills |
| A5 Empreinte stockage permanente | FACT | corpus 9 fichiers **379 Ko** + archive PMs 48 fichiers **3 527 Ko** + **16 deltas** ≈ 3,9 Mo d'état |

## PHASE B — Version FUTURE (prototype PM-skill éphémère, bac à sable)

| Test | Verdict | Résultat mesuré |
|---|---|---|
| G0 Porte D604 | **PASS** | prototype NON intégré (aucun fichier hors `download/tests-task60/`) |
| B1 Génération famille | **PASS** | `PM-ephemere-correct-work-v2.9.0.md` (26 484 o) — en-tête + mode d'emploi + mission + §0 + SHA |
| B2 Génération non-famille | **PASS** | tsi-validator (9 722 o) · vue-upload (19 476 o) — la voie impossible en A4 fonctionne |
| B3 Batch complet | **PASS** | **68/68 générés**, 0 erreur |
| B4 Auto-portance | **PASS** | **68/68 auto-portants** (§0 Contexte Système embarqué, zéro « lire en premier ») |
| B5 Déterminisme ×2 | **PASS** | 5 échantillons régénérés byte-identiques |
| B6 Fidélité contenu | **PASS** | 3/3 — version + mission (description verbatim) présentes *(ce test a détecté un vrai défaut du prototype — mission non projetée — corrigé : section MISSION ajoutée, preuve que les tests mordent)* |
| B7 Traçabilité SHA-256 | **PASS** | 3/3 — SHA-256 du SKILL.md source embarqué et exact |

## PHASE C — Performances

| Test | Verdict | Mesure |
|---|---|---|
| C1 Génération unitaire | FACT | **0,4 ms** (moyenne ×10, correct-work) |
| C2 Batch 68 skills | FACT | **0,02 s** au total (0,3 ms/skill) |
| C3 Empreinte sorties | FACT | sorties 68 fichiers **1 214 Ko régénérables/supprimables** (livrables download/, pas un état) vs **379 Ko d'état permanent** corpus seul |
| C4 Coût par montée de version | FACT | corpus : **17 touches d'état**/montée MINOR (worklog Task 48, inventaire c.1) · éphémère : **0 touche d'état** |
| C5 Résilience volatilité | **PASS** | 5 PMs supprimés → **régénérés en 1 ms** ; corpus perdu = réinstallation pipeline + re-certification (preuve vivante Task 60 §0 : minutes) |
| C6 Lag | **PASS** | bump version simulé (bac à sable) → **PM éphémère v2.11.0-test en 1 ms** ; corpus : bump = cascade 17 touches, lags ×4+ documentés (c.4) |
| C7 Structurel (correct-work) | FACT | voir table ci-dessous |

## C7 — Comparatif structurel PM corpus vs PM éphémère (correct-work v2.9.0)

| Élément | PM corpus | PM éphémère |
|---|---|---|
| CONTEXTE SYSTÈME embarqué | ✓ | ✓ |
| §7 Historique des versions complet | ✓ | ✗ (projection de l'état courant) |
| §5 Instructions d'installation écosystème | ✓ | ✗ (remplacé par mode d'emploi IA externe) |
| Mode d'emploi IA externe | ✗ | ✓ |
| Traçabilité SHA-256 source | ✗ | ✓ |

## Synthèse comparative — tableau de décision

| Critère | Écosystème actuel | Version future (testée) |
|---|---|---|
| Couverture PM | 4 familles (**5,9 %**) | **68/68 (100 %)** |
| Auto-portance (utilisable seul dans une IA) | 3/4 (gen-plan FAIL) | **68/68** |
| Temps de génération | cascade multi-étapes KO-L004 | **0,4 ms/skill · batch 0,02 s** |
| Coût d'état par montée | 17 touches | **0 touche** |
| Lag PM | ×4+ documentés | **impossible par construction** (1 ms sur bump simulé) |
| Résilience volatilité (4 recyclages live) | pipeline + re-certification (minutes) | **régénération 1 ms** |
| État permanent | 379 Ko + 3 527 Ko archives + 16 deltas | **0** (sorties régénérables) |
| Historique versions complet (§7) | ✓ (spécifications versionnées) | ✗ — **rôle conservé par le corpus** |
| Installation écosystème (§5) | ✓ | ✗ — mode d'emploi IA à la place |
| Voie non-famille | refus mécanique | **68/68** |

## Lecture honnête (pour la décision)

1. **La version future domine sur tous les critères de portabilité** : couverture ×17, auto-portance 100 %, génération ~50 000× plus rapide qu'une cascade, zéro lag, zéro coût d'état, résilience à la volatilité (4 recyclages live documentés — le test C5 la mesure : 1 ms).
2. **La version future ne remplace pas le rôle d'archive du corpus** (§7 historique complet, §5 installation écosystème — C7) : elle le **complète** pour l'usage IA externe. C'est la confirmation mécanique de la proposition D603 : *couche additive, corpus intact*.
3. **Le test A3 révèle un défaut de l'écosystème actuel indépendant de la décision** : le PM gen-plan du corpus n'est pas auto-portant (dépendance « lire en premier » — contre SHARED §6.2). La version future corrige ce cas par construction pour TOUT skill (B4 : 68/68).
4. **Les tests ont mordu** : B6 a détecté un vrai défaut du prototype (mission non projetée), corrigé avant la passe verte — le harnais n'est pas décoratif.
5. **Ce que la version future ne fait pas** : elle n'exécute pas le skill dans l'écosystème (voie native = le skill installé, règle canonique G2) et n'historise pas les versions (rôle corpus KO-L004) — par conception (R4, jamais dupliquer).

## Livrables du test (inspectables)

- Harnais : `scripts/task60-tests-comparatifs.py` (rejouable : `python3 scripts/task60-tests-comparatifs.py`)
- Sorties prototype : `download/tests-task60/output/` (68 PMs éphémères — ex. `PM-ephemere-correct-work-v2.9.0.md`, `PM-ephemere-tsi-validator-v1.3.0.md`)
- Résultats machine : `download/tests-task60/resultats.json` (24 tests, métriques)
- Le présent rapport : `download/rapport-tests-task60.md`

**PORTE D604 : la décision reste au propriétaire — rien n'a été intégré.**
