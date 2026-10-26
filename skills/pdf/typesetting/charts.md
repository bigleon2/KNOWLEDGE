# Conception de graphiques — Règles de mise en page et d'empilement anti-collision

> Principe fondamental : **Ratio Encre-Données** — supprimez chaque ligne qui ne représente pas de données. Puis supprimez encore un peu plus.

---

## Partie 1 : Empilement anti-collision (prévention des collisions)

L'empilement de texte est fondamentalement une "densité d'informations dépassant l'espace physique disponible". Appliquez ces stratégies de dégradation dynamique.

### 0. Pré-vérification universelle anti-recouvrement (OBLIGATOIRE)

**Avant de RENDRE N'IMPORTE QUEL graphique, exécutez cette vérification préalable :**

```python
# Étape 1 : Réserver de l'espace pour les étiquettes D'ABORD, puis dessiner le graphique
# FAUX : dessiner le graphique → ajouter des étiquettes → découvrir un recouvrement → pleurer
# CORRECT : mesurer les étiquettes → réserver de l'espace → dessiner le graphique dans l'espace restant

# Étape 2 : Séparation graphique-texte
CHART_TEXT_MIN_GAP = 12  # pt — espace minimum entre le bord du graphique et le texte adjacent
CHART_LABEL_MIN_GAP = 6  # pt — espace minimum entre les étiquettes du graphique et les éléments du graphique

# Étape 3 : Vérification de collision étiquette-étiquette
def labels_overlap(label_a, label_b):
    """Vérifie si les boîtes englobantes de deux étiquettes se chevauchent."""
    return not (label_a.right < label_b.left or
                label_a.left > label_b.right or
                label_a.bottom < label_b.top or
                label_a.top > label_b.bottom)

# Étape 4 : Cascade de résolution
# 1. Repositionner (déplacer légèrement l'étiquette en conflit)
# 2. Réduire la taille de la police (min 8pt)
# 3. Supprimer l'étiquette (remplacer par une entrée de légende)
# 4. Fusionner les petits éléments (regroupement "Autres")
```

**Anti-recouvrement spécifique à Matplotlib :**
```python
# OBLIGATOIRE pour tous les graphiques matplotlib
import matplotlib.pyplot as plt
from adjustText import adjust_text  # pip install adjustText

# Après avoir ajouté des annotations de texte :
# adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

# Pour les étiquettes de valeur de barre :
fig.tight_layout(pad=2.0)  # Toujours utiliser un remplissage généreux
plt.subplots_adjust(bottom=0.15)  # Réserver de l'espace pour les étiquettes tournées

# Pour les graphiques circulaires/anneaux :
# étiquettes autopct : vérifier la distance angulaire entre les tranches adjacentes
# Si l'angle < 15°, utiliser des étiquettes externes avec des lignes de liaison
```

**Séparation graphique-texte corporel (ReportLab) :**
```python
# Espaces obligatoires autour des éléments graphiques dans le flux
story.append(Spacer(1, 24))       # espace de 24pt avant le graphique
story.append(chart_image)          # Graphique
story.append(Spacer(1, 8))        # espace de 8pt
story.append(chart_caption)        # Légende
story.append(Spacer(1, 24))       # espace de 24pt après le graphique
# JAMAIS placer un graphique sans espaces de garde
```

### 1. Graphique circulaire/Anneau — Prévention des collisions d'étiquettes

Lorsque les tranches sont trop petites, les étiquettes NE DOIVENT PAS être placées à l'intérieur de l'arc.

#### Stratégie A : Lignes de liaison + Évitement de collision avec l'axe Y

Lorsque l'angle de la tranche `< 15°` (ou la part de surface `< 5%`), forcer les étiquettes externes :
- Dessiner une polyligne (ligne de liaison) du bord externe de l'arc au texte de l'étiquette
- **Logique anti-collision axe Y** : Calculer les coordonnées Y des étiquettes adjacentes. Si `Y2 - Y1 < font_height + padding`, pousser `Y2` vers le bas (ou tirer `Y1` vers le haut). Allonger/raccourcir le segment horizontal de la ligne de liaison en conséquence.
- Lignes de liaison : 1pt, même couleur que la tranche à 60% d'opacité

#### Stratégie B : Regroupement "Autres" (Fusion de la longue traîne)

Avant que les données n'atteignent le moteur de rendu, intercepter et fusionner :
- Seuil : tranches `< 3%` → fusionner en une seule tranche "其他 (Autres)"
- Si des détails sont nécessaires, ajouter un tableau minimal à côté du graphique montrant le détail
- Cela empêche 5+ petits fragments d'encombrer le graphique

#### Stratégie C : Étiquettes supprimées, légende riche

L'approche premium — **zéro texte sur le graphique lui-même** :
- Le corps du graphique circulaire/anneau montre uniquement des formes pures + couleurs
- Tous les noms, pourcentages et valeurs sont disposés dans une grille alignée de légende à droite ou en dessous
- Cela NE JAMAIS s'empile et a l'aspect le plus professionnel

**Ordre de priorité** : C (meilleur) → A (bon) → B (solution acceptable)

---

### 2. Graphique en barres — Prévention des collisions d'étiquettes

#### Stratégie A : Rotation automatique en barres horizontales

**Règle stricte** : Lorsque la longueur moyenne des étiquettes de l'axe X dépasse **5 caractères chinois** (ou 10 caractères latins), convertir automatiquement en graphique en barres horizontales.
- L'axe Y a un espace inférieur vers le bas pour les étiquettes — l'empilement est impossible
- C'est la mesure anti-collision la plus efficace pour les graphiques en barres

#### Stratégie B : Éclaircissement des graduations + Alternance

Lorsqu'il y a de nombreuses barres (par exemple, tendance sur 30 jours) :
- **Éclaircissement** : Afficher chaque 2ème ou 5ème étiquette (sauter les graduations intermédiaires)
- **Alternance** : Alterner les étiquettes entre deux lignes (décalage vertical)
- **Inclinaison (dernier recours)** : La rotation à 45° fonctionne mais réduit la lisibilité dans les rapports premium. Préférer l'éclaircissement ou les barres horizontales.

#### Stratégie C : Inversion intérieur/extérieur des étiquettes de valeur

- Si la barre est suffisamment haute : placer l'étiquette de valeur **à l'intérieur** de la barre près du haut (utiliser une couleur de texte contrastée)
- Si la barre est trop courte pour une étiquette interne : placer la valeur **au-dessus** de la barre
- Si les étiquettes de valeur se chevauchent entre barres adjacentes : afficher les valeurs uniquement sur les barres les plus hautes/plus basses, ou utiliser des boîtes d'appel de style infobulle

---

### 3. Graphique en courbe — Prévention des étiquettes de points de données

Des points de données denses avec des étiquettes sur chaque point = chaos visuel.

#### Stratégie A : Règle "Premier, Dernier, Max, Min" (Standard en journalisme de données)

Ne mettre d'étiquettes automatiquement que sur **4 points** de n'importe quelle ligne :
- **Point de départ** (première valeur)
- **Point d'arrivée** (dernière valeur)
- **Maximum** (pic)
- **Minimum** (creux)

Tous les autres points montrent uniquement la forme de la courbe — pas d'étiquettes. Cela élève instantanément le niveau de professionnalisme.

#### Stratégie B : Boîtes d'appel

Pour les points qui doivent être mis en évidence :
- Ne laissez pas le texte nu sur la courbe
- Enveloppez dans une boîte à coins arrondis (fond blanc, ombre très légère ou fine bordure)
- Reliez au point de données avec une fine ligne aiguille
- Les boîtes ont des limites physiques → détection et déplacement des collisions plus faciles

---

## Partie 2 : Affinement visuel (Élimination des "bon marché" Esthétiques)

### 1. Traitement des axes et des lignes de grille

**Le signe n°1 des graphiques amateurs : cadres de bordure épais et noirs et lignes de grille pleines.**

| Élément | Règle |
|---------|------|
| Épine supérieure | **SUPPRIMER** (sans condition) |
| Épine droite | **SUPPRIMER** (sans condition) |
| Épine de l'axe Y gauche | Optionnelle — peut être supprimée si les valeurs sont étiquetées directement sur les barres |
| Axe X inférieur | Conserver comme référence de base (fin, gris) |
| Lignes de grille | **Tiretées uniquement** (pointillées ou tiretées), 0.5pt, 15-20% d'opacité. JAMAIS pleines. |
| Lignes de grille (lorsque les valeurs sont affichées) | **SUPPRIMER entièrement** — si les valeurs de barre/ligne sont étiquetées directement, les lignes de grille sont redondantes |

### 2. Affinement des formes géométriques

#### Circulaire → Anneau (Défaut obligatoire)

- **Toujours utiliser des graphiques en anneau** au lieu de cercles pleins
- Rayon intérieur = **60–70%** du rayon extérieur
- Espace central : afficher la valeur totale ou la métrique principale en gros texte (par exemple, "100%" / "¥2.4M")
- Le poids visuel est plus léger, la hiérarchie d'information est plus claire

#### Style des barres

| Propriété | Valeur | Pourquoi |
|----------|-------|-----|
| Rapport barre-espace | `1.5:1` ou `2:1` | Pas trop fin (baguettes), pas trop gros (pas d'espace pour respirer) |
| Rayon de bordure supérieur | `2px – 4px` | L'arrondi micro supprime la dureté machine, ajoute un sentiment d'UI moderne |
| Rayon de bordure inférieur | `0px` | Base plate ancrée à l'axe |

#### Affinement du graphique en courbe

| Propriété | Valeur | Pourquoi |
|----------|-------|-----|
| Type de courbe | **Lisse (Bézier/spline)** | À moins de montrer des données strictement discrètes |
| Largeur de ligne | `2pt – 3pt` | Se détache contre une grille affaiblie |
| Remplissage de zone | Dégradé de la couleur de ligne à 20% d'opacité → 0% d'opacité vers le bas | Ajoute du volume et de la profondeur |
| Marqueurs de points de données | Petits cercles (rayon 3-4px), uniquement sur les points étiquetés | Ne pas marquer chaque point |

### 3. Légende et hiérarchie de texte

#### Mise en page du titre du graphique

- **Titre principal** : Aligné à gauche au-dessus du graphique, gras, 14-16pt
- **Sous-titre** : Sous le titre principal, poids normal, plus petit (11-12pt), décrit la source/période/unités des données
- Titre et corps du graphique doivent avoir une séparation visuelle claire (≥16px d'écart)
- **⚠️ Règle légende vs titre** : Lorsque le graphique a une légende externe (légende de figure / 图注, par exemple "图 1: XXX" sous le graphique), **n'ajoutez PAS de titre à l'intérieur du graphique** (`ax.set_title()`). La légende sert déjà d'identifiant du graphique — un titre interne la dupliquerait et gaspillerait l'espace vertical. N'ajouter un titre interne que lorsque le graphique est autonome (pas de légende).

#### Règles de légende

| Règle | Détails |
|------|---------|
| Bordure | **AUCUNE** — ne jamais mettre de boîte autour de la légende |
| Position | Ligne horizontale en haut à gauche (préférée) ou directement au-dessus de la zone du graphique |
| Marqueurs | Petits cercles (4px) ou segments de ligne courts — PAS de carrés épais |
| Taille de police | Identique aux étiquettes d'axe (10-12pt) |
| Espacement | Espacement horizontal généreux entre les éléments (≥24px) |

---

## Partie 3 : Configuration par défaut des graphiques

Lors de la génération de n'importe quel graphique (HTML/SVG pour le pipeline Créatif, ou matplotlib/ReportLab pour le pipeline Rapport), appliquez ces paramètres par défaut :

```
Paramètres par défaut des graphiques :
  axes:
    top_spine: hidden
    right_spine: hidden
    left_spine: light_gray_or_hidden
    bottom_spine: light_gray_thin
    grid: dashed, 0.5pt, 20% opacity (or hidden if values labeled)
  
  pie:
    type: donut
    hole_ratio: 0.65
    min_slice_for_internal_label: 5%
    small_slice_strategy: leader_lines  # or "others_merge" or "rich_legend"
    others_threshold: 3%
  
  bar:
    top_radius: 3px
    bar_gap_ratio: 0.5  # gap = 50% of bar width
    auto_horizontal_threshold: 5_cjk_chars  # or 10 latin chars
    value_label_position: auto  # inside if tall, outside if short
  
  line:
    smooth: true  # Bézier curve
    width: 2.5pt
    area_fill: gradient_20_to_0
    label_strategy: first_last_max_min
    point_markers: labeled_points_only
  
  legend:
    border: none
    position: top_left_horizontal
    marker_shape: circle_small  # 4px radius
    marker_size: 4px
  
  typography:
    chart_title: bold, 14-16pt, left-aligned
    chart_subtitle: regular, 11-12pt, left-aligned
    axis_labels: 10-12pt
    value_labels: 10-12pt
    legend_text: 10-12pt
```

---

## Partie 4 : Notes spécifiques au pipeline

### Pipeline Créatif (Playwright HTML/CSS)

Les graphiques dans le pipeline Créatif sont rendus en HTML/SVG au sein des composants du plan. Appliquez les règles de graphique via :
- SVG inline avec viewBox et positionnement de texte appropriés
- Classes CSS pour masquage d'axe, style de grille, mise en page de légende
- Détection de collision basée sur JavaScript pour les lignes de liaison (si dynamique)

### Pipeline Rapport (ReportLab)

Les graphiques dans le pipeline Rapport utilisent des objets Drawing ReportLab ou des figures matplotlib intégrées :
- Utiliser matplotlib avec `plt.rcParams` qui correspondent aux paramètres par défaut ci-dessus
- `ax.spines['top'].set_visible(False)`, `ax.spines['right'].set_visible(False)`
- `ax.grid(True, linestyle='--', alpha=0.2, linewidth=0.5)`
- Pour les graphiques circulaires : `plt.pie(..., wedgeprops=dict(width=0.35))` pour l'effet anneau
- Pour les graphiques en barres : utiliser `matplotlib.patches.FancyBboxPatch` ou `bar(..., edgecolor='none')` avec des patches rectangulaires arrondis manuels

### Pipeline Académique (LaTeX/TikZ)

- Utiliser `pgfplots` avec configuration axe/grille similaire
- `\pgfplotsset{every axis/.append style={...}}`
- Graphiques en anneau via `tikz` avec dessin d'arc

---

## Partie 5 : Espacement des graphiques et garanties anti-empilement

### 5.1 Séparation graphique-texte corporel

| Contexte | Écart minimum | Notes |
|---------|-------------|-------|
| Graphique au-dessus/en dessous du texte corporel | 24pt | À la fois au-dessus et en dessous du graphique |
| Légende du graphique au graphique | 8pt | Légende directement sous le graphique |
| Légende du graphique au texte suivant | 18pt | Séparation claire |
| Deux graphiques consécutifs | 30pt | Empêcher la fusion visuelle |

### 5.2 Prévention du chevauchement légende-graphique

**La LÉGENDE NE DOIT PAS chevaucher la zone de données du graphique.** C'est une règle de tolérance zéro.

```python
# matplotlib : déplacer la légende hors de la zone de tracé lorsqu'il y a chevauchement
leg = ax.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=False)
# Si la légende chevauche toujours, la déplacer sous le graphique :
# leg
