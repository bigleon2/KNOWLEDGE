# Plan Task 51 — Exécution du PM ghorg-to-ecosysteme.md v1.1 en mode STEP (forks ghorg/cmdr · tests $FACON2 fonctionnels · correct-work(projet) · clone-chat)

Session : web-c30e6506 · Date : 2026-11-04 · Générateur : gen-plan v3.34.0 (mode step)
Horodatage plan : 2026-11-04T19:50:00+00:00

## Directives verbatim (règle d'or n°7 — expansion alias-eco : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » · $ECO-LEON = « mon écosystème personnel »)

1. « exécute le MD en mode STEP » — cible : `upload/ghorg-to-ecosysteme.md` (PM v1.1, certifié Task 50 — batterie T1-T6 PASS).
2. « "bigleon2/ghorg" » — objectif 1 du MD : intégrer GHORG (fork, scripts idempotents, configuration, documentation).
3. « "bigleon2/cmdr" » — objectifs 2-3 du MD : cloner CMDR EDITOR via ghorg + intégrer la famille TSI complète dans le clone.
4. « fais $FACON des tests $FACON2 fonctionnels sur "bigleon2/ghorg" dans l'objectif de trouver des failles et de l'optimiser (ainsi que son intégration à mon écosystème). »
5. « fais $FACON des tests $FACON2 fonctionnels sur "bigleon2/cmdr" dans l'objectif de trouver des failles et de l'optimiser (ainsi que son intégration à mon écosystème). »
6. « correct-work (projet). »
7. « clone-chat. »

## Constats d'état disque et environnement (E1-E2 — règle d'or n°5, tout relevé par commande le 2026-11-04T19:4xZ)

- **Environnement** (§4 du MD) : Linux · bash · git présent · `gh` ABSENT · `go` ABSENT (mais **apt 3.0.3 fonctionnel, candidat golang-go 2:1.24~2** → compilation ghorg réellement vérifiable après provisioning P1) · réseau github.com OK (ls-remote anonyme fonctionne) · **jeton GH_TOKEN ABSENT de la session** → repli MD §4 : audit + plan + fichiers prêts + commits locaux, **aucune action distante** (KO-L009 point 5).
- **Forks** : `bigleon2/ghorg` et `bigleon2/cmdr` **inexistants** (F=0 ×2 — ls-remote anonyme → demande d'identifiants = dépôt absent ; API REST rate-limit 0/60, reset 20:23:26Z). Les dépôts d'origine existent : `gabrie30/ghorg` HEAD e05d9b5f (master) · `cmdr-editor/cmdr` HEAD 5b795027 (master).
- **Clone KNOWLEDGE** : `~/GitHub/bigleon2/KNOWLEDGE`, branche main, HEAD 5fed294 (à jour, fb52137 poussé Task 50). Aucune branche `feat/ghorg-ecosysteme` existante.
- **Famille TSI au dépôt** (git ls-files) : 7 skills confirmés (tsi-architect, tsi-validator, multi-shift-architect, midi-doc-expert, orchestrateur-tsi, analyse-doc-s4mk2, inter-scripts) + **2 agents** (`skills/tsi-architect/tsi-architect.agent`, `skills/orchestrateur-tsi/agent-TSI.agent` — le second est une découverte d'audit, non listé dans le MD).
- **Conventions dépôt** : scripts/ = **Python stdlib kebab-case** (147 scripts — le MD présumait bash/PowerShell → finding d'optimisation : scripts en Python convention dépôt, règle d'or n°9) · style commits « Task NN — description » · worklog.md format SHARED §1.4 · registre KB `skills/KNOWLEDGE.md` (48 sections — inscription du nouveau skill requise, KO-L004).
- **Hygiène** : `dev.log` EST suivi par git (P2 — proposer .gitignore + git rm --cached, sans suppression disque) ; `.next` non suivi.
- **Espace de travail MD §4** : `~/GitHub/_outils/` ABSENT (à créer).

## Groupes d'exécution (mode step — correct-work(groupe) après chaque groupe, max 2 rounds de correction)

### G1 — Phase A (environnement) + Phase B (audit KNOWLEDGE + dépôts d'origine) + provisioning Go [~6 k#token]
- SG1.1 · [À FAIRE] Relevé §4 complet consigné (OS, shell, versions, réseau, identité — jeton ABSENT documenté, pas de contournement) + **installation Go via apt** (P1 — prérequis tests fonctionnels réels ; en cas d'échec : ghorg compilation NON VÉRIFIÉE documenté, règle MD §4).
- SG1.2 · [À FAIRE] Audit Phase B : arborescence 2 niveaux, README, worklog (format), .gitignore, package.json scripts, git log -20 (style) ; inventaire famille TSI complet (7 skills + 2 agents, classification skill/agent/script/document/donnée/bruit) ; contrôle hygiène (dev.log suivi → P2) ; audit dépôts d'origine (branche par défaut, licence — via clone/ls-remote, API étant rate-limitée).

### G2 — Phase C (PLAN) + D1 (forks — repli documenté) + D2-D3 (branche + arborescence + commits) [~10 k#token]
- SG2.1 · [À FAIRE] `~/GitHub/_outils/PLAN-ghorg-ecosysteme.md` (tableau 7 colonnes du MD §6.C) + journal d'état `etat-ghorg-ecosysteme.json` (§10) — **avant toute écriture dans le dépôt**.
- SG2.2 · [À FAIRE] D1 : forks non créables (pas de jeton) — repli MD §4 documenté dans le PLAN et le rapport : fichiers prêts, commits locaux, zéro action distante (KO-L009 point 5).
- SG2.3 · [À FAIRE] D2-D3 : branche `feat/ghorg-ecosysteme` + arborescence complète — `ecosystem/` (manifest.yaml réécrit par bootstrap, selection-tsi.yaml [7 skills + 2 agents + raisons], ghorg/reclone.yaml.tmpl, ghorg/targets/cmdr.txt) · `scripts/ecosystem/` (**Python stdlib** — bootstrap.py, ghorg-install.py, cmdr-clone.py [Karnaugh F/L/S/B — 4 variables relevées avant action], cmdr-overlay-sync.py [SHA-256, SOURCE.md]) · `skills/ghorg-cmdr/SKILL.md` (format écosystème) + inscription registre KB (KO-L004) ; commits atomiques au style du dépôt.

### G3 — Phase D4-D5 : GHORG local + tests $FACON2 fonctionnels ghorg [~10 k#token]
- SG3.1 · [À FAIRE] D4 : `ghorg-install.py` exécuté — clone `gabrie30/ghorg` (deviation documentée : fork absent → source directe, remote origin à re-pointer quand le fork existera) vers `~/GitHub/_outils/ghorg`, remote upstream, **build Go réel** (go build), marqueur `.ghorg-commit`, PATH.
- SG3.2 · [À FAIRE] **Batterie tests ghorg** : TG1 compilation + version ; TG2 surface CLI vs options du MD (8/8) ; TG3 comportement sans jeton (chemin d'erreur attendu — finding : ghorg exige GHORG_GITHUB_TOKEN même pour publics) ; TG4 Karnaugh F/L/S/B du `cmdr-clone.py` — simulation mécanique des 16 états (dépôts git locaux factices, sans action distante) ; TG5 reclone.yaml (écriture balisée UTF-8 sans BOM, entrée cmdr-editor-fork) ; TG6 idempotence ghorg-install ×2. **Failles trouvées → listées + optimisations appliquées (P2 risque nul) ou proposées.**

### G4 — Phase D6-D8 : superposition cmdr + tests $FACON2 fonctionnels cmdr [~8 k#token]
- SG4.1 · [À FAIRE] D5/D6 : clonage réel de CMDR (git anonyme depuis `cmdr-editor/cmdr` — deviation origin documentée en attente du fork ; ghorg clone tenté si API reset + jeton disponible, sinon chemin git direct documenté) ; branche overlay `ecosystem/tsi-traktor-s4mk2` ; `cmdr-overlay-sync.py` : copie unilatérale KNOWLEDGE → `cmdr/ecosystem/` (sélection complète, comparaison SHA-256, non-réécriture si identique, SOURCE.md avec SHA, suppression seulement si listé au SOURCE.md précédent) ; licence CMDR lue et rapportée ; 0 fichier touché hors `ecosystem/`.
- SG4.2 · [À FAIRE] **Batterie tests cmdr** : TC1 intégrité superposition (hashes, SOURCE.md ↔ disque) ; TC2 re-jeu overlay = 0 changement (idempotent) ; TC3 0 fichier modifié hors ecosystem/ (git diff --stat) ; TC4 **E2E famille TSI : tsi-validator exécuté sur les fichiers .tsi du dépôt cmdr** (preuve d'intégration écosystème ↔ CMDR) ; TC5 licence + structure ; compilation NON VÉRIFIÉ (Linux — règle MD §4). Failles → rapport.
- SG4.3 · [À FAIRE] D8 : entrée worklog.md (dépôt, format existant) + miroir profil `/home/z/my-project`.

### G5 — Phase E : vérification §8 + rapport final [~6 k#token]
- SG5.1 · [À FAIRE] Tableau §8 (11 contrôles — VÉRIFIÉ/NON VÉRIFIÉ/ÉCHEC + preuve commande/sortie ; contrôles distants = NON VÉRIFIÉ [repli §4]) ; **contrat d'idempotence : bootstrap ×2** (2ᵉ exécution : tout « déjà à jour », porcelain vide, 0 commit, exit 0) ; arbitres dépôt (verify-cross, integrity, coherence, doublons, garde-plans) ; rapport final §9 → `download/rapport-final-task51-ghorg-cmdr.md` + miroirs profil (skills/ghorg-cmdr, scripts/ecosystem, ecosystem/, plan).

### G6 — correct-work (projet) + clone-chat [~5 k#token]
- SG6.1 · [À FAIRE] correct-work **Mode PROJET** sur la chaîne G1-G5 (max 2 rounds de correction) — verdict consigné.
- SG6.2 · [À FAIRE] **clone-chat** — archive de la discussion → `download/` (format PM CLONE-CHAT v2.0.2).

**Budget total estimé : ~45 k#token** + contingence ×2-3.

## Answer key (décisions D201-D208 — criterion + verification exécutable)

- **D201** — Audit Phase A+B complet, 0 donnée inventée
  - criterion: chaque valeur du rapport provient d'une commande exécutée ; absences consignées ABSENT (jeton, gh, forks, go avant provisioning) ; découverte agent-TSI.agent intégrée
  - verification: rapport final §audit + worklog citent les commandes ; `grep -c "ABSENT" rapport ≥ 3`
- **D202** — PLAN Phase C produit AVANT toute écriture dépôt
  - criterion: `~/GitHub/_outils/PLAN-ghorg-ecosysteme.md` (tableau 7 colonnes ID/Priorité/Constat/Action/Fichiers/Risque/Vérification) existe avant le premier commit D3
  - verification: horodatage fichier < premier commit feat/ghorg-ecosysteme ; colonnes présentes
- **D203** — 0 action distante (repli MD §4 + KO-L009 point 5)
  - criterion: forks non créés, 0 push, 0 PR ; déviations (origin=source en attente de fork) documentées
  - verification: `git log origin/main..feat/ghorg-ecosysteme` = commits locaux non poussés ; ls-remote bigleon2/ghorg et /cmdr toujours absents
- **D204** — Arborescence D3 complète + commits atomiques + inscription KB
  - criterion: ecosystem/ (manifest, selection-tsi 7+2, reclone tmpl, targets), scripts/ecosystem/ 4 scripts Python, skills/ghorg-cmdr/SKILL.md, registre KNOWLEDGE.md mis à jour ; style commits conforme
  - verification: `git ls-files` sur la branche liste l'arborescence ; `grep ghorg-cmdr skills/KNOWLEDGE.md` ≥ 1
- **D205** — GHORG compilé réellement + marqueur + manifeste re-scellé
  - criterion: go build exécuté (Go provisionné), `.ghorg-commit` = SHA du clone ghorg, manifest.yaml réécrit par bootstrap avec SHA réels du jour (ls-remote/rev-parse)
  - verification: `~/GitHub/_outils/bin/ghorg` exécutable + version ; SHA .ghorg-commit == rev-parse HEAD du clone ghorg
- **D206** — Tests fonctionnels ghorg exécutés avec preuves + failles + optimisations
  - criterion: TG1-TG6 consignés (sorties réelles), ≥ 1 faille documentée, optimisations appliquées (P2) ou proposées
  - verification: rapport tests (worklog + download/) ; Karnaugh 16 états simulés couverts
- **D207** — Superposition cmdr réelle et idempotente
  - criterion: clone cmdr réel, branche overlay, ecosystem/ rempli, SOURCE.md SHA-256, 0 fichier hors ecosystem/, re-jeu = 0 changement
  - verification: `git -C cmdr diff --stat master...HEAD` ne touche que ecosystem/ ; re-jeu overlay-sync → porcelain vide
- **D208** — Vérification §8 + rapport final + worklog + bootstrap ×2
  - criterion: tableau 11 contrôles rempli avec preuves, contrat idempotence ×2 respecté (exit 0), rapport §9 complet, worklog dépôt + profil, arbitres verts (ou WARN baseline préservée)
  - verification: `ls download/rapport-final-task51-ghorg-cmdr.md` ; bootstrap 2ᵉ run exit 0 ; sorties arbitres consignées

## Statuts (état disque — règle d'or n°5, mis à jour à chaque groupe)

- G1 [TERMINÉ 2/2 SG — correct-work(groupe) PASS : D201 audit 0 invention, ABSENT consignés (gh, jeton, licences→clones), agent-TSI.agent découvert] · G2 [TERMINÉ 3/3 SG — correct-work(groupe) PASS : D202 PLAN 19:53:57 < commit 19:58:23 (11 lignes × 7 colonnes) · D203 3 commits locaux 0 push (831d7a6, 6496980, b74dbf9) · D204 arborescence complète + KB 49e section] · G3 [TERMINÉ 2/2 SG — correct-work(groupe) PASS : D205 ghorg v1.11.18 compilé (marqueur==rev-parse==ls-remote e05d9b5f) · D206 TG1-TG6 PASS (TG2 8/8, TG3 exit 1 sans jeton [finding], TG4 20/20, TG5 sans BOM préservé, TG6 déjà à jour) — commit 548b9ec] · G4 [TERMINÉ 3/3 SG — correct-work(groupe) PASS : D207 superposition réelle 55 fichiers idempotente (TC2 ×3 : 0 copie, porcelain 0 ; TC1 55/55 ; TC3 0 hors ecosystem/) · D208 partiel : TC4 E2E 21 PASS/2 FAIL légitimes (findings F1/F2), TC5 GPL v3, compilation NON VÉRIFIÉ — commits 40ce41a + 58abfc2 (worklog D8) + e4fdd1c (cmdr)] · G5 [TERMINÉ 1/1 SG — correct-work(groupe) PASS : D208 — contrat idempotence §8 VÉRIFIÉ (runs 4-5 : exit 0, déjà à jour, porcelain 0/0, 0 commit) après résorption de 3 failles (doublon cibles, boucle de salissure SOURCE.md, couplage épingle HEAD) ; tableau §8 rempli (8 VÉRIFIÉ + 1 déviation documentée + 2 NON VÉRIFIÉ légitimes) ; arbitres dépôt verify-cross 100 % + integrity 100/100 + garde-plans PASS ; arbitres profil 100/100 (sync version-management + KNOWLEDGE.md) ; rapport final download/rapport-final-task51-ghorg-cmdr.md ; miroir profil byte-identique] · G6 [À FAIRE]

---

Verdict E8 : PASS (P1-P5 exécutés via `skills/gen-plan/scripts/check_plan_protocol.py` — plan présent 11110 caractères, answer key 8 décisions vérifiables, worklog R5 cite le plan, PLAN-AFFICHE dans l'entrée, verdict + horodatage couplés — Horodatage vérifié : 2026-11-04T19:50:00+00:00)

---

Clôture (G6) : chaîne G1→G6 TERMINÉE — correct-work(groupe) PASS ×5 · correct-work(projet) PASS (mécanique 16/16, D201-D208 vérifiés, 0 finding ouvert) · clone-chat archivé (`download/clone-discussion-2026-11-04-task51-ghorg-cmdr-execution.md`). Aucun push (KO-L009 point 5).
