---
name: task-review
version: 1.0.0
category: ecosystem
language: fr
tags:
  - capitalisation
  - post-tache
  - sedimentation
  - skill-creation
  - plateforme
description: >
  Revue de fin de tâche à haute complexité : décider si le chemin d'exécution qui
  vient de se dérouler mérite d'être sauvegardé comme compétence réutilisable, puis
  consolider ou créer le SKILL.md correspondant. Déclencher en fin de tâche quand
  la session a mobilisé 5 appels d'outils ou plus, surmonté des erreurs avant de
  trouver la bonne voie, ou enchaîné 3 étapes explicites ou plus.
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "Norme d'écriture des SKILL.md consolidés ou créés"
read_when:
  - Déclencher quand la demande concerne : la clôture d'une tâche complexe (5+ appels
    d'outils, erreurs surmontées, ou 3+ étapes explicites) dont le chemin d'exécution
    est réutilisable.
  - Déclencher si la situation réunit : tâche venant de se terminer ET caractère
    répétable probable OU méthode/structure/écueils réutilisables identifiés.
  - Ne pas déclencher pour les tâches triviales sans réutilisation probable, ni
    pendant l'exécution (la revue est post-tâche) — convention protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# TASK-REVIEW v1.0.0 — Revue post-tâche et sédimentation en skill

## §0 — Contexte Système (SHARED v1.7.45)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME importé aux normes de l'écosystème via skill-creator —
directive propriétaire Task 113 (trace 1a201e4bda5a2289). Original chinois conservé
byte-identité : `references/plateforme-original.md` (archive R4). Dans l'écosystème
Knowledge, la création d'un skill suit la norme skill-creator (frontmatter complet,
§0, historique des versions) — la présente revue oriente vers cette norme plutôt
que vers le gabarit minimal de l'original.

## §1 — Spécification fonctionnelle

Au moment de livrer le résultat d'une tâche, exécuter en silence la revue de
complexité suivante (sans en informer l'utilisateur) :

1. **Critères de complexité** — la tâche satisfait-elle au moins un critère ?
   - 5 appels d'outils ou plus ont été nécessaires ;
   - des erreurs ou impasses ont été rencontrées avant de trouver la bonne voie ;
   - la tâche comportait 3 étapes explicites ou plus.
   Si aucun critère n'est rempli : ne rien faire, ne rien mentionner.
2. **Critères de réutilisation** — si complexe, évaluer :
   - la tâche a-t-elle des chances d'être répétée ou d'avoir des variantes proches ?
   - l'exécution a-t-elle produit un flux, une structure ou des avertissements
     d'écueils réutilisables ?
   Si aucun « oui » : ne rien faire, ne rien mentionner.
3. **Sédimentation** — si au moins un « oui » :
   - vérifier si un skill existant couvre déjà le domaine dans `{{SKILLS_ROOT}}` ;
   - si oui : mettre à jour le SKILL.md existant (ajouter l'expérience et les
     écueils rencontrés — montée de version semver et historique), ne jamais créer
     un doublon ;
   - si non : créer un nouveau skill selon la norme skill-creator (frontmatter
     complet : name, version, category, language, tags, description avec clause de
     déclenchement, read_when ; §0 Contexte Système ; corps en français ; historique
     des versions).
4. **Mention finale** — en cas de sédimentation ou de mise à jour, l'indiquer
   brièvement en fin de réponse ; en cas d'absence de sédimentation, ne pas
   mentionner cette revue du tout.

## §2 — Spécification technique

### Normes de qualité

- La `description` doit être spécifique, formulée comme parlerait l'utilisateur
  (bon exemple : « surveiller l'actualité IA mondiale et générer une revue HTML » ;
  mauvais exemple : « traiter des tâches d'information »).
- Les étapes d'exécution doivent être reproductibles à la lettre.
- Les écueils consignés ne relatent que des écueils réellement rencontrés —
  jamais d'invention (règle d'or : ne jamais inventer de données).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| skill-creator | Norme aval | Tout nouveau skill créé par cette revue suit la norme skill-creator |
| knowledge-observer | Complément | Journal des leçons apprises observées en continu (pattern différent : observation de session) |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, orientation vers la norme skill-creator pour la sédimentation ; original chinois archivé byte-identité references/plateforme-original.md (R4) |
