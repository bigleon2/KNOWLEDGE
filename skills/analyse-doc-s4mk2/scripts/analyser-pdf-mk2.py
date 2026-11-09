#!/usr/bin/env python3
"""analyser-pdf-mk2.py v1.0.0 — Analyse mécanique d'un PDF compagnon de mapping S4 MK2.

Skill : analyse-doc-s4mk2 (famille TSI, orchestré par agent-TSI).

Rôle : les packs de mapping sont livrés avec des documents non-TSI liés (listes
d'assignation, descriptions du fonctionnement, notices). Le pipeline
analyser-zip-mk2.py doit les ANALYSER et non les laisser « autres » muets.
Ce module extrait mécaniquement d'un PDF (stdlib uniquement, zlib + parse
des opérateurs texte) :
  - version PDF, nb de pages, polices (BaseFont, présence ToUnicode + nb entrées CMap) ;
  - texte extractible (opérateurs Tj/TJ, décodage via CMap ToUnicode bfchar/bfrange,
    fallback cp1252 pour polices sans ToUnicode), codes non mappés, échantillon ;
  - mots-clés du vocabulaire mapping détectés (comptes par mot, tri stable) ;
  - métadonnées (titre, producteur, date de création) ;
  - signature de chaque flux (décompressé/échec).

Limites assumées (§6 du SKILL.md) : PDF scannés (image) → AUCUN_TEXTE_EXTRAIT ;
PDF 1.5+ avec ObjStm non résolus → objets manquants consignés ; polices sans
ToUnicode décodées cp1252 (approximation documentée).

Usage :
  analyser-pdf-mk2.py <fichier.pdf> [--json OUT.json] [--max-cars N]
Exit code : 0 analysé / 1 PDF invalide (rejet propre) / 2 usage.
Stdlib uniquement. Lecture seule. Sortie JSON déterministe (tri stable).
"""
import argparse
import json
import os
import re
import sys
import zlib

# Vocabulaire mécanique du mapping S4 MK2 / Traktor (comptes par mot, casse ignorée)
MOTS_CLES = (
    "traktor s4 mk2 mapping freeze fx shift jog jogwheel deck hotcue loop slice "
    "mode remix sample sync cue pitch filter echo mod panic button knob encoder "
    "fader crossfader tempo beat grid master super touch flux keylock quant dry "
    "wet effect assignment channel unit"
).split()

MAX_BFRANGE = 65535  # garde-fou contre une expansion de plage absurde


class RejetPropre(Exception):
    """Rejet contrôlé sans traceback (rc porté par l'exception)."""

    def __init__(self, message, rc=1):
        super().__init__(message)
        self.rc = rc


def decoder_meta(brut):
    """Décode une chaîne PDF : hex UTF-16BE (BOM FEFF) ou littérale cp1252."""
    m = re.match(rb"\s*<([0-9A-Fa-f]+)>", brut)
    if m:
        h = m.group(1)
        if len(h) % 2:
            h += b"0"
        o = bytes.fromhex(h.decode("ascii"))
        if o[:2] == b"\xfe\xff":
            try:
                return o[2:].decode("utf-16-be"), True
            except UnicodeDecodeError:
                return o[2:].decode("latin-1"), True
        return o.decode("latin-1"), True
    m = re.match(rb"\s*\(((?:\\.|[^\\()])*)\)", brut, re.S)
    if m:
        return m.group(1).decode("cp1252", errors="replace"), False
    return None, False


def parser_cmap(data):
    """Parse un CMap ToUnicode : codespacerange + bfchar + bfrange.

    Gère bfrange forme DIRECTE (<s> <e> <u>) et forme TABLEAU (<s> <e> [u1 u2 …]),
    en respectant l'ordre du flux (une entrée ultérieure l'emporte sur une
    entrée antérieure pour un même code — sémantique lecteurs PDF).
    Rend (cmap {code: unicode}, octets_par_code issu du codespacerange réel).
    """
    cmap = {}

    def uni(h):
        return "".join(chr(int(h[j : j + 4], 16)) for j in range(0, len(h), 4))

    for m in re.finditer(rb"begin(bfchar|bfrange)(.*?)end\1", data, re.S):
        genre, bloc = m.group(1), m.group(2)
        if genre == b"bfchar":
            for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", bloc):
                cmap[int(src, 16)] = uni(dst)
        else:
            for mm in re.finditer(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(\[([^\]]*)\]|<[0-9A-Fa-f]+>)", bloc):
                s, e = int(mm.group(1), 16), int(mm.group(2), 16)
                if e < s or e - s > MAX_BFRANGE:
                    continue
                if mm.group(4) is not None:  # forme tableau : i-ème code → i-ème valeur
                    for k, v in enumerate(re.findall(rb"<([0-9A-Fa-f]+)>", mm.group(4))):
                        cmap[s + k] = uni(v)
                else:  # forme directe : plage continue
                    base = int(mm.group(3)[1:-1], 16)
                    for k in range(e - s + 1):
                        cmap[s + k] = chr(base + k)
    mo = re.search(rb"begincodespacerange\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", data)
    if mo:
        octets = max(1, min(2, (len(mo.group(1)) + 1) // 2))
    else:
        octets = 2 if max(cmap, default=0) > 0xFF else 1
    return cmap, octets


def decadrer_litteral(s):
    """Décode les échappements PDF d'une chaîne littérale (octets)."""
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i : i + 1]
        if c == b"\\" and i + 1 < len(s):
            n = s[i + 1 : i + 2]
            if n in b"nrtbf()\\\\":
                out.extend({b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f"}.get(n, n))
                i += 2
                continue
            m = re.match(rb"\\([0-7]{1,3})", s[i:])
            if m:
                out.append(int(m.group(1), 8) & 0xFF)
                i += 1 + len(m.group(1))
                continue
            out.extend(n)
            i += 2
            continue
        out.extend(c)
        i += 1
    return bytes(out)


def extraire_texte_contenu(contenu, cmaps_par_police, espaces_par_police):
    """Extrait le texte d'un flux de contenu (Tj/TJ, séparateurs Td/TD/T*/ET).

    Rend (texte, codes_non_mappes, litéraux_bruts_utilisés).
    """
    hors = []
    texte = []
    non_mappes = 0
    police = None
    en_attente = []

    def vider():
        nonlocal non_mappes, en_attente
        texte.extend(en_attente)
        en_attente = []

    motif = re.compile(
        rb"<([0-9A-Fa-f]*)>|\(((?:\\.|[^\\()])*)\)|(T[jJ]|Td|TD|T\*|ET|BT)|/([A-Za-z0-9]+)\s+[-0-9.]+\s+Tf"
    )
    for m in motif.finditer(contenu):
        hexa, lit, op, fnt = m.group(1), m.group(2), m.group(3), m.group(4)
        if fnt is not None:
            police = fnt.decode("latin-1")
            vider()
            continue
        if op is not None:
            if op in (b"Tj", b"TJ"):
                vider()
            elif op in (b"Td", b"TD", b"T*", b"ET") and en_attente:
                texte.append("\n")
            en_attente = []
            continue
        cmap = cmaps_par_police.get(police) if police else None
        espace = espaces_par_police.get(police, 1) if police else 1
        if hexa is not None:
            if len(hexa) % 2:
                hexa += b"0"
            brut = bytes.fromhex(hexa.decode("ascii"))
            pas = espace if cmap else 1
            for j in range(0, len(brut), pas):
                code = int.from_bytes(brut[j : j + pas], "big")
                if cmap and code in cmap:
                    en_attente.append(cmap[code])
                elif cmap is None:
                    en_attente.append(brut[j : j + pas].decode("cp1252", errors="replace"))
                else:
                    non_mappes += 1
        elif lit is not None:
            brut = decadrer_litteral(lit)
            if cmap:
                pas = espace
                for j in range(0, len(brut), pas):
                    code = int.from_bytes(brut[j : j + pas], "big")
                    if code in cmap:
                        en_attente.append(cmap[code])
                    else:
                        non_mappes += 1
            else:
                en_attente.append(brut.decode("cp1252", errors="replace"))
    vider()
    return "".join(texte), non_mappes


def analyser_pdf(buf, nom="fichier.pdf", max_cars=300):
    """Analyse mécanique d'un PDF en mémoire. Rend un dict déterministe."""
    if buf[:5] != b"%PDF-":
        raise RejetPropre(f"REJET PROPRE : {nom} n'est pas un PDF (signature absente)")
    m = re.match(rb"%PDF-(\d\.\d)", buf)
    version = m.group(1).decode("ascii") if m else "?"
    objets = {}
    for mo in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", buf, re.S):
        objets[int(mo.group(1))] = mo.group(2)
    # streams par objet (décompressés si FlateDecode)
    streams = {}
    echecs = 0
    for num, corps in objets.items():
        ms = re.search(rb"stream\r?\n(.*?)endstream", corps, re.S)
        if not ms:
            continue
        brut = ms.group(1)
        if b"FlateDecode" in corps.split(b"stream", 1)[0]:
            try:
                brut = zlib.decompress(brut)
            except zlib.error:
                echecs += 1
                continue
        streams[num] = brut
    # polices : BaseFont + ToUnicode → cmap
    polices = []
    cmaps_par_police = {}
    espaces_par_police = {}
    fontes_par_ref = {}
    for num, corps in objets.items():
        if not re.search(rb"/Type\s*/Font\b", corps):
            continue
        mb = re.search(rb"/BaseFont\s*/([A-Za-z0-9+-]+)", corps)
        base = mb.group(1).decode("latin-1") if mb else "?"
        mt = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", corps)
        entrees = 0
        if mt:
            data = streams.get(int(mt.group(1)), b"")
            cmap, octets = parser_cmap(data)
            entrees = len(cmap)
            cmaps_par_police[str(num)] = cmap
            espaces_par_police[str(num)] = octets
        polices.append({"objet": num, "basefont": base, "tounicode": bool(mt), "cmap_entries": entrees, "octets_code": espaces_par_police.get(str(num), 1)})
        fontes_par_ref[num] = str(num)
    # pages → contenus + ressources (fonts par nom)
    pages = [n for n, c in objets.items() if re.search(rb"/Type\s*/Page\b(?!s)", c)]
    fonte_par_nom = {}
    contenus = []
    for p in pages:
        corps = objets[p]
        mr = re.search(rb"/Resources\s+(\d+)\s+0\s+R", corps)
        res = objets[int(mr.group(1))] if mr else corps
        mf = re.search(rb"/Font\s+(\d+)\s+0\s+R", res)
        dict_f = objets[int(mf.group(1))] if mf else res
        for nom_fonte, ref in re.findall(rb"/([A-Za-z0-9]+)\s+(\d+)\s+0\s+R", dict_f):
            if int(ref) in fontes_par_ref:
                fonte_par_nom[nom_fonte.decode("latin-1")] = fontes_par_ref[int(ref)]
        mc = re.search(rb"/Contents\s+(\d+)\s+0\s+R", corps)
        if mc:
            contenus.append(int(mc.group(1)))
        else:
            mca = re.search(rb"/Contents\s*\[([^\]]*)\]", corps)
            if mca:
                contenus.extend(int(r) for r in re.findall(rb"(\d+)\s+0\s+R", mca.group(1)))
    # secours : tous les flux contenant des opérateurs texte
    if not contenus:
        contenus = [n for n, d in streams.items() if b"BT" in d and (b"Tj" in d or b"TJ" in d)]
    texte_brut = []
    non_mappes = 0
    cmap_par_nom = {nom: cmaps_par_police.get(ref) for nom, ref in sorted(fonte_par_nom.items())}
    espace_par_nom = {nom: espaces_par_police.get(ref, 1) for nom, ref in sorted(fonte_par_nom.items())}
    for n in contenus:
        d = streams.get(n)
        if not d:
            continue
        t, k = extraire_texte_contenu(d, cmap_par_nom, espace_par_nom)
        texte_brut.append(t)
        non_mappes += k
    texte = "".join(texte_brut)
    texte = re.sub(r"[ \t]+", " ", texte).strip()
    # métadonnées (objet Info / catalogue)
    meta = {}
    for cle in ("Title", "Producer", "Creator"):
        mm = re.search(rb"/" + cle.encode() + rb"\s*<([0-9A-Fa-f\s]+)>", buf)
        ml = re.search(rb"/" + cle.encode() + rb"\s*\(((?:\\.|[^\\()])*)\)", buf)
        if mm:
            v, _ = decoder_meta(b"<" + re.sub(rb"\s", b"", mm.group(1)) + b">")
            if v:
                meta[cle.lower()] = v
        elif ml:
            meta[cle.lower()] = decadrer_litteral(ml.group(1)).decode("cp1252", errors="replace")
    md = re.search(rb"/CreationDate\s*\(([^)]*)\)", buf)
    if md:
        meta["date_creation"] = md.group(1).decode("latin-1")
    # mots-clés du vocabulaire mapping
    bas = texte.lower()
    mots_cles = {}
    for mot in MOTS_CLES:
        c = len(re.findall(r"\b" + re.escape(mot) + r"s?\b", bas))
        if c:
            mots_cles[mot] = c
    mots_cles = dict(sorted(mots_cles.items(), key=lambda kv: (-kv[1], kv[0])))
    mots = [w for w in re.split(r"\s+", texte) if w]
    return {
        "fichier": nom,
        "taille": len(buf),
        "version_pdf": version,
        "pages": len(pages) if pages else max(1, len(contenus)),
        "polices": sorted(polices, key=lambda p: (p["objet"],)),
        "texte": {
            "statut": "TEXTE_EXTRAIT" if texte else "AUCUN_TEXTE_EXTRAIT",
            "caracteres": len(texte),
            "mots": len(mots),
            "codes_non_mappes": non_mappes,
            "echantillon": texte[:max_cars],
        },
        "mots_cles_mapping": mots_cles,
        "metadonnees": meta,
        "flux": {"objets": len(objets), "streams": len(streams) + echecs, "streams_decompresses": len(streams), "streams_echec": echecs},
    }


def main():
    ap = argparse.ArgumentParser(description="Analyse mécanique d'un PDF compagnon de mapping S4 MK2")
    ap.add_argument("pdf")
    ap.add_argument("--json", help="écrire le rapport JSON dans ce fichier")
    ap.add_argument("--max-cars", type=int, default=300, help="longueur de l'échantillon de texte")
    try:
        a = ap.parse_args()
        if not os.path.isfile(a.pdf):
            raise RejetPropre(f"USAGE : fichier introuvable : {a.pdf}", 2)
        r = analyser_pdf(open(a.pdf, "rb").read(), os.path.basename(a.pdf), a.max_cars)
        print(f"fichier     : {r['fichier']} ({r['taille']} o, PDF {r['version_pdf']})")
        print(f"pages       : {r['pages']} — polices : {', '.join(p['basefont'] for p in r['polices']) or 'aucune'}")
        t = r["texte"]
        print(f"texte       : {t['statut']} — {t['caracteres']} caractères, {t['mots']} mots, {t['codes_non_mappes']} codes non mappés")
        mc = r["mots_cles_mapping"]
        print(f"mots-clés   : {sum(mc.values())} occurrences — top : {dict(list(mc.items())[:8])}")
        if r["metadonnees"]:
            print(f"métadonnées : {r['metadonnees']}")
        if a.json:
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(r, fh, ensure_ascii=False, indent=2)
            print(f"JSON → {a.json}")
        return 0
    except RejetPropre as e:
        print(e)
        return e.rc


if __name__ == "__main__":
    sys.exit(main())
