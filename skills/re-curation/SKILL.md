---
name: re-curation
version: 1.1.0
category: ecosystem
language: fr
tags:
  - progressive-disclosure
  - re-curation
  - optimization
  - testing
  - ecosystem
description: >
  Skill de re-curation progressive disclosure d'éléments de l'écosystème — IMPLÉMENTÉ
  du script principal scripts/protocole-test.py (directive propriétaire Task 72) : GÉNÈRE
  un protocole de test ADAPTÉ à l'élément ciblé, l'exécute en phase PRE AVANT toute
  re-curation (baseline golden master → verdict GO/NO-GO), le ré-exécute en POST
  (maintien de l'optimisation vérifié : écosystème cohérent, optimisé, fonctionnel),
  arbitre les méthodes candidates (--compare — la plus optimisée et performante) ;
  méthode P0-P7 (P0 = tests AVANT re-curation, P7 = vérification POST du maintien de
  l'optimisation), arbitre check-recuration.py (C1-C4), mesure-sections.py généralisé.
dependencies:
  - skill: gen-plan
    version: ">=3.39.0"
    used_at: "chaînage mode step des re-curations ; règles d'or partagées (n°5 état vérifiable, KO-L003)"
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "vérification par phase (P6)"
    optional: true
read_when:
  - Déclencher quand la demande concerne : re-curation progressive disclosure d'un élément de l'écosystème
  - "re-cure" / "re-curer" / "re-curation" — alléger un skill LOURD/CRITIQUE ( progressive disclosure)
  - « protocole de test » avant re-curation — baseline golden master, GO/NO-GO
  - "maintien de l'optimisation" — vérifier qu'une re-curation préserve le fonctionnement
  - comparer les méthodes de re-curation — la plus optimisée et performante
---

## §A — DÉCLENCHEURS

- `re-curation` / `re-cure` / `re-curer` — re-curation progressive disclosure d'un élément de l'écosystème (skill, agent, script)
- « protocole de test » avant re-curation — génération du protocole adapté + phase PRE (GO/NO-GO)
- « maintien de l'optimisation » — phase POST : l'écosystème demeure cohérent, optimisé, fonctionnel
- `--compare` méthodes de re-curation — arbitrage de la plus optimisée et performante
- $FACON = de façon cohérente, optimisée et fonctionnelle · $FACON2 = (cohérent, optimisé et fonctionnel) — glossaire inline auto-contenu (registre canonique @historique/@Alias/aliases.json)

## §0 — Contexte Système (SHARED v1.7.36)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

> **Règles structurantes du présent skill** : R4 ne jamais dupliquer (les intégraux déplacés vivent UNE fois en references/), R2 ne jamais rétrograder, KO-L003 l'état dérive du disque (jamais de la mémoire), règle d'or n°5 tout chiffre est mesuré.

## §1 — Mission et nature

**Mission** (directive propriétaire Task 72, directive complémentaire 1a1b7b297b7b4975) : s'assurer $FACON du **maintien de l'optimisation** du fonctionnement de l'écosystème pour qu'il demeure $FACON2, **en faisant des tests $FACON2 AVANT d'effectuer** les re-curations progressive disclosure — pour trouver **la méthode la plus optimisée et performante**.

**Le skill est IMPLÉMENTÉ de son script principal** `scripts/protocole-test.py` : c'est lui qui génère le protocole de test adapté, l'exécute (PRE puis POST) et arbitre les méthodes. Les deux autres scripts sont des outils : `mesure-sections.py` (poids par section, généralisé de Task 72) et `check-recuration.py` (arbitre C1-C4). Le présent SKILL.md porte la MÉTHODE ; les scripts portent l'EXÉCUTION.

**Cible prioritaire 2026-11-08** (liste priorisée Task 72 G3 — download/liste-recuration-priorisee-task72.md) : version-management (n°1) → iphone19 → iphone18 → [skill-creator noyau, protocole renforcé] → web-reader → cahier-des-charges → iphone17 ; pdf/pptx = plateforme (décision propriétaire).

## §2 — Méthode P0-P7 (ordre strict — les tests AVANT la re-curation)

| Phase | Nom | Mécanique | Outil |
|---|---|---|---|
| **P0** | **Protocole de test adapté GÉNÉRÉ puis EXÉCUTÉ (PRE)** | Nature de l'élément détectée (contrats §A/read_when/evals/description, sections, poids, gouvernance KB/ECO_SKILLS) → baseline golden master (sha256 des contrats + sections mesurées) → **verdict GO / NO-GO** — NO-GO = la re-curation NE DÉMARRE PAS | `protocole-test.py --pre <skill>` |
| P1 | Cartographie sèche | Sections mesurées + blocs déplaçables identifiés (≥ 1,5 Kio, hors contrats) + gain projeté — SANS ÉCRITURE | `mesure-sections.py <skill>` |
| P2 | Sélection de méthode | Arbitrage des méthodes candidates : gains projetés calculés des sections mesurées + conformité R4 → **la plus optimisée et performante** (les non-R4-compliantes sont disqualifiées) | `protocole-test.py --compare <skill>` |
| P3 | Moves R4 byte-identiques | Extraction mécanique par marqueurs (jamais réécriture du contenu déplacé) vers `references/` avec en-tête de provenance (section d'origine, version, date, SHA-256 du bloc) — script d'extraction dédié à la passe, verrouillé count==1 | script d'extraction de la passe |
| P4 | Résumés opérationnels inline | Textes NOUVEAUX compacts + pointeurs `references/` (aucune duplication) ; contrats verbatim intacts (D005-class) ; compensation de taille pour tenir les seuils | éditions chirurgicales |
| **P5** | **Vérification POST du maintien de l'optimisation** | Protocole ré-exécuté : contrats == baseline (**cohérent**) + pointeurs/non-duplication (**fonctionnel**) + poids réduit ou sous seuil LOURD (**optimisé**) → verdict **MAINTIEN DE L'OPTIMISATION** / DÉRIVE (blocant) | `protocole-test.py --post <skill>` |
| P6 | Idempotence + arbitres | Re-jeu ×2 no-op des scripts de la passe + arbitres écosystème (integrity/coherence/vcw/cross) + correct-work par phase | arbitres écosystème |
| P7 | Vérification finale + traçabilité | `check-recuration.py <skill>` (C1-C4) + worklog R5 (verdicts PRE/POST/--compare tracés) + cascade selon gouvernance (KB/ECO_SKILLS → pin + KB + historiques + ULTRA ; famille PM → KO-L004 complète) | `check-recuration.py` |

**Règles d'or de la méthode** :
1. **Jamais de re-curation sans verdict PRE = GO** (baseline capturée) — directive « tests avant re-curation ».
2. **Jamais de suppression non archivée** (R4) — la méthode « suppression » est disqualifiée d'office dans --compare.
3. **Contrats intacts** : déclencheurs verbatim §A, read_when, evals, description — comparés sha256 en POST (l'étiquette SHARED du §0 est normalisée : un bump écosystème n'est pas une dérive — leçon harnais v2 Task 72).
4. **Gouvernance respectée** : élément KB/ECO_SKILLS → cascade légère obligatoire (pin + KB + historiques + ULTRA + arbitres + sync hôte↔dépôt) ; famille PM (gen-plan, correct-work, clone-chat, refactor-guard) → cascade KO-L004 complète ; plateforme (hors KB) → décision propriétaire explicite AVANT toute écriture.
5. **Statuts et chiffres dérivés du disque** (KO-L003, règle d'or n°5) — les verdicts des scripts font foi.

## §3 — Protocole de test adapté (ce que --pre génère)

Le protocole **s'adapte à la nature de l'élément** (détectée, jamais supposée) : présence/absence de §A, §0, read_when, evals/, scripts/, references/, entrée KB, registre ECO_SKILLS, famille PM. Tests générés selon ce qui existe — le fichier `download/protocole-test-<skill>.json` porte : nature détectée, protocole (tests PRE/POST), baseline (octets, contrats sha256, sections mesurées, #token estimés = caractères ÷ 4), verdict PRE. En POST, le même fichier est enrichi de la comparaison et du verdict de maintien.

## §4 — Structure des fichiers

```
skills/re-curation/
├── SKILL.md               # la méthode P0-P7 (présent fichier)
├── scripts/
│   ├── protocole-test.py  # SCRIPT PRINCIPAL — --pre / --post / --verifier / --compare / --selftest
│   ├── mesure-sections.py # poids par section (généralisé Task 72) + --selftest
│   └── check-recuration.py# arbitre C1-C4 + --selftest
└── evals/
    ├── evals.json         # 6 cas (schéma skill-creator)
    └── trigger_evals.json # 12 cas (Description Optimization)
```

## §5 — Journal des versions

- **v1.1.0 (2026-11-09, session web-ecef7f80 — pendance consignée au commit Task 79 0b1712b, directive gen-plan(step) « correctif du comparateur §0 de protocole-test (harnais) »)** : harnais v3 — deux défauts du comparateur §0 de `scripts/protocole-test.py` résorbés : (1) **borne du bloc socle** — le contrat `section_0_normalisee` capturait de « ## §0 » jusqu'à « ## §1 », et quand le skill n'a pas de section §1 (cas réel version-management : 23,4 Kio capturés sur 25,8 ; ASR : 16,7 Kio ; preuve : 104 des 119 porteurs corrigés, contrat §0 cumulé 1 180,3 → 193,4 Kio — `download/protocole-test-correctif-comparateur-v110-preuves.json`), le contrat couvrait le CORPS entier → une re-curation légitime du corps (déplacement R4) donnait un DÉRIVE fausse ; nouvelle borne `bloc_socle()` = premier titre markdown suivant (~1,6 Kio) ; (2) **dates de directives du socle normalisées** — extension de la leçon harnais v2 (étiquette SHARED) : une date de directive propriétaire enrichie au bloc socle (ex. « directive 2026-10-31, renforcée 2026-11-06 ») n'est pas une dérive de contrat ; selftest étendu 5→7 tests (bump socle étiquette+date → PASS ; déplacement R4 du corps, socle intact → MAINTIEN), 7/7 ×2 idempotent ; MINOR, description frontmatter inchangée (non-régression triggers) ; baselines capturées avant v1.1.0 à re-capturer (convention de mesure §0 v3).

- **v1.0.0 (2026-11-08, session web-ecef7f80 — Task 72 G4, directive à 7 items item 4 + directive complémentaire 1a1b7b297b7b4975)** : création — skill IMPLÉMENTÉ du script principal `scripts/protocole-test.py` (GÉNÈRE le protocole de test adapté à l'élément ciblé, l'exécute en phase PRE avant toute re-curation [baseline golden master, GO/NO-GO], le ré-exécute en POST [maintien de l'optimisation : cohérent/optimisé/fonctionnel], arbitre les méthodes candidates en `--compare`) + méthode P0-P7 (P0 = tests avant re-curation, P7 = vérification POST) + arbitre check-recuration.py (C1 pointeurs, C2 non-duplication 1024 o, C3 marqueurs, C4 seuils) + mesure-sections.py généralisé (selftests embarqués ×3) ; liste des cibles priorisées (G3) ; cascade légère (KB + pin ECO_SKILLS + historiques + ULTRA + arbitres + sync).
