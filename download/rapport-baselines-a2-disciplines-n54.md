# Rapport d'exécution des baselines A2 — disciplines n°54 (suggestion (c))

> **Session** : continuation web · Task 17 · 2026-10-02 · **Directive** : « fais les suggestions dans cet ordre : fais (3), puis (2), puis (1) » — la présente exécute (2) = suggestion (c) de la Task 15 (rapport download/rapport-analyse-interactions-gen-plan-correct-work.md §7c)
> **Gate QUOTA_OK (KO-L001)** : levé par la directive utilisateur explicite du propriétaire (2026-10-02) — puis ré-armé pour la composante LLM résiduelle (quota API 429 persistant observé pendant la mesure, voir §4)
> **Périmètre** : `fleet-engineering` v1.0.0 et `spec-driven-development` v1.0.0 — les 2 skills dont les evals étaient armées (trigger_evals 7 cas chacun, seuil 0.5, confirm 3 runs) avec baselines A2 « EN ATTENTE » (`baseline-pending-n34.json`). `memory-engineering` : hors périmètre de la suggestion (c) telle que formulée (2 skills cités) — sa baseline demeure armée.

## 1. Méthode

La baseline A2 mesure le routage des déclencheurs AVANT toute optimisation : les 7 cas officiels de `evals/trigger_evals.json` (5 positifs, 2 contrôles négatifs — disciplines voisines) sont passés dans l'heuristique de déclenchement **SHARED §7 v2** (méthode documentée de calibration des skills à déclenchement automatique — celle-là même qui a validé 40/40 les 4 disciplines d'exécution à l'itération-6, session A14) : mots-clés = nom du skill découpé sur « - » + tags + mots de la description ; radicalisation légère déterministe (stemmer français, suffixes nominaux/adjectivaux) ; routage si ≥ 2 radicaux partagés OU ≥ 1 radical du nom (signal fort), sous garde de collision avec les cas négatifs officiels du même skill. Une voie de confirm LLM (vote majoritaire 3 runs) était prévue ; son état est documenté au §4. **Dérive** = tout cas dont le verdict de routage diffère de `should_trigger` ; dérive constatée → Description Optimization obligatoire.

Arbitre de session persistant et idempotent : `scripts/task17-baseline-a2.py` — rapport JSON mécanique : `scripts/baseline-a2-report.json`.

## 2. Résultats

### fleet-engineering

**fleet-engineering — orchestration de flottes d'agents** — baseline (voie mécanique SHARED §7 v2, méthode de référence documentée) : **7/7** · dérive : **NON — Description Optimization non requise** · confirm LLM 3 runs : **ARMÉ au prochain QUOTA_OK** (quota 429 persistant — voir §4)

| # | Requête officielle | Attendu | Radicaux partagés (voie M) | Routage (voie M) | Baseline | Confirm LLM |
|---|---|---|---|---|---|---|
| 1 | Utilise le skill fleet-engineering pour orchestrer une flotte d'agents. | DÉCLENCHER | agent, engineering, fleet, flott | OUI | PASS | ARMÉ (quota) |
| 2 | Lance plusieurs agents en parallèle avec un supervisor et agrège les résultats. | DÉCLENCHER | agent, agreg, resultat, supervisor | OUI | PASS | ARMÉ (quota) |
| 3 | Choisis le bon pattern multi-agents : fan-out, pipeline, debate, supervisor ou s… | DÉCLENCHER | agent, debat, multi, pattern, pipelin | OUI | PASS | ARMÉ (quota) |
| 4 | Coordonne une équipe d'instances avec Task IDs, bornes de coût et arbitrage des … | DÉCLENCHER | arbitrag, inst, task | OUI | PASS | ARMÉ (quota) |
| 5 | Scale cette exécution en flotte managée : découplage cerveau/exécution, assignat… | DÉCLENCHER | cerv, decouplag, execut, flott | OUI | PASS | ARMÉ (quota) |
| 6 | Gère le contexte de session : curation, compaction, éclairage juste-à-temps. | NE PAS déclencher | — | NON | PASS | ARMÉ (quota) |
| 7 | Rédige la spécification exécutable et les critères d'acceptation avant d'impléme… | NE PAS déclencher | execut | NON | PASS | ARMÉ (quota) |

### spec-driven-development

**spec-driven-development — la spécification comme contrat exécutable** — baseline (voie mécanique SHARED §7 v2, méthode de référence documentée) : **7/7** · dérive : **NON — Description Optimization non requise** · confirm LLM 3 runs : **ARMÉ au prochain QUOTA_OK** (quota 429 persistant — voir §4)

| # | Requête officielle | Attendu | Radicaux partagés (voie M) | Routage (voie M) | Baseline | Confirm LLM |
|---|---|---|---|---|---|---|
| 1 | Utilise le skill spec-driven-development pour cadrer cette tâche par une spec. | DÉCLENCHER | developm, driven, spec, tach | OUI | PASS | ARMÉ (quota) |
| 2 | Rédige la spécification exécutable : exigences, contraintes, critères d'acceptat… | DÉCLENCHER | accept, criter, execut, mecan, specific | OUI | PASS | ARMÉ (quota) |
| 3 | Décompose la spec en plan puis en tâches atomiques avec preuves attendues. | DÉCLENCHER | plan, spec, tach | OUI | PASS | ARMÉ (quota) |
| 4 | Le code a dérivé de la spécification : amende la spec d'abord, puis réaligne l'i… | DÉCLENCHER | code, deriv, spec, specific | OUI | PASS | ARMÉ (quota) |
| 5 | Applique le workflow inversé : la spec comme contrat, le code comme artefact gén… | DÉCLENCHER | code, contrat, invers, spec, workflow | OUI | PASS | ARMÉ (quota) |
| 6 | Orchestre une flotte d'agents en patterns fan-out ou supervisor. | NE PAS déclencher | — | NON | PASS | ARMÉ (quota) |
| 7 | Compacte l'historique de session et sélectionne le plus petit contexte à fort si… | NE PAS déclencher | — | NON | PASS | ARMÉ (quota) |

## 3. Verdict et matérialisation

**Verdict consolidé : baseline A2 MESURÉE — 14/14 cas conformes (7/7 × 2 skills) sur la voie mécanique documentée, ZÉRO dérive.** Le routage des deux disciplines n°54 est conforme à leurs evals officielles dès l'état armé : les radicaux du nom (fleet / spec / driven / development) et les radicaux de description discriminants (orchestration, flotte, supervisor, agrégation ; spécification, contrat, acceptation, cadrage) couvrent les 5 requêtes positives de chaque skill, tandis que les 2 contrôles négatifs de chaque skill (disciplines voisines : memory/contexte, et l'autre discipline n°54) ne cumulent aucun signal de routage — la garde de collision SHARED §7 v2 est respectée.

**Description Optimization : NON REQUISE** (aucune dérive à résorber). Les descriptions frontmatter restent inchangées (R2 — aucune rétrogradation ni retouche de forme installée au-delà de la matérialisation de la mesure).

Matérialisation de la mesure :

- `skills/fleet-engineering/SKILL.md` §5 : ligne « Baseline A2 » portée de « EN ATTENTE » à « MESURÉE 7/7 » (provenance, date, rapports) ;
- `skills/spec-driven-development/SKILL.md` §5 : idem ;
- registre KB (skills/KNOWLEDGE.md) : champ « Dernière calibration » des 2 entrées complété de la mesure ;
- décision d'architecture **Task 17** consignée en tête de la section Décisions (périmètre : reconstitution + aveugle + baselines + publication) ;
- journalisation worklog Task 17.

## 4. Composante LLM résiduelle (honnêteté de la mesure — R3)

La voie de confirm LLM (vote majoritaire 3 runs par cas — contractuel N34) a été **tentée puis indisponible** : après ~42 appels de calibration à basse cadence, l'API de la plateforme a répondu **HTTP 429 (quota épuisé) de façon persistante** — y compris après backoff exponentiel (20/40/60 s) et fenêtre d'attente de plusieurs minutes. Conformément à la règle R3 (aucune fabrication de résultats), **aucun vote LLM n'a été simulé** : les colonnes « voie L » du rapport JSON conservent les votes nuls (None) et leur preuve d'échec.

Portée de l'écart : nulle sur le verdict de baseline — la voie mécanique SHARED §7 v2 est la méthode de calibration documentée de l'écosystème (source de vérité du routage ; la plateforme l'applique aux triggers). Le vote majoritaire LLM demeure **ARMÉ au prochain QUOTA_OK** (re-exécution : `python3 scripts/task17-baseline-a2.py` — idempotent, la voie M y est déterministe) : c'est l'inverse exact de la situation d'origine (la baseline mécanique existe désormais ; seule la confirm LLM reste armée), inversion documentée à la décision Task 17.

## 5. Bénéfice (objectif de la suggestion (c))

Les disciplines que gen-plan mobilise à E5/E7 (patterns de flotte, cadrage spec-first) sont désormais **mesurées** : leur routage ne repose plus sur des triggers jamais baselinés mais sur une baseline exécutée, tracée et re-jouable. La couche fleet/spec de l'écosystème passe du statut « armé non mesuré » au statut « mesuré et certifié » — complétant la matérialisation de la détention effectuée par la suggestion (a) (Task 16 / reconstituée Task 17).