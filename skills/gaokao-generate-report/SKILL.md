---
name: gaokao-generate-report
version: "1.0.0"
category: "Éducation"
tags:
  - gaokao
  - generate
  - report
description: >-
  Fusionner les informations du candidat, la liste de vœux, les recommandations de filières et
  d'établissements pour générer un rapport HTML de remplissage des vœux avec analyse intégrée et
  liste de vœux ambitieux/sûrs/de repli. Convient pour la génération de rapports Gaokao, la
  production de scénarios de candidature et la visualisation de la liste de vœux.
language: fr

read_when:
  - Déclencher quand la demande concerne : >-
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Générer le rapport de remplissage des vœux

Ce skill est la **cinquième étape** du pipeline : fusionner les JSON précédents et rendre un rapport HTML.

## Amont / aval

- **Amont** :
  - `parsed.json` (liste de vœux)
  - `major_recommendation.json` (recommandations de filières)
  - `school_recommendation.json` (recommandations d'établissements)
- **Sortie** : `volunteer_report.html`

## Préparation de l'environnement

```bash
cd gaokao-generate-report
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Étapes d'exécution

### 1. Fusionner en analysis.json

```bash
python3 scripts/merge_analysis.py \
  --majors output/major_recommendation.json \
  --schools output/school_recommendation.json \
  -o output/analysis.json
```

`merge_analysis.py` fusionne les recommandations de filières et d'établissements dans la structure `analysis.json` attendue par `generate_html.py`.

### 2. Générer le HTML

```bash
python3 scripts/generate_html.py \
  -i output/parsed.json \
  -a output/analysis.json \
  -o output/volunteer_report.html
```

### 3. Livrer à l'utilisateur

Fournir le **chemin absolu** de `volunteer_report.html` et expliquer brièvement la structure du rapport :

1. **Bilan global et conseils** (orientations de filières + stratégie d'établissements)
2. **Liste de vœux recommandés** (ambitieux/sûrs/de repli, ⭐ établissements recommandés / 🔥 filières recommandées cliquables pour voir le détail)

## Contrôles avant fusion

| Point de contrôle | Description |
|--------|------|
| Cohérence des champs de filières | Le name/code de `recommended_majors` doit correspondre à `parsed.json` |
| Cohérence des champs d'établissements | Le name/code de `recommended_schools` doit correspondre à `parsed.json` |
| Textes complets | `intro`, `strategy`, `school_strategy` non vides |

Si des champs de recommandation ne correspondent pas avant la fusion, revenir au skill concerné pour corriger le JSON.

## Ressources annexes

- [examples/analysis_merged_example.json](examples/analysis_merged_example.json) — exemple de structure complète après fusion
