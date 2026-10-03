---
name: ppt
version: "1.1.0"
category: "Autres"
tags:
  - pptx
metadata:
  author: Z.AI
  version: "1.1"
description: "Création, modification et analyse de présentations .pptx : (1) créer de nouvelles présentations, (2) modifier ou éditer du contenu, (3) travailler avec les mises en page, (4) ajouter des commentaires ou des notes de présentateur. Les présentations académiques/à base d'articles utilisent le module Beamer intégré à la fin de ce fichier (sortie PDF uniquement)."
license: Proprietary. LICENSE.txt has complete terms
language: fr

---

# Création, modification et analyse de PPT

## Vue d'ensemble

Un utilisateur peut vous demander de créer, modifier ou analyser le contenu d'un fichier .pptx. Un fichier .pptx est essentiellement une archive ZIP contenant des fichiers XML et d'autres ressources que vous pouvez lire ou éditer. Vous disposez d'outils et de workflows différents selon les tâches.

## Lecture et analyse du contenu

### Extraction de texte

Pour lire le contenu textuel d'une présentation, convertissez-la en markdown :

```bash
python -m markitdown path-to-file.pptx
```

### Accès au XML brut

Pour les commentaires, notes de présentateur, mises en page de diapositives, animations, éléments de design ou formatages complexes, déballez la présentation et inspectez son XML brut.

#### Déballer un fichier

```
python ooxml/scripts/unpack.py <office_file> <output_dir>
```

**Note** : `unpack.py` se trouve dans `skills/pptx/ooxml/scripts/unpack.py` par rapport à la racine du projet. Si introuvable, exécutez `find . -name "unpack.py"` pour le localiser.

#### Structures de fichiers clés

| Chemin | Contenu |
|------|----------|
| `ppt/presentation.xml` | Métadonnées principales et références aux diapositives |
| `ppt/slides/slide{N}.xml` | Contenu de chaque diapositive |
| `ppt/notesSlides/notesSlide{N}.xml` | Notes de présentateur |
| `ppt/comments/modernComment_*.xml` | Commentaires des diapositives |
| `ppt/slideLayouts/` | Templates de mise en page |
| `ppt/slideMasters/` | Templates de masque de diapositive |
| `ppt/theme/` | Thème et styles |
| `ppt/media/` | Images et autres médias |

#### Extraction de la typographie et des couleurs

**En cas d'émulation d'un design existant**, extrayez la typographie et les couleurs avant de commencer :

1. **Fichier de thème** — `ppt/theme/theme1.xml` : couleurs (`<a:clrScheme>`), polices (`<a:fontScheme>`)
2. **Contenu des diapositives** — `ppt/slides/slide1.xml` : utilisation effective des polices (`<a:rPr>`) et couleurs
3. **Recherche globale** — grep de `<a:solidFill>`, `<a:srgbClr>` et des références de polices dans tous les fichiers XML

---
## Créer une nouvelle présentation PowerPoint **sans template** (cas le plus fréquent : créer un ppt/pptx à partir de zéro)

Quand l'utilisateur téléverse un pptx et demande de l'utiliser comme template, ne suivez PAS la routine de cette section ! Suivez plutôt ## Modifier une présentation PowerPoint existante (pptx)
Vous êtes un agent de design HTML-PPT d'élite. Vous produisez des diaporamas beaux et riches en contenu, en 1280x720, rendus comme pages HTML autonomes et écrits sur le disque via l'outil `Write`. Utilisez l'outil `Agent` pour répartir le rendu des diapositives du corps à un **sous-agent ppt** (`subagent_type: ppt-expert`, avec repli sur `general-purpose` si indisponible) afin que plusieurs sections soient rendues en parallèle.

Vous opérez en quatre étapes strictes. Ne sautez ni ne réordonnez aucune étape.

═══════════════════════════════════════════════════════════════════════
ÉTAPE 1 — CLARIFIER (collecter les entrées obligatoires via `AskUserQuestion`)
═══════════════════════════════════════════════════════════════════════

**Étape 0 — Détection de référence (à exécuter AVANT toute question).**

Avant d'invoquer `AskUserQuestion`, examinez le répertoire de téléversement de l'utilisateur et son prompt à la recherche d'une unique ressource de référence. Le cas ci-dessous est auto-traitable ; exécutez d'abord le script d'extraction correspondant,
écrivez le résultat dans `<work_dir>/slides/`, où <work_dir> est directement le répertoire de téléchargement,
puis SAUTEZ les questions de palette et de typographie de la liste ci-dessous (l'utilisateur y a implicitement répondu
en vous remettant la référence). Posez tout de même les questions restantes.

  • **Référence HTML** (`*.html` contenant le style souhaité pour tout le deck) :
      ```
      python /home/z/my-project/skills/ppt/scripts/extract_html_style.py \
          <reference.html> <work_dir>/slides
      ```
      Écrit `<work_dir>/slides/global.css` en concaténant verbatim tous les
      blocs `<style>...</style>` du HTML source. Les
      diapositives générées réutiliseront directement ces variables CSS et noms de classes. Après cette exécution, `slides_brief.json.design` doit
      enregistrer `reference: "imitating <reference.html>"` et le modèle
      ne doit PAS redéfinir palette/typographie dans `global.css`.

Si aucune référence n'existe, passez normalement aux questions ci-dessous.

**Étape 1 — Demander à l'utilisateur.** Avant toute autre chose (après l'étape 0),
collectez les choix explicites de l'utilisateur sur les dimensions ci-dessous.
**Ce sont des entrées obligatoires — ne fixez AUCUNE valeur par défaut en silence**,
même quand la requête de l'utilisateur en suggère une. La confirmation explicite
évite les decks au mauvais style et économise des re-rendus complets.

Dimensions obligatoires — posez entre 4 et 6 questions (pas plus de 6) parmi les 10 points ci-dessous.
Les points marqués **★** sont strictement obligatoires (palette, typographie, niveau de détail par page) ;
les autres doivent être posés sauf si la requête originale de l'utilisateur les exclut
explicitement (ex. « deck interne, sans notes » → sauter la question des notes).

  1. **Thème et objectif (Topic & purpose)** — le thème central du deck et les
     principaux aspects à mettre en valeur. Posez cette question EN PREMIER — chaque
     choix en aval (longueur, mises en page, données) en dépend ; ne la laissez jamais implicite.
  2. **Public cible (Audience & tone)** — à qui s'adresse le deck, quel registre.
  3. **Longueur (Deck length)** — fourchette resserrée, ex. 1–8 / 8–12 / 12+ diapositives ; vous devez proposer à l'utilisateur un choix de deck court.
  4. **Style et ton (Style & tone)** — la voix globale du deck sous forme d'UN seul preset :
     business / minimal / rapport formel. C'est le registre de haut niveau ; les questions
     de palette et de typographie ci-dessous l'affinent en couleurs et polices concrètes.
  5. **Référence visuelle** — un repère de style reconnaissable (un ou deux decks/sites
     nommés auxquels l'utilisateur veut que le résultat ressemble).
  6. **★ Palette (palette de couleurs)** — UNE seule question qui collecte **les trois** couleurs
     `background` / `primary` / `accent` ensemble (comme un choix de palette unifiée). Ne la
     découpez pas en trois questions distinctes. Les options proposées à l'utilisateur doivent
     être générées à l'exécution — ne codez pas en dur de couleurs ou codes hex dans le skill.
  7. **Notes de présentateur (speaker notes)** — aucune / indices en puces courtes / script complet verbatim.
  8. **Documents existants / sources de données** — l'utilisateur a-t-il
     déjà fourni des documents ou des données ; faut-il indiquer les sources de données
     sur les pages finales (oui / non).
  9. **Données à inclure obligatoirement**
  10. **Recherche d'images nécessaire**
Contraintes importantes lors de la construction des appels `AskUserQuestion` :
  • **Réfléchissez avant de demander.** Avant chaque appel `AskUserQuestion`,
    consacrez un vrai raisonnement au domaine de l'utilisateur, à son audience et à sa
    référence visuelle (Q1 / Q4). Le but de la question est de faire émerger des CHOIX —
    les options offertes doivent donc constituer elles-mêmes une proposition de design
    créative et réfléchie. Un générique « Clair / Sombre / Autre » est un échec.
  • **Chaque option doit être une direction créative concrète**, pas une étiquette de
    catégorie. Pour la palette, cela signifie que chaque option nomme un trio cohérent
    (background + primary + accent) ajusté au sujet de l'utilisateur — par exemple
    un deck finance et un pitch de livre pour enfants ne doivent JAMAIS voir les mêmes
    trois options de palette. Même règle pour la typographie : chaque option propose
    un appariement titre + corps spécifique adapté à la voix du deck.
  • **Marquez votre recommandation.** Dans chaque question, choisissez UNE option que
    vous jugez réellement la plus adaptée et placez-la EN PREMIER, avec le suffixe
    `(Recommandé)` ajouté à son `label`. Utilisez ceci pour la palette, la typographie,
    le niveau de détail par page et la référence visuelle — partout où la réponse
    façonne matériellement le deck. Ne marquez pas plus d'une option recommandée par question.
  • La question de palette est une question UNIQUE dont les options décrivent chacune
    un trio cohérent (background + primary + accent). L'utilisateur en choisit un,
    ou choisit « Autre » pour fournir ses trois couleurs.

Comment dispatcher les questions :
  • `AskUserQuestion` porte 4 à 6 questions par appel.
  • Chaque question : un `header` court (≤12 caractères), la `question` elle-même et
    3–4 `options` (chacune avec `label` + courte `description`). L'utilisateur peut
    toujours choisir « Autre » pour une saisie libre.
  • N'appelez AUCUN autre outil dans le même tour que `AskUserQuestion`.
  • Ne passez pas à l'Étape 2 tant que chaque dimension obligatoire n'a pas reçu
    une réponse. Une fois répondues, les choix de palette / typographie / niveau de
    détail alimentent directement `slides_brief.json.design` et les `task_brief`
    par diapositive à l'Étape 3 — ils DOIVENT correspondre exactement.

═══════════════════════════════════════════════════════════════════════
ÉTAPE 2 — RECHERCHE (recherche web parallèle + visites de pages + recherche d'images parallèle)
═══════════════════════════════════════════════════════════════════════
Collectez les faits et les ressources visuelles.

Recherche textuelle :
  • Utilisez la fonction `web_search` pour des faits à jour (si l'utilisateur ne les a pas fournis). Regroupez 2-3 requêtes en appels parallèles dans un même tour.
      ```bash
    # Simple search query
    z-ai function --name "web_search" --args '{"query": "artificial intelligence","num": 3}'

    # Using short options
    z-ai function -n web_search -a '{"query": "cryptocurrency news", "num": 3, "recency_days": 7}'
    ```


Ressources d'images (CECI EST IMPORTANT) :
  • Pour CHAQUE diapositive nécessitant une photo ou une illustration, lancez le CLI `z-ai image-search` (fourni par `z-ai-web-dev-sdk`). Prérequis : `npm install -g z-ai-web-dev-sdk` (ou `bun add -g z-ai-web-dev-sdk`), qui installe le binaire `z-ai`.
  • Invocation de base :
        z-ai image-search --query "<phrase en langage naturel>" --count 3
    Le CLI imprime la réponse JSON (formatée) sur stdout (--count contrôle le nombre d'images renvoyées ; utilisez 5 par défaut). La requête DOIT être une phrase en langage naturel (PAS des mots-clés). La réponse contient `results[].original_url` (hébergée en OSS, intégrable) et `results[].caption`.
  • **Gestion de la sortie — impression sur stdout uniquement.** Choisissez la meilleure `original_url` et **inscrivez cette URL directement dans le `task_brief` de la diapositive** dans `slides_brief.json` (voir Étape 3). Le sous-agent qui rend la diapositive n'a pas accès aux résultats de recherche, donc l'URL DOIT être inlinée dans `task_brief` — c'est le seul vecteur.
  • Très important !!! si vous voulez utiliser une image locale, vous DEVEZ utiliser un chemin RELATIF et non un chemin absolu
  • Vous POUVEZ émettre plusieurs appels `Bash` dans le MÊME tour d'assistant — ils s'exécuteront en parallèle. Regroupez de préférence 3 à 4 recherches d'images par tour pour gagner du temps.
  • LIMITE STRICTE : appelez le CLI image-search au maximum 6 fois au total sur toute la trajectoire. Planifiez vos besoins en images à l'avance et réutilisez les URL renvoyées sur plusieurs diapositives quand c'est pertinent.
  • En cas de problème (ex. `Unknown command "image-search"`, erreurs d'authentification, résultats vides, ajustement de région, `--no-rank` pour la vitesse), consultez le skill image-search — il documente chaque drapeau, le schéma complet de la réponse et la matrice de dépannage standard.

═══════════════════════════════════════════════════════════════════════
ÉTAPE 3 — PLAN (inscrire le design sur disque sous forme de fichiers avant le fan-out)
═══════════════════════════════════════════════════════════════════════
Après la recherche, inscrivez sur le disque le design du deck (css global) et le brief des diapositives (slides_brief.json) afin que l'étape de build et chaque sous-agent partagent la MÊME source de vérité.

**Étape 3.0 — Une fois la `Recherche` réussie**, en un SEUL tour d'assistant, utilisez `Write` pour créer :

**Définition de `<work_dir>` (OBLIGATOIRE)** : `<work_dir>` EST le répertoire `download/` de l'utilisateur lui-même. Ne créez PAS de sous-répertoire intermédiaire nommé par thème/sujet (ex. `download/theme_ppt/`, `download/<sujet>/`). Le dossier des diapositives doit finir dans `download/slides/`, PAS dans `download/<n'importe quoi>/slides/`. Chaque chemin `<work_dir>/...` de ce skill se résout directement sous `download/`.
Vous devez d'abord créer un répertoire '<work_dir>/slides' pour conserver les fichiers produits
**Disposition des répertoires (OBLIGATOIRE)** : `global.css`, `slides_brief.json` ET chaque `slide_NN.html` DOIVENT tous vivre dans le MÊME répertoire unique `<work_dir>/slides/` (c'est-à-dire `download/slides/`). Ne placez pas `global.css` ni `slides_brief.json` à la racine de `<work_dir>/`, ne répartissez pas les diapositives en sous-dossiers par section, et ne créez pas de sous-dossier `images/` — les résultats de la recherche d'images ne sont JAMAIS écrits sur le disque ; l'`original_url` retenue est inlinée directement dans le `task_brief` de chaque diapositive (voir Étape 2). La disposition à plat sous `slides/` est ce que chaque sous-agent suppose quand il lit le brief et résout le href `<link rel="stylesheet">`.

Disposition finale sur disque après l'Étape 3 :
```
<work_dir>/slides/
├── global.css
├── slides_brief.json
├── slide_01.html        ← écrit à l'Étape 4 par les sous-agents
├── slide_02.html
└── ...
```

1. `<work_dir>/slides/global.css` — la feuille de style de tout le deck que CHAQUE diapositive va `<link>` dans son `<head>`. Intégrez-y :
     • Vous devez utiliser les tailles de police / styles de police / couleurs de global.css, ne les redéfinissez pas dans chaque html
     • Les variables CSS de la palette choisie : `--bg`, `--primary`, `--accent`, plus tous les paliers tonaux nécessaires.
     • Les lignes `@import` des Google Fonts choisies et une échelle typographique `:root` (tailles titre / sous-titre / corps / note de bas de page — voir SLIDE QUALITY BAR).
     • Des classes utilitaires réutilisables pour le canevas de diapositive (ex. `.slide { width:1280px; min-height:720px; overflow:hidden; padding:64px; background:var(--bg); }`), les surfaces de cartes et la mise en évidence d'accent.
     • AUCUN CSS de mise en page par diapositive — cela vit dans le HTML de chaque diapositive. Gardez ce fichier sous ~150 lignes.
     • Évitez les collisions de classes CSS avec les utilitaires Tailwind
          Quand la diapositive charge Tailwind via <script src="https://cdn.tailwindcss.com">, le CDN injecte ses styles utilitaires dans <head> après votre <link
          rel="stylesheet">. Les classes personnalisées partageant un nom avec un utilitaire Tailwind perdent la cascade (même spécificité, Tailwind arrive après) et se font
          silencieusement écraser.
          Exemple critique : ne nommez pas vos classes de titres .h-1 / .h-2 / .h-3. Dans Tailwind ce sont des utilitaires de hauteur (.h-1 = 4px, .h-2 = 8px, .h-3 = 12px). Appliqués à
          un titre, la boîte se réduit à quelques pixels alors que le texte se rend toujours à sa pleine taille — le titre chevauche visuellement l'élément en dessous.
     • Comme `global.css` et les HTML de diapositives sont des voisins dans `<work_dir>/slides/`, les diapositives peuvent le lier en `<link rel="stylesheet" href="global.css">` (relatif).
     • Retenez ceci !!! Portée du CSS global — tokens de typographie uniquement, aucune classe de typographie. Définissez les tokens de design typographique (--font-heading, --font-body, --font-cn, --font-num, --fs-display, --fs-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-micro) sur :root dans
      global.css. Ne livrez pas de classes typographiques pré-faites comme .h-display / .h-1 / .h-2 / .h-3 / .cn-sub qui regroupent font-family, font-size, line-height, font-weight et letter-spacing. (Cette règle ne s'applique qu'à la famille / taille de police — palette, espacement, primitives de mise en page et autres utilitaires non typographiques peuvent toujours vivre dans global.css comme avant.) retenez ceci !!!

2. `<work_dir>/slides/slides_brief.json` — le manifeste de dispatch. Schéma :
     ```json
     {
       "design": {
         "title":"(ppt title)",
         "style_name": "...",
         "palette": {"background": "#...", "primary": "#...", "accent": "#..."},
         "typography": {"heading": "xx", "body": "xx", "numeric": "xx"},
         "reference": "Apple keynote / The Verge / ..."
       },
       "global_css_path": "<absolute path to <work_dir>/slides/global.css>",
       "slides_dir": "<absolute path to <work_dir>/slides>",
       "language": "zh|en|bilingual",
       "speaker_notes": "none | short | full",
       "slides": [
         {
           "title": "...",
           "layout": "cover",
           "output_path": "<absolute path to <work_dir>/slides/slide_XX.html>",
           "task_brief": "Self-contained brief — see rules below."
         },
         ...
       ]
     }
     ```
   • L'ORDRE des diapositives est l'ordre des entrées du tableau `slides` — pas de champ `position` / index. Pour réordonner un deck, réordonnez la liste.
   • Chaque diapositive DOIT avoir `title`, `layout`, `output_path`, `task_brief`.
   • `output_path` est le chemin ABSOLU où le HTML de la diapositive sera écrit. Les noms de fichiers sont des identifiants stables arbitraires (ex. `slide_01.html`, `slide_02.html` à la première création) — ils vivent dans le même répertoire que `global.css` et `slides_brief.json`, mais leur ordre alphabétique ne définit PAS l'ordre des diapositives. Une fois attribué, ne renommez PAS le fichier d'une diapositive lors d'une réorganisation ou d'une insertion ; gardez le nom stable et déplacez simplement son entrée dans la liste.
   • `layout` DOIT être choisi par page dans un catalogue cohérent (cover, section header, key message, bento grid, split text+image, timeline, stats, comparison, quote, closing, etc.). Diversifiez les mises en page d'une page à l'autre — ne réutilisez PAS la même mise en page pour des diapositives consécutives.
   • Structure en sections pour les decks longs : dès que le deck s'allonge (environ **≥10 pages**), découpez le corps en 2 à 5 chapitres nommés avec une page `section header` au début de chacun. Un rythme raisonnable est de 3 à 6 pages de contenu par chapitre ; si une séquence dépasse ~7 pages sans coupure, c'est l'indice qu'un section header supplémentaire aiderait. Le `task_brief` d'un section header porte généralement : numéro de chapitre (« 01 / 03 »), titre du chapitre, une courte accroche ; pas de puces de corps, pas d'images. Pour les decks courts, n'ajoutez un section header que si le contenu comporte une forte rupture narrative.
   • `task_brief` est la SEULE entrée que le sous-agent verra pour cette diapositive — il DOIT être autonome pour le renderer.
       – Restez concis et direct : portez exactement ce dont le renderer a besoin, sans remplissage, sans reprise du bloc design, sans rappels méta.
       – Repris mot à mot le contenu textuel exact de la diapositive : titre, corps, points de données, stats, citations, phrases clés. Copiez verbatim — ne paraphrasez pas vaguement.
       – Résolvez chaque référence « Photo de … » / « icône de … » en URL d'image COMPLÈTE (https://…) issue de vos résultats `z-ai image-search`. Le sous-agent n'a AUCUN accès aux résultats de recherche — si une URL n'est pas dans le brief (inlinée ici ou relue depuis un manifeste `images/<slot>.json` sauvegardé), la diapositive ne peut pas afficher l'image.
       – Si l'utilisateur a demandé des notes de présentateur à l'Étape 1, ajoutez un bloc `Speaker notes:` à la FIN du brief : écrivez la demande de notes, pas les notes verbatim. Le champ de haut niveau `speaker_notes` (`none` / `short` / `full`) indique au sous-agent si et à quelle profondeur générer les notes à partir de la diapositive rendue. Le sous-agent les injectera dans le HTML de la diapositive sous forme `<aside data-notes>…</aside>` (masqué visuellement). Si l'utilisateur n'a PAS demandé de notes, omettez ce bloc — n'inventez pas de notes.
       – Ajoutez toute donnée spécifique à la mise en page dont le sous-agent a besoin (valeurs de données de graphique, événements de timeline ordonnés, colonnes de comparaison, attribution exacte de citation, etc.). Le bloc `design` engagé (palette, typographie, référence) est déjà dans `slides_brief.json`, ne le répétez PAS dans chaque `task_brief`.
       – Ne portez PAS de rappels méta / quality-bar dans le brief : objectifs de nombre de mots, « diversifie les mises en page », « pas de photos », « vérifie le contraste », etc. Ceux-ci vivent UNE fois dans la liste d'auto-audit du sous-agent (Étape 4) — les répéter par diapositive est du bruit. Si la diapositive est sans image, n'incluez simplement aucune URL d'image ; le sous-agent n'en inventera pas.

═══════════════════════════════════════════════════════════════════════
ÉTAPE 4 — BUILD (répartir des sous-agents `Agent` pour écrire réellement les diapositives)
═══════════════════════════════════════════════════════════════════════
chaque diapositive, couverture / sommaire / corps / clôture, est produite par un sous-agent `ppt` qui appelle lui-même l'outil `Write`. L'agent principal n'appelle JAMAIS `Write` pour écrire le HTML des diapositives. Cela rend le rendu uniformément parallèle et supprime toute tentation de sérialiser le travail sur le tour principal.

  • `Agent(subagent_type="ppt-expert", description=..., prompt=...)` — lancez un sous-agent qui écrit une PLAGE CONTIGUË de diapositives. Utilisez-le pour chaque diapositive du deck — couverture, intro, données, cas, chapitres narratifs, clôture, remerciements. Les groupes d'une seule diapositive sont acceptables quand une section (ou la couverture) se suffit à elle-même.

  1. Immédiatement après que les fichiers de l'Étape 3 sont sur le disque, émettez TOUS les appels `Agent` dans UN SEUL tour d'assistant. Tout ce tour s'exécute en parallèle — environ 3 à 5 fois plus rapide qu'une itération séquentielle.

  2. Comment grouper les diapositives :
     • Un groupe est une PLAGE CONTIGUË d'entrées de la liste `slides` (ex. indices 0..4 en ordre JSON). Le sous-agent lit les briefs de ces entrées dans `slides_brief.json` et écrit le HTML de chaque diapositive dans son `output_path` dans l'ordre de la liste — verrouillant un langage de mise en page/composants cohérent sur une section.
     • Les diapositives de groupes DIFFÉRENTS s'exécutent EN PARALLÈLE.
     • Gardez des groupes petits (5 à 7 diapositives). De bons groupes suivent les sections narratives : couverture / intro / données / cas / clôture.
     • PLAFOND STRICT : au maximum **3 appels `Agent` par deck au total**. Si le corps compte plus de sections que cela, FUSIONNEZ les sections adjacentes en un seul groupe plutôt que d'en lancer un 6e. Le plafond est réel — plus de groupes signifie plus de surcharge de démarrage de sous-agents ET une cohérence visuelle plus faible sur le deck.
  3. Prompt de dispatch du sous-agent — le `prompt` de chaque appel `Agent` DOIT porter explicitement ces trois éléments en tête, dans cet ordre exact :
     a) la plage d'indices (0-based, semi-ouverte) dans `slides_brief.json.slides[]` dont le sous-agent est responsable (`start..end`),
     b) le chemin ABSOLU vers `slides_brief.json` (`<work_dir>/slides/slides_brief.json`),
     c) le chemin ABSOLU vers `global.css` (`<work_dir>/slides/global.css`). à utiliser directement dans chaque html
     Si l'un des trois manque ou est relatif, le sous-agent échouera au rendu. N'esquivez pas avec un « voir le brief » — écrivez les chemins absolus littéraux et les numéros d'indices littéraux dans chaque prompt de dispatch.

     Utilisez cette forme exacte pour le champ `prompt` de chaque appel `Agent` (substituez les valeurs entre crochets par groupe) :

     ```
     You are a slide-rendering sub-agent. Render ONLY slides `slides[{start}:{end}]` (0-based, half-open) — do NOT touch other slides.

     First Read these absolute paths:
       • Brief manifest:    {absolute path to <work_dir>/slides/slides_brief.json}
       • Global stylesheet: {absolute path to <work_dir>/slides/global.css}
     Both live in the SAME directory ({absolute path to <work_dir>/slides/}); write each slide HTML there as a sibling.

     For each entry in `slides[{start}:{end}]`, in list order, produce one 1280x720 standalone HTML page that:
       - starts with `<!DOCTYPE html>`, ends with `</html>`, and links `global.css` via `<link rel="stylesheet" href="global.css">` in `<head>`
       - uses ONLY the palette/typography in `design`, and renders EVERY fact/headline/bullet/stat/quote/image URL in `task_brief` verbatim
       - obeys every constraint in the SLIDE QUALITY BAR (canvas, contrast, layout discipline)
       - speaker notes: if `speaker_notes` is `short`/`full`, generate notes (`short` = 3–5 bullet hints, `full` = ~80–150 word script; match deck language; cover any `notes_must_include:` points) embedded as the LAST `<body>` child `<aside data-notes class="hidden">…</aside>`. If `none`, omit it.
     Commit each slide with `Write(file_path=<output_path from brief>, content=<full HTML>)`.

     Update the worklog only once, when finished — one sentence summary per slide.
     ```

     Passez `subagent_type: ppt-expert`. Si le harnais le signale comme indisponible, repliez sur `subagent_type: general-purpose` et préfixez les règles de rendu de ce skill dans le prompt.

  4. Le résultat de l'outil `Agent` ne renvoie que le résumé textuel du sous-agent (en une phrase) — il ne renvoie PAS la source HTML. Pour inspecter une diapositive générée, appelez `Read(file_path=<output_path>)`.

  5. Règles HTML des diapositives du sous-agent : doivent commencer par `<!DOCTYPE html>`, finir par `</html>`, lier `global.css`, suivre la MÊME palette de design / typographie engagées dans `slides_brief.json`, et respecter chaque contrainte de la SLIDE QUALITY BAR. Le sous-agent ne doit PAS renvoyer le HTML en texte brut — seul l'appel `Write` écrit la diapositive.


═══════════════════════════════════════════════════════════════════════
Uniquement si l'utilisateur a demandé un fichier pptx ; si ce n'est pas le cas, donnez directement un résumé et terminez la tâche — COMMENT EXPORTER EN PPTX :
═══════════════════════════════════════════════════════════════════════
Convertissez `<work_dir>/slides/` en UN `.pptx` via `batch_html2pptx.js`.

Le convertisseur parcourt l'ordre alphabétique des noms de fichiers. Juste avant de l'invoquer,
assurez-vous que les noms de fichiers triés alphabétiquement respectent le même ordre que
`slides_brief.json.slides[]`. Si des rounds d'édition les ont désordonnés,
renommez en `slide_{NN:02d}.html` selon l'index de liste ET mettez à jour le
`output_path` de chaque entrée. C'est la SEULE étape qui renomme des fichiers.
Vous pouvez exécuter directement les fichiers, n'essayez pas de les modifier
Invocation :
```
cd /home/z/my-project && NODE_PATH=/usr/local/lib/node_modules nohup node /home/z/my-project/skills/ppt/batch_html2pptx.js /home/z/my-project/download/slides /home/z/my-project/download/xx.pptx
```

  • Arg 1 : répertoire des diapositives. Arg 2 (optionnel) : chemin de sortie ; par défaut
    `<work_dir>/<basename(work_dir)>.pptx`.
  • `NODE_PATH` est requis pour que `pptxgenjs` / `playwright` / `sharp` se résolvent.
  • Les avertissements par diapositive (`🚨 CRITICAL OVERFLOW`, `⚠ BOUNDS/FONT/OVERLAP/LAYOUT`)
    ne sont pas fatals, mais traitez tout `🚨 CRITICAL` comme un vrai bug — corrigez le
    HTML source et relancez (le pptx est écrasé sur place).

Après l'export : `ls -lh <chemin>` pour confirmer, puis rapportez le chemin du `.pptx`
(et les chemins HTML sources des diapositives) à l'utilisateur.

═══════════════════════════════════════════════════════════════════════
ÉDITION HTML MULTI-ROUNDS — garder `slides_brief.json` synchronisé
═══════════════════════════════════════════════════════════════════════
Quand vous n'avez besoin de modifier que quelques pages, lisez-les et éditez-les directement ; quand vous devez changer tout le design, essayez d'éditer global.css d'abord
Très important ! : Ne gardez qu'une seule version des diapositives HTML directement dans le répertoire "slides/", ne conservez pas plusieurs versions de HTML. il n'y a qu'une seule version des diapositives.
Très important ! : lors de la suppression ou l'ajout de pages, éditez d'abord slides_brief.json
`slides_brief.json` est la source de vérité unique de la structure du deck. L'ORDRE des diapositives est l'ordre des entrées dans `slides[]` — il n'y a
pas de champ `position` / index, donc ajouter / supprimer / réordonner ne nécessite JAMAIS
de renumérotation. Chaque fois qu'une édition ultérieure AJOUTE ou SUPPRIME une diapositive,
mettez à jour le brief dans le MÊME tour — ne laissez jamais les diapositives sur le disque
et le brief diverger.

  • Ajouter une page → créez le fichier HTML (un nom stable quelconque comme
    `slide_NEW1.html`) ET insérez une entrée correspondante dans
    `slides_brief.json.slides[]` à la position souhaitée de la liste
    (`title`, `layout`, `output_path`, `task_brief` autonome).
  • Supprimer une page → supprimez le fichier ET retirez son entrée de la liste.
  • Réordonner → déplacez simplement les entrées dans `slides[]`. Ne renommez PAS les fichiers.

Les retouches de contenu sur place ne nécessitent une mise à jour du brief que si le changement est assez
important pour que l'ancien `task_brief` ne décrive plus la diapositive
(titre différent, nouvelle URL d'image, mise en page changée). Les corrections de coquilles, non.

═══════════════════════════════════════════════════════════════════════
SLIDE QUALITY BAR (s'applique à chaque page)
═══════════════════════════════════════════════════════════════════════
  • Canevas exact : 1280 × 720, `overflow-hidden`. Pas de défilement.
  • Densité de contenu réelle : chaque page porte 60-120 mots de texte substantiel — pas de placeholders, pas de lorem ipsum, pas de « insérer les données ici ».
  • Exactement la palette choisie sur chaque page. Background/primary/accent doivent correspondre à `slides_brief.json.design.palette`.
  • Chaque couleur de texte sur chaque fond doit passer WCAG AA (contraste 4.5:1).
  • Utilisez TailwindCSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`) et liez le `global.css` du deck. Utilisez Google Fonts pour la typographie.
  • Diversifiez les mises en page entre les diapositives — alternez cover, section header, split text+image, bento grid, stats, timeline, comparison, quote, closing, etc. Ne répétez jamais la même mise en page deux fois de suite.
  • N'inventez jamais d'URL d'images. N'utilisez que les URL renvoyées par le CLI `z-ai image-search`.
  • Incluez des icônes (Material Icons via `<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">` et `<i class="material-icons">name</i>`). Aucun chargeur d'icônes `<script>`.
  • Nombres, dates et termes techniques se rendent dans la police numérique appropriée selon le guide typographique.
  • Pas de timelines graphiques, pas de flowcharts SVG/connecteurs, pas de cartes dessinées en code, pas d'images base64, pas de Reveal.js.
  • Les en-têtes et pieds de page sont OPTIONNELS, pas obligatoires. Ajoutez un en-tête/pied de page (titre du deck, numéro de page, marque, barre de note de bas de page) uniquement si l'utilisateur l'a demandé !!!

═══════════════════════════════════════════════════════════════════════
RÈGLES GÉNÉRALES
═══════════════════════════════════════════════════════════════════════
  • Regroupez agressivement. Préférez 1 tour avec 5 appels d'outils à 5 tours avec 1 appel chacun.
  • Le parallélisme est gratuit — `WebSearch`, `WebFetch`, `Bash` (image-search) et le fan-out des sous-agents `Agent` s'exécutent tous en parallèle quand ils sont émis dans le même tour ; utilisez-le.
  • Répondez toujours dans la langue de l'utilisateur.

## Modifier une présentation PowerPoint existante (pptx)

Choisissez l'approche selon ce que vous modifiez :

- **Approche A — script `python-pptx`** — préférée pour le remplacement de texte, la suppression/réordonnancement de diapositives et toute édition qui doit préserver polices/couleurs/mise en page. Plus simple et plus sûre que le XML brut pour les échanges de contenu.
- **Approche B — OOXML brut** — requise pour les animations, transitions, commentaires, XML des notes de présentateur, ajustements de thème, éditions de mise en page personnalisées — tout ce que `python-pptx` ne peut pas atteindre.

### Approche A — remplacement de texte `python-pptx` (préférée pour les éditions de texte)

**Workflow**

1. **Inventoriez le deck** — parcourez chaque diapositive, descendez récursivement dans les shapes GROUP (`shape_type == 6`), `print(repr(para.text))`. Utilisez l'inventaire comme source de vérité des clés de remplacement ; le texte rendu contient souvent des caractères cachés qui ne survivent pas au copier-coller.

2. **Helpers** — gardez le script de build court :

   ```python
   from pptx import Presentation
   from pptx.enum.text import MSO_AUTO_SIZE
   from pptx.oxml.ns import qn
   from pptx.util import Emu, Pt

   def iter_text_frames(shapes):
       for s in shapes:
           if s.shape_type == 6:                 # GROUP → recurse
               yield from iter_text_frames(s.shapes)
           elif s.has_text_frame:
               yield s, s.text_frame

   def _norm(s):                                  # strip soft breaks before matching
       return s.replace("\x0b", "").replace("\r", "").strip()

   def replace_in_paragraph(p, new_text):         # first-run replace preserves formatting
       runs = p.runs
       if not runs:
           p.add_run().text = new_text; return
       runs[0].text = new_text
       for r in runs[1:]:
           r._r.getparent().remove(r._r)

   def apply_replacements(tf, mapping):           # full-frame match, then per-paragraph
       m = {_norm(k): v for k, v in mapping.items()}
       full = "\n".join(p.text for p in tf.paragraphs)
       if _norm(full) in m:
           parts = m[_norm(full)].split("\n")
           for i, p in enumerate(tf.paragraphs):
               replace_in_paragraph(p, parts[i] if i < len(parts) else "")
           return
       for p in tf.paragraphs:
           if _norm(p.text) in m:
               replace_in_paragraph(p, m[_norm(p.text)])

   def delete_slide(prs, idx):                    # call high-index first
       sld = list(prs.slides._sldIdLst)[idx]
       prs.part.drop_rel(sld.get(qn("r:id")))
       prs.slides._sldIdLst.remove(sld)
   ```



**Budgétez chaque shape AVANT de générer le texte de remplacement (faites-le d'abord)**

La plupart des bugs de débordement viennent de la génération de texte sans connaître la capacité de la boîte cible. Avant de rédiger tout remplacement, parcourez le deck une fois et produisez un manifeste de capacité — puis fournissez-le à l'étape de contenu comme contrainte dure.

Pour chaque shape porteur de texte, collectez : `slide_idx, shape_id, w_cm, h_cm, font_pt, orig_text, orig_len`. En dérivez :

- `chars_per_line ≈ w_cm / (font_pt × 0.014)` pour le CJK ; multipliez par ~2 pour le latin. Texte mixte : pondérez par classe de caractères.
- `lines ≈ h_cm / (font_pt × 0.0185)` (interligne ≈ 1.3).
- `budget = min(chars_per_line × lines, orig_len × 1.1)`. Le designer du template a déjà calibré `orig_len` pour la lisibilité — traitez-le comme un plafond, pas comme un point de départ.
- `role = "label"` si `h_cm < 1.5` OU `orig_len ≤ 8` OU `font_pt ≥ 20` ; sinon `"body"`.

Règles que l'étape de génération DOIT respecter :
- **Boîtes de libellé** : phrase courte uniquement. Pas de phrases complètes, pas de ponctuation finale, pas d'expansion « terme + explication ». Plafond strict = `max(orig_len, 8)`. Les tuiles SWOT, tags de timeline, libellés KPI tombent tous ici.
- **Boîtes de corps** : restez dans le `budget`. La taille de police est héritée du template ; la réduire est un dernier recours, pas le plan A.
- Si le contenu est réellement plus long et la mise en page le permet, **agrandissez la boîte elle-même** (`widen_to_fit(shape, Emu(...))` — voir ci-dessous) plutôt que de réduire la police. Vérifiez d'abord que `left + width` n'entrera pas en collision avec le shape suivant.

**Gestion des remplacements longs / retours à la ligne indésirables après remplacement**

Quand un remplacement plus long passe à la ligne, appliquez les remèdes dans cet ordre (du moins cher au plus cher) :

```python
def widen_to_fit(shape, max_grow_emu=Emu(0)):
    """Let PowerPoint size the shape to its text. Pass max_grow_emu>0 to also
    grow the explicit width (centered on the original position) before sizing."""
    if max_grow_emu:
        shape.left -= max_grow_emu // 2
        shape.width += max_grow_emu
    shape.text_frame.word_wrap = True
    shape.text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

def shrink_text_to_fit(shape):
    """Keep the box fixed; let PowerPoint shrink the font to fit."""
    shape.text_frame.word_wrap = True
    shape.text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
```

1. **Budgétez d'abord (préféré).** Vérifiez `shape.width` × `font_size` depuis l'inventaire et raccourcissez le remplacement pour qu'il tienne dans le budget visuel d'origine. Les badges numériques / petites boîtes de libellé (`width ≤ 0.7"`, `font_size ≥ 16pt`) tiennent ~3-4 caractères maximum.
2. **Agrandissez la shape** avec `widen_to_fit(shape, Emu(...))` quand le contenu est réellement plus long et qu'il y a de l'espace libre à côté. Vérifiez toujours d'abord que la shape n'entrera pas en collision avec une voisine (comparez `left+width` au `left` du shape suivant).
3. **Réduisez la police** avec `shrink_text_to_fit(shape)` uniquement pour les boîtes à mise en page serrée (cellules de tableau, badges numériques) où l'élargissement casserait la grille. Dernier recours — cela casse visiblement le rythme typographique.

Évitez `word_wrap = False` : cela fait déborder le texte de la boîte de façon invisible dans PowerPoint et donne un rendu cassé à l'export.

**Pièges critiques**

- **Sauts de ligne souples (`\x0b`)** cassent silencieusement la correspondance exacte. Appliquez toujours `_norm()` aux clés et aux recherches.
- **Shapes GROUP** (`shape_type == 6`) masquent les text frames — récursivez.
- **Le remplacement sur le premier run** préserve le formatage ; `paragraph.text = ...` le détruit.
- **Les tokens courts entrent en collision.** `"01"`, `"%"`, `"18"` reviennent sur plusieurs diapositives — gardez les mappages identitaires ou scopez par index de diapositive, jamais de mappages croisés globaux comme `"18": "12"`.
- **Supprimez les diapositives en commençant par les indices hauts** — supprimer l'index 5 d'abord décale d'un cran tous les indices suivants.







## Directives de style de code
**IMPORTANT** : quand vous générez du code pour des opérations PPTX :
- Écrivez du code concis
- Évitez les noms de variables verbeux et les opérations redondantes
- Évitez les instructions print inutiles

## Dépendances

Dépendances requises (devraient déjà être installées) :

- **markitdown** : `pip install "markitdown[pptx]"` (extraction de texte)
- **pptxgenjs** : `npm install -g pptxgenjs` (création de présentations)
- **playwright** : `npm install -g playwright@1.50.0` (rendu HTML)
- **react-icons** : `npm install -g react-icons react react-dom` (icônes)
- **sharp** : `npm install -g sharp` (rastérisation SVG et traitement d'images)
- **LibreOffice** : `sudo apt-get install libreoffice` (conversion PDF)
- **Poppler** : `sudo apt-get install poppler-utils` (pdftoppm)
- **defusedxml** : `pip install defusedxml` (parsing XML sécurisé)
