#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test mécanique qa-animation v1.0.0 (D005 — plan Task 8, G3).

  1. GIF synthétique conforme (8 frames, carré mobile, boucle infinie) → PASS rc 0
  2. référentiel conforme (frames/dimensions/boucle/mouvement/poids)   → PASS rc 0
  3. référentiel VIOLÉ (frames: 5)                                     → FAIL rc 1
  4. référentiel mouvement=false sur GIF animé                         → FAIL rc 1
  5. non-GIF (PNG)                                                     → ERREUR rc 6
  6. critères subjectifs LISTÉS comme non vérifiés (honnêteté R3)      → présent
  7. GIF RÉEL du pipeline gif-animator-pro (moteur + sprite asset)     → PASS rc 0
Usage : python3 scripts/task8/test-qa-animation.py  (rc 0 = PASS)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

QA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                  "skills", "gif-animator-pro", "scripts", "qa_animation.py")
MOTEUR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "skills", "gif-animator-pro", "scripts", "gif_sprite_gif_pro.py")
SPRITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "skills", "gif-animator-pro", "assets", "emoji_sheep.png")


def run(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, timeout=120)
    try:
        j = json.loads(p.stdout)
    except Exception:
        j = {"_stdout": p.stdout[-500:], "_stderr": p.stderr[-300:]}
    return p.returncode, j


def gif_syntheque(path, frames=8, w=320, h=240):
    from PIL import Image
    imgs = []
    for i in range(frames):
        img = Image.new("RGB", (w, h), (30, 40, 60))
        x = int(i * (w - 60) / max(1, frames - 1))
        for dx in range(40):
            for dy in range(40):
                img.putpixel((min(w - 1, x + dx), 100 + dy), (230, 220, 40))
        imgs.append(img)
    imgs[0].save(path, save_all=True, append_images=imgs[1:], loop=0, duration=100,
                 format="GIF")


def main():
    echecs = []

    def check(nom, ok, detail=""):
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", nom, (" — " + str(detail)) if detail else ""))
        if not ok:
            echecs.append(nom)

    bac = tempfile.mkdtemp(prefix="qatest-")
    try:
        print("— 1-2. GIF synthétique conforme + référentiel conforme —")
        g1 = os.path.join(bac, "synthetique.gif")
        gif_syntheque(g1)
        rc, res = run([QA, "--gif", g1, "--json"])
        check("GIF conforme → verdict PASS rc 0", rc == 0 and res.get("verdict") == "PASS",
              (rc, res.get("verdict")))
        m = res.get("mesures", {})
        check("mesures complètes (frames 8, boucle infinie, mouvement)",
              m.get("frames") == 8 and m.get("boucle") == "infinie" and m.get("mouvement") is True, m)
        ref = {"frames": 8, "dimensions": [320, 240], "boucle": "infinie",
               "mouvement": True, "poids_max_mo": 1.0, "duree_frame_ms": [80, 120]}
        rf = os.path.join(bac, "ref.json")
        json.dump(ref, open(rf, "w"))
        rc, res = run([QA, "--gif", g1, "--referentiel", rf, "--json"])
        check("référentiel conforme → PASS rc 0", rc == 0 and res.get("verdict") == "PASS", (rc, res.get("verdict")))
        check("criteres_subjectifs_non_verifies présents (R3)",
              len(res.get("criteres_subjectifs_non_verifies", [])) >= 3,
              res.get("criteres_subjectifs_non_verifies"))

        print("— 3. référentiel violé (frames 5) → FAIL rc 1 —")
        json.dump(dict(ref, frames=5), open(rf, "w"))
        rc, res = run([QA, "--gif", g1, "--referentiel", rf, "--json"])
        fails = [c["controle"] for c in res.get("controles", []) if c["verdict"] == "FAIL"]
        check("verdict FAIL rc 1 avec contrôle frames nominatif",
              rc == 1 and res.get("verdict") == "FAIL" and any("frames" in f for f in fails),
              (rc, fails))

        print("— 4. mouvement attendu absent (référentiel mouvement=false) → FAIL —")
        json.dump(dict(ref, mouvement=False), open(rf, "w"))
        rc, res = run([QA, "--gif", g1, "--referentiel", rf, "--json"])
        check("mouvement incohérent détecté (rc 1)", rc == 1 and res.get("verdict") == "FAIL", rc)

        print("— 5. non-GIF → rc 6 —")
        png = os.path.join(bac, "pasungif.png")
        from PIL import Image
        Image.new("RGB", (10, 10), (0, 0, 0)).save(png, format="PNG")
        rc, res = run([QA, "--gif", png, "--json"])
        check("PNG refusé proprement (rc 6)", rc == 6, (rc, res.get("erreur", "")))

        print("— 7. GIF RÉEL du pipeline gif-animator-pro —")
        from PIL import Image
        photo = os.path.join(bac, "photo.jpg")
        Image.new("RGB", (640, 480), (120, 160, 110)).save(photo, format="JPEG")
        g2 = os.path.join(bac, "mouton_reel.gif")
        p = subprocess.run([sys.executable, MOTEUR, "--photo", photo, "--sprite", SPRITE,
                            "--out", g2, "--gait", "hopscotch", "--direction", "ltr",
                            "--baseline", "0.5", "--size", "0.15", "--hops", "4",
                            "--fps", "10", "--duration", "1.6", "--supersample", "1"],
                           capture_output=True, text=True, timeout=120)
        check("moteur réel produit le GIF", os.path.isfile(g2) and os.path.getsize(g2) > 1000,
              (p.returncode, p.stderr[-160:] if p.returncode else "ok"))
        rc, res = run([QA, "--gif", g2, "--json"])
        m = res.get("mesures", {})
        check("GIF réel : PASS mécanique (animé, boucle, mouvement)",
              rc == 0 and res.get("verdict") == "PASS" and m.get("frames", 0) >= 8
              and m.get("boucle") == "infinie" and m.get("mouvement") is True,
              (rc, {k: m.get(k) for k in ("frames", "boucle", "mouvement", "dimensions")}))
        check("GIF réel : dimensions = photo 640×480", m.get("dimensions") == [640, 480], m.get("dimensions"))
    finally:
        shutil.rmtree(bac, ignore_errors=True)

    print("\n=== TEST qa-animation : %s ===" % ("PASS" if not echecs else "FAIL — " + ", ".join(echecs)))
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
