---
name: ai-news-collector
version: "1.0.0"
category: "Autres"
tags:
  - ai
  - news
  - collectors
description: Agrégateur d'actualités IA avec tri par popularité. Se déclenche lorsque l'utilisateur demande les dernières actualités du domaine de l'IA, par exemple : « Quelles nouvelles IA aujourd'hui ? », « Résume l'actu IA de la semaine », « Quels produits IA font le buzz en ce moment ? », « De quoi parle-t-on dans le monde de l'IA ? ». Couvre : lancements de produits, articles de recherche, actualités du secteur, levées de fonds, mises à jour de projets open source, phénomènes viraux de communauté, projets IA/Agent populaires. Produit une liste de résumés triée par popularité, avec les liens vers les sources d'origine.
language: fr

---

# AI News Collector

Collecter, agréger et trier par popularité les actualités du domaine de l'IA.

## Principe fondamental

**Ne faites pas seulement une recherche « AI news today ».** Les recherches génériques renvoient des pages d'agrégation SEO et des articles de prévisions, qui passent systématiquement à côté des phénomènes viraux issus des communautés (outils open source devenus viraux, événements de niveau mème, etc.). Une stratégie de recherche multi-dimensionnelle et par niveaux est indispensable.

## Workflow

### 1. Recherche multi-dimensionnelle par niveaux (au minimum 8 requêtes, 10-12 recommandées)

Exécutez les recherches selon les **6 dimensions** suivantes, au moins 1 requête par dimension :

#### Dimension A : agrégateurs hebdomadaires / Newsletter (priorité maximale 🔑)

C'est la source la plus dense en informations : un seul article peut couvrir plus de 10 actualités.

```
Requêtes :
- "last week in AI" [mois et année en cours]
- "AI weekly roundup" [mois et année en cours]
- "the batch AI newsletter"
- site:substack.com AI news [mois en cours]
```

Après avoir trouvé une newsletter hebdomadaire, utilisez web_fetch pour récupérer le texte intégral et en extraire toutes les pistes d'actualités.

#### Dimension B : popularité communautaire / viralité (dimension clé 🔑)

Capter les succès venus d'en bas, presque inatteignables par une recherche générique.

```
Requêtes :
- "viral AI tool" OR "viral AI agent"
- "AI trending" site:reddit.com OR site:news.ycombinator.com
- "GitHub trending AI" OR "AI open source trending"
- AI buzzing OR "everyone is talking about" AI
- "most popular AI" this week
```

#### Dimension C : lancements de produits et mises à jour de modèles

```
Requêtes :
- "AI model release" OR "LLM launch" [mois en cours]
- "AI product launch" [mois et année en cours]
- OpenAI OR Anthropic OR Google OR Meta AI announcement
- "大模型 发布" OR "AI 新产品"
```

#### Dimension D : financement et business

```
Requêtes :
- "AI startup funding" [mois et année en cours]
- "AI acquisition" OR "AI IPO"
- "AI 融资" OR "人工智能投资"
```

#### Dimension E : percées de recherche

```
Requêtes :
- "AI breakthrough" OR "AI paper" [mois en cours]
- "state of the art" machine learning
- "AI 论文" OR "机器学习突破"
```

#### Dimension F : régulation et politiques publiques

```
Requêtes :
- "AI regulation" OR "AI policy" [mois et année en cours]
- "AI law" OR "AI governance" 
- "AI 监管" OR "人工智能法案"
```

### 2. Recoupement et comblement des manques

À la fin de la première série de recherches, vérifiez qu'il ne manque rien :

- Si une newsletter mentionne un projet/événement non couvert par la première série → recherche ciblée sur ce projet
- Si le même événement est mentionné par 3+ sources différentes → très probablement un sujet chaud ; approfondissez pour obtenir plus de détails
- Si les sujets chauds des médias francophones et anglophones diffèrent complètement → couvrez les deux côtés

### 3. Principes de conception des requêtes (liste des anti-patterns)

| ❌ Ne pas faire cette recherche | ✅ Faire plutôt cette recherche | Raison |
|---|---|---|
| "AI news today February 2026" | "AI weekly roundup February 2026" | La première renvoie des pages d'agrégation, la seconde du contenu éditorialisé |
| "AI news today" | "viral AI tool" + "AI model release" recherchés séparément | Une recherche générique ne couvre pas les phénomènes communautaires |
| "artificial intelligence breaking news" | Rechercher par dimension | Trop large, renvoie du bruit |
| Ajouter une date précise dans la requête | Utiliser "this week" "today" "latest" | Les dates orientent vers des articles de prévisions/perspectives |
| Faire 3 recherches et commencer à rédiger | Au moins 8 recherches, couvrant les 6 dimensions | 3 recherches couvrent moins de 30 % du terrain |

### 4. Évaluation globale de la popularité

Évaluez la popularité de chaque actualité (1 à 5 étoiles) à partir des signaux suivants :

| Signal | Poids | Commentaire |
|------|------|------|
| Plusieurs médias rapportent le même événement | ⭐⭐⭐ élevé | 3+ sources = sujet chaud confirmé |
| Preuves de viralité communautaire | ⭐⭐⭐ élevé | Étoiles GitHub en flèche, Twitter saturé, page d'accueil HN |
| Source faisant autorité (conférences majeures, annonces officielles des grands acteurs) | ⭐⭐⭐ élevé | Mais attention : la com d'un grand acteur n'est pas un vrai sujet chaud |
| Retours d'expérience d'utilisateurs réels | ⭐⭐ moyen | Des gens l'utilisent vraiment > c'est juste sorti |
| Rupture technologique / périmètre d'impact | ⭐⭐ moyen | |
| Caractère controversé (débats sécurité, éthique) | ⭐⭐ moyen | Une controverse révèle souvent une forte influence |
| Fraîcheur (plus c'est récent, plus c'est chaud) | ⭐ moyen/faible | Sert au tri secondaire |

### 5. Format de sortie

Triées par popularité décroissante, sortez **15 à 25** actualités :

```
## 🔥 À la une IA (YYYY-MM-DD)

### ⭐⭐⭐⭐⭐ Popularité maximale

1. **[Titre de l'actualité]**
   > Résumé en une phrase (50 caractères maximum)
   > 🔗 [Nom de la source](URL)

### ⭐⭐⭐⭐ Forte popularité

2. ...

### ⭐⭐⭐ Popularité moyenne

...

---
📊 Total de cette collecte : XX actualités | XX recherches | Dimensions couvertes : A/B/C/D/E/F | Mise à jour : HH:MM
```

### 6. Déduplication et fusion

- Quand le même événement est rapporté par plusieurs médias, fusionnez-le en une seule entrée en retenant la source la plus fiable/détaillée
- Mentionnez « rapporté par plusieurs médias » dans le résumé pour traduire la popularité
- Les projets renommés comptent comme un même événement (ex. Clawdbot → Moltbot → OpenClaw)

## Sources d'actualités recommandées

Voir [references/sources.md](references/sources.md).

## Points d'attention

- Privilégiez les liens HTTPS
- En cas de paywall/contenu inaccessible, indiquez « sur abonnement »
- Restez objectif : pas d'évaluation subjective du contenu des actualités
- Ne commencez pas à rédiger avant d'avoir fait au moins 8 recherches
- Si une dimension ne donne aucun résultat, reformulez les mots-clés et relancez
