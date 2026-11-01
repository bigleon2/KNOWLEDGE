# Référence — diamètres officiels des pièces en euros (référence d'échelle)

Source : BCE / spécifications officielles des pièces en euros (diamètres en mm).
Utilisée par la fonction **capture de forme** : la pièce de monnaie posée à côté
de l'objet photographié fournit l'échelle px/mm de la photo.

| Pièce | Diamètre (mm) | Épaisseur (mm) |
|-------|--------------:|---------------:|
| 1 centime   | 16,25 | 2,38 |
| 2 centimes  | 18,75 | 2,35 |
| 5 centimes  | 21,25 | 2,33 |
| 10 centimes | 19,75 | 2,38 |
| 20 centimes | 22,25 | 2,44 |
| 50 centimes | 24,25 | 2,58 |
| 1 euro      | 23,25 | 2,42 |
| 2 euros     | 25,75 | 2,58 |

## Protocole de photographie (pour une déduction fiable)

1. Poser la pièce **dans le même plan** que la pièce à mesurer (même distance
   de l'objectif — jamais devant ni derrière).
2. Face visible de la pièce bien éclairée, contraste suffisant avec le fond.
3. Objectif parallèle au plan (pas de plongée/contre-plongée marquée).
4. Si la dénomination n'est pas précisée, le script retient le candidat
   circulaire le plus proche du diamètre attendu d'une pièce (16-26 mm
   à l'échelle du reste de la scène) — préciser `--coin` pour lever le doute.

## Tolérances

- Détection circulaire : circularité ≥ 0,60, ratio d'aspect 0,85-1,15.
- Erreur attendue sur les cotes déduites : ≤ 5 % (photo conforme au protocole),
  ≤ 8 % en plongée légère (cos θ de l'axe optique).
