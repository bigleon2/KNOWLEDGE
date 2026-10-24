# Rapport — Publication GO + Campagne A/B/C de résorption des dérives triggers

Directive propriétaire (gen-plan prompt, session web-f90062ce, 2026-10-24) : « GO (PAT éphémère) + armer la campagne A/B/C de résorption des 16 dérives triggers (verdicts figés de la discussion réutilisables) ». gen-plan v3.26.0 — plan : `download/plan-campagne-abc-publication-go.md`.

## 1. Publication GO (G1 — D001 PASS)

- Push `a076086..45ef2ba main->main` (3 commits en attente : H1-P2 rejeu sandbox 84, gen-plan v3.26.0, livrables directive v3.26.0) — vérifié `ls-remote` : remote HEAD = local HEAD = **45ef2ba**.
- Anti-persistance PAT : le jeton n'a été utilisé qu'en argument de commande (jamais écrit dans un fichier du dépôt, des livrables ou des logs persistés). **Rappel : révoquer le PAT post-session (protocole G1).**

## 2. Constat mesuré avant campagne (règle d'or n°5)

Re-joue frais de l'arbitre V6 : **104 skills, 85 OK, 19 en dérive (3 iphone + 16 autres), 33 cas échoués** — la « 16 dérives » du propriétaire désigne les 16 autres skills ; périmètre canonique Task 30 = 19. Instrumentation Task 30 de la vérité source (vetos, cache, arbitre V6.1) jamais commitée (D005) — reconstruction doctrinale depuis l'archive `scripts/discussion-64c90144.txt` (+ raw : arbitrage Task 25 §4 complet).

## 3. Option A — vetos exclusifs (D003 PASS)

Champ optionnel `exclusifs` par cas dans trigger_evals.json ; l'arbitre **V6.1** applique le veto AVANT le scoring (doctrine « périmètre » des SKILL.md encodée comme donnée). Script persisté idempotent `scripts/task30-vetos-exclusifs.py` (re-jeu ×2 no-op) — **14 vetos / 11 corpus** mesurés :

| Corpus | Termes réservés | Doctrine |
|--------|-----------------|----------|
| iphone17 | iphone 18 | périmètre d'époque (arbitrage Task 25 D1 CONFIRME) |
| iphone18 | iphone 17 | périmètre d'époque (D2) |
| iphone19 | iphone 18 | génération confirmée courante = iphone18 (D3) |
| agent-creator | zapier | automatisation SaaS tierce |
| audio-metadata | transcris | transcription = ASR |
| prompt-engineering | nouveau skill | skill-creator |
| script-reviewer | nouveau script | script-creator |
| script-mon-ecosysteme-infrastructure | installation complète | PM-INSTALL |
| skills-inventory | clawhub · et installe | skill-finder-cn |
| pdf-llm | produis un rapport · génère un nouveau pdf · fusionne | skill pdf |
| vue-upload | vérifie le travail | script-reviewer/correct-work |

0 bump semver (champ doctrinal additif, précédent Task 27-A) ; verify-cross 100 % (champ additionnel toléré).

## 4. Option B — voie L sémantique à cache déterministe (D004 PASS)

- `scripts/voie-l-semantique.py` : cache-first, mode sériel, retry/backoff, fichier `-o` purgé avant appel, description SKILL.md **complète** au juge (leçon Task 30 : jamais tronquer la doctrine de périmètre), question de **routage** (jamais d'appartenance), verdict parsé strict.
- Cache R4 `scripts/voie-l-cache.json` — **19 verdicts figés** : 16 seedés depuis la discussion sans re-appel (jd→true, ai→true — convention token de tâche ; cahier→false ; trio iphone19→false doctrine d'époque ; gen-plan « stp »→false ; refactor-guard « God Class »→true ; agent-browser ×3 ; agent-prompt-engineering ×2 ; version-management zh ×3) + 3 arbitrages LLM réels (sériel, 0 INDECIS) : version-management 个人主页→true, 仪表盘→true (doctrine-conformes), vue-upload DOCX→**false**.

## 5. Option C — re-replay ×2 + verdict résiduel (D005 PASS)

- **Dépôt : 103/104 skills, ×2 byte-identique (sha256 a75a1c0f)** · **Hôte : 42/43, ×2 byte-identique (sha256 64dfcd40)** — miroir cohérent.
- Sources mesurées (dépôt) : **773 voie-m · 14 veto-exclusif · 18 voie-l-cache · 1 voie-l-cache-desaccord**. Voie M seule conservée à titre informatif (FAIL informatif, transparence intacte — la voie M seule reste en échec sur 19 skills : leçon structurelle, mots-clés non discriminants).
- **Résiduel documenté (Option C statu quo assumé)** : vue-upload « Je ne peux pas télécharger le document DOCX… ouvre-moi un accès » (attendu true) — le juge répond false y compris après re-arbitrage ancré dans la clause doctrine (« Répond à la douleur… ») ; verdict mesuré figé sans surcharge. Recommandation future : affiner la doctrine de déclenchement de la description vue-upload.

## 6. Non-événement documenté (anti-aspirant — règle d'or n°5)

Deux révisions REFUTE version-management avaient été déduites de la mention « (+ 2 révisions REFUTE, version-management v1.2.1) » de la discussion. Après re-lecture du référentiel : la description SKILL.md inclut **explicitement** « toute demande de création de page web ou d'interface… tableau de bord / dashboard » dans le périmètre → les 2 cas (个人主页， 仪表盘) restent attendu=true, confirmé par la voie L à description complète (true/true). Révisions annulées, bump 1.2.1 revert (v1.2.0 conservé, integrity re-verte). Les « 2 REFUTE » exactes de Task 30 ne sont pas reconstructibles (cache non commité) — hypothèse écartée faute de preuve, consigné plutôt que forcé.

## 7. Cascades KO-L004 + arbitres (D006 PASS)

- KB `skills/KNOWLEDGE.md` : entrée **Task 30-ABC** (journal complète, non-événement documenté) ; `@historique/historique-autres-elements.md` : section **§6bis** créée (journal des campagnes trigger_evals, convention Task 30) ; archive rescellée (round-trip vérifié).
- **Dépôt** : verify-cross 100 % · integrity **82/82 ×2** · interactions 51 PASS / 1 WARN hérité B1 / 0 FAIL (PASS AVEC RÉSERVES) · doublons 0.
- **Hôte** (sync miroir repo→hôte, archive incluse) : verify-cross 100 % · integrity 82/82 · interactions PASS AVEC RÉSERVES · doublons 0 · replay ×2 byte-identique.

## 8. Answer key finale

| ID | Critère | Verdict |
|----|---------|---------|
| D001 | push vérifié ls-remote, 0 persistance PAT | **PASS** (45ef2ba) |
| D002 | arbitre V6.1 compile, veto avant scoring | **PASS** (veto testé sur cas iphone17) |
| D003 | vetos appliqués 14/11 corpus, idempotent ×2 | **PASS** |
| D004 | cache 19 verdicts figés, 16 réutilisés sans re-appel | **PASS** |
| D005 | replay ×2 byte-identique, verdict mesuré | **PASS** (a75a1c0f — 103/104) |
| D006 | 4 arbitres verts dépôt + hôte, sync ×2 idempotent | **PASS** (WARN B1 hérité) |
| D007 | rapport + commit + push | **PASS** (commit campagne) |

**Réserves transparentes** : 1 résiduel assumé (vue-upload, divergence juge-corpus documentée — Option C) ; replay verdict global FAIL informatif par ce résiduel unique ; les 13 vetos/19 verdicts exacts de Task 30 non reconstructibles → reconstruction doctrinale traçable, chiffres re-mesurés (14 vetos/19 cache — écho fidèle des ordres de grandeur documentés).
