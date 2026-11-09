# Rapport correct-work (projet) --bloc — Task 84

> **Mode PROJET** · correct-work v2.11.0 · session web-ecef7f80 · 2026-11-09 · directive trace `1a1bed51ccaf78f1`
> Périmètre : campagne tests $FACON2 chronologique (G2) + inscription socle discipline n°56 (G3) + clôture (G4-G5)
> Agrégation : pire-des-verdicts · garde anti-boucle 2 rounds (SHARED §4.4) — **0 round consommé**

## B1 — Installation + certification : **PASS**

- É1-INSTALL ouverture : **INSTALLE-REPARÉ rc=0** (version-management — volatilité environnementale récurrente documentée, auto-réparation miroir, kb_entrees 55, 0 manquant après).
- Pipeline pleine passe ×4 dans le tour (campagne C10c · G3 ×2 · clôture) : **rc=0 · 55/55 SHA-256 · divergences [] · garde R2 0 rétrogradation · archive round-trip corpus 9/9** à chaque passe.
- G-RES : OK (3 indicateurs niveau 0, ouverture et clôture).
- ensure-installed --check final : INSTALLE, `"skills_kb_manquants": []`.

## B2 — Corpus + KB + outillage : **PASS**

- **Corpus 9 fichiers** : GEN-PLAN **v3.42.0** (PM généré mécaniquement, delta verrouillé `scripts/delta-genplan-v3420.json`, couverture SKILL↔PM OK) · SHARED **v1.7.37** (§7 n°56 inscription + §6.1 recalibrés) · PM-INSTALL **v1.9.14** · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1 · ULTRA (SHA 2ed4ec470abc ×2 idempotent) · README corpus v2.1.22 · **SYNC-CONTEXT v1.5.11** (compteurs MESURÉS : 120/120 SKILL.md porteurs · 4 .agent · **200/200 scripts porteurs — couverture TOTALE**).
- Générateur --check : **4/4 COHERENT**. Archive : PM v3.41.0 archivé R4 `git mv` (sceau f0a44d495519c3df…) — archives gen-plan 46, total 4 familles 58 — RETRAITS_SANCTIONNES += v3.41.0.
- **Arbitres 5/5** : verify-cross **100,0 %** · interactions **PASS STRICT 55/55 · 0 WARN · 0 FAIL** (arête gen-plan↔n°56 désormais bidirectionnelle complète) · vcw **16/16** · integrity **114/114** (round-trip corpus 9/9, manifeste DUALS pins 3.42.0 ×2 arbres) · corpus PM --check 4/4.
- Parité zip hôte==dépôt : **2619e9f48e9f6bd9** (ordre canonique L-82-b/L-83-a : seal pipeline → cp → manifeste).
- Propagation §0 v1.7.37 : 120 skills + 197 scripts + 4 agents (passe 1) → passes 3-4 **convergée 0/0/0** ; lot §0 campagne : parité hôte==dépôt 12/12 + 3 scripts G3 absorbés (couverture 200/200).

## B3 — Livrables Task 84 : **PASS**

- Plan FINAL E8 (`download/plan-task84-campagne-tests-chronologiques-socle-n56-push.md` — answer key **12/12 verified**, P1-P5 PASS, horodatages couplés 07:42:00Z, #token estimé ≈ 33 000).
- **Campagne chronologique** : `scripts/task84-campagne-tests.py` (orchestrateur, 21 items C1-C21, reproductible idempotent) + rapport `download/rapport-campagne-tests-task84.md` (profil+dépôt) + JSON `scripts/task84-campagne-tests.json` — **round 1 : 40/51 MESURÉS (11 FAIL) → 3 failles réelles corrigées + 7 calibrages harnais → round 2 : 52/52 PASS rc=0 (3,5 s)**. Failles : (1) propagation §0 en retard — 11 scripts Tasks 78-82 + gabarit n°56 périmé → absorbés, passe 2 no-op, parité 12/12 ; (2) invariants périmés task82-tests-conversions T4b/T6 → dynamisés KO-L003 (T6a noyau byte-identique au CLOSE 95fef2b + T6b périmètre ⊆ commit), re-jeu 9/9 ; (3) ordre interne pipeline (dry-run certifié sur état synchronisé — garde F3 prouvée par détection d'une divergence transitoire réelle).
- **Socle n°56** : `scripts/task84-socle-n56.py` (amendement chirurgical, budget garde prouvé : 1ᵉʳ passage ABANDONNÉ rc=2 à 30 833 o > 30 719, compensation → 30 644 o) + `scripts/delta-genplan-v3420.json` (delta verrouillé) + `scripts/task84-cascade-socle.py` (mécanique 9 surfaces) + `scripts/task84-sweep-citations.py` (9 citations vives recalées v3.42.0 + KB « Dépend de » += n°56) — PM v3.42.0 1 818 lignes, archives 46, KB 55 entrées bidirectionnelles, ULTRA 2ed4ec47, propagation convergée.
- **verifiers POST** : `--verifier gen-plan` **VERDICT PASS** (v3.42.0 · 29,9 Kio · 7 661 #token INTERMÉDIAIRE — allégé de 13 #token vs v3.41.0) · `--verifier re-curation` PASS · harnais selftest 15/15 ×2 · conversions 9/9.
- Clone-chat scellé `download/clone-chat-session-web-ecef7f80-20261109-task84.md` (§0-§5, 8 checks S1-S8, 0 secret).

## B4 — Extension / pendances : **PASS**

- P1 inscription socle n°56 (pendance Task 83) : **ÉTEINTE** — SHARED §7 v1.7.37 + gen-plan v3.42.0 §1.6/§3 + cascade complète.
- Cadence 2 h : tâche planifiée native **job 516921** (fixed_rate 7200 s, message {réinstalle avant toute chose ; continue $FACON}, **0 jeton dans le payload**).
- Failles du tour : **6/6 éteintes** (propagation §0 ×12, invariants T4b/T6, ordre pipeline, budget garde amendement, asymétrie interactions, citations stale ×9).
- Pendances honnêtes R5 : **P2 file re-curation** [skill-creator PROCHAINE → web-reader → cahier-des-charges → iphone17 — serviced par cadence 2 h] · **baseline A2 n°56** [R3 — QUOTA_OK, KO-L001] · **rotation PAT** [propriétaire].
- E15 : PAT utilisé pour le PUSH final (instruction permanente de la discussion — KO-L009 levée, zéro-persistance stricte ×2, **7ᵉ exposition consignée**).

## Verdict agrégé : **PASS** (4/4 blocs · 0 S1 · 0 S2 · 0 round consommé)

Conformité worklog ↔ disque vérifiée (entrées suites 99-102, marqueurs PLAN-AFFICHÉ ×4, statuts dérivés des verdicts réels). Le présent rapport est le livrable de contrôle du mode PROJET — agrégation pire-des-verdicts : B1 PASS · B2 PASS · B3 PASS · B4 PASS → **CHAÎNE TASK 84 : PASS**.
