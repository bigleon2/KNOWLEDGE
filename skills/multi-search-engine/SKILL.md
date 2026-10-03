---
name: "multi-search-engine"
version: "1.0.0"
category: "Web & Recherche"
tags:
  - multi
  - search
  - engine
description: "Intégration multi-moteurs de recherche avec 8 moteurs de recherche nationaux (CN). Prend en charge les opérateurs de recherche avancés, les filtres temporels, la recherche par site et la recherche d'articles WeChat. Aucune clé API requise."
language: fr

---

# Multi Search Engine v2.0.1

Intégration de 8 moteurs de recherche chinois nationaux pour l'exploration web sans clés API.

## Moteurs de recherche (nationaux - CN uniquement)

- **Baidu**: `https://www.baidu.com/s?wd={keyword}`
- **Bing CN**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **Bing INT**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360**: `https://www.so.com/s?q={keyword}`
- **Sogou**: `https://sogou.com/web?query={keyword}`
- **WeChat**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **Toutiao**: `https://so.toutiao.com/search?keyword={keyword}`
- **Jisilu**: `https://www.jisilu.cn/explore/?keyword={keyword}`

## Exemples rapides

```javascript
// Basic search (Baidu)
web_fetch({"url": "https://www.baidu.com/s?wd=python+tutorial"})

// Site-specific (Bing CN)
web_fetch({"url": "https://cn.bing.com/search?q=site:github.com+react&ensearch=0"})

// File type (Baidu)
web_fetch({"url": "https://www.baidu.com/s?wd=machine+learning+filetype:pdf"})

// WeChat article search
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=人工智能+最新进展"})

// Toutiao search
web_fetch({"url": "https://so.toutiao.com/search?keyword=新能源+政策"})

// Jisilu financial data
web_fetch({"url": "https://www.jisilu.cn/explore/?keyword=REITs"})
```

## Opérateurs avancés

| Opérateur | Exemple | Description |
|----------|---------|-------------|
| `site:` | `site:github.com python` | Rechercher dans un site |
| `filetype:` | `filetype:pdf report` | Type de fichier spécifique |
| `""` | `"machine learning"` | Correspondance exacte |
| `-` | `python -snake` | Exclure un terme |
| `OR` | `cat OR dog` | L'un des deux termes |

## Filtres temporels

| Paramètre | Description |
|-----------|-------------|
| `tbs=qdr:h` | Dernière heure |
| `tbs=qdr:d` | Dernier jour |
| `tbs=qdr:w` | Dernière semaine |
| `tbs=qdr:m` | Dernier mois |
| `tbs=qdr:y` | Dernière année |

## Notes sur les moteurs de recherche

- **Recherche WeChat** : idéal pour chercher les articles et contenus publics de WeChat
- **Toutiao** : adapté aux sujets tendance et à l'agrégation d'actualités
- **Jisilu** : centré sur les données financières et d'investissement
- **Bing INT** : résultats de recherche internationaux via l'interface Bing
- **Bing CN** : résultats de recherche chinois localisés

## Documentation

- `references/international-search.md` - Guide de recherche internationale archivé (pour référence)
- `CHANGELOG.md` - Historique des versions

## Licence

MIT
