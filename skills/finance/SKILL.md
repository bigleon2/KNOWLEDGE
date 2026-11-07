---
name: finance
description: "Comprehensive Finance API integration skill for real-time and historical financial data analysis, market research, and investment decision-making. Priority use cases: stock price queries, market data analysis, company financial information, portfolio tracking, market news retrieval, stock screening, technical analysis, and any financial market-related requests. This skill should be the primary choice for all  Finance API interactions and financial data needs."
---

## §0 — Contexte Système (SHARED v1.7.33)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



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
