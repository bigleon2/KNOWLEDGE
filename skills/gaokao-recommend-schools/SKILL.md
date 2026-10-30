---
name: gaokao-recommend-schools
description: >-
  À partir de la liste de filières recommandées, du profil du candidat et de la liste de vœux, l'Agent analyse et recommande des établissements avec des raisons personnalisées,
  et produit un school_recommendation.json。Convient à la recommandation d'établissements gaokao, au choix d'universités et à la répartition ambitif/stable/sécurisé (chong-wen-bao).
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Recommander des établissements et justifier

Cette skill est la **quatrième étape**：sur la base des orientations de filière déjà déterminées, recommander depuis `parsed.json` et justifier.

## Amont et aval

- **Amont**：`student.json` + `parsed.json` + `major_recommendation.json`
- **Aval**：[gaokao-generate-report](../gaokao-generate-report/SKILL.md)

## Entrées

1. `student.json` — villes visées, situation familiale, orientation d'emploi, etc.
2. `parsed.json` — étiquettes d'établissement, ville, palan ambitif/stable/sécurisé, probabilité d'admission
3. `major_recommendation.json` — filières et orientations déjà recommandées, pour juger l'adéquation établissement-filière

## Agent Tâche d'analyse

1. Recommander en priorité **les établissements qui contiennent les filières recommandées**ou**dont les disciplines fortes correspondent à l'orientation**.
2. Combiner `preferred_cities`、opportunités industrielles de la ville (voir [career_reference.md](career_reference.md) la table des villes), le niveau d'établissement (985/211/Double première classe, etc.).
3. Équilibrer la répartition ambitif/stable/sécurisé : objectifs centraux en palan stable, avec des représentants parmi les établissements d'élite ambitieux et les établissements de sécurité.
4. Sélectionner **6–12 établissements**, avec pour chacun une `modal` raison de recommandation personnalisée.

## La raison de recommandation doit couvrir

- **avantage géographique**：ressources industrielles, stages et emploi de la ville
- **niveau de l'établissement**：étiquettes et reconnaissance sociale
- **adéquation de filière**：et son lien avec `major_recommendation.json` .
- **rapport admission/valeur**：palan et probabilité en adéquation avec la demande du candidat

## Contraintes dures

`recommended_schools` pour chaque élément, `university_name`、`university_code` doivent être `parsed.json` **strictement identiques**。

## Sortie

Enregistrer sous `output/school_recommendation.json`，structure voir [examples/school_recommendation_template.json](examples/school_recommendation_template.json)。

```json
{
  "school_strategy": "stratégie de répartition des établissements (comment répartir ambitif/stable/sécurisé)",
  "recommended_schools": [
    {
      "university_name": "...",
      "university_code": "...",
      "modal": {
        "title": "raisons de recommandation des écoles :...",
        "body": "<h4>raison de recommandation</h4><ul><li>...</li></ul>"
      }
    }
  ]
}
```

## Livrer à l'utilisateur

- enregistrer le chemin absolu du JSON
- expliquer en langage naturel la logique de recommandation et la répartition en gradins

## Ressources complémentaires

- [career_reference.md](career_reference.md) — référence industries urbaines et niveaux d'établissements
