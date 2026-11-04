#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task44-valider-mapping-catalogue.py — Valide les commandes référencées par un fichier .tsi
contre le catalogue enrichi de l'écosystème (source de vérité DJTT + référence Interaktiv Audio).

Gère les deux formats :
  A) TSI Traktor 3.x réel : mappings dans le blob DeviceIO.Config.Controller (base64,
     chaînes UTF-16 : noms de contrôles DCDT « Left.Cue », commandes « Hotcue A1 »,
     mappings « _(Mod) Freeze Mode », couleurs LED DCBM…)
  B) TSI format toolkit/2.x : XML avec <MAPPING ... CONTROL="..."> / <MAPPINGSETTING ... NAME="...">

Verdicts (JSON + exit code) :
  PASS                 toutes les commandes plausibles sont couvertes (≥ seuil 95 %)
  PASS_AVEC_RESERVES   couverture < 95 % — inconnues listées avec suggestion de nom officiel
  FAIL                 fichier illisible / sans commandes exploitables

Usage :
  python3 task44-valider-mapping-catalogue.py --catalogue <commandes-traktor.json> --tsi <fichier.tsi> [--json] [--seuil 0.95]
Idempotent ×2. rc : 0 PASS/PASS_AVEC_RESERVES · 3 usage · 4 FAIL.
"""
import difflib
import importlib.util
import json
import re
import sys
from pathlib import Path

_mod = Path(__file__).parent / "task44-decoder-deviceio.py"
_spec = importlib.util.spec_from_file_location("task44_decoder_deviceio", _mod)
_m = importlib.util.module_from_spec(_spec)
sys.modules["task44_decoder_deviceio"] = _m
_spec.loader.exec_module(_m)
extraire_blob = _m.extraire_blob
extraire_utf16 = _m.extraire_utf16

# Noms plausibles : lettre initiale, contient espace/point/slash ou suffixe numérique,
# length raisonnable — les chaînes techniques (versions, ports, UUID) sont exclues.
RE_PLAUSIBLE = re.compile(r"^[A-Za-z_(0-9\"]{1,3}[\w'\"()\[\]/+ .&*-]{3,78}$")
EXCLUSIONS = (
    "http", "Traktor.Kontrol", "Traktor Virtual", ".tsi", ".exe", "www.",
)
PREFIXES_HW = ("Left.", "Right.", "Center.", "Front.", "Back.")


def charger_catalogue(catalogue_path: Path):
    d = json.loads(catalogue_path.read_text(encoding="utf-8"))
    noms_officiels = {}
    ci = d.get("catalogue_interaktiv", {}).get("commandes", [])
    for c in ci:
        noms_officiels[str(c.get("name"))] = {
            "id": c.get("id"), "section": c.get("section"), "source": "interaktiv",
        }
    for nom, cat in (d.get("commandes") or {}).items():
        noms_officiels.setdefault(nom, {"id": None, "section": cat, "source": "djtt"})
    return noms_officiels


def noms_du_tsi(tsi_path: Path):
    """Extrait les noms plausibles de commandes/contrôles d'un .tsi (formats A et B)."""
    data = tsi_path.read_text(encoding="utf-8", errors="replace")
    noms = []
    # Format B : mappings XML explicites
    for m in re.finditer(r'<MAPPING[^>]*CONTROL="([^"]+)"', data):
        noms.append(m.group(1))
    for m in re.finditer(r'<MAPPINGSETTING[^>]*NAME="([^"]+)"', data):
        noms.append(m.group(1))
    # Format A : blob DeviceIO
    blob = extraire_blob(tsi_path)
    if blob:
        strings = extraire_utf16(blob)
        seen = set()
        for s in strings:
            s = s.strip()
            if not s or s in seen or len(s) < 4 or len(s) > 80:
                continue
            seen.add(s)
            if any(x in s for x in EXCLUSIONS):
                continue
            plausible = RE_PLAUSIBLE.match(s) and (
                " " in s or "." in s or "/" in s or re.search(r"\d", s)
            )
            if plausible:
                noms.append(s)
    # Déduplication préservant l'ordre
    out, seen = [], set()
    for n in noms:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def est_connu(nom: str, noms_officiels: dict) -> bool:
    if nom in noms_officiels:
        return True
    # Variante normalisée : casse/espaces
    n_norm = re.sub(r"\s+", " ", nom.strip().lower())
    for off in noms_officiels:
        if re.sub(r"\s+", " ", off.strip().lower()) == n_norm:
            return True
    return False


def est_controle_hardware(nom: str) -> bool:
    """Left.Cue / Right.HotCue 2.Turquoise / A.FX.On / Center.LoopRec.Record…"""
    return nom.startswith(PREFIXES_HW) or re.match(r"^[A-D]\.", nom) is not None


def est_couleur_led(nom: str) -> bool:
    couleurs = (
        "Red", "Green", "Blue", "Cyan", "Mint", "Turquoise", "Fuchsia", "Lime",
        "Orange", "Yellow", "White", "Pink", "Purple", "Amber", "Violet",
    )
    return any(f".{c}" in nom or nom.endswith(f" {c}") for c in couleurs)


def valider(tsi_path: Path, noms_officiels: dict, seuil: float) -> dict:
    noms = noms_du_tsi(tsi_path)
    if not noms:
        return {
            "verdict": "FAIL",
            "fichier": tsi_path.name,
            "raison": "aucun nom de commande/contrôle exploitable (fichier illisible ou sans mappings)",
            "nb_noms": 0, "connus": [], "inconnues": [],
            "midi_controls_detectees": [], "couverture": 0.0,
        }
    liste_officielle = list(noms_officiels.keys())
    connus, inconnues = [], []
    for nom in noms:
        if est_connu(nom, noms_officiels) or est_controle_hardware(nom) or est_couleur_led(nom):
            connus.append(nom)
        else:
            suggestions = difflib.get_close_matches(nom, liste_officielle, n=2, cutoff=0.6)
            inconnues.append({"nom": nom, "suggestions": suggestions})
    mc = [n for n in noms if re.match(r"MIDI (Button|Knob|Fader) [1-8]$", n)]
    cov = len(connus) / len(noms) if noms else 0.0
    verdict = "PASS" if cov >= seuil else "PASS_AVEC_RESERVES"
    return {
        "verdict": verdict,
        "fichier": tsi_path.name,
        "nb_noms": len(noms),
        "connus": len(connus),
        "inconnues": inconnues,
        "midi_controls_detectees": mc,
        "seuil": seuil,
        "couverture": round(cov, 4),
    }


def main() -> int:
    args = sys.argv[1:]
    def opt(flag, default=None):
        return args[args.index(flag) + 1] if flag in args else default
    if "--tsi" not in args or "--catalogue" not in args:
        print(__doc__)
        return 3
    catalogue = Path(opt("--catalogue"))
    tsi = Path(opt("--tsi"))
    seuil = float(opt("--seuil", "0.95"))
    if not catalogue.exists() or not tsi.exists():
        print("ERREUR : catalogue ou tsi introuvable")
        return 3
    noms_officiels = charger_catalogue(catalogue)
    res = valider(tsi, noms_officiels, seuil)
    if "--json" in args:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"Verdict : {res['verdict']} — {res['fichier']} : {res['connus']}/{res['nb_noms']} connus ({res['couverture']*100:.1f} %), {len(res['inconnues'])} inconnues, MIDI Controls: {res['midi_controls_detectees'] or 'aucune'}")
        for inc in res["inconnues"][:15]:
            sug = f"  → suggéré : {inc['suggestions']}" if inc["suggestions"] else ""
            print(f"  INCONNUE : {inc['nom']}{sug}")
        if len(res["inconnues"]) > 15:
            print(f"  … +{len(res['inconnues']) - 15} autres")
    return 4 if res["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
