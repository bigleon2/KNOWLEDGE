# Prompt Maître — Génération gen-plan v3.4.0

> **Modèle cible** : GLM-5.1
> **Objectif** : Générer la v3.4.0 du skill `gen-plan` à partir de la v3.3.0
> **Sortie** : `/home/z/my-project/skills/gen-plan/`

---

## Règle zéro — Contexte perdu

Les fichiers v3.3.0 n'existent plus dans cette session. Tu dois **reconstruire** l'intégralité du skill à partir du contexte ci-dessous. Ne jamais utiliser le verbe « conserver » — tout est à recréer.

**Contexte matériel cible** : HP ProBook 640 G2, i5-6300U, 16 Go RAM, SSD ~5 Go libres. Ce matériel justifie le profil VIEUX PC par défaut et les seuils de détection ci-dessous.

---

## Phase 1 — Génération (sections 1.1 à 1.5)

### 1.1 — État reconstruit de gen-plan v3.3.0

gen-plan est un skill de planification de tâches pour assistant IA. Il fonctionne en 4 modes (planification, exécution, surveillance, adaptation) et 15 étapes (E1 à E15) :

| Étape | Rôle |
|-------|------|
| E1 | Analyse de la demande, tagging #token |
| E2 | Classification du type de tâche |
| E3 | Routage vers le bon skill/agent |
| E4 | Détection du profil ressource |
| E5 | Construction du plan structuré |
| E6 | Estimation des coûts |
| E7 | Validation du plan |
| E8 | Génération des todos |
| E9 | Allocation des ressources |
| E10 | Vérification des dépendances |
| E11 | Optimisation du plan |
| E12 | Génération du plan final |
| E13 | Exécution et suivi (commandes concrètes, critères de succès) |
| E14 | Adaptation en cours de route |
| E15 | Bilan, rapport et mise à jour knowledge.md |

**8 principes fondateurs** :
1. Toujours classifier avant d'agir (E2)
2. Le profil ressource ne remonte jamais automatiquement (downgrade irréversible)
3. Préférer un agent spécialisé à N appels génériques
4. Chaque étape produit un artifact vérifiable
5. Les dépendances sont explicites et tracées
6. Le coût est estimé avant l'exécution
7. Les scripts sont en Python, jamais en shell
8. Le plan est adaptatif — il évolue avec le contexte

**3 profils ressource** :

| Profil | Modèle | Signaux de pression | Règles spécifiques |
|--------|--------|---------------------|-------------------|
| NORMAL | sonnet | aucun | Aucune restriction |
| ECO | haiku | 1 signal | Exclure les tâches `#token:>8000` |
| VIEUX PC | haiku/parent-direct | 2+ signaux | Exclure les tâches `#token:>5000`, 5 règles supplémentaires |

**Signaux de pression** : disque < 5 Go (pression) / < 3 Go (critique), timeout 2+ appels consécutifs sur 5 min, tokens > 80 % du budget.

**VIEUX PC — 5 règles** :
1. Dépendances séquentielles uniquement (pas de parallélisme)
2. Choix agent/skill justifié par le coût (le moins cher qui suffit)
3. Budget ressource par phase, jamais global
4. Actions d'économie explicites (résumé de contexte, troncature)
5. Plan de contingence si le profil se dégrade encore

### 1.2 — Exigences v3.4.0 (3 nouveautés)

**N1 — Tagging `#token`** (étape E1) :
- Chaque sous-tâche reçoit un tag `#token:<estimation_numérique>`
- L'estimation est numérique uniquement (ex. `#token:4500`, pas `#token:high`)
- Le tagging est filtré par profil : NORMAL = aucun filtre, ECO = exclure `#token:>8000`, VIEUX PC = exclure `#token:>5000`
- Le filtrage s'applique à l'étape E1, avant la construction du plan

**N2 — Snippets pour recherche accélérée** :
- Chaque sous-tâche reçoit un snippet descriptif de ~80 caractères
- Format : `[snippet] description courte de la sous-tâche [/snippet]`
- Utilisé pour la recherche et le tri rapides dans les plans longs

**N3 — Scripts Python uniquement** :
- Tous les scripts générés par gen-plan doivent être en Python (`.py`)
- Aucun script shell (`.sh`, `bash -c`, heredoc piped)
- Cette règle s'applique globalement (principe fondateur #7)

### 1.3 — Spécifications des fichiers à générer

```
skills/gen-plan/
├── SKILL.md              (< 500 lignes, logique principale)
├── references/
│   ├── resource-management.md   (profils, seuils, VIEUX PC rules)
│   ├── e3-classification.md     (routage Type 1-4)
│   ├── tagging-rules.md         (N1 : tagging #token)
│   └── snippets-spec.md         (N2 : format snippets)
└── evals/
    └── evals.json        (5 evals, schema obligatoire)
```

Règle skill-creator : SKILL.md < 500 lignes. Les détails techniques vont dans `references/`. Chaque fichier référencé doit exister et être complet.

### 1.4 — Classification E3 (routage Type 1-4)

L'étape E3 classe la tâche et route vers le bon outil :

| Type | Livrable | Skill/Agent | Action |
|------|----------|-------------|--------|
| Type 1 | Document (rapport, PPT, PDF, XLSX, docx) | `docx` / `pdf` / `xlsx` / `pptx` | Invoquer le skill correspondant |
| Type 2 | Visualisation (chartes, diagrammes, mind maps) | `charts` | Invoquer `charts` (matplotlib / ECharts / Mermaid / Playwright+CSS) |
| Type 3 | Application web interactive (dashboard, site) | `fullstack-dev` | Invoquer `fullstack-dev` (Next.js) |
| Type 4 | Traitement de données (analyse, transformation) | Python natif | Écrire un script Python |

Alias : `full-stack-developer` = `fullstack-dev` (même agent, noms interchangeables).

Cas ambigus (« dashboard » sans contexte) → demander à l'utilisateur : page interactive ou rapport avec graphiques ?

### 1.5 — Mise à jour resource-management.md

Ce fichier est le cœur de la gestion des ressources dans gen-plan. Il doit contenir :

**Tables obligatoires** :
- Table des profils (NORMAL / ECO / VIEUX PC) avec seuils de tagging
- Table des agents/skills avec tags `#token:<coût_estimé>` pour chaque entrée
- Table des signaux de pression avec seuils numériques

Intégrer dans `resource-management.md` les éléments suivants :

- **Tagging `#token`** : estimation numérique à E1, filtrage par profil
- **Filtrage par profil** : tableau des seuils (NORMAL / ECO / VIEUX PC)
- **Choix agent/skill par coût** : chaque agent/skill reçoit un tag `#token:<coût_estimé>` dans les tables de référence
- **Scripts Python uniquement** : remplacer toute référence à shell/bash par Python
- **Seuils de détection** : disque < 5 Go = pression, < 3 Go = critique ; timeout 2+/5 min ; tokens > 80 %
- **Snippets** : ajout du snippet ~80 chars dans la représentation des sous-tâches

---

## Phase 2 — Intégration (section 2)

Une fois les fichiers v3.4.0 générés et validés :

1. **Intégration skills/agents** : mettre à jour les références croisées entre `gen-plan` et les autres skills (`docx`, `pdf`, `xlsx`, `pptx`, `charts`, `fullstack-dev`, `full-stack-developer`). Vérifier que le routing E3 (Type 1-4) est cohérent avec les noms de skills réellement disponibles.
2. **knowledge.md** : créer ou mettre à jour `knowledge.md` avec le résumé de la v3.4.0 (nouveautés N1/N2/N3, changements de routing E3, profils ressource). Ce fichier sert de mémoire persistante entre sessions.
3. **Push GitHub** : si un repo est configuré, pusher les fichiers sur la branche appropriée avec un commit descriptif (ex. `feat(gen-plan): v3.4.0 — tagging, snippets, python-only`).

**Note** : la Phase 2 ne démarre que si la Phase 1 est validée (checklist 3.4 partiellement cochée pour les items de Phase 1).

---

## Phase 3 — Évaluations et rapport (section 3)

Les evals sont exécutées après la Phase 2. Elles valident que les 3 nouveautés (N1, N2, N3) sont correctement intégrées et que le routing E3 fonctionne pour les 4 types.

### 3.1 — Schéma evals.json obligatoire

```json
{
  "evals": [
    {
      "id": "eval-1",
      "name": "description de l'eval",
      "type": "unit|integration|regression",
      "input": "description du scénario d'entrée",
      "expected": "résultat attendu",
      "profile": "NORMAL|ECO|VIEUX_PC",
      "tags": ["#token:3500", "snippets"]
    }
  ]
}
```

5 evals obligatoires couvrant :
1. Tagging #token avec filtrage par profil
2. Snippets ~80 caractères dans un plan
3. Routing E3 Type 1-4
4. Détection VIEUX PC et application des 5 règles
5. **Scripts Python uniquement** (aucun shell)

Chaque eval doit spécifier le profil de test (`NORMAL`, `ECO` ou `VIEUX_PC`) pour vérifier le filtrage par profil.

### 3.2 — Rapport de validation

Générer un rapport de validation (pas comparatif — les fichiers v3.3.0 n'existent pas) :
- Chaque eval : statut (pass/fail), détail de l'exécution, écart éventuel
- Vérification de la structure fichiers (arbre conforme à la section 1.3)
- Vérification SKILL.md < 500 lignes
- Vérification que chaque référence dans SKILL.md pointe vers un fichier existant dans `references/`
- Si une eval fail : analyser la cause, corriger le fichier concerné, relancer

### 3.3 — Critères de succès par phase

- **Phase 1** : tous les fichiers de l'arbre 1.3 présents et complets, SKILL.md < 500 lignes
- **Phase 2** : références croisées mises à jour, knowledge.md généré, push effectué si possible
- **Phase 3** : 5 evals pass, rapport de validation rédigé, checklist 3.4 cochée

### 3.4 — Checklist de vérification finale

- [ ] SKILL.md < 500 lignes
- [ ] Tous les fichiers référencés existent dans `references/`
- [ ] 5 evals présentes dans `evals.json` avec le schéma correct
- [ ] Aucun script shell dans les exemples ou instructions
- [ ] Tagging `#token` présent à E1 avec filtrage par profil
- [ ] Snippets ~80 chars présents dans la spec
- [ ] Routing E3 Type 1-4 complet avec alias full-stack-developer
- [ ] Seuils de détection explicites (< 5 Go / < 3 Go / timeout / tokens)
- [ ] 5 règles VIEUX PC toutes présentes
- [ ] knowledge.md créé ou mis à jour
- [ ] Rapport de validation généré

---

## Ordre d'exécution

1. Lire ce prompt intégralement avant de commencer
2. Phase 1 → générer tous les fichiers
3. Auto-vérifier avec la checklist 3.4 (items Phase 1)
4. Phase 2 → intégration écosystème
5. Phase 3 → evals + rapport
6. Vérification finale : checklist 3.4 complète
