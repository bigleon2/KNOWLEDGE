# Shader Extraction de code shader : Agent Prompt et déobfuscation

## Agent modèle de prompt d'extraction approfondie

Lancer l'Agent (subagent_type: general-purpose）pour analyser le bundle :

```
Analyser le fichier /tmp/main.js（bundle JS minifié d'environ X Mo), extraire tout le code lié aux effets visuels.

Contenu à extraire :

1. **GLSL Shader source**：chercher les chaînes contenant "precision", "uniform", "void main",
   "gl_FragColor", "gl_Position" Extraire les vertex/fragment shader complets.

2. **Classes JS liées au rendu**：canvas/renderer création, gestion des particules/géométries,
   requestAnimationFrame boucle d'animation, code d'interaction souris.

3. **Table de correspondance des symboles**：minified noms de variables → signification d'origine
   （THREE.Vector2, THREE.Color, THREE.Scene  etc.)

4. **Configuration et paramètres**：couleurs, tailles, densités par défaut et autres paramètres réglables

Enregistrer tout le code extrait dans /tmp/extracted-effects.txt，annoté par sections fonctionnelles.
```

**Point clé**：Agent peut voir le fichier complet ; le contexte principal ne peut pas contenir un bundle de 1MB+ ou plus.

## Identifier les symboles minifiés

Déduire via les paramètres du constructeur et les appels de méthodes :

```javascript
new ??(40, w/h, 0.1, 1000)       → PerspectiveCamera(fov, aspect, near, far)
new ??(-1, 1, 1, -1, 0, 1)      → OrthographicCamera
new ??({canvas, antialias, ...}) → WebGLRenderer
new ??(2, 2)                     → PlaneGeometry(w, h)
new ??(data, w, h, fmt, type)    → DataTexture
new ??(w, h, {minFilter, ...})   → WebGLRenderTarget

??.setRenderTarget()  → renderer
??.getElapsedTime()   → clock
??.setAttribute()     → bufferGeometry
```

## Déshabillage du framework (React / Vue etc. → Vanilla JS）

Canvas Les effets sont souvent enveloppés par des frameworks React/Vue. Stratégie de déshabillage :

1. **Trouver le point d'entrée des effets de bord**：`useEffect`/`onMounted` le code d'initialisation Canvas est la logique centrale
2. **Collecter le cleanup**：toutes les opérations de destruction (`removeEventListener`、`cancelAnimationFrame`、`observer.disconnect()`）rassemblées en une fonction `destroy()` 
3. **Abandonner l'enveloppe réactive**：Canvas l'état (positions de particules, compteur de trames, etc.) est lu/écrit uniquement dans le RAF, utiliser directement `let` variables, sans besoin de `useState`/`ref` et autres conteneurs réactifs

Les API natives (`IntersectionObserver`、`ResizeObserver`、`matchMedia` etc.) ne sont pas affectées par le framework, à conserver telles quelles.

## Règles de déobfuscation

1. **Noms de classes**：déduire des paramètres du constructeur et des appels de méthodes
2. **Noms de variables**：nommer selon l'usage (`ringPos`, `particleScale`, `simMaterial`）
3. **Shader Variables**：uniform/varying noms généralement non minifiés (`uTime`, `vPosition`）
4. **Conserver le GLSL d'origine**：shader le code est généralement une chaîne complète, à extraire directement
5. **Injection de chaînes**：`${someVar.noise}` indique que la bibliothèque de bruit est injectée dans le shader
