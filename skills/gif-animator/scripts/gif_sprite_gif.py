#!/usr/bin/env python3
"""Génération d'un GIF animé : sprite (emoji/sticker) sautant au-dessus d'une photo.

Le sprite traverse la photo (droite -> gauche par défaut) en enchaînant des
petits sauts paraboliques au-dessus d'une ligne de base choisie (par exemple
le sommet de la tête du sujet). Effets inclus : squash & stretch à
l'atterrissage, légère inclinaison pendant le saut, boucle infinie.

Dépendance : Pillow uniquement.

Exemple :
    python gif_sprite_gif.py --photo selfie.jpg --sprite mouton.png \
        --out sortie.gif --direction rtl --baseline 0.27 --amplitude 0.055 \
        --size 0.18 --hops 7 --fps 20 --duration 3.2
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image


def parse_length(value: str, total: int) -> int:
    """Convertit une longueur en pixels.

    Accepte une fraction (0 < v <= 1, relative à ``total``) ou des pixels
    absolus (v > 1). Le suffixe optionnel 'px' force l'interprétation pixels.
    """
    txt = str(value).strip().lower().replace("px", "")
    v = float(txt)
    if 0 < v <= 1.0:
        return max(1, int(round(v * total)))
    return max(1, int(round(v)))


def load_sprite(path: Path, target_w: int, flip: bool) -> Image.Image:
    """Charge le sprite, le rogne sur son contenu opaque puis le redimensionne."""
    sprite = Image.open(path).convert("RGBA")
    bbox = sprite.getchannel("A").getbbox()
    if bbox:
        sprite = sprite.crop(bbox)
    ratio = target_w / sprite.width
    target_h = max(1, int(round(sprite.height * ratio)))
    sprite = sprite.resize((target_w, target_h), Image.LANCZOS)
    if flip:
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
    return sprite


def build_frames(
    base: Image.Image,
    sprite: Image.Image,
    baseline_y: int,
    amplitude: int,
    n_hops: int,
    n_frames: int,
    direction: str,
    stretch: float,
    tilt_deg: float,
) -> list[Image.Image]:
    """Compose chaque frame du GIF (base + sprite en trajectoire sautante)."""
    width, _height = base.size
    sw, sh = sprite.size
    margin = sw
    if direction == "rtl":
        x_start, x_end = width, -margin
    else:
        x_start, x_end = -margin, width

    frames: list[Image.Image] = []
    for i in range(n_frames):
        t = i / n_frames
        cx = x_start + t * (x_end - x_start) + sw / 2.0

        hop_phase = (t * n_hops) % 1.0 if n_hops > 0 else 0.0
        hop_h = amplitude * math.sin(math.pi * hop_phase)
        k = abs(math.cos(math.pi * hop_phase)) if n_hops > 0 else 0.0

        # Squash & stretch : écrasé à l'atterrissage, étiré à l'apex.
        sx = 1.0 + stretch * k - stretch * 0.5 * (1.0 - k)
        sy = 1.0 - stretch * k + stretch * 0.5 * (1.0 - k)
        fw = max(1, int(round(sw * sx)))
        fh = max(1, int(round(sh * sy)))
        frame_sprite = sprite.resize((fw, fh), Image.BICUBIC)

        # Inclinaison : museau vers le haut en montée, vers le bas en descente.
        tilt = -tilt_deg * math.cos(math.pi * hop_phase) if n_hops > 0 else 0.0
        if abs(tilt) > 0.3:
            frame_sprite = frame_sprite.rotate(
                tilt, expand=True, resample=Image.BICUBIC
            )

        bottom_y = baseline_y - hop_h
        px = int(round(cx - frame_sprite.width / 2.0))
        py = int(round(bottom_y - frame_sprite.height))

        frame = base.copy()
        frame.paste(frame_sprite, (px, py), frame_sprite)
        frames.append(frame.convert("RGB"))
    return frames


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI : parse les arguments et génère le GIF."""
    parser = argparse.ArgumentParser(
        description="Anime un sprite (emoji/sticker) qui saute au-dessus d'une "
        "photo et exporte un GIF en boucle infinie."
    )
    parser.add_argument("--photo", required=True, help="chemin de la photo de fond")
    parser.add_argument("--sprite", required=True, help="PNG du sprite (fond transparent)")
    parser.add_argument("--out", required=True, help="chemin du GIF de sortie")
    parser.add_argument(
        "--direction",
        choices=["rtl", "ltr"],
        default="rtl",
        help="sens de traversée : rtl (droite->gauche, défaut) ou ltr",
    )
    parser.add_argument(
        "--baseline",
        default="0.27",
        help="hauteur de la ligne de sol du sprite : fraction de H (<=1) ou "
        "pixels (>1). Défaut : 0.27 (au-dessus de la tête d'un selfie)",
    )
    parser.add_argument(
        "--amplitude",
        default="0.055",
        help="hauteur des sauts : fraction de H ou pixels. Défaut : 0.055",
    )
    parser.add_argument(
        "--size",
        default="0.18",
        help="largeur du sprite : fraction de la largeur ou pixels. Défaut : 0.18",
    )
    parser.add_argument("--hops", type=int, default=7, help="nombre de sauts (0 = glisse)")
    parser.add_argument("--fps", type=int, default=20, help="images par seconde (défaut : 20)")
    parser.add_argument(
        "--duration", type=float, default=3.2, help="durée d'une boucle en secondes (défaut : 3.2)"
    )
    parser.add_argument("--flip", action="store_true", help="miroir horizontal du sprite")
    parser.add_argument(
        "--stretch", type=float, default=0.06, help="intensité squash & stretch (0 = off)"
    )
    parser.add_argument(
        "--tilt", type=float, default=5.0, help="inclinaison max du sprite en degrés"
    )
    parser.add_argument(
        "--max-width", type=int, default=0, help="redimensionne la sortie à cette largeur (0 = natif)"
    )
    parser.add_argument(
        "--palette-colors",
        type=int,
        default=256,
        help="nombre de couleurs de la palette GIF globale (16-256, défaut : 256)",
    )
    args = parser.parse_args(argv)

    photo_path = Path(args.photo)
    sprite_path = Path(args.sprite)
    out_path = Path(args.out)
    if not photo_path.is_file():
        parser.error(f"photo introuvable : {photo_path}")
    if not sprite_path.is_file():
        parser.error(f"sprite introuvable : {sprite_path}")

    base = Image.open(photo_path).convert("RGB")
    if args.max_width and base.width > args.max_width:
        ratio = args.max_width / base.width
        base = base.resize(
            (args.max_width, int(round(base.height * ratio))), Image.LANCZOS
        )

    width, height = base.size
    sprite_w = parse_length(args.size, width)
    sprite = load_sprite(sprite_path, sprite_w, args.flip)
    baseline_y = parse_length(args.baseline, height)
    amplitude = parse_length(args.amplitude, height)
    if amplitude >= baseline_y:
        amplitude = max(8, baseline_y // 3)

    n_frames = max(2, int(round(args.duration * args.fps)))
    frames = build_frames(
        base,
        sprite,
        baseline_y,
        amplitude,
        max(0, args.hops),
        n_frames,
        args.direction,
        max(0.0, min(args.stretch, 0.25)),
        max(0.0, min(args.tilt, 20.0)),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    per_frame_ms = max(20, int(round(1000 / args.fps)))

    # Palette globale unique : les pixels identiques entre frames restent
    # identiques après quantification (dither désactivé), ce qui permet à PIL
    # de n'encoder que le rectangle du sprite en delta -> GIF léger.
    ref_palette = frames[len(frames) // 2].quantize(
        colors=max(16, min(args.palette_colors, 256)),
        method=Image.Quantize.MEDIANCUT,
    )
    frames_p = [
        f.quantize(palette=ref_palette, dither=Image.Dither.NONE) for f in frames
    ]

    frames_p[0].save(
        out_path,
        save_all=True,
        append_images=frames_p[1:],
        loop=0,
        duration=per_frame_ms,
        optimize=True,
        disposal=1,
    )

    size_kb = out_path.stat().st_size / 1024
    print(
        f"GIF généré : {out_path} | {width}x{height}px | {len(frames)} frames "
        f"| {per_frame_ms} ms/frame | {size_kb:.0f} Ko"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
