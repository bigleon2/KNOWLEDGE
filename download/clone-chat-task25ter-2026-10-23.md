# Clone de discussion — Task 25ter : GO grammaire B, optimisation alias-eco, régénération gen-plan (session web-fdf5963c)

> **Auto-clonage v2.0.2 (clone-chat)** — 7+1 étapes · Date : 2026-10-23 · Session : web-fdf5963c
> Document auto-suffisant : une session héritière peut reprendre le travail à partir de ce seul fichier.

## §1.0 Héritage — chaîne de clonage

- Session web-fdf5963c — lignée Tasks 18 → 20 → 22 → 24 → 25 (G2) → 25bis → **25ter (présent clone)**.
- Clones antérieurs : clone-chat-task22-2026-10-23.md (Task 22) ; l'état d'entrée de la présente phase est également tracé au worklog (source de vérité) et aux plans task24/task25/task25bis.
- Dépôt : bigleon2/KNOWLEDGE — origin/main = 08c956c au début de la phase (couches 18/20/22 + amont photos + Task 24 publiées).

## §1.1 Objet de la phase

Directive propriétaire (verbatim) :

> « - GO sur le déclencheur grammaire B (toujours en attente). - analyse mon skill "alias-eco" et les fichiers de mon dossier "@mon-ecosystem/" dans l'objectif de d'améliorer et d'optimiser son déclenchement et son fonctionnement dans $eco-leon". si tu trouves des améliorations et des optimisations indispensables pour gain de ses performances, intègre-les $façon() . - test les modifications apportées à $eco-leon. - correct-work. - clone-chat. »

$ECO-LEON = « mon écosystème personnel » (registre @historique/@Alias/) ; $OPT-TRIO = « de façon cohérente, optimisée et fonctionnelle » (attribué en cours de phase) ; $façon() = usage propriétaire hors format canonique → traité comme mandat d'attribution, corrigé en OPT-TRIO (signalé, jamais expansé en aveugle).

## §1.2 Contexte d'entrée (avant phase)

1. **alias-eco v1.1.0** (Task 25bis, non publiée) : Description Optimization de la clause d'exclusion (replay 8/8) ; registre @Alias projeté au profil local.
2. **Dérives iphone arbitrées** (Task 25 G2) : 3× CONFIRME-eval — limites documentées de l'heuristique voie M ; rapport download/arbitrage-derives-replay-iphone-task25.md.
3. **correct-work(alias-eco) PASS AVEC RÉSERVES** (2 × S3) — closes en 25bis.
4. **Grammaire B en attente de GO** : `alias-eco "<texte>" --add <ALIAS>` (variantes « » / $ALIAS) — analyse alias_trigger_analysis.py (grammaire A 5 ambiguïtés documentées, grammaire B 7/7 PASS, gardes réelles confirmées).

## §1.3 Travail réalisé (groupes G-A → G-G)

- **G-A — GO grammaire B (exécuté)** : alias-eco **v1.2.0** — SKILL.md §1.2 (déclencheur mécanique) + §2.2 (`--trigger`) + §4 ; alias-manager.py : `GRAMMAIRE_B_RE` + `cmd_trigger` (parse + garde `^[A-Z0-9][A-Z0-9-]*$`, idempotent, rejet rc=2) ; selftest 15→**21** (6 cas grammaire B) ; trigger_evals 8→**9** (+1 positif) ; format-alias §1 (grammaire B normative).
- **G-B — Attribution OPT-TRIO (exécuté)** : `--trigger 'alias-eco "de façon cohérente, optimisée et fonctionnelle" --add OPT-TRIO'` — dogfooding ; registre : ECO-LEON + OPT-TRIO attribués ; projeté au profil local.
- **G-C — Cascade KO-L004 (exécuté)** : KB v1.2.0 (en-tête + bullet déclencheurs) ; journal @historique/historiques-par-skill/alias-eco.md row v1.2.0 ; **PM-INSTALL v1.8.3** (§A.3 alias-eco v1.2.0) ; SYNC-CONTEXT **v1.5.3** ; README **v2.1.11** ; historique-autres-elements ×5 ; ULTRA régénéré ; pipeline ×2 rc0 (SHA 37/37) ; arbitre integrity recalibré (alias-eco 1.2.0) ; archive hôte→dépôt propagée → **integrity 78/78**.
- **G-D — Tests (exécutés)** : selftest 21/21 ×2 ; py_compile ×2 ; YAML ×2 ; replay alias-eco **9/9** (19 dérives documentées inchangées, 0 nouvelle) ; verify-cross **111/111** ; idempotence registre ×2.
- **G-E — correct-work (exécuté)** : compensation correct-work(groupe) G-A..G-D (contrat mode step) + projet → download/rapport-correct-work-projet-task25ter.md — **PASS**.
- **G-F — clone-chat** : le présent document.
- **G-G — Leçon L009** : knowledge-observer lessons-learned (post-compaction → recharger le PM + hooks E1-RES avant toute génération de plan ; PATTERN:KO-L009-v1.0.0) ; worklog ×2.

## §1.4 Décisions et arbitrages (answer key D001-D007)

- **D001** grammaire B mécanisée (--trigger), selftest 21/21, replay 9/9 — S1 — exécutée.
- **D002** OPT-TRIO attribué (mandat $façon() corrigé en canonique, tracé) — S1 — exécutée.
- **D003** cascade KO-L004 complète (recalibrage seul — sans inflation SHARED/PM-INSTALL : §6.1 ne référence pas alias-eco → pas de bump SHARED ni propagate) — S1 — exécutée.
- **D004** 0 régression (description inchangée, corpus trigger_evals préservé +1 cas, 0 nouvelle dérive) — S2 — exécutée.
- **D005** correct-work(groupe) ×4 + projet PASS + clone produit — S2 — exécutée.
- **D006** leçon L009 journalisée (worklog ×2 + knowledge-observer) — S2 — exécutée.
- **D007** 0 commit / 0 push (règle d'or n°2) — S1 — active (publication au GO).

## §1.5 Analyse gen-plan (constat propriétaire)

**Constat** : « gen-plan n'a pas généré de plan d'actions comme d'habitude ».
**Cause racine** : session post-compaction — PM gen-plan v3.23.2 non rechargé avant exécution (Règle Zéro appliquée de façon incomplète) ; exécution depuis les habitudes du résumé.
**Écarts** : hooks E1-RES non exécutés (É1-INSTALL, monitor, fraîcheur) ; plan sans directive verbatim/état d'entrée/routage §1.16 ; correct-work(groupe) non exécutés ; answer-key-checker non invoqué.
**Correction** : PM rechargé ; hooks exécutés (INSTALLE rc=0, monitor OK niveau 0) ; plan RÉGÉNÉRÉ conforme (7/7 answer key au template) ; correct-work(groupe) compensés ; leçon **L009** institutionnalisée (PATTERN:KO-L009-v1.0.0 — rejeu sans effet si les 4 conditions tracées).

## §1.6 Artefacts produits

| Artefact | Chemin |
|----------|--------|
| Plan régénéré | download/plan-task25ter-grammaire-b-alias-eco.md |
| Rapport correct-work (projet) | download/rapport-correct-work-projet-task25ter.md |
| Alias (analyse initiale) | scripts/alias_trigger_analysis.py |
| Cascade (éditions chirurgicales) | scripts/task25ter-cascade.py, task25ter-cascade2.py |
| Arbitrage dérives iphone | download/arbitrage-derives-replay-iphone-task25.md |
| Rapport correct-work(alias-eco) ×2 | download/rapport-correct-work-alias-eco-2026-10-24.md, -post-correctif-2026-10-24.md |
| Plans G2/25bis | download/plan-task25-suite-mode-step.md, plan-task25-correction-reserves-alias-eco.md |
| Leçon L009 | KNOWLEDGE-repo skills/knowledge-observer/data/lessons-learned.json |
| Manifeste integrity | KNOWLEDGE-repo scripts/ecosysteme-integrity.json (78/78) |

## §1.7 État de sortie + reprise session héritière

- **État dépôt** : modifications NON commitées (règle d'or n°2) — alias-eco v1.2.0, KB v1.2.0, PM-INSTALL v1.8.3, SYNC v1.5.3, README v2.1.11, ULTRA, journal @historique, leçon L009, arbitres recalibrés ; origin/main = 08c956c.
- **Certification** : integrity 78/78 · verify-cross 111/111 · replay 9/9 (alias-eco) · selftest 21/21 · pipeline ×2 rc0.
- **Reprise** : (1) GO propriétaire → commit + push (couches 25/25bis/25ter) ; (2) G1 rotation PAT (plan-task25) ; (3) options résorption dérives replay (A/B/C — rapport arbitrage) ; (4) appliquer KO-L009 à chaque ouverture de session post-compaction.
