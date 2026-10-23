#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Harnais de tests Task 20 — « test si l'installation de $ECO-LEON est performante ».

Expansion alias (registre @historique/@Alias/) : $ECO-LEON = « mon écosystème personnel ».
Plan : download/plan-task20-test-installation-performante.md (answer key D001-D012, seuils §5).

Tests :
  T1 Complétude      — inventaire dérivé du registre KB (KO-L003) : projection hôte + égalité versions
  T2 Intégrité hôte  — check-ecosysteme-integrity.py --check (projection hôte, lecture seule)
  T3 Certification   — certification-complete.py (dépôt, 5 arbitres, rc 0)
  T4 gen-plan        — SKILL.md hôte v3.23.2 (frontmatter, déclencheurs, E1-E15) + garde É1-INSTALL
  T5 correct-work    — arbitre verify-correct-work.py (forme installée hôte) 16/16
  T6 alias-eco       — selftest 15/15 + --list + registre vivant (trié, dédupliqué, ECO-LEON)
  T7 Processus run 1 — snapshot A → eco_install_pipeline.py (chrono, preflight, garde R2, purges)
                        → snapshot B → diff → certification post-install (étape 9, manifeste hôte)
  T8 Idempotence     — run 2 → snapshot C → diff → re-certification post-install → point fixe
  T9 Mesures         — durées, empreinte disque, temps arbitres

Non-destructif : snapshots SHA-256 avant/après ; __pycache__ exclu (artefacts de compilation).
Écrit scripts/task20-tests-report.json (après les runs — jamais synchronisé pendant la session).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # KNOWLEDGE-repo
HOST = "/home/z/my-project"
PY = sys.executable

RAPPORT = os.path.join(BASE, "scripts", "task20-tests-report.json")
MANIFEST_ETAT = "scripts/ecosysteme-integrity.json"     # fichier d'état par arbre (étape 8 → étape 9)
JUSTIFIES = {                                           # nouveaux fichiers hôte attendus au run 1 (union-merge)
    "scripts/task20-answer-key-check.py",
    "scripts/task20-tests-installation.py",
}


def sh(cmd, cwd=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def run_py(args, cwd=None, timeout=300):
    return subprocess.run([PY] + args, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def semver_of(path):
    try:
        head = open(path, encoding="utf-8", errors="replace").read(3000)
    except OSError:
        return None
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", head, re.M)
    return m.group(1) if m else None


def kb_eco_skills():
    kb = open(os.path.join(BASE, "skills", "KNOWLEDGE.md"), encoding="utf-8").read()
    noms = re.findall(r"^## ([\w-]+) v[\d.]+$", kb, re.MULTILINE)
    return [n for n in noms if os.path.isfile(os.path.join(BASE, "skills", n, "SKILL.md"))]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(eco):
    """Inventaire {chemin_relatif: sha256} de l'arbre projeté géré (hors __pycache__)."""
    racines = [
        os.path.join(HOST, "skills", "@mon-ecosysteme"),
        os.path.join(HOST, "skills", "KNOWLEDGE.md"),
        os.path.join(HOST, "skills", "@historique"),
        os.path.join(HOST, "scripts"),
        os.path.join(HOST, "download", "mon-ecosysteme_archive.zip"),
    ] + [os.path.join(HOST, "skills", s) for s in eco]
    snap = {}
    for racine in racines:
        if os.path.isfile(racine):
            snap[os.path.relpath(racine, HOST)] = sha256_file(racine)
            continue
        for dirpath, dirnames, filenames in os.walk(racine):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                snap[os.path.relpath(p, HOST)] = sha256_file(p)
    return snap


def diff(snap_avant, snap_apres):
    mod = sorted(k for k in snap_avant if k in snap_apres and snap_avant[k] != snap_apres[k])
    sup = sorted(k for k in snap_avant if k not in snap_apres)
    new = sorted(k for k in snap_apres if k not in snap_avant)
    return {"modifies": mod, "supprimes": sup, "nouveaux": new}


def dir_size(path):
    total = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            total += os.path.getsize(os.path.join(dirpath, fn))
    return total


res = {"t1": {}, "t2": {}, "t3": {}, "t4": {}, "t5": {}, "t6": {}, "t7": {}, "t8": {}, "t9": {},
       "decisions": {}, "verdict": None, "mesures": {}}

# ============================== T1 — Complétude ==============================
eco = kb_eco_skills()
manquants, divergents, detail_versions = [], [], {}
for s in eco:
    repo_md = os.path.join(BASE, "skills", s, "SKILL.md")
    host_md = os.path.join(HOST, "skills", s, "SKILL.md")
    v_repo, v_host = semver_of(repo_md), semver_of(host_md)
    if not os.path.isfile(host_md):
        manquants.append(s)
    elif v_repo != v_host:
        divergents.append(f"{s}: host {v_host} != repo {v_repo}")
    detail_versions[s] = {"repo": v_repo, "host": v_host}
res["t1"] = {"n_skills_registre": len(eco), "manquants": manquants, "divergents": divergents}
d002 = not manquants and not divergents
print(f"[T1] Complétude : {len(eco)} skills écosystème au registre KB — "
      f"manquants {len(manquants)}, divergents {len(divergents)} → {'PASS' if d002 else 'FAIL'}")

# ========================= T2 — Intégrité hôte (--check) =====================
t0 = time.perf_counter()
r = run_py([os.path.join(HOST, "scripts", "check-ecosysteme-integrity.py"), "--check"], cwd=HOST)
dur_t2 = time.perf_counter() - t0
fails_t2 = len(re.findall(r"\[FAIL\]", r.stdout))
res["t2"] = {"rc": r.returncode, "fails": fails_t2, "duree_s": round(dur_t2, 2),
             "resume": (r.stdout.strip().splitlines()[-2:] if r.stdout else []) + (["STDERR:" + r.stderr[-200:]] if r.stderr else [])}
d003 = r.returncode == 0 and fails_t2 == 0
print(f"[T2] Intégrité hôte : rc {r.returncode}, {fails_t2} FAIL, {dur_t2:.2f}s → {'PASS' if d003 else 'FAIL'}")

# ========================= T4 — gen-plan fonctionnel =========================
gp = os.path.join(HOST, "skills", "gen-plan", "SKILL.md")
gpc = open(gp, encoding="utf-8", errors="replace").read() if os.path.isfile(gp) else ""
fm = gpc.split("---", 2)[1] if gpc.startswith("---") else ""
champs = {c: (c + ":" in fm) for c in ["name", "version", "category", "language", "description", "dependencies"]}
v_gp = semver_of(gp)
declencheurs = {t: (t in gpc) for t in ["gen-plan(step)", "plan d'actions", "E15", "É1-INSTALL", "correct-work"]}
t0 = time.perf_counter()
r_guard = run_py([os.path.join(HOST, "skills", "gen-plan", "scripts", "ensure-installed.py"), "--check"], cwd=HOST)
dur_guard = time.perf_counter() - t0
guard_ok = r_guard.returncode == 0
try:
    guard_json = json.loads(r_guard.stdout)
except Exception:
    guard_json = {"raw": (r_guard.stdout or r_guard.stderr)[:300]}
d005 = (all(champs.values()) and v_gp == "3.23.2" and all(declencheurs.values()) and guard_ok)
res["t4"] = {"frontmatter": champs, "version": v_gp, "lignes": gpc.count("\n") + 1,
             "declencheurs": declencheurs, "garde_E1_INSTALL": {"rc": r_guard.returncode, "verdict": guard_json.get("verdict"),
             "fichiers_manquants": guard_json.get("fichiers_manquants"), "duree_s": round(dur_guard, 2)}}
print(f"[T4] gen-plan hôte : v{v_gp}, frontmatter {sum(champs.values())}/6, déclencheurs "
      f"{sum(declencheurs.values())}/5, garde É1-INSTALL rc {r_guard.returncode} ({guard_json.get('verdict')}) → {'PASS' if d005 else 'FAIL'}")

# ========================= T5 — correct-work fonctionnel =====================
t0 = time.perf_counter()
r = run_py([os.path.join(HOST, "skills", "correct-work", "scripts", "verify-correct-work.py")], cwd=HOST)
dur_t5 = time.perf_counter() - t0
m16 = re.search(r"PASS\s*:\s*(\d+)/(\d+)", r.stdout)
d006 = r.returncode == 0 and m16 and m16.group(1) == m16.group(2) and "ALL PASS" in r.stdout
res["t5"] = {"rc": r.returncode, "score": m16.group(0) if m16 else None, "duree_s": round(dur_t5, 2),
             "all_pass": "ALL PASS" in r.stdout}
print(f"[T5] Arbitre correct-work hôte : rc {r.returncode}, {m16.group(0) if m16 else '?'}, {dur_t5:.2f}s → {'PASS' if d006 else 'FAIL'}")

# ========================= T6 — alias-eco fonctionnel ========================
t0 = time.perf_counter()
r_st = run_py([os.path.join(HOST, "skills", "alias-eco", "scripts", "alias-manager.py"), "--selftest"], cwd=HOST)
r_ls = run_py([os.path.join(HOST, "skills", "alias-eco", "scripts", "alias-manager.py"), "--list"], cwd=HOST)
dur_t6 = time.perf_counter() - t0
m15 = re.search(r"(\d+)/(\d+)", r_st.stdout)
reg = json.load(open(os.path.join(HOST, "skills", "@historique", "@Alias", "aliases.json"), encoding="utf-8"))
phrases = [p.get("phrase") for p in reg.get("phrases", [])]
eco_leon = any(p.get("alias") == "ECO-LEON" and p.get("phrase") == "mon écosystème personnel"
               for p in reg.get("phrases", []))
trie = phrases == sorted(phrases)
dedup = len(phrases) == len(set(phrases))
d007 = (r_st.returncode == 0 and m15 and m15.group(1) == m15.group(2) == "15"
        and r_ls.returncode == 0 and eco_leon and trie and dedup)
res["t6"] = {"selftest_rc": r_st.returncode, "selftest": m15.group(0) if m15 else None,
             "list_rc": r_ls.returncode, "registre": {"n_phrases": len(phrases), "eco_leon": eco_leon,
             "trie": trie, "deduplique": dedup}, "duree_s": round(dur_t6, 2)}
print(f"[T6] alias-eco : selftest {m15.group(0) if m15 else '?'} rc {r_st.returncode}, --list rc {r_ls.returncode}, "
      f"registre {len(phrases)} phrases (ECO-LEON {'OK' if eco_leon else 'ABSENT'}, trié {trie}, dédupliqué {dedup}) → {'PASS' if d007 else 'FAIL'}")

# ===================== T3 — Certification du dépôt (5 arbitres) ==============
t0 = time.perf_counter()
r = run_py([os.path.join(BASE, "scripts", "certification-complete.py")], cwd=BASE, timeout=600)
dur_t3 = time.perf_counter() - t0
verd = [l for l in r.stdout.splitlines() if "VERDICT" in l.upper() or "ALL PASS" in l]
d004 = r.returncode == 0
res["t3"] = {"rc": r.returncode, "duree_s": round(dur_t3, 2), "verdicts": verd[-3:],
             "stderr": r.stderr[-300:] if r.stderr else ""}
print(f"[T3] Certification dépôt : rc {r.returncode}, {dur_t3:.2f}s, {verd[-1] if verd else '(voir rapport)'} → {'PASS' if d004 else 'FAIL'}")

# =============== T7 — Processus d'installation : run 1 instrumenté ===========
snapA = snapshot(eco)
t0 = time.perf_counter()
r_inst = run_py([os.path.join(BASE, "scripts", "eco_install_pipeline.py")], cwd=BASE, timeout=600)
dur_run1 = time.perf_counter() - t0
inst1 = {}
try:
    inst1 = json.loads(r_inst.stdout)
except Exception:
    inst1 = {"erreur_parse": (r_inst.stdout or r_inst.stderr)[-400:]}
preflight_ok = isinstance(inst1.get("etapes", {}).get("preflight"), str) and "OK" in inst1["etapes"]["preflight"]
garde_ok = inst1.get("garde_R2") == "0 rétrogradation — host ≤ repo partout"
purges_ok = inst1.get("purges") == []
snapB = snapshot(eco)
diff1 = diff(snapA, snapB)
mod_attendus1 = [k for k in diff1["modifies"] if k != MANIFEST_ETAT]
ok_diff1 = (not diff1["supprimes"] and not mod_attendus1
            and set(diff1["nouveaux"]) <= JUSTIFIES)
# Étape 9 du pipeline canonique : certification post-install (écrit le manifeste de SON arbre)
t0 = time.perf_counter()
r_cert1 = run_py([os.path.join(HOST, "scripts", "check-ecosysteme-integrity.py")], cwd=HOST, timeout=300)
dur_cert1 = time.perf_counter() - t0
cert1_ok = r_cert1.returncode == 0 and not re.findall(r"\[FAIL\]", r_cert1.stdout)
snapB2 = snapshot(eco)
manifest_apres_cert1 = snapB2.get(MANIFEST_ETAT)
manifest_pre_run_stale = snapA.get(MANIFEST_ETAT) != manifest_apres_cert1
d008 = (r_inst.returncode == 0 and preflight_ok and garde_ok and purges_ok and dur_run1 < 60)
res["t7"] = {"run1": {"rc": r_inst.returncode, "duree_s": round(dur_run1, 2), "preflight_ok": preflight_ok,
           "garde_R2": inst1.get("garde_R2"), "purges": inst1.get("purges"),
           "etapes": {k: v for k, v in list(inst1.get("etapes", {}).items())[:8]}},
           "diff_A_vers_B": diff1, "modifies_hors_manifeste": mod_attendus1,
           "diff1_conforme": ok_diff1,
           "cert_post_install": {"rc": r_cert1.returncode, "all_pass": cert1_ok, "duree_s": round(dur_cert1, 2)},
           "manifeste_pre_run_stale": manifest_pre_run_stale}
print(f"[T7] Run 1 : rc {r_inst.returncode}, {dur_run1:.2f}s, preflight {'OK' if preflight_ok else 'FAIL'}, "
      f"garde R2 {'OK' if garde_ok else 'FAIL'}, purges {inst1.get('purges')}")
print(f"     diff A→B : modifiés {len(diff1['modifies'])} (hors manifeste: {len(mod_attendus1)}), "
      f"supprimés {len(diff1['supprimes'])}, nouveaux {len(diff1['nouveaux'])} → {'CONFORME' if ok_diff1 else 'ÉCART'}")
print(f"     certification post-install : rc {r_cert1.returncode} ({dur_cert1:.2f}s), "
      f"manifeste pré-run périmé : {'OUI (mis à jour par étape 9 — légitime)' if manifest_pre_run_stale else 'non'}")

# =============== T8 — Idempotence : run 2 + point fixe =======================
t0 = time.perf_counter()
r_inst2 = run_py([os.path.join(BASE, "scripts", "eco_install_pipeline.py")], cwd=BASE, timeout=600)
dur_run2 = time.perf_counter() - t0
snapC = snapshot(eco)
diff2 = diff(snapB2, snapC)
mod_attendus2 = [k for k in diff2["modifies"] if k != MANIFEST_ETAT]
ok_diff2 = (not diff2["supprimes"] and not mod_attendus2 and not diff2["nouveaux"])
t0 = time.perf_counter()
r_cert2 = run_py([os.path.join(HOST, "scripts", "check-ecosysteme-integrity.py")], cwd=HOST, timeout=300)
dur_cert2 = time.perf_counter() - t0
cert2_ok = r_cert2.returncode == 0 and not re.findall(r"\[FAIL\]", r_cert2.stdout)
snapC2 = snapshot(eco)
manifest_apres_cert2 = snapC2.get(MANIFEST_ETAT)
manifest_converge = manifest_apres_cert1 == manifest_apres_cert2
archive_stable = snapB2.get("download/mon-ecosysteme_archive.zip") == snapC2.get("download/mon-ecosysteme_archive.zip")
d009 = ok_diff1 and ok_diff2 and manifest_converge and archive_stable and cert1_ok and cert2_ok
res["t8"] = {"run2": {"rc": r_inst2.returncode, "duree_s": round(dur_run2, 2)},
             "diff_B2_vers_C": diff2, "modifies_hors_manifeste": mod_attendus2,
             "diff2_conforme": ok_diff2,
             "cert_post_install_2": {"rc": r_cert2.returncode, "all_pass": cert2_ok, "duree_s": round(dur_cert2, 2)},
             "manifeste_convergence_inter_cycles": manifest_converge,
             "archive_byte_stable_run2": archive_stable}
print(f"[T8] Run 2 : rc {r_inst2.returncode}, {dur_run2:.2f}s — diff B2→C : modifiés {len(diff2['modifies'])} "
      f"(hors manifeste: {len(mod_attendus2)}), supprimés {len(diff2['supprimes'])}, nouveaux {len(diff2['nouveaux'])} → "
      f"{'CONFORME' if ok_diff2 else 'ÉCART'} ; manifeste convergent inter-cycles : {'OUI' if manifest_converge else 'NON'} ; "
      f"archive byte-stable : {'OUI' if archive_stable else 'NON'}")

# ========================= T9 — Mesures consolidées ==========================
taille = {
    "corpus_depot": dir_size(os.path.join(BASE, "skills", "@mon-ecosysteme")),
    "corpus_hote": dir_size(os.path.join(HOST, "skills", "@mon-ecosysteme")),
    "skills_eco_hote": sum(dir_size(os.path.join(HOST, "skills", s)) for s in eco),
    "scripts_hote": dir_size(os.path.join(HOST, "scripts")),
    "archive_hote": dir_size(os.path.join(HOST, "download", "mon-ecosysteme_archive.zip")),
}
res["t9"] = {"tailles_octets": taille,
             "tailles_mo": {k: round(v / 1048576, 2) for k, v in taille.items()},
             "durees_s": {"run1": round(dur_run1, 2), "run2": round(dur_run2, 2),
                          "certification_depot": round(dur_t3, 2),
                          "integrite_hote": round(dur_t2, 2),
                          "cert_post_install_1": round(dur_cert1, 2),
                          "cert_post_install_2": round(dur_cert2, 2),
                          "arbitre_correct_work": round(dur_t5, 2),
                          "garde_E1_INSTALL": round(dur_guard, 2)}}

# ============================== Verdict (§5) =================================
res["decisions"] = {
    "D002": {"ok": d002, "detail": f"{len(eco)} skills, {len(manquants)} manquant(s), {len(divergents)} divergence(s)"},
    "D003": {"ok": d003, "detail": f"rc {r.returncode if False else res['t2']['rc']}, {res['t2']['fails']} FAIL"},
    "D004": {"ok": d004, "detail": f"rc {res['t3']['rc']}"},
    "D005": {"ok": d005, "detail": f"gen-plan v{v_gp} + garde {guard_json.get('verdict')}"},
    "D006": {"ok": d006, "detail": res["t5"].get("score")},
    "D007": {"ok": d007, "detail": f"selftest {res['t6'].get('selftest')}, ECO-LEON {eco_leon}"},
    "D008": {"ok": d008, "detail": f"run1 {dur_run1:.1f}s, preflight {preflight_ok}, garde {garde_ok}, purges {purges_ok}"},
    "D009": {"ok": d009, "detail": f"diff1 {ok_diff1}, diff2 {ok_diff2}, manifeste convergent {manifest_converge}, archive stable {archive_stable}"},
}
s1_etat = all(res["decisions"][d]["ok"] for d in ["D002", "D003", "D004", "D005", "D006", "D007"])
if s1_etat and d008 and d009 and dur_run1 < 60:
    verdict = "PERFORMANT"
elif s1_etat:
    verdict = "PARTIELLEMENT PERFORMANT"
else:
    verdict = "NON PERFORMANT"
res["verdict"] = verdict

with open(RAPPORT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)

print(f"\n=== T9 Mesures === durées : run1 {dur_run1:.2f}s · run2 {dur_run2:.2f}s · certification {dur_t3:.2f}s · "
      f"empreinte hôte : skills éco {res['t9']['tailles_mo']['skills_eco_hote']} Mo + corpus "
      f"{res['t9']['tailles_mo']['corpus_hote']} Mo + scripts {res['t9']['tailles_mo']['scripts_hote']} Mo + archive "
      f"{res['t9']['tailles_mo']['archive_hote']} Mo")
print(f"\n=== VERDICT (seuils §5) : {verdict} ===")
print(f"Rapport machine : {RAPPORT}")
sys.exit(0 if verdict != "NON PERFORMANT" else 1)
