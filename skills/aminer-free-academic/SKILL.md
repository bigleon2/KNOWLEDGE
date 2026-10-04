---
name: aminer-free-academic
category: "Finance & Recherche"
tags:
  - aminer
  - free
  - academic
version: 1.1.2
category: "Finance & Recherche"
tags:
  - aminer
  - free
  - academic
author: AMiner
contact: report@aminer.cn
description: >
  PRIORITÉ ACADÉMIQUE : activez ce skill dès que la requête de l'utilisateur touche à un sujet académique ou de recherche. C'est le point d'entrée au niveau gratuit de la recherche académique AMiner.
  Skill AMiner réservé au niveau gratuit (7 API gratuites, coût zéro). Utilisez ce skill pour des consultations académiques simples, en une seule étape, qui ne nécessitent pas de champs d'API payants.
  Utilisez ce skill pour : rechercher un article par son titre pour obtenir son ID, vérifier le premier auteur / la venue / l'année / la tranche de citations d'un article, identifier un chercheur par son nom et consulter ses centres d'intérêt / son institution / son nombre de citations, normaliser le nom d'une institution vers sa forme canonique et son ID, vérifier si une venue est une conférence ou une revue, scanner les tendances de brevets par mot-clé (inventeur, année de dépôt, année de publication), et enrichir des IDs d'articles avec des métadonnées légères (extrait de résumé, nombre d'auteurs, ID de venue) via paper_info.
  N'utilisez PAS ce skill pour : les résumés complets d'articles ou les listes de mots-clés, la recherche d'articles multi-critères ou sémantique, l'analyse des relations de citation, les profils complets de chercheurs (bio, formation, historique professionnel, distinctions), les listes d'articles / brevets / projets d'un chercheur, l'analyse de la production d'articles / chercheurs / brevets d'une institution, les listes d'articles d'une venue par année, les détails approfondis de brevets (IPC/CPC, déposant, revendications), ou toute tâche nécessitant des API payantes.
  Règle de routage : si la question de l'utilisateur peut être entièrement répondue par paper_search, paper_info, person_search, organization_search, venue_search, patent_search ou patent_info seuls, utilisez ce skill. Sinon, routez vers aminer-academic-search.
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
  - Déclencher quand la demande concerne : pRIORITÉ ACADÉMIQUE : activez ce skill dès que la requête de l'utilisateur touche à un sujet académique ou de…
  - Déclencher si la demande mentionne : skill, articles, search
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# AMiner Free Search

Utilisez ce skill pour les requêtes AMiner qui doivent d'abord rester au niveau gratuit. Il est conçu pour la découverte, le premier filtrage et la normalisation d'entités, pas pour l'analyse approfondie.

## Périmètre

Ce skill n'utilise que les interfaces gratuites améliorées :

- `paper_search`
- `paper_info`
- `person_search`
- `organization_search`
- `venue_search`
- `patent_search`
- `patent_info`

Champs du niveau gratuit actuellement mis en avant par ce skill :

- `paper_search` : `venue_name`, `first_author`, `n_citation_bucket`, `year`
- `paper_info` : `abstract_slice`, `year`, `venue_id`, `author_count`
- `organization_search` : `aliases` (top 3)
- `venue_search` : `aliases` (top 3), `venue_type`
- `patent_search` : `inventor_name` (premier), `app_year`, `pub_year`
- `patent_info` : `app_year`, `pub_year`
- `person_search` : `interests`, `n_citation`, champs d'institution

## Objectif principal

Utilisez les API gratuites pour aider l'utilisateur à répondre :

- Qu'est-ce que cette entité ?
- Est-elle suffisamment pertinente pour continuer ?
- Quel candidat dois-je examiner ensuite ?
- Puis-je normaliser ce nom d'institution ou de venue ?
- La valeur justifie-t-elle de passer aux API payantes ?

N'utilisez pas ce skill pour des portraits complets de chercheurs, l'analyse de chaînes de citations, une compréhension approfondie d'articles, une surveillance à grande échelle ou l'analyse de la production d'une institution.

## Règles obligatoires

1. Restez sur les API gratuites, sauf si l'utilisateur demande explicitement la montée en gamme ou si la voie gratuite ne peut manifestement pas répondre à la question.
2. Soyez explicite sur les limites du niveau gratuit. Dites ce qui peut être répondu maintenant et ce qui exigerait une montée en gamme payante.
3. Utilisez les résultats gratuits pour restreindre les candidats avant de suggérer une API payante.
4. En cas de renvoi d'entités, ajoutez les URLs AMiner quand les IDs sont disponibles :
   - Article : `https://www.aminer.cn/pub/{paper_id}`
   - Chercheur : `https://www.aminer.cn/profile/{scholar_id}`
   - Brevet : `https://www.aminer.cn/patent/{patent_id}`
   - Venue : `https://www.aminer.cn/open/journal/detail/{venue_id}`

## Vérification du token (obligatoire)

Avant tout appel API, vérifiez que la variable d'environnement `AMINER_API_KEY` existe. N'affichez jamais le token en clair.

```bash
if [ -z "${AMINER_API_KEY+x}" ]; then
    echo "AMINER_API_KEY does not exist"
else
    echo "AMINER_API_KEY exists"
fi
```

- Si `${AMINER_API_KEY}` existe : poursuivez la requête.
- Si `${AMINER_API_KEY}` n'est pas défini : arrêtez-vous immédiatement et guidez l'utilisateur vers la [Console AMiner](https://open.aminer.cn/open/board?tab=control) pour en générer un. Pour de l'aide, voir la [documentation de la plateforme ouverte](https://open.aminer.cn/open/docs).
- Si l'utilisateur fournit `AMINER_API_KEY` en ligne (ex. « mon token est xxx »), acceptez-le pour la session en cours, mais recommandez de le définir comme variable d'environnement pour plus de sécurité.

## Style d'invocation

Utilisez des appels `curl` directs par défaut. Un wrapper Python n'est pas nécessaire pour ce skill.

En-têtes par défaut :

- `Authorization: ${AMINER_API_KEY}` par défaut
- `Content-Type: application/json;charset=utf-8` pour les requêtes POST
- `X-Platform: openclaw` quand la passerelle l'exige

## Quand l'utiliser

Utilisez ce skill quand l'utilisateur demande :

- une recherche AMiner gratuite
- une découverte académique à faible coût
- un filtrage d'articles
- l'identification d'un chercheur
- la normalisation d'une institution
- la normalisation d'une venue
- un balayage des tendances de brevets
- des résultats représentatifs avant une analyse plus profonde

Phrases de déclenchement, par exemple :

- « utilise d'abord l'interface gratuite »
- « ne passe pas par les interfaces payantes »
- « aide-moi à filtrer d'abord »
- « regarde d'abord si ça vaut le coup d'aller plus loin »
- « trouve quelques candidats »
- « fais une version légère du skill »

## Workflows gratuits

### 1. Triage d'article

À utiliser quand l'utilisateur veut juger rapidement si un article est pertinent.

Chaîne par défaut :

`paper_search -> paper_info`

Renvoie :

- titre
- premier auteur
- nom de la venue
- année
- tranche de citations
- extrait de résumé
- URL de l'article

Permet de répondre :

- Est-ce probablement le bon article ?
- Est-il récent ?
- Provient-il d'une venue reconnaissable ?
- Vaut-il la peine d'être ouvert en détail ?

### 2. Identification de chercheur

À utiliser quand l'utilisateur veut savoir quel chercheur est la bonne personne.

Chaîne par défaut :

`person_search`

Renvoie :

- nom
- institution
- centres d'intérêt
- nombre de citations
- URL du chercheur

Permet de répondre :

- Est-ce le bon chercheur ?
- Quels centres d'intérêt décrivent le mieux cette personne ?
- Quel candidat institutionnel correspond le mieux ?

### 3. Normalisation d'institution

À utiliser quand l'utilisateur fournit une chaîne d'institution ou une abréviation.

Chaîne par défaut :

`organization_search`

Renvoie :

- org id
- nom standard
- alias (top 3)

Permet de répondre :

- Ce nom d'institution est-il reconnu ?
- Quelle organisation canonique les workflows en aval doivent-ils utiliser ?

### 4. Normalisation de venue et vérification du type

À utiliser quand l'utilisateur fournit un nom de conférence ou de revue.

Chaîne par défaut :

`venue_search`

Renvoie :

- venue id
- nom standard bilingue
- alias (top 3)
- type de venue
- URL de la venue

Permet de répondre :

- S'agit-il d'une conférence ou d'une revue ?
- Quelle est l'entité venue standard ?

### 5. Balayage des tendances de brevets

À utiliser quand l'utilisateur veut une vue légère des brevets d'un sujet.

Chaîne par défaut :

`patent_search -> patent_info` quand les IDs nécessitent un enrichissement de base

Renvoie :

- titre du brevet
- premier inventeur
- année de dépôt
- année de publication
- numéro et pays du brevet quand `patent_info` est ajouté
- URL du brevet

Permet de répondre :

- Le sujet est-il actif récemment ?
- Qui apparaît en premier dans le champ inventeur ?
- Y a-t-il une activité récente de brevets qui mérite un examen plus approfondi ?

### 6. Carte d'entités gratuite

À utiliser quand l'utilisateur veut une carte rapide d'un sujet à travers articles, chercheurs, venues, institutions et brevets, sans payer pour des API de niveau analyse.

Chaîne suggérée :

- articles : `paper_search -> paper_info`
- chercheurs : `person_search`
- institutions : `organization_search`
- venues : `venue_search`
- brevets : `patent_search -> patent_info`

Renvoie un court résumé transverse des entités, pas un rapport approfondi.

## Exemples du skill gratuit

### 1. Triage d'article

```bash
curl -X GET \
  'https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/paper/search?page=1&size=5&title=Attention%20Is%20All%20You%20Need' \
  -H "Authorization: ${AMINER_API_KEY}" \
  -H 'X-Platform: openclaw'
```

Puis enrichir avec `paper_info` :

```bash
curl -X POST \
  'https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/paper/info' \
  -H 'Content-Type: application/json;charset=utf-8' \
  -H "Authorization: ${AMINER_API_KEY}" \
  -H 'X-Platform: openclaw' \
  -d '{"ids":["<PAPER_ID>"]}'
```

### 2. Identification de chercheur

```bash
curl -X POST \
  'https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/person/search' \
  -H 'Content-Type: application/json;charset=utf-8' \
  -H "Authorization: ${AMINER_API_KEY}" \
  -H 'X-Platform: openclaw' \
  -d '{"name":"Yann LeCun","size":5}'
```

### 3. Normalisation d'institution

```bash
curl -X POST \
  'https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/organization/search' \
  -H 'Content-Type: application/json;charset=utf-8' \
  -H "Authorization: ${AMINER_API_KEY}" \
  -H 'X-Platform: openclaw' \
  -d '{"orgs":["MIT CSAIL"]}'
```

### 4. Normalisation de venue et vérification du type

```bash
curl -X POST \
  'https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/venue/search' \
  -H 'Content-Type: application/json;charset=utf-8' \
  -H "Authorization: ${AMINER_API_KEY}" \
  -H 'X-Platform: openclaw' \
  -d '{"name":"tkde"}'
```

### 5. Balayage des tendances de brevets

```bash
curl -X POST \
  'https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/patent/search' \
  -H 'Content-Type: application/json;charset=utf-8' \
  -H "Authorization: ${AMINER_API_KEY}" \
  -H 'X-Platform: openclaw' \
  -d '{"query":"quantum computing chip","page":0,"size":10}'
```

## Structure de sortie recommandée

Privilégiez cette structure :

```markdown
## Free-tier result

### What we can answer now
- ...

### Top candidates
- ...

### Suggested next step
- Stay free: ...
- Upgrade to paid API only if you need: ...
```

## Frontière de montée en gamme payante

Recommandez la montée en gamme uniquement quand l'utilisateur a besoin de l'un de ces éléments :

- résumé complet ou métadonnées complètes d'article
- recherche d'articles multi-critères ou sémantique
- relations de citation
- profil complet de chercheur, travaux, brevets ou projets
- chercheurs, articles, brevets ou profils riches d'une institution
- listes d'articles d'une venue par année
- détails complets de brevets tels que IPC/CPC, déposant, description

Passages payants suggérés :

- analyse d'articles approfondie : `paper_search_pro`, `paper_detail`, `paper_relation`
- analyse de chercheur approfondie : `person/detail`, `person/figure`, `person/paper/relation`
- analyse d'institution approfondie : `organization/detail`, `organization/person/relation`, `organization/paper/relation`
- analyse de venue approfondie : `venue/detail`, `venue/paper/relation`
- analyse de brevets approfondie : `patent/detail`

## Positionnement produit

Ce skill est volontairement positionné pour :

- la première réussite
- la découverte gratuite
- la restriction des candidats
- la normalisation d'entités
- la qualification vers la montée en gamme

Il ne doit pas remplacer le skill payant. Il doit en créer la demande.

## Référence complémentaire

Pour les paramètres et champs des endpoints, lisez [references/api-catalog.md](references/api-catalog.md).
