---
name: quality-gate
description: Porte de livraison finale bloquante pour les artefacts générés ou édités de manière majeure. Un noyau de blocage court (doit être passé à chaque fois) plus des vérifications détaillées à la demande (seulement les pertinentes) et un polissage non bloquant. Exécuté comme une checklist, pas comme une référence passive. Déclenché par "contrôle qualité", "contrôle de livraison", "delivery check", "design QA", "compliance check", ou chaque fois qu'un artefact est sur le point d'être transmis.
mode: quality-gate
platform: any
scenario: delivery-quality
preview:
  type: none
default_for:
  - quality gate
  - design QA
  - delivery check
  - compliance check
  - Contrôle de livraison
  - Contrôle qualité
fidelity: system
---

# Quality Gate

Exécuté **après** qu'un artefact est généré ou édité de manière substantielle, **avant** la livraison. Ce fichier ne vérifie que les bonnes règles ont été réellement appliquées et sont visibles dans la sortie — les règles elles-mêmes résident dans les compétences de l'artefact et `horizontal-craft/*.md`.

```text
Brief → Artifact Skill → Template / Design System / Craft → Artifact → [Quality Gate] → Delivery
```

Si une vérification échoue, corrigez le **plus petit** problème ayant échoué. Ne rediseignez pas l'ensemble de l'artefact à moins que l'utilisateur ne vous le demande.

Cette porte comporte trois niveaux — exécutez-les dans l'ordre :

1. **Noyau de blocage** — une courte liste obligatoire à passer. Exécuté **chaque** fois, à chaque livraison, à chaque tour. Si vous ne faites rien d'autre, faites celui-ci.
2. **Vérifications à la demande** — vérifications détaillées qui s'appliquent **uniquement lorsque l'artefact a l'élément pertinent** (formulaires, graphiques, modèles, animations…). Ignorez ceux qui ne s'appliquent pas.
3. **Polissage non bloquant** — notez dans le résumé ; ne bloquez jamais sur ces points.

---

## NIVEAU 1 — Noyau de blocage (doit passer, à chaque fois)

Il s'agit d'échecs de niveau **incident** : l'artefact atteint l'utilisateur cassé, hors-cible, malhonnête ou visivement bon marché. Vérifiez tous ces points à chaque livraison — cette liste est courte intentionnellement pour qu'elle soit réellement exécutée.

```text
[ ] 1. Bon type de support / bon format d'artefact — correspond à ce que l'utilisateur a demandé
       (une affiche livrée comme une page défilante, ou un brief produit traité comme une page de destination, échoue). [§A]
[ ] 2. Pertinent par rapport au brief — résout visiblement la demande réelle, pas une réponse faussement polie. [§A]
[ ] 3. Aucun lien mort / aucun faux JS dans un artefact prêt à être publié —
       pas de href="#" / javascript:void(0) sauf s'ils sont visiblement marqués comme des espaces réservés ; pas d'alert('todo'),
       de gestionnaire TODO, ou d'« interaction » uniquement pour la console ; chaque CTA a une destination réelle ou un état d'attente visible. [§B]
[ ] 4. Vérité et intégrité du contenu —
       le contenu provient d'une lecture réelle de la source : il ne fabrique pas ce qui n'existe pas
       (données factices, projets/travaux factices, logos/témoignages/récompenses/metrics/presse factices),
       NI omet ou dilue ce qui EXISTE (pour les tâches basées sur une source, la substance de chaque projet/section réel
       est effectivement extraite et affichée — pas laissée comme un remplissage vague ou un espace réservé mince).
       Profondeur plutôt que quantité : le test est « a-t-il fidèlement représenté la source », pas « y a-t-il plus de texte ». [§B]
[ ] 5. Les polices chinoises se chargent réellement — pour le contenu chinois, chaque police nommée est réellement chargée
       (<link> ou @font-face) et font-family contient une police CJK ; elle ne DOIT PAS tomber directement sur system-ui. [§C]
[ ] 6. Les artefacts interactifs ont un comportement réel — les contrôles sont cliquables et font quelque chose de réel ;
       les états pertinents (chargement / vide / erreur / succès / peuplé) existent ; pas d'interaction uniquement des espaces réservés. [§D]
[ ] 7. Anti-AI-slop (section entière, bloquante — c'est ce qui affecte le plus la qualité visuelle) —
       pas d'emoji décoratifs comme icônes/puces ; pas de dégradé bleu-violet par défaut comme système visuel ;
       pas de fausse preuve (logos/témoignages/récompenses/classements/presse/metrics présentés comme réels) ;
       pas de grille de remplissage de cartes de fonctionnalités (vague 3-up/4-up) ; pas de « héros + trois cartes + CTA » générique
       sans idée spécifique au contenu ; pas de preuve par photo de stock / appareil flottant / fausse maquette ;
       pas de clichés d'IA chinoise (chinese AI-cliché) ; pas de taches/orbes décoratives pour remplir l'espace ;
       famille d'icônes cohérente (pas de mélange emoji/icone) ; pas de visualisation ou d'interaction ajoutée
       uniquement paraître avancée. [§E]
[ ] 8. Marqueurs d'éditabilité — sections / diapositives / écrans / composants / états sont individuellement
       identifiables ; des ancres structurelles stables existent (HTML sémantique, sections nommées, ou commentaires de région sélectionnée) ;
       pas de blocs générés opaques qui bloquent les éditions locales ; le contenu d'espace réservé est étiqueté. [§F]
```

Si un élément de blocage échoue, corrigez-le avant livraison. Corrigez l'échec spécifique — ne rediseignez pas par défaut.

---

## NIVEAU 2 — Vérifications à la demande (uniquement pertinentes)

Exécutez une vérification ci-dessous **uniquement si l'artefact contient réellement cet élément**. N'exécutez pas une vérification de formulaires sur une page sans formulaires. Ces vérifications approfondissent le noyau de blocage ; c'est là que vous confirmez que le savoir-faire a vraiment été appliqué.

### À la demande : quel horizontal-craft vérifier

Pour le savoir-faire qui s'applique réellement, ouvrez ce fichier et confirmez que ses règles sont visiblement appliquées. Ne chargez pas les fichiers qui ne s'appliquent pas.

| Uniquement si l'artefact a… | Vérifier contre |
|---|---|
| **(toujours, passage final)** le noyau anti-slop ci-dessus | `horizontal-craft/anti-ai-slop.md` (fichier complet, pour la vérification de blocage §E) |
| Texte chinois substantiel / titres/couverts menés par la typographie | `horizontal-craft/chinese-typography.md` (+ `reference/fonts.md` quand le choix de police est important) |
| Graphiques, diagrammes, chronologies, cartes, modèles explorables | `horizontal-craft/visual-explanation.md` |
| Icônes UI / pictogrammes / boutons avec icône | `horizontal-craft/icon-system.md` |
| Formulaires / entrées / validation | `horizontal-craft/form-validation.md` |
| États interactifs / tableaux de bord / outils / prototypes | `horizontal-craft/state-coverage.md` |
| Metrics / graphiques / tableaux / données de démonstration / affirmations | `horizontal-craft/data-integrity.md` |
| CTAs / liens / preuves / citations / logos | `horizontal-craft/link-and-proof.md` |
| Direction de couleur peu claire / pas de système de design | `horizontal-craft/color.md` |
| Animation / transitions / graphiques animés | `horizontal-craft/animation-discipline.md` |
| Tarification / intégration / tableaux de bord / H5 / flux de conversion | `horizontal-craft/laws-of-ux.md` |
| Effets avancés au-delà du CSS/SVG standard | `horizontal-craft/technique-library.md` |

### À la demande : Adaptation de modèle — uniquement si un modèle/graine a été utilisé

```text
[ ] les instructions markdown / SKILL.md ont été traitées comme primaires sur pattern.html
[ ] pattern.html n'a pas été copié en bloc ; la sortie n'est pas un re-skinage superficiel de texte/couleur
[ ] le texte d'espace réservé / les faux actifs sont remplacés ou étiquetés ; les sections inutilisées sont supprimées, pas remplies de contenu factice
[ ] la structure de modèle sert la compétence d'artefact actuelle et l'objectif de l'utilisateur
```

### À la demande : Système de design / cohérence visuelle — uniquement si un système/référence s'applique ou si la cohérence visuelle est à risque

```text
[ ] typographie, couleur, espacement, rayon, ombres, composants partagent un langage visuel
[ ] la couleur d'accent a un rôle et n'est pas trop utilisée ; aucun système de style non lié n'est mélangé par accident
[ ] les contraintes système ne remplacent pas l'utilisabilité ou l'adéquation au support
```

### À la demande : Détail d'interaction & d'état — uniquement pour les artefacts interactifs (au-delà du blocage #6)

```text
[ ] la validation de formulaire préserve la saisie et explique la récupération
[ ] les actions dangereuses ont confirmation / annulation / prévention d'effacement
[ ] le comportement clavier et focus est utilisable
```
Référence : `horizontal-craft/state-coverage.md`, `horizontal-craft/form-validation.md`.

### À la demande : Explication visuelle — uniquement si des graphiques / diagrammes / chronologies / cartes / modèles explorables existent

```text
[ ] la représentation correspond à la forme de l'information ; a un objectif de compréhension clair
[ ] l'interaction change ce que l'utilisateur peut comprendre/comparer/filtrer/décider (pas de contrôles purement décoratifs ou de filtres factices)
[ ] les graphiques ont des étiquettes lisibles, unités, échelles, conclusions ; les diagrammes ont des nœuds lisibles, des flèches claires, des branches étiquetées
[ ] les étiquettes restent lisibles à l'échelle de vue/export cible
[ ] cela explique PLUS qu'un paragraphe ou tableau clair ne le ferait (sinon, simplifier)
```
Référence : `horizontal-craft/visual-explanation.md`.

### À la demande : Accessibilité — vérifier quand cela compte ; PAS bloquant pour les artefacts marketing/d'affichage

Les artefacts de design sont principalement marketing/d'affichage, donc l'accessibilité **n'est pas** une porte de blocage ici. Appliquez-la lorsque l'artefact est un outil interactif réel, un formulaire, ou lorsque l'utilisateur/la marque exige la conformité. Même alors, seuls deux éléments tendent vers « devrait vraiment être corrigé » : **contraste sévéré qui nuit à la lisibilité**, et **contrôles uniquement avec icônes sans nom accessible** (ceux-ci affectent l'utilisabilité réelle). Le reste ci-dessous est une bonne pratique, noté mais non bloquant.

```text
[ ] contraste texte + non-texte suffisant
[ ] focus-visible existe ; les éléments interactifs sont accessibles au clavier
[ ] les boutons/liens utilisent la sémantique correcte ; les entrées ont des étiquettes ; les contrôles uniquement avec icônes ont des noms accessibles
[ ] les icônes décoratives aria-hidden ; les informations du graphique ne sont pas transmises uniquement par la couleur
[ ] repli en cas de réduction du mouvement quand le mouvement existe
```
Référence : `horizontal-craft/accessibility.md`.

---

## NIVEAU 3 — Polissage non bloquant

Notez dans le résumé de livraison ; ne bloquez pas sauf cas graves. Ne sur-polissez pas en ajoutant de la décoration — réparez d'abord la structure, la hiérarchie, le contenu, les preuves, l'interaction et la représentation.

```text
[ ] le rythme visuel pourrait être plus distinctif
[ ] une section semble générique
[ ] l'animation pourrait être plus intentionnelle
[ ] un graphique pourrait être simplifié davantage
[ ] le système de design pourrait être rendu plus explicite
```

---

## Références de section (pour le noyau de blocage)

Les éléments de blocage ci-dessus pointent vers ces courtes clarifications :

- **§A Brief & support** — le type d'artefact correspond à la demande ; public/cas d'utilisation visible ; langue correspondante ; surface de sortie correspondant à la plateforme ; contraintes majeures respectées ; le support se comporte comme son genre (landing = conversion à sujet unique ; portfolio = hiérarchie travail/identité + détail projet ; prototype = états atteignables + interaction réelle ; content-page = lecture linéaire ; info-interactive = information explorables, pas une démo produit ; web-tool = saisie→logique→résultat ; social-card = canevas fixe, un rôle ; deck = une idée par diapositive).
- **§B Vérité & intégrité** — honnêté vérifiable (liens, données, étiquettes de démo) ET représentation fidèle et complète du contenu source réel. Ne fabriquez pas ; omettez pas. Données de démo/échantillon étiquetées ; nombres sources ou adoucis.
- **§C Typographie chinoise** — polices nommées réellement chargées ; police CJK dans la pile ; ne tombe jamais sur un repli non contrôlé. (Règles complètes : `chinese-typography.md`.)
- **§D Interaction** — comportement réel, pas de JS d'espace réservé, états pertinents présents. (Règles complètes : `state-coverage.md`.)
- **§E Anti-AI-slop** — toute la liste anti-AI-slop est bloquante car c'est ce qui affecte le plus la qualité visuelle. (Règles complètes : `anti-ai-slop.md`.)
- **§F Editabilité** — sections/composants identifiables, ancres stables, pas de blocs opaques, espaces réservés étiquetés — afin que l'utilisateur puisse éditer localement et itérer.

---

## Livraison (la porte tourne en interne, ne pas réciter la liste à l'utilisateur)

La porte de qualité est une **action interne** — exécutez-la, mais **ne rapportez pas la checklist point par point à l'utilisateur** (ne sortez pas de tableaux pass/fail, ne listez pas « ① type d'artefact pass ② pertinent pass… »). Cela est cohérent avec la discipline de sortie : l'utilisateur veut un bien fait produit, pas le processus de contrôle qualité.

- Par défaut : si la vérification passe, **livrez directement l'artefact**, sans aucune checklist / tableau récapitulatif de porte.
- Uniquement si un problème a été effectivement **corrigé**, ou s'il y a des **non-bloques que l'utilisateur devrait savoir** (comme « les images du projet sont des espaces réservés, je vous suggère de les remplacer par de vraies images »), expliquez-le avec **une phrase naturelle**, pas en lisant la checklist.
- Ne mettez JAMAIS de blocs de commentaires de conformité dans l'artefact.
