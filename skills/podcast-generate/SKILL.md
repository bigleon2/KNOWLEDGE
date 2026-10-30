---
name: Podcast Generate
description: Generate podcast episodes from user-provided content or by searching the web for specified topics. If user uploads a text file/article, creates a dual-host dialogue podcast (or single-host upon request). If no content is provided, searches the web for information about the user-specified topic and generates a podcast. Duration scales with content size (3-20 minutes, ~240 chars/min). Uses z-ai-web-dev-sdk for LLM script generation and TTS audio synthesis. Outputs both a podcast script (Markdown) and a complete audio file (WAV).
license: MIT
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Skill Podcast Generate (version TypeScript)

Génère automatiquement un script de podcast et son audio à partir de documents fournis par l'utilisateur ou de résultats de recherche web.

Ce skill convient pour :
- La compréhension rapide et la conversion en podcast de contenus longs
- La mise en audio de contenus de type connaissances
- L'analyse approfondie et la discussion de sujets d'actualité
- La recherche d'informations en temps réel et la production de podcasts

---

## Description des capacités

### Ce que ce skill peut faire
- **Génération depuis un fichier** : reçoit un document (txt/md/docx/pdf et autres formats texte), génère un script de podcast dialogué et l'audio correspondant
- **Génération avec recherche web** : selon le thème spécifié par l'utilisateur, recherche les informations les plus récentes sur le web et génère script et audio
- Contrôle automatique de la durée, ajusté à la longueur du contenu (3-20 minutes)
- Génération du script de podcast au format Markdown (éditable à la main)
- Synthèse d'un audio de haute qualité via z-ai TTS et assemblage en podcast final

### Ce que ce skill ne fait pas (actuellement)
- Ne génère pas de mp3 / sous-titres / horodatages
- Ne prend pas en charge trois rôles ou plus dans le podcast
- N'ajoute ni musique de fond ni effets sonores

---

## Fichiers et responsabilités

Ce skill est composé des fichiers suivants :

- `generate.ts`
  Point d'entrée unifié (prend en charge le mode fichier et le mode recherche)
  - **Mode fichier** : lit le fichier texte fourni par l'utilisateur → génère le podcast
  - **Mode recherche** : appelle le skill web-search pour obtenir la documentation → génère le podcast
  - Utilise z-ai-web-dev-sdk pour la génération du script par LLM
  - Utilise z-ai-web-dev-sdk pour la génération audio par TTS
  - Assemble automatiquement les segments audio
  - Ne produit que les fichiers finaux

- `readme.md`
Guide d'utilisation

- `SKILL.md`
  Le présent fichier : décrit les capacités, les limites et les conventions d'usage du skill

- `package.json`
Configuration du projet Node.js et dépendances

- `tsconfig.json`
Configuration de compilation TypeScript

---

## Conventions d'entrée et de sortie

### Entrée (au choix)

**Méthode 1 : envoi de fichier**
- Un fichier de documentation (txt / md / docx / pdf et autres formats texte)
- Longueur libre : le skill compresse automatiquement à la longueur appropriée

**Méthode 2 : recherche web**
- L'utilisateur spécifie un thème de recherche
- Le skill web-search est appelé automatiquement pour récupérer le contenu pertinent
- Plusieurs résultats de recherche sont intégrés comme sources

### Sortie (2 fichiers uniquement)

- `podcast_script.md`
  Script du podcast (format Markdown, éditable à la main)

- `podcast.wav`
  Audio du podcast final, assemblé

**Aucun fichier intermédiaire n'est produit** (segments.jsonl, meta.json, etc.)

---

## Mode d'exécution

### Environnement requis
- Node.js 18+
- z-ai-web-dev-sdk (installé)
- skill web-search (pour le mode recherche web)

**Le CLI z-ai n'est pas requis**

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

### Générer un podcast avec recherche web

```bash
# Rechercher selon un thème et générer le podcast
npm run generate -- --topic="最新AI技术突破" --out_dir=out

# Spécifier le thème de recherche et la durée
npm run generate -- --topic="量子计算应用场景" --out_dir=out --duration=8

# Rechercher puis générer un podcast à voix seule
npm run generate -- --topic="气候变化影响" --out_dir=out --mode=single-male
```

---

## Description des paramètres

| Paramètre | Description | Valeur par défaut |
|------|------|--------|
| `--input` | Chemin du fichier de documentation (à choisir entre --input et --topic) | - |
| `--topic` | Mots-clés du thème de recherche (à choisir entre --topic et --input) | - |
| `--out_dir` | Répertoire de sortie (obligatoire) | - |
| `--mode` | Mode podcast : dual / single-male / single-female | dual |
| `--duration` | Durée imposée en minutes (3-20) ; 0 = automatique | 0 |
| `--host_name` | Nom de l'animateur/trice | 小谱 (Xiaopu) |
| `--guest_name` | Nom de l'invité(e) | 锤锤 (Chuichui) |
| `--voice_host` | Voix de l'animateur/trice | xiaochen |
| `--voice_guest` | Voix de l'invité(e) | chuichui |
| `--speed` | Vitesse d'élocution (0.5-2.0) | 1.0 |
| `--pause_ms` | Pause inter-segments en millisecondes | 200 |

---

## Voix disponibles

| Voix | Caractère |
|------|------|
| xiaochen | Posée et professionnelle |
| chuichui | Vive et attachante |
| tongtong | Chaleureuse et accessible |
| jam | Gentleman britannique |
| kazi | Claire et standard |
| douji | Naturelle et fluide |
| luodo | Pleine de conviction |

---

## Architecture technique

### generate.ts (point d'entrée unifié)
- **Mode fichier** : lit le fichier fourni par l'utilisateur → génère le podcast
- **Mode recherche** : appelle le skill web-search → récupère la documentation → génère le podcast
- **LLM** : `z-ai-web-dev-sdk` (`chat.completions.create`)
- **TTS** : `z-ai-web-dev-sdk` (`audio.tts.create`)
- **Le CLI z-ai n'est pas requis**
- Assemblage automatique des segments audio
- Ne produit que les fichiers finaux ; les fichiers intermédiaires sont nettoyés automatiquement

### Appel LLM
- System prompt : rôle de scénariste de podcast
- User prompt : contient la documentation + contraintes strictes + exigences de naturel (respiration)
- Validation de la sortie : nombre de caractères, structure, étiquettes de rôles
- Nouvelle tentative automatique : jusqu'à 3 fois

### Appel TTS
- Utilise `zai.audio.tts.create()`
- Voix et vitesse d'élocution personnalisables
- Assemblage automatique de plusieurs segments wav
- Nettoyage automatique des fichiers temporaires

---

## Exemple de sortie

### podcast_script.md (extrait)
```markdown
**小谱 (Xiaopu)** : Bonjour à toutes et à tous, bienvenue dans le podcast du jour. Aujourd'hui, nous allons parler d'un sujet passionnant…

**锤锤 (Chuichui)** : Oui, ce sujet est vraiment intéressant. Moi-même je m'y intéresse beaucoup ces derniers temps…

**小谱 (Xiaopu)** : À ce propos, je voudrais vous donner un exemple…
```

---

## License

MIT
