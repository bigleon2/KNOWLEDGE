---
name: multi-shift-architect
version: 1.1.0
category: ecosystem
language: fr
tags:
  - multi-shift
  - shift
  - couches
  - traktor
  - mapping
  - couverture
description: >-
  Skill méthode des couches SHIFT (multi-shift) pour mappings TSI Traktor /
  contrôleur S4 MK2 — détient la méthode de conception des architectures à
  couches : définition des couches logiques (BASE, SHIFT gauche, SHIFT droit,
  FREEZE via modifiers), matrices de couverture contrôles × couches (100 %
  couverts, 0 conflit d'allocation), transitions et activations complètes
  (aucune couche morte — matérialisée par la règle E7 de tsi-validator),
  patterns S4 MK2 (Freeze = SHIFT+LOOP IN — corroboré par le réel DJTT v2.1.0, hotcues étendus, encodeurs
  contextuels). Déclencher pour concevoir ou auditer la répartition des
  fonctions entre couches, vérifier une matrice de couverture, détecter les
  conflits entre couches, ou documenter les transitions d'états d'un mapping
  multi-shift.
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "conception des couches dans les plans d'architecture TSI"
read_when:
  - Déclencher quand la demande concerne : conception ou audit de couches SHIFT dans un mapping TSI, matrice de couverture contrôles × couches, détection de conflits entre couches, transitions/activations de couches, architecture multi-shift S4 MK2.
  - Déclencher si la demande mentionne : multi-shift, couche SHIFT, Freeze, modifier, couche morte, matrice de couverture, SHIFT+LOOP IN.
  - Ne pas déclencher pour la validation mécanique d'un TSI (tsi-validator), la conception structurelle générale (tsi-architect), ni la documentation (midi-doc-expert).
---

## §0 — Contexte Système (SHARED v1.7.24)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.

# multi-shift-architect — Méthode des couches SHIFT

## §1 — Mission

Détenir la méthode de conception et d'audit des **architectures multi-shift** : la répartition des fonctions d'un mapping TSI entre couches logiques superposées au même ensemble de contrôles physiques. Sur le S4 MK2, les couches de référence sont BASE (aucun modifier), SHIFT-G (SHIFT gauche maintenu), SHIFT-D (SHIFT droit maintenu) et FREEZE (modifier M1=1, activé par SHIFT+LOOP IN). La méthode garantit trois invariants vérifiables : **couverture 100 %** (chaque contrôle × couche a une affectation décidée, action ou inactif documenté « — »), **zéro conflit** (aucune fonction dupliquée sur deux contrôles d'une même couche ; aucun numéro MIDI partagé sans condition distincte — règle E5) et **transitions complètes** (chaque couche non-BASE a une activation et un retour documentés, aucune couche morte — règle E7 de `tsi-validator`, interface I-3).

## §2 — Méthode (4 étapes)

1. **Définir les couches** — nommer chaque couche, son modifier (ou son maintien physique), sa durée (momentanée vs toggle) et sa portée (deck gauche/droit/global). Une couche = un besoin d'expansion du contrôleur, jamais une redite.
2. **Dresser la matrice** — lignes = contrôles physiques (inventaire de l'agent `s4-hardware-expert`), colonnes = couches ; remplir CHAQUE cellule : fonction, ou « — » si inactif (l'inactivité documentée est une décision d'architecture, pas un oubli). Voir `references/matrice-couverture-s4-mk2.md` (matrice de référence Freeze Mode, machine-parsable).
3. **Arbitrer les conflits** — trois familles : doublon de fonction dans une couche (deux contrôles → même effet), chevauchement de couches simultanées (définir la priorité, ex. FREEZE prioritaire sur SHIFT-G), et collision MIDI inter-couches sur les mêmes numéros (autorisée SSI conditions de modifier distinctes — E5).
4. **Documenter les transitions** — pour chaque couche : activation (geste exact, ex. SHIFT gauche + LOOP IN), retour (relâche ou re-pression toggle), et comportement des LED (interface I-4 : ces transitions structurent les sections Activation/Désactivation du document `midi-doc-expert`).

## §3 — Patterns S4 MK2 de référence

- **Freeze Mode** (golden) : FREEZE en toggle sur M1, pads 1-8 passent de Hotcues à Slices, encodeur LOOP de Loop Size à Slice Size, LED Freeze en miroir de M1.
- **Hotcues étendus** : SHIFT-G + pad = Hotcue Delete (couche momentanée, priorité sous FREEZE).
- **Deck focusing** : SHIFT-D + PLAY = lecteur C/D (couche de redirection de deck) — documenter la non-interaction avec FREEZE.

## §4 — Relations

| Avec | Nature |
|------|--------|
| `tsi-validator` | La règle E7 (aucune couche morte) matérialise l'invariant de transitions complètes (I-3) |
| `midi-doc-expert` | Les couches et transitions structurent les sections Activation/Désactivation et Slices du document (I-4) |
| `tsi-architect` (skill + agent) | La matrice précède l'allocation MIDI (étape 1 de la méthode d'architecture) |
| `s4-hardware-expert` (agent) | Couches physiques (SHIFT gauche/droit) vs couches logiques (modifiers) |

## §5 — Références internes

- `references/matrice-couverture-s4-mk2.md` — matrice de couverture de référence (format machine-parsable, auditée par la batterie).
- `evals/evals.json` + `evals/trigger_evals.json` — cas de déclenchement (conception/audit de couches) et contrôles négatifs.
