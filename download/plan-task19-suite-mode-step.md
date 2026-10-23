# Plan d'actions — Task 19 (SUITE, mode step) : publication + amorçage opérationnel alias + résidus

> **Session** : web-fdf5963c · **Date** : 2026-10-23 · **gen-plan** : v3.23.2 (mode **step** — enchaînement autonome des groupes séquentiels, `correct-work(groupe)` après chaque groupe (max 2 rounds), `correct-work(projet)` en fin de chaîne)
> **Provenance** : directive propriétaire Task 18 — « lorsque les taches de ce nouveau plan d'actions seront toutes terminées alors génère un nouveau plan d'action pour effectuer les suivantes (mode "step") » ; plan généré à E15/F1 via gen-plan (le mécanisme est dorénavant systématique — leçon Task 18 consignée : l'enchaînement des plans passe TOUJOURS par gen-plan, y compris dans les projets à venir).
> **État d'entrée** : couche Task 18 terminée et certifiée (6/6 arbitres ALL PASS dépôt, 72/72 hôte) — tout est LOCAL (règle d'or n°2 : aucun commit/push sans GO).

## §1 — Classification (E1-E3)
Type 4 (méta-outil/écosystème) · complexité moyenne · profil NORMAL · les groupes 1-2 sont **bloqués sur entrée propriétaire** (GO + PAT), les groupes 3-4 sont exécutables à la demande.

## §2 — Groupes séquentiels (mode step)

| Groupe | Tâches | Prérequis | #token |
|--------|--------|-----------|--------|
| **G1 — Publication de la couche Task 18** | commit local (conventions git : `chore(écosystème): …`) → push HTTPS x-access-token (jeton ÉPHÉMÈRE en URL d'invocation uniquement — jamais persisté, audit anti-persistance post-push) → vérification distante anonyme (ls-remote) → journal B5 (commit de journalisation + push) | **GO propriétaire + PAT éphémère** | ~8 k |
| **G2 — Amorçage opérationnel du système d'alias** | (a) résolution à la lecture : tout `$<ALIAS>` des messages propriétaires est expansé avant interprétation (registre @historique/@Alias/) ; (b) à chaque `correct-work (projet)` sur une discussion : tenue du registre via alias-eco (délégation v2.8.0 §10.1) ; (c) proposition d'alias pour les phrases récurrentes détectées (attribution explicite propriétaire — jamais inventée) | discussions suivantes | ~4 k/session |
| **G3 — Résidus hérités (exécutables à la demande)** | re-mesure voie L du cas QUOTA agent-creator (429 durable — KO-L001) ; décision résiduelle éventuelle sur les 2 WARN de couverture PM (§1.13 gen-plan, §11 correct-work — héritage S4) | quota API disponible | ~6 k |
| **G4 — Rotation du PAT** | révocation/régénération du jeton GitHub exposé au canal de discussion (procédure propriétaire : Settings → Developer settings → Personal access tokens) — consigné depuis les Tasks 18/22/24 de l'ancienne campagne | côté propriétaire | ~1 k |

## §3 — Answer key (spécifications vérifiables)

```yaml
decisions:
  - id: "D001"
    criterion: "La couche Task 18 est publiée : origin/main avance de b75a620 au commit de couche puis au commit de journalisation, audit anti-persistance 0 occurrence"
    verification: "git ls-remote origin main (vérification distante anonyme) + grep anti-persistance"
    source: "règle d'or n°2 + pattern B5 (worklog Tasks 13-push/14-push)"
    priority: "S1"
    status: "pending"
  - id: "D002"
    criterion: "Le registre alias est tenu à jour à chaque correct-work(projet) et les $ALIAS des messages propriétaires sont expansés à la lecture"
    verification: "python3 skills/alias-eco/scripts/alias-manager.py --list (registre croissant, trié, dédupliqué)"
    source: "directive propriétaire Task 18 (skill alias-eco) + correct-work v2.8.0 §10.1"
    priority: "S2"
    status: "pending"
  - id: "D003"
    criterion: "Le cas QUOTA agent-creator est re-mesuré (voie L) ou re-consigné si quota toujours épuisé"
    verification: "présence du verdict re-mesuré au worklog/rapport de session"
    source: "restant propriétaire Task 17-final (héritage)"
    priority: "S3"
    status: "pending"
  - id: "D004"
    criterion: "Le PAT exposé est révoqué/régénéré côté propriétaire"
    verification: "confirmation propriétaire (aucune action agent possible)"
    source: "sécurité — consigné Tasks 18/22/24/13-push/14-push (ancienne campagne)"
    priority: "S2"
    status: "pending"
```

## §4 — Exécution (mode step)
Enchaînement autonome : G1 (si GO) → correct-work(groupe) → G2 (au fil des discussions) → G3 (sur demande) → G4 (rappel propriétaire) → correct-work(projet) en fin de chaîne. Les groupes bloqués sur entrée propriétaire sont journalisés en attente explicite (jamais contournés). E15 : bilan + génération du plan suivant via gen-plan (le mécanisme est permanent).
