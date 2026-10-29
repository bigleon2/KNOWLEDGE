# Liste de contrôle qualité (Checklist)

Cette liste vient des itérations réelles du PPT de partage « l'entreprise d'une seule personne ». Chaque point découle d'un piège rencontré, classé par importance.

Avant de générer le PPT, la lire en entier ; après génération, s'auto-contrôler point par point.

---

## 🔴 P0 · Les erreurs à ne jamais commettre

### 0. Contrôle des classes avant génération (le plus important)

**Symptôme** : coller tel quel le squelette de layouts.md dans un nouveau HTML fait perdre tous les styles — grands titres devenus sans-serif, grands chiffres en corps de texte, pipeline multi-pages en bouillie, images empilées en bas du navigateur.

**Cause racine** : si le `<style>` de `template.html` ne définit pas ces classes, le navigateur retombe sur ses styles par défaut.

**Conduite** :
- **Avant de générer, obligatoirement `Read` `assets/template.html`** et vérifier que les classes utilisées par layouts.md existent toutes
- Classes le plus souvent oubliées : `h-hero / h-xl / h-sub / h-md / lead / meta-row / stat-card / stat-label / stat-nb / stat-unit / stat-note / pipeline-section / pipeline-label / pipeline / step / step-nb / step-title / step-desc / grid-2-7-5 / grid-2-6-6 / grid-2-8-4 / grid-3-3 / frame / img-cap / callout-src`
- Si une classe manque réellement, **l'ajouter dans le `<style>` de template.html**, pas la réécrire en inline sur chaque page
- Après génération, ouvrir dans le navigateur : si « les grands titres sont en sans-serif » ou « les étapes du pipeline s'écrasent sur une ligne », c'est ce problème à ~100 %

### 1. Pas d'emoji comme icônes

**Symptôme** : dans le style magazine à la chinoise, des emoji (🎯 💡 ✅) cassent immédiatement le ton.

**Conduite** : utiliser la bibliothèque Lucide, référencée via CDN :

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
...
<i data-lucide="target" class="ico-md"></i>
...
<script>lucide.createIcons();</script>
```

Icônes courantes : `target / palette / search-check / compass / share-2 / crown / check-circle / x-circle / plus / arrow-right / grid-2x2 / network`

### 2. Les images ne peuvent être rognées qu'en bas ; jamais les côtés ni le haut

**Symptôme** : dimensionner les images avec `aspect-ratio` : dans une grille au parent exigu, elles s'empilent ou perdent une information clé (ex. la barre de titre d'une capture en haut).

**Conduite** : conteneur d'image en **height fixe + overflow hidden**, image en `object-fit:cover + object-position:top` :

```html
<figure class="frame-img" style="height:26vh">
  <img src="screenshot.png">
</figure>
```

Dans le CSS, `.frame-img img` a déjà `object-position:top` préréglé — rogne le bas seulement.

**Jamais cette écriture** (elle fait éclater le conteneur dans une grille) :

```html
<!-- mauvais exemple -->
<figure class="frame-img" style="aspect-ratio: 16/9">...</figure>
```

**Exception** : un visuel principal isolé (hors grille) peut prendre `aspect-ratio + max-height`, le parent servant de garde-fou.

### 2b. Page claire + WebGL sombre = voile gris (bascule de thème inefficace)

**Symptôme** : tous les fonds des pages light semblent voilés de gris, même le hero light.

**Cause racine** : le JS bascule l'opacité des deux canvas selon le thème du slide. Si le deck commence en hero dark sans qu'aucun mécanisme ne ramène le fond en light, le body ne reçoit jamais la classe `light-bg` et `canvas#bg-dark` reste au-dessus.

**Conduite** :
- Dans le gabarit, la fonction `go()` déduit désormais le thème du `classList` (`light` / `dark`) : **les slides doivent donc explicitement porter la classe `light` ou `dark`**. Ne pas l'omettre, et n'inventer aucun autre nom de thème
- Pages hero : `hero light` / `hero dark` ; pages de contenu : `light` / `dark`. Écrire seulement `hero` sans thème est une erreur
- Un deck doit contenir au moins une page light **non hero**, pour que le body ait l'occasion de recevoir `light-bg`

### 2b-2. Un deck entièrement light, sans rythme

**Symptôme** : sauf la couverture `hero dark`, toutes les pages sont écrites `light` par défaut — visuel plat, sans respiration, une nappe blanche.

**Cause racine** : les squelettes de layouts.md sont écrits `light` par défaut ; coller les squelettes sans ajuster les thèmes donne un tout-clair.

**Conduite** :
- **Avant génération, dessiner la « table de rythme des thèmes »** : pour chaque page, noter `hero dark` / `hero light` / `light` / `dark`, et aligner avant de coder
- **Règle dure** : plus de 3 pages consécutives du même thème = interdit ; au-delà de 8 pages, exiger ≥1 `hero dark` + ≥1 `hero light` ; pas que des pages de contenu `light` — il faut des pages de contenu `dark`
- **Choisir le thème selon la mise en page** (voir « planification du rythme des thèmes » en tête de layouts.md) :
  - texte-gauche image-droite (Layout 4), grande citation (Layout 8), mixte (Layout 10) → **alternance `light` / `dark`**
  - grands chiffres, grille d'images, Pipeline, pages de comparaison → `light` (captures/chiffres/flux exigent un fond clair)
  - couverture, page-question → `hero dark`
  - volet de chapitre → alternance `hero dark` et `hero light`
- **Auto-contrôle après génération** : `grep 'class="slide' index.html`, vérifier visuellement l'alternance

### 2c. chrome et kicker ne doivent pas dire la même chose

**Symptôme** : en haut à gauche `.chrome` dit « Design First · design d'abord », et sur la même page `.kicker` dit « Phase 01 · phase de conception » — traduction synonyme, fort relent d'IA.

**Conduite** :
- **chrome = en-tête de magazine / onglet de navigation** : peut se répéter sur plusieurs pages (« Act II · Workflow », « Data · Result », « lukew.com · 2026.04 »)
- **kicker = phrase d'accroche unique à la page** : courte, avec un crochet, « petit préfixe » du grand titre (« BUT », « une seule personne, qu'a-t-elle fait. », « The Question »)
- L'un décrit la rubrique, l'autre cette page — jamais l'un comme traduction de l'autre

### 3. La taille des grands titres ne doit pas dépasser la largeur d'écran / le nombre de caractères

**Symptôme** : un grand titre chinois réglé trop grand (ex. 13vw) : une seul caractère par ligne, avec des retours forcés très laids.

**Conduite** :
- `h-hero` (le plus grand) : 10vw, **et titre ≤ 5 caractères**
- `h-xl` (grand suivant) : 6vw-7vw
- Les titres longs se coupent manuellement par `<br>`, sans compter sur le retour automatique
- Ajouter `white-space:nowrap` si nécessaire

**Exemple** : « Je ne suis pas programmeur. » (6 caractères) en `h-xl` 7.2vw + nowrap, tient sur une ligne.

### 4. Répartition des polices : titres serif, corps sans-serif

**Conduite** :
- Grands titres, citations fortes, grands chiffres → **serif** (Noto Serif SC + Playfair Display + Source Serif)
- Corps, descriptions, noms d'étapes pipeline → **sans-serif** (Noto Sans SC + Inter)
- Métadonnées, code, étiquettes → **monospace** (IBM Plex Mono + JetBrains Mono)

Toutes les polices arrivent par le CDN Google Fonts, déjà préréglées dans le gabarit.

### 4b. Ne pas caler les images en bas avec `align-self:end`

**Symptôme** : dans le layout texte-gauche image-droite, un `align-self:end` posé sur `<figure>` pour aligner l'image avec le bas du callout de gauche. Résultat :
- si le parent n'est pas une grid (ex. classe non définie), `align-self` est sans effet et l'image descend au fond du flux, masquée par la barre du navigateur
- même en grid, l'image se cale en bas de la cellule et reste masquée par `.foot` et les pastilles `#nav` sur petits écrans

**Conduite** :
- le mixte texte-image **doit utiliser `.frame.grid-2-7-5`** (ou `.grid-2-6-6`/`.grid-2-8-4`)
- la figure de droite `<figure class="frame-img">` en **ratio standard 16/10 ou 4/3 + max-height:56vh**, laissée naturellement en haut
- pour donner au callout de gauche l'effet « calé en bas », poser sur la **colonne de gauche** flex column + `justify-content:space-between`, sans toucher la droite

### 4c. Ne pas reprendre les ratios bizarres des images d'origine

**Symptôme** : un `aspect-ratio: 2592/1798` copié depuis la photo produit des vides étranges ou des débordements selon les écrans.

**Conduite** : quel que soit le ratio d'origine, le conteneur prend toujours un ratio standard **16/10 / 4/3 / 3/2 / 1/1 / 16/9**. L'image suit `object-fit:cover + object-position:top` : le haut reste entier, rogner un peu en bas est sans conséquence.

### 5. Pas de bordures épaisses ni d'ombres sur les images

**Symptôme** : une ombre forte ou un cadre noir pour faire « premium » — effet PPT corporate immédiat.

**Conduite** : au plus 1-4px de micro-arrondi + **un très léger grain de fond** (déjà dans le gabarit). Pas de `box-shadow`, pas de `border` (sauf 1px gris très pâle).

---

## 🟡 P1 · Rythme de mise en page

### 6. Alterner pages hero et non-hero

**Rythme recommandé** (25-30 pages) :
```
Hero Cover → Act Divider (hero) → 3-4 pages non-hero → Act Divider (hero)
→ 4-5 pages non-hero → Hero Question → ... → Hero Close
```

Plus de 2 pages hero d'affilée fatigue ; plus de 4 pages non-hero d'affilée tue le rythme.

### 7. Alterner pages en grands caractères et pages denses

Alterner grands chiffres / questions hero avec les pages denses (pipeline / grille d'images) : l'œil de l'auditoire se repose.

### 8. Unifier l'usage chinois/anglais d'un même concept

**Symptôme** : tantôt « Skills », tantôt « compétences », tantôt « harnais mince, compétences épaisses » — incohérence sur tout le deck.

**Conduite** :
- privilégier le **mot anglais** pour les termes (Skills / Harness / Pipeline / Workflow), familiers au milieu
- **ne pas forcer la traduction** — la traduction forcée sonne raide
- un seul libellé par mot sur tout le deck

### 9. La pagination du chrome bas doit être cohérente

Au format `XX / total` (ex. `05 / 27`). **Pas de pagination dynamique en haut à droite** (elle ferait doublon avec `.chrome`).

---

## 🟢 P2 · Polissage visuel

### 10. Opacité du voile sur le fond WebGL

**dark hero** : voile 12-15 % (WebGL nettement visible)
**light hero** : voile 16-20 % (WebGL suggéré, ne vole pas le texte)
**pages light/dark ordinaires** : voile 92-95 % (presque opaque)

Si la page contient très peu de texte (hero question), le voile peut s'alléger encore ; si le corps est dense, l'épaissir pour la lisibilité.

### 11. Le shader d'un light hero ne doit pas avoir de point central marqué

**Symptôme** : Spiral Vortex, ondulations radiales trop voyantes en thème light — effet économiseur d'écran Windows 98.

**Conduite** : pour le light hero, un écoulement sans centre piloté par distorsion de domaine FBM, fond argenté/papier (proche de #F0F0F0 / #FBF8F3), irisation subtile (sous 0.05).

### 12. Le dark hero tolère plus d'impact visuel

Le dark hero peut prendre des shaders à structure centrale — Holographic Dispersion (dispersion titane) etc. — car le fond noir absorbe plus d'information visuelle.

### 13. Alignement du layout texte-gauche image-droite

- Groupe de texte à gauche en `justify-content:space-between` : titre en haut, cadre de citation en bas
- Image à droite en `align-self:end` : alignée sur l'élément bas de gauche
- Grille entière en `align-items:start` (pas `center` / `end`)

### 14. Micro-arrondi des images

Tous les `.frame-img` et `.frame-img img` reçoivent `border-radius:4px` — « adouci » sans être mou. **Pas plus de 8px**, sinon effet app grand public.

---

## 🔵 P3 · Détails d'exécution

### 15. Chemins d'images relatifs

Images dans le dossier `images/`, chemins relatifs `images/xxx.png` dans le HTML, jamais de chemins absolus.

### 16. Pagination figée dans `.chrome`

Le JS calcule dynamiquement le total et étend les pastilles de pagination, mais le `XX / N` de `.chrome` est figé. Ajouter/retirer une page impose de corriger N à la main.

### 17. Conserver la navigation de pagination

Le gabarit gère par défaut : ← → / molette / glisser tactile / pastilles en bas / Home·End. Ne pas supprimer la logique de navigation du JS.

### 18. Pas de `height:100vh` en dur ; préférer `min-height:80vh`

`100vh` cale exactement l'écran, mais barre d'outils et onglets du navigateur grignotent la hauteur et le contenu déborde. `min-height:80vh + align-content:center` est plus robuste.

---

## 🧪 Liste d'auto-contrôle final

Après génération du PPT, cocher chaque point :

```
Pré-contrôle (avant génération)
  □ avoir lu le <style> de template.html et vérifié les classes requises
  □ avoir décidé le Layout (1-10) de chaque page
  □ avoir dessiné la « table de rythme des thèmes » : hero dark / hero light / light / dark par page
  □ la table respecte les règles dures : pas 3 pages de suite au même thème / ≥1 hero dark + ≥1 hero light (au-delà de 8 pages) / au moins 1 page de contenu dark
  □ `<title>` remplacé par le vrai titre du deck (grep « [à renseigner] » sans résultat)

Contenu
  □ proportion de pages équilibrée par acte (pas de top-heavy)
  □ aucun emoji en icône
  □ usage unifié des termes Skills / Harness etc.
  □ sur chaque page, les trois niveaux kicker + titre + corps sont clairs

Mise en page
  □ aucun grand titre avec un caractère par ligne
  □ grilles d'images en height:Nvh, pas aspect-ratio
  □ images rognées en bas seulement, haut et côtés entiers
  □ répartition serif/sans-serif conforme au gabarit
  □ séparations nettes entre les groupes du Pipeline

Visuel
  □ alternance pages hero / non-hero
  □ fond WebGL visible sur les pages hero
  □ micro-arrondi des images
  □ ni ombres lourdes ni cadres

Interactions
  □ pagination ← → fonctionnelle
  □ nombre de pastilles = nombre de pages
  □ pagination du chrome conforme au réel
  □ touche ESC ouvre la vue index (si conservée)
```

Tout coché, et seulement tout coché : le PPT est conforme.
