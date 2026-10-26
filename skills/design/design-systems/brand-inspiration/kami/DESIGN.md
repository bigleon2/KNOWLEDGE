---
version: alpha
name: Kami
description: "Système de papier éditorial : toile de parchemin chaleureuse, accent bleu encre, hiérarchie menée par les empattements. Conçu pour les CV, les pages uniques, les livres blancs, les portfolios, les présentations — tout ce qui devrait avoir l'air d'une impression de haute qualité plutôt que d'une interface utilisateur. Multilingue par conception (EN · zh-CN · ja)."
category: "Éditorial & Impression"
colors:
  palette: ["#f5f4ed", "#1b365d", "#ffffff", "#e4ecf5", "#2d5a8a", "#faf9f5"]
typography:
  fonts: "JetBrains Mono"
note: "Le frontmatter est extrait automatiquement ; le corps de texte ci-dessous est la source autorisée pour les jetons complets, composants et règles."
---
# Système de design inspiré par kami (紙 / 纸)

> Catégorie : Éditorial & Impression
> Système de papier éditorial : toile de parchemin chaleureuse, accent bleu encre, hiérarchie menée par les empattements. Conçu pour les CV, les pages uniques, les livres blancs, les portfolios, les présentations — tout ce qui devrait avoir l'air d'une impression de haute qualité plutôt que d'une interface utilisateur. Multilingue par conception (EN · zh-CN · ja).

## 1. Thème visuel & Atmosphère

kami se résume en une phrase : **toile de parchemin chaleureuse, accent bleu encre, serif porte la hiérarchie, aucun gris froid, aucune ombre dure.** Ce n'est pas un framework d'interface utilisateur — c'est un système de contraintes pour la page, conçu pour garder les livrables stables, clairs et incontestablement *imprimés*. Le nom se lit comme **kami / 紙 / 纸** — le même mot pour "papier" en japonais et en chinois — et le système est co-conçu en anglais, chinois simplifié et composition japonaise dès le départ, pas adapté a posteriori.

L'arrière-plan de la page est du parchemin (`#f5f4ed`), jamais blanc pur. Le texte repose sur un crème. Le seul mouvement chromatique est le bleu encre (`#1B365D`) — utilisé sur les numéros de section, les CTAs primaires, la règle gauche d'une citation, le poids W500 dans une métrique. Tout le reste est un neutre chaud avec une sous-teinte jaune-brun ; les gris bleus froids sont intentionnellement absents.

La hiérarchie est portée presque entièrement par **le serif à un seul poids (500)**. Il n'y a pas de gras, pas d'italique, pas de deuxième couleur d'accentuation. La densité est obtenue par des interlignages serrés (1,10–1,55), des rampes de gris à quatre niveaux, et des ombres en anneau/ murmure qui agissent comme des halos plutôt que comme des gouttes. L'esthétique emprunte à l'impression éditoriale, aux livres blancs techniques et aux anciennes correspondances à machine à écrire — l'objectif est "un bon contenu sur un bon papier", pas "une interface d'application moderne".

**Caractéristiques clés :**
- Toile de parchemin chaleureuse (`#f5f4ed`) — jamais `#ffffff`
- Un seul accent : bleu encre (`#1B365D`), couvre ≤ 5% de toute surface
- Tous les gris sont chauds (R ≈ G > B), aucun gris bleu froid n'est présent
- Serif partout pour la hiérarchie : Charter (EN), TsangerJinKai02 / Source Han Serif (CN), YuMincho (JA)
- Verrouillé au poids 500 — aucun gras synthétique (700/900) et **pas d'italique**
- Rythme d'impression serré (interlignages 1,10–1,55), beaucoup plus dense que le corps web typique
- Profondeur via des anneaux de 1px et des ombres murmure (`0 4px 24px rgba(0,0,0,0,05)`), jamais d'ombres dures
- Les remplissages de balises sont hexadécimaux solides (ex. `#E4ECF5`), jamais `rgba()` — les rendus d'impression repeignent deux fois les balises alpha
- Les chiffres sont dans `font-variant-numeric: tabular-nums` afin que les colonnes de métriques ne tremblent pas

## 2. Palette de couleurs & Rôles

### Marque
- **Bleu Encre** (`#1B365D`) : La seule couleur chromatique. CTAs, numéros de section, texte de lien sur des surfaces claires, la règle gauche sur un titre de section ou citation, l'état actif d'un sélecteur, la valeur métrique W500.
- **Bleu Encre Clair** (`#2D5A8A`) : Variante plus claire, uniquement pour les liens sur des surfaces sombres.

> Règle : le bleu encre couvre ≤ **5% de la surface du document**. Plus que cela, cela devient un ornement et la contrainte s'effondre.

### Surface
- **Parchemin** (`#f5f4ed`) : Arrière-plan de page — crème chaud, la base émotionnelle. Ne jamais remplacer par du blanc.
- **Ivoire** (`#faf9f5`) : Cartes et conteneurs surélevés. Assis un demi-teinte plus clair que le parchemin.
- **Sable Chaud** (`#e8e6dc`) : Arrière-plan de bouton par défaut, surfaces interactives secondaires.
- **Surface Sombre** (`#30302e`) : Conteneurs en thème sombre — charbon chaud, pas ardoise.
- **Foncé Profond** (`#141413`) : Arrière-plan de page en thème sombre. Noir légèrement olive, jamais `#000000`.

### Texte (quatre niveaux — pas de cinquième)
- **Noir Proche** (`#141413`) : Texte principal. Chaleur d'olive légère, plus douce que le noir pur.
- **Foncé Chaud** (`#3d3d3a`) : Texte secondaire, en-têtes de tableau, liens par défaut.
- **Olive** (`#504e49`) : Sous-texte, légendes, descriptions. (Remplacement JA : `#4d4c48` car les traits de YuMincho sont plus fins.)
- **Pierre** (`#6b6a64`) : Tertiaire — dates, métadonnées, étiquettes méta.

### Bordure
- **Bordure** (`#e8e6dc`) : Bordure principale — séparateurs de section, bords de carte, en-têtes de tableau.
- **Bordure Douce** (`#e5e3d8`) : Séparateurs de ligne, séparateurs internes, lignes internes subtiles.

### Teintes de balise (solide, PAS rgba)
Les rendus d'impression (WeasyPrint et consorts) repeignent deux fois les remplissages alpha, laissant un "double rectangle" visible au zoom. Les arrière-plans de balise et puce doivent être hexadécimaux solides, pré-mélangés sur parchemin :

| Alpha effectif de `#1B365D` sur parchemin | Hexadécimal solide |
|---|---|
| 0,08 | `#EEF2F7` |
| 0,14 | `#E4ECF5` |
| **0,18 (balise par défaut)** | **`#E4ECF5`** |
| 0,22 | `#D0DCE9` |
| 0,30 | `#D6E1EE` |

### Système de dégradé
kami est **sans dégradé** par défaut. Le seul dégradé autorisé est le pinceau doux de balise courant `#D6E1EE → #E4ECF5 → #EEF2F7` de gauche à droite à très faible contraste — utilisé au plus une fois par page sur une seule balise décorative. N'introduisez pas de dégradés héroïques, de lavages de couleur de marque, ou de flous de filtre d'arrière-plan.

### Couleurs interdites
- `#ffffff` comme arrière-plan de page
- `#000000` n'importe où
- Toute surface gris froid (`#f8f9fa`, `#f3f4f6`, `slate-*`)
- Toute deuxième couleur saturée (pas deuxième accent — choisissez le bleu encre ou rien)

## 3. Règles de typographie

### Piles de polices

```css
/* Anglais (par défaut) */
--serif: Charter, Georgia, Palatino, "Times New Roman", serif;

/* Chinois */
--serif: "TsangerJinKai02", "Source Han Serif SC", "Noto Serif CJK SC",
         "Songti SC", "STSong", Georgia, serif;

/* Japonais */
--serif: "YuMincho", "Yu Mincho", "Hiragino Mincho ProN",
         "Noto Serif CJK JP", "Source Han Serif JP",
         "TsangerJinKai02", Georgia, serif;

/* Mono — doit inclure le repl CJK afin que les étiquettes/commentaires ne s'affichent pas comme des boîtes */
--mono: "JetBrains Mono", "SF Mono", "Fira Code", Consolas, Monaco,
        "TsangerJinKai02", "Source Han Serif SC", monospace;

/* Sans est toujours égal à serif. Il n'y a pas de famille sans-serif séparée. */
--sans: var(--serif);
```

### Quand changer la pile

Les trois piles ci-dessus sont **des valeurs alternatives pour `--serif`**, pas trois familles superposées. Lors de la génération d'un artefact, définissez la pile principale sur `:root` en fonction de la langue dominante du contenu ; laissez le repl par glyphe du navigateur résoudre le texte à scripts mélangés en ligne. Concrètement :

- `<html lang="en">` (ou contenu dominant en anglais) → laissez `--serif` sur la pile EN. Les glyphes CJK qui apparaissent en ligne tomberont jusqu'au repl Han système.
- `<html lang="zh-CN">` → remplacez `--serif` par la pile CN sur `:root` ou sur `html[lang="zh-CN"]`. Les glyphes latins s'affichent via la queue Georgia de la pile.
- `<html lang="ja">` → remplacez `--serif` par la pile JA et appliquez le remplacement de couleur de texte `--olive: #4d4c48` (les traits de YuMincho sont plus fins ; l'olive standard paraît pâle sur parchemin).
- Artefacts multilingues (ex. une présentation avec un chapitre japonais) : définissez la pile de langue dominante sur `:root`, puis portez le remplacement sur un élément wrapper (`section[lang="ja"] { --serif: …; }`). N'enchaînez **pas** les trois familles à l'intérieur d'un seul `font-family` — cela dilue le caractère visuel de chaque page.

### Hiérarchie (écran, px)

Le tableau de hiérarchie ci-dessous est dimensionné pour **les pages web rendues à l'écran** (CV, page unique, portfolio affichés en largeur bureau). Pour d'autres surfaces, mettez à l'échelle à partir de la base en points d'impression en utilisant ces ratios — les mêmes règles que le modèle kami `slides.py` applique :

| Surface | Jetons macro (police, padding) | Jetons micro (bordure, rayon, espacement) |
|---|---|---|
| Page / artefact web (page unique, CV, livre blanc) | points d'impression × ~1,33 | points d'impression × 1 |
| Diapositive / présentation 1920×1080 | points d'impression × ~1,6 | points d'impression × ~0,6 |

Concrètement : un H1 de 22 points en impression devient ~29px sur une page web et ~36px sur une diapositive ; une valeur d'espacement de lettres de 8 points qui paraît confiante en impression tombe à ~5px sur une diapositive. L'espacement des lettres utilise toujours le ratio micro de la diapositive — l'espacement d'impression appliqué à l'échelle diapositive se désintègre.

| Rôle | Famille | Taille | Poids | Interligne | Espacement des lettres | Notes |
|------|--------|------|--------|-------------|----------------|-------|
| Héros / Affichage | serif | 96–106px | 500 | 1,05–1,10 | -1,2px | Un par page max — couverture ou héros de page unique |
| Affichage CN/JA | serif | 48–64px | 500 | 1,10–1,12 | 0–0,3px | Les glyphes CJK ont besoin d'un espacement plus lâche et d'une taille absolue plus petite |
| Titre de section | serif | 28–32px | 500 | 1,20 | 0,4px | Ancre un chapitre ; précédé du numéro de section |
| H2 | serif | 22px | 500 | 1,25 | 0 | Sous-section |
| H3 | serif | 17–18px | 500 | 1,30 | 0 | Titre d'élément, en-tête de carte |
| Manifesto / citation extraite | serif | 20px | 400 | 1,65 | 0,05em | Le seul endroit où l'espacement des lettres mérite sa place |
| Lede | serif | 15–16px | 500 | 1,55 | 0 | Paragraphe d'introduction sous un titre de section |
| Corps | serif | 14px | 400 | 1,55 | 0 (EN) · 0,35px (CN) · 0,02em (JA) | Corps de lecture |
| Corps dense | serif | 13–14px | 400 | 1,40–1,45 | 0 | CV, page unique, listes denses |
| Légende | serif | 12px | 500 | 1,45 | 0 | Notes, légendes de figure |
| Sourcil / surtitre | sans | 12px | 500 | 1 | 1,2px, **MAJUSCULES** | Sourcil de section, sélecteur, en-tête méta |
| Étiquette | sans | 12px | 500 | 1,35 | 0,4px, majuscules | Petite étiquette en ligne, bleu encre si active |
| Mono / spécification | mono | 12–13px | 400 | 1,55 | 0,4px | Codes hex, spécifications de police, code |

### Règles de poids
- Le serif utilise **uniquement les poids 400 et 500**. Pas de 600, pas de 700, pas de 900.
- `strong { font-weight: 500 }` est explicitement défini afin que les navigateurs ne synthétisent pas le gras.
- Les étiquettes sans peuvent utiliser 500 ou 600 à petites tailles pour la lisibilité.
- **Pas d'italique nulle part.** Pas de `font-style: italic`. Si l'accent est nécessaire, changez la couleur en bleu encre ou entourez d'une balise.

### Interligne
- Titre serré : 1,10–1,30 (affichage, H1, H2)
- Corps dense : 1,40–1,45 (CV, page unique, listes denses)
- Corps de lecture : 1,50–1,55 (chapitres de longue forme, lettres)
- Étiquette / légende : 1,30–1,40

Interdit : 1,6+ (rythme web, flotte hors de la page) et 1,0–1,05 (lignes entrent en collision sauf à très grandes tailles d'affichage).

### Espacement des lettres
- Corps EN : `0`
- Corps CN (TsangerJinKai02) : `0,35px` pour compenser la densité naturelle de la police
- Corps JA : `0,02em`
- Tout-majuscules surtitres et petites étiquettes (< 10pt) : +0,5 à +1,2px est obligatoire
- Affichage CJK à 24px+ : `0,2–1px` d'espace respiratoire optique
- Sur les diapositives, l'espacement est à peu près **la moitié** des valeurs d'impression — un espacement de 8px qui paraît confiant dans un deck imprimé se désintègre à l'échelle diapositive.

### Contextes à chiffres tabulaires

`font-variant-numeric: tabular-nums` est obligatoire partout où les chiffres kami s'empilent verticalement ou se situent à côté d'autres chiffres — les chiffres proportionnels déséquilibrés se lisent comme un bug de mise en page à la résolution d'impression. Appliquez-le à :

- Valeurs métriques (le grand chiffre bleu encre dans `.metric-value`) et toute ligne métrique côte à côte
- Pieds de page et compteurs de diapositive (`02 / 05## 4. Styles de composants

### Cartes / Conteneurs
```css
background: var(--ivoire);             /* jamais parchemin — les cartes s'élèvent d'un ton */
border: 1px solid var(--bordure);
border-radius: 8px;                   /* par défaut ; cartes en vedette 12px ; héros 16–24px */
padding: 28px 28px 24px;              /* intérieur du composant */
transition: box-shadow 0.2s;
/* Le survol élève uniquement via une ombre discrète — pas de transformation, pas de modification de luminosité */
&:hover { box-shadow: 0 4px 24px rgba(0,0,0,0.05); }
```

### Boutons
```css
.btn-primary {
  background: var(--marque);                    /* #1B365D */
  color: var(--ivoire);
  box-shadow: 0 0 0 1px var(--marque);          /* ombre de bordure comme contour */
  padding: 8px 14px;
  border-radius: 8px;
  font: 500 12px/1 var(--sans);
  letter-spacing: 0.4px;
}
.btn-secondary {
  background: var(--sable-chaud);
  color: var(--foncé-chaud);
  box-shadow: 0 0 0 1px var(--bordure);
}
.btn-ghost {
  background: transparent;
  color: var(--marque);
  box-shadow: 0 0 0 1px var(--marque);
}
```

### Étiquettes / Puces
```css
.tag {
  font: 500 12px/1 var(--sans);
  padding: 2px 7px;
  border-radius: 2px;
  color: var(--marque);
  background: #EEF2F7;        /* hex solide, PAS rgba */
  letter-spacing: 0.4px;
}
.tag.standard { background: #E4ECF5; padding: 2px 8px; border-radius: 4px; }

/* Le seul gradient autorisé — voir §2 "Système de gradient".
 * Utilisez au plus une fois par page sur une étiquette "en vedette" ou "nouvelle". Le gradient
 * va du plus foncé au plus clair de gauche à droite pour que l'œil le lise comme une
 * aquarelle, pas un surbrillance de bouton. */
.tag.brush {
  background: linear-gradient(to right, #D6E1EE, #E4ECF5 70%, #EEF2F7);
}
```

```html
<!-- Exemple : une seule étiquette brush signalant le nouveau chapitre dans un document long -->
<span class="tag brush">Nouveau · Édition 02</span>
```

### Citation
```css
.quote {
  border-left: 2px solid var(--marque);
  padding: 4px 0 4px 14px;
  font: 500 15px/1.55 var(--serif);
  color: var(--olive);
}
```

### Motif de titre de section
```html
<div class="section-head">
  <p class="section-num">01</p>            <!-- bleu-encre, 14px serif, espacement 0.4px -->
  <h2 class="section-title">Couleur</h2>     <!-- 32px serif 500 -->
  <p class="section-lede">Description facultative d'une ligne en olive.</p>
</div>
```
Le numéro est défini dans le même serif que le titre, en bleu-encre, de la même taille que le texte de légende. Il n'y a pas de soulignement, de barre gauche, ni de sourcil — le numéro *est* le marqueur.

### Métriques
```html
<div class="metric">
  <div class="metric-value">8.4×</div>     <!-- serif 500 24px bleu-encre, tabular-nums -->
  <div class="metric-label">expédition plus rapide</div> <!-- serif 12px olive -->
</div>
```
Les nombres sont toujours définis dans `font-variant-numeric: tabular-nums` pour que les métriques adjacentes s'alignent.

### Listes
```css
ul.dash {
  list-style: none; padding: 0;
}
ul.dash li {
  position: relative; padding-left: 14px;
}
ul.dash li::before {
  content: "\2013";          /* trait d'union long, bleu-encre */
  position: absolute; left: 0;
  color: var(--marque);
}
```
Les puces sont des traits d'union longs en bleu-encre, jamais des disques pleins.

### Bloc de code
```css
.code {
  background: var(--ivoire);
  border: 1px solid var(--bordure);
  border-radius: 6px;
  padding: 12px 14px;
  font: 12px/1.55 var(--mono);
  color: var(--presque-noir);
  white-space: pre;
}
.code .k { color: var(--marque); }   /* mot-clé */
.code .c { color: var(--pierre); }   /* commentaire */
```

## 5. Principes de mise en page

### Géométrie de page (impression A4)

| Document | Haut | Droite | Bas | Gauche |
|---|---|---|---|---|
| CV (dense) | 11mm | 13mm | 11mm | 13mm |
| Page unique | 15mm | 18mm | 15mm | 18mm |
| Document long | 20mm | 22mm | 22mm | 22mm |
| Lettre | 25mm | 25mm | 25mm | 25mm |
| Portfolio | 12mm | 15mm | 12mm | 15mm |

Règle : **plus dense = marges plus petites, plus formel = marges plus grandes.**

### Pages Web / écran
- Largeur maximale du contenu : `1120px`, centrée, avec `padding: 88px 64px 120px` sur desktop.
- Espacement des sections : `72px` entre les sections de premier niveau.
- Colonnes de grille de cartes : 2 par défaut sur desktop ; passe à 1 en dessous de 768px.
- Colonnes de table dimensionnées en px absolus ( pas % ), pour que les kami tables ne se reflucent pas en spaghettis.

### Diapositives (1920×1080)
- Marge de base sur quatre côtés : `--slide-pad: 80px`.
- Marge supérieure d'une diapositive de contenu : 72–80px (impression 96–120px ; les diapositives sont plus compactes).
- Le dimensionnement suit les ratios de surface de §3 ("Hiérarchie") : jetons macro × 1,6, jetons micro × 0,6 par rapport à la base de l'impression pt.
- Les diapositives de couverture et de chapitre peuvent inverser le fond en bleu-encre (`#1B365D`) avec texte ivoire ; tout le reste reste sur parchemin.

## 6. Profondeur & Élévation

Trois niveaux autorisés — c'est tout le système :

| Niveau | Traitement | Utilisation |
|-------|-----------|-----|
| Plat (0) | Pas d'ombre, pas de bordure | Texte corps, manifeste, paragraphes sur parchemin |
| Bordure (1) | `1px solid var(--bordure)` ou `0 0 0 1px var(--marque)` | Cartes, boutons principaux, bords de table |
| Murmure (2) | `0 4px 24px rgba(0,0,0,0.05)` | Cartes survolées, conteneurs héros élevés, captures d'écran |

Interdit :
- Ombres dures (`0 12px 40px rgba(0,0,0,0.25)` et similaire) — la page est du papier, pas un panneau UI
- Néomorphisme, verrucisme, flous de fond
- Ombres composites multicouches

### Échelle de rayon de bordure
`2px → 4px → 6px → 8px (par défaut) → 12px → 16px`. Les étiquettes ont un rayon de 2–4px, les boutons et cartes de 8px, les conteneurs en vedette / héros de 12–16px. Tout ce qui dépasse 16px est réservé aux visuels de diapositives de couverture.

## 7. À faire et à ne pas faire

### À faire
- Utiliser du parchemin (`#f5f4ed`) comme fond de page — la crème chaude *est* la personnalité kami.
- Utiliser un seul poids de serif (500) pour chaque titre ; laisser la taille porter la hiérarchie.
- Utiliser le bleu-encre (`#1B365D`) uniquement pour les CTA principaux, numéros de section, liens, la règle gauche d'une citation, et le W500 dans les métriques.
- Garder chaque gris chaud (teinte jaune-brun). En cas de doute, échantillonnez avec `R ≈ G > B`.
- Utiliser des ombres de bordure ou des ombres de murmure pour l'élévation ; jamais de ombres dures.
- Définir les fonds d'étiquette comme hex pré-mélangé sur parchemin, jamais `rgba()`.
- Définir les nombres dans `font-variant-numeric: tabular-nums`.
- Apparier le numéro de section avec le titre de section dans le même serif — pas de sourcil nécessaire.
- Définir les puces par défaut sur des traits d'union longs en bleu-encre (`–`).

### À ne pas faire
- Ne pas utiliser `#ffffff` comme fond de page, n'importe où.
- Pas introduire une seconde couleur d'accent ou un chromatique gradient.
- Ne pas utiliser des bleu-gris froids (`slate-*`, `#f3f4f6`, `#6b7280`). Chaque neutre est chaud.
- Ne pas utiliser le gras (700+) sur serif — le poids 500 est le maximum.
**Ne pas utiliser l'italique nulle part.** Pas de `font-style: italic`. Remplacez par bleu-encre ou une étiquette à la place.
- Ne pas utiliser du sans-serif pour les titres ou le corps — le sans est réservé aux sourcils, commutateurs et petites étiquettes (et la pile sans littéralement égale à la pile serif).
- Ne pas descendre en dessous de 1.4 ou monter au-dessus de 1.55 pour la hauteur de ligne du corps — cette gamme *est* le rythme de lecture kami.
- Ne pas utiliser de puces en disque rond, d'ombres portées ou de puces en forme de pilule avec de lourds bords.
- Ne pas appliquer `backdrop-filter`, `mix-blend-mode`, ou autre truc de compositage moderne — le système cible la fidélité d'impression.## 8. Comportement Responsive

### Points de rupture

| Nom | Largeur | Modifications principales |
|------|-------|-------------|
| Téléphone | < 768px | Colonne unique. Hero 46px, titre de section 24px, manifeste 17px. Le padding des cartes passe à 20px 16px. Masquer la ligne `.hero-tokens`. |
| Tablette | 768–979px | La plupart des grilles 2-colonnnes sont maintenues ; passer les teintes de tags de 5 à 3 colonnes. |
| Bureau | ≥ 980px | Grilles complètes 2-colonnes / 4-colonnes, JA obtient des règles de secours `white-space: nowrap` sur les chapeaux longs. |

### Cibles tactiles
- Les boutons conservent un padding minimum de `8 14px`.
- Les cibles tactiles restent au-dessus de 44×44 en donnant aux cartes un padding interne généreux plutôt qu'en surdimensionnant le chrome.

### Impression
- `@page { size: A4; margin: 14mm 16mm; background: #f5f4ed; }`.
- Section, hero, famille, comp, échantillon, teinte, citation, blockquote, pre, tr, blocs anti-pattern utilisent tous `break-inside: avoid` pour que les pages kami ne se cassent pas au milieu d'une carte.
- `-webkit-print-color-adjust: exact` est requis pour que l'arrière-plan parchemin atteigne réellement le papier.

## 9. Guide de Prompt pour Agent

### Référence rapide des couleurs
- Arrière-plan de page : "Parchemin (#f5f4ed)"
- Surface de carte : "Ivoire (#faf9f5)"
- Marque / CTA : "Bleu Encre (#1B365D)"
- Texte primaire : "Noir Proche (#141413)"
- Texte secondaire : "Chaud Foncé (#3d3d3a)"
- Sous-texte / Légende : "Olive (#504e49)"
- Tertiaire / Métadonnées : "Pierre (#6b6a64)"
- Bordure : "Bordure (#e8e6dc)"
- Remplissage de tag (par défaut) : "#E4ECF5 solide (PAS rgba)"

### Exemples de prompts de composants
- "Construire un kami hero sur une page unique sur Parchemin (#f5f4ed). Ligne de sourcil en 12px sans majuscules Pierre (#6b6a64), letter-spacing 1.2px. Titre en serif 500 à 96px Noir Proche (#141413), line-height 1.05, letter-spacing -1.2px. Slogan en dessous en serif 500 à 21px Olive."
- "Designer un en-tête de section kami. Une empilement de deux lignes : numéro de section `01` en serif 500 à 14px Bleu Encre (#1B365D) tracking 0.4px, puis le titre en serif 500 à 32px Noir Proche. Chapeau optionnel en serif 500 à 16px Olive."
- "Rendre une ligne de métriques kami de trois métriques. Chaque métrique est une paire verticale : valeur en serif 500 à 24px Bleu Encre avec `font-variant-numeric: tabular-nums`, étiquette en 12px Olive. Espacement entre les métriques : 28px."
- "Construire une carte kami sur Ivoire (#faf9f5) avec 1px Bordure (#e8e6dc), 8px rayon, 28px padding. Titre en serif 500 à 16px Noir Proche. Indication en dessous en 12px mono Pierre. Au survol, ajouter une ombre chuchotée `0 4px 24px rgba(0,0,0,0.05)`. Pas de transform, pas de changement de couleur."
- "Construire une couverture de diapositive kami à 1920×1080. Arrière-plan bleu-encre (#1B365D). Titre centré en serif 500 à 96px Ivoire (#faf9f5). En dessous, une règle ivoire de 1px, largeur 96px. Auteur et date en dessous en serif 500 à 18px Ivoire à 70% d'opacité."

### Guide d'itération
1. **Commencer par vérifier la température du gris.** Si un gris paraît froid, le design n'est plus kami. Remplacer par la rampe chaude.
2. **Auditer l'accent.** Si le bleu-encre couvre plus de ~5% de la surface visible, réduire - pousser les éléments vers Olive ou Chaud Foncé.
3. **Auditer le poids.** Tout poids au-dessus de 500 sur serif est faux. Remplacer par le poids 500 et laisser la taille porter le contraste.
4. **Auditer l'italique.** Aucun italique, jamais. Passer à la couleur bleu-encre ou à un petit tag.
5. **Auditer les ombres.** Si une ombre est visible à première vue, elle est trop forte. Les seules ombres sont les anneaux de 1px et le `0 4px 24px rgba(0,0,0,0.05)` chuchotement.
6. **Les remplissages de tag doivent être hex solides.** Si vous avez écrit `rgba(27, 54, 93, 0.18)`, remplacer par `#E4ECF5`.
7. **Nombres tabular-nums.** Toute colonne de nombres sans `font-variant-numeric: tabular-nums` paraîtra fausse sur un rendu d'impression.
8. **Pour le travail de diapositive, diviser le tracking par deux et mettre à l'échelle les jetons macro par 1.6.** Le rythme d'impression est trop lâche à 1920×1080 sans cet ajustement.

## Attribution

L'inspiration esthétique tirée de [tw93/kami](https://github.com/tw93/kami) (MIT, © Tw93 et contributeurs). kami est une compétence Claude pour la mise en page de documents professionnels et de présentations ; les jetons, les règles de typographie et les "dix invariants" ci-dessus adaptent son langage de design orienté impression pour une utilisation en tant que système de design Open.
