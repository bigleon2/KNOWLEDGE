# Matrice de couverture S4 MK2 — Freeze Mode de référence (multi-shift-architect)

> Matrice de référence machine-parsable (format auditée par `scripts/tests-projet-tsi/test-multi-shift-architect.py`).
> Invariants : couverture 100 % (toute cellule remplie : fonction ou « — » inactif documenté) · zéro conflit (aucune fonction dupliquée dans une même couche) · transitions complètes (chaque couche non-BASE documentée ci-dessous). Statuts de calibration : référentiel de référence à calibrer (R-1/R-2).

| Contrôle | BASE | SHIFT-G | SHIFT-D | FREEZE (M1=1) |
|---|---|---|---|---|
| Pad 1 | Hotcue 1 | Hotcue Delete 1 | — | Slice 1 |
| Pad 2 | Hotcue 2 | Hotcue Delete 2 | — | Slice 2 |
| Pad 3 | Hotcue 3 | Hotcue Delete 3 | — | Slice 3 |
| Pad 4 | Hotcue 4 | Hotcue Delete 4 | — | Slice 4 |
| Pad 5 | Hotcue 5 | Hotcue Delete 5 | — | Slice 5 |
| Pad 6 | Hotcue 6 | Hotcue Delete 6 | — | Slice 6 |
| Pad 7 | Hotcue 7 | Hotcue Delete 7 | — | Slice 7 |
| Pad 8 | Hotcue 8 | Hotcue Delete 8 | — | Slice 8 |
| PLAY (deck A) | Play/Pause | — | Play/Pause deck C | — |
| SYNC (deck A) | Sync | Master tempo | — | — |
| CUE (deck A) | Cue/Set | — | — | — |
| LOOP IN (deck A) | Loop In | Modifier 1 (activation FREEZE) | — | Loop In (décalage du slicer) |
| LOOP OUT (deck A) | Loop Out | — | — | Loop Out |
| Encodeur LOOP (deck A) | Loop Size (Inc/Dec) | — | — | Slice Size (Inc/Dec) |
| Fader canal A | Volume | — | — | — |
| Crossfader | Crossfader position | — | — | — |
| SHIFT gauche (maintien) | Layer SHIFT-G | — | — | — |
| SHIFT droit (maintien) | Layer SHIFT-D | — | — | — |
| LED Freeze | — | — | — | Freeze LED ON (127) |
| LED PLAY (deck A) | Play LED | — | — | Play LED |

## Transitions et activations (couche par couche)

- SHIFT-G : activation = maintien SHIFT gauche ; retour = relâche (couche momentanée, priorité SOUS FREEZE).
- SHIFT-D : activation = maintien SHIFT droit ; retour = relâche (couche momentanée, redirection decks C/D).
- FREEZE (M1=1) : activation = SHIFT gauche + LOOP IN (mapping CONTROL « Modifier 1 », MODE Toggle — source de couche, règle E7) ; retour = nouvelle pression SHIFT gauche + LOOP IN (toggle off) ; LED Freeze en miroir de l'état M1.

## Conflits arbitrés

- Chevauchement SHIFT-G × FREEZE sur LOOP IN : FREEZE prioritaire (activation toggle), SHIFT-G+LOOP IN n'a pas d'autre affectation.
- Partage des numéros de pads entre BASE (Hotcues) et FREEZE (Slices) : autorisé — conditions de modifier distinctes (E5 : unicité par CHANNEL+MESSAGE+NUMBER+conditions).
