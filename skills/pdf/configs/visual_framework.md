# Visual Framework — Aesthetic Axioms

Système de design non-template. Ce fichier est le cadre de réflexion du LLM — pas une liste de styles parmi lesquels choisir, mais un ensemble de lois immuables qui régissent chaque décision de design.

---

## Les Trois Absolus

1. **Restrainte** — Retirer jusqu'à ce que ça fasse mal. Puis retirer encore une chose.
2. **Contraste** — Hiérarchie par l'échelle et le poids, jamais par la multiplication des couleurs.
3. **Métaphore de l'Espace** — Chaque page a une énergie physique : gravité, tension, respiration.

### L'Impératif Anti-Vulgaire

> **En cas de doute, retirer. Jamais ajouter.**

Un document semble "bon marché" ou "土" (tǔ - vulgaire/rustique) quand il a trop d'éléments visuels concurrents. Le remède est toujours la soustraction, jamais le réagencement.

**Signes d'alarme qu'un design est vulgaire :**
- Plus de 3 éléments décoratifs sur une seule page de contenu
- Icônes ou emoji utilisés comme décoration d'en-tête de section (utiliser la typographie à la place)
- Bordures ou cadres décoratifs autour du contenu
- Arrière-plans avec motif/texture sur les pages de contenu
- 3+ familles de teintes différentes visibles simultanément
- Éléments ajoutés "parce qu'il y a de l'espace vide" plutôt que pour une fonction

**La solution est toujours :** Supprimer l'élément décoratif. Si la page communique toujours son message clairement, elle n'avait pas besoin de la décoration. Si ce n'est pas le cas, corriger la hiérarchie typographique — pas en ajoutant plus de bruit visuel.

### 🚫 L'Interdiction des Images de Banque / Clipart / Décorations Générées par IA

> **INTERDICTION ABSOLUE : Ne PAS intégrer de photos de banque, clipart, illustrations aquarelles, images générées par IA (fleurs, motifs, bordures, cadres, ornements), ou tout artwork décoratif raster/vectoriel dans les documents PDF.**

C'est la source n°1 de designs "bon marché" / "土" (tǔ - vulgaire/rustique) / "婚庆风" (hūnqìngfēng - style invitation de mariage). Exemples de ce qui EST INTERDIT :
- ✘ Fleurs aquarelles / roses / coins floraux / bordures de vignes
- ✘ Cadres ou bordures décoratifs dorés/métalliques
- ✘ Arrière-plans de photos de banque (paysages, textures, marbre)
- ✘ Illustrations en clipart (rubans, nœuds, cœurs, étoiles)
- ✘ Artwork décoratif généré par IA (fleurs DALL-E, motifs Midjourney)
- ✘ Toute balise `<img>` utilisée à des fins purement décoratives (non informatives)
- ✘ Photos de banque Unsplash/Pexels/Pixabay utilisées comme arrière-plan ou décoration

**Ce QUI EST AUTORISÉ :**
- ✔ Formes géométriques rendues en CSS/SVG (cercles, lignes, rectangles — depuis `geometry.md`)
- ✔ Décoration basée sur la typographie (lettres surdimensionnées, texte filigrane, effets d'espacement des lettres)
- ✔ Blocs de couleur et dégradés (dans les règles de palette)
- ✔ Photos/logos fournis par l'utilisateur qui sont du CONTENU (pas de décoration)
- ✔ Graphiques et visualisations de données
- ✔ Diagrammes qui transmettent des informations

**Le principe :** Si retirer une image ne réduit pas le contenu informationnel du document, cette image est une décoration et devrait être remplacée par de la typographie ou des éléments géométriques.

**Invitations de mariage, cartes d'événement, certificats :** Utiliser une typographie élégante + accents géométriques (lignes fines, formes minimales) + beaucoup d'espace blanc. Un nom superbement mis en page en 48pt serif avec 6pt d'espacement des lettres est infiniment plus élégant que des roses aquarelles.

---

## Axiomes de Couleur

### La Loi 60-30-10

Chaque design se compose exactement de trois zones tonales :

| Zone | Couverture | Rôle | Généré par |
|------|----------|------|-------------|
| **60% — Fond** | Arrière-plan, marges, espace vide | Fixe l'humeur ; le spectateur ne "voit" pas consciemment | `--c-bg` depuis `design_engine.py` |
| **30% — Structure** | Cartes, séparateurs, zones secondaires | Fournit l'architecture ; même famille de teinte que le fond, luminosité différente | `--c-mid` |
| **10% — Accentuation** | Titres, nombres clés, un élément d'accentuation | Attire le regard ; seul endroit où la "couleur" existe | `--c-accent` |

### Discipline de Saturation (RÈGLE FERME)

Toutes les couleurs passent par `design_engine.py` qui impose :
- **Plage de saturation** : 0.05 – 0.25 (HSL). Ceci est non négociable.
- **Aucune primaire pure** : Rouge pur (#ff0000), bleu pur (#0000ff), jaune pur (#ffff00) sont interdits.
- **Max 3 teintes** dans tout le document. Les variations de luminosité/saturation ne comptent pas comme des teintes séparées.

### Polarité de Luminosité

Seuls deux régimes de luminosité existent. Le milieu est interdit.

| Mode | L de fond | L de texte | Zone Interdite |
|------|-------------|--------|----------------|
| **Sombre** (Cinématique) | < 0.10 | > 0.85 | L entre 0.30–0.70 pour les fonds |
| **Clair** (Éditorial) | > 0.95 | < 0.15 | L entre 0.30–0.70 pour les fonds |

Les tons moyens troubles (L 0.30–0.70) pour les fonds donnent l'aspect "application web bon marché". Jamais.

### Ce que la Couleur n'est Pas Pour

La couleur ne crée pas de hiérarchie. La taille et le poids le font.

| ❌ Faux | ✅ Correct |
|----------|---------|
| Titre bleu, sous-titre gris, corps noir | Toute même teinte ; titre 900 poids 48px, sous 600 36px, corps 400 16px |
| Étiquettes/badges colorés pour les catégories | Étiquettes monochromes avec variation de poids de bordure |
| Texte dégradé sur tout | Texte dégradé sur exactement UN élément principal, nulle part ailleurs |

---

## Axiomes de Typographie

### Le Poids est la Nouvelle Couleur

La hiérarchie vient du contraste entre les extrêmes de poids :

| Élément | Poids | Taille relative au corps |
|---------|--------|----------------------|
| Titre principal | 100 (Fin) OU 900 (Noir) | 4–6× corps |
| Titre de section | 700 | 2× corps |
| Corps | 400 | 1× (de base) |
| Légende / métadonnées | 300 | 0.7× corps |

L'écart entre le titre principal et le corps doit être **dramatique** — au moins un ratio de 4× de taille. Moins que cela semble timide.

### Règles de Police

- **Max 2 familles par page**. Une serif, une sans (ou une d'affichage, une de texte). Jamais trois.
- **Chaque `font-family` doit se terminer par un générique** : `sans-serif`, `serif`, ou `monospace`.
- **Pour l'impression physique (>500mm)** : Utiliser `pt`/`mm` pour les tailles de police, jamais `px`.

### Hauteur de Ligne par Densité

| Type de Contenu | Hauteur de Ligne | Pourquoi |
|-------------|------------|-----|
| Texte de corps, paragraphes | 1.6–1.8 | Lecture confortable |
| Titres | 0.85–1.0 | Étroit, sculptural — les titres sont des objets visuels, pas des phrases |
| Légendes, métadonnées | 1.4 | Compact mais lisible |

---

## Axiomes d'Espace

### La Règle de la Marge Respiratoire (OBLIGATOIRE)

Chaque page doit avoir une **marge claire de 10–12%** sur tous les bords. Rien — aucun texte, aucune décoration, aucune carte — ne peut entrer dans cette zone.

Le pourcentage exact dépend de la densité du contenu :
- **Contenu clairsemé** (pages principales, couvertures) : 15% est bien — beaucoup d'air
- **Contenu standard** (éditorial, données) : **12%** est le point idéal
- **Contenu dense** (tableaux, grilles de statistiques) : 10% minimum — plus serré mais toujours respirable

Défaut dans `design_engine.py` : `inset: 10% 12%` (vertical 10%, horizontal 12%).

```
┌──────────────────────────────┐
│  10-12% marge (respiration)   │
│  ┌────────────────────────┐  │
│  │                        │  │
│  │    Le contenu vit ici   │  │
│  │    (76-80% du canevas)  │  │
│  │                        │  │
│  └────────────────────────┘  │
│  10-12% marge (respiration)   │
└──────────────────────────────┘
```

Les arrière-plans SVG décoratifs peuvent s'étendre dans la zone de marge (ils sont atmosphériques, pas du contenu). Mais tous les éléments lisibles la respectent.

### L'Espace Négatif est du Contenu

L'espace vide n'est pas "de l'espace gaspillé". C'est un élément compositionnel :
- Un poster avec 50% d'espace blanc communique **la confiance**
- Un poster encombré à 90% communique **le désespoir**
- Le ratio de contenu à vide fixe le ton émotionnel

### Règle de Proximité

Les éléments liés sont proches. Les éléments non liés sont éloignés. L'écart entre les éléments non liés devrait être **au moins 3× l'écart entre ceux qui liés**.

---## Intent → Traduction Visuelle

Cinq intentions de conception. Chacune décrit une **ambiance** — le champ émotionnel que le spectateur devrait ressentir. Les intentions NE PRÉSCRIVENT PAS de paramètres spécifiques (graisse de police, interligne, type de SVG, etc.). Toutes les correspondances de paramètres concrets se trouvent dans `briefs/creative-fixed-canvas.md` § Table de Mappage des Intentions et `design_engine.py` INTENT_HUES/INTENT_HARMONY_MAP.

### Calme
Immobilité. La respiration du spectateur ralentit. Espace ouvert vaste, palette restreinte, rien ne rivalise pour l'attention. Couvre la santé, le bien-être, la méditation et les esthétiques minimalistes. La conception communique par ce qu'elle *supprime*.

### Tension
Conflit. Angles vifs, contraste dramatique, éléments qui se repoussent. Urgence, crise, disruption. La page a une énergie physique — quelque chose est sur le point de se briser ou s'est déjà brisé.

### Énergie
Mouvement. Composition dense, légères rotations, chaleur. Marketing, lancements, campagnes sociales. La conception vibre — elle veut sortir de la page. Rien n'est parfaitement centré.

### Autorité
Gravitas. Formel, délibéré, symétrique. Gouvernement, finance, luxe, corporate haut de gamme. Chaque élément est placé avec une précision chirurgicale. La commande de respect par la conception par la retenue et le poids.

### Chaleur
Confort. Bords arrondis, espacement généreux, tons terrestres. Nourriture, mode de vie, maison. La sensation ressemble à une pièce chaude — accueillante, douce, humaine.

---

> **Mappage hérité** : Sérénité → Calme, Minimalisme → Calme, Élégance → Autorité. Les anciens noms d'intentions sont acceptés comme alias dans `design_engine.py` pour la compatibilité ascendante.

---

## Techniques Visuelles Avancées

### Sémantique - Typographie Topologique (Score de Tension)

Le texte n'est pas visuellement plat — son "poids" devrait refléter son intensité émotionnelle. Quand un document a un arc narratif (introduction calme → crise → résolution), la graisse de police devrait respirer avec lui.

**Le Principe** : Attribuer un `tension_score` (0.0–1.0) aux composants `Glass_Canvas`. Le moteur mappe cela à une graisse de police continue via la police de variable Inter (axe 300–900).

**Quand cela compte** :
- Documents de 3+ pages avec des déplacements émotionnels clairs
- Récit : études de cas, présentations de pitch, manifestes
- Le lecteur ne remarquera pas consciemment, mais la variation de poids inconsciente crée une "texture" dans l'expérience de lecture — de la même manière qu'une bande sonore de film opère en dessous de la conscience

**Quand sauter** :
- Affiches d'une seule page (pas d'arc à exprimer)
- Rapports riches en données (les nombres n'ont pas "de sentiments")
- Documents courts où tous les paragraphages partagent le même ton

### Continuité Visuelle Inter-Pages (Flux Continu)

Les documents multi-pages ne sont pas une collection d'affiches isolées — c'est un voyage. L'arrière-plan devrait refléter cela.

**Le Principe** : Au lieu de générer des SVG indépendants par page, générer UNE courbe de bézier continue s'étendant sur toute la hauteur du document, puis la découper par page via SVG `viewBox`. Le résultat : des courbes qui sortent du bord inférieur d'une page entrent de manière transparente dans le bord supérieur de la page suivante.

**Quand utiliser `continuous_flow`** :
- Documents multi-pages (2+) avec une structure narrative
- Documents voyage/chronologie
- Pièces de marque où la sophistication transparente compte
- Mieux associé à : intentions `Chaleur`, `Élégance`, `Sérénité`

**Quand utiliser `flow` régulier à la place** :
- Documents d'une seule page (le continu n'a pas de sens)
- Chaque page est conceptuellement indépendante (pas une histoire)

### Enveloppement de Forme Sémantique (Shaped_Canvas)

La plus dramatique des trois techniques. Le texte s'enroule autour de formes géométriques invisibles, et l'espace négatif lui-même devient l'illustration.

**Le Principe** : Un `<div>` flottant avec CSS `shape-outside` crée une limite non rectangulaire pour le flux de texte. Le vide laissé par la forme est l'élément de conception.

**L'inspiration clé** : Nous n'ajoutons pas une image — nous sculptons le TEXTE en forme. C'est un minimalisme extrême : zéro actif visuel, impact visuel maximal.

**Quand utiliser** :
- Pages qui ont un "wow" sans images
- Ouvrages de section, alternatives de couverture
- Contenu qui se connecte thématiquement à une forme (océan → vague, progrès → coin)
- Pages avec densité de texte modérée (100–200 mots) — la forme a besoin d'espace

**QUAND NE PAS UTILISER** :
- Pages de contenu dense (la forme mange 30-40% de la zone de texte → risque de dépassement)
- Avec `Glass_Canvas` sur la même page (conflits backdrop-filter)
- Plus d'un par page (chaos visuel)

---

## Tests de Qualité

Avant la livraison, chaque page doit passer ces tests :

| Test | Méthode |
|------|--------|
| **Test à 3 mètres** | Peut-on lire le titre de 3 mètres de distance ? (hiérarchie des tailles) |
| **Test de plissement** | Plisser les yeux sur la page — voit-on des zones sombres/claires distinctes ? (contraste) |
| **Test magazine** | Cela pourrait-il être une page dans Monocle, Kinfolk, ou Cereal magazine ? (goût) |
| **Test de suppression** | Peut-on supprimer un élément sans perdre du sens ? Si non, on a trop peu. Si oui, supprimez-le. |
| **Compte de couleurs** | Compter les teintes distinctes. Si > 3, vous avez échoué l'axiome des couleurs. |
| **Vérification de saturation** | Exécuter `design_engine.py audit` — tout S > 0.25 sur non-accent = violation |
| **Test de respiration** | Y a-t-il 15% de marge claire sur tous les bords ? |
| **Cohérence** | Toutes les pages partagent-elles la même paire de polices, jetons de couleur, épaisseur de ligne et rayon de coin ? |
