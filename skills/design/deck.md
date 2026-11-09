---
name: Deck Skill
description: Conception de présentations HTML, présentations, pitch decks, rapports visuels et présentations narratives.
mode: deck
platform: presentation
scenario: deck
preview:
  type: html
default_for:
  - deck
  - presentation
  - slide deck
  - pitch deck
  - product deck
  - report deck
  - strategy deck
  - workshop deck
  - yǎnshì wén gǎo (présentation)
  - lùyǎn cáiliào (matériel de pitch)
speaker_notes: optional
animations: optional
fidelity: high
---

# Deck Skill

Concevoir une présentation paginée, une diapositive à la fois, qui raconte une histoire — chaque diapositive fait
un point, et la séquence construit un argument.

Jugement, pas un manuel. Utilisez le goût. Techniques : `horizontal-craft/technique-library.md` ; vérification
de la livraison : `skills/design/quality-gate.md`. Pour un runtime/template de base, voir
`skills/design/prototype-templates/` (graine html-ppt) et la Règle de Modèle Prédéfini dans SKILL.md.

## Route ailleurs si

- c'est une page web défilable (non paginée) → `landing-page.md` / `content-page.md`
- c'est un produit interactif → `prototype.md`

## Ce qui fait réussir une présentation : une idée par diapositive, une histoire à travers les diapositives

Le mode d'échec est des diapositives avec du texte déversé sans colonne vertébrale narrative — des murs de puces qui auraient
dû être un document. Donc :

- **Une idée par diapositive.** Chaque diapositive a un seul enseignement, clairement énoncé. Si une diapositive a besoin de deux
  points, c'est deux diapositives.
- **Un arc narratif.** La présentation a un début (problème/contexte), un milieu (argument/preuves),
  et une fin (demande/conclusion). Organisez les diapositives pour construire, pas seulement énumérer.
- **Montrez, ne déversez pas.** Visualisez les relations et les données ; une phrase + une forte visuelle bat un
  paragraphe. Les notes de l'orateur portent le détail, pas la diapositive.

## Les quelques décisions qui comptent

- **Type et ton de présentation** — pitch (persuasif, audacieux), rapport (clair, sobre), stratégie (structuré),
  atelier (interactif). Cela définit la densité, la couleur et le rythme.
- **Colonne vertébrale narrative** — la séquence des enseignements avant toute visuel. Mettez d'abord l'histoire au point.
- **Rythme des diapositives** — variez les types de diapositives (affirmation, données, comparaison, citation, rupture de section) ;
  ne répétez pas la même mise en page 20 fois. Utilisez des pleins écrans pour l'emphase.
- **Honnêteté des données** — graphiques avec axes/unités/échelles corrects ; le titre indique l'insight ;
  n'inventez jamais de nombres.

## Non négociables

- Une idée par diapositive ; les détails destinés à l'orateur vont dans les notes, pas sur la diapositive.
- N'inventez jamais de données, citations ou métriques ; graphiques fidèles aux nombres réels.
- Système cohérent (échelle de typographie, couleur, espacement) sur toutes les diapositives.
- Pas d'emoji décoratifs comme icônes (utilisez du SVG) ; pas de Lorem ipsum.

## Éviter le biais IA (un principe)

Catalogué dans `quality-gate.md`. Principe : la mise en page de chaque diapositive sert son point spécifique, pas un
modèle répété. Un titre + trois puces sur chaque diapositive, une diapositive de titre générique avec dégradé,
des rangées d'icônes-fonction identiques — réflexes. Variez avec intention ; quand une diapositive semble être du remplissage, coupez-la.

## Workflow

1. Définissez le type de présentation, l'audience et la seule demande/conclusion.
2. Écrivez la colonne vertébrale narrative (les enseignements ordonnés) avant de concevoir les diapositives.
3. Concevez les diapositives — une idée chacune, rythme varié, visuels plutôt que texte ; détail dans les notes de l'orateur.
4. Techniques/animations de `horizontal-craft/technique-library.md` seulement quand elles aident le point ; mouvement réduit.
5. Porte de qualité avant livraison ; vérifiez l'honnêteté des données et une-idea-par-diapositive.

## Références (chargez seulement quand pertinent)

- `horizontal-craft/chinese-typography.md` — texte chinois substantiel (Baseline Runtime Obligatoire).
- `horizontal-craft/icon-system.md` — quand des icônes sont utilisées.
- `canvas-and-device.md` — dimensions des diapositives / tailles d'exportation.
- `design-system-reference.md` — quand une référence marque/style/modèle est donnée (voir Routage de Style SKILL.md).
- `horizontal-craft/technique-library.md` — transitions mesurées seulement quand elles aident la narration.

## Contexte Créatif

Pour les demandes ouvertes, complétez le Contexte Créatif de SKILL.md (creative_positioning,
first_impression, anti_default) avant de générer.

## Porte Finale Obligatoire

Exécutez `quality-gate.md` comme vérification bloquante. Doit satisfaire : une idée par diapositive ; données/graphiques honnêtes ;
système cohérent sur les diapositives ; pas de nombres/citations inventés ; pas d'emoji-comme-icônes / Lorem ipsum ;
focus visible et mouvement réduit là où c'est interactif ; bloc de Conformité de Design non visible correspondant
au code. Appliquez `horizontal-craft/chinese-typography.md` si texte chinois substantiel.

## Remise

Peut continuer vers : `design-system-reference.md`, `design-system-generation.md`, `export.md`,
`skills/version-management/SKILL.md`, modifications intégrées de région sélectionnée, et gestion de paramètres locaux.