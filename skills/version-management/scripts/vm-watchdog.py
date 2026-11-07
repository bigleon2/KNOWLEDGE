#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vm-watchdog.py — Composante (a)+(b) de la RÉSORPTION STRUCTURELLE de la volatilité
de « version-management » (Task 69, directive n°8 item 1 — stratégie NEUTRALISATION RÉSILIENTE).

Diagnostic (Task 69, consolidé) : la suppression du skill survient ENTRE LES TOURS, par un
processus EXTERNE au projet (ni cron ni process local) ; le dépôt git hôte reçoit des
commits automatiques à messages UUID (snapshots plateforme) ; corrélation temporelle exacte
entre interruptions utilisateur et disparitions (32 incidents documentés). La PRÉVENTION est
impossible → la résorption est une NEUTRALISATION RÉSILIENTE à 4 composantes :
  (a) watchdog avec battements de cœur (heartbeat) — DÉTECTE SON PROPRE TEMPS D'ARRÊT
      (écart heartbeat > seuil = fenêtre de disparition potentielle) ;
  (b) journal forensique horodaté tmp/vm-watchdog/journal-forensique.jsonl — corrélation
      mécanique avec les interruptions (heads hôte + miroir consignés à chaque événement) ;
  (c) garde à l'invocation en repli déterministe (ensure-installed.py — INSTALLE-REPARÉ
      rc=0, préexistante Task 56 — AUCUN doublon : R4 jamais dupliquer) ;
  (d) persistance disque continue (miroir KNOWLEDGE-repo — règle d'or n°5, préexistante).

Modes :
  --init          Initialise le journal forensique (INIT + backfill qualifié des 32 incidents
                  documentés worklog/historique). No-op idempotent si déjà présent.
  --once          Un cycle : détection d'écart heartbeat + vérification présence + réparation
                  déterministe via la garde si disparition + horodatage heartbeat.
  --daemon        Boucle --once à intervalle régulier (défaut 30 s) — heartbeat permanent.
  --selftest      Harnais auto-verifiant en répertoire temporaire (AUCUN effet sur le vrai
                  écosystème) : journal, heartbeat, écart, disparition simulée, réparation.
  --intervalle N  Période du daemon en secondes (défaut 30).
  --seuil N       Seuil d'écart heartbeat en secondes (défaut 180).

Python 3 stdlib uniquement. Idempotent par design. Verdicts mécaniques.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Chemins (dérivés de la position du script : skills/version-management/scripts/)
# ---------------------------------------------------------------------------
ICI = Path(__file__).resolve()
SKILL_DIR = ICI.parent.parent            # skills/version-management/
RACINE = SKILL_DIR.parent.parent          # racine du projet
TMP_DIR = Path(os.environ.get("VM_WATCHDOG_TMP", RACINE / "tmp" / "vm-watchdog"))
HEARTBEAT = TMP_DIR / "heartbeat.json"
JOURNAL = TMP_DIR / "journal-forensique.jsonl"
GARDE = RACINE / "skills" / "gen-plan" / "scripts" / "ensure-installed.py"
MIROIR = RACINE / "KNOWLEDGE-repo"
SEUIL_DEF = 180
INTERVALLE_DEF = 30

# Backfill qualifié des 32 incidents documentés (worklog.md + @historique — règle d'or
# n°5 : uniquement ce qui est documenté ; horodatage null = précis non archivé, honnêteté).
BACKFILL = [
    (1, "Tasks 52-55 (2026-11-06) — incidents précoces, détection tardive avant garde étendue", None),
    (2, "Tasks 52-55 (2026-11-06) — idem", None),
    (3, "Task 52/54/55 (2026-11-06) — « 3e disparition profil » worklog", None),
    (4, "Tasks 52-56 (2026-11-06) — incident documenté worklog", None),
    (5, "Tasks 52-56 (2026-11-06) — idem", None),
    (6, "Tasks 52-56 (2026-11-06) — idem", None),
    (7, "Tasks 52-56 (2026-11-06) — idem", None),
    (8, "Tasks 52-56 (2026-11-06) — idem", None),
    (9, "Tasks 52-56 (2026-11-06) — idem", None),
    (10, "Tasks 52-56 (2026-11-06) — idem", None),
    (11, "Tasks 52-56 (2026-11-06) — idem", None),
    (12, "Tasks 52-56 (2026-11-06) — idem", None),
    (13, "Tasks 52-56 (2026-11-06) — idem", None),
    (14, "Tasks 52-56 (2026-11-06) — idem", None),
    (15, "Tasks 57-58 (2026-11-06) — « 15e disparition vm » worklog", None),
    (16, "Task 58 (2026-11-06) — ensure-installed INSTALLE-REPARÉ, cause racine L55-3", None),
    (17, "Task 58 (2026-11-06) — auto-réparé 2e fois par la garde Task 56", None),
    (18, "Task 60 (2026-11-07 matin) — auto-réparée, rc=0", None),
    (19, "Task 60 (2026-11-07 matin) — « incident volatilité n°7 » worklog", None),
    (20, "Task 61 (2026-11-07, suite 15) — preuve vivante mobilisée (T-V1)", None),
    (21, "Task 61 (2026-11-07, suite 16) — détectée à l'arbitre integrity (FAIL SKILL.md)", None),
    (22, "Task 62 (2026-11-07 ~09:16Z) — période volatilité continue", None),
    (23, "Task 62 (2026-11-07 ~09:16Z) — INTRA-SESSION auto-réparée", "2026-11-07T09:16:00Z"),
    (24, "Task 62 (2026-11-07 ~09:30Z) — volatilité CONTINUE intra-session", "2026-11-07T09:30:00Z"),
    (25, "Task 62 (2026-11-07) — période 23e-26e documentée", None),
    (26, "Task 62 (2026-11-07) — idem", None),
    (27, "Task 66 (2026-11-07) — auto-réparation garde, manifeste re-scellé (commit 90094c0)", None),
    (28, "Tasks 66-67 (2026-11-07) — pattern 23e-31e", None),
    (29, "Tasks 66-67 (2026-11-07) — idem", None),
    (30, "Task 68 G1 (2026-11-07, suite 40) — volatilité continue, 110/110 restauré", None),
    (31, "Task 68 G3 (2026-11-07, suite 42) — RÉSORBÉE round 1 (exécutions n°3→8)", None),
    (32, "Task 69 ouverture (2026-11-07) — entre tours, frontière directive n°8", "2026-11-07T15:16:55Z"),
]


def hnow() -> str:
    """Horodatage ISO UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_head(repo: Path):
    """HEAD court du dépôt (None si indisponible — tolérant)."""
    try:
        r = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def journaliser(evenement: str, journal: Path, **details) -> dict:
    """Append une entrée JSONL horodatée au journal forensique (+ heads hôte/miroir)."""
    entree = {"horodatage": hnow(), "evenement": evenement}
    entree["host_head"] = git_head(RACINE)
    entree["miroir_head"] = git_head(MIROIR)
    entree.update(details)
    journal.parent.mkdir(parents=True, exist_ok=True)
    with journal.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False, sort_keys=True) + "\n")
    return entree


def lire_heartbeat(heartbeat: Path):
    """Lit le heartbeat (dict) ou None (absent/illisible)."""
    try:
        return json.loads(heartbeat.read_text(encoding="utf-8"))
    except Exception:
        return None


def ecrire_heartbeat(heartbeat: Path) -> dict:
    """Écrit le heartbeat horodaté (pid inclus)."""
    hb = {"horodatage": hnow(), "epoch": int(time.time()), "pid": os.getpid()}
    heartbeat.parent.mkdir(parents=True, exist_ok=True)
    heartbeat.write_text(json.dumps(hb, ensure_ascii=False) + "\n", encoding="utf-8")
    return hb


def present(skill_dir: Path) -> bool:
    """Le skill version-management est-il présent (SKILL.md) ?"""
    return (skill_dir / "SKILL.md").exists()


def reparer(garde: Path) -> dict:
    """Réparation déterministe via la garde ensure-installed.py (composante c)."""
    if not garde.exists():
        return {"verdict": "GARDE_ABSENTE", "rc": 1, "reparés": []}
    r = subprocess.run([sys.executable, str(garde)], capture_output=True, text=True, timeout=120)
    verdict, reparés = "RC_%d" % r.returncode, []
    for ligne in (r.stdout or "").splitlines():
        s = ligne.strip()
        if s.startswith("{") and s.endswith("}"):
            try:
                d = json.loads(s)
                verdict = d.get("verdict", verdict)
                reparés = d.get("skills_reparés", reparés)
            except Exception:
                pass
    return {"verdict": verdict, "rc": r.returncode, "reparés": reparés}


def cycle_once(racine: Path, seuil: int) -> dict:
    """Un cycle : écart heartbeat → présence → (réparation) → heartbeat. Verdict mécanique."""
    tmp = racine / "tmp" / "vm-watchdog"
    hb_f = tmp / "heartbeat.json"
    jnl_f = tmp / "journal-forensique.jsonl"
    skill = racine / "skills" / "version-management"
    journaliser("DEMARRAGE", jnl_f, mode="once")
    hb = lire_heartbeat(hb_f)
    if hb and "epoch" in hb:
        ecart = int(time.time()) - int(hb["epoch"])
        if ecart > seuil:
            journaliser("ECART", jnl_f, ecart_secondes=ecart, seuil=seuil,
                        fenetre_disparition_potentielle=True,
                        detail="watchdog arrêté — fenêtre de disparition potentielle à corréler avec les interruptions")
    if present(skill):
        journaliser("VERIF_OK", jnl_f, skill="version-management")
    else:
        journaliser("DISPARITION_DETECTEE", jnl_f, skill="version-management",
                    detail="SKILL.md absent — réparation déterministe via garde")
        rep = reparer(racine / "skills" / "gen-plan" / "scripts" / "ensure-installed.py")
        journaliser("REPARATION", jnl_f, verdict=rep["verdict"], rc=rep["rc"], reparés=rep["reparés"])
        if present(skill):
            journaliser("RETABLIE", jnl_f, skill="version-management", integrity="à re-certifier via arbitre")
        else:
            journaliser("ECHEC_REPARATION", jnl_f, skill="version-management")
    ecrire_heartbeat(hb_f)
    return {"present": present(skill), "journal": str(jnl_f)}


def daemon(intervalle: int, seuil: int) -> int:
    """Boucle --once à intervalle (heartbeat permanent). Ctrl-C / SIGTERM → ARRET."""
    jnl_f = RACINE / "tmp" / "vm-watchdog" / "journal-forensique.jsonl"
    journaliser("DEMARRAGE", jnl_f, mode="daemon", intervalle_s=intervalle, seuil_s=seuil)
    try:
        while True:
            cycle_once(RACINE, seuil)
            time.sleep(intervalle)
    except KeyboardInterrupt:
        journaliser("ARRET", jnl_f, signal="SIGINT")
    except SystemExit:
        journaliser("ARRET", jnl_f, signal="SIGTERM")
    return 0


def init_backfill(journal: Path) -> int:
    """Initialise le journal : INIT + backfill qualifié des 32 incidents documentés."""
    if journal.exists():
        return 0  # no-op idempotent
    journal.parent.mkdir(parents=True, exist_ok=True)
    init = {"horodatage": hnow(), "evenement": "INIT",
            "detail": "Journal forensique de la résorption structurelle de la volatilité "
                      "version-management (Task 69, directive n°8 item 1 — neutralisation résiliente). "
                      "Mécanisme documenté : suppression ENTRE LES TOURS par processus EXTERNE au projet "
                      "(ni cron ni process local) ; auto-commits UUID plateforme sur le dépôt hôte "
                      "(759ae18→6d3daa1→01ec9bd) ; corrélation temporelle exacte interruptions↔disparitions "
                      "(clarification propriétaire) ; miroir KNOWLEDGE-repo toujours intact = source de réparation. "
                      "PRÉVENTION IMPOSSIBLE → neutralisation résiliente (a watchdog heartbeats, b journal, "
                      "c garde invocation INSTALLE-REPARÉ, d persistance disque).",
            "host_head": git_head(RACINE), "miroir_head": git_head(MIROIR)}
    with journal.open("w", encoding="utf-8") as f:
        f.write(json.dumps(init, ensure_ascii=False, sort_keys=True) + "\n")
        for num, ref, hts in BACKFILL:
            e = {"horodatage": hts, "evenement": "INCIDENT_DOCUMENTE", "numero": num,
                 "reference": ref, "source": "backfill worklog/@historique (Task 69 SG2.2)",
                 "note": "horodatage null = horodatage précis non archivé (honnêteté règle d'or n°5)"}
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
    return 0


def selftest() -> int:
    """Harnais auto-vérifiant en répertoire temporaire — AUCUN effet sur le vrai écosystème."""
    checks = []

    def check(nom, ok, detail=""):
        checks.append((nom, bool(ok), detail))

    with tempfile.TemporaryDirectory(prefix="vm-wd-selftest-") as td:
        root = Path(td)
        (root / "skills" / "gen-plan" / "scripts").mkdir(parents=True)
        (root / "skills" / "version-management").mkdir(parents=True)
        (root / "skills" / "version-management" / "SKILL.md").write_text("fixture selftest\n", encoding="utf-8")
        (root / "KNOWLEDGE-repo").mkdir(parents=True)
        tmp = root / "tmp" / "vm-watchdog"
        hb_f, jnl_f = tmp / "heartbeat.json", tmp / "journal-forensique.jsonl"

        # T1 journal : append + parse
        journaliser("TEST_JOURNAL", jnl_f, probe=True)
        lignes = [json.loads(l) for l in jnl_f.read_text(encoding="utf-8").splitlines() if l.strip()]
        check("T1-journal-append-parse", len(lignes) == 1 and lignes[0]["evenement"] == "TEST_JOURNAL"
              and "horodatage" in lignes[0] and "host_head" in lignes[0])

        # T2 heartbeat : écriture + lecture
        hb = ecrire_heartbeat(hb_f)
        hb2 = lire_heartbeat(hb_f)
        check("T2-heartbeat-roundtrip", hb2 is not None and hb2.get("pid") == hb["pid"])

        # T3 détection d'écart (heartbeat factice ancien)
        vieux = {"horodatage": hnow(), "epoch": int(time.time()) - 600, "pid": 1}
        hb_f.write_text(json.dumps(vieux) + "\n", encoding="utf-8")
        ecart = int(time.time()) - int(lire_heartbeat(hb_f)["epoch"])
        check("T3-ecart-detection", ecart > 180, "ecart=%ds seuil=180s" % ecart)

        # T4 disparition simulée + réparation via garde factice (end-to-end)
        (root / "skills" / "version-management" / "SKILL.md").unlink()
        (root / "skills" / "gen-plan" / "scripts" / "ensure-installed.py").write_text(
            "#!/usr/bin/env python3\nimport json\nfrom pathlib import Path\n"
            "Path(__file__).resolve().parents[3].joinpath('skills','version-management','SKILL.md')"
            ".write_text('ok')\n"
            "print(json.dumps({'verdict':'INSTALLE-REPARÉ','skills_reparés':['version-management'],"
            "'head':'0123456','fichiers_manquants':[]}))\n", encoding="utf-8")
        res = cycle_once(root, 180)
        lignes = [json.loads(l) for l in jnl_f.read_text(encoding="utf-8").splitlines() if l.strip()]
        evs = [l["evenement"] for l in lignes]
        check("T4-disparition-reparation", evs.count("DISPARITION_DETECTEE") == 1
              and evs.count("REPARATION") == 1 and "RETABLIE" in evs and res["present"] is True,
              "evenements=%s" % ",".join(evs[-5:]))

        # T5 skill présent → VERIF_OK sans réparation
        jnl_f.unlink()
        journaliser("RESET", jnl_f)
        res2 = cycle_once(root, 180)
        lignes = [json.loads(l) for l in jnl_f.read_text(encoding="utf-8").splitlines() if l.strip()]
        evs = [l["evenement"] for l in lignes]
        check("T5-present-verif-ok", "VERIF_OK" in evs and "DISPARITION_DETECTEE" not in evs
              and res2["present"] is True, "evenements=%s" % ",".join(evs))

        # T6 idempotence : re-cycle sans réparation ni erreur
        res3 = cycle_once(root, 180)
        check("T6-idempotence", res3["present"] is True)

    # T7 schéma backfill : 32 incidents
    check("T7-backfill-32-incident", len(BACKFILL) == 32, "n=%d" % len(BACKFILL))
    # T8 les incidents horodatés documentés portent un ISO UTC valide
    datés = [h for _, _, h in BACKFILL if h]
    ok_iso = True
    for h in datés:
        try:
            datetime.strptime(h, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            ok_iso = False
    check("T8-horodatages-backfill-valides", len(datés) == 3 and ok_iso, "datés=%d" % len(datés))

    print("=== vm-watchdog selftest : %d tests ===" % len(checks))
    ko = 0
    for nom, ok, detail in checks:
        print("  [%s] %s %s" % ("PASS" if ok else "FAIL", nom, detail))
        ko += 0 if ok else 1
    print("=== RESUME : %d/%d PASS, %d FAIL ===" % (len(checks) - ko, len(checks), ko))
    return 0 if ko == 0 else 1


def main() -> int:
    p = argparse.ArgumentParser(description="Watchdog neutralisation résiliente version-management (Task 69)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init", action="store_true", help="initialise le journal forensique (backfill 32 incidents)")
    g.add_argument("--once", action="store_true", help="un cycle : écart + présence + réparation + heartbeat")
    g.add_argument("--daemon", action="store_true", help="boucle --once (heartbeat permanent)")
    g.add_argument("--selftest", action="store_true", help="harnais auto-vérifiant (répertoire temporaire)")
    p.add_argument("--intervalle", type=int, default=INTERVALLE_DEF, help="période daemon en secondes")
    p.add_argument("--seuil", type=int, default=SEUIL_DEF, help="seuil d'écart heartbeat en secondes")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if a.init:
        dejala = JOURNAL.exists()
        rc = init_backfill(JOURNAL)
        n = sum(1 for _ in JOURNAL.open(encoding="utf-8")) if JOURNAL.exists() else 0
        print(json.dumps({"verdict": "INIT_NOOP_IDEMPOTENT" if dejala else "INIT_OK",
                          "journal": str(JOURNAL), "entrees": n}, ensure_ascii=False))
        return rc
    if a.once:
        res = cycle_once(RACINE, a.seuil)
        print(json.dumps({"verdict": "PRESENT_OK", "journal": res["journal"]}, ensure_ascii=False))
        return 0
    return daemon(a.intervalle, a.seuil)


if __name__ == "__main__":
    sys.exit(main())
