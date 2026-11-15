# Plan — Task 96 : ré-armage cron cadence autonome (3 ticks/jour — limite plateforme) + tri des pendances R5 (écart cas 6 voie M hors cadence · proposition future check N1 périmètre KB)

**Directive propriétaire** trace `1a1df19ddd9c60c1` (reformulation `1a1df1c1f2ff1875` « continue mais en discutant toujours avec moi en français » — règle d'or n°6 confirmée PERMANENTE) — gen-plan mode NULL v3.43.0 (décisions données, exécution directe sans portes de confirmation)
**Référentiel à l'ouverture** : HEAD `2d37797` (Task 95 CLOSE, poussé — 0 unpushed, arbre propre) · SHARED v1.7.39 · PM-INSTALL v1.9.16 · gen-plan v3.43.0 · worklog dernière entrée **suite 135** (parité hôte/dépôt 2 283 lignes) · **0 PAT frais ce tour** (ancien jeton 19 expositions — à révoquer côté propriétaire, jamais réutilisé ; KO-L009)

---

## Enquête E1-E2 (exécutée avant plan — read before planning)

- **Cron 516921** (API plateforme interrogée directement) : ENREGISTRÉ mais **INACTIF** — status -1, invisible à `list` (0 job actif sur la plateforme), 5 exécutions du 2026-11-09 13:50→23:50, désactivé le 2026-11-10 00:29:56, **0 tick depuis** — le ré-armage était la pendance « décision propriétaire » (suites 126/130/131/135) : **décision DONNÉE ce tour**. Mission d'origine (Task 84) : réinstall d'abord (voie directe `eco_install_pipeline.py`) puis continue $FACON autonome (source de vérité = plan le plus récent download/ + worklog.md) + $FACON2 avant commit + PUSH par délégation PAT (KO-L009/E15).
- **Écart cas 6 voie M** : écart structurel consigné Task 86 (agent-engineering, Description Optimization A10/A14) — re-mesure 6/7, le cas 6 sur voie M reste en faux positif STRUCTUREL : radical « agent » ∈ strong arbitre V6 (le mot appartient au domaine, incurable par re-formulation de la description) ; re-mesures stables Task 86/90 (6/7) ; seul remède identifié = **mission dédiée arbitre V6** (pondération/lexique), jamais lancée ; statut antérieur « hors cadence » — le propriétaire CONFIRME « hors cadence ».
- **Check N1 skill** (`check-tool-routing.py` L22-27) : la couche N1 exige un frontmatter conforme skill-creator §2 (name/version/category/language/tags/description, semver) de tout artefact de type « skill » modifié ; ~65 skills miroirs plateforme (ASR, LLM, TTS, VLM, agent-browser…) pré-existants à HEAD n'ont pas ce frontmatter (preuve git show, Task 95 G4) → échec N1 documenté en certification Task 95 (5/6) quand la propagation de cascade touche ces fichiers ; **proposition future** (suite 134) : calibrer le périmètre du check N1 sur la **KB** (registre = source de vérité) — le propriétaire CONFIRME le statut « proposition future ».
- **Routage (N2, table SHARED §3.1/§7)** : éléments touchés ce tour = plan [gen-plan] + worklog [gen-plan] + job cron [action plateforme directe — primitive API cron, aucun skill dédié, consigné] ; **aucun skill/script/agent/registre KB modifié**.

## G1 — Ré-armage de la cadence autonome (remplacement du job inactif 516921)

- **AMENDEMENT en exécution (adaptation autonome règle d'or n°1)** : la 1re création en fixed_rate 7200 (job 531670) a été REFUSÉE par la plateforme (« estimated 12 daily executions exceeds limit 3, excess triggers will be ignored » — la cadence 2 h n'est plus honorée) ; jamais de re-jeu à l'identique (règle d'or n°5) : jobs 531670 + 516921 supprimés, recréation en **cron déterministe 3×/jour** — nom « Cadence autonome écosystème — réinstall + continue $FACON (Task 84, ré-armée Task 96 — 3 ticks/jour) », schedule `0 0 7,15,23 * * ?` tz Europe/Paris (3 exécutions/jour = limite plateforme, heures fixes prévisibles), payload agentTurn, priorité 5, routage auto-injecté vers la présente discussion — **nouvel ID : 531671 (status 1 actif, prochain tick 15:00 CET)**.
- **Message rafraîchi** (l'ancien citait la file re-curation ÉTEINTE depuis Task 85 et un littéral de compte de certification périmé) : réinstall d'abord (voie directe, certification SHA-256 complète, 0 divergence — littéral « 54/54+ » retiré, anti-dérive classe S4-1 ; garde R2 0 rétrogradation ; dépôt propre) · source de vérité (plan le plus récent download/ + worklog.md) · **pendances au 2026-11-15** : PMs famille §0 L2 [rafraîchis automatiquement aux prochaines montées] · écart cas 6 voie M [HORS CADENCE — mission arbitre V6 à ne PAS lancer sans décision] · proposition future check N1 périmètre KB [FUTURE — à ne PAS exécuter sans décision] · rotation PAT [propriétaire] · $FACON2 avant tout commit · PUSH UNIQUEMENT avec un PAT frais fourni dans la discussion (KO-L009 zéro-persistance, E15 consignation), sinon commit local SANS PUSH + pendance · **résumés TOUJOURS en français** (règle d'or n°6).
- Suppression de l'ancien enregistrement 516921 (inactif — mission intégralement conservée au worklog, KO-L003 zéro perte ; la plateforme en garde un tombstone status -1) + vérification `get` du nouveau job + **consignation du nouvel ID** (le propriétaire référençait le job par l'ancien numéro).

## G2 — Écart cas 6 voie M : maintien HORS CADENCE consigné

- **Aucune exécution** (pas de mission arbitre V6, pas de modification de skill/agent/arbitre) — le maintien « hors cadence » confirmé par le propriétaire (trace 1a1df19ddd9c60c1) est consigné au plan + worklog avec contexte décision-ready : écart structurel stable (radical « agent » ∈ strong arbitre V6, re-mesures 6/7 Task 86/90), remède = mission dédiée arbitre V6 à lancer sur décision propriétaire ultérieure.

## G3 — Proposition future « check N1 skill sur périmètre KB » : inscription

- Formulation consignée : dériver le périmètre du check N1 « skill » de `check-tool-routing.py` de la **KB** (registre des skills de l'écosystème = source de vérité) au lieu du scan du répertoire `skills/` — les ~65 skills miroirs plateforme pré-existants (sans frontmatter skill-creator) sortiraient du périmètre N1 profond (exemption typée ou check allégé) ; bénéfice : certification reproductible, indépendante du périmètre de diffusion des cascades de propagation ; statut **FUTURE** — aucune exécution sans décision propriétaire.

## G4 — Miroirs + worklog + arbitres + commit local SANS PUSH

- Plan → download/ hôte + miroir dépôt ; worklog suites 136-137 hôte + dépôt (parité byte) ; $FACON2 avant commit : arbitres ×6 AU VERT (verify-cross ×2 modes · verify-correct-work · integrity · interactions · tool-routing) ; **COMMIT LOCAL « Task 96 CLOSE » SANS PUSH** (0 PAT frais — KO-L009 ; E15 : 0 nouvelle exposition) ; pendance PUSH [propriétaire — PAT frais post-révocation] ; résumé concis au propriétaire en français.

---

## Answer key (preuves vérifiables par décision)

| ID | Décision | Preuve mécanique |
|----|----------|------------------|
| D001 | Ré-armage = job remplaçant ACTIF (cadence honorée 3×/jour, mission conservée, message rafraîchi) | cron `get` **531671** : rc 0, status 1, cron `0 0 7,15,23 * * ?` Europe/Paris, prochain tick planifié |
| D002 | Ancien 516921 retiré SANS perte (KO-L003) | `get` 516921 → tombstone inactif (supprimé) + mission citée au worklog suites 136-137 + toutes les clauses reprises dans le nouveau message |
| D003 | Message rafraîchi : file re-curation éteinte retirée, littéral « 54/54+ » retiré, pendances 2026-11-15, garde « PAT frais uniquement », cadence 3×/jour explicite, français permanent (règle d'or n°6) | texte du job (`get`) + deltas consignés suite 137 |
| D004 | Écart cas 6 voie M maintenu HORS CADENCE — aucune exécution | plan G2 + worklog suite 137 ; diff git limité aux .md (0 skill/agent/arbitre modifié) |
| D005 | Proposition future check N1 inscrite (périmètre KB = source de vérité) — aucune exécution | plan G3 + worklog suite 137 ; `check-tool-routing.py` NON modifié (diff git) |
| D006 | Parité hôte/dépôt : plan ×2 + worklog suites 136-137 identiques | diff worklogs vide + plan présent dans les deux download/ |
| D007 | Arbitres $FACON2 avant commit : AU VERT | certification-complete.py (5 arbitres canoniques : verify-cross ×2 modes · verify-correct-work · integrity · interactions) + check-tool-routing.py — sorties consignées suite 137 |
| D008 | Commit local SANS PUSH + E15 0 exposition + résumé français | `git log -1` « Task 96 CLOSE » + origin..HEAD = 1 commit en attente + réponse finale au propriétaire |

*Plan Task 96 — gen-plan mode NULL v3.43.0, enquête E1-E2 terminée (API cron interrogée · worklog suites 126-135 croisées · code N1 check-tool-routing.py lu · git vérifié propre · worklogs hôte/dépôt en parité 2 283 lignes).*
