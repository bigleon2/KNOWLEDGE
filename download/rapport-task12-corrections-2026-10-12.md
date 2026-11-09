# Rapport Task 12-CORRECTIONS — application des plans approuvés

**Date** : 2026-10-12 · **Session** : web-b4d7dd19 · **Mode** : gen-plan v3.23.1 STEP
**Directive propriétaire** : « Appliquer les corrections » (réponse à la pause Task 12) — périmètre : **C-12a / C-12b / C-12c** (Task 12) + **C-A / C-B** (Task 11, F1-F6) — cascade KO-L004 complète à chaque montée de version.

## 1. Montées de version exécutées

| Élément | Avant | Après | Motif |
|---|---|---|---|
| clone-chat | v2.0.0 | **v2.0.1** | C-12c : F-c1 (deps += skill-creator conventions) + F-c2 (§5.2 item 8 modèle PM-§7) |
| refactoring-engineering | v1.1.0 | **v1.1.1** | C-A : F1 (§5 baseline A2 MESURÉE 7/7) + F3 (§6 entrées v1.1.1 + v1.1.0 rétrospective) + F4 (plancher ref-test >=1.0.1) |
| refactoring-test | v1.0.1 | **v1.0.2** | C-A : F2 (§5 baseline A2 MESURÉE 7/7 les 2 voies) |
| PM SHARED | v1.7.6 | **v1.7.7** | C-12b : F-e (dé-figage 4 pins n°53 — doctrine KO-L003 alignée sur n°54/55) + refs PM (KO-L004 mécanique) |
| PM-INSTALL | v1.7.0 | **v1.7.1** | KO-L004 mécanique : §2ter row clone-chat v2.0.1 + §A.3 instantané (v1.7.1) + §7 |
| README @mon-ecosysteme | v2.1.6 | **v2.1.7** | Recalibrage manuel cascade (pattern Task 11-INSTALL) + §2 arbre (archives gen-plan×19 — ×18 stale résorbé — + clone-chat×1) |
| SYNC-CONTEXT | v1.4.8 | **v1.4.9** | Recalibrage manuel cascade |

Éditions sans montée de version : entrées §6 rétrospectives ×5 disciplines (**C-12a** : loop v1.1.0, harness v1.1.0, fleet v1.0.1, memory v1.1.1, spec-driven v1.0.1 — bumps déjà enregistrés FM+KB, entrées complétées avec mention explicite « rétrospectivement » + constat F-dx ; precedent refactor-guard 1.2.0) ; KB calibrations ×6 (clone-chat, ref-eng, ref-test + appends fleet/spec-driven/memory) ; F-g résorbé au passage (historiques-par-skill/gen-plan.md en-tête « Version vivante » v3.23.0→v3.23.1, stale Task 8).

## 2. Cascade KO-L004 (mécanique + manuelle)

1. **generer-pm-skill.py --generate clone-chat --delta** : PM `PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md` écrit (704 lignes, couverture SKILL.md↔PM complète, [OK]) ; recalibrage mécanique : SHARED v1.7.7 (refs PM + §6.1) + PM-INSTALL v1.7.1 (§2ter/§A.3/§7) ; entrée §7 v2.0.1 du PM (delta history verbatim).
2. **Archivage R4** : `git mv` PM v2.0.0 → `skills/@historique/prompts-maitres/clone-chat/` (création dossier famille) ; historiques-par-skill/clone-chat.md recalibré (vivante v2.0.1, archivées 1 PM, table 5 lignes — v2.0.0 « supplantée — archivée », v2.0.1 **VERSION VIVANTE**) ; **task21-f2-rebuild-archive.py étendu** : `RETRAITS_SANCTIONNES` + `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` + `dest_historique()` branche clone-chat (garde anti-perte maintenue — 1 PM déplacé vérifié byte-identique).
3. **propagate-context.py** : marqueurs v1.7.6→v1.7.7 (4 emplacements) + propagation **98 skills + 65 scripts + 2 agents** (idempotent : re-run 0/0/0).
4. **gen-ultra-maitre.py — extension C-B (F5/F6)** : familles 3→**4** (+REFACTOR-GUARD, regex corpus) ; ROUTING +2 routes refactoring (refactorer un élément / évaluer l'impact blast radius) ; ECO_SKILLS 21 en dur → **dérivée du registre KB** (32 rows — KO-L003, jamais plus stale) ; date de génération figée 2026-10-02 → **« État dérivé de SHARED v1.7.7 (révision 2026-10-12) — date non figée »** (déterministe, byte-idempotent ×2 vérifié) ; §3 correct-work version dynamique ; §5 +1 arête ref-eng→refactoring-test. ULTRA régénéré (109 lignes, idempotent ×2).
5. **README/SYNC** : v2.1.7/v1.4.9 avec révisions tracées (arborescence §2 recalibrée).
6. **Arbitres recalibrés** (12 substitutions verrouillées) : integrity ECO_SKILLS (clone-chat 2.0.1, ref-eng 1.1.1, ref-test 1.0.2 + 2 commentaires Task 12) ; task17 C01 (SHARED 1.7.7) / C02 (SYNC 1.4.9) / C04 (propagate v1.7.7) ; task17b C02 (tables 26/10/**5** — label stale 22 corrigé au passage) ; task9 T-R1.7 (PM-INSTALL 1.7.1) / T-R1.8 (SHARED 1.7.7 + PM-INSTALL v1.7.1) / T-R2.4 (1.1.1 + phrase hors §6) / T-R2.6 (KB 1.1.1) / T-R2.7 (ECO_SKILLS+manifeste 1.1.1).

## 3. Projection hôte (R4 double arbre)

`scripts/task12-projection-hote.py` (pattern g3 Task 9) : périmètre git status session + renommages → **109 fichiers copiés**, post-check byte-identité ×2 : 0 divergent ; exclusion R2 version-management respectée (homonymie Task 6 G8). Manifeste : `scripts/projection-hote-task12-manifest.json`.

## 4. Batterie post-corrections — VERTE ×11 fronts + pré-vol

| Front | Résultat |
|---|---|
| check-ecosysteme-integrity.py | **68/68 PASS** (archive rescellée round-trip 9/9, garde anti-perte 1/1) |
| generer-pm-skill.py --check | **4/4 COHERENT** (clone-chat v2.0.1 vivant) |
| verify-cross.py | 0 erreur — 100.0% |
| task14-scan-doublons.py | 0 doublon |
| test-coherence-interactions.py | 47/0/0 — PASS STRICT |
| task17 / task17b | 16/16 · 16/16 |
| task8-tests-n55-fusion.py | 39/39 |
| task9-tests-reserves.py | 26/26 (T-R3.3 byte-identité hôte verte post-projection) |
| VCW verify-correct-work.py | 16/16 ALL PASS |
| propagate-context.py re-run | 0/0/0 idempotent |
| outil n°55 refactoring-test-graph.py | vivant (gen-plan : blast radius CRITIQUE attendu) |
| Pré-vol ×12 cibles (task12-prevol-cibles.py) | **GO** — versions FM=KB (v1.1.1/v1.0.2/v2.0.1 incluses), SHA-256 ×2 arbres IDENTIQUE |
| Grille ×8 disciplines (task12-cible-disciplines.py) | **0 finding** (ref-eng v1.1.1 PASS pur — F1/F3/F4 résorbés) |

Rapports d'arbitres re-scellés au nouvel état (manifeste integrity, generer-pm-report, interactions-report, task9-tests-report).

## 5. Résorption des findings — bilan

| Finding | Source | Statut |
|---|---|---|
| F-c1, F-c2 (clone-chat S4) | Task 12 | **RÉSORBÉS** (v2.0.1) |
| F-d1..F-d5 (bumps non tracés ×5) | Task 12 | **RÉSORBÉS** (entrées §6 rétrospectives + calibrations KB ×3) |
| F-e (pins SHARED n°53) | Task 12 | **RÉSORBÉ** (dé-figage KO-L003, SHARED v1.7.7) |
| F1/F3/F4 (ref-eng) + F2 (ref-test) | Task 11 (C-A) | **RÉSORBÉS** (v1.1.1 / v1.0.2) |
| F5/F6 (générateur ULTRA) | Task 11 (C-B) | **RÉSORBÉS** (4 familles + routes + ECO_SKILLS KB-dérivée + date non figée) |
| F-g (en-tête gen-plan.md stale) | découverte au passage | **RÉSORBÉ** (v3.23.1) |

**0 finding restant des 13 consignés (Task 11 + Task 12)** — tous les plans de correction approuvés ont été exécutés.

## 6. Traçabilité

- Scripts Task 12 (projet hôte) : task12-corrections.py (27 opérations), task12-corrections-manuelles.py (7), task12-historiques-par-skill.py (6), task12-readme-sync.py (8), task12-recalibrage-arbitres.py (12), task12-projection-hote.py (109 copies) ; delta `KNOWLEDGE/scripts/delta-clonechat-v201.json`.
- Méthode : substitutions verrouillées (assert count==1), idempotence vérifiée (re-run = SKIP/no-op), R3 anti-fabrication (chaque entrée rétrospective ancrée sur une preuve existante : calibration KB, registre ECO_SKILLS arbitre, rapport baseline-a2-n55).
- Commits non poussés à date : 3475b17, c2811ca, ca7cf4b, 75875f6, af2220c, 4716f58 + le présent commit (règle d'or n°4 — push sur validation propriétaire explicite).
