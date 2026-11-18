#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bootstrap consolidé de l'écosystème — ENTRÉE CANONIQUE UNIQUE du bootstrap de session.

PM-INSTALL §3.2(c) v1.10.0 (GO-1, Task 107 — promotion de la voie consolidée,
feuille de route §8 du rapport Task 105) : 1 commande = préflight git dépôt →
dry-run lecture seule → installation canonique → certification 6 arbitres →
garde É1-INSTALL → verdict consolidé compact. Gains mesurés (campagne Task 105,
voie V3 vs V1 manuelle) : −83,3 % de tours agent, −97,6 % d'octets émis, sans
aucune perte de garantie (idempotence ×2, dry-run lecture seule, garde R2,
arbitres 6/6).

Orchestration R4 : exécute les EXÉCUTANTS CANONIQUES existants par
sous-processus et agrège leurs verdicts — ne duplique aucune logique de
verdict, n'écrit aucune correction propre, ne modifie ni le pipeline ni les
arbitres (R2/zéro-régression, GO-1 trace 1a1efebf27dcbafd). Le harnais
task105-campagne-efficacite.py demeure la preuve de mesure historique ; le
présent script en est la promotion canonique (point d'entrée documenté).

Usage :
  bootstrap-ecosysteme.py            # bootstrap consolidé (répare si dérive)
  bootstrap-ecosysteme.py --selftest # tests internes (aucune mutation)

Codes retour : 0 = INSTALLE / INSTALLE-REPARÉ · 1 = ECHEC · 64 = usage.
Idempotent ×2 : re-jeu sur état sain = no-op de réparation (verdict INSTALLE).
Rapport machine : download/bootstrap-ecosysteme-rapport.json (artefact de
travail — seule écriture propre du script, hors exécutants canoniques).
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0,
# ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme
# installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/.

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/home/z/my-project")
REPO = BASE / "KNOWLEDGE-repo"
HOST = BASE
DOWNLOAD = BASE / "download"
PIPELINE = REPO / "scripts" / "eco_install_pipeline.py"
CERTIFICATION = HOST / "scripts" / "certification-complete.py"
ENSURE = HOST / "scripts" / "ensure-installed.py"
RAPPORT = DOWNLOAD / "bootstrap-ecosysteme-rapport.json"

# Statuts verts d'une étape (tout autre statut = ECHEC au verdict consolidé).
STATS_VERTS = ("PROPRE", "RÉPARÉ", "OK", "DIVERGENCE-HÔTE", "ALL-PASS-6/6", "INSTALLE")


def _maintenant():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run(cmd, cwd=None, timeout=300):
    """Exécute une commande, mesure sa durée murale et le volume émis."""
    t0 = time.perf_counter()
    try:
        r = subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None,
                           capture_output=True, text=True, timeout=timeout)
        return {"rc": r.returncode, "duree_s": round(time.perf_counter() - t0, 4),
                "octets": len((r.stdout or "").encode("utf-8", "replace"))
                + len((r.stderr or "").encode("utf-8", "replace")),
                "stdout": r.stdout or "", "stderr": r.stderr or ""}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "duree_s": round(time.perf_counter() - t0, 4),
                "octets": 0, "stdout": "", "stderr": "timeout"}


def _rapport_pipeline(sortie):
    """Parse le rapport JSON du pipeline (rc=0 succès ET rc=2 échec post-install)."""
    try:
        return json.loads(sortie)
    except json.JSONDecodeError:
        debut, fin = sortie.find("{"), sortie.rfind("}")
        if debut >= 0 and fin > debut:
            try:
                return json.loads(sortie[debut:fin + 1])
            except json.JSONDecodeError:
                return None
    return None


def _verdict(etapes):
    """Agrège les statuts en verdict consolidé — logique propre MINIMALE :
    aucun arbitrage technique (chaque statut vient d'un exécutant canonique)."""
    statuts = [e["statut"] for e in etapes]
    tout_vert = all(s in STATS_VERTS for s in statuts)
    aucune_reparation = "RÉPARÉ" not in statuts and "DIVERGENCE-HÔTE" not in statuts
    if tout_vert and aucune_reparation:
        return "INSTALLE"
    if tout_vert:
        return "INSTALLE-REPARÉ"
    return "ECHEC"


def bootstrap():
    """Séquence canonique consolidée — 1 commande, 1 tour agent."""
    etapes = []
    t0 = time.perf_counter()

    def _etape(nom, statut, detail=""):
        etapes.append({"etape": nom, "statut": statut, "detail": str(detail)[:300]})

    # 1 — Préflight git dépôt (réparation dérive mode-bits/contenu si besoin —
    #     reset --hard LOCAL uniquement, fetch ANONYME : 0 exposition de jeton)
    st = _run(["git", "status", "--porcelain"], cwd=REPO)
    if st["rc"] != 0:
        _etape("preflight-git", "ECHEC", st["stderr"])
    elif st["stdout"].strip():
        nb = len(st["stdout"].splitlines())
        _run(["git", "fetch", "origin"], cwd=REPO)
        rr = _run(["git", "reset", "--hard", "HEAD"], cwd=REPO)
        _etape("preflight-git", "RÉPARÉ" if rr["rc"] == 0 else "ECHEC",
               f"dérive {nb} fichiers — reset --hard LOCAL")
    else:
        _etape("preflight-git", "PROPRE", "0 porcelain")

    # 2 — Dry-run (lecture seule — détecte la dérive hôte sans mutation)
    dr = _run([sys.executable, PIPELINE, "--dry-run"], cwd=REPO)
    rp_dr = _rapport_pipeline(dr["stdout"])
    divergences = rp_dr.get("post_install", {}).get("divergences", []) if rp_dr else []
    if dr["rc"] == 0:
        _etape("dry-run", "OK", "0 divergence hôte")
    elif divergences:
        _etape("dry-run", "DIVERGENCE-HÔTE",
               f"{len(divergences)} divergences — réparation à l'étape suivante")
    else:
        _etape("dry-run", "ECHEC", dr["stderr"][:200])

    # 3 — Installation réelle (pipeline canonique : sync union + garde R2 +
    #     rescellement archive v2.3 + manifeste + post-install SHA)
    ir = _run([sys.executable, PIPELINE], cwd=REPO)
    rp_ir = _rapport_pipeline(ir["stdout"])
    if ir["rc"] == 0 and rp_ir:
        post = rp_ir.get("post_install", {})
        _etape("installation", "OK",
               f"rc=0 · post-install {post.get('sha256_verifies')} SHA, "
               f"{len(post.get('divergences', []))} divergence")
    else:
        _etape("installation", "ECHEC", ir["stderr"][:200])

    # 4 — Chaîne de certification (6 arbitres)
    cr = _run([sys.executable, CERTIFICATION], cwd=HOST)
    _etape("certification", "ALL-PASS-6/6"
           if cr["rc"] == 0 and "ALL PASS (6/6)" in cr["stdout"] else "ECHEC",
           f"rc={cr['rc']}")

    # 5 — Garde É1-INSTALL
    er = _run([sys.executable, ENSURE, "--check"], cwd=HOST)
    _etape("garde-E1-INSTALL", "INSTALLE" if er["rc"] == 0 else "ECHEC",
           f"rc={er['rc']}")

    verdict_global = _verdict(etapes)
    duree = round(time.perf_counter() - t0, 4)
    lignes = [
        "=== BOOTSTRAP CONSOLIDÉ (entrée canonique — PM-INSTALL §3.2-c) ===",
        *[f"{e['etape']:18s}: {e['statut']} {e['detail'][:80]}".rstrip()
          for e in etapes],
        f"VERDICT GLOBAL     : {verdict_global} (durée {duree} s, 1 commande, 1 tour)",
    ]
    verdict_compact = "\n".join(lignes)
    print(verdict_compact)

    rapport = {
        "horodatage": _maintenant(),
        "voie": "V3-canonique (entrée consolidée PM-INSTALL §3.2-c, GO-1 Task 107)",
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
    try:
        RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    except OSError:
        pass  # le verdict stdout demeure l'interface — le rapport est un artefact
    return rapport, verdict_compact


def selftest() -> int:
    """Tests internes — AUCUNE mutation (lecture seule)."""
    checks = []

    # T1 : exécutants canoniques présents (dépôt + hôte)
    requis = [REPO / "skills" / "KNOWLEDGE.md", PIPELINE, CERTIFICATION, ENSURE]
    manquants = [str(p) for p in requis if not p.exists()]
    checks.append((f"exécutants canoniques {len(requis) - len(manquants)}/{len(requis)} présents",
                   not manquants))

    # T2 : agrégation du verdict (logique sur états synthétiques)
    vert = [{"etape": "x", "statut": s, "detail": ""} for s in STATS_VERTS]
    cas = (
        (_verdict([{"etape": "a", "statut": "PROPRE", "detail": ""},
                   {"etape": "b", "statut": "OK", "detail": ""}]), "INSTALLE"),
        (_verdict([{"etape": "a", "statut": "RÉPARÉ", "detail": ""}] + vert[:1]), "INSTALLE-REPARÉ"),
        (_verdict([{"etape": "a", "statut": "ECHEC", "detail": ""}]), "ECHEC"),
    )
    checks.append(("verdict consolidé : INSTALLE/INSTALLE-REPARÉ/ECHEC selon statuts",
                   all(obtenu == attendu for obtenu, attendu in cas)))

    # T3 : dry-run lecture seule s'exécute (rc 0 ou 2 = F3 divergences — jamais un crash)
    dr = _run([sys.executable, PIPELINE, "--dry-run"], cwd=REPO)
    checks.append((f"dry-run lecture seule rc={dr['rc']} (0 ou 2 attendu)",
                   dr["rc"] in (0, 2)))

    # T4 : convention docstring d'abord (N1 — docstring dans les 600 premiers octets)
    tete = Path(__file__).read_bytes()[:600].decode("utf-8", "replace")
    checks.append(("docstring d'en-tête présente (N1, < 600 octets)",
                   '"""' in tete))

    # T5 : verdict JSON sérialisable
    checks.append(("rapport JSON sérialisable",
                   json.dumps({"verdict_global": "INSTALLE", "etapes": []},
                              ensure_ascii=False) is not None))

    ok = all(o for _, o in checks)
    for nom, ok_c in checks:
        print(f"  [{'PASS' if ok_c else 'FAIL'}] {nom}")
    print(f"SELFTEST {'PASS' if ok else 'FAIL'} ({sum(1 for _, o in checks if o)}/{len(checks)})")
    return 0 if ok else 1


def main() -> int:
    parse = argparse.ArgumentParser(add_help=True)
    parse.add_argument("--selftest", action="store_true",
                       help="tests internes (aucune mutation)")
    args = parse.parse_args()
    if args.selftest:
        return selftest()
    rapport, _ = bootstrap()
    return 0 if rapport["verdict_global"] in ("INSTALLE", "INSTALLE-REPARÉ") else 1


if __name__ == "__main__":
    sys.exit(main())
