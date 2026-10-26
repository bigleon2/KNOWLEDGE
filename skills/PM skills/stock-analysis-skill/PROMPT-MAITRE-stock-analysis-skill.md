---
nom: stock_analysis
source: skills/stock-analysis-skill/SKILL.md
sha256_source: f34e727e4528
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — stock_analysis (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/stock-analysis-skill/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: stock_analysis
description: "Comprehensive stock market analysis skill covering A-share (China), Hong Kong, and US equities. Priority use cases: stock analysis and buy/sell/hold recommendations by ticker code, generating decision dashboards and research reports with technical/fundamental/sentiment analysis, position-aware investment strategies based on user's cost price, dividend income scoring and safety analysis, rumor and early market signal scanning (M&A, insider activity, analyst actions), watchlist management with price target and stop-loss alerts, and K-line chart pattern recognition from images. This skill should be the primary choice whenever users mention a stock ticker, ask whether to buy or sell a stock, reference their holding cost or position, request dividend analysis, ask about market rumors or early signals, want to add/check/manage a watchlist, or upload a chart image for technical analysis."
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Stock Analysis Skill

## 依赖平台 Skills

- `finance skill` — 所有市场数据（A股/港股/美股统一）
- `pdf skill` — PDF 研报生成
- `docx skill` — Word 文档生成
- `vlm skill`（内置）— K线图形态识别

---

## Commands & Triggers

| 命令 | 触发词示例 |
|------|-----------|
| 个股分析 | 分析600519 / AAPL值不值得买 / 帮我看看腾讯 |
| 带持仓分析 | 我持仓成本1450分析茅台 / AAPL我170买的现在怎样 |
| 股息分析 | JNJ股息怎么样 / 帮我分析这几只股的股息 KO PG JNJ |
| 传闻扫描 | 今日有什么并购传闻 / 扫描一下市场早期信号 |
| 添加自选股 | 关注AAPL / 把600519加入自选，目标价1600止损1350 |
| 查看自选股 | 我的自选股列表 / 看一下我关注的股票 |
| 检查提醒 | 检查自选股提醒 / 有没有触发止损 |
| 删除自选股 | 从自选股删除TSLA |
| K线图分析 | （上传图片）帮我分析这个K线图 |
| 大盘复盘 | 附带大盘复盘分析600519 |

---

## Input Schemas

### 个股分析
```typescript
{
  stocks: (string | { code: string; position?: { status: "empty"|"holding"; cost?: number; shares?: number } })[],
  outputFormat?: "markdown" | "pdf" | "word",  // 默认 markdown
  mode?: "full" | "quote",                      // 默认 full
  includeMarketReview?: boolean,                // 默认 false
  includeGlobalMacro?: boolean,                 // 默认 true
  includeDividend?: boolean,                    // 美股附加股息分析，默认 false
}
```

### 股息分析
```typescript
runDividend(tickers: string | string[])
```

### 传闻扫描
```typescript
runRumorScan()  // 无需参数，自动扫描今日信号
```

### 自选股管理
```typescript
runWatchlistAdd(ticker, { targetPrice?, stopPrice?, alertOnSignal?, notes? })
runWatchlistRemove(ticker)
runWatchlistList()
runWatchlistCheck()  // 检查是否触发价格/信号提醒
```

---

## Report Structure

```
# 股票智能分析报告

## 🌍 全球宏观速览（默认开启）
## 🎯 大盘复盘（需开启）
## 📊 个股决策仪表盘（每只）
   ### 📰 重要信息速览（舆情/业绩预期/🚨风险/✨利好/最新动态）
   ### 📌 核心结论（结论/一句话/空仓者建议/持仓者建议+盈亏）
   ### 📈 当日行情
   ### 📊 数据透视（技术面/基本面/资金面）
   ### 🎯 作战计划（狙击点位表/仓位/风控）
   ### ✅ 检查清单（综合结论）
   ### 💰 股息分析（美股，需开启 includeDividend）
```

---

## Dividend Analysis Metrics

| 指标 | 说明 |
|------|------|
| 安全评分 | 0-100，综合派息率/增长/连续年数 |
| 收入评级 | excellent/good/moderate/poor |
| 派息率状态 | safe(<40%)/moderate/high/unsustainable |
| 5年CAGR | 股息复合增长率 |
| 连续增长年数 | 25年以上为股息贵族 |

---

## Rumor Scanner Signal Types

| 类型 | 冲击分 | 说明 |
|------|--------|------|
| 并购传闻 (ma) | +5 | M&A/收购/要约 |
| 内部人动态 (insider) | +4 | CEO/董事买卖 |
| 分析师调整 (analyst) | +3 | 评级上调/下调/目标价变动 |
| 监管动态 (regulatory) | +3 | SEC调查/合规风险 |
| 业绩预期 (earnings) | +2 | 盈利预警/上调 |

---

## Watchlist Alert Types

| 提醒类型 | 触发条件 |
|---------|---------|
| 🎯 目标价 | 当前价 ≥ targetPrice |
| 🛑 止损价 | 当前价 ≤ stopPrice |
| 📊 信号变化 | 本次结论 ≠ 上次结论 |

---

## Behavior Rules

- 乖离率 > 5% → 结论不得为买入/强烈买入
- 数据缺失 → 标"暂缺"，严禁捏造
- 有持仓成本 → 必须给出盈亏分析
- 未提供持仓 → 同时给出空仓/持仓两套建议
- 每次分析后自动静默更新自选股信号

---

## File Structure

```
stock-analysis-skill/
├── SKILL.md
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts          # 主入口（所有命令路由）
    ├── types.ts          # 类型定义
    ├── dataFetcher.ts    # 数据层（finance skill）
    ├── analyzer.ts       # 个股分析（LLM/VLM）
    ├── dividend.ts       # 股息分析
    ├── rumorScanner.ts   # 传闻扫描
    └── watchlist.ts      # 自选股管理（storage 持久化）
```

---

## Limitations

- 传闻扫描依赖 finance skill 新闻数据质量
- 自选股数据持久化依赖平台 storage API
- 港股基本面数据较少
- 不支持期货、ETF、可转债
- 仅供参考，不构成投资建议


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
