#!/usr/bin/env python3
"""Fix YAML parse errors in frontmatter — quote unquoted colons in description values."""
import os, re, yaml

SKILLS = '/home/z/my-project/skills'
ECOSYSTEM = {'gen-plan','correct-work','clone-chat','skills-inventory','skill-creator','autonomous-agent'}
BROKEN = []

for d in sorted(os.listdir(SKILLS)):
    p = os.path.join(SKILLS, d, 'SKILL.md')
    if not os.path.isfile(p) or d.startswith('_') or d in ECOSYSTEM: continue
    with open(p, 'r', encoding='utf-8') as f: c = f.read()
    if not c.startswith('---'): continue
    try:
        end = c.index('---', 3)
        yaml.safe_load(c[3:end])
    except Exception:
        BROKEN.append(d)

print(f'Skills avec YAML cassé : {len(BROKEN)}')
for d in BROKEN: print(f'  - {d}')

# Fix: rewrite frontmatter using raw string reconstruction
# instead of yaml.dump to avoid quoting issues
for d in BROKEN:
    p = os.path.join(SKILLS, d, 'SKILL.md')
    with open(p, 'r', encoding='utf-8') as f: content = f.read()
    end = content.index('---', 3)
    fm_raw = content[3:end].strip()
    body = content[end+3:].lstrip('\n')
    
    # Parse line by line to extract fields
    fields = {}
    current_key = None
    current_val_lines = []
    desc_block = False
    
    for line in fm_raw.split('\n'):
        if line.startswith('description:') and '>' not in line:
            # description: unquoted text with colons — wrap in quotes
            val = line[len('description:'):].strip()
            if val and not val.startswith('"') and not val.startswith("'"):
                fields['description'] = val
                desc_block = True
            else:
                fields['description'] = val
                desc_block = False
        elif desc_block:
            if line.startswith('  ') or line == '':
                fields['description'] += '\n' + line
            else:
                desc_block = False
                m = re.match(r'^(\w[\w-]*):\s*(.*)', line)
                if m:
                    fields[m.group(1)] = m.group(2).strip()
        else:
            m = re.match(r'^(\w[\w-]*):\s*(.*)', line)
            if m:
                fields[m.group(1)] = m.group(2).strip()
    
    # Build compliant frontmatter
    lines = ['---']
    lines.append(f"name: {fields.get('name', d)}")
    lines.append(f"version: {fields.get('version', '1.0.0')}")
    lines.append(f"category: {fields.get('category', 'metier')}")
    lines.append(f"language: {fields.get('language', 'fr')}")
    
    desc = fields.get('description', '')
    # Always quote description to avoid YAML issues
    if desc:
        # Use folded scalar for multi-line, quoted for single
        if '\n' in desc:
            lines.append('description: >')
            for dl in desc.strip().split('\n'):
                lines.append(f'  {dl}')
        else:
            lines.append(f'description: "{desc.replace(chr(34), chr(39))}"')
    else:
        lines.append('description: >')
        lines.append('  (no description)')
    
    # tags and dependencies as arrays
    tags = fields.get('tags', '[]')
    if tags in ('[]', ''):
        lines.append('tags: []')
    else:
        lines.append(f'tags: {tags}')
    
    deps = fields.get('dependencies', '[]')
    if deps in ('[]', ''):
        lines.append('dependencies: []')
    else:
        lines.append(f'dependencies: {deps}')
    
    # Any extra fields
    for k in ['argument-hint', 'metadata']:
        if k in fields and fields[k]:
            lines.append(f'{k}: {fields[k]}')
    
    lines.append('---')
    new_content = '\n'.join(lines) + '\n\n' + body
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  FIXED: {d}')

# Verify
print(f'\nVérification post-fix...')
still_broken = 0
for d in sorted(os.listdir(SKILLS)):
    p = os.path.join(SKILLS, d, 'SKILL.md')
    if not os.path.isfile(p) or d.startswith('_') or d in ECOSYSTEM: continue
    with open(p) as f: c = f.read()
    if not c.startswith('---'): continue
    try:
        end = c.index('---', 3)
        yaml.safe_load(c[3:end])
    except Exception:
        still_broken += 1
        print(f'  STILL BROKEN: {d}')
print(f'Still broken: {still_broken}')
