---
name: image-search
category: "IA & Media"
tags:
  - image
  - search
version: 1.0.1
category: "IA & Media"
tags:
  - image
  - search
description: |
  Service de recherche d'images maison de ZAI, exposé via le CLI du z-ai-web-dev-sdk.
  Récupère de vraies images du web pour n'importe quelle requête textuelle, avec des
  légendes courtes en option, et renvoie des URLs directes hébergées sur OSS garanties
  accessibles. À utiliser quand l'utilisateur veut trouver, récupérer, illustrer ou
  intégrer des images — p. ex. « cherche des images de X », « trouve une photo de Y »,
  « il me faut une couverture pour Z », « donne-moi des photos de référence de W »,
  "插图", "配图", "找图", "找张图",
  "搜张图", "搜图".
language: fr

---

# image-search (service maison ZAI, via le SDK z-ai)

Recherche des images du web public pour une requête en langage naturel, réhéberge chaque résultat sur OSS pour que le lien soit intégrable, et (optionnellement) joint une légende courte. Le backend est le **service de recherche d'images développé en propre par ZAI**.

Vous **n'appelez pas le backend directement**, et vous **n'appelez pas directement l'API HTTP de la passerelle**. Passez toujours par la sous-commande `z-ai image-search` du CLI `z-ai-web-dev-sdk` — c'est le seul point d'entrée supporté.

## Quand activer

Déclenchez ce skill quand l'utilisateur veut :

- Trouver des images pour un article, un diaporama, un PPT, un billet de blog ou un rapport.
- Obtenir des photos de référence / de l'inspiration sur un sujet.
- Intégrer des images dans des documents générés avec des URLs stables.
- Légendrer un lot d'images en chinois ou en anglais.

**N'utilisez pas** ce skill pour :

- Générer de nouvelles images à partir de zéro — utilisez `z-ai image` (génération d'images).
- La recherche d'image inversée (« qu'est-ce que cette image ? »).
- Rechercher des images dans un corpus privé — ce skill interroge des sources web publiques.

## Prérequis

**`z-ai-web-dev-sdk` installé**, fournissant le binaire `z-ai` :

```bash
npm install -g z-ai-web-dev-sdk
# or:  bun add -g z-ai-web-dev-sdk
```

## Invocation

```bash
z-ai image-search --query "<natural-language sentence>" [flags]
```

Le CLI imprime la réponse JSON (mise en forme) sur stdout, ou l'écrit dans `--output <path>` si fourni.

### Options

| Option              | Défaut  | Notes |
|---------------------|---------|-------|
| `--query`, `-q`     | —       | Obligatoire. Phrase en langage naturel décrivant ce que l'image doit contenir. Préférer un concept cohérent unique ; éviter de mélanger des mots-clés sans rapport. |
| `--count`, `-c`     | 5       | Nombre d'images à renvoyer. Plage 1–20. |
| `--gl`              | `cn`    | Code de région pour la localisation. Courants : `cn`, `us`, `jp`, `kr`. |
| `--no-rank`         | —       | Désactive les légendes pour une réponse plus rapide, sans légendes (activé par défaut). |
| `--output`, `-o`    | —       | Optionnel : écrit la réponse JSON complète dans ce chemin. |
| `--help`, `-h`      | —       | Affiche l'aide du CLI. |

### Exemples

```bash
# Default search (5 images, cn region, captions on).
z-ai image-search -q "a cute orange tabby kitten playing with yarn" --count 5

# US region, no captioning (faster).
z-ai image-search -q "vintage red sports car on a mountain road" --count 5 --gl us --no-rank

# Chinese query — captions come back in Chinese.
z-ai image-search -q "中国传统水墨山水画" --count 5 -o results.json
```

## Choisir les paramètres

- **`--query`** : utiliser une phrase descriptive, pas une liste de mots-clés. Le service
  est optimisé pour le langage naturel et renvoie des résultats plus pertinents ainsi.
  Adapter la langue à l'audience : les requêtes chinoises produisent des légendes
  chinoises, les requêtes anglaises des légendes anglaises.
- **`--count`** : rester à `5` par défaut pour la plupart des tâches de collecte d'assets.
  Descendre à `1`–`3` quand l'utilisateur n'a besoin que d'un choix final ; monter vers
  `10`–`20` pour construire un moodboard ou explorer des options. Rester dans `1`–`20`.
- **`--no-rank`** : couper les légendes pour les moodboards ou quand la latence compte ;
  les laisser activées quand l'utilisateur choisira les images en lisant les légendes.
- **Un concept par appel** : pour deux sujets sans rapport, lancer deux invocations
  distinctes plutôt que de concaténer des mots-clés.

## Forme de la réponse

```json
{
  "success": true,
  "query": "cute orange tabby kitten",
  "count": 5,
  "ranked": true,
  "results": [
    {
      "original_url": "https://sfile.chatglm.cn/images-ppt/<hash>.png",
      "caption": "A cute orange tabby kitten playing with yarn on a rug.",
      "source": "Unsplash",
      "original_width": "750px",
      "original_height": "500px"
    }
  ]
}
```

Réponse d'échec (le HTTP reste 200 ; vérifier `success`) :

```json
{
  "success": false,
  "query": "...",
  "count": 0,
  "ranked": true,
  "results": [],
  "error": "<human-readable reason>"
}
```

### Référence des champs

| Champ                       | Type    | Notes |
|-----------------------------|---------|-------|
| `success`                   | boolean | Toujours le vérifier avant de lire `results`. |
| `query`                     | string  | Écho de la requête d'entrée. |
| `count`                     | integer | Nombre d'images effectivement renvoyées. |
| `ranked`                    | boolean | Indique si les légendes ont été appliquées. |
| `results[].original_url`    | string  | URL directe de l'image hébergée sur OSS. Stable et intégrable. |
| `results[].caption`         | string  | Légende courte. Présente uniquement quand `ranked` est `true`. |
| `results[].source`          | string  | Site source d'origine (p. ex. `Unsplash`, `Pinterest`). |
| `results[].original_width`  | string  | Largeur de l'image sous la forme `"NNNpx"`. |
| `results[].original_height` | string  | Hauteur de l'image sous la forme `"NNNpx"`. |
| `error`                     | string  | Présent uniquement en cas d'échec. |

## Conseils opérationnels

1. **Toujours présenter l'`original_url` OSS, pas l'URL du site source.** Le lien OSS
   est celui garanti accessible ; les pages sources peuvent être derrière un paywall,
   bloquées géographiquement ou supprimées.
2. **Couper les légendes pour la vitesse.** `--no-rank` réduit généralement le temps de
   réponse de plus de moitié. À utiliser quand vous légenderez vous-même les résultats.
3. **Être patient avec les timeouts.** Un appel complet peut prendre 90 secondes ou plus —
   l'amont enchaîne sondes d'accessibilité des images, upload OSS et légendage. Prévoir
   un timeout côté client d'au moins 120 secondes.
4. **La région compte.** `gl=cn` favorise les sources en langue chinoise ;
   `gl=us` les sources anglaises. Choisir celle qui correspond à l'audience de l'utilisateur.

## Gestion des erreurs

| Symptôme | Cause probable | Que faire |
|---------|--------------|------------|
| `Unknown command "image-search"` | SDK trop ancien | Mettre à jour : `npm install -g z-ai-web-dev-sdk@latest`. |
| `API request failed with status 401` / `403` | Problème d'authentification à la passerelle | En informer l'utilisateur — les identifiants sont gérés en dehors de ce skill. |
| `API request failed with status 502` | Service amont inaccessible | Réessayer ; si cela persiste, le service maison est hors service. |
| `results` vide mais `success: true` | Requête trop étroite ou l'amont a tout filtré | Élargir la requête, augmenter `--count` ou changer `--gl`. |
