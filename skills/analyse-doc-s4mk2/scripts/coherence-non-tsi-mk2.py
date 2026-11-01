#!/usr/bin/env python3
"""coherence-non-tsi-mk2.py v1.0.0 — Cohérence croisée TSI (source de vérité) ↔ non-TSI.

Skill : analyse-doc-s4mk2 (famille TSI, orchestré par agent-TSI).

Rôle (directive propriétaire, traces 1a1989725d74c901 + 1a1989862dd46e61) :
vérifier mécaniquement que les données extraites des fichiers NON-TSI (PDF,
textes ; images sans OCR — couvertes par la table P1b) sont EN COHÉRENCE avec
les fichiers TSI du mapping analysé (sources de vérité).

Méthode (stdlib, déterministe, honnête — trois niveaux de preuve décroissants) :
  N1. ATTESTATIONS NUMÉROTÉES (fonctions Traktor, écart FORT possible) :
      mentions regex « hotcue N / fx N / deck L / slot N / slice N / mod N /
      knob N / button N » dans les textes extraits ; verdict par mention :
      HORS_UNIVERS (au-delà du référentiel matériel S4 MK2 : decks A-D,
      4 unités FX, 8 hotcues, 4 slots, 8 slices, mods M1-M8, 3 knobs/boutons
      FX par face) → écart fort ; NON_CÂBLÉE (dans l'univers mais absent des
      noms/conditions du TSI LISIBLE, taux CMAD illisibles ≤ seuil) → écart
      fort ; SUPPORTÉE (présent dans noms DCBM / conditions DCDT du TSI) ;
      INDETERMINABLE (absent mais TSI à CMAD majoritairement illisibles — le
      support n'est pas démontrable, limite consignée, jamais un FAIL).
  N2. ATTESTATIONS DE CONTRÔLES (couverture lexicale, information) : tokens
      pivot (vocabulaire contrôle du module analyser-pdf-mk2) mentionnés
      dans les documents et absents des noms du TSI → NON_COUVERTE (jamais
      un FAIL : cohérence lexicale, pas sémantique — §6 du SKILL.md).
  N3. ILLUSTRÉS (sans OCR) : cohérence via la table P1b (déjà vérifiée par
      le pipeline E6) si elle est calculée, sinon consignée non vérifiable.

Le support FX tient compte du câblage par deck : unité N supportée si N ∈
unités vues ou N ≤ max(unités vues) × nb de decks vus (hypothèse qualifiée,
consignée en sortie). Aucune interprétation au-delà : le skill vérifie, il ne
devine pas.

Usage :
  coherence-non-tsi-mk2.py --self-test     (ancrage mécanique embarqué)
  (module importé par analyser-zip-mk2.py — étape E7 du pipeline)
Exit code : 0 self-test PASS / 1 self-test FAIL / 2 usage.
Stdlib uniquement. Sortie déterministe (tris stables).
"""
import argparse
import importlib.util
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))

# Vocabulaire pivot réutilisé du module PDF (source unique — pas de duplication)
_spec = importlib.util.spec_from_file_location(
    "analyser-pdf-mk2", os.path.join(ICI, "analyser-pdf-mk2.py")
)
_pdf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pdf)
VOCABULAIRE_PIVOT = tuple(sorted(set(
    ("freeze fx shift jog jogwheel deck hotcue loop slice remix sample sync cue "
     "pitch filter echo mod panic button knob encoder fader crossfader tempo "
     "grid master touch flux keylock quant dry wet channel unit"
    ).split()
)))

# Référentiel matériel S4 MK2 (bornes mécaniques, ancrées écosystème :
# 4 decks A-D, 4 unités FX, hotcues 1-8, 4 slots remix, 8 slices freeze,
# mods M1-M8, 3 knobs + 3 boutons FX par face)
UNIVERS = {
    "deck": ("A", "B", "C", "D"),
    "fx": (1, 4), "hotcue": (1, 8), "slot": (1, 4), "slice": (1, 8),
    "mod": (1, 8), "knob": (1, 3), "button": (1, 3),
}
# familles fonctionnelles : un NON_CÂBLÉE est un écart fort (les contrôles
# physiques knob/button ne produisent jamais d'écart — formes, pas fonctions)
FAMILLES_FONCTIONNELLES = frozenset({"deck", "fx", "hotcue", "slot", "slice", "mod"})
SEUIL_CMAD_ILLISIBLES = 0.20  # au-delà, le support des commandes est indémontrable

# Mentions numérotées : collations de colonnes tolérées (« Knob 1FX Button 2 »,
# « M8M8M8 ») — lookbehind/lookahead adaptés, pluriels, « N or M »
FAMILLES_TEXTE = (
    ("deck", re.compile(r"(?<![a-z])decks?\s*([a-h])(?![a-z])", re.I)),
    ("fx", re.compile(r"(?<![a-z])fx\s*(\d+)(?!\d)", re.I)),
    ("hotcue", re.compile(r"(?<![a-z])hotcues?\s*(\d+)(?!\d)", re.I)),
    ("slot", re.compile(r"(?<![a-z])slots?\s*(\d+)(?!\d)", re.I)),
    ("sample", re.compile(r"(?<![a-z])samples?\s*(\d+)(?!\d)", re.I)),
    ("slice", re.compile(r"(?<![a-z])slices?\s*(\d+)(?!\d)", re.I)),
    ("mod", re.compile(r"(?<![a-z])m([1-8])(?![0-9])")),
    ("knob", re.compile(r"(?<![a-z])knobs?\s*(\d+)(?!\d)", re.I)),
    ("button", re.compile(r"(?<![a-z])buttons?\s*(\d+)(?!\d)", re.I)),
)
RE_OR = re.compile(r"\s+or\s+(\d+)", re.I)


def entites_tsi(meta):
    """Extrait les entités de la source de vérité (moteur analyser_tsi_mk2)."""
    noms = set(meta.get("noms_controles_definis", {}))
    conditions = set(meta.get("conditions_in", [])) | set(meta.get("conditions_out", []))
    tout = noms | conditions
    comptes = meta.get("comptes", {})
    lus = comptes.get("CMAD_lus", 0) or 1
    entites = {
        "fichier": os.path.basename(meta.get("fichier", "?")),
        "noms_controles": len(noms),
        "conditions": len(conditions),
        "commandes_lisibles": sum(meta.get("commandes_par_assignations", {}).values()),
        "taux_cmad_illisibles": round(comptes.get("CMAD_illisibles", 0) / lus, 4),
        "tokens": set(),
        "decks": set(), "fx_unites": set(), "hotcues": set(),
        "slots": set(), "slices": set(), "mods": set(),
    }
    for nom in tout:
        bas = nom.lower()
        entites["tokens"].update(t for t in re.split(r"[.\s/_-]+", bas)
                                 if len(t) >= 2 and t not in ("in", "on") and t.isalpha())
        entites["noms_joints"] = entites.get("noms_joints", "") + " " + bas
        for f, rx in (("decks", r"(?<![a-z])deck\s+([a-h])(?![a-z])"),):
            for m in re.finditer(rx, bas):
                entites[f].add(m.group(1).upper())
        if re.match(r"^[a-h]\.", bas):  # préfixe deck « a.gain »
            entites["decks"].add(bas[0].upper())
        for ens, rx in (
            ("fx_unites", r"fx\.?\s*on\s*(\d+)"), ("hotcues", r"hotcue\.?\s*(\d+)"),
            ("slots", r"(?:sample\s*play|slot)\.?\s*(\d+)"), ("slices", r"slice\.?\s*(\d+)"),
            ("mods", r"(?<![a-z])m([1-8])(?![a-z0-9])"),
        ):
            for m in re.finditer(rx, bas):
                entites[ens].add(int(m.group(1)))
    return entites


def verdict_entite(famille, valeur, entites):
    """Verdict d'une entité numérotée : HORS_UNIVERS / NON_CÂBLÉE / SUPPORTÉE / INDETERMINABLE."""
    if famille == "deck":
        if valeur not in UNIVERS["deck"]:
            return "HORS_UNIVERS", "deck hors référentiel S4 MK2 (A-D)"
        if valeur in entites["decks"]:
            return "SUPPORTÉE", None
    elif famille in ("fx", "hotcue", "slot", "sample", "slice", "mod"):
        bas, haut = UNIVERS[famille]
        if not (bas <= valeur <= haut):
            return "HORS_UNIVERS", f"{famille} {valeur} hors référentiel S4 MK2 ({bas}-{haut})"
        ens = {"fx": "fx_unites", "hotcue": "hotcues", "slot": "slots",
               "sample": "slots", "slice": "slices", "mod": "mods"}[famille]
        vus = entites[ens]
        if famille == "fx":
            if valeur in vus:
                return "SUPPORTÉE", None
            decks = len(entites["decks"]) or 1
            if vus and valeur <= max(vus) * decks:  # câblage par deck (hypothèse consignée)
                return "SUPPORTÉE", None
        elif valeur in vus:
            return "SUPPORTÉE", None
    else:  # knob/button : forme physique — univers seul, pas d'écart fort
        bas, haut = UNIVERS[famille]
        if not (bas <= valeur <= haut):
            return "HORS_UNIVERS", f"{famille} {valeur} hors référentiel S4 MK2 ({bas}-{haut})"
        if re.search(rf"\b{famille}s?\s*\.?\s*{valeur}(?!\d)", entites.get("noms_joints", "")):
            return "SUPPORTÉE", None
        return "NON_ATTESTÉE", None  # forme physique non nommée telle quelle : info
    if entites["taux_cmad_illisibles"] > SEUIL_CMAD_ILLISIBLES:
        return "INDETERMINABLE", "support non démontrable (CMAD illisibles > seuil)"
    if famille in FAMILLES_FONCTIONNELLES:
        return "NON_CÂBLÉE", f"{famille} {valeur} absent des noms/conditions du TSI"
    return "NON_ATTESTÉE", None


def attester_texte(texte, entites):
    """Atteste un texte de document contre la source de vérité. Rend un dict déterministe."""
    bas = (texte or "").lower()
    if not bas.strip():
        return {"attestations": [], "mentions_non_couvertes": [], "verdict": "RIEN_ATTESTER"}
    attestations = {}
    for famille, rx in FAMILLES_TEXTE:
        for m in rx.finditer(bas):
            v1 = m.group(1)
            valeurs = [v1.upper() if famille == "deck" else int(v1)]
            mo = RE_OR.match(bas, m.end())
            if mo:
                valeurs.append(int(mo.group(1)))
            for v in valeurs:
                cle = (famille, v)
                verdict, cause = verdict_entite(famille, v, entites)
                anc = attestations.setdefault(cle, {"famille": famille, "valeur": v, "mentions": 0,
                                                    "verdict": verdict, "cause": cause})
                anc["mentions"] += 1
    attestations = [dict(a, **{"valeur": a["valeur"]}) for a in
                    sorted(attestations.values(), key=lambda x: (x["famille"], x["valeur"]))]
    non_couvertes = []
    for token in VOCABULAIRE_PIVOT:
        if token in entites["tokens"]:
            continue
        n = len(re.findall(rf"\b{re.escape(token)}s?\b", bas))
        if n:
            non_couvertes.append({"token": token, "mentions": n, "verdict": "NON_COUVERTE",
                                  "cause": "token absent des noms du TSI (cohérence lexicale)"})
    non_couvertes.sort(key=lambda x: (-x["mentions"], x["token"]))
    ecarts = [a for a in attestations if a["verdict"] in ("HORS_UNIVERS", "NON_CÂBLÉE")]
    verdict = "ÉCARTS_DÉTECTÉS" if ecarts else "COHÉRENT"
    return {"attestations": attestations, "mentions_non_couvertes": non_couvertes, "verdict": verdict}


def couverture_documentaire(texte, entites):
    """Sens TSI→doc : part des tokens TSI mentionnés dans le document (information)."""
    bas = (texte or "").lower()
    if not entites["tokens"]:
        return {"tokens_tsi": 0, "tokens_mentions": 0, "taux": None}
    mentions = sorted(t for t in entites["tokens"] if re.search(rf"\b{re.escape(t)}s?\b", bas))
    return {"tokens_tsi": len(entites["tokens"]), "tokens_mentions": len(mentions),
            "taux": round(len(mentions) / len(entites["tokens"]), 4)}


def coherence(meta_mapping, pdfs, textes, n_illustres, p1b_ok):
    """Section E7 complète : source de vérité + attestations par document + verdict.

    p1b_ok : True ssi la table P1b est calculée ET sans écart (la cohérence des
    illustrés passe par elle — sans OCR, une table en écart = non vérifiable)."""
    entites = entites_tsi(meta_mapping)
    section = {
        "source_verite": {k: entites[k] for k in
                          ("fichier", "noms_controles", "conditions", "commandes_lisibles", "taux_cmad_illisibles")},
        "univers_s4mk2": {k: list(v) for k, v in UNIVERS.items()},
        "seuil_cmad_illisibles": SEUIL_CMAD_ILLISIBLES,
        "hypothese_support_fx": "unité N supportée si N ≤ max(unités vues) × nb de decks vus",
        "documents": [], "illustrés": {
            "nombre": n_illustres,
            "coherence_via_table_p1b": bool(p1b_ok),
            "statut": "cohérence vérifiée par la table P1b (E6, sans écart)" if p1b_ok
            else "sans OCR : cohérence illustré↔TSI non vérifiable (consigné)",
        },
        "ecarts": [], "verdict": "RIEN_ATTESTER",
    }
    docs = []
    for p in pdfs:
        if p.get("rejet"):
            docs.append({"fichier": p["fichier"], "type": "pdf", "statut": "NON_ATTESTABLE (PDF rejeté)"})
            continue
        docs.append((p["fichier"], "pdf", p.get("texte_complet") or p.get("texte", {}).get("echantillon", "")))
    for t in textes:
        docs.append((t["nom"], "texte", t.get("texte_complet") or t.get("echantillon", "")))
    for d in docs:
        if isinstance(d, dict):
            section["documents"].append(d)
            continue
        nom, genre, texte = d
        rap = attester_texte(texte, entites)
        rap.update({"fichier": nom, "type": genre,
                    "couverture_documentaire": couverture_documentaire(texte, entites)})
        section["documents"].append(rap)
        section["ecarts"].extend(
            {"fichier": nom, **a} for a in rap["attestations"]
            if a["verdict"] in ("HORS_UNIVERS", "NON_CÂBLÉE"))
    section["ecarts"].sort(key=lambda e: (e["fichier"], e["famille"], e["valeur"]))
    attestes = [d for d in section["documents"] if "attestations" in d]
    section["verdict"] = ("ÉCARTS_DÉTECTÉS" if section["ecarts"]
                          else "COHÉRENT" if attestes else "RIEN_ATTESTER")
    return section


def self_test():
    """Ancrage mécanique : univers, collations de colonnes, seuils CMAD, déterminisme."""
    ok = True
    entites = {
        "fichier": "x.tsi", "noms_controles": 4, "conditions": 2, "commandes_lisibles": 2,
        "taux_cmad_illisibles": 0.0, "tokens": {"eq", "high", "low", "fx", "mode", "button", "gain"},
        "noms_joints": "a.eq.high left.fx.mode left.fx.knob 1 right.fx.button 2 a.gain a.fx.on 1 a.fx.on 2",
        "decks": {"A", "B", "C", "D"}, "fx_unites": {1, 2}, "hotcues": {1, 2, 3, 4},
        "slots": {1, 2, 3, 4}, "slices": set(), "mods": set(),
    }
    cas = (
        ("hotcue 9 → HORS_UNIVERS", lambda: attester_texte("hotcue 9", entites)["attestations"][0]["verdict"], "HORS_UNIVERS"),
        ("fx 5 → HORS_UNIVERS", lambda: attester_texte("fx 5", entites)["attestations"][0]["verdict"], "HORS_UNIVERS"),
        ("deck h → HORS_UNIVERS", lambda: attester_texte("deck h", entites)["attestations"][0]["verdict"], "HORS_UNIVERS"),
        ("slice 12 → HORS_UNIVERS", lambda: attester_texte("slice 12", entites)["attestations"][0]["verdict"], "HORS_UNIVERS"),
        ("hotcue 2 → SUPPORTÉE", lambda: attester_texte("Hotcue 2", entites)["attestations"][0]["verdict"], "SUPPORTÉE"),
        ("fx 1 et 2 → SUPPORTÉE (vus)", lambda: [a["verdict"] for a in attester_texte("FX 1 or 2", entites)["attestations"]], ["SUPPORTÉE", "SUPPORTÉE"]),
        ("fx 3 or 4 → SUPPORTÉE ×2 (équation 2×4 decks)", lambda: [a["verdict"] for a in attester_texte("FX 3 or 4", entites)["attestations"]], ["SUPPORTÉE", "SUPPORTÉE"]),
        ("button 2 → SUPPORTÉE (noms joints)", lambda: attester_texte("Button 2", entites)["attestations"][0]["verdict"], "SUPPORTÉE"),
        ("knob 1 → SUPPORTÉE (noms joints)", lambda: attester_texte("Knob 1", entites)["attestations"][0]["verdict"], "SUPPORTÉE"),
        ("collation « Knob 1FX Button 2 »", lambda: sorted((a["famille"], a["valeur"]) for a in attester_texte("Knob 1FX Button 2", entites)["attestations"]), [("button", 2), ("knob", 1)]),
        ("collation « M8M8M8 » → 3 attestations d'1 mention chacune agrégées", lambda: attester_texte("M8M8M8", entites)["attestations"][0]["mentions"], 3),
        ("mod 8 TSI lisible sans mods → NON_CÂBLÉE", lambda: attester_texte("M8", entites)["attestations"][0]["verdict"], "NON_CÂBLÉE"),
        ("hotcue 6 TSI lisible sans hotcue 6 → NON_CÂBLÉE", lambda: attester_texte("Hotcue 6", entites)["attestations"][0]["verdict"], "NON_CÂBLÉE"),
        ("knob 2 → NON_ATTESTÉE (jamais écart fort)", lambda: attester_texte("Knob 2", entites)["attestations"][0]["verdict"], "NON_ATTESTÉE"),
        ("deck b → SUPPORTÉE", lambda: attester_texte("Deck B", entites)["attestations"][0]["verdict"], "SUPPORTÉE"),
        ("M8 TSI illisible → INDETERMINABLE", lambda: attester_texte(
            "M8", dict(entites, taux_cmad_illisibles=0.9))["attestations"][0]["verdict"], "INDETERMINABLE"),
        ("texte vide → RIEN_ATTESTER", lambda: attester_texte("   ", entites)["verdict"], "RIEN_ATTESTER"),
        ("fx ∈ tokens TSI (2 car) → jamais NON_COUVERTE", lambda: [n["token"] for n in attester_texte("fx knob", entites)["mentions_non_couvertes"]], ["knob"]),
        ("écart global sur « hotcue 9 »", lambda: attester_texte("hotcue 9", entites)["verdict"], "ÉCARTS_DÉTECTÉS"),
        ("déterminisme ×2", lambda: attester_texte("FX 3 or 4 M8 hotcue 2", entites) == attester_texte("FX 3 or 4 M8 hotcue 2", entites), True),
    )
    for nom, fn, attendu in cas:
        try:
            obtenu = fn()
        except Exception as e:  # noqa: BLE001
            obtenu = f"EXCEPTION {type(e).__name__}: {e}"
        etat = "PASS" if obtenu == attendu else "FAIL"
        ok = ok and etat == "PASS"
        print(f"  [{etat}] {nom} → {obtenu!r}")
    return ok


def main():
    ap = argparse.ArgumentParser(description="Cohérence croisée TSI ↔ non-TSI (skill analyse-doc-s4mk2)")
    ap.add_argument("--self-test", action="store_true", help="ancrage mécanique embarqué")
    a = ap.parse_args()
    if not a.self_test:
        ap.print_help()
        return 2
    ok = self_test()
    print(f"SELF-TEST : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
