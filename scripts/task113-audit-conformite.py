#!/usr/bin/env python3
"""Task 113 — Audit de conformité de tous les skills et agents de l'écosystème.

Directive propriétaire trace 1a201e4bda5a2289 (session web-f492e049) :
« vérifie tous les skills et les agents contenus dans mon écosystème
(même s'ils n'ont pas été écrits par moi) » + réécriture agent-browser si non conforme.

Critères de conformité (norme skill-creator + conventions §0 SHARED v1.7.44) :
  S01 frontmatter YAML parseable
  S02 name kebab-case == nom du dossier
  S03 version semver présente
  S04 category présente
  S05 language: fr
  S06 tags présents
  S07 description française avec clause de déclenchement
  S08 read_when avec triptyque « Ne pas déclencher hors de ce périmètre (convention protocole, Task 28) »
  S09 bloc §0 Contexte Système (SHARED v…) présent
  S10 aucun emoji
  S11 aucune métadonnée de plateforme externe (clawdbot/allowed-tools/metadata:)
  S12 corps majoritairement français (heuristique stopwords)

Agents (.agent) :
  A01 en-tête §0 Contexte Système (SHARED v…)
  A02 bloc agent: avec nom, version, objectif
  A03 modes présents
  A04 gardes présents
  A05 règles présentes
  A06 aucun emoji
  A07 corps majoritairement français

Verdict par élément : CONFORME (0 défaillance) / NON_CONFORME (liste).
Sortie : JSON download/rapport-audit-conformite-task113.json + sortie console.
Idempotent (lecture seule), stdlib uniquement.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import os
import re
import sys
from pathlib import Path

SKILLS_ROOT = Path("/home/z/my-project/skills")
CORPUS_PREFIX = "@"
RAPPORT = Path("/home/z/my-project/download/rapport-audit-conformite-task113.json")

# Heuristique française : stopwords et marqueurs fréquents du français
FR_MARQUEURS = [
    "le", "la", "les", "des", "une", "un", "du", "et", "ou", "pour", "dans",
    "avec", "sur", "est", "sont", "quand", "si", "ne", "pas", "dès", "que",
    "qui", "au", "aux", "ce", "cette", "ces", "plus", "jamais", "toute",
    "toutes", "vers", "par", "comme", "être", "avoir", "faire", "lorsque",
    "utilisée", "utilisez", "déclencher", "demande", "écosystème",
]

# Emoji VRAIS uniquement : plans supplémentaires (U+1F000–U+1FAFF) + séquences
# variation-selector FE0F + étoile/cercle rouges U+2B50/U+2B55. Les flèches
# typographiques (U+2190–U+21FF), ✓/✗ et symboles mathématiques sont LÉGITIMES
# dans la prose française de l'écosystème (KO-L003 : jamais ajuster la réalité).
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF]"       # plans supplémentaires emoji
    "|[\u2600-\u27BF]\uFE0F"       # symboles avec variation selector (rendu emoji)
    "|[\u2B50\u2B55]"              # étoile / cercle rouges
    "|\uFE0F"                       # variation selector isolé
)

TRIPTYQUE = "Ne pas déclencher hors de ce périmètre"
SECTION0_RE = re.compile(r"§0\s*[—-]\s*Contexte Système\s*\(SHARED\s*v")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Exception documentée KO-L003 (Task 113) : la séquence « ⚙️ » de script-creator
# documente le FORMAT CANONIQUE d'injection de propagate-context.py (« # ⚙️ CONTEXTE
# SYSTÈME » présent dans 116 scripts) — référence technique verbatim, pas un ornement.
EXCEPTION_CANON = re.compile(r"#\s*⚙️\s*…")


def extraire_frontmatter(texte: str) -> tuple:
    """Rend (dict_frontmatter, corps) — parseur minimal sans dépendance."""
    if not texte.startswith("---"):
        return None, texte
    fin = texte.find("\n---", 3)
    if fin < 0:
        return None, texte
    fm_txt = texte[3:fin].strip()
    corps = texte[fin + 4:]
    fm = {}
    cle = None
    bloc = None  # clé courante en bloc scalaire plié/littéral (>/>-/|/|-)
    for ligne in fm_txt.splitlines():
        if not ligne.strip() or ligne.strip().startswith("#"):
            continue
        retrait = len(ligne) - len(ligne.lstrip())
        if retrait == 0:
            bloc = None
            if ":" in ligne:
                cle, _, val = ligne.partition(":")
                cle = cle.strip()
                val = val.strip()
                if val.startswith((">", "|")):
                    # bloc scalaire plié/littéral : les lignes indentées suivantes
                    # TOUTES appartiennent au texte (YAML) — jamais une seule
                    fm[cle] = ""
                    bloc = cle
                elif val == "":
                    # valeur vide : attend une liste de puces indentées
                    fm[cle] = []
                else:
                    fm[cle] = val.strip("'\"")
            continue
        # niveau indenté
        if bloc is not None:
            fm[bloc] = (fm[bloc] + " " + ligne.strip()).strip()
            continue
        if cle is not None and isinstance(fm.get(cle), list) and ligne.strip().startswith("-"):
            fm[cle].append(ligne.strip()[1:].strip())
            continue
        # sous-clé YAML (dependencies.skill etc.) — mémorisée sans structure fine
        if cle == "dependencies" and ":" in ligne:
            fm.setdefault("dependencies_cles", []).append(ligne.strip().rstrip(":"))
    return fm, corps


def ratio_francais(corps: str) -> float:
    mots = re.findall(r"[a-zA-ZàâäéèêëïîôöùûüçÀÉÈÊ]+", corps.lower())
    if not mots:
        return 0.0
    hits = sum(1 for m in mots[:400] if m in FR_MARQUEURS)
    echantillon = max(1, min(len(mots), 400))
    return hits / echantillon


def auditer_skill(dossier: Path) -> dict:
    nom = dossier.name
    fail = []
    chemin = dossier / "SKILL.md"
    if not chemin.exists():
        return {"element": nom, "type": "skill", "verdict": "ABSENT", "defaillances": ["SKILL.md manquant"]}
    texte = chemin.read_text(encoding="utf-8")
    fm, corps = extraire_frontmatter(texte)

    if fm is None:
        return {"element": nom, "type": "skill", "verdict": "NON_CONFORME",
                "defaillances": ["S01 frontmatter YAML absent ou non parseable"]}

    name = str(fm.get("name", ""))
    version = str(fm.get("version", ""))
    category = str(fm.get("category", ""))
    language = str(fm.get("language", ""))
    tags = fm.get("tags")
    description = str(fm.get("description", "") or "")
    read_when = fm.get("read_when") or []

    if not KEBAB_RE.match(name) or name != nom:
        fail.append(f"S02 name « {name} » ≠ kebab-case du dossier « {nom} »")
    if not SEMVER_RE.match(version):
        fail.append(f"S03 version absente ou non-semver (« {version or '—'} »)")
    if not category:
        fail.append("S04 category absente")
    if language != "fr":
        fail.append(f"S05 language « {language or '—'} » ≠ fr")
    if not tags or (isinstance(tags, list) and len(tags) == 0):
        fail.append("S06 tags absents")
    desc_fr = ratio_francais(description) > 0.10 or any(
        m in description.lower() for m in ["utiliser quand", "déclencher", "skill", "l'utilisateur"]
    )
    if not description:
        fail.append("S07 description absente")
    elif not desc_fr:
        fail.append("S07 description non française / sans clause de déclenchement")
    if not read_when:
        fail.append("S08 read_when absent")
    elif not any(TRIPTYQUE in str(b) for b in read_when):
        fail.append("S08 read_when sans triptyque « " + TRIPTYQUE + "… (convention protocole, Task 28) »")
    if not SECTION0_RE.search(corps[:3000]) and not SECTION0_RE.search(texte):
        fail.append("S09 bloc §0 Contexte Système (SHARED v…) absent")
    emoji_hits = [e for e in EMOJI_RE.findall(texte) if not EXCEPTION_CANON.search(texte)]
    if emoji_hits:
        fail.append(f"S10 emoji présent ×{len(emoji_hits)}")
    ext = []
    if "clawdbot" in texte[:1500]:
        ext.append("metadata clawdbot")
    if "allowed-tools" in texte[:1500]:
        ext.append("allowed-tools")
    if fm.get("metadata"):
        ext.append("champ metadata")
    if ext:
        fail.append("S11 métadonnées plateforme externe : " + ", ".join(ext))
    r = ratio_francais(corps[:6000])
    if r < 0.05:
        fail.append(f"S12 corps non français (ratio marqueurs {r:.3f} < 0.05)")

    return {"element": nom, "type": "skill", "version": version or None,
            "verdict": "CONFORME" if not fail else "NON_CONFORME",
            "defaillances": fail, "corps_fr_ratio": round(r, 3)}


def auditer_agent(chemin: Path) -> dict:
    nom = chemin.stem
    fail = []
    texte = chemin.read_text(encoding="utf-8")
    if not SECTION0_RE.search(texte[:2500]):
        fail.append("A01 en-tête §0 Contexte Système (SHARED v…) absent")
    bloc_agent = re.search(r"^agent:\s*$", texte, re.M)
    if not bloc_agent:
        fail.append("A02 bloc « agent: » absent")
    else:
        for champ in ("nom:", "version:", "objectif:"):
            if not re.search(r"^\s{2}" + re.escape(champ), texte[bloc_agent.start():], re.M):
                fail.append(f"A02 champ « {champ[:-1]} » absent du bloc agent")
    for crit, nomc in ((r"^\s{2}modes:", "A03"), (r"^\s{2}gardes:", "A04"), (r"^\s{2}regles:", "A05")):
        if not re.search(crit, texte, re.M):
            fail.append(f"{nomc} section « {crit.strip('^\\s{}:')} » absente")
    emoji_hits = EMOJI_RE.findall(texte)
    if emoji_hits:
        fail.append(f"A06 emoji présent ×{len(emoji_hits)}")
    r = ratio_francais(texte[:6000])
    if r < 0.05:
        fail.append(f"A07 corps non français (ratio {r:.3f})")
    return {"element": nom, "type": "agent", "fichier": str(chemin.relative_to(SKILLS_ROOT)),
            "verdict": "CONFORME" if not fail else "NON_CONFORME",
            "defaillances": fail, "corps_fr_ratio": round(r, 3)}


def main() -> int:
    resultats = {"skills": [], "agents": []}
    for dossier in sorted(SKILLS_ROOT.iterdir()):
        if not dossier.is_dir() or dossier.name.startswith(CORPUS_PREFIX):
            continue
        if (dossier / "SKILL.md").exists():
            resultats["skills"].append(auditer_skill(dossier))
    for chemin in sorted(SKILLS_ROOT.glob("*/*.agent")):
        resultats["agents"].append(auditer_agent(chemin))

    ns = len(resultats["skills"])
    nc = len(resultats["agents"])
    conformes_s = sum(1 for x in resultats["skills"] if x["verdict"] == "CONFORME")
    conformes_a = sum(1 for x in resultats["agents"] if x["verdict"] == "CONFORME")
    synthese = {
        "skills_total": ns, "skills_conformes": conformes_s, "skills_non_conformes": ns - conformes_s,
        "agents_total": nc, "agents_conformes": conformes_a, "agents_non_conformes": nc - conformes_a,
    }
    rapport = {"tache": "Task 113 audit conformité skills+agents",
               "norme": "skill-creator + §0 SHARED v1.7.44 + read_when triptyque (Task 28)",
               "synthese": synthese, "resultats": resultats}
    RAPPORT.parent.mkdir(parents=True, exist_ok=True)
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"SKILLS  : {conformes_s}/{ns} CONFORMES — {ns - conformes_s} NON_CONFORMES")
    for x in resultats["skills"]:
        if x["verdict"] != "CONFORME":
            print(f"  ✗ {x['element']} : " + " | ".join(x["defaillances"]))
    print(f"AGENTS  : {conformes_a}/{nc} CONFORMES — {nc - conformes_a} NON_CONFORMES")
    for x in resultats["agents"]:
        if x["verdict"] != "CONFORME":
            print(f"  ✗ {x['element']} : " + " | ".join(x["defaillances"]))
    print(f"RAPPORT : {RAPPORT}")
    return 0


SELFTESTS = [
    ("semver", SEMVER_RE.match("1.2.4") is not None),
    ("semver_ko", SEMVER_RE.match("abc") is None),
    ("kebab", KEBAB_RE.match("agent-browser") is not None),
    ("kebab_ko", KEBAB_RE.match("Agent Browser") is None),
    ("emoji_detect", EMOJI_RE.search("🌐 test") is not None),
    ("fleche_legitime", EMOJI_RE.search("P1→P2 ↔ transmission 3.10.0→3.46.0") is None),
    ("check_legitime", EMOJI_RE.search("PASS ✓ / FAIL ✗") is None),
    ("triptyque", TRIPTYQUE in "Ne pas déclencher hors de ce périmètre (convention protocole, Task 28)."),
]


def selftest() -> int:
    ok = 0
    for nom, res in SELFTESTS:
        print(("PASS" if res else "FAIL") + " " + nom)
        ok += 1 if res else 0
    total = len(SELFTESTS)
    print(f"SELFTEST {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
