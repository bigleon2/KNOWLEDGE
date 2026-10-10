# Plan Task 15 — traitement des décisions restantes : S3 dormants, 64 enveloppes, tmp/, rétro-sync worklog

## Métadonnées
- **Date** : 2026-10-10 (session web-b93f42fa)
- **Directive propriétaire** : « traite les décisions restantes : 11 harnais dormants (S3), 64 enveloppes, disposance, rétro-sync repo. "tmp/" »
- **gen-plan** : v3.21.0 (frontmatter installé `skills/gen-plan/SKILL.md` — source de vérité, contrat §1.5)
- **Hook É1-INSTALL frais** : rc0 INSTALLE (head b36f177, kb 28, 0 manquant)
- **Profil** : NORMAL
- **Estimation #token** : ~12 000 (grille §4)
- **Règle d'or n°2** : 0 commit, 0 push sans GO propriétaire — HEAD b36f177 (= origin/main)

## E1 — Livrables + critères de succès
1. **D002 (préalable) — re-scellement archive 28→27** : la suppression distante `d72226a` (clone-discussion-2026-09-27-…-b13-r7-f.md, décision propriétaire UI web) a rompu le round-trip archive↔corpus (integrity 58/60, coherence FAIL). Évolution de `scripts/task21-f2-rebuild-archive.py` (instrument VIVANT, liste LIVE 14-CW) : retrait sanctionné explicite (liste `RETRAITS_SANCTIONNES`), protection anti-perte conservée pour tout autre extra. Calibration `scripts/ecosysteme-integrity.json` : retrait du fichier des dicts `archive` + `corpus` (28→27), nouveau sha256 du zip dans `download`. Succès : integrity 60/60 rc0 ; coherence PASS ; zip gitignoré (*.zip — aucun commit zip).
2. **D001 — normalisation 64 enveloppes** : les 64 `skills/*/evals/trigger_evals.json` hors schéma canonique (100 % homogènes : `{_calibration,_provenance,evals,skill_name}`, 512 cas = 8/skill, 0 anomalie) → schéma canonique bare-liste, 512 cas verbatim (précédent C006 Task 14 : enveloppe supprimée, « absente »). Métadonnées `_provenance`/`_calibration` préservées HORS données (rapport + worklog — precedent D005 Task 14). AUCUN fix instrument. Succès : 64 json list ; replay `ignores_schema_non_canonique`=0, `n_skills`=93, dérives documentées honnêtement ; verify-cross 84/84 ; md5 arbitres inchangés.
3. **D003 — archivage des 11 dormants (finding S3)** : critère calibré reproduit à HEAD (chaîne `my-project/ecosystem` présente, hors 9 instruments VIVANTS ; stale_live=AUCUN) : task17 ×3, task18 ×1, task21 ×5 (f3-status-mesure, p2b-pass2, p2b-kb-decision, p2b-kb-sync, p4b-pass2), task23 ×2 → `git mv` vers `scripts/_archive/` (précédent task40-cw-projet.py). Aucun correctif de masse (zéro churn sur scripts one-shots historiques). Succès : 11 fichiers dans `_archive/` ; 0 dormant restant ; les 9 vivants md5 inchangés.
4. **D004 — disposition tmp/ + D005 rétro-sync** : suppression `tmp/` (13 artefacts Task 12 reproductibles : t12-* ×11, r5-token-dashboard.json, vrs-full.json ; 64 Ko ; 0 référence vivante — refs trouvées = /tmp système + docstring phase2). Rétro-sync : port verbatim des entrées de campagne 0→14-CW (19 entrées, excl. 14-push déjà présent) du worklog de session vers le worklog du dépôt, avec préambule de désambiguïsation vs ancienne campagne web-8a7e5653 (homonymes Task 12/13/14 laissés en place). Succès : tmp/ absent ; 19 Task IDs présents au dépôt ; préambule explicite.

## E2 — Ressources (mesuré)
Hook rc0 INSTALLE (b36f177, kb 28) ; 64 enveloppes homogènes 512 cas (sonde Python) ; archive zip 28 entrées 448 Ko, gitignore l.17 ; integrity.json : archive=28/corpus=28 (fichier supprimé dans les 2), skills=28 ECO (sha256 SKILL.md — non affecté par evals, 0 occurrence « evals » au checker), download=1 pin sha256 zip ; F2 = instrument vivant refusant par design tout extra hors homologues (protection) ; 11 dormants reproduits exactement (stale_live=AUCUN) ; `_archive/` existe (5 entrées) ; tmp/ = 13 fichiers 64 Ko ; worklog dépôt 519 L (arrête ancienne campagne à 24-push + 14-push) vs externe 390 L (campagne complète 0→14-push) ; harnais session 14-CW : 4 FAIL = 2 péremptions attendues (HEAD/arbre calibrés pré-commit) + 2 recalibrations réelles (traitées par D002).

## E3 — Type 2 (ingénierie écosystème — protocole + scripts ; rapport .md secondaire)

## E5 — Skills mobilisés
gen-plan (plan) · arbitres : check-ecosysteme-integrity, test-coherence-interactions, check-triggers-replay, verify-cross, verify-correct-work (via shim), generer-pm-skill · instrument : task21-f2-rebuild-archive.py (évolué, D002) · leçons KO-L003 (anti-écho byte-level) appliquées en continu.

## E7 — Séquence (série par défaut — philosophie #4)
| Phase | Contenu | #token |
|---|---|---|
| A | Plan + answer-key-checker 16/16 | 2 000 |
| B | D002 : F2 évolué + integrity.json calibré + re-scellement + integrity 60/60 + coherence PASS | 2 500 |
| C | D001 : normalisation 64 (script mécanique) + replay 93 skills + verify-cross | 2 500 |
| D | D003 archivage git mv ×11 + D004 rm tmp/ + D006 recalibration harnais session | 1 500 |
| E | D005 : rétro-sync verbatim (port 19 entrées + préambule) | 1 500 |
| F | R2 sweep 5 arbitres + rapport + worklog interne/externe + proposition commit | 2 000 |

## Answer key (hook E1 — décisions D001-D006)
| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|---|---|---|---|---|---|
| D001 | 64 enveloppes → bare-liste canonique, 512 cas verbatim, métadonnées hors données, 0 fix instrument | 64 json list ; len total 512 ; replay ignores=0 n_skills=93 ; md5 check-triggers-replay.py + verify-cross.py inchangés | précédent C006 (sfc : enveloppe absente) + sonde homogénéité 64/64 | S2 | pending |
| D002 | Re-scellement 28→27 : F2 évolué (retrait sanctionné), integrity.json calibré (archive+corpus+pin download) | integrity 60/60 rc0 ; coherence PASS ; zip 27 entrées round-trip ; F2 refuse tout extra non sanctionné (test) | d72226a (décision propriétaire) + logique F2 + finding 14-CW (zip=28/corpus=27) | S2 | pending |
| D003 | Archivage des 11 dormants (git mv → scripts/_archive/), aucun correctif de masse, 9 vivants intacts | 11 fichiers dans _archive/ ; 0 `my-project/ecosystem` hors _archive/ + LIVE ; md5 ×9 vivants inchangés | critère calibré 14-CW reproduit + précédent _archive (task40) | S3 | pending |
| D004 | tmp/ supprimé (13 artefacts reproductibles, 0 référence vivante) | tmp/ absent ; inventaire documenté au rapport | sonde tmp/ + grep références (rc1) | S3 | pending |
| D005 | Rétro-sync verbatim 0→14-CW (19 entrées) + préambule campagne, homonymes ancienne campagne intacts | 19 Task IDs présents au worklog dépôt ; préambule présent ; lignes 250-295 (ancienne campagne) inchangées | gap consigné 14-CW + Task 0 (origine campagne) | S2 | pending |
| D006 | Règle d'or n°2 : 0 commit/push sans GO ; recalibration harnais session (2 attentes périmées) | git rev-parse b36f177 avant/après ; harnais session dynamisé | règle d'or n°2 + constat péremption | S1 | pending |

## E8 — Validation du plan
task15-answer-key-check.py (16 checks mécaniques) exécuté après exécution ; verdict consigné au rapport ; fallback honnête journalisé si arbitre inopérant (règle d'or n°1).

## R2 — Baselines (HEAD b36f177, mesuré)
vcw 16/16 (shim) · integrity 58/60 (2 FAIL calibration D002) · coherence FAIL (1 round-trip D002) · verify-cross 84/84 · generer-pm 3/3 · replay 29 canoniques + 64 ignores, 20 ok / 9 dérives · hook rc0 INSTALLE kb 28. **Cibles Task 15** : integrity 60/60, coherence PASS, replay ignores=0 n_skills=93 (dérives documentées), vcw 16/16, verify-cross 84/84, generer-pm 3/3 stables.
