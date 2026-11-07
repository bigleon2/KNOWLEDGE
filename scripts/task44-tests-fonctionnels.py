#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""task44-tests-fonctionnels.py — Batterie de tests fonctionnels robustes Task 44 (G5).

Teste TOUT élément créé/modifié aujourd'hui (Task 44) pour trouver ses failles :
  - catalogues enrichis (validité, idempotence enrichisseur ×2, non-régression DJTT/app)
  - validateur mapping↔catalogue (3 TSI réels ×2 idempotence, usages, corruption,
    TSI sans blob, suggestions de noms officiels)
  - décodeur DeviceIO (2 TSI réels, usages)
  - intégration app (tsc --noEmit, eslint), suite toolkit (unittest 20/20),
    intégrité SKILL.md (D010)

Journal : work/task44-tests-journal.json (JSON structuré).
Verdict : « BATTERIE : N/N PASS » — rc=0 si tout PASS, rc=1 sinon.
Usage invalide → rc=3.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PROJ = Path("/home/z/my-project/work/knowledge-clone-fddbe94")
WORK = Path("/home/z/my-project/work")
HOST_SCRIPTS = Path("/home/z/my-project/scripts")
TOOLKIT_SCRIPTS = PROJ / "tsi-toolkit/scripts"
CAT = PROJ / "tsi-toolkit/data/commandes-traktor.json"
APP_CAT = PROJ / "src/data/commands.json"
TSI_DJTT = WORK / "djtt/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi"
TSI_FREEZE = WORK / "task43-freeze-e2e.tsi"
VAL = TOOLKIT_SCRIPTS / "task44-valider-mapping-catalogue.py"
DEC = TOOLKIT_SCRIPTS / "task44-decoder-deviceio.py"
ENR = TOOLKIT_SCRIPTS / "task44-enricher-catalogues.py"
JOURNAL = WORK / "task44-tests-journal.json"

RESULTATS = []


def t(nom, cond, detail=""):
    RESULTATS.append({"test": nom, "pass": bool(cond), "detail": str(detail)[:300]})
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom}" + (f" — {detail}" if detail and not cond else ""))
    return bool(cond)


def run(args, timeout=300):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] not in ("--run",):
        print(__doc__)
        return 3
    t0 = time.time()
    print("=== BATTERIE Task 44 — tests fonctionnels robustes (G5) ===")

    # TB-01 — JSON valides
    try:
        d1 = json.loads(CAT.read_text(encoding="utf-8"))
        d2 = json.loads(APP_CAT.read_text(encoding="utf-8"))
        t("TB-01 JSON catalogues valides", True)
    except Exception as e:
        t("TB-01 JSON catalogues valides", False, e)
        d1 = d2 = None

    # TB-02 — idempotence enrichisseur ×2 (sha256 stable après 2 exécutions)
    if d1 and d2:
        s1a, s2a = sha256(CAT), sha256(APP_CAT)
        r1, r2 = run([sys.executable, str(ENR)]), run([sys.executable, str(ENR)])
        s1b, s2b = sha256(CAT), sha256(APP_CAT)
        t("TB-02 enrichisseur idempotent ×2", r1.returncode == 0 and r2.returncode == 0 and s1a == s1b and s2a == s2b,
          f"rc=({r1.returncode},{r2.returncode}) sha stable={s1a == s1b and s2a == s2b}")

    # TB-03 — non-régression DJTT / app
    try:
        t("TB-03 non-régression DJTT 393/163 + app 455",
          d1["comptes"]["commandes"] == 393 and len(d1["controles"]) == 163
          and d2["comptes"]["commandes"] == 455
          and d1["comptes"]["conditions_in"] == 125 and d1["comptes"]["conditions_out"] == 220)
    except Exception as e:
        t("TB-03 non-régression DJTT / app", False, e)

    # TB-04..06 — validateur ×2 idempotent sur 3 TSI réels
    att = {"DJTT": "PASS", "DREW": "PASS", "freeze-e2e": "PASS_AVEC_RESERVES"}
    paths = {
        "DJTT": TSI_DJTT,
        "DREW": sorted((WORK / "drew-fixtures").rglob("*.tsi"))[0] if (WORK / "drew-fixtures").exists() else None,
        "freeze-e2e": TSI_FREEZE,
    }
    for nom, attendu in att.items():
        p = paths[nom]
        if p is None or not Path(p).exists():
            t(f"TB-0X validateur {nom}", False, "fichier introuvable")
            continue
        r1 = run([sys.executable, str(VAL), "--catalogue", str(CAT), "--tsi", str(p), "--json"])
        r2 = run([sys.executable, str(VAL), "--catalogue", str(CAT), "--tsi", str(p), "--json"])
        ok = False
        det = ""
        try:
            j1, j2 = json.loads(r1.stdout), json.loads(r2.stdout)
            ok = j1["verdict"] == attendu and j1 == j2 and r1.returncode == r2.returncode == 0
            det = f"verdict={j1['verdict']} inconnues={len(j1['inconnues'])} idempotent={j1 == j2}"
        except Exception as e:
            det = f"exception {e} stderr={r1.stderr[:150]}"
        t(f"TB validateur {nom} (attendu {attendu}) ×2", ok, det)

    # TB-07 — usage : fichier inexistant → rc=3
    r = run([sys.executable, str(VAL), "--catalogue", str(CAT), "--tsi", "/tmp/inexistant-44.tsi"])
    t("TB usage fichier inexistant → rc=3", r.returncode == 3, f"rc={r.returncode}")

    # TB-08 — fichier corrompu (garbage binaire) → FAIL rc=4
    with tempfile.NamedTemporaryFile(suffix=".tsi", delete=False, dir="/tmp") as f:
        f.write(b"\x00\x01\x02 garbage \xff\xfe pas de xml ni blob" * 100)
        corrompu = f.name
    r = run([sys.executable, str(VAL), "--catalogue", str(CAT), "--tsi", corrompu, "--json"])
    try:
        j = json.loads(r.stdout)
        ok = j["verdict"] == "FAIL" and r.returncode == 4
    except Exception as e:
        ok, j = False, {"err": str(e)}
    t("TB corruption binaire → FAIL rc=4", ok, f"rc={r.returncode} verdict={j.get('verdict')}")
    Path(corrompu).unlink(missing_ok=True)

    # TB-09 — TSI préférences sans blob ni mappings → FAIL rc=4 (comportement documenté)
    fx = WORK / "djtt/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/FX Settings.tsi"
    if fx.exists():
        r = run([sys.executable, str(VAL), "--catalogue", str(CAT), "--tsi", fx, "--json"])
        try:
            j = json.loads(r.stdout)
            ok = j["verdict"] == "FAIL" and r.returncode == 4 and "sans mappings" in j.get("raison", "")
        except Exception as e:
            ok, j = False, {"err": str(e)}
        t("TB préférences FX (sans mappings) → FAIL propre rc=4", ok, f"rc={r.returncode} verdict={j.get('verdict')}")

    # TB-10 — suggestions de noms officiels (Slice 1 → Slice Trigger 1)
    r = run([sys.executable, str(VAL), "--catalogue", str(CAT), "--tsi", str(TSI_FREEZE), "--json"])
    try:
        j = json.loads(r.stdout)
        inc = {i["nom"]: i["suggestions"] for i in j["inconnues"]}
        ok = "Slice Trigger 1" in inc.get("Slice 1", [])
    except Exception as e:
        ok = False
        inc = {"err": str(e)}
    t("TB suggestion « Slice 1 » → « Slice Trigger 1 »", ok, str(inc.get("Slice 1")))

    # TB-11/12 — décodeur : usage et sans-blob
    r = run([sys.executable, str(DEC)])
    t("TB décodeur usage vide → rc=3", r.returncode == 3, f"rc={r.returncode}")
    fx_settings = WORK / "djtt/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/FX Settings.tsi"
    with tempfile.TemporaryDirectory() as td:
        r = run([sys.executable, str(DEC), str(fx_settings), td])
        t("TB décodeur TSI sans blob → rc=4 (refus propre)", r.returncode == 4, f"rc={r.returncode} out={r.stdout[:80]}")

    # TB-13 — décodeur ×2 idempotent sur settings perso (inventaire identique)
    pers = WORK / "zip-setting-431/TRAKTOR 3 (v11.1.17) - SETTING et  MIDI CONTROL (entrées MIDI)_captures d'écran/Settings-TRAKTOR_3 (v1_1_17).tsi"
    if pers.exists():
        with tempfile.TemporaryDirectory() as td:
            r1 = run([sys.executable, str(DEC), str(pers), td])
            inv1 = (Path(td) / "inventaire-deviceio.json").read_text(encoding="utf-8")
            r2 = run([sys.executable, str(DEC), str(pers), td])
            inv2 = (Path(td) / "inventaire-deviceio.json").read_text(encoding="utf-8")
            try:
                d = json.loads(inv1)
                t("TB décodeur settings perso ×2 idempotent + sections",
                  r1.returncode == r2.returncode == 0 and inv1 == inv2
                  and d["sections_detectees"]["DCDT"] == 3105 and d["taille_blob_octets"] == 2940882)
            except Exception as e:
                t("TB décodeur settings perso ×2", False, e)

    # TE-01/02 — intégration app : tsc + eslint
    # Convention écosystème (task43-verifier-projet.py ligne 339-341) : seules les erreurs
    # sur src/ comptent — la baseline template (examples/, skills/ hors jalon) est exclue.
    import re as _re
    tsc = subprocess.run(["npx", "tsc", "--noEmit"], cwd=PROJ, capture_output=True, text=True, timeout=600)
    sortie = tsc.stdout + tsc.stderr
    err_src = [l for l in sortie.splitlines()
               if _re.match(r"^src/[\w./-]+", l) and "error TS" in l]
    t("TE-01 tsc --noEmit 0 erreur sur src/ (baseline template hors jalon)", not err_src,
      f"{len(err_src)} erreur(s) src/ : {err_src[:3]}")
    eslint = subprocess.run(["npx", "eslint", "src", "--quiet"], cwd=PROJ, capture_output=True, text=True, timeout=600)
    t("TE-02 eslint src 0 erreur", eslint.returncode == 0, eslint.stdout[-200:] + eslint.stderr[-200:])

    # TE-03 — suite toolkit unittest
    ut = subprocess.run([sys.executable, "-m", "unittest", "tests.test_toolkit", "-v"],
                        cwd=PROJ / "tsi-toolkit", capture_output=True, text=True, timeout=300)
    t("TE-03 unittest toolkit 20/20", "OK" in ut.stderr and ut.returncode == 0, ut.stderr[-200:])

    # TE-04 — intégrité SKILL.md (D010)
    a = (PROJ / "skills/analyse-doc-s4mk2/SKILL.md").read_text(encoding="utf-8")
    b = (PROJ / "skills/tsi-architect/SKILL.md").read_text(encoding="utf-8")
    t("TE-04 SKILL.md intégrité D010",
      "version: 1.3.0" in a and "DeviceIO.Config.Controller" in a
      and "version: 1.2.0" in b and "MIDI Button 1-8" in b and "850-857" in b and "866-873" in b
      and "interaktivaudio.com" in b)

    # TE-05 — miroir hôte↔clone du script de batterie (R4 byte-identité)
    miroir = HOST_SCRIPTS / Path(__file__).name
    t("TE-05 miroir hôte↔clone byte-identique", miroir.exists() and sha256(miroir) == sha256(Path(__file__)))

    # TE-06 — vérificateur catalogue re-run (D008/D009/D011 stables)
    vr = run([sys.executable, str(TOOLKIT_SCRIPTS / "task44-verifier-catalogue.py")])
    t("TE-06 verifier-catalogue CATALOGUE PASS", vr.returncode == 0 and "CATALOGUE PASS" in vr.stdout, vr.stdout[-150:])

    n_pass = sum(1 for r in RESULTATS if r["pass"])
    duree = round(time.time() - t0, 2)
    journal = {
        "meta": {"script": Path(__file__).name, "date": time.strftime("%Y-%m-%dT%H:%M:%S"), "duree_s": duree},
        "batterie": RESULTATS,
        "verdict": f"BATTERIE : {n_pass}/{len(RESULTATS)} PASS",
    }
    JOURNAL.write_text(json.dumps(journal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n{journal['verdict']} — durée {duree}s — journal {JOURNAL.name}")
    return 0 if n_pass == len(RESULTATS) else 1


if __name__ == "__main__":
    sys.exit(main())
