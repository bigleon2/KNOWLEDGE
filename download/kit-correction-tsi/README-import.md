# Kit de correction TSI — Guide d'import ordonné (F1/F2/F4)

**Contenu du kit** (généré Task 57, session web-c30e6506, 2026-11-06) :

| Fichier | Rôle | Verdict tsi-validator v1.3.0 |
|---|---|---|
| `Traktor - Setting NOVEMBRE  2024.tsi` | Vos réglages Traktor les plus récents (6 devices) — **à charger EN PREMIER** | PASS (exit 0) |
| `Kontrol S4 _ Mon Mapping (Aout 2024).tsi` | Votre mapping de référence (31 assignations, 1 device S4 MK2) — **à importer EN SECOND** | PASS (exit 0) |
| `Préférences Juin 2024-2025.tsi` | Renommage honnête de « Mapping Juin 2024-2025.tsi » : c'est un fichier de **préférences**, PAS un mapping | PRÉFÉRENCES (exit 2) |

---

## ⚠️ Pourquoi ce guide (faille F1)

Votre fichier de Settings récent embarque un mapping contrôleur **minimal (15 assignations)**, alors que votre mapping de référence « Mon Mapping (Aout 2024) » en contient **31**. Si vous chargez uniquement les Settings, votre S4 MK2 tournera sur la version réduite — **la divergence 15 ≠ 31** constatée par l'analyse (rapport G2 Task 56).

## ✅ Procédure d'import ordonné (2 imports)

1. **Charger les réglages** : dans Traktor Pro, `Fichier → Importer` (ou Préférences) → sélectionner `Traktor - Setting NOVEMBRE  2024.tsi`.
2. **Ré-importer le mapping de référence** : dans le Controller Manager (`Préférences → Gestionnaire de contrôleurs`) → `Importer` → sélectionner `Kontrol S4 _ Mon Mapping (Aout 2024).tsi` → **activer ce mapping** comme mapping en cours pour le device Kontrol S4 MK2 (et désactiver/supprimer l'embarqué minimal si les deux coexistent).
3. **Vérifier** : le mapping actif doit afficher **31 assignations** (et non 15).

> Alternative : ré-exporter un Settings complet **après** l'étape 2 (Traktor embarquera alors le bon mapping) — le fichier ré-exporté remplacera avantageusement le Settings actuel dans vos archives.

## 📛 Renommage (faille F2)

« Mapping Juin 2024-2025.tsi » est un fichier de **préférences** (0 device contrôleur — vérifié mécaniquement), pas un mapping : son nom prêtait à confusion. Ce kit en fournit la copie renommée **« Préférences Juin 2024-2025.tsi »** (contenu inchangé — verdict PRÉFÉRENCES identique avant/après). À l'avenir, à l'export : « Exporter mapping contrôleur » ≠ « Exporter réglages/préférences » — nommez en conséquence.

## 🧹 Hygiène doublon (faille F4)

`Kontrol S4 Mapping _ Aout 2023.tsi` ≡ `Mapping TRAKTOR _ KONTROL S4 MK2 Novembre 2023.tsi` : **même contenu** (14 assignations chacun, exports dupliqués). Conservation recommandée : **Novembre 2023** (nom le plus explicite) ; Aout 2023 peut être archivé (le portail vue-upload gère les familles multi-versions via `archive/`).

## 📋 Le 6ᵉ fichier (informatif)

`Traktor Settings.tsi` (4 Mo, 9 devices) : second fichier de réglages — non requis par la procédure ci-dessus (NOVEMBRE 2024 est le plus récent daté).

---
*Validation : tsi-validator v1.3.0 avant/après — conformité 3/3 (PASS/PASS/PRÉFÉRENCES inchangés par le renommage). Détails : `rapport-kit-correction-tsi.md`.*
