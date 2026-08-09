# Guide de Sélection Agent/Skill — gen-plan E5/E7

## Arbre de décision

```
1. Existe-t-il un SKILL correspondant ?
   |-- OUI -> Charger le skill
   |   |-- Le skill bénéficie-t-il d'un agent spécialisé ?
   |       |-- OUI -> Skill + Agent Spécialisé (OPTIMAL)
   |       |-- NON -> Skill seul via agent général (BON)
   |-- NON -> Existe-t-il un agent spécialisé ?
       |-- OUI -> Agent Spécialisé seul
       |-- NON -> Agent général (DERNIER RECOURS)
```

## Critères de sélection (ordonnés par impact performance)

1. **Skill + agent spécialisé** (meilleure performance) — Un skill dont le protocole correspond à la tâche ET qui délègue en interne à un agent spécialisé.
2. **Skill seul** (bonne performance) — Un skill dont le protocole couvre entièrement la tâche.
3. **Agent spécialisé seul** (performance modérée) — Aucun skill correspondant, mais un agent spécialisé couvre la tâche.
4. **Agent général** (fallback) — Ni skill ni agent spécialisé. Ne jamais utiliser comme premier choix.

## Tableau de correspondance

| Type de tâche | Skill | Agent | Performance |
|--------------|-------|-------|-------------|
| Dev web Next.js | fullstack-dev | full-stack-developer | OPTIMAL |
| Création PPT/slides | pptx | ppt-expert | OPTIMAL |
| Génération PDF | pdf | general-purpose | OPTIMAL |
| Compréhension images | VLM | general-purpose | OPTIMAL |
| Charts/diagrammes | charts | general-purpose | OPTIMAL |
| Documents Word | docx | general-purpose | BON |
| Fichiers Excel | xlsx | general-purpose | BON |
| Recherche web | web-search | general-purpose | BON |
| Extraction web | web-reader | general-purpose | BON |
| Création skills | skill-creator | general-purpose | BON |
| Génération images | image-generation | general-purpose | BON |
| Édition images | image-edit | general-purpose | BON |
| Speech-to-text | ASR | general-purpose | BON |
| Text-to-speech | TTS | general-purpose | BON |
| Video understanding | video-understand | general-purpose | BON |
| LLM chat | LLM | general-purpose | BON |
| Recherche images | image-search | general-purpose | BON |
| Navigation web | agent-browser | general-purpose | BON |
| Exploration fichiers | — | Explore | Agent seul |
| Architecture/planif | — | Plan | Agent seul |
| Styling CSS | — | frontend-styling-expert | Agent seul |
| Vérification correction | correct-work | general-purpose | BON |