---
name: Design System Generation Skill
description: Import, extract, normalize, or persist a reusable DESIGN.md from an existing design system, HTML artifact, screenshot, template, style reference, or generated interface.
---

# Design System Generation Skill

Transformer des règles visuelles en un `DESIGN.md` réutilisable. La génération ordinaire d'une première page n'a **pas besoin** de ce skill ; il sert uniquement quand l'utilisateur veut importer, extraire, normaliser, pérenniser ou réutiliser un langage de design. Idée centrale (empruntée à la méthode DESIGN.md) : décrire le système visuel en langage naturel, conserver les valeurs exactes quand elles existent, et expliquer **pourquoi** chaque choix de design existe, pas seulement à quoi il ressemble. Le produit transite par `skills/design/design-system-reference.md` pour être réutilisé lors des générations futures.

## Trois modes

- **Import** : l'utilisateur fournit un `DESIGN.md`/une charte existante à transformer en référence réutilisable. Conduite : lire, conserver les règles propres de l'utilisateur, contrôler les sections manquantes, normaliser la structure seulement si utile, **ne pas réécrire selon le goût du modèle**, conserver les valeurs exactes, signaler les ambiguïtés si nécessaire. (« voici mon DESIGN.md, s'y conformer ensuite », « vérifie s'il manque quelque chose »)
- **Extraction** : extraire les règles de design depuis HTML/capture/gabarit/page/CSS/style skill/référence de marque. Conduite : inspecter la source, extraire valeurs et motifs visibles, distinguer valeurs exactes et valeurs inférées, **décrire à la fois le style de surface et l'intention sous-jacente**, ne pas recopier mécaniquement chaque CSS, ne rien inventer, séparer règles réutilisables et détails ponctuels. (« distille un DESIGN.md de ce HTML », « résume cette capture en système de design »)
- **Persistence** : congeler le style du produit courant, déjà validé, en système réutilisable. Conduite : inspecter le produit courant, extraire les règles stables du design validé, identifier ce qui doit se répéter et ce qui est ponctuel, **ne pas ériger les détails propres à la page en règle générale**. (« fige le style de la page courante en DESIGN.md », « les pages suivantes reprennent cette version »)

Si plusieurs modes s'appliquent, suivre la demande explicite de l'utilisateur.

## Quand ne PAS utiliser ce skill

Générer une simple première page, utiliser un design system existant sans le modifier, faire une édition locale, changer des paramètres déterministes (couleur/espacement/arrondi/densité), ou une simple consultation de référence (cela relève de `design-system-reference.md`).

---

## Workflow

### 1. Déterminer le mode
Classer en Import / Extraction / Persistence ; en cas de concurrence, suivre la demande explicite.

---

### 2. Extraire l'intention de design (pas seulement l'apparence)

Expliquer pourquoi le design emploie chaque motif, pas seulement ce qu'il montre.

Faible : `Boutons bleus, cartes arrondies.`
Bon : `Le bleu est réservé aux actions principales et aux états de progression, donnant à l'interface un chemin clair ; l'arrondi adoucit une mise en page à dominante technique et rend l'information dense plus accessible.`

Préciser : ce que chaque choix visuel communique, ce qui est structurel vs décoratif, comment l'étendre aux pages futures, quels éléments sont au cœur du style, ce qui ne doit pas être galvaudé.

### 3. Séparer règles stables et choix ponctuels

Un bon design system ne conserve pas chaque détail aveuglément. Répartir les décisions en : **règles cardinales** (à répéter partout), **motifs optionnels** (utiles mais pas obligatoires), **détails ponctuels** (propres au produit courant), **à éviter** (à ne pas répéter).

Exemple :
```text
Règle cardinale : années/rôles/statuts des projets en étiquettes de métadonnées monospace compactes.
Motif optionnel : quand les projets sont nombreux, la liste offre une vignette au survol.
Détail ponctuel : le numéro de projet animé surdimensionné n'appartient qu'au hero de l'accueil.
À éviter : ne pas coller des étiquettes système aléatoires sur des pages sans rapport.
```

### 4. Produire ou mettre à jour le DESIGN.md

Si l'utilisateur a fourni un `DESIGN.md` → mettre à jour/normaliser, jamais remplacer en bloc ; si extraction d'un produit → en produire un nouveau ; si persistance du design courant → produire une sortie réutilisable via `design-system-reference.md`. Concis mais suffisant pour guider les générations futures — pas une bible du design monumentale.

---

# Structure du DESIGN.md

Par défaut, la structure en 9 sections ci-dessous. Dans chaque section, des **règles pratiques + le pourquoi** (pas seulement des valeurs) ; conserver les valeurs exactes, marquer clairement les inférences.

**1. Visual Theme & Atmosphere** — le tempérament d'ensemble : émotion, raffinement, densité, température visuelle, personnalité, audience, la sensation des 2 premières secondes. **Ancrer le thème sur un référent concret, pas une cascade d'adjectifs** — « moderne/propre/premium/crédible » ne spécifie rien : le modèle ne produira que la moyenne tiède de ces mots ; un adjectif décrit une « zone », un référent concret (un type d'objet/scène/d'époque, ex. « les polycopiés de cours d'une vieille université, années 1970 ») décrit un « point » : une phrase entraîne couleurs/typographie/blancs/présence ou absence d'ornement, et dit aussi ce que ce n'est pas. Si un adjectif s'impose, définir son sens précis dans ce système.

**2. Color Palette & Roles** — enregistrer les couleurs par **rôle** et non en liste, préciser où chacune sert et lesquelles ne pas galvauder, insister sur la retenue de l'accent ; sans valeur visible, ne rien inventer, marquer les inférences :
```md
### Core Palette
- Background `#F7F3EA` — fond éditorial à dominante chaude, fond de page.
- Text Primary `#171717` — corps et titres à fort contraste.
- Text Muted `#73706A` — métadonnées, légendes, détails secondaires.
- Accent `#D94F30` — réservé au CTA principal, aux états actifs, un point fort par bloc.
- Border `rgba(23,23,23,0.14)` — structure fine, sans lourdes boîtes.
```

**3. Typography Rules** — familles + **système hiérarchique sémantique** (la plupart des systèmes : 9–15 niveaux, nommés sémantiquement headline/display/body/label/caption, chaque famille pouvant se décliner en small/medium/large), corps/graisse/interligne de chaque niveau, l'amplitude hiérarchique (retenue : titre ≈ 1,9× le corps, pas 5×), le mélange chinois-latin-chiffres.

**4. Layout & Elevation (mise en page et profondeur)** — grille/zone de composition, rythme des espacements, stratégie des blancs, structure de la zone de contenu, logique d'alignement (structure, pas décoration). **Et préciser « comment la hiérarchie/la profondeur s'exprime »** : si ombres il y a, définir les règles d'ombre ; un design plat doit expliciter ses substituts (bordures / contraste de couleur / stratification tonale, ex. fond en teinte claire, contenu principal en cartes blanc pur) — la façon de communiquer la hiérarchie est une décision cardinale, à ne jamais omettre.

**5. Component & Shape (composants et formes)** — **langage des formes** : le caractère général (anguleux / doux) et la stratégie d'arrondi unifiée (ex. tous les éléments interactifs à 4px, « modernité retenue »). **Morphologie des composants** : arrondis, bordures, ombres, paddings des composants clés (cartes/boutons/étiquettes/champs), **avec une couverture particulière des variantes d'état** (primary/secondary, hover/pressed/active, vide/erreur/désactivé) — la couverture des états est la clé d'un design system : ne pas dessiner seulement l'état par défaut.

**6. Interaction & Motion** — caractère de l'animation, conventions d'entrée/hover/transition, toujours avec reduced-motion, distinguer interactions cardinales et effets ponctuels.

**7. Responsive Behavior** — points de rupture, réorganisation mobile, confort tactile, lisibilité par viewport.

**8. Do's and Don'ts** — des règles concrètes. **Attention : des Don'ts longs et bavards signalent souvent un thème trop flou (un référent assez précis embarque déjà la plupart des contraintes négatives) ; le meilleur combo, c'est un référent précis + un Do/Don't assumé.**
```text
Do : les œuvres comme preuve principale ; hiérarchie forte ; étiquettes de métadonnées retenues et cohérentes ; accent limité en nombre ; une idée structurelle/interactive mémorable ; réutiliser les valeurs exactes quand elles existent.
Don't : faux témoignages/faux indicateurs/faux logos ; blocs génériques de remplissage ; recopie de marqueurs de marque/UI propriétaires ; dégradés décoratifs sans but/emoji ; chaque bloc qui crie pareil ; liens morts/clics inertes dans un livrable ; ériger un effet hero ponctuel en règle générale.
```

**9. Agent Prompt Guide** — des instructions de génération directement actionnables pour l'agent futur :
```md
Pour générer une nouvelle page dans ce système : partir de la structure œuvres d'abord ; rôles/années/catégories en étiquettes compactes ; l'accent réservé aux actions principales et aux états actifs ; montrer de vraies œuvres au plus tôt, pas de longue bio d'entrée ; un geste structurel audacieux, le reste des blocs au calme ; sauf demande contraire, éviter la grille de cartes générique ; conserver responsive et confort tactile.
```

---


## Lightweight Tokens

Si utile, inclure une section de tokens compacte.

À n'utiliser que si les valeurs sont disponibles ou inférables de façon responsable.

Exemple :

```json
{
  "color": {
    "background": "#F7F3EA",
    "surface": "#FFFFFF",
    "textPrimary": "#171717",
    "textMuted": "#73706A",
    "accent": "#D94F30",
    "border": "rgba(23, 23, 23, 0.14)"
  },
  "radius": {
    "sm": "6px",
    "md": "12px",
    "lg": "24px"
  },
  "spacing": {
    "base": "8px",
    "section": "96px"
  },
  "typography": {
    "bodySize": "16px",
    "bodyLineHeight": "1.5",
    "labelSize": "11px"
  }
}
```

Pas de fausse précision. Si des valeurs sont inférées, le dire.

---

## Compléments par mode (à éviter)

Les comportements cardinaux des trois modes sont donnés plus haut. Pour chaque mode :
- **Extraction** : ne pas déverser le CSS brut dans le DESIGN.md, ne pas inventer de valeurs absentes, ne pas prendre un détail ponctuel pour une règle système, ne pas oublier responsive/interactions.
- **Persistence** : ne pas sur-ajuster à la page courante, ne pas prendre du contenu de remplissage pour une règle, ne pas figer une expérimentation temporaire en système permanent, ne pas ignorer les décisions de style déjà validées par l'utilisateur.
- **Import** : la sortie peut être une version mise à jour/normalisée, une analyse de lacunes + suggestions, ou une note de compatibilité ; ne supprimer les règles de l'utilisateur qu'en cas de conflit ou de doublon.

## Quality Rules

Un bon `DESIGN.md` : réutilisable, précis, enraciné dans le matériau source, aussi concis qu'utile, distinguant le cardinal de l'optionnel, sûr vis-à-vis de la PI, utile aux générations futures. **À éviter** : les généralités design, les formules vides premium/moderne/épuré, de la théorie sans règles actionnables, la copie de systèmes de marque propriétaires, ériger un détail d'un produit en règle générale, inventer des tokens que la source ne justifie pas.

## IP and Brand Safety

Si la source est une inspiration de marque publique : ne pas présenter la sortie comme un système officiel, ne pas copier logo/éléments/structure de page exacte/UI propriétaire, ne décrire que des traits visuels de haut niveau, produire des règles réutilisables orientées création originale. Si la source appartient à l'utilisateur : ce qui est fourni explicitement fait autorité ; conserver les valeurs exactes ; marquer les hypothèses aux endroits incomplets.

## Chinese Typography Reference

Quand le produit comporte beaucoup de chinois/CJK, de la mise en page éditoriale chinoise, des comptes officiels WeChat, Xiaohongshu, un deck chinois, des libellés UI chinois ou un HTML façon impression : utiliser `horizontal-craft/chinese-typography.md` ; traduire les méthodes d'imprimerie en structure HTML : zone de composition, grille, blancs, groupe de titres, images, notes marginales, rythme des chapitres et ponctuation.

## Quality Gate

Avant livraison, appliquer `quality-gate.md` ; ce scénario peut durcir les contrôles, jamais les affaiblir.

## Handoff

Le `DESIGN.md` généré/importé/normalisé/mis à jour transite par `skills/design/design-system-reference.md` pour la réutilisation future : une référence réutilisable, pas un résumé jetable. Le cas échéant, consigner : produit/gabarit/capture source, style skill/inspiration de marque retenu, date et version, hypothèses, informations manquantes.
