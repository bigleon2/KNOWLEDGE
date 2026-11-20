# Tâches restantes à faire — vue $FACON (cohérente, optimisée, fonctionnelle)

> Directive propriétaire trace `1a1f2096f9b3406d`, item b : « dis-moi $FACON les tâches restantes à faire » — $FACON = « de façon cohérente, optimisée et fonctionnelle » (registre @Alias, entrée D-105). Sources : relecture intégrale Task 108 G1 (153 suites + 21 clones), feuille de route §8 du rapport Task 105, findings CW Tasks 105-107, point d'état continue suite 153. Chaque tâche est ancrée dans sa source (cohérence), regroupée sans doublon (optimisation), et porte un critère d'extinction mécanique (fonctionnalité). Généré le 2026-11-19 · Task 108 G2.

## Vue priorisée (résumé chat)

| # | Tâche | Acteur | Priorité | État |
|---|---|---|---|---|
| 1 | Révoquer le PAT du tour Task 107 + fournir un PAT frais au prochain push | PROPRIÉTAIRE | **P1 — CRITIQUE** | ouvert |
| 2 | PUSH du commit Task 108 (nécessite le PAT frais) | PROPRIÉTAIRE→session | **P1** | **ÉTEINTE** (2026-11-19, Task 109 SUIVI — push f658e4c9 rc=0, 0 unpushed) |
| 3 | GO futur — correctif structurel F3 : injecteur propagate-context.py (gabarit périmé + 5 scripts protégés sans bloc CONTEXTE) | PROPRIÉTAIRE (GO) + session | **P2** | **ÉTEINTE** (2026-11-19, Task 110 G1 — injecteur v2.2.0 + durcissement, 5+2 scripts porteurs, 0 SyntaxError, certification 6/6) |
| 4 | GO futur — correctif structurel F2 : garde anti-perte du scelleur v2.3 (évolution légitime du corpus sans ECHEC transitoire) | PROPRIÉTAIRE (GO) + session | **P2** | **ÉTEINTE** (2026-11-19, Task 110 G2 — scelleur v2.4 discrimination PERTE/ÉVOLUTION git, harnais T1-T5 9/9, voie mécanique) |
| 5 | GO-3 (optionnel) : convention « docstring d'abord » (S3/F4) aux canons script-creator + correct-py | PROPRIÉTAIRE (GO) + session | **P3** | **ÉTEINTE** (2026-11-19, Task 110 G3 — canons v1.2.0 + cascade KO-L004, tool-routing N1 PASS inchangé) |
| 6 | Décision cron 531684 (3ᵉ dispositif perdu) : recréer ou entériner l'absence | PROPRIÉTAIRE | **P3** | escalade maintenue |
| 7 | Surveillance F3 au prochain bootstrap (si récidive : capture immédiate) | session (AUTO) | P3 | **ÉTEINTE** (2026-11-20, Task 111 — constat consigné : bootstrap du tour SAIN, injection v2.2.0 0 récidive) |
| 8 | PMs §0 : propagation automatique aux prochaines montées de version | AUTO (générateur KO-L004) | P3 | nominal |

Aucune autre pendance : re-curation ÉTEINTE (Task 85), différés Task 101 vérifiés éteints, familles/orchestrateurs tranchés (Task 106 : non-création), pendances PUSH antérieures toutes éteintes (Task 107 G0), G-RES OK (7,6 Go, profil NORMAL). **Mise à jour Task 110 (2026-11-19, trace 1a1f2297d90c957d « GO futur + GO-3 ») : tâches 3-4-5 ÉTEINTES — cf. détails ci-dessous. Mise à jour Task 111 (2026-11-20, trace 1a1f7d3e607663f1) : pendance PUSH du commit Task 110 (d4e228f4) ÉTEINTE — push a5daa964..d4e228f4 rc=0, atterrissage vérifié ls-remote anonyme (refs/heads/main = d4e228f4, parité HEAD = origin, E15 36ᵉ) ; tâche 7 ÉTEINTE (constat bootstrap consigné) ; cron list = 0 job (4ᵉ dispositif perdu — escalade tâche 6 maintenue).**

## Détail par tâche

### 1. Rotation/révocation du PAT GitHub — P1 CRITIQUE [PROPRIÉTAIRE]
- **Nature** : le jeton utilisé depuis la Task 63 a cumulé **33 expositions** (E15, suite 153). Le jeton du tour Task 107 doit être révoqué côté GitHub ; un PAT frais sera fourni par le propriétaire à tout tour nécessitant un push.
- **Mise à jour Task 109 (2026-11-19)** : une clé fraîche a été fournie et utilisée pour les pushes du tour (E15 34ᵉ/35ᵉ). L'ancien jeton (Task 107) reste à révoquer — le jeton précédent n'ayant jamais été stocké (KO-L009), la comparaison est impossible par construction ; la révocation de l'ANCIEN jeton demeure requise.
- **Source** : suite 153 point d'état (« rotation/révocation PAT [PROPRIÉTAIRE — CRITIQUE — 33 expositions cumulées, révoquer le jeton du tour après usage] ») ; leçons Task 98/101.
- **Critère d'extinction** : révocation effectuée côté GitHub + (si push requis) nouveau PAT fourni dans une directive — 0 trace écrite (KO-L009).

### 2. PUSH du commit Task 108 — P1 [PROPRIÉTAIRE→session] — **ÉTEINTE**
- **Nature** : le commit « Task 108 CLOSE » (créé en G5 ce tour) restera local — **aucun PAT n'a été fourni ce tour** (0 manipulation, 0 exposition). Pendance PUSH 1 commit.
- **Source** : présent tour (G5) ; leçon Task 98/101 (« push immédiat dès PAT frais disponible »).
- **Critère d'extinction** : `git ls-remote` anonyme → origin/main = HEAD dépôt ; `git rev-list --count origin/main..HEAD` = 0.
- **EXTINCTION (2026-11-19, Task 109 SUIVI, trace 1a1f223f6f3ecab9)** : push `19eb34b1..f658e4c9 HEAD → main` rc=0 avec la clé du tour (E15 34ᵉ) ; atterrissage vérifié ls-remote anonyme : refs/heads/main = f658e4c9, 0 unpushed, parité HEAD = origin/main ✓.

### 3. Correctif structurel F3 — injecteur propagate-context.py — P2 [GO propriétaire requis] — **ÉTEINTE**
- **Nature** : la branche « injection fraîche » de l'injecteur §0 porte un gabarit LITTÉRAL périmé (v1.7.39 — la dynamisation v2.1.1 ne couvre que la branche remplacement, classe F-70-2) et casse les scripts `from __future__`. 5 scripts (task98/101/102/104/106) ont été protégés par revert et **demeurent sans bloc CONTEXTE** (état certifié R2).
- **Source** : suite 153 (constat F3, S3) ; CW Task 107 finding F3.
- **Critère d'extinction** : propagation re-jeuée idempotente ×2 sur les 338 fichiers → 0 SyntaxError, 0 revert requis, les 5 scripts restaurés portent un bloc §0 v1.7.40 correct ; certification ALL PASS 6/6.
- **EXTINCTION (2026-11-19, Task 110 G1, GO trace 1a1f2297d90c957d)** : injecteur **v2.2.0** — dynamisation robuste re.sub (cause racine : clé figée `.replace("(SHARED v1.7.31)")` échouait silencieusement) + DRY + injection en lignes commentées APRÈS la docstring (canon GO-3, jamais de second littéral) + remplacement des 2 formes + durcissement mesuré en séance (scoping ast, garde tokenize, garde de parse — harnais 15/15 cas a-k) ; les 5 scripts portent le bloc §0 v1.7.40 ×2 arbres, 0 SyntaxError, 0 revert ; propagation idempotente ×2 (0/0/0) ; DÉCOUVERTES restaurées : task107-rejeu-answer-key.py (6ᵉ script orphelin) + task105-campagne-efficacite.py (porteur comment-form stale v1.7.39) ; 17 SKILL.md hôte stale resynchronisés (parité 120/120) ; bootstrap inchangé (R2) ; certification ALL PASS 6/6.

### 4. Correctif structurel F2 — garde anti-perte du scelleur v2.3 — P2 [GO propriétaire requis] — **ÉTEINTE**
- **Nature** : le scelleur traite toute divergence corpus↔archive comme une dérive (ECHEC sans distinction dérive/légitime), bloquant la 1ʳᵉ évolution de corpus légitime depuis Task 100 ; contournement manuel actuel = mise à l'écart explicite de l'archive entrante + rescellement fraî.
- **Source** : suite 153 (constat F2, S3) ; CW Task 107 finding F2.
- **Critère d'extinction** : une montée de version de corpus (bump PM) rescellée SANS ECHEC transitoire ni intervention manuelle — la voie opérationnelle documentée devient mécanique.
- **EXTINCTION (2026-11-19, Task 110 G2, GO trace 1a1f2297d90c957d)** : **NOUVEAU véhicule `scripts/task-f5-seal-archive-v24.py`** (v2.3 conservé intact R4, précédent v2.2→v2.3 Task 100) — PERTE bloquée rc=2 (jamais contournable), ÉVOLUTION LÉGITIME à contenu local commité (chaîne git BASE→--depot-git) rescellée SANS ECHEC ni intervention (harnais T1 : bump corpus commité → rc=0 tracé — matrice T0-T5 **9/9 PASS ×2**), divergence non commitée rc=3 + guidance, drapeau --autoriser-evolution ; pipeline repointé (--depot-git REPO) ; parité v2.3/v2.4 prouvée (SHA identiques, EPOQUE_FIXE) + rescellement réel état propre byte-stable (SHA fd2b5682…) et pilier KB mis à jour rescellé par la voie mécanique (G3).

### 5. GO-3 — convention S3 aux canons script-creator/correct-py — P3 (optionnel) [GO propriétaire requis] — **ÉTEINTE**
- **Nature** : formaliser la convention « docstring d'abord, bloc CONTEXTE ensuite » (démontrée par bootstrap-ecosysteme.py, 7ᵉ script scanné au titre N1 par tool-routing) dans les SKILL.md de script-creator et correct-py.
- **Source** : feuille de route §8.3 du rapport Task 105.
- **Critère d'extinction** : les 2 SKILL.md portent la convention (montée de version mineure + cascade KO-L004) ; tool-routing N1 inchangé (PASS).
- **EXTINCTION (2026-11-19, Task 110 G3, GO trace 1a1f2297d90c957d)** : script-creator **v1.1.0→v1.2.0** (§2 + §4) + correct-py **v1.1.0→v1.2.0** (§4 + HISTORIQUE) ; cascade KO-L004 : KB (2 montées + notes), pins ECO_SKILLS de check-ecosysteme-integrity.py recalibrés ×2 arbres, rescellement v2.4 mécanique (pilier KB), manifeste régénéré ×2 arbres, miroirs ; lignage @historique NO-OP honnête (aucun fichier par-skill pour ces 2 skills — convention non applicable, consigné) ; tool-routing **PASS 6/6 AVANT et APRÈS** (N1 inchangé) ; certification ALL PASS 6/6.

### 6. Décision cron 531684 — P3 [PROPRIÉTAIRE]
- **Nature** : le job de cadence autonome (2 h) est absent de la plateforme (3ᵉ dispositif perdu — vérifié ce tour : cron list = 0 job). L'escalade propriétaire est maintenue ; AUCUNE recréation en boucle (clause anti-boucle, règle d'or n°5).
- **Mise à jour Task 111 (2026-11-20)** : re-vérification cron list = 0 job — **4ᵉ dispositif perdu** ; escalade maintenue, décision propriétaire toujours requise (recréation OU entérinement de l'absence).
- **Source** : suites 141-142 (incident), 153 (point d'état), présent tour (vérification cron list 0).
- **Critère d'extinction** : décision propriétaire consignée — recréation (cron list ≥ 1 job actif) OU entérinement de l'absence (le préflight/bootstrap en ouverture de session couvre déjà le besoin de réparation).

### 7. Surveillance F3 au prochain bootstrap — P3 [AUTO, surveillance] — **ÉTEINTE**
- **Nature** : si la branche injection de l'injecteur récidive au prochain bootstrap (tâche 3 non exécutée), capture immédiate — le harnais sait désormais le faire.
- **Source** : feuille de route §8.4 du rapport Task 105.
- **Critère d'extinction** : constat consigné au prochain tour d'installation (récidive capturée OU absence constatée après exécution de la tâche 3).
- **EXTINCTION (2026-11-20, Task 111, trace 1a1f7d3e607663f1)** : constat consigné au tour d'installation GO-1 — bootstrap-ecosysteme.py exécuté : preflight RÉPARÉ (2778 modes, 0 contenu), dry-run 55 divergences hôte, installation 55 SHA **0 divergence**, certification ALL-PASS-6/6, garde É1 INSTALLE — branche injection v2.2.0 SAIN : 0 récidive, 0 SyntaxError, 0 revert ; re-check ensure-installed rc=0 (55 entrées KB, 0 manquant).

### 8. PMs §0 — propagation automatique aux prochaines montées — P3 [AUTO]
- **Nature** : le générateur KO-L004 recalibre mécaniquement SHARED/PM-INSTALL à chaque montée de version (comportement vérifié Task 92/107) ; les en-têtes §0 des skills/scripts suivent par propagate-context (une fois F3 corrigé, sans limite).
- **Source** : suite 153 (PMs §0 [AUTO]) ; §2quater PM-INSTALL.
- **Critère d'extinction** : continu — vérifié à chaque cascade (statut nominal, aucune action isolée).

## Clôture des fichiers de suivi antérieurs (vérifiée éteinte en G1)

- ~~File re-curation priorisée (Task 72 G3)~~ — éteinte en Task 85 (iphone17 = dernière cible).
- ~~Pendance F1 scelleur v2.3 (Task 99)~~ — éteinte en Task 100 (GO).
- ~~Différés Task 76/78/81~~ — vérifiés éteints en Task 101.
- ~~Pendance PUSH 3 commits (Tasks 104-106)~~ — éteinte en Task 107 G0.
- ~~Défaut F1 auto-install D727 (Task 105)~~ — éteinte en Task 107 GO-2 (V2 rend INSTALLE rc=0).
- ~~Fiche agent-engineering (Task 104)~~ — livrée (PDF 12 pages) ; seul son push était en pendance, éteint en Task 107.
