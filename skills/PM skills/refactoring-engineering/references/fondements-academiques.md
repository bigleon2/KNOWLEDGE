# Fondements académiques et veille — refactoring-engineering (n°55)

> Sources de la recherche web approfondie (Task 7, session web-b4d7dd19, 2026-10-12 — subagent de recherche, ~17 requêtes ; seules les sources effectivement retournées sont citées — R3).

## Transformations préservant le comportement (D1/D3)
- **Définition canonique (Fowler)** : « série de petites transformations préservant le comportement observable », pas-à-pas avec tests après chaque changement — https://refactoring.com ; https://martinfowler.com ; https://agilealliance.org ; https://refactoring.guru
- **Preparatory refactoring (Fowler/Beck)** : « make the change easy, then make the easy change » — https://martinfowler.com/articles/preparatory-refactoring-example.html
- **Opportunistic refactoring / règle du camping** : laisser la cible en meilleur état qu'on l'a trouvée — https://martinfowler.com/bliki/OpportunisticRefactoring.html
- **Katas (Bache — Gilded Rose, Samman method)** : transformations sans réécriture, practice en environnement sûr — https://github.com/emilybache/GildedRose-Refactoring-Kata ; https://se-radio.net ; https://understandlegacycode.com

## Sécurisation préalable (D2 — golden master)
- **Characterization tests (Feathers)** : décrire le comportement ACTUEL avant toute transformation — https://en.wikipedia.org/wiki/Characterization_test ; https://michaelfeathers.silvrback.com ; https://chrismelinn.wordpress.com ; https://understandlegacycode.com ; https://khalilstemmler.com/articles/legacy-code
- Dans l'écosystème : les pré-checks verrouillés (arbitres verts AVANT) = golden master documentaire.

## Migrations progressives (D4)
- **Strangler Fig** : remplacement graduel, zéro downtime — https://www.thoughtworks.com ; https://www.gocodeo.com ; https://hackernoon.com
- **Branch by Abstraction (Humble/Fowler)** : « le code fonctionne à tout instant pendant la restructuration » — https://continuousdelivery.com ; https://martinfowler.com ; https://www.stevesmith.tech
- **Feature flags / commutation** : complément du branch by abstraction — https://www.davefarley.net ; méfaits des branches longues — https://thinkinglabs.io

## Garde-fous et post-conditions (§1.4)
- **Fitness functions automatisées et continues** comme arbitres mécaniques de post-condition — https://ebrary.net ; https://www.thoughtworks.com (radar 2017)
- **Anti-auto-certification** : les revues (humaines ou LLM) ratent des régressions de refactoring — https://www.janeasystems.com (« The 40 % Problem ») → double commande : arbitres + évaluateur indépendant (refactoring-test)
- **Priorisation par intérêt** : traiter la dette « comme une scène de crime » (fréquence de changement, ROI) — https://refactoring.fm ; https://se-radio.net
- **Déploiement progressif aligné sur le blast radius** (consommé depuis refactoring-test M3) — https://www.gocodeo.com ; https://www.nofire.ai/glossary/blast-radius-analysis

## Risques documentés (pièges)
1. Se fier à la revue seule — janeasystems.com.
2. Refactoring en branche longue — continuousdelivery.com ; thinkinglabs.io.
3. Mélanger refactoring et changement de comportement dans une même opération — martinfowler.com (préparatory).
4. Réécrire au lieu de refactorer — emilybache/GildedRose-Refactoring-Kata.
5. Transformer du legacy sans filet (characterization tests absents) — en.wikipedia.org/wiki/Characterization_test.
6. Mesurer la dette uniquement en statique (ignorer churn/hotspots) — guidefari.com ; usenix.org.
7. Confondre principal et intérêt — devopedia.org (SQALE).
8. Ignorer la dérive induite par l'IA (duplication ×4/×8) — gitclear.com ; tembo.io.
9. Modifier sans quantifier le blast radius au préalable — nofire.ai ; PMC3984771.
10. Laisser des agents modifier un système vivant sans garde-fous mécaniques — adversa.ai ; securitylab.github.com.

## Limites documentées
- Pas de source dédiée retournée pour canary/shadow deployment en isolation (l'échelle de déploiement de l'écosystème reste fondée sur les stratégies strangler/branch-by-abstraction + arbitres).
