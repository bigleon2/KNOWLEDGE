# Plan d'actions — Task 71 — gen-plan(step) : langue + push + R1/R2 + tests chronologiques + correct-work --bloc + clone-chat

- **Skill** : gen-plan v3.37.1 — **mode step** (enchaînement autonome des groupes, correct-work(groupe) après chaque groupe — max 2 rounds, correct-work(projet) en fin de chaîne)
- **Demande propriétaire** (verbatim, 2026-11-08, session web-ecef7f80) : 6 items — (1) durcissement règle français ; (2) PUSH avec clé collée au chat ; (3) appliquer R1+R2 avec analyse d'intégration $FACON et tests $FACON2 avant intégration ; (4) tests $FACON2 fonctionnels + performances des éléments créés/modifiés dans cette discussion (hier + aujourd'hui), ordonnés par chronologie de création/modification, incluant tout ce qui sera POUSSÉ et ses dépendances ; (5) correct-work (projet) --bloc ; (6) clone-chat.
- Horodatage plan : 2026-11-07T18:58:31Z
- **Classification** : mixte Type 1 (opération git) + Type 2 (analyse/intégration + harnais de tests) — profil NORMAL — #token total estimé : ~85 k
- **Contexte incidents vivants** : (a) règle d'or n°6 violée en début de session (textes d'analyse en anglais/chinois) — constat propriétaire FONDÉ ; (b) **KO-L009 déclenché** : un PAT GitHub a été collé au chat par le propriétaire (valeur JAMAIS recopiée, stockée ni utilisée — réaction systématique, guidance révocation en G2) ; (c) volatilité version-management : **3 disparitions dans la session courante** (35ᵉ–37ᵉ incidents), réparées ×3 par la garde externe `ensure-installed.py` (verdict `INSTALLE-REPARÉ`), arbitre re-certifié 110/110 ×3.

## Answer key

- **D001** — criterion: règle d'or n°6 durcie dans gen-plan (portée étendue aux textes de raisonnement affichés, résumés de continuation, sorties reformulées + reprise immédiate sans transition, version bumpée v3.37.2) · verification: `rg -c "vii" skills/gen-plan/SKILL.md` ≥ 1 dans la règle n°6 ET `rg "^version: 3.37.2" skills/gen-plan/SKILL.md` · S1 · pending
- **D002** — criterion: durcissement propagé au §0 SHARED v1.7.32 (porté par le corpus, s'applique à tous les skills) · verification: `rg "v1.7.32" skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md` · S2 · pending
- **D003** — criterion: incident KO-L009 consigné SANS la valeur du secret + guidance révocation remise · verification: `rg -c "KO-L009" worklog.md` ≥ 1 entrée du jour et 0 occurrence du pattern `github_pat_` dans tout fichier écrit · S1 · pending
- **D004** — criterion: PUSH NON exécuté avec le jeton exposé (KO-L009 (1)+(5)) ; pendance consignée avec commandes exactes pour le propriétaire · verification: `git -C KNOWLEDGE-repo log origin/main..main --oneline` — l'agent n'a rien poussé + entrée worklog pendance push · S1 · pending
- **D005** — criterion: R1 — arbitre de poids de chargement `scripts/poids-chargement.py` (Kio + #token estimé + verdict OK/LOURD/CRITIQUE + self-test + idempotence ×2) · verification: `python3 scripts/poids-chargement.py --selftest` → PASS puis exécution ×2 → sorties identiques · S1 · pending
- **D006** — criterion: R1 — hook E5-POIDS intégré à gen-plan v3.38.0 (skill CRITIQUE → lecture ciblée §0 + references/ à la demande) · verification: `rg -c "E5-POIDS" skills/gen-plan/SKILL.md` ≥ 1 · S1 · pending
- **D007** — criterion: R2 — cache de verdicts généralisé `scripts/cache-verdicts.py` (clé SHA-256 commande+cibles, verdict figé, rejeu sans ré-appel, invalidation par stat, --force/--clear/--selftest) · verification: `python3 scripts/cache-verdicts.py --selftest` → PASS + démo cold/warm verdict identique et warm ≥ 10× plus rapide · S1 · pending
- **D008** — criterion: R2 — pattern appliqué à ≥ 1 arbitre réel avec preuve horodatée + hook documenté dans gen-plan · verification: `rg -c "cache-verdicts" skills/gen-plan/SKILL.md` ≥ 1 + fichier preuve démo · S2 · pending
- **D009** — criterion: harnais `scripts/task71-tests-chronologiques.py` couvrant les éléments de la discussion dans l'ordre chronologique de création/modification (1. propagate-context v2.1.0 → 2. @Bibliotheque-skills-Multi-IA → 3. @GHORG-ecosysteme + ghorg-cmdr v1.1.0 → 4. étude faisabilité + livrables Task 70 → 5. éléments du jour) · verification: `python3 scripts/task71-tests-chronologiques.py` → verdict global + `download/rapport-tests-chronologiques-task71.md` · S1 · pending
- **D010** — criterion: cascade KO-L004 complète après montées de version (KB + pin ECO_SKILLS + manifeste re-scellé + arbitres 0 FAIL) · verification: `python3 scripts/check-ecosysteme-integrity.py` → 110/110 PASS 0 FAIL · S1 · pending
- **D011** — criterion: correct-work (projet) --bloc — rapport bloc par bloc (6 blocs G1→G6), verdict par bloc, agrégation pire-des-verdicts · verification: fichier `download/rapport-correct-work-task71.md` avec table « Blocs vérifiés » + verdict global · S1 · pending
- **D012** — criterion: clone-chat — archive auto-suffisante de la discussion · verification: fichier `download/clone-chat-session-web-ecef7f80-20261108.md` non vide contenant contexte + décisions + artefacts + worklog · S2 · pending
- **D013** — criterion: zéro exposition du secret — aucun fichier écrit ne contient la valeur du PAT · verification: `rg -l "github_pat_"` sur download/ scripts/ skills/ worklog.md → 0 résultat · S1 · pending

## Groupes d'exécution (mode step — enchaînement séquentiel, correct-work(groupe) après chaque groupe)

### G1 — Durcissement règle d'or n°6 (français) (#token ~8 k)
Sous-groupes :
- G1.1 — gen-plan SKILL.md règle d'or n°6 : ajout durcissement (v3.37.1 → **v3.37.2**, PATCH) — portée étendue : tout texte produit dans une session (raisonnement affiché, titres, libellés de statut, légendes, résumés de continuation, sorties d'outils reformulées) est en français ; dérive constatée → reprise immédiate sans transition ; le constat propriétaire de dérive déclenche journalisation worklog.
- G1.2 — SHARED §0 : même durcissement propagé (v1.7.31 → **v1.7.32**) — porté par le corpus → s'applique aux 116 skills.
- G1.3 — Journalisation : entrée worklog constatant la dérive du jour (textes anglais/chinois) + correction immédiate.
- correct-work(groupe G1) → D001, D002.

### G2 — PUSH : incident KO-L009 + pendance (#token ~5 k)
Sous-groupes :
- G2.1 — **Réaction systématique KO-L009** (jamais dépendante du jugement du moment) : (1) le jeton collé au chat n'est NI recopié, NI stocké, NI utilisé, même « pour vérifier » ; (2) guidance immédiate de révocation : GitHub → Settings → Developer settings → Personal access tokens → **révoquer le jeton** (il est exposé au canal de discussion) ; (3) re-provisionnement one-shot par le propriétaire HORS canal si l'agent doit pousser ; (4) incident consigné au worklog SANS la valeur ; (5) push par le propriétaire — jamais par l'agent avec un secret de chat.
- G2.2 — État des commits : après G1+G3+G4, la branche `main` du miroir certifié contiendra les commits Task 71 à pousser EN PLUS des 2 commits Task 70 (`cea7d12`, `886604d`) — pendance documentée avec la commande exacte : `cd KNOWLEDGE-repo && git push origin main` (après révocation du jeton exposé, depuis un environnement authentifié du propriétaire).
- correct-work(groupe G2) → D003, D004, D013.

### G3 — R1 + R2 : intégration optimisations performance (#token ~30 k)
Sous-groupes :
- G3.1 — **R1 (progressive disclosure)** : création `scripts/poids-chargement.py` — mesure par skill : taille SKILL.md (Kio), #token estimé (caractères/4), total references/, verdict OK (< 12 Kio) / LOURD (≥ 30 Kio) / CRITIQUE (≥ 60 Kio) ; sortie JSON + table Markdown triée ; `--selftest` (fixture temporaire, 8+ checks mécaniques) ; idempotence ×2.
- G3.2 — **R1** : exécution sur l'écosystème complet → rapport des top lourds = file de priorisation R1 (curation progressive disclosure) ; identification du pire SKILL.md et démonstration lecture ciblée (§0 + references à la demande).
- G3.3 — **R2 (cache de verdicts)** : création `scripts/cache-verdicts.py` — couche générique : clé = SHA-256(commande + arguments + stat des fichiers cibles [taille+mtime]) ; verdict JSON figé + horodatage ; rejeu sans ré-appel si clé intacte ; invalidation automatique si stat change ; `--force`, `--clear`, `--selftest` (10+ checks : stockage, rejeu identique, invalidation sur touch, purge) ; idempotence ×2.
- G3.4 — **R2** : démo réelle sur `check-ecosysteme-integrity.py` (grader coûteux, ~1 s+) : mesure cold vs warm (gain attendu ≥ 10×), verdict identique, invalidation sur modification de fichier — preuves horodatées.
- G3.5 — **Intégration gén-plan** (v3.37.2 → **v3.38.0**, MINOR) : deux nouveaux hooks au §1.2bis — **E5-POIDS** (R1) et **R2-CACHE** (R2) ; montée de version + cascade légère (KB + pin ECO_SKILLS + manifeste re-scellé + coherence).
- correct-work(groupe G3) → D005, D006, D007, D008.

### G4 — Tests chronologiques $FACON2 éléments de la discussion (#token ~20 k)
Sous-groupes (ORDRE CHRONOLOGIQUE de création/modification — hier Task 70 puis aujourd'hui Task 71) :
- G4.1 — **Élément n°1 (hier, F-70-2)** : `propagate-context.py` v2.1.0 — py_compile + exécution idempotence ×2 + périmètre étendu scripts embarqués.
- G4.2 — **Élément n°2 (hier, Task 70 G2)** : collection `@Bibliotheque-skills-Multi-IA` — 10 fichiers présents, entrée KB, projections hôte, générateur ×2 byte-identique.
- G4.3 — **Élément n°3 (hier, Task 70 G3)** : collection `@GHORG-ecosysteme` + `ghorg-cmdr` v1.1.0 — 4 fichiers, constantes MANIFESTE/SELECTION re-pointées, py_compile scripts ecosystem 6/6, Karnaugh 20/20, distinction ×3 (branche overlay CMDR + cmdr/ecosystem/ intacts).
- G4.4 — **Élément n°4 (hier, Task 70 G4)** : étude faisabilité — livrable présent + mesures terrain JSON re-vérifiées (existence, cohérence des chiffres cités R1/R2).
- G4.5 — **Élément n°5 (hier, Task 70 G5 + CLOSE)** : plan Task 70 + rapport final + rapport tests installation — présents, verdicts PASS tracés.
- G4.6 — **Élément n°6 (aujourd'hui)** : plan `plan-genplan-push-main-20261108.md` + chaîne E7-DISP (check_plan_protocol P1-P5) + réparations volatilité ×3 (ensure-installed INSTALLE-REPARÉ) + éléments G1-G3 du présent plan (règle durcie, R1, R2) re-testés en fin de chaîne (auto-inclusion).
- G4.7 — Harnais orchestrateur `scripts/task71-tests-chronologiques.py` (stdlib, T1-T13+, verdict PASS/FAIL par test, rapport JSON + MD dans download/).
- correct-work(groupe G4) → D009.

### G5 — correct-work (projet) --bloc (#token ~12 k)
- Rapport bloc par bloc : 6 blocs (G1→G6 du présent plan), Étapes 2-5 par bloc, findings classés S1-S4, verdict par bloc, agrégation pire-des-verdicts, table « Blocs vérifiés » → `download/rapport-correct-work-task71.md` → D011.

### G6 — clone-chat (#token ~10 k)
- Archive auto-suffisante de la discussion (contexte, décisions, artefacts, worklog — format clone-chat v2.0.2, 7+1 étapes) → `download/clone-chat-session-web-ecef7f80-20261108.md` → D012.

## Verdict E8 : PASS (13 décisions à vérification exécutable criterion/verification, structure conforme P1-P5, chaîne step G1→G6 avec correct-work(groupe) après chaque groupe et correct-work(projet) --bloc en G5 — Horodatage vérifié : 2026-11-07T18:58:31Z)

- Arbitre : `python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task71-step-langue-push-r1r2-tests-cw-clone.md --worklog worklog.md`
- #token par groupe : G1 ~8 k · G2 ~5 k · G3 ~30 k · G4 ~20 k · G5 ~12 k · G6 ~10 k.
