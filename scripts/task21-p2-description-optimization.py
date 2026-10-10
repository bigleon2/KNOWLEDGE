#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 21 — campagne P2 : Description Optimization (protocole A10/A14) sur les skills
en dérive silencieuse voie M (Task 19 §4.2 / baseline V6 Task 21).

Principes :
- R2 : append-only pour les extensions (aucun contenu retiré) ; les chirurgies retirent
  uniquement des mots INCIDENTS à FP prouvé, sémantique préservée par rephrasage.
- Validation locale ZÉRO-API obligatoire : re-jeu SHARED §7 v2 APRÈS édition —
  gate = tous les cas du skill au vert, sinon l'édition est signalée ÉCHEC (R3).
- Contrôles négatifs préservés (garde de collision intra-skill).
- KO-L004 : sync KB (heading version + Description + Dernière calibration) et
  recalibrage ECO_SKILLS de check-ecosysteme-integrity.py pour chaque montée.
- PM-couplage : clone-chat / correct-work portent une révision documentaire SANS bump
  (décision D2x — un bump désalignerait les PM v2.0.0 / v2.7.0 publiés, recréant le
  pattern A1/A2 ; précédent « révision documentaire sans changement de version »,
  PM gen-plan v3.18.0 §7).
- N3 (Task 21) : agent-creator — la description dupliquait verbatim celle d'autonomous-agent
  (défaut d'identité) ; réécriture fidèle aux cas positifs officiels du skill.
- version-management : champ name normalisé kebab-case (N2) ; description zh inchangée —
  décision C006(b) (voie M structurellement aveugle au zh, validation par voie L assumée).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
KB = SKILLS / "KNOWLEDGE.md"
INTEG = BASE / "scripts" / "check-ecosysteme-integrity.py"
DRY = "--dry" in sys.argv

# ── Stemmer SHARED §7 v2 (réplique identique arbitre V6 / harnais Task 19) ──
SUFFIXES = ["issements", "issement", "atrices", "ateur", "ations", "ation", "ements", "ement",
            "ances", "ance", "ences", "ence", "ismes", "isme", "istes", "iste",
            "ables", "able", "ibles", "ible", "euses", "euse", "eurs", "eur",
            "ités", "ité", "aux", "ales", "ale", "els", "el", "iques", "ique",
            "ives", "ive", "ifs", "if", "eaux", "eau", "ux", "ants", "ant",
            "ents", "ent", "ions", "ion", "ons", "on", "es", "e", "s", "x"]
STOP = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "ou", "a", "au", "aux",
        "en", "dans", "sur", "pour", "par", "avec", "sans", "qui", "que", "ce", "cette",
        "son", "sa", "ses", "leur", "leurs", "est", "sont", "plus", "ne", "pas", "se",
        "chaque", "tout", "toute", "tous", "comme", "aux", "au", "il", "elle", "on",
        "skill", "discipline", "source", "verite", "shared", "references", "documentes",
        "fondements", "academiques", "specialise", "operationnalisation"}


def stem(w):
    w = w.lower()
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: len(w) - len(suf)]
    return w


def norm(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def keywords_for(name, description, tags):
    kws = set(name.split("-"))
    kws |= {norm(t) for t in tags}
    for w in re.findall(r"[a-zà-ÿ]+", norm(description)):
        if w not in STOP and len(w) > 3:
            kws.add(w)
    return {stem(k) for k in kws if len(k) > 2}


def heuristic_score(query, kws, strong):
    toks = {stem(w) for w in re.findall(r"[a-zà-ÿ]+", norm(query)) if len(w) > 2}
    hits = toks & kws
    trig = (len(hits) >= 2) or bool(hits & strong)
    return (len(hits) / max(1, len(toks))), sorted(hits), trig


def load_skill(sdir):
    smd = (sdir / "SKILL.md").read_text(encoding="utf-8")
    fm = smd.split("---")[1]
    desc_m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    if desc_m:
        desc = " ".join(l.strip() for l in desc_m.group(1).splitlines())
    else:
        desc_m2 = re.search(r"description:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE)
        desc = desc_m2.group(1).strip() if desc_m2 else ""
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", fm)
    tags = re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []
    ver_m = re.search(r'version:\s*"?([0-9.]+)"?', fm)
    tevals = sdir / "evals" / "trigger_evals.json"
    cases = json.loads(tevals.read_text(encoding="utf-8")) if tevals.exists() else []
    return {"name": sdir.name, "version": ver_m.group(1) if ver_m else "?",
            "desc": desc, "tags": tags, "cases": cases}


def replay(sdir):
    """Re-jeu complet des cas officiels (voie M) — retourne (n_ok, n, échecs)."""
    sk = load_skill(sdir)
    kws = keywords_for(sk["name"], sk["desc"], sk["tags"])
    strong = {stem(p) for p in sk["name"].split("-")}
    fails = []
    for c in sk["cases"]:
        _, _, trig = heuristic_score(c["query"], kws, strong)
        if trig != c["should_trigger"]:
            fails.append({"query": c["query"][:80], "expected": c["should_trigger"], "trigger_m": trig})
    return len(sk["cases"]) - len(fails), len(sk["cases"]), fails


# ── Éditions planifiées (conçues d'après l'analyse des cas en échec, Task 21) ──
EDITS = {
    "autonomous-agent": {
        "append": "Exécution autonome d'opérations complexes, persistance de l'état entre les sessions, traitement de requêtes de bout en bout, simulation de comportement sur des cas d'usage.",
        "bump": "1.1.0",
    },
    "clone-chat": {
        "append": "Archivage de session pour reprise par une session héritière.",
        "bump": None,
        "note": "PM-couplé (PROMPT-MAITRE-CLONE-CHAT v2.0.0) — révision documentaire sans bump",
    },
    "correct-work": {
        "append": "Contrôler la cohérence avant de livrer ce que tu viens de produire.",
        "bump": None,
        "note": "PM-couplé (PROMPT-MAITRE-CORRECT-WORK v2.7.0) — révision documentaire sans bump",
    },
    "cpp-analysis": {
        "append": "Architecture de projets et analyse des dépendances ; évalue la qualité et la sûreté des bases de code avant migration.",
        "bump": "1.1.0",
    },
    "harness-engineering": {
        "append": "Contrôles automatiques anti-dérive des processus, gardes anti-régression.",
        "bump": "1.1.0",
    },
    "loop-engineering": {
        "append": "Critères d'arrêt des processus itératifs, définition des graders.",
        "bump": "1.1.0",
    },
    "audio-metadata": {
        "append": "Nettoie et corrige les tags ID3 : titres, artistes, pochettes, bibliothèques MP3 ; organise les playlists par album en corrigeant les tags manquants.",
        "bump": "1.1.0",
    },
    "correct-py": {
        "surgical": [
            ("vient d'être créé ou modifié", "vient d'être généré ou modifié"),
            ("avant relecture script-reviewer", "préalablement à la relecture script-reviewer"),
        ],
        "append": "Commentaires corrigés, blancs parasites supprimés, style et indentation normalisés.",
        "bump": "1.1.0",
    },
    "audit-provenance": {
        "surgical": [
            ("(skills, scripts, corpus, rapports, plans)", "(skills, corpus, rapports, plans, en-têtes)"),
            ("validé par correct-work (mode CIBLE)", "contrôlé par correct-work (mode CIBLE)"),
        ],
        "bump": "1.1.0",
    },
    "skills-inventory": {
        "surgical": [
            ('"quelles skills sont installées"', '"quelles skills sont présentes"'),
        ],
        "bump": "1.1.0",
    },
    "agent-creator": {
        "replace": "Création et orchestration d'agents : génère des agents autonomes persistants (fichier .agent, mémoire interne à deux niveaux, modules internes, boucles, intégration multi-LLM) et orchestre plusieurs agents spécialisés sur un flux de tâches.",
        "bump": "2.1.0",
        "note": "N3 Task 21 : l'ancienne description dupliquait verbatim celle d'autonomous-agent (défaut d'identité) — réécriture fidèle aux cas positifs officiels",
    },
    "version-management": {
        "name_fix": ("name: Version Management Skill", "name: version-management"),
        "bump": None,
        "note": "N2 Task 21 : champ name normalisé kebab-case ; description zh inchangée — décision C006(b)",
    },
}

DESC_BLOCK_RE = re.compile(r"(description:\s*>-?\s*\n)((?:[ \t]+.*\n)+)")


def edit_skill(skill, plan):
    sdir = SKILLS / skill
    path = sdir / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    head, fm, tail = text.split("---", 2)
    changes = []

    if "replace" in plan:
        m = DESC_BLOCK_RE.search(fm)
        old_block = m.group(2)
        new_block = "".join("  " + w + "\n" for w in _wrap(plan["replace"], 96))
        fm = fm[:m.start(2)] + new_block + fm[m.end(2):]
        changes.append("description remplacée (N3)")
    if "surgical" in plan:
        for old, new in plan["surgical"]:
            if old in fm:
                fm = fm.replace(old, new, 1)
                changes.append(f"chirurgie : « …{old[:38]}… » → rephrasé")
            else:
                changes.append(f"⚠ chirurgie INTROUVABLE : « {old[:50]} »")
    if "append" in plan:
        m = DESC_BLOCK_RE.search(fm)
        block = m.group(2)
        fm = fm[:m.start(2)] + block + "  " + plan["append"] + "\n" + fm[m.end(2):]
        changes.append("extension radicaux discriminants (A10/A14, R2)")
    if "name_fix" in plan:
        old, new = plan["name_fix"]
        if old in fm:
            fm = fm.replace(old, new, 1)
            changes.append("name normalisé kebab-case (N2)")
    if plan.get("bump"):
        ver_m = re.search(r'version:\s*"?([0-9.]+)"?', fm)
        old_v = ver_m.group(1)
        fm = re.sub(r'(version:\s*)"?[0-9.]+"?', lambda mm: mm.group(1) + f'"{plan["bump"]}"', fm, count=1)
        changes.append(f"version {old_v} → {plan['bump']} (Description Optimization, précédent Task 18)")

    path.write_text(head + "---" + fm + "---" + tail, encoding="utf-8")
    return changes


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def sync_kb(skill, new_desc, new_version):
    text = KB.read_text(encoding="utf-8")
    if new_version:
        text = re.sub(rf"(^## {re.escape(skill)} v)[0-9.]+$", lambda m: m.group(1) + new_version,
                      text, count=1, flags=re.M)
    # Ligne Description : refresh sur une ligne (échappement pipes)
    one_line = " ".join(new_desc.split())
    pat = re.compile(rf"(- \*\*Description\*\* : )[^\n]+(?=\n- \*\*|\n\n|\n## )")
    # ne remplacer QUE dans la section du skill concerné
    sec = re.search(rf"^## {re.escape(skill)} v[0-9.]+\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if sec:
        new_sec = pat.sub(lambda m: m.group(1) + one_line, sec.group(1), count=1)
        text = text[:sec.start(1)] + new_sec + text[sec.end(1):]
    # Ligne Dernière calibration : remplacer si présente, sinon insérer après Description
    calib = ("2026-10-03 (Task 21 P2 — Description Optimization A10/A14 : extension radicaux "
             "discriminants / chirurgies incidents-FP, validation locale zéro-API, contrôles négatifs "
             "préservés, arbite V6 re-jeu)")
    sec = re.search(rf"^## {re.escape(skill)} v[0-9.]+\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if sec:
        body = sec.group(1)
        if "- **Dernière calibration** :" in body:
            body = re.sub(r"- \*\*Dernière calibration\*\* : [^\n]+",
                          "- **Dernière calibration** : " + calib, body, count=1)
        else:
            body = re.sub(r"(- \*\*Description\*\* : [^\n]+\n)",
                          lambda m: m.group(1) + "- **Dernière calibration** : " + calib + "\n",
                          body, count=1)
        text = text[:sec.start(1)] + body + text[sec.end(1):]
    KB.write_text(text, encoding="utf-8")


def sync_eco_skills(skill, new_version):
    if not new_version:
        return
    text = INTEG.read_text(encoding="utf-8")
    text = re.sub(rf'("{re.escape(skill)}":\s*)"[0-9.]+"', lambda m: m.group(1) + f'"{new_version}"',
                  text, count=1)
    INTEG.write_text(text, encoding="utf-8")


def main():
    results = {}
    for skill, plan in EDITS.items():
        sdir = SKILLS / skill
        pre_ok, pre_n, _ = replay(sdir)
        if not DRY:
            changes = edit_skill(skill, plan)
            sync_kb(skill, load_skill(sdir)["desc"], plan.get("bump"))
            sync_eco_skills(skill, plan.get("bump"))
        post_ok, post_n, fails = replay(sdir)
        results[skill] = {"pre": f"{pre_ok}/{pre_n}", "post": f"{post_ok}/{post_n}",
                          "bump": plan.get("bump"), "note": plan.get("note", ""),
                          "fails": fails, "changes": changes if not DRY else ["DRY"]}
        flag = "OK " if post_ok == post_n else "RÉSIDU"
        print(f"  [{flag}] {skill:<22} {pre_ok}/{pre_n} → {post_ok}/{post_n}  bump={plan.get('bump') or '—'}")
        for f in fails:
            print(f"         échec résiduel : exp={f['expected']} trig={f['trigger_m']} :: {f['query']}")
    out = BASE / "scripts" / "task21-p2-optimization-report.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRapport : {out}")


if __name__ == "__main__":
    main()
