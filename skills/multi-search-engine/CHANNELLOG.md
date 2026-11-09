# Multi Search Engine

## Informations de base

- **Nom**: multi-search-engine
- **Version**: v2.0.1
- **Description**: intègre 17 moteurs de recherche (8 domestiques+9internationaux), prend en charge la syntaxe de recherche avancée
- **Date de publication**: 2026-02-06

## Moteurs de recherche

**Domestiques (8)**: Baidu, Bing, 360, Sogou, WeChat, Toutiao, Jisilu
**Internationaux (9)**: Google、DuckDuckGo、Yahoo、Brave、Startpage、Ecosia、Qwant、WolframAlpha

## Fonctionnalités clés

- opérateurs de recherche avancée (site:, filetype:, intitle: etc.)
- DuckDuckGo Bangscommandes rapides
- filtrage temporel (heures/jours/semaines/mois/années)
- recherche respectueuse de la vie privée
- WolframAlphacalcul de connaissances

## Historique des mises à jour

### v2.0.1 (2026-02-06)
- documentation allégée, publication optimisée

### v2.0.0 (2026-02-06)
- ajout de 9 moteurs de recherche internationaux
- renforcement des capacités de recherche approfondie

### v1.0.0 (2026-02-04)
- version initiale : 8 moteurs de recherche domestiques

## Exemples d'utilisation

```javascript
// Google (recherche)
web_fetch({"url": "https://www.google.com/search?q=python"})

// recherche privée
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy"})

// recherche dans le site
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python"})
```

MIT License
