# Rapport final — Task 73 : Tests fonctionnels et performances — gen-plan hôte · écosystème hôte · gen-plan miroir

**Horodatage : 2026-11-09T01:30:00Z** · Session : web-ecef7f80 · Trace directive : 1a1b853d77f65451 · Plan : download/plan-task73-tests-fonctionnels-performances-genplan-ecosysteme-miroir.md (13 décisions) · Prérequis : Task 72 CLOSE

## 1. Résumé exécutif

| Cible | PRE | POST | Non-régression |
|---|---|---|---|
| **C1 — gen-plan hôte** (skills/gen-plan/) | **PASS** 11/11 (130,0 ms) | **PASS** 11/11 (131,5 ms) | ✓ stable |
| **C2 — écosystème hôte** (skills/) | **FAIL** (3 FAIL · 1 réserve) | **PASS AVEC RÉSERVES** (0 FAIL · 2 réserves légitimes, 270,3 ms) | ✓ 3 failles résorbées |
| **C3 — gen-plan miroir** (KNOWLEDGE-repo/skills/gen-plan/) | **PASS** 7/7 (4,7 ms) | **PASS** 7/7 (3,2 ms) | ✓ stable |
| **Global (pire des cibles)** | **FAIL** | **PASS AVEC RÉSERVES** | **non-régression stricte : TRUE (0 dégradation test à test)** |

**Une seule faille réelle détectée** — version-management absente de l'hôte (7ᵉ récidive documentée) — confirmée par **3 tests indépendants** (integrity, coherence, effectifs), **corrigée en 1 commande** (garde Task 56 : `ensure-installed.py --check` → INSTALLE-REPARÉ, rc=0), cause racine revérifiée **environnementale** (aucun script de l'écosystème coupable). Les 2 réserves POST restantes sont des tolérances adjudiquées légitimes du protocole (WARN B1 hérité + auto-références historiques v3.38.0 dans la table des hooks de gen-plan). L'écosystème est $FACON2 : **cohérent** (0 FAIL), **optimisé** (0 CRITIQUE, 71 skills), **fonctionnel** (arbitres ×4 + selftests + garde auto-réparation démontrée en réel).

## 2. Directive et alias

« génère $FACON, effectue des tests $FACON2 fonctionnels et performances sur mon skill "gen-plan", mon écosystème hôte et sur le skill "gen-plan" du miroir dans l'objectif de corriger $FACON leurs failles et d'optimiser $FACON leur fonctionnement et leurs interactions au sein de mon écosystème. » — $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » (registre skills/@historique/@Alias/aliases.json).

## 3. Méthodologie (protocole $FACON2)

- **Protocole** : download/protocole-tests-fonctionnels-performances-task73.json — 3 cibles, **26 tests** (17 fonctionnels, 7 de performances/méta, 2 hybrides), échelle PASS < PASS AVEC RÉSERVES < FAIL, agrégation pire-des-verdicts, phases PRE (capture sans correction) / POST (après corrections), non-régression stricte test à test.
- **Outillage** : scripts/task73-campagne-tests.py — orchestration **R4** de 9 arbitres existants (zéro duplication de logique de verdict) : check-ecosysteme-integrity.py, test-coherence-interactions.py, cache-verdicts.py (wrapper vcw), verify-cross.py, poids-chargement.py, protocole-test.py (re-curation), generer-pm-skill.py --check, check_plan_protocol.py, ensure-installed.py (hors campagne — appelé uniquement en phase correction). Durées mesurées par test. Selftest 8/8. Aucune écriture corrective en PRE.
- **Livrables JSON** : rapports de campagne par cible et phase (download/rapport-campagne-task73-{pre,post}-{C1,C2,C3}.json) + synthèse comparative (…-post-synthese.json).

## 4. C1 — skill gen-plan hôte : PASS 11/11

| Test | Verdict | Mesure clé |
|---|---|---|
| C1-F01 frontmatter | PASS | name/version 3.39.0/language fr |
| C1-F02 taille | PASS | 30 668 o = 29,95 Kio ≤ 30 Kio (contrat D002 Task 72) |
| C1-F03 references | PASS | 15/15 fichiers, 0 manquant, 0 inattendu |
| C1-F04 pointeurs | PASS | 15/15 cités dans SKILL.md |
| C1-F05 contrats verbatim | PASS | read_when ×1 · $FACON ×11 · SHARED ×20 · PATTERN:GEN-PLAN-HOOKS-PATTERNS ×2 · fenêtre native ×3 · TodoWrite ×3 |
| C1-F06 evals | PASS | evals 9/9 · trigger_evals 15/15 (non-régression triggers) |
| C1-F07 selftest plan | PASS | « RESUME : OK (7/7) » (34,3 ms) |
| C1-F08 re-curation | PASS | « VERDICT : PASS » C1-C4 (39,6 ms) |
| C1-F09 PM --check | PASS | [COHERENT] ×4 familles (22,7 ms) |
| C1-P01 poids | PASS | 29,9 Kio · 7 667 #token · INTERMÉDIAIRE (rang 10) |
| C1-P02 durées | PASS | campagne C1 complète : 130,0 ms (PRE) / 131,5 ms (POST) |

**Lecture** : la re-curation v3.39.0 (Task 72) est fonctionnellement et structurellement saine ; la lecture ciblée (progressive disclosure) est l'état par défaut ; les contrats de déclenchement sont intacts.

## 5. C2 — écosystème hôte : FAIL → PASS AVEC RÉSERVES

| Test | PRE | POST | Détail |
|---|---|---|---|
| C2-F01 integrity | **FAIL** | PASS | PRE : « version-management — SKILL.md manquant » → POST : 0 FAIL, vm v1.3.0 = attendu 1.3.0 |
| C2-F02 coherence | **FAIL** | PASS AVEC RÉSERVES | PRE : 1 FAIL (vm répertoire absent) + 3 WARN → POST : 0 FAIL, seul WARN B1 légitime hérité |
| C2-F03 vcw mécanisme | PASS* | PASS | cache-verdicts fonctionnel (2 commandes via wrapper --cibles, cache-hit démontré) |
| C2-F04 cross | PASS | PASS | 100,0 % · 0 erreur |
| C2-F05 effectifs | **FAIL** | PASS | PRE : hôte 70, KB manquants [version-management] → POST : hôte 71 · miroir 119 · 0 en trop · KB manquants : aucun |
| C2-F06 sweep v3.38.0 | RÉSERVES | RÉSERVES | adjudiqué LÉGITIME : auto-références historiques de la table des hooks (E5-POIDS/R2-CACHE, lignes 116-117) |
| C2-F07 ULTRA | PASS | PASS | SHA f40ea21e… identique hôte/dépôt |
| C2-P01 poids global | PASS | PASS | PRE : 70 skills (sans vm) · 0 CRITIQUE → POST : **71 skills · 29 OK · 33 intermédiaires · 9 LOURD · 0 CRITIQUE** |
| C2-P02 durées | PASS | PASS | campagne C2 : 342,1 ms (PRE) → 270,3 ms (POST) |

\* après calibrage du harnais (le wrapper exige `--cibles` — voir §9).

**Écart arithmétique de comptage (T3.2) RÉSOLU** : les comptages Task 72 (69 à G1-SG1.3, 70 à G2/G6) étaient mouvants au fil des disparitions/réparations successives de vm intra-journée ; l'état mesuré fait foi : hôte = 71 dirs avec vm, hôte ⊆ miroir (0 en trop), 3 tests indépendants concordants — aucun skill fantôme.

## 6. C3 — skill gen-plan du miroir : PASS 7/7

Identité **byte à byte** hôte ↔ dépôt (diff -rq vide sur SKILL.md + 15 references + scripts + evals) · frontmatter v3.39.0 (30 668 o == hôte) · PM v3.39.0 SHA 918bc692… identique (211 054 o) · KB « montée v3.39.0 » ×1 chaque côté · historiques v3.39.0 ×5 occurrences chaque côté · ULTRA SHA identique. **La sync Task 72 SG1.4 est intacte** — le miroir est conforme ; campagne C3 : 4,7 ms (PRE) / 3,2 ms (POST).

## 7. Failles → corrections ($FACON)

**Faille n°1 (unique racine) — version-management absente de l'hôte (7ᵉ récidive du jour, ~16ᵉ occurrence historique)** :
1. **Détection PRE** : 3 tests indépendants (C2-F01 integrity, C2-F02 coherence [+ 2 WARN « evals absents » conséquences], C2-F05 effectifs) — mono-racine confirmée mécaniquement (les WARN conséquences disparaissent après restauration).
2. **Correction** : garde Task 56 `ensure-installed.py --check` → **verdict INSTALLE-REPARÉ, rc=0** (copie depuis miroir local, aucun jeton, aucune action distante) — vm v1.3.0 restaurée (SKILL.md + evals + scripts).
3. **Validation POST** : integrity 0 FAIL (vm v1.3.0 = attendu) · coherence 0 FAIL · effectifs KB manquants : aucun · poids : 71 skills, 0 CRITIQUE.
4. **Cause racine revérifiée (règle d'or n°5)** : (a) `rg "rmtree|rm -rf"` — toutes occurrences sûres (tmp/selftest) ou = mécanique de réparation (ensure-installed.py:106, suppression du dossier partiel avant copytree complet) ; (b) aucun script de sync n'utilise `--delete` (C5 respectée) ; (c) git hôte ne suit pas skills/ (commits plateforme UUID, arbre propre). **Conclusion : cause environnementale** (volatilité sandbox, recyclage inter-messages — héritée du diagnostic Task 56 v3.35.2 : volatilité × angle mort × détection tardive). **Parade adéquate en place et démontrée** : garde É1-INSTALL étendue — la récidive a été détectée par la campagne et réparée en 1 commande.

**Aucune autre faille S1/S2** : les 3 FAIL initiaux de la campagne PRE provenaient tous de la racine unique vm ; les 3 bugs détectés en cours de route étaient des **bugs de harnais** (voir §9), jamais du système testé.

## 8. Performances

| Mesure | PRE | POST |
|---|---|---|
| Campagne C1 (11 tests) | 130,0 ms | 131,5 ms |
| Campagne C2 (9 tests) | 342,1 ms | 270,3 ms |
| Campagne C3 (7 tests) | 4,7 ms | 3,2 ms |
| gen-plan chargement par défaut | 29,9 Kio / 7 667 #token (INTERMÉDIAIRE rang 10) | idem (stable) |
| Écosystème (poids global) | 70 skills · 0 CRITIQUE (sans vm) | 71 skills · 0 CRITIQUE (vm comptée LOURD) |

Les 3 campagnes complètes (26 tests) s'exécutent en **~405 ms** — la surveillance complète de l'écosystème est quasiment gratuite en temps.

## 9. Bugs de harnais corrigés en round (jamais du système testé)

1. **C1-F07** : le critère cherchait l'absence de la chaîne « FAIL » dans la sortie du selftest — or les libellés de scénarios contiennent légitimement « -> FAIL (P4 seul) » ; critère v2 = « RESUME : OK » + rc=0 (idem C1-F08 : « VERDICT : PASS »).
2. **C2-F03** : le wrapper cache-verdicts.py exige `--cibles <fichier suivi>` (rc=3 + message explicite) — syntaxe calibrée `run -- <commande> --cibles <fichier>`.
3. **Synthèse v1.0.0** : le verdict global POST agrégeait aussi les verdicts PRE (pollution par le FAIL attendu) — v1.0.1 : verdict_global_post n'agrège que les POST, verdict_global_pre informatif.

## 10. Optimisation et interactions (recommandations)

1. **Détection systématique** : exécuter `task73-campagne-tests.py --cible C2` (~300 ms : effectifs + KB manquants + arbitres ×4) à l'ouverture de session post-coupure, en complément mécanique de la garde E1-INSTALL (qui reste le mécanisme d'auto-réparation canonical).
2. **Interactions re-certifiées** : KB bidirectionnelle (95 arêtes PASS coherence), réciprocités « Utilisé par », corpus ULTRA identique hôte/dépôt, citations gen-plan v3.39.0 à jour (sweep clean hors auto-références légitimes).
3. **Aucune montée de version nécessaire** : aucune évolution de contrat — la correction est une restauration ; les outils (campagne) sont des scripts racine réutilisables.

## 11. Verdicts et answer key

- Answer key du plan : **13/13 décisions verified** (re-jeu mécanique scripts/task73-rejeu-answer-key.py).
- correct-work (projet) --bloc : **PASS** (0 S1 · 0 S2 ; 3 constats S3-class résorbés en round — bugs de harnais).
- E8 final : PASS (horodatage couplé, check_plan_protocol P1-P5 PASS).
- Fenêtre native AFFICHE-PLAN (E7-DISP point 6) : affichée au début de l'exécution et mise à jour à chaque fin de groupe G1→G8.

## 12. Pendance PUSH (KO-L009 — héritage Task 71/72)

Aucun push ni manipulation de jeton par l'agent durant la Task 73. Les commits Task 73 (dépôt KNOWLEDGE-repo) sont à pousser **par le propriétaire uniquement**, après **révocation du PAT exposé** dans le chat précédent (un jeton collé en conversation doit être considéré compromis : révocation puis rotation recommandées avant tout push).
