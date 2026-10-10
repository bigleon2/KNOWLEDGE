---
name: ASR
version: "1.0.0"
category: "IA & Media"
tags:
  - ASR
description: Implémente des capacités de reconnaissance vocale (ASR/speech-to-text) à l'aide du z-ai-web-dev-sdk. Utilisez ce skill lorsque l'utilisateur doit transcrire des fichiers audio, convertir de la parole en texte, créer des fonctionnalités de saisie vocale ou traiter des enregistrements audio. Prend en charge les fichiers audio encodés en base64 et renvoie des transcriptions textuelles précises.
language: fr
license: MIT

read_when:
  - Déclencher quand la demande concerne : implémente des capacités de reconnaissance vocale (ASR/speech-to-text) à l'aide du z-ai-web-dev-sdk
  - Déclencher si la demande mentionne : audio, vocale, fichiers
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Skill ASR (Speech to Text)

Ce skill guide l'implémentation de la reconnaissance vocale (ASR) à l'aide du package z-ai-web-dev-sdk, permettant de transcrire avec précision de l'audio parlé en texte.

## Emplacement du skill

**Emplacement du skill** : `{project_path}/skills/ASR`

Ce skill se trouve à l'emplacement ci-dessus dans votre projet.

**Scripts de référence** : des scripts de test d'exemple sont disponibles dans le répertoire `{Skill Location}/scripts/` pour des tests rapides et comme référence. Voir `{Skill Location}/scripts/asr.ts` pour un exemple fonctionnel.

## Vue d'ensemble

La reconnaissance vocale (ASR - Automatic Speech Recognition) permet de créer des applications qui convertissent la langue parlée d'un fichier audio en texte écrit, ouvrant la voie à des interfaces contrôlées par la voix, des services de transcription et l'analyse de contenu audio.

**IMPORTANT** : le z-ai-web-dev-sdk doit être utilisé exclusivement dans du code backend. Ne l'utilisez jamais dans du code côté client.

## Prérequis

Le package z-ai-web-dev-sdk est déjà installé. Importez-le comme montré dans les exemples ci-dessous.

## Utilisation du CLI (pour les tâches simples)

Pour des tâches simples de transcription audio, vous pouvez utiliser le CLI z-ai au lieu d'écrire du code. C'est idéal pour des transcriptions rapides, tester des fichiers audio ou du traitement par lots.

### Transcription de base depuis un fichier

```bash
# Transcribe an audio file
z-ai asr --file ./audio.wav

# Save transcription to JSON file
z-ai asr -f ./recording.mp3 -o transcript.json

# Transcribe and view output
z-ai asr --file ./interview.wav --output result.json
```

### Transcription depuis du base64

```bash
# Transcribe from base64 encoded audio
z-ai asr --base64 "UklGRiQAAABXQVZFZm10..." -o result.json

# Using short option
z-ai asr -b "base64_encoded_audio_data" -o transcript.json
```

### Sortie en streaming

```bash
# Stream transcription results
z-ai asr -f ./audio.wav --stream
```

### Paramètres du CLI

- `--file, -f <path>` : **Obligatoire** (si `--base64` n'est pas utilisé) - chemin du fichier audio
- `--base64, -b <base64>` : **Obligatoire** (si `--file` n'est pas utilisé) - audio encodé en base64
- `--output, -o <path>` : Optionnel - chemin du fichier de sortie (format JSON)
- `--stream` : Optionnel - streame la sortie de la transcription

### Formats audio pris en charge

Le service ASR prend en charge divers formats audio, notamment :
- WAV (.wav)
- MP3 (.mp3)
- Autres formats audio courants

### Quand utiliser le CLI ou le SDK

**Utilisez le CLI pour :**
- Des transcriptions rapides de fichiers audio
- Tester la précision de la reconnaissance vocale
- Des scripts simples de traitement par lots
- Des tâches de transcription ponctuelles

**Utilisez le SDK pour :**
- La transcription audio en temps réel dans des applications
- L'intégration avec des systèmes d'enregistrement
- Des workflows personnalisés de traitement audio
- Des applications de production avec de l'audio en streaming

## Implémentation ASR de base

### Transcription audio simple

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function transcribeAudio(audioFilePath) {
  const zai = await ZAI.create();

  // Read audio file and convert to base64
  const audioFile = fs.readFileSync(audioFilePath);
  const base64Audio = audioFile.toString('base64');

  const response = await zai.audio.asr.create({
    file_base64: base64Audio
  });

  return response.text;
}

// Usage
const transcription = await transcribeAudio('./audio.wav');
console.log('Transcription:', transcription);
```

### Transcrire plusieurs fichiers audio

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function transcribeBatch(audioFilePaths) {
  const zai = await ZAI.create();
  const results = [];

  for (const filePath of audioFilePaths) {
    try {
      const audioFile = fs.readFileSync(filePath);
      const base64Audio = audioFile.toString('base64');

      const response = await zai.audio.asr.create({
        file_base64: base64Audio
      });

      results.push({
        file: filePath,
        success: true,
        transcription: response.text
      });
    } catch (error) {
      results.push({
        file: filePath,
        success: false,
        error: error.message
      });
    }
  }

  return results;
}

// Usage
const files = ['./interview1.wav', './interview2.wav', './interview3.wav'];
const transcriptions = await transcribeBatch(files);

transcriptions.forEach(result => {
  if (result.success) {
    console.log(`${result.file}: ${result.transcription}`);
  } else {
    console.error(`${result.file}: Error - ${result.error}`);
  }
});
```

## Cas d'usage avancés

### Traitement de fichiers audio avec métadonnées

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

async function transcribeWithMetadata(audioFilePath) {
  const zai = await ZAI.create();

  // Get file metadata
  const stats = fs.statSync(audioFilePath);
  const audioFile = fs.readFileSync(audioFilePath);
  const base64Audio = audioFile.toString('base64');

  const startTime = Date.now();

  const response = await zai.audio.asr.create({
    file_base64: base64Audio
  });

  const endTime = Date.now();

  return {
    filename: path.basename(audioFilePath),
    filepath: audioFilePath,
    fileSize: stats.size,
    transcription: response.text,
    wordCount: response.text.split(/\s+/).length,
    processingTime: endTime - startTime,
    timestamp: new Date().toISOString()
  };
}

// Usage
const result = await transcribeWithMetadata('./meeting_recording.wav');
console.log('Transcription Details:', JSON.stringify(result, null, 2));
```

### Service de traitement audio en temps réel

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

class ASRService {
  constructor() {
    this.zai = null;
    this.transcriptionCache = new Map();
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  generateCacheKey(audioBuffer) {
    const crypto = require('crypto');
    return crypto.createHash('md5').update(audioBuffer).digest('hex');
  }

  async transcribe(audioFilePath, useCache = true) {
    const audioBuffer = fs.readFileSync(audioFilePath);
    const cacheKey = this.generateCacheKey(audioBuffer);

    // Check cache
    if (useCache && this.transcriptionCache.has(cacheKey)) {
      return {
        transcription: this.transcriptionCache.get(cacheKey),
        cached: true
      };
    }

    // Transcribe audio
    const base64Audio = audioBuffer.toString('base64');

    const response = await this.zai.audio.asr.create({
      file_base64: base64Audio
    });

    // Cache result
    if (useCache) {
      this.transcriptionCache.set(cacheKey, response.text);
    }

    return {
      transcription: response.text,
      cached: false
    };
  }

  clearCache() {
    this.transcriptionCache.clear();
  }

  getCacheSize() {
    return this.transcriptionCache.size;
  }
}

// Usage
const asrService = new ASRService();
await asrService.initialize();

const result1 = await asrService.transcribe('./audio.wav');
console.log('First call (not cached):', result1);

const result2 = await asrService.transcribe('./audio.wav');
console.log('Second call (cached):', result2);
```

### Transcription d'un répertoire

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';
import path from 'path';

async function transcribeDirectory(directoryPath, outputJsonPath) {
  const zai = await ZAI.create();

  // Get all audio files
  const files = fs.readdirSync(directoryPath);
  const audioFiles = files.filter(file => 
    /\.(wav|mp3|m4a|flac|ogg)$/i.test(file)
  );

  const results = {
    directory: directoryPath,
    totalFiles: audioFiles.length,
    processedAt: new Date().toISOString(),
    transcriptions: []
  };

  for (const filename of audioFiles) {
    const filePath = path.join(directoryPath, filename);

    try {
      const audioFile = fs.readFileSync(filePath);
      const base64Audio = audioFile.toString('base64');

      const response = await zai.audio.asr.create({
        file_base64: base64Audio
      });

      results.transcriptions.push({
        filename: filename,
        success: true,
        text: response.text,
        wordCount: response.text.split(/\s+/).length
      });

      console.log(`✓ Transcribed: ${filename}`);
    } catch (error) {
      results.transcriptions.push({
        filename: filename,
        success: false,
        error: error.message
      });

      console.error(`✗ Failed: ${filename} - ${error.message}`);
    }
  }

  // Save results to JSON
  fs.writeFileSync(
    outputJsonPath,
    JSON.stringify(results, null, 2)
  );

  return results;
}

// Usage
const results = await transcribeDirectory(
  './audio-recordings',
  './transcriptions.json'
);

console.log(`\nProcessed ${results.totalFiles} files`);
console.log(`Successful: ${results.transcriptions.filter(t => t.success).length}`);
console.log(`Failed: ${results.transcriptions.filter(t => !t.success).length}`);
```

## Bonnes pratiques

### 1. Gestion des formats audio

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function transcribeAnyFormat(audioFilePath) {
  // Supported formats: WAV, MP3, M4A, FLAC, OGG, etc.
  const validExtensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg'];
  const ext = audioFilePath.toLowerCase().substring(audioFilePath.lastIndexOf('.'));

  if (!validExtensions.includes(ext)) {
    throw new Error(`Unsupported audio format: ${ext}`);
  }

  const zai = await ZAI.create();
  const audioFile = fs.readFileSync(audioFilePath);
  const base64Audio = audioFile.toString('base64');

  const response = await zai.audio.asr.create({
    file_base64: base64Audio
  });

  return response.text;
}
```

### 2. Gestion des erreurs

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function safeTranscribe(audioFilePath) {
  try {
    // Validate file exists
    if (!fs.existsSync(audioFilePath)) {
      throw new Error(`File not found: ${audioFilePath}`);
    }

    // Check file size (e.g., limit to 100MB)
    const stats = fs.statSync(audioFilePath);
    const fileSizeMB = stats.size / (1024 * 1024);
    
    if (fileSizeMB > 100) {
      throw new Error(`File too large: ${fileSizeMB.toFixed(2)}MB (max 100MB)`);
    }

    // Transcribe
    const zai = await ZAI.create();
    const audioFile = fs.readFileSync(audioFilePath);
    const base64Audio = audioFile.toString('base64');

    const response = await zai.audio.asr.create({
      file_base64: base64Audio
    });

    if (!response.text || response.text.trim().length === 0) {
      throw new Error('Empty transcription result');
    }

    return {
      success: true,
      transcription: response.text,
      filePath: audioFilePath,
      fileSize: stats.size
    };
  } catch (error) {
    console.error('Transcription error:', error);
    return {
      success: false,
      error: error.message,
      filePath: audioFilePath
    };
  }
}
```

### 3. Post-traitement des transcriptions

```javascript
function cleanTranscription(text) {
  // Remove excessive whitespace
  text = text.replace(/\s+/g, ' ').trim();

  // Capitalize first letter of sentences
  text = text.replace(/(^\w|[.!?]\s+\w)/g, match => match.toUpperCase());

  // Remove filler words (optional)
  const fillers = ['um', 'uh', 'ah', 'like', 'you know'];
  const fillerPattern = new RegExp(`\\b(${fillers.join('|')})\\b`, 'gi');
  text = text.replace(fillerPattern, '').replace(/\s+/g, ' ');

  return text;
}

async function transcribeAndClean(audioFilePath) {
  const zai = await ZAI.create();
  
  const audioFile = fs.readFileSync(audioFilePath);
  const base64Audio = audioFile.toString('base64');

  const response = await zai.audio.asr.create({
    file_base64: base64Audio
  });

  return {
    raw: response.text,
    cleaned: cleanTranscription(response.text)
  };
}
```

## Cas d'usage courants

1. **Transcription de réunions** : convertir des réunions enregistrées en texte consultable
2. **Traitement d'entretiens** : transcrire des entretiens pour analyse et documentation
3. **Transcription de podcasts** : créer des versions textuelles des épisodes de podcast
4. **Notes vocales** : convertir des mémos vocaux en texte pour s'y référer plus facilement
5. **Analytique de centre d'appels** : analyser les appels du service client
6. **Accessibilité** : fournir des alternatives textuelles au contenu audio
7. **Commandes vocales** : activer des applications contrôlées à la voix
8. **Apprentissage des langues** : transcrire des exercices de prononciation

## Exemples d'intégration

### Point d'accès API Express.js

```javascript
import express from 'express';
import multer from 'multer';
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const app = express();
const upload = multer({ dest: 'uploads/' });

let zaiInstance;

async function initZAI() {
  zaiInstance = await ZAI.create();
}

app.post('/api/transcribe', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    const audioFile = fs.readFileSync(req.file.path);
    const base64Audio = audioFile.toString('base64');

    const response = await zaiInstance.audio.asr.create({
      file_base64: base64Audio
    });

    // Clean up uploaded file
    fs.unlinkSync(req.file.path);

    res.json({
      success: true,
      transcription: response.text,
      wordCount: response.text.split(/\s+/).length
    });
  } catch (error) {
    // Clean up on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

initZAI().then(() => {
  app.listen(3000, () => {
    console.log('ASR API running on port 3000');
  });
});
```

## Dépannage

**Problème** : « le SDK doit être utilisé côté backend »
- **Solution** : assurez-vous que z-ai-web-dev-sdk n'est importé que dans du code côté serveur

**Problème** : transcription vide ou incorrecte
- **Solution** : vérifiez la qualité et le format de l'audio. Contrôlez que l'audio contient une parole claire

**Problème** : échec du traitement des gros fichiers
- **Solution** : envisagez de découper les fichiers audio volumineux en segments plus petits

**Problème** : vitesse de transcription lente
- **Solution** : mettez en cache les transcriptions répétées, optimisez la taille des fichiers

**Problème** : erreurs de mémoire avec les gros fichiers
- **Solution** : traitez les fichiers par morceaux ou augmentez la limite de mémoire de Node.js

## Conseils de performance

1. **Réutilisez l'instance du SDK** : créez-la une fois, utilisez-la plusieurs fois
2. **Implémentez un cache** : mettez en cache les transcriptions des fichiers en doublon
3. **Traitement par lots** : traitez plusieurs fichiers efficacement avec une file d'attente appropriée
4. **Optimisation audio** : compressez les fichiers audio avant traitement quand c'est possible
5. **Opérations asynchrones** : utilisez Promise.all pour un traitement parallèle quand c'est approprié

## Recommandations de qualité audio

Pour de meilleurs résultats de transcription :
- **Fréquence d'échantillonnage** : 16 kHz ou plus
- **Format** : WAV, MP3 ou M4A recommandés
- **Niveau de bruit** : minimisez le bruit de fond
- **Clarté de la parole** : prononciation claire et débit normal
- **Taille de fichier** : moins de 100 Mo recommandé pour un fichier individuel

## À retenir

- Utilisez toujours z-ai-web-dev-sdk uniquement dans du code backend
- Le SDK est déjà installé - importez-le comme montré dans les exemples
- Les fichiers audio doivent être convertis en base64 avant traitement
- Implémentez une gestion d'erreurs appropriée pour les applications de production
- Tenez compte de la qualité audio pour une meilleure précision de transcription
- Nettoyez les fichiers temporaires après traitement
- Mettez en cache les résultats pour les fichiers fréquemment transcrits
