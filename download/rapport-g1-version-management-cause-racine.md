# Rapport G1 — Cause racine : disparition récidivante de `version-management` (Task 56, D002)

**Date** : 2026-11-06 · **Session** : web-c30e6506 · **Générateur** : gen-plan v3.35.2 (plan `download/plan-task56-version-management-zip-bloc-clone.md`)

## 1. Chaîne causale complète (chaque affirmation ancrée à un artefact — règle d'or n°5)

| # | Maillon | Preuve mécanique |
|---|---|---|
| 1 | **Phénomène plateforme** : volatilité du sandbox — suppressions de fichiers `skills/` entre les tours + recyclages inter-sessions | Worklog lignes 516, 527, 536 (« disparu de l'hôte **entre deux messages** », ×3 le jour même), 554 (5ᵉ matérialisation « Pré-flight ») ; recyclages documentés Tasks 52→53→54→55→56 (5ᵉ : `~/GitHub` détruit, livrables download/ Tasks 53-55 perdus) ; **10ᵉ matérialisation le 2026-11-06 ~21:30 (re-disparu PENDANT la session, entre deux invocations d'outils)** |
| 2 | **Angle mort de la garde d'ouverture** : `ensure-installed.py` (canonique É1-INSTALL §1.16) rendait « INSTALLE » rc=0 malgré l'absence — `installe()` = root + fichiers clés + kb_entrees ≥ 14, **sans contrôle des répertoires des 52 entrées KB** | Code source `installe()` (avant correctif) ; worklog ligne 536 (« le garde a rendu INSTALLE À TORT — angle mort : les 7 fichiers critiques n'incluent pas ce skill ») ; constat vivant 2026-11-06 21:04 : `--check` = INSTALLE rc=0 alors que integrity = 107/108 FAIL vm |
| 3 | **Réintroduction historique** : la garde étendue Task 31 (`scripts/auto-install-ecosysteme.py`, `critiques_kb()` — contrôle du SKILL.md de TOUTES les entrées KB, dérivation dynamique) **n'est plus au chemin d'invocation canonique** — remplacée de fait par `ensure-installed.py` (É1-INSTALL v3.20.0, Task 23+29) SANS reprise de la couverture étendue | `scripts/auto-install-ecosysteme.py` lignes 60-77 (garde étendue, testée 5/5 en Task 31, « fait ses preuves en production » ligne 554) ; §1.16 gen-plan (chemin canonique = ensure-installed.py seul) |
| 4 | **Détection tardive** : la perte n'était détectée que par l'arbitre `check-ecosysteme-integrity.py` (règle d'or n°9 — à l'invocation gen-plan) → restauration toujours MANUELLE et différée → fenêtres de carence prolongées → les recyclages/détections suivants rencontrent l'état carencé → **récidive structurelle** | Worklog Tasks 52, 54, 55 (« restauré » manuel à chaque fois) + leçon L55-3 (« la disparition récidivante reste inexpliquée — si récidive, investiguer la cause racine au lieu de restaurer ») |

**Total : 10 matérialisations documentées** (5 historiques pré-Task-52 + Tasks 52, 54, 55 + récidive du 2026-11-06 21:04 + re-disparition ~21:30 en session).

## 2. Correctif durable appliqué (D003) — gen-plan v3.35.2

Extension de la garde `skills/gen-plan/scripts/ensure-installed.py` (reprise du concept Task 31, R4) :
1. `etat()` dérive **dynamiquement** le SKILL.md de TOUTES les entrées KB versionnées (regex identique à l'arbitre integrity — KO-L003, jamais figé) ;
2. `installe()` exige **0 skill KB manquant** ;
3. Dérive limitée aux skills KB manquants → **AUTO-RÉPARATION** depuis le miroir local `KNOWLEDGE-repo/` (verdict `INSTALLE-REPARÉ`, rc=0, trace worklog, aucune action distante, aucun jeton) ;
4. Idempotence ×2 prouvée (2ᵉ passage = no-op).

## 3. Preuves (mécaniques, rejouables)

| Preuve | Résultat |
|---|---|
| 4ᵉ récidive réelle (21:04) | détection + réparation `INSTALLE-REPARÉ` (vm v1.2.0) — conditions réelles |
| Absence simulée (`mv` vers /tmp) | `INSTALLE-REPARÉ` rc=0 → vm restauré v1.2.0 → run 2 `INSTALLE` no-op |
| **10ᵉ matérialisation (~21:30, PENDANT la session)** | **preuve vivante en production** : la garde a auto-réparé à la volée, la session n'a pas été interrompue |
| integrity | 108/108 PASS ×2 (baseline Task 55 restaurée) |
| coherence | 53/23/0 au nadir ; reliquat §0 v1.7.24→v1.7.26 en cours de résorption via G5 (E13) |
| Cascade KO-L004 | PM v3.35.2 (1521 l., delta verrouillé `scripts/delta-genplan-v3352.json`), SHARED v1.7.25 / PM-INSTALL v1.9.3 recalibrés, PM v3.35.1 archivé R4, pin ECO_SKILLS 3.35.2, KB, historiques, archive rescellée (15 entrées), sync miroir byte-identique, verify-correct-work 16/16 |

## 4. Ce qui ne peut plus se reproduire (réponse à la demande propriétaire)

La disparition **physique** peut encore se produire (phénomène plateforme externe, incontrôlable), mais elle est désormais **impossible à ne pas remarquer et impossible à laisser persister** : toute invocation de gen-plan (hook É1-INSTALL en préemption, règle d'or n°9 à toute invocation) détecte ET répare automatiquement depuis le miroir local — dans cette discussion comme dans toutes les futures (le correctif est versionné v3.35.2, synchronisé profil + miroir ; **pendance propriétaire : push distant sur GO** — KO-L009 point 5).

## 5. Leçons (knowledge-observer — E15)

- **L56-1** : la substitution d'une garde par une autre doit prouver la COUVERTURE de l'ancienne (le remplacement Task 23/29 a silencieusement réintroduit l'angle mort que Task 31 avait résorbé) — toute substitution de garde exige un diff de couverture documenté.
- **L56-2** (clôture L55-3) : la cause racine de la récidive version-management était TRIPLE (plateforme × angle mort × détection tardive) — restaurer sans investiguer (comme aux Tasks 52/54/55) entretenait le cercle ; l'investigation demandée par L55-3 l'a brisé.
- **L56-3** : le miroir local `KNOWLEDGE-repo/` (dans le projet) survit aux recyclages qui détruisent `~/GitHub` — c'est la source de réparation locale de référence pour la garde étendue.
