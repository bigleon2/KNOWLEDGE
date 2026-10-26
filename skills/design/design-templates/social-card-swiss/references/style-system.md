# Système de style

Cette compétence extrait les principes visuels de Guizang PPT pour les images sociales statiques. Elle ne dépend pas des modèles PPT originaux.

## Règles partagées

- La forme du contenu détermine la mise en page. Ne choisissez pas d'abord une mise en page attrayante et inventez du contenu pour l'adapter.
- Utilisez une forte hiérarchie : titre, accroche, preuve, légende, métadonnées.
- Utilisez de vraies images comme preuves ou pour l'ambiance, pas comme décoration.
- Évitez le désordre visible : aucun cercle SVG aléatoire, gouttes ovales, amas, bokeh, autocollants décoratifs, fausses décorations de diagrammes ou dégradés décoratifs.
- Gardez toutes les pages d'un package visuellement liées par grille, typographie, palette et métadonnées récurrentes.
- Chaque page doit avoir un point focal clair.

## Style ↔ type de contenu sont découplés

Les deux modes ci-dessous sont **des positions visuelles, pas des catégories de contenu**. N'importe quel sujet peut être rendu dans l'un ou l'autre mode - ce qui change est le sentiment de la page et les dispositifs structurels disponibles (ledger / marginalia / citation extraite vs matrice / KPI tower / h-bar). Choisissez par intention éditoriale ("article à la une" vs "note de version" / "explicateur système"), pas par recherche de sujet. Les listes ci-dessous sont des *bonnes correspondances*, pas exhaustives.

## Mode A : Magazine éditorial x E-ink

Bonnes correspondances : outdoor, lifestyle, réfléchi, humaniste, culturel, narratif — mais aussi essais de lieu de travail, réflexions sur l'IA, rétrospectives de produit, tout ce qui veut un rythme de magazine à la une lent.

Ancres visuelles :

- Titre d'affiche Serif ou Songti-like (style de police chinoise traditionnelle) avec du corps de texte sans-serif discret.
- Papier chaud, encre profonde, gris raffinés, couleurs mesurées.
- WebGL ou atmosphère/encre procédurale/contour, surtout sur les couvertures, séparateurs, citations extraites et pages éparses.
- Photographie documentaire, légendes de notes de terrain, étiquettes de numéro, numéros de page.
- Grand blanc mais avec intention.
- Lignes fines, colonnes de magazine, légendes d'images, citations extraites, contraste éditorial.
- Une texture de papier subtile est autorisée ; elle ne doit pas réduire la lisibilité du texte.

Utilisez l'une des 6 palettes magazine dans `theme-presets.md`. N'improvisez pas de couleurs de papier chaud arbitraires. Cinq palettes sont claires (papier-et-encre) ; une — **Midnight Ink** — est la seule variante sombre approuvée, réservée au contenu où l'imagerie source est déjà sombre (art de jeu, photographie de nuit, couvertures cinématiques). N'inventez pas une deuxième palette sombre.

**Position typographique — "plus grand, plus léger."** Cette règle est non négociable pour l'Éditorial. Les titres d'affiche s'exécutent à **weight 500** avec **tracking large** (`.+03em` à `.+04em`). Le petit texte (accroche, méta, étiquette) est le *seul* endroit où le weight 500 est associé à majuscules mono et espacement large (`.+20em` à `.+22em`). Le corps utilise **serif-zh**, pas sans. Le contre-modèle — poids d'affichage 700 à 900, corps sans, tracking négatif — réduit l'Éditorial à un look générique de "bannière d'infographie". Si une page semble lourde ou criarde, le titre est trop gras ou le corps est passé au sans. Voir `local-tests/demo-showcase/editorial.html` pour la source de vérité.

Motifs de mise en page :

- Couverture : grand titre en haut ou à gauche, grande photo/image de preuve, liste de contrôle ou bande de numéro en bas.
- Page à la une : une grande image plus une colonne étroite d'explication compressée.
- Page de liste : en-tête éditorial, éléments numérotés, une image de support coupée ou un diagramme sans icône.
- Page citation/enseignement : grande citation extraite avec petite ligne source/contexte.
- Page de comparaison : tension à deux colonnes, étiquettes simples, une ancre visuelle.

Règle de fond :

- Une couleur de papier plate n'est pas suffisante pour ce mode. Utilisez un fond multicouche de `background-systems.md` : base de papier, grain subtil, lavis d'encre ou champ de contour, et toile WebGL optionnelle. Le fond doit créer de l'ambiance tout en maintenant la lisibilité du texte.

## Mode B : Suisse International

Bonnes correspondances : outils d'IA, mises à jour produit, workflows d'ingénierie, explicatifs logiciels, notes de version, publications de comparaison — mais aussi carnets de voyage, journaux de dépenses, données de fitness, décomptes d'étapes de recette, tout ce qui veut un rythme ingénieur/quantifié. Le sujet n'est pas la porte ; la position visuelle l'est.

Ancres visuelles :

- Inter, Helvetica Neue, sentiment Noto Sans SC.
- Poids très légers pour le grand type ; poids plus forts pour les petites étiquettes.
- Grille stricte 12/16 colonnes, alignement à gauche, blanc asymétrique.
- Blanc/blanc cassé, noir, gris raffinés, exactement une accentuation haute saturation.
- Modules droits, lignes fines, pas de cartes arrondies, pas d'ombres, pas de glassmorphism.

Utilisez l'une des 4 palettes d'accentuation Suisse dans `theme-presets.md`. Un package obtient exactement une accentuation.

Règles :

- Utilisez une seule accentuation. Ne mélangez pas bleu, jaune, vert et orange.
- Évitez les dégradés. Utilisez des blocs de couleur pure, des lignes fines et des modules de grille.
- Les titres se situent généralement sur l'axe de contenu en haut à gauche, pas au centre, sauf pour les couvertures carrées spéciales ou les compositions d'affiche explicites.
- Le grand texte doit être plus léger ; le petit texte doit être plus lourd.
- Les images sont des blocs de preuve. Utilisez des bords droits et des conteneurs à ratio d'aspect stable.

Conseils typographiques :

| Rôle | Indication de taille | Poids |
| --- | --- | --- |
| Titre principal de couverture | 84-128px sur 1080x1440 | 200-400 |
| Titre de page | 52-82px | 300-500 |
| Copie du corps | 28-42px | 400-500 |
| Légendes/méta | 20-28px | 500-650 |

Les titres chinois sont visuellement denses. Raccourcir d'abord, puis réduire la taille. Ne résolvez pas le dépassement en réduisant le texte du corps en dessous de la lisibilité.

## Règles d'image

- Photos : coupez avec intention. Gardez les visages, mains, produits et objets principaux dans des zones sûres.
- Captures d'écran de produit : préservez le texte ; utilisez `object-fit:contain` quand les détails sont importants.
- Photos de matériel : faites de l'objet un signal de première vue. La photo doit être assez grande pour être inspectée.
- Images générées : générez seulement le contenu de l'image, pas l'affiche finale avec texte.
- Ne faites pas inclure des images générées avec chrome de page, titres, bordures, légendes ou fausses UI sauf si requis par le concept.

## Mauvaises odeurs

Réviser si vous voyez :

- Une page qui ressemble à un modèle générique avec l'article collé dedans.
- Grande zone vide en bas sur plusieurs pages.
- Formes décoratives qui n'expliquent rien.
- Captures d'écran trop petites pour être lues.
- Marges incohérentes entre pages.
- Texte bleu sur noir ou photo sombre avec mauvais contraste.
- Une couverture 1:1 qui est un crop serré d'une couverture 21:9.

## Test d'identité de style

Une affiche compile proprement bien avant que son identité de style soit correcte. Lancez ce test sur chaque page avant livraison.

### Test d'identité Suisse

Une affiche est Suisse seulement si **les quatre** tiennent :

1. Chaque grand titre d'affichage (>=72px sur 1080x1440) utilise une classe typée de `components.md` (`.h-hero` / `.h-statement` / `.h-xl` / `.num-mega`). Son `font-weight` calculé est `<=300`.
2. Aucune famille serif n'est chargée dans l'en-tête du document. Aucun élément n'utilise `font-family: serif` ou `Noto Serif SC` / `Playfair Display`.
3. Les séparateurs de section sont des lignes fines (1-2px) ou des gouttières de grille, pas des bordures de carte + ombres portées.
4. Exactement une palette d'accentuation est en utilisation. Pas d'accentuations mélangées entre pages.

Si l'une de ces échoue, l'affiche n'est pas Suisse — elle est éditoriale générique ou "carte Suisse-aromatisée". Corrigez-la ou renommez le package.

### Test d'identité Éditorial

Une affiche est Éditoriale seulement si **les trois** tiennent :

1. Le fond a au moins une couche d'ambiance au-delà d'un remplissage plat : grain de papier, lavis d'encre, toile WebGL gelée ou champ de contour (voir `background-systems.md`). Un `#f3f0e8` solide sur toute la page avec rien par-dessus n'est pas Éditorial.
2. Le titre d'affichage utilise une famille serif-zh / serif-en (`Noto Serif SC` / Songti SC / Playfair Display).
3. L'affiche contient au moins un des : un grand puits de photo, une citation extraite serif avec anglais en em-italic, une colonne de marginalia gauche/droite, ou un carnet avec vraie hiérarchie de rangée de magazine.

Si une affiche a un titre serif, étiquettes mono partout, grilles de pilotes structurées, et un fond de papier plat — c'est **Suisse-avec-serif**, pas Éditorial. Ajoutez soit ambiance + structure magazine, ou basculez le package en Suisse honnêtement.

## Anti-modèles à partir de vrais démos

Tous ont été rendus sans erreur et semblaient plausibles en isolation, mais ont échoué une fois comparés à une référence propre.

### Anti-modèle A : gros titre épais en Suisse

```html
<!-- MAUVAIS : poids inline 700-800 sur un gros titre -->
<h1 style="font-size: 92px; font-weight: 800">如果只能留 5 个,我留这些。</h1>

<!-- BON : classe typée, poids automatique 200-300 -->
<h1 class="h-statement">如果只能<br>留 <em>5 个</em>,<br>我留这些。</h1>
```

"Plus grand, plus léger" est une règle stricte. Un h1 de 90px à weight 700+ dégrade instantanément le design de Suisse International en éditorial de page de générique. Toujours atteindre pour `.h-hero` / `.h-statement` / `.h-xl` / `.num-mega`. Ne les contournez pas avec `font-size` + `font-weight` inline.

### Anti-modèle B : Éditorial sans ambiance

Une page avec tout ce qui suit ressemble à Suisse-en-déguême même si vous vouliez Éditorial :

- Couleur de papier plate unique, pas de grain, pas de lavis d'encre, pas de WebGL,
- Étiquettes mono (`IBM Plex Mono majuscules`) sur chaque accroche, pied, pilote et étiquette de rangée,
- Un titre serif flottant seul sans grande image, citation extraite ou colonne de marginalia.

Corrigez par **une** de :

- Ajoutez le grain de papier + fond de lavis d'encre selon `background-systems.md`.
- Remplacez les étiquettes mono par micro copie serif / italique.
- Introduisez une grande photo ou citation extraite serif avec structure de colonne.
- Basculez le package en Suisse honnêtement — le contenu pourrait vouloir Suisse.

### Anti-modèle C : chevauchement de pied de page (article de clôture entre en collision avec `.foot`)

Quand `.foot` ou `.issue-strip` est positionné avec `position: absolute; bottom: ...`, tout contenu au-dessus qui dépasse sa hauteur attendue traverse le pied de page. Utilisez à la place l'un de ces motifs sûrs :

```css
/* Motif A — colonne flex. Foot est le dernier enfant, poussé par margin-top: auto. */
.poster .pad { display: flex; flex-direction: column; height: 100%; }
.poster .foot { margin-top: auto; }

/* Motif B — grille avec ligne de pied de page fixe. */
.poster .pad { display: grid; grid-template-rows: auto 1fr auto; height: 100%; }
```

Les deux modèles de départ utilisent déjà le Motif A. Préservez-le. Si une recette a vraiment besoin d'un pied de positionné absolument, réservez `padding-bottom: <hauteur-pied + 24px>` sur le conteneur de contenu.

### Anti-modèle D : photo pleine page avec titre traversant le sujet

L'affiche semble dramatique à 100% de zoom et illisible en taille miniature. Deux sous-échecs courants :

- Une photo hero couvre toute l'affiche, le titre s'assied directement sur n'importe quel pixel se trouvant derrière. La propre luminosité de l'image varie sur la toile, donc le titre est lisible dans certaines bandes et invisible dans d'autres.
- Une couche de masque est présente mais seulement sur une bande (bas), tandis que le visage du sujet a été poussé en haut par `object-position: center top`. Le titre d'affichage atterrit sur le visage.

Les deux passent le lint HTML ; les deux échouent le test de lisibilité miniature.

Corrigez en suivant `image-overlay.md` :

1. **Qualifiez d'abord la photo.** Elle a besoin d'une zone calme de faible détail et de lumière mesurée. Si elle échoue, basculez vers une recette de photo encadrée au lieu de forcer le texte par-dessus.
2. **Cartographiez le sujet avant de placer le titre.** Lisez l'image, décrivez en langage simple où le visage/point focal se situe, enregistrez la carte du sujet comme commentaire HTML à côté du bloc hero. Placez du texte seulement dans les zones sûres documentées.
3. **Adaptez `object-position` à l'emplacement du sujet** — voir le tableau dans `image-overlay.md`. Ne le laissez jamais par défaut pour les visages / photos hero.
4. **Test miniature** — rendez le PNG, réduisez à 360 px de large, et regardez le titre. S'il lutte contre la photo, ajoutez une teinte localisée, ton image, seulement autour de la zone du titre ; si la photo semble morte, la teinte est trop lourde ou la photo est mauvaise.

Cet anti-modèle survit à presque tous les autres tests car le HTML est valide, l'image charge et le titre rend. La seule façon de le repérer est de regarder le rendu à la taille où les lecteurs la verront réellement.
