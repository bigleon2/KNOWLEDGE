---
name: gif-animator-pro
version: 1.0.0
category: ecosystem
language: fr
tags:
  - gif-anime
  - sprite
  - demarches
  - ombre-portee
  - supersampling
  - pillow
  - plateforme
description: >
  Moteur d'animation GIF de sprites sur photo (v2, succède à gif-animator) — anime
  un emoji/sticker/PNG transparent qui traverse l'image avec des démarches au choix :
  hopscotch (saut à cloche-pied au rythme de la marelle), bounce (rebonds réguliers),
  gallop (grand et petit saut), glide (glisse). Ajoute ombre portée dynamique ancrant
  le sprite au sol, rendu supersamplé anti-aliasé, easing smoothstep par case,
  squash & stretch, palette globale optimisée, boucle infinie. Déclencher pour tout
  GIF animé avancé ou toute amélioration de rendu (bords lisses, ancrage au sol).
  Dépendance : Pillow uniquement.
dependencies:
  - skill: gif-animator
    version: ">=1.0.0"
    used_at: "Moteur v1 prédécesseur — rebonds simples (le présent skill est le moteur avancé)"
read_when:
  - Déclencher quand la demande concerne : un GIF animé avancé (cloche-pied, marelle,
    ombre portée, bords lisses, ancrage au sol), une amélioration du rendu d'un GIF
    de sprite, des démarches multiples.
  - Déclencher si la demande mentionne : saute à cloche-pied, marelle, ombre du
    sprite, GIF pro, anti-aliasing, hopscotch, gallop, glide.
  - Ne pas déclencher pour l'animation simple à rebonds réguliers (gif-animator
    suffit), ni pour la génération d'images par IA (image-generation) — convention
    protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# GIF-ANIMATOR-PRO v1.0.0 — Moteur d'animation avancé (v2)

## §0 — Contexte Système (SHARED v1.7.45)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME importé aux normes de l'écosystème via skill-creator —
directive propriétaire Task 113 (trace 1a201e4bda5a2289). Le corps original était
déjà francophone : il est conservé byte-identité dans `references/plateforme-original.md`
(archive R4), les emojis décoratifs ont été retirés du corps actif (norme écosystème :
zéro emoji). Dépendance unique : Pillow (aucun SDK externe).

## §1 — Spécification fonctionnelle

Successeur de gif-animator (v1) avec démarches variées, ombre portée dynamique et
rendu supersamplé. Apports v2 :

| Capacité | v1 | v2 (pro) |
|----------|----|----------|
| Démarches | rebonds sinusoïdaux uniques | `hopscotch` (cloche-pied marelle), `bounce`, `gallop`, `glide` |
| Ombre portée | aucune | ellipse dynamique (rétrécit et s'estompe avec la hauteur) |
| Anti-aliasing | collage direct | supersampling x2 (rendu doublé + réduction LANCZOS) |
| Vitesse horizontale | linéaire | easing smoothstep par case (vitesse nulle aux réceptions) |
| Rythme marelle | aucun | cases `H,H,H,R` : 3 sauts + pause, la pause ne fait pas avancer |
| Palette / poids | palette globale | identique (delta-encoding préservé) |

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}gif-animator-pro/` — moteur CLI : `scripts/gif_sprite_gif_pro.py`
(Pillow uniquement) ; sprite par défaut : `assets/emoji_sheep.png` (mouton OpenMoji
618 px, fond transparent).

### Démarrage rapide

```bash
# Cas canonique : mouton sautant à cloche-pied de gauche à droite au-dessus
# de la tête, avec ombre et anti-aliasing
python3 {{SKILLS_ROOT}}gif-animator-pro/scripts/gif_sprite_gif_pro.py \
  --photo selfie.jpg \
  --sprite mouton_rasta.png \
  --out sortie.gif \
  --gait hopscotch --direction ltr --flip \
  --baseline 0.27 --amplitude 0.06 --size 0.16 \
  --hops 8 --fps 20 --duration 3.6 --shadow on --supersample 2
```

### Paramètres CLI

| Paramètre | Défaut | Description |
|---|---|---|
| `--photo` | (requis) | photo de fond (JPG/PNG) |
| `--sprite` | (requis) | PNG du sprite, fond transparent requis |
| `--out` | (requis) | GIF de sortie |
| `--gait` | `hopscotch` | `hopscotch` (cloche-pied : H,H,H,R), `bounce`, `gallop` (H,h), `glide` |
| `--direction` | `rtl` | `rtl` droite vers gauche, `ltr` gauche vers droite |
| `--hops` | `8` | nombre de cases (hopscotch : multiple de 4 = groupes complets 3 sauts + pause) |
| `--baseline` | `0.27` | ligne de sol du sprite (fraction de H ou pixels) — AU-DESSUS de la tête |
| `--amplitude` | `0.055` | hauteur des sauts |
| `--size` | `0.18` | largeur du sprite (fraction de la largeur ou pixels) |
| `--fps` | `20` | images par seconde |
| `--duration` | `3.5` | durée d'une boucle en secondes |
| `--flip` | désactivé | miroir horizontal (orienter la tête dans le sens de marche) |
| `--tilt` | `6` | inclinaison max en degrés |
| `--stretch` | `0.07` | squash & stretch (0 = désactivé, max 0.25) |
| `--shadow` | `on` | ombre portée dynamique au sol |
| `--supersample` | `2` | facteur anti-aliasing (1 = désactivé, 2-3 conseillé) |
| `--max-width` | `0` | largeur max de sortie (0 = résolution native) |
| `--palette-colors` | `256` | couleurs de la palette GIF globale |

### Fonctionnement

La boucle est découpée en cases selon la démarche (`H` saut plein, `h` petit saut,
`R` pause, `G` glisse) ; la pause ne fait PAS avancer le sprite — c'est elle qui
crée le rythme marelle (abscisse non-décroissante). Progression horizontale avec
easing smoothstep, verticale sinusoïdale par case ; ombre en ellipse au niveau de
la baseline, largeur et alpha décroissants avec la hauteur ; chaque frame composée
à échelle de supersampling puis réduite en LANCZOS ; palette globale unique sans
tramage (GIF d'environ 1-2 Mo).

### Conseils et limites

`--flip` oriente le sprite dans le sens de marche ; pour un sprite portrait (plus
haut que large), réduire `--size` (environ 0.14-0.16) ; si le GIF dépasse la cible,
jouer sur `--max-width`, `--fps`, `--duration`. Limites : sprite statique unique
(démarche simulée par transformations, pas d'articulation), pas de détection de
visage (baseline manuelle), 256 couleurs max, pas d'audio.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| gif-animator | Prédécesseur | Moteur v1 simple — le présent skill est le moteur avancé |
| image-edit | Frontière | Retouche générative d'une image fixe, pas d'animation |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, retrait des emojis décoratifs (norme zéro emoji) ; corps original français conservé byte-identité references/plateforme-original.md (R4) |
