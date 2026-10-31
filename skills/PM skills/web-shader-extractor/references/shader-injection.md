# Pièges de l'injection GLSL via onBeforeCompile

## Scénario

Quand on utilise la fonction `transmission` de `MeshPhysicalMaterial` mais qu'un effet renforcé est nécessaire (comme le MeshTransmissionMaterial de drei),
on injecte du code GLSL personnalisé via `material.onBeforeCompile`.

## Pièges courants

### 1. Différences de signature selon la version

Les fonctions internes de Three.js changent de signature selon la version :

```glsl
// r166 et avant
vec4 getIBLVolumeRefraction(n, v, roughness, diffuseColor, specularColor, specularF90,
  pos, modelMatrix, viewMatrix, projectionMatrix, ior, thickness,
  attenuationColor, attenuationDistance)

// r167+ ajoute le paramètre dispersion
vec4 getIBLVolumeRefraction(n, v, roughness, diffuseColor, specularColor, specularF90,
  pos, modelMatrix, viewMatrix, projectionMatrix, dispersion, ior, thickness,
  attenuationColor, attenuationDistance)
```

**Vérifier obligatoirement la signature réelle de la version cible** :
```bash
curl -s "https://cdn.jsdelivr.net/npm/three@0.167.0/src/renderers/shaders/ShaderChunk/transmission_pars_fragment.glsl.js" \
  | tr '\n' ' ' | grep -oE 'vec4 getIBLVolumeRefraction\([^)]+\)'
```

### 2. Le GLSL n'autorise pas les définitions de fonctions imbriquées

```glsl
// Erreur ! Le GLSL ne permet pas de définir une fonction dans une fonction
void main() {
  float myRand(vec2 co) { return fract(sin(...)); }  // échec de compilation
}

// Correct : les fonctions doivent être en portée globale
float myRand(vec2 co) { return fract(sin(...)); }
void main() {
  float r = myRand(uv);
}
```

### 3. Garde des macros de compilation conditionnelle

Certaines variables ne sont disponibles que sous des macros spécifiques :
- `vWorldPosition` → nécessite `USE_TRANSMISSION` activé
- `vTransmissionMapUv` → nécessite `USE_TRANSMISSIONMAP` activé
- `roughnessFactor` → disponible après `lights_physical_fragment`

```glsl
// En remplaçant #include <transmission_fragment>
// le code d'origine est enveloppé dans #ifdef USE_TRANSMISSION, le code de remplacement doit aussi l'inclure
#ifdef USE_TRANSMISSION
  // ... votre code
#endif
```

### 4. Conflits de noms de variables

Les fonctions/variables globales injectées peuvent entrer en conflit avec les internes de Three.js :
- éviter les noms génériques comme `hash`, `random`, `noise`
- préfixer les fonctions personnalisées : `snoise` → OK, `random` → conflit probable
- préfixer les noms d'uniforms par `u` : `uDistortion`, `uNoiseTime`

## Motifs recommandés

### Injection sûre : modifier normal sans remplacer tout le chunk

```javascript
material.onBeforeCompile = (shader) => {
  shader.uniforms.uDistortion = { value: 0 };
  shader.uniforms.uNoiseTime = { value: 0 };

  // Ajouter au tout début du fragment shader les déclarations d'uniforms + les fonctions utilitaires
  shader.fragmentShader = `
    uniform float uDistortion;
    uniform float uNoiseTime;
    ${noiseGLSL}
  ` + shader.fragmentShader;

  // Insérer la perturbation des normales avant transmission_fragment
  shader.fragmentShader = shader.fragmentShader.replace(
    '#include <transmission_fragment>',
    `
    #ifdef USE_TRANSMISSION
    {
      // perturber normal pour influencer la direction de réfraction
      if (uDistortion > 0.0) {
        normal = normalize(normal + uDistortion * vec3(
          snoiseFractal(vWorldPosition * 0.08 + vec3(uNoiseTime)),
          snoiseFractal(vWorldPosition.zxy * 0.08 - vec3(uNoiseTime)),
          snoiseFractal(vWorldPosition.yxz * 0.08)
        ));
      }
    }
    #endif
    #include <transmission_fragment>
    `
  );
};
```

### Remplacement complet : quand il faut échantillonnage aléatoire multiple + aberration chromatique

Quand on recherche le grain du MeshTransmissionMaterial (bruit d'échantillonnage aléatoire) et l'effet d'aberration chromatique,
il faut remplacer complètement `#include <transmission_fragment>`. Points clés :

1. Conserver l'enveloppe `#ifdef USE_TRANSMISSION` / `#endif`
2. Conserver les blocs `#ifdef` de transmissionMap et thicknessMap
3. Utiliser la signature de `getIBLVolumeRefraction` de la bonne version
4. Pour gérer soi-même l'aberration chromatique, passer `dispersion = 0.0` et échantillonner R/G/B avec des IOR différents
5. Faible nombre d'échantillons (6) + décalage aléatoire par pixel → produit un grain de film visible

## Aide-mémoire des sources des effets visuels

| Effet | Source | Implémentation |
|------|------|----------|
| Réfraction du verre | MeshPhysicalMaterial `transmission` | intégré à Three.js |
| Aberration chromatique | échantillonnage R/G/B avec IOR différents | remplacement de transmission_fragment |
| Grain de film | faible échantillonnage + direction aléatoire par pixel | remplacement de transmission_fragment |
| Distorsion organique | bruit simplex perturbant les normales/directions de réfraction | injection via onBeforeCompile |
| Décalage chromatique | propriété `dispersion` (r167+) | intégré à MeshPhysicalMaterial |
