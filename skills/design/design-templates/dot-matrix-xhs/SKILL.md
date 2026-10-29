---
name: dot-matrix-xhs
description: Gabarit de couverture Xiaohongshu / affiche magazine / couverture de publication indépendante en trame de points noir et blanc par dithering de Bayer — fond noir + vrai Bayer 8×8 exécuté dans un Canvas pour convertir n'importe quelle image en trame pure noir et blanc + vignette double haut-bas + textes aux quatre coins façon rubriques de magazine (numéro / rubrique / wordmark / credit) + très grands titres chinois gras Noto Sans JP Black en grille 2×2 + numéro de livraison entre crochets au centre. 4 squelettes de mise en page (couverture image unique / image en haut texte en bas / triptyque de série / page intérieure long format), requêtes de conteneur cqh pour s'adapter à toute taille. Déclencheurs : l'utilisateur réclame « trame de points / dither / 1-bit / grain noir et blanc / couverture Xiaohongshu / affiche Vol numéro / publication indépendante / impression journal ». NOT page produit multi-blocs, NOT affiche en couleurs.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: 点阵.html
source_priority: skill-first
triggers:
  - « fais une couverture Xiaohongshu en trame de points »
  - « couverture grain noir et blanc »
  - « affiche 1-bit »
  - « couverture Vol numéro »
  - « couverture de publication indépendante »
  - « couverture à l'impression journal »
  - « dither, tramage »
related_patterns: social-card-editorial
---

# dot-matrix-xhs — couverture en trame de points noir et blanc par dithering Bayer

Soumettre n'importe quelle photo en temps réel à un dithering ordonné Bayer 8×8 pour la transformer en « trame d'impression journal », posée sur un squelette de textes aux quatre coins façon magazine + grand titre chinois 2×2. **Ratio de conteneur fixe 1280×1644 (couverture verticale Xiaohongshu)**, mais mise en page en unités de requête de conteneur (cqh) : réduite à n'importe quelle taille, jamais floue.

## Comment utiliser ce skill

1. **Saisir le ton** : d'abord Read `点阵.html` (exemple « feu de camp nocturne / a fire at midnight »), en regardant la densité de grain du Bayer, l'intensité du vignettage, la hiérarchie des textes des quatre coins. **Cette étape sert uniquement à « savoir à quoi ressemble le juste résultat ».**
2. **Choisir le squelette** : prendre l'un des 4 squelettes ci-dessous (couverture image unique / image haut texte bas / triptyque / page intérieure), **interdiction de cloner intégralement le feu de camp nocturne** (le combo 2×2 + crochets centraux + wordmark en bas = resemblance assurée).
3. **Copier les briques** : la fonction Canvas Bayer, la mise en page par requêtes de conteneur, la disposition des quatre coins se transplantent telles quelles.
4. **Passer la ligne rouge** : auto-contrôle avec la liste « obligatoire / interdit » après écriture.

## ADN visuel — à ne jamais perdre

S'il manque un seul de ces éléments, ce n'est plus la trame magazine :

1. **Fond noir + vrai dithering Bayer dans un Canvas** : la couche de fond est toujours une image tramée par Bayer 8×8, **pas du CSS noise, pas un filtre SVG, pas un PNG pré-rendu — le Canvas doit tourner en temps réel**. Toute image (personne, paysage, objet) ne devient juste qu'après `adjustBrightness(-20~-30) + adjustLevels(60~80, 190~210) + bayerDither`.
2. **Rendu aux bords nets de pixels** : le canvas doit avoir `image-rendering:pixelated`, pour que la trame garde ses bords durs au redimensionnement, sans flouter ni griser à l'agrandissement.
3. **Vignette double haut-bas** : `linear-gradient(180deg, rgba(0,0,0,.55) 0%, transparent 18%, transparent 70%, rgba(0,0,0,.45) 100%)`, pour asseoir le numéro en haut et le wordmark en bas ; **pas de vignette aux quatre coins** (l'arrondi ferait immédiatement « objectif d'appareil photo »).
4. **Quatre coins façon rubriques de magazine** : haut-gauche = numéro (`No 04 / 2026`), haut-droit = rubrique anglaise + petit chinois, bas-gauche = wordmark principal, bas-droit = année + credit. **Remplir au moins 3 coins** — c'est la marque des publications indépendantes ; en dessous de 3, ce n'est qu'une image avec du texte.
5. **Très grand titre chinois ultra-gras** : `Noto Sans JP Black` + repli `PingFang SC`, `font-weight:900`, `line-height:1.1`, `letter-spacing:0` (composition serrée du chinois, sans interlettrage). **Interdits : corps fins / kai / lishu / ronds**.
6. **Texte blanc avec léger text-shadow** : tout texte posé sur la trame doit recevoir `text-shadow:0 0 .8cqh rgba(0,0,0,.85)`, pour rester lisible sur les zones claires de la trame.

## Obligatoire / Interdit (auto-contrôle après écriture)

**Obligatoire** :
- [ ] un vrai dithering Bayer dans le Canvas (pas de filtre CSS, pas de SVG noise, pas d'image pré-rendue)
- [ ] le conteneur a un `aspect-ratio` fixe (couverture 1280/1644, affiche libre)
- [ ] le conteneur porte `container-type:size`, et la mise en page utilise `cqh` / `cqw`
- [ ] au moins 3 coins remplis (numéro, rubrique, wordmark, credit — en choisir 3)
- [ ] graisse du titre principal ≥ 800
- [ ] webfont chinoise chargée en « quatre pièces » (preconnect + preload + print-onload + noscript)
- [ ] les trois lignes `image-rendering:pixelated / -moz-crisp-edges / crisp-edges` du canvas, aucune ne manque

**Interdit** :
- [ ] ne pas recopier le combo complet « matrice 2×2 de caractères chinois + crochets centraux + wordmark en bas » — c'est l'empreinte du feu de camp nocturne
- [ ] ne pas simuler la trame par SVG noise / `filter: contrast` / `background-image: radial-gradient(...dot)` — ça se voit immédiatement
- [ ] la trame ne doit pas garder de niveaux de gris (la sortie Bayer est binaire : noir pur 0 ou blanc pur 255, aucune valeur intermédiaire)
- [ ] pas de teinte saturée sur l'image (filtre crépuscule, dominante bleu-vert, crème) — cette esthétique est du 1-bit noir et blanc pur
- [ ] pas d'arrondis — cadres, boutons, cartes : tout à angles droits
- [ ] pas d'emoji / stickers 3D / dégradés de couleur / glassmorphism / ombres flottantes
- [ ] pas de titres en PingFang Regular / Source Han Sans Light — graisse Heavy / Black obligatoire
- [ ] ne pas reprendre « 深/夜/篝/火 + VOL IV / 2026 + wordmark 夜火 + identifiant Xiaohongshu 955873829 » — c'est l'empreinte de l'exemple

## Quatre squelettes de mise en page (en choisir un ; plus jamais le combo « feu de camp nocturne »)

Chacun porte l'ADN trame + quatre coins, mais avec des **structures radicalement différentes**, pour éviter les ressemblances.

### Squelette A — couverture image unique (prototype du feu de camp nocturne, à consulter mais à utiliser avec prudence)
```
[fond]  image plein écran en trame Bayer + vignette haut-bas
[coins] haut-gauche numéro / haut-droit rubrique+chinois / bas-gauche wordmark / bas-droit credit
[haut-centre] filet hr + très grand titre chinois 2×2 + sous-titre anglais italique
[centre] numéro de livraison ou mot-thème entre crochets
```
Adapté à : une seule photo à forte présence visuelle en couverture (portrait, paysage, nature morte). 1280×1644.

### Squelette B — image en haut, texte en bas
```
[haut 60 %]  image en trame Bayer + numéro en haut + rubrique
[bas 40 %]   zone noir pur, grand titre à gauche (une ou deux lignes horizontales), citation + source à droite
[bandeau bas] filet fin + wordmark + numéro
```
Adapté à : longs titres, ou présence de texte secondaire, citation, signature (pas de grille 2×2 obligatoire). 1280×1644 ou 1080×1350.

### Squelette C — couverture triptyque de série
```
[toute la surface en 3 colonnes]  chaque colonne une image Bayer indépendante (portrait / objet / décor)
                                 chaque colonne a en bas son propre sous-titre + numéro 01 / 02 / 03
[bandeau haut]  numéro + rubrique unifiés
[bandeau bas]   wordmark + nom de l'ensemble unifiés
```
Adapté à : reportages en série, portfolios de portraits, gammes de produits, couvertures de carnet de voyage. Paysage 1644×1280 ou portrait 1280×1644.

### Squelette D — page intérieure / long format
```
[bandeau haut] numéro + rubrique + filet
[colonne gauche] titre sticky + citation (40 % de la largeur)
[colonne droite] long corps de texte (paragraphes + citations en ligne), avec 1-2 petites images Bayer insérées
[bandeau bas] pagination + wordmark
```
Adapté à : pages intérieures de publication, longs essais, entretiens (au-delà de la couverture, du contenu à lire). 1280×1800+ ou ratio A4.

## Briques de code à copier directement

### Dithering Bayer 8×8 (cœur, à ne pas simplifier)
```js
function bayerDither(ctx, W, H){
  const d = ctx.getImageData(0,0,W,H), px = d.data;
  const m = [
    [ 0,32, 8,40, 2,34,10,42],[48,16,56,24,50,18,58,26],
    [12,44, 4,36,14,46, 6,38],[60,28,52,20,62,30,54,22],
    [ 3,35,11,43, 1,33, 9,41],[51,19,59,27,49,17,57,25],
    [15,47, 7,39,13,45, 5,37],[63,31,55,23,61,29,53,21]
  ];
  for (let y=0; y<H; y++) for (let x=0; x<W; x++){
    const i=(y*W+x)*4;
    const luma = (0.299*px[i] + 0.587*px[i+1] + 0.114*px[i+2]) / 255;
    const t = (m[y%8][x%8] + 0.5) / 64;
    const v = luma > t ? 255 : 0;
    px[i]=px[i+1]=px[i+2]=v; px[i+3]=255;
  }
  ctx.putImageData(d,0,0);
}
```
**Point clé** : ne pas remplacer la matrice 8×8 par du 4×4 (grain trop grossier), ni par Floyd-Steinberg (une autre saveur de diffusion d'erreur, le grain « coule »). La densité de la trame = résolution interne du canvas : W=600 H=771 par défaut pour la couverture ; plus fin : 900×1158 ; plus rugueux : 400×514.

### Prétraitement : assombrir + renforcer le contraste (pour une trame nettement binaire)
```js
function adjustBrightness(ctx, W, H, delta){
  const d = ctx.getImageData(0,0,W,H), px = d.data;
  for (let i=0; i<px.length; i+=4)
    for (let c=0; c<3; c++){ let v=px[i+c]+delta; px[i+c]=v<0?0:v>255?255:v; }
  ctx.putImageData(d,0,0);
}
function adjustLevels(ctx, W, H, lo, hi){
  const d = ctx.getImageData(0,0,W,H), px = d.data, scale = 255 / (hi - lo);
  for (let i=0; i<px.length; i+=4)
    for (let c=0; c<3; c++){ let v=(px[i+c]-lo)*scale; px[i+c]=v<0?0:v>255?255:v; }
  ctx.putImageData(d,0,0);
}
```
**Ordre d'appel fixe** : `drawImage → adjustBrightness(-25) → adjustLevels(70, 195) → bayerDither`. **Ne jamais dither avant d'ajuster le contraste** — le dither est déjà binaire, ajuster ensuite est sans effet.

### Configuration de l'élément Canvas
```html
<canvas class="bg" id="bg" width="600" height="771"></canvas>
<img class="src" id="src" src="YOUR_IMG_URL" crossorigin="anonymous" alt="">
```
```css
canvas.bg{
  position:absolute; inset:0;
  width:100%; height:100%;
  image-rendering:pixelated;
  image-rendering:-moz-crisp-edges;
  image-rendering:crisp-edges;
  z-index:0; display:block;
}
img.src{ display:none }
```
L'image source `<img>` sert uniquement au drawImage du canvas, jamais affichée directement. `crossorigin="anonymous"` est obligatoire — sinon getImageData échoue en cross-origin.

### Flux complet de traitement Canvas
```js
(async function(){
  if (document.fonts && document.fonts.ready){ try { await document.fonts.ready; } catch(e){} }
  const img = document.getElementById('src');
  const canvas = document.getElementById('bg');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;

  const ready = (img.complete && img.naturalWidth > 0)
    ? Promise.resolve()
    : new Promise((res, rej) => { img.onload = res; img.onerror = rej; });
  try { await ready; } catch(e){ console.warn('img failed', e); return; }

  const ratio = Math.max(W / img.naturalWidth, H / img.naturalHeight);
  const dw = img.naturalWidth * ratio, dh = img.naturalHeight * ratio;
  ctx.drawImage(img, (W - dw) / 2, (H - dh) / 2, dw, dh);

  adjustBrightness(ctx, W, H, -25);
  adjustLevels(ctx, W, H, 70, 195);
  bayerDither(ctx, W, H);
})();
```

### Mise en page par requête de conteneur (netteté à toute taille)
```css
.frame{
  position:relative;
  height:min(94vh, 1644px);
  aspect-ratio: 1280 / 1644;
  container-type:size;
  background:#000; color:#fff;
  overflow:hidden;
}
.title{ font-size:12cqh; }
.credit{ font-size:.85cqh; letter-spacing:.28em; }
```
**Pourquoi cqh plutôt que vh** : vh suit le viewport — si le conteneur change de taille, le texte ne suit pas. cqh suit le conteneur `.frame` : la couverture réduite de moitié garde ses proportions.

### Vignette double haut-bas
```css
.vignette{
  position:absolute; inset:0; z-index:1; pointer-events:none;
  background: linear-gradient(180deg,
    rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 18%,
    rgba(0,0,0,0) 70%, rgba(0,0,0,.45) 100%);
}
```
Le haut est plus appuyé (.55 vs .45) car le numéro est plus petit que le credit et demande plus de protection par le contraste.

### Disposition des quatre coins
```css
.layer{
  position:absolute; inset:0; z-index:2;
  padding:3.6cqh 4.4cqh;
  display:flex; flex-direction:column;
  pointer-events:none;
}
.layer *{ text-shadow:0 0 .8cqh rgba(0,0,0,.85) }
.top{
  display:flex; justify-content:space-between; align-items:center;
  font-size:.95cqh; letter-spacing:.32em; text-transform:uppercase; font-weight:500;
}
.bottom{
  margin-top:auto;
  display:flex; justify-content:space-between; align-items:flex-end;
}
```
Le `margin-top:auto` garantit le footer en bas, quel que soit le volume du contenu intermédiaire.

### Titre chinois 2×2 (squelette A seulement)
```html
<div class="title-grid">
  <div class="col"><span class="sm">深</span><span class="sm">篝</span></div>
  <div class="col"><span class="lg">夜</span><span class="lg">火</span></div>
</div>
```
```css
.title-grid{
  display:inline-flex; align-items:flex-start; gap:0;
  font-family:'Noto Sans JP','PingFang SC','Heiti SC',sans-serif;
  font-weight:900; line-height:1.1; letter-spacing:0;
}
.title-grid .col{ display:flex; flex-direction:column }
.title-grid .sm, .title-grid .lg{ font-size:12cqh }
```
**Contrainte** : exactement 4 caractères chinois, scindés en deux colonnes selon les mots (深/篝 d'un côté, 夜/火 de l'autre), pas dans l'ordre de lecture. 3, 5 ou 6 caractères : autre squelette.

### Numéro entre crochets (décor)
```css
.brackets{
  position:relative; padding:1cqh 2.6cqh;
  font-weight:500; font-size:1.1cqh; letter-spacing:.36em;
  text-transform:uppercase;
}
.brackets::before, .brackets::after{
  content:''; position:absolute;
  width:1.3cqh; height:1.3cqh; border:1px solid #fff;
}
.brackets::before{ top:0; left:0; border-right:none; border-bottom:none }
.brackets::after{ bottom:0; right:0; border-left:none; border-top:none }
```
Deux angles en L, haut-gauche et bas-droite, comme un viseur d'appareil / des traits de coupe d'imprimerie.

## Chargement des webfonts chinoises (obligatoire)

`Noto Sans JP` Heavy est une police japonaise en très forte graisse (avec repli sur les caractères chinois), volumineuse ; le chinois privilégie d'abord PingFang/Heiti locaux. En « quatre pièces » :

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" fetchpriority="high"
  href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@900&display=swap">
<link rel="stylesheet" media="print" onload="this.media='all'"
  href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@900&display=swap">
<noscript><link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+JP:wght@900&display=swap"></noscript>
```
La pile de polices doit toujours inclure les replis `'PingFang SC','Heiti SC'` ; les petits textes anglais en Inter (italique pour les sous-titres).

## Vérification des informations d'entrée

Faire rassembler ceci à l'utilisateur avant de commencer :
1. **Une image de fond** (obligatoire) — URL ou chemin local. Visage / paysage / nature morte, tous conviennent, mais **le contraste doit être fort** : une image terne devient une nappe après le dither ; vérifier d'abord dans un éditeur que sujet et fond se distinguent
2. **Numéro + rubrique** (obligatoires) — `No 04 / 2026` + rubrique anglaise (CAMPING / TRAVEL / FOOD…) + 2-4 caractères chinois
3. **Titre** (obligatoire) — squelette A : 4 caractères + sous-titre anglais italique ; squelettes B/C/D : longueur libre
4. **wordmark + credit** (obligatoires) — grande marque 2-4 caractères + année / identifiant Xiaohongshu / auteur / source
5. **Ratio** (optionnel) — défaut 1280/1644 ; possibles 1080/1350, 1644/1280, 1×1
6. **Densité du grain dither** (optionnel) — « fin / moyen / grossier » correspond à une largeur interne du canvas de 900 / 600 / 400

## Aide-mémoire des anti-patterns (corriger dès qu'on les voit)

| Symptôme | Erreur | Correction |
|---|---|---|
| La trame devient une nappe, l'image se devine à peine | pas d'adjustLevels | ajouter `adjustLevels(70, 195)`, sinon pas d'effet trame |
| Trame toute noire ou toute blanche | brightness/levels trop poussés | brightness ∈ [-30, -10], levels lo<80 hi>180 |
| Le texte flotte et devient illisible | pas de text-shadow / pas de vignette | `text-shadow:0 0 .8cqh rgba(0,0,0,.85)` + dégradés haut-bas |
| La trame floue après redimensionnement | `image-rendering:pixelated` oublié | les trois lignes image-rendering du canvas |
| Les tailles de texte ne suivent pas le conteneur | vh au lieu de cqh | `container-type:size` sur le conteneur, tailles en cqh |
| Titre trop fin, rendu mou | PingFang Regular / Light | Noto Sans JP 900 + repli PingFang Heavy |
| Titre chinois espacé façon enseigne | letter-spacing ajouté | composition serrée `letter-spacing:0` |
| Un ou deux coins seulement remplis | l'effet magazine s'effondre en « image avec texte » | au moins 3 coins (numéro / rubrique / wordmark / credit — en choisir 3) |
| Emoji / arrondis / couleur présents | violation de l'esthétique 1-bit | supprimer, retour au noir et blanc pur + angles droits |
| La trame ressemble à du CSS noise | pas de vrai Bayer dans Canvas | Canvas obligatoire avec `bayerDither`, jamais de simulation SVG/CSS |
| Copie conforme du feu de camp nocturne | aucun autre squelette choisi | imposer B/C/D |

## À propos de 点阵.html

Placé dans le même répertoire que le skill, c'est l'exemple complet « feu de camp nocturne · a fire at midnight » (squelette A implémenté). **N'en retenir que l'ordre d'appel du Bayer, la structure cqh, la hiérarchie des quatre coins** ; ne pas transposer tels quels « 深/夜/篝/火 + VOL IV / 2026 + wordmark 夜火 + identifiant Xiaohongshu 955873829 » dans un nouveau projet — c'est l'empreinte de l'exemple.

## Exigences de sortie

- HTML monofichier (HTML + CSS + JS de traitement Canvas)
- Requêtes de conteneur + `aspect-ratio` fixe, netteté au redimensionnement
- Webfont chinoise chargée en quatre pièces
- Les trois lignes `image-rendering` du canvas
- Pas de commentaires expliquant ce qu'est Bayer — l'ordre d'appel suffit
