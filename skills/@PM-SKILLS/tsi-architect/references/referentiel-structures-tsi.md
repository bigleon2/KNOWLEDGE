# Référentiel des structures TSI (skill tsi-architect)

> Source de vérité structuelle — schéma de référence spec-projet-tsi-traktor.md §5 (provenance : reverse-engineering public IvanZ 2014 + articles NI Controller Manager + mappings TSI tiers documentés, cible actuelle S4 MK2 corroborée par le réel DJTT v2.1.0 ; R-1 : extension déclarative si écart avec un TSI réel).

## 1. Squelette canonique

```xml
<?xml version="1.0" encoding="UTF-8"?>
<NISYSTEM VERSION="1">
  <DEVICE NAME="…" TYPE="MIDI" IN_PORT="…" OUT_PORT="…" DECK_TARGET="Focus">
    <MAPPINGS COUNT="N">          <!-- N = nombre exact de MAPPING enfants -->
      <MAPPING NAME="…" TYPE="IN|OUT" GROUP="Deck A|…|Global" CONTROL="…">
        <MODIFIER M1="0|1" … M8="0|1"/>   <!-- optionnel : condition d'assignation -->
        <MIDI CHANNEL="0-15" MESSAGE="NOTE|CC|PB|PC" NUMBER="0-127"
              MODE="Direct|Toggle|Inverse|Increment|Decrement|Reset"/>
        <LED NUMBER="0-127" ON="0-127" OFF="0-127" MODE="Output"/>  <!-- TYPE=OUT uniquement -->
      </MAPPING>
    </MAPPINGS>
  </DEVICE>
</NISYSTEM>
```

## 2. Ordre d'assemblage (ordre de dépendance)

1. Sources de modifiers (CONTROL=`Modifier n`, MODE Toggle/Direct) — inconditionnelles.
2. Mappings conditionnés par ces modifiers (MODIFIER Mx=1) — slices, fonctions de couche.
3. Mappings de base inconditionnels (transport, mixer).
4. Sorties LED (TYPE=OUT), conditionnées par les mêmes modifiers que leurs entrées miroir.

## 3. Règles d'assemblage (rappel E1-E8 — exécution mécanique par tsi-validator)

E1 structure · E2 comptage COUNT exact · E3 attributs (NAME unique, GROUP énuméré) · E4 plages MIDI · E5 anti-doublon (CHANNEL, MESSAGE, NUMBER, conditions) · E6 LED en OUT uniquement · E7 toute couche conditionnée a une source (aucune couche morte) · E8 modifiers binaires 0/1.

## 4. Patterns types

- **Couche simple** : source `Modifier 1` + N mappings conditionnés + LED miroir conditionnée.
- **Double couche (SHIFT gauche/droit)** : M1 = SHIFT gauche, M2 = SHIFT droit ; les combinaisons M1=1 ET M2=1 forment une 4e couche (transitoire) — documenter la priorité.
- **Encodeur double sens** : `Increment` et `Decrement` sur le même NUMBER/CC avec conditions distinctes, ou MODE Increment unique selon le contrôle physique.

## 5. Statuts de calibration

Toute valeur MIDI du référentiel porte un statut : `référence à calibrer` (valeur projet, remplaçable sans changement de pipeline — interface stable) ou `vérifiée` (2 sources concordantes ou TSI réel fourni, ENF-04).
