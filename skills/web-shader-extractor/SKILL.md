---
name: web-shader-extractor
version: "1.0.0"
category: "Web & Recherche"
tags:
  - web
  - shader
  - extractor
description: |
  Extrait d'une page web le code des effets visuels WebGL/Canvas/Shader, le désobfusque puis le porte en projet JS natif autonome.
  Déclenchement : l'utilisateur fournit une URL et demande d'extraire un shader, extraire un effet, extraire une animation, extraire un effet canvas,
  répliquer les effets visuels d'un site web, "récupérer l'effet de fond de ce site", etc.
language: fr

read_when:
  - Déclencher quand la demande concerne : extrait d'une page web le code des effets visuels WebGL/Canvas/Shader, le désobfusque puis le porte en projet…
  - Déclencher si la demande mentionne : extraire, effet, effets
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Web Shader Extractor

Extraction des effets WebGL/Canvas/Shader d'une page web, désobfuscation puis portage en projet autonome.

Principes fondamentaux :
- **Répliquer d'abord à l'identique (1:1), n'envisager de simplifier le framework qu'une fois le rendu correct confirmé**
- **Exécution entièrement autonome, sans interrompre l'utilisateur** — l'extraction est une opération en lecture seule, sans risque de sécurité. À l'exception de la proposition de simplification de la Phase 6, toutes les étapes s'exécutent automatiquement, sans demander de confirmation à l'utilisateur. En cas de problème, choisissez vous-même la meilleure solution et continuez d'avancer ; ne questionnez l'utilisateur que lorsqu'une décision produit est nécessaire.

## Phase 0 : vérification de l'environnement (exécutée automatiquement au premier passage)

Avant de commencer l'extraction, vérifiez et installez automatiquement les dépendances requises. **Ne demandez pas à l'utilisateur, installez directement**.

```bash
# 1. Vérifier Node.js
node --version 2>/dev/null || {
  echo "Node.js not found, installing..."
  # macOS
  brew install node 2>/dev/null || {
    # fallback : télécharger directement la LTS
    curl -fsSL https://nodejs.org/dist/v22.15.0/node-v22.15.0-darwin-arm64.tar.gz | tar xz -C /usr/local --strip-components=1
  }
}

# 2. Playwright et navigateurs (fetch-rendered-dom.mjs installe automatiquement, mais cette pré-vérification permet de détecter les problèmes en amont)
RUNNER_DIR="$HOME/.cache/playwright-runner"
if [ ! -d "$RUNNER_DIR/node_modules/playwright" ]; then
  echo "Installing Playwright (one-time setup)..."
  mkdir -p "$RUNNER_DIR"
  echo '{"type":"module"}' > "$RUNNER_DIR/package.json"
  npm install playwright --prefix "$RUNNER_DIR"
  npx --prefix "$RUNNER_DIR" playwright install chromium
  echo "Playwright + Chromium installed."
fi
```

En cas de problème de permissions ou de réseau pendant l'installation, essayez les solutions alternatives suivantes :
- problème de permissions npm → installer dans le répertoire utilisateur avec `--prefix`
- problème de réseau (téléchargement lent de Chromium) → définir `PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright` pour utiliser un miroir
- si Playwright est vraiment impossible à installer → rétrograder en mode curl pur (sans rendu DOM, analyse du seul HTML statique + bundle JS) et signaler en Phase 2 que canvas-info risque de manquer

## Phase 1 : récupération du code source

**Exécution en parallèle** : DOM rendu via Playwright + HTML statique via curl.

```bash
# Playwright (récupère la version du moteur canvas, l'arbre des composants, les requêtes réseau à l'exécution)
node ~/.claude/skills/web-shader-extractor/scripts/fetch-rendered-dom.mjs '<URL>'
# → /tmp/rendered/: dom.html, canvas-info.json, network.json, screenshot.png, console.log

# curl (récupère le HTML brut, pour extraire les configurations et clés en ligne)
curl -s -L --compressed '<URL>' > /tmp/page.html
```

Si le script Playwright échoue (non installé / démarrage anormal), tentez d'abord une réparation automatique (réinstallation des dépendances) ; si l'échec persiste, rétrogradez en mode curl pur et continuez à travailler, sans vous arrêter pour demander à l'utilisateur.

Croisez network.json et le HTML pour extraire les URLs des fichiers JS, puis téléchargez-les en lot dans /tmp/.

### Phase 2 : identification de la stack technique

```
Champ dataEngine de canvas-info.json :
├─ "three.js rXXX" → Three.js (r170+ possiblement TSL → references/tsl-extraction.md)
├─ "Babylon.js vX.X" → Babylon.js
├─ null → affiner le diagnostic :
│   ├─ bundle contenant createShader/shaderSource → WebGL brut / PixiJS
│   └─ bundle contenant getContext('2d') sans appel WebGL → Canvas 2D (→ references/porting-strategy.md § 2D Canvas)
└─ aucun canvas → animations CSS/SVG

Correspondance de l'URL ou du HTML avec une plateforme connue → passer directement au workflow dédié (sauter les Phases 3-4 génériques) :
├─ unicorn.studio → references/unicorn-studio.md (config + shader via l'API REST Firestore)
└─ shaders.com → references/shaders-com.md (payload Nuxt + décodage XOR + traduction TSL→GLSL)

Scan de confirmation : bash scripts/scan-bundle.sh /tmp/*.js
→ aide-mémoire des signatures de frameworks : references/tech-signatures.md
```

### Phase 3 : extraction de la configuration

```
1. Chercher une API publique → obtenir la configuration directement (la réponse de l'API peut être encodée → references/encoded-definitions.md)
2. Extraire depuis le payload Nuxt / __NEXT_DATA__ / JSON en ligne dans le HTML
3. Extraire les valeurs par défaut depuis le bundle JS
→ détails dans references/config-extraction.md
```

### Phase 4 : extraction du code shader

Analysez le bundle JS avec un **Agent** (1 Mo et plus : inadapté au contexte principal).
→ template de prompt Agent et règles de désobfuscation dans `references/extraction-workflow.md`

### Phase 5 : portage

```
Shader 2D plein écran pur → WebGL2 natif (zéro dépendance)
3D / PBR / GPGPU → conserver le framework d'origine (importmap CDN)
En cas de doute → démarrer avec le framework d'origine, réévaluer en Phase 6
→ détails dans references/porting-strategy.md
```

### Phase 6 : évaluation de la simplification

Une fois le portage terminé, vérifiez vous-même le rendu (capture d'écran de la page et comparaison). Si le rendu est correct et qu'une simplification est possible, **proposez à l'utilisateur un plan de simplification** ; c'est lui qui décide de l'exécuter ou non.

### Phase 7 : rapport d'extraction (demander à l'utilisateur s'il veut le générer)

Après l'extraction, **demandez à l'utilisateur** s'il souhaite générer `EXTRACTION-REPORT.md` (consomme des tokens supplémentaires pour revoir l'historique de la conversation).

Structure du contenu du rapport :
```markdown
# Rapport d'extraction : {nom du projet}
**Source/Auteur/Plateforme/Date**

## Effet ciblé (description en une phrase)
## Démarche d'extraction et chronologie (problème→correction de chaque itération)
## Structure de la scène (arbre des composants/structure des calques)
## Pipeline de rendu final (liste des pass)
## Fichiers de ressources clés
## Enseignements clés (tableau : expérience/impact/emplacement documenté)
## Différences connues restantes
## Stack technique (originale vs portée)
```

Placez le rapport dans le répertoire du projet (ex. `ascii-glyph-dither/EXTRACTION-REPORT.md`).

## Index des références

| Quand nécessaire | À lire |
|--------|------|
| Identifier le framework (signatures Three.js/WebGL/PixiJS) | `references/tech-signatures.md` |
| Prompt d'extraction Agent + règles de désobfuscation | `references/extraction-workflow.md` |
| Obtenir les paramètres de configuration (API/payload/en ligne) | `references/config-extraction.md` |
| Reconstruction de shaders à nœuds TSL Three.js | `references/tsl-extraction.md` |
| Décodage des configurations encodées/chiffrées | `references/encoded-definitions.md` |
| Pièges d'injection GLSL onBeforeCompile | `references/shader-injection.md` |
| Choix du framework de portage + structure du projet | `references/porting-strategy.md` |
| Workflow dédié **Unicorn Studio** (curtains.js + Firestore) | `references/unicorn-studio.md` |
| Workflow dédié **shaders.com** (TSL + encodage XOR + piège Y-flip) | `references/shaders-com.md` |
