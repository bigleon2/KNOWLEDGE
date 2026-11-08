#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.34)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""Task 72 G1 — T1.1.0 : baseline golden master AVANT re-curation de gen-plan.

Directive complémentaire 2026-11-08 (trace 1a1b7b297b7b4975) : « en faisant des tests
(génère un protocole de test adapté à mon écosystème) AVANT d'effectuer les re-curations
progressive disclosure » — le présent script est le précurseur du protocole-test du futur
skill re-curation (G4) : phase PRE = --capturer, phase POST = --verifier.

Modes :
  --capturer       capture la baseline du SKILL.md gen-plan v3.38.0 INTACT →
                   download/task72-baseline-genplan.json (SHA-256 des 9 blocs déplacés
                   [brut + rstrip], contrats verrouillés §A/§0/read_when/evals, comptages
                   canoniques DANS §A, poids) ;
  --verifier-moves (pré-remplacement, D003) : chaque bloc extrait vers references/ par
                   task72-extraction-genplan.py est byte-identique à la baseline ;
  --verifier       (post-remplacement) : D001 partiel (version 3.39.0) · D002 (poids
                   < 30 Kio, réduction >= 60 % #token) · D003 (blocs ↔ references/) ·
                   D004 (aucune fenêtre de 1024 octets d'un bloc dupliquée inline) ·
                   D005 (contrats == baseline).

Liste verrouillée D005 (comparaison stricte avant/après) : bloc §A (déclencheurs
verbatim + glossaire $FACON/$FACON2), bloc §0 SHARED, lignes read_when, evals/evals.json,
evals/trigger_evals.json, comptages des commandes canoniques DANS §A. La description
frontmatter est étendue par conception (SG1.2) : son SHA est tracé, non verrouillé.

Règle d'or n°5 : tout chiffre affiché est mesuré ici. Python stdlib (N3). Idempotent ×2.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILL = RACINE / "skills" / "gen-plan" / "SKILL.md"
REFS = RACINE / "skills" / "gen-plan" / "references"
EVALS = RACINE / "skills" / "gen-plan" / "evals"
BASELINE = RACINE / "download" / "task72-baseline-genplan.json"

MOTIFS_CANONIQUES = [
    "gen-plan:", "gen-plan(step)", "gen-plan(step-ok)", "gen-plan:correct-work(projet)",
    "gen-plan:correct-work(<cible>)", "gen-plan:generate",
    "intègre dans le plan d'actions", "met à jour (le plan d'actions)", "orchestre",
    "$FACON", "$FACON2",
]

FICHIERS_MOVES = {  # cle → fichier references/ (bornes identiques à l'extracteur)
    "journal_versions": "journal-versions.md",
    "regles_or": "regles-or.md",
    "lecons_ko": "regles-or.md",
    "disciplines": "disciplines-mobilisation.md",
    "hooks_patterns": "protocoles-detailles.md",
    "routage_install": "protocoles-detailles.md",
    "mode_step": "protocoles-detailles.md",
    "philo4": "protocoles-detailles.md",
    "contingences": "grille-token.md",  # append, sans marqueur FIN
}


def sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def bornes(lignes, debut, fin=None, inclure_fin=False):
    """[i0, i1) : de la ligne contenant debut à la ligne contenant fin (exclue par défaut)."""
    i0 = next((i for i, l in enumerate(lignes) if debut in l), None)
    if i0 is None:
        raise SystemExit(f"ABANDON : marqueur introuvable ({debut!r})")
    if fin is None:
        return i0, i0 + 1
    i1 = next((i for i in range(i0, len(lignes)) if fin in lignes[i]), None)
    if i1 is None:
        raise SystemExit(f"ABANDON : borne de fin introuvable ({fin!r})")
    return i0, (i1 + 1 if inclure_fin else i1)


def blocs_9(lignes):
    """Les 9 blocs déplacés — bornes STRICTEMENT identiques à task72-extraction-genplan.py."""
    b = {}
    idx_56 = next(i for i, l in enumerate(lignes) if l.startswith("### §5.6"))
    j0 = next(i for i in range(idx_56, len(lignes))
              if re.match(r"^- \*\*v3\.\d+\.\d+ \(", lignes[i]))
    b["journal_versions"] = "\n".join(lignes[j0:])

    a, f = bornes(lignes, "### §1.5 Règles d'or", "### §1.6 Disciplines")
    b["regles_or"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "### §1.14 Leçons", "### §1.16 Routage")
    b["lecons_ko"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "### §1.6 Disciplines", "### §1.7 Pipeline")
    b["disciplines"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "<!-- PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->",
                  "<!-- FIN-PATTERN:GEN-PLAN-HOOKS-E7-DISP-v1.0.0 -->", inclure_fin=True)
    b["hooks_patterns"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "### §1.16 Routage", "## §2 — Spécification technique")
    b["routage_install"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "### §5.5 Mode step", "### §5.6 Journal des versions")
    b["mode_step"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "- **Coefficient profil frais local",
                  "- **Contingence récupération externe bloquée", inclure_fin=True)
    b["contingences"] = "\n".join(lignes[a:f])
    a, f = bornes(lignes, "4. **Parallélisation par défaut")
    b["philo4"] = lignes[a]
    return b


def bloc_depuis_references(chemin: Path, cle: str):
    """Extrait le bloc déplacé (contenu matériel, rstrip) d'un fichier references/."""
    texte = chemin.read_text(encoding="utf-8")
    m = re.search(r"<!-- BLOC-DEPLACÉ:" + re.escape(cle) + r":v3\.38\.0:[0-9a-f]{16} -->", texte)
    if not m:
        return None
    apres = texte[m.end():]
    ancre = "SHA-256 du bloc d'origine : `"
    i = apres.find(ancre)
    j = apres.find("`.", i + len(ancre))  # fin de la ligne de provenance : « `<sha>`. »
    if i < 0 or j < 0:
        return None
    reste = apres[j + 2:]
    if cle == "contingences":  # append en fin de fichier : pas de marqueur FIN
        return reste.strip("\n")
    k = reste.find("<!-- FIN-BLOC-DEPLACÉ:" + re.escape(cle) + " -->")
    if k < 0:
        return None
    return reste[:k].strip("\n")


def capturer() -> int:
    texte = SKILL.read_text(encoding="utf-8")
    lignes = texte.splitlines()
    a_, f_ = bornes(lignes, "## §A — DÉCLENCHEURS", "## §0 — Contexte Système")
    bloc_a = "\n".join(lignes[a_:f_])
    a0, f0 = bornes(lignes, "## §0 — Contexte Système", "## §1 — Spécification fonctionnelle")
    bloc_0 = "\n".join(lignes[a0:f0])
    ar, fr = bornes(lignes, "read_when:", "---")
    read_when = "\n".join(lignes[ar:fr])
    version = next(l.split(":", 1)[1].strip() for l in lignes if l.startswith("version:"))

    b9 = blocs_9(lignes)
    donnees = {
        "horodatage": "2026-11-08T10:45:00Z",
        "skill_md": {
            "version": version, "octets": len(texte.encode("utf-8")),
            # Convention de mesure (note croisée Task 76 D010 — différés Task 75
            # §6.4) : ici octets disque COMPLETS (read_text intégral) — le
            # protocole-test.py du skill re-curation mesure 1 o de moins
            # (join(splitlines()), saut final non reconstitué) : ex. gen-plan
            # 30 668 o ici vs 30 667 o là-bas ; chaque mesureur self-consistant.
            "lignes": len(lignes), "sha256": sha(texte),
            "kio": round(len(texte.encode("utf-8")) / 1024, 1),
            "token_estimes": len(texte.encode("utf-8")) // 4,
        },
        "blocs": {
            cle: {"sha256_brut": sha(v), "sha256_rstrip": sha(v.rstrip("\n")),
                  "octets": len(v.encode("utf-8")), "octets_rstrip": len(v.rstrip("\n").encode("utf-8"))}
            for cle, v in b9.items()
        },
        "contrats": {
            "bloc_A_sha256": sha(bloc_a), "bloc_A_octets": len(bloc_a.encode("utf-8")),
            "bloc_0_sha256": sha(bloc_0), "bloc_0_octets": len(bloc_0.encode("utf-8")),
            "read_when_sha256": sha(read_when),
            "evals_json_sha256": sha((EVALS / "evals.json").read_text(encoding="utf-8")),
            "trigger_evals_json_sha256": sha((EVALS / "trigger_evals.json").read_text(encoding="utf-8")),
            "comptages_dans_A": {m: bloc_a.count(m) for m in MOTIFS_CANONIQUES},
        },
    }
    BASELINE.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"BASELINE capturée → {BASELINE}")
    print(f"  SKILL.md v{version} : {donnees['skill_md']['octets']} octets "
          f"({donnees['skill_md']['kio']} Kio ≈ {donnees['skill_md']['token_estimes']} #token)")
    total = sum(v["octets"] for v in donnees["blocs"].values())
    for cle, v in donnees["blocs"].items():
        print(f"  bloc {cle:<16} {v['octets']:>6} octets  sha {v['sha256_brut'][:12]}")
    print(f"  total 9 blocs : {total} octets ({total/1024:.1f} Kio)")
    print(f"  contrats : §A {donnees['contrats']['bloc_A_octets']} o · §0 "
          f"{donnees['contrats']['bloc_0_octets']} o · read_when · evals ×2 · "
          f"comptages §A {len(MOTIFS_CANONIQUES)} motifs")
    return 0


def verifier_moves() -> int:
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    print("=== D003 (pré-remplacement) — moves R4 byte-identiques baseline ↔ references/ ===")
    ok = True
    for cle, fichier in FICHIERS_MOVES.items():
        extrait = bloc_depuis_references(REFS / fichier, cle)
        if extrait is None:
            print(f"  [FAIL] {cle} : marqueur BLOC-DEPLACÉ introuvable dans {fichier}")
            ok = False
            continue
        attendu = base["blocs"][cle]["sha256_rstrip"]
        match = sha(extrait) == attendu
        ok = ok and match
        print(f"  [{'PASS' if match else 'FAIL'}] {cle:<16} ↔ {fichier} "
              f"({len(extrait.encode('utf-8'))} octets)")
    print(f"VERDICT D003 moves : {'PASS (9/9 byte-identiques)' if ok else 'FAIL'}")
    return 0 if ok else 1


def verifier() -> int:
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    texte = SKILL.read_text(encoding="utf-8")
    lignes = texte.splitlines()
    octets = len(texte.encode("utf-8"))
    avant = base["skill_md"]
    resultats = {}

    # D001 partiel : version
    version = next(l.split(":", 1)[1].strip() for l in lignes if l.startswith("version:"))
    resultats["D001_version"] = (version == "3.39.0", f"version frontmatter = {version}")

    # D002 : poids
    kio = octets / 1024
    reduc = 100 * (1 - octets / avant["octets"])
    resultats["D002_poids"] = (
        octets < 30 * 1024 and reduc >= 60,
        f"{octets} octets ({kio:.1f} Kio ≈ {octets//4} #token) — réduction "
        f"{reduc:.1f}% (avant {avant['octets']} octets / {avant['kio']} Kio)")

    # D003 : blocs ↔ references/ (SHA rstrip)
    d003 = True
    details003 = []
    for cle, fichier in FICHIERS_MOVES.items():
        extrait = bloc_depuis_references(REFS / fichier, cle)
        if extrait is None or sha(extrait) != base["blocs"][cle]["sha256_rstrip"]:
            d003 = False
            details003.append(f"{cle}≠{fichier}")
    resultats["D003_moves"] = (d003, "9/9 byte-identiques baseline ↔ references/"
                                if d003 else "écarts : " + ", ".join(details003))

    # D004 : non-duplication (fenêtres 1024 octets, pas 512)
    d004 = True
    details004 = []
    for cle in FICHIERS_MOVES:
        extrait = bloc_depuis_references(REFS / fichier_of(cle), cle) or ""
        b = extrait.encode("utf-8")
        if len(b) <= 1024:
            if extrait in texte:
                d004 = False
                details004.append(f"{cle} (bloc entier dupliqué)")
        else:
            for i in range(0, len(b) - 1024 + 1, 512):
                if b[i:i + 1024] in texte.encode("utf-8"):
                    d004 = False
                    details004.append(f"{cle} @offset {i}")
                    break
    resultats["D004_non_duplication"] = (
        d004, "aucune fenêtre 1024 o d'un bloc déplacé dupliquée inline"
        if d004 else "duplications : " + ", ".join(details004))

    # D005 : contrats inline == baseline
    a_, f_ = bornes(lignes, "## §A — DÉCLENCHEURS", "## §0 — Contexte Système")
    bloc_a = "\n".join(lignes[a_:f_])
    a0, f0 = bornes(lignes, "## §0 — Contexte Système", "## §1 — Spécification fonctionnelle")
    bloc_0 = "\n".join(lignes[a0:f0])
    ar, fr = bornes(lignes, "read_when:", "---")
    read_when = "\n".join(lignes[ar:fr])
    c = base["contrats"]
    d005 = True
    details005 = []
    if sha(bloc_a) != c["bloc_A_sha256"]:
        d005 = False; details005.append("bloc §A")
    # harnais v2 (SG1.4) : étiquette SHARED normalisée si référence étendue présente —
    # le bump SHARED par propagate-context est une évolution écosystème légitime (preuve :
    # §0 == baseline modulo étiquette, consigné au baseline JSON) ; le CONTENU du contrat
    # reste comparé intégralement.
    ref_0 = c.get("bloc_0_sha256_sans_label")
    bloc_0_cmp = (re.sub(r"SHARED v[\d.]+", "SHARED ‹label›", bloc_0)
                  if ref_0 else bloc_0)
    if sha(bloc_0_cmp) != (ref_0 or c["bloc_0_sha256"]):
        d005 = False; details005.append("bloc §0 SHARED")
    if sha(read_when) != c["read_when_sha256"]:
        d005 = False; details005.append("read_when")
    if sha((EVALS / "evals.json").read_text(encoding="utf-8")) != c["evals_json_sha256"]:
        d005 = False; details005.append("evals.json")
    if sha((EVALS / "trigger_evals.json").read_text(encoding="utf-8")) != c["trigger_evals_json_sha256"]:
        d005 = False; details005.append("trigger_evals.json")
    comptages = {m: bloc_a.count(m) for m in MOTIFS_CANONIQUES}
    if comptages != c["comptages_dans_A"]:
        d005 = False; details005.append("comptages canoniques §A")
    resultats["D005_contrats"] = (
        d005, "§A + §0 SHARED + read_when + evals ×2 + comptages §A == baseline"
        if d005 else "écarts : " + ", ".join(details005))

    print("=== Vérification POST re-curation (D001 partiel, D002, D003, D004, D005) ===")
    for k, (ok, detail) in resultats.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {k} — {detail}")
    verdict = all(ok for ok, _ in resultats.values())
    print(f"VERDICT POST : {'PASS' if verdict else 'FAIL'}")
    rapport = {"verdict": "PASS" if verdict else "FAIL",
               "resultats": {k: {"statut": "PASS" if ok else "FAIL", "detail": d}
                             for k, (ok, d) in resultats.items()},
               "poids": {"octets": octets, "kio": round(kio, 1), "token_estimes": octets // 4,
                          "reduction_pct": round(reduc, 1)}}
    (RACINE / "download" / "task72-verif-recuration.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  rapport → download/task72-verif-recuration.json")
    return 0 if verdict else 1


def fichier_of(cle):
    return FICHIERS_MOVES[cle]


def main() -> int:
    ap = argparse.ArgumentParser(description="Baseline golden master + vérificateur re-curation gen-plan (T1.1.0)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--capturer", action="store_true")
    g.add_argument("--verifier-moves", action="store_true")
    g.add_argument("--verifier", action="store_true")
    args = ap.parse_args()
    if args.capturer:
        return capturer()
    if args.verifier_moves:
        return verifier_moves()
    return verifier()


if __name__ == "__main__":
    sys.exit(main())
