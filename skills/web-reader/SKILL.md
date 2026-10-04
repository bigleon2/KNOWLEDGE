---
name: web-reader
version: "1.0.0"
category: "Web & Recherche"
tags:
  - web
  - reader
description: Implémente des capacités d'extraction de contenu de pages web avec le z-ai-web-dev-sdk. Utilise ce skill lorsque l'utilisateur a besoin de scraper des pages web, d'extraire le contenu d'articles, de récupérer les métadonnées d'une page, ou de construire des applications traitant du contenu web. Prend en charge l'extraction automatique du contenu avec récupération du titre, du HTML et de la date de publication.
license: MIT
language: fr

read_when:
  - Déclencher quand la demande concerne : implémente des capacités d'extraction de contenu de pages web avec le z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : contenu, extraction, pages
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Skill Web Reader

Ce skill guide l'implémentation de la lecture de pages web et de l'extraction de contenu à l'aide du package z-ai-web-dev-sdk, permettant aux applications de récupérer et de traiter du contenu web par programmation.

## Chemin du skill

**Emplacement du skill** : `{project_path}/skills/web-reader`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/web-reader.ts` pour un exemple fonctionnel.

## Vue d'ensemble

Web Reader permet de construire des applications capables d'extraire le contenu de pages web, de récupérer les métadonnées d'articles et de traiter du contenu HTML. L'API gère automatiquement l'extraction de contenu et fournit des données propres et structurées à partir de n'importe quelle URL web.

**IMPORTANT** : z-ai-web-dev-sdk DOIT être utilisé uniquement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme illustré dans les exemples ci-dessous.

## Utilisation du CLI (tâches simples)

Pour une extraction simple de contenu de page web, vous pouvez utiliser le z-ai CLI au lieu d'écrire du code. C'est idéal pour du scraping rapide de contenu, des tests d'URLs ou des tâches d'automatisation simples.

### Lecture basique d'une page

```bash
# Extract content from a web page
z-ai function --name "page_reader" --args '{"url": "https://example.com"}'

# Using short options
z-ai function -n page_reader -a '{"url": "https://www.example.com/article"}'
```

### Sauvegarde du contenu d'une page

```bash
# Save extracted content to JSON file
z-ai function \
  -n page_reader \
  -a '{"url": "https://news.example.com/article"}' \
  -o page_content.json

# Extract and save blog post
z-ai function \
  -n page_reader \
  -a '{"url": "https://blog.example.com/post/123"}' \
  -o blog_post.json
```

### Cas d'usage courants

```bash
# Extract news article
z-ai function \
  -n page_reader \
  -a '{"url": "https://news.site.com/breaking-news"}' \
  -o news.json

# Read documentation page
z-ai function \
  -n page_reader \
  -a '{"url": "https://docs.example.com/getting-started"}' \
  -o docs.json

# Scrape blog content
z-ai function \
  -n page_reader \
  -a '{"url": "https://techblog.com/ai-trends-2024"}' \
  -o blog.json

# Extract research article
z-ai function \
  -n page_reader \
  -a '{"url": "https://research.org/papers/quantum-computing"}' \
  -o research.json
```

### Paramètres du CLI

- `--name, -n` : **Obligatoire** — Nom de la fonction (utilisez "page_reader")
- `--args, -a` : **Obligatoire** — Objet d'arguments JSON avec :
  - `url` (string, obligatoire) : l'URL de la page web à lire
- `--output, -o <path>` : Optionnel — Chemin du fichier de sortie (format JSON)

### Structure de la réponse

Le CLI renvoie un objet JSON contenant :
- `title` : titre de la page
- `html` : HTML du contenu principal
- `text` : contenu en texte brut
- `publish_time` : horodatage de publication (si disponible)
- `url` : URL d'origine
- `metadata` : métadonnées supplémentaires de la page

### Exemple de réponse

```json
{
  "title": "Introduction to Machine Learning",
  "html": "<article><h1>Introduction to Machine Learning</h1><p>Machine learning is...</p></article>",
  "text": "Introduction to Machine Learning\n\nMachine learning is...",
  "publish_time": "2024-01-15T10:30:00Z",
  "url": "https://example.com/ml-intro",
  "metadata": {
    "author": "John Doe",
    "description": "A comprehensive guide to ML"
  }
}
```

### Traitement de plusieurs URLs

```bash
# Create a simple script to process multiple URLs
for url in \
  "https://site1.com/article1" \
  "https://site2.com/article2" \
  "https://site3.com/article3"
do
  filename=$(echo $url | md5sum | cut -d' ' -f1)
  z-ai function -n page_reader -a "{\"url\": \"$url\"}" -o "${filename}.json"
done
```

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Une extraction rapide de contenu
- Tester l'accessibilité d'URLs
- Des tâches simples de scraping web
- Une récupération de contenu ponctuelle

**Utilisez le SDK pour :**
- Le traitement d'URLs par lots avec logique personnalisée
- L'intégration dans des applications web
- Des pipelines complexes de traitement de contenu
- Des applications de production avec gestion d'erreurs

## Fonctionnement

Le Web Reader utilise la fonction `page_reader` pour :
1. Récupérer le contenu de la page web
2. Extraire le contenu principal de l'article et les métadonnées
3. Analyser et nettoyer le HTML
4. Renvoyer des données structurées incluant le titre, le contenu et la date de publication

## Implémentation basique de la lecture web

### Lecture simple d'une page

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function readWebPage(url) {
  try {
    const zai = await ZAI.create();

    const result = await zai.functions.invoke('page_reader', {
      url: url
    });

    console.log('Title:', result.data.title);
    console.log('URL:', result.data.url);
    console.log('Published:', result.data.publishedTime);
    console.log('HTML Content:', result.data.html);
    console.log('Tokens Used:', result.data.usage.tokens);

    return result.data;
  } catch (error) {
    console.error('Page reading failed:', error.message);
    throw error;
  }
}

// Usage
const pageData = await readWebPage('https://example.com/article');
console.log('Page title:', pageData.title);
```

### Extraction du texte seul d'un article

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function extractArticleText(url) {
  const zai = await ZAI.create();

  const result = await zai.functions.invoke('page_reader', {
    url: url
  });

  // Convert HTML to plain text (basic approach)
  const plainText = result.data.html
    .replace(/<[^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  return {
    title: result.data.title,
    text: plainText,
    url: result.data.url,
    publishedTime: result.data.publishedTime
  };
}

// Usage
const article = await extractArticleText('https://news.example.com/story');
console.log(article.title);
console.log(article.text.substring(0, 200) + '...');
```

### Lecture de plusieurs pages

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function readMultiplePages(urls) {
  const zai = await ZAI.create();
  const results = [];

  for (const url of urls) {
    try {
      const result = await zai.functions.invoke('page_reader', {
        url: url
      });

      results.push({
        url: url,
        success: true,
        data: result.data
      });
    } catch (error) {
      results.push({
        url: url,
        success: false,
        error: error.message
      });
    }
  }

  return results;
}

// Usage
const urls = [
  'https://example.com/article1',
  'https://example.com/article2',
  'https://example.com/article3'
];

const pages = await readMultiplePages(urls);
pages.forEach(page => {
  if (page.success) {
    console.log(`✓ ${page.data.title}`);
  } else {
    console.log(`✗ ${page.url}: ${page.error}`);
  }
});
```

## Cas d'usage avancés

### Analyseur de contenu web

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class WebContentAnalyzer {
  constructor() {
    this.cache = new Map();
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async readPage(url, useCache = true) {
    // Check cache
    if (useCache && this.cache.has(url)) {
      console.log('Returning cached result for:', url);
      return this.cache.get(url);
    }

    // Fetch fresh content
    const result = await this.zai.functions.invoke('page_reader', {
      url: url
    });

    // Cache the result
    if (useCache) {
      this.cache.set(url, result.data);
    }

    return result.data;
  }

  async getPageMetadata(url) {
    const data = await this.readPage(url);

    return {
      title: data.title,
      url: data.url,
      publishedTime: data.publishedTime,
      contentLength: data.html.length,
      wordCount: this.estimateWordCount(data.html)
    };
  }

  estimateWordCount(html) {
    const text = html.replace(/<[^>]*>/g, ' ');
    const words = text.split(/\s+/).filter(word => word.length > 0);
    return words.length;
  }

  async comparePages(url1, url2) {
    const [page1, page2] = await Promise.all([
      this.readPage(url1),
      this.readPage(url2)
    ]);

    return {
      page1: {
        title: page1.title,
        wordCount: this.estimateWordCount(page1.html),
        published: page1.publishedTime
      },
      page2: {
        title: page2.title,
        wordCount: this.estimateWordCount(page2.html),
        published: page2.publishedTime
      }
    };
  }

  clearCache() {
    this.cache.clear();
  }
}

// Usage
const analyzer = new WebContentAnalyzer();
await analyzer.initialize();

const metadata = await analyzer.getPageMetadata('https://example.com/article');
console.log('Article Metadata:', metadata);

const comparison = await analyzer.comparePages(
  'https://example.com/article1',
  'https://example.com/article2'
);
console.log('Comparison:', comparison);
```

### Lecteur de flux RSS

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class FeedReader {
  constructor() {
    this.articles = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async fetchArticlesFromUrls(urls) {
    const articles = [];

    for (const url of urls) {
      try {
        const result = await this.zai.functions.invoke('page_reader', {
          url: url
        });

        articles.push({
          title: result.data.title,
          url: result.data.url,
          publishedTime: result.data.publishedTime,
          content: result.data.html,
          fetchedAt: new Date().toISOString()
        });

        console.log(`Fetched: ${result.data.title}`);
      } catch (error) {
        console.error(`Failed to fetch ${url}:`, error.message);
      }
    }

    this.articles = articles;
    return articles;
  }

  getRecentArticles(limit = 10) {
    return this.articles
      .sort((a, b) => {
        const dateA = new Date(a.publishedTime || a.fetchedAt);
        const dateB = new Date(b.publishedTime || b.fetchedAt);
        return dateB - dateA;
      })
      .slice(0, limit);
  }

  searchArticles(keyword) {
    return this.articles.filter(article => {
      const searchText = `${article.title} ${article.content}`.toLowerCase();
      return searchText.includes(keyword.toLowerCase());
    });
  }
}

// Usage
const reader = new FeedReader();
await reader.initialize();

const feedUrls = [
  'https://example.com/article1',
  'https://example.com/article2',
  'https://example.com/article3'
];

await reader.fetchArticlesFromUrls(feedUrls);
const recent = reader.getRecentArticles(5);
console.log('Recent articles:', recent.map(a => a.title));
```

### Agrégateur de contenu

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function aggregateContent(urls, options = {}) {
  const zai = await ZAI.create();
  const aggregated = {
    sources: [],
    totalWords: 0,
    aggregatedAt: new Date().toISOString()
  };

  for (const url of urls) {
    try {
      const result = await zai.functions.invoke('page_reader', {
        url: url
      });

      const text = result.data.html.replace(/<[^>]*>/g, ' ');
      const wordCount = text.split(/\s+/).filter(w => w.length > 0).length;

      aggregated.sources.push({
        title: result.data.title,
        url: result.data.url,
        publishedTime: result.data.publishedTime,
        wordCount: wordCount,
        excerpt: text.substring(0, 200).trim() + '...'
      });

      aggregated.totalWords += wordCount;

      if (options.delay) {
        await new Promise(resolve => setTimeout(resolve, options.delay));
      }
    } catch (error) {
      console.error(`Failed to fetch ${url}:`, error.message);
    }
  }

  return aggregated;
}

// Usage
const sources = [
  'https://example.com/news1',
  'https://example.com/news2',
  'https://example.com/news3'
];

const aggregated = await aggregateContent(sources, { delay: 1000 });
console.log(`Aggregated ${aggregated.sources.length} sources`);
console.log(`Total words: ${aggregated.totalWords}`);
```

### Pipeline de scraping web

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ScrapingPipeline {
  constructor() {
    this.processors = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  addProcessor(name, processorFn) {
    this.processors.push({ name, fn: processorFn });
  }

  async scrape(url) {
    // Fetch the page
    const result = await this.zai.functions.invoke('page_reader', {
      url: url
    });

    let data = {
      raw: result.data,
      processed: {}
    };

    // Run through processors
    for (const processor of this.processors) {
      try {
        data.processed[processor.name] = await processor.fn(data.raw);
        console.log(`✓ Processed with ${processor.name}`);
      } catch (error) {
        console.error(`✗ Failed ${processor.name}:`, error.message);
        data.processed[processor.name] = null;
      }
    }

    return data;
  }
}

// Processor functions
function extractLinks(pageData) {
  const linkRegex = /href=["'](https?:\/\/[^"']+)["']/g;
  const links = [];
  let match;

  while ((match = linkRegex.exec(pageData.html)) !== null) {
    links.push(match[1]);
  }

  return [...new Set(links)]; // Remove duplicates
}

function extractImages(pageData) {
  const imgRegex = /src=["'](https?:\/\/[^"']+\.(jpg|jpeg|png|gif|webp))["']/gi;
  const images = [];
  let match;

  while ((match = imgRegex.exec(pageData.html)) !== null) {
    images.push(match[1]);
  }

  return [...new Set(images)];
}

function extractPlainText(pageData) {
  return pageData.html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// Usage
const pipeline = new ScrapingPipeline();
await pipeline.initialize();

pipeline.addProcessor('links', extractLinks);
pipeline.addProcessor('images', extractImages);
pipeline.addProcessor('plainText', extractPlainText);

const result = await pipeline.scrape('https://example.com/article');
console.log('Links found:', result.processed.links.length);
console.log('Images found:', result.processed.images.length);
console.log('Text length:', result.processed.plainText.length);
```

## Format de réponse

### Réponse en cas de succès

```typescript
{
  code: 200,
  status: 200,
  data: {
    title: "Article Title",
    url: "https://example.com/article",
    html: "<div>Article content...</div>",
    publishedTime: "2025-01-15T10:30:00Z",
    usage: {
      tokens: 1500
    }
  },
  meta: {
    usage: {
      tokens: 1500
    }
  }
}
```

### Champs de la réponse

| Champ | Type | Description |
|-------|------|-------------|
| `code` | number | Code de statut de la réponse |
| `status` | number | Code de statut HTTP |
| `data.title` | string | Titre de la page |
| `data.url` | string | URL de la page |
| `data.html` | string | Contenu HTML extrait |
| `data.publishedTime` | string | Date de publication (optionnel) |
| `data.usage.tokens` | number | Tokens utilisés pour le traitement |
| `meta.usage.tokens` | number | Nombre total de tokens utilisés |

## Bonnes pratiques

### 1. Gestion des erreurs

```javascript
async function safeReadPage(url) {
  try {
    const zai = await ZAI.create();

    // Validate URL
    if (!url || !url.startsWith('http')) {
      throw new Error('Invalid URL format');
    }

    const result = await zai.functions.invoke('page_reader', {
      url: url
    });

    // Check response status
    if (result.code !== 200) {
      throw new Error(`Failed to fetch page: ${result.code}`);
    }

    // Verify essential data
    if (!result.data.html || !result.data.title) {
      throw new Error('Incomplete page data received');
    }

    return {
      success: true,
      data: result.data
    };
  } catch (error) {
    console.error('Page reading error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 2. Limitation de débit

```javascript
class RateLimitedReader {
  constructor(requestsPerMinute = 10) {
    this.requestsPerMinute = requestsPerMinute;
    this.requestTimes = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async readPage(url) {
    await this.waitForRateLimit();

    const result = await this.zai.functions.invoke('page_reader', {
      url: url
    });

    this.requestTimes.push(Date.now());
    return result.data;
  }

  async waitForRateLimit() {
    const now = Date.now();
    const oneMinuteAgo = now - 60000;

    // Remove old timestamps
    this.requestTimes = this.requestTimes.filter(time => time > oneMinuteAgo);

    // Check if we need to wait
    if (this.requestTimes.length >= this.requestsPerMinute) {
      const oldestRequest = this.requestTimes[0];
      const waitTime = 60000 - (now - oldestRequest);

      if (waitTime > 0) {
        console.log(`Rate limit reached. Waiting ${waitTime}ms...`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }
  }
}

// Usage
const reader = new RateLimitedReader(10); // 10 requests per minute
await reader.initialize();

const urls = ['https://example.com/1', 'https://example.com/2'];
for (const url of urls) {
  const data = await reader.readPage(url);
  console.log('Fetched:', data.title);
}
```

### 3. Stratégie de cache

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class CachedWebReader {
  constructor(cacheDuration = 3600000) { // 1 hour default
    this.cache = new Map();
    this.cacheDuration = cacheDuration;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async readPage(url, forceRefresh = false) {
    const cacheKey = url;
    const cached = this.cache.get(cacheKey);

    // Return cached if valid and not forcing refresh
    if (cached && !forceRefresh) {
      const age = Date.now() - cached.timestamp;
      if (age < this.cacheDuration) {
        console.log('Returning cached content for:', url);
        return cached.data;
      }
    }

    // Fetch fresh content
    const result = await this.zai.functions.invoke('page_reader', {
      url: url
    });

    // Update cache
    this.cache.set(cacheKey, {
      data: result.data,
      timestamp: Date.now()
    });

    return result.data;
  }

  clearCache() {
    this.cache.clear();
  }

  getCacheStats() {
    return {
      size: this.cache.size,
      entries: Array.from(this.cache.keys())
    };
  }
}

// Usage
const reader = new CachedWebReader(3600000); // 1 hour cache
await reader.initialize();

const data1 = await reader.readPage('https://example.com'); // Fresh fetch
const data2 = await reader.readPage('https://example.com'); // From cache
const data3 = await reader.readPage('https://example.com', true); // Force refresh
```

### 4. Traitement parallèle

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function readPagesInParallel(urls, concurrency = 3) {
  const zai = await ZAI.create();
  const results = [];
  
  // Process in batches
  for (let i = 0; i < urls.length; i += concurrency) {
    const batch = urls.slice(i, i + concurrency);
    
    const batchResults = await Promise.allSettled(
      batch.map(url =>
        zai.functions.invoke('page_reader', { url })
          .then(result => ({
            url: url,
            success: true,
            data: result.data
          }))
          .catch(error => ({
            url: url,
            success: false,
            error: error.message
          }))
      )
    );

    results.push(...batchResults.map(r => r.value));
    console.log(`Completed batch ${Math.floor(i / concurrency) + 1}`);
  }

  return results;
}

// Usage
const urls = [
  'https://example.com/1',
  'https://example.com/2',
  'https://example.com/3',
  'https://example.com/4',
  'https://example.com/5'
];

const results = await readPagesInParallel(urls, 2); // 2 concurrent requests
results.forEach(result => {
  if (result.success) {
    console.log(`✓ ${result.data.title}`);
  } else {
    console.log(`✗ ${result.url}: ${result.error}`);
  }
});
```

### 5. Traitement du contenu

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ContentProcessor {
  static extractMainContent(html) {
    // Remove scripts, styles, and comments
    let content = html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<!--[\s\S]*?-->/g, '');

    return content;
  }

  static htmlToPlainText(html) {
    return html
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/p>/gi, '\n\n')
      .replace(/<[^>]*>/g, '')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/\s+/g, ' ')
      .trim();
  }

  static extractMetadata(html) {
    const metadata = {};

    // Extract meta description
    const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i);
    if (descMatch) metadata.description = descMatch[1];

    // Extract keywords
    const keywordsMatch = html.match(/<meta\s+name=["']keywords["']\s+content=["']([^"']+)["']/i);
    if (keywordsMatch) metadata.keywords = keywordsMatch[1].split(',').map(k => k.trim());

    // Extract author
    const authorMatch = html.match(/<meta\s+name=["']author["']\s+content=["']([^"']+)["']/i);
    if (authorMatch) metadata.author = authorMatch[1];

    return metadata;
  }
}

// Usage
async function processWebPage(url) {
  const zai = await ZAI.create();
  const result = await zai.functions.invoke('page_reader', { url });

  return {
    title: result.data.title,
    url: result.data.url,
    mainContent: ContentProcessor.extractMainContent(result.data.html),
    plainText: ContentProcessor.htmlToPlainText(result.data.html),
    metadata: ContentProcessor.extractMetadata(result.data.html),
    publishedTime: result.data.publishedTime
  };
}

const processed = await processWebPage('https://example.com/article');
console.log('Processed content:', processed.title);
```

## Cas d'usage courants

1. **Agrégation d'actualités** : collecter et agréger des articles de presse depuis plusieurs sources
2. **Surveillance de contenu** : suivre les changements sur des pages web spécifiques
3. **Outils de recherche** : extraire des informations de sites académiques ou de référence
4. **Suivi de prix** : surveiller les pages produits pour détecter les changements de prix
5. **Analyse SEO** : extraire les métadonnées et le contenu des pages à des fins SEO
6. **Création d'archives** : créer des copies locales de contenu web
7. **Curation de contenu** : collecter et organiser du contenu web par thème
8. **Veille concurrentielle** : surveiller les sites des concurrents pour détecter les mises à jour

## Exemples d'intégration

### Endpoint API Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';

const app = express();
app.use(express.json());

let zaiInstance;

async function initZAI() {
  zaiInstance = await ZAI.create();
}

app.post('/api/read-page', async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({ 
        error: 'URL is required' 
      });
    }

    const result = await zaiInstance.functions.invoke('page_reader', {
      url: url
    });

    res.json({
      success: true,
      data: {
        title: result.data.title,
        url: result.data.url,
        content: result.data.html,
        publishedTime: result.data.publishedTime,
        tokensUsed: result.data.usage.tokens
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.post('/api/read-multiple', async (req, res) => {
  try {
    const { urls } = req.body;

    if (!urls || !Array.isArray(urls)) {
      return res.status(400).json({ 
        error: 'URLs array is required' 
      });
    }

    const results = await Promise.allSettled(
      urls.map(url =>
        zaiInstance.functions.invoke('page_reader', { url })
          .then(result => ({
            url: url,
            success: true,
            data: result.data
          }))
          .catch(error => ({
            url: url,
            success: false,
            error: error.message
          }))
      )
    );

    res.json({
      success: true,
      results: results.map(r => r.value)
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
    console.log('Web reader API running on port 3000');
  });
});
```

### Récupérateur de contenu planifié

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import cron from 'node-cron';

class ScheduledFetcher {
  constructor() {
    this.urls = [];
    this.results = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  addUrl(url, schedule) {
    this.urls.push({ url, schedule });
  }

  async fetchContent(url) {
    try {
      const result = await this.zai.functions.invoke('page_reader', {
        url: url
      });

      return {
        url: url,
        success: true,
        title: result.data.title,
        content: result.data.html,
        fetchedAt: new Date().toISOString()
      };
    } catch (error) {
      return {
        url: url,
        success: false,
        error: error.message,
        fetchedAt: new Date().toISOString()
      };
    }
  }

  startScheduledFetch(url, schedule) {
    cron.schedule(schedule, async () => {
      console.log(`Fetching ${url}...`);
      const result = await this.fetchContent(url);
      this.results.push(result);
      
      // Keep only last 100 results
      if (this.results.length > 100) {
        this.results = this.results.slice(-100);
      }
      
      console.log(`Fetched: ${result.success ? result.title : result.error}`);
    });
  }

  start() {
    for (const { url, schedule } of this.urls) {
      this.startScheduledFetch(url, schedule);
    }
  }

  getResults() {
    return this.results;
  }
}

// Usage
const fetcher = new ScheduledFetcher();
await fetcher.initialize();

// Fetch every hour
fetcher.addUrl('https://example.com/news', '0 * * * *');

// Fetch every day at midnight
fetcher.addUrl('https://example.com/daily', '0 0 * * *');

fetcher.start();
console.log('Scheduled fetching started');
```

## Dépannage

**Problème** : "Le SDK doit être utilisé en backend"
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé et utilisé que dans du code côté serveur

**Problème** : échec de récupération de la page (404, 403, etc.)
- **Solution** : vérifiez que l'URL est accessible et non protégée par une authentification ou un paywall

**Problème** : contenu incomplet ou manquant
- **Solution** : certaines pages peuvent contenir du contenu dynamique nécessitant JavaScript. Le lecteur extrait le contenu HTML statique.

**Problème** : consommation élevée de tokens
- **Solution** : la consommation de tokens dépend de la taille de la page. Envisagez de mettre en cache les pages fréquemment consultées.

**Problème** : temps de réponse lents
- **Solution** : mettez en place un cache, utilisez le traitement parallèle pour plusieurs URLs et envisagez une limitation de débit

**Problème** : contenu HTML vide
- **Solution** : vérifiez si la page nécessite une authentification ou comporte des mesures anti-scraping. Vérifiez que l'URL est correcte.

## Conseils de performance

1. **Mettez en place un cache** : mettez en cache les pages fréquemment consultées pour réduire les appels API
2. **Utilisez le traitement parallèle** : récupérez plusieurs pages simultanément (avec limitation de débit)
3. **Traitez le contenu efficacement** : extrayez du HTML uniquement les informations nécessaires
4. **Définissez des timeouts** : implémentez des délais d'expiration raisonnables pour la récupération des pages
5. **Surveillez la consommation de tokens** : suivez l'usage pour optimiser les coûts
6. **Opérations par lots** : regroupez plusieurs récupérations d'URLs lorsque c'est possible

## Considérations de sécurité

- Validez toutes les URLs avant traitement
- Assainissez le contenu HTML extrait avant de l'afficher
- Implémentez une limitation de débit pour prévenir les abus
- N'exposez jamais les identifiants du SDK dans du code côté client
- Respectez le robots.txt et les conditions d'utilisation des sites web
- Traitez les données utilisateur conformément aux réglementations sur la vie privée
- Implémentez une gestion d'erreurs appropriée pour les requêtes en échec

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- Le SDK est déjà installé — importez-le comme montré dans les exemples
- Implémentez une gestion d'erreurs appropriée pour des applications robustes
- Utilisez le cache pour améliorer les performances et réduire les coûts
- Respectez les conditions d'utilisation des sites web et les limites de débit
- Traitez le contenu HTML avec soin pour en extraire des données exploitables
- Surveillez la consommation de tokens pour optimiser les coûts
