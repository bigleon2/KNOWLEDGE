---
nom: ai-news-collector
source: skills/ai-news-collectors/SKILL.md
sha256_source: 84c8db19578d
genere: 2026-10-28 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — ai-news-collector (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/ai-news-collectors/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: ai-news-collector
description: >-
  Outil d'agrégation et de classement par popularité de l'actualité IA. Se déclenche quand
  l'utilisateur demande les dernières nouvelles du domaine IA, ex. : « 今天有什么 AI 新闻？ »
  (Quelles nouvelles IA aujourd'hui ?), « 总结一下这周的 AI 动态 » (résume l'actualité IA de la
  semaine), « 最近有什么火的 AI 产品？ » (produits IA en vogue récemment), « AI 圈最近在讨论什么？ »
  (de quoi parle la communauté IA en ce moment ?). Couverture : lancements de produits, articles
  de recherche, actualité sectorielle, levées de fonds, mises à jour de projets open source,
  phénomènes viraux communautaires, projets IA/Agent populaires. Produit une liste récapitulative
  en chinois, triée par popularité, avec liens vers les sources originales.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# AI News Collector

Collecte, agrège et classe par popularité l'actualité du domaine IA.

## Principe fondamental

**Ne pas se contenter de chercher « AI news today ».** Une recherche générique renvoie des pages agrégées SEO et des articles de prospective, et omet systématiquement les phénomènes viraux au niveau communautaire (outil open source qui explose, événement mémétique). Une stratégie de recherche multidimensionnelle et étagée est indispensable.

## Flux de travail

### 1. Recherche étagée multidimensionnelle (minimum 8 recherches, 10-12 recommandées)

Exécuter les recherches selon les **6 dimensions** suivantes, au moins une par dimension :

#### Dimension A : hebdomadaires / newsletters (priorité maximale 🔑)

Source à la plus forte densité d'information : un seul article peut couvrir 10+ actualités.

```
Termes de recherche :
- "last week in AI" [mois année en cours]
- "AI weekly roundup" [mois année en cours]
- "the batch AI newsletter"
- site:substack.com AI news [mois en cours]
```

Une fois un hebdo repéré, récupérer le texte intégral via web_fetch et en extraire tous les indices d'actualité.

#### Dimension B : engouement communautaire / viralité (dimension clé 🔑)

Capte les succès communautaires ascendants, quasi inaccessibles via la recherche générique.

```
Termes de recherche :
- "viral AI tool" OR "viral AI agent"
- "AI trending" site:reddit.com OR site:news.ycombinator.com
- "GitHub trending AI" OR "AI open source trending"
- AI buzzing OR "everyone is talking about" AI
- "most popular AI" this week
```

#### Dimension C : lancements de produits et mises à jour de modèles

```
Termes de recherche :
- "AI model release" OR "LLM launch" [mois en cours]
- "AI product launch" [mois année en cours]
- OpenAI OR Anthropic OR Google OR Meta AI announcement
- "大模型 发布" OR "AI 新产品"   (médias chinois)
```

#### Dimension D : financement et affaires

```
Termes de recherche :
- "AI startup funding" [mois année en cours]
- "AI acquisition" OR "AI IPO"
- "AI 融资" OR "人工智能投资"   (médias chinois)
```

#### Dimension E : percées de recherche

```
Termes de recherche :
- "AI breakthrough" OR "AI paper" [mois en cours]
- "state of the art" machine learning
- "AI 论文" OR "机器学习突破"   (médias chinois)
```

#### Dimension F : régulation et politique

```
Termes de recherche :
- "AI regulation" OR "AI policy" [mois année en cours]
- "AI law" OR "AI governance"
- "AI 监管" OR "人工智能法案"   (médias chinois)
```

### 2. Recoupement et rattrapage

Une fois la première vague de recherches terminée, vérifier les oublis :

- Si un hebdo mentionne un projet/événement non couvert par la recherche initiale → recherche dédiée sur ce projet
- Si un même événement est cité par 3+ sources distinctes → très probablement un sujet chaud ; approfondir pour plus de détails
- Si les sujets chauds des médias chinois et anglophones diffèrent complètement → couvrir les deux

### 3. Principes de conception des mots-clés (liste d'anti-patterns)

| ❌ À ne pas faire | ✅ À faire | Raison |
|---|---|---|
| "AI news today February 2026" | "AI weekly roundup February 2026" | Le premier renvoie des pages agrégées, le second du contenu éditorial |
| "AI news today" | Séparer "viral AI tool" + "AI model release" | La recherche générique ne couvre pas les phénomènes communautaires |
| "artificial intelligence breaking news" | Rechercher par dimension | Trop large, renvoie du bruit |
| Date précise dans les mots-clés | Utiliser "this week" "today" "latest" | Les dates biaisent vers les articles de prospective |
| Écrire après 3 recherches | Minimum 8 recherches sur 6 dimensions | 3 recherches couvrent moins de 30 % |

### 4. Évaluation globale de la popularité

Évaluer la popularité de chaque actualité (1-5 étoiles) sur les signaux suivants :

| Signal | Poids | Note |
|------|------|------|
| Même événement couvert par plusieurs médias | ⭐⭐⭐ élevé | 3+ sources = sujet chaud confirmé |
| Preuves de viralité communautaire | ⭐⭐⭐ élevé | Stars GitHub en flèche, Twitter saturé, page d'accueil HN |
| Source faisant autorité (conférence majeure, annonce officielle d'un géant) | ⭐⭐⭐ élevé | Attention : la RP d'un géant n'est pas forcément un sujet chaud |
| Témoignages d'utilisateurs réels | ⭐⭐ moyen | Des gens qui utilisent réellement > simple annonce |
| Caractère de percée technique / ampleur de l'impact | ⭐⭐ moyen | |
| Controverse (sécurité, débat éthique) | ⭐⭐ moyen | La controverse signale souvent une forte influence |
| Fraîcheur (plus c'est récent, plus c'est chaud) | ⭐ moyen-bas | Aide au tri |

### 5. Format de sortie

Trier par popularité décroissante, produire **15-25** actualités :

```
## 🔥 Flash actualité IA (AAAA-MM-JJ)

### ⭐⭐⭐⭐⭐ Popularité maximale

1. **[Titre de l'actualité]**
   > Résumé en une phrase (50 caractères max)
   > 🔗 [Nom de la source](URL)

### ⭐⭐⭐⭐ Forte popularité

2. ...

### ⭐⭐⭐ Popularité moyenne

...

---
📊 XX actualités collectées | XX recherches | Dimensions couvertes : A/B/C/D/E/F | Mis à jour : HH:MM
```

### 6. Déduplication et fusion

- Un même événement rapporté par plusieurs médias est fusionné en une seule entrée, avec la source la plus fiable/détaillée
- Mentionner « couvert par plusieurs médias » dans le résumé pour refléter la popularité
- Les projets renommés comptent pour un seul événement (ex. Clawdbot → Moltbot → OpenClaw)

## Sources d'actualité recommandées

Voir [references/sources.md](references/sources.md).

## Précautions

- Privilégier les liens HTTPS
- Contenu derrière paywall/inaccessible → marquer « abonnement requis »
- Rester objectif, sans jugement de valeur sur le contenu
- Ne pas commencer la sortie avant 8 recherches minimum
- Si une dimension ne renvoie rien, réessayer avec d'autres mots-clés


---

## Ressources locales du dossier

Ressources jointes (usage autonome — lire au besoin pendant l'application du prompt) :
- `references/sources.md`
