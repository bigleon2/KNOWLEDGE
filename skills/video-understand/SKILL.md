---
name: video-understand
version: "1.0.0"
category: "IA & Media"
tags:
  - video
  - understand
description: Implémente des capacités spécialisées de compréhension vidéo avec le z-ai-web-dev-sdk. Utilise ce skill lorsque l'utilisateur a besoin d'analyser du contenu vidéo, de comprendre les mouvements et les séquences temporelles, d'extraire des informations de frames vidéo, de décrire des scènes vidéo, ou de réaliser des analyses vidéo par IA. Optimisé pour les formats MP4, AVI, MOV et autres formats vidéo courants.
license: MIT
language: fr

read_when:
  - Déclencher quand la demande concerne : implémente des capacités spécialisées de compréhension vidéo avec le z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : vidéo, formats, implémente
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Skill Video Understanding

Ce skill fournit une fonctionnalité spécialisée de compréhension vidéo à l'aide du package z-ai-web-dev-sdk, permettant aux modèles d'IA d'analyser, de décrire et d'extraire des informations de contenus vidéo, y compris les mouvements, les séquences temporelles et les changements de scène.

## Chemin du skill

**Emplacement du skill** : `{project_path}/skills/video-understand`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/video-understand.ts` pour un exemple fonctionnel.

## Vue d'ensemble

La compréhension vidéo se concentre spécifiquement sur l'analyse de contenus vidéo, avec les capacités suivantes :
- Compréhension et description des scènes vidéo
- Détection des actions et des mouvements
- Analyse des séquences temporelles
- Détection d'événements dans les vidéos
- Résumé du contenu vidéo
- Détection des changements de scène
- Suivi des personnes et des objets à travers les frames
- Analyse de contenus audio-visuels (le cas échéant)

**IMPORTANT** : z-ai-web-dev-sdk DOIT être utilisé uniquement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme illustré dans les exemples ci-dessous.

## Utilisation du CLI (tâches simples)

Pour des tâches rapides d'analyse vidéo, vous pouvez utiliser le z-ai CLI au lieu d'écrire du code. C'est idéal pour des descriptions vidéo simples, des tests ou des automatisations.

### Analyse vidéo basique

```bash
# Analyze a video from URL
z-ai vision --prompt "Summarize what happens in this video" --image "https://example.com/video.mp4"

# Note: Use --image flag for video URLs as well
z-ai vision -p "Describe the key events" -i "https://example.com/presentation.mp4"
```

### Analyser des vidéos locales

```bash
# Analyze a local video file
z-ai vision -p "What activities are shown in this video?" -i "./recording.mp4"

# Save response to file
z-ai vision -p "Provide a detailed summary" -i "./meeting.mp4" -o summary.json
```

### Analyse vidéo avancée

```bash
# Complex scene understanding with thinking
z-ai vision \
  -p "Analyze this video and identify: 1) Main events, 2) People and their actions, 3) Timeline of key moments" \
  -i "./event.mp4" \
  --thinking \
  -o analysis.json

# Action detection
z-ai vision \
  -p "Identify all actions performed by people in this video" \
  -i "./sports.mp4" \
  --thinking
```

### Sortie en streaming

```bash
# Stream the video analysis
z-ai vision -p "Describe this video content" -i "./video.mp4" --stream
```

### Paramètres du CLI

- `--prompt, -p <text>` : **Obligatoire** — Question ou instruction concernant la vidéo
- `--image, -i <URL ou chemin>` : Optionnel — URL de la vidéo ou chemin d'un fichier local (malgré son nom, fonctionne aussi pour les vidéos)
- `--thinking, -t` : Optionnel — Active le raisonnement en chaîne de pensée pour les analyses complexes (défaut : désactivé)
- `--output, -o <path>` : Optionnel — Chemin du fichier de sortie (format JSON)
- `--stream` : Optionnel — Diffuse la réponse en temps réel

### Formats vidéo pris en charge

- MP4 (.mp4) - Format le plus largement pris en charge
- AVI (.avi) - Audio Video Interleave
- MOV (.mov) - Format QuickTime
- WebM (.webm) - Format optimisé pour le web
- MKV (.mkv) - Format Matroska
- FLV (.flv) - Format Flash Video

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Des résumés vidéo rapides
- Une analyse vidéo ponctuelle
- Le test des capacités de compréhension vidéo
- Des scripts d'automatisation simples
- La génération de descriptions vidéo

**Utilisez le SDK pour :**
- Des conversations multi-tours à propos de vidéos
- Des pipelines complexes de traitement vidéo
- Des applications de production avec gestion d'erreurs
- Une intégration personnalisée avec la logique de traitement vidéo
- Un traitement vidéo par lots avec workflows personnalisés

## Approche recommandée

Pour de meilleures performances et une meilleure fiabilité avec des vidéos locales, envisagez :
1. De téléverser les vidéos sur un CDN et d'utiliser des URLs
2. Pour les vidéos courtes, de convertir les images clés en images pour une analyse plus rapide
3. Pour les vidéos longues, de découper ou d'échantillonner à intervalles réguliers

## Implémentation basique de la compréhension vidéo

### Analyse d'une seule vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function analyzeVideo(videoUrl, prompt) {
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
            type: 'video_url',
            video_url: {
              url: videoUrl
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
const summary = await analyzeVideo(
  'https://example.com/presentation.mp4',
  'Summarize the key points presented in this video'
);

const actionDetection = await analyzeVideo(
  'https://example.com/sports.mp4',
  'Identify and describe all athletic actions performed in this video'
);
```

### Compréhension des scènes vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function understandVideoScenes(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Analyze this video and provide:
1. Overall summary of the video content
2. Main scenes or segments (with approximate timestamps if possible)
3. Key people or characters and their roles
4. Important actions or events in chronological order
5. Setting and environment description
6. Overall mood or tone`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' } // Enable for detailed analysis
  });

  return response.choices[0]?.message?.content;
}

// Usage
const sceneAnalysis = await understandVideoScenes(
  'https://example.com/documentary.mp4'
);
```

### Détection des mouvements et actions

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function detectActions(videoUrl, specificAction = null) {
  const zai = await ZAI.create();

  const prompt = specificAction
    ? `Identify all instances of "${specificAction}" in this video. For each instance, describe when it occurs and provide details about how it's performed.`
    : 'Identify and describe all significant actions and movements in this video. Include who is performing them and when they occur.';

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' }
  });

  return response.choices[0]?.message?.content;
}

// Usage
const runningActions = await detectActions(
  'https://example.com/sports.mp4',
  'running'
);

const allActions = await detectActions(
  'https://example.com/activity.mp4'
);
```

### Extraction de la chronologie des événements

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function extractTimeline(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Create a detailed timeline of events in this video:
- Identify key moments and transitions
- Note approximate timing (beginning, middle, end or specific timestamps if visible)
- Describe what happens at each key point
- Identify any cause-and-effect relationships between events

Format as a chronological list.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' }
  });

  return response.choices[0]?.message?.content;
}
```

### Classification du contenu vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function classifyVideo(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Classify this video content:
1. Primary category (e.g., educational, entertainment, sports, news, tutorial)
2. Sub-category or genre
3. Target audience
4. Content style (professional, casual, documentary, etc.)
5. Key themes or topics
6. Suggested tags (10-15 keywords)

Format your response as structured JSON.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
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

## Cas d'usage avancés

### Conversation vidéo multi-tours

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class VideoConversation {
  constructor() {
    this.messages = [];
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async loadVideo(videoUrl, initialQuestion) {
    this.messages.push({
      role: 'user',
      content: [
        { type: 'text', text: initialQuestion },
        { type: 'video_url', video_url: { url: videoUrl } }
      ]
    });

    return this.getResponse();
  }

  async askFollowUp(question) {
    this.messages.push({
      role: 'user',
      content: [
        { type: 'text', text: question }
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
const conversation = new VideoConversation();
await conversation.initialize();

const initial = await conversation.loadVideo(
  'https://example.com/lecture.mp4',
  'What is the main topic of this lecture?'
);

const followup1 = await conversation.askFollowUp(
  'Can you explain the key concepts mentioned?'
);

const followup2 = await conversation.askFollowUp(
  'What examples were used to illustrate these concepts?'
);
```

### Évaluation de la qualité vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function assessVideoQuality(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Assess the quality of this video:
1. Visual quality (resolution, clarity, lighting) - Rate 1-10
2. Audio quality (if audio is present) - Rate 1-10
3. Camera work (stability, framing, composition) - Rate 1-10
4. Production value (editing, transitions, effects) - Rate 1-10
5. Content clarity (is the message clear?) - Rate 1-10
6. Pacing (too fast, too slow, just right)
7. Technical issues (artifacts, blur, audio sync, etc.)
8. Overall rating - 1-10
9. Specific recommendations for improvement

Provide detailed feedback for each criterion.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' }
  });

  return response.choices[0]?.message?.content;
}
```

### Modération du contenu vidéo

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function moderateVideo(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Review this video for content moderation:
1. Check for any inappropriate or sensitive content
2. Identify any potential safety concerns
3. Note any content that might violate common community guidelines
4. Assess age-appropriateness
5. Identify any copyrighted material visible (logos, brands, music)
6. Overall safety rating: Safe / Caution / Review Required

Provide specific examples for any concerns identified.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' }
  });

  return response.choices[0]?.message?.content;
}
```

### Génération de transcription vidéo (description visuelle)

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function generateVisualTranscript(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Generate a detailed visual transcript of this video:
- Describe what's happening in each scene
- Note any text that appears on screen
- Describe important visual elements
- Mention any scene changes or transitions
- Include descriptions of people's actions and expressions

Format as a time-based narrative (e.g., "At the beginning...", "Then...", "Finally...").`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'disabled' }
  });

  return response.choices[0]?.message?.content;
}
```

### Analyse de vidéos sportives

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function analyzeSportsVideo(videoUrl, sport = null) {
  const zai = await ZAI.create();

  const prompt = sport
    ? `Analyze this ${sport} video in detail:
1. Identify players and their positions
2. Describe key plays and strategies
3. Note scoring events or important moments
4. Assess player performance
5. Identify any rule violations or fouls
6. Describe the pace and flow of the game`
    : `Analyze this sports video:
1. Identify the sport being played
2. Describe the key actions and plays
3. Note any scoring or significant events
4. Describe player movements and strategies
5. Overall assessment of the game or match`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' }
  });

  return response.choices[0]?.message?.content;
}
```

### Résumé de vidéos éducatives

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function summarizeEducationalVideo(videoUrl) {
  const zai = await ZAI.create();

  const prompt = `Summarize this educational video for students:
1. Main topic or learning objective
2. Key concepts explained (in order)
3. Important definitions or terminology
4. Examples used to illustrate concepts
5. Visual aids or demonstrations shown
6. Key takeaways or conclusions
7. Suggested review points

Format as a study guide.`;

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'video_url', video_url: { url: videoUrl } }
        ]
      }
    ],
    thinking: { type: 'enabled' }
  });

  return response.choices[0]?.message?.content;
}
```

## Traitement vidéo par lots

### Traiter plusieurs vidéos

```javascript
import ZAI from 'z-ai-web-dev-sdk';

class VideoBatchProcessor {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async processVideo(videoUrl, prompt) {
    const response = await this.zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'video_url', video_url: { url: videoUrl } }
          ]
        }
      ],
      thinking: { type: 'disabled' }
    });

    return response.choices[0]?.message?.content;
  }

  async processBatch(videoUrls, prompt) {
    const results = [];
    
    for (const videoUrl of videoUrls) {
      try {
        console.log(`Processing: ${videoUrl}`);
        const result = await this.processVideo(videoUrl, prompt);
        results.push({ videoUrl, success: true, result });
        
        // Add delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        results.push({ 
          videoUrl, 
          success: false, 
          error: error.message 
        });
      }
    }

    return results;
  }
}

// Usage
const processor = new VideoBatchProcessor();
await processor.initialize();

const videos = [
  'https://example.com/video1.mp4',
  'https://example.com/video2.mp4',
  'https://example.com/video3.mp4'
];

const results = await processor.processBatch(
  videos,
  'Provide a brief summary of this video suitable for a content catalog'
);
```

## Bonnes pratiques

### 1. Préparation des vidéos
- Utilisez des formats vidéo standard (MP4, MOV, AVI)
- Assurez-vous que les vidéos sont accessibles via des URLs publiques ou correctement encodées
- Pour les vidéos longues, envisagez de créer des extraits plus courts pour des analyses spécifiques
- Optimisez la taille des vidéos pour un traitement plus rapide
- Assurez-vous d'un bon éclairage et d'une bonne qualité audio dans les vidéos sources

### 2. Prompt engineering pour les vidéos
- Soyez précis sur les aspects temporels ("au début", "tout au long", "à la fin")
- Précisez le type d'analyse souhaité (actions, événements, scènes, etc.)
- Pour les vidéos longues, demandez des résumés ou les moments clés
- Utilisez le mode thinking pour un raisonnement temporel complexe
- Indiquez si vous souhaitez une organisation chronologique ou thématique

### 3. Gestion des erreurs

```javascript
async function safeVideoAnalysis(videoUrl, prompt) {
  try {
    const zai = await ZAI.create();
    
    const response = await zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'video_url', video_url: { url: videoUrl } }
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
    console.error('Video analysis error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 4. Optimisation des performances
- Mettez l'instance SDK en cache pour le traitement par lots
- Implémentez un throttle des requêtes (ajoutez des délais entre les requêtes)
- Traitez les vidéos de manière asynchrone lorsque c'est possible
- Pour les très longues vidéos, envisagez une analyse à intervalles spécifiques
- Utilisez le mode thinking approprié (désactivé pour les descriptions simples, activé pour les analyses complexes)

### 5. Considérations de sécurité
- Validez les URLs vidéo avant traitement
- Implémentez une limitation de débit pour les API publiques
- Assainissez les URLs vidéo fournies par l'utilisateur
- N'exposez jamais les identifiants du SDK dans du code côté client
- Implémentez une modération de contenu pour les vidéos téléversées par les utilisateurs
- Tenez compte des limites de taille des fichiers vidéo

## Cas d'usage courants

1. **Modération de contenu** : examiner automatiquement les vidéos téléversées pour vérifier leur conformité aux règles
2. **Catalogage vidéo** : générer des descriptions et des tags pour des vidéothèques
3. **Analyse sportive** : analyser des matchs, identifier les phases de jeu, évaluer les performances
4. **Contenu éducatif** : résumer des cours, créer des guides d'étude
5. **Sécurité et surveillance** : détecter des événements, suivre des activités (avec l'autorisation appropriée)
6. **Contrôle qualité** : évaluer la qualité de production des vidéos
7. **Réseaux sociaux** : générer des sous-titres et des descriptions de vidéos
8. **Formation et documentation** : analyser des vidéos de formation, créer de la documentation
9. **Enregistrement d'événements** : résumer des réunions, conférences, présentations
10. **Divertissement** : analyser films et émissions pour le contenu, les thèmes, les scènes

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

// Analyze video from URL
app.post('/api/analyze-video', async (req, res) => {
  try {
    const { videoUrl, prompt } = req.body;

    if (!videoUrl || !prompt) {
      return res.status(400).json({ 
        error: 'videoUrl and prompt are required' 
      });
    }

    const response = await zaiInstance.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'video_url', video_url: { url: videoUrl } }
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

// Get video summary
app.post('/api/video-summary', async (req, res) => {
  try {
    const { videoUrl } = req.body;

    if (!videoUrl) {
      return res.status(400).json({ error: 'videoUrl is required' });
    }

    const prompt = 'Provide a comprehensive summary of this video including: 1) Main content/topic, 2) Key events in chronological order, 3) Important people or subjects, 4) Overall takeaway.';

    const response = await zaiInstance.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'video_url', video_url: { url: videoUrl } }
          ]
        }
      ],
      thinking: { type: 'enabled' }
    });

    res.json({
      success: true,
      summary: response.choices[0]?.message?.content
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
    console.log('Video understanding API running on port 3000');
  });
});
```

### Route API Next.js

```javascript
// pages/api/video-understand.js
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
    const { videoUrl, prompt, enableThinking = false } = req.body;

    if (!videoUrl || !prompt) {
      return res.status(400).json({ 
        error: 'videoUrl and prompt are required' 
      });
    }

    const zai = await getZAI();

    const response = await zai.chat.completions.createVision({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'video_url', video_url: { url: videoUrl } }
          ]
        }
      ],
      thinking: { type: enableThinking ? 'enabled' : 'disabled' }
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

**Problème** : "Le SDK doit être utilisé en backend"
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé et utilisé que dans du code côté serveur, jamais dans du code client/navigateur

**Problème** : la vidéo ne se charge pas ou n'est pas analysée
- **Solution** : vérifiez que l'URL de la vidéo est accessible, renvoie le bon type MIME et est dans un format pris en charge

**Problème** : analyse temporelle imprécise
- **Solution** : activez le mode thinking pour un raisonnement temporel complexe et fournissez des prompts plus précis sur le temps/la séquence

**Problème** : temps de réponse lents pour les vidéos
- **Solution** : les vidéos demandent plus de traitement que les images ; envisagez des extraits plus courts ou un échantillonnage pour les vidéos longues

**Problème** : détails manquants dans la vidéo
- **Solution** : soyez plus précis dans votre prompt, interrogez des segments temporels ou des aspects particuliers

**Problème** : format vidéo non pris en charge
- **Solution** : convertissez la vidéo en MP4 (le plus largement pris en charge) et vérifiez que l'URL renvoie le bon type MIME vidéo

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- Le SDK est déjà installé — importez-le comme montré dans les exemples
- Utilisez le type de contenu `video_url` pour les fichiers vidéo
- L'analyse vidéo prend plus de temps que l'analyse d'images — soyez patient
- Activez le mode thinking pour un raisonnement temporel complexe et la détection d'événements
- Structurez les prompts pour inclure l'information temporelle (début, milieu, fin)
- Gérez les erreurs avec soin en production
- Implémentez une limitation de débit et des délais pour le traitement par lots
- Validez et assainissez les entrées utilisateur
- Tenez compte de la vie privée et de la sécurité lors du traitement des vidéos des utilisateurs
- Pour les très longues vidéos, envisagez d'analyser des segments spécifiques ou des images clés
