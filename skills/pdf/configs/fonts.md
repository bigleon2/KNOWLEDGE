# Système de polices

## Piles de polices (par pipeline)

### Pipeline Créative (Playwright / HTML)

Les polices sont chargées via Google Fonts CDN dans l'en-tête HTML `<head>` :

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
```

#### Police variable (pour la mise en page de type tension)

Lorsque `tension_score` est utilisé sur `Glass_Canvas`, le moteur bascule vers **Inter Variable** pour une interpolation de poids continue (100–900) :

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
```

Ceci permet `font-variation-settings: 'wght' <valeur>` pour des transitions de poids fluides et non discrètes. L'URL de poids standard discret est toujours utilisée lorsque la tension n'est pas active.

| Variable | Pile | Usage |
|----------|-------|-------|
| `--font-sans` | Inter, Noto Sans SC, Liberation Sans, Noto Color Emoji, sans-serif | Texte du corps, éléments UI, statistiques |
| `--font-serif` | Playfair Display, Noto Serif SC, Cormorant Garamond, Noto Color Emoji, serif | Texte principal, titres éditoriaux |
| `--font-mono` | Liberation Mono, DejaVu Sans Mono, Noto Color Emoji, monospace | Métadonnées flottantes, horodatages, codes |

### Pipeline Rapport (ReportLab)

ReportLab nécessite des polices enregistrées. La police chinoise principale est **Noto Serif SC** (siyuan songti, police serif avec des traits nets et élégants) :

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Police chinoise principale — Noto Serif SC (serif, haute qualité, licence OFL)
# FONT_DIR = '/usr/share/fonts' (Linux) ou '~/.openclaw/workspace/fonts' (macOS)
pdfmetrics.registerFont(TTFont('NotoSerifSC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')

# Polices chinoises de secours / héritées (sans-serif, poids statique)
pdfmetrics.registerFont(TTFont('Noto Sans SC', f'{FONT_DIR}/truetype/chinese/NotoSansSC-Regular.ttf'))  # secours sans-serif
pdfmetrics.registerFont(TTFont('Noto Sans SC Bold', f'{FONT_DIR}/truetype/chinese/NotoSansSC-Bold.ttf'))
# Utiliser 'NotoSerifSC' pour le corps, 'NotoSerifSC-Bold' pour les titres
```

> **⚠️ ReportLab NE PEUT PAS restituer les emoji.** Si le contenu contient des emoji, rediriger vers le pipeline Créatif.

### Pipeline Académique (Tectonic / LaTeX)

Prise en charge CJK via le package `ctex` :
```latex
\usepackage{ctex}  % Sélectionne automatiquement les polices CJK appropriées
```

Pour la sélection manuelle de polices :
```latex
\setCJKmainfont{Noto Serif CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
```

> **⚠️ LaTeX supprime silencieusement les caractères emoji.** Si le contenu contient des emoji, rediriger vers le pipeline Créatif.

## Police de secours pour emoji

Toutes les piles de polices du pipeline Créatif incluent une police de secours pour emoji :
- **macOS** : `Noto Color Emoji` (multiplateforme, emoji pleine couleur)
- **Windows** : `Noto Color Emoji`
- **Linux** : `Noto Color Emoji` (installation : `apt install fonts-noto-color-emoji`)

Chromium (utilisé par Playwright) sur macOS restitue les emoji nativement — aucune configuration supplémentaire n'est nécessaire.

## Guide de poids de police CJK

| Valeur de poids | Équivalent Inter | Nom Noto Sans SC | Usage |
|-------------|------------------|-------------------|-------|
| 300 | Light | Light | Sous-titres, légendes, métadonnées |
| 400 | Regular | Regular | Texte du corps |
| 500 | Medium | Medium | Demi-emphase |
| 700 | Bold | Bold | Titres, emphase |
| 900 | Black | Black | Texte principal, nombres de statistiques |

> **Astuce** : Les poids Noto Sans SC 300–900 couvrent la plupart des cas d'utilisation. Toujours charger au moins 400 et 700 via Google Fonts.

## Échelle de taille de police

Échelle de type recommandée (base : 16px pour le corps) :

| Rôle | Taille | Poids | Interligne |
|------|------|--------|-------------|
| Numéro fantôme de page | 240px | 900 | 1.0 |
| Héros (grand) | clamp(48px, 10vw, 110px) | 900 | 0.88 |
| Héros (serif fin) | clamp(48px, 10vw, 110px) | 100 | 0.88 |
| Nombre statistique | clamp(32px, 5vw, 56px) | 900 | 0.9 |
| Titre de section | 24px | 800 | 1.2 |
| Sous-section | 20px | 700 | 1.3 |
| Corps | 16px | 400 | 1.6–1.7 |
| Légende | 14px | 400 | 1.5 |
| Métadonnées flottantes | 10px | 400 (mono) | 1.4 |
| Étiquette statistique | 11px | 400 | 1.2 |