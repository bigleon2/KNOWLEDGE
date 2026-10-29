---
name: ascii-cosmos
description: Generate a single-file product landing page with a layered ASCII cosmos hero (rotating ASCII planet, drifting irregular asteroids, comet trails, nebula gas clouds — each in its own harmonious color) plus full marketing sections (about / features grid / showcase / spec / pricing / CTA / footer). Takes a natural-language description of one product (any kind — a note app, a coffee subscription, a CLI tool, an indie hardware, a hosting service…) and outputs ONE working .html file with deep-space dark or warm-letterpress theme. Runs in BOTH Claude Code (writes to ~/Desktop) and GLM / online chat (outputs HTML inline). Trigger phrases : « fais une landing produit façon cosmos », « génère un site produit ASCII », « ascii-cosmos-gen ... », « fais une landing logiciel indépendant / matériel indépendant », ou quand l'utilisateur glisse ce dossier de skill dans le chat en demandant une landing produit atmosphérique.
visibility: public
mode: template
carrier: web-page
scenario: marketing-landing
pattern_source: reference.html
source_priority: skill-first
triggers:
  - « fais une landing produit façon cosmos »
  - « génère un site produit ASCII »
  - « fais une landing logiciel indépendant »
  - « fais une landing matériel indépendant »
  - « landing ascii »
  - « hero ascii »
legacy_gen: true
---

# ascii-cosmos — générateur de landing produit à l'univers ASCII

## À quoi ressemble le résultat

Un site produit HTML monofichier, dont le hero est un cosmos ASCII animé en couches :

- **nuages de nébuleuse** (violet, points diffus et doux)
- **étoiles scintillantes** (blanc froid, avec décor ★ ✦)
- **planète ASCII en rotation** (cyan, avec 3 anneaux d'orbites satellites)
- **astéroïdes irréguliers en flottaison** (or ambré, 6 formes ASCII multi-lignes avec cratères, rotation + dérive lente)
- **traînées de comète** (rose, frôlant l'écran)

Puis les blocs marketing classiques : à propos / grille de 6 cartes fonctionnalités / 2 blocs d'aperçu d'interface / spécifications techniques / 3 paliers d'abonnement / CTA / pied de page. Tous les champs en valeur possèdent l'animation de brouillage-décodage des caractères au survol (classe `.pt`).

Adapté à : logiciels indépendants, outils de notes/écriture, IA locale-first, CLI, matériel indépendant, services par abonnement, SaaS, livres numériques, podcasts — tout produit « calme / retenu / avec une touche artisanale ».

## Quand se déclencher

L'utilisateur dit :
- « fais une landing produit façon cosmos »
- « fais un site produit façon ASCII »
- « génère une landing comme MoSI — mon produit est ... »
- « ascii-cosmos-gen ... »
- glisse le dossier de ce skill dans le chat et décrit un produit

Il fournit :
- **nom du produit + positionnement en une phrase** (obligatoire)
- **arguments clés / liste de fonctionnalités** (recommandé — pour les 6 cartes)
- **paliers de prix** (optionnel — sinon en inventer 3 : gratuit / pro / équipe)
- **style** (optionnel — cyan cosmos / parchemin chaud / violet cyber / vert terminal…, reprendre un nom de préréglage de `styles.md` ou décrire librement. À défaut, le cyan cosmos par défaut)

Si l'utilisateur **ne donne qu'un nom et une phrase** : imaginer soi-même autour du produit les 6 fonctionnalités, les 3 paliers de prix et les spécifications. Ton retenu, artisanal, sans enthousiasme marketing forcé.

## Deux modes d'exécution

### Mode A · Claude Code / local (avec système de fichiers)
- Sortie : `~/Desktop/{slug}.html` (**monofichier**, toutes les images en URL unsplash ou liens fournis)
- slug = nom anglais du produit, minuscules et tirets
- rapport en une phrase : chemin + style + nombre de cartes

### Mode B · GLM / dialogue en ligne (sans système de fichiers)
- Sortir le HTML complet dans un bloc ` ```html `
- images toutes en `https://images.unsplash.com/photo-XXX?...` ou `https://picsum.photos/seed/{slug}-NN/W/H`
- ne pas tenter d'accéder aux fichiers locaux, pas de ligne de commande
- une ligne finale : enregistrer en .html et double-cliquer

Décision : si vous **ne pouvez pas Read les images locales** ou si le répertoire de travail n'est pas le home de l'utilisateur → mode B.

## Étapes de travail

### 1. Lire le gabarit
Lire `template.html` dans le répertoire du skill. C'est le squelette complet, avec :
- tout le CSS (thème cosmos + 5 couches ASCII + cartes / prix / specs / police tramée du hero…)
- tout le JS (rendu ASCII 5 couches, orbites de la zone info, brouillage de caractères, filtrage par tags, défilement doux, horloge temps réel)
- 12 marqueurs de commentaire `<!-- SWAP-N -->` aux emplacements à remplacer

**Ne pas toucher au JS / CSS** (hors variables de thème et polices, ajustables selon styles).

### 2. Lire les préréglages de style
Voir `styles.md` : 5 préréglages. Si la description de l'utilisateur correspond à un nom, remplacer `:root` par les variables CSS de ce préréglage. Sinon, concevoir soi-même 6 variables (`--bg / --fg / --dim / --accent / --accent2 / --accent3 / --line / --paper`) + les couleurs des 5 couches ASCII (`#ascii-nebula / -stars / -planet / -asteroids / -comets`) selon la description.

> Règle de fer des couleurs : les 5 couches ASCII doivent être **harmonieuses entre elles + toutes lisibles sur le fond**. Fond sombre → couleurs saturées lumineuses ; fond clair → couleurs de luminosité moyenne-basse, avec du poids.

### 3. Analyser l'entrée utilisateur

Extraire :
- **PRODUCT_EN** — nom de logo anglais, lettres ASCII en capitales (pour le grand titre ASCII du hero)
- **PRODUCT_CN** — 1-2 caractères chinois (grand sous-titre du hero, rendu en police tramée)
- **TAGLINE** — sous-devise en une phrase (30-50 caractères)
- **VERSION / TYPE / PLATFORM** — 3 étiquettes meta
- **ABOUT_PARAGRAPH** — paragraphe à propos de 80-150 caractères, avec 3-5 expressions mises en valeur par `<span class="pt">`
- **3 HIGHLIGHT** — 3 cellules (titre + description en une phrase)
- **6 FEATURES** — 6 cartes : URL d'image + overlay ASCII (petit motif 5-6 lignes) + titre + sous-titre + 1-2 tags + catégorie (ai/write/graph/sync au choix ou libre)
- **2 SHOWCASE** — 2 présentations d'interface (URL de capture + déco mini-ascii + titre avec emphase `<em>` + 2 paragraphes de 60-100 caractères)
- **10 SPEC ROWS** — 10 lignes clé-valeur (version / plateforme / moteur / format de données / protocole de synchronisation…)
- **3 PRICING** — 3 paliers (nom / chiffre du prix / unité / description / 5-6 caractéristiques / libellé du bouton CTA). **Ajouter la classe `featured` au palier du milieu**
- **CTA_BIG** — CTA en grands corps (avec emphase `<em>`) + sous-texte + 3 boutons + 6-7 étiquettes de plateforme

### 4. Remplacer les 12 SWAP

| SWAP | Emplacement | Contenu |
|---|---|---|
| 1 | `<title>` | `{PRODUCT_CN}{PRODUCT_EN} — {TAGLINE}` |
| 2 | logo du header + nav 5 items | texte du logo + ancres de navigation (défaut : fonctionnalités / interface / specs / abonnement / à propos) |
| 3 | titre ASCII du hero | ASCII de `PRODUCT_EN` façon ANSI Shadow (style https://patorjk.com/software/taag, 5 lignes de haut) |
| 4 | grands caractères chinois du hero + tagline + 3 meta | `PRODUCT_CN` + `TAGLINE` + 3 spans meta |
| 5 | paragraphe d'intro + 3 cellules | `ABOUT_PARAGRAPH` (avec emphases `<span class="pt">`) + 3 `<div class="cell">` |
| 6 | 6 cartes features | chacune : `data-cat` + `<img src>` + overlay ASCII + titre + small + tags |
| 7 | 4 tags de filtre | chips de catégorie (all + vos 3-4 catégories, appariées aux data-cat des cartes) |
| 8 | 2 blocs showcase | chacun : capture + mini-ascii + h3 (avec em) + 2 p (avec emphase pt) |
| 9 | table de specs 10 lignes | chaque ligne : champ `<b>` + valeur `<span class="pt">` |
| 10 | 3 paliers pricing | name / num / desc / ul li / btn |
| 11 | CTA de la zone info | grands caractères info-big (avec em) + sous-texte hero-sub + 3 boutons + platforms |
| 12 | footer | copyright + une ligne de signature |

**À conserver impérativement** (ne pas toucher) :
- tous les blocs `<script>` (rendu ASCII 5 couches / orbites de la zone info / scramble / filtrage de tags / défilement doux / horloge)
- le mécanisme de brouillage de la classe `.pt` (parsemés à la main dans les textes : `<span class="pt" data-text="...">...</span>`)
- les nœuds `<pre id="ascii-...">` des 5 couches ascii
- le nœud `<pre id="info-ascii">`
- les data-cat des 6 cartes et la logique de filtrage
- le style du palier featured

### 5. Écrire le grand titre ASCII (SWAP-3)

Un ASCII 5 lignes en police ANSI Shadow / ANSI Regular. Chaque lettre avec les caractères de trait ╗╔═║║║╝╚═╝. Exemple pour INKWEAVE :
```
██╗███╗   ██╗██╗  ██╗██╗    ██╗███████╗ █████╗ ██╗   ██╗███████╗
██║████╗  ██║██║ ██╔╝██║    ██║██╔════╝██╔══██╗██║   ██║██╔════╝
██║██╔██╗ ██║█████╔╝ ██║ █╗ ██║█████╗  ███████║██║   ██║█████╗
██║██║╚██╗██║██╔═██╗ ██║███╗██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝
██║██║ ╚██╗██║██║  ██╗╚███╔███╔╝███████╗██║  ██║ ╚████╔╝ ███████╗
╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝
```

**Si le nom anglais dépasse 8 lettres** → raccourcir à 8 lettres ou moins (ex. `INTERSTELLAR` → `STELLAR`), ou utiliser une police ANSI plus étroite (`▌▐█` plus fins).

**En cas de doute sur le gabarit de lettres** → fournir au moins un ASCII 5 lignes présentable, ne jamais laisser vide.

### 6. Écrire les overlays ASCII des cartes (dans SWAP-6)

Chaque carte reçoit en bas à droite un petit décor ASCII de 4-5 lignes, en rapport avec sa fonction. Exemples :
- « complétion intelligente » → `╭─────╮ │ ... │ ╰──→──╯`
- « graphe de connaissances » → `●─●─● │\ │/│ ●─●`
- « recherche » → `┌─────┐ │ ⌕ trouvé │ │  3 occurrences │ └─────┘`
- « synchronisation » → `▣ ⇄ ▢ ╲ ╱ ⇅ ╱ ╲ ▤ ⇄ ▥`
- « frise chronologique » → `←─◆─◆─◆─→ ░░▒▒▓▓██`

Pas plus de 5 lignes, pas plus de 14 caractères de large.

### 7. Parsemer les emphases `<span class="pt" data-text="...">`

Dans le gabarit, toutes les expressions à « brouiller puis décoder au survol » :
```html
<span class="pt" data-text="texte original">texte original</span>
```
- 3-5 occurrences dans le paragraphe d'intro
- 1-2 par paragraphe des showcase
- la valeur de chaque ligne de spec enveloppée dans `<span class="pt">`
- le texte des boutons pricing également en `pt`
- les mots colorés dans les titres via `<span class="em">...</span>` (pas `pt`)

### 8. Variantes de style (optionnel)
Si l'utilisateur précise un style, ajuster selon `styles.md` :
- les 8 variables de `:root`
- le dégradé de fond de `.hero`
- les couleurs des 5 `#ascii-{layer}`
- les filtres d'images (sombre : `hue-rotate(200deg) brightness(.7)` ; chaud : `sepia(.3) saturate(.85)`)

> **Sans style précisé** : choisir automatiquement les couleurs selon les « mots de tempérament » du produit — voir « correspondance tempérament → couleurs » ci-dessous.

### 8.5 Remplacer le motif de scène ASCII (recommandé !)

Le hero du gabarit est par défaut un cosmos (planète + astéroïdes + comètes + nébuleuse). **Ce motif doit suivre le tempérament du produit** — un abonnement café n'a pas à voir flotter des astéroïdes, une app de balade en forêt n'a pas à avoir de comètes.

La modification ne touche **qu'un seul objet** : repérer le marqueur `// SWAP-13 · ASCII 场景资产` dans le `<script>` et remplacer entièrement le `SCENE = { ... }`. Tout le reste du JS reste intact.

Les 11 clés de `SCENE` et leurs rôles :

| Clé | Défaut (cosmos) | Rôle / responsabilité visuelle |
|---|---|---|
| `floaters` | 6 formes ASCII irrégulières d'astéroïdes (tableaux multi-lignes) | les « corps principaux » flottant et tournant à l'écran |
| `centerShade` | `" .,:;-~+*=%#@█"` | le dégradé d'ombrage de la sphère centrale en rotation (14 caractères, sombre→clair) |
| `diffuseChars` | `"·∙∶⋮⋯░▒"` | le dégradé de densité de la « nappe gazeuse » diffuse (pâle→dense) |
| `sparkRare` | `"★"` | point lumineux rare (4 %) |
| `sparkBright` | `"✦"` | point lumineux fréquent (15 %) |
| `sparkDim` | `".∙"` | points ordinaires, discrets |
| `streakHead` | `"☄"` | la « tête » de l'objet volant (la case la plus brillante) |
| `streakTailNear/Mid/Far/End` | `"*","∙","·","."` | la traînée, 4 segments s'estompant du proche au lointain |
| `centerSats` | `"◉◎○"` | les 3 « satellites » autour de la sphère centrale, de l'intérieur vers l'extérieur |
| `orbitDots` | `".∙•"` | les points des 3 anneaux d'orbite, de l'intérieur vers l'extérieur |

#### Bibliothèque de motifs (selon le type de produit)

| Type de produit | floaters | centerShade | diffuseChars | sparks | streakHead/tail | centerSats | Histoire visuelle |
|---|---|---|---|---|---|---|---|
| **café / thé / boissons** | formes grains de café / feuilles de thé | `" .'-=+oO0@#"` | `"·~,'\""` (vapeur) | `★ ✧ . ∙` | `"☕"` en tête + `"*∙·."` | `"●◐○"` (trois torréfactions) | une tasse + grains flottants + vapeur + un grain qui passe |
| **forêt / nature / plein air** | formes feuilles / pommes de pin | `" .,;:!|tT#"` (anneaux de croissance) | `"~^,'\""` (brume) | `"⁂"` lucioles + `"·"` rosée | `"𓅯"` oiseau + `"~~~~"` trajectoire | `"❀✿✾"` (fleurs) | un arbre + feuilles qui tombent + brume + lucioles + un oiseau qui passe |
| **musique / podcast / audio** | notes / fragments de disque | `" .─=≡▪▫■□"` | `"·∶⋮⁞"` (bruit) | `"♪♫"` + `"·"` | `"♬"` en tête + `"~∼≈"` onde | `"◉◎○"` (cercles vinyl) | un disque + notes flottantes + bruit de spectre + le rythme |
| **code / CLI / développeurs** | petits blocs ASCII dans `{}` `[]` `()` `<>` | `" 01[](){}<>#"` | `"·.,:|"` | `"★ ✦ . _"` | `"_"` curseur + `"   "` (clignotant) | `"◉⊞⊟"` modules | un graphe d'appels + un commit qui passe + curseur clignotant + pluie de rectangles |
| **artisanat / fait main** | marteau / copeaux / clous / points de rouille | `" .·°*+x#X@"` | `"·:.,"` (poussière) | `"✦ ▪ ▫"` | `"→"` en tête + `"-—"` tangente | `"◉○⊙"` (engrenages) | un établi + copeaux au vent + sciure + un coup de temps en temps |
| **méditation / bien-être / slow life** | formes ondulations / cercles / vagues | `" ··∘○●"` | `"~∼≈"` (onde respirante) | `". ∙ °"` | `"◌"` en tête + `"·· ··"` pointillés | `"◯◌○"` (cercles vides) | un cercle de respiration + ondulations + poussière chaude + lenteur |
| **matériel geek / électronique** | puces / blocs de circuit (`├┤├ ┐└┘`) | `" .·•◊◆■"` | `"⋅¨"` (bruit électrique) | `"⚡"` occasionnel + `"·"` | `"►"` en tête + `"==="` flux de données | `"⊙⊚⊛"` (LED) | un PCB + condensateurs flottants + un flux de données qui passe |
| **écriture / notes / pensée** | formes de ponctuation `"…"` `"——"` `"§"` | `" .,;:!?¶§"` | `"··¨"` | `". ∶ ⋮"` | `"✒"` en tête + `"~~~"` trait de plume | `"◉◯●"` (taches d'encre) | une plume + ponctuation flottante + un trait qui passe + des points de pensée |
| **rétro italien / années 80** | carrés pixel / géométries contrastées | `" .░▒▓█"` | `"·:|"` | `"◆ ◇ ▰"` | `"◉"` en tête + `"━━"` trait plein | `"■□▣"` | un CRT + particules pixel + lignes de balayage |
| **océan / voyage / ailleurs** | poissons / voiles / bateaux / vagues | `" .~≈≋"` ondulation | `"~∼≈≋"` (moirures) | `"·°"` (bulles) | `"⛵"` en tête + `"~~~"` sillage | `"◐◑◯"` (phases de lune) | un bateau + vagues + bulles + un oiseau de mer qui frôle |

#### Comment écrire les formes floaters

Chaque forme est un ASCII multi-lignes de 3-4 lignes, large de 8-12 caractères. Impérativement :
- contour fermé (ex. feuille `,/^\,` `(   )` `'\_/'`)
- des variantes différentes entre elles, au moins 3-6 distinctes
- largeur d'un caractère, pas de pleine chasse
- garder 1 case de padding pour que le tremblement en rotation soit joli

**Exemple feuilles** :
```js
floaters: [
  [" ,-^-, ",
   "|     |",
   " '---' "],
  ["  /\\\\  ",
   " /  \\\\ ",
   " \\__/ "],
  ["  *_*  ",
   " /...\\\\ ",
   " '___' "]
]
```

**Exemple notes de musique** :
```js
floaters: [
  ["  ♪    ",
   " /|    ",
   "♪ |____♪"],
  ["    ♫  ",
   "    /\\\\ ",
   "♪__/  \\\\"],
  ["  ♩    ",
   "  |    ",
   "  o    "]
]
```

**Contrôle après écriture** : coller SCENE dans la console, lancer `JSON.stringify(SCENE)` sans erreur, c'est bon.

#### Critères d'improvisation

Si le produit de l'utilisateur **n'est pas dans les 10 catégories** → concevoir le motif soi-même, en respectant :
1. **floaters** : 3-6 petits graphiques en lien concret avec le produit (« ça fait penser au produit »)
2. **centerShade** : 14 caractères de dégradé sombre→clair, débutant par les caractères sombres (` .,`) et finissant par les lumineux (`@#█`), transition continue
3. **diffuseChars** : 5-8 caractères « semi-transparents » (points / petits carrés / ondulations), pour l'atmosphère de fond
4. **streak** : l'ensemble doit s'estomper « lourd devant, léger derrière »
5. **sat / orbitDots** : 3 chacun, pour trois niveaux de poids

> Le principe en une phrase : **sans lunettes, à 3 mètres, on doit deviner de quel produit il s'agit.**

### 9. Correspondance tempérament → couleurs (sans style précisé)

| Mots-clés dans la description | Préréglage recommandé | Couleur dominante |
|---|---|---|
| calme / retenu / réflexion / écriture / notes / local-first | **cyan cosmos** (défaut) | `#8be9ff` cyan |
| chaleureux / fait main / à la chinoise / littéraire / lent / thé / rétro | **parchemin chaud** | `#660125` bordeaux |
| énergie / futur / IA / Web3 / jeu / geek | **violet cyber** | `#ff00aa` magenta néon |
| CLI / terminal / sécurité / rétro 80s / phosphor | **vert terminal** | `#00ff66` |
| nature / santé / méditation / voyage / nordique | **aurore** | `#7fe3c4` vert aurore |
| café / torréfaction / artisanat / alimentaire / désert / terre | **coucher de désert** | `#ff8b3d` orange brûlé |
| océan / ailleurs / bleu / calme / données | design libre | `#4fc3f7` bleu océan |
| noir et or / luxe / précision / horlogerie / matériel haut de gamme | design libre | `#d4af37` or champagne + fond noir |

Procédure de décision :
1. **L'utilisateur nomme le style** → suivre `styles.md`
2. **Pas de nom, mais tempérament évident** → prendre le préréglage le plus proche du tableau
3. **Tout ouvert** → cyan cosmos par défaut

### 10. Rapport

**Mode A** : une phrase.
> Généré ~/Desktop/{slug}.html — landing produit {nom}, 6 cartes fonctionnalités + 3 paliers de prix, style cyan cosmos. Double-cliquez pour ouvrir.

**Mode B** : le bloc HTML complet + une ligne.
> Enregistrez sous `{slug}.html` et double-cliquez. Pour changer les images, remplacez les URL par les vôtres. Pour modifier le grand titre ASCII, remplacez le gabarit dans le `<pre class="ascii-title lg">` en haut.

## Aide-mémoire des pièges

- **5 couches ASCII qui se bagarrent** : tester — sur fond sombre, les 5 couleurs doivent rester lisibles. Un rose trop vif ou un violet trop sombre fait tout s'effondrer
- **Grand ASCII mal gabarié** : le titre ANSI Shadow doit faire strictement 5-6 lignes de haut, pas 3
- **Dans `<pre>`, de vrais retours à la ligne**, pas des littéraux `\n`
- **data-cat des cartes non apparié au filtre** → le filtrage casse. Contrôler la cohérence
- **Palier du milieu sans `featured`** → le centre de gravité visuel se perd
- **Guillemets chinois dans les objets JSON** : dans les overlays ASCII, des guillemets → toujours des formes pleines `""`
- **Suppression d'une couche type `<pre id="ascii-comets">`** → erreur JS. Les 5 nœuds doivent tous rester
- **Pas d'URL d'images** → images paysage unsplash (`?auto=format&fit=crop&w=900&q=70`) ou picsum
