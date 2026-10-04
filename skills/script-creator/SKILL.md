---
name: script-creator
version: 1.1.0
category: ecosystem
language: fr
description: >
  Créer et modifier les scripts de l'écosystème (arbitres, collecteurs, outils de
  vérification stdlib) avec critères de succès et tests mécaniques intégrés. Utiliser
  lorsque l'utilisateur souhaite créer un script, corriger ou améliorer un
  script existant, rendre un check certifiable exécutable localement, ou garantir
  l'idempotence (rejeu ×2 sans effet) d'un outil. Structure, conventions
  de description héritées de skill-creator ; objectif principal : la création ou la
  modification des scripts (et non des skills).
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "Conventions de description, d'évals et de frontmatter (§1.4)"
  - skill: correct-work
    version: ">=2.6.0"
    used_at: "Validation des scripts produits (mode CIBLE, hook §1.3)"
  - skill: correct-py
    version: ">=1.0.0"
    used_at: "Post-traitement obligatoire des scripts Python produits — normes du langage (§1.3 GF-6)"
tags: [script, créer, scripts]
read_when:
  - Déclencher quand la demande concerne : créer et modifier les scripts de l'écosystème (arbitres, collecteurs, outils de vérification stdlib) avec crit…
  - Déclencher si la demande mentionne : créer, scripts, script
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Créateur de scripts

Un skill pour créer de nouveaux scripts et modifier des scripts existants de manière
sûre, testée et traçable.

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

script-creator industrialise la **création et la modification des scripts** de
l'écosystème : arbitres de vérification, collecteurs d'état, outils de transformation.
Il applique les règles fondamentales de l'écosystème au cas particulier des scripts :
persistance avant exécution (R9), Python stdlib d'abord (N3), vérification mécanique
(R-F2), lecture avant écriture (R-F3), boucles courtes (R-F4). La connaissance des
leçons de session (knowledge-observer L001/L003 — arbitrage local d'abord, auto-test
cas limites) fait partie intégrante de sa mission.

### §1.2 Le processus en 7 étapes

| Étape | Action | Sortie |
|-------|--------|--------|
| 1 | Comprendre la demande : entrées, sorties, critères de succès observables | critères listés |
| 2 | Brouillon du script : docstring d'intention, entrées/sorties, code de retour | fichier sous `scripts/` |
| 3 | Codifier les critères en vérifications mécaniques (grep, JSON, hachage) | checklist exécutable |
| 4 | Test simple : exécution contrôlée des critères | verdict PASS/FAIL |
| 5 | Itération par édition ciblée (patch de la ligne fautive, jamais réécriture totale) | script corrigé |
| 6 | Preuve d'idempotence : rejeu ×2 à l'identique (sorties ou hachages) | preuve ×2 |
| 7 | Traçabilité : worklog + verdict journalisé (règle d'or n°1) | entrée worklog |

### §1.3 Garde-fous

1. **Persistance avant exécution (R9)** : tout script de plus de ~10 lignes est écrit
   sous `scripts/` via un outil de fichier avant d'être exécuté — jamais en commande
   inline fragile ; en cas d'échec, on édite le fichier, on ne le régénère pas.
2. **Python stdlib d'abord (N3)** : aucune dépendance externe non justifiée ; JSON en
   sortie déterministe ; code de retour explicite (0 = succès).
3. **Idempotence ×2** : un script de vérification doit être rejouable à l'identique —
   arbitres en lecture seule, modifications gardées par marqueur ou hachage.
4. **Auto-test des cas limites (P2, gen-plan §1.14)** : tout arbitre générique embarque
   ses cas limites connus (entrées vides, fences complets, multi-lignes, racine absente)
   dans son test.
5. **Validation correct-work** : tout script destiné à devenir un livrable d'écosystème
   passe en mode CIBLE (hook de cette section) avant d'être déclaré fiable.
6. **Post-traitement correct-py (hook)** : tout script Python produit ou modifié passe
   le skill `correct-py` (conformité aux normes du langage — PEP 8 : style et nommage ;
   PEP 257 : docstrings ; conventions de commentaires) avant d'être déclaré terminé ;
   les corrections sont mécaniques, ciblées et idempotentes (jamais de réécriture
   totale, jamais la logique).

### §1.4 Déclencheurs et conventions héritées

- Manuel : « crée un script », « modifie ce script », « rend ce check exécutable »,
  « persiste ce code en script réexécutable ».
- De skill-creator, script-creator hérite : frontmatter avec dépendances versionnées,
  schéma d'evals (`evals/evals.json` + `evals/trigger_evals.json`), discipline de
  description (déclencheurs explicites, cas négatifs), itération par évaluation.

## §2 — SPÉCIFICATION TECHNIQUE

- **Langage** : Python 3 (stdlib uniquement) ; JSON pour les sorties machine.
- **Normes du langage (Python — PEP 8 / PEP 257)** : indentation 4 espaces ; identifiants
  en snake_case (le kebab-case reste réservé aux noms de fichiers) ; docstring de module
  en tête (PEP 257) et docstring par fonction publique ; commentaires en phrases
  complètes avec un espace après `#` ; shebang `#!/usr/bin/env python3` ; imports stdlib
  en tête du module ; code de retour explicite (`sys.exit(code)`) pour les outils. Les
  autres langages suivent leurs normes propres (shell : POSIX + en-têtes commentés ;
  JS : JSDoc). Le contrôle fin de ces normes est délégué au post-traitement
  `correct-py` (GF-6).
- **Localisation** : `{{SKILLS_ROOT}}script-creator/` pour le skill ; scripts produits
  sous `scripts/` à la racine du projet.
- **Nommage** : descriptif kebab-case pour les outils durables ; préfixe de session
  (`nXX-…`) pour les arbitres de session ; `_archive/` pour les retraités.
- **Structure type** : docstring d'intention en tête, constantes de chemins, fonctions
  pures, `main()` avec sortie JSON `ensure_ascii=False`, `sys.exit(code)`.
- **Test** : chaque critère est vérifiable par commande unique ; la preuve d'idempotence
  compare les sorties ou hachages de deux exécutions consécutives.

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|---------|
| skill-creator | hérite de | Conventions de description, d'évals et de frontmatter (>= 1.0.0) |
| gen-plan | servi par | R9 (persistance), §1.14 P1 (arbitrage local d'abord) |
| correct-work | valide via | Mode CIBLE sur les scripts produits (>= 2.6.0) |
| knowledge-observer | applique | Lessons L001/L003 (arbitrage local, auto-test cas limites) |
| correct-py | post-traitement | Conformité aux normes du langage (PEP 8/PEP 257) des scripts Python produits (>= 1.0.0, §1.3 GF-6) — exécuté après chaque utilisation |
| script-reviewer | relecture via | Grille G1-G8 sur les scripts produits avant adoption (>= 1.0.0) — homologue de la famille skill-creator |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; idempotence R1-R6 (gen-plan §1.11).
- Toute création/modification de script est tracée au worklog (règle d'or n°1) — jamais
  d'édition silencieuse.
- Non-duplication (SHARED §6.3) : script-creator ne redéfinit ni le processus de création
  de skills (skill-creator), ni la méthode de planification (gen-plan) — il couvre
  uniquement le cycle de vie des scripts.
