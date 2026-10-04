---
name: aminer-deep-search
category: "Finance & Recherche"
tags:
  - aminer
  - deep
  - search
version: 2.0.1
category: "Finance & Recherche"
tags:
  - aminer
  - deep
  - search
author: AMiner
contact: report@aminer.cn
description: >
  Activez ce skill lorsque l'utilisateur veut une collecte approfondie et multi-passes d'articles académiques pour un état de l'art ou une revue de littérature.
  Le modèle hôte (le modèle qui exécute ce skill) pilote lui-même la boucle : il étend les requêtes, juge la pertinence, fait du « snowballing » sur les références en amont et décide quand s'arrêter.
  Les scripts fournis sont de purs outils en ligne de commande qui appellent les endpoints documentés de la plateforme ouverte AMiner et n'impriment que des résultats JSON d'outils — aucune configuration LLM supplémentaire n'est nécessaire.
  Utilisez ce skill pour l'exploration large d'un sujet, la constitution d'une bibliographie d'état de l'art, et la collecte de centaines d'articles candidats avec leurs identifiants et titres AMiner.
  Non adapté à la recherche d'un article unique ou à des recommandations légères ; utilisez aminer-free-academic ou aminer-daily-paper pour cela.
language: fr
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["python3"],
          "env": ["AMINER_API_KEY"]
        },
        "primaryEnv": "AMINER_API_KEY"
      }
  }

read_when:
  - Déclencher quand la demande concerne : activez ce skill lorsque l'utilisateur veut une collecte approfondie et multi-passes d'articles académiques po…
  - Déclencher si la demande mentionne : aminer, skill, collecte
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# AMiner Deep Search

Collecte d'articles pour état de l'art pilotée par le modèle hôte. Vous (le modèle qui lit ceci) êtes le contrôleur : exécutez les scripts outils, lisez leur sortie JSON, jugez vous-même la pertinence et itérez jusqu'à atteindre l'objectif de collecte.

## Périmètre

- À utiliser pour : la constitution d'une bibliographie d'état de l'art (des centaines d'articles), l'expansion de mots-clés, le snowballing de citations en amont.
- Ne pas utiliser pour : la recherche d'un article unique ou du Q&A (routez vers `aminer-free-academic`), les recommandations personnalisées (routez vers `aminer-daily-paper`).

## Pré-vol

1. Vérifiez la clé sans l'afficher :

```bash
[ -z "${AMINER_API_KEY:-}" ] && echo "AMINER_API_KEY missing" || echo "AMINER_API_KEY exists"
```

Si absent, arrêtez-vous et demandez à l'utilisateur de définir `AMINER_API_KEY` (console : https://open.aminer.cn/open/board?tab=control). N'affichez jamais la clé.

2. Confirmez le `topic` et le `target-size` (défaut 400). Si votre plan de passes est estimé à 5 ¥ ou plus, donnez l'estimation à l'utilisateur et obtenez sa confirmation avant de démarrer.

## Outils

Les deux scripts vivent dans `scripts/` sous le répertoire de ce skill. Ils impriment exactement un document JSON sur stdout (le résultat de l'outil) ; les diagnostics et une ligne `[cost]` vont sur stderr. Ils n'évaluent jamais la pertinence — c'est votre travail.

### `scripts/aminer_api.py` — appels API AMiner

| Sous-commande | Endpoint | Prix |
|---|---|---|
| `search --query Q [--size 20] [--year YYYY] [--order n_citation\|year] [--max-pages 3]` | GET `/api/paper/search/pro` + enrichissement gratuit `paper/info` | ¥0.01/page |
| `qa-search [--query "natural language question"] [--topic-high '[["termA","termB"],["termC"]]'] [--size 20] [--year-from Y] [--year-to Y] [--citation-sort]` | POST `/api/paper/qa/search` (toujours `use_topic=true` ; le backend ignore `query` quand `use_topic=false`) + enrichissement gratuit | ¥0.05/appel |
| `info --ids id1 id2 ...` | POST `/api/paper/info` (par lots ≤100 ids) | Gratuit |
| `references --ids id1 id2 ... [--per-seed 20]` | GET `/api/paper/relation` par graine + enrichissement gratuit | ¥0.10/graine |

Forme de la sortie : `search`/`qa-search`/`info` impriment `[{id, title, year?, venue?, abstract_slice?}]` ; `references` inclut en plus `source_paper_ids` (les graines qui ont cité l'article). Les graines elles-mêmes sont exclues de la sortie de `references`.

### `scripts/paper_set.py` — fichier d'état inter-passes (sans réseau)

Fichier d'état par défaut : `outputs/paper_set.json`, relatif au répertoire de travail.

```bash
# Merge kept results (pipe the filtered JSON array in), dedupe by id
python3 scripts/aminer_api.py search --query "..." | python3 scripts/paper_set.py add
# → {"added": N, "duplicates": M, "total": T}

python3 scripts/paper_set.py stats     # totals, expanded_seeds, by_year
python3 scripts/paper_set.py mark-expanded --ids id1 id2   # record snowballed seeds
python3 scripts/paper_set.py export -o outputs/final_papers.json
```

`add` accepte aussi `--ids id1 id2 ...` pour des IDs nus. Les éléments portant `source_paper_ids` (issus de `references`) marquent automatiquement ces graines comme étendues.

Si vous voulez filtrer avant d'ajouter, lisez d'abord la sortie de recherche, puis ne redirigez que les éléments conservés :

```bash
printf '%s' '[{"id":"...","title":"..."}]' | python3 scripts/paper_set.py add
```

## Protocole de passe (cœur)

### Passe 0 — plan

- Dérivez 4 à 8 requêtes graines du sujet : synonymes, sous-domaines, noms de méthodes, jeux de données/benchmarks, abréviations anglaises courantes.
- Estimez le nombre de passes et le coût (recherches ≈ 0,01–0,05 ¥ chacune, références ≈ 0,10 ¥/graine). Si l'estimation est ≥ 5 ¥, obtenez d'abord la confirmation de l'utilisateur.

### Chaque passe (budget par défaut : 12 passes), cinq étapes fixes

1. **Rechercher** : exécutez 1 à 4 appels `search` / `qa-search` depuis la file de requêtes en attente. Privilégiez `search` (moins cher) ; utilisez `qa-search` quand la requête est une question en langage naturel.
2. **Filtrer et ajouter** : lisez les résultats de stdout, jugez vous-même la pertinence par rapport au sujet et ne redirigez que les éléments conservés vers `paper_set.py add`. N'ajoutez jamais d'articles que vous jugez hors sujet.
3. **Vérifier** : lancez `stats` pour voir le total et l'incrément de la passe.
4. **Snowball** : parmi les ajouts pertinents de cette passe, choisissez ≤5 graines fortes (très pertinentes, bien classées avec `--order n_citation`, absentes de `expanded_seeds`) et lancez `references --ids ...`. Filtrez la sortie pour la pertinence, puis ajoutez-la. Lancez `mark-expanded` pour les graines qui n'ont rien donné d'ajoutable.
5. **Décider** : choisissez le mouvement suivant —
   - une recherche a renvoyé <5 résultats ou des résultats de mauvaise qualité → remplacez-la par une requête reformulée (max 2 variantes par direction, puis passez au snowballing) ;
   - les références donnent beaucoup d'articles pertinents → continuez le snowballing à partir de nouvelles graines ;
   - `target-size` atteint, ou résultats épuisés, ou 2 passes consécutives avec <5 articles ajoutés → terminer.

### Conclusion

Lancez `export`, puis rapportez : le nombre final d'articles, le coût total (sommez les lignes `[cost]` de stderr) et le chemin du fichier de sortie.

## Règles

1. Ne fabriquez jamais d'IDs ni de titres d'articles ; ne citez que des données réellement renvoyées par les outils.
2. Gratuit d'abord : les métadonnées viennent toujours du `paper/info` gratuit (les scripts le font déjà) ; n'appelez jamais le `paper/detail` payant pour des métadonnées en masse.
3. Gardez la sortie brute des outils hors de votre réponse finale ; rapportez plutôt les compteurs et le chemin du fichier exporté.
4. N'imprimez et ne journalisez jamais `AMINER_API_KEY`.
5. Si AMiner renvoie moins d'articles que la cible, rapportez le nombre réel au lieu d'inventer des articles.
