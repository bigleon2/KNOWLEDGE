# Plan Task 14 — KO-L004 : régénération PM correct-work v2.7.0 + clôture C006 (skill-finder-cn)

## Métadonnées
- **Date** : 2026-10-10 (session web-b93f42fa)
- **Directive propriétaire** : « régénération PM correct-work v2.7.0 (KO-L004), clôture C006 (skill-finder-cn) »
- **gen-plan** : v3.21.0 (frontmatter installé — source de vérité, contrat §1.5)
- **Profil** : NORMAL (hook E1-RES : worklog lu, fraîcheur plan OK — plan nouveau)
- **Estimation #token** : ~12 000 (grille §4)
- **Règle d'or n°2** : 0 commit, 0 push sans GO propriétaire — HEAD 2992bae

## E1 — Livrables + critères de succès
1. **KO-L004 PM** : édits chirurgicaux `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` — miroir exact de la forme certifiée SKILL.md v2.7.0 (S2-β Task 12) : L175 `Agent: correct-work v2.4.0`→`v2.7.0` (§2.6) ; L176 corruption RÉELLE `ode]`→`[mode]` (byte-proof md5 3789699e) ; L540 §9.2 progression « (via gen-plan ou autonome) »→« (via gen-plan — OBLIGATOIRE, §1.5) » ; §10.1 L572-576 : 2 édits + 1 insertion garde ARRÊT EXPLICITE + 1 edit #token. Plus 1 ligne provenance KO-L004 datée 2026-10-10 (aucun faux lignage ; PAS de bump de version — calibration de forme). Succès : grep « ou autonome »=0, « si gen-plan disponible »=0, « ode] »=0, « Agent: correct-work v2.7.0 » présent, generer-pm --check 3/3, vcw 16/16.
2. **C006** : normalisation `skills/skill-finder-cn/evals/trigger_evals.json` — enveloppe objet auto-v1-t27 (1019 o, `_calibration: requise`, 8 cas intacts) → schéma canonique bare-liste, 8 cas verbatim (5 positifs / 3 négatifs). AUCUN fix instrument. Succès : json list, 8 cas query/should_trigger, verify-cross 84/84 (C006 close), check-triggers-replay inclut skill-finder-cn sans exception.
3. **R2 sweep** 5 arbitres vs baseline 2992bae + worklog Task 14 + rapport + PROPOSITION commit (GO requis).

## E2 — Ressources (mesuré)
Hook rc0 INSTALLE (head 2992bae, kb 28) ; PM 724 L md5 3789699e (stale L175/L540/L572/573/576 ; corruption réelle L176 ; lignage historique légitime L8/L74/L486-L552 intouché) ; sfc trigger_evals = objet (enveloppe auto-v1-t27 : `_provenance`/`_calibration`/`skill_name`/`evals[8]`) vs 4/4 échantillon listes canoniques ; verify-cross L96 `isinstance(list)` ; check-triggers-replay L99+L119 exige liste de dicts — report 2026-10-03, 26 skills, SANS sfc (divergence latente prouvée) ; r1-evals existence seule (insensible) ; generer-pm 3/3 (3.21.0/2.7.0/2.0.0).

## E3 — Type 2 (ingénierie écosystème — protocole + scripts ; rapport .md secondaire)

## E5 — Skills mobilisés
gen-plan (plan) · arbitres : verify-correct-work, check-ecosysteme-integrity, test-coherence-interactions, verify-cross, generer-pm-skill, check-triggers-replay · leçons KO-L003/L004 appliquées en continu.

## E7 — Séquence (série par défaut — philosophie #4)
| Phase | Contenu | #token |
|---|---|---|
| A | Plan + answer-key-checker 16/16 | 2 000 |
| B | KO-L004 : 7 édits PM + provenance + validation (grep ×4, generer-pm, vcw) | 3 000 |
| C | C006 : normalisation JSON canonique + verify-cross 84/84 + replay sfc | 2 500 |
| D | R2 sweep 5 arbitres vs baseline 2992bae | 2 500 |
| E | Rapport download/ + worklog Task 14 + proposition commit | 2 000 |

## Answer key (hook E1 — décisions D001-D006)
| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|---|---|---|---|---|---|
| D001 | 7 édits PM miroir SKILL.md v2.7.0 (§2.6 Agent, ode]→[mode], §9.2, §10.1 ×4) | grep « ou autonome »=0 ; « si gen-plan disponible »=0 ; « ode] »=0 ; « Agent: correct-work v2.7.0 » ; generer-pm 3/3 ; vcw 16/16 | directive KO-L004 + byte-proof L176 (md5 3789699e) + S2-β Task 12 | S2 | pending |
| D002 | Provenance KO-L004 journalisée au PM, PAS de bump version | ligne révision 2026-10-10 présente ; generer-pm 3/3 inchangé | convention provenance PM (L8/L493-494) | S3 | pending |
| D003 | C006 = fix DONNÉE (normalisation schéma canonique), 8 cas verbatim | json type list ; len=8 ; clés query/should_trigger ; verify-cross 84/84 | mesure échantillon 4/4 listes + validator L96 + directive | S2 | pending |
| D004 | AUCUN fix instrument (verify-cross et replay inchangés) | md5 verify-cross.py et check-triggers-replay.py inchangés avant/après | KO-L003 (forme canonique établie : 27/28 fichiers + certifications) | S2 | pending |
| D005 | Métadonnées enveloppe (_provenance/_calibration voie L) préservées au journal/rapport, hors fichier | mention rapport Task 14 + worklog Task 14 | réserve Task 23 (re-mesure R3 QUOTA_OK) | S3 | pending |
| D006 | 0 commit / 0 push sans GO ; HEAD 2992bae inchangé | git rev-parse avant/après | règle d'or n°2 | S1 | pending |

## E8 — Validation du plan
answer-key-checker.py exécuté (verdict consigné) ; fallback honnête journalisé (règle d'or n°1) si l'arbitre est inopérant dans la layout courante.

## R2 — Baselines (HEAD 2992bae)
vcw 16/16 · integrity 60/60 · coherence PASS AVEC RÉSERVES · verify-cross 83/84 (C006, 98,8 %) · generer-pm 3/3 · hook rc0 INSTALLE kb 28. **Cibles Task 14** : verify-cross 84/84 (C006 close), replay inclut skill-finder-cn, autres stables.
