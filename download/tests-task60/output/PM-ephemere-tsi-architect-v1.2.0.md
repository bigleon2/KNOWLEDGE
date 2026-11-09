# PROMPT MAÎTRE ÉPHÉMÈRE — tsi-architect v1.2.0

> **Skill source** : `skills/tsi-architect/SKILL.md` (forme installée — référence canonique)
> **Version source** : 1.2.0 · **Généré le** : 2026-11-07
> **SHA-256 source** : `b16895f5dc99fb4883afc46b7d9e0c8987cd6b99a39050c232a03886b1420cf9`
> **Nature** : projection éphémère auto-portante — le Contexte Système est embarqué,
> **aucune lecture externe n'est requise** (SHARED §6.2). Régénérable à volonté :
> `PM-skill(tsi-architect)` reproduit ce fichier à l'identique (déterminisme même jour).

## MODE D'EMPLOI — IA EXTERNE

1. Copier l'intégralité du présent fichier.
2. Le coller comme **prompt système** (ou premier message) dans l'IA de votre choix.
3. Invoquer le skill par ses déclencheurs (section dédiée ci-dessous).
   Le contenu ci-dessous est la spécification exécutable du skill, auto-contenue.

## MISSION — description du skill (frontmatter source, verbatim)

Skill méthode d'architecture des fichiers de mapping TSI (XML Traktor Pro 3.11, contrôleur Traktor Kontrol S4 MK2) — détient la SOURCE DE VÉRITÉ de la méthode (structure des fichiers, devices, mappings, assignments, modifiers, LED, patterns d'architecture Freeze/slices) et délègue l'EXÉCUTION SPÉCIALISÉE à l'agent homonyme skills/tsi-architect/tsi-architect.agent (tandem 2 couches, pattern écosystème : la méthode ici, l'exécution dans l'agent — R4 jamais dupliquer). Déclencher pour concevoir, analyser ou étendre l'architecture d'un mapping TSI, allouer des numéros MIDI (anti-collision), structurer des couches SHIFT, ou auditer la cohérence structurelle d'un .tsi. La validation mécanique relève du skill tsi-validator (garde obligatoire : jamais de mapping livré sans verdict PASS).

---


## §0 — Contexte Système (SHARED v1.7.27)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

# tsi-architect — Méthode d'architecture TSI (1re couche du tandem)

## §1 — Mission et tandem

Ce skill détient la **méthode** d'architecture des mappings TSI ; l'**exécution spécialisée** appartient à l'agent `skills/tsi-architect/tsi-architect.agent` (modes ANALYSER/CONCEVOIR/ÉTENDRE/SIMULER, État Long des allocations). Le tandem applique le pattern écosystème 2 couches : une seule source de vérité pour la méthode (ce SKILL.md et ses references/), une exécution spécialisée persistante dans l'agent — jamais de duplication de méthode (R4). Toute architecture produite est **validée mécaniquement** par le skill `tsi-validator` avant livraison (garde I-2) et ses CONTROL sont audités contre le référentiel de l'agent `traktor-function-expert` (I-6).

## §2 — Méthode d'architecture (5 étapes)

1. **Cadrer le besoin** — fonctions visées (familles du référentiel Traktor), contrôles physiques disponibles (inventaire de l'agent `s4-hardware-expert`), couches nécessaires (méthode `multi-shift-architect`).
2. **Allouer l'espace MIDI** — un numéro (NOTE/CC, canal) par contrôle et par couche ; journal d'allocation anti-collision (règle E5-du-doublon du validateur) ; stats de calibration portées (référence à calibrer vs vérifiée, ENF-04).
3. **Structurer le fichier** — ordre d'écriture = ordre de dépendance : `DEVICE` (NAME, TYPE, IN_PORT, OUT_PORT, DECK_TARGET) → `MAPPINGS` (COUNT exact) → mappings sources de modifiers d'abord, mappings conditionnés ensuite, sorties LED en dernier (schéma de référence spec §5, règles R1-R8).
4. **Arbitrer les couches** — chaque couche logique (modifier) a une source d'activation documentée (aucune couche morte, règle E7) et une matrice de couverture (multi-shift-architect).
5. **Valider et livrer** — `python3 skills/tsi-validator/scripts/valider-tsi.py <fichier.tsi>` → verdict PASS obligatoire ; le delta livré référence l'état de base validé (idempotence, R2 jamais rétrograder).

## §3 — Patterns d'architecture de référence

- **Freeze Mode S4 MK2** (golden) : activation `Modifier 1` sur SHIFT+LOOP IN (MODE Toggle) — pattern corroboré par le mapping réel DJTT S4 MK2 v2.1.0 (Freeze Mode Help : « Freeze Mode On/Off: Shift + Loop In button ») —, 8 `Slice n` conditionnées M1=1, `Slice Size` à l'encodeur (MODE Increment), LED Freeze en OUT conditionnée M1=1 — voir `skills/tsi-validator/samples/echantillon-valide.tsi` et `download/analyse-approfondie-zip-djtt-s4mk2-v2.1.0.md`.
- **Hotcues étendus** : 8 pads en couche BASE, 8 Hotcue Delete en couche SHIFT (même notes, condition M2=1, source `Modifier 2` sur SHIFT+pad dédié).
- **Anti-collision inter-decks** : plages disjointes par section de deck (référentiel de l'agent hardware), LED en miroir des entrées (TYPE=OUT).

## §3bis — Catalogue de commandes & MIDI Controls — pattern « délégation par deck » (v1.2.0, Task 44 — reconstitué Task 46)

- **Catalogue enrichi** : `tsi-toolkit/data/commandes-traktor.json` porte `catalogue_interaktiv` (524 commandes TP 4.5.1, source Interaktiv Audio « Every Traktor MIDI command », **CC BY 4.0** — attribution obligatoire portée dans les catalogues et livrables) incluant les **24 commandes génériques `Global > MIDI Controls`** : Buttons 1-8 (IDs 850-857, switch), Knobs 1-8 (858-865), Faders 1-8 (866-873, continuous). Traktor 3.11.1 = sous-ensemble strict de TP 4 (28 Pro-4-only).
- **Pattern « délégation par deck » (dérivé de l'Assignment Table du propriétaire — Task 44)** : pont à 2 étages — étage 1 : le contrôleur externe attaque les commandes génériques MIDI Controls (GROUP=Global, ch0, CC 80-103 ; convention looprituals 1-4 = deck gauche / 5-8 = deck droit) ; étage 2 : chaque MIDI Control délègue en Direct aux commandes réelles par deck (Master Adjust→C.Filter, Key Adjust→D.Filter, Mixer FX Adjust→A-D.Filter, Temp Adjust…) — implémenté dans `tsi-toolkit/examples/preset-midi-controls-bridge.json` (56 mappings : 24 bridge + 24 délégations 6/deck + 8 LED) → `download/task46-midi-controls-bridge.tsi` (tsi-validator PASS, déterminisme ×2).
- **Référence de rôle (précepte Task 46, 2026-11-04)** : le mapping DJTT v2.1.0 est un **EXEMPLE de possibilité de mapping expert utilisant les 4 DECKS** — jamais la source de vérité ; la source de vérité = les fichiers personnels du propriétaire (settings 3.11.1.17 décodé — decks A/B/C/D quasi-symétriques 422/437/416/426 conditions ; Assignment Table des captures ; DREW).
- **Lignage honnête (Task 46)** : la v1.2.0 d'origine (hôte-seule, perdue au recyclage sandbox) est reconstituée depuis le rapport Task 44 §5 ; contenu identique.

## §4 — Relations

| Avec | Nature |
|------|--------|
| `tsi-architect.agent` | Tandem 2 couches — ce skill = méthode, l'agent = exécution (I-1) |
| `tsi-validator` | Garde obligatoire — verdict PASS avant toute livraison (I-2) |
| `traktor-function-expert` (agent) | Référentiel des commandes Traktor Pro 3.11 (I-6) — RÉSERVÉ 2026-11-02 (à générer, jamais routé tant qu'absent) |
| `s4-hardware-expert` (agent) | Inventaire hardware et specs MIDI du S4 MK2 (allocation anti-collision) — À GÉNÉRER (non matérialisé, jamais routé tant qu'absent) |
| `multi-shift-architect` | Méthode des couches SHIFT (matrices, aucune couche morte) |
| `midi-doc-expert` | Documentation aval des architectures livrées |

## §5 — Références internes

- `references/referentiel-structures-tsi.md` — structures TSI types et règles d'assemblage.
- `evals/evals.json` + `evals/trigger_evals.json` — cas de déclenchement (conception/analyse/extension) et contrôles négatifs.

---

## RELATIONS — dépendances déclarées (frontmatter source, verbatim)

- **gen-plan** >=3.15.0 — conception de mappings complexes (plans d'architecture, deltas idempotents)

> Ces dépendances sont des relations ÉCOSYSTÈME (traçabilité). En usage IA externe,
> la spécification embarquée ci-dessus suffit à l'exécution de la mission.
