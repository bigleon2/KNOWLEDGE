---
name: visual-design-foundations
version: "1.0.0"
category: "Visualisation & Design"
tags:
  - visual
  - design
  - foundations
description: Applique la typographie, la théorie des couleurs, les systèmes d'espacement et les principes d'iconographie pour créer des designs visuels cohérents. À utiliser pour établir des design tokens, construire des guides de style, ou améliorer la hiérarchie visuelle et la cohérence.
language: fr

read_when:
  - Déclencher quand la demande concerne : applique la typographie, la théorie des couleurs, les systèmes d'espacement et les principes d'iconographie po…
  - Déclencher si la demande mentionne : applique, typographie, théorie
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Visual Design Foundations

Construisez des systèmes visuels cohérents et accessibles en vous appuyant sur les fondamentaux de la typographie, de la couleur, de l'espacement et de l'iconographie.

## Quand utiliser ce skill

- Établir des design tokens pour un nouveau projet
- Créer ou affiner un système d'espacement et de dimensionnement
- Choisir et associer des polices de caractères
- Construire des palettes de couleurs accessibles
- Concevoir des systèmes d'icônes et des ressources visuelles
- Améliorer la hiérarchie visuelle et la lisibilité
- Auditer des designs pour la cohérence visuelle
- Implémenter le mode sombre ou le theming

## Systèmes fondamentaux

### 1. Échelle typographique

**Échelle modulaire** (dimensionnement basé sur des ratios) :

```css
:root {
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px */
  --font-size-5xl: 3rem; /* 48px */
}
```

**Recommandations d'interligne** :
| Type de texte | Interligne |
|-----------|-------------|
| Titres | 1.1 - 1.3 |
| Corps de texte | 1.5 - 1.7 |
| Libellés UI | 1.2 - 1.4 |

### 2. Système d'espacement

**Grille de 8 points** (standard du secteur) :

```css
:root {
  --space-1: 0.25rem; /* 4px */
  --space-2: 0.5rem; /* 8px */
  --space-3: 0.75rem; /* 12px */
  --space-4: 1rem; /* 16px */
  --space-5: 1.25rem; /* 20px */
  --space-6: 1.5rem; /* 24px */
  --space-8: 2rem; /* 32px */
  --space-10: 2.5rem; /* 40px */
  --space-12: 3rem; /* 48px */
  --space-16: 4rem; /* 64px */
}
```

### 3. Système de couleurs

**Tokens de couleurs sémantiques** :

```css
:root {
  /* Brand */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-active: #1e40af;

  /* Semantic */
  --color-success: #16a34a;
  --color-warning: #ca8a04;
  --color-error: #dc2626;
  --color-info: #0891b2;

  /* Neutral */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
}
```

## Démarrage rapide : design tokens dans Tailwind

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      fontSize: {
        xs: ["0.75rem", { lineHeight: "1rem" }],
        sm: ["0.875rem", { lineHeight: "1.25rem" }],
        base: ["1rem", { lineHeight: "1.5rem" }],
        lg: ["1.125rem", { lineHeight: "1.75rem" }],
        xl: ["1.25rem", { lineHeight: "1.75rem" }],
        "2xl": ["1.5rem", { lineHeight: "2rem" }],
      },
      colors: {
        brand: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
        },
      },
      spacing: {
        // Extends default with custom values
        18: "4.5rem",
        88: "22rem",
      },
    },
  },
};
```

## Bonnes pratiques typographiques

### Association de polices

**Combinaisons sûres** :

- Titres : **Inter** / Corps : **Inter** (famille unique)
- Titres : **Playfair Display** / Corps : **Source Sans Pro** (contraste)
- Titres : **Space Grotesk** / Corps : **IBM Plex Sans** (géométrique)

### Typographie responsive

```css
/* Fluid typography using clamp() */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 3.5rem);
  line-height: 1.1;
}

p {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.125rem);
  line-height: 1.6;
  max-width: 65ch; /* Optimal reading width */
}
```

### Chargement des polices

```css
/* Prevent layout shift */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter.woff2") format("woff2");
  font-display: swap;
  font-weight: 400 700;
}
```

## Théorie des couleurs

### Exigences de contraste (WCAG)

| Élément            | Ratio minimum |
| ------------------ | ------------- |
| Corps de texte     | 4.5:1 (AA)    |
| Texte large (18px+) | 3:1 (AA)      |
| Composants UI      | 3:1 (AA)      |
| Renforcé           | 7:1 (AAA)     |

### Stratégie de mode sombre

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
}

[data-theme="dark"] {
  --bg-primary: #111827;
  --bg-secondary: #1f2937;
  --text-primary: #f9fafb;
  --text-secondary: #9ca3af;
  --border: #374151;
}
```

### Accessibilité des couleurs

```tsx
// Check contrast programmatically
function getContrastRatio(foreground: string, background: string): number {
  const getLuminance = (hex: string) => {
    const rgb = hexToRgb(hex);
    const [r, g, b] = rgb.map((c) => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);

  return (lighter + 0.05) / (darker + 0.05);
}
```

## Recommandations d'espacement

### Espacement des composants

```
Card padding:      16-24px (--space-4 to --space-6)
Section gap:       32-64px (--space-8 to --space-16)
Form field gap:    16-24px (--space-4 to --space-6)
Button padding:    8-16px vertical, 16-24px horizontal
Icon-text gap:     8px (--space-2)
```

### Rythme visuel

```css
/* Consistent vertical rhythm */
.prose > * + * {
  margin-top: var(--space-4);
}

.prose > h2 + * {
  margin-top: var(--space-2);
}

.prose > * + h2 {
  margin-top: var(--space-8);
}
```

## Iconographie

### Système de tailles d'icônes

```css
:root {
  --icon-xs: 12px;
  --icon-sm: 16px;
  --icon-md: 20px;
  --icon-lg: 24px;
  --icon-xl: 32px;
}
```

### Composant Icône

```tsx
interface IconProps {
  name: string;
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  className?: string;
}

const sizeMap = {
  xs: 12,
  sm: 16,
  md: 20,
  lg: 24,
  xl: 32,
};

export function Icon({ name, size = "md", className }: IconProps) {
  return (
    <svg
      width={sizeMap[size]}
      height={sizeMap[size]}
      className={cn("inline-block flex-shrink-0", className)}
      aria-hidden="true"
    >
      <use href={`/icons.svg#${name}`} />
    </svg>
  );
}
```

## Bonnes pratiques

1. **Établissez des contraintes** : limitez les choix pour maintenir la cohérence
2. **Documentez les décisions** : créez un guide de style vivant
3. **Testez l'accessibilité** : vérifiez le contraste, les tailles, les cibles tactiles
4. **Utilisez des tokens sémantiques** : nommez selon l'usage, pas selon l'apparence
5. **Concevez mobile-first** : partez des contraintes, ajoutez de la complexité
6. **Maintenez le rythme vertical** : un espacement cohérent crée l'harmonie
7. **Limitez les graisses de police** : 2 à 3 graisses par famille suffisent

## Problèmes courants

- **Espacement incohérent** : absence d'échelle définie
- **Contraste insuffisant** : non-respect des exigences WCAG
- **Surcharge de polices** : trop de familles ou de graisses
- **Nombres magiques** : valeurs arbitraires au lieu de tokens
- **États manquants** : oubli des états hover, focus, disabled
- **Absence de plan de mode sombre** : l'adaptation a posteriori est plus difficile que la planification
