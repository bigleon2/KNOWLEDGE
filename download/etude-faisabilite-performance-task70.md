# Étude de faisabilité — optimisation des performances de l'écosystème Knowledge : (a) refactoring orienté objet intégral · (b) compilation en un noyau unique

**Horodatage : 2026-11-07T17:48:17Z** · Task 70 G4 (Task 3 de la directive propriétaire) · Livrable du plan `download/plan-task70-integration-bibliotheque-ghorg-etude-faisabilite.md` · Méthode : mesures terrain mécaniques (script `scripts/task70-inventaire-ecosysteme.py`, sortie `download/task70-mesures-terrain.json`) + simulations from-scratch + recherche web (sources citées §7) — **toute affirmation chiffrée est reproductible par re-jeu du script** (règle d'or n°5).

## 1. Contexte et questions posées

L'écosystème Knowledge est un système **prompt/file-based** : 125 dossiers sous `skills/` (dont 6 collections `@`), 231 fichiers SKILL.md (10,4 Kio moyen), 327 scripts Python, orchestration par fichiers (SHARED, PM, KB), certification par arbitres mécaniques (integrity 110 checks, coherence, vcw, cross), installation par pipeline PM INSTALL. Le propriétaire a proposé deux axes d'optimisation des performances — installation et exécution :

- **Idée A — OOP intégral** : réécrire l'écosystème en objet « de façon cohérente » ;
- **Idée B — noyau compilé unique** : « compiler l'écosystème en un seul noyau façon Linux » pour optimiser installation/exécution.

## 2. Résultat de l'étude en une ligne

**Les deux idées, prises littéralement, n'optimisent PAS les performances — car le goulot réel n'est ni l'entr-sortie fichiers ni la structure des données, mais le budget #token (contexte LLM). En revanche, réinterprétées, elles décrivent l'architecture que l'écosystème met déjà en place ; les gains réels accessibles sont listés en §6 (feuille de route chiffrée).**

## 3. Mesures terrain (baseline chiffrée — environnement bac à sable, disque local SSD)

| Métrique | Valeur mesurée | Commande / méthode |
|---|---|---|
| Fichiers écosystème (skills/ + scripts/) | **2 164 fichiers · 71,3 Mio** | `task70-inventaire-ecosysteme.py` |
| Lecture séquentielle de TOUT l'arbre (2 164 fichiers) | **33 ms** (cache froid) · 24 ms (chaud) | open() boucle |
| Lecture des mêmes contenus depuis un zip unique | **327 ms — 10× plus lent** | zipfile.ZipFile.read() |
| Construction du zip unique (2 164 fichiers) | 2,86 s | ZIP_DEFLATED |
| Taille du zip | 45,5 Mio (**−36 %** vs arbre) | — |
| **Garde d'installation** (`ensure-installed.py --check`, 53 entrées KB) | **0,04 s** | perf_counter |
| **Arbitre integrity** (110 checks) | **0,04 s** | perf_counter |
| **Pipeline PM INSTALL complet** (sync 53 formes + rescellement archive + 53 SHA) | **0,14 s** | perf_counter |
| Installation from-scratch **git clone** (local, --no-hardlinks) | **0,69 s** | simulation §5 |
| Installation from-scratch **bundle noyau** (build zip + unzip cible vierge) | **3,94 s — 5,7× plus lent** que git | simulation §5 |

**Lecture** : l'installation et l'orchestration de l'écosystème sont **déjà quasi instantanées** (pipeline : 140 ms). Le temps passé « dans l'écosystème » lors d'une session est dominé par les appels LLM (estimation de grille #token du plan présent : ~56 k #token pour une tâche de cette taille), pas par les fichiers. **Il n'existe aucun goulot d'entr-sortie à éliminer** : un facteur 10 d'accélération sur 33 ms ne serait pas perceptible.

## 4. Analyse de faisabilité — Idée A : refactoring orienté objet intégral

### 4.1 Ce que « passer en objet » signifierait ici

Réécrire les artefacts (SKILL.md, PM, registre KB, worklog) en classes Python : `Skill`, `Registry`, `Arbiter`, `Plan`… avec un chargeur unique (le « runtime »).

### 4.2 Constat central : l'écosystème EST déjà orienté objet — par des fichiers

| Concept OOP | Réalisation actuelle dans l'écosystème |
|---|---|
| Encapsulation | Skills auto-contenus (Règle Zéro : frontmatter complet, scripts, references/) |
| Interface / contrat typé | Frontmatter YAML (name, version, dependencies) + **arbitres mécaniques = contrats exécutables** (spec-driven development) |
| Héritage de méthode | SHARED §7 — la « méthode-mère » (gen-plan) héritée par les disciplines (§1.6) |
| Registre de types / DI | Registre KB (source de vérité, 53 entrées versionnées, `kb_eco_skills()` = chargement dynamique) |
| Classes abstraites | PM générés mécaniquement (KO-L004) = spécifications stables dérivées des formes installées |
| Tests unitaires | Harnais $FACON2, self-tests embarqués, idempotence ×2 (R6) |

Le paradigme objet est **déjà réalisé, sous une forme fichier** — parce que le runtime de cet écosystème n'est pas Python : **c'est un modèle de langage**. Un LLM consomme du TEXTE (auto-contenu, lisible, diffable) ; une classe Python exigerait une couche de traduction (import/sérialisation) à chaque utilisation par n'importe quelle IA (la promesse pm-skill : « coller comme prompt système » dans une IA externe — incompatible avec un binaire/bibliothèque).

### 4.3 Verdict Idée A — **NON RECOMMANDÉ tel quel** (coût >> gain, gain = 0 sur le goulot réel)

- **Gain performance** : nul — le goulot est le contexte LLM (#token), pas la structure des artefacts ; une réécriture ne change pas un seul token lu.
- **Coûts** : rupture des invariants R4 (archivage byte-identité @historique, git diff granulaire = forensique des disparitions version-management), perte de l'auto-contenance inter-IA, migration de 125 dossiers / 231 SKILL.md / 327 scripts, invalidation des 110 checks integrity et du pin ECO_SKILLS, réécriture des gardes.
- **Risques** : chaque garde (É1-INSTALL, auto-réparation, KO-L004 cascade) est calée sur la forme fichier ; tout réécrire d'un coup viole le principe zéro-régression de refactor-guard (refactoring par petites transformations préservant le comportement observable — discipline n°55).
- **Ce qui a du sens** (réinterprétation) : (a) appliquer l'OO **aux scripts Python réels** (arbitres, harnais) là où c'est natif — déjà en pratique (classes `Path`, modules stdlib) ; (b) durcir les « interfaces » existantes : le frontmatter comme contrat formel (déjà), les dépendances YAML comme graphe typé (déjà), et continuer la chasse aux duplications R4.

## 5. Analyse de faisabilité — Idée B : compilation en un noyau unique « façon Linux »

### 5.1 Simulation mécanique (from-scratch, appels apples-to-apples)

| Scénario d'installation | Temps | Taille cible |
|---|---|---|
| git clone (local) — voie actuelle | **0,69 s** | 71,3 Mio |
| Noyau : build zip unique + unzip en cible vierge | **3,94 s** (build 3,34 s + unzip 0,60 s) | 45,5 Mio |
| Lecture d'exécution complète (arbre) | **33 ms** | — |
| Lecture d'exécution complète (zip) | **327 ms** | — |

Le bundle unique **perd sur les deux tableaux** qu'il prétend optimiser : installation 5,7× plus lente (le build compile tout à chaque fois), exécution 10× plus lente (décompression à la volée ; premiers démarrages shiv/zipapp encore plus lents le temps de peupler le cache — source §7.5). Son seul avantage mesuré : **−36 % de taille** — un gain de DIFFUSION, pas d'exécution — et l'écosystème a déjà un véhicule de diffusion compact : l'archive d'intégrité `mon-ecosysteme_archive.zip` (véhicule v2.2/v2.3, rescellée à chaque pipeline, round-trip SHA).

### 5.2 L'analogie Linux, correctement lue

Linux est un noyau **monolithique mais MODULAIRE** : un socle compact et stable + des **modules chargeables** (LKM) + des interfaces stables + un système de build (Kbuild) qui produit des configurations par cible (sources §7.6-§7.9). Le réel enseignement n'est pas « tout compiler en un bloc » (le modèle micro-noyau tout-objet a été historiquement le choix de Mach/GNU Hurd — latences de communication inter-modules ; c'est l'échec dont Linux s'est écarté en gardant un noyau monolithique). Traduit pour l'écosystème :

| Linux | Équivalent écosystème (DÉJÀ EN PLACE) |
|---|---|
| Noyau compact stable | gen-plan + correct-work + SHARED + gardes (le socle) |
| Modules chargeables (LKM) | Les skills — chargés À LA DEMANDE (E5 sélection) |
| Table des symboles | Registre KB |
| Interfaces stables (API LKM) | Frontmatter + dependencies YAML + §0 Contexte Système |
| Bootloader / install | PM INSTALL + pipeline + garde É1-INSTALL |
| Kbuild | Générateurs mécaniques (KO-L004, PM-INSTALL v1.9.7 §2quater) |
| kselftest | Arbitres (integrity/coherence/vcw/cross) |

**L'écosystème EST déjà architecturé « façon Linux » correctement comprise** : petit noyau + modules chargeables + interfaces stables + certification. « Compiler en un seul noyau » reviendrait à l'anti-pattern que Linux a précisément évité (liaison statique totale : chaque changement = recompilation complète — mesurée : 3,34 s — et perte de la réparabilité module-par-module, précisément le mécanisme qui a neutralisé les 34+ disparitions de version-management).

### 5.3 Verdict Idée B — **NON RECOMMANDÉ** (contre-productif mesuré)

- Installation : **5,7× plus lente** (0,69 s → 3,94 s).
- Exécution : **10× plus lente** (33 ms → 327 ms).
- Casserait : git diff granulaire (forensique R4), auto-réparation fichier-par-fichier (garde Task 56), lecture ciblée on-demand (progressive disclosure), @historique byte-identité.
- Le seul gain (−36 % taille) est déjà couvert par l'archive de diffusion existante.

## 6. Recommandations d'aide à la décision $FACON2 — feuille de route incrémentale

Le goulot RÉEL est le **budget #token** (le coût d'une session est en dizaines de milliers de tokens, pas en millisecondes de fichiers). Les leviers suivants attaquent ce goulot, sans rupture R2/R4 :

- **R1 — Progressive disclosure renforcée (gain réel, risque faible, S2)** : re-curation des SKILL.md les plus lourds (la moyenne 10,4 Kio cache des extrêmes ; les top lourds du dépôt dépassent 100 Kio — le présent SKILL.md gen-plan pèse ~100 Kio). Méthode éprouvée dans l'industrie (source §7.3) : corps de skill court (checklist) + détails externalisés en `references/` lus à la demande — 1 156 lignes retirées à fonctionnalité égale dans le cas cité. L'écosystème possède déjà la mécanique (§0 en-tête + references/) ; il manque un arbitre de « poids de chargement » (mesure #token par skill à l'invocation E5). **C'est LE chantier performance de l'écosystème.**
- **R2 — Prompt cache / anti-sprawl (S2)** : les prompts système qui grossissent dégradent silencieusement la qualité LLM (source §7.4) ; l'écosystème a déjà KO-L001 (économie API) et des caches de verdicts — généraliser le pattern « verdict figé une fois, re-jeu sans re-appel » aux graders coûteux.
- **R3 — Diffusion compacte EXISTANTE (S4, à documenter)** : l'archive d'intégrité (45,5 Mio, round-trip SHA) couvre le besoin « un seul fichier transportable » — le documenter comme voie de diffusion officielle dans PM INSTALL §2ter (déjà partiellement le cas : « unique voie de diffusion » du PM).
- **R4 — Clonage allégé si besoin (S4)** : pour un dépôt qui grossit, `git clone --depth 1` / sparse-checkout (chemins skills/ + scripts/ uniquement) réduit le clone SANS changer la forme d'exécution — non disruptif, mesurable.
- **R5 — OO ciblée sur le code (S3)** : là où il y a du VRAI code exécuté souvent (arbitres, harnais), continuer les refactorings par petites passes (discipline refactoring-engineering + refactor-guard) — jamais de grande bascule.
- **R6 — Doctrine « noyau + LKM » à formaliser (S3, quasi gratuit)** : consigner dans SHARED §8 l'architecture implicite déjà réalisée (socle stable / modules chargeables / interfaces frontmatter / certification) — elle donne le cadre pour arbitrer toute future proposition d'architecture (la réponse à « faut-il compiler ? » devient un critère mécanique : tout ce qui casse la réparabilité module-par-module est rejeté).

### 6.1 Tableau de décision

| Option | Gain installation | Gain exécution | Gain #token (goulot réel) | Risque invariants (R2/R4) | Verdict |
|---|---|---|---|---|---|
| OOP intégral (réécriture) | nul | nul | nul | **critique** (casse tout) | **Rejeté** |
| Noyau compilé unique | **−5,7×** (pire) | **−10×** (pire) | nul | **critique** | **Rejeté** |
| R1 progressive disclosure | nul | nul | **direct, majeur** | faible (R2 append-only) | **Recommandé (priorité 1)** |
| R2 caches de verdicts | nul | nul | **direct** | faible | Recommandé |
| R3 archive de diffusion | +36 % transport | nul | nul | nul (existant) | À documenter |
| R4 clone allégé | + mesurable | nul | nul | nul | Optionnel |
| R5 OO ciblée scripts | nul | marginal | nul | maîtrisé (guard) | Au cas par cas |
| R6 doctrine formalisée | nul | nul | **indirect** (cadre d'arbitrage) | nul | Recommandé (quasi gratuit) |

## 7. Sources web (consultées le 2026-11-07)

1. **Refactoring AI Skills for Better Performance** (Doneyli De Jesus, LinkedIn) — pattern progressive disclosure : 20 lignes/skill + références à la demande, 1 156 lignes retirées à fonctionnalité égale. https://www.linkedin.com/top-content/artificial-intelligence/skills-for-the-ai-workforce/refactoring-ai-skills-for-better-performance
2. **A Comprehensive Survey on Agent Skills: Taxonomy** (2026) — agents = raisonnement/planification, skills = couches opérationnelles complémentaires. arxiv.org (via agrégateur).
3. **Building a Reusable Skills Ecosystem for AI Agents** (Medium) — Skills comme spécification ouverte : instruction + scripts + ressources découvrables.
4. **Prompt Sprawl: When System Prompts Grow** (2026-04) — les prompts système qui ballonnent (200 → 4 000 tokens) dégradent silencieusement la performance LLM ; audit + décomposition modulaire.
5. **Bundling Python Environments in a ZIP Archive** (shiv/zipapp, 2020-03) — premiers démarrages ralentis par le peuplement du cache ; et doc shiv : « executables created with shiv can outperform [PEX] » mais restent des artefacts de DIFFUSION.
6. **Prompt Cache** (arXiv 2311.04934) — réduction du coût de calcul des préfixes de prompts partagés (modules de prompts système réutilisés).
7. **Understanding the Linux Kernel** (Sysdig, 2026) + **Kbuild: the Linux Kernel Build System** — noyau monolithique + modules chargeables (LKM) : extension SANS recompilation ; Kbuild produit des configurations par cible.
8. **Modular vs monolithic vs microkernel** (StackOverflow 46410886 + littérature Mach/Hurd) — le choix monolithique-mais-modulaire de Linux contre la dérive micro-noyau tout-message.

## 8. Conclusion

Les deux idées propriétaires partagent une intuition juste — **l'architecture doit rester gouvernée et compacte** — et l'écosystème la réalise déjà par la voie correcte pour un runtime LLM : fichiers auto-contenus (≈ objets), frontmatter (≈ interfaces), KB (≈ registre de types), arbitres (≈ contrats), socle minimal chargé systématiquement (≈ noyau) et skills chargés à la demande (≈ LKM). La compilation en bloc unique est le seul des deux axes qui dégrade MESURABLEMENT les deux métriques qu'il vise (installation 5,7× plus lente, exécution 10× plus lente) ; la réécriture OOP ne touche pas le goulot réel (le budget #token) tout en cassant les invariants forensiques qui ont prouvé leur valeur (34+ disparitions capturées et réparées). **La priorité performance n° 1 est la progressive disclosure des SKILL.md lourds (R1), adossée à un arbitre de poids de chargement — tout le reste est soit déjà en place, soit optionnel.**
