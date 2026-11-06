---
name: midi-doc-expert
version: 1.2.0
category: ecosystem
language: fr
tags:
  - midi
  - documentation
  - traktor
  - s4-mk2
  - redacteur-technique
description: >-
  Skill de génération de documentation technique MIDI pour mappings TSI
  Traktor / contrôleur S4 MK2 — matérialise le persona du cahier des charges
  (Rédacteur Technique Expert en Mappings MIDI et Contrôleurs Audio :
  rédacteur technique + spécialiste MIDI + designer pédagogique). Génère la
  structure document type complète — Introduction, Vue d'ensemble,
  Activation/Désactivation, Contrôle des Slices, Réglages avancés, Tableau de
  Référence MIDI, Modes de sortie, États des LED, Annexes — aux formats
  Markdown et JSON natifs via scripts/generer-doc-midi.py (déterministe,
  couverture 100 % des mappings, vérifiable mécaniquement) ; PDF principal et
  PDF allégé en aval via le skill plateforme pdf (chaîne PyMuPDF/pymupdf4llm).
  Déclencher pour documenter un mapping TSI validé, produire un tableau de
  référence MIDI ou un état des LED, ou structurer une notice de contrôleur.
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "génération documentaire des projets TSI (phases de rédaction)"
read_when:
  - Déclencher quand la demande concerne : documenter un mapping TSI validé, générer un document technique MIDI (tableaux de référence MIDI, états LED), produire la notice d'un mode contrôleur (ex. Freeze Mode), exporter un mapping en Markdown/JSON/PDF.
  - Déclencher si la demande mentionne : documentation MIDI, tableau de référence MIDI, états LED, notice mapping, documenter le Freeze Mode, midi-doc-expert.
  - Ne pas déclencher pour valider un TSI (tsi-validator), concevoir une architecture (tsi-architect) ou arbitrer des couches (multi-shift-architect).
---

## §0 — Contexte Système (SHARED v1.7.23)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# midi-doc-expert — Génération de documentation technique MIDI

## §1 — Mission

Générer la **documentation technique** des mappings TSI validés, selon la structure type du cahier des charges S2 (persona : Rédacteur Technique Expert en Mappings MIDI et Contrôleurs Audio). Le skill consomme un `.tsi` **déjà validé** par `tsi-validator` (entrée saine), exploite les couches et transitions de `multi-shift-architect` (I-4) et l'inventaire de l'agent `s4-hardware-expert` (I-5), et produit deux formats natifs : **Markdown** (documentation principale, structure 9 sections, tableaux complets) et **JSON** (machine-readable : mappings, LED, couverture). Les formats **PDF principal et PDF allégé** sont produits en aval par le skill plateforme `pdf` (chaîne PyMuPDF/pymupdf4llm — I-7, hors périmètre de génération native).

## §2 — Structure document type (cahier des charges S2)

1. **Introduction** — objet, contrôleur, logiciel, vocabulaire MIDI défini à première occurrence (note, CC, canal, mode).
2. **Vue d'ensemble du mapping** — device, ports, cible de deck, effectifs (entrées/sorties), couches logiques.
3. **Activation / Désactivation** — geste d'activation de chaque couche (ex. Freeze : SHIFT+LOOP IN, toggle), retour, portée.
4. **Contrôle des Slices** — pads, notes, conditions de couche, comportement de rejeu des tranches.
5. **Réglages avancés** — encodeurs (CC, mode Increment/Decrement), paramètres continus.
6. **Tableau de Référence MIDI** — tableau exhaustif : affectation, groupe, commande, sens, message, canal, mode, couche — **couverture 100 % des mappings** (invariant vérifié mécaniquement).
7. **Modes de sortie** — sorties TYPE=OUT, restitution d'état, mode Output, valeurs ON/OFF.
8. **États des LED** — par LED : note, condition de couche, OFF par défaut, ON à l'état actif.
9. **Annexes** — statuts de calibration (R-1/R-2), sources (ENF-04), chaîne PDF aval.

## §3 — Méthodologie (6 phases du cahier des charges S2, outillées)

1. **Analyse du mapping** — extraction des données depuis le TSI (`scripts/generer-doc-midi.py` : devices, mappings, modifiers, LED).
2. **Extraction des données** — structure machine : mappings triés (sens, groupe, nom), conditions → couches, LED séparées.
3. **Structuration** — allocation aux 9 sections ; les mappings conditionnés alimentent Activation/Slices ; les CC alimentent Réglages avancés.
4. **Rédaction** — gabarit `references/gabarit-document.md` : paragraphes complets (3 phrases minimum), vocabulaire défini, persona designer pédagogique.
5. **Mise en forme** — génération MD + JSON déterministe (ENF-05 : aucun horodatage, tri stable → rejeu = no-op binaire).
6. **Validation** — vérification mécanique : 9 sections présentes, couverture 100 %, toutes les affectations dans le tableau (self-test embarqué).

## §4 — Usage

```bash
python3 skills/midi-doc-expert/scripts/generer-doc-midi.py <fichier.tsi> --outdir <dir> --titre "…"
python3 skills/midi-doc-expert/scripts/generer-doc-midi.py --self-test
```

Seuil de performance (ENF-02, audité par la batterie) : génération MD+JSON < 5 s par TSI de référence.

## §5 — Relations

| Avec | Nature |
|------|--------|
| `tsi-validator` | Entrée saine : documentation générée sur TSI validés uniquement |
| `multi-shift-architect` | Couches et transitions → sections Activation/Désactivation et Slices (I-4) |
| `s4-hardware-expert` (agent) | Inventaire hardware → Tableau de Référence MIDI et états LED (I-5) |
| `pdf` (skill plateforme) | Conversion PDF principal/allégé en aval (I-7 — PyMuPDF/pymupdf4llm) |

## §6 — Références internes

- `references/gabarit-document.md` — gabarit de rédaction (persona, règles de style, annexes types).
- `evals/evals.json` + `evals/trigger_evals.json` — cas de déclenchement (documentation MIDI) et contrôles négatifs.

## §7 — Historique

- **v1.2.0 (2026-11-04, Task 45)** : §5 rédigé par mode (Increment/Decrement = encodeur ; Toggle = bouton/commutation ; Direct = valeur absolue, verbe « attaque la commande générique » pour les MIDI Controls) ; §2 détecte et explique un bridge MIDI Controls (2 étages, IDs 850-873, convention looprituals 1-4 gauche / 5-8 droite) ; attribution Interaktiv Audio CC BY 4.0 portée dans le §2 ; JSON `generateur: midi-doc-expert v1.2.0`.
- **v1.1.0 (Task 33)** : conversion du périmètre MK3 → MK2 (S4 MK2 = contrôleur cible, MK3 = exemple d'Autre modèle) ; §0 re-normalisé SHARED v1.7.18.
- **v1.0.0** : création (cahier des charges S2, structure 9 sections, génération MD+JSON déterministe).
