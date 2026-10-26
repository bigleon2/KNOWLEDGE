# Rapport correct-work Mode PROJET — Directive 10 tâches (phases P2-P5, session web-eb6c8580)

> **Mode** : PROJET (fin de chaîne, couplage gen-plan §1.5) · **Cible** : exécution des phases P2-P5 du plan task3 (directive propriétaire à 10 tâches) · **Date** : 2026-10-26
> **Plan de vérification** : `download/plan-task3-directive-10-taches-github.md` (answer key D001-D012, 16/16 ALL PASS à E8 — hook Étape 1 respecté)
> **Méthode** : 5 étapes correct-work v2.7.0 — détection, structure, interactions, cohérence, verdict

## Étape 1 — Plan de vérification

Le plan task3 (généré et validé en Task 6) fait foi. La session a traversé un **reset plateforme** (wipe partiel : corpus, gen-plan, correct-work, KB, @historique perdus) → reprise E1-RES (D009) : restauration complète depuis tarball b75a620 + archive v2.3 (MODE CLONE + corrections (e)/(g) idempotentes + alignements §0) → re-certification 6/6 PASS AVEC RÉSERVES AVANT reprise des phases. La reprise dérivée du disque a réaligné le plan sur l'état réel (aucune phase perdue : P0/P1 déjà poussées b2d4e5b).

## Étape 2 — Problèmes détectés et traitements

| # | Problème | Sévérité | Traitement |
|---|----------|----------|------------|
| 1 | Wipe plateforme inter-sessions (corpus + gen-plan + correct-work + KB + @historique absents) | S2 | CORRIGÉ — restauration PM-INSTALL §3.4 (MODE CLONE tarball + archive v2.3 + task-restore-phaseB), certification 6/6 re-vérifiée |
| 2 | dessin-technique KB v1.1.1 ↔ SKILL.md v1.0.0 (wipe des alignements) | S3 | CORRIGÉ — restauration depuis tarball (v1.1.1), integrity 70/70 |
| 3 | Marqueurs §0 plateforme stale (alias-eco v1.7.10, cahier-des-charges v1.7.8) | S3 | CORRIGÉ — alignement v1.7.7 (byte-identique corpus), interactions 47/48 |
| 4 | Écrasement de statut dans p2-franciser.py (ligne résiduelle `statut=TRADUIT` en fin de try) → TRADUIT-RESIDUEL masqués | S3 | CORRIGÉ — suppression ligne 191, statuts recomptés |
| 5 | Réponses LLM « true » sur contenus YAML (interprétation question/réponse) | S3 | CORRIGÉ — wrapper `<DOCUMENT À TRADUIRE>` + instruction anti-confirmation |
| 6 | Générateur PM : NO-OP sur corpus déjà cohérent court-circuite le recalibrage croisé (PM-INSTALL/SHARED restés à l'ancienne version) | S3 | CORRIGÉ — complétion agent (SHARED §6.1, PM-INSTALL v1.8.7 §2ter/§A.3, KB), leçon consignée au worklog distant |
| 7 | HTTP 429 récurrent (quota API z-ai) — facteur limitant de la francisation | S3 | CONTORNE — backoff 12-48 s + pause anti-rafale 45 s + throttle + tri par taille croissante + journal d'état idempotent ; reprise par cycles (matérialisée dans le coefficient « appels API en masse ×2-3 » v3.28.1) |
| 8 | Scan de rattrapage incluant les copies des dossiers « PM skills » (double compte 214→294) | S4 | CORRIGÉ — exclusion « PM skills » du scan (les copies sont re-générées depuis les sources, jamais traduites en place) |
| 9 | PAT fourni tronqué dans le contexte de session reprise → push impossible | S3 | JOURNALISÉ — commits locaux durables (anti-reset), push différé jusqu'à PAT complet ; 0 persistance du jeton (D006) |

## Étape 3 — Contrôles structurels

- Certification locale (environnement d'exécution, D007) : **6/6 PASS AVEC RÉSERVES** (verify-cross 99/99 ×2, verify-correct-work 16/16, integrity 70/70, interactions 47/48, tool-routing 6/6) — re-vérifiée post-restauration et post-phases
- Syntaxe : py_compile 7/7 sur les scripts du worktree (générateur PM, arbitres, outillage p2)
- Additivité publication (D001) : `git diff --stat b2d4e5b..HEAD` = 412 fichiers, **0 fichier supprimé** (additions + modifications de contenu francisation uniquement)
- Corpus local : 9 fichiers (CORPUS_ATTENDU), SHAs inchangés pendant P2-P5 (D011 ✓)

## Étape 4 — Interactions vérifiées

- Canal canonique : `generer-pm-skill.py --check` → **4/4 familles COHERENT** (gen-plan v3.28.1, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.8.1)
- Graphe KB distante : entrée gen-plan v3.28.1 recalibrée, bidirectionnalité préservée (Dépend de / Utilisé par inchangés — R2)
- Trigger_evals distants : check-triggers-replay **104/104 au score maximal, dérives aucune**
- Gardes D010 : dossiers « PM skills » sans SKILL.md (0 impact arbitres), sans entrée KB, marqueur d'exclusion sur 106/106 dossiers + README racine ; certification re-jeu PASS après génération

## Étape 5 — Cohérence answer key (D001-D012)

| Décision | Statut | Preuve |
|----------|--------|--------|
| D001 push additive anti-régression | ✓ | 0 suppression de fichier b2d4e5b..HEAD ; pas de force-push |
| D002 double-piste | ✓ | ENV local certifié 6/6 (exécution) + worktree lignée distante (cible) |
| D003 P0 push sauvegarde | ✓ (Task 27) | commit e98ad0d poussé avant les tâches lourdes |
| D004 correctif bug §6 OBSOLÈTE | ✓ | rapport-arbitrage-4-propositions.md (adoption distante v3.27.0 documentée) |
| D005 drifts 4/4 statutés | ✓ | CORRIGÉ/JOURNALISÉ/OBSOLÈTE non vides (rapport P4) |
| D006 hygiène PAT | ✓ (provisoire) | 0 remote URL, 0 ~/.git-credentials, 0 valeur PAT dans scripts/commits ; audit 5 zones final = P6 (ci-dessous) |
| D007 zéro-régression locale | ✓ | certification 6/6 après chaque phase lourde ; golden masters ; SHAs corpus stables |
| D008 lots résumables | ✓ | commit + worklog à chaque phase (a9a2427 P2, 0453a87 P3, c5c1832 P4, b792f4f journal) |
| D009 reprise E1-RES | ✓ | 2 reprises effectives depuis le disque (reset plateforme + troncature PAT) |
| D010 garde anti-lecture | ✓ | 106/106 marqueurs, 0 indexation KB, certification 6/6 post-P2 |
| D011 environnement non re-projeté | ✓ | SHAs @mon-ecosysteme locaux inchangés P2-P5 ; section re-projection au rapport final |
| D012 traçabilité | ✓ | worklog distant Task 28-29 + clone-chat final prévu (P7) |

## Verdict

**PASS AVEC RÉSERVES** — 5 corrections appliquées, 2 contournements documentés, 1 journalisé (PAT tronqué — push différé). Les réserves : (1) francisation P2 en état intermédiaire (214/233 fichiers avec résiduels, reprise idempotente prête — cause : quota API, externe) ; (2) push final en attente de PAT complet (commits locaux durables b2d4e5b→b792f4f). Aucun blocage de la directive : les tâches 1-9 ont chacune un livrable vérifiable.
