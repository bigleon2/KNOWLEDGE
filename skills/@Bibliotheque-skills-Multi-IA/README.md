# bibliotheque-skills-ia — @processus multi-plateformes

> **Version** : 1.0.0 · **Task 39 / G3** — convergence $facon de la
> bibliothèque créée dans la discussion L2 (TSI_Generator v7.7.9) :
> core unique + déclinaisons générées (6 plateformes).

```
bibliotheque-skills-ia/
├── core/processus.md          # source de vérité unique (5 processus)
├── platforms/                 # GÉNÉRÉ — ne pas éditer
│   ├── qwen/claude/chatgpt/copilot/perplexity/gemini/prompt_systeme.md
├── tools/generate_prompts.py  # générateur déterministe (×2 identiques)
└── validation_checklist.md    # pré-flight avant déclaration de fin
```

**Ancrage écosystème (R4 — pas de duplication)** : dans l'écosystème
KNOWLEDGE, chaque processus délègue au skill existant (correct-py,
refactoring-engineering, skill-creator, charts, script-creator) — voir la
table de correspondance dans `core/processus.md`.

**Régénération** : `python3 tools/generate_prompts.py`
