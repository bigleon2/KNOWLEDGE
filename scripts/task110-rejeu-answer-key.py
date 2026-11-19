#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 110 — Re-jeu mécanique de l'answer key D001-D010 (lecture seule).

Ré-exécute chaque verification du plan download/plan-task110-go-futur-f3-f2-go3-cw-clone.md
et imprime le tableau criterion/obtenu/verdict (pattern task107-rejeu-answer-key.py).
"""
import subprocess
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")

DECISIONS = [
    ("D001", "Périmètre GO = tâches 3-4-5 ; tâches 1/6/7/8 hors périmètre",
     'python3 -c "from pathlib import Path; t=Path(\'download/taches-restantes-task108.md\').read_text(encoding=\'utf-8\'); p=Path(\'download/plan-task110-go-futur-f3-f2-go3-cw-clone.md\').read_text(encoding=\'utf-8\'); assert \'## 3. Correctif structurel F3\' in t and \'## 4. Correctif structurel F2\' in t and \'### 5. GO-3\' in t and \'HORS périmètre\' in p and \'cron 531684\' in p"'),
    ("D002", "Injecteur v2.2.0 : re.sub robuste + DRY + insertion après docstring + remplacement 2 formes",
     "python3 scripts/task110-test-injecteur.py > /dev/null"),
    ("D003", "5 scripts protégés portent bloc §0 v1.7.40 ×2 arbres, 0 SyntaxError",
     'python3 -c "from pathlib import Path; import py_compile; noms=[\'task98-simulation-extinction.py\',\'task101-scan-differes.py\',\'task102-extraction-blocs.py\',\'task104-genere-fiche.py\',\'task106-inventaire-familles.py\']; [py_compile.compile(str(Path(t)/\'scripts\'/n), doraise=True) for t in [\'.\',\'KNOWLEDGE-repo\'] for n in noms]; assert all(\'CONTEXTE SYSTÈME\' in (Path(t)/\'scripts\'/n).read_text(encoding=\'utf-8\') for t in [\'.\',\'KNOWLEDGE-repo\'] for n in noms)"'),
    ("D004", "Non-régression : bootstrap inchangé + idempotence + certification 6/6",
     "python3 scripts/certification-complete.py > /dev/null"),
    ("D005", "Scelleur v2.4 discrimine PERTE/ÉVOLUTION/drapeau (harnais T1-T5)",
     "python3 scripts/task110-test-scelleur.py > /dev/null"),
    ("D006", "Pipeline repointé v24 ×2 arbres (3 références) + exécution réelle byte-stable",
     'python3 -c "from pathlib import Path; p=Path(\'scripts/eco_install_pipeline.py\').read_text(encoding=\'utf-8\'); r=Path(\'KNOWLEDGE-repo/scripts/eco_install_pipeline.py\').read_text(encoding=\'utf-8\'); assert p==r and p.count(\'task-f5-seal-archive-v24.py\')==2 and p.count(\'task-f5-seal-archive-v23.py\')==1"'),
    ("D007", "Canons v1.2.0 portent la convention + cascade ×2 arbres",
     'python3 -c "from pathlib import Path; c=chr(39); assert all((\'version: 1.2.0\' in (Path(t)/\'skills\'/sk/\'SKILL.md\').read_text(encoding=\'utf-8\')) and ((\'docstring d\'+c+\'abord\') in (Path(t)/\'skills\'/sk/\'SKILL.md\').read_text(encoding=\'utf-8\').replace(chr(8217), c)) for t in [\'.\',\'KNOWLEDGE-repo\'] for sk in [\'script-creator\',\'correct-py\'])"'),
    ("D008", "tool-routing N1 PASS (inchangé avant/après)",
     "python3 scripts/check-tool-routing.py > /dev/null"),
    ("D009", "Clôture : worklog parité + rapports CW/clone présents",
     'python3 -c "import hashlib; from pathlib import Path; h=hashlib.md5(Path(\'worklog.md\').read_bytes()).hexdigest(); r=hashlib.md5(Path(\'KNOWLEDGE-repo/worklog.md\').read_bytes()).hexdigest(); assert h==r and (Path(\'download/rapport-cw-task110-projet.md\')).exists() and (Path(\'download/clone-chat-session-web-ecef7f80-20261119-task110.md\')).exists()"'),
    ("D010", "0 PAT ce tour : commit local non poussé (pendance)",
     'python3 -c "import subprocess; r=subprocess.run([\'git\',\'rev-list\',\'--count\',\'origin/main..HEAD\'],capture_output=True,text=True,cwd=\'KNOWLEDGE-repo\'); assert int(r.stdout.strip())>=1"'),
]


def main() -> int:
    print("=== Re-jeu answer key Task 110 (D001-D010) — lecture seule ===")
    passes = 0
    for did, critere, cmd in DECISIONS:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(RACINE))
        ok = r.returncode == 0
        passes += ok
        print("  [%s] %s — %s" % ("verified" if ok else "FAILED", did, critere))
        if not ok:
            print("        détail : %s" % (r.stderr.strip()[-200:] or r.stdout.strip()[-200:]))
    print("=== RESUME : %d/%d verified ===" % (passes, len(DECISIONS)))
    return 0 if passes == len(DECISIONS) else 1


if __name__ == "__main__":
    sys.exit(main())
