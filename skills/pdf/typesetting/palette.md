# Système de Palette de Couleurs

> La couleur est le squelette du design. Unifié, mesuré, systématique. Voyant = amateur.

---

## Système de Palette en Cascade (V2 — Préféré)

La palette de cascade applique une règle de fer : **Surface ∝ 1/Saturation**.
Plus la surface colorée est grande, plus sa saturation doit être faible.

### Système de Niveaux

| Niveau | Surface % | Saturation max | Rôles |
|--------|-----------|----------------|-------|
| **XL** | >50% | ≤ 0.08 | `page_bg`, `section_bg` |
| **L** | 20-50% | ≤ 0.15 | `card_bg`, `table_stripe` |
| **M** | 5-20% | ≤ 0.30 | `header_fill`, `cover_block` |
| **S** | 1-5% | ≤ 0.50 | `border`, `icon` |
| **XS** | <1% | ≤ 0.75 | `accent`, `accent_secondary` |

### Fonctionnement

Une teinte de base → 12 rôles + 4 couleurs sémantiques. Couverture, corps et graphiques tirent tous de la même palette :

```
palette.cascade
  ├── sous-ensemble cover  (page_bg, header_fill, cover_block, accent, text_primary...)
  ├── sous-ensemble body   (page_bg, section_bg, card_bg, table_stripe, border...)
  ├── sous-ensemble chart  (accent comme series_1, accent_secondary comme series_2, ...)
  └── sémantique      (success, warning, error, info — tous à basse saturation)
```

Pas de couleurs orphelines. Pas de dérive du type "couverture terminée, maintenant choisir de nouvelles couleurs pour le corps".

### Règle de la Teinte d'Accent Primaire (V2.1)

**`accent` (niveau XS) DOIT utiliser `base_hue`** — la même teinte que `header_fill`, `cover_block`, `border`, `icon`, et tous les autres rôles structurels. Seule la saturation et la luminosité diffèrent (S=0.50-0.70, L=0.40-0.55 pour les modes clairs).

Cela garantit que les lignes structurelles de couverture, les titres H2 du corps, les en-têtes de tableau et les surbrillons d'accent appartiennent tous visiblement à la **même famille de couleurs**.

`accent_secondary` utilise la teinte d'harmonie géométrique (`accent_hue`) pour la différenciation des séries de graphiques — c'est le **seul** rôle qui peut dévier de `base_hue`.

```
base_hue (ex: 200° bleu acier)
  ├── header_fill:  H=200°, S=0.22, L=0.25   (niveau M, structurel)
  ├── accent:       H=200°, S=0.65, L=0.45   (niveau XS, même teinte, saturation plus élevée)
  └── accent_2:     H=350°, S=0.50, L=0.50   (niveau XS, teinte géométrique pour graphiques)
```

### Utilisation

```bash
# Via design_engine.py
python3 "$PDF_SKILL_DIR/scripts/design_engine.py" palette-cascade --intent cold --mode minimal

# Via pdf.py (dérive automatiquement l'intention du titre)
python3 "$PDF_SKILL_DIR/scripts/pdf.py" palette.cascade --title "2025年度报告" --format reportlab

# Formats: summary (défaut) | json | css | reportlab
```

### Formats de Sortie

- **summary**: Tableau lisible par l'humain avec niveau/rôle/hex/saturation
- **json**: Données structurées complètes (rôles, cover, body, charts, semantic, meta)
- **css**: Propriétés personnalisées CSS prêtes pour HTML/Playwright
- **reportlab**: Code Python prêt à être collé dans des scripts ReportLab

---

## Règles de Fer Fondamentales

### 1. Un Document, Une Famille de Couleurs

**Pas une couleur — une famille de couleurs.**

- Après avoir choisi la couleur primaire, toutes les couleurs secondaires, d'accent et d'arrière-plan doivent en être dérivées
- **`accent` doit partager la même teinte que `header_fill`** — seule la saturation et la luminosité diffèrent
- Méthodes de dérivation : décalage de luminosité, décalage de saturation, micro-ajustement de teinte (±15° max)
- **Interdit** d'avoir des couleurs non liées dans le même document
- La seule exception est `accent_secondary` qui peut utiliser une teinte d'harmonie géométrique pour la différenciation des graphiques

```
Primaire       → Titres, données clés, boutons primaires
Secondaire     → Luminosité primaire ±15-25%
Accent        → Teinte primaire ±10-15°, pour surbrillons/avertissements
Neutre        → Série de gris pour le corps du texte, sans conflit avec le primaire
Arrière-plan  → Blanc pur / primaire à opacité 3-8%
```

### 2. Limites de Nombre de Couleurs

| Type d'Élément | Nb Max de Couleurs | Notes |
|----------------|-------------------|-------|
| Document entier | 4-5 | Primaire + secondaire + accent + neutre + arrière-plan |
| Composant unique (carte/tableau) | 2-3 | Ne pas donner à chaque carte une couleur différente |
| Graphiques / visualisation de données | Dégradé de même famille | Différencier par opacité/luminosité, pas par teintes différentes |
| Étiquettes / badges | 1 couleur + couleur du texte | Pas d'étiquettes arc-en-ciel |

### 3. Règles de Couleur pour Tableaux (Règle de Fer)

Les tableaux sont des éléments de niveau M+L. Leurs couleurs **doivent** provenir du sous-ensemble body de la palette en cascade :

| Élément de Tableau | Rôle Cascade | Niveau | Saturation max | ❌ Jamais Utiliser |
|---------------------|-------------|--------|----------------|-------------------|
| Arrière-plan en-tête | `HEADER_FILL` | M | ≤ 0.30 | `ACCENT` (trop vif pour une zone d'en-tête) |
| Texte en-tête | `colors.white` | — | — | Texte coloré sur fond coloré |
| Lignes paires | `colors.white` | — | — | Remplissages colorés |
| Lignes impaires | `TABLE_STRIPE` | L | ≤ 0.15 | Rayures à haute saturation |
| Bordures/grille | `BORDER` | S | ≤ 0.50 | Noir pur `#000` |

**Pourquoi c'est important :** Les en-têtes de tableau occupent ~5-20% de la surface visuelle. Le système de niveau en cascade dit que les éléments de niveau M (5-20% de surface) doivent avoir S ≤ 0.30. Utiliser `ACCENT` (niveau XS, S = 0.50-0.75) pour les en-têtes de tableau viole la règle surface∝1/saturation et crée des blocs de couleurs discordants qui entrent en conflit avec le corps à faible environnant.

**Tous les tableaux d'un document doivent utiliser des couleurs identiques.** Pas de thèmes de couleur par tableau.

### 3. Remplissages de Couleur Absolument Interdits

Les suivants sont des échecs automatiques :

- ❌ 4 cartes utilisant 4 couleurs complètement différentes (rouge/bleu/vert/violet)
- ❌ Lignes de table alternant en différentes couleurs (ligne bleue/ligne rose)
- ❌ Graphiques circulaires/barres en arc-en-ciel
- ❌ Chaque section avec une couleur de thème différente
- ❌ Dégradé transitionnant de tons chauds à froids (rouge → bleu)
- ❌ Utiliser `ACCENT` (niveau XS) pour les arrière-plans d'en-tête de tableau — utiliser `HEADER_FILL` (niveau M)
- ❌ Utiliser n'importe quelle couleur en dehors de la palette en cascade pour le style des tableaux

---

## Règles de Génération de Couleurs

### Dérivation d'une Palette Complète depuis une Couleur Primaire

```
Étant donné une primaire H(teinte) S(saturation) L(luminosité) :

Primaire:         hsl(H, S, L)           — Titres, éléments clés
Variante foncée:  hsl(H, S, L-15%)       — Survol, bordures, icônes
Variante claire:  hsl(H, S-10%, L+25%)   — Arrière-plans d'étiquettes, remplissages légers
Arrière-plan ultra-léger: hsl(H, S-20%, 96%) — Arrière-plans de section, base de carte
Accent:          hsl(H+15, S, L)        — Avertissements, surbrillons (micro-décalage de teinte)
```

### Exemple : Dérivation depuis une couleur primaire

> ⚠️ Les valeurs hex ci-dessous sont **uniquement des exemples**. En production, utilisez `palette.cascade` ou `palette.generate` pour calculer la palette complète depuis l'intention.

```css
:root {
  --c-primary:    #2d5a87;   /* Primaire (depuis palette.cascade) */
  --c-primary-d:  #1e3d5c;   /* Variante foncée */
  --c-primary-l:  #5a8ab8;   /* Variante claire */
  --c-primary-bg: #f0f4f8;   /* Arrière-plan ultra-léger */
  --c-accent:     #2d6a87;   /* Accent (teinte +10°) */
  --c-text:       #333;      /* Texte du corps */
  --c-text-muted: #888;      /* Texte secondaire */
  --c-border:     #e0e4e8;   /* Lignes de bordure */
}
```

---

## Stratégies de Différenciation d'Éléments Multiples

Lors de la différenciation de plusieurs éléments frères (ex: plusieurs cartes, catégories), **n'utilisez pas de couleurs différentes — utilisez plutôt ces approches** :

### Stratégie A : Même Teinte, Luminosité Différente
```css
.card-1 { background: hsl(220, 40%, 95%); }  /* Le plus clair */
.card-2 { background: hsl(220, 40%, 90%); }
.card-3 { background: hsl(220, 40%, 85%); }
.card-4 { background: hsl(220, 40%, 80%); }  /* Le plus foncé */
```

### Stratégie B : Même Couleur, Opacité Différente
```css
.item-1 { background: rgba(30, 58, 95, 0.06); }
.item-2 { background: rgba(30, 58, 95, 0.12); }
.item-3 { background: rgba(30, 58, 95, 0.18); }
.item-4 { background: rgba(30, 58, 95, 0.24); }
```

### Stratégie C : Primaire + Espace Blanc + Lignes
```css
/* Différencier par couleur/épaisseur/style de bordure, arrière-plan blanc uniforme */
.card-1 { border-left: 3px solid var(--primary); }
.card-2 { border-left: 3px solid var(--primary-l); }
.card-3 { border-left: 3px solid var(--primary-d); }
```

### Stratégie D : Icônes / Numérotation (Pas Couleur)
```css
/* Toutes les cartes de même couleur, différenciées par icônes, nombres ou variations de mise en page */
```

---

## Règles d'Utilisation des Dégradés

### Dégradés Autorisés
- **Dégradé de même famille** : `linear-gradient(135deg, var(--c-primary), var(--c-primary-l))` — différence de teinte < 20°
- **Dégradé de luminosité** : `linear-gradient(180deg, #fff, #f5f5f5)` — changement pur de luminosité
- **Primaire à transparent** : `linear-gradient(90deg, var(--c-primary), transparent)` — pour lignes décoratives

### Dégradés Interdits
- ❌ Croisement chaud-froid : `linear-gradient(#ff6b6b, #4ecdc4)`
- ❌ Plus de 3 couleurs : `linear-gradient(red, yellow, green, blue)`
- ❌ Dégradés néons : N'importe quel dégradé à haute saturation
- ❌ Dégradés gratuits : Dégradés ajoutés purement pour "ça a l' bien" sans but

---

## Palettes Prédéfinies (Prêtes à l'Usage)

### Bleu d'Affaires
```
#1a365d → #2a5298 → #4a7ac7 → #dce6f5 → #f5f8fc
```

### Gris Chaud
```
#2d2d2d → #5a5a5a → #8a8a8a → #e8e8e8 → #f9f9f9
```

### Vert Forêt
```
#1a3c2a → #2d6b4a → #4a9a6a → #d5ead8 → #f2f8f4
```

### Rouge Terre Cuite
```
#5c2018 → #8a3828 → #b85a48 → #f0d8d0 → #faf4f2
```

### Indigo Violet
```
#2d1b4e → #4a2d7a → #6a4aaa → #ddd0f0 → #f5f2fa
```

---

## Vérification Rapide

```
□ Combien de couleurs utilise le document entier ? (Cible ≤ 5)
□ Chaque couleur peut-elle être tracée jusqu'à la couleur primaire ?
□ Y a-t-il des couleurs qui "apparaissent soudainement" sans dérivation ?
□ Les éléments frères sont-ils en arc-en-ciel ?
□ La différence de teinte entre les extrémités du dégradé < 20° ?
□ Si vous retirez toutes les couleurs et ne regardez qu'en niveaux de gris, la hiérarchie est-elle encore claire ?
```
