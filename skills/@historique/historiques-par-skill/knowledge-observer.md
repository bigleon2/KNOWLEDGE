# Historique par skill — knowledge-observer

> **Version** : 1.1.0 — **Date** : 2026-11-09 (Task 82 G2, session web-ecef7f80 — directive « conversions », trace 1a1be717bb0fbdb1)
> **Version vivante** : v1.1.0 — `skills/knowledge-observer/SKILL.md` + agent autonome `skills/knowledge-observer/knowledge-observer.agent` (tandem 2 couches)
> **Versions archivées** : néant (pas de corpus PM propre à cette famille ; l'historique des états N20/B13-r5 est consigné au registre KB — entrée « Dernière calibration »)
> **Provenance** : conversion « cibles-to-agent » P1 — analyse mesurée `download/analyse-conversions-task82.md` §3 (inventaire `scripts/task82-inventaire.py` : knowledge-observer = seul skill avec `data/` persistant)

## Famille KNOWLEDGE-OBSERVER — 2 versions (skill : knowledge-observer)

**Particularité durable de la famille** : observation automatique des sessions pour détecter les patterns d'erreur et améliorer les skills — cycle A-H (Task Observer), 4 modes M1-M4, journal `data/lessons-learned.json`, propositions idempotentes VALIDÉES par correct-work avant application (garde anti-boucle SHARED §4.4). Depuis v1.1.0 : premier **agent autonome déployé** de l'écosystème (tandem méthode/exécution).

| Version | Date | Améliorations implantées | Avantage par rapport à la version précédente |
|---------|------|--------------------------|----------------------------------------------|
| v1.0.0 | 2026-09-19 | N20 : matérialisation du pattern Task Observer (source de vérité : `gen-plan/references/observation-patterns.md`) — SKILL.md (cycle A-H §1.2, modes M1-M4 §1.3, garde-fous §1.4), `evals/evals.json` + `evals/trigger_evals.json`, journal `data/lessons-learned.json` | Le cycle d'apprentissage continu (worklog + boucles R3 + KB Décisions) devient observé, journalisé et validé mécaniquement |
| v1.0.0 (restauration) | 2026-09-26 | B13-r5 : restauration post-wipe — journal L001-L004 restitué, référence observation-patterns.md restaurée | Résilience : le journal persistant survit aux volatilités de plateforme (leçon L001-L004) |
| v1.1.0 | 2026-11-09 | Task 82 G2 (directive « conversions ») : **conversion en agent autonome** — `knowledge-observer.agent` créé au format `.agent` canonique (mémoire 2 niveaux : État Court [session, max 20] / État Long [`data/lessons-learned.json`, persistance file] ; pipeline A-H avec modules Observation/Mémoire/Analyse/Proposition/Validation/Application + verification ; modes M1-M4 ; gardes [validation correct-work étape F, anti-boucle, idempotence R1-R6, seuil de récurrence 3/2-S1] ; sécurité no_hallucination / no_rule_modification / no_sensitive_data ; relations gen-plan/correct-work/skill-creator/audit-provenance/correct-py) + SKILL.md §1.6 tandem (ajouts purs — description frontmatter verbatim, triggers non-régression R2) | Le skill qui implémentait DÉJÀ l'architecture complète d'un agent autonome (cycle A-H = pipeline 8 étapes du format, modes M1-M4 = modes du format, journal persistant = État Long) obtient son porteur canonique `.agent` — l'écosystème compte son premier agent autonome déployé ; invocation E15/gen-plan inchangée — **VERSION VIVANTE** |
