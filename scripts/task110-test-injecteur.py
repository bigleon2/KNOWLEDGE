#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 110 — Harnais de test de l'injecteur propagate-context.py (T1.1/T1.2).

Règle d'or n°5 (mesurer avant corriger) : le harnais construit un bac à sable
minimal (mini-arbre skills/ + scripts/ + SHARED corpus factice v1.7.40), y copie
l'injecteur COURANT et exécute la propagation, puis vérifie mécaniquement chaque
cas de la matrice F3 (CW Task 107) + les gardes v2.2.0 :

  a) docstring + from __future__  → doit compiler ET porter le bloc (v2.1.1 : SyntaxError)
  b) docstring simple             → bloc APRÈS la docstring, jamais de second littéral
  c) shebang + coding, sans docstring → bloc inséré SANS casser la ligne coding (2 1ʳᵉˢ lignes)
  d) sans shebang ni docstring    → bloc en tête
  e) porteur forme docstring v1.7.39 (docstring de module) → resynchronisé v1.7.40
  f) porteur forme commentée v1.7.39 (vrais commentaires)  → resynchronisé v1.7.40
  g) script embarqué skills/*/scripts/ → JAMAIS injecté, byte-identique
  h) SKILL.md porteur §0 v1.7.39 → §0 v1.7.40
  i) SKILL.md sans §0            → bloc §0 injecté
  j) en-tête STALE dans un LITTÉRAL de chaîne (délimiteur collé) → JAMAIS touché
     (garde scoping ast — la substitution textuelle historique avalait le « \"\"\" »)
  k) bloc commenté STALE dans un LITTÉRAL de chaîne → JAMAIS touché (garde tokenize)

Hygiène des fixtures (leçon du cas mesuré en séance) : aucun texte d'en-tête
matchable n'est embarqué littéralement dans le présent harnais — les porteurs
stales sont construits à l'exécution depuis un modèle à jeton {{VERSION}}.

Idempotence : 2ᵉ exécution de l'injecteur = fichiers byte-stables (sha256).
Lecture seule sur l'arbre réel (copie vers bac à sable tempfile).
Sortie : verdicts par cas + résumé ; rc 0 ssi tous PASS.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import hashlib
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOTE = Path("/home/z/my-project")
INJECTEUR = HOTE / "scripts" / "propagate-context.py"

SHARED_FICTIF = """# PM SHARED factice (bac à sable — Task 110)

> **Version** : 1.7.40

Contenu factice : le seul champ lu par l'injecteur est la ligne Version.
"""

CAS_A = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cas a — docstring puis from __future__ (les 2 compilations cassées CW 107).

Description du cas : le script porte sa docstring d'intention en tête, puis
l'import future. L'injection d'un SECOND littéral de chaîne avant l'import
produit une SyntaxError (from __future__ doit suivre la docstring, pas une
expression).
"""
from __future__ import annotations

CONST = 1
'''

CAS_B = '''#!/usr/bin/env python3
"""Cas b — docstring simple sans import future."""

import os

X = os.name
'''

CAS_C = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

print(json.__name__)
'''

CAS_D = '''import sys

print(sys.version)
'''

# Modèle à jeton (jamais matchable par `v[0-9.]+`) — les porteurs stales sont
# dérivés à l'exécution (hygiène des fixtures, leçon du cas mesuré en séance).
L37_MODELE = """⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v{{VERSION}})
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE_JETON}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/)."""

L37 = L37_MODELE.replace("{{VERSION}}", "1.7.39").replace("{{VARIABLE_JETON}}", "{{VARIABLE}}")
L37_COLLE = "\n".join(L37.split("\n")[:-1] + [L37.split("\n")[-1] + '\"\"\"'])
BLOC_COMMENT_STALE = "\n".join("# " + ligne for ligne in L37.split("\n"))

CAS_E = '#!/usr/bin/env python3\n"""%s\n"""\n\nimport sys\nprint(sys.version)\n' % L37

CAS_F = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"""Cas f — porteur forme commentée v1.7.39."""\n%s\nimport sys\nprint(sys.version)\n' % BLOC_COMMENT_STALE

CAS_J = ('#!/usr/bin/env python3\n'
         '# -*- coding: utf-8 -*-\n'
         '"""Cas j — littéral porteur : en-tête STALE à délimiteur collé (jamais touché)."""\n'
         'FIXTURE = """%s\n'
         'import sys\nprint(sys.version)\n') % L37_COLLE

CAS_K = ('#!/usr/bin/env python3\n'
         '"""Cas k — bloc commenté STALE dans un littéral (jamais touché — garde tokenize)."""\n'
         'FIXTURE_COMMENTEE = """\n%s\n"""\n'
         'import sys\nprint(sys.version)\n') % BLOC_COMMENT_STALE

EMBARQUE = '"""Cas g — script embarqué, jamais injecté (F-70-2)."""\n\nX = 1\n'

SKILL_ALPHA = """---
name: alpha
version: 1.0.0
---
## §0 — Contexte Système (SHARED v1.7.39)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md
> Conventions : kebab-case.

# Corps alpha
"""

SKILL_BETA = """---
name: beta
version: 1.0.0
---
# Corps beta — aucun bloc §0 à l'origine.
"""


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def compiler_chemin(chemin: Path) -> bool:
    """Vrai si le fichier compile (py_compile, doraise → exception attrapée)."""
    try:
        py_compile.compile(str(chemin), doraise=True)
        return True
    except (py_compile.PyCompileError, SyntaxError):
        return False


def construire_sandbox(base: Path) -> dict:
    """Monte le bac à sable et renvoie la carte des fichiers témoins."""
    (base / "skills" / "@mon-ecosysteme").mkdir(parents=True)
    (base / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md").write_text(SHARED_FICTIF, encoding="utf-8")
    for nom, skill in (("alpha", SKILL_ALPHA), ("beta", SKILL_BETA)):
        (base / "skills" / nom).mkdir()
        (base / "skills" / nom / "SKILL.md").write_text(skill, encoding="utf-8")
    (base / "skills" / "gamma" / "scripts").mkdir(parents=True)
    (base / "skills" / "gamma" / "scripts" / "embarque.py").write_text(EMBARQUE, encoding="utf-8")
    (base / "scripts").mkdir()
    shutil.copy2(INJECTEUR, base / "scripts" / "propagate-context.py")
    cas = {"a": CAS_A, "b": CAS_B, "c": CAS_C, "d": CAS_D, "e": CAS_E, "f": CAS_F, "j": CAS_J, "k": CAS_K}
    for lettre, contenu in cas.items():
        (base / "scripts" / ("cas_%s.py" % lettre)).write_text(contenu, encoding="utf-8")
    return {("script", l): base / "scripts" / ("cas_%s.py" % l) for l in cas} | {
        ("embarque", "g"): base / "skills" / "gamma" / "scripts" / "embarque.py",
        ("skill", "h"): base / "skills" / "alpha" / "SKILL.md",
        ("skill", "i"): base / "skills" / "beta" / "SKILL.md",
    }


def executer_injecteur(base: Path) -> str:
    r = subprocess.run([sys.executable, str(base / "scripts" / "propagate-context.py")],
                       capture_output=True, text=True, cwd=str(base))
    return r.stdout + r.stderr


def verdicts(base: Path, carte: dict) -> list:
    """Vérifie chaque cas — renvoie [(cas, PASS/FAIL, détail)]."""
    res = []

    def add(cas, ok, detail):
        res.append((cas, bool(ok), detail))

    a = carte[("script", "a")].read_text(encoding="utf-8")
    add("a: docstring+future compile", compiler_chemin(carte[("script", "a")]),
        "py_compile cas_a")
    add("a: bloc CONTEXTE présent", "CONTEXTE SYSTÈME" in a and "v1.7.40" in a,
        "marqueur + version courante")

    b_txt = carte[("script", "b")].read_text(encoding="utf-8")
    add("b: compile", compiler_chemin(carte[("script", "b")]), "py_compile cas_b")
    add("b: bloc après docstring sans second littéral",
        "CONTEXTE SYSTÈME" in b_txt and b_txt.count('"""') == 2,
        "marqueur présent + exactement 1 docstring (2 délimiteurs)")

    c_txt = carte[("script", "c")].read_text(encoding="utf-8")
    lignes_c = c_txt.split("\n")
    add("c: compile", compiler_chemin(carte[("script", "c")]), "py_compile cas_c")
    add("c: coding dans les 2 premières lignes",
        any("coding" in l for l in lignes_c[:2]) and "CONTEXTE SYSTÈME" in c_txt,
        "PEP 263 préservée + bloc présent")

    d_txt = carte[("script", "d")].read_text(encoding="utf-8")
    add("d: compile + bloc", compiler_chemin(carte[("script", "d")]) and "CONTEXTE SYSTÈME" in d_txt,
        "py_compile cas_d + marqueur")

    e_txt = carte[("script", "e")].read_text(encoding="utf-8")
    add("e: porteur docstring-form resynchronisé",
        "(SHARED v1.7.40)" in e_txt and "(SHARED v1.7.39)" not in e_txt and compiler_chemin(carte[("script", "e")]),
        "version à jour + compile")

    f_txt = carte[("script", "f")].read_text(encoding="utf-8")
    add("f: porteur comment-form resynchronisé",
        "# ⚙️ CONTEXTE SYSTÈME" in f_txt and "(SHARED v1.7.40)" in f_txt and "(SHARED v1.7.39)" not in f_txt
        and compiler_chemin(carte[("script", "f")]),
        "forme commentée à jour + compile (garde sur l'étiquette (SHARED v…))")

    g_txt = carte[("embarque", "g")].read_text(encoding="utf-8")
    add("g: embarqué intact", g_txt == EMBARQUE, "byte-identique à la source")

    h_txt = carte[("skill", "h")].read_text(encoding="utf-8")
    add("h: SKILL.md §0 v1.7.40", "(SHARED v1.7.40)" in h_txt and "(SHARED v1.7.39)" not in h_txt,
        "L2 resynchronisé")

    i_txt = carte[("skill", "i")].read_text(encoding="utf-8")
    add("i: SKILL.md sans §0 → injecté", "## §0 — Contexte Système (SHARED v1.7.40)" in i_txt,
        "L2 injecté après frontmatter")

    j_txt = carte[("script", "j")].read_text(encoding="utf-8")
    add("j: littéral porteur collé INTACT",
        j_txt == CAS_J and compiler_chemin(carte[("script", "j")]),
        "byte-identique + compile (scoping ast : la docstring de module seule est substituée)")

    k_txt = carte[("script", "k")].read_text(encoding="utf-8")
    add("k: bloc commenté dans littéral INTACT",
        k_txt == CAS_K and compiler_chemin(carte[("script", "k")]),
        "byte-identique + compile (garde tokenize : pas de vrais tokens COMMENT)")
    return res


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="task110-injecteur-"))
    try:
        carte = construire_sandbox(tmp)
        executer_injecteur(tmp)
        res = verdicts(tmp, carte)
        empreintes_1 = {k: sha256(p) for k, p in carte.items()}
        executer_injecteur(tmp)  # 2ᵉ passe — idempotence
        empreintes_2 = {k: sha256(p) for k, p in carte.items()}
        stable = [k for k in empreintes_1 if empreintes_1[k] != empreintes_2[k]]
        print("=== Harnais task110-test-injecteur — matrice F3 (CW 107) + gardes v2.2.0 ===")
        for cas, ok, detail in res:
            print("  [%s] %s — %s" % ("PASS" if ok else "FAIL", cas, detail))
        print("  [%s] idempotence ×2 — %d/%d fichiers byte-stables"
              % ("PASS" if not stable else "FAIL", len(empreintes_1) - len(stable), len(empreintes_1)))
        if stable:
            print("      instables : %s" % ", ".join(map(str, stable)))
        total = len(res) + 1
        passes = sum(1 for _, ok, _ in res if ok) + (0 if stable else 1)
        print("=== RESUME : %d/%d PASS ===" % (passes, total))
        return 0 if passes == total else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
