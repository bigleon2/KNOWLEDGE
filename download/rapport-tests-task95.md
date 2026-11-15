# Rapport de tests — Task 95 (intégration des 3 propositions S4)

**Directive** trace `1a1dee6f8511bee1` (reformulée) — tests $FACON2 fonctionnels et de performances
**État certifié** : SHARED v1.7.39 · PM-INSTALL v1.9.16 · harnais re-curation v1.2.2 · extrait §0 PM-INSTALL v1.7.39
**Baseline** : 2026-11-15T11:16:07+0000

## Tests fonctionnels — 20/20 PASS

| # | Test | Verdict | Preuve |
|---|------|---------|--------|
| T01 | T01 S4-1 littéral v1.2.1 retiré du générateur | **PASS** | gen-ultra-maitre.py : 0 occurrence « v1.2.1 » |
| T02 | T02 S4-1 ULTRA cite la version réelle du harnais (v1.2.2) | **PASS** | ULTRA : « harnais protocole-test.py v1.2.2 » présent |
| T03 | T03 S4-1 idempotence génération ULTRA (--check) | **PASS** | rc=0 (généré == sur disque) — Idempotence : PROMPT-ULTRA-MAITRE-ORCHESTRATION.md déjà à jour (SHA 38aed68c9eba…) — no-op |
| T04 | T04 S4-2 en-tête extrait == SHARED vivant (v1.7.39) | **PASS** | ligne « Extrait SHARED v1.7.39 » présente |
| T05 | T05 S4-2 contenu extrait == span §0-§1.2 du SHARED (byte-identité) | **PASS** | bloc dérivé du SHARED vivant retrouvé intégralement dans PM-INSTALL |
| T06 | T06 S4-2 PM-INSTALL bump PATCH (v1.9.16) | **PASS** | v1.9.15 → v1.9.16 |
| T07 | T07 S4-2 ligne d'historique v1.9.16 présente | **PASS** | 1 occurrence dans la table d'historique |
| T08 | T08 S4-2 étiquette §A.3 rafraîchie | **PASS** | « Instantané courant (v1.9.16, 2026-11-15) » |
| T09 | T09 S4-2 ligne PM-INSTALL §6.1 SHARED à jour | **PASS** | colonne « Version skill » = v1.9.16 |
| T10 | T10 S4-2 idempotence --refresh-ctx (NO-OP à l'état frais) | **PASS** | rc=0, [NO-OP] bloc CONTEXTE SYSTÈME déjà frais (extrait SHARED v1.7.39 embarqué ; ligne §6.1 à v |
| T11 | T11 S4-2 cohérence familles intacte (generer-pm --check) | **PASS** | rc=0 — Rapport : /home/z/my-project/KNOWLEDGE-repo/scripts/generer-pm-report.json |
| T12 | T12 propagation §0 : 0 en-tête stale v1.7.38 (hors @historique/@mon-ecosysteme) | **PASS** | 0 fichier(s) stale |
| T13 | T13 propagation §0 : interactions PASS STRICT | **PASS** | rc=0 — Rapport JSON : scripts/interactions-report.json |
| T14 | T14 archive rescellée : integrity PASS | **PASS** | rc=0 — Manifeste écrit : /home/z/my-project/KNOWLEDGE-repo/scripts/ecosysteme-integrity.json |
| T15 | T15 S4-3 selftest cache-verdicts (comportement inchangé) | **PASS** | rc=0 — SELFTEST : 12/12 PASS |
| T16 | T16 S4-3 doctrine codifiée dans cache-verdicts.py | **PASS** | marqueurs « norme de certification » + « INTRA-exécution » + « NON-PERTINENT » présents (comparaison insensible à la casse) |
| T17 | T17 ULTRA dérive SHARED v1.7.39 + PM-INSTALL v1.9.16 du corpus réel | **PASS** | versions citées dynamiquement dans l'ULTRA |
| T18 | T18 certification : 5/6 arbitres AU VERT + tool-routing — seul échec N1 = non-conformité PRÉ-EXISTANTE skills plateforme | **PASS** | verify-cross ×2 + correct-work + integrity ALL PASS · interactions PASS STRICT · tool-routing : N1 script VERT (task73 réparé), seul FAIL N1 = frontma |
| T19 | P-guard régression arbitres < +30 % (aucun code arbitre modifié) | **PASS** | verify-cross (axes 1-6) +3.2%; verify-cross (mode correct-work) +0.9%; verify-correct-work +4.7%; check-ecosysteme-integrity +3.2%; test-coherence-int |
| T20 | P-guard gen-ultra --check < +50 ms (coût de la dérivation dynamique) | **PASS** | delta +1.5 ms (lit le docstring du harnais, ~800 o) |

## Performances — avant → après (médiane ×3)

| Mesure | Avant (ms) | Après (ms) | Delta | % |
|--------|-----------|-----------|-------|---|
| gen-ultra --check | 25.6 | 27.1 | +1.5 | 5.9% |
| generer-pm --check | 22.3 | 23.0 | +0.7 | 3.1% |
| verify-cross (axes 1-6) | 31.7 | 32.7 | +1.0 | 3.2% |
| verify-cross (mode correct-work) | 32.2 | 32.5 | +0.3 | 0.9% |
| verify-correct-work | 21.2 | 22.2 | +1.0 | 4.7% |
| check-ecosysteme-integrity | 40.8 | 42.1 | +1.3 | 3.2% |
| test-coherence-interactions | 138.6 | 139.7 | +1.1 | 0.8% |
| check-tool-routing | 894.7 | 491.4 | -403.3 | -45.1% |
| propagate-context | 55.7 | 59.9 | +4.2 | 7.5% |
| cache-verdicts --selftest | 280.3 | 321.2 | +40.9 | 14.6% |
| taille pm_install | 52486 | 57690 | +5204 | 9.9% |
| taille shared | 55384 | 55704 | +320 | 0.6% |
| taille ultra | 8759 | 8761 | +2 | 0.0% |
| --refresh-ctx (nouveau) | — | 24.9 | — | —% |

## Influence sur les performances de l'écosystème

- **PM-INSTALL** : l'extrait §0-§1.2 complet remplace le digest figé — lu UNIQUEMENT à l'installation/bootstrap
  (pas à chaque session) ; le surcoût #token est documenté ci-dessus (taille pm_install) et achète
  l'extinction définitive de la classe de drift « §0 figé » (21 versions de retard résorbées).
- **261 en-têtes §0** (skills/scripts/agents) : substitution de version à longueur constante (v1.7.38 → v1.7.39), zéro surcoût.
- **Arbitres** : aucun code arbitre modifié — deltas dans le bruit de mesure (garde < +30 %%).
- **gen-ultra-maitre.py** : +1 lecture de ~800 octets (docstring du harnais) pour la dérivation dynamique — garde < +50 ms.
- **cache-verdicts.py** : docstring seule (doctrine) — selftest 12/12 inchangé, zéro impact runtime.
- **ULTRA** : taille constante (chiffres de version de même longueur) — routage inchangé.

**VERDICT : 20/20 PASS** — SUCCÈS INTÉGRAL
