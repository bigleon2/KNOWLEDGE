---
name: tsi-validator
version: 1.3.0
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
  Traktor Pro 3.11, contrôleur Kontrol S4 MK2) — vérifie structure (E1), comptage (E2), attributs (E3),
  plages MIDI (E4), doublons d'allocation (E5), LED (E6), couches mortes
  multi-shift (E7) et modifiers binaires (E8) ; rend un verdict
  PASS/FAIL/PRÉFÉRENCES mécanique avec rapport JSON et exit code (v1.3.0 : F1
  verdict PRÉFÉRENCES pour les TSI de préférences sans Entry contrôleur, F2
  support multi-devices — itération de toutes les trames DEVI de DEVS, erreurs
  qualifiées par device). Bras exécutable :
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

## §0 — Contexte Système (SHARED v1.7.24)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.

# tsi-validator — Arbitre mécanique de validation TSI

## §1 — Mission

Valider MÉCANIQUEMENT tout fichier TSI et rendre un verdict exploitable machine-à-machine : `PASS` (exit 0), `FAIL` (exit 1) ou `PRÉFÉRENCES` (exit 2 — v1.3.0 F1 : TSI de préférences hors périmètre mapping) avec la liste complète des erreurs par catégorie. Le validateur est BI-RACINE (v1.2.0 — pendante Task 33 n°1 résorbée) : racine `NISYSTEM` (format déclaratif des échantillons écosystème — règles E1-E8 complètes sur le XML) ou racine `NIXML` (format réel Traktor Pro 3.11, constats Task 33 sur DJTT v2.1.0 et DREW) — pour la voie réelle, validation structurelle du blob DIOM embarqué (Entry `DeviceIO.Config.Controller@Value` base64 : magique DIOM, hiérarchie DEVS→DEVI→DDAT→DDDC→DDCB→CMAS→CMAI/CMAD + DCBM, cohérence des comptes en E2, devices en E3 — MULTI-DEVICES supporté depuis v1.3.0 F2 : toutes les trames DEVI de DEVS sont itérées et validées individuellement, erreurs qualifiées « device i : », `stats.devices` = liste des noms) ; un NIXML structurellement sain dont l'Entry contrôleur est absente est un fichier de préférences → verdict `PRÉFÉRENCES`, aucune erreur E1-E8 (fichier de référence : cmdr `tests/keyboard/keyboard__timecode_mode…tsi` ; multi-devices de référence : cmdr `tests/traktor-ready/PIONEER_DDJ-T1_V103.tsi`, 2 devices Pioneer.DDJ-T1 + Generic MIDI). La sémantique E4-E8 du contenu binaire reste du ressort du moteur `analyse-doc-s4mk2` (délégation R4, jamais dupliquer). Le validateur ne modifie jamais les fichiers validés (arbitre, pas exécutant — anti-auto-certification). Il matérialise la règle E7-multishift de la méthode `multi-shift-architect` (aucune couche morte) et constitue la garde obligatoire du tandem `tsi-architect` (interface I-2 : jamais de mapping livré sans verdict PASS).

## §2 — Catégories d'erreur (E1-E8)

| Cat. | Règle | Exemple de détection |
|------|-------|----------------------|
| E1-structure | BI-RACINE : racine `NISYSTEM` (déclaratif) + VERSION + 1 DEVICE (NAME, TYPE, IN_PORT, OUT_PORT, DECK_TARGET) — ou racine `NIXML` (réel) + Entry contrôleur + blob base64 DIOM décodable + hiérarchie de trames ; TSI de préférences (Entry contrôleur absente, NIXML sain) → verdict `PRÉFÉRENCES` (exit 2, v1.3.0 F1 — aucune erreur E1-E8) | DEVICE sans DECK_TARGET ; blob base64 illisible |
| E2-comptage | Déclaratif : MAPPINGS COUNT = MAPPING enfants. Réel : comptes déclarés == lus (DDCI/DDCO, CMAI/CMAD embarqués, DCBM) — PAR DEVICE (v1.3.0 F2, qualifié « device i : ») | COUNT=12 pour 8 mappings ; device 1 : CMAS : 2 CMAI déclarés, 1 lu |
| E3-attributs | NAME unique non vide ; TYPE IN/OUT ; GROUP énuméré ; CONTROL non vide ; réel : toutes les trames DEVI de DEVS itérées (multi-devices, v1.3.0 F2) | GROUP="Deck Z" ; DEVS déclare 3 devices, 2 trames lues |
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

Sortie : `VERDICT : PASS|FAIL|PRÉFÉRENCES` en dernière ligne ; exit code 0 ssi tous PASS, 1 si au moins un FAIL, 2 si aucun FAIL mais au moins un PRÉFÉRENCES (v1.3.0 — l'usage invalide passe de 2 à 3) ; en mode `--json`, le rapport JSON est sur stdout et le verdict sur stderr (JSON parseable en pipe). Rapport JSON : liste `erreurs` (categorie, detail) + `stats` (mappings, in, out, couches_logiques ; voie réelle : format, devices [liste des noms — multi-devices F2], cmai/dcbm en cumul, device en mono-device ; préférences : `preferences: true` + note). Extension déclarative (R-1) : toute divergence constatée avec un TSI réel s'ajoute comme nouvelle règle — l'interface (verdict/exit code/JSON) reste stable.

## §4 — Échantillons de référence (golden samples)

- `samples/echantillon-valide.tsi` — Freeze Mode S4 MK2 (15 mappings, règles R1-R8 conformes ; pattern Shift+Loop In corroboré par le réel DJTT S4 MK2 v2.1.0) : DOIT rendre PASS.
- `samples/echantillon-invalide.tsi` — porte au moins une violation de chaque catégorie E1-E8 : DOIT rendre FAIL avec les 8 catégories déclenchées (vérifié par --self-test).
- Voie réelle NIXML : fixtures DIOM minimales générées à la volée par le self-test (tempfile — valide → PASS avec device/CMAI ; incohérence de comptage CMAS → FAIL E2 ; préférences → PRÉFÉRENCES ; multi-devices 2 devices → PASS avec stats.devices == 2 entrées), aucune dépendance obligatoire à des fichiers externes — le cas préférences utilise le fichier réel cmdr `tests/keyboard/keyboard__timecode_mode…tsi` lorsqu'il est présent (lu en place, jamais copié dans le skill), sinon une fixture synthétique équivalente.

## §5 — Relations

| Avec | Nature |
|------|--------|
| `tsi-architect` (skill + agent) | Garde obligatoire des livraisons d'architecture (I-2) |
| `multi-shift-architect` | Matérialisation mécanique de la règle d'aucune-couche-morte (I-3) |
| `midi-doc-expert` | La documentation n'est générée que sur des TSI validés (entrée saine) |
| `gen-plan` / `correct-work` | Arbitre mobilisable par les hooks de phase (verdict machine) |
