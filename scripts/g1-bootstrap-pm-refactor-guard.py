#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 9 / G-RES-1 — Bootstrap du PM canonique refactor-guard v1.7.0 (décision D009).

Décision propriétaire D009 (directive gen-plan(step) 2026-10-12, session
web-b4d7dd19) : les PMs de la lignée externe refactor-guard (v1.3.0 -> v1.6.0,
discussion 468a4c26) sont ACCEPTÉS non portés (non verbatim — provenance R4) ;
le corpus démarre le PM refactor-guard à v1.7.0 = version convergée du canonique.

Mécanique (KO-L003 — le script n'invente jamais de contenu) :
  - sections portées VERBATIM depuis skills/refactor-guard/SKILL.md (§0, §1, §2,
    §3, §4) + frontmatter YAML (exemplaire §4 du PM) ;
  - structure alignée sur les ancres `scripts/generer-pm-skill.py` (famille n°4) :
    titre « — Installation du skill refactor-guard v1.7.0 », « Skill cible »,
    « Version du prompt », « Date », YAML `version: 1.7.0`, ancre historique
    « | v1.7.0 | » ;
  - §5/§6 (installation/vérification) = gabarit standard écosystème, documenté
    comme scaffolding de bootstrap au §7 (provenance) ;
  - idempotent : si le PM existe et est byte-identique -> NO-OP ; s'il existe et
    diverge -> ABANDON sans écriture (R2 — jamais écraser).

Sortie : skills/@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md
Code retour : 0 = écrit ou no-op ; 2 = ABANDON.
"""

import os
import sys
import hashlib
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(BASE, "skills", "refactor-guard", "SKILL.md")
OUT = os.path.join(BASE, "skills", "@mon-ecosysteme",
                   "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md")
TODAY = date.today().isoformat()


def abandon(msg, code=2):
    print("ABANDON : %s" % msg)
    sys.exit(code)


def read(path):
    if not os.path.isfile(path):
        abandon("fichier introuvable : %s" % path)
    with open(path, encoding="utf-8") as f:
        return f.read()


def slice_between(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j].rstrip() + "\n"


def main():
    skill = read(SKILL)

    # — Frontmatter YAML (verbatim) —
    parts = skill.split("---", 2)
    if len(parts) < 3:
        abandon("frontmatter introuvable dans SKILL.md")
    frontmatter = "---" + parts[1] + "---"
    if "version: 1.7.0" not in frontmatter:
        abandon("ancre YAML `version: 1.7.0` absente du frontmatter")

    # — Description (frontmatter, reflow) —
    desc_lines = []
    in_desc = False
    for line in parts[1].splitlines():
        if line.startswith("description:"):
            in_desc = True
            rest = line[len("description:"):].strip()
            if rest and rest != ">":
                desc_lines.append(rest)
            continue
        if in_desc:
            if line.startswith("  ") or line == "":
                if line.strip():
                    desc_lines.append(line.strip())
                continue
            break
    description = " ".join(desc_lines)

    # — Sections verbatim —
    s0 = slice_between(skill, "## §0 — Contexte Système", "\n## §1 —")
    s1 = slice_between(skill, "## §1 — Spécification fonctionnelle", "\n---\n\n## §2 —")
    s2 = slice_between(skill, "## §2 — Spécification technique", "\n---\n\n## §3 —")
    s3 = slice_between(skill, "## §3 — Relations", "\n---\n\n## §4 —")
    s4 = slice_between(skill, "## §4 — Conventions", "\n## §5 —")
    if "version: 1.7.0" not in frontmatter:
        abandon("YAML exemplaire incomplet")

    pm = f"""# PROMPT MAÎTRE — Installation du skill refactor-guard v1.7.0

> **Version du prompt** : 1.0.0
> **Révision prompt** : {TODAY} — 1.0.0 : bootstrap initial (décision propriétaire D009 — PMs de la lignée externe ACCEPTÉS non portés)
> **Skill cible** : refactor-guard v1.7.0
> **Date** : {TODAY}
> **Source** : Écosystème Knowledge — Refactor-guard (garde-fous de refactoring, complément triangulaire de la discipline n°55)
> **Dépend** : `CONTEXTE SYSTÈME` (embarqué ci-dessous)

---
{s0}
---

## §A — DÉCLENCHEURS

- `refactor-guard`, `refactorisation`, `refactor`, `restructuration de modules`
- gen-plan détecte un besoin de refactorisation (métriques dégradées, dette technique, demande utilisateur explicite) — hook E13
- La demande mentionne : refactorisation, refactor, refactor-guard, restructuration de modules
- Ne pas déclencher pour du code neuf sans base existante (pas de refactorisation possible)

---

## §1 — Spécification fonctionnelle

**Description (frontmatter verbatim)** : {description}

{s1}
---

## §2 — Spécification technique

{s2}
---

## §3 — Relations

{s3}
---

## §4 — YAML FRONTMATTER (exemplaire verbatim)

```yaml
{frontmatter}
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

1. **Récupération du dépôt par clone git local** (règle d'or n°4 — jamais de lecture distante du contenu) : `git clone https://github.com/bigleon2/KNOWLEDGE.git`
2. **Copie du skill** : porter `skills/refactor-guard/` (SKILL.md + `scripts/` + `evals/` + `references/`) vers `{{{{SKILLS_ROOT}}}}refactor-guard/`
3. **Vérification des dépendances** (frontmatter YAML §4) : `gen-plan >= 3.21.0`, `correct-work >= 2.7.0`, `resource-monitor >= 1.0.0`, `graph-engineering >= 1.0.1`, `spec-driven-development >= 1.0.0`, `harness-engineering >= 1.1.0`, `loop-engineering >= 1.1.0`
4. **Registre KB** ({{{{KB_PATH}}}}) : vérifier la présence de l'entrée `refactor-guard v1.7.0` (arêtes bidirectionnelles — gen-plan hook E13, refactoring-engineering garde-fous, correct-work validation) ; l'inscrire si absente
5. **Evals** : vérifier `evals/evals.json` (schéma skill-creator) et `evals/trigger_evals.json` (bare-liste canonique — décision C006)
6. **Gouvernance** : l'installation laisse le skill en **N0** (`enabled: false` — jamais enabled à l'installation) ; tout passage de niveau est conditionné (§1.3 — stabilité, tests verts, contrats §1.5, rollback testé, journalisation complète)

---

## §6 — VÉRIFICATION POST-INSTALLATION

| # | Vérification | Attendu |
|---|--------------|---------|
| 1 | Fichiers présents | SKILL.md + 11 scripts stdlib + 2 references + 2 evals |
| 2 | Self-tests | 79/79 PASS idempotents ×2 (cumul réel vérifié — §2.1) |
| 3 | `python3 scripts/generer-pm-skill.py --check` | refactor-guard **COHERENT** (4 familles) |
| 4 | Registre KB | entrée `refactor-guard v1.7.0` présente, arêtes bidirectionnelles |
| 5 | Configuration | `enabled: false` (N0) + `allow_push: false` + `require_human_approval: true` |

---

## §7 — HISTORIQUE DES VERSIONS (PM)

| Version | Date | Contenu |
|---------|------|---------|
| v1.7.0 | {TODAY} | Bootstrap initial (décision propriétaire D009 — directive gen-plan(step), session web-b4d7dd19) : PM canonique refactor-guard démarre à v1.7.0 = version convergée du canonique ; sections SKILL.md portées verbatim (§0-§4 + frontmatter) ; structure alignée sur les ancres `scripts/generer-pm-skill.py` (famille n°4 — extension 3→4 familles) ; §5/§6 = gabarit standard d'installation écosystème (scaffolding de bootstrap documenté). |

**Note de provenance (R4 — décision D009)** : les 6 PMs de la lignée externe refactor-guard (v1.2.0→v1.7.0 côté instance source, discussion 468a4c26) ne sont **PAS portés** verbatim au corpus — décision propriétaire D009 (2026-10-12, session web-b4d7dd19) : le PM canonique démarre à v1.7.0 à partir de l'état convergé du skill ; la lignée PM externe demeure documentée par ses preuves de discussion (provenance R4). Les futures montées de version de refactor-guard génèrent leur PM MÉCANIQUEMENT (`scripts/generer-pm-skill.py --generate refactor-guard` — KO-L004 v1.1.0, §2quater PM-INSTALL).

---

## §8 — Conventions

{s4}"""

    # — Idempotence / garde R2 —
    if os.path.isfile(OUT):
        with open(OUT, "rb") as f:
            cur = f.read()
        if hashlib.sha256(cur).hexdigest() == hashlib.sha256(pm.encode("utf-8")).hexdigest():
            print("[NO-OP] PM refactor-guard v1.7.0 déjà présent et byte-identique")
            return
        abandon("PM existant DIVERGENT — ABANDON sans écriture (R2 : jamais écraser)")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(pm)
    print("PM écrit : %s (%d lignes)" % (OUT, pm.count("\n")))
    # — Auto-vérification des ancres generer-pm —
    checks = [
        ("titre", "— Installation du skill refactor-guard v1.7.0"),
        ("skill cible", "> **Skill cible** : refactor-guard v1.7.0"),
        ("version prompt", "> **Version du prompt** : 1.0.0"),
        ("date", "> **Date** : " + TODAY),
        ("yaml", "version: 1.7.0"),
        ("ancre historique", "\n| v1.7.0 | "),
    ]
    for label, motif in checks:
        n = pm.count(motif)
        print("  [%s] ancre %s : %d occurrence(s)" % ("OK" if n >= 1 else "ECART", label, n))
        if n < 1:
            abandon("ancre generer-pm absente : %s" % label)


if __name__ == "__main__":
    main()
