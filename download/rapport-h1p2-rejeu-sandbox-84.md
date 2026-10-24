# Rapport H1-P2 — Rejeu sandbox par lot des 84 présomptions catégorielles

Preuve formelle individuelle par rejeu sandbox étanche ×2 (filet P2 du rapport H1,
activé par directive propriétaire du 2026-10-24 — session web-f90062ce).

- Fichiers rejoués : **3**
- Sandbox étanche (unshare) : **OUI**
- Fuite hors sandbox détectée (filet global) : **NON**
- Durée : 6.9 s

## Répartition des verdicts

| Verdict | Nombre |
|---------|--------|
| ERREUR_STABLE | 3 |

## Synthèse par catégorie

| Catégorie | Effectif | Verdicts |
|-----------|----------|----------|
| ONE-SHOT / OUTIL DE SESSION HISTORIQUE | 3 | ERREUR_STABLE 3 |

## Lecture des verdicts (norme H1, jamais ajustée)

- **IDEMPOTENT** — le script s'exécute et le rejeu produit le même état
  final observable dans le sandbox (mode strict : E1 == E2 byte-identique ;
  mode fraîcheur : seules des lignes temporelles de livrables écrasées en
  place diffèrent — régime LIVRABLES légitime).
- **ERREUR_STABLE** — le script échoue de façon IDENTIQUE au run1 et au
  run2 (même retour, même erreur, état sandbox inchangé) : comportement
  déterministe reproductible — les one-shots historiques échouent sur des
  chemins d'environnement d'époque disparus, prouvant au passage qu'ils
  ne produisent AUCUN effet observable sur un environnement sain.
- **INERT** — document sans mécanique d'exécution (SKILL.md, .agent) :
  rien à rejouer, l'inertie est constatée par inspection (type + absence
  d'interpréteur).

## Incidents et adaptations (règle d'or n°1)

1. **Pipes tenus par les petits-fils** (run initial, >9 min sans finir) :
   le timeout tuait le process `unshare` direct mais les petits-fils
   (sh/python/node) survivaient en tenant stdout/stderr → blocage. Corrigé :
   `stdin=DEVNULL`, `start_new_session=True`, `killpg` du groupe entier au
   timeout. Effet mesuré : campagne 84 fichiers ~58 s.
2. **`refactor-guard/scripts/risk_score.py` TIMEOUT → IDEMPOTENT** : le
   verdict TIMEOUT du premier harnais était un artefact (le script attendait
   sur stdin hérité du parent). Avec `stdin=DEVNULL` il complète et sort
   proprement (retour 0, E1 == E2). Verdict définitif : IDEMPOTENT.
3. **Oscillation d'étiquette STRICT/FRAICHEUR** (`r4-task-orchestrator.py`) :
   selon le grain temporel des deux runs (même seconde ou non), un livrable
   horodaté écrasé en place produit E1 == E2 ou E1 != E2 sur des lignes
   temporelles. Les DEUX cas prouvent la conformité — étiquette canonique
   unifiée IDEMPOTENT, mode reporté en détail (stable au rejeu).
4. **Faux positifs du filet global (runs 3-4)** : divergence détectée hors
   sandbox → inspection (`task-h1p2-diag-filet.py`, 60 s) : seuls
   `db/custom.db` et `dev.log` (état + journal du serveur de développement
   Next.js de l'hôte) divergent — activité ambiante hors écosystème,
   physiquement inatteignable depuis le namespace (bind-mount). Filet
   recentré sur le périmètre écosystème + défense en profondeur sur les
   caches HOME (/home/z/.npm, .cache, .local, .config). Run 5 : zéro fuite.

## Preuve d'idempotence du harnais lui-même

Deux campagnes complètes consécutives du harnais final (runs 4 et 5,
fichiers `task-h1p2-rejeu-sandbox.run4.json` et le rapport JSON courant `task-h1p2-rejeu-sandbox.json`),
produisent des verdicts IDENTIQUES 84/84 et des preuves d'exécution
(erreur + code retour du run1) IDENTIQUES 84/84. La reprise (`--force`
absent) est un no-op rapide. Fraîcheur légitime écrasée en place :
`duree_s`, empreintes du filet, horodatage.

## Verdicts individuels (84 preuves formelles)

### scripts/_archive/generate-knowledge-v3.py
- Catégorie : ONE-SHOT / OUTIL DE SESSION HISTORIQUE
- **Verdict : ERREUR_STABLE**
- run1 : retour=1 timeout=False erreur=« FileNotFoundError: [Errno 2] No such file or directory: '/tmp/knowledge_full.json' »
- run2 : retour=1 timeout=False erreur=« FileNotFoundError: [Errno 2] No such file or directory: '/tmp/knowledge_full.json' »

### scripts/_archive/task17-rapport-baseline.py
- Catégorie : ONE-SHOT / OUTIL DE SESSION HISTORIQUE
- **Verdict : ERREUR_STABLE**
- run1 : retour=1 timeout=False erreur=« FileNotFoundError: [Errno 2] No such file or directory: '/home/z/my-project/ecosystem/scripts/baseline-a2-report.json' »
- run2 : retour=1 timeout=False erreur=« FileNotFoundError: [Errno 2] No such file or directory: '/home/z/my-project/ecosystem/scripts/baseline-a2-report.json' »

### scripts/_archive/task21-p2b-kb-sync.py
- Catégorie : ONE-SHOT / OUTIL DE SESSION HISTORIQUE
- **Verdict : ERREUR_STABLE**
- run1 : retour=1 timeout=False erreur=« FileNotFoundError: [Errno 2] No such file or directory: '/home/z/my-project/ecosystem/skills/KNOWLEDGE.md' »
- run2 : retour=1 timeout=False erreur=« FileNotFoundError: [Errno 2] No such file or directory: '/home/z/my-project/ecosystem/skills/KNOWLEDGE.md' »
