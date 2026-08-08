---
name: gen-plan
version: 3.3.0
date: 2026-07-29
authors: [Z AI, Francois]
description: >
  Planification et orchestration multi-etapes de taches complexes. Analyse la
  conversation/projet, decompose en sous-taches, selectionne l'agent ou skill
  optimal pour chaque phase, et execute en mode serie. Integre automatiquement
  les fichiers de skills/ecosysteme dans z.ai. Use when the user says
  "gen-plan", "plan d'actions", "correct-work", "orchestre", or requests
  structured multi-step execution. V3.3.0 : registre de skills personnalise
  (knowledge base), protocole de decouverte dynamique, scan automatique des
  skills externes a l'Etape 4, guide de selection etendu avec skills KB,
  matrice agents/skills dynamique, compatibilite ascendante v3.2.0.
---

# gen-plan v3.3.0

Skill d'orchestration et de planification structuree pour taches complexes multi-etapes.
Version 3.3.0 : protocole 15 etapes avec decomposition precoce (etape 2),
etape d'invocation gen-plan (etape 3), orchestration d'agents performance-driven,
lecture bloc par bloc (E4), paradigme CoT+Chaining avec auto-correction,
gestion des tokens pour conversations longues, **registre de skills personnalise
avec protocole de decouverte dynamique des skills externes (knowledge base)**.

## Declencheurs

- `gen-plan:` suivi d'une description de tache
- `gen-plan:correct-work(projet)` -- verification et correction d'un projet complet
- `gen-plan:correct-work(<cible>)` -- verification/correction d'un element specifique
- `plan d'actions` -- demande explicite de planification
- `orchestre` -- orchestration multi-agents
- Toute demande impliquant plusieurs etapes sequentielles avec des livrables
- `gen-plan:generate(<description>)` -- generation d'un plan auto-executable

## Modes

| Mode | Declencheur | Comportement |
|------|-------------|--------------|
| **TACHE** | `gen-plan: <description>` | Planifie et execute une tache specifique |
| **PROJET** | `gen-plan:correct-work(projet)` | Analyse complete du projet, corrections, mise a jour prompt-master |
| **CIBLE** | `gen-plan:correct-work(<cible>)` | Verification/correction d'un element specifique |
| **GENERATE** | `gen-plan:generate(<description>)` | Genere un plan d'actions structure sans l'executer |

## Philosophie

1. **Read before planning** -- Toujours lire le projet avant de planifier. Un plan sans
   connaissance du projet est generique et probablement inadequat. La lecture exhaustive
   est un investissement necessaire.
2. **Performance-driven selection** -- Le choix entre skill, agent specialise ou agent
   general est dicte par le gain de performance, pas par une hierarchie rigide.
   Evaluer quelle combinaison produit le meilleur resultat en moins de temps pour chaque
   sous-tache. Un skill avec un protocole pertinent bat toujours un agent nu ; un agent
   specialise bat toujours le general-purpose -- MAIS un skill peut aussi deleguer a un
   agent specialise en interne si cette combinaison produit de meilleurs resultats.
3. **Skills can launch specialized agents** -- Les skills ne sont pas des terminaisons
   mais des orchestrateurs. Un skill charge peut lancer en interne un agent specialise
   (full-stack-developer, ppt-expert, frontend-styling-expert, etc.) quand la sous-tache
   le requiert. Cela cree un modele a deux couches : **Skill (protocole + connaissances
   domaine) -> Agent Specialise (execution)**. Le skill fournit le "comment" (protocole,
   templates, criteres de qualite) ; l'agent fournit le "qui" (capacites specialisees,
   outils, vitesse).
4. **Serial execution by DEFAULT** -- Toutes les taches s'executent UNE A LA UNE dans
   l'ordre defini. Le parallelisme est INTERDIT sauf demande explicite de l'utilisateur
   ET preuve que les sous-taches sont independantes (pas de fichiers partages, pas de
   dependance causale).
5. **Visible progress** -- L'utilisateur sait toujours quelle phase est en cours, ce qui
   est termine, et ce qui vient ensuite.
6. **CoT + Chaining avec auto-correction** -- Chaque etape est executee avec un
   raisonnement structure (Chain-of-Thought) avant l'action. Le chainage des etapes
   suit un pipeline hierarchique ou chaque sortie est verifiee et corrigee avant de
   passer a la suivante. En cas d'echec, le systeme propose une strategie alternative
   avant de demander a l'utilisateur. Inspire du SUPER-AGENT HYBRIDE CoT + CHAINING_v2.
7. **Lecture bloc par bloc** -- Les fichiers volumineux (> 500 lignes) sont lus par
   blocs successifs avec une synthese intermediaire a chaque bloc, evitant la surcharge
   de contexte et garantissant une couverture totale.

## Registre de Skills Personnalise (Knowledge Base)

### Concept

En plus des skills natifs de l'ecosysteme z.ai, gen-plan peut utiliser des skills
personnalises stockes dans une **knowledge base externe**. Cela permet a
l'utilisateur d'etendre les capacites de planification avec ses propres skills,
agents specialises et protocoles maison.

### Declaration du Registre

Le registre est declare dans la section "Registre KB" ci-dessous. Chaque entree
specifie :

- **Chemin KB** : Emplacement de la knowledge base sur la machine locale
- **Chemin z.ai** : Emplacement equivalent dans l'environnement z.ai (si applicable)
- **Scan depth** : Profondeur de scan pour la decouverte des skills

### Registre KB (configurable)

| Parametre | Valeur |
|-----------|--------|
| **Chemin KB (Windows)** | `C:\Users\PC\Downloads\knowledge\skills` |
| **Chemin z.ai (Linux)** | `/home/z/my-project/skills/` |
| **Scan depth** | 2 niveaux (racine + 1 sous-dossier) |
| **Fichier detect** | `SKILL.md` ou tout `.md` avec YAML frontmatter (name, description) |
| **Priorite** | Les skills KB sont evalues APRES les skills ecosysteme z.ai |
| **Overlap** | Si un skill KB a le meme nom qu'un skill ecosysteme, le skill **ecosysteme**
  est prioritaire sauf si l'utilisateur specifie explicitement le skill KB |

**NOTE** : Le "Chemin z.ai (Linux)" pointe vers le repertoire ecosysteme natif.
Lors du scan KB, gen-plan detectera les skills ecosysteme ET les skills utilisateur
dans le meme repertoire. Pour distinguer les skills KB des skills ecosysteme,
gen-plan maintient une liste interne des skills ecosysteme natifs (ceux presents
avant le scan KB). Tout skill trouve qui n'est pas dans cette liste interne est
considere comme un skill KB. Si l'utilisateur souhaite separer physiquement ses
skills KB des skills ecosysteme, il peut utiliser un sous-repertoire dedie
(ex : `/home/z/my-project/skills-kb/`) et mettre a jour le "Chemin z.ai" en
consequence.

### Protocole de Decouverte de Skills (Knowledge Base)

Ce protocole definit comment gen-plan decouvre et evalue les skills de la
knowledge base externe.

**Etapes de decouverte** :

1. **Scanner le repertoire KB** : Lister tous les sous-repertoires contenant un
   fichier `SKILL.md` ou un fichier `.md` avec un YAML frontmatter valide.
2. **Construire la liste de reference (skills ecosysteme natifs)** : Avant le scan,
   lister les skills deja presents dans le repertoire cible. Ces skills constituent
   la "baseline" ecosysteme. Tout skill detecte lors du scan qui figure dans cette
   baseline est tague "Ecosysteme". Les autres sont tagues "KB".
3. **Extraire les metadonnees** : Pour chaque skill detecte, lire le frontmatter
   YAML pour extraire : `name`, `version`, `description`, `requires` (dependances
   inter-skills).
4. **Classifier le skill** :
   - **Skill executable** : Possede un protocole complet (declencheurs, etapes,
     checklist) -- peut etre utilise directement.
   - **Skill de reference** : Document de reference, template, configuration --
     consulte mais pas execute comme un protocole.
   - **Agent specialise KB** : Skill definissant un agent avec des capacites
     specifiques (prompt, outils, contraintes).
5. **Construire le registre dynamique** : Fusionner les skills KB avec les skills
   ecosysteme dans une liste unifiee, ordonnee par pertinence. Chaque skill est
   tague "Ecosysteme" ou "KB" selon la baseline construite a l'etape 2.
6. **Evaluer la compatibilite** : Verifier que les dependances inter-skills
   sont satisfaites (ex : correct-work requiert gen-plan >=3.1.0).
7. **Presenter a l'utilisateur** : Afficher la liste des skills KB detectes et
   leur classification avant de proceder.

**Format du registre dynamique en sortie** :

```
## Skills KB Detectes
| Skill | Version | Type | Chemin KB | Compatibilite |
|-------|---------|------|-----------|---------------|
| gen-plan | 3.3.0 | Executable | /skills/gen-plan/ | OK |
| correct-work | 2.2.0 | Executable | /skills/correct-work/ | OK (requiert gen-plan >=3.1.0, integre Registre KB v3.3.0) |
| [custom-skill] | x.x.x | Executable/Ref/Agent | /skills/[custom]/ | OK/N/A |

## Skills Ecosysteme z.ai (references)
[liste des skills ecosysteme pertinents pour le projet]
```

**Regle de priorite** :

1. Si l'utilisateur specifie explicitement un skill KB (`gen-plan: utiliser le skill X de ma KB`),
   le skill KB est prioritaire.
2. Si un skill KB et un skill ecosysteme ont le meme nom, le skill **ecosysteme** est
   prioritaire (sauf override explicite).
3. Si aucun skill ecosysteme ne correspond mais un skill KB correspond, le skill KB est utilise.
4. Les skills KB sont toujours evalues apres les skills ecosysteme dans la matrice de decision.

**Integrer un skill KB dans le plan** :

Lorsqu'un skill KB est selectionne pour une sous-tache :
- Charger le `SKILL.md` du skill KB comme reference de protocole.
- Si le skill KB definit un agent specialise, l'utiliser comme executeur.
- Respecter les dependances et versions declarees dans le frontmatter du skill KB.
- Logger l'utilisation du skill KB dans le worklog avec son chemin d'origine.

---

## Protocole -- 15 Etapes Sequentielles

Le skill s'execute en suivant les etapes sequentielles ci-dessous. L'ordre est important :
il faut **collecter les demandes, puis decomposer immediatement, puis lire le projet
pour nourrir la decomposition**. La decomposition precoce (etape 2) guide toute l'analyse
subsequente en fournissant une structure cible a verifier.

**Changement v3.0.0** : L'ancienne "Etape 5 -- Decomposition en Sous-taches" est desormais
en position 2 (apres la collecte des demandes). Une nouvelle "Etape 3 -- Invocation de
gen-plan" decrit le protocole d'appel recursif/chainable sans creer de dependance circulaire.

### Etape 1 -- Collecte et Analyse des Demandes

**Objectif** : Relire toute la conversation pour extraire chaque demande explicite et implicite.

**Checklist** :

1. Relire tous les messages utilisateur (demandes initiales, specs, contraintes, corrections).
2. Identifier les demandes explicites (ce que l'utilisateur a directement demande).
3. Identifier les demandes implicites (prerequis, effets de bord, consequences logiques).
4. Lister chaque demande sans ambiguite.

**Methode** :

- Relire toute la conversation pour extraire chaque demande.
- Si un fichier de travail (`worklog.md`) existe, l'utiliser pour comprendre le contexte.

### Etape 2 -- Decomposition en Sous-taches

**Objectif** : Decomposer chaque demande en sous-taches atomiques, avec un ordre logique
d'execution. Cette decomposition initiale guide toute l'analyse subsequente.

**Pourquoi en position 2 ?** La decomposition precoce oblige a structurer la reflexion
des le depart. L'analyse du projet (etape 4) et l'identification de la nature (etape 5)
viendront ensuite pour affiner, valider ou corriger cette premiere decomposition.

**Checklist** :

1. Pour chaque demande identifiee (Etape 1), identifier les sous-taches atomiques necessaires.
2. Ordonner les sous-taches logiquement (prerequis d'abord, puis execution, puis validation).
3. Adapter les sous-taches au type de projet si deja connu :
   - **Projet fullstack** : inclure la verification API frontend-backend, schema BDD, auth.
   - **Projet frontend only** : inclure la verification responsive, accessibilite, composants.
   - **Projet backend/API** : inclure la verification endpoints, validation, securite.
   - **Document/PDF** : inclure la verification contenu, mise en page, coherence des donnees.
   - **Script/automatisation** : inclure la verification edge cases, robustesse, gestion des erreurs.
   - **Auto-deploiement** : inclure la verification securite, integrite, codes retour, nettoyage.
4. Marquer les sous-taches qui necessitent une lecture approfondie du projet pour etre precisees.

**Methode** :

- Partir de chaque demande et la decomposer en etapes concretes.
- Verifier que chaque sous-tache est suffisamment precise pour etre executee de maniere autonome.
- **IMPORTANT** : Cette decomposition est **strictement hypothetique** -- elle se base UNIQUEMENT sur la demande de l'utilisateur et le type de projet suppose, SANS lire le code ni les fichiers du projet. Elle ne doit contenir que des suppositions raisonnables.
- Cette decomposition sera **exclusivement** affinee a l'Etape 7, apres que les Etapes 4, 5 et 6 auront fourni les donnees reelles du projet.

### Etape 3 -- Invocation de gen-plan (Protocole)

**Objectif** : Definir le protocole d'invocation de gen-plan par d'autres skills ou agents,
sans creer de dependance circulaire. Cette etape decrit COMMENT invoquer gen-plan, elle ne
l'execute pas.

**Principe** : gen-plan peut etre invoque de deux manieres :
1. **Directement** par l'utilisateur via les declencheurs (voir section "Declencheurs")
2. **Par un autre skill** (ex: correct-work) comme sous-protocole

**Protocole d'invocation par un skill externe** :

Quand un skill (ex: correct-work) souhaite invoquer gen-plan, il doit :

1. **Preparer le contexte** : Rassembler les demandes utilisateur pertinentes dans un format
   structure (liste de demandes avec priorites)
2. **Specifier le mode** : TACHE, PROJET, CIBLE, ou GENERATE
3. **Passer les parametres** :
   - `mode` : le mode d'execution choisi
   - `contexte` : resume du travail deja effectue (si applicable)
   - `cible` : element specifique a verifier (si mode CIBLE)
   - `fichiers_concernes` : liste des fichiers pertinents (si connus)
4. **Lancer gen-plan** : L'agent orchestrateur charge le skill gen-plan et l'execute
   selon son protocole 15 etapes
5. **Recevoir le plan** : gen-plan produit un plan structure (voir "Format de Sortie du Plan")
   que le skill appelant peut utiliser directement

**Anti-circularite** : Cette etape ne dit PAS "executer gen-plan maintenant". Elle dit
"voici le protocole SI un skill veut invoquer gen-plan". L'execution effective se fait
uniquement quand gen-plan est declenche par l'utilisateur ou par un skill appelant.

**Exemples d'utilisation** :
- `correct-work` appelle gen-plan en mode PROJET a son Etape 1
- `skill-creator` appelle gen-plan en mode TACHE pour planifier la creation d'un skill
- L'utilisateur ecrit `gen-plan: corriger les bugs du script de deploiement` (mode TACHE)

### Etape 4 -- Lecture et Analyse du Projet (avec Scan KB)

**Objectif** : Traverser tous les fichiers du projet pour comprendre structure, architecture,
dependances, etat actuel. **Inclus le scan de la Knowledge Base pour decouverte des
skills personnalises disponibles.**

**Principe cle** : Un plan sans connaissance du projet est un plan generique et probablement
inadapte. La lecture exhaustive est un investissement necessaire. En position 4, cette lecture
sert a **affiner la decomposition initiale** (Etape 2) avec la connaissance reelle du projet.

**Checklist** :

1. **Structure des fichiers** : parcourir l'arborescence, l'organisation des dossiers,
   les fichiers de config (package.json, tsconfig, next.config, tailwind, etc.).
2. **Code source** : lire chaque fichier source significatif (composants, routes, API,
   modeles, utilitaires, scripts) pour comprendre la logique implementee.
3. **Schema de base de donnees** (si applicable) : lire le schema Prisma ou equivalent.
4. **Dependances** : analyser package.json, les imports croises entre modules, les
   dependances externes et leurs versions.
5. **Configuration** : lire les fichiers de config pertinents.
6. **Documentation** : README, worklog.md, specifications, fichiers de reference.
7. **Assets et ressources** : images, templates, fichiers statiques pertinents.
8. **NOUVEAU v3.3.0 -- Scan Knowledge Base** : Scanner le repertoire de la knowledge base
   (chemin declare dans le "Registre KB") pour decouvrir les skills personnalises
   disponibles. Lister les skills detectes, extraire leurs metadonnees (name, version,
   description, type, dependances), et les classer (executable, reference, agent).
   Construire le registre dynamique fusionne (ecosysteme + KB).

**Methode** :

- Utiliser les outils de lecture de fichiers (Read, Glob, Grep) pour parcourir chaque
  fichier significatif du projet.
- Ne pas se limiter aux fichiers recemment modifies -- lire tout ce qui est pertinent
  pour comprendre le projet dans son ensemble.
- Si le projet est tres volumineux, prioriser la lecture des fichiers principaux et
  utiliser Grep pour les recherches ciblees.
- **NOUVEAU v3.3.0** : Pour le scan KB :
  - Utiliser Glob pour lister tous les `SKILL.md` ou `*.md` dans le repertoire KB.
  - Pour chaque fichier detecte, lire les 20 premieres lignes pour extraire le YAML
    frontmatter (name, version, description).
  - Classifier le skill selon son contenu (protocole executable vs reference vs agent).
  - Construire la liste fusionnee ecosysteme + KB.
  - Afficher le registre dynamique a l'utilisateur pour validation.

**Methode de lecture bloc par bloc** (fichiers > 500 lignes) :

1. Estimer la taille du fichier (nombre de lignes ou de caracteres).
2. Si le fichier depasse 500 lignes, le decouper en blocs de 200-300 lignes.
3. Lire le bloc 1 (lignes 1-300), produire une synthese des findings intermediaires.
4. Lire le bloc 2 (lignes 301-600), produire une synthese et comparer avec le bloc 1.
5. Continuer jusqu'a couverture totale du fichier.
6. Synthetiser l'ensemble des findings intermediaires en un rapport de lecture unifie.
7. Si le fichier depasse 2000 lignes, utiliser Grep pour cibler les sections pertinentes
   avant la lecture bloc par bloc, puis lire uniquement les blocs cibles.

Cette methode evite la surcharge de contexte tout en garantissant qu'aucune
section pertinente n'est ignoree.

- **Apres la lecture** : comparer les findings avec la decomposition de l'Etape 2 et
  ajuster si necessaire (sous-taches manquantes, incorrectes, ou superflues).

### Etape 5 -- Identification de la Nature du Projet

**Objectif** : Determiner le type de projet, ses technologies, son architecture et sa
complexite. Cette identification conditionne l'ensemble du plan d'actions.

**Checklist** :

1. **Type de projet** : application web, API, script, document, analyse, skill,
   auto-deploiement, etc.
2. **Technologies** : framework, langage, base de donnees, outils de build.
3. **Architecture** : monolithe, micro-services, fullstack, frontend only, backend only.
4. **Complexite** : nombre de fichiers, profondeur de l'arborescence, nombre de
   dependances, surface d'interaction.

**Methode** :

- Croiser les informations collectees aux etapes 1, 2 et 4 pour determiner la nature du projet.
- La classification n'est pas mutuellement exclusive : un projet peut etre "fullstack + micro-services"
  ou "document + script d'automatisation".

### Etape 6 -- Identification des Objectifs

**Objectif** : Lister explicitement chaque objectif a atteindre, sans ambiguite ni omission.
Les objectifs doivent etre specifiques au projet verifie.

**Checklist** :

1. Lister chaque objectif derive des demandes de l'utilisateur (Etape 1).
2. Lister les objectifs implicites (prerequis, effets de bord, contraintes).
3. Verifier que chaque objectif est mesurable (on peut dire s'il est atteint ou non).
4. Eliminer les doublons et les redondances.
5. **Croiser avec la decomposition de l'Etape 2** : chaque sous-tache doit correspondre
   a un objectif, et chaque objectif doit etre couvert par au moins une sous-tache.

**Methode** :

- Reprendre la liste des demandes (Etape 1) et la transformer en objectifs.
- Valider que chaque objectif est specifique au projet identifie (Etape 5).
- Verifier la coherence avec la decomposition preliminaire (Etape 2).

### Etape 7 -- Affinement de la Decomposition

**Objectif** : Affiner la decomposition preliminaire (Etape 2) a la lumiere de l'analyse
du projet (Etape 4), de la nature du projet (Etape 5) et des objectifs (Etape 6).

**Pourquoi cette etape ?** La decomposition de l'Etape 2 etait faite "a froid" sans connaitre
le projet. Maintenant que le projet est analyse et les objectifs identifies, il faut verifier
et corriger la decomposition.

**Checklist** :

1. Comparer la decomposition de l'Etape 2 avec les findings des Etapes 4-6
2. Ajouter les sous-taches manquantes revelees par l'analyse du projet
3. Supprimer les sous-taches superflues ou incorrectes
4. Re-ordonner si necessaire en fonction des dependances decouvertes
5. Verifier que chaque sous-tache est toujours atomique et autonome

**Methode** :

- Reprendre la liste de sous-taches de l'Etape 2 comme base
- **IMPORTANT** : Cette etape est le **SEUL endroit autorise** a modifier la decomposition de l'Etape 2. Aucune autre etape ne doit restructurer la liste des sous-taches.
- Chaque modification doit etre **justifiee par un finding specifique** des Etapes 4, 5 ou 6 (ex : "E4 a revele un fichier de config non detecte a E2, ajout de la sous-tache de verification de config").
- La version affinee devient la decomposition de reference pour les etapes suivantes

### Etape 8 -- Detection des Dependances

**Objectif** : Identifier les dependances entre sous-taches et les contraintes de precedence,
en tenant compte de l'architecture du projet.

**Checklist** :

1. Identifier les dependances sequentielles (A doit etre termine avant B).
2. Identifier les dependances paralleles (A et B peuvent etre executees en meme temps).
3. Identifier les dependances conditionnelles (B ne s'execute que si A echoue/reussit).
4. Verifier qu'il n'y a pas de dependances circulaires.

**Methode** :

- Construire un graphe de dependances (mental ou ecrit).
- Identifier les chemins critiques (sequence la plus longue de dependances sequentielles).

### Etape 9 -- Priorisation

**Objectif** : Classer les sous-taches par priorite en fonction de leur impact sur le
resultat final et de la nature du projet.

| Priorite | Definition |
|----------|------------|
| **Critique** | Echec invalide le resultat entier |
| **Importante** | Impact significatif sur qualite |
| **Secondaire** | Ameliore resultat mais non bloquant |

**Methode** :

- Evaluer l'impact de chaque sous-tache sur le resultat final.
- Prioriser en fonction du type de projet (ex : pour un projet avec BDD, la verification
  du schema est critique ; pour un document, la coherence du contenu est critique).

### Etape 10 -- Estimation des Risques

**Objectif** : Pour chaque sous-tache, identifier les risques potentiels et prevoir des
solutions de secours. Les risques doivent etre specifiques au contexte du projet.

**Checklist** :

1. **Complexite technique** : la sous-tache requiert-elle des competences ou des
   connaissances specifiques ?
2. **Ambiguite** : la sous-tache est-elle clairement definie ou sujette a interpretation ?
3. **Dependance externe** : la sous-tache depend-elle d'un service, d'une API ou d'un
   outil externe qui pourrait echouer ?
4. **Solution de secours** : que faire si la sous-tache echoue ? Contourner, reporter,
   simplifier ?

**Methode** :

- Pour chaque risque identifie, definir une strategie d'attenuation.
- Les risques doivent etre specifiques au contexte du projet (ex : risques de migration
  de schema pour un projet avec BDD, risques de compatibilite navigateur pour un frontend,
  risques de formatage pour un document).

### Etape 11 -- Structuration du Plan

**Objectif** : Produire un plan d'actions formel, complet et adapte au projet.

Le plan doit comprendre :

1. **En-tete** :
   - Nature du projet (type, technologies, architecture)
   - Objectifs principaux
   - Contraintes et hypotheses

2. **Liste ordonnee des etapes** avec identifiants (1, 2-a, 2-b, 3...) :
   - Pour chaque etape : objectif, fichiers concernes, dependances, priorite
   - Indication du parallelisme possible (etapes independantes executables en parallele)
   - Critere de validation pour chaque etape
   - **Adaptation au projet** : pour chaque etape, indiquer en quoi elle est specifique
     au type de projet verifie et quels points de verification particuliers s'appliquent

3. **Carte des dependances** : resume des relations entre etapes.

4. **Matrice des risques** : resume des risques et solutions de secours.

**Methode** :

- Structurer le plan selon le format ci-dessus.
- Verifier que le plan couvre tous les objectifs identifies.
- Verifier que l'ordre d'execution respecte les dependances.

### Etape 12 -- Validation du Plan

**Objectif** : Verifier que le plan est complet, coherent et adapte au projet.

**Checklist** :

1. Le plan couvre-t-il toutes les demandes de l'utilisateur ?
2. Y a-t-il des etapes manquantes ?
3. L'ordre d'execution est-il logique (pas de dependance non respectee) ?
4. Le plan est-il adapte au projet (pas de verification generique ignorant les specificites) ?
5. Chaque etape a-t-elle un critere de validation clair ?
6. Les risques principaux sont-ils couverts par des solutions de secours ?

**Methode** :

- Relire le plan en entier et verifier chaque point de la checklist.
- Si un probleme est detecte, revenir a l'etape concernee et corriger.

### Etape 13 -- Test et Correction Pre-Integration

**Objectif** : Tester chaque fichier genere ou modifie AVANT de l'integrer a l'ecosysteme.

Pour chaque fichier candidat a l'integration :

1. **Classifier le fichier** :
   - **Skill** : Fichier avec YAML frontmatter (name, description) ou contenu definissant
     un protocole/routine reutilisable
   - **Eco-systeme** : Fichier de configuration, prompt maitre, contexte, memoire, agent,
     ou tout fichier qui etend les capacites du systeme
   - **Utilitaire** : Script, outil, fichier temporaire -- ne pas integrer

2. **Tester le fichier** :
   - **Skill (.md avec YAML)** : Verifier que le YAML frontmatter est valide (name,
     description presents), que le contenu est coherent et complet (> 200 chars), qu'il
     ne contient pas de fragments ou de placeholders non resolus
   - **Python (.py)** : Compiler avec `compile()` ou `ast.parse()` pour verifier la syntaxe.
     Verifier les imports, les fonctions principales, l'absence de code mort evident
   - **Shell (.sh)** : Verifier le shebang (`#!/bin/bash`), la syntaxe avec `bash -n`,
     l'absence de commandes destructrices non gardees
   - **Markdown (.md)** : Verifier la structure (titres `#`, sections coherentes),
     l'absence de contenu tronque ou de fragments de code incomplets
   - **Configuration (.json, .yaml)** : Valider le format JSON/YAML, verifier les cles
     obligatoires

3. **Corriger les anomalies detectees** :
   - Si un test echoue, corriger le fichier immediatement
   - Si le fichier est un fragment trop petit (< 100 chars) ou incomplet, le marquer
     comme "invalide" et ne pas l'integrer
   - Si le fichier contient des artefacts de parsing (XML tags, balises `<parameter>`, etc.),
     les nettoyer
   - Documenter chaque correction dans le worklog

4. **Valider la coherence entre fichiers** :
   - Verifier que les references croisees entre fichiers sont valides
   - Verifier qu'un skill reference dans le prompt-maitre existe bien
   - Verifier qu'un agent mentionne dans la matrice de decision est bien defini

**Validation de scripts d'auto-deploiement** :

Pour tout script Python d'auto-deploiement (ex: auto_deploy_*.py), verifier en plus :
- **Securite** : Pas de `shell=True` sans validation, verification des telechargements
- **Integrite** : Verification des magic bytes des fichiers telecharges (MSI: `0xD0CF11E0`)
- **Codes retour** : Verification systematique de `returncode` de subprocess
  (jamais afficher `[SUCCESS]` si le code retour est non-zero)
- **Versions** : Verifier que les versions logicielles referencees existent
  (ex: Node.js 20.18.0 vs 20.18.1)
- **Robustesse** : Gestion des erreurs avec messages clairs en francais
- **Nettoyage** : Verification que les outils installes temporairement sont desinstalles
  en fin de script

### Etape 14 -- Integration Eco-Systeme (SPECIFIQUE z.ai)

**Objectif** : Si les fichiers concernent des skills ou l'ecosysteme, les integrer a
l'ecosysteme de z.ai.

**Prerequis** : Etape 13 (Test et Correction) doit etre terminee avec succes.

1. **Si le fichier est un Skill** :
   - Creer le repertoire `/home/z/my-project/skills/<skill-name>/` s'il n'existe pas
   - Y placer le fichier `SKILL.md` avec le contenu valide
   - Verifier la conformite du YAML frontmatter (name, description obligatoires)
   - **Ne jamais ecraser un skill existant sans confirmation utilisateur**
   - Si le skill existe deja, proposer un diff ou une mise a jour

2. **Si le fichier est un fichier d'Eco-systeme** :
   - **Prompt maitre / Contexte** : Sauvegarder dans `/home/z/my-project/skills/gen-plan/references/`
   - **Configuration memoire** : Sauvegarder dans `/home/z/my-project/skills/gen-plan/references/`
   - **Definitions d'agents** : Integrer dans la section agents du prompt maitre ou creer
     un fichier de reference
   - **Matrices de decision** : Sauvegarder dans `/home/z/my-project/skills/gen-plan/references/`

3. **Validation post-integration** :
   - Verifier que chaque fichier integre ne casse pas les skills existants
   - Verifier qu'il n'y a pas de conflit de noms
   - Mettre a jour l'inventaire des skills si necessaire
   - Logger l'integration dans `/home/z/my-project/worklog.md`

### Etape 15 -- Auto-Reapplication si gen-plan.SKILL.md Mis a Jour

**Objectif** : Si le fichier gen-plan.SKILL.md (ce fichier) est lui-meme mis a jour pendant
l'execution du plan, reappliquer la nouvelle version aux taches restantes.

**Regle de reapplication** :

1. Apres toute modification de ce fichier `SKILL.md` (mise a jour, correction, ajout de
   regles) :
   - **Marquer les taches restantes** avec le format : `[REEVALUER: <ID-phase> | Raison: <description de la modification> | Sections affectees: <liste>]`
   - **Recharger le skill** : relire l'integralite du fichier SKILL.md mis a jour
   - **Comparer les sections modifiees** avec les taches restantes : pour chaque tache restante non encore executee :
     - Verifier si la nouvelle version du skill modifie la maniere dont la tache doit etre executee
     - Si oui : reecrire le plan de la tache selon les nouvelles regles, enlever le tag `[REEVALUER]`
     - Si non : retirer le tag `[REEVALUER]` et executer tel quel
2. **Cas d'usage typiques de reapplication** :
   - Ajout d'une nouvelle regle de classification (ex: nouveau type de fichier a integrer)
   - Modification de la matrice de decision agent/skill
   - Ajout d'un nouveau critere de test dans l'etape 13
   - Correction d'un bug dans le protocole
3. **Logging** : Documenter chaque reapplication dans le worklog avec l'ID de la tache
   affectee et la raison de la reevaluation

---

## Orchestration d'Agents

Apres le plan valide (Etape 12), le presenter a l'utilisateur et offrir de l'executer :

> "Plan valide. Executer les phases en serie avec les agents specialises et skills ?"

Si l'utilisateur confirme, orchestrer l'execution.

### Matrice de Decision Agent/Skill

Pour chaque sous-tache, evaluer quelle combinaison produit le meilleur resultat :

```
1. Existe-t-il un SKILL correspondant ?
   |-- OUI -> Charger le skill
   |   |-- Le skill beneficie-t-il d'un agent specialise ?
   |       |-- OUI -> Skill + Agent Specialise (OPTIMAL)
   |       |-- NON -> Skill seul via agent general (BON)
   |-- NON -> Existe-t-il un agent specialise ?
       |-- OUI -> Agent Specialise seul
       |-- NON -> Agent general (DERNIER RECOURS)
```

### Criteres de Selection (ordonnes par impact performance)

1. **Skill + agent specialise** (meilleure performance) -- Un skill dont le protocole
   correspond a la tache ET qui delegue en interne a un agent specialise. Exemple :
   `fullstack-dev` charge, puis delegue a `full-stack-developer`. Le skill fournit
   templates, conventions, criteres de qualite ; l'agent fournit execution specialisee.
2. **Skill seul** (bonne performance) -- Un skill dont le protocole couvre entierement
   la tache sans besoin d'agent specialise. Exemple : `web-search` via `general-purpose`.
3. **Agent specialise seul** (performance moderee) -- Aucun skill correspondant, mais un
   agent specialise (Explore, Plan, frontend-styling-expert, ppt-expert) couvre la tache.
4. **Agent general** (fallback) -- Ni skill ni agent specialise ne convient.
   Ne jamais utiliser comme premier choix -- toujours verifier l'ecosysteme de skills d'abord.

**Insight cle** : Un skill n'est pas un remplacement pour un agent -- c'est un **accelerateur**.
Charger un skill donne a l'agent des connaissances domaine, des templates et des protocoles
de qualite. L'agent execute plus vite et mieux avec le skill charge que sans lui.

### Guide de Selection Agent/Skill

| Type Tache | Skill | Agent | Performance |
|------------|-------|-------|-------------|
| Dev web Next.js | fullstack-dev | full-stack-developer | Skill + Agent (OPTIMAL) |
| Creation PPT/slides | pptx | ppt-expert | Skill + Agent (OPTIMAL) |
| Generation PDF | pdf | general-purpose | Skill + Agent (OPTIMAL) |
| Comprehension images | VLM | general-purpose | Skill + Agent (OPTIMAL) |
| Charts/diagrammes | charts | general-purpose | Skill + Agent (OPTIMAL) |
| Documents Word | docx | general-purpose | Skill + Agent (BON) |
| Fichiers Excel | xlsx | general-purpose | Skill + Agent (BON) |
| Recherche web | web-search | general-purpose | Skill + Agent (BON) |
| Extraction web | web-reader | general-purpose | Skill + Agent (BON) |
| Creation skills | skill-creator | general-purpose | Skill + Agent (BON) |
| Generation images | image-generation | general-purpose | Skill + Agent (BON) |
| Edition images | image-edit | general-purpose | Skill + Agent (BON) |
| Speech-to-text | ASR | general-purpose | Skill + Agent (BON) |
| Text-to-speech | TTS | general-purpose | Skill + Agent (BON) |
| Video understanding | video-understand | general-purpose | Skill + Agent (BON) |
| LLM chat | LLM | general-purpose | Skill + Agent (BON) |
| Recherche images | image-search | general-purpose | Skill + Agent (BON) |
| Navigation web | agent-browser | general-purpose | Skill + Agent (BON) |
| Recherche skills (CN) | skill-finder-cn | general-purpose | Skill + Agent (BON) |
| Exploration fichiers | -- | Explore | Agent seul |
| Architecture/planif | -- | Plan | Agent seul |
| Styling CSS | -- | frontend-styling-expert | Agent seul |
| Codage/execution scripts | coding-agent | general-purpose | Skill + Agent (BON) |
| Review de tache | task-review | general-purpose | Skill + Agent (BON) |
| Gestion de versions | version-management | general-purpose | Skill + Agent (BON) |
| **Verification correction** | **correct-work** | general-purpose | Skill + Agent (BON) |

### Guide de Selection Agent/Skill -- Skills Knowledge Base (v3.3.0)

En plus du tableau ci-dessus (ecosysteme natif), gen-plan evalue les skills de
la knowledge base personnalisee de l'utilisateur. Le registre dynamique est
construit a l'Etape 4 via le Protocole de Decouverte.

**Processus de selection KB** :

```
1. Le registre dynamique (ecosysteme + KB) est-il construit (Etape 4, point 8) ?
   |-- NON -> Construire le registre maintenant (scan KB)
   |-- OUI -> Passer a l'evaluation
2. Un skill KB correspond-il a la sous-tache ?
   |-- OUI -> Le skill ecosysteme correspond-il aussi ?
   |   |-- OUI -> Skill ecosysteme prioritaire (sauf override utilisateur)
   |   |-- NON -> Skill KB selectionne
   |-- NON -> Utiliser le skill ecosysteme ou l'agent selon la matrice standard
```

**Tableau de selection KB** (dynamique, construit a l'Etape 4) :

| Type Tache | Skill KB | Skill Ecosysteme | Selection | Performance |
|------------|----------|------------------|-----------|-------------|
| [Tache X] | [skill-KB-name] | -- | Skill KB seul | Skill KB + Agent |
| [Tache Y] | [skill-KB-name] | [skill-eco] | Ecosysteme | Skill Eco + Agent |
| [Tache Z] | -- | [skill-eco] | Ecosysteme | Skill Eco + Agent |

**NOTE** : Ce tableau est dynamique et construit a chaque execution en fonction
des skills reels detectes dans la knowledge base de l'utilisateur.

**Forcer l'utilisation d'un skill KB** :

L'utilisateur peut forcer l'utilisation d'un skill KB en le specifiant explicitement :
- `gen-plan: [tache] avec le skill [skill-name] de ma KB`
- `gen-plan: [tache] --kb-skill=[skill-name]`

Dans ce cas, le skill KB est prioritaire meme si un skill ecosysteme existe.

### Regles d'Execution Orchestree

1. **Annoncer** chaque phase avant de commencer (avec mode : Skill+Agent / Skill / Agent / General)
2. **Marquer** la phase comme in_progress dans la todo list
3. **Verifier** s'il existe un skill correspondant -- si oui, le charger
4. **Evaluer** si le skill peut lancer un agent specialise pour meilleure performance
5. **Lancer** l'agent avec une description de tache autonome incluant les exigences du skill
6. **Attendre** la completion totale avant d'envisager la phase suivante
7. **Verifier** les outputs -- fichiers/artefacts produits
8. **Logger** les resultats dans worklog (mode d'execution inclus)
9. **Marquer** la phase comme terminee et annoncer la suivante

**Checklist d'evaluation performance (par sous-tache)** :

| Question | Si OUI | Si NON |
|----------|--------|--------|
| Un skill correspondant existe ? | Le charger -> evaluer besoin agent | Passer a la recherche d'agent |
| Skill + agent specialise > skill seul ? | Deleguer a l'agent specialise | Utiliser le skill directement |
| Agent specialise > agent general ? | Utiliser l'agent specialise | Utiliser l'agent general |

### Gestion des Erreurs et Auto-Correction (CoT + Chaining)

**Principe CoT+Chaining** : Chaque etape du plan est executee en suivant le cycle
Raisonnement -> Action -> Verification -> Correction (inspire du SUPER-AGENT
HYBRIDE CoT + CHAINING_v2). Ce n'est pas une simple execution lineaire mais un
pipeline intelligent ou chaque sortie est evaluee avant de nourrir l'entree suivante.

**Cycle d'execution par etape** :

1. **Raisonnement (CoT)** -- Avant d'executer l'action, expliciter le raisonnement :
   - Quel est l'objectif precis de cette etape ?
   - Quelles sont les contraintes identifiees ?
   - Quelle strategie a ete choisie et pourquoi ?
2. **Action** -- Executer l'etape selon la strategie definie.
3. **Verification** -- Evaluer le resultat produit :
   - Le resultat correspond-il a l'objectif ?
   - Y a-t-il des artefacts, des incoherences, des omissions ?
4. **Auto-correction** -- Si la verification echoue :
   - Corriger le resultat directement si l'anomalie est mineure.
   - Proposer une strategie alternative si l'anomalie est majeure.
   - Documenter la correction dans le worklog.

**Si une phase echoue apres auto-correction** :
1. Logger l'echec dans worklog avec details erreur + tentative(s) de correction
2. Annoncer l'echec a l'utilisateur avec le diagnostic
3. Proposer des options : retry avec strategie alternative, changer d'agent/skill, ou skip
4. **NE PAS continuer silencieusement** a la phase suivante
5. Si retry, evaluer si un autre type de skill/agent pourrait resoudre le probleme
6. Documenter chaque tentative dans le worklog (cycle CoT complet)

---

## Template de Phase

```markdown
## PHASE [ID] -- [Titre]

**Objectif** : [Ce que cette phase accomplit]
**Mode** : [Skill+Agent / Skill / Agent / General]
**Dependances** : [Phases precedentes requises]
**Priorite** : [Critique / Importante / Secondaire]

**Tache :**
[Description claire]

**Skill a charger (si applicable) :**
- Nom : [skill-name]
- Chemin : /home/z/my-project/skills/[skill-name]/SKILL.md

**Fichiers concernes :**
- [Liste des fichiers a lire/ecrire/modifier]

**Outputs attendus :**
- [Artefacts specifiques a produire]

**Criteres de validation :**
- [Comment verifier que cette phase a reussi]
```

### Template de Description de Tache (pour delegation agent)

```
Execute this task:
- Task ID: [global-phase-id, e.g. "2-b"]
- Phase: [phase name]
- Execution mode: [Skill+Agent / Skill / Agent / General]
- Performance rationale: [why this mode is optimal for this subtask]

**Context:**
[What has been done so far, relevant context from previous phases]

**Task:**
[Clear description of what this phase should accomplish]

**Skill to load (mandatory if applicable):**
- Skill name: [e.g. "pdf", "charts", "fullstack-dev"]
- Skill path: [e.g. /home/z/my-project/skills/pdf/SKILL.md]
- Key skill requirements to pass to the agent: [extracted from skill instructions]
- Can the skill delegate to a specialized agent for better performance?
  |-- YES -> Agent type: [e.g. "full-stack-developer", "ppt-expert"]
  |-- NO  -> Execute via general-purpose agent

**Inputs:**
- [File paths, parameters, or artifacts from previous phases]

**Expected outputs:**
- [Specific files or artifacts to produce]
- Save to: [exact output path]

**Quality criteria:**
- [How to verify this phase succeeded]

**Execution mode:**
- Serial: YES (mandatory unless explicitly exempted)
- Wait for completion: YES

**Instructions:**
- Read /home/z/my-project/worklog.md first for previous phase context
- Append your work log to /home/z/my-project/worklog.md when done
- Return a summary of what was accomplished (include which execution mode was used)
```

---

## Format de Sortie du Plan

```markdown
## Plan d'actions -- [Nom du projet]

### Nature du projet
- Type : [fullstack / frontend / backend / document / script / auto-deploiement / ...]
- Technologies : [framework, langage, BDD, ...]
- Architecture : [monolithe / micro-services / ...]
- Complexite : [faible / moyenne / elevee]

### Objectifs
1. [Objectif 1]
2. [Objectif 2]

### Etapes

#### 1. [Titre de l'etape]
- **Objectif** : ...
- **Fichiers concernes** : ...
- **Dependances** : aucune / apres etape X
- **Priorite** : critique / importante / secondaire
- **Critere de validation** : ...
- **Adaptation au projet** : ...

#### 2-a. [Titre] (parallele avec 2-b)
- ...

### Carte des dependances
[Schema ou description des dependances entre etapes]

### Matrice des risques
| Etape | Risque | Probabilite | Impact | Solution de secours |
|-------|--------|-------------|--------|---------------------|

### Validation du plan
- [x] Couverture des demandes : OUI/NON
- [x] Absence d'etapes manquantes : OUI/NON
- [x] Ordre logique : OUI/NON
- [x] Adaptation au projet : OUI/NON
- [x] Criteres de validation : OUI/NON
- [x] Couverture des risques : OUI/NON
**Plan valide** : OUI / NON
```

---

## Regles d'Execution

- **Serielle par defaut** : Un maximum de taches s'executent en serie, une a la
  fois, dans l'ordre defini. Le parallelisme est INTERDIT sauf demande explicite
  de l'utilisateur ET preuve que les sous-taches sont independantes (pas de fichiers
  partages, pas de dependance causale). L'execution serie maximise la qualite et la
  coherence du resultat global.
- **Quality gates** : Validation apres chaque phase avant de continuer
- **Worklog** : Mettre a jour `/home/z/my-project/worklog.md` apres chaque phase
- **Communications** : L'utilisateur sait toujours ou on en est (progression visible)
- **Tester avant d'integrer** : Aucun fichier n'est integre a l'ecosysteme sans avoir
  passe les tests de l'Etape 13
- **Auto-reapplication** : Si ce skill est mis a jour en cours d'execution, les taches
  restantes sont reevaluees a la lumiere de la nouvelle version (Etape 15)
- **Gestion des tokens** : Si la synthese intermediaire de l'Etape 4 depasse **8000 mots** pour un seul bloc, activer le mode lecture bloc par bloc (decouper en blocs de 200-300 lignes, synthetiser chaque bloc en **500 mots maximum**). Si la conversation est si longue que le contexte risque d'etre sature avant la fin de l'execution, hierarchiser les syntheses : synthese par section, puis synthese des syntheses. Prioriser la qualite sur l'exhaustivite quand le contexte est contraint.
- **CoT+Chaining** : Chaque etape suit le cycle Raisonnement -> Action ->
  Verification -> Correction (voir section Gestion des Erreurs et Auto-Correction).

---

## Relations avec les Autres Skills

| Skill | Relation | Peut lancer un Agent ? | Source |
|-------|----------|----------------------|--------|
| **correct-work** | Appelle gen-plan a son Etape 1 | -- | Ecosysteme |
| **skills-inventory** | gen-plan scanne l'inventaire a l'Etape 4 | -- | Ecosysteme |
| **skill-creator** | gen-plan delegue la creation de skills | `general-purpose` | Ecosysteme |
| **fullstack-dev** | gen-plan produit des plans pour projets fullstack | `full-stack-developer` | Ecosysteme |
| **pptx** | gen-plan delegue la creation de slides | `ppt-expert` | Ecosysteme |
| **charts** | gen-plan delegue la creation de chartes/visualisations | `general-purpose` | Ecosysteme |
| **pdf / docx / xlsx** | gen-plan delegue la creation de documents | `general-purpose` | Ecosysteme |
| **web-search / web-reader** | gen-plan delegue la recherche/extraction | `general-purpose` | Ecosysteme |
| **image-generation / image-edit** | gen-plan delegue les taches image | `general-purpose` | Ecosysteme |
| **ASR / TTS / VLM / LLM** | gen-plan delegue les taches media/AI | `general-purpose` | Ecosysteme |
| **video-understand** | gen-plan delegue les taches d'analyse video | `general-purpose` | Ecosysteme |
| **Skills KB** | gen-plan scanne et evalue les skills de la knowledge base a l'Etape 4 | Variable | Knowledge Base |
| **Tous les skills** | gen-plan evalue le gain de performance skill+agent vs skill seul vs agent seul | Variable | Ecosysteme + KB |

---

## Metriques de Qualite du Plan

Un plan genere par ce skill est evalue selon les metriques suivantes. Ces metriques aident a juger de la qualite objective du plan, au-dela de l'evaluation subjective.

| Metrique | Definition | Seuil acceptable |
|----------|------------|------------------|
| Taux de couverture | Nombre de demandes utilisateur couvertes par au moins une sous-tache / Nombre total de demandes | 100% |
| Phases avec critere de validation | Nombre de phases ayant un critere de validation explicite / Nombre total de phases | >= 80% |
| Correspondance nature du projet | Nombre de points de verification adaptes au type de projet / Nombre total de phases | >= 60% |
| Couverture des risques | Nombre de phases avec un risque identifie et une solution de secours / Nombre total de phases | >= 50% |
| Dependances respectees | Toute phase qui depend d'une autre est listee apres sa dependance | 100% (0 violation) |

Ces metriques sont verifiees a l'Etape 12 (Validation du Plan). Si un seuil n'est pas atteint, le plan doit etre corrige avant d'etre presente a l'utilisateur.

---

## Limites Connues

Ce skill a les limites suivantes, qu'il est important de connaitre pour l'IA qui l'execute :

1. **Pas d'execution parallele native** : Le protocole est strictement serie. Le parallelisme n'est possible que si l'utilisateur le demande explicitement et prouve l'independance des sous-taches. gen-plan ne detecte pas automatiquement les opportunites de parallelisme.

2. **Pas de persistance entre sessions** : Le plan genere n'est pas persiste dans une base de donnees. Si la session est reinitialisee, le plan est perdu. Seul le worklog fournit une trace partielle.

3. **Pas de verification d'execution reelle** : gen-plan planifie et orchestre, mais il ne verifie pas que le code produit fonctionne reellement (pas de test unitaire, pas de linter, pas de compilation). Cette verification incombe aux skills d'execution (fullstack-dev, coding-agent, etc.) ou a correct-work.

4. **Dependance a la qualite de la demande** : Si la demande de l'utilisateur est ambigue ou incomplete, le plan reflétera cette ambiguite. gen-plan ne remplace pas une specification formelle.

5. **Matrice de selection semi-dynamique (v3.3.0)** : La partie ecosysteme du "Guide de Selection Agent/Skill" reste statique. La partie Knowledge Base est dynamique (construite a l'Etape 4). Si de nouveaux skills sont ajoutes a l'ecosysteme natif, la matrice statique doit etre mise a jour manuellement. En revanche, les skills KB sont decouverts automatiquement a chaque execution.

6. **Accessibilite de la Knowledge Base (v3.3.0)** : Le scan de la knowledge base suppose que les fichiers sont accessibles depuis l'environnement d'execution. Si le chemin KB n'est pas accessible (ex : chemin Windows dans un environnement Linux sans montage), le scan est saute et seuls les skills ecosysteme sont utilises. L'utilisateur est informe du skip.

---

## Compatibilite de Version

| Skill dependant | Version requise de gen-plan |
|-----------------|---------------------------|
| correct-work v2.2.0 | >= 3.1.0 |

Si un skill dependant specifie un champ `requires_gen_plan_version` dans son frontmatter, verifier la compatibilite avant l'invocation.

---

## Historique des Versions

| Version | Date | Auteurs | Modifications |
|---------|------|---------|---------------|
| 3.3.0 | 2026-07-29 | Z AI + Francois | Ajout registre de skills personnalise (Knowledge Base). Protocole de decouverte dynamique des skills externes. Etape 4 enrichie avec scan KB automatique. Guide de selection etendu avec skills KB et regles de priorite (ecosysteme > KB sauf override). Matrice agents/skills semi-dynamique. Compatibilite ascendante v3.2.0 preservee. |
| 3.2.0 | 2026-07-25 | Z AI + Francois | Optimisation : frontiere E2/E7 clarifiee, matrice agents/skills alignee sur l'ecosysteme reel, metriques de qualite, gestion tokens operationnelle, mecanisme E15 concret, limites connues, compatibilite de version. |
| 3.1.0 | 2026-07-10 | Z AI + Francois | Lecture bloc par bloc pour fichiers volumineux (E4). Paradigme CoT+Chaining avec auto-correction inspire du SUPER-AGENT HYBRIDE. Gestion des tokens pour conversations longues. Execution serie maximale renforcee. |
| 3.0.0 | 2026-07-10 | Z AI + Francois | Restructuration majeure : 15 etapes. Decomposition deplacee en position 2. Nouvelle etape 3 (protocole d'invocation gen-plan, anti-circularite). Nouvelle etape 7 (affinement decomposition). Sans accents (ASCII pur). |
| 2.1.0 | 2026-07-10 | Z AI + Francois | Fusion optimisee v1.1.0 (13 etapes detaillees) + v2.0.0 (orchestration agents). Checklist detaillees par etape. Mode GENERATE. Validation scripts auto-deploiement. Template delegation agent. Guide selection complet. |
| 2.0.0 | 2026-07-10 | Z AI + Francois | Fusion v1.1.0 (13 etapes) + v1.0.0 EN (orchestration agents). Ajout mode GENERATE. Ajout validation scripts d'auto-deploiement. Matrice performance-driven en francais. |
| 1.1.0 | 2026-06-21 | Z AI | Passage 11 -> 13 etapes. Ajout test pre-integration, integration ecosysteme, auto-reapplication. |
| 1.0.0 | 2026-06-14 | Z AI | Version initiale -- protocole 11 etapes, modes DIRECT/PROJET/CIBLE. |