#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""
"""gen-ultra-maitre.py — Générateur idempotent du PROMPT-ULTRA-MAITRE-ORCHESTRATION.md

Directive propriétaire 2026-10-02 (« prompt ultra maître ») : au lieu de convertir
les prompts maîtres existants en monolithes enrichis (rejeté — R4 duplication, R2
corpus figé, KO-L004 drift), ce script GÉNÈRE un ultra-PM orchestrateur LÉGER dont
tout le contenu est DÉRIVÉ dynamiquement de l'état réel (KO-L003) :
  - listing réel du corpus skills/@mon-ecosysteme/ (PMs par famille, plus récent)
  - versions réelles des skills écosystème (frontmatter SKILL.md = source de vérité)
  - version de l'installateur unique PM-INSTALL et du socle SHARED
Le régénérer après chaque évolution du corpus EST le recalibrage (KO-L004).

Idempotence : même état du corpus -> bytes identiques (rejeu ×2 sans effet).
Usage :
    python3 scripts/gen-ultra-maitre.py            # génère + vérifie
    python3 scripts/gen-ultra-maitre.py --check    # vérifie sans écrire
"""
import os
import re
import sys
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE_DIR, "skills", "@mon-ecosysteme")
SKILLS = os.path.join(BASE_DIR, "skills")
KB = os.path.join(SKILLS, "KNOWLEDGE.md")
OUT = os.path.join(CORPUS, "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md")

ECO_SKILLS = ["gen-plan", "correct-work", "clone-chat", "skills-inventory",
              "skill-creator", "agent-creator", "script-creator",
              "script-reviewer", "audit-provenance", "prompt-engineering",
              "context-engineering", "loop-engineering", "graph-engineering",
              "harness-engineering", "knowledge-observer",
              "script-mon-ecosysteme-infrastructure",
              "audio-metadata", "cpp-analysis", "pdf-llm",
              "resource-monitor", "version-management"]

ROUTING = [
    ("Planifier une tâche / un projet", "gen-plan (dernière version)", "PM gen-plan le plus récent", "E1-E15, 4 modes"),
    ("Vérifier / corriger un travail", "correct-work v2.7.0 (gen-plan OBLIGATOIRE à l'Étape 1)", "PM correct-work le plus récent", "5 étapes, 4 modes"),
    ("Archiver une session / clone", "clone-chat", "PM clone-chat v2.0.0", "7+1 étapes, 8 checks"),
    ("Installer / réinstaller l'écosystème", "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md — SOURCE UNIQUE", "ce fichier (§A + pipeline 10 étapes)", "corpus -> registre -> arbitres"),
    ("Synchroniser contexte / canaux", "SYNC-CONTEXT.md + scripts de sync", "—", "2 voies byte-identiques"),
    ("Auditer la provenance", "audit-provenance", "—", "L006, avant clone/install"),
    ("Observer les leçons", "knowledge-observer", "—", "journal lessons-learned, M1-M2 à E15"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def frontmatter_version(skill):
    p = os.path.join(SKILLS, skill, "SKILL.md")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        m = re.search(r"^version:\s*[\"']?([\d.]+)", f.read(), re.MULTILINE)
    return m.group(1) if m else None


def corpus_state():
    files = sorted(f for f in os.listdir(CORPUS)
                   if os.path.isfile(os.path.join(CORPUS, f)))
    families = {"GEN-PLAN": [], "CORRECT-WORK": [], "CLONE-CHAT": []}
    for f in files:
        m = re.match(r"PROMPT-MAITRE-(GEN-PLAN|CORRECT-WORK|CLONE-CHAT)-v([\d.]+)\.md$", f)
        if m:
            families[m.group(1)].append((f, m.group(2)))
    for k in families:
        families[k].sort(key=lambda t: [int(x) for x in t[1].split(".")])
    install_v = shared_v = "?"
    with open(os.path.join(CORPUS, "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"), encoding="utf-8") as f:
        install_v = re.search(r"^Version : ([\d.]+)", f.read(), re.MULTILINE).group(1)
    with open(os.path.join(CORPUS, "PROMPT-MAITRE-SHARED.md"), encoding="utf-8") as f:
        shared_v = re.search(r"\*\*Version\*\* : ([\d.]+)", f.read()).group(1)
    return files, families, install_v, shared_v


def build():
    files, families, install_v, shared_v = corpus_state()
    files = [f for f in files if f != "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"]  # exclusion auto-référentielle (idempotence)
    versions = [(s, frontmatter_version(s)) for s in ECO_SKILLS]
    kb_entries = 0
    if os.path.isfile(KB):
        with open(KB, encoding="utf-8") as f:
            kb_entries = len(re.findall(r"^## ([\w-]+) v([\d.]+)", f.read(), re.MULTILINE))

    rows_pm = "\n".join(
        f"| {fam} | {lst[-1][0]} (la plus récente) | {', '.join(v for _, v in lst[:-1]) or '—'} |"
        for fam, lst in families.items() if lst)
    rows_skills = "\n".join(f"| `{s}` | {v} |" for s, v in versions)
    rows_routing = "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in ROUTING)

    md = f"""# PROMPT ULTRA MAÎTRE — Orchestration de l'écosystème personnel

> **Version** : 1.0.0 (généré)
> **Généré par** : `scripts/gen-ultra-maitre.py` (idempotent — ne pas éditer à la main ; éditer le script puis régénérer)
> **Date de génération** : 2026-10-02
> **Rôle** : point d'entrée UNIQUE d'orchestration à l'usage — route chaque demande vers le bon prompt maître / skill, sans dupliquer leur contenu (R4)
> **Directive** : propriétaire 2026-10-02 (« prompt ultra maître ») — design retenu : orchestrateur léger dérivé dynamiquement du corpus (KO-L003), PAS de conversion des PMs existants en monolithes (R4 duplication / R2 corpus figé / KO-L004 drift)

---

## §0 — Règle Zéro et invariants vitaux

- Écosystème Knowledge : `{{{{SKILLS_ROOT}}}}`=skills/ | `{{{{KB_PATH}}}}`=skills/KNOWLEDGE.md | `{{{{KB_ENABLED}}}}`=true | `{{{{PROFILE_DEFAULT}}}}`=NORMAL
- **Règle Zéro (SHARED §0)** : skills auto-contenus, versionnés semver, registre KB source de vérité, cross-references bidirectionnelles.
- **Idempotence (R1-R6)** : vérifier présence avant insertion ; ne jamais rétrograder ; fusionner les frontmatters ; ne jamais dupliquer ; journaliser ; auto-adaptation sans duplication.
- **Arbitres dynamisés (KO-L003)** : tout invariant dérive de l'état courant — jamais d'état figé ; re-verdict honnête après correction.
- **Recalibrage croisé (KO-L004)** : toute montée de version recalibre arbitres, miroirs-canaux, SYNC_MAP et CET orchestrateur (régénération = recalibrage).

## §1 — Routage demande → prompt maître / skill (table T1)

| Demande | Skill mobilisé | Prompt maître | Cadre |
|---------|----------------|---------------|-------|
{rows_routing}

## §2 — Registre dynamique des prompts maîtres (dérivé du corpus réel)

État réel de `skills/@mon-ecosysteme/` : **{len(files)} fichiers canoniques + cet orchestrateur** (invariant `CORPUS_ATTENDU` du checker).

| Famille | PM le plus récent (source d'assemblage) | Versions historiques figées (R2) |
|---------|------------------------------------------|----------------------------------|
{rows_pm}

Socle : `PROMPT-MAITRE-SHARED.md` v{shared_v} (lire en premier). Installateur : `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` v{install_v} — **source d'installation UNIQUE** (fusion v1.1.0 : `INSTALL-ECOSYSTEME.md` supprimé, miroir `skills/_prompts-maitres/` supprimé, décision d'architecture v2.0 exécutée).

## §3 — Skills écosystème installés (versions réelles, frontmatter = source de vérité)

| Skill | Version |
|-------|---------|
{rows_skills}

Registre KB : {kb_entries} entrées versionnées (`skills/KNOWLEDGE.md`). correct-work v2.7.0 exige gen-plan (dernière version installée) à son Étape 1 — couplage obligatoire.

## §4 — Points d'entrée et ordre de lecture

1. **Socle** : `PROMPT-MAITRE-SHARED.md` (v{shared_v}) — toujours en premier.
2. **Installation** : `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` (v{install_v}) — périmètre §A + pipeline 10 étapes + critères §3.
3. **Planification** : PM gen-plan le plus récent — §A DÉCLENCHEURS (dont verbatim « intègre dans le plan d'actions » → E13).
4. **Vérification** : PM correct-work le plus récent + `skills/correct-work/scripts/verify-correct-work.py` (16 checks).
5. **Publication** : `scripts/sync-download.py --sync` + archive `download/mon-ecosysteme_archive.zip` (round-trip v2.1).

## §5 — Interactions clés (extrait graphe KB)

| Arête | Nature |
|-------|--------|
| gen-plan —invoque→ correct-work | E1 + hook E8 + contrôle par phase E9-E14 |
| correct-work —utilise→ gen-plan | Étape 1 OBLIGATOIRE (dernière version) |
| gen-plan —délègue→ prompt-engineering | optimisation fine des prompts (SHARED §3.1) |
| clone-chat —enrichit→ KNOWLEDGE.md | descriptions §2 |
| knowledge-observer —valide→ gen-plan | leçons §1.14/§1.15 (M1-M2 à E15) |
| install-ecosysteme —précondition→ audit-provenance | audit avant installation (L006) |

## §6 — Maintenance

- Toute évolution du corpus/skills : `python3 scripts/gen-ultra-maitre.py` PUIS recalibrage KO-L004 (checker, SYNC_MAP, archive) — la régénération de ce fichier fait partie du recalibrage.
- Ce fichier NE remplace AUCUN prompt maître : il ROUTE. Il ne détient ni méthode ni spécification (fonction héritée SHARED §7).
- Recréer un second installateur ou un second orchestrateur est interdit (R4).
"""
    return md


def main():
    md = build()
    check_only = "--check" in sys.argv
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            current = f.read()
        if current == md:
            print(f"Idempotence : {os.path.basename(OUT)} déjà à jour (SHA {sha256(OUT)[:12]}…) — no-op.")
            return 0
    if check_only:
        print("DÉRIVE : le fichier généré diffère de l'état courant du corpus — régénération requise.")
        return 1
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Généré : {OUT} ({len(md.splitlines())} lignes, SHA {sha256(OUT)[:12]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
