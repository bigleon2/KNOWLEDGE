---
nom: web-shader-extractor
source: skills/web-shader-extractor/SKILL.md
sha256_source: a0c52594ae56
genere: 2026-10-28 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — web-shader-extractor (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/web-shader-extractor/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: web-shader-extractor
description: |
Extraire le code de effets visuels WebGL/Canvas/Shader des pages web, le déobfusquer et le porter en projet JS natif autonome.
  Conditions de déclenchement : l'utilisateur fournit une URL et demande l'extraction de shader, d'effets spéciaux, d'animations, d'effets canvas,
  de répliquer les effets visuels d'un site, de "récupérer l'effet de fond de ce site", etc.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Web Shader Extractor

Extraire les effets WebGL/Canvas/Shader d'une page web, les déobfusquer et les porter en projet autonome.

Principes fondamentaux :
- **D'abord une réplication 1:1, ne considérer la simplification du framework qu'après validation de l'exactitude**
- **Exécution autonome de bout en bout, sans interrompre l'utilisateur** — l'extraction est une opération en lecture seule, sans risque. Hormis la proposition de simplification de la Phase 6, toutes les étapes s'exécutent automatiquement, sans demande de confirmation. En cas de problème, choisir soi-même la meilleure solution et continuer ; ne solliciter l'utilisateur que pour une décision produit.

## Phase 0: Vérification de l'environnement (première exécution automatique)

Avant de commencer l'extraction, vérifier et installer automatiquement les dépendances requises. **Ne pas demander à l'utilisateur, installer directement**.

```bash
# 1. Vérifier Node.js
node --version 2>/dev/null || {
  echo "Node.js not found, installing..."
  # macOS
  brew install node 2>/dev/null || {
# repli : télécharger directement la LTS
    curl -fsSL https://nodejs.org/dist/v22.15.0/node-v22.15.0-darwin-arm64.tar.gz | tar xz -C /usr/local --strip-components=1
  }
}

# 2. Playwright et navigateur (installation automatique intégrée à fetch-rendered-dom.mjs, mais ce précontrôle détecte les problèmes plus tôt)
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

En cas de problème de permissions ou de réseau pendant l'installation, essayer les solutions de repli suivantes :
- Problème de permissions npm → installer dans le répertoire utilisateur avec `--prefix`
- Problème réseau (téléchargement lent de Chromium) → définir `PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright` pour utiliser un miroir chinois
- Si Playwright reste impossible à installer → rétrograder en mode curl pur (sans rendu DOM, analyse du seul HTML statique + bundle JS), en signalant dans la Phase 2 que canvas-info risque de manquer

## Phase 1: Récupération du code source

**Exécution en parallèle** : Playwright récupère le DOM rendu + curl récupère le HTML statique.

```bash
# Playwright (obtient la version du moteur canvas, l'arbre de composants, les requêtes réseau à l'exécution)
node ~/.claude/skills/web-shader-extractor/scripts/fetch-rendered-dom.mjs '<URL>'
# → /tmp/rendered/: dom.html, canvas-info.json, network.json, screenshot.png, console.log

# curl (obtient le HTML brut, pour extraire les configurations embarquées et les clés)
curl -s -L --compressed '<URL>' > /tmp/page.html
```

Si le script Playwright échoue (non installé / anomalie au démarrage), tenter d'abord une réparation automatique (réinstallation des dépendances) ; en cas d'échec persistant, rétrograder en mode curl pur et continuer, sans s'arrêter pour demander à l'utilisateur.

Extraire en croisant network.json et le HTML les URL des JS, puis les télécharger en masse dans /tmp/.

### Phase 2: Identification de la pile technique

```
Champ dataEngine de canvas-info.json :
├─ "three.js rXXX" → Three.js (r170+ : possiblement TSL → references/tsl-extraction.md)
├─ "Babylon.js vX.X" → Babylon.js
├─ null → distinguer plus finement :
│   ├─ bundle contient createShader/shaderSource → Raw WebGL / PixiJS
│   └─ bundle contient getContext('2d') sans appel WebGL → 2D Canvas (→ references/porting-strategy.md § 2D Canvas)
└─ pas de canvas → animation CSS/SVG

L'URL ou des signatures HTML correspondent à une plateforme connue → passer directement au workflow dédié (phases génériques 3-4 sautées) :
├─ unicorn.studio → references/unicorn-studio.md (configuration + shader via l'API REST Firestore)
└─ shaders.com → references/shaders-com.md (payload Nuxt + décodage XOR + traduction TSL→GLSL)

Confirmation par scan : bash scripts/scan-bundle.sh /tmp/*.js
→ mémo des signatures de frameworks : references/tech-signatures.md
```

### Phase 3: Extraction de la configuration

```
1. Chercher une API publique → récupérer la configuration directement (la réponse API peut être encodée → references/encoded-definitions.md)
2. Extraire du payload Nuxt / __NEXT_DATA__ / JSON embarqué dans le HTML
3. Extraire les valeurs par défaut du bundle JS
→ détails : references/config-extraction.md
```

### Phase 4: Extraction du code shader

Utiliser un **Agent** pour analyser le bundle JS (1 Mo+ inadapté au contexte principal).
→ Modèle de prompt agent et règles de déobfuscation : `references/extraction-workflow.md`

### Phase 5: Portage

```
Shader 2D plein écran pur → WebGL2 natif (zéro dépendance)
3D / PBR / GPGPU → conserver le framework d'origine (importmap CDN)
Incertain → partir du framework d'origine, réévaluer en Phase 6
→ détails : references/porting-strategy.md
```

### Phase 6: Évaluation de simplification

Une fois le portage terminé, vérifier soi-même le rendu (ouvrir la page et comparer les captures). Si le rendu est correct et qu'une simplification est possible, **proposer le plan de simplification à l'utilisateur**, qui décide de l'exécuter ou non.

### Phase 7: Rapport d'extraction (demander à l'utilisateur s'il le veut)

Une fois l'extraction terminée, **demander à l'utilisateur** s'il souhaite générer `EXTRACTION-REPORT.md` (la relecture de l'historique de conversation consomme des tokens supplémentaires).

Structure du rapport :
```markdown
# Rapport d'extraction : {nom du projet}
**Source / auteur / plateforme / date**

## Effet visé (description en une phrase)
## Démarche d'extraction et chronologie (problème → correctif, itération par itération)
## Structure de la scène (arbre de composants / structure des couches)
## Pipeline de rendu final (liste des passes)
## Fichiers de ressources clés
## Enseignements clés (tableau : enseignement / impact / lieu de capitalisation)
## Différences connues restantes
## Pile technique (origine vs portage)
```

Le rapport est déposé dans le répertoire du projet (ex. `ascii-glyph-dither/EXTRACTION-REPORT.md`).

## Index des references

| Quand c'est nécessaire | À lire |
|--------|------|
| Identifier le framework (signatures Three.js/WebGL/PixiJS) | `references/tech-signatures.md` |
| Prompt d'extraction Agent + règles de déobfuscation | `references/extraction-workflow.md` |
| Récupérer les paramètres de configuration (API/payload/embarqué) | `references/config-extraction.md` |
| Reconstruction de shaders à nœuds Three.js TSL | `references/tsl-extraction.md` |
| Décodage de configurations encodées/chiffrées | `references/encoded-definitions.md` |
| Pièges d'injection GLSL onBeforeCompile | `references/shader-injection.md` |
| Choix du framework de portage + structure du projet | `references/porting-strategy.md` |
| Workflow dédié **Unicorn Studio** (curtains.js + Firestore) | `references/unicorn-studio.md` |
| Workflow dédié **shaders.com** (TSL + encodage XOR + piège Y-flip) | `references/shaders-com.md` |


---

## Ressources locales du dossier

Ressources jointes (usage autonome — lire au besoin pendant l'application du prompt) :
- `references/config-extraction.md`
- `references/encoded-definitions.md`
- `references/extraction-workflow.md`
- `references/porting-strategy.md`
- `references/shader-injection.md`
- `references/shaders-com.md`
- `references/tech-signatures.md`
- `references/tsl-extraction.md`
- `references/unicorn-studio.md`
