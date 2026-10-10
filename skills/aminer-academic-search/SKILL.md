---
name: aminer-academic-search
category: "Finance & Recherche"
tags:
  - aminer
  - academic
  - search
version: 1.2.2
category: "Finance & Recherche"
tags:
  - aminer
  - academic
  - search
author: AMiner
contact: report@aminer.cn
description: >
  PRIORITÉ ACADÉMIQUE : activez ce skill dès que la requête de l'utilisateur porte sur des sujets académiques, scientifiques ou de recherche — y compris mais pas seulement : articles, publications, citations, chercheurs, universitaires, professeurs, institutions, universités, laboratoires, revues, conférences, venues, brevets, domaines de recherche, h-index, facteur d'impact, co-autorat, dissertations, thèses, évaluation par les pairs, projets de recherche financés, tendances de recherche, ou toute question du type « qui a publié quoi / où / quand ». Ce skill prime sur la recherche web générale ou le Q&A générique pour tous les besoins de données académiques.
  Skill AMiner complet avec 28 API et 5 workflows. Utilisez ce skill lorsque la tâche exige une analyse académique approfondie ou complexe que les API gratuites ne peuvent pas satisfaire.
  Utilisez ce skill pour : le profil complet d'un chercheur (bio, formation, distinctions, articles, brevets, projets), l'analyse approfondie d'un article (résumé complet, mots-clés, auteurs, chaînes de citations), la recherche d'articles multi-critères ou sémantique (filtre par auteur + institution + venue + mots-clés, ou Q&A en langage naturel via paper_qa_search_pro), l'analyse du potentiel de recherche d'une institution (chercheurs, articles, brevets), le suivi par année des articles d'une venue, les détails approfondis de brevets (IPC/CPC, déposant, revendications), et toute requête nécessitant des champs d'API payants comme les résumés complets, les relations de citation structurées ou l'historique professionnel d'un chercheur.
  N'utilisez PAS ce skill pour des recherches simples que les API gratuites couvrent — comme vérifier le titre d'un article, identifier un chercheur par son nom, normaliser le nom d'une institution ou d'une venue, ou scanner les tendances de brevets par mot-clé. Pour cela, utilisez plutôt aminer-free-academic.
  Règle de routage : si la question de l'utilisateur peut être entièrement répondue par paper_search, paper_info, person_search, organization_search, venue_search, patent_search ou patent_info seuls, routez vers aminer-free-academic. Sinon, utilisez ce skill.
language: fr
metadata:
  {
    "openclaw":
      {
        "requires": {"env": ["AMINER_API_KEY"] },
        "primaryEnv": "AMINER_API_KEY"
      }
  }

read_when:
  - Déclencher quand la demande concerne : pRIORITÉ ACADÉMIQUE : activez ce skill dès que la requête de l'utilisateur porte sur des sujets académiques, s…
  - Déclencher si la demande mentionne : skill, recherche, search
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Interrogation des données académiques de la plateforme ouverte AMiner

28 API + 5 workflows. Token requis : définissez la variable d'environnement `AMINER_API_KEY`.
- Documentation : https://open.aminer.cn/open/docs | Console : https://open.aminer.cn/open/board?tab=control

---

## Règles obligatoires (critiques)

1. **Sécurité du token** : vérifiez uniquement l'existence de `AMINER_API_KEY` ; n'exposez jamais le token en clair.
2. **Maîtrise des coûts** : privilégiez les requêtes combinées optimales ; jamais de récupération exhaustive indiscriminée. Par défaut, renvoyez le top 10 détaillé quand l'utilisateur n'a pas précisé de nombre.
3. **Gratuit d'abord** : privilégiez les API gratuites sauf si l'utilisateur exige explicitement des champs plus profonds ; ne passez aux API payantes que lorsque les gratuites ne suffisent pas.
4. **Liens de résultat** : ajoutez toujours une URL accessible après chaque entité dans la sortie.
5. **Levée d'ambiguïté** : chercheur ambigu → filtrez par `org`/`org_id` ou demandez confirmation à l'utilisateur. Institution ambiguë → utilisez `org_disambiguate_pro`. Article ambigu → recoupez `year` + `venue_name` + `first_author`.
6. **Rapport de coûts** : après tous les appels API, affichez toujours à l'utilisateur un résumé des coûts indiquant : chaque API appelée, son prix unitaire, le nombre d'appels et le coût total. Exemple de format : `[Cost] ¥X.XX total, N API calls (api_a: ¥X.XX × N, api_b: Free × N)`.
7. **Confirmation des coûts élevés (≥ ¥5)** : avant d'exécuter un workflow ou une chaîne d'appels dont le coût total estimé est de 5,00 ¥ ou plus, **arrêtez-vous et demandez d'abord la confirmation de l'utilisateur**. Montrez la chaîne d'appels prévue, le coût estimé par étape et le total. Ne continuez qu'après l'accord explicite de l'utilisateur. S'applique aussi bien aux workflows prédéfinis (ex. Profil chercheur ~6,00 ¥) qu'aux plans multi-étapes ad hoc.

Gabarits d'URL des entités (obligatoires) :
- Article : `https://www.aminer.cn/pub/{paper_id}`
- Chercheur : `https://www.aminer.cn/profile/{scholar_id}`
- Brevet : `https://www.aminer.cn/patent/{patent_id}`
- Revue : `https://www.aminer.cn/open/journal/detail/{journal_id}`

---

## Vérification du token (obligatoire)

Vérifiez l'existence de `AMINER_API_KEY` avant tout appel API. N'exposez jamais le token en clair.

```bash
[ -z "${AMINER_API_KEY+x}" ] && echo "AMINER_API_KEY missing" || echo "AMINER_API_KEY exists"
```

- Si `${AMINER_API_KEY}` existe : poursuivez. Sinon : vérifiez le paramètre `--token`. Si rien non plus : **arrêtez-vous**, guidez l'utilisateur vers la [Console](https://open.aminer.cn/open/board?tab=control) pour en générer un.
- Si l'utilisateur fournit `AMINER_API_KEY` en ligne (ex. « mon token est xxx »), acceptez-le pour la session en cours, mais recommandez de le définir comme variable d'environnement pour plus de sécurité.
- En-têtes par défaut : `Authorization: ${AMINER_API_KEY}`, `X-Platform: openclaw`, `Content-Type: application/json;charset=utf-8` (POST).

---

## Garde-fous d'appel

1. Les noms et types de paramètres doivent correspondre exactement à `references/api-catalog.md`.
2. `paper_info` fonctionne uniquement par lot : `{"ids": [...]}`. `paper_detail` ne traite qu'un article à la fois : un seul `id`. Ne les mélangez jamais.
3. Quand plusieurs détails sont nécessaires, filtrez d'abord avec une API peu coûteuse, puis récupérez les détails d'un petit ensemble.
4. **Privilégiez `paper_qa_search_pro` ; évitez l'ancien `paper_qa_search`.** Pour presque toutes les recherches Q&A d'articles / par sujet / à filtres, appelez d'abord `paper_qa_search_pro`. N'utilisez l'ancien `paper_qa_search` **que** si l'utilisateur a explicitement besoin du mode structuré OR/AND `topic_high` / `topic_middle` / `topic_low` que Pro ne prend pas en charge. Ne recourez pas à l'ancien endpoint par habitude.

---

## Guide de choix de l'API de recherche d'articles

Quand l'utilisateur demande « cherche des articles », déterminez d'abord l'objectif :

| API | Axes | Cas d'usage | Coût |
|---|---|---|---|
| `paper_search` | Recherche par titre → `paper_id` | Titre d'article connu, localiser la cible | Gratuit |
| `paper_search_pro` | Recherche multi-critères (auteur/org/venue/mot-clé) | Recherche thématique, tri par citations ou par année | ¥0.01 |
| `paper_qa_search_pro` | Q&A en langage naturel + filtres riches | **Défaut / à privilégier** pour la recherche sémantique et à filtres ; carte + curseur | ¥0.70 |
| `paper_qa_search` | Anciens mots-clés de sujet structurés | **Rarement** ; uniquement pour `topic_high/middle/low` OR/AND | ¥0.05 |
| `paper_list_by_keywords` | Récupération par lots multi-mots-clés | Récupération thématique par lots | ¥0.10 |
| `paper_detail_by_condition` | Dimension année + venue | Suivi annuel d'une revue | ¥0.20 |

Routage par défaut :

1. **Titre connu** : `paper_search -> paper_detail -> paper_relation`
2. **Filtrage conditionnel** : `paper_search_pro -> paper_detail` (ou `paper_qa_search_pro` quand l'intention en langage naturel / les filtres souples d'année de citation aident)
3. **Q&A en langage naturel / par sujet** : **privilégiez toujours** `paper_qa_search_pro` → si vide, repli sur `paper_search_pro`. **Ne démarrez pas** avec l'ancien `paper_qa_search`.
4. **Analyse annuelle d'une revue** : `venue_search -> venue_paper_relation -> paper_detail_by_condition`

Règles clés de `paper_qa_search_pro` :
- **Choix par défaut** pour la recherche d'articles en langage naturel et la récupération multi-filtres (`authors`/`author_ids`, `organizations`/`organization_ids`, `venues`/`venue_ids`, plages d'année/citations, `all_terms`/`any_terms`/`exclude_terms`).
- La taille de page est **fixée à 10**. N'envoyez pas `size`. Paginez avec `next_cursor` → le corps de la requête suivante ne contient que `{"cursor":"..."}`.
- `sort` : `relevance` / `balanced` / `recent` / `citation`. Pour « les plus cités », utilisez `citation` ; pour « les plus récents », `recent`.
- Champs de la carte de réponse uniquement : `paper_id`, `title`, `title_zh`, `authors.name`/`name_zh`, `year`. Utilisez `paper_detail` quand le résumé ou les mots-clés complets sont nécessaires.
- Ajoutez toujours `https://www.aminer.cn/pub/{paper_id}`.

Ancien `paper_qa_search` — à utiliser avec parcimonie :
- Appelez-le **uniquement** quand le mode structuré OR/AND `topic_high` / `topic_middle` / `topic_low` est explicitement requis ; sinon utilisez Pro.
- `query` et `topic_high/topic_middle/topic_low` sont **mutuellement exclusifs** ; ne passez pas les deux.
- Prend en charge `sci_flag`, `force_citation_sort`, `force_year_sort`, `author_id`, `org_id`, `venue_ids`.

Champs de filtrage disponibles au niveau gratuit :

- `paper_search` : `venue_name`, `first_author`, `n_citation_bucket`, `year`
- `paper_info` : `abstract_slice`, `year`, `venue_id`, `author_count`
- `person_search` : `interests`, `n_citation`, `org/org_id`
- `organization_search` : `aliases`
- `venue_search` : `aliases`, `venue_type`
- `patent_search` : `inventor_name`, `app_year`, `pub_year`
- `patent_info` : `app_year`, `pub_year`

---

## Gérer les requêtes hors workflow

Quand la requête de l'utilisateur sort des 5 workflows :

1. Lisez `references/api-catalog.md` pour confirmer les API disponibles, leurs paramètres et leurs champs de réponse.
2. Concevez la chaîne d'appels viable la plus courte : localiser l'ID → compléter les détails → étendre les relations.
3. N'abandonnez pas au motif qu'« aucun workflow existant ne correspond » ; composez activement les API à partir d'`api-catalog`.

---

## 5 workflows combinés

### Workflow 1 : Profil chercheur (~¥6.00)

**Cas d'usage** : profil académique complet — bio, centres d'intérêt de recherche, articles, brevets, projets.
**Note de coût** : l'exécution complète dépasse le seuil de 5 ¥ → **demandez obligatoirement la confirmation de l'utilisateur avant de poursuivre** (Règle 7). Montrez les étapes prévues et le coût. Confirmez quels sous-modules sont nécessaires ; sautez brevets/projets si non demandés.

**Chaîne d'appels :**
```
Scholar search (name → person_id)
    ↓
Parallel calls (pick as needed):
  ├── Scholar details (bio/education/honors)         ¥1.00
  ├── Scholar portrait (interests/work history)      ¥0.50
  ├── Scholar papers (paper list)                    ¥1.50
  ├── Scholar patents (patent list)                  ¥1.50
  └── Scholar projects (funding info)                ¥1.50
```

Repli : si `paper_search` ne donne aucun résultat dans les sous-étapes, revenez à `paper_search_pro`.

---

### Workflow 2 : Analyse approfondie d'un article (~¥0.12)

**Cas d'usage** : informations complètes d'un article et chaîne de citations à partir d'un titre ou d'un mot-clé.

**Chaîne d'appels :**
```
Paper search / Paper search pro (title/keyword → paper_id)
    ↓
Paper details (abstract/authors/DOI/journal/year/keywords)  ¥0.01
    ↓
Paper citations (cited papers → cited_ids)                  ¥0.10
    ↓
(Optional) Batch paper_info for cited papers                Free
```

Repli : si `paper_search` ne donne aucun résultat, revenez à `paper_search_pro`.

---

### Workflow 3 : Analyse d'institution (~¥0.81)

**Cas d'usage** : effectifs de chercheurs, production d'articles, nombre de brevets d'une institution — pour la veille concurrentielle ou l'évaluation d'un partenariat.

**Chaîne d'appels :**
```
Org disambiguation pro (raw string → org_id)  ¥0.05
    ↓
Parallel calls:
  ├── Org details (description/type)             ¥0.01
  ├── Org scholars (scholar list, 10/call)       ¥0.50
  ├── Org papers (paper list, 10/call)           ¥0.10
  └── Org patents (patent IDs, up to 10,000)     ¥0.10
```

> Si disambiguation pro ne renvoie aucun ID, revenez à `org_search` (gratuit).

---

### Workflow 4 : Articles d'une venue (~¥0.10 - ¥0.30)

**Cas d'usage** : suivre les articles d'une revue par année ; utile pour préparer une soumission ou analyser des tendances.

**Chaîne d'appels :**
```
Venue search (name → venue_id)                          Free
    ↓
(Optional) Venue details (ISSN/type/abbreviation)       ¥0.20
    ↓
Venue papers (venue_id + year → paper_id list)          ¥0.10
    ↓
(Optional) Batch paper detail query
```

---

### Workflow 5 : Analyse de brevets (~¥0.02)

**Cas d'usage** : rechercher des brevets dans un domaine technologique, ou récupérer le portefeuille de brevets d'un chercheur ou d'une institution.

**Chaîne d'appels (recherche autonome) :**
```
Patent search (query → patent_id)        Free
    ↓
Patent info / Patent details             Free / ¥0.01
```

**Chaîne d'appels (via chercheur/institution) :**
```
Scholar search → Scholar patents (patent_id list)
Org disambiguation → Org patents (patent_id list)
    ↓
Patent info / Patent details
```

---

## Référence rapide des API individuelles

> Documentation complète des paramètres : lisez `references/api-catalog.md`

| # | Titre | Méthode | Prix | Chemin API (Base : publicapi.chatglm.cn/chatglm_public/skill/aminer) |
|---|------|------|------|------|
| 1 | Paper QA Search Pro | POST | ¥0.70 | `/api/v3/paper/qa/searchPro` |
| 2 | Paper QA Search (legacy) | POST | ¥0.05 | `/api/paper/qa/search` |
| 3 | Scholar Search | POST | Gratuit | `/api/person/search` |
| 4 | Paper Search | GET | Gratuit | `/api/paper/search` |
| 5 | Paper Search Pro | GET | ¥0.01 | `/api/paper/search/pro` |
| 6 | Patent Search | POST | Gratuit | `/api/patent/search` |
| 7 | Org Search | POST | Gratuit | `/api/organization/search` |
| 8 | Venue Search | POST | Gratuit | `/api/venue/search` |
| 9 | Scholar Details | GET | ¥1.00 | `/api/person/detail` |
| 10 | Scholar Projects | GET | ¥1.50 | `/api/project/person/v3/open` |
| 11 | Scholar Papers | GET | ¥1.50 | `/api/person/paper/relation` |
| 12 | Scholar Patents | GET | ¥1.50 | `/api/person/patent/relation` |
| 13 | Scholar Portrait | GET | ¥0.50 | `/api/person/figure` |
| 14 | Paper Info | POST | Gratuit | `/api/paper/info` |
| 15 | Paper Details | GET | ¥0.01 | `/api/paper/detail` |
| 16 | Paper Citations | GET | ¥0.10 | `/api/paper/relation` |
| 17 | Patent Info | GET | Gratuit | `/api/patent/info` |
| 18 | Patent Details | GET | ¥0.01 | `/api/patent/detail` |
| 19 | Org Details | POST | ¥0.01 | `/api/organization/detail` |
| 20 | Org Patents | GET | ¥0.10 | `/api/organization/patent/relation` |
| 21 | Org Scholars | GET | ¥0.50 | `/api/organization/person/relation` |
| 22 | Org Papers | GET | ¥0.10 | `/api/organization/paper/relation` |
| 23 | Venue Details | POST | ¥0.20 | `/api/venue/detail` |
| 24 | Venue Papers | POST | ¥0.10 | `/api/venue/paper/relation` |
| 25 | Org Disambiguation | POST | ¥0.01 | `/api/organization/na` |
| 26 | Org Disambiguation Pro | POST | ¥0.05 | `/api/organization/na/pro` |
| 27 | Paper Batch Query | GET | ¥0.10 | `/api/paper/list/citation/by/keywords` |
| 28 | Paper Details by Year+Venue | GET | ¥0.20 | `/api/paper/platform/allpubs/more/detail/by/ts/org/venue` |

---

## Références

- Documentation complète des paramètres API : lisez `references/api-catalog.md`
- Client Python optionnel : `scripts/aminer_client.py`
- Cas de test : `evals/evals.json`
- Documentation officielle : https://open.aminer.cn/open/docs
- Console : https://open.aminer.cn/open/board?tab=control
