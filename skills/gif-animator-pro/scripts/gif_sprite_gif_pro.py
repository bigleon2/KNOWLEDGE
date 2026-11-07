#!/usr/bin/env python3
"""gif-animator-pro : moteur d'animation GIF de sprites sur photo (v2).

Nouveautés par rapport à gif-animator v1 :
- démarches (gaits) : ``hopscotch`` (cloche-pied, rythme marelle 3 sauts +
  pause), ``bounce`` (rebonds réguliers), ``gallop`` (grand + petit saut),
  ``glide`` (glisse sans saut) ;
- ombre portée dynamique au sol : elle rétrécit et s'estompe quand le sprite
  s'élève, ce qui l'ancre visuellement dans la scène ;
- rendu supersamplé (calcul à échelle doublée puis réduction LANCZOS) pour
  des bords de sprite lisses ;
- easing smoothstep par case : la vitesse horizontale s'annule à chaque
  réception, ce qui donne le rythme saut-pause de la marelle ;
- squash & stretch en deux phases (élan étiré, réception écrasée).

Dépendance : Pillow uniquement (aucun SDK externe).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

GAIT_PATTERNS = {
    "hopscotch": ["H", "H", "H", "R"],
    "bounce": ["H"],
    "gallop": ["H", "h"],
    "glide": ["G"],
}
AMPLITUDE_RATIO = {"H": 1.0, "h": 0.45, "R": 0.12, "G": 0.0}


def parse_length(value: str, total: int) -> int:
    """Convertit une longueur : fraction (0 < v <= 1) ou pixels (> 1, 'px' ok)."""
    txt = str(value).strip().lower().replace("px", "")
    v = float(txt)
    if 0 < v <= 1.0:
        return max(1, int(round(v * total)))
    return max(1, int(round(v)))


def load_sprite(path: Path, target_w: int, flip: bool, scale: int) -> Image.Image:
    """Charge le sprite, rogne sur l'alpha, redimensionne (échelle S) et retourne."""
    sprite = Image.open(path).convert("RGBA")
    bbox = sprite.getchannel("A").getbbox()
    if bbox:
        sprite = sprite.crop(bbox)
    ratio = target_w * scale / sprite.width
    target_h = max(1, int(round(sprite.height * ratio)))
    sprite = sprite.resize((target_w * scale, target_h * scale), Image.LANCZOS)
    if flip:
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
    return sprite


def build_slots(gait: str, hops: int) -> list[str]:
    """Construit la séquence de cases (H saut, h petit saut, R pause, G glisse)."""
    pattern = GAIT_PATTERNS[gait]
    if gait == "glide":
        return ["G"]
    slots: list[str] = []
    while len(slots) < hops:
        slots.extend(pattern)
    return slots[: max(1, hops)]


def slot_progress(slots: list[str]) -> tuple[list[float], list[float]]:
    """Progression horizontale par case : les pauses n'avancent pas."""
    n_advance = sum(1 for s in slots if s in ("H", "h"))
    step = 1.0 / max(1, n_advance)
    starts: list[float] = []
    prog = 0.0
    for s in slots:
        starts.append(prog)
        prog += step if s in ("H", "h") else 0.0
    return starts, [step if s in ("H", "h") else 0.0 for s in slots]


def smoothstep(u: float) -> float:
    """Easing smoothstep : vitesse nulle aux bornes de la case."""
    return u * u * (3.0 - 2.0 * u)


def draw_shadow(
    overlay: Image.Image,
    cx: float,
    baseline_y: int,
    h_norm: float,
    sprite_w: int,
    sprite_h: int,
) -> None:
    """Dessine l'ombre portée au sol (rétrécit et s'estompe en hauteur)."""
    width = sprite_w * (1.08 - 0.30 * h_norm)
    height = max(4, sprite_h * 0.13 * (1.0 - 0.30 * h_norm))
    alpha = int(80 * (1.0 - 0.55 * h_norm))
    if alpha <= 2:
        return
    draw = ImageDraw.Draw(overlay)
    cy = baseline_y + height * 0.35
    draw.ellipse(
        (cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2),
        fill=(20, 20, 30, alpha),
    )


def build_frames(
    base: Image.Image,
    sprite: Image.Image,
    args: argparse.Namespace,
) -> list[Image.Image]:
    """Compose chaque frame (ombre + sprite) à l'échelle S puis réduit."""
    width, height = base.size
    scale = max(1, min(3, args.supersample))
    sw_s, sh_s = sprite.size
    margin = sw_s // scale
    if args.direction == "rtl":
        x_start, x_end = width, -margin
    else:
        x_start, x_end = -margin, width

    baseline_y = parse_length(args.baseline, height)
    amplitude = parse_length(args.amplitude, height)
    if amplitude >= baseline_y:
        amplitude = max(8, baseline_y // 3)

    slots = build_slots(args.gait, max(1, args.hops))
    n_slots = len(slots)
    starts, steps = slot_progress(slots)

    n_frames = max(2, int(round(args.duration * args.fps)))
    base_s = (
        base.resize((width * scale, height * scale), Image.LANCZOS)
        if scale > 1
        else base
    )
    base_ref = base_s.convert("RGBA")

    frames: list[Image.Image] = []
    for i in range(n_frames):
        t = i / n_frames
        idx = min(n_slots - 1, int(t * n_slots))
        u = t * n_slots - idx
        eased = smoothstep(u)
        travel = x_end - x_start
        cx = x_start + travel * (starts[idx] + eased * steps[idx]) + sw_s / 2.0

        kind = slots[idx]
        amp = amplitude * AMPLITUDE_RATIO[kind] * scale
        hop_h = amp * math.sin(math.pi * u) if kind != "G" else 0.0
        k = abs(math.cos(math.pi * u)) if kind != "G" else 0.0

        stretch = max(0.0, min(args.stretch, 0.25))
        sx = 1.0 + stretch * k - stretch * 0.5 * (1.0 - k)
        sy = 1.0 - stretch * k + stretch * 0.5 * (1.0 - k)
        fw = max(1, int(round(sw_s * sx)))
        fh = max(1, int(round(sh_s * sy)))
        frame_sprite = sprite.resize((fw, fh), Image.BICUBIC)

        tilt = -args.tilt * math.cos(math.pi * u) if kind in ("H", "h") else 0.0
        if abs(tilt) > 0.3:
            frame_sprite = frame_sprite.rotate(tilt, expand=True, resample=Image.BICUBIC)

        bottom_y = (baseline_y - hop_h / scale) * scale
        px = int(round(cx - fw / 2.0))
        py = int(round(bottom_y - fh))

        frame = base_ref.copy()
        if args.shadow != "off" and kind != "G":
            overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            h_norm = min(1.0, hop_h / max(1, amplitude * scale))
            draw_shadow(overlay, cx, baseline_y * scale, h_norm, sw_s, sh_s)
            frame = Image.alpha_composite(frame, overlay)
        frame.paste(frame_sprite, (px, py), frame_sprite)

        if scale > 1:
            frame = frame.convert("RGB").resize((width, height), Image.LANCZOS)
        frames.append(frame.convert("RGB"))
    return frames


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI : parse les arguments et génère le GIF."""
    parser = argparse.ArgumentParser(
        description="gif-animator-pro : anime un sprite (emoji/sticker) au-dessus "
        "d'une photo avec démarches au choix, ombre portée et anti-aliasing."
    )
    parser.add_argument("--photo", required=True, help="chemin de la photo de fond")
    parser.add_argument("--sprite", required=True, help="PNG du sprite (fond transparent)")
    parser.add_argument("--out", required=True, help="chemin du GIF de sortie")
    parser.add_argument(
        "--gait",
        choices=["hopscotch", "bounce", "gallop", "glide"],
        default="hopscotch",
        help="démarche : hopscotch (cloche-pied marelle, défaut), bounce, gallop, glide",
    )
    parser.add_argument(
        "--direction", choices=["rtl", "ltr"], default="rtl", help="sens de traversée"
    )
    parser.add_argument("--hops", type=int, default=8, help="nombre de cases de la démarche")
    parser.add_argument("--baseline", default="0.27", help="ligne de sol (fraction <=1 ou px)")
    parser.add_argument("--amplitude", default="0.055", help="hauteur des sauts")
    parser.add_argument("--size", default="0.18", help="largeur du sprite")
    parser.add_argument("--fps", type=int, default=20, help="images par seconde")
    parser.add_argument("--duration", type=float, default=3.5, help="durée d'une boucle (s)")
    parser.add_argument("--flip", action="store_true", help="miroir horizontal du sprite")
    parser.add_argument("--tilt", type=float, default=6.0, help="inclinaison max (degrés)")
    parser.add_argument("--stretch", type=float, default=0.07, help="squash & stretch (0-0.25)")
    parser.add_argument(
        "--shadow", choices=["on", "off"], default="on", help="ombre portée dynamique"
    )
    parser.add_argument(
        "--supersample", type=int, default=2, help="facteur de supersampling (1 = off)"
    )
    parser.add_argument(
        "--max-width", type=int, default=0, help="largeur max de sortie (0 = natif)"
    )
    parser.add_argument(
        "--palette-colors", type=int, default=256, help="couleurs de la palette globale"
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
    scale = max(1, min(3, args.supersample))
    sprite = load_sprite(sprite_path, sprite_w, args.flip, scale)

    frames = build_frames(base, sprite, args)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    per_frame_ms = max(20, int(round(1000 / args.fps)))
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

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(
        f"GIF généré : {out_path} | {width}x{height}px | {len(frames)} frames "
        f"| gait={args.gait} | ombre={args.shadow} | S={scale} | {size_mb:.2f} Mo"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
