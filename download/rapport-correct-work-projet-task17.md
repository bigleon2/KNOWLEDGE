# Rapport correct-work PROJET — Task 17 (re-exécution post-incident)

> **Mode** : PROJET (couplage gen-plan §1.5 — plan vivant : `download/plan-task17-reexecution-optimisee.md`) — **Vérificateur** : correct-work v2.7.0 — **Date** : 2026-10-11 (session web-b93f42fa)

## Verdict : PASS AVEC RÉSERVES

## Périmètre vérifié

La couche Task 17 re-exécutée (R1 + R2 publiées : 2df7429, ff8c061) et les couches R3/R4/R5 en cours de matérialisation (présent rapport inclus). Le plan de vérification suit les 5 étapes du mode PROJET sur l'artefact global « Task 17 re-exécution ».

## 1. Vérification de la complétude du plan (E1)

Le plan vivant déclare R1→R5 avec answer key mécanique et baselines. R1 (codification + cascade) et R2 (voie L + replay) sont publiées et vérifiées par le harnais dédié (16/16). R3 (présent rapport, harnais, sweep) et R4 (historique par skill : D001/D002/D004 déjà matérialisés sur disque) sont en cours de publication ; R5 (journal) suivra. Chaque livrable déclaré au plan a un critère mécanique — cohérence plan/exécution maintenue : les écarts de parcours (incident, décalibrage des votes, reversion script-mon) sont documentés dans le plan et son rapport, sans modification rétrospective du plan (traçabilité).

## 2. Vérification factuelle (E2 — échantillon byte-level)

- SHARED : `> **Version** : 1.6.8` présent, §1.2 contient la codification @historique (R4, git mv, KO-L004) — vérifié C01 harnais.
- Cascade : 0 résidu « SHARED v1.5.2 » hors archive dormante et hors instruments de check — C03.
- Voie L : report 31/31 (21 CONFIRME / 7 REFUTE / 2 AMBIGU / 1 QUOTA), 7 révisions auto (toutes sur cas templates « la tâche « x » »), reversion script-mon tracée par note — C05-C07.
- Evals révisés : ui-ux ×3 templates → False vérifié en JSON — C08.
- Replay : 79/93, 14 dérivants, verdict FAIL informatif — C09.
- R4 disque : `historiques-par-skill/{gen-plan,correct-work,clone-chat}.md` (22/10/4 lignes de versions — migration verbatim des tables), `historique-autres-elements.md`, README @historique v1.1.0.

## 3. Cohérence et régressions (E3)

Aucune régression détectée sur les 9 arbitres du sweep (rapport Task 17 §6) : integrity corpus 8/8 SHA vives, coherence 0 FAIL, verify-cross 100 %, vcw ALL PASS, generer-pm 3/3, doublons 0, registry-sync ECARTS conception connu (0 ghost). Les corrections apportées aux instruments (propagate idempotence v2, blocs L2/L3 v1.6.8, install-ecosystem extrait) améliorent la mécanique sans modifier les contrats.

## 4. Écarts et réserves (E4)

1. **RÉSERVE — re-mesure non reproductible** : les verdicts de la voie L diffèrent partiellement de la campagne originelle perdue (composition des révisions et des dérives ; 79/93 vs 80/93). Cause : les votes LLM ne sont pas déterministes et le runner a été réécrit. Traitement : tracé au rapport et au plan ; les politiques sont plus prudentes qu'à l'originale (calibrage au contrat, reversion des négatifs officiels, AMBIGU sans révision).
2. **RÉSERVE — 1 QUOTA** : le cas agent-creator reste non voté (rate-limit durable) — re-mesurable à la prochaine campagne (precedent QUOTA_OK), documenté au report.
3. **ÉCART — process** : un script d'annulation a signalé un faux succès (0 match silencieux) — corrigé par garde de match et documenté (leçon : tout script de mutation doit échouer si aucun match).
4. **NOTE — original non rétabli byte-identique** : la codification v1.6.8 et le harnais sont des réécritures fidèles au CONCEPT, pas aux octets de la couche perdue (impossible) — assumé, les SHA actuelles font foi.

## 5. Verdict et suites (E5)

**PASS AVEC RÉSERVES** : l'objectif de la Task 17 (codification §1.2, re-mesure voie L, correct-work projet) est atteint avec des garanties mécaniques équivalentes à l'originale, sous réserves ci-dessus (toutes documentées et re-mesurables). Aucune correction bloquante requise. Suites : publication R4 (D003 disposition distillation + D005 SYNC + D006 harnais 17-B) et R5 (journal), avec audits anti-persistance canoniques après chaque push.
