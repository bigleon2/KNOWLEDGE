---
name: inter-scripts
version: 1.0.0
category: ecosystem
language: fr
tags:
  - "#inter-scripts"
  - "#orchestration"
  - "#multi-langages"
  - "#graph-engineering"
  - "#fleet-engineering"
description: >
  Orchestre la communication entre les scripts de l'écosystème écrits dans des
  langages différents (C++, Python, …) : registre des nœuds (scripts, langage,
  interface, capacités), client générique multi-canaux (one-shot fichiers JSON,
  pipe stdin, daemon socket UNIX NDJSON multi-clients) et orchestrateur
  multi-projets qui — par graph engineering (tri topologique de Kahn, détection
  de cycles, niveaux d'exécution) et fleet engineering (fan-out ThreadPool par
  niveau = M2, pipeline entre niveaux = M3, Task IDs préfixés par projet,
  agrégation arbitrée, journal JSON) — génère et adapte ses canaux de
  communication À L'ÉVOLUTION DES PLANS D'ACTIONS de chaque projet : tâche
  isolée → one-shot ; ≥ 2 tâches restantes sur un nœud concurrent (même projet
  ou projets distincts) → daemon socket maintenu et réutilisé ; sortie→entrée
  chaînée → handoff par fichier typé. Canal trigo-euler (dessin-technique).
dependencies:
  - skill: graph-engineering
    version: ">=1.0.1"
    used_at: "graphe de tâches multi-projets : nœuds/arêtes, Kahn, cycles (M1-M3)"
  - skill: fleet-engineering
    version: ">=1.0.1"
    used_at: "patterns M2 fan-out / M3 pipeline, Task IDs, agrégation arbitrée"
  - skill: dessin-technique
    version: ">=1.3.0"
    used_at: "nœud trigo-euler (C++) du registre — canal démon multi-clients"
  - skill: script-creator
    version: ">=1.1.0"
    used_at: "conventions de création/évolution des scripts du registre"
read_when:
  - Déclencher quand la demande concerne : faire communiquer des scripts écrits dans des langages différents, orchestrer des appels de scripts depuis un plan d'actions, exécuter plusieurs tâches simultanément sur un même binaire (concurrence), choisir un canal de communication (one-shot, pipe, socket, fichier typé)
  - Déclencher si la demande mentionne : inter-scripts, canal, daemon, socket, orchestration de scripts, graphe de tâches, fan-out de scripts, multi-langages, trigo-euler daemon
  - Ne pas déclencher hors de ce périmètre (orchestration d'AGENTS → fleet-engineering ; documents → pdf/docx)
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

inter-scripts matérialise la COUCHE DE COMMUNICATION INTER-SCRIPTS de l'écosystème : tout script, quel que soit son langage, devient un nœud appelable par tout plan d'actions, via le canal le mieux adapté à l'état courant des plans. Le skill ne remplace ni graph-engineering (discipline, source SHARED §7) ni fleet-engineering (patterns M1-M5) : il les OPÉRATIONNALISE au niveau des scripts et des processus — nœuds = scripts/binaires, arêtes = dépendances de données sortie→entrée, flotte = processus concurrents. Son premier locataire est le binaire C++ `trigo-euler` (skill dessin-technique), appelé simultanément par plusieurs tâches de plans d'actions via son démon socket.

### §1.2 Composants

| Composant | Rôle |
|-----------|------|
| `scripts/registre.json` | Source de vérité des nœuds : id, langage, chemin/binaire, interface (json-ndjson, cli-fichiers), modes (one-shot/stdin/daemon), paramètres daemon (socket, ready-file, pid-file, max_clients), capacités, concurrent oui/non, skill propriétaire. Déclare aussi les 4 canaux et la règle de sélection. |
| `scripts/is_client.py` | Client générique (`Client(script)`) : `appeler(op, args, canal)` — canal auto (daemon si vivant), démarrage paresseux du démon (ready-file + health-check `echo`), repli one-shot fichiers JSON ; CLI `--script X --op Y --args '{…}'` et `--daemon demarrer\|arreter\|etat`. |
| `scripts/orchestrer.py` | Orchestrateur multi-projets : `--plans p1.json p2.json [--verifier|--executer] [--out-dir D]` — cf. §1.3. |

### §1.3 Orchestrateur (graph + fleet engineering)

- **Graph engineering** : chaque plan (un par projet) déclare des tâches `{id, script, op|cmd, args, deps, out}` ; l'orchestrateur construit le graphe multi-projets, exécute le tri topologique de Kahn en NIVEAUX (diamond), et REJETTE tout cycle avec verdict explicite `CYCLE_DETECTE` (rc=1, liste des nœuds impliqués).
- **Canaux adaptés à l'évolution des plans** : à chaque exécution, l'état restant de TOUS les plans est relu ; la règle du registre s'applique — 1 tâche restante sur le nœud → `one-shot` ; ≥ 2 tâches restantes (même niveau ou projets distincts) sur un nœud `concurrent: true` → `daemon-socket` (démarré/vérifié paresseusement, réutilisé par toutes les tâches) ; tâche avec deps (sortie→entrée) → `fichier-typé`. Chaque décision porte sa rationale dans le journal.
- **Fleet engineering** : exécution niveau par niveau (pipeline M3) ; tâches d'un niveau lancées simultanément en ThreadPoolExecutor (fan-out M2) ; Task IDs préfixés par projet (`projet/T1`) ; agrégation unique avec verdict global PASS/ECHEC ; journal JSON (`journal.json`) : graphe (nœuds, arêtes, niveaux, canaux), entrée par tâche (statut, canal, durée, sha16 de la sortie).
- **Idempotence** : ré-exécuter le même plan → sorties byte-identiques (sha16 égaux) pour tout nœud déterministe — vérifié en G3/G5 mission TRIGO-INTER-SCRIPTS.

### §1.4 Règles opérationnelles

1. **Registre d'abord** : tout nœud appelé doit être inscrit au registre (sinon ValueError) — pas d'appel implicite hors graphe.
2. **Un démon par nœud concurrent** : socket UNIX + ready-file + pid-file ; le client vérifie la vitalité (`echo`) avant réutilisation ; arrêt propre par op `daemon.stop` (socket supprimée).
3. **Saturation maîtrisée** : au-delà de `max_clients`, le démon répond `daemon sature` sans bloquer (jamais de file d'attente silencieuse).
4. **Traçabilité** : toute exécution réelle est journalisée (Task ID, canal, sha16) ; les preuves vont dans `tmp/` de la mission.
5. **Zéro-régression** : l'ajout d'un nœud au registre ne modifie jamais un script existant ; les évolutions de canal sont consignées au journal, jamais codées en dur.
6. **R3** : un résultat non vérifié mécaniquement reste « en attente de validation ».

### §1.5 Mémoire

État Long : registre.json (nœuds/canaux), KB (entrée du skill), worklog des missions. État Court : le journal d'exécution courant (graphe, décisions de canal, sorties).

## §2 — SPÉCIFICATION TECHNIQUE

- Python 3 std uniquement (json, socket, subprocess, threading/concurrent.futures) ; protocole JSON strict ; NDJSON (une requête/réponse par ligne) sur socket UNIX.
- Format plan : `{"projet": str, "taches": [{"id", "script", "op"|"cmd", "args"?, "deps"?, "out"?}]}`.
- Scripts JSON-protocole (champ `binaire` au registre) : requête/réponse JSON ; scripts CLI (champ `script`/`cmd`) : code retour + fichiers déclarés.
- Preuves mission de création : `tmp/mission-voss/trigo-inter-scripts/` (concurrence 4×25 = 100/100, mini-plans ×2 idempotents, cycle rejeté, chaîne joint-v2 ×2 idempotente).

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| graph-engineering | opérationnalise (niveau scripts) | Kahn, cycles, niveaux — discipline : SHARED §7 |
| fleet-engineering | opérationnalise (niveau processus) | M2 fan-out, M3 pipeline, agrégation arbitrée |
| dessin-technique | consomme | nœud `trigo-euler` (C++, daemon multi-clients) inscrit au registre |
| script-creator | consulte | conventions de création des scripts inscrits |

## §4 — CONVENTIONS

Kebab-case ; semver strict ; journal JSON en `tmp/` de mission ; aucune fabrication de résultat (R3) ; toute évolution du registre passe par une révision versionnée de `registre.json` (champ `version`).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS

- `evals/evals.json` : 4 évals (registre, client daemon, orchestration + cycles, idempotence).
- `evals/trigger_evals.json` : 4 cas (3 positifs, 1 contrôle négatif) au format LISTE.

## §6 — TRAÇABILITÉ

- **v1.0.0 (mission TRIGO-INTER-SCRIPTS, Task ID 10, 2026-10-23, session web-da654199)** : création sur directive propriétaire — « génère un skill inter-scripts (cohérent, optimisé et fonctionnel) qui aura pour objectif d'orchestrer cette communication en générant et en orchestrant (utilisant au mieux le graph et le fleet engineering) ses canaux de communications adaptés en fonctions de l'évolution des plans d'actions de chaque projet ». Preuves : concurrence 100/100, mini-plans ×2 idempotents, cycle détecté, chaîne joint-v2 ×2.

## §7 — RÉFÉRENCES

- `skills/graph-engineering/SKILL.md` — discipline graphe (SHARED §7).
- `skills/fleet-engineering/SKILL.md` — patterns de flotte M1-M5.
- `skills/dessin-technique/scripts/trigo-euler.cpp` — premier nœud C++ du registre.
- `skills/KNOWLEDGE.md` — entrée du registre KB.
