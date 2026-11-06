# Plan d'actions — Task 53 : continuation GHORG/CMDR sur clés écriture (reconstruction locale + compilation Windows + publication) + clôture

**Généré via gen-plan v3.35.0** (mode step §5.5, KO-L005 — régénération ordonnée par directive propriétaire, l'installation de l'écosystème étant terminée et certifiée) · Session web-c30e6506 · 2026-11-06
**Horodatage plan : 2026-11-06T16:58:10+00:00**

---

## Contexte (E1-E2 — recensement intégral, règle d'or n°7)

**Directives propriétaire couvertes (verbatim, dans l'ordre d'arrivée) :**
1. « continue. GO avec mes clés "github_pat_…" et "at_…". fais un test $FACON2 fonctionnel de la compilation de CMDR sous WINDOWS. » (lignée Task 51/52 — $FACON2 = « (cohérent, optimisé et fonctionnel) », registre @historique/@Alias/)
2. « avant de continuer vérifie que mon écosystème est encore installé (si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill gen-plan est appelé après une coupure. » — directive PERMANENTE codifiée **règle d'or n°9** (gen-plan v3.35.0)
3. « voilà mes clés avec "actions", "pull request", "contents" et "worfkflows" en "read/write" » (2 PAT fournies ce jour — exactement les permissions demandées au §4 du rapport Task 52)
4. « avant de continuer, fais dans l'ordre les étapes suivantes : { - installe mon écosystème personnel en tant que mon écosystème personnel sur mon profil local grâce à mon fichier "https://github.com/bigleon2/KNOWLEDGE/blob/b75a62066791a8cce8c1ec5d1dbe7d976bae4244/skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md" et lorsque l'installation de mon écosystème sera terminée, prend en compte mon skill "gen-plan" fraichement installé pour générer le plan d'actions des étapes suivantes : { - regénère les taches du plan d'actions actuel via à "gen-plan (step)". } } » — **EXÉCUTÉE EN PRÉALABLE** (règle d'or n°9, 3ᵉ application) : profil post-recyclage 13/51 → PM SHARED lu intégralement → installation voie directe `eco_install_pipeline.py` (clone certifié descendant du pin b75a620) → **découverte : l'archive d'intégrité locale était l'archive scellée Task 52 portant le PM v3.35.0 perdu → garde anti-perte → état certifié Task 52 RESTAURÉ byte-exact depuis l'archive** (commits d33b8e5 + 6720617 : corpus v3.35.0/SHARED v1.7.23/PM-INSTALL v1.9.1 + SKILL.md v3.35.0 reconstruit + recalibrage KO-L004 rejoué + propagateur v2.0.5) → certification **6/6 arbitres** (141/141 ×2, 16/16, 98/98, cohérence 51/23/0 baseline restaurée) → **présent plan régénéré via le gen-plan v3.35.0 réinstallé** (chemin (d) de la règle d'or n°9).

**État disque vérifié (règle d'or n°5) :**
- Écosystème : installé + certifié (voir ci-dessus) — clone ~/GitHub/bigleon2/KNOWLEDGE @ 6720617 (main, commits de restauration NON poussés) ; profil synchronisé (F3 47 SHA, 0 divergence) ; archive d'intégrité rescellée round-trip 9/9.
- Clés : **K1 testée — auth `bigleon2`, admin/push TRUE sur bigleon2/KNOWLEDGE + bigleon2/cmdr + bigleon2/ghorg** (le bloqueur P0 de Task 52 — clé lecture seule, 4×403 + re-test — est LEVÉ) ; K2 auth bigleon2 OK (écriture non testée, K1 suffisante — consignée). Expositions canal : 10e/11e (KO-L009 — rotation en pendances).
- ~/GitHub : clone KNOWLEDGE ✓ ; **ghorg + cmdr + journal d'état PERDUS** (3ᵉ recyclage sandbox) ; sauvegarde de récupération ~/GitHub/_recuperation-task52/ (archive + corpus extraits).
- Forks : bigleon2/ghorg + bigleon2/cmdr **EXISTANTS** (créés par le propriétaire — D301 pérenne, vérifiés API : fork=true, parents gabrie30/ghorg @ e05d9b5f + cmdr-editor/cmdr @ 5b795027).
- Remotes : KNOWLEDGE main @ 5fed294 (fast-forward local 6720617 ✓ vérifié ls-remote), cmdr master @ 5b795027, ghorg master @ e05d9b5f — AUCUNE branche distante (feat/overlay/test inexistantes côté distant).
- Artifacts Task 52 perdus à reconstruire : branche feat/ghorg-ecosysteme (@ d71a897, 7 commits), branche ecosystem/tsi-traktor-s4mk2 (@ 22490d4, superposition 55 fichiers), branche test/compilation-windows (@ f14be50, workflow). **Fichiers survivant au profil** : ecosystem/ (4 fichiers), scripts/ecosystem/ (6 + tests), skills/ghorg-cmdr/ (§0 v1.7.23 — fix F-G préservé), livrables download/.
- Environnement : Linux, git 2.x, python3 ; **go ABSENT** (repli documenté requis pour le binaire ghorg — l'API REST remplace gh pour tout le distant ; le clone cmdr se fait par git, Karnaugh F1L0 règle 2).

**Périmètre et dérogations documentées :** PM ghorg-to-ecosysteme.md v2 (download/ghorg-to-ecosysteme-v2.md, D1-D8 + §8) + lignée plans Task 51/52. Dérogation 1 (héritée, validée Task 52) : compilation CMDR sous Windows via **GitHub Actions `runs-on: windows-latest`** (runner Windows réel — la contrainte MD §4 « ni compiler, ni lancer » sous Linux reste respectée) ; branche dédiée `test/compilation-windows`. Dérogation 2 (nouvelle, go absent) : binaire ghorg NON RECONSTRUIT (repli documenté — clone cmdr par git avec remotes équivalents à la règle Karnaugh 2 ; règle d'or n°1, journalisation worklog).

---

## Answer key (E1 — décisions D401-D408, criterion + verification exécutable)

- **D401** (S1, pending) — Arbre de travail local reconstruit : clone cmdr (~/GitHub/bigleon2/cmdr, origin=fork, upstream=cmdr-editor/cmdr, master @ 5b795027) + clone ghorg (~/GitHub/_outils/ghorg, origin=fork, upstream=source @ e05d9b5f, binaire NON RECONSTRUIT — go absent, repli documenté) + reclone.yaml (UTF-8 sans BOM) + journal d'état recréé
  - criterion: les 2 clones présentent les remotes Karnaugh corrects et le journal d'état couvre D1-D8
  - verification: `git -C ~/GitHub/bigleon2/cmdr remote -v` (origin=bigleon2/cmdr, upstream=cmdr-editor/cmdr) ; `git -C ~/GitHub/bigleon2/cmdr rev-parse HEAD` == 5b7950272a55f73034d2df15de2917248e2e9616 ; `git -C ~/GitHub/_outils/ghorg remote -v` ; `grep cmdr ~/.config/ghorg/reclone.yaml` ; `ls ~/GitHub/_outils/etat-ghorg-ecosysteme.json`
- **D402** (S1, pending) — Branche feat/ghorg-ecosysteme reconstruite depuis main @ 6720617 (fichiers Task 51 du profil : ecosystem/ + scripts/ecosystem/ + skills/ghorg-cmdr §0 v1.7.23, KB 50ᵉ entrée ghorg-cmdr v1.0.0, arbiter ECO_SKILLS += ghorg-cmdr, worklog lignée, hygiène dev.log, commits atomiques)
  - criterion: la branche porte le contenu D3 du MD + l'entrée KB + l'arbiter recalibré, sans régression de l'état v3.35.0 de main
  - verification: `git -C ~/GitHub/bigleon2/KNOWLEDGE log --oneline main..feat/ghorg-ecosysteme` (commits atomiques) ; sur la branche : `python3 scripts/check-ecosysteme-integrity.py` → 0 FAIL (avec ghorg-cmdr) ; `git ls-files dev.log` vide ; `grep -c "## ghorg-cmdr" skills/KNOWLEDGE.md` == 1
- **D403** (S1, pending) — Superposition D6 rejouée idempotente (branche ecosystem/tsi-traktor-s4mk2 du clone cmdr : 55 fichiers famille TSI + SOURCE.md, bootstrap re-scellant le manifeste avec les SHA réels du jour)
  - criterion: 2ᵉ exécution bootstrap = « déjà à jour », porcelain vide ×2, 0 nouveau commit
  - verification: `python3 scripts/ecosystem/bootstrap.py` ×2 → 2ᵉ run D6 « déjà à jour » ; `git -C ~/GitHub/bigleon2/cmdr status --porcelain | wc -l` == 0 ; `grep -c sha256 ~/GitHub/bigleon2/cmdr/ecosystem/SOURCE.md` ≥ 55 ; `git -C ~/GitHub/bigleon2/cmdr diff --name-only master...HEAD | grep -v "^ecosystem/" | wc -l` == 0
- **D404** (S1, pending) — Test $FACON2 compilation CMDR sous WINDOWS (workflow RECRÉÉ — le f14be50 est perdu : .github/workflows/test-compilation-windows.yml sur branche dédiée test/compilation-windows depuis master, windows-latest, checkout + restore NuGet + build Release|Any CPU + upload artefacts, push, activation Actions API, dispatch API, monitoring ≤ 20 min, logs + conclusion + artefacts récupérés)
  - criterion: un run Windows réel est exécuté sur bigleon2/cmdr et sa conclusion + logs sont récupérés (succès OU échec documenté = résultat réel)
  - verification: `curl -s -H "Authorization: Bearer $GH_TOKEN" "https://api.github.com/repos/bigleon2/cmdr/actions/runs?branch=test/compilation-windows"` → status completed + conclusion ∈ {success, failure} ; logs téléchargés (preuve .txt) ; §8 n°11 du rapport mis à jour avec le résultat réel
- **D405** (S1, pending) — Publication sur GO (contrôles pré-push 4/4 puis 3 pushes + 2 PR brouillon) : push KNOWLEDGE main (5fed294 → 6720617 + commits de clôture) ; push feat/ghorg-ecosysteme + PR brouillon (base main) ; push cmdr ecosystem/tsi-traktor-s4mk2 + PR brouillon (base master, mention superposition TSI + test Windows) ; push cmdr test/compilation-windows
  - criterion: ls-remote == HEAD local ×4 et les 2 PR brouillon existent (draft=true)
  - verification: `git ls-remote origin main` == HEAD local (idem branches ×3) ; `curl -s -H "Authorization: Bearer $GH_TOKEN" "https://api.github.com/repos/bigleon2/KNOWLEDGE/pulls?head=bigleon2:feat/ghorg-ecosysteme"` → draft=true (idem cmdr overlay) ; scan `github_pat_[A-Za-z0-9_]{20,}` sur les diffs == 0
- **D406** (S2, pending) — Tableau §8 du MD re-rempli (11 contrôles avec preuves — n°1-2 forks VÉRIFIÉS, n°11 compilation = résultat réel D404)
  - criterion: le rapport final porte les 11 statuts avec commandes et sorties en preuve
  - verification: `grep -c "VÉRIFIÉ\|ÉCHEC\|NON VÉRIFIÉ\|PRÊT" download/rapport-final-task53-ghorg-cmdr.md` ≥ 11
- **D407** (S1, pending) — correct-work (projet) exécuté sur l'ensemble (installation v3.35.0 + reconstruction + compilation + publication) — findings corrigés
  - criterion: verdict correct-work(projet) consigné avec 0 finding ouvert (ou réserves documentées)
  - verification: `python3 scripts/verify-correct-work.py` 16/16 + rapport balayage D401-D408 présent au rapport final
- **D408** (S2, pending) — Clôture : worklog (profil + dépôt), clone-chat scellé (8 checks S1-S8), livrables download/, pendances propriétaire (fusion 2 PR, rotation des 2 PAT — 10e/11e expositions, GHORG_GITHUB_TOKEN au poste, go local pour le binaire ghorg)
  - criterion: le clone de discussion passe les 8 checks et les livrables sont dans download/
  - verification: `ls download/clone-*task53*` + entrée worklog finale + section pendances au rapport final

---

## Groupes d'exécution (mode step — structure hiérarchique §5.5)

**Vue d'ensemble** : G1 (arbre de travail local) → G2 (branche Task 51 + superposition + idempotence) → G3 (compilation Windows) → G4 (publication sur GO) → G5 (vérification §8 + rapport) → G6 (clôture correct-work + clone-chat).

### G1 — Arbre de travail local (D401)
- **SG1.1 Clone cmdr (règle Karnaugh F1L0-2)** : clone --single-branch du fork bigleon2/cmdr (master @ 5b795027) → ~/GitHub/bigleon2/cmdr, remote upstream cmdr-editor/cmdr, fetch --prune. — *T1.1.1 clone, T1.1.2 remotes*
- **SG1.2 Clone ghorg (repli documenté)** : clone du fork → ~/GitHub/_outils/ghorg, upstream gabrie30/ghorg ; go ABSENT → binaire NON RECONSTRUIT (mention worklog, disposition manifeste inchangée — le marqueur .ghorg-commit attendra go). — *T1.2.1 clone, T1.2.2 mention repli*
- **SG1.3 reclone.yaml + journal d'état** : entrée cmdr-editor-fork (UTF-8 sans BOM, entrées existantes préservées) ; etat-ghorg-ecosysteme.json recréé (phases D1-D8, états réels du jour). — *T1.3.1, T1.3.2*
- **correct-work(groupe) G1** (max 2 rounds).

### G2 — Branche feat/ghorg-ecosysteme + superposition + idempotence (D402, D403)
- **SG2.1 Reconstruction de la branche** : depuis main @ 6720617, copie des fichiers Task 51 depuis le profil (ecosystem/ 4 fichiers, scripts/ecosystem/ 6 fichiers + test-karnaugh, skills/ghorg-cmdr §0 v1.7.23), KB += 50ᵉ entrée ghorg-cmdr v1.0.0, arbiter ECO_SKILLS += ghorg-cmdr 1.0.0, worklog lignée Task 51/52 repositionné, hygiène dev.log, commits atomiques au style du dépôt. — *T2.1.1 copies, T2.1.2 KB+arbiter, T2.1.3 worklog+hygiène, T2.1.4 commits*
- **SG2.2 Bootstrap D4→D5→D6 + re-scellement** : exécution bootstrap.py (re-scelle le manifeste avec les SHA réels : forks existants, clone du jour), superposition branche ecosystem/tsi-traktor-s4mk2 (55 fichiers + SOURCE.md). — *T2.2.1 bootstrap, T2.2.2 vérification overlay*
- **SG2.3 Contrat idempotence §8 + arbitres** : bootstrap ×2 (« déjà à jour », porcelain 0, 0 commit), arbitres sur l'arbre branche (integrity 0 FAIL avec ghorg-cmdr, TC1 55/55 hashes, TC3 0 fichier hors ecosystem/). — *T2.3.1 run 2, T2.3.2 arbitres*
- **correct-work(groupe) G2** (max 2 rounds).

### G3 — Test $FACON2 compilation CMDR sous WINDOWS (D404 — dérogation documentée, §8 n°11)
- **SG3.1 Inspection de la chaîne de build** : lecture du clone cmdr (.sln/.csproj, style SDK vs old-style, dépendances NuGet, README build) → choix build (dotnet build / msbuild). — *T3.1.1 inventaire, T3.1.2 choix commande*
- **SG3.2 Workflow GitHub Actions (RECRÉÉ)** : branche dédiée test/compilation-windows (depuis master du fork), .github/workflows/test-compilation-windows.yml (windows-latest, checkout, setup build tools, restore, build Release|Any CPU, upload artefacts, summary), push branche, activation Actions sur le fork (PUT actions/permissions), dispatch (POST workflows/…/dispatches, ref=test/compilation-windows). — *T3.2.1 branche+workflow, T3.2.2 push+activation, T3.2.3 dispatch*
- **SG3.3 Monitoring + preuves** : poll API runs (≤ 20 min), récupération logs + conclusion + artefacts, verdict $FACON2 (cohérent : workflow versionné ré-exécutable ; optimisé : restore/outils adaptés ; fonctionnel : conclusion réelle + artefacts). — *T3.3.1 poll, T3.3.2 logs+artefacts, T3.3.3 verdict*
- **correct-work(groupe) G3** (max 2 rounds).

### G4 — Publication (D405 — GO propriétaire donné, KO-L009 point 5)
- **SG4.1 Contrôles pré-push 4/4** : (1) fast-forward ls-remote origin/main == 5fed294 (base locale 6720617) ; (2) arbitres re-exécutés ; (3) 0 secret (scan pattern + diff des 3 arbres) ; (4) diffs propres (main / feat / overlay / test). — *T4.1.1-T4.1.4*
- **SG4.2 Push main** : 6720617 (+ commits clôture G5-G6) → main, ls-remote == HEAD. — *T4.2.1*
- **SG4.3 Push + PR KNOWLEDGE** : feat/ghorg-ecosysteme → origin, PR brouillon (titre + description français, base main). — *T4.3.1 push, T4.3.2 PR*
- **SG4.4 Push + PR cmdr** : ecosystem/tsi-traktor-s4mk2 → fork bigleon2/cmdr, PR brouillon (base master, description : superposition famille TSI + branche test Windows) ; push test/compilation-windows. — *T4.4.1 push ×2, T4.4.2 PR*
- **SG4.5 Vérifications post-push** : ls-remote ×4, URLs PR consignées, journal d'état mis à jour. — *T4.5.1*
- **correct-work(groupe) G4** (max 2 rounds).

### G5 — Vérification finale §8 + rapport (D406)
- **SG5.1 Tableau §8 complet** : 11 contrôles re-remplis avec preuves (n°1-2 forks VÉRIFIÉS, n°3 manifeste re-scellé, n°4 origin=fork, n°5 écart upstream, n°6 reclone.yaml, n°7 SOURCE.md, n°8 périmètre, n°9 0 secret, n°10 idempotence, n°11 compilation Windows = résultat réel D404). — *T5.1.1*
- **SG5.2 Rapport final Task 53** : download/rapport-final-task53-ghorg-cmdr.md (installation v3.35.0 + restauration + continuation + compilation + publication, pendances réduites). — *T5.2.1*
- **correct-work(groupe) G5** (max 2 rounds).

### G6 — Clôture (D407, D408)
- **SG6.1 correct-work (projet)** : balayage D401-D408 + lignée héritée D301-D310 (D306/D307 résolus par les présentes D404/D405) + vérificateur mécanique. — *T6.1.1*
- **SG6.2 Worklog + clone-chat** : entrées worklog (profil + dépôt), clone-chat scellé (8 checks), livrables download/. — *T6.2.1, T6.2.2*
- **SG6.3 Pendances propriétaire** : fusion 2 PR, rotation des 2 PAT (10e/11e expositions), GHORG_GITHUB_TOKEN au poste, go local pour le binaire ghorg. — *T6.3.1*

---

## Budget #token (profil NORMAL, contingence ×2)

| Groupe | Estimation | Dominante |
|---|---|---|
| G1 | ~8 k | clones + remotes + journal |
| G2 | ~14 k | reconstruction branche + bootstrap ×2 + arbitres |
| G3 | ~12 k | workflow + monitoring API + logs |
| G4 | ~10 k | contrôles + 4 pushes + 2 PR |
| G5 | ~6 k | tableau §8 + rapport |
| G6 | ~8 k | correct-work + clone-chat |
| **Total** | **~58 k** | + contingence ×2 (coupure possible) |

---

## Verdict E8

Verdict E8 : PASS — la chaîne D401-D408 couvre l'intégralité des directives (continuation lignée Task 51/52 sur GO avec les clés écriture fournies ce jour, test $FACON2 compilation Windows via runner GitHub réel, publication 4 pushes + 2 PR brouillon) ET de la directive d'installation (exécutée en préalable : écosystème restauré à l'état certifié v3.35.0 + certification 6/6 — le présent plan étant généré par le gen-plan fraîchement installé, chemin (d) de la règle d'or n°9) ; l'ordre des groupes respecte les dépendances (arbre local → branches + idempotence → build Windows → publication → vérification → clôture) ; chaque décision porte une vérification exécutable ; budget ~58 k#token calibré profil NORMAL avec contingence ×2 ; dérogations documentées (compilation Windows via runner GitHub ; repli go absent pour le binaire ghorg — clone cmdr par git, remotes Karnaugh équivalents). — Horodatage vérifié : 2026-11-06T16:58:10+00:00
