# Exemples d'intégration — web-reader (zones archivées R4)

> **Provenance** : skill `web-reader` · zones « Cas d'usage avancés » (intégral), bloc code « 5. Traitement du contenu » et « Exemples d'intégration » (intégral) · déplacées R4 byte-identité vers `references/` le 2026-11-09 (Task 85 G3, re-curation progressive disclosure — protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)) · **SHA-256 zone A : `ecc60659b0fd1628…`** · **SHA-256 bloc B : `9c57dcbb7efb717c…`** · **SHA-256 zone C : `357f24d6b4beb4e2…`** · le skill intégral demeure `skills/web-reader/SKILL.md` — les zones archivées ne sont jamais éditées (R4 byte-identité).

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


