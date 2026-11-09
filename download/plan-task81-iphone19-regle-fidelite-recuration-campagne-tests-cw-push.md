# Plan Task 81 — Règle fidélité iphone19 (v0.12.0) + re-curation progressive disclosure (P1→P7) + campagne de tests chronologique + CW --bloc + clone-chat + PUSH

**Horodatage plan : 2026-11-08T21:25:00Z (INITIAL)** · Mode : gen-plan (step, chaîne autonome — enchaînement des groupes sans portes, correct-work(groupe) après chaque groupe, max 2 rounds) · Session : web-ecef7f80 · Trace directive : 1a1bcf4fecbf5f29 (précisant la trace 1a1bcf27774c5a81 — « mon skill iphone19 »).

## Contexte et périmètre

Directive propriétaire (2026-11-09, trace 1a1bcf4fecbf5f29), verbatim (jeton tronqué) :

> « {- fais en sorte que mon skill "iphone19" intègre la règle suivante : "ne jamais inventer et rester fidèle (visage, vêtement, arrière-plan, etc....) à l'image d'origine si je ne t'ai pas précisé que je voulais que tu fasses des modifications." - effectue $FACON la re-curation divulgation progressive d'iPhone19 (P1→P7). - fais $FACON et de façon autonome, le reste des taches. - génère $FACON, puis effectue des tests $FACON2 fonctionnels et performances des éléments de mon écosystème créés ou modifiés dans cette discussion hier et aujourd'hui dans l'objectif de corriger $FACON leurs failles et d'optimiser $FACON leur fonctionnement interne et au sein de mon écosystème. je précise que tu dois organiser l'exécution des tests en suivant la chronologie de la création ou de modification des éléments créés ou modifiés dans cette discussion (tous les éléments qui vont être POUSSER (ainsi que les éléments dont leur création ou leurs modifications de ces éléments POUSSER dépendent) sur mon dépôt doivent aussi être testés). - correct-work (projet) --bloc. - clone-chat. - PUSH avec ma clé "github_pat_11AJ…CTrp".} »

Glossaire (§A gen-plan, auto-contenu) : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) ».

Interprétation (règle d'or n°5, dérivée du disque) :
- **Item 1 — règle fidélité** : la règle propriétaire étend la protection existante (règle absolue 9 + G1/G3/G6/G7 + inventaire B6 couvrent visages/vêtements/accessoires/décor) avec trois ajouts : **« ne jamais inventer »** (principe absolu), **l'arrière-plan cité explicitement** dans l'énumération de fidélité, et la **condition maîtresse « si je ne t'ai pas précisé que je voulais que tu fasses des modifications »** (toute modification créative exige une demande explicite — cohérent règle 10/G7). Intégration en **règle absolue 15 + critère QC 14** (vérifiabilité mécanique) — **ajout pur** (convention v0.10.0/v0.11.0 : aucune règle 1-14, aucun R1-R19, aucun G1-G7, aucun QC 1-13 modifié ni affaibli). Ligne métier respectée : bump du PM source `skills/@photos/iphone19-photos.md` v0.11.0 → **v0.12.0 [ANTICIPÉE]** (v1.0.0 réservé génération confirmée §6.10) + archivage byte-identique v0.11.0 @historique/photos/ + INDEX + README §2 (règle du dépôt @photos), puis projection SKILL.md (description ADDITIVE — non-régression triggers).
- **Item 2 — re-curation P1→P7** : la méthode re-curation v1.2.0 exige P0 (PRE tests, GO) AVANT P1 — directive précédente 1a1bcb98c022bfe9 intégrée au skill (règle d'or 1 : « jamais de re-curation sans verdict PRE = GO »). Exécution P0 (baseline fraîche v0.12.0) puis P1→P7 comme demandé.
- **Item 3 — reste des tâches autonome** : items 4-7 + les exigences de cohérence de l'écosystème (worklog dépôt synchronisé — faille F-a détectée à l'ouverture ; SYNC-CONTEXT resync v1.5.8 — l'état documenté doit couvrir Task 80 + 81 avant PUSH).
- **Item 4 — campagne chronologique** : éléments créés/modifiés hier (2026-11-08 : Tasks 78 → 79 → 74 CLOSE → pendances 79 → Task 80 → Task 80 CLOSE) et aujourd'hui (2026-11-09 : Task 81), DANS L'ORDRE de création/modification, incluant tout ce qui sera POUSSÉ (les 3 commits non poussés + les commits du jour) et leurs DÉPENDANCES (5 arbitres, corpus PM, KB/pins/ULTRA, pipeline miroir). Outil : la suite v1.2.0 elle-même (F1/F2/F3) + arbitres écosystème.
- **Items 5-7** : correct-work (projet) --bloc → clone-chat → PUSH final avec délégation PAT explicite (dérogation KO-L009 point 5, précédents Task 63/77/79 G5 — jeton UNIQUEMENT en mémoire de commande, jamais persisté ; E15 à consigner : 5ᵉ exposition).

## État initial mesuré (E1-RES + E2, règle d'or n°5)

- **E1-RES (hook, complet)** : (1) B-11 — Task 80 CLOSE (e00bbe4, E8 FINAL 21:10:00Z), plans 72-80 clôturés, aucun plan en vol ; (2) G-RES **OK** (monitor.py — niveaux 0, PARALLELE) ; (3) fraîcheur : aucun plan en exécution ; (4) garde post-coupure (règle d'or n°9) : **version-management disparu à l'ouverture (récidive) → AUTO-RÉPARÉ É1-INSTALL v3.35.2 (INSTALLE-REPARÉ, rc=0)** — 54/54.
- **Git dépôt** : HEAD e00bbe4 · **avance 3 non poussés** (54090b4 · 40ed3d1 · e00bbe4) · arbre propre · remote SANS jeton (https://github.com/bigleon2/KNOWLEDGE.git) · branche main.
- **Corpus** : PM --check **4/4 COHERENT** (GEN-PLAN v3.41.0 · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1) · SHARED v1.7.36 · SYNC-CONTEXT **v1.5.7** (ne couvre pas Task 80 ni 81) · arbitres dernier verdict 5/5 (Task 80 : cross 100 % · vcw 16/16 · integrity 112/112 · doublons 0 · interactions 55/55 STRICT).
- **FAILLE F-a (détectée à l'ouverture, à corriger G4)** : worklog DÉPÔT stale — 1 806 lignes (dernier commit worklog ef51c55) vs worklog PROFIL 1 850 lignes : les suites 72-75 (Task 80, +32 lignes) n'ont pas été synchronisées dans les commits Task 80 → le PUSH publierait un dépôt dont le worklog contredit ses propres commits Task 80.
- **Cible iphone19** : SKILL.md v0.11.0 [ANTICIPÉE], 51 172 o (50,0 Kio LOURD — seuil 30 Kio), 466 lignes, 41 sections, 5 contrats (section_0_normalisee · read_when · evals ×2 · description_frontmatter), 0 scripts, 3 dépendances (skill-creator · VLM · image-edit [plateforme NON-VERSIONNÉ]), KB `## iphone19 v0.11.0` (ligne 381), pin ECO_SKILLS 0.11.0, PAS d'historique par-skill (à CRÉER), lignage PM `@photos/iphone19-photos.md` v0.11.0 (corps verbatim — recalibrage requis pour la projection curée post-re-curation).
- **Baseline PRE v1.2.0 (Task 80, hier)** : iphone19 **GO** (F1 PASS · F2 MESURÉ 50,0 Kio / 12 793 #token · F3 SAINES, empreinte 2a76554b…) — baseline capturée sur v0.11.0 : à RE-CAPTURER sur v0.12.0 après la règle (P0 de G2).
- **Chronologie des éléments à tester (G3)** : (hier) 18:09 Task 78 gen-plan v3.41.0 + cascade → 18:26 Task 79 G2 version-management re-curé 25,2 Kio → 18:35 Task 74 CLOSE livrables → 18:40 Task 79 CLOSE livrables → 19:17 pendances 79 (SYNC-CONTEXT v1.5.7 + protocole-test v1.1.0 + re-curation v1.1.0) → 20:42 Task 80 (protocole-test v1.2.0 + re-curation v1.2.0 + preuves ×4) → 20:46 Task 80 CLOSE (clone-chat 80 + plan FINAL) ; (aujourd'hui) Task 81 (iphone19 v0.12.0 + re-curation + cascade + livrables du jour).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Ouverture saine : garde n°9 — version-management disparu (récidive) AUTO-RÉPARÉ (INSTALLE-REPARÉ rc=0, 54/54) · G-RES OK · corpus PM --check 4/4 COHERENT · git HEAD e00bbe4, avance 3, arbre propre, remote sans jeton"
    verification: "ensure-installed.py --check (INSTALLE-REPARÉ, rc=0) && generer-pm-skill.py --check (4/4) && git -C KNOWLEDGE-repo rev-list origin/main..HEAD --count (=3) && git status (propre) — traces 2026-11-08T21:1xZ"
    source: "Directive 1a1bcf4fecbf5f29 ; règle d'or n°9 ; É1-INSTALL v3.35.2"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "État initial mesuré : baseline iphone19 v1.2.0 GO sur v0.11.0 (51 172 o, 5 contrats, 41 sections, F1/F2/F3) · v1.0.0 réservé → bump v0.12.0 MINOR ajouts purs · KB v0.11.0 ligne 381 · pin ECO_SKILLS 0.11.0 · historique par-skill ABSENT · FAILLE F-a worklog dépôt 1806 vs profil 1850 lignes (suites 72-75 non synchronisées) · convention @photos (bump + archive byte-identique + INDEX + README §2)"
    verification: "python3 -c json baseline (verdict GO, genere_par 1.2.0) && rg '## iphone19 v0.11.0' skills/KNOWLEDGE.md && wc -l worklogs (=1806/1850) && ls @historique/photos/INDEX.md"
    source: "Directive ; KO-L003 ; règle d'or n°5 ; file Task 72 G3 ; règle @photos/INDEX.md"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "G1 — Règle fidélité intégrée en règle absolue 15 + critère QC 14 (ajouts purs, auto-audit §11 : règles 1-14 · R1-R19 · G1-G7 · QC 1-13 intacts) : PM @photos v0.11.0→v0.12.0 [ANTICIPÉE] (règle 15 « ne jamais inventer et rester fidèle (visage, vêtement, arrière-plan, etc.) à l'image d'origine tant que le propriétaire n'a pas explicitement demandé des modifications » + QC 14 + §8 ligne fidélité (1-4, 14) + §9.3 ancrage + origine v0.12.0 + changelog + note rétroactive) + archive v0.11.0 byte-identique scellée SHA-256 + INDEX.md + README §2 + projection SKILL.md v0.12.0 (frontmatter + description ADDITIVE non-régression triggers + Lignage recalibré + corps v0.12.0) + cascade version (KB ## iphone19 v0.12.0 + Dernière calibration + pin ECO_SKILLS 0.12.0 + historiques-par-skill/iphone19.md CRÉÉ + ULTRA régénéré)"
    verification: "rg -c 'règle absolue 15|Règle absolue 15|FIDÉLITÉ TOTALE' @photos/iphone19-photos.md (>=1) && rg 'Version 0.12.0' @photos && diff archive vs blob git v0.11.0 (byte-identique) && rg '## iphone19 v0.12.0' KNOWLEDGE.md && integrity 112/112 && --verifier iphone19 (F3 SAINES)"
    source: "Directive item 1 (verbatim règle) ; convention @photos (INDEX) ; non-régression triggers v1.2.0 ; KO-L004"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "G2 — Re-curation P0→P7 : P0 --pre iphone19 v0.12.0 baseline fraîche → GO (3 familles) · P1 mesure-sections (blocs ≥ 1,5 Kio hors contrats) · P2 --compare (méthode la plus optimisée R4-compliante) · P3 moves R4 byte-identité (script dédié verrouillé count==1, en-têtes provenance) + P4 résumés inline + pointeurs (contrats verbatim intacts) · P5 POST ×2 MAINTIEN DE L'OPTIMISATION (COHÉRENT · FONCTIONNEL · OPTIMISÉ · INTERACTIONS SAINES · PERF STABLE) · P6 re-jeu ×2 no-op + arbitres 5/5 · P7 check-recuration C1-C4 + Lignage « projection curée » + sync miroir MÊME PASSE (pipeline 54/54, version-management présent)"
    verification: "protocole-test.py --pre iphone19 (GO, genere_par 1.2.0, v0.12.0) && --compare && --post ×2 (MAINTIEN ×2) && check-recuration.py iphone19 (C1-C4 PASS) && eco_install_pipeline.py (rc=0, 54/54)"
    source: "Directive item 2 (P1→P7) ; re-curation §2 (P0 golden rule 1) ; précédent version-management Task 79 G2"
    priority: "S1"
    status: "verified-avec-ecart (C4 classe LOURD 39,5 Kio assumée — cœur opérationnel intrinsèque : sub-LOURD exigeait d'externaliser grille ANALYSE + moteur R1-R19 [dégradation par-mission refusée] ; C1-C3 PASS · R4-INTÈGRE 6/6 · POST ×2 MAINTIEN [harnais v1.2.1 correctif idempotence] · pipeline 54/54 — détail worklog suite 78)"
  - id: "D005"
    criterion: "G3 — Campagne de tests fonctionnels + performance $FACON2 en ORDRE CHRONOLOGIQUE (hier 2026-11-08 → aujourd'hui 2026-11-09) sur les éléments créés/modifiés de la discussion + tout ce qui sera POUSSÉ + dépendances : T1 gen-plan v3.41.0 --verifier · T2 version-management v1.3.0 --verifier · T3 SYNC-CONTEXT v1.5.7 (cohérence citations ↔ corpus réel) · T4 protocole-test.py v1.2.0 selftest 13/13 ×2 + re-curation v1.2.0 --verifier · T5 preuves Task 80 (baselines ×4 valides) · T6 livrables Tasks 74/79/80 (clones-chat, rapports, plans — présence, statuts finaux, 0 jeton complet) · T7 iphone19 v0.12.0 (référence croisée G1/G2 : PRE GO + POST ×2 + C1-C4) · T8 dépendances (5 arbitres un bloc + corpus --check 4/4 + pipeline 54/54) · T9 artefacts du jour — failles corrigées (dont F-a) + rapport download/rapport-campagne-tests-task81.md"
    verification: "protocole-test.py --verifier gen-plan && --verifier version-management && --selftest (13/13 ×2) && --verifier re-curation && 5 arbitres rc=0 && corpus 4/4 && pipeline 54/54 && ls download/rapport-campagne-tests-task81.md (verdicts par élément, chronologie tracée)"
    source: "Directive item 4 (chronologie + POUSSER + dépendances) ; re-curation v1.2.0 (F1/F2/F3) ; règle d'or n°5"
    priority: "S1"
    status: "verified (15/15 éléments PASS — selftest re-jeu 14/14 ×2 v1.2.1 [évolution 13/13 documentée] ; rapport download/rapport-campagne-tests-task81.md profil+dépôt ; métrique #token recalculée 13 911→10 107, −3 804/chargement)"
  - id: "D006"
    criterion: "G4 — Cohérence avant clôture : SYNC-CONTEXT v1.5.8 resync (état corpus couvrant Task 80 [re-curation v1.2.0, suite 3 familles] + Task 81 [iphone19 v0.12.0 règle 15 + re-curation P1→P7], citations recalées) + FAILLE F-a ÉTEINTE (worklog dépôt ← profil : suites 72-75 + suites du jour) + livrables syncés dépôt (plan 81 + rapport campagne) + commit local Task 81 (message détaillé)"
    verification: "rg 'v1.5.8' SYNC-CONTEXT.md && diff worklog dépôt vs profil (identiques) && git -C KNOWLEDGE-repo log --oneline -1 (commit Task 81) && git status (propre)"
    source: "Directive item 3 (reste autonome) ; SYNC-CONTEXT v1.5.7 lag ; faille F-a ; R5"
    priority: "S2"
    status: "pending"
  - id: "D007"
    criterion: "G5 — Clôture conforme : correct-work (projet) --bloc (B1 installation+certification · B2 corpus+KB+outillage · B3 livrables 81 · B4 extension/pendances) agrégation pire-des-verdicts PASS · clone-chat session 81 scellé (§0-§5, 0 secret, jeton tronqué) · E8 FINAL answer key 10/10 verified horodatages couplés · check_plan_protocol P1-P5 PASS · commit final CLOSE"
    verification: "verdict CW --bloc consigné worklog + rapport download/ && ls download/clone-chat-session-web-ecef7f80-20261109-task81.md && answer key verified + horodatage final couplé + P1-P5 PASS"
    source: "Directive items 5-6 ; mode step §5.5 ; E7-DISP ; précédents Task 76-80"
    priority: "S1"
    status: "pending"
  - id: "D008"
    criterion: "G6 — PUSH final délégation PAT (protocole Task 63/77) : cadre zéro-persistance vérifié AVANT (remote sans jeton · credential.helper AUCUN local+global · ~/.git-credentials absent · jeton complet 0 occurrence disque) + pré-vol (fsck --full rc=0 · commits en attente listés · ls-remote authentifié rc=0 · SHA distant == merge-base → fast-forward pur prouvé) + push one-shot rc=0 (jeton UNIQUEMENT en mémoire de commande — jamais git config ni fichier) + post-push (distant == HEAD · avance 0 · zéro-persistance re-vérifiée) + E15 : RÉVOCATION/ROTATION PAT consignée (5ᵉ exposition)"
    verification: "cadre vérifié (grep remote/credentials) && fsck rc=0 && push rc=0 && git ls-remote (== HEAD local) && re-vérification zéro-persistance && E15 au worklog + clone-chat"
    source: "Directive item 7 (PUSH avec la clé) ; dérogation KO-L009 point 5 ; précédents Task 63/77/79 G5"
    priority: "S1"
    status: "pending"
```

## Estimation et profil (E3-E6)

- **E3** : Type 2 (développement/édition Markdown + scripts Python N3 + preuves JSON — aucun docx/pdf/xlsx/pptx).
- **E4** : G1 ≈ 6 500 · G2 ≈ 9 000 · G3 ≈ 8 000 · G4 ≈ 2 500 · G5 ≈ 5 000 · G6 ≈ 1 500 — **total ≈ 32 500 #token** (bornes 24 000-44 000).
- **E5-POIDS** : gen-plan 29,9 Kio INTERMÉDIAIRE (lecture ciblée FAITE — §A/§0/§1.2bis/§1.5/§5.5) · re-curation 18,2 Kio (intégrale — méthode P0-P7 exécutée) · iphone19 50,0 Kio LOURD (cible — intégrale de travail légitime, lecture bloc par bloc faite) · correct-work 28,6 Kio (contrat --bloc).
- **E6** : NORMAL (G-RES OK — PARALLELE ; vagues internes par défaut, série entre groupes justifiée par les écritures chaînées).

## G1 — Règle fidélité iphone19 v0.12.0 (ligne métier + projection + cascade version) `[À FAIRE]` (0/3)

- **SG1.1 Ligne métier PM @photos** (D003) : T1.1.1 archivage v0.11.0 — extraction git byte-identique → `@historique/photos/iphone19-photos-v0.11.0.md` + scellement SHA-256 + INDEX.md (table) + README @photos §2 ; T1.1.2 bump PM vivant v0.12.0 [ANTICIPÉE] — règle absolue **15** (fidélité totale à l'image d'origine, condition maîtresse « sauf demande explicite de modifications ») + **QC critère 14** + §8 (fidélité 1-4, 14) + §9.3 ancrage règle 15 + bloc origine v0.12.0 + changelog v0.11.0→v0.12.0 + note rétroactive §11 + auto-audit (ajouts purs, invariants intacts).
- **SG1.2 Projection skill** (D003) : T1.2.1 SKILL.md frontmatter v0.12.0 + description **ADDITIVE** (mention fidélité image d'origine sauf demande explicite — phrases existantes verbatim) + Lignage recalibré (v0.12.0, directive tracée) ; T1.2.2 corps projeté v0.12.0 (règle 15 + QC 14 + propagations §8/§9/§11) · evals contrats intacts vérifiés (recalibrés uniquement si le contenu additif l'exige — sinon inchangés).
- **SG1.3 Cascade version (gouvernance KB + ECO_SKILLS)** (D003) : T1.3.1 KB `## iphone19 v0.12.0` (description recalée + Dernière calibration bump règle 15) ; T1.3.2 pin ECO_SKILLS integrity → 0.12.0 (KO-L004) + `historiques-par-skill/iphone19.md` CRÉÉ (vivante v0.12.0) + ULTRA régénéré ; T1.3.3 pré-contrôle `--verifier iphone19` (F1/F2/F3 — alignement KB/pin attendu SAINES).

## G2 — Re-curation progressive disclosure iphone19 (P0→P7) `[À FAIRE]` (0/3)

- **SG2.1 P0-P2** (D004) : T2.1.1 **P0** `--pre iphone19` — baseline v1.2.0 FRAÎCHE sur v0.12.0 → **GO exigé** (3 familles ; jamais de re-curation d'un élément déjà cassé) ; T2.1.2 **P1** cartographie `mesure-sections.py iphone19` (blocs ≥ 1,5 Kio hors contrats, gains projetés) ; T2.1.3 **P2** `--compare iphone19` (méthode la plus optimisée et performante R4-compliante — suppression disqualifiée d'office).
- **SG2.2 P3-P5** (D004) : T2.2.1 **P3** script d'extraction dédié de la passe (moves R4 byte-identité, verrouillé count==1, en-têtes de provenance section/version/date/SHA-256) ; T2.2.2 **P4** résumés opérationnels inline + pointeurs `references/` (aucune duplication, contrats verbatim intacts) ; T2.2.3 **P5** `--post iphone19` **×2** → MAINTIEN DE L'OPTIMISATION (5 dimensions : COHÉRENT · FONCTIONNEL · OPTIMISÉ · INTERACTIONS SAINES · PERF STABLE).
- **SG2.3 P6-P7** (D004) : T2.3.1 **P6** re-jeu ×2 no-op du script de passe + arbitres 5/5 un bloc (integrity recalibré · verify-cross · verify-correct-work · doublons · coherence) ; T2.3.2 **P7** `check-recuration.py iphone19` (C1-C4) + Lignage « projection curée » (intégraux en references/, PM source = intégral de référence) + KB calibration re-curation + ULTRA stable + **sync miroir MÊME PASSE** (pipeline 54/54, version-management présent anti-disparition).

## G3 — Campagne de tests fonctionnels + performance chronologique `[À FAIRE]` (0/3)

- **SG3.1 Chronologie hier (2026-11-08, 18:09 → 20:46)** (D005) : T3.1.1 **T1 gen-plan v3.41.0** (18:09 Task 78) — `--verifier gen-plan` (F1 selftests scripts + F2 poids/durées + F3 interactions) ; T3.1.2 **T2 version-management v1.3.0 re-curé** (18:26 Task 79 G2) — `--verifier version-management` + **T3 SYNC-CONTEXT v1.5.7** (19:17) — cohérence citations ↔ corpus réel (GEN-PLAN/CORRECT-WORK/CLONE-CHAT/REFACTOR-GUARD/INSTALL/SHARED/README versions + 119 porteurs §0) ; T3.1.3 **T4 protocole-test.py v1.2.0 + re-curation v1.2.0** (19:17→20:42) — `--selftest` 13/13 ×2 idempotent + `--verifier re-curation` + **T5 preuves Task 80** (baselines ×4 : structure, verdicts, genere_par 1.2.0) + **T6 livrables Tasks 74/79/80** (clones-chat, rapports CW --bloc, rapports finaux, plans — présence, statuts finaux, 0 occurrence jeton complet sur disque).
- **SG3.2 Chronologie aujourd'hui (2026-11-09)** (D005) : T3.2.1 **T7 iphone19 v0.12.0** (référence croisée G1/G2 : PRE GO + POST ×2 MAINTIEN + C1-C4 + règle 15/QC 14 vérifiés en texte) ; T3.2.2 **T8 dépendances de tout ce qui est poussé** — 5 arbitres un bloc (verify-cross 100 % · vcw 16/16 · integrity 112/112 · doublons 0 · coherence STRICT) + corpus `--check` 4/4 + pipeline miroir 54/54.
- **SG3.3 Corrections + rapport** (D005) : T3.3.1 correction des failles détectées (F-a worklog → corrigée G4 ; toute faille nouvelle corrigée dans la passe — max 2 rounds) ; T3.3.2 **rapport campagne** `download/rapport-campagne-tests-task81.md` (ordre chronologique, verdicts par élément F1/F2/F3, métriques, failles + corrections) + projection dépôt.

## G4 — SYNC-CONTEXT v1.5.8 + worklog sync + commit local `[À FAIRE]` (0/3)

- T4.1 SYNC-CONTEXT **v1.5.8** (révision resync état : corpus + lignée Task 80 [re-curation v1.2.0 suite 3 familles + preuves PRE GO ×4] + Task 81 [iphone19 v0.12.0 règle 15 + re-curation P1→P7] — procédure inchangée, citations recalées) ;
- T4.2 **FAILLE F-a ÉTEINTE** — worklog dépôt ← profil (suites 72-75 + suites du jour) ;
- T4.3 livrables du jour syncés dépôt (plan 81 + rapport campagne) + **commit local Task 81** (message détaillé : règle 15, re-curation chiffres, campagne, F-a, cascade).

## G5 — correct-work (projet) --bloc + clone-chat + E8 FINAL `[À FAIRE]` (0/2)

- T5.1 **CW (projet) --bloc** B1-B4 (B1 installation+certification · B2 corpus+KB+outillage · B3 livrables 81 · B4 extension/pendances) — agrégation pire-des-verdicts, max 2 rounds/bloc, délégation alias-eco §10.1 (registre vérifié) ;
- T5.2 **clone-chat session 81** (§0-§5, drifts typés, leçons, 0 secret — jeton tronqué) + **E8 FINAL** (answer key 10/10 verified, horodatages couplés) + check_plan_protocol P1-P5 + commit final Task 81 CLOSE.

## G6 — PUSH final (délégation PAT — protocole Task 63/77) `[À FAIRE]` (0/2)

- T6.1 **cadre zéro-persistance AVANT** (remote sans jeton · credential.helper AUCUN local+global · ~/.git-credentials ABSENT · jeton complet 0 occurrence disque) + **pré-vol** (fsck --full rc=0 · commits en attente listés [3 hérités + commits du jour] · ls-remote authentifié rc=0 · SHA distant == merge-base → fast-forward pur prouvé) ;
- T6.2 **push one-shot rc=0** (jeton UNIQUEMENT en mémoire de commande — URL one-shot, jamais git config ni fichier) + **post-push** (distant == HEAD · avance 0 · zéro-persistance re-vérifiée) + **E15 : RÉVOCATION/ROTATION du PAT — 5ᵉ exposition** (2026-10-26 · 2026-11-07 · 2026-11-08 ×2 · 2026-11-09) consignée worklog + clone-chat + chat final.

## PLAN-AFFICHE

(Task 81 — download/plan-task81-iphone19-regle-fidelite-recuration-campagne-tests-cw-push.md — INITIAL — **G1 règle fidélité iphone19 v0.12.0 [À FAIRE] 0/3 · G2 re-curation P0→P7 [À FAIRE] 0/3 · G3 campagne tests chronologique [À FAIRE] 0/3 · G4 SYNC-CONTEXT v1.5.8 + worklog + commit [À FAIRE] 0/3 · G5 CW --bloc + clone-chat + E8 FINAL [À FAIRE] 0/2 · G6 PUSH final PAT [À FAIRE] 0/2** — answer key 8 décisions (D001-D002 verified ouverture · D003-D008 pending exécution) — E8 initial PASS 2026-11-08T21:25:00Z — #token ≈ 32 500 (bornes 24 000-44 000) — exécution step : G1→G6 chaîne autonome (série justifiée ENTRE groupes : écritures chaînées règle→re-curation→campagne→clôture→push), vagues PAR INTERNES (selftests ×2, arbitres un bloc, preuves indépendantes) — fenêtre native TodoWrite : affichée au début d'exécution, mise à jour à chaque fin de groupe (E7-DISP point 6))

Verdict E8 : PASS INITIAL (8 décisions — D001 ouverture saine [garde n°9 auto-réparation version-management INSTALLE-REPARÉ rc=0, G-RES OK, corpus 4/4, avance 3, arbre propre] · D002 état mesuré [baseline GO v0.11.0 50,0 Kio, bump v0.12.0 MINOR, KB/pin/historique, FAILLE F-a worklog 1806/1850, convention @photos] — D003-D008 pending exécution, critères vérifiables armés) — Horodatage vérifié : 2026-11-08T21:25:00Z
