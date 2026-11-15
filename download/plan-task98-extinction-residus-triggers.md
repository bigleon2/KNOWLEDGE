# Plan — Task 98 : extinction des résidus triggers (GO propriétaire — midi-doc-expert 5/6 + re-curation 9/12) + PUSH intermédiaire

**Directive propriétaire** trace `1a1df74c670cddc1` « GO avec ma clé "<PAT fourni dans la discussion courante>" » — 2 items : (1) PUSH du commit en attente avec la clé ; (2) GO sur la Task 98 d'extinction des 4 résidus triggers de l'arbitre V6.2 (99/101 — voies d'extinction documentées Task 97 G1.5).
**Référentiel à l'ouverture** : HEAD `5a7b983` (Task 97 SUIVI) poussé · worklogs parité 2 295 · cron 531684 ACTIF (tick 15:00 CET imminent) · arbitres ×6 AU VERT (suite 141).

---

## Incident de milieu de tour (consigné suites 142-143 — deux réparations convergentes)

Au tick 15:00 CET (14:00 UTC), **wipe inter-sessions §3.4** (recyclage sandbox) : `.git` local restauré à l'état Task 93 (`32706b4`, reflog figé, 0 objet des commits Task 94-97/`5a7b983`), worklog dépôt retombé à 2 273 lignes, scripts V6.2 écrasés par les formes anciennes — worklog hôte (2 295, suite 141) et download/ INTACTS. **Le PUSH du item 1 (13:51) avait sauvé tout l'historique : 0 perte définitive.** Deux réparations convergentes et indépendantes : le tour GO (fetch ANONYME — 0 exposition — puis `reset --hard origin/main`, pipeline, rescellement, certification 6/6) et le tour cron tick 15:00 (suite 142, commit `c276680c` poussé). Leçon renforcée : **pousser dès qu'un PAT frais est fourni**.

## Enquête E1-E2 (read before planning)

- **4 dérives exactes** (rapport triggers) : midi-doc-expert cas 5 « Valide la conformité de ce TSI au schéma de référence. » (attendu False, trig True — hits {refer, valid}) ; re-curation cas 1 « Re-cure mon skill version-management… » (attendu True, hits {skill}) ; cas 7 « re-cure l'élément n°1… » (attendu True, hits {elem}) ; cas 10 « Optimise les dépendances npm… » (attendu False, hits {depend, optimis}).
- **Mécanismes** (code de l'arbitre) : veto `exclusifs` = champ optionnel PAR CAS (expressions, sous-chaîne normalisée — précédent Task 30 « vetos croisés ») ; lexique voie M = nom + description + tags — les TAGS ne sont PAS découpés sur le tiret (un tag « re-cure » ne matcherait jamais le token « cure » → voie description) ; le read_when de re-curation documentait déjà « re-cure »/« re-curer » mais le lexique mécanique non.
- **Doctrine versions** : midi-doc-expert = révision documentaire SANS bump (précédent Task 30 exact) ; re-curation = PATCH + description ADDITIVE (précédent v1.2.0) + cascade légère (KB, pin ECO_SKILLS L77, historique, arbitres, sync). PM midi-doc-expert non concerné (projette le SKILL.md, pas les evals).
- Artefact d'enquête corrigé : le harnais task97-simulation-v62.py EXISTE dans l'arbre sain (son « absence » constatée à 14:07 était un artefact de l'arbre restauré ancien).

## G1 — Simulation préalable (règle d'or n°5)

Harnais `scripts/task98-simulation-extinction.py` : réplique EXACTE des 4 couches (veto → voie M → cache L → V6.2) **par import des fonctions de l'arbitre** (zéro duplication R4) + deltas en mémoire (Δ1 exclusifs midi cas 5 ["valide la conformité"] · Δ2 exclusifs re-curation cas 10 ["npm"] · Δ3 description re-curation += ' (forme verbale : "re-cure")'). S1 baseline 99/101 ✓ cohérent · S2 chaque delta isole sa cible (1+1+2 réparations, 0 régression) · S3 rejeu global simulé **101/101, exactement 4 réparations cibles, 0 régression, 0 autre changement** · S4 **GO** (rc=0). Rapport `scripts/task98-simulation-report.json` (déterministe, sans horloge — capture pré-implémentation conservée comme preuve).

## G2 — Implémentation + cascade légère

1. `skills/midi-doc-expert/evals/trigger_evals.json` : cas 5 += exclusifs ["valide la conformité"] (la validation relève de tsi-validator — tandem).
2. `skills/re-curation/evals/trigger_evals.json` : cas 10 += exclusifs ["npm"].
3. `skills/re-curation/SKILL.md` : description ADDITIVE ligne « (forme verbale : "re-cure") » + version 1.2.2 → **1.2.3** (PATCH, additions pures).
4. Cascade : registre KB (titre v1.2.3 + Dernière calibration) · pin ECO_SKILLS integrity (1.2.3 + commentaire KO-L004) · historique re-curation.md (en-tête rattrapé + ligne v1.2.3, famille 4 versions) · midi-doc-expert.md (Révisions documentaires += Task 98) · harnais + rapport copiés dans scripts/.

## G3 — Rejeu réel

`check-triggers-replay.py` : **101/101 — PASS, 0 dérive, 0 non-resorbe** (sources : voie-m + veto-exclusif + cache + V6.2 inchangés ailleurs). Précédent 99/101 → l'objectif du GO est atteint intégralement.

## G4 — $FACON2

Idempotence ×2 : 3 rejeux → **3 SHA byte-identiques `c1ff466e`** ; performance médiane ×3 : **0,148 s** vs baseline V6.2 0,146 s = **+1,4 % < garde 30 %** ; réinstallation hôte voie directe (55/55 SHA, 0 divergence, R2 0 rétrogradation) + ressellement archive piliers (task21-f2) ; arbitres ×6 AU VERT (certification-complete ALL PASS 6/6 — tool-routing 8/8 : les 2 skills modifiés vérifiés).

## G5 — Worklog + miroirs + commit + PUSH + résumé

Suite 143 (hôte + dépôt, parité) ; plan dans download/ ×2 (hôte + dépôt) ; commit « Task 98 CLOSE » + PUSH avec la clé du GO (E15 : 25ᵉ exposition, 6ᵉ utilisation — ROTATION IMPÉRATIVE) ; résumé concis au propriétaire en français (règle d'or n°6).

---

## Answer key (preuves vérifiables par décision)

| ID | Décision | Preuve mécanique |
|----|----------|------------------|
| D001 | PUSH item 1 effectué, 0 unpushed | push `b603285..5a7b983` + ls-remote = `5a7b983` (E15 22ᵉ) |
| D002 | Incident wipe réparé, 0 perte | fetch + reset --hard origin/main + parité worklogs 2 297 + certification 6/6 pré-Task 98 |
| D003 | Simulation préalable GO | task98-simulation-report.json : S1 99/101 · S3 101/101 simulé · 4 réparations cibles · 0 régression |
| D004 | Arbitre 101/101 réel | triggers-replay-report.json : verdict PASS, 0 dérive, 0 non-resorbe |
| D005 | Description ADDITIVE (aucune suppression) | git diff skills/re-curation/SKILL.md : additions pures (+1 ligne description, version bump) |
| D006 | Cascade cohérente v1.2.3 | KB titre + calibration · pin ECO_SKILLS 1.2.3 · historique 4 versions · verify-cross 165/165 · integrity 114/114 |
| D007 | Idempotence ×2 | 3 SHA c1ff466e byte-identiques |
| D008 | Performance dans la garde | médiane ×3 0,148 s vs 0,146 s (+1,4 % < 30 %) |
| D009 | Arbitres ×6 AU VERT avant commit | certification-complete ALL PASS 6/6 · tool-routing 8/8 (2 skills modifiés) |
| D010 | Commit + PUSH + E15 + résumé français | git log « Task 98 CLOSE » + ls-remote + suite 143 + réponse finale |

*Plan Task 98 — gen-plan mode step v3.43.0, enquête E1-E2 terminée (4 dérives exactes · mécanismes veto/lexique · précédents Task 30 / v1.2.0 · incident wipe réparé en cours d'ouverture).*
