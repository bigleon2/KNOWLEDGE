# Rapport de validation des agents TSI sur le corpus réel (pré-calibration)

> **Task 7 G3** · Session web-eb6c8580 · 2026-10-30 · Généré via gen-plan v3.28.2 (plan amendé 1)
> **Objet** : verdicts BRUTS des 3 agents du trio TSI (v1.0.0) sur le corpus ZIP DJTT S4 MK2 v2.1.0 — état AVANT la calibration G4. Constat d'écart R-1 (« extension déclarative en cas d'écart avec un TSI réel — interface stable »), pas des bugs.
> **Corpus** : mapping principal (blob DIOM 1 352 130 o, 5 626 CMAI, Traktor 2.12.0) + 2 fichiers de préférences (Layouts, FX Settings — sans blob). Référentiel du format réel : `download/analyse-zip-djtt-s4mk2-v2.1.0.md` (G2).

## 1. tsi-validator v1.0.0 — `valider-tsi.py` × 3 fichiers

| Fichier | Verdict | Exit code | Erreurs (brutes) |
|---|---|---|---|
| Mapping principal (1,8 Mo) | **FAIL** | **1** | `[E1-structure] racine attendue NISYSTEM, trouvée 'NIXML'` · `[E1-structure] attribut VERSION manquant ou non entier sur NISYSTEM` · `[E1-structure] 0 éléments DEVICE (attendu 1)` |
| Extra/Layouts.tsi | **FAIL** | **1** | idem ×3 (E1-structure) |
| Extra/FX Settings.tsi | **FAIL** | **1** | idem ×3 (E1-structure) |

**Lecture** : comportement CONFORME à la spec v1.0.0 (format projet NISYSTEM/DEVICE/MAPPINGS — Traktor Pro 3.11 / S4 MK3). L'échec E1 est la manifestation exacte de l'écart R-1 : le format réel (NIXML + blob DIOM binaire, Traktor 2.12.0 / S4 MK2) n'est pas le format projet. **Aucun bug de l'agent** : parsing XML sain, catégorisation E1 correcte, verdict + exit code cohérents (FAIL → 1). Nota : les 2 fichiers de préférences échouent de façon identique alors qu'ils ne sont PAS des mappings — le validateur ne distingue pas « fichier de préférences Traktor » d'un « mapping au format inattendu » (constat de calibration : détection de nature de fichier à ajouter côté format réel).

## 2. midi-doc-expert v1.0.0 — `generer-doc-midi.py` sur le mapping principal

| Aspect | Constat brut |
|---|---|
| Appel | `generer-doc-midi.py <mapping principal> --outdir …` |
| Verdict | **Échec structurel — exception non gérée** : `AttributeError: 'NoneType' object has no attribute 'findall'` (`dev.findall("MAPPINGS/MAPPING")` avec `dev=None` — l'élément `DEVICE` est absent du NIXML) |
| Exit code | **1** (crash Python) |
| Sortie | aucune (0 fichier généré) |

**Lecture** : échec structurel attendu (le générateur cherche `NISYSTEM/DEVICE/MAPPINGS` — absents du format réel). Constat de calibration : l'échec devrait être **un message catégorisé + exit code propre** (pas une traceback) — la v1.1.0 transforme ce crash en diagnostic E1-structure réutilisé du validateur (interface stable, échecs honnêtes).

## 3. tsi-architect v1.0.0 — audit du référentiel `references/referentiel-structures-tsi.md`

| Dimension du référentiel (spec) | Réalité du corpus | Écart |
|---|---|---|
| Squelette `NISYSTEM VERSION` → `DEVICE` → `MAPPINGS COUNT` → `MAPPING` (+ `MODIFIER`, `MIDI`, `LED`) | `NIXML` → `TraktorSettings/Entry` → blob `DIOM` → trames `CMAI/CMAD/DCBM/DCDT` | **total** (aucun élément commun) |
| Ordre d'assemblage : sources modifiers → mappings conditionnés → base → LED | Réel : 345 conditions DCDT (125 DDCI + 220 DDCO) et commandes `_(Mod)` — doctrine IDENTIQUE, encodage différent | doctrine convergente, encodage ≠ |
| Patterns types (couche SHIFT, double couche, encodeur 2 sens) | Réel : Left/Right.Shift parmi les conditions, 5 626 assignations à forte densité de modifiers | concept applicable, représentation ≠ |
| Clause R-1 (§ en-tête : « extension déclarative si écart avec un TSI réel ») | écart AVÉRÉ sur ce corpus | **clause mobilisée — cadre canonique de G4** |

**Lecture** : le référentiel est **cohérent pour le format projet** (provenance IvanZ 2014 + NI Controller Manager + mappings S4 MK3 documentés) et porte déjà la clause R-1. L'écart constaté est un écart de **génération de format** (Traktor 2.x binaire vs Pro 3.x XML projet), pas une incohérence interne. **Périmètre G4** (per directive) : calibration de midi-doc-expert + tsi-validator uniquement — le référentiel architect reste au format projet ; son extension au format réel est une décision propriétaire future (non sollicitée).

## 4. Self-tests golden (non-régression format spec)

| Agent | Self-test | Résultat |
|---|---|---|
| tsi-validator | `--self-test` (échantillon valide → PASS, invalide → FAIL, catégories E1-E8) | **PASS** (rc 0, catégories E1-E8 déclenchées) |
| midi-doc-expert | `--self-test` (9 sections, couverture 100 %, 15 mappings) | **PASS** (rc 0) |

Les 2 agents restent **verts sur le format spec** — la calibration G4 (v1.1.0) devra préserver ces self-tests (extension, pas régression — R2 addition pure).

## 5. Synthèse : périmètre de calibration dérivé (entrée G4)

1. **Module décodeur format réel** (détenteur R4 : `skills/tsi-validator/scripts/decoder-format-reel.py`) : NIXML → `DeviceIO.Config.Controller` → Base64 → DIOM → hiérarchie stricte (DIOI/DEVS/DEVI/DDAT/DDIF/DDIV/DDIC/DDPT/DDDC/DDCB[CMAS/DCBM]/DVST), chaînes UTF-16-BE — socle commun aux 2 skills (structure interne normalisée).
2. **valider-tsi v1.1.0** : routage format spec ↔ format réel (détection racine) — règles E1-E8 **adaptées** au réel (structure trames, comptages déclarés≡marchés, liaison réf CMAI→DCBM, conditions DCDT), verdict exploitable sur le TSI principal (PASS ou FAIL sur erreurs réelles catégorisées) ; interface stable (verdict/exit/JSON) ; échec propre sur préférences (pas un mapping) ; self-test étendu (golden spec + échantillon réel).
3. **generer-doc-midi v1.1.0** : génération 9 sections MD+JSON depuis le format réel via le décodeur (couverture 100 % des assignations décodées), échec propre catégorisé (plus de traceback), dépendance YAML déclarée à tsi-validator (décodeur).
4. **Hors périmètre** (per directive) : tsi-architect (référentiel au format projet — extension = décision propriétaire) ; champs binaires CMAD (canal/message/numéro MIDI, modes) — non décodés (G2 §3.4, R-1 honnête).

---
*Artefacts : sorties brutes ci-dessus (rejouables) · `tmp/gdm-pre.txt` (traceback intégral generer-doc-midi) · référentiel G2 : `download/analyse-zip-djtt-s4mk2-v2.1.0.md`.*
