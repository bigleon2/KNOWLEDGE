# matplotlib Template Library

> **⚠️ Avant d'écrire du code, lisez [`_rules.md`](references/_rules.md) — trois règles non négociables sur le chevauchement, la hiérarchie et la couleur.**


## Initialisation de l'Environnement (Doit être exécuté avant chaque graphique)

```python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ═══ Configuration de la Police Chinoise ═══
# SimHei est la police par défaut ; autres polices disponibles :
#   SimSun.ttf (Songti, documents formels), SimKai.ttf (Kaiti, artistique),
#   SarasaMonoSC-*.ttf (monospace CJK, scènes de code)
# Exécutez `fc-list :lang=zh` pour les polices système (PingFang SC, Heiti TC, etc.)
# Chemin de la police : ajustez pour votre système. Emplacements courants :
#   macOS: '/System/Library/Fonts/Supplemental/SimHei.ttf'
#   Linux: '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
#   Personnalisé: './fonts/SimHei.ttf'
import os
SIMHEI_PATH = os.environ.get('SIMHEI_FONT', '/System/Library/Fonts/Supplemental/SimHei.ttf')
matplotlib.font_manager.fontManager.addfont(SIMHEI_PATH)

# ═══ Style Global ═══
plt.rcParams.update({
    # Police
    'font.sans-serif': ['SimHei'],
    'axes.unicode_minus': False,
    # Arrière-plan
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    # Bordure : ne conserver que gauche et bas
    'axes.edgecolor': '#E5E7EB',
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    # Grille : désactivée par défaut
    'axes.grid': False,
    # Graduations : masquer les marques de graduation
    'xtick.major.size': 0,
    'ytick.major.size': 0,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    # Titre
    'axes.labelsize': 10,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.titlepad': 16,
    # Légende : sans cadre
    'legend.frameon': False,
    'legend.fontsize': 9,
    # Exportation
    'figure.dpi': 200,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#FFFFFF',
    'savefig.pad_inches': 0.3,
})
```

## Constantes de Couleur

```python
# ─── Couleurs Froides (Business/Tech) ───
C_BLUE   = '#3B82F6'
C_CYAN   = '#06B6D4'
C_PURPLE = '#8B5CF6'
C_AMBER  = '#F59E0B'
C_RED    = '#EF4444'
C_GREEN  = '#10B981'
COOL = [C_BLUE, C_CYAN, C_PURPLE, C_AMBER, C_RED, C_GREEN]

# ─── Couleurs Chaudes (Chaleur/Créatif) ───
WARM = ['#F59E0B', '#EF4444', '#8B5CF6', '#3B82F6', '#10B981', '#EC4899']

# ─── Gris Académique ───
ACADEMIC = ['#111827', '#6B7280', '#9CA3AF', '#D1D5DB', '#E5E7EB', '#F3F4F6']

# ─── Couleurs Adaptées aux Daltoniens (Préférées pour les articles) ───
CB_SAFE = ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377']

# ─── Gris ───
G900, G700, G500, G400, G300, G200, G100, G50 = \
    '#111827', '#374151', '#6B7280', '#9CA3AF', '#D1D5DB', '#E5E7EB', '#F3F4F6', '#F9FAFB'

# ─── Gain/Perte ───
POS = '#22C55E'
NEG = '#EF4444'
```

## Fonctions Utilitaires

```python
def clean_axis(ax, grid=True):
    """Nettoyer l'axe : supprimer les bordures supérieure et droite, ajouter une grille faible"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if grid:
        ax.yaxis.grid(True, alpha=0.08, color=G300)
        ax.set_axisbelow(True)

def add_value_labels(ax, bars, values, highlight_idx=None, fmt='{:,.0f}',
                     offset_ratio=0.02):
    """Ajouter des étiquettes de valeur au-dessus des barres, mettre en gras la barre en surbrillance.
    ⚠️ Étend automatiquement la limite supérieure de l'axe Y pour s'assurer que les étiquettes ne dépassent pas la zone du graphique."""
    max_val = max(values)
    for i, (bar, val) in enumerate(zip(bars, values)):
        is_hl = (i == highlight_idx) if highlight_idx is not None else False
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + max_val * offset_ratio,
                fmt.format(val), ha='center', va='bottom',
                fontsize=10 if is_hl else 9,
                color=G900 if is_hl else G400,
                fontweight='bold' if is_hl else 'normal')

    # ⚠️ Critique : étendre la limite supérieure de l'axe Y pour laisser suffisamment d'espace pour les étiquettes (au moins 15%)
    ax.set_ylim(0, max_val * 1.18)

def save(fig, path, dpi=200):
    """Sauvegarde unifiée — préfère constrained_layout, fallback sur tight_layout"""
    if not fig.get_constrained_layout():
        try:
            fig.tight_layout()
        except Exception:
            pass
    fig.savefig(path, dpi=dpi, facecolor='white', bbox_inches='tight')
    plt.close(fig)
    import os
    size_kb = os.path.getsize(path) / 1024
    print(f'✅ {path} ({size_kb:.0f}KB)')
```

### Évitement du Texte des Étiquettes (adjustText)

Lorsque les graphiques ont plusieurs annotations de texte (par exemple, étiquettes de nuage de points, annotations de boîte à moustaches), **doit utiliser la bibliothèque adjustText** pour éviter le chevauchement de texte :

```python
# pip install adjustText
from adjustText import adjust_text

# Appeler après avoir ajouté toutes les annotations
texts = []
for i, (x, y, label) in enumerate(zip(x_data, y_data, labels)):
    texts.append(ax.text(x, y, label, fontsize=9, color='#374151'))

# Auto-évitement — passer tous les objets texte, adjustText les déplacera pour éviter le chevauchement
adjust_text(texts, ax=ax,
            arrowprops=dict(arrowstyle='->', color='#9CA3AF', lw=0.8),
            force_text=(0.5, 0.8),   # Force pour repousser le texte
            force_points=(0.3, 0.5), # Répulsion depuis les points de données
            expand=(1.2, 1.4))       # Facteur d'expansion pour le bbox du texte
```

---

## Modèle 1 : Graphique à Barres d'Analyse

**Scénario** : Mettre en évidence la performance exceptionnelle d'un élément de données. Griser les autres, mettre en évidence l'élément cible.

```python
def insight_bar(labels, values, highlight_idx, title, 
                highlight_color=C_BLUE, save_path='insight_bar.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = [G200] * len(labels)
    colors[highlight_idx] = highlight_color
    
    bars = ax.bar(labels, values, color=colors, width=0.6,
                  zorder=3, edgecolor='white', linewidth=0.5)
    add_value_labels(ax, bars, values, highlight_idx)
    
    ax.set_title(title, loc='left')
    # ⚠️ add_value_labels définit déjà ylim automatiquement, pas besoin de le répéter ici
    clean_axis(ax)
    save(fig, save_path)
```

---

## Modèle 2 : Graphique Ligne de Comparaison de Tendance

**Scénario** : Cette année vs l'année dernière, réel vs cible. Ligne principale en couleur pleine, ligne de comparaison en gris pointillée.

```python
def trend_compare(x, y_main, y_ref, label_main, label_ref, title,
                  color=C_BLUE, save_path='trend_compare.png'):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Ligne de comparaison (gris pointillé, en couche inférieure)
    ax.plot(x, y_ref, color=G300, linewidth=1.5, linestyle='--', zorder=2)
    ax.text(len(x)-0.5, y_ref[-1], label_ref, color=G400, fontsize=9, va='center')

    # Ligne principale (couleur pleine + points blancs au centre)
    ax.plot(x, y_main, color=color, linewidth=2.5, marker='o', markersize=5,
            markerfacecolor='white', markeredgewidth=2, markeredgecolor=color, zorder=3)
    ax.text(len(x)-0.5, y_main[-1], f'{label_main}  {y_main[-1]:,.0f}',
            color=color, fontsize=10, fontweight='bold', va='center')

    # Zone de différence
    ax.fill_between(range(len(x)), y_ref, y_main, alpha=0.06, color=color)

    ax.set_title(title, loc='left')
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x)
    clean_axis(ax)
    save(fig, save_path)
```

---## Template 3: Barres Groupées

**Scénario**: Comparaison de plusieurs catégories sur plusieurs dimensions.

```python
def grouped_bar(labels, datasets, series_names, title,
                colors=None, save_path='grouped_bar.png'):
    if colors is None:
        colors = COOL[:len(datasets)]

    fig, ax = plt.subplots(figsize=(12, 6))
    n = len(datasets)
    width = 0.7 / n
    x = np.arange(len(labels))

    for i, (data, name, color) in enumerate(zip(datasets, series_names, colors)):
        offset = (i - n/2 + 0.5) * width
        ax.bar(x + offset, data, width=width*0.85, color=color,
               label=name, zorder=3, edgecolor='white', linewidth=0.3)

    ax.set_title(title, loc='left')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(max(d) for d in datasets) * 1.20)  # Laisser 20% d'espace pour les étiquettes
    ax.legend(loc='upper right', ncol=n)
    clean_axis(ax)
    save(fig, save_path)
```

---

## Template 4: Graphique de Classement Horizontal

**Scénario**: Classements / Top N. Mise en progressif pour les éléments principaux.

```python
def ranking_bar(labels, values, title, top_n=3,
                color=C_BLUE, save_path='ranking.png'):
    from matplotlib.colors import to_rgba
    
    sorted_pairs = sorted(zip(labels, values), key=lambda x: x[1])
    labels_s, values_s = zip(*sorted_pairs)
    
    fig, ax = plt.subplots(figsize=(10, max(6, len(labels)*0.45)))
    
    bar_colors = [G200] * len(labels_s)
    for i in range(len(labels_s) - top_n, len(labels_s)):
        progress = (i - (len(labels_s) - top_n)) / max(top_n - 1, 1)
        bar_colors[i] = to_rgba(color, 0.35 + 0.65 * progress)
    
    bars = ax.barh(range(len(labels_s)), values_s, color=bar_colors,
                   height=0.6, zorder=3, edgecolor='white', linewidth=0.3)
    
    for i, (bar, val) in enumerate(zip(bars, values_s)):
        is_top = i >= len(labels_s) - top_n
        ax.text(bar.get_width() + max(values_s)*0.01,
                bar.get_y() + bar.get_height()/2,
                f'{val:,.0f}', va='center', fontsize=9,
                color=G900 if is_top else G400)
    
    ax.set_yticks(range(len(labels_s)))
    ax.set_yticklabels(labels_s)
    ax.set_title(title, loc='left')
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.set_visible(False)
    save(fig, save_path)
```

---

## Template 5: Graphique en Anneau

**Scénario**: Distribution de proportions (max 5 tranches, à éviter si possible — les graphiques en barres sont généralement meilleurs).

```python
def donut(labels, values, title, center_text=None,
          colors=None, save_path='donut.png'):
    if colors is None:
        colors = COOL[:len(labels)]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, _, autotexts = ax.pie(
        values, labels=None, colors=colors, autopct='%1.0f%%',
        startangle=90, pctdistance=0.78,
        wedgeprops=dict(width=0.35, edgecolor='white', linewidth=2))
    
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight('bold')
    
    if center_text:
        ax.text(0, 0.06, str(center_text), ha='center', va='center',
                fontsize=28, fontweight='bold', color=G900)
        ax.text(0, -0.1, 'Total', ha='center', va='center', fontsize=11, color=G500)
    
    ax.legend(wedges, labels, loc='center left',
              bbox_to_anchor=(1, 0.5), fontsize=10)
    ax.set_title(title, loc='center', pad=20)
    save(fig, save_path)
```

---

## Template 6: Nuage de Points + Ligne de Tendance

**Scénario**: Analyse de corrélation à deux variables.

```python
def scatter_trend(x, y, title, xlabel, ylabel,
                  color=C_BLUE, save_path='scatter.png'):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.scatter(x, y, c=color, s=50, alpha=0.6,
               edgecolors='white', linewidth=1, zorder=3)
    
    # Ligne de tendance
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(x), max(x), 100)
    ax.plot(x_line, p(x_line), color=G400, linewidth=1.5,
            linestyle='--', zorder=2, alpha=0.7)
    
    ax.set_title(title, loc='left')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    clean_axis(ax, grid=True)
    ax.xaxis.grid(True, alpha=0.08, color=G300)
    save(fig, save_path)
```

---

## Template 7: Carte de Chaleur

**Scénario**: Données matricielles, corrélations, temps × catégorie.

```python
def heatmap(data, row_labels, col_labels, title,
            cmap_color=C_BLUE, save_path='heatmap.png'):
    from matplotlib.colors import LinearSegmentedColormap
    
    cmap = LinearSegmentedColormap.from_list('bc', ['#FFFFFF', cmap_color])
    fig, ax = plt.subplots(
        figsize=(max(8, len(col_labels)*1.2), max(6, len(row_labels)*0.6)))
    
    arr = np.array(data)
    im = ax.imshow(arr, cmap=cmap, aspect='auto')
    
    vmax = arr.max()
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = arr[i][j]
            color = 'white' if val > vmax * 0.6 else G700
            ax.text(j, i, f'{val:.1f}', ha='center', va='center',
                    fontsize=9, color=color)
    
    ax.set_xticks(range(len(col_labels)))
    ax.set_yticks(range(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    ax.set_title(title, loc='left', pad=16)
    
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.08, shrink=0.8)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(labelsize=8)  # les graduations de la barre de couleur ne doivent pas être trop grandes
    
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(G200)
    save(fig, save_path)
```

---

## Template 8: Cartes de Métriques KPI

**Scénario**: Affichage des chiffres clés principaux d'un tableau de bord.

```python
def kpi_cards(metrics, save_path='kpi.png'):
    """
    metrics: [{'label': 'Revenu total', 'value': '12.8M', 
               'change': '+23%', 'positive': True}, ...]
    """
    from matplotlib.patches import FancyBboxPatch
    
    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=(3.8*n, 2.8))
    if n == 1: axes = [axes]
    
    for ax, m in zip(axes, metrics):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        
        bg = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
            boxstyle='round,pad=0.05', facecolor=G50, edgecolor=G200, linewidth=0.8)
        ax.add_patch(bg)
        
        ax.text(0.5, 0.75, m['label'], ha='center', va='center',
                fontsize=10, color=G500)
        ax.text(0.5, 0.45, m['value'], ha='center', va='center',
                fontsize=24, fontweight='bold', color=G900)
        
        if 'change' in m:
            is_pos = m.get('positive', True)
            ax.text(0.5, 0.18,
                    f'{"↑" if is_pos else "↓"} {m["change"]}',
                    ha='center', va='center', fontsize=11,
                    color=POS if is_pos else NEG, fontweight='bold')
    
    save(fig, save_path)
```

---## Template 9: Radar Chart

**Scenario**: Comparaison des capacités multidimensionnelles (max 8 dimensions, max 3 groupes).

```python
def radar(categories, datasets, series_names, title,
          colors=None, save_path='radar.png'):
    if colors is None:
        colors = COOL[:len(datasets)]
    
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # Ferme le polygone
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.yaxis.set_visible(False)
    
    # Beautification de la grille
    ax.spines['polar'].set_color(G200)
    ax.grid(color=G200, linewidth=0.5, alpha=0.5)
    
    for data, name, color in zip(datasets, series_names, colors):
        vals = data + data[:1]  # Ferme le polygone
        ax.plot(angles, vals, color=color, linewidth=2, label=name)
        ax.fill(angles, vals, color=color, alpha=0.08)
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_title(title, pad=30, fontsize=16, fontweight='bold')
    save(fig, save_path)
```

---

## Template 10: Waterfall Chart

**Scenario**: Montrer les changements incrémentaux de la valeur initiale à la valeur finale.

```python
def waterfall(labels, values, title, save_path='waterfall.png'):
    """Les labels et valeurs correspondent, positif=augmentation négatif=diminution, dernier élément traité automatiquement comme total"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    cumulative = [0]
    for v in values[:-1]:
        cumulative.append(cumulative[-1] + v)
    
    bar_colors = []
    for i, v in enumerate(values):
        if i == len(values) - 1:
            bar_colors.append(C_BLUE)      # Total
        elif v >= 0:
            bar_colors.append(POS)          # Augmentation
        else:
            bar_colors.append(NEG)          # Diminution
    
    bottoms = []
    for i, v in enumerate(values):
        if i == len(values) - 1:
            bottoms.append(0)               # Le total commence à 0
        elif v >= 0:
            bottoms.append(cumulative[i])
        else:
            bottoms.append(cumulative[i] + v)
    
    bars = ax.bar(labels, [abs(v) for v in values], bottom=bottoms,
                  color=bar_colors, width=0.6, edgecolor='white', linewidth=0.5, zorder=3)
    
    # Lignes de connexion
    for i in range(len(values) - 2):
        y = cumulative[i+1]
        ax.plot([i+0.3, i+0.7], [y, y], color=G300, linewidth=0.8, zorder=2)
    
    # Étiquettes de valeur
    for i, (bar, val) in enumerate(zip(bars, values)):
        y_pos = bar.get_y() + bar.get_height() + max(abs(v) for v in values)*0.01
        prefix = '+' if val > 0 and i < len(values)-1 else ''
        ax.text(bar.get_x()+bar.get_width()/2, y_pos,
                f'{prefix}{val:,.0f}', ha='center', va='bottom',
                fontsize=9, color=G700)
    
    ax.set_title(title, loc='left')
    clean_axis(ax)
    save(fig, save_path)
```

---

## Template 11: Multi-Subplot Dashboard (GridSpec Precision Layout)

**Scenario**: Combiner plusieurs sous-graphiques en un tableau de bord. ⚠️ Maximum 4 sous-graphiques par canevas, diviser si dépassé.

**Principe de base**: Utilisez `GridSpec` pour un contrôle précis de la position et de l'espacement de chaque sous-graphique, ne vous fiez pas à `tight_layout()`.

```python
import matplotlib.gridspec as gridspec

def dashboard(data_dict, title, save_path='dashboard.png'):
    """
    Exemple de mise en page de tableau de bord 2x2.
    data_dict contient les données nécessaires pour chaque sous-graphique.
    """
    # ⚠️ Utilisez constrained_layout au lieu de tight_layout
    fig = plt.figure(figsize=(16, 12), constrained_layout=True)
    fig.suptitle(title, fontsize=20, fontweight='bold', y=0.98)
    
    # GridSpec : contrôle précis de l'espacement
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           wspace=0.35,  # Espacement des colonnes (au moins 0.3)
                           hspace=0.35,  # Espacement des lignes (au moins 0.3)
                           left=0.08, right=0.92,
                           top=0.92, bottom=0.08)
    
    # ─── Haut-gauche : graphique en barres ───
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title('Revenu trimestriel', loc='left', fontsize=13, fontweight='bold')
    # ... lier les données ...
    clean_axis(ax1)
    
    # ─── Haut-droite : graphique en ligne ───
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title('Tendance mensuelle', loc='left', fontsize=13, fontweight='bold')
    # ... lier les données ...
    clean_axis(ax2)
    
    # ─── Bas-gauche : graphique circulaire ───
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title('Part par catégorie', loc='left', fontsize=13, fontweight='bold')
    # ... lier les données ...
    
    # ─── Bas-droite : graphique de dispersion ───
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title('Analyse de conversion', loc='left', fontsize=13, fontweight='bold')
    # ... lier les données ...
    clean_axis(ax4)
    
    fig.savefig(save_path, dpi=200, facecolor='white', bbox_inches='tight')
    plt.close(fig)
```

### Règles d'Or de la Mise en Page du Tableau de Bord

| Règle | Description |
|------|-------------|
| **Maximum 4 sous-graphiques** | Diviser en plusieurs graphiques si dépassé |
| **Utiliser `constrained_layout=True`** + Plus intelligent que `tight_layout()`, évite automatiquement les étiquettes |
| **`wspace/hspace ≥ 0.3`** | Un espacement trop petit entre les sous-graphiques cause un chevauchement |
| **Titre indépendant par sous-graphique** | Utilisez `ax.set_title()` au lieu de `fig.suptitle()` |
| **Tailles de police cohérentes** | Sous-titre 13px, étiquettes d'axe 10px, étiquettes de données 9px |
| **Barre de couleurs dans une colonne séparée** | Si un sous-graphique a besoin d'une barre de couleurs, attribuez `gs[0, 2]` séparément |
| **Ne pas mélanger légende et étiquettes directes** | Utilisez soit toutes des légendes, soit toutes des étiquettes directes dans un tableau de bord |

### Mise en Page Sécurisée avec Barre de Couleurs

```python
# Quand un sous-graphique a besoin d'une barre de couleurs, utilisez une mise en page à 3 colonnes, colonne de droite pour la barre de couleurs
gs = gridspec.GridSpec(2, 3, figure=fig,
                       width_ratios=[1, 1, 0.05],  # Troisième colonne très étroite, dédiée à la barre de couleurs
                       wspace=0.4, hspace=0.35)

ax_heat = fig.add_subplot(gs[0, 1])
im = ax_heat.imshow(data, cmap='Blues')

# Barre de couleurs placée dans sa propre position de sous-graphique, n'obstruira aucun contenu
cbar_ax = fig.add_subplot(gs[0, 2])
fig.colorbar(im, cax=cbar_ax)
cbar_ax.set_ylabel('Valeur', fontsize=10)
```

### Stratégie de Division pour Plus de 4 Sous-graphiques

```python
# ❌ Faux : 8 sous-graphiques entassés dans un seul canevas
fig, axes = plt.subplots(2, 4, figsize=(20, 10))  # Tout devient illisible

# ✅ Correct : diviser en 2 figures, 4 sous-graphiques chacune
# Figure 1 : indicateurs généraux
fig1 = plt.figure(figsize=(16, 12), constrained_layout=True)
# ... 4 sous-graphiques ...
fig1.savefig('dashboard_overview.png', dpi=200)

# Figure 2 : analyse détaillée
fig2 = plt.figure(figsize=(16, 12), constrained_layout=True)
# ... 4 sous-graphiques ...
fig2.savefig('dashboard_detail.png', dpi=200)
```
