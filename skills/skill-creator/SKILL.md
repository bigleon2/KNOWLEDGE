---
name: skill-creator
version: 1.1.0
category: ecosystem
language: fr
tags:
    - skill
    - creator
description: Skill creator servant à créer de nouveaux skills, à modifier et améliorer des skills existants, et à mesurer leur performance. Utiliser quand l'utilisateur veut créer un skill de zéro, écrire un SKILL.md, accompagner la création ou la modification d'un skill (frontmatter, name, description, version, tags), éditer ou optimiser un skill existant, évaluer un skill en lançant des evals, benchmarker sa performance avec analyse de variance, ou optimiser la description d'un skill pour une meilleure précision de déclenchement.
---

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# Skill Creator

Un skill pour créer de nouveaux skills et les améliorer de manière itérative.

À un haut niveau, le processus de création d'un skill se déroule ainsi :

- Décider ce que le skill doit faire et, grossièrement, comment il doit le faire
- Écrire une ébauche du skill
- Créer quelques prompts de test et les exécuter avec glm-with-access-to-the-skill
- Aider l'utilisateur à évaluer les résultats à la fois qualitativement et quantitativement
  - Pendant que les exécutions tournent en arrière-plan, rédiger quelques evals quantitatifs s'il n'y en a pas (s'il y en a, vous pouvez les utiliser tels quels ou les modifier si vous estimez que quelque chose doit changer). Puis les expliquer à l'utilisateur (ou, s'ils existaient déjà, expliquer ceux qui existent déjà)
  - Utiliser le script `eval-viewer/generate_review.py` pour montrer les résultats à l'utilisateur et lui permettre aussi de consulter les métriques quantitatives
- Réécrire le skill en fonction du feedback de l'utilisateur sur les résultats (et aussi s'il y a des défauts flagrants qui apparaissent dans les benchmarks quantitatifs)
- Répéter jusqu'à satisfaction
- Étendre le jeu de tests et réessayer à plus grande échelle

Votre travail lorsque vous utilisez ce skill consiste à déterminer où l'utilisateur en est dans ce processus, puis à intervenir pour l'aider à progresser à travers ces étapes. Par exemple, l'utilisateur dit peut-être « je veux créer un skill pour X ». Vous pouvez l'aider à préciser ce qu'il veut, écrire une ébauche, rédiger les cas de test, déterminer comment il souhaite évaluer, exécuter tous les prompts, et répéter.

Inversement, l'utilisateur a peut-être déjà une ébauche du skill. Dans ce cas, vous pouvez passer directement à la partie évaluer/itérer de la boucle.

Bien sûr, restez toujours flexible : si l'utilisateur dit « pas besoin de lancer tout un tas d'évaluations, on avance au feeling », vous pouvez faire exactement cela.

Ensuite, une fois le skill terminé (mais encore une fois, l'ordre reste flexible), vous pouvez aussi lancer l'améliorateur de description de skill — un script entièrement dédié existe pour cela — afin d'optimiser le déclenchement du skill.

Ça marche ? Ça marche.

## Communiquer avec l'utilisateur

Le skill-creator est susceptible d'être utilisé par des personnes dont la familiarité avec le jargon informatique varie énormément. Si vous n'étiez pas au courant (et comment le seriez-vous, c'est très récent), il existe désormais une tendance où la puissance de GLM inspire aux plombiers d'ouvrir leur terminal, et aux parents et grands-parents de googler « comment installer npm ». À l'inverse, la majorité des utilisateurs sont probablement assez à l'aise avec l'informatique.

Portez donc attention aux indices du contexte pour adapter votre façon de communiquer ! Dans le cas par défaut, pour vous donner une idée :

- « évaluation » et « benchmark » sont limites, mais acceptables
- pour « JSON » et « assertion », attendez des signaux sérieux indiquant que l'utilisateur sait ce que c'est avant de les employer sans les expliquer

Rien ne vous empêche d'expliquer brièvement un terme en cas de doute, et n'hésitez pas à clarifier le vocabulaire par une courte définition si vous craignez que l'utilisateur ne comprenne pas.

---

## Créer un skill

### Capter l'intention

Commencez par comprendre l'intention de l'utilisateur. La conversation en cours contient peut-être déjà un workflow que l'utilisateur veut capturer (par exemple, il dit « transforme ça en skill »). Dans ce cas, extrayez d'abord les réponses de l'historique de conversation — les outils utilisés, la séquence d'étapes, les corrections apportées par l'utilisateur, les formats d'entrée/sortie observés. L'utilisateur devra peut-être combler les lacunes, et il doit confirmer avant de passer à l'étape suivante.

1. Qu'est-ce que ce skill doit permettre à GLM de faire ?
2. Quand ce skill doit-il se déclencher ? (quelles formulations/quels contextes utilisateur)
3. Quel est le format de sortie attendu ?
4. Faut-il mettre en place des cas de test pour vérifier que le skill fonctionne ? Les skills aux sorties objectivement vérifiables (transformations de fichiers, extraction de données, génération de code, étapes de workflow fixes) tirent profit de cas de test. Les skills aux sorties subjectives (style d'écriture, art) n'en ont souvent pas besoin. Proposez la valeur par défaut adaptée au type de skill, mais laissez l'utilisateur décider.

### Entretien et recherche

Posez proactivement des questions sur les cas limites, les formats d'entrée/sortie, les fichiers d'exemple, les critères de succès et les dépendances. Attendez d'avoir réglé cette partie avant de rédiger les prompts de test.

Vérifiez les MCP disponibles — s'ils sont utiles pour la recherche (consulter de la doc, trouver des skills similaires, chercher les bonnes pratiques), recherchez en parallèle via des sous-agents si disponibles, sinon en direct. Arrivez préparé avec du contexte pour réduire la charge sur l'utilisateur.

### Rédiger le SKILL.md

À partir de l'entretien avec l'utilisateur, renseignez ces composants :

- **name** : identifiant du skill
- **description** : quand se déclencher, ce que ça fait. C'est le mécanisme principal de déclenchement — incluez à la fois ce que fait le skill ET les contextes précis d'utilisation. Toute l'information « quand l'utiliser » va ici, pas dans le corps. Remarque : actuellement, GLM a tendance à « sous-déclencher » les skills — à ne pas les utiliser alors qu'ils seraient utiles. Pour contrer cela, rendez les descriptions de skills un peu « insistantes ». Par exemple, au lieu de « Comment construire un dashboard simple et rapide pour afficher les données internes de Zhipu AI. », vous pourriez écrire « Comment construire un dashboard simple et rapide pour afficher les données internes de Zhipu AI. Pensez à utiliser ce skill dès que l'utilisateur mentionne des dashboards, de la visualisation de données, des métriques internes, ou souhaite afficher n'importe quelles données d'entreprise, même s'il ne demande pas explicitement un "dashboard". »
- **compatibility** : outils requis, dépendances (optionnel, rarement nécessaire)
- **le reste du skill :)**

### Guide de rédaction d'un skill

#### Anatomie d'un skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Divulgation progressive (progressive disclosure)

Les skills utilisent un système de chargement à trois niveaux :
1. **Métadonnées** (name + description) — toujours en contexte (~100 mots)
2. **Corps du SKILL.md** — en contexte à chaque déclenchement du skill (<500 lignes idéalement)
3. **Ressources embarquées** — au besoin (sans limite, les scripts peuvent s'exécuter sans être chargés)

Ces compteurs de mots sont indicatifs et vous pouvez largement dépasser si nécessaire.

**Patterns clés :**
- Gardez le SKILL.md sous 500 lignes ; si vous approchez de cette limite, ajoutez un niveau de hiérarchie supplémentaire ainsi que des pointeurs clairs indiquant où le modèle qui utilise le skill doit poursuivre.
- Référencez clairement les fichiers depuis le SKILL.md, en indiquant quand les lire
- Pour les fichiers de référence volumineux (>300 lignes), incluez une table des matières

**Organisation par domaine** : quand un skill prend en charge plusieurs domaines/frameworks, organisez par variante :
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

GLM ne lit que le fichier de référence pertinent.

#### Principe d'absence de surprise

Cela va de soi, mais les skills ne doivent contenir ni malware, ni code d'exploit, ni aucun contenu susceptible de compromettre la sécurité du système. Le contenu d'un skill ne doit pas surprendre l'utilisateur quant à son intention lorsqu'il est décrit. N'acceptez pas les demandes de création de skills trompeurs ou conçus pour faciliter un accès non autorisé, l'exfiltration de données ou d'autres activités malveillantes. En revanche, des choses comme « joue le rôle d'un XYZ » sont acceptables.

#### Patterns de rédaction

Privilégiez la forme impérative dans les instructions.

**Définir les formats de sortie** — vous pouvez procéder ainsi :
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Pattern des exemples** — il est utile d'inclure des exemples. Vous pouvez les formater ainsi (mais si "Input" et "Output" figurent dans vos exemples, vous pouvez vous en écarter un peu) :
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Style de rédaction

Essayez d'expliquer au modèle pourquoi les choses sont importantes, plutôt que d'aligner des MUST poussiéreux et pesants. Utilisez la théorie de l'esprit et veillez à rendre le skill général, et non ultra-étroit sur des exemples précis. Commencez par écrire une ébauche, puis relisez-la avec un regard neuf et améliorez-la.

### Cas de test

Après avoir écrit l'ébauche du skill, concevez 2-3 prompts de test réalistes — le genre de choses qu'un véritable utilisateur dirait vraiment. Partagez-les avec l'utilisateur : [pas besoin d'utiliser ce libellé exact] « Voici quelques cas de test que j'aimerais essayer. Vous semblent-ils corrects, ou voulez-vous en ajouter d'autres ? » Puis exécutez-les.

Enregistrez les cas de test dans `evals/evals.json`. N'écrivez pas encore les assertions — seulement les prompts. Vous rédigerez les assertions à l'étape suivante, pendant que les exécutions sont en cours.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

Voir `references/schemas.md` pour le schéma complet (y compris le champ `assertions`, que vous ajouterez plus tard).

## Exécuter et évaluer les cas de test

Cette section est une séquence continue — ne vous arrêtez pas en cours de route. N'utilisez PAS `/skill-test` ni aucun autre skill de test.

Placez les résultats dans `<skill-name>-workspace/`, au même niveau que le répertoire du skill. Dans le workspace, organisez les résultats par itération (`iteration-1/`, `iteration-2/`, etc.) et, à l'intérieur, chaque cas de test obtient un répertoire (`eval-0/`, `eval-1/`, etc.). Ne créez pas tout cela d'avance — créez simplement les répertoires au fur et à mesure.

### Étape 1 : Lancer toutes les exécutions (avec skill ET baseline) dans le même tour

Pour chaque cas de test, lancez deux sous-agents dans le même tour — un avec le skill, un sans. C'est important : ne lancez pas d'abord les exécutions avec skill pour revenir aux baselines ensuite. Lancez tout d'un coup afin que tout se termine à peu près en même temps.

**Exécution avec skill :**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Exécution baseline** (même prompt, mais la baseline dépend du contexte) :
- **Création d'un nouveau skill** : aucun skill du tout. Même prompt, pas de chemin de skill, enregistrement dans `without_skill/outputs/`.
- **Amélioration d'un skill existant** : l'ancienne version. Avant toute modification, faites un snapshot du skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), puis pointez le sous-agent baseline vers le snapshot. Enregistrement dans `old_skill/outputs/`.

Écrivez un `eval_metadata.json` pour chaque cas de test (les assertions peuvent rester vides pour l'instant). Donnez à chaque eval un nom descriptif basé sur ce qu'il teste — pas juste « eval-0 ». Utilisez aussi ce nom pour le répertoire. Si cette itération utilise des prompts d'eval nouveaux ou modifiés, créez ces fichiers pour chaque nouveau répertoire d'eval — ne supposez pas qu'ils se propagent des itérations précédentes.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Étape 2 : Pendant que les exécutions sont en cours, rédiger les assertions

Ne vous contentez pas d'attendre la fin des exécutions — vous pouvez utiliser ce temps de façon productive. Rédigez des assertions quantitatives pour chaque cas de test et expliquez-les à l'utilisateur. Si des assertions existent déjà dans `evals/evals.json`, relisez-les et expliquez ce qu'elles vérifient.

Les bonnes assertions sont objectivement vérifiables et portent des noms descriptifs — elles doivent se lire clairement dans le viewer de benchmark pour que quiconque jette un œil aux résultats comprenne immédiatement ce que chacune vérifie. Les skills subjectifs (style d'écriture, qualité de design) s'évaluent mieux qualitativement — n'imposez pas d'assertions à ce qui requiert un jugement humain.

Mettez à jour les fichiers `eval_metadata.json` et `evals/evals.json` avec les assertions une fois rédigées. Expliquez aussi à l'utilisateur ce qu'il verra dans le viewer — à la fois les sorties qualitatives et le benchmark quantitatif.

### Étape 3 : À mesure que les exécutions se terminent, capturer les données de timing

À la fin de chaque tâche de sous-agent, vous recevez une notification contenant `total_tokens` et `duration_ms`. Enregistrez immédiatement ces données dans `timing.json` dans le répertoire de l'exécution :

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

C'est la seule occasion de capturer ces données — elles arrivent via la notification de tâche et ne sont persistées nulle part ailleurs. Traitez chaque notification dès son arrivée au lieu d'essayer de les grouper.

### Étape 4 : Noter, agréger et lancer le viewer

Une fois toutes les exécutions terminées :

1. **Notez chaque exécution** — lancez un sous-agent grader (ou notez en direct) qui lit `agents/grader.md` et évalue chaque assertion par rapport aux sorties. Enregistrez les résultats dans `grading.json` dans chaque répertoire d'exécution. Le tableau `expectations` du grading.json doit utiliser les champs `text`, `passed` et `evidence` (pas `name`/`met`/`details` ni d'autres variantes) — le viewer dépend de ces noms de champs exacts. Pour les assertions vérifiables programmatiquement, écrivez et exécutez un script plutôt que d'estimer à l'œil — les scripts sont plus rapides, plus fiables et réutilisables entre itérations.

2. **Agrégez en benchmark** — exécutez le script d'agrégation depuis le répertoire du skill-creator :
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Cela produit `benchmark.json` et `benchmark.md` avec pass_rate, temps et tokens pour chaque configuration, avec moyenne ± écart-type et le delta. Si vous générez benchmark.json manuellement, consultez `references/schemas.md` pour le schéma exact qu'attend le viewer.
Placez chaque version with_skill avant sa contrepartie baseline.

3. **Faites une passe d'analyse** — lisez les données du benchmark et faites émerger les patterns que les stats agrégées peuvent masquer. Voir `agents/analyzer.md` (la section « Analyzing Benchmark Results ») pour savoir quoi chercher — par exemple des assertions qui passent toujours quel que soit le skill (non discriminantes), des evals à forte variance (potentiellement instables) et les arbitrages temps/tokens.

4. **Lancez le viewer** avec à la fois les sorties qualitatives et les données quantitatives :
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   Pour l'itération 2 et plus, passez aussi `--previous-workspace <workspace>/iteration-<N-1>`.

   **Environnements Cowork / headless :** si `webbrowser.open()` n'est pas disponible ou que l'environnement n'a pas d'affichage, utilisez `--static <output_path>` pour écrire un fichier HTML autonome au lieu de démarrer un serveur. Le feedback sera téléchargé sous forme de fichier `feedback.json` quand l'utilisateur cliquera sur « Submit All Reviews ». Après le téléchargement, copiez `feedback.json` dans le répertoire du workspace pour que l'itération suivante puisse le récupérer.

Remarque : utilisez generate_review.py pour créer le viewer ; inutile d'écrire du HTML personnalisé.

5. **Dites à l'utilisateur** quelque chose comme : « J'ai ouvert les résultats dans votre navigateur. Il y a deux onglets — "Outputs" permet de parcourir chaque cas de test et de laisser un feedback, "Benchmark" affiche la comparaison quantitative. Quand vous avez terminé, revenez ici me le dire. »

### Ce que l'utilisateur voit dans le viewer

L'onglet « Outputs » montre un cas de test à la fois :
- **Prompt** : la tâche qui a été donnée
- **Output** : les fichiers produits par le skill, affichés en ligne quand c'est possible
- **Previous Output** (itération 2+) : section repliée montrant la sortie de l'itération précédente
- **Formal Grades** (si la notation a été exécutée) : section repliée montrant réussite/échec des assertions
- **Feedback** : une zone de texte qui s'enregistre automatiquement pendant la saisie
- **Previous Feedback** (itération 2+) : leurs commentaires de la dernière fois, affichés sous la zone de texte

L'onglet « Benchmark » affiche le résumé des stats : taux de réussite, timing et consommation de tokens pour chaque configuration, avec ventilations par eval et observations de l'analyste.

La navigation se fait via les boutons précédent/suivant ou les touches fléchées. Une fois terminé, l'utilisateur clique sur « Submit All Reviews », ce qui enregistre tout le feedback dans `feedback.json`.

### Étape 5 : Lire le feedback

Quand l'utilisateur vous dit qu'il a terminé, lisez `feedback.json` :

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Un feedback vide signifie que l'utilisateur a trouvé cela bon. Concentrez vos améliorations sur les cas de test où l'utilisateur a formulé des critiques précises.

Arrêtez le serveur du viewer quand vous avez fini avec lui :

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Améliorer le skill

C'est le cœur de la boucle. Vous avez exécuté les cas de test, l'utilisateur a relu les résultats, et vous devez maintenant rendre le skill meilleur à partir de son feedback.

### Comment aborder les améliorations

1. **Généralisez à partir du feedback.** L'idée de fond ici, c'est que nous essayons de créer des skills utilisables un million de fois (peut-être littéralement, voire plus, qui sait) sur une grande variété de prompts. Ici, vous et l'utilisateur itérez sur quelques exemples seulement, encore et encore, parce que cela permet d'avancer plus vite. L'utilisateur connaît ces exemples sur le bout des doigts et il lui est rapide d'évaluer les nouvelles sorties. Mais si le skill que vous co-développez ne fonctionne que pour ces exemples, il est inutile. Plutôt que d'introduire des changements pointilleux et sur-spécifiques, ou des MUST oppressants et contraignants, s'il y a un problème tenace, essayez d'élargir la perspective avec des métaphores différentes, ou recommandez d'autres façons de travailler. Essayer coûte relativement peu et vous tomberez peut-être sur quelque chose de génial.

2. **Gardez le prompt léger.** Retirez ce qui ne justifie pas sa présence. Pensez à lire les transcripts, pas seulement les sorties finales — s'il semble que le skill fait perdre beaucoup de temps au modèle dans des activités improductives, vous pouvez essayer de supprimer les parties du skill qui le poussent à faire cela et voir ce que ça donne.

3. **Expliquez le pourquoi.** Efforcez-vous d'expliquer le **pourquoi** de tout ce que vous demandez au modèle. Les LLM d'aujourd'hui sont *intelligents*. Ils ont une bonne théorie de l'esprit et, dotés d'un bon harnais, peuvent aller au-delà d'instructions apprises par cœur et vraiment faire advenir les choses. Même si le feedback de l'utilisateur est laconique ou agacé, essayez de comprendre réellement la tâche, pourquoi l'utilisateur écrit ce qu'il écrit, et ce qu'il a réellement écrit, puis transmettez cette compréhension dans les instructions. Si vous vous surprenez à écrire ALWAYS ou NEVER en majuscules, ou à utiliser des structures ultra rigides, c'est un signal d'alerte — dans la mesure du possible, reformulez et expliquez le raisonnement pour que le modèle comprenne pourquoi ce que vous demandez est important. C'est une approche plus humaine, plus puissante et plus efficace.

4. **Repérez le travail répété entre les cas de test.** Lisez les transcripts des exécutions de test et remarquez si les sous-agents ont tous écrit indépendamment des scripts d'aide similaires ou suivi la même approche multi-étapes pour quelque chose. Si les 3 cas de test ont tous conduit le sous-agent à écrire un `create_docx.py` ou un `build_chart.py`, c'est un signal fort que le skill devrait embarquer ce script. Écrivez-le une fois, placez-le dans `scripts/`, et dites au skill de l'utiliser. Cela évite à chaque invocation future de réinventer la roue.

Cette tâche est vraiment importante (nous essayons de créer des milliards de valeur économique par an ici !) et votre temps de réflexion n'est pas le facteur limitant ; prenez votre temps et mûrissez vraiment vos idées. Je suggère d'écrire une ébauche de révision, puis de la relire à neuf et de l'améliorer. Faites vraiment de votre mieux pour entrer dans la tête de l'utilisateur et comprendre ce qu'il veut et ce dont il a besoin.

### La boucle d'itération

Après avoir amélioré le skill :

1. Appliquez vos améliorations au skill
2. Réexécutez tous les cas de test dans un nouveau répertoire `iteration-<N+1>/`, y compris les exécutions baseline. Si vous créez un nouveau skill, la baseline est toujours `without_skill` (aucun skill) — cela reste identique entre les itérations. Si vous améliorez un skill existant, à vous de juger ce qui a du sens comme baseline : la version originale avec laquelle l'utilisateur est arrivé, ou l'itération précédente.
3. Lancez le reviewer avec `--previous-workspace` pointant vers l'itération précédente
4. Attendez que l'utilisateur relise et vous dise qu'il a terminé
5. Lisez le nouveau feedback, améliorez à nouveau, répétez

Continuez jusqu'à ce que :
- L'utilisateur dit qu'il est satisfait
- Le feedback est entièrement vide (tout semble bon)
- Vous ne progressez plus de manière significative

---

## Avancé : comparaison à l'aveugle

Pour les situations où vous voulez une comparaison plus rigoureuse entre deux versions d'un skill (par exemple, l'utilisateur demande « la nouvelle version est-elle vraiment meilleure ? »), il existe un système de comparaison à l'aveugle. Lisez `agents/comparator.md` et `agents/analyzer.md` pour les détails. L'idée de base : donner deux sorties à un agent indépendant sans lui dire laquelle est laquelle, et le laisser juger la qualité. Analysez ensuite pourquoi le gagnant a gagné.

C'est optionnel, cela requiert des sous-agents, et la plupart des utilisateurs n'en auront pas besoin. La boucle de relecture humaine suffit généralement.

---

## Optimisation de la description

Le champ description dans le frontmatter du SKILL.md est le mécanisme principal qui détermine si GLM invoque un skill. Après avoir créé ou amélioré un skill, proposez d'optimiser la description pour une meilleure précision de déclenchement.

### Étape 1 : Générer les requêtes d'eval de déclenchement

Créez 20 requêtes d'eval — un mélange de should-trigger et de should-not-trigger. Enregistrez en JSON :

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Les requêtes doivent être réalistes et correspondre à ce qu'un utilisateur de GLM Code ou de GLM.ai taperait réellement. Pas des demandes abstraites, mais des demandes concrètes et précises, avec une bonne dose de détails. Par exemple : des chemins de fichiers, du contexte personnel sur le métier ou la situation de l'utilisateur, des noms et valeurs de colonnes, des noms d'entreprise, des URLs. Un peu de contexte en arrière-plan. Certaines peuvent être en minuscules ou contenir des abréviations, des fautes de frappe ou un langage familier. Variez les longueurs et concentrez-vous sur les cas limites plutôt que sur des cas évidents (l'utilisateur aura l'occasion de les valider).

Mauvais : `"Formate ces données"`, `"Extrait le texte du PDF"`, `"Crée un graphique"`

Bon : `"alors mon boss vient de m'envoyer ce fichier xlsx (il est dans mes téléchargements, il s'appelle un truc comme 'Q4 sales final FINAL v2.xlsx') et elle veut que j'ajoute une colonne qui montre la marge bénéficiaire en pourcentage. Le chiffre d'affaires est en colonne C et les coûts en colonne D je pense"`

Pour les requêtes **should-trigger** (8-10), pensez à la couverture. Vous voulez différentes formulations d'une même intention — certaines formelles, certaines décontractées. Incluez des cas où l'utilisateur ne nomme pas explicitement le skill ou le type de fichier mais en a clairement besoin. Ajoutez des cas d'usage peu courants et des cas où ce skill est en concurrence avec un autre mais devrait l'emporter.

Pour les requêtes **should-not-trigger** (8-10), les plus précieuses sont les quasi-collisions — des requêtes qui partagent des mots-clés ou des concepts avec le skill mais nécessitent en réalité autre chose. Pensez aux domaines adjacents, aux formulations ambiguës où une correspondance naïve par mot-clé déclencherait à tort, et aux cas où la requête touche à quelque chose que fait le skill mais dans un contexte où un autre outil est plus approprié.

Le piège principal à éviter : ne rendez pas les requêtes should-not-trigger trivialement hors sujet. « Écris une fonction fibonacci » comme test négatif pour un skill PDF est trop facile — ça ne teste rien. Les cas négatifs doivent être vraiment retors.

### Étape 2 : Relecture avec l'utilisateur

Présentez le jeu d'evals à l'utilisateur pour relecture en utilisant le template HTML :

1. Lisez le template depuis `assets/eval_review.html`
2. Remplacez les placeholders :
   - `__EVAL_DATA_PLACEHOLDER__` → le tableau JSON des items d'eval (sans guillemets autour — c'est une affectation de variable JS)
   - `__SKILL_NAME_PLACEHOLDER__` → le nom du skill
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → la description actuelle du skill
3. Écrivez dans un fichier temporaire (par ex. `/tmp/eval_review_<skill-name>.html`) et ouvrez-le : `open /tmp/eval_review_<skill-name>.html`
4. L'utilisateur peut modifier les requêtes, basculer should-trigger, ajouter/supprimer des entrées, puis cliquer sur « Export Eval Set »
5. Le fichier se télécharge dans `~/Downloads/eval_set.json` — vérifiez le dossier Downloads pour la version la plus récente au cas où il y en aurait plusieurs (par ex. `eval_set (1).json`)

Cette étape compte — de mauvaises requêtes d'eval mènent à de mauvaises descriptions.

### Étape 3 : Lancer la boucle d'optimisation

Dites à l'utilisateur : « Cela va prendre du temps — je lance la boucle d'optimisation en arrière-plan et je vérifie périodiquement. »

Enregistrez le jeu d'evals dans le workspace, puis lancez en arrière-plan :

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Utilisez l'ID du modèle de votre system prompt (celui qui alimente la session en cours) afin que le test de déclenchement corresponde à ce que l'utilisateur connaît réellement.

Pendant son exécution, consultez périodiquement la sortie (tail) pour donner à l'utilisateur des nouvelles sur l'itération en cours et l'allure des scores.

Cela gère automatiquement la boucle d'optimisation complète. Il divise le jeu d'evals en 60 % train et 40 % test retenu, évalue la description actuelle (en exécutant chaque requête 3 fois pour obtenir un taux de déclenchement fiable), puis appelle GLM pour proposer des améliorations à partir de ce qui a échoué. Il réévalue chaque nouvelle description sur train et test, en itérant jusqu'à 5 fois. Une fois terminé, il ouvre un rapport HTML dans le navigateur montrant les résultats par itération et renvoie un JSON avec `best_description` — sélectionné d'après le score de test plutôt que le score de train pour éviter le surapprentissage.

### Fonctionnement du déclenchement des skills

Comprendre le mécanisme de déclenchement aide à concevoir de meilleures requêtes d'eval. Les skills apparaissent dans la liste `available_skills` de GLM avec leur name + description, et GLM décide de consulter ou non un skill sur la base de cette description. Le point important à savoir : GLM ne consulte les skills que pour les tâches qu'il ne sait pas gérer facilement tout seul — des requêtes simples en une étape comme « lis ce PDF » peuvent ne pas déclencher de skill même si la description correspond parfaitement, car GLM peut les traiter directement avec ses outils de base. Les requêtes complexes, multi-étapes ou spécialisées déclenchent de manière fiable les skills quand la description correspond.

Cela signifie que vos requêtes d'eval doivent être suffisamment consistantes pour que GLM tire réellement profit de la consultation d'un skill. Des requêtes simples comme « lis le fichier X » sont de mauvais cas de test — elles ne déclencheront pas de skills quelle que soit la qualité de la description.

### Étape 4 : Appliquer le résultat

Prenez `best_description` de la sortie JSON et mettez à jour le frontmatter du SKILL.md du skill. Montrez à l'utilisateur l'avant/après et rapportez les scores.

---

### Packager et présenter (uniquement si l'outil `present_files` est disponible)

Vérifiez si vous avez accès à l'outil `present_files`. Si non, passez cette étape. Si oui, packagez le skill et présentez le fichier .skill à l'utilisateur :

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Après le packaging, indiquez à l'utilisateur le chemin du fichier `.skill` obtenu afin qu'il puisse l'installer.

---

## Instructions spécifiques à GLM.ai

Dans GLM.ai, le workflow central est le même (ébauche → test → relecture → amélioration → répétition), mais comme GLM.ai n'a pas de sous-agents, certaines mécaniques changent. Voici ce qu'il faut adapter :

**Exécution des cas de test** : pas de sous-agents signifie pas d'exécution parallèle. Pour chaque cas de test, lisez le SKILL.md du skill, puis suivez ses instructions pour réaliser vous-même le prompt de test. Faites-les un par un. C'est moins rigoureux que des sous-agents indépendants (vous avez écrit le skill et vous l'exécutez aussi, donc vous avez tout le contexte), mais c'est une vérification de bon sens utile — et l'étape de relecture humaine compense. Passez les exécutions baseline — utilisez simplement le skill pour accomplir la tâche comme demandé.

**Relecture des résultats** : si vous ne pouvez pas ouvrir de navigateur (par ex. la VM de GLM.ai n'a pas d'affichage, ou vous êtes sur un serveur distant), sautez complètement le reviewer navigateur. Présentez plutôt les résultats directement dans la conversation. Pour chaque cas de test, montrez le prompt et la sortie. Si la sortie est un fichier que l'utilisateur doit voir (comme un .docx ou un .xlsx), enregistrez-le sur le système de fichiers et indiquez où il se trouve pour qu'il puisse le télécharger et l'inspecter. Demandez un feedback en direct : « Qu'en pensez-vous ? Y a-t-il quelque chose que vous changeriez ? »

**Benchmarking** : sautez le benchmarking quantitatif — il repose sur des comparaisons baseline qui n'ont pas de sens sans sous-agents. Concentrez-vous sur le feedback qualitatif de l'utilisateur.

**La boucle d'itération** : comme avant — améliorez le skill, réexécutez les cas de test, demandez un feedback — simplement sans le reviewer navigateur au milieu. Vous pouvez toujours organiser les résultats en répertoires d'itération sur le système de fichiers si vous en avez un.

**Optimisation de la description** : cette section requiert l'outil CLI `glm` (plus précisément `glm -p`), disponible uniquement dans GLM Code. Sautez-la si vous êtes sur GLM.ai.

**Comparaison à l'aveugle** : requiert des sous-agents. Sautez-la.

**Packaging** : le script `package_skill.py` fonctionne partout où il y a Python et un système de fichiers. Sur GLM.ai, vous pouvez l'exécuter et l'utilisateur peut télécharger le fichier `.skill` obtenu.

**Mise à jour d'un skill existant** : l'utilisateur peut vous demander de mettre à jour un skill existant, et non d'en créer un nouveau. Dans ce cas :
- **Conservez le nom d'origine.** Notez le nom du répertoire du skill et le champ `name` du frontmatter — utilisez-les tels quels. Par ex., si le skill installé est `research-helper`, produisez `research-helper.skill` (pas `research-helper-v2`).
- **Copiez vers un emplacement inscriptible avant de modifier.** Le chemin du skill installé peut être en lecture seule. Copiez dans `/tmp/skill-name/`, modifiez là-bas, et packagez depuis la copie.
- **Si vous packagez manuellement, passez d'abord par `/tmp/`**, puis copiez vers le répertoire de sortie — les écritures directes peuvent échouer à cause des permissions.

---

## Instructions spécifiques à Cowork

Si vous êtes dans Cowork, voici l'essentiel à savoir :

- Vous avez des sous-agents, donc le workflow principal (lancer les cas de test en parallèle, exécuter les baselines, noter, etc.) fonctionne entièrement. (Cependant, si vous rencontrez de sérieux problèmes de timeouts, vous pouvez exécuter les prompts de test en série plutôt qu'en parallèle.)
- Vous n'avez ni navigateur ni affichage, donc pour générer l'eval viewer, utilisez `--static <output_path>` pour écrire un fichier HTML autonome au lieu de démarrer un serveur. Proposez ensuite un lien sur lequel l'utilisateur peut cliquer pour ouvrir le HTML dans son navigateur.
- Pour une raison quelconque, la configuration de Cowork semble dissuader GLM de générer l'eval viewer après l'exécution des tests, donc pour répéter : que vous soyez dans Cowork ou dans GLM Code, après avoir exécuté les tests, vous devez toujours générer l'eval viewer pour que l'humain regarde les exemples avant que vous ne révisiez vous-même le skill et tentiez des corrections, en utilisant `generate_review.py` (pas en écrivant votre propre code html artisanal). Désolé d'avance mais je passe en majuscules : GÉNÉREZ L'EVAL VIEWER *AVANT* d'évaluer vous-même les sorties. Vous voulez les mettre devant les yeux de l'humain au plus vite !
- Le feedback fonctionne différemment : comme il n'y a pas de serveur en marche, le bouton « Submit All Reviews » du viewer téléchargera `feedback.json` sous forme de fichier. Vous pourrez ensuite le lire depuis là (il faudra peut-être d'abord demander l'accès).
- Le packaging fonctionne — `package_skill.py` a juste besoin de Python et d'un système de fichiers.
- L'optimisation de la description (`run_loop.py` / `run_eval.py`) devrait fonctionner dans Cowork sans problème puisqu'elle utilise `glm -p` via subprocess, pas un navigateur, mais gardez-la pour la fin, quand le skill est totalement achevé et que l'utilisateur reconnaît qu'il est en bon état.
- **Mise à jour d'un skill existant** : l'utilisateur peut vous demander de mettre à jour un skill existant, et non d'en créer un nouveau. Suivez les consignes de mise à jour de la section glm.ai ci-dessus.

---

## Fichiers de référence

Le répertoire agents/ contient les instructions pour des sous-agents spécialisés. Lisez-les quand vous devez lancer le sous-agent concerné.

- `agents/grader.md` — Comment évaluer les assertions par rapport aux sorties
- `agents/comparator.md` — Comment réaliser une comparaison A/B à l'aveugle entre deux sorties
- `agents/analyzer.md` — Comment analyser pourquoi une version a battu une autre

Le répertoire references/ contient de la documentation supplémentaire :
- `references/schemas.md` — structures JSON pour evals.json, grading.json, etc.

---

On répète une dernière fois la boucle centrale, pour insister :

- Cerner l'objet du skill
- Ébaucher ou modifier le skill
- Exécuter glm-with-access-to-the-skill sur les prompts de test
- Avec l'utilisateur, évaluer les sorties :
  - Créer benchmark.json et lancer `eval-viewer/generate_review.py` pour aider l'utilisateur à les relire
  - Lancer des evals quantitatifs
- Répéter jusqu'à ce que vous et l'utilisateur soyez satisfaits
- Packager le skill final et le remettre à l'utilisateur.

Ajoutez s'il vous plaît les étapes à votre TodoList, si vous en avez une, pour ne rien oublier. Si vous êtes dans Cowork, mettez spécifiquement « Créer le JSON d'evals et lancer `eval-viewer/generate_review.py` pour que l'humain relise les cas de test » dans votre TodoList pour être sûr que cela arrive.

Bonne chance !
