# Analyse du corpus ZIP — DJTT Kontrol S4 MK2 Custom Mapping v2.1.0

> **Task 7 G2** · Session web-eb6c8580 · 2026-10-30 · Généré via gen-plan v3.28.2 (plan amendé 1)
> **Objet** : analyse du mapping TSI réel tiers (ZIP propriétaire) — objet des tâches G3 (validation agents) et G4 (calibration midi-doc-expert + tsi-validator).
> **Méthode** : décodage mécanique stdlib (`scripts/zip-tsi/analyse-tsi-reel.py`) + lecture VLM des 3 JPG de documentation. Couverture honnête R-1 (champs binaires CMAD non décodés sémantiquement — documenté §3.4).

## 1. Inventaire du ZIP

`upload/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.zip` (4,3 Mo ; doublon URL-encodé ignoré) — extrait dans `scripts/zip-tsi/extracted/` :

| Fichier | Taille | Nature (constatée) |
|---|---|---|
| `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi` | 1 810 459 o | **Mapping TSI réel** — NIXML + blob binaire DIOM (l'objet de l'analyse) |
| `Extra/Layouts.tsi` | 5 923 o | **Préférences Traktor** (39 Entry : Browser.List.RowHeight, Fileinfo.*…) — **AUCUN blob mapping** |
| `Extra/FX Settings.tsi` | 7 517 o | **Préférences Traktor** (96 Entry : DEFAULT_BUTTON_FX1-15, Audio.FX.Selection…) — **AUCUN blob mapping** |
| `QuickGuide v2.1.0.jpg` | 1,8 Mo | Documentation : guide fonctionnel complet (lu VLM §4) |
| `Freeze Mode Help v2.1.0.jpg` | 978 Ko | Documentation : aide du mode Freeze (lu VLM §4) |
| `Extra/Manual.jpg` | 137 Ko | Documentation : manuel d'installation (lu VLM §4) |

## 2. Structure du format réel (décodée mécaniquement)

### 2.1 Couche XML

Racine **`NIXML`** → `TraktorSettings` → 101 `Entry[@Name][@Type][@Value]`. Le mapping complet est encapsulé dans **une seule Entry** : `Name="DeviceIO.Config.Controller" Type="3" Value=<Base64>` → blob binaire de **1 352 130 octets**, magique **`DIOM`**.

Les Entry restantes : préférences diverses (audio, browser, deck defaults…). `Layouts.tsi` et `FX Settings.tsi` partagent la même racine NIXML mais ne contiennent aucune entrée `DeviceIO.Config.Controller` — ce sont des fichiers de préférences purs, à importer séparément (le manuel le confirme : « Importer BOTH Controller Settings ET Mappings », Layouts optionnel).

### 2.2 Blob DIOM — hiérarchie des trames (marche stricte, big-endian intégral)

```
DIOM [u32 taille_totale]
├── DIOI (4 o — version de format)
└── DEVS [u32 nb_devices = 1]
    └── DEVI [u32 n][nom device UTF-16-BE ×n]          ← "Traktor.Kontrol S4MK2.Default"
        └── DDAT
            ├── DDIF (4 o)
            ├── DDIV [u32 n]["<ver> <n>|<cmdr_metadata JSON>" UTF-16-BE]
            │      ← "2.12.0 18|{cmdr_metadata:{Version:0.9.6.0,…}}"
            ├── DDIC [u32 n][titre mapping UTF-16-BE]   ← "DJTT Kontrol S4 MK2 Custom Mapping
            │      v2.1.0 (stewe update)"
            ├── DDPT [u32 n][id ×n]                     ← "2EE94697" ×2 (horodatages)
            ├── DDDC [DDCI[DCDT ×125]][DDCO[u32 220][DCDT ×220]]   ← conditions/modifiers
            ├── DDCB
            │     ├── CMAS [u32 nb = 5626][CMAI ×5626]  ← assignations IN
            │     │     └── CMAI [u32 ordinal][u32 drapeau][u32 réf_contrôle]
            │     │           └── CMAD (binaire : type u32, 3 floats, nom commande,
            │     │               paramètres — partiellement décodé)
            │     └── DCBM [u32 nb = 5626][DCBM ×5626]  ← bindings contrôles physiques
            │           └── DCBM [u32 id][u32 n][nom contrôle UTF-16-BE ×n]
            └── DVST (20 o)
```

Conventions binaires : **big-endian intégral** (u32, floats BE, chaînes **UTF-16-BE** `[u32 nb_chars][nb_chars × 2 octets]`) — cohérent avec la doctrine LEON TSI EDITEUR (« Reader/Writer big-endien, trames FourCC imbriquées »). Comptes réels (marche stricte) : DIOM 1 · DIOI 1 · DEVS 1 · DEVI 1 · DDAT 1 · DDIF/DDIV/DDIC/DDPT/DDDC/DDCB/DVST 1 chacun · DCDT **345** (125 DDCI + 220 DDCO) · CMAI **5 626** · CMAD **5 626** · DCBM **5 626**.

**Nota** : le sondage pré-vol (plan initial) annonçait « CMAI ×158, DCDT ×293 » — ce sondage tronqué est **corrigé** par la présente marche complète : 5 626 CMAI (le compte 158 correspondait aux seules CMAI de taille 158 o d'un échantillon) et 345 DCDT.

### 2.3 cmdr_metadata (extrait DDIV, JSON intégral)

```json
{"cmdr_metadata": {"Version": "0.9.6.0",
  "DeviceMetadata": {"MappingMetadata": {}, "ConditionDescriptions": {}}}}
```

Métadonnées du **Controller Manager** NI (cmdr = éditeur de mappings Traktor 2.x) — version de format 0.9.6.0, tables de métadonnées vides dans ce fichier.

## 3. Mappings extraits

### 3.1 Volumétrie

| Métrique | Valeur |
|---|---|
| Mappings extraits (assignations déclarées CMAS / marchées) | **5 626 mappings** (5 626 / 5 626 — 100 %) |
| Bindings contrôles (DCBM) | **5 626** (ids uniques) |
| Contrôles physiques distincts | **163** |
| Commandes distinctes (noms CMAD) | **394** |
| Assignations avec nom de commande lisible | **4 970** (88,3 %) |
| Assignations liées à un contrôle (réf CMAI→DCBM résolue) | **5 136** (91,3 % — 490 réf. non résolues : bindings internes/clavier, ex. « Cue A » réf. 206) |
| Conditions/modifiers (DCDT) | **345** (125 + 220) |
| Cible logicielle | **Traktor Pro 2.12.0** (DDIV) |

### 3.2 Contrôles les plus sollicités (top 10)

| Contrôle | Assignations | | Contrôle | Assignations |
|---|---|---|---|---|
| Right.Loop.Out | 967 | | Left.Loop.Set | 458 |
| Left.Loop.Out | 787 | | Right.Remix Slot. 4 | 421 |
| Right.Jog.Encoder | 161 | | Right.Remix Slot. 2 | 411 |
| Left.Jog.Encoder | 166 | | Right.Loop.In | (top 8) |
| Left.Loop.Set | — | | … | … |

Les jog wheels (Left/Right.Jog.Encoder) et les contrôles de boucle (Loop.In/Out/Set) portent l'essentiel de la densité — signature du style DJTT « tout est re-mappé par couches de modifiers ».

### 3.3 Commandes les plus assignées (top 10)

| Commande (nom CMAD) | Assignations |
|---|---|
| `_(Mod) Super FX Mode Macro FX` | 446 |
| `Echo Mod 2 (Shift + Loop Set Knob)` | 373 |
| `_(Mod) Freeze Mode` | 307 |
| `Super FX Mode Toggle Settings` | 260 |
| `_(Mod) Flux Mode - Hold other deck's Shift + Any Hotcue` | 120 |
| `Super FX Mode Active Leds` | 109 |
| `_(Mod) Panic Button - [Hold Browse Push] + [Press Undo Loop Rec]` | 101 |
| `_(Mod) Hotcue 5-8 on Sample buttons` | 96 |
| `_(Mod) Remix Deck Volumes on FX Units (Hold Mode Button)` | 85 |
| `JogFX L Mod` | 72 |

Échantillon de paires commande↔contrôle (1res assignations) : `EQ A High`↔`Left.Jog.Encoder` · `EQ B High`↔`Left.Jog.Encoder` · `EQ C/D High`↔`Left.Jog.Encoder` · `EQ A/B Mid`↔`Left.Jog.Touch` — les EQ des 4 decks sont derrière la jog gauche (macro JogFX).

### 3.4 Conditions/modifiers et couverture honnête (R-1)

Les **345 DCDT** portent les noms des états de condition : `Left.Shift`, `Right.Shift`, `Left.Sync`, `Right.Sync`, `Left.Cue`, `Right.Cue`, `Left.Play`, `Right.Play`, `Left.Hotcue.1-4`, `Right.Hotcue.1-4`, … — la table des modifiers du mapping. Le préfixe `_(Mod)` des commandes macro confirme l'usage intensif de modifiers (style Controller Manager Traktor 2.x).

**NON décodé sémantiquement** (couverture honnête R-1) : les champs binaires de **CMAD** — canal/message/numéro **MIDI**, mode d'interaction (Hold/Toggle/Increment), assignation des conditions par assignation et les valeurs de paramètres (3 floats par CMAD : constatés 5.0 / 0.5 / 1.0 / 0.0625 selon les entrées, valeur 0x7f=127 présente). La table CC consolidée attendue à la planification n'est donc **pas produite depuis le binaire** ; la documentation QuickGuide est elle-même un guide fonctionnel sans table MIDI. La structure EXTRAITE (commandes ↔ contrôles ↔ conditions) est néanmoins complète et vérifiable mécaniquement — c'est elle qui sert de socle à la calibration G4 (décodeur + interface stable).

## 4. Documentation JPG (lecture VLM — 3/3, zéro 429)

### 4.1 QuickGuide v2.1.0 (guide fonctionnel)
Vue schématique du S4 MK2 avec blocs explicatifs : Panic, FX Units 1-2, JogFX Mode (Group FX / Single FX), Master, Echo Mods, Beat Tap, Timecode Support, Tempo Fader Buttons, X-Fader Assignments, Browser Mode + Full Browser View, Loop Encoders, **Freeze Mode**, Remix Decks C-D, Hybrid Remix Deck (A+B Track/Stem + contrôles Remix), Flux Mode. Le bouton **Shift (Master)** = modificateur principal de secondaires.

### 4.2 Freeze Mode Help v2.1.0
- **Activation** : `Shift + Loop In` (maintenir Shift, appuyer Loop In) — toggle ON/OFF ; sortie : `Loop Out` (ou méthodes alternatives).
- **Slices** : jusqu'à **8 par deck**, déclencheurs 1-8 (deux rangées), combinables.
- **Encodeurs** : taille des slices (sans Shift) / nombre de slices (avec Shift) ; **jogs** : déplacement des slices.
- Indicateurs : LED Shift clignotante + Hotcues + tête de lecture Remix Slice orange.

### 4.3 Manual.jpg (manuel, Beaubryte 2014)
- Sections : Super FX Mode, JogFX (Samples × jog), Echo Mode (Echo Out via Loop buttons), Looping & Tempo (0,01 bpm, range, Freeze), Remix Decks C-D (slots, filtres, volumes, Loops/One Shots), FX Units 1-4 (libres/groupées, presets, édition Controller Manager), Flux Mode & Navigation (Full Browser), Master & Panic.
- **Installation** : Traktor Pro 2 → Settings → **Import** → `KontrolS4beaubryte.TSI` → importer **BOTH** (Controller Settings + Mappings) → `Layouts.tsi` optionnel → vérifier **In-Port actif** dans Controller Manager.
- Lignée : manuel original **Beaubryte 2014** ; le titre du TSI (« v2.1.0 (stewe update) ») atteste une évolution communautaire ultérieure (stewe).

### 4.4 Croisement documentation ↔ extraction binaire

| Documenté (JPG) | Constatté dans le binaire | Verdict |
|---|---|---|
| Freeze Mode (Shift+Loop In, 8 slices, Loop Out) | `_(Mod) Freeze Mode` (307 assign.), `_(Mod) Hotcue 5-8 on Sample buttons` (96), densité Loop.Set/In/Out | ✓ corroboré |
| Super FX Mode | `_(Mod) Super FX Mode Macro FX` (446), `Super FX Mode Toggle Settings` (260), `Super FX Mode Active Leds` (109) | ✓ corroboré |
| Echo Mods 1-2 | `Echo Mod 2 (Shift + Loop Set Knob)` (373) | ✓ corroboré |
| JogFX (jog × FX, Group/Single) | `JogFX L Mod` (72), Left/Right.Jog.Encoder (166/161), EQ ×4 decks derrière la jog | ✓ corroboré |
| Flux Mode | `_(Mod) Flux Mode - Hold other deck's Shift + Any Hotcue` (120) | ✓ corroboré |
| Panic Button | `_(Mod) Panic Button - [Hold Browse Push] + [Press Undo Loop Rec]` (101) | ✓ corroboré |
| Remix Decks C-D / Hybrid | `_(Mod) Remix Deck Volumes on FX Units` (85), Remix Slot. 1-4 (421+…) | ✓ corroboré |
| Sorties LED | `Deck Select LED` (63), `Super FX Mode Active Leds`, `Shifted Options Leds` (60) | ✓ corroboré (face OUT via commandes LED) |
| Installation BOTH settings+mappings | NIXML = préférences + DeviceIO.Config.Controller (blob mapping) dans le même format | ✓ cohérent |

## 5. Écart quantifié : format réel ↔ format spec du trio TSI

| Dimension | Format spec (trio, LEON/TSI Agents 10/26) | Format réel (ce ZIP) | Écart |
|---|---|---|---|
| Racine XML | `NISYSTEM` | **`NIXML`** | majeur (E1-structure) |
| Porteur du mapping | `DEVICE`/`MAPPINGS` éléments XML | **1 Entry** `DeviceIO.Config.Controller` (Base64) | majeur |
| Encodage du mapping | XML lisible | **blob binaire DIOM** 1,35 Mo (trames FourCC BE) | majeur |
| Cible | Traktor Pro 3.11 / S4 **MK3** | Traktor Pro **2.12.0** / S4 **MK2** | génération matérielle/logicielle ≠ |
| Chaînes | attributs XML | **UTF-16-BE** `[u32 n][n×2 o]` | — |
| Assignations | MAPPINGS/Mapping (XML) | **CMAI×5 626** + CMAD (binaire) | volumétrie ×45 vs spec S4 MK3 (~125 in) |
| Contrôles | éléments XML | **DCBM×5 626** (163 contrôles nommés) | — |
| Modifiers | éléments XML | **DCDT×345** (2 tables DDCI/DDCO) | — |
| Métadonnées | — | `cmdr_metadata` JSON 0.9.6.0 (DDIV) | spécifique réel |

**Conclusion G2** : l'écart est structurel et total (racine, porteur, encodage, génération) — exactement le cas d'usage de la clause **R-1** du SKILL tsi-validator (« extension déclarative en cas d'écart avec un TSI réel — interface stable »). Le présent document constitue le **référentiel du format réel** (hiérarchie + conventions + comptes vérifiables) sur lequel G4 bâtit le décodeur `decoder-format-reel.py` et la calibration v1.1.0 des 2 skills. La sous-documentation CMAD (champs MIDI binaires) est assumée et tracée (§3.4).

---
*Artefacts : `scripts/zip-tsi/analyse-tsi-reel.py` (analyseur stdlib, rejouable) · `scripts/zip-tsi/analyse-trois-tsi.json` (sortie machine complète) · `tmp/vlm-quickguide.json`, `tmp/vlm-freeze.json`, `tmp/vlm-manual.json` (lectures VLM brutes).*
