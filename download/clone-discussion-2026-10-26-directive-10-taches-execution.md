# Clone de discussion — 2026-10-26 — Directive 10 tâches : exécution P2-P7 (session web-eb6c8580, continuation)

> Clone auto-suffisant (clone-chat v2.0.1 — template §0-§5, 7+1 étapes). Sert à reprendre la mission sans le contexte de la discussion d'origine.

## §0 — Métadonnées et héritage

- **Session** : web-eb6c8580 (continuation — la session d'origine a couvert Task 1-5 : installation, certification, audit ; Task 6 : plan task3 + P0 ; P1 poussée b2d4e5b)
- **Lignée** : 3e clone du profil local (précédents : clone 2026-10-25 installation-ecosysteme-plan-audit ; clone 2026-10-25 execution-audit)
- **Directive propriétaire d'origine** : installer l'écosystème via PM-INSTALL (fichier GitHub b75a620) → gen-plan fraîchement installé → plan d'actions → [clone-chat ; vérifie $eco-leon (alias-eco) ; correct-work ; P2 francisation + « Prompt Maitre » par skill dans skills/PM skills/ ; P3-P7 ; correct-work ; clone-chat] + directive PAT GitHub (push des modifications)
- **Étapes 3.5 Context Drift** : 4 drifts tracés — (1) reset plateforme inter-sessions (CORRECTION : restauration PM-INSTALL §3.4 + certification 6/6) ; (2) PAT tronqué au transfert de contexte (ENRICHISSEMENT : commits locaux durables, push différé) ; (3) quota API 429 prolongé (ENRICHISSEMENT : contournement backoff + matérialisation grille v3.28.1) ; (4) directive P2 affinée par le propriétaire (CORRECTION : « ne les sauvegarder que dans skills/PM skills/ » — respectée)

## §1 — Contexte et décisions (résumé auto-suffisant)

- **Architecture double-piste (D002)** : ENVIRONNEMENT = écosystème local certifié v3.23.1 fork (méthode, arbitres, certification 6/6) ; CIBLE = worktree publication `.staging/KNOWLEDGE-publish` (branche `publication/p0-session-web-eb6c8580`, lignée distante).
- **Reprise après wipe plateforme** : restauration MODE CLONE depuis tarball b75a620 (`bash scripts/install-ecosysteme-local.sh <tarball>`) + `rsync @historique` + `python3 scripts/task-restore-phaseB.py` (corrections (e)/(g)) + alignements §0 (alias-eco/cahier-des-charges → v1.7.7) + dessin-technique v1.1.1 → certification 6/6 PASS AVEC RÉSERVES (résidu : avertissement worklog B1 documenté).
- **$eco-leon vérifié** : skills/alias-eco installée ; `python3 skills/alias-eco/scripts/alias-manager.py --add ECO-LEON "mon écosystème personnel"` puis `--resolve` → résolution OK, idempotent ×2.
- **Décisions clés P2-P7** : D001 additions-only (0 fichier supprimé, vérifié b2d4e5b..HEAD) ; D008 lots résumables (commit + worklog par phase) ; D010 marqueurs d'exclusion 106/106 (0 SKILL.md généré, 0 entrée KB — certification re-jeu PASS) ; D011 environnement local non re-projeté en session.

## §2 — Artefacts produits (vérifiables sur disque)

- **Worktree publication** (5 commits en attente de push : a9a2427 P2, 0453a87 P3, c5c1832 P4, b792f4f journal, 8c6e32a P6) :
  - `skills/gen-plan/SKILL.md` v3.28.1 (+ §4 recalibré + journal §5.6) ; `references/grille-token.md` (coefficients + rows 12-13) ; PM v3.28.1 (1479 L) ; PM v3.28.0 archivé @historique R4 (SHA df8d43c1…) ; PM-INSTALL v1.8.7 (§2ter/§A.3) ; SHARED (révision §6.1) ; KB gen-plan v3.28.1
  - `skills/PM skills/` : 106 dossiers + README (marqueur D010) — re-génération idempotente par `scripts/p2-prompt-maitre.py`
  - `scripts/p2-franciser.py`, `p2-segments.py`, `p2-prompt-maitre.py`, `p2-sceau-avant.json`, états JSON
  - `download/rapport-arbitrage-4-propositions.md`, `download/rapport-correct-work-projet-directive-2026-10-26.md`, `download/rapport-final-directive-10-taches-2026-10-26.md`
- **Profil local** : scripts de session `/home/z/my-project/scripts/p2-*.py|json|txt|sh` (états idempotents — reprise francisation) ; certification locale 6/6 (scripts/certification-report.json)

## §3 — État de sortie et reprise mécanique

1. **Push** (dès PAT frais du propriétaire) : `cd /home/z/my-project/.staging/KNOWLEDGE-publish && git push https://<PAT>@github.com/bigleon2/KNOWLEDGE.git HEAD:refs/heads/main` — 5 commits, fast-forward attendu (base b2d4e5b = tip distant vérifié par ls-remote en début de continuation).
2. **Francisation** (dès quota API z-ai rétabli) : boucler `bash /home/z/my-project/scripts/p2-cycle.sh` jusqu'à « 0 restant » (états idempotents, les fichiers finis sont SKIP) → `python3 /home/z/my-project/scripts/p2-prompt-maitre.py` (re-génération PM des sources modifiées) → commit + push.
3. **Arbitre reporté** : implémenter `scripts/check_plan_protocol.py` depuis la spécification C6 (5 points — download/rapport-arbitrage-4-propositions.md) — décision propriétaire.
4. **Re-projection miroir hôte** (décision propriétaire, section 4 du rapport final).

## §4 — Leçons session (propositions knowledge-observer)

- L-P2-a : périmètre de lecture des scripts de génération à vérifier (les copies « PM skills » comptaient dans le scan de rattrapage).
- L-P2-b : le NO-OP d'un générateur idempotent peut masquer un recalibrage croisé non exécuté — vérifier les PORTS, pas seulement la famille.
- L-P2-c : sonder le quota API AVANT de planifier une phase batch.
- L-P2-d (héritée audit) : la contingence « incidents multi-environnements ×1,5 » à ajouter à la grille (row 14 — prochaine montée gen-plan).

## §5 — Sceaux et conformité

- Certification locale : 6/6 PASS AVEC RÉSERVES (verify-cross 99/99 ×2, verify-correct-work 16/16, integrity 70/70, interactions 47/48, tool-routing 6/6)
- Distant : generer-pm --check 4/4 COHERENT ; check-triggers-replay 104/104 ; additivité 0 suppression
- Anti-persistance PAT : 5 zones VERT (0 valeur réelle dans les 8 commits de session — motifs documentaires conformes convention 2165a28)
- Rappels propriétaire : révoquer le PAT 11AJSTJXQ0… · prévoir révocabilité à chaque transfert
