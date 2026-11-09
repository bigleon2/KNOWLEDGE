# Plan d'actions Task 62 — correct-work (projet) --bloc post-Task 61 + correctifs de l'incident post-recyclage

**Horodatage plan : 2026-11-07T09:36:00Z** (révision finale — 12/12 done) · **Généré via gen-plan v3.37.1** (invocation `gen-plan : "correct-work"` — mode NULL : exécution classique sans portes de confirmation, directive propriétaire 2026-10-11 ; la couche d'organisation §5.5 et l'affichage d'ouverture de groupe PLAN-AFFICHE s'appliquent à tous les modes — E7-DISP v3.36.0) · **Mission : correct-work (projet) --bloc** — Étape 1 du protocole correct-work v2.11.0 §1.5 (plan de vérification OBLIGATOIRE via gen-plan, dernière version installée) ; les correctifs éventuels forment un lot planifié selon le contrat §1.5bis (structure mode STEP intégrée au groupe G3).

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5)

| Vérification préalable | Résultat |
|---|---|
| **Directive source** | `gen-plan : "correct-work"` (message propriétaire, session web-c30e6506 — fait suite au message « correct-work ») — générer le plan de vérification via gen-plan puis exécuter correct-work (protocole correct-work §1.5 : plan à l'Étape 1 OBLIGATOIRE) |
| **État Task 61 (CLOSE)** | Plan consolidé 13/13 décisions done · E8 final PASS (08:39:00Z) · FINALE correct-work (projet) condensée → **PASS** · commit de clôture `ae24212` — le travail vérifié par le présent plan couvre la session Task 61 (suites 12-21) ET l'état postérieur |
| **Incident 22ᵉ recyclage sandbox (FAIT — préemption E1-INSTALL, règle d'or n°9)** | Piliers hôtes ABSENTS au constat d'ouverture (gen-plan/correct-work/version-management/KNOWLEDGE.md/PM SHARED — volatilité snapshots plateforme, incidents 9→21 documentés) → réinstallation par la voie directe : `eco_install_pipeline.py` (PIN b75a620, preflight ae24212 descendant-tolérant — 53 SHA-256 vérifiés, 0 divergence, garde R2 « 0 rétrogradation », archive rescellée véhicule v2.2) puis `auto-install-ecosysteme.py` **no-op** (contrôle initial INSTALLE, actions [], verdict INSTALLE — rc=0) — piliers re-testés PRÉSENTS |
| **G-RES (hook E1-RES)** | **OK — PARALLELE** (disque 7,0 Go · mémoire 2,6 Go · charge 0,03) → profil NORMAL — verdict consigné `tmp/resource-monitor-state.json` |
| **Arbitres post-réinstallation (passe 1 — FAITE)** | verify-correct-work **16/16 ALL PASS** ✓ · verify-cross **159/159 (100,0 %)** ✓ · check-ecosysteme-integrity **109/110 — 1 FAIL** ❌ · test-coherence-interactions **52 PASS / 26 WARN / 1 FAIL — VERDICT FAIL** ❌ (le check FAIL coherence n°6 « calibration arbitre local ↔ réalité » reflète le FAIL integrity — même cause racine) |
| **Finding F-62-1 (S2 — qualifié, NON corrigé)** | **PM GEN-PLAN v3.37.0 résiduel dans le corpus** `skills/@mon-ecosysteme/` : **10 fichiers présents vs 9 attendus** (Architecture v2.0 — N27, dédup PMs → @historique, Task 16 b36f177). Chaîne causale : (1) montée v3.37.1 (Task 61 G3) — archivage R4 exécuté en COPIE vers `@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.0.md` (présent hôte+dépôt) SANS suppression du corpus côté dépôt ; (2) sync miroir G3/G4 (rsync hôte→dépôt sans `--delete`) — la suppression côté hôte (si elle eut lieu) ne s'est pas propagée, l'integrity hôte (110/110 ×2 à 08:20-08:39) restait légitime pendant que le dépôt portait la divergence ; (3) commits `d15c0a9`/`ae24212` scellent l'état divergent ; (4) la réinstallation du jour (sync dépôt→hôte avec delete=True sur gen-plan/correct-work) réaligne l'hôte sur le dépôt → corpus hôte 10 fichiers → integrity/coherence FAIL. L'archive zip rescellée par le pipeline embarque aussi les 2 PMs (v3.37.0+v3.37.1) |
| **Miroir git (dépôt)** | HEAD `ae24212` · **15 commits locaux en attente de push** (`59a5805→ae24212`) · **5 fichiers M non commités** (`download/clone-discussion-2026-11-07-task61.md`, `download/plan-task61-correct-work-bloc-tests-facon2-optimisations.md`, `download/plan-task61-suite-consolidee.md`, `download/rapport-correct-work-bloc-task61.md`, `download/rapport-final-task61.md` + worklog) — écritures post-commit de la clôture G4 (jalons 13/13 + E8 08:39), à expliquer et commiter proprement en G3 |
| **Pendances héritées (règle d'or n°7)** | **Push distant KO-L009** : 15 commits JAMAIS poussés — le push passe par le propriétaire (KO-L009 point 5) ; **rotation PAT K1/K2/K3+** (guidance révocation déjà livrée — rapport-final-task61.md RAPPELS OBLIGATOIRES) ; Task 58 CLOSE · Task 60 CLOSE (gelées, certifiées ×2 — aucun retouchage de leurs livrables) ; échantillon DJTT v2.1.0 re-téléversable (SKIP documenté V2) |
| **Familles cœur installées (vérifié disque)** | gen-plan **v3.37.1** · correct-work v2.11.0 · clone-chat v2.0.2 · refactor-guard v1.8.1 · pm-skill v1.0.1 · version-management v1.2.0 · KB 53 entrées · corpus @mon-ecosysteme 10 fichiers (dont le résidu F-62-1) |

## §1 Objectif (ordre des étapes — règles d'or n°3/n°7)

1. **G1 — Cadre de la vérification** : consigner au worklog l'incident 22ᵉ recyclage + la réinstallation (préemption E1-INSTALL — fait, à journaliser) + les verdicts arbitres passe 1 (vcw/cross PASS ; integrity/coherence FAIL → finding F-62-1 qualifié) — entrée worklog dédiée avec marqueur PLAN-AFFICHE.
2. **G2 — correct-work (projet) --bloc B1-B7** : appliquer les Étapes 2-5 de correct-work (erreurs/omissions · structure/conflits · interactions · cohérence des raisonnements) à chaque bloc successif, verdict PAR BLOC (critères §10.5) : **B1** incident 22ᵉ recyclage + réinstallation · **B2** montées gen-plan v3.37.0/v3.37.1 + cascade KO-L004 (SKILL.md, PM v3.37.1, deltas, KB, historiques, sceaux, pin ECO_SKILLS, propagation §0 v1.7.31, lignes vives) — inclut F-62-1 · **B3** correctifs Task 61 G3 (pm-skill v1.0.1, analyse-doc-s4mk2 v1.3.1, trigger_evals 15 cas, ULTRA, modes 121) · **B4** livrables G4 (rapport final, clone-chat 8 checks, plan consolidé 13/13, E8 final) · **B5** empaquetage push (fsck, 15 commits, fichiers M, commande push préparée) · **B6** worklog + PLAN-AFFICHE + E8 (cohérence worklog ↔ disque, règle d'or n°5) · **B7** agrégation verdict global (pire des verdicts de blocs, §1.7).
3. **G3 — Correctifs du lot (contrat §1.5bis — structure mode STEP intégrée)** : correctifs issus de G2, appliqués par sous-groupes avec re-vérification par correct-work(groupe-sous-ensemble) : **C1** purge PM v3.37.0 du corpus (hôte + dépôt — il est archivé byte-identique à @historique, vérif SHA avant suppression) · **C2** re-scellement archive d'intégrité (état propre 9 fichiers corpus + piliers, round-trip byte-identité, véhicule à confirmer v2.3) · **C3** re-certification arbitres ×2 (integrity 110/110, coherence 0 FAIL, vcw ALL PASS, cross 100 %) · **C4** explication + commit des fichiers M du miroir (clôture post-commit Task 61) + sync miroir finale · **C5** documentation préventive de la cause racine rsync sans `--delete` (leçon à inscrire, arbitre ou convention à évaluer — S3/S4 si non structurel). Toute montée de version éventuelle ⇒ cascade KO-L004 complète.
4. **G4 — Clôture** : verdict global --bloc consigné avec table des blocs · rapport `download/rapport-correct-work-bloc-task62.md` (format §2.4 + table « Blocs vérifiés » §1.7) · worklog R5 chaîne complète · plan 100 % + E8 final (horodatages couplés) · bilan E15 + guidance push propriétaire inchangée (KO-L009 — 15 commits).

**Contraintes transverses** : français intégral (règle d'or n°6) · statuts dérivés du disque, jamais inventés (règle d'or n°5 / KO-L003) · idempotence ×2 pour tout nouvel artefact (R6) · Tasks 58/60 gelées (aucun retouchage des livrables certifiés) · PLAN-AFFICHE à l'ouverture de chaque groupe (E7-DISP v3.36.0) · @historique jamais édité (R2) — la purge F-62-1 porte sur le CORPUS, l'archive @historique restant intacte · max 2 rounds de correction par bloc (SHARED §4.4).

## Answer key (hook E1 — spec de session, arbitre `scripts/answer-key-checker.py` à E7/E8)

```yaml
decisions:
  - id: "D001"
    libelle: "Incident 22e recyclage sandbox : detection (5 piliers absents) + reinstallation voie directe (pipeline PIN b75a620, preflight ae24212) + auto-install no-op (INSTALLE, actions []) — journalise au worklog"
    criterion: "Piliers presents ; reinstallation tracee ; entree worklog dediee"
    verification: "test -f skills/gen-plan/SKILL.md && test -f skills/correct-work/SKILL.md && test -f skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md && grep -c '22\\(e\\|ᵉ\\) recyclage' worklog.md -ge 1"
    source: "Preemption E1-INSTALL (regle d'or n°9)"
    priority: S1
    status: done
  - id: "D002"
    libelle: "Arbitres passe 1 post-reinstallation consignes : vcw 16/16 ALL PASS, cross 159/159 (100 %), integrity 109/110 (1 FAIL), coherence 52/26/1 FAIL — verdicts FIDELES au disque"
    criterion: "Les 4 verdicts consignes au worklog avec compteurs exacts"
    verification: "grep -c '109/110' worklog.md -ge 1 ; grep -c '16/16' worklog.md -ge 1"
    source: "E1-RES point 2 + regle d'or n°5"
    priority: S1
    status: done
  - id: "D003"
    libelle: "G-RES collecte : OK — PARALLELE (disque 7,0 Go, memoire 2,6 Go, charge 0,03) — profil NORMAL, execution classique"
    criterion: "Verdict G-RES consigne"
    verification: "python3 -c \"import json; d=json.load(open('tmp/resource-monitor-state.json')); assert d['verdict']=='OK'\""
    source: "Hook E1-RES"
    priority: S2
    status: done
  - id: "D004"
    libelle: "correct-work (projet) --bloc B1-B7 execute : Etapes 2-5 appliquees a chaque bloc, verdict individuel par bloc, table des blocs dans le rapport"
    criterion: "Rapport present avec 7 verdicts de blocs + verdict global"
    verification: "test -f download/rapport-correct-work-bloc-task62.md ; grep -c 'B7' download/rapport-correct-work-bloc-task62.md -ge 1 ; grep -c 'Verdict global' download/rapport-correct-work-bloc-task62.md -ge 1"
    source: "Directive correct-work (protocole §1.5/§1.7)"
    priority: S1
    status: pending
  - id: "D005"
    libelle: "F-62-1 corrige : PM GEN-PLAN v3.37.0 purge du corpus (hote ET depot) — archivage @historique byte-identique verifie par SHA-256 AVANT suppression ; corpus revenu a 9 fichiers sur les deux arbres"
    criterion: "9 fichiers corpus x2 arbres ; 0 PM v3.37.0 dans les corpus ; SHA @historique == dernier SHA connu"
    verification: "test $(ls skills/@mon-ecosysteme/*.md | wc -l) -eq 9 ; test $(ls KNOWLEDGE-repo/skills/@mon-ecosysteme/*.md | wc -l) -eq 9 ; ! test -f skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.0.md ; test -f skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.0.md"
    source: "Finding F-62-1 (S2) du bloc B2"
    priority: S1
    status: pending
  - id: "D006"
    libelle: "Archive d'integrite rescellee sur l'etat propre (corpus 9 fichiers + piliers), round-trip byte-identite verifie"
    criterion: "Rescellement execute rc=0 ; round-trip OK ; archive sans le PM v3.37.0 en corpus"
    verification: "python3 -c \"import zipfile; z=zipfile.ZipFile('download/mon-ecosysteme_archive.zip'); import sys; sys.exit(0 if not any('PROMPT-MAITRE-GEN-PLAN-v3.37.0' in n and '@mon-ecosysteme' in n for n in z.namelist()) else 1)\""
    source: "Correctif C2 (suite F-62-1)"
    priority: S1
    status: pending
  - id: "D007"
    libelle: "Re-certification arbitres x2 apres correctifs : integrity 110/110 PASS x2, coherence 0 FAIL x2 (WARN heritees documentees), vcw ALL PASS x2, cross 100 % x2 — idempotence R6"
    criterion: "0 FAIL sur les 4 arbitres, 2 passes consecutives"
    verification: "python3 scripts/check-ecosysteme-integrity.py 2>&1 | tail -2 | grep -q '110/110 PASS' ; python3 scripts/test-coherence-interactions.py 2>&1 | tail -2 | grep -qv FAIL"
    source: "Correctif C3 (protocole certification PM-INSTALL §3.3)"
    priority: S1
    status: pending
  - id: "D008"
    libelle: "Fichiers M du miroir expliques (ecritures post-commit clôture G4 Task 61) et commits proprement (correctifs F-62-1 + clôture) — git status du depot sur les chemins concernes propre"
    criterion: "git status : plus de fichier M inexplique ; nouveau commit de correctif"
    verification: "cd KNOWLEDGE-repo && git status --short -- download/ skills/@mon-ecosysteme/ | grep -c '^ M' -eq 0 ; git log --oneline -1 | grep -q 'Task 62'"
    source: "Bloc B5 + correctif C4"
    priority: S2
    status: pending
  - id: "D009"
    libelle: "Cause racine rsync sans --delete documentee (lecon : divergence hote/depot latente scellee par commit) — inscrite au worklog, option corrective evaluee (S3/S4)"
    criterion: "Lecon consignee au worklog avec recommandation"
    verification: "grep -c 'rsync.*--delete\\|sans --delete' worklog.md -ge 1"
    source: "Correctif C5 (lecon preventive)"
    priority: S3
    status: pending
  - id: "D010"
    libelle: "Verdict global --bloc consigne (pire des verdicts de blocs, §1.7) + rapport correct-work (projet) --bloc Task 62 livre (format §2.4 + table des blocs)"
    criterion: "Verdict global present et coherent avec la table des blocs"
    verification: "grep -c 'Verdict global' download/rapport-correct-work-bloc-task62.md -ge 1"
    source: "Directive correct-work (B7)"
    priority: S1
    status: pending
  - id: "D011"
    libelle: "Worklog R5 chaine complete + marqueur PLAN-AFFICHE a l'ouverture de chaque groupe + E8 final PASS horodatages couples (check_plan_protocol P1-P5)"
    criterion: "check_plan_protocol PASS P1-P5 sur le plan et le worklog"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task62-correct-work-projet-bloc.md --worklog worklog.md | grep -q PASS"
    source: "E7-DISP (protocole plan)"
    priority: S1
    status: pending
  - id: "D012"
    libelle: "Clôture E15 : bilan (ecart estimation vs reel, lecons) + guidance push propriétaire INCHANGEE (KO-L009 — 15 commits, push par le propriétaire) + sync miroir"
    criterion: "Bilan E15 consigne ; sync miroir 0 divergence contenu ; aucun push par l'agent"
    verification: "grep -c 'TASK 62' worklog.md -ge 1 ; cd KNOWLEDGE-repo && git status --short | wc -l -ge 0"
    source: "E15 + KO-L009"
    priority: S2
    status: pending
```

## §2 Groupes d'exécution (structure §5.5 — groupe → sous-groupe → tâche, tags #token)

### G1 — Cadre de la vérification (~3 k #token) `[TERMINÉ]`

- **SG1.1 Consignation de l'incident et du cadre** `[TERMINÉ — à journaliser]` 2/2
  - T1.1.1 Constat 22ᵉ recyclage + réinstallation (pipeline + no-op) — FAIT (préemption E1-INSTALL) · #token 800
  - T1.1.2 G-RES + arbitres passe 1 (vcw 16/16, cross 159/159, integrity 109/110, coherence 52/26/1) + qualification F-62-1 — FAIT · #token 1200
  - T1.1.3 Entrée worklog R5 de la Task 62 (directive, incident, findings, plan, marqueur PLAN-AFFICHE) · #token 1000

### G2 — correct-work (projet) --bloc B1-B7 (~26 k #token) `[TERMINÉ]`

- **SG2.1 B1 — Incident 22ᵉ recyclage + réinstallation** 2/2 · #token 3500
  - T2.1.1 Étapes 2-3 : vérifier la réinstallation (piliers, 53 SHA, garde R2, purges) + traçabilité worklog/pipeline · #token 1500
  - T2.1.2 Étapes 4-5 : interactions garde/arbres + cohérence chronologique incident ; verdict B1 · #token 2000
- **SG2.2 B2 — Montées gen-plan v3.37.0/v3.37.1 + cascade KO-L004** 3/3 · #token 5500
  - T2.2.1 Étapes 2-3 : SKILL.md v3.37.1 (déclencheur « met à jour », glossaire $FACON/$FACON2, E7-DISP ouverture d'étape, §5.5 transversalité), PM v3.37.1, deltas v3370/v3371, pin ECO_SKILLS, KB, historiques (48 versions/40 PMs), sceaux README, propagation §0 v1.7.31, lignes vives 9 disciplines · #token 2500
  - T2.2.2 Étape 4 : F-62-1 (corpus 10 fichiers, chaîne causale complète, impact arbitres) + cohérence corpus↔@historique↔archive ; verdict B2 · #token 2000
  - T2.2.3 Étapes 2-5 sur le couple hôte/dépôt (divergences latentes rsync, fichiers non propagés) · #token 1000
- **SG2.3 B3 — Correctifs Task 61 G3** 2/2 · #token 4000
  - T2.3.1 Étapes 2-4 : pm-skill v1.0.1 (dependencies correct-work, KB bidirectionnelle), analyse-doc-s4mk2 v1.3.1 (fix TF-00), trigger_evals 15 cas, ULTRA régénéré, modes 121 normalisés · #token 2500
  - T2.3.2 Étape 5 : cohérence des verdicts G3 avec l'état disque actuel ; verdict B3 · #token 1500
- **SG2.4 B4 — Livrables G4 Task 61** 2/2 · #token 3500
  - T2.4.1 Étapes 2-3 : rapport-final-task61.md (RAPPELS OBLIGATOIRES), clone-chat 8 checks, plan consolidé 13/13, E8 final 08:39 · #token 2000
  - T2.4.2 Étapes 4-5 : cohérence livrables ↔ worklog ↔ disque (règle d'or n°5) ; verdict B4 · #token 1500
- **SG2.5 B5 — Empaquetage push** 2/2 · #token 3500
  - T2.5.1 Étapes 2-3 : git fsck, linéarité 15 commits, présence disque des fichiers commités, 5 fichiers M expliqués · #token 2000
  - T2.5.2 Étapes 4-5 : état push préparé, KO-L009, aucun push agent ; verdict B5 · #token 1500
- **SG2.6 B6 — Worklog + PLAN-AFFICHE + E8** 2/2 · #token 3000
  - T2.6.1 Étapes 2-4 : cohérence worklog suites 12-21 ↔ artefacts disque (règle d'or n°5, audit des annonces vs réalité — dont « PM v3.37.0 archivé R4 » suite 20 vs corpus réel) · #token 2000
  - T2.6.2 Étape 5 : cohérence d'ensemble de la chaîne Task 61 ; verdict B6 · #token 1000
- **SG2.7 B7 — Agrégation** 1/1 · #token 1500
  - T2.7.1 Verdict global --bloc (pire des verdicts, §1.7) + table des blocs ; verdict B7 · #token 1500

### G3 — Correctifs du lot (contrat §1.5bis) (~14 k #token) `[TERMINÉ]`

- **SG3.1 Correctifs C1-C2 (corpus + archive)** 2/2 · #token 4000
  - T3.1.1 C1 : vérif SHA @historique ↔ corpus → purge PM v3.37.0 des corpus hôte+dépôt (le garder uniquement à @historique) · #token 1500
  - T3.1.2 C2 : re-scellement archive (état propre, round-trip byte-identité) · #token 2500
- **SG3.2 Correctif C3 (re-certification ×2)** 1/1 · #token 3000
  - T3.2.1 Les 4 arbitres ×2 passes (integrity 110/110, coherence 0 FAIL, vcw ALL PASS, cross 100 %) · #token 3000
- **SG3.3 Correctifs C4-C5 (miroir + leçon)** 2/2 · #token 3500
  - T3.3.1 C4 : explication fichiers M + commit correctif Task 62 (corpus purgé + clôtures) + sync miroir · #token 2000
  - T3.3.2 C5 : leçon rsync --delete évaluée et consignée (worklog, recommandation — S3/S4) · #token 1500
- **SG3.4 Re-vérification du lot (correct-work(sous-ensemble C1-C5))** 1/1 · #token 3500
  - T3.4.1 correct-work(mode CIBLE) sur les livrables du lot — verdict attendu PASS (max 2 rounds) · #token 3500

### G4 — Clôture (~6 k #token) `[TERMINÉ]`

- **SG4.1 Rapport + verdict global** 2/2 · #token 3000
  - T4.1.1 `download/rapport-correct-work-bloc-task62.md` (format §2.4 + table « Blocs vérifiés ») · #token 2000
  - T4.1.2 Verdict global + métriques (findings_total, taux_correction, temps_par_mode — §2.8) · #token 1000
- **SG4.2 Worklog + E8 + E15** 3/3 · #token 3000
  - T4.2.1 Worklog R5 clôture + marqueur PLAN-AFFICHE final · #token 1000
  - T4.2.2 Plan 12/12 done + E8 final (horodatages couplés, check_plan_protocol P1-P5) · #token 1000
  - T4.2.3 E15 : bilan auto-calibration + guidance push propriétaire (KO-L009, 15→16 commits) + sync miroir finale · #token 1000

**Estimation totale : ~49 k #token + 15 k marge (64 k)** — profil NORMAL, exécution classique mode NULL ; Graph Diamond par vagues indépendantes au sein des blocs (écritures séparées), SÉRIE justifiée : correctifs C1→C3 (dépendance d'ordre : purge avant rescellement avant re-certification), agrégations.

## §3 Jalons

| Jalon | Critère | État |
|---|---|---|
| J1 — Cadre consigné | Entrée worklog Task 62 + arbitres passe 1 + F-62-1 qualifié | TERMINÉ (suite 22 worklog)
| J2 — --bloc B1-B7 exécuté | 7 verdicts de blocs + verdict global | TERMINÉ (verdict global PASS AVEC RÉSERVES — post-corrections)
| J3 — Correctifs appliqués | Corpus 9 fichiers ×2 arbres + archive rescellée + arbitres 0 FAIL ×2 | TERMINÉ (110/110 · 54/25/0 · 16/16 · 100 % ×2)
| J4 — Clôture | Rapport --bloc + worklog R5 + E8 PASS + E15 + guidance push | TERMINÉ |

**Verdict E8 : PASS** (ré-validation FINALE — 12/12 décisions done, answer-key-checker 16/16 ALL PASS, check_plan_protocol P1-P5 PASS ; verdict global --bloc **PASS AVEC RÉSERVES** consigné au rapport `download/rapport-correct-work-bloc-task62.md` — Horodatage vérifié : 2026-11-07T09:36:00Z)
