# Extraction des paramètres de configuration

Les valeurs de configuration doivent être extraites du site source, jamais devinées. (Exemple d'erreur de devinette : couleur fausse de 60x, motif totalement différent)

## Sources (par priorité)

### 1. API REST publique

```bash
# Chercher les points d'API dans le bundle JS
grep -oE 'api/(presets|shaders|collections)[^"]*' /tmp/*.js
# Appel direct
curl -s -L --compressed 'https://example.com/api/collections/slug/uuid'
```

API la réponse peut être encodée → voir `encoded-definitions.md`

### 2. Nuxt.js Payload

```bash
grep -oE '_payload\.json[^"]*' /tmp/page.html          # payload URL
grep -oE 'public:\{[^}]*\}' /tmp/page.html             # runtime config（peut contenir des clés）
```

### 3. Next.js

```bash
# App Router (RSC)
grep -oE '"(scene|glass|postProcessing)":\{' /tmp/page.html
# Pages Router
grep -o '<script id="__NEXT_DATA__"[^>]*>[^<]*' /tmp/page.html | sed 's/.*>//'
```

### 4. JSON inline / variables globales window

```bash
grep -oE 'window\.__CONFIG__\s*=\s*\{[^;]+' /tmp/page.html
```

### 5. JS Bundle par défaut（dernier recours）

```bash
grep -oE '(config|options|settings)\s*=\s*\{' /tmp/entry-chunk.js
```

## Vérification

- Plage de couleurs : 0-1 ou 0-255 ?
- resolution：valeur en pixels ou facteur d'échelle ?
- Booléens :`false` `false` saute-t-il toute la passe de rendu ?
