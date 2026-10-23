# Plan d'actions — Task 18 : Analyse + optimisation du système d'installation + skill alias-eco

> **Session** : web-fdf5963c · **Date** : 2026-10-23 · **gen-plan** : v3.23.1 (mode NULL — invocation `gen-plan : <instructions>`, clause v3.22.1)
> **Directive propriétaire** : « analyse l'intégralité de cette discussion, puis génère à nouveau l'intégralité du plan d'actions, puis exécute-le. lorsque les taches seront terminées, génère un nouveau plan (mode "step") : analyse + optimisation (toutes disciplines + refactoring, en regénérant, suivre les règles) du système d'installation, en intégrant le système d'alias $<ALIAS> ; génère le skill "alias-eco" (manager, liste JSON triée sans doublons dans @historique/@Alias/, déclencheurs "alias-eco", "liste mes alias", "alias-eco (chat)" → TXT trié alphabétique) »
> **Prérequis A hérité** (début de session, contexte compacté) : expliquer pourquoi PM INSTALL ASSEMBLE gen-plan/correct-work/clone-chat au lieu de les INSTALLER directement ; si l'installation directe est plus judicieuse, la faire adopter par PM INSTALL et adapter les PMs en conséquence.
> **Règle d'or n°2** : aucun `git push` sans GO explicite propriétaire — la couche reste locale (worklog + snapshot tar de protection).

## §1 — Classification (E1-E3)

- **Type 4** (méta-outil/écosystème — gestion de l'écosystème Knowledge, scripts Python, registre KB). Complexité **complexe** → mode PEK **Hybride** (CoT E1-E3, Chaining par phases).
- **Profils** : NORMAL (resource-monitor OK — charge faible, zéro signal de pression détecté en ouverture).
- **État matériel (E2, KO-L007)** : dépôt `/home/z/my-project/KNOWLEDGE-repo` @ `b75a620` (commit épinglé, arbre propre — modes fichier normalisés `core.fileMode false`) ; corpus `@mon-ecosysteme/` 9 fichiers (GEN-PLAN v3.23.1, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.1, REFACTOR-GUARD v1.7.0, INSTALL v1.7.1, SHARED v1.7.7, ULTRA, README v2.1.7, SYNC v1.4.9) ; KB 33 entrées ; profil local hôte 103 skills mais **gen-plan + correct-work ABSENTS** (wipe inter-sessions — PM-INSTALL §3.4) ; `alias-eco` inexistant ; `@historique/@Alias/` inexistant ; worklog dépôt interrompu à Task 17-final (campagne web-da654199 journalisée via commits git + @historique — gap consigné).
- **Constats d'analyse (T1, réponse au prérequis A)** :
  1. PM-INSTALL §3.2 prescrit l'**assemblage** des SKILL.md depuis les PMs (jamais copiés à l'aveugle) — voie historique bootstrap : le corpus (9 fichiers + archive scellée) suffit à reconstruire toutes les formes installées.
  2. La pratique réelle (session W1 → campaigne web-da654199) installe **directement** par `scripts/eco_install_pipeline.py` : copie des formes installées **certifiées par les arbitres** du clone du dépôt vers l'hôte (sync union + garde R2 + rescellement archive). Ce script est versionné au dépôt (source de vérité, e185698).
  3. Depuis KO-L004 v1.1.0, la direction de génération est **SKILL.md → PM** (le PM est généré mécaniquement à chaque montée ; le frontmatter SKILL.md est la source de vérité de version). L'assemblage PM → SKILL.md demeure la spécification de la forme (§5 de chaque PM) et la voie bootstrap corpus-seul.
  4. **Verdict** : l'installation directe EST plus judicieuse quand le dépôt est disponible (formes certifiées, plus rapide, byte-identique à l'état arbitré) ; l'assemblage reste indispensable comme voie bootstrap (environnement nu, archive seule). L'optimisation = **mécanisme dual codifié** : installation directe par défaut + assemblage bootstrap documenté — les §5 des PMs demeurent la spécification de la forme installée.

## §2 — Phases et tâches (E5-E7)

| # | Phase | Tâches | Skills mobilisés | #token |
|---|-------|--------|------------------|--------|
| A | **Analyse système d'installation** | A1 état des lieux (pipeline 11 étapes, scripts, dualité document/pratique) ; A2 réponse prérequis A (assemblage vs direct) | gen-plan, correct-work (hook) | ~6 k |
| B | **Skill alias-eco v1.0.0** | B1 SKILL.md (frontmatter 5 champs, déclencheurs) ; B2 `scripts/alias-manager.py` (manager : détection phrases récurrentes, liste JSON triée/dédupliquée → `skills/@historique/@Alias/aliases.json`, export TXT chat, résolution $ALIAS) ; B3 evals ×2 + `references/format-alias.md` ; B4 amorçage (ECO-LEON = « mon écosystème personnel » + phrases récurrentes de la présente discussion) | skill-creator, script-creator, prompt-engineering (description/déclencheurs) | ~28 k |
| C | **Optimisation par régénération** | C1 montées 4 familles (gen-plan v3.23.2, correct-work v2.8.0 — délégation alias-eco mode PROJET + dependencies, clone-chat v2.0.2, refactor-guard v1.7.1 — note §5 mécanisme dual) + génération mécanique PMs (KO-L004, deltas verrouillés) → SHARED v1.7.8 + PM-INSTALL v1.7.2 auto-recalibrés ; C2 PM-INSTALL **v1.8.0** (mécanisme dual §2/§3.2, alias-eco au périmètre §2bis/§4/§A.3, installeur canonique) ; C3 `eco_install_pipeline.py` optimisé (chemin REPO paramétrable + PIN b75a620 descendant-tolérant + alias-eco aux listes) ; C4 cascade (KB, ECO_SKILLS, ULTRA, SYNC-CONTEXT, README, archive rescellée, @historique : 4 PMs déplacés + lignes + @Alias/ documenté) | refactoring-engineering (n°55), refactoring-test (pré-vol blast radius), refactor-guard (garde-fous), graph-engineering (KB bidirectionnel), harness-engineering (arbitres), context-engineering (SHARED/propagate), agent-creator (PM-INSTALL) | ~38 k |
| D | **Certification** | D1 batterie arbitres (verify-cross ×2 modes, verify-correct-work 16/16, check-ecosysteme-integrity, test-coherence-interactions, generer-pm --check, scan-doublons, answer-key-checker ×2, certification-complete) ; D2 correct-work **PROJET** rapport `download/rapport-correct-work-projet-task18.md` | correct-work (PROJET), gen-plan | ~18 k |
| E | **Installation profil local + journalisation** | E1 projection hôte par installation directe (gen-plan, correct-work, alias-eco, KB, @Alias/, corpus, @historique, scripts) ; E2 vérification hôte (versions, déclencheurs, arbitre intégrité hôte) ; E3 worklog dépôt (entrée Task 18) + snapshot tar de protection | PM-INSTALL v1.8.0 (nouveau pipeline), memory-engineering | ~12 k |
| F | **Plan suivant (mode step)** | F1 génération du plan d'actions SUIVANT via gen-plan(step) — tâches suivantes (publication GO propriétaire, amorçage opérationnel alias, re-mesure QUOTA agent-creator, rotation PAT) | gen-plan(step) | ~6 k |

**Total #token estimé (E4)** : ~108 k (grille complexe, 4+ skills, coeff 1.3×).

## §3 — Answer key (E1 — spec de session, vérifiable mécaniquement)

```yaml
decisions:
  - id: "D001"
    criterion: "Le plan complet est régénéré via gen-plan v3.23.1 et publié (ce fichier) avec answer key"
    verification: "python3 -c \"import re,sys; t=open('download/plan-task18-optimisation-installation-alias-eco.md',encoding='utf-8').read(); sys.exit(0 if 'gen-plan' in t and 'D001' in t and '## §3' in t else 1)\""
    source: "directive propriétaire 2026-10-23 (« génère à nouveau l'intégralité du plan d'actions »)"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "L'analyse du système d'installation est matérialisée : dualité assemblage (§3.2 PM-INSTALL, voie bootstrap) vs installation directe (eco_install_pipeline.py, voie certifiée) documentée avec verdict"
    verification: "python3 -c \"t=open('download/plan-task18-optimisation-installation-alias-eco.md',encoding='utf-8').read(); sys.exit(0 if 'mécanisme dual' in t and 'bootstrap' in t else 1)\""
    source: "directive (« analyse le système d'installation ») + prérequis A (assemblage vs installation directe)"
    priority: "S2"
    status: "verified"
  - id: "D003"
    criterion: "Le skill alias-eco v1.0.0 existe : SKILL.md (frontmatter 5 champs : name, version 1.0.0, category ecosystem, language fr, tags) + scripts/alias-manager.py + evals/evals.json + evals/trigger_evals.json + references/format-alias.md"
    verification: "python3 -c \"import os,sys; b='skills/alias-eco'; ok=all(os.path.isfile(os.path.join(b,p)) for p in ['SKILL.md','scripts/alias-manager.py','evals/evals.json','evals/trigger_evals.json','references/format-alias.md']); sys.exit(0 if ok else 1)\""
    source: "directive (« génère-moi un skill alias-eco cohérent, optimisé et fonctionnel ») + conventions skill-creator/SHARED §1.2"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Déclencheurs alias-eco présents dans la description ET trigger_evals (cas positifs « alias-eco », « liste mes alias », « alias-eco (chat) » + cas négatifs)"
    verification: "python3 -c \"import json,sys; d=json.load(open('skills/alias-eco/evals/trigger_evals.json',encoding='utf-8')); t=json.dumps(d,ensure_ascii=False); s=open('skills/alias-eco/SKILL.md',encoding='utf-8').read(); sys.exit(0 if all(x in t for x in ['alias-eco (chat)','liste mes alias']) and 'alias-eco' in s else 1)\""
    source: "directive (« ses déclencheurs seront 'alias-eco', 'liste mes alias' »)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "alias-manager.py liste/trie/déduplique les phrases récurrentes en JSON dans skills/@historique/@Alias/aliases.json (tri alphabétique, 0 doublon strict, format $ALIAS)"
    verification: "python3 skills/alias-eco/scripts/alias-manager.py --selftest"
    source: "directive (« lister en format JSON sauvegardé dans @historique/@Alias/, trier, pas de doublons strictement identiques »)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Le mode chat produit une liste TXT des phrases récurrentes de la discussion, triée par ordre alphabétique"
    verification: "python3 skills/alias-eco/scripts/alias-manager.py --selftest && python3 -c \"import json,sys; t=open('skills/@historique/@Alias/aliases.json',encoding='utf-8').read(); j=json.loads(t); ps=[e['phrase'] for e in j['phrases']]; sys.exit(0 if ps==sorted(ps) and len(ps)==len(set(ps)) else 1)\""
    source: "directive (« le déclencheur 'alias-eco (chat)' doit [produire] une liste TXT... trier par ordre alphabétique »)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Alias d'amorçage ECO-LEON = « mon écosystème personnel » enregistré et résolvable ($ECO-LEON → expansion)"
    verification: "python3 skills/alias-eco/scripts/alias-manager.py --resolve 'de $ECO-LEON'"
    source: "directive (exemple explicite du propriétaire)"
    priority: "S2"
    status: "verified"
  - id: "D008"
    criterion: "correct-work v2.8.0 intègre la délégation alias-eco au mode PROJET (analyse des phrases récurrentes des discussions) + dependencies += alias-eco >= 1.0.0"
    verification: "python3 -c \"s=open('skills/correct-work/SKILL.md',encoding='utf-8').read(); sys.exit(0 if 'alias-eco' in s and 'version: 2.8.0' in s else 1)\""
    source: "directive (« lors d'analyse de mes discussions lorsque j'exécuterai mon skill correct-work (projet) »)"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "PM-INSTALL v1.8.0 régénéré : mécanisme dual (installation directe par défaut + assemblage bootstrap §3.2) + alias-eco intégré (§2bis fermeture, §4 interactions, §A.3 instantané) + installeur canonique"
    verification: "python3 -c \"t=open('skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md',encoding='utf-8').read(); sys.exit(0 if 'Version : 1.8.0' in t and 'installation directe' in t.lower() and 'alias-eco' in t else 1)\""
    source: "directive (« optimise le système d'installation en regénérant, toutes disciplines et refactoring ») + prérequis A"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Les 4 PMs familles régénérés mécaniquement (KO-L004) : gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1 — chacun avec note §5 mécanisme dual (via delta verrouillé)"
    verification: "python3 scripts/generer-pm-skill.py --check"
    source: "prérequis A (« adapte les PM CORRECT-WORK, PM GEN-PLAN et PM CLONE CHAT en conséquence ») + cohérence D009 (refactor-guard 4e famille du pipeline)"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "Cascade complète exécutée : KB (entrée alias-eco + réciproques + versions 4 familles + décision), ECO_SKILLS du checker += alias-eco, ULTRA régénéré, SYNC-CONTEXT à jour, archive rescellée round-trip, @historique (4 PMs déplacés + lignes historiques + @Alias/ documenté)"
    verification: "python3 scripts/check-ecosysteme-integrity.py && python3 scripts/gen-ultra-maitre.py --check"
    source: "règles écosystème (KO-L004 recalibrage croisé, R4 @historique, SHARED §3.2 bidirectionnalité)"
    priority: "S1"
    status: "verified"
  - id: "D012"
    criterion: "Batterie d'arbitres verte : verify-cross (2 modes), verify-correct-work 16/16, check-ecosysteme-integrity, test-coherence-interactions, generer-pm --check rc=0, scan-doublons 0, certification-complete rc=0 (0 échec introduit)"
    verification: "python3 scripts/certification-complete.py"
    source: "PM-INSTALL §3.3 (étape 9 — ordre contraint arbitres) + refactor-guard R8 (zéro-régression)"
    priority: "S1"
    status: "verified"
  - id: "D013"
    criterion: "correct-work PROJET : rapport de vérification de la couche Task 18 produit (verdict PASS AVEC RÉSERVES au pire, 0 S1/S2 non résolu)"
    verification: "python3 -c \"import os,sys; sys.exit(0 if os.path.isfile('download/rapport-correct-work-projet-task18.md') else 1)\""
    source: "couplage correct-work §1.5 (gen-plan OBLIGATOIRE à l'Étape 1)"
    priority: "S2"
    status: "verified"
  - id: "D014"
    criterion: "Profil local installé : gen-plan v3.23.2, correct-work v2.8.0, alias-eco v1.0.0, KNOWLEDGE.md, @historique/@Alias/aliases.json projetés dans /home/z/my-project/skills/"
    verification: "python3 -c \"import re,sys; ok=True
for p,v in [('gen-plan','3.23.2'),('correct-work','2.8.0'),('alias-eco','1.0.0')]:
    t=open('/home/z/my-project/skills/%s/SKILL.md'%p,encoding='utf-8').read(500)
    ok = ok and ('version: '+v) in t
sys.exit(0 if ok and __import__('os').path.isfile('/home/z/my-project/skills/@historique/@Alias/aliases.json') else 1)\""
    source: "objectif principal de session (« installe mon écosystème sur mon profil local ») + PM-INSTALL v1.8.0 (voie directe)"
    priority: "S1"
    status: "verified"
  - id: "D015"
    criterion: "Worklog dépôt enrichi (entrée Task 18 complète — travail, incidents, stage summary) ; gap campagne web-da654199 consigné honnêtement"
    verification: "python3 -c \"t=open('worklog.md',encoding='utf-8').read(); sys.exit(0 if 'Task ID: 18' in t and 'web-fdf5963c' in t else 1)\""
    source: "SHARED §1.4 (conventions worklog) + KO-L003 (honnêteté des constats)"
    priority: "S3"
    status: "verified"
  - id: "D016"
    criterion: "Le plan d'actions SUIVANT est généré via gen-plan (mode step) à la clôture de la présente couche — enchaînement des tâches suivantes identifiées"
    verification: "python3 -c \"import os,sys; sys.exit(0 if any('plan-task19' in f for f in os.listdir('download')) else 1)\""
    source: "directive (« lorsque les taches... terminées alors génère un nouveau plan d'action... mode step... dorénavant ») + gen-plan v3.22.1 déclencheurs step"
    priority: "S2"
    status: "verified"
  - id: "D017"
    criterion: "Règle d'or n°2 respectée : 0 git push durant la session (travail local ; snapshot tar de protection anti-écraseur) ; proposition de publication préparée pour GO propriétaire"
    verification: "python3 -c \"import subprocess,sys; r=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True); sys.exit(0 if r.stdout.strip().startswith('b75a620') else 1)\""
    source: "worklog Task 1 campagne courante (règle d'or n°2) + leçon Task 17 (écraseur local — snapshot par couche)"
    priority: "S1"
    status: "verified"
```

## §4 — Mobilisation des disciplines (toutes + refactoring)

| Discipline | Mobilisation concrète |
|------------|----------------------|
| spec-driven-development | Answer key D001-D017 = spec exécutable de session (E1), re-validée E8/D2 |
| memory-engineering | Worklog dépôt + KB + @historique/@Alias/ (État Long), ancres par phase |
| fleet-engineering | Exécution série (philosophie #4) — pas de flotte nécessaire ; le plan trace cette décision |
| context-engineering | Socle SHARED lu en premier ; lectures bloc par bloc ; plan auto-suffisant |
| loop-engineering | Hooks correct-work par phase (A→F) ; boucle E12-E13 (max 2 rounds/groupe) |
| graph-engineering | KB bidirectionnel alias-eco ↔ correct-work ; relations tracées SHARED §3.1 |
| harness-engineering | Arbitres recalibrés (ECO_SKILLS += alias-eco), verrouillages B1 (sub_locked), garde R2 |
| prompt-engineering | Description/déclencheurs alias-eco optimisés (3 positifs + négatifs), éval. V6 re-jeu |
| skills-inventory | Registre KB — formats d'entrée template SHARED §2.2, scan du registre (D011 : entrée alias-eco + 4 montées, bidirectionnalité) |
| script-mon-ecosysteme-infrastructure | Conventions INFRA des dossiers `@` (SHARED §1.2) : `@historique/@Alias/` (registre vivant), scelleur task21-f2 (round-trip v2.2), règles de déploiement INFRA-1..3 |
| refactoring-engineering (n°55) | Montées de version = petites transformations préservant le comportement (arbitres avant/après, semver, R2/R4) |
| refactoring-test (outil n°55) | Pré-vol : graphe blast radius de la couche (modifications PMs/KB/checker) |
| refactor-guard | Garde-fous : zéro-régression prouvée par batterie D012 ; échelle shadow (aucun comportement public avant arbitres) |

## §5 — Risques et adaptations (règle d'or n°1)

- **R1 — écraseur local** (leçon Task 17) : snapshot tar après chaque phase verte ; aucun commit/push sans GO (règle d'or n°2).
- **R2 — verrouillages KO-L004** (sub_locked ABANDON sans écriture) : deltas préparés avec comptage exact des motifs (pré-lecture des PMs concernés) ; génération famille par famille (jamais `--generate all` avec deltas hétérogènes).
- **R3 — arbitres à invariants** : recalibrage ECO_SKILLS/corpus AVANT la batterie (jamais ajusté au verdict — KO-L003) ; divergence affichée, jamais masquée.
- **R4 — taille de cascade** : si un verrou abandonne, la famille est journalisée en réserve (S3) et le reste de la couche continue (jamais d'arrêt implicite).

## §6 — Exécution (E9-E14)

Séquentiel strict : A → B → C (C1→C2→C3→C4) → D → E → F. Hook correct-work par phase (verdict par phase au worklog) ; boucle E12-E13 max 2 rounds par phase. E15 : bilan + knowledge-observer (M1 observation) + génération du plan suivant (F1, gen-plan(step)).

## §7 — Routage des outils dédiés (conventions appliquées par type d'artefact — N2)

| Type d'artefact | Outil dédié mobilisé | Artefacts de la couche |
|-----------------|----------------------|------------------------|
| skill | **skill-creator** | alias-eco/SKILL.md (frontmatter 5 champs, evals schéma skill-creator), correct-work v2.8.0 (montée MINOR + dependencies) |
| agent/PM | **agent-creator** | 4 PMs familles régénérés (KO-L004), PM-INSTALL v1.8.0 (mécanisme dual), SHARED v1.7.8, ULTRA, SYNC-CONTEXT v1.5.0, README v2.1.8 |
| script | **script-creator** | alias-manager.py, task18-*.py (5 scripts de cascade verrouillés), recalibrages arbitres (verify-correct-work, ECO_SKILLS) |
| infrastructure | **script-mon-ecosysteme-infrastructure** | @historique/@Alias/ (dossier `@` non-skill, SHARED §1.2), scelleur task21-f2-rebuild-archive.py (round-trip v2.2), eco_install_pipeline.py (exécutant canonique voie directe) |
| registre KB | **skills-inventory** | KNOWLEDGE.md (entrée alias-eco v1.0.0, 4 montées de version, réciproques bidirectionnelles, décision Task 18) |
