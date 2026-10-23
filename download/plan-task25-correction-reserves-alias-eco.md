# Plan d'actions — Task 25bis : correction des 2 réserves S3 alias-eco (mode step)

> **Session** : web-fdf5963c · **Date** : 2026-10-24 · **gen-plan** : v3.23.2 (mode step)
> **Entrée** : correct-work(alias-eco) PASS AVEC RÉSERVES — 2 × S3 ; `$ECO-LEON` expansé à la lecture.

## §1 — Diagnostic (preuve mécanique)

- **R1 (replay 5/8)** : `keywords_for` (SHARED §7 v2) extrait les radicaux de la **description** ;
  la clause finale « Ne pas déclencher pour l'inventaire des skills, le clonage de session ou la
  vérification de livrables (périmètres skills-inventory, clone-chat, correct-work) » émet les
  radicaux polluants `inventair, skill, clon, sess, livr` → les 3 cas négatifs (clone/inventaire/
  livrables) atteignent ≥ 2 radicaux → faux déclenchement. Cause racine = anti-pattern Description
  Optimization (pollution du routage par l'énumération des périmètres étrangers).
- **R2 (registre local absent)** : `eco_install_pipeline.py` étape 7 sync `@historique/@Alias/`
  (registre vivant) — la projection locale manque (installée avant création du registre 2026-10-23).

## §2 — Groupes séquentiels

| Groupe | Contenu | #token |
|--------|---------|--------|
| G-B | R1 : reformulation de la clause (sans radicaux étrangers) + semver 1.0.0→1.1.0 + refs internes (SKILL §2.3/§3, format-alias, script docstring/source) + cascade KO-L004 (KB en-tête, journal @historique/historiques-par-skill/alias-eco.md créé) + parité profil local | ~8 k |
| G-C | R2 : projection registre dépôt → profil local (byte-identité sha256, idempotence ×2) | ~1 k |
| G-D | Tests : py_compile, selftest 15/15, YAML, replay re-joué (alias-eco 8/8, 0 nouvelle dérive), verify-cross vert, --resolve local | ~3 k |
| G-E | correct-work (CIBLE alias-eco) re-joué → verdict ; rapport + worklog ×2 | ~3 k |

## §3 — Answer key

```yaml
decisions:
  - id: "D001"
    criterion: "R1 close : alias-eco 8/8 au replay voie M (0 faux positif négatif), description sans radicaux étrangers, semver 1.1.0, cascade KO-L004 complète, 0 nouvelle dérive"
    verification: "check-triggers-replay.py re-joué + py_compile + selftest 15/15"
    source: "diagnostic keywords_for + politique Description Optimization"
    priority: "S3"
    status: "executed"
  - id: "D002"
    criterion: "R2 close : @Alias/aliases.json projeté au profil local byte-identique (sha256), --resolve $ECO-LEON fonctionnel en local"
    verification: "sha256 ×2 idempotent + alias-manager.py --resolve local"
    source: "pipeline étape 7 (registre vivant)"
    priority: "S3"
    status: "executed"
  - id: "D003"
    criterion: "Baseline A2 non requise pour alias-eco (hors périmètre des 16 éléments « discipline ») — re-validation = replay voie M + trigger_evals/evals"
    verification: "constat plan"
    source: "plan-task25 G3 (périmètre A2 = 16 disciplines)"
    priority: "S4"
    status: "decided"
  - id: "D004"
    criterion: "0 commit / 0 push — GO propriétaire requis (règle d'or n°2)"
    verification: "git status propre (modifications non commitées intentionnellement)"
    source: "règle d'or n°2"
    priority: "S1"
    status: "pending (GO propriétaire — modifications non commitées tracées)"
```

## §4 — Exécution
G-B → G-C → G-D → G-E (séquentiel). E15 : bilan + worklog.
