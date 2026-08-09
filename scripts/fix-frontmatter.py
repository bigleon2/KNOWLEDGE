#!/usr/bin/env python3
"""Phase 2 — Standardisation frontmatter des skills métier.

Ajoute les champs manquants (version, category, language, tags, dependencies)
pour tous les SKILL.md métier, en préservant les champs existants.
Corrige aussi les name mismatches.
"""

import os
import re
import yaml

SKILLS_ROOT = '/home/z/my-project/skills'
ECOSYSTEM = {'gen-plan', 'correct-work', 'clone-chat', 'skills-inventory', 'skill-creator', 'autonomous-agent'}

# Known Z.AI skills with metadata.version pattern
ZAI_METADATA_SKILLS = {'pdf', 'docx', 'xlsx', 'charts', 'pptx', 'image-edit', 'image-generation',
                        'image-understand', 'video-understand', 'video-generation', 'web-search',
                        'web-reader', 'VLM', 'LLM', 'TTS', 'ASR'}

# Mapping name mismatches: dir_name -> correct name
NAME_FIXES = {
    'agent-browser': 'agent-browser',
    'ai-news-collectors': 'ai-news-collectors',
    'design': 'design',
    'podcast-generate': 'podcast-generate',
    'pptx': 'pptx',
    'qingyan-research': 'qingyan-research',
    'stock-analysis-skill': 'stock-analysis-skill',
    'version-management': 'version-management',
    'video-generation': 'video-generation',
}

stats = {'scanned': 0, 'modified': 0, 'name_fixed': 0, 'version_fixed': 0, 'fields_added': 0, 'skipped': 0}


def extract_frontmatter(content):
    """Extract (frontmatter_dict, body) from SKILL.md content."""
    if not content.startswith('---'):
        return None, content
    try:
        end = content.index('---', 3)
    except ValueError:
        return None, content
    fm_raw = content[3:end].strip()
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        fm = {}
    body = content[end + 3:].lstrip('\n')
    return fm, body


def build_frontmatter(fm, dir_name):
    """Build a compliant frontmatter, preserving existing valid fields."""
    changed = False

    # Fix name mismatch
    if 'name' in fm:
        expected = NAME_FIXES.get(dir_name, dir_name)
        if fm['name'].lower().replace('_', '-') != expected.lower().replace('_', '-'):
            fm['name'] = expected
            stats['name_fixed'] += 1
            changed = True
    else:
        fm['name'] = dir_name
        stats['fields_added'] += 1
        changed = True

    # Fix version
    if 'version' not in fm:
        fm['version'] = '1.0.0'
        stats['fields_added'] += 1
        changed = True
    else:
        ver = str(fm['version'])
        # Handle Z.AI metadata.version pattern: if version is nested or not semver
        if 'metadata' in fm and isinstance(fm['metadata'], dict):
            meta_ver = fm['metadata'].get('version', '')
            if meta_ver and re.match(r'^\d+\.\d+$', str(meta_ver)):
                fm['version'] = str(meta_ver) + '.0'
                del fm['metadata']
                stats['version_fixed'] += 1
                changed = True
        elif not re.match(r'^\d+\.\d+\.\d+$', ver):
            # Try to fix common patterns like "1.0" -> "1.0.0"
            if re.match(r'^\d+\.\d+$', ver):
                fm['version'] = ver + '.0'
                stats['version_fixed'] += 1
                changed = True

    # Add missing standard fields
    if 'category' not in fm:
        fm['category'] = 'metier'
        stats['fields_added'] += 1
        changed = True

    if 'language' not in fm:
        fm['language'] = 'fr'
        stats['fields_added'] += 1
        changed = True

    if 'tags' not in fm or not isinstance(fm.get('tags'), list):
        fm['tags'] = []
        stats['fields_added'] += 1
        changed = True

    if 'dependencies' not in fm:
        fm['dependencies'] = []
        stats['fields_added'] += 1
        changed = True

    return fm, changed


def to_yaml(fm):
    """Serialize frontmatter dict to YAML string."""
    lines = ['---']
    # Order: name, version, category, language, description, tags, dependencies, then rest
    order = ['name', 'version', 'category', 'language', 'description', 'tags', 'dependencies']
    written = set()
    for key in order:
        if key in fm:
            val = fm[key]
            if isinstance(val, str) and '\n' in val:
                lines.append(f'{key}: >')
                for line in val.split('\n'):
                    lines.append(f'  {line}')
            elif isinstance(val, list):
                if not val:
                    lines.append(f'{key}: []')
                else:
                    lines.append(f'{key}:')
                    for item in val:
                        lines.append(f'  - {item}')
            elif isinstance(val, dict):
                lines.append(f'{key}:')
                for k2, v2 in val.items():
                    lines.append(f'  {k2}: {v2}')
            else:
                lines.append(f'{key}: {val}')
            written.add(key)
    # Remaining keys
    for key, val in fm.items():
        if key not in written:
            if isinstance(val, list):
                if not val:
                    lines.append(f'{key}: []')
                else:
                    lines.append(f'{key}:')
                    for item in val:
                        lines.append(f'  - {item}')
            elif isinstance(val, dict):
                lines.append(f'{key}:')
                for k2, v2 in val.items():
                    lines.append(f'  {k2}: {v2}')
            else:
                lines.append(f'{key}: {val}')
    lines.append('---')
    return '\n'.join(lines)


def process_skill(dir_name):
    """Process one skill directory. Returns (status, details)."""
    skill_path = os.path.join(SKILLS_ROOT, dir_name, 'SKILL.md')
    if not os.path.isfile(skill_path):
        return 'skip', 'no SKILL.md'

    stats['scanned'] += 1
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm, body = extract_frontmatter(content)
    if fm is None:
        # No frontmatter at all — create one
        # Try to extract description from first non-empty line
        first_line = ''
        for line in body.split('\n'):
            line = line.strip().lstrip('#').strip()
            if line and len(line) > 20:
                first_line = line[:500]
                break
        new_fm = {
            'name': dir_name,
            'version': '1.0.0',
            'category': 'metier',
            'language': 'fr',
            'tags': [],
            'description': first_line,
            'dependencies': [],
        }
        new_content = to_yaml(new_fm) + '\n\n' + body
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        stats['modified'] += 1
        stats['fields_added'] += 7
        return 'created', 'frontmatter created from scratch'

    # Existing frontmatter — fill gaps
    new_fm, changed = build_frontmatter(fm, dir_name)
    if not changed:
        stats['skipped'] += 1
        return 'ok', 'already compliant'

    new_content = to_yaml(new_fm) + '\n\n' + body
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    stats['modified'] += 1
    details = []
    if stats['name_fixed'] > 0: details.append('name fixed')
    return 'fixed', '; '.join(details) if details else 'fields added'


def main():
    print('Phase 2 — Standardisation frontmatter métier\n')
    for d in sorted(os.listdir(SKILLS_ROOT)):
        if d.startswith('_') or d in ECOSYSTEM:
            continue
        if not os.path.isdir(os.path.join(SKILLS_ROOT, d)):
            continue
        status, detail = process_skill(d)
        if status != 'ok':
            print(f'  [{status:7s}] {d:35s} — {detail}')

    print(f'\n{stats["="]*50}')
    print(f'RÉSULTATS')
    print(f'{"="*50}')
    print(f'  Scannés   : {stats["scanned"]}')
    print(f'  Modifiés  : {stats["modified"]}')
    print(f'  Intouchés : {stats["skipped"]}')
    print(f'  Noms fixés: {stats["name_fixed"]}')
    print(f'  Versions fixées: {stats["version_fixed"]}')
    print(f'  Champs ajoutés: {stats["fields_added"]}')


if __name__ == '__main__':
    main()