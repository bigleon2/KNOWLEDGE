#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.33 — dérivée dynamiquement)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Script de propagation du Contexte Système à tous les fichiers
Version : 2.2.0 (Task 110 G1 — GO futur, correctif structurel F3 CW Task 107, directive trace 1a1f2297d90c957d) : (1) DYNAMISATION ROBUSTE de la version des 3 gabarits par re.sub sur la séquence « (SHARED v…) » — remplace la clé figée `.replace("(SHARED v1.7.31)")` qui échouait SILENCIEUSEMENT dès que le littéral était bumpé manuellement (cause racine du gabarit périmé v1.7.39 injecté en Task 107, classe F-70-2 4ᵉ occurrence) ; (2) DRY — L3_BLOCK_INNER est DÉRIVÉ de CONTEXT_HEADER_L3 (suppression de la duplication littérale qui dérivait : bases 1.7.31 vs 1.7.40) ; (3) BRANCHE INJECTION — détection de la docstring de module (ast) : le bloc CONTEXTE est inséré en LIGNES COMMENTÉES APRÈS la docstring (canon « docstring d'abord, bloc CONTEXTE ensuite », démontré par bootstrap-ecosysteme.py, GO-3) — JAMAIS de second littéral de chaîne (SyntaxError `from __future__`, les 2 compilations cassées Task 107) ; sans docstring, la forme docstring est insérée APRÈS le shebang ET la ligne coding (PEP 263 préservée) ; (4) BRANCHE REMPLACEMENT — support de la forme commentée mono-ligne en plus de la forme docstring (regex à préfixes stricts par ligne : la forme enveloppée de bootstrap-ecosysteme.py, hors gabarit, reste stable R2) ; précédent 2.1.1 (Task 71 G3 — résorption STRUCTURELLE de la classe F-70-2, 3ᵉ occurrence : la version SHARED des gabarits est DÉRIVÉE DYNAMIQUEMENT du corpus vivant — un bump SHARED sans montée de l'injecteur ne peut plus jamais rétrograder les étiquettes §0) ; précédent 2.1.0 (F-70-2 Task 70 G1 : extension périmètre scripts embarqués skills/*/scripts/*.py) ; précédent 2.0.10 (porte §0 SHARED v1.7.31) ; précédents 2.0.8/2.0.9/2.0.7 (lignes protocole §9, alignement des trois blocs, désambiguïsation référence canonique).
"""

import ast
import io
import os
import re
import tokenize
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
SKILLS_ROOT = REPO_DIR / "skills"

CONTEXT_BLOCK_L2 = """## §0 — Contexte Système (SHARED v1.7.31)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

"""

CONTEXT_HEADER_L3 = '''"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

'''

# v2.2.0 (Task 110 G1 — F3) : la version SHARED des gabarits est substituée par
# re.sub ROBUSTE (n'importe quelle version littérale préexistante est remplacée).
# v2.1.1 : la version est dérivée du corpus vivant (KO-L003) — jamais figée.
def _version_shared():
    m = re.search(r">\s*\*\*Version\*\*\s*:\s*([0-9.]+)",
                  (REPO_DIR / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md").read_text(encoding="utf-8"))
    return m.group(1) if m else "1.7.31"

_VSH = _version_shared()
_RE_VERSION_L3 = re.compile(r"\(SHARED v[0-9.]+\)")

def _dynamiser(modele):
    """Substitue la version SHARED courante dans un gabarit, quelle que soit la version littérale qu'il porte."""
    return _RE_VERSION_L3.sub("(SHARED v%s)" % _VSH, modele, count=1)

CONTEXT_BLOCK_L2 = _dynamiser(CONTEXT_BLOCK_L2)
CONTEXT_HEADER_L3 = _dynamiser(CONTEXT_HEADER_L3)

# v2.2.0 (F3, DRY) : le contenu interne L3 est DÉRIVÉ de l'en-tête docstring —
# une seule source littérale (l'ancienne double écriture L3 dérivait : bases
# v1.7.31 vs v1.7.40). Découpe : [4:-5] ôte l'ouvrant « """\n », le fermant
# « """ » et les 2 blancs terminaux — reproduit EXACTEMENT l'ancien L3_BLOCK_INNER.
assert CONTEXT_HEADER_L3.startswith('"""\n') and CONTEXT_HEADER_L3.endswith('"""\n\n')
L3_BLOCK_INNER = CONTEXT_HEADER_L3[4:-5]

# v2.2.0 (F3, GO-3) : forme commentée du bloc — canon « docstring d'abord, bloc
# CONTEXTE ensuite » (démontré par bootstrap-ecosysteme.py, Task 105 S3) : le
# bloc est inséré en lignes commentées APRÈS la docstring du script, jamais en
# second littéral (SyntaxError `from __future__`).
BLOC_COMMENTAIRE_L3 = "\n".join("# " + ligne for ligne in L3_BLOCK_INNER.rstrip("\n").split("\n")) + "\n"

# v2.2.0 (F3) : regex de remplacement de la forme commentée mono-ligne —
# préfixes stricts par ligne (7 lignes) : la forme ENVELOPPÉE de
# bootstrap-ecosysteme.py (continuations « #   », lignes Langue/Référence
# réparties) ne matche pas et reste stable (R2 — jamais de normalisation forcée).
ANCIEN_BLOC_COMMENTAIRE = re.compile(
    r'^# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge \(SHARED v[0-9.]+\)\n'
    r'# SKILLS_ROOT = [^\n]*\n'
    r'# Conventions : [^\n]*\n'
    r'# Règle Zéro : [^\n]*\n'
    r'# Langue : [^\n]*\n'
    r"# Règles d'or & lecture SHARED[^\n]*\n"
    r'# Référence canonique skill/agent[^\n]*\n',
    re.M,
)

def _fin_docstring_module(source):
    """Ligne de fin (1-based) de la docstring de module, ou None si absente/invalide (ast)."""
    try:
        arbre = ast.parse(source)
    except SyntaxError:
        return None
    if (arbre.body and isinstance(arbre.body[0], ast.Expr)
            and isinstance(arbre.body[0].value, ast.Constant)
            and isinstance(arbre.body[0].value.value, str)):
        return arbre.body[0].end_lineno
    return None

def _docstring_module_span(source):
    """(début, fin) 1-based INCLUSIFS de la docstring de module, ou None (ast)."""
    try:
        arbre = ast.parse(source)
    except SyntaxError:
        return None
    if (arbre.body and isinstance(arbre.body[0], ast.Expr)
            and isinstance(arbre.body[0].value, ast.Constant)
            and isinstance(arbre.body[0].value.value, str)):
        return arbre.body[0].lineno, arbre.body[0].end_lineno
    return None

def _remplacer_docstring_forme(content, motif, remplacement):
    """Substitue le motif UNIQUEMENT dans la docstring de module (span ast) — v2.2.0.

    Garde anti-mutation (Task 110 G1, cas mesuré) : la regex docstring-forme peut
    matcher le TEXTE d'en-tête porté dans un LITTÉRAL de chaîne quelconque (fixture
    de test, générateur, documentation) ; historiquement la substitution pouvait
    alors avaler un délimiteur collé (corruption SyntaxError). Le scoping au span
    de la docstring de module — position canonique réelle des 398 porteurs —
    protège toute copie embarquée hors docstring (les gabarits dynamiques des
    générateurs, v%s / v{version}, ne matchent de toute façon jamais le motif).
    """
    span = _docstring_module_span(content)
    if span is None:
        return content
    debut, fin = span
    lignes = content.split("\n")
    zone = "\n".join(lignes[debut - 1:fin])
    zone_nouvelle = motif.sub(remplacement, zone, count=1)
    if zone_nouvelle == zone:
        return content
    return "\n".join(lignes[:debut - 1] + [zone_nouvelle] + lignes[fin:])

def _lignes_commentaires_reelles(content):
    """Ensemble des numéros de ligne (1-based) portant un VRAI token COMMENT (tokenize)."""
    lignes = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(content).readline):
            if tok.type == tokenize.COMMENT:
                lignes.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return lignes

def _remplacer_comment_forme(content):
    """Substitue le bloc commenté UNIQUEMENT s'il est fait de vraies lignes de commentaire — v2.2.0.

    Garde tokenize (Task 110 G1) : un bloc d'apparence commentée DANS un littéral
    de chaîne n'est pas un commentaire — jamais touché.
    """
    vraies = _lignes_commentaires_reelles(content)

    def _garde(m):
        ligne1 = content.count("\n", 0, m.start()) + 1
        if all(l in vraies for l in range(ligne1, ligne1 + 7)):
            return BLOC_COMMENTAIRE_L3
        return m.group(0)

    return ANCIEN_BLOC_COMMENTAIRE.sub(_garde, content, count=1)

def _ecriture_saine(originale, nouvelle, delta_triple=0):
    """Garde de dernière ligne : l'écriture ne doit jamais casser le fichier.

    Invariants : le résultat parse (ast) ET le compte de délimiteurs de chaîne
    triple varie de l'exact delta attendu (0 pour un remplacement ou une
    insertion commentée ; +2 pour une insertion de forme docstring — un
    remplacement ne doit jamais avaler un délimiteur).
    """
    if nouvelle == originale:
        return True
    try:
        ast.parse(nouvelle)
    except SyntaxError:
        return False
    # delta sur « """ » uniquement (l'insertion docstring-forme en ajoute exactement 2 ;
    # un remplacement n'en ajoute aucun) — le compte de « ''' » est TOUJOURS invariant.
    return (nouvelle.count('"""') == originale.count('"""') + delta_triple
            and nouvelle.count("'''") == originale.count("'''"))

def _inserer_apres_docstring(content):
    """Insère le bloc CONTEXTE commenté APRÈS la docstring (garde les blancs existants, déterministe)."""
    lignes = content.split("\n")
    fin = _fin_docstring_module(content)
    bloc = BLOC_COMMENTAIRE_L3.rstrip("\n").split("\n")
    queue = lignes[fin:]
    if queue and queue[0].strip() == "":
        nouvelles = lignes[:fin] + bloc + queue
    else:
        nouvelles = lignes[:fin] + [""] + bloc + [""] + queue
    return "\n".join(nouvelles)

def _inserer_docstring_en_tete(content):
    """Insère la forme docstring APRÈS le shebang et la ligne coding (PEP 263 — 2 premières lignes)."""
    lignes = content.split("\n")
    idx = 0
    if lignes and lignes[0].startswith("#!"):
        idx = 1
        if len(lignes) > 1 and re.match(r"# -\*-.{0,20}coding", lignes[1]):
            idx = 2
    bloc = CONTEXT_HEADER_L3.rstrip("\n").split("\n")
    nouvelles = lignes[:idx] + bloc + [""] + lignes[idx:]
    return "\n".join(nouvelles)

def propagate_to_skills():
    """Injecte le Niveau 2 dans tous les SKILL.md"""
    print("🔄 Propagation du Contexte Système (Niveau 2) aux skills...")

    count = 0
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('@') or skill_dir.name.startswith('_'):
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding='utf-8')

        if "§0 — Contexte Système" in content:
            # Idempotence v2 : remplacement du bloc résumé existant (mise à jour de version SHARED)
            old_pattern = r'## §0 — Contexte Système \(SHARED v[0-9.]+\)\n\n(?:> [^\n]*\n)+\n'
            new_content = re.sub(old_pattern, CONTEXT_BLOCK_L2, content, count=1)
            if new_content != content:
                skill_md.write_text(new_content, encoding='utf-8')
                count += 1
            continue

        if "§0 — Règle zéro" in content:
            old_pattern = r'## §0 — Règle zéro.*?(?=\n## §1|\n## —)'
            new_content = re.sub(old_pattern, CONTEXT_BLOCK_L2.rstrip(), content, flags=re.DOTALL)
            if new_content != content:
                skill_md.write_text(new_content, encoding='utf-8')
                count += 1
        else:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                new_content = parts[0] + "---" + parts[1] + "---\n\n" + CONTEXT_BLOCK_L2 + parts[2]
            else:
                new_content = CONTEXT_BLOCK_L2 + content

            skill_md.write_text(new_content, encoding='utf-8')
            count += 1

    print(f"   ✅ {count} skills mis à jour")
    return count

def propagate_to_scripts():
    """Injecte le Niveau 3 dans tous les scripts Python"""
    print("\n🔄 Propagation du Contexte Système (Niveau 3) aux scripts...")

    scripts_dir = REPO_DIR / "scripts"
    if not scripts_dir.exists():
        return 0

    count = 0
    # F-70-2 (Task 70 G1 — tests installation $FACON2, leçon F-63-1 : le périmètre
    # doit être PROUVÉ, pas présumé) : le périmètre couvre désormais AUSSI les scripts
    # embarqués des skills (skills/*/scripts/*.py) — en MISE À JOUR idempotente des
    # seuls scripts portant déjà un en-tête §0 (jamais d'injection dans un script
    # qui n'en porte pas : les 3 STALE v1.7.17 alias-manager/orchestrer/is_client
    # étaient invisibles à la propagation précédente)
    embarques = sorted((REPO_DIR / "skills").glob("*/scripts/*.py"))
    embarques_set = set(embarques)
    for script in sorted(scripts_dir.glob("*.py")) + embarques:
        content = script.read_text(encoding='utf-8')

        if "CONTEXTE SYSTÈME" in content:
            # Idempotence v2 : remplacement de l'en-tête existant (mise à jour de version SHARED)
            # v2.0.8 : le motif consomme TOUTES les lignes normatives connues (Langue, Règles d'or §9,
            # Référence canonique §0/§1.2) — sinon les en-têtes v1.7.26+ laissent des lignes pendantes dupliquées
            # v2.2.0 (F3) : deux formes reconnues, CHACUNE SCOPÉE — docstring-forme au span
            # de la docstring de module (ast) ; comment-forme aux vraies lignes de commentaire
            # (tokenize) — toute copie du texte d'en-tête portée dans un littéral (fixture,
            # générateur, doc) est PROTÉGÉE ; garde de parse sur toute écriture.
            old_doc = re.compile(
                r'⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge \(SHARED v[0-9.]+\)\n'
                r'SKILLS_ROOT = [^\n]*\n'
                r'Conventions : [^\n]*\n'
                r'Règle Zéro : [^\n]*\n'
                r'(?:Langue : [^\n]*\n)?'
                r"(?:Règles d'or & lecture SHARED[^\n]*\n)?"
                r'(?:Référence canonique skill/agent[^\n]*\n)?'
            )
            new_content = _remplacer_docstring_forme(content, old_doc, L3_BLOCK_INNER)
            if new_content == content:
                new_content = _remplacer_comment_forme(content)
            if new_content != content and _ecriture_saine(content, new_content):
                script.write_text(new_content, encoding='utf-8')
                count += 1
            elif new_content != content:
                print(f"   ⚠️  {script.name} : substitution annulée (garde de parse — littéral porteur protégé)")
            continue

        if script in embarques_set:
            continue  # F-70-2 : jamais d'injection dans les scripts embarqués des skills

        # v2.2.0 (F3) : injection docstring-aware — si le script porte une docstring
        # de module, le bloc CONTEXTE est inséré en lignes COMMENTÉES après elle
        # (jamais de second littéral : `from __future__` reste valide) ; sinon la
        # forme docstring est insérée après shebang + coding (PEP 263).
        # Garde de parse : une insertion ne doit jamais casser le fichier —
        # delta délimiteurs ATTENDU : 0 (forme commentée) ou +2 (forme docstring).
        if _fin_docstring_module(content) is not None:
            new_content = _inserer_apres_docstring(content)
            delta = 0
        else:
            new_content = _inserer_docstring_en_tete(content)
            delta = 2
        if not _ecriture_saine(content, new_content, delta_triple=delta):
            print(f"   ⚠️  {script.name} : insertion annulée (garde de parse)")
            continue
        script.write_text(new_content, encoding='utf-8')
        count += 1

    print(f"   ✅ {count} scripts mis à jour")
    return count

def propagate_to_agents():
    """Injecte le Niveau 2 dans tous les fichiers .agent"""

    agent_files = list(SKILLS_ROOT.rglob("*.agent"))
    if not agent_files:
        print("   ⚠️ Aucun fichier .agent trouvé")
        return 0

    count = 0
    for agent_file in sorted(agent_files):
        content = agent_file.read_text(encoding='utf-8')

        if "§0 — Contexte Système" in content:
            # Idempotence v2 : remplacement du bloc résumé existant (mise à jour de version SHARED)
            old_pattern = r'## §0 — Contexte Système \(SHARED v[0-9.]+\)\n\n(?:> [^\n]*\n)+\n'
            new_content = re.sub(old_pattern, CONTEXT_BLOCK_L2, content, count=1)
            if new_content != content:
                agent_file.write_text(new_content, encoding='utf-8')
                count += 1
            continue

        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('# Agent') or line.startswith('# [nom-agent]'):
                insert_index = i + 1
                break

        new_lines = lines[:insert_index] + [''] + CONTEXT_BLOCK_L2.split('\n') + lines[insert_index:]
        new_content = '\n'.join(new_lines)

        agent_file.write_text(new_content, encoding='utf-8')
        count += 1

    print(f"   ✅ {count} agents mis à jour")
    return count

def main():
    print("🚀 PROPAGATION DU CONTEXTE SYSTÈME — Architecture v2.0\n")
    print("=" * 60)

    skills_count = propagate_to_skills()
    scripts_count = propagate_to_scripts()
    agents_count = propagate_to_agents()

    print("\n" + "=" * 60)
    print(f"🎉 TERMINÉ : {skills_count} skills + {scripts_count} scripts + {agents_count} agents")

if __name__ == "__main__":
    main()
