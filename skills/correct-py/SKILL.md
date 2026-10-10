---
name: correct-py
version: "1.1.0"
category: ecosystem
language: fr
description: >
  Vérifier et corriger la conformité des scripts Python de l'écosystème aux normes
  d'écriture du langage (PEP 8 : style, indentation, nommage snake_case ; PEP 257 :
  docstrings de module et de fonctions ; conventions de commentaires) par analyse
  AST/tokenize stdlib, via corrections mécaniques ciblées et idempotentes et rapport
  JSON déterministe. Utiliser lorsqu'un script Python vient d'être généré ou modifié par
  script-creator (post-traitement obligatoire, garde-fou 6 §1.3 — exécuté APRÈS chaque
  utilisation), lorsqu'un script existant doit être audité ou normalisé aux normes
  Python, ou lorsqu'une vérification de style mécanique est requise préalablement à la relecture
  script-reviewer. Non concerné : création de scripts (script-creator), relecture
  fonctionnelle G1-G8 (script-reviewer), validation d'écosystème (correct-work),
  création de skills (skill-creator).
  Commentaires corrigés, blancs parasites supprimés, style et indentation normalisés.
dependencies:
  - skill: script-creator
    version: ">=1.0.0"
    used_at: "Scripts entrants du post-traitement (§1.1, §3)"
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "Conventions de description, d'évals et de frontmatter (§1.4)"
tags: [script, python, style]
read_when:
  - Déclencher quand la demande concerne : vérifier et corriger la conformité des scripts Python de l'écosystème aux normes d'écriture du langage (PEP 8…
  - Déclencher si la demande mentionne : script, python, style
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Correcteur Python (normes du langage)

Un skill pour vérifier et corriger la conformité des scripts Python de l'écosystème aux
normes PEP 8 / PEP 257 de manière mécanique, idempotente et traçable — le
post-traitement obligatoire de script-creator.

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

correct-py industrialise la conformité aux normes du langage Python des scripts produits
par script-creator : un script fonctionnellement correct mais non conforme à PEP 8 /
PEP 257 (style, docstrings, commentaires) n'est pas terminé. Le skill s'exécute APRÈS
chaque utilisation de script-creator (post-traitement, garde-fou 6 de script-creator
§1.3) et avant la relecture script-reviewer (convergence). Il n'altère jamais la logique
du script : les corrections sont mécaniques et de style uniquement, ciblées, idempotentes
(marqueur ou hachage), et chaque intervention est tracée au worklog (règle d'or n°1).
Sa connaissance des leçons de session (knowledge-observer L003 — auto-test des cas
limites ; L005 — garde post-édition) fait partie intégrante de sa mission.

### §1.2 Le processus en 5 étapes

| Étape | Action | Sortie |
|-------|--------|--------|
| 1 | Scanner le script : analyse AST + tokenize stdlib contre le lexique de conformité (§2) | inventaire des écarts |
| 2 | Rapport de conformité déterministe (JSON) : écarts par catégorie (P8 style / P25 docstrings / CM commentaires / SR structure) | rapport |
| 3 | Mode VÉRIF : lecture seule, verdict CONFORME / NON_CONFORME, code retour explicite | verdict |
| 4 | Mode CORRECT : corrections mécaniques ciblées idempotentes (blancs parasites, commentaires, indentation tabulation — jamais les chaînes de caractères ni la logique) | script corrigé |
| 5 | Re-verdict ×2 à l'identique + traçabilité worklog | preuve ×2 + entrée worklog |

### §1.3 Garde-fous

1. **Lecture seule en mode VÉRIF** : aucun artefact modifié ; idempotence ×2 triviale.
2. **Corrections mécaniques ciblées (R-F3 : lire avant d'écrire)** : jamais de réécriture
   totale d'un script ; la logique fonctionnelle n'est pas altérée (frontière avec
   script-creator étape 5) ; les chaînes de caractères et docstrings existantes ne sont
   jamais retouchées (zones protégées par tokenize).
3. **Idempotence ×2** : rejouer le mode CORRECT sur un script déjà corrigé = 0
   modification (preuve par comparaison de rapports ou hachages).
4. **Auto-test des cas limites (P2, gen-plan §1.14)** : fichier vide, shebang/coding en
   tête, chaînes multi-lignes avec blancs parasites (ne doivent PAS être corrigés),
   docstring manquante, encodage non UTF-8 → verdicts propres sans crash.
5. **Escalade** : un écart non corrigeable mécaniquement (docstring à rédiger, refonte de
   nommage, style ambigu) est RAPPORTÉ (verdict NON_CONFORME) et escaladé au processus
   script-creator (étape 5) puis script-reviewer / correct-work — jamais étouffé.

### §1.4 Déclencheurs et conventions héritées

- Automatique : post-traitement obligatoire après chaque utilisation de script-creator
  (garde-fou 6 §1.3) — hook de cette section.
- Manuel : « vérifie la conformité PEP 8 de ce script », « corrige les docstrings et
  commentaires », « normalise ce script Python aux normes du langage ».
- De skill-creator, correct-py hérite : frontmatter avec dépendances versionnées, schéma
  d'evals (`evals/evals.json` + `evals/trigger_evals.json`), discipline de description
  (déclencheurs explicites, cas négatifs), itération par évaluation.

## §2 — SPÉCIFICATION TECHNIQUE

- **Lexique de conformité (Python)** :
  - **P8 (PEP 8 — style)** : indentation 4 espaces (0 tabulation d'indentation) ;
    identifiants de fonctions en snake_case (rapport seulement — un renommage mécanique
    casserait les appelants) ; 0 blanc parasite en fin de ligne (W291/W293) ; fin de
    fichier par un unique saut de ligne (W292) ; imports en tête du module (rapport).
  - **P25 (PEP 257 — docstrings)** : docstring de module en tête ; docstring par
    fonction publique (non préfixée `_`) ; délimiteurs `"""` (rapport — la rédaction
    d'une docstring est du contenu, pas une correction mécanique).
  - **CM (commentaires)** : un espace après `#` (hors shebang `#!`, ligne de coding et
    `##` stylistiques) ; phrases complètes ; les identifiants de code restent non
    traduits (convention écosystème : contenu FR, noms intacts) — correction mécanique.
  - **SR (structure)** : `main()` + `sys.exit(code)` explicite pour les outils ; shebang
    `#!/usr/bin/env python3` (rapport — norme script-creator §1.3/§2).
- **Outil d'exécution** : `scripts/correct-py-verifie.py` (Python stdlib uniquement, R9)
  — modes VÉRIF (lecture seule, défaut) et CORRECT (`--correct`) ; sortie JSON
  déterministe (`ensure_ascii=False`) ; code retour 0 = conforme, 1 = écarts restants ;
  auto-test intégré (`--auto-test`).
- **Zones protégées** : les corrections ne s'appliquent jamais aux lignes appartenant à
  des chaînes de caractères (tokenize : bornes exactes des tokens STRING) ni aux
  docstrings — la sémantique du script est intouchable.
- **Nommage** : kebab-case pour l'outil durable ; périmètre par défaut = scripts/*.py
  (racine, hors `_archive/`) et tout script produit par script-creator.

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|---------|
| script-creator | post-traitement | exécuté APRÈS chaque utilisation (garde-fou 6 §1.3, >= 1.0.0) |
| script-reviewer | convergence | conformité fine du langage avant relecture G1-G8 |
| correct-work | escalade | mode CIBLE au-delà de l'arbitrage local (écarts non mécaniques) |
| knowledge-observer | applique | L003 (auto-test cas limites), L005 (garde post-édition) |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; idempotence R1-R6 (gen-plan §1.11).
- Toute correction est tracée au worklog (règle d'or n°1) — jamais d'édition silencieuse.
- Non-duplication (SHARED §6.3) : correct-py ne redéfinit ni la création de scripts
  (script-creator), ni la relecture G1-G8 (script-reviewer), ni la validation
  d'écosystème (correct-work) — il couvre uniquement la conformité aux normes du
  langage des scripts Python.
- L'outil de conformité est lui-même un script : il passe sa propre vérification avant
  adoption (autoréférence, esprit L003).

## HISTORIQUE DES VERSIONS

- v1.0.0 (2026-09-27, session B13-r8) : matérialisation initiale — post-traitement de
  script-creator pour les normes du langage (PEP 8 / PEP 257 / commentaires /
  structure), outil `scripts/correct-py-verifie.py` (modes VÉRIF/CORRECT, zones
  protégées tokenize, auto-test intégré), évals au schéma skill-creator.
