---
name: gif-animator
version: 1.0.0
category: ecosystem
language: fr
tags:
  - gif-anime
  - sprite
  - photo
  - pillow
  - animation
  - plateforme
description: >
  Création de GIF animés à partir d'une photo en y superposant un sprite (emoji,
  sticker, PNG à fond transparent) qui traverse l'image en sautant par-dessus un
  point choisi (ex. la tête du sujet) : trajectoire parabolique, squash & stretch,
  inclinaison, boucle infinie, palette globale optimisée pour un fichier léger.
  Déclencher quand l'utilisateur demande de transformer une photo en GIF animé, de
  faire sauter ou se déplacer un emoji/un sticker/un personnage sur une image, ou
  de produire un sticker animé en boucle. Dépendance : Pillow uniquement.
dependencies:
  - skill: gif-animator-pro
    version: ">=1.0.0"
    used_at: "Moteur v2 successeur — démarches multiples, ombre portée, supersampling"
read_when:
  - Déclencher quand la demande concerne : animer un sprite sur une photo (sauts
    paraboliques, traversée de droite à gauche ou l'inverse), produire un GIF en
    boucle légèrement compressé.
  - Déclencher si la demande mentionne : GIF animé, faire sauter un emoji/un mouton/
    un sticker sur une photo, animer une image, sprite qui traverse.
  - Ne pas déclencher pour les rendus avancés (cloche-pied, ombre portée, ombre
    dynamique, anti-aliasing supersamplé → gif-animator-pro), ni pour la génération
    d'images par IA (image-generation) — convention protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# GIF-ANIMATOR v1.0.0 — Sprite animé sur photo (moteur v1)

## §0 — Contexte Système (SHARED v1.7.47)

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

Un sprite (PNG à fond transparent — emoji, sticker) traverse une photo en enchaînant
des petits sauts paraboliques au-dessus d'une ligne de base (par exemple le sommet
de la tête du sujet), en boucle infinie. Moteur v1 : rebonds sinusoïdaux réguliers —
pour les démarches variées (cloche-pied, galop, glisse), l'ombre portée dynamique et
le supersampling, utiliser le successeur gif-animator-pro.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}gif-animator/` — générateur CLI : `scripts/gif_sprite_gif.py`
(Pillow uniquement) ; sprite par défaut : `assets/emoji_sheep.png` (mouton OpenMoji
618 px, fond transparent, orienté vers la gauche).

### Démarrage rapide

```bash
# Cas canonique : mouton qui saute de droite à gauche au-dessus de la tête
python3 {{SKILLS_ROOT}}gif-animator/scripts/gif_sprite_gif.py \
  --photo selfie.jpg \
  --sprite {{SKILLS_ROOT}}gif-animator/assets/emoji_sheep.png \
  --out sortie.gif \
  --direction rtl --baseline 0.27 --amplitude 0.055 \
  --size 0.18 --hops 7 --fps 20 --duration 3.2
```

### Paramètres CLI

| Paramètre | Défaut | Description |
|---|---|---|
| `--photo` | (requis) | photo de fond (JPG/PNG) |
| `--sprite` | (requis) | PNG du sprite, fond transparent requis |
| `--out` | (requis) | chemin du GIF de sortie (répertoires créés si absents) |
| `--direction` | `rtl` | `rtl` = droite vers gauche, `ltr` = gauche vers droite |
| `--baseline` | `0.27` | ligne de sol du sprite : fraction de H (jusqu'à 1) ou pixels (plus de 1) — placer AU-DESSUS de la tête du sujet |
| `--amplitude` | `0.055` | hauteur des sauts (fraction de H ou pixels) |
| `--size` | `0.18` | largeur du sprite (fraction de la largeur ou pixels) |
| `--hops` | `7` | nombre de sauts par boucle ; `0` = glisse sans sauter |
| `--fps` | `20` | images par seconde |
| `--duration` | `3.2` | durée d'une boucle en secondes |
| `--flip` | désactivé | miroir horizontal du sprite (orienter la tête dans le sens de marche) |
| `--stretch` | `0.06` | intensité du squash & stretch (0 = désactivé, max 0.25) |
| `--tilt` | `5` | inclinaison max en degrés (museau levé en montée, baissé en descente) |
| `--max-width` | `0` | redimensionne la sortie à cette largeur (0 = résolution native) |
| `--palette-colors` | `256` | couleurs de la palette GIF globale (16 à 256) |

### Fonctionnement et optimisation

Le sprite est rogné sur son enveloppe alpha puis redimensionné ; la trajectoire
traverse toute la largeur (entrée et sortie hors cadre) avec `--hops` sauts
sinusoïdaux au-dessus de `--baseline` ; le rendu applique squash & stretch ancré
aux pieds et inclinaison selon la phase. Une palette globale unique est construite
depuis la frame médiane et appliquée sans tramage : PIL n'encode alors que le
rectangle du sprite en delta (un GIF d'environ 1 Mo au lieu de 40 Mo en natif).

### Conseils et limites

- Choisir `--baseline` en repérant la hauteur relative de la tête (ex. crâne à
  35 % de H, baseline à 27 %) et vérifier en extrayant quelques frames avant
  livraison.
- Le sprite mouton fourni regarde à gauche (adapté à `rtl`) ; ajouter `--flip`
  pour un sprite orienté à droite allant vers la gauche.
- Fond transparent du sprite OBLIGATOIRE (sinon rectangle visible) ; si le GIF
  dépasse environ 3 Mo, jouer sur `--max-width`, `--fps`, `--duration`.
- Limites : pas de détection de visage (baseline manuelle), pas d'audio (format
  GIF), 256 couleurs maximum.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| gif-animator-pro | Successeur | Démarches multiples, ombre portée, supersampling — le présent skill reste le moteur simple |
| image-edit | Frontière | Retouche générative d'une image fixe, pas d'animation |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, retrait des emojis décoratifs (norme zéro emoji) ; corps original français conservé byte-identité references/plateforme-original.md (R4) |
