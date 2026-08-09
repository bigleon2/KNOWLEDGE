# Classification des types de tâches — gen-plan E3

## Type 1 — Document Création

**Indicateurs** :
- Mots-clés : rapport, document, article, analyse, proposition, PRD, script, manuscrit, présentation, tableur
- Formats : DOCX, PDF, XLSX, PPTX, MD
- Verbes : rédiger, créer, générer, produire, écrire, composer

**Skill à invoquer** :
- docx → `docx`
- PDF → `pdf`
- Tableur → `xlsx`
- Présentation → `pptx`
- Markdown seul → aucun skill (rédaction directe)

**Exemples** :
- "Écris un rapport d'analyse" → Type 1, skill docx
- "Génère une présentation" → Type 1, skill pptx

**Contre-exemples** :
- "Affiche ces données en graphique" → Type 2
- "Construis une page web" → Type 3

---

## Type 2 — Data Visualization

**Indicateurs** :
- Mots-clés : graphique, chart, diagramme, mind map, flowchart, architecture, visualisation
- Formats : PNG, SVG, Mermaid, D3, ECharts
- Verbes : tracer, dessiner, visualiser, représenter

**Skill** : `charts`

**Sous-routage** :
- Données chiffrées → matplotlib/seaborn/echarts
- Structure/diagramme → Mermaid ou Playwright+CSS
- Mind map → Playwright+CSS (pas matplotlib)
- Dashboard → charts d'abord, puis Type 3 si interactif

---

## Type 3 — Interactive Web Development

**Indicateurs** :
- Mots-clés : site web, application, dashboard interactif, page, interface, Next.js, React
- Interactivité : cliquable, dynamique, temps réel, formulaire, navigation
- Verbes : construis, développe, crée une app, build

**Skill** : `fullstack-dev`

**Contre-exemples** :
- "Génère un dashboard en PDF" → Type 1
- "Affiche des données en graphique statique" → Type 2

---

## Type 4 — Data Processing

**Indicateurs** :
- Mots-clés : analyse, traiter, transformer, calculer, extraire, filtrer, convertir
- Absence de livrable document final
- Focus sur le traitement de données

**Action** : Écrire un script Python directement

---

## Cas ambigus — Règle de décision

| Situation | Règle | Type |
|-----------|-------|------|
| "Dashboard" sans précision | Demander : interactif ou statique ? | 3 si interactif, 1/2 si statique |
| "Analyse" avec sortie document | Finalité = document | Type 1 |
| "Analyse" sans sortie | Traitement de données | Type 4 |
| "Visualisation" dans un document | Finalité = document | Type 1 (charts embarqués) |
| "Visualisation" autonome | Finalité = visuel | Type 2 |
| Mention Next.js/React | Toujours web dev | Type 3 |