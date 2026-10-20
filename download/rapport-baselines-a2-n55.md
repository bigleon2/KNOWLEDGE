# Rapport baselines A2 — disciplines n°55 (refactoring-engineering + refactoring-test)

> **Périmètre** : baselines A2 des 2 skills n°55 — mesure du routage des déclencheurs AVANT toute optimisation (méthode SHARED §7 v2, réplique identique aux arbitres certifiés task18/task21 : stemmer français léger, routage si ≥ 2 radicaux partagés OU ≥ 1 radical du nom).
> **Gate QUOTA_OK (KO-L001)** : levé par la directive utilisateur explicite du propriétaire (2026-10-12, session web-b4d7dd19 — gen-plan(step) : « baselines A2 n°55 (QUOTA_OK) ») ; sonde unique verte avant mesure (réponse API valide, 54 tokens).
> **Instruments** : `scripts/task9-baseline-a2-n55.py` (voie M déterministe + voie L 3 runs/cas, backoff 429, politesse 4 s, checkpoints par cas) · rapport machine `scripts/baseline-a2-n55-report.json`.

## 1. refactoring-engineering v1.0.1 → v1.1.0

- **Voie M (mécanique)** : 6/7 au premier passage — **1 dérive** sur le cas négatif n°6 « Renforce le harnais : profils ressource, signaux de pression, gardes-fous. » (attendu NON, routé OUI) : collision lexicale `gard`+`fous` (« gardes-fous » de la requête) ↔ « **Garde-fous mobilisés** pendant les opérations : refactor-guard… » de la description frontmatter.
- **Voie L (confirm LLM, 3 runs/cas — vote majoritaire, seuil 0.5)** : **7/7 conforme** — votes 3/3 unanimes sur chacun des 7 cas (0 vote null), y compris le cas n°6 (NON ×3) : le routeur LLM ne confirme jamais la fausse collévision.
- **Traitement protocolaire** : dérive constatée → **Description Optimization OBLIGATOIRE (protocole SHARED §7)** — `scripts/g2b-description-optimization.py` (éditions verrouillées count==1, cascade v1.0.1→v1.1.0 : SKILL.md, KB heading + calibration, ECO_SKILLS integrity, @historique par-skill) : « Garde-fous mobilisés pendant les opérations » → « **Sécurisation des opérations assurée par le skill refactor-guard** » — sémantique inchangée (refactor-guard demeure le garde-fou déclaré de la discipline n°55).
- **Re-mesure voie M (--remeasure-m, votes L préservés)** : **7/7 — 0 dérive**. Les 5 cas positifs continuent de router (radicaux du nom `refactoring`/`engineering` + radicaux de description `refactor`, `declar`, `transform`, `archivag`), le cas négatif n°6 ne cumule plus aucun signal, le cas négatif n°7 reste hors signal.

## 2. refactoring-test v1.0.1 (inchangé)

- **Voie M** : **7/7 — 0 dérive** dès le premier passage. Les radicaux du nom (`refactoring`, `test`) et de description (`detect`, `evalu`, `graphe`, `interact`, `blast`, `radius`, `scan`, `signaux`, `dette`) couvrent les 5 requêtes positives ; les 2 contrôles négatifs (relecture/verification de rapport S1-S3 ; graphe de connaissances KB) ne cumulent aucun signal de routage — la garde de collision SHARED §7 v2 est respectée.
- **Voie L** : **7/7 conforme** — votes 3/3 unanimes par cas (0 null).

## 3. Verdict consolidé

| Skill | Voie M | Voie L | Dérive | Description Optimization |
|---|---|---|---|---|
| refactoring-engineering | 7/7 (après optim.) | 7/7 | 0 (1 résorbée) | OUI — v1.1.0 (protocole §7) |
| refactoring-test | 7/7 | 7/7 | 0 | NON requise |

**Verdict : baseline A2 MESURÉE — 14/14 cas conformes sur les deux voies, ZÉRO dérive résiduelle.** Le routage des deux skills n°55 est conforme à leurs evals officielles : la dérive détectée AVANT mise en production a été traitée selon le protocole (Description Optimization), prouvant que la boucle baseline → détection → optimisation → re-mesure fonctionne de bout en bout sur les matérialisations n°55. La baselines A2 des disciplines n°55 cesse d'être « armée non mesurée » (clôture de la réserve héritée des Tasks 7/8).

## 4. Traçabilité et invariants

- **Anti-fabrication (R3)** : les 42 votes LLM (14 cas × 3 runs) sont des appels réels (`z-ai` CLI) — aucun vote null, aucune fabrication ; les preuves d'appel sont dans le JSON (champ `evidence` par vote).
- **Idempotence (KO-L001)** : le script est rejouable (`--skip-done` préserve les votes réels ; `--remeasure-m` recalcule la voie M seule après optimisation de description) — re-exécution : `python3 scripts/task9-baseline-a2-n55.py --skip-done`.
- **R2** : les evals officielles (`evals/trigger_evals.json` ×2) sont inchangées — c'est la DESCRIPTION qui est optimisée, jamais les cas de test.
- **Cascade v1.1.0** : SKILL.md canonique + KB (heading + calibration) + ECO_SKILLS (integrity) + @historique par-skill ; projection hôte en fin de Task 9 (G4) ; description hôte alignée à la même édition (byte-identité).
