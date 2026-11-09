# Historique par skill — agent-engineering

> Registre des versions et calibrages de `skills/agent-engineering/` — source de vérité : frontmatter SKILL.md + registre KB ; archive intégrale : `@historique/` (R4).

## v1.0.0 (2026-11-09, Task 83, session web-ecef7f80, directive 1a1beaee032b5aa5)

- **Matérialisation de la discipline n°56** (agent engineering) — forme **SKILL DISCIPLINE** choisie par l'agent (answer key D003 : directive verbatim « il sera défini en tant que "discipline" » + pattern écosystème disciplines = skills n°54 ×3 + n°55 ; agent .agent = exécutant spécialisé d'une tâche ; agent autonome = cycle A-H + État Long — knowledge-observer.agent v1.1.0 seul cas justifié à ce jour ; agent-engineering = méthode transverse de cadrage/routage sans état long propre ni exécution dédiée).
- **Contenu** : SKILL.md 16,3 Kio (§0 Contexte Système + Règle Zéro + §1 [mission · table 3 domaines ABE/AE/MASE · table routage 8 détenteurs · 6 règles opérationnelles · mémoire déléguée · cycle 6 étapes · fondements] + §2-§7 + §8 registre d'assignation décentralisé) · `references/fondements-academiques.md` (State of Agent Engineering LangChain 2026 · Building Effective Agents Anthropic 12/2024 · ABSE/Tropos · multi-agent research system Anthropic 06/2025 · Don't Build Multi-Agents Cognition 2025 · Patterns and problems Anthropic 08/2026) · `evals/trigger_evals.json` 7 cas (5 positifs + 2 négatifs disciplines voisines) + `evals/evals.json` miroir.
- **Cascade KO-L004 locale** : entrée KB `## agent-engineering v1.0.0` + 4 arêtes bidirectionnelles (gen-plan, fleet-engineering, autonomous-agent, agent-creator — « Utilisé par » enrichis, ajouts purs) + pin manifeste ECO_SKILLS integrity + ULTRA 13ᵉ voie (table §1 + ligne §3) + présent fichier CRÉÉ + projection hôte pipeline 55/55.
- **Baseline A2** : EN ATTENTE DE MESURE (voie mécanique + confirm 3 runs LLM à armer au QUOTA_OK — KO-L001 ; aucune baseline pré-écrite, R3).
- **Pendance structurée** : inscription socle SHARED §7 (table définitions + registre assignation, bump v1.7.37) + gen-plan §1.6/§3 (bump MINOR + cascade) — précédents v1.7.0 (n°54) et Task 7/8 (n°55), tâche dédiée.

- **Socle inscrit** (Task 84 G3, 2026-11-09 — directive 1a1bed51ccaf78f1 « continue », pendance P1 éteinte) : SHARED §7 (ligne définition + ligne registre d'assignation, v1.7.37) + gen-plan §1.6/§3 (v3.42.0, mobilisation déclarée à l'entrée KB) ; PM v3.42.0 généré (delta verrouillé scripts/delta-genplan-v3420.json), PM v3.41.0 archivé R4 (sceau f0a44d495519c3df…).

## v1.1.0 (2026-11-09, Task 86, session web-ecef7f80, directive 1a1bed51ccaf78f1 cadence 2 h tick 17:50)

- **Baseline A2 MESURÉE puis Description Optimization A10/A14** (extinction pendance R3) : mesure initiale 5/7 (voie mécanique + confirm 3 runs LLM au QUOTA_OK — 21/21 votes réels, nulls 0 ; harnais `scripts/task21-baseline-a2-all.py --skills=agent-engineering`) ; dérive : cas 6 [contrôle négatif fleet-engineering] faux positif 2 voies + cas 7 [contrôle négatif skill-creator/agent-creator] faux positif voie L.
- **Optimisation A10/A14** : clause « Contrôles négatifs assumés » en description frontmatter (route vers fleet-engineering / fabrique skill-creator-agent-creator) — M-safe prouvée par simulation préalable du stemmer arbitre V6 (hits cas 7 inchangés, positifs 1-5 inconstructibles) ; édition chirurgicale count==1 all-or-nothing, idempotence NO-OP ×2, +325 o (16 346 → 16 671 o) ; SKILL.md SHA 1e043b4f… → 5c65a8a7….
- **Re-mesure post-optimisation : 6/7** (21/21 votes réels, nulls 0) : cas 6/7 voie L corrigés NON×3 ; cas 7 conforme 2 voies ; **écart structurel consigné cas 6 voie M** (radical « agent » ∈ strong — limite arbitre V6, posture Tasks 81/82/85).
- **Cascade KO-L004** : KB v1.1.0 (en-tête + Description miroir + Dernière calibration) + evals.json note + présent fichier ; ULTRA regen ×2 (table versions, KO-L003 dérivation dynamique) ; SHARED §7 no-op (KO-L003 sans version figée) ; gen-plan §1.6 no-op (plancher >= v1.0.0 conforme).

## v1.1.1 (2026-11-09, Task 90, session web-ecef7f80, directive 1a1c1dde3f6d0021)

- **Corrections de consistance post-test $FACON** (écosystème comme entrée — audit T1.1.2, failles F1-F5 mesurées, règle d'or n°5) : F1 §5 staleness résorbé (« Baseline A2 : EN ATTENTE DE MESURE » → MESURÉE 6/7 Task 86, 21/21 votes réels) ; F2 §6 traçabilité v1.1.0 (Task 86) complétée + v1.1.1 (présente) ; F3 evals.json champ version 1.0.0 → 1.1.1 ; F4 doublon description « la discipline agent engineering la discipline agent engineering » supprimé (coquille — présente 2 arbres SKILL.md, absente KB : dérive miroir R4 résorbée par resynchronisation) ; F5 §2 « Pas de script propre en v1.0.0 » recalé.
- **M-safe F4 PROUVÉE par simulation préalable** (pattern Task 86) : suppression d'OCCURRENCES dupliquées (la/discipline = STOP-words stemmer ; agent/engineering présents ailleurs) → ensembles de radicaux stemmer arbitre V6 IDENTIQUES avant/après ; verdicts voie M sur les 7 cas inchangés (True×5 positifs · True cas 6 structurel consigné · False cas 7) — routage inchangé par construction.
- **PATCH** : corrections de contenu/consistance SANS changement de comportement — sémantique, routage et contrats inchangés.
- **Cascade KO-L004** : KB v1.1.1 (en-tête + Description miroir resynchronisée + Dernière calibration) + pin ECO_SKILLS integrity 1.1.1 + présent fichier + miroirs hôte→dépôt (pattern Tasks 83-86).
