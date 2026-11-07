#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.27)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

pm-skill v1.0.0 — Bras exécutable du skill pm-skill (Task 60 G3-SG2, D604
VALIDÉE par le propriétaire — verbatim « je valide ta proposition, tu peux
l'exécuter $FACON pour me générer $FACON un écosystème $FACON2 », session
web-c30e6506, 2026-11-07) : génération de PROMPTS MAÎTRES ÉPHÉMÈRES
auto-portants depuis les SKILL.md vivants de la racine skills/. Forme de
production du prototype testé par le harnais scripts/task60-tests-comparatifs.py
(D603b : 16 PASS · 1 FAIL [défaut réel de l'écosystème actuel — PM gen-plan
corpus non auto-portant] · 7 FACT ; tests B1-B7 verts). Unique extension par
rapport au prototype testé (fidélité à la proposition §3 validée) : section
HISTORIQUE CONDENSÉ projetée depuis skills/@historique/historiques-par-skill/
lorsqu'un historique existe.

Zéro invention (KO-L003) : le contenu du PM éphémère provient EXCLUSIVEMENT du
SKILL.md source (frontmatter + corps — le bloc §0 Contexte Système propagé est
embarqué verbatim, d'où l'auto-portance SHARED §6.2) et de l'historique archivé ;
le script structure, il ne rédige pas.

Déterminisme/idempotence ×2 : même SKILL.md (même jour) → sortie byte-identique
(re-jeu sans effet). 0 octet d'état : les sorties vont dans download/ (livrables
régénérables/supprimables), JAMAIS dans skills/ ni @mon-ecosysteme/ — corpus
intact, KO-L004 continue pour les 4 familles (couche additive).

Usage :
    python3 scripts/generer-pm-ephemere.py --generate <skill>   # → download/PM-ephemere-<skill>-v<version>.md
    python3 scripts/generer-pm-ephemere.py --generate <skill> --out <dir>   # sortie ailleurs (tests)
    python3 scripts/generer-pm-ephemere.py --check <skill>      # éligibilité + cohérence
    python3 scripts/generer-pm-ephemere.py --list               # skills racine éligibles
    python3 scripts/generer-pm-ephemere.py --self-test          # self-test embarqué (tempdir, zéro écriture hors tempdir)

Codes retour : 0 OK · 1 échec (dont self-test FAIL) · 2 usage invalide ·
3 skill inconnu ou inéligible (aligné sur generer-pm-skill.py — le refus
mécanique est honnête, jamais une génération dégradée).
"""

import hashlib
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
DOWNLOAD = BASE / "download"
HISTORIQUE = SKILLS / "@historique" / "historiques-par-skill"
MOTIF_SECTION0 = "§0 — Contexte Système"  # bloc propagé propagate-context (F6 — prérequis d'auto-portance)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def skills_racine():
    """Skills éligibles = dossiers racine skills/ avec SKILL.md (hors @dirs/fichiers)."""
    out = []
    for d in sorted(SKILLS.iterdir()):
        if d.name.startswith("@") or not d.is_dir():
            continue
        if (d / "SKILL.md").is_file():
            out.append(d.name)
    return out


def parse_frontmatter(text):
    """Sépare frontmatter YAML (--- ... ---) et corps ; extrait name/version/
    description/dépendances sans inventer (verbatim du fichier)."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm, body = m.group(1), m.group(2)
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    version = re.search(r"^version:\s*[\"']?([\d.]+(?:-[A-Za-z0-9.-]+)?)", fm, re.M)
    desc = re.search(r"^description:\s*>-?\s*\n((?:\s{2,}.*\n?)+)", fm, re.M)
    description = re.sub(r"\s+", " ", desc.group(1)).strip() if desc else ""
    deps = []
    dm = re.search(r"^dependencies:\n((?:\s+- skill:.*\n(?:\s{4,}.*\n?)*)+)", fm, re.M)
    if dm:
        for bloc in re.finditer(r"-\s+skill:\s*(\S+)\s*\n\s+version:\s*[\"']?([^\"'\n]+)[\"']?\s*\n(?:\s+used_at:\s*(.+))?", dm.group(1)):
            deps.append({"skill": bloc.group(1), "version": bloc.group(2).strip(),
                         "used_at": (bloc.group(3) or "").strip().strip('"')})
    return {"name": name.group(1) if name else "", "version": version.group(1) if version else "",
            "description": description, "dependencies": deps}, body


def historique_condense(skill_name):
    """Projette les lignes de versions depuis @historique/historiques-par-skill/
    <skill>.md (verbatim tronqué — zéro rédaction). None si aucun historique."""
    hpath = HISTORIQUE / ("%s.md" % skill_name)
    if not hpath.is_file():
        return None
    lignes = []
    for raw in hpath.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        # Table 4 colonnes : ['', Version, Date, Améliorations, Avantage, '']
        if len(cells) < 5 or not re.match(r"^v\d+\.\d+\.\d+", cells[1] or ""):
            continue
        version, date_v, amel = cells[1], cells[2], cells[3]
        if len(amel) > 110:
            amel = amel[:110].rsplit(" ", 1)[0].rstrip(",;:") + "…"
        lignes.append("- **%s** (%s) — %s" % (version, date_v, amel or "(détail archivé)"))
    return lignes or None


def generer_pm_ephemere(skill_dir, out_dir):
    """Projection auto-portante du SKILL.md en PM éphémère MD.
    Retourne le chemin écrit (déterministe même jour). Aucune écriture hors out_dir."""
    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError("SKILL.md introuvable : %s" % skill_md)
    src = skill_md.read_text(encoding="utf-8")
    if MOTIF_SECTION0 not in src:
        raise ValueError("bloc §0 Contexte Système absent du SKILL.md — auto-portance "
                         "impossible (SHARED §6.2) ; skill inéligible")
    fm, body = parse_frontmatter(src)
    name = fm.get("name") or Path(skill_dir).name
    version = fm.get("version") or "0.0.0"
    description = fm.get("description") or ""
    sha = sha256_file(skill_md)
    today = date.today().isoformat()
    lignes = [
        "# PROMPT MAÎTRE ÉPHÉMÈRE — %s v%s" % (name, version),
        "",
        "> **Skill source** : `skills/%s/SKILL.md` (forme installée — référence canonique)" % name,
        "> **Version source** : %s · **Généré le** : %s" % (version, today),
        "> **SHA-256 source** : `%s`" % sha,
        "> **Nature** : projection éphémère auto-portante — le Contexte Système est embarqué,",
        "> **aucune lecture externe n'est requise** (SHARED §6.2). Régénérable à volonté :",
        "> `PM-skill(%s)` reproduit ce fichier à l'identique (déterminisme même jour)." % name,
        "",
        "## MODE D'EMPLOI — IA EXTERNE",
        "",
        "1. Copier l'intégralité du présent fichier.",
        "2. Le coller comme **prompt système** (ou premier message) dans l'IA de votre choix.",
        "3. Invoquer le skill par ses déclencheurs (section dédiée ci-dessous).",
        "   Le contenu ci-dessous est la spécification exécutable du skill, auto-contenue.",
        "",
        "## MISSION — description du skill (frontmatter source, verbatim)",
        "",
        description or "(description absente du frontmatter source — voir spécification ci-dessous)",
        "",
        "---",
        "",
        body.rstrip(),
        "",
        "---",
        "",
    ]
    if fm.get("dependencies"):
        lignes.append("## RELATIONS — dépendances déclarées (frontmatter source, verbatim)")
        lignes.append("")
        for d in fm["dependencies"]:
            lignes.append("- **%s** %s — %s" % (d["skill"], d["version"], d["used_at"] or "(usage non précisé)"))
        lignes.append("")
        lignes.append("> Ces dépendances sont des relations ÉCOSYSTÈME (traçabilité). En usage IA externe,")
        lignes.append("> la spécification embarquée ci-dessus suffit à l'exécution de la mission.")
        lignes.append("")
    hist = historique_condense(name)
    if hist:
        lignes.append("## HISTORIQUE CONDENSÉ — versions archivées (projection tronquée @historique)")
        lignes.append("")
        lignes.extend(hist)
        lignes.append("")
        lignes.append("> Historique complet archivé dans l'écosystème : `skills/@historique/historiques-par-skill/%s.md`" % name)
        lignes.append("> (R4 — le rôle d'archive des spécifications versionnées reste porté par le corpus")
        lignes.append("> `@mon-ecosysteme/` via KO-L004 ; le présent PM éphémère projette l'état courant).")
        lignes.append("")
    out = Path(out_dir) / ("PM-ephemere-%s-v%s.md" % (name, version))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lignes), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Commandes
# ---------------------------------------------------------------------------

def cmd_generate(skill, out_dir=None):
    if skill not in skills_racine():
        print("ERREUR : skill inconnu à la racine skills/ : %s (voir --list)" % skill)
        return 3
    out_dir = Path(out_dir) if out_dir else DOWNLOAD
    try:
        out = generer_pm_ephemere(SKILLS / skill, out_dir)
    except ValueError as e:
        print("INÉLIGIBLE : %s — %s" % (skill, e))
        return 3
    print("GÉNÉRÉ : %s (%d o) — auto-portant (§0 embarqué), SHA-256 source tracé" % (out, out.stat().st_size))
    print("Livraison : vue-upload push/featured (download/) ou share sur demande")
    return 0


def cmd_check(skill):
    if skill not in skills_racine():
        print("ERREUR : skill inconnu à la racine skills/ : %s (voir --list)" % skill)
        return 3
    skill_md = SKILLS / skill / "SKILL.md"
    src = skill_md.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(src)
    problems = []
    if not fm.get("name"):
        problems.append("frontmatter: name absent")
    if not fm.get("version"):
        problems.append("frontmatter: version absente")
    if MOTIF_SECTION0 not in src:
        problems.append("bloc §0 Contexte Système absent — auto-portance impossible (SHARED §6.2)")
    hist = historique_condense(skill)
    if problems:
        print("INÉLIGIBLE : %s — %s" % (skill, " ; ".join(problems)))
        return 3
    print("[ÉLIGIBLE] %s v%s — §0 embarqué (auto-portance) · relations ×%d · historique condensé : %s"
          % (fm.get("name") or skill, fm.get("version") or "?", len(fm.get("dependencies") or []),
             ("%d versions" % len(hist)) if hist else "aucun"))
    return 0


def cmd_list():
    eligibles, ineligibles = [], []
    for s in skills_racine():
        src = (SKILLS / s / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        (eligibles if MOTIF_SECTION0 in src else ineligibles).append(s)
    print("Skills racine éligibles PM éphémère : %d/%d" % (len(eligibles), len(eligibles) + len(ineligibles)))
    for s in eligibles:
        print("  %s" % s)
    if ineligibles:
        print("Inéligibles (§0 absent — auto-portance impossible) : %s" % ", ".join(ineligibles))
    return 0


# ---------------------------------------------------------------------------
# Self-test (conventions script-creator : critères mécaniques, tempdir, zéro
# écriture hors tempdir, verdict PASS/FAIL, rc 0/1)
# ---------------------------------------------------------------------------

def cmd_self_test():
    tmp = Path(tempfile.mkdtemp(prefix="pm-skill-selftest-"))
    n_pass, n_fail = 0, 0

    def st(tid, label, ok, detail=""):
        nonlocal n_pass, n_fail
        n_pass, n_fail = n_pass + (1 if ok else 0), n_fail + (0 if ok else 1)
        print("  [%s] ST%s %s%s" % ("PASS" if ok else "FAIL", tid, label, (" — " + detail) if detail else ""))

    try:
        racine = skills_racine()
        # ST1 — --list : les skills vivants sont bien détectés
        st(1, "--list détecte les skills racine (≥ 60, dont pm-skill)",
           len(racine) >= 60 and "pm-skill" in racine and "correct-work" in racine,
           "%d skills" % len(racine))
        # ST2 — éligibilité d'un skill famille
        ok2 = cmd_check_silencieux("correct-work")
        st(2, "--check correct-work ÉLIGIBLE (§0 présent)", ok2)
        # ST3 — refus mécanique d'un skill inconnu (rc=3, aligné generer-pm-skill.py)
        ok3 = cmd_generate("skill-inexistant-aucun-chance") == 3
        st(3, "refus mécanique skill inconnu (rc=3)", ok3)
        # ST4 — génération complète : toutes les sections requises
        out = generer_pm_ephemere(SKILLS / "correct-work", tmp)
        t = out.read_text(encoding="utf-8")
        requis = ["PROMPT MAÎTRE ÉPHÉMÈRE", "MODE D'EMPLOI — IA EXTERNE",
                  "MISSION — description du skill", MOTIF_SECTION0,
                  "SHA-256 source", "RELATIONS — dépendances déclarées"]
        manquantes = [m for m in requis if m not in t]
        st(4, "sections requises présentes (provenance/emploi/mission/§0/SHA/relations)",
           not manquantes, "manquantes : %s" % manquantes if manquantes else "6/6")
        # ST5 — auto-portance : aucune dépendance de lecture externe
        st(5, "auto-portance — zéro « lire en premier »",
           not re.search(r"lire en premier|lire PROMPT-MAITRE-SHARED", t))
        # ST6 — déterminisme ×2 byte-identique (idempotence)
        a = generer_pm_ephemere(SKILLS / "correct-work", tmp / "det1")
        b = generer_pm_ephemere(SKILLS / "correct-work", tmp / "det2")
        st(6, "déterminisme ×2 byte-identique (SHA-256)", sha256_file(a) == sha256_file(b))
        # ST7 — fidélité : version + mission verbatim du frontmatter source
        src = (SKILLS / "correct-work" / "SKILL.md").read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(src)
        t7 = re.sub(r"\s+", " ", t)
        phrase = re.sub(r"\s+", " ", fm["description"])[:70]
        st(7, "fidélité version + mission (description verbatim)",
           ("v%s" % fm["version"]) in t and (phrase in t7 if phrase else True))
        # ST8 — traçabilité SHA-256 exact
        st(8, "SHA-256 source embarqué exact", sha256_file(SKILLS / "correct-work" / "SKILL.md") in t)
        # ST9 — historique condensé : présent si @historique existe, absent proprement sinon
        h9 = historique_condense("correct-work")
        st9 = bool(h9) and any(l in t for l in h9) if h9 else ("HISTORIQUE CONDENSÉ" not in t)
        st(9, "historique condensé projeté (si présent au @historique)", st9,
           "%d versions" % len(h9) if h9 else "aucun historique → section omise")
        # ST10 — zéro écriture hors tempdir (garde d'état : download/ inchangé)
        avant = sorted(str(p) for p in DOWNLOAD.glob("PM-ephemere-*"))
        out11 = generer_pm_ephemere(SKILLS / "tsi-validator", tmp)
        st(11, "génération skill non-famille (tsi-validator)", out11.is_file())
        apres = sorted(str(p) for p in DOWNLOAD.glob("PM-ephemere-*"))
        st(10, "garde d'état — download/ inchangé par le self-test", avant == apres)
    except Exception as e:  # noqa: BLE001 — échec self-test = FAIL, jamais masqué
        st("X", "exception inattendue : %r" % e, False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELF-TEST : %d PASS · %d FAIL" % (n_pass, n_fail))
    return 0 if n_fail == 0 else 1


def cmd_check_silencieux(skill):
    src = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(src)
    return bool(fm.get("name") and fm.get("version") and MOTIF_SECTION0 in src)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--self-test" in argv:
        return cmd_self_test()
    if "--list" in argv:
        return cmd_list()
    if "--generate" in argv:
        i = argv.index("--generate")
        if i + 1 >= len(argv):
            print("Usage : --generate <skill> [--out <dir>]"); return 2
        out_dir = None
        if "--out" in argv:
            j = argv.index("--out")
            if j + 1 >= len(argv):
                print("Usage : --generate <skill> [--out <dir>]"); return 2
            out_dir = argv[j + 1]
        return cmd_generate(argv[i + 1], out_dir)
    if "--check" in argv:
        i = argv.index("--check")
        if i + 1 >= len(argv):
            print("Usage : --check <skill>"); return 2
        return cmd_check(argv[i + 1])
    print(__doc__.split("Usage :")[1].split("Codes retour")[0] if "Usage :" in __doc__ else "voir --help")
    print("Commandes : --generate <skill> [--out <dir>] · --check <skill> · --list · --self-test")
    return 2


if __name__ == "__main__":
    sys.exit(main())
