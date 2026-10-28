# Brief : Flux Créatif (Documents Longue Conception)

**Quand utiliser ce brief :** Documents textuels lourds qui ont besoin d'une touche de design mais dont le contenu s'écoule naturellement à travers les pages — guides, manuels, catalogues, introductions, collections, manuels illustrés. Le contenu est la star ; le design soutient la lisibilité.

**Comment il diffère de `creative.md` :** `creative.md` (Mode Plan) traite chaque page comme une toile visuelle autoportée de taille fixe. Ce brief permet au contenu de s'écouler continuellement, avec le `@page` de Chromium qui s'autopagine automatiquement aux limites de page.

**→ DOIT LIRE : `typesetting/overflow.md`** pour les modèles de dépassement spécifiques à Playwright/HTML.

---

## Principe Fondamental : Le Contenu S'écoule, le Design Enveloppe

Vous écrivez directement du HTML/CSS brut (pas de Plan JSON, pas de `design_engine.py`). Le document est un corps HTML continu, et le moteur d'impression du navigateur le divise automatiquement en pages.

**⚠️ Règle de fer : Toutes les conversions HTML→PDF DOIVENT utiliser `html2pdf-next.js` — n'écrivez PAS de scripts Python Playwright personnalisés.** Il gère automatiquement l'injection @page, la détection de dépassement, l'attente des polices, le rendu Mermaid/KaTeX, les métadonnées PDF, etc.

```bash
node "$PDF_SKILL_DIR/scripts/html2pdf-next.js" input.html --output output.pdf --width 720px --height 1020px
```

---

## Modèle de Pagination

### Les Règles de Fer

1. **PAS de hauteur fixe sur les conteneurs de contenu.** Laissez le contenu s'écouler naturellement. Le navigateur décide où couper les pages.
2. **PAS de divs `.page` pour les sections de contenu.** Utilisez un seul `<div class="main-content">` avec un padding pour tout le contenu du corps.
3. **PAS de `break-before: page` entre les sections de contenu.** C'est la cause n°1 des espaces vides — quand la section précédente ne remplit pas une page, le reste devient un vide. Utilisez `margin-top` pour la séparation visuelle des chapitres à la place.
4. **`break-inside: avoid`** sur les cartes individuelles, éléments et entrées de guide pour les empêcher d'être divisés entre plusieurs pages.
5. **`break-after: avoid`** sur les en-têtes de chapitre (groupe étiquette + titre + séparateur) pour les garder attachés au premier bloc de contenu ci-dessous.
6. **Conteneurs de hauteur fixe SEULEMENT pour les pages de couverture et de fin** qui doivent occuper une page entière :

```css
/* Couverture : hauteur fixe, page autonome */
.cover {
    width: 720px;
    height: 1020px;
    box-sizing: border-box;
    break-after: page;
    overflow: hidden;  /* OK ici — ne coupe que les éléments décoratifs sur la couverture uniquement */
    /* ⚠️ Utilisez justify-content: center (PAS flex-end) pour éviter un vide en haut trop important */
    /* Ajoutez des éléments décoratifs (cercles, lignes) + étiquette d'édition en bas pour l'équilibre visuel */
}

/* Fin : hauteur fixe, page autonome */
.ending {
    width: 720px;
    height: 1020px;
    box-sizing: border-box;
    break-before: page;
    overflow: hidden;
}

/* Contenu : s'écoule naturellement, PAS de hauteur fixe */
.main-content {
    padding: 60px 65px 40px 65px;
    /* PAS de propriété height */
    /* PAS de overflow: hidden */
}
```

### Ce Qu'il Ne Faut PAS Faire (Erreurs Courantes)

| Erreur | Pourquoi ça casse | Correction |
|--------|------------------|------------|
| `.content { height: 1020px; }` | Le contenu qui dépasse la hauteur est coupé ou déborde | Supprimez la hauteur fixe |
| Plusieurs `<div class="content">` chacun avec `padding: 60px` | Double padding (60+60=120px) entre sections crée des vides | Un seul conteneur, chapitres séparés par `margin-top` |
| `break-before: page` sur les en-têtes de chapitre | Le chapitre précédent ne remplit pas la page → espace vide avant le nouveau chapitre | Utilisez `margin-top: 36px` à la place |
| `overflow: hidden` sur le conteneur de contenu | Coupe le contenu aux limites de page | N'utilisez que sur les couvertures/fins de hauteur fixe |
| `justify-content: flex-end` sur la couverture | Le titre descend en bas, 60%+ de vide en haut | Utilisez `center` + ancres décoratives pour l'équilibre |
| Chapitre avec < 3 paragraphes de contenu | Laisse une demi-page vide avant le chapitre suivant | Écrivez suffisamment de contenu pour remplir au moins 50% d'une page |
| `margin-top: 50px+` sur les chapitres | Se combine avec `break-inside: avoid`, crée de grands vides | Gardez le `margin-top` de chapitre ≤ 30px |

---

## Modèle CSS

```css
@page {
    size: 720px 1020px;   /* Valeurs px concrètes — les variables CSS NE SONT PAS prises en charge dans @page */
    margin: 0;
}
:root {
    --c-bg: #0d0d0d;
    --c-text: #e8e6e3;
    --c-accent: #ff4757;
}
html, body {
    margin: 0;
    padding: 0;
    width: 720px;
    background: var(--c-bg);
    color: var(--c-text);
    font-family: 'Noto Sans SC', sans-serif;
}
@media screen {
    html {
        height: auto;
        display: flex;
        justify-content: center;
        background: #222;
    }
    body {
        transform-origin: top center;
        margin: 20px auto;
    }
}
```

**⚠️ Les règles @page NE RÉSOULENT PAS les variables CSS** (`var(--x)` est ignoré silencieusement, retombe sur A4). Utilisez toujours des valeurs `px` concrètes dans `@page`.

---

## Modèle de Structure HTML

```html
<body>

<!-- Couverture : hauteur fixe, occupe une page entière -->
<div class="cover">
    <div class="tag">CATÉGORIE</div>
    <div class="title">Titre du Document</div>
    <div class="subtitle">Texte descriptif</div>
</div>

<!-- Tout le contenu du corps dans UN SEUL conteneur continu -->
<div class="main-content">

    <!-- Chapitre 1 -->
    <div class="section-tag">Chapitre 1</div>
    <div class="section-title">Titre</div>
    <div class="divider"></div>
    <div class="body-text">Contenu du paragraphe...</div>
    <div class="body-text">Plus de paragraphes...</div>

    <!-- Chapitre 2 : séparé par margin-top, PAS break-before -->
    <div class="chapter-header">
        <div class="section-tag">Chapitre 2</div>
        <div class="section-title">Titre</div>
        <div class="divider"></div>
    </div>

    <!-- Cartes / éléments avec break-inside: avoid -->
    <div class="card">Contenu de la carte...</div>
    <div class="card">Contenu de la carte...</div>

</div>

<!-- Fin : hauteur fixe, occupe une page entière -->
<div class="ending">
    <div class="big-text">Texte de clôture</div>
</div>

</body>
```

CSS clé pour les en-têtes de chapitre et les cartes :
```css
.chapter-header {
    break-after: avoid;    /* Garde l'en-tête avec le premier bloc de contenu */
    break-inside: avoid;
    margin-top: 28px;      /* ≤ 30px ! Les valeurs plus grandes se combinent avec break-inside: avoid → pages vides */
}
.card {
    break-inside: avoid;   /* Ne divise pas une seule carte entre plusieurs pages */
    margin-bottom: 14px;   /* ≤ 16px ! Chaque px de marge est un espace perdu si la carte est poussée à la page suivante */
}
```

---

## Règle de Fond du Corps du Document

Définissez `html, body { background }` sur la couleur dominante/la plus foncée du document. Cela empêche les artéfacts d'écart sous-pixel entre le contenu et les limites de page.

- Toutes les pages de même couleur sombre → `body { background: <cette couleur> }`
- Couverture sombre mélangée + corps clair → `body { background: <couleur la plus foncée> }` (le corps sombre est invisible sous les pages de contenu blanc)
- Toutes les pages blanches/claires → `body { background: <fond de contenu le plus clair> }` (ex: `#f8fafc`)

---

## Règles Communes avec creative.md

Les règles suivantes s'appliquent identiquement aux deux pipelines Creative Flow et Creative Blueprint :

### Sécurité d'Encodage de Caractères
N'utilisez jamais les kana japonais (の, が, は), les symboles rares ou les caractères de la Zone d'Utilisation Privée. Ils se corrompent en U+FFFD (�) pendant le transit LLM→écriture fichier→lecture. Remplacez par des équivalens chinois simples : `の`→`之/的/缔`.

### Texte Chinois Vertical
Lors de l'utilisation de `writing-mode: vertical-rl` :
```css
writing-mode: vertical-rl;
text-orientation: upright;
white-space: nowrap;
letter-spacing: 12px;
```

### Couverture de Police
Pour le contenu CJK, chargez toujours Google Fonts via la balise `<link>` dans `<head>` (PAS `@import`) :
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">
```

### Vérification de Texte Post-Génération
Après que Playwright a rendu le PDF, extrayez le texte et scannez pour `?` ou `\ufffd`. Si trouvé, corrigez les caractères corrompus par l'encodage dans le source HTML.

### Validation Pré-Rendu HTML (OBLIGATOIRE)
Avant d'appeler `html2pdf-next.js`, exécutez le validateur :
```bash
python3 "$PDF_SKILL_DIR/scripts/poster_validate.py" check-html <file>.html
```
- **ERROR** → doit être corrigé avant génération PDF. Utilisez `--fix --output <file>.html` pour la réparation automatique.
- **WARNING** → examinez et corrigez si approprié.

---

## Liste de Contrôle Qualité — Flux Créatif

### Mise en Page & Pagination
- [ ] **Pas de hauteur fixe sur les conteneurs de contenu** (seulement pages de couverture/fin)
- [ ] **Pas de `break-before: page` entre les sections de contenu**
- [ ] **`break-inside: avoid`** sur toutes les cartes/éléments/entrées de guide
- [ ] **Les en-têtes de chapitre ont `break-after: avoid`** pour rester avec le premier bloc de contenu
- [ ] **Un seul `<div class="main-content">** enveloppe tout le contenu du corps
- [ ] **Pas de double padding** entre les sections (un seul conteneur, pas plusieurs)

### Pleine Page & Arrière-plan
- [ ] **`@page { margin: 0 }`** avec des valeurs de taille px concrètes
- [ ] **`html, body { margin: 0; padding: 0 }`**
- [ ] **L'arrière-plan du corps correspond à la couleur de page dominante**
- [ ] **Pas d'artéfact blanc sur les bords** sur les pages sombres

### Conception de Page de Couverture
- [ ] **Couverture `justify-content: center`** (pas `flex-end`) — `flex-end` pousse le contenu vers le bas et laisse 60%+ de vide en haut, rendant la page vide
- [ ] **Ajoutez des ancres visuelles** pour remplir la couverture : éléments décoratifs (cercles, lignes), étiquette édition/date en bas, badge en haut. Une couverture avec seulement titre+sous-titre paraîtra creuse.
- [ ] **Padding de couverture ≤ 70px** — un padding excessif réduit encore plus l'empreinte visuelle

### Densité de Contenu (Anti-Page Vide)
- [ ] **Chaque chapitre doit avoir suffisamment de contenu pour remplir au moins 50% d'une page.** Si un chapitre (texte + citation + cartes) occupe < 50% d'une page, il laissera une grande zone vide avant le chapitre suivant. Solution : étendez le contenu (ajoutez 1-2 paragraphes supplémentaires, exemples ou contexte).
- [ ] **`margin-top` de chapitre ≤ 30px.** Des valeurs plus grandes (50px+) se combinent avec `break-inside: avoid` sur les cartes, poussant le contenu à la page suivante et laissant des vides sur la page actuelle.
- [ ] **`margin` de carte/encart ≤ 16px.** Chaque pixel de marge verticale à l'intérieur d'un bloc `break-inside: avoid` est un espace qui ne peut pas être récupéré si le bloc est poussé à la page suivante.
- [ ] **Après génération PDF, vérifiez visuellement chaque page** pour un vide de fin >30%. Si trouvé, soit : (a) ajoutez plus de contenu à ce chapitre, (b) réduisez marges/padding, ou (c) réordonnez les éléments pour qu'un bloc plus petit remplisse l'écart.

### Qualité de Conception
- [ ] **Document entier ≤ 5 couleurs** : Primaire + secondaire + accent + neutre + arrière-plan
- [ ] **2 familles de polices maximum** : Au plus 2 familles de polices
- [ ] **Éléments décoratifs ≤ 3 par page** (couverture exempte)
- [ ] **Pas d'images de stock / clipart / décorations générées par IA** sauf si fournies par l'utilisateur

### Sortie
- [ ] **PDF Vectoriel** via `html2pdf-next.js` (pas de capture d'écran)
- [ ] **Fichier source HTML** livré avec le PDF
- [ ] **Métadonnées PDF** définies via `pdf.py meta.brand`
- [ ] **QA passé** via `pdf_qa.py --no-tables`
