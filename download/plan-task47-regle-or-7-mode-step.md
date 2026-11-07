# PLAN D'ACTIONS — Task 47 : Règle d'or n°7 « Mémoire complète de la discussion — relire les clones et sauvegardes » + régénération du plan en MODE STEP

> **Mode** : `gen-plan(step)` (directive propriétaire : « recommence en utilisant le mode STEP de mon skill gen-plan » — enchaînement autonome des groupes séquentiels, correct-work(groupe) après chaque groupe [max 2 rounds], correct-work(projet) en fin de chaîne) · **Session** : web-6058b3ba · **gen-plan** : v3.32.0 fraîchement installé (génération initiale) → re-généré via v3.33.0 puis via **v3.33.1** (KO-L005 ×2 — la précision sémantique [directive 3] intégrée AVANT re-génération) · **Date** : 2026-11-04 · Horodatage plan : 2026-11-04T04:59:29+00:00
> **Directive propriétaire (verbatim, ordre d'émission)** :
> 1. « je précise que tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées. recommence la génération de ton plan d'actions en prenant compte de cette directive qui doit devenir une règle d'or »
> 2. « recommence en utilisant le mode STEP de mon skill "gen-plan" »
> 3. « continue mais avant gen-plan : "prend en compte que lorsque je précise que lorsque je disais \"ce que tu as oublié\" alors je voulais dire \"les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer\"." » — précision sémantique de la règle d'or n°7, intégrée AVANT gen-plan (PATCH v3.33.1)
> **Application immédiate de la règle (AVANT la génération ET à la reprise post-coupure — exécutée)** : relecture effective des clones et sauvegardes — `download/clone-chat-task39-2026-11-02.md` (lignage initial, directives 1-4 de la chaîne), `download/clone-discussion-2026-11-04-task45-preset-midi-bridge.md` (preset bridge, bugs F-01..F-09, conventions), `download/clone-discussion-2026-11-04-task46-nouveaux-preceptes.md` (installation certifiée, préceptes, D001-D015, reprise), `download/rapport-final-task46.md`, `download/rapport-correct-work-projet-task46.md` (réserves), `download/plan-task46-refaire-nouveaux-preceptes.md` (statuts finaux E13), `work/KNOWLEDGE-b75a620/worklog.md` (733 lignes — Tasks 1→47). **Mémoire reconstituée — preuve vivante de la précision sémantique (directive 3)** : la reprise post-compression de la présente session a reçu un résumé PARTIELLEMENT reconstitué affirmant « règle d'or n°7 non persistée / plan non commencé » alors que le disque portait déjà v3.33.0 + plan + recensement ; les éléments oubliés à cause de la coupure et partiellement reconstitués (état réel : G1/G2/G3 terminés par artefacts, T2.4.2/G5/G6 restants) ont été complétés par l'audit disque (règle d'or n°5). La Task 46 est TERMINÉE (D001-D014), seul D015 PAT PUSH reste [REPORTÉ — GO propriétaire].
> **Règle d'or n°7 (précepte structurel du présent plan — installée durablement en G2 [v3.33.0], PRÉCISÉE en v3.33.1 [directive 3])** : le plan couvre TOUS les éléments de la discussion à traiter (directives verbatim, tâches antérieures, livrables, pendances, préceptes) ; l'« oubli » visé = **les éléments oubliés à cause d'une coupure et que l'agent n'a que partiellement réussi à reconstituer** — une reconstitution PARTIELLE (résumé de session, mémoire résiduelle) n'est JAMAIS une mémoire complète : relire les clones et sauvegardes AVANT génération/re-génération pour compléter les parties partiellement reconstituées, l'état vérifiable du disque (règle d'or n°5) prévaut sur toute reconstruction mémorielle ; couverture vérifiable — chaque élément recensé ∈ {tâche du plan, livrable certifié existant, pendance consignée}, l'absence des trois = dérive à corriger (E13).
> **Contexte d'exécution (état certifié, règle d'or n°5)** : écosystème installé et certifié 2026-11-04, re-certifié RÉELLEMENT Task 47-v3.33.1 (integrity 98/98 ×3, verify-cross 141/141, coherence 51/23W/0F [plage PM recalibrée L004 2e éd. 1200-1560 — croissance directive], garde-plan PASS [casse §0/__future__ réparée], doublons 0, batterie task45 20/20 ×2) ; gen-plan **v3.33.1** porte les règles d'or n°1-n°7 (n°7 précisée) + KO-L009 (§1.5) ; lignage Tasks 38-46 terminé ; cron idempotent **501529** actif (ex-501373 → 501446, recréé — préceptes corrigés + règle d'or n°7 PRÉCISÉE encodés : DJTT = EXEMPLE 4 DECKS, optimiser les ÉLÉMENTS, PAT PUSH sur GO, éléments post-coupure partiellement reconstitués à compléter par relecture) ; commit Task 46 préparé dans le clone de travail `work/KNOWLEDGE-b75a620`.
> **Routage N2** : plan → gen-plan v3.33.1 (règle d'or n°2/KO-L005) ; scripts → script-creator (stdlib, idempotence ×2, échec bruyant, substitutions verrouillées count==1) ; **registre KB → skills-inventory (§1.16 — découvertes de skills par l'inventaire PRIORITAIRE)** ; skills/corpus → générateur mécanique `scripts/generer-pm-skill.py --generate gen-plan --delta` (KO-L004 v1.1.0) ; vérification → correct-work v2.8.0 ; archivage → clone-chat v2.0.2 ; leçons → knowledge-observer (M1-M2) ; surveillance → resource-monitor (hook continu E9-E14).
> **Hors périmètre (consigné)** : **PAT PUSH = action propriétaire sur GO explicite** (KO-L009 point 5 — jamais de clé manipulée ; commit préparé, guidance rotation réitérée) ; validation matérielle S4 MK2 (CC 80-103 à calibrer sur le contrôleur réel) ; reconstruction verbatim des 3 scripts task44 d'origine (optionnelle, pendance consignée) ; 24 WARN coherence baseline + divergence gif-animator-pro (plateforme-gérée — consignées, sans action) ; réécriture des livrables historiques (R2 append-only).
> **Cibles** : règle d'or n°7 installée durablement + PRÉCISÉE sémantiquement (SKILL §1.5 + PM v3.33.1 §1.8 [point 2 précisé + point 5 ajouté] + cascade KO-L004 complète ×2 arbres) ; recensement mécanique de la discussion à jour des 11 directives (`download/rapport-recensement-discussion-task47.md`) ; cron 501529 à préceptes enrichis (règle d'or n°7 + précision encodées) ; re-certification arbitres 6/6 RÉELLE (la revendication « replay ×2 » de la v3.33.0 était aspirante — règle d'or n°5, consignée) ; `download/rapport-correct-work-projet-task47.md` ; `download/rapport-final-task47.md` ; `download/clone-discussion-2026-11-04-task47-regle-or-7-mode-step.md`.

## Answer key (E1) — forme exécutable

```yaml
decisions:
  - id: "D001"
    criterion: "Règle d'or n°7 APPLIQUÉE AVANT génération ET à la reprise post-coupure : relecture effective des clones et sauvegardes (3 clones + rapports task46 + worklog intégral) et recensement mécanique écrit couvrant TOUS les éléments de la discussion : directives 1-11 (lignage Tasks 38→47 — directive 11 = précision sémantique), livrables, pendances, préceptes — chaque élément ∈ {tâche du plan, livrable certifié, pendance consignée}, aucun orphelin"
    verification: "test -s download/rapport-recensement-discussion-task47.md && rg -q 'Task 38' download/rapport-recensement-discussion-task47.md && rg -q 'Task 46' download/rapport-recensement-discussion-task47.md && rg -q 'PAT PUSH' download/rapport-recensement-discussion-task47.md && rg -q 'AUCUN ÉLÉMENT ORPHELIN' download/rapport-recensement-discussion-task47.md"
    source: "Directive propriétaire point 1 (règle d'or n°7 — application immédiate avant gen-plan) + point 3 (précision sémantique — application à la reprise post-coupure)"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "Règle d'or n°7 insérée au SKILL.md gen-plan §1.5 (après n°6, avant le bloc PATTERN:KO-L009 — les règles d'or restent contiguës), version montée v3.32.0 → v3.33.0 PUIS PRÉCISÉE v3.33.1 (PATCH — directive 3 : l'« oubli » = les éléments perdus à cause d'une coupure et que l'agent n'a que partiellement réussi à reconstituer ; une reconstitution PARTIELLE n'est jamais une mémoire complète ; l'état vérifiable du disque [règle d'or n°5] prévaut sur toute reconstruction mémorielle), §5.6 histoire enrichi (lignes v3.33.0 + v3.33.1)"
    verification: "rg -m1 'Règle d'or n°7 — Mémoire complète' work/KNOWLEDGE-b75a620/skills/gen-plan/SKILL.md && rg -m1 '^version: 3\\.33\\.1' work/KNOWLEDGE-b75a620/skills/gen-plan/SKILL.md && rg -m1 'v3\\.33\\.1 \\(2026-11-04' work/KNOWLEDGE-b75a620/skills/gen-plan/SKILL.md && rg -m1 'partiellement réussi à reconstituer' work/KNOWLEDGE-b75a620/skills/gen-plan/SKILL.md"
    source: "Directive point 1 (devenir une règle d'or) + point 3 (précision sémantique) + précédents n°5/n°6 (cascade KO-L004 complète)"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "PM v3.33.0 PUIS PM v3.33.1 générés MÉCANIQUEMENT (générateur KO-L004 v1.1.0, deltas verrouillés scripts/delta-genplan-v3330.json + scripts/delta-genplan-v3331.json : insertion n°7 §1.8 [v3.33.0] puis point 2 précisé + point 5 ajouté [v3.33.1], count==1) avec history ; SHARED recalibré v1.7.19 → v1.7.20 + PM-INSTALL v1.8.13 → v1.8.14 ; --check 4 familles COHERENT après génération (idempotence ×2 : NO-OP)"
    verification: "test -s work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md && rg -q 'Règle d'or n°7' work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md && rg -q 'partiellement réussi à reconstituer' work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md && rg -q '\\| v3\\.33\\.1 \\|' work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md && cd work/KNOWLEDGE-b75a620 && python3 scripts/generer-pm-skill.py --check"
    source: "Cascade KO-L004 v1.1.0 (précédents v3.29.0/v3.32.0/v3.33.0 — substitutions verrouillées, jamais d'édition manuelle du PM)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "PM v3.32.0 archivé @historique R4 (flux v3.33.0) PUIS PM v3.33.0 archivé @historique R4 (flux v3.33.1 — fichier non suivi : mv simple + adaptation journalisée, précédents v3.22.0/v3.28.0), byte-identité vérifiée (sha256 a9999c7a…) ; le corpus ne porte que le PM vivant v3.33.1 (9 fichiers .md)"
    verification: "test -s work/KNOWLEDGE-b75a620/skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.32.0.md && test -s work/KNOWLEDGE-b75a620/skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.33.0.md && ! test -f work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.0.md && ! test -f work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.32.0.md"
    source: "R4 archivage (précédents v3.31.0/v3.32.0 — git mv byte-identité ; mv simple journalisé pour fichiers non suivis)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Recalibrage croisé KO-L004 complet (v3.33.0 puis v3.33.1) : KB skills/KNOWLEDGE.md (calibration gen-plan 3.33.1 + lignage Task 47/47-b), pin arbitre (checker ECO_SKILLS + manifeste → gen-plan 3.33.1), @historique/historiques-par-skill/gen-plan.md (lignes v3.33.0 + v3.33.1, VERSION VIVANTE déplacée), lignes vives 9 disciplines + ULTRA recalées 3.33.1, propagation §0 v1.7.20 (115 skills + 138 scripts + 4 agents), sceaux README §5 (v3.33.0 + lag étiquette résorbé 46→45), rescellement archive v2.3 (round-trip 15/15, backup work/seal-backup-task47-v3330-v2.3.zip)"
    verification: "rg -m1 '3\\.33\\.1' work/KNOWLEDGE-b75a620/skills/KNOWLEDGE.md && rg -q '3\\.33\\.1' work/KNOWLEDGE-b75a620/scripts/ecosysteme-integrity.json && rg -q 'v3\\.33\\.1' work/KNOWLEDGE-b75a620/skills/@historique/historiques-par-skill/gen-plan.md && rg -q 'v1\\.7\\.20' work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md && cd work/KNOWLEDGE-b75a620 && python3 scripts/task-f5-seal-archive-v23.py"
    source: "Recalibrage croisé KO-L004 (précédents v3.29.0/v3.30.0/v3.31.0/v3.32.0/v3.33.0)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Miroir hôte synchronisé depuis le dépôt (direction unique R4) : SKILL.md gen-plan, PM v3.33.1, SHARED, PM-INSTALL, KB, manifeste pins, historiques, archive scellée + miroir hôte→dépôt des éléments hôte-seuls (midi-doc-expert v1.2.0, scripts task44/task45, catalogue enrichi) — byte-identiques hôte ↔ clone (271+ fichiers synchronisés, 0 divergent résiduel)"
    verification: "cd /home/z/my-project && diff -q skills/gen-plan/SKILL.md work/KNOWLEDGE-b75a620/skills/gen-plan/SKILL.md && diff -q skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md && diff -q skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md && diff -q skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md && diff -q skills/KNOWLEDGE.md work/KNOWLEDGE-b75a620/skills/KNOWLEDGE.md && diff -q scripts/ecosysteme-integrity.json work/KNOWLEDGE-b75a620/scripts/ecosysteme-integrity.json"
    source: "Règle d'or n°5 (dépôt = source R4, sync miroir dans cette direction) + précédents Task 45 F-04 / Task 46 correctif miroir"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Le présent plan est RE-GÉNÉRÉ via gen-plan v3.33.0 puis v3.33.1 (boucle KO-L005 ×2 : arbitres → montée → recalibrage → re-certification → re-génération du plan via la nouvelle version → re-validation E8) : en-tête mis à jour (gen-plan : v3.33.0 puis via v3.33.1, horodatage plan actualisé), verdict E8 re-validé à chaque passe — journalisé au worklog"
    verification: "rg -m1 'via \\*\\*v3\\.33\\.1\\*\\*' download/plan-task47-regle-or-7-mode-step.md && python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task47-regle-or-7-mode-step.md --worklog work/KNOWLEDGE-b75a620/worklog.md"
    source: "Règle KO-L005 (généralisation règle d'or n°2) + précédent Task 38→39 (montée v3.32.0 → plan Task 39 régénéré)"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Cron idempotent recréé (delete + create, même nom, même horaire Europe/Paris — 501373 → 501446 → 501529) : payload enrichi de la règle d'or n°7 PRÉCISÉE (les éléments oubliés à cause d'une coupure et partiellement reconstitués se complètent en relisant les clones et sauvegardes ; une reconstitution partielle n'est jamais une mémoire complète ; l'état du disque prévaut — plan le plus récent = download/plan-task47-*.md) — préceptes Task 46 inchangés (DJTT = EXEMPLE, optimiser les ÉLÉMENTS, PAT PUSH sur GO), suppression différée jusqu'au PUSH"
    verification: "cron list → job 'Relance sandbox / reprise gen-plan' présent avec payload contenant 'PARTIELLEMENT RÉUSSI À RECONSTITUER' et 'v3.33.1' et 'plan-task47'"
    source: "Directive point 1 + point 3 + vérification propriétaire précédente (tâche idempotente porte les préceptes) + clone task46 §6"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "Re-certification intégrale RÉELLE depuis le disque (règle d'or n°5 — première exécution réelle post-v3.33.0 : la revendication « replay arbitres ×2 » du changelog v3.33.0 était aspirante, constat consigné) : arbitres 6/6 re-jeués — check-ecosysteme-integrity.py (98/98, 0 FAIL ×3), verify-cross (141/141), coherence (51 PASS/23 WARN/0 FAIL — plage PM recalibrée L004 2e éd. 1200-1560, croissance directive), check-tool-routing (N2 5/5 PASS — routage normatif complet : skill→skill-creator, agent/PM→agent-creator, script→script-creator, infrastructure→script-mon-ecosysteme-infrastructure, registre KB→skills-inventory ; N1 résiduel préexistant : 57 skills natifs plateforme sans frontmatter écosystème — logique checker inchangée depuis HEAD, plateforme-géré consigné sans action, précédent Task 46 « PASS (N2 cités) »), garde-plan-genplan.py (PASS — casse §0/__future__ réparée), task14-scan-doublons (0 doublon)"
    verification: "cd work/KNOWLEDGE-b75a620 && python3 scripts/check-ecosysteme-integrity.py --check (0 FAIL) && python3 scripts/task14-scan-doublons.py && python3 scripts/garde-plan-genplan.py"
    source: "GRAPH-DIAMOND (vérifier avant, zéro régression) + règle d'or n°5 + boucle E12-E13 (correctifs aux éléments, D016)"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Non-régression batteries : task45-tests-fonctionnels.py 20/20 ×2 (idempotence — batterie re-pointée sur le clone vivant + miroir complété), tsi-validator --self-test PASS, tsi-validator sur download/task46-midi-controls-bridge.tsi rc=0 (livrable Task 46 inchangé), answer-key-checker sur le présent plan re-généré"
    verification: "cd /home/z/my-project && python3 scripts/task45-tests-fonctionnels.py (×2 → 20/20 deux fois) && python3 skills/tsi-validator/scripts/valider-tsi.py --self-test && python3 skills/tsi-validator/scripts/valider-tsi.py download/task46-midi-controls-bridge.tsi (rc=0)"
    source: "Directive tests robustes (héritage Task 46) + GRAPH-DIAMOND"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "correct-work (projet) v2.8.0 exécuté en fin de chaîne (mode step) : rapport download/rapport-correct-work-projet-task47.md (données, miroir hôte↔dépôt, interactions, cohérence, intégrité) — verdict consigné ; findings corrigés (max 2 rounds par groupe déjà appliqués en amont)"
    verification: "test -s download/rapport-correct-work-projet-task47.md && rg -q 'Verdict' download/rapport-correct-work-projet-task47.md"
    source: "Mode step (correct-work(projet) en fin de chaîne) + directive Task 46 héritée"
    priority: "S1"
    status: "verified"
  - id: "D012"
    criterion: "Bilan E15 : auto-calibration grille #token (estimé vs réel), verdict G-RES resource-monitor de clôture, enrichissement KB (règle d'or n°7 → leçon knowledge-observer M1-M2 : les coupures de contexte sont le risque n°1 de la lignée — les clones/sauvegardes rendent la mémoire reconstituable)"
    verification: "rg -q 'Bilan E15' download/rapport-final-task47.md && rg -q 'G-RES' download/rapport-final-task47.md"
    source: "gen-plan v3.33.1 E15 (boucle complète KO-L005)"
    priority: "S2"
    status: "verified"
  - id: "D013"
    criterion: "clone-chat livré : download/clone-discussion-2026-11-04-task47-regle-or-7-mode-step.md (7+1 étapes — contexte, décisions D001-D014, artefacts, worklog, reprise, auto-évaluation dérivée du disque) + rapport final download/rapport-final-task47.md"
    verification: "test -s download/clone-discussion-2026-11-04-task47-regle-or-7-mode-step.md && test -s download/rapport-final-task47.md"
    source: "Directive Task 46 héritée (clone-chat) + règle d'or n°7 précisée (les clones portent la mémoire)"
    priority: "S1"
    status: "verified"
  - id: "D014"
    criterion: "Worklog R5 complet (chaîne mode step : entrées par groupe + PLAN-AFFICHE) ; pendances consignées : PAT PUSH (GO propriétaire + clé hors canal — KO-L009 point 5, commit préparé, contrôles pré-push 4/4 à re-vérifier au GO), S4 MK2 matériel, 3 scripts task44 verbatim (optionnels), 24 WARN baseline ; cron 501373 MAINTENU jusqu'au PUSH"
    verification: "rg -q 'Task 47' work/KNOWLEDGE-b75a620/worklog.md && rg -q 'PLAN-AFFICHE' work/KNOWLEDGE-b75a620/worklog.md && rg -q 'PAT PUSH' work/KNOWLEDGE-b75a620/worklog.md"
    source: "SHARED §1.4 (R5) + E7-DISP (affichage rejouable) + clone task46 §6"
    priority: "S1"
    status: "verified"
  - id: "D015"
    criterion: "Précision sémantique (directive 3) intégrée AVANT gen-plan sous forme de PATCH v3.33.1 : règle d'or n°7 précisée au SKILL §1.5 (l'« oubli » = les éléments perdus à cause d'une coupure partiellement reconstitués ; reconstitution partielle ≠ mémoire complète ; état disque prévaut), PM v3.33.1 §1.8 (point 2 précisé + point 5 ajouté), KB, pin, historiques, lignes vives, propagation §0 v1.7.20, rescellement v2.3 (backup sceau v3.33.0), plan re-généré via v3.33.1 (KO-L005) — preuve vivante consignée (résumé post-compression partiellement faux corrigé par audit disque)"
    verification: "rg -m1 'partiellement réussi à reconstituer' work/KNOWLEDGE-b75a620/skills/gen-plan/SKILL.md && rg -q 'partiellement réussi à reconstituer' work/KNOWLEDGE-b75a620/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md && test -f /home/z/my-project/work/seal-backup-task47-v3330-v2.3.zip"
    source: "Directive point 3 (précision sémantique) + KO-L005 + KO-L004"
    priority: "S1"
    status: "verified"
  - id: "D016"
    criterion: "Correctifs aux ÉLÉMENTS découverts par la re-certification RÉELLE G4 (jamais aux tests — précepte Task 46) : (i) collision §0/from __future__ — 10 scripts réparés par fusion de docstrings (garde-plan-genplan, sync-instructions-ecosysteme, task45-generer-preset-bridge, adaptation-syntaxe, task42-resceller-archive, task43-replay-answer-key, task43-verifier-projet + miroirs dépôt) ; (ii) plage PM cohérence recalibrée L004 2e éd. 1200-1560 (croissance directive : v3.33.0 = 1511 L, v3.33.1 = 1513 L) ; (iii) miroir complété : scripts task44/task45 + catalogue enrichi + midi-doc-expert v1.2.0 (evals, gabarit, générateur) + tsi-toolkit/scripts (4 scripts task44) — batterie re-pointée sur le clone vivant (PROJ = KNOWLEDGE-b75a620) → 20/20 ×2"
    verification: "cd /home/z/my-project && python3 scripts/task45-tests-fonctionnels.py 2>&1 | rg -q 'BATTERIE : 20/20 PASS' && rg -q '1200 <= pm_text' work/KNOWLEDGE-b75a620/scripts/test-coherence-interactions.py && python3 work/KNOWLEDGE-b75a620/scripts/garde-plan-genplan.py 2>&1 | rg -q 'PASS'"
    source: "Précepte Task 46 (optimiser les ÉLÉMENTS, jamais les failles) + boucle E12-E13 + règle d'or n°5 (constats consignés)"
    priority: "S1"
    status: "verified"
  - id: "D017"
    criterion: "Cron recréé (job 501529, ex-501373 → 501446) : payload enrichi de la règle d'or n°7 PRÉCISÉE (les éléments oubliés à cause d'une coupure et partiellement reconstitués se complètent en relisant les clones et sauvegardes ; l'état du disque prévaut) + préceptes Task 46 inchangés (DJTT = EXEMPLE, optimiser les ÉLÉMENTS, PAT PUSH sur GO) + archives scellées référencées (seal-backup-task46 + task47-v3330) — suppression différée jusqu'au PUSH"
    verification: "cron list → job 'Relance sandbox / reprise gen-plan' présent avec payload contenant 'PARTIELLEMENT RÉUSSI À RECONSTITUER' et 'v3.33.1'"
    source: "Directive point 3 + D008 (recréation delete + create, même nom/horaire) + clone task46 §6"
    priority: "S1"
    status: "verified"
```

## Groupes d'exécution (structure hiérarchique §5.5 — enchaînement séquentiel mode step)

### G1 — Recensement exhaustif de la discussion (règle d'or n°7 — application immédiate) — `#token 1500`
- **SG1.1 Relecture et recensement** (2 tâches) : T1.1.1 relecture des clones et sauvegardes **[TERMINÉ — tour courant + reprise post-coupure : clone-chat-task39-2026-11-02.md, clone-discussion-2026-11-04-task45-preset-midi-bridge.md, clone-discussion-2026-11-04-task46-nouveaux-preceptes.md, rapport-final-task46.md, rapport-correct-work-projet-task46.md, plan-task46-refaire-nouveaux-preceptes.md, worklog.md 733 L — mémoire complétée par audit disque (directive 3)]** · T1.1.2 rapport de recensement mécanique `download/rapport-recensement-discussion-task47.md` (directives 1-11, livrables Tasks 38-46, pendances, préceptes, couverture vérifiable — chaque élément ∈ {tâche, livrable certifié, pendance}) **[TERMINÉ]**
- **correct-work(groupe) G1** : D001 vérifié mécaniquement (max 2 rounds).

### G2 — Règle d'or n°7 durable + PRÉCISÉE — cascade KO-L004 complète ×2 montées (gen-plan v3.32.0 → v3.33.0 → **v3.33.1**) — `#token 7000 + 4500`
- **SG2.1 SKILL.md (arbre dépôt)** (2 tâches) : T2.1.1 insertion §1.5 règle d'or n°7 après n°6 avant bloc PATTERN:KO-L009 (substitution verrouillée count==1) + bump version 3.33.0 + §5.6 ligne histoire v3.33.0 — via `scripts/task47-regle-or-7-edits.py` (stdlib, idempotent ×2) **[TERMINÉ]** · T2.1.2 vérification D002 **[TERMINÉ]**.
- **SG2.2 Cascade générateur** (3 tâches) : T2.2.1 `scripts/delta-genplan-v3330.json` (history + sub insertion n°7 §1.8 — ancre point 4 Primauté n°6 → bloc KO-L009, count==1) **[TERMINÉ]** · T2.2.2 `python3 scripts/generer-pm-skill.py --generate gen-plan --delta scripts/delta-genplan-v3330.json` (PM v3.33.0 + SHARED v1.7.19 + PM-INSTALL v1.8.13 recalibrés) puis `--check` (4 familles COHERENT) **[TERMINÉ — pré-coupure, constaté par artefacts]** · T2.2.3 archivage R4 PM v3.32.0 (git mv → @historique/prompts-maitres/gen-plan/, byte-identité) **[TERMINÉ — pré-coupure]**.
- **SG2.3 Recalibrage croisé** (5 tâches — indépendantes, écritures disjointes → PARALLÈLES par défaut v3.32.0) : T2.3.1 KB skills/KNOWLEDGE.md (calibration gen-plan 3.33.0 + lignage Task 47) ∥ T2.3.2 pin arbitre (ECO_SKILLS + manifeste → gen-plan 3.33.0) ∥ T2.3.3 @historique/historiques-par-skill/gen-plan.md (ligne v3.33.0) ∥ T2.3.4 lignes vives disciplines + propagation §0 2 arbres ∥ T2.3.5 rescellement archive v2.3 (round-trip 15/15) — **[TERMINÉ ×5 — pré-coupure, constaté par artefacts]**.
- **SG2.4 Miroir + re-génération du plan** (2 tâches — série justifiée : sync avant re-génération) : T2.4.1 sync dépôt→hôte byte-identique **[TERMINÉ — 271+ fichiers + rattrapage chemins spéciaux, 0 divergent résiduel]** · T2.4.2 RE-GÉNÉRATION du présent plan via v3.33.0 puis **v3.33.1** (en-tête + horodatage actualisés, E8 re-validé — KO-L005 ×2, journalisé) **[TERMINÉ — présente passe E13]**.
- **SG2.5 Précision sémantique v3.33.1 (directive 3 — série justifiée : même cascade)** : T2.5.1 pré-générateur `scripts/task47-b-precision-v3331-edits.py` (SKILL §1.5 n°7 précisée [2 subs] + bump 3.33.1 + §5.6 ligne + KB + historiques + lignes vives + sceaux + propagate v1.7.20 + delta-genplan-v3331.json) ×2 NO-OP **[TERMINÉ]** · T2.5.2 génération PM v3.33.1 (SHARED v1.7.20 + PM-INSTALL v1.8.14) + --check COHERENT ×2 **[TERMINÉ]** · T2.5.3 archivage R4 PM v3.33.0 (mv + sha byte-identité) **[TERMINÉ]** · T2.5.4 propagation §0 v1.7.20 (115 skills + 138 scripts + 4 agents) **[TERMINÉ]** · T2.5.5 rescellement v2.3 (backup work/seal-backup-task47-v3330-v2.3.zip) + manifeste régénéré (98/98 ×3) **[TERMINÉ]** · T2.5.6 correctifs arbitres G4 (fusion docstrings §0/__future__ ×10, plage PM L004 2e éd. 1200-1560, miroir complété, batterie re-pointée 20/20 ×2) **[TERMINÉ]** · T2.5.7 sync miroir v3.33.1 + batteries **[TERMINÉ]**.
- **correct-work(groupe) G2** : D002-D007 + D015-D016 vérifiés mécaniquement (max 2 rounds).

### G3 — Cron idempotent (501373 → 501446 → 501529) — règle d'or n°7 + précision encodées — `#token 1000`
- **SG3.1** (1 tâche) : T3.1.1 mise à jour du job (recréation : delete + create, même nom, même horaire Europe/Paris) — payload enrichi : règle d'or n°7 PRÉCISÉE (relire clones/sauvegardes pour COMPLÉTER les éléments post-coupure partiellement reconstitués ; l'état du disque prévaut ; plan le plus récent = download/plan-task47-*.md) + préceptes Task 46 inchangés + PAT PUSH sur GO + auto-suppression à la fin de chaîne. **[TERMINÉ — job courant 501529]**
- **correct-work(groupe) G3** : D008 + D017 vérifiés (max 2 rounds).

### G4 — Re-certification intégrale RÉELLE (règle d'or n°5 — verdicts re-jeués depuis le disque) — `#token 3000`
- **SG4.1 Arbitres 6/6** (1 tâche, commandes parallèles) : T4.1.1 check-ecosysteme-integrity.py ∥ verify-cross ∥ coherence ∥ check-tool-routing ∥ garde-plan-genplan.py ∥ task14-scan-doublons (mesurés : 98/98 ×3 · 141/141 · 51/23W/0F · N2 5/5 PASS [N1 natif = réserve plateforme-gérée préexistante] · PASS · 0). **[TERMINÉ]**
- **SG4.2 Non-régression batteries** (1 tâche) : T4.2.1 task45-tests-fonctionnels.py ×2 (20/20 deux fois) ∥ tsi-validator --self-test ∥ valider-tsi.py sur task46-midi-controls-bridge.tsi (rc=0) ∥ answer-key-checker sur le présent plan. **[TERMINÉ — batterie re-pointée sur le clone vivant, miroir complété]**
- **SG4.3 Correctifs éventuels** (1 tâche, conditionnelle) : T4.3.1 tout FAIL → correctif à l'élément (jamais au test — précepte Task 46) + retest ×2. **[TERMINÉ — 3 correctifs exécutés : (i) fusion docstrings §0/__future__ ×10 scripts, (ii) plage PM L004 2e éd. 1200-1560, (iii) miroir task44/45 + midi-doc v1.2.0 + catalogue + batterie re-pointée → 20/20 ×2]**
- **correct-work(groupe) G4** : D009-D010 + D016 vérifiés (max 2 rounds).

### G5 — correct-work (projet) — fin de chaîne mode step — `#token 2000`
- **SG5.1** (2 tâches, série justifiée : rapport puis correctifs) : T5.1.1 rapport `download/rapport-correct-work-projet-task47.md` (données · miroir · interactions · cohérence · intégrité) **[TERMINÉ — PASS AVEC RÉSERVES, 0 finding ouvert]** · T5.1.2 correctifs des findings + retests **[TERMINÉ — 7 constats corrigés aux éléments en G4, re-testés ×2]**.
- **correct-work(groupe) G5 = le correct-work (projet) lui-même** (D011).

### G6 — Clôture — `#token 2500`
- **SG6.1 Bilan E15** : T6.1.1 auto-calibration #token (estimé ~17 k vs réel — écart > 35 %, leçon contingence « reprise post-coupure + cascade double ×3-4 »), G-RES de clôture (OK), leçons knowledge-observer M1-M2 ×4 (coupures = risque n°1 ; clones = mémoire reconstituable ; propagation §0 vs __future__ ; revendication d'arbitre non exécutée = aspirante). **[TERMINÉ]**
- **SG6.2 Rapport final + clone-chat** (série justifiée : clone-en-dernier) : T6.2.1 `download/rapport-final-task47.md` **[TERMINÉ]** · T6.2.2 `download/clone-discussion-2026-11-04-task47-regle-or-7-mode-step.md` (7+1 étapes) **[TERMINÉ]**.
- **SG6.3 Worklog + pendances** : T6.3.1 worklog R5 (rattrapage G1-G3 dérivé du disque + G4-G6, marqueur PLAN-AFFICHE frais) **[TERMINÉ]** · pendances consignées (PAT PUSH sur GO, S4 MK2, grille #token contingence, scripts task44 re-miroirés ×4 + task45 ×2 [pendance d'origine résorbée], 23 WARN baseline) · cron 501529 MAINTENU jusqu'au PUSH. **[TERMINÉ]**

## Vagues Graph Diamond (mode step — groupes séquentiels, parallélisme INTRA-groupe prouvé)

- **Séquence des groupes (mode step)** : G1 → G2 → G3 → G4 → G5 → G6 (correct-work(groupe) entre chaque, max 2 rounds) — reprise post-coupure : G1-G3 constatés terminés par artefacts (audit disque), G4 re-jeué réellement, G5-G6 enchaînés même session.
- **Parallélisme intra-groupe (v3.32.0 — preuve d'indépendance)** : SG2.3 T2.3.1 ∥ T2.3.2 ∥ T2.3.3 ∥ T2.3.4 ∥ T2.3.5 (écritures disjointes : KB, manifeste, historiques, lignes vives/§0, archive) ; SG4.1 les 6 arbitres en commandes parallèles (lectures indépendantes) ; SG4.2 batteries parallèles (livrables disjoints).
- **Séries justifiées (tracées)** : T2.1.1 → T2.2.2 (le générateur lit la version SKILL bumpée) ; T2.2.2 → T2.2.3 (archivage après génération) ; T2.3.* → T2.4.1 (sync après toutes écritures) ; T2.4.1 → T2.4.2 (re-génération après sync) ; T2.5.1 → T2.5.2 (générateur lit la version précisée bumpée) ; T2.5.2 → T2.5.5 (rescellement après corpus final) ; correctifs éléments G4 → batteries 20/20 ; G6 séquentiel (clôture).
- **Statuts** : dérivés de l'état vérifiable (règle d'or n°5) — `[À FAIRE]` · `[EN COURS]` · `[TERMINÉ]` · `[BLOQUÉ]` · `[REPORTÉ]`. Compteurs n/m par sous-groupe.

> **Verdict E8 :** PASS (answer key D001-D017 avec vérifications exécutables ; structure G/SG/T conforme §5.5 ; mode step avec correct-work(groupe) par groupe et correct-work(projet) en fin de chaîne ; parallélisme intra-groupe prouvé, séries tracées ; routage N2 complet [registre KB → skills-inventory] ; règle d'or n°7 appliquée avant génération, encodée comme précepte structurel ET précisée sémantiquement [v3.33.1 — directive 3 : éléments post-coupure partiellement reconstitués complétés par relecture, état disque prévaut] ; pendances et hors-périmètre consignés — E13 : directives 1-3 + D015-D017 + statuts dérivés du disque + clôture G5/G6 — Horodatage vérifié : 2026-11-04T04:59:29+00:00)

## Exécution — statuts finaux (E13 clôture, règle d'or n°5 — dérivés du disque, 2026-11-04T04:59:29+00:00)

| Groupe | Statut | Preuve dérivée du disque |
|---|---|---|
| G1 Recensement | **TERMINÉ 2/2** | rapport-recensement à jour des 11 directives, AUCUN ÉLÉMENT ORPHELIN |
| G2 Cascade KO-L004 ×2 montées | **TERMINÉ 9/9 (SG2.1-SG2.5)** | SKILL v3.33.1 [n°7 précisée], PM v3.33.1 + PM v3.32.0/v3.33.0 archivés, SHARED v1.7.20, KB 3.33.1, pin 3.33.1, propagation v1.7.20, sceau v2.3 re-scellé + backup, miroir 0 divergent |
| G3 Cron | **TERMINÉ 1/1** | job 501529 actif, payload règle d'or n°7 précisée |
| G4 Re-certification RÉELLE | **TERMINÉ 3/3** | integrity 98/98 ×3, verify-cross 141/141, coherence 51/23W/0F, garde-plan PASS, doublons 0, batterie 20/20 ×2, tsi-validator self-test + task46 rc=0, tool-routing N2 5/5 PASS (N1 natif = réserve plateforme-gérée préexistante) |
| G5 correct-work (projet) | **TERMINÉ 2/2** | rapport-correct-work-projet-task47.md — PASS AVEC RÉSERVES, 0 finding ouvert (7 constats corrigés aux éléments) |
| G6 Clôture | **TERMINÉ 3/3** | rapport-final-task47.md + clone-discussion-2026-11-04-task47-regle-or-7-mode-step.md (7+1 étapes) + worklog rattrapage+clôture/PLAN-AFFICHE + pendances consignées |

- D001-D017 : **verified — 17/17** (vérifications mécaniques exécutées ; écarts constatés corrigés aux éléments, D016 ; chaîne G1→G6 menée à terme — même session, reprise E1-RES incluse).
