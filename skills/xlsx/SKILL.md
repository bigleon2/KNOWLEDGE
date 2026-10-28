---
name: xlsx
metadata:
  author: Z.AI
  version: "1.0"
description: "Utilisez cette compétence chaque fois qu'un fichier de feuille de calcul est l'entrée ou la sortie principale. Cela signifie toute tâche où l'utilisateur souhaite : ouvrir, lire, modifier ou corriger un fichier existant .xlsx, .xlsm, .csv ou .tsv ; créer une nouvelle feuille de calcul à partir de zéro ou à partir d'autres sources de données ; analyser des données et exporter les résultats sous forme de fichier Excel avec des graphiques ; convertir entre les formats de fichiers tabulaires (CSV/JSON/PDF → XLSX ou vice versa) ; nettoyer, fusionner, pivoter ou transformer des données tabulaires. Déclenchez particulièrement lorsque l'utilisateur fait référence à un fichier de feuille de calcul par son nom ou son chemin, dit 'crée un tableau/rapport/modèle', mentionne Excel/CSV/dànjù fēnxī/bàobiǎo/huìzǒng, ou souhaite une visualisation de données dans une feuille de calcul."
license: Proprietary. LICENSE.txt has complete terms
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# XLSX — Scene-Driven Spreadsheet Workbench

## Quick Setup

```bash
bash "$XLSX_SKILL_DIR/setup.sh"    # Interactive environment check + install
```
## Pre-Flight: Intent Gate

Before touching any code, confirm the user actually needs a spreadsheet:

- Report / analysis summary (shuzhi, diaoyan baogao) → **docx skill**
- Presentation (hui bao, yan shi, pitch deck) → **pptx skill**
- Formal print document (he tong, zheng shu, "PDF") → **pdf skill**
- Charts only, no data table needed → **charts skill**
- User explicitly says a format → respect it

If confirmed xlsx → proceed to Scene Router below.

**Request Decomposition** (do this every time):
- **Explicit needs**: sheets, columns, formulas, metrics the user stated
- **Implicit needs**: business context, downstream use (filter? sort? input?)
- **Multi-part requests**: generate ALL parts — never silently drop a component

**Multi-Intent Detection** — some requests combine multiple scenes:

```
"Create a financial model with charts and export a PDF summary"
 → scenes/finance.md + engines/chart.md + (hand off PDF to pdf skill)

"Analyze this CSV, build a dashboard, and make it look professional"
 → scenes/analyze.md + engines/chart.md + engines/design.md

"Edit this budget file, add a new quarter column, and create a pivot"
 → scenes/edit.md + quality/pipeline.md (pivot command)

"Convert these 5 CSVs into one xlsx with a summary sheet"
 → scenes/convert.md + scenes/create.md (for summary)
```

When multiple intents detected, load all matching files and execute in logical order: data preparation → analysis → visualization → styling → QA.

---

## Complexity Gate (evaluate BEFORE Scene Router)

Determine task complexity to control file loading depth:

```
User Request
│
├─ LITE (single aggregation, simple chart, direct conversion, QA-only)
│  → Load: SKILL.md + ONE scene file (lean version)
│  → Skip: engine files (use built-in knowledge for basic styles)
│  → QA: audit + validate only
│  → Target: ≤ 400 lines total context
│
└─ FULL (multi-dimensional analysis, financial model, dashboard, KANO, etc.)
   → Load: SKILL.md + scene + engines (chart.md / design.md) as needed
   → For code patterns: load recipes/templates files ON DEMAND (not upfront)
   → QA: full pipeline (recalc → audit → scan → chart-verify → validate)
   → Target: load recipes/templates only when stuck on implementation
```

**LITE triggers**: single groupby, one chart, format conversion, inspect/audit/validate, simple pivot
**FULL triggers**: correlation matrix, multi-sheet dashboard, statistical analysis, financial model, KANO/funnel/cohort

---

## Scene Router

```
User Request
│
├─ Involves an existing file?
│  ├─ Yes → Modify content or structure?
│  │         ├─ Yes ──────────────────── → scenes/edit.md
│  │         └─ No (read/analyze only) ─ → scenes/analyze.md
│  │
│  └─ Format conversion (CSV↔XLSX, JSON, PDF tables)?
│     └─ Yes ────────────────────────── → scenes/convert.md
│
├─ Create from scratch?
│  ├─ Financial / budget / forecast / cost tracking?
│  │  ├─ Complex (DCF / LBO / three-statement linkage (sān biǎo lián dòng) / sensitivity / IB model)?
│  │  │  └─ Yes ─────────────────────── → scenes/finance.md
│  │  └─ Simple (budget table (yusuan biao) / expense report (feiyong baobiao) / revenue vs cost (shouzhi dui bi) / project cost (xiangmu chengben) / personal finance (geren jizhang))?
│  │     └─ Yes ─────────────────────── → scenes/finance_lite.md
│  └─ General table / report / template
│     └─ ──────────────────────────── → scenes/create.md
│
├─ Batch processing / large files / protection / validation?
│  └─ Yes ───────────────────────────── → scenes/advanced.md
│
├─ VBA / macros / automation inside Excel?
│  └─ Yes ───────────────────────────── → scenes/vba.md + engines/vba-templates.md
│
├─ Needs charts or data visualization?
│  └─ Yes ───────────── append ────────→ engines/chart.md
│
└─ Needs styling / design system?
   └─ Yes ───────────── append ────────→ engines/design.md
```

**Mixed requests**: load all matching files. Engine files always **append** to a scene.

**Finance detection**:
- **finance.md** (complex): DCF, LBO, P&L, 利润表 (lirun biao), 资产负债 (zichan fuzhai), valuation, 估值 (guzhi), IRR, 三表联动 (sanbiao liandong), sensitivity, scenario
- **finance_lite.md** (simple): 预算 (yusuan), budget, 费用 (feiyong), expense, 收支 (shouzhi), 记账 (jizhang), 项目成本 (xiangmu chengben), cost tracking, 报销 (baoxiao), ROI

**VBA detection**: 宏 (hong), macro, VBA, 自动化 (zidonghua), automation, .xlsm, 按钮 (anniu), button, auto-run, 批量处理脚本 (piliang chuli juben)

---

## Design Principles

### 1. Live Formula Guarantee
Every derived value SHOULD be an Excel formula so the spreadsheet stays dynamic.

**Exception — Programmatic Verification**: When the output file will be verified by Python (not opened in Excel), TOTAL/SUM rows should write **computed values** instead of formulas, because openpyxl cannot evaluate formulas and `data_only=True` returns `None` for newly-written formulas. Optionally add the formula as a cell comment for reference.

### 2. Zero Error Tolerance
Deliverables must have zero formula errors. All divisions wrapped with `IFERROR` or `IF(denom=0,...)`. Absolute references (`$C$42`) for shared denominators.

### 3. Compatibility First
No dynamic array functions (`FILTER`, `UNIQUE`, `XLOOKUP`, `SORT`, `SORTBY`, `XMATCH`, `SEQUENCE`, `LET`, `LAMBDA`, `RANDARRAY`). No implicit array formulas — use `SUMPRODUCT` alternatives.

### 4. Preserve & Match
When editing existing files: study and exactly match format, style, conventions. Existing patterns always override defaults. Text starting with `=` must be prefixed with `'`.

### 5. Language Mirror
Output language (sheet names, headers, labels) matches user's input language.

### 6. Data Consistency Over Instructions
When user instructions conflict with the actual data patterns in the existing file:
- **First priority**: match the existing data pattern (e.g., if existing data uses `0` for empty, don't switch to `-`)
- **Second priority**: follow user instructions literally
- Always flag the conflict to the user

Example: User says "show hyphen for zero" but existing data and answer key use numeric `0` → Use `0` and notify user of the discrepancy.

---

## Toolchain

### Script Path Setup (MANDATORY before any script call)

All CLI tools live relative to this skill's directory. Before calling any script, resolve the absolute path once:

```bash
XLSX_SKILL_DIR="<skill_directory>"   # ← parent directory of this SKILL.md

# Then all commands use absolute paths:
python3 "$XLSX_SKILL_DIR/xlsx.py" inspect data.xlsx --pretty
python3 "$XLSX_SKILL_DIR/xlsx.py" pivot data.xlsx output.xlsx --rows Region --values Revenue
python3 "$XLSX_SKILL_DIR/xlsx.py" validate output.xlsx
```

**For Python imports** (when generation code needs to import skill modules):

```python
import sys, os
XLSX_SKILL_DIR = "<skill_directory>"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)
```

**⚠️ NEVER use bare `python3 xlsx.py ...`** — it only works if cwd happens to be the skill directory. Always use the absolute path.

### Tool Reference

| Tool | Use |
|------|-----|
| **openpyxl** | Formulas, formatting, charts, cell-level control |
| **pandas** | Data analysis, bulk operations, CSV/TSV |
| `load_workbook(read_only=True)` | Large file reads |
| `Workbook(write_only=True)` | Large file writes |
| **templates/base.py** | Design tokens, font resolution, style factories, utilities (single source of truth) |
| **xlsx.py** | QA commands (see `quality/pipeline.md`) |

Workbook metadata: `wb.properties.creator = "Z.ai"`

> **All code must import from `templates/base.py`** for colors, fonts, and style helpers. Never hardcode hex values or font names.

---

## Quality Gate

Every deliverable must pass the full integrity pipeline before delivery.

→ **Load `quality/pipeline.md` for the role-based integrity workflow.**

Quick reference:
```
Blueprint → Build & Self-check (per-sheet) → Inspect → Pivot (if needed) → Release
```

---

## Capability Matrix

| Capability | Supported | Scene/Engine |
|-----------|-----------|-------------|
| Create from scratch | ✅ | scenes/create |
| Edit existing file | ✅ | scenes/edit |
| Data analysis & EDA | ✅ | scenes/analyze |
| Format conversion | ✅ | scenes/convert |
| Financial models (DCF/LBO/P&L) | ✅ | scenes/finance |
| Simple budgets & expenses | ✅ | scenes/finance_lite |
| VBA macros & automation | ✅ | scenes/vba + engines/vba-templates |
| Batch processing | ✅ | scenes/advanced |
| Embedded charts | ✅ | engines/chart |
| Smart chart recommendation | ✅ | engines/chart |
| Design system & styling | ✅ | engines/design |
| PivotTable creation | ✅ | quality/pipeline (pivot cmd) |
| Formula validation | ✅ | quality/pipeline |
| Structural validation | ✅ | quality/pipeline |
| Data provenance tracking | ✅ | scenes/analyze |
| Large file handling | ✅ | scenes/advanced |
| Data protection & locking | ✅ | scenes/advanced |
