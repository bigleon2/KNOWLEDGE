# Analyse conversions Task 82 — Skills ↔ Agents ↔ Agents autonomes + PMs → ULTRA

> **Livrable G1 — Task 82** (directive trace `1a1be717bb0fbdb1`) · Horodatage : 2026-11-09T04:15:00Z
> Méthode : inventaire mécanique `scripts/task82-inventaire.py` (71 skills, 3 agents `.agent`, 0 agent autonome déployé, 9 corpus `@mon-ecosysteme`, 5 corpus `@photos`, 6 prompts `@Bibliotheque-skills-Multi-IA` — JSON : `scripts/task82-inventaire.json`) + critères explicites dérivés des doctrines tracées (tandem tsi-architect · format .agent `autonomous-agent/references/agent-format.md` · doctrine ULTRA 2026-10-02 tracée dans `gen-ultra-maitre.py`) · règle d'or n°5 : données mesurées, jamais d'étiquettes.

## §1 — Critères par axe (explicites, avant examen des candidats)

| Axe | Critère de conversion | Anti-critères (non-conversion) |
|-----|----------------------|-------------------------------|
| **Skill → Agent (tandem)** | couche d'EXÉCUTION spécialisée procédurale (non-portable en script) ≥ 8 Kio, réutilisée à travers missions/éléments, séparation méthode/exécution nette, bénéfice d'un contrat versionné séparé | exécution déjà portée par des scripts (le code EST l'exécuteur) ; méthode pure (la valeur EST la méthode) ; frontière de confiance (arbitres) ; couplage verrouillé (R2) |
| **Skill → Agent autonome** | cycle persistant INTER-SESSIONS déjà opéré (État Long existant mesuré : `data/`, journal), pipeline multi-étapes récurrent, modes stables, invocation automatique récurrente | one-shot par session ; exécution scriptée ; persistance inexistante |
| **PM → Prompt ULTRA maître** | **doctrine propriétaire 2026-10-02 tracée dans le générateur** : « PAS de conversion des PMs existants en monolithes (R4 duplication / R2 corpus figé / KO-L004 drift) » — l'ULTRA est un orchestrateur LÉGER dérivé dynamiquement du corpus ; la régénération EST le recalibrage | tout monolithe ; toute duplication d'un PM dans l'ULTRA ; la voie d'édition sanctifiée = « éditer le script puis régénérer » |
| **Agent → Skill / Agent autonome** | agent one-shot sans état (le tandem n'apporte rien) OU agent dont la mémoire n'est jamais écrite (État Long mort) | tandem sain et actif (méthode skill + exécution agent) ; membre actif d'une famille orchestrée |
| **Agent autonome → Agent / Skill** | mémoire 2 niveaux inutilisée, pipeline jamais rejoué, modes théoriques | (population nulle ⇒ a fortiori) |

## §2 — Population mesurée (extrait inventaire)

- **Skills** : 71 (dont ~68 racine écosystème). Usage worklog réel : correct-work **412** · gen-plan **334** · clone-chat 140 · version-management 139 · re-curation 107 · iphone19 40 · dessin-technique 28 · pm-skill 27 · tsi-validator 25 · alias-eco 24 · inter-scripts 20 · orchestrateur-tsi 19 · knowledge-observer 15.
- **Poids écosystème** : iphone18 41 395 o · skill-creator 41 323 · iphone19 40 431 (curé −27,3 %) · iphone17 35 013 · cahier-des-charges 31 583 · gen-plan 30 697 (15 references/) · correct-work 29 331 · version-management 25 783 (curé) · analyse-doc-s4mk2 19 951 · re-curation 19 450.
- **Agents `.agent` réels** : 3 — `tsi-architect.agent` (4 869 o, tandem déclaré SKILL.md §délégation) · `orchestrateur-tsi.agent` (6 851 o) · `agent-TSI.agent` (7 348 o, membre de flotte TSI). Gabarits (NON déployés) : `autonomous-agent/references/autonomous-agent.agent`, `agent-creator/references/agent-creator.agent`.
- **Agents autonomes déployés** : **0**.
- **Skills avec État Long existant (`data/`)** : **knowledge-observer uniquement** (`data/lessons-learned.json`, 1 fichier — journal des lessons).
- **Corpus PM** : 9 fichiers `@mon-ecosysteme` (GEN-PLAN 222 074 o · INSTALL 52 032 · SHARED 52 913 · CORRECT-WORK 51 621 · CLONE-CHAT 34 882 · README 26 668 · REFACTOR-GUARD 27 108 · SYNC-CONTEXT 20 936 · ULTRA 7 950).

## §3 — LISTE « cibles-to-agent » (skills à convertir en agents ou agents autonomes — triée par priorité)

### ✅ P1 — knowledge-observer → **AGENT AUTONOME** (tandem 2 couches)

**Justification mesurée** — knowledge-observer (v1.0.0, 6 368 o, 15 usages worklog) est le seul skill de l'écosystème qui IMPLÉMENTE DÉJÀ l'architecture complète d'un agent autonome, mais dans un fichier de skill :
1. **Cycle A-H (§1.2)** = exactement le pipeline 8 étapes A-H du format `.agent` (`autonomous-agent/references/agent-format.md` — codes A-H, modules, `verification: true`) ;
2. **Modes M1-M4 (§1.3)** = les 4 modes du format `.agent` (OBSERVATION/ANALYSE/PROPOSITION/APPLICATION) ;
3. **`data/lessons-learned.json`** = un **État Long persistant inter-sessions déjà opéré** (règle de persistance du format : « l'État Long est persisté… à la fin de chaque pipeline ») ;
4. **Invocation automatique** par gen-plan à E15 (M1-M2) = exécution autonome récurrente tracée (334 usages gen-plan, 15 usages directs) ;
5. **Garde-fous §1.4** = gardes de l'agent (validation correct-work obligatoire étape F — jamais d'auto-modification non validée).

La conversion formalise ce qu'il est déjà : porteur `.agent` conforme au format (mémoire 2 niveaux, modules, modes, pipeline) + SKILL.md restructuré en tandem (« la méthode ici, l'exécution dans l'agent » — pattern écosystème R4, précédent tsi-architect Task 26+). **Bénéfice** : État Long normalisé (chemin, schéma, règles de persistance), pipeline vérifiable mécaniquement, la population « agents autonomes » de l'écosystème passe de 0 à 1 avec un canon conforme, et l'invocation E15/gen-plan reste identique (R2 — interface inchangée, description ADDITIVE).

### ❌ Évalués et NON retenus (motifs mesurés — extraits)

| Candidat évalué | Verdict | Motif (anti-critère) |
|---|---|---|
| correct-work (usage 412) | NON | **Arbitre de confiance** — son exécution mécanique est déjà portée par `verify-correct-work.py` (16 checks) ; un `.agent` n'apporterait rien et déplacerait la frontière de confiance |
| gen-plan (usage 334) | NON | Méthode maîtresse d'orchestration — convertie, elle cesserait d'être le point d'entrée « méthode » que correct-work exige à son Étape 1 (couplage tracé ULTRA §5) |
| clone-chat (140) | NON | Générateur one-shot par session (7+1 étapes, scellement S1-S8) — pas d'État Long inter-sessions |
| version-management (139) / re-curation (107) | NON | Méthodes + harnais scriptés (`protocole-test.py`) — l'exécution est le harnais, la méthode est le contrat |
| analyse-doc-s4mk2 (19,9 Kio) | NON | Exécution déjà portée par 4 scripts Python (`analyser_tsi_mk2.py`…) + `tests/run_all.py` — le code est l'exécuteur (R4 : un `.agent` dupliquerait) |
| dessin-technique (28) | NON | Exécution portée par daemon C++ `trigo-euler` + 4 scripts Python + registre inter-scripts |
| cahier-des-charges (31,6 Kio) | NON | Méthode M1-M7 — la valeur EST la méthode (CDC 12 sections, EF-xx) ; 2 scripts portent déjà M7 |
| iphone17 / iphone18 / iphone19 | NON | Pipelines CPE **sources PM @photos** (convention v0.9→v0.12 : PM source → projection SKILL.md) — une restructuration tandem casserait la convention de projection R2 ; la voie sanctifiée est la re-curation (G5-G6) |
| resource-monitor | NON | Sondage léger couplé par contrat à gen-plan E6/E9-E14 (D004-P7) — R2 : l'interface d'invocation est verrouillée |
| livraison-garantie | NON | Boucle bornée scriptée (`livraison_garantie.py`, fenêtre --hold, verdict machine CONFIRME/PARTIEL/AUCUN) |
| skills-inventory, pm-skill, alias-eco, traduction-zh-fr, audio-metadata, resume-youtube, gif-animator(-pro), inter-scripts, vue-upload, ghorg-cmdr, audit-provenance | NON | Exécution portée par scripts (le code est l'exécuteur) |
| skill-creator, script-creator, script-reviewer, agent-creator, autonomous-agent, agent-prompt-engineering, prompt-engineering | NON | Fabriques/méthodes de création — ce sont les DÉFINISSEURS du format, pas des exécuteurs |
| disciplines n°50-55 (context/loop/graph/harness/fleet/memory/spec-driven), refactoring trio, refactor-guard | NON | Méthodes disciplinaires à arbitres scriptés (risk_score.py, refactoring-test-graph.py…) |
| plateformes SDK (ASR, TTS, VLM, LLM, image-*, video-understand, web-*, charts, pdf, docx, pptx, xlsx, fullstack-dev) | NON | Hors périmètre tandem : skills plateforme structurés `references/`+`scenes/` natifs |

**LISTE FINALE cibles-to-agent : [knowledge-observer → agent autonome (P1)]**

## §4 — LISTE « cibles-to-ultra-maitre » (PMs à convertir en prompt ultra maître — triée par priorité)

**Verdict : LISTE VIDE — aucun PM à convertir en monolithe.**

**Doctrine opposable (propriétaire 2026-10-02, tracée dans `gen-ultra-maitre.py` en-tête + ULTRA §Directive)** : « au lieu de convertir les prompts maîtres existants en monolithes enrichis (**rejeté — R4 duplication, R2 corpus figé, KO-L004 drift**), ce script GÉNÈRE un ultra-PM orchestrateur LÉGER dont tout le contenu est DÉRIVÉ dynamiquement de l'état réel ». La conversion PM→ULTRA est donc **déjà effective par conception** pour les 9 fichiers du corpus :
- PM GEN-PLAN (222 074 o — le plus gros artefact vivant : un monolithe ULTRA le dupliquerait intégralement, violation R4 maximale) — membre par dérivation (ULTRA §2, §3) ;
- PM CORRECT-WORK, PM CLONE-CHAT, PM REFACTOR-GUARD — membres par dérivation (§2) ;
- PM SHARED + PM INSTALL-ECOSYSTEME — socle + source unique d'installation (§2, §4) ;
- 6 prompts plateforme `@Bibliotheque-skills-Multi-IA` — projections PAR PLATEFORME (gemini, qwen, claude, perplexity, chatgpt, copilot) générées par `tools/generate_prompts.py` — les convertir dupliquerait l'ULTRA (R4) ;
- 3 PM sources `@photos` (iphone17/18/19-photos.md) — sources R2 des skills photo (le PM source fait foi pour les preuves R4), pas des orchestrateurs.

**Lacune réelle détectée (action associée, exécutée en G2)** : la table de routage §1 de l'ULTRA (9 lignes) ne route **aucune** demande de **re-curation progressive disclosure** (« re-curé X », « divulgation progressive » — skill v1.2.1, 107 usages, campagne en cours G5-G6), ni la **création de skills** (skill-creator), ni l'**inventaire** (skills-inventory). L'orchestrateur ultra-maître rate des lanes à usage établi. Voie sanctifiée : **éditer `ROUTING` dans `gen-ultra-maitre.py` puis régénérer** (l'en-tête du fichier l'exige : « ne pas éditer à la main ; éditer le script puis régénérer »). C'est le recalibrage ULTRA = la « conversion » au sens de la doctrine (régénération = recalibrage KO-L004).

**LISTE FINALE cibles-to-ultra-maitre : [] (vide — conversion déjà effective par dérivation) + ACTION recalibrage : extension du routage ULTRA (3 lanes : re-curation, création de skills, inventaire) via le générateur.**

## §5 — LISTE « cibles-agent-to-X » (agents à convertir en skills ou agents autonomes — triée par priorité)

**Verdict : LISTE VIDE — les 3 agents réels sont sains, actifs et conformes.**

| Agent | Audit | Verdict |
|---|---|---|
| `tsi-architect.agent` v1.1.0 (4 869 o) | Tandem 2 couches canonique (SKILL.md détient la méthode + délégation déclarée ; agent détient l'exécution spécialisée : modes M1-M4, gardes AG-3, État Long « allocations MIDI + leçons ») — actif (famille TSI, validation tsi-validator couplée) | **NON — aucune conversion** (le convertir en skill supprimerait la couche d'exécution ; en autonome : dupliquerait la mémoire de famille que orchestrateur-tsi coordine déjà) |
| `orchestrateur-tsi.agent` (6 851 o) | Orchestrateur de la famille TSI (route, spécifie, arbitre, agrège — description skill homonyme) — actif | **NON — aucune conversion** (c'est un orchestrateur, pas un exécuteur) |
| `agent-TSI.agent` (7 348 o) | Membre de flotte TSI (ORCHESTRÉ PAR agent-TSI, multi-agents par mission) — actif | **NON — aucune conversion** (membre actif de la flotte) |

**LISTE FINALE cibles-agent-to-X : [] (vide — audit 3/3 sain).**

## §6 — LISTE « cibles-agent-auto-to-X » (agents autonomes à convertir en agents ou skills — triée par priorité)

**Verdict : LISTE VIDE par vide de population.** Aucun agent autonome n'est déployé en production (les 2 `.agent` de `references/` — `autonomous-agent.agent`, `agent-creator.agent` — sont des **gabarits de format**, doc du format, pas des agents). Après G2, `knowledge-observer.agent` deviendra le premier agent autonome déployé (venant d'un SKILL via cibles-to-agent — pas d'un agent autonome existant). A fortiori : rien à reconvertir.

**LISTE FINALE cibles-agent-auto-to-X : [] (vide — population 0 avant conversion).**

## §7 — Synthèse : conversions à exécuter en G2 (et uniquement celles-ci)

1. **P1 — knowledge-observer → agent autonome** : création `skills/knowledge-observer/knowledge-observer.agent` conforme au format (nom, objectif, version alignée 1.1.0, modes M1-M4, gardes §1.4, règles, inputs/outputs, mémoire court [session observée] / long [`data/lessons-learned.json`, persistence file], pipeline A-H avec modules + verification, sécurité no_hallucination/validation obligatoire) + SKILL.md v1.0.0 → **v1.1.0** restructuré en tandem (ajouts purs — description ADDITIVE inchangée, R2 triggers) + cascade version complète (KB `## knowledge-observer v1.1.0` + Dernière calibration + pin ECO_SKILLS + `@historique/historiques-par-skill/knowledge-observer.md` CRÉÉ + ULTRA régénéré + archive rescellée hôte+dépôt + integrity 112/112 + arbitres 5/5 + miroir même passe 54/54).
2. **Recalibrage ULTRA (axe ultra-maître)** : extension `ROUTING` de `gen-ultra-maitre.py` (3 lanes : re-curation / création de skills / inventaire) + régénération idempotente + `--check`.
3. Aucune autre conversion (listes §4-§6 vides, motifs documentés §3).

**Garantie de non-régression (directive : « écosystème $FACON2 n'ayant subi aucune régression »)** : toutes les conversions en ajouts purs (R1/R2 : rien de rétrogradé, description frontmatter verbatim, evals inchangés) ; R4 (zéro duplication byte : le .agent porte l'exécution sous sa forme opérationnelle, le SKILL.md la méthode — précédent tsi-architect) ; tests G3 avant le CW --bloc #1.
