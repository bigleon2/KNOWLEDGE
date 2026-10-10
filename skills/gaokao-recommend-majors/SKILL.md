---
name: gaokao-recommend-majors
version: "1.0.0"
category: "Éducation"
tags:
  - gaokao
  - recommend
  - majors
description: >-
  À partir du profil du candidat et de la liste de vœux de l'API, l'agent analyse et recommande
  les orientations de filières, les débouchés professionnels et une liste de filières précises,
  et produit un major_recommendation.json structuré. Convient pour la recommandation de filières
  du Gaokao, le choix de spécialité et l'analyse des débouchés professionnels.
language: fr

read_when:
  - Déclencher quand la demande concerne : >-
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Recommander les filières et les débouchés professionnels

Ce skill est la **troisième étape** du pipeline : analyse purement agent, sans script de règles. Il croise les centres d'intérêt, les notes, les intentions professionnelles du candidat et les filières réelles de `parsed.json` pour produire des recommandations de filières personnalisées.

## Amont / aval

- **Amont** : `student.json` + `parsed.json` (issus de la collecte d'informations et de la récupération des vœux)
- **Aval** : [gaokao-recommend-schools](../gaokao-recommend-schools/SKILL.md) lit `major_recommendation.json`

## Entrées

1. `student.json` — profil complet du candidat
2. `parsed.json` — vœux ambitieux/sûrs/de repli et `majors` de chaque établissement (avec les exigences de matières `claim` et les probabilités d'admission)

## Tâches d'analyse de l'agent

1. Lire [career_reference.md](career_reference.md) pour connaître les grandes familles de filières et leurs débouchés (**à titre de référence, pas de règle absolue**).
2. Croiser les exigences de matières, les notes par matière, les centres d'intérêt, la situation familiale et l'orientation professionnelle pour déterminer 2 à 4 **orientations de filières** (`major_directions`).
3. Sélectionner dans `parsed.json` **8 à 15** filières précises les plus pertinentes et les écrire dans `recommended_majors`.
4. Rédiger l'introduction globale `intro` et la stratégie générale `strategy` (dans une perspective filières d'abord).

## Contraintes strictes

Pour chaque élément de `recommended_majors`, `university_name`, `university_code`, `major_name`, `major_code` doivent être **strictement identiques** à `parsed.json`, sinon le rapport final ne pourra pas afficher le badge 🔥.

Avant de générer, retrouver et confirmer les valeurs de ces champs dans `parsed.json`.

## Sortie

Enregistrer sous `output/major_recommendation.json`, structure voir [examples/major_recommendation_template.json](examples/major_recommendation_template.json).

```json
{
  "student": { "...辅助画像字段..." },
  "intro": "综合测评开篇（HTML 可用 <strong>）",
  "strategy": "填报策略（专业视角）",
  "major_directions": [
    { "icon": "🧑‍💻", "title": "...", "match_level": "极高", "description": "..." }
  ],
  "recommended_majors": [
    {
      "major_name": "...",
      "major_code": "...",
      "university_name": "...",
      "university_code": "...",
      "modal": { "title": "...", "body": "<h4>...</h4><ul>...</ul>" }
    }
  ]
}
```

## Livraison à l'utilisateur

- Enregistrer le JSON et fournir le chemin absolu
- Commenter en langage naturel les orientations de filières recommandées et les raisons du Top des filières

## Ressources annexes

- [career_reference.md](career_reference.md) — référence filières/orientations professionnelles
