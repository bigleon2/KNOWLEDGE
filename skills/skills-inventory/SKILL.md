---
name: skills-inventory
version: "1.1.0"
category: ecosystem
language: fr
tags:
  - inventory
  - scanning
  - catalog
  - ecosystem
description: >
  Scanner et rapporteur d'inventaire des skills. S'active dès que l'utilisateur demande de
  lister, d'inventorier, de cataloguer, de parcourir, de chercher ou d'explorer les skills
  disponibles — p. ex. "quelles sont les skills dispo", "list all skills", "montre-moi tes
  skills", "inventaire des skills", "quelles skills sont présentes", "génère l'inventaire
  des skills", "skills.md", "skill browser", "trouve une skill pour X", "quelle skill
  utiliser pour Y", "existe-t-il une skill qui fait Z", "quels outils et capacités
  ai-je", "combien de skills dans la catégorie X". Se déclenche également quand
  l'utilisateur mentionne "skills-inventory" explicitement ou s'interroge sur les catégories,
  les effectifs, les statistiques ou les comparaisons de skills. Utilise ce skill dès qu'il
  faut scanner /home/z/my-project/skills/, produire un document d'inventaire des skills,
  trouver la bonne skill pour une tâche, ou répondre à des questions sur l'écosystème de
  skills — même si l'utilisateur ne dit pas explicitement "inventaire des skills".
dependencies: []
read_when:
  - Déclencher quand la demande concerne : scanner et rapporteur d'inventaire des skills
  - Déclencher si la demande mentionne : skills, skill, inventaire
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Skills Inventory (Inventaire des Skills)

Scanne le répertoire local des skills, construit un inventaire structuré et le présente à l'utilisateur.

## Vue d'ensemble

Ce skill fournit un inventaire complet de toutes les skills installées dans `/home/z/my-project/skills/`.
Il lit le frontmatter de chaque `SKILL.md`, extrait les métadonnées (nom, version, description, catégorie)
et produit un inventaire markdown riche qui peut être affiché en ligne, sauvegardé dans un fichier, ou
utilisé pour répondre aux questions liées aux skills.

## Workflow

1. **Exécuter le script scanner** pour obtenir l'état courant de toutes les skills.
2. **Analyser la sortie** pour en tirer un résumé structuré.
3. **Présenter les résultats** dans le format demandé par l'utilisateur (résumé en ligne, fichier complet, ou réponse ciblée).

## Étape 1 — Exécuter le scanner

Exécute le script scanner fourni avec le skill :

```bash
python /home/z/my-project/skills/skills-inventory/scripts/generate_skills_md.py --json
```

La sortie est un tableau JSON sur stdout avec une entrée par skill :

```json
[
  {
    "name": "pdf",
    "display_name": "pdf",
    "version": "1.0",
    "aka": "",
    "date": "2026-06-02",
    "size": "56.7 KB",
    "lines": 879,
    "description": "Professional PDF toolkit with four production lines...",
    "category": "Documents & Contenu"
  }
]
```

Options :
- `--json` — sortie JSON brute (pour usage programmatique)
- `--output /path/to/file.md` — écrit l'inventaire markdown complet dans un fichier
- `--category "IA & Media"` — filtre sur une seule catégorie
- `--search "chart"` — filtre les skills dont le nom ou la description contient le terme recherché

## Étape 2 — Présenter les résultats

Choisis la présentation en fonction de la demande de l'utilisateur :

### Résumé en ligne (par défaut quand l'utilisateur demande "lister les skills" ou "quelles skills as-tu")

Affiche un tableau compact groupé par catégorie avec les effectifs :

```
### Skills installées (66 skills, 12 catégories)

| Catégorie | Skills |
|---|---|
| IA & Media | ASR, TTS, LLM, VLM, image-generation, image-edit, ... |
| Documents & Contenu | pdf, docx, pptx, xlsx, cheat-sheet |
| ... | ... |
```

### Inventaire complet (quand l'utilisateur demande de "générer skills.md" ou "exporter l'inventaire")

Exécute avec `--output` pour écrire le fichier markdown complet :

```bash
python /home/z/my-project/skills/skills-inventory/scripts/generate_skills_md.py \
  --output /home/z/my-project/download/skills.md
```

### Recherche ciblée (quand l'utilisateur demande "trouve une skill pour X" ou "quelle skill fait Y")

Exécute avec `--search` et présente les résultats correspondants :

```bash
python /home/z/my-project/skills/skills-inventory/scripts/generate_skills_md.py \
  --search "chart" --json
```

## Référentiel des catégories

Le scanner classe les skills dans ces 12 catégories :

| Catégorie | Skills typiques |
|---|---|
| Autres | Skills diverses ne rentrant dans aucune autre catégorie |
| Carrière & Emploi | CV, entretiens, suivi des candidatures |
| Contenu & Marketing | Blog, SEO, stratégie de contenu, marketing |
| Documents & Contenu | PDF, DOCX, PPTX, XLSX, cheat-sheet |
| Développement | Fullstack, agent de codage, gestion de versions |
| Finance & Recherche | Finance, analyse boursière, recherche académique, étude de marché |
| IA & Media | ASR, TTS, LLM, VLM, génération/compréhension d'images et vidéos |
| Lifestyle & Bien-être | Bien-être, interprétation des rêves, analyse de fortune |
| Méta (Skills & Plans) | Créateur de skills, recherche de skills, plans rédactionnels, revue de tâches |
| Visualisation & Design | Charts, design, UI/UX, fondations visuelles |
| Web & Recherche | Recherche web, lecture web, multi-recherche, navigateur d'agent |
| Éducation | Quiz, study buddy, outils gaokao (concours d'entrée universitaire) |

## Format de sortie

L'inventaire markdown complet (`skills.md`) contient :
- Un en-tête avec la date de génération, le nombre total de skills et de catégories
- Une table des matières cliquable vers chaque section de catégorie
- Des tableaux par catégorie : Nom, Version, AKA, Date, Taille, Lignes, Description
- Une section détaillée par skill avec la description complète
- Un pied de page avec les métadonnées du fichier

## Notes

- Le scanner lit le frontmatter YAML de chaque `SKILL.md`. Si une skill n'a pas de frontmatter,
  il retombe sur `_meta.json`, puis sur une classification heuristique par mots-clés.
- Les skills sans `SKILL.md` dans leur répertoire sont silencieusement ignorées.
- L'inventaire est un instantané à un instant donné. Relance le scanner pour l'actualiser.
- Ce skill remplace l'ancien `generate_skills_md.py` manuel qui était dans `/scripts/`.

---

## Écosystème Knowledge — Registre KB (décentralisé, Architecture v2.0)

> 📎 Contenu décentralisé depuis `PROMPT-MAITRE-SHARED.md` (corrige-ecosysteme v2.0.0).

### §2.1 Format d'une entrée KNOWLEDGE.md (décentralisé du SHARED §2.2)

```markdown
## [nom-skill] v[X.Y.Z]

- **Category** : [category]
- **Description** : [description courte]
- **Dépend de** : [liste des skills et versions min]
- **Utilisé par** : [liste des skills qui utilisent celui-ci]
- **Dernière calibration** : [date ou N/A]
- **Statut** : [stable | expérimental | en cours]
```

### §2.2 Protocole de Découverte (décentralisé du SHARED §2.3)

Quand un skill doit identifier les skills pertinents pour une tâche :
1. Scanner les entrées de `KNOWLEDGE.md` par catégorie et tags
2. Filtrer par compatibilité de version
3. Vérifier les dépendances croisées
4. Produire une liste ordonnée des skills candidats

---

## Baseline A2 — statut de mesure
> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique SHARED §7 v2 + voie L 3 runs réels) — score baseline 5/7 (nulls : 0) ; détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les nulls 429 restants.
