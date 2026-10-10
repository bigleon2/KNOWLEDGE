---
name: charts
version: "1.0.1"
category: "Visualisation & Design"
tags:
  - charts
metadata:
  author: Z.AI
  version: "1.0.1"
description: >
  Skill de création professionnelle de graphiques et de schémas. Couvre tous les types de
  représentation visuelle de données et de schémas structurels :
  - **Graphiques de données** : diagrammes en barres, courbes, secteurs, nuages de points,
    cartes de chaleur, radar, chandeliers, boîtes à moustaches, histogrammes, aires,
    cascades, régressions, distributions et visualisations statistiques.
  - **Schémas structurels** : organigrammes de flux, cartes mentales, arbres, organigrammes,
    schémas d'architecture, graphes de réseau/relations, diagrammes ER, diagrammes de classes,
    diagrammes de Gantt, diagrammes de swimlane et diagrammes de séquence.
  - **Tableaux de bord** : dashboards de données, panneaux KPI, compositions multi-graphiques
    et visualisations interactives.
  - **Qualité graphique** : systèmes de couleurs professionnels, règles anti-chevauchement,
    optimisation de mise en page, routage par framework selon la scène
    (matplotlib, seaborn, ECharts, D3.js, Mermaid, Playwright+CSS),
    et sortie prête pour publication.
  S'applique quand l'utilisateur veut créer, générer, dessiner, tracer, visualiser ou améliorer
  un graphique, un schéma ou un tableau de bord. S'applique aussi quand l'utilisateur demande
  quelque chose de plus soigné, plus propre ou prêt à publier.
  PAS pour : la mise en page de documents PDF (utilisez le skill pdf), les diaporamas
  (utilisez le skill slides), les tableurs avec graphiques intégrés (utilisez le skill xlsx),
  la génération d'images par IA (utilisez image_gen),
  les affiches / infographies / cartes créatives (utilisez la pipeline Creative du skill pdf).
  INTERDIT : utiliser matplotlib/seaborn pour dessiner des cartes mentales, des arbres,
  des organigrammes, des flowcharts ou tout schéma structurel. Ceux-ci DOIVENT utiliser Playwright+CSS.
license: Proprietary. LICENSE.txt has complete terms
language: fr
read_when:
  - Déclencher quand la demande concerne : skill de création professionnelle de graphiques et de schémas
  - Déclencher si la demande mentionne : diagrammes, skill, utilisez
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Beautiful Charts

## Mise en place rapide

```bash
bash "$SKILL_DIR/setup.sh"    # Interactive environment check + install
```

Rendez chaque graphique et chaque schéma d'apparence professionnelle, pas générée par IA.

## Architecture

| Module | Fichier | Quand le charger |
|--------|------|-------------|
| **Routage + règles de base** | Ce fichier | Toujours à lire en premier |
| **Templates par framework** | `references/` par framework | Après avoir choisi le framework, lire le fichier correspondant |

**Ordre de chargement : lire ce fichier → choisir le framework → lire le fichier de template → commencer à coder.**

Chaque fichier de template contient ses propres règles spécifiques au framework (espacement, connecteurs, détails de couleurs). Ce fichier contient uniquement les décisions de routage et les règles universelles applicables à TOUS les graphiques.

---

# Partie 1 : Routage

## ⚠️ Règle de contrainte de format (PRIORITÉ MAXIMALE)

**Quand l'utilisateur spécifie un format/outil de sortie, vous devez vous y conformer. Jamais de substitution.**

| L'utilisateur dit | Vous devez faire | Interdit |
|-----------|------------|-----------|
| "use mermaid code" / "sortie au format Mermaid" / "convertir en mermaid" / "mermaid流程" | ① Sortir un bloc de code Mermaid (```mermaid ... ```) ② Fournir aussi un aperçu rendu en image | ❌ Impossible de donner uniquement l'image sans le code ; ❌ Impossible de capturer le code brut en image |
| "use markdown code" | Sortir une hiérarchie formatée en markdown | ❌ Impossible de basculer vers HTML/CSS |
| "via mermaid or markdown code" | Choisir l'un des deux, sortir le code en texte | ❌ Impossible de basculer vers un autre format |
| "flowchart" / "carte mentale" (sans format spécifié) | Libre choix de la meilleure approche | - |
| "use echarts/d3" | Utiliser le framework spécifié | ❌ Impossible de basculer |

### 🚫 INTERDIT : capture d'écran de code Mermaid
**Ne JAMAIS faire une capture d'écran du code source Mermaid brut et la livrer comme « image du schéma ».** C'est le pire résultat possible — l'utilisateur n'obtient ni code utilisable ni schéma visuel. Quand l'utilisateur demande le format Mermaid :
1. **OBLIGATOIRE** : sortir le code Mermaid dans un bloc de code délimité (````mermaid`)
2. **RECOMMANDÉ** : rendre aussi le code en image de schéma visuelle (via mermaid-cli ou Playwright + mermaid.js)
3. Si le rendu échoue, livrer le bloc de code et indiquer à l'utilisateur de le coller sur mermaid.live

### Conflit entre format spécifié et auto-amélioration
Quand l'utilisateur spécifie Mermaid mais que le contenu déclenche les conditions d'auto-amélioration (>8 nœuds, dominante CJK, etc.) :
1. **Le choix de l'utilisateur l'emporte** — utilisez quand même Mermaid, livrez le bloc de code + l'image rendue
2. **Guidez proactivement** — après la livraison, suggérez à l'utilisateur d'essayer sans imposer Mermaid pour une meilleure qualité de mise en page
3. **Ne basculez jamais silencieusement** vers Playwright+CSS quand l'utilisateur a explicitement demandé Mermaid

Quand l'outil spécifié rencontre des difficultés de rendu (ex. échec du CDN mermaid) :
- ✅ Sortir le texte du code mermaid brut, dire à l'utilisateur de le visualiser sur mermaid.live
- ❌ Basculer en secret vers un autre framework
- ❌ Capturer le texte du code comme « image »

---

## Arbre de décision de routage

### 1. Schémas structurels

#### 🔴 Flowchart par défaut : vertical par phases (PRIORITÉ MAXIMALE)

**Quand l'utilisateur demande de « générer/créer un flowchart/debian de flux » sans préciser de format, la mise en page PAR DÉFAUT est le vertical par phases (Layout C dans `references/playwright-css.md`).**

C'est parce que presque tous les processus réels (fabrication, procédures juridiques, gestion de projet, opérations métier, recettes de cuisine, etc.) ont des phases/étapes naturelles. Le Layout C produit le résultat le plus professionnel et le plus lisible.

**Priorité de routage des flowcharts :**
1. **L'utilisateur a spécifié Mermaid/markdown** → suivre le choix de l'utilisateur (règle de contrainte de format)
2. **≤6 nœuds ET pas de phases ET texte court** → Mermaid (flowchart simple)
3. **Tout le reste** → **Playwright + CSS, Layout C (vertical par phases)** → `references/playwright-css.md`

**Détection des phases — considérer « a des phases » si AU MOINS UNE est vraie :**
- Le contenu comporte des sections numérotées (一、二、三 ou 1. 2. 3. ou Phase 1/Étape 1)
- Le processus peut être regroupé par temps/étape/rôle (ex. « préparation → exécution → revue »)
- Nombre total d'étapes ≥ 5 (presque toujours regroupables en 2+ phases)
- Le processus implique plusieurs rôles/départements
- Le processus a un début/fin clairs avec des étapes intermédiaires

**⚠️ En cas de doute, utilisez par défaut le Layout C.** Une mise en page par phases avec une seule phase reste professionnelle. Un layout en grille avec des phases fait désordre.

#### Autres schémas structurels
- Flowchart simple (≤6 nœuds, réellement plat, sans phases) : **Mermaid**
- Flowchart complexe (>6 nœuds / dominante CJK / branches / phases) : **Playwright + CSS Layout C** → `references/playwright-css.md`
- Carte mentale / arbre / organigramme : **Playwright + CSS** → `references/mindmap-css.md`
- Graphe de relations / réseau : **ECharts graph**
- Analyse radiale centrée (SWOT / BSC / 5 forces de Porter / PEST) : **Playwright + CSS** → `references/radial-grid.md`

### 2. Graphiques de données (matplotlib / seaborn)
- Barres/courbes/nuages/heatmap/radar/secteurs standards : **matplotlib**
- Régression/distribution/boîtes à moustaches : **Seaborn**

### 3. Graphiques interactifs / dashboards
- Dashboard de données / chandeliers / temps réel : **ECharts**
- Interactif entièrement personnalisé : **D3.js**

### Stratégie par défaut
**Une scène, un outil — n'hésitez pas :**

| Scène | Outil | Template |
|-------|------|----------|
| Graphique de données (barres/courbes/nuages/secteurs/radar) | matplotlib | `references/matplotlib.md` |
| Statistique (régression/boîtes/distribution) | Seaborn | `references/seaborn.md` |
| Carte mentale / arbre / organigramme | Playwright + CSS | `references/mindmap-css.md` |
| Radial centré (SWOT/BSC/PEST/5 forces) | Playwright + CSS | `references/radial-grid.md` |
| **Tout flowchart (défaut)** | **Playwright + CSS Layout C** | **`references/playwright-css.md`** |
| Flowchart simple (≤6 nœuds, réellement plat) | Mermaid | `references/mermaid.md` |
| Relations / dirigé par les forces | ECharts graph | `references/echarts.md` |
| Dashboard de données | ECharts | `references/echarts.md` |
| Figures d'articles académiques | matplotlib | `references/matplotlib.md` |

---

## Règles d'auto-amélioration Mermaid

Le moteur de layout dagre/elk de Mermaid estime mal les largeurs CJK. **Basculez automatiquement vers Playwright+CSS si AU MOINS UNE condition est remplie :**

| Déclencheur | Action |
|---------|--------|
| Total de nœuds > **6** | → flowchart CSS (Layout C) |
| Tout texte de nœud > **12 caractères chinois** | → flowchart CSS |
| Plus de **3 branches parallèles** | → flowchart CSS |
| Sous-graphes imbriqués > **2 niveaux** | → flowchart CSS |
| Croisements de connecteurs > **2** | → flowchart CSS |
| **Annotations latérales / boîtes de notes en pointillés** | → flowchart CSS |
| **Flèches de retour / cycles** | → flowchart CSS |
| **Processus avec phases/étapes identifiables** | → flowchart CSS (Layout C) |

**Si vous restez avec Mermaid** : `padding: 32`, `nodeSpacing: 80`, `rankSpacing: 80`. Texte de nœud ≤ 10 caractères CJK/ligne, retour à la ligne avec `<br>`, mettez tout le texte entre guillemets `A["texte"]`.

---

## Rendu de grands jeux de données

| Taille des données | Approche |
|-----------|----------|
| < 1 000 points | matplotlib / au choix |
| 1 000 - 10 000 | matplotlib (sans marqueurs) ou ECharts |
| 10 000 - 100 000 | ECharts (mode Canvas) |
| > 100 000 | ECharts (`large: true`) ou WebGL |

---

# Partie 2 : Règles universelles

Ces règles s'appliquent à TOUS les graphiques, quel que soit le framework. Les règles spécifiques à chaque framework vivent dans chaque fichier de template.

## 7 règles de base

1. **Zéro chevauchement.** Aucun élément ne doit recouvrir le texte d'un autre. Chevauchement = perte d'information = échec de la tâche. Après génération : vérifiez que chaque élément est clairement séparé.

2. **Hiérarchie plutôt qu'uniformité.** Nœuds principaux plus grands/gras que les secondaires. Nœuds d'annotation plus petits/atténués. Espacement entre groupes > espacement intra-groupe. Si toutes les boîtes se ressemblent, la mise en page a échoué.

3. **Palette à faible saturation.** 70 % fond/neutre, 20 % secondaire, 10 % accent (une seule couleur de surbrillance). Pas de grands aplats très saturés. Couleurs saturées uniquement sur les bordures (2px), le texte et les petits éléments.

4. **L'insight d'abord.** Les titres expriment des conclusions, pas des noms de champs. Supprimez les éléments non essentiels : bordures hautes/droites, lignes de grille, graduations, bordures de légende. Si le retirer ne réduit pas la compréhension, il ne devrait pas exister.

5. **Clarté des étiquettes plutôt que méthode d'étiquetage.** L'objectif est zéro chevauchement — choisissez la méthode qui l'atteint pour chaque type de graphique. Étiquettes directes, légendes et lignes de rappel sont toutes valides ; ce qui compte, c'est que rien ne se chevauche.

### 🚫 INTERDIT : tout texte chevauchant tout autre élément
**Aucune étiquette, légende, annotation ou titre ne doit chevaucher un autre élément visuel.** C'est le défaut matplotlib le plus fréquent. Étiquettes directes ET légendes peuvent provoquer des chevauchements — rien n'est intrinsèquement sûr.

**Arbre de décision anti-chevauchement :**
1. **Vérifiez si les étiquettes directes tiennent** — si toutes les étiquettes ont assez d'espace (hauts de barres, extrémités de courbes, grandes parts de secteurs), étiquetez directement. Pas besoin de légende.
2. **Si certaines étiquettes risquent d'entrer en collision** (petites parts de secteurs, points denses, barres groupées) → utilisez une légende hors de la zone de tracé au lieu de forcer des étiquettes dans des espaces serrés.
3. **Approche mixte** — étiquetez directement les éléments majeurs, regroupez les petits dans « 其他 » ou utilisez des lignes de rappel + légende pour les petits.

**Spécifique aux diagrammes en secteurs (le pire cas) :**
- Parts < 5 % : OBLIGATOIRE d'utiliser des lignes de rappel (`wedgeprops + texts` repositionnement manuel, ou `matplotlib.patches.ConnectionPatch`) pour tirer les étiquettes vers l'extérieur. Ne comptez PAS sur `autopct` seul — il place le texte dans/autour de la part.
- Plusieurs petites parts adjacentes : utilisez une légende `bbox_to_anchor` à l'extérieur, PAS des étiquettes directes
- `labeldistance=1.25` minimum pour garder les étiquettes hors du camembert
- Quand plus de 2 parts sont < 5 %, envisagez de regrouper tout ce qui est < 3 % dans « 其他（X项） »
- Utilisez la bibliothèque `adjustText` pour résoudre automatiquement les collisions d'étiquettes quand elle est disponible

**Placement de la légende (quand une légende est nécessaire) :**
- Placez la légende **à l'extérieur** de la zone de tracé avec `bbox_to_anchor`
- Positions de départ suggérées :
  - Barres/courbes/nuages : à droite, hors du tracé (`bbox_to_anchor=(1.02, 1), loc='upper left'`)
  - Secteurs : à droite, hors du tracé (`bbox_to_anchor=(1.1, 0.5), loc='center left'`)
  - Radar : sous le graphique (`bbox_to_anchor=(0.5, -0.15), loc='upper center'`)
  - Heatmap : pas besoin de légende (la colorbar suffit)

**🔧 Obligatoire : auto-ajuster la légende pour éviter les chevauchements.** Copiez ce snippet après avoir placé une légende :
```python
# ── Auto-adjust legend position to prevent overlap ──
fig.canvas.draw()  # must render first to get bboxes
legend = ax.get_legend()
if legend:
    renderer = fig.canvas.get_renderer()
    # Try shifting up to 5 times to resolve overlap
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
        # Move legend further outside (direction depends on current loc)
        bbox = legend.get_bbox_to_anchor().transformed(ax.transAxes.inverted())
        x0, y0 = bbox.x0, bbox.y0
        # Heuristic: if legend is below center, move down; if right of center, move right
        if y0 < 0.5:
            legend.set_bbox_to_anchor((x0, y0 - 0.08), transform=ax.transAxes)
        else:
            legend.set_bbox_to_anchor((x0 + 0.08, y0), transform=ax.transAxes)
        fig.canvas.draw()
```
- **Après avoir placé la légende** : appelez toujours `plt.tight_layout()` ou `fig.subplots_adjust()` pour garantir que la légende n'est pas coupée

🚫 INTERDIT :
- `loc='best'` — le « best » de matplotlib chevauche souvent les données
- `loc='upper right'` / `loc='lower right'` sur les courbes/barres — risque de collision élevé
- Étiquettes directes sur des parts de secteurs < 5 % sans lignes de rappel
- Tout placement de texte sans vérification du zéro chevauchement

6. **Discipline des polices.** 2 polices maximum. Chinois : SimHei/PingFang SC. Définissez toujours explicitement les polices dans le code. La taille suit la hiérarchie (titre 18-24px → corps 13-15px → annotation 11-13px). Ne descendez jamais sous le plancher de 10px. En cas de débordement de texte : condensez le texte → agrandissez le canevas → dernier recours : réduisez la police (mais jamais sous le plancher).

7. **L'espace blanc est du design.** Zone du graphique 60-70 % du canevas, marges 15-20 %. Au moins 16pt entre le titre et le graphique. Surchargé ≠ riche en informations.

---

## Système de couleurs

### Palettes recommandées

| Palette | Texte | Fond | Remplissage des blocs | Accent |
|---------|------|------------|------------|--------|
| Business Cool | `#243447` | `#F8FAFC` | `#E9EEF3` | `#4C6EF5` |
| Tech Cyan-Gray | `#1F2937` | `#F5F7FA` | `#E6ECF2` | `#3AAFA9` |
| Morandi Warm | `#4B4A45` | `#FAF8F4` | `#EAE4DB` | `#C6866A` |
| Invisible Precision | `#37352F` | `#FFFFFF` | `#F7F7F7` | `#2383E2` |

### 🚫 Couleurs de fond interdites

| Couleur | Valeurs hex interdites |
|-------|---------------------|
| Bleu pur | `#3B82F6`, `#2563EB`, `#1D4ED8` |
| Vert pur | `#10B981`, `#059669`, `#22C55E` |
| Rouge pur | `#EF4444`, `#DC2626`, `#F87171` |
| Violet pur | `#8B5CF6`, `#7C3AED`, `#A855F7` |
| Ambre pur | `#F59E0B`, `#D97706`, `#FB923C` |

### ✅ Couleurs de fond autorisées

| Couleur | Valeurs hex |
|-------|------------|
| Bleu glacier | `#EFF6FF`, `#DBEAFE` |
| Vert menthe | `#F0FDF4`, `#D1FAE5` |
| Ambre clair | `#FFF7ED`, `#FEF3C7` |
| Lavande | `#F5F3FF`, `#EDE9FE` |
| Gris clair | `#F8FAFC`, `#F1F5F9` |

### Couleur fonctionnelle (états uniquement, pas de décoration)
- Actif/sélectionné : accent de la marque ou ligne d'accent `2px`
- Erreur : `#EF4444`
- Succès : `#10B981`
- Étiquettes : fond clair + texte foncé, jamais de pastilles très saturées

### Accessible aux daltoniens
Ne vous fiez pas à la couleur seule — associez forme, style de ligne ou étiquettes directes.
Palette Paul Tol : `['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377']`

### Thème sombre
- Fond : `#0F172A` (pas de noir pur)
- Texte : `#F1F5F9` (pas de blanc pur)
- Grille : `#1E293B`, alpha faible
- Export : `savefig(facecolor='#0F172A')`

---

## Règles d'export

- Graphiques statiques : 200 DPI minimum, 300 DPI recommandé
- Secteurs/radar : **`figsize=(8, 8)` carré** — non carré = elliptique
- Pas plus de 6 couleurs par graphique (scindez sinon)
- L'axe Y d'un diagramme en barres démarre à 0 (les courbes peuvent tronquer)
- Jamais de 3D (délètre les proportions)

### Capture Playwright
`device_scale_factor=2` par défaut. Grandes cartes mentales (3000px+) : 1.5. Intégration PDF : 1-1.5. Impression : 3.
Après rendu, lisez `bounding_box()` et redimensionnez le viewport pour l'ajuster. Viewport minimal : 800px en une colonne, 1200px en multi-colonnes.

### 🚫 INTERDIT : `max-width` sur les conteneurs Mermaid/SVG
Le moteur dagre de Mermaid produit des SVG de largeur imprévisible (surtout avec sous-graphes, texte CJK ou branches parallèles). **Ne JAMAIS définir de `max-width` sur l'élément conteneur Mermaid.** Utilisez plutôt `width: fit-content; min-width: 800px;`.

**Cause racine** : les SVG Mermaid débordent silencieusement de leur conteneur CSS. `bounding_box()` (Playwright) renvoie la taille du modèle de boîte CSS, PAS la taille réellement rendue du SVG. Redimensionner le viewport sur la seule `bounding_box()` produit donc quand même des captures coupées.

**Correctif** : lisez toujours le `getBoundingClientRect()` propre de **l'élément SVG** via `page.evaluate()`, puis utilisez `max(taille_css, taille_svg) + padding` pour les dimensions du viewport. Voir `references/mermaid.md` pour le script de capture corrigé.

### Préservation du rapport d'aspect (intégration)
**OBLIGATOIRE : lisez les dimensions réelles de l'image et calculez la hauteur proportionnellement. Ne codez JAMAIS en dur largeur et hauteur ensemble.**

---

## Règles spécifiques à matplotlib

Elles s'appliquent quand le routage mène à matplotlib/seaborn :

### Mise en page et chevauchements
- Préférez `constrained_layout=True` à `tight_layout()`
- Utilisez la bibliothèque `adjustText` pour repositionner automatiquement les étiquettes — **c'est l'outil anti-chevauchement le plus fiable pour matplotlib.** Installation : `pip install adjustText`. Usage : `from adjustText import adjust_text; adjust_text(texts)`
- 4 sous-graphiques maximum par canevas. Au-delà → scindez en plusieurs images ou `figsize=(20, 16)` minimum
- Multi-sous-graphiques : `GridSpec` avec `wspace/hspace` ≥ 0.3
- Colorbar : `shrink=0.8` + `pad=0.08`
- Étiquettes de données : limite supérieure de l'axe Y avec 15-20 % de réserve (`ylim(0, max_val * 1.18)`)
- Étiquettes X longues → diagramme en barres horizontal ou affichez une étiquette sur N

### Radar / graphiques en toile d'araignée
- **Chaque `fill()` DOIT avoir `alpha=0.25`** (max 0.3). Omettre alpha = opaque = masque les séries sous-jacentes.
- Légende : placez-la hors du graphique avec `bbox_to_anchor`, démarrez avec `(0.5, -0.15), loc='upper center'`. Si les étiquettes de dimensions sont longues ou s'il y a plus de 8 dimensions, augmentez le décalage (ex. `-0.25` ou `-0.3`). INTERDIT aussi : `loc='lower right'` (entre en collision avec les étiquettes de dimensions du radar).
- Padding des étiquettes de dimensions : `set_rlim(0, max_value * 1.2)`
- Étiquettes de plus de 4 caractères CJK : faites-les suivre l'angle ou abrégez
- `figsize=(8, 8)` obligatoire (carré)

### Une couleur, le reste en gris
5 courbes → colorez uniquement la clé, les autres `#D1D5DB`. 8 barres → accentuez uniquement la mise en évidence, le reste `#E5E7EB`.

---

## Règles de connecteurs (schémas structurels)

- Raccordez-vous aux bords des nœuds, pas par les centres
- Préférez les polylignes orthogonales ou des courbes propres
- Les chemins principaux évitent les croisements
- Ne traversez jamais les zones de texte
- Les points de départ/arrivée d'un même niveau doivent s'aligner (pas de décalage)
- Les connecteurs d'un même niveau suivent la même direction
- Angles de virage cohérents (tous à angle droit ou toutes courbes, pas de mélange)
- Positions des étiquettes uniformes (toutes au-dessus de la ligne ou toutes centrées)

---

## Checklist avant livraison

Avant la livraison, vérifiez :

- [ ] Zéro chevauchement (nœuds, connecteurs, étiquettes, légendes — **vérifiez surtout légende vs données, et les étiquettes adjacentes des secteurs/barres**)
- [ ] Aucun connecteur ne traverse une boîte de texte
- [ ] Hiérarchie claire (principaux/secondaires/annotations visuellement distincts)
- [ ] Palette à faible saturation (aucune couleur de fond interdite)
- [ ] Texte lisible à la taille finale (autonome : corps ≥12px, annotations ≥10px ; intégration PDF : ≥10pt/8pt/7pt)
- [ ] Légende entièrement visible, non coupée, ne chevauchant aucun élément du graphique
- [ ] Canevas assez large/haut (vérifiez la bounding box avant la capture)
- [ ] **Si carte mentale** : chaque niveau distinct (≥3 changements de propriétés), connecteurs visibles (≥ `#94A3B8`), équilibre gauche-droite
- [ ] **Si flowchart** : titres de phases distincts des étapes, flèches uniquement entre les phases, **Layout C par défaut**
- [ ] **Si flowchart** : couleurs des phases dans une même famille de teinte (progression bleu-gris), **PAS arc-en-ciel** (bleu→vert→ambre→violet)
- [ ] **Si le flowchart semble dispersé** : STOP — vous utilisez le mauvais layout, passez au Layout C
- [ ] **Si le rendu Mermaid semblait rigide** : déjà basculé vers Playwright+CSS

---

## Anti-patterns en un coup d'œil

| ❌ Ne pas faire | ✅ Faire à la place |
|----------|-------------------|
| Bleu par défaut de matplotlib `#1f77b4` | Utiliser la palette de ce skill |
| Barres/secteurs en 3D | Toujours en 2D |
| Colormap arc-en-ciel (jet/rainbow) | Dégradé monochrome ou divergent |
| Grille noire épaisse | `alpha=0.08` ou supprimer |
| Couleur différente par barre | Même série = même couleur, surbrillance de la clé seulement |
| Étiquettes X inclinées à 45° | Barres horizontales ou raccourcir |
| 8+ sous-graphiques dans un canevas | Scinder en 2-3 images, 4 maximum chacune |
| `tight_layout()` seul | `constrained_layout=True` ou `GridSpec` |
| Étiquettes débordant du graphique | `ylim` avec 18-25 % de réserve |
| Carte mentale : tous les niveaux identiques | Racine+N1 avec boîtes, feuilles en texte simple |
| Carte mentale : image trop haute | Layout gauche-droite dès 5 branches |
| Carte mentale : connecteurs invisibles | Lignes ≥ `#94A3B8`, racine→N1 `#64748B` 2.5px |
| Carte mentale : côtés déséquilibrés | Alterner grandes/petites branches des deux côtés |
| Flowchart : remplissages très saturés | Fond peu saturé (`#EFF6FF`) + bordure saturée (`#3B82F6`) |
| Flowchart : fond sombre + texte sombre | Fond sombre → texte blanc. Fond clair → texte foncé |
| Flowchart : flèches à chaque étape | Flèches UNIQUEMENT entre les phases, les étapes utilisent l'indentation |
| Flowchart : lignes traversant les nœuds | Ne raccorder que les couches adjacentes |
| Flowchart : layout en grille pour un processus par phases | **Toujours utiliser le Layout C (vertical par phases)** |
| Flowchart : titres de phases en étiquettes flottantes | Les titres de phases DOIVENT être dans les cartes de groupe |
| Flowchart : nœuds dispersés sans regroupement | Regrouper les nœuds dans des cartes de phase avec `.phase-group` |
| Flowchart : couleurs de phases arc-en-ciel (bleu→vert→ambre→violet) | Progression bleu-gris de même teinte pour toutes les phases |
| Plusieurs flèches vers le même point d'entrée | Motif fusion-puis-entrée |
| Légende dans le tracé masquant les données | `bbox_to_anchor` hors de la zone de tracé |
| Remplissage radar sans alpha | `alpha=0.25` obligatoire |
| Icônes/emoji décoratifs | Laissez parler les données |
| Grilles là où l'espace blanc suffit | Contraste de fond ou espacement à la place |

---

## Esthétique UI (dashboards / mises en page en cartes)

Pour les sorties de type UI (dashboards, panneaux), appliquez « Invisible Precision » :

- **Frontières** : subtils changements de fond (`#F7F7F7` sur `#FFFFFF`), pas de lignes de bordure. Réservez les séparateurs `1px` aux ruptures logiques absolues.
- **Actions** : CTA principal en neutre foncé (`#1A1A1B`). Secondaire : ghost/gris. Survol : 5 % plus foncé, sans changement de taille.
- **UI discrète** : boutons d'action `opacity: 0` par défaut, `1` au survol. Seuls les éléments actifs reçoivent un indicateur visuel.
- **Nombres** : `font-variant-numeric: tabular-nums` pour un alignement vertical strict.
- **Espacement** : `line-height: 1.625`, espacement généreux des paragraphes.
