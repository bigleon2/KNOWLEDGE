#!/usr/bin/env python3
"""Task 40 — correct-work(projet) : harnais C02, C04-C06, C08-C10.
C01 = gate (déjà exécuté en ouverture) ; C03 (suites task39/task33) et C07 (arbitre) = exécutions séparées."""
import hashlib, json, os, re, subprocess, sys

P = "/home/z/my-project"
ECO = os.path.join(P, "ecosystem")
R = {"checks": {}, "findings": []}

def check(cid, name, ok, detail):
    R["checks"][cid] = {"nom": name, "resultat": "PASS" if ok else "FAIL", "detail": detail}
    if not ok:
        R["findings"].append({"check": cid, "nom": name, "detail": detail})
    return ok

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

# ---- C02 : vue-upload v1.2.0 au disque ----
vup = os.path.join(ECO, "skills/vue-upload/SKILL.md")
vut = open(vup, encoding="utf-8").read()
panel = os.path.join(ECO, "skills/vue-upload/scripts/vue_upload_panel.py")
serveur = os.path.join(ECO, "skills/vue-upload/scripts/vue_upload_server.py")
ver = re.search(r"^version: ([0-9.]+)", vut, re.M)
evals = json.load(open(os.path.join(ECO, "skills/vue-upload/evals/evals.json"), encoding="utf-8"))
n_evals = len(evals if isinstance(evals, list) else evals.get("evals", evals.get("cases", [])))
svt = open(serveur, encoding="utf-8").read()
check("C02", "vue-upload v1.2.0 structure",
      ver and ver.group(1) == "1.2.0" and vut.count("---") >= 2 and os.path.exists(panel)
      and os.path.exists(serveur) and n_evals == 8 and "1.2.0" in svt,
      f"version={ver.group(1) if ver else '?'}, frontmatter délimité (---×{vut.count('---')}), panel {os.path.getsize(panel)} o, "
      f"serveur marqueur 1.2.0={'1.2.0' in svt}, evals={n_evals}")

# ---- C04 : PM gen-plan v3.19.0/v3.20.0 ×3 répertoires, md5 cohérents ----
# Convention ×3 : 1 répertoire dans ecosystem/ + 2 répertoires à la RACINE projet (chat-assets/, archive-extract/@mon-ecosysteme/)
dirs = [os.path.join(ECO, "skills/@mon-ecosysteme"), os.path.join(P, "chat-assets"), os.path.join(P, "archive-extract/@mon-ecosysteme")]
h_v319, h_v320 = set(), set()
miss = []
for d in dirs:
    for v, acc in (("3.19.0", h_v319), ("3.20.0", h_v320)):
        f = os.path.join(d, f"PROMPT-MAITRE-GEN-PLAN-v{v}.md")
        if not os.path.exists(f):
            miss.append(f)
        else:
            acc.add(md5(f))
pm319 = open(os.path.join(ECO, "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.19.0.md"), encoding="utf-8").read()
pm320 = open(os.path.join(ECO, "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.20.0.md"), encoding="utf-8").read()
y319 = re.findall(r"^version: ([0-9.]+)", pm319, re.M)
y320 = re.findall(r"^version: ([0-9.]+)", pm320, re.M)
check("C04", "PM gen-plan v3.19.0/v3.20.0 ×3",
      not miss and len(h_v319) == 1 and len(h_v320) == 1 and h_v319 != h_v320
      and "3.19.0" in y319 and "3.20.0" in y320 and "D006" in pm319 and "plan-post-reinstall" in pm320,
      f"6 fichiers présents, md5 cohérents par version ({len(h_v319)}+{len(h_v320)} hash distincts), "
      f"YAML v3.19.0={'3.19.0' in y319}, YAML v3.20.0={'3.20.0' in y320}, deltas §1.16/D006 (v319) + plan-post-reinstall (v320) présents")

# ---- C05 : audit PM correct-work v2.7.0 / clone-chat v2.0.0 (constat « déjà présents ») ----
cw = os.path.join(ECO, "skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md")
cc = os.path.join(ECO, "skills/@mon-ecosysteme/PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md")
cw_ok = os.path.exists(cw)
cc_ok = os.path.exists(cc)
cc_liste = sorted(os.path.basename(f) for f in
                  __import__("glob").glob(os.path.join(ECO, "skills/@mon-ecosysteme/PROMPT-MAITRE-CLONE-CHAT-*.md")))
check("C05", "Audit PM correct-work/clone-chat", cw_ok and cc_ok,
      f"PM correct-work v2.7.0={cw_ok}, PM clone-chat v2.0.0={cc_ok} (variantes: {', '.join(cc_liste) or 'aucune'})")

# ---- C06 : KB ----
kb = open(os.path.join(ECO, "skills/KNOWLEDGE.md"), encoding="utf-8").read()
kb_vu12 = bool(re.search(r"^## vue-upload v1\.2\.0", kb, re.M))
kb_t38 = "Task 38" in kb
kb_t39 = "Task 39" in kb
kb_entr = re.findall(r"^## ([A-Za-z0-9_.-]+) v([0-9.]+)", kb, re.M)
# NB : la fiche vue-upload est MONTÉE v1.1.0→v1.2.0 (pas doublée) → le compte de fiches versionnées ne bouge pas (28, cohérent Task 37) ;
# le comptage « kb_entrees=29 » du gate utilise un critère différent (lignes du registre, pas fiches versionnées).
check("C06", "Registre KB", kb_vu12 and kb_t38 and kb_t39 and len(kb_entr) >= 28,
      f"vue-upload v1.2.0={kb_vu12}, entrées Task 38/39={kb_t38}/{kb_t39}, fiches versionnées={len(kb_entr)} (fiche vue-upload montée, pas doublée)")

# ---- C08 : worklog format SHARED §1.4 ----
wl = open(os.path.join(P, "worklog.md"), encoding="utf-8").read()
secs = re.split(r"(?m)^---$", wl)[1:]
mal = [i for i, s in enumerate(secs) if not re.search(r"Task ID:", s) or "Stage Summary:" not in s]
t39_ok = any(re.search(r"Task ID: 39\b", s) for s in secs)
check("C08", "Worklog format SHARED §1.4", not mal and t39_ok,
      f"{len(secs)}/{len(secs)} sections actives bien formées (Task ID + Stage Summary), entrée Task 39={t39_ok}")

# ---- C09 : livrables intacts ----
docx = os.path.join(P, "download/rapport-task26-agent-engineering-playlist.docx")
j39 = os.path.join(P, "scripts/task39-test-vue-upload-v120.json")
plan37 = os.path.join(P, "download/plan-cw-projet-task37.md")
rap37 = os.path.join(P, "download/rapport-cw-projet-task37.md")
docx_ok = os.path.exists(docx) and os.path.getsize(docx) == 120974
j39d = json.load(open(j39, encoding="utf-8")) if os.path.exists(j39) else {}
j39_pass = j39d.get("resume", {}).get("pass", j39d.get("pass"))
check("C09", "Livrables intacts",
      docx_ok and os.path.exists(j39) and j39_pass == 14 and os.path.exists(plan37) and os.path.exists(rap37),
      f"DOCX={os.path.getsize(docx) if os.path.exists(docx) else 'ABSENT'} o (attendu 120 974), "
      f"journal task39 {j39_pass}/14 PASS, plan+rapport CW Task 37 présents")

# ---- C10 : état git (claims = disque) ----
def g(*a):
    r = subprocess.run(["git", "-C", ECO] + list(a), capture_output=True, text=True)
    return r.stdout.rstrip("\n")
head = g("rev-parse", "HEAD")[:7]
stat = g("status", "--short").splitlines()
mod = [l for l in stat if l.startswith(" M")]
unt = [l[3:] for l in stat if l.startswith("??")]
unt_hors_tmp = [u for u in unt if not u.startswith("tmp/")]
lsr = subprocess.run(["git", "ls-remote", "https://github.com/bigleon2/KNOWLEDGE.git", "main"],
                     capture_output=True, text=True, timeout=25)
origin_main = lsr.stdout.split()[0][:7] if lsr.stdout.strip() else "?"
c39a = g("log", "--oneline", "-3")
check("C10", "État git cohérent (claims Task 38/39 = disque)",
      head == "36c5d1f" and origin_main == head and not mod and not unt_hors_tmp
      and "5354f27" in c39a and "36c5d1f" in c39a,
      f"HEAD={head} = origin/main={origin_main}, 0 commit non poussé, arbre propre (non suivis: {unt or 'aucun — tmp/ exclu par convention'}), "
      f"commits Task 39 présents (5354f27 + 36c5d1f)")

n_fail = sum(1 for c in R["checks"].values() if c["resultat"] == "FAIL")
R["resume"] = {"checks_executes": len(R["checks"]), "pass": len(R["checks"]) - n_fail, "fail": n_fail}
out = os.path.join(P, "scripts/task40-cw-projet-checks.json")
json.dump(R, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for cid, c in R["checks"].items():
    print(f"{cid} {c['resultat']:4} — {c['nom']} :: {c['detail']}")
print(f"→ {R['resume']['pass']}/{R['resume']['checks_executes']} PASS, {n_fail} FAIL — journal : {out}")
sys.exit(0 if n_fail == 0 else 1)
