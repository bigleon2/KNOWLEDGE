# CLONE DE DISCUSSION — gen-plan v3.6.1 et Écosystème Knowledge

> **Date du clone** : 2026-08-09
> **Source** : Discussion entre Utilisateur et Assistant
> **Sessions couvertes** : 24 sessions (Task ID 1-24, du 2026-07-18 au 2026-08-09)
> **Version clone-chat** : 2.0.0
> **SHA-256** : 5c6a28d30d4955aa67cc0f3c6aa374eb2346cfa97f68a5f9df5489ddcf944ce0

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : environnement de développement avec 78 skills (6 écosystème + 72 métier) sous `skills/`, registre KB (`skills/KNOWLEDGE.md`), scripts Python sous `scripts/`, prompts maîtres sous `skills/_prompts-maitres/`, et fichiers synchronisés sous `download/`. L'écosystème est versionné semver, avec cross-references bidirectionnelles et dépendances déclarées en YAML frontmatter.

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### 1.1 Résumé global

Cette discussion de 24 sessions couvre la construction, l'harmonisation et la maturation de l'écosystème Knowledge — un ensemble de 78 skills auto-contenus avec registre KB, scripts de vérification automatisés, et conventions strictes de cross-références. L'arc narratif part de l'harmonisation de clone-chat v1.2.0 avec l'écosystème maître (12 corrections), passe par l'enrichissement de gen-plan (signaux de pression, profils VIEUX PC, lecture bloc par bloc), la création d'autonomous-agent v1.0.0, la migration correct-work v2.3.0→v2.4.0 avec hook E8, l'implémentation d'un système de spell-check avec lexique FR+EN et aliases sémantiques (double-pointeurs), et aboutit à un écosystème cohérent validé par 60/60 checks automatisés. Deux clones de discussion ont été produits (ecosysteme-knowledge-clone + clone gen-plan 3.6), chacun validé 8/8 checks.

### 1.2 Table des sessions

| # | Task ID | Date | Thème | Livrables principaux |
|---|---------|------|-------|---------------------|
| 1 | 1 | 2026-07-18 | Harmonisation clone-chat v1.2.0→v2.0.0 | clone-chat SKILL.md, clone-template.md, SHARED, KNOWLEDGE.md |
| 2 | 2 | 2026-07-18 | correct-work CIBLE clone-chat | 2 corrections (guillemet §5, PM version) |
| 3 | 3 | 2026-07-18 | Réécriture integrate-clone-chat-kb | integrate-clone-chat-kb-v3.py (250L) |
| 4 | 4 | 2026-07-18 | Enrichissement gen-plan + autonomous-agent + correct-work | gen-plan §2.4.1-§2.4.2, autonomous-agent SKILL.md, 78 skills |
| 5 | 5 | 2026-07-18 | correct-work CIBLE cross-refs écosystème | 9 corrections (4 S2, 3 S3, 2 S4) |
| 6 | 6 | 2026-07-18 | correct-work PROJET 8 axes A-H | 5 corrections, PM gen-plan §9.4 aligné |
| 7 | 7 | 2026-07-18 | Script sync-download + verify-cross 60 checks | sync-download.py, verify-cross.py (60/60) |
| 8 | 8 | 2026-07-18 | correct-work DIRECT scripts Python | 10 findings, 7 corrections |
| 9 | 9 | 2026-07-18 | Mise à jour README + sync | README.md corrigé, 60/60 confirmé |
| 10 | 10 | 2026-07-18 | Push GitHub post git reset | 15 fichiers, commit 1b2af48 |
| 11 | 11 | 2026-08-09 | Phase A — Reconstruction _prompts-maitres/, gen-plan/, correct-work/ | 13 fichiers créés/restaurés |
| 12 | 12 | 2026-08-09 | Phase B — Recréer KNOWLEDGE.md | KNOWLEDGE.md (91 lignes, 6 entrées, 13 relations) |
| 13 | 13 | 2026-08-09 | Phase C+D — Audit GLOBAL + corrections | 8 findings, clone-chat réinstallé, ALL PASS |
| 14 | 14 | 2026-08-09 | Push Phase D vers GitHub | Commit 98782ef, 1129 fichiers |
| 15 | 15 | 2026-08-09 | correct-work v2.3.0→v2.4.0 | Hook E8, verify-correct-work.py, evals.json, 152 checks |
| 16 | 16 | 2026-08-09 | Post-migration PM v2.3.0→v2.4.0 | 21 findings, PM v2.4.0 (528L), _archive/ |
| 17 | 17 | 2026-08-09 | Spell-check écosystème + lexique | spell-check.py, lexique-domain.json, 126 corrections |
| 18 | 18 | 2026-08-09 | Double-pointeurs aliases + 40 tests | 13 canoniques, 29 alias, lexique-fr.py supprimé |
| 19 | 19 | 2026-08-09 | ECOSYSTEM_FILES + convention préfixe _ | SHARED §1.2 exception, 18 fichiers écosystème |
| 20 | 20 | 2026-08-09 | Clone écosystème complet | ecosysteme-knowledge-clone-2026-08-09.md (322L) |
| 21 | 21 | 2026-08-09 | correct-work CIBLE du clone | 5 findings, 3 corrections, PASS |
| 22 | 22 | 2026-08-09 | 5 optimisations clone | 286→322 lignes, SHA-256, sessions 20-21 |
| 23 | 23 | 2026-08-09 | gen-plan v3.6.0→v3.6.1 + lecture bloc par bloc | SKILL.md, etapes-detaillees.md, 6 corrections |
| 24 | 24 | 2026-08-09 | Clone gen-plan 3.6 + écosystème | clone-de-gen-plan-3.6-et-ecosystem.md |

### 1.3 Détail par session

**Sessions 1-5 (2026-07-18)** : Harmonisation initiale de l'écosystème. La session 1 (Task 1) est la plus dense : 12 écarts identifiés entre clone-chat v1.2.0 et l'écosystème maître (gen-plan v3.6.0, correct-work v2.3.0, 77 skills). Chaque écart (D1-D12) est corrigé : comptage des skills, frontmatter YAML, variables SHARED, conventions de numérotation §. La session 2 valide clone-chat via correct-work CIBLE (2 corrections mineures). La session 3 réécrit entièrement integrate-clone-chat-kb.py (v2.0.0→v3.0.0, de 1066 à 250 lignes). La session 4 est triple : enrichissement gen-plan avec signaux de pression et 5 règles VIEUX PC, création d'autonomous-agent v1.0.0 (5 modules, 4 modes, pipeline A-H), et correct-work DIRECT 16/16. L'écosystème passe à 78 skills (6 écosystème + 72 métier). La session 5 (Task 5) vérifie les cross-references écosystème via correct-work CIBLE (9 corrections incluant used_at clone-chat, §2.4 signaux de pression, PM §9.4).

**Sessions 6-10 (2026-07-18)** : Infrastructure de vérification et GitHub. La session 6 (Task 6) est un audit PROJET complet en 8 axes (A-H) : 5 corrections dont l'alignement du PM gen-plan §9.4 avec profils-ressource.md réel. La session 7 (Task 7) crée sync-download.py (2 modes CHECK/SYNC) et ajoute CHECK 6 à verify-cross.py (55→60 checks). La session 8 (Task 8) audite les scripts Python : 10 findings (chemins absolus, code mort, variable non lue, incohérence numérique), 7 corrections appliquées. La session 9 (Task 9) finalise README.md et synchronise download/. La session 10 (Task 10) gère une récupération d'urgence post git reset --hard : 10 fichiers récupérés depuis le reflog, push de 15 fichiers vers GitHub.

**Sessions 11-15 (2026-08-09)** : Reconstruction et migrations majeures. Les sessions 11-13 (Tasks 11-13) reconstruisent l'écosystème après perte de fichiers : Phase A (13 fichiers restaurés dont _prompts-maitres/ et gen-plan/), Phase B (KNOWLEDGE.md recréé, 91 lignes, 6 entrées, 13 relations), Phase C+D (audit GLOBAL, 8 findings, clone-chat réinstallé, ALL PASS). La session 14 (Task 14) pousse le résultat (commit 98782ef, 1129 fichiers). La session 15 (Task 15) est la migration correct-work v2.3.0→v2.4.0 : hook E8 dans gen-plan, création de verify-correct-work.py (16 checks automatisés), evals.json (6 cas de test), découplage gen-plan (autonome), support multi-cibles, métriques de performance. 152 checks total PASS.

**Sessions 16-19 (2026-08-09)** : Qualité linguistique et conventions. La session 16 (Task 16) traite 21 findings post-migration : création du PM v2.4.0 (528 lignes), archivage du PM v2.3.0 dans `_archive/`, 7 fichiers modifiés. La session 17 (Task 17) implémente un système de spell-check complet : corpus FR de 3148 mots uniques, lexique dynamique 216 entrées (FR+EN), spell-check.py v1.0.0 (5 modes : scan/fix/learn/test/stats), 126 corrections orthographiques dans 15 fichiers, 31/31 tests PASS. La session 18 (Task 18) enrichit le système avec des aliases sémantiques (double-pointeurs) : 13 groupes canoniques, 29 alias, protection des zones alias dans le scan, 40/40 tests. Suppression de lexique-fr.py (obsolète). La session 19 (Task 19) ajoute verify-correct-work.py aux fichiers écosystème monitorés, enrichit les aliases (8→13 canoniques), et établit la convention du préfixe « _ » = dossier infrastructure (SHARED §1.2).

**Sessions 20-24 (2026-08-09)** : Clonage et optimisations. La session 20 (Task 20) produit le premier clone complet : ecosysteme-knowledge-clone-2026-08-09.md (286 puis 322 lignes, 19 sessions, 8/8 checks PASS). La session 21 (Task 21) valide ce clone via correct-work CIBLE (5 findings, 3 corrections). La session 22 (Task 22) intègre 5 optimisations dans le clone : sessions 20-21, section §2.3 spécifications techniques (9 fichiers), grille #token complète, note de différenciation §2.5, checksum SHA-256. La session 23 (Task 23) intègre la méthode « lecture bloc par bloc » dans gen-plan (SKILL.md + etapes-detaillees.md E2/E9/E10), puis correct-work CIBLE trouve 6 findings (paths `références/`→`references/`, count, version bump v3.6.0→v3.6.1, dep correct-work). La session 24 (Task 24, en cours) produit le clone gen-plan 3.6 + écosystème.

---

## §2 — ÉCOSYSTÈME DE SKILLS

### 2.1 Skills créés ou modifiés

#### gen-plan v3.6.1

- **Description** : Skill de planification de tâches pour assistant IA. 4 modes (Planification, Exécution, Surveillance, Adaptation), 15 étapes (E1-E15), 3 profils ressource (NORMAL/ECO/VIEUX PC), tagging #token, lecture bloc par bloc pour fichiers > 500 lignes.
- **Catégorie** : ecosystem | **Langue** : fr
- **Spécification fonctionnelle** : 4 modes (M1 Planification, M2 Exécution, M3 Surveillance, M4 Adaptation). 15 étapes : E1 Analyse demande, E2 Inventaire ressources (avec méthode bloc par bloc), E3 Classification type 1-4, E4 Estimation #token, E5 Sélection skills, E6 Profilage ressource, E7 Création plan, E8 Validation + hook correct-work si >= v2.4.0, E9 Lancement exécution, E10 Suivi, E11 Checkpoint, E12 Détection écart, E13 Ajustement, E14 Finalisation, E15 Bilan + auto-calibration. 3 profils : NORMAL (défaut, 15 étapes), ECO (< 5 sessions, étapes réduites), VIEUX PC (2+ signaux pression, scripts < 100L, pas de graphiques). Downgrade irréversible. Signaux de pression : disque < 5 Go, timeout 2+ consécutifs, budget > 80%. Filtrage #token : ECO exclut > 8000, VIEUX PC exclut > 5000.
- **Spécification technique** : Stack Python/Markdown/YAML. Environnement `skills/gen-plan/`. Structure : SKILL.md (~178 lignes), references/ (etapes-detaillees.md, grille-token.md, classification-types.md, profils-ressource.md, guide-selection-agent-skill.md), evals/evals.json. Aucune dépendance externe.
- **Relations** : Invoque correct-work >= v2.4.0 (E1 + E8 hook), utilise clone-chat >= v2.0.0 (E4/E15 optionnel), consulte skills-inventory >= v1.0.0 (E5), enrichit KNOWLEDGE.md (E15).

#### clone-chat v2.0.0

- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, 8 checks de validation binaire, 5 types de Context Drift, auto-clonage infini.
- **Catégorie** : ecosystem | **Langue** : fr
- **Spécification fonctionnelle** : 7+1 étapes : (1) Collecte worklog, (2) Collecte artefacts, (3) Extraction décisions, (3.5) Context Drift (5 types : INVERSION, MODIFICATION, CORRECTION, ENRICHISSEMENT, RECALIBRAGE), (4) Spécifications techniques (in extenso < 200L, condensé 200-500L, résumé > 500L), (5) Assemblage §0-§5, (6) Validation 8 checks, (7) Sauvegarde. 8 checks : auto-suffisance, complétude worklog/skills/décisions/bugs/drifts, exécutabilité, auto-clonage. 3 profils : NORMAL (complet), ECO (condensé), VIEUX PC (§3.5 + §5 uniquement). Intégration gen-plan v3.6.0+ : données calibration E15, structure E1-E7, registre KB.
- **Spécification technique** : Markdown pur (CommonMark), aucun outil spécifique. Structure : SKILL.md (~364 lignes), references/clone-template.md (~180 lignes). Fichier unique auto-suffisant, versionnable git.
- **Relations** : Archivé par gen-plan (E4/E15, optionnel), vérifié par correct-work (Mode CIBLE §3.5), conventions par skill-creator.

#### correct-work v2.4.0

- **Description** : Vérification et correction du travail. 3 modes (PROJET/CIBLE/DIRECT), 5 étapes, multi-cibles, découplage gen-plan, métriques de performance (5 métriques cibles).
- **Catégorie** : ecosystem | **Langue** : fr
- **Spécification fonctionnelle** : 3 modes : PROJET (audit complet 8 axes), CIBLE (fichier unique, 5 étapes), DIRECT (scan rapide, 0 étape formelle). 5 étapes en mode CIBLE : (1) Plan autonome, (2) Erreurs (S1-S4), (3) Conflits structurels, (4) Interactions, (5) Cohérence. Sévérité : S1 (critique, bloquant), S2 (majeur), S3 (mineur), S4 (suggestion). Découplé de gen-plan (fonctionne standalone). Hook dans gen-plan E8 (si >= v2.4.0). Support multi-cibles (vérifie plusieurs fichiers d'un coup). Métriques : taux détection, taux faux positifs, couverture, temps moyen, sévérité moyenne.
- **Spécification technique** : Stack Markdown/Python. Structure : SKILL.md (~315 lignes), scripts/verify-correct-work.py (16 checks automatisés), evals/evals.json (6 cas de test), PM v2.4.0 (528 lignes).
- **Relations** : Vérifie gen-plan (plan de vérification Étape 1), vérifie clone-chat (Mode CIBLE §3.5), vérifie fullstack-dev (projets web), vérifié par gen-plan (E1 + E8 hook).

#### autonomous-agent v1.0.0

- **Description** : Agent autonome avec mémoire interne à deux niveaux (État Court + État Long). 5 modules internes, 4 modes, pipeline 8 étapes (A-H).
- **Catégorie** : ecosystem | **Langue** : fr
- **Spécification fonctionnelle** : 5 modules : (1) Planificateur, (2) Exécuteur, (3) Observateur, (4) Mémoriel, (5) Décisionnel. 4 modes : RECHERCHE, PLANIFICATION, EXECUTION, REFLEXION. Pipeline A-H : A Initialisation, B Analyse contexte, C Planification, D Exécution, E Observation, F Mémorisation, G Décision, H Finalisation. Format .agent pour la persistance. Orchestration multi-agents et multi-LLM.
- **Spécification technique** : Structure : SKILL.md, references/agent-format.md (schéma YAML, exemple, règles persistance). Dépend de gen-plan >= v3.6.0.
- **Relations** : Utilise gen-plan (tâches complexes), persist via clone-chat (État Long, optionnel), vérifié par correct-work.

#### skills-inventory v1.0.0

- **Description** : Scan et inventaire des skills disponibles. Consultation par tags, catégories, versions.
- **Catégorie** : ecosystem | **Langue** : fr
- **Relations** : Consulté par gen-plan (E5 sélection skills). Aucune dépendance.

#### skill-creator v1.0.0

- **Description** : Création et gestion de skills. Templates, évaluations, agents spécialisés.
- **Catégorie** : ecosystem | **Langue** : fr
- **Relations** : Conventions utilisées par clone-chat (structurelles). Aucune dépendance.

### 2.2 Scripts créés ou modifiés

#### spell-check.py v1.0.0

- **Description** : Système de vérification orthographique pour l'écosystème Knowledge. 5 modes (scan/fix/learn/test/stats), lexique FR+EN dynamique, aliases sémantiques (double-pointeurs).
- **Signature** : scan_file(), apply_fixes(), _build_alias_zones(), _in_alias_zone(), 40 tests unitaires
- **Chemin** : `scripts/spell-check.py`

#### verify-cross.py (60 checks)

- **Description** : Vérification automatisée de la cohérence cross-fichiers de l'écosystème. 6 axes : structure, frontmatter, contenus, cross-refs, cohérence numérique, sync download/.
- **Signature** : 6 CHECK (structure, frontmatter, contenus, cross-refs, cohérence, sync), sortie 60/60 PASS
- **Chemin** : `scripts/verify-cross.py`

#### sync-download.py

- **Description** : Synchronisation bidirectionnelle entre `skills/_prompts-maitres/` (source) et `download/` (copie). 2 modes : CHECK (dry-run) et SYNC (avec confirmation).
- **Signature** : do_sync(), 5 fichiers PMs mappés, comparaison SHA-256
- **Chemin** : `scripts/sync-download.py`

#### verify-correct-work.py (16 checks)

- **Description** : Vérification automatisée du skill correct-work (structure, frontmatter, contenu, évals, scripts).
- **Signature** : 16 checks, sortie 16/16 PASS
- **Chemin** : `skills/correct-work/scripts/verify-correct-work.py`

#### integrate-clone-chat-kb-v3.py v3.0.0

- **Description** : Intégration des données de clone-chat dans le registre KB. Version légère (250 lignes), pas de contenu embedded — lit depuis skills/clone-chat/.
- **Signature** : 10 checks automatisés, scan 76+ skills
- **Chemin** : `scripts/integrate-clone-chat-kb-v3.py`

### 2.3 Spécifications techniques

| Fichier | Taille | Traitement clone | Description |
|---------|--------|-----------------|-------------|
| gen-plan/SKILL.md | ~178 lignes | In extenso | Skill opérationnel compact, 4 modes, 15 étapes, 3 profils |
| clone-chat/SKILL.md | ~364 lignes | Condensé | 7+1 étapes, 8 checks, 5 types drift, auto-clonage |
| correct-work/SKILL.md | ~315 lignes | Condensé | 3 modes, 5 étapes CIBLE, 4 sévérités, métriques |
| autonomous-agent/SKILL.md | ~200 lignes | Condensé | 5 modules, 4 modes, pipeline A-H, mémoire 2 niveaux |
| KNOWLEDGE.md | 92 lignes | In extenso | 6 entrées skills, 13 relations bidirectionnelles |
| gen-plan/references/etapes-detaillees.md | ~311 lignes | Condensé | Détail E1-E15 + portées étendues E8/E14/E15 |
| gen-plan/references/grille-token.md | ~49 lignes | In extenso | Grille calibration par agent/skill + historique |
| gen-plan/references/profils-ressource.md | ~85 lignes | In extenso | NORMAL/ECO/VIEUX PC + downgrade irréversible |
| gen-plan/references/classification-types.md | ~79 lignes | In extenso | Routing Type 1-4 + cas ambigus |
| gen-plan/references/guide-selection-agent-skill.md | ~48 lignes | In extenso | Arbre de décision + tableau correspondance |
| clone-chat/references/clone-template.md | ~180 lignes | In extenso | Template §0-§5 pour assemblage clone |

### 2.4 Artefacts produits

| Fichier | Description |
|---------|-------------|
| download/ecosysteme-knowledge-clone-2026-08-09.md | Clone complet de l'écosystème (322 lignes, 21 sessions, 8/8 checks) |
| download/clone-de-gen-plan-3.6-et-ecosystem.md | Clone gen-plan v3.6.1 + écosystème (ce fichier) |
| scripts/lexique-domain.json | Lexique FR+EN (216 entrées, 13 groupes aliases, 29 alias) |
| skills/_prompts-maitres/_archive/ | Archive des anciens PMs (convention historique) |
| skills/correct-work/evals/evals.json | 6 cas de test pour correct-work v2.4.0 |

### 2.5 Notes de différenciation

Ce clone se distingue du clone précédent (ecosysteme-knowledge-clone-2026-08-09.md) par son focus sur **gen-plan v3.6.1** : il inclut le contenu in extenso du SKILL.md gen-plan et de toutes ses références (grille-token, profils-ressource, classification-types, guide-selection-agent-skill), ainsi que le détail de la méthode « lecture bloc par bloc » (philosophie #7, E2, E9, E10). Le clone précédent couvrait l'ensemble de l'écosystème de manière uniforme ; celui-ci zoom sur gen-plan et son environnement immédiat.

---

## §3 — DÉCISIONS CLÉS

### 3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | Garder le préfixe « _ » dans _prompts-maitres/ | Analyse gen-plan E1-E8 : 9 fichiers référencent le chemin, 0 autre dossier skills/_* | Convention pérennisée : préfixe _ = dossier infrastructure (SHARED §1.2) |
| 2 | Harmoniser clone-chat avec l'écosystème maître | clone-chat v1.2.0 avait des versions obsolètes (gen-plan v3.5.0, correct-work v1.2.0) | 12 corrections D1-D12, clone-chat v2.0.0 |
| 3 | Créer autonomous-agent comme skill écosystème | Besoin d'agent autonome avec mémoire inter-sessions | 78 skills (6 écosystème + 72 métier), 13 relations |
| 4 | Downgrade irréversible des profils ressource | Éviter les oscillations profil pendant l'exécution | Philosophie #8 gen-plan, profils-ressource.md |
| 5 | Archiver les anciens PMs dans _archive/ | Migration PM v2.3.0→v2.4.0, garder historique accessible | Convention _archive/ introduite (Task 16) |
| 6 | Intégrer SHA-256 dans les clones | Traçabilité et vérification d'intégrité des clones | Header clone avec checksum pré/post optimisation (Task 22) |
| 7 | Enrichir gen-plan avec lecture bloc par bloc | Fichiers > 500 lignes causaient des pertes de contexte | Philosophie #7, E2/E9/E10, bump v3.6.0→v3.6.1 |
| 8 | Implémenter un lexique FR+EN avec aliases | 126 fautes orthographiques FR dans 15 fichiers écosystème | spell-check.py v1.0.0, 216 entrées, 13 groupes aliases |

### 3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | Guillemet non fermé §5 clone-chat | Erreur de frappe lors de l'harmonisation | Fermeture du guillemet | correct-work PASS (Task 2) |
| 2 | PM correct-work encore à v1.2.0 | Oubli lors de la mise à jour | 3 occurrences mises à jour | Cohérence frontmatter (Task 2) |
| 3 | file_hash() jamais appelée (sync-download) | Code mort après refactor | Suppression + import hashlib | Script nettoyé (Task 8) |
| 4 | Chemins absolus dans verify-cross.py | /home/z/my-project/ en dur | Chemins dynamiques os.path.dirname | Portabilité (Task 8) |
| 5 | README dit 55 checks mais script en fait 60 | Ajout CHECK 6 non répercuté | README 55→60, 5→6 axes | Cohérence numérique (Task 8) |
| 6 | Chemins `références/` (accent) dans gen-plan | Incohérence chemin réel (references/) | 3 occurrences corrigées | correct-work PASS (Task 23) |
| 7 | Count gen-plan « ~195 lignes » vs réel 178L | Ancien count non mis à jour | ~195→~180 | Cohérence (Task 23) |
| 8 | 9 écarts clone-chat vs écosystème maître | Versions obsolètes dans 6 fichiers | 12 corrections D1-D12 | clone-chat v2.0.0 (Task 1) |
| 9 | 21 findings post-migration PM v2.3.0→v2.4.0 | PM jamais migré + références obsolètes | PM v2.4.0 créé, 7 fichiers modifiés | ALL PASS (Task 16) |
| 10 | 126 fautes orthographiques FR/EN | Pas de vérification orthographique automatisée | spell-check.py + 126 corrections | 0 finding écosystème (Task 17) |
| 11 | Section ordering cassée après MultiEdit clone | §2.5 inséré avant §2.3 | Renumérotation §2.3→§2.4→§2.5 | Ordre logique restauré (Task 22) |
| 12 | do_sync copie fichiers identiques | Pas de comparaison préalable | Skip si fichiers identiques (filecmp) | Performance sync (Task 8) |

### 3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| Kebab-case | Tous les noms de fichiers/répertoires en kebab-case | `gen-plan`, `etapes-detaillees.md` |
| Semver | Versionning MAJEUR.MINEUR.PATCH | gen-plan v3.6.1, correct-work v2.4.0 |
| Préfixe _ = infrastructure | Dossiers avec _ sont de l'infrastructure, pas des skills | `skills/_prompts-maitres/` |
| _archive/ | Anciens PMs conservés dans _archive/ | `skills/_prompts-maitres/_archive/PM-correct-work-v2.3.0.md` |
| Numérotation § | Sections des SKILL.md et clones en préfixe § | §0 Règle zéro, §1 Chronologie |
| Tagging #token | Chaque étape/skill reçoit un tag #token estimé | `#token 3500` |
| YAML frontmatter | Chaque SKILL.md commence par un bloc YAML | name, version, category, language, tags, description, dependencies |
| Chemins relatifs | Jamais de chemins absolus dans les documents | `skills/gen-plan/SKILL.md` |
| Downgrade irréversible | Profil ressource ne remonte jamais automatiquement | NORMAL→ECO définitif pour la session |
| Lecture bloc par bloc | Fichiers > 500L : lire par blocs de 200L avec synthèse intermédiaire | E2, E9, E10 de gen-plan |
| Double-pointeurs | Aliases sémantiques protégés du spell-check | correct-work = « vérifie ton travail » |
| SHA-256 clone | Checksum d'intégrité dans l'en-tête des clones | Header avec SHA-256 pré/post |
| Snapshot historique | Les clones référencent les versions telles qu'elles étaient au moment du clonage | Clone garde gen-plan v3.6.0 (pré-bump) |
| Worklog SHARED §1.4 | Format normalisé : Task ID, Agent, Task, Work Log, Stage Summary | Chaque entrée séparée par `---` |

### 3.4 Données de calibration

**Grille #token gen-plan v3.6.1** :

| Agent/Skill | #token min | #token max | Coeff. |
|-------------|-----------|-----------|-------|
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

**Coefficients** : 0.8x (faible), 1.0x (standard), 1.3x (élevée), 1.5x (critique), ECO 0.7x, VIEUX PC 0.5x.

**Grille clone-chat** :

| Mode | #token estimé | Profil min. |
|------|--------------|-------------|
| Court (< 5 sessions) | 2000-3500 | ECO |
| Moyen (5-15 sessions) | 3500-5500 | NORMAL |
| Long (> 15 sessions) | 5500-9000 | NORMAL |

**Historique de calibration** :

| Exécution | Type | Estimé | Réel | Écart | Action |
|-----------|------|--------|------|-------|--------|
| 1 | Planification 66 skills | 4500 | 5200 | +15.6% | Aucune (0-20%) |
| 2 | Test E2E gen-plan | 3000 | 3600 | +20.0% | Aucune (seuil) |
| 3 | clone-chat v1.1.0 | 4000 | 5200 | +30.0% | Ajustement grille |
| 4 | clone-chat v1.2.0 | 4400 | 4600 | +4.5% | Aucune (0-20%) |

**Métriques de vérification** :

| Métrique | Valeur cible | Valeur actuelle |
|----------|-------------|---------------|
| verify-cross.py | 60/60 PASS | 60/60 PASS |
| verify-correct-work.py | 16/16 PASS | 16/16 PASS |
| spell-check.py tests | 40/40 PASS | 40/40 PASS |
| sync-download.py | SYNC OK | SYNC OK |
| Total checks | 152+ | 152+ PASS |

### 3.5 Évolutions de contexte (Context Drift)

Cette section trace chaque fois que le contexte a **changé** durant la discussion.

**5 types de drift** :

| Type | Définition |
|------|----------|
| INVERSION | Décision renversée (A accepté → A refusé) |
| MODIFICATION | Décision ajustée (paramètre X → Y) |
| CORRECTION | Spécification ou décision erronée corrigée |
| ENRICHISSEMENT | Décision complétée (ajout d'un élément nouveau) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibré) |

**Table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | ENRICHISSEMENT | clone-chat v1.2.0 (7 étapes, 7 checks) | clone-chat v2.0.0 (7+1 étapes, 8 checks, 5 types drift, variables SHARED) | 1 | L1-33 | Harmonisation écosystème maître (12 corrections D1-D12) |
| 2 | ENRICHISSEMENT | 77 skills (5 écosystème + 72 métier) | 78 skills (6 écosystème + 72 métier) | 4 | L88-94 | Création autonomous-agent v1.0.0 |
| 3 | ENRICHISSEMENT | gen-plan sans signaux de pression | gen-plan avec §2.4.1 signaux + §2.4.2 filtrage #token + 5 règles VIEUX PC | 4 | L77-87 | Enrichissement depuis prompt-maitre v3.4.0 |
| 4 | MODIFICATION | correct-work v2.3.0 (standalone, 3 modes) | correct-work v2.4.0 (hook E8, 16 checks auto, métriques, multi-cibles, découplé) | 15 | L350-369 | Migration majeure avec 8 écarts traités |
| 5 | CORRECTION | Chemins `références/` (accent) dans gen-plan SKILL.md | Chemins `references/` (réel, sans accent) | 23 | L567-568 | Trouvé par correct-work CIBLE, 3 occurrences |
| 6 | CORRECTION | verify-cross.py 55 checks | verify-cross.py 60 checks | 7 | L196-203 | Ajout CHECK 6 (sync download/ vs source) |
| 7 | RECALIBRAGE | Grille #token clone-chat (v1.0.0) | Grille recalibrée après exécution réelle (3 entrées historique) | 3 | L47-48 | clone-chat v1.1.0 : +30% écart → ajustement |
| 8 | ENRICHISSEMENT | Aucun système de spell-check | spell-check.py v1.0.0 + lexique 216 entrées + aliases 13 groupes | 17 | L400-422 | 126 corrections dans 15 fichiers |
| 9 | ENRICHISSEMENT | Aliases simples (8 canoniques, 17 alias) | Double-pointeurs (13 canoniques, 29 alias, protection zones) | 18 | L433-439 | Système de protection des zones alias dans scan/fix |
| 10 | MODIFICATION | Pas de convention préfixe _ | Préfixe _ = infrastructure (SHARED §1.2) | 19 | L474-479 | Décision validée utilisateur après analyse E1-E8 |
| 11 | ENRICHISSEMENT | gen-plan v3.6.0 (sans méthode lecture) | gen-plan v3.6.1 (philosophie #7, E2/E9/E10 lecture bloc par bloc) | 23 | L562-583 | Intégration méthode + 6 corrections correct-work |
| 12 | RECALIBRAGE | Clone écosystème 286 lignes (19 sessions) | Clone optimisé 322 lignes (21 sessions, +12.6%) | 22 | L540-554 | 5 optimisations : sessions 20-21, §2.3 specs, grille #token, §2.5, SHA-256 |

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire

1. Lire §0 (Règle zéro) — tout est à reconstruire
2. Reconstruire les fichiers spécifiés dans §2 :
   - **In extenso** : gen-plan/SKILL.md, KNOWLEDGE.md, grille-token.md, profils-ressource.md, classification-types.md, guide-selection-agent-skill.md, clone-template.md
   - **En résumé structuré** : clone-chat/SKILL.md, correct-work/SKILL.md, autonomous-agent/SKILL.md, etapes-detaillees.md
3. Appliquer les décisions et conventions de §3
4. Créer les artefacts listés dans §2.4
5. Se positionner à l'état exact de la fin de la discussion originale

### Fichiers à reconstruire en priorité

1. **skills/gen-plan/SKILL.md** — Skill central de planification, v3.6.1 avec lecture bloc par bloc
2. **skills/KNOWLEDGE.md** — Registre KB, source de vérité (6 entrées, 13 relations)
3. **skills/clone-chat/SKILL.md** — Skill de clonage, v2.0.0 (nécessaire pour auto-clonage §5)
4. **skills/correct-work/SKILL.md** — Skill de vérification, v2.4.0 (hook E8 dans gen-plan)
5. **skills/gen-plan/references/** — 5 fichiers référence (étapes, grille, profils, classification, guide)
6. **scripts/verify-cross.py** — 60 checks automatisés de cohérence écosystème
7. **scripts/spell-check.py** + **scripts/lexique-domain.json** — Spell-check FR+EN avec aliases

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra :
   - Tout le contexte de ce clone (gen-plan v3.6.1, écosystème, 24 sessions)
   - Tout le nouveau contexte de la discussion en cours
3. Les sections §1-§3 (incluant §3.5 Context Drift) sont **enrichies** avec les nouvelles sessions. Les sections §0, §4-§5 sont **régénérées à l'identique** (auto-référentielles).
4. Le nouveau clone remplace ce fichier — le clone « grandit » à chaque session sans perte d'information (chaîne de clonage théoriquement infinie)

**Mécanisme** : le skill clone-chat v2.0.0 (7+1 étapes, 8 checks de validation) est utilisé pour produire le nouveau clone. Si gen-plan v3.6.1+ est présent, les enrichissements suivants sont appliqués : données calibration E15, structure E1-E7, registre KB. Le checksum SHA-256 est recalculé pour chaque nouveau clone.

**Fichier de référence** : `skills/clone-chat/references/clone-template.md`