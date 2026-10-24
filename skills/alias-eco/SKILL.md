---
name: alias-eco
version: 1.2.0
category: ecosystem
language: fr
tags:
  - alias
  - phrases-recurrentes
  - ecosystem
  - lexique
  - token-economie
description: >
  Gestionnaire du système d'alias $<ALIAS> de l'écosystème Knowledge : remplace les grandes phrases
  récurrentes des discussions (ex : « mon écosystème personnel » → $ECO-LEON — lorsque le propriétaire
  écrit « de $ECO-LEON », l'écosystème comprend « de mon écosystème personnel »). Liste, trie par ordre
  alphabétique et déduplique (aucun doublon strictement identique) les phrases récurrentes détectées,
  en format JSON sauvegardé dans @historique/@Alias/ du dépôt KNOWLEDGE. Déclencheurs : « alias-eco »
  (gestion du système d'alias — ajouter, résoudre, synchroniser), « liste mes alias » (affichage du
  registre), « alias-eco (chat) » (liste TXT des phrases récurrentes de la discussion courante, triée
  par ordre alphabétique). Invoqué également lors de l'analyse des discussions par correct-work (projet)
  pour tenir le registre à jour. Résolution à la lecture : tout $<ALIAS> d'un message propriétaire est
  expansé avant interprétation. Ne pas déclencher hors de ce périmètre — chaque compétence sœur
  couvre son propre domaine (convention protocole, Task 28).
dependencies: []
read_when:
  - Déclencher quand la demande concerne : système d'alias de l'écosystème, phrases récurrentes, registre d'alias, économie de frappe
  - Déclencher si la demande mentionne : alias, alias-eco, liste mes alias, $ALIAS, phrases récurrentes
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — Spécification fonctionnelle

### §1.1 Objet

Éviter au propriétaire d'écrire les grandes phrases récurrentes de ses discussions (ex : « de mon écosystème personnel », « de façon cohérente, optimisée et fonctionnelle »). Ces phrases sont remplacées par des **alias** au format **`$<ALIAS>`** — lettres majuscules, chiffres et tirets (regex `^[A-Z0-9][A-Z0-9-]*$`). Exemple canonique : la phrase « mon écosystème personnel » porte l'alias `ECO-LEON` ; « de $ECO-LEON » est lu « de mon écosystème personnel ».

### §1.2 Les déclencheurs (grammaire B incluse, v1.2.0)

| Déclencheur | Action |
|-------------|--------|
| `alias-eco` | Gestion complète du système : lister/synchroniser le registre JSON, ajouter/modifier un alias (`alias-eco : ajoute l'alias X pour « … »`), résoudre les `$<ALIAS>` d'un texte |
| **Grammaire B (mécanique, v1.2.0)** : `alias-eco "<texte>" --add <ALIAS>` — attribution en une expression ; variantes acceptées : guillemets français `« … »`, préfixe `$` de l'ALIAS optionnel ; exécution mécanique via `--trigger` (le texte peut contenir parenthèses, virgules, deux-points, `--add` interne) |
| `liste mes alias` | Affichage lisible du registre des alias (phrase → `$ALIAS`), trié alphabétiquement |
| `alias-eco (chat)` | Analyse de la discussion courante : détection des phrases récurrentes, mise à jour du registre JSON, production d'une **liste TXT** de toutes les phrases récurrentes de la discussion **triée par ordre alphabétique** |

### §1.3 Intégration écosystème

- **Résolution à la lecture (convention)** : tout `$<ALIAS>` présent dans un message du propriétaire est expansé (via le registre) AVANT interprétation par l'agent ou tout autre skill — l'alias est un raccourci d'entrée, jamais une transformation des livrables.
- **correct-work (projet)** : lors de l'analyse des discussions (vérification PROJET), alias-eco est invoqué pour détenir à jour le registre des phrases récurrentes (délégation, correct-work v2.8.0 §10.1).
- **Persistance (R4)** : le registre JSON vit dans `skills/@historique/@Alias/` (dossier `@` = infrastructure non-skill, convention SHARED §1.2 v1.6.8) — une seule source, jamais dupliquée.

### §1.4 Règles du registre

1. **Tri** : les phrases sont triées par ordre alphabétique (clé `phrase`, casse repliée).
2. **Déduplication** : aucun doublon strictement identique — deux entrées ne peuvent porter la même phrase (après normalisation : espaces repliés, ponctuation d'extrémité retirée).
3. **Détection mécanique** : une phrase est récurrente si elle revient ≥ 3 fois (≥ 3 mots, ≥ 12 caractères) — n-grammes maximaux ; l'agent peut ajouter/valider sémantiquement (`--add`, curation).
4. **Alias jamais inventé** : la détection propose des phrases ; l'attribution d'un alias est un acte explicite (propriétaire ou agent mandaté), toujours traçable (champ `source`).

## §2 — Spécification technique

### §2.1 Structure

```text
alias-eco/
├── SKILL.md                      # Ce fichier
├── references/
│   └── format-alias.md           # Conventions du format $<ALIAS> et du registre JSON
├── scripts/
│   └── alias-manager.py          # Gestionnaire mécanique (Python stdlib, N3)
└── evals/
    ├── evals.json                # Cas d'évaluation (schéma skill-creator)
    └── trigger_evals.json        # Cas de déclenchement (9 cas — 6 positifs, 3 négatifs)
```

### §2.2 Le gestionnaire `alias-manager.py`

| Commande | Effet |
|----------|-------|
| `--selftest` | Tests internes (détection, tri, déduplication, résolution, ajout) — sans effet sur le registre réel |
| `--resolve "<texte>"` | Expande les `$<ALIAS>` du texte via le registre |
| `--list` | Affiche le registre (phrase → `$ALIAS`) trié alphabétiquement |
| `--add <ALIAS> "<phrase>"` | Attribue/met à jour l'alias d'une phrase (garde format `^[A-Z0-9][A-Z0-9-]*$`) |
| `--trigger "<expression>"` | Parse une expression grammaire B (`alias-eco "<texte>" --add <ALIAS>`, variantes « » / `$ALIAS`) et applique `--add` — idempotent, garde format identique ; rejet propre (rc=2) si expression mal formée |
| `--scan <fichier>…` | Détecte les phrases récurrentes d'un ou plusieurs fichiers texte et fusionne dans le registre |
| `--chat <fichier>…` | Mode « alias-eco (chat) » : scan + export TXT (`download/alias-eco-chat-<date>.txt`) trié alphabétiquement |

Chemin du registre dérivé de l'emplacement du script (`skills/@historique/@Alias/aliases.json` relatif à la racine portante — fonctionne au dépôt comme au profil local). Sortie JSON déterministe (clés triées) ; idempotent ×2 (re-scan sans changement d'état = bytes identiques si entrée identique).

### §2.3 Format du registre `aliases.json`

```json
{
  "format": "aliases-eco v1",
  "mis_a_jour": "2026-10-23",
  "source": "alias-eco v1.2.0",
  "phrases": [
    {
      "phrase": "mon écosystème personnel",
      "alias": "ECO-LEON",
      "occurrences": 5,
      "occurrences_cumulees": 5,
      "premiere_detection": "2026-10-23",
      "derniere_detection": "2026-10-23",
      "source": "amorçage propriétaire (directive 2026-10-23)"
    }
  ]
}
```

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| correct-work | Utilisé par | Mode PROJET — analyse des discussions : délégation de la tenue du registre (correct-work v2.8.0 §10.1, dependencies >= v1.0.0) |
| @historique/ | Héberge | `@Alias/` — sous-dossier d'infrastructure du registre (convention `@` SHARED §1.2 ; règles de conservation @historique/README) |
| registre KB | Enregistré | Entrée `alias-eco v1.2.0` (category ecosystem) — cross-reference bidirectionnelle avec correct-work |

## §4 — Mode d'emploi rapide

1. **Lire** un message contenant `$ECO-LEON` → expanser via `python3 skills/alias-eco/scripts/alias-manager.py --resolve "<texte>"` (ou lecture directe du registre).
2. **Tenir le registre** pendant une session → `--scan <transcrit>` ou `--chat <transcrit>` (mode « alias-eco (chat) »).
3. **Attribuer un alias** → `--add ECO-LEON "mon écosystème personnel"` (ou grammaire B : `--trigger 'alias-eco "mon écosystème personnel" --add ECO-LEON'`).
4. **Afficher** → `--list` (ou déclencheur « liste mes alias »).
