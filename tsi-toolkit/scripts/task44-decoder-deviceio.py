#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task44-decoder-deviceio.py — Décode le blob DeviceIO.Config.Controller d'un .tsi Traktor 3.x
(intégré tsi-toolkit, adaptation Task 44 de scripts/decode-deviceio.py — Python stdlib, N3).

Usage :
  python3 task44-decoder-deviceio.py <fichier.tsi> [dossier_sortie]

Sorties (dossier par défaut : <dossier tsi>/deviceio) :
  blob.bin (binaire décodé), inventaire-deviceio.json, rapport-deviceio.txt

Idempotent ×2 (re-jeu = mêmes sorties). rc=0 OK, rc=3 usage/faute, rc=4 blob absent.
"""
import base64
import html
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SECTIONS = [
    "DEVS", "DEVI", "DEVD", "DDTA", "DDIF", "DDIV", "DDCM", "DDPT",
    "DDCT", "DCDT", "DCMA", "DCDC", "DCBM", "CMAD", "MDCH",
]


def extraire_blob(tsi_path: Path, entry_name: str = "DeviceIO.Config.Controller") -> bytes:
    data = tsi_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(
        r'<Entry Name="' + re.escape(entry_name) + r'"[^>]*Value="([^"]*)"', data
    )
    if not m:
        return b""
    return base64.b64decode(html.unescape(m.group(1)))


def extraire_utf16(blob: bytes) -> list:
    out = []
    i, n = 0, len(blob)
    cur = []
    while i + 1 < n:
        pair = blob[i : i + 2]
        code = pair[0] | (pair[1] << 8)
        if 0xD800 <= code <= 0xDBFF and i + 3 < n:
            lo = blob[i + 2] | (blob[i + 3] << 8)
            if 0xDC00 <= lo <= 0xDFFF:
                cur.append(chr(0x10000 + ((code - 0xD800) << 10) + (lo - 0xDC00)))
                i += 4
                continue
        if 0xD800 <= code <= 0xDFFF:
            if len(cur) >= 2:
                out.append("".join(cur))
            cur = []
            i += 1
            continue
        if 32 <= code < 0xFFFD and pair[1] != 0xFF:
            cur.append(chr(code))
            i += 2
        else:
            if len(cur) >= 2:
                out.append("".join(cur))
            cur = []
            i += 1 if pair[1] != 0x00 else 2
    if len(cur) >= 2:
        out.append("".join(cur))
    return out


def localiser_sections(blob: bytes) -> dict:
    found = defaultdict(list)
    for sec in SECTIONS:
        sig = sec.encode("ascii")
        start = 0
        while True:
            idx = blob.find(sig, start)
            if idx < 0:
                break
            found[sec].append(idx)
            start = idx + 1
    return dict(found)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 3
    tsi = Path(sys.argv[1])
    if not tsi.exists():
        print(f"ERREUR : fichier introuvable : {tsi}")
        return 3
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else tsi.parent / "deviceio"
    outdir.mkdir(parents=True, exist_ok=True)

    blob = extraire_blob(tsi)
    if not blob:
        print(f"DeviceIO.Config.Controller ABSENT de {tsi.name} (format 2.x ou settings sans device ?)")
        return 4
    (outdir / "blob.bin").write_bytes(blob)

    strings = extraire_utf16(blob)
    sections = localiser_sections(blob)
    prefixes = Counter()
    exemples = defaultdict(list)
    for s in strings:
        if "." in s and 2 <= len(s) < 80:
            p = s.split(".", 1)[0]
            if p.isalpha():
                prefixes[p] += 1
                if len(exemples[p]) < 6:
                    exemples[p].append(s)
    device_names = sorted({s for s in strings if ("S4" in s or "Kontrol" in s.lower())})[:20]
    versions = sorted({s for s in strings if re.match(r"^\d+\.\d+\.\d+", s)})[:10]

    inv = {
        "source": tsi.name,
        "taille_blob_octets": len(blob),
        "sections_detectees": {k: len(v) for k, v in sorted(sections.items())},
        "dcdt_signatures": sections.get("DCDT") and len(sections["DCDT"]) or 0,
        "nb_chaines_utf16": len(strings),
        "devices": device_names,
        "versions": versions,
        "prefixes": dict(prefixes.most_common(40)),
        "exemples_par_prefixe": dict(exemples),
        "chaines_completes": strings,
    }
    (outdir / "inventaire-deviceio.json").write_text(
        json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "RAPPORT DECODE DeviceIO.Config.Controller",
        f"Source : {tsi}",
        f"Taille blob : {len(blob)} octets",
        f"Sections : {inv['sections_detectees']}",
        f"Chaines UTF-16 : {len(strings)}",
        f"Devices : {device_names[:10]}",
        f"Versions : {versions[:6]}",
        "",
        "PREFIXES DE CONTROLES :",
    ] + [f"  {p:30s} {c}" for p, c in prefixes.most_common(30)]
    (outdir / "rapport-deviceio.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
