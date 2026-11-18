# Carte des familles de l'écosystème Knowledge — orchestration, couplages mesurés, routage

**Horodatage : 2026-11-18** · Task 106 (directive trace `1a1efc61db496e75`) · Méthode : inventaire mécanique `scripts/task106-inventaire-familles.py` → `download/inventaire-familles-task106.json` (55 entrées KB, dépendances déclarées des frontmatters, agents `.agent` réels) + doctrine `agent-engineering` v1.1.1 + pattern prouvé `orchestrateur-tsi` v1.1.2. **Tous les couplages cités sont mesurés** (règle d'or n°5 — reproductibles par re-jeu du script).

## 1. La question posée, la réponse en une ligne

**« Regrouper par famille avec des agents orchestrateurs : bonne idée ? » — OUI au regroupement (il est déjà réalisé et capturé là où il paie) ; NON à la création de nouveaux agents orchestrateurs : l'écosystème est déjà intégralement orchestré par les bons détenteurs, et la mesure montre que le goulot n'est pas le routage mais le budget #token** (étude Task 70, campagne Task 105 : bootstrap mesuré 6 tours agent → consolidé à 1 tour ; chaque couche d'agent supplémentaire AJOUTE des lectures de contexte, elle n'en économise pas).

La bonne idée a donc été exécutée sous sa forme utile : **cette carte formalise ce qui manquait — la vue d'ensemble des familles et de leurs détenteurs d'orchestration** (personne ne pouvait voir d'un coup d'œil quelle famille est orchestrée par quoi).

## 2. Les 7 familles (membres réels, couplages mesurés, orchestration en place)

| Famille | Membres (KB) | Arêtes intra* | Détenteur d'orchestration (EXISTANT) | Type de mission |
|---|---|---|---|---|
| **F1 TSI/Traktor** (métier) | 6 — orchestrateur-tsi, tsi-architect, tsi-validator, multi-shift-architect, midi-doc-expert, analyse-doc-s4mk2 | **13 (la plus dense : 2,2/membre)** | **orchestrateur-tsi** (skill méthode + `agent-TSI.agent` exécution, pipeline P1-P6, micro-spécs, garde PASS) | pipeline multi-membres récurrent : concevoir → valider → documenter |
| **F2 Socle gouvernance** | 7 — gen-plan, correct-work, clone-chat, resource-monitor, knowledge-observer, skills-inventory, alias-eco | 12 | **gen-plan** E1-E15 (hub mesuré : **24 dépendances inverses**) + correct-work (12) ; agent-engineering n°56 en CADRE/ROUTE | gouvernance transverse : planifier → vérifier → journaliser |
| **F3 Création d'artefacts** (méta) | 10 — skill-creator, script-creator, agent-creator, correct-py, script-reviewer, script-mon-ecosysteme-infrastructure, pm-skill, version-management, audit-provenance, re-curation | 8 | **table de routage N2** de l'arbitre `check-tool-routing` (skill→skill-creator · script→script-creator · agent→agent-creator…) + lifecycle gouverné par gen-plan/correct-work | lifecycle d'artefacts : créer → corriger → relire → versionner → archiver |
| **F4 Disciplines d'ingénierie** (n°54-56 + 8 fondamentales + trio refactoring) | 15 — agent-engineering, context/loop/graph/harness/memory-engineering, spec-driven-development, refactoring-engineering, refactoring-test, refactor-guard, prompt-engineering, agent-prompt-engineering, fleet-engineering, autonomous-agent, inter-scripts | 10 | **SHARED §7 méthode-mère** (héritage gen-plan §1.6) + n°56 CADRE/ROUTE + **inter-scripts** pour les nœuds scripts/binaires | méthodes transverses héritées, chacune détentrice de son périmètre |
| **F5 Photo/CPE** (métier) | 4 — iphone17, iphone18, iphone19, dessin-technique | **0** | **aucun requis** — générations parallèles (17 = époque, 18 = courante, 19 = anticipée), le choix se fait par génération nommée par le propriétaire | pipeline CPE **mono-membre** : UNE génération par photo |
| **F6 Diffusion / portail** | 3 — vue-upload, livraison-garantie, ghorg-cmdr | 1 (livraison-garantie → vue-upload) | chaque membre **orchestre sa propre procédure** (livraison-garantie compose déjà les primitives vue-upload — zéro duplication R4) | procédures composées auto-portantes |
| **F7 Métier solo / composite** | 10 — cahier-des-charges, traduction-zh-fr, audio-metadata, cpp-analysis, resume-youtube, pdf-llm, fullstack-dev, skill-finder-cn, web-reader, web-search | 2 | aucun requis — solos, ou composites qui détiennent leur propre méthode (cahier-des-charges M1-M4 orchestre déjà ses 6 dépendances) | missions mono-membre |

\* arêtes de dépendances déclarées intra-famille (frontmatters, KB uniquement). Hors KB : outils plateforme (pdf, docx, pptx, xlsx, charts, LLM, VLM, ASR, TTS, image-*) — routés à la demande par gen-plan E5, hors périmètre des familles. Agents `.agent` réels : knowledge-observer, tsi-architect, agent-TSI (+ forme antérieure orchestrateur-tsi.agent archivée).

## 3. Matrice de routage consolidée (quelle demande → quel détenteur)

| Demande du propriétaire | Routage | Garde |
|---|---|---|
| Mission TSI de bout en bout (mapping : concevoir + valider + documenter) | **orchestrateur-tsi** (pipeline P1-P6) | verdict PASS tsi-validator avant documentation ; GO propriétaire avant livraison/push |
| Demande TSI mono-membre | routage DIRECT (tsi-architect / tsi-validator / multi-shift-architect / midi-doc-expert / analyse-doc-s4mk2) | non-substitution — l'orchestrateur ne se déclenche pas (économie de tokens) |
| Planifier/exécuter/surveiller toute tâche | **gen-plan** (E1-E15, modes, answer key) | E7-DISP, E8, profils ressource |
| Vérifier/certifier un livrable ou un projet | **correct-work** (16 checks, modes PROJET/CIBLE/--bloc) | agrégation pire-bloc, AVEUGLE Étape 5 |
| Créer un skill / script / agent | skill-creator / script-creator / agent-creator (routage N2 **arbitré mécaniquement** par check-tool-routing) | conventions frontmatter, evals, cascade KO-L004 |
| Tâche d'agents (flotte, mémoire, handoffs) | **agent-engineering n°56** CADRE → route vers fleet-engineering / memory-engineering / autonomous-agent / spec-driven-development | règle 1 « simple d'abord », **gate anti-flotte** (≈ 15×), traçabilité par agent |
| Coordonner des scripts inter-langages | **inter-scripts** (tri topologique Kahn, fan-out, daemon socket) | registre des nœuds, cycles détectés |
| Améliorer une photo / dessin technique | iphone18 (courant) / iphone17 (époque) / iphone19 (anticipé) / dessin-technique — **choix direct par génénom** | garde-fous photo G1-G7, presets §6 |
| Livrer un fichier au propriétaire | **vue-upload** (portail) ou **livraison-garantie** (boucle fermée avec verdict) | fenêtre --hold, verdict mécanique |
| Archiver l'historique d'une discussion | **clone-chat** (scellement S1-S8) | 0 secret (KO-L009) |

## 4. Pourquoi NE PAS créer un agent orchestrateur par famille (décision motivée)

1. **Règle 1 « simple d'abord »** (agent-engineering §1.4-1) : pas de système multi-agents tant qu'un workflow composé résout. Les familles F5-F7 sont à missions mono-membre ou auto-portantes : il n'existe AUCUNE mission traversant plusieurs membres qui ne soit déjà portée par leur propre méthode.
2. **Gate anti-flotte** (§1.4-2, Cognition 2025 / Anthropic 06/2025) : le coût d'une couche d'orchestration d'agents est mesuré à **≈ 15×** en tokens — non justifié ici : le seul périmètre multi-membres récurrent (TSI) A déjà son orchestrateur (F1, 13 arêtes intra — preuve vivante).
3. **R4 jamais dupliquer** : un orchestrateur des familles F2-F4 dupliquerait la gouvernance de gen-plan/correct-work (exactement le « second cerveau » refusé par la décision de forme d'orchestrateur-tsi §1.1-1, directive 2026-11-01, et par le refus d'agentisation du pipeline Tasks 102-103).
4. **Le goulot mesuré est le budget #token, pas le routage** (étude Task 70 : le vrai coût d'une session est le contexte LLM ; campagne Task 105 : l'optimisation validée = RÉDUIRE les tours/lectures — voie consolidée −83,3 % tours — pas ajouter des couches).

**Voie de révision (quand un futur orchestrateur deviendrait justifié)** — les critères mesurables du précédent TSI, tous requis : (a) famille ≥ 4 membres à couplage intra dense (TSI : 13 arêtes) ; (b) missions récurrentes traversant ≥ 3 membres dans un ordre stable ; (c) gardes spécialisées entre membres (ex. verdict PASS avant documentation) ; (d) volume de missions justifiant un État Long dédié. Toute future demande peut être tranchée par l'inventaire mécanique (re-jeu du script Task 106 — les seuils sont dans cette carte). Les 2 membres TSI réservés (traktor-function-expert, s4-hardware-expert) restent sous la garde anti-routage d'orchestrateur-tsi tant qu'ils ne sont pas créés.

## 5. Ce que cette carte change concrètement

- **Vue d'ensemble inexistante** : 55 entrées KB + 4 agents + plateforme, groupés en 7 familles avec leur détenteur d'orchestration — un point d'entrée unique pour répondre à « qui orchestre quoi ».
- **Routage consolidé** : la matrice §3 rassemble les routages jusqu'ici dispersés (matrice TSI §1.3, table N2 tool-routing, routage n°56 §1.3, E5) — sans créer de nouvelle couche : c'est une CARTE, pas un orchestrateur.
- **Décision d'architecture tranchée et traçable** : la question « un agent orchestrateur par famille ? » a désormais une réponse motivée, mesurée et réversible (critères §4), réexaminable à tout moment par re-jeu de l'inventaire.
