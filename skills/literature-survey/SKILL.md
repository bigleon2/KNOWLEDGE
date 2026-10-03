---
name: literature-survey
version: "1.0.0"
category: "Autres"
tags:
  - literature
  - survey
description: À utiliser quand l'utilisateur veut une revue de littérature complète sur un sujet de recherche précis. Produit un PDF de revue complet (6–20 pages, 60+ citations réelles, 100+ recommandé) avec source LaTeX, figures de taxonomie et table de littérature classée. Monotraitement, sans runtime Python.
language: fr

---

# Literature Survey

## Vue d'ensemble

Générateur de revue de littérature de bout en bout. **Une seule étape, qualité complète dès le départ.** L'agent (Claude Code / Cursor / Aider / Codex / …) réalise toute la construction avec ses propres outils (WebFetch, WebSearch, Write, Bash). Ce SKILL est procédure + playbooks de référence + template LaTeX — pas de runtime Python, pas de SDK LLM.

Le travail de fond est décomposé en playbooks de référence sous `references/` :

| Référence | Sujet |
|---|---|
| `references/00-incremental-execution.md` | comment faire concrètement sans perdre son travail : tailles de lots, persistance, reprise — **à lire en premier** |
| `references/01-bibliography-expansion.md` | porter `bibliography.bib` à 60+ entrées réelles (100+ recommandé) via WebFetch (sans mémoire) |
| `references/02-survey-figures.md` | figures de taxonomie / frise chronologique / matrice de couverture / carte des domaines |
| `references/03-survey-section-playbook.md` | structure section par section pour des articles au format revue |
| `references/04-layout-discipline.md` | tableaux, figures, flottants, renvois croisés, auteur + note de divulgation |
| `references/05-quality-gate.md` | autocontrôle avant livraison |

**Lire la référence pertinente _avant_ d'écrire, pas après.** Le passage complet ne tient pas en un seul tour — `references/00-incremental-execution.md` est le seul mode d'exécution qui va au bout.

## Quand l'utiliser

- L'utilisateur demande une « revue » / un « état de l'art » sur un sujet précis.
- L'utilisateur a un sujet de recherche et veut une carte structurée du domaine avec citations.
- L'utilisateur a besoin d'une lecture de fond pour un chapitre de thèse ou une section de demande de financement.

## Quand ne pas l'utiliser

- L'utilisateur veut de la recherche originale avec expériences → `paper-writer`.
- L'utilisateur ne veut qu'un plan / une exploration de sujet → `research-explorer`.
- L'utilisateur veut du code d'expériences → `experiment-suite`.
- Le sujet est trop vaste (p. ex. « toute l'IA ») — le restreindre avant de commencer.

## Flux de travail

### Étape 1 — Comprendre le sujet et le périmètre

Confirmer avec l'utilisateur :

- **Sujet** — domaine de recherche précis (p. ex. « l'apprentissage fédéré en santé »). Si trop vaste, le restreindre d'abord.
- **Périmètre** — revue large d'un domaine vs revue ciblée d'un sous-domaine.
- **Budget de citations** — minimum 60 entrées uniques ; viser 100+ (plus pour une revue large).
- **Langue** — chinois par défaut en conversation ; l'article LaTeX est en anglais sauf demande contraire.

Toujours indiquer à l'utilisateur qu'une relecture humaine par un expert du domaine est recommandée avant publication ou usage en production.

### Étape 2 — Préparer le répertoire d'exécution

```bash
TOPIC="<topic>"
SLUG=$(python3 -c "import re,hashlib,sys; t=sys.argv[1]; n=re.sub(r'[\\s_]+','-',re.sub(r'[^\\w\\s-]','',t.lower().strip())).strip('-')[:40].rstrip('-'); h=hashlib.sha1(t.encode()).hexdigest()[:8]; print(f'{n}-{h}')" "$TOPIC")
TS=$(date +%Y-%m-%d_%H%M%S)
RUN=output/literature-survey/$SLUG/$TS/survey_paper

mkdir -p "$RUN/sections" "$RUN/figures"
cp -r literature-survey/templates/survey/. "$RUN/"
ln -sfn "$TS" "output/literature-survey/$SLUG/latest"
```

Dans les commandes ci-dessous, `$RUN` = `output/literature-survey/<slug>/latest/survey_paper`.

### Étape 3 — Construire la revue (OBLIGATOIRE — c'est tout le travail)

Ouvrir d'abord `references/00-incremental-execution.md`. Puis mener les cinq chantiers ci-dessous sur de nombreux tours, en persistant l'état dans `$RUN/` après chaque lot.

#### 3.1 Bibliographie — 60+ entrées réelles (100+ recommandé)

**Ouvrir :** `references/01-bibliography-expansion.md`.

**D'abord (§0 de cette référence) : lire l'intention temporelle/de périmètre du sujet et choisir une posture de recherche.** Si le sujet nomme une année ou dit « dernières/récent » (p. ex. « OpenSource LLM **2026** »), adopter une posture *récence-d'abord* — requêtes arXiv triées par date portant l'année explicite, le canon servant seulement de contexte. Sinon, couvrir toute la période. C'est ce qui évite « demandé 2026, obtenu du 2024 ».

Puis planifier **12 à 20** angles de requête, pondérés selon la posture. Pour chaque angle, utiliser **AMiner academic search d'abord, la recherche web en complément** :

- **AMiner `search_papers`** — l'utiliser EN PREMIER pour chaque angle de requête. Il renvoie
  des articles avec des métadonnées structurées (titre, auteurs, année, venue, DOI, citations,
  abstract) bien plus fiables que les résultats scrapés sur le web. Exemple :
  `search_papers(query="federated learning survey", max_results=20, sort_by_citation=true)`.
- **AMiner `get_paper_details`** — pour les articles clés, récupérer les détails complets (abstract,
  citations, références) via leurs identifiants AMiner.
- **`web_search`** — à utiliser quand AMiner renvoie des résultats insuffisants, ou pour des
  sources non académiques (blogs, benchmarks, jeux de données, documentation d'outils).

Pour chaque candidat retenu : extraire directement du retour AMiner le titre/auteurs/année/venue/url/citations
canoniques. Pour les résultats issus uniquement de la recherche web, faire un WebFetch de l'URL d'abstract
pour extraire les métadonnées. Ajouter une entrée BibTeX à
`$RUN/bibliography.bib`. **Chaque entrée doit provenir d'une URL récupérée dans cette
session ou d'un résultat de recherche AMiner.** Les entrées tirées de la mémoire sont interdites.

**Arrêt ferme :** ne pas rédiger la prose avant que `grep -c "^@" $RUN/bibliography.bib` ≥ 60 (viser 100+).

#### 3.2 Figures — 6 à 10 figures au format revue

**Ouvrir :** `references/02-survey-figures.md`.

Une revue se juge à sa capacité à organiser un domaine ; les figures portent cette organisation :

- 1 diagramme de taxonomie / classification (hiérarchie TikZ)
- 1 frise chronologique des travaux majeurs
- 1 matrice de domaines / capacités (heatmap de couverture)
- 1–2 diagrammes d'architecture / mécanisme représentatifs
- 1–2 tracés de tendances quantitatifs (style publication matplotlib)
- Optionnel : réseau de citations, comparaison de paradigmes

Sauvegarder chaque figure dans `$RUN/figures/` avec sa source reproductible à côté.

#### 3.3 Sections — prose au format revue

**Ouvrir :** `references/03-survey-section-playbook.md`.

Les sections d'une revue diffèrent en forme de celles d'un article de recherche. Ordre : introduction → contexte → méthodes (revue thématique) → discussion → conclusion → travaux liés → **abstract en dernier**.

#### 3.4 Discipline de mise en page

**Ouvrir :** `references/04-layout-discipline.md`.

Encadrer chaque tableau dans `\begin{table}[!t]` avec booktabs ; chaque figure dans `\begin{figure}[!t]`. Utiliser `~\cite{}` et `~\ref{}`. Définir `\author{AI4S Agent}` avec une note `\thanks` qui **recommande toujours** une relecture humaine. Les revues ne comportent pas d'expériences numériques simulées, donc **ne pas** inclure de clause simulée.

#### 3.5 Compilation + contrôle qualité

```bash
cd "$RUN"
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

**Ouvrir :** `references/05-quality-gate.md`. Cibles propres aux revues : ≥ 60 entrées bib (100+ recommandé), ≥ 6 pages, ≥ 1 figure de taxonomie, ≥ 1 frise chronologique.

Si un contrôle ne peut pas être atteint honnêtement (p. ex. domaine réellement très petit), le dire explicitement. Pas de remplissage.

### Étape 4 — Livrer

Rapporter :

1. `output/literature-survey/<slug>/latest/survey_paper/main.pdf`
2. `output/literature-survey/<slug>/latest/survey_paper/` — projet LaTeX complet (reproductible)
3. `output/literature-survey/<slug>/latest/literature_table.md` — table de littérature classée (à écrire en parallèle de la constitution de la bib)
4. Statistiques selon le format de rapport de `references/05-quality-gate.md`.

## Flux de données inter-skills (convention de chemins)

Un skill en aval (p. ex. `paper-writer`) calculant le même slug pour le même sujet viendra chercher ici :

- `output/literature-survey/<slug>/latest/survey_paper/bibliography.bib` — point de départ bib.

## Règles importantes

- **Pas de SDK LLM dans ce skill.** Pas de `import anthropic` / `import openai`. Le skill se limite à SKILL.md + références + template LaTeX.
- **Aucune citation fabriquée.** Chaque entrée BibTeX doit remonter à une URL récupérée dans la session. Affirmation réelle ou plus prudente — jamais de fausse référence.
- **Arrêt honnête > remplissage.** Si le domaine est trop petit pour 60 citations réelles, le dire à l'utilisateur au lieu d'inventer des entrées.
- **Périmètre de revue** : 6–20 pages avec 60–150 références (100+ recommandé). Pour des formats plus longs ou plus courts, ajuster explicitement le périmètre avec l'utilisateur au départ.
