#!/usr/bin/env python3
# PROVENANCE: Task 22 (2026-10-23, session web-fdf5963c) — directive propriétaire
# gen-plan(step) item 3 : « disciplines et techniques » (périmètre étendu : skills
# et agents tagués « discipline ») — application des apports de veille 2025-2026.
# Méthode : insertions CHIRURGICALES (une sous-section §1.9bis par SKILL.md, avant
# « ## §2 »), bump semver MINOR/PATCH, recalibrage KO-L004 (ECO_SKILLS arbitre +
# KB en-tête + bullet calibration). Échec si 0 match (garde anti-faux-succès,
# leçon Task 17). Idempotence ×2 (re-run = 0 modification).
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SK = REPO / "skills"
KB = SK / "KNOWLEDGE.md"
ARB = REPO / "scripts" / "check-ecosysteme-integrity.py"

TITRE = "### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)"

# skill -> (ancienne version, nouvelle version, contenu §1.9bis)
APPORTS = {
"spec-driven-development": ("1.0.1", "1.1.0", """
**M1.5 CLARIFIER** (Spec Kit `/clarify`) : avant M2 DÉCOMPOSER, poser 3-7 questions ciblées sur les ambiguïtés et cas limites détectés dans la spécification (hook candidat : gen-plan E4). **Rebuild test** (critère de complétude) : la spec seule doit permettre de reconstruire le livrable — si un détail manque, la spec est incomplète. **Garde de granularité anti-overhead** : SDD est réservé aux tâches complexes ou non réversibles ; micro-tâche et prototype → micro-spec ≤ 3 lignes ou pas de spec (l'overhead démontré : un bug fix traité en 4 user stories et 16 critères ; Tessl 2026 : SDD overkill pour les prototypes). **Conflits documentés** : SDD ne remplace PAS le TDD — les équipes matures les combinent (spec pour le QUOI, tests pour le VÉRIFIÉ) ; modèle hybride avec l'agilité (stories légères pour le flux, spec contractuelle pour périmètre/acceptation) ; remède « spec-poussière » = re-validation de la spec après chaque dérive (hooks d'événement à la Kiro). Sources : arXiv 2602.00180 « From Code to Contract » · github.com/github/spec-kit · kiro.dev/docs/specs · martinfowler.com (SDD-3-tools).
"""),
"cahier-des-charges": ("1.0.0", "1.1.0", """
**M3 grille anti-ambiguïté** : passage détecteur des termes non testables (« rapide », « fluide », « simple », « facile ») — les prompts structurés améliorent la classification d'ambiguïté de +20,2 % (étude industrielle Raj 2025). **M3 scan d'exigences manquantes** : le détecteur propose les EF/ENF omises par l'élicitation humaine (ESEM 2026), marquées `[HYP-xx]` et soumises au propriétaire — jamais inscrites sans attribution explicite. **Format EARS optionnel** pour les EF : « Quand <déclencheur>, le système doit <réponse> » (Kiro) — quasi-exécutable, pont direct vers les critères d'acceptation mécaniques. **Articulation agilité** : modèle hybride recommandé (stories légères pour le flux, CDC contractuel pour périmètre/acceptation) ; l'anti-pattern SRS exhaustif monolithique est documenté (risque MDD — Fowler). Sources : arxiv 2509.11446 · drops.dagstuhl.de ESEM 2026 · kiro.dev/docs/specs · mountaingoatsoftware.com.
"""),
"prompt-engineering": ("2.2.0", "2.3.0", """
**Catalogue technique → cas d'usage** : CoT (raisonnement multi-étapes) · self-consistency (réduction de variance par vote N chemins — prototype des 3 runs de confirm des baselines A2) · least-to-most (décomposition progressive) · plan-and-act (plans long-horizon, arXiv 2503.09572) · JSON-schema (sortie vérifiable — > 99 % d'adhérence avec validation + retry). **Couplage itération ↔ evals mesurés** : la boucle d'itération §1.5 s'ancre sur une métrique objective (trigger_evals, baselines A2) — itérer sans métrique optimise du bruit ; le cap 3 itérations est inchangé ; la grille §1.4 demeure l'outil d'audit. **Règle « artefact générable = schéma + check déterministe »** (arXiv 2601.22025) : tout artefact générable (plan, verdict, answer key) s'accompagne d'un check mécanique — alignement sur la philosophie arbitres de gen-plan. **Veille prompt-as-code** (APE, OPRO, DSPy+GEPA) : horizon d'automatisation de l'optimisation, applicable dès que les evals sont mesurés ; le métier migre vers eval engineering + context engineering (non-duplication SHARED §7 respectée). Sources : platform.claude.com prompt-eng best practices · arxiv 2503.09572 · arxiv 2601.22025 · arize.com GEPA.
"""),
"context-engineering": ("1.1.0", "1.2.0", """
**Just-in-time retrieval en principe M1** (Anthropic 2025) : charger des POINTERS légers (chemins, requêtes, ID) au moment de l'étape concernée plutôt qu'intégralement en amont ; la lecture intégrale devient l'exception motivée (cohérence budget d'attention + resource-monitor). **Hygiène KV-cache** (Manus) : préfixe de contexte stable, journal append-only, pas de timestamps volatils en tête — le cache coûte ~10× moins que le re-calcul. **Anti « Governance Decay »** (arXiv 2606.22528) : la compaction efface silencieusement les contraintes de gouvernance — après CHAQUE compaction, ré-énoncer les invariants critiques (règle zéro, contraintes propriétaire) en tête du contexte compacté, et consigner un tombstone pour toute contrainte évacuée. **Références** : Anthropic « effective context engineering » (09/2025) · ACE arXiv 2510.04618 (le plan complexe = playbook évolutif à deltas incrémentaux — complémentaire de gen-plan) · Claude Cookbook 03/2026 (les stratégies se composent : mémoire + compaction + purge d'outils).
"""),
"memory-engineering": ("1.1.1", "1.2.0", """
**Ops update/forget/consolidate de première classe** (AgeMem, ACL 2026 — opérations mémoire exposées comme outils) : l'append-only demeure la règle d'écriture, mais l'oubli contrôlé devient une opération légitime — tombstone daté pour toute règle contredite, rollback versionné pour toute rétraction (l'EL non administré devient bruit + surface d'attaque — MemoryAgentBench). **Gouvernance des écrits** (survey « Memory in the Age of AI Agents », arXiv 2512.13564) : ranger chaque écrit par sa nature — KB = mémoire factuelle, worklog = mémoire expérientielle, scratchpad = mémoire de travail. **Validation Letta 2025** : la mémoire filesystem (recherche agentic de fichiers) est compétitive avec les bases vectorielles — conforte le choix KB/worklog-as-files de l'écosystème. **Contre-mesure budgétaire** : le « budget d'attention FINI » est lié au signal #token de resource-monitor (cross-ref dependencies) — une écriture sélective coûte moins cher qu'une relecture intégrale. Sources : arXiv 2601.01885 AgeMem · arXiv 2512.13564 · letta.com benchmark 08/2025.
"""),
"fleet-engineering": ("1.0.1", "1.1.0", """
**Règle 0 — gate anti-flotte** (Cognition « Don't Build Multi-Agents » 2025, reconfirmé 04/2026) : une flotte est INTERDITE si (a) les tâches sont séquentielles à écritures entrelacées, ou (b) le ratio de coût ~15× tokens du multi-agent (Anthropic 06/2025 : agents ≈ 4×, multi-agents ≈ 15× vs chat) n'est pas justifié par un périmètre large parallélisable ; sous-tâches en lecture seule/indépendantes = zone verte. **M5 swarm durci** (Anthropic « Patterns and problems in emerging multiagent systems », 08/2026 — coordination failures, collusion, sabotage documentés) : journaliser qui-a-décidé-quoi PAR agent ; quota strict maintenu. **Ordre de routage E5/E7** (neutralise les conflits de périmètre) : (a) tâche séquentielle → 1 agent autonome (autonomous-agent) ; (b) parallélisable/indépendant → flotte M1-M5 ; (c) nœuds scripts/binaires → inter-scripts ; (d) création d'agents réutilisables → agent-creator. **Échecs de handoff** : la majorité des échecs multi-agents sont des pertes de contexte au handoff — la micro-spéc par sous-tâche (liaison spec-driven) est la parade citée. Sources : cognition.com/blog/dont-build-multi-agents · anthropic.com/research/multiagent-systems · anthropic.com/engineering/multi-agent-research-system.
"""),
"loop-engineering": ("1.1.0", "1.2.0", """
**Calibration des graders agentiques (M2)** : avant tout usage d'un grader agentique dans une boucle — échantillon golden de verdicts attendus, accord ≥ 80 % avec la voie mécanique exigé, juge ≠ rédacteur, ordre des cas randomisé (anti-biais positionnel/self-preference). **Critères d'arrêt quantifiés** : toute boucle porte (a) un max d'itérations N, (b) un plateau (gain marginal < ε sur 2 cycles consécutifs → arrêt), (c) une escalade propriétaire ; le hash des graders est scellé AVANT le run — toute modification du grader en cours de boucle est un signal de reward hacking (TRACE, arXiv 2601.20103) et invalide les verdicts. **Vérification intermédiaire** (VPR — Verifiable Process Rewards, arXiv 2605.10325) : un grader léger par étape (contrôle de convergence en cours de route) réduit le coût des échecs découverts tardivement — la vérification unique en fin de phase demeure le filet, pas le seul point de contrôle. **Limite documentée** (« The Limit of RLVR ») : itérer sans changer de méthode améliore l'efficacité d'échantillonnage, pas la capacité — une boucle qui ne converge pas exige un changement de méthode, pas plus d'itérations.
"""),
"harness-engineering": ("1.1.0", "1.2.0", """
**Mode checkpoint/reprise (M1)** (Anthropic « effective harnesses for long-running agents », 11/2025) : sérialiser l'état de session à chaque phase (snapshots tar, fichier d'état JSON daté) pour reprendre après interruption/timeout sans re-exécution intégrale — pattern des snapshots Task 18 ; le checkpoint est un artefact d'état : déterministe ou exclu du périmètre projeté (leçon Task 20). **Budget de resserrage** : tout nouveau check doit être idempotent ET documenté (quoi, pourquoi, coût) ; revue périodique des checks dormants/redondants avec archivage en _archive/ — le harnais doit rester mince, sinon il devient lui-même la dette (90+ checks sans revue = friction permanente). **Frontière du vocabulaire** (table commune avec loop-engineering) : ARBITRE = script stdlib déterministe du dépôt (verdict machine, pas de LLM) ; GRADER = mécanique OU agentique d'évaluation, calibré selon loop-engineering M2 ; les deux sont des points de contrôle du harnais, seuls leurs moyens diffèrent.
"""),
"graph-engineering": ("1.0.1", "1.1.0", """
**Arêtes bi-temporelles** (Graphiti/Zep, arXiv 2501.13956) : chaque arête porte `valid_from` (version d'intégration) et, au remplacement, une INVALIDATION DATÉE au lieu d'un retrait — compatible R2 (on n'efface jamais, on invalide) ; les requêtes « état à la version N » deviennent possibles sans @historique consulté hors graphe. **Arbitre de divergence KB ↔ frontmatters** : les arêtes déclarées deux fois (registre KB + blocs dependencies YAML) doivent diverger JAMAIS — une seule source fait foi, l'autre est dérivée ; un diff mécanique périodique remonte toute asymétrie (extension verify-cross). **Pondération d'arêtes par usage récent** : fréquence d'invocation (#token, dates de calibration) oriente la sélection E5 — les nœuds chauds remontent, les dormants s'estompent ; un résumé par catégorie dans la KB (style résumés de communautés GraphRAG) accélère la navigation sans requête exhaustive. Sources : arXiv 2501.13956 · github.com/getzep/graphiti · github.com/openspg/kag.
"""),
"refactor-guard": ("1.7.1", "1.8.0", """
**Golden master AVANT (renforcement R5)** : avant TOUTE modification, capturer et sceller les sorties baseline (n ≥ 3 runs — entrées nominales + edge cases), puis les rejouer en sandbox ET post-vol ; la preuve comportementale (sorties identiques) remplace le simple hachage avant/après, qui ne prouve rien si les entrées varient. **Mutation testing léger (sandbox)** : avant de considérer une validation acquise, modifier 1 opérateur/constante de la cible et exiger qu'au moins 1 test échoue — une suite qui reste verte sur une mutation prouvée est déclarée INSENSIBLE (anti faux-verts ; tests qui testent le testeur). **Rollback armé (N5)** : en canary, la violation d'un contrat (latence/CPU/mémoire) déclenche le rollback AUTOMATIQUEMENT armé + signalement propriétaire — « rollback testé » ne suffit plus ; détection de contournement de tests dans les journaux (héritage TRACE). Sources : Rackspace/CircleCI progressive delivery 2026 · characterization tests · arXiv 2601.20103.
"""),
"refactoring-test": ("1.0.2", "1.1.0", """
**Co-changes git (change coupling — CodeScene)** : en complément des arêtes déclaratives (KB + dependencies YAML), M3 peut déduire des arêtes EMPIRIQUES de l'historique git — fichiers modifiés ensemble ≥ k fois = couplage réel que les déclarations manquent ; le blast radius déclaratif seul sous-estime l'impact. **Blast radius pondéré** : nœud pivot (centralité forte — arbitres, KB, SHARED) = poids ×2 ; calibration des seuils OK/PRESSION/CRITIQUE sur l'historique des verdicts (mesure, pas a priori — les seuils fixes 4/7, 4/8 ne sont que des points de départ). **Isolation de contexte maker/checker** : l'indépendance refactoring-engineering (maker) / refactoring-test (checker) devient une CONDITION VÉRIFIABLE de validité du verdict — session séparée, mémoire non partagée, l'exécutant sans accès au raisonnement de l'évaluateur (« two AI agents do not give you four eyes ») ; sans isolation, le verdict est consigné « non validable quatre yeux ». Sources : codescene.com · zenn.dev maker-cannot-be-checker 07/2026 · moderne.ai.
"""),
"resource-monitor": ("1.0.0", "1.1.0", """
**2 indicateurs nouveaux (F1-F6)** : dérive d'effort (tokens/étape vs baseline de session — détecte le ×2 silencieux des workers héritant d'un effort haut à output égal) ; taux de hit cache/préfixe (dégradation = dérive de préfixe de contexte — Datadog 09/2026). **429 : anti retry-storm** (Kong/Maxim/Palo Alto 2026) : la recommandation émet `action: backoff_exponentiel` + circuit breaker (arrêt après N échecs consécutifs) — les retry storms déplètent le budget token qu'ils prétendent économiser ; instrumente la leçon KO-L001 (sonde unique, cadence polie). **Downgrades par effort assigné** (pattern Anthropic lead-agent) : option `--task-weights` — PARALLELE_REDUIT/SERIE choisissent d'abord les tâches à faible effort assigné, pas par largeur seule (un downgrade largeur-seule anéantit les gains démontrés du parallélisme : latence ÷2, 90,2 %). **Hystérésis + envergure prédictive** : verdicts anti-flapping (OK↔PRECISION exige un franchissement persistant) + projection « budget restant ÷ étapes restantes » en plus des seuils réactifs — le monitoring passe de réactif à prédictif.
"""),
"autonomous-agent": ("1.1.0", "1.2.0", """
**Étape G2 RE-PLANIFICATION** (entre G et H — pattern plan-and-execute) : si la vérification G échoue → retour au mode M1 avec diagnostic d'échec (max 2 itérations, puis escalade) ; sans transition définie, un échec de vérification laisse l'agent sans issue. **Politique d'oubli/rollback EL** : budget d'EL (taille max), purge des règles contredites (tombstone daté), rollback versionné du .agent — l'EL non administré devient bruit + surface d'attaque (MemoryAgentBench, arXiv 2507.05257 ; lifecycle Write/Store/Retrieve/Execute/Share/Forget). **Machine à états explicite** : matrice de transitions de modes (M1→M2→M3→M4→G→G2→H) consignée — l'exécution autonome sans machine à états dérive silencieusement. Sources : arXiv 2507.05257 · langchain.com/blog/planning-agents · mastra.ai/articles/langgraph.
"""),
"inter-scripts": ("1.0.0", "1.1.0", """
**Retry/timeout au schéma de plan** (primitives Airflow/Temporal/Orkes — pas des options) : champs optionnels par tâche `timeout_s`, `max_retries`, `backoff_s` ; la clé d'idempotence = Task ID journalisée (re-jeu sûr après échec partiel). **Heartbeat daemon** : re-vérification `echo` AVANT chaque tâche du niveau + re-démarrage paresseux si socket morte — un socket détecté mort à mi-plan ne doit pas coûter l'échec de la tâche (health-check au seul démarrage = insuffisant). **Validation de schéma du registre** : `registre.json` validé au chargement (champs requis : nom, langage, interface, capacités) — un registre malformé est rejeté avec verdict, pas interprété à tolérance. **Socket UNIX 0600** : permissions consignées. **Table de correspondance A2A/MCP** (documentation seule — zéro dépendance) : registre ≈ Agent Card (capacités découvrables), tâche ≈ Task lifecycle, sortie typée ≈ Artifact ; le vocabulaire standard simplifie les échanges inter-écosystèmes. Sources : orkes.io idempotency · airflow best-practices · auth0.com mcp-vs-a2a.
"""),
"agent-prompt-engineering": ("1.0.1", "1.1.0", """
**read_when frontmatter** : rétabli (le 1/94 manquant de la normalisation Task 28) — différenciation du périmètre vs prompt-engineering : APE = artefacts D'AGENTS (SKILL.md de skills, prompts de sous-agents, hooks, outils) ; prompt-engineering = artefacts de prompts gouvernés (PMs, corpus). **Progressive disclosure** (Anthropic Agent Skills, 10/2025 — standard ouvert) : description frontmatter = déclencheur dense chargé au départ ; corps = instructions ; `references/` = détails chargés À LA DEMANDE — fenêtres de contexte courtes, déclencheurs fiables, bibliothèque scalable. **Altitude des system prompts** (Anthropic « effective context engineering », 09/2025) : langage simple et direct ; durabilité > micro-gestion des étapes (assez détaillé pour guider, assez durable pour survivre aux variations de modèle) ; sections persona/limites/outils séparées. **Contexte d'agent** (renvoi — non-duplication SHARED §7) : compaction, note-taking, just-in-time → context-engineering. Sources : anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills · anthropic.com/engineering/effective-context-engineering-for-ai-agents.
"""),
}


def bump_skill_version(text, old, new, skill):
    pat = re.compile(r"^version:\s*[\"']?%s[\"']?\s*$" % re.escape(old), re.M)
    ms = pat.findall(text)
    assert len(ms) == 1, f"{skill}: version {old} trouvée {len(ms)} fois"
    return pat.sub(f"version: {new}", text, count=1)


def insert_bis(text, titre, contenu, skill):
    assert titre not in text, f"{skill}: §1.9bis déjà présent (idempotence)"
    idx = text.find("\n## §2")
    assert idx > 0, f"{skill}: ancre « ## §2 » introuvable"
    return text[:idx] + "\n" + titre + "\n" + contenu.rstrip() + "\n" + text[idx:]


def add_read_when(text, skill):
    if re.search(r"^read_when:", text, re.M):
        return text
    parts = text.split("\n---\n", 1)
    assert len(parts) == 2, f"{skill}: frontmatter introuvable"
    block = ("read_when:\n"
             "  - Déclencher quand la demande concerne : prompts/systèmes d'AGENTS"
             " (SKILL.md de skills, prompts de sous-agents, hooks, outils d'agent)\n"
             "  - Déclencher si la demande mentionne : agent prompt, prompt d'agent,"
             " progressive disclosure, sous-agent\n"
             "  - Ne pas déclencher pour les prompts gouvernés du corpus (PMs) —"
             " périmètre prompt-engineering (convention protocole Task 28/22).")
    return parts[0].rstrip() + "\n" + block + "\n\n---\n" + parts[1]


def bump_eco_skills(text, skill, old, new):
    pat = re.compile(r'("%s":\s*)"%s"' % (re.escape(skill), re.escape(old)))
    ms = pat.findall(text)
    assert len(ms) == 1, f"ECO_SKILLS {skill}: {len(ms)} occurrences (attendu 1)"
    return pat.sub(r'\1"%s"' % new, text, count=1)


def bump_kb_heading(text, skill, old, new):
    pat = re.compile(r"^(## %s v)%s(\s*)$" % (re.escape(skill), re.escape(old)), re.M)
    ms = pat.findall(text)
    assert len(ms) == 1, f"KB heading {skill}: {len(ms)} occurrences (attendu 1)"
    return pat.sub(r"\g<1>%s\g<2>" % new, text, count=1)


def add_kb_calibration(text, skill, new, note):
    # Insère un bullet de calibration APRÈS la ligne « Dernière calibration »
    # de l'entrée du skill (bloc délimité par les titres « ## »).
    ent = re.search(r"^## %s v%s\s*$(.*?)(?=^## |\Z)" % (re.escape(skill), re.escape(new)),
                    text, re.M | re.S)
    assert ent, f"KB entrée {skill} v{new} introuvable après bump"
    bloc = ent.group(0)
    # Deux formats attestés : « **Dernière calibration** : … » et « **Dernière calibration : … »
    pat = re.compile(r"^(- \*\*Dernière calibration\b.*(?:\n(?![\n-]))*)", re.M)
    ms = pat.findall(bloc)
    bullet = ("- **Task 22 (2026-10-23, session web-fdf5963c — directive gen-plan(step)"
              " « disciplines/techniques », recherches web ciblées 2025-2026)** : "
              + note + " — bump v" + new + " (recalibrage KO-L004 : ECO_SKILLS + KB).\n")
    if ms:
        ancre = ms[0]
        nouveau_bloc = bloc.replace(ancre, ancre + bullet, 1)
    else:
        # Fallback : pas de ligne Dernière calibration → insertion avant **Statut**
        mstat = re.search(r"^- \*\*Statut\*\*.*$", bloc, re.M)
        assert mstat, f"KB {skill}: ni calibration ni Statut — ancre introuvable"
        nouveau_bloc = bloc[:mstat.start()] + bullet + bloc[mstat.start():]
    return text[:ent.start()] + nouveau_bloc + text[ent.end():]


NOTES = {
"spec-driven-development": "M1.5 CLARIFIER (Spec Kit) + rebuild test + garde de granularité anti-overhead + conflits SDD↔TDD/agilité documentés",
"cahier-des-charges": "grille anti-ambiguïté (+20,2 % Raj 2025) + scan d'exigences manquantes [HYP-xx] + format EARS + articulation agilité hybride",
"prompt-engineering": "catalogue technique→cas d'usage (CoT/self-consistency/least-to-most/plan-and-act/JSON-schema) + couplage itération↔evals + règle schéma+check déterministe + veille prompt-as-code",
"agent-prompt-engineering": "read_when rétabli (1/94 Task 28) + progressive disclosure (Agent Skills 10/2025) + altitude des system prompts (Anthropic 09/2025) + renvoi context-engineering",
"context-engineering": "JIT retrieval en principe M1 + hygiène KV-cache (Manus) + anti Governance-Decay (ré-énoncer invariants après compaction + tombstones) + refs ACE/Anthropic/Cookbook",
"memory-engineering": "ops update/forget/consolidate de première classe (AgeMem ACL 2026) + gouvernance des écrits KB=factuel/worklog=expérientiel/scratchpad=travail (survey 2512.13564) + validation Letta filesystem + contre-mesure #token",
"fleet-engineering": "règle 0 gate anti-flotte (Cognition, ratio 15× Anthropic) + M5 swarm durci (08/2026 collusion/sabotage) + ordre de routage E5/E7 a-b-c-d + échecs de handoff (micro-spéc)",
"loop-engineering": "calibration des graders agentiques (golden ≥80 %, juge≠rédacteur, ordre randomisé) + critères d'arrêt quantifiés (N/plateau ε/escalade + hash scellé anti reward-hacking) + vérification intermédiaire VPR",
"harness-engineering": "mode checkpoint/reprise (Anthropic long-running 11/2025) + budget de resserrage (checks idempotents+documentés, revue des dormants) + frontière vocabulaire arbitre/grader",
"graph-engineering": "arêtes bi-temporelles valid_from/invalidation datée (Graphiti/Zep) + arbitre de divergence KB↔frontmatters (une source fait foi) + pondération d'arêtes par usage récent + résumés par catégorie",
"refactor-guard": "golden master AVANT (n≥3 runs, sandbox+post-vol) + mutation testing léger en sandbox (anti faux-verts) + rollback automatique armé en canary (N5)",
"refactoring-test": "co-changes git comme arêtes empiriques (change coupling CodeScene) + blast radius pondéré par centralité + isolation de contexte maker/checker exigée et vérifiable",
"resource-monitor": "indicateurs dérive d'effort + taux de hit cache/préfixe + anti retry-storm 429 (backoff exponentiel + circuit breaker, KO-L001) + downgrades par effort assigné + hystérésis + envergure prédictive",
"autonomous-agent": "étape G2 RE-PLANIFICATION (plan-and-execute, max 2 itérations) + politique d'oubli/rollback EL (budget, tombstones) + machine à états explicite",
"inter-scripts": "retry/timeout/backoff au schéma de plan (idempotence = Task ID) + heartbeat daemon avant chaque niveau + validation de schéma registre.json + socket 0600 + table de correspondance A2A/MCP",
"agent-creator": "DÉRIVE CRITIQUE résorbée : SKILL.md re-écrit comme VRAIE fabrique d'agents (cadrer→générer gabarit .agent→valider→tester Simulation→inscrire), .agent réécrit (objectif fabrique + champ capacités style Agent Card), read_when réparé, titre/historique alignés",
}


HOTE_SK = Path("/home/z/my-project/skills")
# 3 éléments hôte-seuls (hors registre KB / ECO_SKILLS — préservés par l'union sync)
HOTE_SEUL = {"cahier-des-charges", "inter-scripts", "agent-prompt-engineering"}


def main():
    modifiés = []
    for skill, (old, new, contenu) in APPORTS.items():
        p = (HOTE_SK if skill in HOTE_SEUL else SK) / skill / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        if re.search(r"^version:\s*[\"']?%s[\"']?\s*$" % re.escape(new), t, re.M) \
                and TITRE in t:
            continue  # déjà appliqué (idempotence)
        t2 = bump_skill_version(t, old, new, skill)
        t2 = insert_bis(t2, TITRE, contenu, skill)
        if skill == "agent-prompt-engineering":
            t2 = add_read_when(t2, skill)
        p.write_text(t2, encoding="utf-8")
        modifiés.append(skill)

    # Recalibrage KO-L004 — arbitre ECO_SKILLS (dépôt uniquement)
    a = ARB.read_text(encoding="utf-8")
    for skill, (old, new, _) in APPORTS.items():
        if skill in HOTE_SEUL or f'"{skill}": "{new}"' in a:
            continue
        a = bump_eco_skills(a, skill, old, new)
    ARB.write_text(a, encoding="utf-8")

    # Recalibrage KO-L004 — KB (en-têtes + bullets, dépôt uniquement)
    k = KB.read_text(encoding="utf-8")
    kb_mod = False
    for skill, (old, new, _) in APPORTS.items():
        if skill in HOTE_SEUL or re.search(r"^## %s v%s\s*$" % (re.escape(skill), re.escape(new)), k, re.M):
            continue  # déjà bumpé (idempotence)
        k = bump_kb_heading(k, skill, old, new)
        k = add_kb_calibration(k, skill, new, NOTES[skill])
        kb_mod = True
    if kb_mod:
        KB.write_text(k, encoding="utf-8")

    print(f"SKILL.md modifiés : {len(modifiés)} -> {modifiés}")
    print("ECO_SKILLS + KB recalibrés KO-L004 (bumps + bullets Task 22) — 3 hôte-seuls hors registre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
