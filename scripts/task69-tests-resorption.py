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

# -*- coding: utf-8 -*-
"""task69-tests-resorption.py — Harnais de tests $FACON des correctifs de la RÉSORPTION
STRUCTURELLE de la volatilité de « version-management » (Task 69, directive n°8 item 3).

Tests T1-T8 (verdicts mécaniques + timings, journal JSON tmp/task69/journal.json) :
  T1   watchdog selftest (harnais intégré — 8 tests, répertoire temporaire, 0 effet réel)
  T2   disparition TOTALE (skill entier déplacé) → réparation via GARDE externe (composante
       c — chemin réel des incidents, cf. 33e disparition exécution n°1) + identité récursive
       — journalisation non applicable (le watchdog vit DANS le skill surveillé — honnêteté)
  T2b  disparition PARTIELLE (SKILL.md seul, watchdog survivant) → watchdog --once :
       détection + réparation + JOURNALISATION DISPARITION_DETECTEE/REPARATION/RETABLIE
  T3   détection d'écart heartbeat (heartbeat factice ancien → entrée ECART, gap cohérent)
  T4   fix O-68-1 (head verdict ensure-installed == HEAD miroir, host_head séparé)
  T5   journal forensique (INIT 1re ligne, backfill 32 incidents, INIT présent exactement 1×)
  T6   arbitres post-correctifs (integrity 110/110, coherence PASS, vcw ALL PASS,
       cross 100 %, tool-routing PASS)
  T7   identité hôte↔repo des fichiers modifiés Task 69 (5 fichiers — leçon Task 62 C5)
  T8   idempotence du correctif ×2 (watchdog --once ×2 PRESENT_OK, INIT toujours unique)

Usage : python3 scripts/task69-tests-resorption.py [--selftest]
Python 3 stdlib uniquement. Idempotent (chaque exécution incrémente le compteur du journal).
"""
import filecmp
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SKILL = RACINE / "skills" / "version-management"
WD = RACINE / "skills" / "version-management" / "scripts" / "vm-watchdog.py"
GARDE = RACINE / "skills" / "gen-plan" / "scripts" / "ensure-installed.py"
JNL_WD = RACINE / "tmp" / "vm-watchdog" / "journal-forensique.jsonl"
HB = RACINE / "tmp" / "vm-watchdog" / "heartbeat.json"
JOURNAL = RACINE / "tmp" / "task69" / "journal.json"
MIROIR = RACINE / "KNOWLEDGE-repo"
SIM = RACINE / "tmp" / "task69" / "sim"

FICHIERS_TASK69 = [
    "skills/version-management/SKILL.md",
    "skills/version-management/scripts/vm-watchdog.py",
    "skills/KNOWLEDGE.md",
    "scripts/check-ecosysteme-integrity.py",
    "skills/gen-plan/scripts/ensure-installed.py",
]


def hnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sh(cmd, timeout=180):
    return subprocess.run(cmd, cwd=str(RACINE), capture_output=True, text=True, timeout=timeout)


def dernier_verdict_wd():
    """Verdict du dernier --once du watchdog (JSON sur stdout)."""
    r = sh([sys.executable, str(WD), "--once"])
    for ligne in r.stdout.splitlines():
        s = ligne.strip()
        if s.startswith("{") and s.endswith("}"):
            return json.loads(s)
    return {"verdict": "SORTIE_INATTENDUE", "rc": r.returncode, "stderr": r.stderr[-200:]}


def lignes_journal():
    if not JNL_WD.exists():
        return []
    return [json.loads(l) for l in JNL_WD.read_text(encoding="utf-8").splitlines() if l.strip()]


def fichiers_recursifs(rac):
    """{chemin relatif: taille} de tous les fichiers (identité récursive)."""
    return {str(p.relative_to(rac)): p.stat().st_size for p in rac.rglob("*") if p.is_file()}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def t1_watchdog_selftest():
    r = sh([sys.executable, str(WD), "--selftest"])
    ok = "8/8 PASS, 0 FAIL" in r.stdout
    return ok, "selftest=%s" % ("8/8 PASS" if ok else r.stdout[-120:])


def t2_disparition_totale_garde_externe():
    """Disparition TOTALE (skill entier déplacé) → réparation via GARDE directe (chemin
    réel des incidents — le watchdog vit DANS le skill surveillé : lorsqu'il disparaît
    avec lui, la réplication passe obligatoirement par la garde externe — composante c,
    exactement la 33e disparition : harnais exécution n°1, garde → INSTALLE-REPARÉ).
    La journalisation DISPARITION/REPARATION ne peut PAS être attendue ici (honnêteté)."""
    SIM.mkdir(parents=True, exist_ok=True)
    cible = SIM / "version-management"
    if cible.exists():
        shutil.rmtree(cible)
    shutil.move(str(SKILL), str(cible))          # disparition TOTALE réelle
    try:
        r = sh([sys.executable, str(GARDE)])
        verdict = None
        for ligne in r.stdout.splitlines():
            s = ligne.strip()
            if s.startswith("{") and s.endswith("}"):
                verdict = json.loads(s).get("verdict")
        present = (SKILL / "SKILL.md").exists()
        identite = present and cible.exists() and \
            fichiers_recursifs(SKILL) == fichiers_recursifs(cible)
        ok = present and verdict == "INSTALLE-REPARÉ" and identite
        return ok, "verdict=%s present=%s identite_recursive=%s (%d fichiers) — journalisation " \
                   "non applicable (watchdog déplacé avec le skill — chemin réel = garde externe)" % (
                       verdict, present, identite, len(fichiers_recursifs(SKILL)) if present else 0)
    finally:
        # filet de sécurité : si la garde a échoué, restauration manuelle (jamais de perte)
        if not (SKILL / "SKILL.md").exists() and cible.exists():
            shutil.move(str(cible), str(SKILL))
        if cible.exists():
            shutil.rmtree(cible)                  # purge de la copie de simulation


def t2b_disparition_partielle_watchdog_survivant():
    """Disparition PARTIELLE (SKILL.md seul — watchdog survivant) → watchdog --once :
    détection + réparation via garde + JOURNALISATION end-to-end (composantes a/b)."""
    n_avant = len(lignes_journal())
    (SKILL / "SKILL.md").unlink()                 # disparition partielle réelle
    res = dernier_verdict_wd()
    evs = [l["evenement"] for l in lignes_journal()[n_avant:]]
    present = (SKILL / "SKILL.md").exists()
    ok = (present and res.get("verdict") == "PRESENT_OK"
          and evs.count("DISPARITION_DETECTEE") == 1 and evs.count("REPARATION") == 1
          and "RETABLIE" in evs)
    return ok, "present=%s verdict=%s evenements_nouveaux=%s" % (
        present, res.get("verdict"), ",".join(evs))


def t3_detection_ecart_heartbeat():
    HB.parent.mkdir(parents=True, exist_ok=True)
    HB.write_text(json.dumps({"horodatage": hnow(), "epoch": int(time.time()) - 600, "pid": 1}) + "\n",
                  encoding="utf-8")
    dernier_verdict_wd()  # cycle avec heartbeat ancien → ECART attendu
    evs = [l for l in lignes_journal() if l.get("evenement") == "ECART"]
    ok = bool(evs) and evs[-1].get("ecart_secondes", 0) > 180 \
        and evs[-1].get("fenetre_disparition_potentielle") is True
    return ok, "ecart=%s fenetre=%s" % (
        evs[-1].get("ecart_secondes") if evs else None,
        evs[-1].get("fenetre_disparition_potentielle") if evs else None)


def t4_fix_o681():
    r = sh([sys.executable, str(GARDE)])
    d = None
    for ligne in r.stdout.splitlines():
        s = ligne.strip()
        if s.startswith("{") and s.endswith("}"):
            d = json.loads(s)
    if d is None:
        return False, "verdict JSON absent"
    m = sh(["git", "-C", str(MIROIR), "rev-parse", "--short", "HEAD"]).stdout.strip()
    ok = d.get("head") == m and d.get("host_head") not in (None, m)
    return ok, "head=%s miroir=%s host_head=%s" % (d.get("head"), m, d.get("host_head"))


def t5_journal_forensique():
    ls = lignes_journal()
    n_init = sum(1 for l in ls if l.get("evenement") == "INIT")
    n_backfill = sum(1 for l in ls if l.get("evenement") == "INCIDENT_DOCUMENTE")
    ok = bool(ls) and ls[0].get("evenement") == "INIT" and n_init == 1 and n_backfill == 32 and len(ls) >= 33
    return ok, "INIT=%d backfill=%d total=%d" % (n_init, n_backfill, len(ls))


def t6_arbitres():
    arbitres = {
        "integrity": ([sys.executable, "scripts/check-ecosysteme-integrity.py"], "110/110 PASS, 0 FAIL"),
        "coherence": ([sys.executable, "scripts/test-coherence-interactions.py"], "PASS STRICT"),
        "vcw": ([sys.executable, "scripts/verify-correct-work.py"], "ALL PASS"),
        "cross": ([sys.executable, "scripts/verify-cross.py"], "100.0%"),
        "tool-routing": ([sys.executable, "scripts/check-tool-routing.py"], "VERDICT : PASS"),
    }
    details, ok = {}, True
    for nom, (cmd, attendu) in arbitres.items():
        r = sh(cmd, timeout=240)
        bon = attendu in r.stdout
        details[nom] = "PASS" if bon else "FAIL(attendu %s)" % attendu
        ok = ok and bon
    return ok, " ".join("%s=%s" % kv for kv in details.items())


def t7_identite_hote_repo():
    diffs = []
    for f in FICHIERS_TASK69:
        a, b = RACINE / f, MIROIR / f
        if not (a.exists() and b.exists()) or not filecmp.cmp(a, b, shallow=False):
            diffs.append(f)
    ok = not diffs
    return ok, "5 fichiers %s" % ("IDENTIQUES" if ok else "DIFFERE: %s" % diffs)


def t8_idempotence_correctif():
    v1 = dernier_verdict_wd()
    v2 = dernier_verdict_wd()
    ls = lignes_journal()
    n_init = sum(1 for l in ls if l.get("evenement") == "INIT")
    ok = v1.get("verdict") == "PRESENT_OK" and v2.get("verdict") == "PRESENT_OK" and n_init == 1
    return ok, "once1=%s once2=%s INIT=%d" % (v1.get("verdict"), v2.get("verdict"), n_init)


TESTS = [("T1", "watchdog selftest", t1_watchdog_selftest),
         ("T2", "disparition TOTALE → garde externe + identité récursive", t2_disparition_totale_garde_externe),
         ("T2b", "disparition PARTIELLE (watchdog survivant) → détection+réparation+journal", t2b_disparition_partielle_watchdog_survivant),
         ("T3", "détection écart heartbeat", t3_detection_ecart_heartbeat),
         ("T4", "fix O-68-1 (head miroir, host_head séparé)", t4_fix_o681),
         ("T5", "journal forensique (INIT, backfill 32)", t5_journal_forensique),
         ("T6", "arbitres post-correctifs 5/5", t6_arbitres),
         ("T7", "identité hôte↔repo 5 fichiers", t7_identite_hote_repo),
         ("T8", "idempotence correctif ×2", t8_idempotence_correctif)]


def executer():
    resultats, t_total = [], 0.0
    for tid, libelle, fn in TESTS:
        t0 = time.time()
        try:
            ok, detail = fn()
            verdict = "PASS" if ok else "FAIL"
        except Exception as exc:  # un test qui plante est un FAIL consigné, jamais masqué
            ok, verdict, detail = False, "FAIL", "EXCEPTION: %r" % exc
        dt = round(time.time() - t0, 2)
        t_total += dt
        resultats.append({"id": tid, "libelle": libelle, "verdict": verdict,
                          "detail": str(detail)[:220], "s": dt})
        print("  [%s] %s (%ss) %s" % (verdict, tid, dt, str(detail)[:130]))
    n_pass = sum(1 for r in resultats if r["verdict"] == "PASS")
    etat = json.loads(JOURNAL.read_text(encoding="utf-8")) if JOURNAL.exists() else {"executions": 0, "passes": []}
    etat["executions"] = etat.get("executions", 0) + 1
    etat["passes"].append({"horodatage": hnow(), "n_pass": n_pass, "n_total": len(resultats),
                           "duree_s": round(t_total, 2), "tests": resultats})
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(etat, ensure_ascii=False, indent=1), encoding="utf-8")
    print("=== RESUME : %d/%d PASS — exécution n°%d (%ss) ===" % (
        n_pass, len(resultats), etat["executions"], round(t_total, 2)))
    return 0 if n_pass == len(resultats) else 1


def selftest():
    """Harnais auto-vérifiant : invariants sans exécuter les tests réels."""
    checks = [("T1-T2b-T8 definis", len(TESTS) == 9),
              ("ids uniques", len({t[0] for t in TESTS}) == 9),
              ("journal cible tmp/task69/", str(JOURNAL).endswith("tmp/task69/journal.json")),
              ("5 fichiers identité declares", len(FICHIERS_TASK69) == 5),
              ("watchdog present", WD.exists()),
              ("garde presente", GARDE.exists())]
    ko = 0
    print("=== task69-tests-resorption selftest : %d checks ===" % len(checks))
    for nom, ok in checks:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", nom))
        ko += 0 if ok else 1
    print("=== RESUME : %d/%d PASS, %d FAIL ===" % (len(checks) - ko, len(checks), ko))
    return 0 if ko == 0 else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else executer())
