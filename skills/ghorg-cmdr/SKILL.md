---
name: ghorg-cmdr
version: 1.1.0
category: ecosystem
language: fr
tags:
  - ghorg
  - cmdr
  - integration
  - tsi
  - idempotence
  - ecosystem
description: >
  Skill de procédure d'intégration GHORG + CMDR EDITOR dans l'écosystème (Task 51 — exécution
  du PM ghorg-to-ecosysteme.md v1.1). Trois blocs : (1) GHORG local — fork bigleon2/ghorg (repli :
  source gabrie30/ghorg tant que le fork n'existe pas), build conditionnel par marqueur .ghorg-commit,
  remote upstream, PATH ; (2) clone CMDR — table de Karnaugh 4 variables F/L/S/B (fork existant, clone
  local, clone sale, branche overlay ecosystem/tsi-traktor-s4mk2), règles 1-6, GHORG autorisé seulement
  règles 1/2/5, jamais de reclone sur un clone overlay propre, repli git documenté sans jeton (KO-L009) ;
  (3) superposition famille TSI complète — copie unilatérale KNOWLEDGE → cmdr/ecosystem/ comparée par
  SHA-256, SOURCE.md régénéré, suppression seulement si listée au SOURCE.md précédent, 0 fichier touché
  hors ecosystem/. Scripts : scripts/ecosystem/{bootstrap,ghorg-install,cmdr-clone,cmdr-overlay-sync}.py
  (stdlib, idempotents — le 2e passage ne produit aucun changement git). État GHORG du dépôt : collection
  skills/@GHORG-ecosysteme/ (manifest.yaml + selection-tsi.yaml + ghorg/ — déplacement R4 Task 70 G3 depuis
  ecosystem/, directive propriétaire ; la branche overlay CMDR ecosystem/tsi-traktor-s4mk2 et le dossier
  cmdr/ecosystem/ du clone restent inchangés). Déclencher pour intégrer ou
  mettre à jour ghorg/cmdr dans l'écosystème, rejouer la superposition TSI, diagnostiquer un état de
  clone (F/L/S/B), ou re-sceller le manifeste skills/@GHORG-ecosysteme/manifest.yaml.
dependencies:
  - skill: gen-plan
    version: ">=3.34.0"
    used_at: "plans de mission multi-étapes (l'exécution complète est une tâche planifiée)"
read_when:
  - Déclencher quand la demande concerne : intégration ghorg/cmdr, superposition TSI vers CMDR, Karnaugh F/L/S/B, manifeste ecosystem, reclone cmdr-editor-fork
  - Déclencher si la demande mentionne : ghorg, cmdr editor, bigleon2/ghorg, bigleon2/cmdr, superposition TSI, bootstrap écosystème
  - Ne pas déclencher hors de ce périmètre (convention protocole — la famille TSI de conception/validation reste routée par orchestrateur-tsi).
---

## §0 — Contexte Système (SHARED v1.7.34)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



# ghorg-cmdr — Intégration GHORG + CMDR EDITOR (procédure)

## 1. Mission

Intégrer l'outil GHORG (cloneurs de dépôts GitHub en masse) et l'application CMDR EDITOR (éditeur
Windows de fichiers TSI pour Traktor) à l'écosystème, puis propager la **famille TSI complète**
(7 skills + 2 agents — MK2 ET MK3, sans restriction) dans un dossier dédié `ecosystem/` du clone CMDR,
sans casser la synchronisation avec le dépôt d'origine.

## 2. Blocs (scripts scripts/ecosystem/, tous idempotents)

| Bloc | Script | Rôle |
|---|---|---|
| D4 | `ghorg-install.py` | GHORG local : clone fork (repli : source), remote upstream, build conditionnel (marqueur `.ghorg-commit` = SHA), PATH |
| D5 | `cmdr-clone.py` | Clone CMDR : **Karnaugh F/L/S/B** — 4 variables relevées AVANT action, règles 1-6, GHORG seulement règles 1/2/5 |
| D6 | `cmdr-overlay-sync.py` | Superposition TSI : copie unilatérale SHA-256, SOURCE.md, suppression seulement si listée avant |
| — | `bootstrap.py` | Enchaîne D4→D5→D6 et **re-scelle** `skills/@GHORG-ecosysteme/manifest.yaml` avec les SHA réels du jour |

## 3. Table de Karnaugh F/L/S/B (clone CMDR)

F = fork `bigleon2/cmdr` existe · L = clone local existe · S = clone local sale · B = branche courante
= overlay. Lignes F L, colonnes S B en ordre de Gray. Règles : 1 (F0L0 : fork puis clone — sans jeton :
repli source documenté) · 2 (F1L0 : clone) · 3 (F0L1 : STOP P0 orphelin — sauf origin = source, état
repli résoluble) · 4 (S=1 : ne rien modifier, alerter) · 5 (S0B0 : reclone ghorg puis checkout overlay)
· 6 (S0B1 : git ciblé SEUL — jamais de reclone ghorg sur un clone overlay propre).

## 4. Règles d'or appliquées

- **KO-L009 point 5** : jamais de push ni d'action distante sans GO propriétaire ; le jeton passe
  exclusivement par `GH_TOKEN`/`GHORG_GITHUB_TOKEN` (variables d'environnement, jamais en clair).
- **Règle d'or n°4** : les dépôts se lisent et se travaillent via des clones git locaux.
- **Règle d'or n°6** : français dans tous les livrables.
- **Sans jeton** (repli §4 du PM) : audit + fichiers prêts + commits locaux, aucune action distante.

## 5. État et reprise

Journal `~/GitHub/_outils/etat-ghorg-ecosysteme.json` (phases D1-D8 : à_faire | en_cours | terminé) —
lire au démarrage, ne pas refaire ce qui est terminé. Contrat d'idempotence : `bootstrap.py` exécuté
deux fois de suite → tout « déjà à jour », `git status --porcelain` vide, 0 nouveau commit, exit 0.
