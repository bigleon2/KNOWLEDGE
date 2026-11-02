# tsi-toolkit — Toolchain TSI Traktor Pro 3.11 / Kontrol S4 MK2

> **Version** : 1.0.0 · **Task 39 / G3** (session web-6058b3ba, 2026-11-02) ·
> Convergence $facon des éléments créés dans les discussions QWEN avec la
> famille TSI de l'écosystème KNOWLEDGE · CDC `download/cahier-des-charges-elements-tsi.md`.

## Origine (convergence)

| Élément des discussions | Convergé dans |
|---|---|
| TSI Editor S4 MK2 v7 (parser, Karnaugh, CRUD, virtual MIDI, convertisseurs) — L4/L5 | `tsi_toolkit/nixml.py`, `karnaugh.py`, `convertisseurs.py` |
| TSI Generator v7.7.9 + tsi-cli + static analyzer — L2 | `generateur.py`, `__main__.py` (CLI), `validateur.py` (interne) |
| csv_to_tsi_converter v1-v3 — L8 | `convertisseurs.py` (CSV `;` + hexa toléré) |
| HYPERCONTROL / Multi_SHIFT / couverture — L6/L7/L8 | `couverture.py` (matrice contrôles × couches, méthode multi-shift-architect) |
| Mapping Studio v11 (presets, DSL, audit auto-évolutif) — L9 | `studio.py` (l'UI React complète = extension documentée, non livrée) |
| Base Traktor Commands / enums CMDR — L3 | `data/commandes-traktor.json` (163 contrôles + 393 commandes extraits du mapping réel DJTT) |

**R4 (jamais de duplication)** : le décodage des blobs DIOM réels et le verdict
canonique complet délèguent aux arbitres de l'écosystème quand ils sont
présents (`pont` — `validateur.py`) ; en mode autonome, la toolchain se
limité à ses contrôles internes.

## Utilisation

```bash
cd tsi-toolkit
python3 -m tsi_toolkit --help                    # aide (français)
python3 -m tsi_toolkit inspect  <fichier.tsi>    # multi-format : canonique / réel DIOM / réglages
python3 -m tsi_toolkit generate <preset.json> <sortie.tsi>   # preset → TSI (anti-conflits actif)
python3 -m tsi_toolkit validate <fichier.tsi>    # interne + pont arbitre tsi-validator
python3 -m tsi_toolkit convert csv-tsi  <pseudo.csv> <sortie.tsi>   # Pseudo-TSI → TSI
python3 -m tsi_toolkit convert tsi-json  <fichier.tsi> <sortie.json>
python3 -m tsi_toolkit convert json-tsi  <modele.json> <sortie.tsi>
python3 -m tsi_toolkit coverage <fichier.tsi>    # matrice contrôles × couches (0 couche morte)
python3 -m tsi_toolkit presets                   # presets d'exemple
python3 -m tsi_toolkit studio    <sortie.tsi>    # scénario DSL → TSI + audit_log.md
python3 -m unittest tests.test_toolkit -v        # suite 20 tests (EF-01..08 + ENF)
```

## Formats pris en charge

1. **Canonique écosystème** (génération/validation) : `NISYSTEM`/`NIXML` >
   `DEVICE` > `MAPPINGS` > `MAPPING` [`MODIFIER` M1-M4 binaires] [`MIDI`]
   [`LED`] — format des échantillons dorés `tsi-validator`.
2. **Réel Traktor (mapping contrôleur)** : `NIXML` > `TraktorSettings` >
   `Entry[Name='DeviceIO.Config.Controller']` (blob DIOM base64) — inspection
   via pont `analyse-doc-s4mk2` (DJTT v2.1.0 : DCBM 5 626, 345 conditions).
3. **Réel Traktor (réglages complets)** : centaines d'`Entry` — le mapping
   contrôleur embarqué est isolé automatiquement.

## Contraintes respectées

- **Python stdlib uniquement** (ENF-01) — aucun `pip install` ;
- **Idempotence ×2** (ENF-02/R6) : un preset produit toujours le même XML
  byte-identique ; l'audit_log du studio croît à chaque exécution
  (mécanisme auto-évolutif v11, voulu) ;
- **Performance** (ENF-03) : inspect DJTT 1,8 Mo ≈ 0,2 s ; validate ≈ 0,1 s ;
- **Portabilité** (ENF-07) : autonome hors écosystème (contrôles internes),
  intégrée dedans (ponts arbitres) ; empaquetée dans `zip-tsi.zip`
  (voir `construire-zip-tsi.py` à la racine du dépôt).

## Données

`data/commandes-traktor.json` — 163 contrôles + 393 commandes + 345
conditions, extraits mécaniquement du mapping réel DJTT v2.1.0
(référentiel G2 10/10), complétés par les manuels du Google Drive
« mapping TSI » (Traktor 3.9 Mapping FR/EN, Controller Editor S4 MK2 FR)
et la documentation NI Controller Manager.

## Fixtures réels de test

- `skills/tsi-validator/samples/echantillon-valide.tsi` (canonique, 15 mappings) ;
- mapping réel DJTT v2.1.0 (blob DIOM 1,8 Mo) ;
- TSI réels du propriétaire (Google Drive `mapping kontrol s4/` — 2021/2022).
