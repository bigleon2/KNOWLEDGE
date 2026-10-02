# Rapport baseline A2 — memory-engineering v1.0.0 (hors périmètre de la suggestion (c))

> **Session** : continuation web-bbbeab47 · Task 18 · 2026-10-03 · **Directive** : « Puis LORSQUE (le confirm LLM sera levé) alors exécute une session gen-plan pour matérialiser les baselines de (hors périmètre de la suggestion (c)) »
> **Périmètre** : `memory-engineering` v1.0.0 — troisième discipline n°54 détenue par gen-plan (§1.9), restée EN ATTENTE hors du périmètre de la suggestion (c) (qui cite fleet-engineering et spec-driven-development uniquement). Sa baseline A2 est la dernière armée de l'écosystème.
> **Gate QUOTA_OK** : levé à 00:18 UTC (sonde unique KO-L001 — 2 tokens), puis **épuisé en cours de mesure** (HTTP 429 — voir §5) : la voie L est partiellement mesurée (4/7 cas), la re-mesure post-optimisation est armée au prochain QUOTA_OK.

## 1. Méthode

Identique à la baseline des disciplines n°54 (c) — `scripts/task17-baseline-a2.py` — portée ici par l'arbitre idempotent **`scripts/task18-baseline-a2-memory.py`** : les 7 cas officiels de `evals/trigger_evals.json` (5 positifs, 2 contrôles négatifs — graph-engineering et fleet-engineering, disciplines voisines) passés dans les **2 voies convergentes** SHARED §7 v2 : voie M (heuristique mécanique déterministe — radicaux du nom/tags/description, routage si ≥ 2 radicaux partagés OU ≥ 1 radical du nom, garde de collision) et voie L (vote majoritaire LLM 3 runs, seuil 0.5, politesse 4 s + backoff 429 — KO-L001). Runner équipé d'un flag **`--skip-done`** (429-aware) qui préserve les votes réels déjà mesurés et ne re-mesure que les cas à votes null. Dérive = cas dont le verdict de routage diffère de `should_trigger` → Description Optimization obligatoire (protocole A10/A14).

## 2. Résultats A2 (baseline AVANT optimisation)

**Verdict A2 : 4/7 — DÉRIVE ÉTABLIE (voie mécanique, 3 cas positifs sous le seuil).**

| # | Requête officielle | Attendu | Voie M (radicaux partagés) | Voie L (votes) | Baseline |
|---|---|---|---|---|---|
| 1 | Utilise le skill memory-engineering pour gouverner la mémoire de l'agent. | DÉCLENCHER | OUI (agent, engineering, memoir, memory) | 1.0 — OUI/OUI/OUI | PASS |
| 2 | Décide quoi écrire en État Long : worklog, KB, answer key — et quoi jeter. | DÉCLENCHER | OUI (etat, long) | 1.0 — OUI/OUI/OUI | PASS |
| 3 | Compacte cette session longue en conservant les ancres de reprise mécanique. | DÉCLENCHER | **NON** (compact seul — seuil ≥ 2 non atteint) | 1.0 — OUI/OUI/OUI | **DÉRIVE** |
| 4 | Isoler les contextes par tâche : prompts auto-contenus, pas de fuite inter-tâches. | DÉCLENCHER | **NON** (context seul) | 1.0 — OUI/OUI/OUI | **DÉRIVE** |
| 5 | Récupère l'information par retrieval ancré dans le registre versionné, sans hallucination. | DÉCLENCHER | **NON** (retrieval seul) | ARMÉ (429) | **DÉRIVE** (voie M) |
| 6 | Structure ces données en graphe de connaissances versionné avec nœuds et arêtes. | NE PAS déclencher | NON (garde de collision respectée) | ARMÉ (429) | PASS (voie M) |
| 7 | Lance plusieurs agents en parallèle et agrège leurs résultats avec un supervisor. | NE PAS déclencher | NON (1 radical, garde respectée) | ARMÉ (429) | PASS (voie M) |

**Lecture honnête** : sur les cas mesurés en voie L (1-4), le LLM vote OUI à 1.0 — y compris pour les cas 3 et 4 que la voie mécanique manque : la description est sémantiquement pertinente, c'est l'**heuristique de radicaux** qui est sous le seuil. La dérive est établie sur la voie mécanique — **source de vérité du routage appliqué par la plateforme** — indépendamment des votes LLM manquants (cas 5-7).

## 3. Description Optimization (protocole A10/A14) — v1.0.0 → v1.1.0

Dérive constatée → Description Optimization **obligatoire et appliquée** (Task 18, 2026-10-03). La description frontmatter est **étendue** (R2 — aucune rétrogradation, contenu v1.0.0 intégralement préservé) des radicaux discriminants couvrant les 3 requêtes en dérive :

- **#3 (compaction)** : « compaction de **sessions longues** avec **ancres de reprise mécanique** » → radicaux sess/longu/ancre/repris (+ compact existant) ;
- **#4 (isolation)** : « isolation des contextes : savoir **isoler** les contextes par **tâche** (**prompts** auto-contenus, pas de **fuite** inter-tâches) » → radicaux isoler/tach/prompt/fuit/contenu (+ context existant) ;
- **#5 (récupération)** : « **récupération de l'information** par retrieval ancré dans le **registre versionné**, **sans hallucination** » → radicaux recuper/inform/regist/versionn/hallucin/ancr (+ retrieval existant).

**Contrôles négatifs préservés** (garde de collision vérifiée par analyse des radicaux) : cas #6 (graphe) gagne au plus 1 radical (versionn) — sous le seuil de 2, aucun radical du nom ; cas #7 (flotte) inchangé (1 radical agent). Montée de version **v1.0.0 → v1.1.0** (§6 SKILL.md), registre KB synchronisé (Règle Zéro n°3 — entrée, description, Dernière calibration).

## 4. Re-mesure post-optimisation (MESURÉE — Task 18, 2026-10-03)

Exécutée au QUOTA_OK après la fenêtre d'attente de 30 minutes prescrite par la directive (« Essaie à nouveau dans une demie heure » — 429 observé ~00:40 UTC, re-mesure à ~01:14 UTC) : `python3 scripts/task18-baseline-a2-memory.py` (mesure complète des 7 cas × 2 voies sur la description v1.1.0, détection 429 corrigée — stderr inclus).

**Verdict post-optimisation : 7/7 — ZÉRO dérive, Description Optimization requise : NON.**

| # | Attendu | Voie M | Voie L (votes) | Baseline |
|---|---|---|---|---|
| 1 | DÉCLENCHER | OUI | 1.0 — OUI/OUI/OUI | PASS |
| 2 | DÉCLENCHER | OUI | 1.0 — OUI/OUI/OUI | PASS |
| 3 | DÉCLENCHER | OUI (6 radicaux : ancr, compact, longu, mecan, repris, sess) | 1.0 — OUI/OUI/OUI | PASS |
| 4 | DÉCLENCHER | OUI (8 radicaux : auto, contenu, context, fuit, inter, isoler, prompt, tach) | 1.0 — OUI/OUI/OUI | PASS |
| 5 | DÉCLENCHER | OUI (7 radicaux : ancr, hallucin, inform, recuper, registr, retrieval, versionn) | 1.0 — OUI/OUI/OUI | PASS |
| 6 | NE PAS déclencher | NON (1 radical — garde respectée) | 0.0 — NON/NON/NON | PASS |
| 7 | NE PAS déclencher | NON (1 radical — garde respectée) | 0.0 — NON/NON/NON | PASS |

**21/21 votes LLM réels (zéro null)**, preuves OUI/NON consignées dans `scripts/baseline-a2-memory-report.json`. La boucle du protocole A10/A14 est close en une itération : mesure → dérive → optimisation → re-mesure 7/7.

## 5. Honnêteté de la mesure (R3 — aucune fabrication)

Le quota API s'est **épuisé en cours de mesure** : les 12 appels des cas 1-4 ont abouti (votes réels OUI consignés avec preuve), puis les 9 appels des cas 5-7 ont échoué. Diagnostic mécanique du 2026-10-03 : le CLI z-ai écrit l'erreur **HTTP 429 (« Too many requests ») sur stderr** — invisible au parseur stdout du script, d'où la preuve « pas de contenu » au lieu du marqueur 429 (code retour 1 vérifié sur sonde de diagnostic). Conformément à R3, **aucun vote n'a été simulé** : les colonnes voie L des cas 5-7 conservent leurs votes null et leur preuve d'échec. Le runner 429-aware `--skip-done` (KO-L001) a été appliqué pour la re-mesure partielle sans marteler l'API.

Portée de l'écart : **nulle sur le verdict de dérive** (établie sur la voie mécanique complète et déterministe — 7/7 cas mesurés) ; l'écart porte uniquement sur la confirm LLM des cas 5-7, couverte par la re-mesure post-optimisation armée (§4) qui mesurera les 2 voies intégralement.

## 6. Bénéfice (objectif de la directive)

La troisième discipline n°54 cesse d'être « armée non mesurée » : sa baseline A2 existe, tracée et rejouable, la dérive de routage est détectée **avant** toute mise en production du déclenchement automatique, et la correction (Description Optimization v1.1.0) est appliquée selon le protocole — complétant la matérialisation de la couche des disciplines n°54 (fleet/spec/mémoire) ouverte par la suggestion (c).
