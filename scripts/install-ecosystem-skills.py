#!/usr/bin/env python3
"""
Installation des 3 skills écosystème + registre KB + SHARED.
Exécution séquentielle, chaque fichier est écrit puis vérifié.
"""

import json
import os

BASE = "/home/z/my-project/skills"
DOWNLOAD = "/home/z/my-project/download"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    lines = content.count("\n") + 1
    print(f"  OK {path} ({lines} lignes)")

# ============================================================
# 1. SHARED
# ============================================================
print("\n[1/11] SHARED")
write_file(f"{BASE}/_prompts-maitres/PROMPT-MAITRE-SHARED.md", open(f"{DOWNLOAD}/PROMPT-MAITRE-SHARED.md", encoding="utf-8").read())

# ============================================================
# 2. gen-plan/SKILL.md (~180 lignes)
# ============================================================
print("\n[2/11] gen-plan/SKILL.md")
GEN_PLAN_SKILL = r"""---
name: gen-plan
version: 3.6.1
category: ecosystem
language: fr
tags:
  - planning
  - task-management
  - token-estimation
  - auto-calibration
  - ecosystem
description: >
  Skill de planification de tâches pour assistant IA.
  4 modes (Planification, Exécution, Surveillance, Adaptation),
  15 étapes (E1-E15), 3 profils ressource (NORMAL/ECO/VIEUX PC),
  tagging #token, snippets, scripts Python uniquement.
dependencies:
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "E1, E8 hook"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
---

# gen-plan — Planification de tâches

## §0 — Règle zéro

L'écosystème Knowledge est un ensemble de 77 skills conçus pour un assistant IA (6 skills écosystème + 71 skills métier). Chaque skill est auto-contenu dans son répertoire sous `skills/`, dispose d'un fichier `SKILL.md` principal, d'un frontmatter YAML, et de références optionnelles dans `references/`. Le registre KB (`skills/KNOWLEDGE.md`) est la source de vérité.

## §1 — Spécification fonctionnelle

### Déclencheurs

- `gen-plan:` suivi d'une description de tâche
- `gen-plan:correct-work(projet)` ou `gen-plan:correct-work(<cible>)`
- `plan d'actions`, `orchestre`
- `gen-plan:generate(<description>)`

### 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Planification** | Analyse, classification, estimation, création du plan |
| M2 | **Exécution** | Passage à l'action selon le plan établi |
| M3 | **Surveillance** | Monitoring en temps réel, détection d'écarts |
| M4 | **Adaptation** | Ajustement du plan en cas de dérive |

### 15 étapes (E1-E15)

| Étape | Nom | Mode |
|-------|------|------|
| E1 | Analyse de la demande | M1 |
| E2 | Inventaire des ressources | M1 |
| E3 | Classification du type de tâche | M1 |
| E4 | Estimation #token | M1 |
| E5 | Sélection des skills | M1 |
| E6 | Profilage ressource | M1 |
| E7 | Création du plan | M1 |
| E8 | Validation du plan (+ hook correct-work) | M1 |
| E9 | Lancement de l'exécution | M2 |
| E10 | Suivi d'étape | M2/M3 |
| E11 | Checkpoint intermédiaire | M3 |
| E12 | Détection d'écart | M3 |
| E13 | Ajustement | M4 |
| E14 | Finalisation (+ intégration écosystème) | M2 |
| E15 | Bilan et auto-calibration | M1/M4 |

Détail complet : `references/etapes-detaillees.md`

### Normes

- **N1 (Tagging #token)** : chaque étape/skill reçoit un tag `#token` estimé. Auto-calibré après exécution.
- **N2 (Snippets)** : snippets de code réutilisables, tagués et versionnés.
- **N3 (Python uniquement)** : tous les scripts générés sont en Python. Aucun shell/bash/powershell.

### Philosophie

1. **Read before planning** — Toujours lire le projet avant de planifier.
2. **Performance-driven** — Le choix agent/skill est dicté par le gain de performance.
3. **Skills can launch agents** — Modèle à deux couches : Skill (protocole) → Agent (exécution).
4. **Serial by default** — Parallélisme interdit sauf demande explicite + indépendance prouvée.
5. **Visible progress** — L'utilisateur sait toujours où on en est.
6. **CoT + Chaining** — Raisonnement structuré avant chaque action, sortie vérifiée avant la suivante.
7. **Lecture bloc par bloc** — Fichiers > 500 lignes lus par blocs avec synthèse intermédiaire.
8. **Downgrade irréversible** — Le profil ressource ne remonte jamais automatiquement.

## §2 — Spécification technique

### Stack
- **Langage** : Python (scripts), Markdown (docs), YAML (frontmatter)
- **Environnement** : `skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB)

### Structure

```
skills/gen-plan/
├── SKILL.md                          # Ce fichier (~180 lignes)
├── references/
│   ├── etapes-detaillees.md          # Détail des 15 étapes
│   ├── grille-token.md               # Grille de calibration #token
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   └── guide-selection-agent-skill.md # Arbre de décision + tableau
└── evals/
    └── evals.json                    # Cas de test d'évaluation
```

### Auto-calibration (E15)

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action |
| 20-35% | Ajustement paramétrage fin |
| >35% | Recalibration complète |

### Profils ressource

| Profil | Contexte | Règles clés |
|--------|----------|-------------|
| **NORMAL** | Par défaut | 15 étapes complètes, tous les skills |
| **ECO** | Discussion < 5 sessions, #token < 3500 | Étapes réduites, 1 checkpoint |
| **VIEUX PC** | Matériel limité | Règles ECO + scripts < 100 lignes |

**Downgrade irréversible** : NORMAL → ECO ou ECO → VIEUX PC est définitif pour la session.

Détail complet : `references/profils-ressource.md`

### Intégration KB

Si activé (`kb_path` vers `skills/KNOWLEDGE.md`, flag `--kb-skill`), gen-plan utilise le Protocole de Découverte (SHARED §2.3) pour scanner le registre et identifier les skills pertinents.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| correct-work | Invoque à E1 | Validation plan initial, >= v2.4.0 |
| clone-chat | Calibration + archivage | E4, E15, optionnel, >= v2.0.0 |
| skills-inventory | Consultation à E5 | Sélection skills, >= v1.0.0 |
| KNOWLEDGE.md | Enrichissement à E15 | Mise à jour registre et calibration |

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet.

## §4 — Grille #token (résumé)

| Agent/Skill | #token min | #token max |
|-------------|-----------|-----------|
| Planification E1-E2 | 800 | 1500 |
| Création plan E7 | 1000 | 2500 |
| Exécution simple | 2000 | 5000 |
| Exécution complexe (4+ skills) | 10000 | 20000 |
| Surveillance E10-E12 | 500 | 1500 |
| Auto-calibration E15 | 800 | 2000 |

Grille complète et historique : `references/grille-token.md`

## §5 — Conventions

- **Nommage** : kebab-case (SHARED §1.2), versions semver (X.Y.Z)
- **Python uniquement** (N3) : scripts Python, jamais shell/bash
- **Tagging** : préfixe `#` pour les tokens (`#token 3500`)
- **Variables** : double accolades (`{{SKILLS_ROOT}}` = `skills/`)
- **Worklog** : format SHARED §1.4, mise à jour après chaque phase
"""
write_file(f"{BASE}/gen-plan/SKILL.md", GEN_PLAN_SKILL)

# ============================================================
# 3-7. gen-plan/references/ (5 fichiers)
# ============================================================

print("\n[3/11] gen-plan/references/etapes-detaillees.md")
ETAPES = r"""# Détail des 15 étapes gen-plan

## E1 — Analyse de la demande

**Objectif** : Décortiquer la demande utilisateur pour en extraire les livrables, contraintes et critères de succès.

**Inputs** : Message brut de l'utilisateur, contexte de session (worklog, artefacts), KNOWLEDGE.md (si KB activé)
**Outputs** : Liste des livrables, contraintes, critères de succès, questions clarificatoires
**Validation** : Au moins 1 livrable identifié, contraintes explicites, type identifiable

---

## E2 — Inventaire des ressources

**Objectif** : Bilan de tout ce qui est disponible pour accomplir la tâche.

**Méthode — Lecture bloc par bloc** : Pour chaque fichier > 500 lignes, lire par blocs de 200 lignes avec synthèse intermédiaire.

**Inputs** : Sortie E1, `skills/` (liste skills), KB, fichiers projet
**Outputs** : Skills pertinents, fichiers/sources, synthèses blocs, gaps
**Validation** : Skills pertinents identifiés, gaps listés, fichiers > 500L traités par blocs

---

## E3 — Classification du type de tâche

**Objectif** : Router vers le bon type (Type 1-4).

**Inputs** : Livrables (E1), ressources (E2), grille classification
**Outputs** : Type assigné, skill principal, skills secondaires, mode par défaut
**Validation** : Exactement 1 type, skill principal identifié, pas de conflit

Voir `classification-types.md` pour le détail des 4 types.

---

## E4 — Estimation #token

**Objectif** : Calculer le budget token.

**Inputs** : Type (E3), complexité, profil (E6), grille #token
**Outputs** : Estimation totale, par étape, tag #token par skill
**Validation** : Estimation dans la plage du profil, tags présents

---

## E5 — Sélection des skills

**Objectif** : Identifier les skills pertinents.

**Inputs** : Type (E3), ressources (E2), skills-inventory, KB
**Outputs** : Liste ordonnée des skills, versions minimales, nature utilisation
**Validation** : Chaque skill existe dans registre/inventaire, versions cohérentes

---

## E6 — Profilage ressource

**Objectif** : Choisir le profil adapté (NORMAL/ECO/VIEUX PC).

**Inputs** : Estimation #token (E4), complexité, contraintes matérielles
**Outputs** : Profil assigné, justification, restrictions
**Validation** : 1 profil assigné, justification cohérente

Voir `profils-ressource.md` pour le détail.

---

## E7 — Création du plan

**Objectif** : Assembler le plan d'exécution structuré.

**Inputs** : Livrables (E1), Skills (E5), Profil (E6), #token (E4)
**Outputs** : Plan structuré, TODO list, étapes parallélisables
**Validation** : E9-E14 couvertes, dépendances explicites, 1+ checkpoint

---

## E8 — Validation du plan

**Objectif** : Vérifier cohérence, complétude, faisabilité.

**Inputs** : Plan brut (E7), contraintes (E1)
**Outputs** : Plan validé, risques et contournements

**Checks** :
- Cohérence interne, complétude, faisabilité, pas de cycle dépendances
- Classification fichiers candidats (Skill / Écosystème / Utilitaire)
- YAML frontmatter valide pour les Skills
- Scripts Python compilables, Markdown structurés, config valides
- Références croisées valides

**Hook correct-work** (si >= v2.4.0 disponible) :
- Lancer `correct-work(cibles, mode=CIBLE)` sur les livrables
- FAIL → pause jusqu'à correction
- PASS AVEC RÉSERVES → loggées, exécution continue
- PASS → passage à E9

---

## E9 — Lancement de l'exécution

**Objectif** : Démarrer l'exécution selon le plan validé.

**Méthode** : Si fichiers sources > 500 lignes, appliquer lecture par blocs avant exécution.
**Validation** : Exécution démarrée, worklog initialisé, fichiers volumineux synthétisés

---

## E10 — Suivi d'étape

**Objectif** : Monitorer chaque étape en cours.

**Méthode** : Vérifier cohérence bloc par bloc (utiliser synthèses E2/E9).
**Outputs** : Worklog par étape, #token réel, écarts
**Validation** : Chaque étape loggée, #token réel mesuré

---

## E11 — Checkpoint intermédiaire

**Objectif** : Vérification à mi-parcours.
**Outputs** : Bilan mi-parcours, ajustements mineurs, décision (continuer/ajuster/arrêter)
**Validation** : Checkpoint à ~50%, décision documentée

---

## E12 — Détection d'écart

**Objectif** : Comparer réel vs estimé.
**Outputs** : Tableau écarts, alertes si > 20%
**Validation** : Écarts calculés, alertes si seuil dépassé

---

## E13 — Ajustement

**Objectif** : Modifier le plan en cas de dérive.
**Outputs** : Plan révisé, justification, nouvelle estimation
**Validation** : Modifications justifiées, plan révisé cohérent

---

## E14 — Finalisation

**Objectif** : Achèvement des étapes restantes + intégration écosystème.

**Checks intégration** :
- Fichiers Skill dans `skills/<nom>/SKILL.md`
- Références dans `skills/<nom>/references/`
- Aucun écrasement sans confirmation
- YAML frontmatter conforme (SHARED §1.3)
- Inventaire skills mis à jour si nécessaire

**Validation** : Tous livrables produits, worklog à jour

---

## E15 — Bilan et auto-calibration

**Objectif** : Retour d'expérience et mise à jour des grilles.

**Outputs** : Bilan session, mise à jour grille #token (si écart > 20%), enrichissement KB, clone-chat éventuel

**Auto-réapplication** : Si SKILL.md modifié pendant l'exécution, tâches restantes marquées `[REEVALUER]`.

**Validation** : Bilan produit, calibration mise à jour si nécessaire, KB enrichi si pertinent
"""
write_file(f"{BASE}/gen-plan/references/etapes-detaillees.md", ETAPES)

print("\n[4/11] gen-plan/references/grille-token.md")
GRILLE = r"""# Grille de calibration #token — gen-plan v3.6.1

## Grille par agent/skill

| Agent/Skill | #token min | #token max | Coeff. complexité |
|-------------|-----------|-----------|------------------|
| Planification E1-E2 | 800 | 1500 | 1.0x |
| Classification E3 | 200 | 500 | 1.0x |
| Estimation E4 | 300 | 800 | 1.0x |
| Sélection E5 | 500 | 1200 | 1.2x |
| Profilage E6 | 200 | 400 | 1.0x |
| Création plan E7 | 1000 | 2500 | 1.5x |
| Validation E8 | 500 | 1500 | 1.0x |
| Exécution simple (1 skill) | 2000 | 5000 | 1.0x |
| Exécution moyenne (2-3 skills) | 5000 | 10000 | 1.3x |
| Exécution complexe (4+ skills) | 10000 | 20000 | 1.5x |
| Surveillance E10-E12 | 500 | 1500 | 1.0x |
| Auto-calibration E15 | 800 | 2000 | 1.0x |

## Grille par type de tâche (usage clone-chat)

| Mode | Longueur discussion | #token estimé | Profil min. |
|------|---------------------|---------------|-------------|
| clone-court | < 5 sessions | 2000-3500 | ECO |
| clone-moyen | 5-15 sessions | 3500-5500 | NORMAL |
| clone-long | > 15 sessions | 5500-9000 | NORMAL |

## Coefficients d'ajustement

| Facteur | Coefficient | Condition |
|---------|-------------|-----------|
| Complexité faible | 0.8x | Tâche routinière, template existant |
| Complexité standard | 1.0x | Cas nominal |
| Complexité élevée | 1.3x | Multi-skills, dépendances croisées |
| Complexité critique | 1.5x | Projet nouveau, aucune référence |
| Profil ECO | 0.7x | Réduction surveillance |
| Profil VIEUX PC | 0.5x | Scripts légers, pas de graphiques |

## Historique de calibration

| Exécution | Date | Type tâche | Estimé | Réel | Écart | Action |
|-----------|------|-----------|--------|------|-------|--------|
| 1 | 2026-07-18 | Planification 66 skills | 4500 | 5200 | +15.6% | Aucune |
| 2 | 2026-07-18 | Test E2E gen-plan | 3000 | 3600 | +20.0% | Aucune (seuil) |
| 3 | 2026-07-29 | clone-chat v1.1.0 | 4000 | 5200 | +30.0% | Ajustement grille |
| 4 | 2026-07-29 | clone-chat v1.2.0 | 4400 | 4600 | +4.5% | Aucune |
"""
write_file(f"{BASE}/gen-plan/references/grille-token.md", GRILLE)

print("\n[5/11] gen-plan/references/classification-types.md")
CLASSIF = r"""# Classification des types de tâches — gen-plan E3

## Type 1 — Document création

**Indicateurs** : rapport, document, article, analyse, proposition, PRD, script, manuscrit, présentation, tableur
**Formats** : DOCX, PDF, XLSX, PPTX, MD
**Skill** : docx, pdf, xlsx, pptx (selon format)

---

## Type 2 — Data Visualization

**Indicateurs** : graphique, chart, diagramme, mind map, flowchart, architecture, visualisation
**Formats** : PNG, SVG, Mermaid, D3, ECharts
**Skill** : `charts`
**Sous-routage** : données chiffrées → matplotlib/seaborn/echarts ; structure → Mermaid/Playwright+CSS ; mind map → Playwright+CSS

---

## Type 3 — Interactive Web Development

**Indicateurs** : site web, application, dashboard interactif, page, interface, Next.js, React
**Skill** : `fullstack-dev`

---

## Type 4 — Data Processing

**Indicateurs** : analyse, traiter, transformer, calculer, extraire, filtrer, convertir
**Action** : Script Python directement

---

## Cas ambigus

| Situation | Règle |
|-----------|-------|
| "Dashboard" sans précision | Demander : interactif ou statique ? |
| "Analyse" avec sortie document | Type 1 |
| "Analyse" sans sortie | Type 4 |
| "Visualisation" dans un document | Type 1 |
| "Visualisation" autonome | Type 2 |
| Mention Next.js/React | Toujours Type 3 |
"""
write_file(f"{BASE}/gen-plan/references/classification-types.md", CLASSIF)

print("\n[6/11] gen-plan/references/profils-ressource.md")
PROFILS = r"""# Profils ressource — gen-plan v3.6.1

## NORMAL

**Contexte** : Par défaut. 15 étapes, tous les skills, surveillance complète, snippets versionnés.
**Seuils** : #token sans plafond, E10+E11+E12 obligatoires.

---

## ECO

**Déclenchement** : Discussion < 5 sessions, #token < 3500, tâche simple (1 skill, 1 livrable), 1 signal de pression.
**Règles** : E1-E9 puis E14-E15 (E10-E13 fusionnées), snippets simplifiés, 1 checkpoint, pas de matrice dynamique KB, sous-tâches > 8000 #token exclues.

---

## VIEUX PC

**Déclenchement** : 2+ signaux de pression ou 1 signal critique.
**Règles ECO** + 5 règles supplémentaires :
1. Dépendances séquentielles uniquement (pas de parallélisme)
2. Choix agent/skill justifié par le coût
3. Budget ressource par phase (jamais global)
4. Actions d'économie explicites (résumé contexte, troncature > 500L)
5. Plan de contingence (mode survie : E1, E3, E7, E14 uniquement si 3+ signaux critiques)

**Restrictions** : pas d'images, scripts < 100 lignes, O(n) préféré, pas de gros fichiers en mémoire, pas de graphiques, pas de Playwright.
**Seuils** : #token plafond 2000.

---

## Signaux de pression

| Signal | Seuil pression | Seuil critique |
|--------|---------------|----------------|
| Espace disque | < 5 Go | < 3 Go |
| Timeout appels | 2+ consécutifs / 5 min | 4+ / 5 min |
| Budget tokens | > 80 % | > 95 % |

**1 signal pression** → ECO. **2+ signaux ou 1 critique** → VIEUX PC.

---

## Downgrade irréversible

Le profil ne remonte jamais automatiquement. NORMAL → ECO ou ECO → VIEUX PC est définitif pour la session.
"""
write_file(f"{BASE}/gen-plan/references/profils-ressource.md", PROFILS)

print("\n[7/11] gen-plan/references/guide-selection-agent-skill.md")
GUIDE = r"""# Guide de Sélection Agent/Skill — gen-plan E5/E7

## Arbre de décision

1. Existe-t-il un SKILL correspondant ?
   |-- OUI → Charger le skill
   |   |-- Le skill bénéficie-t-il d'un agent spécialisé ?
   |       |-- OUI → Skill + Agent Spécialisé (OPTIMAL)
   |       |-- NON → Skill seul via agent général (BON)
   |-- NON → Existe-t-il un agent spécialisé ?
       |-- OUI → Agent Spécialisé seul
       |-- NON → Agent général (DERNIER RECOURS)

## Critères de sélection (par impact performance)

1. **Skill + agent spécialisé** (OPTIMAL) — Protocole + exécution spécialisée
2. **Skill seul** (BON) — Protocole couvre la tâche
3. **Agent spécialisé seul** (MODÉRÉ) — Pas de skill correspondant
4. **Agent général** (FALLBACK) — Ni skill ni agent spécialisé

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
| Vérification | correct-work | general-purpose | BON |
| Exploration fichiers | — | Explore | Agent seul |
| Architecture | — | Plan | Agent seul |
| Styling CSS | — | frontend-styling-expert | Agent seul |
"""
write_file(f"{BASE}/gen-plan/references/guide-selection-agent-skill.md", GUIDE)

# ============================================================
# 8. gen-plan/evals/evals.json
# ============================================================
print("\n[8/11] gen-plan/evals/evals.json")
EVALS_GENPLAN = {
    "skill": "gen-plan",
    "version": "3.6.1",
    "evals": [
        {"id": "E1-classification", "name": "Classification correcte Type 1-4", "input": "Crée un rapport d'analyse", "expected_type": 1, "expected_skill": "docx"},
        {"id": "E2-token-estimation", "name": "Estimation #token cohérente", "input": "Tâche moyenne, 5-15 sessions", "expected_token_range": [3500, 5500], "expected_profile": "NORMAL"},
        {"id": "E3-plan-complet", "name": "Plan E1-E15 complet", "input": "Planifier la création d'un dashboard Next.js", "expected_steps": 15, "expected_type": 3},
        {"id": "E4-auto-calibration", "name": "Auto-calibration E15", "input": "Écart estimé 28%", "expected_action": "Ajustement paramétrage fin"},
        {"id": "E5-python-only", "name": "Scripts Python uniquement", "input": "Générer un script de traitement", "expected_language": "python", "forbidden": ["bash", "sh", "powershell"]}
    ]
}
write_file(f"{BASE}/gen-plan/evals/evals.json", json.dumps(EVALS_GENPLAN, indent=2, ensure_ascii=False))

# ============================================================
# 9. correct-work/SKILL.md (~315 lignes)
# ============================================================
print("\n[9/11] correct-work/SKILL.md")
CORRECT_WORK_SKILL = r"""---
name: correct-work
version: 2.4.0
category: ecosystem
language: fr
tags:
  - verification
  - correction
  - quality-assurance
  - ecosystem
  - kb-integration
description: >
  Skill de vérification et correction du travail réalisé.
  5 étapes, 3 modes (PROJET/CIBLE/DIRECT),
  support multi-cibles, découplage gen-plan optionnel,
  intégration KB, matrice de décision (statique + dynamique),
  métriques de performance.
dependencies:
  - skill: gen-plan
    version: ">=3.6.0"
    used_at: "Étape 1 (optionnel, mode PROJET)"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "Mode CIBLE, Context Drift"
  - skill: fullstack-dev
    version: ">=1.0.0"
    used_at: "Vérification projets web"
---

# correct-work — Vérification et correction

## §0 — Règle zéro

L'écosystème Knowledge est un ensemble de 77 skills conçus pour un assistant IA (6 skills écosystème + 71 skills métier). Chaque skill est auto-contenu dans son répertoire sous `skills/`, dispose d'un fichier `SKILL.md` principal, d'un frontmatter YAML, et de références optionnelles dans `references/`. Le registre KB (`skills/KNOWLEDGE.md`) est la source de vérité.

## §1 — Spécification fonctionnelle

### Déclencheurs

- `verifie ton travail`, `verifie tes résultats`, `verifie ton code`
- `correct-work` ou `correct_work`, `verify-work`
- `correct-work(projet)` — vérification complète
- `correct-work(<cible>)` — vérification ciblée
- `correct-work()` — vérification rapide

### 3 modes

| Mode | Nom | Description | Cas d'usage |
|------|-----|-------------|-------------|
| **PROJET** | Prompt-maître | Vérification complète via prompt maître | Validation finale d'un projet complexe |
| **CIBLE** | Ciblé | Vérification d'un skill/fichier spécifique (défaut) | Vérification d'un skill |
| **DIRECT** | Rapide | Correction directe sans plan préalable | Correction rapide d'un fichier |

### 5 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| 1 | Plan d'actions | Création du plan (gen-plan si dispo, sinon autonome) |
| 2 | Erreurs et omissions | Détection erreurs factuelles, omissions, incohérences |
| 3 | Structure et conflits | Vérification structure, conflits, cohérence format |
| 4 | Vérification des interactions | Relations inter-skills, dépendances, interfaces |
| 5 | Cohérence des raisonnements | Logique globale, cohérence argumentaire |

### Support multi-cibles

Plusieurs artefacts dans une même session. Sous-rapport par cible, verdict global = pire des verdicts individuels.

### Découplage gen-plan

Mode PROJET utilise gen-plan à l'Étape 1. Si indisponible, correct-work génère un plan simplifié en autonome.

### Intégration KB

Si activé (`kb_path`, `--kb-skill`), utilisation du Protocole de Découverte (SHARED §2.3) et de la matrice dynamique.

## §2 — Spécification technique

### Stack
- **Langage** : Markdown (rapports), Python (scripts), YAML (frontmatter)
- **Environnement** : `skills/correct-work/`

### Dépendances

| Dépendance | Version | Utilisation | Optionnelle |
|------------|---------|-------------|-------------|
| gen-plan | >= v3.6.0 | Étape 1 | Oui |
| clone-chat | >= v2.0.0 | Mode CIBLE | Oui |
| fullstack-dev | >= v1.0.0 | Projets web | Oui |

### Structure

```
skills/correct-work/
├── SKILL.md              # Ce fichier (~315 lignes)
├── scripts/
│   └── verify-correct-work.py  # 16 checks post-install
└── evals/
    └── evals.json        # Cas de test
```

### Critères de sévérité

| Sévérité | Label | Description | Action |
|----------|-------|-------------|--------|
| **S1** | Critique | Empêche le fonctionnement | Correction immédiate obligatoire |
| **S2** | Majeur | Altère significativement le comportement | Correction dans cette session |
| **S3** | Mineur | Impact limité, cosmétique | Correction souhaitable, non bloquante |
| **S4** | Suggestion | Amélioration possible | Optionnel |

### Métriques de performance

| Métrique | Description | Cible |
|----------|-------------|-------|
| `findings_total` | Nombre total de findings | Réduire au fil des sessions |
| `taux_correction` | Corrections / findings trouvés | > 80% |
| `faux_positifs` | Findings reclassés ou annulés | < 10% |

### Logging worklog

Format SHARED §1.4. Spécifiquement : `Agent: correct-work v2.4.0`, étapes 1-5 loggées, verdict final.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Invocation à E1 | Plan vérification, >= v3.6.0 |
| clone-chat | Vérification CIBLE | Context Drift, >= v2.0.0 |
| fullstack-dev | Vérification | Projets web, >= v1.0.0 |
| KNOWLEDGE.md | Scan dynamique | Découverte versions et dépendances |

## §4 — Checklists

### §4.1 Mode PROJET

**Pré-vérification** : prompt maître disponible, version identifiée, livrables listés
**Phase 1** : plan créé (gen-plan ou autonome), sections identifiées, ordre défini
**Phase 2** : chaque section comparée au livrable, erreurs factuelles listées, classées S1-S4
**Phase 3** : structure vérifiée, conventions respectées, cross-refs cohérentes
**Phase 4** : dépendances vérifiées, versions minimales respectées, interfaces cohérentes
**Phase 5** : chaîne logique, décisions cohérentes, alignement décisions/actions
**Post** : rapport produit, verdict assigné, worklog à jour

### §4.2 Mode CIBLE

**Pré-vérification** : cible identifiée, specs chargées (via KB si dispo), version identifiée
**Vérification** : structure, contenu vs specs, cross-refs, dépendances, format
**Spécifique clone-chat** (si applicable) : Context Drift §3.5, règle drift vide, 5 types drift, 7+1 étapes, chemins relatifs, seuil < 200L
**Post** : corrections appliquées, worklog, verdict

### §4.3 Mode DIRECT

**Inspection** : artefact accessible, problèmes évidents, corrections immédiates
**Post** : correction ne casse rien, worklog (optionnel)

### §4.4 Sélection du mode

| Condition | Mode |
|-----------|-------|
| Un prompt maître existe | PROJET |
| Un skill spécifique à vérifier | CIBLE |
| Correction rapide fichier isolé | DIRECT |
| Non précisé | CIBLE (défaut) |

### §4.5 Verdicts

- **PASS** : 0 problème S1-S2
- **PASS AVEC RÉSERVES** : 0 S1 mais >= 1 S2, ou >= 2 S3
- **FAIL** : >= 1 S1

### §4.6 Adaptation au type de projet

| Type | Étape 2 focus | Étape 3 focus | Étape 4 focus |
|------|---------------|---------------|---------------|
| **Fullstack** | Schema BDD, auth, endpoints | Imports circulaires, state | API frontend-backend, props |
| **Frontend** | Responsive, accessibilité | Conventions CSS | Props, state management |
| **Backend/API** | Endpoints, validation | Gestion erreurs | Services, timeouts, CORS |
| **Document/PDF** | Contenu, mise en page | Cohérence sections | Références entre livrables |
| **Script** | I/O, paramètres, sorties | Chemins en dur, erreurs | Dépendances externes |
| **Écosystème skills** | Versions, frontmatter, deps | Cross-refs, conventions SHARED | Relations bidirectionnelles, KB |

### §4.7 Étape 2 — Détail

1. Relire les spécifications et vérifier chaque exigence satisfaite
2. Vérifier les données factuelles (noms, chemins, versions, counts)
3. Vérifier la cohérence linguistique
4. Vérifier les fichiers de sortie (existent, lisibles, non vides)
5. Vérifier les dépendances (imports, chemins, références croisées)
6. Adapter au type de projet (§4.6)
7. Corriger chaque erreur ou omission

### §4.8 Étape 3 — Détail

1. Imports circulaires
2. Conflits de noms
3. Variables non initialisées
4. Chemins en dur non portables
5. Gestion des erreurs (pas d'échec silencieux)
6. Doublons à factoriser
7. Convention de nommage cohérente
8. Matrice de cohérence logique (conditions complexes)
9. Corriger chaque problème

### §4.9 Étape 4 — Détail

1. API frontend-backend (endpoints, params, codes erreur)
2. Props inter-composants (types, callbacks, optionnalité)
3. State management (store, actions, state mort)
4. Flux de données bout en bout
5. Communications entre services (ports, URLs, WebSockets)
6. Références croisées entre livrables
7. Corriger chaque problème

### §4.10 Étape 5 — Détail

1. Cohérence logique (pas de saut, pas de contradiction)
2. Cohérence numérique (chiffres, pourcentages)
3. Cohérence temporelle (dates, versions, chronologies)
4. Résultat attendu vs obtenu
5. Cohérence entre fichiers
6. Corriger toute incohérence

## §5 — Conventions

- **Nommage** : kebab-case, versions semver (SHARED §1.2)
- **Format rapport** : 5 sections (Étapes 1-5), support multi-cibles, verdict final
- **Verdicts** : PASS / PASS AVEC RÉSERVES / FAIL
- **Worklog** : format SHARED §1.4
"""
write_file(f"{BASE}/correct-work/SKILL.md", CORRECT_WORK_SKILL)

# ============================================================
# 10. correct-work/evals/evals.json
# ============================================================
print("\n[10/11] correct-work/evals/evals.json")
EVALS_CW = {
    "skill": "correct-work",
    "version": "2.4.0",
    "evals": [
        {"id": "CW-mode-projet", "name": "Mode PROJET détecté", "input": "Prompt maître disponible", "expected_mode": "PROJET"},
        {"id": "CW-mode-cible", "name": "Mode CIBLE par défaut", "input": "Vérifie ce skill", "expected_mode": "CIBLE"},
        {"id": "CW-verdict-fail", "name": "FAIL si S1", "input": "Erreur critique S1 trouvée", "expected_verdict": "FAIL"},
        {"id": "CW-verdict-pass", "name": "PASS si 0 S1-S2", "input": "Aucun problème S1-S2", "expected_verdict": "PASS"},
        {"id": "CW-multi-cible", "name": "Support multi-cibles", "input": "Vérifie skill A et B", "expected_targets": 2}
    ]
}
write_file(f"{BASE}/correct-work/evals/evals.json", json.dumps(EVALS_CW, indent=2, ensure_ascii=False))

# ============================================================
# 11. correct-work/scripts/verify-correct-work.py
# ============================================================
print("\n[11/11] correct-work/scripts/verify-correct-work.py")
VERIFY_SCRIPT = r'''#!/usr/bin/env python3
"""verify-correct-work.py — 16 checks post-install pour correct-work v2.4.0."""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.dirname(BASE)

def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not condition else ""))
    return condition

def verify_correct_work():
    print("\n=== Vérification post-installation correct-work v2.4.0 ===")
    passed = 0
    total = 16

    # Check 1: SKILL.md existe
    passed += check("SKILL.md existe", os.path.isfile(f"{BASE}/SKILL.md"))

    # Check 2: Taille SKILL.md (200-350 lignes)
    with open(f"{BASE}/SKILL.md", encoding="utf-8") as f:
        lines = len(f.readlines())
    passed += check(f"Taille SKILL.md ({lines}L, cible 200-350)", 200 <= lines <= 350, f"{lines} lignes")

    # Check 3: YAML frontmatter
    with open(f"{BASE}/SKILL.md", encoding="utf-8") as f:
        content = f.read()
    passed += check("YAML name", "name: correct-work" in content)
    passed += check("YAML version", "version: 2.4.0" in content)
    passed += check("YAML category", "category: ecosystem" in content)
    passed += check("YAML language", "language: fr" in content)
    passed += check("YAML tags", "tags:" in content)
    passed += check("YAML dependencies", "dependencies:" in content)

    # Check 4: 3 modes documentes
    passed += check("Mode PROJET", "PROJET" in content)
    passed += check("Mode CIBLE", "CIBLE" in content)
    passed += check("Mode DIRECT", "DIRECT" in content)

    # Check 5: 5 etapes
    for i in range(1, 6):
        passed += check(f"Etape {i} documentee", f"Etape {i}" in content or f"\u00c9tape {i}" in content)

    # Check 6: Integration KB
    passed += check("Integration KB", "kb_path" in content or "KNOWLEDGE" in content)

    # Check 7: Severite S1-S4
    passed += check("Severite S1", "S1" in content)
    passed += check("Severite S4", "S4" in content)

    # Check 8: Cross-ref gen-plan
    passed += check("Cross-ref gen-plan", "gen-plan" in content and ">=3.6" in content)

    # Check 9: Cross-ref clone-chat
    passed += check("Cross-ref clone-chat", "clone-chat" in content)

    print(f"\nResultat : {passed}/{total} checks PASS")
    return passed == total


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Installation terminee. Lancement des verifications...")
    ok = verify_correct_work()
    sys.exit(0 if ok else 1)
'''
write_file(f"{BASE}/correct-work/scripts/verify-correct-work.py", VERIFY_SCRIPT)

# ============================================================
# VERIFICATION FINALE
# ============================================================
print("\n" + "="*60)
print("INSTALLATION TERMINEE")
print("="*60)

# Liste des fichiers créés
files = []
for root, dirs, filenames in os.walk(BASE):
    for fn in filenames:
        fp = os.path.join(root, fn)
        files.append(fp)

for f in sorted(files):
    size = os.path.getsize(f)
    print(f"  {f} ({size} octets)")

print(f"\nTotal : {len(files)} fichiers crees dans skills/")
