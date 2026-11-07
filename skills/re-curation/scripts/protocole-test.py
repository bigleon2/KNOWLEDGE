#!/usr/bin/env python3
"""protocole-test.py — Script PRINCIPAL du skill re-curation (v1.0.0).

Implémentation de la directive propriétaire (Task 72, directive complémentaire
1a1b7b297b7b4975) : « le skill "re-curation" devra être implémenté d'un script dont
l'objectif est de s'assurer $FACON [de façon cohérente, optimisée et fonctionnelle]
du maintien de l'optimisation du fonctionnement de mon écosystème pour qu'il soit
$FACON2 [(cohérent, optimisé et fonctionnel)] en faisant des tests $FACON2 (génère
un protocole de test adapté à mon écosystème) AVANT d'effectuer les "re-curation
progressive disclosure" sur les éléments de mon écosystème pour trouver la méthode
la plus optimisée et performante. »

Mécanique (méthode P0/P2/P5/P7 du SKILL.md — tests AVANT re-curation) :

  --pre <skill>        GÉNÈRE le protocole de test ADAPTÉ à l'élément ciblé (nature :
                       contrats triggers verbatim §A, read_when, evals, description,
                       sections, poids, gouvernance KB/ECO_SKILLS) puis l'EXÉCUTE en
                       phase PRE : baseline golden master → verdict GO / NO-GO.
                       Sortie : download/protocole-test-<skill>.json
  --post <skill>       Ré-exécute le protocole en phase POST (après re-curation) :
                       contrats == baseline (cohérent) + poids (optimisé) + pointeurs
                       et non-duplication (fonctionnel) → verdict MAINTIEN DE
                       L'OPTIMISATION / DÉRIVE.
  --verifier <skill>   Mode VÉRIFICATION d'une re-curation DÉJÀ exécutée (pointeurs
                       references/ valides, non-duplication 1024 o, seuils) — sans
                       exiger de protocole PRE antérieur.
  --compare <skill> --methodes <m1,m2,…>
                       Arbitrage des méthodes candidates : gains projetés calculés
                       des sections MESURÉES (jamais inventés) + conformité R4 →
                       la plus optimisée et performante (R4-compliantes seules
                       éligibles).
  --selftest           Auto-vérification en bac à sable (sait échouer).

Gardes : Python stdlib (N3) · étiquette SHARED du §0 normalisée à la comparaison
(leçon harnais v2 Task 72 — un bump SHARED écosystème n'est pas une dérive de
contrat) · phases de comparaison en lecture seule · le script n'invente jamais de
contenu (KO-L003) : il mesure, compare et rend un verdict mécanique.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

RACINE = Path("/home/z/my-project")
SEUIL_LOURD = 30 * 1024   # seuils de l'arbitre poids-chargement.py (v1.0.0)
SEUIL_CRITIQUE = 60 * 1024
METHODES = {  # registre des méthodes candidates (conformité R4 figée — le skill ne
    # valide jamais une méthode qui supprime sans archiver)
    "moves-r4-resumes": {"r4": True, "taux_gain": 0.88,
                         "note": "déplacements R4 byte-identité + résumés opérationnels inline (~12 % du déplacé reste inline)"},
    "moves-r4-pur": {"r4": True, "taux_gain": 0.97,
                     "note": "déplacements R4 + pointeurs 1-ligne (résumés minimaux — lisibilité à surveiller)"},
    "append-references-existantes": {"r4": True, "taux_gain": 0.88,
                                     "note": "append aux fichiers references/ existants (grille-token pattern)"},
    "suppression": {"r4": False, "taux_gain": 1.0,
                    "note": "DISQUALIFIÉE — suppression sans archivage R4 (interdite, listée pour mémoire)"},
}


def sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def normalise_shared(texte: str) -> str:
    """Étiquette SHARED normalisée (harnais v2 — bump écosystème ≠ dérive de contrat)."""
    return re.sub(r"SHARED v[\d.]+", "SHARED ‹label›", texte)


def nature_du_skill(racine: Path, nom: str) -> dict:
    """Détecte la nature de l'élément ciblé — le protocole s'adapte à ce qui existe."""
    d = racine / "skills" / nom
    sk = d / "SKILL.md"
    if not sk.is_file():
        raise SystemExit(f"ABANDON : skills/{nom}/SKILL.md introuvable")
    lignes = sk.read_text(encoding="utf-8").splitlines()
    fm_fin = 0
    vues = 0
    for i, l in enumerate(lignes):
        if l.strip() == "---":
            vues += 1
            if vues == 2:
                fm_fin = i + 1
                break
    texte = "\n".join(lignes)
    a_section_a = any(l.startswith("## §A") for l in lignes)
    a_zero = any(l.startswith("## §0") for l in lignes)
    m_read = re.search(r"^read_when:.*?(?=^\S)", texte, re.S | re.M)
    read_when = m_read.group(0) if m_read else ""
    version = next((l.split(":", 1)[1].strip() for l in lignes if l.startswith("version:")), "?")
    description = "\n".join(lignes[1:fm_fin]) if fm_fin else ""
    kb = racine / "skills" / "KNOWLEDGE.md"
    kb_v = None
    if kb.is_file():
        m = re.search(r"^## " + re.escape(nom) + r" v([\d.]+)", kb.read_text(encoding="utf-8"), re.M)
        kb_v = m.group(1) if m else None
    eco = False
    integ = racine / "scripts" / "check-ecosysteme-integrity.py"
    if integ.is_file():
        eco = f'"{nom}"' in integ.read_text(encoding="utf-8")
    return {
        "repertoire": str(d), "version": version, "octets": len(texte.encode("utf-8")),
        "lignes": len(lignes), "a_section_A": a_section_a, "a_section_0": a_zero,
        "a_read_when": bool(read_when),
        "evals": {p.name: p.stat().st_size for p in sorted((d / "evals").glob("*.json"))} if (d / "evals").is_dir() else {},
        "references": sorted(p.name for p in (d / "references").glob("*") if p.is_file()) if (d / "references").is_dir() else [],
        "scripts": sorted(p.name for p in (d / "scripts").glob("*.py")) if (d / "scripts").is_dir() else [],
        "gouvernance": {"kb": kb_v, "eco_skills": eco},
        "_fragments": {"description": description, "read_when": read_when, "lignes": lignes, "fm_fin": fm_fin},
    }


def bloc_entre(lignes: list[str], debut: str, fin: str) -> str | None:
    i0 = next((i for i, l in enumerate(lignes) if l.startswith(debut)), None)
    if i0 is None:
        return None
    i1 = next((i for i in range(i0, len(lignes)) if lignes[i].startswith(fin)), None)
    return "\n".join(lignes[i0:i1 if i1 is not None else len(lignes)])


def mesurer_sections(lignes: list[str], fm_fin: int) -> list[dict]:
    bornes = [(0, "(frontmatter)")]
    bornes += [(i, re.sub(r"^#{2,3}\s+", "", l)[:70]) for i, l in enumerate(lignes)
               if re.match(r"^#{2,3} ", l) and i >= fm_fin]
    secs = []
    for k, (i, titre) in enumerate(bornes):
        j = bornes[k + 1][0] if k + 1 < len(bornes) else len(lignes)
        # octets réels de la section : join + le saut de ligne de clôture (chaque ligne
        # du fichier porte son \n — la somme des sections == taille du fichier)
        secs.append({"section": titre,
                     "octets": len("\n".join(lignes[i:j]).encode("utf-8")) + 1})
    return secs


def capturer(nom: str) -> dict:
    n = nature_du_skill(RACINE, nom)
    lignes = n["_fragments"]["lignes"]
    fm = n["_fragments"]["fm_fin"]
    contrats = {}
    if n["a_section_A"]:
        contrats["section_A"] = sha(bloc_entre(lignes, "## §A", "## §0") or
                                    bloc_entre(lignes, "## §A", "## §B") or
                                    bloc_entre(lignes, "## §A", "## 1") or "")
    if n["a_section_0"]:
        b0 = bloc_entre(lignes, "## §0", "## §1")
        if b0:
            contrats["section_0_normalisee"] = sha(normalise_shared(b0))
    if n["a_read_when"]:
        contrats["read_when"] = sha(n["_fragments"]["read_when"])
    for f in n["evals"]:
        contrats[f"evals/{f}"] = sha((RACINE / "skills" / nom / "evals" / f).read_text(encoding="utf-8"))
    contrats["description_frontmatter"] = sha(n["_fragments"]["description"])  # TRACÉE (étendable par conception)
    sections = mesurer_sections(lignes, fm)
    return {
        "skill": nom, "genere_par": "skills/re-curation/scripts/protocole-test.py v1.0.0",
        "nature": {k: v for k, v in n.items() if k != "_fragments"},
        "protocole": {
            "tests_pre": ["contrats verbatim (§A / §0 normalisé / read_when / evals) → sha256 baseline",
                          "sections mesurées (poids par section)",
                          "poids global (octets / Kio / #token estimés = caractères ÷ 4)"],
            "tests_post": ["contrats == baseline (COHÉRENT)",
                           "pointeurs references/ valides + non-duplication 1024 o (FONCTIONNEL)",
                           "poids réduit ou sous seuil LOURD (OPTIMISÉ)"],
        },
        "baseline": {"octets": n["octets"], "contrats": contrats,
                     "sections": sections, "kio": round(n["octets"] / 1024, 1),
                     "token_estimes": n["octets"] // 4},
    }


def cmd_pre(nom: str) -> int:
    sortie = RACINE / "download" / f"protocole-test-{nom}.json"
    try:
        donnees = capturer(nom)
    except SystemExit as e:
        print(f"NO-GO : {e}")
        return 1
    donnees["verdict_pre"] = "GO" if donnees["baseline"]["contrats"] else "NO-GO"
    donnees["verdict_pre_detail"] = ("baseline golden master capturée — %d contrats, %d sections, %.1f Kio"
                                     % (len(donnees["baseline"]["contrats"]),
                                        len(donnees["baseline"]["sections"]),
                                        donnees["baseline"]["kio"])) if donnees["verdict_pre"] == "GO" \
        else "aucun contrat lisible — élément non éligible"
    sortie.write_text(json.dumps(donnees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"PROTOCOLE GÉNÉRÉ + PRE EXÉCUTÉ → {sortie}")
    print(f"  nature : version {donnees['nature']['version']} · §A={donnees['nature']['a_section_A']} · "
          f"read_when={donnees['nature']['a_read_when']} · evals={len(donnees['nature']['evals'])} · "
          f"gouvernance KB={donnees['nature']['gouvernance']['kb']} / ECO_SKILLS={donnees['nature']['gouvernance']['eco_skills']}")
    print(f"  baseline : {donnees['baseline']['kio']} Kio ≈ {donnees['baseline']['token_estimes']} #token · "
          f"{len(donnees['baseline']['sections'])} sections · {len(donnees['baseline']['contrats'])} contrats sha256")
    print(f"VERDICT PRE : {donnees['verdict_pre']} — {donnees['verdict_pre_detail']}")
    return 0 if donnees["verdict_pre"] == "GO" else 1


def pointeurs_valides(nom: str) -> tuple[bool, list[str]]:
    d = RACINE / "skills" / nom
    texte = (d / "SKILL.md").read_text(encoding="utf-8")
    manquants = []
    for m in set(re.findall(r"references/([A-Za-z0-9_.-]+)", texte)):
        if not (d / "references" / m).is_file():
            manquants.append(m)
    return (not manquants, manquants)


def non_duplication(nom: str) -> tuple[bool, list[str]]:
    d = RACINE / "skills" / nom
    sk = (d / "SKILL.md").read_text(encoding="utf-8")
    sk_b = sk.encode("utf-8")
    ecarts = []
    if not (d / "references").is_dir():
        return True, []
    for rf in sorted((d / "references").glob("*")):
        if not rf.is_file():
            continue
        rb = rf.read_text(encoding="utf-8").encode("utf-8")
        for i in range(0, max(0, len(rb) - 1024 + 1), 512):
            if rb[i:i + 1024] in sk_b:
                ecarts.append(f"{rf.name}@{i}")
                break
    return (not ecarts, ecarts)


def cmd_post(nom: str) -> int:
    fichier = RACINE / "download" / f"protocole-test-{nom}.json"
    if not fichier.is_file():
        print(f"ABANDON : protocole PRE introuvable ({fichier}) — exécuter --pre {nom} AVANT la re-curation")
        return 2
    base = json.loads(fichier.read_text(encoding="utf-8"))
    actuel = capturer(nom)
    resultats, coherent = {}, True
    for cle, sha_base in base["baseline"]["contrats"].items():
        sha_now = actuel["baseline"]["contrats"].get(cle)
        ok = sha_now == sha_base
        if cle == "description_frontmatter" and not ok:
            resultats[cle] = "TRACÉE-ÉTENDUE (par conception — résumés/mention ajoutables)"  # non bloquant, journalisé
        else:
            resultats[cle] = "PASS" if ok else "FAIL"
            coherent = coherent and ok
    pv, manquants = pointeurs_valides(nom)
    nd, dup = non_duplication(nom)
    fonctionnel = pv and nd
    avant, apres = base["baseline"]["octets"], actuel["baseline"]["octets"]
    reduction = 100 * (1 - apres / avant) if avant else 0
    optimise = apres < avant or apres < SEUIL_LOURD
    verdict = ("MAINTIEN DE L'OPTIMISATION" if (coherent and fonctionnel and optimise)
               else "DÉRIVE")
    actuel["post"] = {
        "comparaison_contrats": resultats, "coherent": coherent,
        "pointeurs_valides": pv, "pointeurs_manquants": manquants,
        "non_duplication": nd, "duplications": dup, "fonctionnel": fonctionnel,
        "poids_avant": avant, "poids_apres": apres, "reduction_pct": round(reduction, 1),
        "optimise": optimise, "verdict_post": verdict,
    }
    fichier.write_text(json.dumps(actuel, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"POST EXÉCUTÉ (protocole {fichier.name}) :")
    for k, v in resultats.items():
        print(f"  contrats {k:<28} {v}")
    print(f"  pointeurs references/ : {'PASS' if pv else 'FAIL ' + str(manquants)} · "
          f"non-duplication : {'PASS' if nd else 'FAIL ' + str(dup)}")
    print(f"  poids : {avant} → {apres} octets ({reduction:.1f} %) — seuil LOURD 30 Kio : "
          f"{'sous' if apres < SEUIL_LOURD else 'au-dessus'}")
    print(f"  COHÉRENT={coherent} · FONCTIONNEL={fonctionnel} · OPTIMISÉ={optimise}")
    print(f"VERDICT POST : {verdict}")
    return 0 if verdict == "MAINTIEN DE L'OPTIMISATION" else 1


def cmd_verifier(nom: str) -> int:
    n = nature_du_skill(RACINE, nom)
    pv, manquants = pointeurs_valides(nom)
    nd, dup = non_duplication(nom)
    verdict_poids = ("OK" if n["octets"] < 12 * 1024 else
                     "INTERMÉDIAIRE" if n["octets"] < SEUIL_LOURD else
                     "LOURD" if n["octets"] < SEUIL_CRITIQUE else "CRITIQUE")
    ok = pv and nd
    print(f"VÉRIFICATION re-curation — skills/{nom} v{n['version']} "
          f"({n['octets']} o / {n['octets']/1024:.1f} Kio / verdict poids {verdict_poids})")
    print(f"  pointeurs references/ ({len(n['references'])} fichiers) : "
          f"{'PASS' if pv else 'FAIL — manquants : ' + ', '.join(manquants)}")
    print(f"  non-duplication 1024 o : {'PASS' if nd else 'FAIL — ' + ', '.join(dup)}")
    print(f"VERDICT : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def cmd_compare(nom: str, methodes: str) -> int:
    n = nature_du_skill(RACINE, nom)
    sections = mesurer_sections(n["_fragments"]["lignes"], n["_fragments"]["fm_fin"])
    mobiles = sum(s["octets"] for s in sections
                  if s["octets"] >= 1500 and s["section"] != "(frontmatter)"
                  and not s["section"].startswith("§A") and not s["section"].startswith("§0"))
    print(f"ARBITRAGE DES MÉTHODES — skills/{nom} ({n['octets']/1024:.1f} Kio, "
          f"sections ≥ 1,5 Kio mobilisables : {mobiles/1024:.1f} Kio)")
    classement = []
    for m in [x.strip() for x in methodes.split(",") if x.strip()]:
        reg = METHODES.get(m)
        if reg is None:
            print(f"  {m:<32} MÉTHODE INCONNUE (registre : {', '.join(METHODES)})")
            continue
        gain = int(mobiles * reg["taux_gain"])
        proj = n["octets"] - gain
        eligible = reg["r4"]
        print(f"  {m:<32} gain projeté {gain/1024:>5.1f} Kio → {proj/1024:>5.1f} Kio · "
              f"R4 {'✓' if eligible else '✗ DISQUALIFIÉE'} · {reg['note']}")
        if eligible:
            classement.append((proj, m))
    if not classement:
        print("VERDICT : aucune méthode éligible")
        return 1
    classement.sort()
    meilleure = classement[0]
    print(f"VERDICT : la plus optimisée et performante (R4-compliantes) = {meilleure[1]} "
          f"(projection {meilleure[0]/1024:.1f} Kio)")
    return 0


def selftest() -> int:
    """Bac à sable : PRE→GO, POST identité, contrat altéré→DÉRIVE, compare, pointeur manquant."""
    tmp = Path(tempfile.mkdtemp(prefix="recuration-selftest-"))
    global RACINE
    racine_sauve = RACINE
    try:
        (tmp / "skills" / "temoin" / "evals").mkdir(parents=True)
        (tmp / "skills" / "temoin" / "references").mkdir(parents=True)
        (tmp / "download").mkdir()
        sk = tmp / "skills" / "temoin" / "SKILL.md"
        sk.write_text("""---
name: temoin
version: 1.0.0
read_when:
  - Déclencher pour tester
---
## §A — DÉCLENCHEURS

- `temoin` — test

## §0 — Contexte Système (SHARED v1.7.34)

Bloc zéro.

## §1 — Corps

### §1.1 Grosse section déplaçable

""" + ("Ligne de contenu mesurable. " * 120) + """

### §1.2 Résumé

Fin.
""", encoding="utf-8")
        (tmp / "skills" / "temoin" / "evals" / "evals.json").write_text('{"skill_name": "temoin"}', encoding="utf-8")
        RACINE = tmp
        r = []

        rc = cmd_pre("temoin")
        j1 = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("PRE → GO (rc=0, verdict GO)", rc == 0 and j1["verdict_pre"] == "GO"))

        rc2 = cmd_post("temoin")
        j2 = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("POST identité → contrats PASS + cohérent + fonctionnel",
                  rc2 == 0 and j2["post"]["coherent"] and j2["post"]["fonctionnel"]
                  and j2["post"]["verdict_post"] == "MAINTIEN DE L'OPTIMISATION"))

        t = sk.read_text(encoding="utf-8").replace("- `temoin` — test", "- `temoin` — ALTÉRÉ")
        sk.write_text(t, encoding="utf-8")
        rc3 = cmd_post("temoin")
        j3 = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("contrat §A altéré → COHÉRENT=False + DÉRIVE + rc=1",
                  (not j3["post"]["coherent"]) and j3["post"]["verdict_post"] == "DÉRIVE" and rc3 == 1))

        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc4 = cmd_compare("temoin", "moves-r4-resumes,suppression")
        r.append(("compare → moves-r4-resumes gagnante, suppression disqualifiée (rc=0)",
                  rc4 == 0 and "moves-r4-resumes" in buf.getvalue()
                  and "DISQUALIFIÉE" in buf.getvalue()))

        sk.write_text(sk.read_text(encoding="utf-8") + "\nVoir `references/absent.md`.\n", encoding="utf-8")
        rc5 = cmd_verifier("temoin")
        r.append(("pointeur manquant → verifier rc=1", rc5 == 1))

        print("\n=== SELFTEST protocole-test.py ===")
        ok = True
        for label, passe in r:
            print(f"  [{'PASS' if passe else 'FAIL'}] {label}")
            ok = ok and passe
        print(f"SELFTEST : {'PASS' if ok else 'FAIL'} ({sum(1 for _, p in r if p)}/{len(r)})")
        return 0 if ok else 1
    finally:
        RACINE = racine_sauve
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    p = argparse.ArgumentParser(description="protocole-test.py — skill re-curation v1.0.0")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--pre", metavar="SKILL")
    g.add_argument("--post", metavar="SKILL")
    g.add_argument("--verifier", metavar="SKILL")
    g.add_argument("--compare", metavar="SKILL")
    g.add_argument("--selftest", action="store_true")
    p.add_argument("--methodes", default="moves-r4-resumes,moves-r4-pur,append-references-existantes,suppression")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if a.pre:
        return cmd_pre(a.pre)
    if a.post:
        return cmd_post(a.post)
    if a.verifier:
        return cmd_verifier(a.verifier)
    return cmd_compare(a.compare, a.methodes)


if __name__ == "__main__":
    sys.exit(main())
