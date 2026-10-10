---
name: ui-ux-pro-max
version: "1.0.0"
category: "Visualisation & Design"
tags:
  - ui
  - ux
  - pro
  - max
description: Intelligence de design UI/UX et guidance d'implémentation pour construire des interfaces soignées. À utiliser quand l'utilisateur demande du design UI, des flux UX, de l'architecture d'information, une direction de style visuel, des design systems/tokens, des specs de composants, de la copy/microcopy, de l'accessibilité, ou pour générer/critiquer/affiner une UI frontend (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Inclut des workflows pour (1) générer de nouvelles mises en page et styles UI, (2) améliorer une UI/UX existante, (3) produire des tokens de design system et des guidelines de composants, et (4) transformer des recommandations UX en changements de code concrets.
language: fr

read_when:
  - Déclencher quand la demande concerne : intelligence de design UI/UX et guidance d'implémentation pour construire des interfaces soignées
  - Déclencher si la demande mentionne : design, tokens, composants
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



Suis ces étapes pour produire un rendu UI/UX de haute qualité avec un minimum d'allers-retours.

## 1) Triage
Ne demande que le strict nécessaire pour éviter un travail erroné :
- Plateforme cible : web / iOS / Android / desktop
- Stack (si modifications de code) : React/Next/Vue/Svelte, CSS/Tailwind, bibliothèque de composants
- Objectif et contraintes : conversion, rapidité, ambiance de marque, niveau d'accessibilité (WCAG AA ?)
- Ce dont tu disposes : capture d'écran, Figma, repo, URL, parcours utilisateur

Si l'utilisateur demande « tout » (design + UX + code + design system), traite-le comme quatre livrables et livre-les dans cet ordre.

## 2) Produire les livrables (choisis ceux qui conviennent)
Sois toujours concret : nomme les composants, les états, les espacements, la typographie et les interactions.

- **Concept UI + mise en page** : fournis une direction visuelle claire, une grille, une typographie, un système de couleurs, les écrans/sections clés.
- **Flux UX** : cartographie le parcours utilisateur, les chemins critiques, les états d'erreur/vide/chargement, les cas limites.
- **Design system** : tokens (couleur/typographie/espacement/radius/ombre), règles de composants, notes d'accessibilité.
- **Plan d'implémentation** : modifications exactes au niveau des fichiers, décomposition des composants et critères d'acceptation.

## 3) Utiliser les ressources intégrées
Ce skill intègre des données que tu peux citer comme inspiration/standards.

- **Données de design intelligence** : lis `skills/ui-ux-pro-max/assets/data/` quand tu as besoin de palettes, de patterns ou d'heuristiques UI/UX.
- **Référence amont** : si tu as besoin de formulations/d'exemples supplémentaires, consulte `skills/ui-ux-pro-max/references/upstream-skill-content.md`.

## 4) Script optionnel (générateur de design system)
Si tu dois générer rapidement des tokens et des overrides spécifiques à une page, utilise le script intégré :

```bash
python3 skills/ui-ux-pro-max/scripts/design_system.py --help
```

Privilégie son exécution quand l'utilisateur veut une sortie de tokens structurée (compatible ASCII).

## Standards de sortie
- Par défaut, utilise des tokens/variables en ASCII uniquement, sauf si le projet utilise déjà Unicode.
- Inclus : échelle d'espacement, échelle typographique, 2-3 options de paires de polices, tokens de couleur, états de composants.
- Couvre toujours : états vides/chargement/erreur, navigation clavier, états de focus, contraste.
