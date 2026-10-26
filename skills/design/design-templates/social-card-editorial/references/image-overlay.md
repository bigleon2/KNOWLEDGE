# Image Overlay & Subject Safety

Deux règles qui régissent tout poster où du texte se superpose à une image — fond pleine page, grande photo avec barre de titre, ou image générée/AI avec superposition de texte.

Une composition peut passer le linting HTML et rester illisible. Les deux règles ci-dessous doivent être satisfaites avant d'expédier.

## Rule 1 — Selection first, mask only if selection fails

La réponse par défaut des magazines éditoriaux est **pas de masque**. Les vraies couvertures de magazine (Kinfolk, Cereal, Apartamento, Monocle) mettent presque jamais un dégradé noir uniforme sur une photo principale. Ils s'appuient sur la **sélection photo + composition** pour que le texte atterrisse naturellement dans une zone calme. Si vous ne trouvez pas une telle photo, la réponse est généralement de remplacer la photo, pas de boucher une mauvaise avec un voile à 70% de noir.

Appliquez les étapes dans l'ordre. Arrêtez-vous à la première qui réussit.

### Step 1 — Photo selection (the main lever)

Avant de choisir un masque, vérifiez que la photo convient au traitement pleine page. Les deux tests doivent réussir :

**Quiet-zone test** : au moins une bande de ≥30% du canevas (pleine largeur × ≥30% hauteur, ou pleine hauteur × ≥30% largeur) est **faible en détails / faible en contraste / uniforme**. Exemples : arrière-plan flou, ombre profonde, brouillard, eau calme, ciel simple, herbe floue. Cette bande est où le titre atterrira.

**Light test** : la photo présente une **lumière atmosphérique / retenue** — ciel couvert, brume de l'aube, heure dorée, sous-bois, douceur filmique, silhouette de crépuscule. Rejetez les prises de vue de midi saturées, flash intégré à l'appareil, selfies "tourist trap", joie générique de stock.

Si l'un des tests échoue, **la photo est mauvaise pour M16**. Retournez à M01 (couverture en mise en page divisée avec photo dans un cadre), ou reprenez/tirez à nouveau. Ne "réparez pas avec un masque."

### Step 2 — Compose without a mask first

Placez le titre à l'intérieur de la zone calme qualifiée. Lancez le test de contraste de miniature (Étape 4). Si il se lit bien, expédiez tel quel. La plupart des photos éditoriales bien sélectionnées réussissent à cette étape.

Une couverture sans masque signe le savoir-faire. Une couverture fortement masquée signale "nous n'avons pas trouvé la bonne photo". Essayez l'étape 2 chaque fois avant de passer à l'étape 3.

### Step 3 — Localized, image-toned tint (fallback only)

Seulement lorsque l'étape 2 échoue le test de contraste. Trois règles :

1. **Localized, not full-canvas.** Teinte uniquement la région du titre. Utilisez `radial-gradient` centré sur le bloc titre, ou un dégradé linéaire unilatéral qui s'estompe pour devenir totalement transparent au-delà du titre. Jamais `inset: 0` sur toute l'image avec une courbe alpha uniforme.
2. **Image-toned, not black.** Échantillonnez une teinte sombre déjà présente dans la photo et utilisez-la comme couleur de teinte. Forêt → mousse profonde `#1a2818`. Crépuscule → crépuscule rose thé `#4a2638`. Neige → gris-bleu frais `#2a3438`. Le noir pur `#000` se lit comme "couche d'annotation", pas "profondeur atmosphérique".
3. **Soft, not opaque.** Alpha maximal 0.15-0.30 dans la région du titre, tombant à 0 à l'extérieur. Si vous avez besoin de >0.40 pour lire, la photo a échoué à l'étape 1 — revenez en arrière.

```css
/* Example: title in lower-left, image-toned soft tint */
.hero-bleed::after {
  content: "";
  position: absolute; inset: 0;
  background: radial-gradient(
    60% 45% at 25% 80%,         /* centered on title block */
    rgba(26, 40, 24, 0.28) 0%,  /* forest moss tone, soft peak */
    rgba(26, 40, 24, 0.0) 100%);
  pointer-events: none;
}
```

### Step 4 — Thumbnail contrast check (always)

Que vous ayez appliqué une teinte ou non :

- Rendezu le PNG, réduisez sa largeur à 360 px dans Aperçu / un onglet de navigateur, et regardez.
- Les contours du titre doivent être lisibles sans zoom.
- Si le titre semble "se battre" avec la photo → remplacez la photo ou déplacez le titre vers une zone calme différente, **pas** renforcez le masque.
- Si la photo semble morte et grise sous un sombre uniforme → le masque est beaucoup trop lourd ou couvre la mauvaise zone ; recommencez à l'étape 1.

### Banned

- **Uniform full-canvas vertical falloff** (le modèle `rgba(0,0,0,.55) → .10 → .10 → .80` des versions précédentes de cette compétence). C'est un traitement de jeu-clef-art, pas éditorial.
- **Pure black mask color**. Toujours image-toned (forêt, crépuscule, neige, bleu-encre, sépia).
- Rectangle noir/blanc plat derrière le texte — se lit comme annotation de capture d'écran.
- `mix-blend-mode: difference` pour la lisibilité — détruit les tons de peau, ne fonctionne pas à l'impression.
- `img { opacity: .6 }` — tue la profondeur de la photo, le but même de la pleine page.
- Atteindre l'étape 3 avant d'avoir honnêtement tenté l'étape 1 avec une meilleure photo.

---

## Rule 2 — Place text away from subject / face zones

Les affiches dans 旅行 / 游戏 / 影视 / 穿搭 / 美食 (voyage / jeu / cinéma / mode / gastronomie) utilisent souvent une vraie photo comme élément principal. La photo a un sujet — un visage, une main, un produit, un sommet. Un texte qui chevauche le sujet se lit comme du graffiti, pas comme de l'éditorial.

### Subject zone discovery — multimodal first

Avant de concevoir la position du titre sur une photo principale, regardez l'image. Ouvrez-la avec l'outil Read et observez en langage simple :

1. Où se trouve le **visage / caractéristique focale du sujet principal** ? (par ex. "le visage de l'alpiniste est dans le tiers supérieur droit autour de 70% x 30% y")
2. Où se trouve le **bord du sujet silhouette** ? (par ex. "le bord gauche se termine à ~40% x ; en dessous est le ciel")
3. Où se trouve la **plus grande zone ouverte / faible en détails** ? (par ex. "le quadrant inférieur gauche est du brouillard uniforme")

Enregistrez les réponses comme un commentaire dans le HTML à côté du bloc principal :

```html
<!-- subject map (Wukong cover hero):
     face/skull centerpiece: 50% x 45% y, occupies ~30% of frame
     left-side staff & weapons: 15-40% x, full height
     safe text zone: top band (0-15% y) and bottom band (65-100% y)
-->
```

C'est l'entrée que la mise en page utilise. C'est déterministe et revisible.

### Safe-zone placement rules

Étant donné la carte du sujet, placez le texte dans cet ordre de préférence :

1. **Au-dessus + en dessous** du sujet (accroche en haut, titre en bas). 90% des couvertures pleine page devraient faire cela.
2. **D'un côté** — si le sujet occupe une colonne verticale (par ex. portrait à droite), le texte remplit la colonne opposée. Combinez avec une teinte latérale de la règle 1 étape 3 uniquement si nécessaire.
3. **Coin diagonal** — uniquement lorsque le sujet est dans un coin et que le coin opposé est véritablement vide. Rare.

Ne placez jamais de titres d'affichage **à travers** le visage. Un titre chinois de 90 px traversant les yeux d'une personne est destructeur même avec un masque.

### Composition discipline (editorial look)

Ces quatre règles sont ce qui sépare un poster éditorial d'une image générique avec texte :

- **Asymmetric placement.** Les titres décalés d'un côté / d'un coin se lisent plus confiants que ceux centrés. L'habitude Kinfolk / Cereal.
- **Generous negative space.** Le titre doit occuper ≤40% du canevas. La photo et la zone calme vide font le travail de design.
- **Title in one quiet zone, only one.** Diviser le titre en deux zones (haut + bas) est bien ; le diviser en trois ou l'enrouler autour du sujet est encombré.
- **Title never overlaps the subject silhouette.** Si le seul placement sûr nécessite de franchir le bord du sujet, changez de mode (passez à un cadre, diptyque, ou titre hors-image) — n'agrandissez pas le masque.

### Crop guards

La règle d'évitement du visage devrait également guider `object-position`. Si le sujet est dans le tiers supérieur, n'utilisez pas `object-position: center top` (cela pousse le visage dans la bande de titre).

| Subject location in raw image | Recommended `object-position` for 3:4 crop |
| ----------------------------- | ------------------------------------------ |
| Face / focus in upper third   | `center 25%` (éleve le visage plus haut, donne de l'espace en bas pour le titre) |
| Face / focus in middle third  | `center center` (par défaut ; texte en haut + bas) |
| Face / focus in lower third   | `center 70%` (abaisse le visage, espace en haut pour le titre) |
| Wide landscape, no single subject | `center 35%` (léger biais vers le haut pour conserver la ligne d'horizon) |
| Vertical portrait, full body  | `center top` |

### When the photo cannot accommodate text

Si l'exécution de la carte du sujet montre qu'il n'y a pas de zone sûre plus large que ~30% de l'affiche (le sujet remplit le cadre, par ex. portrait serré), ne le bricolez pas. Options :

- Déplacez la photo dans un **cadre plus petit** (utilisez `.frame-img.r-3x4` ou `.r-1x1` à l'intérieur de la mise en page — donnez-lui un emplacement défini, entourez-la d'espace blanc et de texte).
- **Diptyque à deux images** avec un sujet serré + une image à espace négatif, faites passer les titres sur celle à espace négatif.
- **Déplacez le texte hors de l'image entirely** — titre en haut, photo en bas. La couverture Yading le fait déjà.

Une photo qui exige le plein canevas n'est pas un signe que le texte devrait se battre avec elle. C'est un signe que le texte devrait se placer ailleurs.

---

## Checklist before delivery

Faites ceci pour chaque affiche où le texte touche une image :

- [ ] La photo passe le test de zone calme (bande ≥30% du canevas faible en détails) ET le test de lumière (atmosphérique, pas de midi saturé).
- [ ] Essayé la composition sans masque en premier. Teinte ajoutée uniquement si l'étape 4 de test de contraste a échoué.
- [ ] Si teintée : localisée (`radial-gradient` ou unilatérale), couleur image-tonée (pas noir pur), alpha maximal ≤ 0.30.
- [ ] Pas de dégradé vertical pleine page présent (`linear-gradient(180deg, rgba(0,0,0,.X) → ...)` sur `inset:0`).
- [ ] Carte du sujet documentée comme commentaire près du bloc principal.
- [ ] Aucun titre d'affichage (≥ 72 px) ne chevauche un visage / main / caractéristique clé de produit / silhouette de sujet.
- [ ] Titre occupe ≤40% du canevas. Placement asymétrique préféré au centré.
- [ ] `object-position` choisi depuis le tableau ci-dessus, pas laissé par défaut `center top` pour les portraits.
- [ ] Test de miniature réussi (réduction à 360 px de large ; titre encore lisible sans effort).
- [ ] Pas de plaque noire/blanche plate derrière le titre.

Si un élément échou, réparez-le avant d'exporter le PNG final. Ne livrez pas et "nous ajusterons plus tard" — la fenêtre QA pour les cartes sociales est le moment du téléchargement.
