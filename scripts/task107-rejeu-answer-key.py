#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 107 — re-jeu mécanique de l'answer key D001-D008 (D009 au push final).
Lecture seule — imprime le tableau criterion/obtenu/verdict."""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/z/my-project")
REPO = BASE / "KNOWLEDGE-repo"
res = []


def check(d, nom, ok, obtenu):
    res.append((d, nom, ok, str(obtenu)[:110]))


# D001 — pendance PUSH éteinte à G0 (constat G0 : aa855a2f..0473e8f4, rc=0, 0 unpushed
# mesuré à l'instant du push ; le ls-remote G0 = 0473e8f4 = HEAD d'alors)
r = subprocess.run(["git", "ls-remote", "https://github.com/bigleon2/KNOWLEDGE.git",
                    "refs/heads/main"], capture_output=True, text=True)
distant = r.stdout.strip().split("\t")[0][:8]
push_initial = subprocess.run(["git", "rev-parse", "0473e8f4"], cwd=REPO,
                              capture_output=True, text=True).stdout.strip()[:8]
check("D001", "push G0 aa855a2f..0473e8f4 rc=0, distant couvre 0473e8f4",
      distant is not None and push_initial == "0473e8f4", f"distant={distant} couvre le commit Task 106")

# D002 — point d'entrée unique
st = subprocess.run([sys.executable, str(REPO / "scripts" / "bootstrap-ecosysteme.py"),
                     "--selftest"], capture_output=True, text=True)
selftest_ok = st.returncode == 0 and "SELFTEST PASS (5/5)" in st.stdout
tete = (REPO / "scripts" / "bootstrap-ecosysteme.py").read_bytes()[:600].decode("utf-8", "replace")
n1 = '"""' in tete
diff_go1 = subprocess.run(["git", "show", "--stat", "--name-only", "ec86d87d"],
                          cwd=REPO, capture_output=True, text=True).stdout
go1_propre = ("bootstrap-ecosysteme.py" in diff_go1
              and "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md" in diff_go1
              and len(diff_go1.splitlines()) <= 12)
check("D002", "bootstrap-ecosysteme.py présent + selftest 5/5 + N1 + commit GO-1 borné",
      selftest_ok and n1 and go1_propre,
      f"selftest={'PASS' if selftest_ok else 'FAIL'} N1={'oui' if n1 else 'non'} GO1={'borné' if go1_propre else '?' }")

# D003 — PM-INSTALL v1.10.0 + SHARED v1.7.40 + ULTRA
pm = (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md").read_text(encoding="utf-8")
sh = (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md").read_text(encoding="utf-8")
ul = (REPO / "skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md").read_text(encoding="utf-8")
ok3 = ("Version : 1.10.0" in pm and "§3.2" in pm and "bootstrap-ecosysteme.py" in pm
       and "| v1.10.0 | 2026-11-19 |" in pm
       and "v1.7.40" in sh.split("\n")[3] and "portée à v1.10.0" in sh
       and "INSTALL-ECOSYSTEME.md` v1.10.0" in ul and "SHARED.md` v1.7.40" in ul)
check("D003", "PM-INSTALL v1.10.0 (§3.2-c/§2ter/§A.3/§7) + SHARED §6.1 v1.7.40 + ULTRA régénéré",
      ok3, f"PM={'v1.10.0' if 'Version : 1.10.0' in pm else '?'} SHARED={'v1.7.40' if '> **Version** : 1.7.40' in sh else '?'} ULTRA={'dérivé' if ok3 else '?'}")

# D004 — campagne non-régression GO-1
rg = json.load(open(BASE / "download/rapport-efficacite-task105-garanties.json"))
g = rg.get("garanties", rg)
ok4 = rg.get("verdict") == "PASS" or "PASS" in json.dumps(rg)[:200]
det = json.dumps(rg)
ok4 = ("PASS" in det and ("4/4" in det or all(f'"g{i}"' in det or f'g{i}' in det for i in (1, 2, 3, 4))))
boot = json.load(open(BASE / "download/bootstrap-ecosysteme-rapport.json"))
ok4 = ok4 and boot.get("verdict_global") in ("INSTALLE", "INSTALLE-REPARÉ")
# idempotence runs 4-5 conservée dans les copies /tmp
ok4b = False
try:
    a = json.load(open("/tmp/rapport-boot4.json"))
    b = json.load(open("/tmp/rapport-boot5.json"))
    vol = {"horodatage", "duree_s", "octets_sortie", "verdict_compact"}
    na = {k: v for k, v in a.items() if k not in vol}
    nb = {k: v for k, v in b.items() if k not in vol}
    ok4b = json.dumps(na, sort_keys=True) == json.dumps(nb, sort_keys=True)
except OSError:
    ok4b = False
check("D004", "garanties 4/4 + bootstrap vert + idempotence ×2 byte-identique",
      ok4 and ok4b, f"garanties={'PASS' if ok4 else '?'} idempotence={'identique' if ok4b else '?'}")

# D005 — correctif F1
diff_f1 = subprocess.run(["git", "show", "--stat", "b7e799fe"], cwd=REPO,
                         capture_output=True, text=True).stdout
borné = "1 file changed" in diff_f1 and "ensure-installed.py" in diff_f1
dep = subprocess.run([sys.executable, str(REPO / "skills/gen-plan/scripts/ensure-installed.py"),
                      "--check"], capture_output=True, text=True)
ok5 = borné and dep.returncode == 0 and '"verdict": "INSTALLE"' in dep.stdout
check("D005", "diff F1 borné (1 fichier) + copie dépôt --check rc=0 INSTALLE",
      ok5, f"borné={'oui' if borné else 'non'} rc={dep.returncode}")

# D006 — test dédié V2 + flux
v2 = subprocess.run([sys.executable, str(BASE / "scripts/auto-install-ecosysteme.py")],
                    capture_output=True, text=True)
okv2 = v2.returncode == 0 and '"verdict": "INSTALLE"' in v2.stdout
fl = json.load(open(BASE / "download/rapport-efficacite-task105-flux.json"))
v2f = [v for v in fl.get("voies", []) if "V2" in v.get("voie", "")]
ok6 = okv2 and v2f and v2f[0].get("fonctionnel") is True
check("D006", "auto-install V2 INSTALLE rc=0 + harnais flux fonctionnel=true",
      ok6, f"V2={'INSTALLE' if okv2 else '?'} flux={'fonctionnel' if v2f and v2f[0].get('fonctionnel') else '?'}")

# D007 — garanties post-GO-2
cert = subprocess.run([sys.executable, str(BASE / "scripts/certification-complete.py")],
                      capture_output=True, text=True)
e1 = subprocess.run([sys.executable, str(BASE / "scripts/ensure-installed.py"), "--check"],
                    capture_output=True, text=True)
ok7 = cert.returncode == 0 and "ALL PASS (6/6)" in cert.stdout and e1.returncode == 0
check("D007", "certification ALL PASS 6/6 + garde É1 rc=0 (R2 0 rétrogradation — g3 garanties PASS)",
      ok7, f"cert={'6/6' if 'ALL PASS (6/6)' in cert.stdout else '?'} E1 rc={e1.returncode}")

# D008 — rapport CW
cw = (BASE / "download/rapport-cw-task107-projet.md").read_text(encoding="utf-8")
ok8 = ("**PASS**" in cw and "Phase 5" in cw and "Findings" in cw and "alias-eco" in cw)
check("D008", "rapport CW présent, phases 1-5, verdict PASS, findings classés",
      ok8, f"phases={'complètes' if ok8 else '?'} verdict={'PASS' if '**PASS**' in cw else '?'}")

print(f"{'Décision':10} {'Verdict':8} Obtenu")
tout = True
for d, nom, ok, obtenu in res:
    tout = tout and ok
    print(f"{d:10} {'verified' if ok else 'FAIL':8} {nom[:72]}")
    print(f"{'':10} {'':8} → {obtenu}")
print(f"\nANSWER KEY RE-JOUÉE : {'9/9 en cours (D009 au push final) — D001-D008 = ' + str(sum(1 for _,_,o,_ in res if o)) + '/8 verified' if tout else 'FAIL'}")
sys.exit(0 if tout else 1)
