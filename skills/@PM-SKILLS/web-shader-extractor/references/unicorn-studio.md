# Flux d'extraction Unicorn Studio

Unicorn Studio (unicorn.studio) est un outil de design WebGL no-code, qui utilise curtains.js comme moteur de rendu et Firebase/Firestore comme backend.

## Signes distinctifs

- Motif d'URL : `unicorn.studio/remix/{remixId}` ou `unicorn.studio/edit/{designId}`
- Meta tag : `<meta name="ai:technical-stack" content="Vue 3, curtains.js, Firebase, JavaScript SDK">`
- SDK embarqué : `unicornStudio-*.js` (version embed ~84 Ko)
- Bundle de l'app principale : `index-*.js` (~2,1 Mo, contient les gabarits de shaders)

## Chemins de récupération des données

### Chemin 1 : API REST Firestore (recommandé, pour les remix)

```bash
# Configuration Firebase (extraite du bundle JS frontal de unicorn.studio, à récupérer dynamiquement à chaque extraction)
# Méthode : curl -s https://www.unicorn.studio/ | grep -oP 'apiKey:"[^"]+"' | head -1
API_KEY="<extraire dynamiquement du bundle du site>"
PROJECT="unicorn-studio"

# Étape 1 : récupérer les métadonnées du remix (versionId, designId, infos créateur)
curl -s "https://firestore.googleapis.com/v1/projects/$PROJECT/databases/(default)/documents/remixes/{REMIX_ID}?key=$API_KEY"

# Étape 2 : récupérer les données de version (toutes les définitions de calques, paramètres, références de textures)
# versionId extrait de fields.versionId.stringValue à l'étape 1
curl -s "https://firestore.googleapis.com/v1/projects/$PROJECT/databases/(default)/documents/versions/{VERSION_ID}?key=$API_KEY"
```

### Chemin 2 : données embed GCS/CDN (pour les embeds publiés)

```bash
# Utilisateur non Pro
curl -s "https://storage.googleapis.com/unicornstudio-production/embeds/{DESIGN_ID}"

# Utilisateur Pro
curl -s "https://assets.unicorn.studio/embeds/{DESIGN_ID}"
```

Format embed JSON : `{ options: {...}, layers/history: [...], modules: [...] }`
Contient `compiledFragmentShaders[]` et `compiledVertexShaders[]` (GLSL déjà compilé).

### Chemin 3 : extraction depuis le JSON embarqué dans la page

Les embeds Unicorn Studio utilisent les attributs HTML `data-us-project` ou `data-us-project-src`,
le SDK `init()` scanne ces attributs et charge le projet correspondant.

## D'abord déterminer la forme des données

Unicorn Studio a au moins deux formes de données courantes :

### 1. scène embed/export

- Généralement le JSON de scène destiné à `addScene()`
- Comporte souvent déjà `compiledFragmentShaders[]` / `compiledVertexShaders[]`
- Ce format peut alimenter directement le runtime d'embed

### 2. historique editor/version

- Source courante : le `history` de Firestore `versions/{id}`
- Ce sont les données de calques brutes de l'éditeur, **impossibles** à donner directement à `addScene()`

Si `history` est confondu avec une scène embed, les symptômes typiques sont :

- `Plane: No fragment shader provided, will use a default one`
- `Plane: No vertex shader provided, will use a default one`
- `No composite shader data for element`
- le canvas se crée mais l'image reste noire ou se limite aux calques par défaut

## Structure des collections Firestore

| Collection | Usage | Champs clés |
|---|---|---|
| `designs` | métadonnées de design | creatorId, name, versionId, hasEmbed |
| `versions` | données de version (cœur) | history[], options |
| `remixes` | designs remixables | designId, versionId, creatorId, thumbnail |

## Structure des données de version

Le format REST Firestore enveloppe les valeurs dans `{stringValue, integerValue, arrayValue, mapValue, ...}` — analyse récursive requise.

Chaque élément du tableau `history` est un calque :

```
layerType: "effect" | "text" | "image" | "model" | "shape"
type:      type d'effet (gradient, noiseFill, sdf_shape, glyphDither, bloomFast, ...)
```

### Paramètres de calque (courants)

- `pos`, `scale`, `speed`, `opacity`, `blendMode`
- `trackMouse`, `trackAxes`, `mouseMomentum`
- `parentLayer`: UUID ou false (lien vers le parent)
- `breakpoints[]`: configuration des points de rupture responsifs
- `states`: animations appear/scroll/hover/mousemove
- `customFragmentShaders[]`, `customVertexShaders[]` (généralement vides quand on utilise les effets intégrés)

## Stratégie d'initialisation correcte

Si ce que vous avez est un `version/history` Firestore, imiter en priorité la chaîne d'initialisation du site lui-même, ne pas forcer l'API embed.

Ordre d'appels typique :

1. `unpackageHistory()` ou `unpackVersion()`
2. `createFontScript()`
3. `createCurtains()`
4. `handleItemPlanes()`
5. `fullRedraw()`

Si le bundle de la page contient un composant Remix/Preview dédié, le suivre en priorité plutôt que la seule documentation publique UMD/SDK.

### Localisation des ressources

- Télécharger localement images/polices/textures autant que possible
- Les `src` de `history` et `fontCSS.src` doivent être remplacés par des chemins locaux
- Certains champs d'objets peuvent être des maps à clés numériques — les régulariser en tableaux avant écriture

### Paramètres propres aux types d'effets

| Effet | Paramètres clés |
|---|---|
| gradient | fill[], stops[], gradientType, gradientAngle, wrap |
| noiseFill | noiseType, turbulence, color1, color2, colorPhase, chroma, direction |
| sdf_shape | shape(0-22), refraction, extrude, smoothing, axis, animationDirection, lightPosition |
| glyphDither | characters, glyphSet, scale, gamma, monochrome, texture(sprite atlas) |
| bloomFast | amount, intensity, exposure, tint |

## Extraction du code shader

**Découverte clé** : le SDK d'embed (~84 Ko) ne contient aucun code GLSL. Les gabarits de shaders sont dans le bundle de l'app principale (~2,1 Mo), traités par un pipeline de compilation en 7 étapes puis stockés dans le JSON embed.

### Emplacement des shaders dans le bundle applicatif

Les gabarits sont des littéraux chaînes, identifiés par leur nom de variable :

```
Nom d'effet       → nom de variable
glyphDither     → X$ (fragment)
noiseFill       → WY (fragment)
sdf_shape       → XY (fragment)
gradient        → eX (fragment)
bloomFast       → Hj (fragment)
vertex générique       → ye (vertex)
vertex dégradé       → ko (vertex)
fragment composite       → Uz (composite fragment)
vertex composite       → Nz (composite vertex)
```

Attention : les noms de variables changent selon la version du build — localiser par recherche de signatures.

### Variables des gabarits

Les gabarits contiennent des placeholders `${variable}`, substitués à la compilation :

| Variable | Contenu |
|---|---|
| `${fe}` | déclarations uniform liées au masque |
| `${Vt}` | fonctions utilitaires de mélange de calques (applyLayerMix, applyLayerMixAlpha, applyLayerMixClip) |
| `${gt}` | hash PCG / fonctions aléatoires (pcg2d, randFibo) |
| `${ht}` | fonctions de blend modes (17 modes : Normal, Add, Multiply, Screen, Overlay, ...) |
| `${pe("var")}` | application du masque + sortie fragColor |
| `${wf}` | dérivées du bruit BCC (OpenSimplex2S) |
| `${Aa}` | fonctions de bruit de Perlin |
| `${yr}` | fonction de dithering anti-banding |
| `${cm}` | déclarations uniform couleurs/points d'arrêt du dégradé |
| `${xz}` | fonction de pondération gaussienne (bloom blur) |

### Pipeline de compilation

```
1. Fz() : remplace les valeurs d'uniform par des constantes
2. Dz() : traite le nombre de couleurs du dégradé (élagage switch case)
3. Mz() : évalue les switch constants (élimination de code mort)
4. Rz() : traite les blocs #ifelseopen/#ifelseclose (compilation conditionnelle)
5. Iz() : supprime les fonctions inutilisées
6. Cz() : supprime les déclarations d'uniform inutilisées
7. Bp() : retire les commentaires, normalise les blancs
```

## Pipeline de rendu (cœur — à restituer fidèlement au portage)

```
Moteur de rendu curtains.js WebGL2
├─ chaque calque d'effet = un Plane + un FBO dédié
├─ les calques sont rendus en chaîne linéaire selon renderOrder, chaque plane lisant le FBO précédent comme uTexture
├─ un Element (shape/text/image) + ses effets enfants forment un render group :
│   1. le plane de l'Element se rend d'abord → FBO_elem
│   2. les effets enfants se rendent dans l'ordre du tableau effects → FBO_child1, FBO_child2, ...
│   3. le plane Composite se rend en dernier : alpha-blend des sorties des effets enfants vers la scène de fond
├─ les effets de post-traitement autonomes (parentLayer=false) traitent la scène globale
└─ le dernier plane sort directement sur le canvas (sans FBO)
```

### La chaîne FBO Element + effets enfants (crucial)

```
Exemple d'un groupe de shapes (sdf + noise) :

FBO_before ─────────────────────────────────────────┐
                                                     │
Plane du Shape lui-même → FBO_shape (rend la géométrie de base)
    ↓                                                 │
Child noiseFill → FBO_noise (uBgTexture = FBO_shape)  │
    ↓                                                 │
Child sdf_shape → FBO_sdf (uTexture = FBO_noise)      │
    ↓ (showBg=0 : hors de la forme = vec4(0) transparent) │
    ↓                                                 │
Composite plane → FBO_result                          │
    uTexture = FBO_sdf (sortie du dernier effet enfant) │
    uBgTexture = FBO_before (scène avant l'element) ←─────┘
    output = alpha_blend(fg, bg) = fg + bg * (1 - fg.a)
```

### Mécanisme d'association des effets enfants

```js
// Le tableau effects de l'Element → liste des UUID parentLayer des effets enfants
shape.effects = ["e270a7cd-...", "fb591190-..."]

// Chaque effet enfant référence l'UUID de l'element parent
noiseFill.parentLayer = "e270a7cd-..."   // effects[0]
sdf_shape.parentLayer = "fb591190-..."   // effects[1]

// Dans le SDK embed, retrouver les effets enfants :
getChildEffectItems() {
    return this.effects.map(uuid =>
        state.layers.find(l => l.parentLayer === uuid)
    ).filter(Boolean)
}
```

### La base de temps uTime (piège majeur)

Dans le SDK embed, `uTime` **n'est pas un nombre de secondes**, il s'accumule image par image :
```js
// Dans setEffectPlaneUniforms() :
t.uniforms.time.value += speed * 60 / this.fps;
```

À 60 fps : `uTime += speed` à chaque image. Après 1 seconde, `uTime = speed × 60`.

| Calque d'effet | speed | uTime après 1 s |
|--------|-------|-------------|
| noiseFill | 0.25 | 15 |
| sdf_shape | 0.5 | 30 |
| gradient | 0.25 | 15 |

**Au portage, multiplier obligatoirement par `speed × 60`**, sinon l'animation est 15 à 60 fois trop lente :
```js
// Correct :
uni1f(prog, 'uTime', elapsedSeconds * speed * 60);
// Erreur :
uni1f(prog, 'uTime', elapsedSeconds);
```

### Le rôle clé du paramètre showBg

- `showBg=0` : quand le rayon ne touche pas la géométrie, sortie `vec4(0)` **transparent** (pas noir !)
- `showBg=1` : sans toucher, échantillonnage de `uTexture/uBgTexture` (affiche le fond)

**Au portage, showBg=0 est le piège le plus fréquent** : si l'on sort à tort un `vec4(0,0,0,1)` noir opaque,
l'alpha blend composite est écrasé au lieu de laisser voir les couches inférieures. Alpha doit valoir 0.

## Stratégie de portage

1. **Effets de post-traitement 2D purs** (glyphDither, bloomFast) : quad plein écran WebGL2 natif
2. **Effets génératifs** (noiseFill, gradient) : WebGL2 natif
3. **SDF 3D** (sdf_shape) : raymarching WebGL2 natif
4. **Scènes complexes** (composition multi-calques) : pipeline FBO multi-pass requis
5. **Calques de texte** : rendu du texte en Canvas 2D → téléversement comme texture WebGL

## Vérification Playwright

L'environnement headless par défaut de Playwright peut ne pas offrir de WebGL utilisable. Devant ces symptômes, suspecter d'abord l'environnement, pas la logique d'extraction :

- `Renderer: WebGL context could not be created`
- `0 canvas(es) found`
- `Error creating Curtains instance`
- capture d'écran totalement noire

Dans ce cas, revérifier avec `swiftshader` :

```bash
--use-angle=swiftshader
--use-gl=angle
--enable-unsafe-swiftshader
--ignore-gpu-blocklist
```

Ordre de vérification recommandé :

1. Regarder si la console montre une erreur shader/runtime ou un échec de création de contexte WebGL
2. Vérifier qu'un `canvas` est réellement présent dans le DOM
3. Capturer avec `swiftshader`
4. Comparer la composition avec la vignette du site d'origine ou la capture du premier écran

### Génération du glyph atlas

L'atlas de glyphes d'origine est un PNG base64 (problèmes de compatibilité inter-navigateurs).
Recommandé : le générer dynamiquement en Canvas 2D :

```js
function createGlyphAtlas(chars, size = 40) {
  const canvas = document.createElement('canvas');
  canvas.width = size * chars.length;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#fff';
  ctx.font = `bold ${size * 0.8}px monospace`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let i = 0; i < chars.length; i++) {
    ctx.fillText(chars[i], size * i + size / 2, size / 2);
  }
  return canvas; // → gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas)
}
```

## Points d'entrée Cloud Functions

Tous sur `https://us-central1-unicorn-studio.cloudfunctions.net/` :
- `publishEmbedTest` — publier/mettre à jour un embed (authentification requise)
- `getUserIdByUsername` — nom d'utilisateur → userId
- `handleVideos/handleModels/handleImages` — traitement des ressources
- `generateImprovedMSDF` — rendu de texte MSDF
- `generateDepthMap` — génération de cartes de profondeur
- `copyRemixAssets` — copie des ressources de remix

## Exemple : flux d'extraction complet

```bash
# 1. Extraire le remix ID de l'URL
REMIX_ID="QZxhNFb1X1OaUqaJLT9S"

# 2. Récupérer les métadonnées du remix
curl -s "https://firestore.googleapis.com/v1/projects/unicorn-studio/databases/(default)/documents/remixes/$REMIX_ID?key=$API_KEY" > remix.json

# 3. Extraire le versionId
VERSION_ID=$(python3 -c "import json; print(json.load(open('remix.json'))['fields']['versionId']['stringValue'])")

# 4. Récupérer les données de version
curl -s "https://firestore.googleapis.com/v1/projects/unicorn-studio/databases/(default)/documents/versions/$VERSION_ID?key=$API_KEY" > version.json

# 5. Analyser calques et paramètres des données de version → analyse récursive du format REST Firestore en Python/Node

# 6. Extraire du bundle applicatif les gabarits de shaders des types d'effets correspondants
curl -s "https://www.unicorn.studio/assets/index-*.js" > app-bundle.js
# Rechercher les noms de types d'effets pour localiser le code shader

# 7. Combiner paramètres + gabarits de shaders → construire un projet WebGL2 autonome
```
