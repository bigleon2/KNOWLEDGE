# Plan — Publication GO + Campagne A/B/C de résorption des dérives triggers

Directive propriétaire (gen-plan prompt, session web-f90062ce) : « GO "PAT éphémère" + armer la campagne A/B/C de résorption des 16 dérives triggers (verdicts figés de la discussion réutilisables) ».

gen-plan : **v3.26.0** (hôte certifié INSTALLE, dépôt HEAD 45ef2ba). Mode : exécution directe (GO déjà accordé, aucune porte de confirmation).

## Lecture du périmètre (constat mesuré, règle d'or n°5)

- « 16 dérives » = la formulation de la discussion (« les 16 autres skills ») ; le périmètre canonique Task 30 = **19 skills en dérive = 3 iphone + 16 autres** — la campagne couvre les 19.
- Rejoue frais de l'arbitre `check-triggers-replay.py` (2026-10-24) : **104 skills, 85 OK, 19 en dérive, 33 cas échoués** (verdict FAIL informatif hérité — instrumentation Task 30 jamais commitée, D005).
- Source des verdicts figés : archive `scripts/discussion-64c90144.txt` (+ raw) — arbitrage Task 30 : Option A = 13 vetos exclusifs / 12 corpus (champ `exclusifs`, veto AVANT scoring) ; Option B = `voie-l-semantique.py` + cache `voie-l-cache.json` (19 verdicts figés, questions de ROUTAGE, description complète, sériel, 429 blindé) ; Option C = replay ×2 byte-identique. Verdicts explicites documentés : jd→true, ai→true, cahier→false, iphone19 poster→false (re-arbitrage routage), trio iphone (vetos « iphone 18 »/« iphone 17 »), 2 révisions REFUTE version-management v1.2.1, description-complète corrigée (version-management ×3, iphone19 « Améliore », cahier).
- Doctrine d'arbitrage Task 25 : verdict **CONFIRME-eval 3/3** — les evals sont conformes aux SKILL.md, la dérive vient de l'instrument (voie M). Le verdict figé d'un cas arbitrée = la valeur `should_trigger` du corpus, sauf les 2 REFUTE version-management (l'eval lui-même est révisé).

## Structure hiérarchique (§5.5)

### G1 — Publication GO (commits en attente) — 2 tâches
- **T1.1** Push origin/main des commits locaux (cad21a9, b38e0f7, 45ef2ba) avec le PAT éphémère ; vérification `ls-remote` ; zéro écriture du token dans tout fichier du dépôt ou des logs persistés (audit anti-persistance).
- **T1.2** Contrôle post-push : HEAD local = HEAD remote, arborescence propre (git status).

### G2 — Option A : vetos exclusifs (schéma + arbitre V6.1) — 3 tâches
- **T2.1** Arbitre `check-triggers-replay.py` V6 → **V6.1** : (a) veto AVANT scoring — si le cas porte `exclusifs` et que la requête contient un terme exclusif → verdict false (source `veto-exclusif`) ; (b) en cas de désaccord voie M/attendu → consultation lecture seule du cache voie L (`scripts/voie-l-cache.json`) — accord = OK (source `voie-l-cache`), désaccord = FAIL documenté, absence = FAIL (dégradation honnête) ; docstring Task 30.
- **T2.2** Application des vetos exclusifs aux corpus (script persisté, recensement mécanique) — dérivation depuis les cas négatifs échoués et les doctrines SKILL.md : trio iphone (périmètre d'époque, documenté), agent-creator (« zapier »), audio-metadata (transcription → ASR), prompt-engineering (« nouveau skill » → skill-creator), script-reviewer (« nouveau script » → script-creator), script-mon-ecosysteme-infrastructure (« installation complète » → PM-INSTALL), skills-inventory (« clawhub » → hub)… — chaque veto tracé avec sa doctrine ; count mesuré (pas de pré-écriture du « 13 »).
- **T2.3** Révisions REFUTE version-management (2 cas documentés : création de page/accueil et dashboard → should_trigger false) + bump **v1.2.1** + journaux KO-L004.

### G3 — Option B : voie L sémantique à cache déterministe — 3 tâches
- **T3.1** Écriture de `scripts/voie-l-semantique.py` : cache-first, mode sériel, retry/backoff, suppression du fichier `-o` avant appel (CLI exit 0 même en erreur), description SKILL.md COMPLÈTE au juge (leçon Task 30 : jamais tronquer — question de ROUTAGE, pas d'appartenance), température 0, verdict parsé strict.
- **T3.2** Seed du cache avec les **verdicts figés de la discussion** (réutilisables — zéro re-appel pour ces cas) : jd→true, ai→true (convention token de tâche), cahier→false, gen-plan « (stp) »→false, refactor-guard « God Class »→true, trio iphone résiduels→false (doctrine d'époque), version-management ×3 (看看/恢复/切回)→true (description-complète), + tout cas couvert par un verdict CONFIRME tracé.
- **T3.3** Cas non couverts par la discussion (corpus évolué : vue-upload v1.2.0, cas nouveaux) → appels z-ai CLI réels (sériel, blindés 429), figement R4, traçabilité dans l'entrée du cache.

### G4 — Option C + cascade + publication — 4 tâches
- **T4.1** Re-replay ×2 idempotence byte-identique (sha256) + verdict résiduel documenté (répartition mesurée : voie-m / veto-exclusif / voie-l-cache).
- **T4.2** Cascade KO-L004 : KB, README/journaux, sync miroir hôte (dépôt = source R4), re-replay hôte ×2 ; arbitres verts : verify-cross 100 %, integrity 82/82, interactions (PASS, réserve héritée acceptée), doublons 0.
- **T4.3** Rapport `download/rapport-campagne-abc-triggers.md` + commit dépôt.
- **T4.4** Push (le GO de la directive couvre la publication des travaux de la session ; garde : push seulement si les 4 arbitres sont verts, sinon commit local + rapport au propriétaire) ; rappel révocation PAT.

## Answer key (statuts dérivés de l'état vérifiable — remplis à l'exécution)

| ID | Tâche | Critère de succès mécanique | Statut |
|----|-------|------------------------------|--------|
| D001 | T1.1/T1.2 | `ls-remote` = HEAD local, 0 occurrence du PAT dans le dépôt | à mesurer |
| D002 | T2.1 | arbitre compile, veto appliqué avant scoring (test unitaire sur cas iphone17) | à mesurer |
| D003 | T2.2/T2.3 | vetos appliqués count=N mesuré ; version-management v1.2.1 ; verify-cross 100 % | à mesurer |
| D004 | T3.1/T3.2/T3.3 | cache figé complet (0 INDECIS), verdicts figés discussion réutilisés sans re-appel | à mesurer |
| D005 | T4.1 | replay ×2 sha256 identique, verdict global mesuré | à mesurer |
| D006 | T4.2 | 4 arbitres verts dépôt + hôte, sync miroir ×2 idempotent | à mesurer |
| D007 | T4.3/T4.4 | rapport + commits + push vérifié ls-remote | à mesurer |

## Réserves transparentes
- Les 13 vetos/19 verdicts exacts de Task 30 ne sont pas intégralement recoverables (instrumentation non commitée) — reconstruction doctrinale traçable depuis l'arbitrage documenté, chiffres re-mesurés.
- PAT éphémère : à révoquer par le propriétaire après la session (rotation G1).
