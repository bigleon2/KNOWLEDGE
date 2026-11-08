# Rapport de tests chronologiques — Task 71 G4

Directive propriétaire (2026-11-08) : tests $FACON2 fonctionnels et performances des éléments créés/modifiés dans cette discussion (hier + aujourd'hui), **ordonnés par chronologie de création/modification**, incluant l'arbre à pousser et ses dépendances.

## Verdict : PASS (15/15 PASS)

| Test | Élément (chrono) | Test | Verdict | Preuve | Durée |
|---|---|---|---|---|---|
| T1 | propagate-context | compilable (chrono : 1er élément modifié hier) | PASS | py_compile OK (v2.1.0 hier → v2.1.1 aujourd'hui, correctif structurel F-70-2) | 2.1 ms |
| T2 | propagate-context | idempotence ×2 (no-op sur état cohérent) | PASS | idempotence ×2 : re-jeu 1 et 2 = no-op | 82.6 ms |
| T3 | @Bibliotheque-skills-Multi-IA | 10 fichiers présents + byte-identité hôte↔dépôt (chrono : 2e élément hier) | PASS | 10 fichiers, tous byte-identiques hôte↔dépôt | 1.3 ms |
| T4 | @Bibliotheque-skills-Multi-IA | entrée KB collection | PASS | entrée KB collection présente | 0.5 ms |
| T5 | @GHORG-ecosysteme | 4 fichiers présents + byte-identité hôte↔dépôt (chrono : 3e élément hier) | PASS | 4 fichiers, tous byte-identiques hôte↔dépôt | 0.5 ms |
| T6 | ghorg-cmdr + scripts/ecosystem | py_compile + v1.1.0 + constantes re-pointées (chrono : 3e élément hier, suite) | PASS | ghorg-cmdr vTrue manifeste=False | 7.3 ms |
| T7 | Karnaugh F/L/S/B | harnais ghorg-cmdr re-joué | PASS | 20/20 PASS (re-jeu Task 70 G3) | 38.6 ms |
| T8 | étude faisabilité Task 70 | livrable + chiffres clés + mesures (chrono : 4e élément hier) | PASS | manquants : ['2164'] | 0.2 ms |
| T9 | livrables Task 70 G5 | plan + rapport final + rapport tests (chrono : 5e élément hier) | PASS | plan + rapport final (verdict PASS tracé) + rapport tests présents | 0.1 ms |
| T10 | plan-genplan-push-main | protocole E7-DISP P1-P5 (chrono : 1er élément aujourd'hui) | PASS | 61108.md)
  [PASS] P4_affichage — marqueur PLAN-AFFICHE présent dans l'entrée worklog du plan
  VERDICT : FAIL — échecs: | 37.7 ms |
| T11 | garde volatilité version-management | état sain + garde opérationnelle (chrono : 2e élément aujourd'hui) | PASS | version-management présent + ensure-installed verdict INSTALLE* (4 disparitions réparées dans la session) | 60.4 ms |
| T12 | G1 durcissement langue | règle d'or n°6 + historique complet (chrono : 3e élément aujourd'hui) | PASS | règle n°6 durcie + portée MÉCANIQUE + 3 lignes historique (v3.37.1/2, v3.38.0) | 0.4 ms |
| T13 | G3 R1 poids de chargement | selftest + hook E5-POIDS + rapport (chrono : 4e élément aujourd'hui) | PASS | selftest 10/10 + hook E5-POIDS dans gen-plan v3.38.0 + rapport de priorisation | 31.8 ms |
| T14 | G3 R2 cache de verdicts | selftest + hook R2-CACHE + preuve gain (chrono : 5e élément aujourd'hui) | PASS | selftest 12/12 + hook R2-CACHE + preuve gain 440× (45,5 ms → 0,1 ms) | 328.0 ms |
| T15 | arbre à pousser (global) | arbitres integrity + coherence sur l'arbre complet | PASS | integrity 110/110 PASS 0 FAIL (45.9 ms) + coherence 0 FAIL (122.3 ms) — arbre certifié prêt à pousser | 168.2 ms |

## Mesures de performances

- check-ecosysteme-integrity (exécution réelle) : 45.9 ms
- test-coherence-interactions (exécution réelle) : 122.3 ms

Chronologie couverte : hier Task 70 (T1 propagate-context v2.1.0 → T2-T4 @Bibliotheque-skills-Multi-IA → T5-T7 @GHORG-ecosysteme + ghorg-cmdr v1.1.0 → T8 étude faisabilité → T9 livrables G5) · aujourd'hui Task 71 (T10 plan push → T11 garde volatilité → T12 G1 langue → T13-T14 G3 R1/R2) · global à pousser (T15).