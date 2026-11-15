# Note — Explication des 3 propositions S4 en attente (Task 94)

**Directive propriétaire** trace `1a1deb52b30fe8a9` — « PUSH des commits avec ma clé [PAT fourni] + explique-moi chacune des 3 propositions S4 en attente »
**Référentiel** : HEAD `32706b4` (Task 93 CLOSE — poussé ce tour, 0 unpushed) · SHARED v1.7.38 · gen-plan v3.43.0 · PM-INSTALL v1.9.15
**Origine des propositions** : Task 91 G2 (analyse $FACON — verdict « NON, RIEN À OPTIMISER MAINTENANT »), findings R2/R3/R4 classés S4, consignés worklog suites 116/121/126/127/130.
**Faits re-vérifiés mécaniquement ce tour** (2026-11-15, à HEAD `32706b4`) — chaque finding demeure vivant.

---

## Rappel — que signifie « S4 » ?

Échelle de sévérité de l'analyse Task 91 G2 : S1 (bloquant) · S2 (sécurité — action propriétaire) · S3 (observation — décision propriétaire) · **S4 (cosmétique / informationnel — AUCUNE incidence comportementale)**. Les 3 propositions sont S4 : elles ne modifient ni le comportement de gen-plan ni son contrat, et portent sur des outils du dépôt (générateur ULTRA, générateur PM, pratique de câblage) — pas sur le skill gen-plan lui-même. C'est pourquoi elles sont **en attente** : les exécuter maintenant n'apporterait aucune amélioration fonctionnelle (et monter une version sans substance violerait la semver — Règle Zéro n°2).

---

## Proposition S4-1 (finding R2) — Recalibrer ou dynamiser le littéral ULTRA « protocole-test v1.2.1 »

**Le fait (vérifié ce tour)** : `scripts/gen-ultra-maitre.py` ligne 56 contient le littéral statique « harnais protocole-test.py **v1.2.1** », alors que le harnais réel `skills/re-curation/scripts/protocole-test.py` est à **v1.2.2** (docstring ligne 2 — monté en v1.2.2 par la Task 82, le 2026-11-09).

**Pourquoi c'est un problème (cosmétique)** : l'ULTRA (table agent-engineering, 13 voies) est régénéré depuis ce générateur — chaque régénération propage le littéral périmé dans la documentation de la voie re-curation. Aucune incidence comportementale : l'ULTRA n'est pas épinglé par l'arbitre integrity, et le littéral ne pilote aucune logique d'exécution.

**La proposition** : deux options —
1. *Recalibrer* : édition chirurgicale d'une ligne (v1.2.1 → v1.2.2), coût minime ;
2. *Dynamiser* (recommandé, aligné KO-L003) : le générateur lit la version réelle du harnais au moment de la génération au lieu d'un littéral codé en dur — élimine définitivement la récidive (à chaque montée du harnais, sinon).

**Coût / bénéfice** : ~1 ligne (option 1) ou petite fonction (option 2) + re-génération ULTRA. Bénéfice : hygiène documentaire perpétuelle.

---

## Proposition S4-2 (finding R3) — Étendre les substitutions du générateur PM au bloc §0 de PM-INSTALL

**Le fait (vérifié ce tour)** : `skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` (v1.9.15, généré le 2026-11-15 par la Task 92) embarque encore, ligne 13, l'en-tête « ⚙️ CONTEXTE SYSTÈME (Extrait SHARED **v1.7.17**) » — alors que le SHARED vivant (`skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md`, ligne 3) est à **v1.7.38**. Soit 21 versions de retard.

**La cause racine** : `scripts/generer-pm-skill.py` (voie sanctifiée KO-L004) applique ses substitutions verrouillées (§2ter / §A.3 — références de versions des PMs) mais **ne touche pas au bloc CONTEXTE SYSTÈME** lors des recalibrages : le §0 du PM-INSTALL reste figé à la version du jour où le bloc a été rédigé (v1.7.17, le 2026-11-01).

**Pourquoi c'est un problème (informationnel)** : les formes **exécutées** sont saines — le §0 propagé aux 72 skills / 210+ scripts / agents est frais (v1.7.38, propagation Task 93), et le SHARED vivant fait foi. Le stale vit uniquement dans une **spécification documentaire** : le PM-INSTALL. MAIS ce PM est « l'UNIQUE source d'installation de l'écosystème » (son propre en-tête) — toute installation future via la voie bootstrap corpus-seul embarquerait un Contexte Système périmé de 21 versions.

**La proposition** : étendre le générateur pour que chaque montée remplacre aussi l'en-tête de version du bloc §0 (et idéalement le contenu du bloc §0 depuis le SHARED vivant) — extinction définitive de cette classe de drift, au lieu de le re-figer à la main à chaque fois.

**Coût / bénéfice** : modéré (extension du générateur + idempotence ×2 + re-génération PM-INSTALL + re-scellage archive). Bénéfice : cohérence perpétuelle de la source unique d'installation.

---

## Proposition S4-3 (finding R4) — Câblage R2-CACHE exhaustif des graders fréquents (valeur faible)

**Le fait (vérifié ce tour)** : `scripts/cache-verdicts.py` existe et n'est référencé que par 4 scripts consommateurs (`task71-g3-cascade.py`, `task71-tests-chronologiques.py`, `task73-campagne-tests.py`, `task84-campagne-tests.py`, + traces JSON des deltas) — le « câblage exhaustif des graders fréquents » suggéré par la Task 71 (F-71-4) n'a jamais été exécuté en tâche dédiée.

**Pourquoi c'est un problème (marginal)** : les arbitres réels sont mesurés **sub-seconde** (integrity 0,045 s · verify-cross 0,03 s · interactions 0,146 s). Le gain spectaculaire de la démo Task 71 (440×) portait sur un cas isolé, pas sur les arbitres de certification. Et le principe écosystème demeure : « un verdict figé n'est JAMAIS une preuve en soi » — l'exécution réelle reste la norme de certification ; câbler le cache dans les arbitrages de certification affaiblirait la preuve.

**La proposition** : soit **classer NON-PERTINENT** (recommandé — valeur faible, et risque sémantique sur la certification), soit restreindre le câblage aux appels répétitifs INTRA-exécution (boucles de campagne type task84, où le même verdict est re-demandé en boucle) — jamais dans les arbitrages de certification.

**Coût / bénéfice** : tâche dédiée modérée pour un bénéfice marginal (quelques secondes par campagne).

---

## Recommandation (si le propriétaire décide d'agir)

| Priorité | Proposition | Raison |
|---|---|---|
| 1 | **S4-2 (R3)** — substitutions §0 du générateur PM | Le PM-INSTALL est la source unique d'installation : le drift documentaire y a un destin réel (installation future) |
| 2 | **S4-1 (R2)** — littéral ULTRA dynamisé | 1 ligne / petite fonction, hygiène perpétuelle (option dynamiser > recalibrer) |
| 3 | **S4-3 (R4)** — plutôt classer NON-PERTINENT | Valeur faible mesurée ; risque sémantique sur la certification |

**Statut** : les 3 demeurent des propositions futures — aucune exécution sans décision propriétaire explicite (la présente note est une EXPPLICATION, pas une exécution).

---
*Note Task 94 — explication des 3 propositions S4 (findings R2/R3/R4, Task 91 G2), faits re-vérifiés à HEAD `32706b4` le 2026-11-15. Aucune exécution — portes propriétaire respectées.*
