---
description: AMiner recommandation d'articles personnalisée (AMiner Personalized Paper Recommendation) — par sujet ou profil de chercheur (By Topic or Scholar Profile)
argument-hint: [topics: sujet1, sujet2 | scholar: nom org: institution | langage naturel]
allowed-tools: Read, Bash, Glob, Grep
---

# /aminer-dp — AMiner Daily Paper

User invoked the AMiner daily paper recommendation skill with the following arguments:

```
$ARGUMENTS
```

## Your task

Strictly follow `${CLAUDE_PLUGIN_ROOT}/SKILL.md` (English) or `${CLAUDE_PLUGIN_ROOT}/SKILL.zh.md` (Chinese). Key rules summarized below — but read the SKILL file if you need detail.

### 1. Pre-flight

Verify the `AMINER_API_KEY` env var is set:

```bash
[ -z "${AMINER_API_KEY+x}" ] && echo "AMINER_API_KEY missing" || echo "AMINER_API_KEY exists"
```

If missing, stop and tell the user to set it (token from <https://open.aminer.cn>). Do not call the script.

### 2. Parse `$ARGUMENTS` into structured fields

Extract any of: `topics`, `scholar` / `author_name`, `org` / `author_org`, `papers`, `size`, `language_sort`.

**Critical rules — do NOT violate:**

- **`topics`** : conservez la formulation exacte de l'utilisateur. S'ils ont écrit `具身智能, 环境保护` (jushen zhineng, huanjing baohu), transmettez ces chaînes chinoises. **Ne les traduisez jamais** en champs anglais non liés (par exemple, ne les mappez pas à "Knowledge Distillation" ou "Smart agriculture"). Si vous ajoutez un alias anglais, il doit être une traduction fidèle du même concept (par exemple, 具身智能 → intelligence incarnée).
- **`language_sort`** : incluez `zh` ou `en` **uniquement lorsque l'utilisateur demande explicitement** un classement biaisé chinois/anglais (par exemple, "prioriser les articles en chinois" / "préférer les articles en anglais"). Sinon, omez-le entièrement.
- **`scholar` / `org`**: use English-canonical names where reasonable (e.g. `Jie Tang`, `Tsinghua University`). If a Chinese name is ambiguous and no org is given, ask the user before guessing.
- If `$ARGUMENTS` is empty, call the script with no extra fields — the API will return personalized recs based on the API key.

### 3. Run the entrypoint

Reconstruct the trigger and execute (one call per topic group; ≤3 closely related terms per group):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/handle_trigger.py" \
  --base-dir "${CLAUDE_PLUGIN_ROOT}" \
  --text "/aminer-dp <reconstructed fields>"
```

### 4. Present the result

Parse the JSON output. When `final_response == "TEXT"`, render the `reply_text` (Markdown) directly to the user. On error, surface the error message; do not fall back to other skills.
