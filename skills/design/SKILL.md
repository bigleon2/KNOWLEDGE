---
name: Design Skill
description: Route design-related HTML artifact tasks (landing pages, portfolios, prototypes, decks, content pages, web tools, social cards, info-interactive) to the right artifact skill, and decide whether to use design-system-reference, design-system-generation, or export. Use for any UI/visual/HTML design work.
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Design Skill (compétence design)

Le **routeur** des productions HTML à caractère design : décide si la tâche relève du design, quel artifact skill prend le rôle principal, s'il faut `design-system-reference.md` / `design-system-generation.md` / `export.md`, et combien clarifier avant d'agir. (La structure des productions, le jugement de scénario, le craft transversal et la référence/export relèvent respectivement des artifact skills, d'horizontal-craft/ et des fichiers correspondants.)

---

## Flux d'ensemble

Voici un flux unique ; la plupart des étapes sont internes et instantanées — on ne s'arrête pour questionner que quand le besoin est **réellement ambigu**. **Ne jamais** transformer une étape en formulaire à remplir ou en fichier à lire d'abord.

```text
Requête utilisateur
   │
   ▼
1. Comprendre les trois axes (en interne, instantané ; silence sur l'évident)
     • content (contenu)  — sujet, information, objectif
     • scenario (scénario) — forme + intention → quel artifact skill (voir Routing)
     • style               — l'utilisateur a-t-il donné un indice de style (voir Style Routing)
   Contenu manquant → demander ; scénario manquant → demander. (C'est le seul endroit
   « question par manque d'information ».)
   Trancher en même temps : scénario « interface (stabilité, cohérence) » ou
   « créatif (unicité, impact) » — ce choix détermine la présentation du style à l'étape 2
   et, plus loin, la voie design system vs création originale.
   Demandes créatives : faire au passage la lecture créative (Design Read, voir §Creative Context).
   │
   ▼
2. Confirmer le cadre de contenu + l'orientation de style (à confirmer par défaut ;
   sauter dimension par dimension ce qui est déjà clair)
   ⚠️ C'est LA pause obligatoire avant construction — **présenter ce qui doit être confirmé,
   puis s'arrêter et attendre la réponse ; jamais sauter cette étape pour construire le site
   entier**. Chercher/lire les supports puis construire directement sans confirmation est une erreur.
   Dans « le même tour », livrer ensemble ce qui doit être confirmé :
     • Cadre de contenu (plan) :
         - à étudier (supports fournis) / à rechercher (sujet réel) / formulation vague →
           lister le plan pour validation (pour l'étude, vraiment lire les supports en profondeur
           avant de proposer une architecture — pas d'extraction « juste suffisante »)
         - l'utilisateur a déjà tout structuré (modules listés explicitement) → ne pas reconfirmer,
           utiliser tel quel
     • Orientation de style :
         - style explicite (style nommé / image donnée / site ou marque de référence / DESIGN.md)
           → pas de cartes de style, suivre l'indication
         - implicite + interface → cartes de style montrant plusieurs design systems matures
           (recherche de stabilité)
         - implicite + créatif → cartes de style montrant plusieurs directions créatives
           (recherche d'unicité)
   Forme des cartes : §Style Sampling (cartes simples côte à côte, A/B/C, jamais d'onglets).
   Ex. : « un site personnel pour Kenya Hara » → créatif, recherche nécessaire, style implicite →
   après recherche sur ses œuvres réelles, lister le plan (quels blocs/quelles œuvres) + trois cartes
   de directions créatives → **s'arrêter et attendre validation et choix de direction** → seulement
   alors construire (étape 3). Jamais : recherche finie, site entier sorti d'un coup.
   Les deux dimensions se jugent séparément : toutes deux claires → étape 3 directe ; dès qu'une
   dimension demande confirmation, pause obligatoire.
   Après réponse, étape 3. Si l'utilisateur n'ajuste que le contenu (sans changer de direction),
   garder la direction choisie, sans nouvelles cartes.
   │
   ▼
3. Vérifier les gabarits (seulement si le scénario touche la bibliothèque)
   Chercher dans `design-templates/INDEX.md` par support + scénario : correspondance nette →
   adopter comme point de départ et lire son SKILL.md (généralement mieux que de zéro) ;
   rien de convenable → artifact skill directement, jamais forcer un gabarit.
   Le gabarit est une ossature de départ, pas un clone — conserver le contenu réel de
   l'utilisateur, appliquer artifact skill + horizontal craft.
   │
   ▼
4. Compléter les dimensions restantes du style (dans la grande direction fixée à l'étape 2)
   La direction est déjà posée à l'étape 2 (imposée / design system / direction créative).
   Ici, seulement remplir les dimensions concrètes non couvertes, par priorité de source :
   ① description immédiate de l'utilisateur (maximale, verrouillante) ② DESIGN.md
   ③ gabarit/semence ④ contraintes parallèles en repli (ne charger que le nécessaire :
   polices/icônes/couleurs…). Les sources se combinent.
   Conflit : si la description de l'utilisateur contredit le design system sur une dimension,
   l'utilisateur prime, avec une phrase pour signaler l'écart.
   │
   ▼
5. Annonce de chantier (avant toute construction longue) — voir §Build Preview
   Interdit de dire seulement « un instant ». D'abord une annonce de chantier avec du contenu,
   en langage humain : quels blocs, comment présentés, couleurs/polices, durée estimée.
   Pendant la construction, pas de compte rendu temps réel possible (l'écriture de fichier est
   un appel d'outil unique, pas de rendu en flux) : l'information doit être donnée en une fois
   avant de commencer, pour que l'attente ait du contenu et que la direction soit vérifiable.
   │
   ▼
6. Construire : le jugement de l'artifact skill + le style complété + la direction choisie à l'étape 2.
   │
   ▼
7. Guider la suite — à chaque tour, au jugement (voir §Guiding the Next Step)
   Selon la situation, proposer « au plus une » suite pertinente : combler un manque, relier
   l'usage (offrir les produits d'accompagnement), signaler une nouvelle bifurcation, diagnostiquer
   la dimension la plus faible, pointer vers le partage ou l'édition. Rien de pertinent → ne rien
   proposer ; montrer le chemin, ne pas faire à la place.
   │
   ▼
8. Porte de qualité — avant livraison, dérouler quality-gate.md comme liste de contrôle finale
   condensée. (Vaut pour « chaque » tour produisant un livrable, pas seulement le premier —
   voir §Every turn.)
```

---

### Interface vs créatif : les deux voies du style (principe cardinal)

Le classement « interface / créatif » de l'étape 1 détermine comment le style se fixe — **c'est un principe directeur de tout le flux** :

- **Interface** (prototypes produit, dashboards, back-offices, outils web, formulaires/onboarding/checkout, interfaces denses en données, pages corporate/notification génériques) : recherche de maturité et de cohérence, **via design system, non via le goût libre du modèle**. Mapper le scénario (et tout mot d'humeur) via les tags `mood` vers une entrée `design-systems/style-skills` comme socle UI — un vrai système apporte structure, discipline de composants, rythme des espacements, états et conventions d'interaction. Style implicite : les cartes de l'étape 2 montrent plusieurs design systems.
- **Créatif** (sites de marque, campagnes, portfolios, hero de landing, sujets éditoriaux/culturels, cartes sociales, pages de contenu) : recherche d'unicité et d'impact, **via le jugement visuel de l'artifact skill + horizontal craft + Creative Context, en création originale**. On peut *s'inspirer* du tempérament d'un système (une marque nommée charge `brand-inspiration`), sans être enfermé dans une suite UI générique. Style implicite : les cartes de l'étape 2 montrent plusieurs directions créatives.

Le critère en une phrase : **ce livrable cherche-t-il « fiable et cohérent » ou « unique et marquant » — fiable → design system ; marquant → original (avec référence possible).** Si le style est explicite (nommé / image / référence / DESIGN.md), aucune carte pour personne : suivre l'indication.

---

Sources de contexte pouvant alimenter l'étape 4 : contenu utilisateur, captures, gabarit/semence retenu, `DESIGN.md` téléversé, production courante, éléments de marque, pages existantes, design system / suite UI, ou références Figma/dépôt. Utiliser ce qui est là ; ne lire le fichier de contraintes parallèles correspondant que si aucune autre source ne couvre la dimension.

---

## Discipline de sortie : cacher les noms, pas les productions (tout le long, priorité maximale)

Vis-à-vis de l'utilisateur, **ne cacher que les « noms » des opérations internes, jamais leurs « productions »**.

- **À ne pas prononcer** : noms d'opérations/mécanismes internes (Content Read, Style Sampling, Design Read, Creative Context, Variation Policy…), logique de fonctionnement du skill, motifs de décision.
- **À donner normalement** : les productions de ces opérations — l'analyse de design (« je le comprends comme… »), le plan de contenu, l'orientation de style (échantillons), l'annonce de chantier, les suggestions de suite, les questions à l'utilisateur. En langage humain, sans étiquette « voici mon Content Read ».

En cas de doute, pencher pour **donner** : ne garder le silence que sur les quelques noms d'opérations ; toute analyse ou production utile à l'utilisateur se dit clairement — ne jamais dissimuler ou expédier plans, positionnements de design, orientations de style « par peur d'exposer ».

- ✅ « J'ai mis de l'ordre dans tes supports : trois blocs X / Y / Z (liste complète), et voici trois directions de style — dis-moi si le découpage est juste et laquelle tu préfères. »
- ❌ « Je fais mon Content Read et mon Style Sampling. » (noms prononcés)
- ❌ (contenu à étudier validé, mais on se lance sans lister le plan) (production cachée)

**Insistance : les productions des tours de confirmation fusionnés — plan de contenu, orientation de style (voir §Content Read / §Style Sampling) — doivent être présentées à l'utilisateur pour validation ; comprendre « ne pas exposer la logique interne » comme « ne pas donner le plan » est une erreur.** La pause de validation reste une pause ; seuls les noms d'opérations disparaissent du discours.

En une phrase : **on ne rapporte pas les « noms d'opérations », mais on livre normalement leurs « productions ».**

# 1. Comprendre d'abord

Cette partie décide « quoi penser clair avant de faire ». La plupart du temps intériorisé, instantané ; une seule question si vraiment ambigu.

## Role (rôle)

Cet agent est « orienté design », pas un générateur UI générique — il apporte à chaque production un jugement de design : comprendre l'usage du livrable, décider ce que l'utilisateur voit en premier, supprimer les éléments indignes de leur place, passer par des références avant le goût générique, garder une structure pour l'édition ultérieure, produire quelque chose d'utilisable, éditable et intentionnel.

L'objectif n'est pas de générer plus d'interfaces, mais de créer un artefact de design qui aide l'utilisateur à communiquer/tester/publier/présenter/livrer quelque chose d'utile.

---

## Content Language (langue du contenu)

La langue du contenu HTML généré doit suivre la langue de conversation de l'utilisateur, sauf demande explicite d'une autre langue.

Règle : l'utilisateur écrit en chinois → tout le texte visible (titres/corps/étiquettes/CTA/microcopies/navigation/placeholders/alt) en chinois ; en anglais → anglais ; mélange → suivre la langue dominante, en conservant naturellement les mélanges (noms de produits, termes). Vaut pour tous les scénarios. `<html lang>` doit coïncider avec la langue du contenu. Sur un gabarit, remplacer les textes placeholder par la bonne langue, sans garder les placeholders anglais d'origine.

Au contenu chinois/CJK détecté (par cette règle ou par demande), charger `horizontal-craft/chinese-typography.md`. **Règle de fer des polices (en vigueur avant même de lire ce fichier) : toute police non système du `font-family` doit être réellement chargée (`<link>` ou `@font-face`), et toute page contenant du chinois doit avoir un nom de police CJK dans son `font-family` — jamais laisser une police latine retomber directement sur `system-ui`, sinon le chinois se rendrait avec une police de repli incontrôlée.** Détails dans `horizontal-craft/fonts.md`.

Ne pas faire confirmer la langue du contenu, sauf ambiguïté réelle (brief bilingue sans dominante).

---

## Core Principle (principe cardinal)

Agir par défaut, mais ne pas conceir aveuglément.

Questionner sélectivement : par défaut, pas de long questionnaire ; mais demander quand un bref éclairage améliore substantiellement le résultat. Sinon, inférer des hypothèses raisonnables de : la requête, le contexte de l'espace de travail, le contenu/références fournis, le gabarit retenu, l'état de la production courante, le `DESIGN.md` téléversé, les patterns usuels du scénario.

Ne demander que si l'information manquante rend le résultat : inutilisable, ingénérable, à risque juridique/marque, ou visiblement à côté de l'intention. Sinon, générer une première version raisonnable et laisser l'utilisateur peaufiner par annotations de sélection, éditions locales, relances ou export.

**Exception — tâches avec support source (voir Content Read) :** quand l'utilisateur joint un support ou qu'il faut présenter un sujet réel, ne pas sauter sur une première version : lire le contenu, proposer l'architecture, confirmer. « Agir par défaut » vaut pour les demandes abstraites/créatives ; la profondeur des tâches à support vient de la lecture préalable.

---

## Content Read (lecture de contenu)

C'est l'« axe contenu » de l'étape 1 — au même rang que Creative Context (axe style) et Routing (axe scénario). Le flux nomme trois axes (content / scenario / style) ; c'est ici que l'axe contenu se réalise. Il **ne vaut que pour les tâches avec support source**, définies par :

- l'utilisateur joint un matériau à présenter ou sur lequel construire : PDF, document, présentation, jeu de données, tableau, collection d'images, site/texte existant ; ou
- la tâche présente un **sujet réel** avec une information réelle : portfolio d'œuvres réelles, présentation personnelle/société/produit/événement, rapport ou data-story, « présenter XX / faire un site sur XX ».

Il **ne vaut pas** pour la génération abstraite sans source réelle (« une page d'événement club de lecture », « une landing pour un outil IA », « une affiche ») — celles-ci suivent le scaffold de la politique d'hypothèses par défaut et restent sur le chemin rapide. La ligne de partage : **y a-t-il un contenu réel à comprendre, ou invente-t-on un point de départ plausible ?**

Pour les tâches avec support, avant structure / style / gabarit / construction :

```text
Content Read (tâches avec support uniquement)
1. read_through (lire à fond) : vraiment lire tout le support — pas d'extraction « juste
                         suffisante ». « survoler puis construire » est précisément le mode
                         d'échec qui amincit le résultat.
2. extract (extraire) :    retirer les blocs d'information réels. Portfolio : pour chaque
                         projet, défi / ce que tu as fait / résultat + quelles images s'y
                         rattachent. Présentation/rapport : faits clés, chapitres, figures,
                         citations. Comprendre le sens de chaque matériau et où il doit
                         aller — jamais choisir les images par taille de fichier ou ordre
                         d'apparition.
3. architect (structurer) : dériver l'architecture de l'information du contenu — quels
                         blocs, que dit chaque bloc, ce que l'utilisateur doit voir en
                         premier, la correspondance matériau→bloc. La structure pousse
                         depuis le matériau ; elle ne vient ni des emplacements par défaut
                         d'un scénario, ni de la liste de blocs d'un gabarit.
4. confirm (confirmer) :   dans « un seul tour », présenter le cadre de contenu (un plan
                         court : blocs, contenu de chaque bloc, l'élément premier/le plus
                         fort, correspondance des matériaux) avec trois échantillons de
                         style commutables (voir §Style Sampling). Demander à l'utilisateur
                         de valider le cadre et choisir une direction en une seule réponse.
                         Un tour, pas un interrogatoire — « un plan + trois échantillons de
                         premier écran ». Puis enchaîner l'étape 3 et la suite.
```

La profondeur, pas l'empilement : l'objectif est de vraiment comprendre et organiser le contenu, pas plus de blocs ou des textes plus longs. Cela sert — sans jamais primer sur — l'« interdiction d'inventer / anti-recettes IA » : lire à fond n'autorise ni forger ni gonfler ; ce que le support n'a vraiment pas (ex. un projet sans résultat) se signale ou se remplace par un placeholder clairement étiqueté, sans invention.

**Exigence de présentation (à respecter scrupuleusement) :** l'étape confirm doit lister le plan de contenu **réellement et intégralement dans la réponse** (blocs, contenu, premier élément, attribution des images), avec les trois directions de style, demander validation, puis s'arrêter — ne jamais poursuivre seul vers la page complète. Le plan est une production à livrer, **non soumise à la discipline de dissimulation** (ne juste pas prononcer « Content Read » ; ne pas omettre le plan). Cacher le plan et construire directement est une erreur. Ce tour fusionné aligne « quoi dire + à quoi ça ressemble » d'un coup et évite « 5 minutes perdues sur une mauvaise direction » ; les tâches abstraites n'ont pas cette pause.

---

## Style Sampling (échantillons de style)

Les échantillons de style sont produits dans « le même tour de confirmation » que le cadre de contenu (étape 2), pas dans une étape séparée ultérieure. C'est voulu et non du gaspillage : cela permet de choisir la direction visuelle « en regardant » (l'utilisateur choisit mal un style depuis une description textuelle, surtout sans design system nommé à capturer), cela élimine la première source de reprise intégrale (« pas ce feeling → tout refaire ») et fabrique en un tour un point de décision naturel et de qualité. **Après avoir donné les échantillons : pause obligatoire, attendre le choix A/B/C ; jamais choisir à la place de l'utilisateur et partir sur le site complet.**

```text
Style Sampling (produit avec le cadre de contenu, étape 2)
0. Dire d'abord les directions : une ou deux phrases sur l'intention/le ton des trois
                          directions (le tempérament seulement, sans figer couleurs ni
                          polices), puis générer le HTML des échantillons dans la même
                          réponse.
1. one file (un fichier) : les trois directions dans « un seul fichier HTML », montrées
                          « côte à côte dans la même page ».
                          ⚠️ Obligatoirement côte à côte ; jamais onglets / bascule /
                          repli — la bascule exige des allers-retours et interdit la
                          comparaison, ce qui tue l'échantillon. Bureau : trois colonnes ;
                          mobile étroit : empilement vertical. Jamais trois fichiers/
                          aperçus séparés — le produit n'affiche qu'une production à la
                          fois.
2. forme sample :          pour chaque direction, une « carte de style simple » — pas une
                          mini-page web, pas une vignette haute fidélité. Le but est de
                          faire ressentir la direction d'un coup d'œil : rester léger — un
                          titre d'exemple (typographie), une ou deux lignes de texte de
                          démonstration + un bouton/étiquette de démonstration (mise en
                          page de base et blancs), la palette de la direction (fond + texte
                          + accent). ⚠️ Pas de hero complet, pas de blocs de contenu réel,
                          pas de finition proche du produit final — ce serait lent et lourd
                          et ce n'est pas le but. Les trois cartes ensemble doivent être
                          rapides et légères, très en deçà d'une page complète. La « finesse »
                          vient après le choix, lors de la construction intégrale.
                          ⚠️ Au stade échantillon : ne pas collecter ni embarquer d'images
                          réelles — l'illustration relève de la « construction complète » ;
                          pour suggérer un emplacement, juste un bloc de couleur minimal ;
                          jamais chercher/générer des images pour l'échantillon (ce serait
                          le ralentir).
3. label (étiquette) :     un repère A / B / C visible en haut à gauche de chaque
                          échantillon ; le titre en bas porte aussi le numéro (« A · galerie
                          d'encre » / « B · blanc de papier de riz » / « C · sans-serif
                          moderne »), avec une ligne de description et des pastilles de
                          couleur. L'utilisateur doit pouvoir désigner d'un mot (« je
                          prends A »).
4. content :               les trois utilisent le même contenu déjà validé.
5. distinct (différenciation) : les trois doivent différer sur des dimensions réelles —
                          palette / tempérament typographique / ton d'ensemble, pas une
                          décoration de surface.
6. pick (choix) :          demander à l'utilisateur de choisir en une réponse (« A, B ou
                          C ? »), quitte à ajuster le cadre en même temps ; puis construire
                          la page complète dans la direction choisie, couvrant tous les
                          blocs validés.
```

Le nerf de la guerre : **l'échantillon doit être « léger ».** La dérive la plus fréquente : trois vignettes haute fidélité (lentes, lourdes, et qui dégénèrent en onglets) — à éviter ; il suffit que la palette, le tempérament typographique et le ton se distinguent d'un coup d'œil ; la finition attend le choix. Avec §Content Read, c'est l'unique préalable des tâches à support : un tour qui donne « quoi dire (cadre) + à quoi ça ressemble (trois échantillons) » → validation et choix → une construction intégrale assurée. Les échantillons n'ont lieu qu'à la première construction ; ensuite, éditions locales/itérations normales, sans nouveaux échantillons.

---

## Guiding the Next Step (guider la suite)

Le levier de l'étape suivante, selon la situation :

- **un manque** → combler (le plus typique : images placeholder → inviter l'utilisateur à fournir les vraies).
- **déjà formé** → relier à l'usage : si l'usage est inconnu, demander et offrir l'accompagnement. Accompagnements naturels : landing → cartes sociales/version e-mail ; deck → notes d'orateur ; portfolio → page détail d'un projet.
- **une nouvelle bifurcation se dessine** → la signaler (ex. « cette version penche marketing ; pour une recherche d'emploi, plus de retenue — laquelle ? »). Une direction déjà choisie à l'échantillonnage ne se rouvre pas.
- **encore perfectible** → diagnostiquer la dimension **actuellement la plus faible** et offrir la correction : hiérarchie de l'information / parcours de conversion / densité et blancs / cohérence / rapport texte-image / animations d'entrée / ambiance sonore / blocs de persuasion. Le grossier (structure/parcours) avant le fin (espacements/réglages) ; le réglé ne se rouvre pas ; ce que l'utilisateur a verrouillé reste fermé ; si c'est déjà complet ou que le style s'y prête mal, ne rien dire.
- **petites retouches dictées** → indiquer que l'entrée d'édition de l'aperçu est plus rapide.
- **envie de publier** → pointer le bouton de partage au-dessus de l'aperçu.

Partage/édition : montrer le chemin, ne pas faire à la place ; les optimisations proposées se font par l'agent après accord.

---

## Build Preview (annonce de chantier : avant toute construction longue)

La construction d'une page complète prend une à deux minutes ; c'est sur un « un instant » suivie d'un écran noir que l'utilisateur s'évapore. **Pendant la construction, pas de compte rendu en direct possible** (l'écriture est un appel d'outil unique, pas de rendu en flux — « écrire en commentant » est impossible, ne pas le promettre). L'information se donne donc **en une fois avant de commencer** : avant d'entrer en construction, une **annonce de chantier avec du contenu**, en langage humain — quels blocs, présentation approximative de chacun, orientation couleurs/polices, durée honnête. Puis on construit.

Exemple : « cette version : un hero en grands caractères sur sa philosophie du design, encre et blancs ; la section œuvres en trois temps MUJI/typographie/HOUSE VISION avec une œuvre phare chacun ; palette noir d'encre + blanc de papier de riz, titres en Noto Serif SC. Environ 1–2 minutes. »

Cela transforme « l'attente aveugle » en « attente informée » et réaligne la direction au passage (une erreur se fait arrêter sur-le-champ). **« C'est parti, patientez un instant » ne satisfait pas l'exigence** — l'annonce doit avoir du contenu (blocs + présentation + couleurs/polices + durée). Les petites retouches de quelques secondes n'exigent pas d'annonce.

---

## Creative Context Completion (complétion du contexte créatif)

**La méthode pour fixer la direction : un référent concret, pas une cascade d'adjectifs.** « Moderne/propre/crédible/premium » ne spécifie rien — le modèle ne produira que le centre tiède de ces mots ; un adjectif décrit une « zone », un référent concret décrit un « point ». Remplacer par un monde précis (« les polycopiés d'une vieille université, années 1970 », « l'emballage minimaliste d'un parfumeur indépendant de Tokyo », « la mise en page d'un magazine japonais des années 90 ») : une seule phrase entraîne couleurs, typographie, blancs, ornement ou pas — et dit d'elle-même « ce que ce n'est pas » (un polycopié ne brille pas, n'utilise pas de dégradé, sans déclaration supplémentaire). La position créative se pose donc d'abord sur un référent concret, dont on déduit les détails.

Pour la génération ouverte, avant construction, compléter silencieusement un court contexte créatif (une phrase par item ; pris de l'utilisateur si fourni, sinon inféré du scénario/audience/contenu/références ; non montré à l'utilisateur sauf utilité) :

```text
Creative Context
1. creative_positioning : ce dont il s'agit vraiment, au-delà de la demande littérale
                          (viser un référent concret)
2. first_impression :    ce que le public doit ressentir dans les 3 premières secondes
3. anti_default :        quel défaut générique éviter
```

La production doit le manifester visuellement.

### Dire d'abord une phrase de Design Read (lecture de design)

Puis une phrase explicite sur la façon dont tu lis la demande :

Format : **« Je le comprends comme : une <type de page> pour <audience>, <tempérament/ton>, s'orientant vers <direction / système / référence>. »** (ex. : « une landing SaaS pour acheteurs techniques, calme et précise, s'orientant vers un système retenu à la Linear. »)

**Cette phrase d'analyse de design se dit réellement à l'utilisateur** (production de catégorie B, non soumise à la dissimulation — on ne cache que le mot « Design Read », pas l'analyse ; pas d'étiquette « voici mon Design Read », mais l'analyse se donne). Elle permet de vérifier d'un coup d'œil que la direction est juste. Si un axe est réellement ambigu, poser ici L'unique question focalisée, plutôt que deviner.

**Le Design Read doit se clore par une sous-phrase « source du style » — obligatoire, l'une des trois, jamais vide :**

- **Scénario interface** (prototype, info-interactive, outil web, dashboard/back-office) : nommer un système — « s'orientant vers <style-skill> (apparié par tag d'humeur) », ou, marque spécifiée, « s'orientant vers <brand> issu de brand-inspiration ». Par défaut un système mature ; ne pas fabriquer l'UI de zéro.
- **Scénario créatif** (landing, portfolio, campagne, cartes, contenu) : « référencant le <tempérament> de <system>, mise en page originale » ou « direction originale : <une phrase> ». Les deux sont valides — « original » est une source légale ; l'important est qu'on ait considéré la bibliothèque.
- **Tout scénario + marque spécifiée** → « s'orientant vers <brand> issu de brand-inspiration ».

### Puis classer interface/créatif ; les scénarios créatifs (expressifs) exigent un engagement visuel concret

Reprendre le classement de l'étape 1 (voir le principe cardinal). **Créatif/expressif** (site de marque, campagne, portfolio, hero de landing, sujet éditorial/culturel, couverture sociale) : l'impact visuel fait partie du contrat — une page centrée, correcte mais sage, est un échec ; prendre l'engagement ci-dessous. **Interface/retenu** (dashboard, back-office, outil, formulaire, notification, rapport) : la clarté calme EST le contrat — animations minimales, mise en page régulière, engagement sauté.

Pour le **créatif/expressif**, engagement silencieux avant d'écrire le code — chaque item est un élément concret + une action, jamais un adjectif (« audacieux/premium/stupéfiant » interdits : ils ne contraignent rien) :

```text
Visual commitment (scénarios expressifs uniquement)
1. hero_subject :   LE « un » élément agrandi/dominant (ex. nom du produit sur 1/3 du viewport,
                    palette spécifique)
2. entrance :       quels éléments entrent, comment
3. break_symmetry : où la mise en page rompt le centrage/la grille
4. focal_contrast : ce qui pose le regard en premier (saut de taille / aplat de couleur / blanc)
```

Une page entièrement centrée, symétrique, statique, sans élément dominant est le résultat « médiocre » par défaut — pour un scénario expressif, cela signifie l'engagement non tenu. Exécuter item par item. Détails d'animation → `horizontal-craft/animation-discipline.md`.


## Compléter l'ossature de contenu des demandes abstraites (sans forger de faits)

Les demandes abstraites (« une page d'événement club de lecture ») veulent un **point de départ** éditable, pas une coquille vide : ériger avec des contenus d'exemple concrets et crédibles le cadre exigé par le scénario (une page quasi vide, même techniquement correcte, est un échec), écrire des textes de démonstration précis (un vrai nom d'événement, trois points d'ordre du jour concrets) plutôt que `Lorem ipsum` ou des placeholders vides. **L'ossature ne vaut que pour les demandes abstraites sans support** — avec support/sujet réel, blocs et contenu viennent du Content Read et de sa validation.

**Ce n'est pas de la fabrication ; la ligne de partage :** remplissable librement (structurel/démonstratif : structure des blocs, arguments, programmes, FAQ, noms de produits d'exemple, emplacements d'images clairement étiquetés) ; **à ne jamais forger** (factuel/crédentiel : chiffres précis, logos de clients nommés, témoignages, prix, couverture médiatique, notes — toute affirmation sur le réel : sans preuve réelle, un placeholder clairement étiqueté, jamais d'invention).

---
# 2. Router — décider quoi faire

Fixer d'abord la forme et l'intention, puis le format de sortie et la source de style.

## Routing (routage)

Router par **artifact skill principal** (pas de couche de routage séparée par « bac de formes »). La forme de sortie (`output_target`) découle de l'artifact skill choisi + de la requête, pour fixer forme technique/dimensions/export/références ; rien à consigner à part, ce n'est pas une couche de routage.

## Primary Routing — Artifact Skills (routage principal)

Pour une production concrète, choisir précisément UN artifact skill principal. Celui-ci définit forme, structure, mécanisme de sortie et attentes d'édition.

| Artifact skill | Quand l'utilisateur veut… | output target par défaut |
|---|---|---|
| `landing-page.md` | landing produit, page d'accueil, site SaaS, page marketing, waitlist, page de service | `responsive-html` |
| `portfolio.md` | site perso, portfolio, page de créateur, page CV, vitrine de projets | `responsive-html` |
| `prototype.md` | prototype d'app, prototype de produit web, démo produit/fonction, dashboard, back-office, parcours produit, wireframe, maquette UI | `responsive-html` ou `mobile-html` |
| `content-page.md` | article, page éditoriale, newsletter, mise en page WeChat/compte officiel, page de longue lecture | `responsive-html` |
| `info-interactive.md` | page d'explication, explication visuelle, diagramme de flux, schéma d'architecture, schéma de système, cartographie de processus, graphe de relations, frise, navigation comparative, page de savoir/ressources filtrable, rapport interactif, data-story, explication explorable ; mots déclencheurs courants : « expliquer clairement / mettre de l'ordre / illustrer / visualiser / flowchart / architecture / relations / timeline / page comparative » | `responsive-html` |
| `web-tool.md` | outil web mono-tâche, calculateur, générateur, vérificateur, sélecteur, quiz, test, minuteur, outil de décision ; bureau ou mobile/H5 | `responsive-html` ou `mobile-html` |
| `social-card.md` | couverture/carte sociale, Xiaohongshu, couverture WeChat/Douyin, séquence de cartes long format, visuel social à taille fixe | `fixed-image` |
| `deck.md` | diapositives, présentation, pitch deck, deck de rapport, deck de stratégie, atelier, enseignement | `html-slide-deck` |

### Mot ambigu : demo

« demo / fais une démo de XX / démonstration » = par défaut **un prototype produit interactif et cliquable** (`prototype.md`, livraison double fichier prototype.html + flow.html), **jamais** par défaut une page marketing/événement. Uniquement si la demande porte explicitement une intention marketing (landing/site officiel/promotion/waitlist/page d'événement) → `landing-page.md` ; un petit outil mono-tâche → `web-tool.md` ; des slides de pitch → `deck.md`. Si le sujet ne se prête pas à une démonstration interactive, demander, plutôt que dégrader silencieusement en vitrine.

## Output Target (cible de sortie)

Sert à fixer forme technique, dimensions, comportement d'export et références d'appui (dérivée de l'artifact skill + de la requête ; pas une couche de routage) :

| Output target | Sens | Références d'appui usuelles |
|---|---|---|
| `responsive-html` | page navigateur défilable ou interactive | `canvas-and-device.md`, `horizontal-craft/accessibility.md` |
| `mobile-html` | page interactive mobile-first, H5 ou outil web mobile | `canvas-and-device.md`, `horizontal-craft/state-coverage.md`, `horizontal-craft/form-validation.md` |
| `html-slide-deck` | présentation HTML une page par écran | `deck.md`, `design-templates/`, `canvas-and-device.md` |
| `fixed-image` | carte sociale, couverture, affiche, long format ou planche d'export à taille fixe | `social-card.md`, `canvas-and-device.md` |
| `design-system-spec` | `DESIGN.md` / tokens / règles de composants réutilisables | `design-system-generation.md` |
| `package` | livraison ZIP/PDF/PPTX/image/export | `export.md` |

## Style Routing (routage du style ; comment traiter un indice de style)

Les demandes portent souvent un indice de style. Avant de mobiliser les bibliothèques, classer l'indice — **la plupart des indices ne sont pas une recherche de référence**. Cela évite deux échecs : traiter un simple adjectif en recherche de bibliothèque, et confondre « lire une charte » et « écrire une charte ».

| L'indice de style est… | À traiter comme… | Destination |
|---|---|---|
| un adjectif / mot d'humeur (« tech », « épuré », « premium ») | aiguillage interface/créatif | voir le principe cardinal (interface → mapper un style-skill ; créatif → direction créative) |
| une marque nommée (« style Apple », « like Stripe ») — **tout scénario** | une **référence de marque** | `skills/design/design-system-reference.md` → `design-systems/brand-inspiration/` (niveau site/marque ; lire le DESIGN.md de la marque) |
| un style skill nommé (« avec le style `minimal` », « atelier-zero ») | un **style skill** | `skills/design/design-system-reference.md` → `design-systems/style-skills/` |
| un système existant à suivre (DESIGN.md téléversé, capture, production précédente, « comme notre produit ») | une **référence fournie** | `skills/design/design-system-reference.md` (cohérence avec la source donnée) |
| « extraire / définir / produire un DESIGN.md réutilisable » | une **tâche de génération** | `design-system-generation.md` |

Distinctions clés (le ① relève du principe cardinal) : ② **un mot de marque atteint toujours brand-inspiration** (l'aspect officiel, le mieux pour les pages marketing/créatives). ③ **lire vs écrire un DESIGN.md** — « dans le style Apple » : la marque est référence de lecture, le livrable reste la page ; seule la demande « produire un DESIGN.md réutilisable » passe par `design-system-generation.md` pour écrire une charte.

Un indice de style ne change jamais l'artifact skill principal (« une landing à la Apple » reste `landing-page.md`).

---

## Désambiguïsation des artifact skills (les frontières que le tableau ne tranche pas)

- **social-card vs content-page** : carte/couverture/visuel à taille fixe/Xiaohongshu/couverture WeChat-Douyin/carte de capture/carte KPI/carte de citation/séquence long format → `social-card.md` ; page de lecture linéaire → `content-page.md`.
- **content-page vs info-interactive** : lire → `content-page.md` ; comprendre/illustrer/expliquer/comparer/filtrer/visualiser (« mets de l'ordre », « fais un schéma », « flowchart », « architecture », « timeline », « page comparative ») → `info-interactive.md`, même si la production reste surtout du HTML/SVG statique.
- **frontière info-interactive** : expliquer de *l'information*, pas démontrer un *produit* ; un corps d'information fixe, pas des données temps réel ; si le support est explicitement une slide ou un visuel social, prendre le skill de ce support + `horizontal-craft/visual-explanation.md`.
- **skills inexistants, prendre le substitut** : dashboard → `prototype.md` à dominante tableau de bord ; app mobile → `prototype.md` + `platform: mobile` ; affiche → `social-card.md`. Skill absent → le plus proche ; ne signaler le manque que s'il gêne l'exécution.

# 3. Bien le faire — exécution, qualité, références

## Execution essentials (l'essentiel de l'exécution)

### Ne charger une référence que si son déclencheur apparaît

C'est l'unique critère du « quand lire quoi ». Par défaut, rien ; 1 à 3 fichiers pertinents par tâche.

```text
quality-gate.md                              → toute production HTML générée / fortement modifiée (obligatoire)
canvas-and-device.md                         → canevas fixe, aperçu device/mobile/tablette/bureau, canevas deck,
                                              carte sociale, long format, dimensions d'export, ratio fixe
design-system-reference.md                   → présence d'une référence marque / style / gabarit / DESIGN.md ; ou
                                              production à dominante produit/interface sans direction de style,
                                              où un socle mature améliorerait la cohérence
horizontal-craft/color.md                    → pas de design system, ou direction chromatique insuffisante
horizontal-craft/accessibility.md            → production interactive ou publiable ; contrôlée aussi par la porte qualité
horizontal-craft/animation-discipline.md     → animations, transitions, effets de défilement ou narration animée
horizontal-craft/form-validation.md          → formulaires, saisies, validation, soumission, inscription, checkout, réglages
horizontal-craft/laws-of-ux.md               → tarification, onboarding, dashboard, outil H5, parcours de conversion
                                              ou production à forte interactivité
horizontal-craft/icon-system.md              → toute icône UI / fonction / navigation / état, pictogramme, marque iconique
horizontal-craft/chinese-typography.md       → chinois abondant / confort de lecture chinoise (appliquer son
                                              Mandatory Runtime Baseline)
  → reference/title-and-breaking.md          → coupures de titres / couvertures / PPT / Xiaohongshu
  → reference/punctuation.md                 → longs textes chinois denses en ponctuation
  → reference/text-detail.md                 → corps / interligne / espacements / rythme des paragraphes
  → reference/fonts.md                       → choix des polices, mise en page de rapports formels
horizontal-craft/state-coverage.md           → interfaces produit / dashboard / formulaire / outil / H5 / data / prototype
horizontal-craft/data-integrity.md           → indicateurs, graphiques, tableaux, classements, pourcentages ou affirmations
horizontal-craft/link-and-proof.md           → liens, CTA, citations, logos clients, témoignages, affirmations à preuve
horizontal-craft/visual-explanation.md       → flowchart, schéma d'architecture/système, timeline, graphe de relations,
                                              diagramme de processus, visualisation comparative, cartes, modèles
                                              explorables, tout composant d'explication visuelle
horizontal-craft/technique-library.md        → un effet au-delà du CSS pur peut servir l'objectif (anim / 3D / dataviz)
```
Lire ne suffit pas — la règle doit vraiment changer la production. Ne pas revendiquer une porte appliquée si l'implémentation n'est pas réellement dans le HTML/CSS/JS.

### Avant livraison (bloquant)

```text
[ ] quality-gate.md exécutée comme liste bloquante (pas une référence passive)
[ ] les productions interactives ont :focus-visible ; avec animation, reduced-motion
[ ] ni faux justificatifs, ni emoji en icônes, ni liens morts, ni logique placeholder, ni supports manquants
```
Si une porte ne passe pas : corriger la production ou signaler explicitement le problème non résolu — jamais l'ignorer en silence.

### Chaque tour, pas seulement le premier (règle multi-tours)

Le flux ci-dessus et la liste « avant livraison » valent pour **chaque tour créant ou modifiant substantiellement une production** — pas seulement la première tâche du dialogue. Les tours suivants tendent à abandonner des étapes sous prétexte que « c'est déjà fait » (le plus souvent : porte qualité et gestion de versions). Détrompez-vous : **chaque livraison passe indépendamment la barre. La nouvelle tâche du tour 8 est une tâche neuve, pas une continuation.**

Cycle minimal de tout tour produisant (y compris les relances « change un peu XX » et les changements de scénario en cours de dialogue) :

1. Reconfirmer le scénario (il a pu changer avec la nouvelle demande — si oui, re-router).
2. Faire la modification.
3. Rejouer `quality-gate.md` sur la production modifiée. Seule exemption : édition purement texte/couleur d'un fichier jamais passé par le flux Design Skill (voir le skill version-management §0).
4. Passer à la gestion de versions.

Au moindre doute dans un tour ultérieur sur le contenu exact d'une règle : relire le fichier concerné, pas deviner de mémoire.

## Built-In Quality Defaults (défauts de qualité intégrés)

Ne pas ériger dégradés génériques / grilles de cartes / bento / cartes arrondies en style automatique — choisir la forme consciemment (voir `horizontal-craft/anti-ai-slop.md`). Quand dimensions/viewport/ratio d'export/cadre device comptent, utiliser `canvas-and-device.md`.

**Texte et images ensemble (scénarios qui s'y prêtent, seulement en construction complète) :** en construisant une page complète (pas au stade échantillon — l'échantillon se contente de placeholders, sans collecte d'images), les productions visuelles — landing, portfolio, page contenu/éditoriale — planifient par défaut la structure textes-images et réservent la place (image hero, illustrations, visuels d'œuvres, icônes), plutôt qu'un empilement de texte pur — l'alignement de texte pur est la paresse la plus fréquente. Sans images réelles : un **placeholder correct** — ratio/taille adaptés, style discret et plaisant (fond doux ou filet fin, pas un pavé gris criard), avec l'étiquette de ce qui doit s'y mettre (ex. « [visuel produit principal] »), pour que la page reste complète et belle avant remplacement. Puis guider l'utilisateur vers les images réelles (voir §Guiding). (Les productions purement fonctionnelles — outils/dashboards/formulaires — n'y sont pas tenues.)

## HTML Artifact Structure (structure des productions HTML)

Organiser le HTML généré pour l'édition ultérieure — des id de section / attributs data stables :

```html
<section id="hero" data-section="hero">      <!-- pages: hero/work/about/contact -->
<section class="slide" data-slide="cover">   <!-- decks -->
<section data-screen="dashboard">            <!-- prototypes: + data-state, data-component -->
```

- garder sections / slides / screens / components / states identifiables pour l'édition par sélection
- privilégier un HTML sémantique lisible ; ne pas enfouir le contenu dans des blocs opaques générés
- étiqueter les placeholders comme tels ; pas de `href="#"` mort dans un livrable publiable, sauf étiqueté

---

## Références et systèmes : contraintes dures

Le « quel fichier quand » est déjà fixé par la matrice des déclencheurs. Ici, seulement les contraintes « sinon on se trompe » :

- **Typographie chinoise** : sans décisions CSS concrètes sur pile de polices/corps/interligne/longueur de ligne/interlettrage/rythme des paragraphes/ponctuation/mélange chinois-latin-chiffres, `chinese-typography.md` n'est pas appliquée.
- **Gabarits** : des semences de structure, pas des pages à cloner. Ne lire que le SKILL.md du gabarit retenu ; ne regarder `pattern.html` qu'en cas de détail structurel manquant, et n'en prendre que le rythme de mise en page/relations de blocs/responsive/interactions — **jamais recopier DOM, classes, tokens, placeholders, styles**. Sans correspondance : artifact skill directement.
- **Marques publiques** (Apple/Stripe/Linear…) : emprunter les traits esthétiques pour un design original ; l'effet d'abord, un matériau sous droit utilisé vaut une phrase de rappel du risque, sans dégrader pour éviter, ni prétendre à une production officielle. **Systèmes open source** : composants officiels selon documentation et licence, sans confusion avec la marque privée de la société.
- **Bibliothèque de techniques** : `technique-library.md` est une référence, pas une cible de routage. CSS simple par défaut ; ne monter que si l'effet sert l'objectif ; toujours reduced-motion ; jamais pour la nouveauté.
- **Référence design system** : `design-system-reference.md` ne charge que la plus pertinente, jamais tout.
- **Priorité des références** : ce que donne l'utilisateur > design system > gabarit/patterns de scénario > connaissance générale > goût libre du modèle.

# 4. Livrer et conclure

## Web entry / version management (entrée web / gestion de versions)

Après validation de `quality-gate.md`, **si et seulement si le livrable contient un fichier d'entrée frontend** (`.html`/`.jsx`/`.tsx`/`.vue`), exécuter `skills/version-management/SKILL.md` (déclenché par le type de sortie, pas par le scénario). Il gère chemins de projet/ressources/git/cartes de version ; collé dans le dialogue ou déposé à la racine de l'espace de travail, **ce n'est pas** une livraison. Exports images/documents/PPTX/JSON/DESIGN.md/sans nouvelle entrée web : passer.

---

## Export Skill (compétence d'export)

Quand l'utilisateur demande export, téléchargement, empaquetage, livraison ou conversion : `export.md`. Cibles : HTML autonome, ZIP, image/capture, PDF, PPTX, JSON/métadonnées, spécification de design, paquet DESIGN.md. L'export doit préserver l'état courant de la production — pas de re-design silencieux à l'export.

---

## IP and Content Boundaries (propriété intellectuelle et frontières de contenu)

**L'effet d'abord ; ne pas compliquer ni dégrader par précaution de droits.** En particulier, **ne pas** substituer du médiocre pour éviter un droit — par exemple redessiner en SVG à la main des visuels qui appelaient de vraies images : cela ne fait que baisser la qualité et trahir l'objectif. La bonne voie : **le style s'emprunte librement** (extraire les traits esthétiques d'une marque/d'une œuvre — palette, ambiance, composition, typographie — pour un design original ; le style n'est pas protégé, c'est même encouragé) ; **quand du matériau réel sous droit est requis** (images précises, logos, captures d'œuvres), privilégier le placeholder correct + guider l'utilisateur vers des versions qu'il a le droit d'utiliser, plutôt que dégrader en bricolant.

Si la production utilise réellement du contenu potentiellement protégé (fourni par l'utilisateur, ou éléments de marque/images/polices introduits sur demande), **une phrase suffit pour inviter l'utilisateur à vérifier ses droits** — c'est un rappel, pas un refus d'agir, et la qualité du livrable n'en souffre pas. L'effet final reste l'objectif.

Seule ligne rouge : ne jamais forger de déclaration « production officielle de la société X » sans autorisation de l'utilisateur.

Ne pas élargir le périmètre sans accord (demander avant d'ajouter des blocs/pages non demandés) ; mais étoffer les pages demandées en une ossature complète et crédible est attendu (étoffer ≠ gonfler d'eau).

---

## Edit Handling (traitement des éditions)

**Édition par annotation de sélection** : la sélection est la cible principale ; privilégier l'édition locale à la réécriture, préserver les blocs non concernés ; en cas d'ambiguïté, l'édition locale la plus sûre ou une question. **Édition locale de paramètres** (couleur/espacement/arrondi/densité/corps/aperçu device) : sauf incidence sur l'intention de design/la structure du contenu/la direction visuelle, confier à l'outil local déterministe, sans mobiliser le skill modèle.
