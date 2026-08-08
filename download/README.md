# Prompts Maîtres — Écosystème Knowledge

> **Architecture en 3 fichiers + workflow**
>
> - **Date** : 2026-08-09
> - **Version** : 1.0.0
> - **Vérification** : 55/55 checks PASS (`scripts/verify-cross.py`)

---

## 1. Fichiers

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `PROMPT-MAITRE-SHARED.md` | ~216 | Socle commun de l'écosystème. Contexte, conventions, variables d'installation, registre KB, relations inter-skills, matrice agent × skill. |
| `PROMPT-MAITRE-GEN-PLAN-v3.6.0.md` | ~866 | Spécification complète du skill **gen-plan** v3.6.0. 4 modes, 15 étapes E1-E15, normes N1-N3, YAML frontmatter, instructions d'installation, contenu in extenso des 5 fichiers référence + evals. |
| `PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md` | ~490 | Spécification complète du skill **correct-work** v2.3.0. 3 modes, 5 étapes, sévérité S1-S4, checklists unifiées (§10.1-§10.10), historique corrections clone-chat. |

---

## 2. Principe d'architecture

**SHARED** est le « socle ». Les deux autres fichiers sont les « spécifiques ».

Avant le refactoring (v1), chaque prompt maître dupliquait ~15-20 % de contenu identique (contexte écosystème, conventions, variables, relations, matrice agent × skill). En cas de modification d'une info commune, il fallait la reporter dans chaque fichier.

Après le refactoring (v2) :

- L'info commune est centralisée dans **SHARED** (§0 à §6)
- Les fichiers spécifiques contiennent uniquement la logique propre à leur skill et font référence à SHARED via des renvois (ex : « voir SHARED §1.2 »)
- Toute mise à jour d'une info commune se fait **une seule fois**

Réduction mesurée : les 3 fichiers totalisent ~1572 lignes, avec une maintenance simplifiée et un risque d'incohérence réduit.

---

## 3. Structure de chaque fichier

### PROMPT-MAITRE-SHARED.md

- **§0** — Règle zéro (contexte écosystème, principes fondamentaux)
- **§1** — Conventions écosystème
  - §1.1 Variables d'installation (`{{SKILLS_ROOT}}`, `{{KB_PATH}}`, etc.)
  - §1.2 Conventions de nommage (kebab-case, semver, tags)
  - §1.3 Conventions YAML frontmatter (template minimum)
  - §1.4 Format worklog (format partagé)
- **§2** — Registre KB (KNOWLEDGE.md)
  - §2.1 Rôle
  - §2.2 Format d'une entrée (template)
  - §2.3 Protocole de Découverte
- **§3** — Registre des relations inter-skills
  - §3.1 Tableau complet des relations
  - §3.2 Règles de cross-references
- **§4** — Matrice agent × skill (statique)
  - §4.1 Matrice principale
  - §4.2 Légende des droits
- **§5** — Format du fichier SKILL.md (conventions structurelles)
- **§6** — Prompt maîtres : architecture et workflow

### PROMPT-MAITRE-GEN-PLAN-v3.6.0.md

- **§A** — Déclencheurs
- **§B** — Prérequis (référence SHARED)
- **§1** — Spécification fonctionnelle (4 modes, 15 étapes, N1-N3)
- **§2** — Spécification technique (stack, auto-calibration, profils, KB)
- **§3** — Relations (extrait SHARED §3.1)
- **§4** — YAML frontmatter
- **§5** — Instructions d'installation
- **§6** — Vérification post-installation (9 checks)
- **§7** — Historique des versions
- **§8** — Notes de conception
- **§9** — Contenu in extenso des 5 fichiers référence + evals

### PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md

- **§A** — Déclencheurs
- **§B** — Prérequis (référence SHARED)
- **§1** — Spécification fonctionnelle (3 modes, 5 étapes, KB)
- **§2** — Spécification technique (rapport, matrices, sévérité S1-S4)
- **§3** — Relations (extrait SHARED §3.1)
- **§4** — YAML frontmatter
- **§5** — Instructions d'installation
- **§6** — Vérification post-installation (16 checks)
- **§7** — Historique des versions
- **§8** — Historique des corrections clone-chat (3 rounds)
- **§9** — Notes de conception
- **§10** — Checklists unifiées (par mode + opérationnelles)

---

## 4. Workflow d'utilisation

### Cas A — Installer un skill depuis zéro

1. Lire `PROMPT-MAITRE-SHARED.md` en premier
2. Lire le prompt maître du skill cible (gen-plan ou correct-work)
3. Suivre les « Instructions d'installation » (§5 du fichier spécifique)
4. Créer la structure de répertoires
5. Créer le fichier `SKILL.md` en assemblant :
   - Le YAML frontmatter (§4)
   - La règle zéro (SHARED §0, adaptée en résumé)
   - La spec fonctionnelle et technique (§1-§2)
   - Les relations (§3 + SHARED §3)
   - Les sections spécifiques (checklists, grilles, etc.)
6. Créer les fichiers de référence (si applicable, §9 in extenso)
7. Exécuter les checks de vérification post-installation
8. Mettre à jour `KNOWLEDGE.md` (SHARED §2.2 template)
9. Mettre à jour les cross-references (SHARED §3.2)

### Cas B — Mettre à jour une info commune

1. Modifier l'info dans `PROMPT-MAITRE-SHARED.md` (une seule fois)
2. Vérifier que les références dans les fichiers spécifiques pointent toujours vers la bonne section
3. Relancer la vérification croisée si disponible

### Cas C — Ajouter un nouveau prompt maître (ex : clone-chat)

1. Créer `PROMPT-MAITRE-CLONE-CHAT-vX.Y.Z.md`
2. Le faire dépendre de SHARED (préfixe PRÉREQUIS identique)
3. Remplir les sections propres au skill
4. Référencer SHARED pour tout ce qui est commun
5. Ajouter les relations dans SHARED §3.1
6. Mettre à jour la matrice SHARED §4.1 si nécessaire
7. Lancer la vérification croisée

### Cas D — Vérifier la cohérence des 3 fichiers

1. Lancer le script : `python3 scripts/verify-cross.py`
2. Vérifier que tous les checks sont PASS
3. Corriger les FAILs éventuels

---

## 5. Relations de dépendance entre fichiers

```
SHARED.md
├── lu par GEN-PLAN (références §0, §1.1, §1.2, §2.2, §2.3, §3, §3.1)
└── lu par CORRECT-WORK (références §0, §1.1, §1.2, §1.4, §2.2, §2.3, §3, §3.1, §4, §4.1)

GEN-PLAN v3.6.0
├── dépend de SHARED
├── référence correct-work >= v2.3.0 (à E1)
├── référence clone-chat >= v1.2.0 (E1-E7, E4, E15)
└── référence skills-inventory >= v1.0.0 (E5)

CORRECT-WORK v2.3.0
├── dépend de SHARED
├── référence gen-plan >= v3.6.0 (Étape 1)
├── référence clone-chat >= v1.2.0 (Mode CIBLE)
└── référence fullstack-dev (projets web)
```

---

## 6. Notes

- Les numéros de version dans les noms de fichiers correspondent aux versions des skills, pas des prompts : gen-plan v3.6.0, correct-work v2.3.0.
- SHARED n'a pas de numéro de version skill car ce n'est pas un skill, c'est un socle de référence commun.
- Le contenu in extenso des fichiers référence de gen-plan (§9) est inclus dans le prompt maître pour permettre l'installation autonome sans avoir à consulter d'autres sources.
- La vérification croisée (`scripts/verify-cross.py`) valide 5 axes : pas de duplication, références SHARED cohérentes, relations bidirectionnelles, aucune info perdue, tailles conformes.

---

## 7. Intégration dans l'écosystème

**Date d'intégration** : 2026-08-09

### Skills installés

```
skills/gen-plan/
├── SKILL.md                          (172 lignes, version compacte)
├── references/                       (5 fichiers)
│   ├── etapes-detaillees.md
│   ├── grille-token.md
│   ├── classification-types.md
│   ├── profils-ressource.md
│   └── guide-selection-agent-skill.md
└── evals/
    └── evals.json                    (5 evals)

skills/correct-work/
└── SKILL.md                          (128 lignes, version compacte)
```

### Registre KB

```
skills/KNOWLEDGE.md                   (5 skills écosystème, 10 relations)
```

### Prompts maîtres (copies de travail)

```
skills/_prompts-maitres/
├── PROMPT-MAITRE-SHARED.md
├── PROMPT-MAITRE-GEN-PLAN-v3.6.0.md
├── PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md
└── README.md
```

### Vérifications effectuées

| Vérification | Résultat |
|--------------|----------|
| gen-plan post-installation | 9/9 PASS |
| correct-work post-installation | 16/16 PASS |
| Cross-refs gen-plan ↔ correct-work | PASS |
| Interactions 3 fichiers MD + déclencheurs | PASS |
| `verify-cross.py` (prompts maîtres) | 55/55 PASS |

**Total fichiers intégrés** : 11 fichiers
