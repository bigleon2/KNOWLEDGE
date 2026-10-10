---
name: storyboard-manager
version: "1.0.0"
category: "Contenu & Marketing"
tags:
  - storyboard
  - manager
description: Aide les écrivains pour la planification d'histoire, le développement des personnages, la structuration de l'intrigue, l'écriture de chapitres, le suivi de la chronologie et la vérification de cohérence. Utilise ce skill pour les projets d'écriture créative organisés en dossiers contenant des personnages, des chapitres, des documents de planification d'histoire et des résumés. Déclenche ce skill pour des tâches comme « aide-moi à développer ce personnage », « écris le prochain chapitre », « vérifie la cohérence de mon histoire » ou « suis la chronologie des événements ».
language: fr

read_when:
  - Déclencher quand la demande concerne : aide les écrivains pour la planification d'histoire, le développement des personnages, la structuration de l'i…
  - Déclencher si la demande mentionne : histoire, aide, planification
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Storyboard Manager

## Aperçu

Le skill Storyboard Manager dote Claude de connaissances et d'outils spécialisés pour les flux de travail d'écriture créative. Il fournit des frameworks de développement de personnages, des modèles de structure narrative, un suivi automatisé de la chronologie et une vérification de cohérence pour les projets narratifs. Ce skill s'adapte automatiquement à différentes structures de dossiers de storyboard tout en maintenant les bonnes pratiques d'écriture de roman, de scénario et de fiction sérialisée.

## Capacités principales

Le skill fournit quatre capacités principales :

### 1. Développement & gestion des personnages
Soutenir la création de profils de personnages profonds et cohérents, avec passés, arcs et relations.

### 2. Planification & structure de l'histoire
Guider le développement de l'intrigue à l'aide de frameworks établis (structure en trois actes, Voyage du héros, Save the Cat, etc.) et aider à organiser les éléments narratifs.

### 3. Écriture de chapitres & de scènes
Générer du contenu de chapitre, des découpes de scènes et des dialogues cohérents avec les personnages et l'intrigue établis.

### 4. Suivi de la chronologie & vérification de cohérence
Utiliser des outils automatisés pour vérifier la cohérence chronologique, la continuité des personnages et la cohérence du world-building.

## Détection de la structure du projet

Storyboard Manager détecte automatiquement et s'adapte aux différentes organisations de dossiers. Repère ces schémas de répertoires courants :

**Dossiers de personnages :** `characters/`, `Characters/`, `cast/`, `Cast/`
**Dossiers de chapitres :** `chapters/`, `Chapters/`, `scenes/`, `Scenes/`, `story/`
**Dossiers de planification :** `story-planning/`, `planning/`, `outline/`, `notes/`
**Fichiers de résumé :** `summary.md`, `README.md`, `overview.md`

Au déclenchement, scanne la racine du projet pour identifier la structure et ajuste les flux en conséquence. Si aucune structure standard n'existe, recommande d'organiser les fichiers selon le schéma : `characters/`, `chapters/`, `story-planning/` et `summary.md`.

## Arbre de décision des flux de travail

Utilise cet arbre de décision pour déterminer le flux approprié :

```
User Request
├─ Character-related? ("develop character," "create backstory," "character arc")
│  └─ → Character Development Workflow
│
├─ Planning/Plot? ("outline story," "plan act 2," "plot structure")
│  └─ → Story Planning Workflow
│
├─ Writing content? ("write chapter," "generate scene," "continue story")
│  └─ → Chapter/Scene Writing Workflow
│
└─ Checking/Analysis? ("check consistency," "track timeline," "find contradictions")
   ├─ Timeline? → Use timeline_tracker.py script
   └─ Consistency? → Use consistency_checker.py script
```

## Flux de développement des personnages

### Étape 1 : Rassembler le contexte

Avant de développer un personnage, lis les fichiers de personnages existants pour comprendre :
- les conventions de nommage et le format de profil établis
- les personnages et relations existants
- le genre et le ton de l'histoire
- les archétypes de personnages déjà utilisés

Utilise l'outil Read pour examiner les fichiers de personnages existants dans le répertoire characters.

### Étape 2 : Accéder au framework de développement des personnages

Quand un accompagnement détaillé sur les personnages est nécessaire, lis `references/character_development.md` qui contient :
- les éléments centraux du personnage (personnalité, motivation, objectifs)
- le framework de passé (fantôme/blessure, relations formatives)
- les types d'arcs de personnage (changement positif, plat, négatif)
- la dynamique des relations
- les techniques de développement de la voix
- les règles de cohérence

Pour trouver efficacement une guidance précise, utilise Grep pour chercher les sections pertinentes :
```bash
# Example: Find guidance on character arcs
grep -i "character arc" references/character_development.md
```

### Étape 3 : Développer le profil du personnage

Crée ou enrichis les profils de personnages avec ces éléments essentiels :

**Informations de base**
- Nom, âge, rôle, apparence physique
- Traits de personnalité clés (positifs et négatifs)

**Passé**
- Origine et expériences formatives
- Fantôme/blessure qui façonne son comportement
- Relations clés et dynamiques familiales

**Arc du personnage**
- Croyance ou défaut de départ
- Désir vs Besoin (objectif externe vs croissance interne)
- Parcours de transformation
- État final

**Relations**
- Liens avec les autres personnages
- Types de dynamiques (allié, rival, mentor, etc.)
- Évolution des relations

**Éléments uniques**
- Capacités, compétences ou savoirs particuliers
- Secrets ou facettes cachées
- Voix/façons de parler
- Manies propres au personnage

### Étape 4 : Garantir la cohérence

Recoupe avec :
- les profils de personnages existants (éviter la redondance des rôles/traits)
- les documents de planification de l'histoire (garantir l'alignement avec les besoins de l'intrigue)
- le résumé/aperçu (respecter le genre et le ton)

### Étape 5 : Créer ou mettre à jour le fichier

Écris le profil du personnage dans `characters/[character-name].md` au format markdown. Reprends le style et la structure existants des autres fichiers de personnages.

## Flux de planification de l'histoire

### Étape 1 : Évaluer l'état de la planification

Lis les documents de planification existants pour comprendre :
- le concept et la prémisse de l'histoire
- les points d'intrigue ou le plan établis
- l'audience cible et le genre
- les thèmes et les questions centrales
- la structure prévue (le cas échéant)

Cherche dans des dossiers comme `story-planning/`, `outline/`, ou des fichiers comme `summary.md`.

### Étape 2 : Accéder à la référence des structures narratives

Pour une guidance structurelle détaillée, lis `references/story_structures.md` qui inclut :
- la structure en trois actes
- le Voyage du héros (monomythe de Campbell)
- la beat sheet Save the Cat
- les modèles d'arcs de personnage
- les composants de structure de scène
- les repères de rythme par genre
- les techniques d'intégration de sous-intrigues
- les structures propres à chaque genre

Utilise Grep pour trouver des frameworks précis :
```bash
# Example: Find Three-Act Structure details
grep -A 20 "Three-Act Structure" references/story_structures.md
```

### Étape 3 : Déterminer les besoins structurels

Selon la demande de l'utilisateur et le genre de l'histoire, recommande les frameworks appropriés :

- **Thriller/Mystère** : trois actes avec un retournement fort au milieu
- **Fantasy/Aventure** : Voyage du héros pour les récits de quête
- **Young Adult/Contemporain** : Save the Cat pour des beats émotionnels serrés
- **Littéraire** : focus sur la structure d'arc de personnage
- **Romance** : structure propre au genre avec beats de relation

### Étape 4 : Élaborer le document de planification

Crée ou enrichis les documents de planification avec :

**Aperçu de l'histoire**
- Prémisse en 2-3 phrases
- Genre, audience cible, ton
- Thèmes et questions centrales

**Structure de l'intrigue**
- Découpage en actes/chapitres avec événements clés
- Incident déclencheur et points d'intrigue
- Twist ou révélation au milieu
- Climax et résolution

**Arcs des personnages**
- Comment chaque personnage principal se transforme
- Intégration des arcs avec les beats de l'intrigue

**Éléments de world-building** (si applicable)
- Cadre et lieux
- Systèmes magiques ou technologie
- Structures ou règles sociales
- Contexte historique

**Chronologie**
- Durée de l'histoire
- Séquence des événements clés
- Considérations de rythme

### Étape 5 : Créer le fichier de planification

Écris les documents de planification dans `story-planning/[document-name].md`. Utilise une structure hiérarchique claire avec des en-têtes markdown pour une navigation facile.

## Flux d'écriture de chapitres & de scènes

### Étape 1 : Rassembler le contexte de l'histoire

Avant d'écrire tout contenu, lis de manière exhaustive :

**Fichiers de personnages** : tous les profils pertinents pour comprendre les voix, motivations, arcs
**Documents de planification** : structure de l'histoire, points d'intrigue, position actuelle dans l'histoire
**Chapitres précédents** : les chapitres récents pour maintenir la continuité (lis au moins 1-2 chapitres antérieurs)
**Résumé** : prémisse globale et thèmes de l'histoire

Cela garantit l'alignement du nouveau contenu avec les éléments établis.

### Étape 2 : Identifier les exigences du chapitre

Détermine :
- **Position dans l'histoire** : où cela s'insère-t-il dans la structure globale ?
- **Personnage POV** : de quel point de vue ?
- **Objectif de la scène** : que veut le personnage POV dans cette scène ?
- **Conflit** : qu'est-ce qui s'oppose à son objectif ?
- **Issue** : comment la scène se termine-t-elle ? (généralement par une complication)
- **Développement du personnage** : quels beats d'arc se produisent ici ?
- **Avancée de l'intrigue** : quelles questions narratives sont soulevées ou résolues ?

### Étape 3 : Structurer le chapitre

Applique les composants de structure de scène :

**Scène (Action)**
1. Objectif - Ce que poursuit le personnage POV
2. Conflit - Opposition rencontrée
3. Désastre - Issue négative qui fait avancer

**Séquelle (Réaction)**
1. Réaction - Réponse émotionnelle au désastre
2. Dilemme - Examen des options
3. Décision - Choix menant à l'objectif suivant

Alterne les beats de haute tension (action, conflit) et de basse tension (réflexion, world-building) pour le rythme.

### Étape 4 : Écrire avec la cohérence des personnages

Préserve la voix du personnage en te référant à :
- les traits de personnalité établis
- les façons de parler et le vocabulaire
- les schémas comportementaux (sous stress, quand il est heureux, style de prise de décision)
- la position actuelle dans l'arc du personnage
- les relations avec les autres personnages présents

### Étape 5 : Intégrer des marqueurs temporels

Inclus des références temporelles pour garder la clarté chronologique :
- Marqueurs explicites : « Jour 3 », « Deux semaines plus tard »
- Marqueurs implicites : moment de la journée, indices saisonniers, références à des événements
- Format : `**Timeline:** Day 5, Evening` dans l'en-tête du chapitre ou comme saut de section

### Étape 6 : Créer le fichier du chapitre

Écris le contenu du chapitre dans `chapters/chapter-[number].md` ou `chapters/[chapter-name].md`. Inclus :

**En-tête du chapitre**
```markdown
# Chapter [Number]: [Optional Title]

**Timeline:** [When this occurs]
**POV:** [Character name]
**Location:** [Where this takes place]
```

**Contenu du chapitre**
- Découpage scène par scène
- Dialogues et action
- Pensées du personnage (pour le POV)
- Éléments descriptifs

### Étape 7 : Noter les éléments de continuité

Après l'écriture, documente toute nouvelle information introduite :
- Révélations ou évolution de personnage
- Points d'intrigue ou indices
- Détails de world-building
- Événements chronologiques

Cela aide à maintenir la cohérence dans les chapitres futurs.

## Suivi de la chronologie

### Quand utiliser le suivi de la chronologie

Invoque le timeline tracker quand :
- l'utilisateur demande une analyse chronologique ou le séquençage des événements
- on vérifie la cohérence chronologique
- on planifie l'ordre des événements entre chapitres
- on identifie des périodes non marquées

### Exécuter le timeline tracker

Exécute le script depuis la racine du projet :

```bash
python3 .claude/skills/storyboard-manager/scripts/timeline_tracker.py . --output markdown
```

**Options de format de sortie :**
- `markdown` - Rapport lisible par l'humain (défaut)
- `json` - Données structurées pour traitement ultérieur

### Comprendre la sortie de la chronologie

Le script fournit :

**Statistiques**
- Nombre total d'événements suivis
- Nombre total de personnages apparaissant
- Événements par personnage

**Vue chronologique**
- Séquence chronologique des événements
- Emplacements chapitre/scène
- Personnages présents dans chaque événement
- Aperçu du contenu des événements

**Avertissements**
- Événements sans marqueur temporel
- Personnages mentionnés mais non définis dans les fichiers de personnages

### Agir sur les résultats de la chronologie

Après exécution du tracker :

1. **Examine les avertissements** - Traite les marqueurs temporels manquants en les ajoutant aux chapitres
2. **Vérifie la séquence** - Contrôle que les événements suivent un ordre logique
3. **Identifie les trous** - Repère les périodes sans événements
4. **Suivi des personnages** - Garantis que les personnages apparaissent en cohérence avec leur arc

Ajoute des marqueurs temporels aux chapitres où ils manquent :
```markdown
**Timeline:** Day 7, Morning
```

Ou utilise des marqueurs en ligne :
```markdown
Three days had passed since the incident...
```

## Vérification de cohérence

### Quand utiliser la vérification de cohérence

Invoque le consistency checker quand :
- l'utilisateur demande une analyse de cohérence
- on finalise des chapitres ou des actes
- des changements significatifs de personnage ou d'intrigue viennent d'être faits
- on traque des contradictions ou des erreurs

### Exécuter le consistency checker

Exécute le script depuis la racine du projet :

```bash
python3 .claude/skills/storyboard-manager/scripts/consistency_checker.py . --output markdown
```

**Options de format de sortie :**
- `markdown` - Rapport lisible avec le détail des problèmes (défaut)
- `json` - Données structurées pour analyse programmatique

### Comprendre la sortie de cohérence

Le script identifie les problèmes selon trois niveaux de gravité :

**Critique (🔴)**
- Contradictions majeures nécessitant une attention immédiate
- Personnage apparaissant après sa mort
- Contradictions fondamentales de l'intrigue

**Avertissement (⚠️)**
- Incohérences potentielles à examiner
- Écarts d'âge
- Contradictions de description physique
- Conflits de relations

**Info (ℹ️)**
- Problèmes mineurs ou variations
- Incohérences de casse des noms
- Variations stylistiques

### Agir sur les résultats de cohérence

Pour chaque problème signalé :

1. **Lis les emplacements signalés** - Examine les fichiers spécifiques mentionnés
2. **Détermine la vérité** - Décide quelle version est correcte (le profil du personnage fait généralement foi)
3. **Mets à jour les fichiers** - Corrige les contradictions avec l'outil Edit
4. **Relance le checker** - Vérifie que les corrections ont résolu les problèmes

**Exemple de flux pour une incohérence d'âge de personnage :**
```markdown
Issue: Age inconsistency for Maya
- Profile: 18 years old
- Chapter 3: mentions "21-year-old Maya"

Fix: Edit chapter-3.md to change "21-year-old" to "18-year-old"
```

### Limites de la vérification de cohérence

Le checker automatisé détecte :
- les contradictions d'attributs physiques
- les écarts d'âge
- les variations de noms
- les faits de world-building basiques

Le checker ne peut pas détecter :
- les incohérences de personnalité subtiles
- les erreurs logiques complexes de l'intrigue
- les contradictions thématiques
- les évolutions de relations nuancées

La relecture manuelle reste essentielle pour une cohérence profonde.

## Bonnes pratiques

### Chargement progressif du contexte

Ne charge pas tous les fichiers de référence d'un coup. À la place :
1. Scanne d'abord la structure du projet
2. Ne lis que les fichiers de personnages pertinents pour la tâche en cours
3. N'accède à la documentation de référence que quand une guidance précise est nécessaire
4. Utilise Grep pour trouver des sections précises dans les gros fichiers de référence

### Préserver la voix du genre

Respecte le ton établi de l'histoire :
- **Young Adult** : présent, connexion émotionnelle immédiate, langage contemporain
- **Fantasy** : langage descriptif riche, intégration du world-building
- **Thriller** : phrases courtes, haute tension, détails sensoriels
- **Littéraire** : prose complexe, réflexion intérieure, éléments symboliques

Réfère-toi au summary.md pour identifier l'audience cible et ajuster en conséquence.

### Intégration des arcs de personnages

Chaque chapitre doit servir les arcs des personnages :
- Suis où chaque personnage en est dans son arc
- Montre un changement progressif, pas une transformation soudaine
- Utilise les événements de l'intrigue pour éprouver les croyances du personnage
- Démontre la croissance à travers les choix et le comportement

### Équilibrer montrer vs raconter

Pour l'écriture narrative :
- **Montre** les émotions par les actions, les dialogues, les réactions physiques
- **Raconte** pour compresser le temps, fournir l'information nécessaire efficacement
- Utilise une description filtrée par le personnage (que remarquerait ce personnage POV ?)

### Gérer les POV multiples

Quand l'histoire a plusieurs points de vue :
- Crée des voix distinctes pour chaque personnage POV
- Garantis que chaque section POV fait avancer à la fois l'arc du personnage et l'intrigue
- Varie la structure de phrases et le vocabulaire selon le personnage
- Suis ce que chaque personnage sait ou ne sait pas

## Demandes utilisateur courantes & réponses

### « Aide-moi à développer le passé d'un personnage »
1. Lis les fichiers de personnages existants pour le contexte
2. Lis le profil du personnage (s'il existe) pour l'enrichir
3. Accède à la référence character_development.md pour le framework de passé
4. Crée un passé détaillé couvrant : fantôme/blessure, relations formatives, histoire clé
5. Intègre-le à son arc de personnage et à son rôle dans l'histoire

### « Écris le prochain chapitre »
1. Lis summary.md et les documents de planification de l'histoire
2. Lis tous les profils des personnages apparaissant dans le chapitre
3. Lis les 2 chapitres précédents pour la continuité
4. Identifie la position du chapitre dans la structure de l'histoire
5. Écris le chapitre avec la structure scène/séquelle
6. Inclus les marqueurs temporels et les en-têtes POV/lieu

### « Décris le plan de l'acte 2 »
1. Lis le résumé et les documents de planification existants
2. Accède à story_structures.md pour la guidance structurelle
3. Identifie les exigences de l'acte 2 (complications, milieu, tension montante)
4. Crée un plan beat par beat aligné avec les arcs des personnages
5. Note comment l'intrigue et les arcs de personnages se croisent

### « Vérifie la cohérence de mon histoire »
1. Exécute le script consistency_checker.py
2. Examine la sortie identifiant les problèmes
3. Lis les fichiers signalés pour comprendre les contradictions
4. Recommande des corrections précises pour chaque problème
5. Propose d'effectuer les modifications si l'utilisateur confirme

### « Suis la chronologie de mon histoire »
1. Exécute le script timeline_tracker.py
2. Examine la sortie montrant la séquence d'événements
3. Identifie les trous ou incohérences chronologiques
4. Recommande d'ajouter des marqueurs temporels où ils manquent
5. Fournis un résumé chronologique organisé par personnage ou chapitre

### « Quelle structure utiliser pour mon thriller ? »
1. Accède à la référence story_structures.md
2. Recommande la structure en trois actes ou Save the Cat
3. Explique les exigences propres au thriller (tension croissante, compte à rebours)
4. Fournis une beat sheet adaptée à son concept d'histoire
5. Propose de créer un document de planification détaillé

## Ressources

### scripts/timeline_tracker.py
Script Python qui analyse les fichiers markdown pour extraire et organiser les événements chronologiques. Suit les apparitions des personnages, identifie les marqueurs temporels, regroupe les événements par ordre chronologique et signale les problèmes de cohérence.

**Utilisation :** exécuter depuis la racine du projet avec `python3 .claude/skills/storyboard-manager/scripts/timeline_tracker.py .`

### scripts/consistency_checker.py
Script Python qui détecte les incohérences de détails de personnages, de descriptions physiques, d'âges, de noms et de faits de world-building dans tous les fichiers de l'histoire. Produit les problèmes classés par gravité avec leurs emplacements fichiers.

**Utilisation :** exécuter depuis la racine du projet avec `python3 .claude/skills/storyboard-manager/scripts/consistency_checker.py .`

### references/character_development.md
Framework complet pour créer des personnages multidimensionnels : éléments centraux, structure du passé, types d'arcs, dynamique des relations, développement de la voix et règles de cohérence.

**Charger quand :** création de nouveaux personnages, enrichissement de profils existants, résolution de problèmes de cohérence de personnage ou planification d'arcs de personnages.

### references/story_structures.md
Référence détaillée couvrant les grandes structures narratives (trois actes, Voyage du héros, Save the Cat), les modèles d'arcs de personnage, la structure de scène, les repères de rythme, les techniques de développement de l'intrigue et les structures propres à chaque genre.

**Charger quand :** planification du plan de l'histoire, structuration des actes, organisation des beats de l'intrigue, détermination du rythme ou application de frameworks narratifs précis.
