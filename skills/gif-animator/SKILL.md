---
name: gif-animator
description: Crée des GIF animés à partir d'une photo en y superposant un sprite (emoji, sticker, PNG à fond transparent) qui traverse l'image en sautant par-dessus un point choisi (ex. la tête du sujet) : trajectoire parabolique, squash & stretch, inclinaison, boucle infinie, palette globale optimisée pour un fichier léger. Utiliser ce skill dès que l'utilisateur demande de transformer une photo en GIF animé, de faire sauter ou se déplacer un emoji/un mouton/un sticker sur une image, d'animer un personnage de droite à gauche, ou de produire un sticker animé en boucle. Dépendance : Pillow uniquement (pas de SDK externe).
license: MIT
---

# GIF Animator Skill

Création de GIF animés : un sprite (emoji/sticker PNG transparent) traverse une
photo en enchaînant des petits sauts paraboliques au-dessus d'une ligne de base
(par exemple le sommet de la tête du sujet), en boucle infinie.

## Emplacement du skill

**Skill Location** : `{project_path}/skills/gif-animator`

- `scripts/gif_sprite_gif.py` : générateur CLI (Pillow uniquement)
- `assets/emoji_sheep.png` : sprite mouton 🐑 par défaut (OpenMoji 618px, fond transparent, orienté vers la gauche)

## Démarrage rapide

```bash
# Cas canonique : mouton 🐑 qui saute de droite à gauche au-dessus de la tête
python3 {Skill Location}/scripts/gif_sprite_gif.py \
  --photo selfie.jpg \
  --sprite {Skill Location}/assets/emoji_sheep.png \
  --out sortie.gif \
  --direction rtl --baseline 0.27 --amplitude 0.055 \
  --size 0.18 --hops 7 --fps 20 --duration 3.2
```

## Paramètres CLI

| Paramètre | Défaut | Description |
|---|---|---|
| `--photo` | (requis) | photo de fond (JPG/PNG) |
| `--sprite` | (requis) | PNG du sprite, fond transparent requis |
| `--out` | (requis) | chemin du GIF de sortie (répertoires créés si absents) |
| `--direction` | `rtl` | `rtl` = droite→gauche, `ltr` = gauche→droite |
| `--baseline` | `0.27` | ligne de sol du sprite : fraction de H (≤1) ou pixels (>1). Choisir une valeur AU-DESSUS de la tête du sujet (ex. tête à ~35 % de H → baseline 0.27) |
| `--amplitude` | `0.055` | hauteur des sauts (fraction de H ou pixels) |
| `--size` | `0.18` | largeur du sprite (fraction de la largeur ou pixels) |
| `--hops` | `7` | nombre de sauts par boucle ; `0` = glisse sans sauter |
| `--fps` | `20` | images par seconde |
| `--duration` | `3.2` | durée d'une boucle en secondes |
| `--flip` | off | miroir horizontal du sprite (si le sprite regarde à droite et va vers la gauche) |
| `--stretch` | `0.06` | intensité du squash & stretch (0 = désactivé, max 0.25) |
| `--tilt` | `5` | inclinaison max en degrés (museau levé en montée, baissé en descente) |
| `--max-width` | `0` | redimensionne la sortie à cette largeur (0 = résolution native) |
| `--palette-colors` | `256` | couleurs de la palette GIF globale (16-256) |

## Fonctionnement

1. Le sprite est rogner sur son enveloppe alpha, redimensionné à `--size`.
2. Trajectoire : traversée linéaire sur toute la largeur (`margin = largeur du
   sprite` de chaque côté, entrée/sortie hors cadre), avec `--hops` sauts
   sinusoïdaux par boucle au-dessus de `--baseline`.
3. Rendu : squash & stretch ancré aux « pieds » du sprite, inclinaison selon la
   phase du saut, collage alpha sur une copie de la photo pour chaque frame.
4. Optimisation taille : une **palette globale unique** est construite depuis la
   frame médiane et appliquée à toutes les frames avec `dither=NONE` — les
   pixels identiques entre frames restent identiques, PIL n'encode alors que le
   rectangle du sprite en delta (un GIF de ~1 Mo au lieu de ~40 Mo en natif).

## Recettes

```bash
# Emoji qui glisse sans sauter (hops 0), vers la droite, sprite orienté à gauche
python3 .../gif_sprite_gif.py --photo p.jpg --sprite s.png --out g.gif \
  --direction ltr --flip --hops 0 --baseline 0.20 --amplitude 0

# Sortie plus légère pour messagerie (720px de large)
python3 .../gif_sprite_gif.py ... --max-width 720

# Petits sauts discrets d'un cœur 💜 au-dessus d'un objet
python3 .../gif_sprite_gif.py --photo p.jpg --sprite coeur.png --out g.gif \
  --baseline 0.4 --amplitude 0.03 --size 0.08 --hops 10
```

## Conseils et limites

- **Choix de `--baseline`** : repérer la position verticale relative de la tête
  du sujet dans la photo (ex. sommet du crâne à ~35 % de la hauteur) et placer
  la baseline 5 à 10 points au-dessus. Vérifier le résultat en extrayant
  quelques frames (`PIL Image.seek(i)`) avant livraison.
- **Sens du sprite** : l'emoji mouton 🐑 fourni regarde à gauche (adapté à
  `rtl`) ; pour un sprite regardant à droite qui va vers la gauche, ajouter
  `--flip`.
- **Fond transparent obligatoire** : un sprite avec fond opaque donnera un
  rectangle visible. En cas de fond blanc uni, le détourer d'abord.
- **Poids du fichier** : jouer sur `--max-width`, `--fps` et `--duration` si le
  GIF dépasse ~3 Mo ; la palette globale fait le reste.
- **Limites** : pas de détection de visage automatique (baseline manuelle) ;
  pas d'audio (format GIF) ; 256 couleurs max (palette globale, tramage désactivé).
