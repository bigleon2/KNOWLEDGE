# Plan Task 50 — Corrections du PM ghorg-to-ecosysteme.md (règle d'or n°8 Périmètre TSI complet · Karnaugh 4 variables · jeton KO-L009) + adaptation $ECO-LEON + tests $FACON2 + analyse GHORG/CMDR

Session : web-c30e6506 · Date : 2026-11-04 · Générateur : gen-plan v3.34.0 (mode step)
Horodatage plan : 2026-11-04T21:05:00+01:00

## Directives verbatim (règle d'or n°7 — expansion alias-eco : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » · $ECO-LEON = « mon écosystème personnel »)

1. « Corrige $FACON le 1 : le périmètre doit être là famille TSI complète. »
2. « Corrige $FACON le 2 : ajoute $FACON la variable "branche courante" à la logique d'idempotence du clone. »
3. « Corrige $FACON le 3 : "<jeton github_pat_… révoqué depuis — consigné>" et réécrire $FACON les SHA du manifeste. »
4. « adapte $FACON le MD à mon écosystème personnel. »
5. « effectue $FACON des tests $FACON2 fonctionnels du MD dans l'objectif de l'optimiser $FACON. »
6. « analyse $FACON comment mieux intégrer $FACON GHORG et CMDR EDITOR à mon écosystème dans l'objectif de d'optimiser les performances et les fonctionnalités de mon écosystème et des éléments de ma famille TSI. Puis propose moi $FACON plusieurs suggestions $FACON2. »

Cible : `/home/z/my-project/upload/ghorg-to-ecosysteme.md` (PM autonome v1.0 pour agent GLM — analysed en préalable, session courante). Livrables : MD corrigé (in place + copie `download/ghorg-to-ecosysteme-v2.md`) + `download/rapport-integration-ghorg-cmdr-ecosysteme.md`.

## Constats d'état disque (E1-E2 — règle d'or n°5)

- MD original : 322 lignes, périmètre §1.3 = « KONTROL S4 MK2 » (restrictif vs famille TSI réelle : 7 entrées KB — tsi-architect v1.2.0, tsi-validator v1.2.0, multi-shift-architect v1.1.0, midi-doc-expert v1.2.0, orchestrateur-tsi v1.1.0, analyse-doc-s4mk2 v1.3.0 + inter-scripts v1.0.0 ; agent `tsi-architect.agent` ; livrable existant au dépôt : preset MIDI Controls Bridge task45 + extension LEON TSI EDITEUR v11).
- §7 : Karnaugh 3 variables (F, L, S) — le MD exige lui-même une table dès 3 variables ; la branche courante (B) manque → interaction « pull ghorg » × « branche overlay » non modélisée.
- §4/D5 : double canal de jeton (GH_TOKEN utilisateur vs `gh auth token` dans les scripts) ; manifeste §6.D3 à SHA épinglés jamais réécrits (dérive silencieuse) ; jeton fourni en session = **RÉVOQUÉ (401 vérifié)** — consigné KO-L009 (6e exposition canal), jamais persisté, scan 0 occurrence.
- SHA réels relevés par `git ls-remote` (canal natif, anonyme — règle d'or n°4) : cmdr-editor/cmdr + gabrie30/ghorg.
- Registre `@Alias` : expansions ci-dessus (aliases.json, mis à jour 2026-11-04).

## Groupes d'exécution (mode step)

### G1 — Corrections 1-3 du MD [~8 k#token]
- SG1.1 · Tâche 1.1 [À FAIRE] : **Correction 1** — §1 (objectif 3), §2.2, §6.B.3, §6.D6 : périmètre = **famille TSI complète** (les 7 entrées KB + l'agent, MK2 ET MK3 — sans restriction de génération de contrôleur ; `selection-tsi.yaml` liste la famille entière avec `raison` par entrée).
- SG1.2 · Tâche 1.2 [À FAIRE] : **Correction 2** — §7 : nouvelle **table de Karnaugh 4 variables (F, L, S, B)** — lignes F,L et colonnes S,B en ordre de Gray (16 cases, X pour les impossibilités L=0∧S=1 et L=0∧B=1), règles dérivées réécrites (le clone overlay sur branche non-défaut = cas explicite), §6.D5/D6 : `cmdr-clone` vérifie la branche courante (checkout `ecosystem/tsi-traktor-s4mk2` si divergence locale propre, jamais d'écrasement sale).
- SG1.3 · Tâche 1.3 [À FAIRE] : **Correction 3** — jeton : canal UNIQUE `GH_TOKEN` (variable d'environnement, jamais dans le MD/fichiers/commandes — aligné règle KO-L009 de l'écosystème, citée) ; `gh auth token` = repli si `gh` authentifié ; manifeste : `bootstrap` RÉÉCRIT les SHA (`commit_epingle`) à chaque exécution (relevés par `git rev-parse`/`ls-remote`) — le manifeste n'est jamais périmé ; valeurs d'exemple = SHA réels relevés (provenance `ls-remote`, date).
- SG1.4 · Tâche 1.4 [À FAIRE] : livraison — MD corrigé in place + copie `download/ghorg-to-ecosysteme-v2.md`.

### G2 — Adaptation du MD à $ECO-LEON [~4 k#token]
- SG2.1 · Tâche 2.1 [À FAIRE] : en-tête enrichi (cible, langue FR — règle d'or n°6 de l'écosystème citée), règles d'or de l'écosystème citées là où pertinentes (n°4 clone le dépôt / n°6 français / n°8 PM INSTALL installe les skills jamais les PMs / KO-L009 exposition d'identifiant), conventions (kebab-case, semver, worklog R5), glossaire alias-eco ($ECO-LEON, $FACON, $FACON2 — registre `@historique/@Alias/aliases.json`), chemins profil local `/home/z/my-project` + `~/GitHub` — le MD reste un prompt AUTONOME (intégrité structurelle préservée, R2 addition pure).

### G3 — Tests $FACON2 fonctionnels du MD [~5 k#token]
- SG3.1 · Tâche 3.1 [À FAIRE] : batterie T1-T6 — T1 Karnaugh 4 var (16 cases, Gray, X, règles ↔ table) ; T2 commandes ghorg vs README officiel (flags déjà validés en analyse, re-vérifiés) ; T3 YAML manifeste parse + SHA réels (re-jeu `ls-remote`) ; T4 scan secrets (motifs nus uniquement, 0 valeur) ; T5 answer key (chaque correction vérifiable) ; T6 simulation à blanc D1/D4/D5 (commandes citées existent et enchaînent logiquement). Optimisations identifiées appliquées si risque nul (P2).

### G4 — Analyse intégration GHORG/CMDR + suggestions multiples [~6 k#token]
- SG4.1 · Tâche 4.1 [À FAIRE] : rapport `download/rapport-integration-ghorg-cmdr-ecosysteme.md` — analyse (état, synergie famille TSI : preset task45 + LEON TSI EDITEUR v11 existants au dépôt) + **≥ 6 suggestions** numérotées avec justification/risque/effet.

### G5 — Clôture [~3 k#token]
- SG5.1 · Tâche 5.1 [À FAIRE] : worklog Task 50 (dépôt + miroir profil) + statuts plan + bloc récapitulatif final au chat. Pas de push (KO-L009 point 5).

**Budget total estimé : ~26 k#token** + contingence ×2-3.

## Answer key (décisions D101-D107 — criterion + verification exécutable)

- **D101** — Périmètre famille TSI complète = les 7 entrées KB nommées + agent, sans restriction MK2
  - criterion: le MD cite les 7 skills de la famille TSI et l'agent ; « famille TSI complète » apparaît au §1/§6.B.3 ; plus aucune restriction « S4 MK2 » comme unique périmètre
  - verification: `grep -c "famille TSI complète" upload/ghorg-to-ecosysteme.md` ≥ 2 ; les 7 noms présents ; `grep "MK2" | grep -v "MK2 ET MK3\|S4 MK2 et"` = 0 restriction résiduelle
- **D102** — Karnaugh 4 variables (F, L, S, B) complète et cohérente
  - criterion: table 16 cases en ordre de Gray, X aux impossibilités, règles dérivées couvrant la branche overlay, §6.D5/D6 mis à jour (checkout branche)
  - verification: lecture croisée table↔règles (chaque combinaison critique → action unique) ; `grep -c "branche courante" ≥ 3`
- **D103** — Jeton canal unique + manifeste réécrit par bootstrap + SHA réels
  - criterion: GH_TOKEN unique canal (var env), KO-L009 cité, 0 valeur de jeton dans le MD, bootstrap réécrit les SHA, SHA réels avec provenance
  - verification: `grep -E "github_pat_[A-Za-z0-9_]{20,}" upload/…` = 0 ; `git ls-remote` re-jeu = SHA du MD ; `grep "réécriv" manifeste` présent
- **D104** — Adaptation écosystème : règles d'or citées (n°4, n°6, n°8, KO-L009), glossaire alias, chemins profil
  - verification: `grep -c "règle d'or n°" ≥ 3` ; `$ECO-LEON` défini ; `/home/z/my-project` présent
- **D105** — Batterie T1-T6 PASS (0 échec), optimisations P2 appliquées
  - verification: sorties consignées au worklog + rapport
- **D106** — ≥ 6 suggestions distinctes justifiées dans le rapport
  - verification: `grep -c "^## Suggestion" rapport` ≥ 6
- **D107** — Livrables download/ + worklog + aucun push
  - verification: `ls download/ghorg-to-ecosysteme-v2.md download/rapport-integration-*.md` ; `git status` dépôt = commits locaux non poussés

## Statuts (état disque — règle d'or n°5, mis à jour à chaque groupe)

- G1 [TERMINÉ 4/4 SG] · G2 [TERMINÉ 1/1 SG] · G3 [TERMINÉ 1/1 SG — batterie T1-T6 PASS] · G4 [TERMINÉ 1/1 SG — 8 suggestions] · G5 [TERMINÉ 1/1 SG]

---

Verdict E8 : PASS (P1-P5 exécutés via `skills/gen-plan/scripts/check_plan_protocol.py` — 5/5 checks : plan présent, answer key 7 décisions vérifiables, worklog R5 cite le plan, PLAN-AFFICHE dans l'entrée, verdict + horodatages couplés — Horodatage vérifié : 2026-11-04T21:05:00+01:00)
