#!/usr/bin/env python3
"""
integrate-clone-chat-kb-v2.py — Intègre clone-chat v1.2.0 dans une base de connaissance
locale en utilisant le Protocole de Découverte KB (gen-plan v3.3.0+).

Usage :
    python integrate-clone-chat-kb-v2.py <kb_path> [--register] [--verify] [--full]

Options :
    --register    Enregistrer clone-chat dans le registre KB (KNOWLEDGE.md)
    --verify      Vérifier la compatibilité avec les skills KB existants
    --full        Exécuter toutes les étapes (scan + install + register + verify)

Exemples :
    python integrate-clone-chat-kb-v2.py "C:\\Users\\PC\\Downloads\\knowledge\\skills" --full
    python integrate-clone-chat-kb-v2.py "/home/user/knowledge/skills" --full
    python integrate-clone-chat-kb-v2.py "/home/user/knowledge/skills" --register
    python integrate-clone-chat-kb-v2.py "/home/user/knowledge/skills" --verify

Ce script implémente le Protocole de Découverte KB de gen-plan v3.3.0 :
    1. Scanner le répertoire KB pour découvrir les skills existants
    2. Construire la liste de référence (baseline ecosysteme)
    3. Extraire les métadonnées de chaque skill (YAML frontmatter)
    4. Classifier les skills (exécutable, référence, agent)
    5. Construire le registre dynamique fusionné
    6. Évaluer la compatibilité (dépendances inter-skills)
    7. Installer clone-chat v1.2.0 dans la KB
    8. Enregistrer clone-chat dans le registre KB (KNOWLEDGE.md)

Auteur : François + gen-plan v3.5.0
Version : 2.0.0
Date : 2026-07-29
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime


# ─── Constantes ───────────────────────────────────────────────────────────────

CLONE_CHAT_VERSION = "1.2.0"
CLONE_CHAT_CATEGORY = "ecosystem"
CLONE_CHAT_LANGUAGE = "fr"
CLONE_CHAT_TAGS = ["clonage", "discussion", "memoire", "prompt-maitre", "transfert-contexte"]

# Skills de l'écosystème connus (baseline)
ECOSYSTEM_BASELINE = {
    "gen-plan": {"version": "3.3.0", "category": "ecosystem", "type": "executable"},
    "correct-work": {"version": "2.2.0", "category": "ecosystem", "type": "executable"},
}


# ─── Contenu SKILL.md ───────────────────────────────────────────────────────

SKILL_MD = r'''---
name: clone-chat
aka: clone-chat-skill, chat-cloner, discussion-clone
version: 1.2.0
date: 2026-07-29
authors: [Francois]
language: fr
category: ecosystem
tags: clonage, discussion, memoire, prompt-maitre, transfert-contexte
description: >
  Clone l'intégralité d'une discussion (contexte, décisions, artefacts, worklog)
  dans un fichier Markdown auto-suffisant. En exécutant ce clone dans une nouvelle
  session, l'assistant IA recrée le contexte complet de la discussion originale.
---

# clone-chat v1.2.0 — Clonage de Discussions

## Vue d'ensemble

clone-chat est un skill de capture et de transfert de contexte. Exécuté à la fin d'une discussion, il produit un **artefact de clonage** (fichier Markdown) qui contient tout le nécessaire pour recréer cette discussion dans une nouvelle session.

**Cas d'usage** :
- Poursuivre une discussion longue dans une nouvelle session sans perdre le contexte
- Transférer le contexte d'un projet à un autre assistant IA
- Archiver l'état d'une discussion pour la reprendre plus tard
- Créer un "snapshot" avant une itération risquée

## Format de sortie

**Fichier unique** : `<slug>-clone-<date>.md` dans le répertoire de téléchargement

Le format Markdown est choisi car :
1. **Universel** — lisible par tout assistant IA, tout éditeur de texte
2. **Auto-suffisant** — un seul fichier contient tout le contexte
3. **Exécutable** — l'assistant IA peut interpréter le contenu comme un prompt
4. **Versionnable** — Git-friendly, diff-friendly
5. **Pas de dépendance** — pas besoin de ZIP, de scripts, ou d'outils externes

## 7+1 Étapes d'exécution

### Étape 1 — Collecte du worklog

Lire le worklog intégralement. C'est la source primaire de l'historique de la discussion.

**Action** :
- Lire le worklog complet
- Identifier chaque Task ID et son résumé
- Extraire la chronologie des sessions

**Livrable** : Chronologie structurée de la discussion

### Étape 2 — Collecte des artefacts

Scanner les répertoires pour identifier tous les fichiers produits pendant la discussion :

| Répertoire | Ce qu'il contient |
|------------|-------------------|
| `skills/` | Skills créés ou modifiés |
| `scripts/` | Scripts Python persistants |
| `download/` | Livrables finaux |
| `upload/` | Fichiers sources |

**Action** :
- Lister les fichiers pertinents créés/modifiés pendant la discussion
- Pour chaque fichier SKILL.md, lire le contenu (c'est le cœur du skill)
- Pour les scripts, noter le nom et la version (pas le contenu complet si > 500 lignes)

**Livrable** : Inventaire des artefacts avec chemins et tailles

### Étape 3 — Extraction des décisions clés

Analyser le worklog et les messages de la discussion pour identifier :

- **Décisions de l'utilisateur** — Ce que l'utilisateur a explicitement choisi ou refusé
- **Corrections de bugs** — Les problèmes rencontrés et leurs fixes
- **Conventions établies** — Les règles et standards adoptés pendant la discussion
- **Arbitrages** — Les choix entre plusieurs options (ex: MD vs DOCX, v2.0 vs v3.5)

**Action** :
- Pour chaque décision : qui, quoi, pourquoi, conséquence
- Pour chaque bug : description, cause, fix, résultat
- Pour chaque convention : nom, règle, exemple

**Livrable** : Table structurée des décisions et conventions

### Étape 3.5 — Détection des évolutions de contexte (Context Drift)

**Objectif** : Identifier chaque fois que le contexte a **changé** durant la discussion — c'est-à-dire quand une décision, une spécification, une convention ou un paramètre a été modifié, inversé, corrigé ou enrichi par rapport à un état antérieur.

**Pourquoi cette étape ?** L'Étape 3 capture les décisions dans leur état **final**. Mais une discussion longue peut contenir des inversions, des corrections, des recalibrages. Sans traçage de ces évolutions, le clone perd l'historique des **pourquoi** et des **comment** le contexte a évolué.

**Méthode de détection** :
1. Relire le worklog chronologiquement (session par session)
2. Pour chaque Task ID, comparer les décisions/specs avec les sessions précédentes
3. Identifier les deltas : quand une valeur A est devenue B
4. Catégoriser le type de drift
5. Enregistrer la référence (session #, ligne worklog)

**5 types de drift** :

| Type | Définition | Exemple |
|------|-----------|---------|
| INVERSION | Décision renversée | v2.0.0 accepté → refusé (Session 2) |
| MODIFICATION | Décision ajustée | in extenso < 500 lignes → < 200 lignes |
| CORRECTION | Spécification ou décision erronée corrigée | convention chemins absolus → relatifs |
| ENRICHISSEMENT | Décision complétée | grille #token ajoutée |
| RECALIBRAGE | Paramètre ajusté | seuil -32% → -35% |

**Format de chaque drift** :
```
| # | Type | Avant | Après | Session | Ligne worklog | Raison |
```

**Règles** :
- Un drift est enregistré **uniquement** si un changement effectif est détecté (pas de drift si la décision est restée stable)
- La ligne worklog est le numéro de ligne dans le worklog où le changement est documenté
- Si le worklog ne contient pas de ligne explicite pour le changement, indiquer la session # et la mention « (inféré) »
- Les bugs corrigés (§3.2) sont exclus du drift — ils ont leur propre section. Le drift capture les **décisions et specs** qui ont évolué, pas les erreurs techniques
- Si aucun drift n'est détecté, écrire : « Aucune évolution de contexte détectée — toutes les décisions sont restées stables. » Cette mention certifie que l'analyse a été effectuée

**Livrable** : Table §3.5 des évolutions de contexte avec références de lignes

### Étape 4 — Extraction des spécifications techniques

Pour chaque skill, script, ou artefact technique identifié, capturer :

- **Spécification fonctionnelle** — Ce que ça fait, les étapes, les modes
- **Spécification technique** — Stack, dépendances, formats, structures de données
- **Données de calibration** — Grilles #token, seuils, ratios ajustés
- **Structure de fichiers** — Arborescence avec noms de fichiers

**Règle** : Le contenu des SKILL.md est inclus **en résumé structuré** (description, étapes, modes, fichiers). Pour les scripts Python > 500 lignes, inclure uniquement la signature des fonctions/classes et les structures de données clés. L'inclusion in extenso est réservée aux skills < 200 lignes ; au-delà, le résumé structuré garantit un clone lisible et de taille raisonnable.

**Intégration gen-plan** : Si gen-plan est présent dans l'écosystème, utiliser ses données de classification (E1-E7) et de calibration (E15) pour enrichir les spécifications techniques :
- Profils ressource (NORMAL / ECO / VIEUX PC) détectés
- Grilles #token calibrées par gen-plan
- Types de tâche (Type 1-4) déjà classifiés
- Auto-calibration (estimé vs réel) pour ajuster les données du clone

**Livrable** : Spécifications techniques complètes

### Étape 5 — Assemblage du clone

Assembler l'artefact de clonage en suivant le template `references/clone-template.md`.

**Structure obligatoire du clone** (suivre `references/clone-template.md`) :

```
En-tête     — Métadonnées (date, source, sessions, participants)
§0 — RÈGLE ZÉRO — Contexte perdu, tout à recréer
§1 — CHRONOLOGIE — Sessions résumées (table + détails)
§2 — ÉCOSYSTÈME — Skills, scripts, artefacts (spécifications incluses)
§3 — DÉCISIONS — Décisions clés, bugs, conventions, calibration, drifts (§3.5)
§4 — INSTRUCTIONS — Comment utiliser ce clone
§5 — AUTO-CLONAGE — Instructions pour que le clone se clone lui-même
```

**Note** : l'En-tête et les artefacts (§2.3) sont intégrés dans les sections existantes, pas des sections numérotées séparément.

**Règles d'assemblage** :
- Le clone doit être **auto-suffisant** : aucune dépendance externe
- Le clone doit être **exécutable** : l'assistant IA peut l'interpréter comme un prompt
- Le clone doit être **idempotent** : l'exécuter plusieurs fois produit le même résultat
- Le clone doit être **auto-référentiel** : il contient les instructions pour se régénérer

### Étape 6 — Validation du clone

Vérifier que le clone est complet et fonctionnel :

| # | Vérification | Critère |
|---|-------------|---------|
| 1 | Auto-suffisance | Aucune référence à un fichier externe non-inclus |
| 2 | Complétude worklog | Tous les Task IDs du worklog sont documentés |
| 3 | Complétude skills | Tous les skills créés/modifiés sont spécifiés |
| 4 | Complétude décisions | Toutes les décisions utilisateur sont capturées |
| 5 | Complétude bugs | Tous les bugs corrigés sont documentés |
| 6 | Complétude drifts | Toutes les évolutions de contexte détectées sont dans §3.5 |
| 7 | Exécutabilité | Le clone peut être interprété comme un prompt |
| 8 | Auto-clonage | Le clone contient les instructions pour se régénérer |

**Action** : Cocher chaque vérification. Si une vérification échoue, compléter le clone.

### Étape 7 — Sauvegarde et rapport

1. Sauvegarder le clone dans le répertoire de téléchargement
2. Mettre à jour le worklog avec le résumé du clonage
3. Afficher le rapport de validation à l'utilisateur

**Format du nom de fichier** :
- `<slug>` = résumé de la discussion en 2-3 mots kebab-case (ex: `skills-ecosysteme-dj`)
- `<date>` = YYYY-MM-DD (ex: `2026-07-29`)
- Exemple : `skills-ecosysteme-dj-clone-2026-07-29.md`

## Mode d'emploi du clone

### Comment utiliser un clone dans une nouvelle session

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu du fichier clone (ou indiquer le chemin)
3. Dire : **« Exécute le clone de discussion »**
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant fait avec le clone

1. Lit la section RÈGLE ZÉRO
2. Reconstruit les fichiers spécifiés dans ÉCOSYSTÈME
3. Applique les décisions et conventions de la section DÉCISIONS
4. Crée les artefacts listés dans ARTEFACTS
5. Se positionne à l'état exact de la fin de la discussion originale

### Propriété d'auto-clonage

Le clone contient (§5 — AUTO-CLONAGE) les instructions pour se régénérer. Ainsi :
- À la fin de la nouvelle session, le clone peut être régénéré
- Le nouveau clone contient le contexte de la discussion originale + la nouvelle discussion
- Le clone "grandit" à chaque session sans perdre l'historique

## Relation avec l'écosystème

| Skill | Relation | Détail |
|-------|----------|--------|
| gen-plan (v3.5.0) | **Orchestration amont** | gen-plan peut invoquer clone-chat comme sous-tâche (Type 4, Python natif). clone-chat utilise les données de classification gen-plan (E1-E7) et de calibration (E15) pour enrichir les spécifications techniques du clone. |
| gen-plan (v3.3.0 KB) | **Référence de compatibilité** | La v3.3.0 introduit le Registre de Skills KB et le protocole de découverte dynamique. clone-chat exploite ce registre pour documenter les skills KB dans §2. |
| correct-work | **Validation croisée** | clone-chat peut être vérifié par correct-work (Mode CIBLE). Réciproquement, clone-chat capture les corrections dans §3.5 (Context Drift). |
| skill-creator | **Conventions** | clone-chat suit les conventions de skill-creator (YAML frontmatter, structure de fichiers, nommage). |

**Flux de données entre gen-plan et clone-chat** :

```
gen-plan E1-E7 (classification)  →  clone-chat Étape 4 (spécifications enrichies)
gen-plan E4 (scan KB)            →  clone-chat Étape 2 (artefacts KB détectés)
gen-plan E15 (auto-calibration)  →  clone-chat Étape 3.5 (drift de recalibrage)
clone-chat (clone produit)       →  gen-plan E4 (lecture du clone si ré-exécution)
```

**Dépendance gen-plan** : clone-chat fonctionne **sans** gen-plan (données de calibration absentes), mais **avec** gen-plan les spécifications sont enrichies.

## Grille d'Estimation #token

| Mode d'exécution | #token Estimé | Profil Min. |
|------------------|---------------|-------------|
| Discussion courte (< 5 sessions) | 2000-3500 | ECO |
| Discussion moyenne (5-15 sessions) | 3500-5500 | NORMAL |
| Discussion longue (> 15 sessions) | 5500-9000 | NORMAL |

**Note v1.2.0** : l'estimation est augmentée de ~10% pour couvrir l'Étape 3.5 (Context Drift) et l'intégration gen-plan.

**Note** : l'estimation couvre les 7+1 étapes de collecte, assemblage et validation. Le clone produit est un fichier Markdown, pas un appel d'agent.

## Limites connues

1. **Pas de capture des messages bruts** — clone-chat capture le contexte, pas le verbatim
2. **Scripts longs** — Les scripts > 500 lignes sont résumés, pas inclus in extenso
3. **Fichiers binaires** — Les images, ZIP, PDF ne sont pas inclus dans le clone (chemins uniquement)
4. **Contexte implicite** — Les sous-entendus non documentés dans le worklog peuvent être perdus
5. **Taille** — Un clone de discussion très longue peut dépasser 1000 lignes. **Mitigation** : (a) résumer les sessions anciennes, (b) détail §1.3 pour les 5-10 dernières, (c) skills stables en 1 ligne
6. **Drift inféré** — Si le worklog ne documente pas explicitement un changement, le drift est marqué « (inféré) »
7. **gen-plan optionnel** — Sans gen-plan, les données de calibration et les drifts de recalibrage ne sont pas détectés

## Structure Fichiers

```
skills/clone-chat/
├── SKILL.md                    (ce fichier)
└── references/
    └── clone-template.md       (template de structure du clone)
```

## Historique des Versions

| Version | Date | Changements |
|---------|------|-------------|
| v1.0.0 | 2026-07-29 | Version initiale, 7 étapes, format Markdown |
| v1.1.0 | 2026-07-29 | correct-work : numérotation §0-§5 harmonisée, grille #token ajoutée, règle in extenso clarifiée, mitigation taille, ref section 8 corrigée |
| v1.2.0 | 2026-07-29 | Étape 3.5 Context Drift (5 types de drift avec réf. lignes worklog), intégration gen-plan v3.5.0+v3.3.0 KB, validation 8 checks, grille #token +10%, limites drift inféré + gen-plan optionnel |
'''


# ─── Contenu clone-template.md ──────────────────────────────────────────────

CLONE_TEMPLATE_MD = r'''# Template de Clone — clone-chat v1.2.0

Ce template définit la structure obligatoire d'un artefact de clonage produit par le skill `clone-chat`.

---

## Structure du fichier clone

```markdown
# CLONE DE DISCUSSION — <titre>

> **Date du clone** : YYYY-MM-DD
> **Source** : Discussion entre <utilisateur> et <assistant>
> **Sessions couvertes** : N sessions (du YYYY-MM-DD au YYYY-MM-DD)
> **Version clone-chat** : 1.2.0

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

<Contexte matériel cible si pertinent>

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### 1.1 Résumé global

<Résumé en 3-5 phrases de la discussion complète>

### 1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | ... | ... | ... |

### 1.3 Détail par session

Pour chaque session :
- Objectif
- Actions réalisées
- Résultats
- Bugs corrigés (si applicable)

---

## §2 — ÉCOSYSTÈME DE SKILLS

### 2.1 Skills créés ou modifiés

Pour chaque skill :
- Nom, version, description courte
- Spécification fonctionnelle (étapes, modes, règles)
- Spécification technique (stack, dépendances, formats)
- Structure de fichiers
- Contenu SKILL.md (in extenso si < 200 lignes, sinon résumé structuré)

### 2.2 Scripts créés ou modifiés

Pour chaque script :
- Nom, version, description courte
- Signature des fonctions/classes principales
- Structures de données clés
- Chemin d'accès

### 2.3 Artefacts produits

| Fichier | Taille | Description |
|---------|--------|-------------|
| ... | ... | ... |

---

## §3 — DÉCISIONS CLÉS

### 3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | ... | ... | ... |

### 3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | ... | ... | ... | ... |

### 3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| ... | ... | ... |

### 3.4 Données de calibration

<Grilles #token, seuils, ratios ajustés — si applicable>

### 3.5 Évolutions de contexte (Context Drift)

Cette section trace chaque fois que le contexte a **changé** durant la discussion. Chaque évolution est catégorisée et référencée par session et ligne du worklog.

**5 types de drift** :

| Type | Définition |
|------|-----------|
| INVERSION | Décision renversée (A accepté → A refusé) |
| MODIFICATION | Décision ajustée (paramètre X → Y) |
| CORRECTION | Spécification ou décision erronée corrigée (valeur fausse → valeur correcte) |
| ENRICHISSEMENT | Décision complétée (ajout d'un élément nouveau) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibré) |

**Table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | ... | ... | ... | ... | ... | ... |

**Règles de remplissage** :
- Chaque drift DOIT référencer la session # et la ligne du worklog où le changement est documenté
- Si le worklog ne contient pas de ligne explicite, indiquer la session # et la mention « (inféré) »
- Les bugs corrigés (§3.2) sont exclus du drift — ils ont leur propre section
- Le drift capture les **décisions et specs** qui ont évolué, pas les erreurs techniques
- Si aucun drift n'est détecté, écrire : « Aucune évolution de contexte détectée — toutes les décisions sont restées stables. »

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire

1. Lire §0 (Règle zéro)
2. Reconstruire les fichiers spécifiés dans §2
3. Appliquer les décisions et conventions de §3
4. Créer les artefacts listés dans §2.3
5. Se positionner à l'état exact de la fin de la discussion originale

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra :
   - Tout le contexte de ce clone (discussion originale)
   - Tout le nouveau contexte de la discussion en cours
3. Le nouveau clone remplace ce fichier
4. Le clone "grandit" à chaque session sans perdre l'historique

**Mécanisme** : les sections §1-§3 (incluant §3.5 Context Drift) sont enrichies avec les nouvelles sessions.
Les sections §0, §4-§5 sont régénérées à l'identique (auto-référentielles).
```

---

## Règles de remplissage

| Section | Source principale | Complétude requise |
|---------|------------------|-------------------|
| §0 | Fixe (toujours identique) | 100% |
| §1 | worklog.md | 100% des Task IDs |
| §2 | skills/, scripts/, download/ | 100% des fichiers créés |
| §3.1-3.4 | worklog.md + messages | 100% des décisions utilisateur |
| §3.5 | worklog.md (comparaison chronologique) | 100% des drifts détectés |
| §4 | Fixe (toujours identique) | 100% |
| §5 | Fixe (auto-référentiel) | 100% |

## Règles de validation

- Le clone ne doit contenir **aucune référence** à un fichier non-inclus dans le clone
- Si un contenu est trop long (> 500 lignes), le résumer avec les signatures et structures clés
- Les chemins de fichiers doivent être **relatifs** (pas de chemins absolus)
- Les sections fixes (§0, §4, §5) sont identiques à chaque clone
- La section §3.5 (Context Drift) est obligatoire même si vide — elle certifie que l'analyse de drift a été effectuée
- Si gen-plan est présent dans l'écosystème, les drifts de recalibrage (E15) sont automatiquement inclus dans §3.5
'''


# ─── Contenu KNOWLEDGE.md ────────────────────────────────────────────────────

KNOWLEDGE_MD_TEMPLATE = r'''# Knowledge Base — Registre de Skills

> **Dernière mise à jour** : {date}
> **Chemin KB** : `C:\Users\PC\Downloads\knowledge\skills`
> **Protocole** : gen-plan v3.3.0 — Registre KB avec Protocole de Découverte

---

## Configuration du Registre KB

| Paramètre | Valeur |
|-----------|--------|
| **Chemin KB (Windows)** | `C:\Users\PC\Downloads\knowledge\skills` |
| **Chemin z.ai (Linux)** | `/home/z/my-project/skills/` |
| **Scan depth** | 2 niveaux (racine + 1 sous-dossier) |
| **Fichier detect** | `SKILL.md` ou tout `.md` avec YAML frontmatter (name, description) |
| **Priorité** | Les skills KB sont évalués APRES les skills écosystème z.ai |
| **Overlap** | Si un skill KB a le même nom qu'un skill écosystème, le skill **écosystème** est prioritaire sauf override explicite |

---

## Skills KB Enregistrés

| Skill | Version | Catégorie | Type | Langue | Dépendances | Compatibilité |
|-------|---------|-----------|------|--------|-------------|---------------|
| gen-plan | 3.3.0 | ecosystem | Exécutable | fr | Aucune | OK (orchestrateur) |
| correct-work | 2.2.0 | ecosystem | Exécutable | fr | gen-plan >=3.1.0 | OK (requiert gen-plan >=3.1.0, intégré Registre KB v3.3.0) |
| clone-chat | 1.2.0 | ecosystem | Exécutable | fr | gen-plan (optionnel) | OK (enrichi si gen-plan présent, standalone sinon) |

---

## Détail des Skills KB

### gen-plan v3.3.0

**Catégorie** : ecosystem
**Langue** : fr
**Description** : Planification et orchestration multi-étapes de tâches complexes. Analyse la conversation/projet, décompose en sous-tâches, sélectionne l'agent ou skill optimal pour chaque phase, et exécute en mode série. V3.3.0 : registre de skills personnalisé (knowledge base), protocole de découverte dynamique, scan automatique des skills externes à l'Étape 4.
**Chemin** : `skills/gen-plan/SKILL.md`
**Tags** : planification, orchestration, routage, ressources, execution
**Déclencheurs** : `gen-plan:`, `plan d'actions`, `orchestre`

### correct-work v2.2.0

**Catégorie** : ecosystem
**Langue** : fr
**Description** : Vérification et correction du travail réalisé. 5 étapes systématiques, 3 modes (PROJET/CIBLE/DIRECT). Intégration gen-plan v3.3.0+ avec CoT+Chaining. V2.2.0 : registre KB, protocole de découverte, paramètre kb_path.
**Chemin** : `skills/correct-work/SKILL.md`
**Tags** : verification, correction, quality-gate, validation, gen-plan
**Dépendances** : gen-plan >=3.1.0
**Déclencheurs** : `vérifie ton travail`, `correct_work`, `verify_work`

### clone-chat v1.2.0

**Catégorie** : ecosystem
**Langue** : fr
**Description** : Clone l'intégralité d'une discussion (contexte, décisions, artefacts, worklog) dans un fichier Markdown auto-suffisant. En exécutant ce clone dans une nouvelle session, l'assistant IA recrée le contexte complet de la discussion originale.
**Chemin** : `skills/clone-chat/SKILL.md`
**Tags** : clonage, discussion, memoire, prompt-maitre, transfert-contexte
**Dépendances** : gen-plan (optionnel, pour enrichir les spécifications)
**Relations** : gen-plan v3.5.0 (orchestration amont), gen-plan v3.3.0 KB (Registre KB, protocole de découverte), correct-work (validation croisée), skill-creator (conventions)
**Déclencheurs** : `clone-chat`, `cloner la discussion`, `exécuter le clone`

---

## Matrice de Compatibilité

| Skill | gen-plan | correct-work | clone-chat |
|-------|----------|--------------|------------|
| gen-plan | — | correct-work l'appelle (Étape 1) | clone-chat utilise ses données (E1-E7, E15) |
| correct-work | requiert >=3.1.0 | — | peut vérifier clone-chat (Mode CIBLE) |
| clone-chat | optionnel (enrichit specs) | optionnel (validation croisée) | — |

---

## Flux de Données Inter-Skills

```
gen-plan E1-E7 (classification)  →  clone-chat Étape 4 (spécifications enrichies)
gen-plan E4 (scan KB)            →  clone-chat Étape 2 (artefacts KB détectés)
gen-plan E15 (auto-calibration)  →  clone-chat Étape 3.5 (drift de recalibrage)
clone-chat (clone produit)       →  gen-plan E4 (lecture du clone si ré-exécution)
correct-work (Mode CIBLE)        →  clone-chat vérifié
correct-work (corrections)       →  clone-chat §3.5 (Context Drift)
```

---

## Règle de Priorité

1. Si l'utilisateur spécifie explicitement un skill KB (`gen-plan: utiliser le skill X de ma KB`), le skill KB est prioritaire.
2. Si un skill KB et un skill écosystème ont le même nom, le skill **écosystème** est prioritaire (sauf override explicite).
3. Si aucun skill écosystème ne correspond mais un skill KB correspond, le skill KB est utilisé.
4. Les skills KB sont toujours évalués après les skills écosystème dans la matrice de décision.
'''


# ─── Protocole de Découverte KB ──────────────────────────────────────────────

def extract_yaml_frontmatter(content: str) -> dict:
    """Extrait le YAML frontmatter d'un contenu Markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    yaml_text = match.group(1)
    metadata = {}
    for line in yaml_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            # Nettoyer les guillemets
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Nettoyer les listes
            if value.startswith('[') and value.endswith(']'):
                value = value[1:-1]
            # Nettoyer le > YAML
            if value.startswith('>'):
                value = value[1:].strip()
            metadata[key] = value

    return metadata


def classify_skill(metadata: dict, content: str) -> str:
    """Classifie un skill selon son contenu.

    Returns:
        'executable' — Protocole complet avec étapes et checklist
        'reference' — Document de référence, template, configuration
        'agent' — Définit un agent avec capacités spécifiques
    """
    content_lower = content.lower()

    # Heuristiques pour classifier
    has_steps = bool(re.search(r'étape|etape|step|checklist|protocole', content_lower))
    has_triggers = bool(re.search(r'déclencheur|declencheur|trigger|mot-clé|mot-cle', content_lower))
    has_agent = bool(re.search(r'agent spécialisé|agent specialise|agent.*capacité|capacit.*agent', content_lower))

    if has_agent:
        return 'agent'
    elif has_steps or has_triggers:
        return 'executable'
    else:
        return 'reference'


def scan_kb(kb_path: str) -> list:
    """Scanne le répertoire KB pour découvrir les skills existants.

    Implémente le Protocole de Découverte KB (gen-plan v3.3.0) :
    1. Scanner le répertoire KB
    2. Construire la liste de référence (baseline écosystème)
    3. Extraire les métadonnées (YAML frontmatter)
    4. Classifier les skills
    5. Construire le registre dynamique
    6. Évaluer la compatibilité

    Returns:
        Liste de dicts avec les métadonnées de chaque skill
    """
    kb = Path(kb_path)
    if not kb.exists():
        print(f"⚠️  Le répertoire KB n'existe pas : {kb_path}")
        return []

    skills = []

    # Étape 1 : Scanner le répertoire KB
    for item in sorted(kb.iterdir()):
        if not item.is_dir():
            continue

        # Chercher SKILL.md
        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            # Chercher tout .md avec YAML frontmatter
            for md_file in item.glob("*.md"):
                content = md_file.read_text(encoding="utf-8", errors="replace")
                metadata = extract_yaml_frontmatter(content)
                if "name" in metadata:
                    skill_md = md_file
                    break

        if not skill_md.exists():
            continue

        # Étape 3 : Extraire les métadonnées
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        metadata = extract_yaml_frontmatter(content)

        if not metadata.get("name"):
            continue

        # Étape 4 : Classifier
        skill_type = classify_skill(metadata, content)

        # Étape 2 : Tagger écosystème vs KB
        skill_name = metadata.get("name", "")
        source = "Ecosysteme" if skill_name in ECOSYSTEM_BASELINE else "KB"

        skill_info = {
            "name": skill_name,
            "version": metadata.get("version", "0.0.0"),
            "category": metadata.get("category", "unknown"),
            "language": metadata.get("language", "unknown"),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", ""),
            "type": skill_type,
            "source": source,
            "path": str(skill_md),
            "requires": metadata.get("requires_gen_plan_version", metadata.get("requires", "")),
        }

        skills.append(skill_info)

    return skills


def evaluate_compatibility(skills: list, new_skill: dict) -> list:
    """Évalue la compatibilité d'un nouveau skill avec les skills existants.

    Returns:
        Liste de dicts avec les résultats de compatibilité
    """
    results = []

    for skill in skills:
        compat = {
            "skill": skill["name"],
            "version": skill["version"],
            "compatible": True,
            "details": "",
        }

        # Vérifier les dépendances
        if new_skill["name"] == "clone-chat":
            # clone-chat dépend optionnellement de gen-plan
            if skill["name"] == "gen-plan":
                compat["details"] = "clone-chat utilise gen-plan (optionnel) pour enrichir les spécifications"
            elif skill["name"] == "correct-work":
                compat["details"] = "clone-chat peut être vérifié par correct-work (Mode CIBLE)"
            else:
                compat["details"] = "Aucune interaction directe"

        elif skill["name"] == "correct-work":
            if skill.get("requires"):
                compat["details"] = f"requiert gen-plan {skill['requires']}"

        results.append(compat)

    return results


# ─── Installation ─────────────────────────────────────────────────────────────

def install_clone_chat(kb_path: str) -> bool:
    """Installe clone-chat v1.2.0 dans la KB.

    Returns:
        True si l'installation a réussi, False sinon
    """
    base = Path(kb_path) / "clone-chat"
    refs = base / "references"

    # Créer les répertoires
    refs.mkdir(parents=True, exist_ok=True)

    # Écrire SKILL.md
    skill_path = base / "SKILL.md"
    skill_path.write_text(SKILL_MD, encoding="utf-8")
    print(f"✅ Créé : {skill_path}")

    # Écrire clone-template.md
    template_path = refs / "clone-template.md"
    template_path.write_text(CLONE_TEMPLATE_MD, encoding="utf-8")
    print(f"✅ Créé : {template_path}")

    # Vérification de l'installation
    print("\n--- Vérification de l'installation ---")
    checks = [
        ("SKILL.md existe", skill_path.exists()),
        ("SKILL.md non vide", skill_path.stat().st_size > 0),
        ("YAML frontmatter", "---" in skill_path.read_text(encoding="utf-8")[:100]),
        ("Version correcte", f"version: {CLONE_CHAT_VERSION}" in skill_path.read_text(encoding="utf-8")),
        ("Étape 3.5 présente", "3.5" in skill_path.read_text(encoding="utf-8")),
        ("clone-template.md existe", template_path.exists()),
        ("clone-template.md non vide", template_path.stat().st_size > 0),
        ("Structure répertoires", refs.exists()),
    ]

    all_pass = True
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        if not result:
            all_pass = False
        print(f"  {status} — {name}")

    if all_pass:
        print(f"\n🎉 clone-chat v{CLONE_CHAT_VERSION} installé avec succès dans : {kb_path}")
    else:
        print(f"\n⚠️  Installation incomplète — vérifiez les erreurs ci-dessus")

    # Afficher la structure
    print(f"\nStructure créée :")
    print(f"  {base}/")
    print(f"  ├── SKILL.md               ({skill_path.stat().st_size:,} octets)")
    print(f"  └── references/")
    print(f"      └── clone-template.md  ({template_path.stat().st_size:,} octets)")

    return all_pass


# ─── Enregistrement dans le Registre KB ──────────────────────────────────────

def register_in_knowledge_md(kb_path: str) -> bool:
    """Enregistre clone-chat dans le registre KB (KNOWLEDGE.md).

    Si KNOWLEDGE.md n'existe pas, le crée avec le template complet.
    Si KNOWLEDGE.md existe mais ne contient pas clone-chat, ajoute l'entrée.

    Returns:
        True si l'enregistrement a réussi, False sinon
    """
    kb = Path(kb_path)
    knowledge_md = kb / "KNOWLEDGE.md"

    if knowledge_md.exists():
        # Vérifier si clone-chat est déjà enregistré
        content = knowledge_md.read_text(encoding="utf-8")
        if "clone-chat" in content:
            print(f"✅ clone-chat déjà enregistré dans {knowledge_md}")
            return True

        # Ajouter l'entrée clone-chat au tableau existant
        # Chercher le tableau des skills KB
        table_match = re.search(
            r'(\| clone-chat \|.*\|)',
            content
        )
        if not table_match:
            # Ajouter une ligne au tableau des skills
            # Chercher le dernier skill dans le tableau
            last_row_match = re.findall(r'^\| .+ \| .+ \| .+ \| .+ \| .+ \| .+ \| .+ \|$', content, re.MULTILINE)
            if last_row_match:
                # Insérer après la dernière ligne du tableau
                new_row = f"| clone-chat | {CLONE_CHAT_VERSION} | {CLONE_CHAT_CATEGORY} | Exécutable | {CLONE_CHAT_LANGUAGE} | gen-plan (optionnel) | OK (enrichi si gen-plan présent, standalone sinon) |"
                # Trouver la position de la dernière ligne
                last_pos = content.rfind(last_row_match[-1])
                insert_pos = last_pos + len(last_row_match[-1])
                content = content[:insert_pos] + "\n" + new_row + content[insert_pos:]

                # Ajouter la section détaillée
                detail_section = f"""

### clone-chat v{CLONE_CHAT_VERSION}

**Catégorie** : {CLONE_CHAT_CATEGORY}
**Langue** : {CLONE_CHAT_LANGUAGE}
**Description** : Clone l'intégralité d'une discussion (contexte, décisions, artefacts, worklog) dans un fichier Markdown auto-suffisant. En exécutant ce clone dans une nouvelle session, l'assistant IA recrée le contexte complet de la discussion originale.
**Chemin** : `skills/clone-chat/SKILL.md`
**Tags** : {', '.join(CLONE_CHAT_TAGS)}
**Dépendances** : gen-plan (optionnel, pour enrichir les spécifications)
**Relations** : gen-plan v3.5.0 (orchestration amont), gen-plan v3.3.0 KB (Registre KB, protocole de découverte), correct-work (validation croisée), skill-creator (conventions)
**Déclencheurs** : `clone-chat`, `cloner la discussion`, `exécuter le clone`
"""
                # Insérer avant la section Matrice de Compatibilité
                matrice_pos = content.find("## Matrice de Compatibilité")
                if matrice_pos > 0:
                    content = content[:matrice_pos] + detail_section + "\n" + content[matrice_pos:]
                else:
                    content += detail_section

                # Mettre à jour la date
                content = re.sub(
                    r'\*\*Dernière mise à jour\*\* : .+',
                    f'**Dernière mise à jour** : {datetime.now().strftime("%Y-%m-%d")}',
                    content
                )

                knowledge_md.write_text(content, encoding="utf-8")
                print(f"✅ clone-chat ajouté au registre KB : {knowledge_md}")
                return True

    # Créer KNOWLEDGE.md depuis le template
    knowledge_content = KNOWLEDGE_MD_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d")
    )
    knowledge_md.write_text(knowledge_content, encoding="utf-8")
    print(f"✅ Registre KB créé : {knowledge_md}")

    return True


# ─── Vérification de compatibilité ───────────────────────────────────────────

def verify_compatibility(kb_path: str) -> bool:
    """Vérifie la compatibilité de clone-chat avec les skills KB existants.

    Returns:
        True si toutes les compatibilités sont OK, False sinon
    """
    print("\n=== Vérification de Compatibilité KB ===\n")

    # Scanner les skills existants
    skills = scan_kb(kb_path)

    if not skills:
        print("⚠️  Aucun skill KB existant trouvé — clone-chat fonctionnera en mode standalone")
        return True

    # Afficher le registre dynamique
    print("## Skills KB Détectés")
    print(f"| Skill | Version | Type | Source | Compatibilité |")
    print(f"|-------|---------|------|--------|---------------|")

    for skill in skills:
        source_tag = "🌍" if skill["source"] == "Ecosysteme" else "📦"
        print(f"| {skill['name']} | {skill['version']} | {skill['type']} | {source_tag} {skill['source']} | Évalué |")

    # Évaluer la compatibilité avec clone-chat
    new_skill = {
        "name": "clone-chat",
        "version": CLONE_CHAT_VERSION,
        "category": CLONE_CHAT_CATEGORY,
    }

    compat_results = evaluate_compatibility(skills, new_skill)

    print(f"\n## Compatibilité clone-chat v{CLONE_CHAT_VERSION}")
    print(f"| Skill | Version | Compatible | Détails |")
    print(f"|-------|---------|------------|---------|")

    all_compatible = True
    for result in compat_results:
        status = "✅" if result["compatible"] else "❌"
        if not result["compatible"]:
            all_compatible = False
        print(f"| {result['skill']} | {result['version']} | {status} | {result['details']} |")

    if all_compatible:
        print(f"\n✅ clone-chat v{CLONE_CHAT_VERSION} est compatible avec tous les skills KB existants")
    else:
        print(f"\n⚠️  Des incompatibilités ont été détectées")

    return all_compatible


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Intègre clone-chat v1.2.0 dans la base de connaissance (Protocole de Découverte KB v3.3.0)"
    )
    parser.add_argument("kb_path", help="Chemin vers la base de connaissance (ex: C:\\Users\\PC\\Downloads\\knowledge\\skills)")
    parser.add_argument("--register", action="store_true", help="Enregistrer clone-chat dans le registre KB (KNOWLEDGE.md)")
    parser.add_argument("--verify", action="store_true", help="Vérifier la compatibilité avec les skills KB existants")
    parser.add_argument("--full", action="store_true", help="Exécuter toutes les étapes (scan + install + register + verify)")

    args = parser.parse_args()

    if not args.full and not args.register and not args.verify:
        # Mode par défaut : installation uniquement
        args.full = False
        print("Mode : installation uniquement (utilisez --full pour toutes les étapes)")

    print(f"clone-chat v{CLONE_CHAT_VERSION} — Intégration dans la base de connaissance")
    print(f"Chemin cible : {args.kb_path}")
    print(f"Protocole : gen-plan v3.3.0 — Registre KB avec Protocole de Découverte")
    print()

    # ─── Étape 1 : Scanner la KB ────────────────────────────────────────────
    if args.full or args.verify:
        print("=== Étape 1 : Scan de la Knowledge Base ===\n")
        skills = scan_kb(args.kb_path)

        if skills:
            print(f"Skills KB détectés : {len(skills)}")
            for skill in skills:
                source_tag = "🌍" if skill["source"] == "Ecosysteme" else "📦"
                print(f"  {source_tag} {skill['name']} v{skill['version']} ({skill['type']}, {skill['category']})")
        else:
            print("Aucun skill KB existant trouvé — clone-chat sera le premier skill KB")
        print()

    # ─── Étape 2 : Installer clone-chat ─────────────────────────────────────
    print("=== Étape 2 : Installation de clone-chat ===\n")
    success = install_clone_chat(args.kb_path)
    print()

    if not success:
        print("❌ Installation échouée — arrêt")
        sys.exit(1)

    # ─── Étape 3 : Enregistrer dans le registre KB ─────────────────────────
    if args.full or args.register:
        print("=== Étape 3 : Enregistrement dans le registre KB ===\n")
        register_in_knowledge_md(args.kb_path)
        print()

    # ─── Étape 4 : Vérifier la compatibilité ────────────────────────────────
    if args.full or args.verify:
        print("=== Étape 4 : Vérification de compatibilité ===")
        verify_compatibility(args.kb_path)
        print()

    # ─── Bilan ──────────────────────────────────────────────────────────────
    print("=" * 60)
    print(f"clone-chat v{CLONE_CHAT_VERSION} — Intégration terminée")
    print(f"Chemin : {args.kb_path}/clone-chat/")
    print()
    print("Structure créée :")
    print(f"  {args.kb_path}/clone-chat/")
    print(f"  ├── SKILL.md               (skill clone-chat v{CLONE_CHAT_VERSION})")
    print(f"  └── references/")
    print(f"      └── clone-template.md  (template de structure du clone)")

    if args.full or args.register:
        print(f"\nRegistre KB : {args.kb_path}/KNOWLEDGE.md")

    print()
    print("Pour utiliser clone-chat depuis gen-plan :")
    print("  gen-plan: utiliser le skill clone-chat de ma KB")
    print()
    print("Pour vérifier l'installation :")
    print(f'  python integrate-clone-chat-kb-v2.py "{args.kb_path}" --verify')


if __name__ == "__main__":
    main()
