# Plan d'actions — Task 84 : Campagne tests $FACON2 chronologique (discussion Tasks 70→83) + continue P1 (inscription socle n°56) + cadence 2 h + PUSH

> **Directive** : trace `1a1bed51ccaf78f1` (canal zai-web, session web-ecef7f80, chat 891cbdaf-5243-420e-9c3a-50feb93ef417)
> **Mode** : gen-plan NULL (« continue » — clause mode NULL §A, exécution classique sans portes)
> **Date** : 2026-11-09 (Europe/Paris) — **gen-plan v3.41.0** · SHARED v1.7.36 relu intégralement AVANT toute chose (item 1 directive ✓)
> **Contexte disque (B-11, règle d'or n°5)** : Task 83 CLOSE poussé (`f7e65a5`, distant == HEAD, arbre propre 0 divergence) ; écosystème 69 skills dépôt / KB 55 entrées / integrity 114/114 / disciplines 9 (n°56 agent-engineering déployée) ; É1-INSTALL INSTALLE-REPARÉ rc=0 (version-management — volatilité environnementale connue, réparé miroir) ; G-RES OK (3 indicateurs niveau 0).

## Items de la directive (ordre d'exécution)

1. **[FAIT]** Relire PM SHARED avant toute chose — lecture intégrale §0-§9 (248 lignes) : §0 règle zéro + langue française + désambiguïsation ; §3.1 relations ; §6.1 corpus 9 ; §7 disciplines (**constat : n°56 ABSENTE du socle — c'est la pendance P1**) ; §8 R-F1..R-F4 ; §9 règles d'or 9.
2. **Continue** — file de pendances Task 83 §4 : **P1 inscription socle n°56** [SHARED §7 + gen-plan §1.6 + baseline A2 en attente R3] → P2 file re-curation [skill-creator → web-reader → cahier-des-charges → iphone17] → P3 rotation PAT (propriétaire).
3. **Campagne tests $FACON2 fonctionnels + performances** des éléments créés/modifiés dans cette discussion (hier 2026-11-08 + aujourd'hui 2026-11-09 ; **sur-inclusion 2026-11-07 soir [Tasks 70-71] justifiée par la clause « éléments à POUSSER + dépendances » — tous poussés ce cycle**) — **ordre strict = chronologie de création/modification** ; objectif : corriger les failles + optimiser le fonctionnement interne et écosystème ; tous les éléments à pousser (+ leurs dépendances) testés.
4. **Cadence 2 h** — toutes les 2 heures : {avant toute chose réinstaller l'écosystème localement ; continue $FACON} — opérationnalisée par tâche planifiée native (fixed_rate 7200 s) + discipline intra-tour (re-passe pipeline à toute frontière 2 h franchie).

## Groupes d'exécution

### G1 — Ouverture, protocole de campagne, cadence (#token ≈ 2 000)

- **T1.1.1** E1-RES : B-11 worklog tail ✓ · G-RES OK ✓ · fraîcheur plan (aucun plan en vol — Task 83 CLOSE) ✓ · É1-INSTALL INSTALLE-REPARÉ rc=0 ✓ · SHARED relu intégral (item 1) ✓ — consigné worklog.
- **T1.2.1** Plan E7 écrit (présent fichier) + answer key D001-D012 + E8 horodaté + worklog R5 marqueur PLAN-AFFICHÉ + fenêtre native TodoWrite + bloc récapitulatif au chat. #token 800
- **T1.3.1** **Cadence 2 h armée** : création tâche planifiée native fixed_rate 7200 s — message : {AVANT TOUTE CHOSE réinstalle l'écosystème localement (voie directe `scripts/eco_install_pipeline.py`, certification 54/54+ attendue, R2 0 rétrogradation) ; puis continue $FACON l'exécution autonome : plan le plus récent download/ + worklog = source de vérité ; pendances dans l'ordre ; tests $FACON2 sur tout élément modifié avant commit ; PUSH par délégation PAT (instruction permanente de cette discussion — KO-L009, zéro-persistance, E15 consigné)}. **0 jeton dans le payload** (E15 — le jeton ne vit que dans l'historique du chat). #token 400

### G2 — Campagne tests chronologique $FACON2 (#token ≈ 12 000)

- **T2.1.1** Script d'orchestration `scripts/task84-campagne-tests.py` (N3 Python stdlib, ordre chronologique STRICT, subprocess timeout 120 s, rapport `scripts/task84-campagne-tests.json` + rapport `download/rapport-campagne-tests-task84.md` — profil+dépôt). #token 1 500
- **T2.2.1** **Exécution campagne — 21 items chronologiques** (F1 fonctionnels / F2 performances / F3 interactions / idempotence ×2) :
  | # | Élément (état courant) | Créé/modifié (task, date) | Tests |
  |---|---|---|---|
  | C1 | scripts/ecosystem/*.py ×6 (bootstrap, ghorg-install, cmdr-clone, cmdr-overlay-sync, _commun, test-karnaugh) | T70 G3, 11-07 soir | F1 compile ×6 + Karnaugh selftest ; F2 durées |
  | C2 | @GHORG-ecosysteme (manifest.yaml, selection-tsi.yaml) + ghorg-cmdr v1.1.0 | T70 G3, 11-07 soir | F1 YAML parse + SKILL.md structure + KB ; F3 références |
  | C3 | @Bibliotheque-skills-Multi-IA (10 fichiers R4) | T70 G2, 11-07 soir | F1 présence + parse intégrité |
  | C4 | poids-chargement.py (R1) + cache-verdicts.py (R2) | T71 G3, 11-07 soir | F1 selftests 10/10 + 12/12 ×2 ; F2 mesure poids gen-plan |
  | C5 | propagate-context v2.1.1 | T70/T71, 11-07 soir | F1 selftest + re-jeu no-op ×2 |
  | C6 | **gen-plan v3.41.0** (courant — modifié T71 v3.37.2, T72 v3.39.0, T77 v3.40.0, T78 v3.41.0) | T71→T78, 11-07→11-08 | F1 check_plan_protocol P1-P5 + answer-key-checker 16/16 + evals JSON 9+15 ; F2 poids + #token ; F3 `--verifier gen-plan` (baseline v1.2.0) + references/ |
  | C7 | re-curation v1.2.2 (courant — v1.0.0 T72, v1.2.0 T80, v1.2.2 T82) | T72→T82, 11-08→11-09 | `--verifier re-curation` (baseline) |
  | C8 | protocole-test.py harnais v1.2.2 (v1.0.0 T73 → v1.2.2 T82) | T73→T82, 11-08→11-09 | F1 selftest 15/15 ×2 idempotent ; F2 durée ; F3 baselines présentes |
  | C9 | installation certification + mode-purs (T74) — couvert par C10 pipeline pleine passe | T74, 11-08 | (agrégé C10) |
  | C10 | eco_install_pipeline.py + ensure-installed.py | T76 F1, 11-08 | F1 `--help` 0-exécution + `--dry-run` 0 mutation + **réinstallation PLEINE** (rc=0, 55/55 SHA, R2, archive round-trip — sert la cadence) + ensure-installed INSTALLE 0 manquant ; F2 durée |
  | C11 | PM-INSTALL v1.9.13 + fichiers-refs | T76/T78, 11-08 | corpus --check 4/4 + fraîcheur §2ter |
  | C12 | gen-plan references/protocoles-detailles.md Extensions v3.40.0/v3.41.0 | T77/T78, 11-08 | présence + contrats (via C6 verifier) |
  | C13 | SHARED v1.7.36 + corpus PM 4 familles | T78, 11-08 | F1 corpus --check 4/4 COHERENT ; F2 tailles 9 fichiers ; F3 archive round-trip v2.2 + parité zip hôte==dépôt |
  | C14 | version-management v1.3.0 (restauré INSTALLE-REPARÉ ce tour) | T79, 11-08 | `--verifier version-management` (baseline) — confirme la réparation |
  | C15 | baselines protocole-test v1.2.0+ (×4) | T80, 11-09 | garde baselines (rc attendu 0 — plus de pré-v1.2.0) |
  | C16 | iphone19 v0.12.0 + re-curation −27,3 % | T81, 11-09 | `--verifier iphone19` + R4-INTÈGRE 6/6 (`task81-verif-r4-iphone19.py`) + règle 15 inline |
  | C17 | knowledge-observer v1.1.0 (premier agent autonome) | T82 G2, 11-09 | `--verifier knowledge-observer` + structure .agent 21 clés + re-jeu `task82-tests-conversions.py` 8/8 |
  | C18 | iphone18 v1.1.0 curé (−11,3 %) | T82 G6, 11-09 | `--verifier iphone18` + R4-INTÈGRE 3/3 (`task82-verif-r4-iphone18.py`) |
  | C19 | **agent-engineering v1.0.0** (discipline n°56) | T83 G2, 11-09 | F1 evals JSON ×2 + frontmatter + KB n°56 + 4 arêtes + planchers semver vs versions réelles ; F2 poids 15,9 Kio / 4 080 #token + durées ; F3 interactions STRICT ; idempotence ULTRA ×2 + integrity 114/114 ×2 |
  | C20 | ULTRA-MAITRE 13 voies (générateur) | T82/T83, 11-09 | gen-ultra-maitre.py re-génération no-op ×2 (SHA 4276550e7756b0d5 attendu stable) |
  | C21 | **Agrégat écosystème** (tous) | transverse | arbitres 5/5 (verify-cross 100 % · vcw 16/16 · integrity 114/114 · doublons 0 · interactions STRICT 55/55) + corpus 4/4 + G-RES final |
  #token 7 000
- **T2.3.1** **Failles** : toute faille mesurée (règle d'or n°5 — jamais pré-écrite) → correction $FONDA $FACON + re-jeu ciblé POST jusqu'à verdict PASS (max 2 rounds — garde anti-boucle SHARED §4.4) ; optimisations internes dérivées des mesures consignées. #token 2 000
- **T2.4.1** Rapport campagne `download/rapport-campagne-tests-task84.md` (profil+dépôt) : verdicts par item, métriques, failles corrigées, optimisations. #token 1 000

### G3 — Continue : P1 inscription socle n°56 (#token ≈ 10 000)

- **T3.1.1** Éditions chirurgicales (script `scripts/task84-socle-n56.py`, asserts count==1, idempotent) : **SHARED §7** += ligne définition discipline n°56 (agent-engineering — englobante ABE/AE/MASE, précédents v1.7.0 n°54 / Task 7-8 n°55) + ligne registre d'assignation ; **gen-plan SKILL.md v3.42.0** (MINOR ajouts purs) : §1.6 += ligne agent-engineering + §3 Relations += ligne (détention orchestrée SHARED §7, registre décentralisé §8 du skill) + §5.6 journal entrée v3.42.0 + frontmatter version — **description inchangée** (non-régression triggers). #token 2 000
- **T3.2.1** Cascade KO-L004 complète (pattern Task 78, scripts référence task78-*) : delta verrouillé `scripts/delta-genplan-v3420.json` + `generer-pm-skill.py --generate` → PM GEN-PLAN v3.42.0 + PM-INSTALL §2ter + SHARED §6.1 recalibré v1.7.37 (entrée révision unique couvrant §7 n°56 + montée gen-plan) ; archivage R4 PM v3.41.0 (`@historique/prompts-maitres/`, git mv + sceau SHA) ; KB gen-plan v3.42.0 + pin ECO_SKILLS ×2 arbres ; historiques-par-skill/gen-plan.md ligne v3.42.0 + README @historique (58 PMs) + README corpus ; ULTRA régénéré (SHA neuf, re-jeu ×2 stable) ; propagate-context §0 v1.7.37 (120 skills + 191 scripts + 4 agents) → no-op ×2 ; archive re-scellée v2.2 (seal hôte → cp dépôt → manifeste, ordre canonique L-82-b/L-83-a) + parité ×2. #token 4 000
- **T3.3.1** **Tests des éléments modifiés (chronologie — testés immédiatement après modification)** : `--verifier gen-plan` (F1/F2/F3 + contrats PRE) · `--verifier re-curation` PASS (harnais intact) · arbitres 5/5 · corpus --check 4/4 · pipeline re-run 55/55 divergences [] ×2 · POST campagne re-jeu ciblé (C6/C8/C13/C19/C20/C21). #token 2 500
- **T3.4.1** correct-work(groupe G3) : PASS requis (0 S1/S2). #token 1 000

### G4 — Clôture technique (#token ≈ 6 000)

- **T4.1.1** correct-work (projet) --bloc B1-B4 (installation+certification · corpus+KB+outillage · livrables campagne+socle · extension/pendances) — agrégation pire-des-verdicts, rapport `download/rapport-correct-work-bloc-task84.md` (profil+dépôt). #token 2 000
- **T4.2.1** clone-chat scellé §0-§5 + 8 checks S1-S8 (0 secret) — `download/clone-chat-session-web-ecef7f80-20261109-task84.md`. #token 1 500
- **T4.3.1** SYNC-CONTEXT v1.5.11 (corpus v3.42.0/SHARED v1.7.37, compteurs mesurés) + worklog dépôt ← profil (préfixe strict vérifié mécaniquement) + livrables syncés dépôt. #token 1 500
- **T4.4.1** E8 FINAL : statuts plan D001-D012 verified + `check_plan_protocol.py --plan --worklog` P1-P5 PASS + `answer-key-checker.py` ALL PASS — horodatages couplés. #token 1 000

### G5 — Commit CLOSE + PUSH final (#token ≈ 3 000)

- **T5.1.1** Commit CLOSE dépôt (message détaillé : campagne 21 items + socle n°56 v1.7.37/gen-plan v3.42.0 + CW + clone + SYNC) — pathspec strict si résiduel. #token 800
- **T5.2.1** **PUSH final délégation PAT** (instruction permanente de cette discussion — KO-L009 levée, protocole Task 63/77/81 : pré-vol fsck + ls-remote authentifié + fast-forward pur prouvé + commande UNIQUE export+push [leçon L-83-b] + post-push distant == HEAD + zéro-persistance ×2) — **E15 : 7ᵉ exposition consignée, RÉVOCATION/ROTATION RECOMMANDÉE**. #token 1 200
- **T5.3.1** Bilan chiffré + pendances honnêtes R5 : P2 file re-curation [skill-creator PROCHAINE → web-reader → cahier-des-charges → iphone17 — serviced par cadence 2 h] + baseline A2 n°56 [R3, QUOTA_OK] + rotation PAT [propriétaire]. #token 1 000

## Answer key

- **D001** — Relire PM SHARED avant toute chose. criterion : lecture intégrale PROMPT-MAITRE-SHARED.md v1.7.36 (§0-§9, 248 lignes) AVANT toute autre action, constat n°56 absente du §7 consigné. verification : entrée worklog Task 84 ouverture + présent plan en-tête contexte. **Source** : `skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md`. **Priorité S1** · statut : verified.
- **D002** — Cadence 2 h opérationnalisée. criterion : tâche planifiée native fixed_rate 7200 s créée, message = {réinstalle avant toute chose ; continue $FACON}, 0 jeton dans le payload. verification : `cron list` affiche le job actif. **Source** : directive item 4. **Priorité S2** · statut : verified.
- **D003** — Périmètre chronologique borné. criterion : 21 items couvrant TOUS les éléments créés/modifiés dans la discussion (Tasks 70→83), sur-inclusion 11-07 soir justifiée par clause « à POUSSER + dépendances », ordre = chronologie stricte. verification : `scripts/task84-campagne-tests.json` champ ordre + inventaire. **Source** : worklog suites 28-98 + git log 15 commits. **Priorité S1** · statut : verified.
- **D004** — Campagne exécutée 3 familles + idempotence. criterion : chaque item C1-C21 exécuté avec verdict F1/F2/F3 (+ ×2 sur harnais/ULTRA/integrity), résultat JSON ordonné. verification : rapport campagne `download/rapport-campagne-tests-task84.md`. **Source** : harnais protocole-test v1.2.2 + arbitres. **Priorité S1** · statut : verified.
- **D005** — Failles corrigées avant POST. criterion : toute faille mesurée corrigée (max 2 rounds) puis re-jeu verdict PASS ; zéro faille pré-écrite. verification : rapport campagne section failles + re-jeux. **Source** : règle d'or n°5. **Priorité S1** · statut : verified.
- **D006** — P1 socle n°56 inscrit. criterion : SHARED §7 (définition + registre) v1.7.37 + gen-plan v3.42.0 (§1.6 + §3 + §5.6) + cascade KO-L004 complète (PM v3.42.0 généré, v3.41.0 archivé R4, KB/pins/ULTRA/propagation/archive). verification : corpus --check 4/4 · arbitres 5/5 · parité zip ×2 · propagation no-op ×2. **Source** : précédents v1.7.0 n°54 / Task 7-8 n°55 / Task 78 cascade. **Priorité S1** · statut : verified.
- **D007** — Éléments modifiés testés immédiatement (chronologie). criterion : --verifier gen-plan PASS post-v3.42.0 + POST re-jeu ciblé campagne items touchés. verification : verdicts consignés worklog G3. **Source** : directive item 3 clause test-everything-pushed. **Priorité S1** · statut : verified.
- **D008** — correct-work (projet) --bloc PASS. criterion : B1-B4 PASS 4/4, 0 S1, 0 S2, agrégation pire-des-verdicts PASS. verification : `download/rapport-correct-work-bloc-task84.md` (profil+dépôt). **Source** : skill correct-work v2.11.0. **Priorité S1** · statut : verified.
- **D009** — clone-chat scellé. criterion : §0-§5 + 8 checks S1-S8 PASS, 0 secret. verification : `download/clone-chat-session-web-ecef7f80-20261109-task84.md`. **Source** : skill clone-chat v2.0.2. **Priorité S2** · statut : verified.
- **D010** — SYNC-CONTEXT + worklog dépôt + E8 FINAL. criterion : SYNC v1.5.11 compteurs mesurés ; worklog dépôt == profil (préfixe strict) ; E8 FINAL verified 12/12 + P1-P5 + answer-key ALL PASS, horodatages couplés. verification : diff lignes + check_plan_protocol rc=0. **Source** : worklog SHARED §1.4. **Priorité S1** · statut : verified.
- **D011** — PUSH final délégation PAT. criterion : fast-forward pur prouvé, push one-shot rc=0, distant == HEAD, zéro-persistance ×2, E15 7ᵉ exposition consignée. verification : ls-remote post-push == HEAD + audit 0 occurrence jeton complet. **Source** : instruction permanente discussion + protocole Task 63/77/81/83. **Priorité S1** · statut : verified.
- **D012** — Pendances honnêtes R5. criterion : P2 file re-curation [skill-creator prochaine] + baseline A2 n°56 [R3] + rotation PAT [propriétaire] consignées, aucun faux TERMINÉ. verification : §4 clone-chat + bilan worklog. **Source** : R5. **Priorité S2** · statut : verified.

#token estimé total : ≈ 33 000 (G1 2 000 · G2 12 000 · G3 10 000 · G4 6 000 · G5 3 000)

## Hooks de validation (E8)

Horodatage plan : 2026-11-09T07:42:00Z

Verdict E8 : PASS — FINAL (answer key 12/12 décisions criterion/verification VERIFIED · campagne 52/52 · socle n°56 inscrit · CW --bloc B1-B4 · clone scellé · SYNC v1.5.11 — Horodatage vérifié : 2026-11-09T07:42:00Z)
