# PROMPT MAÎTRE — Pipeline d'installation de l'écosystème personnel

Version : 1.0.0
Date : 2026-09-06
Dépend : PROMPT-MAITRE-SHARED.md (socle commun, à lire EN PREMIER)
Complète : INSTALL-ECOSYSTEME.md (périmètre P0-P7) — le présent fichier définit l'ORDRE D'EXÉCUTION OPTIMAL et les critères de passage.
Fonction héritée (SHARED §7) : ce pipeline applique la méthode prompt-engineering (méthode-mère : gen-plan, PM v3.7.0 §1.9) en tant que fonction héritée — chaque étape est un artefact de prompt (entrée, instruction, arbitre, sortie).

---

## §0 — Objet et règle zéro

Ce fichier est la **source de vérité de l'ordre d'exécution** pour installer l'écosystème Knowledge de façon optimale, reproductible et vérifiable, à partir du seul contenu du répertoire `mon-ecosysteme/`. Il synthétise le pipeline complet en une référence unique.

Règle zéro (SHARED §0) : skills auto-contenus sous `{{SKILLS_ROOT}}`, registre KB (`{{KB_PATH}}`) comme source de vérité, cross-references bidirectionnelles, conventions de nommage SHARED §1.2. Aucune étape ne produit d'effet public avant le passage des arbitres (§4).

Variables (SHARED §1.1) : `{{SKILLS_ROOT}}` = `skills/` · `{{KB_PATH}}` = `skills/KNOWLEDGE.md` · `{{KB_ENABLED}}` = `true` · `{{PROFILE_DEFAULT}}` = `NORMAL`.

## §1 — Pourquoi cet ordre (principe de dépendance)

L'ordre dérive du graphe d'interactions cartographié (README §8, SHARED §3.1) :

1. **Rien ne s'interprète sans le socle** — chaque fichier spécifique ouvre par « Lire SHARED en premier » (§B) → SHARED est l'étape 1.
2. **Rien ne s'installe depuis un corpus non authentifié** — les formes installées sont assemblées DEPUIS les PMs ; si le corpus est corrompu, tout le reste l'est → intégrité en étape 2.
3. **Le miroir précède l'installation** — `skills/_prompts-maitres/` garantit la byte-identité de la source avant toute transformation → étape 3.
4. **gen-plan avant les skills qu'il orchestre** — correct-work (Étape 1 : « gen-plan si dispo ») et clone-chat (§2.6 : intégration optionnelle) s'enregistrent auprès d'un gen-plan présent → étape 4.
5. **correct-work et clone-chat après gen-plan** — l'ordre P4-b/P4-c respecte le précédent validé (worklog A2/A3) et la direction de dépendance dominante (gen-plan —invoque→ correct-work) → étapes 5-6.
6. **Le registre KB après les skills** — KNOWLEDGE.md décrit les skills installés ; une entrée sans skill installé est une référence morte → étape 7.
7. **L'outillage avant la certification** — les arbitres vérifient l'état installé, ils ne le précèdent pas → étape 8.
8. **Rien ne se publie sans certification** — download/, archives et clones ne sont produits qu'après verdicts PASS → étapes 9-10.

## §2 — Le pipeline en 10 étapes (ordre d'exécution optimal)

| # | Étape | Source → Destination | Arbitre | Critère de passage |
|---|-------|----------------------|---------|--------------------|
| 0 | **Contexte** | Lire PROMPT-MAITRE-SHARED.md (§0-§7) + INSTALL-ECOSYSTEME.md | — | Conventions, variables, 22 relations connues |
| 1 | **Corpus** | Vérifier `mon-ecosysteme/` : 7 fichiers cœur + 8 `_archive/` | SHAs cœur vs clones scellés (verify-by-sha.py) | 15/15 présents, byte-identité cœur OK |
| 2 | **Miroir** | `mon-ecosysteme/` → `skills/_prompts-maitres/` (15 fichiers) | SHA src = SHA miroir | 15/15 byte-identiques |
| 3 | **gen-plan** | PM v3.7.0 §5 → `skills/gen-plan/` : SKILL.md (~202 L) + 5 `references/` (extraction §9, fences incluses) + `evals/evals.json` (6 evals) | Checks §6 du PM | 202 L ±tolérance ; 5 refs ; JSON valide |
| 4 | **correct-work** | PM v2.4.0 §5 → `skills/correct-work/SKILL.md` (assemblage §4+§A+§1+§2+§3+§10) | Checks §6 du PM | ~200-400 L ; 3 modes ; 5 étapes |
| 5 | **clone-chat** | PM v2.0.0 §5 → `skills/clone-chat/SKILL.md` (assemblage §4+§A+§1+§2+§3+§5) + `références/clone-template.md` (§9.1) | Checks §6 du PM | ~300-450 L ; 7+1 étapes ; template présent |
| 6 | **Registre KB** | INSTALL-ECOSYSTEME §9.1 → `skills/KNOWLEDGE.md` (9 entrées écosystème + verify-by-sha = 10) | Compte d'entrées + formats §2.2 SHARED | ≥ 9 entrées, versions exactes |
| 7 | **Outillage** | Déployer `scripts/` : verify-cross.py, sync-download.py, verify-by-sha.py, install/p4_install_skills.py | python -c import (syntaxe) | 4 scripts exécutables |
| 8 | **Certification** | Exécuter dans l'ordre : (a) verify-cross.py → (b) correct-work Mode PROJET → (c) verify-by-sha.py --manifest | Les 3 arbitres eux-mêmes | 60/60 ; 0 S1-S4 ; N/N authentiques |
| 9 | **Publication** | `sync-download.py --sync` (download/) + archive zip (round-trip) + worklog | Vérif round-trip byte-identique | 15/15 round-trip OK |
| 10 | **Clôture** | clone-chat (archivage session) + mise à jour KNOWLEDGE.md si nouveau skill | 8 checks S1-S8 clone-chat | Clone scellé, idempotent |

Note (correct-work CIBLE, 2026-09-06, S3 ; révisée session A9, 2026-09-06) : les skills sans prompt maître propre — `skills-inventory`, `skill-creator`, `autonomous-agent`, `fullstack-dev` — n'ont pas de forme installée locale : ils existent comme entrées du registre KB (étape 6) et sont mobilisés à l'exécution, pas à l'installation. `agent-prompt-engineering` est désormais MATÉRIALISÉ (forme installée `agent-prompt-engineering/` : SKILL.md + evals/evals.json + evals/trigger_evals.json + references/grille-evaluation-prompt.md ; recommandation clone 2026-09-06 §5.2 exécutée).

## §3 — Détail des points de contrôle critiques

### §3.1 Étape 1 — Intégrité du corpus
Comparer les SHAs SHA-256 des 7 fichiers cœur aux valeurs scellées dans les clones de référence (méthode neutral-line, Annexe D du PDF source ; canal R-1 = README §13). Toute divergence = STOP : restaurer depuis `download/mon-ecosysteme_archive.zip` ou le stockage versionné avant de reprendre au contrôle 1.

### §3.2 Étapes 3-5 — Assemblage des formes installées
Les SKILL.md sont ASSEMBLÉS depuis les PMs (jamais copiés à l'aveugle) : YAML frontmatter (§4 du PM) + règle zéro + spécifications (§1-§2) + relations (§3) + sections spécifiques. Les fichiers de référence sont extraits des blocs ```` ```markdown ```` du §9 avec fences incluses (round-trip déterministe, leçon A2) — l'extraction doit être insensible aux titres internes des blocs (logique de balance des fences).

### §3.3 Étape 8 — Arbitres et sévérité
L'ordre (a)→(b)→(c) est contraint : verify-cross valide la structure (rapide, déterministe), correct-work valide le raisonnement (coûteux, ne s'exécute que si la structure est saine), verify-by-sha valide l'authenticité historique. Toute sévérité S1 (critique) ou S2 (majeure) à l'étape 8 = retour à l'étape correspondante du pipeline ; S3/S4 = journalisation au worklog + reprise.

### §3.4 Incidents (règle d'or n°1, PM gen-plan §1.8)
Tout blocage (fichier absent, wipe inter-sessions, outil perdu) = signal d'adaptation, jamais un arrêt : contournement conforme aux conventions, journalisation au worklog (cause, solution, coût #token), reprise à l'étape en échec. Le wipe inter-sessions est un cas documenté : ré-exécuter ce pipeline depuis l'étape 2 (le corpus `mon-ecosysteme/` est la source de vérité restaurable).

## §4 — Interactions mobilisées par le pipeline (cartographie T2)

| Interaction | Mobilisée aux étapes | Nature |
|-------------|----------------------|--------|
| gen-plan —invoque→ correct-work | 3, 8(b) | E1 + hook E8 + contrôle par phase |
| gen-plan —utilise→ clone-chat | 3, 10 | E4, E15 (optionnel) |
| correct-work —utilise→ gen-plan | 4, 8(b) | Plan de vérification |
| correct-work —vérifie→ clone-chat | 5, 10 | Mode CIBLE (drifts) |
| clone-chat —enrichit→ KNOWLEDGE.md | 6, 10 | Descriptions §2 |
| skills-inventory —scanne→ KNOWLEDGE.md | 6 | Registre source |
| install-ecosystem —utilise→ infrastructure | 2-7 | Déploiement P6-P7 |
| gen-plan —délègue→ agent-prompt-engineering | 0-10 | Optimisation fine des prompts |

## §5 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| PROMPT-MAITRE-SHARED.md | Socle | Conventions, variables, registre relations (§3.1), méthode prompt-engineering (§7) |
| INSTALL-ECOSYSTEME.md | Périmètre | Ce fichier définit l'ORDRE et les critères ; INSTALL définit le PÉRIMÈTRE (26 fichiers, 4 zones, P0-P7) |
| PM gen-plan v3.7.0 | Spécification | Étape 3 (méthode-mère prompt-engineering, §1.9) |
| PM correct-work v2.4.0 | Spécification | Étape 4 + arbitre étape 8(b) |
| PM clone-chat v2.0.0 | Spécification | Étape 5 + clôture étape 10 |
| README.md | Documentation | §9 architecture, §10 workflows, §12 verify-cross, §13 canal R-1 |

## §6 — Maintenance

- Toute évolution du périmètre (nouveau PM, nouveau skill) se traduit par : mise à jour de la table §2 + entrée KNOWLEDGE.md + cross-references bidirectionnelles (SHARED §3.2).
- L'ordre des étapes 3-5 suit le précédent P4-a/P4-b/P4-c ; il ne doit être modifié qu'avec un changement de contrat documenté (SHARED §3.2 règle 5).
- Ce fichier est documentaire et orchestration : il ne détient pas la méthode prompt-engineering (fonction héritée, SHARED §7) et ne remplace ni INSTALL-ECOSYSTEME.md ni les §5 des PMs.

## §7 — Historique

| Version | Date | Changements |
|---------|------|-------------|
| v1.0.0 | 2026-09-06 | Création (directive utilisateur) : pipeline 10 étapes issu de la cartographie des interactions ; principes de dépendance §1 ; critères de passage et arbitres §3 ; intégration règle d'or n°1 et canal R-1. Certification correct-work Mode CIBLE : PASS 31/31, 0 S1-S2, 1 S3 corrigée (note skills sans PM) |
