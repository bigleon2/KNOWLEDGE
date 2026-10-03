---
name: audit-provenance
version: "1.1.0"
category: ecosystem
language: fr
  tags:
    - audit
    - provenance
description: >
  Auditer la provenance des artefacts de l'écosystème (skills, scripts, corpus,
  rapports, plans) : traçabilité de l'origine (session, directive, clone épinglé,
  reconstitution post-wipe), lignage des wipes/restaurations, détection des
  artefacts sans provenance et réécriture idempotente des en-têtes manquants.
  Utiliser après chaque wipe ou restauration, avant chaque clone de discussion
  (clone-chat), avant chaque installation (PROMPT-MAITRE-INSTALL-ECOSYSTEME.md), ou lorsque
  l'utilisateur demande un audit de provenance / un contrôle de traçabilité.
  Matérialise la leçon L006 (knowledge-observer) ; dépend de script-creator pour
  les conventions des scripts produits ; contrôlé par correct-work (mode CIBLE).
dependencies:
  - skill: knowledge-observer
    version: ">=1.0.0"
    used_at: "Journal lessons-learned (L006) — patterns de provenance (§1.1)"
  - skill: script-creator
    version: ">=1.0.0"
    used_at: "Conventions des scripts produits (R9, stdlib, idempotence ×2 — §2)"
  - skill: correct-work
    version: ">=2.6.0"
    used_at: "Validation du skill et des artefacts corrigés (mode CIBLE, §1.3 GF-4)"
---

# Audit de provenance

Un skill pour tracer l'origine et le lignage des artefacts de l'écosystème, détecter
ceux qui en sont dépourvus et corriger les manques de manière idempotente.

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

La provenance d'un artefact est sa traçabilité d'origine : quelle session l'a créé,
quelle directive ou quel pattern l'a motivé, quel clone épinglé ou quelle
restauration le rattache à l'écosystème. Les incidents de lignée (wipe inter-sessions,
incident B-17, restauration B13-r4/r5, travail interrompu sans append worklog)
produisent des artefacts orphelins — vérifiables mais sans historique exploitable.
audit-provenance ferme ce trou : il scanne les artefacts, déduit leur provenance
(heuristique documentée §2), signale les orphelins et corrige idempotemment les
en-têtes manquants. Il matérialise la leçon **L006** (knowledge-observer) :
« tout artefact créé ou modifié porte une provenance traçable ; l'audit de
provenance est exécuté après chaque wipe/restauration et avant chaque clone ».

### §1.2 Le processus en 6 étapes

| Étape | Action | Sortie |
|-------|--------|--------|
| 1 | Délimiter le périmètre d'audit (skills écosystème, scripts, corpus, rapports, plans) | liste d'artefacts |
| 2 | Exécuter le collecteur `scripts/audit-provenance.py` (heuristique §2) | rapport JSON |
| 3 | Analyser les orphelins : artefact obsolète (à archiver) ou vivant (à documenter) | tri des orphelins |
| 4 | Réécriture idempotente `--fix` : en-tête `PROVENANCE:` inséré (garde par marqueur) | artefacts documentés |
| 5 | Preuve d'idempotence : rejeu ×2 à l'identique (0 ajout au 2e passage) | preuve ×2 |
| 6 | Traçabilité : leçon L006 appliquée, worklog + rapport journalisés (règle d'or n°1) | entrée worklog |

### §1.3 Garde-fous

1. **Lecture seule par défaut** : le collecteur n'écrit que par `--fix` explicite ;
   aucun artefact n'est modifié sans rapport préalable.
2. **Idempotence ×2 (GF-3 script-creator)** : l'insertion est gardée par le marqueur
   `PROVENANCE:` — le 2e passage est un no-op vérifiable (rapports comparés).
3. **Heuristique assumée** : la détection est déclarative (§2) — un artefact
   considéré « avec provenance » peut toujours être enrichi ; aucun faux négatif
   n'est masqué (les orphelins restent listés au rapport).
4. **Validation correct-work** : tout artefact corrigé est couvert par la garde
   post-écriture (arbitres ×2, certification complète) avant d'être déclaré fiable.
5. **R9 (persistance)** : le collecteur vit sous `scripts/` ; les rapports sous
   `tmp/` — jamais de code inline.
6. **Post-traitement correct-py (GF-6)** : le collecteur passe le skill `correct-py`
   (PEP 8/PEP 257) avant d'être déclaré terminé.

### §1.4 Déclencheurs

- Manuel : « audite la provenance », « d'où vient cet artefact », « trace le lignage »,
  « corrige les provenances manquantes ».
- Systématique : après chaque wipe/restauration ; avant chaque clone-chat ; avant
  chaque installation (PROMPT-MAITRE-INSTALL-ECOSYSTEME.md étape d'audit).

## §2 — SPÉCIFICATION TECHNIQUE

- **Langage** : Python 3 (stdlib uniquement) ; JSON `ensure_ascii=False` en sortie ;
  code retour explicite (`sys.exit(code)`).
- **Heuristique de provenance (v1.0.0)** : un artefact est « avec provenance » si son
  contenu contient au moins un marqueur parmi : `Provenance` / `provenance`,
  référence de session (`B1\d`, `N\d+`, `n\d+`, `nXX-`), référence de directive
  (`trace`, `directive`), mention de reconstitution (`reconstitué`, `restitué`,
  `restaur`, `assemblé`, `calibré`, `épinglé`, `wipé`, `wipe`), marqueur de scellage
  (`PATTERN:`, `PROVENANCE:`, `SYNC-CONTEXT`). La liste est extensible (paramètre
  `--markers`) et documentée dans le rapport.
- **Réécriture `--fix`** : pour les scripts Python orphelins, insertion d'un
  commentaire `# PROVENANCE: ...` après le shebang (ou en tête si absent) —
  syntaxe-safe, garde par marqueur, jamais de réécriture totale (GF-5 script-creator).
- **Localisation** : `{{SKILLS_ROOT}}audit-provenance/` ; collecteur
  `scripts/audit-provenance.py` ; rapports sous `tmp/b13r5-install/`.
- **Test** : chaque critère est vérifiable par commande unique ; la preuve
  d'idempotence compare les rapports de deux exécutions consécutives (post-fix).

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|---------|
| knowledge-observer | applique | Leçon L006 (provenance, journal lessons-learned — >= 1.0.0) |
| script-creator | hérite de | Conventions des scripts produits (R9, stdlib, idempotence ×2, correct-py — >= 1.0.0) |
| correct-work | valide via | Mode CIBLE sur le skill et les artefacts corrigés (>= 2.6.0, GF-4) |
| clone-chat | précondition | Audit de provenance exécuté avant tout clone de discussion |
| install-ecosysteme | précondition | Audit exécuté avant installation (PROMPT-MAITRE-INSTALL-ECOSYSTEME.md — source d'installation unique v1.1.0) |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; idempotence R1-R6 (gen-plan §1.11).
- Toute correction d'artefact est tracée au worklog (règle d'or n°1) — jamais d'édition silencieuse.
- Non-duplication (SHARED §6.3) : audit-provenance ne redéfinit ni la vérification
  mécanique de l'écosystème (arbitres certification/integrity/interactions), ni la
  relecture de scripts (script-reviewer) — il couvre uniquement la traçabilité d'origine.
