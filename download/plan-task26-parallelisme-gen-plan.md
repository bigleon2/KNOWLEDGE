# Plan d'actions — Task 26 : parallélisation par défaut de gen-plan

> **Directive verbatim** (2026-10-24, session web-fdf5963c) : « gen-plan : "le problème avec 'gen-plan' a débuté lors de ma requête où j'ai fait des recherches web sur les disciplines. j'ai trouvé que sans l'exécution de 'gen-plan' tu as orchestré plus de taches en parallèle (exécution plus rapide du plan d'actions) que si 'gen-plan' exécute dans ces plans d'actions (exécution plus lente du plan d'actions). trouve pourquoi 'gen-plan' ne le fais pas, puis fais en sorte qu'il le fasse." »
> **Mode** : NULL (clause mode NULL §1.5 — exécution classique, sans portes de confirmation).
> **Règle d'or n°2** : 0 commit, 0 push — publication au GO propriétaire.

## État d'entrée (B-11 + hooks)

- É1-INSTALL : INSTALLE rc=0 (root présent, git_repo, 37 entrées KB) — no-op.
- Hook E1-RES : resource-monitor niveau 0 → mode d'exécution **PARALLELE** autorisé.
- 25ter clôturé (alias-eco v1.2.0, protocole rétabli, leçon L009) — publication au GO.
- gen-plan v3.23.2 byte-identique hôte ↔ dépôt ; PM-INSTALL v1.8.3 des deux côtés.

## Diagnostic — pourquoi gen-plan ne parallélise pas (réponse au « pourquoi »)

1. **SKILL.md §1.4 philosophie #4** : « Serial exécution by DEFAULT — Tâches UNE À LA UNE. Parallélisme INTERDIT sauf demande explicite. » — l'exécutant gen-plan est contraint au série par défaut, même sur des sous-tâches indépendantes.
2. **references/graph-diamond-pattern.md** : la parallélisation est qualifiée d'« exceptionnelle » (titre, hook §1.2bis) et l'anti-pattern n°3 interdit explicitement le « parallélisme par défaut » — le Graph Diamond n'est ouvert que sur justification explicite, donc presque jamais.
3. **PM installé** (PROMPT-MAITRE-GEN-PLAN v3.23.2, ligne philosophie #4) : forme renforcée « Le parallélisme est INTERDIT sauf demande explicite de l'utilisateur ET preuve que les sous-tâches sont indépendantes » — tout exécutant installé hérite du défaut série.
4. **Explication du constat propriétaire** : hors gen-plan, l'agent hôte suit sa consigne d'orchestration native (appels indépendants groupés en un seul message, agents lancés en parallèle dès que possible) → davantage de tâches en parallèle et une exécution plus rapide. C'est l'écart observé lors de la session de recherches web sur les disciplines.
5. **Constat de cohérence** : ce défaut contredit l'écosystème lui-même (fleet-engineering n°54 orchestrée par gen-plan à E5/E7 ; resource-monitor émet un mode PARALLELE ; SHARED §7 n°54 documente M2 fan-out). La philosophie #4 date des premières versions (présente dès v3.6.1) et n'a jamais été réalignée sur la matérialisation n°54.

## Fix — inversion du défaut (le « faire en sorte »)

**Philosophie #4 réécrite** : les sous-tâches **prouvées indépendantes** s'exécutent en **PARALLÈLE PAR DÉFAUT** (Graph Diamond ouvert automatiquement à E9-E14 dès que la preuve d'indépendance existe) ; le **série devient l'exception justifiée** (dépendance d'ordre, écriture partagée, pression ressource — verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC). Les gardes restent inchangées : preuve d'indépendance, verrous mono-writer, tracé worklog (Task IDs), re-verdict resource-monitor entre les vagues, arbitre sur l'ensemble fusionné, correct-work par phase.

**Semver** : 3.23.2 → **3.24.0** (MINOR — changement de comportement documenté, gardes conservées).

## Groupes d'exécution

- **G-A — Révisions gen-plan** : SKILL.md (frontmatter version+description ; §1.2bis ligne hook Graph Diamond ; §1.4 #4 réécrite ; §2.2 description graph-diamond-pattern.md) ; graph-diamond-pattern.md (titre, §1 principe, §3 conditions inversées, §4 anti-patterns requalifiés — « parallélisme sans preuve d'indépendance » et « sériographie par défaut » deviennent les anti-patterns) ; etapes-detaillees.md (E7 : partitionnement en vagues parallèles ; E9 : lancement en vagues) ; evals.json (+1 cas id 9 GP-diamond-defaut) ; semver 3.24.0.
- **G-B — Cascade KO-L004** : PM v3.24.0 généré mécaniquement (`generer-pm-skill.py --generate gen-plan`) ; archive v3.23.2 `git mv` byte-identité R4 ; SHARED §6.1 → v1.7.11 ; PM-INSTALL v1.8.4 (§2ter/§A.3) ; SYNC-CONTEXT ; README corpus ; ULTRA régénéré ; KB (en-tête + bullet) ; journal gen-plan.md ; arbitres recalibrés (CORPUS_ATTENDU, ECO_SKILLS, integrity manifest) ; propagation marqueur §0 ; miroir hôte → dépôt.
- **G-C — Tests** : py_compile scripts touchés ; arbitres rejoués ×2 (idempotence) : verify-cross, check-ecosysteme-integrity (round-trip archive), test-coherence-interactions, answer-key-checker ×2, check-triggers-replay (0 nouvelle dérive) ; alias selftest.
- **G-D — correct-work** : mode CIBLE (gen-plan + livrables) → rapport `download/rapport-correct-work-gen-plan-task26.md` ; verdict 0 S1/S2 requis.
- **G-E — Clôture** : worklog (template) + bilan E15 ; plan archivé miroir dépôt.

## Answer key (E1)

```yaml
decisions:
  - id: "D001"
    criterion: "Le diagnostic du défaut série est documenté avec les causes citées (SKILL.md §1.4 #4, graph-diamond-pattern.md, PM)"
    verification: "python3 -c \"import pathlib; t=pathlib.Path('skills/gen-plan/SKILL.md').read_text(); assert 'PARALLÈLE PAR DÉFAUT' in t; print('D001 OK')\""
    source: "demande utilisateur (« trouve pourquoi gen-plan ne le fais pas » — trace 1a169d11f4ff5b41)"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "La philosophie #4 du SKILL.md installé ouvre le parallélisme par défaut sur preuve d'indépendance, le série devient l'exception justifiée"
    verification: "python3 -c \"import pathlib; t=pathlib.Path('skills/gen-plan/SKILL.md').read_text(); assert 'Parallélisme INTERDIT' not in t; assert 'PARALLÈLE PAR DÉFAUT' in t and 'série' in t.lower(); print('D002 OK')\""
    source: "demande utilisateur (« fais en sorte qu'il le fasse ») ; cohérence SHARED §7 n°54"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "graph-diamond-pattern.md est aligné : titre sans « exceptionnelle », anti-patterns requalifiés (parallélisme sans preuve / sériographie par défaut)"
    verification: "python3 -c \"import pathlib; t=pathlib.Path('skills/gen-plan/references/graph-diamond-pattern.md').read_text(); assert 'exceptionnelle' not in t.lower(); assert 'sans preuve' in t; print('D003 OK')\""
    source: "cohérence interne gen-plan v3.24.0 (hook §1.2bis)"
    priority: "S2"
    status: "verified"
  - id: "D004"
    criterion: "PM v3.24.0 généré mécaniquement et v3.23.2 archivé R4 (git mv byte-identité)"
    verification: "test -f skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.24.0.md && test -f skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.23.2.md && echo D004 OK"
    source: "règle KO-L004 v1.1.0 (génération mécanique du PM à toute montée de version)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Cascade KO-L004 complète : SHARED, PM-INSTALL, SYNC, README, ULTRA, KB, journal portent les versions 3.24.0 / v1.7.11 / v1.8.4"
    verification: "rg -c 'v3\\.24\\.0' skills/KNOWLEDGE.md skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md skills/@historique/historiques-par-skill/gen-plan.md"
    source: "règle KO-L004 (recalibrage croisé) + convention §2quater"
    priority: "S2"
    status: "verified"
  - id: "D006"
    criterion: "Arbitres verts rejoués ×2 (idempotence) : verify-cross, integrity round-trip, coherence-interactions, answer-key-checker, replay 0 nouvelle dérive"
    verification: "python3 skills/gen-plan/scripts/answer-key-checker.py skills/gen-plan 2>/dev/null; python3 scripts/verify-cross.py 2>/dev/null | tail -1"
    source: "hook E7/E8 + KO-L003 (re-verdict après chaque vague)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "correct-work (CIBLE) sur gen-plan v3.24.0 et livrables : verdict PASS ou PASS AVEC RÉSERVES, 0 S1/S2"
    verification: "test -f download/rapport-correct-work-gen-plan-task26.md && rg -c 'S1|S2' download/rapport-correct-work-gen-plan-task26.md; echo 'D007 vérifié au rapport'"
    source: "hook correct-work par phase (§5.4) + couplage gen-plan"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Règle d'or n°2 respectée : 0 commit, 0 push pendant la tâche (modifications locales + dépôt, publication au GO)"
    verification: "git -C KNOWLEDGE-repo log --oneline -1; git -C KNOWLEDGE-repo status --short | wc -l > /dev/null && echo 'D008 OK (HEAD inchangé, publication au GO)'"
    source: "règle d'or n°2 (PM §1.8) — constante de session"
    priority: "S1"
    status: "verified"
```

## Estimation #token

- G-A ~2500 · G-B ~3500 · G-C ~1200 · G-D ~2000 · G-E ~600 — total ~9800 #token (coefficient 1.0, profil NORMAL, mode PARALLELE autorisé : les révisions G-A sont parallélisables par groupes de fichiers indépendants — application immédiate de la nouvelle règle).
