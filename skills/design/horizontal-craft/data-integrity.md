---
name: data-integrity
description: Règles d'intégrité pour les marqueurs de données, graphiques, tableaux, métriques et données de démonstration pour les artefacts de conception modifiables.
mode: reference
platform: web
scenario: horizontal-craft
preview:
  type: none
default_for:
  - marqueurs de données
  - graphiques
  - métriques
  - tableaux
  - données de tableau de bord
  - données de démonstration
  - artefact modifiable
fidelity: system
---

# Intégrité des données

Utilisez ce fichier lorsqu'un artefact contient des données, des métriques, des graphiques, des tableaux, des nombres à prétention probante, ou a besoin d'être modifié ultérieurement.

Règle de base :

```text
Un artefact de conception peut utiliser des données de démonstration, mais il ne doit jamais dissimuler des données de démonstration comme de véritables preuves.
```

---

## Marqueurs de données

Les marqueurs de données préservent la modifiabilité et le ciblage ultérieur des commentaires.

Utilisez le squelette d'artefact :

```text
portfolio        → data-portfolio / data-section / data-project / data-component
présentation     → data-deck / data-slide / data-component
prototype        → data-prototype / data-screen / data-section / data-component / data-state
page de contenu  → data-content-page / data-mode / data-section / data-component
page d'atterrissage → data-landing-page / data-section / data-component
outil web        → data-web-tool / data-tool-type / data-screen / data-component / data-state
```

Si un marqueur serait excessif pour une petite modification, préservez les marqueurs existants et ajoutez le minimum de marqueurs manquants autour des régions modifiées.

---

## Métriques et données de démonstration

Les nombres spécifiques doivent être l'un des suivants :

```text
fourni par l'utilisateur
sourced
demo-labeled
placeholder
```

N'inventez pas de preuves impressionnantes pour améliorer une conception.

N'inventez jamais :

- revenus
- taille du marché
- nombre d'utilisateurs
- taux de croissance
- taux de conversion
- rétention / désabonnement
- scores de satisfaction
- classements
- disponibilité
- victoires de référence
- nombre de clients

Si le nombre est illustratif, étiquetez-le comme démonstration.

Exemple :

```html
<span data-proof="demo">92% démo</span>
<p class="data-note">Données de démonstration — remplacez par des chiffres vérifiés avant publication.</p>
```

---

## Graphiques

Les graphiques doivent communiquer une affirmation, pas décorer une carte.

Requis :

- titre ou conclusion
- axes ou étiquettes lorsque quantitatifs
- unités
- source / étiquette de démonstration lorsque les données ne sont pas fournies par l'utilisateur
- valeurs lisibles
- contraste qui survive sur petits écrans

Évitez :

- fausses lignes de tendance sans signification de données
- décoration de sparkline non étiquetée
- précision impossible
- lignes de croissance aléatoires ascendantes
- couleurs de graphique sans légende ou signification d'état

---

## Tableaux

Les tableaux doivent optimiser le balayage.

Règles :

- colonnes numériques alignées de manière cohérente
- étiquettes de statut utilisent un vocabulaire cohérent
- filtres/recherche/tri apparaissent lorsque le tableau implique des opérations
- long texte a une stratégie de retour à la ligne ou de troncature
- états vides et d'erreur existent
- actions de ligne sont proches des lignes
- unités apparaissent dans l'en-tête ou les valeurs, pas aléatoirement

---

## Copie des données

Préférez les étiquettes honnêtes :

- Données de démonstration
- Données d'exemple (shìlì shùjù)
- À remplir (dài tiánxiē)
- Remplacer par des chiffres vérifiés
- Source en attente

Évitez de prétendre :

- fait confiance à 10 000+ équipes
- 99.9% de disponibilité
- plateforme n°1
- leader du secteur
- vérifié par des experts

---

## Contrôles qualité

```text
[ ] Les marqueurs de données requis sont présents.
[ ] Les nombres à prétention probante ont une provenance.
[ ] Les données de démonstration sont étiquetées visiblement.
[ ] Les graphiques ont des étiquettes, des unités et une conclusion.
[ ] Les tableaux sont alignés, balayables et ont des états.
[ ] Aucune métrique impressionnante inventée n'existe.
[ ] De fausses logos de clients, citations, récompenses et affirmations de presse sont absentes.
```
