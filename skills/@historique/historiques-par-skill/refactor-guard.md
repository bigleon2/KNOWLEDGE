# Historique — refactor-guard (garde-fous de refactoring)

> **Objet** : lignée versionnée du skill `refactor-guard` (convention SHARED §1.2 — @historique R4). Matérialisation canonique issue de la FUSION de la discussion externe 468a4c26 (Task 8, session web-b4d7dd19).

| Version | Date | Contenu |
|---------|------|---------|
| v1.7.0 | 2026-10-12 | Task 8 — CONVERGENCE de la lignée externe (discussion 468a4c26 : double-montée Tasks 23-24 de l'instance source — 6 PM v1.2.0→v1.7.0, rollout enabled échelle H15 terminale, ledger N6, verif-finale-n6 réconcilié Task 26 « périmées-par-conception ») ; matérialisation canonique = base mécanique v1.2.0 portée à l'identique (11 scripts stdlib + evals + references ×2) + calibration de provenance ; diffs v1.3.0→v1.6.0 non verbatim consignés par preuves de discussion (R4 — réserve : PMs externes non portés, extension generer-pm 3→4 familles = décision propriétaire D009 reportée) ; arêtes bidirectionnelles ×7 (gen-plan hook E13, refactoring-engineering garde-fous, correct-work validation, resource-monitor, graph/spec/harness/loop) |
| v1.7.1 | 2026-10-23 | Optimisation du système d'installation (Task 18, session web-fdf5963c) : note §5 mécanisme dual explicitant la cohérence de ce §5 avec PM-INSTALL v1.8.0 §3.2 (ce §5 prescrit DÉJÀ l'installation directe par copie des formes certifiées — voie par défaut ; l'assemblage depuis le corpus demeure la voie bootstrap) ; PM v1.7.1 généré mécaniquement KO-L004 (complétion agent) ; recalibrage croisé SHARED v1.7.8 / PM-INSTALL v1.7.2→v1.8.0 ; PM v1.7.0 archivé `prompts-maitres/refactor-guard/` (git mv byte-identité R4) | Première montée mécanique de la 4e famille — **VERSION VIVANTE (corpus)** |
| v1.2.0 | 2026-10-10 | Première exécution N1 shadow réelle (3 cibles vivantes) + calibration grille #token §2.5 ; scripts/shadow_run.py (self-tests 79/79 ×2) — version d'origine du port hôte (contenu intégré à l'identique) |
| v1.1.0 | 2026-10-10 | Matérialisation des 8 modules C-SAFE-1 (config, audit_ledger H09, spec_builder H07, policy_engine H10, sandbox_runner H04, checker H05, human_gate H15, rollout H08) — chaîne script-creator → correct-py → script-reviewer |
| v1.0.0 | 2026-10-10 | Matérialisation initiale (projet « Skill Refactorisation Plan » — discussion Qwen T1-T46 : conception C05/C-SAFE-1, zéro-régression, gouvernance N0-N5) |

### PM canonique (2026-10-12 — décision D009)

Le PM refactor-guard entre au corpus sous décision propriétaire D009 (Task 9, session web-b4d7dd19 — gen-plan(step)) : `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md` (bootstrap — sections SKILL.md portées verbatim, ancres `generer-pm-skill.py` alignées, famille n°4). Les 6 PMs de la lignée externe (v1.2.0→v1.7.0, discussion 468a4c26) sont ACCEPTÉS non portés (non verbatim — provenance R4) ; les futures montées génèrent leur PM mécaniquement (extension generer-pm 3→4 familles, §2quater PM-INSTALL v1.6.5).
