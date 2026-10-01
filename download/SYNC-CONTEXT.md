# Procédure de Synchronisation du Contexte Système

> **Version** : 1.2.0
> **Date** : 2026-10-02
> **Objet** : Maintenir la cohérence entre `PROMPT-MAITRE-SHARED.md` (source de vérité) et les blocs `## ⚙️ CONTEXTE SYSTÈME` embarqués dans les prompts maîtres.

## Contexte

Le bloc `## ⚙️ CONTEXTE SYSTÈME` présent dans chaque prompt maître actif est une **copie figée** des sections §0, §1.1 et §1.2 du fichier `PROMPT-MAITRE-SHARED.md` à la version v1.5.2.

Si le SHARED évolue (nouvelles conventions, nouvelles variables, correction de règles), les blocs embarqués doivent être resynchronisés.

### État du corpus (mis à jour 2026-10-02 — fusion installateurs v1.1.0)

- **Corpus canonique `skills/@mon-ecosysteme/`** : l'invariant `CORPUS_ATTENDU` de `scripts/check-ecosysteme-integrity.py` fait foi (dérivation dynamique — KO-L003) ; dernier recalibrage : **21 fichiers** (fusion installateurs PM-INSTALL v1.1.0 — historique : 21 @6ea0e0c, 22 @v3.17.1, 21 après fusion).
- Dernier changement : fusion installateurs PM-INSTALL v1.1.0 (directive utilisateur « source d'installation unique ») — `INSTALL-ECOSYSTEME.md` supprimé (R4) ; miroir `skills/_prompts-maitres/` supprimé (exécution décision d'architecture v2.0 — le script `restore-miroir.py` avait disparu au wipe inter-sessions et n'est pas reconstitué ; la voie de restauration est l'archive).
- **Deux voies de diffusion byte-identiques** (le corpus fait foi, sens de réplication corpus → canaux) :
  1. **Canal download/** — SYNC_MAP de 11 fichiers courants (ci-dessous), répliqué par `scripts/sync-download.py --sync` ;
  2. **Archive** `download/mon-ecosysteme_archive.zip` — véhicule d'intégrité v2.1 (corpus byte-identique + extras sous `homologues/` uniquement).

## Fichiers concernés par la synchronisation

| # | Fichier | Niveau | Emplacement du bloc |
| :--- | :--- | :---: | :--- |
| 1 | `PROMPT-MAITRE-GEN-PLAN-v3.11.0.md` | N1 | Après le frontmatter |
| 2 | `PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md` | N1 | Après le frontmatter |
| 3 | `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | N1 | Après le frontmatter |
| 4 | `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | N1 | Après le frontmatter |
| 5 | Tous les `SKILL.md` (94 fichiers au 1er niveau de `skills/`) | N2 | §0 — Contexte Système |
| 6 | Tous les fichiers `.agent` (2 fichiers) | N2 | Après le titre |
| 7 | Scripts `.py` porteurs du bloc en docstring (78 fichiers sur 106 dans `scripts/`) | N3 | Docstring en en-tête |

> **Note N1** : les prompts maîtres GEN-PLAN postérieurs à la v3.11.0 (v3.12.0 → v3.17.x) ne portent plus le bloc figé — ils s'appuient sur la dépendance externe au registre KB (`skills/KNOWLEDGE.md`, Règle Zéro : KB source de vérité). Le dernier porteur N1 est donc la v3.11.0 ; `scripts/sync-context-block.py` cible exactement les 4 fichiers du tableau (INSTALL-ECOSYSTEME.md retiré — fusion installateurs v1.1.0, R4).
> **Rétro-compatibilité R2** : les versions antérieures (PM GEN-PLAN v3.6.1 → v3.10.0, PM CORRECT-WORK v2.4.0/v2.5.0) sont conservées byte-identité historique assumée (§11b) — elles ne sont PAS des cibles de resynchronisation.

## Procédure étape par étape

### Étape 1 : Modifier la source de vérité
Éditer `PROMPT-MAITRE-SHARED.md` avec les nouvelles informations.

### Étape 2 : Incrémenter la version
Mettre à jour le champ `Version` dans l'en-tête du SHARED.
Exemple : `v1.5.2` → `v1.6.0` (si nouvelle convention), `v1.5.3` (si correction mineure).

### Étape 3 : Exécuter les scripts de synchronisation
```bash
python scripts/sync-context-block.py --level all   # bloc figé N1 (4 porteurs)
python scripts/propagate-context.py                # N2 skills + N3 scripts
```

### Étape 4 : Répliquer sur les deux voies
```bash
python scripts/sync-download.py --sync --force     # canal download/ (SYNC_MAP 11)
```
Puis régénérer l'archive si le corpus lui-même a changé (round-trip v2.1 vérifié par l'arbitre integrity).

### Étape 5 : Vérifier
```bash
python scripts/verify-cross.py --check-context     # cohérence des blocs embarqués
python scripts/check-ecosysteme-integrity.py       # corpus 21 + miroir + canal + archive
python scripts/test-coherence-interactions.py      # cohérence inter-fichiers
```

### Étape 6 : Commit
```bash
git add .
git commit -m "chore(shared): synchronisation Contexte Système v[X.Y.Z]"
git push origin main
```

## Fréquence recommandée

- **À chaque modification du SHARED** : Synchronisation immédiate requise.
- **À chaque changement du corpus** (ajout/retrait de fichier, montée de version) : recalibrage L004 des arbitres (`CORPUS_ATTENDU`, SYNC_MAP) + mise à jour de la présente section « État du corpus ».
- **Audit trimestriel** : Vérifier que les blocs embarqués correspondent toujours à la version courante du SHARED.

## Commandes rapides

```bash
# Synchroniser uniquement les prompts maîtres (Niveau 1)
python scripts/sync-context-block.py --level all

# Synchroniser uniquement les skills (Niveau 2)
python scripts/propagate-context.py

# Répliquer le corpus sur le miroir et le canal download/
python scripts/restore-miroir.py
python scripts/sync-download.py --sync --force
```

## En cas de conflit

Si la synchronisation automatique échoue :
1. Identifier le fichier problématique
2. Supprimer manuellement l'ancien bloc Contexte Système
3. Réexécuter le script de synchronisation
4. Vérifier avec `verify-cross.py`
5. Si le miroir diverge du corpus : `python scripts/restore-miroir.py` (sens corpus → miroir fait foi, invariant SHARED §1.2)
