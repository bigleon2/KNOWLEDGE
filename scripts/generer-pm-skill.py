#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer-pm-skill.py — Génération mécanique du prompt maître à toute montée de version.

Règle KO-L004 v1.1.0 (gen-plan §1.15, leçon L004 matérialisée — directive
utilisateur 2026-10-09) : toute montée de version d'un skill des 3 familles
(gen-plan, correct-work, clone-chat) déclenche, AVANT la certification :
  (1) le recalibrage mécanique des outils dépendants (arbitres, pre-checks,
      skills-meta.json, run-order, SYNC_MAP, miroir, archive) ;
  (2) la génération mécanique du prompt maître de la nouvelle version —
      PROMPT-MAITRE-<famille>-v<version>.md dans skills/@mon-ecosysteme/
      — par le présent script.

Mécanique (méthode B1 généralisée — substitutions verrouillées) :
  - source de vérité : frontmatter `version:` de skills/<famille>/SKILL.md ;
  - base : PM le plus récent du corpus (dérivation dynamique — KO-L003) ;
  - chaque substitution verrouille son motif : si le motif n'apparaît pas
    exactement n fois, ABANDON SANS ÉCRITURE (l'état courant est préservé) ;
  - garde anti-rétrogradation R2 : v_cible < v_PM => ABANDON ;
  - recalibrage croisé inclus : SHARED (référence PM + révision + version),
    PM-INSTALL (ligne §2ter + instantané §A.3 + révision + version) ;
  - rapport de couverture SKILL.md <-> PM : le script ne masque jamais un
    écart (KO-L003) — les sections du SKILL.md absentes du PM sont listées ;
  - le delta sémantique de la montée (nouvelles sections) n'est PAS inventé :
    il est fourni via --delta <fichier.json> ou complété par l'agent après
    lecture du rapport (le script n'invente jamais de contenu) ;
  - idempotent x2 : re-exécution sur état cohérent = no-op.

Format --delta (JSON) :
  {
    "history": "texte de la ligne d'historique (changements de la montée)",
    "subs": [{"old": "...", "new": "...", "count": 1}, ...]
  }

Usage :
    python3 scripts/generer-pm-skill.py --check
    python3 scripts/generer-pm-skill.py --generate <famille|all> [--delta FILE] [--dry-run]

Codes retour : 0 = ok / no-op ; 1 = écart détecté (--check) ; 2 = ABANDON
verrouillé (aucune écriture) ; 3 = usage invalide.
"""

import json
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")
CORPUS = os.path.join(SKILLS, "@mon-ecosysteme")
SHARED = os.path.join(CORPUS, "PROMPT-MAITRE-SHARED.md")
PM_INSTALL = os.path.join(CORPUS, "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md")
REPORT = os.path.join(BASE, "scripts", "generer-pm-report.json")

FAMILLES = {
    "gen-plan": "PROMPT-MAITRE-GEN-PLAN",
    "correct-work": "PROMPT-MAITRE-CORRECT-WORK",
    "clone-chat": "PROMPT-MAITRE-CLONE-CHAT",
}


def abandon(msg, code=2):
    print("ABANDON : %s" % msg)
    sys.exit(code)


def bump_minor(v):
    a, b, c = (int(x) for x in v.split("."))
    return "%d.%d.%d" % (a, b + 1, 0)


def semver_tuple(s):
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", s.strip())
    if not m:
        abandon("version non semver 3-parties : %r" % s)
    return tuple(int(x) for x in m.groups())


def read(path):
    if not os.path.isfile(path):
        abandon("fichier introuvable : %s" % path)
    with open(path, encoding="utf-8") as f:
        return f.read()


def skill_version(famille):
    content = read(os.path.join(SKILLS, famille, "SKILL.md"))
    m = re.search(r"^version:\s*[\"']?([\d.]+)", content, re.MULTILINE)
    if not m:
        abandon("frontmatter `version:` absent de skills/%s/SKILL.md" % famille)
    return m.group(1)


def pms_of(famille):
    prefix = FAMILLES[famille]
    pms = []
    for name in os.listdir(CORPUS):
        m = re.fullmatch(re.escape(prefix) + r"-v(\d+\.\d+\.\d+)\.md", name)
        if m:
            pms.append((semver_tuple(m.group(1)), m.group(1), name))
    return sorted(pms)


def sub_locked(text, motif, remplace, n, label):
    """Substitution verrouillée : ABANDON sans écriture si count != n."""
    c = text.count(motif)
    if c != n:
        abandon("motif [%s] trouvé %d fois (attendu %d) : %r"
                % (label, c, n, motif[:70]))
    return text.replace(motif, remplace)


def sections_of(text):
    return sorted(set(re.findall(r"§(\d+(?:\.\d+)*)", text)))


def coverage(skill_text, pm_text):
    sk = sections_of(skill_text)
    pm = sections_of(pm_text)
    return [s for s in sk if s not in pm], sk, pm


def cmd_check():
    report = {"mode": "check", "date": date.today().isoformat(), "familles": {}}
    ecart = False
    for famille in FAMILLES:
        sv = skill_version(famille)
        pms = pms_of(famille)
        pname = pms[-1][2] if pms else None
        st = {"skill": sv, "pm": pname}
        if not pms:
            st["etat"] = "PM-ABSENT"
            ecart = True
        elif semver_tuple(pms[-1][1]) == semver_tuple(sv):
            st["etat"] = "COHERENT"
        elif semver_tuple(pms[-1][1]) < semver_tuple(sv):
            st["etat"] = "PM-ANTERIEUR (KO-L004 v1.1.0 : generer-pm-skill.py --generate %s)" % famille
            ecart = True
        else:
            st["etat"] = "PM-POSTERIEUR (garde R2 : forme installée fait foi — jamais de rétrogradation)"
            ecart = True
        report["familles"][famille] = st
        print("[%s] %-13s SKILL.md v%-7s PM %s" % (st["etat"].split(" ")[0], famille, sv, pname or "ABSENT"))
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("Rapport : %s" % REPORT)
    sys.exit(1 if ecart else 0)


def generate_famille(famille, delta, dry):
    sv = skill_version(famille)
    pms = pms_of(famille)
    if not pms:
        abandon("aucun PM %s au corpus — génération impossible sans base (fournir le PM initial)" % famille)
    _, old, base_name = pms[-1]
    if semver_tuple(sv) == semver_tuple(old):
        print("[NO-OP] %s déjà cohérent (SKILL.md v%s = PM v%s)" % (famille, sv, old))
        return None
    if semver_tuple(sv) < semver_tuple(old):
        abandon("rétrogradation interdite R2 : SKILL.md v%s < PM v%s" % (sv, old))
    base = read(os.path.join(CORPUS, base_name))
    new = sv
    t = base
    t = sub_locked(t, "— Installation du skill %s v%s" % (famille, old),
                   "— Installation du skill %s v%s" % (famille, new), 1, "titre")
    t = sub_locked(t, "> **Skill cible** : %s v%s" % (famille, old),
                   "> **Skill cible** : %s v%s" % (famille, new), 1, "skill cible")
    m = re.search(r"> \*\*Version du prompt\*\* : (\d+\.\d+\.\d+)", t)
    if not m:
        abandon("« Version du prompt » introuvable dans le PM de base")
    t = sub_locked(t, "> **Version du prompt** : %s" % m.group(1),
                   "> **Version du prompt** : %s" % bump_minor(m.group(1)), 1, "version prompt")
    t = sub_locked(t, "> **Date** : %s" % base_date(base),
                   "> **Date** : %s" % date.today().isoformat(), 1, "date")
    n_yaml = t.count("version: %s" % old)
    if n_yaml == 0:
        print("[WARN] aucun exemplaire YAML `version: %s` dans le PM de base (écart consigné — KO-L003)" % old)
    else:
        t = t.replace("version: %s" % old, "version: %s" % new)
    history_txt = (delta or {}).get("history") or (
        "Génération mécanique KO-L004 v1.1.0 (`scripts/generer-pm-skill.py`) : "
        "montée %s v%s -> v%s — deltas sémantiques à complétion agent "
        "(rapport de couverture : scripts/generer-pm-report.json) ; recalibrage "
        "croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3" % (famille, old, new))
    anchor = "\n| v%s | " % old
    c_anchor = t.count(anchor)
    if c_anchor < 1:
        abandon("ligne d'historique v%s introuvable dans le PM de base" % old)
    idx = t.index(anchor)
    t = t[:idx] + "\n| v%s | %s | %s |" % (new, date.today().isoformat(), history_txt) + t[idx:]
    for s in (delta or {}).get("subs", []):
        t = sub_locked(t, s["old"], s["new"], int(s.get("count", 1)),
                       "delta %s" % famille)
    missing, sk_secs, pm_secs = coverage(read(os.path.join(SKILLS, famille, "SKILL.md")), t)
    return {"famille": famille, "old": old, "new": new, "text": t,
            "yaml_subs": n_yaml, "coverage_missing": missing,
            "skill_sections": len(sk_secs), "pm_sections": len(pm_secs)}


def base_date(text):
    m = re.search(r"> \*\*Date\*\* : (\d{4}-\d{2}-\d{2})", text)
    return m.group(1) if m else abandon("date du PM de base introuvable")


def recalibrage(results, dry):
    """SHARED (§6.1 + révision + version) et PM-INSTALL (§2ter + §A.3 + révision + version)."""
    today = date.today().isoformat()
    shared = read(SHARED)
    pm_install = read(PM_INSTALL)
    sh_old = re.search(r"> \*\*Version\*\* : (\d+\.\d+\.\d+)", shared).group(1)
    sh_new = bump_minor(sh_old)
    pi_old = re.search(r"^Version : (\d+\.\d+\.\d+)", pm_install, re.MULTILINE).group(1)
    pi_new = bump_minor(pi_old)
    fams = " · ".join("%s v%s→v%s" % (r["famille"], r["old"], r["new"]) for r in results)
    for r in results:
        f, old, new = r["famille"], r["old"], r["new"]
        ref = "%s-v%s.md" % (FAMILLES[f], old)
        c = shared.count(ref)
        if c == 0:
            print("[WARN] SHARED : référence %r absente (écart consigné — KO-L003)" % ref)
        else:
            shared = shared.replace(ref, "%s-v%s.md" % (FAMILLES[f], new))
        pat = re.compile(r"^\| %s \| `%s-v%s\.md` \| %s v%s \| (\d+) \|\s*$"
                         % (f, FAMILLES[f], re.escape(old), f, re.escape(old)), re.MULTILINE)
        m = pat.findall(pm_install)
        if len(m) != 1:
            abandon("PM-INSTALL §2ter : ligne %s v%s trouvée %d fois (attendu 1)" % (f, old, len(m)))
        pm_install = pat.sub("| %s | `%s-v%s.md` | %s v%s | %s |" % (f, FAMILLES[f], new, f, new, m[0]),
                             pm_install, count=1)
        mi = re.search(r"^Instantané courant \([^)]*\) : (.+)$", pm_install, re.MULTILINE)
        if mi and ("%s v%s" % (f, old)) in mi.group(1):
            ligne_new = mi.group(0).replace("%s v%s" % (f, old), "%s v%s" % (f, new))
            pm_install = sub_locked(pm_install, mi.group(0), ligne_new, 1, "instantané §A.3")
    shared = sub_locked(shared, "> **Version** : %s" % sh_old, "> **Version** : %s" % sh_new, 1, "version SHARED")
    shared = sub_locked(shared, "> **Révision** : ",
                        "> **Révision** : %s (montée %s, KO-L004 v1.1.0) — **v%s** : §6.1 — référence(s) PM portée(s) "
                        "à la/les version(s) générée(s) mécaniquement (`scripts/generer-pm-skill.py` — substitutions "
                        "verrouillées, recalibrage inclus). " % (today, fams, sh_new), 1, "révision SHARED")
    pm_install = sub_locked(pm_install, "Version : %s" % pi_old, "Version : %s" % pi_new, 1, "version PM-INSTALL")
    anchor = "\n| v%s | " % pi_old
    if pm_install.count(anchor) < 1:
        abandon("PM-INSTALL : ligne d'historique v%s introuvable" % pi_old)
    idx = pm_install.index(anchor)
    row = "\n| v%s | %s | KO-L004 v1.1.0 — génération mécanique du PM à toute montée de version (`scripts/generer-pm-skill.py`) : %s ; recalibrage croisé : SHARED v%s (§6.1), §2ter, §A.3 |" % (
        pi_new, today, fams, sh_new)
    pm_install = pm_install[:idx] + row + pm_install[idx:]
    if dry:
        print("[DRY-RUN] aucune écriture — SHARED v%s→v%s, PM-INSTALL v%s→v%s" % (sh_old, sh_new, pi_old, pi_new))
        return
    with open(SHARED, "w", encoding="utf-8") as f:
        f.write(shared)
    with open(PM_INSTALL, "w", encoding="utf-8") as f:
        f.write(pm_install)
    print("Recalibrage écrit : SHARED v%s, PM-INSTALL v%s" % (sh_new, pi_new))
    return sh_new, pi_new


def run_generate(target, delta_path, dry):
    familles = list(FAMILLES) if target == "all" else [target]
    if target != "all" and target not in FAMILLES:
        abandon("famille inconnue : %s (attendu : %s)" % (target, ", ".join(FAMILLES)), 3)
    delta = json.load(open(delta_path, encoding="utf-8")) if delta_path else {}
    results = [r for r in (generate_famille(f, delta, dry) for f in familles) if r]
    if not results:
        with open(REPORT, "w", encoding="utf-8") as f:
            json.dump({"mode": "generate", "date": date.today().isoformat(), "resultat": "no-op"}, f, indent=2, ensure_ascii=False)
        print("Rien à générer — corpus cohérent.")
        return
    if not dry:
        for r in results:
            out = os.path.join(CORPUS, "PROMPT-MAITRE-%s-v%s.md" % (FAMILLES[r["famille"]], r["new"]))
            with open(out, "w", encoding="utf-8") as f:
                f.write(r["text"])
            print("PM écrit : %s (%d lignes)" % (out, r["text"].count("\n")))
    recalibrage(results, dry)
    rep = {"mode": "generate", "date": date.today().isoformat(), "dry_run": dry,
           "familles": [{"famille": r["famille"], "old": r["old"], "new": r["new"],
                         "yaml_subs": r["yaml_subs"], "coverage_missing": r["coverage_missing"],
                         "skill_sections": r["skill_sections"], "pm_sections": r["pm_sections"]} for r in results]}
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    for r in results:
        if r["coverage_missing"]:
            print("[WARN] couverture %s : sections SKILL.md absentes du PM : %s (complétion agent — KO-L003)"
                  % (r["famille"], ", ".join("§" + s for s in r["coverage_missing"])))
        else:
            print("[OK] couverture %s : toutes les sections SKILL.md représentées dans le PM" % r["famille"])
    print("Rapport : %s" % REPORT)


def main():
    args = sys.argv[1:]
    if "--check" in args:
        cmd_check()
    elif "--generate" in args:
        i = args.index("--generate")
        target = args[i + 1] if i + 1 < len(args) else abandon("--generate exige <famille|all>", 3)
        dry = "--dry-run" in args
        delta_path = args[args.index("--delta") + 1] if "--delta" in args else None
        run_generate(target, delta_path, dry)
    else:
        print(__doc__)
        sys.exit(3)


if __name__ == "__main__":
    main()
