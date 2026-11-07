---
name: gaokao-recommend-majors
description: >-
  Basé sur le profil de l'étudiant et la liste des choix d'orientation via API, l'Agent analyse et recommande des orientations de spécialité adaptées, les débouchés professionnels et une liste spécifique de spécialités,
  produisant un major_recommendation.json structuré. Convient pour la recommandation de spécialités pour le gaokao (examen national d'entrée à l'université en Chine), le choix de spécialité et l'analyse des orientations professionnelles.
---

## §0 — Contexte Système (SHARED v1.7.31)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



# Recommandation de spécialités et orientations professionnelles

Ce Skill est la **troisième étape** du pipeline : analyse pure par Agent, sans scripts de règles. En combinant les intérêts de l'étudiant, ses résultats, ses intentions professionnelles et les spécialités réelles de `parsed.json`, il produit des recommandations de spécialités personnalisées.

## Amont et aval

- **Amont** : `student.json` + `parsed.json` (provenant de la collecte d'informations et de l'obtention des choix d'orientation)
- **Aval** : [gaokao-recommend-schools](../gaokao-recommend-schools/SKILL.md) lit `major_recommendation.json`

## Entrées

1. `student.json` — Profil complet de l'étudiant
2. `parsed.json` — Choix d'orientation ambitieux/raisonnables/sûrs et `majors` par université (avec les exigences de matière `claim` et probabilités d'admission)

## Tâches d'analyse de l'Agent

1. Lire [career_reference.md](career_reference.md) pour comprendre les grandes catégories de spécialités et les débouchés professionnels (**référence, pas règles strictes**).
2. Combiner les exigences de matière, les résultats dans chaque matière, les intérêts, la situation familiale et l'orientation professionnelle pour déterminer 2–4 **orientations de spécialité** (`major_directions`).
3. Sélectionner parmi `parsed.json` **8–15 spécialités spécifiques** les plus pertinentes, à inscrire dans `recommended_majors`.
4. Rédiger une introduction synthétique `intro` et une stratégie globale `strategy` (perspective spécialité prioritaire).

## Contraintes strictes

Les champs `university_name`, `university_code`, `major_name`, `major_code` de chaque élément de `recommended_majors` doivent être **exactement identiques** à ceux de `parsed.json`, sinon les étiquettes 🔥 ne s'afficheront pas dans le rapport final.

Vérifier les valeurs des champs dans `parsed.json` avant génération.

## Sortie

Enregistrer sous `output/major_recommendation.json`, la structure est visible dans [examples/major_recommendation_template.json](examples/major_recommendation_template.json).

```json
{
  "student": { "...champs d'assistance au profil..." },
  "intro": "Introduction de l'évaluation synthétique (HTML autorisé <strong>)",
  "strategy": "Stratégie de candidature (perspective spécialité)",
  "major_directions": [
    { "icon": "🧑‍💻", "title": "...", "match_level": "très élevé", "description": "..." }
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

- Enregistrer le chemin absolu du JSON
- Interpréter en langage naturel les orientations de spécialité recommandées et les raisons pour les spécialités de premier plan

## Ressources supplémentaires

- [career_reference.md](career_reference.md) — Référence pour spécialités/orientations professionnelles

</DOCUMENT>
