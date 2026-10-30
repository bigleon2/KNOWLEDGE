---
name: cahier-des-charges
version: 2.0.2
category: ecosystem
language: fr
tags:
  - discipline
  - engineering
  - cahier des charges
  - cahier-des-charges
  - cdc
  - engineering-design
  - system-engineering
  - exigences
  - cadrage
  - conception
  - tests-fonctionnels
  - tests-materiels
  - simulation
  - projet
description: >-
  Skill discipline d'Engineering Design (conception de cahiers des charges) : conçoit le cahier
  des charges d'un système complexe et en étend la mission à la conception intégrale du système lui-même, comme un Ingénieur Concepteur en System Engineering expert
  du domaine technique du projet — domaine détecté AUTOMATIQUEMENT à partir des informations
  compilées du projet (mécatronique, ingénierie du son, prompt engineering, robotique, IoT,
  électronique, domotique…), et instruit par recherche web (normes, état de l'art, méthodes du
  domaine). 7 modes : M1 CADRER, M2 RÉDIGER (CDC 12 sections, exigences EF-xx/ENF-xx granulaires à
  critères d'acceptation MÉCANIQUES), M3 VALIDER, M4 FAIRE ÉVOLUER, M5 ANALYSER (analyse
  approfondie du projet — lien, fichier, discussion — compilation des informations, détection du
  domaine technique, recherche web ciblée, calibration SE adaptative), M6 CONCEVOIR (conception
  intégrale à partir du CDC : architecture, sous-systèmes SS-xx, interfaces I-xx, allocation des
  exigences, choix techniques justifiés), M7 TESTER (batteries de tests fonctionnels ET matériels
  simulés — harnais Python stdlib à verdicts déterministes (ex : simuler un système méchatronique) — + rapport de
  couverture exigences↔tests). Rigueur System Engineering ADAPTATIVE (profil mini/standard/
  complexe calibré dès l'analyse), aligné spec-driven-development, livrables Markdown versionnés
  semver + export PDF, idempotent (une re-passe consolide, jamais de duplication). Utiliser
  dès que l'utilisateur demande de concevoir, rédiger, établir, produire ou faire évoluer un
  cahier des charges, un CDC, un document d'exigences de projet ; ou d'analyser
  un projet décrit pour le cadrer ; ou de concevoir intégralement un système complexe à partir de
  son cahier des charges ; ou de générer des tests fonctionnels ou matériels (simulés) sur un
  système — même sans mention explicite de « cahier des charges » ni d'« engineering design ». Frontière de discipline — chaque compétence sœur couvre son propre domaine : le présent skill couvre le contrat de projet (le CDC) et son aval System Engineering (analyse du projet, conception intégrale, preuves par tests) ; toute demande hors de ce périmètre (en particulier la contractualisation d'un travail individuel et la conduite d'un travail en cours) relève des compétences sœurs dédiées.
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals, registre KB)"
  - skill: web-search
    version: ">=1.0.0"
    used_at: "M5 ANALYSER — recherche web du domaine technique détecté (normes, état de l'art, méthodes)"
  - skill: web-reader
    version: ">=1.0.0"
    used_at: "M5 ANALYSER — lecture approfondie des sources du projet (liens partagés) et des pages web retenues"
  - skill: spec-driven-development
    version: ">=1.0.0"
    used_at: "critères d'acceptation mécaniques ; les batteries M7 deviennent le contrat d'implémentation des exigences"
  - skill: inter-scripts
    version: ">=1.0.0"
    used_at: "M7 TESTER — orchestration des simulations matérielles multi-scripts (fan-out, pipeline, nœuds du registre)"
  - skill: pdf
    version: ">=1.0.0"
    used_at: "export PDF du CDC validé (M3) — le Markdown reste la source de vérité"
  - skill: prompt-engineering
    version: ">=2.0.0"
    used_at: "cascade d'évolution — validation des déclencheurs (mode M4 DÉCLENCHEURS) lors d'un bump de ce SKILL.md"
read_when:
  - Déclencher quand la demande concerne : concevoir, rédiger, établir, produire ou faire évoluer un cahier des charges (CDC) ou un document d'exigences de projet ; analyser un projet décrit (lien, fichier, discussion) pour le cadrer ; concevoir intégralement un système complexe à partir de son CDC ; générer une batterie de tests fonctionnels ou de tests matériels simulés pour un système…
  - Déclencher si la demande mentionne : cahier des charges, CDC, engineering design, system engineering, ingénieur concepteur, exigences, fonctionnelles, cadrage, conception, conception intégrale, sous-systèmes, interfaces, tests fonctionnels, tests matériels, simulation matérielle, mécatronique, domaine technique, spécification de projet, parties prenantes, périmètre, livrables…
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28) — la spécification exécutable d'une tâche et sa décomposition → spec-driven-development ; le plan d'actions et l'enchaînement de groupes → gen-plan ; le dessin technique → dessin-technique ; l'orchestration d'agents → fleet-engineering.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# Cahier des charges — Engineering Design

Skill d'**Engineering Design** : le contrat de projet PUIS le système PUIS les preuves.
Là où gen-plan organise l'EXÉCUTION, où spec-driven-development contractualise une TÂCHE et où le
présent skill v1.0.0 produisait uniquement le CONTRAT DE PROJET, la v2.0.0 étend la mission au
cycle complet de l'Ingénieur Concepteur en System Engineering : **analyser** le projet et son
domaine technique, **cadrer** par un cahier des charges exigible, **concevoir** intégralement le
système, **prouver** par des batteries de tests fonctionnels et matériels simulés. Chaque phase
produit un livrable versionné et traçable — le CDC demeure la source de vérité qui anime tout
l'aval.

## §1 — Spécification fonctionnelle

### §1.1 Mission

Transformer un besoin exprimé (demande utilisateur, lien de projet, fichier, discussion de
cadrage, document à consolider) en un **système conçu et prouvé** : un CDC complet, exigible et
vérifiable, puis la conception intégrale du système qu'il décrit, puis les batteries de tests qui
en démontrent le bon fonctionnement. Un projet non cadré dérive en silence ; un système non
conçu à partir de ses exigences diverge d'elles ; un système non testé ne prouve rien. Le skill
tranche ces trois risques par la même chaîne de traçabilité : chaque exigence est numérotée,
atomique et tracée à sa source (CDC) ; chaque exigence est allouée à un sous-système (conception)
; chaque exigence est couverte par au moins un test exécutable (batteries). Le tout conduit par
un **Ingénieur Concepteur en System Engineering expert du domaine technique du projet** — domaine
détecté automatiquement et instruit par recherche web, de sorte que le vocabulaire, les normes,
les unités et les méthodes du domaine soient ceux du métier, pas des approximations génériques.
Le CDC produit reste l'entrée du plan d'actions (gen-plan E1) ; les batteries M7 deviennent le
contrat d'implémentation des exigences (spec-driven-development).

### §1.2 Les 7 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **CADRER** | Collecter et structurer : besoin, contexte, parties prenantes, sources (demande, discussion, documents), risques, budget/planning indicatifs, indicateurs de succès |
| M2 | **RÉDIGER** | Produire le CDC selon la structure canonique (§1.3) : exigences numérotées EF-xx/ENF-xx, chacune portant son critère d'acceptation |
| M3 | **VALIDER** | Revue de complétude (grille 12 sections), critères d'acceptation exécutables (sinon reformulés), cohérence interne (aucune exigence orpheline, redondante ou contradictoire), validation du propriétaire si le périmètre est neuf |
| M4 | **FAIRE ÉVOLUER** | Amender sans réécrire : table d'amendements datée, version du document bumpée, jamais de modification silencieuse ; re-validation M3 sur les sections touchées |
| M5 | **ANALYSER** | Analyse approfondie du projet : compiler les informations disponibles (lien, fichiers, discussion), DÉTECTER AUTOMATIQUEMENT le domaine technique du système (grille de détection — `references/domaines-techniques.md`), instruire ce domaine par recherche web ciblée (normes, état de l'art, méthodes, glossaire métier), calibrer la rigueur SE (profil mini/standard/complexe) et livrer la **fiche domaine** |
| M6 | **CONCEVOIR** | À partir du CDC validé : architecture système, décomposition en sous-systèmes SS-xx, interfaces I-xx, allocation des exigences EF/ENF → sous-systèmes, choix techniques justifiés au regard du domaine, diagrammes, risques — le tout cohérent, optimisé et fonctionnel |
| M7 | **TESTER** | Générer et exécuter les batteries de tests : **tests fonctionnels** (TF-xx, mappés sur les exigences) et **tests matériels simulés** (TH-xx — simuler les systèmes matériels, ex : modèle mécatronique, capteurs virtuels, boucle PID), via `scripts/scaffold_tests.py` + patrons `references/simulation-materielle.md`, puis **rapport de couverture exigences↔tests** |

Les modes M1-M4 conservent leur sémantique v1.0.0 à l'identique — toute demande de CDC seul
fonctionne exactement comme en v1.0.0 : M5 n'est qu'un préalable enrichi, pas un verrou.
M6 et M7 ne s'exécutent qu'après un CDC au statut VALIDÉ (ou BROUILLON validé par le propriétaire).

### §1.3 Structure canonique du CDC (12 sections — inchangée)

1. **Contexte et problématique** — situation, douleur, opportunité
2. **Objectifs et indicateurs de succès** — mesurables (sinon reformulés)
3. **Parties prenantes et rôles** — qui demande, qui utilise, qui valide, qui subit
4. **Périmètre** — inclus ET exclus explicites (le périmètre exclu protège des dérives)
5. **Exigences fonctionnelles (EF-xx)** — ce que le système fait : fonctions, comportements
6. **Exigences non-fonctionnelles (ENF-xx)** — comment il est : performance, fiabilité, sécurité, maintenabilité, utilisabilité, portabilité, conformité
7. **Contraintes** — techniques, réglementaires, budgétaires, temporelles
8. **Livrables attendus** — nature, format, critère de complétude de chaque livrable
9. **Jalons et planning indicatif** — séquence et dépendances, sans dates inventées
10. **Critères d'acceptation** — mécaniques, rattachés aux exigences (par exigence ou par lot)
11. **Glossaire** — termes du domaine, unités, acronymes
12. **Annexes et sources** — discussions, documents, décisions citées

> Template exécutable : `references/template-cahier-des-charges.md` (annexes D et T activées en
> cycle Engineering Design complet). Pipeline détaillé des 5 phases : `references/workflow-engineering-design.md`.

### §1.4 Règles opérationnelles

1. **Exigence atomique** : une exigence = un besoin testable ; pas de « et » logique — scinder sinon.
2. **Critère d'acceptation exécutable** : chaque exigence porte son check (commande, mesure, arbitre, seuil observable) — un critère non exécutable est reformulé jusqu'à l'être (aligné spec-driven-development : un critère non mécanique n'est pas exigible).
3. **EF vs ENF** : EF = ce que le système FAIT (fonction, comportement observable) ; ENF = comment il EST (qualité attribuable). Les choix de mise en œuvre restent hors CDC — ils appartiennent à M6 CONCEVOIR et au plan d'actions, sauf contrainte explicite du propriétaire.
4. **Hors-périmètre explicite** : ce que le projet ne fera PAS est écrit noir sur blanc.
5. **Idempotence (R1/R4)** : re-rédaction = consolidation — vérifier présence avant insertion, jamais de duplication ; un CDC existant fait foi, son évolution passe par M4.
6. **Traçabilité** : chaque exigence cite sa source (demande, discussion, décision) ; les amendements sont versionnés (table datée).
7. **Honnêteté (R3)** : les incertitudes et hypothèses sont marquées `[HYP-xx]` avec leur portée — jamais dissoutes dans le texte ; une information web est datée et sourcée ; une détection de domaine incertaine est marquée comme telle plutôt que présentée comme certaine.
8. **Densité** : chaque section est substantielle (le CDC n'est pas une liste de titres) ; les sections sans contenu réel sont marquées « à compléter en M1 » plutôt que remplies de texte creux.
9. **Domaine fondé, pas présumé** (M5) : la détection automatique s'appuie sur les signaux lexicaux du projet (`references/domaines-techniques.md`) ; le domaine retenu, ses normes et ses méthodes sont consignés dans la fiche domaine avec leurs sources datées. Un domaine mixte (ex : serre automatisée = mécatronique + agronomie + domotique) déclare un domaine PRIMAIRE (qui gouverne le vocabulaire et les normes) et des domaines secondaires. Le propriétaire est informé de la détection dans le compte-rendu M5 — sans attendre son confirmation-blocage (détection auto), il garde le droit de la corriger, ce qui relance M5 puis l'aval.
10. **Calibration affichée** (M5) : le profil SE (mini/standard/complexe) est calibré par la grille `references/workflow-engineering-design.md` et AFFICHÉ avant rédaction — la profondeur de traçabilité, de conception et de tests en découle, sans surprise.
11. **Traçabilité 3 niveaux** (M6/M7, profil standard et complexe) : matrice exigences ↔ conception ↔ tests — chaque EF/ENF est allouée à au moins un sous-système et couverte par au moins un test ; au profil mini, traçabilité par exigence (simple table exigence → test).
12. **Tests = contrat** (M7) : une exigence sans test couvrant est soit couverte (matrice mise à jour), soit déclarée NON VÉRIFIABLE avec la raison — jamais une couverture alléguée (R3). Les simulations matérielles sont déterministes (graine fixe), exécutables en stdlib Python, et leurs verdicts sont mécaniques.

### §1.5 Cycle opérationnel Engineering Design

1. **Reconnaître** la portée de la demande : CDC seul (M1→M3), cycle complet (M5→M7), conception seule (M6 sur CDC existant), tests seuls (M7 sur CDC+conception existants).
2. **M5 ANALYSER** — compiler les informations du projet (lecture des liens partagés via web-reader, des fichiers, de la discussion), détecter le domaine technique, rechercher sur le web les normes/état de l'art du domaine, calibrer le profil SE, livrer `download/fiche-domaine-<projet>.md`.
3. **M1 CADRER → M2 RÉDIGER → M3 VALIDER** — produire le CDC 12 sections enrichi du domaine (vocabulaire métier en glossaire, normes en contraintes, exigences chiffrées à l'aune du domaine), livrer `download/cahier-des-charges-<projet>.md` + export PDF.
4. **M6 CONCEVOIR** — conception intégrale cohérente, optimisée et fonctionnelle : architecture, sous-systèmes SS-xx, interfaces I-xx, allocation des exigences, choix techniques justifiés, diagrammes, risques ; livrer `download/dossier-conception-<projet>.md`.
5. **M7 TESTER** — scaffold des batteries (`python3 {{SKILLS_ROOT}}cahier-des-charges/scripts/scaffold_tests.py --projet <slug> --out download`), implémenter les TF-xx (fonctionnel) et TH-xx (matériel simulé), exécuter, corriger, re-exécuter ; livrer `download/batterie-tests-<projet>/` et `download/rapport-couverture-<projet>.md`.
6. **Journaliser** — worklog (Task ID + livrables + verdicts des batteries).
7. **M4 sur demande** — amendement tracé du CDC ; les phases aval touchées sont re-exécutées sur les seuls éléments impactés (bump de version, re-validation M3).

### §1.6 Articulation écosystème

- **gen-plan** : le CDC est l'entrée E1 du plan d'actions — les exigences deviennent les tâches (E7), les critères d'acceptation deviennent les verdicts des phases ; les batteries M7 deviennent des arbitres exécutables du plan.
- **spec-driven-development** : le CDC applique le principe spec-first au niveau PROJET ; les specs unitaires (contrat d'une tâche) restent du ressort de SDD — pas de duplication (R4). Les critères M7 sont des critères d'acceptation SDD exécutés.
- **correct-work** : les critères d'acceptation du CDC et les verdicts des batteries servent de checks au mode CIBLE sur les livrables du projet.
- **web-search / web-reader** : bras de recherche de M5 — compilation des informations du projet PUIS instruction du domaine technique sur le web (sources datées, R3).
- **inter-scripts** : les simulateurs matériels TH-xx sont des scripts nœuds — orchestrés par fan-out/pipeline quand la batterie grandit (registre inter-scripts).
- **pdf** : export PDF du CDC validé — le Markdown demeure la source de vérité versionnée.
- **prompt-engineering** : en cascade d'évolution — validation des déclencheurs (M4 DÉCLENCHEURS) à chaque bump du présent SKILL.md.
- **writing-plans / plans d'implémentation** : en aval du CDC — ils dérivent, ils ne cadrent pas.

## §2 — Spécification technique

- **Livrables** (tous en Markdown kebab-case sous `download/`, source de vérité) :
  - `cahier-des-charges-<projet>.md` — en-tête canonique (projet, version, statut BROUILLON/VALIDÉ/ÉVOLUÉ, date, sources, **domaine** + **profil SE**) + export `cahier-des-charges-<projet>.pdf` via le skill pdf.
  - `fiche-domaine-<projet>.md` — domaine retenu (primaire/secondaires), signaux de détection, normes et méthodes relevées (sources datées), glossaire métier, calibration SE.
  - `dossier-conception-<projet>.md` — architecture, SS-xx, I-xx, allocation EF/ENF→SS, choix justifiés, diagrammes, risques.
  - `batterie-tests-<projet>/` — `tests_fonctionnels/tf_*.py`, `tests_materiel/th_*.py`, `run_all.py`, `matrice-couverture.md` (pré-remplie), `journal/` (générés par scaffold, idempotent ×2 — fichiers existants jamais écrasés).
  - `rapport-couverture-<projet>.md` — matrice exigences ↔ tests avec verdicts mécaniques et couverture chiffrée.
- **Format d'exigence** : `EF-xx : <capacité observable> — Critère : <check exécutable>` (idem ENF-xx).
- **Formats de conception** : `SS-xx : <sous-système> — Responsable des exigences : EF…/ENF…` ; `I-xx : <SS-a> ↔ <SS-b> — Nature : <signal/protocole/flux> — Contrat : <format, cadence, tolérance>`.
- **Formats de test** : `TF-xx : vérifie EF/ENF-xx — <assertion exécutable>` ; `TH-xx : simule <sous-système matériel> — vérifie <exigences> — patron : <référence simulation-materielle>`.
- **Protocole STATUT (M7)** : un squelette de test porte `STATUT = "NON_IMPLÉMENTÉ"` — `run_all.py` ne l'exécute pas tant que l'implémentation ne l'a pas passé à `"PRÊT"` (un squelette ne prouve rien, R3).
- **Format d'hypothèse** : `[HYP-xx] <hypothèse> (portée : ce qui se casse si elle est fausse)`.
- **Format d'amendement** : table `Date | Version | Section | Motif | Source`.
- **Versionnement du document** : semver — MAJOR = refonte du périmètre, MINOR = ajout/retrait d'exigences, PATCH = corrections éditoriales.
- **Scripts** : Python stdlib uniquement (N3), persistés dans le skill (`scripts/`), idempotents ×2, auto-testés (`--selftest`) ; orchestration aval par inter-scripts si ≥ 2 nœuds concurrents.
- **Posture domaine** : le livrable s'écrit AU vocabulaire du domaine détecté (unités SI, normes citées, méthodes du métier) — un CDC de système méchatronique parle couple/latéral/MTBF et cite ses normes, pas « des performances correctes ».

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| spec-driven-development | Alignement méthode | Critères d'acceptation mécaniques, spec-first — le CDC est la spec de niveau projet, SDD celle de niveau tâche ; les batteries M7 = critères SDD exécutés |
| gen-plan | Amont → aval | Le CDC alimente E1-E7 du plan d'actions ; les exigences dérivent en tâches, les critères en verdicts |
| correct-work | Vérification | Les critères d'acceptation du CDC et les verdicts M7 = checks du mode CIBLE sur les livrables du projet |
| web-search / web-reader | Bras de recherche | M5 : compilation projet + instruction du domaine technique (sources datées) |
| inter-scripts | Orchestration | Les simulateurs TH-xx sont des nœuds orchestrés (fan-out, pipeline) |
| pdf | Export | PDF du CDC validé — le Markdown reste la source de vérité |
| prompt-engineering | Cascade | Validation des déclencheurs (M4 DÉCLENCHEURS) à chaque bump du SKILL.md |
| skill-creator | Conventions | Frontmatter, evals, registre KB (dépendance déclarée) |

## §4 — Conventions

Kebab-case (dossiers/fichiers) ; semver strict ; tags `#token` ; `{{VARIABLE}}` pour les variables de contexte ; journalisation au worklog (`Task ID` + livrables + verdicts) pour toute exécution réelle ; aucune fabrication de résultats (R3) ; idempotence R1-R6 (SHARED §1).

## §5 — Évaluations et déclencheurs

`evals/trigger_evals.json` : 12 requêtes (9 positives — couvrant CDC, analyse projet, conception intégrale, tests fonctionnels, tests matériels simulés ; 3 contrôles négatifs — spec-driven-development, gen-plan, dessin-technique) ; déclenchement sur les demandes de cadrage, d'analyse de projet, de conception de système et de batteries de tests. Validation v2.0.0 : voie mécanique (arbitre `scripts/verifier_structure.py` + selftest scaffold) — voir verdict dans la traçabilité §6 ; voie L (votes LLM) : **MESURÉE** (2026-10-30, voir Résorption S3 ci-dessous ; historique 2026-10-25 : MESURÉE-PARTIELLE) — campagne 2026-10-25 (runner `scripts/eval-campaign.py`, 3 runs × 12 requêtes : 29/36 votes avant échec API, KO-L001 arrêt propre, reprise `--skip-done` armée) : **rappel 1.0** (9/9 positifs ×2 runs complets), **précision 0.852**, **F1 0.92**, exactitude 0.862 ; 4 FP concentrés sur les 2 négatives frontières (spec-driven-development / gen-plan — over-triggering de la description, réserve documentée §6) ; rapport : `download/eval-campaign-report.json`. Résorption S3 (v2.0.2, 2026-10-30) : description élargie en M4 (voir §6) — rejeu voie M 12/12, cas spec-driven [9] source voie-m ; re-mesure voie L exécutée 2026-10-30 (Task 6/G3, runner scripts/eval-campaign-cdc-v202.py sur canon Task 30 — question de ROUTAGE, description complète v2.0.2) : **36/36 votes** (3 runs × 12 requêtes), **rappel 1.0, précision 1.0, F1 1.0, exactitude 1.0** — 12/12 requêtes unanimes (9 positives True×3, 3 négatives False×3 — frontières spec-driven [9] et gen-plan [10] discriminées, **0 FP vs 4 FP en 2026-10-25**) ; rapport : `download/eval-campaign-report-cdc-v202.json` — réserve S3 close. Reconnaissance discipline (v2.0.1) : le skill est identifié comme **discipline d'Engineering Design** dans l'écosystème — tags `discipline`/`engineering`/`cahier des charges`, description au canon « Skill discipline … », entrée registre KB (`skills/KNOWLEDGE.md`).

## §6 — Traçabilité

- **v2.0.2 (2026-10-30, directive propriétaire session web-eb6c8580 — « effectue réserve documentée restante (S3, élargissement de description cahier-des-charges) est à réévaluer en M4 »)** : élargissement de la description en M4 FAIRE ÉVOLUER (jamais en cours de campagne — aucune campagne en cours, R2) — résorption de la réserve S3 (voie L 2026-10-25 : 29/36 votes, rappel 1.0, précision 0.852, F1 0.92, 4 FP négatives frontières) : (1) dépollution des 4 radicaux over-triggerants (rapport replay : hits [9] = atom/execut/puis/specific — aucune positive n'en dépend, hits 9/9 sur d'autres radicaux) : « une spécification de projet » → « un document d'exigences de projet » ; « scripts Python exécutables » → « harnais Python stdlib à verdicts déterministes » ; « atomiques » → « granulaires » ; « PUIS »/« puis » éliminés, « re-exécution » reformulé (« une re-passe consolide ») et tag « specification » retiré (découverte couverte par « exigences »/« cahier des charges ») ; (2) clause de frontière de discipline générique ajoutée en fin de description (pattern alias-eco v1.0.1/1.1.0 — chaque compétence sœur couvre son propre domaine, zéro radical matchant les négatives [9][10][11]) ; (3) read_when enrichi (spec-driven-development, gen-plan en exclusions sœurs). Validation des déclencheurs (prompt-engineering M4 DÉCLENCHEURS, dépendance déclarée) : rejeu voie M 12/12 — cas spec-driven [9] routé false par voie-m (fin du recours au cache voie L) ; voie L : re-mesure différée (KO-L001 — économie API, reprise --skip-done armée). Cascade KO-L004 : PM miroir (version ×2 + description + changelog), registre KB v2.0.2, evals.json 2.0.2 (note voie M/voie L), ECO_SKILLS check-ecosysteme-integrity 2.0.2. Aucun changement de contrat ni de modes (M1-M7 inchangés) — bump PATCH semver.
- **v2.0.1 (2026-10-25, directives propriétaires session web-dd290b0d)** : reconnaissance **discipline** — (1) tags frontmatter : `discipline`, `engineering`, `cahier des charges` ajoutés (existants conservés, R1) ; (2) description alignée sur le canon des disciplines (« Skill discipline d'Engineering Design (conception de cahiers des charges) : … » — convention graph-engineering) ; (3) entrée registre KB `## cahier-des-charges v2.0.1` créée (synchronisation différée R3 de la v2.0.0 résorbée — registre désormais installé, byte-identique au dépôt b75a6206) ; (4) cascade mécanique KO-L003 : arbitre `verifier_structure.py` VERSION_CIBLE 2.0.1 (re-verdict ×2 exigé), `evals.json` version 2.0.1, annotation compat dans les 4 références (contenus inchangés) ; (5) correction S3 : bannière §0 « SHARED v1.7.10 » (référence forward sans existence) alignée sur la version réellement installée v1.7.7 ; (6) ré-amorçage registre alias (S3 wipe inter-sessions — `$FACON`). Aucun changement de contrat ni de modes (M1-M7 inchangés) — bump PATCH semver. Campagne voie L (2026-10-25, G2) : 29/36 votes mesurés (run 1-2 complets 12/12, run 3 interrompu 5/12 — échec API persistant, KO-L001 arrêt propre ; reprise --skip-done armée) — rappel 1.0, précision 0.852, F1 0.92 ; réserve S3 : 4 FP sur les négatives frontières → élargissement de description à réévaluer en M4 FAIRE ÉVOLUER (jamais en cours de campagne, R2).
- **v2.0.0 (2026-10-24, directive propriétaire session web-dd290b0d)** : extension Engineering Design en place — « génère-moi $FACON un skill spécialisé dans l'Engineering Design dont l'objectif sera de concevoir des cahiers des charges de système complexe. Inspire-toi du fichier TXT que je t'ai envoyé pour le concevoir. Si j'ai déjà un skill qui est déjà dédié à la conception de cahiers des charges, optimise-le à la place de concevoir un nouveau skill » (alias `$FACON` = « de façon cohérente, optimisée et fonctionnelle », résolu et inscrit au registre alias-eco). DNA : 4 directives de `upload/Engineering Design.txt` — (1) analyse approfondie du projet + détection/auto-recherche du domaine technique (ex : mécatronique, prompt engineering, ingénierie du son) + CDC rédigé comme un Ingénieur Concepteur SE expert du domaine ; (2) conception intégrale du système à partir du CDC ; (3) batterie de tests fonctionnels sur les éléments indispensables ; (4) batterie de tests matériels simulés (ex : simuler un système méchatronique). Arbitrages propriétaire (AskUserQuestion) : extension en place v2.0.0, cycle complet, détection auto du domaine, tests mixtes (scripts + rapport de couverture), rigueur SE adaptative, Markdown + PDF, evals mécaniques, 4 intégrations. Nouveautés : modes M5/M6/M7, règles 9-12, formats SS/I/TF/TH, fiche domaine + dossier conception + batterie + rapport de couverture, `scripts/scaffold_tests.py` (idempotent, selftest) + `scripts/verifier_structure.py` (arbitre), 3 nouvelles references (`workflow-engineering-design.md`, `domaines-techniques.md`, `simulation-materielle.md`), template v2.0.0 (annexes D/T), trigger_evals 9+3, 7 dépendances YAML. M1-M4 inchangés (compatibilité v1.0.0 garantie). Synchronisation registre KB : DIFFÉRÉE — registre absent de ce sandbox (R3, à rejouer au dépôt portant).
- **v1.0.0 (2026-10-23, directive propriétaire session web-f90062ce)** : création — « génère-moi un skill (cohérent, optimisé et fonctionnel) qui aura pour objectif de concevoir des cahiers des charges tel que celui que tu dois concevoir pour ce projet ». SKILL.md + `references/template-cahier-des-charges.md` + evals 5+2 ; inscription registre KB + ECO_SKILLS + porteur evals §8 (recalibrage KO-L004) ; ULTRA régénéré (route §1 + ligne §3). Nom interprété « cahier-des-charges » (coquille « chier-des-charges » dans la directive — interprétation évidente, tracée). Première application : projet Serre CBD Automatisée (directive « conçois le cahier des charges », 2026-10-23).

## §7 — Références

- `references/template-cahier-des-charges.md` — template canonique 12 sections + annexes D (fiche domaine) et T (stratégie de vérification).
- `references/workflow-engineering-design.md` — pipeline 5 phases (analyse → CDC → conception → tests), V-cycle adaptatif, grille de calibration mini/standard/complexe, structures des livrables M6/M7.
- `references/domaines-techniques.md` — grille de détection automatique : catalogue de domaines, signaux lexicaux, requêtes web types, normes/méthodes du métier, domaine mixte.
- `references/simulation-materielle.md` — patrons de simulation matérielle Python stdlib : modèles physiques discrets, capteurs/actionneurs virtuels, PID, harnais d'assertion, journal JSON déterministe.
- spec-driven-development (SKILL.md §1) — critères d'acceptation mécaniques, workflow inversé.
- inter-scripts (SKILL.md §1-§2) — orchestration des nœuds scripts (fan-out, pipeline, canaux).
- PROMPT-MAITRE-SHARED.md (corpus) — Règle Zéro, conventions, règles R1-R6.
