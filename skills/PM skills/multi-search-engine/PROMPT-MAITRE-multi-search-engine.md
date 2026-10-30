---
nom: multi-search-engine
source: skills/multi-search-engine/SKILL.md
sha256_source: 83c520b97a61
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — multi-search-engine (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/multi-search-engine/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: "multi-search-engine"
description: "Multi search engine integration with 8 domestic (CN) search engines. Supports advanced search operators, time filters, site search, and WeChat article search. No API keys required."
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Multi Search Engine v2.0.1

Integration of 8 domestic Chinese search engines for web crawling without API keys.

## Search Engines (Domestic - CN Only)

- **Baidu**: `https://www.baidu.com/s?wd={keyword}`
- **Bing CN**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **Bing INT**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360**: `https://www.so.com/s?q={keyword}`
- **Sogou**: `https://sogou.com/web?query={keyword}`
- **WeChat**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **Toutiao**: `https://so.toutiao.com/search?keyword={keyword}`
- **Jisilu**: `https://www.jisilu.cn/explore/?keyword={keyword}`

## Quick Examples

```javascript
// Basic search (Baidu)
web_fetch({"url": "https://www.baidu.com/s?wd=python+tutorial"})

// Site-specific (Bing CN)
web_fetch({"url": "https://cn.bing.com/search?q=site:github.com+react&ensearch=0"})

// File type (Baidu)
web_fetch({"url": "https://www.baidu.com/s?wd=machine+learning+filetype:pdf"})

// WeChat article search
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=intelligence artificielle (Rengong Zhineng) derniers progrès (Zuijin Jinzhan)"})

// Toutiao search
web_fetch({"url": "https://so.toutiao.com/search?keyword=Xin Neng Yuan + Zhengce"})

// Jisilu financial data
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=REITs"})
```

## Advanced Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `site:` | `site:github.com python` | Search within site |
| `filetype:` | `filetype:pdf report` | Specific file type |
| `""` | `"machine learning"` | Exact match |
| `-` | `python -snake` | Exclude term |
| `OR` | `cat OR dog` | Either term |

## Time Filters

| Parameter | Description |
|-----------|-------------|
| `tbs=qdr:h` | Past hour |
| `tbs=qdr:d` | Past day |
| `tbs=qdr:w` | Past week |
| `tbs=qdr:m` | Past month |
| `tbs=qdr:y` | Past year |

## Search Engine Notes

- **WeChat Search**: Best for searching WeChat public articles and content
- **Toutiao**: Good for trending topics and news aggregation
- **Jisilu**: Focused on financial and investment data
- **Bing INT**: International search results via Bing interface
- **Bing CN**: Localized Chinese search results

## Documentation

- `references/international-search.md` - Archived international search guide (for reference)
- `CHANGELOG.md` - Version history

## License

MIT


---

## Ressources locales du dossier

Ressources jointes (usage autonome — lire au besoin pendant l'application du prompt) :
- `references/international-search.md`
