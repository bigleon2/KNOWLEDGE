#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Arbitre dédié de session — answer key Task 15 (6 décisions D001-D006, 16 checks).

Vérifie MÉCANIQUEMENT que chaque décision du plan Task 15 (traitement des
décisions restantes : S3 dormants, 64 enveloppes, tmp/, rétro-sync) est bien
l'état réel de l'écosystème local (boucle E12-E13 du PM gen-plan v3.21.0).
"""
import hashlib
import json
import os
import subprocess
import zipfile

BASE = "/home/z/my-project/work_knowledge"
SCRIPTS = os.path.join(BASE, "scripts")
DOWNLOAD = os.path.join(BASE, "download")
RAPPORT = os.path.join(DOWNLOAD, "rapport-task15-decisions-restantes.md")
WORKLOG = os.path.join(BASE, "worklog.md")
EXTERNAL = "/home/z/my-project/worklog.md"

# liste pré-exécution (capturée du report Task 14 avant normalisation — git HEAD b36f177)
IGNORES_AVANT = ["ASR", "LLM", "TTS", "VLM", "agent-browser", "ai-news-collectors", "aminer-daily-paper", "aminer-deep-search", "anti-pua", "auto-target-tracker", "blog-writer", "charts", "cheat-sheet", "coding-agent", "content-strategy", "contentanalysis", "design", "docx", "dream-interpreter", "experiment-suite", "finance", "fullstack-dev", "gaokao-collect-student-info", "gaokao-fetch-volunteers", "gaokao-generate-report", "gaokao-recommend-majors", "gaokao-recommend-schools", "get-fortune-analysis", "gift-evaluator", "image-edit", "image-generation", "image-search", "image-understand", "interview-designer", "interview-prep", "jd-resume-tailor", "job-intent-tracker", "literature-survey", "market-research-reports", "marketing-mode", "mindfulness-meditation", "multi-search-engine", "pdf", "podcast-generate", "pptx", "qingyan-research", "quiz-html", "quiz-mastery", "research-explorer", "resume-builder", "seo-content-writer", "stock-analysis-skill", "storyboard-manager", "study-buddy", "task-review", "ui-ux-pro-max", "video-generation", "video-understand", "visual-design-foundations", "web-reader", "web-search", "web-shader-extractor", "writing-plans", "xlsx"]
DORMANTS = [
    "task17-aveugle-pms.py", "task17-baseline-a2.py", "task17-rapport-baseline.py",
    "task18-baseline-a2-memory.py", "task21-f3-status-mesure.py",
    "task21-p2b-description-optimization-pass2.py", "task21-p2b-kb-decision.py",
    "task21-p2b-kb-sync.py", "task21-p4b-agents-fixes-pass2.py",
    "task23-complete-frontmatters.py", "task23-install-minimale.py",
]
MD5_INCHANGES = {  # référence pré-exécution (md5 8 premiers hex)
    "check-triggers-replay.py": "d4563d6f",
    "verify-cross.py": "8ecc3ec9",
    "test-coherence-interactions.py": "65c91b4a",
    "generer-pm-skill.py": "ad736c28",
    "verify-correct-work.py": "ced99ef7",
    "verify-registry-sync.py": "0af7f53d",
    "answer-key-checker.py": "ef563c44",
}

results = []


def check(did, label, ok):
    results.append((did, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {did} — {label}")


def md5_8(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]


def main():
    print("=== ANSWER KEY TASK 15 — vérification mécanique D001-D006 (16 checks) ===")

    # D001 — normalisation 64 enveloppes → bare-liste canonique (512 cas verbatim)
    lists = 0
    total_cas = 0
    for sk in IGNORES_AVANT:
        p = os.path.join(BASE, "skills", sk, "evals", "trigger_evals.json")
        try:
            x = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(x, list):
            lists += 1
            total_cas += len(x)
    check("D001.1", f"64/64 trigger_evals.json en bare-liste canonique (ignores pré-exécution)", lists == 64)
    check("D001.2", "512 cas verbatim préservés (8/skill)", total_cas == 512)
    rep = json.load(open(os.path.join(SCRIPTS, "triggers-replay-report.json"), encoding="utf-8"))
    check("D001.3", "replay : ignores_schema_non_canonique=0, n_skills=93",
          rep.get("ignores_schema_non_canonique") == [] and rep.get("n_skills") == 93)
    check("D001.4", "0 fix instrument (md5 check-triggers-replay + verify-cross inchangés)",
          md5_8(os.path.join(SCRIPTS, "check-triggers-replay.py")) == MD5_INCHANGES["check-triggers-replay.py"]
          and md5_8(os.path.join(SCRIPTS, "verify-cross.py")) == MD5_INCHANGES["verify-cross.py"])

    # D002 — re-scellement archive 28→27 (suppression d72226a sanctionnée)
    integ = json.load(open(os.path.join(SCRIPTS, "ecosysteme-integrity.json"), encoding="utf-8"))
    absent = "clone-discussion-2026-09-27-ecosysteme-knowledge-b13-r7-f.md"
    check("D002.1", "integrity.json calibré : archive=27, corpus=27, fichier supprimé absent des 2 dicts",
          len(integ["archive"]) == 27 and len(integ["corpus"]) == 27
          and absent not in integ["archive"] and absent not in integ["corpus"])
    zip_path = os.path.join(DOWNLOAD, "mon-ecosysteme_archive.zip")
    corpus_dir = os.path.join(BASE, "skills", "@mon-ecosysteme")
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        corpus_files = sorted(f for f in os.listdir(corpus_dir) if os.path.isfile(os.path.join(corpus_dir, f)))
        roundtrip = all(any(m.split("@mon-ecosysteme/")[-1] == f
                            and z.read(m) == open(os.path.join(corpus_dir, f), "rb").read()
                            for m in names) for f in corpus_files)
    check("D002.2", "archive 27 entrées, round-trip corpus ⊆ archive byte-identique",
          len(names) == 27 and roundtrip)
    r1 = subprocess.run(["python3", os.path.join(SCRIPTS, "check-ecosysteme-integrity.py"), "--check"],
                        capture_output=True, text=True, timeout=120)
    check("D002.3", "integrity --check 60/60 rc0", r1.returncode == 0 and "60/60" in r1.stdout)
    r2 = subprocess.run(["python3", os.path.join(SCRIPTS, "test-coherence-interactions.py")],
                        capture_output=True, text=True, timeout=180)
    check("D002.4", "coherence verdict PASS (PASS ou PASS AVEC RÉSERVES)",
          "VERDICT : COHÉRENCE DES INTERACTIONS : PASS" in r2.stdout)

    # D003 — archivage des 11 dormants (finding S3), 9 vivants intacts
    arch_dir = os.path.join(SCRIPTS, "_archive")
    arch = sorted(os.listdir(arch_dir)) if os.path.isdir(arch_dir) else []
    check("D003.1", "11 dormants présents dans scripts/_archive/",
          all(n in arch for n in DORMANTS))
    stale_restant = sorted(p for p in os.listdir(SCRIPTS)
                           if p.endswith(".py") and p != "task15-answer-key-check.py"
                           and b"my-project/ecosystem" in open(
                               os.path.join(SCRIPTS, p), "rb").read())
    check("D003.2", "0 dormant restant (0 « my-project/ecosystem » hors _archive/ à la racine scripts/ ; auto-référence checker exclue)",
          not stale_restant, )
    md5_ok = all(md5_8(os.path.join(SCRIPTS, k)) == v for k, v in MD5_INCHANGES.items()
                 if k not in ("check-triggers-replay.py", "verify-cross.py"))
    check("D003.3", "5 instruments stables md5 inchangés (integrity/coherence/generer-pm/vcw/registry/akc)",
          md5_ok)

    # D004 — disposition tmp/ (13 artefacts reproductibles)
    check("D004.1", "tmp/ absent du dépôt", not os.path.exists(os.path.join(BASE, "tmp")))
    rap = open(RAPPORT, encoding="utf-8").read() if os.path.exists(RAPPORT) else ""
    check("D004.2", "inventaire tmp/ documenté au rapport (13 artefacts, sources de régénération)",
          "r5-token-dashboard.json" in rap and "vrs-full.json" in rap and "13" in rap)

    # D005 — rétro-sync verbatim 0→14-CW + préambule campagne
    wl = open(WORKLOG, encoding="utf-8").read()
    ids_uniques = ["Task ID: 0\n", "Task ID: 1 ", "Task ID: 2 ", "Task ID: 3 ", "Task ID: 4",
                   "Task ID: 5 ", "Task ID: 6", "Task ID: 7", "Task ID: P3", "Task ID: 8",
                   "Task ID: 11", "Task ID: 14-S0", "Task ID: 14-CW"]
    check("D005.1", "entrées de campagne portées au worklog du dépôt (13 IDs uniques + homonymes 12/13/13-commit/13-push/14)",
          all(i in wl for i in ids_uniques) and "Task ID: 13-commit" in wl and "Task ID: 13-push" in wl)
    check("D005.2", "préambule rétro-sync présent + ancienne campagne intacte (web-8a7e5653)",
          "Rétro-sync du worklog du dépôt" in wl
          and "installation locale écosystème" in wl  # marqueur ancienne campagne Task 12
          and wl.count("Task ID: 12") >= 2 and wl.count("Task ID: 14\n") >= 2)

    # D006 — règle d'or n°2 : HEAD inchangé
    head = subprocess.run(["git", "-C", BASE, "rev-parse", "--short=7", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    check("D006", f"HEAD inchangé b36f177 pendant toute l'exécution (0 commit) — {head}", head == "b36f177")

    n_pass = sum(1 for _, ok in results if ok)
    print(f"=== RÉSUMÉ : {n_pass}/{len(results)} PASS ===")
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
