---
name: aminer-deep-search
version: 2.0.0
author: AMiner
contact: report@aminer.cn
description: >
  Activer ce skill quand l'utilisateur doit collecter des publications académiques en profondeur et en plusieurs tours pour une revue de littérature.
  Le modèle hôte (celui qui exécute ce skill) pilote lui-même la boucle : étendre les requêtes, juger la pertinence, faire rouler la boule de neige des citations, décider quand s'arrêter.
  Les scripts fournis sont de pures commandes-outils : ils appellent les interfaces officielles de la plateforme ouverte AMiner et ne produisent qu'un tool-result JSON, sans configuration d'aucun LLM supplémentaire.
  Adapté à l'exploration large de sujets, à la construction de bibliographies de revue, à la collecte de centaines de candidats dotés d'ID AMiner et de titres.
  Inadapté à la requête sur une publication isolée ou aux recommandations légères — utiliser respectivement aminer-free-academic ou aminer-daily-paper.
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
---

# Collecte approfondie AMiner

Collecte bibliographique de revue pilotée directement par le modèle hôte. Toi (le modèle qui lit ce document) es le contrôleur : exécuter les scripts-outils, lire les sorties JSON, juger soi-même la pertinence, itérer jusqu'à l'objectif de collecte.

## Périmètre d'application

- Adapté : collecte bibliographique de niveau revue (centaines de publications), expansion de mots-clés, boule de neige de citations rétrogrades.
- Inadapté : requête ou question-answer sur une publication isolée (via `aminer-free-academic`), recommandation personnalisée (via `aminer-daily-paper`).

## Pre-flight

1. Vérifier la clé (sans imprimer sa valeur) :

```bash
[ -z "${AMINER_API_KEY:-}" ] && echo "AMINER_API_KEY missing" || echo "AMINER_API_KEY exists"
```

Si absente, s'arrêter et faire définir `AMINER_API_KEY` par l'utilisateur (console : https://open.aminer.cn/open/board?tab=control). Ne jamais imprimer la clé.

2. Confirmer `topic` et `target-size` (défaut 400). Si le plan de tours prévoit un coût ≥¥5, en informer l'utilisateur et obtenir son accord avant de commencer.

## Outils

Les deux scripts sont dans `scripts/` du répertoire de ce skill. stdout ne produit qu'un document JSON (le tool-result) ; les diagnostics et les lignes de coût `[cost]` vont sur stderr. Les scripts ne font aucun scoring de pertinence — c'est ton travail.

### `scripts/aminer_api.py` — appels aux interfaces AMiner

| Sous-commande | Point d'entrée | Prix |
|---|---|---|
| `search --query Q [--size 20] [--year YYYY] [--order n_citation\|year] [--max-pages 3]` | GET `/api/paper/search/pro` + complétion gratuite `paper/info` | ¥0.01/page |
| `qa-search [--query "question en langage naturel"] [--topic-high '[["motA","motB"],["motC"]]'] [--size 20] [--year-from Y] [--year-to Y] [--citation-sort]` | POST `/api/paper/qa/search` (`use_topic=true` fixé : quand `use_topic=false` le backend ignore `query`) + complétion gratuite | ¥0.05/appel |
| `info --ids id1 id2 ...` | POST `/api/paper/info` (par lots de ≤100 id) | gratuit |
| `references --ids id1 id2 ... [--per-seed 20]` | GET `/api/paper/relation` par seed + complétion gratuite | ¥0.10/seed |

Forme de sortie : `search`/`qa-search`/`info` produisent `[{id, title, year?, venue?, abstract_slice?}]` ; `references` ajoute `source_paper_ids` (quels seeds citent la publication) et exclut les seeds eux-mêmes des résultats.

### `scripts/paper_set.py` — fichier d'état inter-tours (sans réseau)

Le fichier d'état par défaut est `outputs/paper_set.json` dans le répertoire de travail.

```bash
# Piper les résultats conservés (directement après une recherche), dédupliqués par id
python3 scripts/aminer_api.py search --query "..." | python3 scripts/paper_set.py add
# → {"added": N, "duplicates": M, "total": T}

python3 scripts/paper_set.py stats     # total, expanded_seeds, distribution par année
python3 scripts/paper_set.py mark-expanded --ids id1 id2   # consigner les seeds déjà déroulés
python3 scripts/paper_set.py export -o outputs/final_papers.json
```

`add` accepte aussi `--ids id1 id2 ...` pour ajouter des id bruts. Les entrées portant `source_paper_ids` (issues de `references`) marquent automatiquement les seeds correspondants comme étendus.

Pour filtrer avant d'ajouter au corpus : lire d'abord la sortie de recherche, puis piper uniquement les entrées conservées :

```bash
printf '%s' '[{"id":"...","title":"..."}]' | python3 scripts/paper_set.py add
```

## Protocole par tour (cœur du skill)

### Tour 0 — planification

- Dériver du topic 4–8 requêtes semences : synonymes, sous-domaines, noms de méthodes, jeux de données/benchmarks, abréviations anglaises usuelles.
- Estimer le nombre de tours et le coût (recherche ≈ ¥0.01–0.05/appel, references ≈ ¥0.10/seed). Si l'estimation ≥¥5, faire confirmer par l'utilisateur d'abord.

### Chaque tour (12 tours maximum par défaut), cinq étapes fixes

1. **Chercher** : exécuter 1–4 `search` / `qa-search` sur la file à traiter. Privilégier `search` (moins cher) ; utiliser `qa-search` quand la requête est une question en langage naturel.
2. **Filtrer et verser** : lire les résultats stdout, juger soi-même la pertinence pour le thème, piper uniquement les entrées conservées vers `paper_set.py add`. Ne jamais verser une publication jugée hors sujet.
3. **Voir la progression** : lancer `stats` pour le total et l'accroissement du tour.
4. **Boule de neige** : parmi les publications pertinentes ajoutées ce tour, choisir ≤5 seeds forts (forte pertinence, bien classés par `--order n_citation`, absents des `expanded_seeds`), lancer `references --ids ...`. Refiltrer la sortie par pertinence puis la verser. Les seeds sans production versable sont consignés via `mark-expanded`.
5. **Décider du tour suivant** :
   - une recherche donne <5 résultats ou de mauvais résultats → changer pour une requête reformulée (au plus 2 variantes par direction, puis basculer sur la boule de neige) ;
   - references produit continuellement beaucoup de publications pertinentes → continuer la boule de neige depuis les nouveaux seeds ;
   - `target-size` atteint, résultats épuisés, ou 2 tours consécutifs avec <5 ajouts → terminer.

### Clôture

Lancer `export`, puis rapporter : nombre final de publications, coût total (somme des lignes `[cost]` de stderr), chemin du fichier de sortie.

## Règles

1. Ne jamais inventer d'ID ou de titre de publication ; ne citer que les données réellement renvoyées par les outils.
2. Priorité au gratuit : les métadonnées viennent toujours du `paper/info` gratuit (déjà intégré aux scripts) ; jamais d'appel au `paper/detail` payant pour des métadonnées en masse.
3. Ne pas fourrer les sorties brutes des outils dans la réponse finale ; ne rapporter que les comptages et le chemin du fichier exporté.
4. Ne jamais imprimer ni consigner `AMINER_API_KEY`.
5. Si AMiner renvoie moins de publications que la cible, rapporter honnêtement le nombre réel, sans invention.
