---
name: analyse-doc-s4mk2
version: 1.0.0
category: ecosystem
language: fr
tags:
  - tsi
  - famille-tsi
  - agent-tsi
  - s4-mk2
  - djtt
  - analyse
  - documents-illustres
  - vue-partielle
  - vue-complete
  - referentiel-g2
description: >-
  Skill d'analyse des mappings TSI existants ET des documents illustrés qui
  leurs sont liés (Kontrol S4 MK2) — pipeline 6 étapes sur un ZIP ou un
  dossier : inventaire exhaustif Y COMPRIS les sous-dossiers (l'échantillon
  de référence DJTT v2.1.0 porte Extra/), classification des TSI (mapping
  DeviceIO.Config.Controller vs préférences-FX vs préférences-layouts),
  analyse du mapping au format réel DIOM (référentiel G2, erratum Task 33 :
  CMAD embarqué, 163 noms DCBM, 393 commandes), résumé des TSI compagnons
  (FX Settings : mode 4 unités FX ; Layouts : decks C/D Remix), documents
  illustrés (vue complète QuickGuide, vues partielles : photos d'éléments et
  vignettes du Manual) et vérification mécanique de la table de
  correspondance visuels↔contrôles (P1b, 22 noms) ; verdict PASS/FAIL +
  rapport JSON + batterie de tests $FACON2 11/11. Membre de la famille TSI,
  ORCHESTRÉ PAR agent-TSI. Déclencher pour analyser un ZIP de mapping
  DJTT/Traktor, relier des photos d'éléments du S4 MK2 à la vue complète,
  classifier les TSI d'un pack, ou obtenir les comptes d'un mapping réel.
dependencies: []
read_when:
  - Déclencher quand la demande concerne : analyser un ZIP/dossier de mapping TSI avec ses documents illustrés, relier des captures d'éléments du S4 MK2 à la vue d'ensemble (QuickGuide), classifier les TSI d'un pack (mapping/préférences), extraire les comptes d'un mapping réel (format DIOM), analyser les sous-dossiers d'un pack.
  - Déclencher si la demande mentionne : analyse-doc-s4mk2, documents illustrés, vue partielle, vue complète, QuickGuide, Manual, Freeze Mode Help, sous-dossiers du ZIP, DJTT, FX Settings, Layouts, correspondance visuels↔contrôles, comptes G2.
  - Ne pas déclencher pour concevoir une architecture (tsi-architect), valider la structure d'un TSI synthétique E1-E8 (tsi-validator), les couches SHIFT d'une architecture (multi-shift-architect), ni la documentation d'un mapping (midi-doc-expert).
---

## §0 — Contexte Système (SHARED v1.7.17)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# analyse-doc-s4mk2 — Analyse des mappings TSI réels et de leurs documents illustrés

## §1 — Mission

Analyser MÉCANIQUEMENT les mappings TSI **existants** (format réel Traktor, blob DIOM) **et les documents illustrés qui leurs sont liés** — captures des éléments du S4 MK2 et vue d'ensemble du contrôleur contenues dans le ZIP (y compris les **sous-dossiers**) — afin de produire : un inventaire exhaustif, une classification des TSI (mapping contre préférences), les comptes du mapping contre le référentiel G2, la **relation vues partielles ↔ vue complète** (photo d'élément → zone du QuickGuide → contrôles TSI exacts → fonction de mapping), et un verdict exploitable machine-à-machine (`PASS`/`FAIL`, exit code, JSON). Le skill ne modifie jamais l'échantillon analysé (lecture seule, rejets propres sans traceback).

**Orchestration** : membre de la famille TSI, **orchestré par `agent-TSI`** (matrice de routage : « analyser un mapping existant + ses documents illustrés » → ce skill). Hors orchestration, mobilisable directement en CLI (§3). Le skill assume la même discipline que les arbitres de la famille : jamais de verdict sans preuve mécanique, jamais d'interprétation non documentée (les hypothèses sont qualifiées comme telles — cf. §6).

## §2 — Pipeline (6 étapes)

| Étape | Action | Garde |
| --- | --- | --- |
| E1 | **Inventaire exhaustif** (ZIP ou dossier : tous membres, tailles, dossiers Y COMPRIS sous-dossiers) | 8 membres attendus sur l'échantillon de référence (6 fichiers + 2 dossiers) |
| E2 | **Classification** de chaque `.tsi` : `MAPPING` (Entry `DeviceIO.Config.Controller`) / `PRÉFÉRENCES-FX` (`Audio.FX.Selection`, `Status.4 FX Units`) / `PRÉFÉRENCES-LAYOUTS` (`Gui.Layouts2`, `Status.Select Layout`) / `PRÉFÉRENCES-GÉNÉRIQUES` / `ILLISIBLE` | 1/1/1 attendu sur la référence ; rejet propre des préférences par le moteur |
| E3 | **Analyse du mapping** (moteur `analyser_tsi_mk2.py`) : comptes + conformité référentiel G2 (10/10) + baseline stricte | erratum Task 33 intégré : 4960 lisibles / 666 illisibles / 393 commandes / 163 noms |
| E4 | **Résumé des compagnons** (Entries, clés structurantes) | FX Settings 96 Entry, Layouts 39 Entry attendus |
| E5 | **Documents illustrés** : dimensions (marqueurs JPEG SOF, stdlib) + rôle identifié (QuickGuide/vue complète, Manual/fonctionnement+vignettes, Freeze Help) | 3 illustrés attendus sur la référence (4000×2500, 858×892, 2149×2753) |
| E6 | **Correspondance visuels↔contrôles** (table P1b de `references/correspondance-visuels.md`) : présence et nb cid exacts des noms de contrôles des vues partielles dans les 163 noms définis | 22/22 attendus ; verdict `PASS` ssi (a) 1 mapping analysé, (b) G2 conforme si référence, (c) P1b sans écart, (d) aucun TSI illisible |

## §3 — Usage

```bash
# Pipeline complet sur un ZIP (inventaire, classification, mapping, compagnons, illustrés, P1b)
python3 skills/analyse-doc-s4mk2/scripts/analyser-zip-mk2.py "<zip-ou-dossier>" --json rapport.json

# Moteur seul sur un .tsi de mapping (comptes + conformité G2 + self-test)
python3 skills/analyse-doc-s4mk2/scripts/analyser_tsi_mk2.py <fichier.tsi> --json rapport.json
python3 skills/analyse-doc-s4mk2/scripts/analyser_tsi_mk2.py <fichier.tsi> --self-test

# Batterie de tests $FACON2 (cohérent, optimisé et fonctionnel) : TF-01..06 + TR-01..05
python3 skills/analyse-doc-s4mk2/tests/run_all.py [--zip CHEMIN] [--dir CHEMIN_DOSSIER]
```

Exit codes : `0` PASS / `1` écart ou FAIL / `2` usage ou cible absente. Les rapports JSON sont byte-stables (idempotence ×2 vérifiée par TR-03).

## §4 — Échantillon de référence (golden) et batterie

- `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0` (ZIP du propriétaire) : 6 fichiers + 2 dossiers — mapping 1 810 459 o (conforme G2 10/10), `Extra/FX Settings.tsi` 7 517 o (96 Entry), `Extra/Layouts.tsi` 5 923 o (39 Entry), QuickGuide 4000×2500, Freeze Help 858×892, Manual 2149×2753 (978 634 o).
- Batterie `$FACON2` (`tests/run_all.py`) : **11 tests** — TF-01 inventaire, TF-02 classification, TF-03 comptes G2, TF-04 baseline stricte (4960/666/49), TF-05 table P1b (22 noms, cid exacts), TF-06 illustrés (dimensions+rôles), TR-01 rejet préférences (rc=1 sans traceback), TR-02 blob corrompu (rejet contrôlé), TR-03 idempotence ×2 byte-stable, TR-04 cible absente (rc=2), TR-05 self-test moteur. Journal JSON individuel par test (`tests/journal/`) + `synthese.json`. Échantillon introuvable = **FAIL explicite** (le skill ne ment jamais).
- Résultat de référence : **BATTERIE PASS (11/11)**.

## §5 — Relations (famille TSI)

| Avec | Nature |
| --- | --- |
| `agent-TSI` | **Orchestration** : membre routé de la matrice (« analyser un mapping existant + documents illustrés » → ce skill) ; verdicts consommés par l'agrégation de l'agent |
| `tsi-validator` | Complémentarité de formats : le validateur couvre les TSI synthétiques écosystème (`NISYSTEM`) ; ce skill couvre les TSI réels (`NIXML`, blob DIOM) — écart E1 consigné dans la doc approfondie §7, évolution du validateur proposée (non appliquée) |
| `tsi-architect` | En amont : les comptes réels (163 noms, 345 conditions, top commandes `_(Mod)`) calibrent les conceptions |
| `multi-shift-architect` | En lecture : les 9 couches logiques du mapping réel (BASE, Shifts, Super FX, JogFX, Freeze, Echo Mods, Flux, Panic, Hotcue 5-8) alimentent l'analyse de couverture — lien CMAI↔condition non décodé (§6) |
| `midi-doc-expert` | En aval : les comptes et la table P1b nourrissent la documentation illustrée d'un mapping validé |
| `gen-plan` / `correct-work` | Verdicts machine mobilisables par les hooks de phase (analyse d'artefacts TSI réels dans un projet) |

**Provenance** : moteur issu de `scripts/zip-tsi/analyse-djtt-mk2.py` v1.1.0 (session Task 33, GO trace 1a197aaf0eb6557d) — self-test PASS ; table P1b ancrée sur les crops vérifiés (`crop-fx1-quickguide.png`, `crop-vignettes-manual.png`) et le doc approfondi `download/analyse-djtt-s4mk2-v2.1.0-approfondie.md`.

## §6 — Limites assumées (jamais masquées)

1. Lien CMAI ↔ condition **non décodé** : le candidat « index de condition » du payload CMAD (@44/@48) est une hypothèse qualifiée ; l'analyse multi-shift s'appuie sur les sources textuelles du pack (Manual, Freeze Help) et non sur une attribution mécanique par assignation.
2. Les 666 CMAD illisibles (11,83 %) : payloads de 120 o sans champ nom (erratum Task 33, reproductible) — les comptes G2 publiés 394/4970 contenaient un artefact non reproductible du décodeur perdu.
3. La reconnaissance des photos d'éléments non listées dans la table P1b reste **assistée** (libellés sérigraphiés → préfixe DCBM → vérification mécanique) : le skill vérifie, il ne devine pas.
4. `Status.Effect 4 Select` absent du FX Settings.tsi : constat brut, interprétation refusée.
