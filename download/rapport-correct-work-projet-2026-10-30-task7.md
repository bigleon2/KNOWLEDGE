# Rapport correct-work Mode PROJET — Task 7 (contingence grille + ZIP DJTT S4 MK2 : validation & calibration trio TSI + amendement vue-upload v1.4.0)

> **Agent** : correct-work v2.8.0 (Mode PROJET — hook §5.4) · Session web-eb6c8580 · 2026-10-30
> **Objet** : vérification complète des livrables du tour — directive Task 7 (4 tâches) + directive d'amendement (discussion « Rasta Mouton » : optimisation avant tout + suggestions).

## Phase 1 — Plan (gen-plan v3.28.2, obligatoire §1.5)

Plan `download/plan-task7-contingence-grille-zip-trio-tsi.md` + **amendement 1** (G0 vue-upload v1.4.0 inséré « avant tout chose » + D013-D019 + R6) : 19 décisions D001-D019 (criterion/verification/source/priority complets), 6 groupes G0-G5 en série justifiée, verdict **E8 PASS** (answer-key-checker 16/16 arbre publication ; check_plan_protocol P1-P5 PASS, verdict frais). Estimation #token amendée ~43 k.

## Phase 2 — Exigences (4 + 2) et alias-eco

| Exigence | Preuve | Statut |
|---|---|---|
| Contingence « récupération externe bloquée ×3-4 » → grille #token gen-plan | grille-token.md coefficient 3-4x v3.28.2 + row 14 (preuve E15 Task 6) + puce §4 SKILL + PM v3.28.2 + cascade complète ×2 arbres | ✓ satisfaites |
| Analyse du ZIP (objet des tâches suivantes) | analyse-tsi-reel.py + rapport 5 sections ×2 arbres (inventaire, structure DIOM, mappings, VLM ×3, écart spec↔réel) | ✓ satisfaites |
| Validation des agents TSI | rapport validation ×2 arbres (verdicts bruts ×3, crash consigné, audit architect, self-tests golden ×2) | ✓ satisfaites |
| Calibration midi-doc-expert + tsi-validator | v1.1.0 ×2 + décodeur R4 + verdict réel PASS 5 626 mappings + doc 100 % + replay trio 6/6 ×3 inchangé | ✓ satisfaites |
| (Amendement) Optimisation écosystème issue de la discussion, AVANT tout | vue-upload v1.4.0 épinglage + journal — test 16 checks, G0 exécuté en premier | ✓ satisfaites |
| (Amendement) Suggestions skills/agents $facon | 3 candidates fondées (hygiène des versions, livraison-garantie, qa-animation) — worklog + chat | ✓ satisfaites |

Alias-eco : registre consulté (7 phrases) — discussion à message unique, 0 nouvelle phrase récurrente.

## Phase 3 — Structure

- **verify-cross (dépôt)** : **117/117 PASS ×2 exécutions** (axes 1-6 + mode correct-work) — 100 %.
- **Garde anti-doublons download/** : 0 doublon (142 + 3 nouveaux rapports = uniques).
- **Projections hôte ≡ dépôt** : gen-plan (SKILL + grille + PM) ✓, vue-upload (SKILL + scripts + evals) ✓, KB ✓, arbitre ECO ✓ — vérifiés par SHA lors du correct-work(G0+G1).
- **Hiérarchie trio** : tsi-validator détenteur R4 du décodeur, midi-doc-expert dépendance YAML déclarée — cohérent.
- **T2.5 sweep** : 106+ en-têtes §0 SHARED v1.7.14 + citations gen-plan vivantes v3.28.2 — 2 corruptions de changelog historique détectées et **réparées** (R2 append-only : « v3.28.1→v3.28.2 » restauré ×4 fichiers, corpus byte-identique à HEAD).

## Phase 4 — Interactions

- **test-coherence-interactions** : **51/52 PASS** (1 WARN hérité by design — worklog B1 artefact propriétaire non cloné, statu quo Task 6).
- **check-ecosysteme-integrity** : **82/82 ×2 arbres** (manifestes rescellés, archives round-trip v2.3).
- **check-triggers-replay** : **47/47 skills au score maximal, verdict PASS** — vue-upload 9/9, trio 6/6 ×3, dérivées voie-M-seule = 5 héritées Task 30 (aucune nouvelle après les éditions de descriptions v1.4.0/v1.1.0).
- **check-tool-routing** : 5/5 (couche courante propre après commits).
- **Dépendances** : vue-upload→gen-plan (É1-INSTALL) ✓ ; midi-doc-expert→tsi-validator >=1.1.0 (décodeur) ✓ ; planchers semver respectés.

## Phase 5 — Cohérence

- Chiffres re-calculés indépendamment : 5 626 assignations ≡ analyseur ≡ validateur ≡ doc générée (100 %) ; 163 contrôles, 394 commandes, 345 conditions ≡ rapport G2 ≡ §6bis.
- Answer key : **19/19 traitées** — 17 re-vérifiées mécaniquement à la relecture (D001-D009, D011, D013-D017, D019), D010 push DIFFÉRÉ (PAT absent du contexte — fallback D019 : commits locaux prêts 652b193→4a5619f, demande de re-provision adressée), D012/D018 accomplies en clôture (clone + suggestions).
- Promis vs livré : directive 4 tâches + amendement 3 volets — tous livrés ; périmètre tsi-architect respecté (hors calibration, per directive).
- Corrections de vérificateurs tracées (pattern Task 5) : D002/D003 casse, D009 statu quo 5 héritées, race test v1.4.0 (poll), phrasing D004 — critères JAMAIS modifiés.

## Verdict

**PASS (0 S1, 0 S2)** — 3 constats S4/cosmétiques documentés : ① sondage pré-vol initial (158 CMAI) corrigé honnêtement dans le rapport G2 ; ② push différé (PAT absent — décision propriétaire attendue) ; ③ échantillon réel 1,8 Mo hôte seul (hors dépôt, statu quo trio).

*Rapports fils : correct-work CIBLE G0+G1 (18 checks), G2 (8), G3 (7), G4 (11) — tous PASS.*
