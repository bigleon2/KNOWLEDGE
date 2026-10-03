---
name: image-understand
version: "1.0.0"
category: "IA & Media"
tags:
  - image
  - understand
description: Implémente des fonctionnalités spécialisées de compréhension d'images avec le z-ai-web-dev-sdk. Utilisez ce skill quand l'utilisateur a besoin d'analyser des images statiques, extraire des informations visuelles, effectuer de l'OCR, détecter des objets, classer des images ou comprendre du contenu visuel. Optimisé pour les formats PNG, JPEG, GIF, WebP et BMP.
license: MIT
language: fr

---

# Skill de compréhension d'images

Ce skill fournit des fonctionnalités spécialisées de compréhension d'images avec le paquet z-ai-web-dev-sdk, permettant aux modèles d'IA d'analyser, décrire et extraire des informations d'images statiques.

## Emplacement du skill

**Emplacement** : `{project_path}/skills/image-understand`

Ce skill se trouve à l'emplacement indiqué ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/image-understand.ts` pour un exemple concret.

## Vue d'ensemble

La compréhension d'images se concentre spécifiquement sur l'analyse d'images statiques, avec des capacités pour :
- La description d'images et la compréhension de scènes
- La détection et la reconnaissance d'objets
- L'OCR (reconnaissance optique de caractères) et l'extraction de texte
- La classification et le catégorisation d'images
- L'analyse de contenu visuel
- L'évaluation de la qualité
- L'accessibilité (génération de texte alt)

**IMPORTANT** : z-ai-web-dev-sdk doit être utilisé UNIQUEMENT dans le code backend. Ne jamais l'utiliser dans le code côté client.

## Prérequis

Le paquet z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Utilisation CLI (pour les tâches simples)

Pour des tâches rapides d'analyse d'images, vous pouvez utiliser le CLI z-ai au lieu d'écrire du code. Idéal pour de simples descriptions d'images, des tests ou de l'automatisation.

### Analyse basique d'image

```bash
# Describe an image from URL
z-ai vision --prompt "What's in this image?" --image "https://example.com/photo.jpg"

# Using short options
z-ai vision -p "Describe this image" -i "https://example.com/image.png"
```

### Analyser des images locales

```bash
# Analyze a local image file
z-ai vision -p "What objects are in this photo?" -i "./photo.jpg"

# Save response to file
z-ai vision -p "Describe the scene" -i "./landscape.png" -o description.json
```

### Comparaison de plusieurs images

```bash
# Compare multiple images
z-ai vision \
  -p "Compare these two images and highlight the differences" \
  -i "./photo1.jpg" \
  -i "./photo2.jpg" \
  -o comparison.json

# Analyze a series of images
z-ai vision \
  --prompt "What patterns do you see across these images?" \
  --image "https://example.com/img1.jpg" \
  --image "https://example.com/img2.jpg" \
  --image "https://example.com/img3.jpg"
```

### Analyse avancée avec thinking

```bash
# Enable chain-of-thought reasoning for complex tasks
z-ai vision \
  -p "Count all people in this image and describe what each person is doing" \
  -i "./crowd.jpg" \
  --thinking \
  -o analysis.json

# Complex object detection with reasoning
z-ai vision \
  -p "Identify all safety hazards in this workplace image" \
  -i "./workplace.jpg" \
  --thinking
```

### Sortie en streaming

```bash
# Stream the analysis in real-time
z-ai vision -p "Provide a detailed description" -i "./photo.jpg" --stream
```

### Paramètres CLI

- `--prompt, -p <text>` : **obligatoire** - question ou instruction sur la ou les images
- `--image, -i <URL ou chemin>` : optionnel - URL de l'image ou chemin du fichier local (utilisable plusieurs fois)
- `--thinking, -t` : optionnel - active le raisonnement en chaîne de pensée (désactivé par défaut)
- `--output, -o <chemin>` : optionnel - chemin du fichier de sortie (format JSON)
- `--stream` : optionnel - diffuse la réponse en temps réel

### Formats d'images pris en charge

- PNG (.png) - idéal pour les diagrammes, captures d'écran et graphiques avec transparence
- JPEG (.jpg, .jpeg) - idéal pour les photos et images complexes
- GIF (.gif) - supporte les images statiques et animées
- WebP (.webp) - format moderne avec bonne compression
- BMP (.bmp) - format bitmap non compressé

### Quand utiliser le CLI vs le SDK

**Utiliser le CLI pour :**
- L'analyse ou la description rapide d'images
- Des tâches OCR ponctuelles
- Tester les capacités de compréhension d'images
- Des scripts simples de traitement par lot
- Générer du texte alt pour l'accessibilité

**Utiliser le SDK pour :**
- Les conversations multi-tours sur des images
- Les pipelines complexes de traitement d'images
- Les applications en production avec gestion d'erreurs
- L'intégration personnalisée avec la logique de votre application
- Le traitement par lot avec logique métier personnalisée

## Approche recommandée

Pour de meilleures performances et fiabilité, utilisez l'encodage base64 pour transmettre les images au modèle plutôt que des URLs d'images.

## Implémentation de base de la compréhension d'images

### Analyse d'une image unique

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function analyzeImage(imageUrl, prompt) {
  const zai = await ZAI.create();

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: prompt
          },
          {
            type: 'image_url',
            image_url: {
              url: imageUrl
            }
          }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}

// Usage examples
const description = await analyzeImage(
  'https://example.com/landscape.jpg',
  'Describe this landscape in detail, including colors, lighting, and mood'
);

const objectDetection = await analyzeImage(
  'https://example.com/room.jpg',
  'List all objects visible in this room'
);
```

### Comparaison de plusieurs images

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function compareImages(imageUrls, question) {
  const zai = await ZAI.create();

  const content = [
    {
      type: 'text',
      text: question
    },
    ...imageUrls.map(url => ({
      type: 'image_url',
      image_url: { url }
    }))
  ];

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: content
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}

// Usage
const comparison = await compareImages(
  [
    'https://example.com/before.jpg',
    'https://example.com/after.jpg'
  ],
  'What are the key differences between these before and after images?'
);
```

### Support des images base64 (recommandé)

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

async function analyzeLocalImage(imagePath, prompt) {
  const zai = await ZAI.create();

  // Read image file and convert to base64
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  
  // Determine MIME type based on file extension
  const ext = path.extname(imagePath).toLowerCase();
  const mimeTypes = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp'
  };
  const mimeType = mimeTypes[ext] || 'image/jpeg';

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: prompt
          },
          {
            type: 'image_url',
            image_url: {
              url: `data:${mimeType};base64,${base64Image}`
            }
          }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}

// Usage
const result = await analyzeLocalImage(
  './product-photo.jpg',
  'Analyze this product image for e-commerce listing'
);
```

## Cas d'usage avancés

### OCR et extraction de texte

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function extractText(imageUrl, options = {}) {
  const zai = await ZAI.create();

  const prompt = options.preserveLayout 
    ? 'Extract all text from this image. Preserve the exact layout, formatting, and structure.'
    : 'Extract all visible text from this image.';

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}

// Usage examples
const receiptText = await extractText(
  'https://example.com/receipt.jpg',
  { preserveLayout: true }
);

const businessCardInfo = await extractText(
  'https://example.com/business-card.jpg'
);
```

### Détection et comptage d'objets

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function detectObjects(imageUrl, objectType) {
  const zai = await ZAI.create();

  const prompt = objectType 
    ? `Count and locate all ${objectType} in this image. Provide their positions and describe each one.`
    : 'Detect and list all objects in this image with their approximate locations.';

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' } // Enable thinking for complex counting
  });

  return response.choices[0]?.message?.content;
}

// Usage
const peopleCount = await detectObjects(
  'https://example.com/crowd.jpg',
  'people'
);

const allObjects = await detectObjects(
  'https://example.com/room.jpg'
);
```

### Classification et étiquetage d'images

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function classifyAndTag(imageUrl) {
  const zai = await ZAI.create();

  const prompt = `Analyze this image and provide a comprehensive classification:
1. Primary category (e.g., nature, urban, portrait, product)
2. Subject matter (main focus of the image)
3. Style or mood (e.g., professional, casual, artistic, vintage)
4. Color palette description
5. Suggested tags (10-15 keywords, comma-separated)

Format your response as structured JSON.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  const content = response.choices[0]?.message?.content;
  
  try {
    return JSON.parse(content);
  } catch (e) {
    return { rawResponse: content };
  }
}

// Usage
const classification = await classifyAndTag(
  'https://example.com/photo.jpg'
);
console.log('Tags:', classification.tags);
```

### Évaluation de la qualité

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function assessImageQuality(imageUrl) {
  const zai = await ZAI.create();

  const prompt = `Assess the technical quality of this image:
1. Sharpness and focus (1-10)
2. Exposure and brightness (1-10)
3. Color balance (1-10)
4. Composition (1-10)
5. Any technical issues (blur, noise, artifacts, etc.)
6. Overall quality rating (1-10)
7. Suggestions for improvement

Provide specific feedback for each criterion.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}
```

### Accessibilité - génération de texte alt

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function generateAltText(imageUrl, context = '') {
  const zai = await ZAI.create();

  const prompt = context
    ? `Generate concise, descriptive alt text for this image. Context: ${context}. Focus on the most important visual elements that convey the image's purpose.`
    : 'Generate concise, descriptive alt text for this image suitable for screen readers. Focus on key visual elements.';

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}

// Usage
const altText = await generateAltText(
  'https://example.com/hero-image.jpg',
  'Website hero section for a tech startup'
);
```

### Compréhension de scène

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function understandScene(imageUrl) {
  const zai = await ZAI.create();

  const prompt = `Provide a comprehensive scene analysis:
1. Setting/location type (indoor/outdoor, specific place)
2. Time of day and lighting conditions
3. Weather (if applicable)
4. People present (number, activities, interactions)
5. Key objects and their arrangement
6. Overall atmosphere and mood
7. Notable details or interesting elements`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}
```

## Traitement par lot

### Traiter plusieurs images

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class ImageBatchProcessor {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async processImage(imageUrl, prompt) {
    const response = await this.zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ],
      thinking: { type: 'disabled' }
    });

    return response.choices[0]?.message?.content;
  }

  async processBatch(imageUrls, prompt) {
    const results = [];
    
    for (const imageUrl of imageUrls) {
      try {
        const result = await this.processImage(imageUrl, prompt);
        results.push({ imageUrl, success: true, result });
      } catch (error) {
        results.push({ 
          imageUrl, 
          success: false, 
          error: error.message 
        });
      }
    }

    return results;
  }
}

// Usage
const processor = new ImageBatchProcessor();
await processor.initialize();

const images = [
  'https://example.com/img1.jpg',
  'https://example.com/img2.jpg',
  'https://example.com/img3.jpg'
];

const results = await processor.processBatch(
  images,
  'Generate a short description suitable for social media'
);
```

## Bonnes pratiques

### 1. Qualité et préparation des images
- Utiliser des images haute résolution pour une meilleure précision d'analyse
- S'assurer que les images sont bien éclairées et correctement exposées
- Pour l'OCR, s'assurer que le texte est net et lisible
- Optimiser la taille des fichiers pour équilibrer qualité et performances
- Formats pris en charge : PNG (idéal pour texte/diagrammes), JPEG (idéal pour photos), WebP, GIF, BMP

### 2. Ingénierie des prompts pour les images
- Être précis sur les informations dont vous avez besoin
- Mentionner le type d'image (photo, diagramme, capture d'écran, etc.)
- Pour les tâches complexes, décomposer en questions spécifiques
- Utiliser des prompts structurés pour une sortie JSON
- Inclure le contexte quand c'est pertinent

### 3. Gestion d'erreurs

```javascript
async function safeImageAnalysis(imageUrl, prompt) {
  try {
    const zai = await ZAI.create();
    
    const response = await zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ],
      thinking: { type: 'disabled' }
    });

    return {
      success: true,
      content: response.choices[0]?.message?.content
    };
  } catch (error) {
    console.error('Image analysis error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 4. Optimisation des performances
- Mettre en cache l'instance du SDK pour le traitement par lot
- Utiliser l'encodage base64 pour les images locales
- Implémenter un contrôle de débit pour les grands lots
- Envisager un prétraitement des images (redimensionnement, compression) pour les gros fichiers
- Utiliser le mode thinking approprié (désactivé pour les tâches simples, activé pour le raisonnement complexe)

### 5. Considérations de sécurité
- Valider les URLs d'images avant traitement
- Implémenter une limitation de débit pour les API publiques
- Assainir les données d'images fournies par l'utilisateur
- Ne jamais exposer les identifiants du SDK dans le code côté client
- Implémenter une modération de contenu pour les images téléversées par les utilisateurs

## Cas d'usage courants

1. **Analyse de produits e-commerce** : analyser des images de produits, extraire des caractéristiques, générer des descriptions
2. **Traitement de documents** : extraire du texte de reçus, factures, formulaires, cartes de visite
3. **Modération de contenu** : détecter des contenus inappropriés, vérifier la conformité des images
4. **Contrôle qualité** : identifier des défauts, évaluer la qualité des produits en fabrication
5. **Accessibilité** : générer automatiquement du texte alt pour les images
6. **Catalogage d'images** : étiqueter et catégoriser automatiquement des bibliothèques d'images
7. **Recherche visuelle** : comprendre et indexer des images pour des fonctionnalités de recherche
8. **Imagerie médicale** : analyse préliminaire avec les avertissements appropriés
9. **Immobilier** : analyser des photos de biens, extraire des caractéristiques
10. **Réseaux sociaux** : générer des légendes, hashtags et descriptions

## Exemples d'intégration

### Point d'accès API Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';
import multer from 'multer';

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

let zaiInstance;

async function initZAI() {
  zaiInstance = await ZAI.create();
}

// Analyze image from URL
app.post('/api/analyze-image', express.json(), async (req, res) => {
  try {
    const { imageUrl, prompt } = req.body;

    if (!imageUrl || !prompt) {
      return res.status(400).json({ 
        error: 'imageUrl and prompt are required' 
      });
    }

    const response = await zaiInstance.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ],
      thinking: { type: 'disabled' }
    });

    res.json({
      success: true,
      analysis: response.choices[0]?.message?.content
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Analyze uploaded image file
app.post('/api/analyze-upload', upload.single('image'), async (req, res) => {
  try {
    const { prompt } = req.body;
    const imageFile = req.file;

    if (!imageFile || !prompt) {
      return res.status(400).json({ 
        error: 'image file and prompt are required' 
      });
    }

    // Convert to base64
    const base64Image = imageFile.buffer.toString('base64');
    const mimeType = imageFile.mimetype;

    const response = await zaiInstance.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { 
              type: 'image_url', 
              image_url: { 
                url: `data:${mimeType};base64,${base64Image}` 
              } 
            }
          ]
        }
      ],
      thinking: { type: 'disabled' }
    });

    res.json({
      success: true,
      analysis: response.choices[0]?.message?.content
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
    console.log('Image understanding API running on port 3000');
  });
});
```

### Route API Next.js

```javascript
// pages/api/image-understand.js
import ZAI from 'z-ai-web-dev-sdk';

let zaiInstance = null;

async function getZAI() {
  if (!zaiInstance) {
    zaiInstance = await ZAI.create();
  }
  return zaiInstance;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { imageUrl, prompt } = req.body;

    if (!imageUrl || !prompt) {
      return res.status(400).json({ 
        error: 'imageUrl and prompt are required' 
      });
    }

    const zai = await getZAI();

    const response = await zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ],
      thinking: { type: 'disabled' }
    });

    res.status(200).json({
      success: true,
      analysis: response.choices[0]?.message?.content
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
```

## Dépannage

**Problème** : « SDK must be used in backend »
- **Solution** : s'assurer que z-ai-web-dev-sdk n'est importé et utilisé que dans le code côté serveur, jamais dans le code client/navigateur

**Problème** : image non chargée ou non analysée
- **Solution** : vérifier que l'URL de l'image est accessible, renvoie le bon type MIME et est dans un format pris en charge

**Problème** : précision OCR médiocre
- **Solution** : s'assurer que le texte est net et lisible, augmenter la résolution de l'image, garantir un bon éclairage et contraste

**Problème** : détection ou comptage d'objets imprécis
- **Solution** : activer le mode thinking pour les tâches de comptage complexes, utiliser des images haute résolution, fournir des prompts précis

**Problème** : temps de réponse lents
- **Solution** : optimiser la taille des images (redimensionner avant upload), utiliser base64 pour les images locales, mettre en cache l'instance du SDK pour le traitement par lot

**Problème** : échec de l'encodage base64
- **Solution** : vérifier que le chemin du fichier est correct, contrôler les permissions du fichier, s'assurer que le type MIME correspond à l'extension

## À retenir

- Toujours utiliser z-ai-web-dev-sdk uniquement dans le code backend
- Le SDK est déjà installé - importer comme montré dans les exemples
- Utiliser le type de contenu `image_url` pour les images statiques
- L'encodage base64 est recommandé pour de meilleures performances
- Structurer clairement les prompts pour de meilleurs résultats
- Activer le mode thinking pour les tâches de raisonnement complexes (comptage, analyse détaillée)
- Gérer les erreurs avec soin en production
- Valider et assainir les entrées utilisateur
- Prendre en compte la vie privée et la sécurité lors du traitement des images utilisateur
