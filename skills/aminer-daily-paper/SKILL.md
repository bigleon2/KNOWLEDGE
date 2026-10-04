---
name: aminer-daily-paper
category: "Finance & Recherche"
tags:
  - aminer
  - daily
  - paper
version: 1.1.3
category: "Finance & Recherche"
tags:
  - aminer
  - daily
  - paper
description: "Recommandation personnalisée d'articles académiques via l'API rec5 d'AMiner. Activez ce skill dès que l'utilisateur demande des recommandations d'articles, que ce soit via /aminer-dp, /skill aminer-dp, ou toute demande en langage naturel comme « recommande-moi des articles sur les agents multimodaux ». À l'invocation : extrayez vous-même les sujets/signaux de chercheur de l'entrée, appelez handle_trigger.py avec les champs structurés, puis présentez le Markdown de `reply_text` à l'utilisateur."
language: fr
user-invocable: true
disable-model-invocation: false
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": {
          "bins": ["python3"],
          "env": ["AMINER_API_KEY"]
        },
        "primaryEnv": "AMINER_API_KEY"
      }
  }

read_when:
  - Déclencher quand la demande concerne : "Recommandation personnalisée d'articles académiques via l'API rec5 d'AMiner
  - Déclencher si la demande mentionne : articles, aminer, skill
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# aminer-daily-paper

Recommandation personnalisée d'articles via l'API rec5 d'AMiner. Token requis : définissez la variable d'environnement `AMINER_API_KEY`.
- Documentation : https://open.aminer.cn/open/docs | Console : https://open.aminer.cn/open/board?tab=control

**Quand l'activer** : chaque fois que l'utilisateur demande des recommandations d'articles — commande explicite (`/aminer-dp ...`) ou langage naturel (« recommande-moi des articles récents sur le RAG », « 帮我推荐最近的多模态论文 »).

---

## Pré-vol : vérifier les variables d'environnement requises

**`AMINER_API_KEY`** — toujours requis. Vérifiez avant d'appeler le script :

```bash
[ -z "${AMINER_API_KEY+x}" ] && echo "AMINER_API_KEY missing" || echo "AMINER_API_KEY exists"
```

Si absent, arrêtez-vous et dites à l'utilisateur :
> `AMINER_API_KEY` n'est pas défini. Merci d'obtenir un token sur https://open.aminer.cn et de le définir comme variable d'environnement.

Aucune autre variable d'environnement n'est requise.

---

## Point d'accès API

```
POST https://publicapi.chatglm.cn/chatglm_public/skill/aminer/api/v3/paper/rec5
Authorization: ${AMINER_API_KEY}
Content-Type: application/json;charset=utf-8
```

### Champs de la requête

| Champ | Type | Requis | Description |
|-------|------|----------|-------------|
| `author_name` | string | conditionnel | Nom du chercheur (en anglais). Le backend le résout en ID de chercheur via une recherche de personne. |
| `author_org` | string | optionnel | Institution du chercheur (nom complet en anglais). Requis pour la levée d'ambiguïté quand le nom est ambigu. |
| `topics` | string[] | conditionnel | Phrases de sujets de recherche. **Utilisez les mots de l'utilisateur** (français, chinois, anglais ou mixte). L'API accepte des chaînes de sujets multilingues. |
| `size` | int | optionnel | Nombre d'articles par appel (1–20). Omettez pour laisser le modèle décider (voir ci-dessous). |
| `offset` | int | optionnel | Décalage de pagination (0–100, défaut 0). |
| `language_sort` | string | optionnel | `zh` ou `en` **uniquement si l'utilisateur demande explicitement** un classement à dominante chinoise ou anglaise (ex. « 优先中文论文 » / « prefer English papers »). Sinon, omettez ; la requête ne contiendra pas ce champ. |

Au moins un des champs `author_name` ou `topics` doit être fourni. Quand aucun n'est donné, l'API renvoie des recommandations personnalisées basées sur le compte associé à `AMINER_API_KEY`.

### Structure de la réponse

```json
{
  "code": 200,
  "success": true,
  "data": [{
    "offset": 0,
    "size": 5,
    "total": 32,
    "papers": [{
      "paper_id": "...",
      "arxiv_id": "",
      "title": "...",
      "year": 2026,
      "authors": ["Author A", "Author B"],
      "keywords": ["kw1", "kw2"],
      "summary": "...",
      "structured_summary": {
        "research_problem": "...",
        "research_challenge": "...",
        "research_method": "...",
        "experimental_results": ""
      },
      "famous_authors": [],
      "aminer_author_profiles": [],
      "author_entries": [],
      "links": {
        "aminer": "https://www.aminer.cn/pub/{paper_id}",
        "arxiv": "",
        "pdf": ""
      },
      "paper_url": "https://www.aminer.cn/pub/{paper_id}",
      "source": "local_rec5"
    }]
  }]
}
```

---

## Formats d'entrée

Commandes structurées ou langage naturel simple — les deux sont valides.

```
/aminer-dp
/aminer-dp topics: multimodal agents, tool-use
/aminer-dp scholar: Jie Tang org: Tsinghua papers: OAG-Bench | RPC-Bench
recommend me recent papers on RAG
```

`/aminer-dp` sans paramètre appelle l'API avec le seul token — l'API utilise `AMINER_API_KEY` pour identifier le compte et renvoie des recommandations personnalisées.

**Entrée en langage naturel** — vous (le modèle) devez la décoder en champs avant d'appeler le script. **Critique pour `topics` :**

1. **`topics` — ne « traduisez pas » l'intention de l'utilisateur**
   - Si l'utilisateur a déjà écrit `topics:` dans le déclencheur (ex. `具身智能`, `环境保护`), passez **ces chaînes exactes** au `--text` de `handle_trigger.py`. **Ne les remplacez pas** par des termes anglais sans rapport (ex. ne mappez **pas** des sujets arbitraires vers « Knowledge Distillation », « Smart agriculture » ou tout autre domaine non demandé par l'utilisateur).
   - Si vous ajoutez de l'anglais pour la recherche, ce doit être un alias **fidèle** du même concept (ex. 具身智能 → `embodied intelligence`, 环境保护 → `environmental protection`). En cas de doute, **conservez les mots originaux de l'utilisateur** et n'inventez pas de synonymes.
   - **Ne changez jamais** le sujet de l'utilisateur vers un autre domaine de recherche.

2. **Chercheurs et institutions (la recherche de personnes reste orientée anglais)**
   - `author_name` / `author_org` : utilisez les formes **anglaises** usuelles pour résoudre les chercheurs (ex. `Jie Tang`, `Tsinghua University`), développez les abréviations d'institutions connues en noms officiels complets, et ajoutez `author_org` quand le nom est ambigu. Si vous ne pouvez pas établir une correspondance sûre, demandez à l'utilisateur.

3. **`language_sort`** — mettez `language_sort: zh` ou `language_sort: en` dans le déclencheur **uniquement si** l'utilisateur veut clairement des recommandations classées avec une préférence **chinoise** ou **anglaise**. S'il ne l'a pas demandé, **ne l'ajoutez pas** (l'appel API omet `language_sort`).

4. Décidez de `size` et de la nécessité de plusieurs appels (voir **Stratégie d'appel**).
5. Reconstruisez le déclencheur, puis appelez `handle_trigger.py`.

Exemple (sujets en chinois — **conserver tels quels**) :
- Utilisateur : `/aminer-dp topics: 具身智能, 环境保护`
- Vous appelez : `handle_trigger.py --text "/aminer-dp topics: 具身智能, 环境保护"`  
  (Ne réécrivez **pas** `topics` en anglais sans rapport.)

Exemple :
- Utilisateur : `/aminer-dp je travaille sur les agents multimodaux et le tool-use, recommande-moi des articles récents`
- Vous extrayez : `topics: multimodal agents, tool-use`
- Vous appelez : `handle_trigger.py --text "/aminer-dp topics: multimodal agents, tool-use size: 5"`

Exemple (chercheur) :
- Utilisateur : `/aminer-dp je suis Tang Jie, de Tsinghua, je travaille sur le multimodal et les graphes de connaissances`
- Vous extrayez : `scholar: Jie Tang, org: Tsinghua University, topics: multimodal, knowledge graph`
- Vous appelez : `handle_trigger.py --text "/aminer-dp scholar: Jie Tang org: Tsinghua University topics: multimodal, knowledge graph"`

Exemple (nom ambigu, demander à l'utilisateur) :
- Utilisateur : `/aminer-dp recommande des articles du domaine de 张伟`
- Vous : « 张伟 est un nom très courant ; merci d'indiquer l'institution pour une correspondance précise, par exemple : 张伟, Université de Pékin. Vous pouvez aussi fournir directement un aminer_author_id. »

**Champ `papers`** : les titres d'articles représentatifs (ex. `papers: OAG-Bench | RPC-Bench`) accompagnent `scholar`/`author_name` comme contexte de levée d'ambiguïté. Ils ne correspondent pas directement à un champ de l'API.

---

## Stratégie d'appel

Vous décidez de `size` et de la nécessité de plusieurs appels selon l'entrée :

| Scénario | Action |
|----------|--------|
| Sujet unique ou chercheur unique, demande ponctuelle | 1 appel, omettre `size` (défaut 10) |
| L'utilisateur demande explicitement un nombre (ex. « donne-m'en 5 ») | 1 appel, respecter le nombre (max 20) |
| Plusieurs sujets distincts (ex. RAG + agents multimodaux) | 1 appel par groupe de sujets, `size: 5` chacun |
| Demande large ouverte sans sujets | 1 appel, omettre `size` (défaut 10) |

**Règles multi-appels :**
- Appelez `handle_trigger.py` une fois par groupe de sujets, en passant à chaque fois un sous-ensemble `topics:` ciblé.
- Limitez chaque liste `topics:` à 1–3 termes étroitement liés pour la précision.
- Faites les appels séquentiellement ; présentez tous les résultats ensemble une fois tous les appels terminés.
- Le total d'articles sur tous les appels ne doit pas dépasser ~15, sauf demande contraire de l'utilisateur.

---

## Exécution

Un seul point d'entrée pris en charge :

```bash
python3 "{baseDir}/scripts/handle_trigger.py" \
  --base-dir "{baseDir}" \
  --text "<trigger text with explicit fields>" \
  [--config /path/to/config.yaml]
```

- `--text` : déclencheur reconstruit avec les champs explicites (`topics:`, `scholar:`, etc.)
- `--config` : chemin optionnel vers une config YAML (par défaut `{baseDir}/config.yaml` si le fichier existe, via la copie d'exécution sous `outputs/`)

`handle_trigger.py` analyse les champs, appelle l'API rec5 et renvoie un JSON incluant `reply_text` (Markdown) à présenter à l'utilisateur.

---

## Contrat

- Chaque invocation explicite est une nouvelle exécution.
- Ne répondez pas par un simple texte d'état.
- Ne cherchez, n'installez et ne réparez pas de skills.
- Après l'exécution de `handle_trigger.py`, vérifiez `final_response` dans la sortie JSON :
  - `TEXT` — chemin normal. Présentez `reply_text` (Markdown) à l'utilisateur. Optionnel : vous pouvez encore affiner la formulation pour le canal actif ; `prompts/enrich.md` est une référence d'enrichissement en chinois si vous voulez un texte plus riche.
  - Toute erreur → signalez le `reply_text` (ou le détail de l'erreur) à l'utilisateur.

**Remarque :** le skill ne renvoie qu'un JSON avec `reply_text` ; il n'implémente pas d'envoi spécifique à un canal.

---

## Gestion des erreurs

- `AMINER_API_KEY` absent → arrêtez-vous, demandez à l'utilisateur de le définir.
- Aucun profil en entrée → demandez à l'utilisateur des sujets, un nom de chercheur ou un `aminer_author_id`.
- Erreur API → signalez l'étape de l'erreur ; ne basculez pas vers d'autres skills.
