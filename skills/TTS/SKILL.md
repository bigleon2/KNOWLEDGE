---
name: TTS
version: "1.0.0"
category: "IA & Media"
tags:
  - TTS
description: Implémente des capacités de synthèse vocale (TTS/text-to-speech) à l'aide du z-ai-web-dev-sdk. Utilisez ce skill lorsque l'utilisateur doit convertir du texte en parole naturelle, créer du contenu audio, construire des applications vocales ou générer des fichiers audio parlés. Prend en charge plusieurs voix, une vitesse ajustable et divers formats audio.
language: fr
license: MIT

---

# Skill TTS (Text to Speech)

Ce skill guide l'implémentation de la synthèse vocale (TTS) à l'aide du package z-ai-web-dev-sdk, permettant de convertir du texte en audio parlé naturel.

## Emplacement du skill

**Emplacement du skill** : `{project_path}/skills/TTS`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/tts.ts` pour un exemple fonctionnel.

## Vue d'ensemble

La synthèse vocale (TTS) permet de créer des applications qui génèrent de l'audio parlé à partir d'un texte saisi, avec diverses voix, vitesses et formats de sortie pour des usages variés.

**IMPORTANT** : le z-ai-web-dev-sdk doit être utilisé exclusivement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Limitations et contraintes de l'API

Avant d'implémenter la fonctionnalité TTS, prenez connaissance de ces limitations importantes :

### Contraintes sur le texte d'entrée
- **Longueur maximale** : 1024 caractères par requête
- Le texte dépassant cette limite doit être découpé en morceaux plus petits

### Paramètres audio
- **Plage de vitesse** : 0,5 à 2,0
  - 0,5 = demi-vitesse (plus lent)
  - 1,0 = vitesse normale (défaut)
  - 2,0 = double vitesse (plus rapide)
- **Plage de volume** : supérieur à 0, jusqu'à 10
  - Défaut : 1.0
  - Les valeurs doivent être strictement supérieures à 0 (exclu) et au plus 10 (inclus)

### Format et streaming
- **Limitation du streaming** : quand `stream: true` est activé, seul le format `pcm` est pris en charge
- **Sans streaming** : prend en charge les formats `wav`, `pcm` et `mp3`
- **Fréquence d'échantillonnage** : 24000 Hz (recommandé)

### Bonne pratique pour les textes longs
```javascript
function splitTextIntoChunks(text, maxLength = 1000) {
  const chunks = [];
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
  
  let currentChunk = '';
  for (const sentence of sentences) {
    if ((currentChunk + sentence).length <= maxLength) {
      currentChunk += sentence;
    } else {
      if (currentChunk) chunks.push(currentChunk.trim());
      currentChunk = sentence;
    }
  }
  if (currentChunk) chunks.push(currentChunk.trim());
  
  return chunks;
}
```

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Utilisation du CLI (pour les tâches simples)

Pour des conversions simples de texte en parole, vous pouvez utiliser le CLI z-ai au lieu d'écrire du code. C'est idéal pour une génération audio rapide, tester des voix ou une automatisation simple.

### TTS de base

```bash
# Convert text to speech (default WAV format)
z-ai tts --input "Hello, world" --output ./hello.wav

# Using short options
z-ai tts -i "Hello, world" -o ./hello.wav
```

### Différentes voix et vitesses

```bash
# Use specific voice
z-ai tts -i "Welcome to our service" -o ./welcome.wav --voice tongtong

# Adjust speech speed (0.5-2.0)
z-ai tts -i "This is faster speech" -o ./fast.wav --speed 1.5

# Slower speech
z-ai tts -i "This is slower speech" -o ./slow.wav --speed 0.8
```

### Différents formats de sortie

```bash
# MP3 format
z-ai tts -i "Hello World" -o ./hello.mp3 --format mp3

# WAV format (default)
z-ai tts -i "Hello World" -o ./hello.wav --format wav

# PCM format
z-ai tts -i "Hello World" -o ./hello.pcm --format pcm
```

### Sortie en streaming

```bash
# Stream audio generation
z-ai tts -i "This is a longer text that will be streamed" -o ./stream.wav --stream
```

### Paramètres du CLI

- `--input, -i <text>` : **Obligatoire** - texte à convertir en parole (1024 caractères maximum)
- `--output, -o <path>` : **Obligatoire** - chemin du fichier audio de sortie
- `--voice, -v <voice>` : Optionnel - type de voix (défaut : tongtong)
- `--speed, -s <number>` : Optionnel - vitesse de la parole, 0.5-2.0 (défaut : 1.0)
- `--format, -f <format>` : Optionnel - format de sortie : wav, mp3, pcm (défaut : wav)
- `--stream` : Optionnel - activer la sortie en streaming (prend uniquement en charge le format pcm)

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Des conversions rapides de texte en parole
- Tester différentes voix et vitesses
- Une génération audio simple par lots
- Des scripts d'automatisation en ligne de commande

**Utilisez le SDK pour :**
- La génération audio dynamique dans des applications
- L'intégration avec des services web
- Des pipelines personnalisés de traitement audio
- Des applications de production aux exigences complexes

## Implémentation TTS de base

### Conversion simple de texte en parole

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function textToSpeech(text, outputPath) {
  const zai = await ZAI.create();

  const response = await zai.audio.tts.create({
    input: text,
    voice: 'tongtong',
    speed: 1.0,
    response_format: 'wav',
    stream: false
  });

  // Get array buffer from Response object
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  console.log(`Audio saved to ${outputPath}`);
  return outputPath;
}

// Usage
await textToSpeech('Hello, world!', './output.wav');
```

### Plusieurs choix de voix

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function generateWithVoice(text, voice, outputPath) {
  const zai = await ZAI.create();

  const response = await zai.audio.tts.create({
    input: text,
    voice: voice, // Available voices: tongtong, chuichui, xiaochen, jam, kazi, douji, luodo
    speed: 1.0,
    response_format: 'wav',
    stream: false
  });

  // Get array buffer from Response object
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Usage
await generateWithVoice('Welcome to our service', 'tongtong', './welcome.wav');
```

### Vitesse ajustable

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function generateWithSpeed(text, speed, outputPath) {
  const zai = await ZAI.create();

  // Speed range: 0.5 to 2.0 (API constraint)
  // 0.5 = half speed (slower)
  // 1.0 = normal speed (default)
  // 2.0 = double speed (faster)
  // Values outside this range will cause API errors

  const response = await zai.audio.tts.create({
    input: text,
    voice: 'tongtong',
    speed: speed,
    response_format: 'wav',
    stream: false
  });

  // Get array buffer from Response object
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Usage - slower narration
await generateWithSpeed('This is an important announcement', 0.8, './slow.wav');

// Usage - faster narration
await generateWithSpeed('Quick update', 1.3, './fast.wav');
```

### Volume ajustable

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function generateWithVolume(text, volume, outputPath) {
  const zai = await ZAI.create();

  // Volume range: greater than 0, up to 10 (API constraint)
  // Values must be > 0 (exclusive) and <= 10 (inclusive)
  // Default: 1.0 (normal volume)

  const response = await zai.audio.tts.create({
    input: text,
    voice: 'tongtong',
    speed: 1.0,
    volume: volume, // Optional parameter
    response_format: 'wav',
    stream: false
  });

  // Get array buffer from Response object
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(new Uint8Array(arrayBuffer));

  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Usage - louder audio
await generateWithVolume('This is an announcement', 5.0, './loud.wav');

// Usage - quieter audio
await generateWithVolume('Whispered message', 0.5, './quiet.wav');
```

## Cas d'usage avancés

### Traitement par lots

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

async function batchTextToSpeech(textArray, outputDir) {
  const zai = await ZAI.create();
  const results = [];

  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  for (let i = 0; i < textArray.length; i++) {
    try {
      const text = textArray[i];
      const outputPath = path.join(outputDir, `audio_${i + 1}.wav`);

      const response = await zai.audio.tts.create({
        input: text,
        voice: 'tongtong',
        speed: 1.0,
        response_format: 'wav',
        stream: false
      });

      // Get array buffer from Response object
      const arrayBuffer = await response.arrayBuffer();
      const buffer = Buffer.from(new Uint8Array(arrayBuffer));

      fs.writeFileSync(outputPath, buffer);
      results.push({
        success: true,
        text,
        path: outputPath
      });
    } catch (error) {
      results.push({
        success: false,
        text: textArray[i],
        error: error.message
      });
    }
  }

  return results;
}

// Usage
const texts = [
  'Welcome to chapter one',
  'Welcome to chapter two',
  'Welcome to chapter three'
];

const results = await batchTextToSpeech(texts, './audio-output');
console.log('Generated:', results.length, 'audio files');
```

### Génération dynamique de contenu

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

class TTSGenerator {
  constructor() {
    this.zai = null;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  async generateAudio(text, options = {}) {
    const {
      voice = 'tongtong',
      speed = 1.0,
      format = 'wav'
    } = options;

    const response = await this.zai.audio.tts.create({
      input: text,
      voice: voice,
      speed: speed,
      response_format: format,
      stream: false
    });

    // Get array buffer from Response object
    const arrayBuffer = await response.arrayBuffer();
    return Buffer.from(new Uint8Array(arrayBuffer));
  }

  async saveAudio(text, outputPath, options = {}) {
    const buffer = await this.generateAudio(text, options);
    if (buffer) {
      fs.writeFileSync(outputPath, buffer);
      return outputPath;
    }
    return null;
  }
}

// Usage
const generator = new TTSGenerator();
await generator.initialize();

await generator.saveAudio(
  'Hello, this is a test',
  './output.wav',
  { speed: 1.2 }
);
```

### Exemple de route API Next.js

```javascript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { text, voice = 'tongtong', speed = 1.0 } = await req.json();

    // Import ZAI SDK
    const ZAI = (await import('z-ai-web-dev-sdk')).default;

    // Create SDK instance
    const zai = await ZAI.create();

    // Generate TTS audio
    const response = await zai.audio.tts.create({
      input: text.trim(),
      voice: voice,
      speed: speed,
      response_format: 'wav',
      stream: false,
    });

    // Get array buffer from Response object
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));

    // Return audio as response
    return new NextResponse(buffer, {
      status: 200,
      headers: {
        'Content-Type': 'audio/wav',
        'Content-Length': buffer.length.toString(),
        'Cache-Control': 'no-cache',
      },
    });
  } catch (error) {
    console.error('TTS API Error:', error);

    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : '生成语音失败，请稍后重试',
      },
      { status: 500 }
    );
  }
}
```

## Bonnes pratiques

### 1. Préparation du texte
```javascript
function prepareTextForTTS(text) {
  // Remove excessive whitespace
  text = text.replace(/\s+/g, ' ').trim();

  // Expand common abbreviations for better pronunciation
  const abbreviations = {
    'Dr.': 'Doctor',
    'Mr.': 'Mister',
    'Mrs.': 'Misses',
    'etc.': 'et cetera'
  };

  for (const [abbr, full] of Object.entries(abbreviations)) {
    text = text.replace(new RegExp(abbr, 'g'), full);
  }

  return text;
}
```

### 2. Gestion des erreurs
```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function safeTTS(text, outputPath) {
  try {
    // Validate input
    if (!text || text.trim().length === 0) {
      throw new Error('Text input cannot be empty');
    }

    if (text.length > 1024) {
      throw new Error('Text input exceeds maximum length of 1024 characters');
    }

    const zai = await ZAI.create();

    const response = await zai.audio.tts.create({
      input: text,
      voice: 'tongtong',
      speed: 1.0,
      response_format: 'wav',
      stream: false
    });

    // Get array buffer from Response object
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));

    fs.writeFileSync(outputPath, buffer);

    return {
      success: true,
      path: outputPath,
      size: buffer.length
    };
  } catch (error) {
    console.error('TTS Error:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

### 3. Réutilisation de l'instance du SDK

```javascript
import ZAI from 'z-ai-web-dev-sdk';

// Create a singleton instance
let zaiInstance = null;

async function getZAIInstance() {
  if (!zaiInstance) {
    zaiInstance = await ZAI.create();
  }
  return zaiInstance;
}

// Usage
const zai = await getZAIInstance();
const response = await zai.audio.tts.create({ ... });
```

## Cas d'usage courants

1. **Livres audio et podcasts** : convertir du contenu écrit en format audio
2. **E-learning** : créer la narration de contenus éducatifs
3. **Accessibilité** : fournir des versions audio de contenus textuels
4. **Assistants vocaux** : générer des réponses dynamiques
5. **Annonces** : créer des notifications audio automatisées
6. **Systèmes IVR** : générer les messages des standards téléphoniques
7. **Localisation de contenu** : créer de l'audio dans différentes langues

## Exemples d'intégration

### Point d'accès API Express.js

```javascript
import express from 'express';
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());

let zaiInstance;
const outputDir = './audio-output';

async function initZAI() {
  zaiInstance = await ZAI.create();
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
}

app.post('/api/tts', async (req, res) => {
  try {
    const { text, voice = 'tongtong', speed = 1.0 } = req.body;

    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    const filename = `tts_${Date.now()}.wav`;
    const outputPath = path.join(outputDir, filename);

    const response = await zaiInstance.audio.tts.create({
      input: text,
      voice: voice,
      speed: speed,
      response_format: 'wav',
      stream: false
    });

    // Get array buffer from Response object
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(new Uint8Array(arrayBuffer));

    fs.writeFileSync(outputPath, buffer);

    res.json({
      success: true,
      audioUrl: `/audio/${filename}`,
      size: buffer.length
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.use('/audio', express.static('audio-output'));

initZAI().then(() => {
  app.listen(3000, () => {
    console.log('TTS API running on port 3000');
  });
});
```

## Dépannage

**Problème** : « le texte d'entrée dépasse la longueur maximale »
- **Solution** : le texte d'entrée est limité à 1024 caractères. Découpez les textes plus longs en morceaux à l'aide de la fonction `splitTextIntoChunks` présentée dans la section Limitations et contraintes de l'API

**Problème** : « paramètre de vitesse invalide » ou comportement de vitesse inattendu
- **Solution** : la vitesse doit être comprise entre 0.5 et 2.0. Vérifiez que votre valeur de vitesse est dans cette plage

**Problème** : « paramètre de volume invalide »
- **Solution** : le volume doit être supérieur à 0 et au plus 10. Assurez-vous que la valeur du volume est dans l'intervalle (0, 10]

**Problème** : « format de stream non pris en charge » avec WAV/MP3
- **Solution** : le mode streaming ne prend en charge que le format PCM. Utilisez soit `response_format: 'pcm'` avec le streaming, soit désactivez le streaming (`stream: false`) pour une sortie WAV/MP3

**Problème** : « le SDK doit être utilisé côté backend »
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé que dans du code côté serveur

**Problème** : « TypeError: response.audio is undefined »
- **Solution** : le SDK renvoie un objet Response standard ; utilisez `await response.arrayBuffer()` au lieu d'accéder à `response.audio`

**Problème** : fichier audio généré vide ou corrompu
- **Solution** : assurez-vous d'appeler `await response.arrayBuffer()` et de convertir correctement en Buffer : `Buffer.from(new Uint8Array(arrayBuffer))`

**Problème** : audio qui sonne artificiel
- **Solution** : préparez correctement le texte (supprimez les caractères spéciaux, développez les abréviations)

**Problème** : temps de traitement longs
- **Solution** : découpez les textes longs en morceaux plus petits et traitez-les en parallèle

**Problème** : le cache Next.js sert une ancienne route API
- **Solution** : créez un nouveau point d'accès de route API ou redémarrez le serveur de développement

## Conseils de performance

1. **Réutilisez l'instance du SDK** : créez l'instance ZAI une seule fois et réutilisez-la
2. **Implémentez un cache** : mettez en cache l'audio généré pour les textes répétés
3. **Traitement par lots** : traitez plusieurs textes efficacement
4. **Optimisez le texte** : supprimez le contenu superflu avant la génération
5. **Traitement asynchrone** : utilisez des files d'attente pour gérer plusieurs requêtes

## Notes importantes

### Contraintes de l'API

**Longueur du texte d'entrée** : 1024 caractères maximum par requête. Pour les textes plus longs :
```javascript
// Split long text into chunks
const longText = "..."; // Your long text here
const chunks = splitTextIntoChunks(longText, 1000);

for (const chunk of chunks) {
  const response = await zai.audio.tts.create({
    input: chunk,
    voice: 'tongtong',
    speed: 1.0,
    response_format: 'wav',
    stream: false
  });
  // Process each chunk...
}
```

**Limitation du format de streaming** : avec `stream: true`, seul le format `pcm` est pris en charge. Pour une sortie `wav` ou `mp3`, utilisez `stream: false`.

**Fréquence d'échantillonnage** : l'audio est généré à 24000 Hz (réglage recommandé pour la lecture).

### Format de l'objet Response

La méthode `zai.audio.tts.create()` renvoie un objet **Response** standard (pas un objet personnalisé avec une propriété `audio`). Utilisez toujours :

```javascript
// ✅ CORRECT
const response = await zai.audio.tts.create({ ... });
const arrayBuffer = await response.arrayBuffer();
const buffer = Buffer.from(new Uint8Array(arrayBuffer));

// ❌ WRONG - This will not work
const response = await zai.audio.tts.create({ ... });
const buffer = Buffer.from(response.audio); // response.audio is undefined
```

### Voix disponibles

- `tongtong` - chaleureuse et affectueuse
- `chuichui` - vive et adorable
- `xiaochen` - posée et professionnelle
- `jam` - gentleman à l'accent britannique
- `kazi` - claire et standard
- `douji` - naturelle et fluide
- `luodo` - pleine d'expression

### Plage de vitesse

- Minimum : `0.5` (demi-vitesse)
- Défaut : `1.0` (vitesse normale)
- Maximum : `2.0` (double vitesse)

**Important** : les valeurs de vitesse hors de la plage [0.5, 2.0] provoquent des erreurs d'API.

### Plage de volume

- Minimum : supérieur à `0` (exclu)
- Défaut : `1.0` (volume normal)
- Maximum : `10` (inclus)

**Remarque** : le paramètre de volume est optionnel. S'il n'est pas spécifié, il vaut 1.0 par défaut.

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- **Le texte d'entrée est limité à 1024 caractères maximum** - découpez les textes plus longs en morceaux
- **La vitesse doit être comprise entre 0.5 et 2.0** - les valeurs hors plage provoquent des erreurs
- **Le volume doit être supérieur à 0 et au plus 10** - paramètre optionnel avec 1.0 par défaut
- **Le streaming ne prend en charge que le format PCM** - utilisez le mode sans streaming pour une sortie WAV ou MP3
- Le SDK renvoie un objet Response standard - utilisez `await response.arrayBuffer()`
- Convertissez l'ArrayBuffer en Buffer avec `Buffer.from(new Uint8Array(arrayBuffer))`
- Gérez correctement les buffers audio lors de l'enregistrement dans des fichiers
- Implémentez une gestion d'erreurs pour les applications de production
- Envisagez un cache pour les contenus fréquemment générés
- Nettoyez périodiquement les anciens fichiers audio pour gérer le stockage
