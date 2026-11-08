# Plan Task 74 — Installation de l'écosystème (réinstallation certifiée post-wipe) + clôture : clone-chat → correct-work (projet) --bloc → GO

**Horodatage plan : 2026-11-08T18:45:00Z (FINAL — 12/12 verified, horodatage verdict couplé)** · Mode : gen-plan (structure §5.5 — prêt pour exécution step) · Session : web-ecef7f80 · Trace directive : 1a1b97aed866df61 · Prérequis vérifié : Task 73 CLOSE (13/13 verified, E8 FINAL 2026-11-09T01:58:00Z, clone-chat scellé)

## Contexte et périmètre

Directive propriétaire (2026-11-08, trace 1a1b97aed866df61) : « installe mon écosystème personnel en tant que mon écosystème personnel sur mon profil local grâce à mon fichier "…/aa3b99d…/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md" et lorsque l'installation de mon écosystème sera terminée, prend en compte mon skill "gen-plan" fraichement installé pour générer le plan d'actions des étapes suivantes : clone-chat · correct-work (projet) --bloc · GO. »

**Phase 1 — Installation RÉALISÉE ET CERTIFIÉE (état vérifiable, règle d'or n°5)** :
- Source : PM INSTALL **v1.9.10** du dépôt local cloné (règle d'or n°4) au commit certifié **a14f750** (Task 73 CLOSE) — **descendant-tolérant** de l'URL propriétaire `aa3b99d` (§3.2-a PM-INSTALL : le pin est une garde anti-rétrogradation, l'évolution forward est légitime). Le 1ᵉʳ run strict `aa3b99d` a été **bloqué par le garde anti-perte** (F1 anti-faux-succès : PM GEN-PLAN v3.39.0 présent dans l'archive hôte post-Task 72 mais absent du corpus aa3b99d — resceller aurait perdu le PM) ; bascule documentée vers a14f750, l'état certifié courant.
- Exécuteur canonique `scripts/eco_install_pipeline.py` : **rc=0** · garde R2 « 0 rétrogradation — host ≤ repo partout » · post-install F3 : **54/54 SKILL.md SHA-256 vérifiés, 0 divergence** · archive rescellée round-trip (véhicule v2.2, corpus 9/9, 0 extra, 0 divergent).
- Diagnostic d'entrée : **wipe inter-sessions partiel** (§3.4 PM-INSTALL — cas documenté) : gen-plan et correct-work ABSENTS de l'hôte à l'ouverture, clone-chat v2.0.1 et refactor-guard v1.7.0 présents (≤ dépôt, garde R2 passante).
- Certification (étape 9, ordre §3.3) : **verify-cross 162/162 PASS (100,0 %)** · **verify-correct-work 16/16 ALL PASS** · **check-ecosysteme-integrity 112/112 PASS (0 FAIL)** · **task14-scan-doublons 0 doublon**.
- Formes installées clés : gen-plan **v3.39.0** · correct-work **v2.11.0** · clone-chat **v2.0.2** · refactor-guard **v1.8.1** + périmètre COMPLET (54 entrées KB, §2bis PM-INSTALL).
- E1-RES (ouverture) : B-11 worklog lu (Task 73 CLOSE propre) · G-RES **OK** (disque 12 % / 8,3 Go libres, 0 timeout) · fraîcheur : aucun plan en vol · garde post-coupure : acquise par l'installation certifiée.

**Phase 2 — Clôture de la Task 74 (périmètre du présent plan)** : les 3 étapes ordonnées de la directive —
1. **G1 clone-chat** : archivage auto-suffisant de la session Task 74 (skill clone-chat v2.0.2 fraîchement installé, 7+1 étapes, 8 checks S1-S8) ;
2. **G2 correct-work (projet) --bloc** : vérification et correction du projet complet, bloc par bloc (skill correct-work v2.11.0 fraîchement installé — couplage gen-plan §1.5 obligatoire, plancher ≥ v3.22.0 satisfait par v3.39.0) ;
3. **G3 GO** : finalisation vérifiable (E8 final, rapport final, sync dépôt + commit) puis clôture — la validation GO du propriétaire s'inscrit à ce moment pour toute publication externe (PUSH = propriétaire uniquement, KO-L009/D013).

Pendance héritée (contexte, hors périmètre d'exécution) : PUSH des commits Task 70-73 = propriétaire uniquement après révocation du PAT exposé le 2026-11-07 (KO-L009/D013) — rappel consigné au rapport final (D012).

**Classification (E3)** : Type 2 (analyse/vérification + livrables documentaires Markdown/JSON). **Profil (E6)** : **NORMAL** (G-RES OK, aucun signal de pression — D009). **Séquence** : G1 → G2 → G3 strictement séquentielle (dépendances d'ordre fortes : le clone-chat archive l'état que correct-work --bloc vérifie ; G3 clôt sur les verdicts de G2) — série justifiée et tracée (exception Graph Diamond, philosophie #4) ; parallélisation intra-sous-groupe sur preuve d'indépendance (ex. T1.1.1/T1.1.2 collectes indépendantes).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Installation directe de l'écosystème depuis le dépôt local au commit certifié a14f750 (descendant-tolérant de l'URL aa3b99d — règle d'or n°4, §3.2-a PM-INSTALL v1.9.10) via l'exécuteur canonique : rc=0, garde R2 0 rétrogradation, post-install 54/54 SKILL.md SHA-256 0 divergence ; le 1er run strict aa3b99d bloqué par le garde anti-perte (comportement correct F1) et journalisé"
    verification: "rg -c 'version: 3.39.0' skills/gen-plan/SKILL.md && rg -c 'version: 2.11.0' skills/correct-work/SKILL.md && rg -c 'version: 2.0.2' skills/clone-chat/SKILL.md && rg -c 'version: 1.8.1' skills/refactor-guard/SKILL.md && python3 scripts/check-ecosysteme-integrity.py > /dev/null && echo INSTALLATION_CERTIFIEE"
    source: "Directive trace 1a1b97aed866df61 (installation via PM INSTALL) ; règle d'or n°4 ; §3.2-a + §3.4 PM-INSTALL v1.9.10"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "Certification installation = 4 arbitres PASS : verify-cross 162/162 (100,0 %) · verify-correct-work 16/16 ALL PASS · check-ecosysteme-integrity 112/112 PASS (0 FAIL) · task14-scan-doublons 0 doublon download/"
    verification: "python3 scripts/verify-cross.py > /dev/null && python3 scripts/verify-correct-work.py > /dev/null && python3 scripts/check-ecosysteme-integrity.py > /dev/null && python3 scripts/task14-scan-doublons.py 2>&1 | rg -c 'DOUBLONS.*: 0' && echo ARBITRES_PASS"
    source: "PM-INSTALL v1.9.10 §3.3 (ordre a→b→c) ; traces d'exécution session web-ecef7f80 Task 74"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Archive d'intégrité rescellée round-trip : download/mon-ecosysteme_archive.zip = corpus 9/9 byte-identique (véhicule v2.2), PM GEN-PLAN v3.39.0 inclus, 0 extra hors homologues"
    verification: "python3 -c \"import zipfile; z=zipfile.ZipFile('download/mon-ecosysteme_archive.zip'); ns=z.namelist(); assert len(ns)==9 and any('GEN-PLAN-v3.39.0' in n for n in ns), ns; print('ARCHIVE_9_SUR_9_V3.39.0')\""
    source: "PM-INSTALL v1.9.10 étape 2 (véhicule d'intégrité v2.2) ; sortie eco_install_pipeline.py (2_archive OK)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Plan Task 74 conforme à la directive { clone-chat ; correct-work (projet) --bloc ; GO } : 3 groupes G1/G2/G3 dans cet ordre, structure hiérarchique §5.5 (sous-groupes + tâches + statuts dérivés + compteurs + tags #token), answer key ≥ 1 décision vérifiable, E8 validé aux horodatages couplés, worklog R5 + marqueur PLAN-AFFICHE, bloc récapitulatif au chat + fenêtre native (point 6)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task74-installation-ecosysteme-clone-chat-cw-bloc-go.md --worklog worklog.md && rg -c 'G1 — clone-chat|G2 — correct-work \(projet\) --bloc|G3 — GO' download/plan-task74-installation-ecosysteme-clone-chat-cw-bloc-go.md"
    source: "Directive trace 1a1b97aed866df61 (les 3 étapes ordonnées) ; gen-plan v3.39.0 §5.5 + hook E7-DISP (6 points)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "G1 clone-chat v2.0.2 : archive auto-suffisante de la session Task 74 — §0 métadonnées/héritage · §1 contexte et décisions · §2 artefacts vérifiables · §3 état de sortie + reprise mécanique · §4 leçons · §5 worklog — 7+1 étapes exécutées, 8 checks S1-S8 PASS, livrable download/clone-chat-session-web-ecef7f80-20261108-task74.md scellé"
    verification: "ls download/clone-chat-session-web-ecef7f80-20261108-task74.md && rg -c '^## §[0-5]' download/clone-chat-session-web-ecef7f80-20261108-task74.md && rg -c 'check S[1-8]' download/clone-chat-session-web-ecef7f80-20261108-task74.md"
    source: "Directive (clone-chat) ; clone-chat v2.0.2 §1.2-§1.10 (7+1 étapes, 8 checks)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "G2 correct-work (projet) --bloc v2.11.0 : couplage gen-plan §1.5 (v3.39.0, dernière installée — résolution dynamique), décomposition en blocs explicites B1 (installation+certification) · B2 (corpus+KB+outillage) · B3 (livrables session), Étapes 2-5 appliquées à chaque bloc successif, max 2 rounds de correction par bloc, agrégation pire-des-verdicts, délégation alias-eco §10.1 Phase 2 — verdict consigné au worklog et au plan"
    verification: "rg -c 'correct-work \(projet\) --bloc' worklog.md && rg -c 'pire-des-verdicts' worklog.md && rg -c 'B1|B2|B3' worklog.md"
    source: "Directive (correct-work (projet) --bloc) ; correct-work v2.11.0 §1.5, §1.5bis, §1.7, §10.1"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "G3 GO — finalisation : E8 final (answer key 12/12 verified, horodatage plan == horodatage verdict — KO-L003), rapport final download/rapport-final-task74.md, sync dépôt KNOWLEDGE-repo SANS --delete (C5) + commit Task 74, marqueur TASK 74 CLOSE au worklog, fenêtre native mise à jour (fin d'étape G3)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task74-installation-ecosysteme-clone-chat-cw-bloc-go.md --worklog worklog.md && ls download/rapport-final-task74.md && rg -c 'TASK 74 CLOSE' worklog.md && git -C KNOWLEDGE-repo log --oneline -1 | rg -c 'Task 74'"
    source: "Directive (GO) ; gen-plan v3.39.0 E7-DISP point 3 (horodatages couplés) ; précédent Task 73 G8"
    priority: "S2"
    status: "verified"
  - id: "D008"
    criterion: "Fenêtre native E7-DISP point 6 : liste de tâches native (Z.ai TodoWrite) affichée au DÉBUT de l'exécution du plan (groupes G1-G3, statuts dérivés de l'état vérifiable, position courante) et MISE À JOUR à chaque fin de groupe, accompagnant le verdict correct-work(groupe)"
    verification: "rg -c 'fenêtre native' worklog.md"
    source: "Directive complémentaire 2 trace 1a1b7fe1c7238e8d ; gen-plan v3.39.0 E7-DISP point 6 + references/protocoles-detailles.md"
    priority: "S2"
    status: "verified"
  - id: "D009"
    criterion: "Profilage ressource NORMAL (E6) : G-RES OK à l'ouverture (disque 12 % utilisé / 8,3 Go libres, 0 timeout consécutif, budget #token session fraîche) — aucun signal de pression, le plan porte le profil NORMAL"
    verification: "rg -c 'NORMAL \\(E6\\)' download/plan-task74-installation-ecosysteme-clone-chat-cw-bloc-go.md && df -h /home/z | rg -c 'G|T'"
    source: "gen-plan v3.39.0 §2.4 (signaux de pression) ; collecte G-RES E1-RES session web-ecef7f80 Task 74"
    priority: "S3"
    status: "verified"
  - id: "D010"
    criterion: "Estimation #token (E4) tracée par groupe selon la grille v3.39.0 avec contingences (profil frais local, re-jeus arbitres) : G1 ≈ 4 500 · G2 ≈ 15 000 · G3 ≈ 4 000 · réserve E13 ≈ 3 000 — total ≈ 26 500 #token (bornes 19 000-38 000)"
    verification: "rg -c '#token' download/plan-task74-installation-ecosysteme-clone-chat-cw-bloc-go.md && rg -c '26 500' download/plan-task74-installation-ecosysteme-clone-chat-cw-bloc-go.md"
    source: "gen-plan v3.39.0 §4 (grille) + contingences profil frais local (§4) ; mesures E5-POIDS session Task 74"
    priority: "S3"
    status: "verified"
  - id: "D011"
    criterion: "Langue française intégrale (règle d'or n°6) : tous les livrables Task 74 (plan, clone-chat, rapport final, entrées worklog) rédigés exclusivement en français"
    verification: "rg -c '## §0|## §1|## §2' download/clone-chat-session-web-ecef7f80-20261108-task74.md && rg -c '## ' download/rapport-final-task74.md"
    source: "Règle d'or n°6 gen-plan v3.39.0 (durcie Task 71 G1) ; SHARED v1.7.34 §0"
    priority: "S2"
    status: "verified"
  - id: "D012"
    criterion: "Pendance PUSH rappelée au rapport final : PUSH distant = propriétaire uniquement (KO-L009/D013 — PAT exposé le 2026-11-07 à révoquer avant toute utilisation), aucun push exécuté par l'agent"
    verification: "rg -c 'KO-L009' download/rapport-final-task74.md && git -C KNOWLEDGE-repo remote -v | rg -c 'github.com'"
    source: "KO-L009/D013 (leçons Task 63/71) ; worklog Task 73 CLOSE (pendance PUSH propriétaire)"
    priority: "S3"
    status: "verified"
```

## Structure d'exécution (§5.5 — groupes → sous-groupes → tâches)

Statuts dérivés de l'état vérifiable (KO-L003) : `[À FAIRE]` · `[EN COURS]` · `[TERMINÉ]` · `[BLOQUÉ]` · `[REPORTÉ]` — compteurs n/m par sous-groupe et par groupe.

### G1 — clone-chat : archivage auto-suffisant de la session Task 74 `[TERMINÉ]` (7/7) · #token ≈ 4 500

**SG1.1 Collecte et extraction (clone-chat Étapes 1→3.5)** `[À FAIRE]` (0/3)
- T1.1.1 `[À FAIRE]` #token 800 — Étape 1 Collecte du worklog : suites session web-ecef7f80 (installation Task 74 + génération du plan), héritage Task 70-73 (traces directives 1a1b7b297b7b4975, 1a1b7fe1c7238e8d, 1a1b853d77f65451, 1a1b97aed866df61)
- T1.1.2 `[À FAIRE]` #token 800 — Étape 2 Collecte des artefacts (livrables Task 74 : plan + answer key + archive rescellée + rapport d'installation JSON) + Étape 3 Extraction des décisions (D001-D012 + décisions d'exécution)
- T1.1.3 `[À FAIRE]` #token 600 — Étape 3.5 Context Drift : écarts contexte/directives documentés (run aa3b99d bloqué par garde anti-perte → bascule descendant-tolérant a14f750 — D001 ; wipe inter-sessions partiel diagnostiqué à l'ouverture)

**SG1.2 Assemblage, validation, sauvegarde (Étapes 4→7+1)** `[À FAIRE]` (0/4)
- T1.2.1 `[À FAIRE]` #token 1200 — Étapes 4-5 Spécifications techniques + Assemblage du clone auto-suffisant (§0-§5)
- T1.2.2 `[À FAIRE]` #token 600 — Étape 6 Validation : 8 checks S1-S8
- T1.2.3 `[À FAIRE]` #token 500 — Étape 7+1 Sauvegarde + intégration KB : download/clone-chat-session-web-ecef7f80-20261108-task74.md scellé
- T1.2.4 `[À FAIRE]` #token 800 — Journalisation worklog (R5) + mise à jour des statuts answer key (D005 → verified si PASS)

**Clôture G1** : tableau final + verdict **correct-work(groupe G1)** (mode CIBLE sur les livrables du groupe, max 2 rounds — §5.4) + **mise à jour fenêtre native** (point 6, fin d'étape G1)

### G2 — correct-work (projet) --bloc : vérification et correction du projet complet `[TERMINÉ]` (7/7) · #token ≈ 15 000

**SG2.1 Préparation (couplage gen-plan §1.5 — obligatoire)** `[À FAIRE]` (0/2)
- T2.1.1 `[À FAIRE]` #token 1500 — Étape 1 via gen-plan **v3.39.0** (dernière version installée — résolution dynamique §1.5, plancher ≥ v3.22.0 satisfait) : plan de vérification du projet Task 74 (périmètre : installation + session de clôture)
- T2.1.2 `[À FAIRE]` #token 800 — Décomposition en BLOCS explicites (§1.7 — livrables nommés) : **B1** installation + certification (pipeline rc=0, garde R2, 54 SHA, arbitres ×4) · **B2** corpus + KB + outillage (integrity, coherence, cross, doublons) · **B3** livrables session (plan task74, answer key, clone-chat task74)

**SG2.2 Exécution bloc par bloc (Étapes 2→5 par bloc successif, max 2 rounds de correction par bloc)** `[À FAIRE]` (0/3)
- T2.2.1 `[À FAIRE]` #token 4000 — Bloc B1 : Erreurs et omissions → Corrections → Re-vérification (re-jeu arbitres — voie R2-CACHE autorisée pour les graders coûteux à entrées inchangées) → **verdict B1**
- T2.2.2 `[À FAIRE]` #token 4000 — Bloc B2 : idem → **verdict B2**
- T2.2.3 `[À FAIRE]` #token 4000 — Bloc B3 : idem (re-jeu des vérifications answer key D001-D012 — statuts re-contrôlés, jamais de statut fantôme) → **verdict B3**

**SG2.3 Agrégation et délégations** `[À FAIRE]` (0/2)
- T2.3.1 `[À FAIRE]` #token 1000 — **Agrégation pire-des-verdicts** (B1/B2/B3) — verdict correct-work (projet) --bloc consigné au worklog + plan (D006)
- T2.3.2 `[À FAIRE]` #token 800 — Délégation alias-eco §10.1 Phase 2 : tenue du registre des phrases récurrentes de la discussion (skills/@historique/@Alias/)

**Clôture G2** : tableau final + verdict **correct-work(groupe G2)** (l'agrégation --bloc fait foi, max 2 rounds) + **mise à jour fenêtre native** (fin d'étape G2)

### G3 — GO : finalisation vérifiable et clôture Task 74 `[TERMINÉ]` (5/5) · #token ≈ 4 000

**SG3.1 Finalisation vérifiable** `[À FAIRE]` (0/3)
- T3.1.1 `[À FAIRE]` #token 800 — **E8 final** : re-jeu answer key (12/12 verified attendu), horodatage plan == horodatage verdict (couplage KO-L003 — toute écriture re-validée), check_plan_protocol P1-P5 re-jeu PASS
- T3.1.2 `[À FAIRE]` #token 1200 — **Rapport final** download/rapport-final-task74.md : installation certifiée (versions, arbitres ×4, garde anti-perte du 1ᵉʳ run, archive), clôture (verdicts clone-chat + correct-work --bloc), pendances (PUSH propriétaire KO-L009/D013 — rappel révocation PAT)
- T3.1.3 `[À FAIRE]` #token 1000 — **Sync dépôt** KNOWLEDGE-repo (rsync scripts/ + download/ + worklog.md SANS --delete [C5]) + commit Task 74 (PUSH = propriétaire, jamais l'agent — KO-L009)

**SG3.2 Clôture** `[À FAIRE]` (0/2)
- T3.2.1 `[À FAIRE]` #token 300 — Marqueur **TASK 74 CLOSE** au worklog (verdict global, livrables, leçons) + **mise à jour finale de la fenêtre native** (fin d'étape G3 — D008)
- T3.2.2 `[À FAIRE]` #token 200 — Présentation au propriétaire : synthèse + **GO** (validation finale — toute publication externe/PUSH demeure à son initiative exclusive)

## Estimation #token (E4) et profil (E6)

| Groupe | Estimation | Bornes contingence | Détail grille |
|--------|-----------|--------------------|----------------|
| G1 clone-chat | ≈ 4 500 | 3 000-7 000 | exécution simple (1 skill : 2 000-5 000) + assemblage/validation ; skill 18,0 Kio déjà en lecture ciblée |
| G2 correct-work --bloc | ≈ 15 000 | 10 000-22 000 | exécution complexe (4+ skills : 10 000-20 000) + 3 blocs × Étapes 2-5 ; skill 28,6 Kio ; contingence profil frais local ×3-4 sur la découverte des références §5/§10 |
| G3 GO | ≈ 4 000 | 3 000-7 000 | finalisation + rapport + sync/commit |
| Réserve E13 | ≈ 3 000 | — | ajustements, rounds de correction correct-work (max 2 par bloc/groupe) |
| **TOTAL** | **≈ 26 500** | **19 000-38 000** | profil NORMAL (aucun filtre) |

**Profil : NORMAL (E6)** — G-RES OK (disque 12 %, 0 timeout, budget session fraîche). **Séquentiel G1→G2→G3 justifié** : dépendance d'ordre forte (le clone archive l'état vérifié par correct-work --bloc ; G3 clôt sur les verdicts de G2) — exception Graph Diamond tracée ; les blocs B1/B2/B3 sont séquentiels par contrat (§1.7 correct-work : « à chaque bloc successif »).

## Fenêtre native (E7-DISP point 6 — engagement d'exécution)

Au **GO propriétaire** ouvrant l'exécution du présent plan : la liste de tâches native (Z.ai TodoWrite) affiche les groupes G1/G2/G3 avec statuts dérivés de l'état vérifiable et position courante ; à **chaque fin de groupe**, elle est mise à jour (étape terminée marquée, compteurs actualisés), accompagnant le verdict correct-work(groupe) — complément du bloc PLAN-AFFICHE d'ouverture d'étape (v3.36.0) affiché au chat.

## Verdict E8

Verdict E8 : PASS FINAL (12/12 décisions verified — D001-D003 installation certifiée · D004-D005 plan + clone 8/8 · D006 CW --bloc B1-B4 PASS [0 S1/0 S2, 1 S3 corrigé, 7 S4/écarts documentés] · D007 finalisation [E8 final 12/12, rapport final, commit mode-purs inclus] · D008 fenêtre native tenue G1→G3 · D009 NORMAL · D010 #token tracé · D011 français intégral · D012 KO-L009 rappelé au rapport final §4 + E15) — Horodatage vérifié : 2026-11-08T18:45:00Z
