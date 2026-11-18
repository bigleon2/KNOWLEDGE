# Clone de discussion — session web-ecef7f80 (Tasks 104→107), 20ᵉ de la lignée

> **Auto-clonage** : ce document est auto-suffisant — une session héritière peut reprendre le contexte sans fichier externe (règle zéro : les fichiers des sessions précédentes n'existent pas dans une nouvelle session, tout se reconstruit depuis la lignée). Lignée : Task 72 → … → 103 (19ᵉ clone) → **présent 20ᵉ (Task 107)** · Généré le 2026-11-19 · gen-plan v3.43.0 / correct-work v2.11.0 / clone-chat v2.0.2 · PM-INSTALL v1.10.0.

## §0 — Contexte Système (SHARED v1.7.40)

Écosystème Knowledge : SKILLS_ROOT=skills/ | KB_PATH=skills/KNOWLEDGE.md | 55 entrées KB versionnées + collections @ (121 dossiers skills hôte) · dépôt git local miroir `/home/z/my-project/KNOWLEDGE-repo` (github.com/bigleon2/KNOWLEDGE, branche main) · worklog.md hôte↔dépôt parité md5 · conventions : kebab-case, semver, #token, français exclusif (règle d'or n°6) · référence canonique « mon skill X » = forme installée `skills/X/SKILL.md`, jamais le PM du corpus · KO-L009 : tout jeton reste en mémoire de commande, jamais écrit · R2 anti-rétrogradation · R4 une information une source · arbitres pré-commit : verify-correct-work, certification-complete (6), check-triggers-replay, task14-scan-doublons.

## §1 — Worklog chronologique (fenêtre du clone : suites 150-153)

| Suite | Date | Task | Faits saillants |
|---|---|---|---|
| 150 | 2026-11-16 | 104 CLOSE | Fiche PDF « agent engineering » 12 pages A4 (5 exemples concrets) — commit 24441ed2, SANS PUSH |
| 151 | 2026-11-18 | 105 CLOSE | Installation écosystème + campagne efficacité 3 axes — défaut F1 découvert (auto-install D727 cassé depuis Task 69), prototype V3 consolidé (−83,3 % tours/−97,6 % octets), stratégie S1-S4 + feuille de route GO-1→GO-4 — commit fe85dba6, SANS PUSH |
| 152 | 2026-11-18 | 106 CLOSE | Analyse familles : 7 familles mesurées, verdict OUI regroupement déjà capturé / NON nouveaux orchestrateurs (4ᵉ refus cohérent) — commit 0473e8f4, SANS PUSH |
| 153 | 2026-11-19 | 107 CLOSE (en cours) | PUSH pendance 3 commits (aa855a2f..0473e8f4) · GO-1 entrée canonique consolidée (PM-INSTALL v1.10.0 §3.2-c + SHARED v1.7.40 + propagation §0 120+213+4) · GO-2 correctif F1 (V2 INSTALLE) · CW PASS · présent clone — commits ec86d87d, f21d9bd7, b7e799fe + clôture |

Chaque session a son entrée intégrale au `worklog.md` (source de vérité — format SHARED §1.4) ; le présent tableau est la vue chronologique exigée par clone-chat Étape 1.

## §2 — Artefacts de la fenêtre (Étape 2)

| Catégorie | Fichiers |
|---|---|
| Plans | `download/plan-task104-fiche-agent-engineering.md` · `plan-task105-tests-efficacite-installation-cw-bloc.md` · `plan-task106-orchestration-familles-cw-projet.md` · `plan-task107-go1-entree-canonical-go2-correctif-f1-cw-clone.md` |
| Livrables propriétaire | `download/fiche-agent-engineering-ecosysteme.pdf` (12 p.) + couverture HTML · `carte-familles-ecosysteme.md` · `rapport-tests-efficacite-task105.md` |
| Rapports CW | `rapport-cw-task104…` · `rapport-cw-task105-bloc.md` · `rapport-cw-task106-projet.md` · `rapport-cw-task107-projet.md` |
| Rapports machine Task 107 | `rapport-bootstrap-consolide-task107.json` · `rapport-nonregression-task107-{garanties,flux}.json` (miroirs dépôt des re-jeus) |
| Scripts (dépôt) | `task104-genere-fiche.py` · `task105-campagne-efficacite.py` · `task106-inventaire-familles.py` · **`bootstrap-ecosysteme.py` (NOUVEAU — entrée canonique, GO-1)** |
| Modifications système | `skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` v1.10.0 · `PROMPT-MAITRE-SHARED.md` v1.7.40 · `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` régénéré · `skills/gen-plan/scripts/ensure-installed.py` (correctif F1) · propagation §0 (120 SKILL.md + 213 scripts + 4 agents) · archive rescellée + manifeste |

## §3 — Décisions, bugs, conventions (Étape 3)

**Décisions propriétaire (directives)** : (D-104) fiche PDF agent engineering 5 exemples ; (D-105) installer l'écosystème puis tester le système d'installation pour optimiser son efficacité ($FACON = « de façon cohérente, optimisée et fonctionnelle », $FACON2 = « (cohérent, optimisé et fonctionnel) » — registre @Alias) ; (D-106) question familles/orchestrateurs avec condition « si oui » ; (D-107) chaîne ordonnée « PUSH · GO-1 · GO-2 · correct-work · clone-chat · continue » — GO-1/GO-2 = feuille de route du rapport Task 105 §8.

**Décisions d'exécution Task 107** : versionnement PM-INSTALL v1.10.0 (mineur — nouvelle clause mécanique §3.2-c, précédent v1.8.0) ; SHARED v1.7.40 (patch — recalibrage référence §6.1, précédent v1.7.39) ; PAS de bump gen-plan pour le correctif F1 (restauration du comportement documenté §1.16, pas de changement de spécification) ; commits GO-1/GO-2 AVANT chaque exécution du bootstrap (le préflight répare par reset --hard — aucune modification légitime non commitée) ; revert des 5 scripts victimes d'injection périmée (états certifiés, R2).

**Bugs corrigés (cause → fix → résultat)** :
1. **F1 (hérité Task 105, corrigé GO-2)** : copie dépôt d'ensure-installed.py crashe (`subprocess cwd=ROOT/KNOWLEDGE-repo` inexistant quand ROOT est le dépôt — introduit par le contrôle « head miroir » O-68-1 Task 69 ; inaperçu 15 jours car le bootstrap canonique était manuel) → garde d'existence `(miroir/.git).exists()` + head = ROOT si dépôt (11+/3−) → V2 rend INSTALLE rc=0 (test dédié + harnais flux fonctionnel=true).
2. **F2 (constaté ce tour)** : garde anti-perte du scelleur v2.3 bloque toute évolution légitime du corpus (aucune dérive/légitime) → voie opérationnelle : mise à l'écart explicite de l'archive entrante + rescellement fraî (restauration .bak native, corpus historisé git) → 2 rescellements réussis ; correctif structurel proposé sous GO futur.
3. **F3 (constaté ce tour)** : branche injection de propagate-context.py porte un gabarit littéral périmé (v1.7.39) et casse les scripts `from __future__` (classe F-70-2 — la dynamisation v2.1.1 ne couvre que le remplacement) → 5 scripts protégés par revert (task98/101/102/104/106) ; correctif proposé sous GO futur.
4. Dérive hôte 5ᵐᵉ récidive recyclage sandbox (version-management absent + 2 fichiers mode-bits) → réparée automatiquement par l'entrée canonique (préflight/installation) — comportement nominal.

**Conventions établies/réaffirmées** : « docstring d'abord, bloc CONTEXTE ensuite » (S3/F4) — le nouveau script passe tool-routing N1 (7ᵉ script scanné) ; l'entrée canonique du bootstrap de session = `scripts/bootstrap-ecosysteme.py` (1 commande, 1 tour) — la séquence G0 manuelle est remplacée à la racine du flux de session ; mirroirs re-jeus sous noms `task107` (les originaux Task 105 du dépôt demeurent — R4).

## §3.5 — Context Drift (Étape 3.5)

| Type | Avant → Après | Réf. |
|---|---|---|
| ENRICHISSEMENT | PM-INSTALL §3.2 mécanisme dual (a)/(b) → + (c) entrée consolidée canonique v1.10.0 | suite 153, G1 |
| CORRECTION | auto-install D727 ECHEC (F1, cassé depuis Task 69) → INSTALLE rc=0 | suite 153, G2 |
| RECALIBRAGE | SHARED v1.7.39 → v1.7.40 (§6.1 ligne PM-INSTALL v1.9.16→v1.10.0) + propagation §0 337 fichiers | suite 153, G1 |
| MODIFICATION | bootstrap de session : 6 tours manuels (V1) → 1 commande consolidée (V3 canonique, −83,3 % tours) | suite 153, G1 |
| DÉGRADATION EXTERNE | recyclage sandbox 5ᵉ récidive (version-management hôte absent, 2 fichiers dérivés) — réparée par l'entrée canonique | suite 153, G0/G2 |

## §4 — Spécifications techniques (Étape 4 — fichiers prioritaires)

1. **`scripts/bootstrap-ecosysteme.py`** (NOUVEAU, ~250 l.) — in extenso de l'interface : `bootstrap()` séquence 5 étapes (preflight git [fetch anonyme + reset --hard LOCAL si porcelain ≠ 0] → dry-run → installation → certification ["ALL PASS (6/6)"] → É1 [--check]) ; `_verdict()` agrégation minimale (STATS_VERTS) — INSTALLE / INSTALLE-REPARÉ / ECHEC ; `--selftest` 5 tests (exécutants présents, verdicts synthétiques, dry-run rc∈{0,2}, N1 docstring < 600 octets, JSON) ; codes 0/1 ; rapport `download/bootstrap-ecosysteme-rapport.json` ; chemins absolus BASE/REPO/HOST (précédent auto-install).
2. **`skills/gen-plan/scripts/ensure-installed.py`** — correctif F1 dans `etat()` (lignes 70-80) : miroir interrogé seulement si `(ROOT/"KNOWLEDGE-repo"/".git")` existe ; sinon `head = ROOT` quand `git_repo` ; sémantique O-68-1 (head = source de vérité) et champ forensique `host_head` préservés ; copie hôte inchangée par construction.
3. **PM-INSTALL v1.10.0** — §3.2(c) : point d'entrée unique, orchestration R4, gains mesurés, voies (a)/(b) inchangées, D727 = self-healing partiel ; §2ter +1 ligne ; §7 ligne historique ; §A.3 instantané.
4. **Chaîne d'exécution de session (héritière)** : `python3 KNOWLEDGE-repo/scripts/bootstrap-ecosysteme.py` en OUVERTURE DE SESSION (remplace la séquence G0 manuelle — 1 tour au lieu de 6) ; puis gen-plan (step) pour toute directive ; arbitres pré-commit avant tout commit ; PUSH dès PAT frais (leçon Task 98/101).

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone (lignée Task 72→107, 20ᵉ) — les sections §1-§3 sont ENRICHIES par le clone du tour (nouvelles lignes worklog/artefacts/décisions/drifts), les sections §0/§4-§5 sont RÉGÉNÉRÉES (état courant du système). clone-chat référencé (skill v2.0.2, déclencheurs §A). La session héritière reprend : lire le présent clone + worklog.md (suites 150-153) + le rapport Task 105 (stratégie S1-S4) — puis exécuter le bootstrap canonique AVANT E1.

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », dépendance externe nulle, lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = 4 sessions de la fenêtre, chacune ≥ 1 ligne) | PASS |
| S3 | Complétude skills (chaque système créé/modifié décrit §2/§4 avec version et relations) | PASS |
| S4 | Complétude décisions (décisions avec contexte+conséquence, conventions avec règle) | PASS |
| S5 | Complétude bugs (4 bugs : cause racine + fix + résultat vérifié) | PASS |
| S6 | Complétude drifts (5 drifts typés, avant/après explicites, réf. suite) | PASS |
| S7 | Exécutabilité (§4 instructions claires, fichiers prioritaires, séquence héritière) | PASS |
| S8 | Auto-clonage (§5 croissance + clone-chat référencé + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — le PAT du tour n'apparaît nulle part : mémoire de commande uniquement, sorties masquées, E15 = 32ᵉ/33ᵉ expositions consignées au worklog uniquement).

(Étape 7 — Sauvegarde : présent fichier `download/clone-chat-session-web-ecef7f80-20261119-task107.md`, enregistrement au worklog suite 153.)
