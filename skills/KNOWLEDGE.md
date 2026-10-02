# KNOWLEDGE.md — Registre central de l'écosystème Knowledge

> Source de vérité des versions et des relations (README §4 / SHARED §2).
> Format des entrées : template SHARED §2.2. Mise à jour à chaque matérialisation (gen-plan E15).

## gen-plan v3.18.0

- **Category** : ecosystem
- **Description** : Planification structurée des tâches — 4 modes, 15 étapes E1-E15, classification Type 1-4 (E3), règles d'or §1.5 (n°1 adaptation autonome, n°2 régénération post-installation, n°3 mise à jour à chaque nouvelle demande — déclencheur verbatim « intègre dans le plan d'actions » v3.17.2), disciplines d'ingénierie §1.6 (source de vérité : SHARED §7 ; mobilisation E1-E8), méthode de raisonnement adaptative PEK v4.1 (3 modes, blocs A-J, 9 règles, 12 checks), hooks patterns avancés §1.2bis (answer key obligatoire E1, arbitre answer-key-checker E7/E8, Graph Diamond E9-E14, knowledge-observer E15), leçons knowledge-observer §1.14/§1.15 (KO-L001 économie API, KO-L003 arbitres à invariants dynamisés, KO-L004 recalibrage croisé, KO-L005 généralisation règle d'or n°2 — §1.5, KO-L007 matérialisation d'abord sur clone sparse — v3.18.0) ; hook E1-RES §1.2bis (n67-1 reconstitué post-wipe : B-11 + collecte G-RES + fraîcheur du plan)
- **Dépend de** : correct-work >= v2.4.0 (hooks E9-E14), clone-chat >= v2.0.0 (E4, E15, optionnel), skills-inventory >= v1.0.0 (E5), prompt-engineering >= v1.0.0 (délégation §1.9), resource-monitor >= v1.0.0 (hook E1-RES — collecte G-RES, v3.17.2), context-engineering (mobilisation §1.6), loop-engineering (mobilisation §1.6), graph-engineering (mobilisation §1.6), harness-engineering (mobilisation §1.6), knowledge-observer >= v1.0.0 (E15)
- **Utilisé par** : correct-work (Étape 1, OBLIGATOIRE — dernière version installée, v2.7.0), clone-chat (optionnel), agent-creator, Main (planification complète), prompt-engineering (contexte écosystème, E1-E8), knowledge-observer (invoqué à E15, modes M1-M2)
- **Dernière calibration** : 2026-09-10 (révision B3 : harmonisation bidirectionnelle du registre — réciproques « Utilisé par » clone-chat, prompt-engineering ; révision B1 : intégration PEK v4.1 par assemblage — couche de raisonnement adaptative, 6e référence prompt-engineering-kit.md, PM v3.11.0 ; A12 : règles d'or n°2-n°3, directive utilisateur ; A11 : disciplines implantées en SHARED §7, triggers 9/9) ; N14-b (2026-09-19) : re-montée v3.12.0 — table de mobilisation E1-E8 §1.6, relations §3 étendues aux 4 disciplines, E1/E5/E7/E8, porteurs propagés) ; B13-r5 (2026-09-26) : re-curation leçons KO (§1.14/§1.15), hooks §1.2bis, reconstitution post-wipe (trace 1a0dfca3a0ffe13d) ; N23-b/N28 (2026-09-27, B13-r6) : montée v3.17.0 — §1.5 bloc PATTERN:KO-L005-v1.0.0 (leçon L005 validée), §1.2bis hook E1-RES (n67-1 reconstitué, provenance tracée), PM v3.17.0 assemblé 1362 L déployé ×3, arbitre n60b 12/12 ×2 ; montée v3.17.1 (2026-10-02, trace a91dd80) : propagation renommage prompt-engineering — patterns-avances-qwen.md (mode M5), PM v3.17.1 assemblé et déployé ×3, recalibrage KO-L004 (integrité, corpus 22, SYNC_MAP 12), arbitres re-certifiés ; montée v3.17.2 (2026-10-02) : déclencheur verbatim « intègre dans le plan d'actions » (§A PM + règle d'or n°3 + trigger_evals 8 cas), correction E1 → PM-INSTALL v1.1.0 (fusion installateurs), recalibrage KO-L004 (CORPUS_ATTENDU 22, SYNC_MAP 12) ; montée v3.18.0 (2026-10-02) : application M4 leçon L007 (verdict correct-work étape F PASS, cycle fusion installateurs) — §1.15 PATTERN:KO-L007-v1.0.0, PM v3.18.0 déployé ×3, §4 exemplaire YAML synchronisé, recalibrage KO-L004 (CORPUS_ATTENDU 24, SYNC_MAP 14)
- **Statut** : stable

## correct-work v2.7.0

- **Category** : ecosystem
- **Description** : Vérification et correction des livrables (erreurs, omissions, incohérences) — 4 modes (PROJET/CIBLE/DIRECT/AVEUGLE), 5 étapes, multi-cibles, couplage gen-plan OBLIGATOIRE (Étape 1, dernière version installée), checklists unifiées §10, hook 2nd opinion agent-driven (Étape 5)
- **Dépend de** : gen-plan >= v3.7.0 (Étape 1, OBLIGATOIRE — dernière version installée, v2.7.0), clone-chat >= v2.0.0 (Mode CIBLE, §3.5), fullstack-dev >= v1.0.0 (projets web), skills-inventory >= v1.0.0 (scan dynamique KB)
- **Utilisé par** : gen-plan (hooks par phase E9-E14), clone-chat (validation croisée), Main (vérification finale), knowledge-observer (validation des lessons, étape F), script-creator (GF-5, mode CIBLE sur les scripts produits), script-reviewer (sévérités S1-S4, escalade CIBLE), audit-provenance (GF-4, validation des artefacts corrigés)
- **Dernière calibration** : 2026-10-02 (v2.7.0 : couplage gen-plan obligatoire à l'Étape 1, fin du mode autonome — directive propriétaire ; recalibrage arbitre KO-L004) ; 2026-09-10 (révision B3 : harmonisation bidirectionnelle du registre — réciproque « Utilisé par » clone-chat, dépendance skills-inventory (scan dynamique KB) ; A10 : Description Optimization « erreurs, omissions, incohérences », itération-3 triggers 8/8 ; A9 : schéma evals unifié)
- **Note v2.0 (corrige-ecosysteme)** : règles de cross-references décentralisées (SHARED §3.2 → §3.2) — Contexte Système appliqué (Architecture v2.0). ; N27/N28 (B13-r6) : provenance tracée — `verify-correct-work.py` documenté par en-tête `PROVENANCE:` (audit audit-provenance, 25 scripts), réciproques script-creator/script-reviewer/audit-provenance complétées.
- **Statut** : stable

## clone-chat v2.0.0

- **Category** : ecosystem
- **Description** : Clonage de discussion en Markdown auto-suffisant — protocole 7+1 étapes, 8 checks, 5 types de drift, protocole d'héritage §1.0, compatibilité ascendante (révision prompt 1.0.3)
- **Dépend de** : gen-plan >= v3.6.1 (optionnel), correct-work >= v2.4.0 (validation croisée), skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : gen-plan (E15, archivage — leçon E23), correct-work (Mode CIBLE, §3.5), agent-creator (persistance d'état)
- **Dernière calibration** : 2026-09-10 (révision B3 : harmonisation bidirectionnelle du registre — réciproque « Utilisé par » correct-work ; 10ᵉ clone scellé 776ff9c0…, révision prompt 1.0.3)
- **Note v2.0 (corrige-ecosysteme)** : aucune section décentralisée ; relation G8 (persistance agent-creator) documentée bidirectionnellement (SHARED §3.1) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## skills-inventory v1.0.0

- **Category** : ecosystem
- **Description** : Scan et inventaire des skills disponibles (E5 de gen-plan)
- **Dépend de** : —
- **Utilisé par** : gen-plan (E5), correct-work (scan dynamique KB)
- **Dernière calibration** : N/A
- **Note v2.0 (corrige-ecosysteme)** : template des entrées KB (SHARED §2.2 → §2.1) + Protocole de Découverte (SHARED §2.3 → §2.2) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## skill-creator v1.0.0

- **Category** : ecosystem
- **Description** : Création et gestion de skills (conventions structurelles)
- **Dépend de** : —
- **Utilisé par** : clone-chat (conventions), prompt-engineering (création), script-mon-ecosysteme-infrastructure v1.1.0 (conventions + évals — INFRA-1/2/3), knowledge-observer (application des mises à jour), script-creator v1.0.0 (conventions), script-reviewer v1.0.0 (conventions)
- **Dernière calibration** : N/A
- **Note v2.0 (corrige-ecosysteme)** : conventions YAML (SHARED §1.3 → §2), format SKILL.md (SHARED §5 → §3), règle impérative Contexte Système (§3.0) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## agent-creator v2.0.0

- **Category** : ecosystem
- **Description** : Agent autonome avec mémoire interne (tâches longues)
- **Dépend de** : gen-plan >= v3.6.0, clone-chat >= v2.0.0 (persistance, optionnel)
- **Utilisé par** : —
- **Dernière calibration** : N/A
- **Note v2.0.0 (B11)** : renommage effectué depuis l'ancien identifiant (bump majeur — rupture d'identité assumée, plan B11 Phase A ; écosystème adapté de manière idempotente : évals, arbitres, corpus actif, harness, véhicule de réinstallation).
- **Statut** : stable

## prompt-engineering v2.1.0

- **Category** : ecosystem
- **Description** : Optimisation fine des prompts complexes (rédaction, restructuration, évaluation, itération — 4 modes M1-M4) + mode M5 IDÉATION (ToT, protocole ideation-protocol.md). Spécialise la méthode prompt-engineering (méthode-mère : gen-plan ; source de vérité : SHARED §7)
- **Dépend de** : gen-plan >= v3.7.0 (contexte écosystème, E1-E8), skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : gen-plan (délégation §1.9), install-ecosystem (P6-P7)
- **Dernière calibration** : 2026-09-06 (MATÉRIALISÉ : SKILL.md + evals/evals.json + evals/trigger_evals.json + references/grille-evaluation-prompt.md ; A11 : pointeurs SHARED §7, v1.0.1)
- **Note v2.0.0 (B11)** : renommage effectué depuis l'ancien identifiant (bump majeur — rupture d'identité assumée, plan B11 Phase A ; écosystème adapté de manière idempotente : évals, arbitres, corpus actif, harness, véhicule de réinstallation).
- **Statut** : stable

## context-engineering v1.1.0

- **Category** : ecosystem
- **Description** : Discipline context engineering (curation de contexte, compaction, clairage juste-à-temps, mémoire externe, budget d'attention). Spécialise la discipline context engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (couche disciplines E2/E5/E9-E14), sessions d'ingénierie
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Note v2.0 (corrige-ecosysteme)** : registre d'assignation des disciplines (SHARED §7 → §8) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## loop-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline loop engineering (boucle d'exécution, boucle de vérification avec graders, boucle externe d'amélioration continue). Spécialise la discipline loop engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (couche disciplines E10-E15), correct-work (hooks de vérification), sessions d'ingénierie
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Note v2.0 (corrige-ecosysteme)** : registre d'assignation des disciplines (SHARED §7 → §8) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## graph-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline graph engineering (graphe de connaissances, nœuds/arêtes versionnés, requêtes ancrées KB, anti-hallucination). Spécialise la discipline graph engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (E5/E15), correct-work (scan dynamique KB), sessions d'ingénierie
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Note v2.0 (corrige-ecosysteme)** : registre d'assignation des disciplines (SHARED §7 → §8) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## harness-engineering v1.0.1

- **Category** : ecosystem
- **Description** : Discipline harness engineering (harnais d'exécution, gardes-fous, profilage ressource, arbitres, resserrage après dérive). Spécialise la discipline harness engineering (source de vérité : SHARED §7)
- **Dépend de** : — (socle normatif SHARED §7)
- **Utilisé par** : gen-plan (E4/E6/E8/E9-E14), correct-work (verdicts), arbitres du dépôt
- **Dernière calibration** : 2026-09-07 (heuristique v2 — stemmer français léger sous garde de collision ; itération-6 : 4/4 v1 et v2, +1 gain v2 ; SKILL.md + evals/evals.json + evals/trigger_evals.json ; agents `_disciplines/` retirés, SHA prouvés)
- **Note v2.0 (corrige-ecosysteme)** : registre d'assignation des disciplines (SHARED §7 → §8) — Contexte Système appliqué (Architecture v2.0).
- **Statut** : stable

## script-mon-ecosysteme-infrastructure v1.1.0

- **Category** : ecosystem (infrastructure)
- **Description** : Infrastructure de génération de fichiers — injection automatique du Contexte Système à 3 niveaux (N1 prompts maîtres, N2 skills/agents, N3 scripts), gardes d'intégrité, idempotence
- **Dépend de** : skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : install-ecosystem (P6-P7), corrige-ecosysteme (Phases C et I)
- **Note v2.0 (corrige-ecosysteme)** : matérialisé en SKILL.md v1.1.0 (Phase I1 — règles INFRA-1/2/3) — Contexte Système appliqué (Architecture v2.0).
- **Dernière calibration** : 2026-09-14 (corrige-ecosysteme v2.0.0 — matérialisation locale)
- **Statut** : stable

## knowledge-observer v1.0.0

- **Category** : ecosystem
- **Description** : Skill d'observation automatique des sessions pour détecter les patterns d'erreur et améliorer les skills de l'écosystème. Cycle A-H (Task Observer), 4 modes M1-M4 (observation, analyse, proposition, application), journal lessons-learned, propositions idempotentes validées par correct-work
- **Dépend de** : gen-plan >= v3.13.0 (E15, analyse post-session), correct-work >= v2.6.0 (validation des lessons, étape F), skill-creator >= v1.0.0 (application des mises à jour)
- **Utilisé par** : gen-plan (hook E15, modes M1-M2), audit-provenance (leçon L006 — journal lessons-learned)
- **Dernière calibration** : 2026-09-19 (N20 : matérialisation du pattern Task Observer — SKILL.md + evals/evals.json + evals/trigger_evals.json + data/lessons-learned.json ; source de vérité du pattern : gen-plan/references/observation-patterns.md) ; 2026-09-26 (B13-r5 : restauration post-wipe — journal L001-L004 restitué, référence observation-patterns.md restaurée)
- **Statut** : stable

## script-creator v1.0.0

- **Category** : ecosystem
- **Description** : Création et modification des scripts de l'écosystème (arbitres, collecteurs, outils de vérification stdlib) avec critères de succès et tests mécaniques intégrés ; idempotence rejeu ×2 (rejeu ×2 sans effet)
- **Dépend de** : skill-creator >= v1.0.0 (conventions de description/évals/frontmatter), correct-work >= v2.6.0 (validation mode CIBLE), correct-py >= v1.0.0 (post-traitement GF-6 — exécuté après chaque utilisation)
- **Utilisé par** : script-reviewer v1.0.0 (scripts entrants du processus de création), audit-provenance v1.0.0 (conventions des scripts produits)
- **Dernière calibration** : 2026-09-27 (N25, B13-r6 : ajout au registre — verdict correct-work mode CIBLE round 1 **PASS AVEC RÉSERVES** [1 S2 : entrées KB absentes ; 3 S3 cross-refs] ; test simple de bout en bout §1.2 PASS avec preuve d'idempotence ×2 ; corrections des réserves appliquées R2 idempotentes)
- **Note N25 (B13-r6)** : famille skill-creator ; processus §1.2 en 7 étapes + 6 garde-fous (R9, N3, idempotence ×2, auto-test P2, correct-work CIBLE, correct-py GF-6) ; evals 4 + trigger_evals 7 en base réelle ; relations bidirectionnelles complétées (script-reviewer §3).
- **Statut** : stable

## script-reviewer v1.0.0

- **Category** : ecosystem
- **Description** : Relecture et validation des scripts de l'écosystème avant adoption : grille de relecture en 8 checks mécaniques (G1-G8), sévérités S1-S4 alignées correct-work, verdict PASS / PASS AVEC RÉSERVES / FAIL, preuve d'idempotence ×2
- **Dépend de** : script-creator >= v1.0.0 (scripts entrants du processus de création), correct-work >= v2.6.0 (sévérités S1-S4, escalade mode CIBLE), skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : —
- **Dernière calibration** : 2026-09-27 (N26, B13-r6 : homologation au véhicule d'intégrité — archive v2.1 `homologues/skills/script-reviewer/` SKILL.md + evals + references ; clone épinglé `d9ff9fb`, restauration B13-r4)
- **Note N26 (B13-r6)** : homologue de la famille agent-creator ; pendant « relecture » de script-creator ; référencée au registre (décision N26).
- **Statut** : stable

## audit-provenance v1.0.0

- **Category** : ecosystem
- **Description** : Audit de la provenance des artefacts de l'écosystème (traçabilité d'origine : session, directive, clone épinglé, reconstitution post-wipe), détection des orphelins et réécriture idempotente des en-têtes manquants — matérialise la leçon L006
- **Dépend de** : knowledge-observer >= v1.0.0 (journal lessons-learned L006), script-creator >= v1.0.0 (conventions des scripts produits), correct-work >= v2.6.0 (validation mode CIBLE)
- **Utilisé par** : —
- **Dernière calibration** : 2026-09-27 (N27, B13-r6 : matérialisation — SKILL.md + evals 4+7 + collecteur scripts/audit-provenance.py ; audit exécuté : 214 scannés, 189 tracés, 25 scripts documentés, idempotence ×2 no-op prouvée)
- **Note N27 (B13-r6)** : déclencheurs systématiques — après wipe/restauration, avant clone-chat, avant installation ; périmètre écosystème strict (ECO_SKILLS dynamique) ; heuristique déclarative extensible (--markers) ; orphelins résiduels 33 assumés v1.0.0 (GF-3 — listés au rapport).
- **Statut** : stable

## audio-metadata v1.0.0

- **Category** : metier
- **Description** : Gestion avancée des métadonnées audio — extraction, normalisation, conversion de tags ID3v2, MP4, FLAC, Vorbis ; formats DJ (MP3, FLAC, WAV, AIFF, M4A)
- **Dépend de** : —
- **Utilisé par** : Main (gestion de collections audio)
- **Note P-H (2026-10-02)** : entrée créée pour compléter la bidirectionnalité registre↔skills (gap S3 préexistant à 68ff91d, résolu)
- **Statut** : stable

## cpp-analysis v1.0.0

- **Category** : metier
- **Description** : Analyse de code C/C++ — détection de bugs, optimisation de performance, analyse de complexité, génération de documentation ; support C à C++20
- **Dépend de** : —
- **Utilisé par** : Main (analyse de code C/C++)
- **Note P-H (2026-10-02)** : entrée créée pour compléter la bidirectionnalité registre↔skills (gap S3 préexistant à 68ff91d, résolu)
- **Statut** : stable

## pdf-llm v1.0.0

- **Category** : metier
- **Description** : Extraction documentaire PDF vers Markdown + JSON structuré RAG-ready — 4 modes (qwen/glm/multi/pipeline), zéro hallucination ; déclencheurs RAG, vectorisation, OCR
- **Dépend de** : —
- **Utilisé par** : Main (extraction documentaire PDF)
- **Note P-H (2026-10-02)** : entrée créée pour compléter la bidirectionnalité registre↔skills (gap S3 préexistant à 68ff91d, résolu)
- **Statut** : stable

## resource-monitor v1.0.0

- **Category** : ecosystem
- **Description** : Surveillance permanente des ressources de l'écosystème — collecte des indicateurs critiques (budget #token, timeouts consécutifs, disque, RAM), verdicts OK/PRESSION/CRITIQUE → mode d'exécution
- **Dépend de** : —
- **Utilisé par** : gen-plan (hook E1-RES — collecte G-RES, §1.2bis), Main (surveillance permanente §1.14)
- **Note P-H (2026-10-02)** : entrée créée pour fermer la boucle bidirectionnelle E1-RES : gen-plan « Dépend de » resource-monitor ↔ resource-monitor « Utilisé par » gen-plan (réciprocité SHARED §3.1)
- **Statut** : stable

## version-management v1.0.0

- **Category** : metier
- **Description** : Gestion du cycle de vie complet des projets front-end (versionnement par send_file/meta.json, historique, restauration, bascule de projets) — skill brut d'origine (description en chinois), version normalisée Z1 au frontmatter
- **Dépend de** : —
- **Utilisé par** : Main (projets web front-end)
- **Note P-H (2026-10-02)** : entrée créée pour compléter la bidirectionnalité registre↔skills ; frontmatter normalisé minimale (version: 1.0.0 ajoutée — le corps reste inchangé, R2)
- **Statut** : stable

## Décisions d'architecture (corrige-ecosysteme v2.0.0)

- **Task 14 — déduplication download/ (décision v2.2)** : exécution approuvée (directive utilisateur « vérifie qu'il n'existe pas de doublons (même nom, même contexte, idempotent) … si c'est le cas, effacer ceux du dossier download/ », session web-8a7e5653, 2026-10-02) — le canal de fichiers `download/` est SUPPRIMÉ : les 14 fichiers corpus répliqués dans `download/` (byte-identiques à `skills/@mon-ecosysteme/`) sont effacés ; l'archive `mon-ecosysteme_archive.zip` (véhicule d'intégrité **v2.2**, round-trip 24/24) devient l'UNIQUE voie de diffusion du corpus ; `scripts/sync-download.py` retiré (→ `scripts/_archive/`) et remplacé par la garde `scripts/task14-scan-doublons.py` (0 doublon attendu, critère « même nom + byte-identique ») ; recalibrage croisé KO-L004 : PM-INSTALL v1.3.0 (étape 9 recentrée archive), SHARED v1.6.3 (§6.1 + doctrine harness), SYNC-CONTEXT v1.4.0 (une voie de diffusion), README v2.1.0, orchestrateur ULTRA régénéré (SHA 9e21cf6a), arbitres inversés (check 3 integrity + §7/§11d interactions) ; résorption des réserves héritées : evals skill-creator (5 evals + 8 triggers, en) et version-management (5 evals + 8 triggers, zh) équipés, orchestrateur certification recalibré (parseur B8+). Les artefacts de session NON corpus (clones, rapports, plans — noms distincts) restent légitimes dans `download/`.
- **G9 — agent-lifecycle** : non créé (décision documentée). Le cycle de vie des agents est couvert par agent-creator §6.3 (AG-1/AG-2/AG-3 : création, enregistrement KB, gardes) et SHARED §4.3-§4.4 (droits + gardes anti-boucle) ; un skill dédié dupliquerait ce périmètre (règle R4 anti-duplication). À réévaluer si un 3ᵉ cas d'usage de cycle de vie apparaît.
- **G8 — clone-chat → agent-creator** : relation confirmée bidirectionnelle (SHARED §3.1 « agent-creator persist via clone-chat » + KB : clone-chat « Utilisé par » / agent-creator « Dépend de »). Aucun enrichissement supplémentaire requis.
- **N19 — patterns avancés Qwen (Answer Key, Graph Diamond, ToT, Second Opinion, Task Observer)** : intégration additive idempotente approuvée (demande n°33, session B12-r40) — références `skills/gen-plan/references/patterns-avances-qwen.md` + premier registre réel `references/answer-key-b12.md` (10 décisions B12, 10/10 verified) ; source : `download/propositions-qwen.md` (extraction discussion Qwen 2026-09-12) ; hooks obligatoires (E1 answer key, arbitre dédié, mode M5) ARBÉTRÉS phase N20 (montée v3.12.0 → v3.13.0, propagation ×3 voies + re-calibrage arbitres) — R2 : aucune rétrogradation, v3.12.0 demeure la version installée certifiée.
- **N20 — hooks patterns avancés (montée gen-plan v3.12.0 → v3.13.0)** : intégration cohérente approuvée (demande n°34, session B12-r41) — §1.2bis (answer key obligatoire E1, arbitre answer-key-checker.py 16 checks E7/E8, Graph Diamond E9-E14, knowledge-observer E15) ; 5 références N20 (answer-key-template, graph-diamond-pattern, observation-patterns, ideation-protocol, verification-protocol) ; correct-work v2.6.0 (4e mode AVEUGLE + hook 2nd opinion) ; prompt-engineering v2.1.0 (mode M5 IDÉATION) ; SHARED §8 règles fondamentales. Reconstituée B13-r5 post-wipe (trace 1a0dfca3a0ffe13d).
- **N25/N26 — famille script-creator au registre + homologues archive (B13-r6)** : intégration additive approuvée (directives `1a0def365a639149` / `1a0df0297431ea3d`, session B13-r6) — (a) entrées KB script-creator v1.0.0 + script-reviewer v1.0.0 (R2, 13 → 15 entrées versionnées, recalibrage croisé integrity L004 : ECO_SKILLS 15, check 5, docstring) ; (b) archive `mon-ecosysteme_archive.zip` étendue v2.1 : homologues/ agent-creator + script-reviewer (clone épinglé `d9ff9fb`) + PROVENANCE-homologues.md, arbitre integrity check 2 recalibré « corpus ⊆ archive + extras sous homologues/ » (bijection stricte levée) ; (c) verdict correct-work(script-creator) mode CIBLE round 1 : PASS AVEC RÉSERVES → corrections des réserves (F-1/F-2/F-3 cette décision, F-4 consignée — résolu au niveau KB, source de vérité) ; R2 : aucune entrée existante modifiée ou supprimée.
- **N27 — audit de provenance (B13-r6)** : matérialisation approuvée (directive `1a0df36f356c3add`, session B13-r6) — skill audit-provenance v1.0.0 (SKILL.md + evals 4+7 + collecteur `scripts/audit-provenance.py` stdlib) ; leçon **L006** au journal (statut appliqué, occurrences 3, matérialisation M4 exécutée) ; audit réel : périmètre écosystème strict 214 artefacts (adaptation R-RES3 : périmètre initial débordant corrigé en vol), 189 avec provenance, **25 scripts orphelins documentés** (en-tête `PROVENANCE:` syntaxe-safe, garde par marqueur), idempotence ×2 prouvée (no-op au 2e passage, sha16 `ded19f62…`), 33 orphelins résiduels listés au rapport v1.0.0 (limite heuristique assumée GF-3) ; KB 16 entrées versionnées (recalibrage croisé integrity L004 + interactions).
