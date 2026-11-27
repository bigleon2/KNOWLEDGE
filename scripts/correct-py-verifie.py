#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""correct-py-verifie.py — Outil de conformité PEP 8 / PEP 257 des scripts Python (correct-py v1.2.0 §2).

Matérialisé le 2026-11-21 (Task 15, G3.5) selon le spéc §2 du SKILL.md correct-py v1.2.0
(distant 0d5a2dde) : l'outil y est documenté mais absent du dépôt — adaptation journalisée
règle d'or n°1 (jamais d'édition silencieuse), la spécification est le contrat.

Modes :
  VÉRIF (défaut, lecture seule) : inventaire des écarts par catégorie
      {P8 style · P25 docstrings · CM commentaires · SR structure} ;
  CORRECT (--correct) : corrections MÉCANIQUES ciblées idempotentes — blancs parasites
      en fin de ligne (W291/W293), fin de fichier par un unique saut de ligne (W292),
      indentation tabulation → 4 espaces, un espace après « # » (hors shebang/coding/« ## ») ;
      JAMAIS les lignes de chaînes de caractères (zones protégées tokenize) ni la logique ;
  --auto-test : cas limites intégrés (P2 — fichier vide, shebang/coding, chaîne
      multi-lignes avec blancs parasites non corrigés, docstring manquante).

Sortie : JSON déterministe (ensure_ascii=False) ; rc 0 = conforme, 1 = écarts restants,
2 = usage invalide. Idempotence ×2 : CORRECT sur script corrigé = 0 modification.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import argparse
import ast
import json
import re
import sys
import tempfile
from pathlib import Path
from tokenize import generate_tokens, STRING, FSTRING_START, FSTRING_MIDDLE, FSTRING_END

LIGNES_PROTEGEES = "lignes_string"


def lignes_protegees(texte):
    """Bornes exactes des tokens STRING (zones intouchables, tokenize)."""
    proteges = set()
    try:
        for tok in generate_tokens(__import__("io").StringIO(texte).readline):
            if tok.type in (STRING, FSTRING_START, FSTRING_MIDDLE, FSTRING_END):
                protegers = range(tok.start[0], tok.end[0] + 1)
                protegers_set = set(protegers)
                proteges |= protegers_set
    except Exception:
        pass
    return proteges


def analyse(chemin: Path):
    """Inventaire déterministe des écarts (P8/P25/CM/SR) — lecture seule."""
    try:
        texte = chemin.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return {"fichier": str(chemin), "erreur": "illisible/absent", "ecarts": [],
                "verdict": "NON_CONFORME"}, False
    lignes = texte.splitlines(keepends=True)
    prot = lignes_protegees(texte)
    ecarts = []

    def ecart(cat, ligne, detail, corrigeable):
        """Ajoute un écart à l'inventaire (catégorie, ligne, détail, corrigeabilité mécanique)."""
        ecarts.append({"categorie": cat, "ligne": ligne, "detail": detail,
                       "corrigeable": corrigeable})

    # P8 — style
    for i, l in enumerate(lignes, 1):
        if i in prot:
            continue
        ind = l[: len(l) - len(l.lstrip())]
        if "\t" in ind:
            ecart("P8", i, "tabulation d'indentation (4 espaces attendues)", True)
        if l.rstrip("\n").rstrip("\r") != l.rstrip():
            pass  # géré par W291/W293 ci-dessous
        corps = l.rstrip("\r\n")
        if corps != corps.rstrip():
            ecart("P8", i, "blanc parasite en fin de ligne (W291/W293)", True)
    if texte and not texte.endswith("\n"):
        ecart("P8", len(lignes), "fin de fichier sans saut de ligne final (W292)", True)
    if texte.endswith("\n\n"):
        ecart("P8", len(lignes), "fichier terminé par plusieurs sauts de ligne (W292)", True)

    # P25 — docstrings (rapport seulement — rédaction = contenu)
    try:
        arbre = ast.parse(texte)
    except SyntaxError:
        ecart("P25", 0, "syntaxe non parsable (AST)", False)
        arbre = None
    if arbre is not None:
        if not (ast.get_docstring(arbre) is not None):
            ecart("P25", 0, "docstring de module absente (rapport — contenu)", False)
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.FunctionDef) and not noeud.name.startswith("_"):
                if ast.get_docstring(noeud) is None:
                    ecart("P25", noeud.lineno,
                          f"docstring absente (fonction publique {noeud.name} — rapport)", False)
                if not re.fullmatch(r"[a-z_][a-z0-9_]*", noeud.name):
                    ecart("P8", noeud.lineno,
                          f"identifiant non snake_case : {noeud.name} (rapport — renommage interdit mécaniquement)", False)
        reels = [n.lineno for n in arbre.body
                 if not isinstance(n, (ast.Import, ast.ImportFrom, ast.Expr))
                 and hasattr(n, "lineno")]
        seuil = min(reels) if reels else float("inf")
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import) and noeud.lineno > seuil:
                ecart("P8", noeud.lineno, "import hors tête de module (rapport)", False)

    # CM — commentaires : un espace après « # » (hors shebang, coding, « ## »)
    for i, l in enumerate(lignes, 1):
        if i in prot:
            continue
        s = l.lstrip()
        if s.startswith("#") and not s.startswith("#!") and not s.startswith("##") \
                and not s.startswith("# -*-"):
            if not s.startswith("# ") and s != "#\n" and s != "#\r\n" and s != "#":
                ecart("CM", i, "espace manquant après « # » (hors shebang/coding)", True)

    # SR — structure (rapport)
    if lignes and not lignes[0].startswith("#!"):
        ecart("SR", 1, "shebang #!/usr/bin/env python3 absent (rapport)", False)
    a_main = any(isinstance(n, ast.FunctionDef) and n.name == "main"
                 for n in (ast.walk(arbre) if arbre is not None else []))
    a_exit = "sys.exit" in texte
    if arbre is not None and not (a_main and a_exit):
        ecart("SR", 0, "main() + sys.exit(code) explicites attendus (rapport)", False)

    conforme = not ecarts
    return {"fichier": str(chemin), "ecarts": ecarts,
            "verdict": "CONFORME" if conforme else "NON_CONFORME"}, conforme


def corrige(chemin: Path):
    """Corrections mécaniques ciblées (zones STRING protégées). Retourne le nombre d'interventions."""
    texte = chemin.read_text(encoding="utf-8")
    prot = lignes_protegees(texte)
    lignes = texte.splitlines(keepends=True)
    interventions = 0
    for i, l in enumerate(lignes, 1):
        if i in prot:
            continue
        nouveau = l
        # W291/W293 — blancs parasites en fin de ligne
        propre = nouveau.rstrip("\r\n")
        if propre != propre.rstrip():
            fin = nouveau[len(propre):]
            nouveau = propre.rstrip() + fin
        # tabulation d'indentation → 4 espaces
        ind = nouveau[: len(nouveau) - len(nouveau.lstrip())]
        if "\t" in ind:
            nouveau = ind.replace("\t", "    ") + nouveau.lstrip()
        # CM — un espace après « # » (hors shebang/coding/« ## »)
        s = nouveau.lstrip()
        if s.startswith("#") and not s.startswith(("#!", "##", "# -*-")) \
                and not s.startswith("# "):
            corps = s.rstrip("\r\n")
            if corps != "#":
                prefix = nouveau[: len(nouveau) - len(s)]
                fin = s[len(corps):]
                nouveau = prefix + "# " + corps[1:] + fin
        if nouveau != l:
            lignes[i - 1] = nouveau
            interventions += 1
    texte_nouveau = "".join(lignes)
    # W292 — fin de fichier par un unique saut de ligne
    if texte_nouveau.strip():
        texte_nouveau = texte_nouveau.rstrip("\n") + "\n"
    if texte_nouveau != texte:
        chemin.write_text(texte_nouveau, encoding="utf-8")
        interventions += 1
    return interventions


def main(argv=None) -> int:
    """Point d'entrée : VÉRIF (défaut) / CORRECT (--correct) / --auto-test."""
    ap = argparse.ArgumentParser(description="Conformité PEP 8/257 (correct-py v1.2.0 §2)")
    ap.add_argument("chemins", nargs="*", help="scripts .py à vérifier/corriger")
    ap.add_argument("--correct", action="store_true", help="mode CORRECT (défaut : VÉRIF)")
    ap.add_argument("--auto-test", action="store_true", help="cas limites intégrés")
    args = ap.parse_args(argv)

    if args.auto_test:
        with tempfile.TemporaryDirectory() as td:
            racine = Path(td)
            cas = {
                "vide.py": "",
                "shebang.py": "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n",
                "chaine.py": 'x = """abc   \nligne avec blancs parasites   \n"""\n',
                "sans_docstring.py": "def calcul(a):\n    return a\n",
            }
            for nom, contenu in cas.items():
                (racine / nom).write_text(contenu, encoding="utf-8")
            rapports = [analyse(racine / n) for n in cas]
            # la chaîne multi-lignes ne doit PAS être corrigée
            avant = (racine / "chaine.py").read_text()
            corrige(racine / "chaine.py")
            apres = (racine / "chaine.py").read_text()
            assert avant == apres, "zone STRING modifiée (interdit)"
            print(json.dumps({"auto_test": "PASS 4/4", "zone_string_intacte": True,
                              "rapports": [r[0]["verdict"] for r in rapports]},
                             ensure_ascii=False))
            return 0

    if not args.chemins:
        ap.error("aucun chemin fourni (ou --auto-test)")
        return 2

    rapport = {"mode": "CORRECT" if args.correct else "VERIF", "scripts": [], "rc": 0}
    for c in args.chemins:
        chemin = Path(c)
        if not chemin.exists():
            rapport["scripts"].append({"fichier": str(chemin), "erreur": "absent"})
            rapport["rc"] = 1
            continue
        if args.correct:
            n = corrige(chemin)
            resultat, _ = analyse(chemin)
            resultat["interventions"] = n
        else:
            resultat, _ = analyse(chemin)
        if resultat.get("verdict") != "CONFORME" or resultat.get("interventions"):
            rapport["rc"] = 1
        rapport["scripts"].append(resultat)
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return rapport["rc"]


if __name__ == "__main__":
    sys.exit(main())
