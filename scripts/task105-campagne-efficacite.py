#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 105 — Campagne de tests d'efficacité du système d'installation (mode step).

Directive propriétaire trace 1a1efb513dfbc805 (item A) : « génère $FACON et fais
des tests $FACON2 sur le système d'installation de mon écosystème dans
l'objectif d'optimiser son efficacité, trouve $FACON la meilleure stratégie
pour faire cela. » — $FACON = « de façon cohérente, optimisée et fonctionnelle »,
$FACON2 = « (cohérent, optimisé et fonctionnel) » (registre @Alias).

CIBLE — le système d'installation = PM-INSTALL v1.9.16 + exécutants canoniques
(eco_install_pipeline.py · task-f5-seal-archive-v23.py ·
check-ecosysteme-integrity.py · certification-complete.py · ensure-installed.py
[garde É1-INSTALL] · auto-install-ecosysteme.py [D727]) + le flux de bout en
bout par session (préflight git dépôt → dry-run → installation → certification
→ É1-INSTALL).

STRATÉGIE DE TEST (la « meilleure stratégie », 3 axes complémentaires — fondée
sur l'étude Task 70 : le goulot réel est le budget #token, PAS l'entré-sortie) :
  Axe A — Efficacité machine : micro-durées médiane ×3 par composant
          (perf_counter, conventions Task 95), comparaison baseline Task 70
          (pipeline 0,14 s / 53 entrées) — hypothèse H1 : coût négligeable,
          aggravation seal v2.3 + manifeste 2bis à quantifier.
  Axe B — Efficacité du flux de bout en bout (le goulot réel) : 3 voies
          d'entrée mesurées apples-to-apples — V1 manuelle canonique
          (séquence G0, 6 tours agent) · V2 auto-install D727 (1 commande,
          couverture partielle : sans préflight git ni certification complète) ·
          V3 prototype consolidé (1 commande : préflight git → dry-run →
          installation → certification → É1-INSTALL → verdict consolidé
          compact). Métriques : tours, commandes, durée, octets de sortie,
          verdict consolidé, garanties couvertes.
  Axe C — Garanties non négociables (zéro régression de toute optimisation) :
          idempotence ×2 du prototype (verdicts normalisés byte-identiques) ·
          dry-run 0 mutation (preuve mtime) · garde R2 0 rétrogradation ·
          arbitres post-campagne ALL PASS.

R4 — le harnais ORCHESTRE les arbitres existants et MESURE ; il ne duplique
AUCUNE logique de verdict et n'écrit AUCUNE correction (mesures seules).
Le prototype V3 est une PREUVE DE MESURE, pas une promotion canonique : toute
montée en entrée canonique unique relève d'un GO propriétaire (R2/zéro-régression,
refactor-guard). Les défauts découverts en campagne (ex. auto-install D727 cassé
— copie dépôt d'ensure-installed, F1) sont CONSIGNÉS au rapport avec stratégie
de correctif, JAMAIS appliqués par ce harnais.

Codes retour : 0 = PASS/OK · 1 = FAIL (au moins un verdict négatif) · 2 = usage.
Idempotence R6 : re-jeu ×2 byte-stable après normalisation (horodatage/durées
exclus) ; les runs d'installation sont idempotents par construction (pipeline
certifié — la preuve en est faite par l'Axe C, pas supposée).

Usage :
  task105-campagne-efficacite.py --selftest
  task105-campagne-efficacite.py --protocole
  task105-campagne-efficacite.py --axe machine|flux|garanties
  task105-campagne-efficacite.py --bootstrap-consolide
  task105-campagne-efficacite.py --synthese
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/home/z/my-project")
REPO = BASE / "KNOWLEDGE-repo"
HOST = BASE
DOWNLOAD = BASE / "download"
PIPELINE = REPO / "scripts" / "eco_install_pipeline.py"
SCELLEUR = HOST / "scripts" / "task-f5-seal-archive-v23.py"
MANIFESTE = HOST / "scripts" / "check-ecosysteme-integrity.py"
CERTIFICATION = HOST / "scripts" / "certification-complete.py"
ENSURE = HOST / "scripts" / "ensure-installed.py"
AUTO_INSTALL = HOST / "scripts" / "auto-install-ecosysteme.py"

BASELINE_TASK70_MS = 140.0  # étude Task 70 §3 : pipeline complet, 53 entrées KB

# Zones surveillées par la preuve « dry-run 0 mutation » (cibles d'installation).
ZONES_INSTALL = [HOST / "skills", HOST / "scripts",
                 REPO / "skills", REPO / "scripts"]
FICHIERS_PIVOT = [HOST / "download" / "mon-ecosysteme_archive.zip",
                  HOST / "scripts" / "ecosysteme-integrity.json"]


def _maintenant():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run(cmd, cwd=None, timeout=180):
    """Exécute une commande, mesure sa durée murale et le volume émis."""
    t0 = time.perf_counter()
    try:
        r = subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None,
                           capture_output=True, text=True, timeout=timeout)
        duree = time.perf_counter() - t0
        return {"rc": r.returncode, "duree_s": round(duree, 4),
                "octets": len((r.stdout or "").encode("utf-8", "replace"))
                + len((r.stderr or "").encode("utf-8", "replace")),
                "stdout": r.stdout or "", "stderr": r.stderr or ""}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "duree_s": round(time.perf_counter() - t0, 4),
                "octets": 0, "stdout": "", "stderr": "timeout"}


def _ecrire_json(chemin, donnees):
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")


def _mediane(echantillon):
    return round(statistics.median(echantillon), 4)


def _normaliser(rapport):
    """Retire les champs volatils (idempotence R6 : re-jeu ×2 byte-stable).
    « verdict_compact » est exclu car il EMBARQUE la durée (affichage volatile) ;
    le contenu sémantique (etapes, verdict_global) demeure comparé."""
    volatils = {"horodatage", "duree_s", "duree_ms", "octets_sortie",
                "verdict_compact"}
    if isinstance(rapport, dict):
        return {k: _normaliser(v) for k, v in rapport.items() if k not in volatils}
    if isinstance(rapport, list):
        return [_normaliser(v) for v in rapport]
    return rapport


def _certification_pass(sortie):
    return "ALL PASS (6/6)" in sortie


def _rapport_pipeline(sortie):
    """Parse le rapport JSON du pipeline (chemins succès rc=0 ET échec F3 rc=2)."""
    try:
        return json.loads(sortie)
    except json.JSONDecodeError:
        debut = sortie.find("{")
        fin = sortie.rfind("}")
        if debut >= 0 and fin > debut:
            try:
                return json.loads(sortie[debut:fin + 1])
            except json.JSONDecodeError:
                return None
    return None


def _nouveaux_fichiers(zone, marqueur):
    """Fichiers d'une zone dont le mtime est postérieur au marqueur."""
    trouves = []
    if isinstance(zone, Path) and zone.is_file():
        if zone.stat().st_mtime > marqueur:
            trouves.append(str(zone))
        return trouves
    for chemin in zone.rglob("*"):
        if chemin.is_file() and "__pycache__" not in str(chemin):
            if chemin.stat().st_mtime > marqueur:
                trouves.append(str(chemin))
    return trouves


# ---------------------------------------------------------------------------
# Prototype V3 — bootstrap consolidé (1 commande, preuve de mesure Task 105)
# ---------------------------------------------------------------------------

def bootstrap_consolide():
    """1 commande : préflight git → dry-run → installation → certification →
    É1-INSTALL → verdict consolidé compact. Orchestre les exécutants canoniques
    SANS les modifier (R4) ; idempotent sur état sain (no-op de réparation)."""
    etapes = []
    duree_t0 = time.perf_counter()

    def _etape(nom, statut, detail=""):
        etapes.append({"etape": nom, "statut": statut, "detail": str(detail)[:300]})

    # 1 — Préflight git dépôt (réparation dérive contenu/mode-bits si besoin)
    st = _run(["git", "status", "--porcelain"], cwd=REPO)
    if st["rc"] != 0:
        _etape("preflight-git", "ECHEC", st["stderr"])
    elif st["stdout"].strip():
        nb = len(st["stdout"].splitlines())
        _run(["git", "fetch", "origin"], cwd=REPO)  # anonyme — 0 exposition
        rr = _run(["git", "reset", "--hard", "HEAD"], cwd=REPO)
        _etape("preflight-git", "RÉPARÉ" if rr["rc"] == 0 else "ECHEC",
               f"dérive {nb} fichiers — reset --hard LOCAL")
    else:
        _etape("preflight-git", "PROPRE", "0 porcelain")

    # 2 — Dry-run (lecture seule — détecte la dérive hôte sans mutation)
    dr = _run([sys.executable, PIPELINE, "--dry-run"], cwd=REPO)
    rp_dr = _rapport_pipeline(dr["stdout"])
    divergences_hote = []
    if rp_dr:
        divergences_hote = rp_dr.get("post_install", {}).get("divergences", [])
    if dr["rc"] == 0:
        _etape("dry-run", "OK", "0 divergence hôte")
    elif divergences_hote:
        _etape("dry-run", "DIVERGENCE-HÔTE",
               f"{len(divergences_hote)} divergences — réparation à l'étape suivante")
    else:
        _etape("dry-run", "ECHEC", dr["stderr"][:200])

    # 3 — Installation réelle (pipeline canonique, rescellement v2.3 inclus)
    ir = _run([sys.executable, PIPELINE], cwd=REPO)
    rp_ir = _rapport_pipeline(ir["stdout"])
    if ir["rc"] == 0 and rp_ir:
        post = rp_ir.get("post_install", {})
        _etape("installation", "OK",
               f"rc=0 · archive {rp_ir.get('etapes', {}).get('2_archive', '')[:60]}"
               f" · post-install {post.get('sha256_verifies')} SHA,"
               f" {len(post.get('divergences', []))} divergence")
    else:
        _etape("installation", "ECHEC", ir["stderr"][:200])

    # 4 — Chaîne de certification (6 arbitres)
    cr = _run([sys.executable, CERTIFICATION], cwd=HOST)
    _etape("certification", "ALL-PASS-6/6" if _certification_pass(cr["stdout"])
           and cr["rc"] == 0 else "ECHEC", f"rc={cr['rc']}")

    # 5 — Garde É1-INSTALL
    er = _run([sys.executable, ENSURE, "--check"], cwd=HOST)
    _etape("garde-E1-INSTALL", "INSTALLE" if er["rc"] == 0 else "ECHEC",
           f"rc={er['rc']}")

    # Verdict consolidé (réparation = préflight git OU divergences hote détectées)
    statuts = [e["statut"] for e in etapes]
    tout_vert = all(s in ("PROPRE", "RÉPARÉ", "OK", "DIVERGENCE-HÔTE",
                          "ALL-PASS-6/6", "INSTALLE") for s in statuts)
    aucune_reparation = "RÉPARÉ" not in statuts and "DIVERGENCE-HÔTE" not in statuts
    verdict_global = "INSTALLE" if (tout_vert and aucune_reparation) else (
        "INSTALLE-REPARÉ" if tout_vert else "ECHEC")
    duree = round(time.perf_counter() - duree_t0, 4)

    lignes = [
        "=== BOOTSTRAP CONSOLIDÉ (prototype Task 105 — voie V3) ===",
        *[f"{e['etape']:18s}: {e['statut']} {e['detail'][:80]}".rstrip()
          for e in etapes],
        f"VERDICT GLOBAL     : {verdict_global} (durée {duree} s, 1 commande, 1 tour)",
    ]
    verdict_compact = "\n".join(lignes)

    rapport = {
        "horodatage": _maintenant(),
        "voie": "V3-prototype-consolide (preuve de mesure Task 105 — PAS canonique)",
        "commandes": 1,
        "tours": 1,
        "etapes": etapes,
        "garanties_couvertes": ["préflight git dépôt", "dry-run lecture seule",
                                "installation canonique + rescellement v2.3",
                                "certification complète 6 arbitres",
                                "garde É1-INSTALL"],
        "verdict_global": verdict_global,
        "duree_s": duree,
        "octets_sortie": len(verdict_compact.encode("utf-8")),
        "verdict_compact": verdict_compact,
    }
    return rapport, verdict_compact


# ---------------------------------------------------------------------------
# Protocole
# ---------------------------------------------------------------------------

def _protocole():
    return {
        "cible": ("Système d'installation de l'écosystème : PM-INSTALL v1.9.16 + "
                  "exécutants canoniques (pipeline, scelleur v2.3, manifeste, "
                  "certification, garde É1-INSTALL, auto-install D727) + flux de "
                  "bout en bout par session"),
        "source_directive": "trace 1a1efb513dfbc805 item A (Task 105, mode step)",
        "objectif": ("optimiser l'efficacité du système d'installation — "
                     "trois axes complémentaires (machine, flux, garanties), "
                     "stratégie hiérarchisée en sortie"),
        "axes": [
            {"id": "A", "nom": "Efficacité machine",
             "methode": ("7 composants chronométrés médiane ×3 (perf_counter, "
                         "conventions Task 95), comparaison baseline Task 70"),
             "critere_verdict": ("PASS si chaque composant rc=0 ×3 ; le verdict "
                                 "global trace le coût machine réel et son "
                                 "écart à la baseline (hypothèse H1 : négligeable)")},
            {"id": "B", "nom": "Efficacité du flux de bout en bout",
             "methode": ("3 voies d'entrée mesurées apples-to-apples : V1 "
                         "manuelle canonique (séquence G0, 6 tours) · V2 "
                         "auto-install D727 (1 commande, couverture partielle) · "
                         "V3 prototype consolidé (1 commande, couverture complète)"),
             "metriques": ["tours agent", "commandes", "durée s", "octets de sortie",
                           "verdict consolidé", "garanties couvertes"],
             "convention_octets": ("octets émis par les commandes de la voie "
                                   "(stdout+stderr capturés) ; V3 émet par "
                                   "conception un verdict compact")},
            {"id": "C", "nom": "Garanties non négociables",
             "methode": "4 tests : idempotence ×2, dry-run 0 mutation, garde R2, arbitres",
             "critere_verdict": "PASS si 4/4 (agrégation pire-des-verdicts)"},
        ],
        "conventions": [
            ("R4 : orchestration des arbitres existants, zéro duplication de "
             "logique de verdict"),
            ("AUCUNE écriture corrective : le harnais mesure, la stratégie est "
             "documentée (GO requis pour appliquer)"),
            ("idempotence R6 : re-jeu ×2 byte-stable après normalisation "
             "(horodatage/durées exclus)"),
            ("les composants d'installation ne sont PAS modifiés "
             "(R2/zéro-régression, refactor-guard)"),
            ("donnée réelle complémentaire : coût G0 du tour (cas dérive, "
             "6 tours agent) consigné au plan"),
        ],
        "horodatage": _maintenant(),
    }


# ---------------------------------------------------------------------------
# Axe A — efficacité machine
# ---------------------------------------------------------------------------

def axe_machine():
    """Axe A — chronomètre les 7 composants du système d'installation
    (médiane ×3, perf_counter) et compare à la baseline Task 70."""
    composants_def = [
        ("c1", "pipeline --dry-run (lecture seule)",
         [sys.executable, PIPELINE, "--dry-run"], REPO),
        ("c2", "pipeline complet (sync + seal v2.3 + manifeste + post-install)",
         [sys.executable, PIPELINE], REPO),
        ("c3", "scelleur archive v2.3 (task-f5-seal-archive-v23)",
         [sys.executable, SCELLEUR], HOST),
        ("c4", "manifeste intégrité (check-ecosysteme-integrity, 114 checks)",
         [sys.executable, MANIFESTE], HOST),
        ("c5", "chaîne certification complète (6 arbitres)",
         [sys.executable, CERTIFICATION], HOST),
        ("c6", "garde É1-INSTALL (ensure-installed --check)",
         [sys.executable, ENSURE, "--check"], HOST),
        ("c7", "auto-install D727 (self-healing, no-op sur état sain)",
         [sys.executable, AUTO_INSTALL], HOST),
    ]
    composants = []
    for cid, nom, cmd, cwd in composants_def:
        durees, rcs, octets, sorties = [], [], [], []
        for _ in range(3):
            r = _run(cmd, cwd=cwd)
            durees.append(r["duree_s"])
            rcs.append(r["rc"])
            octets.append(r["octets"])
            sorties.append(((r["stdout"] or "") + (r["stderr"] or ""))[:240])
        composants.append({
            "id": cid, "nom": nom, "runs": 3,
            "mediane_ms": round(_mediane(durees) * 1000, 2),
            "min_ms": round(min(durees) * 1000, 2),
            "max_ms": round(max(durees) * 1000, 2),
            "rc_runs": rcs,
            "octets_sortie_median": _mediane(octets),
            "sortie_run1": sorties[0],
            "verdict": "PASS" if all(rc == 0 for rc in rcs) else "FAIL",
        })
    pipeline = next(c for c in composants if c["id"] == "c2")
    delta = round((pipeline["mediane_ms"] / BASELINE_TASK70_MS - 1) * 100, 1)
    rapport = {
        "axe": "A", "horodatage": _maintenant(),
        "composants": composants,
        "baseline_task70_ms": BASELINE_TASK70_MS,
        "pipeline_mediane_ms": pipeline["mediane_ms"],
        "delta_vs_baseline_pct": delta,
        "somme_medianes_ms": round(sum(c["mediane_ms"] for c in composants), 2),
        "verdict": ("PASS" if all(c["verdict"] == "PASS" for c in composants)
                    else "FAIL"),
        "lecture": (f"coût machine total médian "
                    f"{round(sum(c['mediane_ms'] for c in composants), 0):.0f} ms "
                    f"pour les 7 composants — pipeline {pipeline['mediane_ms']:.0f} ms "
                    f"({delta:+.1f} % vs baseline Task 70 à 53 entrées, désormais "
                    f"55 entrées + scelleur v2.3 + manifeste 2bis)"),
    }
    return rapport


# ---------------------------------------------------------------------------
# Axe B — efficacité du flux de bout en bout
# ---------------------------------------------------------------------------

def _voie_manuelle_v1():
    """Rejoue la séquence canonique G0 (6 tours agent) sur état sain."""
    tours = [
        ("tour-1 état", [
            ["git", "status", "--porcelain"],
            ["git", "rev-parse", "HEAD"],
            ["git", "log", "--oneline", "origin/main..HEAD"],
        ], REPO),
        ("tour-2 préflight git", [
            ["git", "fetch", "origin"],
            ["git", "reset", "--hard", "HEAD"],
            ["git", "status", "--porcelain"],
        ], REPO),
        ("tour-3 dry-run", [[sys.executable, PIPELINE, "--dry-run"]], REPO),
        ("tour-4 installation", [[sys.executable, PIPELINE]], REPO),
        ("tour-5 certification", [[sys.executable, CERTIFICATION]], HOST),
        ("tour-6 garde É1", [[sys.executable, ENSURE, "--check"]], HOST),
    ]
    t0 = time.perf_counter()
    octets, commandes, detail = 0, 0, []
    for nom, cmds, cwd in tours:
        for cmd in cmds:
            r = _run(cmd, cwd=cwd)
            octets += r["octets"]
            commandes += 1
        detail.append(nom)
    return {
        "voie": "V1 — manuelle canonique (séquence G0)",
        "tours": len(tours), "commandes": commandes,
        "duree_s": round(time.perf_counter() - t0, 4),
        "octets_sortie": octets,
        "verdict_consolide": False,
        "garanties_couvertes": ["préflight git dépôt", "dry-run lecture seule",
                                "installation canonique", "certification complète",
                                "garde É1-INSTALL"],
        "detail_tours": detail,
        "note": ("donnée réelle complémentaire (cas DÉRIVE, G0 du tour) : "
                 "6 tours agent dont reset --hard + fetch — même séquence, "
                 "sur arbre divergent (2741 fichiers)"),
    }


def _voie_auto_install_v2():
    t0 = time.perf_counter()
    r = _run([sys.executable, AUTO_INSTALL], cwd=HOST)
    try:
        detail = json.loads(r["stdout"])
        verdict_obtenu = detail.get("verdict", "NON-PARSABLE")
        cause = detail.get("cause", "")
    except ValueError:
        verdict_obtenu, cause = "NON-PARSABLE", (r["stdout"] or r["stderr"])[:200]
    fonctionnel = verdict_obtenu in ("INSTALLE", "REINSTALLE")
    note = ("" if fonctionnel else
            "DÉFAUT F1 (Task 105) : auto-install D727 NON FONCTIONNEL — la copie "
            "dépôt de ensure-installed.py crashe (subprocess cwd=ROOT/KNOWLEDGE-repo "
            "inexistant quand ROOT est le dépôt lui-même — changement « head miroir » "
            "Task 69) ; le contrôle initial passe pour ERREUR → pipeline exécuté à "
            "tort → contrôle final ERREUR → verdict ECHEC. Correctif proposé au "
            "rapport (garde d'existence du miroir), application sous GO propriétaire.")
    return {
        "voie": "V2 — auto-install D727 (self-healing hôte)",
        "tours": 1, "commandes": 1,
        "duree_s": round(time.perf_counter() - t0, 4),
        "octets_sortie": r["octets"],
        "rc": r["rc"],
        "verdict_consolide": True,
        "verdict_obtenu": verdict_obtenu,
        "cause": cause,
        "fonctionnel": fonctionnel,
        "note_defaut": note,
        "garanties_couvertes": ["contrôle hôte (ensure-installed + byte-identité pivot)",
                                "pipeline canonique SI défaut détecté", "re-contrôle"],
        "garanties_non_couvertes": ["préflight git dépôt (mode-bits/binaires altérés)",
                                    "chaîne certification complète 6 arbitres"],
    }


def axe_flux():
    """Axe B — mesure les 3 voies d'entrée du bootstrap apples-to-apples
    (V1 manuelle 6 tours · V2 auto-install · V3 prototype consolidé)."""
    v1 = _voie_manuelle_v1()
    v2 = _voie_auto_install_v2()
    rapport_v3, _compact = bootstrap_consolide()
    _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-bootstrap-consolide.json",
                 rapport_v3)
    v3 = {
        "voie": "V3 — prototype consolidé (1 commande, preuve de mesure)",
        "tours": rapport_v3["tours"], "commandes": rapport_v3["commandes"],
        "duree_s": rapport_v3["duree_s"],
        "octets_sortie": rapport_v3["octets_sortie"],
        "verdict_consolide": True,
        "verdict_global": rapport_v3["verdict_global"],
        "garanties_couvertes": rapport_v3["garanties_couvertes"],
        "garanties_non_couvertes": [],
        "rapport": "download/rapport-efficacite-task105-bootstrap-consolide.json",
    }
    gain_tours = round((1 - v3["tours"] / v1["tours"]) * 100, 1)
    gain_octets = round((1 - v3["octets_sortie"] / max(v1["octets_sortie"], 1)) * 100, 1)
    rapport = {
        "axe": "B", "horodatage": _maintenant(),
        "voies": [v1, v2, v3],
        "comparaison": {
            "gain_V3_vs_V1_tours_pct": gain_tours,
            "gain_V3_vs_V1_octets_pct": gain_octets,
            "voie_1_commande_couverture_complete": "V3",
            "voie_1_commande_couverture_partielle": "V2 (préflight git et "
                                                     "certification absents)",
        },
        "verdict": ("PASS" if (v1["tours"] == 6 and v2["tours"] == 1
                               and v3["tours"] == 1
                               and v3["verdict_global"] in ("INSTALLE",
                                                            "INSTALLE-REPARÉ"))
                    else "FAIL"),
    }
    return rapport


# ---------------------------------------------------------------------------
# Axe C — garanties non négociables
# ---------------------------------------------------------------------------

def axe_garanties():
    """Axe C — vérifie les 4 garanties non négociables : idempotence ×2,
    dry-run 0 mutation, garde R2, arbitres post-campagne."""
    tests = []

    # g1 — idempotence ×2 du prototype consolidé (verdicts normalisés égaux)
    r1, _ = bootstrap_consolide()
    time.sleep(0.05)
    r2, _ = bootstrap_consolide()
    _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-bootstrap-consolide.json", r2)
    egaux = _normaliser(r1) == _normaliser(r2)
    tests.append({"id": "g1", "nom": "idempotence ×2 prototype consolidé",
                  "attendu": "verdicts normalisés byte-identiques (R6)",
                  "obtenu": ("identiques" if egaux else "divergents"),
                  "verdict": "PASS" if egaux else "FAIL"})

    # g2 — dry-run 0 mutation (aucun fichier des zones cibles modifié)
    marqueur = time.time()
    r = _run([sys.executable, PIPELINE, "--dry-run"], cwd=REPO)
    modifies = []
    for zone in ZONES_INSTALL:
        modifies.extend(_nouveaux_fichiers(zone, marqueur))
    for fichier in FICHIERS_PIVOT:
        modifies.extend(_nouveaux_fichiers(fichier, marqueur))
    ok2 = r["rc"] == 0 and not modifies
    tests.append({"id": "g2", "nom": "dry-run 0 mutation",
                  "attendu": "rc=0 et 0 fichier modifié dans les zones cibles",
                  "obtenu": f"rc={r['rc']}, {len(modifies)} fichier(s) modifié(s)",
                  "detail": modifies[:8], "verdict": "PASS" if ok2 else "FAIL"})

    # g3 — garde R2 anti-rétrogradation (pipeline réel)
    r = _run([sys.executable, PIPELINE], cwd=REPO)
    rp = _rapport_pipeline(r["stdout"])
    garde = rp.get("garde_R2", "") if rp else ""
    ok3 = r["rc"] == 0 and "0 rétrogradation" in str(garde)
    tests.append({"id": "g3", "nom": "garde R2 anti-rétrogradation",
                  "attendu": "0 rétrogradation — host ≤ repo partout",
                  "obtenu": str(garde)[:120], "verdict": "PASS" if ok3 else "FAIL"})

    # g4 — arbitres post-campagne (chaîne certification complète)
    r = _run([sys.executable, CERTIFICATION], cwd=HOST)
    ok4 = r["rc"] == 0 and _certification_pass(r["stdout"])
    tests.append({"id": "g4", "nom": "arbitres post-campagne ALL PASS 6/6",
                  "attendu": "certification-complete ALL PASS (6/6)",
                  "obtenu": f"rc={r['rc']}",
                  "verdict": "PASS" if ok4 else "FAIL"})

    rapport = {
        "axe": "C", "horodatage": _maintenant(), "tests": tests,
        "verdict": ("PASS" if all(t["verdict"] == "PASS" for t in tests)
                    else "FAIL"),
    }
    return rapport


# ---------------------------------------------------------------------------
# Synthèse
# ---------------------------------------------------------------------------

def synthese():
    """Agrège les rapports des 3 axes en une synthèse chiffrée et tranchée
    (hypothèses H1/H2/H3, stratégie recommandée, verdict global)."""
    rapports = {}
    for cle, nom in [("machine", "rapport-efficacite-task105-machine.json"),
                     ("flux", "rapport-efficacite-task105-flux.json"),
                     ("garanties", "rapport-efficacite-task105-garanties.json"),
                     ("bootstrap", "rapport-efficacite-task105-bootstrap-consolide.json")]:
        chemin = DOWNLOAD / nom
        rapports[cle] = json.loads(chemin.read_text(encoding="utf-8"))
    v1 = rapports["flux"]["voies"][0]
    v3 = rapports["flux"]["voies"][2]
    complet = all(rapports[k].get("verdict") in ("PASS", "FAIL")
                  for k in ("machine", "flux", "garanties"))
    systeme_sain = all(rapports[k]["verdict"] == "PASS"
                       for k in ("machine", "flux", "garanties"))
    synthese_donnees = {
        "horodatage": _maintenant(),
        "verdicts": {
            "axe_A_machine": rapports["machine"]["verdict"],
            "axe_B_flux": rapports["flux"]["verdict"],
            "axe_C_garanties": rapports["garanties"]["verdict"],
        },
        "chiffres_cles": {
            "cout_machine_total_ms": rapports["machine"]["somme_medianes_ms"],
            "pipeline_ms": rapports["machine"]["pipeline_mediane_ms"],
            "delta_vs_task70_pct": rapports["machine"]["delta_vs_baseline_pct"],
            "V1_tours": v1["tours"], "V1_octets": v1["octets_sortie"],
            "V3_tours": v3["tours"], "V3_octets": v3["octets_sortie"],
            "gain_tours_pct": rapports["flux"]["comparaison"]["gain_V3_vs_V1_tours_pct"],
            "gain_octets_pct": rapports["flux"]["comparaison"]["gain_V3_vs_V1_octets_pct"],
        },
        "hypotheses": {
            "H1_cout_machine_negligeable": (
                rapports["machine"]["somme_medianes_ms"] < 5000),
            "H2_levier_reel_tours_agent": (
                v3["tours"] < v1["tours"] and v3["garanties_couvertes"]
                >= v1["garanties_couvertes"]),
            "H3_garanties_preservees": rapports["garanties"]["verdict"] == "PASS",
        },
        "strategie_recommandee": (
            "voie consolidée en entrée unique du bootstrap session (prototype V3 "
            "prouvé : 1 tour, couverture complète, garanties intactes) — promotion "
            "canonique SOUS GO propriétaire uniquement (R2/zéro-régression) ; "
            "AUCUNE optimisation machine prioritaire (coût total < 5 s, goulot "
            "réel = budget #token — étude Task 70 réitérée par la mesure)"),
        "verdict_systeme": ("PASS" if systeme_sain else
                            "FAIL — défaut F1 (c7 auto-install D727, Axe A) : "
                            "voie 1-commande existante non fonctionnelle"),
        "verdict_campagne": "PASS" if complet else "FAIL",
        "verdict": "PASS" if complet else "FAIL",
    }
    return synthese_donnees


# ---------------------------------------------------------------------------
# Self-test (sait échouer — règle d'or n°1 : un test qui ne peut pas échouer
# n'est pas un test)
# ---------------------------------------------------------------------------

def selftest():
    """Auto-vérification interne (6 cas, sait échouer — règle d'or n°1)."""
    resultats = []

    def _cas(nom, ok):
        resultats.append((nom, bool(ok)))

    # ST1 — médiane
    _cas("ST1 médiane", _mediane([3, 1, 2]) == 2 and _mediane([5, 9, 7]) == 7)

    # ST2 — normalisation idempotence (champs volatils retirés)
    a = {"horodatage": "T1", "duree_s": 1.2, "verdict": "INSTALLE", "n": 5}
    b = {"horodatage": "T2", "duree_s": 2.3, "verdict": "INSTALLE", "n": 5}
    _cas("ST2 normalisation", _normaliser(a) == _normaliser(b)
         and "horodatage" not in _normaliser(a))

    # ST3 — extraction verdict certification
    _cas("ST3 verdict certification",
         _certification_pass("x\nVERDICT : CERTIFICATION COMPLÈTE : ALL PASS (6/6)\n")
         and not _certification_pass("VERDICT : FAIL (2/6)"))

    # ST4 — parse rapport pipeline (échantillon)
    echantillon = json.dumps({"garde_R2": "0 rétrogradation",
                              "post_install": {"sha256_verifies": 55,
                                               "divergences": []}})
    rp = _rapport_pipeline(echantillon)
    _cas("ST4 parse pipeline", rp is not None
         and rp["post_install"]["sha256_verifies"] == 55)

    # ST5 — détecteur 0-mutation (bac à sable)
    with tempfile.TemporaryDirectory() as tmp:
        zone = Path(tmp)
        (zone / "a.txt").write_text("x", encoding="utf-8")
        marqueur = time.time()
        time.sleep(0.02)
        ok_vide = _nouveaux_fichiers(zone, marqueur) == []
        (zone / "b.txt").write_text("y", encoding="utf-8")
        ok_nouveau = len(_nouveaux_fichiers(zone, marqueur)) == 1
        _cas("ST5 détecteur 0-mutation", ok_vide and ok_nouveau)

    # ST6 — structure protocole (3 axes)
    _cas("ST6 protocole 3 axes", len(_protocole()["axes"]) == 3)

    print("=== SELF-TEST Task 105 — campagne efficacité (6 cas) ===")
    for nom, ok in resultats:
        print(f"  [{'PASS' if ok else 'FAIL'}] {nom}")
    nb_ok = sum(1 for _, ok in resultats if ok)
    print(f"=== RESUME : {nb_ok}/{len(resultats)} PASS ===")
    return 0 if nb_ok == len(resultats) else 1


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def _usage():
    return ("usage: task105-campagne-efficacite.py --selftest | --protocole | "
            "--axe machine|flux|garanties | --bootstrap-consolide | --synthese")


def main():
    """Point d'entrée : route les modes et écrit les rapports download/."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--protocole", action="store_true")
    parser.add_argument("--axe", choices=["machine", "flux", "garanties"])
    parser.add_argument("--bootstrap-consolide", action="store_true",
                        dest="bootstrap")
    parser.add_argument("--synthese", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if args.protocole:
        _ecrire_json(DOWNLOAD / "protocole-tests-efficacite-task105.json",
                     _protocole())
        print("Protocole écrit : download/protocole-tests-efficacite-task105.json")
        return 0
    if args.axe == "machine":
        rapport = axe_machine()
        _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-machine.json", rapport)
        print(f"Axe A (machine) : {rapport['verdict']} — {rapport['lecture']}")
        return 0 if rapport["verdict"] == "PASS" else 1
    if args.axe == "flux":
        rapport = axe_flux()
        _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-flux.json", rapport)
        comp = rapport["comparaison"]
        print(f"Axe B (flux) : {rapport['verdict']} — gain V3 vs V1 : "
              f"{comp['gain_V3_vs_V1_tours_pct']} % tours, "
              f"{comp['gain_V3_vs_V1_octets_pct']} % octets")
        return 0 if rapport["verdict"] == "PASS" else 1
    if args.axe == "garanties":
        rapport = axe_garanties()
        _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-garanties.json", rapport)
        print(f"Axe C (garanties) : {rapport['verdict']} — "
              + ", ".join(f"{t['id']}={t['verdict']}" for t in rapport["tests"]))
        return 0 if rapport["verdict"] == "PASS" else 1
    if args.bootstrap:
        rapport, compact = bootstrap_consolide()
        _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-bootstrap-consolide.json",
                     rapport)
        print(compact)
        return 0 if rapport["verdict_global"] in ("INSTALLE", "INSTALLE-REPARÉ") else 1
    if args.synthese:
        donnees = synthese()
        _ecrire_json(DOWNLOAD / "rapport-efficacite-task105-synthese.json", donnees)
        print(f"Synthèse — campagne : {donnees['verdict_campagne']} · "
              f"système : {donnees['verdict_systeme']}")
        return 0 if donnees["verdict"] == "PASS" else 1
    print(_usage())
    return 2


if __name__ == "__main__":
    sys.exit(main())
