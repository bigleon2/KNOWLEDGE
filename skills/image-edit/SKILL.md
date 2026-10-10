---
name: image-edit
version: "1.0.0"
category: "IA & Media"
tags:
  - image
  - edit
description: Implémente des fonctionnalités d'édition et de modification d'images par IA avec le z-ai-web-dev-sdk. Utilisez ce skill quand l'utilisateur a besoin de modifier des images existantes, créer des variantes, changer le contenu visuel, redessiner des assets ou transformer des images à partir de descriptions textuelles. Prend en charge plusieurs tailles d'images et renvoie des résultats encodés en base64. Inclut aussi un outil CLI pour une édition rapide d'images.
license: MIT
language: fr

read_when:
  - Déclencher quand la demande concerne : implémente des fonctionnalités d'édition et de modification d'images par IA avec le z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : images, édition, implémente
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Skill d'édition d'images

Ce skill guide l'implémentation de fonctionnalités d'édition et de modification d'images avec le paquet z-ai-web-dev-sdk et l'outil CLI, permettant la transformation et l'édition intelligentes d'images à partir de descriptions textuelles.

## Emplacement du skill

**Emplacement** : `{project_path}/skills/image-edit`

Ce skill se trouve à l'emplacement indiqué ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/image-edit.ts` pour un exemple concret.

## Vue d'ensemble

L'édition d'images permet de construire des applications qui modifient, transforment et améliorent des images existantes grâce aux modèles d'IA. Idéal pour redessiner des assets, créer des variantes, améliorer le contenu visuel et transformer des images à partir de descriptions textuelles.

**IMPORTANT** : z-ai-web-dev-sdk doit être utilisé UNIQUEMENT dans le code backend. Ne jamais l'utiliser dans le code côté client.

## Méthode de l'API du SDK

La fonctionnalité d'édition d'images utilise la méthode d'API suivante :

```javascript
await zai.images.generations.edit({
  prompt: string,              // Required: Description of the edit to apply
  images: [{ url: string }],  // Required: Array with image URL or base64 data URL
  size?: string,              // Optional: Output size (default: '1024x1024')
  model?: string              // Optional: Model name
})
```

**Important** : le paramètre `images` doit être un tableau d'objets avec une propriété `url`, pas une simple chaîne.

**Point d'accès API** : `POST /images/generations/edit`

**Renvoie** : `ImageGenerationResponse` avec l'image éditée encodée en base64

## Prérequis

Le paquet z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Édition d'images de base

### Transformation simple d'une image

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function editImage(imageSource, editPrompt, outputPath, size = '1024x1024') {
  const zai = await ZAI.create();

  const response = await zai.images.generations.edit({
    prompt: editPrompt,
    images: [{ url: imageSource }],  // Array of objects with url property
    size: size
  });

  const imageBase64 = response.data[0].base64;
  
  // Save edited image
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);
  
  console.log(`Edited image saved to ${outputPath}`);
  return outputPath;
}

// Usage - Using remote image URL
await editImage(
  'https://example.com/landscape.jpg',
  'Transform this landscape into a night scene with stars and moon',
  './landscape_night.png'
);

// Usage - Using local image converted to base64
import { readFileSync } from 'fs';
const imageBuffer = readFileSync('./photo.jpg');
const base64Image = imageBuffer.toString('base64');
const dataUrl = `data:image/jpeg;base64,${base64Image}`;

await editImage(
  dataUrl,
  'Change the cat to a dog, keep everything else the same',
  './dog_version.png'
);
```

### Créer des variantes d'image

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function createVariation(imageSource, baseDescription, variation, outputPath, size = '1024x1024') {
  const zai = await ZAI.create();

  // Combine base description with variation request
  const prompt = `${baseDescription}, ${variation}`;

  const response = await zai.images.generations.edit({
    prompt: prompt,
    images: [{ url: imageSource }],
    size: size
  });

  const imageBase64 = response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    prompt: prompt,
    variation: variation
  };
}

// Usage - Create variations from original image
await createVariation(
  'https://example.com/headshot.jpg',
  'Professional headshot photo',
  'with blue background instead of gray',
  './headshot_blue.png'
);

await createVariation(
  './smartphone.png',
  'Product photo of smartphone',
  'on wooden table instead of white background',
  './product_wood.png'
);
```

### Plusieurs tailles d'images pour l'édition

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

async function editImageWithSize(imageSource, editPrompt, size, outputPath) {
  if (!SUPPORTED_SIZES.includes(size)) {
    throw new Error(`Unsupported size: ${size}. Use one of: ${SUPPORTED_SIZES.join(', ')}`);
  }

  const zai = await ZAI.create();

  const response = await zai.images.generations.edit({
    prompt: editPrompt,
    images: [{ url: imageSource }],
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

// Usage - Edit with different aspect ratios
await editImageWithSize(
  './logo.png',
  'Redesign the logo to be more modern and minimalist',
  '1024x1024',
  './logo_redesigned.png'
);

await editImageWithSize(
  'https://example.com/portrait.jpg',
  'Transform the portrait to landscape orientation, sunset lighting',
  '1344x768',
  './portrait_landscape.png'
);
```

## Utilisation de l'outil CLI

L'outil CLI z-ai offre un moyen pratique de modifier des images directement depuis la ligne de commande.

### Utilisation CLI de base

```bash
# Edit image with full options
z-ai image-edit --prompt "Change the background to sunset colors" --image "./photo.png" --output "./edited.png"

# Short form
z-ai image-edit -p "Make it darker and moodier" -i "./original.jpg" -o "./moody.png"

# Specify output size
z-ai image-edit -p "Redesign in modern style" -i "./design.png" -o "./modern.png" -s 1344x768

# Using remote image URL
z-ai image-edit -p "Convert to landscape orientation" -i "https://example.com/photo.png" -o "./landscape.png" -s 1344x768
```

### Paramètres CLI

- `--prompt, -p` : **obligatoire** - description de la modification à appliquer
- `--image, -i` : **obligatoire** - URL de l'image d'origine ou chemin du fichier local
- `--output, -o` : **obligatoire** - chemin du fichier image de sortie (format PNG)
- `--size, -s` : optionnel - taille de l'image, 1024x1024 par défaut
- `--help, -h` : optionnel - affiche l'aide

### Tailles prises en charge

- `1024x1024`, `768x1344`, `864x1152`, `1344x768`, `1152x864`, `1440x720`, `720x1440`

### Cas d'usage CLI pour l'édition d'images

```bash
# Redesign existing asset
z-ai image-edit -p "Redesign the logo with gradients and modern styling" -i "./logo.png" -o "./logo_v2.png" -s 1024x1024

# Change color scheme
z-ai image-edit -p "Change color scheme to blue and white, professional style" -i "./original.png" -o "./recolored.png" -s 1440x720

# Style transformation
z-ai image-edit -p "Transform to oil painting style, vibrant colors" -i "./photo.jpg" -o "./oil_painting.png" -s 1152x864

# Background replacement
z-ai image-edit -p "Replace background with modern office setting" -i "./portrait.png" -o "./new_background.png" -s 1344x768

# Lighting adjustment
z-ai image-edit -p "Adjust to golden hour lighting, warm tones" -i "./landscape.jpg" -o "./golden_hour.png" -s 1024x1024

# Element modification
z-ai image-edit -p "Replace the red car with a blue motorcycle" -i "./scene.png" -o "./modified.png" -s 1344x768

# Mood transformation
z-ai image-edit -p "Transform to dark moody atmosphere with dramatic lighting" -i "./bright.jpg" -o "./moody.png" -s 1440x720

# Using remote image URL
z-ai image-edit -p "Add a hat to the person" -i "https://example.com/photo.png" -o "./result.png" -s 1024x1024
```

## Cas d'usage avancés

### Édition d'images par lot

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

async function batchEditImages(editInstructions, outputDir, size = '1024x1024') {
  const zai = await ZAI.create();

  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const results = [];

  for (let i = 0; i < editInstructions.length; i++) {
    try {
      const instruction = editInstructions[i];
      const filename = `edited_${i + 1}.png`;
      const outputPath = path.join(outputDir, filename);

      const response = await zai.images.generations.edit({
        prompt: instruction.prompt,
        images: [{ url: instruction.imageSource }],
        size: size
      });

      const imageBase64 = response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');
      fs.writeFileSync(outputPath, buffer);

      results.push({
        success: true,
        instruction: instruction.prompt,
        path: outputPath,
        size: buffer.length
      });

      console.log(`✓ Edited: ${filename}`);
    } catch (error) {
      results.push({
        success: false,
        instruction: editInstructions[i].prompt,
        error: error.message
      });

      console.error(`✗ Failed: ${editInstructions[i].prompt} - ${error.message}`);
    }
  }

  return results;
}

// Usage - Create multiple variations from the same image
const editInstructions = [
  { 
    imageSource: './original.jpg',
    prompt: 'Change background to blue gradient' 
  },
  { 
    imageSource: './original.jpg',
    prompt: 'Transform to black and white, high contrast' 
  },
  { 
    imageSource: './original.jpg',
    prompt: 'Add sunset lighting effects' 
  }
];

const results = await batchEditImages(editInstructions, './edited-images');
console.log(`Edited ${results.filter(r => r.success).length} images`);
```

### Service d'édition d'images

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

class ImageEditingService {
  constructor(outputDir = './edited-images') {
    this.outputDir = outputDir;
    this.zai = null;
    this.editHistory = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
    
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  generateFilename(editPrompt) {
    const hash = crypto
      .createHash('md5')
      .update(`${editPrompt}-${Date.now()}`)
      .digest('hex')
      .substring(0, 8);
    
    return `edited_${hash}.png`;
  }

  async edit(imageSource, editPrompt, options = {}) {
    const {
      size = '1024x1024',
      saveToHistory = true,
      filename = null
    } = options;

    const response = await this.zai.images.generations.edit({
      prompt: editPrompt,
      images: [{ url: imageSource }],
      size: size
    });

    const imageBase64 = response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');

    // Determine output path
    const outputFilename = filename || this.generateFilename(editPrompt);
    const outputPath = path.join(this.outputDir, outputFilename);

    fs.writeFileSync(outputPath, buffer);

    const result = {
      path: outputPath,
      imageSource: imageSource,
      editPrompt: editPrompt,
      size: size,
      fileSize: buffer.length,
      timestamp: new Date().toISOString()
    };

    // Save to history
    if (saveToHistory) {
      this.editHistory.push(result);
    }

    return result;
  }

  async createVariations(imageSource, basePrompt, variations, options = {}) {
    const results = [];
    
    for (const variation of variations) {
      const fullPrompt = `${basePrompt}, ${variation}`;
      const result = await this.edit(imageSource, fullPrompt, options);
      result.variation = variation;
      results.push(result);
    }

    return results;
  }

  getEditHistory() {
    return this.editHistory;
  }

  clearHistory() {
    this.editHistory = [];
  }
}

// Usage
const service = new ImageEditingService();
await service.initialize();

// Single edit
const edited = await service.edit(
  './original.jpg',
  'Transform to watercolor painting style',
  { size: '1024x1024' }
);

// Multiple variations from the same image
const variations = await service.createVariations(
  'https://example.com/product.png',
  'Professional product photo',
  [
    'with blue background',
    'with wooden surface',
    'with dramatic lighting'
  ]
);

console.log('Edit history:', service.getEditHistory());
```

### Transfert de style et transformation

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function applyStyleTransfer(imageSource, content, style, outputPath, size = '1024x1024') {
  const zai = await ZAI.create();

  const prompt = `${content} transformed into ${style} style, maintain composition and subject`;

  const response = await zai.images.generations.edit({
    prompt: prompt,
    images: [{ url: imageSource }],
    size: size
  });

  const imageBase64 = response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    content: content,
    style: style
  };
}

// Usage - Apply different styles to the same image
await applyStyleTransfer(
  './portrait.jpg',
  'Portrait photograph',
  'oil painting',
  './portrait_oil.png'
);

await applyStyleTransfer(
  'https://example.com/city.jpg',
  'City landscape',
  'watercolor',
  './city_watercolor.png'
);

await applyStyleTransfer(
  './product.png',
  'Product photo',
  'minimalist illustration',
  './product_minimal.png'
);
```

### Remplacement d'éléments

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function replaceElement(imageSource, baseScene, replaceWhat, replaceWith, outputPath, size = '1024x1024') {
  const zai = await ZAI.create();

  const prompt = `${baseScene}, replace ${replaceWhat} with ${replaceWith}, keep everything else identical`;

  const response = await zai.images.generations.edit({
    prompt: prompt,
    images: [{ url: imageSource }],
    size: size
  });

  const imageBase64 = response.data[0].base64;
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync(outputPath, buffer);

  return {
    path: outputPath,
    modification: `${replaceWhat} → ${replaceWith}`
  };
}

// Usage
await replaceElement(
  './workspace.jpg',
  'Office workspace with laptop',
  'laptop',
  'desktop computer with dual monitors',
  './workspace_desktop.png'
);

await replaceElement(
  'https://example.com/living-room.jpg',
  'Living room interior with sofa',
  'blue sofa',
  'brown leather sofa',
  './living_room_leather.png'
);
```

## Bonnes pratiques

### 1. Prompts d'édition efficaces

```javascript
function buildEditPrompt(baseDescription, modification, preserveElements = []) {
  const components = [
    baseDescription,
    modification
  ];

  if (preserveElements.length > 0) {
    components.push(`keep ${preserveElements.join(', ')} unchanged`);
  }

  components.push('maintain overall composition');

  return components.filter(Boolean).join(', ');
}

// Usage
const editPrompt = buildEditPrompt(
  'Professional headshot photo',
  'change background to modern office',
  ['lighting', 'pose', 'expression']
);

// Result: "Professional headshot photo, change background to modern office, keep lighting, pose, expression unchanged, maintain overall composition"
```

### 2. Choix de la taille selon le type d'édition

```javascript
function selectSizeForEdit(editType) {
  const sizeMap = {
    'background-change': '1440x720',
    'style-transfer': '1024x1024',
    'color-adjustment': '1024x1024',
    'element-replacement': '1344x768',
    'composition-change': '1152x864',
    'portrait-edit': '768x1344',
    'landscape-edit': '1344x768'
  };

  return sizeMap[editType] || '1024x1024';
}

// Usage
const size = selectSizeForEdit('background-change');
await editImage('Replace background with beach scene', './beach_bg.png', size);
```

### 3. Gestion d'erreurs avec retry

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function safeEditImage(imageSource, editPrompt, size, outputPath, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const zai = await ZAI.create();

      const response = await zai.images.generations.edit({
        prompt: editPrompt,
        images: [{ url: imageSource }],
        size: size
      });

      if (!response.data || !response.data[0] || !response.data[0].base64) {
        throw new Error('Invalid response from image editing API');
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

## Cas d'usage courants d'édition d'images

1. **Remplacement d'arrière-plan** : changer ou supprimer les arrière-plans des photos
2. **Transformation de style** : convertir des photos en peintures, illustrations, etc.
3. **Ajustement des couleurs** : changer les palettes, la saturation, l'ambiance
4. **Modification d'éléments** : remplacer ou modifier des éléments précis
5. **Changements de composition** : ajuster le cadrage, l'orientation, la disposition
6. **Ajustements d'éclairage** : modifier la lumière, les ombres, les hautes lumières
7. **Redesign d'assets** : moderniser ou rebrander des designs existants
8. **Amélioration de la qualité** : améliorer la qualité visuelle globale
9. **Création de variantes** : générer plusieurs versions d'une image
10. **Conversion de format** : transformer entre différents styles ou formats

## Exemples d'intégration

### Point d'accès API Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());
app.use('/edited-images', express.static('edited-images'));

let zaiInstance;
const outputDir = './edited-images';

async function initZAI() {
  zaiInstance = await ZAI.create();
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
}

app.post('/api/edit-image', async (req, res) => {
  try {
    const { 
      imageSource,           // URL or base64 data URL
      editPrompt, 
      size = '1024x1024', 
      baseDescription = '' 
    } = req.body;

    if (!imageSource || !editPrompt) {
      return res.status(400).json({ 
        error: 'imageSource and editPrompt are required' 
      });
    }

    // Combine base description with edit instruction
    const fullPrompt = baseDescription 
      ? `${baseDescription}, ${editPrompt}`
      : editPrompt;

    const response = await zaiInstance.images.generations.edit({
      prompt: fullPrompt,
      images: [{ url: imageSource }],
      size: size
    });

    const imageBase64 = response.data[0].base64;
    const buffer = Buffer.from(imageBase64, 'base64');
    
    const filename = `edited_${Date.now()}.png`;
    const filepath = path.join(outputDir, filename);
    fs.writeFileSync(filepath, buffer);

    res.json({
      success: true,
      imageUrl: `/edited-images/${filename}`,
      editPrompt: fullPrompt,
      size: size
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.post('/api/create-variations', async (req, res) => {
  try {
    const { 
      imageSource,      // URL or base64 data URL
      baseDescription, 
      variations, 
      size = '1024x1024' 
    } = req.body;

    if (!imageSource || !baseDescription || !variations || !Array.isArray(variations)) {
      return res.status(400).json({ 
        error: 'imageSource, baseDescription and variations array are required' 
      });
    }

    const results = [];

    for (const variation of variations) {
      const fullPrompt = `${baseDescription}, ${variation}`;

      const response = await zaiInstance.images.generations.edit({
        prompt: fullPrompt,
        images: [{ url: imageSource }],
        size: size
      });

      const imageBase64 = response.data[0].base64;
      const buffer = Buffer.from(imageBase64, 'base64');
      
      const filename = `variation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.png`;
      const filepath = path.join(outputDir, filename);
      fs.writeFileSync(filepath, buffer);

      results.push({
        variation: variation,
        imageUrl: `/edited-images/${filename}`
      });
    }

    res.json({
      success: true,
      results: results
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
    console.log('Image editing API running on port 3000');
  });
});
```

## Intégration CLI dans les scripts

### Script shell pour l'édition par lot

```bash
#!/bin/bash

# Batch edit images with different styles
echo "Creating style variations..."

ORIGINAL_IMAGE="./product.jpg"
BASE="Professional product photo of laptop"

z-ai image-edit -p "$BASE, modern minimalist style, white background" -i "$ORIGINAL_IMAGE" -o "./variations/minimal.png" -s 1024x1024
z-ai image-edit -p "$BASE, dramatic lighting, dark background" -i "$ORIGINAL_IMAGE" -o "./variations/dramatic.png" -s 1024x1024
z-ai image-edit -p "$BASE, on wooden desk, natural lighting" -i "$ORIGINAL_IMAGE" -o "./variations/natural.png" -s 1024x1024

echo "Variations created successfully!"
```

## Dépannage

**Problème** : « SDK must be used in backend »
- **Solution** : s'assurer que z-ai-web-dev-sdk n'est utilisé que dans le code côté serveur

**Problème** : paramètre de taille invalide
- **Solution** : n'utiliser que les tailles prises en charge : 1024x1024, 768x1344, 864x1152, 1344x768, 1152x864, 1440x720, 720x1440

**Problème** : l'image éditée ne correspond pas à l'intention
- **Solution** : être plus précis dans les prompts d'édition. Indiquer ce qu'il faut changer ET ce qu'il faut préserver

**Problème** : commande CLI introuvable
- **Solution** : s'assurer que le CLI z-ai est correctement installé et présent dans le PATH

**Problème** : perte de qualité d'image après édition
- **Solution** : utiliser des options de taille plus grandes et inclure des termes de qualité dans les prompts

**Problème** : résultats incohérents entre les variantes
- **Solution** : inclure une description de base plus précise et des instructions de modification détaillées

## Conseils d'ingénierie des prompts d'édition

### Bons prompts d'édition
- ✓ "Change background to modern office, keep subject and lighting identical"
- ✓ "Transform to watercolor style, maintain composition and colors"
- ✓ "Replace red car with blue motorcycle, keep road and scenery unchanged"
- ✓ "Adjust to golden hour lighting, preserve all elements"

### Mauvais prompts d'édition
- ✗ "make it better"
- ✗ "change something"
- ✗ "different version"

### Composants d'un prompt d'édition
1. **Contexte de base** : ce que l'image représente actuellement
2. **Modification** : quels changements précis effectuer
3. **Préservation** : quels éléments conserver à l'identique
4. **Qualité** : qualité ou style de sortie souhaité

### Modèles d'édition efficaces

**Changements d'arrière-plan :**
```
"[Subject description], replace background with [new background], maintain subject lighting and pose"
```

**Transferts de style :**
```
"[Current description] transformed into [style name] style, preserve composition and key elements"
```

**Remplacement d'éléments :**
```
"[Scene description], replace [element A] with [element B], keep everything else identical"
```

**Ajustements de couleurs :**
```
"[Image description], change color scheme to [colors], maintain contrast and composition"
```

## Tailles d'images prises en charge

- `1024x1024` - Carré (idéal pour l'édition générale)
- `768x1344` - Portrait
- `864x1152` - Portrait
- `1344x768` - Paysage
- `1152x864` - Paysage
- `1440x720` - Paysage large
- `720x1440` - Portrait allongé

## À retenir

- Toujours utiliser z-ai-web-dev-sdk uniquement dans le code backend
- Le SDK est déjà installé - importer comme montré
- L'outil CLI est disponible pour une édition rapide d'images
- Être précis sur ce qu'il faut changer ET sur ce qu'il faut préserver
- Inclure la description de base pour un meilleur contexte
- Utiliser la taille appropriée selon le type d'édition
- Implémenter une logique de retry pour les applications en production
- Tester les prompts d'édition de manière itérative pour de meilleurs résultats
- Envisager de créer des variantes pour explorer les options
- Les images base64 doivent être décodées avant enregistrement
