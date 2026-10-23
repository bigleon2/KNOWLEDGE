# Plan d'actions — Task 20 : test de performance de l'installation de $ECO-LEON

> **Session** : web-fdf5963c · **Date** : 2026-10-23 · **gen-plan** : v3.23.2 (mode **NULL** — exécution classique, sans portes de confirmation)
> **Provenance** : directive propriétaire — `gen-plan : "test si l'installation de $ECO-LEON est performante"`. **Expansion alias appliquée à la lecture** (registre `skills/@historique/@Alias/aliases.json` — G2 plan Task 19) : `$ECO-LEON` → « mon écosystème personnel ». Objectif expansé : *test si l'installation de mon écosystème personnel est performante*.
> **État d'entrée** : couche Task 18 terminée et certifiée (6/6 arbitres dépôt ALL PASS, 72/72 hôte), profil local installé (36 skills écosystème projetés par l'exécuteur canonique `scripts/eco_install_pipeline.py` @ pin b75a620), 207 fichiers locaux non commités (règle d'or n°2 : 0 commit, 0 push sans GO).
> **Cible du test** : le PROFIL INSTALLÉ (`/home/z/my-project/skills/` — projection hôte) ET le PROCESSUS d'installation (ré-exécution instrumentée de l'exécuteur canonique PM-INSTALL v1.8.0, voie directe).

## §1 — Classification (E1-E3)

Type 4 (méta-outil/écosystème — campagne de tests non destructifs) · complexité moyenne · profil NORMAL · lecture seule partout sauf la ré-installation idempotente (écritures de contenu identique, garde R2 + snapshots de contrôle). Livrables : plan + harnais de tests + rapport à verdict explicite. Aucun nouveau skill créé ; instruments = arbitres existants.

## §2 — Définition opérationnelle : « installation performante » (5 axes)

| Axe | Question | Instrument |
|-----|----------|------------|
| **Complétude** | Les 36 skills écosystème du registre KB sont-ils projetés au profil hôte, aux versions du dépôt ? | Inventaire dérivé du registre KB (KO-L003 — jamais de liste figée) |
| **Intégrité** | L'arbitre d'intégrité re-certifie-t-il la projection hôte (manifeste 72/72) ? | `check-ecosysteme-integrity.py` depuis la projection hôte |
| **Fonctionnalité** | Les organes critiques répondent-ils : gen-plan lisible, arbitre correct-work 16/16, alias-eco selftest + registre + résolution $ECO-LEON ? | Formes installées hôte (SKILL.md, scripts, selftests) |
| **Performance (processus)** | La ré-exécution de l'exécuteur canonique est-elle rapide, sûre (preflight pin, garde R2, purges 0) et mesurée ? | `eco_install_pipeline.py` instrumenté (chrono + rapport JSON) |
| **Idempotence** | Une double exécution produit-elle un arbre hôte strictement identique (contenu par SHA-256, Z6/R6) ? | Snapshots de hachage avant/run1/run2 + diff |

## §3 — Groupes séquentiels (E7)

| Groupe | Tâches | Prérequis | #token |
|--------|--------|-----------|--------|
| **G1 — Planification validée** | présent plan + answer key D001-D012 + harnais `scripts/task20-answer-key-check.py` (16 checks, rc 0) | — | ~6 k |
| **G2 — Tests statiques (état)** | (T1) inventaire complétude 36 skills projetés + égalité de versions host/dépôt ; (T2) intégrité hôte re-certifiée ALL PASS ; (T3) certification dépôt 6 arbitres code retour 0 | G1 | ~10 k |
| **G3 — Tests fonctionnels (organes)** | (T4) gen-plan v3.23.2 frontmatter + déclencheurs §A + E1-E15 ; (T5) arbitre correct-work hôte 16/16 ; (T6) alias-eco selftest 15/15 + `--list` + registre vivant trié dédupliqué contenant `ECO-LEON` → « mon écosystème personnel » | G2 | ~8 k |
| **G4 — Tests de performance (processus)** | (T7) snapshot SHA-256 A → ré-installation instrumentée run 1 (chrono, preflight, garde R2, purges) → snapshot B → diff A→B (0 modifié/supprimé ; nouveaux = seuls fichiers task20-* justifiés, union-merge) ; (T8) run 2 → snapshot C → diff B→C strictement vide ; (T9) mesures consolidées (durées, empreinte disque, temps arbitres) | G3 | ~12 k |
| **G5 — Synthèse et clôture** | rapport `download/rapport-task20-test-installation-performante.md` à verdict explicite selon seuils §5 ; correct-work(cibles) sur les livrables de phase (hooks E9-E14) ; tenue du registre alias via délégation alias-eco §10.1 (correct-work v2.8.0) ; worklog + E15 bilan | G4 | ~9 k |

**Total estimé** : ~45 k #token (profil NORMAL).

## §4 — Answer key (spécifications vérifiables)

```yaml
decisions:
  - id: "D001"
    criterion: "Plan Task 20 créé + harnais scripts/task20-answer-key-check.py 16/16 PASS code retour 0 (validation E8 avant exécution)"
    verification: "python3 scripts/task20-answer-key-check.py → rc 0, 16/16"
    source: "hook E7/E8 gen-plan §1.12 (pattern task14-17)"
    priority: "S1"
    status: "pending"
  - id: "D002"
    criterion: "Complétude : chaque skill écosystème du registre KB (périmètre dérivé dynamique) est projeté au profil hôte avec SKILL.md et version strictement égale à celle du dépôt (36 attendus à l'état Task 18)"
    verification: "harnais T1 : inventaire dérivé du registre KB, comparaison host/dépôt, 0 manquant, 0 divergence"
    source: "PM-INSTALL v1.8.0 §2bis (périmètre COMPLET dynamique KO-L003) + Phase E Task 18"
    priority: "S1"
    status: "pending"
  - id: "D003"
    criterion: "Intégrité : l'arbitre d'intégrité exécuté depuis la projection hôte re-certifie l'état hôte sans aucun échec (manifeste 72/72 Task 18)"
    verification: "python3 /home/z/my-project/scripts/check-ecosysteme-integrity.py --check → ALL PASS"
    source: "Phase E Task 18 (intégrité hôte 72/72, manifeste hôte écrit)"
    priority: "S1"
    status: "pending"
  - id: "D004"
    criterion: "Certification du dépôt source : certification-complete.py code retour 0 (5 arbitres verts, verdict consolidé ALL PASS)"
    verification: "python3 scripts/certification-complete.py → rc 0, rapport scripts/certification-report.json"
    source: "Phase D Task 18 (6/6 ALL PASS) — l'installation directe projette les formes certifiées"
    priority: "S1"
    status: "pending"
  - id: "D005"
    criterion: "gen-plan fonctionnel : SKILL.md hôte v3.23.2 avec frontmatter complet (name, version, category, language, description, dependencies), déclencheurs §A (gen-plan:, plan d'actions, orchestre) et pipeline E1-E15 présents"
    verification: "harnais T4 : lecture/parsage de /home/z/my-project/skills/gen-plan/SKILL.md"
    source: "montée v3.23.2 Task 18 (Phase C1)"
    priority: "S1"
    status: "pending"
  - id: "D006"
    criterion: "correct-work fonctionnel : arbitre verify-correct-work.py (forme installée hôte) 16/16 ALL PASS code retour 0"
    verification: "python3 /home/z/my-project/skills/correct-work/scripts/verify-correct-work.py → rc 0, 16/16"
    source: "recalibrage v2.8.0 Task 18 (Phase D, EXPECTED_VERSION)"
    priority: "S1"
    status: "pending"
  - id: "D007"
    criterion: "alias-eco fonctionnel : selftest 15/15 rc 0 ; --list rc 0 ; registre vivant valide (trié, dédupliqué strict) contenant l'entrée alias ECO-LEON = « mon écosystème personnel » ; la résolution à la lecture est démontrée en direct dans la session (expansion du message propriétaire)"
    verification: "python3 /home/z/my-project/skills/alias-eco/scripts/alias-manager.py --selftest et --list + parsage aliases.json + constat de session"
    source: "skill alias-eco v1.0.0 Task 18 (Phase B) + G2 plan Task 19 (amorçage opérationnel)"
    priority: "S1"
    status: "pending"
  - id: "D008"
    criterion: "Processus d'installation performant : ré-exécution instrumentée de l'exécuteur canonique — preflight pin b75a620 OK (descendant-tolérant), garde R2 « 0 rétrogradation », purges 0, durée run 1 < 60 s"
    verification: "harnais T7 : chrono + rapport JSON eco_install_pipeline.py parsé"
    source: "PM-INSTALL v1.8.0 §3.2(a) — eco_install_pipeline.py exécuteur canonique (Task 18 Phase C3)"
    priority: "S1"
    status: "pending"
  - id: "D009"
    criterion: "Idempotence : run 1 — 0 fichier hôte préexistant modifié ou supprimé, nouveaux fichiers limités à l'ensemble justifié des harnais task20-* (union-merge, aucun effet de bord) ; run 2 — diff strictement vide (0 modifié, 0 nouveau, 0 supprimé)"
    verification: "harnais T7/T8 : snapshots SHA-256 A/B/C de l'arbre projeté géré + diff"
    source: "Z6/R6 (idempotence §1.10-§1.11) + garde R2 + archive round-trip idempotente (Task 18 Phase E)"
    priority: "S2"
    status: "pending"
  - id: "D010"
    criterion: "Mesures de performance consolidées au rapport : durées run 1/run 2, empreinte disque (corpus @mon-ecosysteme, 36 skills écosystème, scripts hôte, archive), temps des arbitres"
    verification: "harnais T9 : relevés écrits dans scripts/task20-tests-report.json et repris au rapport"
    source: "§4 profils ressource + étiquette #token gen-plan"
    priority: "S2"
    status: "pending"
  - id: "D011"
    criterion: "Rapport final à verdict explicite selon les seuils §5 (PERFORMANT / PARTIELLEMENT PERFORMANT / NON PERFORMANT), livré à download/, avec preuves et écarts éventuels"
    verification: "lecture du rapport : verdict présent, seuils appliqués, traçabilité answer key D001-D012"
    source: "critère de succès E1 (la question propriétaire reçoit une réponse tranchée)"
    priority: "S1"
    status: "pending"
  - id: "D012"
    criterion: "Clôture écosystème : registre alias tenu via délégation alias-eco §10.1 (scan de la discussion courante), worklog complété (dépôt + session), E15 bilan avec leçons et régénération du plan suivant via gen-plan"
    verification: "registre aliases.json mis à jour (trié, dédupliqué) + entrée worklog Task 20 + bilan E15 en réponse session"
    source: "correct-work v2.8.0 §10.1 (délégation registre) + E15 gen-plan + directive Task 18 (le mécanisme gen-plan est permanent)"
    priority: "S2"
    status: "pending"
```

## §5 — Seuils de verdict

- **PERFORMANT** ⟺ D002-D008 tous verified ET durée run 1 < 60 s ET idempotence parfaite (D009 : run 2 diff vide, run 1 sans effet de bord hors ensemble justifié).
- **PARTIELLEMENT PERFORMANT** ⟺ D002-D007 verified (état installé complet, intègre, fonctionnel) MAIS durée run 1 ≥ 60 s OU écart d'idempotence résiduel justifié et documenté.
- **NON PERFORMANT** ⟺ au moins un échec S1 parmi D002-D008 (l'installation ne fait pas ce qu'elle doit, ou de façon non sûre).

## §6 — Exécution et gardes

- Hooks correct-work par phase (E9-E14) : après chaque groupe G2/G3/G4, vérification CIBLE des livrables du groupe (arbitres + re-lecture) ; FAIL → pause et correction (max 2 rounds) ; PASS AVEC RÉSERVES → réserves journalisées, exécution continue.
- Règle d'or n°2 : **0 commit, 0 push** — tous les artefacts Task 20 restent locaux (dépôt travail + hôte).
- Non-destructivité : la ré-installation n'écrit que du contenu identique (union-merge + garde R2 + purge bornée NON_CANONIQUES) ; snapshots SHA-256 avant/après prouvent l'absence d'effet de bord ; `__pycache__` exclu du périmètre de diff (artefacts de compilation, jamais sources).
- Instrumentation consolidée : un harnais unique `scripts/task20-tests-installation.py` exécute T1-T9 (tests statiques, fonctionnels et de performance), écrit le relevé machine `scripts/task20-tests-report.json` et applique les seuils de verdict §5.
- E15 : bilan + auto-calibration + régénération du plan suivant via gen-plan (le mécanisme est permanent, leçon Task 18).
