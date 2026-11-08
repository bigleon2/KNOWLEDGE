# Plan Task 80 — Suite de tests fonctionnels + performance + interactions intégrée au skill re-curation (v1.2.0) — réinstallation locale préalable exécutée

**Horodatage plan : 2026-11-08T20:06:49Z (INITIAL)** · Mode : gen-plan (step, chaîne autonome — enchaînement des groupes sans portes, correct-work(groupe) après chaque groupe, max 2 rounds) · Session : web-ecef7f80 · Trace directive : 1a1bcb98c022bfe9 (précisions antérieures 1a1bcb6b140f94ad — « réinstalle mon écosystème localement, puis lorsqu'il sera réinstallé alors génère (en utilisant mon skill "gen-plan" fraîchement installé en mode STEP), puis exécute le plan d'actions ») · Prérequis exécuté : **réinstallation locale FAITE** (eco_install_pipeline.py rc=0 ×2 — 54/54 SHA-256, 0 divergence, garde R2 « 0 rétrogradation », archive rescellée round-trip v2.2, integrity 112/112 PASS).

## Contexte et périmètre

Directive propriétaire (2026-11-09, trace 1a1bcb98c022bfe9), verbatim :

> « Dans l'objectif d'optimiser de façon cohérente, optimisée et fonctionnelle le fonctionnement et les performances de mon écosystème final et de garantir son idempotence : avant d'appliquer la "re-curation progressive disclosure" à l'élément ciblé, fais-lui passer des tests fonctionnels et de performance. Ces tests doivent impérativement inclure la validation de toutes les interactions de l'élément ciblé avec les autres composants auxquels il est lié. Effectue ces tests rigoureusement avant et après la "re-curation progressive disclosure" pour garantir la livraison d'un écosystème cohérent, optimisé et fonctionnel, parfaitement idempotent par rapport à sa version précédente. Intégrer cette suite de tests au sein de mon skill "re-curation" de façon cohérente, optimisée et fonctionnelle, tout en respectant scrupuleusement l'ensemble des règles et des protocoles d'architecture de mon écosystème global. »

Interprétation (règle d'or n°5, dérivée du disque) :
- **L'action explicite de la directive = « Intégrer cette suite de tests au sein de mon skill "re-curation" »** : le livrable est le skill re-curation v1.2.0 porteur de la suite. La re-curation d'un élément ciblé (prochaine cible : iphone19, n°2 de la file Task 72 G3) est la TÂCHE SUIVANTE — elle consommera la suite (PRE → re-curation → POST) ; la directive exige que la suite EXISTE AVANT toute application (« avant d'appliquer… fais-lui passer des tests »).
- **Trois familles exigées, absentes du harnais v1.1.0** (diagnostic mesuré) : (1) **tests fonctionnels** — v1.1.0 ne teste que la structure (contrats sha256, pointeurs, non-duplication), jamais l'EXÉCUTION des fonctionnalités de l'élément ; (2) **tests de performance** — v1.1.0 mesure le poids (octets/#token) mais aucune durée d'exécution, aucune stabilité PRE/POST ; (3) **validation de TOUTES les interactions** — v1.1.0 détecte la gouvernance (KB/ECO_SKILLS) sans JAMAIS valider les arêtes (dépendances sortantes/entrantes, contrats semver, alignement registre, corpus PM, agents).
- **PRE et POST rigoureux** : les familles s'intègrent aux verdicts existants — PRE : GO/NO-GO étendu (jamais de re-curation sur un élément déjà cassé : fonctionnels FAIL ou interactions CASSÉES → NO-GO) ; POST : MAINTIEN DE L'OPTIMISATION / DÉRIVE étendu aux 5 dimensions (cohérent + fonctionnel + optimisé + interactions saines + perf stable) — « parfaitement idempotent par rapport à sa version précédente » = contrats identiques + comportement exécutable identique + arêtes identiques + poids sous seuil.
- **Respect scrupuleux de l'architecture** : re-curation = élément KB + ECO_SKILLS → **cascade légère obligatoire** (KB + pin arbitre integrity + historique par-skill + ULTRA + arbitres + sync hôte↔dépôt même passe) ; R4 jamais dupliquer (une seule machinerie baseline/verdict dans le script principal — pas de script redondant) ; N3 Python stdlib ; semver MINOR (nouvelle capacité, rétro-compatible) ; description frontmatter évolutive ADDITIVE (phrases de déclenchement existantes conservées verbatim — non-régression triggers, précédent v1.1.0).

## État initial mesuré (E1-RES + E2, règle d'or n°5)

- **E1-RES (hook, complet)** : (1) B-11 lecture préalable — worklog.md 499 990 o (dernier suite 71 : Task 79 G5 CLOSE), plans Task 72-79 clôturés, **aucun plan en vol** ; (2) G-RES **OK** (monitor.py — tous niveaux 0) ; (3) fraîcheur : aucun plan en exécution ; (4) garde post-coupure : réinstallation exécutée à l'ouverture (54/54), **version-management DISPARU inter-tours** (récidive — volatilité plateforme documentée Task 56/72/75/79) → **rétablissement immédiat : eco_install_pipeline rc=0 (54/54, 0 divergence) — integrity 112/112 PASS, manifeste écrit**.
- **Corpus (réinstallé, certifié)** : SHARED v1.7.36 · GEN-PLAN v3.41.0 · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1 · INSTALL v1.9.13 · README v2.1.21 · SYNC-CONTEXT **v1.5.7** (lag inerte RÉSORBÉ — pendances Task 79 éteintes au commit 54090b4) · re-curation **v1.1.0** (KB ligne 57 + ECO_SKILLS integrity ligne 77 — correctif comparateur §0 harnais v3 livré Task 79).
- **Harnais v1.1.0 cartographié** (485 lignes, 24 472 o) : contrats sha256 (§A borné, §0 bloc socle normalisé [étiquette SHARED + dates], read_when, evals, description) + poids (octets/Kio/#token) + pointeurs references/ + non-duplication 1024 o + --compare (registre 4 méthodes, R4-compliantes seules éligibles) + selftest 7 cas (7/7 ×2) — **sans** les 3 familles de la directive.
- **Baselines STALE (pendance consignée 54090b4)** : download/protocole-test-gen-plan.json + protocole-test-version-management.json générés par **v1.0.0** (convention de mesure §0 v3 : non comparables — à re-capturer).
- **Git dépôt** : HEAD `54090b4` (pendances Task 79 CLOSE, post-push) · **avance 1 commit sur origin/main** (0b1712b poussé) · arbre propre (0 mode-pur résiduel — Task 79 CLOSE).
- **Cible suivante** (file priorisée Task 72 G3) : iphone19 (n°2 — version-management n°1 traitée Task 79 G2, 46,1→25,2 Kio −45,4 %).
- **Arbitre interactions global existant** : scripts/test-coherence-interactions.py (616 lignes, 11 sections, verdict 55/55 STRICT Task 79) — périmètre GLOBAL inter-fichiers ; la suite re-curation implémente la vue SCOPÉE par élément (baseline + comparaison PRE/POST) — complémentaire, pas duplication (R4 : la machinerie baseline/verdict n'existe que dans protocole-test.py).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Ouverture saine : écosystème réinstallé localement (eco_install_pipeline rc=0 ×2, 54/54 SHA-256, 0 divergence, garde R2 0 rétrogradation, archive round-trip v2.2) · version-management rétabli après disparition inter-tours · integrity 112/112 PASS · G-RES OK"
    verification: "python3 scripts/eco_install_pipeline.py (rc=0, divergences==[]) && python3 scripts/check-ecosysteme-integrity.py (112/112) && monitor.py (OK) — traces 2026-11-08T20:0xZ"
    source: "Directive 1a1bcb6b140f94ad (réinstaller d'abord) ; règle d'or n°9 ; garde É1-INSTALL v3.35.2"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "État initial mesuré : harnais v1.1.0 sans les 3 familles de la directive (fonctionnels/performance/interactions) · baselines gen-plan + version-management STALE v1.0.0 (convention §0 v3) · git avance 1 (54090b4) · file Task 72 : iphone19 prochaine cible · SKILL.md re-curation 12 096 o / protocole-test.py 24 472 o"
    verification: "rg -c 'tests_fonctionnels|interactions' skills/re-curation/scripts/protocole-test.py (=0 avant G1) && python3 -c json genere_par v1.0.0 ×2 && git -C KNOWLEDGE-repo rev-list origin/main..HEAD --count (=1)"
    source: "Directive 1a1bcb98c022bfe9 ; KO-L003 ; file priorisée Task 72 G3"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "G1 — Suite construite dans le SCRIPT PRINCIPAL protocole-test.py (v1.2.0, une seule machinerie baseline/verdict — R4) : famille FONCTIONNELS (selftest de chaque script de l'élément détecté dans le source puis exécuté, timeout 60 s, capture rc + durée ; py_compile pour les scripts sans selftest ; evals JSON valides ; structure frontmatter minimale — nature-adapté) + famille PERFORMANCE (poids octets/Kio/#token [goulot réel Task 70] + durée MESURÉE des tests fonctionnels + fonction pure perf_stable[durée_base, durée_post] tolérance ×1.5 + 0.5 s) + famille INTERACTIONS (sortantes : chaque dépendance frontmatter existe + contrat semver satisfait ; entrantes : scan des frontmatters du registre KB → dépendants de l'élément + contrats satisfaits ; alignement entrée KB == version frontmatter ; ECO_SKILLS arbitre integrity == version ; corpus PM si famille (sinon nature non-famille documentée) ; agents .agent mentionnant l'élément ; empreinte sha256 de l'ensemble normalisé)"
    verification: "rg -c 'def tests_fonctionnels|def tests_performance|def tests_interactions|def perf_stable' skills/re-curation/scripts/protocole-test.py (>=4) && python3 skills/re-curation/scripts/protocole-test.py --selftest (PASS)"
    source: "Directive (3 familles + toutes les interactions) ; re-curation §1 (script principal) ; R4 ; N3 stdlib ; règle d'or n°5 (mesuré)"
    priority: "S1"
    status: "pending"
  - id: "D004"
    criterion: "G1 — Verdicts étendus : PRE GO/NO-GO (GO = contrats lisibles ET fonctionnels PASS ET interactions SAINES — jamais de re-curation sur un élément déjà cassé) ; POST MAINTIEN DE L'OPTIMISATION / DÉRIVE sur 5 dimensions (cohérent + fonctionnel + optimisé + interactions_saines + perf_stable) ; JSON protocole enrichi (familles, métriques, empreintes, tolérances documentées) ; --verifier étendu aux 3 familles en direct (sans exiger de PRE antérieur)"
    verification: "python3 skills/re-curation/scripts/protocole-test.py --pre <temoin-réel> (JSON contient tests.fonctionnels/performance/interactions + verdict) && --post (5 dimensions dans post)"
    source: "Directive (« Effectue ces tests rigoureusement avant et après » + « parfaitement idempotent ») ; méthode P0/P5 §2"
    priority: "S1"
    status: "pending"
  - id: "D005"
    criterion: "G1 — Selftest étendu 7 → 12 cas en bac à sable (tmp, sait échouer) : +selftest du script témoin exécuté PASS · +interactions saines → empreinte + SAINES → GO · +dépendance sortante cassée → interactions CASSÉES → NO-GO · +contrat entrant violé → CASSÉES → DÉRIVE · +perf_stable unitaire (1.0/1.4 → True ; 1.0/2.5 → False) — 12/12 ×2 idempotent (re-jeu no-op)"
    verification: "python3 skills/re-curation/scripts/protocole-test.py --selftest ×2 (12/12 PASS ×2, sorties identiques)"
    source: "Directive (garantir idempotence) ; harnais v3 selftest 7/7 ×2 précédent ; R6"
    priority: "S1"
    status: "pending"
  - id: "D006"
    criterion: "G2 — SKILL.md re-curation v1.2.0 : description frontmatter ADDITIVE (phrases de déclenchement existantes conservées verbatim + mention suite fonctionnels/performance/interactions) · read_when + §A enrichis (déclencheurs directive) · §2 P0/P5 enrichis des 3 familles · §3 protocole adapté documenté pour les 3 familles · §5 journal v1.2.0 (directive tracée 1a1bcb98c022bfe9) · taille < 30 Kio (seuil LOURD)"
    verification: "rg -c 'v1.2.0' skills/re-curation/SKILL.md (>=1) && wc -c skills/re-curation/SKILL.md (<30720) && diff description = additif seul (phrases existantes intactes)"
    source: "Directive (« intégrer au sein de mon skill re-curation ») ; non-régression triggers v1.1.0 ; semver MINOR"
    priority: "S1"
    status: "pending"
  - id: "D007"
    criterion: "G2 — Cascade légère (gouvernance KB + ECO_SKILLS) : entrée KB ## re-curation v1.2.0 + pin arbitre integrity ECO_SKILLS re-curation 1.2.0 (KO-L004) + historiques-par-skill/re-curation.md entrée v1.2.0 + ULTRA régénéré + arbitres 5/5 en un bloc (verify-cross · vcw 16/16 · integrity 112/112 · doublons 0 · interactions STRICT) + archive rescellée round-trip v2.2"
    verification: "grep '## re-curation v1.2.0' skills/KNOWLEDGE.md && python3 scripts/check-ecosysteme-integrity.py (112/112) && 5 arbitres rc=0"
    source: "re-curation §2 règle 4 (gouvernance) ; KO-L004 ; précédent Task 79 (cascade légère vm)"
    priority: "S1"
    status: "pending"
  - id: "D008"
    criterion: "G3 — Preuve réelle de la suite : --pre iphone19 (prochaine cible file Task 72 — 4 scripts + evals, nature riche) → GO avec les 3 familles dans la baseline · re-capture des baselines STALE (gen-plan + version-management — convention §0 v3) · replay identité --post re-curation (la suite se prouve sur SON PROPRE skill : contrats + selftests + interactions → MAINTIEN attendu)"
    verification: "python3 .../protocole-test.py --pre iphone19 (GO, JSON 3 familles) && --pre gen-plan && --pre version-management (genere_par v1.2.0) && --post re-curation (MAINTIEN DE L'OPTIMISATION)"
    source: "Directive (avant d'appliquer à l'élément ciblé — la baseline doit exister) ; pendance 54090b4 (baselines à re-capturer)"
    priority: "S1"
    status: "pending"
  - id: "D009"
    criterion: "G3 — Projection + sync miroir MÊME PASSE + commit local : édition dans le DÉPÔT (source de vérité R4) puis eco_install_pipeline rc=0 (54/54, 0 divergence, version-management PRÉSENT à l'hôte en fin de passe — anti-disparition) · commit local Task 80 (message détaillé) · **PUSH = propriétaire uniquement** (règle d'or n°4 — KO-L009 : PAT exposé 4×, E15 Task 79 a recommandé révocation/rotation ; l'agent ne pousse pas)"
    verification: "python3 scripts/eco_install_pipeline.py (rc=0, divergences==[]) && ls skills/version-management/SKILL.md && git -C KNOWLEDGE-repo log --oneline -1 (commit Task 80) && git status (propre)"
    source: "Règle d'or n°4/5 ; KO-L009 ; contrainte miroir file Task 72 ; précédents Task 63/77/79"
    priority: "S1"
    status: "pending"
  - id: "D010"
    criterion: "G3 — Clôture conforme : correct-work (projet) --bloc (B1 installation+certification · B2 corpus+KB+outillage · B3 livrables session 80 · B4 bloc extension) verdict agrégé PASS · clone-chat session 80 scellé (§0-§5, 0 secret) · E8 final answer key 10/10 verified horodatages couplés · check_plan_protocol P1-P5 PASS · fenêtre native maintenue G1→G3 · bilan chiffré"
    verification: "verdict CW --bloc consigné worklog && ls download/clone-chat-session-web-ecef7f80-20261109-task80.md && answer key 10/10 + horodatage final couplé"
    source: "Mode step §5.5 ; E7-DISP ; précédents Task 76-79"
    priority: "S2"
    status: "pending"
```

## Estimation et profil (E3-E6)

- **E3** : Type 2 (développement scripts Python N3 + livrables documentaires MD/JSON — aucun docx/pdf/xlsx/pptx).
- **E4** : G1 ≈ 10 000 (code ~250 lignes + selftests ×2) · G2 ≈ 5 000 · G3 ≈ 9 000 (preuves 2 500 + CW --bloc 4 000 + clone-chat/E8 2 500) — **total ≈ 24 000 #token** (bornes 18 000-32 000).
- **E5-POIDS** : gen-plan 29,9 Kio INTERMÉDIAIRE (lecture ciblée FAITE — §A/§0/§1.2bis/§1.5/§5.5/§5.6 uniquement) · re-curation 11,8 Kio (intégrale légitime — cible de la tâche) · protocole-test.py 23,9 Kio (intégrale — cible) · correct-work 28,6 Kio INTERMÉDIAIRE (contrat --bloc connu des précédents).
- **E6** : NORMAL (G-RES OK — PARALLELE).

## G1 — Construction de la suite dans protocole-test.py (v1.2.0) `[À FAIRE]` (0/4)

- **SG1.1 Familles FONCTIONNELS + PERFORMANCE** (D003) : T1.1.1 `tests_fonctionnels()` — détection du flag --selftest dans le source de chaque script de l'élément puis exécution réelle (subprocess, timeout 60 s, rc + durée capturés), py_compile pour les sans-selftest, evals JSON, structure frontmatter · T1.1.2 `tests_performance()` — poids (octets/Kio/#token, goulot réel Task 70) + durée MESURÉE des tests fonctionnels + `perf_stable()` fonction pure (tolérance ×1.5 + 0.5 s documentée dans le JSON).
- **SG1.2 Famille INTERACTIONS** (D003) : T1.2.1 sortantes (parse dependencies frontmatter → existence + contrat semver) + entrantes (scan frontmatters des entrées du registre KB → dépendants + contrats satisfaits — version élément ≥ min exigée) · T1.2.2 alignement KB (entrée `## <nom> v<x>` == frontmatter) + ECO_SKILLS (pin arbitre integrity == version) + corpus PM si famille + agents .agent mentionnant l'élément + empreinte sha256 normalisée → verdict SAINES/CASSÉES.
- **SG1.3 Intégration verdicts + JSON** (D004) : T1.3.1 `cmd_pre` étendu — GO exige fonctionnels PASS + interactions SAINES (NO-GO sinon : jamais de re-curation d'un élément déjà cassé) · T1.3.2 `cmd_post` étendu — 5 dimensions (cohérent + fonctionnel + optimisé + interactions_saines + perf_stable) → MAINTIEN/DÉRIVE ; JSON enrichi (nature + protocole 3 familles + métriques + empreintes) ; `--verifier` étendu aux 3 familles en direct.
- **SG1.4 Selftest étendu** (D005) : T1.4.1 fixture bac à sable enrichie (script témoin avec --selftest + dépendance sortante + dépendant entrant + entrée KB témoin) + 5 nouveaux cas (12 total : selftest exécuté · interactions saines → GO · sortante cassée → NO-GO · entrante violée → DÉRIVE · perf_stable unitaire) · T1.4.2 re-jeu ×2 idempotent (12/12 ×2).

## G2 — SKILL.md v1.2.0 + cascade légère (gouvernance KB + ECO_SKILLS) `[À FAIRE]` (0/3)

- **SG2.1 SKILL.md re-curation v1.2.0** (D006) : T2.1.1 description ADDITIVE (phrases existantes verbatim + suite v1.2.0 : fonctionnels/performance/interactions) + read_when + §A (déclencheurs « tests fonctionnels et de performance » / « validation de toutes les interactions ») · T2.1.2 §1 mission enrichie (directive 1a1bcb98c022bfe9) + §2 P0/P5 (3 familles dans les verdicts) + §3 protocole adapté (3 familles documentées) + §5 journal v1.2.0 — < 30 Kio.
- **SG2.2 Gouvernance** (D007) : T2.2.1 KB `## re-curation v1.2.0` (+ note calibration) · T2.2.2 arbitre integrity ECO_SKILLS re-curation → 1.2.0 (KO-L004, commentaire directive) · T2.2.3 historiques-par-skill/re-curation.md entrée v1.2.0 + ULTRA régénéré (gen-ultra-maitre.py).
- **SG2.3 Certification un bloc** (D007) : T2.3.1 arbitres 5/5 PAR (verify-cross 100 % · vcw 16/16 · integrity 112/112 · doublons 0 · interactions STRICT) · T2.3.2 archive rescellée round-trip v2.2 (task21-f2-rebuild-archive.py).

## G3 — Preuves réelles + projection + clôture `[À FAIRE]` (0/3)

- **SG3.1 Preuves réelles de la suite** (D008) : T3.1.1 `--pre iphone19` (prochaine cible file Task 72 — nature riche : scripts + evals + §A + §0) → GO attendu (baseline 3 familles complète) · T3.1.2 re-capture baselines STALE : `--pre gen-plan` + `--pre version-management` (genere_par v1.2.0 — pendance 54090b4 éteinte) · T3.1.3 replay identité `--post re-curation` (la suite se prouve sur son propre skill : contrats + selftests des 3 scripts + interactions → MAINTIEN DE L'OPTIMISATION attendu).
- **SG3.2 Projection + commit** (D009) : T3.2.1 édité dans le DÉPÔT puis eco_install_pipeline rc=0 (54/54 — contrainte miroir même passe, version-management présent en fin de passe) · T3.2.2 commit local Task 80 (message détaillé : directive, 3 familles, selftest 12/12, cascade légère, preuves) — **PUSH = propriétaire** (KO-L009, E15 Task 79 : révocation/rotation PAT recommandée).
- **SG3.3 Clôture** (D010) : T3.3.1 correct-work (projet) --bloc B1-B4 (max 2 rounds/bloc, agrégation pire-des-verdicts) · T3.3.2 clone-chat session 80 + E8 final (answer key 10/10 verified, horodatages couplés) + check_plan_protocol P1-P5 + bilan chiffré + fenêtre native close.

## PLAN-AFFICHE

(Task 80 — download/plan-task80-suite-tests-recuration-v120.md — INITIAL — **G1 construction suite `[À FAIRE]` 0/4 · G2 SKILL.md v1.2.0 + cascade légère `[À FAIRE]` 0/3 · G3 preuves + projection + clôture `[À FAIRE]` 0/3** — answer key 10 décisions (D001-D002 verified ouverture · D003-D010 pending exécution) — E8 initial PASS 2026-11-08T20:06:49Z — #token ≈ 24 000 (bornes 18 000-32 000) — exécution step : G1→G3 chaîne autonome (série justifiée ENTRE groupes : écritures chaînées code → gouvernance → preuves), vagues PAR internes (selftests ×2, arbitres un bloc, preuves indépendantes) — fenêtre native TodoWrite : affichée au début d'exécution, mise à jour à chaque fin de groupe (E7-DISP point 6) — PUSH final = propriétaire, jamais l'agent)

Verdict E8 : PASS INITIAL (10/10 décisions bien formées — criterion/verification/source/priority/status présents, S1/S2 à vérifications exécutables ; D001-D002 verified sur traces disque ; D003-D010 pending — exécution step autonome) — Horodatage : 2026-11-08T20:06:49Z
