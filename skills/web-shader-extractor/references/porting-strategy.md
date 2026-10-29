# Stratégie de portage

## Choix du framework

```
Canvas 2D pur (getContext('2d'), sans WebGL) ?
├─ OUI → Vanilla JS (zéro dépendance, voir § Canvas 2D ci-dessous)
└─ NON → shader plein écran 2D pur / post-traitement pur ?
         ├─ OUI → WebGL2 natif (zéro dépendance)
         └─ NON → implique 3D / PBR / GPGPU / onBeforeCompile ?
                  ├─ OUI → conserver le framework d'origine (importmap CDN)
                  └─ incertain → partir du framework d'origine, réévaluer en Phase 6
```

## Structure d'un projet WebGL natif

```
<name>/
├── index.html        # <canvas>
├── js/
│   ├── main.js       # initialisation WebGL2 + boucle de rendu multi-pass
│   └── shaders/      # .glsl.js (export const fragmentShader)
└── README.md
```

- `canvas.getContext('webgl2')` + `#version 300 es` (`in`/`out`, `texture()`)
- multi-pass par framebuffer + texture attachment
- pilotage par `requestAnimationFrame`

## Structure d'un projet Three.js

```
<name>/
├── index.html        # importmap CDN
├── js/
│   ├── main.js       # scène/caméra/moteur de rendu + pipeline RTT
│   └── shaders/      # .glsl.js
└── README.md
```

- `RawShaderMaterial` + `glslVersion: THREE.GLSL3`
- `WebGLRenderTarget` pour le multi-pass
- importmap CDN, aucune installation

Gabarit CDN :
```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.183.0/build/three.module.js" } }
</script>
```

Vérification : `curl -sI '<url>' | head -3`

## Points clés du portage des scènes à composition multi-couches

Les scènes extraites d'outils no-code comme Unicorn Studio / curtains.js comportent souvent des chaînes FBO complexes. Pièges courants et bonnes pratiques :

### 1. Comprendre la relation parent-enfant parentLayer / effects

Dans Unicorn Studio :
- Le tableau `effects[]` d'une couche **Element** (shape/text/image) stocke les UUID des effets enfants
- Le champ `parentLayer` d'une couche **Effect** pointe vers l'UUID de l'élément parent
- Les effets enfants sont rendus dans l'ordre du tableau effects, chaque passe lisant le FBO de la précédente

Le portage doit restituer cette chaîne FBO ; impossible de tout fusionner en une seule passe.

### 2. Fond transparent avec showBg=0

`showBg=0` signifie que le shader sort `vec4(0)` (totalement transparent) hors de la géométrie touchée.
Ce n'est pas du « noir » mais de la **transparence** : la composition révèle ensuite les couches inférieures.

```glsl
// Correct : showBg=0 → transparent
if (hit < 0.5) { fragColor = vec4(0.0); return; }

// Erreur : sortir du noir (écraserait les couches inférieures)
if (hit < 0.5) { fragColor = vec4(0.0, 0.0, 0.0, 1.0); return; }
```

Le portage doit superposer le résultat aux couches inférieures par une passe d'alpha compositing (`fg + bg * (1 - fg.a)`).

### 3. Mode de composition des éléments texte/image

Les couches Element (texte/image) doivent être rendues en Canvas 2D puis téléversées comme texture WebGL.
**Le mode de composition détermine le rendu visuel** :

```glsl
// Erreur : recouvrement alpha-over (perte de la texture de fond)
fragColor = mix(bg, vec4(txt.rgb, 1.0), txt.a);

// Erreur : additif (sature en blanc, perte des variations de teinte)
fragColor = vec4(bg.rgb + txt.rgb * txt.a, 1.0);

// Correct : amplification de luminance (conserve les variations de teinte du bruit de fond)
fragColor = vec4(bg.rgb * mix(1.0, amplifyFactor, txt.a), 1.0);
```

**Principe** : dans la scène d'origine, l'élément textuel est superposé à une couche de bruit ; après glyph dither,
la couleur des caractères est celle du pixel à cet endroit. Si la zone de texte est unie, les caractères ASCII sont unis.
Avec l'amplification de luminance, les proportions de teintes du bruit sont intégralement conservées (violet:cyan:sombre amplifiés du même coefficient),
et les caractères issus du glyph dither héritent des variations colorées de la texture de bruit.

### 4. Instances d'effets répétées

Un même effet (ex. noiseFill) peut apparaître plusieurs fois dans la scène : une fois comme couche de fond autonome,
une fois comme effet enfant d'un groupe de formes. Les paramètres peuvent être identiques mais la position dans le pipeline diffère :
la sortie de l'effet enfant sera traitée par les effets suivants (ex. réfraction SDF), produisant un rendu différent.

### 5. Compatibilité du glyph atlas

Un atlas PNG de glyphes embarqué en base64 fait échouer `texImage2D` sur certains navigateurs/environnements WebGL avec
`INVALID_VALUE: bad image data`. Recommandé : le générer dynamiquement en Canvas 2D.

### 6. Cohérence de l'espace colorimétrique (source d'écart visuel la plus fréquente)

Des outils comme Three.js / shaders.com travaillent intégralement dans l'espace **linéaire**. En portant vers du WebGL natif :

```
Mauvaise approche (un gamma par passe) :
  Passe1 : sort pow(linéaire, 1/2.2)       ← sRGB
  Passe2 : lit le sRGB + calcule les reflets (linéaire) + sort pow(résultat, 1/2.2)  ← incohérent !

Bonne approche (linéaire de bout en bout, un seul gamma final) :
  Passe1~N : sortent toutes des valeurs linéaires
  Finale :  pow(linéaire, 1/2.2)           ← l'unique encodage sRGB
```

Définition de couleur hex → `pow(srgb, 2.2)` vers le linéaire → calculs en linéaire de bout en bout → sortie finale `pow(linéaire, 1/2.2)`.

### 7. Principe d'alignement exact des paramètres

**Strictement interdit de régler des paramètres à la main pour « compenser » un écart visuel.** Tous les multiplicateurs des formules doivent correspondre exactement au code d'origine.
Si l'effet est faux, chercher les causes racines — espace colorimétrique, implémentation du bruit, base de temps — plutôt que modifier les multiplicateurs.
Un réglage manuel peut sembler meilleur dans la configuration courante mais explosera sous d'autres combinaisons de paramètres.

## Canvas 2D

Un fichier par effet, exportant `create<Name>Effect(container)` → `{ destroy }`. Le multi-effet est géré par `main.js` qui orchestre la bascule.

### Exigences de performance

- `IntersectionObserver` + `visibilitychange` — stopper le RAF quand non visible
- plafonner le DPR à `Math.min(devicePixelRatio, 2)`
- post-traitement mis en cache dans un Canvas hors écran, le contenu statique n'est reconstruit qu'au resize
- données volumineuses de particules en `Float32Array`

## Spécifications générales

- Modules ES (`import`/`export`)
- renommer les variables minifiées en noms signifiants
- README avec description de l'effet, principe technique, paramètres réglables

## Phase 6 : évaluation de simplification

**Déclencheur** : après le portage, vérifier soi-même la justesse du rendu. **Proposition, jamais exécution automatique** — seule étape du flux nécessitant une décision de l'utilisateur.

```
N'a servi que de RawShaderMaterial + WebGLRenderTarget + quad plein écran ?
├─ → simplifiable en WebGL2 natif (~600 KB en moins)
Fait usage de PBR / onBeforeCompile / scène 3D ?
├─ → ne pas simplifier
Incertain ?
└─ → ne pas proposer
```
