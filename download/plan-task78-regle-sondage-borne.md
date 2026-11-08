# Plan Task 78 — Règle de sondage borné (gen-plan v3.41.0) : protocole d'inspection bornée des greps et lectures transverses

**Horodatage plan : 2026-11-08T18:05:00Z (FINAL — 10 décisions : 10/10 verified, horodatage verdict couplé)** · Mode : gen-plan(step) · Session : web-ecef7f80 · Trace directive : 1a1bbf9f403a2865 · Prérequis vérifié : Task 77 CLOSE (E8 final PASS 2026-11-08T11:00:00Z, 16/16, commit 7d86b3d PUSHé, distant == HEAD) · Task 74 EN VOL au GO propriétaire — INTACTE (R2, hors périmètre)

## Contexte et périmètre

Directive propriétaire (2026-11-08, trace 1a1bbf9f403a2865), 2 items :
1. « génère le plan du Task "règle de sondage borné", puis intègre-le au plan d'actions actuel. »
2. « dis-moi quelles tâches restent à faire. »

Interprétation (règle d'or n°5, dérivée du disque) :
- **Item 1 — objet du Task 78** : ajouter à gen-plan (**v3.41.0, MINOR**) la **règle de sondage borné** — extension de la discipline « lecture ciblée » (hook E5-POIDS v3.38.0, qui ne couvre que les lectures de skills LOURD/CRITIQUE) aux **commandes d'inspection transverses** (greps/lectures d'arbre) pendant l'exécution des plans. Origine : durant SG2.2 du Task 77 (cascade SHARED v1.7.35), avertissement « Sortie trop volumineuse (en-tête SHARED très long) — reprise en greps ciblés, lignes tronquées » : le réflexe borné a été appliqué au vol mais n'est codifié NULLE PART dans gen-plan (vérifié mécaniquement). Le présent échange génère le plan (E1-E8 INITIAL) et l'intègre à la file d'actions (worklog suite 65 + PLAN-AFFICHE) ; **l'exécution des groupes G1-G3 reste à déclencher au GO du propriétaire** (gen-plan step / step-ok).
- **Item 2** : réponse au chat (file d'actions à jour) — PAS un groupe du présent plan.

Alternatives écartées (analyse pré-directive, mesures session — règle d'or n°5) :
- **re-curation** : le §0 SHARED est un contrat d'amorçage — l'auto-contenance SHARED §6.2/§9 (« aucune lecture externe requise ») interdit de le déplacer vers references/ ; et le protocole re-curation a DÉJÀ été passé sur gen-plan (2026-11-08, download/protocole-test-gen-plan.json : POST « MAINTIEN DE L'OPTIMISATION », réduction 0,0 %).
- **refactoring** : la duplication du §0 est VOLONTAIRE (pattern d'injection de contexte — 119 SKILL.md) ; une centralisation « SHARED + pointeur » altérerait le comportement de chaque exécution de skill (interdit refactor-guard — zéro-régression).
- **Verdict** : le symptôme est un **déficit de protocole de sondage**, pas un poids de skill → correctif gen-plan v3.41.0.

## État initial mesuré (E1-RES + E2, règle d'or n°5)

- **E1-RES (hook complet)** : (1) worklog frais — Task 77 CLOSE (suite 64 : G4 + finale, 16/16, commit 7d86b3d PUSHé) ; (2) G-RES **OK — PARALLELE** (monitor.py) ; (3) fraîcheur : aucun plan en vol de la présente session ; (4) **garde post-coupure : cas §3.4 détecté** (gen-plan + correct-work + version-management + registre KB absents de l'hôte — wipe inter-sessions partiel, 2ᵉ occurrence consécutive) → **réinstallation IMMÉDIATE voie directe §3.2-a : `eco_install_pipeline.py` rc=0** — post-install **54/54 SHA-256 vérifiés, 0 divergence**, garde R2 passante, archive rescellée round-trip (véhicule v2.2, corpus 9/9) — 2ᵉ validation en conditions réelles des correctifs Task 76 F1-F5.
- **Certification d'ouverture** (4 arbitres + monitor émis en UN BLOC de 5 commandes parallèles — protocole d'émission v3.40.0 appliqué à l'ouverture) : verify-cross **100,0 %, 0 erreur** · verify-correct-work **16/16 ALL PASS** · check-ecosysteme-integrity **112/112 PASS, 0 FAIL** · task14-scan-doublons **0 doublon (269 uniques)**.
- **Diagnostic sondage (mesures)** : §0 SHARED de gen-plan = **1 653 o** (lignes jusqu'à **422 o**) ; lignes les plus longues du SKILL.md = **1 074 o** (changelog) ; §0 dupliqué dans **119 SKILL.md** du dépôt (cumul ≈ 236 Kio, moyenne 2,0 Kio, max **qingyan-research 15,1 Kio**) — tout match de grep imprime ces lignes EN ENTIER → plafond de sortie atteint en SG2.2, diagnostic perdu puis repris manuellement.
- **Absence de règle (vérifié mécaniquement)** : aucun « sondage borné » / max-columns / head_limit dans gen-plan v3.40.0 (SKILL.md + 15 references/) ; doctrine sœur EXISTANTE à étendre : **E5-POIDS voie « lecture ciblée »** (§1.2bis) couvre les lectures de skills, PAS les greps transverses.
- **Budget byte** : gen-plan v3.40.0 = **30 666 o** vs seuil LOURD 30 720 o (30 Kio, C4 re-curation) → **tête 54 o** → amendement inline avec compensations byte (résumés compactés, intégraux references/ intacts — précédent v3.40.0, ABANDON rc=2 si budget dépassé).
- **Fichiers cibles mesurés** : protocoles-detailles.md 23 919 o · graph-diamond-pattern.md 5 246 o (HORS périmètre au présent Task) · correct-work 28,6 Kio (INTERMÉDIAIRE).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Ouverture saine post-wipe (2ᵉ occurrence consécutive) : réinstallation PM-INSTALL voie directe §3.2-a rc=0 — post-install 54/54 SHA-256 vérifiés, 0 divergence, garde R2 passante, archive rescellée round-trip (véhicule v2.2, corpus 9/9)"
    verification: "python3 scripts/eco_install_pipeline.py → rc=0, JSON post_install.sha256_verifies==54 et post_install.divergences==[] (traces session 2026-11-08T16:25Z)"
    source: "Règle d'or n°9 (garde mécanique à toute invocation) ; PM-INSTALL §3.2-a/§3.4 ; précédents Task 74/77"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "Certification d'ouverture : verify-cross 100,0 % (0 erreur) · verify-correct-work 16/16 ALL PASS · check-ecosysteme-integrity 112/112 PASS 0 FAIL · task14-scan-doublons 0 doublon (269 uniques) — 4 arbitres + monitor émis en un bloc de 5 commandes parallèles (protocole d'émission v3.40.0)"
    verification: "re-jeu des 4 arbitres (rc=0 chacun) — traces session 2026-11-08T16:26Z"
    source: "Ordre §3.3 étape 9 (certification) ; protocole d'émission parallèle gen-plan v3.40.0"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Diagnostic sondage mesuré et absence de règle vérifiée : §0 gen-plan 1 653 o (lignes ≤ 422 o), lignes max SKILL.md 1 074 o, §0 dupliqué dans 119 SKILL.md (moyenne 2,0 Kio, max qingyan-research 15,1 Kio) ; 0 occurrence de max-columns/head_limit/« sondage » dans gen-plan v3.40.0 (SKILL.md + references/)"
    verification: "awk '/^## §0/{f=1;next} f&&/^## /{f=0} f' skills/gen-plan/SKILL.md | wc -c (=1653) && rg -c 'max-columns|head_limit|sondage' skills/gen-plan/SKILL.md skills/gen-plan/references/*.md (0 match)"
    source: "Directive item 1 (origine SG2.2 Task 77) ; analyse pré-directive session web-ecef7f80"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Amendement chirurgical inline gen-plan v3.41.0 : rangée « Sondage borné » au §1.2bis (étape E9-E14) + rappel compact au #4 (émission + sondage) + §5.6 entrée courante v3.41.0 (v3.40.0 migrée R4 vers journal-versions.md) — SKILL.md < 30 720 o après compensations byte (résumés compactés, intégraux references/ intacts) ; description frontmatter et §A INCHANGÉS (non-régression triggers — précédents v3.32.0/v3.40.0)"
    verification: "wc -c skills/gen-plan/SKILL.md (< 30720) && rg -c 'Sondage borné' skills/gen-plan/SKILL.md (≥ 1) && protocole-test.py --post (contrat description_frontmatter PASS, evals/trigger_evals intacts)"
    source: "Directive item 1 ; précédent v3.40.0 (task77-amendement — ABANDON rc=2 si budget dépassé)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Intégral protocoles-detailles.md « Extension v3.41.0 — Sondage borné » (insérée après le bloc extension v3.40.0) : (1) jamais de pattern générique sur l'arbre sans mode -l ; (2) greps multi-fichiers bornés (--max-columns + head_limit) ; (3) §0/contrats jamais catés en entier — lectures par plages de lignes ; (4) exceptions : golden-master et lecture de contrats PRE/POST (un fichier à la fois) — volumétrie motivée par les mesures T1.1.1 + anti-régression"
    verification: "rg -n 'Extension v3.41.0 — Sondage borné' skills/gen-plan/references/protocoles-detailles.md (présent, positionné après la section v3.40.0) && les 4 règles numérotées présentes"
    source: "Directive item 1 ; précédent v3.40.0 (protocoles-detailles extension +3,6 Kio)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Cascade KO-L004 périmètre gen-plan (SHARED et PM-INSTALL INCHANGÉS) : PM GEN-PLAN v3.41.0 généré mécaniquement (delta verrouillé, generer-pm-skill --check 4/4 familles) · PM v3.40.0 archivé R4 (git mv + sceau SHA-256 + inscription RETRAITS_SANCTIONNES) · registre KB v3.41.0 · pin ECO_SKILLS 3.41.0 ×2 arbres · historiques-par-skill/gen-plan.md · README @historique + README corpus (comptages mécaniques) · ULTRA régénéré ×2 idempotent (SHA stable)"
    verification: "présence des 8 artefacts (ls + rg) && ULTRA régénéré ×2 → SHA identique && rg 'gen-plan v3.41.0' skills/KNOWLEDGE.md"
    source: "Famille PM gen-plan → cascade KO-L004 complète ; précédent Task 77 T2.2.2 (16 artefacts)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Preuves comportementales et de non-régression : mesure volumétrie grep BRUT vs BORNÉ sur skills/*/SKILL.md (même pattern, bytes émis comparés — ratio consigné au worklog) + protocole-test.py --pre gen-plan verdict GO (baseline v3.40.0 capturée AVANT amendement) puis --post ×2 MAINTIEN DE L'OPTIMISATION (COHÉRENT/FONCTIONNEL/OPTIMISÉ, poids < 30 Kio tenu)"
    verification: "protocole-test.py --pre (GO, baseline) puis --post ×2 (MAINTIEN DE L'OPTIMISATION) && mesures volumétrie au worklog (2 lignes chiffrées)"
    source: "Règle d'or n°5 (tests avant re-curation — analogie amendement) ; skill re-curation §2 P0/P5"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Arbitres post-cascade en un bloc PAR : verify-cross 100 % · verify-correct-work 16/16 · integrity 112/112 · doublons 0 · coherence PASS STRICT — sweep citations vives gen-plan v3.40.0→v3.41.0 recalé (précédent Task 77 : 9 citations context/fleet/graph/harness/loop/memory/refactoring-engineering/refactoring-test/spec-driven-development, max 2 rounds)"
    verification: "re-jeu des 5 arbitres (rc=0 chacun, un bloc) && test-coherence-interactions.py PASS STRICT après sweep"
    source: "Ordre §3.3 étape 9 ; précédent Task 77 T2.2.3 (9 citations recalées)"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "Sync hôte : eco_install_pipeline rc=0 — 54/54 SHA-256 vérifiés, retrait PM v3.40.0 inscrit RETRAITS_SANCTIONNES, archive rescellée round-trip véhicule v2.2"
    verification: "python3 scripts/eco_install_pipeline.py → rc=0, post_install.sha256_verifies==54, divergences==[]"
    source: "PM-INSTALL v1.9.12 ; précédent Task 77 T2.2.3 (aller-retour RETRAITS_SANCTIONNES documenté)"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Clôture : E8 final answer key 10/10 verified, horodatage plan == horodatage verdict (KO-L003), check_plan_protocol P1-P5 PASS post-finalisation, fenêtre native maintenue G1→G3, commit dédié Task 78 SANS les mode-purs (R2 — héritage Task 74/76) — PUSH = propriétaire (KO-L009, délégation PAT possible — précédents Task 63/77) ; correct-work (projet) + clone-chat recommandés au GO (hors périmètre présent)"
    verification: "check_plan_protocol.py --plan --worklog PASS && git log (1 commit dédié Task 78) && git status (mode-purs intacts, non-commités)"
    source: "gen-plan E7-DISP point 3 (horodatages couplés) ; KO-L009/D013 ; précédents Task 76/77"
    priority: "S1"
    status: "verified"
```

## Estimation et profil (E3-E6)

- **E3** : Type 2 (analyse/amendement + livrables documentaires Markdown/JSON — aucun docx/pdf/xlsx/pptx).
- **E4** : G1 ≈ 4 000 · G2 ≈ 4 000 · G3 ≈ 3 000 · réserve E13 ≈ 2 500 — **total ≈ 13 500 #token** (bornes 9 000-20 000).
- **E5-POIDS** : gen-plan 29,9 Kio ≈ 7 666 #token (INTERMÉDIAIRE, rang 13 — lecture ciblée §0 + sections dédiées, JAMAIS intégrale) · correct-work 28,6 Kio (INTERMÉDIAIRE — lectures ciblées) · protocoles-detailles.md 23,4 Kio (lecture par sections).
- **E6** : NORMAL (G-RES OK — mode recommandé PARALLELE, aucune cause).

## G1 — Diagnostic PRE + amendement gen-plan v3.41.0 `[TERMINÉ]` (3/3)

- **SG1.1 PRE — preuves avant écriture** :
  - **T1.1.1 Mesure volumétrie de sondage [VAGUE-PAR T1.1.1-a ∥ T1.1.1-b — lectures seules, aucune écriture partagée]** : (a) grep BRUT d'un pattern générique (« Contexte Système ») sur skills/*/SKILL.md — bytes émis mesurés ; (b) même grep BORNÉ (-l puis troncature + head_limit) — bytes émis mesurés ; ratio consigné (motivation chiffrée de la règle).
  - **T1.1.2 Baseline golden master** : `protocole-test.py --pre gen-plan` → verdict GO/NO-GO (NO-GO = amendement non déclenché).
- **SG1.2 Amendement chirurgical** (script dédié `scripts/task78-amendement-v3410.py` — éditions assert count==1, idempotent ×2, ABANDON rc=2 sans écriture si budget dépassé) :
  - **T1.2.1 Inline SKILL.md v3.41.0** (D004) : rangée « Sondage borné » §1.2bis + rappel #4 + §5.6 (migration R4 v3.40.0 → journal-versions.md) + compensations byte → **< 30 720 o** ; description frontmatter + §A intacts.
  - **T1.2.2 Intégral protocoles-detailles.md** (D005) : « Extension v3.41.0 — Sondage borné » (4 règles + exceptions + volumétrie motivée + anti-régression), insérée après le bloc extension v3.40.0.
- **SG1.3 correct-work(G1)** : PASS requis (max 2 rounds) → G2.

## G2 — Cascade KO-L004 (périmètre gen-plan) + sync hôte `[TERMINÉ]` (3/3)

- **SG2.1 Cascade** (scripts `task78-{delta,cascade}.py` — idempotents ×2, comptages mécaniques KO-L003) (D006) : PM GEN-PLAN v3.41.0 (delta verrouillé + generer-pm-skill --check 4/4 familles) · PM v3.40.0 archivé R4 (git mv + sceau + RETRAITS_SANCTIONNES task21-f2) · registre KB · pin ECO_SKILLS ×2 arbres · historiques-par-skill/gen-plan.md · README @historique + README corpus · ULTRA ×2 idempotent · **SHARED et PM-INSTALL INCHANGÉS** (règle gen-plan-scopée — pas de recalibrage écosystème, pas de propagation §0).
- **SG2.2 Sync hôte** (D009) : `eco_install_pipeline.py` rc=0 (54/54 SHA-256, retrait PM v3.40.0 inscrit, archive rescellée round-trip v2.2).
- **SG2.3 correct-work(G2)** : PASS requis → G3.

## G3 — Preuves + arbitres + E8 final + commit `[TERMINÉ]` (3/3)

- **SG3.1 Preuves et arbitres [VAGUE-PAR : T3.1.1 protocole-test --post ×2 ∥ T3.1.2 les 5 arbitres en un bloc]** (D007, D008) : POST ×2 MAINTIEN DE L'OPTIMISATION · verify-cross 100 % · verify-correct-work 16/16 · integrity 112/112 · doublons 0 · coherence PASS STRICT — **sweep citations vives v3.40.0→v3.41.0** (max 2 rounds).
- **SG3.2 E8 final** (D010) : answer key 10/10 verified · horodatages couplés (KO-L003) · check_plan_protocol P1-P5 PASS post-finalisation · fenêtre native maintenue G1→G3 (E7-DISP point 6).
- **SG3.3 Clôture** : commit dédié Task 78 SANS les mode-purs (R2) + sync dépôt livrables + marqueur **TASK 78 CLOSE** · **PUSH = propriétaire (KO-L009)** · correct-work (projet) + clone-chat recommandés au GO (hors périmètre présent — précédent Task 77 G3/G4).

## PLAN-AFFICHE

(Task 78 — download/plan-task78-regle-sondage-borne.md — FINAL — **G1 Diagnostic + amendement ✅ 3/3 · G2 Cascade + sync ✅ 3/3 · G3 Preuves + clôture ✅ 3/3** — answer key 10 décisions (D001-D003 verified ouverture · D004-D010 pending exécution) — E8 initial PASS 2026-11-08T16:32:00Z (answer-key-checker 16/16 ×2 sha16 stable + check_plan_protocol P1-P5) — #token ≈ 13 500 (bornes 9 000-20 000) — exécution step : G1→G2→G3 séquentiel (écritures chaînées sur les mêmes fichiers — amendement → cascade → preuves), vagues PAR aux PRE (T1.1.1) et aux preuves/arbitres (SG3.1) — fenêtre native TodoWrite : affichée au début d'exécution, mise à jour à chaque fin de groupe (E7-DISP point 6))

Verdict E8 : PASS FINAL (10/10 décisions verified — D001-D003 ouverture · D004 amendement v3.41.0 [30 697 o < 30 720, description/§A intacts, idempotence amendement NO-OP ×2] · D005 extension protocoles-detailles [4 règles + exceptions, +15 L] · D006 cascade [PM v3.41.0 1 810 L + PM v3.40.0 archivé R4 sceau 8fa129f9… + KB + pin ×2 + historiques + README ×2 + ULTRA ×2 SHA 1eb7269eb078… ; ÉCART consigné règle d'or n°5 : SHARED v1.7.36 + PM-INSTALL v1.9.13 recalibrés par le générateur contrairement au plan, réversion = lag §6.1 — propagation §0 v1.7.36 convergée 0/0/0] · D007 preuves [PRE GO baseline v3.40.0 6 contrats 31 sections · POST ×2 MAINTIEN DE L'OPTIMISATION · volumétrie BRUT 12 207 o / BORNÉ 3 763 o ×3,2, re-mesure fraîche 11 068/3 168 ×3,5] · D008 arbitres [cross 100,0 % · vcw 16/16 · integrity 112/112 · doublons 0/271 · coherence 55/0/0 PASS STRICT · sweep 9 citations recalées en 1 round] · D009 sync [pipeline rc=0 ×2 passes 54/54, 0 divergence, rescelage task21-f2 ×2 byte-stable, archive véhicule v2.2] · D010 clôture [E8 final 10/10, horodatages couplés 2026-11-08T18:05:00Z, commit dédié SANS mode-purs]) — Horodatage vérifié : 2026-11-08T18:05:00Z

