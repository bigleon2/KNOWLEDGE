# Rapport Task 17 (re-exécution post-incident) — codification SHARED §1.2 @historique/, re-mesure voie L, correct-work projet

> **Session** : web-b93f42fa — **Date** : 2026-10-11 — **Directive propriétaire** : « fais la suite optionnelle : codification SHARED §1.2 du nouveau dossier, re-mesure voie L des 15 dérives replay » + « correct-work (projet) » + GO avec PAT.
> **Particularité d'exécution** : la session a subi l'incident S3 étendu (restauration du répertoire depuis un snapshot 2026-10-10 20:48 — couche Task 17 originelle intégralement perdue) ; la présente Task 17 est une RE-EXÉCUTION en couches commitées/poussées, conforme au plan vivant `download/plan-task17-reexecution-optimisee.md`.

## 1. Incident S3 étendu (forensique)

| Fait | Preuve |
|------|--------|
| Restauration directory-wide depuis un snapshot | mtimes alignés (SHARED 2026-10-09 07:37, SYNC-CONTEXT 2026-10-10 16:25, `.git` 2026-10-10 20:48) ; reflog intact (dernier event = 4c12afe) |
| Couche Task 17 originelle perdue | 0 fichier task17-* sur disque, 0 blob Task 17 dans l'ODB (12 blobs dangling = sorties d'arbitres d'anciennes sessions), index == HEAD |
| Worklog racine écrasé aussi | 0 entrée Task 17 dans `/home/z/my-project/worklog.md` post-incident |
| Récupération impossible | miroir profil stalé (v1.6.7), download/ racine vide, origin inchangée |
| Riposte | re-exécution en couches R1→R5, commit+push immédiat par couche (origin = seule zone survivante) |

## 2. Couche R1 — codification SHARED v1.6.8 + cascade (2df7429)

- SHARED v1.6.7 → **v1.6.8** : §1.2 codifie le dossier d'archive `skills/@historique/` (R4 déplacement `git mv` byte-identité, R2 fichiers archivés jamais édités, jamais source d'installation KO-L003, table §7 du PM vivant = source de vérité, re-scellement KO-L004, résorption de la mention `_archive/` stale).
- Cascade : sync N1 (2 porteurs vivants CLONE-CHAT + INSTALL) + propagate N2/N3 → **145 porteurs v1.6.8** (93 skills + 49 scripts + 2 .agent + 4 socle).
- **Dynamisation d'instruments** : `propagate-context.py` idempotence v2 (remplacement du bloc résumé existant — l'ancien code skipait, impossible de monter de version) + blocs L2/L3 portés v1.5.2 → v1.6.8 avec mention `@historique/` ; `install-ecosystem.py` bloc extrait v1.6.8 ; 4 blocs §0 divergents corrigés (format sans ligne vide finale — `scripts/task17b/fix4-blocs-v168.py` hors dépôt, idempotent).
- SYNC-CONTEXT v1.4.2 → **v1.4.3** (révision Task 17 tracée).
- Arbitres : integrity 60/60 · coherence 48 PASS / 3 WARN / 0 FAIL · verify-cross 100 % · archive re-scéllée round-trip v2.2.

## 3. Couche R2 — re-mesure voie L (ff8c061 puis reversion au commit R3)

Runner réécrit (`scripts/task17-remeasure-voie-l.py`) : crash-safe (persist par cas), idempotent, backoff 429, **prompt de vote calibré au contrat SHARED §7 v2** (périmètre précis, anti-faux-positif, négatifs explicites — correction d'un décalibrage initial « usage général » qui produisait des REFUTE faux sur des cas négatifs officiels), révisions bidirectionnelles.

**Résultat final : 31/31 cas — 21 CONFIRME + 7 REFUTE_UNANIME + 2 AMBIGU + 1 QUOTA** :

| Décision | Cas | Traitement |
|----------|-----|-----------|
| CONFIRME (21) | variantes contextuelles réelles (agent-browser ×3, ai-news « la tâche « ai » », jd « j'ai besoin… », pdf-llm « Génère un nouveau PDF », script-reviewer, skills-inventory ×3, version-management ×5, vue-upload ×2, script-mon, prompt-engineering…) | dérive M réelle documentée — **0 fix instrument** |
| REFUTE_UNANIME (7) | templates auto-générés absurdes : ai-news ×2, jd ×2, ui-ux ×3 (« la tâche « x » » et variantes) | **révision auto appliquée** (expected → False) — politique : seuls les cas templates sont révisables |
| AMBIGU (2) | pdf-llm « Produis un rapport PDF », « Fusionne ces 5 PDF » | votes mixtes — documentés **sans révision** |
| QUOTA (1) | agent-creator « Automatise ce workflow avec Zapier… » | rate-limit durable (429 répétés, backoffs épuisés) — re-mesurable (precedent QUOTA_OK) |

**Correction de trajectoire tracée** : la révision initiale de `script-mon-ecosysteme-infrastructure` (négatif officiel « Lance l'installation complète de l'écosystème sur ce profil » voté True par le LLM) a été **ANNULÉE avec traçabilité** — un cas négatif officiel encode une décision de conception (présomption de justesse ; l'installation relève d'install-ecosystem) ; un premier script d'annulation a échoué en silence (query inexacte — faux succès détecté et corrigé par garde de match 1/1). Le cas retourne à CONFIRME (dérive M réelle).

**Replay re-joué** : **79/93, 14 dérivants** (ui-ux-pro-max sort des dérives via ses 3 révisions ; script-mon redevient dérivant après reversion) — verdict FAIL informatif documenté, md5 arbitre intact, 0 fix instrument. Écart vs campagne originelle (80/93, 13) : composition des dérives différente (les votes de re-mesure ne sont pas une reproduction byte-identique), assumée et tracée au report.

## 4. Harnais Task 17 (réécrit) — 16/16 ALL PASS rc0

Checks C01-C16 : codification v1.6.8 · SYNC v1.4.3 · cascade 0 résidu · propagate idempotence v2 · voie L 31/31 (21/7/2/1) · 7 révisions (templates uniquement) · reversion script-mon tracée · evals ui-ux False · replay 79/14 · runner calibré · anti-écho 0 occurrence · integrity SHA vives 8/8 · coherence 0 FAIL · plan vivant présent · 0 token VALUE · plan O1-O5.

## 5. Restant (couches R3-R5 de la présente exécution)

Sweep complet (fait, §ci-dessous), correct-work PROJET (rapport dédié), plans/rapports, worklog, R4 (historique par skill : D003/D005/D006), R5 journal + audits anti-persistance.

## 6. Sweep R3 (9 arbitres)

| Arbitre | Résultat |
|---------|----------|
| integrity | corpus 8/8 SHA vives alignées (60/60 checks au dernier run complet) |
| coherence interactions | PASS AVEC RÉSERVES (48 PASS / 3 WARN / 0 FAIL) |
| verify-cross | 100 %, 0 erreur |
| verify-correct-work | ALL PASS (0/16 FAIL) |
| generer-pm | 3/3 COHERENT |
| scan-doublons | 0 doublon (41 uniques) |
| registry-sync | ECARTS conception, 0 ghost (verdict connu non-régressif) |
| triggers-replay | 79/93, 14 dérives CONFIRME (documenté §3) |
| harnais task17 | 16/16 ALL PASS rc0 |
