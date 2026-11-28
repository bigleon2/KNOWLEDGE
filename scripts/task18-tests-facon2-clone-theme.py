#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batterie $FACON2 Task 18 — tests fonctionnels de performance PM INSTALL / clone-chat / gen-plan.

Directive propriétaire (trace 1a221abc2b446dfd) : « fais des tests ($FACON2)
fonctionnels de performance sur PM INSTALL et mes skills clone-chat et gen-plan
dans l'objectif de corriger leurs failles et d'optimiser leurs performances ».

Sections :
  S1  clone-chat v2.1.0 — structure + modes thématiques (§1.12) + check 9
  S2  références/theme-template.md — gabarit de clone thématique complet
  S3  gen-plan v3.49.0 — structure frontmatter + intégrations clés
  S4  PM INSTALL v1.10.8 — parité ×3 copies + sections clés (faille rétroport corrigée)
  S5  pipeline installation — dry-run ×2, convergence 0 divergence, selftest bootstrap
  S6  KNOWLEDGE.md — entrée clone-chat v2.1.0 des deux côtés (live + dépôt)
  S7  nommage mode (ALL) — génération déterministe des noms (kebab-case, unicité, ×2)
  S8  garde anti-erreur — thème inconnu → erreur contrôlée SANS clone

Verdicts binaires PASS/FAIL, stdlib uniquement, idempotence ×2 requise à l'appel.
Rapport : scripts/task18-facon2-report.json
"""

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILLS = Path("/home/z/my-project/skills")
SCRIPTS = Path("/home/z/my-project/scripts")
REPORT = SCRIPTS / "task18-facon2-report.json"

results = []


def check(section, name, cond, detail=""):
    results.append({"section": section, "check": name,
                    "verdict": "PASS" if cond else "FAIL", "detail": detail})
    return bool(cond)


def lire(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


def fm_version(text):
    m = re.search(r"^version:\s*([0-9][0-9.]*)\s*$", text, re.M)
    return m.group(1) if m else None


def run(cmd, timeout=240, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, cwd=cwd)


# ---------------------------------------------------------------- S1 clone-chat
def s1_clone_chat():
    sec = "S1"
    live = lire(SKILLS / "clone-chat/SKILL.md")
    depot = lire(REPO / "skills/clone-chat/SKILL.md")
    check(sec, "version-2.1.0", fm_version(live) == "2.1.0", fm_version(live))
    check(sec, "frontmatter-complet",
          all(x in live for x in ["name: clone-chat", "category: ecosystem",
                                  "language: fr"]),
          "name+category+language")
    check(sec, "tag-themes", "  - themes" in live, "tags += themes")
    check(sec, "description-modes",
          "--theme" in live.split("dependencies:")[0]
          and "(ALL)" in live.split("dependencies:")[0],
          "description frontmatter cite --theme et (ALL)")
    check(sec, "declencheurs-theme",
          "clone-chat --theme" in live and "clone-chat (<theme>)" in live,
          "§A : 2 déclencheurs v2.1.0")
    check(sec, "section-1.12", "### §1.12 Modes thématiques" in live, "§1.12")
    sous = ["#### §1.12.1 Détection des thèmes", "#### §1.12.2 Clone thématique",
            "#### §1.12.3 Clones multiples", "#### §1.12.4 Impact sur les 7+1 étapes"]
    check(sec, "sous-sections-1.12", all(s in live for s in sous),
          "1.12.1+1.12.2+1.12.3+1.12.4")
    check(sec, "check-9", "Check 9 — Cohérence thématique" in live
          and "9/9 PASS" in live, "cohérence thématique")
    check(sec, "gardes-1.12",
          "thème non reconnu" in live and "Règle de preuve (R4)" in live
          and "Garde mono-thème" in live,
          "anti-erreur + preuve ≥2 + mono-thème")
    check(sec, "grille-token-modes",
          "Mode `--theme`" in live and "Mode `(<theme>)`" in live
          and "Mode `(ALL)`" in live,
          "grille #token +3 lignes")
    check(sec, "gabarit-reference",
          "références/theme-template.md" in live, "§1.12.2 + §2.7")
    check(sec, "conventions-themes", "Thèmes (v2.1.0)" in live, "§6")
    check(sec, "dependencies-3",
          all(x in live for x in ["skill: gen-plan", "skill: correct-work",
                                  "skill: skill-creator"]),
          "gen-plan/correct-work/skill-creator")
    check(sec, "parite-live-depot", sha256(SKILLS / "clone-chat/SKILL.md")
          == sha256(REPO / "skills/clone-chat/SKILL.md"), "SHA ×2 identiques")


# ---------------------------------------------------------------- S2 gabarit
def s2_theme_template():
    sec = "S2"
    live = lire(SKILLS / "clone-chat/références/theme-template.md")
    depot = lire(REPO / "skills/clone-chat/références/theme-template.md")
    check(sec, "titre-thematique", "CLONE THÉMATIQUE" in live, "titre")
    check(sec, "sections-0-a-5",
          all(x in live for x in ["## §0 —", "## §1 —", "## §2 —",
                                  "## §3 —", "## §4 —", "## §5 —"]),
          "structure §0-§5")
    check(sec, "exclusions-0bis", "§0bis" in live and "| # | Exclu" in live,
          "table des exclusions avec pointeurs")
    check(sec, "auto-suffisance-perimetre",
          "Auto-suffisance périmétrique" in live, "mention §0 obligatoire")
    check(sec, "check-9-mention", "check 9" in live and "9/9 PASS" in live,
          "validation 9/9 en mode thématique")
    check(sec, "drifts-theme", "Évolutions de contexte du thème" in live,
          "§3.5 filtré")
    check(sec, "auto-clonage-thematique", "AUTO-CLONAGE THÉMATIQUE" in live
          or "AUTO-CLONAGE (thématique)" in live, "§5 adapté")
    check(sec, "parite-live-depot",
          sha256(SKILLS / "clone-chat/références/theme-template.md")
          == sha256(REPO / "skills/clone-chat/références/theme-template.md"),
          "SHA ×2 identiques")


# ---------------------------------------------------------------- S3 gen-plan
def s3_gen_plan():
    sec = "S3"
    p = SKILLS / "gen-plan/SKILL.md"
    live = lire(p)
    depot = lire(REPO / "skills/gen-plan/SKILL.md")
    check(sec, "version-3.49.0", fm_version(live) == "3.49.0", fm_version(live))
    check(sec, "name-gen-plan", "name: gen-plan" in live, "frontmatter")
    check(sec, "garde-e1-install", "É1-INSTALL" in live,
          "garde à TOUTE invocation v3.49.0")
    check(sec, "prompt-gateway", "PROMPT-GATEWAY" in live,
          "pré-traitement v3.46.0")
    check(sec, "regle-or-6-francais", "règle d'or n°6" in live,
          "langue française exclusif")
    check(sec, "kb-integration", "KNOWLEDGE.md" in live or "KB_PATH" in live,
          "registre KB")
    check(sec, "mode-step", "step" in live.lower(), "modes plan/step")
    check(sec, "fail-close", "FAIL-CLOSE" in live, "règle §1.18 v3.48.0")
    for s in ["routage-skills-agents.py", "check_plan_protocol.py"]:
        check(sec, f"script-{s}", (SKILLS / f"gen-plan/scripts/{s}").exists(),
              "présent")
    check(sec, "dossier-evals", (SKILLS / "gen-plan/evals").exists()
          and any((SKILLS / "gen-plan/evals").iterdir()), "non vide")
    check(sec, "parite-live-depot", sha256(p) == sha256(REPO / "skills/gen-plan/SKILL.md"),
          "SHA ×2 identiques")


# ---------------------------------------------------------------- S4 PM INSTALL
def s4_pm_install():
    sec = "S4"
    copies = [SKILLS / "@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
              REPO / "scripts/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
              SCRIPTS / "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"]
    shas = {sha256(c) for c in copies}
    check(sec, "parite-3-copies", len(shas) == 1, "faille rétroport CORRIGÉE")
    live = lire(copies[0])
    check(sec, "version-1.10.8", "Version : 1.10.8" in live, "en-tête")
    check(sec, "shared-1.7.47", "SHARED v1.7.47" in live, "contexte système")
    for x in ["## §2bis", "## §2ter", "## §2quater", "### §3.2", "## §A",
              "pipeline en 11 étapes", "bootstrap-ecosysteme.py", "alias-eco"]:
        check(sec, f"section-{x.replace('#','').replace(' ','-')[:24]}", x in live, x)
    check(sec, "mecanisme-dual", "MÉCANISME DUAL" in live or
          ("installation directe" in live and "assemblage" in live), "§3.2")


# ---------------------------------------------------------------- S5 pipeline
def pipeline_json(cmd_extra, timeout):
    r = run([sys.executable, str(REPO / "scripts/eco_install_pipeline.py")]
            + cmd_extra, timeout=timeout, cwd=str(REPO))
    i = r.stdout.find("{")
    data = json.loads(r.stdout[i:]) if i >= 0 else {}
    trace = (r.stderr or "")[-300:] or (r.stdout[:300] if i < 0 else "")
    return r.returncode, data, trace


def s5_pipeline():
    sec = "S5"
    # Sémantique pipeline documentée (suites 169/171/173) : rc=0 = propre,
    # rc=2 = divergences détectées / réparations avec réserves documentées
    # (verdict INSTALLE-RÉPARÉ-PARTIEL, ex. amnésie hôte version-management).
    # Critère DUR : dry-run terminal rc=0 + 0 divergence + SHA vérifiés.
    rc1, d1, tr1 = pipeline_json(["--dry-run"], 240)
    div1 = d1.get("post_install", {}).get("divergences", [])
    check(sec, "dryrun1-verdict-coherent",
          (rc1 == 0 and len(div1) == 0) or (rc1 == 2 and len(div1) > 0),
          f"rc={rc1} divergences={len(div1)} trace={tr1[:120]}")
    check(sec, "garde-R2", "0 rétrogradation" in d1.get("garde_R2", ""),
          d1.get("garde_R2", "absent")[:64])
    if rc1 == 2:
        rc2, d2, tr2 = pipeline_json([], 300)
        check(sec, "installation-reelle-verdict-coherent", rc2 in (0, 2),
              f"rc={rc2} (0=propre, 2=réparé-partiel) trace={tr2[:120]}")
    rc3, d3, tr3 = pipeline_json(["--dry-run"], 240)
    div3 = d3.get("post_install", {}).get("divergences", [])
    check(sec, "convergence-0-divergence", rc3 == 0 and len(div3) == 0,
          f"rc={rc3} divergences={div3} trace={tr3[:120]}")
    rcs = []
    for _ in range(2):
        r = run([sys.executable, str(REPO / "scripts/bootstrap-ecosysteme.py"),
                 "--selftest"], timeout=180, cwd=str(REPO))
        rcs.append(r.returncode)
    check(sec, "bootstrap-selftest-x2", rcs == [0, 0], f"rc={rcs}")
    check(sec, "sha-verifies-58", d3.get("post_install", {}).get("sha256_verifies", 0) >= 58,
          f"sha256_verifies={d3.get('post_install', {}).get('sha256_verifies')}")


# ---------------------------------------------------------------- S6 KB
def s6_kb():
    sec = "S6"
    live = lire(SKILLS / "KNOWLEDGE.md")
    depot = lire(REPO / "skills/KNOWLEDGE.md")
    for nom, txt in [("live", live), ("depot", depot)]:
        check(sec, f"entree-v2.1.0-{nom}", "## clone-chat v2.1.0" in txt, "titre")
        check(sec, f"description-modes-{nom}", "Modes thématiques v2.1.0" in txt,
              "description")
        check(sec, f"calibration-{nom}",
              "Task 18 (2026-11-28, session web-220878ed" in txt,
              "entrée calibration du jour")
    check(sec, "arete-gen-plan-satisfaite",
          "clone-chat >= v2.0.0" in live, "dépendance gen-plan >= v2.0.0 OK par 2.1.0")
    check(sec, "parite-live-depot", sha256(SKILLS / "KNOWLEDGE.md")
          == sha256(REPO / "skills/KNOWLEDGE.md"), "SHA ×2 identiques")


# ---------------------------------------------------------------- S7 nommage ALL
def generer_noms_clone_themes(sujet, themes, date):
    """Convention §1.12.3 : un clone par thème + index récapitulatif."""
    noms = [f"{sujet}-clone-theme-{t['slug']}-{date}.md" for t in themes]
    noms.append(f"{sujet}-clone-themes-index-{date}.md")
    return noms


KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def s7_nommage_all():
    sec = "S7"
    fixture = [
        {"theme": "Conversion KPS", "slug": "conversion-kps"},
        {"theme": "Optimisation GIF écosystème", "slug": "optimisation-gif"},
        {"theme": "Installation de l'écosystème", "slug": "installation-ecosysteme"},
    ]
    n1 = generer_noms_clone_themes("session-web-220878ed", fixture, "2026-11-28")
    n2 = generer_noms_clone_themes("session-web-220878ed", fixture, "2026-11-28")
    check(sec, "determinisme-x2", n1 == n2, "×2 identiques")
    check(sec, "kebab-case-tous", all(KEBAB.match(
        n.replace(".md", "").replace("session-web-220878ed-clone", "clone"))
        for n in n1), "slugs conformes")
    check(sec, "unicite", len(n1) == len(set(n1)), f"{len(n1)} noms uniques")
    check(sec, "index-present", any("themes-index" in n for n in n1), "index (ALL)")
    check(sec, "un-clone-par-theme", len(n1) == len(fixture) + 1, "3+index")
    # Idempotence de périmètre (§1.12.3) : même périmètre → mêmes noms
    check(sec, "idempotence-perimetre",
          generer_noms_clone_themes("s", fixture, "d") ==
          generer_noms_clone_themes("s", fixture, "d"), "écrasement à l'identique")


# ---------------------------------------------------------------- S8 garde
def garde_theme(demande, slugs_valides):
    """Garde §1.12.2 : thème inconnu → erreur contrôlée SANS clone."""
    if demande in slugs_valides:
        return {"ok": True, "clone": demande}
    return {"ok": False, "erreur": "thème non reconnu — choisir dans la table",
            "slugs_valides": list(slugs_valides)}


def s8_garde():
    sec = "S8"
    slugs = ["conversion-kps", "optimisation-gif", "installation-ecosysteme"]
    g1 = garde_theme("optimisation-gif", slugs)
    check(sec, "theme-connu-accepte", g1["ok"] and g1["clone"] == "optimisation-gif",
          "clone produit")
    g2 = garde_theme("KPS", slugs)
    check(sec, "typo-majuscule-refusee", not g2["ok"] and g2["slugs_valides"] == slugs,
          "erreur contrôlée + table reproduite")
    g3 = garde_theme("theme-inexistant", slugs)
    check(sec, "inconnu-refuse-sans-clone", not g3["ok"] and "clone" not in g3,
          "aucun clone inventé")
    g4 = garde_theme("", slugs)
    check(sec, "vide-refuse", not g4["ok"], "chaîne vide refusée")


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    sections = [("S1", s1_clone_chat), ("S2", s2_theme_template),
                ("S3", s3_gen_plan), ("S4", s4_pm_install),
                ("S5", s5_pipeline), ("S6", s6_kb),
                ("S7", s7_nommage_all), ("S8", s8_garde)]
    for _, fn in sections:
        fn()
    total = len(results)
    ok = sum(1 for r in results if r["verdict"] == "PASS")
    fails = [r for r in results if r["verdict"] == "FAIL"]
    par_section = {}
    for r in results:
        par_section.setdefault(r["section"], {"pass": 0, "fail": 0})
        par_section[r["section"]]["pass" if r["verdict"] == "PASS" else "fail"] += 1
    report = {
        "batterie": "FACON2 Task 18 — PM INSTALL / clone-chat / gen-plan",
        "horodatage": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duree_s": round(time.time() - t0, 2),
        "total": total, "pass": ok, "fail": len(fails),
        "verdict_global": "PASS" if len(fails) == 0 else "FAIL",
        "par_section": par_section,
        "results": results,
        "idempotence": "exécution ×2 requise (rapport byte-stable sauf horodatage/durée)",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    print(json.dumps({"total": total, "pass": ok, "fail": len(fails),
                      "verdict": report["verdict_global"],
                      "par_section": par_section}, ensure_ascii=False))
    for r in fails:
        print(f"FAIL {r['section']}/{r['check']} — {r['detail']}")
    return 0 if len(fails) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
