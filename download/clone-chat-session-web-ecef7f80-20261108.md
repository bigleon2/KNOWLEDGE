# Clone de discussion — 2026-11-08 — Task 71 : langue + push + R1/R2 + tests chronologiques + correct-work --bloc + clone-chat (session web-ecef7f80, continuation Task 70)

> Clone auto-suffisant (clone-chat v2.0.2 — template §0-§5, 7+1 étapes). Sert à reprendre la mission sans le contexte de la discussion d'origine.

## §0 — Métadonnées et héritage

- **Session** : web-ecef7f80 (continuation — la veille a couvert Task 70 CLOSE : intégration collections @Bibliotheque-skills-Multi-IA + @GHORG-ecosysteme, tests installation $FACON2, étude faisabilité performance OOP/noyau, chaîne step G1→G5 complète, commit cea7d12 + 886604d)
- **Lignée** : continuation directe de la discussion Task 70 (clone le plus récent : 2026-10-26 directive 10 tâches)
- **Directive propriétaire (verbatim, gen-plan(step))** : (1) « tu communiques à nouveau depuis quelques instants dans d'autres langues que le "français" […] durcis l'application de cette règle au sein de mon écosystème pour que cette erreur ne se reproduise plus » ; (2) « PUSH avec ma clé "github_pat_…" » ; (3) « je veux appliquer tes recommandations "R1" et "R2". analyse comment les intégrer $FACON à mon écosystème […] fais des tests $FACON2 avant de les intégrer pour trouver la méthode la plus optimisée et performante » ; (4) « génère $FACON, effectue des tests $FACON2 fonctionnels et performances des éléments de mon écosystème créés ou modifiés dans cette discussion hier et aujourd'hui […] en suivant la chronologie de la création ou modification » ; (5) correct-work (projet) --bloc ; (6) clone-chat.
- **Étapes 3.5 Context Drift** : (1) dérive langue constatée par le propriétaire (textes de raisonnement anglais/chinois alors que la réponse finale était conforme) — CORRECTION immédiate sans transition + durcissement règle d'or n°6 (G1) ; (2) PAT GitHub collé au chat — KO-L009 systématique : jeton ni recopié ni stocké ni utilisé, guidance révocation, push délégué au propriétaire ; (3) volatilité version-management : 4 disparitions DANS la session (35e-38e), réparées ×4 par la garde externe ensure-installed.py.

## §1 — Contexte et décisions (résumé auto-suffisant)

- **D001/D002 (langue)** : règle d'or n°6 durcie — gen-plan v3.37.2 : portée MÉCANIQUE de la règle étendue à TOUT texte produit par l'agent (raisonnements affichés, titres, libellés, légendes, blocs PLAN-AFFICHE, résumés de continuation, reformulations de sorties d'outils) ; un raisonnement interne en langue étrangère = DÉRIVE au même titre qu'une réponse ; constat propriétaire → correction + worklog + durcissement (cycle fermé). Propagée par SHARED v1.7.32 (§0) à tout l'écosystème.
- **D003/D004/D013 (push/KO-L009)** : le PAT collé au chat n'est PAS utilisé (KO-L009 1-2-5) ; valeur complète absente du disque (vérifié : les occurrences `github_pat_` = motifs de garde + formes tronquées de l'incident du 2026-10-26 — ce jeton a donc circulé au moins 2 fois en clair) ; pendance push : 6 commits en attente, à pousser par le propriétaire APRÈS révocation du jeton exposé.
- **D005/D006 (R1)** : hook E5-POIDS — arbitre `scripts/poids-chargement.py` (Kio + #token estimés par skill, seuils OK < 12 / LOURD ≥ 30 / CRITIQUE ≥ 60 Kio ; lecture ciblée obligatoire pour LOURD/CRITIQUE : §0 + sommaire + sections dédiées, references/ à la demande). Rapport de priorisation : gen-plan = CRITIQUE (102,8 Kio ≈ 26 312 tokens) = cible n°1 de la curation R1 future.
- **D007/D008 (R2)** : hook R2-CACHE — `scripts/cache-verdicts.py` (verdict figé une fois, re-jeu sans ré-appel, clé SHA-256 commande + état des cibles, invalidation automatique, --force = re-exécution réelle). Démo mesurée sur check-ecosysteme-integrity.py : **gain 440×** (45,5 ms → 0,1 ms), verdict figé identique, invalidation sur touch OK.
- **D009 (tests chronologiques)** : harnais `scripts/task71-tests-chronologiques.py` — 15/15 PASS, ordre = chronologie de création/modification (T1-T9 hier Task 70, T10-T14 aujourd'hui Task 71, T15 arbre à pousser + dépendances).
- **D010 (cascade)** : après chaque montée de version (v3.37.2 PATCH, v3.38.0 MINOR) : PM généré mécaniquement + SHARED/PM-INSTALL recalibrés + PMs archivés R4 + pin ECO_SKILLS + KB + historiques-par-skill + ULTRA + sweep §0 + re-scellage archive + arbitres (integrity 110/110 · coherence 54/1/0 · cross 100 % · vcw ALL PASS · tool-routing PASS).
- **F-71-3 (résorption structurelle, 3ᵉ occurrence classe F-70-2)** : propagate-context v2.1.1 — la version SHARED des gabarits est désormais DÉRIVÉE DYNAMIQUEMENT du corpus vivant (KO-L003) ; un bump SHARED sans montée de l'injecteur ne peut plus jamais rétrograder les étiquettes §0. Preuve : propagation = 70 skills + 166 scripts + 2 agents, puis no-op idempotent.

## §2 — Artefacts produits (vérifiables sur disque)

- **Plan** : `download/plan-task71-step-langue-push-r1r2-tests-cw-clone.md` (13 décisions, E8 PASS, answer-key-checker 16/16) + plan intermédiaire `download/plan-genplan-push-main-20261108.md` (P1-P5 PASS).
- **Nouveaux scripts** (hôte + dépôt) : `scripts/poids-chargement.py` v1.0.0 (selftest 10/10), `scripts/cache-verdicts.py` v1.0.0 (selftest 12/12), `scripts/task71-tests-chronologiques.py` (15/15), `scripts/task71-g1-cascade.py`, `scripts/task71-g3-cascade.py`, deltas `scripts/delta-genplan-v3372.json` / `v3380.json`, preuve `scripts/task71-r2-demo-preuve.json`, rapport JSON `scripts/task71-tests-chronologiques.json`.
- **Écosystème versionné** : gen-plan v3.38.0 (hooks E5-POIDS + R2-CACHE au §1.2bis) ; PM v3.38.0 (corpus) ; PMs v3.37.1/v3.37.2 archivés @historique/prompts-maitres/gen-plan/ ; SHARED v1.7.33 ; PM-INSTALL v1.9.9 ; KB gen-plan v3.38.0 ; propagate-context v2.1.1 (dérivation dynamique) ; ULTRA SHA c3146d6a171a ; pin ECO_SKILLS 3.38.0.
- **Rapports** : `download/rapport-poids-chargement-task71.md`, `download/rapport-tests-chronologiques-task71.md`, `download/rapport-correct-work-task71.md` (bloc par bloc, 6 blocs PASS), le présent clone.
- **Commits en attente de push (6)** : cea7d12 + 886604d (Task 70) · 1f80594 (G1) · 8acc8c1 (G2+G3) · 2daaa9b (G4) · commit final G5+G6 (worklog + rapports + clone).

## §3 — État de sortie et reprise mécanique

1. **PUSH (propriétaire uniquement — KO-L009 point 5)** : (a) RÉVOQUER d'abord le jeton exposé : GitHub → Settings → Developer settings → Personal access tokens → révoquer (il a circulé en clair au moins 2 fois : 2026-10-26 + 2026-11-08) ; (b) puis depuis un environnement authentifié : `cd /home/z/my-project/KNOWLEDGE-repo && git push origin main` — 6 commits, fast-forward attendu (base = origin/main = 7eb5f42).
2. **Curation R1 (prochaine mission suggérée)** : re-curation progressive disclosure du SKILL.md gen-plan (102,8 Kio → corps court + references/, cible : < 30 Kio) — file de priorisation complète dans `download/rapport-poids-chargement-task71.md` (9 LOURD + 1 CRITIQUE).
3. **Volatilité version-management** : la garde externe (ensure-installed.py) répare à toute invocation gen-plan ; pour une résorption structurelle complète, voir le chantier Task 69 (watchdog — noté : le watchdog hébergé DANS le skill disparaît avec lui, chemin T2b).
4. **Câblage R2 exhaustif** : passer les graders fréquents par `cache-verdicts.py` avec leurs listes de cibles complètes (démo : 4 cibles représentatives — F-71-4).

## §4 — Leçons session (propositions knowledge-observer)

- L-71-a : une règle de langue ne couvrant que la « réponse finale » laisse les textes de raisonnement dériver — le durcissement rend la portée mécanique (tout texte produit).
- L-71-b : un injecteur à gabarit figé rétrograde silencieusement les étiquettes propagées à chaque run — la version d'un gabarit de propagation doit TOUJOURS être dérivée dynamiquement de la source (KO-L003 appliqué aux injecteurs, 3ᵉ occurrence de la classe).
- L-71-c : l'ordre « tests AVANT intégration » d'une directive doit être prouvé par les horodatages des artefacts (selftests → hooks), pas seulement déclaré.
- L-71-d : la sécurité (KO-L009) prime sur une directive d'exécution contraire — la réaction est systématique, la guidance remplace l'exécution, la pendance est consignée avec les commandes exactes.

## §5 — Worklog (extrait Task ID 27 — forme conforme SHARED §1.4, dépôt = source R4)

- E1-RES : piliers présents ; 4 disparitions version-management dans la session (35e-38e), réparées ×4 (INSTALLE-REPARÉ), arbitre 110/110 à chaque reprise.
- Dérive langue constatée → corrigée immédiatement sans transition ; durcissement G1 (gen-plan v3.37.2, cascade complète).
- KO-L009 déclenché : PAT collé au chat — ni recopié ni stocké ni utilisé ; guidance révocation ; push non exécuté par l'agent.
- G2+G3 : R1+R2 intégrés (hooks E5-POIDS + R2-CACHE, gen-plan v3.38.0, cascade, résorption structurelle F-71-3 propagate-context v2.1.1).
- G4 : harnais chronologique 15/15 PASS idempotent.
- G5 : correct-work (projet) --bloc PASS (0 S1 · 0 S2 · 3 S3 résorbés · 1 S4 consigné) ; G6 : clone-chat (le présent fichier).
- Pendance : push des 6 commits par le propriétaire après révocation du jeton exposé.
