# Écosystème Knowledge — Architecture & Guide de référence

> **Date** : 2026-10-12
> **Version** : 2.1.8
> **Architecture** : v2.2 — SHARED v1.7.8 — Contexte Système 3 niveaux
> **Révision v2.1.9 (2026-10-23, Task 22 — session web-fdf5963c, directive propriétaire gen-plan(step) « analyse pipeline d'installation + disciplines/techniques »)** : refactor-guard v1.7.1→v1.8.0 (§1.9bis apports de veille 2025-2026 : golden master AVANT + mutation testing léger + rollback automatique armé — 12 disciplines/techniques enrichies, agent-creator v2.2.0 dérive critique résorbée) ; PM REFACTOR-GUARD v1.8.0 généré mécaniquement KO-L004, v1.7.1 archivé @historique/prompts-maitres/refactor-guard/ (SHA scellé) ; PM-INSTALL v1.8.0→v1.8.1 (F1 anti-faux-succès rc propagé + F2 exclusion __pycache__ + F3 vérification post-install SHA-256 embarquée) ; SHARED v1.7.9 ; arborescence §2 recalibrée.
> **Révision v2.1.8 (2026-10-23, Task 18 — session web-fdf5963c, directive propriétaire « optimise le système d'installation en regénérant » + skill alias-eco)** : 4 PMs familles régénérés mécaniquement KO-L004 (GEN-PLAN v3.23.2, CORRECT-WORK v2.8.0 — intégration alias-eco mode PROJET, CLONE-CHAT v2.0.2, REFACTOR-GUARD v1.7.1 — note §5 mécanisme dual) ; PM-INSTALL v1.8.0 (MÉCANISME DUAL : installation directe des formes certifiées par défaut — exécutant canonique eco_install_pipeline.py ; assemblage bootstrap ; périmètre += alias-eco §2bis/§4/§A.3) ; SHARED v1.7.8 ; skill alias-eco v1.0.0 créé (registre d'alias $<ALIAS>, déclencheurs « alias-eco »/« liste mes alias »/« alias-eco (chat) », registre @historique/@Alias/) ; KB 34 entrées ; cascade KO-L004 : propagate v1.7.8 (100 skills + 69 scripts + 2 agents), ULTRA régénéré, arbitres recalibrés, archive rescellée round-trip 9/9 ; arborescence §2 recalibrée.
> **Révision v2.1.7 (2026-10-12, Task 12 — directive propriétaire « appliquer les corrections », session web-b4d7dd19, gen-plan(step))** : clone-chat v2.0.0→v2.0.1 (dependencies += skill-creator conventions — F-c1, §5.2 item 8 modèle PM-§7 — F-c2), v2.0.0 archivé `@historique/prompts-maitres/clone-chat/` (git mv byte-identité R4) ; refactoring-engineering v1.1.1 (§5 baseline A2 MESURÉE 7/7 — F1/F3, plancher ref-test >=1.0.1 — F4) ; refactoring-test v1.0.2 (§5 baseline — F2) ; entrées §6 rétrospectives ×5 disciplines (F-d1..F-d5) ; SHARED v1.7.7 (§7 dé-figage pins n°53 — F-e, §6.1) ; PM-INSTALL v1.7.1 (§2ter/§A.3) ; cascade KO-L004 : propagate v1.7.7 (98 skills + 65 scripts + 2 agents), ULTRA régénéré (4 familles + routes refactoring + ECO_SKILLS dérivée KB + date non figée — F5/F6), arbitres recalibrés (integrity ECO_SKILLS, task17, task9), archive rescellée round-trip 9/9 ; arborescence §2 recalibrée (clone-chat v2.0.1, PM-INSTALL v1.7.1, archives gen-plan×19 + clone-chat×1 — ×18 stale résorbé).
> **Révision v2.1.6 (2026-10-12, directive propriétaire PM-INSTALL — session web-b4d7dd19, gen-plan(step))** : PM-INSTALL v1.7.0 — étape 6 refactor-guard au pipeline (10→11 étapes, 4e famille D009 désormais installée depuis le corpus), périmètre COMPLET explicite (formes installées de toutes les entrées KB — 8 disciplines n°54/n°55 + outil refactoring-test + refactor-guard), fermeture MINIMALE étendue +6 éléments, §A.3 extensions +6 entrées + instantané courant, socle §2ter +1 ligne (refactoring-test-graph.py) ; cascade KO-L004 : SHARED v1.7.6 (§3.2/§6.1), ULTRA régénéré (11 étapes), propagate v1.7.6 (98 skills + 65 scripts + 2 agents), SYNC-CONTEXT v1.4.8, archive rescellée round-trip 9/9 ; arborescence §2 recalibrée.
> **Révision v2.1.5 (cascade gen-plan v3.23.1, session web-b4d7dd19 Task 8 gen-plan(step) — fusion discussion externe 468a4c26)** : PM GEN-PLAN v3.23.1 vivant (correction outil n°55 — refactoring-test = outil de la discipline refactoring-engineering, directive propriétaire), v3.23.0 archivé (19 PMs GEN-PLAN) ; SHARED v1.7.4 (§7 : outil + registre ×3 lignes), PM-INSTALL v1.6.4 ; KB 32 entrées (+refactor-guard v1.7.0 garde-fous, +fullstack-dev — fusion 468a4c26 ; n°55 corrigées) ; propagation §0 v1.7.4 (idempotent ×2) ; arborescence §2 recalibrée.
> **Révision v2.1.4 (cascade gen-plan v3.23.0, session web-b4d7dd19 Task 7 gen-plan(step))** : recalibrage état — PM GEN-PLAN v3.23.0 vivant (matérialisation des disciplines de refactoring n°55 : refactoring-engineering + refactoring-test — directive propriétaire), v3.22.1 archivé `@historique/` (18 PMs GEN-PLAN) ; SHARED v1.7.3 (§6.1 + §7 n°55), PM-INSTALL v1.6.3 (§2ter/§A.3) ; KB 30 entrées (2 n°55 + réciproques) ; propagation §0 ×97+51+2 (idempotent ×2) ; arborescence §2 recalibrée.
> **Révision v2.1.3 (cascade gen-plan v3.22.1, session web-b4d7dd19)** : recalibrage état — PM GEN-PLAN v3.22.1 vivant (renommage du mode step-confirm → step-ok + clause mode NULL — directive propriétaire), v3.22.0 archivé `@historique/` (17 PMs GEN-PLAN) ; SHARED v1.7.2 (§6.1), PM-INSTALL v1.6.2 (§2ter/§A.3) ; arborescence §2 recalibrée.
> **Révision v2.1.2 (cascade gen-plan v3.22.0, session web-b4d7dd19)** : recalibrage état — PM GEN-PLAN v3.22.0 vivant (orchestration matérialisations n°54 + déclencheurs de mode step/step-confirm), v3.21.0 archivé `@historique/` (16 PMs GEN-PLAN) ; §7 SHARED : « Définitions des 5 disciplines » → « 5 + 3 matérialisations n°54 » (SHARED v1.7.0, discussion parente 5ef6176f) ; arborescence §2 recalibrée.
> **Révision v2.1.1 (Task 16)** : déduplication des prompts maîtres (directive propriétaire « ne garder que la dernière version ») — le corpus `@mon-ecosysteme/` ne porte plus que les PMs sources (GEN-PLAN v3.21.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0) + socle ; les 19 PMs historiques sont archivés dans le nouveau dossier `skills/@historique/` (byte-identité SHA-256 scellée, distillation des particularités/améliorations/avantages par version) ; arborescence §2 recalibrée.
> **Révision v2.1.0 (Task 14)** : décision d'architecture v2.2 — canal de fichiers `download/` supprimé (déduplication, le corpus est publié uniquement via l'archive d'intégrité `download/mon-ecosysteme_archive.zip`) ; `sync-download.py` retiré de l'outillage, remplacé par la garde `scripts/task14-scan-doublons.py` ; arborescence et commandes recalibrées (certification-complete.py ajouté) ; drift SHARED §6.1 (GEN-PLAN v3.12.0 → v3.18.0) résorbé au passage.

---

## 1. Vue d'ensemble

L'écosystème Knowledge est un ensemble de **86 skills** conçus pour un assistant IA (9 skills écosystème + 71 skills métier + 6 skills de discipline — dont la discipline de refactoring n°55 refactoring-engineering (refactoring-test = son outil, non discipline — Task 8) ; + refactor-guard (garde-fous) et fullstack-dev inscrits au registre, fusion discussion 468a4c26).

### Principes fondamentaux

1. **Autonomie** : Chaque skill est auto-porteur avec son Contexte Système embarqué
2. **Décentralisation** : Le contenu spécifique est dans les skills, pas dans le SHARED
3. **Vérification** : Scripts d'arbitres pour valider la cohérence
4. **Traçabilité** : Références 📎 pour retrouver le contenu décentralisé

---

## 2. Architecture des répertoires

```
KNOWLEDGE/
├── @mon-ecosysteme/                     ← Prompts maîtres (Niveau 1) — dernières versions seules (Task 16)
│   ├── README.md                        ← Ce guide
│   ├── PROMPT-MAITRE-SHARED.md          ← Socle commun (source de vérité)
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.23.2.md
│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md
│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.2.md
│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md  ← 4e famille (décision D009)
│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md  ← Installation (source unique v1.8.0 — pipeline 11 étapes, mécanisme dual)
│   ├── PROMPT-ULTRA-MAITRE-ORCHESTRATION.md ← Orchestration à l'usage (généré idempotent v1.0.0)
│   └── SYNC-CONTEXT.md                  ← Procédure de synchronisation
│
├── @historique/                         ← Archive des versions historiques des PMs et skills (Task 16)
│   ├── README.md                        ← Objet, règles de conservation (byte-identité R2, unicité R4)
│   ├── historiques-par-skill/{gen-plan,correct-work,clone-chat}.md ← Historique par skill (Task 17-B)
│   ├── historique-autres-elements.md ← Historique du socle non-PM (Task 17-B)
│   └── prompts-maitres/{gen-plan×19, correct-work×4, clone-chat×1} ← PMs historiques déplacés (byte-identité scellée)
│
├── skills/                              ← Skills métier (Niveau 2)
│   ├── gen-plan/
│   ├── correct-work/
│   ├── clone-chat/
│   ├── skill-creator/
│   ├── autonomous-agent/
│   ├── context-engineering/
│   ├── loop-engineering/
│   ├── graph-engineering/
│   ├── harness-engineering/
│   └── ...
│
├── scripts/                             ← Scripts d'arbitres (Niveau 3)
│   ├── verify-cross.py
│   ├── verify-correct-work.py
│   ├── verify-by-sha.py
│   ├── spell-check.py
│   ├── check-ecosysteme-integrity.py
│   ├── certification-complete.py
│   ├── task14-scan-doublons.py
│   ├── sync-context-block.py
│   ├── propagate-context.py
│   ├── install-ecosystem.py
│   └── back-depot.py
│
├── config.json                          ← Configuration centralisée
└── .gitignore                           ← Fichiers ignorés
```

---

## 3. Les 3 niveaux de Contexte Système

### Niveau 1 : Bloc complet (Prompts maîtres)
- **Cibles** : 6 fichiers `PROMPT-MAITRE-*.md`
- **Contenu** : Règle Zéro + Variables + Conventions (complet)
- **Position** : Après le frontmatter, avant §A
- **Taille** : ~1 250 caractères

### Niveau 2 : Bloc compact (Skills et Agents)
- **Cibles** : 84 `SKILL.md` + N fichiers `.agent`
- **Contenu** : 3 lignes (Variables, Conventions, Règle Zéro)
- **Position** : `§0 — Contexte Système` (après frontmatter)
- **Taille** : ~400 caractères

### Niveau 3 : En-tête commenté (Scripts Python)
- **Cibles** : 9 scripts `.py`
- **Contenu** : 3 lignes en docstring
- **Position** : Après le shebang, avant le code
- **Taille** : ~250 caractères

---

## 4. Workflow d'utilisation

> **⚠️ NOTE (Architecture v2.0)** : Les prompts maîtres sont **auto-porteurs**. Le contexte système est embarqué directement dans chaque fichier. Aucune lecture externe n'est requise.

1. **Invoquer le prompt maître souhaité**
2. **Le contexte est automatiquement chargé** via le bloc embarqué
3. **Suivre les instructions** du fichier spécifique
4. **Utiliser les scripts** pour vérifier la cohérence

---

## 5. Décentralisation du SHARED

Les informations spécifiques à un skill ont été extraites du SHARED et intégrées directement dans les fichiers concernés.

### Sections décentralisées

| Section SHARED | Fichier destination | Référence |
| :--- | :--- | :--- |
| §1.3 YAML frontmatter | `skill-creator/SKILL.md §2` | 📎 Décentralisé |
| §1.4 Worklog | `autonomous-agent/SKILL.md §2.1` | 📎 Décentralisé |
| §2.2 Template entrées KB | `skills-inventory/SKILL.md §2.1` | 📎 Décentralisé |
| §2.3 Protocole Découverte | `skills-inventory/SKILL.md §2.2` | 📎 Décentralisé |
| §3.2 Cross-references | `correct-work/SKILL.md §3` | 📎 Décentralisé |
| §4 Matrice agents | `autonomous-agent/SKILL.md §2.2` | 📎 Décentralisé |
| §5 Format SKILL.md | `skill-creator/SKILL.md §3` | 📎 Décentralisé |

### Sections conservées dans le SHARED

- §0 : Règle Zéro
- §1.1 : Variables d'installation
- §1.2 : Conventions de nommage
- §2.1 : Rôle du registre KB
- §3.1 : Tableau complet des relations
- §6 : Architecture des prompts maîtres
- §7 : Définitions des 5 disciplines + 3 matérialisations n°54 (SHARED v1.7.0)

---

## 6. Scripts d'arbitres

### Scripts de vérification

```bash
# Vérification croisée des relations
python scripts/verify-cross.py --check-context

# Vérification des outputs correct-work
python scripts/verify-correct-work.py

# Vérification par empreinte SHA
python scripts/verify-by-sha.py --generate  # Première exécution
python scripts/verify-by-sha.py              # Vérifications suivantes

# Vérification orthographique
python scripts/spell-check.py
```

### Scripts de propagation

```bash
# Propagation du Contexte Système à tous les fichiers
python scripts/propagate-context.py

# Synchronisation après évolution du SHARED
python scripts/sync-context-block.py --level all
```

### Scripts d'infrastructure

```bash
# Installation complète de l'écosystème
python scripts/install-ecosystem.py

# Certification complète (orchestrateur des 5 arbitres)
python scripts/certification-complete.py

# Garde anti-doublons download/ (décision v2.2 — 0 doublon attendu)
python scripts/task14-scan-doublons.py

# Backup du dépôt
python scripts/back-depot.py
```

---

## 7. Procédure de synchronisation

Voir `SYNC-CONTEXT.md` pour la procédure détaillée.

**Commande rapide** :
```bash
python scripts/sync-context-block.py --level all
```

---

## 8. Configuration centralisée

Le fichier `config.json` à la racine contient toutes les variables globales :

```json
{
  "ecosystem": {
    "name": "Knowledge",
    "version": "2.0.0",
    "skills_root": "skills/",
    "kb_path": "skills/KNOWLEDGE.md"
  },
  "context_system": {
    "enabled": true,
    "shared_version": "1.5.2",
    "levels": { ... }
  }
}
```

---

## 9. Installation

```bash
# Cloner le dépôt
git clone https://github.com/bigleon2/KNOWLEDGE.git
cd KNOWLEDGE

# Exécuter le script d'installation
python scripts/install-ecosystem.py

# Vérifier l'installation
python scripts/verify-cross.py --check-context
```

---

## 10. Correction de l'écosystème

Pour exécuter la correction complète de l'écosystème :

```bash
# Exécution complète
corrige-ecosysteme

# Ou phase par phase
corrige-ecosysteme:phase-A
corrige-ecosysteme:phase-B
...
corrige-ecosysteme:phase-I
```

**Durée estimée** : 3h30
**Résultat** : Écosystème stable, autonome, vérifiable

---

*Fin du README.md v2.1.1*
