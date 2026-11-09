# Référence des composants · Components

C'est le manuel des composants du skill `magazine-web-ppt`. template.html définit déjà tous les styles ; ici, uniquement « à quoi ressemble ce composant, comment l'utiliser ».

## Sommaire

- [Coque de Slide de base](#coque-de-slide-de-base)
- [Typographie](#typographie)
- [Chrome & Foot](#chrome--foot)
- [Callout, cadre de citation](#callout-cadre-de-citation)
- [Stat, matrice de chiffres](#stat-matrice-de-chiffres)
- [Platform, carte de plateforme](#platform-carte-de-plateforme)
- [Rowline, ligne de tableau](#rowline-ligne-de-tableau)
- [Pillar, carte pilier](#pillar-carte-pilier)
- [Tag & Kicker](#tag--kicker)
- [Figure, cadre d'image](#figure-cadre-dimage)
- [Icônes](#icônes)
- [Ghost, caractère géant de fond](#ghost-caractère-géant-de-fond)
- [Highlight, surlignage](#highlight-surlignage)

---

## Coque de Slide de base

Chaque page est un `<section class="slide ...">`. L'attribut `data-theme` (`light` ou `dark`) est obligatoire : le JS de pagination bascule le fond selon cet attribut.

```html
<section class="slide light" data-theme="light">   <!-- page claire -->
<section class="slide dark" data-theme="dark">     <!-- page sombre -->
<section class="slide light hero" data-theme="light">  <!-- page Hero : claire + voile fin laissant passer le WebGL -->
<section class="slide dark hero" data-theme="dark">    <!-- page Hero : sombre + voile fin -->
```

**Usage de light vs dark : alterner**, changer de thème toutes les 2-3 pages, éviter plus de 3 pages consécutives du même ton. Au passage d'une page, le fond WebGL fond automatiquement d'un shader à l'autre.

**Usage de la classe hero** : uniquement pour les pages à dominante visuelle (couverture, page de citation, transition de chapitre, fin). Avec `hero`, le voile descend à 12-16 % et le fond WebGL transparaît largement — ne pas surcharger une page hero de texte.

---

## Typographie

La répartition typographique est LA règle la plus importante de ce gabarit ; tout mélange est interdit.

| Class | Usage | Police |
|---|---|---|
| `.display` | très grand anglais (pages Hero) | Playfair Display 700, 11vw |
| `.display-zh` | très grand titre chinois | Noto Serif SC 700, 7.8vw |
| `.h1-zh` | titre principal de page | Noto Serif SC 700, 4.6vw |
| `.h2-zh` | sous-titre | Noto Serif SC 600, 3.2vw |
| `.h3-zh` | titre d'étape de pipeline | Noto Serif SC 500, 1.9vw |
| `.lead` | paragraphe d'appel (plus grand que body) | Noto Serif SC 400, 1.9vw |
| `.body-zh` | **corps/description (sans-serif)** | Noto Sans SC 400, 1.22vw |
| `.body-serif` | corps (serif) | Noto Serif SC 400, 1.3vw |
| `.kicker` | indicatif de section (au-dessus du titre) | IBM Plex Mono, 12px uppercase |
| `.meta` | étiquettes de métadonnées | IBM Plex Mono, 0.88vw uppercase |
| `.big-num` | chiffre géant | Playfair Display 800, 10vw |
| `.mid-num` | chiffre moyen | Playfair Display 700, 5.5vw |

**Règles fondamentales** :
- **Serif** (`serif-zh` / `serif-en`) : titres, citations fortes, chiffres — pour « l'accent visuel »
- **Sans-serif** (`sans-zh`) : descriptions, longs contenus de lecture — pour « la densité d'information »
- **Monospace** (`mono`) : étiquettes anglaises de kicker, meta, foot — pour « le rythme décoratif »

**Techniques d'emphase** :
- `<em class="en">mot anglais</em>` — rend le mot anglais en Playfair Display italique (très élégant)
- `<em style="opacity:.65">groupe de mots</em>` — estompe la fin d'un titre pour créer du rythme

---

## Chrome & Foot

Les bandeaux de métadonnées en haut et en bas de chaque page. Presque toutes les pages devraient les porter.

```html
<div class="chrome">
  <div class="left">
    <span>Acte I · Données dures</span>
    <span class="sep"></span>
    <span>Act I</span>
  </div>
  <div class="right"><span>02 / 27</span></div>
</div>

<!-- ... corps de la page ... -->

<div class="foot">
  <div class="title">Nom du projet · CodePilot　|　github.com/codepilot</div>
  <div>Act I · Dev Numbers</div>
</div>
```

**Règles** :
- `chrome.right` porte toujours la pagination `NN / TOTAL` (TOTAL = nombre de pages)
- `foot.title` est le libellé français, `foot.right` le marqueur d'acte en anglais
- chrome et foot constituent ensemble l'« en-tête / pied de page » façon magazine

---

## Callout, cadre de citation

Pour citations fortes / idées clés / propos rapportés.

```html
<div class="callout" style="max-width:80vw">
  <div class="q-big">« Ça, il y a trois ans,<br>il fallait une équipe de dix pendant un an. »</div>
  <span class="cite">— le jugement d'un observateur</span>
</div>
```

Variantes :
- Sans cite : retirer simplement `<span class="cite">`
- Citation anglaise : `<em class="en">"Thin Harness, Fat Skills."</em>`
- Sur une page hero : ajouter `style="position:relative;z-index:2"` sur le conteneur (pour ne pas être couvert par le voile de fond)

---

## Stat, matrice de chiffres

Pour présenter des indicateurs, souvent associé à `.grid-6` / `.grid-4`.

```html
<div class="grid-6">
  <div class="stat">
    <span class="m">Duration</span>
    <span class="n">64<em style="font-size:.4em;opacity:.5;font-style:normal"> jours</em></span>
    <span class="l">de 0 à aujourd'hui</span>
  </div>
  <!-- ... autres stats ... -->
</div>
```

Structure en trois segments : `.m` petite étiquette monospace → `.n` chiffre géant → `.l` description. L'unité après le chiffre, dans un `<em>` réduit à 0.4em, opacité 0.5.

**Conteneurs de mise en page usuels** :
- `.grid-6` — grille 3×2 (la plus courante, 6 stats)
- `.grid-4` — grille 2×2 (4 stats)
- `.grid-3` — 3 colonnes sur une ligne (3 stats / pillars)

---

## Platform, carte de plateforme

Pour présenter une plateforme sociale / un canal + son audience.

```html
<div class="plat">
  <div class="sub">Weibo</div>
  <div class="name">微博</div>
  <div class="nb">289K</div>
</div>
```

Quatrième ligne optionnelle (note complémentaire) :
```html
<div class="body-zh" style="font-size:max(11px,.8vw);opacity:.5;margin-top:.6vh">
  synchronization Xiaolüshu incluse
</div>
```

**Variante « Also On »** (plateformes secondaires) :
```html
<div class="plat" style="border-top-style:dashed;opacity:.72">
  <div class="sub">Also On</div>
  <div class="body-zh" style="font-weight:600;margin-top:.8vh">
    Bilibili　·　Zhihu
  </div>
</div>
```

---

## Rowline, ligne de tableau

Contenus en liste, une entrée par ligne.

```html
<div class="rowline">
  <div class="k">CLAUDE.md</div>
  <div class="v">comment tu dois travailler — règles de conduite + préférences + interdits</div>
  <div class="m">EMPLOYEE · HANDBOOK</div>
</div>
```

Structure en trois colonnes : `.k` mot-clé serif · `.v` description corps · `.m` étiquette monospace (alignée à droite). Le premier et le dernier rowline reçoivent automatiquement les bordures hautes et basses.

**Variante 2 colonnes** : `style="grid-template-columns:1fr 3fr"` sans la colonne `.m`.

---

## Pillar, carte pilier

Structure en trois piliers, courante pour les pages « concepts en parallèle ».

```html
<div class="grid-3">
  <div class="pillar">
    <div class="ic">01</div>
    <div class="t">Système documentaire<br>à trois niveaux</div>
    <div class="d">CLAUDE.md<br>+ base de connaissances projet<br>+ fichiers garde-fous</div>
  </div>
  <!-- ... autres pillars ... -->
</div>
```

**Pillar avec icône (pages d'emphase)** :
```html
<div class="pillar" style="padding:4vh 2vw;border:1px solid currentColor;border-color:rgba(10,10,11,.2)">
  <div class="ic"><i data-lucide="compass" class="ico-lg"></i></div>
  <div class="t">Capacité de jugement</div>
  <div class="d">L'autorité des décisions et du cap.<br>Arbitrer, le goût, le sens de la direction.</div>
</div>
```

`.ic` peut être un numéro (`01 / 02 / 03` ou `A. / B. / C.`) ou une icône Lucide.

---

## Tag & Kicker

**Kicker** : petit indicatif au-dessus du titre (monospace, tout en capitales, petit corps) :
```html
<div class="kicker">64 derniers jours · volet développement</div>
<div class="h1-zh">Une seule personne, qu'a-t-elle fait.</div>
```

**Tag** : pastille étiquette autonome (avec bordure) :
```html
<div style="display:flex;gap:1.6vw;flex-wrap:wrap">
  <div class="tag">lever à 10 h</div>
  <div class="tag">sport le mardi / jeudi après-midi</div>
  <div class="tag">séries et jeux le soir, comme d'habitude</div>
</div>
```

---

## Figure, cadre d'image

**C'est le composant le plus piégeux du gabarit — respecter scrupuleusement les règles suivantes**.

### Structure de base

```html
<figure class="tile">
  <div class="frame-img" style="height:26vh">
    <img src="assets-img/xxx.png" alt="légende">
  </div>
  <figcaption class="frame-cap">
    <span class="pf">Twitter · Twitter</span>
    <span class="nb">137K</span>
  </figcaption>
</figure>
```

### Contraintes clés (leçons à la dure, ne pas violer)

1. **Fixer la hauteur avec `height:Nvh`**, jamais avec `aspect-ratio`.
   - Raison : dans une grille, aspect-ratio fait déborder le conteneur parent et les images s'empilent.
   - Tailles recommandées : `height:18vh` (bande compacte) / `22vh` (grille standard) / `26vh` (mise en valeur) / `28vh` (grande image).

2. **`object-position:top center` (déjà réglé dans le CSS)** : seule la partie basse peut être rognée.
   - Rogner les côtés ou le haut est strictement interdit — c'est la zone d'identité centrale de l'image.

3. **Plusieurs images en grille : utiliser une grid inline plutôt que `grid-3`** :
   ```html
   <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1vh 1.2vw">
     <figure class="tile">...</figure>
     <figure class="tile">...</figure>
     <figure class="tile">...</figure>
   </div>
   ```

4. **Aligner les images avec le reste de la mise en page** : ajouter `align-self:end` sur la figure pour caler l'image en bas.

### Variantes de Frame Caption

```html
<!-- Standard : nom à gauche, chiffre à droite -->
<figcaption class="frame-cap">
  <span class="pf">Twitter · Twitter</span>
  <span class="nb">137K</span>
</figcaption>

<!-- Avec numéro -->
<figcaption class="frame-cap">
  <span class="idx">01</span>
  <span class="pf">Retouche IA</span>
  <span>Polish</span>
</figcaption>
```

### Placeholder d'image (phase de conception)

Quand l'image n'est pas encore en place, utiliser un cadre en pointillés :
```html
<div class="img-slot r-4x3">  <!-- r-4x3 / r-16x9(default) / r-3x2 / r-1x1 -->
  <span class="plus">+</span>
  <span class="label">Emplacement capture GitHub</span>
</div>
```

---

## Icônes

**Les emoji sont strictement interdits.** Utiliser Lucide via CDN (déjà chargé dans template.html).

```html
<i data-lucide="compass" class="ico-lg"></i>     <!-- grande icône (pillar) -->
<i data-lucide="target" class="ico-md"></i>      <!-- icône moyenne (item de liste) -->
<i data-lucide="check-circle" class="ico-sm"></i>  <!-- petite icône (inline) -->
```

**Noms Lucide courants (groupés par sens)** :

- jugement : `compass`, `target`, `crosshair`, `search-check`
- relations : `share-2`, `users`, `network`, `link`, `handshake`
- marque : `crown`, `gem`, `award`, `star`, `badge-check`
- processus : `workflow`, `route`, `arrow-right-left`, `repeat`
- données : `grid-2x2`, `bar-chart-3`, `trending-up`, `activity`
- esthétique : `palette`, `brush`, `eye`, `sparkles`
- vrai/faux : `check-circle`, `x-circle`, `check`, `x`
- direction : `arrow-right`, `arrow-up-right`, `corner-down-right`

**Combinaison inline icône + texte** :
```html
<div class="h3-zh" style="display:flex;align-items:center;gap:.8em">
  <i data-lucide="target" class="ico-md"></i>
  Juger — ce qui mérite d'être écrit
</div>
```

---

## Ghost, caractère géant de fond

« Caractère décoratif de fond », opacité très faible, pour l'effet magazine.

```html
<div class="ghost" style="right:-6vw;top:-8vh">BUT</div>
<div class="ghost" style="left:-8vw;bottom:-18vh;font-style:italic">Harness</div>
```

- Corps 34vw, opacité 0.06
- Positionnements usuels : `right:-6vw;top:-8vh` (débordement en haut à droite) / `left:-8vw;bottom:-18vh` (en bas à gauche)
- Contenu : mot anglais ou chiffre (numéro de chapitre 01/02/03, mot-clé BUT/NOW/HERE)

**Attention** : sur une page avec ghost, les autres contenus doivent recevoir `position:relative;z-index:2` pour ne pas passer dessous.

---

## Highlight, surlignage

Effet « surligneur » sur un groupe de mots en ligne :

```html
<span class="hi">pas</span>
<span class="hi">une explosion unique</span>
```

Génère une bande de surlignage semi-transparente sous le texte. Bande claire sur thème sombre, bande sombre sur thème clair (géré par le CSS).

**Usages** : uniquement sur 1 à 3 mots-clés, jamais sur de grandes surfaces.
