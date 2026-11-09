# Rapport — Kit de correction TSI (Task 57, G1)

**Session** : web-c30e6506 · **Date** : 2026-11-06 · **Source** : failles F1/F2/F4 du rapport G2 Task 56 (`rapport-g2-analyse-zip-s4mk2.md`) · **Arbitre** : tsi-validator v1.3.0.

## 1. Périmètre et méthode

Traitement actionnable des failles identifiées à l'analyse du ZIP `upload/mes-mappings-tsi-actuels.zip` (6 TSI). Méthode : extraction fraîche (`tmp/zip-task57/`), copies non-destructives (originaux jamais modifiés), renommage documenté, validation mécanique avant/après.

## 2. Verdicts avant/après (conformité)

| Fichier kit | Avant (original) | Après (kit) | Conforme |
|---|---|---|---|
| `Préférences Juin 2024-2025.tsi` (ex « Mapping Juin 2024-2025.tsi ») | PREFERENCES (exit 0) — 0 device, 0 `<Name>` interne | PREFERENCES (exit 0) | ✅ |
| `Kontrol S4 _ Mon Mapping (Aout 2024).tsi` | PASS (exit 0) — 1 device `Traktor.Kontrol S4MK2.Default`, CMAI 31, DCBM 31 | PASS (exit 0) | ✅ |
| `Traktor - Setting NOVEMBRE  2024.tsi` | PASS (exit 0) — 6 devices, CMAI 5730, DCBM 5730 | PASS (exit 0) | ✅ |

**Conformité : 3/3** — le renommage (nom de fichier uniquement) n'a aucun effet structurel ; il n'existe aucun nom interne à renommer dans le fichier de préférences (0 `<Name>`, 0 `<Device>` — constat mécanique).

## 3. Traitement des failles

| Faille | Traitement | Livrable |
|---|---|---|
| **F1** — mapping embarqué Settings (15 assignations) ≠ référence Aout 2024 (31) | Guide d'import ordonné (Settings d'abord, ré-import du mapping ensuite) ; **pas de chirurgie TSI** (décision motivée : risque de corruption des préférences propriétaire ; la procédure 2 imports est celle recommandée par le rapport G2 ; alternative ré-export documentée) | `kit-correction-tsi/README-import.md` |
| **F2** — « Mapping Juin 2024-2025.tsi » = préférences, nom trompeur | Copie renommée « Préférences Juin 2024-2025.tsi » (filename only — pas de nom interne) | `kit-correction-tsi/Préférences Juin 2024-2025.tsi` |
| **F3** — couverture P1b 0/22 | **Décision propriétaire** (compléter le mapping via tsi-architect) — rappelé au rapport final | — |
| **F4** — doublon Aout 2023 ≡ Novembre 2023 (14 assignations chacun) | Hygiène documentée : conservation recommandée Novembre 2023 (nom explicite), Aout 2023 à archiver (vue-upload v1.5.0 gère `archive/`) | Section du README-import.md |

## 4. Livrables du kit

```
download/kit-correction-tsi/
├── README-import.md                              # Guide F1 + renommage F2 + hygiène F4
├── Préférences Juin 2024-2025.tsi                 # F2 — copie renommée (PREFERENCES, exit 0)
├── Kontrol S4 _ Mon Mapping (Aout 2024).tsi       # Référence F1 (PASS, 31 assignations)
└── Traktor - Setting NOVEMBRE  2024.tsi           # Settings F1 (PASS, 6 devices)
```

## 5. Verdict G1

**LIVRÉ 3/3 failles actionnables** (F1 guide · F2 renommage validé · F4 hygiène) — F3 reste décision propriétaire. Verdicts mécaniques conformes avant/après 3/3. Action restante propriétaire : exécuter la procédure d'import dans Traktor (2 imports), puis idéalement ré-exporter un Settings complet.
