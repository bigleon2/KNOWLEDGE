# Tâches restantes à faire — vue $FACON (cohérente, optimisée, fonctionnelle)

> Directive propriétaire trace `1a1f2096f9b3406d`, item b : « dis-moi $FACON les tâches restantes à faire » — $FACON = « de façon cohérente, optimisée et fonctionnelle » (registre @Alias, entrée D-105). Sources : relecture intégrale Task 108 G1 (153 suites + 21 clones), feuille de route §8 du rapport Task 105, findings CW Tasks 105-107, point d'état continue suite 153. Chaque tâche est ancrée dans sa source (cohérence), regroupée sans doublon (optimisation), et porte un critère d'extinction mécanique (fonctionnalité). Généré le 2026-11-19 · Task 108 G2.

## Vue priorisée (résumé chat)

| # | Tâche | Acteur | Priorité | État |
|---|---|---|---|---|
| 1 | Révoquer le PAT du tour Task 107 + fournir un PAT frais au prochain push | PROPRIÉTAIRE | **P1 — CRITIQUE** | ouvert |
| 2 | PUSH du commit Task 108 (nécessite le PAT frais) | PROPRIÉTAIRE→session | **P1** | ouvert (créé en G5) |
| 3 | GO futur — correctif structurel F3 : injecteur propagate-context.py (gabarit périmé + 5 scripts protégés sans bloc CONTEXTE) | PROPRIÉTAIRE (GO) + session | **P2** | proposé (suite 153) |
| 4 | GO futur — correctif structurel F2 : garde anti-perte du scelleur v2.3 (évolution légitime du corpus sans ECHEC transitoire) | PROPRIÉTAIRE (GO) + session | **P2** | proposé (suite 153) |
| 5 | GO-3 (optionnel) : convention « docstring d'abord » (S3/F4) aux canons script-creator + correct-py | PROPRIÉTAIRE (GO) + session | **P3** | proposé (§8 Task 105) |
| 6 | Décision cron 531684 (3ᵉ dispositif perdu) : recréer ou entériner l'absence | PROPRIÉTAIRE | **P3** | escalade maintenue |
| 7 | Surveillance F3 au prochain bootstrap (si récidive : capture immédiate) | session (AUTO) | P3 | surveillance |
| 8 | PMs §0 : propagation automatique aux prochaines montées de version | AUTO (générateur KO-L004) | P3 | nominal |

Aucune autre pendance : re-curation ÉTEINTE (Task 85), différés Task 101 vérifiés éteints, familles/orchestrateurs tranchés (Task 106 : non-création), pendances PUSH antérieures toutes éteintes (Task 107 G0), G-RES OK (7,6 Go, profil NORMAL).

## Détail par tâche

### 1. Rotation/révocation du PAT GitHub — P1 CRITIQUE [PROPRIÉTAIRE]
- **Nature** : le jeton utilisé depuis la Task 63 a cumulé **33 expositions** (E15, suite 153). Le jeton du tour Task 107 doit être révoqué côté GitHub ; un PAT frais sera fourni par le propriétaire à tout tour nécessitant un push.
- **Source** : suite 153 point d'état (« rotation/révocation PAT [PROPRIÉTAIRE — CRITIQUE — 33 expositions cumulées, révoquer le jeton du tour après usage] ») ; leçons Task 98/101.
- **Critère d'extinction** : révocation effectuée côté GitHub + (si push requis) nouveau PAT fourni dans une directive — 0 trace écrite (KO-L009).

### 2. PUSH du commit Task 108 — P1 [PROPRIÉTAIRE→session]
- **Nature** : le commit « Task 108 CLOSE » (créé en G5 ce tour) restera local — **aucun PAT n'a été fourni ce tour** (0 manipulation, 0 exposition). Pendance PUSH 1 commit.
- **Source** : présent tour (G5) ; leçon Task 98/101 (« push immédiat dès PAT frais disponible »).
- **Critère d'extinction** : `git ls-remote` anonyme → origin/main = HEAD dépôt ; `git rev-list --count origin/main..HEAD` = 0.

### 3. Correctif structurel F3 — injecteur propagate-context.py — P2 [GO propriétaire requis]
- **Nature** : la branche « injection fraîche » de l'injecteur §0 porte un gabarit LITTÉRAL périmé (v1.7.39 — la dynamisation v2.1.1 ne couvre que la branche remplacement, classe F-70-2) et casse les scripts `from __future__`. 5 scripts (task98/101/102/104/106) ont été protégés par revert et **demeurent sans bloc CONTEXTE** (état certifié R2).
- **Source** : suite 153 (constat F3, S3) ; CW Task 107 finding F3.
- **Critère d'extinction** : propagation re-jeuée idempotente ×2 sur les 338 fichiers → 0 SyntaxError, 0 revert requis, les 5 scripts restaurés portent un bloc §0 v1.7.40 correct ; certification ALL PASS 6/6.

### 4. Correctif structurel F2 — garde anti-perte du scelleur v2.3 — P2 [GO propriétaire requis]
- **Nature** : le scelleur traite toute divergence corpus↔archive comme une dérive (ECHEC sans distinction dérive/légitime), bloquant la 1ʳᵉ évolution de corpus légitime depuis Task 100 ; contournement manuel actuel = mise à l'écart explicite de l'archive entrante + rescellement fraî.
- **Source** : suite 153 (constat F2, S3) ; CW Task 107 finding F2.
- **Critère d'extinction** : une montée de version de corpus (bump PM) rescellée SANS ECHEC transitoire ni intervention manuelle — la voie opérationnelle documentée devient mécanique.

### 5. GO-3 — convention S3 aux canons script-creator/correct-py — P3 (optionnel) [GO propriétaire requis]
- **Nature** : formaliser la convention « docstring d'abord, bloc CONTEXTE ensuite » (démontrée par bootstrap-ecosysteme.py, 7ᵉ script scanné au titre N1 par tool-routing) dans les SKILL.md de script-creator et correct-py.
- **Source** : feuille de route §8.3 du rapport Task 105.
- **Critère d'extinction** : les 2 SKILL.md portent la convention (montée de version mineure + cascade KO-L004) ; tool-routing N1 inchangé (PASS).

### 6. Décision cron 531684 — P3 [PROPRIÉTAIRE]
- **Nature** : le job de cadence autonome (2 h) est absent de la plateforme (3ᵉ dispositif perdu — vérifié ce tour : cron list = 0 job). L'escalade propriétaire est maintenue ; AUCUNE recréation en boucle (clause anti-boucle, règle d'or n°5).
- **Source** : suites 141-142 (incident), 153 (point d'état), présent tour (vérification cron list 0).
- **Critère d'extinction** : décision propriétaire consignée — recréation (cron list ≥ 1 job actif) OU entérinement de l'absence (le préflight/bootstrap en ouverture de session couvre déjà le besoin de réparation).

### 7. Surveillance F3 au prochain bootstrap — P3 [AUTO, surveillance]
- **Nature** : si la branche injection de l'injecteur récidive au prochain bootstrap (tâche 3 non exécutée), capture immédiate — le harnais sait désormais le faire.
- **Source** : feuille de route §8.4 du rapport Task 105.
- **Critère d'extinction** : constat consigné au prochain tour d'installation (récidive capturée OU absence constatée après exécution de la tâche 3).

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
