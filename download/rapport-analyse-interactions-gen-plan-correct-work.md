# Rapport d'analyse des interactions — gen-plan ↔ correct-work et écosystème

> **Session** : web-8a7e5653 · Task 15 / Phases P1-P2 · 2026-10-02
> **Méthode** : gen-plan v3.18.0 (pipeline E1-E15, mode PEK Hybride, profil NORMAL) · Arbitre mécanique : `scripts/analyse-interactions-gc.py` (rapport JSON : `scripts/interactions-gc-report.json`)
> **Périmètre** : les 2 skills pivot (`gen-plan` v3.18.0, `correct-work` v2.7.0) et **tous les éléments avec lesquels ils interagissent** — skills, outillage, corpus, registre KB, couche session.

---

## 1. Objet et méthode

La présente analyse répond à la directive utilisateur d'analyser les interactions entre les skills `gen-plan` et `correct-work`, ainsi qu'avec tous les éléments avec lesquels ils interagissent. Elle a été exécutée de façon **mécanique et vérifiable** : un arbitre dédié (`analyse-interactions-gc.py`, généré pour l'occasion) dérive l'intégralité du graphe de l'état réel des fichiers — frontmatters YAML des deux skills, tableaux §3 Relations, registre `KNOWLEDGE.md` (format liste, parseur deux passes calibré B4), scan inverse des 95 répertoires de skills, scan des scripts d'outillage, listing du corpus `@mon-ecosysteme/`. Aucun invariant n'est figé : chaque arête, chaque version et chaque réciprocité provient d'une lecture réelle du disque (règle KO-L003 — arbitres à invariants dynamisés). Le résultat consolidé couvre **87 arêtes d'interaction**, croisées sur cinq couches : skills, outillage Python, corpus de prompts maîtres, registre KB et couche session (worklog, plan, answer key).

Le verdict structurel est d'emblée positif : sur les arêtes internes au registre, la réciprocité est de **66 OK / 0 ABSENTE** — le graphe de relations est intégralement bidirectionnel (harmonisation B3 confirmée à l'échelle des deux pivots). Les 6 arêtes « N-A » restantes pointent hors registre pour des raisons documentées : `fullstack-dev` (skill plateforme, frontière S3 héritée), `knowledge.md` (le registre lui-même, cible méta) et `answer-key` (un pattern matériel en référence + script, pas un skill). Aucune asymétrie réelle n'a été détectée.

## 2. Le cœur : le couplage circulaire gen-plan ↔ correct-work

L'interaction centrale de l'écosystème est un **couplage circulaire assumé et protégé**. Dans un sens, `gen-plan` mobilise `correct-work` à deux niveaux : le **hook E8** (validation du plan initial, verdict PASS / PASS AVEC RÉSERVES / FAIL gate l'entrée en exécution) et le **contrôle par phase E9-E14** (hook §5.4 du SKILL : dès qu'une phase du plan se termine, `correct-work(livrables de la phase, mode=CIBLE)` s'exécute AVANT la phase suivante — PASS → continuation, RÉSERVES → réserves journalisées au worklog, FAIL → pause jusqu'à correction). Dans l'autre sens, `correct-work` mobilise `gen-plan` à son Étape 1 : en mode PROJET, la création du plan de vérification **passe obligatoirement par gen-plan** (contrat v2.7.0, directive propriétaire du 2026-10-02 — fin du mode autonome), en résolvant dynamiquement la **dernière version installée** (frontmatter de `skills/gen-plan/SKILL.md` d'abord, entrée KB ensuite).

Cette circularité est le mécanisme de qualité de l'écosystème : tout plan est vérifié avant et pendant l'exécution, et toute vérification est elle-même planifiée. Elle est **bornée par trois protections** : (1) les planchers de version asymétriques et assumés (gen-plan exige correct-work ≥ v2.4.0 pour les hooks de phase ; correct-work exige gen-plan ≥ v3.7.0 comme plancher d'intégration, avec règle §3.2-6 des « planchers gradués » documentée) ; (2) l'**ARRÊT EXPLICITE** prévu par correct-work §1.5 si gen-plan est indisponible ou corrompu (règle d'or n°1 — jamais de plan de substitution autonome) ; (3) le hook **Second Opinion** (mode AVEUGLE, v2.6.0) qui permet de rejouer une vérification sans biais de confirmation en cas de divergence persistante à l'Étape 5. Le couple forme ainsi une boucle de vérification fermée avec garde-fous anti-dégénérescence — c'est le constat F5, assumé by-design (sévérité S4, aucune action requise).

## 3. Cartographie des interactions de gen-plan (v3.18.0)

`gen-plan` est le centre gravitationnel de l'écosystème : l'analyse consolide **12 relations déclarées §3 + 5 dépendances frontmatter + 6 rôles consommateurs inverses** (skills qui déclarent dépendre de gen-plan). Le tableau ci-dessous classe chaque interaction par nature et mécanisme.

| Élément | Nature | Mécanisme (étape/section) | Réciprocité KB |
|---|---|---|---|
| **correct-work** | Invocation + hook | E1, hook E8, contrôle par phase E9-E14 (§5.4) | OK (réciproque « Utilisé par ») |
| **clone-chat** | Calibration + archivage | E4, E15 — optionnel, ≥ v2.0.0 | OK |
| **skills-inventory** | Consultation | E5 — sélection des skills (Protocole de Découverte KB §2.3) | OK |
| **prompt-engineering** | Délégation | §1.6 — optimisation des prompts complexes ; gen-plan = méthode-mère (SHARED §7) | OK |
| **context-engineering** | Mobilisation discipline | §1.6 — socle SHARED, lecture bloc par bloc, E2/E5 | OK |
| **loop-engineering** | Mobilisation discipline | §1.6 — boucle E10-E13, auto-calibration E15 | OK |
| **graph-engineering** | Mobilisation discipline | §1.6 — registre KB graphe bidirectionnel, matrice agent × skill | OK |
| **harness-engineering** | Mobilisation discipline | §1.6 — profils ressource, hooks, arbitres, worklog | OK |
| **knowledge-observer** | Invocation | E15 (§1.2bis) — observation post-session, modes M1-M2 | OK |
| **resource-monitor** | Hook d'ouverture | E1-RES (§1.2bis) — collecte G-RES, verdict → mode d'exécution | OK |
| **answer-key** (pattern) | Arbitrage | E1 (answer key obligatoire) + E7/E8 (arbitre `answer-key-checker.py`, 16 checks) | N-A (pattern, non-skill) |
| **knowledge.md** (registre) | Enrichissement | E15 (mise à jour registre) + §2.5 (intégration KB) | N-A (cible méta) |

À ces relations s'ajoutent les **consommateurs inverses** déclarés au frontmatter : `correct-work` (Étape 1, OBLIGATOIRE), `clone-chat`, `agent-creator` (≥ v3.6.0), `knowledge-observer` (≥ v3.13.0), `prompt-engineering` (contexte écosystème E1-E8) et `autonomous-agent` — ce dernier étant hors registre (voir constat F1). Enfin, `gen-plan` est **détenteur principal** des disciplines n°54 — `fleet-engineering` (§1.9 : choix du pattern et des bornes à E5/E7), `spec-driven-development` (cadrage E4, re-validation E7) et `memory-engineering` — mais cette détention n'est matérialisée **ni dans son frontmatter, ni au registre KB** (constat F4).

La couche outillage confirme la centralité : **18 scripts sur 39** de `scripts/` référencent gen-plan ou correct-work (285 occurrences cumulées), dont les 5 arbitres de certification (`verify-cross.py`, `verify-correct-work.py`, `check-ecosysteme-integrity.py`, `test-coherence-interactions.py`, `certification-complete.py`), l'arbitre d'answer key, le moniteur de ressources et l'auditeur de provenance. La couche corpus porte **14 PMs GEN-PLAN** (v3.6.1 → v3.18.0), le générateur `gen-ultra-maitre.py` (orchestrateur ULTRA régénéré à chaque montée — KO-L004) et l'archive d'intégrité `mon-ecosysteme_archive.zip` (unique voie de diffusion du corpus, décision v2.2).

## 4. Cartographie des interactions de correct-work (v2.7.0)

`correct-work` est plus compact (4 relations §3 + 3 dépendances frontmatter) mais concentre le rôle d'**arbitre universel** de l'écosystème : 6 skills déclarent l'utiliser ou en dépendre.

| Élément | Nature | Mécanisme | Réciprocité KB |
|---|---|---|---|
| **gen-plan** | Dépendance OBLIGATOIRE | Étape 1 (mode PROJET) — plan de vérification, dernière version installée, plancher ≥ v3.7.0 | OK |
| **clone-chat** | Vérification | Mode CIBLE, §3.5 Context Drift (5 types de drift) | OK |
| **fullstack-dev** | Vérification | Projets web : structure et dépendances, ≥ v1.0.0 | N-A (skill plateforme, frontière S3 documentée) |
| **skills-inventory** | Scan dynamique | Découverte des versions/dépendances via KB | OK |
| **knowledge.md** (registre) | Scan dynamique | Matrice dynamique KB, `--kb-skill`, `verify-cross.py --mode correct-work` (8 checks KB) | N-A (cible méta) |
| **loop-engineering / graph-engineering / harness-engineering** | Mobilisation | Hooks de vérification ; scan KB ; verdicts + sévérités S1-S4 | OK |

Les **consommateurs inverses** de correct-work sont la preuve de son rôle transversal : `gen-plan` (hooks par phase), `clone-chat` (validation croisée), `knowledge-observer` (validation des lessons, étape F), `script-creator` (GF-5, mode CIBLE sur les scripts produits), `script-reviewer` (sévérités S1-S4, escalade CIBLE), `audit-provenance` (GF-4, validation des artefacts corrigés) et `autonomous-agent` (hors registre). Son outillage propre : `verify-correct-work.py` (16 checks post-install), le protocole `references/verification-protocol.md` (Second Opinion, inputs filtrés) et les checklists unifiées §10 (modes PROJET/CIBLE/DIRECT/AVEUGLE, adaptation par type de projet §10.6 incluant la ligne « Écosystème skills » utilisée par toutes les sessions de certification).

## 5. Le graphe consolidé (87 arêtes, 5 couches)

La consolidation mécanique produit **87 arêtes d'interaction** autour des deux pivots, distribuées en cinq couches complémentaires qui se valident mutuellement :

1. **Couche skills** (le registre + les frontmatters) : 21 entrées KB, toutes les arêtes internes réciproques ; 7 consommateurs inverses de gen-plan, 7 de correct-work (dont 2 hors registre : `autonomous-agent`, `agent-prompt-engineering` — skill plateforme).
2. **Couche outillage** : 18 scripts Python (5 arbitres de certification + arbitre answer key + moniteur + auditeur), qui matérialisent les hooks décrits dans les SKILL.md — chaque hook déclaré a son arbitre exécutable.
3. **Couche corpus** : 24 fichiers — 14 PMs GEN-PLAN (v3.6.1→v3.18.0), 3 PMs CORRECT-WORK (v2.4.0→v2.5.1), 1 PM CLONE-CHAT, SHARED, PM-INSTALL, ULTRA (routeur), SYNC-CONTEXT, README + clone de discussion scellé.
4. **Couche registre/distribution** : `KNOWLEDGE.md` (21 entrées + décisions d'architecture) et l'archive d'intégrité v2.2 (round-trip 24/24) — unique voie de diffusion.
5. **Couche session** : worklog (14 Tasks journalisées), plans d'actions, answer keys — l'État Long que les deux skills lisent (règle B-11, lecture seule préalable) et alimentent.

La **validation croisée** avec l'arbitre d'interactions existant (`test-coherence-interactions.py` §3, calibré B3-B4) est cohérente : même graphe de base 14 arêtes bidirectionnelles, la présente analyse l'étendant aux couches outillage/corpus/session et aux arêtes inverses frontmatter.

## 6. Constats (F1-F5, tous ≤ S3 — zéro bloquant)

**F1 (S3) — Skills famille installés hors registre.** Les 5 skills famille écosystème (`autonomous-agent` v1.0.0, `correct-py` v1.0.0, `fleet-engineering` v1.0.0, `memory-engineering` v1.0.0, `spec-driven-development` v1.0.0) sont installés dans `skills/` mais absents du registre KB (21 entrées) et de l'invariant `ECO_SKILLS` de l'arbitre d'intégrité. Conséquence directe : ils sont **invisibles au Protocole de Découverte** (gen-plan E5, correct-work scan dynamique KB), alors même que deux d'entre eux déclarent dépendre des pivots au frontmatter. La Règle Zéro (« registre KB source de vérité ») est franchie pour ces 5 skills — écart hérité du dépôt source 42c2a41 (installation Task 12 : « 5 skills famille écosystème du dépôt » installés, registre livré à 21 entrées).

**F2 (S3) — Lignée corpus CORRECT-WORK en retard.** Le PM CORRECT-WORK le plus récent du corpus est v2.5.1, alors que la forme installée est v2.7.0 (les PMs v2.6.0 et v2.7.0 — introduction du mode AVEUGLE puis du couplage obligatoire — ne sont pas matérialisés au corpus). La garde anti-rétrogradation R2 du PM-INSTALL v1.2.0+ protège ce cas (la forme installée fait foi), mais l'archive d'intégrité — unique voie de diffusion depuis la décision v2.2 — ne peut pas redistribuer la forme documentaire certifiée actuelle.

**F3 (S4) — Trous de lignée GEN-PLAN documentés.** Les PMs v3.14.0 et v3.15.0 sont absents du corpus (perte au wipe inter-sessions, provenance documentée in extenso dans gen-plan §1.14 : « les contenus exacts de v3.14.0/v3.15.0, non documentés, restent perdus »). Constat d'honnêteté : non reconstituibles, aucune action.

**F4 (S3) — Détention des disciplines n°54 non matérialisée.** gen-plan est détenteur principal de `fleet-engineering`, `spec-driven-development` et `memory-engineering` (§1.9, registres d'assignation §8 de chaque discipline) mais son entrée KB ne les liste pas dans « Dépend de », et ces disciplines n'ont pas d'entrée KB (conséquence directe de F1). Asymétrie de la règle SHARED §3.2 (cross-references bidirectionnelles) pour la couche disciplines n°54.

**F5 (S4) — Couplage circulaire assumé.** Voir §2 : by-design, protections en place (ARRÊT EXPLICITE, planchers gradués, Second Opinion).

## 7. Suggestions (a)/(b)/(c)

**(a) Inscrire les 5 skills famille au registre KB — résorbe F1 et F4** *(S3, coût modéré : une session légère)*
Créer les 5 entrées KB (`autonomous-agent` v1.0.0, `correct-py` v1.0.0, `fleet-engineering` v1.0.0, `memory-engineering` v1.0.0, `spec-driven-development` v1.0.0 — descriptions et relations dérivées de leurs SKILL.md réels), ajouter les réciproques « Utilisé par » (gen-plan pour fleet/spec/memory via §1.9 ; correct-work pour correct-py si contractuel), puis recalibrer `ECO_SKILLS` 21→26 dans `check-ecosysteme-integrity.py` et le compte d'entrées du test d'interactions (KO-L004 — recalibrage croisé), resceller l'archive. Bénéfice : le Protocole de Découverte (E5) voit enfin les disciplines n°54 que gen-plan mobilise ; la Règle Zéro redevient vraie pour 100 % des skills écosystème installés.

**(b) Matérialiser les PMs CORRECT-WORK v2.6.0/v2.7.0 au corpus — résorbe F2** *(S3, coût modéré : assemblage par diffs chirurgicaux)*
Reconstituer les deux PMs manquants par la méthode éprouvée de la session B1 (diffs chirurgicaux depuis v2.5.1 + contenu du SKILL.md v2.6.0/v2.7.0 : mode AVEUGLE + hook 2nd opinion pour v2.6.0 ; couplage gen-plan obligatoire + fin du mode autonome pour v2.7.0), les ajouter au corpus (CORPUS_ATTENDU 24→26), resceller l'archive v2.2 et recalibrer les arbitres. Si la reconstitution documentaire s'avérait non fidèle (contenus non traçables), l'alternative honnête serait de documenter l'écart permanent dans le §3.2 du PM-INSTALL (la garde R2 couvre déjà le fonctionnel). Bénéfice : l'unique voie de diffusion du corpus porte la forme certifiée actuelle ; lignée documentaire complète depuis v2.4.0.

**(c) Exécuter les baselines A2 en attente des disciplines n°54 — consolide la couche fleet/spec** *(S4, coût nul en dehors du quota API : armé QUOTA_OK)*
Les skills `fleet-engineering` et `spec-driven-development` ont leurs evals armées (trigger_evals 7 cas chacun, seuil 0.5, confirm 3 runs) mais leurs baselines A2 sont « EN ATTENTE » (`baseline-pending-n34.json`, gate quota — règle KO-L001 économie API). Au prochain QUOTA_OK : exécuter les baselines, puis la Description Optimization si dérive. Bénéfice : les disciplines que gen-plan mobilise à E5/E7 (patterns de flotte, cadrage spec-first) deviennent **mesurées** — leur routage repose aujourd'hui sur des triggers jamais baselinés.

## 8. Verdict de phase (hook correct-work CIBLE)

Livrable P1 (rapport + JSON) vérifié : arêtes dérivées de l'état réel (KO-L003), cross-validation cohérente avec l'arbitre §3 existant, 5 couches couvertes, 7 constats classés S3/S4, aucune omission dans le périmètre demandé (« tous les éléments avec lesquels ils interagissent » → 87 arêtes consolidées). **Verdict : PASS** — l'analyse est complète et mécaniquement traçable ; les constats alimentent les suggestions (a)/(b)/(c) ci-dessus.
