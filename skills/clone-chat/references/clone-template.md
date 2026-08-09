# CLONE DE DISCUSSION — [TITRE DU PROJET]

> **Date du clone** : [AAAA-MM-JJ]
> **Source** : Discussion entre [Utilisateur] et [Assistant]
> **Sessions couvertes** : [N] sessions (du [DATE_DÉBUT] au [DATE_FIN])
> **Version clone-chat** : 1.2.0

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : [DESCRIPTION DE L'ENVIRONNEMENT CIBLE]

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### 1.1 Résumé global

[Paragraphe de 3-5 phrases résumant l'ensemble de la discussion :
- Le sujet principal
- Les livrables clés produits
- L'évolution de la complexité
- L'état final atteint]

### 1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | [DATE] | [THÈME] | [LIVRABLES] |
| 2 | [DATE] | [THÈME] | [LIVRABLES] |
| ... | ... | ... | ... |
| N | [DATE] | [THÈME] | [LIVRABLES] |

### 1.3 Détail par session

[Groupement par période avec résumé des sessions.
Exemple :]

**Sessions 1-5 ([DATE])** : [Résumé des 5 sessions :
actions principales, skills utilisés, décisions clés.]

**Sessions 6-10 ([DATE])** : [Résumé des 5 sessions...]

**Sessions [dernières] ([DATE])** : [Résumé des dernières sessions...]

---

## §2 — ÉCOSYSTÈME DE SKILLS

### 2.1 Skills créés ou modifiés

[Pour chaque skill écosystème créé ou modifié :]

#### [nom-skill] v[x.y.z]

- **Description** : [Description en 1-2 phrases]
- **Catégorie** : [ecosystem | tool | ...] | **Langue** : [fr | en]
- **Spécification fonctionnelle** : [Fonctionnalités clés, modes,
  étapes, règles spécifiques]
- **Spécification technique** : [Stack, dépendances, structure fichiers]
- **Relations** : [Autres skills avec lesquels il interagit]

### 2.2 Scripts créés ou modifiés

[Pour chaque script :]

#### [nom-script].py v[x.y.z]

- **Description** : [Description en 1-2 phrases]
- **Signature** : [Modules, fonctions principales, nb tests]
- **Chemin** : `scripts/[nom-script].py` ([taille])

### 2.3 Artefacts produits

| Fichier | Taille | Description |
|---------|--------|-------------|
| [chemin/relatif] | [X Ko] | [Description] |
| ... | ... | ... |

---

## §3 — DÉCISIONS CLÉS

### 3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | [Décision] | [Pourquoi cette décision] | [Ce qui a changé] |
| ... | ... | ... | ... |

### 3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | [Description du bug] | [Cause racine] | [Solution] | [Résultat] |
| ... | ... | ... | ... | ... |

### 3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| [Nom] | [Règle] | [Exemple concret] |
| ... | ... | ... |

### 3.4 Données de calibration

[Grilles #token, métriques, historique de calibration.
Tableaux avec chiffres concrets.]

### 3.5 Évolutions de contexte (Context Drift)

Cette section trace chaque fois que le contexte a **changé** durant la discussion.

**5 types de drift** :

| Type | Définition |
|------|----------|
| INVERSION | Décision renversée (A accepté → A refusé) |
| MODIFICATION | Décision ajustée (paramètre X → Y) |
| CORRECTION | Spécification ou décision erronée corrigée |
| ENRICHISSEMENT | Décision complétée (ajout d'un élément nouveau) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibré) |

**Table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | [TYPE] | [Avant] | [Après] | [N°] | [ligne] | [Raison] |
| ... | ... | ... | ... | ... | ... | ... |

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire

1. Lire §0 (Règle zéro) — tout est à reconstruire
2. Reconstruire les fichiers spécifiés dans §2 :
   - [Liste des fichiers in extenso]
   - [Liste des fichiers en résumé structuré]
3. Appliquer les décisions et conventions de §3
4. Créer les artefacts listés dans §2.3
5. Se positionner à l'état exact de la fin de la discussion originale

### Fichiers à reconstruire en priorité

1. **[fichier prio 1]** — [Raison]
2. **[fichier prio 2]** — [Raison]
3. **[fichier prio 3]** — [Raison]
4. [etc.]

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra :
   - Tout le contexte de ce clone (discussion originale)
   - Tout le nouveau contexte de la discussion en cours
3. Le nouveau clone remplace ce fichier
4. Le clone « grandit » à chaque session sans perdre l'historique

**Mécanisme** : les sections §1-§3 (incluant §3.5 Context Drift) sont
enrichies avec les nouvelles sessions. Les sections §0, §4-§5 sont
régénérées à l'identique (auto-référentielles).
