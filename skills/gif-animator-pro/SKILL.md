---
name: gif-animator-pro
description: Moteur d'animation GIF de sprites sur photo (v2, succède à gif-animator) — anime un emoji/sticker/PNG transparent qui traverse l'image avec des démarches au choix : hopscotch (saut à cloche-pied au rythme de la marelle : 3 sauts + pause), bounce (rebonds réguliers), gallop (grand+petit saut), glide (glisse). Ajoute ombre portée dynamique ancrant le sprite au sol, rendu supersamplé anti-aliasé, easing smoothstep par case (vitesse nulle aux réceptions), squash & stretch, palette globale optimisée (GIF léger), boucle infinie. Utiliser ce skill dès que l'utilisateur demande un GIF animé avancé, un personnage qui saute à cloche-pied/ joue à la marelle, un sprite avec ombre, ou toute amélioration du rendu du GIF (bords lisses, ancrage au sol). Dépendance : Pillow uniquement.
license: MIT
---

## §0 — Contexte Système (SHARED v1.7.32)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



# GIF Animator Pro Skill (v2)

Moteur d'animation GIF de sprites sur photo — succède à `gif-animator` (v1)
avec démarches variées, ombre portée dynamique et rendu supersamplé.

## Emplacement du skill

**Skill Location** : `{project_path}/skills/gif-animator-pro`

- `scripts/gif_sprite_gif_pro.py` : moteur CLI (Pillow uniquement)
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
