---
name: gaokao-generate-report
description: >-
  Fusionne les infos du candidat, la liste de vœux, les recommandations de filières et d'établissements, et génère un rapport HTML de candidatures avec analyse fusionnée et liste de vœux triée ambitif/stable/sécurisé (chong-wen-bao).
  Convient à la génération de rapports de vœux gaokao, à la production de plans de candidature et à la visualisation du tableau de vœux.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Générer le rapport de candidatures

Cette skill est la **cinquième étape**：du pipeline : fusionner les JSON amont et rendre le rapport HTML.

## Amont et aval

- **Amont**：
  - `parsed.json`（liste de vœux）
  - `major_recommendation.json`（recommandations de filières）
  - `school_recommendation.json`（recommandations d'établissements）
- **Sortie**：`volunteer_report.html`

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

`merge_analysis.py` fusionne les recommandations de filières et d'établissements en la structure requise par `generate_html.py` `analysis.json` 

### 2. Générer le HTML

```bash
python3 scripts/generate_html.py \
  -i output/parsed.json \
  -a output/analysis.json \
  -o output/volunteer_report.html
```

### 3. Livrer à l'utilisateur

Fournir `volunteer_report.html` — **chemin absolu**，, et expliquer brièvement la structure du rapport :

1. **Évaluation globale et conseils**（orientation filière + stratégie d'établissements）
2. **Liste de vœux recommandés**（冲/稳/保，⭐ école recommandée / 🔥 filière recommandée cliquable pour les détails）

## Contrôles avant fusion

| Point de contrôle | Description |
|--------|------|
| Champs filière cohérents | `recommended_majors` : name/code conforme à `parsed.json` |
| Champs établissement cohérents | `recommended_schools` : name/code conforme à `parsed.json` |
| Textes complets | `intro`、`strategy`、`school_strategy` non vides |

Si des champs recommandés ne correspondent pas avant la fusion, revenir à la skill correspondante pour corriger le JSON.

## Ressources complémentaires

- [examples/analysis_merged_example.json](examples/analysis_merged_example.json) — exemple de structure complète après fusion
