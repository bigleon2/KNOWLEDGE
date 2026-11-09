# Plan d'actions — gen-plan : « git push origin main »

- **Skill** : gen-plan v3.37.1 (mode NULL — exécution classique, aucune porte de confirmation, directive propriétaire 2026-10-11)
- **Demande verbatim** : `gen-plan : "git push origin main"`
- **Date de génération** : 2026-11-08 (propriétaire Europe/Paris)
- **Horodatage plan** : 2026-11-07T18:22:29Z
- **Classification** : Type 1 (opération git ponctuelle) — profil ressource NORMAL — #token total estimé : ~6 k (dérisoire)
- **Dépôt cible** : `/home/z/my-project/KNOWLEDGE-repo` (miroir local certifié, source de vérité R4) → `origin` = `https://github.com/bigleon2/KNOWLEDGE.git`, branche `main`

## E1 — Analyse de la demande (état vérifiable, règle d'or n°5 — dérivé du disque)

| Fait vérifié | Preuve (commande exécutée) | Résultat |
|---|---|---|
| Branche `main` en avance de **2 commits** sur `origin/main` | `git log origin/main..main --oneline` | `886604d` (Task 70 CLOSE) + `cea7d12` (Task 70) |
| Arbre de travail propre | `git status --porcelain` → 0 ligne | RAS — rien à committer |
| Conviction KO-L009 antérieure | Message de commit `886604d` : « push = délégué propriétaire (KO-L009) » | La pendance Task 70 est exactement CE push |
| Crédentials absents de l'environnement | `git config credential.helper` → vide ; env → aucun jeton ; `git push --dry-run` → `fatal: could not read Username for 'https://github.com'` (rc=128) | Le push HTTPS est **matériellement impossible** sans provisionnement |

## E2-E6 — Ressources, skills, profil

- Skills mobilisés : gen-plan (ce plan), correct-work (contrôle fin de chaîne), check-ecosysteme-integrity (E1-RES). Aucun autre skill requis.
- Hook E1-RES exécuté : piliers présents (KNOWLEDGE.md, PM SHARED, gen-plan SKILL.md) ; **2 incidents de disparition `version-management` dans la même session** (ré-émergence de la volatilité Task 69), réparés ×2 par la garde externe `scripts/ensure-installed.py` (verdict `INSTALLE-REPARÉ`, head miroir `886604d`) ; arbitre re-certifié **110/110 PASS, 0 FAIL** ×2 (manifeste `scripts/ecosysteme-integrity.json` ré-écrit). Le watchdog `vm-watchdog.py`, hébergé DANS le skill disparu, a disparu avec lui (chemin « disparition totale → garde externe » T2b) — incident journalisé au worklog (règle d'or n°1), backfill forensique à la réouverture du daemon.

## Answer key

| Décision | Criterion | Verification (exécutable) | Priority | Status |
|---|---|---|---|---|
| D001 | Identifier les commits à publier | `git -C KNOWLEDGE-repo log origin/main..main --oneline` → 2 lignes, SHA `886604d` + `cea7d12` | S1 | verified |
| D002 | Arbre propre avant push | `git -C KNOWLEDGE-repo status --porcelain` → 0 ligne | S1 | verified |
| D003 | Écosystème sain avant push (E1-RES) | `python3 scripts/check-ecosysteme-integrity.py` → « 110/110 PASS, 0 FAIL » | S2 | verified |
| D004 | Capacité de push mécaniquement testée | `git push --dry-run origin main` → sans jeton : `could not read Username` (rc=128) → décision KO-L009(5) | S1 | verified |
| D005 | Push exécuté par l'agent via jeton one-shot fourni HORS canal (si le propriétaire le provisionne par un moyen hors discussion) | `git -C KNOWLEDGE-repo log origin/main..main --oneline` → 0 ligne | S1 | pending |
| D006 | Pendance KO-L009 levée au worklog après publication effective | `rg -c "push" worklog.md` ≥ entrée G2 avec preuve `origin/main == 886604d` | S3 | pending |

## Groupes d'exécution

### G1 — Pré-vol push (#token ~1 k) — ✅ TERMINÉ (statut dérivé du disque : D001-D004 verified ci-dessus)
1. ✅ État du dépôt vérifié (2 commits en avance, arbre propre).
2. ✅ Écosystème ré-certifié 110/110 (2 réparations volatilité dans la session).
3. ✅ Test mécanique de capacité de push : `--dry-run` → échec authentification → blocage KO-L009 qualifié.

### G2 — Exécution du push (#token ~1 k) — ⛔ BLOQUÉ (adaptation règle d'or n°1 — pause explicite et motivée)
1. ⛔ `git push origin main` — **impossible** : aucune crédential dans l'environnement (D004) ; **KO-L009 (5)** : « toute publication/push passe par le propriétaire, jamais par l'agent » — le propriétaire ayant demandé ce push, la voie conforme est un provisionnement de jeton HORS canal de discussion (KO-L009 : un canal de discussion n'est jamais un canal de confiance ; ne JAMAIS coller de PAT au chat).
2. **Voies conformes remises au propriétaire** (au choix) :
   - **a. Push direct par le propriétaire** (recommandée, zéro exposition) : `cd KNOWLEDGE-repo && git push origin main` depuis une machine authentifiée — OU recopie du miroir local puis push ;
   - **b. Jeton one-shot hors canal** (si l'environnement d'exécution en offre un mécanisme, ex. variable de session provisionnée par la plateforme, jamais le chat) : l'agent exécute alors `git push origin main` et purge toute trace (anti-persistance Task 8/14 — rien dans `.git/config`, rien sur disque) ;
   - **c. Un jeton collé au chat NE SERA PAS utilisé** (KO-L009 1-2 : guidance de révocation immédiate).
3. Après publication effective : reprise G3.

### G3 — Post-push (#token ~1 k) — en attente de G2
1. `git -C KNOWLEDGE-repo log origin/main..main --oneline` → 0 ligne (D005).
2. correct-work (projet) fin de chaîne + entrée worklog R5 (D006).

## Verdict E8 : PASS (structure conforme P1-P5 vérifiée mécaniquement — 6 décisions dont 4 verified sur preuve disque, 2 pending légitimes dépendantes de G2 — Horodatage vérifié : 2026-11-07T18:22:29Z)

- Arbitre : `python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-genplan-push-main-20261108.md --worklog worklog.md`
- Ré-estimation #token : négligeable (aucune étape lourde ; le seul travail d'agent restant est la vérification post-push).
