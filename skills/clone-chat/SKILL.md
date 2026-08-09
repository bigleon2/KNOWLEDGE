---
name: clone-chat
version: 1.2.0
category: ecosystem
language: fr
tags: [clone, discussion, context, drift, gen-plan, auto-clonage, worklog]
description: >
  Clone l'intégralité d'une discussion (contexte, décisions, artefacts,
  worklog) dans un fichier Markdown auto-suffisant. 7+1 étapes, Étape 3.5
  Context Drift, intégration gen-plan v3.5.0+v3.3.0 KB. Format Markdown unique,
  propriété auto-clonage.
---

# CLONE-CHAT v1.2.0

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle
session. Tu dois **reconstruire** l'intégralité du contexte à partir de ce
fichier clone.

Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : Z AI (GLM), environnement `my-project/`,
skills/ contenant 72+ skills.

---

## §1 — SPÉCIFICATIONS FONCTIONNELLES

### 1.1 Objectif

Produire un fichier Markdown **auto-suffisant** qui capture l'intégralité
du contexte d'une discussion multi-sessions : les décisions, les artefacts
produits, les spécifications techniques, et les évolutions de contexte.

Un clone doit permettre à un assistant IA dans une **nouvelle session** de
reconstruire l'état exact de la discussion et de poursuivre le travail sans
perte d'information.

### 1.2 Les 7+1 étapes

#### Étape 1 — Collecte du worklog

Lire le fichier `worklog.md` à la racine du projet. Identifier les sessions
distinctes (séparées par des lignes `---`). Extraire pour chaque session :
- Le Task ID et le nom de l'agent
- La tâche effectuée
- Les actions concrètes réalisées
- Les résultats et livrables produits

Produire un tableau chronologique des sessions.

#### Étape 2 — Collecte des artefacts

Scanner l'arborescence du projet pour identifier tous les fichiers
**créés ou modifiés** durant la discussion. Pour chaque artefact :
- Le chemin relatif
- La taille (Ko)
- Une description de son contenu et rôle

Grouper par catégorie : skills, scripts, documents, charts, archives.

#### Étape 3 — Extraction des décisions

Parcourir le worklog et le contexte pour identifier :

1. **Décisions de l'utilisateur** : chaque choix explicite avec son
   contexte et ses conséquences
2. **Bugs corrigés** : chaque bug avec cause, fix et résultat
3. **Conventions établies** : chaque règle avec sa formulation et un exemple
4. **Données de calibration** : grilles #token, métriques, historique

Produire des tableaux structurés pour chaque catégorie.

#### Étape 3.5 — Context Drift

Cette étape **trace chaque fois que le contexte a changé** durant la
discussion. C'est une étape d'analyse critique qui certifie que les
évolutions ont été détectées.

**5 types de drift** :

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

**Règle obligatoire** : Même si aucun drift n'est détecté, écrire
« Aucune évolution de contexte détectée » pour certifier que l'analyse
a bien été effectuée. Ne jamais laisser cette section vide.

#### Étape 4 — Spécifications techniques

Détailler les fichiers principaux créés ou modifiés. Le niveau de détail
dépend de la taille du fichier (convention in extenso) :

| Taille | Traitement |
|--------|------------|
| < 200 lignes | In extenso (contenu complet) |
| 200-500 lignes | In extenso avec sections condensées |
| > 500 lignes | Résumé structuré : objectifs, structure, modules clés |

Pour chaque fichier : description, signature (fonctions/modules),
chemin relatif, taille.

**Intégration gen-plan (optionnelle)** :
- Si gen-plan v3.5.0+ est présent : enrichir avec les données de
  calibration E15 et les étapes E1-E7
- Si gen-plan v3.3.0+ avec KB : enrichir §2 avec le Registre KB
  pour la description des skills

#### Étape 5 — Assemblage

Combiner toutes les sections collectées en un document Markdown unique
et cohérent. L'ordre des sections est imposé :

1. §0 — Règle zéro (contexte perdu)
2. §1 — Chronologie de la discussion
3. §2 — Écosystème de skills (fichiers, scripts, artefacts)
4. §3 — Décisions clés (décisions, bugs, conventions, calibration)
5. §3.5 — Évolutions de contexte (Context Drift)
6. §4 — Instructions d'utilisation
7. §5 — Auto-clonage

Voir `references/clone-template.md` pour la structure complète du template.

#### Étape 6 — Validation (8 checks)

Exécuter les **8 checks de validation**. Chaque check est binaire
(PASS/FAIL). Le clone est valide si 8/8 PASS.

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

#### Étape 7 — Sauvegarde

Sauvegarder le clone dans `download/` avec un nom
descriptif incluant la date et le sujet.

Format du nom : `<sujet>-clone-<AAAA-MM-JJ>.md`

Enregistrer la sauvegarde dans le worklog.

### 1.3 Profils ressource

| Profil | Comportement pour le clone |
|--------|--------------------------|
| NORMAL | Clone complet, toutes les sections détaillées |
| ECO | Clone condensé, sections §3 regroupées |
| VIEUX PC | Clone minimal, §3.5 et §5 uniquement |

Le profil est déterminé par la longueur de la discussion (voir grille
#token en §2.3).

---

## §2 — SPÉCIFICATIONS TECHNIQUES

### 2.1 Format de sortie

- Fichier Markdown unique, auto-suffisant
- Aucune dépendance externe (pas de ZIP, pas d'images embed)
- Tout le contexte est contenu dans le fichier
- Le fichier doit être lisible sans aucun outil spécifique

### 2.2 Stack

- Markdown pur (CommonMark compatible)
- Pas de dépendance externe
- Tableaux Markdown pour les données structurées
- Code fences pour les extraits de code

### 2.3 Grille #token

| Mode | #token estimé | Profil min. | Plage |
|------|--------------|-------------|-------|
| Discussion courte (< 5 sessions) | 2750 | ECO | 2000-3500 |
| Discussion moyenne (5-15 sessions) | 4500 | NORMAL | 3500-5500 |
| Discussion longue (> 15 sessions) | 7250 | NORMAL | 5500-9000 |

**Note v1.2.0** : estimation +10% par rapport à v1.1.0 pour couvrir
l'Étape 3.5 Context Drift et l'intégration gen-plan optionnelle.

### 2.4 Intégration gen-plan (optionnelle)

Clone-chat fonctionne **standalone** sans gen-plan. Si gen-plan est
présent, les enrichissements suivants sont appliqués :

| Composant gen-plan | Enrichissement clone-chat |
|--------------------|------------------------|
| v3.5.0+ (calibration) | Étape 1 : données E15, grille #token |
| v3.5.0+ (étapes E1-E7) | Étape 4 : structure de planification |
| v3.3.0+ (Registre KB) | §2 : descriptions skills depuis KB |
| v3.3.0+ (kb_path) | §4 : liens vers skills du Registre |

### 2.5 Mitigation taille

Pour les clones de discussions longues (> 15 sessions), appliquer :
1. Résumer les sessions anciennes en 1 ligne
2. Détailler §1.3 pour les 5-10 dernières sessions seulement
3. Skills stables décrits en 1 ligne

### 2.6 Structure de fichiers

```
skills/clone-chat/
├── SKILL.md
└── references/
    └── clone-template.md
```

---

## §3 — CONVENTIONS

### 3.1 Nommage des fichiers

Les skills suivent la convention : `skills/<nom>/SKILL.md`

Les références suivent la convention : `skills/<nom>/references/<fichier>.md`

### 3.2 Chemins relatifs

Tous les chemins dans le clone sont **relatifs**, jamais absolus.

- Correct : `skills/clone-chat/SKILL.md`
- Incorrect : `/un/chemin/absolu/quelconque/skills/clone-chat/SKILL.md`

### 3.3 Règle in extenso

| Taille fichier | Traitement dans le clone |
|----------------|------------------------|
| < 200 lignes | Contenu complet (in extenso) |
| 200-500 lignes | In extenso avec sections condensées |
| > 500 lignes | Résumé structuré (spécifications + structure) |

### 3.4 Numérotation des sections

Les sections du clone utilisent la numérotation §0-§5 (pas 1-8).

### 3.5 Context Drift obligatoire

La section §3.5 doit toujours être présente, même si aucun drift n'est
détecté. Écrire « Aucune évolution de contexte détectée » certifie
l'analyse.

---

## §4 — RELATIONS AVEC LES AUTRES SKILLS

### 4.1 gen-plan

- **Orchestration amont** : gen-plan structure la discussion en étapes
  E1-E15. clone-chat utilise ces données pour Étape 1 (collecte worklog)
  et Étape 4 (spécifications techniques)
- **Calibration** : les données de calibration E15 de gen-plan alimentent
  la grille #token du clone (§2.3)
- **Registre KB** : si gen-plan v3.3.0+ avec KB, les descriptions des
  skills dans le clone sont enrichies depuis le Registre
- **Optionnel** : clone-chat fonctionne sans gen-plan

### 4.2 correct-work

- **Validation croisée** : correct-work en mode CIBLE peut valider un
  clone produit par clone-chat (audit SKILL.md, template, clone artefact)
- **Context Drift** : correct-work peut identifier des drifts que clone-chat
  n'a pas détectés (mode CIBLE, §3.5)
- **Co-évolution** : les corrections de correct-work génèrent des drifts
  de type CORRECTION dans le clone
- **Session 17** : correct-work a audité clone-chat v1.0.0 avec 11+4+10
  critères, identifié 8 problèmes (3 HAUTE, 3 MOYENNE, 2 BASSE),
  tous corrigés → v1.1.0

### 4.3 skill-creator

- **Conventions** : clone-chat suit les conventions de formatage établies
  par skill-creator (YAML frontmatter, structure §0-§5)

---

## §5 — AUTO-CLONAGE

Ce skill est **auto-référentiel**. À la fin de chaque session où des
modifications significatives ont été apportées :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra :
   - Tout le contexte du clone précédent (discussion originale)
   - Tout le nouveau contexte de la discussion en cours
3. Le nouveau clone **remplace** le fichier de clone précédent
4. Le clone « grandit » à chaque session sans jamais perdre l'historique

**Mécanisme de croissance** :
- Les sections §1-§3 (incluant §3.5 Context Drift) sont **enrichies**
  avec les nouvelles sessions et les nouveaux artefacts
- Les sections §0, §4 et §5 sont **régénérées à l'identique** car
  elles sont auto-référentielles (le template ne change pas)

**Propriété fondamentale** : un clone peut se cloner lui-même. Le §5
décrit cette propriété, et le template (`references/clone-template.md`)
inclut toujours le §5 pour permettre la chaîne de clonage infinie.

### 5.1 Fichiers de référence

| Fichier | Description |
|---------|-------------|
| `references/clone-template.md` | Template de structure pour les clones produits |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-07-29 | Version initiale, 7 étapes, template, auto-clonage |
| 1.1.0 | 2026-07-29 | 8 corrections correct-work (§0-§5, #token, chemins) |
| 1.2.0 | 2026-07-29 | Étape 3.5 Context Drift, 5 types, 8 checks, gen-plan KB |
