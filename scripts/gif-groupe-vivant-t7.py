# -*- coding: utf-8 -*-
"""
PA-GROUPE-005 — GIF anti-modifications, mouvement PLUS MARQUÉ (Task 7 G3, spec v2).
Base : PA-GROUPE-004 (qualité seule). Différences vs Task 6 (PA-GROUPE-003) :
- amplitudes ≈ ×2,3 (8,0 px horizontal, 3,4 px vertical) + 2ᵉ harmonique douce k=2 ;
- plafond spec v2 inchangé : 5 % de la hauteur des personnes (≈ 25 px) ;
- fond pixel-identique, boucle parfaite sans crossfade, palette globale médiane.
"""
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates, gaussian_filter

BASE = '/home/z/my-project/download/PA-GROUPE-004.png'
OUT = '/home/z/my-project/download/PA-GROUPE-005-groupe-vivant-marque.gif'
CONTACT = '/home/z/my-project/download/PA-GROUPE-005-contact-sheet.png'

DUREE = 4.0
FPS = 12
K1 = 1          # respiration : 1 cycle par boucle
K2 = 2          # 2ᵉ harmonique (balancement organique)
W2 = 0.25       # poids de l'harmonique

TETES = [(145, 255, 95, 110), (295, 390, 85, 95), (545, 85, 90, 95),
         (870, 50, 95, 100), (1140, 130, 85, 100)]
CORPS = [(0, 270, 340, 768), (235, 420, 460, 585), (395, 700, 180, 768),
         (705, 1085, 150, 768), (1070, 1344, 230, 768)]

ANCRES = [145, 295, 545, 870, 1140]
AX = [8.0, 5.5, 7.0, 8.0, 6.5]
AY = [3.4, 2.4, 3.2, 3.4, 2.6]
PHX = [0.0, 0.9, 1.8, 2.7, 3.6]
PHY = [1.2, 2.0, 2.8, 0.4, 1.9]
FEATHER = 14.0

def masque_personnes(w, h):
    m = np.zeros((h, w), dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for (cx, cy, rx, ry) in TETES:
        m = np.maximum(m, np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 4)))
    for (x0, x1, y0, y1) in CORPS:
        m = np.maximum(m, ((xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)).astype(np.float32))
    return np.clip(gaussian_filter(m, FEATHER), 0.0, 1.0)

def main():
    base_img = Image.open(BASE).convert('RGB')
    w, h = base_img.size
    base = np.asarray(base_img).astype(np.float32)
    m = masque_personnes(w, h)

    xs = np.arange(w, dtype=np.float32)
    ax = np.interp(xs, ANCRES, AX)
    ay = np.interp(xs, ANCRES, AY)
    phx = np.interp(xs, ANCRES, PHX)
    phy = np.interp(xs, ANCRES, PHY)

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = int(round(DUREE * FPS))
    frames = []
    dmax = 0.0
    for j in range(n):
        t = j / FPS
        o1 = 2 * np.pi * K1 * t / DUREE
        o2 = 2 * np.pi * K2 * t / DUREE
        dx = (ax[None, :] * np.sin(o1 + phx[None, :]) + W2 * ax[None, :] * np.sin(o2 + phx[None, :])) * m
        dy = (ay[None, :] * np.sin(o1 + phy[None, :])) * m
        dmax = max(dmax, float(np.sqrt(dx ** 2 + dy ** 2).max()))
        coords = np.stack([yy - dy, xx - dx])
        warped = np.stack([map_coordinates(base[..., c], coords, order=3, mode='nearest')
                           for c in range(3)], axis=-1)
        out = base * (1.0 - m[..., None]) + warped * m[..., None]
        frames.append(Image.fromarray(np.clip(np.round(out), 0, 255).astype(np.uint8)))

    # QC mécanique pleine résolution (Q3/Q4 fond figé ; Q6 couture ; Q5 amplitude)
    f0 = np.asarray(frames[0]).astype(np.int16)
    f47 = np.asarray(frames[-1]).astype(np.int16)
    f12 = np.asarray(frames[12]).astype(np.int16)
    fond = m < 0.01
    diff_fond = float(np.abs(f12 - f0)[fond].max())
    adj = [float(np.abs(np.asarray(frames[i + 1]).astype(np.int16)
                        - np.asarray(frames[i]).astype(np.int16)).mean()) for i in range(n - 1)]
    seam = float(np.abs(f0 - f47).mean())

    # Réduction résolution de SORTIE après validation identité (règle poids spec v2)
    OUT_W = 896
    if OUT_W < w:
        out_h = round(OUT_W * h / w)
        frames = [f.resize((OUT_W, out_h), Image.LANCZOS) for f in frames]
    ref_palette = frames[n // 2].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    frames_p = [f.quantize(palette=ref_palette, dither=Image.Dither.NONE) for f in frames]
    frames_p[0].save(OUT, save_all=True, append_images=frames_p[1:],
                     loop=0, duration=int(round(1000 / FPS)), optimize=True, disposal=1)

    sel = [0, 12, 24, 36, 47]
    th = [frames[i].resize((268, 153), Image.LANCZOS) for i in sel]
    sheet = Image.new('RGB', (268 * len(sel) + 8 * (len(sel) - 1), 153), 'white')
    for i, timg in enumerate(th):
        sheet.paste(timg, (i * (268 + 8), 0))
    sheet.save(CONTACT)

    import os
    print(f'GIF : {OUT} | sortie {frames[0].size[0]}x{frames[0].size[1]} (base {w}x{h}) | {n} frames | '
          f'{int(round(1000 / FPS))} ms/frame | {os.path.getsize(OUT) / 1024:.0f} Ko')
    print(f'Q5 amplitude max : {dmax:.2f} px (plafond spec 5 % hauteur ≈ 25 px) — PA-003 était 3,65 px')
    print(f'Q3/Q4 diff fond (frame 12 vs 0) : {diff_fond:.1f} (attendu 0)')
    print(f'Q6 couture 47->0 : {seam:.3f} | adjacent moyen : {np.mean(adj):.3f} '
          f'| adjacent max : {np.max(adj):.3f}')

if __name__ == '__main__':
    main()
