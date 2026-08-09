#!/usr/bin/env python3
"""correct-work Mode PROJET — Vérification du dépôt GitHub KNOWLEDGE

Vérifie que le contenu pushé sur GitHub est cohérent, complet et sans
fichiers indésirables.
"""

import os
import subprocess
import sys

findings = []

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/home/z/my-project')
    return r.stdout.strip()

def add(sev, target, desc):
    findings.append((sev, target, desc))

def check_sensitive():
    print('=== CIBLE 1 : FICHIERS SENSIBLES ===')
    # .env
    env = run('git ls-tree -r --name-only HEAD | grep -E "^\\.env$"')
    if env:
        add('S1', '.env', '.env est tracké dans le dépôt')
        print(f'  [S1 FAIL] .env présent dans le dépôt')
    else:
        print(f'  [PASS] .env absent du dépôt')

    # Tokens
    token_files = run('git ls-tree -r --name-only HEAD | grep -iE "(token|secret|credential|private|api.key)"')
    if token_files:
        for tf in token_files.split('\n'):
            if tf:
                add('S1', tf, 'Fichier sensible potentiel')
        print(f'  [S1 FAIL] Fichiers sensibles détectés')
    else:
        print(f'  [PASS] Aucun fichier sensible')

def check_gitignore():
    print('\n=== CIBLE 2 : .gitignore ===')
    with open('.gitignore') as f:
        gi = f.read()
    
    # skills/ ne doit PAS être exclu
    if 'skills/' in gi:
        add('S1', '.gitignore', 'skills/ est exclu par .gitignore')
        print(f'  [S1 FAIL] skills/ est encore exclu')
    else:
        print(f'  [PASS] skills/ nest pas exclu')
    
    # Exclusions requises
    required = {'.env', 'tool-results', 'upload', 'node_modules'}
    for r in required:
        if r in gi:
            print(f'  [PASS] {r} bien exclu')
        else:
            add('S2', '.gitignore', f'{r} manquant dans .gitignore')
            print(f'  [S2 FAIL] {r} manquant')
    
    # Vérifier que les exclusions sont effectives
    for d in ['tool-results/', 'upload/']:
        tracked = run(f'git ls-tree -r --name-only HEAD | grep "^{d}"')
        if tracked:
            add('S2', d, f'{d} encore tracké malgré .gitignore')
            print(f'  [S2 FAIL] {d} encore dans le dépôt')
        else:
            print(f'  [PASS] {d} absent du dépôt')

def check_skills_tree():
    print('\n=== CIBLE 3 : ARBORESCENCE skills/ ===')
    tracked_skills = run('git ls-tree -r --name-only HEAD | grep "^skills/" | grep "/SKILL.md$" | sed "s|skills/||;s|/SKILL.md||" | sort')
    skills = [s for s in tracked_skills.split('\n') if s]
    count = len(skills)
    
    print(f'  Skills trouvés : {count}')
    
    if count < 70:
        add('S1', 'skills/', f' seulement {count}/78 skills')
    elif count < 78:
        add('S3', 'skills/', f'{count}/78 skills (manquants possibles)')
    else:
        print(f'  [PASS] {count} skills présents')
    
    # Vérifier les 6 skills écosystème
    ecosystem = ['gen-plan', 'correct-work', 'clone-chat', 'autonomous-agent', 'skills-inventory', 'skill-creator']
    for s in ecosystem:
        path = f'skills/{s}/SKILL.md'
        exists = run(f'git ls-tree -r --name-only HEAD | grep "^{path}$"')
        if exists:
            print(f'  [PASS] {s}/SKILL.md présent')
        else:
            add('S1', path, f'Skill écosystème {s} manquant')
            print(f'  [S1 FAIL] {s}/SKILL.md MANQUANT')
    
    # Vérifier KNOWLEDGE.md
    kb = run('git ls-tree -r --name-only HEAD | grep "^skills/KNOWLEDGE.md$"')
    if kb:
        print(f'  [PASS] skills/KNOWLEDGE.md présent')
    else:
        add('S1', 'skills/KNOWLEDGE.md', 'Registre KB manquant')
        print(f'  [S1 FAIL] skills/KNOWLEDGE.md MANQUANT')
    
    # Vérifier _prompts-maitres/
    pm_dir = run('git ls-tree -r --name-only HEAD | grep "^skills/_prompts-maitres/"')
    pm_files = [f for f in pm_dir.split('\n') if f]
    if len(pm_files) >= 5:
        print(f'  [PASS] _prompts-maitres/ : {len(pm_files)} fichiers')
    else:
        add('S2', '_prompts-maitres/', f'Seulement {len(pm_files)} fichiers')

def check_obsolete_files():
    print('\n=== CIBLE 4 : FICHIERS OBSOLÈTES ===')
    # Vérifier que les old versions ne sont pas dans download/
    old = ['PROMPT-MAITRE-GEN-PLAN-v3.6.0.md', 'PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md']
    for o in old:
        path = f'download/{o}'
        tracked = run(f'git ls-tree -r --name-only HEAD | grep "^{path}$"')
        if tracked:
            add('S3', path, f'Version obsolète présente : {o}')
            print(f'  [S3 FAIL] {o} encore dans download/')
        else:
            print(f'  [PASS] {o} absent')
    
    # Vérifier les versions actuelles sont présentes
    current = ['PROMPT-MAITRE-GEN-PLAN-v3.6.1.md', 'PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md',
               'PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md', 'PROMPT-MAITRE-SHARED.md', 'README.md']
    for c in current:
        path = f'download/{c}'
        tracked = run(f'git ls-tree -r --name-only HEAD | grep "^{path}$"')
        if tracked:
            print(f'  [PASS] {c} présent')
        else:
            add('S2', path, f'Fichier manquant dans download/ : {c}')
            print(f'  [S2 FAIL] {c} MANQUANT')

def check_scripts():
    print('\n=== CIBLE 5 : SCRIPTS DE VÉRIFICATION ===')
    scripts = ['scripts/verify-cross.py', 'scripts/sync-download.py', 'scripts/audit-gen-plan-versions.py', 'scripts/spell-check.py']
    for s in scripts:
        tracked = run(f'git ls-tree -r --name-only HEAD | grep "^{s}$"')
        if tracked:
            print(f'  [PASS] {s} présent')
        else:
            add('S3', s, 'Script de vérification manquant')
            print(f'  [S3 FAIL] {s} MANQUANT')

def check_download_sync():
    print('\n=== CIBLE 6 : SYNCHRONISATION download/ ===')
    import filecmp
    pairs = [
        ('skills/_prompts-maitres/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md', 'download/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md'),
        ('skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md', 'download/PROMPT-MAITRE-SHARED.md'),
        ('skills/_prompts-maitres/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md', 'download/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md'),
        ('skills/_prompts-maitres/PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md', 'download/PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md'),
        ('skills/_prompts-maitres/README.md', 'download/README.md'),
    ]
    for src, dst in pairs:
        if os.path.exists(src) and os.path.exists(dst):
            if filecmp.cmp(src, dst, shallow=False):
                print(f'  [PASS] {os.path.basename(dst)} sync')
            else:
                add('S3', dst, f'{os.path.basename(dst)} non synchronisé')
                print(f'  [S3 FAIL] {os.path.basename(dst)} DIFFÈRE')
        else:
            add('S2', dst, f'Fichier manquant : {dst}')

def check_worklog():
    print('\n=== CIBLE 7 : WORKLOG ===')
    tracked = run('git ls-tree -r --name-only HEAD | grep "^worklog.md$"')
    if tracked:
        size = os.path.getsize('worklog.md')
        lines = size // 80  # approx
        print(f'  [PASS] worklog.md présent ({size} octets)')
    else:
        add('S4', 'worklog.md', 'worklog.md absent du dépôt')
        print(f'  [S4 FAIL] worklog.md MANQUANT')

# --- Exécution ---
print('╔══════════════════════════════════════════════════════════════╗')
print('║  correct-work PROJET — github.com/bigleon2/KNOWLEDGE.git   ║')
print('║  7 cibles, mode PROJET, profil NORMAL                       ║')
print('╚══════════════════════════════════════════════════════════════╝\n')

check_sensitive()
check_gitignore()
check_skills_tree()
check_obsolete_files()
check_scripts()
check_download_sync()
check_worklog()

# --- Rapport ---
print('\n' + '='*60)
print('RAPPORT correct-work')
print('='*60)

s1 = [(t, d) for s, t, d in findings if s == 'S1']
s2 = [(t, d) for s, t, d in findings if s == 'S2']
s3 = [(t, d) for s, t, d in findings if s == 'S3']
s4 = [(t, d) for s, t, d in findings if s == 'S4']

print(f'\n  S1 (Critique)  : {len(s1)}')
print(f'  S2 (Majeur)     : {len(s2)}')
print(f'  S3 (Mineur)     : {len(s3)}')
print(f'  S4 (Suggestion) : {len(s4)}')
print(f'  TOTAL           : {len(findings)}')

if findings:
    print(f'\n  DÉTAIL :')
    for s, t, d in findings:
        print(f'    [{s}] {t} — {d}')

print()
if len(s1) > 0:
    verdict = 'FAIL'
elif len(s2) > 0:
    verdict = 'PASS AVEC RÉSERVES'
else:
    verdict = 'PASS'

print(f'  VERDICT : {verdict}')
sys.exit(0 if verdict == 'PASS' else 1)
