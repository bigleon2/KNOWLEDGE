# Rapport G2 — Analyse du ZIP `mes-mappings-tsi-actuels.zip` (Task 56, D004/D005/D007)

**Date** : 2026-11-06 · **Pipeline** : analyse-doc-s4mk2 v1.3.0 (7 étapes, référentiel G2) + tsi-validator v1.3.0 (verdicts E1-E8) · **Source** : `upload/mes-mappings-tsi-actuels.zip` (6 TSI, ~6 Mo) · **Rapport machine** : `download/rapport-zip-s4mk2-task56.json`

## 1. Classification (T2.1.2/T2.1.3 — verdicts mécaniques)

| Fichier | Verdict tsi-validator | Type réel | Devices | Assignations (CMAI) | Contrôles distincts | Commandes distinctes |
|---|---|---|---|---|---|---|
| Kontrol S4 Mapping _ Aout 2023.tsi | **PASS** (exit 0) | MAPPING S4 MK2 (3 Entry) | 1 · Traktor.Kontrol S4MK2.Default | 14 | 8 | 4 |
| Mapping TRAKTOR _ KONTROL S4 MK2 Novembre 2023.tsi | **PASS** | MAPPING S4 MK2 (3 Entry) | 1 | 14 | 8 | 4 |
| Kontrol S4 _ Mon Mapping (Aout 2024).tsi | **PASS** | MAPPING S4 MK2 (3 Entry) | 1 | **31** | 23 | 6 |
| Mapping Juin 2024-2025.tsi | **PRÉFÉRENCES** (exit 2 — F1) | PRÉFÉRENCES-GÉNÉRIQUES | 0 contrôleur | — | — | — |
| Traktor - Setting NOVEMBRE 2024.tsi | **PASS** (6 devices) | HYBRIDE settings + mapping (438 Entry) | 6 | 15 | 9 | 5 |
| Traktor Settings.tsi | **PASS** (9 devices) | HYBRIDE settings + mapping (492 Entry) | 9 | 15 | 9 | 5 |

**Surprise D005 qualifiée honnêtement** : les 2 fichiers volumineux « Settings » (2/4 Mo) ne sont PAS des préférences pures — ils embarquent un mapping contrôleur minimal (15 assignations) au milieu de préférences multi-devices (6 et 9 devices : FX, layouts). Inversement, « Mapping Juin 2024-2025.tsi » — dont le nom suggère un mapping — est un fichier de **PRÉFÉRENCES** (verdict PRÉFÉRENCES, 0 device contrôleur) : **le fichier le plus récemment nommé « mapping » n'est pas un mapping**.

## 2. Lecture croisée chronologique (T2.2.2 — évolution du mapping propriétaire)

```
Aout 2023 ──── identique ────→ Novembre 2023 ──── enrichissement ×2,2 ────→ Aout 2024
14 assignations                  14 assignations                          31 assignations
8 contrôles                      8 contrôles                              23 contrôles
4 commandes                      4 commandes                              6 commandes
```

- **Aout 2023 ≡ Novembre 2023** (mêmes comptes : le mapping de Novembre 2023 est une ré-exportation de celui d'Aout 2023 — probablement renommé/sauvegardé tel quel).
- **Aout 2024 = enrichissement net** : +17 assignations, +15 contrôles, +2 commandes distinctes — le propriétaire a plus que doublé la couverture de son mapping personnel.
- **Settings Nov 2024 & Traktor Settings** (les plus récents) : le mapping contrôleur embarqué ne porte que **15 assignations** — différent du « Mon Mapping (Aout 2024) » (31). **Piste de faille n°1 (voir §3)**.

## 3. Interprétation du verdict G2 « non conforme » (KO-L003 — honnêteté sur l'invariant)

Le pipeline rend « non conforme G2 » pour les 5 mappings car ils s'écartent du **référentiel complet DJTT v2.1.0** (5626 commandes, 163 contrôles, 393 commandes distinctes — l'échantillon de référence usine). **Cet écart est INFORMATIF, pas une faille** : le propriétaire utilise des mappings personnels volontairement minimaux (14-31 assignations vs 5626). La conformité G2 stricte n'a de sens que pour un mapping complet de type DJTT. Table P1b 0/22 : les contrôles FX (Dry/Wet, Knobs 1-3, Buttons 1-3, On, Mode ×2 decks) et les jogs (Encoder/Touch ×2) ne sont pas couverts — cohérent avec des mappings minimaux qui n'assignent pas les FX par le biais du mapping (les FX des S4 MK2 sont gérés en mode matériel natif).

## 4. Failles et recommandations (T2.2.3 — $FACON2)

| # | Constat | Faille/risque | Recommandation |
|---|---|---|---|
| F1 | Le mapping contrôleur embarqué dans les Settings récents (15 assignations, 9 contrôles) ≠ « Mon Mapping (Aout 2024) » (31 assignations) | Divergence entre le mapping de référence du propriétaire et celui réellement actif dans sa config Traktor | Ré-importer « Mon Mapping (Aout 2024).tsi » dans Traktor après le chargement des Settings, ou ré-exporter un Settings complet après import |
| F2 | « Mapping Juin 2024-2025.tsi » est un fichier de préférences, pas un mapping | Confusion de nommage — risque de perdre du temps à importer un « mapping » qui n'en est pas un | Renommer les exports (ex. « Préférences Juin 2024-2025.tsi ») ; à l'export TSI, distinguer « Exporter mapping contrôleur » vs « Exporter réglages » |
| F3 | Aucun mapping ne couvre les 22 contrôles P1b (FX, jogs) | Couverture matérielle partielle — les commandes non mappées retombent sur le comportement par défaut | Si besoin : compléter le mapping via tsi-architect (l'écosystème fournit la méthode + l'agent) — décision propriétaire |
| F4 | Aout 2023 ≡ Novembre 2023 (doublon d'export) | Doublon de fichier dans les archives | Hygiène : versionner via le dossier `archive/` du portail (vue-upload v1.5.0 gère les familles multi-versions) |

**Cohérence croisée** : RIEN_ATTESTER (0 document PDF/PNG compagnon dans le ZIP — pas d'attestation visuelle possible ; pas d'écart possible non plus).

## 5. Verdict G2

**ANALYSÉ 6/6** — 3 mappings purs (dont 2 identiques) + 1 préférences + 2 hybrides settings+mappings ; évolution 14→31 assignations mesurée ; écart G2 qualifié (minimaux vs usine — informatif) ; 4 failles/risques identifiés avec recommandations (F1 = la plus actionnable). Données complètes dans `rapport-zip-s4mk2-task56.json` (rejouable).
