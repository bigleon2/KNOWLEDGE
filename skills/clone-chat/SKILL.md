---
name: clone-chat
version: 2.3.0
category: ecosystem
language: fr
tags:
  - clone
  - discussion
  - context
  - drift
  - gen-plan
  - auto-clonage
  - worklog
  - themes
  - cache
  - yaml
  - yalm
description: >
  Clone l'intégralité d'une discussion (contexte, décisions, artefacts,
  worklog) dans un fichier Markdown auto-suffisant. 7+1 étapes, Étape 3.5
  Context Drift, intégration gen-plan v3.6.1+ KB. Format Markdown unique,
  propriété auto-clonage.
  Modes thématiques v2.1.0 : `--theme` (table des thèmes/sous-projets de la
  discussion), `(<theme>)` (clone partiel restreint au thème précisé),
  `(ALL)` (un clone par thème + index récapitulatif).
  Cache d'analyse v2.2.0 : le clone antérieur canonique sert de cache sémantique —
  §1-§3 réutilisés byte-stables pour les sessions déjà couvertes, seule la delta
  worklog est re-analysée (§1.13) ; le cache n'accélère jamais la validation.
  Sortie duale v2.3.0 : `--yaml` (alias `--yalm` — formulation propriétaire
  « YALM », trace 1a221e5599452e2d, interprétée YAML) produit en tandem un
  jumeau `.yaml` structuré dérivé du clone (vue machine non canonique,
  idempotente) ; le Markdown demeure l'instantané canonique.
  Archive la session pour reprise par une session héritière.
dependencies:
  - skill: gen-plan
    version: ">=3.6.1"
    used_at: "Calibration E15, archivage sessions longues"
    optional: true
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "Validation croisée (Mode CIBLE, §3.5)"
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "Conventions structurelles (§5, §9)"
read_when:
  - Déclencher quand la demande concerne : clone l'intégralité d'une discussion (contexte, décisions, artefacts, worklog) dans un fichier Markdown auto-s…
  - Déclencher si la demande mentionne : markdown, auto, session
  - Déclencher si la demande mentionne : yaml, yalm, jumeau, clone yaml
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.47)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



## §0bis — Règle zéro (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §A — DÉCLENCHEURS

- `clone-chat` ou `clone_chat`
- `clone-chat --theme` — analyse de l'intégralité de la discussion et table des thèmes (sous-projets) principaux (v2.1.0)
- `clone-chat (<theme>)` — clone partiel restreint au thème précisé ; `(ALL)` = un clone par thème + index (v2.1.0)
- `clone-chat --yaml` (alias `clone-chat --yalm`) — clone complet + jumeau `.yaml` structuré dérivé (v2.3.0 ; combinable aux modes thématiques ; formulation propriétaire « clones au format YALM » acceptée)
- `clone la discussion` ou `clone cette session`
- `clone-chat:` suivi d'une description de session
- `archiver la discussion` — archivage complet d'une session multi-sessions
- `sauvegarde de contexte` — sauvegarde du contexte pour reprise dans une nouvelle session
- `crée un clone` — demande explicite de clonage
- Toute demande de capturer l'intégralité d'une discussion en vue d'une reprise ultérieure
- Fin de session longue avec demande de préservation du contexte


## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

clone-chat est un skill de **clonage de discussion** pour assistant IA. Il produit un fichier Markdown auto-suffisant qui capture l'intégralité du contexte d'une discussion multi-sessions : les décisions, les artefacts produits, les spécifications techniques, les évolution de contexte (drifts), et les instructions de reprise. Le clone permet à un assistant IA dans une nouvelle session de reconstruire l'état exact de la discussion et de poursuivre le travail sans perte d'information. Depuis v2.3.0 (`--yaml`), le clone peut être accompagné d'un **jumeau YAML** : vue structurée machine-lisible dérivée du Markdown, qui demeure le seul format canonique (§1.14).

### §1.2 Les 7+1 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| **1** | Collecte du worklog | Lire le fichier `worklog.md` (format SHARED §1.4), identifier les sessions distinctes, produire un tableau chronologique |
| **2** | Collecte des artefacts | Scanner l'arborescence pour identifier fichiers créés/modifiés, grouper par catégorie |
| **3** | Extraction des décisions | Identifier décisions utilisateur, bugs corrigés, conventions établies, données de calibration |
| **3.5** | Context Drift | Tracer chaque changement de contexte (5 types : INVERSION, MODIFICATION, CORRECTION, ENRICHISSEMENT, RECALIBRAGE) |
| **4** | Spécifications techniques | Détailler les fichiers principaux avec niveau de détail selon taille (in extenso / condensé / résumé) |
| **5** | Assemblage | Combiner toutes les sections en un document Markdown unique et cohérent (ordre imposé §0-§5) |
| **6** | Validation (8 checks) | Exécuter les 8 checks de validation (auto-suffisance, complétude worklog/skills/décisions/bugs/drifts, exécutabilité, auto-clonage) |
| **7** | Sauvegarde | Sauvegarder le clone dans `download/` avec nom descriptif, enregistrer dans le worklog |

### §1.3 Détail de l'Étape 1 — Collecte du worklog

Lire le fichier `worklog.md` à la racine du projet (format SHARED §1.4). Identifier les sessions distinctes (séparées par des lignes `---`). Extraire pour chaque session :
- Le Task ID et le nom de l'agent
- La tâche effectuée
- Les actions concrètes réalisées
- Les résultats et livrables produits

Produire un tableau chronologique des sessions.

### §1.4 Détail de l'Étape 2 — Collecte des artefacts

Scanner l'arborescence du projet pour identifier tous les fichiers **créés ou modifiés** durant la discussion. Pour chaque artefact :
- Le chemin relatif (convention SHARED §1.2 : kebab-case)
- La taille (Ko)
- Une description de son contenu et rôle

Grouper par catégorie : skills, scripts, documents, charts, archives.

### §1.5 Détail de l'Étape 3 — Extraction des décisions

Parcourir le worklog et le contexte pour identifier :

1. **Décisions de l'utilisateur** : chaque choix explicite avec son contexte et ses conséquences
2. **Bugs corrigés** : chaque bug avec cause, fix et résultat
3. **Conventions établies** : chaque règle avec sa formulation et un exemple
4. **Données de calibration** : grilles #token, métriques, historique

Produire des tableaux structurés pour chaque catégorie.

### §1.6 Détail de l'Étape 3.5 — Context Drift

Cette étape **trace chaque fois que le contexte a changé** durant la discussion. C'est une étape d'analyse critique qui certifie que les évolutions ont été détectées.

**5 types de drift** :

| Type | Définition | Exemple |
|------|-----------|--------|
| INVERSION | Décision renversée (A accepté puis A refusé) | « Version v2.0.0 » acceptée puis refusée au profit de v3.1.0 |
| MODIFICATION | Décision ajustée (paramètre X remplacé par Y) | Export DOCX remplacé par export MD par défaut |
| CORRECTION | Spécification ou décision erronée corrigée | Chemins absolus corrigés en chemins relatifs |
| ENRICHISSEMENT | Décision complétée par ajout d'un élément nouveau | Ajout Étape 3.5 Context Drift à clone-chat v1.1.0→v1.2.0 (historique) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibrée) | Grille #token ajustée de -32% après calibration E15 |

**Format de la table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|

**Règle obligatoire** : Même si aucun drift n'est détecté, écrire « Aucune évolution de contexte détectée » pour certifier que l'analyse a bien été effectuée. Ne jamais laisser cette section vide.

### §1.7 Détail de l'Étape 4 — Spécifications techniques

Détailler les fichiers principaux créés ou modifiés. Le niveau de détail dépend de la taille du fichier (convention in extenso) :

| Taille | Traitement |
|--------|------------|
| < 200 lignes | In extenso (contenu complet) |
| 200-500 lignes | In extenso avec sections condensées |
| > 500 lignes | Résumé structuré : objectifs, structure, modules clés |

Pour chaque fichier : description, signature (fonctions/modules), chemin relatif, taille.

**Intégration gen-plan (optionnelle)** :
- Si gen-plan v3.6.1+ est présent : enrichir avec les données de calibration E15 et les étapes E1-E7
- Si `{{KB_ENABLED}}` est `true` : enrichir §2 avec les descriptions du Registre KB (`{{KB_PATH}}`) pour les skills de l'écosystème

### §1.8 Détail de l'Étape 5 — Assemblage

Combiner toutes les sections collectées en un document Markdown unique et cohérent. L'ordre des sections est imposé :

1. §0 — Règle zéro (contexte perdu)
2. §1 — Chronologie de la discussion
3. §2 — Écosystème de skills (fichiers, scripts, artefacts)
4. §2.4 — Historique des interactions (si `{{KB_ENABLED}}`)
5. §3 — Décisions clés (décisions, bugs, conventions, calibration)
6. §3.5 — Évolutions de contexte (Context Drift)
7. §4 — Instructions d'utilisation
8. §5 — Auto-clonage

Voir `références/clone-template.md` pour la structure complète du template.

### §1.9 Détail de l'Étape 6 — Validation (8 checks)

Exécuter les **8 checks de validation**. Chaque check est binaire (PASS/FAIL). Le clone est valide si 8/8 PASS.

| # | Check | Critère principal | Sous-critères de validation |
|---|-------|-------------------|--------------------------|
| 1 | Auto-suffisance | Le clone est lisible et exécutable sans fichier externe | (a) Pas de « voir fichier X », (b) Pas de dépendance externe, (c) Un assistant neuf peut le lire et agir |
| 2 | Complétude worklog | Chaque session du worklog est représentée en §1 | (a) Table §1.2 complète, (b) Chaque session a au moins 1 ligne en §1.3, (c) Sessions manquantes = FAIL |
| 3 | Complétude skills | Chaque skill créé/modifié est détaillé en §2 | (a) Version présente, (b) Description fonctionnelle, (c) Spécifications techniques, (d) Relations listées |
| 4 | Complétude décisions | Chaque décision, bug, convention est en §3 | (a) Décisions utilisateur avec contexte + conséquence, (b) Bugs avec cause + fix + résultat, (c) Conventions avec règle + exemple |
| 5 | Complétude bugs | Chaque bug corrigé a cause + fix + résultat | (a) Cause racine identifiée, (b) Fix décrit, (c) Résultat vérifié, (d) Pas de bug sans résolution |
| 6 | Complétude drifts | Chaque drift identifié est dans la table §3.5 | (a) Type correct parmi les 5, (b) Avant/Après explicites, (c) Session et ligne worklog référencées, (d) Section présente même si vide |
| 7 | Exécutabilité | Un assistant IA peut reconstruire le contexte | (a) §4 instructions claires, (b) Fichiers prioritaires listés, (c) In extenso pour fichiers < 200 lignes, (d) Résumé structuré pour > 500 lignes |
| 8 | Auto-clonage | La section §5 est présente et auto-référentielle | (a) §5 décrit le mécanisme de croissance, (b) Clone-chat référencé, (c) Mécanisme §1-§3 enrichis / §0,§4-§5 régénérés |

Si un check échoue, corriger avant de passer à l'étape 7.

**Check 9 — Cohérence thématique (v2.1.0, modes `(<theme>)` et `(ALL)` uniquement)** : (a) aucun contenu hors-thème dans les sections §1-§3, (b) exclusions listées en §0bis du clone thématique, (c) slug du thème présent dans le nom de fichier, (d) preuves ≥2 citées pour le périmètre retenu (R4). Le clone thématique est valide si 9/9 PASS (8 checks + check 9).

**Check 10 — Validité du jumeau YAML (v2.3.0, mode `--yaml` uniquement)** : (a) le jumeau `.yaml` parse sans erreur (parseur YAML si disponible, sinon garde structurelle des clés racines), (b) les 9 clés racines attendues sont présentes (§1.14), (c) couverture : chaque section §0-§5 du clone a son équivalent dans le jumeau, (d) idempotence prouvée : régénération du jumeau sur le même clone → bytes identiques. Le clone en mode `--yaml` est valide si 10/10 PASS (8 checks + check 9 thématique le cas échéant + check 10).

### §1.10 Détail de l'Étape 7 — Sauvegarde

Sauvegarder le clone dans `download/` avec un nom descriptif incluant la date et le sujet.

Format du nom : `<sujet>-clone-<AAAA-MM-JJ>.md`

Enregistrer la sauvegarde dans le worklog (format SHARED §1.4).

### §1.11 Intégration KB

Si `{{KB_ENABLED}}` est `true` :

- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **Registre KB** : enrichir la section §2 du clone avec les descriptions des skills depuis le registre
- **Historique des interactions** : reproduire en §2.4 l'historique des interactions clés entre skills
- **Protocole de Découverte** : voir SHARED §2.3

### §1.12 Modes thématiques (v2.1.0)

clone-chat supporte 4 modes d'invocation, plus un modificateur transversal `--yaml` (v2.3.0) :

| Mode | Invocation | Sortie |
|------|-----------|--------|
| Complet (défaut) | `clone-chat` | Clone intégral de la discussion (7+1 étapes, 8 checks) |
| Analyse des thèmes | `clone-chat --theme` | Table des thèmes détectés — AUCUN clone produit |
| Clone thématique | `clone-chat (<theme>)` | Clone partiel restreint au thème `<theme>` |
| Clones multiples | `clone-chat (ALL)` | Un clone par thème + index récapitulatif |
| Jumeau YAML (modificateur transversal) | `clone-chat --yaml` (alias `--yalm`) | Clone du mode choisi + jumeau `.yaml` dérivé — combinable aux 4 modes ci-dessus (v2.3.0, §1.14) |

#### §1.12.1 Détection des thèmes (`--theme`)

Analyse de l'intégralité de la discussion en cours — fenêtre courante, résumés de
continuation hérités, worklog, §1.0 des clones antérieurs — pour différencier les
thèmes principaux (sous-projets). Critères de segmentation (au moins 2 réunis) :
1. Objet technique distinct (ex : KPS, GIF, installation de l'écosystème)
2. Famille de livrables distincte (skills, scripts, documents, clones)
3. Plages de sessions/fenêtres disjointes ou quasi disjointes
4. Chaîne de décisions propre (décisions/drifts non partagés avec les autres thèmes)

**Règle de preuve (R4)** : un thème n'est retenu que s'il est ancré par ≥ 2 preuves
(entrée worklog, artefact disque, trace_id, section de clone antérieur). Nommage :
slug kebab-case (`<slug>`).

**Format de sortie — table des thèmes** :

| # | Thème | Slug | Sessions / fenêtres | Artefacts associés | Preuves (≥2) | Statut |
|---|-------|------|--------------------|--------------------|--------------|--------|

Statut : `ACTIF` (sous-projet en cours) / `CLÔTURÉ` (archivé).

**Garde mono-thème** : si la discussion ne comporte qu'un seul sous-projet
distinguable, la table contient 1 ligne et la mention explicite « aucun sous-projet
distinguable ». Aucun thème inventé.

#### §1.12.2 Clone thématique (`(<theme>)`)

Le clone thématique suit la structure §0-§5 du gabarit `références/theme-template.md`
avec filtrage par thème :

| Section | Contenu en mode thématique |
|---------|---------------------------|
| §0 + §0bis | Règle zéro + périmètre + table des EXCLUSIONS (thèmes et sections hors périmètre, avec pointeurs) |
| §1 | Sessions du thème uniquement |
| §2 | Artefacts (skills, scripts, documents) du thème uniquement |
| §3 | Décisions, bugs, conventions, drifts du thème uniquement |
| §4 | Instructions de reprise POUR CE THÈME (état courant + prochaine étape exécutable) |
| §5 | Auto-clonage thématique (le clone thématique grandit par ses propres sessions) |

**Gardes** :
1. Thème inconnu ou mal orthographié → reproduire la table `--theme` + erreur contrôlée
   « thème non reconnu — choisir dans la table » ; AUCUN clone partiel inventé.
2. Auto-suffisance périmétrique : le clone thématique se suffit AU PÉRIMÈTRE du thème
   (check 9) ; la reprise globale de la discussion exige le clone complet ou `(ALL)` —
   mention obligatoire en §0.
3. Nommage : `<sujet>-clone-theme-<slug>-<AAAA-MM-JJ>.md`.

#### §1.12.3 Clones multiples (`(ALL)`)

`<theme> = "ALL"` : exécuter `--theme` puis générer un clone thématique PAR thème de la
table, plus un index `<sujet>-clone-themes-index-<AAAA-MM-JJ>.md` récapitulant : table
des thèmes, fichiers produits, tailles, verdicts de validation (9/9). Idempotence :
ré-exécution régénère les mêmes noms de fichiers (même périmètre → écrasement à
l'identique) ; périmètre modifié → nouveaux fichiers, l'ancien index reste lisible.

#### §1.12.4 Impact sur les 7+1 étapes

| Étape | Mode complet | Modes `(<theme>)` / `(ALL)` |
|-------|--------------|----------------------------|
| 1 (worklog) | Collecte intégrale | Collecte intégrale + attribution de thème par session |
| 2-4 | Collecte intégrale | Collecte filtrée par thème |
| 3.5 | Drifts intégraux | Drifts du thème uniquement |
| 5 | Assemblage §0-§5 complet | Assemblage filtré + §0bis exclusions |
| 6 | 8 checks | 8 checks + check 9 (cohérence thématique) |
| 7 | `<sujet>-clone-<date>.md` | `<sujet>-clone-theme-<slug>-<date>.md` |

### §1.13 Cache d'analyse des clones (v2.2.0)

Le clone complet antérieur canonique (dernier clone de clôture — §1.0 chaîne de
clonage) est le **cache sémantique de l'analyse** : ses sections §1-§3 sont une
analyse déjà validée des sessions qu'il couvre. À l'Étape 1 :

1. **Couverture** : lire la dernière suite worklog couverte par le clone antérieur
   (§1.0) et la comparer à la dernière suite présente au worklog courant ;
2. **Réutilisation** : pour toute session DÉJÀ couverte, réutiliser les lignes §1.2
   et les extraits §1.3 du clone antérieur tels quels (byte-stable — la cohérence
   historique prime sur la reformulation) ;
3. **Delta** : n'analyser fraîchement que les sessions NOUVELLES (delta worklog) ;
   l'Étape 3.5 trace les drifts du delta uniquement ;
4. **Garde de couverture** : l'union {sessions du clone antérieur} ∪ {sessions du
   delta} doit égaler l'ensemble des sessions du worklog — toute session non couverte
   = FAIL du check 2 (complétude worklog) ; AUCUNE session inventée ;
5. **Validation inchangée** : les 8 checks (et le check 9 en mode thématique)
   s'exécutent sur le clone FINAL complet — le cache accélère la COLLECTE, jamais
   la VALIDATION ;
6. **Sans clone antérieur** : premier clone de la lignée → collecte intégrale
   (comportement v2.1.0 inchangé).

**Gain** : pour une fenêtre type (1-3 suites worklog nouvelles), la collecte Étapes
1-4 ne re-analyse que le delta — voir ligne « clone incrémental » de la grille §2.3.

### §1.14 Jumeau YAML (v2.3.0)

**Terminologie** : « YALM » (formulation propriétaire, trace 1a221e5599452e2d)
est interprété comme **YAML** (sérialisation structurée) — aucune norme publique
« YALM » n'existe comme format documentaire. Le déclencheur accepte l'alias
`--yalm` ; le format produit est du YAML valide. Évolution réversible (ajout de
mode, aucune fonction retirée).

**Principe (sortie duale)** : `clone-chat --yaml` produit le clone Markdown
intégral (7+1 étapes, 8 checks + check 9 thématique le cas échéant) PUIS dérive
mécaniquement son **jumeau** `<sujet>-clone-<AAAA-MM-JJ>.yaml` à l'Étape 7 :

| Règle | Contenu |
|-------|---------|
| R-1 Non-canonique | Le Markdown demeure l'unique instantané canonique (§5 inchangé) ; le jumeau est une VUE DÉRIVÉE régénérable — R4 : jamais une seconde source d'information |
| R-2 Provenance | Le jumeau cite sa source : `meta.source_md` (nom de fichier) + `meta.sha256_source` (SHA-256 du clone canonique) |
| R-3 Combinabilité | `--yaml` se combine aux modes thématiques : jumeau du clone complet ou du clone thématique |
| R-4 Idempotence | Régénération sur clone md inchangé → bytes identiques (ordre des clés stable, listes non chronologiques triées, indentation fixe 2 espaces) |
| R-5 Sérialisation | Pas de tabulations ; blocs scalaires `\|` indentés pour les extraits multi-lignes ; tableaux de lignes pour les longues citations ; aucune clé contenant `: ` non échappé |
| R-6 Validation | Check 10 : parse sans erreur, 9 clés racines présentes, couverture §0-§5, idempotence prouvée |

**Schéma des clés racines** (9 clés, miroir des sections du gabarit) :

```yaml
meta:         # sujet, date, session_id, trace_id, generation, source_md, sha256_source
rule_zero:    # §0 — règle zéro + contexte écosystème
chronologie:  # §1 — sessions (table de hachage task -> lignes)
artefacts:    # §2 — skills, scripts, documents, charts, archives
decisions:    # §3 — decisions, bugs, conventions, calibration
drifts:       # §3.5 — table des évolutions de contexte (5 types)
instructions: # §4 — instructions de reprise
autoclone:    # §5 — mécanisme de croissance
chain:        # §1.0 — chaîne de clonage (lignée des clones antérieurs)
```

**Usage cible** : reprise par une session héritière avec lecture machine
(parsing direct), réingestion par arbitres/scripts écosystème (ancrage KO-L003,
checkpoints E11) — le jumeau ne remplace JAMAIS la lecture humaine du clone
canonique.

---


## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack technique

- **Langage** : Markdown pur (CommonMark compatible)
- **Environnement** : `{{SKILLS_ROOT}}clone-chat/`
- **Pas de dépendance externe** (aucun ZIP, aucune image embed, aucun outil spécifique requis)
- Le fichier doit être lisible avec n'importe quel éditeur de texte
- **Jumeau YAML (v2.3.0)** : texte YAML pur, lisible dans tout éditeur ; PRODUCTION sans dépendance installée, VALIDATION par parseur YAML si disponible (PyYAML), sinon garde structurelle des clés racines (§1.14, check 10)

### §2.2 Format de sortie

- Fichier Markdown unique, auto-suffisant
- Aucune dépendance externe
- Tout le contexte est contenu dans le fichier
- Tableaux Markdown pour les données structurées
- Code fences pour les extraits de code
- Jumeau `.yaml` optionnel (`--yaml`, v2.3.0) : vue structurée dérivée, non canonique (§1.14)

### §2.3 Grille #token

| Mode | #token estimé | Profil min. | Plage |
|------|--------------|-------------|-------|
| Discussion courte (< 5 sessions) | 2750 | ECO | 2000-3500 |
| Discussion moyenne (5-15 sessions) | 4500 | NORMAL | 3500-5500 |
| Discussion longue (> 15 sessions) | 7250 | NORMAL | 5500-9000 |
| Mode `--theme` (analyse seule) | 2000 | ECO | 1500-2500 |
| Mode `(<theme>)` (clone thématique) | 3500 | NORMAL | 2500-4500 (60-80 % du clone complet) |
| Mode `(ALL)` (N clones + index) | 7000 | NORMAL | 4500-10000 (croît avec le nombre de thèmes) |
| Clone incrémental (§1.13, delta worklog) | 3000 | NORMAL | 2000-4000 (40-60 % du clone complet — seul le delta est re-analysé) |
| Mode `--yaml` (clone choisi + jumeau, §1.14) | +325 | NORMAL | +15-20 % du mode correspondant (dérivation mécanique, aucune re-analyse, check 10 inclus) |

**Note v2.0.0** : estimation recalibrée pour couvrir l'Étape 3.5 Context Drift, l'intégration gen-plan v3.6.1+ KB, et la section historique des interactions.
**Note v2.1.0** : trois lignes ajoutées pour les modes thématiques (§1.12) — l'analyse `--theme` est plus légère qu'un clone, le clone `(<theme>)` vaut ~60-80 % du complet, `(ALL)` est la somme des clones plus l'index.
**Note v2.2.0** : ligne « clone incrémental » ajoutée (§1.13) — la réutilisation du cache d'analyse du clone antérieur ramène la collecte à ~40-60 % d'un clone complet pour une fenêtre type.
**Note v2.3.0** : ligne « mode `--yaml` » ajoutée (§1.14) — le jumeau YAML est dérivé mécaniquement des sections déjà assemblées : surcoût ~15-20 % (#token de sérialisation + check 10), aucune re-analyse.

### §2.4 Profils ressource

| Profil | Comportement pour le clone |
|--------|--------------------------|
| **NORMAL** | Clone complet, toutes les sections détaillées |
| **ECO** | Clone condensé, sections §3 regroupées |
| **VIEUX PC** | Clone minimal, §3.5 et §5 uniquement |

Le profil est déterminé par la longueur de la discussion (voir grille #token en §2.3).

### §2.5 Mitigation taille

Pour les clones de discussions longues (> 15 sessions), appliquer :
1. Résumer les sessions anciennes en 1 ligne
2. Détailler §1.3 pour les 5-10 dernières sessions seulement
3. Skills stables décrits en 1 ligne

### §2.6 Intégration gen-plan (optionnelle)

Clone-chat fonctionne **standalone** sans gen-plan. Si gen-plan v3.6.1+ est présent, les enrichissements suivants sont appliqués :

| Composant gen-plan | Enrichissement clone-chat |
|--------------------|------------------------|
| v3.6.1+ (calibration E15) | Étape 1 : données E15, grille #token |
| v3.6.1+ (étapes E1-E7) | Étape 4 : structure de planification |
| v3.6.1+ (Registre KB) | §2 : descriptions skills depuis `{{KB_PATH}}` |
| v3.6.1+ (kb_path) | §4 : liens vers skills du Registre |

### §2.7 Structure des fichiers

```
{{SKILLS_ROOT}}clone-chat/
├── SKILL.md
└── références/
    ├── clone-template.md
    └── theme-template.md
```

### §2.8 Logging worklog

Voir SHARED §1.4 pour le format. Spécifiquement pour clone-chat :

```markdown
---
Task ID: [task-id]
Agent: clone-chat v2.0.0
Task: Clonage de discussion — [sujet]

Work Log:
- Étape 1 : Worklog collecté, N sessions identifiées
- Étape 2 : N artefacts découverts
- Étape 3 : N décisions, N bugs, N conventions extraites
- Étape 3.5 : N drifts identifiés
- Étape 4 : N fichiers détaillés (X in extenso, Y résumés)
- Étape 5 : Assemblage terminé
- Étape 6 : 8/8 checks PASS
- Étape 7 : Clone sauvegardé dans download/ (+ jumeau .yaml et check 10 si --yaml)

Stage Summary:
- Clone produit : [nom-du-clone].md ([taille] Ko)
- 8/8 checks PASS
- Profil : [NORMAL|ECO|VIEUX PC]
```

---


## §3 — RELATIONS

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet des relations inter-skills.

Relations directes de clone-chat (extrait de SHARED §3.1) :

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Archivé par | Sessions longues, optionnel, version >= v3.6.1 |
| correct-work | Vérifié par | Validation croisée, §3.5 Context Drift, version >= v2.4.0 |
| skill-creator | Conventions par | Conventions structurelles, version >= v1.0.0 |
| KNOWLEDGE.md | Lecture seule | Consultation du registre KB pour enrichissement §2 |

---


## §5 — INSTRUCTIONS D'INSTALLATION

### §5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}clone-chat/références
```

### §5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~480 lignes) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** : contexte écosystème (voir SHARED §0), mention du corpus de skills (nombre réel courant, recalibré), variables `{{SKILLS_ROOT}}`, `{{KB_PATH}}`, `{{KB_ENABLED}}`
3. **§1 — Spécification fonctionnelle** : objectif, 7+1 étapes (détail de chaque), modes thématiques (§1.12), profils ressource
4. **§2 — Spécification technique** : format sortie, stack, grille #token, intégration gen-plan, mitigation taille, structure fichiers
5. **§3 — Conventions** : nommage (SHARED §1.2), chemins relatifs, règle in extenso, numérotation §0-§5, Context Drift obligatoire
6. **§4 — Relations** : gen-plan (§4.1), correct-work (§4.2), skill-creator (§4.3)
7. **§5 — Auto-clonage** : mécanisme de croissance, fichiers de référence
8. **Historique des versions** : porté par la table §7 du PM vivant de la famille (R4 une information une source — KO-L003) ; aucune section locale requise dans SKILL.md.

### §5.3 Créer le fichier de référence

Le contenu in extenso du template est en §9.

### §5.4 Mettre à jour KNOWLEDGE.md

Ajouter l'entrée clone-chat au registre KB (format SHARED §2.2) :

```markdown
## clone-chat v2.1.0

- **Category** : ecosystem
- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, intégration gen-plan v3.6.1+ KB.
- **Dépend de** : gen-plan >= v3.6.1 (optionnel), correct-work >= v2.4.0 (validation croisée), skill-creator >= v1.0.0 (conventions), skill-creator >= v1.0.0 (conventions), skill-creator >= v1.0.0 (conventions)
- **Utilisé par** : gen-plan (E4, E15), correct-work (Mode CIBLE, §3.5)
- **Dernière calibration** : [date]
- **Statut** : stable
```

### §5.5 Mettre à jour les cross-references

Vérifier que (SHARED §3.2) :
1. gen-plan mentionne clone-chat dans ses dépendances (déjà fait)
2. correct-work mentionne clone-chat dans ses dépendances (déjà fait)
3. KNOWLEDGE.md mentionne clone-chat dans les entrées « Utilisé par » de gen-plan et correct-work

---

## §6 — CONVENTIONS

- Nommage kebab-case ; sections de clone préfixées « § » (§0 règle zéro, §1.0 héritage,
  §3.5 Context Drift, §5 auto-clonage)
- Worklog format SHARED §1.4
- Clonage en DERNIER dans l'ordonnancement (leçon E23) : l'instantané de clôture absorbe
  l'état le plus frais
- Scellement APRÈS enrichissement final (méthode neutral-line, Annexe D du PDF) pour que la
  SHA déclarée reste vérifiable byte-identique
- Thèmes (v2.1.0) : slug kebab-case, règle de preuve ≥2 par thème (R4), exclusions toujours
  citées en §0bis d'un clone thématique ; le clone complet demeure l'instantané de clôture
  canonique — les clones thématiques en dérivent et ne le remplacent jamais (§5 inchangé)
- Cache d'analyse (v2.2.0) : le clone antérieur canonique est le cache sémantique —
  réutilisation byte-stable des sessions couvertes, re-analyse du delta worklog uniquement
  (§1.13) ; le cache n'accélère JAMAIS la validation : les 8 checks s'exécutent sur le
  clone final complet
- Jumeau YAML (v2.3.0) : `--yaml` (alias `--yalm`) ajoute au clone un jumeau `.yaml`
  DÉRIVÉ (vue machine non canonique — R4), idempotent, validé par le check 10 (§1.14) ;
  le Markdown demeure l'unique instantané canonique ; « YALM » (formulation propriétaire)
  est la lecture propriétaire de YAML, alias accepté au déclencheur
