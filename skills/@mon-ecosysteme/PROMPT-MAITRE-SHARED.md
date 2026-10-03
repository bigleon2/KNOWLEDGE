# PROMPT MAÎTRE SHARED — Socle commun écosystème Knowledge

> **Version** : 1.6.4
> **Révision** : 2026-10-02 (Task 16, suggestions (a)/(b) — résorption F1/F2/F4) — **v1.6.4** : §6.1 — PM CORRECT-WORK porté à v2.7.0 (PMs v2.6.0/v2.7.0 matérialisés au corpus par diffs chirurgicaux méthode B1, provenance de reconstitution tracée — résorption F2) et référence PM-INSTALL portée à v1.3.1 (cas d'espèce R2 correct-work résorbé) ; directive « appliquer (a) puis (b) pour résorber les écarts F1/F2/F4 », session web-8a7e5653. 2026-10-02 (déduplication download/, Task 14) — **v1.6.3** : §6.1 — référence PM-INSTALL portée à v1.3.0 (décision d'architecture v2.2 : canal de fichiers download/ supprimé — le corpus n'est publié que via l'archive d'intégrité ; directive utilisateur déduplication « même nom, même contexte, idempotent », session web-8a7e5653) ; ligne doctrine harness (§7 registre) — arbitres recalibrés (sync-download retiré, certification-complete ajouté). 2026-10-02 (montée PM-INSTALL v1.2.0) — **v1.6.2** : §6.1 — référence PM-INSTALL portée à v1.2.0 (dérivation dynamique « PM le plus récent » généralisée aux 3 familles + garde anti-rétrogradation R2 au §3.2 du PM-INSTALL — directive utilisateur, session web-8a7e5653, Task 13) ; drift résiduel v1.1.0→v1.1.1 de la ligne §6.1 résorbé au passage. 2026-10-02 (fusion installateurs v1.1.0) — **v1.6.1** : §6.1 — PROMPT-MAITRE-INSTALL-ECOSYSTEME.md devient la SOURCE D'INSTALLATION UNIQUE v1.1.0 (fusion du périmètre d'INSTALL-ECOSYSTEME.md, supprimé — directive utilisateur, R4) ; §1.2 note A18 actualisée — miroir d'installation local `skills/_prompts-maitres/` supprimé (exécution décision d'architecture v2.0, round-trip archive v2.1 fait foi). 2026-09-19 (session B12-r41) — **v1.6.0** : §8 Règles Fondamentales (4 règles Karpathy adaptées — propositions-qwen.md §2.2, phase N20, marqueur d'idempotence, contenu reconstitué avec transparence : le détail exact était élague par le composant de rendu Qwen, constat N19). (session A21) — **v1.5.2** : §1.2 codification du préfixe « @ » — `mon-ecosysteme/` → `@mon-ecosysteme/` (dépôt GitHub bigleon2/KNOWLEDGE, session A20, commit 1519bbe) : le préfixe « @ » (ASCII 64) précède les lettres au tri alphabétique, le dossier s'affiche en tête du listing skills/ du dépôt ; le canonique local et le miroir GitHub portent le même nom ; le nom du skill d'infrastructure `script-mon-ecosysteme-infrastructure` reste inchangé. (session A18) — **v1.5.1** : §1.2 codification du renommage des prompts maîtres — `_prompts-maitres/` → `mon-ecosysteme/` (dépôt GitHub bigleon2/KNOWLEDGE, session A17, commit 6995823) : le canonique local et le miroir GitHub portent désormais le même nom ; le préfixe `_` reste réservé aux dossiers d'infrastructure (miroir d'installation local `skills/_prompts-maitres/`, archive `mon-ecosysteme/_archive/`). (session A14) — **v1.5.0** : §7 heuristique de déclenchement v1 → v2 (stemmer français léger : radicalisation des mots-clés et tokens sous garde de collision avec les cas négatifs officiels — itération-6 : 40/40 v1 et v2, 3 gains v2 uniques, 0 faux positif ; cas trigger_evals inchangés). (session A12-1) — **v1.4.0** : §7 matérialisation des 4 disciplines d'exécution en skills complets à déclenchement automatique (levée de la réserve A11 « agents sans trigger_evals — évaluer matérialisation skill si déclenchement requis ») ; §1.2 : matérialisations agent `_disciplines/` retirées ; registre d'assignation étendu. (session A12-PRÉ) — §6.1 : PM gen-plan v3.10.0 (règles d'or n°2-n°3, gestion du plan d'actions de session — directive utilisateur). 2026-09-06 (session A11) — §7 réécrit : les 5 disciplines d'ingénierie de prompts sont implantées dans SHARED en tant que **source de vérité** (définitions ancrées état de l'art 2025-2026, registre d'assignation, matérialisations `{{SKILLS_ROOT}}_disciplines/` + prompt-engineering) ; §1.2 : exception infrastructure `_disciplines/` ; §6.1 : PM gen-plan v3.9.0. 2026-09-06 — §6.1 : PM gen-plan v3.8.1 / correct-work v2.5.1 (Description Optimization : enrichissement des descriptions frontmatter, itération-3 workspaces — session A10) ; §7 : référence méthode-mère actualisée (PM v3.8.1 §1.9). Révision précédente : 2026-09-06 — §6.1 : PM gen-plan v3.8.0 / correct-work v2.5.0 (révision unifiant le schéma evals skill-creator au §5 des PMs, recommandation clone 2026-09-06) ; §7 : matérialisation de prompt-engineering et de la couche agent gen-plan (references/gen-plan.agent). Révision antérieure : 2026-09-05 (§3.2 complétée, planchers gradués). Modèle de toilettage : révision de prompt sans changement de version (précédent clone-chat, révision prompt 1.0.1) Révision antérieure : 2026-09-05 (§3.2 complétée, planchers gradués).
> **Date** : 2026-08-30
> **Source** : Écosystème Knowledge — Clone de discussion
> **Usage** : Ce fichier doit être lu en premier avant tout prompt maître spécifique (gen-plan, correct-work, etc.)

---

## §0 — Règle zéro (Contexte commun)

L'écosystème Knowledge est un ensemble de 80 skills conçus pour un assistant IA (9 skills écosystème — dont 2 skills d'infrastructure — + 71 skills métier). Chaque skill est auto-contenu dans son répertoire sous `{{SKILLS_ROOT}}`, dispose d'un fichier `SKILL.md` principal, d'un frontmatter YAML, et de références optionnelles dans `references/`.

**Principes fondamentaux** :
- Chaque skill est versionné sémantiquement (MAJEUR.MINEUR.PATCH)
- Les dépendances inter-skills sont déclarées dans le frontmatter YAML avec versions minimales
- Les cross-references entre skills doivent être maintenues bidirectionnellement
- Le registre KB (`KNOWLEDGE.md`) est la source de vérité pour l'état de l'écosystème

---

## §1 — Conventions écosystème

### §1.1 Variables d'installation

| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine du répertoire des skills |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Chemin vers le registre KB |
| `{{KB_ENABLED}}` | `true` | Activation/désactivation du registre KB |
| `{{PROFILE_DEFAULT}}` | `NORMAL` | Profil ressource par défaut |

### §1.2 Conventions de nommage

- **Répertoires** : kebab-case (`gen-plan`, `correct-work`, `clone-chat`). Exception : le dossier des prompts maîtres `@mon-ecosysteme/` = pas un skill, pas de `SKILL.md` ; `@mon-ecosysteme/_archive/` = archive des anciens PMs, pas des skills actifs. Note session A21 : préfixe « @ » appliqué (session A20, commit 1519bbe) — « @ » (ASCII 64) précède les lettres au tri alphabétique, dossier en tête du listing skills/ du dépôt ; le canonique local et le miroir GitHub portent le même nom. Note session A18 : renommé depuis `_prompts-maitres/` (session A17, dépôt GitHub) ; le préfixe `_` reste réservé aux dossiers d'infrastructure (miroir d'installation local `skills/_prompts-maitres/` — supprimé 2026-10-02, décision d'architecture v2.0 exécutée, fusion installateurs v1.1.0). Note session A12 : les matérialisations agent `_disciplines/` (session A11) sont retirées — les 4 disciplines d'exécution sont désormais des skills actifs à part entière (voir §7).
- **Fichiers** : kebab-case avec extension (`SKILL.md`, `etapes-detaillees.md`, `evals.json`)
- **Versions** : format semver (`3.6.1`, `2.4.0`)
- **Tags** : préfixe `#` pour les tokens (`#token 3500`)
- **Variables** : double accolades (`{{SKILLS_ROOT}}`)

### §1.3 Conventions YAML frontmatter

> 📎 **Décentralisé** (Architecture v2.0) : voir `skills/skill-creator/SKILL.md` §2 pour la spécification complète.

### §1.4 Format worklog

> 📎 **Décentralisé** (Architecture v2.0) : voir `skills/agent-creator/SKILL.md` §6.1.

---

## §2 — Registre KB (KNOWLEDGE.md)

### §2.1 Rôle

`KNOWLEDGE.md` est le registre central de l'écosystème. Il contient :
- La liste de tous les skills installés avec leurs versions
- Les relations inter-skills
- Les métadonnées de calibration
- L'historique des interactions

### §2.2 Format d'une entrée (template)

> 📎 **Décentralisé** (Architecture v2.0) : voir `skills/skills-inventory/SKILL.md` §2.1.

### §2.3 Protocole de Découverte

> 📎 **Décentralisé** (Architecture v2.0) : voir `skills/skills-inventory/SKILL.md` §2.2.

---

## §3 — Registre des relations inter-skills

### §3.1 Tableau complet

| Skill A | Relation | Skill B | Nature | Détails |
|---------|----------|---------|--------|--------|
| gen-plan | invoque | correct-work | Étape 1 + E8 hook + contrôle par phase | Validation plan + vérification post-plan et par phase, >= v2.4.0 |
| gen-plan | utilise | clone-chat | Calibration + archivage | E4, E15, optionnel, >= v2.0.0 |
| gen-plan | consulte | skills-inventory | Sélection skills | E5, >= v1.0.0 |
| gen-plan | enrichit | KNOWLEDGE.md | Calibration | E15, mise à jour registre |
| correct-work | utilise | gen-plan | Plan de vérification | Étape 1, >= v3.7.0 |
| correct-work | vérifie | clone-chat | Mode CIBLE | §3.5 Context Drift, >= v2.0.0 |
| correct-work | vérifie | fullstack-dev | Projets web | Structure et dépendances |
| clone-chat | archivé par | gen-plan | Sessions longues | Optionnel, >= v3.6.1 |
| clone-chat | vérifié par | correct-work | Validation croisée | §3.5 drift, >= v2.0.0 |
| clone-chat | conventions par | skill-creator | Conventions structurelles | >= v1.0.0 |
| agent-creator | utilise | gen-plan | Planification | Tâches complexes, >= v3.6.0 |
| agent-creator | persist via | clone-chat | État Long | Inter-sessions, optionnel, >= v2.0.0 |
| agent-creator | vérifié par | correct-work | Validation | Cohérence agent, >= v2.4.0 |
| agent-creator | consulte | skills-inventory | Découverte agents | Sélection, >= v1.0.0 |
| clone-chat | enrichit | KNOWLEDGE.md | Enrichissement KB | Lecture + enrichissement, descriptions §2, >= v2.0.0 |
| clone-chat | consulte | skills-inventory | Descriptions skills | Enrichissement §2 du clone, >= v1.0.0 |
| skills-inventory | scanne | KNOWLEDGE.md | Registre source | Inventaire et calibration, >= v1.0.0 |
| skill-creator | validé par | correct-work | Conformité | Check 8 frontmatter métier, >= v2.4.0 |
| correct-work | vérifie | gen-plan | Mode PROJET | SKILL.md, refs, evals, >= v3.7.0 |
| install-ecosystem | utilise | script-mon-ecosysteme-infrastructure | Déploiement | P6-P7, bootstrap v1.1.0, >= v1.0.0 |
| gen-plan | délègue | prompt-engineering | Optimisation prompts | §1.9, prompts complexes, >= v1.0.0 |
| prompt-engineering | consulte | gen-plan | Contexte écosystème | Planification E1-E8, >= v3.7.0 |
| gen-plan | invoque | knowledge-observer | Observation post-session | E15 (modes M1-M2), >= v1.0.0 |
| knowledge-observer | valide par | correct-work | Étape F du cycle A-H | Validation des lessons, >= v2.6.0 |

### §3.2 Règles de cross-references

> 📎 **Décentralisé** (Architecture v2.0) : voir `skills/correct-work/SKILL.md` §3.2.

---

## §4 — Matrice agent × skill (statique)

Cette matrice définit quels agents peuvent utiliser quels skills et dans quel contexte.

### §4.1 Matrice principale

> 📎 **Décentralisée** (Architecture v2.0) : matrice complète + légende des droits dans `skills/agent-creator/SKILL.md` §6.2.

### §4.3 Droits spécifiques de agent-creator

| Agent | Droits | Détails |
|-------|--------|---------|
| **agent-creator** | Exécution autonome + création d'agents (règles AG-1..AG-3, `agent-creator` §6.3) | utilise gen-plan >= v3.6.0 · persist via clone-chat >= v2.0.0 · consulte skills-inventory >= v1.0.0 · vérifié par correct-work >= v2.4.0 |
| **4 disciplines** (context/loop/graph/harness-engineering) | Déclenchement automatique — application dédiée de leur discipline | Matérialisations skills (SHARED §7) ; invoquées sans commande manuelle dès que la demande touche leur périmètre |

### §4.4 Règles de création d'agents et gardes anti-boucle

1. Toute création d'agent suit **AG-1/AG-2/AG-3** (`skills/agent-creator/SKILL.md` §6.3) : Contexte Système N2 obligatoire, enregistrement KB, gardes déclarées.
2. **Garde anti-boucle** : max **2 rounds** de correction par artefact (correct-work) — au-delà, escalade Mode PROJET + journalisation worklog (cause, coût #token, décision).
3. Tout agent généré est vérifié par correct-work Mode CIBLE avant enregistrement définitif ; non-régression contrôlée par `verify-cross.py --check-context`.

---

## §5 — Format du fichier SKILL.md (conventions structurelles)

> 📎 **Décentralisé** (Architecture v2.0) : voir `skills/skill-creator/SKILL.md` §3 (structure type + tailles cibles) et §3.0 (règle impérative Contexte Système).

---

## §6 — Prompt maîtres : architecture et workflow

### §6.1 Fichiers

| Fichier | Rôle | Version skill |
|---------|------|---------------|
| `PROMPT-MAITRE-SHARED.md` | Socle commun (ce fichier) | — |
| `PROMPT-MAITRE-GEN-PLAN-v3.18.0.md` | Spécification gen-plan (PM le plus récent du corpus — dérivation dynamique KO-L003, harmonisation Task 14) | v3.18.0 |
| `PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` | Spécification correct-work (PM le plus récent du corpus — v2.6.0/v2.7.0 matérialisés Task 16, reconstitution méthode B1 documentée §7 du PM) | v2.7.0 |
| `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | Spécification clone-chat | v2.0.0 |
| `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | Pipeline d'installation — SOURCE UNIQUE (périmètre §A + ordre optimal 10 étapes ; fusion v1.1.0 ; dérivation dynamique 3 familles + garde anti-rétrogradation v1.2.0 ; déduplication download/ — canal de fichiers supprimé, v1.3.0 ; cas d'espèce R2 correct-work résorbé, v1.3.1) | v1.3.1 |
| `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` | Orchestration à l'usage — routeur dérivé dynamiquement (généré idempotent gen-ultra-maitre.py) | v1.0.0 |

### §6.2 Workflow d'utilisation

1. **Les prompts maîtres sont auto-porteurs** (Architecture v2.0) : le Contexte Système est embarqué dans chaque prompt maître — aucune lecture externe n'est requise
2. **Lire le prompt maître spécifique** (gen-plan, correct-work ou clone-chat)
3. Suivre les instructions d'installation du fichier spécifique
4. Utiliser les références vers SHARED pour éviter la duplication
5. Mettre à jour KNOWLEDGE.md et les cross-references (SHARED §2.2 et §3.2)

### §6.3 Maintenance

- Toute modification d'une info commune (convention, relation, variable) se fait **une seule fois** dans SHARED
- Les prompts spécifiques contiennent uniquement la logique propre à leur skill
- La vérification croisée régulière garantit la cohérence (relations bidirectionnelles, versions)

## §7 — Disciplines d'ingénierie de prompts (source de vérité)

Implantation (session A11, 2026-09-06 — directive utilisateur) : les cinq disciplines de l'ingénierie de prompts sont des **informations communes** à tous les skills (règle §6.3) ; leurs définitions sont implantées dans le présent §7, qui en est la **source de vérité**. Le PM gen-plan (§1.9) enregistre uniquement l'**orchestration gen-plan** des disciplines (mécanismes appliqués à E1-E15) ; les autres skills les détiennent en **fonction héritée** (registre d'assignation ci-dessous), sans les redéfinir. **Matérialisations (session A12, 2026-09-07 — levée de la réserve A11)** : les 4 disciplines d'exécution sont matérialisées en **skills complets** (`{{SKILLS_ROOT}}context-engineering/`, `loop-engineering/`, `graph-engineering/`, `harness-engineering/` — SKILL.md + evals/evals.json + evals/trigger_evals.json) dotés d'un **déclenchement automatique** : chaque skill embarque ses trigger_evals (Description Optimization, heuristique v2 — mots-clés = nom du skill normalisé découpé sur « - » + mots de la description ; radicalisation légère : stemmer français déterministe (suffixes nominaux/adjectivaux) appliqué aux mots-clés et aux tokens de requête, sous garde de collision avec les cas négatifs officiels du même skill — la distinction de forme qui porte la calibration est préservée ; session A14) calibrés en workspaces skill-creator pour se déclencher sans invocation manuelle. La matérialisation intermédiaire en agents (`{{SKILLS_ROOT}}_disciplines/*.agent`, session A11) est **retirée** (SHA prouvés avant retrait — contenu normatif repris dans les SKILL.md). La discipline prompt-engineering demeure matérialisée en skill spécialisé (`prompt-engineering`).

| Discipline | Définition (ancrage état de l'art 2025-2026) | Implantation écosystème | Matérialisation |
|------------|-----------------------------------------------|--------------------------|-----------------|
| **Prompt engineering** (méthode-mère) | Méthodes de rédaction et d'organisation des instructions d'un LLM ; en 2026, les prompts sont des artefacts **versionnés, testés et conscients de leur environnement** — le corpus PM (versionné, scellé, evals, workspaces) en est l'incarnation. Insuffisante seule, elle se compose avec les 4 disciplines ci-dessous. | PM gen-plan §1.9 (orchestration) ; corpus PM scellé ; opérations fines : prompt-engineering | Skill `prompt-engineering` v1.0.1 |
| **Context engineering** | Décider ce que le système lit avant de répondre : curation de la fenêtre de contexte (budget d'attention), compaction, clairage juste-à-temps, mémoire externe. | SHARED §0-§2 (socle lu en premier ; Protocole de Découverte = clairage juste-à-temps) ; gen-plan §1.7 #7 (lecture bloc par bloc = compaction) ; mémoire EC/EL (agent-creator) | Skill `context-engineering` v1.0.0 (déclenchement automatique) |
| **Loop engineering** | Structurer les actions en cycles itératifs à feedback : boucle d'exécution, boucle de vérification (graders déterministes ou agentiques, feedback exploitable), boucle externe (chaque cycle rend les boucles internes plus efficaces). | gen-plan E10-E13 (exécution) ; hooks correct-work E8 + E9-E14 (vérification, graders déterministes S1-S4) ; E15 auto-calibration + workspaces skill-creator (boucle externe) | Skill `loop-engineering` v1.0.0 (déclenchement automatique) |
| **Graph engineering** | Construire et maintenir des graphes de connaissances (nœuds, arêtes, schéma) pour ancrer les décisions dans des faits enregistrés (anti-hallucination). | SHARED §2 (KB = graphe : nœuds skills, schéma template §2.2) ; §3.1-§3.2 (arêtes = relations bidirectionnelles versionnées, planchers) ; §4 (matrice agent × skill) ; Protocole de Découverte = requête graphe | Skill `graph-engineering` v1.0.0 (déclenchement automatique) |
| **Harness engineering** | Le harnais est un **artefact réel** : outillage, gardes-fous, boucles de feedback qui transforment un modèle en agent — versionné et **resserré à chaque dérive constatée**. | Arbitres (verify-cross, verify-correct-work, spell-check, certification-complete, check-ecosysteme-integrity, verify-by-sha) ; profils ressource + signaux de pression (gen-plan §2.4) ; worklog SHARED §1.4 ; règle d'or n°1 ; idempotence R1-R6 | Skill `harness-engineering` v1.0.0 (déclenchement automatique) |

**Registre d'assignation** :

| Détenteur | Mode de détention | Usage |
|-----------|-------------------|-------|
| `gen-plan` | **Application principale** (méthode-mère, lignage historique) — orchestration : PM gen-plan v3.12.0 §1.9 | Applique les 5 disciplines à E1-E15 ; délègue l'optimisation fine à `prompt-engineering` (SHARED §3.1) |
| `correct-work` | **Fonction héritée** (déclaration : PM §B) | Lecture et validation d'artefacts de prompts (specs, SKILL.md, rapports de vérification) |
| `clone-chat` | **Fonction héritée** (déclaration : PM §B) | Assemblage de documents-clones, produits d'ingénierie de prompts |
| `prompt-engineering` | Compétence spécialisée (SHARED §3.1 ; matérialisé 2026-09-06 : SKILL.md + evals + trigger_evals) | Optimisation fine des prompts complexes (délégation gen-plan) |
| `agent-creator` | Fonction héritée (auto-définition : `references/agent-creator.agent` §2.3) | Contexte (mémoire EC/EL) et boucles (pipeline A-H) |
| `context-engineering` / `loop-engineering` / `graph-engineering` / `harness-engineering` | **Matérialisations skills des disciplines** (session A12 : SKILL.md + evals + trigger_evals — déclenchement automatique ; remplacement des agents `_disciplines/` A11) | Application dédiée de leur discipline respective dans les sessions d'ingénierie ; socle normatif : présent §7 |
| `fleet-engineering` / `spec-driven-development` / `memory-engineering` | **Matérialisations skills des disciplines n°54** (N34, Tasks 16-18 : SKILL.md + evals + trigger_evals — déclenchement automatique ; détention orchestrée : registre décentralisé §8 du skill + registre KB) | Application dédiée (orchestration de flottes d'agents ; développement piloté par specs ; mémoire longue de session) — orchestration gen-plan §1.9 |

Toute évolution d'une discipline se fait dans le présent §7 (source de vérité) ; le PM gen-plan §1.9 enregistre uniquement l'orchestration. Déclenchement automatique (session A12) : les 4 skills de discipline sont invoqués sans commande manuelle dès qu'une demande touche leur périmètre — la calibration des triggers (heuristique v2, session A14) est rejouée à chaque itération de workspaces (non-régression : gen-plan 9/9, correct-work 8/8, prompt-engineering 7/7, 4 disciplines 4/4 ×4). Les fichiers documentaires (README.md, INSTALL-ECOSYSTEME.md) décrivent les disciplines sans les détenir ; le corpus figé (`PROMPT-MAITRE-GEN-PLAN-v3.6.1.md`, Annexe B du PDF) n'est pas modifiable. Ancrage externe (recherche web ciblée, session A11 — preuves : `data/audit/a11_disciplines/recherche/`) : Anthropic, « Effective context engineering for AI agents » (2025) ; LangChain, « The Art of Loop Engineering » (2026) ; M. Fowler, « Harness engineering for coding agent users » ; A. Osmani, « Agent Harness Engineering » (2026) ; Databricks, « What is an AI Agent Harness? » ; GraphRAG (InfoQ, 2026).

## §8 — Règles Fondamentales (source de vérité)

<!-- PATTERN:SHARED-8-FONDAMENTALES-v1.0.0 -->

> Ajouté phase N20 (session B12-r41, 2026-09-19) — intégration des propositions-qwen.md §2.2
> (« Ajouter §8 Règles Fondamentales — 4 règles Karpathy adaptées »). **Transparence** : le détail
> exact des 4 règles était élague par le composant de rendu Qwen (constat N19) ; le contenu
> ci-dessous est une adaptation cohérente avec les principes publics de Karpathy et avec
> l'écosystème (règle N1 auto-portance). Idempotent : ne jamais dupliquer ce marqueur.

Les 4 règles fondamentales s'appliquent à tous les skills, prompts maîtres et sessions —
elles sont la distillation transversale des mécanismes existants (philosophie gen-plan §1.4,
idempotence R1-R6, arbitres, B-11) :

| # | Règle | Définition | Ancrage écosystème |
|---|-------|------------|--------------------|
| **R-F1** | **Simplicité d'abord** | La solution la plus simple qui satisfait les critères vérifiables prévaut — pas de mécanisme additionnel sans bénéfice mesuré. | gen-plan §1.4 (économie), SHARED §6.3 (non-duplication) |
| **R-F2** | **Vérification mécanique > confiance** | La conformité se prouve par exécution (arbitres, answer key, evals), jamais par intuition ou auto-déclaration. | arbitres (verify-cross, integrity, interactions), answer-key-checker, evals |
| **R-F3** | **Lire avant d'écrire** | Tout artefact est lu intégralement avant modification ; le filesystem fait foi sur tout résumé de contexte hérité. | B-11 (lecture seule préalable), règle zéro §0 |
| **R-F4** | **Boucles courtes** | Itérer par cycles courts à feedback rapide ; chaque cycle resserre le harnais (dérive détectée → correction immédiate). | loop-engineering (SHARED §7), hooks E9-E14, boucles R3 |

Toute évolution des règles fondamentales se fait dans le présent §8 (source de vérité) —
les skills les citent sans les redéfinir (règle §6.3, non-duplication).

<!-- FIN-PATTERN:SHARED-8-FONDAMENTALES-v1.0.0 -->
