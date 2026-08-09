---
name: skills-inventory
version: 1.0.0
category: ecosystem
language: fr
tags:
  - inventory
  - scanning
  - catalog
  - ecosystem
description: >
  Skill inventory scanner and reporter. Activates whenever the user asks to list, inventory,
  catalog, browse, search, or explore available skills — e.g. "quelles sont les skills dispo",
  "list all skills", "show me what skills I have", "inventory of skills", "what skills are
  installed", "génère l'inventaire des skills", "skills.md", "skill browser", "find a skill for X",
  "which skill should I use for Y", "is there a skill that does Z", "what tools and capabilities
  do I have", "how many skills in category X". Also triggers when the user mentions "skills-inventory"
  explicitly or asks about skill categories, counts, statistics, or comparisons between skills.
  Use this skill whenever you need to scan /home/z/my-project/skills/, generate a skills inventory
  document, find the right skill for a task, or answer questions about the skill ecosystem — even
  if the user doesn't explicitly say "skill inventory".
dependencies: []
---

# Skills Inventory

Scan the local skills directory, build a structured inventory, and present it to the user.

## Overview

This skill provides a complete inventory of all installed skills in `/home/z/my-project/skills/`.
It reads every `SKILL.md` frontmatter, extracts metadata (name, version, description, category),
and produces a rich markdown inventory that can be displayed inline, saved as a file, or used to
answer skill-related questions.

## Workflow

1. **Run the scanner script** to get the current state of all skills.
2. **Parse the output** into a structured summary.
3. **Present results** in the format the user requested (inline summary, full file, or targeted answer).

## Step 1 — Run the Scanner

Execute the bundled scanner script:

```bash
python /home/z/my-project/skills/skills-inventory/scripts/generate_skills_md.py --json
```

This outputs a JSON array to stdout with one entry per skill:

```json
[
  {
    "name": "pdf",
    "display_name": "pdf",
    "version": "1.0",
    "aka": "",
    "date": "2026-06-02",
    "size": "56.7 KB",
    "lines": 879,
    "description": "Professional PDF toolkit with four production lines...",
    "category": "Documents & Contenu"
  }
]
```

Flags:
- `--json` — output raw JSON (for programmatic use)
- `--output /path/to/file.md` — write full markdown inventory to a file
- `--category "IA & Media"` — filter to a single category
- `--search "chart"` — filter skills whose name or description contains the search term

## Step 2 — Present Results

Choose the presentation based on what the user asked for:

### Inline summary (default when user asks "list skills" or "what skills do you have")

Show a compact table grouped by category with skill counts:

```
### Skills installées (66 skills, 12 catégories)

| Catégorie | Skills |
|---|---|
| IA & Media | ASR, TTS, LLM, VLM, image-generation, image-edit, ... |
| Documents & Contenu | pdf, docx, pptx, xlsx, cheat-sheet |
| ... | ... |
```

### Full inventory (when user asks to "generate skills.md" or "export inventory")

Run with `--output` to write the complete markdown file:

```bash
python /home/z/my-project/skills/skills-inventory/scripts/generate_skills_md.py \
  --output /home/z/my-project/download/skills.md
```

### Targeted search (when user asks "find a skill for X" or "which skill does Y")

Run with `--search` and present matching results:

```bash
python /home/z/my-project/skills/skills-inventory/scripts/generate_skills_md.py \
  --search "chart" --json
```

## Category Reference

The scanner classifies skills into these 12 categories:

| Category | Typical Skills |
|---|---|
| Autres | Miscellaneous skills not fitting other categories |
| Carrière & Emploi | Resume, interview, job tracking |
| Contenu & Marketing | Blog, SEO, content strategy, marketing |
| Documents & Contenu | PDF, DOCX, PPTX, XLSX, cheat-sheet |
| Développement | Fullstack, coding agent, version management |
| Finance & Recherche | Finance, stock analysis, academic search, market research |
| IA & Media | ASR, TTS, LLM, VLM, image/video generation & understanding |
| Lifestyle & Bien-être | Wellness, dream interpreter, fortune analysis |
| Méta (Skills & Plans) | Skill creator, skill finder, writing plans, task review |
| Visualisation & Design | Charts, design, UI/UX, visual foundations |
| Web & Recherche | Web search, web reader, multi-search, agent browser |
| Éducation | Quiz, study buddy, gaokao (college entrance exam) tools |

## Output Format

The full markdown inventory (`skills.md`) contains:
- Header with generation date, total skill count, category count
- Clickable table of contents linking to each category section
- Per-category tables: Name, Version, AKA, Date, Size, Lines, Description
- Detailed per-skill section with full description
- Footer with file metadata

## Notes

- The scanner reads YAML frontmatter from each `SKILL.md`. If a skill has no frontmatter,
  it falls back to `_meta.json`, then to keyword-based heuristic classification.
- Skills without a `SKILL.md` in their directory are silently skipped.
- The inventory is a point-in-time snapshot. Re-run the scanner to refresh.
- This skill replaces the old manual `generate_skills_md.py` that was in `/scripts/`.
