---
name: VLM
version: "1.0.0"
category: "IA & Media"
tags:
  - VLM
description: Implémente des capacités de chat visuel (IA basée sur la vision) à l'aide du z-ai-web-dev-sdk. Utilisez ce skill lorsque l'utilisateur doit analyser des images, décrire du contenu visuel ou créer des applications combinant compréhension d'image et IA conversationnelle. Prend en charge les URLs d'images et les images encodées en base64 pour les interactions multimodales.
language: fr
license: MIT

read_when:
  - Déclencher quand la demande concerne : implémente des capacités de chat visuel (IA basée sur la vision) à l'aide du z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : images, visuel, implémente
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Skill VLM (Vision Chat)

Ce skill guide l'implémentation de la fonctionnalité de chat visuel à l'aide du package z-ai-web-dev-sdk, permettant aux modèles d'IA de comprendre et de répondre à des images combinées à des prompts textuels.

## Emplacement du skill

**Emplacement du skill** : `{project_path}/skills/VLM`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/vlm.ts` pour un exemple fonctionnel.

## Vue d'ensemble

Le chat visuel permet de créer des applications capables d'analyser des images, d'extraire des informations d'un contenu visuel et de répondre à des questions sur les images via une conversation en langage naturel.

**IMPORTANT** : le z-ai-web-dev-sdk doit être utilisé exclusivement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Utilisation du CLI (pour les tâches simples)

Pour des tâches simples d'analyse d'images, vous pouvez utiliser le CLI z-ai au lieu d'écrire du code. C'est idéal pour des descriptions d'images rapides, tester les capacités de vision ou une automatisation simple.

### Analyse d'image de base

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

### Plusieurs images

```bash
# Analyze multiple images at once
z-ai vision \
  -p "Compare these two images" \
  -i "./photo1.jpg" \
  -i "./photo2.jpg" \
  -o comparison.json

# Multiple images with detailed analysis
z-ai vision \
  --prompt "What are the differences between these images?" \
  --image "https://example.com/before.jpg" \
  --image "https://example.com/after.jpg"
```

### Avec réflexion (Chain of Thought)

```bash
# Enable thinking for complex visual reasoning
z-ai vision \
  -p "Count the number of people in this image and describe their activities" \
  -i "./crowd.jpg" \
  --thinking \
  -o analysis.json
```

### Sortie en streaming

```bash
# Stream the vision analysis
z-ai vision -p "Describe this image in detail" -i "./photo.jpg" --stream
```

### Paramètres du CLI

- `--prompt, -p <text>` : **Obligatoire** - question ou instruction à propos de la ou des images
- `--image, -i <URL or path>` : Optionnel - URL de l'image ou chemin de fichier local (utilisable plusieurs fois)
- `--thinking, -t` : Optionnel - activer le raisonnement pas à pas (désactivé par défaut)
- `--output, -o <path>` : Optionnel - chemin du fichier de sortie (format JSON)
- `--stream` : Optionnel - streame la réponse en temps réel

### Formats d'image pris en charge

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Une analyse d'images rapide
- Tester les capacités du modèle de vision
- Des descriptions d'images ponctuelles
- Des scripts d'automatisation simples

**Utilisez le SDK pour :**
- Des conversations multi-tours avec images
- L'analyse dynamique d'images dans des applications
- Le traitement par lots avec logique personnalisée
- Des applications de production aux workflows complexes

## Approche recommandée

Pour de meilleures performances et plus de fiabilité, transmettez les images au modèle en encodage base64 plutôt que par URLs d'images.

## Types de contenu pris en charge

L'API de chat visuel prend en charge trois types de contenu média :

### 1. **image_url** - pour les fichiers image
Utilisez ce type pour les images statiques (PNG, JPEG, GIF, WebP, etc.)
```typescript
{
    role: 'user',
    content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: imageUrl } }
    ]
}
```

### 2. **video_url** - pour les fichiers vidéo
Utilisez ce type pour le contenu vidéo (MP4, AVI, MOV, etc.)
```typescript
{
    role: 'user',
    content: [
        { type: 'text', text: prompt },
        { type: 'video_url', video_url: { url: videoUrl } }
    ]
}
```

### 3. **file_url** - pour les fichiers documents
Utilisez ce type pour les fichiers documents (PDF, DOCX, TXT, etc.)
```typescript
{
    role: 'user',
    content: [
        { type: 'text', text: prompt },
        { type: 'file_url', file_url: { url: fileUrl } }
    ]
}
```

**Remarque** : vous pouvez combiner plusieurs types de contenu dans un même message. Par exemple, du texte avec plusieurs images, ou du texte avec à la fois une image et un document.

## Implémentation de base du chat visuel

### Analyse d'une seule image

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function analyzeImage(imageUrl, question) {
  const zai = await ZAI.create();

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: question
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

// Usage
const result = await analyzeImage(
  'https://example.com/product.jpg',
  'Describe this product in detail'
);
console.log('Analysis:', result);
```

### Analyse de plusieurs images

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
  'Compare these two images and describe the differences'
);
```

### Prise en charge des images base64

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function analyzeLocalImage(imagePath, question) {
  const zai = await ZAI.create();

  // Read image file and convert to base64
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  const mimeType = imagePath.endsWith('.png') ? 'image/png' : 'image/jpeg';

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: question
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
```

## Cas d'usage avancés

### Chat visuel conversationnel

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class VisionChatSession {
  constructor() {
    this.messages = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async addImage(imageUrl, initialQuestion) {
    this.messages.push({
      role: 'user',
      content: [
        {
          type: 'text',
          text: initialQuestion
        },
        {
          type: 'image_url',
          image_url: { url: imageUrl }
        }
      ]
    });

    return this.getResponse();
  }

  async followUp(question) {
    this.messages.push({
      role: 'user',
      content: [
        {
          type: 'text',
          text: question
        }
      ]
    });

    return this.getResponse();
  }

  async getResponse() {
    const response = await this.zai.chat.completions.createVision({
      messages: this.messages,
      thinking: { type: 'disabled' }
    });

    const assistantMessage = response.choices[0]?.message?.content;
    
    this.messages.push({
      role: 'assistant',
      content: assistantMessage
    });

    return assistantMessage;
  }
}

// Usage
const session = new VisionChatSession();
await session.initialize();

const initial = await session.addImage(
  'https://example.com/chart.jpg',
  'What does this chart show?'
);
console.log('Initial analysis:', initial);

const followup = await session.followUp('What are the key trends?');
console.log('Follow-up:', followup);
```

### Classification et étiquetage d'images

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function classifyImage(imageUrl) {
  const zai = await ZAI.create();

  const prompt = `Analyze this image and provide:
1. Main subject/category
2. Key objects detected
3. Scene description
4. Suggested tags (comma-separated)

Format your response as JSON.`;

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
            image_url: { url: imageUrl }
          }
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
```

### OCR et extraction de texte

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function extractText(imageUrl) {
  const zai = await ZAI.create();

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: 'Extract all text from this image. Preserve the layout and formatting as much as possible.'
          },
          {
            type: 'image_url',
            image_url: { url: imageUrl }
          }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}
```

## Bonnes pratiques

### 1. Qualité et taille des images
- Utilisez des images de haute qualité pour de meilleurs résultats d'analyse
- Optimisez la taille des images pour équilibrer qualité et vitesse de traitement
- Formats pris en charge : JPEG, PNG, WebP

### 2. Ingénierie des prompts
- Soyez précis sur les informations que vous attendez de l'image
- Structurez les requêtes complexes avec des listes numérotées ou à puces
- Donnez le contexte du type d'image (photo, schéma, graphique, etc.)

### 3. Gestion des erreurs
```javascript
async function safeVisionChat(imageUrl, question) {
  try {
    const zai = await ZAI.create();
    
    const response = await zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: question },
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
    console.error('Vision chat error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 4. Optimisation des performances
- Mettez en cache la création de l'instance du SDK lors du traitement de plusieurs images
- Utilisez des formats d'image adaptés (JPEG pour les photos, PNG pour les schémas)
- Envisagez un prétraitement des images pour les gros lots

### 5. Considérations de sécurité
- Validez les URLs d'images avant traitement
- Assainissez les données d'image fournies par l'utilisateur
- Implémentez une limitation de débit pour les API exposées au public
- N'exposez jamais les identifiants du SDK dans du code côté client

## Cas d'usage courants

1. **Analyse de produits** : analyser des images de produits pour des applications e-commerce
2. **Compréhension de documents** : extraire des informations de reçus, factures, formulaires
3. **Imagerie médicale** : assister une analyse préliminaire (avec les avertissements appropriés)
4. **Contrôle qualité** : détecter des défauts ou anomalies dans la fabrication
5. **Modération de contenu** : analyser des images pour vérifier le respect des règles
6. **Accessibilité** : générer automatiquement du texte alternatif pour les images
7. **Recherche visuelle** : comprendre et catégoriser des images pour une fonctionnalité de recherche

## Exemples d'intégration

### Point d'accès API Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';

const app = express();
app.use(express.json());

let zaiInstance;

// Initialize SDK once
async function initZAI() {
  zaiInstance = await ZAI.create();
}

app.post('/api/analyze-image', async (req, res) => {
  try {
    const { imageUrl, question } = req.body;

    if (!imageUrl || !question) {
      return res.status(400).json({ 
        error: 'imageUrl and question are required' 
      });
    }

    const response = await zaiInstance.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: question },
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

initZAI().then(() => {
  app.listen(3000, () => {
    console.log('Vision chat API running on port 3000');
  });
});
```

## Dépannage

**Problème** : « le SDK doit être utilisé côté backend »
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé et utilisé que dans du code côté serveur

**Problème** : image qui ne se charge pas ou n'est pas analysée
- **Solution** : vérifiez que l'URL de l'image est accessible et renvoie un format d'image valide

**Problème** : qualité d'analyse médiocre
- **Solution** : donnez des prompts plus spécifiques et assurez-vous que la qualité de l'image est suffisante

**Problème** : temps de réponse lents
- **Solution** : optimisez la taille des images et envisagez de mettre en cache les images fréquemment analysées

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- Le SDK est déjà installé - importez-le comme montré dans les exemples
- Structurez clairement les prompts pour de meilleurs résultats
- Gérez les erreurs avec soin dans les applications de production
- Respectez la vie privée des utilisateurs lors du traitement des images
