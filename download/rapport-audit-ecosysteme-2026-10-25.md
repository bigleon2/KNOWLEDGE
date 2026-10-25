# Rapport d'audit complet — Écosystème Knowledge (profil local)

> **Session** : web-eb6c8580 (suite) · 2026-10-25 · **Directive propriétaire** : « fais un audit complet de mon écosystème (inclus dedans un test pour comprendre le bug "GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0") »
> **Plan d'actions** : `download/plan-task2-audit-ecosysteme.md` (gen-plan v3.23.1 — E1-E15, Phases A-D, série stricte, hooks correct-work par phase)
> **État audité** : écosystème installé le 2026-10-25 depuis `bigleon2/KNOWLEDGE` @ `b75a62066791a8cce8c1ec5d1dbe7d976bae4244` (PM-INSTALL v1.7.1, pipeline 11 étapes) — 9 corpus, `@historique/` (24 PMs archivés scellés SHA-256), 33 skills écosystème, registre KB 33 entrées, outillage 160 scripts compilables, archive d'intégrité v2.3 (15 entrées scellées)
> **Verdict consolidé** : **PASS AVEC RÉSERVES** — 7 drifts traités (3 CORRIGÉ, 4 JOURNALISÉ avec propositions), bug v3.24.0 diagnostiqué (canal canonique exonéré, faille « complétion agent » identifiée, correctif proposé), zéro-régression prouvée à chaque phase

## §1 — Périmètre & méthode

L'audit couvre l'intégralité de l'état installé tel que défini par la décision D001 du plan (answer key exécutable, spec de session — spec-driven n°54) : corpus certifié b75a620, archive documentaire @historique, formes installées des 33 skills écosystème, registre KB, outillage scripts/, evals et trigger_evals. L'exécution suit la série stricte A→B→C→D imposée par le plan (Graph Diamond interdit — C dépend du diagnostic B, D dépend de tous), avec un hook `correct-work(mode=CIBLE)` après chaque phase et `correct-work(mode=PROJET)` en fin de chaîne. Chaque phase a scellé un golden master avant opération et re-certifié les 6 arbitres après (doctrine refactoring-engineering R2/R4 — zéro-régression D007).

## §2 — Phase A : audit structurel & certification (E9)

**Certification complète re-jouée : 6/6 arbitres verts, PASS AVEC RÉSERVES, exit 0** (D001, D002) — verify-cross axes 1-6 : 99/99 ; verify-cross mode correct-work : 99/99 ; verify-correct-work : 16/16 ; check-ecosysteme-integrity : 70/70 ; test-coherence-interactions : 47/48 (1 avertissement — drift d, voir §3) ; check-tool-routing : 5/5. Le rejeu confirme l'état d'entrée installé ce jour : aucune régression entre l'installation (Task 1) et l'audit.

**@historique byte-identité** : 24/24 fichiers archivés conformes à leur sceau SHA-256 de l'index §5 (nouvel arbitre `scripts/audit-phaseA-historique.py`, ALL PASS après correction — voir §3). Les 24 PMs archivés (19 gen-plan v3.6.1→v3.23.0, 4 correct-work v2.4.0→v2.6.0, 1 clone-chat v2.0.0) n'ont subi aucune édition (R2) — preuve par re-calcul intégral des sceaux.

**Rejeu des triggers (voie M)** : `check-triggers-replay.py` — 26/43 skills au score maximal, 17 en dérive (drift f, §3). Point critique pour le bug : **gen-plan 11/12** — toutes les demandes canoniques de plan (« Élabore le plan d'action structuré », « Intègre dans le plan d'actions », modes step/step-ok) routent correctement à l'état v3.23.1 ; le seul échec est le cas négatif « gen-plan (stp) » (mode invalide qui ne doit PAS déclencher — faux positif de la réplique mécanique, hérité v3.22.0).

**Autres axes** : py_compile 160/160 (0 échec) ; graphe KB bidirectionnel (« Dépend de » ↔ « Utilisé par ») vérifié par test-coherence-interactions §3 — PASS ; structure frontmatter 33 SKILL.md (verify-cross) ; registre ↔ frontmatter ↔ ECO_SKILLS (check-ecosysteme-integrity) — conformes.

**Hook correct-work(CIBLE) Phase A : PASS AVEC RÉSERVES** (3 constats : dérives voie M, drift documentaire index §5, worklog B1).

## §3 — Phase B : audit des drifts & lignée (E10)

### §3.1 — Tableau des drifts (statut × 7, aucun laissé sans statut — D008)

| # | Drift | Diagnostic | Statut |
|---|-------|-----------|--------|
| a | `verify-correct-work.py` référence `PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md` (PM_PATH, ligne 19) alors que le corpus porte v2.7.0 — l'arbitre valide contre un contrat PM périmé (16 checks = table §6 de v2.5.1) ; non bloquant (16/16 ALL PASS) | Hérité de l'état certifié du dépôt ; le recalibrage exigerait de réécrire les checks sur la table §6 de v2.7.0 (couplage gen-plan obligatoire) — refactoring d'un arbitre certifié | **JOURNALISÉ** — proposition §5.1 |
| b | `certification-complete.py` invoque `verify-cross.py --mode correct-work` mais `verify-cross.py` (162 L) n'implémente aucun parsing d'arguments — l'arbitre 2 est une ré-exécution identique au mode défaut (99/99 deux fois) | Hérité (S4, rapport installation Task 2) ; institutionnel : le doublon est cosmétique, pas erroné | **JOURNALISÉ** — proposition §5.2 |
| c | Fragments plateforme post-b75a620 : §0 alias-eco (SHARED v1.7.10) et cahier-des-charges (v1.7.8) ≠ v1.7.7 installé | Résorbé à l'installation (Task 1 incident §3.4 n°3) : marqueurs §0 alignés v1.7.7 — vérifié ce jour (§0 v1.7.7 des deux côtés) ; la valeur documentaire de lignée est conservée §3.2 | **CORRIGÉ** (installation) |
| d | Worklog B1 : l'arbitre interactions attend que le worklog local porte l'historique B1 (v3.11.0 + PEK, 2026-09-10 — artefact historique propriétaire) — le profil local a démarré un worklog neuf (WARN 47/48) | Choix de design : la lignée B1 vit chez le propriétaire (worklog d'origine, jamais cloné) ; le porter au profil local est une décision de architecture propriétaire, pas un défaut d'installation | **JOURNALISÉ** — proposition §5.3 |
| e | Index §5 @historique : en-tête « 21 PMs » vs 23 lignes vs **24 fichiers réels** (clone-chat v2.0.0 archivé Task 12 jamais indexé) ; parseur de l'arbitre figé sur les familles gen-plan/correct-work (KO-L003) | Drift documentaire + invariant non dynamisé | **CORRIGÉ** — en-tête 24, ligne clone-chat scellée (SHA `403435c9…`), compléments Task 8/Task 12 documentés, parseur recalibré (familles génériques + couverture croisée index ↔ disque) → arbitre ALL PASS |
| f | `check-triggers-replay` : 17/43 skills en dérive voie M (gen-plan 11/12 — seul échec = cas négatif « stp » ; agent-creator, prompt-engineering, refactoring trio, iphone*, vue-upload, version-management…) | La réplique mécanique (SHARED §7 v2) est plus stricte que le routage réel LLM ; les trigger_evals d'époque portent des attendus postérieurs à la réplique ; **non intégrée aux 6 arbitres de certification** (aucun blocage) | **JOURNALISÉ** — proposition §5.4 |
| g | Couche @historique en retard de 3-4 versions sur chaque table : SHARED documenté ≤ v1.7.4 (corpus v1.7.7), PM-INSTALL ≤ v1.6.3 (corpus v1.7.1), SYNC-CONTEXT ≤ v1.4.7 (corpus v1.4.9), README ≤ v2.1.4 (corpus v2.1.7) ; instantané KB « 30 entrées » vs table 32 vs registre vivant 33 (gen-plan v3.23.0, clone-chat v2.0.0, refactoring trio v1.0.x, dessin-technique absent) ; README §2 (familles, comptes archivés, « 3 familles » sans refactor-guard) ; marqueur « VERSION VIVANTE » résiduel sur v3.23.0 ; lignes « Fichiers archivés de la famille » périmées (gen-plan 18→19, clone-chat 0→1) | Les montées Task 8/9/PM-INSTALL-directive/Task 12 (2026-10-12, dernières pré-commit b75a620) n'ont pas déclenché la mise à jour documentaire @historique (procédure §4/§7 non exécutée — le recalibrage croisé KO-L004 ne couvre pas @historique) | **CORRIGÉ** — 12 lignes ajoutées (sources : en-têtes Révision vivants + PM-INSTALL §7, dates consensuelles 2026-10-12 ; coquille de date §7 v1.7.1 « 2026-10-11 » consignée), instantané KB rafraîchi 33 entrées + dessin-technique, README §2 recalibré (4e famille refactor-guard ajoutée), marqueurs VIVANTE corrigés → arbitre ALL PASS + re-certification 6/6 |

**Preuves de correction (g/e)** : golden master des 4 fichiers scellé avant édition (`scripts/audit-phaseB-golden-avant.txt`) ; seuls les 4 fichiers de documentation vivante modifiés — les 24 PMs archivés intacts (R2) ; l'archive d'intégrité v2.3 ne scelle aucun fichier @historique (vérifié — 15 entrées = 9 corpus + 6 piliers) → aucun rescellement requis ; re-certification 6/6 après correction.

### §3.2 — Lignée post-b75a620 (reconstruction)

Bornage par recoupement des fragments plateforme avec @historique et les §7 des PMs :

1. **b75a620 (2026-10-12, session web-b4d7dd19 Task 12)** : corpus gen-plan v3.23.1, SHARED v1.7.7, PM-INSTALL v1.7.1, SYNC-CONTEXT v1.4.9, README v2.1.7, KB 33 entrées. La couche @historique est déjà en retard (drift g) — le commit matérialise un état dont la documentation documentaire n'a pas suivi.
2. **Post-b75a620, avant instantané plateforme** : le propriétaire poursuit l'évolution — SHARED v1.7.8 (le skill cahier-des-charges est créé/aligné sous ce marqueur), puis v1.7.9, v1.7.10 (alias-eco porte ce marqueur). La simulation du canal canonique (rapport bug §5) produit **précisément SHARED v1.7.8** lors d'un bump gen-plan v3.23.1→v3.24.0 : la transition propriétaire a très probablement été un bump gen-plan de cette nature.
3. **gen-plan v3.24.0** : existé dans cette lignée (le bug le rapporte « depuis v3.24.0 »), **jamais commité** — aucune trace locale (`rg "3\.24"` : unique mention = ce contexte d'audit). Le dépôt s'arrête à v3.23.1 ; l'instantané plateforme (qui porte cahier-des-charges §0 v1.7.8 et alias-eco §0 v1.7.10) est postérieur à SHARED v1.7.10 mais ne porte aucun matériau v3.24.0 — la v3.24.0 a été créée puis perdue (ou wipe) entre les deux.

**Conclusion de lignée** : le bug « oublie de générer les plans d'actions depuis v3.24.0 » provient d'un état propriétaire intermédiaire (post-b75a620, pré-instantané plateforme) dont la v3.24.0 était un PM « coquille » ou une restructuration non complétée — voir le rapport dédié pour le diagnostic mécanique complet.

## §4 — Phase C : test du bug v3.24.0 (E11) — résumé

Exécuté intégralement en sandbox N0 (blast radius CRITIQUE 17/22, golden master scellé, zéro écriture vivante). **Discrimination : H1/H2/H3 réfutées pour le canal canonique** — le diff intégral PM v3.23.1 → v3.24.0 montre exactement 6 points de substitution de version et rien d'autre ; la machinerie de génération de plans est intégralement préservée (comptes identiques : déclencheur « plan d'actions » 1/1, E1-E15 10/10, answer key 5/5, grille 15/15, hook 26/26) ; les champs de routage sont inchangés (replay 11/12 identique).

**La faille identifiée** : le point aveugle « complétion agent » de KO-L004 — le générateur écrit le PM malgré les gaps de couverture (WARN sans gate, exit 0), le PM généré porte lui-même la mention « deltas sémantiques à complétion agent », `--check` ne vérifie que les versions (COHERENT), et aucun des 6 arbitres ne contrôle la complétude sémantique. Toute montée MINOR sémantiquement substantive produit ainsi un PM coquille vert partout — si les nouveautés touchaient la machinerie des plans, l'agent oublie de générer les plans d'actions : le symptôme rapporté. Corroboration de lignée : la simulation produit SHARED v1.7.8, exactement le marqueur du fragment plateforme cahier-des-charges.

Détail complet (protocole, reproduction rejouable, diff, correctif proposé en 5 points) : **`download/rapport-test-bug-genplan-v3240.md`**.

## §5 — Propositions (application = décision propriétaire explicite — D007)

1. **(a) Recalibrer `verify-correct-work.py` sur le contrat v2.7.0** : PM_PATH → `PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md`, checks réécrits sur la table §6 de v2.7.0 (couplage gen-plan obligatoire Étape 1) — refactoring sous golden master + sweep arbitres.
2. **(b) Implémenter `--mode correct-work` dans `verify-cross.py`** (checks 7-8 : KB + frontmatter métier) ou retirer l'invocation redondante de `certification-complete.py` — l'un ou l'autre, jamais l'état actuel (invoqué/non implémenté).
3. **(d) Trancher la sémantique de lignée du worklog** : soit porter l'historique B1 du propriétaire dans le worklog local à l'installation (extension PM-INSTALL), soit recaler l'arbitre interactions pour traiter un profil frais comme attendu (pas de WARN) — décision d'architecture propriétaire.
4. **(f) Recalibrer la réplique voie M** : aligner le stemmer/routage de `check-triggers-replay.py` sur les trigger_evals d'époque (17 dérives), ou resynchroniser les corpus trigger_evals — et l'intégrer aux 6 arbitres de certification (angle mort : aucun arbitre ne re-joue les triggers aujourd'hui).
5. **(bug) Appliquer le correctif en 5 points du rapport dédié §6** : gate de complétude (exit 4), `--check` renforcé (PM-SHELL), passe `--complete`, arbitre de complétude sémantique (sections SKILL.md ⊆ PM), propagation documentaire §2quater/§1.15.

## §6 — Certification finale & livrables

- **Re-certification post-audit** : 6/6 PASS AVEC RÉSERVES (l'avertissement worklog B1 — drift d JOURNALISÉ — est le seul résidu, identique à l'état d'entrée D002).
- **Zéro-régression** : golden masters byte-identité vérifiés Phase B (documentation @historique) et Phase C (gen-plan vivant) ; l'archive d'intégrité v2.3 reste valide (aucun fichier scellé touché) ; les 24 PMs archivés intacts (R2).
- **Livrables** : ce rapport ; `download/rapport-test-bug-genplan-v3240.md` ; arbitres `scripts/audit-phaseA-historique.py` (ALL PASS) + rapports JSON (`audit-phaseA-report.json`, `triggers-replay-report.json`, `certification-report.json`) ; sceaux `scripts/audit-phaseB-golden-avant.txt` / `scripts/audit-phaseC-golden-avant.txt`.
- **Décisions** : aucune écriture KB (R-F2 — aucune décision d'architecture adoptée ; les propositions §5 attendent la directive propriétaire). Worklog : append Task 5+ (E13). Leçons knowledge-observer : E15.
