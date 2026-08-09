#!/usr/bin/env python3
"""Install gen-plan v3.6.0 from prompt maître into skills directory."""

import re
import os

BASE = "/home/z/my-project"
PROMPT = os.path.join(BASE, "download", "PROMPT-MAITRE-GEN-PLAN-v3.6.0.md")
SKILLS_ROOT = os.path.join(BASE, "skills")
GEN_PLAN_DIR = os.path.join(SKILLS_ROOT, "gen-plan")
REFS_DIR = os.path.join(GEN_PLAN_DIR, "references")
EVALS_DIR = os.path.join(GEN_PLAN_DIR, "evals")

with open(PROMPT) as f:
    content = f.read()

# Extract fenced code blocks under §9.1-§9.5
pattern = r'### §9\.(\d) `([^`]+)`\s*\n```markdown\n(.*?)```'
matches = re.findall(pattern, content, re.DOTALL)

print(f"Fichiers référence trouvés : {len(matches)}")

for num, filename, body in matches:
    # Remove 'references/' prefix if present in the filename
    clean_name = filename.replace('references/', '')
    filepath = os.path.join(REFS_DIR, clean_name)
    with open(filepath, 'w') as f:
        f.write(body.strip() + '\n')
    print(f"  Créé : {filepath} ({len(body.strip().splitlines())} lignes)")

# Extract evals.json block (after §5.4)
evals_pattern = r'### §5\.4.*?```json\n(.*?)```'
evals_match = re.search(evals_pattern, content, re.DOTALL)
if evals_match:
    evals_path = os.path.join(EVALS_DIR, "evals.json")
    with open(evals_path, 'w') as f:
        f.write(evals_match.group(1).strip() + '\n')
    print(f"  Créé : {evals_path}")

print("\nTerminé.")
