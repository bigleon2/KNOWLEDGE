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
  Context Drift, intégration gen-plan v3.6.1+ KB. Format Markdown unique,
  propriété auto-clonage.
dependencies:
  - skill: gen-plan
    version: ">=3.6.1"
    used_at: "Calibration E15, archivage sessions longues"
    optional: true
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "Validation croisée (Mode CIBLE, §3.5)"
---

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §A — DÉCLENCHEURS

- `clone-chat` ou `clone_chat`
- `clone la discussion` ou `clone cette session`
- `clone-chat:` suivi d'une description de session
- `archiver la discussion` — archivage complet d'une session multi-sessions
- `sauvegarde de contexte` — sauvegarde du contexte pour reprise dans une nouvelle session
- `crée un clone` — demande explicite de clonage
- Toute demande de capturer l'intégralité d'une discussion en vue d'une reprise ultérieure
- Fin de session longue avec demande de préservation du contexte


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
- Si gen-plan v3.6.1+ est présent : enrichir avec les données de calibration E15 et les étapes E1-E7
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

Voir `références/clone-template.md` pour la structure complète du template.

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

**Note v2.0.0** : estimation recalibrée pour couvrir l'Étape 3.5 Context Drift, l'intégration gen-plan v3.6.1+ KB, et la section historique des interactions.

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

Clone-chat fonctionne **standalone** sans gen-plan. Si gen-plan v3.6.1+ est présent, les enrichissements suivants sont appliqués :

| Composant gen-plan | Enrichissement clone-chat |
|--------------------|------------------------|
| v3.6.1+ (calibration E15) | Étape 1 : données E15, grille #token |
| v3.6.1+ (étapes E1-E7) | Étape 4 : structure de planification |
| v3.6.1+ (Registre KB) | §2 : descriptions skills depuis `{{KB_PATH}}` |
| v3.6.1+ (kb_path) | §4 : liens vers skills du Registre |

### §2.7 Structure des fichiers

```
{{SKILLS_ROOT}}clone-chat/
├── SKILL.md
└── références/
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
| gen-plan | Archivé par | Sessions longues, optionnel, version >= v3.6.1 |
| correct-work | Vérifié par | Validation croisée, §3.5 Context Drift, version >= v2.4.0 |
| skill-creator | Conventions par | Conventions structurelles, version >= v1.0.0 |
| KNOWLEDGE.md | Lecture seule | Consultation du registre KB pour enrichissement §2 |

---


## §5 — INSTRUCTIONS D'INSTALLATION

### §5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}clone-chat/références
```

### §5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~365 lignes) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** : contexte écosystème (voir SHARED §0), mention 80 skills, variables `{{SKILLS_ROOT}}`, `{{KB_PATH}}`, `{{KB_ENABLED}}`
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
- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, intégration gen-plan v3.6.1+ KB.
- **Dépend de** : gen-plan >= v3.6.1 (optionnel), correct-work >= v2.4.0 (validation croisée)
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

## §6 — CONVENTIONS

- Nommage kebab-case ; sections de clone préfixées « § » (§0 règle zéro, §1.0 héritage,
  §3.5 Context Drift, §5 auto-clonage)
- Worklog format SHARED §1.4
- Clonage en DERNIER dans l'ordonnancement (leçon E23) : l'instantané de clôture absorbe
  l'état le plus frais
- Scellement APRÈS enrichissement final (méthode neutral-line, Annexe D du PDF) pour que la
  SHA déclarée reste vérifiable byte-identique
