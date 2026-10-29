---
name: guizang-ppt
description: Générer un PPT web à pagination horizontale façon « magazine électronique × encre électronique » (fichier HTML unique), avec fond WebGL fluides, titres serif + corps sans-serif, volets de chapitre, grands chiffres, grilles d'images et autres gabarits. À utiliser quand l'utilisateur veut produire un PPT web de partage / conférence / lancement, ou mentionne « PPT façon magazine », « horizontal swipe deck », « editorial magazine », « e-ink presentation ».
visibility: public
mode: template
carrier: deck
scenario: marketing
pattern_source: assets/template.html, assets/pattern-slides.html
source_priority: skill-first
triggers:
  - "ppt"
  - "deck"
  - "slides"
  - "presentation"
  - "magazine"
  - « 杂志 (magazine) »
  - « PPT façon magazine »
  - "horizontal swipe"
  - "horizontal swipe deck"
  - "editorial magazine"
  - "e-ink presentation"
  - « PPT web »
  - « conférence de lancement »
  - « PPT de partage »
od:
  default_for: deck
  upstream: "https://github.com/op7418/guizang-ppt-skill"
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: « Fais-moi un PPT façon magazine — sur "l'entreprise d'une personne : l'organisation repliée par l'IA", un partage de 25 minutes, audience : designers + entrepreneurs. Recommande-moi d'abord une orientation (Monocle / WIRED / Kinfolk / Domus / Lab) à choisir. »
---

# Magazine Web Ppt

## Ce que fait ce skill

Produire un PPT à pagination horizontale en **HTML monofichier**, au ton visuel :

- hybride **magazine électronique + encre électronique**
- **fond WebGL fluides / lignes de niveau / dispersion** (visible sur les pages hero)
- **titres serif (Noto Serif SC + Playfair Display) + corps sans-serif (Noto Sans SC + Inter) + métadonnées monospace (IBM Plex Mono)**
- **icônes linéaires Lucide** (pas d'emoji)
- **pagination horizontale** (clavier ← →, molette, glisser tactile, pastilles en bas, index ESC)
- **interpolation douce des thèmes** : en tournant vers une page hero, couleurs et shader transitionnent en douceur

L'esthétique de ce skill n'est ni « PPT corporate », ni « UI internet grand public » — c'est le magazine *Monocle* après qu'on lui a plaqué du code.

## Quand l'utiliser

**Scénarios adaptés** :
- partage en présentiel / discours internes au secteur / rencontres privées
- lancement de produit IA / demo day
- conférences à forte personnalité
- des slides web « tout en une fois, sans outil de pagination »

**Scénarios inadaptés** :
- gros tableaux de données, empilements de graphiques (prendre un PPT classique)
- supports de formation (densité d'information insuffisante)
- édition collaborative multi-auteurs (c'est du HTML statique)

## Workflow

### Étape 0 · Choisir l'orientation (Direction — premier geste obligatoire)

**Avant les 6 questions de clarification, faire d'abord choisir une des 5 orientations magazine.** Chaque orientation regroupe « thème / layouts recommandés / style chrome / nombre de slides conseillé » : l'orientation répond d'avance à la moitié des questions.

Ouvrir `references/styles.md`, **copier tout le passage** pour montrer à l'utilisateur les résumés en une ligne des 5 orientations, puis le laisser choisir :

```
1. Monocle Editorial · magazine international ✦ défaut
2. WIRED Tech · données + ingénierie
3. Kinfolk Slow · art de vivre / humanités
4. Domus Architectural · architecture / sens de l'espace
5. Lab / Reference · académique + manuel de savoir-faire
```

Si l'utilisateur dit « je ne sais pas, recommande » — **proposer Monocle Editorial par défaut**, le risque d'échec le plus faible. S'il mentionne « IA / benchmark / lancement technique » → WIRED ; « lecture / rencontres privées / cercle d'amis » → Kinfolk ; « design / architecture / portfolio » → Domus ; « recherche / académique / méthodologie » → Lab.

Après le choix, créer ou mettre à jour `projet.md` dans le répertoire projet, avec en première ligne orientation + thème + audience + durée (gabarit en fin de `styles.md`). **Ne jamais changer d'orientation en cours** — changer à mi-chemin = tout recommencer.

### Étape 1 · Clarification du besoin (**avant d'agir, obligatoire**)

**Si l'utilisateur a déjà fourni plan complet + images**, passer directement à l'étape 2.

**S'il n'a donné qu'un thème ou une idée vague**, aligner avec ces 6 questions avant d'écrire. Ne jamais écrire des slides au doigt mouillé — une structure mal posée coûte très cher à reprendre :

#### La liste des 6 questions

> La question 5 a déjà trouvé sa réponse à l'étape 0 (orientation → thème). Sur les 5 restantes, laisser la 5e en blanc.

| # | Question | Pourquoi la poser |
|---|------|-----------|
| 1 | **Qui est l'audience ? Quel cadre ?** (interne au secteur / publication commerciale / demo day / rencontre privée) | détermine ton et profondeur |
| 2 | **Quelle durée ?** | 15 min ≈ 10 pages, 30 min ≈ 20 pages, 45 min ≈ 25-30 pages (fourchettes par orientation dans `styles.md`) |
| 3 | **Y a-t-il des supports d'origine ?** (documents / données / ancien PPT / liens d'articles) | avec supports, partir des supports ; sans, l'aider à bâtir |
| 4 | **Y a-t-il des images ? Où ?** | voir « conventions images » ci-dessous |
| 5 | ~~**Quel thème de couleurs ?**~~ | ✓ déjà tranché par l'orientation à l'étape 0 |
| 6 | **Y a-t-il des contraintes dures ?** (inclure la donnée XX / ne jamais montrer YY) | éviter les reprises |

#### Aide au plan (si l'utilisateur n'en a pas)

Bâtir la ossature sur l'« arc narratif », puis remplir :

```
Crochet (Hook)       → 1 page   : un contraste / une question / un chiffre dur qui arrête
Mise en ton (Context) → 1-2 pages : le contexte / qui vous êtes / pourquoi ce sujet
Corps (Core)         → 3-5 pages : le cœur, en alternant Layouts 4/5/6/9/10
Bascule (Shift)      → 1 page   : briser l'attendu / introduire l'idée nouvelle
Chute (Takeaway)     → 1-2 pages : citation forte / question en suspens / appel à l'action
```

Arc narratif + plan de pagination + table de rythme des thèmes (voir `layouts.md`) : **les trois tableaux alignés**, puis étape 2.

Conserver le plan dans `projet.md` ou `plan-v1.md` pour les itérations.

#### Conventions images (à dire à l'utilisateur)

Avant d'agir, préciser :
- **emplacement** : sous `projet/XXX/ppt/images/` (au même niveau qu'`index.html`)
- **nommage** : `{n° de page}-{sémantique}.{ext}`, ex. `01-cover.jpg` / `03-figma.jpg` / `05-dashboard.png`
  - numéro de page complété par des zéros, pour le tri
  - sémantique en anglais, courte, précise, cohérente avec le contenu
- **spécifications conseillées** :
  - chaque image ≥ 1600 px de large (éviter le flou sur grand écran)
  - JPG pour photos/captures, PNG pour UI transparents/graphiques
  - poids total sous 10 Mo (fluidité de pagination)
- **comment remplacer** : garder **le même nom et écraser**, c'est le plus sûr (aucun chemin à changer dans le HTML) ; sinon, rechercher-remplacer globalement `images/ancien-nom`
- **pas d'images ?** : s'aligner avec l'utilisateur — on peut d'abord générer la structure avec des blocs de couleur, puis compléter ; mais prévenir que les pages mixtes 4/5/10 ne pourront pas être validées visuellement sans images

### Étape 2 · Copier le gabarit

Copier `assets/template.html` vers la cible (généralement `projet/XXX/ppt/index.html`), et créer au même niveau un dossier `images/`.

```bash
mkdir -p "projet/XXX/ppt/images"
cp "<SKILL_ROOT>/assets/template.html" "projet/XXX/ppt/index.html"
```

`template.html` est un fichier **complet et exécutable** — CSS, shaders WebGL, JS de pagination, CDN polices/icônes déjà préréglés ; seul `<main id="deck">` contient 3 slides d'exemple (couverture, volet de chapitre, page vide de remplissage).

#### 2.1 · Placeholders à remplacer (**souvent oubliés**)

Juste après la copie, remplacer les placeholders suivants, sinon l'onglet du navigateur affichera « [à renseigner] remplacer par le titre du PPT » :

| Emplacement | Origine | À remplacer par |
|------|------|--------|
| `<title>` | `[必填] 替换为 PPT 标题 · Deck Title` | le vrai titre du deck (ex. `Une nouvelle façon de travailler · Luke Wroblewski`) |

Après chaque copie de template.html, premier réflexe : grep « [必填] » pour confirmer que tout est remplacé.

#### 2.2 · Choisir le thème (5 préréglages · pas de personnalisation)

Ce skill **autorise uniquement le choix parmi 5 préréglages méticuleusement réglés** ; aucune valeur hex libre — une couleur fausse ruine l'image à la seconde ; protéger l'esthétique compte plus que la liberté.

| # | Thème | Adapté à |
|---|------|------|
| 1 | 🖋 Encre classique | universel / publication commerciale / le défaut quand on ne sait pas |
| 2 | 🌊 Indigo porcelaine | tech / recherche / données / conférences techniques |
| 3 | 🌿 Encre forêt | nature / durabilité / culture / documentaire |
| 4 | 🍂 Papier kraft | nostalgie / humanités / littérature / magazine indépendant |
| 5 | 🌙 Dune | art / design / création / galerie |

**Opération** :
1. Recommander un ensemble selon le contenu, ou demander directement à l'utilisateur
2. Ouvrir `references/themes.md`, repérer le bloc `:root` du thème
3. **Remplacer en bloc** dans `assets/template.html` (la copie) les lignes marquées du commentaire « couleur du thème » du `:root{` initial (`--ink` / `--ink-rgb` / `--paper` / `--paper-rgb` / `--paper-tint` / `--ink-tint`)
4. Tout le reste du CSS passe par des `var(--...)` : aucune autre modification

**Règles dures** :
- un seul thème par deck, pas de changement de couleur en route
- refuser poliment toute valeur hex donnée par l'utilisateur — montrer les 5 préréglages et faire choisir
- pas de mélange (ex. l'encre de l'Encre classique + le papier de la Dune) — rupture totale d'harmonie

### Étape 3 · Remplir le contenu

#### 3.0 · Pré-contrôle : chaque classe doit exister dans template.html (**le plus important**)

**C'est la source de tous les problèmes de génération.** Les squelettes de layouts.md utilisent beaucoup de classes (`h-hero` / `h-xl` / `stat-card` / `pipeline` / `grid-2-7-5`…) : si le `<style>` d'`assets/template.html` ne les définit pas, le navigateur retombe sur ses styles par défaut — grands titres en sans-serif, cartes de données écrasées, pipeline en une ligne, images empilées en bas.

**Avant d'écrire le moindre slide :**
1. **Read `assets/template.html`** (au moins jusqu'à la fin du bloc `<style>`)
2. **Contrôler avec la liste Pre-flight de layouts.md** : chaque classe à utiliser existe dans le `<style>`
3. Si une classe manque : **l'ajouter dans le `<style>` de template.html**, pas la réécrire en inline dans chaque slide
4. **template.html est la seule source des noms de classes** — n'en pas inventer ; pour du sur-mesure, `style="..."` en inline

Classes fréquemment oubliées (dont l'existence doit être confirmée d'abord) :
`h-hero` / `h-xl` / `h-sub` / `h-md` / `lead` / `kicker` / `meta-row` / `stat-card` / `stat-label` / `stat-nb` / `stat-unit` / `stat-note` / `pipeline-section` / `pipeline-label` / `pipeline` / `step` / `step-nb` / `step-title` / `step-desc` / `grid-2-7-5` / `grid-2-6-6` / `grid-2-8-4` / `grid-3-3` / `grid-6` / `grid-3` / `grid-4` / `frame` / `frame-img` / `img-cap` / `callout` / `callout-src` / `chrome` / `foot`

#### 3.0.5 · Planifier le rythme des thèmes (**aussi important que le pré-contrôle des classes**)

**Avant de choisir les mises en page**, lister la classe de thème de chaque page (`hero dark` / `hero light` / `light` / `dark`) et l'aligner dans un document ou un brouillon. Règles détaillées dans « planification du rythme des thèmes » en tête de `references/layouts.md`.

**Règles impératives** :

- chaque section doit porter `light` / `dark` / `hero light` / `hero dark` — jamais `hero` seul
- plus de 3 pages consécutives au même thème = fatigue visuelle, interdit
- au-delà de 8 pages : ≥1 `hero dark` + ≥1 `hero light`
- le deck ne peut pas ne contenir que des pages de contenu `light` : il faut des pages `dark` pour la respiration
- une page hero (couverture/volet/question/grande citation) toutes les 3-4 pages

**Auto-contrôle après génération** : `grep 'class="slide' index.html` pour lister les thèmes, validation humaine du rythme avant livraison.

#### 3.1 · Choisir la mise en page

**Ne jamais écrire un slide de zéro.** Ouvrir `references/layouts.md` : 10 squelettes prêts, chacun un bloc `<section>` complet à coller :

| Layout | Usage |
|---|---|
| 1. Couverture d'ouverture | la page 1 |
| 2. Volet de chapitre | ouverture de chaque acte |
| 3. Grands chiffres | lancer des données dures |
| 4. Texte-gauche image-droite (Quote + Image) | contraste d'identité / récit |
| 5. Grille d'images | comparaisons / preuves par captures |
| 6. Pipeline deux colonnes | flux de travail |
| 7. Conclusion en suspens / page-question | fin d'acte / clôture |
| 8. Grande citation (Big Quote) | phrase forte serif / takeaway |
| 9. Comparaison côte à côte (Avant / Après) | ancien mode vs nouveau |
| 10. Mixte texte-image (Lead Image + Side Text) | pages denses en texte et image |

Choisir le layout, coller, changer textes et chemins d'images. **Le pré-contrôle 3.0 d'abord, impérativement.**

#### 3.2 · Normes de ratios d'images

Toujours des **ratios standards**, jamais les ratios bizarres des images d'origine (ex. `2592/1798`) :

| Scénario | Ratio recommandé |
|------|---------|
| Image principale texte-gauche image-droite | 16:10 ou 4:3 + `max-height:56vh` |
| Grille d'images (comparaison) | **`height:26vh` fixe**, pas d'aspect-ratio |
| Petite image à gauche + texte à droite | 1:1 ou 3:2 |
| Visuel plein écran | 16:9 + `max-height:64vh` |
| Vignettes du mixte | 3:2 ou 3:4 |

**Jamais `align-self:end` sur les images** — elles glisseraient au fond de la cellule, masquées par la barre du navigateur. Utiliser le conteneur grid + `align-items:start` (préréglé dans le template) pour caler les images en haut ; si la colonne de gauche doit être calée en bas : flex column + `justify-content:space-between`.

Les détails de composants (typographie, couleurs, grille, icônes, callout, stat-card…) sont dans `references/components.md`.

### Étape 4 · Auto-contrôle avec la liste de contrôle

Après génération, ouvrir `references/checklist.md` et contrôler point par point. Elle condense **tous les pièges des itérations réelles** ; les problèmes P0 (emoji, images qui débordent, retours de titres, répartition des polices) doivent tous passer.

Points particulièrement sensibles :

1. **Les grands titres doivent être en serif** — si l'affichage est sans-serif, à 99 % le pré-contrôle 3.0 n'a pas été fait : la classe `h-hero` manque dans template.html
2. **Dans les grilles d'images, uniquement `height:Nvh`, jamais `aspect-ratio`** (débordement)
3. **Les images ne doivent pas s'empiler en bas de page** — pas d'`align-self:end` ; grid + `align-items:start` (voir 3.2)
4. **Uniquement des ratios standards** (16:10 / 4:3 / 3:2 / 1:1 / 16:9), ne pas copier les ratios bizarres des images d'origine
5. **Grands titres chinois ≤ 5 caractères + `nowrap`** (éviter un caractère par ligne)
6. **Lucide, pas d'emoji**
7. **Titres serif, corps sans-serif, métadonnées monospace**

### Étape 5 · Prévisualisation locale

Ouvrir simplement `index.html` dans le navigateur. Sous macOS :

```bash
open "projet/XXX/ppt/index.html"
```

Pas de serveur local nécessaire. Images en chemins relatifs `images/xxx.png`.

### Étape 6 · Itération

Ajuster selon les retours — le CSS du gabarit est très paramétré : 90 % des retouches se font en inline style (corps `font-size:Xvw` / hauteur `height:Yvh` / espacement `gap:Zvh`).

---

## Guide des ressources

```
magazine-web-ppt/
├── SKILL.md              ← vous êtes ici
├── assets/
│   ├── template.html     ← le gabarit complet exécutable (fichier semence)
│   └── pattern-slides.html ← un deck d'exemple de 9 pages (pour l'aperçu Examples)
└── references/
    ├── styles.md         ← les 5 orientations magazine (Monocle / WIRED / Kinfolk / Domus / Lab)
    ├── components.md     ← manuel des composants (typo, couleurs, grille, icônes, callout, stat, pipeline...)
    ├── layouts.md        ← 10 squelettes de pages (collables directement)
    ├── themes.md         ← 5 préréglages de thème (à choisir, pas de personnalisation)
    └── checklist.md      ← liste de contrôle qualité (niveaux P0/P1/P2/P3)
```

**Ordre de lecture conseillé** :
1. Lire d'abord `SKILL.md` (ce fichier) pour la vue d'ensemble
2. **À l'étape 0, lire `styles.md`** — chaque orientation regroupe thème + layouts recommandés + style chrome
3. Après l'étape 1, si l'orientation demande confirmation, lire `themes.md` pour les palettes
4. **Avant d'agir, Read le bloc `<style>` d'`assets/template.html`** — l'unique source des classes ; une classe manquante casse la page entière
5. Lire `layouts.md` pour choisir les mises en page (avec la liste Pre-flight et la planification du rythme en tête)
6. Pour les détails, consulter les composants dans `components.md`
7. Après génération, lire `checklist.md` pour l'auto-contrôle (la règle P0-0 impose le pré-contrôle)

## Principes de design cardinaux (philosophie)

> Ces principes viennent des 5 tours d'itération du PPT « l'entreprise d'une seule personne ». Enfreindre l'un d'eux fait s'effondrer la sensation visuelle.

1. **La retenue prime sur la démonstration** — le fond WebGL ne transparaît que sur les pages hero, presque invisible ailleurs
2. **La structure prime sur la décoration** — ni ombres, ni cartes flottantes, ni padding box : toute l'information repose sur **grands corps + contrastes typographiques + grille et blancs**
3. **La hiérarchie du contenu naît des corps et des polices** — serif max = titre principal, serif moyen = sous-titre, sans-serif grand = lead, sans-serif petit = corps, monospace = métadonnées
4. **L'image est citoyenne de première classe** — rogne en bas seulement, haut et côtés intacts ; la grille fige avec `height:Nvh`, jamais `aspect-ratio`
5. **Le rythme vient des pages hero** — alterner hero et non-hero, sinon l'œil se fatigue
6. **Terminologie stable** — Skills reste Skills, pas de traduction mi-chinoise mi-anglaise

## Références

Le ton visuel de ce skill s'inspire de :

- le partage de 歸藏 « l'entreprise d'une personne : l'organisation repliée par l'IA » (2026-04-22, 27 pages)
- la mise en page du magazine *Monocle*
- la démo du billet « Thin Harness, Fat Skills » de Garry Tan (YC)

À considérer comme ancres de style.
