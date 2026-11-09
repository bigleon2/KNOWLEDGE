# Catalogue des signaux H01-H15 (projet « Skill Refactorisation Plan »)

> Source : discussion Qwen T7-T9 (15 hypothèses d'intégration, scores méthodologiques
> « simulation logique et méthodologique » — aucun benchmark matériel réel revendiqué,
> avertissement d'honnêteté conservé). Adapté à l'écosystème d72226a+ (2026-10-10).

## 1. Les 15 hypothèses (par score décroissant)

| ID | Hypothèse | Score | Statut dans refactor-guard v1.0.0 |
|----|-----------|-------|-----------------------------------|
| H04 | Sandbox obligatoire (exécution isolée avant application) | 9.4/10 | **Actif** (R5 — harness-engineering) |
| H02 | Graphe de dépendances (détection par structure) | 9.1/10 | **Actif** (R2 — scripts/graph_scan.py) |
| H05 | Maker-checker (vérification systématique par instance distincte) | 9.0/10 | **Actif** (R7 — loop-engineering) |
| H10 | Fitness architecturales (métriques cibles mesurables) | 8.9/10 | **Actif** (contrats §1.5 SKILL.md) |
| H15 | Human-in-the-loop (GO explicite pour application réelle) | 8.6/10 | **Actif** (N4 + règle d'or push) |
| H07 | Spécification formelle (refactorisation = contrat exécutable) | 8.5/10 | **Actif** (R4 — spec-driven-development) |
| H14 | Score de risque pondéré | 8.4/10 | **Actif** (R3 — scripts/risk_score.py) |
| H09 | Audit log exhaustif (chaque pas écrit, byte-level fait foi) | 8.3/10 | **Actif** (R8 + worklog) |
| H08 | Rollout progressif (petits pas réversibles) | 8.2/10 | **Actif** (N5 canary) |
| H06 | DAG externe (ordonnancement par graphe acyclique) | 8.0/10 | **Reporté** (graphe interne suffisant v1) |
| H11 | Tests de non-régression rejoués (baseline vs candidat) | 7.9/10 | **Actif** (R5/R7 — couche tests_required) |
| H01 | Signaux fleet-engineering (charge, concurrence d'agents) | 7.6/10 | **Passif** (jamais déclencheur seul — asymétrie T5) |
| H12 | Mémoire inter-sessions (historique des refactorisations) | 7.4/10 | **Passif** (worklog fait foi ; consolidation future) |
| H13 | Pipeline multi-agents (fan-out de scans) | 7.2/10 | **Reporté** (futures sessions, KO-L001 souverain) |
| H03 | Code smells (détection heuristique de motifs) | 6.8/10 | **Passif** (faux positifs — lecture seule uniquement) |

## 2. Combinaisons testées (T8 — C01-C12 sur scénarios S1-S4)

- **C05 = H02+H04+H05+H07+H10+H14 — MEILLEURE (9.6/10)** : le noyau gardé.
- **C-SAFE-1 = C05 + H09 + H15 + H08 — retenue pour v1.0.0** : noyau + audit + humain + rollout.
- **Combinaison maximale (toutes actives d'un coup) — REJETÉE (7.6/10)** : « À ne pas activer d'un coup » — complexité de gouvernance non maîtrisée.
- **C12 = H01 + H03 sans H04 ni H14 ni H15 — DANGEREUSE (2.0/10)** : « À éviter absolument » — refactorisation sans sandbox, sans scoring, sans humain.

## 3. Synergies fortes documentées (T8)

| Synergie | Effet |
|----------|-------|
| H02 + H10 | Le graphe fournit les métriques, la fitness fixe les seuils cibles |
| H04 + H05 | La sandbox exécute, le maker-checker vérifie — boucle de confiance |
| H07 + H05 | Le contrat définit ce que le checker doit vérifier (critères mécaniques) |
| H14 + H15 | Le score pilote le niveau de gouvernance ; l'humain tranche les cas ≥ 6 |
| H09 + H11 | L'audit consomme les résultats des tests rejoués — preuve traçable |

## 4. Anti-patterns (10 pratiques à éviter, T7 — extrait structurant)

1. Refactoriser sans baseline mesurée préalable (impossible de prouver la non-régression).
2. Activer tous les niveaux de gouvernance d'un coup (rejet de la combinaison maximale).
3. Laisser un agent appliquer une refactorisation critique sans GO humain (H15 violé).
4. Confondre signal passif (H01/H03) et déclencheur (H02/H14) — l'asymétrie T5 fait règle.
5. Écrire directement sur les cibles (sandbox obligatoire — H04).
6. Omettre le plan de rollback (rollback_required).
7. Benchmarks revendiqués sans mesure réelle (leçon d'honnêteté T37/Qwen : « métrique inventée » — toute mesure doit être produite par exécution réelle, byte-level fait foi).
8. Dupliquer les arbitres existants (R4 — réutiliser check-ecosysteme-integrity.py, verify-cross.py, etc.).
9. Refactoriser pendant une phase audio temps réel (realtime_guard — pause_analysis_during_live).
10. Rétrograder un niveau de gouvernance sans cause documentée (R2).

## 5. Prolongements

Le catalogue évolue par propositions argumentées (score + justification), jamais par suppression silencieuse (R2). Toute nouvelle hypothèse rejoint le registre avec son statut (actif/passif/reporté/rejeté) et sa preuve. Provenance : projet Qwen « Skill Refactorisation Plan » (clone `download/ecosystem-corrections-clone-2026-10-10.md`), matérialisé dans l'écosystème Knowledge le 2026-10-10.
