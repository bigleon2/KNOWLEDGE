# Écosystème Knowledge — Architecture & Guide de référence

> **Date** : 2026-08-09
> **Version** : 2.0.0
> **Vérification** : 60/60 checks PASS (`scripts/verify-cross.py`)

---

## 1. Vue d'ensemble

L'écosystème Knowledge est un ensemble de **78 skills** conçus pour un assistant IA (6 skills écosystème + 72 skills métier). Chaque skill est auto-contenu dans son répertoire sous `skills/`, dispose d'un fichier `SKILL.md` principal, et peut inclure des références, scripts, évaluations et modèles.

Deux skills — **gen-plan** et **correct-work** — jouent un rôle central : ils sont utilisés dans toutes les discussions pour planifier les tâches et vérifier/corriger le travail produit. Leur cycle d'interaction (gen-plan produit un plan, correct-work le valide) forme le moteur opérationnel de l'écosystème.

---

## 2. Architecture des répertoires

```
my-project/
├── skills/                              ← Racine de l'écosystème (78 skills)
│   ├── KNOWLEDGE.md                    ← Registre central (source de vérité)
│   ├── _prompts-maitres/               ← Specs d'installation des skills écosystème
│   │   ├── PROMPT-MAITRE-SHARED.md     ← Socle commun (conventions, KB, matrice)
│   │   ├── PROMPT-MAITRE-GEN-PLAN-v3.6.0.md
│   │   ├── PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md
│   │   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md
│   │   └── README.md
│   ├── gen-plan/                       ← Skill écosystème
│   │   ├── SKILL.md                    (~195 lignes, version compacte)
│   │   ├── references/                 (5 fichiers)
│   │   └── evals/evals.json            (5 evals)
│   ├── correct-work/                   ← Skill écosystème
│   │   └── SKILL.md                    (129 lignes, version compacte)
│   ├── clone-chat/                     ← Skill écosystème
│   │   ├── SKILL.md
│   │   └── references/                 (1 fichier)
│   ├── skills-inventory/               ← Skill écosystème
│   │   ├── SKILL.md
│   │   ├── evals/                      (2 fichiers)
│   │   └── scripts/
│   ├── skill-creator/                  ← Skill écosystème
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   └── agents/
│   └── [72 autres skills]/             ← Skills métier (docx, pdf, xlsx, pptx, charts, …)
│       ├── SKILL.md
│       └── [references/, scripts/, evals/, …]
├── download/                            ← Copies de référence des prompts maîtres
└── scripts/
    └── verify-cross.py                 ← Vérification croisée (60 checks, 6 axes)
```

---

## 3. Principes fondamentaux

| Principe | Description |
|----------|-------------|
| **Versionnage semver** | Chaque skill versionné MAJEUR.MINEUR.PATCH (ex : `3.6.0`) |
| **Dépendances déclarées** | Versions minimales dans le YAML frontmatter (`>= v2.3.0`) |
| **Cross-references bidirectionnelles** | Si A référence B, alors B mentionne A dans KB |
| **Registre KB unique** | `KNOWLEDGE.md` est la source de vérité pour l'état de l'écosystème |
| **Conventions uniformes** | kebab-case, préfixe `§` pour les sections, `#token` pour les budgets |
| **Design compact** | SKILL.md = résumé opérationnel ; le prompt maître contient la spec complète |

---

## 4. Registre KB (`KNOWLEDGE.md`)

`KNOWLEDGE.md` est le **registre central** de l'écosystème. Il contient :

- La liste de tous les skills avec leurs versions, catégories et statuts
- Les dépendances inter-skills (bidirectionnelles)
- Les métadonnées de calibration
- L'historique des interactions entre skills

### Template d'une entrée

```markdown
## [nom-skill] v[X.Y.Z]

- **Category** : [category]
- **Description** : [description courte]
- **Dépend de** : [liste des skills et versions min]
- **Utilisé par** : [liste des skills qui utilisent celui-ci]
- **Dernière calibration** : [date ou N/A]
- **Statut** : [stable | expérimental | en cours]
```

### Protocole de Découverte

Quand un skill doit identifier les skills pertinents pour une tâche :
1. Scanner les entrées de `KNOWLEDGE.md` par catégorie et tags
2. Filtrer par compatibilité de version
3. Vérifier les dépendances croisées
4. Produire une liste ordonnée des skills candidats

---

## 5. Structure type d'un skill

```
skills/[nom-skill]/
├── SKILL.md                  ← Fichier principal (obligatoire)
├── references/               ← Fichiers de référence (optionnel)
├── evals/evals.json          ← Évaluations (optionnel)
├── scripts/                  ← Scripts utilitaires (optionnel)
└── templates/                ← Templates (optionnel)
```

### Fichier SKILL.md — Structure type

1. **YAML frontmatter** (obligatoire) : nom, version, category, tags, description, dépendances
2. **§0 — Règle zéro** : contexte écosystème (résumé de SHARED §0)
3. **§1 — Spécification fonctionnelle** : modes, étapes, normes propres au skill
4. **§2 — Spécification technique** : stack, structure fichiers, intégrations
5. **§3 — Relations** : extrait de SHARED §3.1 pour les relations directes
6. **Sections spécifiques** : grilles de vérification, checklists, grilles #token, etc.
7. **§N — Conventions** : nommage (SHARED §1.2), règles propres

### Tailles cibles (design compact)

| Type de skill | Lignes SKILL.md | Fichiers references | Note |
|---------------|-----------------|-------------------|-------|
| Complexe (gen-plan) | ~195 lignes | 5 fichiers | Le prompt maître (~912 lignes) contient la spec complète et le contenu in extenso des références |
| Moyen (correct-work) | ~130 lignes | 0 fichier | Le prompt maître (490 lignes) contient les checklists complètes (§10) |
| Simple | < 100 lignes | 0-1 fichier | Pas de prompt maître ; tout le contenu tient dans le SKILL.md |

---

## 6. Conventions écosystème

### Nommage

- **Répertoires** : kebab-case (`gen-plan`, `correct-work`, `clone-chat`)
- **Fichiers** : kebab-case avec extension (`SKILL.md`, `etapes-detaillees.md`, `evals.json`)
- **Versions** : format semver (`3.6.0`, `2.3.0`)
- **Tags budget** : préfixe `#` pour les tokens (`#token 3500`)
- **Variables** : double accolades (`{{SKILLS_ROOT}}`)
- **Sections** : préfixe `§` pour toutes les sections (`§1.2`, `§3.1`)

### Variables d'installation

| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine du répertoire des skills |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Chemin vers le registre KB |
| `{{KB_ENABLED}}` | `true` | Activation/désactivation du registre KB |
| `{{PROFILE_DEFAULT}}` | `NORMAL` | Profil ressource par défaut |

### Format worklog (partagé par tous les agents)

```markdown
---
Task ID: [task-id]
Agent: [nom-agent] [version]
Task: [description de la tâche]

Work Log:
- [action concrète 1]
- [action concrète 2]

Stage Summary:
- [résultats clés / décisions / artefacts produits]
```

---

## 7. Matrice agent × skill

Cette matrice définit quels agents peuvent utiliser quels skills et dans quel contexte.

| Agent | gen-plan | correct-work | clone-chat | skills-inventory | fullstack-dev | KB |
|-------|----------|-------------|------------|-----------------|---------------|-----|
| **Main** | Planification complète | Vérification finale | Archivage sessions | Consultation | Développement web | Lecture/écriture |
| **Subagent** | Exécution étapes | Vérification ciblée | Non | Non | Développement délégué | Lecture seule |
| **gen-plan (E1)** | — | Validation plan | Non | Scan skills | Non | Consultation |
| **correct-work (E1)** | Création plan | — | Vérification | Non | Vérification | Scan dynamique |
| **clone-chat** | Non | Non | — | Non | Non | Lecture seule |

**Légende détaillée** : voir SHARED §4.2

**Résumé** : Planification complète = E1-E15 · Exécution = E9-E14 sans E15 · Vérification finale = mode PROJET · Vérification ciblée = mode CIBLE/DIRECT · Scan dynamique = vérifie versions via KB · Lecture/écriture = accès complet au registre

---

## 8. Relations inter-skills

### Graphique de dépendances

```
gen-plan v3.6.0
├── invoque correct-work >= v2.3.0       (Étape 1 : validation plan)
├── utilise clone-chat >= v2.0.0          (E1-E7, E4, E15 : calibration + archivage)
├── consulte skills-inventory >= v1.0.0   (E5 : sélection skills)
└── enrichit KNOWLEDGE.md                 (E15 : mise à jour registre)

correct-work v2.3.0
├── utilise gen-plan >= v3.6.0           (Étape 1 : plan de vérification)
├── vérifie clone-chat >= v2.0.0          (Mode CIBLE : §3.5 Context Drift)
└── vérifie fullstack-dev                 (Projets web : structure et dépendances)

clone-chat v2.0.0
├── archivé par gen-plan >= v3.6.0          (Sessions longues, optionnel)
├── vérifié par correct-work              (Validation croisée, §3.5 drift)
└── conventions par skill-creator         (Conventions structurelles)

autonomous-agent v1.0.0
├── utilise gen-plan >= v3.6.0             (Tâches complexes, planification)
├── persist via clone-chat >= v2.0.0       (État Long, inter-sessions, optionnel)
└── vérifié par correct-work >= v2.3.0     (Cohérence agent)
```

### Règles de cross-references

1. La référence dans A inclut la version minimale requise de B
2. B mentionne A dans sa section « Utilisé par » de KNOWLEDGE.md
3. Si A modifie le comportement de B, la relation est documentée dans les deux sens
4. Toute mise à jour de version déclenche une vérification des dépendances

---

## 9. Prompts maîtres — Architecture en 4 fichiers

Les prompts maîtres sont les **spécifications d'installation** pour les skills écosystème. Ils permettent de recréer un skill complet à partir de zéro, de façon autonome.

### Principe SHARED + spécifiques

**SHARED** est le socle commun. Les trois autres fichiers sont les spécifiques. L'info commune (contexte, conventions, variables, relations, matrice) est centralisée dans SHARED (§0 à §6). Les fichiers spécifiques contiennent uniquement la logique propre à leur skill et référencent SHARED via `« voir SHARED §X.X »`. Toute mise à jour d'une info commune se fait **une seule fois**.

### Fichiers

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `PROMPT-MAITRE-SHARED.md` | ~220 | Socle commun. Contexte, conventions, variables, registre KB, relations inter-skills, matrice agent × skill. |
| `PROMPT-MAITRE-GEN-PLAN-v3.6.0.md` | ~912 | Spec complète gen-plan. 4 modes, 15 étapes E1-E15, normes N1-N3, YAML frontmatter, instructions d'installation, contenu in extenso des 5 références + evals. |
| `PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md` | ~490 | Spec complète correct-work. 3 modes, 5 étapes, sévérité S1-S4, checklists unifiées (§10.1-§10.10), historique corrections clone-chat. |
| `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | ~520 | Spec complète clone-chat. 7+1 étapes, 8 checks validation, 5 types de drift, auto-clonage, grille #token, contenu in extenso du template, historique corrections correct-work.

### Structure des fichiers

**SHARED** : §0 (Règle zéro) · §1 (Conventions : variables, nommage, YAML, worklog) · §2 (Registre KB : rôle, template, Protocole de Découverte) · §3 (Relations inter-skills : tableau complet + règles) · §4 (Matrice agent × skill) · §5 (Format SKILL.md) · §6 (Workflow PMs)

**GEN-PLAN** : §A (Déclencheurs) · §B (Prérequis SHARED) · §1-§2 (Spec fonctionnelle + technique) · §3 (Relations) · §4 (YAML frontmatter) · §5 (Installation) · §6 (Vérification 9 checks) · §7 (Historique) · §8 (Notes conception) · §9 (Contenu in extenso 5 références + evals)

**CORRECT-WORK** : §A (Déclencheurs) · §B (Prérequis SHARED) · §1-§2 (Spec fonctionnelle + technique) · §3 (Relations) · §4 (YAML frontmatter) · §5 (Installation) · §6 (Vérification 16 checks) · §7 (Historique) · §8 (Historique corrections clone-chat) · §9 (Notes conception) · §10 (Checklists unifiées)

**CLONE-CHAT** : §A (Déclencheurs) · §B (Prérequis SHARED) · §1-§2 (Spec fonctionnelle + technique) · §3 (Relations) · §4 (YAML frontmatter) · §5 (Installation) · §6 (Vérification 16 checks) · §7 (Historique) · §8 (Notes conception) · §9 (Contenu in extenso template) · §10 (Historique corrections correct-work)

---

## 10. Workflows

### Cas A — Installer un skill écosystème depuis zéro

1. Lire `PROMPT-MAITRE-SHARED.md` en premier
2. Lire le prompt maître du skill cible
3. Suivre les instructions d'installation (§5 du fichier spécifique)
4. Créer la structure de répertoires (`SKILL.md`, `references/`, `evals/`)
5. Assembler `SKILL.md` : YAML frontmatter + règle zéro + spec + relations + sections spécifiques
6. Créer les fichiers de référence (contenu in extenso depuis §9)
7. Exécuter les checks de vérification post-installation
8. Mettre à jour `KNOWLEDGE.md` (template SHARED §2.2)
9. Mettre à jour les cross-references (règles SHARED §3.2)

### Cas B — Mettre à jour une info commune

1. Modifier l'info dans `PROMPT-MAITRE-SHARED.md` (une seule fois)
2. Vérifier que les références dans les fichiers spécifiques pointent toujours vers la bonne section
3. Relancer `python3 scripts/verify-cross.py`

### Cas C — Ajouter un nouveau prompt maître

1. Créer le fichier (ex : `PROMPT-MAITRE-CLONE-CHAT-vX.Y.Z.md`)
2. Le faire dépendre de SHARED (préfixe PRÉREQUIS identique)
3. Remplir les sections propres au skill
4. Référencer SHARED pour tout ce qui est commun
5. Ajouter les relations dans SHARED §3.1
6. Mettre à jour la matrice SHARED §4.1 si nécessaire
7. Lancer `python3 scripts/verify-cross.py`

### Cas D — Vérifier la cohérence

```bash
python3 scripts/verify-cross.py
```

Le script valide **6 axes** (60 checks) :
1. Pas de duplication entre SHARED et les spécifiques
2. Références SHARED cohérentes dans les fichiers spécifiques
3. Relations bidirectionnelles respectées
4. Aucune information perdue par rapport à la v1
5. Tailles des SKILL.md conformes au design compact
6. Synchronisation download/ vs source de vérité

---

## 11. Skills écosystème — État actuel

| Skill | Version | Rôle | Fichiers installés |
|-------|---------|------|-------------------|
| gen-plan | v3.6.0 | Planification de tâches (4 modes, 15 étapes) | SKILL.md (~195 lignes), 5 références, 5 evals |
| correct-work | v2.3.0 | Vérification et correction (3 modes, S1-S4) | SKILL.md (129 lignes) |
| clone-chat | v2.0.0 | Clonage de discussion en Markdown | SKILL.md (365 lignes), 1 référence, 1 prompt maître |
| skills-inventory | v1.0.0 | Scan et inventaire des skills | SKILL.md, 2 evals, scripts |
| skill-creator | v1.0.0 | Création et gestion de skills | SKILL.md, 1 référence, 7 scripts, 3 agents |
| autonomous-agent | v1.0.0 | Agent autonome avec mémoire interne | SKILL.md, 1 référence |

**Registre KB** : `skills/KNOWLEDGE.md` — 6 skills écosystème, 13 relations bidirectionnelles

---

## 12. Vérifications

| Vérification | Résultat |
|--------------|----------|
| gen-plan post-installation | 9/9 PASS |
| correct-work post-installation | 16/16 PASS |
| clone-chat post-installation | 16/16 PASS |
| Cross-refs gen-plan ↔ correct-work ↔ clone-chat | PASS |
| Interactions 4 fichiers MD + déclencheurs | PASS |
| `verify-cross.py` (prompts maîtres) | [à relancer — 3 S2 corrigés dans cette session] |