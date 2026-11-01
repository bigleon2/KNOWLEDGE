---
name: tsi-validator
version: 1.0.0
category: ecosystem
language: fr
tags:
  - tsi
  - validator
  - arbitre
  - traktor
  - midi
description: >-
  Skill-arbitre de validation mécanique des fichiers de mapping TSI (XML
  Traktor Pro 3.11) — vérifie structure (E1), comptage (E2), attributs (E3),
  plages MIDI (E4), doublons d'allocation (E5), LED (E6), couches mortes
  multi-shift (E7) et modifiers binaires (E8) ; rend un verdict PASS/FAIL
  mécanique avec rapport JSON et exit code. Bras exécutable :
  scripts/valider-tsi.py (Python stdlib, self-test embarqué sur échantillons
  golden samples/). Déclencher pour valider un .tsi, contrôler une architecture
  avant livraison (garde obligatoire du tandem tsi-architect), diagnostiquer
  les erreurs d'un mapping, ou fournir un verdict machine-à-machine à un
  autre élément de l'écosystème.
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "arbitre des hooks de phase du projet TSI (garde E9-E14)"
read_when:
  - Déclencher quand la demande concerne : valider ou diagnostiquer un fichier TSI, vérifier la conformité d'un mapping Traktor au schéma de référence, contrôler des allocations MIDI (doublons, plages), détecter une couche morte.
  - Déclencher si la demande mentionne : valider TSI, vérifier un mapping, tsi-validator, erreurs TSI, conflits MIDI, couche morte.
  - Ne pas déclencher pour concevoir une architecture (tsi-architect), la méthode des couches SHIFT (multi-shift-architect), ni la documentation (midi-doc-expert).
---

## §0 — Contexte Système (SHARED v1.7.17)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# tsi-validator — Arbitre mécanique de validation TSI

## §1 — Mission

Valider MÉCANIQUEMENT tout fichier TSI contre le schéma de référence (spec §5, règles R1-R8) et rendre un verdict exploitable machine-à-machine : `PASS` (exit 0) ou `FAIL` (exit 1) avec la liste complète des erreurs par catégorie. Le validateur ne modifie jamais les fichiers validés (arbitre, pas exécutant — anti-auto-certification). Il matérialise la règle E7-multishift de la méthode `multi-shift-architect` (aucune couche morte) et constitue la garde obligatoire du tandem `tsi-architect` (interface I-2 : jamais de mapping livré sans verdict PASS).

## §2 — Catégories d'erreur (E1-E8)

| Cat. | Règle | Exemple de détection |
|------|-------|----------------------|
| E1-structure | racine NISYSTEM + VERSION ; 1 DEVICE avec NAME, TYPE, IN_PORT, OUT_PORT, DECK_TARGET | DEVICE sans DECK_TARGET |
| E2-comptage | MAPPINGS COUNT = nombre de MAPPING enfants | COUNT=12 pour 8 mappings |
| E3-attributs | NAME unique non vide ; TYPE IN/OUT ; GROUP énuméré ; CONTROL non vide | GROUP="Deck Z" |
| E4-plages | CHANNEL 0-15 ; MESSAGE NOTE/CC/PB/PC ; NUMBER 0-127 ; MODE énuméré | NUMBER=200 |
| E5-doublon | unicité (CHANNEL, MESSAGE, NUMBER, conditions) en TYPE=IN | même note deux fois |
| E6-led | LED uniquement en TYPE=OUT ; NUMBER/ON/OFF 0-127 ; MODE=Output | LED dans un mapping IN |
| E7-multishift | toute condition Mx a une source CONTROL="Modifier x" | couche morte M2=1 |
| E8-modifier | M1..M8 binaires 0/1 | M3="5" |

## §3 — Usage

```bash
python3 skills/tsi-validator/scripts/valider-tsi.py <fichier.tsi>          # verdict + erreurs
python3 skills/tsi-validator/scripts/valider-tsi.py <fichier.tsi> --json  # rapport JSON
python3 skills/tsi-validator/scripts/valider-tsi.py --self-test           # golden samples
```

Sortie : `VERDICT : PASS|FAIL` en dernière ligne ; exit code 0 ssi PASS. Rapport JSON : liste `erreurs` (categorie, detail) + `stats` (mappings, in, out, couches_logiques). Extension déclarative (R-1) : toute divergence constatée avec un TSI réel s'ajoute comme nouvelle règle — l'interface (verdict/exit code/JSON) reste stable.

## §4 — Échantillons de référence (golden samples)

- `samples/echantillon-valide.tsi` — Freeze Mode S4 MK3 (15 mappings, règle R1-R8 conformes) : DOIT rendre PASS.
- `samples/echantillon-invalide.tsi` — porte au moins une violation de chaque catégorie E1-E8 : DOIT rendre FAIL avec les 8 catégories déclenchées (vérifié par --self-test).

## §5 — Relations

| Avec | Nature |
|------|--------|
| `tsi-architect` (skill + agent) | Garde obligatoire des livraisons d'architecture (I-2) |
| `multi-shift-architect` | Matérialisation mécanique de la règle d'aucune-couche-morte (I-3) |
| `midi-doc-expert` | La documentation n'est générée que sur des TSI validés (entrée saine) |
| `gen-plan` / `correct-work` | Arbitre mobilisable par les hooks de phase (verdict machine) |
