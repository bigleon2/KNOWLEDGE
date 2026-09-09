# Écosystème Knowledge — Architecture & Guide de référence

> **Date** : 2026-08-30
> **Version** : 2.1.1
> **Vérification** : 60/60 checks PASS (`scripts/verify-cross.py`, 6 axes — état courant 2026-09-06) · état historique v2.1.0 (30-08) : 68/68

---

## 1. Vue d'ensemble

L'écosystème Knowledge est un ensemble de **80 skills** conçus pour un assistant IA (9 skills écosystème + 71 skills métier). Chaque skill est auto-contenu dans son répertoire sous `skills/`, dispose d'un fichier `SKILL.md` principal, et peut inclure des références, scripts, évaluations et modèles.

Deux skills — **gen-plan** et **correct-work** — jouent un rôle central : ils sont utilisés dans toutes les discussions pour planifier les tâches et vérifier/corriger le travail produit. Leur cycle d'interaction (gen-plan produit un plan, correct-work le valide) forme le moteur opérationnel de l'écosystème.

---

## 2. Architecture des répertoires

```
my-project/
├── @mon-ecosysteme/                     ← Prompts maîtres — dossier canonique (préfixe « @ » le 2026-09-07 : tri GitHub premier plan ; renommé depuis _prompts-maitres le 2026-08-28)
│   ├── README.md                        ← Le présent guide
│   ├── INSTALL-ECOSYSTEME.md            ← Procédure d'installation (8 phases P0-P7)
│   ├── PROMPT-MAITRE-SHARED.md          ← Socle commun
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.10.0.md ← Version courante
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.9.0.md
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.8.1.md
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.8.0.md
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.7.0.md
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.6.1.md ← Version intermédiaire conservée
│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md ← Version courante
│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.5.0.md
│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md
│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md
│   └── _archive/                        ← Versions obsolètes (8 fichiers, voir _archive/README.md)
├── skills/                              ← Racine de l'écosystème (80 skills)
│   ├── KNOWLEDGE.md                    ← Registre central (source de vérité)
│   ├── _prompts-maitres/               ← Miroir byte-identique de @mon-ecosysteme/ (22 fichiers — préfixe « _ » = infrastructure, pas un skill)
│   │   ├── PROMPT-MAITRE-SHARED.md     ← Socle commun (conventions, KB, matrice)
│   │   ├── PROMPT-MAITRE-GEN-PLAN-v3.7.0.md
│   │   ├── PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md
│   │   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md
│   │   ├── README.md
│   ├── context-engineering/            ← Skill discipline (socle SHARED §7 — déclenchement automatique)
│   │   ├── SKILL.md                    (~130 lignes, version compacte)
│   │   └── evals/                      (evals.json 4 evals + trigger_evals.json 4 cas)
│   ├── loop-engineering/               ← Skill discipline (socle SHARED §7 — déclenchement automatique)
│   │   ├── SKILL.md                    (~130 lignes, version compacte)
│   │   └── evals/                      (evals.json 4 evals + trigger_evals.json 4 cas)
│   ├── graph-engineering/              ← Skill discipline (socle SHARED §7 — déclenchement automatique)
│   │   ├── SKILL.md                    (~130 lignes, version compacte)
│   │   └── evals/                      (evals.json 4 evals + trigger_evals.json 4 cas)
│   ├── harness-engineering/            ← Skill discipline (socle SHARED §7 — déclenchement automatique)
│   │   ├── SKILL.md                    (~130 lignes, version compacte)
│   │   └── evals/                      (evals.json 4 evals + trigger_evals.json 4 cas)
│   ├── gen-plan/                       ← Skill écosystème
│   │   ├── SKILL.md                    (~232 lignes, version compacte — plancher 180-260)
│   │   ├── references/                 (5 fichiers)
│   │   └── evals/                      (evals.json 6 evals + trigger_evals.json 9 cas)
│   ├── correct-work/                   ← Skill écosystème
│   │   ├── SKILL.md                    (~400 lignes)
│   │   ├── scripts/                    (1 script)
│   │   └── evals/                      (evals.json 5 evals + trigger_evals.json 8 cas)
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
│   └── [71 autres skills]/             ← Skills métier (docx, pdf, xlsx, pptx, charts, …)
│       ├── SKILL.md
│       └── [references/, scripts/, evals/, …]
├── download/                            ← Copies de référence (sync via sync-download.py)
└── scripts/
    ├── verify-cross.py                 ← Vérification croisée (84 checks, 9 axes)
    └── sync-download.py                ← Synchronisation download/ ↔ source de vérité
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

| Type de skill | Lignes SKILL.md | Fichiers références | Note |
|---------------|-----------------|-------------------|-------|
| Complexe (gen-plan) | ~180 lignes | 5 fichiers | Le prompt maître (~937 lignes) contient la spec complète et le contenu in extenso des références |
| Moyen (correct-work) | ~315 lignes | scripts/ + evals/ | Le prompt maître (~500 lignes) contient les checklists complètes (§10), historique et notes de conception |
| Simple | < 100 lignes | 0-1 fichier | Pas de prompt maître ; tout le contenu tient dans le SKILL.md |

---

## 6. Conventions écosystème

### Nommage

- **Répertoires** : kebab-case (`gen-plan`, `correct-work`, `clone-chat`)
- **Fichiers** : kebab-case avec extension (`SKILL.md`, `etapes-detaillees.md`, `evals.json`)
- **Versions** : format semver (`3.6.1`, `2.4.0`)
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
gen-plan v3.10.0
├── invoque correct-work >= v2.4.0       (Étape 1 : validation plan + E8 hook + contrôle par phase)
├── utilise clone-chat >= v2.0.0          (E4, E15 : calibration + archivage)
├── consulte skills-inventory >= v1.0.0   (E5 : sélection skills)
└── enrichit KNOWLEDGE.md                 (E15 : mise à jour registre)

correct-work v2.5.1
├── utilise gen-plan >= v3.7.0           (Étape 1 : plan de vérification, optionnel)
├── vérifie clone-chat >= v2.0.0          (Mode CIBLE : §3.5 Context Drift)
└── vérifie fullstack-dev                 (Projets web : structure et dépendances)

clone-chat v2.0.0
├── archivé par gen-plan >= v3.6.1          (Sessions longues, optionnel)
├── vérifié par correct-work              (Validation croisée, §3.5 drift)
└── conventions par skill-creator         (Conventions structurelles)

autonomous-agent v1.0.0
├── utilise gen-plan >= v3.6.0             (Tâches complexes, planification)
├── persist via clone-chat >= v2.0.0       (État Long, inter-sessions, optionnel)
└── vérifié par correct-work >= v2.4.0     (Cohérence agent)
```

### Règles de cross-references

1. La référence dans A inclut la version minimale requise de B
2. B mentionne A dans sa section « Utilisé par » de KNOWLEDGE.md
3. Si A modifie le comportement de B, la relation est documentée dans les deux sens
4. Toute mise à jour de version déclenche une vérification des dépendances

---

## 9. Prompts maîtres — Architecture en 6 fichiers

Les prompts maîtres sont les **spécifications d'installation** pour les skills écosystème. Ils permettent de recréer un skill complet à partir de zéro, de façon autonome.

### Principe SHARED + spécifiques

**SHARED** est le socle commun. Les trois autres fichiers sont les spécifiques. L'info commune (contexte, conventions, variables, relations, matrice) est centralisée dans SHARED (§0 à §6). Les fichiers spécifiques contiennent uniquement la logique propre à leur skill et référencent SHARED via `« voir SHARED §X.X »`. Toute mise à jour d'une info commune se fait **une seule fois**.

### Fichiers

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `PROMPT-MAITRE-SHARED.md` | ~260 | Socle commun. Contexte, conventions, variables, registre KB, 22 relations inter-skills, matrice agent × skill, disciplines d'ingénierie de prompts (source de vérité §7 : 5 disciplines, registre d'assignation, matérialisations). |
| `PROMPT-MAITRE-GEN-PLAN-v3.10.0.md` | ~1113 | Spec complète gen-plan version courante. 4 modes, 15 étapes E1-E15, règles d'or §1.8 (n°1 adaptation autonome, n°2 régénération post-installation, n°3 mise à jour à chaque nouvelle demande), disciplines d'ingénierie §1.9 (orchestration gen-plan — source de vérité : SHARED §7 ; matérialisation : 4 skills à déclenchement automatique), pipeline d'optimisation Z0-Z6 (§1.10), idempotence R1-R6 (§1.11), hook correct-work par phase E9-E14, normes N1-N3, YAML frontmatter, instructions d'installation, evals schéma skill-creator (§5.4-§5.6), contenu in extenso des 5 références + evals. |
| `PROMPT-MAITRE-GEN-PLAN-v3.6.1.md` | ~941 | Spec complète gen-plan version intermédiaire conservée (identique au corpus figé — Annexe B du PDF). |
| `PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md` | ~631 | Spec complète correct-work version courante. 3 modes, 5 étapes, multi-cibles, découplage gen-plan, métriques, checklists unifiées (§10.1-§10.10), evals schéma skill-creator (§5.3-§5.5), historique corrections clone-chat. Versions intermédiaires (v2.4.0, v2.5.0) conservées dans le dossier. |
| `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | ~688 | Spec complète clone-chat. 7+1 étapes, 8 checks validation, 5 types de drift, auto-clonage, protocole d'héritage §1.0, compatibilité ascendante, grille #token, contenu in extenso du template, historique corrections correct-work. |
| `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | ~135 | Pipeline d'installation de l'écosystème (v1.0.0) : ordre d'exécution optimal en 10 étapes (corpus → miroir → gen-plan → correct-work → clone-chat → KB → outillage → certification → publication → clôture), principes de dépendance, critères de passage et arbitres par étape. |

### Structure des fichiers

**SHARED** : §0 (Règle zéro) · §1 (Conventions : variables, nommage, YAML, worklog) · §2 (Registre KB : rôle, template, Protocole de Découverte) · §3 (Relations inter-skills : tableau complet + règles) · §4 (Matrice agent × skill) · §5 (Format SKILL.md) · §6 (Workflow PMs) · §7 (Disciplines d'ingénierie — source de vérité)

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

### Cas E — Synchroniser download/

Après toute modification d'un fichier dans `@mon-ecosysteme/` (source canonique) :

```bash
python3 scripts/sync-download.py --sync
```

Le script compare chaque fichier source avec sa copie dans `download/` et ne copie que les fichiers effectivement modifiés. Le mode CHECK (sans `--sync`) affiche un rapport sans rien écrire. Le miroir `skills/_prompts-maitres/` est ensuite resynchronisé byte-identique depuis la source canonique (le CHECK 6 de `verify-cross.py` signale tout écart).

Le CHECK 6 de `verify-cross.py` signale automatiquement tout écart et rappelle la commande de synchronisation.

---

## 11. Skills écosystème — État actuel

| Skill | Version | Rôle | Fichiers installés |
|-------|---------|------|-------------------|
| gen-plan | v3.10.0 | Planification de tâches (4 modes, 15 étapes, gestion du plan d'actions de session) | SKILL.md (~232 lignes), 5 références, 6 evals + 9 triggers |
| correct-work | v2.5.1 | Vérification et correction (3 modes, S1-S4, multi-cibles) | SKILL.md (~400 lignes), scripts/, 5 evals + 8 triggers |
| clone-chat | v2.0.0 | Clonage de discussion en Markdown | SKILL.md (~310 lignes), 1 référence, 1 prompt maître |
| skills-inventory | v1.0.0 | Scan et inventaire des skills | SKILL.md, 2 evals, scripts |
| skill-creator | v1.0.0 | Création et gestion de skills | SKILL.md, 1 référence, 7 scripts, 3 agents |
| agent-prompt-engineering | v1.0.1 | Optimisation fine des prompts complexes (4 modes) | SKILL.md, 5 evals + 7 triggers, 1 référence |
| context-engineering | v1.0.0 | Discipline context engineering (curation de contexte, compaction, mémoire externe) | SKILL.md, 4 evals + 4 triggers |
| loop-engineering | v1.0.0 | Discipline loop engineering (boucles exécution / vérification / externe) | SKILL.md, 4 evals + 4 triggers |
| graph-engineering | v1.0.0 | Discipline graph engineering (graphe de connaissances, anti-hallucination) | SKILL.md, 4 evals + 4 triggers |
| harness-engineering | v1.0.0 | Discipline harness engineering (harnais d'exécution, gardes-fous, arbitres) | SKILL.md, 4 evals + 4 triggers |
| autonomous-agent | v1.0.0 | Agent autonome avec mémoire interne | SKILL.md, 1 référence |

**Registre KB** : `skills/KNOWLEDGE.md` — 14 entrées : 12 skills écosystème (dont 4 matérialisations skills des disciplines, session A12) + 2 infrastructure (script-mon-ecosysteme-infrastructure v1.0.0, verify-by-sha v1.0.0), 22 relations (SHARED §3.1)

---

## 12. Vérifications

| Vérification | Résultat |
|--------------|----------|
| gen-plan post-installation | 9/9 PASS |
| correct-work post-installation | 16/16 PASS |
| clone-chat post-installation | 16/16 PASS |
| Cross-refs gen-plan ↔ correct-work ↔ clone-chat | PASS |
| Interactions 4 fichiers MD + déclencheurs | PASS |
| `verify-cross.py` (prompts maîtres + sync) | 60/60 PASS (6 axes) |
| `sync-download.py` (scripts Python) | SYNC OK (5/5 fichiers identiques) |
| `integrate-clone-chat-kb-v3.py` | 10/10 checks PASS |

---

## 13. Canal de vérification byte-identique pour tiers (R-1)

Pour permettre à un tiers non-authentifié de vérifier l'authenticité d'un clone de la lignée Knowledge (sans accès au storage endpoint authentifié de la plateforme), un canal de vérification public a été mis en place.

### Principe

1. **Manifeste public** (`data/public-verify/manifest.json`) : indexe tous les clones scellés avec leurs SHAs (brute, scellée, déclarée), tailles, et URLs publiques.
2. **Copies publiques** (`data/public-verify/clones/<name>.md`) : miroir byte-identique des clones scellés, accessible sans authentification.
3. **Script verify-by-sha.py** (`scripts/verify-by-sha.py`) : script Python autonome qui télécharge un clone, applique la méthode de scellement « ligne neutralisée », et compare le SHA scellé calculé à la valeur déclarée.

### Méthode de scellement (rappel)

La méthode « ligne neutralisée » consiste à :
1. Localiser la ligne `**SHA-256** : <64 hex>` dans le clone
2. Remplacer cette ligne par `**SHA-256** : <64 zeros>` (64 zeros exactement)
3. Calculer sha256 du contenu ainsi neutralisé
4. Le résultat doit correspondre au SHA declared dans le fichier ET dans le manifeste

Cette méthode, formalisée à l'Annexe D du PDF « Analyse récursive des discussions Knowledge », élimine la circularité du scellement (un fichier contenant son propre SHA ne peut pas être vérifié byte-identique sans cette neutralisation).

### Usage

```bash
# Vérifier un clone spécifique (par filename)
python3 scripts/verify-by-sha.py ecosysteme-knowledge-clone-2026-09-05-4.md

# Vérifier tous les clones du manifeste
python3 scripts/verify-by-sha.py --manifest data/public-verify/manifest.json

# Vérifier par SHA-256 scellé
python3 scripts/verify-by-sha.py 62dce02fede75cce20ba5fedd6464293da6c26fe450eae2eeefef654ebba0e1c
```

### État au 2026-09-06

- 9 clones indexés dans le manifeste — lignée préservée complète, du GML 2026-08-09
  (`clone-de-gen-plan-3.6-et-ecosystem.md`) au 10ᵉ clone 2026-09-05
  (`ecosystem-knowledge-clone-2026-09-05-5.md`) ; le maillon 0 (322 lignes, 09-08) reste
  perdu, statut assumé et documenté
- 5 AUTHENTIC (6ᵉ → 10ᵉ — scellés après enrichissement, SHA déclarée ≡ recalcul neutral-line)
- 3 HISTORICAL_ENRICHED (GML, C, D — SHA déclarée calculée sur la version initiale scellée,
  fichier enrichi ensuite ; artefact documenté, non défaut de sécurité — convention §3.3-30)
- 1 UNKNOWN (B — pré-protocole de scellement, aucune ligne neutral-line ; identité ancrée par
  la SHA brute e05587ea…, documentée worklog A2 et 10ᵉ clone §3.4)
- Recalcul neutral-line conforme aux valeurs du manifeste pour les 9 (méthode Annexe D du PDF)
