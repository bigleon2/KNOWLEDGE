---
name: portfolio-detail
description: Générer un site portfolio monofichier d'atelier à la chinoise (liste en lignes horizontales + vignette révélée au survol, typographie artistique lishu « Alimama DaoLiTi » via CDN, thème clair/sombre, pages détail routées par hash). Prend une description en langage naturel du studio (nom, directeur, discipline, œuvres) et produit UN fichier .html fonctionnel. Fonctionne AUSSI BIEN dans Claude Code (écrit dans ~/Desktop) que dans GLM / chat en ligne (sort le HTML en ligne). Phrases déclencheuses : « fais un portfolio d'atelier à la chinoise », « fais un portfolio en lishu », « lishu-portfolio-gen ... », « fais un portfolio façon Baiwu », ou quand l'utilisateur glisse ce dossier de skill dans le chat en demandant un site façon atelier.
visibility: public
mode: template
carrier: web-page
scenario: portfolio
pattern_source: reference.html
source_priority: skill-first
triggers:
  - « fais un portfolio d'atelier à la chinoise »
  - « fais un portfolio en lishu »
  - « fais un portfolio façon Baiwu »
  - « portfolio en lignes horizontales »
  - « portfolio en écriture dao-li »
related_patterns: vr-canvas, digital-eguide
legacy_gen: true
---

# portfolio-detail — atelier à la chinoise / portfolio lishu (avec pages détail)

## Signature en une phrase
Lignes de texte horizontales + grande image révélée au survol à droite + grands caractères artistiques Alimama DaoLiTi + aplat noir et blanc + light/dark + pages détail en routage hash + double vue liste/album.

## Différence avec les autres skills de portfolio

| skill | Motif central | Pour qui |
|---|---|---|
| `portfolio-gen` | canevas infini en glisser + tuiles | photographes / graphistes exposant des échantillons |
| `portfolio-museum-gen` | carrousel héro + grandes cartes + cascade + pages détail (curation d'images) | artistes vidéo/image/installation |
| `industrial-archive-gen` | couverture paginée à cadre noir + archives en barre latérale + industriel scandinave | produits physiques / objets / matériel |
| **`lishu-portfolio-gen`** | **lignes de texte horizontales + vignette au survol à droite + grands caractères lishu + retenue à la chinoise** | **reliure / typographie / artisanat / studio à la chinoise** |

Si le projet de l'utilisateur relève du « livre / lettrage / exposition / nature morte / pharmacopée / thé / céramique / bois / papier / encens » — tout ce qui exige une élégance retenue — c'est ce gabarit qu'il faut.

## Quand se déclencher

L'utilisateur dit :
- « fais un portfolio de style chinois / oriental / classique »
- « fais un site / une page de studio en style lishu »
- « fais un portfolio façon Baiwu » / « fais un site en liste horizontale comme Gurgel D'Alfonso »
- « lishu-portfolio-gen ... »

Et fournit :
- **la description du studio** (obligatoire) : nom, directeur, ville, discipline, titres et histoires de quelques œuvres
- **des images d'œuvres** (optionnel) : URL / téléversement / chemin. Sans images, ça tourne (placeholders picsum)

Si l'utilisateur **ne donne aucun titre d'œuvre** → demander au moins une fois quelles œuvres exposer.
S'il **ne donne que les titres** → écrire soi-même : pour chaque œuvre, générer 1 phrase d'appel + 3 paragraphes de prose + 6-8 lignes de specs + 3-6 images picsum + quelques crédits. Le ton adapté au type d'œuvre (livre → reliure / lettres → typographie / objet → nature morte / expo → identité d'exposition).

## Deux modes d'exécution

### Mode A · Claude Code / local (avec système de fichiers)
- Utiliser `Bash` pour lister les dossiers, `sips` pour sonder les dimensions de chaque image
- Sortie : `~/Desktop/{slug}-portfolio.html` (**monofichier**, toutes les images en URL)
- Si l'utilisateur fournit des images locales : les copier dans `~/Desktop/{slug}-portfolio-images/` et passer les src en chemins relatifs

### Mode B · GLM / dialogue en ligne (sans système de fichiers)
- L'utilisateur glisse un zip et voit 4 fichiers après décompression
- **Ne produire qu'une chaîne HTML complète**, dans un bloc ` ```html `
- Images téléversées sans URL → tout en `https://picsum.photos/id/{id}/{w}/{h}` (ID connus pour exister)
- Ne pas tenter d'accéder aux fichiers locaux, ne pas suggérer de ligne de commande

Décision : si vous **ne pouvez pas Read les images locales** → mode B par défaut.

## Répartition des fichiers

| Fichier | Rôle | Usage |
|---|---|---|
| `reference.html` | **référence achevée** — Baiwu 白屋, 6 œuvres | à regarder : formulations des items, ton de la prose, vocabulaire des specs, densité des champs JSON |
| `template.html` | **squelette vide** — mêmes CSS/JS/routage, 2 exemples + 20 repères SWAP | le modifier pour produire le HTML final |
| `README.md` | mode d'emploi côté utilisateur | le modèle n'a pas à le lire |
| `SKILL.md` | workflow pour le modèle (ce fichier) | **à lire obligatoirement** |

**Règle cardinale** : toutes les modifications partent de `template.html` ; on apprend de `reference.html` **comment écrire** (ton, longueurs, vocabulaire des tags), sans copier le contenu.

## Étapes de travail

### 1. Lire les deux HTML
- D'abord `reference.html` pour saisir « à quoi ressemble l'achevé » (notamment la densité des champs du JSON `works-data` et le ton de la prose)
- Puis `template.html` pour repérer les 20 emplacements SWAP

**Ne pas toucher au JS / au CSS / au système de routage des pages détail / à l'import des polices**.
Les SWAP se trouvent dans le texte HTML et les données JSON.

### 2. Analyser l'entrée utilisateur

Extraire :
- **ATELIER_NAME_ZH** — nom chinois du studio (2-4 caractères idéalement, ex. 白屋「maison blanche」, 素园「jardin simple」, 墨记「carnet d'encre」, 青庐「hutte verte」, 拙轩「pavillon rustique」)
- **PINYIN** — transcription (5-6 lettres, tout en capitales : BAIWU / SUYUAN / MOJI)
- **CHAR** — caractère unique du logo (généralement le premier du nom : 白 / 素 / 墨 / 青 / 拙)
- **CITY** — ville
- **DIRECTOR_ZH / DIRECTOR_EN** — nom du directeur + transcription
- **DISCIPLINE** — 3 mots de discipline (« reliure · typographie · nature morte »)
- **TAGLINE** — positionnement en une phrase (20-40 caractères, tempérament kai)
- **YEAR_FOUNDED** — année de création (peut prendre la forme du cycle sexagésimal : « hiver yiwei », « printemps jiachen »)

Pour chaque œuvre :
- **slug** — identifiant d'URL, minuscules et tirets (`kong-shan-ji` / `wu-ming-shu`)
- **title_zh** — titre chinois (2-5 caractères idéalement ; plus c'est concis, plus c'est distingué)
- **title_en** — sous-titre anglais (style titre d'ouvrage : `An Anthology of Empty Mountains`)
- **year** — année, éventuellement en cycle sexagésimal (`甲辰 / 2024` / `2025` / `乙巳 / 2025`)
- **tag** — catégorie de tête, entre crochets : `[ recueil de poèmes · design de reliure ]` / `[ design typographique · herbier de pharmacopée ]`
- **cover** — URL de la grande image de la page détail
- **location de la ligne de liste** — `ville, année · procédé/format` (révélée au survol)
- **meta** — 4 paires clé-valeur (résumé 4 colonnes de la page détail)
- **lead** — 30-70 caractères en grands corps, un mot soulignable en `<em>mot-clé</em>`
- **prose** — 3-4 paragraphes, 80-150 caractères chacun
- **specs** — 6-10 lignes de fiche technique (format/papier/reliure/typographie/tirage/impression/procédé/prix…)
- **gallery** — 3-6 images, layout au choix parmi `g-wide` / `g-half` / `g-third`
- **credits** — 4-7 paires rôle/nom

Si l'utilisateur ne donne qu'une phrase / pas d'histoire → **composer soi-même** : d'après le titre et le type de l'œuvre, écrire lead et prose au ton qui convient. Le ton de référence est dans reference.html — pas de langage marketing, plutôt « cartel de musée + notes d'atelier » (retenu, précis, lent, avec des traces d'artisanat).

### 3. Lister les œuvres + sonder les dimensions (mode A seulement)

```bash
ls -la "{works_path}"
sips -g pixelWidth -g pixelHeight "{works_path}/{file}" 2>/dev/null
```

Obtenir (fichier, l, h, ratio) pour chaque image. Privilégier les portraits pour les vignettes de liste (conteneur 4:3 : les verticales sont plus photogéniques).

### 4. Remplacer les 20 SWAP

| SWAP | Emplacement | Contenu |
|---|---|---|
| 1 | `<title>` | `{ATELIER_NAME} {PINYIN} — portfolio de {DIRECTOR} / Studio` |
| 2 | meta description | une phrase de présentation du site |
| 3 | caractère unique du rideau | premier caractère du nom du studio (ex. 白) |
| 4 | caractère unique dans le logo SVG | identique au SWAP-3 |
| 5 | pinyin dans le logo SVG | `{PINYIN}` en capitales |
| 6 | li de la navigation principale | généralement 3 entrées : œuvres / à propos / contact |
| 7 | nom chinois du brand-block | `{ATELIER_NAME}` éclaté avec espaces (ex. `白&nbsp;&nbsp;屋`) |
| 8 | anglais du brand-block | `{PINYIN} Studio · {CITY}` |
| 9 | tagline | positionnement en kai, 20-40 caractères, `<br>` possible |
| 10 | **N items de liste** | chaque `<a class="item" href="#work/{slug}">` avec num/project-name/en-name/location/photo-thumb |
| 11 | **N items de galerie** | les mêmes N œuvres, grille plus resserrée — le slug doit coïncider avec la liste |
| 12 | titre À propos | `À&nbsp;propos&nbsp;{name}<span class="en">About</span>` |
| 13 | paragraphes À propos | 1-3 paragraphes en kai (genèse / directeur / vision du design), 60-120 caractères chacun |
| 14 | fiche de faits À propos | 4-6 li (Fondation/Lieu/Discipline/Directeur/Horaires) |
| 15 | titre Contact | `Écrivez-nous<span class="en">Get in Touch</span>` |
| 16 | paragraphes Contact | 1-2 paragraphes d'invitation à écrire + promesse de délai de réponse |
| 17 | fiche de faits Contact | 4-6 entrées (E-mail/Téléphone/Adresse/Instagram/compte officiel) |
| 18 | credit tournant | `Site by {WHO}` (généralement le nom du studio) |
| 19 | les trois blocs du footer | © / ICP / liens sociaux |
| 20 | **JSON works-data** | **les données détail complètes des N œuvres (capital !)** |

### 5. Écrire le JSON works-data (l'étape décisive)

Chaque œuvre doit avoir son entrée dans le tableau ; **le slug doit coïncider exactement avec le `#work/SLUG` des href des cartes list/gallery**.

Champs du JSON :
```json
{
  "slug": "kong-shan-ji",
  "title_zh": "空山集",
  "title_en": "An Anthology of Empty Mountains",
  "year": "甲辰 / 2024",
  "tag": "[ 诗集 · 装帧设计 ]",
  "cover": "https://picsum.photos/id/143/1800/1100",
  "meta": [
    {"label": "Type / 类型", "value": "诗集装帧"},
    {"label": "Year / 年份", "value": "2024"},
    {"label": "Edition / 印量", "value": "首印 320 本"},
    {"label": "Format / 开本", "value": "130 × 195 毫米"}
  ],
  "lead": "三十六首关于山的诗。我们想做一本——读者翻开后，先听见<em>风声</em>，再读见字的书。",
  "prose": [
    "段落一：诗稿来源 / 设计语境。80—150 字。",
    "段落二：制作中的关键决定 — 字体、纸张、装订选择。",
    "段落三：最后呈现 / 留给读者的感受。"
  ],
  "specs": [
    ["开本 / Format", "130 × 195 毫米"],
    ["页数 / Pages", "144 页"],
    ["纸张 / Paper", "本色棉纸 90gsm"],
    ["装订 / Binding", "线装四目"],
    ["字体 / Typeface", "老宋（标题）· 楷体（正文）"],
    ["印刷 / Printing", "单色凸印"],
    ["印量 / Edition", "首印 320 本"],
    ["定价 / Price", "¥ 388"]
  ],
  "gallery": [
    {"src": "...", "layout": "g-wide", "caption": "封面"},
    {"src": "...", "layout": "g-half"},
    {"src": "...", "layout": "g-half"},
    {"src": "...", "layout": "g-third"},
    {"src": "...", "layout": "g-third"},
    {"src": "...", "layout": "g-third"}
  ],
  "credits": [
    ["设计 / Design", "周墨白"],
    ["手工装订 / Binding", "陈漱石（杭州·订书坊）"]
  ]
}
```

**Pièges du JSON ⚠️** :
- pour des guillemets dans la prose chinoise → utiliser obligatoirement les formes pleines `「...」` ou `"..."` (U+201C / U+201D), **jamais** le `"` ASCII (il casse le JSON)
- pas de vrais retours à la ligne dans les chaînes JSON ; pour un paragraphe de plus, ajouter un élément au tableau prose
- `<em>mot</em>` dans lead s'écrit **directement en HTML** — rendu via innerHTML
- `layout` de gallery : exactement l'un des trois — `g-wide` (pleine largeur) / `g-half` (moitié) / `g-third` (tiers)

### 6. Choix des images sources
- **placeholder picsum** : préférer la forme `id/X` à `seed/X` (plus stable). ID éprouvés : 0, 20, 40, 51, 64, 76, 88, 91, 96, 119, 121, 130, 143, 145, 158, 164, 165, 175, 177, 180, 187, 195, 200
- Pour cover / gallery d'une même œuvre, prendre des ID voisins : la teinte reste cohérente
- Ne pas utiliser le paramètre `?grayscale` (les images doivent rester en couleur)

### 7. Inspiration de noms de studios chinois (si l'utilisateur n'en donne pas)
Si l'utilisateur vous laisse nommer → 2 caractères, patine ancienne :
- noms d'objets : 白屋 / 素园 / 墨记 / 青庐 / 拙轩 / 听雨 / 一勺 / 半亩
- noms de lettres : 素白 / 子衿 / 砚池 / 半山 / 寻常 / 浮云
- éviter les mots fonctionnels « studio / design / Studio » : le nom doit être poème en soi

### 8. Support vidéo
Si la cover d'une œuvre est un .mp4 / .webm / .mov, la page détail substitue automatiquement `<video autoplay muted loop>` à `<img>`. Il suffit de donner le chemin vidéo dans l'URL de cover.

### 9. Rapport

**Mode A** : une phrase.
> Généré ~/Desktop/baiwu-portfolio.html — 6 œuvres ; survoler une ligne affiche la vignette, un clic ouvre le détail. Light/Dark en bas à gauche, liste/album en haut au centre.

**Mode B** : le bloc HTML complet + une ligne.
> Enregistre ce qui précède en `index.html` et double-clique. Survole un titre d'œuvre pour voir la vignette à droite, clique pour la page détail. Pour changer les images, remplace les URL picsum par les tiennes.

## À conserver impérativement (ne pas modifier)

- **l'import des polices** : `@font-face` chargeant le woff2 Alimama DaoLiTi (ne pas changer de source)
- **le système de variables CSS** : double thème light/dark
- **tout le JS** : bascule de thème, bascule de vue, interaction hover-row, credit tournant, routage hash des pages détail `applyRoute()`, `renderDetail()`
- **le nœud `<script id="works-data">`** doit rester
- **`<main id="detail-root">`** doit rester (point de montage des pages détail)
- **le système d'états `body[data-view="home/detail"]` et `body[data-mode="list/gallery"]`**
- **les cinq éléments en position fixe #logo / #main-menu / .theme-toggle / #project-view / #svp-credit**

## Aide-mémoire des pièges

- **slug non apparié** : item de liste `#work/kong-shan-ji` ↔ item de galerie `#work/kong-shan-ji` ↔ JSON `"slug": "kong-shan-ji"` — les trois doivent coïncider exactement
- **guillemets JSON** : dans le contenu chinois, toujours des formes pleines 「」 ou `"..."`, jamais le `"` ASCII
- **galerie trop chargée** : 6 images maximum par œuvre, au-delà la mise en page se dérègle
- **prose trop longue** : 80-150 caractères par paragraphe ; au-delà de 200, la lecture se dégrade
- **liste / galerie désynchronisées** : les mêmes œuvres dans les deux vues (correspondance un à un)
- **picsum seed** : `id/X` plutôt que `seed/X`, pour éviter qu'un ID aléatoire tombe sur une image supprimée
- **moins de 3 œuvres** : possible, 2 suffisent pour que ça tourne
- **plus de 8 œuvres** : envisager deux lots — trop de lignes allongent la page
- **lettrine** : `.detail__prose p:first-of-type::first-letter` en DaoLiTi — le premier paragraphe doit commencer par un caractère chinois (pas par `<em>` ni par de l'anglais)
- **ne pas décolorer picsum** : les images restent en couleur, pas de `filter: grayscale()` dans le CSS
