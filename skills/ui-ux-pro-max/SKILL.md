---
name: ui-ux-pro-max
description: Intelligence de conception UI/UX et directives de mise en œuvre pour la construction d'interfaces soignées. À utiliser lorsque l'utilisateur demande une conception UI, des parcours UX, une architecture d'information, une direction de style visuel, des systèmes/tokens de design, des spécifications de composants, du texte/microcopy, l'accessibilité, ou pour générer/critiquer/affiner une interface frontend (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Inclut des workflows pour (1) générer de nouvelles mises en page et styles UI, (2) améliorer l'UI/UX existante, (3) produire des tokens de système de design et des directives de composants, et (4) transformer les recommandations UX en modifications de code concrètes.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



Suivez ces étapes pour fournir une sortie UI/UX de haute qualité avec un minimum d'allers-retours.

## 1) Tri
Demandez seulement ce qui est nécessaire pour éviter un travail incorrect :
- Plateforme cible : web / iOS / Android / desktop
- Stack (si modifications de code) : React/Next/Vue/Svelte, CSS/Tailwind, bibliothèque de composants
- Objectifs et contraintes : conversion, vitesse, ambiance de marque, niveau d'accessibilité (WCAG AA ?)
- Ce que vous avez : capture d'écran, Figma, dépôt, URL, parcours utilisateur

Si l'utilisateur dit "quán dōu yào" (tout en un - design + UX + code + système de design), traitez-le comme quatre livrables et livrez-les dans cet ordre.

## 2) Produire les Livrables (choisissez ce qui convient)
Soyez toujours concret : nommez les composants, les états, l'espacement, la typographie et les interactions.

- **Concept UI + mise en page** : Fournissez une direction visuelle claire, une grille, une typographie, un système de couleurs, des écrans/sections clés.
- **Parcours UX** : Cartographiez le parcours utilisateur, les chemins critiques, les états d'erreur/vide/chargement, les cas particuliers.
- **Système de design** : Tokens (couleur/typographie/espacement/rayon/ombre), règles de composants, notes d'accessibilité.
- **Plan de mise en œuvre** : Modifications exactes au niveau des fichiers, décomposition des composants, et critères d'acceptation.

## 3) Utiliser les Ressources Groupées
Cette compétence regroupe des données que vous pouvez citer pour l'inspiration/les normes.

- **Données d'intelligence de design** : Lisez depuis `skills/ui-ux-pro-max/assets/data/` lorsque vous avez besoin de palettes, de motifs, ou d'heuristiques UI/UX.
- **Référence amont** : Si vous avez besoin de plus de formulations/exemples, consultez `skills/ui-ux-pro-max/references/upstream-skill-content.md`.

## 4) Script Optionnel (Générateur de Système de Design)
Si vous avez besoin de générer rapidement des tokens et des substitutions spécifiques à la page, utilisez le script groupé :

```bash
python3 skills/ui-ux-pro-max/scripts/design_system.py --help
```

Préférez l'exécuter lorsque l'utilisateur veut une sortie de token structurée (compatible ASCII).

## Normes de Sortie
- Par défaut, utilisez uniquement des tokens/variables ASCII sauf si le projet utilise déjà Unicode.
- Incluez : échelle d'espacement, échelle de typographie, 2-3 options de paires de polices, tokens de couleur, états de composants.
- Couvrez toujours : états vide/chargement/erreur, navigation au clavier, états de focus, contraste.