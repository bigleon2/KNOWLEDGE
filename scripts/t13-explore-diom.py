#!/usr/bin/env python3
"""t13-explore-diom.py — exploration du format DIOM (TSI SXM) pour ancrer le moteur Go.

v2 : préfixes auto-détectés (DIOM sans préfixe, DEVS/CMAS/DCBM avec compteur,
DEVI avec 4+n*2). Parcours TLV id 4 octets ASCII + taille UInt32 big-endian.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import base64
import re
import struct
import sys

TSI = "/home/z/my-project/tools/sxm/super-xtreme-mapper/XtremeMapping/XtremeMappingTests/Fixtures/TSI/traktor-4.5.1-xone-k3-benchmark-01-continuous.tsi"

CONTENEURS = {"DIOM", "DEVS", "DEVI", "DDAT", "DDCB", "CMAS"}


def parse_frames(data: bytes, offset: int = 0, end: int | None = None, max_nodes: int = 500):
    """Parcourt les trames TLV (id 4 octets ASCII + taille UInt32 big-endian) et retourne les nœuds."""
    if end is None:
        end = len(data)
    out = []
    while offset + 8 <= end and len(out) < max_nodes:
        fid = data[offset:offset + 4]
        if not all(65 <= b <= 90 for b in fid):
            break
        (size,) = struct.unpack(">I", data[offset + 4:offset + 8])
        if offset + 8 + size > end:
            break
        out.append((fid.decode(), data[offset + 8:offset + 8 + size], offset))
        offset += 8 + size
    return out


def utf16_guess(raw: bytes):
    """Devine et décode une chaîne UTF-16 préfixée (longueur UInt32) — retourne la taille consommée ou -1."""
    if len(raw) < 4:
        return None
    (n,) = struct.unpack(">I", raw[:4])
    if 0 < n <= 64 and len(raw) >= 4 + n * 2:
        corps = raw[4:4 + n * 2]
        for enc in ("utf-16-be", "utf-16-le"):
            try:
                t = corps.decode(enc)
                if all(32 <= ord(c) < 127 for c in t):
                    return (enc, t)
            except UnicodeDecodeError:
                continue
    return None


def enfant_pos(fid: str, payload: bytes) -> int:
    """Rend la position de départ des frames enfants selon le conteneur."""
    if fid == "DIOM" or fid == "DDAT" or fid == "DDCB":
        return 0
    if fid in ("DEVS", "CMAS"):
        return 4
    if fid == "DEVI":
        (n,) = struct.unpack(">I", payload[:4])
        return 4 + n * 2
    return -1


def walk(data: bytes, fid: str, depth: int, budget=[0]):
    """Parcours récursif borné des conteneurs DIOM avec indentation par profondeur."""
    pad = "  " * depth
    pos = enfant_pos(fid, data)
    if pos < 0:
        return
    for cid, payload, off in parse_frames(data[pos:]):
        budget[0] += 1
        if budget[0] > 200:
            print(pad + "…budget")
            return
        g = utf16_guess(payload)
        note = f' str[{g[0]}]="{g[1]}"' if g else ""
        (cnt,) = struct.unpack(">I", payload[:4]) if len(payload) >= 4 and payload[:4].strip(b"\x00") == b"" or True else (0,)
        print(f"{pad}{cid} taille={len(payload)}@{off}{note}")
        if cid == "DCBM" and depth < 9:
            # liste DCBM : compteur + frames unitaires (id BE + utf16)
            for j, (u, up, uo) in enumerate(parse_frames(payload[4:])):
                if u != "DCBM" or j >= 2:
                    continue
                (bid,) = struct.unpack(">I", up[:4])
                g2 = utf16_guess(up[4:])
                print(f"{pad}  unit[{j}] binding={bid} note={g2}")
        if cid in CONTENEURS and depth < 8:
            walk(payload, cid, depth + 1, budget)


def main():
    """Extrait le blob DIOM du TSI de benchmark et affiche l'arborescence des trames."""
    src = open(TSI, encoding="utf-8").read()
    m = re.search(r'Entry Name="DeviceIO.Config.Controller" Type="3" Value="([^"]+)"', src)
    blob = base64.b64decode(m.group(1))
    print(f"blob DIOM : {len(blob)} octets")
    frames = parse_frames(blob)
    for fid, payload, off in frames:
        print(f"racine {fid} taille={len(payload)}@{off}")
        walk(payload, fid, 1)
    print("OK")


if __name__ == "__main__":
    sys.exit(main())
