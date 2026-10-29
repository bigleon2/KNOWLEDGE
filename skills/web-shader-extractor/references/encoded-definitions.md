# Décodage des configurations encodées

## Signaux d'identification

1. API renvoie le marqueur `_encoded: true` 
2. `definition` est une chaîne Base64 plutôt que du JSON
3. JS contient `atob()`/`btoa()` + `TextEncoder`/`TextDecoder` + XOR
4. Runtime config contient `obfuscationKey`

```bash
grep -oE '(atob|btoa|obfuscation|_encoded)' /tmp/*.js | sort | uniq -c
grep -oE 'obfuscationKey:"[^"]*"' /tmp/page.html
```

## Schémas courants

### Base64 + XOR

```python
import base64, json

def decode(encoded, key):
    raw = base64.b64decode(encoded)
    key_bytes = key.encode('utf-8')
    decrypted = bytes([raw[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(raw))])
    return json.loads(decrypted.decode('utf-8'))
```

### Mappage par codes courts (abréviations de composants et de propriétés)

Dans la configuration, `C74`/`p29` remplacent `StudioBackground`/`color`。

```bash
grep -oE '(codeToComponent|codeToProp)' /tmp/bundle.js
```

La table de mappage est en général générée dynamiquement — tous les noms, triés alphabétiquement, se voient attribuer des numéros `C{nn}`/`p{nn}` 

## Sources de la clé

| Framework | Emplacement |
|------|------|
| Nuxt.js | `public:{obfuscationKey:"..."}` in HTML |
| Next.js | `__NEXT_DATA__` — runtimeConfig |
| SPA | bundle constantes ou `window.__CONFIG__` |

## Repérer la fonction de décodage

```bash
grep -l '_encoded' /tmp/*.js
grep -A3 '_encoded' /tmp/bundle.js
# motif : if (t._encoded) { return decode(t.definition, key) }
```
