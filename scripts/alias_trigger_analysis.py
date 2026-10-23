#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""
analyse du déclencheur proposé par le propriétaire pour alias-eco :

    alias-eco (<texte récurrent>) --add [<alias>]
    ex : alias-eco ("(de façon cohérente, optimisée et fonctionnelle)") --add $[façon()]

Objectif : tester MÉCANIQUEMENT la logique de parsing de ce format,
détecter les ambiguïtés, puis tester un format alternatif proposé.

Aucune écriture du registre réel — simulation isolée (fixtures en mémoire).
"""
import re
import sys

# ---------------------------------------------------------------- constantes
# garde d'alias ACTUELLE (SKILL.md §1.1, format-alias.md §1)
ALIAS_NAME_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]*$")
# regex de résolution ACTUELLE (alias-manager.py ALIAS_RE)
ALIAS_RESOLVE_RE = re.compile(r"\$([A-Z0-9][A-Z0-9-]*)")

OK, KO = "PASS", "FAIL"
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print("  [%s] %s%s" % (OK if cond else KO, name, (" — " + detail) if detail else ""))


# ================================================================ GRAMMAIRE A
print("=" * 76)
print("GRAMMAIRE A (déclencheur proposé) : alias-eco (<texte>) --add [<alias>]")
print("=" * 76)

# lecture littérale la plus charitable : ( … ) non-gourmand au dernier ) avant --add
GRAMMAIRE_A = re.compile(r"^alias-eco\s*\((.+)\)\s*--add\s*\[?\$?\[?(.+?)\]?\]?\s*$", re.S)

def parse_a(raw):
    m = GRAMMAIRE_A.match(raw.strip())
    if not m:
        return None
    texte, alias = m.group(1), m.group(2)
    # dépouillement des enveloppes « "..." », « (...) » éventuelles
    texte = texte.strip().strip('"').strip()
    if texte.startswith("(") and texte.endswith(")"):
        texte = texte[1:-1]
    alias = alias.strip().strip("$")
    return texte, alias

CAS_A = [
    # (libellé, entrée brute, texte attendu, alias attendu)
    ("exemple exact du propriétaire",
     'alias-eco ("(de façon cohérente, optimisée et fonctionnelle)") --add $[façon()]',
     "de façon cohérente, optimisée et fonctionnelle", "façon()"),
    ("texte sans parenthèses internes",
     'alias-eco (mon écosystème personnel) --add [ECO-LEON]',
     "mon écosystème personnel", "ECO-LEON"),
    ("collision déclencheur existant « (chat) »",
     'alias-eco (chat)',
     None, None),
    ("texte contenant une parenthèse fermante",
     'alias-eco (la compétence alias-eco (chat) est active) --add [X]',
     None, None),
    ("texte contenant la séquence --add",
     'alias-eco (ajouter --add ici) --add [X]',
     None, None),
    ("alias entre crochets non fermés",
     'alias-eco (phrase test) --add [ECO-X',
     "phrase test", "ECO-X"),
    ("alias en minuscules avec accent (façon())",
     'alias-eco (phrase test) --add $[façon()]',
     "phrase test", "façon()"),
]

for label, raw, want_txt, want_alias in CAS_A:
    print("\nCas : %s\n  entrée : %s" % (label, raw))
    parsed = parse_a(raw)
    if want_txt is None:
        check("comportement défini/non-ambigu ?", False,
              "parsing imprévisible ou échec : %r" % (parsed,))
        continue
    if parsed is None:
        check("parsing réussi ?", False, "aucun match")
        continue
    txt, alias = parsed
    check("texte extrait fidèle ?", txt == want_txt, "obtenu %r" % txt)
    check("alias extrait fidèle ?", alias == want_alias, "obtenu %r" % alias)

print("\n-- Gardes fonctionnelles du gestionnaire (format actuel) --")
alias_ex = "façon()"
check("alias %r passe la garde ^[A-Z0-9][A-Z0-9-]*$ ?" % alias_ex,
      bool(ALIAS_NAME_RE.match(alias_ex)),
      "minuscules + accent ç + parenthèses : 3 violations")
res = ALIAS_RESOLVE_RE.sub(lambda m: "<EXPANSÉ:" + m.group(1) + ">",
                           "c'est de la $façon() vraie")
check("$façon() est expansé par --resolve ?", "EXPANSÉ" in res,
      "résultat : %r (alias INTACT, résolution cassée)" % res)
res2 = ALIAS_RESOLVE_RE.sub(lambda m: "<EXPANSÉ:" + m.group(1) + ">",
                            "c'est de la $FAÇON vraie")
check("$FAÇON (accent) est expansé ?", "EXPANSÉ" in res2,
      "résultat : %r" % res2)

# ================================================================ GRAMMAIRE B
print()
print("=" * 76)
print("GRAMMAIRE B (proposée) : alias-eco \"<texte>\" --add <ALIAS>")
print("=" * 76)

GRAMMAIRE_B = re.compile(
    r'^alias-eco\s+(?:«\s*(.+?)\s*»|"(.*?)"\s*)\s*--add\s+\$?([A-Za-z0-9()çéèêàâùûôôîï\-]+)\s*$',
    re.S)

def parse_b(raw):
    m = GRAMMAIRE_B.match(raw.strip())
    if not m:
        return None
    texte = m.group(1) if m.group(1) is not None else m.group(2)
    return texte, m.group(3)

CAS_B = [
    ("exemple propriétaire reformaté",
     'alias-eco "de façon cohérente, optimisée et fonctionnelle" --add OPT-TRIO',
     "de façon cohérente, optimisée et fonctionnelle", "OPT-TRIO"),
    ("guillemets français « »",
     'alias-eco «mon écosystème personnel» --add ECO-LEON',
     "mon écosystème personnel", "ECO-LEON"),
    ("texte avec parenthèses internes",
     'alias-eco "la compétence alias-eco (chat) est active" --add CHAT-REF',
     "la compétence alias-eco (chat) est active", "CHAT-REF"),
    ("texte avec virgules et deux-points",
     'alias-eco "de façon cohérente, optimisée et fonctionnelle : partout" --add OPT-TRIO',
     "de façon cohérente, optimisée et fonctionnelle : partout", "OPT-TRIO"),
    ("texte avec --add interne",
     'alias-eco "écrire --add ici est du texte" --add DOC-ADD',
     "écrire --add ici est du texte", "DOC-ADD"),
    ("alias sans $ (cohérent avec --add du script)",
     'alias-eco "mon dépôt KNOWLEDGE" --add ECO-DEPOT',
     "mon dépôt KNOWLEDGE", "ECO-DEPOT"),
    ("collision (chat) impossible",
     'alias-eco (chat)',
     None, None),
]
for label, raw, want_txt, want_alias in CAS_B:
    print("\nCas : %s\n  entrée : %s" % (label, raw))
    parsed = parse_b(raw)
    if want_txt is None:
        check("rejeté proprement (pas de faux positif) ?", parsed is None,
              "parse_b → %r" % (parsed,))
        continue
    if parsed is None:
        check("parsing réussi ?", False, "aucun match")
        continue
    txt, alias = parsed
    check("texte extrait fidèle ?", txt == want_txt, "obtenu %r" % txt)
    check("alias extrait fidèle ?", alias == want_alias, "obtenu %r" % alias)

print("\n-- Cohérence avec la garde du gestionnaire --")
check("OPT-TRIO passe la garde actuelle ?", bool(ALIAS_NAME_RE.match("OPT-TRIO")))
res3 = ALIAS_RESOLVE_RE.sub(lambda m: "«de façon cohérente, optimisée et fonctionnelle»",
                            "installation $OPT-TRIO.")
check("$OPT-TRIO expansé par --resolve ?", "OPT-TRIO" not in res3, "résultat : %r" % res3)

# ================================================================ BILAN
print()
print("=" * 76)
fails = [n for n, p, _ in results if not p]
print("BILAN : %d/%d PASS — %d FAIL" % (len(results) - len(fails), len(results), len(fails)))
for n in fails:
    print("  FAIL : %s" % n)
sys.exit(0)
