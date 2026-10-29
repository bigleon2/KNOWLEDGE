# Podcast Generate Skill (version TypeScript en ligne)

Transforme automatiquement un document en podcast dialogué, avec une durée ajustée selon la longueur du contenu (3-20 minutes, environ 240 caractères/minute) :
- Extraction automatique du contenu essentiel
- Génération d'un script de podcast modifiable
- Synthèse audio via z-ai TTS

Il s'agit d'une version TypeScript utilisant **z-ai-web-dev-sdk**, adaptée à l'environnement en ligne.

---

## Démarrage rapide

### Génération en une commande (script + audio)

```bash
npm run generate -- --input=test_data/material.txt --out_dir=out
```

**Sorties finales :**
- `out/podcast_script.md` - script du podcast (format Markdown)
- `out/podcast.wav` - audio final du podcast

---

## Structure du répertoire

```text
podcast-generate/
├── readme.md               # mode d'emploi (ce fichier)
├── SKILL.md                # capacités du skill et conventions d'interface
├── package.json            # configuration des dépendances Node.js
├── tsconfig.json           # configuration de compilation TypeScript
├── generate.ts             # ⭐ point d'entrée unifié (seul fichier nécessaire)
└── test_data/
    └── material.txt        # exemple de document en entrée
```

---

## Prérequis

- **Node.js 18+**
- **z-ai-web-dev-sdk** (déjà installé dans l'environnement)

Le CLI z-ai n'est **pas nécessaire**, ce code utilise exclusivement le SDK.

---

## Installation

```bash
npm install
```

---

## Modes d'utilisation

### Mode 1 : génération depuis un fichier

```bash
npm run generate -- --input=material.txt --out_dir=out
```

### Mode 2 : génération via recherche web

```bash
npm run generate -- --topic="最新AI新闻" --out_dir=out
npm run generate -- --topic="量子计算应用" --out_dir=out --duration=8
```

### Description des paramètres

| Paramètre | Description | Valeur par défaut |
|------|------|--------|
| `--input` | chemin du document d'entrée, formats texte txt/md/docx/pdf etc. (alternative à --topic) | - |
| `--topic` | mots-clés du sujet de recherche (alternative à --input) | - |
| `--out_dir` | répertoire de sortie (obligatoire) | - |
| `--mode` | mode du podcast : dual / single-male / single-female | dual |
| `--duration` | durée imposée en minutes (3-20) ; 0 pour automatique | 0 |
| `--host_name` | nom de l'animateur/de l'animateur principal | 小谱 |
| `--guest_name` | nom de l'invité | 锤锤 |
| `--voice_host` | voix de l'animateur | xiaochen |
| `--voice_guest` | voix de l'invité | chuichui |
| `--speed` | vitesse d'élocution (0.5-2.0) | 1.0 |
| `--pause_ms` | pause entre les segments en millisecondes | 200 |

---

## Exemples d'utilisation

### Podcast à deux voix (par défaut)

```bash
npm run generate -- --input=material.txt --out_dir=out
```

### Podcast solo voix masculine

```bash
npm run generate -- --input=material.txt --out_dir=out --mode=single-male
```

### Durée imposée à 5 minutes

```bash
npm run generate -- --input=material.txt --out_dir=out --duration=5
```

### Noms de rôles personnalisés

```bash
npm run generate -- --input=material.txt --out_dir=out --host_name=Marc --guest_name=Léa
```

### Autres voix

```bash
npm run generate -- --input=material.txt --out_dir=out --voice_host=tongtong --voice_guest=douji
```

### Podcast généré via recherche web

```bash
# rechercher selon le sujet puis générer le podcast
npm run generate -- --topic="最新AI技术突破" --out_dir=out

# préciser le sujet de recherche et la durée
npm run generate -- --topic="量子计算应用场景" --out_dir=out --duration=8

# rechercher puis générer un podcast solo
npm run generate -- --topic="气候变化影响" --out_dir=out --mode=single-male
```

---

## Voix disponibles

| Voix | Caractéristiques |
|------|------|
| xiaochen | posée et professionnelle |
| chuichui | vive et attachante |
| tongtong | chaleureuse et bienveillante |
| jam | gentleman à l'accent britannique |
| kazi | claire et standard |
| douji | naturelle et fluide |
| luodo | très expressive |

---

## Architecture technique

### generate.ts (point d'entrée unifié)
- **LLM** : via `z-ai-web-dev-sdk` (`chat.completions.create`)
- **TTS** : via `z-ai-web-dev-sdk` (`audio.tts.create`)
- le CLI z-ai n'est **pas nécessaire**
- assemblage automatique des segments audio
- seul le fichier final est conservé, les fichiers intermédiaires sont nettoyés automatiquement

### Appel LLM
- System prompt : rôle de scénariste de script de podcast
- User prompt : contient le document + contraintes strictes + exigences de rythme naturel
- Validation de sortie : nombre de caractères, structure, étiquettes de rôles
- Relances automatiques : jusqu'à 3 fois

### Appel TTS
- via `zai.audio.tts.create()`
- voix et vitesse personnalisables
- assemblage automatique de plusieurs segments wav
- nettoyage automatique des fichiers temporaires

---

## Licence

MIT
