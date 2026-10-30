---
nom: gaokao-recommend-schools
source: skills/gaokao-recommend-schools/SKILL.md
sha256_source: 8cf8c9c1f5ea
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — gaokao-recommend-schools (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/gaokao-recommend-schools/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: gaokao-recommend-schools
description: >-
  À partir de la liste de filières recommandées, du profil du candidat et de la liste de vœux, l'Agent analyse et recommande des établissements avec des raisons personnalisées,
  et produit un school_recommendation.json。Convient à la recommandation d'établissements gaokao, au choix d'universités et à la répartition ambitif/stable/sécurisé (chong-wen-bao).
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
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


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
