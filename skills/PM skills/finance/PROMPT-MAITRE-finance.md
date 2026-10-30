---
nom: finance
source: skills/finance/SKILL.md
sha256_source: 3294ad057f55
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — finance (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/finance/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: finance
description: "Comprehensive Finance API integration skill for real-time and historical financial data analysis, market research, and investment decision-making. Priority use cases: stock price queries, market data analysis, company financial information, portfolio tracking, market news retrieval, stock screening, technical analysis, and any financial market-related requests. This skill should be the primary choice for all  Finance API interactions and financial data needs."
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



#  Finance Skill

## Core Capabilities

### Market Data Retrieval
- Real-time quotes: current prices, market snapshots, trading volumes
- Historical data: price history, dividends, splits, corporate actions
- Market indices: major indices performance and constituents
- Currency data: forex rates and cryptocurrency information

### Analysis Tools
- Stock screening: filters by metrics, ratios, and technical indicators
- Financial ratios: P/E, EPS, ROE, debt-to-equity, and other key metrics
- Technical indicators: moving averages, RSI, MACD, chart patterns
- Comparative analysis: sector and peer group comparisons

### Market Intelligence
- Company information: business profiles, management teams, statements
- Market news: earnings reports and market analysis
- Insider trading: buy/sell activities and ownership changes
- Options data: chain data, implied volatility, and statistics
## API Overview

 Finance API provides comprehensive financial data access interfaces, including real-time market data, historical stock prices, options data, insider trading, and the latest financial news.

Skills Path
Skill Location: {project_path}/skills/finance

this skill is located at above path in your project.

Reference Docs: See {Skill Location}/Finance_API_Doc.md for a working example.

## Zhipu AI - Hong Kong IPO Information
- **Stock Code**: 2513.HK 
- **Company Name (Chinese)**: Beijing Zhizhu Huazhang Technology Co., Ltd.
- **Company Name (English)**: Knowledge Atlas Technology Joint Stock Company Limited
Zhipu AI is a leading Chinese large language model company specializing in AI foundational model research and development.

### Best Practices for Zhipu AI Stock Research (One-Shot Success Guide)

**Search Strategy:**
- ✅ Use full English company name: `search=Knowledge+Atlas`
- ❌ Avoid: `search=Zhipu`, `search=02513.HK` (returns empty results)

** Important **
always read `Finance_API_Doc.md` before use the API



</DOCUMENT CI-DESSUS TRADUIT (INTÉGRAL, MÊME STRUCTURE, MÊMES LIGNES) — JAMAIS UN AVIS, JAMAIS UNE CONFIRMATION, JAMAIS UNE RÉPONSE COURTE.


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
