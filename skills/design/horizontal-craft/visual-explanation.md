---
name: Visual Explanation Craft
description: Règles de conception pour les diagrammes, graphiques, explications visuelles, modèles explorables et infographies. Choisissez la représentation à partir de la forme de l'information ; l'interaction doit améliorer la compréhension.
mode: reference
platform: any
scenario: visual-explanation
preview:
  type: none
default_for:
  - diagram
  - chart
  - data visualization
  - visual explanation
  - explorable model
  - interactive report
  - flowchart
  - architecture diagram
  - system map
  - process map
  - user journey map
  - data flow diagram
  - timeline
  - comparison graphic
  - information graphic
  - visual explanation
  - infographic
  - interactive explanation
  - flowchart
  - architecture diagram
  - system relationship diagram
  - business process diagram
  - user journey map
  - data flow diagram
  - timeline
fidelity: system
---

# Visual Explanation Craft

Utilisez ce fichier lorsqu'un artefact contient un **diagramme, graphique, explication visuelle, explication interactive, chronologie, carte, graphe de relations, matrice de comparaison, modèle explorable ou infographie/data**.

Ce n'est pas un préréglage de style et ce n'est pas un guide de bibliothèque de graphiques. Il décide **quelle forme visuelle l'information mérite**. Utilisez `horizontal-craft/technique-library.md` seulement après que le choix de représentation nécessite une technique d'implémentation spécifique.

## Core Principle

Choisissez la représentation à partir de la forme de l'information, et non à partir de l'habitude visuelle.

Chaque explication visuelle doit répondre à l'une de ces questions :

```text
Quelle est la structure ?
Qu'est-ce qui a changé avec le temps ?
Qu'est-ce qui cause quoi ?
Qu'est-ce qui est plus grand / plus petit / meilleur / pire ?
Où est-ce ?
Comment le processus se déplace-t-il ?
Que se passe-t-il si je change cette entrée ?
Que le lecteur devrait-il comparer ou décider ?
```

Si un graphique, diagramme, animation ou interaction ne change pas ce que l'utilisateur peut comprendre, décider ou faire, supprimez-le.

---

## Information Shape → Representation

| Information shape | Preferred representation | Avoid |
|---|---|---|
| Hierarchy / taxonomy | tree, nested cards, layered outline, collapsible hierarchy | force-fitting into a timeline |
| Process / workflow | flowchart, stepper, pipeline, state machine | disconnected numbered cards |
| Time / evolution | timeline, sequence strip, trend chart | unordered bullet grid |
| Comparison / trade-off | matrix, side-by-side, before/after, toggle compare | decorative radar charts with unclear axes |
| Quantity / metric | chart, KPI group, ranking, distribution, small multiples | chart without units, labels, or conclusion |
| Relationship / network | node-link, adjacency list, map of dependencies | dense spaghetti graph |
| System inventory / architecture | layered architecture map, responsibility map, component relationship diagram | pretending architecture is a time sequence |
| Geography / spatial relation | map, route, region block, schematic geography | fake map when real geography matters |
| Argument / evidence chain | claim → evidence → implication layout | pile of quotes or stats without logic |
| Explorable model | input controls that update output or explanation | sliders that only animate decoration |
| Collection / resource set | filterable grid/list, facets, search, detail drawer | endless undifferentiated cards |

Utilisez la représentation la plus simple qui rend l'information plus claire.

---

## Interaction Must Earn Its Place

Utilisez l'interaction seulement lorsqu'elle crée l'une de ces valeurs :

```text
reveal detail on demand
filter to a relevant subset
compare alternatives
advance through a sequence
change an input and see the result
highlight a relationship
reduce cognitive load by progressive disclosure
```

L'interaction échoue si :

```text
it only creates motion;
it hides essential information;
it makes the user click just to read basics;
it has no visible output change;
it has fake controls or placeholder handlers;
it is worse than a static chart or table.
```

Chaque contrôle interactif doit avoir un état visible, un accès au clavier et un résultat clair.

---

## Chart and Data Explanation Rules

Pour les graphiques, utilisez `horizontal-craft/data-integrity.md` avec ce fichier.

Un graphique doit avoir :

```text
clear title that states the insight or question;
visible units and labels;
honest scale and axis treatment;
legend only when needed;
source/provenance or visible demo-data label;
one main reading path.
```

N'utilisez pas :

```text
3D charts for normal data;
decorative charts with unreadable labels;
truncated axes that exaggerate difference without disclosure;
precise-looking fake data;
multiple chart types when one table would be clearer.
```

Pour les petits graphiques dans des cartes, des présentations ou sur des mobiles, préférez moins de points de données et des étiquettes plus grandes plutôt que la complétion visuelle.

---

## Standalone Diagram Mode

Utilisez ce mode lorsque la demande finale de l'utilisateur est un organigramme, un diagramme d'architecture, une carte système, un diagramme de processus métier, une carte de parcours utilisateur, un diagramme de dépendances ou un diagramme de flux de données.

Un diagramme autonome peut être statique. N'ajoutez pas de filtres, d'états au survol ou d'animations simplement pour le rendre interactif. L'interaction n'est utile que lorsqu'elle révèle des détails, change de couches, compare des variantes ou réduit le encombrement.

Avant de dessiner, choisissez une seule histoire de diagramme :

```text
execution flow      → what happens first, next, last
system inventory    → what parts exist and how they relate
responsibility map  → who/what owns each step or component
data flow           → where data enters, transforms, and exits
dependency map      → what depends on what
journey map         → what the user/actor experiences over time
```

N' mélangez pas d'histoires incompatibles dans un seul diagramme. Si la demande combine un inventaire système et une séquence d'exécution, divisez en deux diagrammes ou en couches séparées.

Complexité par défaut :

```text
4–8 primary nodes
one dominant reading path
at most two secondary branches
one clear reading direction: left-to-right, top-to-bottom, radial, or loop
no unlabeled spaghetti connectors
```

Les types de nœuds doivent avoir un sens :

```text
step · decision · data · external system · actor · component · annotation
```

Les types de relations doivent avoir un sens :

```text
main pipeline · optional branch · feedback loop · async signal · dependency · ownership · data movement
```

Règles de connecteur :

- edge labels sit near the relationship, not on top of the line;
- arrows should not cross through nodes;
- line style encodes meaning, not decoration;
- avoid unnecessary connector colors;
- if labels or arrows need long explanation, simplify the diagram.

Échouez un diagramme autonome s'il nécessite un long texte pour être compris, si les nœuds sont trop petits pour être lus, si chaque connecteur semble également important, ou si la structure système et le timing d'exécution sont confondus.

---

## Diagram Rules

### Flowcharts and Process Diagrams

- One node = one step, state, decision, actor, component, or data object — but do not mix these meanings without visual distinction.
- Keep primary flow visually dominant.
- Branches must be labeled by trigger or condition.
- Do not let arrows cross casually; if arrows cross, simplify the graph.
- For user journeys, label the user action between states.
- For system diagrams, label data/object movement between nodes.
- For architecture diagrams, separate layers or groups before drawing arrows; boxes alone are not architecture.

### Timelines

- Use time only when order or duration matters.
- Make scale explicit: chronological, phase-based, or milestone-based.
- Do not mix exact dates and vague phases without visual distinction.
- Long timelines need grouping or zoom/filter.

### Hierarchies

- Use indentation, nesting, or containment consistently.
- Parent/child relations must be obvious without reading all text.
- Avoid more than 3 visible hierarchy levels on a small canvas unless expandable.

### Comparisons

- Compare like with like.
- Keep dimensions aligned across columns or rows.
- If one side has extra criteria, explain why.
- Difference must be visible before decorative styling.

### Maps and Spatial Views

- Use a real map when geography matters.
- Use a schematic map when only relationship, route, or grouping matters.
- Do not use live map widgets for exported images unless the final export captures a stable state.

---

## Carrier-Native Behavior

The visual explanation must feel native to its final carrier.

```text
info-interactive → explorable page or standalone visual explanation, not a product demo
web-tool → controls update the result, not just decoration
prototype → diagram explains product flow, not a marketing infographic
social-card → readable image, not a shrunk webpage
standalone diagram → clear SVG/HTML diagram, not a full report page
landing-page → visual proof supports conversion, not a full report
slide/deck → one idea per slide, not a dense dashboard screenshot
```

If the carrier is fixed image, prioritize readability at export scale. If the carrier is interactive HTML, prioritize progressive exploration and accessible state changes.

---

## Implementation Guidance

Choose implementation after choosing representation.

```text
simple static chart / diagram → inline SVG or semantic HTML/CSS
simple interaction → vanilla JS + SVG/HTML state updates
complex custom data viz → D3 or canvas only when needed
standard charts → chart library only when supported and appropriate
3D / shader / WebGL → almost never for explanation; use only when spatial/physical meaning matters
```

Default to stable HTML/SVG. Do not escalate to advanced libraries for novelty.

---

## Accessibility and Resilience

- Provide text alternatives or visible summaries for charts/diagrams.
- Do not rely on color alone; use labels, shapes, patterns, or position.
- Ensure controls are keyboard reachable.
- Preserve focus-visible styling.
- Support reduced motion when animation exists.
- Keep labels readable at the target viewport/export size.
- If data is missing, say so; do not invent a complete visualization.

---

## Failure Cases

Fail the visual explanation if:

```text
[ ] representation does not match the information shape
[ ] interaction does not change understanding, decision, or task outcome
[ ] chart lacks labels, units, scale, or conclusion
[ ] diagram arrows/nodes are visually confusing
[ ] standalone diagram mixes incompatible stories such as architecture inventory and execution sequence
[ ] connectors lack semantic meaning or labels
[ ] visual form looks impressive but explains less than text would
[ ] controls are fake, hidden, or inaccessible
[ ] data/proof is invented or not marked as demo/sample
[ ] labels are too small for the final carrier
[ ] carrier mismatch: image behaves like a webpage, deck behaves like a report, tool behaves like an infographic
```

Fix by simplifying the representation before adding more decoration.

</DOCUMENT>
