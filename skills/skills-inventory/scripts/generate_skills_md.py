#!/usr/bin/env python3
"""
generate_skills_md.py — Scan /home/z/my-project/skills/ and generate skills inventory.

Outputs:
  --json       Raw JSON array of skill records to stdout
  --output F   Full markdown inventory written to file F
  --category C Filter to a single category
  --search T   Filter skills whose name or description contains T (case-insensitive)

Default (no flags): print compact summary to stdout.

Usage:
    python scripts/generate_skills_md.py                    # inline summary
    python scripts/generate_skills_md.py --json             # JSON for programmatic use
    python scripts/generate_skills_md.py --output skills.md # full markdown file
    python scripts/generate_skills_md.py --search "chart"   # filtered search
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILLS_ROOT = Path("/home/z/my-project/skills")

# ── Category mapping (keyword → display category) ──────────────────────────
CATEGORY_KEYWORDS = {
    # IA & Media
    "ASR": "IA & Media", "TTS": "IA & Media", "LLM": "IA & Media", "VLM": "IA & Media",
    "image-generation": "IA & Media", "image-edit": "IA & Media", "image-search": "IA & Media",
    "image-understand": "IA & Media", "video-understand": "IA & Media", "video-generation": "IA & Media",
    "pdf-llm": "IA & Media", "podcast-generate": "IA & Media",
    # Documents & Contenu
    "pdf": "Documents & Contenu", "docx": "Documents & Contenu", "pptx": "Documents & Contenu",
    "ppt": "Documents & Contenu", "xlsx": "Documents & Contenu", "cheat-sheet": "Documents & Contenu",
    # Visualisation & Design
    "charts": "Visualisation & Design", "design": "Visualisation & Design",
    "ui-ux-pro-max": "Visualisation & Design", "visual-design-foundations": "Visualisation & Design",
    "interview-designer": "Visualisation & Design",
    # Web & Recherche
    "web-search": "Web & Recherche", "web-reader": "Web & Recherche",
    "web-shader-extractor": "Web & Recherche", "multi-search-engine": "Web & Recherche",
    "agent-browser": "Web & Recherche", "qingyan-research": "Web & Recherche",
    # Développement
    "fullstack-dev": "Développement", "coding-agent": "Développement",
    "version-management": "Développement",
    # Carrière & Emploi
    "resume-builder": "Carrière & Emploi", "jd-resume-tailor": "Carrière & Emploi",
    "job-intent-tracker": "Carrière & Emploi", "interview-prep": "Carrière & Emploi",
    # Contenu & Marketing
    "blog-writer": "Contenu & Marketing", "content-strategy": "Contenu & Marketing",
    "seo-content-writer": "Contenu & Marketing", "marketing-mode": "Contenu & Marketing",
    "storyboard-manager": "Contenu & Marketing", "contentanalysis": "Contenu & Marketing",
    # Finance & Recherche
    "finance": "Finance & Recherche", "stock-analysis": "Finance & Recherche",
    "ai-news": "Finance & Recherche", "aminer": "Finance & Recherche",
    "market-research": "Finance & Recherche",
    # Éducation
    "quiz-mastery": "Éducation", "quiz-html": "Éducation", "study-buddy": "Éducation",
    "gaokao": "Éducation",
    # Lifestyle & Bien-être
    "anti-pua": "Lifestyle & Bien-être", "dream-interpreter": "Lifestyle & Bien-être",
    "get-fortune": "Lifestyle & Bien-être", "gift-evaluator": "Lifestyle & Bien-être",
    "mindfulness": "Lifestyle & Bien-être",
    # Méta (Skills & Plans)
    "skill-creator": "Méta (Skills & Plans)", "skill-finder": "Méta (Skills & Plans)",
    "task-review": "Méta (Skills & Plans)", "writing-plans": "Méta (Skills & Plans)",
    "correct-work": "Méta (Skills & Plans)", "skills-inventory": "Méta (Skills & Plans)",
    # Autres (fallback)
    "auto-target-tracker": "Autres",
}

CATEGORY_ORDER = [
    "Autres", "Carrière & Emploi", "Contenu & Marketing", "Documents & Contenu",
    "Développement", "Finance & Recherche", "IA & Media", "Lifestyle & Bien-être",
    "Méta (Skills & Plans)", "Visualisation & Design", "Web & Recherche", "Éducation",
]


def extract_frontmatter(filepath: Path) -> dict:
    frontmatter = {}
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return frontmatter, ""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return frontmatter, text
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            frontmatter[key.strip().lower()] = val.strip().strip("'\"")
    return frontmatter, text[m.end():]


def read_meta_json(filepath: Path) -> dict:
    try:
        return json.loads(filepath.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_file_size_kb(filepath: Path) -> str:
    size = filepath.stat().st_size
    return f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"


def get_line_count(filepath: Path) -> int:
    try:
        return sum(1 for _ in filepath.open(encoding="utf-8", errors="replace"))
    except Exception:
        return 0


def get_last_modified(filepath: Path) -> str:
    ts = filepath.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def truncate(text: str, max_len: int = 120) -> str:
    return text if len(text) <= max_len else text[:max_len - 1] + "…"


def detect_category(skill_name: str, frontmatter: dict, meta: dict) -> str:
    if "category" in frontmatter:
        return frontmatter["category"]
    if meta and "category" in meta:
        return meta["category"]
    for keyword, cat in CATEGORY_KEYWORDS.items():
        if keyword.lower() in skill_name.lower():
            return cat
    return "Autres"


def extract_description(body: str, max_len: int = 120) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith(">"):
            cleaned = re.sub(r"\*+", "", stripped)
            cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
            return truncate(cleaned, max_len)
    return ""


def scan_skills() -> list[dict]:
    skills = []
    if not SKILLS_ROOT.exists():
        print(f"ERROR: Skills root not found: {SKILLS_ROOT}", file=sys.stderr)
        sys.exit(1)

    for entry in sorted(SKILLS_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        frontmatter, body = extract_frontmatter(skill_md)
        meta_path = entry / "_meta.json"
        meta = read_meta_json(meta_path) if meta_path.exists() else {}
        skill_yaml = entry / "skill.yaml"

        name = frontmatter.get("name", entry.name)
        description_raw = frontmatter.get("description", "")
        version = frontmatter.get("version", meta.get("version", ""))
        aka = frontmatter.get("aka", meta.get("aka", ""))

        if not description_raw:
            description_raw = extract_description(body)

        category = detect_category(entry.name, frontmatter, meta)
        size = get_file_size_kb(skill_md)
        lines = get_line_count(skill_md)
        date = get_last_modified(skill_md)

        if not version and skill_yaml.exists():
            try:
                yaml_text = skill_yaml.read_text(encoding="utf-8", errors="replace")
                vm = re.search(r"version:\s*(.+)", yaml_text)
                if vm:
                    version = vm.group(1).strip()
            except Exception:
                pass

        skills.append({
            "name": name,
            "display_name": entry.name,
            "version": version or "—",
            "aka": aka or "—",
            "date": date or "—",
            "size": size,
            "lines": lines,
            "description": truncate(description_raw, 120) if description_raw else "",
            "category": category,
        })
    return skills


def filter_skills(skills: list[dict], category: str = None, search: str = None) -> list[dict]:
    if category:
        skills = [s for s in skills if s["category"].lower() == category.lower()]
    if search:
        term = search.lower()
        skills = [s for s in skills if term in s["display_name"].lower() or term in s.get("description", "").lower()]
    return skills


def print_summary(skills: list[dict]) -> None:
    """Print compact inline summary grouped by category."""
    categories: dict[str, list[str]] = {}
    for s in skills:
        categories.setdefault(s["category"], []).append(s["display_name"])

    # Sort categories
    sorted_cats = []
    for cat in CATEGORY_ORDER:
        if cat in categories:
            sorted_cats.append(cat)
    for cat in sorted(categories.keys()):
        if cat not in sorted_cats:
            sorted_cats.append(cat)

    print(f"\n### Skills installées ({len(skills)} skills, {len(sorted_cats)} catégories)\n")
    print("| Catégorie | Skills |")
    print("|---|---|")
    for cat in sorted_cats:
        names = ", ".join(sorted(categories[cat]))
        print(f"| {cat} | {names} |")
    print()


def generate_markdown(skills: list[dict]) -> str:
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

    categories: dict[str, list[dict]] = {}
    for s in skills:
        categories.setdefault(s["category"], []).append(s)

    sorted_cats = []
    for cat in CATEGORY_ORDER:
        if cat in categories:
            sorted_cats.append(cat)
    for cat in sorted(categories.keys()):
        if cat not in sorted_cats:
            sorted_cats.append(cat)

    lines = []
    lines.append("# Inventaire des Skills installés")
    lines.append("")
    lines.append(f"> Fichier généré automatiquement le {now} UTC")
    lines.append(f"> Total : **{len(skills)} skills** répartis en **{len(sorted_cats)} catégories**")
    lines.append(f"> Source : `{SKILLS_ROOT}/`")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sommaire
    lines.append("## Sommaire")
    lines.append("")
    for cat in sorted_cats:
        count = len(categories[cat])
        anchor = cat.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("&", "")
        lines.append(f"- [{cat}](#{anchor}) ({count})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-category tables
    for cat in sorted_cats:
        cat_skills = sorted(categories[cat], key=lambda s: s["display_name"].lower())
        lines.append(f"## {cat}")
        lines.append("")
        lines.append("| Nom | Version | AKA | Date | Taille | Lignes | Description courte |")
        lines.append("|---|---|---|---|---|---|---|")
        for s in cat_skills:
            desc = truncate(s["description"], 100) if s["description"] else ""
            lines.append(
                f"| `{s['display_name']}` | v{s['version']} | {s['aka']} | {s['date']} "
                f"| {s['size']} | {s['lines']} | {desc} |"
            )
        lines.append("")

    # Détails section
    lines.append("---")
    lines.append("")
    lines.append("## Détails des skills")
    lines.append("")
    for cat in sorted_cats:
        cat_skills = sorted(categories[cat], key=lambda s: s["display_name"].lower())
        for s in cat_skills:
            lines.append(f"### `{s['display_name']}` v{s['version']}")
            lines.append("")
            lines.append(f"- **Chemin** : `skills/{s['display_name']}/SKILL.md`")
            lines.append(f"- **Date** : {s['date']}")
            lines.append(f"- **AKA** : {s['aka']}")
            lines.append(f"- **Taille** : {s['size']} ({s['lines']} lignes)")
            lines.append("")
            if s["description"]:
                lines.append("**Description** :")
                lines.append("")
                lines.append(f"> {s['description']}")
                lines.append("")

    # Metadata footer
    lines.append("---")
    lines.append("")
    lines.append("## Métadonnées du fichier")
    lines.append("")
    lines.append(f"- **Fichier** : généré par `skills-inventory`")
    lines.append(f"- **Date de génération** : {now}")
    lines.append(f"- **Nombre total de skills** : {len(skills)}")
    lines.append(f"- **Nombre de catégories** : {len(sorted_cats)}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Scan skills directory and generate inventory")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--output", type=str, help="Write full markdown inventory to file")
    parser.add_argument("--category", type=str, help="Filter to a single category")
    parser.add_argument("--search", type=str, help="Filter by name or description substring")
    args = parser.parse_args()

    skills = scan_skills()
    skills = filter_skills(skills, args.category, args.search)

    if args.json:
        json.dump(skills, sys.stdout, ensure_ascii=False, indent=2)
        print()  # trailing newline
    elif args.output:
        md = generate_markdown(skills)
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"Written to {out} ({len(skills)} skills)")
    else:
        print_summary(skills)


if __name__ == "__main__":
    main()
