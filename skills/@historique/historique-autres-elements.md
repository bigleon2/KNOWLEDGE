# Historique des autres éléments — socle `@mon-ecosysteme/` (hors familles à PM)

> **Version** : 1.0.0 — **Date** : 2026-10-11 (Task 17-B, session web-b93f42fa — directive propriétaire « un fichier historique pour les autres éléments de @mon-ecosysteme/ »)
> **Périmètre** : les éléments du socle sans famille de prompt maître dérivé — `PROMPT-MAITRE-SHARED.md`, `SYNC-CONTEXT.md`, `README.md`, `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md`, `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md`, registre KB. Les 3 familles à PM (gen-plan, correct-work, clone-chat) ont leurs historiques dédiés dans `historiques-par-skill/`.
> **Sources de vérité vivantes** : l'en-tête Révision de chaque fichier (SHARED, SYNC-CONTEXT, README) et SYNC-CONTEXT pour la mécanique ; le présent fichier en est l'archive documentaire — en cas de divergence, l'en-tête vivant fait foi.

## 1. PROMPT-MAITRE-SHARED.md (socle commun — source de vérité des blocs CONTEXTE SYSTÈME)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.4.0 | 2026-09-06 | Matérialisation des 4 disciplines d'exécution en skills complets à déclenchement automatique (levée réserve A11) ; §1.2 matérialisations agent `_disciplines/` retirées |
| v1.5.0 | 2026-09-06 | §7 heuristique de déclenchement v2 (stemmer français — radicalisation sous garde de collision, itération-6 : 40/40, 0 faux positif) |
| v1.5.1 | 2026-09-06 | §1.2 codification du renommage `_prompts-maitres/` → `mon-ecosysteme/` (session A17, commit 6995823) |
| v1.5.2 | 2026-09-06 | §1.2 codification du préfixe « @ » — `mon-ecosysteme/` → `@mon-ecosysteme/` (session A20, commit 1519bbe) |
| v1.6.0 | 2026-09-19 | §8 Règles Fondamentales (4 règles Karpathy adaptées, phase N20 — session B12-r41) |
| v1.6.1 | 2026-10-02 | PM-INSTALL source d'installation UNIQUE v1.1.0 (fusion installateurs, R4) ; §1.2 miroir `_prompts-maitres/` supprimé |
| v1.6.2 | 2026-10-02 | Référence PM-INSTALL v1.2.0 (dérivation dynamique 3 familles + garde anti-rétrogradation R2) |
| v1.6.3 | 2026-10-02 | Référence PM-INSTALL v1.3.0 (décision d'architecture v2.2 — canal download/ supprimé) |
| v1.6.4 | 2026-10-02 | PM CORRECT-WORK v2.7.0 (reconstitutions méthode B1) ; référence PM-INSTALL v1.3.1 |
| v1.6.5 | 2026-10-09 | Référence PM-INSTALL v1.5.0 (§2ter instantané explicite des dernières versions) |
| v1.6.6 | 2026-10-09 | Référence gen-plan v3.21.0 (règle d'or n°4 — clone git local, jamais lecture distante) |
| v1.6.7 | 2026-10-09 | Référence PM-INSTALL v1.6.0 (§2quater génération automatique du PM — KO-L004 v1.1.0) |
| v1.6.8 | 2026-10-11 | §1.2 codification du dossier d'archive `skills/@historique/` (R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003, re-scellement KO-L004, résorption mention `_archive/` stale) — Task 17 |
| v1.7.0 | 2026-10-11 | §7 matérialisation des définitions normatives des 3 disciplines n°54 dans la table de définitions (spec-driven development, memory engineering, fleet engineering — ancrage état de l'art dans `references/fondements-academiques.md` de chaque skill ; registre d'assignation inchangé — R4) — session web-b4d7dd19, objectif principal discussion Qwen |
| v1.7.1 | 2026-10-11 | §6.1 référence gen-plan portée à v3.22.0 (recalibrage mécanique KO-L004 v1.1.0 — `generer-pm-skill.py`, bump PATCH conformité semver — adaptation locale journalisée : D010 + précédents v3.21.0) |
| v1.7.2 | 2026-10-11 | §6.1 référence gen-plan portée à v3.22.1 (recalibrage mécanique KO-L004 v1.1.0 — `generer-pm-skill.py`, bump PATCH conformité semver ; cascade renommage step-ok + clause mode NULL, session web-b4d7dd19) |
| v1.7.11 | 2026-10-24 | §6.1 — référence PM GEN-PLAN portée à v3.24.0 (génération mécanique `scripts/generer-pm-skill.py` — substitutions verrouillées, recalibrage inclus — Task 26, session web-fdf5963c ; note : lignes v1.7.9/v1.7.10 absentes de cette table — écart hérité documenté, la table §7 du PM vivant fait foi) |
| v1.7.8 | 2026-10-23 | §6.1 — référence(s) PM portée(s) aux 4 versions générées mécaniquement (gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1) + référence PM-INSTALL portée à v1.8.0 (mécanisme dual d'installation + périmètre alias-eco — Task 18, session web-fdf5963c) ; complétion de la ligne de révision |
| v1.7.4 | 2026-10-12 | §7 correction outil (ligne « Refactoring test » = outil de la discipline n°55 — Task 8, directive propriétaire) + registre scindé en 3 lignes (refactoring-engineering discipline / refactoring-test outil / refactor-guard garde-fous — fusion discussion 468a4c26) ; §6.1 référence gen-plan portée à v3.23.1 (recalibrage mécanique KO-L004 — `generer-pm-skill.py`, bump PATCH conformité semver) — session web-b4d7dd19 Task 8 gen-plan(step) |
| v1.7.3 | 2026-10-12 | §7 matérialisation des définitions normatives des 2 disciplines de refactoring n°55 (refactoring engineering, refactoring test — ancrage état de l'art dans `references/fondements-academiques.md` de chaque skill ; registre d'assignation +1 ligne) ; §6.1 référence gen-plan portée à v3.23.0 (recalibrage mécanique KO-L004 v1.1.0 — `generer-pm-skill.py`, bump PATCH conformité semver) — session web-b4d7dd19 Task 7 gen-plan(step) |

## 2. SYNC-CONTEXT.md (procédure de synchronisation des blocs)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.5.4 | 2026-10-24 | Cascade Task 26 (session web-fdf5963c, KO-L004) : gen-plan v3.23.2→v3.24.0 (parallélisation par défaut — philosophie #4 inversée, directive propriétaire) ; PM GEN-PLAN v3.24.0 généré mécaniquement (complétion agent), v3.23.2 archivé R4 ; SHARED v1.7.11 ; PM-INSTALL v1.8.4 ; KB recalibrée ; ULTRA régénéré ; propagation marqueur §0 v1.7.11 (106 skills + 107 scripts + 2 agents) ; archive rescellée round-trip v2.3 |
| v1.5.3 | 2026-10-23 | Cascade Task 25bis/25ter (GO propriétaire, session web-fdf5963c) : alias-eco v1.1.0→v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization replay 8/8) ; KB, PM-INSTALL v1.8.3 (§A.3), ULTRA recalibrés ; registre @Alias vivant (ECO-LEON, OPT-TRIO — non-cible resync) |
| v1.4.0 | 2026-10-02 | Decision d'architecture v2.2 — canal download/ supprimé, archive d'intégrité = unique voie de diffusion ; `sync-download.py` retiré, garde `task14-scan-doublons.py` (Task 14) |
| v1.4.1 | 2026-10-02 | Résorption F1/F2/F4 — corpus 26 fichiers, PMs v2.6.0/v2.7.0 reconstitués méthode B1, blocs gelés R2 (Task 16, session web-8a7e5653) |
| v1.4.2 | 2026-10-11 | Dédup des PMs — cibles de resync réduites à 2 porteurs N1 vivants, corpus 8 fichiers, `@historique/` archive documentaire (Task 16) |
| v1.4.3 | 2026-10-11 | Codification SHARED §1.2 en v1.6.8 (dossier `@historique/` — R4/R2/KO-L003, re-scellement KO-L004) ; cascade resync 2 N1 + 93 N2 + 49 N3 + 2 .agent (Task 17) |
| v1.4.4 | 2026-10-11 | Recalibrage état gen-plan v3.22.0 — v3.21.0 archivé (16 PMs GEN-PLAN) ; décision propagation N2 tracée : bloc §0 byte-identique v1.6.8→v1.7.1, aucune re-propagation requise (cascade n°54, session web-b4d7dd19) |
| v1.4.5 | 2026-10-11 | Recalibrage état gen-plan v3.22.1 — v3.22.0 archivé (17 PMs GEN-PLAN) ; propagation marqueur §0 v1.7.1→v1.7.2 recalibrée et exécutée (cascade renommage step-ok + clause mode NULL, session web-b4d7dd19) |
| v1.5.0 | 2026-10-23 | Cascade Task 18 (session web-fdf5963c, KO-L004) : 4 PMs familles régénérés mécaniquement (gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1 — note §5 mécanisme dual) ; PM-INSTALL v1.7.2→v1.8.0 ; SHARED v1.7.8 ; propagation marqueur §0 v1.7.7→v1.7.8 exécutée (100 skills + 69 scripts + 2 agents, idempotent) ; skill alias-eco v1.0.0 créé (registre @historique/@Alias/ — état vivant) ; KB 34 entrées ; ULTRA régénéré ; archive rescellée round-trip 9/9 |
| v1.4.7 | 2026-10-12 | Révision Task 8 (cascade gen-plan v3.23.1 — gen-plan(step), fusion discussion 468a4c26) : propagation marqueur §0 v1.7.3→v1.7.4 (constantes recalibrées — skills + scripts + agents, idempotent ×2) |
| v1.4.6 | 2026-10-12 | Recalibrage état gen-plan v3.23.0 — v3.22.1 archivé (18 PMs GEN-PLAN) ; propagation marqueur §0 v1.7.2→v1.7.3 recalibrée et exécutée (97 skills + 51 scripts + 2 agents, idempotent ×2 — matérialisation n°55, session web-b4d7dd19 Task 7) |

## 3. README.md (guide de référence de l'écosystème)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v2.1.12 | 2026-10-24 | Task 26 (session web-fdf5963c, KO-L004) : gen-plan v3.24.0 (parallélisation par défaut sur preuve d'indépendance) ; PM GEN-PLAN v3.24.0 généré mécaniquement, v3.23.2 archivé @historique/prompts-maitres/gen-plan/ (mv byte-identité R4) ; SHARED v1.7.11 / PM-INSTALL v1.8.4 ; SYNC v1.5.4, ULTRA, KB recalibrés |
| v2.1.11 | 2026-10-23 | Cascade Task 25bis/25ter (GO propriétaire, session web-fdf5963c) : alias-eco v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization) ; KB, PM-INSTALL v1.8.3, SYNC v1.5.3, ULTRA recalibrés |
| v2.1.0 | 2026-10-02 | Décision d'architecture v2.2 — canal download/ supprimé, outillage recalibré, drift SHARED §6.1 résorbé (Task 14) |
| v2.1.1 | 2026-10-11 | Dédup des PMs — corpus dernières versions seules, `@historique/` documenté, arborescence §2 recalibrée (Task 16) |
| v2.1.2 | 2026-10-11 | Recalibrage état gen-plan v3.22.0 — §7 « 5 disciplines » → « 5 + 3 matérialisations n°54 », arborescence v3.22.0/v1.6.1/×16, SHARED v1.7.1 (cascade n°54, session web-b4d7dd19) |
| v2.1.3 | 2026-10-11 | Recalibrage état gen-plan v3.22.1 — arborescence v3.22.1/v1.6.2/×17, SHARED v1.7.2 (cascade renommage step-ok + clause mode NULL, session web-b4d7dd19) |
| v2.1.4 | 2026-10-12 | Recalibrage état gen-plan v3.23.0 — arborescence v3.23.0/v1.6.3/×18, SHARED v1.7.3, « 5 + 3 matérialisations n°54 » → « 5 + 3 n°54 + 2 n°55 » (matérialisation n°55, session web-b4d7dd19 Task 7) |

## 4. PROMPT-ULTRA-MAITRE-ORCHESTRATION.md (orchestrateur)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.0.0 | généré | Orchestrateur régénéré mécaniquement par `scripts/gen-ultra-maitre.py` depuis les sources vivantes (jamais édité à la main) ; dernier recalibrage Task 16 (STALE v3.18.0 résorbé) |

## 5. PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (pipeline d'installation — source unique)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.8.4 | 2026-10-24 | KO-L004 v1.1.0 — génération mécanique du PM à toute montée de version (`scripts/generer-pm-skill.py`) : gen-plan v3.23.2→v3.24.0 ; recalibrage croisé : SHARED v1.7.11 (§6.1), §2ter, §A.3 |
| v1.8.3 | 2026-10-23 | Cascade alias-eco v1.2.0 (Task 25bis/25ter, GO propriétaire) : §A.3 instantané recalibré (alias-eco v1.0.0→v1.2.0) — bump PATCH conformité semver |
| v1.8.0 | 2026-10-23 | MÉCANISME DUAL d'installation (§3.2 réécrit : installation directe des formes certifiées du dépôt = voie par défaut, exécutant canonique eco_install_pipeline.py ; assemblage bootstrap corpus-seul) + intégration alias-eco (§2bis/§4/§A.3) — Task 18, session web-fdf5963c, directive propriétaire « optimise le système d'installation en regénérant » + prérequis A |
| v1.7.2 | 2026-10-23 | Génération mécanique KO-L004 des 4 PMs familles (gen-plan v3.23.2 · correct-work v2.8.0 · clone-chat v2.0.2 · refactor-guard v1.7.1) — recalibrage croisé §2ter/§A.3 ; SHARED v1.7.8 |
| v1.1.0 | 2026-10-02 | Fusion des installateurs (périmètre §A + ordre optimal 10 étapes) — source d'installation unique (R4) |
| v1.2.0 | 2026-10-02 | Dérivation dynamique « PM le plus récent » généralisée aux 3 familles + garde anti-rétrogradation R2 (§3.2) |
| v1.3.0 | 2026-10-02 | Déduplication download/ — canal de fichiers supprimé (décision d'architecture v2.2) |
| v1.3.1 | 2026-10-02 | Cas d'espèce R2 correct-work résorbé |
| v1.5.0 | 2026-10-09 | §2ter — instantané explicite des dernières versions des PMs sources et du socle indispensable |
| v1.5.1 | 2026-10-09 | Instantané rafraîchi gen-plan v3.21.0 (règle d'or n°4 clone git local) |
| v1.6.0 | 2026-10-09 | §2quater — génération automatique du PM à toute montée de version (KO-L004 v1.1.0, `generer-pm-skill.py`) |
| v1.6.1 | 2026-10-11 | §2ter + §A.3 instantané rafraîchi gen-plan v3.22.0 (recalibrage mécanique KO-L004 — `generer-pm-skill.py`, bump PATCH conformité semver — adaptation locale journalisée : D010 + précédents v3.21.0) |
| v1.6.2 | 2026-10-11 | §2ter + §A.3 instantané rafraîchi gen-plan v3.22.1 (recalibrage mécanique KO-L004 — `generer-pm-skill.py`, bump PATCH conformité semver ; cascade renommage step-ok + clause mode NULL) |
| v1.6.3 | 2026-10-12 | §2ter + §A.3 instantané rafraîchi gen-plan v3.23.0 (recalibrage mécanique KO-L004 — `generer-pm-skill.py`, bump PATCH conformité semver ; matérialisation disciplines de refactoring n°55) |

## 6. Registre KB — `skills/KNOWLEDGE.md` (source de vérité de l'état de l'écosystème)

Registre à 34 entrées — instantané des versions archivé ci-dessous (source : registre KB, instantané rafraîchi 2026-10-23 Task 18 (création alias-eco) puis Task 25bis/25ter (alias-eco v1.2.0 — grammaire B --trigger, OPT-TRIO) ; le registre vivant fait foi ; les versions des 4 familles = versions de leurs PMs vivants, contrat KO-L004).

| Skill | Version | Skill | Version |
|-------|---------|-------|---------|
| gen-plan | v3.23.2 | audit-provenance | v1.1.0 |
| correct-work | v2.8.0 | autonomous-agent | v1.1.0 |
| clone-chat | v2.0.2 | correct-py | v1.1.0 |
| skills-inventory | v1.1.0 | fleet-engineering | v1.0.1 |
| skill-creator | v1.1.0 | memory-engineering | v1.1.1 |
| agent-creator | v2.1.0 | spec-driven-development | v1.0.1 |
| prompt-engineering | v2.2.0 | audio-metadata | v1.1.0 |
| context-engineering | v1.1.0 | cpp-analysis | v1.1.0 |
| loop-engineering | v1.1.0 | pdf-llm | v1.0.0 |
| graph-engineering | v1.0.1 | resource-monitor | v1.0.0 |
| harness-engineering | v1.1.0 | version-management | v1.2.0 |
| script-mon-ecosysteme-infrastructure | v1.1.0 | skill-finder-cn | v1.0.0 |
| knowledge-observer | v1.0.0 | vue-upload | v1.2.0 |
| script-creator | v1.1.0 | script-reviewer | v1.0.0 |
| refactoring-engineering | v1.0.1 | refactoring-test | v1.0.1 |
| refactor-guard | v1.7.1 | fullstack-dev | v1.0.0 |
| alias-eco | v1.2.0 | dessin-technique | v1.1.1 |

## 7. Mise à jour de ce fichier

À chaque révision d'un élément du socle (montée de version du SHARED, du SYNC-CONTEXT, du README, de PM-INSTALL ou du registre KB) : ajouter une ligne à la table de la section correspondante (version, date, résumé fidèle à l'en-tête Révision du fichier vivant), sans réécrire l'historique antérieur. L'orchestrateur `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` n'entre dans ce fichier que si sa mécanique de génération change (il est régénéré mécaniquement). Procédure normative générale au `README.md` du présent dossier (§4) ; sweep arbitres avant tout commit.
