# Préréglages de style — changer les 8 variables CSS du `:root` suffit pour basculer

Chaque préréglage fait 8 lignes de CSS. Pour changer de style, remplacer les lignes correspondantes du bloc `:root` dans `template.html`.
Ne pas toucher aux polices (sauf si l'utilisateur demande explicitement un changement), afin de préserver la texture industrielle / musée.

---

## 1. default — bleu acier froid (par défaut / version originale « objets retenus »)

```css
:root{
  --bg:        #e6e9ee;
  --bg-soft:   #f1f3f6;
  --paper:     #c9cfd6;
  --ink:       #0c0f14;
  --ink-soft:  #535963;
  --line:      #aab0b8;
  --line-soft: #c4c9d0;
  --steel:     #3a4a5a;
}
```
Convient à : industriel scandinave, collections mécaniques, métal gris, instruments, objets en fonte
Mots-clés déclencheurs : retenu / scandinave / industriel / acier / gris

---

## 2. warm-leather — brun chaud rétro

```css
:root{
  --bg:        #ece4d6;
  --bg-soft:   #f4eee2;
  --paper:     #d8cdb8;
  --ink:       #1c160e;
  --ink-soft:  #6e5e44;
  --line:      #b6a787;
  --line-soft: #cdc1a5;
  --steel:     #8a5a2e;   /* cuivre brun */
}
```
Convient à : cuir, bois, pipes, appareils photo, vieilles horloges, mobilier vintage
Mots-clés déclencheurs : chaud / rétro / brun / cuir / nostalgie / objets anciens

---

## 3. night-iron — fer de nuit

```css
:root{
  --bg:        #14161a;
  --bg-soft:   #1c1f24;
  --paper:     #2a2e35;
  --ink:       #e8eaee;     /* inversion : fond sombre, texte clair */
  --ink-soft:  #9aa0a8;
  --line:      #3a3f46;
  --line-soft: #2a2e34;
  --steel:     #c9a35a;   /* or sombre */
}
```
Convient à : hi-fi haut de gamme, claviers mécaniques, pétards et feux d'artifice, produits en tons sombres, luminaires
Mots-clés déclencheurs : sombre / foncé / nuit / or sombre / noir

Note : avec ce préréglage, ajuster aussi les deux couleurs radiales du `background-image` du body vers des tons plus profonds, suggestion :
```css
body{
  background-image:
    radial-gradient(at 20% 22%, rgba(58,74,90,0.18) 0px, transparent 50%),
    radial-gradient(at 78% 80%, rgba(201,163,90,0.05) 0px, transparent 55%);
}
```

---

## 4. paper-press — papier imprimé

```css
:root{
  --bg:        #f3eee2;
  --bg-soft:   #faf5e8;
  --paper:     #e2d9c1;
  --ink:       #181410;
  --ink-soft:  #5a4f3e;
  --line:      #b9ac8e;
  --line-soft: #cec3a6;
  --steel:     #9a3324;   /* rouge plomb */
}
```
Convient à : livres, papeterie, imprimés, carnets artisanaux, contenu presse
Mots-clés déclencheurs : papier / impression / report / papeterie / presse / édition

---

## 5. navy-blueprint — blueprint marine

```css
:root{
  --bg:        #1f2a3a;
  --bg-soft:   #263244;
  --paper:     #324154;
  --ink:       #f4f6fa;
  --ink-soft:  #aab6c8;
  --line:      #4a5568;
  --line-soft: #2e3a4d;
  --steel:     #ffffff;     /* traits blancs */
}
```
Convient à : instruments maritimes, aéronautique, navigation, pièces navales, cadrans sombres
Mots-clés déclencheurs : marine / blueprint / blueprint / navigation / navire

Note : il est conseillé de passer aussi le fond du bandeau défilant `.ticker` à `var(--bg-soft)` et son texte à `var(--ink)`, sinon le texte sombre sur fond clair devient illisible.

---

## 6. ceramic-clay — terre cuite et argile

```css
:root{
  --bg:        #e7d8c4;
  --bg-soft:   #f1e6d5;
  --paper:     #d3bfa3;
  --ink:       #2a1c12;
  --ink-soft:  #6b4f38;
  --line:      #b39472;
  --line-soft: #c8ad8c;
  --steel:     #5e3a1f;   /* brun de four */
}
```
Convient à : poteries, porcelaines, objets ottomans, antiquités d'Asie de l'Est, artisanat aux accents terreux
Mots-clés déclencheurs : poterie / porcelaine / terre / four / argile

---

## 7. mint-laboratory — menthe de laboratoire

```css
:root{
  --bg:        #e8efea;
  --bg-soft:   #f1f5f2;
  --paper:     #c8d4ce;
  --ink:       #102018;
  --ink-soft:  #4f655a;
  --line:      #99ada3;
  --line-soft: #b9c7bf;
  --steel:     #2a6e5a;   /* vert mousse */
}
```
Convient à : matériel médical, verrerie, instruments de laboratoire, végétal, médical neutre
Mots-clés déclencheurs : laboratoire / médical / verre / mousse / vert

---

## Comment choisir

Si l'utilisateur n'a pas précisé de style, choisir automatiquement selon la catégorie :

| Catégorie | Style par défaut |
|---|---|
| Fonte, acier, mécanique, objets scandinaves | default |
| Bois, cuir, rétro, photo | warm-leather |
| Audio, luminaires, haut de gamme sombre | night-iron |
| Papeterie, articles papier, livres | paper-press |
| Maritime, aéronautique, navigation | navy-blueprint |
| Céramique, objets d'Asie de l'Est | ceramic-clay |
| Instruments de laboratoire, médical, verre | mint-laboratory |
| Incertain | default (le plus sûr) |
