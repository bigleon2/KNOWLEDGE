# Three.js TSL identification et reconstruction

Three.js r170+  : le TSL (Three Shading Language) compose des graphes de nœuds shader par chaînes d'appels JS, compilés en GLSL à l'exécution.

## Signaux d'identification

1. Bundle contient de nombreux `uniform`/`shader` mais quasiment aucun `precision`/`gl_FragColor`
2. canvas `data-engine` indique r170+
3. présence de `.mul()`/`.add()`/`.toVar()`/`.assign()` en chaîne

## TSL → GLSL (mapping)

| TSL | GLSL |
|-----|------|
| `screenUV` | `gl_FragCoord.xy / resolution` |
| `viewportSize` | `uniform vec2 resolution` |
| `float()`/`vec2()`/`vec3()`/`vec4()` | homonymes (mais fonctions JS en TSL) |
| `.mul()`/`.add()`/`.sub()`/`.div()` | `*`/`+`/`-`/`/` |
| `sin()`/`cos()`/`mix()`/`smoothstep()` | homonymes |
| `clamp()`/`abs()`/`fract()`/`floor()` | homonymes |
| `pow()`/`exp()`/`sqrt()`/`dot()`/`length()` | homonymes |
| `Fn()` | shader wrapper de fonction (inliné en GLSL) |
| `uniform()` | `uniform <type> name` |
| `convertToTexture()` | RTT（rendu multi-pass） |
| `.sample(uv)` | `texture(sampler, uv)` |
| `.toVar()`/`.assign()` | déclaration/affectation de variables mutables |
| `.oneMinus()` | `1.0 - x` |

## Étapes de reconstruction

1. **Localiser**：chercher autour du nom du composant la propriété `fragmentNode` 
2. **Table de correspondance**：déduire des imports en tête du bundle la table → TSL fonctions
   ```javascript
   import { A as screenUV, W as sin, ... } from "three-module"
   ```
3. **Traduire**：chaînages → GLSL expressions
   ```javascript
   // TSL: screenUV.x.sub(center.x).mul(aspect)
   // GLSL: (uv.x - center.x) * aspect
   ```
4. **RTT**：`convertToTexture(childNode)` → pass indépendant rendu vers FBO ; dans le shader principal, `texture()` fait l'échantillonnage
