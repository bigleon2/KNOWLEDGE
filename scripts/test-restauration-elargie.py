#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Test de restauration élargi — corruption multi-fichiers + piliers (Task 7).

Protocole en phases (chaque phase idempotente et relançable) :
  --baseline         état initial : arbitre integrity --check + SHA 32 SKILL.md
                     + 9 corpus comparés au manifeste scellé (refus si état souillé)
  --corrupt          sauvegarde de sûreté (7 fichiers) puis corruption contrôlée :
                     3 corpus (append), 1 pilier agressif (version cassée),
                     3 piliers silencieux (append)
  --detect           constat de détection : arbitre integrity --check, matrice
                     corruption → détecté / non détecté
  --reinstall        réinstallateur en mode autonome (sans argument)
  --restore-pillars  restauration des 4 piliers depuis les sauvegardes
                     (les piliers ne sont PAS dans l'archive v2.2 → voie externe de test)
  --verify           SHA corpus vs manifeste + SHA piliers vs sauvegardes + garde --check
  --cleanup          suppression du répertoire de sauvegarde
  --report           rapport JSON consolidé dans scripts/outputs/

Racines dérivées de __file__ (L008 — portabilité des chemins, jamais de chemin absolu).
Chemins : BASE = parents[1] du présent script (scripts/ → profil).
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CORPUS = BASE / "skills" / "@mon-ecosysteme"
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
MANIFEST = BASE / "scripts" / "ecosysteme-integrity.json"
BACKUP = BASE / "scripts" / "outputs" / "sauvegarde-test-elargie"
OUTDIR = BASE / "scripts" / "outputs"
MARQUEUR_MD = "\n<!-- [TEST-ELARGIE-T7] corruption contrôlée — ligne ajoutée -->\n"
MARQUEUR_PY = "\n# [TEST-ELARGIE-T7] corruption contrôlée — ligne ajoutée\n"

# (chemin relatif au profil, mode) — 7 cibles : 3 corpus + 4 piliers
CIBLES = [
    ("skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", "append"),
    ("skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md", "append"),
    ("skills/@mon-ecosysteme/SYNC-CONTEXT.md", "append"),
    ("skills/gen-plan/SKILL.md", "append"),           # pilier silencieux
    ("skills/correct-work/SKILL.md", "strip-version"),  # pilier agressif
    ("skills/KNOWLEDGE.md", "append"),                 # pilier silencieux
    ("scripts/certification-complete.py", "append-py"),  # pilier silencieux
]
PILIERS = [c for c, _ in CIBLES if not c.startswith("skills/@mon-ecosysteme")]

RAPPORT = {"phases": {}, "ts_debut": time.strftime("%Y-%m-%d %H:%M:%S")}
STATE = OUTDIR / "test-elargie-etat.json"  # état persistant entre invocations (phases multiples)
if STATE.exists():
    RAPPORT = json.loads(STATE.read_text(encoding="utf-8"))


def sauver_etat():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(RAPPORT, indent=2, ensure_ascii=False), encoding="utf-8")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE), **kw)
    return r.returncode, r.stdout, r.stderr


def integrity():
    rc, out, err = run([sys.executable, "scripts/check-ecosysteme-integrity.py", "--check"])
    res = [l.strip() for l in (out + err).splitlines() if "[FAIL]" in l]
    resume = next((l.strip() for l in out.splitlines() if "RESUME" in l), "?")
    return rc, resume, res


def garde():
    rc, out, _ = run([sys.executable, "skills/gen-plan/scripts/ensure-installed.py", "--check"])
    verdict = next((l.strip() for l in out.splitlines() if l.strip()), "?")
    return rc, verdict


def phase_baseline():
    rc, resume, fails = integrity()
    mani = json.loads(MANIFEST.read_text(encoding="utf-8"))
    der_corpus = [n for n, s in mani.get("corpus", {}).items()
                  if not (CORPUS / n).exists() or sha256(CORPUS / n) != s]
    der_skills = [k for k, m in mani.get("skills", {}).items()
                  if not (BASE / "skills" / k / "SKILL.md").exists()
                  or sha256(BASE / "skills" / k / "SKILL.md") != m.get("sha256")]
    etat = {"integrity_rc": rc, "integrity": resume, "integrity_fails": fails,
            "sha_corpus_derives": der_corpus, "sha_skills_derives": der_skills}
    RAPPORT["phases"]["baseline"] = etat
    print("=== BASELINE ===")
    print(f"  integrity --check : rc={rc} — {resume}")
    print(f"  SHA corpus vs manifeste : {len(mani.get('corpus', {})) - len(der_corpus)}/{len(mani.get('corpus', {}))} conformes")
    print(f"  SHA skills vs manifeste : {len(mani.get('skills', {})) - len(der_skills)}/{len(mani.get('skills', {}))} conformes")
    if rc != 0 or der_corpus or der_skills:
        print("  ✋ ÉTAT SOUILLÉ — refus de corrompre (restaurer/re-certifier d'abord)")
        sys.exit(1)
    print("  état certifié propre — test autorisé")


def phase_corrupt():
    if BACKUP.exists():
        print(f"✋ sauvegarde déjà présente ({BACKUP}) — corruption déjà appliquée (relancer --detect)")
        sys.exit(1)
    BACKUP.mkdir(parents=True)
    detail = {}
    for rel, mode in CIBLES:
        src = BASE / rel
        dst = BACKUP / rel.replace("/", "__")
        shutil.copy2(src, dst)
        content = src.read_text(encoding="utf-8")
        if mode == "append":
            src.write_text(content + MARQUEUR_MD, encoding="utf-8")
        elif mode == "append-py":
            src.write_text(content + MARQUEUR_PY, encoding="utf-8")
        elif mode == "strip-version":
            lignes = content.splitlines(keepends=True)
            out, tue = [], False
            for l in lignes:
                if not tue and l.startswith("version:"):
                    out.append("version: BROKEN-TEST\n")
                    tue = True
                else:
                    out.append(l)
            if not tue:
                print(f"  ✋ {rel} : ligne version introuvable — corruption impossible")
                sys.exit(1)
            src.write_text("".join(out), encoding="utf-8")
        detail[rel] = {"mode": mode, "sha_avant": sha256(dst), "sha_apres": sha256(src),
                       "corrompu": sha256(dst) != sha256(src)}
    RAPPORT["phases"]["corrupt"] = detail
    print("=== CORRUPTION CONTRÔLÉE (7 fichiers, sauvegardes dans scripts/outputs/sauvegarde-test-elargie/) ===")
    for rel, d in detail.items():
        print(f"  [{mode_lib(d['mode'])}] {rel} — SHA modifié : {d['corrompu']}")


def mode_lib(m):
    return {"append": "append silencieux", "append-py": "append py silencieux",
            "strip-version": "version cassée (agressif)"}[m]


def phase_detect():
    rc, resume, fails = integrity()
    mani = json.loads(MANIFEST.read_text(encoding="utf-8"))
    # détection indépendante par SHA (référence = manifeste scellé)
    detect_sha = {}
    for rel, mode in CIBLES:
        p = BASE / rel
        nom = Path(rel).name
        if rel.startswith("skills/@mon-ecosysteme/"):
            ref = mani.get("corpus", {}).get(nom)
        elif rel == "skills/KNOWLEDGE.md":
            ref = None  # non scellé au manifeste
        else:
            ref = mani.get("skills", {}).get(Path(rel).parts[-2], {}).get("sha256")
        detect_sha[rel] = (ref is not None and p.exists() and sha256(p) != ref) if ref else None
    RAPPORT["phases"]["detect"] = {"integrity_rc": rc, "integrity": resume,
                                   "fails": fails, "detect_sha_vs_manifeste": detect_sha}
    print("=== DÉTECTION (arbitre integrity --check) ===")
    print(f"  rc={rc} — {resume}")
    for f in fails:
        print(f"    FAIL → {f}")
    print("  matrice SHA vs manifeste scellé (None = fichier non scellé) :")
    for rel, mode in CIBLES:
        d = detect_sha[rel]
        print(f"    {rel} : {'DÉTECTÉ (SHA divergent)' if d else ('NON SCELLÉ au manifeste' if d is None else 'non détecté')} [{mode_lib(mode)}]")


def phase_reinstall():
    rc, out, err = run(["bash", "scripts/install-ecosysteme-local.sh"])
    texte = out + err
    lignes = [l for l in texte.splitlines() if any(k in l for k in
              ("restauré", "pilier", "dérive", "DÉRIVE", "CONFORME", "RESUME", "MODE", "corpus :",
               "SHA divergent", "manquant", "introuvable"))]
    RAPPORT["phases"][f"reinstall_{time.strftime('%H%M%S')}"] = {"rc": rc, "extraits": lignes}
    print(f"=== RÉINSTALLEUR AUTONOME (sans argument) — rc={rc} ===")
    for l in lignes:
        print(f"  | {l}")
    return rc


def phase_restore_pillars():
    if not BACKUP.exists():
        print("✋ aucune sauvegarde — rien à restaurer")
        sys.exit(1)
    ok = 0
    for rel in PILIERS:
        dst, src = BACKUP / rel.replace("/", "__"), BASE / rel
        if dst.exists():
            shutil.copy2(dst, src)
            conf = sha256(src) == sha256(dst)
            ok += 1 if conf else 0
            print(f"  pilier restauré depuis sauvegarde : {rel} — byte-identique : {conf}")
    RAPPORT["phases"]["restore_pillars"] = {"restaures": ok, "attendus": len(PILIERS)}
    print(f"piliers restaurés : {ok}/{len(PILIERS)}")


def phase_verify():
    mani = json.loads(MANIFEST.read_text(encoding="utf-8"))
    der_corpus = [n for n, s in mani.get("corpus", {}).items()
                  if not (CORPUS / n).exists() or sha256(CORPUS / n) != s]
    der_skills = [k for k, m in mani.get("skills", {}).items()
                  if not (BASE / "skills" / k / "SKILL.md").exists()
                  or sha256(BASE / "skills" / k / "SKILL.md") != m.get("sha256")]
    piliers_ok = all(sha256(BASE / rel) == sha256(BACKUP / rel.replace("/", "__"))
                     for rel in PILIERS if (BACKUP / rel.replace("/", "__")).exists())
    rc_i, resume, fails = integrity()
    rc_g, verdict = garde()
    etat = {"sha_corpus_derives": der_corpus, "sha_skills_derives": der_skills,
            "piliers_byte_identiques": piliers_ok, "integrity_rc": rc_i,
            "integrity": resume, "garde_rc": rc_g, "garde": verdict}
    RAPPORT["phases"]["verify"] = etat
    print("=== VÉRIFICATION FINALE ===")
    print(f"  SHA corpus vs manifeste : {len(mani.get('corpus', {})) - len(der_corpus)}/{len(mani.get('corpus', {}))} conformes (dérives : {der_corpus or 'aucune'})")
    print(f"  SHA skills vs manifeste : {len(mani.get('skills', {})) - len(der_skills)}/{len(mani.get('skills', {}))} conformes (dérives : {der_skills or 'aucune'})")
    print(f"  piliers byte-identiques aux sauvegardes : {piliers_ok}")
    print(f"  integrity --check : rc={rc_i} — {resume}")
    print(f"  garde É1-INSTALL  : rc={rc_g} — {verdict}")
    return rc_i == 0 and not der_corpus and not der_skills and piliers_ok and rc_g == 0


def phase_cleanup():
    if BACKUP.exists():
        shutil.rmtree(BACKUP)
        print(f"sauvegardes supprimées : {BACKUP}")
    RAPPORT["phases"]["cleanup"] = True


def phase_report():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    f = OUTDIR / f"test-restauration-elargie-{time.strftime('%Y%m%d-%H%M%S')}.json"
    RAPPORT["ts_fin"] = time.strftime("%Y-%m-%d %H:%M:%S")
    f.write_text(json.dumps(RAPPORT, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"rapport JSON : {f}")
    print(f"phases consignées : {sorted(RAPPORT.get('phases', {}))}")
    if STATE.exists():
        STATE.unlink()  # état consommé


PHASES = {
    "baseline": phase_baseline, "corrupt": phase_corrupt, "detect": phase_detect,
    "reinstall": phase_reinstall, "restore-pillars": phase_restore_pillars,
    "verify": phase_verify, "cleanup": phase_cleanup, "report": phase_report,
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Test de restauration élargi (Task 7)")
    ap.add_argument("phases", nargs="+", choices=sorted(PHASES),
                    help="phases à exécuter, dans l'ordre donné")
    args = ap.parse_args()
    for p in args.phases:
        PHASES[p]()
        sauver_etat()
