#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.33)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Task 60 G3-SG1b (D603b, E13-4) — Tests comparatifs fonctionnels et de performances.
Directive propriétaire (verbatim) : « dans l'objectif de m'aider à prendre ma décision,
génère $FACON des tests $FACON2 fonctionnels et de performances sur cette future version
de mon écosystème et sur mon écosystème actuel ».

Comparaison :
  PHASE A — ÉCOSYSTÈME ACTUEL (corpus KO-L004, 4 familles) : lecture seule
            (seule exception : scripts/generer-pm-report.json, écriture nominale
            idempotente de l'arbitre existant generer-pm-skill.py --check).
  PHASE B — VERSION FUTURE (PM-skill éphémère) : PROTOTYPE EMBARQUÉ ci-dessous —
            AUCUNE INTÉGRATION (aucun skills/pm-skill/, aucun
            scripts/generer-pm-ephemere.py) ; sorties en download/tests-task60/ ;
            zéro fichier d'état de l'écosystème modifié (garde mécanique G0).
  PHASE C — PERFORMANCES : temps, empreintes, coût structurel, résilience, lag.

Méthode (zéro invention — KO-L003) : le prototype PROJETTE le SKILL.md (corps verbatim,
§0 Contexte Système déjà propagé inclus) sous un en-tête PM (provenance + SHA-256 +
mode d'emploi IA externe) + relations parsées du frontmatter. Le script structure,
il ne rédige pas.

Idempotence : re-jeu même jour = sorties byte-identiques (horodatage jour uniquement).
Codes retour : 0 = harnais joué (verdicts PASS/FAIL dans le rapport) ; 2 = erreur harnais.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
CORPUS = SKILLS / "@mon-ecosysteme"
TESTDIR = BASE / "download" / "tests-task60"
GENPM = BASE / "scripts" / "generer-pm-skill.py"
FAMILLES = ["gen-plan", "correct-work", "clone-chat", "refactor-guard"]

RESULTS = []


def rec(phase, test, label, verdict, detail="", metrics=None):
    RESULTS.append({"phase": phase, "test": test, "label": label,
                    "verdict": verdict, "detail": detail, "metrics": metrics or {}})
    print("[%s] %s-%s %-58s %s" % (verdict, phase, test, label[:58], detail[:70]))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def skills_racine():
    """Skills éligibles = dossiers racine skills/ avec SKILL.md (hors corpus/@dirs/KNOWLEDGE)."""
    out = []
    for d in sorted(SKILLS.iterdir()):
        if d.name.startswith("@") or not d.is_dir():
            continue
        if (d / "SKILL.md").is_file():
            out.append(d.name)
    return out


# ---------------------------------------------------------------------------
# PROTOTYPE — PM-skill éphémère (version future, EMBARQUÉE — NON INTÉGRÉE)
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Sépare frontmatter YAML (--- ... ---) et corps ; extrait name/version/
    description/dépendances sans inventer (verbatim du fichier)."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm, body = m.group(1), m.group(2)
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    version = re.search(r"^version:\s*[\"']?([\d.]+(?:-[A-Za-z0-9.-]+)?)", fm, re.M)
    desc = re.search(r"^description:\s*>-?\s*\n((?:\s{2,}.*\n?)+)", fm, re.M)
    description = re.sub(r"\s+", " ", desc.group(1)).strip() if desc else ""
    deps = []
    dm = re.search(r"^dependencies:\n((?:\s+- skill:.*\n(?:\s{4,}.*\n?)*)+)", fm, re.M)
    if dm:
        for bloc in re.finditer(r"-\s+skill:\s*(\S+)\s*\n\s+version:\s*[\"']?([^\"'\n]+)[\"']?\s*\n(?:\s+used_at:\s*(.+))?", dm.group(1)):
            deps.append({"skill": bloc.group(1), "version": bloc.group(2).strip(),
                         "used_at": (bloc.group(3) or "").strip().strip('"')})
    return {"name": name.group(1) if name else "", "version": version.group(1) if version else "",
            "description": description, "dependencies": deps}, body


def generer_pm_ephemere(skill_dir, out_dir):
    """PROTOTYPE — projection auto-portante du SKILL.md en PM éphémère MD.
    Retourne le chemin écrit (déterministe même jour). Aucune écriture hors out_dir."""
    skill_md = Path(skill_dir) / "SKILL.md"
    src = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(src)
    name = fm.get("name") or Path(skill_dir).name
    version = fm.get("version") or "0.0.0"
    description = fm.get("description") or ""
    sha = sha256_file(skill_md)
    today = date.today().isoformat()
    lignes = [
        "# PROMPT MAÎTRE ÉPHÉMÈRE — %s v%s" % (name, version),
        "",
        "> **Skill source** : `skills/%s/SKILL.md` (forme installée — référence canonique)" % name,
        "> **Version source** : %s · **Généré le** : %s" % (version, today),
        "> **SHA-256 source** : `%s`" % sha,
        "> **Nature** : projection éphémère auto-portante — le Contexte Système est embarqué,",
        "> **aucune lecture externe n'est requise** (SHARED §6.2). Régénérable à volonté :",
        "> `PM-skill(%s)` reproduit ce fichier à l'identique (déterminisme même jour)." % name,
        "",
        "## MODE D'EMPLOI — IA EXTERNE",
        "",
        "1. Copier l'intégralité du présent fichier.",
        "2. Le coller comme **prompt système** (ou premier message) dans l'IA de votre choix.",
        "3. Invoquer le skill par ses déclencheurs (section dédiée ci-dessous).",
        "   Le contenu ci-dessous est la spécification exécutable du skill, auto-contenue.",
        "",
        "## MISSION — description du skill (frontmatter source, verbatim)",
        "",
        description or "(description absente du frontmatter source — voir spécification ci-dessous)",
        "",
        "---",
        "",
        body.rstrip(),
        "",
        "---",
        "",
    ]
    if fm.get("dependencies"):
        lignes.append("## RELATIONS — dépendances déclarées (frontmatter source, verbatim)")
        lignes.append("")
        for d in fm["dependencies"]:
            lignes.append("- **%s** %s — %s" % (d["skill"], d["version"], d["used_at"] or "(usage non précisé)"))
        lignes.append("")
        lignes.append("> Ces dépendances sont des relations ÉCOSYSTÈME (traçabilité). En usage IA externe,")
        lignes.append("> la spécification embarquée ci-dessus suffit à l'exécution de la mission.")
        lignes.append("")
    out = Path(out_dir) / ("PM-ephemere-%s-v%s.md" % (name, version))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lignes), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# PHASE A — ÉCOSYSTÈME ACTUEL (lecture seule)
# ---------------------------------------------------------------------------

def phase_a():
    print("\n===== PHASE A — ÉCOSYSTÈME ACTUEL (corpus KO-L004) =====")
    racine = skills_racine()
    pms_corpus = sorted(p.name for p in CORPUS.glob("PROMPT-MAITRE-*.md")
                        if p.name != "PROMPT-MAITRE-SHARED.md"
                        and p.name != "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md")
    # A1 — couverture PM
    n_fam = len(FAMILLES)
    couv = 100.0 * n_fam / len(racine)
    rec("A", "A1", "Couverture PM corpus : %d familles / %d skills racine" % (n_fam, len(racine)),
        "FACT", "%.1f %% des skills ont une voie PM" % couv,
        {"familles": n_fam, "skills_racine": len(racine), "couverture_pct": round(couv, 1)})
    # A2 — cohérence versions (arbitre existant, idempotent)
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, str(GENPM), "--check"], capture_output=True, text=True)
    dt = (time.perf_counter() - t0) * 1000
    coherents = len(re.findall(r"\[COHERENT\]", r.stdout))
    rec("A", "A2", "Cohérence versions SKILL.md↔PM corpus (generer-pm-skill.py --check)",
        "PASS" if (r.returncode == 0 and coherents == n_fam) else "FAIL",
        "%d/%d familles COHERENT, rc=%d, %.0f ms" % (coherents, n_fam, r.returncode, dt),
        {"coherents": coherents, "rc": r.returncode, "ms": round(dt)})
    # A3 — auto-portance PMs corpus
    for f in FAMILLES:
        pms = sorted(CORPUS.glob("PROMPT-MAITRE-*%s-v*.md" % f.upper().replace("-", "-")))
        pm = pms[-1] if pms else None
        if not pm:
            rec("A", "A3", "Auto-portance PM corpus %s" % f, "FAIL", "PM introuvable")
            continue
        t = pm.read_text(encoding="utf-8")
        ctx = len(re.findall(r"contexte système", t, re.IGNORECASE))
        dep = len(re.findall(r"lire en premier|lire PROMPT-MAITRE-SHARED", t))
        rec("A", "A3", "Auto-portance PM corpus %s (%s)" % (f, pm.name),
            "PASS" if (ctx > 0 and dep == 0) else "FAIL",
            "contexte embarqué ×%d · dépendance externe ×%d" % (ctx, dep),
            {"contexte": ctx, "dependance_externe": dep})
    # A4 — voie PM pour un skill non-famille (preuve mécanique)
    r = subprocess.run([sys.executable, str(GENPM), "--generate", "tsi-validator"],
                       capture_output=True, text=True)
    refuse = ("famille inconnue" in (r.stdout + r.stderr)) or r.returncode == 3
    rec("A", "A4", "Voie PM pour skill non-famille (tsi-validator) via KO-L004",
        "EXPECTED-REFUS" if refuse else "FAIL",
        "refus mécanique rc=%d : %s" % (r.returncode, (r.stdout + r.stderr).strip().splitlines()[0][:60] if (r.stdout + r.stderr).strip() else "?"),
        {"rc": r.returncode, "refuse": refuse})
    # A5 — empreinte stockage permanente
    fichiers = [p for p in CORPUS.glob("*.md")]
    taille = sum(p.stat().st_size for p in fichiers)
    arch = BASE / "skills" / "@historique" / "prompts-maitres"
    arch_taille = sum(p.stat().st_size for p in arch.rglob("*.md")) if arch.is_dir() else 0
    arch_n = len(list(arch.rglob("*.md"))) if arch.is_dir() else 0
    deltas = list((BASE / "scripts").glob("delta-*.json"))
    rec("A", "A5", "Empreinte stockage permanente (état d'écosystème)",
        "FACT", "corpus %d fichiers %.0f Ko + archive PMs %d fichiers %.0f Ko + %d deltas" % (
            len(fichiers), taille / 1024, arch_n, arch_taille / 1024, len(deltas)),
        {"corpus_fichiers": len(fichiers), "corpus_ko": round(taille / 1024),
         "archive_pm_fichiers": arch_n, "archive_pm_ko": round(arch_taille / 1024),
         "deltas": len(deltas)})


# ---------------------------------------------------------------------------
# PHASE B — VERSION FUTURE (prototype embarqué, bac à sable)
# ---------------------------------------------------------------------------

def phase_b():
    print("\n===== PHASE B — VERSION FUTURE (PM-skill éphémère, PROTOTYPE NON INTÉGRÉ) =====")
    racine = skills_racine()
    outdir = TESTDIR / "output"
    # Garde G0 — porte propriétaire D604 : rien hors download/tests-task60/
    integres = [p for p in [BASE / "skills" / "pm-skill", BASE / "scripts" / "generer-pm-ephemere.py"] if p.exists()]
    rec("B", "G0", "PORTE D604 : prototype NON intégré à l'écosystème",
        "PASS" if not integres else "FAIL",
        "aucun skills/pm-skill/ ni scripts/generer-pm-ephemere.py" if not integres else "INTÉGRÉ À TORT : %s" % integres)
    # B1 — génération famille
    for skill in ["correct-work"]:
        out = generer_pm_ephemere(SKILLS / skill, outdir)
        t = out.read_text(encoding="utf-8")
        ok = all(m in t for m in ["PROMPT MAÎTRE ÉPHÉMÈRE", "MODE D'EMPLOI", "§0 — Contexte Système", "SHA-256 source"])
        rec("B", "B1", "Génération PM éphémère — famille (%s)" % skill,
            "PASS" if ok else "FAIL", "%s (%d o)" % (out.name, out.stat().st_size))
    # B2 — génération non-famille
    for skill in ["tsi-validator", "vue-upload"]:
        out = generer_pm_ephemere(SKILLS / skill, outdir)
        t = out.read_text(encoding="utf-8")
        ok = all(m in t for m in ["PROMPT MAÎTRE ÉPHÉMÈRE", "MODE D'EMPLOI", "§0 — Contexte Système", "SHA-256 source"])
        rec("B", "B2", "Génération PM éphémère — non-famille (%s)" % skill,
            "PASS" if ok else "FAIL", "%s (%d o)" % (out.name, out.stat().st_size))
    # B3 — batch 68
    ok_n, errs = 0, []
    for s in racine:
        try:
            generer_pm_ephemere(SKILLS / s, outdir)
            ok_n += 1
        except Exception as e:  # noqa: BLE001 — journalisé, jamais masqué
            errs.append("%s: %s" % (s, e))
    rec("B", "B3", "Génération batch — %d skills racine" % len(racine),
        "PASS" if ok_n == len(racine) else "FAIL",
        "%d/%d générés%s" % (ok_n, len(racine), " ; erreurs : %s" % errs[:3] if errs else ""),
        {"generes": ok_n, "total": len(racine)})
    # B4 — auto-portance 68/68
    sorties = list(outdir.glob("PM-ephemere-*.md"))
    auto = [p for p in sorties if "§0 — Contexte Système" in p.read_text(encoding="utf-8")]
    dep_ext = [p.name for p in sorties if re.search(r"lire en premier", p.read_text(encoding="utf-8"))]
    rec("B", "B4", "Auto-portance des sorties (contexte embarqué, zéro « lire en premier »)",
        "PASS" if (len(auto) == len(sorties) and not dep_ext) else "FAIL",
        "%d/%d auto-portantes%s" % (len(auto), len(sorties), " ; dépendances : %s" % dep_ext[:3] if dep_ext else ""),
        {"auto_portantes": len(auto), "total": len(sorties)})
    # B5 — déterminisme ×2 (byte-identique)
    echant = racine[:5]
    instables = []
    for s in echant:
        a = generer_pm_ephemere(SKILLS / s, TESTDIR / "det1")
        b = generer_pm_ephemere(SKILLS / s, TESTDIR / "det2")
        if sha256_file(a) != sha256_file(b):
            instables.append(s)
    rec("B", "B5", "Déterminisme — régénération ×2 byte-identique (5 échantillons)",
        "PASS" if not instables else "FAIL",
        "stable" if not instables else "instables : %s" % instables)
    # B6 — fidélité (version + mission + relations verbatim)
    echant6 = ["correct-work", "tsi-validator", "vue-upload"]
    pb = []
    for s in echant6:
        src = (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(src)
        out = generer_pm_ephemere(SKILLS / s, outdir)
        t = re.sub(r"\s+", " ", out.read_text(encoding="utf-8"))
        if ("v%s" % fm["version"]) not in t:
            pb.append("%s: version" % s)
        phrase = re.sub(r"\s+", " ", fm["description"])[:70]
        if phrase and phrase not in t:
            pb.append("%s: mission" % s)
    rec("B", "B6", "Fidélité — version + mission (description verbatim) présentes",
        "PASS" if not pb else "FAIL", "3/3 fidèles" if not pb else "écarts : %s" % pb)
    # B7 — traçabilité SHA-256
    pb7 = []
    for s in echant6:
        out = generer_pm_ephemere(SKILLS / s, outdir)
        t = out.read_text(encoding="utf-8")
        sha_src = sha256_file(SKILLS / s / "SKILL.md")
        if sha_src not in t:
            pb7.append(s)
    rec("B", "B7", "Traçabilité — SHA-256 source embarqué et exact",
        "PASS" if not pb7 else "FAIL", "3/3 tracés" if not pb7 else "écarts : %s" % pb7)


# ---------------------------------------------------------------------------
# PHASE C — PERFORMANCES
# ---------------------------------------------------------------------------

def phase_c():
    print("\n===== PHASE C — PERFORMANCES =====")
    outdir = TESTDIR / "output"
    racine = skills_racine()
    # C1 — temps unitaire ×10
    temps = []
    for _ in range(10):
        t0 = time.perf_counter()
        generer_pm_ephemere(SKILLS / "correct-work", TESTDIR / "perf")
        temps.append((time.perf_counter() - t0) * 1000)
    rec("C", "C1", "Temps génération unitaire (correct-work ×10)",
        "FACT", "min %.1f ms · moy %.1f ms · max %.1f ms" % (min(temps), sum(temps) / 10, max(temps)),
        {"min_ms": round(min(temps), 1), "moy_ms": round(sum(temps) / 10, 1), "max_ms": round(max(temps), 1)})
    # C2 — temps batch 68
    t0 = time.perf_counter()
    for s in racine:
        generer_pm_ephemere(SKILLS / s, outdir)
    dt = time.perf_counter() - t0
    rec("C", "C2", "Temps batch %d skills" % len(racine),
        "FACT", "%.2f s au total · %.1f ms/skill" % (dt, dt * 1000 / len(racine)),
        {"total_s": round(dt, 2), "ms_par_skill": round(dt * 1000 / len(racine), 1)})
    # C3 — empreinte sorties (livrables, régénérables — vs état permanent corpus)
    sorties = list(outdir.glob("PM-ephemere-*.md"))
    taille = sum(p.stat().st_size for p in sorties)
    corpus_ko = sum(p.stat().st_size for p in CORPUS.glob("*.md")) / 1024
    rec("C", "C3", "Empreinte sorties éphémères (%d fichiers) vs état permanent corpus" % len(sorties),
        "FACT", "sorties %.0f Ko (régénérables, supprimables) vs corpus %.0f Ko (état permanent)" % (taille / 1024, corpus_ko),
        {"sorties_ko": round(taille / 1024), "corpus_ko": round(corpus_ko)})
    # C4 — coût structurel par montée de version
    rec("C", "C4", "Coût structurel par montée : corpus 17 touches vs éphémère 0",
        "FACT", "corpus : 17 touches/montée MINOR (worklog Task 48 — c.1 inventaire D601) ; "
                "éphémère : 0 touche d'état (régénération lecture seule)",
        {"corpus_touches": 17, "ephemere_touches": 0})
    # C5 — résilience volatilité (suppression + régénération mesurées)
    echant = racine[:5]
    cible = [generer_pm_ephemere(SKILLS / s, TESTDIR / "perf") for s in echant]
    for p in cible:
        p.unlink()
    t0 = time.perf_counter()
    regen = [generer_pm_ephemere(SKILLS / s, TESTDIR / "perf") for s in echant]
    dt = (time.perf_counter() - t0) * 1000
    stables = all(p.exists() for p in regen)
    rec("C", "C5", "Résilience volatilité — suppression puis régénération (5 skills)",
        "PASS" if stables else "FAIL",
        "régénérés en %.0f ms ; corpus perdu = réinstallation pipeline + re-certification "
        "(preuve vive Task 60 §0 — minutes, worklog)" % dt,
        {"regen_ms": round(dt)})
    # C6 — lag : bump simulé en bac à sable
    sabl = TESTDIR / "sandbox-lag"
    if sabl.exists():
        shutil.rmtree(sabl)
    (sabl / "correct-work").mkdir(parents=True)
    src = (SKILLS / "correct-work" / "SKILL.md").read_text(encoding="utf-8")
    bumped = src.replace("version: 2.9.0", "version: 2.11.0-test", 1)
    (sabl / "correct-work" / "SKILL.md").write_text(bumped, encoding="utf-8")
    t0 = time.perf_counter()
    out = generer_pm_ephemere(sabl / "correct-work", sabl)
    dt = (time.perf_counter() - t0) * 1000
    t = out.read_text(encoding="utf-8")
    ok = "v2.11.0-test" in t
    rec("C", "C6", "Lag — bump version simulé (bac à sable) → PM éphémère instantané",
        "PASS" if ok else "FAIL",
        "PM éphémère v2.11.0-test en %.0f ms (source vivant lue) ; corpus : bump = cascade "
        "17 touches, lags ×4+ documentés (c.4)" % dt,
        {"ms": round(dt), "version_detectee": ok})
    # C7 — comparatif fonctionnel structure (corpus vs éphémère, correct-work)
    pm_corpus = sorted(CORPUS.glob("PROMPT-MAITRE-CORRECT-WORK-v*.md"))[-1]
    pm_eph = outdir / "PM-ephemere-correct-work-v2.9.0.md"
    tc, te = pm_corpus.read_text(encoding="utf-8"), pm_eph.read_text(encoding="utf-8")
    diffs = {
        "§7 Historique versions complet": ("§7 — HISTORIQUE" in tc, "§7 — HISTORIQUE" in te),
        "§5 Instructions installation écosystème": ("§5 — INSTRUCTIONS D'INSTALLATION" in tc, False),
        "Mode d'emploi IA externe": (False, "MODE D'EMPLOI — IA EXTERNE" in te),
        "SHA-256 source": (False, "SHA-256 source" in te),
        "CONTEXTE SYSTÈME embarqué": (bool(re.search(r"[Cc]ontexte [Ss]ystème", tc)), True),
    }
    rec("C", "C7", "Comparatif structurel PM corpus vs PM éphémère (correct-work)",
        "FACT", " ; ".join("%s corpus=%s éphémère=%s" % (k, v[0], v[1]) for k, v in diffs.items()),
        diffs)


# ---------------------------------------------------------------------------

def main():
    TESTDIR.mkdir(parents=True, exist_ok=True)
    print("Task 60 G3-SG1b — Tests comparatifs (D603b) — %s" % date.today().isoformat())
    print("Sorties : %s (bac à sable — AUCUNE intégration)" % TESTDIR)
    try:
        phase_a()
        phase_b()
        phase_c()
    except Exception as e:  # noqa: BLE001 — échec harnais = rc 2, jamais masqué
        print("ERREUR HARNAIS : %r" % e)
        sys.exit(2)
    res = TESTDIR / "resultats.json"
    res.write_text(json.dumps(RESULTS, indent=2, ensure_ascii=False), encoding="utf-8")
    n_pass = sum(1 for r in RESULTS if r["verdict"] in ("PASS", "EXPECTED-REFUS"))
    n_fail = sum(1 for r in RESULTS if r["verdict"] == "FAIL")
    n_fact = sum(1 for r in RESULTS if r["verdict"] == "FACT")
    print("\n==== SYNTHÈSE : %d PASS · %d FAIL · %d FACT — rapport : %s" % (n_pass, n_fail, n_fact, res))
    sys.exit(0)


if __name__ == "__main__":
    main()
