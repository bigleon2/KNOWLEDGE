---
name: rea-analysis
version: 1.0.0
category: ecosystem
language: fr
tags:
  - rea
  - reverse-engineering
  - analyse
  - ghidra
  - integration
  - ecosystem
description: >
  Skill d'analyse rétro-ingénierie par le kit REA (REA_Reverse_All_Thing_Kit — fork bigleon2,
  miroir-épingle de morluto/rea v6.8.0, npm rea-agents, MIT) intégré à l'écosystème (Task ID 12 —
  directive 1a1fa816474a35ad volet « intègre $FACON REA à mon écosystème », pattern ghorg-cmdr Task 51).
  Le kit : CLI ~180 commandes (analyze/inspect/capture/compare) + serveur MCP de rétro-ingénierie
  d'artefacts SANS code source (Ghidra/Hopper/IDA/JADX/Kuna/Frida — binaires, APK/IPA, web/JS,
  Electron/.NET, Android/Apple, firmware, bases de données). État local : kit sous
  tools/rea/REA_Reverse_All_Thing_Kit (épingle 03a3fcb, clone anonyme lecture seule — règle d'or n°4),
  Ghidra 12.2 PUBLIC présent (doctor ghidra healthy ×7 via GHIDRA_INSTALL_DIR), moteurs
  hopper/ida/jadx/kuna absents du sandbox (état dégradé documenté — analyses natives bornées D7 ≤ 590 s).
  Installation idempotente : scripts/rea-install.py (stdlib — clone si absent, npm ci+build:cached si
  dist absent, sonde CLI, rc 0/1/2 — le second passage ne produit aucun changement). Périmètre :
  ANALYSE d'artefacts a posteriori (audit, inspection, evidence) — la REPRODUCTION d'applications
  reste la voie git clone + build (verdict Task 8 : REA inapplicable comme mécanisme de reproduction,
  orthogonale à ghorg-cmdr [clonage]). Déclencher pour analyser/auditer un binaire, un frontend, un
  artefact compilé via le kit REA, réinstaller ou mettre à jour le kit (épingle datée), ou diagnostiquer
  ses moteurs d'analyse.
dependencies:
  - skill: gen-plan
    version: ">=3.22.0"
    used_at: "campagnes d'analyse multi-étapes (chaîne inspect → analyze → rapport — tâche planifiée)"
read_when:
  - Déclencher quand la demande concerne : analyse rétro-ingénierie d'un artefact sans code source, audit de binaire, inspection de frontend
  - Déclencher si la demande mentionne : rea, rea-analysis, REA_Reverse_All_Thing_Kit, rétro-ingénierie, reverse engineering, inspect-go-binary, analyze-javascript-application, ghidra headless, evidence REA
  - Ne pas déclencher hors de ce périmètre (convention protocole — le clonage/reproduction relève de ghorg-cmdr/git, la validation de mappings TSI de tsi-validator)
---

## §A — DÉCLENCHEURS

- `rea`, `REA_Reverse_All_Thing_Kit`, `kit REA` — installation, mise à jour, diagnostic du kit
- `rétro-ingénierie`, `reverse engineering`, `analyse ce binaire`, `audite ce frontend` — campagnes d'analyse d'artefacts SANS code source
- `inspect-*`, `analyze-*`, `capture`, `compare` (commandes REA) — exécution bornée de la surface du kit
- Toute demande d'Evidence d'analyse (YAML) sur un artefact compilé (ELF, APK, IPA, bundle web/Electron/.NET, firmware, DB)

## §0 — Contexte Système (SHARED v1.7.43)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06).
> Référence canonique skill/agent : « mon skill X » = la forme installée `skills/X/SKILL.md` à la racine, JAMAIS le prompt maître du corpus `@mon-ecosysteme/`.

# rea-analysis — Analyse rétro-ingénierie par le kit REA

## §1. Mission

Mettre le kit REA (rétro-ingénierie d'artefacts SANS code source) au service de l'écosystème :
installation idempotente maintenable, campagnes d'analyse bornées (Evidence YAML vérifiables),
diagnostic des moteurs — SANS jamais remplacer la voie canonique de reproduction d'applications
(git clone + build — verdict $FACON2 Task 8 : REA = analyse a posteriori, orthogonale à ghorg-cmdr).

## §2. État du kit (vérifiable au disque)

| Élément | État | Preuve |
|---|---|---|
| Kit | tools/rea/REA_Reverse_All_Thing_Kit @ épingle 03a3fcb (clone anonyme, 6701 commits) | git rev-parse HEAD |
| Runtime | node_modules (npm ci) + dist (build:cached) — CLI `node scripts/rea.mjs` | --help rc=0, 215 lignes |
| Ghidra | 12.2 PUBLIC sain (healthy ×7 : plateforme, architecture, installation, version, headless, décompilateur elf) | doctor, GHIDRA_INSTALL_DIR |
| Moteurs natifs | hopper/ida/jadx/kuna ABSENTS sandbox (missing_analysis_engine — dégradé documenté) | doctor |
| Amont | morluto/rea hyper-actif (0 ahead / 2317 behind au 2026-11-21) — fork = miroir-épingle SANS commit propre | rev-list --left-right --count |
| Evidence | tools/rea/*.out (batterie 5/5 Task 9 : hardening, entropy, elf-notes, exports, layout) | fichiers |

## §3. Installation idempotente — scripts/rea-install.py

```bash
python3 skills/rea-analysis/scripts/rea-install.py                 # complet idempotent (défaut)
python3 skills/rea-analysis/scripts/rea-install.py --pin 03a3fcbce # re-calage sur une épingle datée
```

Comportement (stdlib uniquement, rc 0 = opérationnel / 1 = échec d'étape / 2 = état incohérent) :
1. **clone si absent** — clone ANONYME lecture seule (règle d'or n°4 : dépôt public bigleon2/REA_Reverse_All_Thing_Kit, jamais de jeton — KO-L009) ;
2. **npm ci si node_modules absent** (cache dédié périmètre tools/rea/npm-cache — zéro écriture hors /home/z/my-project) ;
3. **npm run build:cached si dist absent** ;
4. **sonde CLI** `node scripts/rea.mjs --help` (rc=0 requis) + rapport HEAD/commits/dist.
Idempotence ×2 : composant présent = étape sautée (« déjà présent ») — le re-jeu sur état installé ne modifie RIEN (contrat identique ghorg-install.py Task 51).

## §4. Campagnes d'analyse (usage)

- **Bornes D7** : tout appel REA est borné ≤ 590 s (contrainte sandbox nproc=2 — leçons Task 9 : analyze Ghidra sur binaire 41 Mio et analyze-frontend 9 336 fichiers ont atteint la borne — verdict retryable: true, reprise sur profil plus puissant).
- **Commandes** : `inspect-*` (rapides, déterministes) puis `analyze-*` (lourdes, bornées) — surface intégrale : `references/referentiel-kit-rea.md`.
- **GO + KO-L009** : réseau limité aux clones anonymes lecture seule (dépôts publics) et releases publiques (Ghidra/JDK) ; AUCUNE écriture distante ; aucun jeton manipulé.
- **Rapports** : Evidence YAML conservées sous tools/rea/ (préfixe par commande) ; livrables de campagne dans `download/`.

## §5. Règles d'or appliquées

- **Règle d'or n°1** : blocage moteur (missing_analysis_engine) = état dégradé documenté, jamais un arrêt — analyses natives couvertes exécutées, branches bornées consignées.
- **Règle d'or n°4** : le kit et l'amont se lisent par clones git locaux anonymes ; l'épingle est datée au moment de l'installation (--pin).
- **Règle d'or n°5** : toute affirmation d'état (HEAD, rc, moteurs, divergence) dérive du disque — `git rev-parse`, `doctor`, fichiers Evidence.
- **Règle d'or n°6** : rapports et journaux en français ; artefacts techniques verbatim (commandes, chemins, YAML Evidence) en langue d'origine.

## §6. Référentiel et reprise

- **Intégral** : `references/referentiel-kit-rea.md` (surface ~180 commandes par classe, moteurs, verdicts Task 8/9, politique d'épingles, Evidence).
- **Historique** : `@historique/historiques-par-skill/rea-analysis.md` (R4 — jamais édité).
- **Vérification install** : re-jeu `rea-install.py` → no-op ; certification écosystème (arbitre integrity) après toute modification.
