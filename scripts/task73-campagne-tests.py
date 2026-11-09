#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 73 — Campagne de tests fonctionnels et performances $FACON2.

Cibles :
  C1 — skill gen-plan hote (skills/gen-plan/)
  C2 — écosystème hôte (skills/)
  C3 — skill gen-plan du miroir (KNOWLEDGE-repo/skills/gen-plan/ + ancrages dépôt)

Le script ORCHESTRE les arbitres existants (R4 — jamais dupliquer) et MESURE
les durées. Aucune écriture corrective : la phase PRE capture l'état tel quel
(ensure-installed.py n'est volontairement PAS appelé par la campagne).

Usage :
  python3 scripts/task73-campagne-tests.py --protocole
  python3 scripts/task73-campagne-tests.py --phase pre  --cible C1|C2|C3|all
  python3 scripts/task73-campagne-tests.py --phase post --cible C1|C2|C3|all
  python3 scripts/task73-campagne-tests.py --synthese pre|post
  python3 scripts/task73-campagne-tests.py --selftest

Sorties (download/) :
  protocole-tests-fonctionnels-performances-task73.json
  rapport-campagne-task73-<phase>-<cible>.json
  rapport-campagne-task73-<phase>-synthese.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
HOTE = RACINE / "skills"
DEPOT = RACINE / "KNOWLEDGE-repo" / "skills"
DOWNLOAD = RACINE / "download"
GENPLAN_HOTE = HOTE / "gen-plan"
GENPLAN_DEPOT = DEPOT / "gen-plan"

VERSION_ATTENDUE = "3.39.0"
TAILLE_MAX_SKILL_MD = 30720  # 30 Kio — contrat D002 Task 72
REFERENCES_ATTENDUES = {
    "answer-key-b12.md", "answer-key-template.md", "classification-types.md",
    "disciplines-mobilisation.md", "etapes-detaillees.md",
    "graph-diamond-pattern.md", "grille-token.md",
    "guide-selection-agent-skill.md", "journal-versions.md",
    "observation-patterns.md", "patterns-avances-qwen.md",
    "profils-ressource.md", "prompt-engineering-kit.md",
    "protocoles-detailles.md", "regles-or.md",
}
CONTRATS_MOTIFS = [
    ("read_when", "read_when (lecture ciblée)"),
    ("FACON", "glossaire $FACON/$FACON2 inline §A"),
    ("SHARED", "§0 Contexte Système SHARED"),
    ("PATTERN:GEN-PLAN-HOOKS-PATTERNS", "bloc PATTERN E5-POIDS (contrat R2)"),
    ("fenêtre native", "E7-DISP point 6 fenêtre native (D015)"),
    ("TodoWrite", "mécanisme natif Z.ai liste de tâches"),
]
EVALS_ATTENDUS = 9
TRIGGER_EVALS_ATTENDUS = 15

RANG = {"PASS": 0, "PASS AVEC RÉSERVES": 1, "FAIL": 2}


def maintenant() -> str:
    """Horodatage UTC canonique."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def executer(cmd: list[str], timeout: int = 240) -> dict:
    """Exécute une commande, renvoie rc / sortie / durée ms."""
    debut = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                          cwd=str(RACINE))
    duree = round((time.perf_counter() - debut) * 1000, 1)
    sortie = (proc.stdout or "") + (proc.stderr or "")
    return {"rc": proc.returncode, "sortie": sortie, "duree_ms": duree}


def lire(chemin: Path) -> str:
    return chemin.read_text(encoding="utf-8", errors="replace")


def sha256(chemin: Path) -> str:
    import hashlib
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def resultat(ident: str, nom: str, verdict: str, duree_ms: float,
             details: str = "") -> dict:
    return {"id": ident, "nom": nom, "verdict": verdict,
            "duree_ms": duree_ms, "details": details[:1200]}


# ---------------------------------------------------------------------------
# Contexte partagé (une seule exécution de poids-chargement par invocation)
# ---------------------------------------------------------------------------

def poids_json(ctx: dict) -> dict | None:
    if "poids" not in ctx:
        rep = executer([sys.executable, "scripts/poids-chargement.py", "--json"])
        try:
            ctx["poids"] = json.loads(rep["sortie"])
            ctx["poids_duree"] = rep["duree_ms"]
        except json.JSONDecodeError:
            ctx["poids"] = None
            ctx["poids_duree"] = rep["duree_ms"]
    return ctx["poids"]


# ---------------------------------------------------------------------------
# C1 — skill gen-plan hôte
# ---------------------------------------------------------------------------

def tests_c1(ctx: dict) -> list[dict]:
    tests = []
    skill_md = GENPLAN_HOTE / "SKILL.md"
    texte = lire(skill_md)
    tete = "\n".join(texte.splitlines()[:14])

    # C1-F01 frontmatter
    debut = time.perf_counter()
    ok = ("name: gen-plan" in tete and f"version: {VERSION_ATTENDUE}" in tete
          and "language: fr" in tete)
    tests.append(resultat(
        "C1-F01", "frontmatter (name/version/language)", "PASS" if ok else "FAIL",
        round((time.perf_counter() - debut) * 1000, 1),
        f"version attendue {VERSION_ATTENDUE} ; en-tête : "
        + " | ".join(l.strip() for l in tete.splitlines() if l.strip())[:300]))

    # C1-F02 taille
    debut = time.perf_counter()
    taille = skill_md.stat().st_size
    ok = taille <= TAILLE_MAX_SKILL_MD
    tests.append(resultat(
        "C1-F02", "taille SKILL.md <= 30 Kio (contrat D002 Task 72)",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"{taille} octets = {taille / 1024:.2f} Kio (max {TAILLE_MAX_SKILL_MD})"))

    # C1-F03 references attendues
    debut = time.perf_counter()
    refs_dir = GENPLAN_HOTE / "references"
    reels = {p.name for p in refs_dir.iterdir() if p.is_file()}
    manquantes = sorted(REFERENCES_ATTENDUES - reels)
    inattendues = sorted(reels - REFERENCES_ATTENDUES)
    ok = not manquantes and not inattendues
    tests.append(resultat(
        "C1-F03", f"references/ : {len(REFERENCES_ATTENDUES)} fichiers attendus",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"réels {len(reels)} ; manquants {manquantes} ; inattendus {inattendues}"))

    # C1-F04 pointeurs (chaque fichier references/ cité dans SKILL.md)
    debut = time.perf_counter()
    non_cites = [r for r in sorted(REFERENCES_ATTENDUES)
                 if f"references/{r}" not in texte and r not in texte]
    tests.append(resultat(
        "C1-F04", "pointeurs : chaque fichier references/ cité dans SKILL.md",
        "PASS" if not non_cites else "FAIL",
        round((time.perf_counter() - debut) * 1000, 1),
        f"non cités : {non_cites}" if non_cites else "15/15 cités"))

    # C1-F05 contrats verbatim
    debut = time.perf_counter()
    lignes = []
    ok = True
    for motif, desc in CONTRATS_MOTIFS:
        n = texte.count(motif)
        lignes.append(f"{desc} : {n} occurrence(s)")
        if n < 1:
            ok = False
    tests.append(resultat(
        "C1-F05", "contrats verbatim intacts (baseline D005 + D015 Task 72)",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        " ; ".join(lignes)))

    # C1-F06 evals
    debut = time.perf_counter()
    try:
        ev = json.loads(lire(GENPLAN_HOTE / "evals" / "evals.json"))
        te = json.loads(lire(GENPLAN_HOTE / "evals" / "trigger_evals.json"))
        n_ev = len(ev.get("evals", []))
        n_te = len(te) if isinstance(te, list) else len(te.get("cas", []))
        ok = n_ev == EVALS_ATTENDUS and n_te == TRIGGER_EVALS_ATTENDUS
        det = f"evals.json {n_ev}/{EVALS_ATTENDUS} · trigger_evals.json {n_te}/{TRIGGER_EVALS_ATTENDUS}"
    except (json.JSONDecodeError, OSError) as exc:
        ok, det = False, f"lecture impossible : {exc}"
    tests.append(resultat(
        "C1-F06", "evals non-régression (9 cas + 15 triggers)",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1), det))

    # C1-F07 selftest check_plan_protocol
    # NB : les libellés de scénarios du selftest contiennent la chaîne « -> FAIL » ;
    # le critère est la ligne de résumé « RESUME : OK » + le code retour (harnais v2).
    rep = executer([sys.executable,
                    "skills/gen-plan/scripts/check_plan_protocol.py", "--selftest"])
    ok = rep["rc"] == 0 and "RESUME : OK" in rep["sortie"]
    tests.append(resultat(
        "C1-F07", "selftest check_plan_protocol.py (P1-P5 + scénarios)",
        "PASS" if ok else "FAIL", rep["duree_ms"],
        rep["sortie"].strip().splitlines()[-1][:200] if rep["sortie"].strip() else "silence"))

    # C1-F08 vérification re-curation (C1-C4) — critère : ligne « VERDICT : »
    rep = executer([sys.executable, "skills/re-curation/scripts/protocole-test.py",
                    "--verifier", "gen-plan"])
    ok = (rep["rc"] == 0 and "VERDICT : PASS" in rep["sortie"]
          and "ABANDON" not in rep["sortie"])
    tests.append(resultat(
        "C1-F08", "vérification re-curation (protocole-test.py --verifier : C1-C4)",
        "PASS" if ok else "FAIL", rep["duree_ms"],
        rep["sortie"].strip().splitlines()[-1][:300] if rep["sortie"].strip() else "silence"))

    # C1-F09 PM --check (4 familles)
    rep = executer([sys.executable, "scripts/generer-pm-skill.py", "--check"])
    nb_coherents = rep["sortie"].count("[COHERENT]")
    ok = rep["rc"] == 0 and nb_coherents == 4 and "DIVERGENT" not in rep["sortie"]
    tests.append(resultat(
        "C1-F09", "PM --check : 4 familles COHERENT (couverture PM v3.39.0)",
        "PASS" if ok else "FAIL", rep["duree_ms"],
        f"[COHERENT] x{nb_coherents} ; rc={rep['rc']}"))

    # C1-P01 poids gen-plan
    donnees = poids_json(ctx)
    if donnees is None:
        tests.append(resultat("C1-P01", "poids gen-plan (arbitre officiel)",
                              "FAIL", ctx.get("poids_duree", 0.0),
                              "sortie poids-chargement.py --json illisible"))
    else:
        ligne = next((m for m in donnees["mesures"] if m["skill"] == "gen-plan"), None)
        if ligne is None:
            verdict, det = "FAIL", "gen-plan absent des mesures"
        else:
            verdict = ("PASS" if ligne["verdict"] in ("OK", "INTERMÉDIAIRE")
                       and ligne["kio_skill_md"] < 30.0 else "FAIL")
            det = (f"{ligne['kio_skill_md']} Kio · {ligne['tokens_estimes']} #token · "
                   f"refs {ligne['kio_references']} Kio/{ligne['fichiers_references']} fichiers · "
                   f"verdict arbitre {ligne['verdict']}")
        tests.append(resultat("C1-P01", "poids gen-plan (arbitre officiel)",
                              verdict, ctx.get("poids_duree", 0.0), det))

    # C1-P02 durées agrégées (méta-test informationnel)
    total = round(sum(t["duree_ms"] for t in tests), 1)
    tests.append(resultat(
        "C1-P02", "durées agrégées C1 (performance temporelle)", "PASS", 0.0,
        f"total {total} ms sur {len(tests)} tests"))
    return tests


# ---------------------------------------------------------------------------
# C2 — écosystème hôte
# ---------------------------------------------------------------------------

def tests_c2(ctx: dict) -> list[dict]:
    tests = []

    # C2-F01 integrity
    rep = executer([sys.executable, "scripts/check-ecosysteme-integrity.py"])
    nb_fail = rep["sortie"].count("[FAIL]")
    verdict = "FAIL" if (nb_fail or rep["rc"] != 0) else "PASS"
    tests.append(resultat(
        "C2-F01", "arbitre integrity (corpus + archive + garde doublons + versions)",
        verdict, rep["duree_ms"],
        f"[FAIL] x{nb_fail} ; rc={rep['rc']} ; "
        + " | ".join(l.strip() for l in rep["sortie"].splitlines()
                     if "[FAIL]" in l)[:400]))

    # C2-F02 coherence (également source de la liste des entrées KB manquantes)
    rep = executer([sys.executable, "scripts/test-coherence-interactions.py"])
    nb_fail = rep["sortie"].count("[FAIL]")
    nb_warn = rep["sortie"].count("[WARN]")
    verdict = ("FAIL" if nb_fail else
               "PASS AVEC RÉSERVES" if nb_warn else "PASS")
    lignes_fail = [l.strip() for l in rep["sortie"].splitlines() if "[FAIL]" in l]
    lignes_warn = [l.strip() for l in rep["sortie"].splitlines() if "[WARN]" in l]
    ctx["coherence_fail"] = lignes_fail
    tests.append(resultat(
        "C2-F02", "arbitre coherence (KB versions + bidirectionnalité)",
        verdict, rep["duree_ms"],
        f"[FAIL] x{nb_fail} · [WARN] x{nb_warn} ; " + " | ".join(lignes_fail)[:400]
        + " || WARN : " + " | ".join(lignes_warn)[:400]))

    # C2-F03 vcw — mécanisme de cache de verdicts
    # NB : le wrapper EXIGE --cibles (fichiers suivis dont dépend le verdict) —
    # syntaxe calibrée : run -- <commande> --cibles <fichier suivi> (harnais v2).
    ok_cmds, det_cmds = 0, []
    for cmd, cible in ((["python3", "scripts/poids-chargement.py", "--json"],
                        "scripts/poids-chargement.py"),
                       (["python3", "scripts/verify-cross.py"],
                        "scripts/verify-cross.py")):
        rep = executer([sys.executable, "scripts/cache-verdicts.py", "run", "--"]
                       + cmd + ["--cibles", cible])
        if rep["rc"] == 0 and ("rc=" in rep["sortie"]
                               or '"version"' in rep["sortie"]
                               or "Score de conformité" in rep["sortie"]):
            ok_cmds += 1
        det_cmds.append(f"{' '.join(cmd[1:])} -> rc={rep['rc']} ({rep['duree_ms']} ms)")
    tests.append(resultat(
        "C2-F03", "vcw : mécanisme cache-verdicts fonctionnel (2 commandes)",
        "PASS" if ok_cmds == 2 else "FAIL", 0.0, " ; ".join(det_cmds)))

    # C2-F04 cross
    rep = executer([sys.executable, "scripts/verify-cross.py"])
    score, erreurs = None, None
    for ligne in rep["sortie"].splitlines():
        if "Score de conformité" in ligne:
            try:
                score = float(ligne.split(":")[1].strip().rstrip("%"))
            except (ValueError, IndexError):
                score = None
        if "ERRORS" in ligne:
            try:
                erreurs = int(ligne.split(":")[1].strip())
            except (ValueError, IndexError):
                erreurs = None
    ok = rep["rc"] == 0 and erreurs == 0 and score is not None and score >= 100.0
    tests.append(resultat(
        "C2-F04", "arbitre cross (conformité croisée)", "PASS" if ok else "FAIL",
        rep["duree_ms"], f"score {score} % · errors {erreurs} · rc={rep['rc']}"))

    # C2-F05 effectifs hôte vs miroir + entrées KB manquantes
    debut = time.perf_counter()
    hote = {p.name for p in HOTE.iterdir()
            if p.is_dir() and not p.name.startswith("@")}
    miroir = {p.name for p in DEPOT.iterdir()
              if p.is_dir() and not p.name.startswith("@")}
    en_trop = sorted(hote - miroir)
    kb_manquants = sorted(
        {m for m in miroir if m not in hote
         and any(m in l for l in ctx.get("coherence_fail", []))})
    verdict = "FAIL" if (en_trop or kb_manquants) else "PASS"
    tests.append(resultat(
        "C2-F05", "effectifs : hôte ⊆ miroir + entrées KB présentes",
        verdict, round((time.perf_counter() - debut) * 1000, 1),
        f"hôte {len(hote)} · miroir {len(miroir)} · en trop {en_trop} · "
        f"KB manquants {kb_manquants or 'aucun'}"))

    # C2-F06 sweep citations v3.38.0 (WARN à adjudication manuelle)
    debut = time.perf_counter()
    citations = []
    for p in HOTE.glob("*/SKILL.md"):
        if p.name == "SKILL.md" and "v3.38.0" in lire(p):
            citations.append(p.parent.name)
    verdict = "PASS AVEC RÉSERVES" if citations else "PASS"
    tests.append(resultat(
        "C2-F06", "sweep citations « v3.38.0 » dans les SKILL.md",
        verdict, round((time.perf_counter() - debut) * 1000, 1),
        f"skills concernés : {citations}" if citations else "0 citation résiduelle"))

    # C2-F07 ancrage corpus ULTRA (hôte + dépôt)
    debut = time.perf_counter()
    ultra_h = HOTE / "@mon-ecosysteme" / "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"
    ultra_d = DEPOT / "@mon-ecosysteme" / "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"
    ok = ultra_h.exists() and ultra_d.exists() and sha256(ultra_h) == sha256(ultra_d)
    tests.append(resultat(
        "C2-F07", "ancrage corpus : ULTRA présent et identique hôte/dépôt",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"SHA {sha256(ultra_h)[:16]}… (hôte) vs {sha256(ultra_d)[:16]}… (dépôt)"
        if ok else "fichier absent ou divergent"))

    # C2-P01 poids global
    donnees = poids_json(ctx)
    if donnees is None:
        tests.append(resultat("C2-P01", "poids global écosystème", "FAIL", 0.0,
                              "sortie poids-chargement.py --json illisible"))
    else:
        st = donnees["stats"]
        ok = st["critique"] == 0
        tests.append(resultat(
            "C2-P01", "poids global écosystème (0 CRITIQUE attendu)",
            "PASS" if ok else "FAIL", ctx.get("poids_duree", 0.0),
            f"{st['nb_skills']} skills · OK {st['ok']} · intermédiaires "
            f"{st['intermediaire']} · LOURD {st['lourd']} · CRITIQUE {st['critique']}"))

    total = round(sum(t["duree_ms"] for t in tests), 1)
    tests.append(resultat(
        "C2-P02", "durées agrégées C2 (performance temporelle)", "PASS", 0.0,
        f"total {total} ms sur {len(tests)} tests"))
    return tests


# ---------------------------------------------------------------------------
# C3 — skill gen-plan du miroir
# ---------------------------------------------------------------------------

def tests_c3(ctx: dict) -> list[dict]:
    tests = []

    # C3-F01 identité byte hôte <-> miroir
    rep = executer(["diff", "-rq", str(GENPLAN_HOTE), str(GENPLAN_DEPOT)])
    ok = rep["rc"] == 0 and not rep["sortie"].strip()
    tests.append(resultat(
        "C3-F01", "identité byte gen-plan hôte <-> miroir (diff -rq)",
        "PASS" if ok else "FAIL", rep["duree_ms"],
        "arborescences identiques (SKILL.md + references + scripts + evals)"
        if ok else rep["sortie"].strip()[:400]))

    # C3-F02 frontmatter + taille miroir
    debut = time.perf_counter()
    skill_md = GENPLAN_DEPOT / "SKILL.md"
    texte = lire(skill_md)
    tete = "\n".join(texte.splitlines()[:14])
    taille_h = (GENPLAN_HOTE / "SKILL.md").stat().st_size
    taille_d = skill_md.stat().st_size
    ok = (f"version: {VERSION_ATTENDUE}" in tete and taille_h == taille_d)
    tests.append(resultat(
        "C3-F02", "miroir : frontmatter v3.39.0 + taille identique à l'hôte",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"dépôt {taille_d} o vs hôte {taille_h} o"))

    # C3-F03 PM v3.39.0 identique
    debut = time.perf_counter()
    pm_h = HOTE / "@mon-ecosysteme" / "PROMPT-MAITRE-GEN-PLAN-v3.39.0.md"
    pm_d = DEPOT / "@mon-ecosysteme" / "PROMPT-MAITRE-GEN-PLAN-v3.39.0.md"
    ok = pm_h.exists() and pm_d.exists() and sha256(pm_h) == sha256(pm_d)
    tests.append(resultat(
        "C3-F03", "PM v3.39.0 identique hôte/dépôt (SHA-256)",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"SHA {sha256(pm_h)[:16]}… · {pm_h.stat().st_size} o" if ok else "absent ou divergent"))

    # C3-F04 KB « montée v3.39.0 » des deux côtés
    debut = time.perf_counter()
    n_h = lire(HOTE / "KNOWLEDGE.md").count("montée v3.39.0")
    n_d = lire(DEPOT / "KNOWLEDGE.md").count("montée v3.39.0")
    ok = n_h >= 1 and n_d >= 1
    tests.append(resultat(
        "C3-F04", "KB : calibration « montée v3.39.0 » hôte + dépôt",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"occurrences : hôte {n_h} · dépôt {n_d}"))

    # C3-F05 historiques gen-plan v3.39.0 des deux côtés
    debut = time.perf_counter()
    n_h = lire(HOTE / "@historique" / "historiques-par-skill" / "gen-plan.md").count("v3.39.0")
    n_d = lire(DEPOT / "@historique" / "historiques-par-skill" / "gen-plan.md").count("v3.39.0")
    ok = n_h >= 1 and n_d >= 1
    tests.append(resultat(
        "C3-F05", "historiques-par-skill gen-plan : entrée v3.39.0 hôte + dépôt",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"occurrences : hôte {n_h} · dépôt {n_d}"))

    # C3-F06 ULTRA identique (ancrage orchestration)
    debut = time.perf_counter()
    ultra_h = HOTE / "@mon-ecosysteme" / "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"
    ultra_d = DEPOT / "@mon-ecosysteme" / "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"
    ok = ultra_h.exists() and ultra_d.exists() and sha256(ultra_h) == sha256(ultra_d)
    tests.append(resultat(
        "C3-F06", "ULTRA orchestration identique hôte/dépôt (SHA-256)",
        "PASS" if ok else "FAIL", round((time.perf_counter() - debut) * 1000, 1),
        f"SHA {sha256(ultra_h)[:16]}…" if ok else "absent ou divergent"))

    total = round(sum(t["duree_ms"] for t in tests), 1)
    tests.append(resultat(
        "C3-P01", "durées agrégées C3 (performance temporelle)", "PASS", 0.0,
        f"total {total} ms sur {len(tests)} tests"))
    return tests


# ---------------------------------------------------------------------------
# Agrégation, comparaison, protocole, synthèse
# ---------------------------------------------------------------------------

def agreger(tests: list[dict]) -> str:
    """Verdict d'une cible : pire des verdicts de ses tests."""
    pire = "PASS"
    for t in tests:
        if RANG[t["verdict"]] > RANG[pire]:
            pire = t["verdict"]
    return pire


def construire_protocole() -> dict:
    """Description du protocole (source unique, exportée en JSON)."""
    return {
        "format": "protocole-tests-task73 v1.0.0",
        "horodatage": maintenant(),
        "mission": ("tests $FACON2 fonctionnels et performances sur C1 gen-plan hôte, "
                    "C2 écosystème hôte, C3 gen-plan miroir — corriger $FACON les failles, "
                    "optimiser le fonctionnement et les interactions"),
        "aliases": {"FACON": "de façon cohérente, optimisée et fonctionnelle",
                    "FACON2": "(cohérent, optimisé et fonctionnel)"},
        "cibles": {
            "C1": {"chemin": "skills/gen-plan/",
                   "fonctionnels": ["C1-F01 frontmatter", "C1-F02 taille <= 30 Kio",
                                    "C1-F03 15 references", "C1-F04 pointeurs",
                                    "C1-F05 contrats verbatim", "C1-F06 evals 9+15",
                                    "C1-F07 selftest plan", "C1-F08 re-curation C1-C4",
                                    "C1-F09 PM --check 4 familles"],
                   "performances": ["C1-P01 poids arbitre officiel",
                                    "C1-P02 durées agrégées"]},
            "C2": {"chemin": "skills/",
                   "fonctionnels": ["C2-F01 integrity", "C2-F02 coherence",
                                    "C2-F03 vcw mécanisme", "C2-F04 cross",
                                    "C2-F05 effectifs hôte ⊆ miroir + KB",
                                    "C2-F06 sweep v3.38.0", "C2-F07 ULTRA"],
                   "performances": ["C2-P01 poids global 0 CRITIQUE",
                                    "C2-P02 durées agrégées"]},
            "C3": {"chemin": "KNOWLEDGE-repo/skills/gen-plan/",
                   "fonctionnels": ["C3-F01 diff -rq vide", "C3-F02 frontmatter+taille",
                                    "C3-F03 PM SHA", "C3-F04 KB montée v3.39.0",
                                    "C3-F05 historiques v3.39.0", "C3-F06 ULTRA SHA"],
                   "performances": ["C3-P01 durées agrégées"]},
        },
        "criteres_verdict": {
            "echelle": "PASS < PASS AVEC RÉSERVES < FAIL",
            "agregation": "pire des verdicts par cible, puis pire des cibles",
            "tolerances": {
                "C2-F02 WARN B1": "WARN légitime hérité (artefact historique) toléré — verdict PASS AVEC RÉSERVES",
                "C2-F06": "citation v3.38.0 = WARN à adjudication manuelle (contexte historique possible)",
            },
        },
        "phases": {
            "pre": "capture de l'état réel SANS aucune correction (ensure-installed non appelé)",
            "post": "re-exécution intégrale après corrections (G5)",
            "non_regression": "aucun verdict dégradé test à test entre PRE et POST",
        },
        "reutilisation_R4": ["check-ecosysteme-integrity.py", "test-coherence-interactions.py",
                             "cache-verdicts.py", "verify-cross.py", "poids-chargement.py",
                             "re-curation/protocole-test.py", "re-curation/check-recuration.py",
                             "gen-plan/check_plan_protocol.py", "generer-pm-skill.py --check"],
    }


def comparer(pre: dict, post: dict) -> dict:
    """Comparaison test à test PRE -> POST."""
    pre_par_id = {t["id"]: t["verdict"] for t in pre["tests"]}
    degradations, ameliorations, resorbees = [], [], []
    for t in post["tests"]:
        avant = pre_par_id.get(t["id"])
        if avant is None:
            continue
        if RANG[t["verdict"]] > RANG[avant]:
            degradations.append(f"{t['id']} : {avant} -> {t['verdict']}")
        elif RANG[t["verdict"]] < RANG[avant]:
            ameliorations.append(f"{t['id']} : {avant} -> {t['verdict']}")
            if avant == "FAIL":
                resorbees.append(t["id"])
    return {"cible": post["cible"], "verdict_pre": pre["verdict"],
            "verdict_post": post["verdict"],
            "degradations": degradations, "ameliorations": ameliorations,
            "failles_resorbees": resorbees,
            "non_regression": not degradations}


def synthese(phase: str) -> int:
    cmps, verdicts = [], {}
    for cible in ("C1", "C2", "C3"):
        try:
            pre = json.loads(lire(DOWNLOAD / f"rapport-campagne-task73-pre-{cible}.json"))
            post = json.loads(lire(DOWNLOAD / f"rapport-campagne-task73-post-{cible}.json"))
        except OSError:
            print(f"[ABANDON] fichiers manquants pour {cible} (phase {phase})")
            return 2
        cmps.append(comparer(pre, post))
        verdicts[cible] = {"pre": pre["verdict"], "post": post["verdict"]}
    # Harnais v2 : le verdict global POST n'agrège QUE les verdicts POST
    # (le pire examiné côté PRE est une information, pas le verdict de sortie).
    pire_post = "PASS"
    pire_pre = "PASS"
    for c in cmps:
        if RANG[c["verdict_post"]] > RANG[pire_post]:
            pire_post = c["verdict_post"]
        if RANG[c["verdict_pre"]] > RANG[pire_pre]:
            pire_pre = c["verdict_pre"]
    non_regression_globale = all(c["non_regression"] for c in cmps)
    sortie = {
        "format": "synthese-campagne-task73 v1.0.1", "phase": phase,
        "horodatage": maintenant(), "cibles": verdicts,
        "comparaisons": cmps,
        "non_regression": non_regression_globale,
        "failles_resorbees": [f for c in cmps for f in c["failles_resorbees"]],
        "verdict_global_pre": pire_pre,
        "verdict_global_post": pire_post,
    }
    chemin = DOWNLOAD / f"rapport-campagne-task73-{phase}-synthese.json"
    chemin.write_text(json.dumps(sortie, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"[SYNTHÈSE {phase}] verdict global POST : {pire_post} (PRE : {pire_pre}) · "
          f"non-régression : {non_regression_globale} · "
          f"failles résorbées : {sortie['failles_resorbees']}")
    print(f"  -> {chemin}")
    return 0


def campagne(phase: str, cible: str) -> int:
    ctx: dict = {}
    cibles = ["C1", "C2", "C3"] if cible == "all" else [cible]
    rc = 0
    for c in cibles:
        debut = time.perf_counter()
        tests = {"C1": tests_c1, "C2": tests_c2, "C3": tests_c3}[c](ctx)
        duree = round((time.perf_counter() - debut) * 1000, 1)
        verdict = agreger(tests)
        sortie = {"format": "campagne-task73 v1.0.0", "phase": phase, "cible": c,
                  "horodatage": maintenant(), "duree_totale_ms": duree,
                  "verdict": verdict, "tests": tests}
        chemin = DOWNLOAD / f"rapport-campagne-task73-{phase}-{c}.json"
        chemin.write_text(json.dumps(sortie, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
        nb = {v: sum(1 for t in tests if t["verdict"] == v) for v in RANG}
        print(f"[{phase} {c}] verdict : {verdict} — "
              f"PASS {nb['PASS']} · RÉSERVES {nb['PASS AVEC RÉSERVES']} · FAIL {nb['FAIL']} "
              f"({duree} ms)")
        for t in tests:
            if t["verdict"] != "PASS":
                print(f"    {t['verdict']} : {t['id']} {t['nom']} — {t['details'][:120]}")
        print(f"  -> {chemin}")
        if verdict == "FAIL":
            rc = 1
    return rc


def selftest() -> int:
    """Auto-vérification intégrée (logique pure, aucun effet de bord)."""
    resultats = []

    def check(nom, obtenu, attendu):
        resultats.append((nom, obtenu == attendu, f"obtenu={obtenu!r} attendu={attendu!r}"))

    check("T1 échelle de verdicts ordonnée", RANG["FAIL"] > RANG["PASS AVEC RÉSERVES"] > RANG["PASS"], True)
    check("T2 agrégation pire-des-verdicts",
          agreger([{"verdict": "PASS"}, {"verdict": "FAIL"}, {"verdict": "PASS"}]), "FAIL")
    check("T3 agrégation toutes PASS", agreger([{"verdict": "PASS"}]), "PASS")
    faux_pre = {"cible": "X", "verdict": "FAIL",
                "tests": [{"id": "a", "verdict": "FAIL"}, {"id": "b", "verdict": "PASS"}]}
    faux_post = {"cible": "X", "verdict": "PASS",
                 "tests": [{"id": "a", "verdict": "PASS"}, {"id": "b", "verdict": "PASS"}]}
    comp = comparer(faux_pre, faux_post)
    check("T4 faille résorbée détectée", comp["failles_resorbees"], ["a"])
    check("T5 non-régression sans dégradation", comp["non_regression"], True)
    faux_post2 = {"cible": "X", "verdict": "FAIL",
                  "tests": [{"id": "a", "verdict": "PASS"}, {"id": "b", "verdict": "FAIL"}]}
    check("T6 dégradation détectée", comparer(faux_pre, faux_post2)["non_regression"], False)
    protocole = construire_protocole()
    check("T7 protocole : 3 cibles décrites",
          sorted(protocole["cibles"].keys()), ["C1", "C2", "C3"])
    check("T8 réutilisation R4 : 9 arbitres listés", len(protocole["reutilisation_R4"]), 9)

    nb_ok = sum(1 for _, ok, _ in resultats if ok)
    print(f"SELFTEST task73-campagne-tests : {nb_ok}/{len(resultats)} PASS")
    for nom, ok, det in resultats:
        print(f"  [{'PASS' if ok else 'FAIL'}] {nom}" + ("" if ok else f" — {det}"))
    return 0 if nb_ok == len(resultats) else 1


def main() -> int:
    parseur = argparse.ArgumentParser(
        description="Task 73 — campagne de tests fonctionnels et performances")
    parseur.add_argument("--phase", choices=["pre", "post"])
    parseur.add_argument("--cible", choices=["C1", "C2", "C3", "all"], default="all")
    parseur.add_argument("--synthese", choices=["pre", "post"])
    parseur.add_argument("--protocole", action="store_true")
    parseur.add_argument("--selftest", action="store_true")
    args = parseur.parse_args()

    if args.selftest:
        return selftest()
    if args.protocole:
        chemin = DOWNLOAD / "protocole-tests-fonctionnels-performances-task73.json"
        chemin.write_text(json.dumps(construire_protocole(), ensure_ascii=False,
                                     indent=2) + "\n", encoding="utf-8")
        print(f"[PROTOCOLE] exporté -> {chemin}")
        return 0
    if args.synthese:
        return synthese(args.synthese)
    if args.phase:
        return campagne(args.phase, args.cible)
    parseur.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
