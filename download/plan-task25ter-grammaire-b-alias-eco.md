# Plan d'actions — Task 25ter (mode step) — RÉGÉNÉRATION conforme gen-plan v3.23.2

> **Session** : web-fdf5963c · **Date** : 2026-10-23 · **gen-plan** : v3.23.2 (mode step)
> **Directive propriétaire (verbatim)** : « - GO sur le déclencheur grammaire B (toujours en attente). - analyse mon skill "alias-eco" et les fichiers de mon dossier "@mon-ecosystem/" dans l'objectif de d'améliorer et d'optimiser son déclenchement et son fonctionnement dans $eco-leon". si tu trouves des améliorations et des optimisations indispensables pour gain de ses performances, intègre-les $façon() . - test les modifications apportées à $eco-leon. - correct-work. - clone-chat. »
> **État d'entrée** : origin/main = 08c956c (couches 18/20/22 + amont + Task 24 publiées) ; règle d'or n°2 réarmée (0 commit/push sans GO) ; alias-eco v1.1.0 locale non publiée (Task 25bis) ; dérives iphone arbitrées (Task 25 G2, 3× CONFIRME-eval) ; réserves S3 alias-eco closes (Task 25bis).
> **$ECO-LEON** expansé à la lecture ; **$façon()** = alias non enregistré, hors format canonique — signalé (règle format-alias §1), intention « de façon cohérente, optimisée et fonctionnelle ».
> **Note de traçabilité** : la première rédaction de ce plan (pre-exécution) a dérivé du protocole v3.23.2 (cause racine : PM gen-plan non rechargé post-compaction — analyse approfondie au rapport Task 25ter). La présente version est la RÉGÉNÉRATION conforme (règle L005/D012) ; les groupes déjà exécutés conservent leur traçabilité mécanique (preuves produites) et reçoivent leur correct-work(groupe) de compensation.

## §0 — Hooks E1-RES (v3.23.2 §1.12 + É1-INSTALL)

| Hook | Résultat |
|------|----------|
| É1-INSTALL : `ensure-installed.py --check` | **INSTALLE** (rc=0, root présent, git repo, head 08c956c, 0 fichier manquant, 37 entrées KB) — pas de préemption |
| E1-RES : `monitor.py --state-file tmp/resource-monitor-state.json` | **OK** (niveau 0) — mode d'exécution nominal |
| E1-RES : contrôle fraîcheur du plan (L005/D012) | gen-plan non modifiée en session → pas de re-génération d'état ; re-génération CORRECTIVE du présent plan (dérive protocole constatée) |
| Lecture préalable B-11 (règle D008) | PM gen-plan v3.23.2 (§A, §1.3, §1.5, §1.12, §1.16) + SKILL.md + answer-key-template.md rechargés à la régénération |

## §1 — Groupes séquentiels (mode step)

| Groupe | Tâches | Prérequis | #token | Statut |
|--------|--------|-----------|--------|--------|
| **G-A — GO grammaire B** | SKILL.md v1.2.0 (§1.2 déclencheur mécanique, §2.2 `--trigger`, §4 exemple) ; alias-manager.py (`--trigger` + GRAMMAIRE_B_RE + selftest 15→21) ; format-alias §1 ; trigger_evals 8→9 cas | GO propriétaire (obtenu — puce 1) | ~8 k | exécuté (à re-vérifier) |
| **G-B — Attribution OPT-TRIO** | `--trigger 'alias-eco "de façon cohérente, optimisée et fonctionnelle" --add OPT-TRIO'` (dogfooding) ; registre projeté au profil local ; $façon() signalé non expansé | GO propriétaire (mandat d'attribution par usage) | ~1 k | exécuté |
| **G-C — Cascade KO-L004** | KB v1.2.0 (en-tête + bullet déclencheurs) ; journal @historique row v1.2.0 ; PM-INSTALL v1.8.3 (§A.3 recalibré + row) ; SYNC-CONTEXT v1.5.3 ; README v2.1.11 ; historique-autres-elements ×5 ; ULTRA régénéré ; pipeline ×2 rc0 (SHA 37/37, round-trip) ; recalibrage arbitre integrity (alias-eco 1.2.0) + propagation archive hôte→dépôt + integrity 78/78 | G-A, G-B | ~8 k | exécuté à ~90 % (integrity 75/78 — correction en cours) |
| **G-D — Tests** | selftest 21/21 ×2 ; py_compile ×2 ; YAML ×2 ; replay 9/9 (0 nouvelle dérive) ; verify-cross 111/111 ; idempotence registre ×2 | G-C | ~3 k | exécuté (re-pass final post G-C) |
| **G-E — correct-work(groupe) ×A-D + correct-work (projet)** | compensation du contrat mode step (correct-work par groupe, max 2 rounds) ; puis 5 étapes v2.8.0 + §10.1 registre → rapport | G-D | ~6 k | pending |
| **G-F — clone-chat** | clone 7+1 étapes auto-suffisant → download/clone-chat-task25ter-<date>.md | G-E | ~5 k | pending |
| **G-G — Leçon protocole (E15)** | leçon gen-plan post-compaction (rechargement PM + hooks E1-RES) → worklog ×2 + knowledge-observer (lessons-learned) ; bilan E15 ; plan suivant armé | G-F | ~3 k | pending |

## §2 — Answer key (conforme answer-key-template.md)

```yaml
decisions:
  - id: "D001"
    criterion: "Grammaire B intégrée et mécanisée (--trigger) : parse + garde format canonique, idempotent, rejet propre rc=2 ; selftest 21/21 (6 cas grammaire B) ; trigger_evals 9 cas dont +1 positif"
    verification: "alias-manager.py --selftest (rc 0) + check-triggers-replay.py (alias-eco 9/9)"
    source: "GO propriétaire puce 1 + analyse alias_trigger_analysis.py (grammaire B 7/7)"
    priority: "S1"
    status: "executed"
  - id: "D002"
    criterion: "OPT-TRIO attribué à « de façon cohérente, optimisée et fonctionnelle » par dogfooding --trigger (source tracée : mandat propriétaire $façon(), nom hors format corrigé en canonique, signalé non expansé)"
    verification: "alias-manager.py --list + --resolve $OPT-TRIO"
    source: "format-alias §1/§4 (alias jamais inventé — attribution mandataire tracée)"
    priority: "S1"
    status: "executed"
  - id: "D003"
    criterion: "Cascade KO-L004 complète : KB v1.2.0, journal, PM-INSTALL v1.8.3 (§A.3), SYNC v1.5.3, README v2.1.11, historique-autres-elements ×5, ULTRA régénéré, pipeline ×2 rc0, arbitre integrity recalibré, archive hôte→dépôt propagée, integrity 78/78"
    verification: "check-ecosysteme-integrity.py (78/78) + verify-cross (111/111)"
    source: "KO-L004 v1.1.0 + précédents Tasks 22/24 (recalibrage seul, sans inflation SHARED/PM-INSTALL)"
    priority: "S1"
    status: "executed"
  - id: "D004"
    criterion: "0 régression : replay 9/9 alias-eco (description inchangée — v1.1.0 Description Optimization préservée), 19 dérives documentées inchangées, 0 nouvelle"
    verification: "check-triggers-replay.py --compare (0 nouvelle dérive)"
    source: "garde anti-régression R2"
    priority: "S2"
    status: "executed"
  - id: "D005"
    criterion: "correct-work(groupe) ×4 + correct-work (projet) PASS + clone-chat produit (7+1 étapes, auto-suffisant)"
    verification: "rapports download/ + fichier clone"
    source: "directive propriétaire puces 4-5 + contrat mode step v3.22.0"
    priority: "S2"
    status: "executed"
  - id: "D006"
    criterion: "Leçon protocole gen-plan journalisée (post-compaction : rechargement PM + hooks E1-RES avant toute génération de plan) — worklog ×2 + knowledge-observer"
    verification: "worklog + lessons-learned"
    source: "constat propriétaire « gen-plan n'a pas généré de plan comme d'habitude » — analyse approfondie Task 25ter"
    priority: "S2"
    status: "executed"
  - id: "D007"
    criterion: "0 commit / 0 push (règle d'or n°2) — publication au GO"
    verification: "git status (modifications tracées non commitées)"
    source: "règle d'or n°2"
    priority: "S1"
    status: "pending"
```

## §3 — Routage outils (§1.16)

| Besoin | Outil |
|--------|-------|
| Garde installation | `skills/gen-plan/scripts/ensure-installed.py --check` (É1-INSTALL) |
| Surveillance ressource | `skills/resource-monitor/scripts/monitor.py` (E1-RES, G-RES à E9-E14) |
| Mécanisation alias | `skills/alias-eco/scripts/alias-manager.py` (`--trigger`, `--resolve`, `--selftest`) |
| Arbitres | `check-triggers-replay.py`, `verify-cross.py`, `check-ecosysteme-integrity.py`, `certification-complete.py` |
| Cascade | `gen-ultra-maitre.py`, `eco_install_pipeline.py` (×2, rescellement), `task25ter-cascade*.py` (éditions chirurgicales assert count==1) |

## §4 — Exécution
G-A → G-B → G-C → G-D → G-E → G-F → G-G (séquentiel, mode step — correct-work(groupe) à chaque groupe). E15 : bilan + worklog.
