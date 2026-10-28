---
nom: gaokao-fetch-volunteers
source: skills/gaokao-fetch-volunteers/SKILL.md
sha256_source: bb1a925f1bd4
genere: 2026-10-28 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — gaokao-fetch-volunteers (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/gaokao-fetch-volunteers/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: gaokao-fetch-volunteers
description: >-
  Appelle l'API intelligente de recommandation des vœux du gaokao : à partir des informations
  du candidat et de ses préférences en filières/villes/établissements (mappées vers les
  paramètres optionnels de l'API), récupère la liste de vœux chong/wen/bao (ambitieux/sûrs/de
  sécurité) et la parse en `parsed.json`. À utiliser pour obtenir les établissements
  recommandés, le tableau de vœux chong/wen/bao ou l'appel de l'API des vœux.
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Obtenir le tableau de vœux recommandés

Ce skill est la **deuxième étape** du pipeline : il lit `student.json`, **extrait et mappe les préférences du candidat vers les paramètres optionnels de l'API**, appelle l'API des vœux et produit `parsed.json`.

## Amont / aval

- **Amont** : [gaokao-collect-student-info](../gaokao-collect-student-info/SKILL.md) → `student.json`
- **Aval** : [gaokao-recommend-majors](../gaokao-recommend-majors/SKILL.md), [gaokao-recommend-schools](../gaokao-recommend-schools/SKILL.md), [gaokao-generate-report](../gaokao-generate-report/SKILL.md)

## Préparation de l'environnement (Huanjing zhunbei)

```bash
cd gaokao-fetch-volunteers
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Étapes d'exécution

### 1. Extraire les préférences des informations auxiliaires (obligatoire pour l'agent)

Lire `student.json` et compléter/écrire les préférences du candidat dans les champs suivants selon [preference_mapping.md](preference_mapping.md) :

| Champ | Mappé vers l'API |
|------|-----------|
| `preferred_universities` | `universitys` |
| `preferred_provinces` / `preferred_cities` | `provinces` |
| `preferred_tags` | `tags` |
| `preferred_major_classes` | `majorClass` |

Sources de l'extraction : `interests`, `career_direction`, `preferred_cities`, `notes` ainsi que les préférences d'établissements/filières/niveau exprimées dans la conversation.

Si l'étape 1 a déjà structuré et écrit ces champs, cette étape vérifie et complète ; **les champs requis avant l'appel API ne doivent pas être un tableau vide** (sauf si le candidat n'a aucune préférence).

### 2. Construire la requête API

```bash
python3 scripts/build_api_request.py \
  -i output/student.json \
  -o output/api_request.json \
  --summary output/preference_summary.json
```

Le script convertit les `preferred_*` en paramètres optionnels de l'API ; `preferred_cities` déduit automatiquement `provinces` (voir `preference_mapping.md`).

`build_api_request.py` appelle `province_config.validate_classify` pour vérifier que `classify` correspond bien au mode de la province.

### 2.5 Vérification des paramètres avant l'appel (obligatoire)

Avant d'appeler l'API, consulter [reference.md](reference.md) pour vérifier `student.json` / `api_request.json` :

| Point de contrôle | Règle |
|--------|------|
| `classify` | Xinjiang (Xinjiang) → `文科` (littéraire) / `理科` (scientifique) ; provinces 3+1+2 → `物理` (physique) / `历史` (histoire) ; provinces 3+3 → `综合` (général). **Une erreur de classify conduit à une liste de lots vide** |
| `subjects` | 3+1+2 : **les trois matières complètes** (choix principal + deux choix secondaires, ex. `物理,化学,生物`) ; 3+3 : trois matières complètes ; Xinjiang : ne pas transmettre ; filières courtées Pékin/Shanghai/Tianjin : géré par le script |
| `gradeType` | **Pékin/Shanghai/Tianjin uniquement** : renseigner `本科` (licence) ou `专科` (filière courte) ; les autres provinces doivent laisser `null` ou ne rien transmettre |
| `score` | Xinjiang : **obligatoire** (pas de table un-point-un-rang, le rang seul est inutilisable) |
| `batch` | Accepte les libellés génériques « 本科批 » (lot licence) / « 专科批 » (lot filière courte), résolus par batch/list en noms de lots spécifiques par province |
| Tibet (西藏) | Non pris en charge par l'environnement de test ; retourner à l'étape de collecte pour l'expliquer |

**Lot (batch)** : côté utilisateur, on peut saisir le libellé générique `Benke pi` (本科批) / `Zhuanke pi` (专科批) ; le script le résout via batch/list en nom de lot spécifique de la province (ex. Shandong → `Putong lei yi duan` (普通类一段)). En cas d'échec de l'interface, utiliser la table statique de repli de [reference.md](reference.md).

### 3. Appeler l'API des vœux (deux phases : lots → liste de vœux)

```bash
python3 scripts/fetch_volunteers.py \
  --config output/api_request.json \
  -o output/parsed.json
```

Ou tout en une étape (logique de construction intégrée) :

```bash
python3 scripts/fetch_volunteers.py \
  --student output/student.json \
  -o output/parsed.json
```

Le script appelle d'abord `batch/list` pour résoudre le `batch` et le `volunteerType` concrets à partir du score et des matières choisies, puis interroge l'API de recommandation des vœux. La normalisation des paramètres est effectuée automatiquement par `scripts/province_config.py`. L'option `--no-auto-batch` désactive la résolution automatique.

**SOP en deux phases** :

```
1. GET  batch/list  →  obtenir les lots disponibles par province + volunteerType
2. POST intelligenceVolunteer  →  récupérer les vœux avec le batch / volunteerType choisis
```

Pour Pékin/Shanghai/Tianjin, l'étape 1 doit aussi transmettre `gradeType` (inféré automatiquement par le script selon score / batch).

### 4. Expliquer à l'utilisateur

En combinant `preference_summary.json` et le champ `stats` de `parsed.json`, expliquer :

- Quels paramètres de préférence ont été transmis (établissements/provinces/niveau/classes de filières)
- Combien d'établissements en chong/wen/bao (ambitieux/sûrs/sécurité)

## Description des paramètres optionnels de l'API

| Champ API | Signification | Source |
|----------|------|------|
| `universitys` | Établissements souhaités | `preferred_universities` |
| `provinces` | Préférence de province | `preferred_provinces` ou déduit des villes |
| `tags` | Attributs d'établissement | `preferred_tags` (985/211, etc.) |
| `majorClass` | Classes de filières souhaitées | `preferred_major_classes` |

Documentation API complète dans [reference.md](reference.md).

## Structure de sortie (parsed.json)

| Champ | Description |
|------|------|
| `profile` | Rejoue les paramètres optionnels transmis |
| `stats` | Comptages chong/wen/bao |
| `schools_by_type` | Liste des établissements groupés |
| `request` | Corps de requête API réel (paramètres de préférence inclus) |
| `batch_resolution` | Source de résolution du lot, choix retenu et options disponibles |

## Dépannage

| Symptôme | Traitement |
|------|------|
| Résultats incohérents avec les préférences | Vérifier que les paramètres optionnels de `api_request.json` sont corrects |
| Aucun lot disponible | Consulter [reference.md](reference.md) ; confirmer que classify correspond au mode de la province |
| Liste de lots vide | classify erroné (ex. `Wùlǐ` transmis pour une province 3+3) — le script le signale explicitement |
| Candidat du Tibet | Non pris en charge par l'environnement de test ; changer de province ou attendre l'intégration par la plateforme |
| API des vœux en erreur 500 | Vérifier dans reference : gradeType/subjects transmis selon les règles de la province |
| `subjects` manquant | Obligatoire pour 3+3/3+1+2 ; exceptions : Xinjiang / filières courtées Pékin-Shanghai-Tianjin |
| `subjects` avec seulement deux matières | 3+1+2 exige **les trois matières complètes** (y compris 物理/histoire) — ne pas transmettre seulement 化学,生物 |
| Préférences non transmises | Confirmer que l'étape 1 / cette étape a bien rempli les champs `preferred_*` |

## Ressources complémentaires

- [preference_mapping.md](preference_mapping.md) — règles de mapping préférences → paramètres API
- [reference.md](reference.md) — mémo API, modes de sélection des matières, pièges de l'API des lots
- [scripts/province_config.py](scripts/province_config.py) — validation et normalisation classify/subjects/gradeType par province
- [scripts/test_batch_api.py](scripts/test_batch_api.py) — tests de régression de l'API des lots pour les 31 provinces
- [examples/api_request_shandong.json](examples/api_request_shandong.json) — exemple avec paramètres optionnels


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
