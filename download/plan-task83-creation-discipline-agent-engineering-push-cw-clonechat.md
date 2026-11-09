# Plan Task 83 — Création discipline agent-engineering v1.0.0 + PUSH chaîne + CW --bloc + clone-chat

> **Directive** : `gen-plan (step)` — trace `1a1beaee032b5aa5`, 2 items : (1) créer un skill/agent/agent autonome « Agent Engineering » (forme au choix de l'agent) défini comme **discipline** de l'écosystème, expert des domaines « Agent-Based Engineering », « Agent Engineering », « Multi-Agent Systems Engineering », orchestrant leurs tâches $FACON et de façon autonome ; (2) « continue $FACON et de façon autonome en utilisant ma clé "github_pat_…" pour les PUSH » — **PUSH autorisés par délégation PAT explicite** (KO-L009 levé pour cette chaîne).
> **Session** : web-ecef7f80 · canal zai-web · 2026-11-09 · mode step (§5.5 — correct-work(groupe) après chaque groupe, max 2 rounds, correct-work(projet) en fin de chaîne).
> **Profil ressource** : NORMAL (G-RES niveaux 0 — collecte monitor.py fraîche). #token estimé chaîne : 18 000-28 000.

## État de reprise (E1-RES — mesuré sur le disque)

- **Garde post-coupure (règle d'or n°9) — FAITE pré-E1** : profil hôte partiellement wiped (skills/gen-plan, skills/correct-work, skills/@mon-ecosysteme, skills/KNOWLEDGE absents du profil — cas documenté §3.4 pipeline) → réinstallation voie directe `scripts/eco_install_pipeline.py` : **rc=0 · 54/54 SHA-256 · 0 divergence · garde R2 0 rétrogradation · archive round-trip v2.2** (preuve /tmp/reinstall.log, log de la session).
- **Dépôt** : HEAD `95fef2b` « Task 82 CLOSE » — commit certifié (CW --bloc #2 B1-B4 4/4, E8 FINAL 10/10 verified 04:37:00Z), **NON poussé** (instruction PUSH absente de la directive Task 82 — maintenant explicite). Distant : à vérifier (pré-vol).
- **Arbre de travail dépôt** : 23 fichiers divergents en **bits de mode uniquement** (100644→100755, contenu byte-identique — diff --stat 0 insertions/0 suppressions) : livrables download/, scripts task81/82, skills/@historique/knowledge-observer, iphone18/references, knowledge-observer.agent. Source : fichiers profil créés en 755, sync profil→dépôt préservant le mode. Fix à la source requis avant PUSH.
- **File re-curation (R5 honnête, Task 82 §4 clone CLOSE)** : skill-creator → web-reader → cahier-des-charges → iphone17 (P2-P4). **Aucune fausse promesse** : la présente session consacre sa fenêtre à l'item 1 (création) + PUSH ; la file reste priorisée et consignée.
- **Worklog** : profil 1 997 lignes (Task 82 CLOSE complet) ; dépôt identique au commit CLOSE.
- **Veille fondements (D006, sonde unique KO-L001 — FAITE)** : LangChain **State of Agent Engineering 2026** (langchain.com/state-of-agent-engineering — « agent engineering = processus itératif de transformation de LLMs en systèmes fiables », 1300+ praticiens, 57 % en production) · **Agent-Based Software Engineering** (ABSE — paradigme agents-as-building-blocks, méthodologie Tropos) · sources N31/N34 déjà vérifiées (Anthropic Agent Teams & Managed Agents 2026 · multi-agent research system 06/2025 · Cognition « Don't Build Multi-Agents » 2025 · Anthropic « Patterns and problems in emerging multiagent systems » 08/2026 · Building Effective Agents 12/2024).

## Groupes d'exécution (mode step)

### G1 — PRÉ-VOL & PUSH Task 82 CLOSE (#token 2 500)

- **SG1.1 Hygiène arbre** — `T1.1.1` : fix mode-bits — chmod 644 des 23 fichiers profil concernés (download/, scripts/) + `git restore` dépôt (modes 100755→100644, contenu byte-identique R2) → arbre propre vérifié (`git status` vide).
- **SG1.2 PUSH one-shot** — `T1.2.1` : pré-vol protocole Task 63/77 : zéro-persistance ×4 (jeton complet 0 occurrence disque `/home/z/my-project` + `~`, remote sans jeton, `credential.helper` aucun, `~/.git-credentials` absent) + `git fsck` rc=0 + fetch + ls-remote authentifié + fast-forward pur prouvé (SHA distant == merge-base). `T1.2.2` : push one-shot `95fef2b` (jeton UNIQUEMENT en mémoire de commande — variable d'environnement du shell persistant, jamais git config ni fichier) + post-push (distant == HEAD, avance 0, arbre propre, zéro-persistance re-vérifiée par grep disque) + **E15 : 6ᵉ exposition consignée au worklog (2026-10-26 · 2026-11-07 · 2026-11-08 ×2 · 2026-11-09 ×2) — RÉVOCATION/ROTATION recommandée**.

### G2 — CRÉATION SKILL DISCIPLINE agent-engineering v1.0.0 (#token 6 000)

- **SG2.1 Conception** — `T2.1.1` : positionnement consigné (answer key D003/D004) : **skill discipline n°56** ; frontière R4 — agent-engineering = discipline UMBRELLA des 3 domaines (cadre de cadrage/routage/évaluation), ROUTE vers détenteurs (fleet patterns flottes · memory mémoire · harness gardes-fous · spec-dd contrats · autonomous-agent format .agent · agent-creator fabrique · gen-plan planification) — complémentaire de fleet-engineering, jamais duplicatif.
- **SG2.2 Rédaction** — `T2.2.1` : `skills/agent-engineering/references/fondements-academiques.md` (sources veille D006 citées + N31/N34). `T2.3.1` : `skills/agent-engineering/SKILL.md` **v1.0.0** — gabarit canonique disciplines (fleet-engineering 117 lignes) : frontmatter (category ecosystem, langue fr, description verbatim « Skill discipline agent engineering : … », dependencies, read_when borné Task 28) + §0 Contexte Système + Règle Zéro + §1 spécification fonctionnelle (mission · 3 domaines ABE/AE/MASE · routage inter-éléments · règles opérationnelles · fondements) + §2 spécification technique + §3 relations + §4 conventions + §5 évaluations + §6 traçabilité v1.0.0 + §7 références + **§8 registre d'assignation des disciplines (décentralisé du SHARED §7)**. `T2.4.1` : `evals/trigger_evals.json` (7 cas : 5 positifs + 2 négatifs disciplines voisines fleet/agent-creator) + `evals/evals.json`.

### G3 — CASCADE KO-L004 (#token 4 000)

- **SG3.1 Registres** — `T3.1.1` : KB `skills/KNOWLEDGE.md` — entrée `## agent-engineering v1.0.0` (gabarit fleet-engineering : Category/Description/Dépend de/Utilisé par/Dernière calibration/Statut) + arêtes bidirectionnelles (fleet-engineering §3/§8, autonomous-agent, agent-creator, gen-plan §3 relations du vivant existant — ajouts purs R2). `T3.2.1` : `scripts/check-ecosysteme-integrity.py` — dict ECO_SKILLS += `agent-engineering: 1.0.0` (manifeste DUALS leçon L-82-a — patch PATCH de l'arbitre, §0/description inchangés) → exécution : manifeste écrit, attendu ~114/114 (dynamisé KO-L004 : len(ECO_SKILLS)). `T3.3.1` : ULTRA `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` — 13ᵉ rangée table §1 (routage) + ligne §3 skills (agent-engineering 1.0.0) — idempotence ×2. `T3.4.1` : `skills/@historique/historiques-par-skill/agent-engineering.md` CRÉÉ (v1.0.0 — Task 83, directive 1a1beaee032b5aa5).
- **SG3.2 Projection hôte** — `T3.5.1` : re-exécution pipeline installation (projection dépôt→profil) → skills/agent-engineering présent profil + SHA-256 vérif post-install **55/55 attendu** + zip rescellé parité hôte == dépôt + corpus 4/4 COHERENT + arbitres post-cascade (verify-cross, interactions STRICT, doublons 0, corpus).

### G4 — TESTS BREFS FONCTIONNELS + PERFORMANCES + IDEMPOTENCE (#token 3 500)

- `T4.1.1` Fonctionnels : structure frontmatter (YAML parse, description SKILL==KB byte-identique sur la phrase canonique), `task14-scan-doublons.py` 0, `verify-cross.py` 100 %, `test-coherence-interactions.py` STRICT, `check-ecosysteme-integrity.py` ×2 (idempotent), corpus 4/4, `spell-check.py`, selftest harnais `protocole-test.py` 15/15 ×2 (fraîcheur chaîne).
- `T4.2.1` Idempotence ×2 : pipeline re-run (divergences []), ULTRA re-run no-op, manifeste sha stable, re-scellage archive stable, `--verifier agent-engineering` si applicable (harnais re-curation — sinon structure seule consignée honnêtement).
- `T4.3.1` Performances : `poids-chargement.py --json` (poids agent-engineering < 30 Kio cible progressive disclosure ; #token estimés), durées arbitres mesurées, perf stable ×2.

### G5 — CLÔTURE + PUSH FINAL (#token 5 000)

- `T5.1.1` : **correct-work (projet) --bloc** B1-B4 (B1 installation+certification · B2 corpus+KB+outillage · B3 livrables création+tests · B4 extension/pendances) + rapport `download/rapport-correct-work-bloc-task83.md` (profil+dépôt).
- `T5.2.1` : **clone-chat** scellé `download/clone-chat-session-web-ecef7f80-20261109-task83.md` (§0-§5 + S1-S8 PASS + §4 reprise : file re-curation P2-P4 + inscription socle SHARED §7/gen-plan §1.6 pendances documentées).
- `T5.3.1` : **E8 FINAL** horodatage couplé + `check_plan_protocol.py --plan --worklog` P1-P5 + `answer-key-checker.py` ALL PASS + statuts finaux plan.
- `T5.4.1` : **SYNC-CONTEXT** resync état Task 83 (compteurs mesurés — skills/disciplines/agents) + worklog dépôt ← profil (préfixe strict vérifié) + livrables syncés dépôt + **commit CLOSE** (message détaillé).
- `T5.5.1` : **PUSH final one-shot** (PAT, protocole identique G1 — zéro-persistance, fast-forward pur prouvé, post-push distant == HEAD) + E15 bilan expositions.

## Pendances consignées (R5 — aucune fausse promesse)

1. **Inscription socle de la discipline n°56** : table définitions + registre assignation du **SHARED §7** (bump v1.7.37 + propagation) + rangée **gen-plan §1.6/§3** (bump MINOR 3.42.0 + cascade gen-plan KO-L004). Méthode : précédents v1.7.0 (n°54) et Task 7/8 (n°55) — tâche dédiée. En attendant : discipline opérable via KB (Règle Zéro : registre source de vérité) + ULTRA 13ᵉ voie + read_when + registre §8 local.
2. **File re-curation P2-P4** : skill-creator → web-reader → cahier-des-charges → iphone17 (analyse-recuration-task82.md — priorités intactes).
3. **PAT** : révocation/rotation recommandée (6ᵉ exposition consignée).

## Answer key (E1 — décisions D001-D010, format canonique)

**D001** (S1 — hygiène arbre)
- criterion: "Profil réinstallé (fait pré-E1) + arbre dépôt propre + modes 644 sources profil"
- verification: "pipeline rc=0 54/54 consigné ; git status dépôt vide après chmod/git restore ; stat -c %a des 23 fichiers = 644"
- source: /tmp/reinstall.log + git status
- status: verified

**D002** (S1 — PUSH Task 82 CLOSE)
- criterion: "Commit 95fef2b poussé one-shot, distant == HEAD, zéro-persistance prouvée"
- verification: "push rc=0 ; git ls-remote == 95fef2b ; grep -r jeton /home/z/my-project → 0 occurrence ; E15 6e exposition consignée worklog"
- source: git + protocole Task 63/77
- status: verified

**D003** (S2 — forme choisie : SKILL discipline)
- criterion: "skills/agent-engineering/SKILL.md v1.0.0 conforme gabarit disciplines (category ecosystem, description verbatim, §8 registre) ; justification forme consignée (vs agent .agent / agent autonome)"
- verification: "structure dossiers + frontmatter YAML parse + KB entrée Category ecosystem"
- source: directive verbatim « discipline » + gabarit fleet-engineering
- status: verified

**D004** (S2 — frontière R4 anti-duplication)
- criterion: "agent-engineering = UMBRELLA 3 domaines (cadre/routage/évaluation), ROUTE vers détenteurs (fleet/memory/harness/spec-dd/autonomous-agent/agent-creator/gen-plan) — zéro duplication de méthode fleet-engineering"
- verification: "§1 routage + §3 relations du SKILL.md + arêtes KB bidirectionnelles + verify-cross 100 % + interactions STRICT"
- source: fleet-engineering SKILL.md + KB
- status: verified

**D005** (S2 — cascade KO-L004 locale + pendance socle)
- criterion: "KB entrée + ECO_SKILLS integrity (PATCH arbitre, attendu dynamisé ~114/114) + manifeste + ULTRA 13e voie + historiques-par-skill CRÉÉ + projection hôte 55/55 + zip parité ; inscription SHARED §7 + gen-plan §1.6 = pendance structurée (précédents v1.7.0 n°54 / Task 7-8 n°55)"
- verification: "arbitres 5/5 ; pipeline 55/55 ×2 ; re-jeux no-op ; pendances consignées clone §4"
- source: mécanique KO-L004
- status: verified

**D006** (S2 — fondements académiques)
- criterion: "references/fondements-academiques.md rédigé, sources réelles citées (State of Agent Engineering 2026 LangChain + ABSE/Tropos + N31/N34)"
- verification: "fichier présent + sources vérifiables (sonde unique KO-L001 de la session)"
- source: WebSearch session + tmp/n31-recherche
- status: verified

**D007** (S2 — SKILL.md v1.0.0 complet)
- criterion: "gabarit canonique §0-§8 + description verbatim + read_when borné (Task 28) + evals 7 cas (5 positifs + 2 négatifs) + poids < 30 Kio"
- verification: "structure + poids-chargement --json + task14-scan-doublons 0"
- source: gabarit fleet-engineering
- status: verified

**D008** (S3 — tests brefs + idempotence ×2)
- criterion: "Fonctionnels (arbitres ×2 idempotents, selftest harnais 15/15 ×2) + performances (poids/durées mesurés, perf stable) + idempotence (pipeline, ULTRA, manifeste sha stables)"
- verification: "sorties consignées worklog ; re-jeux byte-identiques"
- source: arbitres dépôt
- status: verified

**D009** (S3 — clôture)
- criterion: "CW (projet) --bloc B1-B4 rapport profil+dépôt + clone-chat S1-S8 scellé + SYNC-CONTEXT + worklog dépôt + commit CLOSE + PUSH final + E15"
- verification: "rapport présent profil+dépôt ; distant == HEAD final"
- source: correct-work v2.11.0 + clone-chat v2.0.2
- status: verified

**D010** (S4 — file re-curation P2-P4 honnête)
- criterion: "File skill-creator → web-reader → cahier-des-charges → iphone17 NON initiée (fenêtre consacrée à l'item 1), priorités intactes, zéro faux TERMINÉ"
- verification: "pendances consignées clone §4 + commit message"
- source: analyse-recuration-task82.md
- status: verified

Horodatage plan : 2026-11-09T05:22:37Z (statuts finaux — écriture E8 FINAL, re-validation complète)

Verdict E8 : PASS FINAL (chaîne mode step G1→G5 terminée 5/5 : G1 hygiène+PUSH 95fef2b ✅ · G2 création agent-engineering v1.0.0 ✅ · G3 cascade KO-L004 5/5 ✅ · G4 tests 3 familles ✅ · G5 clôture ✅ [CW --bloc 4/4 0 round · rapport · clone scellé · SYNC v1.5.10 · worklog dépôt · commit CLOSE · PUSH final] — answer key 10/10 verified — Horodatage vérifié : 2026-11-09T05:22:37Z — check_plan_protocol P1-P5 PASS re-validés après la présente écriture)

## Contingences

- **Push rejeté (non fast-forward)** : le propriétaire a poussé entre-temps → fetch + rebase INTERDIT sans analyse (R2) → merge-base vérifié, statut consigné, PUSH reporté au propriétaire avec diagnostic (jamais de force-push).
- **Fenêtre contexte insuffisante en G5** : commit CLOSE minimal garanti (livrables + worklog syncés), clone-chat et CW --bloc sont les éléments abrégables en dernier ressort (consigné honnêtement, jamais escamoté silencieusement).
- **Arbitre FAIL** : pause, correction ciblée (max 2 rounds correct-work), re-verdict honnête (KO-L003 : jamais ajuster la réalité).

— Plan écrit le 2026-11-09, session web-ecef7f80, trace directive 1a1beaee032b5aa5. Exécution mode step : G1 → G5, correct-work(groupe) après chaque groupe.
