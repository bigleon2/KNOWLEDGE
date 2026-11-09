#!/usr/bin/env python3
"""protocole-test.py — Script PRINCIPAL du skill re-curation (v1.2.2).

Implémentation de la directive propriétaire (Task 72, directive complémentaire
1a1b7b297b7b4975) : « le skill "re-curation" devra être implémenté d'un script dont
l'objectif est de s'assurer $FACON [de façon cohérente, optimisée et fonctionnelle]
du maintien de l'optimisation du fonctionnement de mon écosystème pour qu'il soit
$FACON2 [(cohérent, optimisé et fonctionnel)] en faisant des tests $FACON2 (génère
un protocole de test adapté à mon écosystème) AVANT d'effectuer les "re-curation
progressive disclosure" sur les éléments de mon écosystème pour trouver la méthode
la plus optimisée et performante. »

Suite de tests v1.2.0 (directive propriétaire 2026-11-09, trace 1a1bcb98c022bfe9) :
« avant d'appliquer la re-curation progressive disclosure à l'élément ciblé,
fais-lui passer des tests fonctionnels et de performance. Ces tests doivent
impérativement inclure la validation de toutes les interactions de l'élément ciblé
avec les autres composants auxquels il est lié. Effectue ces tests rigoureusement
avant et après la re-curation progressive disclosure […] Intégrer cette suite de
tests au sein de mon skill "re-curation". » — TROIS familles intégrées aux phases
PRE et POST :

  F1 FONCTIONNELS   l'élément S'EXÉCUTE : chaque script portant un --selftest est
                    exécuté pour de vrai (subprocess, timeout, rc + durée capturés) ;
                    les scripts sans selftest sont compilés (compile, zéro écriture) ;
                    evals validés (JSON) ; structure frontmatter minimale — la famille
                    s'adapte à la nature (un élément sans scripts est testé sur sa
                    structure + evals).
  F2 PERFORMANCE    métriques MESURÉES (règle d'or n°5) : poids de chargement
                    (octets / Kio / #token — le goulot réel est le budget #token,
                    étude Task 70) + durée d'exécution mesurée des tests
                    fonctionnels ; stabilité PRE/POST via perf_stable (tolérance
                    ×1.5 + 0.5 s — bruit de mesure absorbé).
  F3 INTERACTIONS   TOUTES les interactions de l'élément avec ses composants liés :
                    dépendances YAML sortantes (existence + contrat semver —
                    cible plateforme sans version : NON-VERSIONNÉ tracé, non-bloquant) ·
                    dépendances entrantes (scan du registre KB — chaque dépendant,
                    contrat satisfait) · alignement entrée KB ↔ version frontmatter ·
                    pin ECO_SKILLS (arbitre check-ecosysteme-integrity.py) · corpus
                    PM si famille (sinon nature non-famille documentée) · agents
                    .agent mentionnant l'élément — empreinte sha256 de l'ensemble.

Mécanique (méthode P0/P2/P5/P7 du SKILL.md — tests AVANT re-curation) :

  --pre <skill>        GÉNÈRE le protocole de test ADAPTÉ à l'élément ciblé (nature :
                       contrats triggers verbatim §A, read_when, evals, description,
                       sections, poids, gouvernance KB/ECO_SKILLS) puis l'EXÉCUTE en
                       phase PRE : baseline golden master (contrats sha256 + 3
                       familles) → verdict GO / NO-GO — GO exige contrats lisibles ET
                       fonctionnels PASS ET interactions SAINES (jamais de re-curation
                       d'un élément déjà cassé). Sortie : download/protocole-test-<skill>.json
  --post <skill>       Ré-exécute le protocole en phase POST (après re-curation) sur
                       5 dimensions : contrats == baseline (COHÉRENT) + pointeurs et
                       non-duplication et selftests (FONCTIONNEL) + poids réduit ou
                       sous seuil LOURD (OPTIMISÉ) + interactions SAINES + performance
                       stable → verdict MAINTIEN DE L'OPTIMISATION / DÉRIVE.
  --verifier <skill>   Mode VÉRIFICATION d'une re-curation DÉJÀ exécutée (pointeurs
                       references/ valides, non-duplication 1024 o, seuils + les 3
                       familles en direct) — sans exiger de protocole PRE antérieur.
  --compare <skill> --methodes <m1,m2,…>
                       Arbitrage des méthodes candidates : gains projetés calculés
                       des sections MESURÉES (jamais inventés) + conformité R4 →
                       la plus optimisée et performante (R4-compliantes seules
                       éligibles).
  --selftest           Auto-vérification en bac à sable (sait échouer) — 13 cas.

Gardes : Python stdlib (N3) · étiquette SHARED du §0 normalisée à la comparaison
(leçon harnais v2 Task 72 — un bump SHARED écosystème n'est pas une dérive de
contrat) · dates de directives du socle normalisées (leçon harnais v3 — directive
propriétaire 2026-11-09, pendance consignée au commit Task 79 0b1712b : une date
de directive propriétaire enrichie au bloc socle n'est pas une dérive de contrat)
· contrat §0 borné au BLOC SOCLE (premier titre markdown suivant — la borne naïve
« ## §1 » capturait le corps entier quand le skill n'a pas de section §1 : 23,4
Kio sur version-management, 16,7 Kio sur ASR — et une re-curation légitime du
corps était vue comme DÉRIVE fausse) · phases de comparaison en lecture seule ·
le script n'invente jamais de contenu (KO-L003) : il mesure, compare et rend un
verdict mécanique.

Convention de mesure §0 v3 (v1.1.0) : les baselines capturées par les versions
antérieures à v1.1.0 (périmètre de contrat §0 différent) ne sont plus comparables
— re-capturer la baseline (--pre) avant tout POST postérieur au correctif.
Convention familles v1.2.0 : les baselines antérieures à v1.2.0 (sans clé
baseline.tests) ne portent pas les 3 familles — un --post sur telle baseline est
refusé (rc=2) avec demande de re-capture.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RACINE = Path("/home/z/my-project")
SEUIL_LOURD = 30 * 1024   # seuils de l'arbitre poids-chargement.py (v1.0.0)
SEUIL_CRITIQUE = 60 * 1024
TOL_PERF = 1.5            # famille PERFORMANCE (v1.2.0) : tolérance de stabilité
MARGE_PERF = 0.5          # durée POST ≤ durée PRE × TOL_PERF + MARGE_PERF (secondes)
TIMEOUT_SELFTEST = 60     # famille FONCTIONNELS (v1.2.0) : borne par script exécuté
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
    """Étiquettes vives du socle normalisées (harnais v2 : étiquette SHARED ;
    harnais v3 : dates de directives du socle — bump écosystème ≠ dérive de contrat)."""
    texte = re.sub(r"SHARED v[\d.]+", "SHARED ‹label›", texte)
    return re.sub(r"\d{4}-\d{2}-\d{2}", "‹date›", texte)


def bloc_socle(lignes: list[str]) -> str | None:
    """Bloc Contexte Système du socle, borné au premier titre markdown suivant
    (harnais v3 — la borne naïve « ## §1 » étendait le contrat §0 au corps entier
    quand le skill n'a pas de section §1 ; le bloc socle réel fait ~1,6 Kio)."""
    i0 = next((i for i, l in enumerate(lignes) if l.startswith("## §0")), None)
    if i0 is None:
        return None
    i1 = next((i for i in range(i0 + 1, len(lignes)) if lignes[i].startswith("#")),
              len(lignes))
    return "\n".join(lignes[i0:i1])


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
    # Convention de mesure (note croisée Task 76 D010 — différés Task 75 §6.4) :
    # « texte » reconstitué par join(splitlines()) vaut la taille disque MOINS 1 o
    # (saut de ligne final non reconstitué — ex. gen-plan : 30 667 o ici vs 30 668 o
    # disque [task72-baseline-verifier.py / st_size]) ; chaque mesureur est
    # self-consistant — comparer chaque outil à sa propre convention, jamais l'un
    # à l'autre sans cette clé de lecture.
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


# ---------------------------------------------------------------------------
# Suite de tests v1.2.0 (directive 2026-11-09, trace 1a1bcb98c022bfe9) — 3 familles
# ---------------------------------------------------------------------------

def _vtuple(v: str | None) -> tuple:
    return tuple(int(x) for x in v.split(".")) if v else (0, 0, 0)


def _version_frontmatter(texte: str) -> str | None:
    """Version semver déclarée au frontmatter d'un SKILL.md (None si absente)."""
    tete = texte.split("---")[1] if texte.count("---") >= 2 else ""
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", tete, re.M)
    return m.group(1) if m else None


def _deps_frontmatter(texte: str) -> list[tuple[str, str]]:
    """[(skill, version_min)] du bloc dependencies: multi-lignes — même convention
    de lecture que l'arbitre global test-coherence-interactions.py ; la présente est
    la vue SCOPÉE par élément (baseline + comparaison PRE/POST), complémentaire."""
    deps: list[tuple[str, str]] = []
    tete = texte.split("---")[1] if texte.count("---") >= 2 else ""
    m = re.search(r"dependencies:\s*\n((?:[ \t]+[^\n]*\n?)+)", tete)
    if not m:
        return deps
    cur = None
    for line in m.group(1).splitlines():
        sm = re.search(r"skill:\s*([a-z0-9-]+)", line)
        if sm:
            cur = sm.group(1)
            continue
        vm = re.search(r"version:\s*\"?>?=?\s*([\d.]+)", line)
        if vm and cur:
            deps.append((cur, vm.group(1)))
            cur = None
    return deps


def tests_fonctionnels(nom: str) -> dict:
    """Famille F1 — tests FONCTIONNELS (directive 2026-11-09) : l'élément S'EXÉCUTE.
    Chaque script portant un --selftest est exécuté pour de vrai (subprocess, timeout
    TIMEOUT_SELFTEST, rc + durée capturés) ; les scripts sans selftest sont compilés
    (compile() en mémoire — zéro écriture disque) ; les evals sont validés (JSON
    non vide) ; la structure frontmatter minimale est vérifiée. Nature-adapté : un
    élément sans scripts est testé sur evals + structure."""
    d = RACINE / "skills" / nom
    scripts: dict = {}
    if (d / "scripts").is_dir():
        for sp in sorted((d / "scripts").glob("*.py")):
            src = sp.read_text(encoding="utf-8", errors="replace")
            if "--selftest" in src:
                t0 = time.monotonic()
                try:
                    r = subprocess.run([sys.executable, str(sp), "--selftest"],
                                       capture_output=True, text=True,
                                       timeout=TIMEOUT_SELFTEST, cwd=str(RACINE))
                    scripts[sp.name] = {
                        "test": "selftest exécuté", "rc": r.returncode,
                        "duree_s": round(time.monotonic() - t0, 3),
                        "verdict": "PASS" if r.returncode == 0 else "FAIL",
                        **({"detail": (r.stdout + r.stderr).strip()[-200:]}
                           if r.returncode != 0 else {}),
                    }
                except subprocess.TimeoutExpired:
                    scripts[sp.name] = {"test": "selftest exécuté", "rc": None,
                                        "duree_s": TIMEOUT_SELFTEST, "verdict": "FAIL",
                                        "detail": f"timeout {TIMEOUT_SELFTEST} s"}
            else:
                try:
                    compile(src, str(sp), "exec")
                    scripts[sp.name] = {"test": "compilation (sans selftest)", "verdict": "PASS"}
                except SyntaxError as e:
                    scripts[sp.name] = {"test": "compilation (sans selftest)",
                                        "verdict": "FAIL", "detail": str(e)}
    evals: dict = {}
    if (d / "evals").is_dir():
        for ev in sorted((d / "evals").glob("*.json")):
            try:
                j = json.loads(ev.read_text(encoding="utf-8"))
                # schéma skill-creator : evals.json = OBJET, trigger_evals.json =
                # LISTE de cas (Description Optimization) — tout JSON valide non vide
                # est PASS (correctif v1.2.0 : l'exigence d'objet était un faux positif)
                evals[ev.name] = {"verdict": "PASS" if j else "FAIL",
                                  **({} if j else {"detail": "JSON vide"})}
            except (json.JSONDecodeError, OSError) as e:
                evals[ev.name] = {"verdict": "FAIL", "detail": str(e)[:200]}
    sk = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    tete = sk.split("---")[1] if sk.count("---") >= 2 else ""
    structure = {"champs": {c: bool(re.search(rf"^{c}:", tete, re.M))
                            for c in ("name", "version", "description")}}
    structure["verdict"] = "PASS" if all(structure["champs"].values()) else "FAIL"
    verdict = ("PASS" if all(v["verdict"] == "PASS" for v in scripts.values())
               and all(v["verdict"] == "PASS" for v in evals.values())
               and structure["verdict"] == "PASS" else "FAIL")
    duree = round(sum(v.get("duree_s", 0.0) for v in scripts.values()), 3)
    return {"scripts": scripts, "evals": evals, "structure": structure,
            "duree_totale_s": duree, "verdict": verdict}


def perf_stable(duree_base, duree_post) -> bool:
    """Famille F2 — tolérance de stabilité performance : la durée POST doit rester
    sous durée PRE × TOL_PERF + MARGE_PERF (bruit de mesure absorbé — démarrage
    Python, charge machine). None (élément sans selftest) = non applicable,
    non-bloquant : True."""
    if duree_base is None or duree_post is None:
        return True
    return duree_post <= duree_base * TOL_PERF + MARGE_PERF


def tests_performance(n: dict, fonc: dict) -> dict:
    """Famille F2 — PERFORMANCE MESURÉE (règle d'or n°5) : poids de chargement
    (octets / Kio / #token — le goulot réel est le budget #token, étude Task 70) +
    durée d'exécution MESURÉE des tests fonctionnels. La stabilité PRE/POST se
    juge en phase POST via perf_stable (tolérance documentée dans le JSON)."""
    return {
        "poids": {"octets": n["octets"], "kio": round(n["octets"] / 1024, 1),
                  "token_estimes": n["octets"] // 4},
        "duree_tests_fonctionnels_s": fonc["duree_totale_s"],
        "tolerance_stabilite": f"×{TOL_PERF} + {MARGE_PERF} s",
        "verdict": "MESURÉ",
    }


def interactions(nom: str) -> dict:
    """Famille F3 — TOUTES les interactions de l'élément ciblé avec les composants
    auxquels il est lié (directive 2026-11-09) : dépendances YAML sortantes
    (existence + contrat semver), dépendances ENTRANTES (scan du registre KB),
    alignement entrée KB ↔ frontmatter, pin ECO_SKILLS (arbitre integrity), corpus
    PM (si famille), agents .agent mentionnant l'élément — empreinte sha256 de
    l'ensemble normalisé (capturée en baseline, comparée en POST)."""
    sk_texte = (RACINE / "skills" / nom / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    v_el = _version_frontmatter(sk_texte)
    # — sortantes : les dépendances que l'élément déclare
    sortantes = []
    for cible, vmin in _deps_frontmatter(sk_texte):
        p = RACINE / "skills" / cible / "SKILL.md"
        if not p.is_file():
            sortantes.append({"skill": cible, "contrat": f">={vmin}",
                              "verdict": "FAIL", "detail": "cible absente"})
        else:
            v_c = _version_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            if v_c is None:
                # cible existante SANS version déclarée (skill plateforme — hors
                # convention semver SHARED §1.3, ex. image-edit) : l'arête EXISTE,
                # le contrat semver est invérifiable mécaniquement → NON-VERSIONNÉ,
                # tracé non-bloquant (correctif v1.2.0 : FAIL était un faux positif)
                sortantes.append({"skill": cible, "contrat": f">={vmin}", "version": None,
                                  "verdict": "NON-VERSIONNÉ",
                                  "detail": "cible sans version déclarée (nature plateforme) — contrat semver non vérifiable"})
            else:
                sortantes.append({"skill": cible, "contrat": f">={vmin}", "version": v_c,
                                  "verdict": "PASS" if _vtuple(v_c) >= _vtuple(vmin) else "FAIL"})
    # — entrantes : les éléments du registre KB qui dépendent de l'élément ciblé
    kb_path = RACINE / "skills" / "KNOWLEDGE.md"
    kb_texte = kb_path.read_text(encoding="utf-8") if kb_path.is_file() else ""
    membres = re.findall(r"^## ([\w-]+) v[\d.]+$", kb_texte, re.M)
    entrantes = []
    for autre in membres:
        if autre == nom:
            continue
        p = RACINE / "skills" / autre / "SKILL.md"
        if not p.is_file():
            continue
        for cible, vmin in _deps_frontmatter(p.read_text(encoding="utf-8", errors="replace")):
            if cible == nom:
                entrantes.append({"skill": autre, "contrat": f">={vmin}",
                                  "verdict": "PASS" if v_el and _vtuple(v_el) >= _vtuple(vmin) else "FAIL"})
    # — registre KB : entrée versionnée alignée sur le frontmatter
    m = re.search(r"^## " + re.escape(nom) + r" v([\d.]+)", kb_texte, re.M)
    kb = {"entree": m.group(1) if m else None,
          "verdict": "PASS" if (m and v_el and m.group(1) == v_el) else "FAIL",
          **({} if m else {"detail": "entrée KB absente"})}
    # — pin ECO_SKILLS (arbitre check-ecosysteme-integrity.py — KO-L004)
    integ = RACINE / "scripts" / "check-ecosysteme-integrity.py"
    if integ.is_file():
        it = integ.read_text(encoding="utf-8", errors="replace")
        if f'"{nom}"' in it:
            em = re.search(r'"' + re.escape(nom) + r'":\s*"([\d.]+)"', it)
            eco = {"pin": em.group(1) if em else None,
                   "verdict": "PASS" if (em and v_el and em.group(1) == v_el) else "FAIL"}
        else:
            eco = {"pin": None, "verdict": "PASS", "detail": "hors ECO_SKILLS — nature"}
    else:
        eco = {"pin": None, "verdict": "PASS", "detail": "arbitre integrity absent (environnement réduit)"}
    # — corpus PM (famille des prompts maîtres — KO-L004)
    pms = sorted((RACINE / "skills" / "@mon-ecosysteme").glob(
        f"PROMPT-MAITRE-{nom.upper()}-v*.md")) if (RACINE / "skills" / "@mon-ecosysteme").is_dir() else []
    if pms:
        mpm = re.search(r"-v([\d.]+)\.md$", pms[-1].name)
        pm = {"famille": True, "pm": pms[-1].name,
              "verdict": "PASS" if (mpm and v_el and mpm.group(1) == v_el) else "FAIL"}
    else:
        pm = {"famille": False, "verdict": "PASS", "detail": "hors famille PM — nature"}
    # — agents .agent mentionnant l'élément
    agents = sorted(str(a.relative_to(RACINE)) for a in (RACINE / "skills").rglob("*.agent")
                    if re.search(r"\b" + re.escape(nom) + r"\b",
                                 a.read_text(encoding="utf-8", errors="replace")))
    sous = {"sortantes": sortantes, "entrantes": entrantes, "kb": kb,
            "eco_skills": eco, "pm_corpus": pm, "agents": agents}
    empreinte = sha(json.dumps(sous, sort_keys=True, ensure_ascii=False))
    verdict = ("SAINES" if all(x["verdict"] in ("PASS", "NON-VERSIONNÉ") for x in sortantes)
               and all(x["verdict"] == "PASS" for x in entrantes)
               and kb["verdict"] == "PASS" and eco["verdict"] == "PASS"
               and pm["verdict"] == "PASS" else "CASSÉES")
    return {**sous, "empreinte": empreinte, "verdict": verdict}


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
        b0 = bloc_socle(lignes)
        if b0:
            contrats["section_0_normalisee"] = sha(normalise_shared(b0))
    if n["a_read_when"]:
        contrats["read_when"] = sha(n["_fragments"]["read_when"])
    for f in n["evals"]:
        contrats[f"evals/{f}"] = sha((RACINE / "skills" / nom / "evals" / f).read_text(encoding="utf-8"))
    contrats["description_frontmatter"] = sha(n["_fragments"]["description"])  # TRACÉE (étendable par conception)
    sections = mesurer_sections(lignes, fm)
    fonc = tests_fonctionnels(nom)
    perf = tests_performance(n, fonc)
    inter = interactions(nom)
    nb_self = sum(1 for v in fonc["scripts"].values() if v["test"] == "selftest exécuté")
    nb_comp = sum(1 for v in fonc["scripts"].values() if v["test"] == "compilation (sans selftest)")
    return {
        "skill": nom, "genere_par": "skills/re-curation/scripts/protocole-test.py v1.2.2",
        "nature": {k: v for k, v in n.items() if k != "_fragments"},
        "protocole": {
            "tests_pre": ["contrats verbatim (§A / §0 normalisé / read_when / evals) → sha256 baseline",
                          "sections mesurées (poids par section)",
                          "poids global (octets / Kio / #token estimés = caractères ÷ 4)",
                          f"F1 fonctionnels — {nb_self} selftests exécutés + {nb_comp} compilés · "
                          f"evals {len(n['evals'])} · structure frontmatter",
                          "F2 performance — poids #token + durée mesurée des selftests "
                          f"(tolérance ×{TOL_PERF} + {MARGE_PERF} s)",
                          "F3 interactions — sortantes/entrantes semver · KB · ECO_SKILLS · "
                          "corpus PM · agents → empreinte sha256"],
            "tests_post": ["contrats == baseline (COHÉRENT)",
                           "pointeurs references/ valides + non-duplication 1024 o + selftests (FONCTIONNEL)",
                           "poids réduit ou sous seuil LOURD (OPTIMISÉ)",
                           "F3 interactions SAINES (empreinte comparée)",
                           f"F2 performance stable (tolérance ×{TOL_PERF} + {MARGE_PERF} s)"],
        },
        "baseline": {"octets": n["octets"], "contrats": contrats,
                     "sections": sections, "kio": round(n["octets"] / 1024, 1),
                     "token_estimes": n["octets"] // 4,
                     "tests": {"fonctionnels": fonc, "performance": perf,
                               "interactions": inter}},
    }


def cmd_pre(nom: str) -> int:
    sortie = RACINE / "download" / f"protocole-test-{nom}.json"
    try:
        donnees = capturer(nom)
    except SystemExit as e:
        print(f"NO-GO : {e}")
        return 1
    fonc = donnees["baseline"]["tests"]["fonctionnels"]
    inter = donnees["baseline"]["tests"]["interactions"]
    eligibles = bool(donnees["baseline"]["contrats"])
    donnees["verdict_pre"] = ("GO" if eligibles and fonc["verdict"] == "PASS"
                              and inter["verdict"] == "SAINES" else "NO-GO")
    if donnees["verdict_pre"] == "GO":
        donnees["verdict_pre_detail"] = (
            "baseline golden master capturée — %d contrats, %d sections, %.1f Kio · "
            "3 familles : fonctionnels PASS · interactions SAINES · performance mesurée"
            % (len(donnees["baseline"]["contrats"]), len(donnees["baseline"]["sections"]),
               donnees["baseline"]["kio"]))
    else:
        causes = []
        if not eligibles:
            causes.append("aucun contrat lisible — élément non éligible")
        if fonc["verdict"] != "PASS":
            causes.append("F1 fonctionnels FAIL — l'élément est déjà cassé "
                          "(selftests/evals/structure) : la re-curation ne démarre PAS")
        if inter["verdict"] != "SAINES":
            causes.append("F3 interactions CASSÉES — arêtes défectueuses : "
                          "la re-curation ne démarre PAS")
        donnees["verdict_pre_detail"] = " ; ".join(causes)
    sortie.write_text(json.dumps(donnees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"PROTOCOLE GÉNÉRÉ + PRE EXÉCUTÉ → {sortie}")
    print(f"  nature : version {donnees['nature']['version']} · §A={donnees['nature']['a_section_A']} · "
          f"read_when={donnees['nature']['a_read_when']} · evals={len(donnees['nature']['evals'])} · "
          f"gouvernance KB={donnees['nature']['gouvernance']['kb']} / ECO_SKILLS={donnees['nature']['gouvernance']['eco_skills']}")
    print(f"  baseline : {donnees['baseline']['kio']} Kio ≈ {donnees['baseline']['token_estimes']} #token · "
          f"{len(donnees['baseline']['sections'])} sections · {len(donnees['baseline']['contrats'])} contrats sha256")
    fscripts = fonc["scripts"]
    nbs = sum(1 for v in fscripts.values() if v["test"] == "selftest exécuté")
    nbc = sum(1 for v in fscripts.values() if v["test"] == "compilation (sans selftest)")
    print(f"  F1 fonctionnels : {nbs} selftests exécutés + {nbc} compilés · evals {len(fonc['evals'])} · "
          f"structure → {fonc['verdict']}")
    print(f"  F2 performance : {donnees['baseline']['kio']} Kio ≈ {donnees['baseline']['token_estimes']} #token · "
          f"durée selftests {fonc['duree_totale_s']} s (tolérance ×{TOL_PERF} + {MARGE_PERF} s)")
    print(f"  F3 interactions : {len(inter['sortantes'])} sortantes · {len(inter['entrantes'])} entrantes · "
          f"KB={inter['kb']['entree']} · ECO_SKILLS={inter['eco_skills']['pin']} · "
          f"PM={'oui' if inter['pm_corpus']['famille'] else 'non (nature)'} · "
          f"{len(inter['agents'])} agents → {inter['verdict']} ({inter['empreinte'][:12]}…)")
    print(f"VERDICT PRE : {donnees['verdict_pre']} — {donnees['verdict_pre_detail']}")
    return 0 if donnees["verdict_pre"] == "GO" else 1


def pointeurs_valides(nom: str) -> tuple[bool, list[str]]:
    d = RACINE / "skills" / nom
    texte = (d / "SKILL.md").read_text(encoding="utf-8")
    manquants = []
    # v1.2.2 (Task 82 G3, preuves réelles knowledge-observer) : une citation
    # `<autre-skill>/references/<fichier>` est une référence INTER-SKILL
    # (non-duplication SHARED §6.3 — la source de vérité vit dans un autre
    # skill), PAS un pointeur local : le lookbehind exclut tout `references/`
    # précédé d'un caractère de chemin (`/`, lettre, chiffre, `_`, `-`).
    for m in set(re.findall(r"(?<![\w/-])references/([A-Za-z0-9_.-]+)", texte)):
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
    if "tests" not in base.get("baseline", {}):
        print("ABANDON : baseline antérieure à v1.2.0 (sans familles de tests) — "
              "re-capturer la baseline (convention familles v1.2.0) : "
              f"exécuter --pre {nom} puis re-jouer --post")
        return 2
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
    fonc_post = actuel["baseline"]["tests"]["fonctionnels"]
    inter_post = actuel["baseline"]["tests"]["interactions"]
    inter_base = base["baseline"]["tests"]["interactions"]
    interactions_saines = inter_post["verdict"] == "SAINES"
    d_base = base["baseline"]["tests"]["performance"]["duree_tests_fonctionnels_s"]
    d_post = actuel["baseline"]["tests"]["performance"]["duree_tests_fonctionnels_s"]
    stable = perf_stable(d_base, d_post)
    fonctionnel = pv and nd and fonc_post["verdict"] == "PASS"
    avant, apres = base["baseline"]["octets"], actuel["baseline"]["octets"]
    reduction = 100 * (1 - apres / avant) if avant else 0
    # v1.2.1 (KO-L003, Task 81 G2) — idempotence des verdicts POST : quand la baseline
    # a été ancrée par un POST précédent (re-jeu de stabilité), MAINTIEN = NON-RÉGRESSION
    # (apres <= avant) ; au PREMIER POST (baseline PRE fraîche), la réduction stricte
    # (apres < avant) ou le seuil LOURD restent exigés. Avant ce correctif, tout re-jeu
    # sur un état stable LOURD était structurellement DÉRIVE (faille sur preuves réelles
    # iphone19 Task 81 : run 1 MAINTIEN [−27,3 %], run 2 DÉRIVE [0 %] — non idempotent).
    recap_ancree = "post" in base
    optimise = (apres <= avant if recap_ancree else apres < avant) or apres < SEUIL_LOURD
    verdict = ("MAINTIEN DE L'OPTIMISATION" if (coherent and fonctionnel and optimise
                                                and interactions_saines and stable)
               else "DÉRIVE")
    actuel["post"] = {
        "comparaison_contrats": resultats, "coherent": coherent,
        "pointeurs_valides": pv, "pointeurs_manquants": manquants,
        "non_duplication": nd, "duplications": dup,
        "tests_fonctionnels": fonc_post["verdict"], "fonctionnel": fonctionnel,
        "interactions_saines": interactions_saines,
        "empreinte_interactions": {"avant": inter_base["empreinte"],
                                   "apres": inter_post["empreinte"],
                                   "identique": inter_base["empreinte"] == inter_post["empreinte"]},
        "performance": {"duree_avant_s": d_base, "duree_apres_s": d_post,
                        "tolerance": f"×{TOL_PERF} + {MARGE_PERF} s", "stable": stable},
        "poids_avant": avant, "poids_apres": apres, "reduction_pct": round(reduction, 1),
        "optimise": optimise, "verdict_post": verdict,
    }
    fichier.write_text(json.dumps(actuel, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"POST EXÉCUTÉ (protocole {fichier.name}) :")
    for k, v in resultats.items():
        print(f"  contrats {k:<28} {v}")
    print(f"  pointeurs references/ : {'PASS' if pv else 'FAIL ' + str(manquants)} · "
          f"non-duplication : {'PASS' if nd else 'FAIL ' + str(dup)} · "
          f"F1 selftests : {fonc_post['verdict']}")
    print(f"  F3 interactions : {inter_post['verdict']} · empreinte "
          f"{'identique' if inter_base['empreinte'] == inter_post['empreinte'] else 'ÉVOLUÉE'} · "
          f"F2 durée {d_base} s → {d_post} s : {'STABLE' if stable else 'DÉGRADÉE'}")
    print(f"  poids : {avant} → {apres} octets ({reduction:.1f} %) — seuil LOURD 30 Kio : "
          f"{'sous' if apres < SEUIL_LOURD else 'au-dessus'}")
    print(f"  COHÉRENT={coherent} · FONCTIONNEL={fonctionnel} · OPTIMISÉ={optimise} · "
          f"INTERACTIONS={'SAINES' if interactions_saines else 'CASSÉES'} · PERF={'STABLE' if stable else 'DÉGRADÉE'}")
    print(f"VERDICT POST : {verdict}")
    return 0 if verdict == "MAINTIEN DE L'OPTIMISATION" else 1


def cmd_verifier(nom: str) -> int:
    n = nature_du_skill(RACINE, nom)
    pv, manquants = pointeurs_valides(nom)
    nd, dup = non_duplication(nom)
    fonc = tests_fonctionnels(nom)
    inter = interactions(nom)
    verdict_poids = ("OK" if n["octets"] < 12 * 1024 else
                     "INTERMÉDIAIRE" if n["octets"] < SEUIL_LOURD else
                     "LOURD" if n["octets"] < SEUIL_CRITIQUE else "CRITIQUE")
    ok = pv and nd and fonc["verdict"] == "PASS" and inter["verdict"] == "SAINES"
    print(f"VÉRIFICATION re-curation — skills/{nom} v{n['version']} "
          f"({n['octets']} o / {n['octets']/1024:.1f} Kio / verdict poids {verdict_poids})")
    print(f"  pointeurs references/ ({len(n['references'])} fichiers) : "
          f"{'PASS' if pv else 'FAIL — manquants : ' + ', '.join(manquants)}")
    print(f"  non-duplication 1024 o : {'PASS' if nd else 'FAIL — ' + ', '.join(dup)}")
    print(f"  F1 fonctionnels : {fonc['verdict']} ({len(fonc['scripts'])} scripts · "
          f"{len(fonc['evals'])} evals · {fonc['duree_totale_s']} s)")
    print(f"  F3 interactions : {inter['verdict']} ({len(inter['sortantes'])} sortantes · "
          f"{len(inter['entrantes'])} entrantes · KB={inter['kb']['entree']})")
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
    """Bac à sable : PRE→GO, POST identité, familles v1.2.0 (fonctionnels exécutés,
    interactions saines + empreinte, sortante cassée → NO-GO, entrante violée →
    DÉRIVE, perf_stable unitaire), bump socle→PASS (harnais v3), déplacement R4 du
    corps→MAINTIEN (harnais v3), contrat altéré→DÉRIVE, compare, pointeur manquant.
    Témoin SANS section « ## §1 » (cas réel version-management — l'ancienne borne
    naïve capturait le corps entier)."""
    tmp = Path(tempfile.mkdtemp(prefix="recuration-selftest-"))
    global RACINE
    racine_sauve = RACINE
    try:
        (tmp / "skills" / "temoin" / "evals").mkdir(parents=True)
        (tmp / "skills" / "temoin" / "references").mkdir()
        (tmp / "skills" / "temoin" / "scripts").mkdir()
        (tmp / "download").mkdir()
        # v1.2.0 — fixture interactions : cible sortante + dépendant entrant + KB
        (tmp / "skills" / "cible-dep").mkdir()
        (tmp / "skills" / "cible-dep" / "SKILL.md").write_text(
            "---\nname: cible-dep\nversion: 2.0.0\ndescription: Cible de dépendance.\n---\nCorps cible.\n",
            encoding="utf-8")
        # v1.2.0 correctif — cible PLATEFORME : existante, SANS version déclarée
        # (cas réel image-edit pour iphone19) → NON-VERSIONNÉ, non-bloquant
        (tmp / "skills" / "cible-plateforme").mkdir()
        (tmp / "skills" / "cible-plateforme" / "SKILL.md").write_text(
            "---\nname: cible-plateforme\ndescription: Cible plateforme sans version.\n---\nCorps.\n",
            encoding="utf-8")
        (tmp / "skills" / "dependant").mkdir()
        (tmp / "skills" / "dependant" / "SKILL.md").write_text(
            "---\nname: dependant\nversion: 1.0.0\ndescription: Dépendant.\ndependencies:\n"
            "  - skill: temoin\n    version: \">=1.0.0\"\n---\nCorps dépendant.\n",
            encoding="utf-8")
        (tmp / "skills" / "KNOWLEDGE.md").write_text(
            "# Registre sandbox\n\n## temoin v1.0.0\n\n## dependant v1.0.0\n\n## cible-dep v2.0.0\n",
            encoding="utf-8")
        # v1.2.0 — fixture fonctionnels : script témoin avec --selftest
        (tmp / "skills" / "temoin" / "scripts" / "outil-mini.py").write_text(
            "#!/usr/bin/env python3\n\"\"\"Outil mini témoin (selftest embarqué).\"\"\"\nimport sys\n\n"
            "if __name__ == \"__main__\":\n    if \"--selftest\" in sys.argv:\n"
            "        print(\"SELFTEST PASS\")\n        sys.exit(0)\n    sys.exit(0)\n",
            encoding="utf-8")
        sk = tmp / "skills" / "temoin" / "SKILL.md"
        sk.write_text("""---
name: temoin
version: 1.0.0
description: >
  Témoin de test du harnais re-curation (frontmatter complet — convention
  SHARED §1.3 : name/version/description).
read_when:
  - Déclencher pour tester
dependencies:
  - skill: cible-dep
    version: ">=1.0.0"
  - skill: cible-plateforme
    version: ">=1.0.0"
---
## §A — DÉCLENCHEURS

- `temoin` — test

## §0 — Contexte Système (SHARED v1.7.34)

Bloc zéro du socle. Directive propriétaire 2026-10-31.

# Corps du témoin (pas de section « ## §1 » — cas réel version-management)

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

        # v1.2.0 — famille F1 : le script témoin est EXÉCUTÉ (selftest réel),
        # evals validés (objet OU liste — correctif), structure vérifiée.
        r.append(("F1 fonctionnels : outil-mini.py selftest EXÉCUTÉ PASS + evals (objet ET liste) + structure → PASS",
                  j2["baseline"]["tests"]["fonctionnels"]["verdict"] == "PASS"
                  and j2["baseline"]["tests"]["fonctionnels"]["scripts"]["outil-mini.py"]["verdict"] == "PASS"
                  and j2["baseline"]["tests"]["fonctionnels"]["scripts"]["outil-mini.py"]["test"] == "selftest exécuté"))

        # v1.2.0 — famille F3 : interactions saines (sortante + entrante + KB)
        # + empreinte sha256 capturée.
        r.append(("F3 interactions : sortante cible-dep PASS + entrante dependant PASS + KB PASS → SAINES + empreinte",
                  j2["baseline"]["tests"]["interactions"]["verdict"] == "SAINES"
                  and j2["baseline"]["tests"]["interactions"]["empreinte"]
                  and j2["baseline"]["tests"]["interactions"]["sortantes"][0]["verdict"] == "PASS"
                  and j2["baseline"]["tests"]["interactions"]["entrantes"][0]["verdict"] == "PASS"
                  and j2["baseline"]["tests"]["interactions"]["kb"]["verdict"] == "PASS"))

        # v1.2.0 correctif — cible PLATEFORME sans version (cas réel image-edit
        # pour iphone19) : l'arête existe, contrat semver invérifiable →
        # NON-VERSIONNÉ tracé, NON-bloquant (F3 demeure SAINES).
        r.append(("F3 cible plateforme sans version → NON-VERSIONNÉ (non-bloquant) + F3 SAINES",
                  j2["baseline"]["tests"]["interactions"]["sortantes"][1]["skill"] == "cible-plateforme"
                  and j2["baseline"]["tests"]["interactions"]["sortantes"][1]["verdict"] == "NON-VERSIONNÉ"
                  and j2["baseline"]["tests"]["interactions"]["verdict"] == "SAINES"))

        # v1.2.0 — dépendance SORTANTE cassée (contrat semver violé par la cible)
        # → interactions CASSÉES → PRE NO-GO (jamais de re-curation d'un élément
        # dont les arêtes sont déjà défectueuses) — puis restauration.
        (tmp / "skills" / "cible-dep" / "SKILL.md").write_text(
            "---\nname: cible-dep\nversion: 0.0.1\ndescription: Cible rétrogradée.\n---\nCorps.\n",
            encoding="utf-8")
        rcS = cmd_pre("temoin")
        jS = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("F3 sortante cassée (cible 0.0.1 < contrat >=1.0.0) → CASSÉES → PRE NO-GO rc=1",
                  rcS == 1 and jS["verdict_pre"] == "NO-GO"
                  and jS["baseline"]["tests"]["interactions"]["verdict"] == "CASSÉES"))
        (tmp / "skills" / "cible-dep" / "SKILL.md").write_text(
            "---\nname: cible-dep\nversion: 2.0.0\ndescription: Cible de dépendance.\n---\nCorps cible.\n",
            encoding="utf-8")

        # v1.2.0 — contrat ENTRANT violé (le dépendant exige temoin >= 2.0.0,
        # témoin 1.0.0) → POST : interactions CASSÉES → DÉRIVE — puis restauration.
        (tmp / "skills" / "dependant" / "SKILL.md").write_text(
            "---\nname: dependant\nversion: 1.0.0\ndescription: Dépendant.\ndependencies:\n"
            "  - skill: temoin\n    version: \">=2.0.0\"\n---\nCorps dépendant.\n",
            encoding="utf-8")
        rcE = cmd_post("temoin")
        jE = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("F3 entrante violée (dépendant exige >=2.0.0) → interactions CASSÉES → POST DÉRIVE rc=1",
                  rcE == 1 and jE["post"]["verdict_post"] == "DÉRIVE"
                  and not jE["post"]["interactions_saines"]))
        (tmp / "skills" / "dependant" / "SKILL.md").write_text(
            "---\nname: dependant\nversion: 1.0.0\ndescription: Dépendant.\ndependencies:\n"
            "  - skill: temoin\n    version: \">=1.0.0\"\n---\nCorps dépendant.\n",
            encoding="utf-8")

        # v1.2.0 — famille F2 : tolérance perf_stable unitaire (fonction pure).
        r.append(("F2 perf_stable : 1.0→1.4 s STABLE · 1.0→2.5 s DÉGRADÉE (×1.5 + 0.5 s)",
                  perf_stable(1.0, 1.4) is True and perf_stable(1.0, 2.5) is False
                  and perf_stable(None, 3.0) is True))

        # harnais v3 — leçon 1 : bump socle (étiquette SHARED + date de directive du
        # socle changées, contenu textuel inchangé) → ni l'un ni l'autre n'est une
        # dérive de contrat (harnais v2 couvrait l'étiquette, v3 couvre la date).
        t = sk.read_text(encoding="utf-8").replace(
            "## §0 — Contexte Système (SHARED v1.7.34)",
            "## §0 — Contexte Système (SHARED v1.7.35)").replace(
            "Directive propriétaire 2026-10-31.",
            "Directive propriétaire 2026-11-09.")
        sk.write_text(t, encoding="utf-8")
        rcB = cmd_post("temoin")
        jB = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("bump socle (étiquette + date) → section_0 PASS + MAINTIEN",
                  rcB == 0 and jB["post"]["comparaison_contrats"]["section_0_normalisee"] == "PASS"
                  and jB["post"]["verdict_post"] == "MAINTIEN DE L'OPTIMISATION"))

        # harnais v3 — leçon 2 : re-curation légitime du CORPS (déplacement R4 +
        # pointeur 1-ligne) avec bloc socle intact → MAINTIEN (l'ancienne borne
        # naïve « ## §1 » donnait un DÉRIVE fausse sur ce cas).
        gros = "Ligne de contenu mesurable. " * 120
        t = sk.read_text(encoding="utf-8").replace(
            gros, "> **Intégral archivé R4** : `references/section-deplacee.md` (déplacé).\n")
        (tmp / "skills" / "temoin" / "references" / "section-deplacee.md").write_text(gros, encoding="utf-8")
        sk.write_text(t, encoding="utf-8")
        rcA = cmd_post("temoin")
        jA = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("déplacement R4 du corps (socle intact) → MAINTIEN (faux-Fail v1.0.0 résorbé)",
                  rcA == 0 and jA["post"]["verdict_post"] == "MAINTIEN DE L'OPTIMISATION"
                  and jA["post"]["coherent"]))

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

        # v1.2.1 (KO-L003, Task 81 G2) — idempotence des verdicts POST sur état LOURD
        # stable : la baseline ancrée par un POST précédent → contrôle de NON-RÉGRESSION
        # (<=) et non de réduction stricte. Avant correctif : tout re-jeu POST sur un
        # élément LOURD (≥ 30 Kio) à poids stable était structurellement DÉRIVE (faille
        # sur preuves réelles iphone19 Task 81 : run 1 MAINTIEN −27,3 %, run 2 DÉRIVE 0 %).
        sk.write_text(sk.read_text(encoding="utf-8").replace(
            "\nVoir `references/absent.md`.\n", ""), encoding="utf-8")
        sk.write_text(sk.read_text(encoding="utf-8") + "\n" +
                      ("# bourre LOURD " + "x" * 60 + "\n") * 520, encoding="utf-8")
        cmd_pre("temoin")
        rcP1 = cmd_post("temoin")
        jP1 = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        rcP2 = cmd_post("temoin")
        jP2b = json.loads((tmp / "download" / "protocole-test-temoin.json").read_text(encoding="utf-8"))
        r.append(("v1.2.1 POST LOURD stable : 1er POST identité LOURD → DÉRIVE (réduction stricte exigée) · re-jeu sur baseline ancrée → MAINTIEN (non-régression)",
                  rcP1 == 1 and jP1["post"]["verdict_post"] == "DÉRIVE"
                  and rcP2 == 0 and jP2b["post"]["verdict_post"] == "MAINTIEN DE L'OPTIMISATION"))

        # v1.2.2 (Task 82 G3, KO-L003 — preuves réelles knowledge-observer) :
        # référence INTER-SKILL tolérée. Une citation
        # `<autre-skill>/references/<fichier>` (ex. réel : knowledge-observer
        # cite gen-plan/references/observation-patterns.md — SHARED §6.3,
        # la définition vit dans gen-plan) n'est pas un pointeur local
        # manquant. Avant correctif : --verifier knowledge-observer FAIL
        # « manquants : observation-patterns.md ».
        sk.write_text(sk.read_text(encoding="utf-8")
                      + "\nVoir `gen-plan/references/observation-patterns.md` (inter-skill).\n",
                      encoding="utf-8")
        rcX = cmd_verifier("temoin")
        r.append(("v1.2.2 référence inter-skill (gen-plan/references/…) tolérée → verifier rc=0 (et pointeur LOCAL manquant demeure rc=1, cas ci-dessus)",
                  rcX == 0))

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
    p = argparse.ArgumentParser(description="protocole-test.py — skill re-curation v1.2.2")
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
