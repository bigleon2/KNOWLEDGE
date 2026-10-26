---
nom: gaokao-recommend-majors
source: skills/gaokao-recommend-majors/SKILL.md
sha256_source: 503a2d5014c8
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — gaokao-recommend-majors (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/gaokao-recommend-majors/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: gaokao-recommend-majors
description: >-
  Basé sur le profil de l'étudiant et la liste des choix d'orientation via API, l'Agent analyse et recommande des orientations de spécialité adaptées, les débouchés professionnels et une liste spécifique de spécialités,
  produisant un major_recommendation.json structuré. Convient pour la recommandation de spécialités pour le gaokao (examen national d'entrée à l'université en Chine), le choix de spécialité et l'analyse des orientations professionnelles.
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



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


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
