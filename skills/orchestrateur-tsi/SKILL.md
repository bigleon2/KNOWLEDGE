---
name: orchestrateur-tsi
version: 1.1.0
category: ecosystem
language: fr
tags:
  - tsi
  - traktor
  - orchestration
  - mapping
  - midi
description: >-
  Orchestrateur du domaine TSI/Traktor : coordonne la famille de skills dédiés aux
  mappings TSI (XML Traktor Pro 3.11, contrôleur Native Instruments Kontrol S4 MK2)
  — tsi-architect (conception, tandem avec son agent), tsi-validator (arbitre
  mécanique PASS/FAIL), multi-shift-architect (couches SHIFT), midi-doc-expert
  (documentation) — en composant par mission des micro-spécifications auto-contenues
  pour chaque membre (niveau prompt méta maître) et en agrégeant leurs verdicts.
  Déclencher pour : orchestrer un projet TSI de bout en bout (concevoir → valider →
  documenter), router une demande vers le bon membre de la famille, coordonner
  plusieurs skills/agents Traktor/S4, arbitrer un flux multi-étapes sur un mapping.
  Ne remplace aucun membre : route, spécifie, arbitre et agrège. Ne pas déclencher
  pour une demande relevant d'un SEUL membre (routage direct : concevoir →
  tsi-architect, valider → tsi-validator, couches SHIFT → multi-shift-architect,
  documenter → midi-doc-expert).
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "plans de mission multi-étapes (conception → validation → documentation)"
read_when:
  - Déclencher quand la demande concerne : orchestration de la famille TSI, mission de bout en bout sur un mapping (concevoir + valider + documenter), routage entre skills Traktor/S4 MK2, coordination de plusieurs skills/agents du domaine TSI.
  - Déclencher si la demande mentionne : orchestre, coordonne, de bout en bout avec TSI/Traktor/S4, pipeline mapping complet.
  - Ne pas déclencher pour une demande relevant d'un seul membre : concevoir/étendre (tsi-architect), valider (tsi-validator), couches SHIFT (multi-shift-architect), documenter (midi-doc-expert).
---

## §0 — Contexte Système (SHARED v1.7.24)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.

# orchestrateur-tsi — Orchestration du domaine TSI/Traktor (méta maître)

## §1 — Spécification fonctionnelle

### §1.1 Objet

Orchestrer les missions qui traversent PLUSIEURS membres de la famille TSI/Traktor — concevoir un mapping (tsi-architect), le valider mécaniquement (tsi-validator), structurer ses couches SHIFT (multi-shift-architect), le documenter (midi-doc-expert) — sans jamais remplacer l'un d'eux. L'orchestrateur route, compose les spécifications, agrège les verdicts et tient le fil de mission de bout en bout.

**Décision de forme (directive propriétaire 2026-11-01, trace 1a1977ef5718a28d)** : tandem 2 couches — le présent skill détient la MÉTHODE, l'agent d'exécution `agent-TSI.agent` (fichier `orchestrateur-tsi/agent-TSI.agent`, renommé Task 33 — directive propriétaire 2026-11-02) détient l'EXÉCUTION (mémoire État Court/État Long, pipeline A-H). Ni un agent pleinement autonome, ni un simple skill de plus :

1. **Pas d'agent pleinement autonome** : la gouvernance d'écosystème est déjà détenue (gen-plan planifie, correct-work vérifie) — un second cerveau autonome dupliquerait la gouvernance (R4 jamais dupliquer, règle d'or n°5 anti-aspirant du PM gen-plan) ; et le domaine impose des checkpoints (verdict PASS tsi-validator, push = propriétaire KO-L009 point 5) incompatibles avec une boucle sans surveillance.
2. **Pas un simple skill mono-tâche** : le besoin couvre un pipeline multi-skills avec micro-spécs et arbitrage — une méthode dédiée de première classe (inscrite KB, trigger_evals) est requise.
3. **Niveau « prompt méta maître »** : l'orchestrateur ne porte pas UN prompt fixe (maître) ni la gouvernance totale de l'écosystème (ultra maître — surdimensionné, en conflit de gouvernance avec gen-plan) ; il COMPOSE, par mission, des **micro-prompts auto-contenus** (règle « prompts auto-contenus » du guide gen-plan E5/E7) pour chaque membre mobilisé, puis agrège.

**Périmètre matériel** : référentiels actuels ancrés Traktor Pro 3.11 + Kontrol S4 **MK2** (directive propriétaire 2026-11-02 ; pattern Freeze Shift+Loop In corroboré par le mapping réel DJTT S4 MK2 v2.1.0 — cf. `download/analyse-approfondie-zip-djtt-s4mk2-v2.1.0.md`). Toute mention du propriétaire d'un AUTRE modèle (ex : S4 MK3) est traitée comme matériau à calibrer (différences hardware/MIDI à sourcer) AVANT toute architecture — jamais inventée (R-1/R-2).

### §1.2 Déclencheurs

| Déclencheur | Action |
|-------------|--------|
| `orchestre … (TSI/Traktor/S4)` | Mission orchestrée : analyse → routage → exécution déléguée → arbitrage |
| Mission « de bout en bout » (concevoir → valider → documenter) | Pipeline complet P1-P6 avec garde PASS |
| Routage (« quel skill TSI pour … ? ») | Matrice de routage §1.3 — réponse + redirection |
| Demande mono-membre | Redirection directe (P1 → routage direct, sans orchestration) |

### §1.3 Matrice de routage

| Demande | Membre routé | Garde de passage |
|---------|--------------|------------------|
| Concevoir / analyser / étendre l'architecture d'un .tsi | tsi-architect (+ son agent) | pré-validation, puis tsi-validator |
| Valider un .tsi (verdict mécanique) | tsi-validator (`scripts/valider-tsi.py`) | verdict PASS/FAIL + exit code |
| Structurer / auditer des couches SHIFT | multi-shift-architect | 100 % couverts, 0 couche morte (E7) |
| Documenter un mapping VALIDÉ | midi-doc-expert (`scripts/generer-doc-midi.py`) | précondition : verdict PASS daté |
| Analyser un mapping TSI EXISTANT et ses documents illustrés (ZIP, captures d'éléments S4 MK2, vue complète, sous-dossiers) | analyse-doc-s4mk2 (`scripts/analyser-zip-mk2.py`) | verdict PASS + batterie $FACON2 11/11 (table P1b vérifiée) |
| Pipeline complet / mission multi-membres | **orchestrateur-tsi (ce skill)** | garde PASS obligatoire avant documentation/livraison |

**Éléments RÉSERVÉS (directive propriétaire 2026-11-02 — génération prévue lors d'une prochaine session)** : `traktor-function-expert` (référentiel des commandes Traktor Pro 3.11) et `s4-hardware-expert` (inventaire hardware et specs MIDI du S4 MK2) sont des futurs membres de la famille — **réservés aujourd'hui, non créés**. Tant qu'ils n'existent pas, l'orchestrateur ne les route JAMAIS (garde anti-routage inchangée) ; les données qu'ils porteront restent à sourcer des référentiels existants (spec du projet, samples golden, analyses `download/analyse-approfondie-zip-djtt-s4mk2-v2.1.0.md`).

### §1.4 Gardes

1. **Garde PASS** : jamais de documentation (midi-doc-expert) ni de livraison de mapping sans verdict PASS tsi-validator daté dans la mission.
2. **Checkpoints propriétaires** : GO explicite avant toute livraison finale, commit ou push (KO-L009 point 5) — l'orchestrateur propose, le propriétaire dispose.
3. **Anti-collision** : toute allocation MIDI passe par tsi-architect (règle E5-du-doublon) — l'orchestrateur n'alloue jamais lui-même.
4. **Micro-spéc auto-contenue** : chaque délégation porte provenance, entrées, sorties attendues et artefacts à produire (pas de fuite inter-tâches).
5. **Non-substitution** : si la demande relève d'un seul membre, l'orchestrateur répond par le routage direct et ne déclenche pas son pipeline (économie de tokens).

## §2 — Spécification technique

### §2.1 Structure

```text
orchestrateur-tsi/
├── SKILL.md                      # Ce fichier (méthode)
├── agent-TSI.agent               # Agent d'exécution (tandem 2 couches — mémoire A-H ; ex orchestrateur-tsi.agent)
└── evals/
    └── trigger_evals.json        # Cas de déclenchement (8 cas — 5 positifs, 3 négatifs)
```

### §2.2 Pipeline de mission (P1-P6)

| Phase | Action | Artefact |
|-------|--------|----------|
| P1 | Analyse de la demande : nature (concevoir/étendre/auditer/documenter/bout-en-bout), périmètre matériel (MK2 ; tout autre modèle = calibration préalable), membres requis | note de mission (État Court) |
| P2 | Routage : matrice §1.3 ; mono-membre → redirection directe ; multi-membres → plan d'ordre (architecture → validation → documentation) | plan de mission |
| P3 | Composition des micro-spécs (méta maître) : une spécification auto-contenue par membre, ordonnée, avec interfaces d'entrée/sortie | micro-spécs |
| P4 | Exécution déléguée : chaque membre produit son artefact (delta de mapping, rapport JSON, documentation) | artefacts membres |
| P5 | Arbitrage et agrégation : verdict tsi-validator PASS obligatoire avant documentation ; agrégation unique re-vérifiée | verdict + bilan de mission |
| P6 | Clôture : bilan au propriétaire + checkpoints GO (livraison/commit/push) ; État Long mis à jour | bilan + État Long |

### §2.3 L'agent `agent-TSI.agent`

Exécution persistante du tandem (pattern tsi-architect.agent ; renommé `agent-TSI` en Task 33 — le nom interne de l'agent est agent-TSI, le skill garde son nom orchestrateur-tsi) : mémoire à deux niveaux (État Court volatil — mission en cours ; État Long persistant — le présent fichier .agent : historiques de missions, verdicts, leçons de routage), pipeline A-H (A analyse, B État Court, C État Long, D routage, E micro-spécs, F exécution déléguée, G arbitrage/checkpoints, H État Long). Aucune écriture hors `skills/orchestrateur-tsi/` et `download/`.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| tsi-architect | Orchestré | conception/extension des mappings — micro-spéc en entrée, delta en sortie, pré-validation en garde |
| tsi-validator | Orchestré (arbitre) | verdict PASS/FAIL mécanique — garde obligatoire de la phase P5 |
| multi-shift-architect | Orchestré | méthode des couches SHIFT (hôte-seul, non inscrit KB au 2026-11-01) |
| midi-doc-expert | Orchestré | documentation aval — précondition verdict PASS daté |
| analyse-doc-s4mk2 | Orchestré | analyse des mappings réels (format DIOM) et de leurs documents illustrés — correspondance visuels↔contrôles (P1b), comptes G2, verdict PASS + batterie $FACON2 |
| fleet-engineering | Pattern | agrégation unique re-vérifiée, Task IDs globaux (missions parallélisables uniquement) |
| gen-plan | Utilise | plans de mission multi-étapes (>= 3.15.0) |

## §4 — Mode d'emploi rapide

1. **Mission complète** → « orchestre la conception, la validation et la documentation de mon mapping TSI » — le pipeline P1-P6 s'applique.
2. **Routage simple** → « quel skill TSI pour valider mon .tsi ? » — réponse directe : tsi-validator (P1 → redirection, sans orchestration).
3. **Agent d'exécution** → mission longue/persistante : charger `orchestrateur-tsi/agent-TSI.agent` (mémoire État Long conservée entre missions).
4. **Gardes** — jamais de livraison sans verdict PASS tsi-validator ; jamais de push sans GO propriétaire.
