---
name: charts
metadata:
  author: Z.AI
  version: "1.0"
description: >
  Compétence de création de diagrammes et graphiques professionnels. Couvre tous les types de représentation de données visuelles et de diagrammes structurels :
  - **Graphiques de données**: graphiques en barres, graphiques linéaires, graphiques circulaires, diagrammes de dispersion, heatmaps,
    graphiques radar, graphiques en chandeliers, boxplots, histogrammes, graphiques en aires, graphiques en cascades,
    graphiques de régression, graphiques de distribution, et visualisations statistiques.
  - **Diagrammes structurels**: organigrammes, cartes mentales, diagrammes arborescents, organigrammes d'entreprise,
    diagrammes d'architecture, graphiques réseau/relationnels, diagrammes entité-relation, diagrammes de classes,
    diagrammes de Gantt, diagrammes de couloirs (swimlane), et diagrammes de séquence.
  - **Tableaux de bord**: tableaux de bord de données, panneaux de KPI, compositions multi-graphiques,
    et visualisations interactives.
  - **Qualité de design**: systèmes de couleurs professionnels, règles d'anti-recouvrement, optimisation de la mise en page,
    routage de cadre basé sur le scénario (matplotlib, seaborn, ECharts, D3.js, Mermaid, Playwright+CSS),
    et sortie prête pour publication.
  S'applique lorsque l'utilisateur souhaite créer, générer, dessiner, tracer, visualiser ou améliorer
  n'importe quel graphique, graphique, diagramme ou tableau de bord. S'applique également lorsque l'utilisateur demande
  quelque chose de plus poli, plus propre ou prêt pour publication.
  PAS POUR: mise en page de document PDF (utiliser la compétence pdf), diapositives (utiliser la compétence slides),
  feuilles de calcul avec graphiques intégrés (utiliser la compétence xlsx), génération d'images IA (utiliser image_gen),
  affiches / infographies / cartes créatives (utiliser la compétence pdf Creative pipeline).
  INTERDIT: Utiliser matplotlib/seaborn pour dessiner des cartes mentales, diagrammes arborescents, organigrammes,
  organigrammes de flux, ou n'importe quel diagramme structurel. Ces derniers DOIVENT utiliser Playwright+CSS.
license: Propriétaire. LICENSE.txt contient les termes complets
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : compétences auto-contenues, versionnées semver, registre KB source de vérité, dépendances YAML, références croisées bidirectionnelles.



# Beautiful Charts

## Quick Setup

```bash
bash "$SKILL_DIR/setup.sh"    # Vérification interactive de l'environnement + installation
```

Rendez chaque graphique et diagramme conçu professionnellement, pas généré par IA.

## Architecture

| Module | File | Quand le charger |
|--------|------|-------------|
| **Routing + Règles de base** | Ce fichier | Toujours lire en premier |
| **Modèles de Framework** | `references/` par framework | Après avoir choisi le framework, lire le fichier correspondant |

**Ordre de chargement: Lire ce fichier → choisir framework → lire fichier modèle → commencer le codage.**

Chaque fichier modèle contient ses propres règles spécifiques au framework (espacement, connecteurs, détails de couleur). Ce fichier ne contient que les décisions de routage et les règles universelles qui s'appliquent à TOUS les graphiques.

---

# Partie 1: Routage

## ⚠️ Règle de Contrainte de Format (PRIORITÉ MAXIMALE)

**Lorsque l'utilisateur spécifie un format/outil, vous DEVEZ vous conformer. Ne jamais substituer.**

| L'utilisateur dit | Vous DEVEZ faire | Interdit |
|-----------|------------|-----------|
| "use mermaid code" / "sortir au format Mermaid" / "convertir en Mermaid" / "diagramme Mermaid" | ① Sortir un bloc de code Mermaid (```mermaid ... ```) ② Fournir également un aperçu d'image rendu | ❌ Ne peut donner que l'image sans code ; ❌ Ne peut prendre une capture d'écran du code brut comme image |
| "use markdown code" | Sortir une hiérarchie formatée en markdown | ❌ Ne peut passer à HTML/CSS |
| "via mermaid or markdown code" | Choisir l'un des deux, sortir le code texte | ❌ Ne peut passer à tout format non spécifié |
| "flowchart" / "mind map" (aucun format spécifié) | Libre de choisir la meilleure approche | - |
| "use echarts/d3" | DOIT utiliser le framework spécifié | ❌ Ne peut changer |

### 🚫 INTERDIT: Capture d'écran de code Mermaid
**NEVER prendre de capture d'écran du code source Mermaid brut et le livrer comme "image de diagramme".** C'est le pire résultat possible — l'utilisateur obtient ni code utilisable ni diagramme visuel. Lorsque l'utilisateur demande le format Mermaid:
1. **DOIT** sortir le code Mermaid dans un bloc de code clôturé (````mermaid`)
2. **DEVRAIT** également rendre le code en image de diagramme visuel (via mermaid-cli ou Playwright + mermaid.js)
3. Si le rend échoue, livrer le bloc de code et dire à l'utilisateur de le coller sur mermaid.live

### Conflit Format Spécifié vs Auto-Amélioration
Lorsque l'utilisateur spécifie Mermaid mais que le contenu déclenche des conditions d'auto-amélioration (>8 nœuds, lourd en CJK, etc.):
1. **Le choix de l'utilisateur prime** — toujours utiliser Mermaid, livrer bloc de code + image rendue
2. **Guider proactivement** — après livraison, suggérer à l'utilisateur d'essayer sans spécifier Mermaid pour une qualité de mise en page meilleure
3. **Jamais changer silencieusement** vers Playwright+CSS lorsque l'utilisateur a explicitement demandé Mermaid

Lorsqu'un outil spécifié rencontre des difficultés de rendu (ex: échec du CDN mermaid):
- ✅ Sortir code mermaid brut, dire à l'utilisateur de le voir sur mermaid.live
- ❌ Changer secrètement vers un autre framework
- ❌ Prendre capture d'écran du code texte comme "image"

---

## Arbre de Décision de Routage

### 1. Diagrammes Structurels

#### 🔴 Organigramme par Défaut: Vertical Phasé (PRIORITÉ MAXIMALE)

**Lorsque l'utilisateur demande de « générer/créer un organigramme XXX » sans spécifier de format, la disposition par DÉFAUT est Verticale Phasée (Mise en page C dans `references/playwright-css.md`).**

C'est parce que presque tous les processus du monde réel (fabrication, procédures légales, gestion de projet, opérations commerciales, recettes de cuisine, etc.) ont des phases/stages naturels. La mise en page C produit le résultat le plus professionnel, lisible.

**Priorité de routage d'organigramme:**
1. **L'utilisateur a spécifié Mermaid/markdown** → suivre le choix de l'utilisateur (Règle de Contrainte de Format)
2. **≤6 nœuds ET pas de phases ET texte court** → Mermaid (organigramme simple)
3. **Tout le reste** → **Playwright + CSS, Mise en page C (Verticale Phasée)** → `references/playwright-css.md`

**Détection de phase — considérer comme "a des phases" si AU MOINS un est vrai:**
- Le contenu a des sections numérotées (1. 2. 3., numérotation chinoise, ou Phase 1/Stage 1)
- Le processus peut être groupé par temps/étape/rôle (ex: "préparation → exécution → révision")
- Total des étapes ≥ 5 (presque toujours groupable en 2+ phases)
- Le processus implique plusieurs rôles/départements
- Le processus a un début/fin clairs avec des étapes intermédiaires

**⚠️ En cas de doute, par défaut à la Mise en page C.** Une mise en page phasée avec seulement 1 phase a toujours l'air professionnel. Une mise en page Grille avec des phases ressemble à un désordre.

#### Autres Diagrammes Structurels
- Organigramme simple (≤6 nœuds, vraiment plat, pas de phases): **Mermaid**
- Organigramme complexe (>6 nœuds / lourd en CJK / branches / phases): **Playwright + CSS Mise en page C** → `references/playwright-css.md`
- Carte mentale / arbre / organigramme d'entreprise: **Playwright + CSS** → `references/mindmap-css.md`
- Diagramme relationnel / réseau: **ECharts graph**
- Analyse centrale-radiale (SWOT / BSC / Cinq Forces de Porter / PEST): **Playwright + CSS** → `references/radial-grid.md`

### 2. Graphiques de Données (matplotlib / seaborn)
- Barre/ligne/nuage de points/heatmap/radar/circulaire standard: **matplotlib**
- Régression/distribution/boxplot: **Seaborn**

### 3. Graphiques Interactifs / Tableaux de Bord
- Tableau de bord de données / chandelier / temps réel: **ECharts**
- Interactif entièrement personnalisé: **D3.js**

### Stratégie par Défaut
**Un scénario, un outil — ne pas hésiter:**

| Scénario | Outil | Modèle |
|-------|------|----------|
| Graphique de données (barre/ligne/nuage de points/circulaire/radar) | matplotlib | `references/matplotlib.md` |
| Statistique (régression/box/dist) | Seaborn | `references/seaborn.md` |
| Carte mentale / arbre / organigramme d'entreprise | Playwright + CSS | `references/mindmap-css.md` |
| Centré-radial (SWOT/BSC/PEST/Cinq Forces) | Playwright + CSS | `references/radial-grid.md` |
| **N'importe quel organigramme (par défaut)** | **Playwright + CSS Mise en page C** | **`references/playwright-css.md`** |
| Organigramme simple (≤6 nœuds, vraiment plat) | Mermaid | `references/mermaid.md` |
| Relationnel / force-directed | ECharts graph | `references/echarts.md` |
| Tableau de bord de données | ECharts | `references/echarts.md` |
| Figures de articles académiques | matplotlib | `references/matplotlib.md` |

---## Règles d'Auto-Upgrade Mermaid

La disposition dagre/elk de Mermaid estime incorrectement les largeurs CJK. **Passage automatique à Playwright+CSS QUAND AU MOINS une condition est remplie :**

| Déclencheur | Action |
|---------|--------|
| Total des nœuds > **6** | → Diagramme de flux CSS (Layout C) |
| Tout texte de nœud > **12 caractères chinois** | → Diagramme de flux CSS |
| Plus de **3 branches parallèles** | → Diagramme de flux CSS |
| Sous-graphes imbriqués > **2 niveaux** | → Diagramme de flux CSS |
| Croisements de connecteurs > **2** | → Diagramme de flux CSS |
| **Annotations latérales / boîtes de note en pointillés** | → Diagramme de flux CSS |
| **Flèches de retour / cycles** | → Diagramme de flux CSS |
| **Le processus a des phases/étapes identifiables** | → Diagramme de flux CSS (Layout C) |

**Si maintien avec Mermaid** : `padding: 32`, `nodeSpacing: 80`, `rankSpacing: 80`. Texte de nœud ≤ 10 caractères CJK/ligne, avec `<br>`, tout texte entre guillemets `A["text"]`.

---

## Rendu de Grandes Données

| Taille des données | Approche |
|-----------|----------|
| < 1,000 points | matplotlib / n'importe lequel |
| 1,000 - 10,000 | matplotlib (pas de marqueurs) ou ECharts |
| 10,000 - 100,000 | ECharts (mode Canvas) |
| > 100,000 | ECharts (`large: true`) ou WebGL |

---

# Partie 2 : Règles Universelles

Ces règles s'appliquent à TOUS les diagrammes quel que soit le framework. Les règles spécifiques au framework se trouvent dans chaque fichier de modèle.

## 7 Règles Fondamentales

1. **Zéro chevauchement.** Aucun élément ne peut masquer le texte d'un autre. Chevauchement = perte d'information = échec de la tâche. Post-génération : vérifier que chaque élément a une séparation claire.

2. **Hiérarchie avant uniformité.** Nœuds primaires plus grands/gras que les secondaires. Nœuds d'annotation plus petits/estompés. Espacement entre les groupes > au sein des groupes. Si chaque boîte a l'air identique, la disposition a échoué.

3. **Palette de faible saturation.** 70% arrière-plan/neutre, 20% secondaire, 10% accent (un seul point fort). Pas de remplissages grands et saturés. Couleurs saturées uniquement sur les bordures (2px), texte et éléments petits.

4. **L'insight d'abord.** Les titres expriment des conclusions, pas des noms de champ. Supprimer les éléments non essentiels : bordures haut/droite, lignes de grille, marques de graduation, bordures de boîte de légende. Si le supprimer ne réduit pas la compréhension, il ne devrait pas exister.

5. **Clarté des étiquettes avant méthode d'étiquetage.** L'objectif est zéro chevauchement — choisir la méthode qui y parvient pour chaque type de diagramme. Étiquetage direct, légendes et lignes de liaison sont toutes valides ; ce qui compte est qu'il n'y ait aucun chevauchement.

### 🚫 INTERDIT : Tout Texte Chevauchant un Autre Élément
**Aucune étiquette, légende, annotation ou titre ne peut chevaucher un autre élément visuel.** C'est le défaut matplotlib le plus courant. Les étiquetages directs ET les légendes peuvent provoquer un chevauchement — aucun n'est intrinsèquement sûr.

**Arbre de décision anti-chevauchement :**
1. **Vérifier si les étiquetages directs passent** — si toutes les étiquettes ont assez d'espace (sommets de barres, extrémités de lignes, grandes parts de camembert), étiqueter directement. Pas de légende nécessaire.
2. **Si certaines étiquettes entreraient en collision** (petites parts de camembert, points de dispersion denses, barres groupées) → utiliser une légende en dehors de la zone de diagramme au lieu de forcer les étiquettes dans des espaces étroits.
3. **Approche mixte** — étiqueter directement les éléments principaux, grouper les petits éléments dans « Autres » ou utiliser des lignes de liaison + légende pour les petits.

**Spécifique aux diagrammes circulaires (le pire coupable) :**
- Parts < 5% : DOIT utiliser des lignes de liaison (`wedgeprops + texts` repositionnement manuel, ou `matplotlib.patches.ConnectionPatch`) pour sortir les étiquettes. Ne pas se fier uniquement à `autopct` — il place le texte à l'intérieur/près de la part.
- Plusieurs petites parts adjacentes : utiliser une légende `bbox_to_anchor` en dehors, PAS d'étiquetage direct
- `labeldistance=1.25` minimum pour garder les étiquettes à l'extérieur du camembert
- Quand >2 parts sont < 5%, envisager de grouper toutes les < 3% en « Autres (X éléments) »
- Utiliser la bibliothèque `adjustText` pour résoudre automatiquement les collisions d'étiquettes quand disponible

**Placement de la légende (quand une légende est nécessaire) :**
- Placer la légende **en dehors** de la zone de diagramme en utilisant `bbox_to_anchor`
- Positions de départ suggérées :
  - Barre/ligne/dispersion : côté droit en dehors (`bbox_to_anchor=(1.02, 1), loc='upper left'`)
  - Camembert : côté droit en dehors (`bbox_to_anchor=(1.1, 0.5), loc='center left'`)
  - Radar : en dessous du diagramme (`bbox_to_anchor=(0.5, -0.15), loc='upper center'`)
  - Carte thermique : pas de légende nécessaire (la barre de couleur suffit)

**🔧 Obligatoire : ajustement automatique de la légende pour éviter le chevauchement.** Copier ce snippet après avoir placé n'importe quelle légende :
```python
# ── Ajustement automatique de la position de la légende pour éviter le chevauchement ──
fig.canvas.draw()  # doit être rendu d'abord pour obtenir les bboxes
legend = ax.get_legend()
if legend:
    renderer = fig.canvas.get_renderer()
    # Essayer de déplacer jusqu'à 5 fois pour résoudre le chevauchement
    for _ in range(5):
        leg_bb = legend.get_window_extent(renderer).transformed(ax.transAxes.inverted())
        has_overlap = False
        for text in ax.texts + [ax.title] + ax.get_xticklabels() + ax.get_yticklabels():
            if not text.get_text():
                continue
            txt_bb = text.get_window_extent(renderer).transformed(ax.transAxes.inverted())
            if leg_bb.overlaps(txt_bb):
                has_overlap = True
                break
        if not has_overlap:
            break
        # Déplacer la légende plus loin à l'extérieur (la direction dépend de loc actuel)
        bbox = legend.get_bbox_to_anchor().transformed(ax.transAxes.inverted())
        x0, y0 = bbox.x0, bbox.y0
# Heuristique : si la légende est en dessous du centre, déplacer vers le bas ; si à droite du centre, déplacer vers la droite
        if y0 < 0.5:
            legend.set_bbox_to_anchor((x0, y0 - 0.08), transform=ax.transAxes)
        else:
            legend.set_bbox_to_anchor((x0 + 0.08, y0), transform=ax.transAxes)
        fig.canvas.draw()
```
- **Après placement de la légende** : toujours appeler `plt.tight_layout()` ou `fig.subplots_adjust()` pour s'assurer que la légende n'est pas rognée

🚫 INTERDIT :
- `loc='best'` — le "meilleur" de matplotlib chevauche souvent les données
- `loc='upper right'` / `loc='lower right'` sur les diagrammes en barres/lignes — risque élevé de collision
- Étiquetage direct des parts de camembert < 5% sans lignes de liaison
- Placement de texte sans vérification de zéro chevauchement

6. **Discipline de police.** Max 2 polices. Chinois : SimHei/PingFang SC. Toujours définir explicitement les polices dans le code. La taille de police suit la hiérarchie (titre 18-24px → corps 13-15px → annotation 11-13px). Jamais en dessous de 10px minimum. Quand le texte déborde : condenser le texte → agrandir la toile → dernier recours : réduire la police (mais jamais en dessous du minimum).

7. **L'espace blanc est un design.** Zone de diagramme 60-70% de la toile, marges 15-20%. Au moins 16pt entre le titre et le diagramme. Encombré ≠ riche en information.

---## Système de couleurs

### Palettes recommandées

| Palette | Texte | Arrière-plan | Remplissage de bloc | Accent |
|---------|------|------------|------------|--------|
| Business Cool | `#243447` | `#F8FAFC` | `#E9EEF3` | `#4C6EF5` |
| Tech Cyan-Gray | `#1F2937` | `#F5F7FA` | `#E6ECF2` | `#3AAFA9` |
| Morandi Warm | `#4B4A45` | `#FAF8F4` | `#EAE4DB` | `#C6866A` |
| Invisible Precision | `#37352F` | `#FFFFFF` | `#F7F7F7` | `#2383E2` |

### 🚫 Couleurs d'arrière-plan interdites

| Couleur | Valeurs hex interdites |
|-------|---------------------|
| Bleu pur | `#3B82F6`, `#2563EB`, `#1D4ED8` |
| Vert pur | `#10B981`, `#059669`, `#22C55E` |
| Rouge pur | `#EF4444`, `#DC2626`, `#F87171` |
| Violet pur | `#8B5CF6`, `#7C3AED`, `#A855F7` |
| Ambre pur | `#F59E0B`, `#D97706`, `#FB923C` |

### ✅ Couleurs d'arrière-plan autorisées

| Couleur | Valeurs hex |
|-------|------------|
| Bleu glace | `#EFF6FF`, `#DBEAFE` |
| Vert menthe | `#F0FDF4`, `#D1FAE5` |
| Ambre clair | `#FFF7ED`, `#FEF3C7` |
| Lavande | `#F5F3FF`, `#EDE9FE` |
| Gris clair | `#F8FAFC`, `#F1F5F9` |

### Couleur fonctionnelle (états uniquement, pas pour la décoration)
- Actif/Sélectionné : accent de marque ou ligne d'accent de `2px`
- Erreur : `#EF4444`
- Succès : `#10B981`
- Étiquettes : arrière-plan clair + texte sombre, jamais de pilules haute saturation

### Accessible aux daltoniens
Ne vous fiez pas uniquement à la couleur — associez à des formes, styles de lignes ou étiquettes directes.
Palette Paul Tol : `['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377']`

### Thème sombre
- Arrière-plan : `#0F172A` (pas noir pur)
- Texte : `#F1F5F9` (pas blanc pur)
- Grille : `#1E293B`, alpha faible
- Exportation : `savefig(facecolor='#0F172A')`

---

## Règles d'exportation

- Graphiques statiques : minimum 200 DPI, recommandé 300 DPI
- Camembert/radar : **carré `figsize=(8, 8)`** — non carré = elliptique
- Maximum 6 couleurs par graphique (diviser si plus)
- Axe Y des graphiques en barres commence à 0 (les graphiques en lignes peuvent tronquer)
- Jamais utiliser 3D (déforme les proportions)

### Capture d'écran Playwright
`device_scale_factor=2` par défaut. Cartes mentales grandes (3000px+) : 1.5. Intégration PDF : 1-1.5. Impression : 3.
Après rendu, lire `bounding_box()` et redimensionner la vue pour s'adapter. Vue minimum : 800px colonne unique, 1200px multi-colonnes.

### 🚫 INTERDIT : `max-width` sur conteneurs Mermaid/SVG
Le moteur dagre de Mermaid produit des SVG de largeur imprévisible (surtout avec sous-graphes, texte CJK ou branches parallèles). **NE JAMAIS définir `max-width` sur l'élément conteneur Mermaid.** Utilisez `width: fit-content; min-width: 800px;` à la place.

**Racine du problème** : les SVG Mermaid dépassent silencieusement leur conteneur CSS. `bounding_box()` (Playwright) retourne la taille du modèle de boîte CSS, PAS la taille réellement rendue du SVG. Ainsi, le redimensionnement automatique de la vue basé uniquement sur `bounding_box()` produira toujours des captures d'écran tronquées.

**Correction** : Toujours lire le **`getBoundingClientRect()` propre de l'élément SVG** via `page.evaluate()`, puis utiliser `max(css_size, svg_size) + padding` pour les dimensions de la vue. Voir `references/mermaid.md` pour le script de capture corrigé.

### Conservation du ratio d'aspect (intégration)
**DOIT lire les dimensions réelles de l'image et calculer la hauteur proportionnellement. JAMAIS coder en dur à la fois largeur et hauteur.**

---

## Règles spécifiques à matplotlib

Celles-ci s'appliquent lors du routage vers matplotlib/seaborn :

### Mise en page & Chevauchement
- Préférer `constrained_layout=True` à `tight_layout()`
- Utiliser la bibliothèque `adjustText` pour le repositionnement automatique des étiquettes — **c'est l'outil anti-chevauchement le plus fiable pour matplotlib.** Installation : `pip install adjustText`. Utilisation : `from adjustText import adjust_text; adjust_text(texts)`
- Maximum 4 sous-graphiques par canevas. Plus → diviser les images ou `figsize=(20, 16)` minimum
- Multi-sous-graphique : `GridSpec` avec `wspace/hspace` ≥ 0.3
- Barre de couleur : `shrink=0.8` + `pad=0.08`
- Étiquettes de données : limite supérieure de l'axe Y avec 15-20% de marge (`ylim(0, max_val * 1.18)`)
- Longues étiquettes X → graphique en barres horizontal ou afficher chaque N-ième étiquette

### Graphiques Radar/Toile d'araignée
- **Chaque `fill()` DOIT avoir `alpha=0.25`** (max 0.3). Omettre alpha = opaque = masque la série sous-jacente.
- Légende : placer à l'extérieur du graphique avec `bbox_anchor`, commencer par `(0.5, -0.15), loc='upper center'`. Si les étiquettes de dimension sont longues ou les dimensions > 8, augmenter le décalage (ex : `-0.25` ou `-0.3`). Aussi INTERDIT : `loc='lower right'` (entre en collision avec les étiquettes de dimension radar).
- Remplissage d'étiquette de dimension : `set_rlim(0, max_value * 1.2)`
- Étiquettes avec >4 caractères CJK : faire pivoter pour suivre l'angle ou abréger
- `figsize=(8, 8)` obligatoire (carré)

### Une couleur, le reste en gris
5 lignes → colorer uniquement la clé, autres `#D1D5DB`. 8 barres → accentuer uniquement la mise en évidence, reste `#E5E7EB`.

---

## Règles de connecteur (diagrammes structurels)

- Attacher aux bords des nœuds, pas par les centres
- Préférer les polylignes orthogonales ou les courbes propres
- Les chemins principaux évitent le croisement
- Jamais traverser les zones de texte
- Les points de départ/fin au même niveau doivent s'aligner (pas décalés)
- Les connecteurs de même niveau suivent la même direction
- Angles de courbure cohérents (tous droits ou tous courbes, pas de mélange)
- Positions d'étiquette uniformes (tous au-dessus de la ligne ou tous centrés)

---

## Liste de vérification pré-livraison

Avant livraison, vérifier :

- [ ] Zéro chevauchement (nœuds, connecteurs, étiquettes, légendes — **vérifier particulièrement légende vs données, et étiquettes adjacentes de camembert/barre**)
- [ ] Aucun connecteur ne traverse de boîtes de texte
- [ ] Hiérarchie claire (primaire/secondaire/annotation visuellement distincts)
- [ ] Palette de faible saturation (pas de couleurs d'arrière-plan interdites)
- [ ] Texte lisible à la taille finale (autonome : ≥12px corps, ≥10px annotation ; PDF : ≥10pt/8pt/7pt)
- [ ] Légende entièrement visible, non tronquée, ne chevauchant aucun élément de graphique
- [ ] Canevas assez large/haut (vérifier la boîte englobante avant capture)
- [ ] **Si carte mentale** : chaque niveau distinct (≥3 changements de propriété), connecteurs visibles (≥ `#94A3B8`), équilibrée gauche-droite
- [ ] **Si organigramme** : titres de phase distincts des étapes, flèches uniquement entre phases, **utiliser Layout C par défaut**
- [ ] **Si organigramme** : couleurs de phase dans même famille de teinte (progression bleu-gris), **PAS arc-en-ciel** (bleu→vert→ambre→violet)
- [ ] **Si organigramme semble dispersé** : STOP — vous utilisez la mauvaise mise en page, passez à Layout C
- [ ] **Si Mermaid semblait rigide** : déjà passé à Playwright+CSS

---## Anti-Pattern Quick Reference

| ❌ Don't | ✅ Do This Instead |
|----------|-------------------|
| matplotlib default blue `#1f77b4` | Use this skill's palette |
| 3D bar/pie | Always 2D |
| Rainbow colormap (jet/rainbow) | Single-hue gradient or diverging |
| Thick black grid lines | `alpha=0.08` or remove |
| Different color per bar | Same series same color, highlight only key |
| 45° tilted X labels | Horizontal bar chart or shorten |
| 8+ subplots in one canvas | Split to 2-3 images, max 4 each |
| `tight_layout()` alone | `constrained_layout=True` or `GridSpec` |
| Labels overflowing chart | `ylim` with 18-25% headroom |
| Mind map: all levels same style | Root+L1 get boxes, leaves plain text |
| Mind map: image too tall | Left-right layout for ≥5 branches |
| Mind map: invisible connectors | Lines ≥ `#94A3B8`, root→L1 `#64748B` 2.5px |
| Mind map: unbalanced sides | Alternate large/small branches across sides |
| Flowchart: high-sat node fills | Low-sat bg (`#EFF6FF`) + sat border (`#3B82F6`) |
| Flowchart: dark bg + dark text | Dark bg → white text. Light bg → dark text |
| Flowchart: arrows between every step | Arrows ONLY between phases, steps use indent |
| Flowchart: cross-layer lines through nodes | Connect adjacent layers only |
| Flowchart: Grid layout for phased process | **Always use Layout C (Phased Vertical)** |
| Flowchart: phase titles as floating labels | Phase titles MUST be inside group cards |
| Flowchart: nodes scattered without grouping | Group nodes into phase cards with `.phase-group` |
| Flowchart: rainbow phase colors (blue→green→amber→purple) | Same-hue blue-gray progression for all phases |
| Multiple arrows to same entry point | Merge-then-enter pattern |
| Legend inside plot obscuring data | `bbox_to_anchor` outside plot area |
| Radar fill without alpha | `alpha=0.25` mandatory |
| Decorative icons/emoji | Let the data speak |
| Grid lines where whitespace suffices | Background contrast or spacing instead |

---

## UI Aesthetics (dashboards / card layouts)

When building UI-style outputs (dashboards, panels), apply "Invisible Precision":

- **Boundaries**: Subtle bg shifts (`#F7F7F7` on `#FFFFFF`), not border lines. Reserve `1px` dividers for absolute logical breaks only.
- **Actions**: Primary CTA in dark neutral (`#1A1A1B`). Secondary: ghost/gray. Hover: 5% darker, no size change.
- **Quiet UI**: Action buttons `opacity: 0` by default, `1` on hover. Only active elements get visual indicators.
- **Numbers**: `font-variant-numeric: tabular-nums` for strict vertical alignment.
- **Spacing**: `line-height: 1.625`, generous paragraph spacing.
