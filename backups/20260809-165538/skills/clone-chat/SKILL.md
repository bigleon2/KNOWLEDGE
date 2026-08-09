---
name: clone-chat
version: 2.0.0
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
description: >
  Clone l'intégralité d'une discussion (contexte, décisions, artefacts,
  worklog) dans un fichier Markdown auto-suffisant. 7+1 étapes, Étape 3.5
  Context Drift, intégration gen-plan v3.6.1+ KB. Format Markdown unique,
  propriété auto-clonage.
dependencies:
  - skill: gen-plan
    version: ">=3.6.1"
    used_at: "Calibration E15, archivage sessions longues"
    optional: true
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "Validation croisée (Mode CIBLE, §3.5)"
---

# CLONE-CHAT v2.0.0

## §0 — RÈGLE ZÉRO

L'écosystème Knowledge comprend **77 skills** (6 écosystème + 71 métier),
chacun auto-contenu dans son répertoire sous `{{SKILLS_ROOT}}` avec un
fichier `SKILL.md` principal, un frontmatter YAML, et des références
optionnelles dans `references/`. Le registre KB (`{{KB_PATH}}`) est la
source de vérité pour l'état de l'écosystème (`{{KB_ENABLED}}`).

**Principes fondamentaux** :
- Chaque skill est versionné sémantiquement (MAJEUR.MINEUR.PATCH)
- Les dépendances inter-skills sont déclarées dans le frontmatter YAML
  avec versions minimales
- Les cross-references entre skills doivent être maintenues
  bidirectionnellement
- Le registre KB (`KNOWLEDGE.md`) est la source de vérité pour l'état
  de l'écosystème

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Objectif

clone-chat produit un fichier Markdown **auto-suffisant** capturant
l'intégralité du contexte d'une discussion multi-sessions : décisions,
artefacts, spécifications techniques, évolutions de contexte (drifts), et
instructions de reprise. Le clone permet à un assistant IA dans une
nouvelle session de reconstruire l'état exact et poursuivre le travail
sans perte d'information.

### §1.2 Les 7+1 étapes

Le numbering « 7+1 » (et non « 8 étapes ») souligne que l'Étape 3.5 est
une analyse transversale insérée entre l'extraction des décisions et les
spécifications techniques, et non une étape séquentielle indépendante.

| # | Étape | Description |
|---|-------|-------------|
| 1 | Collecte du worklog | Lire `worklog.md` (SHARED §1.4), identifier sessions, produire tableau chronologique |
| 2 | Collecte des artefacts | Scanner l'arborescence, identifier fichiers créés/modifiés, grouper par catégorie |
| 3 | Extraction des décisions | Identifier décisions utilisateur, bugs, conventions, données de calibration |
| 3.5 | Context Drift | Tracer chaque changement de contexte (5 types : INVERSION, MODIFICATION, CORRECTION, ENRICHISSEMENT, RECALIBRAGE) |
| 4 | Spécifications techniques | Détailler fichiers principaux selon taille (in extenso / condensé / résumé) |
| 5 | Assemblage | Combiner en document Markdown unique, ordre imposé §0-§5 |
| 6 | Validation (8 checks) | Exécuter 8 checks de validation binaire (PASS/FAIL) |
| 7 | Sauvegarde | Sauvegarder dans `download/`, enregistrer dans le worklog |

### §1.3 Détail des étapes

**Étape 1 — Collecte du worklog** : Lire `worklog.md` à la racine du
projet (format SHARED §1.4). Identifier les sessions distinctes (séparées
par `---`). Extraire pour chaque session : Task ID, agent, tâche, actions
concrètes, résultats. Produire un tableau chronologique.

**Étape 2 — Collecte des artefacts** : Scanner l'arborescence pour
identifier tous les fichiers créés ou modifiés. Pour chaque artefact :
chemin relatif (kebab-case), taille (Ko), description. Grouper par
catégorie : skills, scripts, documents, charts, archives.

**Étape 3 — Extraction des décisions** : Parcourir le worklog et le
contexte pour extraire : (1) décisions utilisateur avec contexte et
conséquences, (2) bugs corrigés avec cause/fix/résultat, (3) conventions
établies avec règle et exemple, (4) données de calibration (grilles #token,
métriques). Produire des tableaux structurés.

**Étape 3.5 — Context Drift** : Étape d'analyse critique qui trace chaque
fois que le contexte a changé durant la discussion. Voir §1.4 pour les 5
types. Produire une table avec colonnes : #, Type, Avant, Après, Session,
Ligne worklog, Raison. **Règle obligatoire** : même si aucun drift n'est
détecté, écrire « Aucune évolution de contexte détectée » — ne jamais
laisser cette section vide.

**Étape 4 — Spécifications techniques** : Détailler les fichiers principaux.
Niveau de détail selon taille (convention in extenso, voir §2.5). Pour chaque
fichier : description, signature (fonctions/modules), chemin relatif,
taille. Si gen-plan v3.6.1+ présent : enrichir avec données calibration E15
et étapes E1-E7.

**Étape 5 — Assemblage** : Combiner toutes les sections en un document
Markdown unique et cohérent. L'ordre est imposé : §0 (Règle zéro), §1
(Chronologie), §2 (Écosystème skills), §2.4 (Historique interactions si
`{{KB_ENABLED}}`), §3 (Décisions clés), §3.5 (Context Drift), §4
(Instructions), §5 (Auto-clonage). Voir `references/clone-template.md`.

**Étape 6 — Validation (8 checks)** : Exécuter les 8 checks de validation.
Chaque check est binaire (PASS/FAIL). Le clone est valide si 8/8 PASS.
Si un check échoue, corriger avant l'étape 7. Voir §1.5 pour le détail.

**Étape 7 — Sauvegarde** : Sauvegarder le clone dans `download/` avec un
nom descriptif incluant date et sujet. Format : `<sujet>-clone-<AAAA-MM-JJ>.md`.
Enregistrer dans le worklog (format SHARED §1.4, voir §2.4).

### §1.4 5 types de drift

| Type | Définition | Exemple |
|------|-----------|--------|
| INVERSION | Décision renversée (A accepté puis A refusé) | « Version v2.0.0 » acceptée puis refusée au profit de v3.1.0 |
| MODIFICATION | Décision ajustée (paramètre X remplacé par Y) | Export DOCX remplacé par export MD par défaut |
| CORRECTION | Spécification ou décision erronée corrigée | Chemins absolus corrigés en chemins relatifs |
| ENRICHISSEMENT | Décision complétée par ajout d'un élément nouveau | Ajout Étape 3.5 Context Drift à clone-chat v1.1.0→v1.2.0 |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibrée) | Grille #token ajustée de -32% après calibration E15 |

**Format de la table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|

### §1.5 8 checks de validation

| # | Check | Critère principal | Sous-critères de validation |
|---|-------|-------------------|--------------------------|
| 1 | Auto-suffisance | Clone lisible et exécutable sans fichier externe | (a) Pas de « voir fichier X », (b) Pas de dépendance externe, (c) Assistant neuf peut le lire et agir |
| 2 | Complétude worklog | Chaque session du worklog est représentée en §1 | (a) Table §1.2 complète, (b) Chaque session a au moins 1 ligne en §1.3, (c) Sessions manquantes = FAIL |
| 3 | Complétude skills | Chaque skill créé/modifié est détaillé en §2 | (a) Version présente, (b) Description fonctionnelle, (c) Spécifications techniques, (d) Relations listées |
| 4 | Complétude décisions | Chaque décision, bug, convention est en §3 | (a) Décisions avec contexte + conséquence, (b) Bugs avec cause + fix + résultat, (c) Conventions avec règle + exemple |
| 5 | Complétude bugs | Chaque bug corrigé a cause + fix + résultat | (a) Cause racine identifiée, (b) Fix décrit, (c) Résultat vérifié, (d) Pas de bug sans résolution |
| 6 | Complétude drifts | Chaque drift identifié est dans la table §3.5 | (a) Type correct parmi les 5, (b) Avant/Après explicites, (c) Session et ligne worklog référencées, (d) Section présente même si vide |
| 7 | Exécutabilité | Un assistant IA peut reconstruire le contexte | (a) §4 instructions claires, (b) Fichiers prioritaires listés, (c) In extenso pour fichiers < 200 lignes, (d) Résumé structuré pour > 500 lignes |
| 8 | Auto-clonage | La section §5 est présente et auto-référentielle | (a) §5 décrit le mécanisme de croissance, (b) Clone-chat référencé, (c) Mécanisme §1-§3 enrichis / §0,§4-§5 régénérés |

Si un check échoue, corriger avant de passer à l'étape 7.

### §1.6 Grille #token

| Mode | #token estimé | Profil min. | Plage |
|------|--------------|-------------|-------|
| Discussion courte (< 5 sessions) | 2750 | ECO | 2000-3500 |
| Discussion moyenne (5-15 sessions) | 4500 | NORMAL | 3500-5500 |
| Discussion longue (> 15 sessions) | 7250 | NORMAL | 5500-9000 |

Estimation recalibrée v2.0.0 pour couvrir l'Étape 3.5 Context Drift,
l'intégration gen-plan v3.6.1+ KB et la section historique des interactions.

### §1.7 Profils ressource

| Profil | Comportement pour le clone |
|--------|--------------------------|
| **NORMAL** | Clone complet, toutes les sections détaillées |
| **ECO** | Clone condensé, sections §3 regroupées |
| **VIEUX PC** | Clone minimal, §3.5 et §5 uniquement |

Le profil est automatiquement déterminé par la grille #token (§1.6).

- **NORMAL** : profil par défaut pour discussions moyennes et longues.
  Toutes les sections sont détaillées, fichiers < 200 lignes in extenso.
- **ECO** : profil pour discussions courtes (< 5 sessions). Sections §3
  regroupées, skills stables décrits en 1 ligne.
- **VIEUX PC** : pour environnements avec contraintes de tokens sévères.
  Clone réduit au strict minimum : §3.5 (Context Drift) et §5 (Auto-clonage).

**Mitigation taille** (> 15 sessions) : résumer sessions anciennes en 1
ligne, détailler §1.3 pour les 5-10 dernières sessions seulement.

### §1.8 Intégration gen-plan

Clone-chat fonctionne **standalone** sans gen-plan. Si gen-plan v3.6.1+
est présent, les enrichissements suivants sont appliqués :

| Composant gen-plan | Enrichissement clone-chat |
|--------------------|------------------------|
| v3.6.1+ (calibration E15) | Étape 1 : données E15, grille #token |
| v3.6.1+ (étapes E1-E7) | Étape 4 : structure de planification |
| v3.6.1+ (Registre KB) | §2 : descriptions skills depuis `{{KB_PATH}}` |
| v3.6.1+ (kb_path) | §4 : liens vers skills du Registre |

### §1.9 Intégration KB

Si `{{KB_ENABLED}}` est `true` :
- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **Registre KB** : enrichir §2 du clone avec les descriptions des skills
  depuis le registre (format SHARED §2.2)
- **Historique des interactions** : reproduire en §2.4 l'historique des
  interactions clés entre skills (tableau chronologique)
- **Protocole de Découverte** : voir SHARED §2.3

Si `{{KB_ENABLED}}` est `false` : les sections §2.4 et les enrichissements
KB sont omis. Le clone reste fonctionnel et auto-suffisant sans le registre.

---

## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack

- **Langage** : Markdown pur (CommonMark compatible)
- **Environnement** : `{{SKILLS_ROOT}}clone-chat/`
- **Dépendances** : aucune (aucun ZIP, aucune image embed, aucun outil spécifique)
- Le fichier doit être lisible avec n'importe quel éditeur de texte

### §2.2 Format de sortie

- Fichier Markdown unique, auto-suffisant, aucune dépendance externe
- Tableaux Markdown pour données structurées, code fences pour extraits
- Le fichier est versionnable avec git et interprétable par tout assistant IA

**Structure imposée du clone (§0-§5)** :

| Section | Contenu | Détails |
|---------|---------|---------|
| **§0** | Règle zéro | Contexte perdu, tout à reconstruire, environnement cible |
| **§1** | Chronologie | Résumé global, table des sessions, détail par session |
| **§2** | Écosystème skills | Skills créés/modifiés, scripts, artefacts, historique interactions si KB |
| **§3** | Décisions clés | Décisions utilisateur, bugs, conventions, données calibration |
| **§3.5** | Context Drift | 5 types de drift, table avec avant/après/session/raison |
| **§4** | Instructions | Comment utiliser le clone, fichiers à reconstruire en priorité |
| **§5** | Auto-clonage | Mécanisme de croissance, référence au template |

### §2.3 Structure des fichiers

```
{{SKILLS_ROOT}}clone-chat/
├── SKILL.md
└── references/
    └── clone-template.md
```

### §2.4 Logging worklog

Format SHARED §1.4. Spécifiquement pour clone-chat :

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
- Étape 7 : Clone sauvegardé dans download/

Stage Summary:
- Clone produit : [nom-du-clone].md ([taille] Ko)
- 8/8 checks PASS
- Profil : [NORMAL|ECO|VIEUX PC]
```

### §2.5 Règle in extenso

| Taille fichier | Traitement dans le clone |
|----------------|------------------------|
| < 200 lignes | Contenu complet (in extenso) |
| 200-500 lignes | In extenso avec sections condensées |
| > 500 lignes | Résumé structuré (objectifs, structure, modules clés) |

Le contenu in extenso généré dans le clone doit rester < 200 lignes.
Ce seuil (200 lignes, et non 500) a été recalibré en v1.1.0 suite à
une correction correct-work.

---

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Archivé par | Sessions longues, optionnel, version >= v3.6.1 |
| correct-work | Vérifié par | Validation croisée, §3.5 Context Drift, version >= v2.4.0 |
| skill-creator | Conventions par | Conventions structurelles (YAML, §0-§5), version >= v1.0.0 |
| KNOWLEDGE.md | Lecture seule | Consultation du registre KB pour enrichissement §2 |

**gen-plan** : clone-chat utilise les données de calibration E15 et la
structure E1-E7 de gen-plan pour enrichir l'Étape 1 et l'Étape 4.
Le Registre KB (gen-plan v3.6.1+) alimente les descriptions de skills
en §2 du clone. Clone-chat fonctionne **standalone** sans gen-plan.

**correct-work** : en mode CIBLE, correct-work peut auditer un clone
produit par clone-chat et identifier des drifts non détectés (§3.5).
Les corrections génèrent des drifts de type CORRECTION dans le clone.

**skill-creator** : clone-chat suit les conventions de formatage établies
par skill-creator (YAML frontmatter, structure §0-§5).

---

## §4 — CONVENTIONS

- **kebab-case** : tous les noms de fichiers et répertoires en kebab-case
  (`clone-chat`, `clone-template`)
- **Chemins relatifs** : tous les chemins dans le clone sont relatifs,
  jamais absolus. Exemple correct : `skills/clone-chat/SKILL.md`
- **Numérotation §0-§5** : les sections du clone utilisent la numérotation
  §0-§5 (pas 1-8)
- **§3.5 Context Drift obligatoire** : la section §3.5 doit toujours être
  présente dans le clone, même si aucun drift n'est détecté. Écrire
  « Aucune évolution de contexte détectée » certifie l'analyse
- **Règle in extenso < 200 lignes** : le contenu généré in extenso dans
  le clone ne doit pas dépasser 200 lignes
- **YAML frontmatter** : chaque SKILL.md commence par un bloc YAML
  (name, version, category, language, tags, description, dependencies)
- **Worklog SHARED §1.4** : référencé pour le format de logging
- **Cross-references bidirectionnelles** : les relations inter-skills
  sont maintenues dans les deux sens (frontmatter + §3 Relations)
- **Pas de contenu externe** : aucun « voir fichier X », le clone est
  l'unique source de vérité pour la reprise

---

## §5 — AUTO-CLONAGE

Ce skill est **auto-référentiel**. Le clone contient dans son §5 les
instructions pour se cloner lui-même. À la fin d'une nouvelle session :

1. Exécuter `clone-chat` sur la discussion en cours
2. Le nouveau clone incorpore tout le contexte du clone précédent
   plus les nouvelles sessions
3. Les sections §1-§3 (données historiques) sont **enrichies**, tandis que
   §0, §4-§5 (auto-référentielles) sont **régénérées à l'identique**
4. Le nouveau clone remplace le précédent — le clone « grandit » à chaque
   session sans perte d'information (chaîne de clonage théoriquement infinie)

**Propriété fondamentale** : un clone peut se cloner lui-même. Le §5
décrit cette propriété, et le template inclut toujours le §5 pour
permettre la chaîne de clonage infinie sans perte d'information.

Fichier de référence : `references/clone-template.md`

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v1.0.0 | 2026-07-29 | Version initiale, 7 étapes, template, auto-clonage |
| v1.1.0 | 2026-07-29 | 8 corrections correct-work (§0-§5, #token, chemins) |
| v1.2.0 | 2026-07-29 | Étape 3.5 Context Drift, 5 types, 8 checks, gen-plan KB |
| v2.0.0 | 2026-08-09 | Harmonisation écosystème maître : gen-plan v3.6.0, correct-work v2.3.0, 78 skills, variables SHARED, dependencies frontmatter, worklog SHARED §1.4, prompt maître |
