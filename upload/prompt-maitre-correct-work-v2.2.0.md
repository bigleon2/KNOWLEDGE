---
name: correct-work
aka: verify-work
version: 2.2.0
date: 2026-07-29
authors: [Z AI, Francois]
description: >
  Skill de verification et correction du travail realise. Declenche par "verifie ton travail",
  "verifie tes resultats", "verifie ton code" ou "correct-work". Execute 5 etapes
  systematiques : plan d'actions (via gen-plan >=3.3.0, 15 etapes avec CoT+Chaining),
  detection et correction des erreurs/omissions, verification structure et conflits,
  verification des interactions entre composants, coherence des raisonnements et resultats.
  S'applique a toute tache anterieure completee. Modes : PROJET (verification complete
  avec gestion prompt-maitre), CIBLE (verification ciblee) et DIRECT (verification rapide).
  v2.2.0 : integration complete gen-plan v3.3.0 (Registre KB, Protocole de Decouverte,
  parametre kb_path, matrice dynamique KB, override --kb-skill).
requires_gen_plan_version: ">=3.1.0"
---

## Presentation

Ce skill declenche une verification complete en 5 etapes du travail realise dans la session
courante. Il doit etre execute systematiquement lorsque l'utilisateur ecrit "verifie ton travail",
"verifie tes resultats", "verifie ton code" ou toute variante similaire.

Le skill s'applique a tout type de tache anterieure completee : code, documents, PDF, analyses,
developpement web, scripts, etc. Les criteres de verification sont systematiquement adaptes
au type de projet detecte lors de l'Etape 1.

---

## Mots-cles de declenchement

- `verifie ton travail`
- `verifie tes resultats`
- `verifie ton code`
- `correct_work`
- `verify_work`

---

## Modes d'appel

Le comportement du skill depend du mode d'appel :

### Mode PROJET : correct_work(projet)

Verification sur l'ensemble du projet. Gen-plan gere le **prompt-maitre** du projet
(fichier MD de reference). A la premiere analyse, l'integralite du projet est analysee
et le prompt-maitre est genere. Aux appels suivants, seule la derniere version du
prompt-maitre est lue. A la fin, le prompt-maitre est mis a jour si le projet a ete
modifie. Ce mode est optimise pour la performance : l'analyse complete n'est faite
qu'une seule fois.

### Mode CIBLE : correct_work(cible)

Verification sur une tache specifique ou un livrable particulier. Le prompt-maitre n'est
**pas** gere dans ce mode. L'analyse se limite aux fichiers pertinents pour la tache verifiee.

### Mode DIRECT : correct_work()

Sous-cas du mode CIBLE avec une portee restreinte. Utile pour une verification
rapide sans analyse approfondie du projet. Herite du comportement du mode CIBLE
mais n'appelle pas gen-plan (l'Etape 1 est sautee, la verification commence
directement a l'Etape 2).

---

## Protocol (5 etapes sequentielles)

Le skill s'execute **apres** qu'une tache a ete completee. Il analyse les demandes de
l'utilisateur, genere un plan d'actions robuste, puis parcourt l'integralite du travail
produit dans la session et applique les 5 etapes sequentielles ci-dessous.

---

### Etape 1 — Plan d'actions (appel au skill gen-plan)

**Objectif** : Analyser toutes les demandes de l'utilisateur, lire et analyser le projet
(selon le mode d'appel), puis generer un plan d'actions robuste (structure, logique et
detaille) **adapte au projet** pour optimiser l'execution des taches necessaires pour
repondre a ces demandes.

**Sous-protocole** : Cette etape est realisee en appelant le skill **gen-plan**.
Le skill gen-plan est un skill autonome qui peut aussi etre invoque independamment
par l'utilisateur. Il execute un protocole en **15 etapes sequentielles** avec le
paradigme **CoT+Chaining** (Raisonnement -> Action -> Verification -> Correction
a chaque etape). Les 15 etapes sont :

1. Collecter et analyser les demandes de l'utilisateur
2. Decomposer en sous-taches (decomposition precoce, guide toute l'analyse subsequente)
3. Definir le protocole d'invocation gen-plan (anti-circularite)
4. Lire et analyser le projet (avec **lecture bloc par bloc** si > 500 lignes)
5. Identifier la nature du projet
6. Identifier les objectifs
7. Affiner la decomposition (a la lumiere de E4, E5, E6)
8. Detecter les dependances (+ scan KB si registre actif via kb_path)
9. Prioriser (Critique / Importante / Secondaire)
10. Estimer les risques
11. Structurer le plan formel
12. Valider le plan
13. Tester et corriger pre-integration
14. Integrer a l'ecosysteme (si applicable)
15. Auto-reappliquer si gen-plan.SKILL.md est mis a jour

**Execution** : Toutes les etapes s'executent en **mode serie** (parallelisme INTERDIT
sauf demande explicite + preuve d'independance). Chaque etape suit le cycle
CoT+Chaining : raisonnement structure avant action, verification apres action,
auto-correction si anomalie, escalation si echec persiste.

**Modes gen-plan utilises par correct-work** :
   - **Mode PROJET** : correct-work appelle gen-plan en mode PROJET. Gen-plan analysera
     l'integralite du projet, generera/mettera a jour le prompt-maitre.
   - **Mode CIBLE** : correct-work appelle gen-plan en mode CIBLE avec la cible
     specifiee. Gen-plan analysera uniquement les fichiers pertinents.

**Principe cle** : Le plan d'actions DOIT etre specifiquement adapte au projet verifie.
Un projet web Next.js n'a pas les memes points de verification qu'un projet Python, un document
PDF ou une analyse de donnees. Le plan doit refleter la nature, la complexite et les specificites
techniques du projet concerne. Les sous-taches, les risques et les criteres de validation
doivent etre calibres en fonction du type de projet (frontend, backend, fullstack, document,
script, etc.).

**Comment appeler gen-plan** :

correct-work passe a gen-plan les parametres structure suivants, conformement au protocole
defini a l'Etape 3 de gen-plan :

- `mode` : PROJET (si correct-work est appele en mode PROJET) ou CIBLE (si appele en mode CIBLE)
- `contexte` : resume du travail realise dans la session et a verifier
- `fichiers_concernes` : liste des fichiers du projet pertinents pour la verification
- `cible` : (mode CIBLE uniquement) l'element specifique a verifier
- `kb_path` : (optionnel) chemin vers la knowledge base personnalisee de l'utilisateur.
  Si fourni, gen-plan v3.3.0+ execute le Protocole de Decouverte des skills KB
  (Registre KB) a son Etape 4, point 8. Les skills KB detectes sont evalues et
  integres au plan de verification si pertinents. Priorite : ecosysteme > KB sauf
  override utilisateur (`--kb-skill=<name>`).

Ces parametres permettent a gen-plan de produire un plan d'actions cible et adapte.

**Integration du Registre KB (gen-plan >=3.3.0)** :

Si gen-plan v3.3.0 ou superieur est disponible et qu'un `kb_path` est fourni,
gen-plan scanne la knowledge base personnalisee a l'Etape 4 via le Protocole
de Decouverte (6 sous-etapes : scan, classification, evaluation compatibilite,
selection, presentation). Les skills KB detectes enrichissent le plan de
verification de la maniere suivante :
- Si un skill KB correspond a une sous-tache de verification, il est evalue
  contre le skill ecosysteme equivalent (si existant). Le skill ecosysteme est
  prioritaire sauf override utilisateur.
- Le plan produit par gen-plan inclut alors les skills KB selectionnes dans les
  phases correspondantes.
- correct-work utilise ces informations pour les Etapes 2 a 5 (corrections
  potentiellement assistees par des skills KB specialises).
- L'utilisateur peut forcer un skill KB specifique avec `--kb-skill=<name>`.

Si aucun `kb_path` n'est fourni ou si gen-plan <3.3.0, le plan est genere sans
skills KB (comportement identique a v2.1.0).

**Methode** :

- Appeler le skill **gen-plan** pour generer le plan d'actions adapte au projet.
- Le plan genere par gen-plan sert de base pour les etapes suivantes (2 a 5) de verify-work.
- Si le plan est invalide ou incomplet, ajuster avant de continuer.
- Si le plan inclut des skills KB (Registre KB actif), les charger et les evaluer
  avant les corrections des Etapes 2 a 5.

---

### Etape 2 — Erreurs et omissions

**Objectif** : Identifier tout ce qui est incorrect, incomplet ou manquant, puis corriger.
Les criteres de verification doivent etre adaptes au type de projet (cf. Etape 1).

**Checklist** :

1. **Relire les specifications initiales** de l'utilisateur et verifier que chaque exigence
   a ete satisfaite. Si une exigence a ete oubliee, la realiser maintenant.
2. **Verifier les donnees factuelles** : noms, chemins, numeros de version, tailles de fichiers,
   counts, etc. — tout chiffre ou valeur assertee doit etre verifie contre la source reelle.
3. **Verifier la coherence linguistique** : la langue utilisee doit etre identique a celle
   de la demande initiale de l'utilisateur. Pas de melange incoherent.
4. **Verifier les fichiers de sortie** : chaque fichier promis existe-t-il ? Est-il lisible ?
   Pas de fichier vide ou corrompu.
5. **Verifier les dependances** : les imports, les chemins de skill, les references croisees
   entre fichiers sont-ils corrects ?
6. **Adapter la verification au projet** : les erreurs et omissions sont evaluees relativement
   au type de projet. Par exemple, une erreur de schema BDD est critique pour un projet fullstack
   mais inexistante pour un document PDF ; une erreur de mise en page est critique pour un PDF
   mais secondaire pour un script.
7. **Corriger** chaque erreur ou omission identifiee.

**Methode** :

- Relire le fichier de travail (`worklog.md`) si disponible pour lister les taches completees.
- Pour chaque livrable (fichier, code, PDF, etc.), l'ouvrir et l'inspecter.
- Comparer le contenu produit aux attentes definies dans la conversation.
- Evaluer les erreurs et omissions en fonction du type de projet identifie a l'Etape 1.

---

### Etape 3 — Structure du code et conflits

**Objectif** : Verifier que le code ou le document est bien structure, qu'il n'y a pas de conflits
entre modules ou de problemes d'architecture. Utilise une **matrice de coherence logique** si
necessaire pour resoudre les conflits logiques ou les conditions contradictoires.

**Adaptation au projet** : Les points de verification ci-dessous s'appliquent differemment
selon le type de projet. Pour du code, verifier les imports, variables, etc. Pour un document
ou une specification, verifier la structure des sections, la coherence des references croisees,
et l'absence de contradictions internes.

**Checklist** :

1. **Imports circulaires** (code) : verifier qu'aucun module n'importe un autre qui l'importe.
2. **Conflits de noms** : deux fonctions/classes/variables avec le meme nom dans des scopes
   qui pourraient interferer. Pour un document, verifier les definitions en double.
3. **Variables non initialisees** ou utilisees avant d'etre definies (code).
4. **Chemins en dur** qui ne fonctionneraient pas dans un autre environnement (code/config).
5. **Gestion des erreurs** : les cas d'erreur sont-ils traites ou le code echouerait silencieusement ?
6. **Doublons** : du code duplique qui devrait etre factorise, ou du contenu duplique dans un document.
7. **Convention de nommage** : coherence dans le style (snake_case, PascalCase, etc.).
8. **Conflits logiques et conditions contradictoires** : si des conditions booleennes
   complexes sont identifiees (ex : XOR, exclusions mutuelles, guard clauses multiples),
   utiliser une **matrice de coherence logique** pour verifier la logique. La methode :
   - Lister toutes les conditions booleennes et leurs combinaisons possibles.
   - Verifier que chaque combinaison est couverte par exactement une branche.
   - Detecter les branches mortes (cas jamais atteints) et les conflits (plusieurs branches
     pour le meme cas).
   - Pour un document, lister les affirmations de chaque section et verifier qu'aucune
     n'en contredit une autre.
9. **Corriger** chaque probleme de structure ou conflit identifie.

**Methode** :

- Lister tous les fichiers de code modifies ou crees dans la session.
- Pour chaque fichier, verifier les imports, les dependances, les conventions.
- Executer un linter ou des tests si disponibles.
- Verifier que les appels entre modules sont compatibles (bonnes signatures, bons types).
- Si des conditions booleennes complexes ou des exclusions mutuelles sont presentes,
  construire une matrice de coherence logique pour valider la logique.
- Pour un document/specification, verifier la coherence entre sections et l'absence
  de contradictions internes.

---

### Etape 4 — Verification des interactions

**Objectif** : Verifier que toutes les interactions entre les composants du systeme
fonctionnent correctement. Les points de verification ci-dessous s'appliquent selon le type
de projet. Si c'est necessaire pour verifier les interactions complexes (conditions d'activation
multiples, exclusions mutuelles entre composants, etats de transition), utiliser une
matrice de coherence logique (voir Etape 3, point 8).

**Adaptation au projet** : Cette etape doit etre adaptee au type de projet verifie :
- **Projet fullstack** : verifier les 5 categories ci-dessous (API, props, state, data flow, services).
- **Projet frontend only** : accent sur les props, le state management et le data flow.
- **Projet backend/API** : accent sur les endpoints, la validation, les communications entre services.
- **Document/PDF/analyse** : verifier les references croisees entre sections, la coherence des
  donnees citees, et les liens entre livrables.
- **Script/automatisation** : verifier les interfaces d'entree/sortie, les appels systeme,
  et les dependances externes.

**Checklist** :

1. **API frontend-backend** (projets fullstack/web) :
   - Chaque endpoint API appele par le frontend existe-t-il cote backend ?
   - Les parametres envoyes par le frontend correspondent-ils a ce que le backend attend
     (noms, types, formats) ?
   - Les reponses du backend sont-elles correctement parsees et utilisees par le frontend ?
   - Les codes d'erreur HTTP sont-ils geres cote frontend (400, 404, 500, etc.) ?
   - Les champs JSON renvoyes par l'API correspondent-ils aux champs attendus par le frontend ?

2. **Props et communication inter-composants** (projets frontend/fullstack) :
   - Les props passees d'un composant parent a un enfant correspondent-elles a l'interface
     attendue par l'enfant (types, noms, optionnalite) ?
   - Les callbacks (onXxx) sont-ils appeles avec les bons arguments et traites correctement ?
   - Y a-t-il des props obligatoires manquantes ou des props non utilisees ?
   - Les valeurs par defaut sont-elles coherentes entre le parent et l'enfant ?

3. **State management (Zustand, Redux, Context, etc.)** (projets frontend/fullstack) :
   - Le store expose-t-il toutes les donnees necessaires aux composants qui l'utilisent ?
   - Les actions du store sont-elles appelees aux bons moments dans le cycle de vie ?
   - Y a-t-il des donnees du store qui ne sont jamais lues (state mort) ?
   - Les transformations de donnees entre l'API et le store sont-elles fideles
     (pas de perte de champs, pas de conversion incorrecte) ?

4. **Flux de donnees bout en bout (data flow)** (tous projets avec flux de donnees) :
   - Tracer un scenario complet (ex : clic utilisateur → appel API → reponse → mise a jour store →
     re-render composant) et verifier que chaque maillon fonctionne.
   - Les donnees affichees a l'ecran proviennent-elles de la bonne source
     (API live vs cache vs state local) ?
   - Les donnees sont-elles rafrachies apres une mutation (POST/PUT/DELETE) ?
   - Les conditions de course (race conditions) sont-elles evitees dans les appels asynchrones ?

5. **Communications entre services (si applicable)** (projets micro-services/distribues) :
   - Les appels entre micro-services ou mini-services passent-ils par les bons ports/URLs ?
   - Le parametre XTransformPort est-il correctement utilise pour les requetes cross-services ?
   - Les WebSockets se connectent-ils au bon endpoint avec les bons parametres ?
   - Les timeouts et reessais sont-ils geres pour les appels reseau ?

6. **References croisees et coherence entre livrables** (documents, specifications, analyses) :
   - Les references d'une section a une autre sont-elles correctes (numeros de section, noms) ?
   - Les donnees citees dans un livrable correspondent-elles aux donnees source ?
   - Les liens entre fichiers (imports, inclusions, dependances) sont-ils valides ?
   - Y a-t-il des contradictions entre differents livrables du meme projet ?

7. **Corriger** chaque probleme d'interaction identifie.

---

### Etape 5 — Coherence des raisonnements et des resultats

**Objectif** : Verifier que la logique suivie est coherente de bout en bout et que les
resultats finaux correspondent aux conclusions intermediaires.

**Checklist** :

1. **Coherence logique** : les etapes de raisonnement s'enchainent-elles logiquement ?
   Pas de saut non justifie, pas de conclusion qui contredit une premissse.
2. **Coherence numerique** : les chiffres s'additionnent-ils ? Les pourcentages sont-ils
   coherents avec les valeurs absolues ? Les tailles de fichiers correspondent-elles ?
3. **Coherence temporelle** : les dates, versions, chronologies sont-elles coherentes
   entre elles et avec le contexte ?
4. **Resultat attendu vs resultat obtenu** : ce qui a ete promis correspond-il a ce
   qui a ete livre ? Si un ecart existe, l'expliquer.
5. **Coherence entre fichiers** : si plusieurs livrables ont ete produits, sont-ils
   coherents entre eux (pas de contradiction entre le contenu de deux fichiers) ?
6. **Corriger** toute incoherence identifiee.

**Methode** :

- Reconstituer le fil logique de la session : demande utilisateur → plan → execution → resultats.
- Pointer chaque assertion et verifier qu'elle est justifiee.
- Pour les donnees numeriques, refaire les calculs si necessaire.
- Comparer les sorties reelles aux sorties attendues.

---

## Format du rapport de verification

Apres les 5 etapes, produire un rapport structure :

```
## Verification du travail

### Mode d'appel
- correct_work(projet) / correct_work() / correct_work(cible)

### Etape 1 — Plan d'actions (gen-plan)
- [x] / [!] Objectif 1 : statut
- [x] / [!] Objectif 2 : statut
- ...
**Plan valide** : OUI / NON (si non, ajuster avant de continuer)
**Prompt-maitre** : genere / lu / non applicable (selon le mode)

### Etape 2 — Erreurs et omissions
- [x] / [!] Exigence 1 : statut
- [x] / [!] Exigence 2 : statut
- ...
**Corrections appliquees** : (liste des corrections faites, ou "aucune")

### Etape 3 — Structure et conflits
- [x] / [!] Point 1 : statut
- [x] / [!] Point 2 : statut
- ...
**Corrections appliquees** : (liste des corrections faites, ou "aucune")

### Etape 4 — Verification des interactions
- [x] / [!] API frontend-backend : statut
- [x] / [!] Props inter-composants : statut
- [x] / [!] State management : statut
- [x] / [!] Flux de donnees bout en bout : statut
- [x] / [!] Communications entre services : statut
- ...
**Corrections appliquees** : (liste des corrections faites, ou "aucune")

### Etape 5 — Coherence des raisonnements
- [x] / [!] Point 1 : statut
- [x] / [!] Point 2 : statut
- ...
**Corrections appliquees** : (liste des corrections faites, ou "aucune")

### Bilan
- Erreurs corrigees : N
- Omissions comblees : N
- Conflits resolus : N
- Interactions corrigees : N
- Incoherences corrigees : N
- Adaptation au projet : OK / A AJUSTER
- Prompt-maitre : mis a jour / non modifie / non applicable
- Statut global : OK / CORRIGE

### Validation positive
Si toutes les etapes sont [x] et le nombre total de corrections est 0 :
**Validation complete -- aucune anomalie detectee.**
```

---

## Logging

Le rapport de verification complet doit etre enregistre dans `/home/z/my-project/worklog.md` apres chaque execution de correct-work. Cela garantit une trace de la verification et des corrections appliquees.

---

## Relations avec les autres skills

| Skill | Relation | Version | Source |
|-------|----------|--------|--------|
| **gen-plan** | Correct-work appelle gen-plan (Etape 1) en mode PROJET ou CIBLE. v3.3.0+ active le Registre KB si `kb_path` fourni. | >=3.1.0 | Ecosysteme |
| **fullstack-dev** | Correct-work peut verifier un projet fullstack produit par ce skill | -- | Ecosysteme |
| **Skills KB** | Correct-work peut utiliser des skills KB dans les corrections (Etapes 2-5) si detectes par gen-plan v3.3.0+ | >=3.3.0 | Knowledge Base |

**Note sur la selection agent/skill** : Pour la selection des agents et skills d'execution lors des corrections, correct-work s'appuie sur deux sources :
- La **Matrice de Decision Agent/Skill** statique definie dans gen-plan (section "Guide de Selection Agent/Skill" -- ecosysteme natif).
- La **Matrice dynamique KB** construite a l'Etape 4 de gen-plan si le Registre KB est actif (gen-plan >=3.3.0). Les skills KB sont evalues avec la regle : ecosysteme prioritaire sauf override utilisateur (`--kb-skill=<name>`).

---

## Installation et utilisation

### Integration dans une IA cible

Pour integrer ce skill dans une IA cible (ChatGPT, Claude, Mistral, etc.), deux methodes sont possibles :

#### Methode 1 — Copier-coller dans le system prompt

1. Ouvrir le fichier `skill-correct-work.md`.
2. Copier l'integralite du contenu.
3. Coller dans la section "System prompt" ou "Instructions personnalisees" de l'IA cible.
4. L'IA reconnaitra les mots-cles de declenchement (`verifie ton travail`, `correct_work`, etc.)
   et executera le protocole automatiquement.

#### Methode 2 — Fichier SKILL.md dans un repertoire de skills

Si l'IA cible dispose d'un systeme de skills (comme Z AI) :

1. Creer le repertoire `skills/correct-work/`.
2. Copier ce fichier sous le nom `SKILL.md` dans ce repertoire.
3. Le systeme de skills detectera automatiquement le frontmatter YAML et enregistrera le skill.

### Dependance

Ce skill depend du skill **gen-plan** pour son Etape 1. Pour un fonctionnement complet,
assurez-vous que gen-plan est egalement integre dans l'IA cible. Si gen-plan n'est pas
disponible, l'Etape 1 devra etre realisee manuellement en suivant le protocole de gen-plan.

### Utilisation

Une fois le skill integre, l'utilisateur peut declencher la verification en ecrivant :
- `verifie ton travail` — declenchement naturel
- `verifie tes resultats` — variante
- `verifie ton code` — variante
- `correct_work` — commande directe
- `verify_work` — alias anglais

Pour choisir le mode d'appel :
- `correct_work(projet)` — verification complete du projet avec gestion du prompt-maitre
- `correct_work(cible)` — verification ciblee sur un livrable specifique
- `correct_work()` — verification rapide sans analyse approfondie

Options avancees (gen-plan >=3.3.0) :
- `correct_work(projet, kb_path=/chemin/KB)` — verification avec scan des skills KB
- `correct_work(cible, --kb-skill=<name>)` — forcer l'utilisation d'un skill KB specifique
  pour les corrections (override la priorite ecosysteme)

---

## Historique des versions

| Version | Date | Auteurs | Modifications |
|---------|------|---------|---------------|
| 2.2.0 | 2026-07-29 | Z AI + Francois | Integration gen-plan v3.3.0 : ajout parametre kb_path vers gen-plan (Registre KB, Protocole de Decouverte), section "Integration du Registre KB" dans Etape 1, colonne Source dans tableau des relations, Skills KB comme source d'interaction (Etapes 2-5), matrice dynamique KB dans selection agent/skill, options avancees (--kb-skill override), compatibilite ascendante v2.1.0 preservee. |
| 2.1.0 | 2026-07-25 | Z AI + Francois | Optimisation : suppression ToC non-standard, correction double YAML, remplacement Karnaugh par matrice de coherence logique, ajout logging worklog, mode DIRECT clarifie, critere de validation positive, parametres structures vers gen-plan, reference matrice agent/skill, couplage version (requires_gen_plan_version). |
| 2.0.0 | 2026-07-10 | Z AI + Francois | Integration gen-plan v3.1.0 : 15 etapes (vs 11), CoT+Chaining, lecture bloc par bloc, execution serie maximale, gestion tokens. Correction YAML frontmatter. |
| 1.0.0 | 2026-06-14 | Z AI | Version initiale — protocole complet en 5 etapes |
