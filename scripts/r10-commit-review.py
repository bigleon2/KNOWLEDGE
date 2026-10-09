#!/usr/bin/env python3
"""R10 — Revue de commit par agent de code avant publication locale (Task 36, vague 2).
Couche D007 du protocole de commit : revue mécanique AVANT tout commit local
du dépôt écosystème. Checks : py_compile des .py modifiés, secrets, SKILL.md
frontmatter délimité, taille des nouveaux fichiers. Verdict + JSON, code retour.
Usage : r10-commit-review.py [--repo <chemin>]  (défaut : dépôt écosystème)
"""
import os, py_compile, re, subprocess, sys, tempfile, time, json

SECRET_RE = re.compile(r"(?i)(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|api[_-]?key\s*=\s*['\"][A-Za-z0-9]{16,})")
OUT = "/home/z/my-project/work_knowledge/tmp/r10-commit-review.json"

def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True).stdout

def main():
    repo = sys.argv[sys.argv.index("--repo") + 1] if "--repo" in sys.argv else "/home/z/my-project/work_knowledge"
    status = git(repo, "status", "--porcelain").splitlines()
    checks, fails = [], []
    tmpd = tempfile.mkdtemp(prefix="r10-")
    for i, line in enumerate(status):
        flag, path = line[:2].strip(), line[3:].strip()
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            checks.append({"fichier": path, "flag": flag, "statut": "supprimé/absent — skip"})
            continue
        if os.path.getsize(full) > 5 * 1024 * 1024 and flag in ("A", "??"):
            fails.append({"fichier": path, "raison": "nouveau fichier > 5 Mo"})
            checks.append({"fichier": path, "flag": flag, "statut": "FAIL taille"})
            continue
        if path.endswith(".py"):
            try:
                py_compile.compile(full, doraise=True, cfile=os.path.join(tmpd, f"c{i}.pyc"))
                checks.append({"fichier": path, "flag": flag, "statut": "py_compile OK"})
            except py_compile.PyCompileError as e:
                fails.append({"fichier": path, "raison": f"py_compile: {str(e)[:120]}"})
                checks.append({"fichier": path, "flag": flag, "statut": "FAIL syntaxe"})
                continue
        if path.endswith("SKILL.md"):
            with open(full, encoding="utf-8", errors="replace") as f:
                head = f.read(4000)
            ok = head.count("---") >= 2
            checks.append({"fichier": path, "flag": flag, "statut": "frontmatter OK" if ok else "FAIL délimitation"})
            if not ok:
                fails.append({"fichier": path, "raison": "frontmatter non délimité (règle Task 33)"})
            continue
        with open(full, "rb") as f:
            blob = f.read()
        if SECRET_RE.search(blob.decode("utf-8", errors="replace")):
            fails.append({"fichier": path, "raison": "motif secret détecté"})
            checks.append({"fichier": path, "flag": flag, "statut": "FAIL secrets"})
            continue
        checks.append({"fichier": path, "flag": flag, "statut": "OK"})
    verdict = "PASS" if not fails else "FAIL"
    out = {
        "regle": "R10 — revue de commit par agent de code avant publication locale (couche D007)",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "repo": repo,
        "fichiers_en_examen": len(status),
        "verdict": verdict,
        "fails": fails,
        "checks": checks,
        "protocole": "avant tout commit local : python3 scripts/r10-commit-review.py → PASS requis",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"R10 : {len(status)} fichier(s) en examen → {verdict}"
          + (f" ({len(fails)} échec(s))" if fails else " — prêt au commit"))
    return 0 if verdict == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
