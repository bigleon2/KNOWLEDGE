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

## 2. SYNC-CONTEXT.md (procédure de synchronisation des blocs)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.4.0 | 2026-10-02 | Decision d'architecture v2.2 — canal download/ supprimé, archive d'intégrité = unique voie de diffusion ; `sync-download.py` retiré, garde `task14-scan-doublons.py` (Task 14) |
| v1.4.1 | 2026-10-02 | Résorption F1/F2/F4 — corpus 26 fichiers, PMs v2.6.0/v2.7.0 reconstitués méthode B1, blocs gelés R2 (Task 16, session web-8a7e5653) |
| v1.4.2 | 2026-10-11 | Dédup des PMs — cibles de resync réduites à 2 porteurs N1 vivants, corpus 8 fichiers, `@historique/` archive documentaire (Task 16) |
| v1.4.3 | 2026-10-11 | Codification SHARED §1.2 v1.6.8 (@historique/) — cascade exécutée 2 N1 + 93 skills N2 + 49 scripts N3 + 2 .agent (Task 17) |

## 3. README.md (guide de référence de l'écosystème)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v2.1.0 | 2026-10-02 | Décision d'architecture v2.2 — canal download/ supprimé, outillage recalibré, drift SHARED §6.1 résorbé (Task 14) |
| v2.1.1 | 2026-10-11 | Dédup des PMs — corpus dernières versions seules, `@historique/` documenté, arborescence §2 recalibrée (Task 16) |

## 4. PROMPT-ULTRA-MAITRE-ORCHESTRATION.md (orchestrateur)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.0.0 | généré | Orchestrateur régénéré mécaniquement par `scripts/gen-ultra-maitre.py` depuis les sources vivantes (jamais édité à la main) ; dernier recalibrage Task 16 (STALE v3.18.0 résorbé) |

## 5. PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (pipeline d'installation — source unique)

| Version | Date | Résumé de révision |
|---------|------|--------------------|
| v1.1.0 | 2026-10-02 | Fusion des installateurs (périmètre §A + ordre optimal 10 étapes) — source d'installation unique (R4) |
| v1.2.0 | 2026-10-02 | Dérivation dynamique « PM le plus récent » généralisée aux 3 familles + garde anti-rétrogradation R2 (§3.2) |
| v1.3.0 | 2026-10-02 | Déduplication download/ — canal de fichiers supprimé (décision d'architecture v2.2) |
| v1.3.1 | 2026-10-02 | Cas d'espèce R2 correct-work résorbé |
| v1.5.0 | 2026-10-09 | §2ter — instantané explicite des dernières versions des PMs sources et du socle indispensable |
| v1.5.1 | 2026-10-09 | Instantané rafraîchi gen-plan v3.21.0 (règle d'or n°4 clone git local) |
| v1.6.0 | 2026-10-09 | §2quater — génération automatique du PM à toute montée de version (KO-L004 v1.1.0, `generer-pm-skill.py`) |

## 6. Registre KB — `skills/KNOWLEDGE.md` (source de vérité de l'état de l'écosystème)

Registre à 28 entrées — instantané des versions archivé ci-dessous (source : registre KB, 2026-10-11 ; le registre vivant fait foi ; les versions des 3 familles = versions de leurs PMs vivants, contrat KO-L004).

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

## 7. Mise à jour de ce fichier

À chaque révision d'un élément du socle (montée de version du SHARED, du SYNC-CONTEXT, du README, de PM-INSTALL ou du registre KB) : ajouter une ligne à la table de la section correspondante (version, date, résumé fidèle à l'en-tête Révision du fichier vivant), sans réécrire l'historique antérieur. L'orchestrateur `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` n'entre dans ce fichier que si sa mécanique de génération change (il est régénéré mécaniquement). Procédure normative générale au `README.md` du présent dossier (§4) ; sweep arbitres avant tout commit.
