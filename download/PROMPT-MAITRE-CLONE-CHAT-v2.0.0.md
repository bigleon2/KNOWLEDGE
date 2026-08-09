# PROMPT MAÎTRE — Installation du skill clone-chat v2.0.0

> **Version du prompt** : 1.0.0
> **Skill cible** : clone-chat v2.0.0
> **Date** : 2026-08-09
> **Source** : Écosystème Knowledge — Clone de discussion
> **Dépend** : `PROMPT-MAITRE-SHARED.md` (lire en premier)

---

## §A — DÉCLENCHEURS

- `clone-chat` ou `clone_chat`
- `clone la discussion` ou `clone cette session`
- `clone-chat:` suivi d'une description de session
- `archiver la discussion` — archivage complet d'une session multi-sessions
- `sauvegarde de contexte` — sauvegarde du contexte pour reprise dans une nouvelle session
- `crée un clone` — demande explicite de clonage
- Toute demande de capturer l'intégralité d'une discussion en vue d'une reprise ultérieure
- Fin de session longue avec demande de préservation du contexte

## §B — PRÉREQUIS

Lire `PROMPT-MAITRE-SHARED.md` avant de continuer. Ce fichier contient le contexte commun, les conventions écosystème, les variables d'installation et le registre des relations.

Résumé des variables utiles (SHARED §1.1) :
- `{{SKILLS_ROOT}}` = `skills/`
- `{{KB_PATH}}` = `skills/KNOWLEDGE.md`
- `{{KB_ENABLED}}` = `true`

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

clone-chat est un skill de **clonage de discussion** pour assistant IA. Il produit un fichier Markdown auto-suffisant qui capture l'intégralité du contexte d'une discussion multi-sessions : les décisions, les artefacts produits, les spécifications techniques, les évolution de contexte (drifts), et les instructions de reprise. Le clone permet à un assistant IA dans une nouvelle session de reconstruire l'état exact de la discussion et de poursuivre le travail sans perte d'information.

### §1.2 Les 7+1 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| **1** | Collecte du worklog | Lire le fichier `worklog.md` (format SHARED §1.4), identifier les sessions distinctes, produire un tableau chronologique |
| **2** | Collecte des artefacts | Scanner l'arborescence pour identifier fichiers créés/modifiés, grouper par catégorie |
| **3** | Extraction des décisions | Identifier décisions utilisateur, bugs corrigés, conventions établies, données de calibration |
| **3.5** | Context Drift | Tracer chaque changement de contexte (5 types : INVERSION, MODIFICATION, CORRECTION, ENRICHISSEMENT, RECALIBRAGE) |
| **4** | Spécifications techniques | Détailler les fichiers principaux avec niveau de détail selon taille (in extenso / condensé / résumé) |
| **5** | Assemblage | Combiner toutes les sections en un document Markdown unique et cohérent (ordre imposé §0-§5) |
| **6** | Validation (8 checks) | Exécuter les 8 checks de validation (auto-suffisance, complétude worklog/skills/décisions/bugs/drifts, exécutabilité, auto-clonage) |
| **7** | Sauvegarde | Sauvegarder le clone dans `download/` avec nom descriptif, enregistrer dans le worklog |

### §1.3 Détail de l'Étape 1 — Collecte du worklog

Lire le fichier `worklog.md` à la racine du projet (format SHARED §1.4). Identifier les sessions distinctes (séparées par des lignes `---`). Extraire pour chaque session :
- Le Task ID et le nom de l'agent
- La tâche effectuée
- Les actions concrètes réalisées
- Les résultats et livrables produits

Produire un tableau chronologique des sessions.

### §1.4 Détail de l'Étape 2 — Collecte des artefacts

Scanner l'arborescence du projet pour identifier tous les fichiers **créés ou modifiés** durant la discussion. Pour chaque artefact :
- Le chemin relatif (convention SHARED §1.2 : kebab-case)
- La taille (Ko)
- Une description de son contenu et rôle

Grouper par catégorie : skills, scripts, documents, charts, archives.

### §1.5 Détail de l'Étape 3 — Extraction des décisions

Parcourir le worklog et le contexte pour identifier :

1. **Décisions de l'utilisateur** : chaque choix explicite avec son contexte et ses conséquences
2. **Bugs corrigés** : chaque bug avec cause, fix et résultat
3. **Conventions établies** : chaque règle avec sa formulation et un exemple
4. **Données de calibration** : grilles #token, métriques, historique

Produire des tableaux structurés pour chaque catégorie.

### §1.6 Détail de l'Étape 3.5 — Context Drift

Cette étape **trace chaque fois que le contexte a changé** durant la discussion. C'est une étape d'analyse critique qui certifie que les évolutions ont été détectées.

**5 types de drift** :

| Type | Définition | Exemple |
|------|-----------|--------|
| INVERSION | Décision renversée (A accepté puis A refusé) | « Version v2.0.0 » acceptée puis refusée au profit de v3.1.0 |
| MODIFICATION | Décision ajustée (paramètre X remplacé par Y) | Export DOCX remplacé par export MD par défaut |
| CORRECTION | Spécification ou décision erronée corrigée | Chemins absolus corrigés en chemins relatifs |
| ENRICHISSEMENT | Décision complétée par ajout d'un élément nouveau | Ajout Étape 3.5 Context Drift à clone-chat v1.1.0→v1.2.0 (historique) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibrée) | Grille #token ajustée de -32% après calibration E15 |

**Format de la table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|

**Règle obligatoire** : Même si aucun drift n'est détecté, écrire « Aucune évolution de contexte détectée » pour certifier que l'analyse a bien été effectuée. Ne jamais laisser cette section vide.

### §1.7 Détail de l'Étape 4 — Spécifications techniques

Détailler les fichiers principaux créés ou modifiés. Le niveau de détail dépend de la taille du fichier (convention in extenso) :

| Taille | Traitement |
|--------|------------|
| < 200 lignes | In extenso (contenu complet) |
| 200-500 lignes | In extenso avec sections condensées |
| > 500 lignes | Résumé structuré : objectifs, structure, modules clés |

Pour chaque fichier : description, signature (fonctions/modules), chemin relatif, taille.

**Intégration gen-plan (optionnelle)** :
- Si gen-plan v3.6.0+ est présent : enrichir avec les données de calibration E15 et les étapes E1-E7
- Si `{{KB_ENABLED}}` est `true` : enrichir §2 avec les descriptions du Registre KB (`{{KB_PATH}}`) pour les skills de l'écosystème

### §1.8 Détail de l'Étape 5 — Assemblage

Combiner toutes les sections collectées en un document Markdown unique et cohérent. L'ordre des sections est imposé :

1. §0 — Règle zéro (contexte perdu)
2. §1 — Chronologie de la discussion
3. §2 — Écosystème de skills (fichiers, scripts, artefacts)
4. §2.4 — Historique des interactions (si `{{KB_ENABLED}}`)
5. §3 — Décisions clés (décisions, bugs, conventions, calibration)
6. §3.5 — Évolutions de contexte (Context Drift)
7. §4 — Instructions d'utilisation
8. §5 — Auto-clonage

Voir `references/clone-template.md` pour la structure complète du template.

### §1.9 Détail de l'Étape 6 — Validation (8 checks)

Exécuter les **8 checks de validation**. Chaque check est binaire (PASS/FAIL). Le clone est valide si 8/8 PASS.

| # | Check | Critère principal | Sous-critères de validation |
|---|-------|-------------------|--------------------------|
| 1 | Auto-suffisance | Le clone est lisible et exécutable sans fichier externe | (a) Pas de « voir fichier X », (b) Pas de dépendance externe, (c) Un assistant neuf peut le lire et agir |
| 2 | Complétude worklog | Chaque session du worklog est représentée en §1 | (a) Table §1.2 complète, (b) Chaque session a au moins 1 ligne en §1.3, (c) Sessions manquantes = FAIL |
| 3 | Complétude skills | Chaque skill créé/modifié est détaillé en §2 | (a) Version présente, (b) Description fonctionnelle, (c) Spécifications techniques, (d) Relations listées |
| 4 | Complétude décisions | Chaque décision, bug, convention est en §3 | (a) Décisions utilisateur avec contexte + conséquence, (b) Bugs avec cause + fix + résultat, (c) Conventions avec règle + exemple |
| 5 | Complétude bugs | Chaque bug corrigé a cause + fix + résultat | (a) Cause racine identifiée, (b) Fix décrit, (c) Résultat vérifié, (d) Pas de bug sans résolution |
| 6 | Complétude drifts | Chaque drift identifié est dans la table §3.5 | (a) Type correct parmi les 5, (b) Avant/Après explicites, (c) Session et ligne worklog référencées, (d) Section présente même si vide |
| 7 | Exécutabilité | Un assistant IA peut reconstruire le contexte | (a) §4 instructions claires, (b) Fichiers prioritaires listés, (c) In extenso pour fichiers < 200 lignes, (d) Résumé structuré pour > 500 lignes |
| 8 | Auto-clonage | La section §5 est présente et auto-référentielle | (a) §5 décrit le mécanisme de croissance, (b) Clone-chat référencé, (c) Mécanisme §1-§3 enrichis / §0,§4-§5 régénérés |

Si un check échoue, corriger avant de passer à l'étape 7.

### §1.10 Détail de l'Étape 7 — Sauvegarde

Sauvegarder le clone dans `download/` avec un nom descriptif incluant la date et le sujet.

Format du nom : `<sujet>-clone-<AAAA-MM-JJ>.md`

Enregistrer la sauvegarde dans le worklog (format SHARED §1.4).

### §1.11 Intégration KB

Si `{{KB_ENABLED}}` est `true` :

- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **Registre KB** : enrichir la section §2 du clone avec les descriptions des skills depuis le registre
- **Historique des interactions** : reproduire en §2.4 l'historique des interactions clés entre skills
- **Protocole de Découverte** : voir SHARED §2.3

---

## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack technique

- **Langage** : Markdown pur (CommonMark compatible)
- **Environnement** : `{{SKILLS_ROOT}}clone-chat/`
- **Pas de dépendance externe** (aucun ZIP, aucune image embed, aucun outil spécifique requis)
- Le fichier doit être lisible avec n'importe quel éditeur de texte

### §2.2 Format de sortie

- Fichier Markdown unique, auto-suffisant
- Aucune dépendance externe
- Tout le contexte est contenu dans le fichier
- Tableaux Markdown pour les données structurées
- Code fences pour les extraits de code

### §2.3 Grille #token

| Mode | #token estimé | Profil min. | Plage |
|------|--------------|-------------|-------|
| Discussion courte (< 5 sessions) | 2750 | ECO | 2000-3500 |
| Discussion moyenne (5-15 sessions) | 4500 | NORMAL | 3500-5500 |
| Discussion longue (> 15 sessions) | 7250 | NORMAL | 5500-9000 |

**Note v2.0.0** : estimation recalibrée pour couvrir l'Étape 3.5 Context Drift, l'intégration gen-plan v3.6.0+ KB, et la section historique des interactions.

### §2.4 Profils ressource

| Profil | Comportement pour le clone |
|--------|--------------------------|
| **NORMAL** | Clone complet, toutes les sections détaillées |
| **ECO** | Clone condensé, sections §3 regroupées |
| **VIEUX PC** | Clone minimal, §3.5 et §5 uniquement |

Le profil est déterminé par la longueur de la discussion (voir grille #token en §2.3).

### §2.5 Mitigation taille

Pour les clones de discussions longues (> 15 sessions), appliquer :
1. Résumer les sessions anciennes en 1 ligne
2. Détailler §1.3 pour les 5-10 dernières sessions seulement
3. Skills stables décrits en 1 ligne

### §2.6 Intégration gen-plan (optionnelle)

Clone-chat fonctionne **standalone** sans gen-plan. Si gen-plan v3.6.0+ est présent, les enrichissements suivants sont appliqués :

| Composant gen-plan | Enrichissement clone-chat |
|--------------------|------------------------|
| v3.6.0+ (calibration E15) | Étape 1 : données E15, grille #token |
| v3.6.0+ (étapes E1-E7) | Étape 4 : structure de planification |
| v3.6.0+ (Registre KB) | §2 : descriptions skills depuis `{{KB_PATH}}` |
| v3.6.0+ (kb_path) | §4 : liens vers skills du Registre |

### §2.7 Structure des fichiers

```
{{SKILLS_ROOT}}clone-chat/
├── SKILL.md
└── references/
    └── clone-template.md
```

### §2.8 Logging worklog

Voir SHARED §1.4 pour le format. Spécifiquement pour clone-chat :

```markdown
---
Task ID: [task-id]
Agent: clone-chat v2.0.0
Task: Clonage de discussion — [sujet]

Work Log:
- Étape 1 : Worklog collecté, N sessions identifiées
- Étape 2 : N artefacts découverts
- Étape 3 : N décisions, N bugs, N conventions extraites
- Étape 3.5 : N drifts identifiés
- Étape 4 : N fichiers détaillés (X in extenso, Y résumés)
- Étape 5 : Assemblage terminé
- Étape 6 : 8/8 checks PASS
- Étape 7 : Clone sauvegardé dans download/

Stage Summary:
- Clone produit : [nom-du-clone].md ([taille] Ko)
- 8/8 checks PASS
- Profil : [NORMAL|ECO|VIEUX PC]
```

---

## §3 — RELATIONS

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet des relations inter-skills.

Relations directes de clone-chat (extrait de SHARED §3.1) :

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Archivé par | Sessions longues, optionnel, version >= v3.6.0 |
| correct-work | Vérifié par | Validation croisée, §3.5 Context Drift, version >= v2.3.0 |
| skill-creator | Conventions par | Conventions structurelles, version >= v1.0.0 |
| KNOWLEDGE.md | Lecture seule | Consultation du registre KB pour enrichissement §2 |

---

## §4 — YAML FRONTMATTER

```yaml
---
name: clone-chat
version: 2.0.0
category: ecosystem
language: fr
tags:
  - clone
  - discussion
  - context
  - drift
  - gen-plan
  - auto-clonage
  - worklog
description: >
  Clone l'intégralité d'une discussion (contexte, décisions, artefacts,
  worklog) dans un fichier Markdown auto-suffisant. 7+1 étapes, Étape 3.5
  Context Drift, intégration gen-plan v3.6.0+ KB. Format Markdown unique,
  propriété auto-clonage.
dependencies:
  - skill: gen-plan
    version: ">=3.6.0"
    used_at: "Calibration E15, archivage sessions longues"
    optional: true
  - skill: correct-work
    version: ">=2.3.0"
    used_at: "Validation croisée (Mode CIBLE, §3.5)"
---
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

### §5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}clone-chat/references
```

### §5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~365 lignes) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** : contexte écosystème (voir SHARED §0), mention 78 skills, variables `{{SKILLS_ROOT}}`, `{{KB_PATH}}`, `{{KB_ENABLED}}`
3. **§1 — Spécification fonctionnelle** : objectif, 7+1 étapes (détail de chaque), profils ressource
4. **§2 — Spécification technique** : format sortie, stack, grille #token, intégration gen-plan, mitigation taille, structure fichiers
5. **§3 — Conventions** : nommage (SHARED §1.2), chemins relatifs, règle in extenso, numérotation §0-§5, Context Drift obligatoire
6. **§4 — Relations** : gen-plan (§4.1), correct-work (§4.2), skill-creator (§4.3)
7. **§5 — Auto-clonage** : mécanisme de croissance, fichiers de référence
8. **HISTORIQUE DES VERSIONS**

### §5.3 Créer le fichier de référence

Le contenu in extenso du template est en §9.

### §5.4 Mettre à jour KNOWLEDGE.md

Ajouter l'entrée clone-chat au registre KB (format SHARED §2.2) :

```markdown
## clone-chat v2.0.0

- **Category** : ecosystem
- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, intégration gen-plan v3.6.0+ KB.
- **Dépend de** : gen-plan >= v3.6.0 (optionnel), correct-work >= v2.3.0 (validation croisée)
- **Utilisé par** : gen-plan (E4, E15), correct-work (Mode CIBLE, §3.5)
- **Dernière calibration** : [date]
- **Statut** : stable
```

### §5.5 Mettre à jour les cross-references

Vérifier que (SHARED §3.2) :
1. gen-plan mentionne clone-chat dans ses dépendances (déjà fait)
2. correct-work mentionne clone-chat dans ses dépendances (déjà fait)
3. KNOWLEDGE.md mentionne clone-chat dans les entrées « Utilisé par » de gen-plan et correct-work

---

## §6 — VÉRIFICATION POST-INSTALLATION

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | SKILL.md existe | `{{SKILLS_ROOT}}clone-chat/SKILL.md` | File exists |
| 2 | YAML frontmatter valide | name, version, category, language, tags, description, dependencies | All present |
| 3 | §0 Règle zéro | 78 skills mentionnés, variables `{{SKILLS_ROOT}}`, `{{KB_PATH}}`, `{{KB_ENABLED}}` | Present |
| 4 | 7+1 étapes | Étapes 1-7 + Étape 3.5 documentées | All present |
| 5 | 8 checks validation | Table complète en Étape 6 | 8 checks |
| 6 | 5 types de drift | INVERSION, MODIFICATION, CORRECTION, ENRICHISSEMENT, RECALIBRAGE | All present |
| 7 | Auto-clonage §5 | Mécanisme de croissance documenté | Present |
| 8 | Template présent | `references/clone-template.md` | File exists |
| 9 | Template version | « 2.0.0 » dans le template | Present |
| 10 | Chemins relatifs | Aucun chemin absolu dans SKILL.md ni template | No absolute paths |
| 11 | Dependencies frontmatter | gen-plan >=3.6.0 (optional), correct-work >=2.3.0 | Correct |
| 12 | Variables SHARED | `{{SKILLS_ROOT}}`, `{{KB_PATH}}`, `{{KB_ENABLED}}` utilisées | Present |
| 13 | Kebab-case | `clone-chat`, `clone-template` | Correct |
| 14 | Worklog SHARED §1.4 | Référencé en §1.1 et §1.7 | Present |
| 15 | KNOWLEDGE.md | Entrée clone-chat présente (SHARED §2.2) | Present |
| 16 | Compatibilité écosystème | 16/16 checks PASS | All PASS |

---

## §7 — HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v1.0.0 | 2026-07-29 | Version initiale, 7 étapes, template, auto-clonage |
| v1.1.0 | 2026-07-29 | 8 corrections correct-work (§0-§5, #token, chemins) |
| v1.2.0 | 2026-07-29 | Étape 3.5 Context Drift, 5 types, 8 checks, gen-plan KB |
| v2.0.0 | 2026-08-09 | Harmonisation écosystème maître : gen-plan v3.6.0, correct-work v2.3.0, 78 skills, variables SHARED, dependencies frontmatter, worklog SHARED §1.4, prompt maître |

---

## §8 — NOTES DE CONCEPTION

### §8.1 Pourquoi 7+1 étapes ?

Les 7 étapes (collecte, artefacts, décisions, spécifications, assemblage, validation, sauvegarde) couvrent le cycle complet de clonage d'une discussion. L'Étape 3.5 (Context Drift) est une étape d'analyse critique ajoutée en v1.2.0 (historique) après correction par correct-work : elle certifie que les évolutions de contexte ont été détectées et tracées. Le numbering « 7+1 » (et non « 8 étapes ») souligne que l'Étape 3.5 est une analyse transversale insérée entre l'extraction des décisions et les spécifications techniques, et non une étape séquentielle indépendante.

### §8.2 Pourquoi le Context Drift ?

Les discussions longues génèrent inévitablement des changements de contexte : des décisions renversées, des paramètres ajustés, des spécifications corrigées. Sans traçage explicite, ces drifts sont invisibles dans le clone final, conduisant à des incohérences quand un assistant tente de reprendre le travail. Les 5 types de drift (INVERSION, MODIFICATION, CORRECTION, ENRICHISSEMENT, RECALIBRAGE) couvrent tous les patterns observés dans les discussions réelles. La règle « section présente même si vide » garantit que l'analyse a été effectuée.

### §8.3 Pourquoi l'auto-clonage ?

La propriété d'auto-clonage résout un problème fondamental : la perte de contexte entre sessions. Un clone contient dans son §5 les instructions pour se cloner lui-même. Quand une nouvelle session prolonge la discussion, le nouveau clone incorpore tout le contexte du clone précédent plus les nouvelles sessions. Les sections §1-§3 (données historiques) sont enrichies, tandis que §0, §4-§5 (auto-référentielles) sont régénérées à l'identique. Ce mécanisme permet une chaîne de clonage théoriquement infinie sans perte d'information.

### §8.4 Pourquoi 3 profils ressource ?

Les profils NORMAL/ECO/VIEUX PC sont hérités de gen-plan (SHARED §4.1, matrice agent × skill). NORMAL est le défaut, produisant un clone complet. ECO condense les sections §3 pour les discussions courtes. VIEUX PC réduit le clone au strict minimum (§3.5 et §5) pour les environnements avec des contraintes de tokens sévères. Le profil est automatiquement déterminé par la grille #token (§2.3) selon la longueur de la discussion.

### §8.5 Pourquoi la règle in extenso ?

La règle in extenso garantit que les fichiers critiques sont entièrement contenus dans le clone. Les fichiers de moins de 200 lignes sont reproduits intégralement, permettant à un assistant dans une nouvelle session de les recréer sans aucune information externe. Entre 200 et 500 lignes, les sections sont condensées. Au-delà de 500 lignes, un résumé structuré (objectifs, structure, modules clés) suffit. Ce seuil de 200 lignes (et non 500) a été recalibré en v1.1.0 suite à une correction correct-work (S2) qui identifiait le seuil initial comme trop haut.

### §8.6 Pourquoi Markdown seul ?

Le choix du Markdown pur (CommonMark compatible) est délibéré : aucun outil spécifique n'est requis pour lire ou éditer un clone. Le fichier est lisible dans n'importe quel éditeur de texte, versionnable avec git, et interprétable par tout assistant IA. Les tableaux Markdown et les code fences fournissent une structure suffisante pour les données sans dépendre de formats propriétaires.

### §8.7 Pourquoi 8 checks de validation ?

Les 8 checks couvrent toutes les dimensions critiques d'un clone valide : auto-suffisance (check 1), complétude des 4 sources de données (worklog, skills, décisions, bugs — checks 2-5), traçabilité des drifts (check 6), exécutabilité par un assistant (check 7), et auto-référentialité (check 8). Chaque check a des sous-critères explicites, rendant la validation reproductible. Un clone doit obtenir 8/8 PASS pour être considéré valide.

---

## §9 — CONTENU IN EXTENSO DES FICHIERS RÉFÉRENCE

Le fichier référence suivant doit être créé dans `{{SKILLS_ROOT}}clone-chat/references/`. Voici son contenu intégral.

### §9.1 `references/clone-template.md`

```markdown
# CLONE DE DISCUSSION — [TITRE DU PROJET]

> **Date du clone** : [AAAA-MM-JJ]
> **Source** : Discussion entre [Utilisateur] et [Assistant]
> **Sessions couvertes** : [N] sessions (du [DATE_DÉBUT] au [DATE_FIN])
> **Version clone-chat** : 2.0.0

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : [DESCRIPTION DE L'ENVIRONNEMENT CIBLE]

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.1 Résumé global

[Paragraphe de 3-5 phrases résumant l'ensemble de la discussion :
- Le sujet principal
- Les livrables clés produits
- L'évolution de la complexité
- L'état final atteint]

### §1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | [DATE] | [THÈME] | [LIVRABLES] |
| 2 | [DATE] | [THÈME] | [LIVRABLES] |
| ... | ... | ... | ... |
| N | [DATE] | [THÈME] | [LIVRABLES] |

### §1.3 Détail par session

[Groupement par période avec résumé des sessions.
Exemple :]

**Sessions 1-5 ([DATE])** : [Résumé des 5 sessions :
actions principales, skills utilisés, décisions clés.]

**Sessions 6-10 ([DATE])** : [Résumé des 5 sessions...]

**Sessions [dernières] ([DATE])** : [Résumé des dernières sessions...]

---

## §2 — ÉCOSYSTÈME DE SKILLS

### §2.1 Skills créés ou modifiés

[Pour chaque skill écosystème créé ou modifié :]

#### [nom-skill] v[x.y.z]

- **Description** : [Description en 1-2 phrases]
- **Catégorie** : [ecosystem | tool | ...] | **Langue** : [fr | en]
- **Spécification fonctionnelle** : [Fonctionnalités clés, modes,
  étapes, règles spécifiques]
- **Spécification technique** : [Stack, dépendances, structure fichiers]
- **Relations** : [Autres skills avec lesquels il interagit]

### §2.2 Scripts créés ou modifiés

[Pour chaque script :]

#### [nom-script].py v[x.y.z]

- **Description** : [Description en 1-2 phrases]
- **Signature** : [Modules, fonctions principales, nb tests]
- **Chemin** : `scripts/[nom-script].py` ([taille])

### §2.3 Artefacts produits

| Fichier | Taille | Description |
|---------|--------|-------------|
| [chemin/relatif] | [X Ko] | [Description] |
| ... | ... | ... |

### §2.4 Historique des interactions

[Si le registre KB est disponible, reproduire ici l'historique
des interactions clés entre skills au cours de la discussion :
quels skills ont été invoqués, dans quel ordre, avec quels résultats.
Tableau chronologique si possible.]

---

## §3 — DÉCISIONS CLÉS

### §3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | [Décision] | [Pourquoi cette décision] | [Ce qui a changé] |
| ... | ... | ... | ... |

### §3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | [Description du bug] | [Cause racine] | [Solution] | [Résultat] |
| ... | ... | ... | ... | ... |

### §3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| [Nom] | [Règle] | [Exemple concret] |
| ... | ... | ... |

### §3.4 Données de calibration

[Grilles #token, métriques, historique de calibration.
Tableaux avec chiffres concrets.]

### §3.5 Évolutions de contexte (Context Drift)

Cette section trace chaque fois que le contexte a **changé** durant la discussion.

**5 types de drift** :

| Type | Définition |
|------|----------|
| INVERSION | Décision renversée (A accepté → A refusé) |
| MODIFICATION | Décision ajustée (paramètre X → Y) |
| CORRECTION | Spécification ou décision erronée corrigée |
| ENRICHISSEMENT | Décision complétée (ajout d'un élément nouveau) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibré) |

**Table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | [TYPE] | [Avant] | [Après] | [N°] | [ligne] | [Raison] |
| ... | ... | ... | ... | ... | ... | ... |

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire

1. Lire §0 (Règle zéro) — tout est à reconstruire
2. Reconstruire les fichiers spécifiés dans §2 :
   - [Liste des fichiers in extenso]
   - [Liste des fichiers en résumé structuré]
3. Appliquer les décisions et conventions de §3
4. Créer les artefacts listés dans §2.3
5. Se positionner à l'état exact de la fin de la discussion originale

### Fichiers à reconstruire en priorité

1. **[fichier prio 1]** — [Raison]
2. **[fichier prio 2]** — [Raison]
3. **[fichier prio 3]** — [Raison]
4. [etc.]

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra :
   - Tout le contexte de ce clone (discussion originale)
   - Tout le nouveau contexte de la discussion en cours
3. Le nouveau clone remplace ce fichier
4. Le clone « grandit » à chaque session sans perdre l'historique

**Mécanisme** : les sections §1-§3 (incluant §3.5 Context Drift) sont
enrichies avec les nouvelles sessions. Les sections §0, §4-§5 sont
régénérées à l'identique (auto-référentielles).
```

---

## §10 — HISTORIQUE DES CORRECTIONS (correct-work)

Cette section retrace les corrections appliquées à clone-chat par correct-work au fil des sessions. Elle sert de référence pour comprendre l'évolution du skill et les problèmes qui ont été identifiés et résolus.

### §10.1 Round 1 (Session 17 → clone-chat v1.1.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Seuil in extenso < 500 lignes trop haut | S2 | Réduit à < 200 lignes |
| 2 | Chemins absolus dans §3.3 | S1 | Remplacés par chemins relatifs |
| 3-8 | Corrections structurelles (SKILL.md ↔ template, §5, #token, 78 skills) | S2-S3 | Alignement complet |

**Bilan** : 8 corrections. 3 HAUTE, 3 MOYENNE, 2 BASSE. → v1.1.0

### §10.2 Round 2 (Sessions 21-22 → clone-chat v1.2.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Template §5 ne mentionnait pas §0 | S2 | Ajout référence §0 dans §5 |
| 2 | Règle « drift vide » absente du SKILL.md | S2 | Ajout règle obligatoire en §3.5 |
| 3 | Décision #12 (intégration v2.2.0) absente de §3 | S3 | Ajout décision dans table §3.1 |
| 4-9 | Autres problèmes (sections manquantes, incohérences mineures) | S2-S4 | Corrections diverses |

**Bilan** : 9 problèmes, 7 corrections. → v1.2.0

### §10.3 Round 3 (Session 23 → stabilisation)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | « 7 étapes » vs « 7+1 étapes » incohérence | S2 | Unification en « 7+1 étapes » partout |
| 2 | Template §5 incomplet | S3 | Enrichissement du mécanisme de croissance |

**Bilan** : 2 problèmes, 2 corrections → **stabilisation atteinte**.

### §10.4 Round 4 (Session actuelle → clone-chat v2.0.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1-27 | Audit complet Mode CIBLE correct-work (cohérence interne, versions, SHARED, complétude, template) | — | 0 finding sur 27 checks → conforme |

**Bilan** : 0 finding. clone-chat v2.0.0 est entièrement conforme aux critères correct-work et à SHARED.