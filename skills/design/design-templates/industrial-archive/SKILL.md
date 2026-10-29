---
name: industrial-archive
description: Generate a single-file industrial-archive product landing page (Nordic museum aesthetic, hash-routed detail pages). Takes a natural-language description of one or more "exhibit-style" products (objects, tools, hardware, watches, kitchenware, lighting, audio, instruments, anything with a designed/forged/restrained quality); outputs ONE working .html file. Visitors see a black-framed cover that flips between exhibits, sidebar index, side meta column (material/origin/year/dimension), and click any exhibit → full detail page (giant italic title, spec table, hero image, lead + 3 prose paragraphs, gallery, prev/next). Runs in BOTH Claude Code (writes to ~/Desktop) and GLM / online chat (outputs HTML inline). Trigger: « fais une landing produit industrielle », « fais une page d'exposition façon objets retenus », « industrial-archive-gen ... », ou quand l'utilisateur glisse ce dossier de skill dans le chat en demandant une page produit au style archive industrielle nordique.
visibility: public
mode: template
carrier: web-page
scenario: brand-landing
pattern_source: reference.html
source_priority: skill-first
triggers:
  - « fais une landing produit industrielle »
  - « fais une page d'exposition façon objets retenus »
  - « style collection de musée nordique »
  - « industrial archive »
  - « page produit façon curation »
related_patterns: portfolio-detail
legacy_gen: true
---

# industrial-archive — générateur de pages d'exposition / landing produit industrielles

Transformer « une description en langage naturel » en un HTML monofichier, avec l'effet **archive industrielle nordique / curation de musée** :

- grandes images produit dans un cadre noir, bascule par clics gauche-droite
- catalogue d'exposition à gauche avec barre d'index
- 4 blocs meta à droite (matière / provenance / époque / dimensions)
- bandeau défilant en haut
- un clic sur le cadre ou le CTA bas → page détail de l'exposé (titre italique géant, fiche technique, image principale, grande ouverture + 3 paragraphes, galerie 6 images, précédent/suivant)
- splash d'entrée avec citation

## Quand se déclencher

L'utilisateur dit « fais une landing produit industrielle / une exposition façon objets retenus / industrial-archive-gen... », et fournit :
- **une description des produits** (obligatoire) : un texte en prose décrivant 1—N exposés — noms, époque, provenance, matière, histoire
- **des URL d'images** (optionnel) : au moins 1 image principale par exposé, idéalement 3—6 détails. Sans images, ça tourne (placeholders picsum gris)
- **un style** (optionnel) : par défaut gris acier froid ; remplaçable par les préréglages de styles.md

Si l'utilisateur **ne donne ni nom ni histoire** → demander au moins une fois quels exposés montrer, et de quelle catégorie (contenant / luminaire / chaise / instrument / outil / ...).

S'il **ne donne que les noms** → composer soi-même : pour chaque exposé, 1 phrase d'appel + 3 paragraphes + 4-6 lignes de specs. Le ton de référence est dans `reference.html` : **cartel de musée** — retenu, précis, lent ; pas de langage marketing.

## Deux modes d'exécution

### Mode A · Claude Code / local (avec système de fichiers)
- Sortie : `~/Desktop/{slug}-archive.html` (**monofichier**, toutes les images en URL)
- Si l'utilisateur fournit des images locales, lui suggérer de passer des URL, ou de les copier dans le même dossier et d'écrire des chemins relatifs

### Mode B · GLM / dialogue en ligne (sans système de fichiers)
- **Produire directement une chaîne HTML complète**, dans un bloc ` ```html `
- Pas d'URL d'images → tout en `https://picsum.photos/seed/{slug}-{nn}/{w}/{h}?grayscale`
- Ne pas tenter d'accéder aux fichiers locaux

Décision : si vous **ne pouvez pas Read les images locales** → mode B par défaut.

## Répartition des fichiers

| Fichier | Rôle | Usage |
|---|---|---|
| `reference.html` | **référence achevée** — 4 pièces d'archive industrielle nordique « objets retenus » | à regarder : comment écrire le lead, le ton de la prose, le vocabulaire des specs, le format des taglines, le nommage des ateliers |
| `template.html` | **squelette vide** — mêmes CSS/JS/routage, 2 exemples + 17 repères SWAP | le modifier pour produire le HTML final |
| `styles.md` | bibliothèque de préréglages | à consulter si l'utilisateur précise un style |
| `README.md` | mode d'emploi côté utilisateur | le modèle n'a pas à le lire |
| `SKILL.md` | workflow pour le modèle (ce fichier) | **à lire obligatoirement** |

**Règle cardinale** : toutes les modifications partent de `template.html` ; on apprend de `reference.html` **comment écrire** (ton, longueurs, vocabulaire), sans copier le contenu.

## Différence clé — la référence utilise du SVG, le gabarit des `<img>`

- Les 4 exposés de `reference.html` sont des **SVG dessinés à la main** (bouilloire en fonte / lampe à roulement / chaise en bouleau / télémètre) — un contenu sur mesure
- `template.html` a remplacé le système SVG par `<img src="cover URL">` : URL de l'utilisateur s'il y en a une, picsum sinon
- Pas besoin d'écrire du SVG. Si l'utilisateur demande expressément un « dessin », alors envisager une fonction SVG injectée dans `coverHTML()`

## Étapes de travail

### 1. Lire les deux HTML
- D'abord `reference.html` pour saisir « l'achevé », notamment la densité des champs du JSON `exhibits-data` et le ton de la prose (retenu, précis, ancré dans l'époque)
- Puis `template.html` pour repérer les 17 marqueurs SWAP (chercher `SWAP-`)

**Ne pas toucher au JS / au CSS / au système de routage des pages détail**.
Les SWAP se trouvent dans le texte HTML et les données JSON.

### 2. Analyser l'entrée utilisateur

#### Niveau site (SWAP 1-15 et 17)
- **COLLECTION_TITLE / COLLECTION_SUB** — grand titre de la série + sous-titre. Ex. « objets retenus / archive industrielle nordique 1948—1988 ». SWAP-1
- **INTRO_VOLUME_TAG** — tag en haut de la page d'entrée, ex. « archive industrielle nordique · Vol.01 ». SWAP-2
- **INTRO_TITLE_HTML** — grand titre du splash, 2-4 caractères + un séparateur `<span class="accent">·</span>`. Ex. `克制<span class="accent">·</span>之物`. SWAP-3
- **INTRO_TITLE_EN** — sous-titre anglais du splash, capitales + tiret cadratin : `Restrained Objects — A Nordic Industrial Archive 1948 — 1988`. SWAP-4
- **INTRO_QUOTE** — une citation de curation, 60—100 caractères, en prose. SWAP-5
- **INTRO_ATTRIBUTION** — source de la citation, ex. `— avant-propos de curation / Curatorial Note`. SWAP-6
- **HEAD_GLYPH** — caractère du logo en haut à gauche. 1-2 caractères serif, de préférence une lettre à caractère : `Æ` `Ø` `沉` `匠` `ʘ`. SWAP-7
- **HEAD_GLYPH_SUB** — ligne sous le logo, ex. `objets retenus / numéros N°01—04`. SWAP-8
- **HEAD_CENTER_CN / HEAD_CENTER_EN** — les deux petites lignes centrales du haut. SWAP-9, 10
- **HEAD_RIGHT_TOP / HEAD_RIGHT_BOTTOM** — deux lignes à droite : date/ville + coordonnées/numéro. SWAP-11, 12
- **CURATOR_NAME / CURATOR_EMAIL** — nom du curateur + e-mail. SWAP-13, 14
- **CRUMB_ROOT / CRUMB_VOLUME** — les deux items fixes du fil d'Ariane des pages détail. SWAP-15
- **TICKER_TAIL** — devise générale en queue de bandeau défilant. SWAP-17

#### Champs de chaque exposé (SWAP-16, le plus important)
```json
{
  "slug": "iron-kettle",
  "num": "N°01",
  "title": "铸铁壶",
  "en": "IRON KETTLE",
  "year": "1958",
  "place": "丹麦 · 哥本哈根",
  "maker": "Carl Hansen Værksted / 卡尔·汉森工坊",
  "material": "灰口铸铁 · 山毛榉木柄<br/>黑釉烧结涂层",
  "origin": "丹麦 · 哥本哈根<br/>Carl Hansen Værksted",
  "dim": "高 18 cm · 容 1.2 L<br/>底径 14 cm",
  "tagline": "FORGED ESSENTIAL / 锻造的必需品",
  "lead": "一只为<em>沉默与水的低温</em>而设计的容器——壶身的厚度，是为了让热停留得久一点，而不是更快地变热。",
  "spec": [
    ["编号", "1958 · K-04"],
    ["材料", "灰口铸铁 + 山毛榉"],
    ["工艺", "砂模铸造 / 黑釉烧结"],
    ["重量", "1.86 kg"],
    ["产量", "限量 240 件 · 现存 31"]
  ],
  "prose": [
    "段一 80—160 字。来源/语境/年份/工坊背景。",
    "段二 80—160 字。工艺/手工细节/关键决定。",
    "段三 80—160 字。今天的状态/影响/仍在用的事实。"
  ],
  "cover": "https://example.com/kettle-cover.jpg 或 picsum URL",
  "gallery": [
    {"src": "...", "layout": "f-3", "caption": "壶身正立面"},
    {"src": "...", "layout": "f-2", "caption": "山毛榉木柄"},
    {"src": "...", "layout": "f-2", "caption": "壶嘴细部"},
    {"src": "...", "layout": "f-2", "caption": "底部砂模印"},
    {"src": "...", "layout": "f-4", "caption": "工坊蓝图"},
    {"src": "...", "layout": "f-6", "caption": "陈列剖面"}
  ]
}
```

### 3. Remplacer les SWAP

Remplacer dans `template.html` les 17 placeholders `{{...}}` par le contenu extrait.
**Attention** : `{{INTRO_TITLE_HTML}}` est du HTML, pas du texte brut — il doit contenir `<span class="accent">·</span>`.

### 4. Écrire le JSON exhibits-data (l'étape décisive)

Remplacer **entièrement** les 2 objets d'exemple du `<script id="exhibits-data" type="application/json">` par N vrais objets d'exposition.

#### Nombre de pièces conseillé
- Minimum 1 (une landing mono-produit marche — le JS gère N=1 sans carrousel automatique)
- Idéal 3—6
- Au-delà de 8, l'index s'encombre ; envisager un découpage

#### Longueur des titres
- `title` : 2-4 caractères chinois pour le meilleur rendu (« bouilloire en fonte », « lampe à roulement », « télémètre »). Nom long → le mettre en tagline
- `en` : anglais en capitales, 2 mots idéalement

#### Format du tagline
Fixe : `phrase anglaise + espace/slash/espace + phrase chinoise`, ex. :
- `FORGED ESSENTIAL / 锻造的必需品`
- `PIVOT & LIGHT / 旋转与光`
- `FOUR LEGS, NO MORE / 四只脚，仅此而已`
- `MEASURED HORIZON / 被丈量的地平线`

#### Écriture du lead
30—80 caractères. **Il faut marquer un ou deux mots-clés avec `<em>...</em>`** — le CSS leur ajoute un fin soulignement bleu acier.
Contre-exemple : `C'est une très bonne bouilloire.` ← pas d'em, pas de détail précis
Bon exemple : `Un récipient conçu pour <em>le silence et la basse température de l'eau</em> — l'épaisseur de la fonte sert à retenir la chaleur, pas à chauffer plus vite.`

#### Écriture de la prose
3 paragraphes de 80—160 caractères. Ton : **cartel de musée** — retenu, précis, ancré dans l'époque, pas de marketing.
- ¶ 1 : provenance / contexte (lieu, année, atelier, époque)
- ¶ 2 : procédé / décisions (choix de design décisifs, détails artisanaux, pourquoi)
- ¶ 3 : devenir / influence (exemplaires restants, usage actuel, postérité)

#### Écriture des specs
4-6 lignes, une paire clé-valeur par ligne.
- La première : `["numéro", "{année} · {référence}"]`
- La dernière, production/extant : `["production", "série limitée 240 exemplaires · 31 subsistants"]` (le JS affiche la valeur de la dernière ligne dans le bloc « EXTANT » de la page détail)

#### layout de gallery : exactement l'un des quatre
- `f-3` — paysage, 16:10, demi-largeur (3 colonnes sur 6)
- `f-2` — portrait, 4:5, tiers de largeur
- `f-4` — paysage, 16:9, deux tiers de largeur
- `f-6` — pleine largeur, 21:8

**Rythme conseillé** : 1 f-3 + 3 f-2 + 1 f-4 + 1 f-6 = 6 images, deux lignes et demie.

#### URL des images
Mode A avec URL de l'utilisateur → l'utiliser ;
Mode B sans → picsum : `https://picsum.photos/seed/{slug}-{numéro}/{w}/{h}?grayscale`
- cover : `1600/1000`
- f-3 : `900/600`
- f-2 : `600/750`
- f-4 : `1200/675`
- f-6 : `1600/610`
- le `?grayscale` garde les placeholders dans le gris industriel

### 5. Variantes de style (optionnel)
Si l'utilisateur précise un style, modifier les 8 variables CSS de `:root` selon `styles.md`. Le défaut gris acier froid colle au mieux à l'original « objets retenus ».

### 6. Rapport

**Mode A** : une phrase.
> Généré `~/Desktop/{slug}-archive.html` — N exposés, gris acier par défaut. Double-cliquez ; un clic sur le cadre ou le CTA ouvre le détail. Pour changer les images, remplacez les URL picsum de cover/gallery par les vôtres.

**Mode B** : le bloc HTML complet + une ligne.
> Enregistrez ce qui précède en `index.html` et double-cliquez. Cliquez le cadre pour le détail, ← → pour changer d'exposé. Pour les images, remplacez toutes les URL picsum par les vôtres.

## À conserver impérativement (ne pas modifier)

- tout le JS : bascule translate / flip, fonction `coverHTML()`, `renderSidebar()`, `applyMeta()`, `renderDetail()`, clavier / carrousel automatique / curseur
- tout le CSS (sauf variante de style sur `:root`)
- le nœud `<script id="exhibits-data" type="application/json">` doit rester
- le nœud `<div id="proj-list" class="proj-list">` doit rester (mais **ne pas** écrire les li à la main — `renderSidebar()` les génère)
- la structure double face du flipper dans `<div id="cover-stage">`
- la grille 9 cases de `<main class="stage">`

## Aide-mémoire des pièges JSON

- **guillemets chinois** : pour des guillemets dans prose / lead, utiliser les formes pleines `"..."` (U+201C / U+201D), **jamais** le `"` ASCII (il casse le JSON)
- **vrais retours à la ligne** : pas de retour réel dans une chaîne JSON (touche Entrée), ni de `\n`. Un paragraphe de plus = un élément de plus dans prose ; un saut de ligne = `<br/>`
- **balise `<em>`** : dans lead, **écrire directement le HTML** `<em>...</em>` — rendu via innerHTML, le CSS ajoute le soulignement bleu acier
- **slug unique** : chaque exposé a un slug unique, minuscules et tirets (`iron-kettle`, pas `IronKettle` ni `iron_kettle`)
- **orthographe des layouts** : exactement `f-3` `f-2` `f-4` `f-6`, toute faute casse l'affichage
- **seed picsum unique** : une graine unique par image, sinon plusieurs emplacements affichent la même
- **format du num** : `N°01` — le N suivi de ° (U+00B0) est obligatoire ; pas `No.01` ni `N01`
- **maker avec « / »** : `"nom d'atelier anglais / nom chinois"` — le JS coupe à gauche du `/` pour l'affichage en bas à droite

## Limites de longueur / de nombre

- title ≤ 4 caractères ; au-delà, reporter le surplus dans le tagline
- lead ≤ 80 caractères (une ligne et demie)
- prose : 80—160 caractères par paragraphe (150, le sweet spot)
- specs : 4-6 lignes
- galerie : 3-6 images (moins de 3, trop vide ; plus de 6, mise en page chaotique)
- nombre total d'exposés : 1—8 (idéal 3—6)
- le bandeau défilant se remplit seul — le JS parcourt les DATA

## Aide-mémoire des déclencheurs de style

Ce que dit l'utilisateur → quel style appliquer :
- rien / « retenu » / « nordique » / « industriel » → défaut gris acier froid (celui du gabarit)
- « chaleureux » / « rétro » / « tons bruns » / « cuir » → styles.md `warm-leather`
- « sombre » / « foncé » / « nuit » → styles.md `night-iron`
- « papier » / « impression » / « report » → styles.md `paper-press`
- « unis » / « bleu marine » → styles.md `navy-blueprint`
