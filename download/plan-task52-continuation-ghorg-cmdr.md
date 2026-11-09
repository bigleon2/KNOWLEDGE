# Plan d'actions — Task 52 : continuation GHORG/CMDR (forks + push + PR sur GO) + test $FACON2 compilation Windows CMDR + clôture

**Généré via gen-plan v3.35.0** (mode step §5.5, KO-L005 — première génération via la version portant la règle d'or n°9, elle-même appliquée en préalable : profil post-coupure réinstallé et certifié) · Session web-c30e6506 · 2026-11-05
**Horodatage plan : 2026-11-05T04:38:16+00:00**

---

## Contexte (E1-E2 — recensement intégral, règle d'or n°7)

**Directives propriétaire couvertes (verbatim, dans l'ordre d'arrivée) :**
1. « continue. GO avec mes clés "github_pat_…" et "at_…". fais un test $FACON2 fonctionnel de la compilation de CMDR sous WINDOWS. » ($FACON2 = « (cohérent, optimisé et fonctionnel) » — registre @historique/@Alias/)
2. « avant de continuer vérifie que mon écosystème est encore installé (si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill "gen-plan") et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill "gen-plan" est appelé après une coupure. » — **EXÉCUTÉE EN PRÉALABLE** : constat 14/52 → PM SHARED v1.7.22 lu intégralement → réinstallation MODE CLONE @ 5fed294 → arbitres 98/98 + 141/141 + 16/16 → gen-plan v3.34.0→v3.35.0 (règle d'or n°9, commit 9346385) → présent plan régénéré via v3.35.0.
3. Lignée Task 51 (rapport final download/rapport-final-task51-ghorg-cmdr.md §8) : forks ×2 à créer, GHORG_GITHUB_TOKEN, GO push feat/ghorg-ecosysteme + ecosystem/tsi-traktor-s4mk2 + 2 PR brouillon, compilation CMDR sous Windows.

**État disque vérifié (règle d'or n°5) :**
- Écosystème : réinstallé + certifié (integrity 98/98 ×2, verify-cross 141/141 (100 %) ×2, verify-correct-work 16/16, coherence 51/23/0 baseline, garde-plans PASS, doublons 0) — dépôt clone ~/GitHub/bigleon2/KNOWLEDGE @ 9346385 (main, Task 52 cascade commitée, non poussé).
- Profil local : gen-plan v3.35.0 synchronisé (pipeline F3 47 SHA 0 divergence) ; fichiers Task 51 présents (ecosystem/ 4 fichiers, scripts/ecosystem/ 6 fichiers + tests, skills/ghorg-cmdr v1.0.0, livrables download/).
- ~/GitHub : clone KNOWLEDGE présent ; **ghorg + cmdr perdus** (recyclage sandbox) ; journal d'état etat-ghorg-ecosysteme.json perdu.
- Forks : bigleon2/ghorg + bigleon2/cmdr **inexistants** (F=0 ×2) — sources gabrie30/ghorg @ e05d9b5f (master), cmdr-editor/cmdr @ 5b795027 (master).
- Clés : GH_TOKEN (github_pat_) **validé bigleon2** (API /user, usage éphémère PAR INVOCATION — leçon Task 50) ; clé at_ → **401 GitHub (clé non-GitHub — usage non déterminé, consignée sans valeur)** ; GO propriétaire explicite pour actions distantes (forks, push, PR — KO-L009 point 5 satisfait, 9e exposition consignée, rotation recommandée).
- Environnement : Linux, git 2.x, python3 ; go/gh à vérifier (go requis pour D4 ; l'API REST remplace gh pour forks/PR).

**Périmètre et dérogation documentée :** PM ghorg-to-ecosysteme.md v1.1 (D1-D8 + §8) — la compilation de CMDR sous Windows (§4 MD : « ni compiler, ni lancer » sous Linux) est testée via **GitHub Actions `runs-on: windows-latest`** (runner Windows réel fourni par GitHub) : la compilation s'exécute SUR Windows, la contrainte Linux reste respectée ; branche dédiée `test/compilation-windows` (jamais la branche par défaut — règle n°3 du MD).

---

## Answer key (E1 — décisions D301-D310, criterion + verification exécutable)

- **D301** (S1, pending) — Forks créés : bigleon2/ghorg ← gabrie30/ghorg et bigleon2/cmdr ← cmdr-editor/cmdr (D1, idempotent : existe + filiation correcte = ne rien créer)
  - criterion: les deux forks existent sur bigleon2 avec filiation parent correcte
  - verification: `curl -s -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/repos/bigleon2/ghorg` → `"fork": true` + `"full_name": "gabrie30/ghorg"` dans .parent (idem bigleon2/cmdr → cmdr-editor/cmdr) ; `git ls-remote https://github.com/bigleon2/ghorg HEAD` répond
- **D302** (S1, pending) — GHORG local reconstruit (D4 : clone du fork, upstream gabrie30/ghorg, build Go conditionnel, marqueur, PATH)
  - criterion: clone ~/GitHub/_outils/ghorg origin=fork + upstream=source ; binaire construit si go présent, sinon repli documenté
  - verification: `git -C ~/GitHub/_outils/ghorg remote -v` (2 remotes corrects) ; `go version` && `~/GitHub/_outils/bin/ghorg version` OU mention « binaire NON RECONSTRUIT » au worklog ; `cat ~/GitHub/_outils/bin/.ghorg-commit` == `git -C ~/GitHub/_outils/ghorg rev-parse HEAD`
- **D303** (S1, pending) — CMDR re-cloné via GHORG (D5 : Karnaugh F1L0 règle 2, --no-clean --concurrency=1, token temporaire même invocation, upstream + fetch)
  - criterion: clone ~/GitHub/bigleon2/cmdr origin=bigleon2/cmdr, upstream=cmdr-editor/cmdr, branche master
  - verification: `git -C ~/GitHub/bigleon2/cmdr remote -v` ; `git -C ~/GitHub/bigleon2/cmdr rev-parse HEAD` == 5b7950272a55f73034d2df15de2917248e2e9616 ; `grep cmdr ~/GitHub/_outils/cmdr-cibles.txt`
- **D304** (S1, pending) — Branche feat/ghorg-ecosysteme reconstruite depuis main @ 9346385 (fichiers Task 51 du profil, KB 50e entrée, arbiter ECO_SKILLS += ghorg-cmdr, worklog Task 51, hygiène dev.log)
  - criterion: la branche porte les fichiers D3 du MD + l'entrée KB ghorg-cmdr v1.0.0 + l'arbiter recalibré, sans toucher au code source
  - verification: `git -C ~/GitHub/bigleon2/KNOWLEDGE log --oneline main..feat/ghorg-ecosysteme` (commits atomiques) ; `git -C ~/GitHub/bigleon2/KNOWLEDGE checkout feat/ghorg-ecosysteme && python3 scripts/check-ecosysteme-integrity.py` → 0 FAIL (100/100 avec ghorg-cmdr) ; `git ls-files dev.log` vide
- **D305** (S1, pending) — Superposition D6 rejouée idempotente (branche ecosystem/tsi-traktor-s4mk2, 55 fichiers + SOURCE.md, bootstrap re-scellant le manifeste)
  - criterion: 2e exécution bootstrap = déjà à jour, porcelain vide, 0 nouveau commit
  - verification: `python3 scripts/ecosystem/bootstrap.py` ×2 → 2e run « déjà à jour » ; `git -C ~/GitHub/bigleon2/cmdr status --porcelain | wc -l` == 0 ; `grep -c sha256 ~/GitHub/bigleon2/cmdr/ecosystem/SOURCE.md` ≥ 55
- **D306** (S1, pending) — Test $FACON2 compilation CMDR sous WINDOWS (GitHub Actions windows-latest, branche dédiée test/compilation-windows, dispatch API, logs + artefacts)
  - criterion: un run Windows réel est exécuté sur bigleon2/cmdr et sa conclusion + logs sont récupérés (succès OU échec documenté = résultat réel)
  - verification: `curl -s -H "Authorization: Bearer $GH_TOKEN" "https://api.github.com/repos/bigleon2/cmdr/actions/runs?branch=test/compilation-windows"` → status completed + conclusion ∈ {success, failure} ; logs téléchargés (preuve .txt) ; §8 n°11 mis à jour
- **D307** (S1, pending) — Publication sur GO : contrôles pré-push 4/4 puis push main + push branches + 2 PR brouillon
  - criterion: les 3 pushes sont vérifiés ls-remote == HEAD et les 2 PR brouillon existent (draft=true)
  - verification: `git ls-remote origin main` == HEAD local ; `curl -s -H "Authorization: Bearer $GH_TOKEN" "https://api.github.com/repos/bigleon2/KNOWLEDGE/pulls?head=bigleon2:feat/ghorg-ecosysteme"` → draft=true (idem cmdr) ; scan `github_pat_[A-Za-z0-9_]{20,}` sur diff == 0
- **D308** (S2, pending) — Tableau §8 du MD re-rempli (11 contrôles avec preuves — n°1-2 forks VÉRIFIÉS, n°11 compilation = résultat réel)
  - criterion: le rapport final porte les 11 statuts avec commandes et sorties en preuve
  - verification: `grep -c "VÉRIFIÉ\|ÉCHEC\|NON VÉRIFIÉ" download/rapport-final-task51-ghorg-cmdr.md` ≥ 11
- **D309** (S1, pending) — correct-work (projet) exécuté sur l'ensemble (chaîne Task 52 + continuation) — findings corrigés
  - criterion: verdict correct-work(projet) consigné avec 0 finding ouvert (ou réserves héritées documentées)
  - verification: `python3 scripts/verify-correct-work.py` 16/16 + rapport balayage D301-D310 présent
- **D310** (S2, pending) — Clôture : worklog D8, clone-chat scellé, livrables profil, pendances propriétaire
  - criterion: le clone de discussion passe les 8 checks S1-S8 et les livrables sont dans download/ (dépôt + profil)
  - verification: `ls download/clone-*task52*` + entrée worklog D8 + section pendances au rapport final

---

## Groupes d'exécution (mode step — structure hiérarchique §5.5)

**Vue d'ensemble** : G1 (forks + arbre de travail) → G2 (branche Task 51 + superposition + idempotence) → G3 (compilation Windows) → G4 (publication sur GO) → G5 (vérification §8 + rapport) → G6 (clôture correct-work + clone-chat).

### G1 — Forks + arbre de travail local (D1, D4, D5)
- **SG1.1 Forks ×2 (D1)** : vérifier inexistence (ls-remote anonyme), créer via API REST POST /repos/{source}/forks (GH_TOKEN même invocation, --default-branch-only équivalent : fork default branch seule — l'API crée toutes les branches par défaut, le clone sera --single-branch), boucle d'attente API < 60 s, vérifier filiation parent. Idempotent : existe + parent correct = ne rien créer. — *Tâches : T1.1.1 ghorg, T1.1.2 cmdr*
- **SG1.2 GHORG local (D4)** : clone fork → ~/GitHub/_outils/ghorg (single-branch master), remote upstream, build `go build -o ../bin/ghorg .` **seulement si go présent** (sinon : repli documenté « binaire NON RECONSTRUIT — compilation reportée au poste propriétaire », règle d'or n°1, le clone + scripts restent opérationnels), marqueur .ghorg-commit, PATH. — *T1.2.1 clone+remote, T1.2.2 build conditionnel, T1.2.3 marqueur+PATH*
- **SG1.3 CMDR via GHORG (D5)** : cmdr-cibles.txt (« cmdr »), GHORG_GITHUB_TOKEN=temporaire (même invocation), commande de référence MD §6.D5 (--no-clean --concurrency=1), origin re-pointé vers le fork (règle Karnaugh 2 — le clone précédent est perdu, F=1 L=0), upstream + fetch --prune, entrée reclone.yaml (UTF-8 sans BOM, entrées existantes préservées). — *T1.3.1 cibles+token, T1.3.2 ghorg clone, T1.3.3 remotes, T1.3.4 reclone.yaml*
- **SG1.4 Journal d'état** : etat-ghorg-ecosysteme.json recréé (phases D1-D8 avec états réels). — *T1.4.1*

### G2 — Branche feat/ghorg-ecosysteme + superposition + idempotence (D2-D3, D6)
- **SG2.1 Reconstruction de la branche** : depuis main @ 9346385, copie des fichiers Task 51 depuis le profil (ecosystem/ 4 fichiers, scripts/ecosystem/ 6 fichiers, skills/ghorg-cmdr/ SKILL.md + evals), KB += 50e entrée ghorg-cmdr v1.0.0, arbiter ECO_SKILLS += ghorg-cmdr 1.0.0 (sur la base v3.35.0 du main), entrées worklog Task 51 (plan + G5-G6) repositionnées avant l'entrée Task 52, hygiène dev.log (.gitignore + git rm --cached), commits atomiques au style du dépôt. — *T2.1.1 copies, T2.1.2 KB+arbiter, T2.1.3 worklog, T2.1.4 hygiène+commits*
- **SG2.2 Bootstrap D4→D5→D6 + re-scellement** : exécution bootstrap.py (re-scelle manifeste avec SHA réels du jour : forks maintenant existants), superposition branche ecosystem/tsi-traktor-s4mk2 (55 fichiers + SOURCE.md). — *T2.2.1 bootstrap, T2.2.2 vérification overlay*
- **SG2.3 Contrat idempotence §8 + arbitres** : bootstrap ×2 (« déjà à jour », porcelain 0, 0 commit), arbitres sur l'arbre branche (integrity 100/100 avec ghorg-cmdr, verify-cross, TC1 55/55 hashes, TC3 0 fichier hors ecosystem/). — *T2.3.1 run 2, T2.3.2 arbitres*
- **correct-work(groupe) G2** (max 2 rounds).

### G3 — Test $FACON2 compilation CMDR sous WINDOWS (§8 n°11, dérogation documentée)
- **SG3.1 Inspection de la chaîne de build** : lecture du clone cmdr (fichiers .sln/.csproj/.targets, style SDK vs old-style, dépendances NuGet, README build) → choix build (dotnet build / msbuild). — *T3.1.1 inventaire, T3.1.2 choix commande*
- **SG3.2 Workflow GitHub Actions** : branche dédiée test/compilation-windows (depuis master du fork), workflow .github/workflows/test-compilation-windows.yml (windows-latest, checkout, setup build tools, restore, build en mode Release, upload artefacts, summary), push branche, activation Actions sur le fork (API), dispatch (API). — *T3.2.1 branche+workflow, T3.2.2 push+activation, T3.2.3 dispatch*
- **SG3.3 Monitoring + preuves** : poll API runs (≤ 15 min), récupération logs + conclusion + artefacts, verdict $FACON2 (cohérent : workflow versionné ré-exécutable ; optimisé : cache/restore adaptés ; fonctionnel : conclusion réelle + artefacts binaires). — *T3.3.1 poll, T3.3.2 logs+artefacts, T3.3.3 verdict*
- **correct-work(groupe) G3** (max 2 rounds).

### G4 — Publication (D7 — GO propriétaire donné, KO-L009 point 5)
- **SG4.1 Contrôles pré-push 4/4** : (1) fast-forward ls-remote origin/main == 5fed294 (parent du commit Task 52) ; (2) arbitres re-exécutés ; (3) 0 secret (scan pattern + diff) ; (4) diff propre. — *T4.1.1-T4.1.4*
- **SG4.2 Push main** : 9346385 (+ commits clôture worklog/livrables) → main, ls-remote == HEAD. — *T4.2.1*
- **SG4.3 Push + PR KNOWLEDGE** : feat/ghorg-ecosysteme → origin, PR brouillon (titre + description français, base main). — *T4.3.1 push, T4.3.2 PR*
- **SG4.4 Push + PR cmdr** : ecosystem/tsi-traktor-s4mk2 → fork bigleon2/cmdr, PR brouillon (base master, description : superposition famille TSI + workflow test Windows). — *T4.4.1 push, T4.4.2 PR*
- **SG4.5 Vérifications post-push** : ls-remote ×3, URLs PR consignées, état journal mis à jour (phases terminé). — *T4.5.1*
- **correct-work(groupe) G4** (max 2 rounds).

### G5 — Vérification finale §8 + rapport (Phase E)
- **SG5.1 Tableau §8 complet** : 11 contrôles re-remplis avec preuves (n°1-2 forks VÉRIFIÉS, n°3 manifeste re-scellé, n°4 origin=fork, n°5 écart upstream, n°6 reclone.yaml, n°7 SOURCE.md, n°8 périmètre, n°9 0 secret, n°10 idempotence, n°11 compilation Windows = résultat réel). — *T5.1.1*
- **SG5.2 Rapport final mis à jour** : download/rapport-final-task51-ghorg-cmdr.md (§3 tableau + §8 actions propriétaire réduites : merge PR, rotation PAT, GHORG_GITHUB_TOKEN poste, clé at_) + sync dépôt download/. — *T5.2.1*
- **correct-work(groupe) G5** (max 2 rounds).

### G6 — Clôture
- **SG6.1 correct-work (projet)** : balayage D301-D310 + vérificateur mécanique + verdict. — *T6.1.1*
- **SG6.2 Worklog + clone-chat** : entrée D8 (continuation + compilation Windows + publication), clone-chat scellé (8 checks), livrables profil. — *T6.2.1, T6.2.2*
- **SG6.3 Pendances propriétaire** : fusion 2 PR, rotation PAT (9e exposition), GHORG_GITHUB_TOKEN au poste, clé at_ (usage à préciser), go local pour binaire ghorg si non provisionné. — *T6.3.1*

---

## Budget #token (profil NORMAL, contingence ×2)

| Groupe | Estimation | Dominante |
|---|---|---|
| G1 | ~12 k | API forks + clones + build |
| G2 | ~14 k | reconstruction branche + bootstrap ×2 + arbitres |
| G3 | ~10 k | workflow + monitoring API + logs |
| G4 | ~8 k | contrôles + push + PR |
| G5 | ~6 k | tableau §8 + rapport |
| G6 | ~8 k | correct-work + clone-chat |
| **Total** | **~58 k** | + contingence ×2 (coupure possible) |

---

## Verdict E8

Verdict E8 : PASS — la chaîne D301-D310 couvre l'intégralité des directives (continuation Task 51 sur GO avec clés, test $FACON2 compilation Windows via runner GitHub réel, vérification post-coupure devenue règle d'or n°9 et exécutée en préalable) ; l'ordre des groupes respecte les dépendances (forks → clones → branche → superposition → build Windows → publication → vérification → clôture) ; chaque décision porte une vérification exécutable ; budget ~58 k#token calibré profil NORMAL avec contingence ×2 ; dérogations documentées (compilation Windows via runner GitHub — la contrainte « pas de compilation sous Linux » reste respectée ; repli go absent). — Horodatage vérifié : 2026-11-05T04:38:16+00:00
