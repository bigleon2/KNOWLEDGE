---
name: gaokao-recommend-schools
version: "1.0.0"
category: "Éducation"
tags:
  - gaokao
  - recommend
  - schools
description: >-
  À partir de la liste de filières recommandées, du profil du candidat et de la liste de vœux,
  l'agent analyse et recommande des établissements en donnant des raisons personnalisées, et
  produit un school_recommendation.json structuré. Convient pour la recommandation d'établissements
  du Gaokao, le choix d'université et la répartition ambitieux/sûrs/de repli des établissements.
language: fr

---

# Recommander les établissements et justifier

Ce skill est la **quatrième étape** du pipeline : une fois les orientations de filières déterminées, recommander des établissements depuis `parsed.json` et en expliquer les raisons.

## Amont / aval

- **Amont** : `student.json` + `parsed.json` + `major_recommendation.json`
- **Aval** : [gaokao-generate-report](../gaokao-generate-report/SKILL.md)

## Entrées

1. `student.json` — villes souhaitées, situation familiale, orientation professionnelle, etc.
2. `parsed.json` — étiquettes des établissements, villes, niveaux ambitieux/sûrs/de repli, probabilités d'admission
3. `major_recommendation.json` — filières déjà recommandées et leurs orientations, pour juger de l'adéquation établissements/filières

## Tâches d'analyse de l'agent

1. Recommander en priorité les établissements **qui proposent les filières déjà recommandées** ou dont **les disciplines d'excellence correspondent aux orientations de filières**.
2. Croiser `preferred_cities`, les opportunités industrielles des villes (se référer à la table des villes de [career_reference.md](career_reference.md)) et le niveau des établissements (985/211/double première classe, etc.).
3. Équilibrer la répartition ambitieux/sûrs/de repli : les objectifs principaux en niveau « sûr », avec au moins un représentant pour les établissements de premier plan ambitieux et pour les établissements de repli.
4. Sélectionner **6 à 12** établissements et rédiger pour chacun une raison de recommandation `modal` personnalisée.

## Ce que les raisons de recommandation doivent couvrir

- **Atout géographique** : industries de la ville et ressources de stages/emplois
- **Niveau de l'établissement** : étiquettes et reconnaissance sociale
- **Adéquation des filières** : lien avec `major_recommendation.json`
- **Rapport qualité/probabilité d'admission** : adéquation du niveau et de la probabilité aux attentes du candidat

## Contraintes strictes

Pour chaque élément de `recommended_schools`, `university_name`, `university_code` doivent être **strictement identiques** à `parsed.json`.

## Sortie

Enregistrer sous `output/school_recommendation.json`, structure voir [examples/school_recommendation_template.json](examples/school_recommendation_template.json).

```json
{
  "school_strategy": "院校布局策略（冲/稳/保如何分配）",
  "recommended_schools": [
    {
      "university_name": "...",
      "university_code": "...",
      "modal": {
        "title": "学校推荐原因：...",
        "body": "<h4>推荐原因</h4><ul><li>...</li></ul>"
      }
    }
  ]
}
```

## Livraison à l'utilisateur

- Enregistrer le JSON et fournir le chemin absolu
- Commenter en langage naturel la logique de recommandation des établissements et la répartition en paliers

## Ressources annexes

- [career_reference.md](career_reference.md) — référence industries des villes et niveaux d'établissements
