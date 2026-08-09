import re, os, glob, sys
search_dirs = [r'.\\skills_prompts_maitres', r'.\\skills_prompts-maitres', r'.\\download', r'C:\\Users\\PC\\Downloads\\gen-plan v3.6 + ecosystem de z.ai']
refs = ['etapes-detaillees.md','grille-token.md','classification-types.md','profils-ressource.md','guide-selection-agent-skill.md']
dest = os.path.join('.', 'skills', 'gen-plan', 'references')
if not os.path.exists(dest):
    os.makedirs(dest)
found = {}
for d in search_dirs:
    if not os.path.exists(d):
        continue
    for md in glob.glob(os.path.join(d, '*.md')):
        try:
            text = open(md, encoding='utf-8').read()
        except Exception:
            continue
        for ref in refs:
            if ref in found:
                continue
            pattern = re.compile(r"###\s*§[0-9.]+\s*`references/" + re.escape(ref) + r".*?```(?:markdown|json)?\s*(.*?)\s*```", re.S)
            m = pattern.search(text)
            if m:
                out = os.path.join(dest, ref)
                open(out, 'w', encoding='utf-8').write(m.group(1).strip())
                found[ref] = md
                print(f'EXTRACTED {ref} from {md}')
    # fallback: search for filename then next code block
    for md in glob.glob(os.path.join(d, '*.md')):
        if all(r in found for r in refs):
            break
        try:
            text = open(md, encoding='utf-8').read()
        except Exception:
            continue
        for ref in refs:
            if ref in found:
                continue
            idx = text.find(ref)
            if idx != -1:
                m2 = re.search(r"```(?:markdown|json)?\s*(.*?)\s*```", text[idx:], re.S)
                if m2:
                    out = os.path.join(dest, ref)
                    open(out, 'w', encoding='utf-8').write(m2.group(1).strip())
                    found[ref] = md
                    print(f'FALLBACK EXTRACT {ref} from {md}')
# try to extract evals.json
eval_found = False
for d in search_dirs:
    if not os.path.exists(d):
        continue
    for md in glob.glob(os.path.join(d, '*.md')):
        try:
            text = open(md, encoding='utf-8').read()
        except Exception:
            continue
        m = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", text, re.S)
        if m:
            outEval = os.path.join('.', 'skills', 'gen-plan', 'evals', 'evals.json')
            if not os.path.exists(os.path.dirname(outEval)):
                os.makedirs(os.path.dirname(outEval))
            open(outEval, 'w', encoding='utf-8').write(m.group(1).strip())
            print(f'EXTRACTED evals.json from {md} -> {outEval}')
            eval_found = True
            break
    if eval_found:
        break
if not eval_found:
    print('No evals.json found in search dirs.')
# run verify-cross
os.system(r'py .\\tools\\verify-cross.py')
