#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.21)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""task45-tests-fonctionnels.py — Batterie de tests fonctionnels robustes Task 45 (G3/G5).

Teste TOUT élément créé/modifié aujourd'hui (Task 45) pour trouver ses failles :
  - preset « MIDI Controls bridge » (comptes 24/24/8, cohérence 1:1 étage 1 ↔ étage 2,
    idempotence générateur ×2, échec bruyant sur preset corrompu)
  - TSI généré (déterminisme ×2, validations idempotentes ×2 : toolkit + arbitre
    tsi-validator E1-E8 + catalogue Task 44 avec 0 inconnue)
  - symétrie des decks A-D (source de vérité DJTT : 6 délégations par deck, 0 écart)
  - documentation midi-doc-expert v1.2.0 (self-test ×2, 9 sections, couverture 56/56,
    re-génération byte-identique, mention bridge + attribution CC BY présentes)
  - non-régression : suite toolkit (unittest), batterie Task 44 (19/19)
  - miroir hôte ↔ clone (scripts de session Task 45 + skill midi-doc-expert)

Journal : work/task45-tests-journal.json (JSON structuré).
Verdict : « BATTERIE : N/N PASS » — rc=0 si tout PASS, rc=1 sinon.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PROJ = Path("/home/z/my-project/work/KNOWLEDGE-b75a620")
WORK = Path("/home/z/my-project/work")
HOST = Path("/home/z/my-project")
PRESET = PROJ / "tsi-toolkit/examples/preset-midi-controls-bridge.json"
GEN = PROJ / "scripts/task45-generer-preset-bridge.py"
TSI = PROJ / "download/task45-midi-controls-bridge.tsi"
DOC_MD = PROJ / "download/task45-midi-controls-bridge-doc.md"
DOC_JSON = PROJ / "download/task45-midi-controls-bridge-doc.json"
DOCGEN = PROJ / "skills/midi-doc-expert/scripts/generer-doc-midi.py"
VAL44 = PROJ / "tsi-toolkit/scripts/task44-valider-mapping-catalogue.py"
BATTERIE44 = PROJ / "scripts/task44-tests-fonctionnels.py"
JOURNAL = WORK / "task45-tests-journal.json"

RESULTATS = []


def t(nom, cond, detail=""):
    RESULTATS.append({"test": nom, "pass": bool(cond), "detail": str(detail)[:300]})
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom}" + (f" — {detail}" if detail and not cond else ""))
    return bool(cond)


def run(args, timeout=300, cwd=None):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                          cwd=str(cwd) if cwd else None)


def sha(chemin):
    return hashlib.sha256(Path(chemin).read_bytes()).hexdigest()


def test_preset():
    print("— Preset « MIDI Controls bridge »")
    p = json.loads(PRESET.read_text(encoding="utf-8"))
    m = p["mappings"]
    e1 = [x for x in m if x["groupe"] == "Global" and x["type"] == "IN"
          and str(x["controle"]).startswith("MIDI ")]
    e2 = [x for x in m if x["type"] == "IN" and str(x["groupe"]).startswith("Deck ")]
    led = [x for x in m if x["type"] == "OUT"]
    t("TB-01 preset valide : 56 mappings = 24 bridge + 24 délégations + 8 LED",
      len(m) == 56 and len(e1) == 24 and len(e2) == 24 and len(led) == 8,
      f"{len(m)}/{len(e1)}/{len(e2)}/{len(led)}")
    app = sorted((x["midi"]["canal"], x["midi"]["numero"]) for x in e1)
    app2 = sorted((x["midi"]["numero"]) for x in e2)
    t("TB-02 appariement 1:1 étage 1 (ch0, CC 80-103) ↔ étage 2 (ch1, mêmes CC)",
      app == [(0, c) for c in range(80, 104)] and app2 == list(range(80, 104)))
    t("TB-03 attribution Interaktiv CC BY 4.0 en méta",
      "CC BY 4.0" in p["meta"]["description"] and "interaktivaudio.com" in p["meta"]["description"])
    # Idempotence générateur ×2
    with tempfile.TemporaryDirectory() as td:
        s1, s2 = Path(td) / "a.json", Path(td) / "b.json"
        r1 = run([sys.executable, str(GEN), str(s1)])
        r2 = run([sys.executable, str(GEN), str(s2)])
        t("TB-04 générateur preset idempotent ×2 (rc=(0,0), sha stable)",
          r1.returncode == 0 and r2.returncode == 0 and sha(s1) == sha(s2),
          f"rc=({r1.returncode},{r2.returncode}) sha_stable={sha(s1) == sha(s2)}")
        # Échec bruyant sur preset corrompu (génération via toolkit)
        corrompu = Path(td) / "corrompu.json"
        mauvais = json.loads(PRESET.read_text(encoding="utf-8"))
        mauvais["mappings"][0]["midi"]["numero"] = mauvais["mappings"][1]["midi"]["numero"]
        corrompu.write_text(json.dumps(mauvais), encoding="utf-8")
        r3 = run([sys.executable, "-m", "tsi_toolkit", "generate", str(corrompu),
                  str(Path(td) / "x.tsi")], timeout=120, cwd=PROJ / "tsi-toolkit")
        t("TB-05 preset corrompu (collision CC) → génération refusée bruyamment",
          r3.returncode != 0 and "conflit" in (r3.stderr + r3.stdout).lower(),
          f"rc={r3.returncode}")


def test_tsi():
    print("— TSI généré + validations")
    t("TB-06 TSI présent et non vide", TSI.is_file() and TSI.stat().st_size > 5000,
      f"{TSI.stat().st_size if TSI.is_file() else 0} o")
    with tempfile.TemporaryDirectory() as td:
        r = run([sys.executable, "-m", "tsi_toolkit", "generate",
                 str(PRESET), str(Path(td) / "re.tsi")],
                timeout=120, cwd=PROJ / "tsi-toolkit")
        t("TB-07 TSI déterministe ×2 (re-génération byte-identique)",
          r.returncode == 0 and sha(Path(td) / "re.tsi") == sha(TSI),
          f"rc={r.returncode}")
    for i in (1, 2):
        vt = run([sys.executable, "-m", "tsi_toolkit", "validate", str(TSI)],
                 timeout=120, cwd=PROJ / "tsi-toolkit")
        va = run([sys.executable, str(PROJ / "skills/tsi-validator/scripts/valider-tsi.py"), str(TSI)])
        vc = run([sys.executable, str(VAL44), "--catalogue",
                  str(PROJ / "tsi-toolkit/data/commandes-traktor.json"),
                  "--tsi", str(TSI), "--json"])
        cat = json.loads(vc.stdout or "{}")
        t(f"TB-08.{i} validations idempotentes (toolkit PASS, arbitre rc=0, catalogue 0 inconnue)",
          vt.returncode == 0 and va.returncode == 0
          and cat.get("verdict") == "PASS" and len(cat.get("inconnues", [])) == 0,
          f"toolkit={vt.returncode} arbitre={va.returncode} verdict={cat.get('verdict')} "
          f"inconnues={len(cat.get('inconnues', []))}")
    # Symétrie des decks depuis le TSI (pas seulement le preset)
    import xml.etree.ElementTree as ET
    racine = ET.parse(TSI).getroot()
    comptes = {}
    for mp in racine.findall("DEVICE/MAPPINGS/MAPPING"):
        if mp.get("TYPE") == "IN" and str(mp.get("GROUP", "")).startswith("Deck "):
            comptes[mp.get("GROUP")] = comptes.get(mp.get("GROUP"), 0) + 1
    t("TB-10 symétrie des decks A-D : 6 délégations chacun, 0 écart (DJTT)",
      comptes == {"Deck A": 6, "Deck B": 6, "Deck C": 6, "Deck D": 6}, str(comptes))


def test_doc():
    print("— Documentation midi-doc-expert")
    for i in (1, 2):
        r = run([sys.executable, str(DOCGEN), "--self-test"])
        t(f"TB-11.{i} self-test generer-doc-midi PASS", r.returncode == 0 and "PASS" in r.stdout)
    md = DOC_MD.read_text(encoding="utf-8")
    dj = json.loads(DOC_JSON.read_text(encoding="utf-8"))
    sections = [f"## {i}." for i in range(1, 10)]
    t("TB-12 9 sections présentes + couverture 56/56 (taux 1.0)",
      all(s in md for s in sections)
      and dj["couverture"]["taux"] == 1.0
      and dj["couverture"]["mappings_tsi"] == 56)
    t("TB-13 bridge expliqué (2 étages + convention 1-4/5-8) + attribution CC BY",
      "Bridge MIDI Controls détecté" in md and "850-873" in md
      and "CC BY 4.0" in md and "looprituals.de" in md)
    t("TB-14 wording par mode (bouton/commutation, valeur absolue, relais bridge — plus d'« encodeur » abusif)",
      "commute" in md and "relais bridge" in md and "valeur absolue" in md
      and "Le mode Increment/decrement" not in md.split("## 6.")[0].split("## 5.")[1]
      if "## 5." in md and "## 6." in md else False)
    with tempfile.TemporaryDirectory() as td:
        r = run([sys.executable, str(DOCGEN), str(TSI), "--outdir", td,
                 "--titre", "MIDI Controls bridge — délégation par deck (Traktor 3.11.1 / Kontrol S4 MK2)"])
        t("TB-15 re-génération doc byte-identique (ENF-05)",
          r.returncode == 0
          and sha(Path(td) / "task45-midi-controls-bridge-doc.md") == sha(DOC_MD)
          and sha(Path(td) / "task45-midi-controls-bridge-doc.json") == sha(DOC_JSON))
    t("TB-16 skill miroir hôte ↔ clone byte-identique (v1.2.0)",
      sha(DOCGEN) == sha(HOST / "skills/midi-doc-expert/scripts/generer-doc-midi.py")
      and sha(PROJ / "skills/midi-doc-expert/SKILL.md")
      == sha(HOST / "skills/midi-doc-expert/SKILL.md")
      and "version: 1.2.0" in (PROJ / "skills/midi-doc-expert/SKILL.md").read_text(encoding="utf-8"))


def test_non_regression():
    print("— Non-régression + miroir")
    r = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            timeout=300, cwd=PROJ / "tsi-toolkit")
    t("TB-17 suite toolkit unittest : 20/20 PASS",
      r.returncode == 0 and "OK" in (r.stderr or r.stdout)[-200:], r.stderr[-120:] if r.returncode else "")
    r2 = run([sys.executable, str(BATTERIE44)], timeout=600)
    t("TB-18 batterie Task 44 : 19/19 PASS (non-régression)",
      r2.returncode == 0 and "19/19" in (r2.stdout or ""), (r2.stdout or "")[-150:])
    # (clone, hôte) — le toolkit n'existe que dans le clone : son preset est
    # miré côté hôte sous scripts/task45-preset-midi-controls-bridge.json.
    paires = [("scripts/task45-generer-preset-bridge.py",
               "scripts/task45-generer-preset-bridge.py"),
              ("scripts/task45-tests-fonctionnels.py",
               "scripts/task45-tests-fonctionnels.py"),
              ("tsi-toolkit/examples/preset-midi-controls-bridge.json",
               "scripts/task45-preset-midi-controls-bridge.json"),
              ("skills/midi-doc-expert/scripts/generer-doc-midi.py",
               "skills/midi-doc-expert/scripts/generer-doc-midi.py"),
              ("skills/midi-doc-expert/SKILL.md",
               "skills/midi-doc-expert/SKILL.md")]
    diffs = [c for c, h in paires
             if sha(PROJ / c) != sha(HOST / h)]
    t("TB-19 miroir hôte ↔ clone : 5 éléments Task 45 byte-identiques", not diffs, str(diffs))


def main():
    if "--self-test" in sys.argv:
        print("self-test task45-tests-fonctionnels : imports OK, constantes OK")
        return 0
    debut = time.time()
    print("BATTERIE TASK 45 — tests fonctionnels robustes")
    test_preset()
    test_tsi()
    test_doc()
    test_non_regression()
    n_pass = sum(1 for r in RESULTATS if r["pass"])
    journal = {
        "meta": {"script": "task45-tests-fonctionnels.py",
                 "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
                 "duree_s": round(time.time() - debut, 2)},
        "batterie": RESULTATS,
        "verdict": f"BATTERIE : {n_pass}/{len(RESULTATS)} PASS",
    }
    JOURNAL.write_text(json.dumps(journal, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
    print(f"\n{journal['verdict']}  (journal : {JOURNAL})")
    return 0 if n_pass == len(RESULTATS) else 1


if __name__ == "__main__":
    sys.exit(main())
