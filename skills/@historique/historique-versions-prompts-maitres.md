# Historique des versions — Prompts maîtres et skills (écosystème Knowledge)

> **Version** : 1.0.0 — **Date** : 2026-10-11 (Task 16, session web-b93f42fa)
> **Objet** : historique consolidé des versions des prompts maîtres (3 familles) et des skills de l'écosystème — particularités du skill installé, améliorations implantées, avantages par rapport à la version précédente.
> **Directive propriétaire** : « plusieurs versions des prompts maitres → ne garder que la dernière version… historique dans skills/@historique/… sans augmenter la taille ni du prompt maitre, ni du dossier @mon-ecosysteme » (2026-10-11).
> **Sources** : tables §7 des PMs les plus récents (`PROMPT-MAITRE-GEN-PLAN-v3.21.0.md`, `PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md`, `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` — sources de vérité vivantes), SYNC-CONTEXT v1.4.1, PM-INSTALL v1.6.0 §7, registre KB (28 entrées), worklog de campagne.
> **Fait foi** : en cas de divergence, la table §7 du PM vivant de la famille prévaut sur la présente distillation (règle 4 du README du dossier).

## 1. Vue d'ensemble des 3 familles

| Famille | Skill installé | Versions documentées | Fichiers archivés ici | Version vivante (corpus) |
|---------|----------------|---------------------|----------------------|--------------------------|
| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 22 (v2.0.0 → v3.21.0) | 15 (v3.6.1 → v3.19.0) | v3.21.0 |
| CORRECT-WORK | correct-work — vérification/correction (5 étapes, 4 modes) | 10 (v1.0.0 → v2.7.0) | 4 (v2.4.0 → v2.6.0) | v2.7.0 |
| CLONE-CHAT | clone-chat — archivage de session (7+1 étapes, 8 checks) | 4 (v1.0.0 → v2.0.0) | 0 (v2.0.0 vit dès sa création) | v2.0.0 |

Versions documentées SANS fichier archivé : GEN-PLAN v2.0.0 → v3.6.0 (antérieures à la matérialisation du corpus, perdues aux wipes inter-sessions — changements tracés par les §7 successifs) et v3.20.0 (remplacée le jour même par v3.21.0) ; CORRECT-WORK v1.0.0 → v2.3.0 (même cause) ; CLONE-CHAT v1.0.0 → v1.2.0 (même cause). Les PMs CORRECT-WORK v2.6.0/v2.7.0 sont des RECONSTITUTIONS par diffs chirurgicaux (méthode B1, Task 16 session web-8a7e5653 — provenance tracée en tête de chaque PM, aucun faux lignage).

## 2. Famille GEN-PLAN — 22 versions (skill : gen-plan)

**Particularité durable du skill** : planification structurée pour assistant IA — 4 modes (Planification, Exécution, Surveillance, Adaptation), 15 étapes E1-E15, classification Type 1-4, 3 profils ressource (NORMAL/ECO/VIEUX PC), tagging #token, scripts Python uniquement (N3), disciplines d'ingénierie de prompts, hooks patterns avancés, règles d'or §1.8.

| Version | Date | Améliorations implantées (source §7 du PM v3.21.0) | Avantage par rapport à la version précédente |
|---------|------|---------------------------------------------------|----------------------------------------------|
| v2.0.0 | 2026-07-18 | Version initiale (refusée par l'utilisateur) | — (point de départ de la lignée) |
| v3.1.0 | 2026-07-18 | Refactoring complet suite au refus de v2.0.0 | Forme restructurée qui devient la base acceptée de toute la lignée |
| v3.3.0 | 2026-07-29 | Ajout du Registre KB et du Protocole de Découverte | gen-plan découvre les skills via le registre vivant au lieu d'un inventaire figé |
| v3.5.0 | 2026-07-29 | Intégration clone-chat, calibration #token, normes N1-N3 | Coût de chaque étape estimé en tokens ; conventions de nommage et de tagging normées |
| v3.6.0 | 2026-08-09 | Refactoring du prompt maître : extraction du socle commun SHARED | Déduplication : les informations communes vivent une seule fois dans SHARED (R4) |
| v3.6.1 | 2026-08-09 | Méthode lecture bloc par bloc (philosophie #7, E2/E9/E10), correct-work >= v2.4.0 avec hook E8, chemins references/ sans accent, description enrichie | Les fichiers volumineux sont couverts sans surcharge de contexte ; le plan est vérifié par correct-work dès sa création |
| v3.7.0 | 2026-08-30 | Règles d'or (§1.8 : adaptation autonome sur blocage), disciplines d'ingénierie de prompts (§1.9), hook correct-work par phase (E9-E14) | Tout blocage devient un signal d'adaptation au lieu d'un arrêt ; chaque phase exécutée est vérifiée avant la suivante |
| v3.8.0 | 2026-09-06 | Unification du schéma evals (skill-creator) au §5, pipeline d'optimisation Z0-Z6, idempotence R1-R6, matérialisation agent | Evals comparables entre exécutions (with_skill vs baseline) ; toute ré-exécution du pipeline est garantie sans effet de bord |
| v3.8.1 | 2026-09-06 | Description Optimization (itération-3 workspaces) : description frontmatter enrichie « classification Type 1-4 » | Déclenchement du skill 9/9 (au lieu de 8/9) — le cas « classe cette tâche » est couvert |
| v3.9.0 | 2026-09-06 | Réimplantation des disciplines : source de vérité déplacée vers SHARED §7, matérialisation des 4 disciplines d'exécution | Non-duplication (§6.3) : les disciplines sont réutilisables par tous les skills en fonction héritée |
| v3.10.0 | 2026-09-07 | Règle d'or n°2 (régénération du plan après installation d'un écosystème) et n°3 (mise à jour à chaque nouvelle demande) | Le plan suit l'écosystème installé et les demandes de l'utilisateur sans réécriture destructrice (extension R2) |
| v3.11.0 | 2026-09-10 | Intégration du Prompt Engineering Kit v4.1 : 3 modes de raisonnement (CoT/Chaining/Hybride), blocs de sortie A-J, 9 règles critiques, 12 checks + scoring | Couche de raisonnement adaptative calibrée par les profils ressource — la profondeur d'analyse s'ajuste à la complexité détectée |
| v3.12.0 | 2026-09-19 | Mobilisation disciplinaire complète (audit N5-a) : table de mobilisation E1-E8, relations étendues aux 4 disciplines | Chaque étape de planification a ses disciplines assignées explicitement — plus d'angle mort disciplinaire |
| v3.13.0 | 2026-09-19 | Hooks patterns avancés (phase N20) : answer key E1, arbitre answer-key-checker E7/E8 (16 checks), Graph Diamond E9-E14, knowledge-observer E15 | Les décisions de planification deviennent vérifiables mécaniquement ; la parallélisation exceptionnelle est tracée |
| v3.16.0 | 2026-09-26 | Re-curation B13 des leçons knowledge-observer : KO-L001 (économie API 429), KO-L003 (arbitres à invariants dynamisés), KO-L004 (recalibrage croisé) | Les leçons d'économie et d'anti-dérive des arbitres sont institutionalisées dans la méthode |
| v3.17.0 | 2026-09-27 | Règle KO-L005 (généralisation règle d'or n°2), hook E1-RES (lecture B-11 + collecte G-RES + fraîcheur du plan) | Le plan est re-généré à chaque version de gen-plan modifiée et jugée valide ; l'ouverture de session est instrumentée (ressources) |
| v3.17.1 | 2026-10-02 | Propagation du renommage du skill prompt-engineering (ex agent-prompt-engineering ; census 118 refs/32 fichiers) | Références opératives alignées sur le renommage — plus de pointeur mort vers l'ancien nom |
| v3.17.2 | 2026-10-02 | Déclencheur verbatim « intègre dans le plan d'actions » (E13, directive propriétaire), correction E1 vers le pipeline PM-INSTALL v1.1.0, trigger_evals 7 → 8 cas | L'intégration d'une nouvelle demande au plan courant devient sans ambiguïté (déclencheur verbatim) |
| v3.18.0 | 2026-10-02 | Application M4 de la leçon L007 (matérialisation d'abord — pièges sparse-checkout), YAML §4 synchronisé sur le frontmatter installé | Les faits de matérialisation sont établis AVANT toute écriture et tout verdict d'arbitre (anti-faux-verdict) |
| v3.19.0 | 2026-10-03 | Routage de découverte (Task 23) : skills-inventory prioritaire, fallback skill-finder-cn avec contrôle cybersécurité audit-provenance, bascule unidirectionnelle ; garde É1-INSTALL --check à l'ouverture | La découverte des skills est priorisée et comparée au registre ; l'écart d'installation est détecté avant tout travail |
| v3.20.0 | 2026-10-04 | Task 29 : script maître ensure-installed.py intégré au skill, mode --preempt (réinstallation immédiate si ROOT absent), directive post-réinstallation download/plan-post-reinstall-<ts>.json | La réinstallation est garantie idempotente et le plan en cours est mis à jour de façon cohérente après réinstallation |
| v3.21.0 | 2026-10-09 | Règle d'or n°4 : toute utilisation d'un élément du dépôt passe par un clone git local (shallow), jamais une lecture distante API/raw/web ; askpass éphémère, zéro persistance de jeton | Accès au dépôt fiable (rate-limiting API 403 contourné) et discipline de sécurité du jeton institutionnalisée — **VERSION VIVANTE (corpus)** |

Fichiers archivés de la famille : `prompts-maitres/gen-plan/` — v3.6.1, v3.7.0, v3.8.0, v3.8.1, v3.9.0, v3.10.0, v3.11.0, v3.12.0, v3.13.0, v3.16.0, v3.17.0, v3.17.1, v3.17.2, v3.18.0, v3.19.0 (15 fichiers, SHA-256 au §5).

## 3. Famille CORRECT-WORK — 10 versions (skill : correct-work)

**Particularité durable du skill** : vérification et correction de travaux pour assistant IA — 5 étapes, 4 modes (PROJET, CIBLE, AVEUGLE, + rapport), verdicts S1-S4, métriques de performance, checklists opérationnelles, hooks gen-plan (E8 + contrôle par phase E9-E14), arbitre verify-correct-work (16 checks).

| Version | Date | Améliorations implantées (source §7 du PM v2.7.0) | Avantage par rapport à la version précédente |
|---------|------|---------------------------------------------------|----------------------------------------------|
| v1.0.0 | 2026-07-18 | Version initiale, vérification basique | — (point de départ) |
| v2.0.0 | 2026-07-29 | Ajout du Mode CIBLE, amélioration du rapport | Vérification d'un élément précis en plus du projet entier ; rapport plus exploitable |
| v2.1.0 | 2026-07-29 | Intégration gen-plan à l'Étape 1 | Toute vérification s'appuie d'abord sur un plan structuré au lieu d'un balayage ad hoc |
| v2.2.0 | 2026-07-29 | Registre KB (gen-plan >= v3.3.0), kb_path, --kb-skill, matrice dynamique | Les vérifications consultent le registre vivant de l'écosystème (contexte à jour) |
| v2.3.0 | 2026-08-09 | Refactoring du prompt maître : extraction du socle commun SHARED | Déduplication : les informations communes vivent une seule fois dans SHARED (R4) |
| v2.4.0 | 2026-08-09 | Support multi-cibles, découplage gen-plan (mode autonome), métriques de performance, checklists opérationnelles (§4.6-§4.10), scripts/ + evals/, hook gen-plan E8, verify-cross --mode correct-work (8 checks KB) | Vérifications opérables même sans gen-plan présent, instrumentées (scripts + evals) et branchées sur le hook E8 de gen-plan |
| v2.5.0 | 2026-09-06 | Unification du schéma evals (skill-creator) au §5 (evals.json, trigger_evals.json, workspaces) | Evals comparables entre exécutions (with_skill vs baseline) — même référentiel que gen-plan |
| v2.5.1 | 2026-09-06 | Description Optimization (itération-3) : description frontmatter enrichie « erreurs, omissions, incohérences » | Déclenchement du skill 8/8 (au lieu de 6/8) — les cas « correction » et « omissions/incohérences » sont couverts |
| v2.6.0 | 2026-09-19 | 4e mode AVEUGLE (Second Opinion — re-vérification sans accès au premier verdict), hook 2nd opinion agent-driven à l'Étape 5 (inputs filtrés), maximum 2 rounds de correction par artefact | Le biais de confirmation est éliminé (le second verdict ne voit pas le premier) ; la boucle de correction est bornée (SHARED §4.4) |
| v2.7.0 | 2026-10-02 | Couplage gen-plan OBLIGATOIRE à l'Étape 1 (résolution dynamique de la dernière version installée) — fin du mode autonome ; ARRÊT EXPLICITE si gen-plan est indisponible ou corrompu ; §5.4 aligné sur la forme installée certifiée (7 cas trigger_evals) | Cohérence méthodologique garantie : toute vérification est planifiée par gen-plan, jamais improvisée — **VERSION VIVANTE (corpus)** |

Révisions documentaires de la famille (sans changement de version) : session A11 2026-09-06 (§B pointeur disciplines → SHARED §7) ; Task 16 2026-10-02 (v2.6.0 et v2.7.0 RECONSTITUTIONS par diffs chirurgicaux méthode B1 — `scripts/materialise-pm-correct-work.py` — les originaux perdus au wipe, provenance tracée en tête de PM, aucun faux lignage) ; Task 14 2026-10-10 (§2.6/§9.2/§10.1 alignés sur le SKILL.md v2.7.0 certifié, corruption « ode] » réparée, calibration de forme).
Fichiers archivés de la famille : `prompts-maitres/correct-work/` — v2.4.0, v2.5.0, v2.5.1, v2.6.0 (4 fichiers, SHA-256 au §5).

## 4. Famille CLONE-CHAT — 4 versions (skill : clone-chat)

**Particularité durable du skill** : archivage de session en document-cloné auto-suffisant — 7+1 étapes, intégralité du contexte (décisions, artefacts, worklog), format Markdown unique, propriété d'auto-clonage, reprise par session héritière.

| Version | Date | Améliorations implantées (source §7 du PM v2.0.0) | Avantage par rapport à la version précédente |
|---------|------|---------------------------------------------------|----------------------------------------------|
| v1.0.0 | 2026-07-29 | Version initiale : 7 étapes, template, auto-clonage | — (point de départ) |
| v1.1.0 | 2026-07-29 | 8 corrections correct-work (§0-§5, #token, chemins) | Conformité vérifiée par correct-work dès la première lignée (seuil in extenso, chemins relatifs, alignement SKILL.md ↔ template) |
| v1.2.0 | 2026-07-29 | Étape 3.5 Context Drift, 5 types de dérive, 8 checks, gen-plan KB | La dérive de contexte est détectée et typée à l'archivage au lieu d'être découverte à la reprise |
| v2.0.0 | 2026-08-09 | Harmonisation écosystème maître : gen-plan v3.6.0, correct-work v2.3.0, 78 skills, variables SHARED, dependencies frontmatter, worklog SHARED §1.4, prompt maître | Le clone est aligné sur tout l'écosystème (variables, dépendances, worklog) — reprise par session héritière fiable — **VERSION VIVANTE (corpus)** |

Révisions documentaires de la famille (sans changement de version du skill) : révisions du PROMPT 1.0.1 / 1.0.2 / 1.0.3 (2026-09-05 → 2026-09-06 — toilettage de cohérence §6, correction de références internes, complétude du template §9.1 bloc « §1.0 Héritage — chaîne de clonage » ; Task 21 observation S4 ; la version du skill reste v2.0.0).
Fichiers archivés de la famille : aucun (v2.0.0 est la version vivante depuis sa création — la lignée v1.x n'a jamais été matérialisée au corpus).

## 5. Index des fichiers sources archivés (19 PMs — sceau SHA-256)

Déplacés du corpus `skills/@mon-ecosysteme/` vers le présent dossier par `git mv` (Task 16, 2026-10-11) — byte-identité prouvée contre les blobs du commit de référence `b36f177` (script `/home/z/my-project/scripts/task16-move-pms.py`, all-or-nothing, garde anti-homonyme R4). Table complète au rapport `download/rapport-task16-corpus-pms-historique-reinstallation.md`.

| Fichier archivé | SHA-256 |
|-----------------|---------|
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md | 6356ae3efe09522a8c6802147cfc88b0e0e58875b2dd3443d84a378395565ef6 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.7.0.md | e053f0ae7ccde425f7f15d84ab263738637a442e48c9e245824a9b32656b8880 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.8.0.md | 25ee244df6a790c02366a57617f2b5ee8ba80b2e3b931d963b7e06b53beef190 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.8.1.md | 69addcc9b1ef060ed348022b4753eccf2a160c6b66b38d946b8f5e49dd144ad9 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.9.0.md | a3c2fafaae6167b7a971a3120029349fca53f3d77c9eb9c3451108c597d82aee |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.10.0.md | aade3e718746827c4a0380d7e2a07bfa40cc4a07d989053f9c8b4696e485613d |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.11.0.md | bde9d5b5fab39647c78c020ef959640e17b52dd6d7a33d6844de1eda8e1c5a94 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.12.0.md | 55cb53dd8871a8bbfb2935976927d8232a79197610fcdae690d57869551f2a81 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.13.0.md | e9bdcfa56570a499a6ac35f0e40beb2b31d25db7ca5fa8c323137f48cdd08d97 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.16.0.md | 9baf0a2f10b4e0bf07d469ade7b9a23917974f3fb2b1d5c922e04787cf696aec |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.17.0.md | 1188c0ea067de8fbaa6e420268464f021014948a2cecfa1cb8ebdb1300d3b692 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.17.1.md | 31139a0738dcdc4faf513a28626d60a789dd2db88493e5931ccc99e645cda44d |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.17.2.md | 45f7e71989f44b85530a689580b969c78b6b33d009d9ab5e910c839f86d5dbe6 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.18.0.md | 65b68b2d7f423e280fa6353dd375e6d8b512043299166491a3cbbf8d44d32cc9 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.19.0.md | df6a59c04d02bc932ceb2d9bac48629ea073f8ca788df2e3af5fbf3a1db5103b |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md | 16f82edb358ce36cfffbbfb9058ffda4d1d8a1e7d144791f11cbc82f67b60063 |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.5.0.md | 8dfc29a77633502609abc7a1d68a73cf53be40be7a7d5a6fd2670d1a40bfb8cf |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md | 9b3fad20a188aeb95a21cf251fb71a36a9a4b038bbb8a1fff96599f4adfba0b5 |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.6.0.md | 45dfedb4812e74304310300947bfe2bca65b4da3f3c94c01d58c18b9a9c15209 |

## 6. Instantané des versions des skills (source : registre KB, 2026-10-11)

Archive datée de l'état installé à la date de création de ce dossier — le registre KB `skills/KNOWLEDGE.md` reste la source de vérité vivante (28 entrées). Les versions des 3 familles = versions de leurs PMs vivants (contrat KO-L004 : SKILL.md frontmatter = source de vérité).

| Skill | Version | Skill | Version |
|-------|---------|-------|---------|
| gen-plan | v3.21.0 | audit-provenance | v1.1.0 |
| correct-work | v2.7.0 | autonomous-agent | v1.1.0 |
| clone-chat | v2.0.0 | correct-py | v1.1.0 |
| skills-inventory | v1.1.0 | fleet-engineering | v1.0.0 |
| skill-creator | v1.1.0 | memory-engineering | v1.1.0 |
| agent-creator | v2.1.0 | spec-driven-development | v1.0.0 |
| prompt-engineering | v2.2.0 | audio-metadata | v1.1.0 |
| context-engineering | v1.1.0 | cpp-analysis | v1.1.0 |
| loop-engineering | v1.1.0 | pdf-llm | v1.0.0 |
| graph-engineering | v1.0.1 | resource-monitor | v1.0.0 |
| harness-engineering | v1.1.0 | version-management | v1.2.0 |
| script-mon-ecosysteme-infrastructure | v1.1.0 | skill-finder-cn | v1.0.0 |
| knowledge-observer | v1.0.0 | vue-upload | v1.2.0 |
| script-creator | v1.1.0 | script-reviewer | v1.0.0 |

## 7. Mise à jour de ce dossier

Procédure normative au `README.md` du présent dossier (§4) : à chaque montée de version d'une famille — génération mécanique du nouveau PM (KO-L004 §2quater PM-INSTALL), `git mv` du PM supplanté vers `prompts-maitres/<famille>/`, byte-identité SHA-256 prouvée, ligne ajoutée à la table de sa famille ci-dessus, index §5 rafraîchi, recalibrage croisé KO-L004 et sweep arbitres avant tout commit.
