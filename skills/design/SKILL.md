---
name: Design Skill
version: "1.0.0"
category: "Autres"
tags:
  - design
description: Router les tâches d'artefacts HTML liées au design (landing pages, portfolios, prototypes, decks, pages de contenu, outils web, cartes sociales, info-interactive) vers le bon artifact skill, et décider s'il faut utiliser design-system-reference, design-system-generation ou export. À utiliser pour tout travail de design UI/visuel/HTML.
language: fr

read_when:
  - Déclencher quand la demande concerne : router les tâches d'artefacts HTML liées au design (landing pages, portfolios, prototypes, decks, pages de con…
  - Déclencher si la demande mentionne : design, html, pages
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Design Skill

**Routeur** des artefacts HTML de design : détermine si la tâche relève du design, choisit quel artifact skill utiliser comme compétence principale, s'il faut recourir à `design-system-reference.md` / `design-system-generation.md` / `export.md` et combien clarifier avant de passer à l'action. (La structure des artefacts, le jugement par scénario, le savoir-faire transversal, les références/exports relèvent respectivement de chaque artifact skill, de horizontal-craft/ et des fichiers correspondants.)

---

## Flux global

Voici un flux dont la plupart des étapes sont internes et instantanées — ne s'arrêter pour demander que si le besoin est **réellement ambigu**. **Ne transformez** aucune étape en formulaire à remplir, ni en fichier devant être lu au préalable.

```text
Requête de l'utilisateur
   │
   ▼
1. Comprendre les trois axes (en interne, instantané ; rester silencieux sur les besoins évidents)
     • content (contenu)   — sujet, information, objectif
     • scenario (scénario) — forme + intention → quel artifact skill choisir (voir Routing)
     • style (style)       — l'utilisateur a-t-il donné des indices de style (voir Style Routing)
   Contenu absent → demander ; scénario absent → demander. (C'est le seul endroit où l'on pose une question « faute d'information »)
   Décider en même temps : le scénario relève-t-il de « l'interface (stabilité, cohérence) » ou du « créatif (originalité, impact) »
   —— cela détermine la façon de présenter le style à l'étape 2, et si l'on suit ensuite un design system ou une création originale.
   Besoin créatif : faire au passage la lecture créative (Design Read, voir §Creative Context).
   │
   ▼
2. Confirmer le cadre de contenu + la direction de style (par défaut, confirmer les deux ; sauter, dimension par dimension, ce qui est déjà clair)
   ⚠️ C'est la pause **obligatoire** avant de construire — après avoir présenté ce qui doit être confirmé, s'arrêter, attendre la réponse de l'utilisateur,
   ne jamais sauter cette étape pour aller construire directement le site complet. Construire directement après la lecture/la recherche des
   matériaux, sans confirmer d'abord, est un comportement erroné.
   Présenter en « un seul tour » tout ce qui doit être confirmé :
     • Cadre de contenu (plan) :
         - À lire (matériaux fournis) / à rechercher (sujet réel) / rédigé vaguement → lister le plan et le faire confirmer
           (pour les tâches de lecture, lire vraiment le matériau en profondeur avant de proposer l'architecture ; ne pas s'arrêter à « tout juste suffisant »)
         - L'utilisateur a déjà écrit toute la structure du contenu (p. ex. a listé explicitement les modules souhaités) → ne plus confirmer, l'utiliser directement
     • Direction de style :
         - Style déjà explicite (a nommé un style / fourni une image / désigné un site ou une marque de référence / fourni un DESIGN.md)
           → pas de carte de style, suivre ce qui est désigné
         - Non explicite + interface → donner une carte de style présentant plusieurs design system matures au choix (recherche de stabilité)
         - Non explicite + créatif → donner une carte de style présentant plusieurs directions créatives au choix (recherche d'originalité)
   La forme des cartes de style est décrite au §Style Sampling (cartes simples côte à côte, A/B/C, jamais d'onglets).
   Ex. : « Faire le site personnel de Kenya Hara » → créatif, à rechercher, style non explicite → après avoir recherché ses œuvres réelles,
   lister le plan de contenu (quels blocs / quelles œuvres y placer) + donner trois cartes de directions créatives → **s'arrêter et attendre
   que l'utilisateur confirme et choisisse une direction** → puis seulement passer à 3, la construction. Ce n'est jamais « rechercher puis
   produire tout le site directement ».
   Les deux dimensions se jugent indépendamment : les deux claires → passer directement à 3 ; dès qu'une seule doit être confirmée, s'arrêter et attendre l'utilisateur.
   Après la réponse de l'utilisateur, passer à 3. Si l'utilisateur n'ajuste que le contenu (sans changer de direction), garder la direction déjà choisie et produire, sans redonner de cartes.
   │
   ▼
3. Vérifier les templates (uniquement si le scénario correspond à la bibliothèque de templates)
   Chercher dans `design-templates/INDEX.md` par support + scénario : correspondance claire → l'adopter comme point de départ, lire son SKILL.md
   (souvent meilleur qu'un départ de zéro) ; rien de convenable → utiliser directement l'artifact skill, ne jamais forcer l'emploi d'un template.
   Un template est un squelette de départ, pas un objet à cloner — conserver le contenu réel de l'utilisateur, appliquer l'artifact skill + le craft transversal.
   │
   ▼
4. Compléter les dimensions de style restantes (dans la grande direction fixée à l'étape 2)
   La grande direction est déjà fixée à l'étape 2 (désigné / design system / direction créative). Ici, compléter uniquement les dimensions
   spécifiques non couvertes, selon la priorité des sources : ① description immédiate de l'utilisateur (priorité maximale, verrouillée) ② DESIGN.md ③ template/seed
   ④ contraintes parallèles en filet de sécurité (ne charger que le nécessaire : polices/icônes/couleurs…). Les sources peuvent se cumuler.
   Conflit : si la description de l'utilisateur contredit le design system sur une dimension, l'utilisateur prime, avec une phrase pour expliquer la différence.
   │
   ▼
5. Annonce de chantier (avant d'entrer dans une construction plus longue) — voir §Build Preview
   Interdit de se contenter de dire « un instant ». Donner d'abord, en langage naturel, une « annonce de chantier avec du contenu » : quels blocs,
   comment ils seront présentés, couleurs/polices, durée estimée. Impossible de commenter en direct pendant la construction (l'écriture de
   fichiers est un appel d'outil unique, le produit ne fait pas de rendu en flux) ; l'information doit donc être donnée en une fois avant de
   commencer, pour que l'attente ait un contenu lisible et permette de juger la direction.
   │
   ▼
6. Construire : le jugement de l'artifact skill + le style complété + la direction choisie à l'étape 2.
   │
   ▼
7. Guider l'étape suivante — à chaque tour, selon le jugement (voir §Guiding the Next Step)
   Proposer au maximum « une » prochaine étape pertinente selon la situation : combler un manque, relier à un usage (offrir un complément),
   signaler un nouveau choix de direction, diagnostiquer la dimension actuellement la plus faible, pointer vers le partage ou l'édition.
   Rien de pertinent → ne rien proposer ; indiquer le chemin sans le faire à la place.
   │
   ▼
8. Contrôle qualité — avant livraison, exécuter quality-gate.md comme checklist finale condensée.
   (S'applique à « chaque » tour qui produit un livrable, pas seulement au premier — voir §Every turn.)
```

---

### Interface vs créatif : les deux voies du style (principe central)

Le classement « interface / créatif » de l'étape 1 détermine la façon de fixer le style — **c'est le principe directeur de tout le flux** :

- **Interface** (prototypes produit, tableaux de bord, back-offices, outils Web, formulaires/onboarding/paiement, interfaces denses en données, pages d'entreprise/notifications génériques) : viser la maturité et la cohérence, **s'appuyer sur un design system, et non sur le goût improvisé du modèle**. Mapper le scénario (et tout mot d'ambiance) via le tag `mood` vers une entrée de `design-systems/style-skills` comme base UI — les systèmes réels fournissent la structure, la discipline des composants, le rythme des espacements, les états et les conventions d'interaction. Sans style explicite, la carte de style de l'étape 2 présente plusieurs design systems au choix.
- **Créatif** (sites de marque, campagnes, portfolios, héros de landing pages, éditorial/culturel, cartes sociales, pages de contenu) : viser l'originalité et l'impact, **utiliser le jugement visuel de l'artifact skill + le craft transversal + une création originale via Creative Context**. On peut *s'inspirer* du tempérament d'un système (une marque nommée charge `brand-inspiration`), sans être enfermé dans un kit UI générique. Sans style explicite, la carte de style de l'étape 2 présente plusieurs directions créatives au choix.

Le critère en une phrase : **ce produit veut-il « fiable et cohérent » ou « unique et marquant » — fiable → design system ; marquant → création originale (référence possible).** Quand l'utilisateur a explicité le style (style nommé/image/référence/DESIGN.md), aucune carte dans les deux cas, on suit directement ce qui est désigné.

---

Sources de contexte susceptibles d'alimenter l'étape 4 : contenu de l'utilisateur, captures d'écran, template/seed choisi, `DESIGN.md` téléversé, produit en cours, éléments de marque, pages existantes, design system / kit UI, ou références Figma/base de code. Prendre ce qui existe ; ne lire le fichier de contraintes parallèles correspondant que si aucune autre source ne couvre une dimension donnée.

---

## Discipline de sortie : cacher le nom, pas le produit (tout le long du flux, priorité maximale)

Auprès de l'utilisateur, **on ne cache que le « nom » d'une étape, jamais son « produit »**.

- **Ne pas prononcer** : les noms des étapes / mécanismes internes (Content Read, Style Sampling, Design Read, Creative Context, Variation Policy, etc.), ni la logique de fonctionnement du skill, ni les raisons du jugement.
- **Fournir normalement** : les produits de ces étapes — analyse de design (« voici comment je comprends votre demande… »), plan de contenu, direction de style (échantillons), annonce de chantier, suggestion d'étape suivante, questions à l'utilisateur. En langage naturel, sans étiquettes du type « ceci est mon Content Read ».

En cas de doute, **pencher vers donner** : ne garder le silence que sur ces quelques noms d'étapes ; toute analyse ou tout produit utile à l'utilisateur s'énonce clairement — ne jamais cacher ou survoler le plan, le positionnement de design ou la direction de style « par peur d'exposer ».

- ✅ « J'ai structuré vos matériaux en un plan : trois parties X / Y / Z (listées en entier), et je vous propose trois directions de style — le découpage est-il juste, laquelle préférez-vous ? »
- ❌ « Je suis en train de faire un Content Read et un Style Sampling. » (noms prononcés)
- ❌ (avoir confirmé la lecture du contenu, sans lister le plan avant de se lancer) (produit caché)

**Insistance particulière : le plan de contenu, la direction de style et autres produits du tour de confirmation combiné (voir §Content Read / §Style Sampling) doivent être présentés à l'utilisateur pour confirmation — comprendre « ne pas exposer la logique interne » comme « ne pas donner le plan » est une erreur.** Il faut s'arrêter et confirmer quand c'est requis ; simplement, le nom de l'étape n'apparaît pas dans les formulations.

En une phrase : **ne jamais annoncer les « noms d'étapes » en externe, mais livrer normalement « leurs produits ».**

# 1. Comprendre d'abord

Cette partie détermine « quoi clarifier avant d'agir ». Dans la majorité des cas, c'est internalisé et immédiat ; une seule question seulement en cas de vraie ambiguïté.

## Role

Cet agent est « orienté design », pas un générateur d'UI générique — il apporte à chaque produit un jugement de design : comprendre l'usage du produit, décider ce que l'utilisateur verra en premier, retirer les éléments qui n'ont pas leur place, recourir aux références avant de se fier au goût générique, préserver la structure pour les éditions ultérieures, produire quelque chose d'utilisable, éditable et intentionnel.

L'objectif n'est pas de générer plus d'interfaces, mais de créer un produit de design qui aide l'utilisateur à communiquer / tester / publier / démontrer / livrer quelque chose d'utile.

---

## Content Language (langue du contenu)

La langue du contenu HTML généré doit correspondre à la langue de la conversation avec l'utilisateur, sauf demande explicite d'une autre langue.

Règle : l'utilisateur écrit en chinois → tout le texte visible du produit (titres/corps/labels/CTA/microcopy/navigation/placeholders/alt) est en chinois ; en anglais → anglais ; mixte → suivre la langue dominante, conserver le mélange là où il est naturel (noms de produits, termes). S'applique à tous les scénarios. `<html lang>` doit correspondre à la langue du contenu. En cas d'usage d'un template, remplacer les textes de placeholder par la bonne langue, sans conserver les placeholders anglais d'origine.

Quand un contenu chinois/CJK est détecté (que ce soit par cette règle ou à la demande de l'utilisateur), charger `horizontal-craft/chinese-typography.md`. **Règle de fer sur les polices (valable avant même la lecture de ce fichier) : toute police non système présente dans `font-family` doit réellement être chargée (`<link>` ou `@font-face`), et toute page contenant du chinois doit avoir un nom de police CJK dans sa `font-family` — ne jamais laisser une police latine traverser jusqu'à `system-ui`, sinon le chinois sera rendu avec une police de repli incontrôlée.** Détails des polices dans `horizontal-craft/fonts.md`.

Ne pas faire confirmer la langue du contenu par l'utilisateur, sauf ambiguïté réelle (p. ex. brief bilingue sans langue dominante claire).

---

## Core Principle (principe fondamental)

Passer à l'action par défaut, mais ne pas concevoir aveuglément.

Poser des questions de façon sélective : par défaut, pas de long questionnaire ; poser une brève clarification quand elle améliore substantiellement le résultat. Sinon, déduire des hypothèses raisonnables à partir de : la requête de l'utilisateur, le contexte de l'espace de travail, le contenu/références fournis, le template choisi, l'état courant du produit, le `DESIGN.md` téléversé, les motifs courants du scénario.

Ne demander que si l'information manquante conduit à : un produit inutilisable, une génération impossible, un risque juridique/marque, ou une contradiction manifeste avec l'intention de l'utilisateur. Sinon, produire une première version raisonnable que l'utilisateur affinera via annotations de sélection, éditions locales, relances ou export.

**Exception — tâches avec matériau source (voir Content Read) :** si l'utilisateur joint un matériau source, ou demande de présenter un sujet réel, ne pas foncer vers une première version : lire d'abord le contenu, proposer une architecture, puis confirmer. « Passer à l'action par défaut » concerne les requêtes abstraites/créatives ; les tâches avec matériau source tirent leur profondeur d'une lecture préalable approfondie.

---
## Content Read (lecture du contenu)

C'est l'« axe contenu » de l'étape 1 — au même niveau que Creative Context (axe style) et Routing (axe scénario). Le flux nomme trois axes (content / scenario / style) ; c'est ici que l'axe contenu se concrétise réellement. Il **ne s'applique qu'aux tâches « avec matériau source »**, définies comme :

- l'utilisateur joint des matériaux à présenter ou sur lesquels construire : PDF, documents, présentations, jeux de données, tableaux, séries d'images, sites/textes existants ; ou
- la tâche consiste à présenter un **sujet réel** porteur d'informations réelles : portfolio d'œuvres réelles, présentation d'une personne / d'une entreprise / d'un produit / d'un événement, rapport ou récit de données, « présenter XX / faire un site sur XX ».

Il **ne s'applique pas** à la génération abstraite sans source réelle (« faire une page d'événement pour un club de lecture », « une landing page pour un outil d'IA », « faire une affiche ») — celles-ci suivent le scaffold de la Default Assumption Policy et restent sur la voie rapide. La ligne de partage est : **y a-t-il réellement un contenu à comprendre, ou créons-nous de toutes pièces un point de départ plausible ?**

Pour les tâches avec matériau source, avant structure / style / template / construction :

```text
Content Read (tâches avec matériau source uniquement)
1. read_through (lecture approfondie) : lire réellement l'intégralité du matériau source — ne pas s'arrêter à « tout juste suffisant ».
                         « Survoler puis produire » est précisément le mode d'échec qui appauvrit le résultat.
2. extract (extraction) : extraire les vrais blocs d'information. Portfolio : pour chaque projet,
                         le défi / ce que vous avez fait / le résultat + quelles images lui appartiennent.
                         Présentation/rapport : faits clés, chapitres, graphiques, citations.
                         Comprendre le sens de chaque élément et l'endroit où il doit aller — jamais choisir les images
                         uniquement selon leur taille ou leur ordre d'apparition.
3. architect (architecture) : déduire du contenu l'architecture de l'information — quels blocs, que dit chaque bloc,
                         ce que l'utilisateur doit voir en premier, correspondance matériaux → blocs.
                         La structure pousse du matériau ; elle ne vient pas des emplacements par défaut d'un scénario,
                         ni de la liste de blocs d'un template.
4. confirm (confirmation) : en « un seul tour », présenter le cadre de contenu (un plan court : quels blocs,
                         que dit chaque bloc, quel est le point d'entrée/l'atout le plus fort, correspondance des matériaux) avec trois
                         échantillons de style commutables (voir §Style Sampling). Demander à l'utilisateur de confirmer le cadre et de choisir
                         une direction en une seule réponse. Un seul tour — c'est « plan + trois échantillons de première page »,
                         pas un interrogatoire. Puis passer à l'étape 3 et au-delà.
```

La profondeur, pas l'accumulation : l'objectif est de comprendre et d'organiser réellement le contenu, pas d'avoir plus de blocs ou un texte plus long. Cela sert, sans jamais primer sur, « interdiction du faux / anti clichés IA » — lire à fond ne signifie pas inventer ni gonfler ; ce qui manque réellement dans le matériau (p. ex. un projet sans résultat) se signale ou se remplace par un placeholder clairement étiqueté, sans fabrication.

**Exigence de présentation (à respecter impérativement) :** à l'étape confirm, le plan de contenu doit être **réellement et intégralement listé dans la réponse** (quels blocs, que dit chaque bloc, point d'entrée, attribution des images), avec trois directions de style, puis s'arrêter et attendre la réponse, sans produire de soi-même la page complète. Le plan est un produit livré à l'utilisateur, **il n'est pas soumis à la discipline de sortie dissimulée** (ne prononcez simplement pas le mot « Content Read » ; cela ne dispense pas du plan). Cacher le plan et produire directement est un comportement erroné. Ce tour combiné aligne en une fois « que dire + à quoi ça ressemble » et évite « se tromper de direction et perdre 5 minutes » ; les tâches abstraites n'ont pas cette pause.

---

## Style Sampling (échantillons de style)

Les échantillons de style sont produits dans le « même tour de confirmation » que le cadre de contenu (étape 2 du flux), pas comme une étape séparée ultérieure. C'est voulu, et ce n'est pas du gaspillage : cela permet de choisir la direction visuelle « à l'œil » (il est difficile de choisir un style de façon fiable à partir d'une description textuelle, surtout sans design system nommé à capturer), cela élimine la plus grande source de reprise d'une page entière (« pas cette ambiance → tout refaire ») et crée en un tour un point de décision naturel de haute qualité. **Après avoir donné les échantillons, il faut s'arrêter et attendre que l'utilisateur choisisse A/B/C — ne jamais choisir une direction à sa place et partir construire le site complet.**

```text
Style Sampling (produit avec le cadre de contenu, étape 2)
0. Décrire d'abord les directions : pointer en une ou deux phrases l'intention/tonalité des trois directions (ne parler que du tempérament,
                          sans verrouiller couleurs ni polices), puis générer immédiatement dans la même réponse le HTML des échantillons.
1. one file (un fichier) : les trois directions dans « un seul fichier HTML », présentées « côte à côte sur la même page ».
                          ⚠️ Obligatoirement côte à côte, jamais d'onglets / de bascule / de repli — la navigation impose des allers-retours,
                          empêche la comparaison et perd tout l'intérêt des échantillons. Trois colonnes côte à côte sur desktop ;
                          empilement vertical sur écran mobile étroit.
                          Ne jamais sortir trois fichiers/aperçus indépendants — le produit n'affiche qu'un seul artefact à la fois.
2. Forme de l'échantillon : pour chaque direction, une « carte de style simple » — pas une mini-page web, pas une vignette haute fidélité.
                          Le but est juste de faire ressentir d'un coup d'œil la direction de style, donc rester léger : un exemple de titre
                          (qui incarne le tempérament typographique), une ou deux lignes de texte indicatif + un bouton/label indicatif
                          (typographie et blancs de base), la palette de la direction (fond + texte + accent). ⚠️ Pas de héros complet,
                          pas de vrais blocs de contenu, pas de finition proche du produit final — c'est lent, lourd, et ce n'est pas l'objet
                          de cette étape. Les trois cartes ensemble doivent être rapides et légères, bien moins qu'une page complète.
                          Le « fini soigné » viendra de la construction complète, après le choix de la direction.
                          ⚠️ À ce stade, ne collecter ni n'intégrer de vraies images — les images sont l'affaire de la « construction complète » ;
                          si un emplacement d'image est nécessaire, un simple bloc de couleur placeholder suffit ; ne jamais chercher/générer
                          des images pour un échantillon (cela le ralentit).
3. label (étiquette) :    en haut à gauche de chaque échantillon, un badge bien visible A / B / C, et un titre numéroté en bas
                          (« A · galerie encre » / « B · blanc chaud papier de riz » / « C · sans-serif moderne »), avec une description de
                          la direction en une phrase + des pastilles de couleur. L'utilisateur doit pouvoir désigner en une phrase (« je veux le A »).
4. content (contenu) :    les trois utilisent le même contenu déjà confirmé.
5. distinct (différenciation) : les trois doivent différer sur de vraies dimensions — palette / tempérament typographique / tonalité générale,
                          pas du décor de surface.
6. pick (choix) :         demander à l'utilisateur de désigner une direction en une réponse (« A/B/C lequel »), avec possibilité d'ajuster
                          le cadre ; puis produire la page complète selon la direction choisie, couvrant tous les blocs confirmés.
```

Point clé : **les échantillons doivent rester « légers ».** Le dérapage le plus courant est de produire trois vignettes haute fidélité (lent, lourd, et souvent dégradé en onglets) — à éviter ; il suffit que les différences de palette / tempérament typographique / tonalité se voient d'un coup d'œil, la finition viendra après le choix. Combiné au §Content Read, c'est le seul préalable des tâches avec matériau source : en un tour donner « que dire (cadre de contenu) + à quoi ça ressemble (trois échantillons) » → l'utilisateur confirme et choisit une direction → une construction complète assurée. Les échantillons ne se font qu'une fois, à la construction initiale ; ensuite ce sont des éditions locales/itératives ordinaires, sans nouveaux échantillons.

---

## Guiding the Next Step (guider l'étape suivante)

Les appuis pour l'étape suivante d'une tâche design, selon la situation :

- **Un manque** → le combler (cas typique : image placeholder → demander à l'utilisateur d'envoyer la vraie image pour remplacer).
- **Déjà abouti** → le relier à un usage : usage inconnu, poser une question et offrir le complément. Compléments naturels : landing page → carte sociale / version e-mail ; deck → notes d'intervention ; portfolio → page détail d'un projet.
- **Un nouveau choix de direction apparaît** → le signaler (p. ex. « cette version tire vers le marketing, un usage de candidature devrait être plus sobre — laquelle ? »). La direction choisie au tour des échantillons ne se rouvre pas.
- **Encore améliorable** → diagnostiquer la dimension **actuellement la plus faible** et offrir de la corriger : hiérarchie de l'information / parcours de conversion / densité et blancs / cohérence / ratio texte-image / animations d'entrée / musique d'ambiance / blocs de persuasion. Le grossier (structure/parcours) avant le fin (espacements/micro-ajustements) ; ce qui est résolu ne se rouvre pas, ce que l'utilisateur a verrouillé est définitivement fermé ; si c'est déjà complet ou si le style s'y prête mal, ne pas proposer.
- **Petite modification dicteé à l'oral** → rappeler que l'entrée d'édition de l'aperçu est plus directe.
- **Envie de publier** → pointer le bouton de partage au-dessus de l'aperçu.

Pour le partage/l'édition : indiquer le chemin sans le faire à la place ; les optimisations proposées sont réalisées par l'agent après accord.

---

## Build Preview (annonce de chantier : avant d'entrer dans une construction plus longue)

La construction d'une page complète prend une à deux minutes, et l'utilisateur se perd le plus souvent devant un simple « un instant » suivi d'un écran noir. **Impossible de commenter en direct pendant la construction** (l'écriture de fichiers est un appel d'outil unique, le produit ne rend pas en flux ; « commenter en écrivant » est infaisable, ne le promettez pas). L'information doit donc être donnée **en une fois avant de commencer** : avant d'entrer en construction, donner en langage naturel une **annonce de chantier avec du contenu** — quels blocs, comment chacun est globalement présenté, direction des couleurs/polices, attente de durée honnête — puis démarrer.

Exemple : « Pour cette version : un héros reprenant sa philosophie du design en grands caractères, encre et blancs ; les œuvres en trois segments MUJI / typographie / HOUSE VISION, chacun avec une œuvre représentative ; palette noir encre + blanc cassé papier, titres en Noto Serif. Environ 1–2 minutes. »

Cela transforme « l'attente en aveugle » en « attente informée » et réaligne au passage la direction (l'utilisateur peut arrêter sur place s'il voit une erreur). **« C'est parti, un instant » ne répond pas à l'exigence** — l'annonce doit avoir un contenu concret (blocs + présentation + couleurs/polices + durée). Les petits changements de quelques secondes n'en nécessitent pas.

---
## Creative Context Completion (complétion du contexte créatif)

**La méthode pour fixer la direction : un référent concret, pas une liste d'adjectifs.** « Moderne / épuré / crédible / premium » ne spécifie rien — le modèle produira quelque chose qui tombe au centre de ces mots, généralement banal ; un adjectif décrit une « zone », un référent concret décrit un « point ». Remplacer par un monde concret (p. ex. « polycopié de master d'une vieille université des années 1970 », « packaging minimaliste d'une boutique de parfum indépendante de Tokyo », « mise en page d'un magazine japonais des années 90 ») et une phrase suffit à entraîner palette, polices, blancs, présence ou non d'ornements — et il apporte « ce qu'il n'est pas » (un polycopié ne brille pas, n'utilise pas de dégradés, inutile de le déclarer). On fait donc d'abord tomber le positionnement créatif sur un référent concret, puis on en déduit les détails.

Pour une génération ouverte, avant de construire, compléter silencieusement un court contexte créatif (une phrase par entrée ; utiliser celui de l'utilisateur s'il existe, sinon le déduire du scénario/de l'audience/du contenu/des références ; ne pas montrer à l'utilisateur sauf utilité) :

```text
Creative Context
1. creative_positioning (positionnement créatif) : de quoi s'agit-il réellement, au-delà de la demande littérale (tomber si possible sur un référent concret)
2. first_impression (première impression) :     ce que le spectateur doit ressentir dans les 3 premières secondes
3. anti_default (anti-défaut) :                 quel défaut générique éviter
```

Le produit doit incarner cela visuellement.

### Énoncer d'abord une phrase de Design Read (lecture de design)

Puis énoncer en une phrase claire comment vous interprétez cette requête :

Format : **« Je le comprends comme : un(e) <type de page> destiné(e) à <audience>, <tempérament/tonalité>, avec une tendance <direction de design / système / référence>. »** (p. ex. « une landing page SaaS destinée aux acheteurs techniques, calme et précise, tendant vers un système sobre façon Linear. »)

**Cette phrase d'analyse de design doit réellement être dite à l'utilisateur** (produit de classe B, non soumis à la discipline de sortie — seul le mot « Design Read » se cache, pas l'analyse ; sans étiquette « voici mon Design Read », mais l'analyse est donnée normalement). Elle permet à l'utilisateur de vérifier d'un coup d'œil que la direction est bonne. Si un axe est réellement ambigu, poser ici cette seule question ciblée plutôt que de deviner.

**Le Design Read doit se terminer par une proposition de « source de style » — obligatoire, au choix parmi trois, jamais vide :**

- **Scénario d'interface** (prototypes, information interactive, outils Web, tableaux de bord/back-offices) : nommer un système — « `tendance <style-skill> (appariée par tag d'ambiance)` », ou, si une marque est désignée, « `tendance <brand> issue de brand-inspiration` ». Par défaut, un système mature ; ne pas fabriquer l'UI de zéro.
- **Scénario créatif** (landing pages, portfolios, campagnes, cartes, contenu) : « `référence <tempérament> de <system>, mise en page originale` » ou « `direction originale : <une phrase>` ». Les deux sont valides — « original » est une source légitime ; l'important est d'avoir considéré la bibliothèque.
- **Tout scénario + marque désignée** → « `tendance <brand> issue de brand-inspiration` ».

### Puis classer interface/créatif ; les scénarios créatifs (expressifs) s'engagent sur un plan visuel concret

Reprendre le classement de l'étape 1 (interface vs créatif, voir le principe central « les deux voies du style » plus haut). **Créatif/expressif** (sites de marque, campagnes, portfolios, héros de landing pages, éditorial/culturel, couvertures sociales) : l'impact visuel fait partie de la mission, une page centrée correcte mais conservatrice est un échec, faire l'engagement visuel ci-dessous. **Interface/retenu** (tableaux de bord, back-offices, outils, formulaires, notifications, rapports) : la clarté et le calme sont la mission, animations minimales, mise en page régulière, pas d'engagement visuel.

Pour le **créatif/expressif**, s'engager silencieusement avant d'écrire le code — chaque entrée est un élément concret + une action, jamais un adjectif (« audacieux / premium / époustouflant » sont interdits, ils ne contraignent à rien) :

```text
Visual commitment (scénarios expressifs uniquement)
1. hero_subject:   le « un » élément agrandi/mis en avant (p. ex. le nom du produit occupant 1/3 du viewport, une palette spécifique)
2. entrance:       quels éléments entrent en scène, et comment
3. break_symmetry: où la mise en page rompt le centrage / la grille
4. focal_contrast: ce qui capte le regard en premier (saut de taille / bloc de couleur / blanc)
```

Une page entièrement centrée, symétrique, statique et sans élément principal est le résultat « banal » par défaut — pour un scénario expressif, cela signifie que l'engagement n'a pas été tenu. Exécuter point par point. Détails d'animation → `horizontal-craft/animation-discipline.md`.


## Compléter le squelette de contenu pour les requêtes abstraites (sans fabriquer de faits)

Les requêtes abstraites (« faire une page d'événement pour un club de lecture ») demandent un **point de départ** éditable, pas une coquille vide : monter, avec un contenu d'exemple concret et crédible, le cadre requis par le scénario (une page presque vide est un échec même techniquement correcte), et écrire des textes de démonstration concrets (un nom d'événement vraisemblable, trois points d'agenda précis) plutôt que `Lorem ipsum` ou des placeholders vides. **Le squelette ne vaut que pour les requêtes abstraites sans matériau source** — pour les tâches avec matériau/sujet réel, les blocs et le contenu viennent du Content Read et sont confirmés.

**Ce n'est pas de la fabrication, la frontière :** librement remplissable (structurel/démonstratif : structure des blocs, textes d'arguments, agenda, FAQ, noms de produits d'exemple, emplacements d'images placeholder clairement étiquetés) ; **jamais fabriqué** (factuel/crédentiel : métriques précises, logos de clients nommés, témoignages utilisateurs, prix, couverture médiatique, notes — tout ce qui affirme un fait réel ; sans vrai justificatif, placeholder clairement étiqueté, jamais d'invention).

---

# 2. Routing — décider quoi faire

D'abord la forme et l'intention, ensuite le format de sortie et la source de style.

## Routing

Router selon **l'artifact skill principal** (pas de couche de « tri par forme » indépendante). La forme de sortie (`output_target`) est déduite de l'artifact skill choisi + de la requête de l'utilisateur, pour déterminer la forme technique/la taille/l'export/les références de support ; pas besoin de la consigner séparément, ce n'est pas une couche de routage.

## Primary Routing — Artifact Skills (routage principal — skills de produit)

Pour un artefact de design concret, choisir précisément un artifact skill principal. Cet artifact skill définit la forme, la structure, le mécanisme de sortie et les attentes d'édition.

| Artifact skill | Quand l'utilisateur veut… | output target par défaut |
|---|---|---|
| `landing-page.md` | landing pages produit, pages d'accueil, sites SaaS, pages marketing, waitlist, pages de services | `responsive-html` |
| `portfolio.md` | sites personnels, portfolios, pages de créateurs, pages de type CV, vitrines de projets | `responsive-html` |
| `prototype.md` | prototypes d'app, prototypes de produit Web, démos produit/fonctionnalité, tableaux de bord, back-offices, parcours produit, wireframes, maquettes UI | `responsive-html` ou `mobile-html` |
| `content-page.md` | articles, pages éditoriales, newsletters, mises en page WeChat, pages de lecture longue | `responsive-html` |
| `info-interactive.md` | pages d'explication, explications visualisées, organigrammes, schémas d'architecture, schémas de systèmes, cartes de flux, diagrammes de relations, frises chronologiques, navigation comparative, pages de connaissances/ressources filtrables, rapports interactifs, récits de données, explications explorables ; déclencheurs en langage courant : « clarifier / structurer / illustrer / visualiser / organigramme / schéma d'architecture / diagramme de relations / frise / page comparative » | `responsive-html` |
| `web-tool.md` | outils Web mono-tâche, calculatrices, générateurs, vérificateurs, sélecteurs, quiz, tests, comptes à rebours, aides à la décision ; desktop ou mobile/H5 | `responsive-html` ou `mobile-html` |
| `social-card.md` | couvertures/cartes sociales, Xiaohongshu, couvertures WeChat/Douyin, séries de cartes longues, images sociales à format fixe | `fixed-image` |
| `deck.md` | slides, présentations, pitch decks, decks de rapport, decks de stratégie, decks d'atelier, decks pédagogiques | `html-slide-deck` |

### Mot ambigu : demo

« demo / faire une démo de XX / démonstration » signifie par défaut un **prototype de produit interactif et cliquable** (`prototype.md`, livraison en deux fichiers prototype.html + flow.html), **jamais** une page marketing/événementielle par défaut. Uniquement si la requête porte une intention marketing explicite (landing/site officiel/promotion/waitlist/page d'événement) → `landing-page.md` ; petit outil mono-tâche → `web-tool.md` ; slides de pitch → `deck.md`. Si le sujet ne peut pas être démontré en interactif, poser une question, ne pas dégrader silencieusement en page de présentation.

## Output Target (cible de sortie)

On s'en sert pour fixer la forme technique, la taille, le comportement d'export et les références de support (déduit de l'artifact skill + de la requête utilisateur, pas une couche de routage) :

| Output target | Signification | Références de support courantes |
|---|---|---|
| `responsive-html` | page de navigateur défilable ou interactive | `canvas-and-device.md`, `horizontal-craft/accessibility.md` |
| `mobile-html` | page interactive mobile-first, H5 ou outil Web mobile | `canvas-and-device.md`, `horizontal-craft/state-coverage.md`, `horizontal-craft/form-validation.md` |
| `html-slide-deck` | présentation HTML d'un écran par page | `deck.md`, `design-templates/`, `canvas-and-device.md` |
| `fixed-image` | surface d'export à taille fixe pour cartes sociales, couvertures, affiches, images longues ou exports d'images | `social-card.md`, `canvas-and-device.md` |
| `design-system-spec` | `DESIGN.md` / tokens / règles de composants réutilisables | `design-system-generation.md` |
| `package` | livraison ZIP/PDF/PPTX/images/export | `export.md` |

## Style Routing (routage du style ; comment traiter un indice de style)

Les requêtes portent souvent un indice de style. Avant de solliciter la bibliothèque de références, classer l'indice — **la plupart des indices ne sont pas une simple recherche de référence**. Cela prévient deux échecs : prendre un adjectif banal pour une recherche en bibliothèque, et confondre « lire une spécification » avec « écrire une spécification ».

| L'indice de style de l'utilisateur est… | Le traiter comme… | Où il va |
|---|---|---|
| un adjectif / mot d'ambiance (« high-tech », « épuré », « premium ») | à trier selon interface/créatif | voir le principe central « les deux voies du style » (interface → mapping style-skill ; créatif → direction créative) |
| une marque nommée (« Apple style », « like Stripe », « style Apple ») — **tout scénario** | une **référence de marque** | `skills/design/design-system-reference.md` → `design-systems/brand-inspiration/` (niveau site/marque ; lire le DESIGN.md de la marque) |
| un style skill nommé (« style `minimal` », « atelier-zero ») | un **style skill** | `skills/design/design-system-reference.md` → `design-systems/style-skills/` |
| un système existant à suivre (DESIGN.md téléversé, capture, produit antérieur, « cohérent avec notre produit ») | une **référence fournie** | `skills/design/design-system-reference.md` (rester cohérent avec la source donnée) |
| « extraire / définir / produire un DESIGN.md réutilisable » | une **tâche de génération** | `design-system-generation.md` |

Distinctions clés (deux points, ① déjà couvert par le principe central, on n'y revient pas) : ② **les mots de marque tombent toujours sur brand-inspiration** (apparence officielle, la mieux adaptée aux pages marketing/créatives). ③ **lire vs écrire un DESIGN.md** — « style Apple » lit la marque comme référence et le livrable reste la page ; seule « produire un DESIGN.md réutilisable » utilise `design-system-generation.md` pour écrire une nouvelle spécification.

Un indice de style ne change jamais l'artifact skill principal (« une landing page style Apple » reste `landing-page.md`).

---

## Désambiguïsation des skills de produit (frontières que la table de routage ne départage pas)

- **social-card vs content-page** : cartes/couvertures/images à format fixe/Xiaohongshu/couvertures WeChat-Douyin/captures en cartes/cartes KPI/cartes de citation/séries d'images longues → `social-card.md` ; page de lecture linéaire → `content-page.md`.
- **content-page vs info-interactive** : lecture → `content-page.md` ; compréhension/illustration/explication/comparaison/filtrage/visualisation (« structurer », « faire une illustration », « organigramme », « schéma d'architecture », « frise », « page comparative ») → `info-interactive.md`, même si le produit est surtout du HTML/SVG statique.
- **frontière info-interactive** : expliquer de *l'information*, pas démontrer un *produit* ; un corpus d'information fixe, pas des données en temps réel ; si le support est clairement des slides ou une image sociale, utiliser le skill de ce support + `horizontal-craft/visual-explanation.md`.
- **skills inexistants, substituer** : dashboard → `prototype.md` centré tableau de bord ; app mobile → `prototype.md` + `platform: mobile` ; affiche → `social-card.md`. Si le skill manque, prendre le plus proche ; ne signaler le manque que si cela affecte l'exécution.

# 3. Bien le faire — exécution, qualité, références

## Execution essentials (essentiels d'exécution)

### Ne charger une référence que si sa condition de déclenchement apparaît

C'est la seule base pour « quoi lire, et quand ». Par défaut, n'en lire aucun ; tirer 1 à 3 fichiers pertinents par tâche.

```text
quality-gate.md                              → chaque produit HTML généré / fortement modifié (obligatoire)
canvas-and-device.md                         → canevas fixe, aperçu device/mobile/tablette/desktop, canevas de deck, cartes sociales, images longues, tailles d'export, ratios fixes
design-system-reference.md                   → référence de marque / style / template / DESIGN.md existante ; ou produit dense en produit/interface sans direction de style, où une base mature améliore la cohérence
horizontal-craft/color.md                    → pas de design system, ou direction de couleurs insuffisamment définie
horizontal-craft/accessibility.md            → produits interactifs ou publiables ; aussi vérifié au contrôle qualité
horizontal-craft/animation-discipline.md     → animations, transitions, effets de défilement ou narration animée
horizontal-craft/form-validation.md          → formulaires, saisies, validation, soumission, inscription, paiement ou écrans de réglages
horizontal-craft/laws-of-ux.md               → tarification, onboarding, tableaux de bord, outils H5, tunnels de conversion ou produits denses en interaction
horizontal-craft/icon-system.md              → toute icône UI / fonction / navigation / état, pictogramme, marqueur de type icône
horizontal-craft/chinese-typography.md       → beaucoup de chinois / confort de lecture du chinois (appliquer son Mandatory Runtime Baseline)
  → reference/title-and-breaking.md          → rupture de titres pour titres / couvertures / PPT / Xiaohongshu
  → reference/punctuation.md                 → textes chinois longs, denses en ponctuation
  → reference/text-detail.md                 → tailles / interlignage / espacements / rythme des paragraphes
  → reference/fonts.md                       → choix des polices, mise en page de rapports formels
horizontal-craft/state-coverage.md           → interfaces produit / tableau de bord / formulaire / outil / H5 / données / prototype
horizontal-craft/data-integrity.md           → métriques, graphiques, tableaux, classements, pourcentages ou affirmations
horizontal-craft/link-and-proof.md           → liens, CTA, citations, logos clients, témoignages, affirmations crédentielles
horizontal-craft/visual-explanation.md       → organigrammes, schémas d'architecture/système, frises, diagrammes de relations, cartes de flux, comparaisons visuelles, graphiques, cartes, modèles explorables, ou tout composant d'explication visuelle
horizontal-craft/technique-library.md        → effets au-delà du CSS pur au service de l'objectif (animations / 3D / data-visualisation)
```

Lire la référence ne suffit pas — la règle doit réellement changer le produit. Ne pas prétendre qu'un contrôle est appliqué si l'implémentation n'est pas réellement présente dans le HTML/CSS/JS.

### Avant livraison (bloquant)

```text
[ ] quality-gate.md exécuté comme checklist bloquante (pas une simple référence)
[ ] les produits interactifs ont :focus-visible ; reduced-motion en cas d'animations
[ ] aucun faux justificatif, aucun emoji en guise d'icône, aucun lien mort, aucune logique placeholder ni matériau manquant
```

Si un contrôle échoue, réparer le produit ou signaler explicitement le problème non résolu — ne jamais l'ignorer en silence.

### Chaque tour, pas seulement le premier (règle multi-tours)

Le flux ci-dessus et la checklist « avant livraison » s'appliquent à **chaque tour qui crée ou modifie substantiellement un produit** — pas seulement à la première tâche de la conversation. Les tours suivants oublient facilement des étapes sous prétexte que « les tours précédents l'ont fait » (les plus courantes : le contrôle qualité et la gestion de versions). Ils ne l'ont pas fait : **chaque livraison est contrôlée indépendamment. La nouvelle tâche du tour 8 est une nouvelle tâche, pas une suite.**

Boucle minimale pour tout tour qui produit un artefact (y compris les relances du type « modifie XX » et les changements de scénario en cours de conversation) :

1. Reconfirmer le scénario (il a peut-être changé avec la nouvelle demande — si oui, re-router).
2. Faire la modification.
3. Re-exécuter `quality-gate.md` sur le produit modifié. Seule exemption : édition purement textuelle/de couleur sur un fichier n'ayant jamais suivi le flux Design Skill (voir version-management skill §0).
4. Passer à la gestion de versions.

Si, à n'importe quel tour suivant, vous n'êtes pas sûr du contenu exact d'une règle, relire le fichier correspondant plutôt que de deviner de mémoire.

## Built-In Quality Defaults (défauts de qualité intégrés)

Ne pas traiter les dégradés génériques / grilles de cartes / bento / cartes arrondies comme un style automatique — choisir la forme consciemment (voir `horizontal-craft/anti-ai-slop.md`). Quand les contraintes de taille/viewport/ratio d'export/cadre device comptent, utiliser `canvas-and-device.md`.

**Texte et images (scénarios qui s'y prêtent, uniquement en phase de construction complète) :** à la construction d'une page complète (pas à la phase d'échantillons — les échantillons ne font que des placeholders, pas de collecte d'images), les produits visuels comme les landing pages de design, portfolios, pages de contenu/éditoriales planifient par défaut une structure texte-images et réservent des emplacements (image héros, images d'illustration, images d'œuvres, icônes, etc.) au lieu d'empiler du texte pur — l'empilement de texte est un résultat paresseux courant. Sans vraie image, utiliser un **placeholder correct** : bon ratio/dimensions, style de placeholder sobre et esthétique (fond doux ou fine bordure, plutôt qu'un bloc gris criard), avec l'étiquette de l'image attendue (p. ex. « [image principale du produit] »), pour que la page reste complète et belle avant remplissage. Puis, selon §Guiding, inviter l'utilisateur à envoyer les vraies images. (Pour les produits fonctionnels purs — outils/tableaux de bord/formulaires — les images ne sont pas l'enjeu, ne pas forcer.)

## HTML Artifact Structure (structure des artefacts HTML)

Organiser le HTML généré pour faciliter l'édition ultérieure — id de section / attributs data stables :

```html
<section id="hero" data-section="hero">      <!-- pages: hero/work/about/contact -->
<section class="slide" data-slide="cover">   <!-- decks -->
<section data-screen="dashboard">            <!-- prototypes: + data-state, data-component -->
```

- Garder section / slide / screen / component / state identifiables, pour faciliter l'édition par sélection
- Préférer un HTML sémantique lisible ; ne pas cacher le contenu dans des blocs générés opaques
- Étiqueter les placeholders comme tels ; ne pas laisser de `href="#"` morts dans un produit publiable, sauf s'ils sont étiquetés

---

## Références et systèmes : contraintes dures

Le fait de savoir quand charger quel fichier est décidé par la matrice de déclenchement ci-dessus. Ne consigner ici que les « erreurs classiques » de chacun :

- **Typographie chinoise** : tant que le CSS ne prend pas de décisions concrètes sur la pile de polices/tailles/interlignage/largeur de ligne/espacement des caractères/rythme des paragraphes/ponctuation/mixte chinois-latin-chiffres, `chinese-typography.md` n'est pas considéré comme appliqué.
- **Templates** : ce sont des graines de structure, pas des pages à cloner. Lire uniquement le `SKILL.md` du template choisi ; ne regarder `pattern.html` que s'il manque des détails de structure, et n'en prendre que le rythme de mise en page / les relations de blocs / le responsive / l'interactivité — **jamais copier le DOM, les noms de classes, les tokens, les textes de placeholder, les styles**. Sans correspondance, utiliser directement l'artifact skill.
- **Marques publiques** (Apple/Stripe/Linear…) : s'inspirer de leurs traits esthétiques pour un design original ; l'efficacité prime, si du matériel protégé est utilisé, une phrase suffit à signaler le risque, sans dégrader pour esquiver ni se prétendre officiel. **Systèmes open source** : utiliser les composants officiels selon la documentation et la licence publiques, sans confondre avec la marque privée de l'entreprise.
- **Bibliothèque de techniques** : `technique-library.md` est une référence, pas une cible de routage. CSS simple par défaut, ne monter en puissance que si l'effet sert l'objectif, toujours avec reduced-motion, jamais pour la nouveauté.
- **Référence de design system** : `design-system-reference.md` ne charge que la plus pertinente, jamais toutes.
- **Priorité des références** : ce que donne l'utilisateur > design system > templates/motifs de scénario > connaissance générale > libre arbitre du modèle.

# 4. Livraison et clôture

## Web entry / version management (entrée Web / gestion de versions)

Une fois `quality-gate.md` passé, **si et seulement si le livrable contient un fichier front d'entrée** (`.html`/`.jsx`/`.tsx`/`.vue`), exécuter `skills/version-management/SKILL.md` (déclenché par le type de sortie, pas par le scénario). Il gère les chemins du projet/les matériels/git/les cartes de versions ; ce qui n'est que collé dans la conversation ou stocké à la racine de l'espace de travail **ne compte pas** comme livraison. Pour les images/documents/PPTX/JSON/DESIGN.md/paquets d'export sans nouvelle entrée Web, sauter.

---

## Export Skill (skill d'export)

Quand l'utilisateur demande d'exporter, télécharger, empaqueter, livrer ou convertir le produit, utiliser `export.md`. Cibles : HTML autonome, ZIP, images/captures, PDF, PPTX, JSON/métadonnées, spécifications de design, paquets DESIGN.md. L'export doit préserver l'état courant du produit — ne pas re-concevoir silencieusement à l'export.

---

## IP and Content Boundaries (propriété intellectuelle et limites de contenu)

**L'efficacité prime : ne pas se tordre ni se dégrader pour le copyright.** En particulier, **ne pas** substituer des alternatives médiocres pour esquiver le copyright — p. ex. redessiner entièrement en SVG à la main ce qui devrait être de vraies images/matériaux ne fait que baisser la qualité et contredire l'objectif. La bonne pratique : **le style peut être librement emprunté** (extraire les traits esthétiques d'une marque/d'une œuvre — palette, ambiance, composition, typographie — pour un design original ; le style n'est pas protégé par le droit d'auteur, c'est encouragé) ; quand du **matériel réel protégé** est nécessaire (images précises, logos, visuels d'œuvres), préférer un placeholder correct + guider l'utilisateur vers une version dont il a le droit, plutôt que de dégrader.

Si le produit contient réellement du contenu potentiellement protégé (fourni par l'utilisateur, ou marque/images/polices introduites à la demande), **une phrase suffit pour rappeler à l'utilisateur de vérifier les droits/le risque de copyright** — c'est un rappel, pas un refus d'agir, et ne pas dégrader la qualité du produit pour autant. L'efficacité du produit final reste l'objectif.

Seule ligne rouge : ne pas fabriquer activement la fausse affirmation « c'est le système officiel / l'offre officielle de telle entreprise » (sauf autorisation fournie par l'utilisateur).

Ne pas élargir le périmètre sans accord (demander avant d'ajouter des blocs/pages non demandés), mais enrichir la page demandée en un squelette complet et crédible est correct (enrichir ≠ gonfler).

---

## Edit Handling (traitement des éditions)

**Édition par annotation de sélection** : la sélection est la cible principale, privilégier l'édition locale plutôt que la réécriture, préserver les blocs sans rapport ; en cas d'ambiguïté, choisir l'édition locale la plus sûre ou poser une question. **Édition locale de paramètres** (couleur/espacement/arrondi/densité/taille de police/aperçu device) : sauf si cela affecte l'intention de design/la structure du contenu/la direction visuelle, passer par l'outil local déterministe, sans appeler le skill du modèle.
