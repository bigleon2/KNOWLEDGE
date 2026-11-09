# Correspondance visuels ↔ contrôles (table P1b)

**Source de vérité visuelle** : `QuickGuide v2.1.0.jpg` (vue complète du contrôleur, 4000×2500).
**Vues partielles** : photos d'éléments (ex. bloc FX 1 fourni par le propriétaire), vignettes matérielles du `Manual.jpg` (4 visuels encadrés « SHIFT » : capture écran unités FX 1/3, bande mixer haute, bloc FX 1, bloc FX 2), vue complète annotée (encadrés rouges FX 1/FX 2, labels orange `DRY/WET·1·2·3·MODE`).
**Ancrage TSI** : noms DCBM extraits mécaniquement (163 noms) — chaque correspondance ci-dessous est vérifiée par la batterie (TF-05 : 22/22, nb cid exacts).

## 1. Table de correspondance

| Vue partielle (source) | Zone sur la vue complète | Contrôles TSI exacts (cid ×) | Fonction mapping (source textuelle) |
| --- | --- | --- | --- |
| Bloc FX 1 complet : 4 encodeurs + boutons FX + MODE, LED MODE orange (photo propriétaire ; vignette 3 du Manual) | haut-gauche, zone « FX 1 » | `Left.FX.Dry/Wet` (16) · `Left.FX.Knob 1/2/3` (17/17/17) · `Left.FX.Button 1/2/3` (113/111/111) · `Left.FX.On` (78) · `Left.FX.Mode` (71) | DRY/WET + 3 paramètres de l'unité active ; boutons FX = sets du Super FX ; MODE = bascule Hybrid/Group ; LED orange = unité FX 1 sélectionnée |
| Bloc FX 2 (vignette 4 du Manual) | haut-droite, zone « FX 2 » | `Right.FX.Dry/Wet` (17) · `Right.FX.Knob 1/2/3` (17/16/17) · `Right.FX.Button 1/2/3` (110/111/110) · `Right.FX.On` (80) · `Right.FX.Mode` (70) | symétrique côté droit (Freely assignable) |
| Bande mixer haute : 4 GAIN + LEVEL central + boutons FX 1/2 (vignette 2 du Manual) | bande haute centrale | `A/B/C/D.Gain` · `A/B/C/D.FX.On 1/2` (22 chacun) | gains de tranches + activation FX 1/2 par deck |
| Capture écran unités FX 1/3 (vignette 1 du Manual : `BEATM/PFTR/ICEVB`, `MHDRV/F92-O/REVRB`) | (logiciel) | `Status.Effect 1/3 Select` (FX Settings.tsi compagnon) | effets chargés par slot — croisés avec `DEFAULT_BUTTON_FXx` / `DEFAULT_PARAM_FXx` |
| JogWheels | decks A/C et B/D | `Left/Right.Jog.Encoder` (166/161) · `Left/Right.Jog.Touch` (105/111) | Super FX Mode / JogFX : 8 presets, leds `range, Load, Sample, Shift` clignotantes quand actif |
| Sample buttons 1-4 | bas des decks | `Left/Right.Remix Slot. 1-4` | sous JogFX : 8 effets instantanés ; sinon slots Remix (decks C/D en `Status.Deck Flavor 0;0;1;1`) |
| Loop In/Out | zone LOOP des decks | `Left.Loop.In/Out` (458/787) · `Right.Loop.Out` (967) | boutons les plus polyvalents (modulés par les couches) : Freeze toggle `Shift+Loop In`, Echo Mods, Slice Size/Count |

## 2. Méthode d'ancrage (reproductible)

1. **Reconnaître** les libellés sérigraphiés de la photo (DRY/WET, 1, 2, 3, MODE, FX 1/2…).
2. **Convertir** en préfixe de nom DCBM (`Left.` / `Right.` / `Center.` + famille `FX.*`, `Loop.*`, `Remix Slot.*`, `Jog.*`).
3. **Vérifier** l'existence mécanique dans les noms définis (163) — le pipeline expose `noms_controles_definis`.
4. **Associer** la section correspondante du Manual et les commandes CMAI éponymes (`_(Mod) Super FX Mode…`).
5. **Consigner** le nb de cid attendu (colonne « cid × ») — toute divergence future entre versions du mapping est détectée par la batterie (TF-05).

## 3. Documents illustrés de l'échantillon de référence

| Fichier | Dimensions | Rôle |
| --- | --- | --- |
| `QuickGuide v2.1.0.jpg` | 4000×2500 | vue complète (référence de correspondance) |
| `Freeze Mode Help v2.1.0.jpg` | 858×892 | mode Freeze : 8 slices, `Shift+Loop In` toggle, 8 sorties, Slice Size/Count via encodeur |
| `Manual.jpg` (sous-dossier `Extra/`) | 2149×2753 | manuel DJTT (Brewhyr 2014) : fonctionnement + vignettes d'éléments (vues partielles) + « One minute setup » (import des 3 artefacts) |

Les **sous-dossiers** font partie du périmètre d'analyse : `Extra/` porte les 2 TSI compagnons (`FX Settings.tsi` : mode 4 unités FX, sets d'effets ; `Layouts.tsi` : decks C/D en Remix, layout 5) — indispensables au fonctionnement documenté.
