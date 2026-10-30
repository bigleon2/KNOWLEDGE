---
name: gif-animator-pro
version: 2.1.0
description: Moteur d'animation GIF de sprites sur photo (v2, succède à gif-animator) — anime un emoji/sticker/PNG transparent qui traverse l'image avec des démarches au choix : hopscotch (saut à cloche-pied au rythme de la marelle : 3 sauts + pause), bounce (rebonds réguliers), gallop (grand+petit saut), glide (glisse). Ajoute ombre portée dynamique ancrant le sprite au sol, rendu supersamplé anti-aliasé, easing smoothstep par case (vitesse nulle aux réceptions), squash & stretch, palette globale optimisée (GIF léger), boucle infinie. v2.1.0 (Task 8, 2026-10-31) : extension qa-animation — contrôles qualité MÉCANIQUES des livrables animés (scripts/qa_animation.py, PIL uniquement) : frames, boucle, dimensions, poids, durées/frame, palette dominante, mouvement (bbox de différence) + référentiel JSON optionnel + critères subjectifs déclarés NON vérifiés (honnêteté R3 — revue visuelle requise). Utiliser ce skill dès que l'utilisateur demande un GIF animé avancé, un personnage qui saute à cloche-pied/ joue à la marelle, un sprite avec ombre, toute amélioration du rendu du GIF (bords lisses, ancrage au sol), ou une vérification qualité mécanique d'un GIF livrable (qa-animation, QA, référentiel). Dépendance : Pillow uniquement.
license: MIT
---

# GIF Animator Pro Skill (v2)

Moteur d'animation GIF de sprites sur photo — succède à `gif-animator` (v1)
avec démarches variées, ombre portée dynamique et rendu supersamplé.

## Emplacement du skill

**Skill Location** : `{project_path}/skills/gif-animator-pro`

- `scripts/gif_sprite_gif_pro.py` : moteur CLI (Pillow uniquement)
- `scripts/qa_animation.py` : QA mécanique des livrables animés (v2.1.0, Pillow uniquement)
- `assets/emoji_sheep.png` : sprite mouton 🐑 par défaut (OpenMoji 618px, fond transparent)

## Améliorations v2 vs v1 (`gif-animator`)

| Capacité | v1 | v2 (pro) |
|----------|----|----------|
| Démarches | rebonds sinusoïdaux uniques | `hopscotch` (cloche-pied marelle), `bounce`, `gallop`, `glide` |
| Ombre portée | — | ellipse dynamique (rétrécit + s'estompe avec la hauteur) |
| Anti-aliasing | collage direct | supersampling ×2 (rendu doublé + réduction LANCZOS) |
| Vitesse horizontale | linéaire | easing smoothstep par case (vitesse nulle aux réceptions) |
| Rythme marelle | — | cases `H,H,H,R` : 3 sauts + pause, la pause ne fait pas avancer |
| Palette / poids | palette globale | idem (delta-encoding préservé) |

## Démarrage rapide

```bash
# Cas canonique : mouton rasta sautant à cloche-pied de gauche à droite
# au-dessus de la tête, avec ombre et anti-aliasing
python3 {Skill Location}/scripts/gif_sprite_gif_pro.py \
  --photo selfie.jpg \
  --sprite mouton_rasta.png \
  --out sortie.gif \
  --gait hopscotch --direction ltr --flip \
  --baseline 0.27 --amplitude 0.06 --size 0.16 \
  --hops 8 --fps 20 --duration 3.6 --shadow on --supersample 2
```

## Paramètres CLI

| Paramètre | Défaut | Description |
|---|---|---|
| `--photo` | (requis) | photo de fond (JPG/PNG) |
| `--sprite` | (requis) | PNG du sprite, fond transparent requis |
| `--out` | (requis) | GIF de sortie |
| `--gait` | `hopscotch` | `hopscotch` (cloche-pied : H,H,H,R), `bounce`, `gallop` (H,h), `glide` |
| `--direction` | `rtl` | `rtl` droite→gauche, `ltr` gauche→droite |
| `--hops` | `8` | nombre de cases (hopscotch :multiple de 4 = groupes complets 3+pause) |
| `--baseline` | `0.27` | ligne de sol du sprite : fraction de H (≤1) ou pixels — placer AU-DESSUS de la tête du sujet |
| `--amplitude` | `0.055` | hauteur des sauts (fraction ou pixels) |
| `--size` | `0.18` | largeur du sprite (fraction de la largeur ou pixels) |
| `--fps` | `20` | images/seconde |
| `--duration` | `3.5` | durée d'une boucle (s) |
| `--flip` | off | miroir horizontal (orienter la tête dans le sens de marche) |
| `--tilt` | `6` | inclinaison max en degrés (museu levé à l'élan, baissé à la réception) |
| `--stretch` | `0.07` | squash & stretch (0 = off, max 0.25) |
| `--shadow` | `on` | ombre portée dynamique au sol |
| `--supersample` | `2` | facteur anti-aliasing (1 = off, 2-3 conseillé) |
| `--max-width` | `0` | largeur max de sortie (0 = résolution native) |
| `--palette-colors` | `256` | couleurs de la palette GIF globale |

## Fonctionnement

1. **Cases (slots)** : la boucle est découpée en cases selon la démarche
   (`H` saut plein, `h` petit saut, `R` pause, `G` glisse). Une pause ne fait
   PAS avancer le sprite — c'est elle qui crée le rythme marelle.
2. **Horizontal** : progression par case avec easing smoothstep (la vitesse
   s'annule à chaque réception) ; vertical : sinusoïde par case.
3. **Ombre** : ellipse au niveau de la baseline, largeur/alpha décroissants
   avec la hauteur normalisée du saut — ancre le sprite dans la scène.
4. **Rendu** : chaque frame est composée à échelle S (base + ombre + sprite),
   puis réduite en LANCZOS → bords lisses.
5. **Poids** : palette globale unique (frame médiane) + dither NONE → PIL
   n'encode que le rectangle du sprite en delta (GIF ~1-2 Mo en natif).

## QA mécanique des livrables animés (v2.1.0 — qa-animation)

Chaque itération de GIF produit une version livrable — la QA de la session du
2026-10-25 (mouton rasta, 3 versions) fut visuelle à chaque tour alors que des
critères de rejet étaient mécaniquement vérifiables. `qa_animation.py` les
vérifie DÉTERMINISTEMENT à chaque itération, AVANT livraison :

```bash
# Contrôle simple (invariants absolus : format, animation, boucle, mouvement…)
python3 {Skill Location}/scripts/qa_animation.py --gif sortie.gif

# Avec référentiel (attendus de la commande) — échec nominatif si violé
python3 {Skill Location}/scripts/qa_animation.py --gif sortie.gif --referentiel ref.json --json
```

| Contrôle | Mesure | Référentiel (clé JSON) |
|---|---|---|
| format | lisible PIL, format GIF | — |
| animation | is_animated + n_frames ≥ 2 | `frames` |
| boucle | `loop` (0 = infinie, absent = inconnue) | `boucle` |
| dimensions | (l, h) | `dimensions` |
| poids | octets | `poids_max_mo` |
| durées | durée/frame + uniformité | `duree_frame_ms` (valeur ou [min,max]) |
| palette | couleurs distinctes + dominantes top 5 | `palette_dominante` (tolérance ±32/canal) |
| mouvement | bbox de différence frame 0 ↔ médiane | `mouvement` (bool) |

Verdicts : **PASS** (rc 0, tous les contrôles applicables) · **FAIL** (rc 1, au moins
un contrôle violé — listé nominativement) · ERREUR (rc 6, fichier invalide).
**Honnêteté R3** : les critères SUBJECTIFS (« peau trop verte », « yeux au menton »,
« une seule jambe », fidélité au personnage, esthétique) sont LISTÉS dans chaque
rapport comme NON vérifiés mécaniquement — ils restent de la revue visuelle et ne
sont JAMAIS simulés. Workflow recommandé : générer → `qa_animation` (mécanique) →
revue visuelle (subjectif) → itérer ; livrer avec vue-upload (épinglage) et
clore par livraison-garantie (boucle fermée).

## Recettes

```bash
# Cloche-pied discret d'un cœur 💜 (petit sprite, ombre douce)
python3 .../gif_sprite_gif_pro.py --photo p.jpg --sprite coeur.png --out g.gif \
  --gait hopscotch --size 0.08 --amplitude 0.03 --hops 8 --baseline 0.4

# Galop rapide sans supersampling (brouillon rapide)
python3 .../gif_sprite_gif_pro.py ... --gait gallop --fps 24 --duration 2.5 --supersample 1

# Glisse flottante sans ombre
python3 .../gif_sprite_gif_pro.py ... --gait glide --shadow off
```

## Conseils et limites

- **Sens du sprite** : `--flip` oriente le sprite dans le sens de marche
  (le mouton rasta du propriétaire regarde à gauche en source → `--flip`
  pour un parcours gauche→droite).
- **Sprite haut** : pour un sprite portrait (plus haut que large), réduire
  `--size` (~0.14-0.16) pour rester au-dessus de la tête sans toucher le
  bord supérieur.
- **Poids** : si le GIF dépasse la cible, jouer sur `--max-width`, `--fps`,
  `--duration` ; la palette globale fait le reste.
- **Pause marelle** : par conception, l'abscisse est non-décroissante (pas
  strictement croissante) — les pauses gèlent la position.
- **Limites** : sprite statique unique (la démarche est simulée par
  transformations, pas d'articulation réelle) ; pas de détection de visage
  (baseline manuelle) ; 256 couleurs max ; pas d'audio (format GIF).
- **QA** : qa_animation vérifie les critères MÉCANIQUES uniquement — la douleur
  du 2026-10-25 (« peau trop verte », « yeux au menton », « 1 jambe ») était
  subjective et reste à la revue visuelle (listée dans chaque rapport, jamais simulée).
