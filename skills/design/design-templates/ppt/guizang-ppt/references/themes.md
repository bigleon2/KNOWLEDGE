# Couleurs de thème prédéfinies (Themes)

5 thèmes de palettes de couleurs méticuleusement ajustés, garantissant que l'esthétique « magazine électronique × encre électronique » ne s'effondre pas. **L'utilisateur n'est pas autorisé à personnaliser les couleurs — un mauvais agencement gâche instantanément l'aspect** ; choisir uniquement parmi les préréglages suivants.

---

## Mode d'emploi

1. Demander à l'utilisateur quel ensemble il choisit (ou recommander un ensemble en fonction du contenu)
2. Ouvrir le bloc `<style>` de `assets/template.html`
3. Repérer le bloc `:root{` au début
4. **Remplacement complet** des lignes marquées de la note « couleur du thème » `--ink` / `--ink-rgb` / `--paper` / `--paper-rgb` / `--paper-tint` / `--ink-tint`
5. Tout le reste du CSS passe par des `var(--...)`, aucune autre modification n'est nécessaire

---

## 🖋 Encre classique (Monocle par défaut)

**Convient à** : partage universel, publication commerciale, produits technologiques — choix par défaut sûr en toutes circonstances.
**Ton** : noir encre pur + blanc cassé chaud, effet magazine maximal, style Monocle / Apricot / A Book Apart.

```css
--ink:#0a0a0b;
--ink-rgb:10,10,11;
--paper:#f1efea;
--paper-rgb:241,239,234;
--paper-tint:#e8e5de;
--ink-tint:#18181a;
```

---

## 🌊 Indigo porcelaine (Indigo Porcelain)

**Convient à** : technologie/recherche/partage de données, culture d'ingénierie, contenu approfondi, conférences technologiques.
**Ton** : bleu indigo profond + blanc porcelaine, calme, rationnel, avec de la profondeur, comme une revue académique ou une porcelaine à décor bleu.

```css
--ink:#0a1f3d;
--ink-rgb:10,31,61;
--paper:#f1f3f5;
--paper-rgb:241,243,245;
--paper-tint:#e4e8ec;
--ink-tint:#152a4a;
```

---

## 🌿 Encre forêt (Forest Ink)

**Convient à** : nature/durabilité/culture/documentaire, marques liées au plein air, thématiques environnementales.
**Ton** : vert forêt profond + ivoire, posé, respirant, comme les anciens numéros de « National Geographic ».

```css
--ink:#1a2e1f;
--ink-rgb:26,46,31;
--paper:#f5f1e8;
--paper-rgb:245,241,232;
--paper-tint:#ece7da;
--ink-tint:#253d2c;
```

---

## 🍂 Papier kraft (Kraft Paper)

**Convient à** : nostalgie/humanités/lecture/histoire/littérature, magazines indépendants, marques artisanales.
**Ton** : brun profond + beige chaud, comme une enveloppe kraft ou un vieux carnet, chaleureux, avec une patine d'époque.

```css
--ink:#2a1e13;
--ink-rgb:42,30,19;
--paper:#eedfc7;
--paper-rgb:238,223,199;
--paper-tint:#e0d0b6;
--ink-tint:#3a2a1d;
```

---

## 🌙 Dune

**Convient à** : art/design/création/mode, catalogues de galeries, rencontres privées où l'esthétique prime.
**Ton** : gris anthracite + couleur de sable, retenu, raffiné, neutre, comme un crépuscule dans le désert ou un album d'architecture.

```css
--ink:#1f1a14;
--ink-rgb:31,26,20;
--paper:#f0e6d2;
--paper-rgb:240,230,210;
--paper-tint:#e3d7bf;
--ink-tint:#2d2620;
```

---

## Table de recommandation

| Si le contenu est... | Thème recommandé |
|---|---|
| Aucune idée / première utilisation | 🖋 Encre classique |
| IA / technologie / lancement produit | 🌊 Indigo porcelaine |
| Contenu / veille sectorielle / culture | 🌿 Encre forêt |
| Critiques de livres / art de vivre / humanités | 🍂 Papier kraft |
| Design / art / marque | 🌙 Dune |

---

## Principes de bascule

- **Un seul et même thème par deck**, ne pas changer de couleur en cours de route
- La couleur principale par défaut du shader WebGL (dispersion or titane / flux argenté) est compatible avec les 5 ensembles (testé et validé)
- Les bordures et icônes pilotées par `currentColor` s'adaptent automatiquement à la couleur de texte de la section, aucun réglage supplémentaire n'est nécessaire
- Une fois le thème choisi, le texte `<title>` et les libellés du `chrome` peuvent renforcer la sémantique du thème (par exemple associer Papier kraft à un « Vol.03 · Automne »)

## ❌ À ne pas faire

- ❌ **Aucun mélange autorisé** (par exemple encre de l'Encre classique + papier de la Dune) — cela produirait une rupture totale d'harmonie
- ❌ **Refuser poliment toute valeur hex donnée au hasard par l'utilisateur** — présenter les 5 préréglages et faire choisir
- ❌ **Ne pas modifier directement les couleurs ailleurs dans template.html** — tous les rgba épars passent par des var, modifier `:root` suffit

Une fois le thème choisi, indiquer à l'utilisateur dans le dialogue du skill : « avec 🖋 Encre classique / 🌊 Indigo porcelaine... » et le consigner dans le dossier projet du deck, pour garder la cohérence lors des itérations suivantes.
