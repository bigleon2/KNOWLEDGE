---
name: Podcast Generate
version: "1.0.0"
category: "Autres"
tags:
  - podcast
  - generate
description: Génère des épisodes de podcast à partir de contenu fourni par l'utilisateur ou en recherchant sur le web le sujet demandé (podcast generate). Si l'utilisateur téléverse un fichier texte/article, crée un podcast dialogue à double animateur (ou à animateur unique sur demande). Si aucun contenu n'est fourni, recherche sur le web des informations sur le sujet spécifié et génère un podcast. La durée s'ajuste à la taille du contenu (3-20 minutes, ~240 caractères/min). Utilise z-ai-web-dev-sdk pour la génération de script LLM et la synthèse audio TTS. Produit à la fois un script de podcast (Markdown) et un fichier audio complet (WAV).
license: MIT
language: fr

read_when:
  - Déclencher quand la demande concerne : génère des épisodes de podcast à partir de contenu fourni par l'utilisateur ou en recherchant sur le web le su…
  - Déclencher si la demande mentionne : podcast, contenu, génère
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Podcast Generate Skill (version TypeScript)

Génère automatiquement des scripts et de l'audio de podcast à partir de documents fournis par l'utilisateur ou de résultats de recherche sur le web.

Ce Skill est adapté à :
- La compréhension rapide de contenus longs et leur transformation en podcast
- La mise en forme audio de contenus à vocation pédagogique
- L'analyse approfondie et la discussion de sujets d'actualité
- La recherche d'informations en temps réel et la production de podcast

---

## Capacités

### Ce que ce Skill peut faire
- **Génération depuis un fichier** : reçoit un document (txt/md/docx/pdf et autres formats texte) et produit un script et un audio de podcast sous forme de dialogue
- **Génération par recherche web** : à partir du thème demandé par l'utilisateur, recherche les informations les plus récentes sur le web et produit un script et un audio de podcast
- Contrôle automatique de la durée, ajustée à la longueur du contenu (3-20 minutes)
- Génère un script de podcast au format Markdown (modifiable à la main)
- Utilise le TTS z-ai pour synthétiser un audio de qualité et l'assembler en podcast final

### Ce que ce Skill ne fait pas actuellement
- Ne génère pas de mp3 / sous-titres / horodatages
- Ne prend pas en charge trois rôles de podcast ou plus
- N'ajoute pas de musique de fond ni d'effets sonores

---

## Fichiers et responsabilités

Ce Skill se compose des fichiers suivants :

- `generate.ts`
  Point d'entrée unifié (mode fichier et mode recherche)
  - **Mode fichier** : lit le fichier texte téléversé par l'utilisateur → génère le podcast
  - **Mode recherche** : appelle le skill web-search pour obtenir de la documentation → génère le podcast
  - Utilise z-ai-web-dev-sdk pour la génération de script par LLM
  - Utilise z-ai-web-dev-sdk pour la génération audio TTS
  - Assemble automatiquement les segments audio
  - Ne produit que les fichiers finaux

- `readme.md`
  Documentation d'utilisation

- `SKILL.md`
  Fichier courant, décrit les capacités, les limites et les conventions d'usage du Skill

- `package.json`
  Configuration et dépendances du projet Node.js

- `tsconfig.json`
  Configuration de compilation TypeScript

---

## Conventions d'entrée et de sortie

### Entrées (au choix, une seule)

**Méthode 1 : téléversement de fichier**
- Un fichier document (txt / md / docx / pdf et autres formats texte)
- Longueur libre, le Skill compresse automatiquement à la bonne longueur

**Méthode 2 : recherche web**
- L'utilisateur spécifie un thème de recherche
- Le skill web-search est appelé automatiquement pour récupérer le contenu pertinent
- Plusieurs résultats de recherche sont consolidés comme sources

### Sorties (2 fichiers seulement)

- `podcast_script.md`
  Script du podcast (format Markdown, modifiable à la main)

- `podcast.wav`
  Audio final du podcast, assemblé

**Aucun fichier intermédiaire en sortie** (segments.jsonl, meta.json, etc.)

---

## Exécution

### Environnement requis
- Node.js 18+
- z-ai-web-dev-sdk (déjà installé)
- skill web-search (pour le mode recherche web)

**Pas besoin** du z-ai CLI

### Installation des dépendances
```bash
npm install
```

---

## Exemples d'utilisation

### Générer un podcast depuis un fichier

```bash
npm run generate -- --input=test_data/material.txt --out_dir=out
```

### Générer un podcast par recherche web

```bash
# 根据主题搜索并生成播客
npm run generate -- --topic="最新AI技术突破" --out_dir=out

# 指定搜索主题和时长
npm run generate -- --topic="量子计算应用场景" --out_dir=out --duration=8

# 搜索并生成单人播客
npm run generate -- --topic="气候变化影响" --out_dir=out --mode=single-male
```

---

## Paramètres

| Paramètre | Description | Valeur par défaut |
|------|------|--------|
| `--input` | Chemin du fichier document en entrée (à choisir avec --topic) | - |
| `--topic` | Mots-clés du thème de recherche (à choisir avec --input) | - |
| `--out_dir` | Répertoire de sortie (obligatoire) | - |
| `--mode` | Mode de podcast : dual / single-male / single-female | dual |
| `--duration` | Durée en minutes imposée (3-20) ; 0 = automatique | 0 |
| `--host_name` | Nom de l'animateur | 小谱 |
| `--guest_name` | Nom de l'invité | 锤锤 |
| `--voice_host` | Voix de l'animateur | xiaochen |
| `--voice_guest` | Voix de l'invité | chuichui |
| `--speed` | Débit de parole (0.5-2.0) | 1.0 |
| `--pause_ms` | Pause inter-segments en millisecondes | 200 |

---

## Voix disponibles

| Voix | Caractéristiques |
|------|------|
| xiaochen | Posée et professionnelle |
| chuichui | Vive et attachante |
| tongtong | Chaleureuse et bienveillante |
| jam | Accent britannique raffiné |
| kazi | Claire et standard |
| douji | Naturelle et fluide |
| luodo | Pleine d'énergie |

---

## Architecture technique

### generate.ts (point d'entrée unifié)
- **Mode fichier** : lit le fichier téléversé par l'utilisateur → génère le podcast
- **Mode recherche** : appelle le skill web-search → récupère la documentation → génère le podcast
- **LLM** : utilise `z-ai-web-dev-sdk` (`chat.completions.create`)
- **TTS** : utilise `z-ai-web-dev-sdk` (`audio.tts.create`)
- **Pas besoin** du z-ai CLI
- Assemble automatiquement les segments audio
- Ne produit que les fichiers finaux ; les fichiers intermédiaires sont nettoyés automatiquement

### Appels LLM
- System prompt : rôle de scénariste de podcast
- User prompt : documentation + contraintes strictes + exigences de respiration du dialogue
- Validation de la sortie : nombre de mots, structure, étiquettes de rôles
- Nouvelle tentative automatique : 3 fois maximum

### Appels TTS
- Utilise `zai.audio.tts.create()`
- Prend en charge voix et débit personnalisés
- Assemble automatiquement plusieurs segments wav
- Nettoyage automatique des fichiers temporaires

---

## Exemple de sortie

### podcast_script.md (extrait)
```markdown
**小谱**：大家好，欢迎收听今天的播客。今天我们来聊一个有趣的话题……

**锤锤**：是啊，这个话题真的很有意思。我最近也在关注……

**小谱**：说到这里，我想给大家举个例子……
```

---

## License

MIT
