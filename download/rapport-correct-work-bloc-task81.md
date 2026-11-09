# Rapport correct-work (projet) --bloc — Task 81 (G5, D007)

**Mode** : correct-work v2.11.0, `--bloc` — revue par blocs B1-B4, agrégation pire-des-verdicts, max 2 rounds/bloc. **Session** : web-ecef7f80, 2026-11-09 — traces directives 1a1bcf4fecbf5f29 + reprises « continue $FACON et de façon autonome » (1a1bdfca428d2fc9, 1a1be05af2520149) + réinstallation préalable explicite ×2.

---

## B1 — Installation + certification

| Vérification | Attendu | Mesuré | Verdict |
|---|---|---|---|
| Réinstallation locale (directive propriétaire ×2) | pipeline rc=0 | eco_install_pipeline rc=0 ×2 — **54/54 SHA-256, 0 divergence, garde R2, archive round-trip v2.2** | PASS |
| Volatilité à l'ouverture (règle d'or n°9) | profil complet | gen-plan VIDE + version-management ABSENT à l'ouverture → **rétablis même passe** (récidive documentée Tasks 56/72/75/79/81) | PASS |
| Integrity dépôt | 112/112 | **112/112 PASS, manifeste écrit** (pins re-curation 1.2.1 + iphone19 0.12.0 alignés) — après rescellage dépôt (leçon scellé hôte≠dépôt) | PASS |
| G-RES (ressources) | OK / niveaux 0 | monitor.py : disque 0 · mémoire 0 · charge 0 → **OK (PARALLELE)** | PASS |

**B1 : PASS** (0 round consommé).

## B2 — Corpus + KB + outillage

| Vérification | Attendu | Mesuré | Verdict |
|---|---|---|---|
| Corpus PM | 4/4 COHERENT | generer-pm-skill.py --check : GEN-PLAN v3.41.0 · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1 — **4/4** | PASS |
| KB | entrées alignées | `## iphone19 v0.12.0` (calibrée règle 15 + re-curation, écart C4 documenté) · `## re-curation v1.2.1` (cibles recalées → iphone18 prochaine) | PASS |
| Pins ECO_SKILLS | 0.12.0 / 1.2.1 | check-ecosysteme-integrity.py pins alignés — 112/112 | PASS |
| ULTRA | régénéré + idempotent | SHA 333685c648ec… régénéré (G2) puis **no-op** (G4) — idempotence prouvée | PASS |
| Archive d'intégrité | corpus 9/9 round-trip | rescellée v2.2 **hôte+dépôt** — 9/9, 0 divergent (piliers retirés par conception 2026-10-23, RETRAITS_SANCTIONNES) | PASS |
| Arbitres 5/5 | rc=0 partout | verify-cross **100,0 %** · answer-key-checker **16/16** · doublons **0** (281 uniques) · interactions **55/55 PASS STRICT** · integrity **112/112** | PASS |
| SYNC-CONTEXT | v1.5.8 | resync état Task 80+81 — porteurs **187/192** mesurés, citations ↔ corpus | PASS |

**B2 : PASS** (0 round).

## B3 — Livrables session 81

| Vérification | Attendu | Mesuré | Verdict |
|---|---|---|---|
| Plan Task 81 | E8 initial + answer key | E8 initial PASS 2026-11-08T21:25:00Z · **D001-D006 verified** (D004 avec écart C4 consigné) · D007-D008 en clôture | PASS |
| Harnais protocole-test v1.2.1 | selftest ×2 idempotent | **14/14 ×2 rc=0** (13→14 cas — correctif idempotence POST) | PASS |
| SKILL.md iphone19 | re-curé, contrats intacts | 55 645 → **40 430 o (−27,3 %)**, 6 references/ R4, version inchangée, Lignage « projection curée » ; règle absolue 15 ×4 + QC 14 ×5 en texte | PASS |
| Preuves re-curation | PRE GO + POST ×2 + C1-C4 | PRE GO v0.12.0 · POST **MAINTIEN ×2** (runs 5-6 rc=0, empreinte identique, perf stable) · **R4-INTÈGRE 6/6** · C1-C3 PASS · **C4 écart consigné** (justification mesurée) | PASS |
| Campagne de tests | rapport chronologique | download/rapport-campagne-tests-task81.md (profil+dépôt) — **15/15 éléments PASS**, jeton complet 0 occurrence | PASS |
| Worklog R5 | frais + conformité disque | suites 76-80 (réinstallation, G2, G3, G4) + marqueurs PLAN-AFFICHE — **dépôt == profil 1 879 lignes** | PASS |
| Commit local Task 81 | présent, arbre propre | **ca7aada** (31 fichiers — règle 15, re-curation, harnais v1.2.1, SYNC v1.5.8, F-a éteinte) | PASS |

**B3 : PASS** (0 round).

## B4 — Extension / pendances

| Vérification | Attendu | Mesuré | Verdict |
|---|---|---|---|
| FAILLE F-a (worklog dépôt stale) | éteinte avant PUSH | **ÉTEINTE** — préfixe strict vérifié avant copie, dépôt ← profil, diff identiques (1 879 lignes) | PASS |
| SYNC-CONTEXT lag | v1.5.8 couvrant Task 80+81 | résorbé (lag inerte — citations restées cohérentes, T3 campagne) | PASS |
| Pendances antérieures | éteintes | baselines v1.2.0 (Task 80) ✓ · comparateur §0 v1.1.0 ✓ · aucune pendance héritée restante | PASS |
| Leçons du jour | consignées | L-81-a (reprise WIP : mesurer avant écrire) · L-81-b (scellé hôte≠dépôt) · L-81-c (idempotence POST v1.2.1) · L-81-d (écart consigné vs contorsion) | PASS |
| Écart C4 | documenté + tracé | KB + historique par-skill + worklog suite 78 + answer key D004 — mesure de non-évitabilité (contrats ≈ 12,5 Kio + cœur ≈ 18 Kio vs seuil 30 Kio) | PASS |
| Calibration answer key | décompte réel | plan D007 « 10/10 » (hérité Task 80) → **8 décisions D001-D008** — E8 FINAL vérifie 8/8 (calibration documentée, aucune décision perdue) | PASS |
| E15 | consignation push | 5ᵉ exposition PAT à consigner au G6 (2026-10-26 · 2026-11-07 · 2026-11-08 ×2 · 2026-11-09) — RÉVOCATION/ROTATION recommandée | PASS (G6) |

**B4 : PASS** (0 round).

---

## Agrégation (pire-des-verdicts)

| Bloc | Verdict |
|---|---|
| B1 Installation + certification | PASS |
| B2 Corpus + KB + outillage | PASS |
| B3 Livrables session 81 | PASS |
| B4 Extension / pendances | PASS |

**VERDICT correct-work (projet) --bloc : PASS — 4/4 blocs, 0 S1, 0 S2, 0 round de correction consommé.** Aucun finding bloquant ; 1 écart consigné (C4 — documenté, mesuré, tracé) ; 1 calibration de décompte (8 décisions vs « 10/10 » hérité) ; leçons L-81-a…d vers knowledge-observer.

*Rapport généré par correct-work v2.11.0 --bloc — Task 81 G5 (D007), session web-ecef7f80, 2026-11-09.*
