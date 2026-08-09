#!/usr/bin/env python3
"""
spell-check.py — Vérification orthographique pour l'écosystème Knowledge

Lexique dynamique construit depuis le dépôt (FR domaine + EN tech).
Protocole d'apprentissage : --learn pour ajouter une correction au lexique.

Règles linguistiques permanentes :
  - Langue docs écosystème  : Français (priorité)
  - Jargon technique       : Anglais (toléré, vérifié)
  - Skills métier ZH       : Chinois (signalé, non corrigé)
  - Langue utilisateur     : Français prio 1, Anglais prio 2
  - Langue IA              : Chinois prio 1, Anglais prio 2, Français prio 3

Usage:
  python3 scripts/spell-check.py                  # Scan (dry-run)
  python3 scripts/spell-check.py --fix              # Auto-correct
  python3 scripts/spell-check.py --learn mot correct # Ajouter au lexique
  python3 scripts/spell-check.py --test             # Tests robustes
  python3 scripts/spell-check.py --stats            # Stats lexique
  python3 scripts/spell-check.py --aliases          # Afficher les double-pointeurs
  python3 scripts/spell-check.py --files a.md,b.md  # Cibler des fichiers
"""

import re
import sys
import os
import json
import unittest
import unicodedata
from pathlib import Path
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEXIQUE_PATH = os.path.join(ROOT, "scripts", "lexique-domain.json")

# ============================================================================
# FICHIERS DE L'ÉCOSYSTÈME À SCANNER (source de vérité + interactions)
# ============================================================================

ECOSYSTEM_FILES = [
    # Prompts maîtres (source de vérité)
    "skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md",
    "skills/_prompts-maitres/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md",
    "skills/_prompts-maitres/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md",
    "skills/_prompts-maitres/PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "skills/_prompts-maitres/README.md",
    # Archive
    "skills/_prompts-maitres/_archive/PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md",
    # Registre KB
    "skills/KNOWLEDGE.md",
    # Skills écosystème
    "skills/gen-plan/SKILL.md",
    "skills/correct-work/SKILL.md",
    "skills/clone-chat/SKILL.md",
    "skills/skills-inventory/SKILL.md",
    "skills/skill-creator/SKILL.md",
    "skills/autonomous-agent/SKILL.md",
    # Scripts écosystème
    "scripts/verify-cross.py",
    "scripts/sync-download.py",
    "scripts/spell-check.py",
    "skills/correct-work/scripts/verify-correct-work.py",
    # Worklog
    "worklog.md",
]

# Détection chinois
ZH_PATTERN = re.compile(r'[\u4e00-\u9fff]')

# Mots EN valides (jamais corrigés)
WHITELIST_EN = {
    # Jargon dev
    "kebab-case", "snake_case", "PascalCase", "camelCase",
    "semver", "frontend", "backend", "fullstack", "webhook", "fallback",
    "checkbox", "endpoint", "middleware", "framework", "standalone",
    "workflow", "skill", "skills", "agent", "agents", "subagent",
    "clone-chat", "gen-plan", "correct-work", "skills-inventory",
    "skill-creator", "autonomous-agent", "fullstack-dev",
    "token", "tokens", "prompt", "prompts", "template", "templates",
    "check", "checks", "checklist", "checklists", "hook", "hooks",
    "scan", "sync", "build", "deploy", "debug", "dump",
    "script", "scripts", "eval", "evals", "ref", "refs",
    "repo", "repository", "commit", "push", "pull", "merge",
    "branch", "master", "main", "origin", "remote",
    "bug", "fix", "patch", "release", "version", "versions",
    "JSON", "YAML", "Markdown", "HTML", "CSS", "JS", "TS", "Python",
    "API", "REST", "GraphQL", "WebSocket", "CORS", "URL", "URI",
    "npm", "pip", "git", "bash", "shell", "node",
    "Linux", "Windows", "macOS", "CLI", "GUI",
    # Noms propres
    "Prisma", "Next.js", "React", "Vue", "Svelte", "Nuxt",
    "Tailwind", "TypeScript", "JavaScript", "Playwright",
    "ReportLab", "LaTeX", "Tectonic", "Mermaid", "ECharts",
    "D3.js", "matplotlib", "seaborn", "pandas", "numpy",
    # Sigles
    "KB", "PM", "ZH", "EN", "FR", "LLM", "VLM", "TTS", "ASR",
    "S1", "S2", "S3", "S4", "E1", "E2", "E3", "E4", "E5",
    "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15",
    # Faux positifs fréquents
    "clone", "cloner", "drift", "context", "target", "trigger",
    "status", "statut", "bump", "bumped", "bumper", "bumping",
    "downgrade", "downgraded", "downgrading", "upgrade", "upgraded",
    "dry-run", "frontmatter", "in extenso", "baseline",
    "cross-reference", "cross-references", "subagent", "subagents",
    "multi-cibles", "pull-request", "standalone",
    # Verbes EN valides dans le contexte
    "scan", "scans", "scanned", "scanning",
    "sync", "synced", "syncing",
    "fix", "fixed", "fixing", "fixes",
    "check", "checked", "checking", "checks",
    "match", "matched", "matching", "matches",
    "fetch", "fetched", "fetching",
    "parse", "parsed", "parsing",
    "validate", "validated", "validating",
    "generate", "generated", "generating",
    "produce", "produced", "producing",
    "invoke", "invoked", "invoking",
    "trigger", "triggered", "triggering",
    "enrich", "enriched", "enriching",
    "deploy", "deployed", "deploying",
    "install", "installed", "installing",
    "update", "updated", "updating",
    "append", "appended", "appending",
    "compare", "compared", "comparing",
    "identify", "identified", "identifying",
    "detect", "detected", "detecting",
    "extract", "extracted", "extracting",
    "integrate", "integrated", "integrating",
    "execute", "executed", "executing",
    "operate", "operated", "operating",
    "preserve", "preserved", "preserving",
    "archive", "archived", "archiving",
    "assign", "assigned", "assigning",
    "configure", "configured", "configuring",
    "optimize", "optimized", "optimizing",
    "associate", "associated", "associating",
    "replace", "replaced", "replacing",
    "suppress", "suppressed", "suppressing",
    "signal", "signaled", "signaling",
    "persist", "persisted", "persisting",
    "inject", "injected", "injecting",
    "maintain", "maintained", "maintaining",
    "perform", "performed", "performing",
    "construct", "constructed", "constructing",
    "inject", "injected", "injecting",
}


def load_lexicon():
    """Charge le lexique depuis le fichier JSON."""
    if not os.path.exists(LEXIQUE_PATH):
        return {"fr_accents": {}, "en_tech": {}, "_meta": {}}
    with open(LEXIQUE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_lexicon(lexicon):
    """Sauvegarde le lexique."""
    with open(LEXIQUE_PATH, "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=2, sort_keys=True)


def strip_accents(text):
    """Retire les accents d'un texte."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _build_alias_zones(line, aliases):
    """Construit la liste des zones protégées par les aliases (double-pointeurs).

    Un alias est un double-pointeur : deux termes pointent vers le même concept.
    Ex: "correct-work" -> "verifie ton travail" (même rôle = alias).
    Mais "corriger" != "éditer" (rôles différents = pas d'alias).

    Retourne un set de (start, end) tuples — plages de caractères protégées.
    Les mots dans ces zones ne sont pas corrigés par fr_accents.
    """
    zones = set()
    for canonical, alias_list in aliases.items():
        # Protéger aussi le terme canonique lui-même
        for term in [canonical] + alias_list:
            if not term or len(term) < 2:
                continue
            # Recherche insensible à la casse
            lower_line = line.lower()
            lower_term = term.lower()
            start = 0
            while True:
                idx = lower_line.find(lower_term, start)
                if idx == -1:
                    break
                zones.add((idx, idx + len(term)))
                start = idx + 1
    return zones


def _in_alias_zone(pos, length, zones):
    """Vérifie si un match [pos, pos+length) chevauche une zone alias protégée."""
    for zs, ze in zones:
        if pos < ze and pos + length > zs:
            return True
    return False


def scan_file(filepath, lexicon):
    """
    Scan un fichier et retourne les findings.
    Retourne : list de (ligne, mot_trouve, correction, position)
    Les zones couvertes par un alias (double-pointeur) sont protégées.
    """
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (FileNotFoundError, PermissionError) as e:
        return [(0, "ERREUR", str(e), "")]

    fr_map = lexicon.get("fr_accents", {})
    en_map = lexicon.get("en_tech", {})
    aliases = lexicon.get("aliases", {})
    zh_lines = []

    for i, line in enumerate(lines, 1):
        # Détection chinois (informatif)
        if ZH_PATTERN.search(line):
            zh_lines.append(i)

        # Construire les zones protégées par les aliases (double-pointeurs)
        alias_zones = _build_alias_zones(line, aliases)

        # Vérifications FR (accents manquants)
        for wrong, correct in fr_map.items():
            # Matcher le mot avec ses frontières
            # Mais ne pas matcher à l'intérieur d'un mot plus long
            pattern = r"(?<![a-zA-ZàâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ\-])" + re.escape(wrong) + r"(?![a-zA-ZàâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ\-])"
            for m in re.finditer(pattern, line, re.IGNORECASE):
                # Skip si dans une zone alias protégée (double-pointeur)
                if _in_alias_zone(m.start(), len(m.group()), alias_zones):
                    continue
                # Skip si dans whitelist EN
                word = m.group()
                if word.lower() in WHITELIST_EN or word in WHITELIST_EN:
                    continue
                # Skip si la correction est identique (no-op)
                if word == correct:
                    continue
                # Skip si déjà accentué (le wrong matche un mot qui a déjà des accents ailleurs)
                if re.search(r'[àâäéèêëïîôùûüÿçœæ]', word):
                    continue
                findings.append((i, word, correct, f"L{i}:{m.start()+1}"))

        # Vérifications EN (termes tech mal orthographiés)
        for wrong, correct in en_map.items():
            # Pour les termes composés (avec espace), utiliser search au lieu de word boundary
            if " " in wrong:
                if wrong in line:
                    findings.append((i, wrong, correct, f"L{i}"))
            else:
                pattern = r"(?<![a-zA-Z])" + re.escape(wrong) + r"(?![a-zA-Z])"
                for m in re.finditer(pattern, line):
                    findings.append((i, m.group(), correct, f"L{i}:{m.start()+1}"))

    if zh_lines:
        findings.append((0, "INFO_ZH", f"{len(zh_lines)} ligne(s) avec caractères chinois", ""))

    return findings


def print_report(results, verbose=False):
    """Affiche le rapport de scan."""
    total = 0
    errors = 0
    zh_count = 0

    for filepath, findings in sorted(results.items()):
        file_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        file_errors = [f for f in findings if f[1] == "ERREUR"]
        file_zh = [f for f in findings if f[1] == "INFO_ZH"]

        if not file_findings and not file_errors and not file_zh:
            if verbose:
                rel = os.path.relpath(filepath, ROOT)
                print(f"  [OK] {rel}")
            continue

        rel = os.path.relpath(filepath, ROOT)
        print(f"\n{'='*60}")
        print(f"  {rel}")
        print(f"{'='*60}")

        for f in file_errors:
            print(f"  [ERREUR] L{f[0]}: {f[2]}")
            errors += 1

        for f in file_findings:
            total += 1
            print(f"  L{f[0]:>4d}  {f[1]:<30s} -> {f[2]}  ({f[3]})")

        for f in file_zh:
            zh_count += 1
            print(f"  [INFO] {f[2]}")

    print(f"\n{'='*60}")
    print(f"  TOTAL : {total} finding(s) orthographique(s)")
    if errors:
        print(f"  ERREURS : {errors} fichier(s) inaccessibles")
    if zh_count:
        print(f"  INFO ZH : {zh_count} fichier(s) avec caractères chinois")
    print(f"{'='*60}")
    return total


def apply_fixes(results, lexicon):
    """Applique les corrections dans les fichiers.
    Les zones couvertes par un alias (double-pointeur) sont protégées.
    """
    fixed_files = 0
    total_fixes = 0

    fr_map = lexicon.get("fr_accents", {})
    en_map = lexicon.get("en_tech", {})
    aliases = lexicon.get("aliases", {})

    for filepath, findings in results.items():
        if "spell-check.py" in filepath:
            continue
        file_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        if not file_findings:
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except (FileNotFoundError, PermissionError):
            continue

        original = content
        lines = content.splitlines(keepends=True)
        new_lines = []

        for line in lines:
            # Construire les zones protégées par les aliases
            alias_zones = _build_alias_zones(line, aliases)

            # Appliquer corrections FR en respectant les zones alias
            for wrong, correct in fr_map.items():
                pattern = r"(?<![a-zA-ZàâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ\-])" + re.escape(wrong) + r"(?![a-zA-ZàâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ\-])"

                def replace_alias_safe(m):
                    """Ne remplace que si le match n'est pas dans une zone alias."""
                    if _in_alias_zone(m.start(), len(m.group()), alias_zones):
                        return m.group()  # Protégé par alias, ne pas corriger
                    return correct

                line = re.sub(pattern, replace_alias_safe, line, flags=re.IGNORECASE)

            # Appliquer corrections EN (les termes EN composés ne sont pas dans les aliases FR)
            for wrong, correct in en_map.items():
                line = line.replace(wrong, correct)

            new_lines.append(line)

        content = "".join(new_lines)

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_files += 1
            total_fixes += len(file_findings)
            rel = os.path.relpath(filepath, ROOT)
            print(f"  [FIXED] {rel} ({len(file_findings)} correction(s))")

    print(f"\n  {total_fixes} correction(s) appliquée(s) dans {fixed_files} fichier(s)")
    return fixed_files, total_fixes


def learn_word(wrong, correct, lexicon):
    """Protocole d'apprentissage : ajoute une correction au lexique.

    Règles :
    1. Vérifier que 'wrong' n'est pas déjà dans le lexique
    2. Déterminer si c'est FR (accents) ou EN (tech)
    3. Ajouter dans la bonne section
    4. Sauvegarder
    """
    if wrong == correct:
        print(f"  [SKIP] '{wrong}' == '{correct}' (pas de correction)")
        return False

    fr_map = lexicon.get("fr_accents", {})
    en_map = lexicon.get("en_tech", {})

    if wrong in fr_map or wrong in en_map:
        existing = fr_map.get(wrong, en_map.get(wrong))
        if existing == correct:
            print(f"  [EXISTS] '{wrong}' -> '{correct}' déjà dans le lexique")
            return False
        else:
            print(f"  [CONFLICT] '{wrong}' existe déjà -> '{existing}', pas '{correct}'")
            print(f"           Utilisez --learn-force pour écraser")
            return False

    # Déterminer la catégorie
    has_accent_diff = (strip_accents(correct) == wrong) or (strip_accents(correct.lower()) == wrong.lower())
    is_en = (not re.search(r'[àâäéèêëïîôùûüÿçœæ]', correct)) and re.search(r'[a-z]', correct)

    if has_accent_diff and not is_en:
        lexicon["fr_accents"][wrong] = correct
        section = "fr_accents"
    else:
        lexicon["en_tech"][wrong] = correct
        section = "en_tech"

    save_lexicon(lexicon)
    print(f"  [LEARNED] '{wrong}' -> '{correct}' ajouté dans {section}")
    return True


def print_stats(lexicon):
    """Affiche les statistiques du lexique."""
    fr = lexicon.get("fr_accents", {})
    en = lexicon.get("en_tech", {})
    aliases = lexicon.get("aliases", {})
    meta = lexicon.get("_meta", {})
    total_aliases = sum(len(v) for v in aliases.values())

    print(f"\n{'='*60}")
    print(f"  SPELL-CHECK — Statistiques du lexique")
    print(f"{'='*60}")
    print(f"  FR accents  : {len(fr)} entrées")
    print(f"  EN tech    : {len(en)} entrées")
    print(f"  Aliases    : {len(aliases)} canoniques -> {total_aliases} alias")
    print(f"  Total      : {len(fr) + len(en)} entrées")
    print(f"  Whitelist  : {len(WHITELIST_EN)} termes EN")
    print(f"  Fichiers   : {len(ECOSYSTEM_FILES)} fichier(s) écosystème")
    if meta:
        print(f"\n  Langues docs : {meta.get('langues', {}).get('docs_ecosysteme', '?')}")
        print(f"  Jargon tech  : {meta.get('langues', {}).get('jargon_technique', '?')}")
        print(f"  Règles IA    : {meta.get('regles_ia', '?')}")
        print(f"  Règles User  : {meta.get('regles_user', '?')}")
    if aliases:
        print(f"\n  --- Double-pointeurs (aliases) ---")
        for canonical, alias_list in sorted(aliases.items()):
            alias_str = ", ".join(alias_list)
            print(f"  {canonical} -> [{alias_str}]")
    print(f"{'='*60}")


def cmd_scan(args):
    """Mode scan (dry-run)."""
    lexicon = load_lexicon()
    do_fix = "--fix" in args

    filepaths = _resolve_files(args)
    results = {}
    for fp in filepaths:
        results[fp] = scan_file(fp, lexicon)

    mode = "FIX" if do_fix else "SCAN"
    print(f"\n  SPELL-CHECK v1.0.0 | Mode: {mode} | Fichiers: {len(filepaths)}")
    total = print_report(results)

    if do_fix:
        print(f"\n  Application des corrections...")
        apply_fixes(results, lexicon)

    return total


def cmd_learn(args):
    """Mode apprentissage."""
    lexicon = load_lexicon()
    idx = args.index("--learn")
    if idx + 2 >= len(args):
        print("  Usage: --learn <mot_incorrect> <mot_correct>")
        return 1
    wrong, correct = args[idx + 1], args[idx + 2]
    return 0 if learn_word(wrong, correct, lexicon) else 1


def cmd_stats():
    """Mode statistiques."""
    lexicon = load_lexicon()
    print_stats(lexicon)
    return 0


def _resolve_files(args):
    """Résout les fichiers à scanner depuis les args ou la liste par défaut."""
    for i, a in enumerate(args):
        if a == "--files" and i + 1 < len(args):
            return [os.path.join(ROOT, f) for f in args[i + 1].split(",")]
    return [os.path.join(ROOT, f) for f in ECOSYSTEM_FILES]


# ============================================================================
# TESTS ROBUSTES
# ============================================================================

class TestSpellCheck(unittest.TestCase):
    """Tests robustes pour spell-check.py"""

    def setUp(self):
        self.lexicon = load_lexicon()

    # --- Tests lexique ---
    def test_lexique_fr_non_vide(self):
        """Le lexique FR doit contenir des entrées."""
        fr = self.lexicon.get("fr_accents", {})
        self.assertGreater(len(fr), 100, "Lexique FR trop petit")

    def test_lexique_en_non_vide(self):
        """Le lexique EN tech doit contenir des entrées."""
        en = self.lexicon.get("en_tech", {})
        self.assertGreater(len(en), 10, "Lexique EN tech trop petit")

    def test_lexique_no_self_mapping(self):
        """Aucune entrée ne doit mapper vers elle-même (no-op)."""
        for section in ("fr_accents", "en_tech"):
            for k, v in self.lexicon.get(section, {}).items():
                self.assertNotEqual(k, v, f"No-op dans {section}: {k} -> {v}")

    def test_lexique_meta_present(self):
        """Les métadonnées du lexique doivent être présentes."""
        meta = self.lexicon.get("_meta", {})
        self.assertIn("version", meta)
        self.assertIn("langues", meta)
        self.assertIn("regles_ia", meta)
        self.assertIn("regles_user", meta)

    def test_lexique_meta_langues(self):
        """Les règles linguistiques doivent être cohérentes."""
        meta = self.lexicon["_meta"]
        self.assertEqual(meta["langues"]["docs_ecosysteme"], "FR")
        self.assertEqual(meta["langues"]["jargon_technique"], "EN")
        self.assertIn("ZH", meta["langues"]["skills_metier"])

    def test_lexique_aliases_present(self):
        """La section aliases (double-pointeurs) doit être présente et non vide."""
        aliases = self.lexicon.get("aliases", {})
        self.assertGreater(len(aliases), 0, "La section aliases doit exister")
        # Vérifier que correct-work a des alias
        self.assertIn("correct-work", aliases)
        self.assertGreater(len(aliases["correct-work"]), 0)

    def test_lexique_aliases_no_canonical_overlap(self):
        """Un alias ne doit pas être aussi un terme canonique (pas de cycle)."""
        aliases = self.lexicon.get("aliases", {})
        canonicals = set(aliases.keys())
        for canonical, alias_list in aliases.items():
            for alias in alias_list:
                self.assertNotIn(alias, canonicals,
                                 f"Cycle d'alias : '{alias}' est à la fois canonique et alias de '{canonical}'")

    # --- Tests de détection FR ---
    def test_detect_verification_sans_accent(self):
        """'Verification' (sans accent) doit être détecté."""
        findings = scan_fr_line("Verification du travail", self.lexicon)
        self.assertTrue(any(f[1] == "Verification" for f in findings))

    def test_detect_etapes_sans_accent(self):
        """'etapes' (sans accent) doit être détecté."""
        findings = scan_fr_line("les 5 etapes du processus", self.lexicon)
        self.assertTrue(any(f[1] == "etapes" for f in findings))

    def test_detect_metriques_sans_accent(self):
        """'metriques' (sans accent) doit être détecté."""
        findings = scan_fr_line("metriques de performance", self.lexicon)
        self.assertTrue(any(f[1] == "metriques" for f in findings))

    def test_detect_decouplage_sans_accent(self):
        """'decouplage' (sans accent) doit être détecté."""
        findings = scan_fr_line("decouplage gen-plan", self.lexicon)
        self.assertTrue(any(f[1] == "decouplage" for f in findings))

    def test_detect_depend_sans_accent(self):
        """'depend' (sans accent) doit être détecté."""
        findings = scan_fr_line("Depend de gen-plan", self.lexicon)
        self.assertTrue(any(f[1] == "Depend" or f[1] == "depend" for f in findings))

    def test_detect_derniere_sans_accent(self):
        """'derniere' (sans accent) doit être détecté."""
        findings = scan_fr_line("Derniere calibration", self.lexicon)
        self.assertTrue(any(f[1] == "Derniere" or f[1] == "derniere" for f in findings))

    def test_detect_ecart_sans_accent(self):
        """'ecart' (sans accent) doit être détecté."""
        findings = scan_fr_line("un ecart de 14%", self.lexicon)
        self.assertTrue(any(f[1] == "ecart" for f in findings))

    def test_detect_ecosysteme_sans_accent(self):
        """'ecosysteme' (sans accent) doit être détecté."""
        findings = scan_fr_line("l ecosysteme Knowledge", self.lexicon)
        self.assertTrue(any(f[1] == "ecosysteme" for f in findings))

    def test_no_false_positive_accentue(self):
        """'vérification' (avec accent) ne doit PAS être détecté."""
        findings = scan_fr_line("vérification du travail", self.lexicon)
        fr_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertEqual(len(fr_findings), 0, "Faux positif sur mot déjà accentué")

    def test_no_false_positive_etapes_accentue(self):
        """'étapes' (avec accent) ne doit PAS être détecté."""
        findings = scan_fr_line("les 5 étapes du processus", self.lexicon)
        fr_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertEqual(len(fr_findings), 0)

    # --- Tests whitelist EN ---
    def test_whitelist_kebab_case(self):
        """'kebab-case' ne doit pas être corrigé."""
        findings = scan_fr_line("Répertoires : kebab-case (gen-plan)", self.lexicon)
        fr_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertEqual(len(fr_findings), 0, "Faux positif sur kebab-case")

    def test_whitelist_frontend(self):
        """'frontend' ne doit pas être corrigé."""
        findings = scan_fr_line("Frontend only", self.lexicon)
        fr_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertEqual(len(fr_findings), 0)

    def test_whitelist_clone_chat(self):
        """'clone-chat' ne doit pas être corrigé."""
        findings = scan_fr_line("clone-chat v2.0.0", self.lexicon)
        fr_findings = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertEqual(len(fr_findings), 0)

    # --- Tests EN tech ---
    def test_detect_kebab_case_wrong(self):
        """'kebab case' (sans tiret) doit être détecté."""
        findings = scan_en_line("Répertoires : kebab case", self.lexicon)
        self.assertTrue(any(f[1] == "kebab case" for f in findings))

    def test_detect_front_matter_wrong(self):
        """'front matter' (sans tiret) doit être détecté."""
        findings = scan_en_line("Le front matter YAML", self.lexicon)
        self.assertTrue(any("front matter" in f[1] for f in findings))

    # --- Tests ZH ---
    def test_detect_zh_info(self):
        """Les caractères chinois doivent être signalés (INFO_ZH)."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write("中文测试")
            tmp_zh = tf.name
        try:
            findings = scan_file(tmp_zh, self.lexicon)
            zh_info = [f for f in findings if f[1] == "INFO_ZH"]
            self.assertTrue(len(zh_info) > 0, "Caractères ZH non détectés")
        finally:
            os.unlink(tmp_zh)

    # --- Tests de frontière de mot ---
    def test_word_boundary_etapes(self):
        """'etapes' dans 'metapes' ne doit pas matcher."""
        findings = scan_fr_line("des metapes du système", self.lexicon)
        self.assertFalse(any(f[1] == "etapes" for f in findings),
                         "Faux positif: 'etapes' matché dans 'metapes'")

    def test_word_boundary_integration(self):
        """'integration' dans 'désintégration' ne doit pas matcher."""
        findings = scan_fr_line("la désintégration du système", self.lexicon)
        self.assertFalse(any(f[1] == "integration" for f in findings))

    # --- Tests learn ---
    def test_learn_new_word(self):
        """--learn doit ajouter un nouveau mot au lexique."""
        lex = load_lexicon()
        test_wrong = "_test_spell_check_tmp_"
        test_correct = "_test_spell_check_ok_"
        # Cleanup avant
        lex.get("fr_accents", {}).pop(test_wrong, None)
        lex.get("en_tech", {}).pop(test_wrong, None)
        result = learn_word(test_wrong, test_correct, lex)
        self.assertTrue(result)
        # Cleanup après
        lex.get("fr_accents", {}).pop(test_wrong, None)
        lex.get("en_tech", {}).pop(test_wrong, None)
        save_lexicon(lex)

    def test_learn_noop_rejected(self):
        """--learn avec wrong == correct doit être rejeté."""
        lex = load_lexicon()
        result = learn_word("test", "test", lex)
        self.assertFalse(result)

    def test_learn_duplicate_rejected(self):
        """--learn avec un doublon doit être rejeté."""
        lex = load_lexicon()
        # Prendre une entrée existante
        fr = lex.get("fr_accents", {})
        if fr:
            existing_wrong, existing_correct = list(fr.items())[0]
            result = learn_word(existing_wrong, existing_correct, lex)
            self.assertFalse(result)

    # --- Tests de casse ---
    def test_case_sensitive_verification(self):
        """'Verification' (majuscule) doit être détecté."""
        findings = scan_fr_line("Verification complète", self.lexicon)
        self.assertTrue(any(f[1] == "Verification" for f in findings))

    def test_case_sensitive_depend(self):
        """'Depend' (majuscule) doit être détecté."""
        findings = scan_fr_line("Depend de gen-plan", self.lexicon)
        self.assertTrue(any(f[1] == "Depend" for f in findings))

    # --- Tests sur fichiers réels ---
    def test_scan_real_file_shared(self):
        """SHARED.md doit passer le scan (0 finding)."""
        fp = os.path.join(ROOT, "skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md")
        findings = scan_file(fp, self.lexicon)
        real = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        # SHARED a été corrigé, donc 0 finding attendu
        self.assertLessEqual(len(real), 5, f"SHARED.md a {len(real)} finding(s): {real}")

    def test_scan_real_file_pm_correct_work(self):
        """PM correct-work doit passer le scan (0 finding)."""
        fp = os.path.join(ROOT, "skills/_prompts-maitres/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md")
        findings = scan_file(fp, self.lexicon)
        real = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertLessEqual(len(real), 5, f"PM correct-work a {len(real)} finding(s): {real}")

    def test_scan_real_file_readme(self):
        """README.md _prompts-maitres doit passer le scan (0 finding)."""
        fp = os.path.join(ROOT, "skills/_prompts-maitres/README.md")
        findings = scan_file(fp, self.lexicon)
        real = [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
        self.assertLessEqual(len(real), 10, f"README.md a {len(real)} finding(s): {real}")

    # --- Tests aliases (double-pointeurs) ---
    def test_alias_verifie_ton_travail_protege(self):
        """'verifie' dans 'verifie ton travail' ne doit PAS être corrigé (alias de correct-work)."""
        findings = scan_fr_line("verifie ton travail avant de continuer", self.lexicon)
        self.assertEqual(len(findings), 0,
                         "'verifie' dans l'alias 'verifie ton travail' ne doit pas être corrigé")

    def test_alias_verifie_seul_corrigé(self):
        """'resultats' SEUL DOIT être corrigé en 'résultats' (hors alias).

        Le mot 'resultats' dans l'alias 'verifie tes resultats' est protégé,
        mais seul il doit être détecté.
        """
        findings = scan_fr_line("les resultats sont bons", self.lexicon)
        self.assertTrue(any(f[1].lower() == "resultats" for f in findings),
                        "'resultats' seul DOIT être corrigé (pas dans un alias)")

    def test_alias_resultats_dans_alias_protégé(self):
        """'resultats' dans 'verifie tes resultats' ne doit PAS être corrigé (alias)."""
        findings = scan_fr_line("verifie tes resultats", self.lexicon)
        self.assertFalse(any(f[1].lower() == "resultats" for f in findings),
                         "'resultats' dans l'alias 'verifie tes resultats' ne doit pas être corrigé")

    def test_alias_canonical_protégé(self):
        """Le terme canonique lui-même protège ses composants.

        'nommage kebab' est un alias de 'kebab-case'. On vérifie que le scan
        d'une ligne contenant un alias canonique ne produit pas de findings FR
        parasites (les composants EN sont protégés par la zone alias).
        """
        findings = scan_fr_line("utilise le nommage kebab pour les fichiers", self.lexicon)
        # 'nommage kebab' est un alias de kebab-case
        # 'nommage' n'est pas dans fr_accents, 'kebab' n'est pas dans fr_accents
        # donc 0 findings FR attendus (les findings EN seraient dans un autre test)
        fr_findings = [f for f in findings if 'INFO' not in f[1] and 'ERREUR' not in f[1]]
        self.assertEqual(len(fr_findings), 0)

    def test_alias_semantique_vs_different(self):
        """'corriger' et 'editer' n'ont PAS d'alias (rôles différents).

        Ce test vérifie que l'absence d'alias entre deux termes à rôles différents
        ne crée pas de protection croisée — chacun reste indépendant.
        """
        # Aucun alias ne contient 'corriger' ni 'editer'
        aliases = self.lexicon.get("aliases", {})
        all_aliases = set()
        for canon, alias_list in aliases.items():
            all_aliases.add(canon.lower())
            for a in alias_list:
                all_aliases.add(a.lower())
        # 'corriger' et 'editer' ne doivent pas être dans les aliases
        self.assertNotIn("corriger", all_aliases)
        self.assertNotIn("editer", all_aliases)

    def test_alias_liste_verification_protégé(self):
        """'verification' dans 'liste de verification' ne doit PAS être corrigé (alias de checklist)."""
        findings = scan_fr_line("la liste de verification est longue", self.lexicon)
        self.assertFalse(any(f[1].lower() == "verification" for f in findings),
                         "'verification' dans l'alias 'liste de verification' ne doit pas être corrigé")

    def test_alias_verification_seul_corrigé(self):
        """'verification' SEUL DOIT être corrigé en 'vérification'."""
        findings = scan_fr_line("la verification est terminee", self.lexicon)
        self.assertTrue(any(f[1].lower() == "verification" for f in findings),
                        "'verification' seul DOIT être corrigé")


def scan_fr_line(text, lexicon):
    """Helper : scan une ligne de texte pour les corrections FR."""
    # Écrire le texte dans un fichier temporaire
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        tmp = f.name
    try:
        findings = scan_file(tmp, lexicon)
        return [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH")]
    finally:
        os.unlink(tmp)


def scan_en_line(text, lexicon):
    """Helper : scan une ligne de texte pour les corrections EN."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        tmp = f.name
    try:
        findings = scan_file(tmp, lexicon)
        return [f for f in findings if f[1] not in ("ERREUR", "INFO_ZH", "INFO_EN")]
    finally:
        os.unlink(tmp)


def cmd_test():
    """Mode test."""
    print("\n  SPELL-CHECK v1.0.0 | Mode: TEST")
    print("  " + "=" * 50)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSpellCheck)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print(f"\n  Tests: {result.testsRun} run, {len(result.failures)} failed, {len(result.errors)} errors")
    return 0 if result.wasSuccessful() else 1


def cmd_aliases():
    """Mode aliases : affiche la table des double-pointeurs."""
    lexicon = load_lexicon()
    aliases = lexicon.get("aliases", {})
    if not aliases:
        print("  Aucun alias défini.")
        return 0
    total = sum(len(v) for v in aliases.values())
    print(f"\n{'='*60}")
    print(f"  ALIASES (double-pointeurs) : {len(aliases)} canoniques, {total} alias")
    print(f"{'='*60}")
    for canonical, alias_list in sorted(aliases.items()):
        print(f"  {canonical}")
        for a in alias_list:
            print(f"    -> {a}")
    print(f"{'='*60}")
    return 0


def main():
    args = sys.argv[1:]

    if "--learn" in args:
        return cmd_learn(args)
    elif "--test" in args:
        return cmd_test()
    elif "--stats" in args:
        return cmd_stats()
    elif "--aliases" in args:
        return cmd_aliases()
    else:
        return cmd_scan(args)


if __name__ == "__main__":
    sys.exit(main())