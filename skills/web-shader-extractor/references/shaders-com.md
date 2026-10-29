# Flux d'extraction shaders.com

shaders.com est un outil de conception de shaders, bâti sur Nuxt.js + Three.js r183 TSL + Supabase.

## Signes distinctifs

- URL : `shaders.com/collection/{slug}/{presetId}` ou `shaders.com/preset/{id}`
- Canvas : `data-renderer="shaders"` + `data-engine="three.js r183"`
- Nuxt.js (chemins `_nuxt/`)
- Authentification Clerk
- Stockage Supabase (`data.shaders.com/storage/v1/`)

## Différences d'architecture clés

Totalement différent d'Unicorn Studio :
- **Pas de GLSL** — utilise le système de nœuds Three.js TSL (Three Shader Language)
- **87 types de composants** — chacun avec sa propre fonction TSL `fragmentNode`
- **Les données de définition sont encodées XOR + base64**
- **Composants imbriquables** — structure arborescente (les children d'un Glass sont ses effets internes)

## Récupération des données

### Points d'entrée API

```bash
# Variante de collection (avec définitions encodées) — public, sans authentification
curl -s "https://shaders.com/api/collections/{slug}/{variantId}"

# API de prévisualisation (définitions encodées + injection de filigrane)
curl -s "https://shaders.com/api/preview/preset/{presetId}"

# Payload Nuxt (métadonnées seules, sans définition de shader)
curl -s "https://shaders.com/collection/{slug}/{id}/_payload.json"
```

### Décodage des définitions

Les définitions sont encodées XOR + base64, avec deux jeux de clés :

1. **API du site** (`/api/collections/`) :
   - clé d'obfuscation : `a5e7244ad0973f07e10285bfa75ddbe4` (issue de la runtime config Nuxt)
   - noms de composants/propriétés en codes courts (`C52`=Plasma, `p06`=angle, etc.)
   - décodage : `JSON.parse(XOR(base64decode(encoded), keyBytes))`
   - puis il faut la table de correspondance code→name pour restituer les noms lisibles

2. **API de prévisualisation** (`/api/preview/`) :
   - clé : `shaders-preview-key`
   - noms de propriétés lisibles (aucune table nécessaire)
   - attention : injection d'un composant `ImageTexture` de filigrane

### Table de correspondance des codes

Les 87 composants sont numérotés `C00-C86` par tri alphabétique, les 233 propriétés `p00-p232` par tri alphabétique.
La table peut être extraite du bundle JS.

## Pièges connus

### Le retournement de l'axe Y (récurrent !)

**Retournement systématique du Y des textures SDF et des coordonnées UV** — confirmé lors de multiples extractions :

Le binaire SDF de shaders.com (`.bin`) utilise le **système de coordonnées image** (Y=0 en haut),
alors qu'en WebGL la coordonnée de texture a Y=0 en bas. Le chargement direct retourne les formes haut-bas.

```glsl
// Erreur : échantillonner directement avec shapeUV
float sdf = texture(tSDF, shapeUV).r;

// Correct : retourner Y
vec2 sdfUV = vec2(shapeUV.x, 1.0 - shapeUV.y);
float sdf = texture(tSDF, sdfUV).r;

// Attention : la composante Y du gradient doit aussi être inversée
float dSdy = -(texture(tSDF, sdfUV - vec2(0, eps)).r - sdf) / eps;
```

De même, le `center.y` des définitions de composants est en coordonnées DOM (Y=0 en haut),
à retourner dans le shader de Glass : `center.y = 1.0 - center.y`.

### Format du binaire SDF

- Format : 512×512 Float32 mono-canal (1 048 576 octets = 512² × 4)
- Plage : distance signée, négatif=intérieur, positif=extérieur (ex. [-0.065, 0.486])
- **Aucun remapping nécessaire** (ne pas faire `*2-1`), utiliser les valeurs brutes
- L'extension `OES_texture_float_linear` est requise pour le filtrage linéaire
- Chargement WebGL2 : `gl.texImage2D(gl.TEXTURE_2D, 0, gl.R32F, 512, 512, 0, gl.RED, gl.FLOAT, data)`

## Aide-mémoire des types de composants

| Catégorie | Composants | Complexité |
|------|------|--------|
| Textures | Plasma, Godrays, SimplexNoise, LinearGradient, RadialGradient | moyenne |
| Formes | Glass, Blob, Circle, Ring, Star, RoundedRect, Polygon | haute (Glass la plus complexe) |
| Distorsions | WaveDistortion, ChromaticAberration, Liquify, Twirl, Bulge | basse-moyenne |
| Stylisation | FilmGrain, Halftone, Ascii, Dither, Glow, Bloom | basse-moyenne |
| Post-traitement | Blur, ProgressiveBlur, BrightnessContrast, HueShift | basse |

## Pipeline de rendu

```
Rendu Three.js r183 TSL
├─ tente WebGPU en priorité, repli sur WebGL
├─ caméra orthographique + un seul quad plein écran
├─ composition de l'arbre de composants du bas vers le haut
├─ les composants avec children captent leur contenu par RTT (render-to-texture)
├─ blend mode par fonctions de mélange personnalisées
└─ composant Glass le plus complexe : évaluation SDF → normales par gradient → réfraction → aberration chromatique → flou → coloration → reflets → Fresnel → composition
```

## Stratégie de portage

1. **Le TSL ne se copie pas directement** — il faut le traduire en GLSL
2. **Extraire le `fragmentNode` TSL du bundle JS** → désobfusquer → traduire en GLSL
3. **Arbre de composants → pipeline multi-pass FBO**
4. **Les textures SDF exigent le Y-flip** (voir le piège ci-dessus)
5. **Le composant Glass a beaucoup de paramètres** (20+), chaque valeur doit correspondre exactement

## Traitement de l'espace colorimétrique (crucial)

Le rendu Three.js de shaders.com travaille intégralement dans l'espace **linéaire** :
- Les couleurs hex des définitions de composants (ex. `#2c2c42`) sont des valeurs **sRGB**
- La fonction `color()` du TSL convertit automatiquement sRGB→linéaire
- Tous les FBO intermédiaires stockent des valeurs linéaires
- L'encodage final linéaire→sRGB est fait par le moteur au moment du rendu

À respecter au portage :
```glsl
// 1. À la définition des couleurs : sRGB hex → linéaire
vec3 colorA = pow(vec3(0.173, 0.173, 0.259), vec3(2.2));  // #2c2c42

// 2. Passes intermédiaires : tout calculer en linéaire, sans gamma
// 3. Passe de sortie finale (une seule fois) : linéaire → sRGB
fragColor = vec4(pow(color.rgb, vec3(1.0/2.2)), color.a);
```

**Erreur courante** : appliquer la correction gamma dans une passe intermédiaire, si bien que les passes suivantes accumulent reflets/Fresnel dans un espace erroné.

## Principe d'alignement exact des paramètres

**Régler les paramètres à la main est strictement interdit.** Tous les paramètres doivent respecter exactement les formules et multiplicateurs de la traduction TSL :

```
Multiplicateur TSL d'origine     → valeur à utiliser obligatoirement en GLSL
aberration * 0.06                → ne pas remplacer par 0.12
fresnelSoftness * 0.06           → ne pas remplacer par 0.12
fresnel (0.17)                   → ne pas remplacer par 0.4
SDF gradient eps = 0.01          → ne pas remplacer par 0.005
```

Si le rendu visuel ne colle pas, vérifier dans l'ordre :
1. l'espace colorimétrique (la confusion sRGB/linéaire est la cause la plus fréquente)
2. les différences d'implémentation du bruit (implémentation Perlin vs `mx_noise_float`)
3. la base de temps
4. l'ordre du pipeline FBO par rapport à l'arbre de composants

**Ne jamais** « compenser » un écart visuel en modifiant un multiplicateur — cela exploserait sous d'autres configurations de paramètres.

## Convention temporelle du TSL

`timerLocal(speed)` = incrémente de `speed` unités par seconde. Au portage : `uTime = seconds * speed`.

Puis le shader applique ensuite son propre coefficient :

| Composant | Paramètre speed | Multiplicateur interne du shader | Vitesse réelle/s |
|------|-----------|----------------|------------|
| Plasma | 2 | × 0.125 | 0.25 |
| Godrays | 0.7 | × 0.2 | 0.14 |
| WaveDistortion | 0.8 | × 0.5 | 0.4 |
| FilmGrain | — | pas de temps (statique) | 0 |

## Correspondance d'identifiants TSL→GLSL (SPCVwBqR.js)

Correspondances usuelles (variables selon la version du build, extraction dynamique requise) :

| Nom local | Fonction TSL | GLSL |
|--------|---------|------|
| C / z | vec4() | vec4 |
| x / D | vec2() | vec2 |
| q / N | vec3() | vec3 |
| P / J | resolution | u_resolution |
| A / $ | uv | vUv |
| se / Oe | sin() | sin() |
| W / I | cos() | cos() |
| ne | mix() | mix() |
| D | smoothstep() | smoothstep() |
| fe | clamp() | clamp() |
| ar | mx_noise_float() | perlinNoise3D() |
| dr / Gt | timerLocal() | u_time × speed |
| Me / wt | rtt() | FBO pass |
| Ce | renderOutput() | fragColor |
