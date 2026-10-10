---
name: image-generation
version: "1.0.0"
category: "IA & Media"
tags:
  - image
  - generation
description: Implémente des fonctionnalités de génération d'images par IA avec le z-ai-web-dev-sdk. Utilisez ce skill quand l'utilisateur a besoin de créer des images à partir de descriptions textuelles, générer du contenu visuel, créer des œuvres, concevoir des assets ou construire des applications avec création d'images par IA. Prend en charge plusieurs tailles d'images et renvoie des images encodées en base64. Inclut aussi un outil CLI pour une génération rapide d'images.
license: MIT
language: fr

read_when:
  - Déclencher quand la demande concerne : implémente des fonctionnalités de génération d'images par IA avec le z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : images, génération, créer
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Skill de génération d'images

Ce skill guide l'implémentation de la fonctionnalité de génération d'images avec le paquet z-ai-web-dev-sdk et l'outil CLI, permettant de créer des images de haute qualité à partir de descriptions textuelles.

## Emplacement du skill

**Emplacement** : `{project_path}/skills/image-generation`

Ce skill se trouve à l'emplacement indiqué ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/image-generation.ts` pour un exemple concret.

## Vue d'ensemble

La génération d'images permet de construire des applications qui créent du contenu visuel à partir de prompts textuels grâce aux modèles d'IA, ouvrant la voie à des workflows créatifs, à l'automatisation du design et à la production de contenu visuel.

**IMPORTANT** : z-ai-web-dev-sdk doit être utilisé UNIQUEMENT dans le code backend. Ne jamais l'utiliser dans le code côté client.

## Prérequis

Le paquet z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Génération d'images de base

### Création simple d'image

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function generateImage(prompt, outputPath) {
  const zai = await ZAI.create();

  const response = await zai.images.generations.create({
    prompt: prompt,
    size: '1024x1024'
  });

  const imageBase64 = response.data[0].base64;
  
  // Save image
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);
  
  console.log(`Image saved to ${outputPath}`);
  return outputPath;
}

// Usage
await generateImage(
  'A cute cat playing in the garden',
  './cat_image.png'
);
```

### Plusieurs tailles d'images

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

// Supported sizes
const SUPPORTED_SIZES = [
  '1024x1024',  // Square
  '768x1344',   // Portrait
  '864x1152',   // Portrait
  '1344x768',   // Landscape
  '1152x864',   // Landscape
  '1440x720',   // Wide landscape
  '720x1440'    // Tall portrait
];

async function generateImageWithSize(prompt, size, outputPath) {
  if (!SUPPORTED_SIZES.includes(size)) {
    throw new Error(`Unsupported size: ${size}. Use one of: ${SUPPORTED_SIZES.join(', ')}`);
  }

  const zai = await ZAI.create();

  const response = await zai.images.generations.create({
    prompt: prompt,
    size: size
  });

  const imageBase64 = response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    size: size,
    fileSize: buffer.length
  };
}

// Usage - Different sizes
await generateImageWithSize(
  'A beautiful landscape',
  '1344x768',
  './landscape.png'
);

await generateImageWithSize(
  'A portrait of a person',
  '768x1344',
  './portrait.png'
);
```

## Utilisation de l'outil CLI

L'outil CLI z-ai offre un moyen pratique de générer des images directement depuis la ligne de commande.

### Utilisation CLI de base

```bash
# Generate image with full options
z-ai image --prompt "A beautiful landscape" --output "./image.png"

# Short form
z-ai image -p "A cute cat" -o "./cat.png"

# Specify size
z-ai image -p "A sunset" -o "./sunset.png" -s 1344x768

# Portrait orientation
z-ai image -p "A portrait" -o "./portrait.png" -s 768x1344
```

### Cas d'usage CLI

```bash
# Website hero image
z-ai image -p "Modern tech office with diverse team collaborating" -o "./hero.png" -s 1440x720

# Product image
z-ai image -p "Sleek smartphone on minimalist desk, professional product photography" -o "./product.png" -s 1024x1024

# Blog post illustration
z-ai image -p "Abstract visualization of data flowing through networks" -o "./blog_header.png" -s 1344x768

# Social media content
z-ai image -p "Vibrant illustration of community connection" -o "./social.png" -s 1024x1024

# Website favicon/logo
z-ai image -p "Simple geometric logo with blue gradient, minimal design" -o "./logo.png" -s 1024x1024

# Background pattern
z-ai image -p "Subtle geometric pattern, pastel colors, website background" -o "./bg_pattern.png" -s 1440x720
```

## Cas d'usage avancés

### Génération d'images par lot

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

async function generateImageBatch(prompts, outputDir, size = '1024x1024') {
  const zai = await ZAI.create();

  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const results = [];

  for (let i = 0; i < prompts.length; i++) {
    try {
      const prompt = prompts[i];
      const filename = `image_${i + 1}.png`;
      const outputPath = path.join(outputDir, filename);

      const response = await zai.images.generations.create({
        prompt: prompt,
        size: size
      });

      const imageBase64 = response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');
      fs.writeFileSync(outputPath, buffer);

      results.push({
        success: true,
        prompt: prompt,
        path: outputPath,
        size: buffer.length
      });

      console.log(`✓ Generated: ${filename}`);
    } catch (error) {
      results.push({
        success: false,
        prompt: prompts[i],
        error: error.message
      });

      console.error(`✗ Failed: ${prompts[i]} - ${error.message}`);
    }
  }

  return results;
}

// Usage
const prompts = [
  'A serene mountain landscape at sunset',
  'A futuristic city with flying cars',
  'An underwater coral reef teeming with life'
];

const results = await generateImageBatch(prompts, './generated-images');
console.log(`Generated ${results.filter(r => r.success).length} images`);
```

### Service de génération d'images

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

class ImageGenerationService {
  constructor(outputDir = './generated-images') {
    this.outputDir = outputDir;
    this.zai = null;
    this.cache = new Map();
  }

  async initialize() {
    this.zai = await ZAI.create();
    
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  generateCacheKey(prompt, size) {
    return crypto
      .createHash('md5')
      .update(`${prompt}-${size}`)
      .digest('hex');
  }

  async generate(prompt, options = {}) {
    const {
      size = '1024x1024',
      useCache = true,
      filename = null
    } = options;

    // Check cache
    const cacheKey = this.generateCacheKey(prompt, size);
    
    if (useCache && this.cache.has(cacheKey)) {
      const cachedPath = this.cache.get(cacheKey);
      if (fs.existsSync(cachedPath)) {
        return {
          path: cachedPath,
          cached: true,
          prompt: prompt,
          size: size
        };
      }
    }

    // Generate new image
    const response = await this.zai.images.generations.create({
      prompt: prompt,
      size: size
    });

    const imageBase64 = response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');

    // Determine output path
    const outputFilename = filename || `${cacheKey}.png`;
    const outputPath = path.join(this.outputDir, outputFilename);

    fs.writeFileSync(outputPath, buffer);

    // Cache result
    if (useCache) {
      this.cache.set(cacheKey, outputPath);
    }

    return {
      path: outputPath,
      cached: false,
      prompt: prompt,
      size: size,
      fileSize: buffer.length
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
const service = new ImageGenerationService();
await service.initialize();

const result = await service.generate(
  'A modern office space',
  { size: '1440x720' }
);

console.log('Generated:', result.path);
```

### Générateur d'assets pour sites web

```bash
# Using CLI for quick website asset generation
z-ai image -p "Modern tech hero banner, blue gradient" -o "./assets/hero.png" -s 1440x720
z-ai image -p "Team collaboration illustration" -o "./assets/team.png" -s 1344x768
z-ai image -p "Simple geometric logo" -o "./assets/logo.png" -s 1024x1024
```

## Bonnes pratiques

### 1. Ingénierie de prompts efficace

```javascript
function buildEffectivePrompt(subject, style, details = []) {
  const components = [
    subject,
    style,
    ...details,
    'high quality',
    'detailed'
  ];

  return components.filter(Boolean).join(', ');
}

// Usage
const prompt = buildEffectivePrompt(
  'mountain landscape',
  'oil painting style',
  ['sunset lighting', 'dramatic clouds', 'reflection in lake']
);

// Result: "mountain landscape, oil painting style, sunset lighting, dramatic clouds, reflection in lake, high quality, detailed"
```

### 2. Aide au choix de la taille

```javascript
function selectOptimalSize(purpose) {
  const sizeMap = {
    'hero-banner': '1440x720',
    'blog-header': '1344x768',
    'social-square': '1024x1024',
    'portrait': '768x1344',
    'product': '1024x1024',
    'landscape': '1344x768',
    'mobile-banner': '720x1440',
    'thumbnail': '1024x1024'
  };

  return sizeMap[purpose] || '1024x1024';
}

// Usage
const size = selectOptimalSize('hero-banner');
await generateImage('website hero image', size, './hero.png');
```

### 3. Gestion d'erreurs

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function safeGenerateImage(prompt, size, outputPath, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const zai = await ZAI.create();

      const response = await zai.images.generations.create({
        prompt: prompt,
        size: size
      });

      if (!response.data || !response.data[0] || !response.data[0].base64) {
        throw new Error('Invalid response from image generation API');
      }

      const imageBase64 = response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');
      fs.writeFileSync(outputPath, buffer);

      return {
        success: true,
        path: outputPath,
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

## Cas d'usage courants

1. **Design web** : générer des images hero, des fonds et des assets visuels
2. **Supports marketing** : créer des visuels pour les réseaux sociaux et des images promotionnelles
3. **Visualisation produit** : générer des maquettes et des variantes de produits
4. **Création de contenu** : produire des illustrations d'articles et des vignettes
5. **Assets de marque** : créer des logos, des icônes et des visuels de marque
6. **Design UI/UX** : générer des éléments d'interface et des illustrations
7. **Développement de jeux** : créer des concept arts et des assets de jeu
8. **E-commerce** : générer des images produits et des mises en scène

## Exemples d'intégration

### Point d'accès API Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());
app.use('/images', express.static('generated-images'));

let zaiInstance;
const outputDir = './generated-images';

async function initZAI() {
  zaiInstance = await ZAI.create();
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
}

app.post('/api/generate-image', async (req, res) => {
  try {
    const { prompt, size = '1024x1024' } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    const response = await zaiInstance.images.generations.create({
      prompt: prompt,
      size: size
    });

    const imageBase64 = response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');
    
    const filename = `img_${Date.now()}.png`;
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, buffer);

    res.json({
      success: true,
      imageUrl: `/images/${filename}`,
      prompt: prompt,
      size: size
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
    console.log('Image generation API running on port 3000');
  });
});
```

## Intégration CLI dans les scripts

### Exemple de script shell

```bash
#!/bin/bash

# Generate website assets using CLI
echo "Generating website assets..."

z-ai image -p "Modern tech hero banner, blue gradient" -o "./assets/hero.png" -s 1440x720
z-ai image -p "Team collaboration illustration" -o "./assets/team.png" -s 1344x768
z-ai image -p "Simple geometric logo" -o "./assets/logo.png" -s 1024x1024

echo "Assets generated successfully!"
```

## Dépannage

**Problème** : « SDK must be used in backend »
- **Solution** : s'assurer que z-ai-web-dev-sdk n'est utilisé que dans le code côté serveur

**Problème** : paramètre de taille invalide
- **Solution** : n'utiliser que les tailles prises en charge : 1024x1024, 768x1344, 864x1152, 1344x768, 1152x864, 1440x720, 720x1440

**Problème** : l'image générée ne correspond pas au prompt
- **Solution** : rendre les prompts plus spécifiques et descriptifs. Inclure le style, les détails et les termes de qualité

**Problème** : commande CLI introuvable
- **Solution** : s'assurer que le CLI z-ai est correctement installé et présent dans le PATH

**Problème** : fichier image corrompu
- **Solution** : vérifier que le décodage base64 et l'écriture du fichier sont corrects

## Conseils d'ingénierie des prompts

### Bons prompts
- ✓ "Professional product photography of wireless headphones, white background, studio lighting, high quality"
- ✓ "Mountain landscape at golden hour, oil painting style, dramatic clouds, detailed"
- ✓ "Modern minimalist logo for tech company, blue and white, geometric shapes"

### Mauvais prompts
- ✗ "headphones"
- ✗ "picture of mountains"
- ✗ "logo"

### Composants d'un prompt
1. **Sujet** : ce que vous voulez voir
2. **Style** : style artistique, style photographique, etc.
3. **Détails** : éléments spécifiques, couleurs, ambiance
4. **Qualité** : « high quality », « detailed », « professional »

## Tailles d'images prises en charge

- `1024x1024` - Carré
- `768x1344` - Portrait
- `864x1152` - Portrait
- `1344x768` - Paysage
- `1152x864` - Paysage
- `1440x720` - Paysage large
- `720x1440` - Portrait allongé

## À retenir

- Toujours utiliser z-ai-web-dev-sdk uniquement dans le code backend
- Le SDK est déjà installé - importer comme montré
- L'outil CLI est disponible pour une génération rapide d'images
- Les tailles prises en charge sont précises - utiliser la liste fournie
- Les images base64 doivent être décodées avant enregistrement
- Envisager le cache pour les prompts répétés
- Implémenter une logique de retry pour les applications en production
- Utiliser des prompts descriptifs pour de meilleurs résultats
