---
name: Video Generation
version: "1.0.0"
category: "Autres"
tags:
  - video
  - generation
description: Implémente des capacités de génération vidéo par IA à l'aide du z-ai-web-dev-sdk. Utilise ce skill lorsque l'utilisateur a besoin de générer des vidéos à partir de prompts texte ou d'images, de créer du contenu vidéo par programmation, ou de construire des applications produisant des sorties vidéo. Prend en charge la gestion asynchrone des tâches avec polling du statut et récupération des résultats.
license: MIT
language: fr

---

# Skill Video Generation

Ce skill guide l'implémentation de la fonctionnalité de génération vidéo à l'aide du package z-ai-web-dev-sdk, permettant aux modèles d'IA de créer des vidéos à partir de descriptions texte ou d'images via un traitement de tâches asynchrone.

## Chemin du skill

**Emplacement du skill** : `{project_path}/skills/video-generation`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/video.ts` pour un exemple fonctionnel.

## Vue d'ensemble

La génération vidéo permet de construire des applications capables de créer du contenu vidéo à partir de prompts texte ou d'images, avec des paramètres personnalisables tels que la résolution, la fréquence d'images, la durée et les réglages de qualité. L'API repose sur un modèle de tâches asynchrone : vous créez une tâche puis interrogez son statut jusqu'à récupérer les résultats.

**IMPORTANT** : z-ai-web-dev-sdk DOIT être utilisé uniquement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme illustré dans les exemples ci-dessous.

## Utilisation du CLI (tâches simples)

Pour les tâches simples de génération vidéo, vous pouvez utiliser le z-ai CLI au lieu d'écrire du code. Le CLI gère automatiquement la création de la tâche et le polling, ce qui le rend idéal pour des tests rapides et des automatisations simples.

### Texte vers vidéo basique

```bash
# Generate video with automatic polling
z-ai video --prompt "A cat playing with a ball" --poll

# Using short options
z-ai video -p "Beautiful landscape with mountains" --poll
```

### Qualité et réglages personnalisés

```bash
# Quality mode (speed or quality)
z-ai video -p "Ocean waves at sunset" --quality quality --poll

# Custom resolution and FPS
z-ai video \
  -p "City timelapse" \
  --size "1920x1080" \
  --fps 60 \
  --poll

# Custom duration (5 or 10 seconds)
z-ai video -p "Fireworks display" --duration 10 --poll
```

### Image vers vidéo

**IMPORTANT** : pour le paramètre `image_url`, il est **fortement recommandé d'utiliser des données d'image encodées en base64** plutôt que des URLs. Cette approche est plus fiable et évite les problèmes potentiels de réseau ou les restrictions d'accès.

**Remarque** : faites correspondre le type MIME de l'URI de données au format réel de votre image (image/jpeg, image/png, image/webp, etc.) pour éviter les erreurs de décodage.

```bash
# Generate video from single image using base64 (RECOMMENDED)
# Convert your image to base64 with correct MIME type

# For PNG images
IMAGE_BASE64=$(base64 -i image.png)
z-ai video \
  --image-url "data:image/png;base64,${IMAGE_BASE64}" \
  --prompt "Make the scene come alive" \
  --poll

# For JPEG images
IMAGE_BASE64=$(base64 -i photo.jpg)
z-ai video \
  --image-url "data:image/jpeg;base64,${IMAGE_BASE64}" \
  --prompt "Make the scene come alive" \
  --poll

# For WebP images
IMAGE_BASE64=$(base64 -i image.webp)
z-ai video \
  --image-url "data:image/webp;base64,${IMAGE_BASE64}" \
  --prompt "Make the scene come alive" \
  --poll

# Using URL (less recommended, may have reliability issues)
z-ai video \
  -i "https://example.com/photo.jpg" \
  -p "Add motion to this scene" \
  --poll
```

### Mode première/dernière frame

**IMPORTANT** : pour une fiabilité optimale, utilisez des images encodées en base64 plutôt que des URLs. Assurez-vous que le type MIME correspond au format réel de chaque image.

```bash
# Generate video between two frames using base64 (RECOMMENDED)
# Make sure to use the correct MIME type for each image

# Example with PNG images
START_BASE64=$(base64 -i start.png)
END_BASE64=$(base64 -i end.png)
z-ai video \
  --image-url "data:image/png;base64,${START_BASE64},data:image/png;base64,${END_BASE64}" \
  --prompt "Smooth transition between frames" \
  --poll

# Example with JPEG images
START_BASE64=$(base64 -i start.jpg)
END_BASE64=$(base64 -i end.jpg)
z-ai video \
  --image-url "data:image/jpeg;base64,${START_BASE64},data:image/jpeg;base64,${END_BASE64}" \
  --prompt "Smooth transition between frames" \
  --poll

# Using URLs (less recommended)
z-ai video \
  --image-url "https://example.com/start.png,https://example.com/end.png" \
  --prompt "Smooth transition between frames" \
  --poll
```

### Avec génération audio

```bash
# Generate video with AI-generated audio effects
z-ai video \
  -p "Thunder storm approaching" \
  --with-audio \
  --poll
```

### Sauvegarde de la sortie

```bash
# Save task result to JSON file
z-ai video \
  -p "Sunrise over mountains" \
  --poll \
  -o video_result.json
```

### Paramètres de polling personnalisés

```bash
# Customize polling behavior
z-ai video \
  -p "Dancing robot" \
  --poll \
  --poll-interval 10 \
  --max-polls 30

# Create task without polling (get task ID)
z-ai video -p "Abstract art animation" -o task.json
```

### Paramètres du CLI

- `--prompt, -p <text>` : Optionnel — Description texte de la vidéo
- `--image-url, -i <data>` : Optionnel — **De préférence des données d'image encodées en base64** (ex. "data:image/png;base64,iVBORw..."). Les URLs sont également prises en charge mais moins recommandées. Pour deux images, utilisez des valeurs séparées par des virgules.
- `--quality, -q <mode>` : Optionnel — Mode de sortie : `speed` ou `quality` (défaut : speed)
- `--with-audio` : Optionnel — Génère des effets audio par IA (défaut : false)
- `--size, -s <resolution>` : Optionnel — Résolution de la vidéo (ex. "1920x1080")
- `--fps <rate>` : Optionnel — Fréquence d'images : 30 ou 60 (défaut : 30)
- `--duration, -d <seconds>` : Optionnel — Durée : 5 ou 10 secondes (défaut : 5)
- `--model, -m <model>` : Optionnel — Nom du modèle à utiliser
- `--poll` : Optionnel — Interroge automatiquement jusqu'à la fin de la tâche
- `--poll-interval <seconds>` : Optionnel — Intervalle de polling (défaut : 5)
- `--max-polls <count>` : Optionnel — Nombre maximum de tentatives de polling (défaut : 60)
- `--output, -o <path>` : Optionnel — Chemin du fichier de sortie (format JSON)

### Résolutions prises en charge

- `1024x1024`
- `768x1344`
- `864x1152`
- `1344x768`
- `1152x864`
- `1440x720`
- `720x1440`
- `1920x1080` (et autres résolutions standard)

### Vérifier le statut d'une tâche plus tard

Si vous créez une tâche sans `--poll`, vous pouvez vérifier son statut ultérieurement :

```bash
# Get the task ID from the initial response
z-ai async-result --id "task-id-here" --poll
```

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Des tests rapides de génération vidéo
- La création d'une vidéo simple et ponctuelle
- Des scripts d'automatisation en ligne de commande
- Le test de différents prompts et réglages

**Utilisez le SDK pour :**
- La génération vidéo par lots avec logique personnalisée
- L'intégration dans des applications web
- La gestion personnalisée de files de tâches
- Des applications de production avec workflows complexes

## Workflow de génération vidéo

La génération vidéo suit un modèle asynchrone en deux étapes :

1. **Créer la tâche** : soumettre la requête de génération vidéo et recevoir un ID de tâche
2. **Interroger les résultats** : consulter le statut de la tâche jusqu'à complétion et récupérer l'URL de la vidéo

## Implémentation basique de la génération vidéo

### Génération simple texte vers vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function generateVideo(prompt) {
  try {
    const zai = await ZAI.create();

    // Create video generation task
    const task = await zai.video.generations.create({
      prompt: prompt,
      quality: 'speed', // 'speed' or 'quality'
      with_audio: false,
      size: '1920x1080',
      fps: 30,
      duration: 5
    });

    console.log('Task ID:', task.id);
    console.log('Task Status:', task.task_status);

    // Poll for results
    let result = await zai.async.result.query(task.id);
    let pollCount = 0;
    const maxPolls = 60;
    const pollInterval = 5000; // 5 seconds

    while (result.task_status === 'PROCESSING' && pollCount < maxPolls) {
      pollCount++;
      console.log(`Polling ${pollCount}/${maxPolls}: Status is ${result.task_status}`);
      await new Promise(resolve => setTimeout(resolve, pollInterval));
      result = await zai.async.result.query(task.id);
    }

    if (result.task_status === 'SUCCESS') {
      // Get video URL from multiple possible fields
      const videoUrl = result.video_result?.[0]?.url ||
                      result.video_url ||
                      result.url ||
                      result.video;
      console.log('Video URL:', videoUrl);
      return videoUrl;
    } else {
      console.log('Task failed or still processing');
      return null;
    }
  } catch (error) {
    console.error('Video generation failed:', error.message);
    throw error;
  }
}

// Usage
const videoUrl = await generateVideo('A cat is playing with a ball.');
console.log('Generated video:', videoUrl);
```

### Génération image vers vidéo

**IMPORTANT** : le paramètre `image_url` accepte à la fois des données d'image encodées en base64 et des URLs, mais **l'encodage base64 est fortement recommandé** pour une meilleure fiabilité et pour éviter les problèmes liés au réseau.

**Critique** : faites toujours correspondre le type MIME de votre URI de données base64 au format réel de l'image pour éviter les erreurs de décodage.

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

// Helper function to detect MIME type from file extension
function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp'
  };
  return mimeTypes[ext] || 'image/jpeg'; // Default to JPEG if unknown
}

async function generateVideoFromImage(imagePath, prompt) {
  const zai = await ZAI.create();

  // Method 1: Using base64-encoded image (RECOMMENDED)
  // Automatically detect MIME type from file extension
  const imageBuffer = fs.readFileSync(imagePath);
  const mimeType = getMimeType(imagePath);
  const base64Image = `data:${mimeType};base64,${imageBuffer.toString('base64')}`;

  const task = await zai.video.generations.create({
    image_url: base64Image,  // Base64 data string with correct MIME type
    prompt: prompt,
    quality: 'quality',
    duration: 5,
    fps: 30
  });

  return task;
}

// Method 2: Using URL (less recommended)
async function generateVideoFromImageUrl(imageUrl, prompt) {
  const zai = await ZAI.create();

  const task = await zai.video.generations.create({
    image_url: imageUrl,  // URL string
    prompt: prompt,
    quality: 'quality',
    duration: 5,
    fps: 30
  });

  return task;
}

// Usage examples
const task1 = await generateVideoFromImage(
  './images/photo.jpg',  // Works with JPEG
  'Animate this scene with gentle motion'
);

const task2 = await generateVideoFromImage(
  './images/graphic.png',  // Works with PNG
  'Add dynamic movement'
);

const task3 = await generateVideoFromImage(
  './images/animation.webp',  // Works with WebP
  'Bring this to life'
);
```

### Image vers vidéo avec frames de début et de fin

**IMPORTANT** : pour le mode keyframes, les images encodées en base64 sont **fortement recommandées** par rapport aux URLs afin de garantir une génération vidéo cohérente et fiable. Utilisez toujours le type MIME correct pour chaque image.

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

// Helper function to detect MIME type from file extension
function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp'
  };
  return mimeTypes[ext] || 'image/jpeg';
}

async function generateVideoWithKeyframes(startImagePath, endImagePath, prompt) {
  const zai = await ZAI.create();

  // Method 1: Using base64-encoded images (RECOMMENDED)
  // Automatically detect MIME type for each image
  const startBuffer = fs.readFileSync(startImagePath);
  const endBuffer = fs.readFileSync(endImagePath);
  
  const startMimeType = getMimeType(startImagePath);
  const endMimeType = getMimeType(endImagePath);
  
  const startBase64 = `data:${startMimeType};base64,${startBuffer.toString('base64')}`;
  const endBase64 = `data:${endMimeType};base64,${endBuffer.toString('base64')}`;

  const task = await zai.video.generations.create({
    image_url: [startBase64, endBase64],  // Array of base64 strings with correct MIME types
    prompt: prompt,
    quality: 'quality',
    duration: 10,
    fps: 30
  });

  console.log('Task created with keyframes:', task.id);
  return task;
}

// Method 2: Using URLs (less recommended)
async function generateVideoWithKeyframesUrl(startImageUrl, endImageUrl, prompt) {
  const zai = await ZAI.create();

  const task = await zai.video.generations.create({
    image_url: [startImageUrl, endImageUrl],  // Array of URL strings
    prompt: prompt,
    quality: 'quality',
    duration: 10,
    fps: 30
  });

  console.log('Task created with keyframes:', task.id);
  return task;
}

// Usage examples with different formats
const task1 = await generateVideoWithKeyframes(
  './frames/start.jpg',  // JPEG start frame
  './frames/end.jpg',    // JPEG end frame
  'Smooth transition between these scenes'
);

const task2 = await generateVideoWithKeyframes(
  './frames/start.png',  // PNG start frame
  './frames/end.webp',   // WebP end frame - different formats work!
  'Morphing effect between images'
);
```

## Gestion asynchrone des résultats

### Interroger le statut d'une tâche

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function checkTaskStatus(taskId) {
  try {
    const zai = await ZAI.create();
    const result = await zai.async.result.query(taskId);

    console.log('Task Status:', result.task_status);

    if (result.task_status === 'SUCCESS') {
      // Extract video URL from result
      const videoUrl = result.video_result?.[0]?.url ||
                      result.video_url ||
                      result.url ||
                      result.video;
      if (videoUrl) {
        console.log('Video URL:', videoUrl);
        return { success: true, url: videoUrl };
      }
    } else if (result.task_status === 'PROCESSING') {
      console.log('Task is still processing');
      return { success: false, status: 'processing' };
    } else if (result.task_status === 'FAIL') {
      console.log('Task failed');
      return { success: false, status: 'failed' };
    }
  } catch (error) {
    console.error('Query failed:', error.message);
    throw error;
  }
}

// Usage
const status = await checkTaskStatus('your-task-id-here');
```

### Polling avec backoff exponentiel

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function pollWithBackoff(taskId) {
  const zai = await ZAI.create();
  
  let pollInterval = 5000; // Start with 5 seconds
  const maxInterval = 30000; // Max 30 seconds
  const maxPolls = 40;
  let pollCount = 0;

  while (pollCount < maxPolls) {
    const result = await zai.async.result.query(taskId);
    pollCount++;

    if (result.task_status === 'SUCCESS') {
      const videoUrl = result.video_result?.[0]?.url ||
                      result.video_url ||
                      result.url ||
                      result.video;
      return { success: true, url: videoUrl };
    }

    if (result.task_status === 'FAIL') {
      return { success: false, error: 'Task failed' };
    }

    // Exponential backoff
    console.log(`Poll ${pollCount}: Waiting ${pollInterval / 1000}s...`);
    await new Promise(resolve => setTimeout(resolve, pollInterval));
    pollInterval = Math.min(pollInterval * 1.5, maxInterval);
  }

  return { success: false, error: 'Timeout' };
}
```

## Cas d'usage avancés

### Gestionnaire de file d'attente de génération vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class VideoGenerationQueue {
  constructor() {
    this.tasks = new Map();
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async createVideo(params) {
    const task = await this.zai.video.generations.create(params);
    
    this.tasks.set(task.id, {
      taskId: task.id,
      status: task.task_status,
      params: params,
      createdAt: new Date()
    });

    return task.id;
  }

  async checkTask(taskId) {
    const result = await this.zai.async.result.query(taskId);
    
    const taskInfo = this.tasks.get(taskId);
    if (taskInfo) {
      taskInfo.status = result.task_status;
      taskInfo.lastChecked = new Date();
      
      if (result.task_status === 'SUCCESS') {
        taskInfo.videoUrl = result.video_result?.[0]?.url ||
                          result.video_url ||
                          result.url ||
                          result.video;
      }
    }

    return result;
  }

  async pollTask(taskId, options = {}) {
    const maxPolls = options.maxPolls || 60;
    const pollInterval = options.pollInterval || 5000;
    
    let pollCount = 0;

    while (pollCount < maxPolls) {
      const result = await this.checkTask(taskId);
      
      if (result.task_status === 'SUCCESS' || result.task_status === 'FAIL') {
        return result;
      }

      pollCount++;
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }

    throw new Error('Task polling timeout');
  }

  getTask(taskId) {
    return this.tasks.get(taskId);
  }

  getAllTasks() {
    return Array.from(this.tasks.values());
  }
}

// Usage
const queue = new VideoGenerationQueue();
await queue.initialize();

const taskId = await queue.createVideo({
  prompt: 'A sunset over the ocean',
  quality: 'quality',
  duration: 5
});

const result = await queue.pollTask(taskId);
console.log('Video ready:', result.video_result?.[0]?.url);
```

### Génération vidéo par lots

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function generateMultipleVideos(prompts) {
  const zai = await ZAI.create();
  const tasks = [];

  // Create all tasks
  for (const prompt of prompts) {
    const task = await zai.video.generations.create({
      prompt: prompt,
      quality: 'speed',
      duration: 5
    });
    tasks.push({ taskId: task.id, prompt: prompt });
  }

  console.log(`Created ${tasks.length} video generation tasks`);

  // Poll all tasks
  const results = [];
  for (const task of tasks) {
    const result = await pollTaskUntilComplete(zai, task.taskId);
    results.push({
      prompt: task.prompt,
      taskId: task.taskId,
      ...result
    });
  }

  return results;
}

async function pollTaskUntilComplete(zai, taskId) {
  let pollCount = 0;
  const maxPolls = 60;

  while (pollCount < maxPolls) {
    const result = await zai.async.result.query(taskId);
    
    if (result.task_status === 'SUCCESS') {
      return {
        success: true,
        url: result.video_result?.[0]?.url ||
             result.video_url ||
             result.url ||
             result.video
      };
    }

    if (result.task_status === 'FAIL') {
      return { success: false, error: 'Generation failed' };
    }

    pollCount++;
    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  return { success: false, error: 'Timeout' };
}

// Usage
const prompts = [
  'A cat playing with yarn',
  'A dog running in a park',
  'A bird flying in the sky'
];

const videos = await generateMultipleVideos(prompts);
videos.forEach(video => {
  console.log(`${video.prompt}: ${video.success ? video.url : video.error}`);
});
```

## Paramètres de configuration

### Paramètres de génération vidéo

| Paramètre | Type | Obligatoire | Description | Défaut |
|-----------|------|----------|-------------|---------|
| `prompt` | string | Optionnel* | Description texte de la vidéo | - |
| `image_url` | string \| string[] | Optionnel* | URL(s) des images pour la génération | - |
| `quality` | string | Optionnel | Mode de sortie : `'speed'` ou `'quality'` | `'speed'` |
| `with_audio` | boolean | Optionnel | Génère des effets audio par IA | `false` |
| `size` | string | Optionnel | Résolution de la vidéo (ex. `'1920x1080'`) | - |
| `fps` | number | Optionnel | Fréquence d'images : `30` ou `60` | `30` |
| `duration` | number | Optionnel | Durée en secondes : `5` ou `10` | `5` |
| `model` | string | Optionnel | Nom du modèle | - |

*Remarque : au moins l'un des deux, `prompt` ou `image_url`, doit être fourni.

### Formats d'URL d'image

```javascript
// Single image (starting frame)
image_url: 'https://example.com/image.jpg'

// Multiple images (start and end frames)
image_url: [
  'https://example.com/start.jpg',
  'https://example.com/end.jpg'
]
```

### Valeurs de statut de tâche

- `PROCESSING` : la tâche est en cours de traitement
- `SUCCESS` : la tâche s'est terminée avec succès
- `FAIL` : la tâche a échoué

## Formats de réponse

### Réponse de création de tâche

```json
{
  "id": "task-12345",
  "task_status": "PROCESSING",
  "model": "video-model-v1"
}
```

### Réponse d'interrogation de tâche (succès)

```json
{
  "task_status": "SUCCESS",
  "model": "video-model-v1",
  "request_id": "req-67890",
  "video_result": [
    {
      "url": "https://cdn.example.com/generated-video.mp4"
    }
  ]
}
```

### Réponse d'interrogation de tâche (en cours)

```json
{
  "task_status": "PROCESSING",
  "id": "task-12345",
  "model": "video-model-v1"
}
```

## Bonnes pratiques

### 1. Stratégie de polling

```javascript
// Recommended polling implementation
async function smartPoll(zai, taskId) {
  // Check immediately (some tasks complete fast)
  let result = await zai.async.result.query(taskId);
  
  if (result.task_status !== 'PROCESSING') {
    return result;
  }

  // Start polling with reasonable intervals
  let interval = 5000; // 5 seconds
  let maxPolls = 60; // 5 minutes total
  
  for (let i = 0; i < maxPolls; i++) {
    await new Promise(resolve => setTimeout(resolve, interval));
    result = await zai.async.result.query(taskId);
    
    if (result.task_status !== 'PROCESSING') {
      return result;
    }
  }
  
  throw new Error('Task timeout');
}
```

### 2. Gestion des erreurs

```javascript
async function safeVideoGeneration(params) {
  try {
    const zai = await ZAI.create();
    
    // Validate parameters
    if (!params.prompt && !params.image_url) {
      throw new Error('Either prompt or image_url is required');
    }
    
    const task = await zai.video.generations.create(params);
    const result = await smartPoll(zai, task.id);
    
    if (result.task_status === 'SUCCESS') {
      const videoUrl = result.video_result?.[0]?.url ||
                      result.video_url ||
                      result.url ||
                      result.video;
      
      if (!videoUrl) {
        throw new Error('Video URL not found in response');
      }
      
      return {
        success: true,
        url: videoUrl,
        taskId: task.id
      };
    } else {
      return {
        success: false,
        error: 'Video generation failed',
        taskId: task.id
      };
    }
  } catch (error) {
    console.error('Video generation error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 3. Gestion des ressources

- Mettez l'instance ZAI en cache pour plusieurs générations vidéo
- Stockez les IDs de tâches pour les opérations de longue durée
- Nettoyez les tâches terminées de votre système de suivi
- Implémentez des mécanismes de timeout pour éviter un polling infini

### 4. Arbitrage qualité vs vitesse

```javascript
// Fast generation for previews or high volume
const quickVideo = await zai.video.generations.create({
  prompt: 'A cat playing',
  quality: 'speed',
  duration: 5,
  fps: 30
});

// High quality for final production
const qualityVideo = await zai.video.generations.create({
  prompt: 'A cat playing',
  quality: 'quality',
  duration: 10,
  fps: 60,
  size: '1920x1080'
});
```

### 5. Considérations de sécurité

- Validez toutes les entrées utilisateur avant de créer des tâches
- Implémentez une limitation de débit pour les endpoints de génération vidéo
- Stockez et validez les IDs de tâches de manière sécurisée
- N'exposez jamais les identifiants du SDK dans du code côté client
- Définissez des timeouts raisonnables pour les opérations de polling

## Cas d'usage courants

1. **Contenu pour réseaux sociaux** : générer de courts clips vidéo pour des publications et des stories
2. **Supports marketing** : créer des vidéos de démonstration de produits
3. **Éducation** : générer des explications visuelles et des tutoriels
4. **Divertissement** : créer du contenu animé à partir de descriptions
5. **Prototypage** : maquettes vidéo rapides pour des présentations
6. **Développement de jeux** : générer des cinématiques ou des vidéos d'arrière-plan
7. **Automatisation de contenu** : génération vidéo en masse pour divers usages

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

// Create video generation task
app.post('/api/video/create', async (req, res) => {
  try {
    const { prompt, image_url, quality, duration } = req.body;

    if (!prompt && !image_url) {
      return res.status(400).json({ 
        error: 'Either prompt or image_url is required' 
      });
    }

    // Note: image_url should preferably be base64-encoded image data
    // Format: "data:image/jpeg;base64,..." or array of such strings
    // URLs are also supported but less recommended
    const task = await zaiInstance.video.generations.create({
      prompt,
      image_url,  // Accepts base64 data or URL
      quality: quality || 'speed',
      duration: duration || 5,
      fps: 30
    });

    res.json({
      success: true,
      taskId: task.id,
      status: task.task_status
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Query task status
app.get('/api/video/status/:taskId', async (req, res) => {
  try {
    const { taskId } = req.params;
    const result = await zaiInstance.async.result.query(taskId);

    const response = {
      taskId: taskId,
      status: result.task_status
    };

    if (result.task_status === 'SUCCESS') {
      response.videoUrl = result.video_result?.[0]?.url ||
                         result.video_url ||
                         result.url ||
                         result.video;
    }

    res.json(response);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

initZAI().then(() => {
  app.listen(3000, () => {
    console.log('Video generation API running on port 3000');
  });
});
```

### Mises à jour temps réel via WebSocket

```javascript
import WebSocket from 'ws';
import ZAI from 'z-ai-web-dev-sdk';

const wss = new WebSocket.Server({ port: 8080 });
let zaiInstance;

async function initZAI() {
  zaiInstance = await ZAI.create();
}

wss.on('connection', (ws) => {
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);

      if (data.action === 'generate') {
        // Create task
        const task = await zaiInstance.video.generations.create(data.params);
        
        ws.send(JSON.stringify({
          type: 'task_created',
          taskId: task.id
        }));

        // Poll for results and send updates
        pollAndNotify(ws, task.id);
      }
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        message: error.message
      }));
    }
  });
});

async function pollAndNotify(ws, taskId) {
  let pollCount = 0;
  const maxPolls = 60;

  while (pollCount < maxPolls) {
    const result = await zaiInstance.async.result.query(taskId);
    
    ws.send(JSON.stringify({
      type: 'status_update',
      taskId: taskId,
      status: result.task_status
    }));

    if (result.task_status === 'SUCCESS') {
      ws.send(JSON.stringify({
        type: 'complete',
        taskId: taskId,
        videoUrl: result.video_result?.[0]?.url ||
                 result.video_url ||
                 result.url ||
                 result.video
      }));
      break;
    }

    if (result.task_status === 'FAIL') {
      ws.send(JSON.stringify({
        type: 'failed',
        taskId: taskId
      }));
      break;
    }

    pollCount++;
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
}

initZAI();
```

## Dépannage

**Problème** : "Le SDK doit être utilisé en backend"
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé et utilisé que dans du code côté serveur

**Problème** : la tâche reste indéfiniment en statut PROCESSING
- **Solution** : implémentez des mécanismes de timeout appropriés et tenez compte de la complexité et de la durée de la vidéo

**Problème** : URL vidéo introuvable dans la réponse
- **Solution** : vérifiez les différents champs de réponse possibles (video_result, video_url, url, video) comme montré dans les exemples

**Problème** : la tâche échoue immédiatement
- **Solution** : vérifiez que les paramètres respectent les exigences (prompt/image_url valides, valeurs prises en charge pour quality/fps/duration)

**Problème** : génération vidéo lente
- **Solution** : utilisez le mode de qualité 'speed', réduisez la durée/le fps, ou envisagez des prompts plus simples

**Problème** : timeout du polling
- **Solution** : augmentez maxPolls ou pollInterval en fonction de la durée et des réglages de qualité de la vidéo

## Conseils de performance

1. **Utilisez des réglages de qualité adaptés** : choisissez 'speed' pour des résultats rapides, 'quality' pour la production finale
2. **Commencez par des durées courtes** : testez avec des vidéos de 5 secondes avant de générer du contenu plus long
3. **Implémentez un polling intelligent** : utilisez un backoff exponentiel pour réduire les appels API
4. **Mettez l'instance ZAI en cache** : réutilisez la même instance pour plusieurs générations vidéo
5. **Traitement parallèle** : créez plusieurs tâches simultanément et interrogez-les indépendamment
6. **Supervisez et journalisez** : suivez les temps de complétion des tâches pour optimiser votre stratégie de polling

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- La génération vidéo est asynchrone — implémentez toujours un polling correct
- Vérifiez plusieurs champs de réponse pour l'URL vidéo afin d'assurer la compatibilité
- Implémentez des timeouts pour éviter des boucles de polling infinies
- Gérez les trois statuts de tâche : PROCESSING, SUCCESS et FAIL
- Tenez compte des limites de débit (rate limits) et ajoutez des délais appropriés entre les requêtes
- Le SDK est déjà installé — importez-le comme montré dans les exemples
