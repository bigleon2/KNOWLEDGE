# Référentiel spécialités et orientations professionnelles (à consulter par l'agent lors de l'analyse)

Ce document est une **base de connaissances de référence** ; il ne remplace pas le jugement personnalisé. L'agent doit croiser le profil du candidat et les données réelles des vœux dans `parsed.json` pour produire `analysis.json`.

---

## Dimensions d'analyse (à considérer obligatoirement par l'agent)

| Dimension | Description |
|------|------|
| Matières choisies et prérequis de spécialité | vérifier le champ `claim` (ex. « physique et chimie ») pour éviter de recommander une spécialité incompatible avec les matières choisies |
| Notes par matière | maths/physique solides → ingénierie, informatique, électronique ; biologie/chimie solides → médecine, sciences du vivant ; chinois/anglais solides → gestion, droit, humanités |
| Centres d'intérêt | les projeter sur de grandes familles de spécialités concrètes, pas de généralités |
| Orientation professionnelle | distinguer « orientation prioritaire » et « orientations de repli », en justifiant |
| Situation familiale | volonté de poursuivre en études longues, capacité financière, préférence géographique, acceptation d'un cursus long (ex. médecine) |
| Opportunités de la ville | industries de la ville visée et ressources de stages/emploi |
| Probabilité d'admission | en croisant les paliers ambitieux/stables/garantis, expliquer pourquoi tel établissement/spécialité est marqué recommandé |

**Contrainte dure** : les `university_name`, `university_code`, `major_name`, `major_code` de `recommended_majors` / `recommended_schools` doivent provenir de `parsed.json`, sinon le HTML ne pourra pas apposer les labels de recommandation.

---

## Grandes familles de spécialités et débouchés

### 🧑‍💻 Informatique et technologies dures

| Famille | Mots-clés types des spécialités | Débouchés | Caractéristiques de formation |
|----------|------------------|----------|----------|
| Informatique | informatique, génie logiciel, IA, big data | internet, IA, fintech, jeu vidéo | débouchés larges, concurrence forte, apprentissage continu requis |
| Électronique et information | électronique et information, télécoms, micro-électronique, circuits intégrés | puces, équipements télécoms, électronique grand public | cœur des technologies dures, fort exigence maths-physique |
| Automatique | automatique, robotique, contrôle | fabrication intelligente, conduite autonome, logiciels industriels | discipline croisée, solide socle d'ingénierie |

**Candidats adaptés** : excellents résultats en maths-physique, goût pour le code/la technologie, famille soutenant des études longues ou acceptant une charge de travail intense.

---

### 🩺 Santé et médecine

| Famille | Mots-clés types | Débouchés | Caractéristiques |
|----------|------------------|----------|----------|
| Médecine clinique | médecine clinique, chirurgie dentaire | hôpitaux de tierce catégorie A, médecine de proximité, recherche | cursus long (5 ans et +), master/residanat fréquents |
| Médecine fondamentale/préventive | médecine fondamentale, médecine préventive, santé publique | contrôle épidémiologique, recherche, administration sanitaire | plutôt recherche et gestion |
| Pharmacie / soins infirmiers | pharmacie, sciences infirmières | industrie pharmaceutique, postes hospitaliers | emploi relativement stable |

**Candidats adaptés** : bons résultats en biologie/chimie, acceptation d'une formation longue, famille soutenant les études supérieures, recherche de stabilité professionnelle.

---

### ⚙️ Ingénierie et fabrication avancée

| Famille | Mots-clés types | Débouchés | Caractéristiques |
|----------|------------------|----------|----------|
| Mécanique / automobile | mécanique, véhicule, fabrication intelligente | automobile, équipementier, énergies nouvelles | socle classique de l'ingénierie, très stable |
| Aérospatial | aérospatial, aéronefs | industrie de défense, spatial, aviation civile | établissements concentrés, les « Sept Fils de la Défense » méritent l'attention |
| Électrique / énergie | électrotechnique, énergie, énergies nouvelles | réseaux électriques, énergies nouvelles, équipementiers | nombreuses opportunités en entreprises publiques |
| Matériaux / génie civil | matériaux, génie civil, architecture | infrastructures, nouveaux matériaux, immobilier | forte cyclicité sectorielle, à croiser avec la ville |

**Candidats adaptés** : physique solide, goût pour l'industrie réelle, acceptation d'un parcours de croissance d'ingénieur.

---

### 📊 Économie, finance et gestion

| Famille | Mots-clés types | Débouchés | Caractéristiques |
|----------|------------------|----------|----------|
| Finance / économie | finance, économie, finances publiques | banque, titres, conseil, finance d'entreprise | le prestige de l'école et les stages comptent beaucoup |
| Gestion des entreprises | gestion, marketing, comptabilité | management, audit, opérations | spectre large, stages à accumuler tôt |
| Statistique | statistique, statistique économique | analyse de données, gestion des risques, recherche | profil maths + business |

**Candidats adaptés** : bons résultats en chinois/anglais, forte capacité de communication, visant les ressources finance/gestion des villes de premier rang.

---

### ⚖️ Droit, éducation et service public

| Orientation | Mots-clés | Description |
|------|--------|------|
| Droit | droit, propriété intellectuelle | barreau exigeant, forte dispersion des débouchés |
| Enseignement / éducation | enseignement (normales), sciences de l'éducation, psychologie | forte stabilité, privilégier les écoles normales nationales/provinciales |
| Administration publique | administration, gestion des affaires publiques | concours de la fonction publique, établissements publics |

---

## Villes cibles et industries de référence

| Ville | Industries fortes et particularités d'emploi |
|------|-------------------|
| Pékin | sièges internet, entreprises publiques centrales, instituts de recherche, sièges financiers ; stages et études longues abondants |
| Shanghai | finance, entreprises étrangères, biopharmacie, circuits intégrés ; très international |
| Shenzhen | technologies dures, internet, innovation et création d'entreprise ; secteur privé et tech très dynamiques |
| Hangzhou | e-commerce, économie numérique, applications IA ; écosystème Alibaba et start-ups |
| Wuhan | pôle optique-électronique de la vallée de la lumière, ressources universitaires, industrie ; plaque tournante du centre au bon rapport qualité/prix |
| Chengdu | jeu vidéo, internet, électronique et information ; coût de la vie des villes du nouveau premier rang relativement doux |
| Xi'an | aérospatial, électronique et information, défense ; riche héritage scientifique et éducatif |
| Guangzhou | industrie de la Grande Baie, santé, commerce ; forte articulation entre universités provinciales et industrie |
| Nanjing | logiciel, fabrication avancée, forte densité universitaire |
| Tianjin | industrie, économie portuaire, concentration d'écoles d'ingénieurs |

---

## Aide-mémoire des niveaux d'établissements (en appui de la recommandation)

| Label | Conseil de stratégie de saisie |
|------|--------------|
| 985 / Double première classe | cible des paliers ambitieux/stables, regarder les disciplines d'excellence et le taux d'accès direct au master |
| 211 | fer de lance des paliers stable/garanti, croiser ville et classement de spécialité |
| Accès master sans examen | à pondérer en priorité si poursuite d'études envisagée |
| National / provincial | forte reconnaissance sectorielle pour l'enseignement, la médecine etc. |
| Sept Fils de la Défense / Six écoles de défense | ingénierie, orientations liées à la défense |

---

## Volumes recommandés pour la production

| Champ | Nombre conseillé | Description |
|------|----------|------|
| `major_directions` | 2–4 entrées | triées par adéquation, chacune avec une description personnalisée |
| `recommended_majors` | 8–15 entrées | couvrant ambitieux/stable/garanti, priorité aux spécialités cœur du palier « stable » |
| `recommended_schools` | 6–12 établissements | dédupliqués, chaque palier représenté |

`modal.body` utilise un fragment HTML (`<h4>`, `<ul>`, `<li>`, `<strong>`), rédigé **pour ce candidat précis**, en évitant les formules toutes faites.
