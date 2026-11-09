# Rapport correct-work — Task 14 (écosystème Knowledge)

## Métadonnées
- **Date** : 2026-10-10 (session web-b93f42fa)
- **Mode** : PROJET
- **Version correct-work** : 2.7.0
- **Cible** : couche Task 14 — KO-L004 (régénération PM correct-work v2.7.0) + clôture C006 (skill-finder-cn) + 2 remédiations d'arbitres (classe S2-δ + garde anti-crash) + état écosystème
- **gen-plan** : v3.21.0 — couplage Étape 1 OBLIGATOIRE honoré (§1.5) : plan `download/plan-task14-cwprojet-verification.md`, answer key D001-D006, arbitre answer-key-checker **16/16 ALL PASS rc0** (E8)

## Étape 1 — Plan d'actions
Plan de vérification généré via gen-plan v3.21.0 (E1-E8, profil NORMAL, ~10 000 #token). Phases A-E séquentielles (philosophie #4) : A plan+checker · B preuves byte-level Étape 2 · C Étapes 3-4 · D Étape 5 + verdict · E rapport+worklog. Pré-vérification §10.1 : PM v2.7.0 disponible et lisible (726 L, md5 e64e85ce), version identifiée, livrables listés (6 M + 2 nouveaux download/ + tmp/). Hook É1-INSTALL frais rc0 INSTALLE (head 2992bae, kb_entrees=28).

## Étape 2 — Erreurs et omissions
Chaque claim du rapport Task 14 re-mesuré indépendamment (KO-L003 — un verdict non reproduit n'est pas une preuve). Script harnais : `task14-cw-etape2-proof.py` — **24/24 PASS rc0**.

| # | Sévérité | Description | Emplacement | Correction proposée |
|---|----------|-------------|-------------|---------------------|
| 1 | **S3 (nouveau)** | 11 scripts de harnais dormants (task17 ×3, task18 ×1, task21 ×5, task23 ×2) portent `BASE/ROOT = Path("/home/z/my-project/ecosystem")` en code exécutable — chemins stale classe S2-δ, jamais remédiés (hors périmètre Task 14 qui a corrigé les 2 arbitres vivants). Aucun invocant vivant ; échec bruyant (répertoire absent) si relancés, jamais de corruption silencieuse | `scripts/task17-*.py, task18-*, task21-*, task23-*` | Directive dédiée : correctif de masse ou dépréciation/archive des one-shots |
| 2 | S4 | Compte d'édits : plan Task 14 « 7 édits + provenance » vs rapport Task 14 « 6 édits + garde insérée + provenance » — même ensemble de 8 opérations, numérotation de l'insertion divergente (cosmétique) | plan vs rapport Task 14 | CONSERVÉE — diff réel +7/-5 (net +2 = 724→726 L) cohérent avec les deux lectures |
| 3 | — | Claims KO-L004/C006 : TOUS re-prouvés (md5 PM e64e85ce, 726 L, « ou autonome »=0, « si gen-plan disponible »=0, `[mode]` hex 5b6d6f64655d ×1, unique `ode]` autonome = mention historique de provenance légitime, sfc bare-liste 8 cas 5+/3- md5 24df0227, D004 verify-cross 0 diff) | PM + sfc | AUCUN DÉFAUT — couche conforme |

Réserves héritées consignées (non imputables à la couche Task 14, décision propriétaire en cours) : 64 enveloppes trigger_evals non canoniques (`_calibration: requise`) ; 9 dérives voie M post-francisation Task 23 (non forcées, re-mesure QUOTA_OK) ; C006 version-management (V6 3/8) ; tmp/ 13 éléments non suivi ; worklog repo arrêté à Task 24-push (sync à décider).

## Étape 3 — Structure et conflits
Script harnais : `task14-cw-etapes34-checks.py` — **16/16 PASS rc0** (avec Étape 4).

| # | Type | Vérification | Résolution |
|---|------|--------------|------------|
| 1 | Chemins stale (S2-δ) | 0 occurrence dans les 9 arbitres VIVANTS ; 11 harnais dormants = finding S3 consigné (Étape 2) | OK (périmètre vivant) |
| 2 | Compilation | compile() ×4 sans écriture (2 scripts remédiés + shim + canonique) | OK |
| 3 | Schéma replay | clé `ignores_schema_non_canonique` présente des 2 côtés (script ↔ rapport JSON) | OK |
| 4 | Conventions | kebab-case des livrables session ; PM fin `\n` ; un seul arbitre vcw racine (cale S2-α) | OK |
| 5 | Doublons/contamination | aucun rapport PROJET Task 14 préexistant écrasé ; arbre stable avant/après (lecture seule) | OK |

## Étape 4 — Interactions
| # | Artefact | Vérification | Statut |
|---|----------|--------------|--------|
| 1 | Couplage §1.5 | gen-plan installée v3.21.0 (frontmatter `skills/gen-plan/SKILL.md`) >= plancher 3.7.0 ; hook É1-INSTALL rc0 INSTALLE kb 28 head 2992bae | CONCORDANT |
| 2 | Déps correct-work | clone-chat 2.0.0 (>= 2.0.0) ; miroir §2.6 « Agent: correct-work v2.7.0 » PM ↔ SKILL.md | CONCORDANT |
| 3 | Registry KB | verify-registry-sync : 28 entrées / 28 synchronisées / ghosts 0 / 67 GAP plateforme par conception (verdict ECARTS, rc1 par conception) | = baseline Task 12 |
| 4 | 5 arbitres R2 (re-run indépendant) | vcw shim 16/16 rc0 + shim ≡ canonique à PYTHONHASHSEED=0 · integrity --check 60/60 rc0 · coherence PASS AVEC RÉSERVES 48/3/0 · verify-cross 84/84 100.0 % ERRORS 0 rc0 · generer-pm --check 3/3 COHERENT | = baseline rapport Task 14 |
| 5 | Archive ↔ corpus | archive re-scelée 28 entrées (zip direct) ; integrity 60/60 inclut checks archive | CONCORDANT |
| 6 | Replay | rapport : 29 canoniques + 64 ignores explicites = 93 fichiers evals ; sfc 8/8 ; date dérivée du commit 2026-10-09 (déterminisme B2) | CONCORDANT |

## Étape 5 — Cohérence des raisonnements
| # | Point vérifié | Résultat |
|---|---------------|----------|
| 1 | Chaîne directive → plan → exécution → verdicts | LOGIQUE — les 2 items de la directive sont clôturés avec preuves ; les 2 remédiations sont traçables (découvertes en cours, classe validée) |
| 2 | Cohérence numérique | CONCORDANTE — 93=29+64 ; 8=5+3 ; archive 28 ; PM net +2 (724→726) churn 12=--stat ; coherence 48+3+0 ; tous les scores R2 identiques au rapport Task 14 |
| 3 | Cohérence temporelle | CONCORDANTE — provenance PM 2026-10-10 ; replay 2026-10-09 = date commit audité (déterminisme, jamais d'horloge) ; plan/rapports datés 2026-10-10 |
| 4 | Résultat attendu vs obtenu | CONFORME — R2 baseline intégralement restaurée (verify-cross 83/84 → 84/84 ; integrity 59/60 → 60/60 ; coherence FAIL → PASS AVEC RÉSERVES 48/3/0) |
| 5 | Cohérence entre fichiers | AUCUN CONTREDIT — rapport Task 14 ↔ worklog 14 ↔ addendum S0 ↔ plan CW ↔ présentes mesures (40 checks) |
| 6 | Divergence persistante É5 | AUCUNE → hook AVEUGLE non déclenché (condition §1.3 non remplie — D004 résolue) |

## Calibration d'instruments (KO-L003 — honnêteté, 7 artefacts corrigés, 0 ajustement de réalité)
1. `ode]` offset : la sous-chaîne démarre à l'index +2 dans `[mode]` (pas +1) — 2 faux « autonomes » ;
2. vcw shim ≠ canonique sans graine : non-déterminisme Check 4 hérité (finding S4 Task 12) — comparaison refaite à PYTHONHASHSEED=0 : identiques ;
3. verify-cross : format réel « Vérifications : 84 / PASS : 84 » (pas « 84/84 ») ;
4. py_compile cfile=/dev/null refusé (artefact déjà documenté au S0) — compile() sans écriture ;
5. registry-sync : verdict ECARTS + rc1 PAR CONCEPTION (67 GAP plateforme) — baseline Task 12, pas un échec ;
6. diff PM « attendu +4/-2 » : supposition d'instrument — ground-truth +7/-5 cohérent (bloc §10.1 réécrit) ;
7. anti-écho « Review the changes… » : 0 occurrence réelle au fichier (grep -c — écho d'affichage pur, ×2 canaux).
Le canal d'affichage a re-avalé `[m` en direct (« `[mode]=1` » affiché « `ode]=1` ») — anomalie 2 ré-confirmée fichier par fichier.

## Résumé
- **Problèmes trouvés** : 2 nouveaux (1 S3 + 1 S4) ; 0 défaut sur la couche Task 14 elle-même
- **Corrections appliquées** : 0 (vérification en LECTURE SEULE — D003 ; la remédiation S3 relève d'une directive dédiée)
- **Problèmes restants** : finding S3 (11 harnais dormants stale) + réserves héritées listées à l'Étape 2
- **Verdict** : **PASS AVEC RÉSERVES** (§10.5 : 0 S1, 0 S2, ≥2 S3)
- **Règle d'or n°2** : 0 commit, 0 push — HEAD 2992bae inchangé ; arbre stable avant/après vérification
- **Recommandations propriétaire** : (1) GO commit + push de la couche Task 14 (6 M + 4 livrables download/ : plan+rapport Task 14, plan+rapport CW ; tmp/ à décider) ; (2) directive remédiation des 11 harnais dormants (correctif de masse ou archive) ; (3) décision 64 enveloppes (normalisation post-calibration vs extension instrument) ; (4) re-mesure voie L des 9 dérives (QUOTA_OK) ; (5) sync worklog repo (arrêté à Task 24-push) ; (6) révocation/régénération du PAT (consigné Tasks 18/22/24/13-push)
