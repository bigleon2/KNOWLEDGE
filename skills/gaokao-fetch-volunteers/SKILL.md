---
name: gaokao-fetch-volunteers
version: "1.0.0"
category: "Éducation"
tags:
  - gaokao
  - fetch
  - volunteers
description: >-
  Appeler l'API de recommandation intelligente de vœux du Gaokao pour obtenir, à partir des
  informations de base du candidat et de ses préférences de filières/villes/établissements
  (mappées vers les paramètres API optionnels), la liste de vœux répartie en ambitieux/sûrs/de
  repli, puis l'analyser en parsed.json. Convient pour obtenir des établissements recommandés,
  des listes de vœux ambitieux/sûrs/de repli et l'appel de l'API de vœux.
language: fr

read_when:
  - Déclencher quand la demande concerne : >-
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Récupérer la liste de vœux recommandée

Ce skill est la **deuxième étape** du pipeline : il lit `student.json`, **extrait et mappe les préférences du candidat vers les paramètres API optionnels**, appelle l'API de vœux et produit `parsed.json`.

## Amont / aval

- **Amont** : [gaokao-collect-student-info](../gaokao-collect-student-info/SKILL.md) → `student.json`
- **Aval** : [gaokao-recommend-majors](../gaokao-recommend-majors/SKILL.md), [gaokao-recommend-schools](../gaokao-recommend-schools/SKILL.md), [gaokao-generate-report](../gaokao-generate-report/SKILL.md)

## Préparation de l'environnement

```bash
cd gaokao-fetch-volunteers
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Étapes d'exécution

### 1. Extraire les préférences depuis les informations auxiliaires (obligatoire pour l'agent)

Lire `student.json` et, selon [preference_mapping.md](preference_mapping.md), compléter/écrire les préférences du candidat dans les champs suivants :

| Champ | Mappé vers l'API |
|------|-----------|
| `preferred_universities` | `universitys` |
| `preferred_provinces` / `preferred_cities` | `provinces` |
| `preferred_tags` | `tags` |
| `preferred_major_classes` | `majorClass` |

Sources d'extraction : `interests`, `career_direction`, `preferred_cities`, `notes` et les préférences d'établissements/filières/niveaux exprimées dans la conversation.

Si l'étape 1 de la collecte a déjà structuré ces données, se contenter de vérifier et compléter ; **les champs de préférences ne doivent pas être des tableaux vides avant l'appel API** (sauf si le candidat n'a aucune préférence).

### 2. Construire la requête API

```bash
python3 scripts/build_api_request.py \
  -i output/student.json \
  -o output/api_request.json \
  --summary output/preference_summary.json
```

Le script convertit les `preferred_*` en paramètres API optionnels ; `preferred_cities` permet de déduire automatiquement `provinces` (voir `preference_mapping.md`).

`build_api_request.py` appelle `province_config.validate_classify` pour vérifier que `classify` correspond au régime de la province.

### 2.5 Vérification des paramètres avant l'appel (obligatoire)

Avant d'appeler l'API, vérifier `student.json` / `api_request.json` à l'aide de [reference.md](reference.md) :

| Point de contrôle | Règle |
|--------|------|
| `classify` | Xinjiang → `文科`/`理科` ; provinces 3+1+2 → `物理`/`历史` ; provinces 3+3 → `综合`. **Une erreur rend la liste des lots vide** |
| `subjects` | 3+1+2 : **les trois matières complètes** (matière principale + deux secondaires, p. ex. `物理,化学,生物`) ; 3+3 : trois matières complètes ; Xinjiang : ne pas transmettre ; filière courte Pékin/Shanghai/Tianjin gérée par le script |
| `gradeType` | **Uniquement Pékin/Shanghai/Tianjin** : `本科` ou `专科` ; pour toutes les autres provinces : `null` ou ne pas transmettre |
| `score` | Xinjiang : **obligatoire** (pas de table de classement ; le rang seul est invalide) |
| `batch` | On peut saisir une appellation générique telle que `本科批` / `专科批`, résolue par batch/list vers le nom de lot spécifique de chaque province |
| Tibet | Non supporté par l'environnement de test ; renvoyer à l'étape de collecte pour en informer l'utilisateur |

**Lot (batch)** : côté utilisateur on peut saisir l'appellation générique `本科批` / `专科批` ; le script la résout via batch/list vers le nom de lot spécifique de chaque province (p. ex. Shandong → `普通类一段`). En cas d'échec de l'interface, utiliser la table de repli statique de [reference.md](reference.md).

### 3. Appeler l'API de vœux (en deux phases : lots → liste de vœux)

```bash
python3 scripts/fetch_volunteers.py \
  --config output/api_request.json \
  -o output/parsed.json
```

Ou en une seule fois (logique de construction intégrée) :

```bash
python3 scripts/fetch_volunteers.py \
  --student output/student.json \
  -o output/parsed.json
```

Le script appelle d'abord `batch/list` pour résoudre le `batch` et le `volunteerType` précis à partir du score et des matières, puis interroge l'interface de recommandation de vœux. La normalisation des paramètres est faite automatiquement par `scripts/province_config.py`. On peut désactiver la résolution automatique avec `--no-auto-batch`.

**SOP en deux phases** :

```
1. GET  batch/list  →  得到各省可选批次 + volunteerType
2. POST intelligenceVolunteer  →  用选中批次的 batch / volunteerType 拉志愿
```

Pour Pékin/Shanghai/Tianjin, il faut aussi transmettre `gradeType` à l'étape 1 (le script le déduit automatiquement du score / du batch).

### 4. Expliquer à l'utilisateur

En s'appuyant sur `preference_summary.json` et le `stats` de `parsed.json`, expliquer :

- quels paramètres de préférences ont été transmis (établissements/provinces/niveaux/familles de filières)
- combien d'établissements dans chaque catégorie : ambitieux / sûrs / de repli

## Paramètres API optionnels

| Champ API | Signification | Source |
|----------|------|------|
| `universitys` | Établissements convoités | `preferred_universities` |
| `provinces` | Provinces souhaitées | `preferred_provinces` ou déduites des villes |
| `tags` | Attributs d'établissement | `preferred_tags` (985/211, etc.) |
| `majorClass` | Familles de filières souhaitées | `preferred_major_classes` |

Documentation API complète : voir [reference.md](reference.md).

## Structure de sortie (parsed.json)

| Champ | Description |
|------|------|
| `profile` | Contient l'écho des paramètres optionnels transmis |
| `stats` | Nombres d'établissements ambitieux/sûrs/de repli |
| `schools_by_type` | Listes d'établissements groupés |
| `request` | Corps de requête API réel (avec les paramètres de préférences) |
| `batch_resolution` | Source de résolution du lot, choix retenu et options disponibles |

## Dépannage

| Symptôme | Traitement |
|------|------|
| Recommandations non conformes aux préférences | Vérifier que les paramètres optionnels dans `api_request.json` sont corrects |
| Aucun lot disponible pour candidater | Consulter [reference.md](reference.md) ; confirmer que `classify` correspond au régime de la province |
| Liste des lots vide | `classify` erroné (p. ex. `物理` transmis pour une province 3+3) — le script renvoie une erreur explicite |
| Candidats du Tibet | Non supporté par l'environnement de test ; changer de province ou attendre l'intégration de la plateforme |
| Erreur 500 de l'interface de vœux | Consulter reference : `gradeType`/`subjects` correctement transmis selon la province |
| `subjects` manquant | Les matières sont obligatoires en 3+3/3+1+2 ; sauf Xinjiang et filière courte Pékin/Shanghai/Tianjin |
| `subjects` limité à deux matières | En 3+1+2, il faut transmettre **les trois matières complètes** (avec `物理`/`历史`), pas seulement chimie-biologie |
| Préférences non transmises | Confirmer que les champs `preferred_*` ont bien été remplis à l'étape 1/2 |

## Ressources annexes

- [preference_mapping.md](preference_mapping.md) — règles de mappage préférences → paramètres API
- [reference.md](reference.md) — API, régimes de matières, pièges des interfaces de lots : aide-mémoire
- [scripts/province_config.py](scripts/province_config.py) — validation et normalisation de classify/subjects/gradeType par province
- [scripts/test_batch_api.py](scripts/test_batch_api.py) — tests de régression de l'interface des lots pour 31 provinces
- [examples/api_request_shandong.json](examples/api_request_shandong.json) — exemple avec paramètres optionnels
