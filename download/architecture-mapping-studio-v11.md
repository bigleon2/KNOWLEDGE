# Traktor Mapping Studio v11 — Architecture $facon outillée

> **Version** : 11.0.0-toolkited · **Task 39 / G3** · Réalisation outillée de
> la vision « Mapping Studio v11 » (discussion L9 « Optimisation Projet
> Multifonctionnel », PDF `_Objectifs de la v11.pdf`).
> **Décision CDC** : l'interface React complète reste une **extension
> documentée** (skill fullstack-dev sur demande dédiée) — la fonctionnalité
> visée (créer des mappings par presets/DSL avec auto-audit) est livrée
> par le module `studio` de la toolchain.

## Vision d'origine (L9, fidèle)

Centraliser la création de mappings Traktor : interface modulaire, éditeur
DSL, système de presets, **mécanisme auto-évolutif** (à chaque exécution,
un `audit_log.md` liste les écarts et alimente l'itération suivante).

## Réalisation outillée (v11-toolkited)

| Brique v11 | Réalisation livrée |
|---|---|
| Interface modulaire | CLI `python3 -m tsi_toolkit studio` (7 sous-commandes cohérentes) |
| Éditeur DSL | `studio.compiler_dsl()` — lignes `contrôle -> fonction [couche]`, couches BASE/M1-M4 |
| Presets | `examples/preset-freeze-mode.json` + `studio.appliquer_preset()` (bloc/deck/paramètre) |
| Auto-audit | `studio.journaliser_audit()` — `audit_log.md` croît à chaque exécution (entrées horodatées : action, mappings, conflits) |
| Génération | `generateur.generer()` — anti-conflits intégré, TSI validé par l'arbitre |
| API presets | `python3 -m tsi_toolkit presets` (extensible — un preset = un JSON versionnable) |

## Scénario de référence (testé — EF-13)

```bash
cd tsi-toolkit
python3 -m tsi_toolkit studio output/scenario.tsi
# DSL → 5 mappings → TSI validé (arbitre PASS) + audit_log.md créé
```

DSL du scénario :
```
play -> Play/Pause
sync -> Sync [M1=1]
cue -> Cue/Set
loop_in -> Loop Set [M2=1]
flux -> Flux Mode
```

## Extension React (documentée, non livrée)

Sur demande dédiée : application fullstack (skill `fullstack-dev` de
l'écosystème) exposant les mêmes presets par API (`localhost:8000/presets`
dans la maquette L9) et consommant la toolchain comme moteur — le DSL et
les presets restant la source de vérité partagée.

## Héritage et écarts vs L9

- Les composants JSX/React maquettés en L9 (`DslEditor.jsx`, hooks
  `useMapping`/`usePresets`) ne sont pas portés tels quels (incomplets et
  hors périmètre CDC) — leurs RÔLES sont documentés ci-dessus ;
- `tableau_valeurs_cc_simple.csv` (L9) : les conflits de canal MIDI détectés
  alors sont couverts par l'anti-conflits `karnaugh.py` (détection
  mécanique, pas juste annotation) ;
- L'« audit log auto-évolutif » est la brique intégralement conservée —
  c'était l'apport le plus original de la v11.
