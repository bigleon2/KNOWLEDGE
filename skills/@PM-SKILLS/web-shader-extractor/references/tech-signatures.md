# Signatures d'identification des frameworks

## Three.js

**Non obfusqué** : `THREE.`, `WebGLRenderer`, `ShaderMaterial`, `BufferGeometry`

**Après obfuscation**（déduit via les paramètres du constructeur）：

| Motif d'appel | Classe d'origine |
|---------|--------|
| `new X({canvas, antialias, alpha})` | `WebGLRenderer` |
| `new X(fov, aspect, near, far)` — 4 nombres | `PerspectiveCamera` |
| `new X(-1, 1, 1, -1, 0, 1)` — 6 paramètres | `OrthographicCamera` |
| `new X(w, h, {wrapS, minFilter})` | `WebGLRenderTarget` |
| `new X(data, w, h, format, type)` — Float32Array | `DataTexture` |
| `new X(2, 2)` comme géométrie | `PlaneGeometry` |
| `new X({uniforms, vertexShader, fragmentShader})` | `ShaderMaterial` |
| `X.getElapsedTime()` | `Clock` |

**Constantes**：`ClampToEdgeWrapping`, `NearestFilter`, `RGBAFormat`, `FloatType`, `DoubleSide`

## 2D Canvas

`dataEngine: null`  : utiliser `getContext('2d')` présence/absence + `createShader`/`shaderSource` présence/absence pour distinguer :
- présence de  `getContext('2d')`，sans appel WebGL → pur Canvas 2D
- avec appels WebGL → Raw WebGL / PixiJS

## Raw WebGL

```javascript
gl.createShader / gl.shaderSource / gl.compileShader / gl.createProgram
gl.bindBuffer / gl.bindFramebuffer / gl.drawArrays
```

## PixiJS

`PIXI.Application`, `PIXI.Filter`, `new PIXI.Filter(vertSrc, fragSrc, uniforms)`

## Babylon.js

`BABYLON.Engine`, `BABYLON.ShaderMaterial`, `BABYLON.Effect.ShadersStore`

## GPGPU mode (Móshì)

Deux `WebGLRenderTarget` (ping-pong) + `OrthographicCamera(-1,1,1,-1,0,1)` + `PlaneGeometry(2,2)` + `DataTexture` position initiale + boucle `setRenderTarget`

## Bruit courant

| Fonction (hánshù) | Type (lèixíng) |
|------|------|
| `snoise` | Simplex noise (Ashima) |
| `cnoise` | Classic Perlin |
| `cellular` | Worley/Voronoi |
| `fbm` | Fractal Brownian Motion |
