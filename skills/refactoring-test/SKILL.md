---
name: refactoring-test
version: 1.0.1
category: ecosystem
language: fr
tags:
  - refactoring-test
  - refactoring
  - detection
  - dette-technique
  - blast-radius
  - graphe-interactions
  - evaluation
  - verdict-machine
description: >-
  Skill outil refactoring test : détecteur/évaluateur des situations de refactoring — reconnaître les situations où un refactoring devient nécessaire (signaux : duplication, dérive de terminologie, versions divergentes, asymétries KB, réserves récurrentes, churn de cascade, complexité des procédures), évaluer ces situations (risque, urgence, portée — scoring principal/intérêt adapté de SQALE), et générer un graphe d'interactions (depuis la KB + dependencies YAML) pour estimer l'impact (blast radius) des modifications futures. Verdict machine-à-machine OK/PRESSION/CRITIQUE consommable par tout élément de l'écosystème (gen-plan, agents, disciplines, scripts). PRODUCTEUR D'INFORMATION : ne modifie rien — l'exécution appartient à refactoring-engineering ; l'indépendance de l'évaluateur vis-à-vis de l'exécutant est la garantie anti-auto-certification. Bras mécanique : scripts/refactoring-test-graph.py (stdlib). Outil de la discipline refactoring-engineering (n°55 — source de vérité : SHARED §7) : refactoring-engineering se sert de refactoring-test comme un outil d'évaluation ; refactoring-test n'est PAS une discipline (correction directive propriétaire, Task 8) et reste appelable par tout élément (gen-plan, agents, disciplines, scripts). Fondements documentés : references/fondements-academiques.md.
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "détenteur principal — détection/évaluation à E4/E7 et en exécution E9-E14 (§8)"
read_when:
  - Déclencher quand la demande concerne : reconnaître ou évaluer une situation de refactoring — signaux de dette technique, scoring de risque/urgence/portée, verdict de nécessité.
  - Déclencher si la demande mentionne : refactoring nécessaire, évaluer un refactoring, blast radius, graphe d'interactions, impact d'une modification, dette technique, scan de signaux, re-scan post-opératoire.
  - Ne pas déclencher pour l'EXÉCUTION d'un refactoring (refactoring-engineering) ni pour une vérification post-hoc générique (correct-work).
---

## §0 — Contexte Système (SHARED v1.7.6)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

1. **Auto-contenu** : ce skill porte tout ce dont il a besoin ; pas de référence hors écosystème hors `references/`.
2. **Versionné semver** : toute modification majeure de comportement → bump MINOR/MAJOR + KB synchronisé.
3. **KB source de vérité** : la description et la version du présent SKILL.md sont répliquées dans `{{KB_PATH}}`.
4. **Dépendances déclarées** : YAML `dependencies` uniquement ; pas d'import implicite.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission
Reconnaître les SITUATIONS où un refactoring est nécessaire, les ÉVALUER (risque, urgence, portée) et produire un GRAPHE D'INTERACTIONS qui estime l'impact (blast radius) des modifications futures — y compris celles du skill `refactoring-engineering` lui-même. Le skill est un producteur d'information : il émet un verdict machine-à-machine consommable par tout élément (gen-plan à E4/E7 et en exécution, agents, disciplines, scripts) et ne modifie JAMAIS la cible évaluée. Son indépendance vis-à-vis de l'exécutant (refactoring-engineering) matérialise la règle d'anti-auto-certification : l'exécutant ne s'auto-évalue pas.

### §1.2 Modes
- **M1 SCAN (défaut)** — détection de signaux sur une cible (skill, corpus, scripts, discipline) : duplication et doubles sources, dérive de terminologie (terme déprécié résiduel), versions divergentes entre arbres/KB/corpus, asymétries d'arêtes KB, réserves récurrentes non résorbées, churn de cascade (re-mécanisations répétées), complexité des procédures (nombre de gardes manuelles).
- **M2 ÉVALUATION** — scoring d'une situation détectée : principal (coût de remédiation estimé) vs intérêt (coût de non-remédiation — fréquence d'usage de la cible, exposition des cascades), urgence (le signal progresse-t-il ?), portée (locale/systémique). Sortie : fiche d'évaluation + verdict.
- **M3 GRAPHE** — génération du graphe d'interactions depuis la KB (arêtes **Dépend de**/**Utilisé par**) + dependencies YAML des frontmatters ; reachability forward (ce dont la cible dépend) et backward (ce qui dépend de la cible) ; blast radius quantifié ; verdict OK/PRESSION/CRITIQUE (seuils §1.3).
- **M4 POST-VOL** — re-scan indépendant après une opération de refactoring : delta de signaux avant/après, verdict de non-régression informationnel (complète les arbitres mécaniques, ne les remplace jamais).

### §1.3 Verdict machine
| Verdict | Critères (cumulatifs) | Conséquence pour l'appelant |
|---------|----------------------|------------------------------|
| OK | 0-3 signaux mineurs ; blast radius < 4 éléments | Refactoring non nécessaire ; opportuniste possible |
| PRESSION | ≥ 4 signaux OU blast radius 4-7 OU intérêt croissant | Refactoring recommandé au prochain cycle ; planifier via gen-plan E4 |
| CRITIQUE | ≥ 7 signaux OU blast radius ≥ 8 OU signal bloquant (double source de vérité, version divergente sur élément pivot) | Refactoring nécessaire ; opération déclarée par refactoring-engineering avant toute nouvelle évolution de la cible |

### §1.4 Mécanismes écosystème
Source d'arêtes : registre KB ({{KB_PATH}}) parsé mécaniquement (sections **Dépend de**/**Utilisé par**) — même convention que l'arbitre `test-coherence-interactions.py` ; enrichissement : frontmatters `dependencies` des SKILL.md. Traçabilité : tout verdict est journalisé (worklog) avec sa liste de signaux et le graphe projeté (JSON). Le verdict est une ENTRÉE de décision (gen-plan E4/E7) — jamais une autorité d'exécution (R3 : un verdict non journalisé n'est pas exigible).

### §1.5 Règles opérationnelles
1. **Ne modifie rien** : M1-M4 sont en lecture seule ; toute proposition de correction est ROUTÉE vers refactoring-engineering, jamais appliquée.
2. **Indépendance** : l'évaluateur d'une opération ne peut être l'exécutant de cette opération (anti-auto-certification — fondement : les revues seules ratent des régressions).
3. **Signaux nommés** : chaque signal cité porte sa preuve (fichier, occurrence, arête) — pas de signal intuitif.
4. **Verdict reproductible** : deux exécutions sur le même état produisent le même verdict (déterminisme ; le bras mécanique est stdlib).
5. **R3** : un verdict non journalisé (worklog) est « en attente de journalisation », jamais « rendu ».

### §1.6 Fondements (outil de la discipline n°55, 2026-10-12)
Détection multi-signaux (taxonomies de code smells — Fowler ; hotspots = complexité × fréquence de changement — Tornhill) ; dette principal/intérêt (SQALE — Letouzey ; Krauchanka) ; impact par graphe de dépendances et reachability (change impact analysis — program dependency graphs) ; blast radius avant action d'agent ; évaluation indépendante de l'exécution (characterization/golden master — Feathers ; fitness functions automatisées). Détail et sources : `references/fondements-academiques.md`.

## §2 — SPÉCIFICATION TECHNIQUE
Bras mécanique : `scripts/refactoring-test-graph.py` (stdlib — re/json/sys) : parse la KB → graphe dirigé (A dépend de B) ; modes : `--target <skill>` (M3 — blast radius backward/forward + verdict), `--graph` (export complet), `--json` (sortie machine : scripts/refactoring-test-report.json). Idempotent ×2 (même état = même sortie). Les modes M1/M2/M4 sont des procédures de session (checklist §1.2) journalisées au worklog ; leurs preuves citent les arbitres existants (test-coherence-interactions, verify-cross, check-ecosysteme-integrity) comme sources de signaux.

## §3 — RELATIONS (extrait de SHARED §3.1)
- `gen-plan` — détenteur principal : détection/évaluation à E4 (conception) et E7 (re-validation), situations en E9-E14.
- `refactoring-engineering` — consommateur obligatoire : pré-vol (M2/M3 avant toute opération) et post-vol (M4) ; l'opposé de la dépendance d'exécution.
- `correct-work` — complémentarité : correct-work vérifie/corrige post-hoc ; refactoring-test détecte/évalue en amont ; les deux verdicts se citent mutuellement.
- `graph-engineering` — même convention de graphe KB (arêtes bidirectionnelles versionnées) ; refactoring-test est un CONSOMMATEUR du graphe.
- `harness-engineering` — les signaux de pression/qualité du harnais alimentent M1 ; le verdict alimente les boucles.

## §4 — CONVENTIONS
Kebab-case ; semver strict ; verdicts OK/PRESSION/CRITIQUE (même vocabulaire que resource-monitor) ; journalisation worklog obligatoire (signaux + preuves + verdict) ; aucune fabrication de signaux (R3) ; lecture seule sur toute cible évaluée.

## §5 — ÉVALUATIONS ET DÉCLENCHEURS
`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs — voisins correct-work et graph-engineering) ; déclenchement attendu sur les requêtes de détection/évaluation/impact de refactoring explicites ; seuil de routage 0.5. Baseline A2 : EN ATTENTE (QUOTA_OK — directive ; précédent n°54 : mesurée en Task dédiée). La voie mécanique M3 est testable sans QUOTA (`--target` sur la KB).

## §6 — TRAÇABILITÉ
- v1.0.1 (2026-10-12, session web-b4d7dd19 Task 8 — gen-plan(step), fusion discussion externe 468a4c26) : correction de déclaration — refactoring-test n'est PAS une discipline ; il est l'OUTIL de la discipline refactoring-engineering (n°55) qui se sert de lui comme d'un outil d'évaluation indépendant (directive propriétaire explicite) ; frontmatter déquoté (S4 — valeur inchangée dans le bump).
- v1.0.0 (n°55, 2026-10-12, session web-b4d7dd19 Task 7 — gen-plan(step) G3/G4) : matérialisation de la discipline refactoring test (directive propriétaire : détecteur/évaluateur + graphe d'interactions pour estimer l'impact des modifications futures de refactoring-engineering) ; sources : recherche web approfondie (rapport Task 7) ; intégration gen-plan v3.23.1 §1.6 bloc n°55 ; baseline A2 en attente QUOTA.

## §7 — RÉFÉRENCES
- `references/fondements-academiques.md` — sources vérifiées de la recherche web (détection, SQALE, impact analysis, blast radius, anti-auto-certification).
- SHARED §7 (PROMPT-MAITRE-SHARED.md, corpus) — source de vérité des disciplines.
- gen-plan v3.23.1 (SKILL.md) §1.6 bloc n°55 — orchestration E4/E7/E9-E14.
- `scripts/refactoring-test-graph.py` — bras mécanique (graphe + verdict).

## §8 — Rattachement à la discipline n°55 (décentralisé du SHARED §7)

refactoring-test est l'OUTIL de la discipline `refactoring-engineering` (n°55) — non une discipline (correction directive propriétaire, Task 8, session web-b4d7dd19 : « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil » ; fusion discussion externe 468a4c26). Détenteur principal : gen-plan (E4/E7 + situations E9-E14) ; consommateur obligatoire : refactoring-engineering (pré-vol/post-vol — anti-auto-certification) ; appelable par tout élément (agents, scripts, disciplines).
