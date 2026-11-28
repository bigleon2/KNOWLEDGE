```markdown
# CLONE THÉMATIQUE — [THÈME] — [TITRE DU PROJET GLOBAL]

> **Date du clone** : [AAAA-MM-JJ]
> **Mode** : `clone-chat (<theme>)` — v2.1.0
> **Thème** : [THÈME] (slug : [theme-slug])
> **Périmètre** : [N] sessions / fenêtres ([plage de dates], traces […])
> **Preuves du périmètre (≥2)** : [worklog lignes X-Y, artefacts, clones antérieurs]
> **Projet global** : clone complet de référence [fichier]
> **Version clone-chat** : 2.1.0

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU + PÉRIMÈTRE

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte du thème à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

**Auto-suffisance périmétrique** : ce clone se suffit AU PÉRIMÈTRE du thème [theme-slug]
pour reprendre ce sous-projet. La reprise GLOBALE de la discussion exige le clone complet
ou `clone-chat (ALL)` — ce clone thématique ne remplace jamais l'instantané de clôture
canonique.

### §0bis — Exclusions (hors périmètre du thème)

| # | Exclu (thème / sections) | Où le retrouver |
|---|--------------------------|-----------------|
| 1 | [thème voisin : …] | [clone complet §X / clone thématique <slug>] |
| ... | ... | ... |

---

## §1 — CHRONOLOGIE DU THÈME

### §1.1 Résumé du thème

[Paragraphe de 3-5 phrases : objet technique du sous-projet, livrables clés,
décisions structurantes, état courant.]

### §1.2 Table des sessions du thème

| # | Date | Session / fenêtre | Livrables du thème |
|---|------|-------------------|--------------------|
| 1 | [DATE] | [fenêtre/trace] | [livrables] |
| ... | ... | ... | ... |

### §1.3 Détail par session

[Groupement par période : actions principales, skills utilisés, décisions clés —
SESSIONS DU THÈME UNIQUEMENT.]

---

## §2 — ARTEFACTS DU THÈME

### §2.1 Skills créés ou modifiés (thème)

#### [nom-skill] v[x.y.z]

- **Description** : [1-2 phrases]
- **Spécification fonctionnelle** : [fonctionnalités clés, modes, étapes]
- **Spécification technique** : [stack, dépendances, structure fichiers]
- **Relations** : [autres skills]

### §2.2 Scripts créés ou modifiés (thème)

#### [nom-script].py v[x.y.z]

- **Description** : [1-2 phrases]
- **Signature** : [modules, fonctions principales, nb tests]
- **Chemin** : `scripts/[nom-script].py` ([taille])

### §2.3 Artefacts produits (thème)

| Fichier | Taille | Description |
|---------|--------|-------------|
| [chemin/relatif] | [X Ko] | [Description] |

---

## §3 — DÉCISIONS CLÉS DU THÈME

### §3.1 Décisions de l'utilisateur (thème)

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | [Décision] | [Pourquoi] | [Ce qui a changé] |

### §3.2 Bugs corrigés (thème)

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | [Bug] | [Cause racine] | [Solution] | [Résultat vérifié] |

### §3.3 Conventions établies (thème)

| Convention | Règle | Exemple |
|------------|-------|---------|
| [Nom] | [Règle] | [Exemple concret] |

### §3.5 Évolutions de contexte du thème (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | [TYPE] | [Avant] | [Après] | [N°] | [ligne] | [Raison] |

[Si aucun drift sur le thème : « Aucune évolution de contexte détectée pour ce thème ».]

---

## §4 — INSTRUCTIONS DE REPRISE DU THÈME

### État courant du sous-projet

[État exact à la clôture : HEAD git, jobs, livrables présents, verdicts en vigueur.]

### Prochaine étape exécutable

[La prochaine action concrète du sous-projet — celle qu'une session héritière
doit lancer en premier.]

### Fichiers à reconstruire en priorité

1. **[fichier prio 1]** — [Raison]
2. **[fichier prio 2]** — [Raison]
3. **[fichier prio 3]** — [Raison]

---

## §5 — AUTO-CLONAGE THÉMATIQUE

Ce clone est auto-référentiel SUR SON PÉRIMÈTRE :

1. Reprendre le sous-projet dans une nouvelle session avec ce clone
2. À la clôture du sous-projet : ré-exécuter `clone-chat (<theme>)` — le clone
   thématique grandit par ses propres sessions (§1-§3 enrichis, §0/§0bis/§4-§5 régénérés)
3. Pour une carte à jour des thèmes de la discussion globale : `clone-chat --theme`
4. Le clone complet de clôture de la session globale demeure canonique et absorbe
   ce sous-projet

**Validation** : 8 checks standards + check 9 (cohérence thématique) = 9/9 PASS.
```
