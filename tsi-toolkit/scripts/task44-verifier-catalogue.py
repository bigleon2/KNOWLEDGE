#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task44-verifier-catalogue.py — Vérificateur mécanique D008/D009/D011 (Task 44).

Vérifie, sur l'état réel du disque :
  D008  catalogues enrichis : tsi-toolkit/data/commandes-traktor.json + src/data/commands.json
        contiennent catalogue_interaktiv (524 commandes, 24 MIDI Controls 850-873) et les
        données DJTT/app existantes restent intactes (393 / 455)
  D009  validateur présent + verdicts sur 3 TSI réels (DJTT, DREW, task43-freeze-e2e)
  D011  décodeur présent + inventaires réels produits

Sortie : « CATALOGUE PASS » + détails ; rc=0 PASS, rc=1 FAIL.
"""
import json
import subprocess
import sys
from pathlib import Path

PROJ = Path("/home/z/my-project/work/knowledge-clone-fddbe94")
WORK = Path("/home/z/my-project/work")
CHEKS = []

def check(nom, cond, detail=""):
    CHEKS.append((nom, bool(cond), detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom} {detail}")
    return bool(cond)


def main() -> int:
    ok = True
    print("=== Vérificateur Task 44 — catalogues enrichis / validateur / décodeur ===")

    # D008 — catalogues
    p1 = PROJ / "tsi-toolkit/data/commandes-traktor.json"
    p2 = PROJ / "src/data/commands.json"
    try:
        t1 = json.loads(p1.read_text(encoding="utf-8"))
        ci1 = t1["catalogue_interaktiv"]
        ok &= check("D008 toolkit : 524 commandes", len(ci1["commandes"]) == 524)
        ok &= check("D008 toolkit : MIDI Controls 850-873", ci1["comptes"]["midi_controls_ids"] == list(range(850, 874)))
        ok &= check("D008 toolkit : DJTT 393 intact", t1["comptes"]["commandes"] == 393 and len(t1["controles"]) == 163)
        ok &= check("D008 toolkit : licence CC BY + attribution", "CC BY 4.0" in ci1["meta"]["licence"] and "interaktivaudio.com" in ci1["meta"]["attribution"])
    except Exception as e:
        ok &= check("D008 toolkit", False, f"exception {e}")
    try:
        t2 = json.loads(p2.read_text(encoding="utf-8"))
        ci2 = t2["catalogue_interaktiv"]
        ok &= check("D008 app : 524 commandes", len(ci2["commandes"]) == 524)
        ok &= check("D008 app : comptes 455 intacts", t2["comptes"]["commandes"] == 455)
        ok &= check("D008 app : source Interaktiv dans meta", any("Interaktiv" in s for s in t2["meta"]["sources"]))
    except Exception as e:
        ok &= check("D008 app", False, f"exception {e}")

    # D009 — validateur sur 3 TSI réels
    val = PROJ / "tsi-toolkit/scripts/task44-valider-mapping-catalogue.py"
    ok &= check("D009 validateur présent", val.exists())
    tsis = {
        "DJTT v2.1.0": WORK / "djtt/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi",
        "DREW": None,  # résolu plus bas
        "freeze-e2e": PROJ / ".." / "task43-freeze-e2e.tsi",
    }
    drew = sorted((WORK / "drew-fixtures").rglob("*.tsi")) if (WORK / "drew-fixtures").exists() else []
    tsis["DREW"] = drew[0] if drew else None
    for nom, path in tsis.items():
        if path is None or not Path(path).exists():
            ok &= check(f"D009 TSI {nom}", False, "fichier introuvable")
            continue
        r = subprocess.run(
            [sys.executable, str(val), "--catalogue", str(p1), "--tsi", str(path), "--json"],
            capture_output=True, text=True, timeout=180,
        )
        try:
            d = json.loads(r.stdout)
            ok &= check(
                f"D009 TSI {nom} : verdict {d['verdict']}",
                d["verdict"] in ("PASS", "PASS_AVEC_RESERVES"),
                f"({d['connus']}/{d['nb_noms']} connus, {len(d['inconnues'])} inconnues)",
            )
        except Exception as e:
            ok &= check(f"D009 TSI {nom}", False, f"exception {e} / stdout={r.stdout[:120]}")

    # D011 — décodeur + inventaires réels
    dec = PROJ / "tsi-toolkit/scripts/task44-decoder-deviceio.py"
    ok &= check("D011 décodeur présent", dec.exists())
    for inv in [WORK / "zip-setting-431/deviceio/inventaire-deviceio.json",
                WORK / "zip-setting-431/deviceio-djtt/inventaire-deviceio.json"]:
        ok &= check(f"D011 inventaire {inv.parent.name}", inv.exists() and inv.stat().st_size > 1000)

    verdict = "CATALOGUE PASS" if ok else "CATALOGUE FAIL"
    n_pass = sum(1 for _, c, _ in CHEKS if c)
    print(f"\n{verdict} — {n_pass}/{len(CHEKS)} checks")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
