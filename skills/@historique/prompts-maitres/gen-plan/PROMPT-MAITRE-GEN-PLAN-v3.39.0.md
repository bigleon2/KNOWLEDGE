# PROMPT MAÎTRE — Installation du skill gen-plan v3.39.0

> **Version du prompt** : 1.37.0
> **Skill cible** : gen-plan v3.39.0
> **Date** : 2026-11-07
> **Source** : Écosystème Knowledge — Clone de discussion
> **Dépend** : `PROMPT-MAITRE-SHARED.md` (lire en premier)

---

## §A — DÉCLENCHEURS (également intégré au SKILL.md depuis v3.28.0 — miroir fidèle)

> **Glossaire alias-eco inline (v3.37.0 — directive propriétaire 2026-11-07 : « fais en sorte qu'à la lecture du skill que tu n'aies pas besoin de "alias-eco" pour comprendre $FACON et $FACON2 »)** : les marqueurs alias employés dans ce PM sont définis ICI pour lecture auto-contenue — **`$FACON` = « de façon cohérente, optimisée et fonctionnelle »** (adverbe modal : la manière d'exécuter) · **`$FACON2` = « (cohérent, optimisé et fonctionnel) »** (qualificatif : la propriété attendue du livrable). Source canonique : registre alias-eco `@historique/@Alias/aliases.json` ; en cas d'écart, le glossaire fait foi pour la lecture du skill/PM, le registre pour l'expansion des messages du propriétaire ; toute évolution du registre est recalibrée ici à la montée de version suivante (cascade KO-L004).

- `gen-plan:` suivi d'une description de tâche
- `gen-plan:correct-work(projet)` — vérification et correction d'un projet complet
- `gen-plan:correct-work(<cible>)` — vérification/correction d'un élément spécifique
- `plan d'actions` — demande explicite de planification
- « intègre dans le plan d'actions » — intégration d'une nouvelle demande dans le plan courant (E13, règle d'or n°3 — extension, jamais réécriture destructrice R2 ; déclencheur verbatim v3.17.2, directive propriétaire)
- « met à jour (le plan d'actions) » — re-génération $FACON d'un NOUVEAU plan d'actions $FACON2 : consolidation de l'état vérifiable du plan courant (groupes terminés reportés avec preuves — statuts dérivés du disque : worklog, verdicts d'arbitres, livrables ; règle d'or n°5 — KO-L003) + restes-à-faire re-planifiés + nouvelles demandes (E13 intégrées à la consolidation) + re-estimation #token + answer key re-numérotée ; le NOUVEAU plan (fichier horodaté dans `download/`) devient la référence d'exécution, l'ancien est conservé (R2) ; chaîne E7-DISP complète (answer key, E8 horodatages couplés, R5, PLAN-AFFICHE) — VOIE DISTINCTE de « intègre dans le plan d'actions » (extension E13 du plan courant EN PLACE) (règle d'or n°3 — déclencheur verbatim v3.37.0, directive propriétaire 2026-11-07)
- `gen-plan(step) : <instructions>` — enchaînement autonome des groupes séquentiels du plan d'actions, correct-work(groupe) après chaque groupe (max 2 rounds de correction), correct-work(projet) en fin de chaîne (v3.22.0) ; à l'ouverture de chaque groupe : vue d'évolution PLAN-AFFICHE (E7-DISP v3.36.0 — tous modes)
- `gen-plan(step-ok) : <instructions>` — identique au mode step avec demande de confirmation du propriétaire avant chaque groupe (nom canonique v3.22.1) ; alias `step-confirm` (v3.22.0) et `step-confim` normalisés en `step-ok` (R4) ; **clause mode NULL** — toute invocation sans `<mode>` explicite (`gen-plan : <instructions>`, ex. « gen-plan : continue ») conserve le comportement antérieur à l'introduction des modes step/step-ok (v3.21.0) : intégration E13 ou exécution classique, sans portes de confirmation (directive propriétaire 2026-10-11) ; tout autre mode → clarification demandée, jamais d'invention de mode (R2)
- `orchestre` — orchestration multi-agents
- Toute demande impliquant plusieurs étapes séquentielles avec des livrables
- `gen-plan:generate(<description>)` — génération d'un plan auto-exécutable

## §B — PRÉREQUIS

Lire `PROMPT-MAITRE-SHARED.md` avant de continuer. Ce fichier contient le contexte commun, les conventions écosystème, les variables d'installation et le registre des relations.

Résumé des variables utiles (SHARED §1.1) :
- `{{SKILLS_ROOT}}` = `skills/`
- `{{KB_PATH}}` = `skills/KNOWLEDGE.md`
- `{{KB_ENABLED}}` = `true`
- `{{PROFILE_DEFAULT}}` = `NORMAL`

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

gen-plan est un skill de **planification de tâches** pour assistant IA. Il fournit un cadre structuré en 4 modes de fonctionnement et 15 étapes (E1-E15) pour analyser, planifier, exécuter, surveiller et adapter toute tâche complexe. La philosophie #7 (v3.6.1) impose la lecture bloc par bloc pour les fichiers > 500 lignes.

### §1.2 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Planification** | Analyse de la demande, classification, estimation, création du plan d'exécution |
| M2 | **Exécution** | Passage à l'action selon le plan établi, suivi des étapes |
| M3 | **Surveillance** | Monitoring en temps réel de l'avancement, détection d'écarts |
| M4 | **Adaptation** | Ajustement du plan en cas de dérive, recalibration |

### §1.3 Les 15 étapes (E1-E15)

| Étape | Nom | Description | Mode par défaut |
|-------|------|-------------|----------------|
| E1 | Analyse de la demande | Décortication de la demande utilisateur, identification des livrables, contraintes et critères de succès | M1 |
| E2 | Inventaire des ressources | Bilan des skills disponibles, outils, fichiers, contexte | M1 |
| E3 | Classification du type de tâche | Routage Type 1-4 (voir §8.3 pour le détail complet) | M1 |
| E4 | Estimation #token | Calcul budgétaire en tokens de la tâche | M1 |
| E5 | Sélection des skills | Identification des skills pertinents via skills-inventory et KNOWLEDGE.md | M1 |
| E6 | Profilage ressource | Choix du profil NORMAL / ECO / VIEUX PC | M1 |
| E7 | Création du plan | Assemblage du plan structuré avec étapes, dépendances, checkpoints | M1 |
| E8 | Validation du plan | Vérification cohérence, complétude, faisabilité | M1 |
| E9 | Lancement de l'exécution | Démarrage des étapes selon le plan | M2 |
| E10 | Suivi d'étape | Monitoring de chaque étape, log worklog | M2/M3 |
| E11 | Checkpoint intermédiaire | Vérification à mi-parcours, ajustements mineurs | M3 |
| E12 | Détection d'écart | Comparaison réel vs estimé, alertes | M3 |
| E13 | Ajustement | Modification du plan si nécessaire (règles d'or n°2-n°3 : §1.8) | M4 |
| E14 | Finalisation | Achèvement des étapes restantes | M2 |
| E15 | Bilan et auto-calibration | Retour d'expérience, mise à jour des grilles, enrichment KNOWLEDGE.md | M1/M4 |

### §1.4 Tagging #token (Norme N1)

Chaque étape et chaque skill utilisé reçoit un tag `#token` indiquant le coût estimé en tokens. La grille est auto-calibrée après exécutions (voir §8.2).

### §1.5 Snippets (Norme N2)

gen-plan peut générer des snippets de code réutilisables pendant l'exécution. Chaque snippet est tagué et versionné.

### §1.6 Python uniquement (Norme N3)

**Règle #7** : Tous les scripts générés par gen-plan doivent être en Python. Aucun script shell (bash, sh, powershell). Cette règle garantit la portabilité cross-platform.

### §1.7 Philosophie

1. **Read before planning** — Toujours lire le projet avant de planifier. Un plan sans connaissance du projet est générique et probablement inadéquat. La lecture exhaustive est un investissement nécessaire.
2. **Performance-driven sélection** — Le choix entre skill, agent spécialisé ou agent général est dicté par le gain de performance, pas par une hiérarchie rigide. Un skill avec un protocole pertinent bat toujours un agent nu.
3. **Skills can launch specialized agents** — Les skills ne sont pas des terminaisons mais des orchestrateurs. Un skill chargé peut lancer en interne un agent spécialisé (full-stack-developer, ppt-expert, etc.). Modèle à deux couches : Skill (protocole + connaissances domaine) → Agent Spécialisé (exécution).
4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** (inversion v3.24.0 ; extension aux commandes v3.32.0 — directive propriétaire 2026-11-02) — Les tâches ET les commandes (invocations d'outils lancées en un seul message multi-outils, vagues de flotte) PROUVÉES indépendantes (aucune écriture partagée, aucune dépendance d'ordre) s'exécutent en PARALLÈLE PAR DÉFAUT : le Graph Diamond s'ouvre automatiquement dès que la preuve d'indépendance existe (E9-E14). L'exécution série est l'exception justifiée et tracée : dépendance d'ordre, écriture partagée, verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC.
5. **Visible progress** — L'utilisateur sait toujours quelle phase est en cours, ce qui est terminé, et ce qui vient ensuite.
6. **CoT + Chaining avec auto-correction** — Chaque étape est exécutée avec un raisonnement structuré (Chain-of-Thought) avant l'action. Le chainage suit un pipeline hiérarchique où chaque sortie est vérifiée et corrigée avant de passer à la suivante.
7. **Lecture bloc par bloc** — Les fichiers volumineux (> 500 lignes) sont lus par blocs successifs avec une synthèse intermédiaire à chaque bloc, évitant la surcharge de contexte et garantissant une couverture totale.
8. **Downgrade irréversible** — Le profil ressource ne remonte jamais automatiquement. Si la détection des signaux de pression (disque < 5 Go, timeout 2+, tokens > 80 %) force un passage de NORMAL à ECO ou VIEUX PC, ce downgrade est définitif pour la session.

### §1.8 Règles d'or (résumé opérationnel — intégral : §9.8 `references/regles-or.md` ; miroir SHARED §9)

| N° | Règle | Portée |
|----|-------|--------|
| 1 | **Adaptation autonome** | Blocage = adaptation journalisée, jamais d'arrêt implicite ; pause explicite si inatteignable. |
| 2 | **Régénération post-installation** | Écosystème installé → plan re-généré via le gen-plan installé (R2). |
| 3 | **Mise à jour à chaque demande** | E13 (extension, jamais réécriture) ; « intègre dans le plan d'actions » = extension en place ; « met à jour » = NOUVEAU plan consolidé $FACON2. |
| — | **Modes** | `step` : chaîne par groupes ; `step-ok` : + confirmation ; NULL : comportement antérieur ; autre mode → clarification (R2). |
| 4 | **Dépôt par clone** | Clone git local, jamais de lecture distante ; jeton éphémère jamais persisté ; publication = validation propriétaire. |
| 5 | **État vérifiable** | Chiffres et statuts du disque, jamais pré-écrits (KO-L003) ; dépôt = source R4. |
| 6 | **Langue française** | Tout texte de l'agent en français dès le premier mot ; dérive → correction + worklog + durcissement. |
| 7 | **Mémoire complète** | Oubli de coupure → relire clones/sauvegardes avant (re-)génération. |
| 8 | **Formes installées** | PM INSTALL installe `skills/<skill>/` uniquement ; prompts maîtres jamais installés. |
| 9 | **Vérification d'installation** | Garde mécanique à toute invocation ; rétablissement auto puis re-génération du plan. |
| KO | **KO-L005** | gen-plan modifiée et validée → re-génération du plan (arbitres → montée → L004 → E8). |
| KO | **KO-L009** | Secret exposé : jamais utiliser ; révocation immédiate ; push = propriétaire, jamais l'agent. |
### §1.9 Disciplines d'ingénierie de prompts (résumé — tables intégrales : §9.9 `references/disciplines-mobilisation.md`)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED d'abord ; lecture par blocs + synthèses |
| **Loop engineering** | Boucle E10-E13 ; auto-calibration E15 |
| **Graph engineering** | KB = graphe bidirectionnel versionné ; matrice agent × skill |
| **Harness engineering** | Profils + signaux ; hook E8 + contrôle par phase ; worklog |
| **Refactoring engineering** | Discipline n°55 : opérations préservant le comportement observable ; garde-fous refactor-guard |
| **Refactoring test** | Outil n°55 (anti-auto-certification) : évaluation + blast radius, verdict OK/PRESSION/CRITIQUE |

- **Mobilisation** : tables E1-E8, n°54-55, E15, par déclencheur × modes — intégrales : `references/disciplines-mobilisation.md` ; socle commun (context/loop/graph/harness + PEK) à tout déclencheur du §A. **Hook continu E9-E14** : G-RES à chaque checkpoint E11 et entre vagues ; PRESSION → ECO, CRITIQUE → série/PAUSE. gen-plan = détenteur principal de la méthode prompt-engineering (SHARED §7 ; PEK v4.1).
### §1.10 Pipeline d'optimisation écosystème (Z0-Z6)

Transféré de la directive utilisateur « Pipeline optimisation écosystème » (2026-09-06) ; formalisé en v3.8.0. Ce pipeline définit les opérations de maintenance et d'optimisation du corpus : gen-plan le mobilise pour toute tâche d'optimisation de l'écosystème (l'opérationnalisation disciplinaire est assurée par les 4 skills de discipline à déclenchement automatique, cf. §1.9). Les vérifications Z4 mobilisent les arbitres existants (verify-cross, verify-correct-work, spell-check, sync-download) et les hooks correct-work.

| Phase | Nom | Objectif | Règles clés |
|-------|-----|----------|-------------|
| **Z0** | Inventaire | Scanner le dossier cible et identifier les fichiers | Règle zéro (SHARED §0) |
| **Z1** | Normalisation | Garantir des frontmatters YAML complets et conformes | SHARED §1.3 |
| **Z2** | Optimisation par fichier | Règles d'or, disciplines d'ingénierie (§1.9), dépendances, cohérence interne, auto-adaptation | §1.7-§1.9 |
| **Z3** | Optimisation des scripts Python | Syntaxe, convention N3, arbitres du dépôt | N3 ; arbitres §2.4 |
| **Z4** | Vérifications croisées | Cohérence versions, sections, frontmatters, règles d'or, dépendances | SHARED §3.2 ; E8 et E9-E14 |
| **Z5** | Journalisation | Tracer chaque optimisation (cause, solution, coût #token) | SHARED §1.4 (worklog) |
| **Z6** | Idempotence | Garantir la ré-exécutabilité sans effet de bord | Règles R1-R6 (§1.11) |

### §1.11 Règles d'idempotence (R1-R6)

| Règle | Énoncé |
|-------|--------|
| **R1** | Vérifier la présence avant insertion |
| **R2** | Ne jamais rétrograder (version ni contenu) |
| **R3** | Fusionner les frontmatters au lieu de les dupliquer |
| **R4** | Ne jamais dupliquer (sections, entrées KB, relations) |
| **R5** | Journaliser toute modification (worklog) |
| **R6** | Auto-adaptation sans duplication |

Ces règles s'appliquent à toute ré-exécution du présent pipeline d'installation (§5) et à toute passe Z0-Z6 sur un corpus déjà traité.

### §1.12 Hooks patterns avancés (v3.13.0, phase N20 — résumés compacts, intégraux : §9.10 `references/protocoles-detailles.md`)

<!-- PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0 -->

| Hook | Étape | Mécanisme | Référence |
|------|-------|-----------|-----------|
| **Answer key obligatoire** | **E1** | Chaque décision E1 devient une entrée `D0NN` de l'answer key (criterion, verification exécutable, source, priority S1-S4, status pending) | `references/answer-key-template.md` |
| **Arbitre answer-key-checker** | **E7/E8** | Le plan référence l'answer key ; à E8, l'arbitre mécanique `scripts/answer-key-checker.py` (16 checks) valide structure, fonctionnalité, idempotence et intégration — verdict PASS requis pour S1/S2 | `scripts/answer-key-checker.py` |
| **E7-DISP — Affichage obligatoire du plan** | **E7/E8/E13 + ouverture d'étape (v3.36.0) + fenêtre native début/fin d'étape (v3.39.0)** | Toute écriture du fichier plan (création E7, E13, re-génération KO-L005, reprise) n'est TERMINÉE qu'après la chaîne : plan écrit + answer key + verdict E8 (horodatages couplés) + worklog R5 marqueur `PLAN-AFFICHE` + bloc récapitulatif au chat — verdict mécanique bloquant ; affichage REJOUABLE (v3.27.0) ; à l'ouverture de chaque étape (v3.36.0) : bloc d'évolution du déroulement (groupes + statuts + compteurs + position — tous modes) | `scripts/check_plan_protocol.py` |
| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes prouvées indépendantes (le série est l'exception justifiée — philosophie #4 v3.24.0, extension aux commandes v3.32.0) — tracée au worklog | `references/graph-diamond-pattern.md` |
| **Observer** | **E15** | Invoque knowledge-observer en modes M1-M2 (observation + analyse post-session) ; les modes M3-M4 exigent un verdict correct-work | `references/observation-patterns.md` |
| **E5-POIDS — arbitre de poids de chargement** | **E5** (v3.38.0) | À la sélection des skills (E5), l'arbitre `scripts/poids-chargement.py` (recommandation R1 de l'étude de faisabilité Task 70 — le goulot réel de l'écosystème est le budget #token) mesure le poids de chargement (Kio + #token estimés = caractères/4) ; un skill CRITIQUE (≥ 60 Kio) ou LOURD (≥ 30 Kio) déclenche la voie lecture ciblée : §0 Contexte Système + sommaire d'abord, sections dédiées ensuite, `references/` chargées à la demande — JAMAIS de lecture intégrale par défaut pour un skill LOURD/CRITIQUE | `scripts/poids-chargement.py` |
| **R2-CACHE — cache de verdicts** | **E9-E14** (v3.38.0) | Les graders coûteux (arbitres, harnais, batteries) ré-exécutés à entrées inchangées passent par `scripts/cache-verdicts.py` (recommandation R2 de l'étude Task 70) : verdict figé une fois (rc + stdout + durée), re-jeu sans ré-appel (démo mesurée : gain 440×), invalidation automatique par état des fichiers cibles (taille/mtime), `--force` pour re-vérification réelle — un verdict figé n'est JAMAIS une preuve en soi, la re-exécution reste disponible à la demande | `scripts/cache-verdicts.py` |

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0 -->

<!-- RÉSUMÉ v3.39.0 — intégraux : references/protocoles-detailles.md -->

**Hook E1-RES — ouverture de session (4 vérifications AVANT analyse)** : (1) lecture seule préalable B-11 (worklog/plan/arbitres) ; (2) collecte G-RES (`monitor.py` : OK/PRESSION/CRITIQUE, journalisé) ; (3) fraîcheur du plan (modifiée et valide → re-généré avant reprise) ; (4) garde post-coupure (règle d'or n°9 : piliers + integrity → rétablissement auto). **Reprise (v3.27.0)** : message pendant un plan en vol → worklog + fraîcheur + E13 + E8 + R5 + affichage ; état « en vol » dérivé du DISQUE (RC3).

**Hook E7-DISP — affichage obligatoire (6 points, garde bloquante)** : (1) plan écrit `download/` ; (2) answer key >= 1 décision ; (3) E8 aux horodatages COUPLÉS (toute écriture = re-validation) ; (4) worklog R5 + marqueur `PLAN-AFFICHE` ; (5) bloc récapitulatif AU chat. Garde `check_plan_protocol.py` (P1-P5) ; affichage REJOUABLE ; ouverture d'étape (v3.36.0, tous modes) : PLAN-AFFICHE d'évolution au début de chaque groupe G<k> (statuts du disque ; step-ok : après confirmation). **(6) Fenêtre native (v3.39.0 — directive 1a1b7fe1c7238e8d)** : fenêtre des étapes du plan via le mécanisme NATIF de l'agent dédié à ce rôle (Z.ai : liste de tâches `TodoWrite`/`TodoRead`) — affichée au DÉBUT de l'exécution du plan d'actions, MISE À JOUR à chaque FIN d'étape ; intégral : `references/protocoles-detailles.md` (point 6).

### §1.12bis Leçons knowledge-observer v3.16.0 (re-curation B13, modes M3-M4)

<!-- PATTERN:PM-GEN-PLAN-KO-LECONS-v1.0.0 -->

Re-curation des leçons L001-L004 du journal `{{SKILLS_ROOT}}knowledge-observer/data/lessons-learned.json`
(cycle A-H, modes M3-M4, sessions B13 ; hook E15). Reconstitution post-wipe B13-r5 d'après les
marqueurs et le lignage documentés — les contenus exacts de v3.14.0/v3.15.0, non documentés,
restent perdus au wipe inter-sessions.

**KO-L001 — Économie API face à un quota 429 persistant** (leçon L001, appliquée) : en cas de
blocage 429 persistant, ne jamais marteler l'API — une seule sonde par message utilisateur
(R3-A11), travail local 100 % entre les sondes, armement automatique des suites à QUOTA_OK
(flag + pré-checks + runner 429-aware `--skip-done`), fenêtres candidates documentées. Toute
boucle d'attente en-tour est interdite : les démons d'arrière-plan de session sont fauchés entre
les appels d'outils (constat expérimental R3-A17-bis — le mécanisme honnête reste la sonde
immédiate à chaque tour, ré-armement best-effort seulement).

**KO-L003 — Arbitres à invariants dynamisés** (leçon L003, appliquée) : tout arbitre mécanique
dérive ses invariants de l'état courant (frontmatter installé = source de vérité, registre KB,
comptage réel), jamais d'un état figé. Un invariant figé produit des faux verdicts (faux négatif
`@mon-ecosysteme` classé PLATEFORME hors set CORE, faux positif `pgrep -f` par auto-match de la
ligne de commande, état « uniformément v3.11.0 » figé). Toute divergence arbitre ↔ réalité se
corrige en dynamisant l'arbitre, avec re-verdict honnête obligatoire après correction — jamais
en ajustant la réalité pour coller au verdict.

**Règle KO-L004 — Recalibrage croisé ET génération du prompt maître** (leçon L004, appliquée —
v1.1.0, directive 2026-10-09, matérialisation M4 : `scripts/generer-pm-skill.py`) : toute montée
de version d'un skill de l'écosystème déclenche, AVANT la certification : (1) le recalibrage
mécanique des outils dépendants : arbitres (`verify-cross.py`, `verify-correct-work.py`,
`test-coherence-interactions.py`, `check-ecosysteme-integrity.py`, `answer-key-checker.py`),
pre-checks (`n8-a-precheck-a2.py`), `skills-meta.json`, run-order, SYNC_MAP, miroir et archive ;
(2) **la génération mécanique du prompt maître de la nouvelle version** —
`PROMPT-MAITRE-<skill>-v<version>.md` dans `@mon-ecosysteme/` via
`scripts/generer-pm-skill.py --generate <skill>` (substitutions verrouillées — ABANDON sans
écriture si un motif n'apparaît pas exactement n fois ; garde anti-rétrogradation R2 ;
recalibrage SHARED §6.1 + PM-INSTALL §2ter/§A.3 inclus ; rapport de couverture SKILL.md↔PM —
le script ne masque jamais un écart, KO-L003). Un PM absent ou antérieur au SKILL.md installé
laisse l'installation dériver (KO-L003 installe un PM sans correspondance de version ; l'arbitre
interactions verdict FAIL sur PM postérieur). Un outil non recalibré valide l'état précédent —
verdict inopérant. L'application M4 de toute leçon knowledge-observer intègre donc d'office la
liste des outils à recalibrer ET l'étape de génération PM (garde post-édition).

Leçon L002 (snapshot de sécurité avant tout montage) : **proposée**, non appliquée (mode M3 sans
verdict correct-work) — aucun bloc PATTERN associé ; le pattern reste documenté au journal.

<!-- FIN-PATTERN:PM-GEN-PLAN-KO-LECONS-v1.0.0 -->

<!-- PATTERN:PM-GEN-PLAN-KO-L005-v1.0.0 -->

**Règle KO-L005 — Généralisation de la règle d'or n°2 : re-génération à chaque version de gen-plan modifiée et jugée valide** (leçon L005, validée — v3.17.0, N23-b/N28) : boucle complète arbitres → montée de version → recalibrage croisé (L004) → re-certification → re-génération du plan via la nouvelle version → re-validation E8. Détail complet : SKILL.md §1.5 (PATTERN:KO-L005-v1.0.0). Première application : plan B13-r5 via v3.16.0 ; matérialisation : ce bloc (B13-r6).

<!-- FIN-PATTERN:PM-GEN-PLAN-KO-L005-v1.0.0 -->

<!-- PATTERN:PM-GEN-PLAN-KO-L007-v1.0.0 -->

**Règle KO-L007 — Matérialisation d'abord : tout travail sur un clone sparse commence par l'établissement
des faits de matérialisation** (leçon L007, appliquée — v3.18.0, verdict correct-work étape F PASS,
cycle fusion installateurs 2026-10-02) : `git sparse-checkout list` + test d'existence des fichiers cibles
AVANT toute écriture (`git add` / `git rm`) et AVANT tout verdict d'arbitre naïf ; un audit dérive de
l'état matérielisé réel (L003) et consigne « non matérialisé » comme statut distinct de « échec ».
4 occurrences documentées avant application (Tasks 4/6/7 P-C, E15 v3.17.1 recomptage 34/72).

<!-- FIN-PATTERN:PM-GEN-PLAN-KO-L007-v1.0.0 -->


---

### §1.16 Routage de découverte des skills + garde d'installation (résumé — intégral : §9.10 `references/protocoles-detailles.md`)

- **É1-INSTALL — garde avec PRÉEMPTION** : à l'ouverture de session, AVANT E1 : `ensure-installed.py --check` (chemin canonique). rc=0 → no-op ; rc≠0 → suspension de toute tâche + `--reinstall` (pipeline PM-INSTALL, clone éphémère) AVANT toute autre étape ; directive post-réinstallation intégrée au plan ; idempotente. **v3.35.2** : contrôle du SKILL.md de toutes les entrées KB ; manquants → AUTO-RÉPARÉS depuis le miroir (INSTALLE-REPARÉ, rc=0, trace worklog).
- **Routage (E5)** : skills-inventory en PRIORITÉ (`generate_skills_md.py --json`/`--search`/`--category`, comparaison mémorisée au KB) ; skill-finder-cn en FALLBACK si échec — contrôle `audit-provenance` AVANT adoption ; bascule unidirectionnelle.
## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack technique

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si `{{KB_ENABLED}}`)

### §2.2 Structure

```
{{SKILLS_ROOT}}gen-plan/
├── SKILL.md                          # < 30 Kio — progressive disclosure (v3.39.0)
├── scripts/
│   ├── ensure-installed.py           # É1-INSTALL — préemption (v3.35.2)
│   └── check_plan_protocol.py        # Arbitre E7-DISP — P1-P5 (v3.27.0)
├── references/
│   ├── etapes-detaillees.md          # 15 étapes + mode step
│   ├── grille-token.md               # Grille #token + contingences (v3.39.0)
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   ├── guide-selection-agent-skill.md # Arbre de décision
│   ├── prompt-engineering-kit.md     # PEK v4.1
│   ├── patterns-avances-qwen.md      # 5 patterns (N19)
│   ├── answer-key-b12.md             # Registre réel (N19)
│   ├── answer-key-template.md        # Schéma Answer Key (N20)
│   ├── graph-diamond-pattern.md      # Parallélisation par défaut
│   ├── observation-patterns.md       # Task Observer (N20)
│   ├── regles-or.md                  # Règles d'or + KO — intégraux (v3.39.0)
│   ├── disciplines-mobilisation.md   # Tables de mobilisation (v3.39.0)
│   ├── protocoles-detailles.md       # E1-RES/E7-DISP/§1.16/§5.5/#4 (v3.39.0)
│   └── journal-versions.md           # Journal — archive (v3.39.0)
└── evals/
    ├── evals.json                    # 9 evals
    └── trigger_evals.json            # 15 cas
```

### §2.3 Auto-calibration E15

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action (estimation fiable) |
| 20-35% | Ajustement de la grille (paramétrage fin) |
| >35% | Recalibration complète (révision des coefficients) |

La calibration porte sur : la grille #token par agent/skill, les seuils de profil ressource, les ratios de complexité par type de tâche.

### §2.4 Profils ressource

Détail complet dans §8.2. Résumé :

| Profil | Contexte | Règles clés |
|--------|----------|-------------|
| **NORMAL** | Par défaut | 15 étapes complètes, tous les skills, surveillance complète |
| **ECO** | Discussion < 5 sessions, #token < 3500 | Étapes réduites, 1 checkpoint, pas de matrice dynamique KB |
| **VIEUX PC** | Matériel limité | Règles ECO + scripts < 100 lignes, pas de graphiques |

**Règle de downgrade irréversible** : le profil ne remonte jamais automatiquement. Si une discussion passe de NORMAL à ECO (ou ECO à VIEUX PC), le profil restera au niveau inférieur pour toute la durée de la session. Le profil initial est NORMAL sauf détection de signaux de pression.

#### §2.4.1 Signaux de pression

| Signal | Seuil pression | Seuil critique |
|--------|---------------|----------------|
| Espace disque | < 5 Go | < 3 Go |
| Timeout appels | 2+ consécutifs sur 5 min | 4+ sur 5 min |
| Budget tokens | > 80 % consommé | > 95 % consommé |

**1 signal pression** → passage en ECO. **2+ signaux pression** ou **1 signal critique** → passage en VIEUX PC.

#### §2.4.2 Filtrage #token par profil

| Profil | Seuil d'exclusion | Action |
|--------|------------------|--------|
| NORMAL | Aucun | Aucun filtrage |
| ECO | > 8000 #token | Sous-tâche exclue du plan |
| VIEUX PC | > 5000 #token | Sous-tâche exclue du plan |

Le filtrage s'applique à l'étape E4 (estimation), avant la construction du plan (E7).

### §2.5 Intégration KB

Si `{{KB_ENABLED}}` est `true` :

- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **`--kb-skill`** : flag pour activer la consultation KB
- **Protocole de Découverte** : scan du registre pour identifier les skills pertinents (voir SHARED §2.3)

---

## §3 — RELATIONS

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet des relations inter-skills.

Relations directes de gen-plan (extrait de SHARED §3.1) :

| Avec | Nature | Détails |
|------|--------|--------|
| correct-work | Invocation à E1 + hook E8 + contrôle par phase | Validation du plan initial + vérification post-plan et à chaque phase terminée (E9-E14), version >= v2.4.0 |
| clone-chat | Calibration + archivage | E4, E15, optionnel, version >= v2.0.0 |
| skills-inventory | Routage prioritaire de découverte (§1.16) + consultation à E5 | Sélection des skills, version >= v1.1.0 |
| skill-finder-cn | Fallback de découverte (§1.16) | Recherche externe UNIQUEMENT si skills-inventory échoue — contrôle cybersécurité audit-provenance obligatoire avant adoption |
| prompt-engineering | Délégation (§1.9) | Optimisation des prompts complexes, version >= v1.0.0 |
| context-engineering | Mobilisation (§1.6) | Socle SHARED, Protocole de Découverte KB, lecture bloc par bloc — déclenchement automatique (SHARED §7) |
| loop-engineering | Mobilisation (§1.6) | Boucle E10-E13 + auto-calibration E15 — déclenchement automatique (SHARED §7) |
| graph-engineering | Mobilisation (§1.6) | Registre KB graphe bidirectionnel versionné, matrice agent × skill — déclenchement automatique (SHARED §7) |
| harness-engineering | Mobilisation (§1.6) | Profils ressource, hooks E8 + E9-E14, arbitres, worklog — déclenchement automatique (SHARED §7) |
| spec-driven-development | Détention orchestrée (SHARED §7, registre décentralisé §8 du skill) | Cadrage spec-first à E4, re-validation à E7 — version >= v1.0.0 |
| memory-engineering | Détention orchestrée (SHARED §7, registre décentralisé §8 du skill) | État Long obligatoire aux exécutions longues, compaction/reprise — version >= v1.1.0 |
| fleet-engineering | Détention orchestrée (SHARED §7, registre décentralisé §8 du skill) | Choix du pattern et des bornes à E5/E7, Graph Diamond — version >= v1.0.0 |
| refactoring-engineering | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Conception/exécution des opérations de refactoring (E4/E7 + situations E9-E14) — version >= v1.0.1 |
| refactor-guard | Garde-fous de refactoring (fusion discussion 468a4c26 — lignée externe v1.7.0) | Mobilisé par refactoring-engineering pendant les opérations à risque (score H01-H15, sandbox, rollout) ; détection de besoins (hook E13) — version >= v1.7.0 |
| refactoring-test | Outil n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.1 |
| knowledge.md | Enrichissement à E15 | Mise à jour registre et calibration |
| knowledge-observer | Invocation à E15 (§1.12) | Observation post-session (modes M1-M2), version >= v1.0.0 |
| answer-key | Arbitrage E7/E8 (§1.12) | Décisions E1 vérifiables mécaniquement — arbitre answer-key-checker.py (16 checks) |
| resource-monitor | Collecte E1-RES (§1.12bis) | Surveillance permanente §1.14 — verdict OK/PRESSION/CRITIQUE, mode d'exécution journalisé |

---

## §4 — YAML FRONTMATTER

```yaml
---
name: gen-plan
version: 3.39.0
category: ecosystem
language: fr
tags:
  - planning
  - task-management
  - token-estimation
  - auto-calibration
  - ecosystem
description: >
  Skill de planification de tâches pour assistant IA.
  4 modes (Planification, Exécution, Surveillance, Adaptation),
  15 étapes (E1-E15), classification Type 1-4 (documents, analyse, développement web, data), 3 profils ressource (NORMAL/ECO/VIEUX PC),
  tagging #token, snippets, scripts Python uniquement,
  règles d'or d'adaptation autonome, disciplines d'ingénierie de prompts,
  hooks patterns avancés (answer key E1, arbitre answer-key-checker E7/E8,
  Graph Diamond E9-E14, knowledge-observer E15),
  déclencheurs verbatim « intègre dans le plan d'actions » (E13 — extension du plan courant, règle d'or n°3)
  et « met à jour » (re-génération $FACON d'un nouveau plan d'actions $FACON2 — v3.37.0),
  glossaire alias-eco inline $FACON/$FACON2 (§A — auto-contenu, v3.37.0)
  progressive disclosure R1 (v3.39.0) : résumés inline, intégraux en references/ à la demande
dependencies:
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "E1, E8 hook, contrôle par phase"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
  - skill: knowledge-observer
    version: ">=1.0.0"
    used_at: "E15 (analyse post-session, modes M1-M2)"
  - skill: resource-monitor
    version: ">=1.0.0"
    used_at: "Hook E1-RES (collecte G-RES, ouverture de session)"
---
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

### §5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}gen-plan/references
mkdir -p {{SKILLS_ROOT}}gen-plan/evals
```

### §5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~337 lignes — progressive disclosure v3.39.0 : résumés inline, intégraux en §9) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** (voir SHARED §0)
3. **§1 — Spécification fonctionnelle** : 4 modes, 15 étapes, normes N1-N3, règles d'or (§1.8), disciplines d'ingénierie (§1.9), pipeline d'optimisation Z0-Z6 (§1.10), idempotence (§1.11)
4. **§2 — Spécification technique** : Stack, structure, auto-calibration, profils, KB
5. **§3 — Relations** : Voir SHARED §3 (résumé des relations directes)
6. **§4 — Grille #token** : Résumé de §8.2
7. **§5 — Conventions** : Nommage (SHARED §1.2), Python uniquement (N3), tagging

### §5.3 Créer les fichiers de référence

Le contenu in extenso de chaque fichier est en §9.

### §5.4 Créer evals/evals.json (schéma skill-creator)

Schéma EXACT skill-creator (`skill_name` ; evals : `id` entier, `prompt`, `expected_output`, `files`, `expectations`) — unifié en v3.8.0 (révision recommandée par le clone 2026-09-06, §5) :

```json
{
  "skill_name": "gen-plan",
  "version": "3.10.0",
  "schema": "skill-creator v1.0.0 (references/schemas.md)",
  "note": "Schéma unifié skill-creator (révision PM v3.8.0, session A9 — recommandation clone 2026-09-06 §5) : sémantique des 6 evals v3.7.0 préservée (5 d'origine + hook correct-work E9-E14) ; eval 7 GP-mode-step ajouté en v3.22.0 (modes step — enchaînement autonome des groupes, correct-work(groupe) par groupe, correct-work(projet) final) ; eval 8 GP-mode-step-ok ajouté en v3.22.1 (renommage step-confirm → step-ok — confirmation propriétaire avant chaque groupe).",
  "evals": [
    {
      "id": 1,
      "name": "E1-classification — Classification correcte Type 1-4",
      "prompt": "Crée un rapport d'analyse",
      "expected_output": "Le plan identifie la tâche comme Type 1 (document) et sélectionne le skill cible docx",
      "files": [],
      "expectations": [
        "La tâche est classée Type 1 (document)",
        "Le skill cible identifié est docx"
      ]
    },
    {
      "id": 2,
      "name": "E2-token-estimation — Estimation #token cohérente",
      "prompt": "Planifie cette tâche : travail moyen estimé entre 5 et 15 sessions",
      "expected_output": "Une estimation #token entre 3500 et 5500 avec le profil ressource NORMAL",
      "files": [],
      "expectations": [
        "L'estimation #token tombe dans l'intervalle [3500, 5500]",
        "Le profil ressource retenu est NORMAL"
      ]
    },
    {
      "id": 3,
      "name": "E3-plan-complet — Plan E1-E15 complet",
      "prompt": "Planifie la création d'un dashboard Next.js",
      "expected_output": "Un plan contenant les 15 étapes E1-E15, classé Type 3 (développement web)",
      "files": [],
      "expectations": [
        "Le plan contient les 15 étapes E1-E15",
        "La tâche est classée Type 3 (développement web)"
      ]
    },
    {
      "id": 4,
      "name": "E4-auto-calibration — Auto-calibration E15",
      "prompt": "À la clôture E15, l'écart entre l'estimation initiale et le réel est de 28%",
      "expected_output": "Un ajustement du paramétrage fin (calibration E15) réduit l'écart des estimations suivantes",
      "files": [],
      "expectations": [
        "E15 déclenche un ajustement du paramétrage fin",
        "La calibration est journalisée (grille #token mise à jour)"
      ]
    },
    {
      "id": 5,
      "name": "E5-python-only — Scripts Python uniquement",
      "prompt": "Génère un script de traitement de données pour cette étape du plan",
      "expected_output": "Un script Python ; aucun script bash/sh/powershell",
      "files": [],
      "expectations": [
        "Le script généré est en Python",
        "Aucun script bash, sh ni powershell n'est produit"
      ]
    },
    {
      "id": 6,
      "name": "E6-hook-correctwork — Hooks correct-work par phase (spécifique v3.7.0)",
      "prompt": "Planifie une tâche en plusieurs phases et vérifie chaque phase après exécution",
      "expected_output": "Le hook correct-work >= v2.4.0 est invoqué par phase (E9-E14) et son verdict est consigné",
      "files": [],
      "expectations": [
        "Le hook correct-work est invoqué pour chaque phase E9-E14",
        "Le plan référence correct-work >= v2.4.0 dans ses relations"
      ]
    },
    {
      "id": 7,
      "name": "GP-mode-step — Enchaînement autonome des groupes (modes step, spécifique v3.22.0)",
      "prompt": "gen-plan(step) : exécute le plan d'actions en cours en groupes séquentiels avec une vérification après chaque groupe",
      "expected_output": "Les groupes du plan s'enchaînent en autonome ; correct-work(groupe) est invoqué après chaque groupe (max 2 rounds de correction) et correct-work(projet) en fin de chaîne",
      "files": [],
      "expectations": [
        "Le mode step est reconnu et les groupes s'exécutent en séquentiel",
        "correct-work(groupe) est invoqué après chaque groupe (max 2 rounds de correction)",
        "correct-work(projet) est invoqué en fin de chaîne"
      ]
    },
    {
      "id": 8,
      "name": "GP-mode-step-ok — Confirmation propriétaire par groupe (renommage step-confirm → step-ok, spécifique v3.22.1)",
      "prompt": "gen-plan(step-ok) : exécute le plan d'actions en groupes séquentiels en me demandant confirmation avant chaque groupe",
      "expected_output": "Le mode step-ok est reconnu (alias step-confirm/step-confim normalisés) ; une confirmation du propriétaire est demandée avant chaque groupe et correct-work(projet) clôt la chaîne",
      "files": [],
      "expectations": [
        "Le mode step-ok (alias step-confirm) est reconnu et route vers le mode step avec confirmation",
        "Une confirmation propriétaire explicite est demandée avant chaque groupe",
        "Aucun groupe n'est exécuté sans confirmation propriétaire préalable"
      ]
    }
  ]
}
```

### §5.5 Créer evals/trigger_evals.json (Description Optimization)

Format `[{"query": "...", "should_trigger": true|false}]` : valider que la description du frontmatter déclenche gen-plan sur les demandes de planification (true) et PAS sur les demandes hors périmètre (false) :

```json
[
  {"query": "planifie cette tâche pour moi", "should_trigger": true},
  {"query": "crée-moi un plan d'exécution détaillé", "should_trigger": true},
  {"query": "organise ce travail en étapes avec une estimation d'effort", "should_trigger": true},
  {"query": "quelle est ton estimation de #tokens pour cette tâche ?", "should_trigger": true},
  {"query": "quel profil ressource (LIGHT/NORMAL/HEAVY) pour cette demande ?", "should_trigger": true},
  {"query": "classe cette tâche : document, analyse ou développement web ?", "should_trigger": true},
  {"query": "vérifie le travail que tu viens de faire", "should_trigger": false},
  {"query": "traduis ce document en anglais", "should_trigger": false},
  {"query": "bonjour", "should_trigger": false}
]
```

### §5.6 Exécution des évaluations en workspaces skill-creator

Les evals §5.4 sont exécutés dans `{{SKILLS_ROOT}}gen-plan-workspace/iteration-N/eval-M/` : chaque eval M reçoit deux exécutions — `with_skill/` (skill chargé) et `baseline/` (sans skill ou version antérieure) — puis une notation `grading.json` (champs `text`, `passed`, `evidence`). Une itération = un cycle complet ; la comparaison with_skill vs baseline fonde les corrections de l'itération suivante. Les exécutions sont journalisées dans le worklog (SHARED §1.4).

---

## §6 — VÉRIFICATION POST-INSTALLATION

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | SKILL.md existe | `{{SKILLS_ROOT}}gen-plan/SKILL.md` | File exists |
| 2 | Taille SKILL.md | ~232 lignes (version compacte) | Within range |
| 3 | YAML frontmatter valide | name, version, category, language, tags | All present |
| 4 | 5 fichiers référence | `references/` contient 5 fichiers | 5 files |
| 5 | evals.json valide | JSON parsable (schéma skill-creator), 8 evals | Valid JSON |
| 6 | Norme N3 (Python) | Aucune mention shell/bash | No shell refs |
| 7 | Intégration KB | Mention kb_path, --kb-skill | Present |
| 8 | KNOWLEDGE.md | Entrée gen-plan présente (SHARED §2.2) | Present |
| 9 | Cross-refs | correct-work et clone-chat mis à jour (SHARED §3.2) | Present |
| 10 | trigger_evals.json | JSON parsable, cas true et false présents | Valid JSON |
| 11 | Workspaces skill-creator | §5.6 documenté (with_skill vs baseline) | Present |

---

## §7 — HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v3.39.0 | 2026-11-07 | MINOR re-curation progressive disclosure R1 (directive propriétaire « Chantier R1 : re-curation progressive disclosure de gen-plan », Task 72 G1 — étude Task 70 R1) + directives complémentaires 1a1b7b297b7b4975 (skill re-curation implémenté d'un script — plan Task 72 : tests AVANT re-curation, protocole-test.py PRE/POST/--compare) et 1a1b7fe1c7238e8d (fenêtre native AFFICHE-PLAN) : 9 blocs déplacés R4 byte-identité vers references/ (journal-versions · regles-or [+ leçons KO] · disciplines-mobilisation · protocoles-detailles) + append contingences grille-token.md — résumés NOUVEAUX inline (SKILL.md 104,0 → 29,95 Kio, −71,2 % #token, CRITIQUE → INTERMÉDIAIRE) ; contrats baseline golden master D001-D005 PASS (task72-baseline-verifier.py, re-vérifiés post-amendement) ; E7-DISP point 6 « fenêtre native » : la fenêtre des étapes du plan s'affiche via le mécanisme natif de l'agent dédié à ce rôle (Z.ai : liste de tâches TodoWrite/TodoRead) au début de l'exécution du plan d'actions + mise à jour à chaque fin d'étape (canal supplémentaire — bloc chat, marqueur worklog PLAN-AFFICHE et garde check_plan_protocol.py P1-P5 inchangés) ; PM : §1.8/§1.9/§1.12/§1.16 → résumés compacts miroirs du SKILL.md, intégraux reportés in extenso en §9.7-§9.10 (aucune duplication intra-PM), §9.2 grille-token à jour (append contingences), description + progressive disclosure, lags §5.2/§5.3/§9 résorbés. |
| v3.38.0 | 2026-11-07 | MINOR recommandations R1+R2 de l'étude de faisabilité Task 70 (directive propriétaire 2026-11-08, Task 71 G3 : « je veux appliquer tes recommandations "R1" et "R2". analyse comment les intégrer $FACON à mon écosystème […] fais des tests $FACON2 avant de les intégrer ») : (1) NOUVEAU hook E5-POIDS — arbitre de poids de chargement scripts/poids-chargement.py (R1 : progressive disclosure ; mesure Kio + #token estimés par skill, seuils OK < 12 Kio / LOURD >= 30 Kio / CRITIQUE >= 60 Kio ; skill LOURD/CRITIQUE → lecture ciblée §0 + sommaire + sections dédiées, references/ à la demande — JAMAIS de lecture intégrale par défaut ; selftest 10/10, idempotence ×2 ; rapport de priorisation : gen-plan CRITIQUE 102,8 Kio ≈ 26 312 tokens = cible n°1 de la curation R1) ; (2) NOUVEAU hook R2-CACHE — cache de verdicts généralisé scripts/cache-verdicts.py (R2 : pattern « verdict figé une fois, re-jeu sans ré-appel » ; clé SHA-256 commande + état des cibles [taille/mtime], invalidation automatique, --force pour re-exécution réelle ; selftest 12/12, idempotence ×2 ; démo mesurée sur check-ecosysteme-integrity.py : froid 45,5 ms → chaud 0,1 ms = gain 440×, verdict figé identique 110/110, invalidation sur touch OK) ; cascade KO-L004 : PM v3.38.0, SHARED v1.7.33 / PM-INSTALL v1.9.9 recalibrés, PM v3.37.2 archivé R4, pin ECO_SKILLS 3.38.0, KB, ULTRA régénéré, replay arbitres ×2. |
| v3.37.2 | 2026-11-07 | PATCH durcissement règle d'or n°6 (directive propriétaire 2026-11-08, session web-ecef7f80 — 2ᵉ constat de dérive : textes de raisonnement affichés en anglais/chinois alors que la réponse finale était conforme) : portée MÉCANIQUE étendue à TOUT texte produit par l'agent (raisonnements et analyses affichés, titres et intertitres, libellés de statuts et compteurs, légendes de tableaux, blocs récapitulatifs PLAN-AFFICHE, résumés de continuation, reformulations de sorties d'outils — seuls les artefacts techniques verbatim restent dans leur langue d'origine) ; correction immédiate sans transition ; constat propriétaire → correction + worklog + durcissement de la règle ; cascade KO-L004 : PM v3.37.2, SHARED v1.7.32 / PM-INSTALL v1.9.8 recalibrés mécaniquement, pin ECO_SKILLS 3.37.2, KB, ULTRA régénéré, replay arbitres ×2. |
| v3.37.1 | 2026-11-07 | PATCH trigger_evals (ticket F-V1-1 des vagues de tests V1 — Task 61 G3) : 13 → 15 cas (+1 positif « Met à jour le plan d'actions avec les nouvelles demandes du jour. » → déclencheur verbatim de consolidation v3.37.0 ; +1 négatif « Met à jour les dépendances npm de ce projet web. » → hors périmètre plan d'actions) — non-régression triggers du second déclencheur verbatim (précédent v3.17.2) ; aucun changement de contrat ni de description ; cascade KO-L004 : PM v3.37.1, pin ECO_SKILLS 3.37.1, KB, historiques-par-skill (48 versions / 40 PMs), ULTRA régénéré ×2, replay arbitres ×2. |
| v3.37.0 | 2026-11-07 | Déclencheur verbatim « met à jour » — re-génération $FACON d'un NOUVEAU plan d'actions $FACON2 (directive propriétaire préalable à gen-plan(step) : « vérifie si mon skill "gen-plan" a un déclencheur "met à jour" qui génère $FACON un nouveau plan d'actions $FACON2 (fais en sorte qu'à la lecture du skill que tu n'aies pas besoin de "alias-eco" pour comprendre $FACON et $FACON2) ») : §A (déclencheur + glossaire alias-eco INLINE auto-contenu : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » — la lecture du SKILL.md n'exige plus le skill alias-eco pour ces deux marqueurs, source canonique registre @historique/@Alias/aliases.json) + règle d'or n°3 (voie CONSOLIDATION distincte de « intègre dans le plan d'actions » = extension E13 en place : nouveau plan horodaté consolidant l'état vérifiable [groupes terminés reportés avec preuves citées — statuts dérivés du disque, règle d'or n°5/KO-L003] + restes-à-faire re-planifiés + nouvelles demandes + re-estimation #token + answer key re-numérotée ; ancien plan conservé R2 ; chaîne E7-DISP complète ; routage : sans mode explicite le verbatim prime sur NULL, avec mode explicite la consolidation s'exécute en tête et le mode enchaîne sur le nouveau plan) + read_when + description frontmatter ; constat d'honnêteté v3.36.0 (règle d'or n°5 : cascade interrompue ~07:53Z par coupure de contexte — pin/KB/historiques/worklog non recalibrés + preuve vivante G3→G5 anticipée, corrigée dans le SKILL.md §5.6 [corrigé v3.37.0] — dette intégralement résorbée par la cascade v3.37.0) ; preuve vivante : déclencheur « met à jour » utilisé en réel pour le plan consolidé Task 61 (13ᵉ directive point 3), puis chaîne mode step G3→G5 exécutée sous v3.37.0 avec PLAN-AFFICHE à chaque ouverture de groupe |
| v3.36.0 | 2026-11-07 | Extension E7-DISP v3.36.0 — affichage d'ouverture d'étape (directive propriétaire 13ᵉ, Task 61 : « intègre à PLAN-AFFICHE qu'il doit se lancer au début de l'exécution d'une nouvelle étape du plan d'actions pour que je puisse visualiser l'évolution du déroulement du plan d'actions ») : le marqueur PLAN-AFFICHE se lance AUSSI au début de l'exécution de chaque nouvelle étape (groupe G<k>) du plan d'actions, pour tout mode d'exécution (step, step-ok, exécution classique mode NULL, groupes du plan des correctifs correct-work §1.5bis) — vue d'évolution du déroulement (tous les groupes + statuts + compteurs + position du groupe ouvert + verdicts correct-work(groupe) antérieurs), statuts toujours dérivés de l'état vérifiable (règle d'or n°5 — KO-L003), affichage rejouable à la reprise, en step-ok après confirmation ; ligne E7-DISP ajoutée à la table §1.12 (écart hérité v3.27.0 résorbé — le hook vivait au SKILL.md §1.2bis sans ligne PM) ; §A déclencheur step enrichi. Transversalité de la couche d'organisation §5.5 (directive 13ᵉ point 2 : « vérifie que tous les modes de mon skill gen-plan ont bénéficiés des optimisations faites dans cette discussion au mode STEP de mon skill gen-plan ») : structure hiérarchique + cadence d'affichage produites à E7 pour tout plan, lues par toute exécution (mode NULL classique inclus) — la distinction des modes ne porte que sur les portes de confirmation ; audit : règles d'or n°6/n°8/n°9 transverses par construction, vagues chronologiques (12ᵉ directive) couche d'organisation transverse, correct-work §1.5bis compatibilité tous modes (correct-work v2.11.0), cadence correct-work par groupe v3.22.0 = protocole référent généralisé par la règle correct-work(livrables de la phase) AVANT la phase suivante. MINOR — additions pures, description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.36.0 (delta verrouillé scripts/delta-genplan-v3360.json), KB + pin ECO_SKILLS + @historique/historiques-par-skill/gen-plan.md + lignes vives disciplines + sceaux README §5 (lag v3.35.1/v3.35.2 résorbé) + README corpus + propagation §0 + rescellement archive ; replay arbitres ×2 ; preuve vivante : chaîne mode step Task 61 (G3→G5) exécutée sous v3.36.0 avec PLAN-AFFICHE affiché à chaque ouverture de groupe. |
| v3.35.2 | 2026-11-06 | Extension Task 56 de la garde É1-INSTALL (leçons L54-1 + L55-3, session web-c30e6506 — demande propriétaire : « analyse pourquoi "version-management" disparait tout le temps de mon écosystème dans l'objectif d'optimiser mon écosystème pour qu'à l'avenir cela ne se reproduise plus ni dans cette discussion, ni dans nos discussions à venir ») : diagnostic cause racine de la disparition récidivante de version-management (volatilité plateforme sandbox × angle mort de la garde ensure-installed.py [installe() sans contrôle des répertoires KB — réintroduction de l'angle mort documenté, la garde étendue Task 31 n'étant plus au chemin canonique] × détection tardive → récidive structurelle, 9 occurrences) ; correctif durable dans scripts/ensure-installed.py : etat() dérive dynamiquement les SKILL.md de TOUTES les entrées KB versionnées (regex identique arbitre integrity, KO-L003) ; installe() exige 0 skill KB manquant ; dérive limitée aux skills KB manquants → AUTO-RÉPARATION depuis le miroir local KNOWLEDGE-repo (verdict INSTALLE-REPARÉ, rc=0, trace worklog, aucune action distante/jeton) ; idempotence ×2 prouvée. Preuves : 4ᵉ récidive détectée+réparée (vm v1.2.0) ; absence simulée → INSTALLE-REPARÉ rc=0 ; integrity 108/108 + coherence 53/23/0 baseline préservée ; sync miroir byte-identique. PATCH — addition pure, description frontmatter inchangée (non-régression triggers). |
| v3.35.1 | 2026-11-06 | Renforcement de la règle d'or n°6 — Langue des échanges avec le propriétaire (français) (directive propriétaire 2026-11-06, session web-c30e6506 : « tu me réponds à nouveau en chinois, fais en sorte que la règle "parle-moi toujours en français" soit intégrer dans mon skill "gen-plan" et dans mon écosystème pour que tu ne réponds plus en chinois à l'avenir. ») : la règle s'applique dès le PREMIER mot de toute session, reprise ou continuation — la langue d'un résumé de continuation, de métadonnées de canal (IM/trace), d'une sortie d'outil ou d'un message utilisateur n'infirme JAMAIS la règle et ne dérive jamais la langue de réponse ; toute dérive constatée est corrigée immédiatement (la réponse suivante repart en français, sans transition) ; la règle est désormais AUSSI portée par le §0 Contexte Système du corpus SHARED (v1.7.24 — propagée à tous les skills via propagate-context), en plus du §1.5. PATCH — addition pure, description frontmatter inchangée (non-régression triggers). |
| v3.35.0 | 2026-11-05 | Règle d'or n°9 — Vérification automatique de l'installation de l'écosystème à toute invocation de gen-plan (post-coupure) (directive propriétaire 2026-11-04, session web-c30e6506 — gen-plan : « avant de continuer vérifie que mon écosystème est encore installé (…) et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill gen-plan est appelé après une coupure. ») : §1.8 — insertion n°9 (vérification mécanique des piliers — registre KB, corpus SHARED, forme installée gen-plan — puis arbitre check-ecosysteme-integrity à TOUTE invocation, la coupure étant DÉTECTÉE par la vérification et non présupposée ; écosystème absent/endommagé → chemin automatique : lecture intégrale PM SHARED → réinstallation PM-INSTALL voie directe eco_install_pipeline.py depuis le clone certifié [règle d'or n°4] → certification arbitres → re-génération du plan via le gen-plan réinstallé [règle d'or n°2 + KO-L005] ; journalisation worklog règle d'or n°1) ; §1.12 — hook E1-RES étendu (trois → quatre vérifications préalables, point (4) garde post-coupure) ; description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 ; preuve vivante : session web-c30e6506 des 2026-11-04/05 (profil post-coupure 14/52 → réinstallation → 98/98 + 141/141 + 16/16 → plan régénéré via v3.35.0) |
| v3.34.0 | 2026-11-04 | Règle d'or n°8 — PM INSTALL installe toujours les formes installées (skills/<skill>/SKILL.md), jamais les prompts maîtres (directive propriétaire 2026-11-04, session web-c30e6506 — gen-plan(step) « fais en sorte que ceux soient toujours mes skills (avec le "skill.md") qui soient installés par PM INSTALL et non pas leur prompt maitre dans "PM skills/" qui soient installés (fais en une règle d'or de mon écosystème.) ») : installation exclusive des formes installées certifiées depuis le clone certifié (règle d'or n°4) ; prompts maîtres — corpus @mon-ecosysteme/ ET miroirs @PM-SKILLS/ (ex-« PM skills/ », renommé Task 49, garde D010) — jamais installés comme formes installées ni déployés sur le profil local ; garantie mécanique : garde post-installation dans l'installateur (0 PROMPT-MAITRE-* hors corpus autorisés — PM-INSTALL §3.5 v1.9.0) ; MINOR — addition pure (précédent v3.33.0 règle n°7) |
| v3.33.1 | 2026-11-04 | Précision sémantique de la règle d'or n°7 (directive propriétaire 2026-11-04, session web-6058b3ba — « prend en compte que lorsque je précise que lorsque je disais "ce que tu as oublié" alors je voulais dire "les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer". ») : §1.8 — point 2 précisé (l'« oubli » visé = les éléments perdus à cause d'une coupure et que l'agent n'a que partiellement réussi à reconstituer) + point 5 ajouté (une reconstitution PARTIELLE n'est jamais une mémoire complète — complétée par la relecture des clones et sauvegardes ; l'état vérifiable du disque, règle d'or n°5, prévaut sur toute reconstruction mémorielle) ; PATCH — addition pure ; description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 |
| v3.33.0 | 2026-11-04 | Règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification (directive propriétaire 2026-11-04, session web-6058b3ba — « tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées » + « recommence en utilisant le mode STEP ») : §1.8 — insertion n°7 (couverture totale des éléments de la discussion par le plan ; oubli dû à une coupure → relecture des clones et sauvegardes AVANT génération/re-génération ; reprise E1-RES = relecture première + état disque règle d'or n°5 ; couverture vérifiable — élément ∈ {tâche du plan, livrable certifié, pendance consignée}, absence = dérive E13) ; description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 |
| v3.32.0 | 2026-11-02 | Parallélisation par défaut étendue aux COMMANDES (directive propriétaire 2026-11-02, session web-6058b3ba — préalable gen-plan : « exécute les tâches et les commandes en parallèle par défaut » + garde de vérification du fonctionnement fondamental du Graph Diamond) : philosophie #4 (§1.7) réécrite — les tâches ET les commandes (invocations d'outils en un seul message multi-outils, vagues de flotte) prouvées indépendantes s'exécutent en PARALLÈLE PAR DÉFAUT ; RESORPTION de la divergence stale héritée (« Serial exécution by DEFAULT — parallélisme INTERDIT », antérieure à l'inversion v3.24.0, qui contredisait le SKILL.md et bloquait l'ouverture automatique du Graph Diamond) ; ligne hook Graph Diamond §1.2bis réalignée sur le SKILL.md ; vérification préalable mécanique : Graph Diamond NON-AFFECTÉ (4 phases, 5 anti-patterns, marqueurs PATTERN uniques, hook E9-E14, eval id 9 — references/graph-diamond-pattern.md laissé byte-identique sha256) ; la preuve d'indépendance reste le prérequis non négociable (anti-pattern n°3), les exceptions série tracées inchangées (dépendance d'ordre, écriture partagée, verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC) ; normalisation §6 (triple ligne vide condensée — plage arbitre 1200-1500 L rétablie) |
| v3.31.0 | 2026-11-01 | Complétion de couverture « tous les cas de figure » de la mobilisation des disciplines (mode NULL, directive propriétaire « GO » — application des recommandations C1-C4 du rapport de vérification des disciplines download/rapport-verification-disciplines-genplan-v3.30.0-2026-11-01.md, session web-4f989063) : C1 — mobilisation E15 ajoutée aux trois tables du SKILL §1.6 (loop auto-calibration, graph enrichissement KB, memory État Long du bilan, refactoring-test re-scan post-session, resource-monitor verdict de clôture) ; C2 — resource-monitor mobilisé à E6 (verdict G-RES → profil) et hook continu E9-E14 encodé (checkpoint E11 + entre vagues du Graph Diamond — résorption du drift bidirectionnel vs la déclaration du provider resource-monitor §1.14/§3) ; §3 recalibrée ; C3 — fleet-engineering aligné E5/E7 (divergence interne table n°54 ↔ §3 résorbée) ; C4 — nouveau bloc PATTERN:GEN-PLAN-DISCIPLINES-MODES-v1.0.0 (SKILL §1.6) — mapping disciplines × déclencheurs (mode NULL, step/step-ok, orchestre, generate, correct-work(projet|cible), reprise E1-RES) avec socle commun appliqué à tout déclencheur. Additions pures R2, description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3, KB, pin ECO_SKILLS, historiques-par-skill/gen-plan.md ; rescellement archive v2.3 ; replay arbitres ×2. |
| v3.30.0 | 2026-10-31 | Installation du bloc PATTERN KO-L009 — sécurité : exposition d'un identifiant dans un canal de discussion (directive propriétaire explicite, session web-4f989063, gen-plan mode NULL 2026-10-31) : §1.8 — insertion KO-L009 (leçon L009 validée M4 — verdict correct-work PASS ; un canal de discussion n'est jamais un canal de confiance pour un identifiant — réaction systématique en 5 points : ne jamais recopier/stocker/utiliser le secret, guidance révocation autorité émettrice, re-provisionnement one-shot hors canal, consignation sans valeur du secret, publication/push par le propriétaire uniquement) ; report Tasks 10-11 exécuté sur directive explicite ; description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED + PM-INSTALL ; PM v3.29.0 archivé @historique R4 |
| v3.29.0 | 2026-10-31 | Règle d'or n°6 — langue des échanges avec le propriétaire (français) (directive propriétaire, session web-4f989063, gen-plan(step) 2026-10-31) : §1.8 — insertion n°6 (le propriétaire est adressé et répondu en français dans toute discussion — courante et futures, profils/réinstallations/reprises inclus, portée par le clone source de réinstallation règle d'or n°4 ; artefacts techniques verbatim exclus ; prime sur la langue du message sauf demande explicite contraire) ; backfill n°5 anti-aspirant (lag hérité v3.26.0 résorbé — complétion agent, texte verbatim du SKILL §1.5) ; description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED v1.7.15 (§6.1), PM-INSTALL v1.8.9 (§2ter + §A.3) ; PM v3.28.2 archivé @historique R4 |
| v3.28.2 | 2026-10-30 | Application de la recommandation E15 Task 6 (consignée au worklog, sollicitée par le propriétaire le 2026-10-30) : contingence **« récupération externe bloquée ×3-4 »** ajoutée au §4 SKILL + references/grille-token.md (tableau coefficients + historique row 14 — preuve Task 6 E15 : estimé ~17 k → réel 60-70 k, cause dominante = récupération externe adversariale des 2 liens chat.z.ai : WAF CDN 405 + SPA non rendue) ; même famille que « profil frais local » v3.28.1 ; non-régression R2 (addition pure) ; lag résorbé au passage : ligne v3.28.1 ajoutée à @historique/historiques-par-skill/gen-plan.md ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 |
| v3.28.1 | 2026-10-26 | Génération mécanique KO-L004 v1.1.0 (`scripts/generer-pm-skill.py`) : montée gen-plan v3.28.0 -> v3.28.1 — deltas sémantiques à complétion agent (rapport de couverture : scripts/generer-pm-report.json) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 |
| v3.28.0 | 2026-10-25 | Intégration du §A — DÉCLENCHEURS du PM dans le SKILL.md (tâche 1 directive 10 tâches, session web-eb6c8580) : nouvelle section §A en tête du corps du SKILL.md (miroir fidèle — 10 déclencheurs : modes gen-plan(step)/gen-plan(step-ok) + clause mode NULL, verbatim « intègre dans le plan d'actions » E13/règle d'or n°3, correct-work(projet)/correct-work(<cible>), orchestre, gen-plan:generate) + enrichissement read_when frontmatter (mentions plan d'actions / intègre dans le plan d'actions / gen-plan(step) / gen-plan(step-ok) / orchestre) ; §A du PM inchangé (source de vérité), description frontmatter inchangée — addition pure R2 ; v3.27.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé KO-L004 SHARED §6.1 / PM-INSTALL §2ter+A.3 ; constat : même lacune chez refactor-guard (PM §A v1.8.1 sans section SKILL.md — consignée) |
| v3.27.0 | 2026-10-24 | Génération mécanique KO-L004 v1.1.0 (`scripts/generer-pm-skill.py`) : montée gen-plan v3.24.0 -> v3.27.0 — deltas sémantiques à complétion agent (rapport de couverture : scripts/generer-pm-report.json) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 |
| v3.24.0 | 2026-10-24 | Génération mécanique KO-L004 v1.1.0 (`scripts/generer-pm-skill.py`) : montée gen-plan v3.23.1 -> v3.24.0 — deltas sémantiques à complétion agent (rapport de couverture : scripts/generer-pm-report.json) ; recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3 |
| v3.23.1 | 2026-10-11 | Correction outil + fusion discussion externe 468a4c26 (Task 8, session web-b4d7dd19 — gen-plan(step)) : refactoring-test n'est plus déclaré discipline — il est l'OUTIL de la discipline n°55 refactoring-engineering (directive propriétaire : « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil ») ; refactor-guard v1.7.0 déclaré (garde-fous des opérations — lignée externe 468a4c26, base hôte v1.2.0 portée R4, 11 scripts stdlib) ; fullstack-dev inscrit au registre KB (précédent vue-upload) ; toilettage KB (3 blancs parasites) ; S4 déquotes frontmatters (17 fichiers, valeurs inchangées) ; bloc PATTERN §1.6 outil+garde-fous, table §1.6 +§3 relations (refactor-guard +1 ligne) ; SHARED v1.7.3→v1.7.4 (§7 outil + registre ×3 lignes) ; PM-INSTALL v1.6.3→v1.6.4 |
| v3.23.0 | 2026-10-11 | Matérialisation des disciplines de refactoring n°55 (Task 7, session web-b4d7dd19 — directive propriétaire) : refactoring-engineering (le système de refactoring effectif déclaré comme discipline d'engineering — correct-work CIBLE/DIRECT + cascade PM + arbitres + @historique R4) ; refactoring-test (détecteur/évaluateur des situations de refactoring + graphe d'interactions/blast radius — verdict machine, bras mécanique scripts/refactoring-test-graph.py) ; bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 §1.6 (table E4/E7/E9-E14) ; table §1.6 +2 lignes ; relations §3 +2 ; KB bidirectionnelle (2 entrées n°55 + réciproques) ; SHARED §7 +2 définitions + registre n°55 |
| v3.22.1 | 2026-10-11 | Renommage du mode step-confirm → step-ok + clause mode NULL (directive propriétaire session web-b4d7dd19 — renommage demandé par le propriétaire avant compaction, jamais matérialisé dans les arbres ; clause NULL héritée de la garde propriétaire « <mode> = NULL ⇒ comportement d'avant les modes step », réserve consignée worklog Task 5) : §1.5 SKILL.md — `gen-plan(step-ok)` nom canonique (confirmation propriétaire avant chaque groupe), alias `step-confirm` (v3.22.0) et `step-confim` normalisés en `step-ok` (R4), **clause mode NULL** explicite — invocation sans `<mode>` (ex. « gen-plan : continue ») = comportement antérieur aux modes step (v3.21.0) : intégration E13 ou exécution classique, sans portes de confirmation ; une demande sans mode explicite ne route JAMAIS vers step/step-ok ; §2.2 — structure evals synchronisée (8 evals, 12 cas) ; evals.json — id 8 GP-mode-step-ok (confirmation propriétaire par groupe) + id 7 porté « modes step/step-ok » ; trigger_evals — cas step-confirm → step-ok + cas alias step-confirm (12 cas) ; description frontmatter inchangée (non-régression triggers) ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) ; recalibrage croisé KO-L004 : SHARED v1.7.2 (§6.1 gen-plan v3.22.1), PM-INSTALL v1.6.2 (§2ter + §A.3) |
| v3.22.0 | 2026-10-11 | Orchestration complète des matérialisations n°54 + déclencheurs de mode (directive propriétaire session web-b4d7dd19 — discussion parente 5ef6176f recalibrée sur l'état réel N34/Tasks 16-18, KO-L007 : matérialisation d'abord) : §1.6 SKILL.md — bloc PATTERN GEN-PLAN-DISCIPLINES-ETENDUES-v2.0.0 (table de mobilisation étendue E4/E5/E7/E9-E14 — spec-driven-development, memory-engineering, fleet-engineering orchestrées au même titre que les 4 disciplines A12) ; §1.5 — déclencheurs de mode gen-plan(step)/gen-plan(step-confirm) (alias step-confim normalisé R4, mode inconnu → clarification, jamais d'invention R2 ; coexistence avec le déclencheur verbatim règle d'or n°3) ; §3 — 3 lignes de relations détention orchestrée (bidirectionnalité SHARED §0.3 — résorption D007 du plan d'actions 2026-10-11) ; §2.2 — structure evals synchronisée (7 evals, 11 cas) ; evals.json — id 7 GP-mode-step (enchaînement autonome des groupes, correct-work(groupe) par groupe, correct-work(projet) final) ; trigger_evals — +2 positifs modes step/step-confirm, +1 négatif mode invalide (gen-plan (stp)) ; description frontmatter inchangée (non-régression triggers) ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) ; recalibrage croisé KO-L004 : SHARED v1.7.1 (§6.1 gen-plan v3.22.0), PM-INSTALL v1.6.1 (§2ter + §A.3) |
| v3.21.0 | 2026-10-09 | Règle d'or n°4 — récupération du dépôt par clone (directive utilisateur « si tu dois utiliser un élément de mon dépôt alors clone-le à la place de lire son contenu sur mon dépôt », session web-b93f42fa) : §1.8 — opérationnalisation en 5 points (déclencheur lecture/usage → clone git local shallow `--depth 1 --filter=blob:none`, jamais lecture distante API/raw/web ; mécanisme askpass éphémère, zéro persistance de jeton, publication uniquement sur validation utilisateur ; exceptions KO-L001 + écritures authentifiées + adaptation journalisée ; journalisation worklog ; continuité d'objectif) ; description frontmatter inchangée (non-régression triggers 9/9) ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) ; recalibrage croisé KO-L004 : SHARED v1.6.6 (§6.1 gen-plan v3.21.0), PM-INSTALL v1.5.1 (§2ter + §A.3) |
| v3.20.0 | 2026-10-04 | Task 29 — intégration de la garde É1-INSTALL au skill (D001 : script maître `skills/gen-plan/scripts/ensure-installed.py`, le fichier racine `scripts/ensure-installed.py` devient un shim délégant) ; mode `--preempt` (D002 : INSTALLE→PRIORITE-NONE rc 0, ROOT absent→réinstallation IMMÉDIATE PRIORITE-REINSTALL-OK, dérivé→PRIORITE-REINSTALL-REQUISE rc 2 non destructif — doctrine Task 23 conservée) ; PRÉEMPTION prescrite au §1.16 comme comportement AGENT (D003 : suspendre toute tâche, réinstaller, puis mettre à jour le plan) ; après réinstallation réussie, génération automatique d'une directive de mise à jour du plan en cours `download/plan-post-reinstall-<ts>.json` (D004 : étapes interrompues → INTERRUPT-REINSTALL, étapes idempotentes KO-L001 reprennent en l'état, re-validation arbitres E7/E8 avant reprise) ; bump 3.19.0→3.20.0 (D005, description inchangée) ; réinstallation exécutée via la garde = no-op idempotent honnête (D007-D008 : 0 modification, audit stable 74 CONFORME / 20 PARTIEL) |
| v3.19.0 | 2026-10-03 | Task 23 — routage de découverte des skills (D004) : skills-inventory PRIORITAIRE à E5/§3 (comparaison des éléments trouvés vs natifs MÉMORISÉE au registre KB), fallback skill-finder-cn avec contrôle cybersécurité audit-provenance AVANT adoption, bascule unidirectionnelle ; garde É1-INSTALL (D006) : `scripts/ensure-installed.py --check` à l'ouverture de session, préemption (suspension de toute tâche en cours) puis `--reinstall` via pipeline PM-INSTALL §2/§2bis sans persistance de jeton (anti-persistance Task 8/14) ; §3 relations (skills-inventory >=1.1.0, ajout skill-finder-cn) ; francisation D007 (skill-creator 1.1.0, version-management 1.1.0) ; recalibrage KO-L004 |
| v3.18.0 | 2026-10-02 | Application M4 leçon L007 (pièges sparse-checkout — verdict correct-work étape F PASS, cycle fusion installateurs) : §1.12bis bloc PATTERN:PM-GEN-PLAN-KO-L007-v1.0.0 ; SKILL.md §1.15 bloc PATTERN:KO-L007-v1.0.0 + note de provenance étendue ; §4 exemplaire YAML synchronisé sur le frontmatter installé (version 3.18.0, description complète, 5 dépendances) ; recalibrage KO-L004 (CORPUS_ATTENDU 24, SYNC_MAP 14, ECO_SKILLS 3.18.0) ; journal L007 statut proposé → appliqué |
| v3.17.1 | 2026-10-02 | Propagation du renommage du skill prompt-engineering (ex agent-prompt-engineering ; archive C0, census 118 refs/32 fichiers, commit a91dd80) : références opératives du PM mises à jour (§1.9 délégation, matérialisation, table de mobilisation) ; référence gen-plan patterns-avances-qwen.md alignée (mode M5) ; recalibrage croisé KO-L004 : CORPUS_ATTENDU 22, SYNC_MAP 12, manifeste intégrité régénéré, arbitres re-certifiés |
| v3.17.2 | 2026-10-02 | Déclencheur verbatim « intègre dans le plan d'actions » (directive propriétaire) : §A DÉCLENCHEURS + règle d'or n°3 point 5 (E13 — extension du plan courant, R2) ; correction E1 : référence « pipeline INSTALL-ECOSYSTEME » → pipeline d'installation P0-P7 porté par PROMPT-MAITRE-INSTALL-ECOSYSTEME.md v1.1.0 (fusion installateurs — INSTALL-ECOSYSTEME.md supprimé, source d'installation unique) ; trigger_evals 7 → 8 cas (cas verbatim positif) ; SKILL.md synchronisé (description + règle d'or n°3 + §2.2 8 cas) ; recalibrage KO-L004 (CORPUS_ATTENDU 22, SYNC_MAP 12, ECO_SKILLS 3.17.2) |
| v3.17.0 | 2026-09-27 | N23-b/N28 (session B13-r6) : §1.5 bloc PATTERN:KO-L005-v1.0.0 (généralisation règle d'or n°2 — leçon L005) ; §1.2bis hook E1-RES (n67-1 reconstitué post-wipe : B-11 + G-RES + fraîcheur du plan) ; hook PM E1-RES + KO-L005 ; relation resource-monitor |
| v3.13.0 | 2026-09-19 | Phase N20 (demande n°34) : hooks patterns avancés obligatoires (§1.12 : E1 answer key, E7/E8 arbitre answer-key-checker 16 checks, E9-E14 Graph Diamond, E15 knowledge-observer) ; 4 nouvelles références patterns ; dépendance knowledge-observer >= v1.0.0 |
| v3.16.0 | 2026-09-26 | Re-curation B13 (modes M3-M4 knowledge-observer, hook E15) : §1.12bis leçons KO-L001 (économie API 429) / KO-L003 (arbitres à invariants dynamisés) / KO-L004 (recalibrage croisé) ; arbitres n60-genplan-3160, n62-1-completude, n62-2-coherence, n63-1, n63-2 ; reconstitution post-wipe B13-r5 |
| v2.0.0 | 2026-07-18 | Version initiale (refusée par l'utilisateur) |
| v3.1.0 | 2026-07-18 | Refactoring complet suite refus v2.0.0 |
| v3.3.0 | 2026-07-29 | Ajout Registre KB, Protocole de Découverte |
| v3.5.0 | 2026-07-29 | Intégration clone-chat, calibration #token, normes N1-N3 |
| v3.6.0 | 2026-08-09 | Refactoring prompt maître : extraction du socle commun SHARED, suppression de la duplication |
| v3.6.1 | 2026-08-09 | Méthode lecture bloc par bloc (philosophie #7, E2/E9/E10), correct-work >= v2.4.0 avec hook E8, chemins references/ sans accent, description enrichie, count ~180L |
| v3.7.0 | 2026-08-30 | Règles d'or (§1.8 : adaptation autonome sur blocage, à la demande utilisateur) ; disciplines d'ingénierie de prompts (§1.9 : context/loop/graph/harness engineering) ; lien agent-prompt-engineering ; hook correct-work par phase (E9-E14 : chaque phase terminée est vérifiée par correct-work CIBLE avant la suivante) |
| v3.8.0 | 2026-09-06 | Unification du schéma evals (skill-creator) au §5 : §5.4 evals.json (id entier/prompt/expected_output/expectations), §5.5 trigger_evals.json, §5.6 workspaces d'évaluation (with_skill vs baseline) ; §1.9 matérialisation agent (references/gen-plan.agent v1.0.0) ; §1.10 pipeline d'optimisation écosystème Z0-Z6 et §1.11 idempotence R1-R6 (directive utilisateur, DOCX « Pipeline optimisation écosystème »). Aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) |
| v3.8.1 | 2026-09-06 | Description Optimization (itération-3 workspaces skill-creator, session A10) : enrichissement de la description frontmatter §4 avec « classification Type 1-4 (documents, analyse, développement web, data) » — réserve du cas déclencheur « classe cette tâche : document, analyse ou développement web ? » levée (trigger 8/9 → 9/9). Sémantique E3/§8.3 inchangée ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) |
| v3.9.0 | 2026-09-06 | Réimplantation des disciplines (directive utilisateur, session A11) : §1.9 devient l'orchestration gen-plan des 5 disciplines, la source de vérité méthodologique est déplacée vers SHARED §7 (SHARED v1.3.0) ; matérialisation des 4 disciplines d'exécution en agents ({{SKILLS_ROOT}}_disciplines/, format §2.3 autonomous-agent) et retrait de la matérialisation erronée references/gen-plan.agent (A9 — matérialisait gen-plan au lieu des disciplines) ; §1.10 actualisé ; evals version 3.9.0. Description frontmatter inchangée ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) |
| v3.10.0 | 2026-09-07 | Gestion du plan d'actions de session (directive utilisateur, session A12) : §1.8 enrichi de la règle d'or n°2 (régénération cohérente du plan d'actions actuel via le nouveau skill gen-plan à chaque installation d'un nouvel écosystème) et de la règle d'or n°3 (mise à jour cohérente du plan d'actions actuel via gen-plan à chaque nouvelle demande utilisateur pendant l'exécution) ; E13 renvoi aux règles d'or n°2-n°3 ; evals version 3.10.0. Description frontmatter inchangée (non-régression triggers 9/9) ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) |
| v3.11.0 | 2026-09-10 | Intégration du Prompt Engineering Kit v4.1 (directive utilisateur, session B1) : couche de raisonnement adaptative — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride, bascule selon complexité E1-E3, calibrage profils §2.4), blocs de sortie adaptatifs A-J mappés sur les Types 1-4 (E3), 9 règles critiques, 12 checks + scoring 25 pts (seuil 22/25) alignés sur les hooks correct-work E9-E14 ; §1.9 enrichi de l'orchestration PEK ; 6e référence `references/prompt-engineering-kit.md` (in extenso §9.6) ; §2.2 actualisée. Description frontmatter inchangée (non-régression triggers 9/9) ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) |
| v3.12.0 | 2026-09-19 | Mobilisation disciplinaire complète de la planification (audit N5-a, session B12 r19-bis ; re-montée N14-b r32 après incident B-15) : §1.9 enrichi de la table de mobilisation E1-E8 (disciplines × étapes de planification — interprétation PEK E1-E3 conforme, génération E4-E8 explicitée) ; §3 relations étendues aux 4 disciplines d'exécution (déclenchement automatique, SHARED §7) ; E1/E5/E7/E8 (§9.1) enrichies de leurs disciplines mobilisées ; aucun changement de contrat d'intégration : planchers de dépendances inchangés (SHARED §3.2 règle 5) |

Révision documentaire 2026-09-06 (sans changement de version ni de contrat) : §1.9 explicité comme détenteur de la méthode prompt-engineering (méthode-mère) ; assignation en fonction héritée enregistrée en SHARED §7, avec déclarations correspondantes dans les §B des PM correct-work v2.4.0 et clone-chat v2.0.0.

---

## §8 — NOTES DE CONCEPTION

### §8.1 Pourquoi 15 étapes ?

Les 15 étapes couvrent le cycle de vie complet d'une tâche complexe : de l'analyse initiale (E1) au bilan post-exécution (E15). Chaque étape a un objectif clair, des inputs/outputs définis, et des critères de validation. La séquence E1-E8 (planification) est suivie de E9-E14 (exécution/surveillance) et clôturée par E15 (calibration). Ce découpage permet un parallélisme partiel (E9-E14 peuvent chevaucher M2/M3) tout en gardant un contrôle strict via E11 (checkpoint) et E12 (détection d'écart).

### §8.2 Pourquoi 3 profils ?

Les profils NORMAL/ECO/VIEUX PC permettent d'adapter la planification aux contraintes matérielles et à la complexité de la tâche. Le profil ECO est conçu pour les discussions courtes (< 5 sessions) ou les tâches simples (1 skill, 1 livrable), évitant la surcharge de planification. Le profil VIEUX PC ajoute des restrictions matérielles (scripts < 100 lignes, pas de graphiques, token plafonné à 2000) pour les environnements limités.

### §8.3 Pourquoi auto-calibration ?

L'estimation en tokens est intrinsèquement imprécise. L'auto-calibration E15 permet d'améliorer continuellement les estimations en comparant le prévu au réel, avec des seuils d'action clairs (20-35% ajustement paramétrage fin, >35% recalibration complète). L'historique de calibration (voir §9.2) trace les écarts successifs pour identifier les biais systématiques.

### §8.4 Pourquoi Python uniquement ?

La règle N3 (Python uniquement) garantit la portabilité cross-platform. Les scripts shell sont dépendants du système d'exploitation, tandis que Python est universellement disponible dans l'environnement de l'assistant. Cette contrainte simplifie aussi la maintenance et réduit les risques d'incompatibilité.

---

## §9 — CONTENU IN EXTENSO DES FICHIERS RÉFÉRENCE

Les 10 fichiers référence suivants doivent être créés dans `{{SKILLS_ROOT}}gen-plan/references/` (plus 1 fichier evals). Voici leur contenu intégral.

### §9.1 `references/etapes-detaillees.md`

```markdown
# Détail des 15 étapes gen-plan

## E1 — Analyse de la demande

**Objectif** : Décortiquer la demande utilisateur pour en extraire les livrables, contraintes et critères de succès.

**Disciplines mobilisées** (v3.12.0) : prompt-engineering (PEK — interprétation CoT/Chaining/Hybride), context-engineering (lecture SHARED/KB préalable). Voir table de mobilisation §1.6.

**Inputs** :
- Message ou demande brute de l'utilisateur
- Contexte de session (worklog, artefacts précédents)
- KNOWLEDGE.md (si disponible via KB)

**Outputs** :
- Liste des livrables identifiés
- Liste des contraintes (techniques, temporelles, ressources)
- Critères de succès explicites
- Questions clarificatoires (si ambiguïté)

**Critères de validation** :
- [ ] Au moins 1 livrable identifié
- [ ] Les contraintes sont explicites
- [ ] Le type de tâche est identifiable

**Exemple** :
> Demande : « Crée un rapport d'analyse des ventes du Q3 »
> Livrables : rapport.docx, graphiques PNG
> Contraintes : données Q3, format professionnel

---

## E2 — Inventaire des ressources

**Objectif** : Faire le bilan de tout ce qui est disponible pour accomplir la tâche.

**Inputs** :
- Sortie de E1 (livrables, contraintes)
- `{{SKILLS_ROOT}}` (liste des skills installés)
- `{{KB_PATH}}` (registre KB)
- Fichiers existants dans le projet

**Méthode — Lecture bloc par bloc** :
Pour chaque fichier > 500 lignes à inventorier :
1. Lire le premier bloc (200 lignes max)
2. Produire une synthèse intermédiaire (objectif, structure, sections clés)
3. Lire le bloc suivant (200 lignes max) en utilisant la synthèse comme contexte
4. Répéter jusqu'à la fin du fichier
5. Synthèse finale consolidée
Les fichiers ≤ 500 lignes sont lus en une seule fois.

**Outputs** :
- Liste des skills disponibles et pertinents
- Liste des fichiers/sources de données existants
- Synthèses intermédiaires des fichiers volumineux
- Gaps identifiés (ressources manquantes)

**Critères de validation** :
- [ ] Skills pertinents identifiés
- [ ] Gaps clairement listés
- [ ] Pas de ressource critique manquante sans contournement
- [ ] Fichiers > 500L lus par blocs avec synthèse intermédiaire

---

## E3 — Classification du type de tâche

**Objectif** : Router la tâche vers le bon type de traitement (Type 1-4).

**Inputs** :
- Sortie de E1 (livrables)
- Sortie de E2 (ressources)
- Grille de classification (voir classification-types.md)

**Outputs** :
- Type assigné (1, 2, 3 ou 4)
- Skill principal à invoquer
- Skills secondaires éventuels
- Mode par défaut (M1-M4)

**Critères de validation** :
- [ ] Exactement 1 type assigné
- [ ] Skill principal identifié
- [ ] Pas de conflit type/skill

---

## E4 — Estimation #token

**Objectif** : Calculer le budget token de la tâche.

**Inputs** :
- Type de tâche (E3)
- Complexité estimée (simple/moyenne/complexe)
- Profil ressource cible (E6, si connu)
- Grille #token (voir grille-token.md)

**Outputs** :
- Estimation #token totale
- Estimation par étape
- Tag #token pour chaque skill utilisé

**Critères de validation** :
- [ ] Estimation dans la plage du profil
- [ ] Tags #token présents sur chaque élément du plan

---

## E5 — Sélection des skills

**Objectif** : Identifier les skills pertinents pour la tâche.

**Disciplines mobilisées** (v3.12.0) : graph-engineering (graphe KB, matrice agent × skill), context-engineering (Protocole de Découverte, lecture bloc par bloc). Voir table de mobilisation §1.6.

**Inputs** :
- Type de tâche (E3)
- Ressources disponibles (E2)
- skills-inventory (scan)
- KNOWLEDGE.md (KB)

**Outputs** :
- Liste ordonnée des skills à utiliser
- Version minimale requise pour chaque skill
- Nature de l'utilisation de chaque skill

**Critères de validation** :
- [ ] Chaque skill cité existe dans le registre ou l'inventaire
- [ ] Versions minimales cohérentes
- [ ] Pas de doublon

---

## E6 — Profilage ressource

**Objectif** : Choisir le profil de ressource adapté.

**Inputs** :
- Estimation #token (E4)
- Complexité de la tâche
- Contraintes matérielles (si connues)
- Grille des profils (voir profils-ressource.md)

**Outputs** :
- Profil assigné (NORMAL/ECO/VIEUX PC)
- Justification du choix
- Restrictions activées (si profil réduit)

**Critères de validation** :
- [ ] 1 profil assigné
- [ ] Justification cohérente avec les inputs

---

## E7 — Création du plan

**Objectif** : Assembler le plan d'exécution structuré.

**Disciplines mobilisées** (v3.12.0) : loop-engineering (boucles R3 prédéfinies — règle d'or n°1), context-engineering (plan auto-suffisant), harness-engineering (hooks par phase E9-E14, worklog structuré). Voir table de mobilisation §1.6.

**Inputs** :
- Livrables (E1), Skills (E5), Profil (E6), #token (E4)

**Outputs** :
- Plan structuré : étapes, dépendances, checkpoints, #token par étape
- TODO list ordonnée
- Identification des étapes parallélisables

**Critères de validation** :
- [ ] Toutes les étapes E9-E14 couvertes
- [ ] Dépendances explicites
- [ ] Au moins 1 checkpoint
- [ ] #token total cohérent avec E4

---

## E8 — Validation du plan

**Objectif** : Vérifier cohérence, complétude et faisabilité.

**Disciplines mobilisées** (v3.12.0) : harness-engineering (hook correct-work — 3 verdicts), prompt-engineering (12 checks PEK — scoring 22/25). Voir table de mobilisation §1.6.

**Inputs** :
- Plan brut (E7), Contraintes (E1)

**Outputs** :
- Plan validé (ou révisé)
- Liste des risques et plans de contournement

**Critères de validation** :
- [ ] Cohérence interne (pas de contradiction)
- [ ] Complétude (tous les livrables couverts)
- [ ] Faisabilité (ressources suffisantes)
- [ ] Pas de cycle dans les dépendances

---

## E9 — Lancement de l'exécution

**Objectif** : Démarrer l'exécution selon le plan validé.

**Inputs** : Plan validé (E8), Contexte session

**Méthode — Lecture bloc par bloc** :
Si les fichiers sources de l'étape E9 sont > 500 lignes, appliquer la méthode de lecture par blocs (voir E2) avant de démarrer l'exécution.

**Outputs** : Première étape lancée, Entrée worklog initialisée

**Critères** : [ ] Exécution démarrée, [ ] Worklog initialisé, [ ] Fichiers volumineux synthétisés par blocs

---

## E10 — Suivi d'étape

**Objectif** : Monitorer chaque étape en cours.

**Inputs** : Plan en cours (E8), État réel

**Méthode — Lecture bloc par bloc** :
Lors du suivi d'étapes manipulant des fichiers > 500 lignes, vérifier la cohérence bloc par bloc (ne pas relire le fichier intégralement, utiliser les synthèses produites à E2/E9).

**Outputs** : Entrée worklog par étape, #token réel, Écarts éventuels

**Critères** : [ ] Chaque étape terminée loggée, [ ] #token réel mesuré, [ ] Fichiers volumineux traités par synthèse de blocs

---

## E11 — Checkpoint intermédiaire

**Objectif** : Vérification à mi-parcours.

**Inputs** : Avancement (E10), Plan initial (E8)

**Outputs** : Bilan mi-parcours, Ajustements mineurs, Décision (continuer/ajuster/arrêter)

**Critères** : [ ] Checkpoint à ~50%, [ ] Décision documentée

---

## E12 — Détection d'écart

**Objectif** : Comparer réel vs estimé.

**Inputs** : #token estimé (E4), #token réel (E10)

**Outputs** : Tableau des écarts, Alertes si > 20%

**Critères** : [ ] Écarts calculés, [ ] Alertes si seuil dépassé

---

## E13 — Ajustement

**Objectif** : Modifier le plan en cas de dérive.

**Inputs** : Écarts (E12), Plan en cours (E8)

**Outputs** : Plan révisé (si nécessaire), Justification, Nouvelle estimation

**Critères** : [ ] Modifications justifiées, [ ] Plan révisé cohérent

---

## E14 — Finalisation

**Objectif** : Achèvement des étapes restantes.

**Inputs** : Plan (révisé ou non), État d'avancement

**Outputs** : Toutes les étapes terminées, Livrables finaux, Worklog complet

**Critères** : [ ] Tous les livrables produits, [ ] Worklog à jour

---

## E15 — Bilan et auto-calibration

**Objectif** : Retour d'expérience et mise à jour des grilles.

**Inputs** : Plan initial (E8), Worklog complet, #token estimé vs réel

**Outputs** :
- Bilan de la session
- Mise à jour grille #token (si écart > 20%)
- Enrichissement KNOWLEDGE.md (si `{{KB_ENABLED}}`)
- Déclenchement éventuel de clone-chat

**Critères** : [ ] Bilan produit, [ ] Calibration mise à jour si nécessaire, [ ] KNOWLEDGE.md enrichi si pertinent

---

## Portées étendues (E8, E14, E15)

Les étapes E8, E14 et E15 incluent des portées héritées des versions antérieures du protocole :

**E8 — Validation du plan** inclut aussi les vérifications de qualité pré-intégration :
- [ ] Chaque fichier candidat à l'intégration est classifié : Skill / Écosystème / Utilitaire
- [ ] Les fichiers Skill ont un YAML frontmatter valide (name, description, > 200 chars)
- [ ] Les scripts Python compilent (pas de syntax error, imports valides)
- [ ] Les fichiers Markdown sont structurés (titres, sections cohérentes, pas de contenu tronqué)
- [ ] Les fichiers de configuration (JSON/YAML) sont valides
- [ ] Les références croisées entre fichiers sont valides

**E8 — Hook correct-work** (si correct-work >= v2.4.0 est disponible) :
- [ ] Après validation du plan, lancer `correct-work(cibles, mode=CIBLE)` sur les livrables produits
- [ ] Si correct-work retourne FAIL, l'exécution est mise en pause jusqu'à correction
- [ ] Si correct-work retourne PASS AVEC RÉSERVES, les réserves sont loggées et l'exécution continue
- [ ] Si correct-work retourne PASS, l'exécution passe directement à E9

**Hook correct-work par phase (E9-E14)** (si correct-work >= v2.4.0 est disponible) :
- [ ] Dès qu'une phase du plan d'actions vient de se terminer, lancer `correct-work(livrables de la phase, mode=CIBLE)` AVANT d'entamer la phase suivante
- [ ] Si correct-work retourne FAIL, l'exécution est mise en pause jusqu'à correction de la phase, puis re-vérification
- [ ] Si correct-work retourne PASS AVEC RÉSERVES, les réserves sont loggées dans le worklog et l'exécution continue
- [ ] Si correct-work retourne PASS, la phase suivante démarre
- [ ] Le hook E8 (fin de plan) reste inchangé et constitue la vérification finale

**E14 — Finalisation** inclut l'intégration écosystème :
- [ ] Les fichiers Skill sont placés dans `{{SKILLS_ROOT}}<nom>/SKILL.md`
- [ ] Les fichiers de référence vont dans `{{SKILLS_ROOT}}<nom>/references/`
- [ ] Aucun skill existant n'est écrasé sans confirmation utilisateur
- [ ] Le YAML frontmatter est conforme (SHARED §1.3)
- [ ] L'inventaire des skills est mis à jour si nécessaire

**E15 — Bilan** inclut l'auto-réapplication :
- [ ] Si le SKILL.md de gen-plan a été modifié pendant l'exécution, les tâches restantes sont réévaluées
- [ ] Les tâches affectées sont marquées `[REEVALUER]` avec la raison et les sections impactées
- [ ] Chaque réévaluation est documentée dans le worklog
```

### §9.2 `references/grille-token.md`

```markdown
# Grille de calibration #token — gen-plan v3.7.0

## Grille par agent/skill

| Agent/Skill | #token sortie (min) | #token sortie (max) | Coeff. complexité |
|-------------|--------------------|--------------------|------------------|
| Planification E1-E2 | 800 | 1500 | 1.0x |
| Classification E3 | 200 | 500 | 1.0x |
| Estimation E4 | 300 | 800 | 1.0x |
| Sélection E5 | 500 | 1200 | 1.2x |
| Profilage E6 | 200 | 400 | 1.0x |
| Création plan E7 | 1000 | 2500 | 1.5x |
| Validation E8 | 500 | 1500 | 1.0x |
| Exécution simple (1 skill) | 2000 | 5000 | 1.0x |
| Exécution moyenne (2-3 skills) | 5000 | 10000 | 1.3x |
| Exécution complexe (4+ skills) | 10000 | 20000 | 1.5x |
| Surveillance E10-E12 | 500 | 1500 | 1.0x |
| Auto-calibration E15 | 800 | 2000 | 1.0x |

## Grille par type de tâche (usage clone-chat)

| Mode | Longueur discussion | #token estimé | Profil min. |
|------|---------------------|---------------|-------------|
| clone-court | < 5 sessions | 2000-3500 | ECO |
| clone-moyen | 5-15 sessions | 3500-5500 | NORMAL |
| clone-long | > 15 sessions | 5500-9000 | NORMAL |

> Note (historique v1.2.0) : estimation +10% pour couvrir l'Étape 3.5 Context Drift et l'intégration gen-plan.

## Coefficients d'ajustement

| Facteur | Coefficient | Condition |
|---------|-------------|-----------|
| Complexité faible | 0.8x | Tâche routinière, template existant |
| Complexité standard | 1.0x | Cas nominal |
| Complexité élevée | 1.3x | Multi-skills, dépendances croisées |
| Complexité critique | 1.5x | Projet nouveau, aucune référence |
| Profil ECO | 0.7x | Réduction surveillance, snippets simplifiés |
| Profil VIEUX PC | 0.5x | Scripts légers, pas de graphiques |
| **Profil frais local** | **3-4x** (v3.28.1) | Première exécution sur profil restauré/réinstallé — coût de découverte du corpus (lectures multi-fichiers, PMs longs, KB, outillage) non couvert par les grilles calibrées sur environnement établi |
| **Appels API en masse** | **2-3x** (v3.28.1) | Phases avec appels LLM/API répétés — rate-limit 429, retries, backoff 12-48 s + pause anti-rafale 45 s ; guidance : ThreadPoolExecutor 2-4 workers, throttle 1-2 s/appel, journal d'état idempotent, tri par taille croissante |
| **Récupération externe bloquée** | **3-4x** (v3.28.2) | Contenu externe adversarial (WAF CDN 405, SPA non rendue en headless, rate-limit API web) — multi-tours de contournement règle d'or n°1 avant la voie gagnante (escalade : WebFetch → curl → agent-browser [double-open] → z-ai function `page_reader`), puis lecture intégrale du contenu récupéré ; la campagne de récupération porte son budget propre AVANT l'étape qui la requiert (preuve : Task 6 E15 — 2 liens chat.z.ai, 10+ tours d'adaptation, ~60 k de texte ; recommandation E15 consignée au worklog, sollicitée par le propriétaire) |

## Historique de calibration

| Exécution | Date | Type tâche | #token estimé | #token réel | Écart | Action |
|-----------|------|-----------|---------------|-------------|-------|--------|
| 1 | 2026-07-18 | Planification 66 skills | 4500 | 5200 | +15.6% | Aucune (0-20%) |
| 2 | 2026-07-18 | Test E2E gen-plan | 3000 | 3600 | +20.0% | Aucune (seuil) |
| 3 | 2026-07-29 | clone-chat v1.1.0 | 4000 | 5200 | +30.0% | Ajustement grille |
| 4 | 2026-07-29 | clone-chat v1.2.0 (historique) | 4400 | 4600 | +4.5% | Aucune (0-20%) |
| 5 | 2026-08-29 | correct-work PROJET écosystème | 12000 | ~11000 | -8.3% | Aucune (0-20%) |
| 6 | 2026-08-29 | Frontmatters + clone-chat 08-29 | 10000 | ~9500 | -5.0% | Aucune (0-20%) |
| 7 | 2026-08-29 | QA clone GML + spell-check | 11000 | ~9800 | -10.9% | Aucune (0-20%) |
| 8 | 2026-08-30 | ZIP v1.1.0 + réconciliation | 9000 | ~8800 | -2.2% | Aucune (0-20%) |
| 9 | 2026-08-30 | correct-work PROJET + archéologie versions + lignée clones | 9500 | ~9800 | +3.2% | Aucune (0-20%) |
| 10 | 2026-08-30 | correct-work PROJET + alignement gen-plan v3.7.0 au sein de correct-work | 9000 | ~9200 | +2.2% | Aucune (0-20%) |
| 11 | 2026-08-30 | Propagation knowledge-repo (Tasks 8-9, commit c79fdb6) | 4500 | ~4700 | +4.4% | Aucune (0-20%) |
| 12 | 2026-10-25 | Audit écosystème complet (profil frais local — session web-eb6c8580, Tasks 1-5) | 12200 | ~52000 | ×3-4 (326 %) | **Recalibration complète** : + coefficient profil frais local ×3-4 (row v3.28.1) |
| 13 | 2026-10-26 | Directive 10 tâches P0-P2 (session web-eb6c8580 — 233 fichiers API en masse, rate-limit 429) | 78000 | ~120000 (partiel) | ×1,5-1,7 (grille déjà recalibrée ×3-4 au plan) | Contingence API en masse ×2-3 + guidance parallélisation ajoutées (row v3.28.1) |
| 14 | 2026-10-30 | Task 6 publication GO + trio TSI + re-mesure voie L (session web-eb6c8580 — récupération externe adversariale : 2 liens chat.z.ai, WAF CDN 405 + SPA non rendue) | 17000 | ~60000-70000 (ressenti, non instrumenté) | ×3,5-4 (> 35 %) | **Contingence « récupération externe bloquée ×3-4 » ajoutée** (row v3.28.2 — recommandation E15 Task 6 consignée au worklog, sollicitée par le propriétaire le 2026-10-30) |
```

<!-- BLOC-DEPLACÉ:contingences:v3.38.0:04dbc8a16d98f41c -->

## Contingences de calibration (déplacées du SKILL.md §4 — re-curation R1 v3.39.0, 2026-11-08)

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `04dbc8a16d98f41c67570fb480e57b964fa28a3e34cd2d13e1692058eb143e66`.

- **Coefficient profil frais local ×3-4** (v3.28.1 — recalibration E15, session web-eb6c8580) : première exécution sur un profil local restauré/réinstallé — le coût de DÉCOUVERTE du corpus (lectures multi-fichiers, PMs longs, registre KB, outillage) n'est pas couvert par les grilles calibrées sur environnement établi (preuve : session audit 2026-10-25, estimé 12,2 k → réel 45-60 k)
- **Contingence appels API en masse ×2-3** (v3.28.1) : toute phase mobilisant des appels LLM/API répétés (traduction batch, génération, synchronisation) subit le rate-limit (HTTP 429), les retries et le backoff (12-48 s + pause anti-rafale 45 s) — guidance de parallélisation : `ThreadPoolExecutor` 2-4 workers, throttle 1-2 s/appel, journal d'état idempotent (reprise par lots — anti-perte au reset, D008), fichiers traités triés par taille croissante (les petits d'abord)
- **Contingence récupération externe bloquée ×3-4** (v3.28.2 — recommandation E15 Task 6, sollicitée par le propriétaire) : la récupération de contenu externe adversarial (WAF CDN 405, SPA non rendue en headless, rate-limit API web) exige des multi-tours de contournement (règle d'or n°1 — escalade WebFetch → curl → agent-browser [double-open] → z-ai function `page_reader`) puis la lecture intégrale du contenu récupéré — la campagne de récupération porte son budget propre ×3-4 AVANT l'étape qui la requiert (preuve : Task 6 E15, estimé ~17 k → réel 60-70 k ; même famille que « profil frais local »)
### §9.3 `references/classification-types.md`

```markdown
# Classification des types de tâches — gen-plan E3

## Type 1 — Document création

**Indicateurs** :
- Mots-clés : rapport, document, article, analyse, proposition, PRD, script, manuscrit, présentation, tableur
- Formats : DOCX, PDF, XLSX, PPTX, MD
- Verbes : rédiger, créer, générer, produire, écrire, composer

**Skill à invoquer** :
- docx → `docx`
- PDF → `pdf`
- Tableur → `xlsx`
- Présentation → `pptx`
- Markdown seul → aucun skill (rédaction directe)

**Exemples** :
- "Écris un rapport d'analyse" → Type 1, skill docx
- "Génère une présentation" → Type 1, skill pptx

**Contre-exemples** :
- "Affiche ces données en graphique" → Type 2
- "Construis une page web" → Type 3

---

## Type 2 — Data Visualization

**Indicateurs** :
- Mots-clés : graphique, chart, diagramme, mind map, flowchart, architecture, visualisation
- Formats : PNG, SVG, Mermaid, D3, ECharts
- Verbes : tracer, dessiner, visualiser, représenter

**Skill** : `charts`

**Sous-routage** :
- Données chiffrées → matplotlib/seaborn/echarts
- Structure/diagramme → Mermaid ou Playwright+CSS
- Mind map → Playwright+CSS (pas matplotlib)
- Dashboard → charts d'abord, puis Type 3 si interactif

---

## Type 3 — Interactive Web Development

**Indicateurs** :
- Mots-clés : site web, application, dashboard interactif, page, interface, Next.js, React
- Interactivité : cliquable, dynamique, temps réel, formulaire, navigation
- Verbes : construis, développe, crée une app, build

**Skill** : `fullstack-dev`

**Contre-exemples** :
- "Génère un dashboard en PDF" → Type 1
- "Affiche des données en graphique statique" → Type 2

---

## Type 4 — Data Processing

**Indicateurs** :
- Mots-clés : analyse, traiter, transformer, calculer, extraire, filtrer, convertir
- Absence de livrable document final
- Focus sur le traitement de données

**Action** : Écrire un script Python directement

---

## Cas ambigus — Règle de décision

| Situation | Règle | Type |
|-----------|-------|------|
| "Dashboard" sans précision | Demander : interactif ou statique ? | 3 si interactif, 1/2 si statique |
| "Analyse" avec sortie document | Finalité = document | Type 1 |
| "Analyse" sans sortie | Traitement de données | Type 4 |
| "Visualisation" dans un document | Finalité = document | Type 1 (charts embarqués) |
| "Visualisation" autonome | Finalité = visuel | Type 2 |
| Mention Next.js/React | Toujours web dev | Type 3 |
```

### §9.4 `references/profils-ressource.md`

```markdown
# Profils ressource — gen-plan v3.7.0

## NORMAL

**Contexte** : Ressources standards, sans contrainte.
**Déclenchement** : Par défaut.

**Règles** :
- 15 étapes exécutées
- Tous les skills disponibles
- Surveillance complète (E10-E12)
- Snippets complets et versionnés
- Graphiques et visuels autorisés

**Seuils** : #token sans plafond, E10+E11+E12 obligatoires.

---

## ECO

**Contexte** : Discussion courte ou tâche simple.

**Déclenchement** :
- Discussion < 5 sessions
- #token estimé < 3500
- Tâche simple (1 skill, 1 livrable)
- Demande explicite de l'utilisateur
- **1 signal de pression** détecté (§2.4.1 du SKILL.md)

**Règles** :
- Étapes réduites : E1-E9 puis E14-E15 (E10-E13 fusionnées)
- Snippets simplifiés (pas de versionnage)
- 1 checkpoint unique à E11
- Pas de matrice dynamique KB (statique seulement)
- Sous-tâches > 8000 #token exclues du plan (filtrage E4)

**Restrictions** :
- Pas de rapport de vérification détaillé
- Auto-calibration E15 simplifiée (ajustement seulement si > 35%)
- Pas de déclenchement clone-chat automatique

---

## VIEUX PC

**Contexte** : Environnement matériel limité.

**Déclenchement** :
- Demande explicite de l'utilisateur
- Environnement détecté comme limité
- **2+ signaux de pression** ou **1 signal critique** (§2.4.1 du SKILL.md)

**Règles ECO** : toutes les règles ECO s'appliquent (filtrage > 5000 #token).

**5 règles supplémentaires** :

1. **Dépendances séquentielles uniquement** — Pas de parallélisme. Chaque étape doit être terminée avant de commencer la suivante.
2. **Choix agent/skill justifié par le coût** — Toujours choisir l'agent ou le skill le moins cher qui suffit pour la tâche. Justifier le choix dans le plan.
3. **Budget ressource par phase** — Le budget #token est alloué par phase (E1-E8, E9-E14, E15), jamais global. Si une phase dépasse son budget, les étapes restantes sont reportées.
4. **Actions d'économie explicites** — Résumé de contexte avant chaque étape majeure, troncature des fichiers > 500 lignes, pas de relecture intégrale.
5. **Plan de contingence** — Si le profil se dégrade encore (3+ signaux critiques), basculer en mode survie : seules les étapes E1, E3, E7, E14 sont exécutées.

**Restrictions supplémentaires** :
- Pas de génération d'images
- Scripts < 100 lignes
- Préférer O(n) à O(n²)
- Pas de chargement de gros fichiers en mémoire
- Scripts Python légers uniquement (pas de bibliothèques lourdes)
- Pas de graphiques Matplotlib/Seaborn
- Pas de Playwright
- Préférer les sorties Markdown/texte

**Seuils** : #token plafond 2000, pas de graphiques.

---

## Règle de downgrade irréversible

Le profil ne remonte jamais automatiquement au cours d'une session :
- NORMAL → ECO : définitif pour la session
- ECO → VIEUX PC : définitif pour la session
- NORMAL → VIEUX PC : définitif pour la session

Le profil initial est NORMAL sauf détection de signaux de pression dès E2.
```

---

### §9.5 `references/guide-selection-agent-skill.md`

```markdown
# Guide de Sélection Agent/Skill — gen-plan E5/E7

## Arbre de décision

```
1. Existe-t-il un SKILL correspondant ?
   |-- OUI -> Charger le skill
   |   |-- Le skill bénéficie-t-il d'un agent spécialisé ?
   |       |-- OUI -> Skill + Agent Spécialisé (OPTIMAL)
   |       |-- NON -> Skill seul via agent général (BON)
   |-- NON -> Existe-t-il un agent spécialisé ?
       |-- OUI -> Agent Spécialisé seul
       |-- NON -> Agent général (DERNIER RECOURS)
```

## Critères de sélection (ordonnés par impact performance)

1. **Skill + agent spécialisé** (meilleure performance) — Un skill dont le protocole correspond à la tâche ET qui délègue en interne à un agent spécialisé.
2. **Skill seul** (bonne performance) — Un skill dont le protocole couvre entièrement la tâche.
3. **Agent spécialisé seul** (performance modérée) — Aucun skill correspondant, mais un agent spécialisé couvre la tâche.
4. **Agent général** (fallback) — Ni skill ni agent spécialisé. Ne jamais utiliser comme premier choix.

## Tableau de correspondance

| Type de tâche | Skill | Agent | Performance |
|--------------|-------|-------|-------------|
| Dev web Next.js | fullstack-dev | full-stack-developer | OPTIMAL |
| Création PPT/slides | pptx | ppt-expert | OPTIMAL |
| Génération PDF | pdf | general-purpose | OPTIMAL |
| Compréhension images | VLM | general-purpose | OPTIMAL |
| Charts/diagrammes | charts | general-purpose | OPTIMAL |
| Documents Word | docx | general-purpose | BON |
| Fichiers Excel | xlsx | general-purpose | BON |
| Recherche web | web-search | general-purpose | BON |
| Extraction web | web-reader | general-purpose | BON |
| Création skills | skill-creator | general-purpose | BON |
| Génération images | image-generation | general-purpose | BON |
| Édition images | image-edit | general-purpose | BON |
| Speech-to-text | ASR | general-purpose | BON |
| Text-to-speech | TTS | general-purpose | BON |
| Video understanding | video-understand | general-purpose | BON |
| LLM chat | LLM | general-purpose | BON |
| Recherche images | image-search | general-purpose | BON |
| Navigation web | agent-browser | general-purpose | BON |
| Exploration fichiers | — | Explore | Agent seul |
| Architecture/planif | — | Plan | Agent seul |
| Styling CSS | — | frontend-styling-expert | Agent seul |
| Vérification correction | correct-work | general-purpose | BON |
```

### §9.6 `references/prompt-engineering-kit.md`

```markdown
# Prompt Engineering Kit (PEK) v4.1 — Méthode de raisonnement adaptative

> **Rôle dans gen-plan** : matérialisation opérationnelle de la philosophie §1.4.6 (« CoT + Chaining avec auto-correction »). La sélection du mode de raisonnement s'effectue à E3 (complexité) et se combine avec le profil ressource (§2.4). Les blocs adaptatifs A-J structurent les livrables de sortie selon le Type 1-4.
> **Provenance** : PEK v4.1-META-PROMPT-EDITED (upload 2026-09-10, édition 2025-07-13) — intégrée par assemblage (§3.2 PM-INSTALL) ; modules d'implémentation web éliminés. Sources secondaires : V4.0-Consolidated (méta-prompt auto-suffisant), kits v3.0.0/v3.0.1 (blocs A-J).

---

## §1 — Les 3 modes d'exécution

| Mode | Pipeline | Complexité cible | Équivalent gen-plan |
|------|----------|------------------|---------------------|
| **CoT** (défaut) | 7 étapes séquentielles | moyenne à complexe | Profil NORMAL — plan complet E1-E15 |
| **Chaining** | 4 étapes pipeline | simple, linéaire | Profil ECO — étapes réduites, 1 checkpoint |
| **Hybride** (auto) | Bascule dynamique | détectée à l'étape 1 | Règle §2.4 signaux de pression → ECO/VIEUX PC |

**Règle de bascule (mode Hybride)** : complexité `simple` → Chaining ; complexité `moyen`/`complexe` → CoT. La complexité est déterminée à la première étape (Compréhension) — jamais recalculée en cours d'exécution (cohérent avec §1.4.8 : downgrade irréversible).

---

## §2 — Pipeline CoT (7 étapes)

| # | Étape | Durée indicative | Livrable |
|---|-------|------------------|----------|
| 1 | **Compréhension** | 5-10 min | Résumé exécutif : type de projet, objectif en une phrase, contraintes majeures, niveau de complexité |
| 2 | **Décomposition** | 5 min | Carte des composants + dépendances + patterns + sélection des blocs A-J |
| 3 | **Extraction** | 10-15 min | Liste exhaustive : objectifs, règles absolues, étapes, format de sortie, style, stack |
| 4 | **Structuration** | 10 min | Plan de mapping éléments → architecture du livrable (blocs sélectionnés) |
| 5 | **Génération** | 20-30 min | Livrable complet, blocs générés dans l'ordre |
| 6 | **Validation** | 10 min | Score qualité (§6) + rapport de validation |
| 7 | **Amélioration** | 5 min | 3 points d'amélioration concrets + cas limites non couverts + tests additionnels |

**Contrainte C1** : séquence stricte 1→7, aucun saut, aucune fusion d'étapes. Revenir en arrière est autorisé (cohérent avec E12-E13 détection d'écart → ajustement).

---

## §3 — Pipeline Chaining (4 étapes)

| # | Étape | Livrable |
|---|-------|----------|
| 1 | **Préparation** | Inventaire structuré des composants, métadonnées, patterns, blocs pertinents |
| 2 | **Traitement** | Contenu détaillé de chaque bloc (versions intermédiaires) |
| 3 | **Vérification** | Auto-évaluation (cohérence, complétude, exemples 4+ domaines) + corrections appliquées |
| 4 | **Optimisation** | Livrable final en 3 versions : Pro (annoté), Clean (prêt à l'emploi), Compacte (synthèse) |

---

## §4 — Blocs de sortie adaptatifs (A-J)

La structure de sortie n'est **pas figée** : elle s'adapte au livrable produit.

### Hiérarchie de priorité

- **Niveau 1 (obligatoires)** : `A` Résumé exécutif (toujours premier) · `H` Recommandations (toujours dernier)
- **Niveau 2 (fortement recommandés)** : `C` Prompt/Instructions · `E` Contraintes & règles · `G` Guide d'utilisation
- **Niveau 3 (contextuels)** : `B` Architecture · `D` Données & schemas · `F` Résultats & outputs · `I` Tests & validation · `J` Glossaire & références

### Correspondance Type de tâche (E3) → blocs

| Type gen-plan | Blocs recommandés |
|---------------|-------------------|
| Type 1 (documents) | A + C + D + E + G + H + J |
| Type 2 (visualisation) | A + C + D + F + G + H |
| Type 3 (développement web) | A + B + C + D + E + G + H + I |
| Type 4 (traitement données) | A + B + D + E + F + G + H + I |
| Méta-outil / écosystème | A + B + C + D + E + F + G + H + I + J |

### Règles de composition

1. Bloc `A` toujours en premier, bloc `H` toujours en dernier.
2. Ordre des blocs contextuels libre (enchaînement le plus logique).
3. Chaque bloc autonome — compréhensible sans lire les autres.
4. Cohérence inter-blocs — aucune contradiction ni redondance (hook correct-work E9-E14).
5. Nombre total recommandé : **5 à 9 blocs** selon la complexité.

---

## §5 — Les 9 règles critiques

| # | Règle | Priorité | Autorisé / Interdit |
|---|-------|----------|---------------------|
| 1 | **Préservation de l'original** | CRITICAL | Structurer, clarifier, organiser / inventer, modifier les décisions, dénaturer |
| 2 | **Complétude des livrables** | CRITICAL | Contenu minimal avec `[À COMPLÉTER]` / omettre un livrable, vide silencieux |
| 3 | **Cohérence des références** | CRITICAL | Chemins relatifs, liens valides / référencer l'inexistant, chemins absolus, liens brisés |
| 4 | **Respect des schemas** | CRITICAL | Valider la conformité, signaler les écarts / output non conforme, champs ignorés |
| 5 | **Application du pipeline** | CRITICAL | Prendre le temps, revenir en arrière / sauter ou mélanger les étapes |
| 6 | **Qualité des exemples** | CRITICAL | Cas limites, 4+ domaines / exemples génériques, mono-domaine, doublons |
| 7 | **Automatisation et versionnage** | CRITICAL | Outils automatisés, traçage VERSION / générer manuellement si script existe |
| 8 | **Détection de contenu trompeur** | HIGH | Vérifier les allégations / greenwashing, fausses promesses, statistiques inventées |
| 9 | **Boucle de feedback itérative** | HIGH | Intégrer les métriques A/B / ignorer les données quantitatives disponibles |

Les règles 1-7 héritent des contraintes absolues V4.0 ; les règles 8-9 sont les ajouts v4.1.

---

## §6 — Contrôle qualité (12 checks, scoring 25 pts)

**Structure du score** : Complétude 10 pts · Cohérence 8 pts · Qualité 7 pts. **Seuil minimum : 22/25 (88%)** — cohérent avec les verdicts correct-work (S1-S4) et l'arbitre verify-cross.

| # | Check | Axe |
|---|-------|-----|
| 1 | Tous les livrables présents et non vides | Complétude |
| 2 | Références croisées valides | Complétude |
| 3 | Livrable directement utilisable (zéro placeholder non signalé) | Complétude |
| 4 | Exemples pertinents, 4+ domaines variés | Cohérence |
| 5 | Structure de sortie adaptée au type de tâche | Cohérence |
| 6 | Format d'entrée correctement pris en compte | Cohérence |
| 7 | Version tracée (registre KB / VERSION) | Complétude |
| 8 | Pas de contenu trompeur détecté | Qualité |
| 9 | Mécanismes de feedback prévus | Qualité |
| 10 | Variables et placeholders définis | Qualité |
| 11 | Cas d'erreur couverts | Cohérence |
| 12 | Instructions claires et non ambigües | Qualité |

**Verdicts** : 25/25 PARFAIT · 22-24 EXCELLENT · 20-21 ACCEPTABLE · <20 À REPRENDRE. Score < 22 → corriger puis re-valider (boucle E12-E13).

### Cas limites (edge cases)

| Cas | Conduite |
|-----|----------|
| Données manquantes | Signaler les champs requis, proposer les formats, NE PAS générer |
| Contexte incomplet | Livrable partiel avec `[À COMPLÉTER]`, aucun contenu inventé |
| Contraintes contradictoires | Identifier chaque contradiction, proposer une résolution |
| Auto-référence | Détecter la circularité → rapport d'auto-analyse, pas de génération imbriquée |
| Génération circulaire | Détecter et interrompre, recommander correction directe |
| Input corrompu | Signaler l'erreur, proposer alternative de format |

---

## §7 — Mapping gen-plan ↔ PEK

| gen-plan (E1-E15) | Étape PEK correspondante |
|--------------------|--------------------------|
| E1 Analyse de la demande | 1 Compréhension (objectif, contraintes, complexité) |
| E2 Inventaire des ressources | 1 Compréhension (fin) — signaux de pression = données manquantes |
| E3 Classification Type 1-4 | 1 Compréhension — type de projet + sélection mode (CoT/Chaining/Hybride) |
| E4 Estimation #token | (spécifique gen-plan — grille §4, coeffs mode PEK applicables) |
| E5 Sélection des skills | 2 Décomposition (blocs A-J) |
| E6 Profilage ressource | 1 Compréhension — calibre le mode d'exécution (cf. §1) |
| E7 Création du plan | 4 Structuration (mapping éléments → blocs) |
| E8 Validation du plan | 6 Validation (pré-validation du plan, hook correct-work) |
| E9-E14 Exécution + hooks | 5 Génération (blocs) + 6 Validation par phase (mode CIBLE) |
| E15 Bilan et auto-calibration | 7 Amélioration (3 points concrets + calibration grille) |

**Règle d'usage** : le PEK ne remplace PAS les 15 étapes — il fournit le **mode de raisonnement** (§1) et la **structure de sortie** (§4) mobilisés par les étapes. Les livrables des plans génèrent leurs blocs selon le Type ; la validation par phase applique les 12 checks ; le score 22/25 s'ajoute aux critères correct-work.

---

## §8 — Provenance et historique

| Version | Nature | Apport |
|---------|--------|--------|
| v1.0 | Kit standalone (structure XML) | Structure modulaire initiale |
| v2.0 | Templates complets | Modules 00-07 |
| v3.0 | Fusion XML + Markdown | 8 modules prompts, build assemblé |
| v3.1 | Universel multi-format | Blocs A-J adaptatifs, 10 tests, structure adaptative |
| v4.0 | Consolidé auto-suffisant | 7 contraintes CRITICAL, edge cases, scoring 25 pts, quickstart zéro placeholder |
| v4.1 | Interface web + 3 modes | Modes CoT/Chaining/Hybride, règles 8-9, 12 checks, buildSystemPrompt() |

**Note d'intégration** : la présente référence est la forme « méthode pure » du PEK v4.1 édité — les modules d'implémentation web (stack Next.js 16, interface 5 onglets, Prisma/SQLite, pipeline temps réel, z-ai-web-dev-sdk, buildSystemPrompt) ont été écartés lors de l'assemblage : ils relèvent d'une matérialisation applicative, pas de la méthode mobilisable par gen-plan (skill prompt pur, auto-contenu, zéro dépendance d'infrastructure — §0 règle zéro). L'implémentation de référence reste documentée dans l'archive source (upload/pek-v4.1.zip).
```
### §9.7 `references/journal-versions.md`

```markdown
# Journal des versions — gen-plan (archive intégrale)

> **Mécanique de migration (v3.39.0)** : le SKILL.md §5.6 ne conserve que l'entrée COURANTE ; à chaque montée de version suivante, l'entrée courante migre ici (R4 byte-identité) et la nouvelle prend sa place inline.


<!-- BLOC-DEPLACÉ:journal_versions:v3.38.0:40c78cc14025e895 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `40c78cc14025e89587bdea18afd63779ce412dd74e78e77ed30fed239b5cd39b`.

- **v3.37.1 (2026-11-07, session web-c30e6506 — Task 61 G3, ticket F-V1-1 des vagues de tests V1 : non-régression triggers du déclencheur « met à jour »)** : `evals/trigger_evals.json` 13 → **15 cas** (+1 positif « Met à jour le plan d'actions avec les nouvelles demandes du jour. » → déclencheur verbatim de consolidation v3.37.0 ; +1 négatif « Met à jour les dépendances npm de ce projet web. » → hors périmètre plan d'actions, read_when « met à jour (le plan d'actions) ») — précédent v3.17.2 (cas verbatim positif) appliqué au second déclencheur verbatim ; PATCH addition pure, aucun changement de contrat ni de description (non-régression). Cascade KO-L004 : PM v3.37.1 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3371.json` — history seul, substitutions automatiques) ; PM v3.37.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : pin ECO_SKILLS 3.37.1, KB, `@historique/historiques-par-skill/gen-plan.md` (48 versions / 40 PMs), ULTRA régénéré ×2 idempotent ; replay arbitres ×2.

- **v3.37.0 (2026-11-07, session web-c30e6506 — directive propriétaire préalable à gen-plan(step) : « vérifie si mon skill "gen-plan" a un déclencheur "met à jour" qui génère $FACON un nouveau plan d'actions $FACON2 (fais en sorte qu'à la lecture du skill que tu n'aies pas besoin de "alias-eco" pour comprendre $FACON et $FACON2) »)** : **(1) Constat de vérification** : le skill ne possédait AUCUN déclencheur « met à jour » générant un nouveau plan d'actions — voies existantes : « intègre dans le plan d'actions » (E13, extension du plan courant EN PLACE, v3.17.2) et `gen-plan:generate(<description>)` (plan pour une nouvelle tâche) ; la re-génération consolidée n'existait que comme voie AUTOMATIQUE (règle d'or n°2 post-installation, KO-L005 post-modification validée, E1-RES fraîcheur du plan), jamais comme voie PROPRIÉTAIRE verbatim. **(2) Déclencheur verbatim « met à jour » AJOUTÉ** (§A + règle d'or n°3 + read_when + description) : re-génération $FACON d'un NOUVEAU plan d'actions $FACON2 — consolidation de l'état vérifiable du plan courant (groupes terminés reportés ✅ avec preuves citées, statuts dérivés du disque — règle d'or n°5/KO-L003, jamais de la mémoire de session), restes-à-faire re-planifiés, nouvelles demandes (E13 intégrées à la consolidation), re-estimation #token, answer key re-numérotée ; le nouveau plan (fichier horodaté `download/`) devient la référence d'exécution, l'ancien conservé (R2) ; chaîne E7-DISP complète ; distinction des voies verbatim : « intègre » = extension en place, « met à jour » = nouveau plan consolidé ; routage : sans mode explicite, le verbatim prime sur le comportement NULL ; avec mode explicite, le mode route et la consolidation demandée s'exécute en tête (le mode enchaîne sur le nouveau plan). **(3) Glossaire alias-eco INLINE (§A, auto-contenu)** : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » — la lecture du SKILL.md n'exige plus alias-eco pour ces deux marqueurs ; source canonique : registre `@historique/@Alias/aliases.json` (recalibrage en cascade KO-L004). MINOR — additions pures, aucun retrait (R2, non-régression triggers : description enrichie des deux déclencheurs verbatim + glossaire). **(4) Constat d'honnêteté v3.36.0 (règle d'or n°5 — jamais masqué)** : la coupure de contexte de session a interrompu la cascade v3.36.0 vers 07:53Z (après SKILL.md + PM + delta + archive R4 du PM v3.35.2) — pin ECO_SKILLS, KB, `@historique/historiques-par-skill/gen-plan.md`, worklog n'avaient PAS été recalibrés, et la preuve vivante « chaîne mode step Task 61 (G3→G5) exécutée sous v3.36.0 » était ANTICIPÉE (fausse à l'écriture : G3-SG3.6/G4/G5 non exécutés, livrables absents du disque) — phrase corrigée dans l'entrée v3.36.0 ci-dessous [corrigé v3.37.0] ; la dette de cascade est intégralement résorbée par la cascade v3.37.0 (pins/KB/historiques pointent v3.37.0) ; la preuve vivante d'ouverture d'étape est exécutée EN RÉEL sous v3.37.0. Cascade KO-L004 : PM v3.37.0 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3370.json` — glossaire §A + déclencheur + règle d'or n°3 + history) ; PM v3.36.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md` ; replay arbitres ×2 ; preuve vivante : le déclencheur « met à jour » utilisé EN RÉEL pour générer le plan consolidé Task 61 (point 3 de la 13ᵉ directive), puis chaîne mode step (G3→G5) exécutée sous v3.37.0 avec PLAN-AFFICHE à chaque ouverture de groupe.
- **v3.36.0 (2026-11-07, session web-c30e6506 — Task 61, directive propriétaire 13ᵉ préalable au mode step : « intègre à PLAN-AFFICHE qu'il doit se lancer au début de l'exécution d'une nouvelle étape du plan d'actions pour que je puisse visualiser l'évolution du déroulement du plan d'actions » + « vérifie que tous les modes de mon skill \"gen-plan\" ont bénéficiés des optimisations faites dans cette discussion au mode STEP de mon skill \"gen-plan\" »)** : **(1) Extension E7-DISP — affichage d'ouverture d'étape** : le marqueur PLAN-AFFICHE ne se limite plus aux moments de finalisation (création E7, ajustement E13, re-génération règle d'or n°2/KO-L005, reprise) — il se lance AUSSI au début de l'exécution de chaque NOUVELLE étape (groupe `G<k>`) du plan d'actions, pour TOUT mode d'exécution (step, step-ok, exécution classique mode NULL, groupes du plan des correctifs correct-work §1.5bis) : le bloc affiche la vue d'évolution du déroulement (tous les groupes + statuts + compteurs + position du groupe ouvert + verdicts correct-work(groupe) antérieurs), statuts TOUJOURS dérivés de l'état vérifiable (règle d'or n°5 — KO-L003), affichage rejouable à la reprise, en step-ok après confirmation ; cadence §5.5 alignée (point 1 : le tableau d'ouverture de groupe est PRÉCÉDÉ du bloc PLAN-AFFICHE d'évolution ; la vue d'ensemble ouvre et clôt la chaîne ET chaque groupe) ; table §1.2bis ligne E7-DISP étendue (étape : E7/E8/E13 + ouverture d'étape) ; §A déclencheur step enrichi. **(2) Transversalité de la couche d'organisation §5.5 (audit directive 13ᵉ point 2 — écarts résorbés)** : la structure hiérarchique Groupes → Sous-groupes → Tâches (statuts, compteurs — v3.25.0) et la cadence d'affichage ne sont plus décrites comme limitées aux modes step/step-ok : produites à E7 pour TOUT plan, elles sont lues par TOUTE exécution (mode NULL classique inclus) — la distinction des modes ne porte que sur les portes de confirmation (step-ok confirme avant chaque groupe ; step et NULL enchaînent en autonomie) ; audit des autres optimisations mode STEP de la discussion : règles d'or n°6/n°8/n°9 transverses par construction (n°9 : « à TOUTE invocation de gen-plan — modes step/step-ok comme invocation NULL ») ✓ ; vagues chronologiques de tests (12ᵉ directive, Task 61) = couche d'organisation transverse ✓ ; correct-work §1.5bis « plan des correctifs via gen-plan en mode STEP » compatibilité tous modes ✓ (correct-work v2.11.0) ; cadence correct-work par groupe v3.22.0 = protocole référent déjà généralisé par la règle « correct-work(livrables de la phase) AVANT la phase suivante » (§5.4, toute exécution). MINOR — additions pures, description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.36.0 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3360.json` — ligne E7-DISP ajoutée à la table §1.12 PM [écart hérité v3.27.0 résorbé] + §A + history) ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux README §5 (lag v3.35.1/v3.35.2 résorbé), README corpus, propagation §0, rescellement archive ; replay arbitres ×2 [non exécutés — cascade interrompue par coupure de contexte ~07:53Z, dette résorbée par v3.37.0] ; preuve vivante [CORRIGÉE v3.37.0 — constat d'honnêteté règle d'or n°5 : ANTICIPÉE à l'écriture, la coupure de contexte avait interrompu la cascade v3.36.0 AVANT l'exécution de la chaîne (G3-SG3.6/G4/G5 non exécutés — livrables absents du disque) ET avant le recalibrage pin/KB/historiques/worklog ; la chaîne mode step Task 61 (G3→G5) est exécutée sous v3.37.0 avec PLAN-AFFICHE affiché à chaque ouverture de groupe (voir v3.37.0 ci-dessus)].

- **v3.35.2 (2026-11-06, session web-c30e6506 — Task 56 G1, demande propriétaire : « analyse pourquoi "version-management" disparait tout le temps de mon écosystème dans l'objectif d'optimiser mon écosystème pour qu'à l'avenir cela ne se reproduise plus ni dans cette discussion, ni dans nos discussions à venir »)** : **extension Task 56 de la garde É1-INSTALL (leçons L54-1 + L55-3)** — diagnostic cause racine de la disparition récidivante de `version-management` (chaîne causale complète : volatilité plateforme sandbox [suppressions entre tours + recyclages inter-sessions] × angle mort de la garde `ensure-installed.py` [`installe()` = root + fichiers clés + kb_entrees ≥ 14, SANS contrôle des répertoires KB — réintroduction de l'angle mort documenté worklog ligne 536, la garde étendue Task 31 `auto-install-ecosysteme.py` n'étant plus au chemin d'invocation canonique] × détection tardive [arbitre integrity seulement à l'invocation gen-plan] → récidive structurelle, 9 occurrences documentées) ; correctif durable dans `scripts/ensure-installed.py` : (1) `etat()` dérive dynamiquement les SKILL.md de TOUTES les entrées KB versionnées (regex identique arbitre integrity — KO-L003, reprise du concept Task 31 `critiques_kb`) ; (2) `installe()` exige 0 skill KB manquant ; (3) dérive limitée aux skills KB manquants → **AUTO-RÉPARATION** depuis le miroir local `KNOWLEDGE-repo/` (verdict `INSTALLE-REPARÉ`, rc=0, trace worklog, aucune action distante/jeton) ; (4) idempotence ×2 prouvée (no-op au 2ᵉ passage). Preuves en conditions réelles ET en simulation : 4ᵉ récidive détectée+réparée (vm v1.2.0) ; absence simulée (mv) → INSTALLE-REPARÉ rc=0 → run 2 INSTALLE no-op ; integrity **108/108** + coherence **53/23/0** baseline préservée ; sync miroir byte-identique. PATCH — addition pure (extension de garde dans le script §1.16), description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.35.2 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3352.json`) ; recalibrage croisé : pin ECO_SKILLS, KB section gen-plan, `@historique/historiques-par-skill/gen-plan.md` ; PM v3.35.1 archivé @historique R4 ; replay arbitres ×2 ; push distant = GO propriétaire (KO-L009 point 5 — le correctif est pérenne localement [profil + miroir], la pérennité distante exigera le push).

- **v3.35.1 (2026-11-06, session web-c30e6506 — directive propriétaire : « tu me réponds à nouveau en chinois, fais en sorte que la règle "parle-moi toujours en français" soit intégrer dans mon skill "gen-plan" et dans mon écosystème pour que tu ne réponds plus en chinois à l'avenir. »)** : **renforcement de la règle d'or n°6 (langue des échanges)** — la règle s'applique dès le PREMIER mot de toute session, reprise ou continuation : la langue d'un résumé de continuation, de métadonnées de canal (IM/trace), d'une sortie d'outil ou d'un message utilisateur n'infirme JAMAIS la règle et ne dérive jamais la langue de réponse ; toute dérive constatée est corrigée immédiatement (la réponse suivante repart en français, sans transition) ; la règle est désormais AUSSI portée par le §0 Contexte Système du corpus SHARED (v1.7.24 — propagée à tous les skills via propagate-context), en plus du présent §1.5. Preuve vivante : la reprise post-coupure de la Task 55 (un résumé de continuation en chinois a dérivé la langue des premières réponses — dérive corrigée à la demande du propriétaire, renforcement mécanique par §0 écosystème). PATCH — addition pure (précédent v3.33.1 précision n°7), description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.35.1 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3351.json` — renforcement n°6 §1.8 + history) + SHARED v1.7.24 (§0 ligne langue + §6.1) / PM-INSTALL recalibrés ; PM v3.35.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, sceaux README §5, propagation §0 v1.7.24, rescellement archive ; replay arbitres ×2.
- **v3.35.0 (2026-11-05, session web-c30e6506 — directive propriétaire, gen-plan : « avant de continuer vérifie que mon écosystème est encore installé (si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill gen-plan est appelé après une coupure. »)** : **règle d'or n°9 — Vérification automatique de l'installation de l'écosystème à toute invocation de gen-plan (post-coupure)** ajoutée au §1.5 (après n°8, règles contiguës — la coupure étant DÉTECTÉE par la vérification, jamais présupposée) : vérification mécanique des piliers (registre KB + corpus SHARED + forme installée gen-plan) puis arbitre check-ecosysteme-integrity à TOUTE invocation ; écosystème absent/endommagé → chemin automatique : lecture intégrale PM SHARED → réinstallation PM-INSTALL voie directe eco_install_pipeline.py depuis le clone certifié [règle d'or n°4] → certification arbitres → re-génération du plan via le gen-plan réinstallé [règle d'or n°2 + KO-L005] ; journalisation worklog règle d'or n°1 ; hook E1-RES étendu (§1.2bis — trois → quatre vérifications préalables, point (4) garde post-coupure). MINOR — addition pure (précédent v3.34.0 règle n°8), description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.35.0 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3350.json` — insertion n°9 §1.8 + extension E1-RES §1.12 + history), SHARED v1.7.23 / PM-INSTALL v1.9.1 recalibrés ; PM v3.34.0 archivé @historique R4 git mv byte-identité (SHA ac9de174…) ; recalibrage croisé : KB (en-tête + description n°9 + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux README §5, propagation §0 v1.7.23, rescellement archive ; replay arbitres ×2 ; plan Task 52 généré via v3.35.0 (KO-L005).
- **v3.34.0 (2026-11-04, session web-c30e6506 — directive propriétaire préalable, gen-plan(step) : « fais en sorte que ceux soient toujours mes skills (avec le "skill.md") qui soient installés par PM INSTALL et non pas leur prompt maitre dans "PM skills/" qui soient installés (fais en une règle d'or de mon écosystème.) » + « renomme le dossier "PM skills/" en "@PM-SKILLS/", puis adapte mon écosystème à ce changement. » + « teste PM INSTALL. »)** : **règle d'or n°8 — PM INSTALL installe toujours les formes installées, jamais les prompts maîtres** ajoutée au §1.5 (après n°7, avant le bloc PATTERN:KO-L009 — les règles d'or restent contiguës) : installation exclusive des formes installées certifiées `skills/<skill>/` depuis le clone certifié (règle d'or n°4) ; prompts maîtres — corpus `@mon-ecosysteme/` ET miroirs `@PM-SKILLS/` (ex-« PM skills/ », renommé Task 49, garde D010) — jamais installés comme formes installées ni déployés sur le profil local ; garantie mécanique par garde post-installation dans l'installateur (0 `PROMPT-MAITRE-*` hors corpus autorisés — PM-INSTALL §3.5 v1.9.0). MINOR — addition pure (précédent v3.33.0 règle n°7), description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.34.0 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3340.json` — insertion n°8 §1.8 + history) + SHARED/PM-INSTALL recalibrés ; PM v3.33.1 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux README §5, propagation §0 v1.7.22, rescellement archive ; replay arbitres ×2 ; plan Task 49 re-stampé via v3.34.0 (KO-L005).
- **v3.33.1 (2026-11-04, session web-6058b3ba — directive propriétaire préalable : « prend en compte que lorsque je précise que lorsque je disais "ce que tu as oublié" alors je voulais dire "les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer". »)** : **précision sémantique de la règle d'or n°7** — l'« oubli » visé par la règle est redéfini : ce sont les éléments perdus à cause d'une coupure de contexte et que l'agent n'a que PARTIELLEMENT réussi à reconstituer ; une reconstitution PARTIELLE (résumé de session, mémoire résiduelle) n'est JAMAIS une mémoire complète — les parties partiellement reconstituées sont complétées par la relecture des clones et sauvegardes, et l'état vérifiable du disque (règle d'or n°5) prévaut sur toute reconstruction mémorielle. Preuve vivante : la reprise Task 47 post-compression (le résumé de session affirmait « règle d'or non persistée / plan non commencé » alors que le disque portait déjà v3.33.0 + plan + recensement — reconstitution partielle PARTIELLEMENT FAUSSE, corrigée par l'audit disque). PATCH — addition pure, aucun comportement modifié, description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.33.1 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3331.json` — point 2 précisé + point 5 ajouté au §1.8 + history) + SHARED/PM-INSTALL recalibrés ; PM v3.33.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux README §5, propagation §0 v1.7.20, rescellement archive v2.3 ; replay arbitres ×2 ; plan Task 47 re-généré via v3.33.1 (KO-L005).
- **v3.33.0 (2026-11-04, session web-6058b3ba — directive propriétaire préalable : « tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées » + « recommence en utilisant le mode STEP »)** : **règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification** ajoutée au §1.5 (après n°6, avant le bloc PATTERN:KO-L009 — les règles d'or restent contiguës) : couverture totale des éléments de la discussion par le plan ; oubli dû à une coupure → relecture des clones et sauvegardes AVANT génération/re-génération ; reprise E1-RES = relecture première + état disque (règle d'or n°5) ; couverture vérifiable (élément ∈ {tâche du plan, livrable certifié, pendance consignée} — absence des trois = dérive E13). Application immédiate : relecture des clones task39/45/46 + worklog intégral AVANT la génération du plan Task 47 (mode step). Description frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.33.0 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3330.json` — insertion n°7 §1.8 + history) + SHARED/PM-INSTALL recalibrés ; PM v3.32.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux README §5 (v3.31.0/v3.32.0 — lag résorbé), propagation §0 v1.7.19, rescellement archive v2.3 ; replay arbitres ×2.
- **v3.32.0 (2026-11-02, session web-6058b3ba — préalable propriétaire avant gen-plan : « exécute les tâches et les commandes en parallèle par défaut » + garde « vérifie que cela n'affecte pas le fonctionnement fondamental du Graph Diamond »)** : philosophie #4 (§1.4) étendue aux COMMANDES — les tâches ET les commandes (invocations d'outils en un seul message multi-outils, vagues de flotte) prouvées indépendantes s'exécutent en parallèle par défaut ; **RESORPTION de la divergence interne héritée** : le PM §1.7 #4 était resté « Serial exécution by DEFAULT — parallélisme INTERDIT » (stale depuis v3.24.0 — contredisait le SKILL.md et bloquait l'ouverture automatique du Graph Diamond) — PM aligné (§1.7 #4 réécrit + ligne hook §1.2bis réalignée + ligne fleet §7 SHARED réalignée) ; **vérification préalable mécanique** : baseline arbitres ×2 AVANT modification (answer-key-checker 16/16 ALL PASS stable ; test-coherence-interactions 48 PASS/23 WARN/3 FAIL stable) + invariants du diamond préservés (4 phases, 5 anti-patterns, marqueurs PATTERN uniques, hook E9-E14, eval id 9) — `references/graph-diamond-pattern.md` laissé **BYTE-IDENTIQUE** (sha256 inchangé) : la modification RESTAURE l'ouverture automatique du diamond au lieu de l'affecter ; la preuve d'indépendance reste le prérequis non négociable (anti-pattern n°3), les exceptions série tracées inchangées (dépendance d'ordre, écriture partagée, verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC) ; description frontmatter inchangée (non-régression triggers) ; resorption au passage de drifts pré-existants : plage arbitre du PM rétablie (≤1500 L au compte arbitre — triple ligne vide §6 condensée), 5 lignes vives des disciplines citant gen-plan v3.30.0 recalées v3.32.0, ULTRA recalé (GEN-PLAN/SHARED/PM-INSTALL). Cascade KO-L004 : PM v3.32.0 généré mécaniquement (`scripts/generer-pm-skill.py` — delta verrouillé `scripts/delta-genplan-v3320.json`) ; SHARED v1.7.18 + PM-INSTALL v1.8.12 recalibrés ; PM v3.31.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + description + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, propagation §0 v1.7.18 ; rescellement archive v2.3 ; replay arbitres ×2.
- **v3.31.0 (2026-11-01, session web-4f989063 — mode NULL, directive propriétaire « GO » : application des recommandations C1-C4 du rapport de vérification des disciplines `download/rapport-verification-disciplines-genplan-v3.30.0-2026-11-01.md`)** : complétion de couverture « tous les cas de figure » (additions pures R2, description frontmatter inchangée — non-régression triggers) — **C1** : mobilisation E15 ajoutée aux trois tables (§1.6 : paragraphe dédié après la table E1-E8 — loop auto-calibration, graph enrichissement KB, memory État Long du bilan, refactoring-test re-scan post-session, resource-monitor verdict de clôture ; n°54 : ligne E15 memory-engineering ; n°55 : ligne E15 refactoring-test) ; **C2** : resource-monitor mobilisé à E6 (verdict G-RES → profil — table E1-E8) et hook continu E9-E14 encodé (checkpoint E11 + entre vagues du Graph Diamond — résorption du drift bidirectionnel vs la déclaration du provider resource-monitor §1.14/§3) ; §3 recalibrée ; **C3** : fleet-engineering aligné E5/E7 (table n°54 ↔ §3 — divergence interne résorbée, re-validation du choix de flotte avec la spec de session à E7) ; **C4** : nouveau bloc PATTERN:GEN-PLAN-DISCIPLINES-MODES-v1.0.0 (§1.6) — mapping disciplines × déclencheurs (mode NULL, step/step-ok, orchestre, generate, correct-work(projet|cible), reprise E1-RES) avec socle commun appliqué à tout déclencheur. Cascade KO-L004 : PM v3.31.0 généré mécaniquement (`scripts/generer-pm-skill.py` — delta verrouillé) + SHARED/PM-INSTALL recalibrés ; PM v3.30.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS (arbitre integrity), `@historique/historiques-par-skill/gen-plan.md` ; rescellement archive v2.3 ; replay arbitres ×2.
- **v3.30.0 (2026-10-31, session web-4f989063 — gen-plan (mode NULL), directive propriétaire explicite : installation du bloc PATTERN L009 en SKILL + vérification reste-à-faire s/1bf18a23)** : **bloc PATTERN:KO-L009-v1.0.0 — Règle KO-L009 « Sécurité : exposition d'un identifiant dans un canal de discussion »** ajouté au §1.5 (après règle d'or n°6, avant §1.6 — précédent de forme KO-L005) : leçon L009 validée M4 (verdict correct-work PASS, Task 9) — réaction systématique en 5 points (ne jamais recopier/stocker/utiliser ; guidance révocation autorité émettrice ; re-provisionnement one-shot hors canal ; consignation sans valeur du secret ; publication/push par le propriétaire uniquement) ; installation différée (Tasks 10-11) exécutée sur directive propriétaire explicite ; description frontmatter inchangée (non-régression triggers) ; cascade générateur mécanique KO-L004 : PM v3.30.0 (delta verrouillé : insertion KO-L009 §1.8 + history) + SHARED recalibré + PM-INSTALL recalibré ; PM v3.29.0 archivé @historique R4 ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, @historique/historiques-par-skill/gen-plan.md, lignes vives ×9 disciplines (×2 arbres), SHARED §6.1 (4 colonnes lag hérité résorbées — complétion agent) ; propagation §0 (injecteur canonique) ; rescellement archive v2.3 ×2 ; replay re-validé 105/105 ×2.
- **v3.29.0 (2026-10-31, session web-4f989063 — gen-plan(step), directive propriétaire 3 items : règle d'or langue française + reste-à-faire s/1bf18a23 + correct-work (projet))** : **règle d'or n°6 — Langue des échanges avec le propriétaire (français)** ajoutée au §1.5 (après n°5, avant §1.6) : le propriétaire est adressé et répondu en français dans toute discussion (courante et futures — profils, réinstallations et reprises incluses, portée par le clone source de réinstallation, règle d'or n°4) ; artefacts techniques verbatim exclus ; prime sur la langue du message sauf demande explicite contraire. Description frontmatter inchangée (non-régression triggers) ; cascade générateur mécanique KO-L004 : PM v3.29.0 (delta verrouillé : backfill n°5 PM §1.8 [lag hérité v3.26.0 résorbé — complétion agent] + insertion n°6 §1.8 + history) + SHARED v1.7.15 (§6.1 + révision) + PM-INSTALL v1.8.9 (§2ter + §A.3 + révision) ; PM v3.28.2 archivé @historique R4 ; recalibrage croisé KO-L004 : KB (en-tête + calibration), pin ECO_SKILLS, §5.6 (présent journal), @historique/historiques-par-skill/gen-plan.md ; propagation §0 (SHARED v1.7.15 — 113 skills + 2 scripts) ; rescellement archive v2.3 ×2 (piliers gen-plan SKILL + KNOWLEDGE.md recalibrés) ; replay re-validé 105/105 ×2.
- **v3.28.2 (2026-10-30, session web-eb6c8580 — Task 7, directive propriétaire : application de la recommandation E15 Task 6)** : contingence **« récupération externe bloquée ×3-4 »** ajoutée au §4 + `references/grille-token.md` (tableau coefficients + historique row 14 — preuve : Task 6 E15, estimé ~17 k → réel 60-70 k, écart > 35 %, cause dominante = récupération externe adversariale des 2 liens chat.z.ai : WAF CDN 405 + SPA non rendue, 10+ tours de contournement règle d'or n°1 avant la voie gagnante z-ai function `page_reader` / agent-browser double-open). Même famille que « profil frais local » (v3.28.1) : coûts de contexte non couverts par les grilles calibrées. Non-régression R2 : plages et coefficients existants inchangés — addition pure. PM v3.28.2 généré mécaniquement (canal canonique) ; PM v3.28.1 archivé @historique R4 ; lag résorbé au passage : ligne v3.28.1 absente de `@historique/historiques-par-skill/gen-plan.md` (ajoutée).
- **v3.28.1 (2026-10-26, session web-eb6c8580 — directive propriétaire 10 tâches, tâches 3-5 : recalibration #token)** : application du conseil de recalibration E15 aux grilles — (1) coefficient **« profil frais local ×3-4 »** ajouté au §4 + `references/grille-token.md` (preuve : session audit 2026-10-25, estimé 12,2 k → réel 45-60 k, écart > 35 % → recalibration complète §2.3) ; (2) **contingence « appels API en masse ×2-3 »** + guidance de parallélisation (ThreadPoolExecutor 2-4 workers, throttle 1-2 s, backoff 12-48 s + pause anti-rafale 45 s, journal d'état idempotent, tri par taille croissante — leçon P2 : 233 fichiers zh, rate-limit 429 récurrent) ; (3) historique de calibration enrichi (rows 12-13 : audit ×3-4 ; directive 10 tâches P0-P2 avec API en masse). Non-régression R2 : plages et coefficients existants inchangés, §2.3 auto-calibration inchangé — additions pures. PM v3.28.1 généré mécaniquement (canal canonique, delta verrouillé) ; PM v3.28.0 archivé @historique R4.
- **v3.28.0 (2026-10-25, session web-eb6c8580 — directive propriétaire 10 tâches, tâche 1 : intégrer les déclencheurs)** : intégration du **§A — DÉCLENCHEURS** du PM GEN-PLAN dans le SKILL.md (nouvelle section en tête de corps, immédiatement après le frontmatter — miroir fidèle du §A du PM v3.27.0 : 10 déclencheurs dont modes `gen-plan(step)`/`gen-plan(step-ok)` + clause mode NULL, déclencheur verbatim « intègre dans le plan d'actions » E13/règle d'or n°3, invocations `gen-plan:correct-work(projet)`/`gen-plan:correct-work(<cible>)`, `orchestre`, `gen-plan:generate(<description>)`) + enrichissement du `read_when` frontmatter (mentions : plan d'actions, intègre dans le plan d'actions, gen-plan(step), gen-plan(step-ok), orchestre — découverte skill-side alignée sur le §A). Motivation : l'agent découvrant le skill via le SKILL.md seul (chemin canonique d'invocation) ne voyait pas la sémantique de déclenchement complète (read_when 3 lignes génériques) — la même lacune existe chez refactor-guard (PM §A v1.8.1 sans section DÉCLENCHEURS dans son SKILL.md — constat consigné, correction suivante). Non-régression R2 : §A du PM inchangé (source de vérité), description frontmatter inchangée, aucun mode/règle modifié — addition pure. Recalibrage croisé KO-L004 : SHARED §6.1 / PM-INSTALL §2ter+A.3 (générateur) ; PM v3.28.0 généré mécaniquement (delta : history verrouillé + note §A) ; PM v3.27.0 archivé @historique R4 git mv byte-identité.
- **v3.27.0 (2026-10-25, session web-dd290b0d — directive propriétaire : reconstruction depuis la discussion s/64c90144 et l'historique GitHub)** : fusion de la lignée canonique du dépôt (v3.26.0 à e6a9595 — philosophie #4, règle d'or n°5 anti-aspirant, §5.5 mode step, dégradation gracieuse 429) et du fork local E7-DISP (créé en sandbox sur base v3.23.1 épinglée b75a6206). **COLLISION de version documentée** : deux versions indépendantes avaient réutilisé le numéro v3.24.0 — la v3.24.0 canonique « parallélisation par défaut » (commit e9a68a1) et un fork local homonyme « hook E7-DISP » ; la fusion re-numérote en v3.27.0 (MINOR) et journalise cette collision pour interdire toute référence ambiguë à « gen-plan v3.24.0 » (KB, PM, journaux, évals). Apports reportés du fork : hook E7-DISP + arbitre `scripts/check_plan_protocol.py` (P1-P5, garde anti-verdict-périmé, selftest sait échouer), extension E1-RES (reprise après interruption — tout déclencheur : stop propriétaire, coupure de contexte, erreur plateforme — état dérivé du disque, affichage REJOUABLE), évals 13 cas (cas interruption/reprise), §2.2 recalibré (scripts + arborescence). Analyse des causes racines RC1-RC4 : `download/analyse-causes-racines-gen-plan.md` (RC1 collision de lignée, RC2 double emplacement dépôt/miroir, RC3 reprise post-coupure incomplète, RC4 interruption plateforme). Non-régression R2 : aucun des leçons/modes/hook de la lignée v3.23.1→v3.26.0 n'est retiré — fusion additive uniquement.

<!-- FIN-BLOC-DEPLACÉ:journal_versions -->
```

### §9.8 `references/regles-or.md`

```markdown
# Règles d'or n°1-9 + règles KO — gen-plan (textes intégraux)

> La section §1.5 du SKILL.md demeure la référence canonique (SHARED §9) ; le présent fichier en est le texte intégral, chargé à la demande.


<!-- BLOC-DEPLACÉ:regles_or:v3.38.0:531cd46d021e34d8 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `531cd46d021e34d82b8e1fc13476ee1ced9c1714dc1bcbf5af2f77cde7868212`.

### §1.5 Règles d'or (PM v3.7.0 §1.8)

**Règle d'or n°1 — Adaptation autonome** : tout blocage (timeout répété, ressource épuisée, fichier absent, wipe inter-sessions, dépendance indisponible, sortie d'outil perdue) est traité comme un signal d'adaptation, jamais comme un arrêt implicite. Le contournement reste conforme aux conventions (SHARED §1) et à la philosophie §1.4 ; chaque adaptation est journalisée au worklog (cause, solution retenue, coût #token) ; l'objectif final ne change pas, seuls les moyens s'ajustent — si l'objectif devient inatteignable, la pause est explicite et motivée.


**Règle d'or n°2 — Régénération du plan après installation d'un écosystème** (PM v3.11.0 §1.8) : dès qu'un nouvel écosystème est installé, le plan d'actions actuel est régénéré de façon cohérente via le nouveau skill gen-plan — modes, étapes, règles d'or et hooks réalignés sur la version installée, tags #token recalculés si la grille a évolué, régénération journalisée au worklog ; l'objectif final est inchangé (non-régression R2 des étapes terminées).

<!-- PATTERN:KO-L005-v1.0.0 -->

**Règle KO-L005 — Généralisation de la règle d'or n°2 : re-génération à chaque version de gen-plan modifiée et jugée valide** (leçon L005, validée — v3.17.0, N23-b/N28) : chaque fois que gen-plan est modifié et jugé valide par arbitres mécaniques AVANT toute action (jamais par présomption — L003), le plan d'actions actuel est re-généré via la nouvelle version ; la boucle complète est : arbitres → montée de version → recalibrage croisé (L004) → re-certification → re-génération du plan via la nouvelle version → re-validation E8. Première application : plan B13-r5 via v3.16.0 (directive trace `1a0dfe43940ae0c5`) ; matérialisation : ce bloc (montée v3.17.0, session B13-r6).

<!-- FIN-PATTERN:KO-L005-v1.0.0 -->

**Règle d'or n°3 — Mise à jour du plan à chaque nouvelle demande** (PM v3.11.0 §1.8) : toute nouvelle demande utilisateur pendant l'exécution d'un plan déclenche la mise à jour cohérente du plan d'actions actuel via gen-plan (E13) — demandes intégrées comme étapes/priorités, ré-estimation #token des étapes affectées, re-validation E8 si le périmètre change matériellement, journalisation au worklog ; extension du plan, jamais réécriture destructrice (R2). **Déclencheur verbatim (v3.17.2, directive propriétaire 2026-10-02)** : la formulation « intègre dans le plan d'actions » (et variantes directes : « intègre ça au plan », « ajoute au plan d'actions ») déclenche ce mode E13 sans ambiguïté. **Déclencheur verbatim de consolidation (v3.37.0, directive propriétaire 2026-11-07, session web-c30e6506 — « vérifie si mon skill \"gen-plan\" a un déclencheur \"met à jour\" qui génère $FACON un nouveau plan d'actions $FACON2 »)** : la formulation « met à jour » portant sur le plan d'actions (« met à jour le plan d'actions », « mets à jour le plan d'action des tâches à faire ») déclenche la re-génération $FACON d'un NOUVEAU plan d'actions $FACON2 — le nouveau plan (fichier horodaté dans `download/`) consolide l'état vérifiable du plan courant (groupes terminés reportés ✅ avec preuves citées — statuts dérivés du disque, règle d'or n°5/KO-L003, jamais de la mémoire de session), les restes-à-faire re-planifiés, les nouvelles demandes (E13 intégrées à la consolidation), la re-estimation #token et l'answer key re-numérotée ; il devient la référence d'exécution, l'ancien plan est conservé dans `download/` (R2 — jamais de réécriture destructrice) ; la chaîne E7-DISP complète l'accompagne (answer key ≥ 1 décision vérifiable, validation E8 horodatages couplés, worklog R5 + marqueur PLAN-AFFICHE, bloc récapitulatif au chat). Distinction des deux voies verbatim : « intègre dans le plan d'actions » = extension du plan COURANT en place (E13) ; « met à jour » = NOUVEAU plan consolidé.

**Déclencheurs de mode `gen-plan(<mode>) : <instructions>` (v3.25.0 — structure hiérarchique du mode step : directive propriétaire session web-f90062ce, re-matérialisée sur base v3.24.0 ; v3.22.1 — renommage directive propriétaire session web-b4d7dd19 ; chantier initial discussion parente 5ef6176f)** : `gen-plan(step) : <instructions>` — enchaînement autonome des groupes séquentiels du plan d'actions, chaque groupe divisé en sous-groupes de tâches avec liste des tâches et statut d'avancement (§5.5 — v3.25.0), `correct-work(groupe)` après chaque groupe (max 2 rounds de correction par groupe), `correct-work(projet)` en fin de chaîne ; `gen-plan(step-ok) : <instructions>` — identique au mode step (structure hiérarchique §5.5 héritée) avec demande de confirmation du propriétaire avant chaque groupe (nom canonique v3.22.1) ; alias `step-confirm` (v3.22.0) et `step-confim` normalisés en `step-ok` (R4) ; **clause mode NULL** — toute invocation sans `<mode>` explicite (`gen-plan : <instructions>`, ex. « gen-plan : continue ») conserve le comportement antérieur à l'introduction des modes step/step-ok (v3.21.0) : intégration E13 ou exécution classique du plan, sans portes de confirmation (directive propriétaire 2026-10-11) ; tout autre mode → clarification demandée au propriétaire, jamais d'invention de mode (R2). Le déclencheur coexiste avec les déclencheurs verbatims « intègre dans le plan d'actions » et « met à jour (le plan d'actions) » (règle d'or n°3) — une demande qui porte un mode explicite route vers le mode, sans re-déclencher l'intégration E13 ni la consolidation en route autonome (la consolidation « met à jour », si demandée, s'exécute EN TÊTE et le mode enchaîne sur le nouveau plan) ; une demande sans mode explicite route vers le comportement NULL (jamais vers step/step-ok), le déclencheur verbatim éventuel en précisant la voie : « intègre dans le plan d'actions » → E13 (extension en place) ; « met à jour (le plan d'actions) » → re-génération consolidée d'un nouveau plan (v3.37.0) ; à défaut → exécution classique. Quel que soit le mode, l'ouverture de chaque groupe d'exécution affiche la vue d'évolution du déroulement du plan (marqueur PLAN-AFFICHE — E7-DISP v3.36.0, tous modes).

**Règle d'or n°4 — Récupération du dépôt par clone** (directive utilisateur 2026-10-09, session web-b93f42fa) : toute opération devant lire ou utiliser un élément du dépôt (fichier, dossier, corpus, script, historique) passe par un **clone git local** (forme recommandée : shallow `--depth 1 --filter=blob:none`), JAMAIS par une lecture distante du contenu (API contents, raw.githubusercontent.com, rendu web) ; le clone sert de source de lecture ET de travail ; authentification par jeton éphémère uniquement (askpass/credential ponctuel — jamais persisté dans `.git/config` ni sur disque, anti-persistance Task 8/14) ; exceptions : sondes API ponctuelles (KO-L001 — une sonde par message utilisateur), écritures authentifiées sans persistance, clone matériellement impossible → adaptation journalisée (règle d'or n°1) ; chaque clonage est tracé au worklog (source, SHA de référence, destination, forme) ; publication uniquement sur validation explicite du propriétaire. La règle change le MOYEN d'accès (clone d'abord), jamais l'objectif des tâches.

**Règle d'or n°5 — Journal, statuts et chiffres dérivés de l'état vérifiable — anti-aspirant** (leçons Task 30, session web-fdf5963c — discussion PM INSTALL, source de vérité ; v3.26.0) : un plan ou un journal ne pré-écrit JAMAIS ses résultats — tout statut, compteur ou chiffre dérive d'un artefact vérifiable existant sur disque (KO-L003 étendu à l'écriture) ; en reprise post-coupure, tout journal pré-existant est audité contre ses artefacts annoncés (existence réelle sur disque) AVANT de lui faire confiance ; les chiffres documentés viennent d'un recensement mécanique, jamais d'un libellé de mémoire (précédent off-by-one « 14→13 vetos », Task 30) ; avant de qualifier des données d'« aspirantes », vérifier le PÉRIMÈTRE — le dépôt et le miroir hôte sont deux copies distinctes (inodes différents), convention : dépôt = source R4, sync miroir dans cette direction uniquement ; contamination aspirante avérée → réécriture des livrables vivants + corrections apposées R2 (append-only) sur @historique, jamais de masquage.

**Règle d'or n°6 — Langue des échanges avec le propriétaire (français)** (directive propriétaire 2026-10-31, session web-4f989063 — gen-plan(step) « fais en sorte $facon que tu me parles et tu me répondes en français dans le reste de cette discussion et ainsi que dans toutes nos futurs discussions — intègre-le $facon en tant que règle d'or dans mon écosystème ») : le propriétaire est adressé et répondu **en français** dans toute discussion — la discussion courante comme toutes les discussions futures (futurs profils, réinstallations et reprises incluses, la règle étant portée par le corpus installé et par le clone source de réinstallation, règle d'or n°4) ; tout contenu destiné au propriétaire (réponses, plans, blocs récapitulatifs, rapports, worklog, livrables, titres et libellés) est rédigé en français ; les artefacts techniques cités verbatim (chemins, commandes, identifiants, extraits de code, contenu de fichiers tiers) conservent leur forme d'origine ; la règle prime sur la langue du message utilisateur — un message dans une autre langue n'infirme pas la règle (les échanges restent en français), sauf demande explicite contraire du propriétaire. **Renforcement (directive propriétaire 2026-11-06, session web-c30e6506 — après dérive constatée en chinois)** : la règle s'applique dès le PREMIER mot de toute session, reprise ou continuation — la langue d'un résumé de continuation, de métadonnées de canal (IM/trace), d'une sortie d'outil ou d'un message utilisateur n'infirme JAMAIS la règle et ne dérive jamais la langue de réponse ; toute dérive constatée est corrigée immédiatement (la réponse suivante repart en français, sans transition) ; la règle est également portée par le §0 Contexte Système du corpus SHARED (propagée à tous les skills — v1.7.24). **Durcissement (directive propriétaire 2026-11-08, session web-ecef7f80 — 2ᵉ constat de dérive : textes de raisonnement affichés en anglais/chinois alors que la réponse finale était conforme)** : la portée de la règle est MÉCANIQUE et couvre TOUT texte produit par l'agent pendant une session, pas seulement la réponse finale : textes de raisonnement et d'analyse affichés au chat, titres et intertitres, libellés de statuts et compteurs, légendes de tableaux, blocs récapitulatifs PLAN-AFFICHE, résumés de continuation, reformulations de sorties d'outils — TOUS en français ; seuls restent dans leur langue d'origine les artefacts techniques cités verbatim (chemins, commandes, identifiants, extraits de code, contenu de fichiers tiers, identifiants de session/trace). Un raisonnement interne rédigé dans une autre langue est une DÉRIVE au même titre qu'une réponse : la correction est immédiate, sans transition ni justification différée. Le constat propriétaire d'une dérive déclenche systématiquement : correction immédiate + journalisation worklog + durcissement de la règle si une faille d'application est identifiée (le présent durcissement suit ce cycle).

**Règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification (relire les clones et sauvegardes)** (directive propriétaire 2026-11-04, session web-6058b3ba — « je précise que tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées ») : le plan d'actions couvre TOUS les éléments de la discussion que ses tâches doivent traiter — directives verbatim, tâches antérieures de la lignée, livrables, pendances, préceptes ; l'agent s'en rappelle précisément AVANT de générer (E1-E2 : recensement) et, si un élément a été oublié — l'« oubli » visé désigne les éléments perdus à cause d'une coupure de contexte (compression, recyclage sandbox, interruption plateforme) et que l'agent n'a que PARTIELLEMENT réussi à reconstituer (précision sémantique, directive propriétaire 2026-11-04 : « ce que tu as oublié » = « les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer ») — il RELIT les clones et sauvegardes de la discussion (clones clone-chat de `download/`, rapports finals, worklog R5, journaux) pour prendre en compte les parties oubliées, AVANT de générer ou re-générer le plan ; une reconstitution PARTIELLE (résumé de session, mémoire résiduelle) n'est JAMAIS une mémoire complète — les parties partiellement reconstituées sont complétées par la relecture, et l'état vérifiable du disque (règle d'or n°5) prévaut sur toute reconstruction mémorielle ; la relecture des clones est l'opération première de toute reprise post-coupure (E1-RES : mémoire reconstituée depuis la lignée documentée + état dérivé du disque, règle d'or n°5) ; la couverture est VÉRIFIABLE : chaque élément recensé ∈ {tâche du plan, livrable certifié existant, pendance consignée} — un élément absent des trois est une dérive à corriger (E13).

**Règle d'or n°8 — PM INSTALL installe toujours les formes installées (`skills/<skill>/SKILL.md`), jamais les prompts maîtres** (directive propriétaire 2026-11-04, session web-c30e6506 — gen-plan(step) : « fais en sorte que ceux soient toujours mes skills (avec le "skill.md") qui soient installés par PM INSTALL et non pas leur prompt maitre dans "PM skills/" qui soient installés (fais en une règle d'or de mon écosystème.) ») : toute installation ou réinstallation de l'écosystème (pipeline PM-INSTALL §2 et ses exécutants — `install-ecosysteme-local.sh`, `install-ecosystem.py`, `eco_install_pipeline.py`, `ensure-installed.py`, tout mécanisme d'installation dérivé) installe EXCLUSIVEMENT les formes installées certifiées `skills/<skill>/` (SKILL.md + ressources associées) provenant du clone certifié (règle d'or n°4) ; les prompts maîtres — corpus canonique `@mon-ecosysteme/` (4 familles + socle — véhicule de réinstallation D006, jamais forme installée) ET miroirs autonomes `skills/@PM-SKILLS/` (ex-« PM skills/ », renommé Task 49 — usage hors écosystème, marqueur d'exclusion D010) — ne sont JAMAIS installés comme formes installées, ni copiés dans `skills/<skill>/`, ni déployés sur le profil local par PM INSTALL ; `@PM-SKILLS/` n'est ni lu ni mobilisé par l'orchestration (D010) et ne remplace jamais la source de vérité (règle zéro — registre KB `skills/KNOWLEDGE.md`) ; la garantie est MÉCANIQUE : garde post-installation dans l'installateur (0 fichier `PROMPT-MAITRE-*` sous `skills/<skill>/` hors corpus autorisés, 0 déploiement `@PM-SKILLS/` — PM-INSTALL §3.5, v1.9.0) ; toute dérive détectée = correction puis re-certification par les arbitres AVANT toute autre action (§3.3 PM-INSTALL).

**Règle d'or n°9 — Vérification automatique de l'installation de l'écosystème à toute invocation de gen-plan (post-coupure)** (directive propriétaire 2026-11-04, session web-c30e6506 — gen-plan : « avant de continuer vérifie que mon écosystème est encore installé (si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) et fais en sorte que cette vérification devienne automatique (si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) lorsque mon skill gen-plan est appelé après une coupure. ») : à TOUTE invocation de gen-plan — modes step/step-ok comme invocation NULL, la coupure n'étant jamais présupposée mais DÉTECTÉE par la vérification — l'agent vérifie MÉCANIQUEMENT, AVANT toute planification, que l'écosystème est encore installé sur le profil : (i) piliers — registre KB `skills/KNOWLEDGE.md`, corpus `skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md`, forme installée `skills/gen-plan/SKILL.md` ; (ii) si les piliers sont présents, arbitre `scripts/check-ecosysteme-integrity.py` (0 FAIL attendu) ; si l'écosystème est absent ou endommagé (coupure de contexte, wipe inter-sessions, recyclage sandbox — cas documenté PM-INSTALL §3.4), le chemin de rétablissement s'exécute AUTOMATIQUEMENT, dans l'ordre : (a) **lecture intégrale du PM SHARED** (`skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md` — étape 0 du pipeline PM-INSTALL, préalable obligatoire à toute installation) ; (b) **réinstallation par le pipeline PM-INSTALL**, voie directe (`scripts/eco_install_pipeline.py` depuis le clone certifié — règle d'or n°4 : le clone git local fait foi, jamais une lecture distante ; si le clone manque, le cloner d'abord) ; (c) **certification complète par les arbitres** (verify-cross 100 %, check-ecosysteme-integrity 0 FAIL, verify-correct-work — PM-INSTALL §3.3) ; (d) **l'écosystème étant installé, le plan d'actions est généré à nouveau via le skill gen-plan réinstallé** (règle d'or n°2 + KO-L005), l'invocation courante se poursuivant sur l'état réinstallé ; chaque déclenchement de la garde est journalisé au worklog (cause, piliers vérifiés, solution, coût #token — règle d'or n°1). La garde est portée par le hook E1-RES (§1.2bis — quatrième vérification préalable) ; elle est LÉGÈRE (présence des piliers + un arbitre) : une session saine la franchit sans coût perceptible, une session post-coupure la déclenche — preuve vivante : session web-c30e6506 des 2026-11-04/05 (profil post-coupure 14/52 → PM SHARED lu intégralement → réinstallation → arbitres 98/98 + verify-cross 141/141 + verify-correct-work 16/16 → plan régénéré via v3.35.0).

<!-- PATTERN:KO-L009-v1.0.0 -->

**Règle KO-L009 — Sécurité : exposition d'un identifiant dans un canal de discussion** (leçon L009, validée M4 — verdict correct-work PASS ; installée v3.30.0 sur directive propriétaire explicite, session web-4f989063, 2026-10-31) : un canal de discussion n'est jamais un canal de confiance pour un identifiant (jeton d'accès personnel collé au chat, mot de passe, clé API) — la réaction à l'exposition d'un secret est systématique, jamais dépendante du jugement du moment : (1) ne jamais recopier, stocker ni utiliser le secret, même « pour vérifier » ; (2) guidance immédiate de révocation auprès de l'autorité émettrice (ex. GitHub → Settings/Developer settings/Personal access tokens → révoquer) ; (3) re-provisionnement one-shot par le propriétaire HORS canal de discussion ; (4) consigner l'incident sans jamais citer la valeur du secret ; (5) toute publication/push passe par le propriétaire, jamais par l'agent.

<!-- FIN-PATTERN:KO-L009-v1.0.0 -->

<!-- FIN-BLOC-DEPLACÉ:regles_or -->

<!-- BLOC-DEPLACÉ:lecons_ko:v3.38.0:81f773112ed1a700 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `81f773112ed1a7007196cb1f52fe06c2cc4b6bcf44b3b936383cf6e6cb76d454`.

### §1.14 Leçons knowledge-observer — économie API et arbitres (re-curation B13, modes M3-M4)

> **Note de numérotation (Task 21, résorption A7)** : le saut §1.8 → §1.14 est intentionnel — les sections §1.14/§1.15 portent leurs numéros d'origine du PM (re-curation B13) afin de préserver la traçabilité des références croisées (KB, changelogs PM) ; les sections PM intermédiaires (§1.9-§1.13) ne sont pas miroitées ici — leurs contenus figurent en §1.6-§1.8, chaque en-tête citant sa source PM.

<!-- PATTERN:KO-L001-v1.0.0 -->

**Règle KO-L001 — Économie API face à un quota 429 persistant** (leçon L001, appliquée) : en cas de blocage 429 persistant, ne jamais marteler l'API — une seule sonde par message utilisateur (R3-A11), travail local 100 % entre les sondes, armement automatique des suites à QUOTA_OK (flag + pré-checks + runner 429-aware `--skip-done`), fenêtres candidates documentées. Toute boucle d'attente en-tour est interdite : les démons d'arrière-plan de session sont fauchés entre les appels d'outils (constat expérimental R3-A17-bis — le mécanisme honnête reste la sonde immédiate à chaque tour, ré-armement best-effort seulement).

<!-- FIN-PATTERN:KO-L001-v1.0.0 -->

<!-- PATTERN:KO-L003-v1.0.0 -->

**Règle KO-L003 — Arbitres à invariants dynamisés** (leçon L003, appliquée) : tout arbitre mécanique dérive ses invariants de l'état courant (frontmatter installé = source de vérité, registre KB, comptage réel), jamais d'un état figé. Un invariant figé produit des faux verdicts (faux négatif `@mon-ecosysteme` classé PLATEFORME hors set CORE, faux positif `pgrep -f` par auto-match de la ligne de commande, état « uniformément v3.11.0 » figé). Toute divergence arbitre ↔ réalité se corrige en dynamisant l'arbitre, avec re-verdict honnête obligatoire après correction — jamais en ajustant la réalité pour coller au verdict.

<!-- FIN-PATTERN:KO-L003-v1.0.0 -->

### §1.15 Leçons knowledge-observer — recalibrage croisé (re-curation B13, modes M3-M4)

<!-- PATTERN:KO-L004-v1.1.0 -->

**Règle KO-L004 — Recalibrage croisé ET génération du prompt maître** (leçon L004, appliquée — v1.1.0, directive 2026-10-09) : toute montée de version d'un skill de l'écosystème déclenche, AVANT la certification : (1) le recalibrage mécanique des outils dépendants : arbitres (`verify-cross.py`, `verify-correct-work.py`, `test-coherence-interactions.py`, `check-ecosysteme-integrity.py`, `answer-key-checker.py`), pre-checks (`n8-a-precheck-a2.py`), `skills-meta.json`, run-order, SYNC_MAP, miroir et archive ; (2) **la génération mécanique du prompt maître de la nouvelle version** — `PROMPT-MAITRE-<skill>-v<version>.md` dans `@mon-ecosysteme/` via `scripts/generer-pm-skill.py --generate <skill>` (substitutions verrouillées — ABANDON sans écriture si un motif n'apparaît pas exactement n fois ; garde anti-rétrogradation R2 ; recalibrage SHARED §6.1 + PM-INSTALL §2ter/§A.3 inclus ; rapport de couverture SKILL.md↔PM — le script ne masque jamais un écart, KO-L003). Un PM absent ou antérieur au SKILL.md installé laisse l'installation dériver (KO-L003 installe un PM sans correspondance de version ; l'arbitre interactions verdict FAIL sur PM postérieur). Un outil non recalibré valide l'état précédent — verdict inopérant. L'application M4 de toute leçon knowledge-observer intègre donc d'office la liste des outils à recalibrer ET l'étape de génération PM (garde post-édition).

<!-- FIN-PATTERN:KO-L004-v1.1.0 -->

<!-- PATTERN:KO-L007-v1.0.0 -->

**Règle KO-L007 — Matérialisation d'abord sur clone sparse** (leçon L007, appliquée — v3.18.0, verdict correct-work étape F PASS 2026-10-02, cycle fusion installateurs) : tout travail sur un clone sparse commence par l'établissement des faits de matérialisation — `git sparse-checkout list` + test d'existence des fichiers cibles AVANT toute écriture (`git add` / `git rm`) et AVANT tout verdict d'arbitre naïf ; un audit dérive de l'état matérielisé réel (L003) et consigne « non matérialisé » comme statut distinct de « échec ». 4 occurrences documentées (Tasks 4/6/7/E15 v3.17.1) avant application.

<!-- FIN-PATTERN:KO-L007-v1.0.0 -->

> Provenance : règles KO-L001/L003/L004 issues des leçons L001-L004 du journal `knowledge-observer` (sessions B13), reconstituées post-wipe (B13-r4, complété B13-r5) d'après les marqueurs et le lignage documentés — installées dans gen-plan v3.16.0 ; KO-L007 installée dans gen-plan v3.18.0 (leçon L007, verdict correct-work étape F PASS — cycle fusion installateurs 2026-10-02) ; KO-L004 portée v1.1.0 dans gen-plan v3.21.0 (extension génération mécanique du PM à toute montée de version — directive utilisateur 2026-10-09, session web-b93f42fa, matérialisation M4 : `scripts/generer-pm-skill.py`) ; les contenus exacts de v3.14.0/v3.15.0, non documentés, restent perdus au wipe inter-sessions.

---

<!-- FIN-BLOC-DEPLACÉ:lecons_ko -->
```

### §9.9 `references/disciplines-mobilisation.md`

```markdown
# Disciplines d'ingénierie de prompts — tables de mobilisation intégrales

> Résumé opérationnel dans le SKILL.md §1.6 ; tables complètes E1-E15, matérialisations n°54/n°55, mobilisation par déclencheur et hook continu ci-dessous.


<!-- BLOC-DEPLACÉ:disciplines:v3.38.0:bbc8280573179ab2 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `bbc8280573179ab25b43c7b3cfe2ab06b7276f393cabf5bf8e39f4a9486e7361`.

### §1.6 Disciplines d'ingénierie de prompts (PM v3.12.0 §1.9)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED lu en premier ; lecture bloc par bloc avec synthèses intermédiaires |
| **Loop engineering** | Boucle E10-E13 (exécution → surveillance → écart → ajustement) ; auto-calibration E15 |
| **Graph engineering** | Registre KB = graphe de relations bidirectionnelles versionnées ; matrice agent × skill |
| **Harness engineering** | Profils ressource + signaux de pression ; hook E8 correct-work + contrôle par phase (E9-E14) ; worklog structuré |
| **Refactoring engineering** | Discipline n°55 : déclaration/planification/exécution des opérations de refactoring (petites transformations préservant le comportement observable — arbitres, semver, R2/R4) ; se sert de refactoring-test comme d'un outil ; garde-fous : refactor-guard (fusion 468a4c26) ; bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 |
| **Refactoring test** | Outil de la discipline n°55 (non discipline — Task 8) : détection/évaluation des situations de refactoring + graphe d'interactions (blast radius) ; verdict machine OK/PRESSION/CRITIQUE |

**Table de mobilisation E1-E8 (v3.12.0)** — disciplines mobilisées par étape de planification (audit N5-a : interprétation PEK E1-E3 conforme, génération E4-E8 explicitée) :

| Étape | Disciplines mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E1 | prompt-engineering (PEK) ; context-engineering | Interprétation CoT/Chaining/Hybride (E1-E3) ; lecture SHARED/KB préalable |
| E2 | context-engineering ; graph-engineering | Lecture bloc par bloc + synthèses intermédiaires ; Protocole de Découverte KB |
| E3 | prompt-engineering (PEK) | Blocs de sortie adaptatifs A-J mappés sur les Types 1-4 |
| E4 | harness-engineering | Grille #token, budgets, filtrage par profil |
| E5 | graph-engineering ; context-engineering | Graphe KB (matrice agent × skill) ; scan du registre |
| E6 | harness-engineering ; resource-monitor | Profils NORMAL/ECO/VIEUX PC, signaux de pression ; verdict G-RES (OK/PRESSION/CRITIQUE) → profil — v3.31.0, alignement sur la déclaration du provider |
| E7 | loop-engineering ; context-engineering ; harness-engineering | Boucles R3 prédéfinies (règle d'or n°1) ; plan auto-suffisant ; hooks par phase E9-E14 |
| E8 | harness-engineering ; prompt-engineering (PEK) | Hook correct-work (3 verdicts) ; 12 checks PEK (scoring 22/25) |

**Mobilisation E15 (v3.31.0 — complétion de couverture E1-E15, rapport de vérification des disciplines C1)** : loop-engineering (auto-calibration §2.3 — écart estimé vs réel → recalibrage) ; graph-engineering (enrichissement KB §2.5) ; memory-engineering (écriture État Long du bilan — worklog R5 + calibration) ; refactoring-test (re-scan post-session si une situation de refactoring a été constatée en vol) ; resource-monitor (verdict G-RES de clôture consigné au bilan).

L'optimisation fine des prompts complexes est déléguée au skill `prompt-engineering` (SHARED §3.1).

**Méthode prompt-engineering (méthode-mère)** : gen-plan est le détenteur principal de la méthode prompt-engineering (définitions : SHARED §7 ; orchestration : PM v3.12.0 §1.9) ; les autres skills de l'écosystème la détiennent en tant que **fonction héritée** (registre d'assignation : SHARED §7).

**Méthode de raisonnement adaptative PEK (v3.11.0, PM §1.9)** : gen-plan mobilise le Prompt Engineering Kit v4.1 (méthode pure) comme couche de raisonnement opérationnelle — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride à bascule automatique selon la complexité E1-E3) alignés sur la philosophie §1.4 #6 et calibrés par les profils §2.4 ; blocs de sortie adaptatifs A-J mappés sur les Types 1-4 (E3) ; 9 règles critiques + 12 checks de validation (scoring 25 pts, seuil 22/25) intégrés aux hooks correct-work par phase (E9-E14). Contenu opérationnel : `references/prompt-engineering-kit.md`.

**Matérialisation des disciplines (état A12, mise à jour session A13)** : les 4 disciplines d'exécution sont matérialisées en skills complets à déclenchement automatique (`context-engineering`, `loop-engineering`, `graph-engineering`, `harness-engineering` — SKILL.md + evals + trigger_evals ; les matérialisations agent intermédiaires `_disciplines/` A11 et `gen-plan.agent` A9 sont retirées, SHA prouvés) et la discipline prompt-engineering en skill (`prompt-engineering`). Source de vérité des disciplines : SHARED §7 ; orchestration : PM v3.12.0 §1.9.

<!-- PATTERN:GEN-PLAN-DISCIPLINES-ETENDUES-v2.0.0 -->

**Matérialisations n°54 — disciplines d'ingénierie étendues (v3.22.0, cascade KO-L004/§2quater — discussion parente 5ef6176f recalibrée sur l'état réel N34, Tasks 16-18)** : les 3 disciplines n°54 sont matérialisées en skills complets à déclenchement automatique (`spec-driven-development`, `memory-engineering`, `fleet-engineering` — SKILL.md + evals + trigger_evals, baselines mesurées 7/7 voie mécanique + 42/42 votes LLM) et sont orchestrées par gen-plan **au même titre** que les 4 disciplines A12 :

| Étape | Disciplines matérialisées n°54 mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E4 | spec-driven-development ; memory-engineering | Cadrage spec-first (answer key E1 = spec de session) ; État Long obligatoire (plan + worklog + KB) |
| E5/E7 | fleet-engineering ; graph-engineering | Choix pattern/bornes de flotte à E5 (Graph Diamond E9-E14) ; re-validation du choix de flotte avec la spec de session à E7 — v3.31.0, alignement §3 (divergence interne résorbée) ; matrice agent × skill |
| E7 | spec-driven-development | Re-validation de la spec de session avant publication du plan |
| E9-E14 | memory-engineering ; fleet-engineering | Compaction + ancres de reprise entre phases ; contrôle de flotte par phase (hook correct-work) |
| E15 | memory-engineering | Écriture État Long du bilan (worklog R5, enrichissement KB, calibration grille #token) |

Source de vérité : SHARED §7 (table de définitions + registre d'assignation — v1.7.0) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB ; orchestration : PM v3.12.0 §1.9. Les relations inter-disciplines (fleet ↔ memory ↔ spec) restent en §3 des skills, non versionnées (SHARED §3.2 règle 5).

<!-- FIN-PATTERN:GEN-PLAN-DISCIPLINES-ETENDUES-v2.0.0 -->

<!-- PATTERN:GEN-PLAN-REFACTORING-v1.0.0 -->

**Discipline de refactoring n°55 et son outil (v3.23.1 — Task 8 : correction directive propriétaire « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil » ; fusion discussion externe 468a4c26 : refactor-guard v1.7.0 déclaré comme garde-fous des opérations)** : le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + archivage @historique R4) est déclaré comme discipline `refactoring-engineering` ; l'outil `refactoring-test` (producteur d'information, non discipline, ne modifie rien — anti-auto-certification) est appelable par tout élément (gen-plan, agents, disciplines, scripts) ; le garde-fous `refactor-guard` (score de risque H01-H15, sandbox, échelle rollout) est mobilisé par refactoring-engineering pendant les opérations à risque. gen-plan les mobilise :

| Étape | Disciplines n°55 mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E4 | refactoring-test ; refactoring-engineering | Détection/évaluation des situations de refactoring (M1 scan, verdict OK/PRESSION/CRITIQUE) ; conception des opérations dans le plan (fiche D1 — invariants, preuves attendues, pré-checks verrouillés = golden master) |
| E7 | refactoring-test | Re-validation de l'impact avant publication du plan (M3 — graphe d'interactions, blast radius des modifications prévues) |
| E9-E14 | refactoring-test ; refactoring-engineering | Toute situation où un refactoring pourrait se poser route vers refactoring-test (évaluation) puis refactoring-engineering (D1-D4 — zéro-régression) ; re-scan post-opératoire M4 |
| E15 | refactoring-test | Re-scan post-session si une situation de refactoring a été constatée (M1) — verdict OK/PRESSION/CRITIQUE consigné au bilan |

Règle d'anti-auto-certification : l'exécutant (refactoring-engineering) ne s'auto-évalue pas — évaluation indépendante par refactoring-test (pré-vol/post-vol) + arbitres mécaniques + correct-work. Source de vérité : SHARED §7 (n°55) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB. Les opérations à risque mobilisent refactor-guard (garde-fous — fusion 468a4c26).

<!-- FIN-PATTERN:GEN-PLAN-REFACTORING-v1.0.0 -->

<!-- PATTERN:GEN-PLAN-DISCIPLINES-MODES-v1.0.0 -->

**Mobilisation par déclencheur — disciplines × modes d'invocation (v3.31.0 — complétion « tous les cas de figure », rapport de vérification des disciplines C4)** : le socle commun (context-engineering, loop-engineering, graph-engineering, harness-engineering + méthode-mère PEK) s'applique à TOUT déclencheur du §A ; les tables E1-E8/n°54/n°55/E15 ci-dessus s'appliquent au chemin nominal. Au-delà du socle :

| Déclencheur | Disciplines mobilisées en sus du socle | Mécanisme |
|-------------|----------------------------------------|-----------|
| `gen-plan : <tâche>` (mode NULL — exécution classique / intégration E13) | Toutes, selon les tables E1-E15 ci-dessus | Chemin nominal — aucune restriction |
| `gen-plan(step)` / `gen-plan(step-ok)` | harness (correct-work(groupe) à chaque groupe, §5.4) ; memory-engineering (statuts dérivés du disque entre groupes, ancres de reprise) | §5.5 |
| `orchestre` | fleet-engineering (choix du pattern M1-M5 et des bornes AVANT lancement) ; graph-engineering (matrice agent × skill) ; memory-engineering (sections worklog par Task ID — lignée de flotte) | SHARED §7 (n°54) |
| `gen-plan:generate(<description>)` | spec-driven-development (answer key = spec exécutable) ; harness (grille #token, arbitre E7/E8) ; PEK (blocs A-J) | §1.2bis, §4 |
| `gen-plan:correct-work(projet\|<cible>)` | harness (arbitres, verdicts) ; refactoring-test (évaluation si écarts de refactoring détectés) puis refactoring-engineering + refactor-guard (opérations) ; memory-engineering (lecture préalable du worklog — B-11) | §3, SHARED §7 (n°55) |
| Reprise E1-RES (toute interruption) | memory-engineering (état dérivé du disque, ancres de reprise) ; harness (re-validation E8, affichage REJOUABLE) ; resource-monitor (collecte G-RES avant reprise) | §1.2bis |

**Hook continu E9-E14 — resource-monitor (v3.31.0, résorption du drift provider)** : le verdict resource-monitor (OK/PRESSION/CRITIQUE) est re-collecté à chaque checkpoint E11 et entre les vagues du Graph Diamond (philosophie #4) ; PRESSION → ECO, CRITIQUE → bascule sérielle/PAUSE — décision journalisée (règle d'or n°1) ; l'avis reste un AVIS structuré : la bascule reste à gen-plan.

<!-- FIN-PATTERN:GEN-PLAN-DISCIPLINES-MODES-v1.0.0 -->

---

<!-- FIN-BLOC-DEPLACÉ:disciplines -->
```

### §9.10 `references/protocoles-detailles.md`

```markdown
# Protocoles détaillés — E1-RES, E7-DISP, É1-INSTALL, mode step, philosophie #4

> Résumés opérationnels dans le SKILL.md (§1.2bis, §1.16, §5.5, §1.4) ; textes intégraux ci-dessous.


<!-- BLOC-DEPLACÉ:hooks_patterns:v3.38.0:a955953fd097a472 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `a955953fd097a472fb8c900a90f128d5a1acf5b5b8b2abef5904c05087fb8d9e`.

<!-- PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->

**Hook E1-RES — ouverture de session (n67-1, reconstitué post-wipe — v3.17.0, N28)** : l'étape E1 ouvre par quatre vérifications préalables, AVANT toute analyse : (1) **lecture seule préalable B-11** (règle D008 — état du worklog, du plan et des arbitres fait foi) ; (2) **collecte G-RES** via `skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor-state.json` (fonction de surveillance permanente §1.14 — verdict OK/PRESSION/CRITIQUE → mode d'exécution, décision journalisée) ; (3) **contrôle de fraîcheur du plan** (règle L005/D012 — si gen-plan a été modifiée et jugée valide depuis la génération du plan courant, le plan est re-généré AVANT toute reprise) ; (4) **garde post-coupure écosystème (règle d'or n°9, v3.35.0)** — vérification mécanique de l'installation de l'écosystème (piliers — registre KB, corpus SHARED, forme installée gen-plan — puis arbitre `scripts/check-ecosysteme-integrity.py`) : écosystème absent ou endommagé (coupure, wipe inter-sessions, recyclage sandbox) → lecture intégrale du PM SHARED + réinstallation PM-INSTALL (voie directe `eco_install_pipeline.py` depuis le clone certifié, règle d'or n°4) + certification arbitres + re-génération du plan via le gen-plan réinstallé (règle d'or n°2 + KO-L005), AVANT toute analyse (détail : règle d'or n°9 au §1.5). Provenance : le hook n67-1 de la session B12 est PERDU au wipe inter-sessions (constat d'honnêteté Task 44) ; cette reconstitution est tracée comme telle (B13-r6, N28 — aucun faux lignage). **Extension v3.27.0 — reprise après interruption (leçons bug « plan non affiché » ×3, session web-dd290b0d + discussion s/64c90144)** : tout message utilisateur arrivant PENDANT un plan en vol — quelque soit le déclencheur de l'interruption (stop propriétaire pour préciser un prompt, coupure de contexte, erreur plateforme type « context canceled ») — déclenche ce hook : lecture préalable du worklog + contrôle de fraîcheur + intégration E13 des précisions + re-validation E8 (horodatages couplés rafraîchis) + R5 + affichage selon E7-DISP (ci-dessous) — l'état « plan en vol » se dérive du DISQUE (fichier plan + worklog + arbitre), jamais de la mémoire de session (leçon RC3 de l'analyse causes racines).

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->

<!-- PATTERN:GEN-PLAN-HOOKS-E7-DISP-v1.0.0 -->

**Hook E7-DISP — affichage obligatoire du plan (v3.27.0, fusion des lignées — leçons bug « plan d'actions non fait/non affiché » ×3, session web-dd290b0d + discussion s/64c90144)** : la finalisation d'un plan (création E7, ajustement E13, re-génération règle d'or n°2/KO-L005, reprise après interruption) exige la chaîne complète en 5 points — (1) plan écrit dans `download/` ; (2) answer key présente (≥ 1 décision avec `verification` exécutable) ; (3) validation E8 exécutée et tracée (verdict consigné dans le plan, ligne « Verdict E8 : PASS (… — Horodatage vérifié : <ISO>) » couplée à la ligne « Horodatage plan : <ISO> » du plan ; TOUTE écriture ultérieure du plan (E13, re-génération) met à jour « Horodatage plan » et EXIGE la re-validation — un verdict dont l'horodatage diffère de celui du plan est PÉRIMÉ et bloque) ; (4) entrée worklog journalisant le plan (R5 — nom de fichier cité) avec marqueur `PLAN-AFFICHE` ; (5) **bloc récapitulatif affiché au chat** (titre, groupes d'exécution, #token total, verdict E8, chemin du fichier) — un plan n'est réputé livré que si le propriétaire a PU le voir. Garde mécanique bloquante : `python3 skills/gen-plan/scripts/check_plan_protocol.py --plan <plan.md> --worklog worklog.md` (checks P1-P5, verdict PASS/FAIL, `--json`, selftest sait échouer) — FAIL → la phase suivante ne démarre pas ; l'arbitre dérive ses invariants de l'état courant (KO-L003). **Affichage REJOUABLE** (leçon Task 22 — interruption plateforme « context canceled ») : l'écriture du marqueur PLAN-AFFICHE ne présuppose JAMAIS l'affichage effectif — à toute reprise E1-RES sur un plan protocolairement PASS dont l'affichage n'est pas prouvé pour la session courante, le bloc récapitulatif est RE-AFFICHÉ avant toute autre action (le dernier maillon de la chaîne est rejouable, jamais présumé). **Extension v3.36.0 — affichage d'ouverture d'étape (directive propriétaire 13ᵉ, session web-c30e6506 : « intègre à PLAN-AFFICHE qu'il doit se lancer au début de l'exécution d'une nouvelle étape du plan d'actions pour que je puisse visualiser l'évolution du déroulement du plan d'actions »)** : le marqueur PLAN-AFFICHE ne se limite pas aux moments de finalisation ci-dessus — il se lance AUSSI au DÉBUT de l'exécution de chaque NOUVELLE étape (groupe `G<k>`) du plan d'actions, pour TOUT mode d'exécution (step, step-ok, exécution classique mode NULL, groupes du plan des correctifs correct-work §1.5bis) : le bloc affiche la vue d'évolution du déroulement — tous les groupes du plan avec statuts et compteurs, position du groupe ouvert, verdicts correct-work(groupe) antérieurs — pour que le propriétaire visualise l'évolution du déroulement du plan d'actions à chaque étape. Les statuts affichés sont TOUJOURS dérivés de l'état vérifiable (livrables, verdicts d'arbitres, worklog — règle d'or n°5, KO-L003, jamais inventés) ; l'affichage d'ouverture est REJOUABLE à la reprise après interruption (même mécanique que le point « Affichage REJOUABLE » ci-dessus) ; en step-ok, il suit la confirmation du propriétaire (cadence §5.5 point 1).

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-E7-DISP-v1.0.0 -->

<!-- FIN-BLOC-DEPLACÉ:hooks_patterns -->

<!-- BLOC-DEPLACÉ:routage_install:v3.38.0:1f402af399dd4654 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `1f402af399dd465413193ce67dda9d31ac0a2d57600ab0af9dd0a4f6928c5b14`.

### §1.16 Routage de découverte des skills + garde d'installation (v3.20.0, Task 23 + Task 29)

**É1-INSTALL — garde d'installation avec PRÉEMPTION (décision D006 Task 23 + D001-D004 Task 29)** : à l'ouverture de session, AVANT E1, et EN PREMIER (préemption), exécuter `python3 skills/gen-plan/scripts/ensure-installed.py --check` (chemin canonique — le script maître est INTÉGRÉ au skill ; le fichier racine `scripts/ensure-installed.py` est un shim de compatibilité qui délègue). rc=0 : écosystème installé (no-op, jamais de réinstallation d'un état à jour). rc≠0 : écosystème absent ou dérivé → **PRÉEMPTION** : l'agent SUSPEND toute tâche, y compris celles en cours d'exécution, et exécute `python3 skills/gen-plan/scripts/ensure-installed.py --reinstall` (pipeline PM-INSTALL §2/§2bis ; clone éphémère SANS persistance de jeton — anti-persistance Task 8/14) AVANT toute autre étape. Le mode `--preempt` concentre la décision : INSTALLE → PRIORITE-NONE (rc 0) ; ROOT absent → réinstallation IMMÉDIATE (PRIORITE-REINSTALL-OK) ; dérivé → PRIORITE-REINSTALL-REQUISE (rc 2, aucune action destructive). Après une réinstallation réussie, le script génère une **directive de mise à jour du plan d'actions en cours** (`download/plan-post-reinstall-<ts>.json`) : l'agent l'intègre au plan de façon COHÉRENTE et OPTIMISÉE (étapes interrompues → statut INTERRUPT-REINSTALL, étapes idempotentes KO-L001 reprennent en l'état, re-validation par arbitres E7/E8 avant reprise), puis journalise au worklog. La garde est idempotente (f(f(x))=f(x)). **Extension Task 56 (v3.35.2 — leçons L54-1/L55-3, garde étendue)** : le contrôle couvre désormais le SKILL.md de TOUTES les entrées KB versionnées (dérivation DYNAMIQUE du registre, regex identique à l'arbitre integrity — KO-L003, jamais figé ; reprise du concept Task 31 `critiques_kb`) ; une dérive limitée à des skills KB manquants est **AUTO-RÉPARÉE** depuis le miroir local `KNOWLEDGE-repo/` (verdict `INSTALLE-REPARÉ`, rc=0, trace worklog — aucune action distante, aucun jeton) — l'angle mort historique « INSTALLE à tort » (version-management, 9 occurrences documentées : worklog lignes 516/527/536/554 + Tasks 52/54/55 + Task 56) est résorbé par construction : la disparition récidivante d'un skill KB ne peut plus passer inaperçue ni persister entre deux invocations de gen-plan.

**Routage de découverte (décision D004)** — quand gen-plan doit trouver, sélectionner ou inventorier des skills (E5, §3) :

1. **skills-inventory en PRIORITÉ** : scanner `{{SKILLS_ROOT}}` via son script (`generate_skills_md.py --json` / `--search` / `--category`). Les performances des éléments trouvés sont comparées aux éléments natifs (couverture, fraîcheur, pertinence des métadonnées) et la comparaison est MÉMORISÉE au registre KB (section Décisions d'architecture) — la mémoire évite de re-comparer à chaque session et alimente le choix du routeur.
2. **skill-finder-cn en FALLBACK** : UNIQUEMENT si skills-inventory échoue (script absent, arbre vide, erreur d'exécution). Tout élément trouvé par le fallback passe un **contrôle cybersécurité `audit-provenance`** (provenance, permissions, contenu dangereux) AVANT adoption ; un échec du contrôle disqualifie l'élément et est consigné au KB. La bascule est unidirectionnelle au cours d'une même recherche : pas de retour à skills-inventory après activation du fallback.

---

<!-- FIN-BLOC-DEPLACÉ:routage_install -->

<!-- BLOC-DEPLACÉ:mode_step:v3.38.0:7f5e2af67f826061 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `7f5e2af67f826061fd02c5c6290f447cbdc9141759725e88544c1cd957f43003`.

### §5.5 Mode step — structure hiérarchique et état d'avancement (v3.25.0)

**Directive propriétaire (2026-10-23, session web-f90062ce ; re-matérialisée v3.25.0 sur base v3.24.0 — directive jamais publiée dans la lignée distante, restaurée sur GO propriétaire ; étendue à toute exécution v3.36.0 — 13ᵉ directive propriétaire, session web-c30e6506 : « vérifie que tous les modes de mon skill \"gen-plan\" ont bénéficiés des optimisations faites dans cette discussion au mode STEP de mon skill \"gen-plan\" » — la couche d'organisation bénéficie à tous les modes)** : en modes step/step-ok — et, depuis v3.36.0, pour TOUTE exécution d'un plan d'actions (mode NULL classique inclus : la couche d'organisation est produite à E7 pour tout plan et lue par toute exécution, la distinction des modes ne portant que sur les portes de confirmation) — chaque groupe du plan d'actions est divisé en sous-groupes de tâches, chaque sous-groupe listant explicitement ses tâches — pour une meilleure compréhension de l'organisation et de l'état du déroulement du plan d'actions.

**Structure canonique** : **Groupe `G<k>`** (unité de vérification — correct-work(groupe), inchangé v3.22.0) → **Sous-groupe `SG<k>.<j>`** (lot cohérent de tâches par affinité de livrable ou de phase, typiquement 2-5 tâches ; un groupe de 3 tâches ou moins admet un sous-groupe unique — jamais de sur-fragmentation) → **Tâche `T<k>.<j>.<i>`** (unité d'exécution élémentaire, taguée #token — N1).

**Statuts d'avancement** (toujours dérivés de l'état vérifiable — livrables, verdicts d'arbitres, worklog — jamais inventés, KO-L003) : `[À FAIRE]` (non entamée) · `[EN COURS]` (entamée) · `[TERMINÉ]` (terminée et constatable) · `[BLOQUÉ]` (adaptation en cours — règle d'or n°1) · `[REPORTÉ]` (déplacée à un groupe ultérieur — E13 journalisé). Compteurs `n/m` par sous-groupe et par groupe.

**Cadence d'affichage (optimisée ; transverse v3.36.0 — toute exécution, tous modes)** : (1) ouverture de groupe — bloc récapitulatif **PLAN-AFFICHE d'évolution du déroulement** (vue d'ensemble : tous les groupes + statuts + compteurs + position du groupe ouvert — E7-DISP v3.36.0) puis tableau complet du groupe (sous-groupes + tâches + statuts + compteurs), en step-ok APRÈS confirmation ; (2) fin de tâche — mise à jour de la ligne et des compteurs, sans ré-affichage complet ; (3) fin de sous-groupe — rappel compact du sous-groupe clôturé ; (4) clôture de groupe — tableau final + verdict correct-work(groupe). Une vue d'ensemble du plan (tous les groupes, statuts, compteurs) ouvre et clôt la chaîne — et, depuis v3.36.0, ouvre CHAQUE groupe de la chaîne (évolution du déroulement visible à chaque étape).

**Règles de cohérence (réconciliées avec la parallélisation par défaut v3.24.0)** : la structure hiérarchique est la couche d'ORGANISATION et de LECTURE du plan (sous-groupes par affinité, statuts, compteurs) — orthogonale à la couche d'EXÉCUTION : l'exécution conserve la parallélisation par défaut (Graph Diamond ouvert automatiquement dès preuve d'indépendance — y compris à travers les frontières de sous-groupes ; le séquentiel reste l'exception justifiée et tracée : dépendance d'ordre, écriture partagée, verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC), chaque tâche d'une vague parallèle mettant à jour individuellement son statut et les compteurs de son sous-groupe ; un plan existant à groupes plats est normalisé à l'ouverture du mode (partition par affinité, idempotente R6, journalisée worklog — extension du plan, jamais réécriture destructrice R2) ; correct-work(groupe) reste calé sur le groupe, pas sur le sous-groupe (cadence v3.22.0 préservée, non-régression R2) ; step-ok hérite intégralement de la structure (confirmation avant chaque groupe, pas avant chaque sous-groupe) ; toute exécution (mode NULL classique inclus) lit la même couche d'organisation depuis v3.36.0 — E7 produit la structure hiérarchique quel que soit le mode d'invocation, et l'affichage d'évolution E7-DISP accompagne l'ouverture de chaque groupe (la distinction des modes ne porte que sur les portes de confirmation).

<!-- FIN-BLOC-DEPLACÉ:mode_step -->

<!-- BLOC-DEPLACÉ:philo4:v3.38.0:f537179d43b93080 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `f537179d43b930807e59e1d6b436de459442e077de65e6cd36e662f1815d93e9`.

4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** (v3.24.0 — inversion du défaut série hérité, directive propriétaire 2026-10-24 ; v3.32.0 — extension aux commandes, directive propriétaire 2026-11-02) — Les sous-tâches ET les commandes (invocations d'outils lancées en un seul message multi-outils, vagues de flotte) PROUVÉES indépendantes (aucune écriture partagée, aucune dépendance d'ordre) s'exécutent en PARALLÈLE PAR DÉFAUT : le Graph Diamond s'ouvre automatiquement dès que la preuve d'indépendance existe (E9-E14). L'exécution série est l'exception justifiée et tracée : dépendance d'ordre, écriture partagée, verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC. Toute vague parallèle est journalisée au worklog (Task IDs `N-a`/`N-b`) et re-vérifiée (re-verdict resource-monitor entre les vagues, arbitre sur l'ensemble fusionné, correct-work par phase). **Dégradation gracieuse des vagues contre un service externe** (leçons Task 29/30, session web-fdf5963c — vérité source PM INSTALL, v3.26.0) : rate limit (429) détecté → bascule sérielle + retry/backoff + cache déterministe (verdicts figés une fois, consultés en lecture seule — jamais re-décidés) ; le code retour seul ne fait jamais foi (purge du fichier de sortie périmé avant appel — un CLI peut sortir rc=0 en erreur) ; tout jugement sémantique délégué pose la question de ROUTAGE du référentiel (jamais une appartenance de domaine) avec la référence complète, jamais tronquée.

<!-- FIN-BLOC-DEPLACÉ:philo4 -->


---

### Extension v3.39.0 — E7-DISP point 6 : fenêtre native d'affichage du plan (AFFICHE-PLAN natif — directive complémentaire 2, trace 1a1b7fe1c7238e8d)

**Directive propriétaire (2026-11-08, session web-ecef7f80)** : « je veux que la fenêtre qui affiche les étapes du plan d'actions soit affichée via la fonction, le script ou la commande qui est dédiée à ce rôle nativement dans "Z.ai" (ou via la commande à laquelle "Z.ai" fait appel) et cela au début de l'exécution du plan d'actions, ainsi qu'à chaque fois qu'une étape du plan d'actions se terminent. intègre $FACON cette fonction, script ou commande dans "AFFICHE-PLAN" de mon écosystème. » — $FACON = de façon cohérente, optimisée et fonctionnelle (glossaire §A).

**Mécanisme natif dédié (Z.ai)** : la **liste de tâches** — fenêtre native du client dédiée à l'affichage des étapes d'un plan d'actions ; outil `TodoWrite` (écriture : création/mise à jour de la liste et des statuts) et `TodoRead` (lecture). Chez tout autre agent : l'équivalent natif dédié à ce rôle (jamais d'invention d'un canal artificiel — R2).

**Point 6 — fenêtre native (canal d'affichage SUPPLÉMENTAIRE, s'ajoute à la chaîne 5 points du hook E7-DISP du bloc hooks_patterns ci-dessus)** :

1. **au DÉBUT de l'exécution du plan d'actions** : la fenêtre native affiche toutes les étapes (groupes `G<k>`) du plan, avec statuts dérivés de l'état vérifiable (règle d'or n°5 / KO-L003 — jamais inventés) et position courante ;
2. **à chaque FIN d'étape (groupe `G<k>`)** : la fenêtre native est MISE À JOUR — l'étape terminée marquée, position et compteurs actualisés (complément du bloc PLAN-AFFICHE d'ouverture d'étape v3.36.0 affiché au chat) ; la mise à jour accompagne le verdict correct-work(groupe).

**Frontières (non-régression des canaux existants)** : la fenêtre native NE REMPLACE ni le bloc récapitulatif au chat (point 5), ni le marqueur `PLAN-AFFICHE` au worklog (point 4), ni la garde mécanique `check_plan_protocol.py` (P1-P5) — la preuve d'affichage journalisable reste le marqueur worklog ; chaque affichage/mise à jour de la fenêtre native est consigné dans la même entrée worklog (mention « fenêtre native »). Affichage REJOUABLE : à toute reprise (E1-RES) sur un plan en vol, la fenêtre native est ré-affichée avant toute autre action (même mécanique que le bloc chat — jamais présumé).
```

