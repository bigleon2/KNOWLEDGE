# Rapport de calibration du trio TSI — midi-doc-expert + tsi-validator v1.1.0 (format réel)

> **Task 7 G4** · Session web-eb6c8580 · 2026-10-30 · Généré via gen-plan v3.28.2 (plan amendé 1)
> **Directive** : « fais la calibration de midi-doc-expert et tsi-validator » (corpus ZIP DJTT Kontrol S4 MK2 v2.1.0 — mapping TSI réel tiers).
> **Cadre** : clause R-1 du SKILL tsi-validator (« extension déclarative en cas d'écart avec un TSI réel — interface stable ») + semver MINOR (addition pure R2). Périmètre : midi-doc-expert + tsi-validator **uniquement** (tsi-architect hors calibration per directive — référentiel au format projet, extension = décision propriétaire future). **Hôte seul** (trio hors dépôt/KB — statu quo Task 6-G2).

## 1. Verdicts post-calibration (re-validation sur corpus réel)

| Agent | Avant (v1.0.0 — G3) | Après (v1.1.0) |
|---|---|---|
| **tsi-validator** sur mapping principal (1,8 Mo) | FAIL E1-structure ×3 (« racine attendue NISYSTEM, trouvée NIXML ») | **PASS — 0 erreur, 5 626 mappings** (format `reel`, device « Traktor.Kontrol S4MK2.Default », Traktor 2.12.0) — exit 0 |
| **tsi-validator** sur Layouts.tsi / FX Settings.tsi | FAIL E1 ×3 (idem) | **FAIL propre catégorisé** ×1 : « fichier de préférences Traktor (NIXML sans DeviceIO.Config.Controller, 39/96 Entry) — aucun mapping à valider » — exit 1, zéro traceback |
| **midi-doc-expert** sur mapping principal | **Crash** `AttributeError` (dev=None), exit 1, traceback | **PASS — MD + JSON générés** (`scripts/zip-tsi/doc-generee/`) : 9 sections, couverture **5 626/5 626 (100 %)**, déterministe |
| **midi-doc-expert** sur préférences | (non testé — crash attendu) | **Échec structurel catégorisé propre** : « ERREUR STRUCTURELLE : fichier de préférences Traktor… — VERDICT : FAIL », exit 1, zéro traceback |

**Verdict final D008 : PASS** — parsing réussi sur le TSI principal (aucune erreur de format), verdict exploitable, documentation générée à couverture 100 %.

## 2. Module décodeur R4 — `skills/tsi-validator/scripts/decoder-format-reel.py`

Détenteur R4 du format réel (source unique, réutilisée par les 2 skills) :
- Détection de nature : `spec` (NISYSTEM) · `reel-mapping` (NIXML + DeviceIO.Config.Controller) · `reel-preferences` (NIXML sans) · `xml-invalide` · `inconnu`.
- Décodage DIOM big-endian intégral (hiérarchie DIOI/DEVS/DEVI/DDAT → DDIF/DDIV/DDIC/DDPT/DDDC/DDCB/DVST, chaînes UTF-16-BE) — référentiel G2.
- Sortie normalisée : device, traktor_version, cmdr_metadata, titre, conditions (345 DCDT), contrôles (163), assignations (5 626 : ordinal, drapeau, réf, commande, contrôle), métriques de cohérence.
- `--self-test` : **PASS** (réel → 5626 CMAI/163 contrôles/345 conditions/Traktor 2.12.0 + golden spec → spec).
- Champ **non décodé assumé (R-1)** : binaires CMAD (canal/message/numéro MIDI, modes, conditions par assignation).

## 3. tsi-validator v1.1.0 — routage + règles adaptées

- **Routage automatique** : racine `NIXML` → validation format réel (via décodeur R4) ; sinon chemin spec inchangé (règles E1-E8 strictes sur NISYSTEM/DEVICE/MAPPINGS — non-régression prouvée par self-test golden).
- **Règles adaptées au réel** : E1-structure (hiérarchie DIOM : device, DDCB, assignations) · E2-comptage (CMAS/DCBM déclarés ≡ marchés) · E3-attributs (chaque CMAI porte sa CMAD ; chaque DCBM porte un nom de contrôle) · E5-doublon (ids DCBM uniques). **Non applicables (R-1, signalés dans `stats.non_applicables_R1`)** : E4-plages, E6-led, E7-multishift, E8-modifier.
- **Interface stable** : verdict PASS/FAIL, exit 0/1/2, rapport JSON `{fichier, verdict, erreurs[{categorie, detail}], stats}` inchangé — champ `format` additif.
- **Self-test étendu** : golden spec (valide→PASS, invalide→FAIL E1-E8) + échantillon réel → **PASS** (format reel, 5 626 mappings, Traktor 2.12.0).

## 4. midi-doc-expert v1.1.0 — génération format réel

- **Génération depuis le réel** via le décodeur R4 (dépendance YAML déclarée : `tsi-validator >=1.1.0`, used_at décodeur) : 9 sections MD + JSON, déterministe (ENF-05), couverture 100 % des assignations (tableau complet commande↔contrôle↔réf↔ordinal).
- **Contenu adapté** : conditions/modifiers DCDT (couches Shift), mode Freeze documenté (croisement G2/VLM), top commandes (macros `_(Mod)`), retours LED, annexes R-1 (champs MIDI binaires non décodés — signalé dans le document).
- **Échec structurel catégorisé** (`StructureError`) : préférences Traktor et formats inconnus → message propre + exit 1, **plus de traceback** (constat G3 résorbé).
- **Self-test étendu** : golden spec (15 mappings, 100 %) + échantillon réel (5 626, 100 %) → **PASS**.

## 5. Échantillon réel + versions

- `skills/tsi-validator/samples/echantillon-reel-djtt-s4mk2.tsi` (1,8 Mo — mapping principal du ZIP, **hôte seul**, hors dépôt) : ancre des self-tests étendus.
- **Versions v1.0.0 → v1.1.0 ×2** (MINOR, addition pure R2) : frontmatter, description enrichie avec parcimonie (format réel NIXML/Traktor 2.x), dépendance YAML (midi-doc-expert → tsi-validator décodeur), notes evals.json ×2.
- Non-régression **voie M** : rejeu `check-triggers-replay` host — **47/47 skills au score maximal, verdict PASS, trio 6/6 ×3 inchangé, dérivées voie-M-seule = les 5 héritées Task 30 (aucune nouvelle)**.

## 6. Ce qui n'a PAS changé (garde R2)

- Règles E1-E8 sur le format spec : strictement inchangées (self-test golden identique).
- Le référentiel tsi-architect : inchangé (format projet — extension au réel hors périmètre directive).
- Les 5 vetos exclusifs doctrinaux du trio (Task 6-G2) : inchangés.
- Le workflow aval PDF (skill plateforme pdf) : inchangé.

---
*Artefacts : decoder-format-reel.py · valider-tsi.py v1.1.0 · generer-doc-midi.py v1.1.0 · doc générée `scripts/zip-tsi/doc-generee/DJTT…-doc.{md,json}` · §6bis ligne Task 7-G4 (@historique). Précédents : rapport G3 (constats pré-calibration) · analyse G2 (référentiel format réel).*
