---
name: web-search
version: "1.0.0"
category: "Web & Recherche"
tags:
  - web
  - search
description: Implémente des capacités de recherche web avec le z-ai-web-dev-sdk. Utilise ce skill lorsque l'utilisateur a besoin de rechercher des informations en temps réel sur le web, de récupérer du contenu à jour au-delà de la date de coupure des connaissances, ou de trouver les dernières actualités et données. Renvoie des résultats de recherche structurés avec URLs, extraits et métadonnées.
license: MIT
language: fr

read_when:
  - Déclencher quand la demande concerne : implémente des capacités de recherche web avec le z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : recherche, implémente, capacités
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Skill Web Search

Ce skill guide l'implémentation de la fonctionnalité de recherche web à l'aide du package z-ai-web-dev-sdk, permettant aux applications de rechercher sur le web et de récupérer des informations actuelles.

## Chemin d'installation

**Emplacement recommandé** : `{project_path}/skills/web-search`

Extrayez ce package de skill à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{project_path}/skills/web-search/scripts/` pour des tests rapides et comme référence. Voir `{project_path}/skills/web-search/scripts/web_search.ts` pour un exemple fonctionnel.

## Vue d'ensemble

Le skill Web Search permet de construire des applications capables de rechercher sur internet, de récupérer des informations actuelles et d'accéder à des données en temps réel depuis des sources web.

**IMPORTANT** : z-ai-web-dev-sdk DOIT être utilisé uniquement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme illustré dans les exemples ci-dessous.

## Utilisation du CLI (tâches simples)

Pour des requêtes de recherche web simples, vous pouvez utiliser le z-ai CLI au lieu d'écrire du code. C'est idéal pour une récupération d'informations rapide, le test de la fonctionnalité de recherche ou l'automatisation en ligne de commande.

### Recherche web basique

```bash
# Simple search query
z-ai function --name "web_search" --args '{"query": "artificial intelligence"}'

# Using short options
z-ai function -n web_search -a '{"query": "latest tech news"}'
```

### Recherche avec paramètres personnalisés

```bash
# Limit number of results
z-ai function \
  -n web_search \
  -a '{"query": "machine learning", "num": 5}'

# Search with recency filter (results from last N days)
z-ai function \
  -n web_search \
  -a '{"query": "cryptocurrency news", "num": 10, "recency_days": 7}'
```

### Sauvegarde des résultats de recherche

```bash
# Save results to JSON file
z-ai function \
  -n web_search \
  -a '{"query": "climate change research", "num": 5}' \
  -o search_results.json

# Recent news with file output
z-ai function \
  -n web_search \
  -a '{"query": "AI breakthroughs", "num": 3, "recency_days": 1}' \
  -o ai_news.json
```

### Exemples de recherche avancée

```bash
# Search for specific topics
z-ai function \
  -n web_search \
  -a '{"query": "quantum computing applications", "num": 8}' \
  -o quantum.json

# Find recent scientific papers
z-ai function \
  -n web_search \
  -a '{"query": "genomics research", "num": 5, "recency_days": 30}' \
  -o genomics.json

# Technology news from last 24 hours
z-ai function \
  -n web_search \
  -a '{"query": "tech industry updates", "recency_days": 1}' \
  -o today_tech.json
```

### Paramètres du CLI

- `--name, -n` : **Obligatoire** — Nom de la fonction (utilisez "web_search")
- `--args, -a` : **Obligatoire** — Objet d'arguments JSON avec :
  - `query` (string, obligatoire) : mots-clés de recherche
  - `num` (number, optionnel) : nombre de résultats (défaut : 10)
  - `recency_days` (number, optionnel) : filtre les résultats des N derniers jours
- `--output, -o <path>` : Optionnel — Chemin du fichier de sortie (format JSON)

### Structure d'un résultat de recherche

Chaque résultat contient :
- `url` : URL complète du résultat
- `name` : titre de la page
- `snippet` : texte d'aperçu/description
- `host_name` : nom de domaine
- `rank` : classement du résultat
- `date` : date de publication/mise à jour
- `favicon` : URL du favicon

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Des recherches d'informations rapides
- Tester des requêtes de recherche
- Des scripts d'automatisation simples
- Des tâches de recherche ponctuelles

**Utilisez le SDK pour :**
- La recherche dynamique dans des applications
- Des workflows de recherche en plusieurs étapes
- Le traitement et le filtrage personnalisés des résultats
- Des applications de production avec logique complexe

## Type de résultat de recherche

Chaque résultat de recherche est un `SearchFunctionResultItem` avec la structure suivante :

```typescript
interface SearchFunctionResultItem {
  url: string;          // Full URL of the result
  name: string;         // Title of the page
  snippet: string;      // Preview text/description
  host_name: string;    // Domain name
  rank: number;         // Result ranking
  date: string;         // Publication/update date
  favicon: string;      // Favicon URL
}
```

## Recherche web basique

### Requête de recherche simple

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function searchWeb(query) {
  const zai = await ZAI.create();

  const results = await zai.functions.invoke('web_search', {
    query: query,
    num: 10
  });

  return results;
}

// Usage
const searchResults = await searchWeb('What is the capital of France?');
console.log('Search Results:', searchResults);
```

### Recherche avec nombre de résultats personnalisé

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function searchWithLimit(query, numberOfResults) {
  const zai = await ZAI.create();

  const results = await zai.functions.invoke('web_search', {
    query: query,
    num: numberOfResults
  });

  return results;
}

// Usage - Get top 5 results
const topResults = await searchWithLimit('artificial intelligence news', 5);

// Usage - Get top 20 results
const moreResults = await searchWithLimit('JavaScript frameworks', 20);
```

### Résultats de recherche formatés

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function getFormattedResults(query) {
  const zai = await ZAI.create();

  const results = await zai.functions.invoke('web_search', {
    query: query,
    num: 10
  });

  // Format results for display
  const formatted = results.map((item, index) => ({
    position: index + 1,
    title: item.name,
    url: item.url,
    description: item.snippet,
    domain: item.host_name,
    publishDate: item.date
  }));

  return formatted;
}

// Usage
const results = await getFormattedResults('climate change solutions');
results.forEach(result => {
  console.log(`${result.position}. ${result.title}`);
  console.log(`   ${result.url}`);
  console.log(`   ${result.description}`);
  console.log('');
});
```

## Cas d'usage avancés

### Recherche avec traitement des résultats

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class SearchProcessor {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async search(query, options = {}) {
    const {
      num = 10,
      filterDomain = null,
      minSnippetLength = 0
    } = options;

    const results = await this.zai.functions.invoke('web_search', {
      query: query,
      num: num
    });

    // Filter results
    let filtered = results;

    if (filterDomain) {
      filtered = filtered.filter(item => 
        item.host_name.includes(filterDomain)
      );
    }

    if (minSnippetLength > 0) {
      filtered = filtered.filter(item => 
        item.snippet.length >= minSnippetLength
      );
    }

    return filtered;
  }

  extractDomains(results) {
    return [...new Set(results.map(item => item.host_name))];
  }

  groupByDomain(results) {
    const grouped = {};
    
    results.forEach(item => {
      if (!grouped[item.host_name]) {
        grouped[item.host_name] = [];
      }
      grouped[item.host_name].push(item);
    });

    return grouped;
  }

  sortByDate(results, ascending = false) {
    return results.sort((a, b) => {
      const dateA = new Date(a.date);
      const dateB = new Date(b.date);
      return ascending ? dateA - dateB : dateB - dateA;
    });
  }
}

// Usage
const processor = new SearchProcessor();
await processor.initialize();

const results = await processor.search('machine learning tutorials', {
  num: 15,
  minSnippetLength: 50
});

console.log('Domains found:', processor.extractDomains(results));
console.log('Grouped by domain:', processor.groupByDomain(results));
console.log('Sorted by date:', processor.sortByDate(results));
```

### Recherche d'actualités

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function searchNews(topic, timeframe = 'recent') {
  const zai = await ZAI.create();

  // Add time-based keywords to query
  const timeKeywords = {
    recent: 'latest news',
    today: 'today news',
    week: 'this week news',
    month: 'this month news'
  };

  const query = `${topic} ${timeKeywords[timeframe] || timeKeywords.recent}`;

  const results = await zai.functions.invoke('web_search', {
    query: query,
    num: 10
  });

  // Sort by date (most recent first)
  const sortedResults = results.sort((a, b) => {
    return new Date(b.date) - new Date(a.date);
  });

  return sortedResults;
}

// Usage
const aiNews = await searchNews('artificial intelligence', 'today');
const techNews = await searchNews('technology', 'week');

console.log('Latest AI News:');
aiNews.forEach(item => {
  console.log(`${item.name} (${item.date})`);
  console.log(`${item.snippet}\n`);
});
```

### Assistant de recherche

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ResearchAssistant {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async researchTopic(topic, depth = 'standard') {
    const numResults = {
      quick: 5,
      standard: 10,
      deep: 20
    };

    const results = await this.zai.functions.invoke('web_search', {
      query: topic,
      num: numResults[depth] || 10
    });

    // Analyze results
    const analysis = {
      topic: topic,
      totalResults: results.length,
      sources: this.extractDomains(results),
      topResults: results.slice(0, 5).map(r => ({
        title: r.name,
        url: r.url,
        summary: r.snippet
      })),
      dateRange: this.getDateRange(results)
    };

    return analysis;
  }

  extractDomains(results) {
    const domains = {};
    results.forEach(item => {
      domains[item.host_name] = (domains[item.host_name] || 0) + 1;
    });
    return domains;
  }

  getDateRange(results) {
    const dates = results
      .map(r => new Date(r.date))
      .filter(d => !isNaN(d));

    if (dates.length === 0) return null;

    return {
      earliest: new Date(Math.min(...dates)),
      latest: new Date(Math.max(...dates))
    };
  }

  async compareTopics(topic1, topic2) {
    const [results1, results2] = await Promise.all([
      this.zai.functions.invoke('web_search', { query: topic1, num: 10 }),
      this.zai.functions.invoke('web_search', { query: topic2, num: 10 })
    ]);

    const domains1 = new Set(results1.map(r => r.host_name));
    const domains2 = new Set(results2.map(r => r.host_name));

    const commonDomains = [...domains1].filter(d => domains2.has(d));

    return {
      topic1: {
        name: topic1,
        results: results1.length,
        uniqueDomains: domains1.size
      },
      topic2: {
        name: topic2,
        results: results2.length,
        uniqueDomains: domains2.size
      },
      commonDomains: commonDomains
    };
  }
}

// Usage
const assistant = new ResearchAssistant();
await assistant.initialize();

const research = await assistant.researchTopic('quantum computing', 'deep');
console.log('Research Analysis:', research);

const comparison = await assistant.compareTopics(
  'renewable energy',
  'solar power'
);
console.log('Topic Comparison:', comparison);
```

### Validation des résultats de recherche

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function validateSearchResults(query) {
  const zai = await ZAI.create();

  const results = await zai.functions.invoke('web_search', {
    query: query,
    num: 10
  });

  // Validate and score results
  const validated = results.map(item => {
    let score = 0;
    let flags = [];

    // Check snippet quality
    if (item.snippet && item.snippet.length > 50) {
      score += 20;
    } else {
      flags.push('short_snippet');
    }

    // Check date availability
    if (item.date && item.date !== 'N/A') {
      score += 20;
    } else {
      flags.push('no_date');
    }

    // Check URL validity
    try {
      new URL(item.url);
      score += 20;
    } catch (e) {
      flags.push('invalid_url');
    }

    // Check domain quality (not perfect, but basic check)
    if (!item.host_name.includes('spam') && 
        !item.host_name.includes('ads')) {
      score += 20;
    } else {
      flags.push('suspicious_domain');
    }

    // Check title quality
    if (item.name && item.name.length > 10) {
      score += 20;
    } else {
      flags.push('short_title');
    }

    return {
      ...item,
      qualityScore: score,
      validationFlags: flags,
      isHighQuality: score >= 80
    };
  });

  // Sort by quality score
  return validated.sort((a, b) => b.qualityScore - a.qualityScore);
}

// Usage
const validated = await validateSearchResults('best programming practices');
console.log('High quality results:', 
  validated.filter(r => r.isHighQuality).length
);
```

## Bonnes pratiques

### 1. Optimisation des requêtes

```javascript
// Bad: Too vague
const bad = await searchWeb('information');

// Good: Specific and targeted
const good = await searchWeb('JavaScript async/await best practices 2024');

// Good: Include context
const goodWithContext = await searchWeb('React hooks tutorial for beginners');
```

### 2. Gestion des erreurs

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function safeSearch(query, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const zai = await ZAI.create();

      const results = await zai.functions.invoke('web_search', {
        query: query,
        num: 10
      });

      if (!Array.isArray(results) || results.length === 0) {
        throw new Error('No results found or invalid response');
      }

      return {
        success: true,
        results: results,
        attempts: attempt
      };
    } catch (error) {
      lastError = error;
      console.error(`Attempt ${attempt} failed:`, error.message);

      if (attempt < retries) {
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
      }
    }
  }

  return {
    success: false,
    error: lastError.message,
    attempts: retries
  };
}
```

### 3. Cache des résultats

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class CachedSearch {
  constructor(cacheDuration = 3600000) { // 1 hour default
    this.cache = new Map();
    this.cacheDuration = cacheDuration;
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  getCacheKey(query, num) {
    return `${query}_${num}`;
  }

  async search(query, num = 10) {
    const cacheKey = this.getCacheKey(query, num);
    const cached = this.cache.get(cacheKey);

    // Check if cached and not expired
    if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
      console.log('Returning cached results');
      return {
        ...cached.data,
        cached: true
      };
    }

    // Perform fresh search
    const results = await this.zai.functions.invoke('web_search', {
      query: query,
      num: num
    });

    // Cache results
    this.cache.set(cacheKey, {
      data: results,
      timestamp: Date.now()
    });

    return {
      results: results,
      cached: false
    };
  }

  clearCache() {
    this.cache.clear();
  }

  getCacheSize() {
    return this.cache.size;
  }
}

// Usage
const search = new CachedSearch(1800000); // 30 minutes cache
await search.initialize();

const result1 = await search.search('TypeScript tutorial');
console.log('Cached:', result1.cached); // false

const result2 = await search.search('TypeScript tutorial');
console.log('Cached:', result2.cached); // true
```

### 4. Limitation de débit

```javascript
class RateLimitedSearch {
  constructor(requestsPerMinute = 60) {
    this.zai = null;
    this.requestsPerMinute = requestsPerMinute;
    this.requests = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async search(query, num = 10) {
    await this.checkRateLimit();

    const results = await this.zai.functions.invoke('web_search', {
      query: query,
      num: num
    });

    this.requests.push(Date.now());
    return results;
  }

  async checkRateLimit() {
    const now = Date.now();
    const oneMinuteAgo = now - 60000;

    // Remove requests older than 1 minute
    this.requests = this.requests.filter(time => time > oneMinuteAgo);

    if (this.requests.length >= this.requestsPerMinute) {
      const oldestRequest = this.requests[0];
      const waitTime = 60000 - (now - oldestRequest);
      
      console.log(`Rate limit reached. Waiting ${waitTime}ms`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
      
      // Recheck after waiting
      return this.checkRateLimit();
    }
  }
}
```

## Cas d'usage courants

1. **Récupération d'informations en temps réel** : obtenir l'actualité courante, les cours boursiers, la météo
2. **Recherche et analyse** : rassembler des informations sur des sujets spécifiques
3. **Découverte de contenu** : trouver des articles, tutoriels, documentations
4. **Analyse concurrentielle** : étudier les concurrents et les tendances du marché
5. **Vérification de faits** : confronter les informations aux sources web
6. **Recherche SEO et de contenu** : analyser les résultats de recherche pour une stratégie de contenu
7. **Agrégation d'actualités** : collecter des nouvelles depuis diverses sources
8. **Recherche académique** : trouver des articles, études et contenus académiques

## Exemples d'intégration

### API de recherche Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';

const app = express();
app.use(express.json());

let zaiInstance;

async function initZAI() {
  zaiInstance = await ZAI.create();
}

app.get('/api/search', async (req, res) => {
  try {
    const { q: query, num = 10 } = req.query;

    if (!query) {
      return res.status(400).json({ error: 'Query parameter "q" is required' });
    }

    const numResults = Math.min(parseInt(num) || 10, 20);

    const results = await zaiInstance.functions.invoke('web_search', {
      query: query,
      num: numResults
    });

    res.json({
      success: true,
      query: query,
      totalResults: results.length,
      results: results
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.get('/api/search/news', async (req, res) => {
  try {
    const { topic, timeframe = 'recent' } = req.query;

    if (!topic) {
      return res.status(400).json({ error: 'Topic parameter is required' });
    }

    const timeKeywords = {
      recent: 'latest news',
      today: 'today news',
      week: 'this week news'
    };

    const query = `${topic} ${timeKeywords[timeframe] || timeKeywords.recent}`;

    const results = await zaiInstance.functions.invoke('web_search', {
      query: query,
      num: 15
    });

    // Sort by date
    const sortedResults = results.sort((a, b) => {
      return new Date(b.date) - new Date(a.date);
    });

    res.json({
      success: true,
      topic: topic,
      timeframe: timeframe,
      results: sortedResults
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

initZAI().then(() => {
  app.listen(3000, () => {
    console.log('Search API running on port 3000');
  });
});
```

### Recherche avec résumé par IA

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function searchAndSummarize(query) {
  const zai = await ZAI.create();

  // Step 1: Search the web
  const searchResults = await zai.functions.invoke('web_search', {
    query: query,
    num: 10
  });

  // Step 2: Create summary using chat completions
  const searchContext = searchResults
    .slice(0, 5)
    .map((r, i) => `${i + 1}. ${r.name}\n${r.snippet}`)
    .join('\n\n');

  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'assistant',
        content: 'You are a research assistant. Summarize search results clearly and concisely.'
      },
      {
        role: 'user',
        content: `Query: "${query}"\n\nSearch Results:\n${searchContext}\n\nProvide a comprehensive summary of these results.`
      }
    ],
    thinking: { type: 'disabled' }
  });

  const summary = completion.choices[0]?.message?.content;

  return {
    query: query,
    summary: summary,
    sources: searchResults.slice(0, 5).map(r => ({
      title: r.name,
      url: r.url
    })),
    totalResults: searchResults.length
  };
}

// Usage
const result = await searchAndSummarize('benefits of renewable energy');
console.log('Summary:', result.summary);
console.log('Sources:', result.sources);
```

## Dépannage

**Problème** : "Le SDK doit être utilisé en backend"
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé et utilisé que dans du code côté serveur

**Problème** : résultats vides ou inexistants
- **Solution** : essayez d'autres termes de requête, vérifiez la connectivité internet, vérifiez le statut de l'API

**Problème** : format de réponse inattendu
- **Solution** : vérifiez que la réponse est un tableau, contrôlez d'éventuels changements d'API, ajoutez une validation de type

**Problème** : erreurs de limitation de débit
- **Solution** : implémentez un throttle des requêtes, ajoutez des délais entre les recherches, utilisez le cache

**Problème** : résultats de recherche de faible qualité
- **Solution** : affinez les termes de requête, filtrez les résultats par domaine ou par date, validez la qualité des résultats

## Conseils de performance

1. **Réutilisez l'instance SDK** : créez l'instance ZAI une seule fois et réutilisez-la pour toutes les recherches
2. **Implémentez un cache** : mettez les résultats de recherche en cache pour réduire les appels API
3. **Optimisez les termes de requête** : utilisez des requêtes spécifiques et ciblées pour de meilleurs résultats
4. **Limitez le nombre de résultats** : ne demandez que le nombre de résultats nécessaire
5. **Recherches parallèles** : utilisez Promise.all pour plusieurs recherches indépendantes
6. **Filtrage des résultats** : filtrez les résultats côté client lorsque c'est possible

## Considérations de sécurité

1. **Validation des entrées** : assainissez et validez les requêtes de recherche des utilisateurs
2. **Limitation de débit** : implémentez des limites pour prévenir les abus
3. **Protection des clés API** : n'exposez jamais les identifiants du SDK dans du code côté client
4. **Filtrage des résultats** : filtrez les contenus potentiellement nuisibles ou inappropriés
5. **Validation des URLs** : validez les URLs avant de rediriger les utilisateurs
6. **Vie privée** : ne journalisez pas les requêtes de recherche sensibles des utilisateurs

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- Le SDK est déjà installé — importez-le comme montré dans les exemples
- Les résultats de recherche sont renvoyés sous forme de tableau d'objets SearchFunctionResultItem
- Implémentez une gestion d'erreurs et des tentatives appropriées pour la production
- Mettez les résultats en cache quand c'est pertinent pour réduire les appels API
- Utilisez des termes de requête spécifiques pour de meilleurs résultats de recherche
- Validez et filtrez les résultats avant de les afficher aux utilisateurs
- Consultez `scripts/web_search.ts` pour un exemple de démarrage rapide
