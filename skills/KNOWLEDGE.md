# KNOWLEDGE.md — Registre central de l'écosystème Knowledge

> Source de vérité des versions et des relations (README §4 / SHARED §2).
> Format des entrées : template SHARED §2.2. Mise à jour à chaque matérialisation (gen-plan E15).

## gen-plan v3.11.0

- **Category** : ecosystem
- **Description** : Planification structurée des tâches — 4 modes, 15 étapes E1-E15, classification Type 1-4 (E3), règles d'or §1.8 (n°2 régénération post-installation, n°3 mise à jour à chaque nouvelle demande), disciplines d'ingénierie (orchestration §1.9 — source de vérité : SHARED §7), méthode de raisonnement adaptative PEK v4.1 (§1.9 — 3 modes CoT/Chaining/Hybride, blocs A-J, 9 règles, 12 checks, référence prompt-engineering-kit.md), hook correct-work par phase E9-E14
- **Dépend de** : correct-work >= v2.4.0 (hooks E9-E14), clone-chat >= v2.0.0 (E4, E15, optionnel), skills-inventory >= v1.0.0 (E5), agent-prompt-engineering >= v1.0.0 (délégation §1.9)
- **Utilisé par** : correct-work (Étape 1, optionnel), clone-chat (optionnel), autonomous-agent, Main (planification complète), agent-prompt-engineering (contexte écosystème, E1-E8)
- **Dernière calibration** : 2026-09-10 (révision B3 : harmonisation bidirectionnelle du registre — réciproques « Utilisé par » clone-chat, agent-prompt-engineering ; révision B1 : intégration PEK v4.1 par assemblage — couche de raisonnement adaptative, 6e référence prompt-engineering-kit.md, PM v3.11.0 ; A12 : règles d'or n°2-n°3, directive utilisateur ; A11 : disciplines implantées en SHARED §7, triggers 9/9)
- **Statut** : stable

## correct-work v2.5.1

- **Category** : ecosystem
- **Description** : Vérification et correction des livrables (erreurs, omissions, incohérences) — 3 modes (PROJET/CIBLE/DIRECT), 5 étapes, multi-cibles, checklists unifiées §10
- **Dépend de** : gen-plan >= v3.7.0 (Étape 1, optionnel), clone-chat >= v2.0.0 (Mode CIBLE, §3.5), fullstack-dev >= v1.0.0 (projets web), skills-inventory >= v1.0.0 (scan dynamique KB)
- **Utilisé par** : gen-plan (hooks par phase E9-E14), clone-chat (validation croisée), Main (vérification finale)
- **Dernière calibration** : 2026-09-10 (révision B3 : harmonisation bidirectionnelle du registre — réciproque « Utilisé par » clone-chat, dépendance skills-inventory (scan dynamique KB) ; A10 : Description Optimization « erreurs, omissions, incohérences », itération-3 triggers 8/8 ; A9 : schéma evals unifié)
- **Statut** : stable

## clone-chat v2.0.0

- **Category** : ecosystem
- **Description** : Clonage de discussion en Markdown auto-suffisant — protocole 7+1 étapes, 8 checks, 5 types de drift, protocole d'héritage §1.0, compatibilité ascendante (révision prompt 1.0.3)
- **Dépend de** : gen-plan >= v3.6.1 (optionnel), correct-work >= v2.4.0 (validation croisée), skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : gen-plan (E15, archivage — leçon E23), correct-work (Mode CIBLE, §3.5), autonomous-agent (persistance d'état)
- **Dernière calibration** : 2026-09-10 (révision B3 : harmonisation bidirectionnelle du registre — réciproque « Utilisé par » correct-work ; 10ᵉ clone scellé 776ff9c0…, révision prompt 1.0.3)
- **Statut** : stable

## skills-inventory v1.0.0

- **Category** : ecosystem
- **Description** : Scan et inventaire des skills disponibles (E5 de gen-plan)
- **Dépend de** : —
- **Utilisé par** : gen-plan (E5), correct-work (scan dynamique KB)
- **Dernière calibration** : N/A
- **Statut** : stable

## skill-creator v1.0.0

- **Category** : ecosystem
- **Description** : Création et gestion de skills (conventions structurelles)
- **Dépend de** : —
- **Utilisé par** : clone-chat (conventions), agent-prompt-engineering (création)
- **Dernière calibration** : N/A
- **Statut** : stable

## autonomous-agent v1.0.0

- **Category** : ecosystem
- **Description** : Agent autonome avec mémoire interne (tâches longues)
- **Dépend de** : gen-plan >= v3.6.0, clone-chat >= v2.0.0 (persistance, optionnel)
- **Utilisé par** : —
- **Dernière calibration** : N/A
- **Statut** : stable

## agent-prompt-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Optimisation fine des prompts complexes (rédaction, restructuration, évaluation, itération — 4 modes M1-M4). Spécialise la méthode prompt-engineering (méthode-mère : gen-plan ; source de vérité : SHARED §7)
- **Dépend de** : gen-plan >= v3.7.0 (contexte écosystème, E1-E8), skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : gen-plan (délégation §1.9), install-ecosystem (P6-P7)
- **Dernière calibration** : 2026-09-06 (MATÉRIALISÉ : SKILL.md + evals/evals.json + evals/trigger_evals.json + references/grille-evaluation-prompt.md ; A11 : pointeurs SHARED §7, v1.0.1)
- **Statut** : stable

## context-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline context engineering (curation de contexte, compaction, clairage juste-à-temps, mémoire externe, budget d'attention). Spécialise la discipline context engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (couche disciplines E2/E5/E9-E14), sessions d'ingénierie
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Statut** : stable

## loop-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline loop engineering (boucle d'exécution, boucle de vérification avec graders, boucle externe d'amélioration continue). Spécialise la discipline loop engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (couche disciplines E10-E15), correct-work (hooks de vérification), sessions d'ingénierie
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Statut** : stable

## graph-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline graph engineering (graphe de connaissances, nœuds/arêtes versionnés, requêtes ancrées KB, anti-hallucination). Spécialise la discipline graph engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (E5/E15), correct-work (scan dynamique KB), sessions d'ingénierie
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Statut** : stable

## harness-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline harness engineering (harnais d'exécution, gardes-fous, profilage ressource, arbitres, resserrage après dérive). Spécialise la discipline harness engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (E4/E6/E8/E9-E14), correct-work (verdicts), arbitres du dépôt
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Statut** : stable
