# PROMPT MAÎTRE — Pipeline d'installation de l'écosystème personnel

Version : 1.3.0
Date : 2026-10-02
Fusionne : INSTALL-ECOSYSTEME.md v1.0.0 (périmètre §A — supprimé, directive utilisateur « source d'installation unique »)
Répare : le bloc CONTEXTE SYSTÈME embarqué, corrompu depuis le sync b13-r7-c (table dupliquée cassée, résolu par git @1519bbe)
Dépend : CONTEXTE SYSTÈME (embarqué ci-dessous)
Complète : ce fichier est l'UNIQUE source d'installation de l'écosystème — périmètre (§A) + ordre d'exécution optimal (§2) + critères de passage (§3).
Fonction héritée (SHARED §7) : ce pipeline applique la méthode prompt-engineering (méthode-mère : gen-plan, PM v3.7.0 §1.9) en tant que fonction héritée — chaque étape est un artefact de prompt (entrée, instruction, arbitre, sortie).

---
## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v1.6.1)
> **INSTRUCTION** : Ce bloc remplace la dépendance de lecture externe.

### Règle Zéro (§0)
L'écosystème Knowledge est un ensemble de 80 skills conçus pour un assistant IA.

### Variables d'installation (§1.1)
| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Registre KB |

### Conventions de nommage (§1.2)
- **Répertoires** : kebab-case
- **Fichiers** : kebab-case avec extension
- **Versions** : format semver

---

---

## §0 — Objet et règle zéro

Ce fichier est la **source de vérité unique de l'installation** — périmètre et ordre — pour installer l'écosystème Knowledge de façon optimale, reproductible et vérifiable, à partir du seul contenu du répertoire `@mon-ecosysteme/`. Il synthétise le pipeline complet en une référence unique et fusionne le contenu du fichier `INSTALL-ECOSYSTEME.md` v1.0.0 (périmètre, §A ci-dessous), supprimé le 2026-10-02 pour mettre fin à la double source d'installation (R4 anti-duplication).

Règle zéro (SHARED §0) : skills auto-contenus sous `{{SKILLS_ROOT}}`, registre KB (`{{KB_PATH}}`) comme source de vérité, cross-references bidirectionnelles, conventions de nommage SHARED §1.2. Aucune étape ne produit d'effet public avant le passage des arbitres (§4).

Variables (SHARED §1.1) : `{{SKILLS_ROOT}}` = `skills/` · `{{KB_PATH}}` = `skills/KNOWLEDGE.md` · `{{KB_ENABLED}}` = `true` · `{{PROFILE_DEFAULT}}` = `NORMAL`.

## §1 — Pourquoi cet ordre (principe de dépendance)

L'ordre dérive du graphe d'interactions cartographié (README §8, SHARED §3.1) :

1. **Rien ne s'interprète sans le socle** — chaque fichier spécifique ouvre par « Lire SHARED en premier » (§B) → SHARED est l'étape 1.
2. **Rien ne s'installe depuis un corpus non authentifié** — les formes installées sont assemblées DEPUIS les PMs ; si le corpus est corrompu, tout le reste l'est → intégrité en étape 2.
3. **L'archive garantit la byte-identité** — l'intégrité du corpus est vérifiée par le round-trip de `download/mon-ecosysteme_archive.zip` (véhicule d'intégrité v2.2 ; décisions d'architecture v2.0 et v2.2 : miroir local `skills/_prompts-maitres/` supprimé, puis canal de fichiers download/ supprimé — le corpus n'est publié que via l'archive) → étape 2.
4. **gen-plan avant les skills qu'il orchestre** — correct-work (Étape 1 : gen-plan obligatoire) et clone-chat (§2.6 : intégration optionnelle) s'enregistrent auprès d'un gen-plan présent → étape 4.
5. **correct-work et clone-chat après gen-plan** — l'ordre P4-b/P4-c respecte le précédent validé (worklog A2/A3) et la direction de dépendance dominante (gen-plan —invoque→ correct-work) → étapes 5-6.
6. **Le registre KB après les skills** — KNOWLEDGE.md décrit les skills installés ; une entrée sans skill installé est une référence morte → étape 7.
7. **L'outillage avant la certification** — les arbitres vérifient l'état installé, ils ne le précèdent pas → étape 8.
8. **Rien ne se publie sans certification** — archives et clones ne sont produits qu'après verdicts PASS (le canal de fichiers download/ est supprimé — décision d'architecture v2.2, déduplication Task 14 : le corpus n'est publié que via l'archive d'intégrité) → étapes 9-10.

## §2 — Le pipeline en 10 étapes (ordre d'exécution optimal)

| # | Étape | Source → Destination | Arbitre | Critère de passage |
|---|-------|----------------------|---------|--------------------|
| 0 | **Contexte** | Lire PROMPT-MAITRE-SHARED.md (§0-§7) | — | Conventions, variables, relations connues |
| 1 | **Corpus** | Vérifier `@mon-ecosysteme/` (corpus canonique, invariant `CORPUS_ATTENDU` du checker) | SHAs corpus vs archive scellée (check-ecosysteme-integrity.py) | N/N présents, byte-identité corpus OK |
| 2 | **Archive** | Round-trip `download/mon-ecosysteme_archive.zip` ↔ corpus (miroir supprimé, décision d'architecture v2.0 ; canal de fichiers download/ supprimé, décision v2.2) | check-ecosysteme-integrity.py §2 | corpus ⊆ archive byte-identique + extras homologues/ |
| 3 | **gen-plan** | PM gen-plan le plus récent §5 → `skills/gen-plan/` : SKILL.md + `references/` (extraction §9, fences incluses) + `evals/` | Checks §6 du PM | Lignes ±tolérance ; refs présentes ; JSON valide |
| 4 | **correct-work** | PM correct-work le plus récent §5 → `skills/correct-work/SKILL.md` (assemblage §4+§A+§1+§2+§3+§10) | Checks §6 du PM | ~200-400 L ; 3 modes ; 5 étapes |
| 5 | **clone-chat** | PM clone-chat le plus récent §5 → `skills/clone-chat/SKILL.md` (assemblage §4+§A+§1+§2+§3+§5) + `références/clone-template.md` (§9.1) | Checks §6 du PM | ~300-450 L ; 7+1 étapes ; template présent |
| 6 | **Registre KB** | §A.3 (ce fichier) → `skills/KNOWLEDGE.md` (14 entrées écosystème cibles) | Compte d'entrées + formats §2.2 SHARED | ≥ 14 entrées, versions = règle §A.3 |
| 7 | **Outillage** | Déployer `scripts/` : verify-cross.py, check-ecosysteme-integrity.py, certification-complete.py, arbitres dédiés | python -c import (syntaxe) | scripts exécutables |
| 8 | **Certification** | Exécuter dans l'ordre : (a) verify-cross.py → (b) correct-work Mode PROJET → (c) check-ecosysteme-integrity.py | Les 3 arbitres eux-mêmes | 0 FAIL ; 0 S1-S2 ; N/N byte-identique |
| 9 | **Publication** | Archive zip (round-trip byte-identique) + worklog — canal de fichiers download/ supprimé (décision v2.2 : aucun fichier du corpus ne doit exister en double dans `download/`, garde `scripts/task14-scan-doublons.py`) | Vérif round-trip byte-identique + scan doublons 0 | N/N round-trip OK ; 0 doublon download/ |
| 10 | **Clôture** | clone-chat (archivage session) + mise à jour KNOWLEDGE.md si nouveau skill | 8 checks S1-S8 clone-chat | Clone scellé, idempotent |

Note (correct-work CIBLE, 2026-09-06, S3 ; révisée session A9, 2026-09-06) : les skills sans prompt maître propre — `skills-inventory`, `skill-creator`, `agent-creator`, `fullstack-dev` — n'ont pas de forme installée locale : ils existent comme entrées du registre KB (étape 6) et sont mobilisés à l'exécution, pas à l'installation. `prompt-engineering` est désormais MATÉRIALISÉ (forme installée `prompt-engineering/` : SKILL.md + evals/evals.json + evals/trigger_evals.json + references/grille-evaluation-prompt.md ; recommandation clone 2026-09-06 §5.2 exécutée).

Note (recalibrage v1.1.0, 2026-10-02) : les comptes et versions d'époque (15 fichiers, 7 fichiers cœur, PM gen-plan v3.7.0, arbitres 60/60) sont remplacés par des invariants dynamiques (KO-L003) : l'invariant `CORPUS_ATTENDU` du checker fait foi pour la taille du corpus ; « PM le plus récent » se dérive du listing réel du corpus ; les critères numériques sont les verdicts des arbitres courants.

## §3 — Détail des points de contrôle critiques

### §3.1 Étape 1 — Intégrité du corpus
Comparer les SHAs SHA-256 des fichiers du corpus aux valeurs scellées dans l'archive de référence (méthode neutral-line, Annexe D du PDF source ; canal R-1 = README §13, référence historique). Toute divergence = STOP : restaurer depuis `download/mon-ecosysteme_archive.zip` ou le stockage versionné avant de reprendre au contrôle 1.

### §3.2 Étapes 3-5 — Assemblage des formes installées
Les SKILL.md sont ASSEMBLÉS depuis les PMs (jamais copiés à l'aveugle) : YAML frontmatter (§4 du PM) + règle zéro + spécifications (§1-§2) + relations (§3) + sections spécifiques. Les fichiers de référence sont extraits des blocs ```` ```markdown ```` du §9 avec fences incluses (round-trip déterministe, leçon A2) — l'extraction doit être insensible aux titres internes des blocs (logique de balance des fences).

**Dérivation « PM le plus récent » (v1.2.0, KO-L003)** : le PM source de chaque famille (gen-plan, correct-work, clone-chat) est le plus récent du corpus, dérivé du listing réel de `@mon-ecosysteme/` par tri semver des suffixes `-vX.Y.Z.md` — jamais d'un numéro figé. **Garde anti-rétrogradation (R2)** : si la version du PM dérivé est inférieure à celle du SKILL.md installé (`skills/<famille>/`, frontmatter = source de vérité), la forme installée est conservée inchangée — l'assemblage ne rétrograde jamais — et l'écart est journalisé au worklog ; l'entrée KB (étape 6) porte la version installée. Cas d'espèce au jour de la v1.2.0 : correct-work — corpus v2.5.1, installé v2.7.0 (PMs v2.6.0/v2.7.0 non matérialisés au corpus, R2 corpus figé) → l'étape 4 conserve v2.7.0.

### §3.3 Étape 8 — Arbitres et sévérité
L'ordre (a)→(b)→(c) est contraint : verify-cross valide la structure (rapide, déterministe), correct-work valide le raisonnement (coûteux, ne s'exécute que si la structure est saine), check-ecosysteme-integrity valide l'authenticité (corpus ↔ archive ↔ registre). Toute sévérité S1 (critique) ou S2 (majeure) à l'étape 8 = retour à l'étape correspondante du pipeline ; S3/S4 = journalisation au worklog + reprise.

### §3.4 Incidents (règle d'or n°1, PM gen-plan §1.8)
Tout blocage (fichier absent, wipe inter-sessions, outil perdu) = signal d'adaptation, jamais un arrêt : contournement conforme aux conventions, journalisation au worklog (cause, solution, coût #token), reprise à l'étape en échec. Le wipe inter-sessions est un cas documenté : ré-exécuter ce pipeline depuis l'étape 2 (le corpus `@mon-ecosysteme/` est la source de vérité restaurable).

## §4 — Interactions mobilisées par le pipeline (cartographie T2)

| Interaction | Mobilisée aux étapes | Nature |
|-------------|----------------------|--------|
| gen-plan —invoque→ correct-work | 3, 8(b) | E1 + hook E8 + contrôle par phase |
| gen-plan —utilise→ clone-chat | 3, 10 | E4, E15 (optionnel) |
| correct-work —utilise→ gen-plan | 4, 8(b) | Plan de vérification (obligatoire, dernière version) |
| correct-work —vérifie→ clone-chat | 5, 10 | Mode CIBLE (drifts) |
| clone-chat —enrichit→ KNOWLEDGE.md | 6, 10 | Descriptions §2 |
| skills-inventory —scanne→ KNOWLEDGE.md | 6 | Registre source |
| install-ecosystem —utilise→ infrastructure | 2-7 | Déploiement P6-P7 |
| gen-plan —délègue→ prompt-engineering | 0-10 | Optimisation fine des prompts |

## §5 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| PROMPT-MAITRE-SHARED.md | Socle | Conventions, variables, registre relations (§3.1), méthode prompt-engineering (§7) |
| (fusion v1.1.0) | Périmètre absorbé | INSTALL-ECOSYSTEME.md v1.0.0 supprimé 2026-10-02 — son périmètre est porté par le §A de ce fichier ; recréer un second installateur est interdit (R4) |
| PM gen-plan le plus récent | Spécification | Étape 3 (méthode-mère prompt-engineering, §1.9) |
| PM correct-work le plus récent | Spécification | Étape 4 + arbitre étape 8(b) |
| PM clone-chat le plus récent | Spécification | Étape 5 + clôture étape 10 |
| PROMPT-ULTRA-MAITRE-ORCHESTRATION.md | Route à l'usage (généré idempotent) | Point d'entrée d'orchestration globale — route chaque demande vers les PMs/skills sans dupliquer leur contenu (v1.0.0, 2026-10-02) ; ce fichier reste la source d'INSTALLATION, l'orchestrateur ne remplace aucun PM |
| README.md | Documentation | §9 architecture, §10 workflows, §12 verify-cross, §13 canal R-1 |

## §6 — Maintenance

- Toute évolution du périmètre (nouveau PM, nouveau skill) se traduit par : mise à jour de la table §2 + du §A + entrée KNOWLEDGE.md + cross-references bidirectionnelles (SHARED §3.2).
- L'ordre des étapes 3-5 suit le précédent P4-a/P4-b/P4-c ; il ne doit être modifié qu'avec un changement de contrat documenté (SHARED §3.2 règle 5).
- Ce fichier est l'UNIQUE source d'installation (documentaire et orchestration) : il ne détient pas la méthode prompt-engineering (fonction héritée, SHARED §7), ne remplace pas les §5 des PMs, et la recréation d'un fichier d'installation parallèle est interdite (R4 anti-duplication — leçon de la fusion v1.1.0).

## §7 — Historique

| Version | Date | Changements |
|---------|------|-------------|
| v1.3.0 | 2026-10-02 | Directive utilisateur (déduplication « même nom, même contexte, idempotent ») : décision d'architecture v2.2 — le canal de fichiers download/ est supprimé, les 14 fichiers corpus répliqués dans download/ sont effacés (le corpus n'est publié que via l'archive d'intégrité, véhicule v2.2) ; étape 7 recalibrée (sync-download.py retiré → certification-complete.py) ; étape 9 recentrée archive + garde anti-doublons `scripts/task14-scan-doublons.py` (0 doublon attendu) ; recalibrage croisé KO-L004 : SHARED v1.6.3 (§6.1 + ligne harness), SYNC-CONTEXT v1.4.0 (une seule voie de diffusion), README v2.1.0, orchestrateur ULTRA régénéré, arbitres recalibrés (check 3 inversé, §7/§11d interactions), résorption des réserves trigger_evals (evals skill-creator + version-management équipés) |
| v1.2.0 | 2026-10-02 | Directive utilisateur (vérification préalable « continue mais avant vérifie… ») : généralisation de la dérivation dynamique « PM le plus récent » aux 3 familles — l'étape 5 et la relation §5 épinglaient clone-chat v2.0.0, incohérence avec la règle §A.3 (KO-L003) ; garde anti-rétrogradation R2 au §3.2 (cas correct-work : corpus v2.5.1 < installé v2.7.0 — la forme installée fait foi, jamais de rétrogradation, écart journalisé au worklog) ; recalibrage croisé KO-L004 : SHARED §6.1 (v1.6.2), orchestrateur régénéré (routage T1 clone-chat dynamisé), archive rescellée, canal download/ resynchronisé (dernière synchronisation avant sa suppression v1.3.0) |
| v1.1.1 | 2026-10-02 | Cross-ref §5 : PROMPT-ULTRA-MAITRE-ORCHESTRATION.md v1.0.0 (route à l'usage, généré idempotent) — complément de cohérence suite à vérification propriétaire « garder un prompt maître et le mettre à jour » : ce fichier EST le prompt maître d'installation conservé, mis à jour selon les demandes du jour (source unique, miroir supprimé, gen-plan obligatoire v2.7.0, périmètre §A absorbé) |
| v1.1.0 | 2026-10-02 | Fusion directive utilisateur : absorption du périmètre d'INSTALL-ECOSYSTEME.md v1.0.0 (supprimé) en §A — source d'installation unique ; réparation du bloc CONTEXTE SYSTÈME corrompu (table dupliquée cassée, contenu restauré depuis git @1519bbe) ; étape 2 « Miroir » révisée « Archive » (exécution décision d'architecture v2.0 : miroir skills/_prompts-maitres/ supprimé, round-trip archive v2.1 fait foi) ; invariants dynamiques recalibrés (KO-L003) : « PM le plus récent », CORPUS_ATTENDU, verdicts arbitres courants ; §A.3 versions dynamiques (anti-drift) ; criterion correct-work étape 1 : gen-plan obligatoire (couplage v2.7.0) |
| v1.0.0 | 2026-09-06 | Création (directive utilisateur) : pipeline 10 étapes issu de la cartographie des interactions ; principes de dépendance §1 ; critères de passage et arbitres §3 ; intégration règle d'or n°1 et canal R-1. Certification correct-work Mode CIBLE : PASS 31/31, 0 S1-S2, 1 S3 corrigée (note skills sans PM) |

## §A — Périmètre d'installation (absorbé d'INSTALL-ECOSYSTEME.md v1.0.0)

### §A.1 Périmètre général
26 fichiers répartis sur 4 zones (sommaire d'époque v1.0.0 conservé tel que documenté ; le détail zone-par-zone n'a jamais été développé dans le fichier source). Zones attestées par les référents : corpus prompts maîtres (`@mon-ecosysteme/`), formes installées (`skills/<skill>/`), registre KB (`skills/KNOWLEDGE.md`), outillage (`scripts/`).

### §A.2 Les 8 phases P0-P7
Note P4 : les SKILL.md + références des 4 skills sont créés en suivant le §5 de chaque prompt maître (ou via gen-plan). Le bootstrap install-ecosystem.py couvre P0-P3, P5-P7.

### §A.3 Registre KB cible (14 entrées)
Règle de version (recalibrage v1.1.0, anti-drift) : la version de chaque entrée est celle du PM le plus récent présent dans le corpus au moment de l'installation (dérivation dynamique — KO-L003) ; les versions figées d'époque ci-dessous (gen-plan v3.10.0, correct-work v2.5.1, prompt-engineering v1.0.1) sont des instantanés historiques et ne doivent pas être ré-installées telles quelles si le corpus porte un PM plus récent.

| Entrée KNOWLEDGE.md | Version d'époque |
|---------------------|------------------|
| gen-plan | v3.10.0 |
| correct-work | v2.5.1 |
| clone-chat | v2.0.0 |
| skills-inventory | v1.0.0 |
| skill-creator | v1.0.0 |
| agent-creator | v1.0.0 |
| script-mon-ecosysteme-infrastructure | v1.0.0 |
| install-ecosystem | v1.0.0 |
| prompt-engineering | v1.0.1 |
| verify-by-sha | v1.0.0 |
| context-engineering | v1.0.1 |
| loop-engineering | v1.0.1 |
| graph-engineering | v1.0.1 |
| harness-engineering | v1.0.1 |

Catégorie (attestée) : ecosystem — les 4 dernières matérialisations sont les skills des disciplines d'exécution (socle SHARED §7, session A12) : forme installée `<discipline>/` — SKILL.md + evals/evals.json + evals/trigger_evals.json, déclenchement automatique ; matérialisations agent `_disciplines/` retirées, SHA prouvés ; « Utilisé par » : gen-plan (couche disciplines), sessions d'ingénierie ; matérialisées 2026-09-07.
