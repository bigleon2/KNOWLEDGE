---
name: pm-skill
version: 1.0.2
category: ecosystem
language: fr
tags:
  - pm
  - prompt-maitre
  - ephemere
  - portabilite
  - export
  - ia-externe
description: >-
  Skill de portabilité universelle — génère à la demande des PROMPTS MAÎTRES
  ÉPHÉMÈRES auto-portants (format MD) depuis les SKILL.md vivants installés à
  la racine skills/ (référence canonique — jamais les PMs du corpus
  @mon-ecosysteme/) : l'invocation verbatim PM-skill(<skill>) projette le
  frontmatter (mission/description verbatim, relations/dépendances) + le corps
  complet — bloc §0 Contexte Système embarqué, d'où l'auto-portance SHARED
  §6.2 (aucune lecture externe requise) — + un historique condensé depuis
  @historique, sous un en-tête PM (provenance : skill, version, date, SHA-256
  du source + mode d'emploi IA externe « coller comme prompt système »).
  Utilisable tel quel dans n'importe quelle IA externe (ChatGPT, Claude,
  Gemini…). Garanties mécaniques : déterminisme même jour (régénération
  byte-identique — idempotence ×2), zéro invention KO-L003 (le script
  structure, il ne rédige pas — contenu exclusivement du SKILL.md source +
  @historique), traçabilité SHA-256 prouvable, 0 octet d'état (sorties
  download/ régénérables — corpus intact, KO-L004 continue pour les 4
  familles), lag impossible par construction (toujours à la version du
  SKILL.md vivant). Couverture universelle : les 68 skills racine, dont les 64
  sans voie PM corpus. Origine : Task 60 G3-SG2, porte propriétaire D604
  VALIDÉE (directive verbatim « je valide ta proposition, tu peux l'exécuter
  $FACON pour me générer $FACON un écosystème $FACON2 » — analyse D603 +
  tests comparatifs D603b : 16 PASS · 1 FAIL [défaut réel de l'écosystème
  actuel, pas du prototype] · 7 FACT). Bras exécutable :
  scripts/generer-pm-ephemere.py (Python stdlib, self-test embarqué ST1-ST11,
  --generate/--check/--list, codes retour 0/1/2/3). Déclencher pour exporter
  un skill vers une IA externe, générer le prompt maître d'un skill
  quelconque (famille ou non-famille), ou obtenir une version auto-portante
  et traçable d'un skill.
dependencies:
  - skill: gen-plan
    version: ">=3.20.0"
    used_at: "garde É1-INSTALL préalable (l'écosystème doit être installé — les SKILL.md sources sont la matière première de la projection)"
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "certification post-intégration (arbitres integrity/verify-cross rejoués après création — finding F2 du correct-work --bloc Task 61, bidirectionnalité SHARED §3.2, v1.0.1)"
  - skill: vue-upload
    version: ">=1.5.0"
    used_at: "livraison du PM éphémère (push/featured ★, share vérifié SHA-256) — canal de diffusion des livrables"
read_when:
  - Déclencher quand la demande concerne : exporter ou utiliser un skill de l'écosystème dans une IA externe (ChatGPT, Claude, Gemini…), générer le prompt maître d'un skill sous forme de fichier MD autonome, obtenir une version auto-portante collable d'un skill.
  - Déclencher si la demande mentionne : PM-skill, PM-skill(<skill>), prompt maître éphémère, « génère le prompt maître de X », « exporte X pour une IA », « je veux utiliser mon skill X dans ChatGPT/Claude/Gemini ».
  - Ne pas déclencher pour : la montée de version d'un skill famille et la génération de son PM corpus (cascade KO-L004 via gen-plan), l'exécution d'un skill dans l'écosystème (voie native = le skill installé, règle canonique SHARED §0/§1.2), l'installation de l'écosystème (PM-INSTALL).
---

## §0 — Contexte Système (SHARED v1.7.36)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

# pm-skill — Portabilité universelle : prompts maîtres éphémères pour IA externe

## §1 — Mission

Générer à la demande, pour N'IMPORTE QUEL skill installé à la racine `skills/` (68 skills — dont les 64 sans voie PM corpus), un **prompt maître éphémère** : un fichier MD unique, auto-portant (SHARED §6.2 — le Contexte Système est embarqué, aucune lecture externe n'est requise), immédiatement utilisable dans une IA externe (ChatGPT, Claude, Gemini…) en le collant comme prompt système. Le PM éphémère est une **projection du SKILL.md vivant** (règle canonique : la forme installée à la racine est la référence) — jamais un artefact versionné, jamais stocké dans l'état de l'écosystème : régénérer = relire. Origine Task 60 : analyse D603 (verdict portabilité AUGMENTE — couverture ×17, coût 17 touches → 0, lag 0 structurel, volatilité absorbée par construction) + tests comparatifs D603b (16 PASS · 1 FAIL [défaut réel de l'écosystème actuel : PM gen-plan corpus non auto-portant] · 7 FACT) + **porte propriétaire D604 VALIDÉE** (directive verbatim « je valide ta proposition, tu peux l'exécuter $FACON pour me générer $FACON un écosystème $FACON2 », session web-c30e6506, 2026-11-07). Architecture retenue : **couche additive, corpus intact** — KO-L004 continue pour les 4 familles (spécifications versionnées + arbitres + archive R4) ; l'idée originale de remplacement du corpus a été écartée par l'analyse (régression certaine des arbitres — D603 §2).

## §2 — Déclencheurs et interface

| Invocation | Effet |
|---|---|
| `PM-skill(<nom-du-skill>)` | **Déclencheur verbatim** (forme canonique de la directive propriétaire) — génère le PM éphémère de `<skill>` dans `download/` et le livre via vue-upload (push + featured) |
| `pm-skill(<nom>)` · « génère le prompt maître de X » · « exporte X pour une IA » · « je veux utiliser mon skill X dans ChatGPT/Claude/Gemini » | Alias sémantiques — même effet |
| `PM-skill --list` | Liste des skills éligibles (68 racine ; un skill sans bloc §0 est INÉLIGIBLE — refus mécanique honnête) |

Le skill s'exécute via son bras `scripts/generer-pm-ephemere.py` (Python stdlib — aucune dépendance hors bibliothèque standard) ; l'agent porteur invoque le script puis livre le fichier (vue-upload `push` + `featured` ★ ; `share` sur demande — lien externe vérifié SHA-256).

## §3 — Usage (bras exécutable)

```bash
python3 scripts/generer-pm-ephemere.py --generate <skill>             # → download/PM-ephemere-<skill>-v<version>.md
python3 scripts/generer-pm-ephemere.py --generate <skill> --out <dir> # sortie ailleurs (tests uniquement)
python3 scripts/generer-pm-ephemere.py --check <skill>                # éligibilité + cohérence
python3 scripts/generer-pm-ephemere.py --list                         # skills racine éligibles
python3 scripts/generer-pm-ephemere.py --self-test                    # ST1-ST11, tempdir, zéro écriture hors tempdir
```

Codes retour : `0` OK · `1` échec (self-test FAIL) · `2` usage invalide · `3` skill inconnu ou inéligible (aligné `generer-pm-skill.py` — le refus mécanique est honnête, jamais une génération dégradée). Livraison : le fichier atterrit dans `download/` (livrable) → vue-upload `push` l'inscrit, `featured` l'épingle en livrable courant ★, `share` donne un lien externe vérifié sur demande.

## §4 — Format du PM éphémère généré (projection, zéro rédaction)

| Section | Source (verbatim) |
|---|---|
| En-tête `# PROMPT MAÎTRE ÉPHÉMÈRE — <name> v<version>` | frontmatter `name`/`version` |
| Bloc provenance (skill source, version, date, **SHA-256 du SKILL.md source**, nature régénérable) | calcul mécanique |
| `## MODE D'EMPLOI — IA EXTERNE` (3 pas : copier · coller comme prompt système · invoquer par déclencheurs) | gabarit fixe (structure, pas du contenu) |
| `## MISSION` — description du skill | frontmatter `description` (repli honnête si absente) |
| Spécification complète (déclencheurs, §0 Contexte Système, règles, conventions, sections §…) | **corps du SKILL.md verbatim** — le bloc §0 propagé (propagate-context) EST l'auto-portance |
| `## RELATIONS` — dépendances déclarées | frontmatter `dependencies` |
| `## HISTORIQUE CONDENSÉ` — versions archivées (projection tronquée) | `skills/@historique/historiques-par-skill/<skill>.md` (section omise proprement si absent) |

## §5 — Garanties mécaniques

1. **Déterminisme / idempotence ×2** : même SKILL.md (même jour) → sortie **byte-identique** (horodatage au jour uniquement) ; re-jeu sans effet.
2. **Zéro invention (KO-L003)** : le contenu provient exclusivement du SKILL.md source et de l'historique archivé ; le script structure, il ne rédige pas.
3. **Auto-portance (SHARED §6.2)** : le bloc §0 est requis — un SKILL.md sans §0 est INÉLIGIBLE (refus rc=3, jamais une sortie non auto-portante) ; l'échec du PM gen-plan corpus (dépendance « lire en premier », test D603b A3) est impossible par construction ici.
4. **Traçabilité SHA-256** : le SHA-256 du SKILL.md source est embarqué — reproductibilité prouvable (recalculable : `sha256sum skills/<skill>/SKILL.md`).
5. **0 octet d'état** : sorties dans `download/` uniquement (régénérables/supprimables) — jamais dans `skills/` ni `@mon-ecosysteme/` ; le corpus reste à 9 fichiers (CORPUS_ATTENDU).
6. **Lag impossible par construction** : le PM éphémère est TOUJOURS à la version du SKILL.md vivant (test C6 : bump simulé détecté en ~1 ms ; les 4+ lags documentés du corpus sont structurellement exclus pour cet usage).

## §6 — Frontière de périmètre (ce que pm-skill ne fait PAS)

- **Ne remplace pas le corpus** : KO-L004 continue pour les 4 familles (PMs versionnés, arbitres verify-cross/integrity, archive R4 @historique) — le PM éphémère d'une famille se génère AUSSI depuis son SKILL.md vivant, sans toucher au corpus.
- **N'exécute pas le skill dans l'écosystème** : la voie native d'exécution est le skill installé lui-même (règle canonique SHARED §0/§1.2) — exécuter un PM généré en interne dupliquerait la voie native (R4, jamais dupliquer). L'exécution via PM reste utile uniquement HORS écosystème (IA externe) — couvert par le mode d'emploi embarqué.
- **N'historise pas** : le rôle d'archive des spécifications versionnées reste porté par le corpus + @historique ; l'historique condensé est une projection de lecture, jamais une écriture.
- **Refuse mécaniquement** les skills inconnus (rc=3) et sans §0 (rc=3) — l'honnêteté prime sur la génération.

## §7 — Relations

| Avec | Nature |
|---|---|
| `gen-plan` | Garde É1-INSTALL préalable (dépendance >= 3.20.0) — porteur de la Task 60 (analyse D603, porte D604, intégration G3-SG2) |
| `correct-work` | Certification de l'intégration (arbitres rejoués après création — integrity, verify-cross) |
| `vue-upload` | Livraison du PM éphémère (`push` inscription download/, `featured` épinglage ★, `share` lien externe vérifié SHA-256) |
| `propagate-context` | Maintien du bloc §0 sur tous les skills — la matière première de l'auto-portance (F6) |
| `@mon-ecosysteme/` (corpus) | **Intact** — KO-L004 continue pour les 4 familles (couche additive) ; pm-skill n'y écrit jamais |
| `@historique/historiques-par-skill/` | Source de l'historique condensé (lecture seule, projection tronquée) |
| `scripts/task60-tests-comparatifs.py` | Harnais de preuve D603b (prototype EMBARQUÉ figé — rejouable pour documenter la décision D604 ; la forme VIVANTE est le présent bras `generer-pm-ephemere.py`, extension unique : historique condensé §4) |

## §8 — Vérifiabilité (preuves rejouables)

- **Self-test embarqué ST1-ST11** : détection, éligibilité, refus rc=3, sections requises, auto-portance, déterminisme ×2, fidélité verbatim, SHA-256 exact, historique condensé, garde d'état (download/ inchangé), non-famille — `python3 scripts/generer-pm-ephemere.py --self-test` (rc 0 attendu, idempotent).
- **Harnais D603b rejouable** : `python3 scripts/task60-tests-comparatifs.py` (16 PASS · 1 FAIL [défaut de l'écosystème actuel, pas du prototype] · 7 FACT — rapport `download/rapport-tests-task60.md`).
- **Vérification manuelle** : régénérer deux fois et comparer (`sha256sum`) ; recalculer le SHA source ; coller le PM éphémère dans une IA externe et invoquer un déclencheur.

## §9 — Historique de version

| Version | Date | Améliorations implantées | Avantage |
|---|---|---|---|
| v1.0.0 | 2026-11-07 | Création (Task 60 G3-SG2, D604 VALIDÉE) : skill + bras `scripts/generer-pm-ephemere.py` (projection auto-portante, §0 embarqué, SHA-256, historique condensé) + evals (4 positifs + 3 négatifs vetos) + entrée KB + pin ECO_SKILLS + `@historique/historiques-par-skill/pm-skill.md` | — (point de départ : la portabilité IA externe passe de 4 familles/68 skills à 68/68) |
