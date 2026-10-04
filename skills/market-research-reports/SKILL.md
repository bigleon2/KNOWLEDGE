---
name: market-research-reports
version: "1.0.0"
category: "Finance & Recherche"
tags:
  - market
  - research
  - reports
description: "Génère des rapports d'étude de marché complets (50+ pages) dans le style des plus grands cabinets de conseil (McKinsey, BCG, Gartner). Inclut une mise en forme LaTeX professionnelle, une génération visuelle étendue avec scientific-schematics et generate-image, une intégration approfondie avec research-lookup pour la collecte de données, et une analyse stratégique multi-frameworks incluant les cinq forces de Porter, PESTLE, SWOT, TAM/SAM/SOM et la matrice BCG."
allowed-tools: [Read, Write, Edit, Bash]
language: fr

read_when:
  - Déclencher quand la demande concerne : "Génère des rapports d'étude de marché complets (50+ pages) dans le style des plus grands cabinets de conseil…
  - Déclencher si la demande mentionne : génère, rapports, étude
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Market Research Reports

## Vue d'ensemble

Les rapports d'étude de marché sont des documents stratégiques complets qui analysent les industries, les marchés et les paysages concurrentiels pour éclairer les décisions d'entreprise, les stratégies d'investissement et la planification stratégique. Ce skill génère des **rapports de qualité professionnelle de 50+ pages** avec un contenu visuel riche, sur le modèle des livrables des grands cabinets comme McKinsey, BCG, Bain, Gartner et Forrester.

**Caractéristiques clés :**
- **Longueur complète** : rapports conçus pour 50+ pages, sans contrainte de tokens
- **Contenu visuel riche** : 5-6 diagrammes clés générés au départ (d'autres ajoutés selon les besoins pendant la rédaction)
- **Analyse orientée données** : intégration approfondie avec research-lookup pour les données de marché
- **Approche multi-frameworks** : cinq forces de Porter, PESTLE, SWOT, matrice BCG, TAM/SAM/SOM
- **Mise en forme professionnelle** : typographie, couleurs et mise en page de qualité cabinet de conseil
- **Recommandations actionnables** : orientation stratégique avec feuilles de route de mise en œuvre

**Format de sortie :** LaTeX avec style professionnel, compilé en PDF. Utilise le package de style `market_research.sty` pour une mise en forme cohérente et professionnelle.

## Quand utiliser ce skill

Ce skill doit être utilisé pour :
- Créer des analyses de marché complètes pour des décisions d'investissement
- Élaborer des rapports sectoriels pour la planification stratégique
- Analyser les paysages concurrentiels et la dynamique de marché
- Réaliser des exercices de dimensionnement de marché (TAM/SAM/SOM)
- Évaluer des opportunités d'entrée sur un marché
- Préparer des supports de due diligence pour des opérations de M&A
- Créer du contenu d'expertise pour le positionnement sectoriel
- Élaborer la documentation d'une stratégie go-to-market
- Analyser les impacts réglementaires et politiques sur les marchés
- Construire des business cases pour le lancement de nouveaux produits

## Exigences d'enrichissement visuel

**CRITIQUE : les rapports d'étude de marché doivent inclure un contenu visuel clé.**

Chaque rapport doit générer **6 visuels essentiels** au démarrage, avec des visuels supplémentaires ajoutés selon les besoins pendant la rédaction. Commencer par les visualisations les plus critiques pour établir le cadre du rapport.

### Outils de génération visuelle

**Utiliser `scientific-schematics` pour :**
- Graphiques de trajectoire de croissance du marché
- Diagrammes TAM/SAM/SOM (cercles concentriques)
- Diagrammes des cinq forces de Porter
- Matrices de positionnement concurrentiel
- Graphiques de segmentation du marché
- Diagrammes de chaîne de valeur
- Feuilles de route technologiques
- Heatmaps de risques
- Matrices de priorisation stratégique
- Chronologies de mise en œuvre / diagrammes de Gantt
- Diagrammes d'analyse SWOT
- Matrices croissance-partage BCG

```bash
# Example: Generate a TAM/SAM/SOM diagram
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circle diagram showing Total Addressable Market $50B outer circle, Serviceable Addressable Market $15B middle circle, Serviceable Obtainable Market $3B inner circle, with labels and arrows pointing to each segment" \
  -o figures/tam_sam_som.png --doc-type report

# Example: Generate Porter's Five Forces
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: 'Threat of New Entrants' (top), 'Bargaining Power of Suppliers' (left), 'Bargaining Power of Buyers' (right), 'Threat of Substitutes' (bottom). Each box should show High/Medium/Low rating" \
  -o figures/porters_five_forces.png --doc-type report
```

**Utiliser `generate-image` pour :**
- Infographies héros de la synthèse pour la direction
- Illustrations conceptuelles d'industrie/secteur
- Visualisations technologiques abstraites
- Imagerie de page de couverture

```bash
# Example: Generate executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, showing key metrics in modern data visualization style, blue and green color scheme, clean minimalist design with icons representing market size, growth rate, and competitive landscape" \
  --output figures/executive_summary.png
```

### Visuels recommandés par section (générer selon les besoins)

| Section | Visuels prioritaires | Visuels optionnels |
|---------|-----------------|------------------|
| Synthèse pour la direction | Infographie exécutive (DÉPART) | - |
| Taille du marché et croissance | Trajectoire de croissance (DÉPART), TAM/SAM/SOM (DÉPART) | Ventilation régionale, croissance par segment |
| Paysage concurrentiel | Cinq forces de Porter (DÉPART), matrice de positionnement (DÉPART) | Graphique de parts de marché, groupes stratégiques |
| Analyse des risques | Heatmap des risques (DÉPART) | Matrice d'atténuation |
| Recommandations stratégiques | Matrice d'opportunités | Cadre de priorisation |
| Feuille de route de mise en œuvre | Chronologie/Gantt | Suivi des jalons |
| Thèse d'investissement | Projections financières | Analyse de scénarios |

**Commencer par les 6 visuels prioritaires** (marqués DÉPART ci-dessus), puis générer des visuels supplémentaires au fil de la rédaction des sections qui nécessitent un support visuel.

---

## Structure du rapport (50+ pages)

### Pages liminaires (~5 pages)

#### Page de couverture (1 page)
- Titre et sous-titre du rapport
- Visualisation héros (générée)
- Date et classification
- Préparé pour / Préparé par

#### Table des matières (1-2 pages)
- Automatisée depuis LaTeX
- Liste des figures
- Liste des tableaux

#### Synthèse pour la direction (2-3 pages)
- **Encadré Instantané du marché** : métriques clés en un coup d'œil
- **Thèse d'investissement** : synthèse en 3-5 points
- **Constats clés** : découvertes et insights majeurs
- **Recommandations stratégiques** : les 3-5 recommandations actionnables principales
- **Infographie de synthèse** : synthèse visuelle des points saillants du rapport

---

### Analyse principale (~35 pages)

#### Chapitre 1 : Vue d'ensemble et définition du marché (4-5 pages)

**Contenu requis :**
- Définition et périmètre du marché
- Cartographie de l'écosystème industriel
- Acteurs clés et leurs rôles
- Frontières et marchés adjacents
- Contexte historique et évolution

**Visuels requis (2) :**
1. Diagramme d'écosystème / chaîne de valeur du marché
2. Diagramme de structure de l'industrie

**Données clés :**
- Critères de définition du marché
- Segments inclus/exclus
- Périmètre géographique
- Horizon temporel de l'analyse

---

#### Chapitre 2 : Taille du marché et analyse de croissance (6-8 pages)

**Contenu requis :**
- Calcul du marché adressable total (TAM)
- Définition du marché adressable exploitable (SAM)
- Estimation du marché obtenable (SOM)
- Analyse de croissance historique (5-10 ans)
- Projections de croissance (5-10 ans à venir)
- Moteurs et freins de croissance
- Ventilation régionale du marché
- Analyse par segment

**Visuels requis (4) :**
1. Graphique de trajectoire de croissance du marché (historique + projeté)
2. Diagramme à cercles concentriques TAM/SAM/SOM
3. Ventilation régionale du marché (camembert ou treemap)
4. Comparaison de croissance des segments (graphique en barres)

**Données clés :**
- Taille actuelle du marché (avec source)
- CAGR (historique et projeté)
- Taille du marché par région
- Taille du marché par segment
- Hypothèses clés des projections

**Sources de données :**
Utiliser `research-lookup` pour trouver :
- Rapports d'études de marché (Gartner, Forrester, IDC, etc.)
- Données d'associations professionnelles
- Statistiques gouvernementales
- Rapports financiers d'entreprises
- Études académiques

---

#### Chapitre 3 : Moteurs et tendances de l'industrie (5-6 pages)

**Contenu requis :**
- Facteurs macroéconomiques
- Tendances technologiques
- Moteurs réglementaires
- Évolutions sociales et démographiques
- Facteurs environnementaux
- Tendances propres au secteur

**Cadres d'analyse :**
- **Analyse PESTLE** : politique, économique, social, technologique, juridique, environnemental
- **Évaluation d'impact des tendances** : matrice probabilité vs impact

**Visuels requis (3) :**
1. Frise des tendances de l'industrie ou graphique radar
2. Matrice d'impact des moteurs
3. Diagramme d'analyse PESTLE

**Données clés :**
- 5 à 10 principaux moteurs de croissance avec impact quantifié
- Tendances émergentes avec chronologie
- Facteurs de disruption

---

#### Chapitre 4 : Paysage concurrentiel (6-8 pages)

**Contenu requis :**
- Analyse de la structure du marché
- Profils des acteurs majeurs
- Analyse des parts de marché
- Positionnement concurrentiel
- Barrières à l'entrée
- Dynamique concurrentielle

**Cadres d'analyse :**
- **Cinq forces de Porter** : analyse complète de l'industrie
- **Matrice de positionnement concurrentiel** : matrice 2x2 sur les dimensions clés
- **Cartographie des groupes stratégiques** : regrouper les concurrents par stratégie

**Visuels requis (4) :**
1. Diagramme des cinq forces de Porter
2. Camembert ou barres des parts de marché
3. Matrice de positionnement concurrentiel (2x2)
4. Carte des groupes stratégiques

**Données clés :**
- Parts de marché par entreprise (top 10)
- Évaluation de l'intensité concurrentielle
- Évaluation des barrières à l'entrée
- Évaluation du pouvoir des fournisseurs/acheteurs

---

#### Chapitre 5 : Analyse et segmentation clients (4-5 pages)

**Contenu requis :**
- Définition des segments de clientèle
- Taille et croissance des segments
- Analyse du comportement d'achat
- Besoins et points de douleur des clients
- Processus de décision
- Moteurs de valeur par segment

**Cadres d'analyse :**
- **Matrice de segmentation client** : taille vs croissance
- **Canvas de proposition de valeur** : tâches, frustrations, gains
- **Cartographie du parcours client** : de la notoriété au plaidoyer

**Visuels requis (3) :**
1. Décomposition de la segmentation client (camembert/treemap)
2. Matrice d'attractivité des segments
3. Parcours client ou diagramme de proposition de valeur

**Données clés :**
- Tailles et pourcentages des segments
- Taux de croissance par segment
- Taille moyenne des transactions / revenu par client
- Coût d'acquisition client par segment

---

#### Chapitre 6 : Paysage technologique et d'innovation (4-5 pages)

**Contenu requis :**
- Stack technologique actuel
- Technologies émergentes
- Tendances d'innovation
- Courbes d'adoption technologique
- Analyse des investissements R&D
- Paysage des brevets

**Cadres d'analyse :**
- **Évaluation de maturité technologique** : niveaux TRL
- **Positionnement sur le cycle du hype** : où se situent les technologies
- **Feuille de route technologique** : évolution dans le temps

**Visuels requis (2) :**
1. Diagramme de feuille de route technologique
2. Courbe d'innovation/d'adoption ou cycle du hype

**Données clés :**
- Dépenses R&D de l'industrie
- Jalons technologiques clés
- Tendances des dépôts de brevets
- Taux d'adoption des technologies

---

#### Chapitre 7 : Environnement réglementaire et politique (3-4 pages)

**Contenu requis :**
- Cadre réglementaire actuel
- Autorités réglementaires clés
- Exigences de conformité
- Changements réglementaires à venir
- Tendances politiques
- Évaluation d'impact

**Visuels requis (1) :**
1. Chronologie réglementaire ou diagramme de cadre

**Données clés :**
- Réglementations clés et dates d'entrée en vigueur
- Coûts de conformité
- Risques réglementaires
- Probabilité de changements politiques

---

#### Chapitre 8 : Analyse des risques (3-4 pages)

**Contenu requis :**
- Risques de marché
- Risques concurrentiels
- Risques réglementaires
- Risques technologiques
- Risques opérationnels
- Risques financiers
- Stratégies d'atténuation des risques

**Cadres d'analyse :**
- **Heatmap des risques** : probabilité vs impact
- **Registre des risques** : inventaire complet des risques
- **Matrice d'atténuation** : risque vs stratégie d'atténuation

**Visuels requis (2) :**
1. Heatmap des risques (probabilité vs impact)
2. Matrice d'atténuation des risques

**Données clés :**
- 10 principaux risques avec notation
- Scores de probabilité des risques
- Scores de sévérité d'impact
- Estimations des coûts d'atténuation

---

### Recommandations stratégiques (~10 pages)

#### Chapitre 9 : Opportunités et recommandations stratégiques (4-5 pages)

**Contenu requis :**
- Identification des opportunités
- Dimensionnement des opportunités
- Analyse des options stratégiques
- Cadre de priorisation
- Recommandations détaillées
- Facteurs de succès

**Cadres d'analyse :**
- **Matrice d'attractivité des opportunités** : attractivité vs capacité à gagner
- **Cadre d'options stratégiques** : construire, acheter, s'associer, ignorer
- **Matrice de priorité** : impact vs effort

**Visuels requis (3) :**
1. Matrice d'opportunités
2. Cadre d'options stratégiques
3. Matrice de priorité / recommandation

**Données clés :**
- Tailles des opportunités
- Besoins d'investissement
- Rendements attendus
- Délai de création de valeur

---

#### Chapitre 10 : Feuille de route de mise en œuvre (3-4 pages)

**Contenu requis :**
- Plan de mise en œuvre par phases
- Jalons et livrables clés
- Besoins en ressources
- Chronologie et séquençage
- Dépendances et chemin critique
- Structure de gouvernance

**Visuels requis (2) :**
1. Chronologie de mise en œuvre / diagramme de Gantt
2. Suivi des jalons ou diagramme de phases

**Données clés :**
- Durées des phases
- Besoins en ressources
- Jalons clés avec dates
- Allocation budgétaire par phase

---

#### Chapitre 11 : Thèse d'investissement et projections financières (3-4 pages)

**Contenu requis :**
- Synthèse de l'investissement
- Projections financières
- Analyse de scénarios
- Attentes de rendement
- Hypothèses clés
- Analyse de sensibilité

**Visuels requis (2) :**
1. Graphique de projections financières (revenus, croissance)
2. Comparaison de scénarios

**Données clés :**
- Projections de revenus (3-5 ans)
- Projections de CAGR
- Attentes ROI/IRR
- Hypothèses financières clés

---

### Pages finales (~5 pages)

#### Annexe A : Méthodologie et sources de données (1-2 pages)
- Méthodologie de recherche
- Approche de collecte des données
- Sources et citations
- Limites et hypothèses

#### Annexe B : Tableaux détaillés de données de marché (2-3 pages)
- Tableaux complets de données de marché
- Ventilations régionales
- Détails par segment
- Séries de données historiques

#### Annexe C : Profils d'entreprises (1-2 pages)
- Brefs profils des concurrents clés
- Faits financiers marquants
- Axes d'orientation stratégique

#### Références/Bibliographie
- Toutes les sources citées
- Format BibTeX pour LaTeX

---

## Flux de travail

### Phase 1 : Recherche et collecte de données

**Étape 1 : Définir le périmètre**
- Clarifier la définition du marché
- Fixer les frontières géographiques
- Déterminer l'horizon temporel
- Identifier les questions clés auxquelles répondre

**Étape 2 : Mener une recherche approfondie**

Utiliser `research-lookup` largement pour collecter les données de marché :

```bash
# Market size and growth data
python skills/research-lookup/scripts/research_lookup.py \
  "What is the current market size and projected growth rate for [MARKET] industry? Include TAM, SAM, SOM estimates and CAGR projections"

# Competitive landscape
python skills/research-lookup/scripts/research_lookup.py \
  "Who are the top 10 competitors in the [MARKET] market? What is their market share and competitive positioning?"

# Industry trends
python skills/research-lookup/scripts/research_lookup.py \
  "What are the major trends and growth drivers in the [MARKET] industry for 2024-2030?"

# Regulatory environment
python skills/research-lookup/scripts/research_lookup.py \
  "What are the key regulations and policy changes affecting the [MARKET] industry?"
```

**Étape 3 : Organisation des données**
- Créer un dossier `sources/` avec les notes de recherche
- Organiser les données par section
- Identifier les manques de données
- Mener des recherches complémentaires si nécessaire

### Phase 2 : Analyse et application des cadres

**Étape 4 : Appliquer les cadres d'analyse**

Pour chaque cadre, mener une analyse structurée :

- **Dimensionnement du marché** : TAM → SAM → SOM avec hypothèses claires
- **Cinq forces de Porter** : noter chaque force Élevé/Moyen/Faible avec justification
- **PESTLE** : analyser chaque dimension avec tendances et impacts
- **SWOT** : forces/faiblesses internes, opportunités/menaces externes
- **Positionnement concurrentiel** : définir les axes, placer les concurrents

**Étape 5 : Développer les insights**
- Synthétiser les constats en insights clés
- Identifier les implications stratégiques
- Élaborer les recommandations
- Prioriser les opportunités

### Phase 3 : Génération visuelle

**Étape 6 : Générer tous les visuels**

Générer les visuels AVANT de rédiger le rapport. Utiliser le script de génération en lot :

```bash
# Generate all standard market report visuals
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "[MARKET NAME]" \
  --output-dir figures/
```

Ou générer individuellement :

```bash
# 1. Market growth trajectory
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Bar chart showing market growth from 2020 to 2034, with historical bars in dark blue (2020-2024) and projected bars in light blue (2025-2034). Y-axis shows market size in billions USD. Include CAGR annotation" \
  -o figures/01_market_growth.png --doc-type report

# 2. TAM/SAM/SOM breakdown
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circles diagram. Outer circle TAM Total Addressable Market, middle circle SAM Serviceable Addressable Market, inner circle SOM Serviceable Obtainable Market. Each labeled with acronym and description. Blue gradient" \
  -o figures/02_tam_sam_som.png --doc-type report

# 3. Porter's Five Forces
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: Threat of New Entrants (top), Bargaining Power of Suppliers (left), Bargaining Power of Buyers (right), Threat of Substitutes (bottom). Color code by rating: High=red, Medium=yellow, Low=green" \
  -o figures/03_porters_five_forces.png --doc-type report

# 4. Competitive positioning matrix
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 competitive positioning matrix with X-axis 'Market Focus (Niche to Broad)' and Y-axis 'Solution Approach (Product to Platform)'. Plot 8-10 competitors as labeled circles of varying sizes. Include quadrant labels" \
  -o figures/04_competitive_positioning.png --doc-type report

# 5. Risk heatmap
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk heatmap matrix. X-axis Impact (Low to Critical), Y-axis Probability (Unlikely to Very Likely). Color gradient: Green (low risk) to Red (critical risk). Plot 10-12 risks as labeled points" \
  -o figures/05_risk_heatmap.png --doc-type report

# 6. (Optional) Executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, modern data visualization style, blue and green color scheme, clean minimalist design" \
  --output figures/06_exec_summary.png
```

### Phase 4 : Rédaction du rapport

**Étape 7 : Initialiser la structure du projet**

Créer la structure de projet standard :

```
writing_outputs/YYYYMMDD_HHMMSS_market_report_[topic]/
├── progress.md
├── drafts/
│   └── v1_market_report.tex
├── references/
│   └── references.bib
├── figures/
│   └── [all generated visuals]
├── sources/
│   └── [research notes]
└── final/
```

**Étape 8 : Rédiger le rapport à partir du template**

Utiliser le `market_report_template.tex` comme point de départ. Rédiger chaque section en suivant le guide de structure, en veillant à :

- **Couverture complète** : chaque sous-section traitée
- **Contenu orienté données** : affirmations étayées par la recherche
- **Intégration visuelle** : référencer toutes les figures générées
- **Ton professionnel** : écriture de style cabinet de conseil
- **Sans contrainte de tokens** : écrire pleinement, sans abréger

**Directives de rédaction :**
- Utiliser la voix active autant que possible
- Commencer par les insights, appuyer avec les données
- Utiliser des listes numérotées pour les recommandations
- Inclure les sources de données pour toutes les statistiques
- Créer des transitions fluides entre les sections

### Phase 5 : Compilation et relecture

**Étape 9 : Compiler le LaTeX**

```bash
cd writing_outputs/[project_folder]/drafts/
xelatex v1_market_report.tex
bibtex v1_market_report
xelatex v1_market_report.tex
xelatex v1_market_report.tex
```

**Étape 10 : Revue qualité**

Vérifier que le rapport respecte les standards de qualité :

- [ ] Le nombre total de pages atteint 50+
- [ ] Tous les visuels essentiels (5-6 cœur + supplémentaires) sont inclus et s'affichent correctement
- [ ] La synthèse pour la direction capture les constats clés
- [ ] Tous les points de données ont des sources citées
- [ ] Les cadres d'analyse sont correctement appliqués
- [ ] Les recommandations sont actionnables et priorisées
- [ ] Aucune figure ou tableau orphelin
- [ ] Table des matières, liste des figures et liste des tableaux exactes
- [ ] Bibliographie complète
- [ ] Le PDF se compile sans erreur

**Étape 11 : Relecture par les pairs**

Utiliser le skill peer-review pour évaluer le rapport :
- Évaluer l'exhaustivité
- Vérifier l'exactitude des données
- Contrôler la fluidité logique
- Évaluer la qualité des recommandations

---

## Standards de qualité

### Objectifs de nombre de pages

| Section | Pages minimum | Pages cible |
|---------|---------------|--------------|
| Pages liminaires | 4 | 5 |
| Vue d'ensemble du marché | 4 | 5 |
| Taille du marché et croissance | 5 | 7 |
| Moteurs de l'industrie | 4 | 6 |
| Paysage concurrentiel | 5 | 7 |
| Analyse clients | 3 | 5 |
| Paysage technologique | 3 | 5 |
| Environnement réglementaire | 2 | 4 |
| Analyse des risques | 2 | 4 |
| Recommandations stratégiques | 3 | 5 |
| Feuille de route de mise en œuvre | 2 | 4 |
| Thèse d'investissement | 2 | 4 |
| Pages finales | 4 | 5 |
| **TOTAL** | **43** | **66** |

### Exigences de qualité visuelle

- **Résolution** : toutes les images à 300 DPI minimum
- **Format** : PNG pour le raster, PDF pour le vectoriel
- **Accessibilité** : palettes adaptées au daltonisme
- **Cohérence** : même palette de couleurs sur tout le rapport
- **Étiquetage** : tous les axes, légendes et points de données étiquetés
- **Attribution des sources** : sources citées dans les légendes des figures

### Exigences de qualité des données

- **Actualité** : données de moins de 2 ans (année courante de préférence)
- **Sourçage** : toutes les statistiques attribuées à des sources précises
- **Validation** : recouper plusieurs sources quand c'est possible
- **Hypothèses** : toutes les projections énoncent leurs hypothèses sous-jacentes
- **Limites** : reconnaître les limites et les manques des données

### Exigences de qualité rédactionnelle

- **Objectivité** : présentation équilibrée, reconnaissance des incertitudes
- **Clarté** : éviter le jargon, définir les termes techniques
- **Précision** : chiffres précis plutôt que qualificatifs vagues
- **Structure** : titres clairs, logique fluide, transitions naturelles
- **Actionnabilité** : recommandations spécifiques et implémentables

---

## Mise en forme LaTeX

### Utilisation du package de style

Le package `market_research.sty` fournit une mise en forme professionnelle. L'inclure dans votre document :

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{market_research}
```

### Environnements d'encadrés

Utiliser des encadrés colorés pour mettre en valeur le contenu clé :

```latex
% Key insight box (blue)
\begin{keyinsightbox}[Key Finding]
The market is projected to grow at 15.3% CAGR through 2030.
\end{keyinsightbox}

% Market data box (green)
\begin{marketdatabox}[Market Snapshot]
\begin{itemize}
    \item Market Size (2024): \$45.2B
    \item Projected Size (2030): \$98.7B
    \item CAGR: 15.3%
\end{itemize}
\end{marketdatabox}

% Risk box (orange/warning)
\begin{riskbox}[Critical Risk]
Regulatory changes could impact 40% of market participants.
\end{riskbox}

% Recommendation box (purple)
\begin{recommendationbox}[Strategic Recommendation]
Prioritize market entry in the Asia-Pacific region.
\end{recommendationbox}

% Callout box (gray)
\begin{calloutbox}[Definition]
TAM (Total Addressable Market) represents the total revenue opportunity.
\end{calloutbox}
```

### Mise en forme des figures

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/market_growth.png}
\caption{Market Growth Trajectory (2020-2030). Source: Industry analysis, company data.}
\label{fig:market_growth}
\end{figure}
```

### Mise en forme des tableaux

```latex
\begin{table}[htbp]
\centering
\caption{Market Size by Region (2024)}
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Region} & \textbf{Size (USD)} & \textbf{Share} & \textbf{CAGR} \\
\midrule
North America & \$18.2B & 40.3\% & 12.5\% \\
\rowcolor{tablealt} Europe & \$12.1B & 26.8\% & 14.2\% \\
Asia-Pacific & \$10.5B & 23.2\% & 18.7\% \\
\rowcolor{tablealt} Rest of World & \$4.4B & 9.7\% & 11.3\% \\
\midrule
\textbf{Total} & \textbf{\$45.2B} & \textbf{100\%} & \textbf{15.3\%} \\
\bottomrule
\end{tabular}
\label{tab:market_by_region}
\end{table}
```

Pour la référence complète de mise en forme, voir `assets/FORMATTING_GUIDE.md`.

---

## Intégration avec d'autres skills

Ce skill fonctionne en synergie avec :

- **research-lookup** : essentiel pour collecter données de marché, statistiques et renseignement concurrentiel
- **scientific-schematics** : générer tous les diagrammes, graphiques et visualisations
- **generate-image** : créer infographies et illustrations conceptuelles
- **peer-review** : évaluer la qualité et l'exhaustivité du rapport
- **citation-management** : gérer les références BibTeX

---

## Exemples de prompts

### Section Vue d'ensemble du marché

```
Write a comprehensive market overview section for the [Electric Vehicle Charging Infrastructure] market. Include:
- Clear market definition and scope
- Industry ecosystem with key stakeholders
- Value chain analysis
- Historical evolution of the market
- Current market dynamics

Generate 2 supporting visuals using scientific-schematics.
```

### Section Paysage concurrentiel

```
Analyze the competitive landscape for the [Cloud Computing] market. Include:
- Porter's Five Forces analysis with High/Medium/Low ratings
- Top 10 competitors with market share
- Competitive positioning matrix
- Strategic group mapping
- Barriers to entry analysis

Generate 4 supporting visuals including Porter's Five Forces diagram and positioning matrix.
```

### Section Recommandations stratégiques

```
Develop strategic recommendations for entering the [Renewable Energy Storage] market. Include:
- 5-7 prioritized recommendations
- Opportunity sizing for each
- Implementation considerations
- Risk factors and mitigations
- Success criteria

Generate 3 supporting visuals including opportunity matrix and priority framework.
```

---

## Checklist : validation 50+ pages

Avant de finaliser le rapport, vérifier :

### Exhaustivité de la structure
- [ ] Page de couverture avec visuel héros
- [ ] Table des matières (auto-générée)
- [ ] Liste des figures (auto-générée)
- [ ] Liste des tableaux (auto-générée)
- [ ] Synthèse pour la direction (2-3 pages)
- [ ] Les 11 chapitres cœur présents
- [ ] Annexe A : Méthodologie
- [ ] Annexe B : Tableaux de données
- [ ] Annexe C : Profils d'entreprises
- [ ] Références/Bibliographie

### Exhaustivité visuelle (5-6 cœur)
- [ ] Graphique de trajectoire de croissance du marché (priorité 1)
- [ ] Diagramme TAM/SAM/SOM (priorité 2)
- [ ] Cinq forces de Porter (priorité 3)
- [ ] Matrice de positionnement concurrentiel (priorité 4)
- [ ] Heatmap des risques (priorité 5)
- [ ] Infographie de synthèse exécutive (priorité 6, optionnel)

### Visuels supplémentaires (générer selon les besoins)
- [ ] Diagramme d'écosystème du marché
- [ ] Graphique de ventilation régionale
- [ ] Graphique de croissance des segments
- [ ] Diagramme de tendances/PESTLE
- [ ] Graphique de parts de marché
- [ ] Graphique de segmentation client
- [ ] Feuille de route technologique
- [ ] Chronologie réglementaire
- [ ] Matrice d'opportunités
- [ ] Chronologie de mise en œuvre
- [ ] Graphique de projections financières
- [ ] Autres visuels spécifiques aux sections

### Qualité du contenu
- [ ] Toutes les statistiques ont des sources
- [ ] Les projections incluent des hypothèses
- [ ] Cadres correctement appliqués
- [ ] Recommandations actionnables
- [ ] Rédaction de qualité professionnelle
- [ ] Aucune section placeholder ou incomplète

### Qualité technique
- [ ] PDF compilé sans erreur
- [ ] Toutes les figures s'affichent correctement
- [ ] Les renvois fonctionnent
- [ ] Bibliographie complète
- [ ] Nombre de pages supérieur à 50

---

## Ressources

### Fichiers de référence

Charger ces fichiers pour des consignes détaillées :

- **`references/report_structure_guide.md`** : exigences de contenu détaillées, section par section
- **`references/visual_generation_guide.md`** : prompts complets pour générer tous les types de visuels
- **`references/data_analysis_patterns.md`** : templates pour Porter, PESTLE, SWOT, etc.

### Assets

- **`assets/market_research.sty`** : package de style LaTeX
- **`assets/market_report_template.tex`** : template LaTeX complet
- **`assets/FORMATTING_GUIDE.md`** : référence rapide des environnements d'encadrés et du style

### Scripts

- **`scripts/generate_market_visuals.py`** : générer en lot tous les visuels du rapport

---

## Dépannage

### Problèmes courants

**Problème** : le rapport fait moins de 50 pages
- **Solution** : développer les tableaux de données en annexes, ajouter des profils d'entreprises plus détaillés, inclure des ventilations régionales supplémentaires

**Problème** : les visuels ne s'affichent pas
- **Solution** : vérifier les chemins de fichiers dans LaTeX, s'assurer que les images sont dans le dossier figures/, vérifier les extensions

**Problème** : entrées manquantes dans la bibliographie
- **Solution** : exécuter bibtex après la première passe xelatex, vérifier les erreurs de syntaxe dans le fichier .bib

**Problème** : débordement de tableau/figure
- **Solution** : utiliser `\resizebox` ou le package `adjustbox`, réduire le pourcentage de largeur des images

**Problème** : qualité visuelle médiocre de la génération
- **Solution** : utiliser l'option `--doc-type report`, augmenter les itérations avec `--iterations 5`

---

Utilisez ce skill pour créer des rapports d'étude de marché complets et riches en visuels qui rivalisent avec les livrables des plus grands cabinets de conseil. La combinaison d'une recherche approfondie, de cadres structurés et d'une visualisation étendue produit des documents qui éclairent les décisions stratégiques et témoignent d'une rigueur analytique.
