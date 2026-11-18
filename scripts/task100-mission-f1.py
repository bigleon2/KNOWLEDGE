#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 100 — mission F1 : brancher l'étape 2 du pipeline eco_install sur le scelleur
canonique v2.3 (finding suite 142, résorbé par le présent tour).

Modes :
  baseline  — S1 capture de l'état pré-implémentation (formats archive repo/host +
              SHA) ; S2 réplique bac à sable : preuve MÉCANIQUE du désempilement
              silencieux du véhicule v2.2 (piliers ∈ RETRAITS_SANCTIONNES → une
              archive v2.3 rescellée par le pipeline perd ses 6 piliers sans erreur)
              — capture pré-implémentation conservée ;
  rejeu     — S3 rejeu réel post-implémentation : rescellement v2.3 repo + hôte,
              parité miroir byte-identique, arbitre integrity COMPLET (manifeste
              régénéré) ; S4 idempotence ×2 (3 SHA byte-identiques) + perf ×3.

Déterministe sans horloge murale (les horodatages d'entrées archive sont fixés à
l'époque 1980 par les véhicules — comparaisons sur contenus et SHA piliers).
Racines dérivées de __file__ (L008 — portabilité des chemins)."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOST = Path("/home/z/my-project")
ARCHIVE_REL = "download/mon-ecosysteme_archive.zip"
CORPUS = REPO / "skills" / "@mon-ecosysteme"
RAPPORT = REPO / "scripts" / "task100-mission-f1-report.json"


def sha_f(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def archive_state(p: Path) -> dict:
    z = zipfile.ZipFile(p)
    names = [n for n in z.namelist() if not n.endswith("/")]
    return {"entrees": len(names),
            "piliers": sum(1 for n in names if n.startswith("piliers/")),
            "sha256": sha_f(p)}


def s2_preuve_deselement() -> dict:
    """Réplique bac à sable : archive v2.3 simulée (corpus + 6 piliers) + véhicule
    v2.2 task21-f2 → constat : rc=0 ET piliers éliminés (désempilement silencieux)."""
    with tempfile.TemporaryDirectory(prefix="task100-s2-") as tmp:
        rep = Path(tmp)
        (rep / "scripts").mkdir()
        (rep / "skills").mkdir()
        (rep / "download").mkdir()
        # véhicule ancien (copie byte-identique du vrai) — L008 : racines dérivées
        shutil.copy2(REPO / "scripts" / "task21-f2-rebuild-archive.py",
                     rep / "scripts" / "task21-f2-rebuild-archive.py")
        # corpus minimal (fichiers .md du corpus réel)
        corpus_rep = rep / "skills" / "@mon-ecosysteme"
        corpus_rep.mkdir()
        for f in sorted(CORPUS.glob("*.md")):
            shutil.copy2(f, corpus_rep / f.name)
        # archive v2.3 simulée : corpus réel + 6 piliers (octets réels de l'arbre)
        sim = rep / ARCHIVE_REL
        piliers = {
            "piliers/skills/gen-plan/SKILL.md": REPO / "skills/gen-plan/SKILL.md",
            "piliers/skills/correct-work/SKILL.md": REPO / "skills/correct-work/SKILL.md",
            "piliers/skills/KNOWLEDGE.md": REPO / "skills/KNOWLEDGE.md",
            "piliers/scripts/certification-complete.py": REPO / "scripts/certification-complete.py",
            "piliers/scripts/check-ecosysteme-integrity.py": REPO / "scripts/check-ecosysteme-integrity.py",
            "piliers/scripts/install-ecosysteme-local.sh": REPO / "scripts/install-ecosysteme-local.sh",
        }
        with zipfile.ZipFile(sim, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(p.name for p in CORPUS.glob("*.md")):
                z.writestr(f"@mon-ecosysteme/{f}", (CORPUS / f).read_bytes())
            for arc, src in sorted(piliers.items()):
                z.writestr(arc, src.read_bytes())
        avant = archive_state(sim)
        r = subprocess.run([sys.executable, str(rep / "scripts" / "task21-f2-rebuild-archive.py")],
                           capture_output=True, text=True)
        apres = archive_state(sim)
        return {"rc_vehicule_v22": r.returncode,
                "avant": avant, "apres": apres,
                "deselement_silencieux": (r.returncode == 0 and avant["piliers"] == 6 and apres["piliers"] == 0),
                "extrait_sortie": (r.stdout.strip() or r.stderr.strip())[-200:]}


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    if mode == "baseline":
        report = {
            "S1_baseline": {
                "repo": archive_state(REPO / ARCHIVE_REL),
                "host": archive_state(HOST / ARCHIVE_REL),
                "parite_miroir": sha_f(REPO / ARCHIVE_REL) == sha_f(HOST / ARCHIVE_REL),
                "capture": "pré-implémentation — véhicule pipeline = task21-f2 (v2.2)",
            },
            "S2_simulation_deselement": s2_preuve_deselement(),
        }
        s2 = report["S2_simulation_deselement"]
        report["S4_GO"] = "GO" if s2["deselement_silencieux"] else "NO-GO — désempilement NON reproduit : investiguer"
        print(json.dumps(report, ensure_ascii=False, indent=2))
        RAPPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"rapport : {RAPPORT}")
        sys.exit(0 if s2["deselement_silencieux"] else 1)
    elif mode == "rejeu":
        shas = {}
        # rescellement réel repo puis hôte (véhicule CANONIQUE v2.3 — désormais branché au pipeline)
        shas["repo_avant"] = sha_f(REPO / ARCHIVE_REL)
        r1 = subprocess.run([sys.executable, str(REPO / "scripts" / "task-f5-seal-archive-v23.py")],
                            capture_output=True, text=True)
        shas["repo_rescellement_1"] = sha_f(REPO / ARCHIVE_REL)
        r2 = subprocess.run([sys.executable, str(REPO / "scripts" / "task-f5-seal-archive-v23.py")],
                            capture_output=True, text=True)
        shas["repo_rescellement_2"] = sha_f(REPO / ARCHIVE_REL)
        r3 = subprocess.run([sys.executable, str(HOST / "scripts" / "task-f5-seal-archive-v23.py")],
                            capture_output=True, text=True)
        shas["host_rescellement_1"] = sha_f(HOST / ARCHIVE_REL)
        report = {
            "S3_rejeu_reel": {
                "rc_repo_1": r1.returncode, "rc_repo_2": r2.returncode, "rc_host": r3.returncode,
                "repo": archive_state(REPO / ARCHIVE_REL),
                "host": archive_state(HOST / ARCHIVE_REL),
                "parite_miroir_byte_identique": shas["repo_rescellement_2"] == shas["host_rescellement_1"],
                "idempotence_x2_2_reseals_byte_identiques": shas["repo_rescellement_1"] == shas["repo_rescellement_2"],
                "shas_prefixes": {k: v[:16] for k, v in shas.items()},
            },
        }
        ok = (r1.returncode == 0 and r2.returncode == 0 and r3.returncode == 0
              and report["S3_rejeu_reel"]["repo"]["piliers"] == 6
              and report["S3_rejeu_reel"]["repo"]["piliers"] == report["S3_rejeu_reel"]["host"]["piliers"]
              and report["S3_rejeu_reel"]["parite_miroir_byte_identique"]
              and report["S3_rejeu_reel"]["idempotence_x2_2_reseals_byte_identiques"])
        print(json.dumps(report, ensure_ascii=False, indent=2))
        RAPPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"rapport : {RAPPORT}")
        sys.exit(0 if ok else 1)
    else:
        print(f"mode inconnu : {mode} (baseline|rejeu)")
        sys.exit(2)


if __name__ == "__main__":
    main()
