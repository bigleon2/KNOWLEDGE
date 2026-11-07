# Analyse approfondie — ZIP DJTT Kontrol S4 MK2 Custom Mapping v2.1.0

**Session** : web-4f989063 (Task 33 P1, GO trace 1a197aaf0eb6557d) · **Date** : 2026-11-02
**Arbitre** : `scripts/zip-tsi/analyse-djtt-mk2.py` v1.1.0 — SELF-TEST PASS (re-jeu ×2 byte-stable, référentiel G2 10/10, baseline stricte OK)
**Compléments** : `extrait-dcbm-conditions.py` v1.1.0 (163 noms DCBM, 345 conditions, sondage condition CMAD), crops vérifiés (`crop-fx1-quickguide.png`, `crop-vignettes-manual.png`)

---

## 1. Résumé exécutif

Le ZIP DJTT v2.1.0 livre **6 fichiers dans 2 dossiers** — pas un simple `.tsi` : un mapping contrôleur (1,8 Mo, blob binaire DIOM), deux TSI de préférences compagnons (`Extra/FX Settings.tsi`, `Extra/Layouts.tsi`) et trois documents illustrés (QuickGuide, Manual, Freeze Mode Help). L'analyse mécanique confirme les comptes de référence G2 (erratum Task 33 intégré), établit la **relation vues partielles ↔ vue complète** (photo bloc FX 1 = vignette du Manual = zone encadrée du QuickGuide, ancrée sur les noms de contrôles TSI exacts), dénombre **9 couches logiques multi-shift**, et révèle un **écart d'interopérabilité** du validateur écosystème (racine `NISYSTEM` attendue contre `NIXML` réelle). Trois constats structurants :

1. **Le mapping seul ne suffit pas** — `FX Settings.tsi` (mode 4 unités FX, sets d'effets) et `Layouts.tsi` (decks C/D en Remix, layout 5) sont indispensables au fonctionnement documenté par le Manual. Un analyseur qui ignore les sous-dossiers rate les deux tiers de l'installation.
2. **La relation visuelle est mécaniquement ancrable** : chaque photo d'élément correspond à des noms de contrôles DCBM univoques (`Left.FX.Mode`, `Left.FX.Knob 1…`) et à des sections du Manual — la table §5 formalise cette correspondance.
3. **Le format réel Traktor (NIXML) n'est pas couvert par le validateur écosystème** — l'analyseur v1.1.0 devient l'arbitre de fait sur ce format (§7).

## 2. Inventaire exhaustif du ZIP (2 dossiers, 6 fichiers)

| Membre | Taille (o) | Rôle |
| --- | ---: | --- |
| `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/` | — | dossier racine |
| `…/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi` | 1 810 459 | **mapping contrôleur** (NIXML, blob base64 DIOM) |
| `…/QuickGuide v2.1.0.jpg` | 3 241 567 | **vue complète** du contrôleur (référence 4000×2500) |
| `…/Freeze Mode Help v2.1.0.jpg` | 136 924 | aide dédiée du mode Freeze (858×892) |
| `…/Extra/` | — | **sous-dossier** compagnon |
| `…/Extra/FX Settings.tsi` | 7 517 | préférences **unités d'effets** (96 Entry) |
| `…/Extra/Layouts.tsi` | 5 923 | préférences **interface/layouts** (39 Entry) |
| `…/Extra/Manual.jpg` | 978 634 | **manuel DJTT** (texte + captures d'éléments, Brewhyr 2014) |

## 3. Le mapping principal (`.tsi`, arbitre v1.1.0)

**Identité** : device logique `Traktor.Kontrol S4MK2.Default` · titre `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0 (stewe update)` · `DDIV` 2.12.0 + métadonnées `cmdr` 0.9.6.0.

**Comptes validés (référentiel G2, 10/10)** :

| Compte | Valeur | Note |
| --- | ---: | --- |
| DEVI | 1 | device unique |
| DCDT in / out / total | 125 / 220 / 345 | conditions déclarées |
| CMAI = CMAD lus = DCBM | 5 626 | trame CMAD **embarquée** dans CMAI (FourCC @+12, taille @+16, payload @+20) |
| noms de commandes lisibles | 4 960 (88,17 %) | erratum Task 33 : G2 publié 4 970 (88,3 %) — décodeur d'origine perdu, non reproductible |
| CMAD illisibles | 666 (11,83 %) | payloads de 120 o sans champ nom (vérifié à tous les offsets) |
| commandes distinctes | 393 | erratum : G2 publié 394 (+1 non reproductible) |
| références résolues / non résolues | 5 136 / 490 | ref CMAI → cid DCBM |

**Formats clés (référentiel G2 §2.2 + diag Task 33)** : NIXML → `Entry DeviceIO.Config.Controller` (attribut **`Value`**, base64) → blob `DIOM` ; trames FourCC+u32 taille big-endian ; chaînes UTF-16-BE `[u32 n][n×2 o]` ; DCBM = 5 626 cid **distincts** portant seulement **163 noms** (chaque contrôle redéfini ~34× selon le contexte Traktor) — le comptage `controles_distincts` se fait par **noms**, pas par ids.

**Usage effectif** : 49 noms de contrôles sollicités au moins une fois (sur 163 définis). Top : `Right.Loop.Out` 967 · `Left.Loop.Out` 787 · `Left.Loop.In` 458 · `Right.Remix Slot. 4` 421 · `Right.Remix Slot. 2` 411 · `Right.Remix Slot. 1` 295 · `Left.Hotcue. 4` 239 · `Right.Remix Slot. 3` 236. Top commandes : `_(Mod) Super FX Mode Macro FX` 446 · `Echo Mod 2 (Shift + Loop Set Knob)` 381 · `_(Mod) Freeze Mode` 307 · `Super FX Mode Toggle Settings` 260 · `_(Mod) Flux Mode - Hold other deck's Shift + Any Hotcue` 120 · `Super FX Mode Active Leds` 109 · `_(Mod) Panic Button - [Hold Browse Push] + [Press Undo Loop Rec]` 97 · `_(Mod) Hotcue 5-8 on Sample buttons` 96. Les préfixes `_(Mod)` marquent les commandes que le Manual déclare **éditables en toute sécurité**.

## 4. Les sous-dossiers (`Extra/`) — les compagnons indispensables

### 4.1 `FX Settings.tsi` (96 Entry, format v3)

TSI de **préférences** (aucune `DeviceIO.Config.Controller` → rejet propre de l'analyseur mapping, comportement attendu). Contenu :

- `Status.4 FX Units = 1` : **mode 4 unités FX exigé** — le Manual l'assume (`FX unit 3 - Grouped JogFX`, `FX unit 4 - Single JogFX, Echo Mod 1-2`) ;
- `Status.FX Panel Mode = 0;0;0;1` : unités 1-3 en Group, unité 4 en Single ;
- `Status.Effect 1/2/3 Select` : effets chargés par slot (ex. unité 1 = `1;35;1;32`) — l'**unité 4 n'a pas d'`Status.Effect 4 Select`** (constat brut, non expliqué) ;
- `Audio.FX.Selection` : palette de 43 effets ordonnant l'espace d'ids des presets ;
- 45 presets `DEFAULT_BUTTON_FXx` (on/off des boutons, type 5) et 45 `DEFAULT_PARAM_FXx` (5 paramètres flottants, type 6) — ce sont les **« Shift - Effect Button X = Set to … »** du Manual (ex. `Set to Beatmasher - PolarWind - Zzzurp`) ;
- `Status.Effect Routing = 1;1;1;1`, `FX Restore Preset on Switch = 0`.

La capture écran du Manual (unités FX 1/3 : `BEATM·PFTR·ICEVB` / `MHDRV·F92-O·REVRB`) matérialise ces sélections.

### 4.2 `Layouts.tsi` (39 Entry, format v3)

TSI de **vue/interface** (rejet propre également) :

- `Status.Deck Flavor = 0;0;1;1` : decks A/B **Track**, decks C/D **Remix** — l'architecture Remix du mapping (slots 1-4, sample buttons) requiert C/D en Remix ;
- `Status.Select Layout = 5`, `Status.Deck Size = 3;4`, panneau avancé `1;2;1;1` ;
- `Gui.Layouts2` (1 704 car.) et `Gui.LayoutFactories2` (1 663 car.) : masquage des 43 panneaux par layout — le « Full Browser View » du mapping s'appuie dessus ;
- `Browser.List.RowHeight = 18`, `Browser.SplitterRatio = 0.262069`, waveforms (grid mode 2, color mode 3).

### 4.3 Conclusion

Le « One minute setup » du Manual impose d'importer **les trois artefacts** (mapping + settings + layouts). La famille TSI et le futur skill doivent classifier les TSI en **mapping** (blob `DeviceIO.Config.Controller`) contre **préférences** (Entries de settings) — la distinction est mécanique et déjà implémentée dans le rejet propre de l'analyseur.

## 5. Relation vues partielles ↔ vue complète (table de correspondance)

**Source de vérité visuelle** : `QuickGuide v2.1.0.jpg` (vue complète). **Vues partielles** : photo utilisateur bloc FX 1 (upload), vignettes matérielles du Manual (4 visuels encadrés « SHIFT »), vue complète annotée fournie par le propriétaire (encadrés rouges FX 1/FX 2, labels orange `DRY/WET·1·2·3·MODE`). **Ancrage TSI** : noms DCBM extraits mécaniquement (163).

| Vue partielle (source) | Zone sur la vue complète | Contrôles TSI exacts (cid ×) | Fonction mapping (source textuelle) |
| --- | --- | --- | --- |
| **Bloc FX 1 complet** : 4 encodeurs + boutons FX + MODE, LED MODE orange allumée (photo utilisateur ; vignette 3 du Manual) | haut-gauche, zone « FX 1 » (encadrée rouge sur la vue annotée) | `Left.FX.Dry/Wet` (16) · `Left.FX.Knob 1/2/3` (17/17/17) · `Left.FX.Button 1/2/3` (113/111/111) · `Left.FX.On` (78) · `Left.FX.Mode` (71) | DRY/WET + 3 paramètres de l'unité active ; boutons FX = sets du Super FX (`Shift - Effect Button 1 = Set to Beatmasher - PolarWind - Zzzurp`, Manual) ; MODE = bascule Hybrid/Group (`Hold The FX MODE button to temporarily hold hybrid mode`, Manual). LED orange = unité FX 1 sélectionnée. |
| **Bloc FX 2** (vignette 4 du Manual) | haut-droite, zone « FX 2 » | `Right.FX.Dry/Wet` (17) · `Right.FX.Knob 1/2/3` (17/16/17) · `Right.FX.Button 1/2/3` (110/111/110) · `Right.FX.On` (80) · `Right.FX.Mode` (70) | symétrique côté droit (Freely assignable) |
| **Bande mixer haute** : 4 GAIN + LEVEL central + boutons FX 1/2 (vignette 2 du Manual) | bande haute centrale (encadré rouge milieu) | `A/B/C/D.Gain` · `A/B/C/D.FX.On 1/2` (22 chacun) | gains de tranches + activation FX 1/2 par deck (`Center FX Buttons 1-2 - Deck A-C G-D FX 1/2 On/Off`, Manual) |
| **Capture écran unités FX 1/3** (vignette 1 du Manual) | (logiciel, superposée à la vue) | `Status.Effect 1/3 Select` (FX Settings.tsi) | effets chargés par slot ; l'écran montre `BEATM/PFTR/ICEVB` (u.1) et `MHDRV/F92-O/REVRB` (u.3) |
| **JogWheels** (vue complète) | decks A/C et B/D | `Left/Right.Jog.Encoder` (166/161) · `Left/Right.Jog.Touch` (105/111) | **Super FX Mode / JogFX** : 8 presets, rotation = navigation, pression = chargement (`Use the Jogwheel for controlling effects… the range, Load, Sample and Shift led blink`, Manual) |
| **Sample buttons 1-4** (zones Remix) | bas des decks | `Left/Right.Remix Slot. 1-4` (sollicitations 4-421) | sous JogFX : déclenchement de 8 effets instantanés ; sinon slots Remix (decks C/D) |
| **Loop In/Out** (vue complète) | zone LOOP des decks | `Left.Loop.In/Out` (458/787) · `Right.Loop.Out` (967) | boutons les plus polyvalents du mapping (modulés par les couches §6) : Freeze toggle (`Shift + Loop In`), Echo Mods, Slice Size/Count |

**Méthode d'ancrage** (réutilisable par le skill) : photo d'élément → reconnaître les libellés sérigraphiés (DRY/WET, 1, 2, 3, MODE, FX 1/2) → convertir en préfixe de nom DCBM (`Left./Right./Center.` + famille) → vérifier l'existence mécanique dans les 163 noms → associer la section correspondante du Manual et les commandes CMAI dont le nom cite la fonction (`_(Mod) Super FX Mode…`).

## 6. Analyse multi-shift (couches logiques)

Le mapping est **multi-couches** : un même contrôle physique change de fonction selon la couche active. Les 345 conditions DCDT (in 125 : Left 35, Right 35, Center 12, A-D 40, Front 2, Back 1 ; out 220 : Left 90, Right 90, Center 12, A-D 28) fournissent l'inventaire des contrôles conditionnables ; les couches effectives sont documentées par le Manual et les commandes `_(Mod)` :

| Couche | Activation (source Manual) | Commandes CMAI associées (assignations) |
| --- | --- | --- |
| **BASE** | — (état standard S4 MK2) | contrôles triviallement mappés (Gain, EQ, transport…) |
| **Shift gauche/droit** | maintenir `Left.Shift` / `Right.Shift` | combos explicites dans tout le Manual (Shift + …) |
| **Super FX Mode** | `Shift + Flux` pour activer, `Flux` pour désactiver | `_(Mod) Super FX Mode Macro FX` 446 · `Super FX Mode Toggle Settings` 260 · `Super FX Mode Active Leds` 109 |
| **JogFX** (groupé/single) | inclus dans Super FX (FX units 3/4) | presets de JogFX via `Left/Right.Jog.Encoder` |
| **Freeze Mode** | `Shift + Loop In` (toggle) — 8 slices | `_(Mod) Freeze Mode` 307 · Slice Size/Count via encodeurs (Freeze Mode Help) |
| **Echo Mods 1-3** | `Left Loop Active Knob` (Mod 1), `Shift + Right Loop Set Knob` (Mod 3)… indépendants du Super FX | `Echo Mod 2 (Shift + Loop Set Knob)` 381 |
| **Flux Mode (cross-deck)** | `Hold other deck's Shift + Any Hotcue` | `_(Mod) Flux Mode - Hold other deck's Shift + Any Hotcue` 120 |
| **Panic** | `Hold Browse Push + Press Undo Loop Rec` | `_(Mod) Panic Button - [Hold Browse Push] + [Press Undo Loop Rec]` 97 |
| **Hotcue 5-8 / Sample remap** | Sample buttons, `Shift + Deck Assign C/D` | `_(Mod) Hotcue 5-8 on Sample buttons` 96 |

Lecture multi-shift au sens `multi-shift-architect` : couverture forte (le top 3 des contrôles — `Right.Loop.Out`, `Left.Loop.Out`, `Left.Loop.In` — porte chacun 458-967 assignations réparties sur plusieurs couches), aucun signe de couche morte : chaque couche citée par le Manual possède ses commandes CMAI éponymes. Limite mécanique assumée : le **lien CMAI ↔ condition** (quel DCDT conditionne quelle assignation) n'est pas décodé — le sondage v1.1.0 situe le candidat « index de condition » dans le payload CMAD autour des offsets **@44 (31 valeurs distinctes) / @48 (42 valeurs)**, hypothèse non conclue, consignée.

## 7. Constat d'interopérabilité : validateur écosystème vs format réel

`tsi-validator` (arbitre mécanique E1-E8) sur le `.tsi` réel → **FAIL 3 erreurs E1** : racine attendue `NISYSTEM`, trouvée `NIXML` ; attribut `VERSION` absent ; 0 élément `DEVICE`. Cause : le validateur cible la structure des TSI **générés par l'écosystème** ; les TSI **réels de Traktor** ont une racine `NIXML` avec `Entry` + blob base64 (référentiel G2 §2.2, confirmé ici). Conséquences :

- l'arbitre de fait sur le format réel est l'**analyseur v1.1.0** (conformité G2 10/10, self-test déterministe) ;
- le skill `analyse-doc-s4mk2` embarque ce constat et utilise la classification mapping/préférences ;
- **recommandation** (proposition, sur GO) : faire évoluer `tsi-validator` E1 pour accepter les deux racines (`NISYSTEM` écosystème / `NIXML` réel avec Entry `DeviceIO.Config.Controller`) — golden samples à étendre, non réalisé dans cette session (périmètre P1).

## 8. MK2 ↔ MK3 (points de divergence mobilisables)

La famille TSI est calibrée S4 MK3 (périmètre de `orchestrateur-tsi`, mentions MK2 = calibration préalable). Ce mapping réel ancre la divergence :

- **MK2** : 2 blocs FX (4 encodeurs + boutons + MODE chacun) asservis à 4 unités logiques via le mode « 4 FX Units » ; JogWheels encodeurs ; pas d'écrans ; LED MODE orange = unité sélectionnée ;
- **MK3** : 4 blocs FX dédiés (one-per-channel), écrans, touch strips, sections HIDE — les couches `_(Mod)` du DJTT (JogFX via jogwheel, Super FX via Flux) n'ont **pas d'équivalent matériel direct** : un portage MK3 repenserait la localisation (c'est la mise en garde de calibration de la famille TSI) ;
- les noms DCBM (`Left./Right./Center.`, familles `FX.*`, `Loop.*`, `Remix Slot.*`) restent la grammaire commune pour la comparaison.

## 9. Limites et réserves

1. 666 CMAD (11,83 %) illisibles : payloads 120 o sans nom — l'erratum Task 33 est documenté et reproductible ; les comptes G2 publiés (394/4 970) contenaient un artefact non reproductible du décodeur perdu.
2. Lien CMAI ↔ condition : non décodé (candidat @44/@48, §6) — l'analyse multi-shift repose sur les sources textuelles du ZIP, pas sur une attribution mécanique par assignation.
3. `Status.Effect 4 Select` absent du FX Settings.tsi : constat brut, interprétation refusée.
4. Le validateur écosystème rejette le format réel (§7) — recommandation d'évolution consignée, non appliquée.
5. Les 2 TSI compagnons sont analysés en structure (Entries) ; la sémantique complète des 43 panneaux de `Gui.Layouts2` n'est pas décodée bit-à-bit (hors périmètre).

## 10. Artefacts produits (session P1)

| Artefact | Rôle |
| --- | --- |
| `scripts/zip-tsi/analyse-djtt-mk2.py` v1.1.0 | analyseur mapping (arbitre format réel) — self-test PASS |
| `scripts/zip-tsi/analyse-djtt-mk2.json` | rapport complet (comptes, top contrôles/commandes, conditions) |
| `scripts/zip-tsi/extrait-dcbm-conditions.py` v1.1.0 + JSON | 163 noms DCBM (cid×), 345 conditions, sondage condition CMAD |
| `scripts/zip-tsi/crop-fx1-quickguide.png` / `crop-vignettes-manual.png` | preuves visuelles P1b |
| `download/analyse-djtt-s4mk2-v2.1.0-approfondie.md` | le présent document |
