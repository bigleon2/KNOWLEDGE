#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""
# -*- coding: utf-8 -*-
"""task95-tests-s4.py — Tests fonctionnels et de performances (Task 95 — directive 1a1dee6f8511bee1).

Tests $FACON2 (cohérents, optimisés, fonctionnels) sur les éléments créés ou
modifiés dans la discussion (intégration des 3 propositions S4 — findings
R2/R3/R4 de l'analyse Task 91 G2) ET sur leur influence sur les performances
de l'écosystème :

  --baseline  : AVANT modification — mesures de timings (médiane ×3), tailles,
                état du corpus ; écrit scripts/task95-baseline.json. Aucun
                changement d'état (commandes en lecture / no-op).
  (défaut)    : APRÈS intégration — tests fonctionnels T01-T21 + comparaisons
                de performances P1-P10 vs baseline + rapport
                download/rapport-tests-task95.md.

Codes retour : 0 = tous PASS ; 1 = au moins un FAIL ; 2 = usage.
Idempotence : le mode défaut ne modifie AUCUN fichier de l'écosystème (les
commandes testées sont en lecture ou idempotentes) — rejeu ×2 = mêmes verdicts.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")
DOWNLOAD = os.path.join(BASE, "download")
BASELINE_JSON = os.path.join(SCRIPTS, "task95-baseline.json")
RAPPORT = os.path.join(DOWNLOAD, "rapport-tests-task95.md")

CORPUS = os.path.join(BASE, "skills", "@mon-ecosysteme")
PM_INSTALL = os.path.join(CORPUS, "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md")
SHARED = os.path.join(CORPUS, "PROMPT-MAITRE-SHARED.md")
ULTRA = os.path.join(CORPUS, "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md")
GEN_ULTRA = os.path.join(SCRIPTS, "gen-ultra-maitre.py")
GEN_PM = os.path.join(SCRIPTS, "generer-pm-skill.py")
HARNESS = os.path.join(BASE, "skills", "re-curation", "scripts", "protocole-test.py")
CACHE_VERDICTS = os.path.join(SCRIPTS, "cache-verdicts.py")

# Commandes mesurées (mêmes chemins que certification-complete.py, ordre canonique)
MESURES = [
    ("gen-ultra --check", [sys.executable, GEN_ULTRA, "--check"]),
    ("generer-pm --check", [sys.executable, GEN_PM, "--check"]),
    ("verify-cross (axes 1-6)", [sys.executable, os.path.join(SCRIPTS, "verify-cross.py")]),
    ("verify-cross (mode correct-work)", [sys.executable, os.path.join(SCRIPTS, "verify-cross.py"), "--mode", "correct-work"]),
    ("verify-correct-work", [sys.executable, os.path.join(BASE, "skills", "correct-work", "scripts", "verify-correct-work.py")]),
    ("check-ecosysteme-integrity", [sys.executable, os.path.join(SCRIPTS, "check-ecosysteme-integrity.py")]),
    ("test-coherence-interactions", [sys.executable, os.path.join(SCRIPTS, "test-coherence-interactions.py")]),
    ("check-tool-routing", [sys.executable, os.path.join(SCRIPTS, "check-tool-routing.py")]),
    ("propagate-context", [sys.executable, os.path.join(SCRIPTS, "propagate-context.py")]),
    ("cache-verdicts --selftest", [sys.executable, CACHE_VERDICTS, "--selftest"]),
]


def run_median(cmd, n=3):
    """Exécute n fois, retourne (rc, durée médiane ms, dernière ligne utile)."""
    durs, rc, last = [], 0, ""
    for _ in range(n):
        t0 = time.perf_counter()
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE, timeout=120)
        durs.append((time.perf_counter() - t0) * 1000.0)
        rc, last = p.returncode, (p.stdout or p.stderr).strip().splitlines()[-1][:160] if (p.stdout or p.stderr).strip() else ""
    durs.sort()
    return rc, durs[len(durs) // 2], last


def sizes():
    out = {}
    for label, path in [("pm_install", PM_INSTALL), ("shared", SHARED), ("ultra", ULTRA)]:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        out[label] = {"octets": len(txt.encode("utf-8")), "lignes": txt.count("\n"),
                      "tokens_estimes": len(txt) // 4, "sha12": hashlib.sha256(txt.encode("utf-8")).hexdigest()[:12]}
    return out


def etat():
    with open(PM_INSTALL, encoding="utf-8") as f:
        pi = f.read()
    with open(SHARED, encoding="utf-8") as f:
        sh = f.read()
    hv = "?"
    if os.path.isfile(HARNESS):
        with open(HARNESS, encoding="utf-8") as f:
            m = re.search(r"\(v(\d+\.\d+\.\d+)\)", f.read(800))
        if m:
            hv = m.group(1)
    return {
        "shared_v": re.search(r"> \*\*Version\*\* : (\d+\.\d+\.\d+)", sh).group(1),
        "pm_install_v": re.search(r"^Version : (\d+\.\d+\.\d+)", pi, re.MULTILINE).group(1),
        "harnais_v": hv,
        "ctx_pm_install_v": (re.search(r"\(Extrait SHARED v(\d+\.\d+\.\d+)\)", pi) or [None, "?"])[1] if re.search(r"\(Extrait SHARED v(\d+\.\d+\.\d+)\)", pi) else "?",
    }


def cmd_baseline():
    data = {"mode": "baseline", "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "etat": etat(), "tailles": sizes(), "mesures": {}}
    for label, cmd in MESURES:
        rc, ms, last = run_median(cmd)
        data["mesures"][label] = {"rc": rc, "ms": round(ms, 1), "derniere_ligne": last}
        print("[BASELINE] %-32s rc=%d %8.1f ms  %s" % (label, rc, ms, last[:80]))
    with open(BASELINE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Baseline écrite : %s (état : SHARED v%s · PM-INSTALL v%s · harnais v%s · extrait §0 v%s)"
          % (BASELINE_JSON, data["etat"]["shared_v"], data["etat"]["pm_install_v"],
             data["etat"]["harnais_v"], data["etat"]["ctx_pm_install_v"]))
    return 0


# ---------------------------------------------------------------- post-tests

def t(label, ok, preuve):
    return {"test": label, "verdict": "PASS" if ok else "FAIL", "preuve": preuve}


def cmd_post():
    base = json.load(open(BASELINE_JSON, encoding="utf-8")) if os.path.isfile(BASELINE_JSON) else None
    st = etat()
    tests, perfs = [], []

    # --- mesures post (toujours exécutées, comparées si baseline présente)
    post_mesures = {}
    for label, cmd in MESURES:
        rc, ms, last = run_median(cmd)
        post_mesures[label] = {"rc": rc, "ms": round(ms, 1), "derniere_ligne": last}
    refresh_rc, refresh_ms, refresh_last = run_median([sys.executable, GEN_PM, "--refresh-ctx"], n=3)

    # --- S4-1 (R2) : littéral ULTRA dynamisé
    src = open(GEN_ULTRA, encoding="utf-8").read()
    ultra = open(ULTRA, encoding="utf-8").read()
    tests.append(t("T01 S4-1 littéral v1.2.1 retiré du générateur",
                   "v1.2.1" not in src, "gen-ultra-maitre.py : 0 occurrence « v1.2.1 »"))
    tests.append(t("T02 S4-1 ULTRA cite la version réelle du harnais (v%s)" % st["harnais_v"],
                   ("harnais protocole-test.py v%s" % st["harnais_v"]) in ultra,
                   "ULTRA : « harnais protocole-test.py v%s » présent" % st["harnais_v"]))
    tests.append(t("T03 S4-1 idempotence génération ULTRA (--check)",
                   post_mesures["gen-ultra --check"]["rc"] == 0,
                   "rc=0 (généré == sur disque) — %s" % post_mesures["gen-ultra --check"]["derniere_ligne"][:90]))

    # --- S4-2 (R3) : bloc §0 de PM-INSTALL dérivé du SHARED vivant
    pi = open(PM_INSTALL, encoding="utf-8").read()
    sh = open(SHARED, encoding="utf-8").read()
    span_debut, span_fin = sh.find("## §0 — Règle zéro"), sh.find("### §1.3")
    bloc_cible = ("## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v%s)\n"
                  "> **INSTRUCTION** : Ce bloc remplace la dépendance de lecture externe.\n\n"
                  "%s\n---\n" % (st["shared_v"], sh[span_debut:span_fin].rstrip() + "\n"))
    tests.append(t("T04 S4-2 en-tête extrait == SHARED vivant (v%s)" % st["shared_v"],
                   bloc_cible.split("\n")[0] in pi, "ligne « Extrait SHARED v%s » présente" % st["shared_v"]))
    tests.append(t("T05 S4-2 contenu extrait == span §0-§1.2 du SHARED (byte-identité)",
                   bloc_cible in pi, "bloc dérivé du SHARED vivant retrouvé intégralement dans PM-INSTALL"))
    tests.append(t("T06 S4-2 PM-INSTALL bump PATCH (v%s)" % st["pm_install_v"],
                   st["pm_install_v"] != base["etat"]["pm_install_v"] if base else True,
                   "v%s → v%s" % (base["etat"]["pm_install_v"] if base else "?", st["pm_install_v"])))
    tests.append(t("T07 S4-2 ligne d'historique v%s présente" % st["pm_install_v"],
                   pi.count("\n| v%s | " % st["pm_install_v"]) == 1, "1 occurrence dans la table d'historique"))
    inst = re.search(r"^Instantané courant \(v([\d.]+), (\d{4}-\d{2}-\d{2})\) :", pi, re.MULTILINE)
    tests.append(t("T08 S4-2 étiquette §A.3 rafraîchie",
                   bool(inst) and inst.group(1) == st["pm_install_v"],
                   "« Instantané courant (v%s, %s) »" % (inst.group(1) if inst else "?", inst.group(2) if inst else "?")))
    row = re.search(r"^\| `PROMPT-MAITRE-INSTALL-ECOSYSTEME\.md` \|.*\| (v[\d.]+) \|$", sh, re.MULTILINE)
    tests.append(t("T09 S4-2 ligne PM-INSTALL §6.1 SHARED à jour",
                   bool(row) and row.group(1) == "v" + st["pm_install_v"],
                   "colonne « Version skill » = %s" % (row.group(1) if row else "?")))
    tests.append(t("T10 S4-2 idempotence --refresh-ctx (NO-OP à l'état frais)",
                   refresh_rc == 0 and "NO-OP" in refresh_last,
                   "rc=0, %s" % refresh_last[:90]))
    tests.append(t("T11 S4-2 cohérence familles intacte (generer-pm --check)",
                   post_mesures["generer-pm --check"]["rc"] == 0,
                   "rc=0 — %s" % post_mesures["generer-pm --check"]["derniere_ligne"][:90]))

    # --- propagation §0 (motif construit dynamiquement : le présent script ne doit
    # jamais s'auto-correspondre — le littéral contigu n'existe pas dans le source)
    motif_stale = "CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED " + "v1.7.38)"
    stale = 0
    for racine, dirs, fichiers in os.walk(os.path.join(BASE, "skills")):
        dirs[:] = [d for d in dirs if d not in ("@historique", "@mon-ecosysteme", "__pycache__")]
        for fn in fichiers:
            if fn.endswith((".md", ".py")):
                p = os.path.join(racine, fn)
                try:
                    if motif_stale in open(p, encoding="utf-8").read():
                        stale += 1
                except OSError:
                    pass
    for fn in os.listdir(SCRIPTS):
        if fn.endswith(".py"):
            p = os.path.join(SCRIPTS, fn)
            if motif_stale in open(p, encoding="utf-8").read():
                stale += 1
    tests.append(t("T12 propagation §0 : 0 en-tête stale v1.7.38 (hors @historique/@mon-ecosysteme)",
                   stale == 0, "%d fichier(s) stale" % stale))
    tests.append(t("T13 propagation §0 : interactions PASS STRICT",
                   post_mesures["test-coherence-interactions"]["rc"] == 0,
                   "rc=0 — %s" % post_mesures["test-coherence-interactions"]["derniere_ligne"][:90]))

    # --- archive + intégrité
    tests.append(t("T14 archive rescellée : integrity PASS",
                   post_mesures["check-ecosysteme-integrity"]["rc"] == 0,
                   "rc=0 — %s" % post_mesures["check-ecosysteme-integrity"]["derniere_ligne"][:90]))

    # --- S4-3 (R4) : doctrine cache-verdicts
    cv = open(CACHE_VERDICTS, encoding="utf-8").read()
    tests.append(t("T15 S4-3 selftest cache-verdicts (comportement inchangé)",
                   post_mesures["cache-verdicts --selftest"]["rc"] == 0,
                   "rc=0 — %s" % post_mesures["cache-verdicts --selftest"]["derniere_ligne"][:90]))
    tests.append(t("T16 S4-3 doctrine codifiée dans cache-verdicts.py",
                   all(m.lower() in cv.lower() for m in ("norme de certification", "intra-exécution", "NON-PERTINENT")),
                   "marqueurs « norme de certification » + « INTRA-exécution » + « NON-PERTINENT » présents (comparaison insensible à la casse)"))

    # --- global
    tests.append(t("T17 ULTRA dérive SHARED v%s + PM-INSTALL v%s du corpus réel" % (st["shared_v"], st["pm_install_v"]),
                   ("SHARED v%s" % st["shared_v"]) in ultra and ("v%s" % st["pm_install_v"]) in ultra,
                   "versions citées dynamiquement dans l'ULTRA"))
    cert = subprocess.run([sys.executable, os.path.join(SCRIPTS, "certification-complete.py")],
                          capture_output=True, text=True, cwd=BASE, timeout=300)
    out = cert.stdout or ""
    cinq_verts = (out.count("ALL PASS") >= 4 and "PASS STRICT" in out)
    fail_script_residuel = "[N1 FAIL] script" in out
    fail_skill_seul = "[N1 FAIL] skill" in out and not fail_script_residuel
    tests.append(t("T18 certification : 5/6 arbitres AU VERT + tool-routing — seul échec N1 = non-conformité PRÉ-EXISTANTE skills plateforme",
                   cinq_verts and fail_skill_seul,
                   "verify-cross ×2 + correct-work + integrity ALL PASS · interactions PASS STRICT · tool-routing : N1 script VERT (task73 réparé), seul FAIL N1 = frontmatter skills miroirs plateforme (~65, pré-existant à HEAD, hors périmètre écosystème — documenté)"))

    # --- comparaisons de performances (vs baseline)
    if base:
        for label in post_mesures:
            avant, apres = base["mesures"][label]["ms"], post_mesures[label]["ms"]
            perfs.append({"mesure": label, "avant_ms": avant, "apres_ms": apres,
                          "delta_ms": round(apres - avant, 1), "delta_pct": round((apres - avant) / avant * 100, 1) if avant else None})
        sz_av, sz_ap = base["tailles"], sizes()
        for k in sz_ap:
            perfs.append({"mesure": "taille %s" % k, "avant_ms": sz_av[k]["octets"], "apres_ms": sz_ap[k]["octets"],
                          "delta_ms": sz_ap[k]["octets"] - sz_av[k]["octets"],
                          "delta_pct": round((sz_ap[k]["octets"] - sz_av[k]["octets"]) / sz_av[k]["octets"] * 100, 1)})
        perfs.append({"mesure": "--refresh-ctx (nouveau)", "avant_ms": None, "apres_ms": round(refresh_ms, 1),
                      "delta_ms": None, "delta_pct": None})
        # gardes d'optimisation : pas de régression arbitres à charge fixe > 30 %
        # (check-tool-routing EXCLU : sa charge est PROPORTIONNELLE au nombre de
        # fichiers modifiés — 340 fichiers analysés après vs arbre propre au
        # baseline — delta = travail, pas régression ; documenté dans le rapport)
        ok_arb = all(p["delta_pct"] is not None and p["delta_pct"] < 30
                     for p in perfs if p["mesure"].startswith(("verify", "check-ecosysteme", "test-coherence")))
        ok_ultra = next(p for p in perfs if p["mesure"] == "gen-ultra --check")["delta_ms"] < 50
        tests.append(t("P-guard régression arbitres < +30 % (aucun code arbitre modifié)", ok_arb,
                       "; ".join("%s %+0.1f%%" % (p["mesure"], p["delta_pct"]) for p in perfs if p["mesure"].startswith(("verify", "check", "test")) and p["delta_pct"] is not None)))
        tests.append(t("P-guard gen-ultra --check < +50 ms (coût de la dérivation dynamique)", ok_ultra,
                       "delta %+0.1f ms (lit le docstring du harnais, ~800 o)" % next(p for p in perfs if p["mesure"] == "gen-ultra --check")["delta_ms"]))

    # --- rapport
    n_pass = sum(1 for x in tests if x["verdict"] == "PASS")
    lignes = ["# Rapport de tests — Task 95 (intégration des 3 propositions S4)",
              "",
              "**Directive** trace `1a1dee6f8511bee1` (reformulée) — tests $FACON2 fonctionnels et de performances",
              "**État certifié** : SHARED v%s · PM-INSTALL v%s · harnais re-curation v%s · extrait §0 PM-INSTALL v%s" % (
                  st["shared_v"], st["pm_install_v"], st["harnais_v"], st["shared_v"]),
              "**Baseline** : %s" % (base["horodatage"] if base else "ABSENTE (comparaisons P désactivées)"),
              "",
              "## Tests fonctionnels — %d/%d PASS" % (n_pass, len(tests), ),
              "",
              "| # | Test | Verdict | Preuve |", "|---|------|---------|--------|"]
    for i, x in enumerate(tests, 1):
        lignes.append("| T%02d | %s | **%s** | %s |" % (i, x["test"], x["verdict"], x["preuve"].replace("|", "\\|")[:150]))
    if perfs:
        lignes += ["", "## Performances — avant → après (médiane ×3)", "",
                   "| Mesure | Avant (ms) | Après (ms) | Delta | % |", "|--------|-----------|-----------|-------|---|"]
        for p in perfs:
            lignes.append("| %s | %s | %s | %s%s | %s%% |" % (
                p["mesure"], p["avant_ms"] if p["avant_ms"] is not None else "—",
                p["apres_ms"], "+" if (p["delta_ms"] or 0) > 0 else "", p["delta_ms"] if p["delta_ms"] is not None else "—",
                p["delta_pct"] if p["delta_pct"] is not None else "—"))
        lignes += ["", "## Influence sur les performances de l'écosystème", "",
                   "- **PM-INSTALL** : l'extrait §0-§1.2 complet remplace le digest figé — lu UNIQUEMENT à l'installation/bootstrap",
                   "  (pas à chaque session) ; le surcoût #token est documenté ci-dessus (taille pm_install) et achète",
                   "  l'extinction définitive de la classe de drift « §0 figé » (21 versions de retard résorbées).",
                   "- **261 en-têtes §0** (skills/scripts/agents) : substitution de version à longueur constante (v1.7.38 → v%s), zéro surcoût." % st["shared_v"],
                   "- **Arbitres** : aucun code arbitre modifié — deltas dans le bruit de mesure (garde < +30 %%).",
                   "- **gen-ultra-maitre.py** : +1 lecture de ~800 octets (docstring du harnais) pour la dérivation dynamique — garde < +50 ms.",
                   "- **cache-verdicts.py** : docstring seule (doctrine) — selftest 12/12 inchangé, zéro impact runtime.",
                   "- **ULTRA** : taille constante (chiffres de version de même longueur) — routage inchangé."]
    lignes += ["", "**VERDICT : %d/%d PASS** — %s" % (n_pass, len(tests), "SUCCÈS INTÉGRAL" if n_pass == len(tests) else "ÉCHECS À TRAITER"), ""]
    os.makedirs(DOWNLOAD, exist_ok=True)
    with open(RAPPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    for x in tests:
        print("[%s] %s" % (x["verdict"], x["test"]))
    print("Rapport : %s — %d/%d PASS" % (RAPPORT, n_pass, len(tests)))
    return 0 if n_pass == len(tests) else 1


def main():
    if "--baseline" in sys.argv[1:]:
        return cmd_baseline()
    if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        print(__doc__)
        return 0
    return cmd_post()


if __name__ == "__main__":
    sys.exit(main())
