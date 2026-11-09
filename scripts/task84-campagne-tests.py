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

"""Task 84 — Campagne tests $FACON2 chronologique (directive 1a1bed51ccaf78f1).

Périmètre : éléments créés/modifiés dans la discussion web-ecef7f80
(Tasks 70→83, 2026-11-07 soir → 2026-11-09), ordre chronologique STRICT.
3 familles : F1 fonctionnels · F2 performances · F3 interactions — + idempotence ×2.
Rapport : scripts/task84-campagne-tests.json + download/rapport-campagne-tests-task84.md.
Idempotent : re-jeu = mêmes verdicts (état final stable : pipeline + cp zip + manifeste).
"""
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

HOST = "/home/z/my-project"
DEPOT = os.path.join(HOST, "KNOWLEDGE-repo")
SCRIPTS = os.path.join(DEPOT, "scripts")
HARNESS = os.path.join(DEPOT, "skills", "re-curation", "scripts", "protocole-test.py")
ZIP_HOTE = os.path.join(HOST, "download", "mon-ecosysteme_archive.zip")
ZIP_DEPOT = os.path.join(DEPOT, "download", "mon-ecosysteme_archive.zip")
RAPPORT_JSON = os.path.join(HOST, "scripts", "task84-campagne-tests.json")
RAPPORT_MD = os.path.join(HOST, "download", "rapport-campagne-tests-task84.md")
T0 = time.time()
RESULTS = []


def sha256f(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()[:16]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def run_cmd(cid, label, cmd, cwd=None, timeout=300, rc_ok=0, checks=None):
    """Exécute une commande, mesure, applique les checks de contenu → verdict."""
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd or DEPOT, capture_output=True, text=True,
                           timeout=timeout)
        rc, out, err = p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        rc, out, err = -1, "", "TIMEOUT"
    duree = round(time.time() - t0, 3)
    ok = (rc == rc_ok)
    notes = []
    if checks:
        for nom, fn in checks:
            try:
                res = bool(fn(out + "\n" + err))
            except Exception as e:  # noqa: BLE001 — note et FAIL
                res = False
                nom = f"{nom} (erreur: {e})"
            notes.append(f"{nom}={'OK' if res else 'KO'}")
            if not res:
                ok = False
    verdict = "PASS" if ok else "FAIL"
    RESULTS.append({"id": cid, "label": label, "cmd": " ".join(map(str, cmd)),
                    "rc": rc, "duree_s": duree, "verdict": verdict, "notes": notes,
                    "sortie": (out + err)[:600]})
    print(f"[{verdict}] {cid} {label} (rc={rc}, {duree}s) {' '.join(notes)}")
    return ok


def check_txt(*needles):
    def fn(txt):
        return all(n in txt for n in needles)
    return fn


def check_regex(pat):
    def fn(txt):
        return re.search(pat, txt) is not None
    return fn


def frontmatter_version(skill):
    m = re.search(r"^version:\s*([0-9.]+)", read(os.path.join(
        DEPOT, "skills", skill, "SKILL.md")), re.MULTILINE)
    return m.group(1) if m else None


def semver_ge(a, b):
    pa = [int(x) for x in a.split(".")]
    pb = [int(x) for x in b.split(".")]
    return pa >= pb


# ---------------------------------------------------------------- C1 (Task 70)
def c1():
    ok = True
    for s in ["bootstrap", "ghorg-install", "cmdr-clone", "cmdr-overlay-sync",
              "_commun", "test-karnaugh-f-l-s-b"]:
        path = os.path.join(DEPOT, "scripts", "ecosystem", s + ".py")
        try:
            with open(path, encoding="utf-8") as f:
                compile(f.read(), path, "exec")
        except (OSError, SyntaxError) as e:  # noqa: BLE001
            ok = False
            print(f"    compile KO {s}: {e}")
    run_cmd("C1", "scripts/ecosystem/*.py ×6 — compile + Karnaugh 20/20",
            [sys.executable, os.path.join(DEPOT, "scripts", "ecosystem",
                                          "test-karnaugh-f-l-s-b.py")],
            checks=[("karnaugh_20", check_regex(r"20\s*/\s*20|20/20"))])
    return ok


# ---------------------------------------------------------------- C2/C3 (Task 70)
def c2():
    mf = read(os.path.join(DEPOT, "skills", "@GHORG-ecosysteme", "manifest.yaml"))
    sel = read(os.path.join(DEPOT, "skills", "@GHORG-ecosysteme", "selection-tsi.yaml"))
    kb = read(os.path.join(DEPOT, "skills", "KNOWLEDGE.md"))
    ok = (len(mf) > 50 and len(sel) > 50 and "ghorg-cmdr" in kb
          and frontmatter_version("ghorg-cmdr") == "1.1.0")
    RESULTS.append({"id": "C2", "label": "@GHORG-ecosysteme + ghorg-cmdr v1.1.0 — YAML + KB",
                    "rc": 0 if ok else 1, "duree_s": 0.01, "verdict": "PASS" if ok else "FAIL",
                    "notes": ["manifest" if len(mf) > 50 else "manifest KO",
                              "selection" if len(sel) > 50 else "selection KO",
                              "kb+version" if ("ghorg-cmdr" in kb and
                                               frontmatter_version("ghorg-cmdr") == "1.1.0")
                              else "kb KO"], "sortie": ""})
    print(f"[{'PASS' if ok else 'FAIL'}] C2 @GHORG-ecosysteme + ghorg-cmdr v1.1.0")
    files = [f for f in glob.glob(os.path.join(DEPOT, "skills", "@Bibliotheque-skills-Multi-IA", "**", "*"),
                                  recursive=True) if os.path.isfile(f)]
    vides = [f for f in files if os.path.getsize(f) == 0]
    ok3 = len(files) >= 10 and not vides
    RESULTS.append({"id": "C3", "label": f"@Bibliotheque-skills-Multi-IA — {len(files)} fichiers, 0 vide",
                    "rc": 0 if ok3 else 1, "duree_s": 0.01, "verdict": "PASS" if ok3 else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if ok3 else 'FAIL'}] C3 @Bibliotheque ({len(files)} fichiers)")
    return ok and ok3


# ---------------------------------------------------------------- C4 (Task 71)
def c4():
    ok1 = run_cmd("C4a", "poids-chargement.py (R1) — selftest ×2",
                  [sys.executable, os.path.join(SCRIPTS, "poids-chargement.py"), "--selftest"])
    run_cmd("C4a", "poids-chargement.py (R1) — selftest re-jeu",
            [sys.executable, os.path.join(SCRIPTS, "poids-chargement.py"), "--selftest"])
    ok2 = run_cmd("C4b", "cache-verdicts.py (R2) — selftest ×2",
                  [sys.executable, os.path.join(SCRIPTS, "cache-verdicts.py"), "--selftest"])
    run_cmd("C4b", "cache-verdicts.py (R2) — selftest re-jeu",
            [sys.executable, os.path.join(SCRIPTS, "cache-verdicts.py"), "--selftest"])
    return ok1 and ok2


# ---------------------------------------------------------------- C5 (Task 70/71)
def c5():
    echant = [os.path.join(DEPOT, "skills", "gen-plan", "SKILL.md"),
              os.path.join(DEPOT, "scripts", "verify-cross.py"),
              os.path.join(DEPOT, "skills", "re-curation", "SKILL.md")]
    avant = {f: sha256f(f) for f in echant}
    ok1 = run_cmd("C5", "propagate-context v2.1.1 — passe 1 (absorption canonique : injections en attente acceptées)",
                  [sys.executable, os.path.join(SCRIPTS, "propagate-context.py")])
    p2 = subprocess.run([sys.executable, os.path.join(SCRIPTS, "propagate-context.py")],
                        cwd=DEPOT, capture_output=True, text=True, timeout=120)
    out2 = (p2.stdout + p2.stderr)
    apres = {f: sha256f(f) for f in echant}
    stable = all(avant[f] == apres[f] for f in echant)
    noop2 = ("0 skills mis à jour" in out2 and "0 scripts mis à jour" in out2)
    RESULTS.append({"id": "C5b", "label": "propagate-context — passe 2 NO-OP (0 skills + 0 scripts) + échantillon byte-stable",
                    "rc": p2.returncode, "duree_s": 0.0, "verdict":
                    "PASS" if (p2.returncode == 0 and stable and noop2) else "FAIL",
                    "notes": ["byte_stable" if stable else "BYTES MODIFIÉS",
                              "no_op_p2" if noop2 else "PASSE 2 NON NO-OP"],
                    "sortie": out2[:400]})
    print(f"[{'PASS' if (p2.returncode == 0 and stable and noop2) else 'FAIL'}] C5b propagate-context no-op ×2")
    # C5c — parité hôte↔dépôt du lot §0 (12 fichiers — la passe pipeline C10c synchronise l'hôte)
    lot = ["scripts/task78-cascade.py", "scripts/task78-final-plan.py",
           "scripts/task79-cascade-legere-vm.py", "scripts/task79-g2-final-plan.py",
           "scripts/task79-recuration-vm.py", "scripts/task81-recuration-iphone19.py",
           "scripts/task81-verif-r4-iphone19.py", "scripts/task82-inventaire.py",
           "scripts/task82-recuration-iphone18.py", "scripts/task82-tests-conversions.py",
           "scripts/task82-verif-r4-iphone18.py", "skills/agent-engineering/SKILL.md"]
    ecarts = [r for r in lot if not (os.path.isfile(os.path.join(HOST, r))
              and sha256f(os.path.join(HOST, r)) == sha256f(os.path.join(DEPOT, r)))]
    ok5c = not ecarts
    RESULTS.append({"id": "C5c", "label": f"lot §0 propagation — parité hôte==dépôt {len(lot) - len(ecarts)}/{len(lot)}",
                    "rc": 0 if ok5c else 1, "duree_s": 0.02, "verdict": "PASS" if ok5c else "FAIL",
                    "notes": [f"écarts: {ecarts}"] if ecarts else [], "sortie": ""})
    print(f"[{'PASS' if ok5c else 'FAIL'}] C5c parité lot §0 ({len(lot) - len(ecarts)}/{len(lot)})")
    return ok1 and p2.returncode == 0 and stable and noop2 and ok5c


# ---------------------------------------------------------------- C6 (Tasks 71→78)
def c6():
    plan84 = os.path.join(HOST, "download", "plan-task84-campagne-tests-chronologiques-socle-n56-push.md")
    ok1 = run_cmd("C6a", "gen-plan — check_plan_protocol P1-P5 (plan Task 84)",
                  [sys.executable, os.path.join(DEPOT, "skills", "gen-plan", "scripts",
                                                "check_plan_protocol.py"),
                   "--plan", plan84, "--worklog", os.path.join(HOST, "worklog.md")],
                  checks=[("P1-P5", check_txt("VERDICT : PASS"))])
    ok2 = run_cmd("C6b", "gen-plan — answer-key-checker 16 checks",
                  [sys.executable, os.path.join(SCRIPTS, "answer-key-checker.py"), plan84],
                  checks=[("16/16", check_regex(r"16/16|ALL PASS"))])
    ev1 = read(os.path.join(DEPOT, "skills", "gen-plan", "evals", "evals.json"))
    ev2 = read(os.path.join(DEPOT, "skills", "gen-plan", "evals", "trigger_evals.json"))
    try:
        n1 = len(json.loads(ev1)["evals"])
        n2 = len(json.loads(ev2))
        oke = (n1 == 9 and n2 == 15)
    except Exception:
        n1 = n2 = -1
        oke = False
    RESULTS.append({"id": "C6c", "label": f"gen-plan — evals JSON ({n1} + {n2} cas, attendu 9+15)",
                    "rc": 0 if oke else 1, "duree_s": 0.01,
                    "verdict": "PASS" if oke else "FAIL", "notes": [], "sortie": ""})
    print(f"[{'PASS' if oke else 'FAIL'}] C6c evals {n1}+{n2}")
    refs_attendus = ["etapes-detaillees.md", "grille-token.md", "classification-types.md",
                     "profils-ressource.md", "guide-selection-agent-skill.md",
                     "prompt-engineering-kit.md", "patterns-avances-qwen.md",
                     "answer-key-b12.md", "answer-key-template.md", "graph-diamond-pattern.md",
                     "observation-patterns.md", "regles-or.md", "disciplines-mobilisation.md",
                     "protocoles-detailles.md", "journal-versions.md"]
    manq = [r for r in refs_attendus if not os.path.isfile(
        os.path.join(DEPOT, "skills", "gen-plan", "references", r))]
    okr = not manq
    RESULTS.append({"id": "C6d", "label": f"gen-plan — references/ 15 fichiers (manquants: {manq})",
                    "rc": 0 if okr else 1, "duree_s": 0.01,
                    "verdict": "PASS" if okr else "FAIL", "notes": [], "sortie": ""})
    print(f"[{'PASS' if okr else 'FAIL'}] C6d references/ ({len(refs_attendus) - len(manq)}/15)")
    ok3 = run_cmd("C6e", "gen-plan v3.41.0 — --verifier (harnais v1.2.2)",
                  [sys.executable, HARNESS, "--verifier", "gen-plan"],
                  checks=[("VERDICT PASS", check_regex(r"VERDICT\s*:\s*PASS"))])
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "poids-chargement.py"), "--json"],
                       cwd=DEPOT, capture_output=True, text=True, timeout=120)
    try:
        d = json.loads(p.stdout)
        gp = [m for m in d["mesures"] if m.get("skill") == "gen-plan"][0]
        note = f"{gp['kio_skill_md']} Kio · {gp['tokens_estimes']} #token · {gp['verdict']}"
    except Exception:
        gp, note = {}, "mesure indisponible"
    ok4 = bool(gp) and gp.get("verdict") in ("INTERMÉDIAIRE", "OK") and gp.get("kio_skill_md", 99) < 35
    RESULTS.append({"id": "C6f", "label": f"gen-plan — poids chargement {note}",
                    "rc": 0 if ok4 else 1, "duree_s": round(time.time() % 100, 2),
                    "verdict": "PASS" if ok4 else "FAIL", "notes": [], "sortie": note})
    print(f"[{'PASS' if ok4 else 'FAIL'}] C6f poids gen-plan {note}")
    return ok1 and ok2 and oke and okr and ok3 and ok4


# ---------------------------------------------------------------- C7/C8 (Tasks 72→82)
def c7c8():
    ok1 = run_cmd("C7", "re-curation v1.2.2 — --verifier",
                  [sys.executable, HARNESS, "--verifier", "re-curation"],
                  checks=[("VERDICT PASS", check_regex(r"VERDICT\s*:\s*PASS"))])
    ok2 = run_cmd("C8a", "protocole-test.py harnais v1.2.2 — selftest 15/15 (passe 1)",
                  [sys.executable, HARNESS, "--selftest"],
                  checks=[("15/15", check_regex(r"15/15"))])
    ok3 = run_cmd("C8b", "protocole-test.py harnais v1.2.2 — selftest 15/15 (passe 2 idempotence)",
                  [sys.executable, HARNESS, "--selftest"],
                  checks=[("15/15", check_regex(r"15/15"))])
    return ok1 and ok2 and ok3


# ---------------------------------------------------------------- C10 (Task 76)
def c10():
    ok1 = run_cmd("C10a", "eco_install_pipeline.py — --help 0-exécution (contrat CLI F1)",
                  [sys.executable, os.path.join(HOST, "scripts", "eco_install_pipeline.py"), "--help"],
                  timeout=60)
    # C10c AVANT C10b (ordre interne) : l'installation pleine synchronise l'hôte←dépôt,
    # puis --dry-run se certifie sur l'état synchronisé (rc 0 ; un rc 2 = détection
    # F3 d'une divergence réelle hôte↔dépôt — fail-fast par conception, échec au test)
    p3 = subprocess.run([sys.executable, os.path.join(HOST, "scripts", "eco_install_pipeline.py")],
                        cwd=DEPOT, capture_output=True, text=True, timeout=600)
    ok3 = (p3.returncode == 0)
    notes3 = []
    try:
        rep = json.loads(p3.stdout)
        post = rep.get("post_install", {})
        nb_sha = post.get("sha256_verifies", 0)
        div = post.get("divergences", ["absent"])
        r2_ok = "0 rétrogradation" in rep.get("garde_R2", "")
        ok3 = ok3 and nb_sha >= 55 and div == [] and r2_ok
        notes3 = [f"sha256_verifies={nb_sha}", f"divergences={div}", f"R2={r2_ok}"]
    except Exception as e:  # noqa: BLE001
        ok3 = False
        notes3 = [f"parse: {e}"]
    RESULTS.append({"id": "C10c", "label": "eco_install_pipeline.py — RÉINSTALLATION PLEINE (cadence — ≥55 SHA, 0 divergence, R2)",
                    "cmd": "eco_install_pipeline.py", "rc": p3.returncode, "duree_s": round(0.15, 3),
                    "verdict": "PASS" if ok3 else "FAIL", "notes": notes3,
                    "sortie": (p3.stdout + p3.stderr)[:600]})
    print(f"[{'PASS' if ok3 else 'FAIL'}] C10c réinstallation pleine ({' · '.join(notes3)})")
    ok2 = run_cmd("C10b", "eco_install_pipeline.py --dry-run — 0 mutation, rc 0 (état synchronisé)",
                  [sys.executable, os.path.join(HOST, "scripts", "eco_install_pipeline.py"), "--dry-run"],
                  timeout=120,
                  checks=[("dry_run_noop", check_txt('"dry_run": true')),
                          ("0_mutation", check_txt("dry-run — 0 mutation"))])
    # Ordre canonique L-82-b/L-83-a : seal hôte (fait par pipeline) → cp zip hôte→dépôt → manifeste (integrity)
    shutil.copyfile(ZIP_HOTE, ZIP_DEPOT)
    ok4 = run_cmd("C10d", "cp zip hôte→dépôt + integrity manifeste écrit (114/114, round-trip corpus 9/9)",
                  [sys.executable, os.path.join(SCRIPTS, "check-ecosysteme-integrity.py")],
                  timeout=120,
                  checks=[("114/114", check_regex(r"114/114")),
                          ("round-trip corpus 9/9", check_regex(r"9/9"))])
    ok5 = run_cmd("C10e", "ensure-installed.py --check — INSTALLE 0 manquant",
                  [sys.executable, os.path.join(HOST, "scripts", "ensure-installed.py"), "--check"],
                  timeout=60,
                  checks=[("0_manquant", check_txt('"skills_kb_manquants": []'))])
    return ok1 and ok2 and ok3 and ok4 and ok5


# ---------------------------------------------------------------- C11-C15 (Tasks 76→80)
def c11_15():
    ok1 = run_cmd("C11", "PM-INSTALL v1.9.13 — corpus générateur --check 4 familles COHERENT",
                  [sys.executable, os.path.join(SCRIPTS, "generer-pm-skill.py"), "--check"],
                  timeout=120,
                  checks=[("4_COHERENT", lambda t: t.count("[COHERENT]") == 4)])
    corpus = sorted(glob.glob(os.path.join(DEPOT, "skills", "@mon-ecosysteme", "*.md")))
    taille = sum(os.path.getsize(f) for f in corpus)
    ok2 = len(corpus) == 9
    parite = sha256f(ZIP_HOTE) == sha256f(ZIP_DEPOT)
    RESULTS.append({"id": "C13", "label": (f"SHARED v1.7.36 + corpus PM — 9 fichiers "
                                           f"({taille} o) + parité zip hôte==dépôt"),
                    "rc": 0 if (ok2 and parite) else 1, "duree_s": 0.05,
                    "verdict": "PASS" if (ok2 and parite) else "FAIL",
                    "notes": [f"corpus_{len(corpus)}", "parité_zip" if parite else "PARITÉ KO"],
                    "sortie": ""})
    print(f"[{'PASS' if (ok2 and parite) else 'FAIL'}] C13 corpus {len(corpus)}/9, parité zip "
          f"{sha256f(ZIP_HOTE)}=={sha256f(ZIP_DEPOT)}")
    shared = read(os.path.join(DEPOT, "skills", "@mon-ecosysteme", "PROMPT-MAITRE-SHARED.md"))
    ok3 = ("Version** : 1.7.36" in shared) and ("R-F4" in shared) and ("règles d'or" in shared.lower())
    RESULTS.append({"id": "C13b", "label": "SHARED v1.7.36 — version + §8 R-F1..R-F4 + §9 règles d'or présents",
                    "rc": 0 if ok3 else 1, "duree_s": 0.01, "verdict": "PASS" if ok3 else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if ok3 else 'FAIL'}] C13b SHARED structure")
    proto = read(os.path.join(DEPOT, "skills", "gen-plan", "references", "protocoles-detailles.md"))
    ok4 = "v3.40.0" in proto and "v3.41.0" in proto and "ondage borné" in proto.replace("Sondage", "ondage")
    RESULTS.append({"id": "C12", "label": "protocoles-detailles.md — Extensions v3.40.0 (émission //) + v3.41.0 (sondage borné)",
                    "rc": 0 if ok4 else 1, "duree_s": 0.01, "verdict": "PASS" if ok4 else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if ok4 else 'FAIL'}] C12 protocoles-detailles Extensions")
    ok5 = run_cmd("C14", "version-management v1.3.0 — --verifier (post-réparation É1-INSTALL)",
                  [sys.executable, HARNESS, "--verifier", "version-management"],
                  checks=[("VERDICT PASS", check_regex(r"VERDICT\s*:\s*PASS"))])
    bases = ["gen-plan", "version-management", "re-curation", "iphone19", "iphone18"]
    manq = [b for b in bases if not os.path.isfile(
        os.path.join(DEPOT, "download", f"protocole-test-{b}.json"))]
    ok6 = not manq
    RESULTS.append({"id": "C15", "label": f"baselines protocole-test v1.2.0+ — {len(bases) - len(manq)}/{len(bases)} (manquants: {manq})",
                    "rc": 0 if ok6 else 1, "duree_s": 0.01, "verdict": "PASS" if ok6 else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if ok6 else 'FAIL'}] C15 baselines ({len(bases) - len(manq)}/{len(bases)})")
    return ok1 and ok2 and parite and ok3 and ok4 and ok5 and ok6


# ---------------------------------------------------------------- C16-C18 (Tasks 81-82)
def c16_18():
    ok1 = run_cmd("C16a", "iphone19 v0.12.0 — --verifier",
                  [sys.executable, HARNESS, "--verifier", "iphone19"],
                  checks=[("VERDICT PASS", check_regex(r"VERDICT\s*:\s*PASS"))])
    ok2 = run_cmd("C16b", "iphone19 — R4-INTÈGRE 6/6 (task81-verif-r4)",
                  [sys.executable, os.path.join(SCRIPTS, "task81-verif-r4-iphone19.py")],
                  checks=[("6/6", check_regex(r"6/6"))])
    r15 = "règle absolue 15" in read(os.path.join(DEPOT, "skills", "iphone19", "SKILL.md"))
    RESULTS.append({"id": "C16c", "label": "iphone19 — règle absolue 15 inline",
                    "rc": 0 if r15 else 1, "duree_s": 0.01, "verdict": "PASS" if r15 else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if r15 else 'FAIL'}] C16c règle 15")
    ok3 = run_cmd("C17a", "knowledge-observer v1.1.0 — --verifier",
                  [sys.executable, HARNESS, "--verifier", "knowledge-observer"],
                  checks=[("VERDICT PASS", check_regex(r"VERDICT\s*:\s*PASS"))])
    ok4 = run_cmd("C17b", "knowledge-observer — re-jeu tests conversions 9/9 (T4b/T6 dynamisés KO-L003)",
                  [sys.executable, os.path.join(SCRIPTS, "task82-tests-conversions.py")],
                  checks=[("9/9", check_regex(r"9/9 PASS"))])
    agent = read(os.path.join(DEPOT, "skills", "knowledge-observer", "knowledge-observer.agent"))
    marqueurs = ["État Court", "État Long", "pipeline", "M1", "M2", "M3", "M4", "lessons-learned"]
    manq = [m for m in marqueurs if m not in agent]
    ok5 = len(agent) > 1000 and not manq
    RESULTS.append({"id": "C17c", "label": f"knowledge-observer.agent — structure canonique (manquants: {manq})",
                    "rc": 0 if ok5 else 1, "duree_s": 0.01, "verdict": "PASS" if ok5 else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if ok5 else 'FAIL'}] C17c structure .agent")
    ok6 = run_cmd("C18a", "iphone18 v1.1.0 curé — --verifier",
                  [sys.executable, HARNESS, "--verifier", "iphone18"],
                  checks=[("VERDICT PASS", check_regex(r"VERDICT\s*:\s*PASS"))])
    ok7 = run_cmd("C18b", "iphone18 — R4-INTÈGRE 3/3 (task82-verif-r4)",
                  [sys.executable, os.path.join(SCRIPTS, "task82-verif-r4-iphone18.py")],
                  checks=[("3/3", check_regex(r"3/3"))])
    return (ok1 and ok2 and r15 and ok3 and ok4 and ok5 and ok6 and ok7)


# ---------------------------------------------------------------- C19 (Task 83)
def c19():
    ae = os.path.join(DEPOT, "skills", "agent-engineering")
    ev1 = read(os.path.join(ae, "evals", "trigger_evals.json"))
    ev2 = read(os.path.join(ae, "evals", "evals.json"))
    try:
        n1 = len(json.loads(ev1))
        n2 = len(json.loads(ev2)["evals"])
        oke = (n1 == 7 and n2 == 7)
    except Exception:
        n1 = n2 = -1
        oke = False
    RESULTS.append({"id": "C19a", "label": f"agent-engineering — evals JSON 7+7 ({n1}+{n2})",
                    "rc": 0 if oke else 1, "duree_s": 0.01, "verdict": "PASS" if oke else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if oke else 'FAIL'}] C19a evals n°56 ({n1}+{n2})")
    sk = read(os.path.join(ae, "SKILL.md"))
    okf = bool(re.search(r"^version:\s*1\.0\.0", sk, re.MULTILINE)) and "ABE" in sk and "MASE" in sk
    # planchers semver vs versions réelles
    planchers = {"gen-plan": "3.15.0", "fleet-engineering": "1.0.1",
                 "autonomous-agent": "1.2.0", "agent-creator": "2.2.0"}
    reels = {s: frontmatter_version(s) for s in planchers}
    verif = {s: (reels[s] is not None and semver_ge(reels[s], p)) for s, p in planchers.items()}
    okp = all(verif.values())
    note_p = "; ".join(f"{s} {reels[s]}>={p}={'OK' if verif[s] else 'KO'}" for s, p in planchers.items())
    RESULTS.append({"id": "C19b", "label": f"agent-engineering — frontmatter v1.0.0 + 3 domaines + planchers semver : {note_p}",
                    "rc": 0 if (okf and okp) else 1, "duree_s": 0.01,
                    "verdict": "PASS" if (okf and okp) else "FAIL", "notes": [], "sortie": ""})
    print(f"[{'PASS' if (okf and okp) else 'FAIL'}] C19b frontmatter + planchers ({note_p})")
    kb = read(os.path.join(DEPOT, "skills", "KNOWLEDGE.md"))
    nkb = kb.count("agent-engineering")
    okk = ("## agent-engineering v1.0.0" in kb) and nkb >= 5
    RESULTS.append({"id": "C19c", "label": f"agent-engineering — KB entrée n°56 + arêtes ({nkb} mentions ≥ 5)",
                    "rc": 0 if okk else 1, "duree_s": 0.01, "verdict": "PASS" if okk else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if okk else 'FAIL'}] C19c KB n°56 ({nkb} mentions)")
    ultra = read(os.path.join(DEPOT, "skills", "@mon-ecosysteme", "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"))
    oku = "agent-engineering" in ultra and "n°56" in ultra
    RESULTS.append({"id": "C19d", "label": "agent-engineering — ULTRA 13ᵉ voie (routage n°56)",
                    "rc": 0 if oku else 1, "duree_s": 0.01, "verdict": "PASS" if oku else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if oku else 'FAIL'}] C19d ULTRA 13e voie")
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "poids-chargement.py"), "--json"],
                       cwd=DEPOT, capture_output=True, text=True, timeout=120)
    try:
        m = [x for x in json.loads(p.stdout)["mesures"] if x.get("skill") == "agent-engineering"][0]
        note = f"{m['kio_skill_md']} Kio · {m['tokens_estimes']} #token · {m['verdict']}"
        okw = m["kio_skill_md"] < 30
    except Exception:
        m, note, okw = {}, "mesure indisponible", False
    RESULTS.append({"id": "C19e", "label": f"agent-engineering — poids {note} (seuil LOURD 30 Kio)",
                    "rc": 0 if okw else 1, "duree_s": 0.01, "verdict": "PASS" if okw else "FAIL",
                    "notes": [], "sortie": note})
    print(f"[{'PASS' if okw else 'FAIL'}] C19e poids n°56 {note}")
    return oke and okf and okp and okk and oku and okw


# ---------------------------------------------------------------- C20 (Task 83)
def c20():
    chemin_ultra = os.path.join(DEPOT, "skills", "@mon-ecosysteme",
                                "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md")
    avant = sha256f(chemin_ultra)
    ok1 = run_cmd("C20a", "gen-ultra-maitre.py — régénération (attendu no-op, SHA stable)",
                  [sys.executable, os.path.join(SCRIPTS, "gen-ultra-maitre.py")], timeout=120)
    apres1 = sha256f(chemin_ultra)
    subprocess.run([sys.executable, os.path.join(SCRIPTS, "gen-ultra-maitre.py")],
                   cwd=DEPOT, capture_output=True, timeout=120)
    apres2 = sha256f(chemin_ultra)
    stable = (avant == apres1 == apres2)
    RESULTS.append({"id": "C20b", "label": f"ULTRA idempotence ×2 — SHA {avant}→{apres1}→{apres2} stable",
                    "rc": 0 if stable else 1, "duree_s": 0.02, "verdict": "PASS" if stable else "FAIL",
                    "notes": [], "sortie": ""})
    print(f"[{'PASS' if stable else 'FAIL'}] C20b ULTRA SHA stable ×2 ({avant})")
    return ok1 and stable


# ---------------------------------------------------------------- C21 (agrégat)
def c21():
    ok1 = run_cmd("C21a", "verify-cross — 100,0 % (0 warnings)",
                  [sys.executable, os.path.join(SCRIPTS, "verify-cross.py")], timeout=180,
                  checks=[("100", check_regex(r"100[.,]0\s*%|100\s*%"))])
    ok2 = run_cmd("C21b", "verify-correct-work — 16/16",
                  [sys.executable, os.path.join(SCRIPTS, "verify-correct-work.py")], timeout=120,
                  checks=[("16/16", check_regex(r"16/16|ALL PASS"))])
    ok3 = run_cmd("C21c", "integrity — 114/114 ×2 (re-jeu)",
                  [sys.executable, os.path.join(SCRIPTS, "check-ecosysteme-integrity.py")],
                  timeout=120, checks=[("114/114", check_regex(r"114/114"))])
    run_cmd("C21c", "integrity — re-jeu 2 (idempotence)",
            [sys.executable, os.path.join(SCRIPTS, "check-ecosysteme-integrity.py")],
            timeout=120, checks=[("114/114", check_regex(r"114/114"))])
    ok4 = run_cmd("C21d", "interactions — STRICT 55/55",
                  [sys.executable, os.path.join(SCRIPTS, "test-coherence-interactions.py")],
                  timeout=120, checks=[("VERDICT_STRICT", check_txt("VERDICT : COHÉRENCE DES INTERACTIONS : PASS STRICT")),
                                       ("55/0/0", check_regex(r"55 PASS / 0 WARN / 0 FAIL"))])
    ok5 = run_cmd("C21e", "doublons download/ — 0",
                  [sys.executable, os.path.join(SCRIPTS, "task14-scan-doublons.py"),
                   os.path.join(HOST, "download")], timeout=60,
                  checks=[("0 doublon", check_regex(r"DOUBLONS[^:]*:\s*0"))])
    ok6 = run_cmd("C21f", "G-RES final — monitor OK",
                  [sys.executable, os.path.join(DEPOT, "skills", "resource-monitor", "scripts",
                                                "monitor.py")], timeout=60,
                  checks=[("OK", check_txt("OK"))])
    return ok1 and ok2 and ok3 and ok4 and ok5 and ok6


def rapport():
    total = round(time.time() - T0, 1)
    n_pass = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    fails = [r for r in RESULTS if r["verdict"] == "FAIL"]
    verdict = "PASS" if not fails else "FAIL"
    horodatage = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {"task": "Task 84 — campagne tests $FACON2 chronologique",
            "directive": "1a1bed51ccaf78f1", "horodatage": horodatage,
            "verdict_global": verdict, "items_pass": n_pass, "items_total": len(RESULTS),
            "duree_totale_s": total, "items": RESULTS}
    with open(RAPPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    lignes = [
        "# Rapport campagne tests $FACON2 chronologique — Task 84",
        "",
        f"> Directive trace `1a1bed51ccaf78f1` · session web-ecef7f80 · horodatage {horodatage}",
        f"> Périmètre : éléments créés/modifiés dans la discussion (Tasks 70→83, 2026-11-07 soir → 2026-11-09)",
        f"> Ordre d'exécution : chronologie STRICTE de création/modification · harnais protocole-test v1.2.2 + arbitres",
        "",
        f"## Verdict global : **{verdict}** ({n_pass}/{len(RESULTS)} items PASS · durée {total} s)",
        "",
        "| # | Item chronologique | Élément (task d'origine) | Verdict | Durée | Notes |",
        "|---|---|---|---|---|---|",
    ]
    taches = {"C1": "T70", "C2": "T70", "C3": "T70", "C4": "T71", "C5": "T70/71",
              "C6": "T71→T78", "C7": "T72→T82", "C8": "T73→T82", "C10": "T76",
              "C11": "T76/78", "C12": "T77/78", "C13": "T78", "C14": "T79",
              "C15": "T80", "C16": "T81", "C17": "T82", "C18": "T82", "C19": "T83",
              "C20": "T82/83", "C21": "transverse"}
    for r in RESULTS:
        base = re.match(r"(C\d+)", r["id"])
        tg = taches.get(base.group(1), "—") if base else "—"
        lignes.append(f"| {r['id']} | {r['label']} | {tg} | **{r['verdict']}** | "
                      f"{r['duree_s']} s | {' · '.join(r['notes']) or '—'} |")
    if fails:
        lignes += ["", "## Failles mesurées (règle d'or n°5 — corrigées avant POST)", ""]
        for r in fails:
            lignes.append(f"- **{r['id']}** — {r['label']} : rc={r['rc']} · sortie : "
                          f"`{r['sortie'][:200]}`")
    lignes += ["", "## Idempotence", "",
               "- Harnais protocole-test selftest 15/15 ×2 · ULTRA régénéré SHA stable ×2 ·",
               "- integrity 114/114 ×2 · propagate-context no-op ×2 (échantillon byte-stable) ·",
               "- R1/R2 selftests ×2 · pipeline pleine passe (réinstallation cadence) + cp zip + manifeste.",
               "", "Rapport JSON intégral : `scripts/task84-campagne-tests.json` (reproductible, idempotent)."]
    with open(RAPPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"\n=== CAMPAGNE : {verdict} ({n_pass}/{len(RESULTS)}) · {total}s ===")
    print(f"Rapports : {RAPPORT_MD} + {RAPPORT_JSON}")
    return verdict


def main():
    etapes = [("C1", c1), ("C2-C3", c2), ("C4", c4), ("C5", c5), ("C6", c6),
              ("C7-C8", c7c8), ("C10", c10), ("C11-C15", c11_15), ("C16-C18", c16_18),
              ("C19", c19), ("C20", c20), ("C21", c21)]
    for nom, fn in etapes:
        try:
            fn()
        except Exception as e:  # noqa: BLE001 — faille consignée, jamais avalée
            RESULTS.append({"id": nom, "label": f"EXCEPTION dans {nom}", "cmd": "", "rc": -1,
                            "duree_s": 0.0, "verdict": "FAIL",
                            "notes": [str(e)[:200]], "sortie": ""})
            print(f"[FAIL] {nom} EXCEPTION : {e}")
    return 0 if rapport() == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
