# Rapport correct-work — gen-plan v3.24.0 « parallélisation par défaut » (mode CIBLE)

## Métadonnées
- **Date** : 2026-10-24 · **Mode** : CIBLE · **correct-work** : v2.8.0
- **Cible** : gen-plan v3.23.2 → v3.24.0 (Task 26 — directive propriétaire « trouve pourquoi gen-plan ne le fais pas, puis fais en sorte qu'il le fasse » ; plan `download/plan-task26-parallelisme-gen-plan.md`, answer key D001-D008)
- **Périmètre** : SKILL.md + references (graph-diamond-pattern.md, etapes-detaillees.md) + evals (id 9) + PM v3.24.0 + cascade KO-L004 (SHARED v1.7.11, PM-INSTALL v1.8.4, SYNC v1.5.4, README v2.1.12, ULTRA, KB, journal) + arbitres recalibrés

## Réponse au « pourquoi » (diagnostic vérifié mécaniquement)

| Cause | Preuve (état d'entrée) |
|-------|------------------------|
| Philosophie #4 « Serial exécution by DEFAULT — Parallélisme INTERDIT sauf demande explicite » (SKILL.md §1.4, héritée dès v3.6.1) | grep SKILL.md/PM v3.23.2 ligne 88 — Contraste : hors gen-plan, l'agent hôte suit sa consigne native d'orchestration (batch d'appels indépendants, agents concurrents) → plus de parallélisme, exécution plus rapide |
| Graph Diamond « exceptionnel » (anti-pattern « Parallélisme par défaut ») | grep graph-diamond-pattern.md v3.24.0-1 (5 occurrences « exceptionnelle/exception ») — le diamond n'était ouvert que sur justification explicite |
| Incohérence écosystème | fleet-engineering n°54 orchestrée par gen-plan (E5/E7) ; resource-monitor émet un verdict PARALLELE (niveau 0 cette session) — contraires au défaut série |

## Vérification du fix (état de sortie)

| Décision | Preuve mécanique | Statut |
|----------|------------------|--------|
| D001 — diagnostic documenté | SKILL.md contient « PARALLÈLE PAR DÉFAUT » + provenance v3.24.0 | verified |
| D002 — philosophie #4 inversée | « Parallélisme INTERDIT » absent ; nouveau #4 (parallèle par défaut sur preuve, série = exception justifiée et tracée) | verified |
| D003 — graph-diamond-pattern.md aligné | 0 « exceptionnelle » ; ouverture AUTOMATIQUE dès preuve ; anti-patterns « parallélisme sans preuve d'indépendance » + « sériographie par défaut » | verified |
| D004 — PM v3.24.0 + archive R4 | PM généré mécaniquement (1479 lignes, complétion agent 4 substitutions — delta non inventé) ; v3.23.2 archivé mv byte-identité (SHA 768e3398… scellé) | verified |
| D005 — cascade KO-L004 complète | KB/SHARED 1.7.11/PM-INSTALL 1.8.4/SYNC 1.5.4/README 2.1.12/ULTRA/journal portent les nouvelles versions ; propagation §0 (106 skills + 107 scripts + 2 agents) | verified |
| D006 — arbitres verts ×2 | answer-key-checker **16/16 ALL PASS** ; verify-cross **100.0 % (0 err/0 warn)** ; interactions **50 PASS / 1 WARN / 0 FAIL ×2** (PASS AVEC RÉSERVES) ; integrity **78/78 PASS** (manifeste écrit, archive rescellée round-trip v2.3) | verified |
| D007 — correct-work 0 S1/S2 | présent rapport | verified |
| D008 — règle d'or n°2 | HEAD dépôt inchangé (08c956c) — 0 commit, 0 push ; publication au GO | verified |

## Corrections appliquées en cours d'exécution (tracées)

1. **Citations vives stalées ×10** (mémoire/flotte/graphe/harnais/boucle/contexte/spec/refactoring-test/refactoring-engineering) : « gen-plan v3.23.2 » → v3.24.0 (arbitre interactions, KO-L003 dynamisé).
2. **refactor-guard:266** : citation historique reformulée sans jeton de version stalé (« gen-plan dans sa version courante à la date ») — l'histoire est préservée sans faux alignement (R2 + KO-L003).
3. **download/README.md parasite supprimé** (34 octets, SHA ≠ corpus — doublon détecté par l'arbitre, décision déduplication v2.2 Task 14).
4. **Écart hérité documenté** : table historique-autres-elements §1 sans lignes v1.7.9/v1.7.10 — ligne v1.7.11 insérée avec note de provenance (la table §7 du PM vivant fait foi).

## Résumé
- **Problèmes trouvés** : 0 nouveau S1/S2 ; 2 réserves S3 héritées (voir ci-dessous)
- **Réserves S3 (héritées, inchangées)** : (a) WARN interactions « worklog B1 non cloné » — artefact historique propriétaire, documenté depuis Task 22 ; (b) dérive replay gen-plan **11/12** — cas négatif « gen-plan (stp) » non discriminable par l'heuristique voie M, hérité et documenté (KB v3.22.0, verdict HEAD identique 20 dérives) — **0 nouvelle dérive** introduite par v3.24.0
- **Verdict** : **PASS AVEC RÉSERVES** (2×S3 héritées, 0 correction requise, publication au GO)
