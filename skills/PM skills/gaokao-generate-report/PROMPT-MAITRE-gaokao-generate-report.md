---
nom: gaokao-generate-report
source: skills/gaokao-generate-report/SKILL.md
sha256_source: 7a7cdfb54e2c
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — gaokao-generate-report (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/gaokao-generate-report/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: gaokao-generate-report
description: >-
  Fusionne les infos du candidat, la liste de vœux, les recommandations de filières et d'établissements, et génère un rapport HTML de candidatures avec analyse fusionnée et liste de vœux triée ambitif/stable/sécurisé (chong-wen-bao).
  Convient à la génération de rapports de vœux gaokao, à la production de plans de candidature et à la visualisation du tableau de vœux.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
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


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
