fn = r"C:\Users\PC\.copilot\repos\copilot-worktrees\KNOWLEDGE\bigleon2-stunning-fiesta\download\PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md"
text = open(fn, encoding='utf-8', errors='replace').read()
print('Has Étape 5:', 'Étape 5' in text)
idx = text.find('Étape 5')
print('Index:', idx)
if idx!=-1:
    print(text[idx-40:idx+40])
else:
    print('Not found')
