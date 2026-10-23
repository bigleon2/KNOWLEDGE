# Rapport correct-work (projet) — Task 25ter (alias-eco v1.2.0 + régénération gen-plan)

## Métadonnées
- **Date** : 2026-10-23 · **Mode** : PROJET (correct-work v2.8.0 — couplage gen-plan v3.23.2, plan régénéré conforme)
- **Cible** : directive propriétaire 5 puces (GO grammaire B, analyse/optimisation, tests, correct-work, clone-chat)
- **Particularité** : compensation du contrat mode step (correct-work(groupe) ×G-A..G-D) + analyse approfondie du constat propriétaire « gen-plan n'a pas généré de plan d'actions comme d'habitude »

## Étape 1 — Plan d'actions
Plan régénéré conforme au protocole v3.23.2 : `download/plan-task25ter-grammaire-b-alias-eco.md` — directive verbatim + état d'entrée + hooks E1-RES tracés (É1-INSTALL INSTALLE rc=0 ; monitor niveau 0) + groupes + answer key D001-D007 (7/7 conformes au template, vérification mécanique des champs) + routage outils §1.16.

## Étape 2 — Erreurs et omissions

| # | Sévérité | Description | Emplacement | Correction |
|---|----------|-------------|-------------|------------|
| 1 | **S2 — corrigée** | **Dérive protocole gen-plan** (constat propriétaire) : post-compaction, le PM v3.23.2 n'a pas été rechargé — plan initial sans directive verbatim/état d'entrée/hooks E1-RES, correct-work(groupe) non exécutés, answer-key-checker non invoqué | plan-task25ter v1 (remplacé) | PM rechargé (B-11) ; hooks exécutés ; plan RÉGÉNÉRÉ conforme (L005/D012) ; leçon L009 journalisée (G-G) |
| 2 | S3 — corrigée | `cp` de propagation archive dans le mauvais sens → archive hôte fraîche écrasée par la copie périmée du dépôt (integrity 75/78 puis 77/78) | session (scripts) | re-scellement hôte + propagation hôte→dépôt sens unique → **integrity 78/78** |
| 3 | S3 — corrigée | Pollution du registre local par des entrées de test (`LOC-TEST/LOC-TEST2`) | profil local @Alias | re-projection depuis la source (R4) |
| 4 | S3 — documentée | `$façon()` : alias non enregistré, hors format canonique (3 violations) — usage traité comme mandat d'attribution → **OPT-TRIO** attribué (dogfooding), signalé non expansé | registre @Alias | attribué + tracé (journal v1.2.0) |
| 5 | S3 — corrigée | Arbitre `check-ecosysteme-integrity.py` : ECO_SKILLS figé `alias-eco: 1.0.0` | scripts (dépôt+hôte) | recalibré 1.2.0 (KO-L004, commentaire tracé) |

0 S1 ouvert. La dérive protocole (n°1) est la plus grave : corrigée et institutionnalisée par la leçon L009.

## Étape 3 — Structure et conflits

| # | Contrôle | Résultat |
|---|----------|----------|
| 1 | alias-eco v1.2.0 : SKILL.md (§1.2 grammaire B, §2.2 --trigger, §4), format-alias §1, script, YAML ×2 | OK — cohérents dépôt ↔ profil |
| 2 | Cascade : KB v1.2.0, journal row, PM-INSTALL v1.8.3 (§A.3), SYNC v1.5.3, README v2.1.11, historique-autres-elements ×5, ULTRA (alias-eco 1.2.0) | OK — cohérence multi-surface |
| 3 | Corpus/archive : 9/9 byte-identiques (v2.2 corpus-seul, piliers retirés sanctionnés v2.3→v2.2 — conforme) | OK |

## Étape 4 — Interactions

| # | Interaction | Statut |
|---|-------------|--------|
| 1 | correct-work v2.8.0 → alias-eco >= v1.0.0 (délégation §10.1) | OK — version satisfaite (1.2.0) |
| 2 | alias-eco → registre KB (entrée v1.2.0) + ULTRA (table dérivée KB) | OK |
| 3 | PM-INSTALL §A.3 instantané = KB = frontmatter (1.2.0) | OK — 0 drift |
| 4 | @historique (R4) : journal + historique-autres-elements alimentés, 0 duplication | OK |

## Étape 5 — Cohérence des raisonnements (compensation correct-work(groupe))

| Groupe | Verdict | Preuves |
|--------|---------|---------|
| G-A grammaire B | **PASS** | selftest 21/21 ×2 (dépôt+hôte) ; parse 100% des cas grammaire B ; rejet propre façon() et `(chat)` ; trigger_evals 9 cas |
| G-B OPT-TRIO | **PASS** | `--list` : OPT-TRIO → phrase (source tracée) ; `--resolve` expansions ECO-LEON+OPT-TRIO ; idempotence re-`--trigger` (alias préservé) |
| G-C cascade | **PASS** | pipeline ×2 rc0 (SHA 37/37, 0 divergence) ; ULTRA régénéré ; integrity **78/78** ; verify-cross **111/111** ; PM-INSTALL v1.8.3 / SYNC v1.5.3 / README v2.1.11 cohérents |
| G-D tests | **PASS** | replay alias-eco **9/9** (description inchangée), 19 dérives documentées inchangées, 0 nouvelle ; py_compile ×2 ; YAML ×2 |

Hook Second Opinion : non déclenché (0 FAIL persistant à l'Étape 5).

## Résumé
- **Problèmes trouvés** : 5 (1 × S2 protocole — corrigée ; 4 × S3 — corrigées/documentées)
- **Corrections appliquées** : 5
- **Problèmes restants** : 0
- **Verdict** : **PASS** — alias-eco v1.2.0 certifié, déclencheur grammaire B opérationnel et testé, OPT-TRIO attribué, cascade complète, protocole gen-plan rétabli et leçon institutionnalisée (L009)
