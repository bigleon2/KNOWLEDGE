# Procédure de Synchronisation du Contexte Système

> **Version** : 1.4.9
> **Date** : 2026-10-12
> **Objet** : Maintenir la cohérence entre `PROMPT-MAITRE-SHARED.md` (source de vérité) et les blocs `## ⚙️ CONTEXTE SYSTÈME` embarqués dans les prompts maîtres.
> **Révision v1.4.9 (2026-10-12, Task 12 — directive propriétaire « appliquer les corrections », session web-b4d7dd19, gen-plan(step))** : état du corpus recalibré — PM CLONE-CHAT v2.0.1 vivant (Task 12 C-12c : dependencies += skill-creator conventions — F-c1, §5.2 item 8 modèle PM-§7 — F-c2), v2.0.0 archivé en `skills/@historique/prompts-maitres/clone-chat/` par `git mv` byte-identité (1 PM CLONE-CHAT archivé) ; refactoring-engineering v1.1.1 (F1/F3/F4 — §5 baseline A2 MESURÉE 7/7, plancher ref-test >=1.0.1), refactoring-test v1.0.2 (F2 — §5 baseline) ; entrées §6 rétrospectives ×5 disciplines (F-d1..F-d5) ; propagation du marqueur §0 v1.7.6→v1.7.7 recalibrée (constantes `propagate-context.py`) et exécutée (98 skills + 65 scripts + 2 agents, idempotent) ; recalibrage croisé inclus (SHARED v1.7.7 — §7 dé-figage pins n°53 F-e + §6.1, PM-INSTALL v1.7.1 — §2ter/§A.3, ULTRA régénéré — 4 familles + routes refactoring + ECO_SKILLS dérivée KB + date non figée F5/F6, README @mon-ecosysteme v2.1.7, arbitres recalibrés, archive rescellée round-trip 9/9).
> **Révision v1.4.8 (2026-10-12, directive propriétaire PM-INSTALL — session web-b4d7dd19, gen-plan(step))** : état du corpus recalibré — PM-INSTALL v1.7.0 (étape 6 refactor-guard au pipeline 10→11 étapes ; périmètre COMPLET explicite — toutes les entrées KB : 8 disciplines n°54/n°55 + outil refactoring-test + refactor-guard ; fermeture MINIMALE étendue +6 ; §A.3 extensions +6 + instantané courant ; socle §2ter +1 ligne refactoring-test-graph.py) ; recalibrage croisé inclus (SHARED v1.7.6 §3.2/§6.1, ULTRA régénéré « 11 étapes » + install_v dynamique v1.7.0, propagate-context v1.7.6 exécuté — 98 skills + 65 scripts + 2 agents idempotent, README @mon-ecosysteme v2.1.6, archive rescellée round-trip 9/9).
> **Révision v1.4.7 (2026-10-12, cascade gen-plan v3.23.1 — session web-b4d7dd19 Task 8 gen-plan(step), fusion discussion externe 468a4c26, KO-L004)** : état du corpus recalibré — PM GEN-PLAN v3.23.1 vivant (correction outil n°55 : refactoring-test = outil de la discipline refactoring-engineering — directive propriétaire ; refactor-guard v1.7.0 garde-fous déclaré, fullstack-dev inscrit), v3.23.0 archivé en `skills/@historique/prompts-maitres/gen-plan/` par `git mv` byte-identité (19 PMs GEN-PLAN archivés) ; propagation du marqueur §0 v1.7.3→v1.7.4 recalibrée (constantes `propagate-context.py`) et exécutée (idempotent ×2) ; recalibrage croisé inclus (SHARED v1.7.4 §6.1 + §7 outil/registre ×3, PM-INSTALL v1.6.4, KB entrée gen-plan + 2 entrées n°55 corrigées + refactor-guard + fullstack-dev + réciproques ×6, ULTRA régénéré, README @mon-ecosysteme v2.1.5, ECO_SKILLS arbitre 3.23.1/1.0.1/1.0.1/1.7.0/1.0.0, @historique ×3 par-skill créés + index §5).
> **Révision v1.4.6 (2026-10-12, cascade gen-plan v3.23.0 — session web-b4d7dd19 Task 7 gen-plan(step), KO-L004)** : état du corpus recalibré — PM GEN-PLAN v3.23.0 vivant (matérialisation des disciplines de refactoring n°55 — directive propriétaire), v3.22.1 archivé en `skills/@historique/prompts-maitres/gen-plan/` par `git mv` byte-identité (18 PMs GEN-PLAN archivés) ; propagation du marqueur §0 v1.7.2→v1.7.3 recalibrée (constantes `propagate-context.py`) et exécutée (97 skills + 51 scripts + 2 agents, idempotent ×2) ; recalibrage croisé inclus (SHARED v1.7.3 §6.1 + §7 définitions n°55, PM-INSTALL v1.6.3, KB entrée gen-plan + 2 entrées n°55 + réciproque correct-work, ULTRA régénéré, README @mon-ecosysteme v2.1.4, ECO_SKILLS arbitre recalibré, @historique ×3 + index §5).
> **Révision v1.4.5 (2026-10-11, cascade gen-plan v3.22.1 — session web-b4d7dd19, KO-L004)** : état du corpus recalibré — PM GEN-PLAN v3.22.1 vivant (renommage du mode step-confirm → step-ok + clause mode NULL — directive propriétaire), v3.22.0 archivé en `skills/@historique/prompts-maitres/` par `mv` byte-identité (fichier non suivi — jamais commité ; adaptation règle d'or n°1 journalisée ; 17 PMs GEN-PLAN archivés) ; propagation du marqueur §0 v1.7.1→v1.7.2 recalibrée (constantes `propagate-context.py`) et exécutée (95 skills + 50 scripts + 2 agents, idempotent) ; recalibrage croisé inclus (SHARED v1.7.2 §6.1, PM-INSTALL v1.6.2, KB entrée gen-plan + note calibration Task 6, ULTRA régénéré, README @mon-ecosysteme v2.1.3, @historique ×3 + index §5 21 PMs).
> **Révision v1.4.4 (2026-10-11, cascade gen-plan v3.22.0 — session web-b4d7dd19, KO-L004)** : état du corpus recalibré — PM GEN-PLAN v3.22.0 vivant (orchestration matérialisations n°54 + déclencheurs de mode step), v3.21.0 archivé en `skills/@historique/prompts-maitres/` par `git mv` byte-identité (16 PMs GEN-PLAN archivés) ; resynchronisation du marqueur exécutée : le contenu du bloc §0 est byte-identique entre SHARED v1.6.8 et v1.7.1 (diff mécanique : 9 lignes — version/révision/référence PM/définitions n°54, aucune ligne §0/§1.1/§1.2) mais le check « Références vives alignées » de l'arbitre interactions (dynamisé KO-L003) exige l'alignement du marqueur sur le socle courant → propagation `propagate-context.py v2.0.0` recalibrée (constantes v1.6.8→v1.7.1) : 95 skills + 50 scripts + 2 agents, idempotent ; première lecture de cette révision (avant propagation) avait consigné « aucune re-propagation requise » — décision INVALIDÉE par l'arbitre mécanique et corrigée ici (KO-L003 : l'arbitre dynamisé fait foi sur le marqueur ; le contenu restant inchangé, la propagation est un no-op sémantique) ; recalibrage croisé inclus (SHARED v1.7.1 §6.1, PM-INSTALL v1.6.1, KB 4 entrées, ULTRA régénéré, ECO_SKILLS arbitre recalibré).
> **Révision v1.4.3 (2026-10-11, Task 17)** : codification SHARED §1.2 en v1.6.8 (dossier d'archive `skills/@historique/` — R4 déplacement `git mv` byte-identité, R2 fichiers archivés jamais édités, jamais source d'installation KO-L003, table §7 du PM vivant source de vérité, re-scellement KO-L004 à chaque montée de version, résorption de la mention `_archive/` stale) ; cascade de resynchronisation exécutée : 2 porteurs N1 vivants + 93 skills N2 + 49 scripts N3 + 2 .agent depuis SHARED v1.6.8 ; Task 17-B : structure @historique/ = historique par skill (`historiques-par-skill/`) + historique du socle (`historique-autres-elements.md`) — distillation globale retirée après migration verbatim (R4 une information, une source).
> **Révision v1.4.2 (2026-10-11, Task 16)** : déduplication des PMs (directive propriétaire « ne garder que la dernière version ») — les PMs GEN-PLAN v3.11.0 et CORRECT-WORK v2.5.1 sont déplacés vers `skills/@historique/prompts-maitres/` (byte-identité scellée) et restent non-cibles de resynchronisation (R2) ; les cibles vivantes du sync sont réduites à 2 (CLONE-CHAT v2.0.0 + INSTALL-ECOSYSTEME) ; état du corpus porté à **8 fichiers** (3 PMs sources + socle) ; le dossier `@historique/` est l'archive documentaire des versions (distillation + fichiers sources).
> **Révision v1.4.1 (2026-10-02, Task 16)** : suggestions (a)/(b) — résorption F1/F2/F4 : état du corpus porté à **26 fichiers** (PMs CORRECT-WORK v2.6.0/v2.7.0 matérialisés par diffs chirurgicaux méthode B1, provenance de reconstitution tracée) ; les PMs reconstitués v2.6.0/v2.7.0 portent le bloc CONTEXTE SYSTÈME figé hérité de v2.5.1 et ne sont PAS des cibles de resynchronisation (même statut que les versions historiques — bloc gelé R2).
> **Révision v1.4.0 (2026-10-02, Task 14)** : décision d'architecture v2.2 — le canal de fichiers `download/` est supprimé (déduplication : les fichiers corpus répliqués dans `download/` étaient des doublons byte-identiques de `skills/`). L'archive d'intégrité devient l'UNIQUE voie de diffusion du corpus ; `scripts/sync-download.py` est retiré (périmètre disparu) et remplacé par la garde `scripts/task14-scan-doublons.py` (0 doublon attendu).

## Contexte

Le bloc `## ⚙️ CONTEXTE SYSTÈME` présent dans chaque prompt maître actif est une **copie figée** des sections §0, §1.1 et §1.2 du fichier `PROMPT-MAITRE-SHARED.md` à la version v1.5.2.

Si le SHARED évolue (nouvelles conventions, nouvelles variables, correction de règles), les blocs embarqués doivent être resynchronisés.

### État du corpus (mis à jour 2026-10-11 — v1.4.2 : dédup PMs vers @historique/, Task 16)

- **Corpus canonique `skills/@mon-ecosysteme/`** : l'invariant `CORPUS_ATTENDU` de `scripts/check-ecosysteme-integrity.py` fait foi (dérivation dynamique — KO-L003) ; dernier recalibrage : **8 fichiers** (3 PMs sources — GEN-PLAN v3.22.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0 — + socle SHARED/INSTALL/ULTRA/README/SYNC-CONTEXT ; les 20 PMs historiques sont archivés en `skills/@historique/prompts-maitres/` — historique : 21 @6ea0e0c, 22 @v3.17.1, 21 après fusion, 22 avec PM v3.17.2, 23 avec ultra-PM, 24 avec le clone -f, 26 avec la lignée CORRECT-WORK complétée, 27 après suppression d72226a, 8 après dédup Task 16, 8 avec GEN-PLAN v3.22.0 @v1.4.4).
- Dernier changement : directive « appliquer (a) puis (b) pour résorber les écarts F1/F2/F4 » (Task 16, session web-8a7e5653) — suggestion (b) : PMs CORRECT-WORK v2.6.0/v2.7.0 reconstitués par diffs chirurgicaux depuis v2.5.1 (méthode B1 — `scripts/materialise-pm-correct-work.py`, gardes d'unicité 24+22 motifs, provenance tracée en-tête + §7 de chaque PM) ; le corpus porte désormais la forme certifiée v2.7.0 (garde R2 du PM-INSTALL v1.3.1 §3.2).
- **Une voie de diffusion byte-identique** (le corpus fait foi, sens de réplication corpus → archive) :
  1. **Archive** `download/mon-ecosysteme_archive.zip` — véhicule d'intégrité v2.2 (corpus byte-identique + extras sous `homologues/` uniquement).
- **Rappel anti-doublons (v2.2)** : aucun fichier du corpus `@mon-ecosysteme/` ne doit exister en copie dans `download/` — un fichier y résidant sous le même nom avec un contenu byte-identique est un doublon (critère « même nom, même contexte, idempotent ») ; vérification : `python3 scripts/task14-scan-doublons.py` (0 doublon attendu). Les artefacts de session NON corpus (clones, rapports, plans — noms distincts) restent légitimes dans `download/`.

## Fichiers concernés par la synchronisation

| # | Fichier | Niveau | Emplacement du bloc |
| :--- | :--- | :---: | :--- |
| 1 | `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | N1 | Après le frontmatter |
| 2 | `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | N1 | Après le frontmatter |
| 3 | Tous les `SKILL.md` (94 fichiers au 1er niveau de `skills/`) | N2 | §0 — Contexte Système |
| 4 | Tous les fichiers `.agent` (2 fichiers) | N2 | Après le titre |
| 5 | Scripts `.py` porteurs du bloc en docstring (78 fichiers sur 106 dans `scripts/`) | N3 | Docstring en en-tête |

> **Note N1 (v1.4.2, Task 16)** : les PMs GEN-PLAN v3.11.0 et CORRECT-WORK v2.5.1 (porteurs N1 d'époque) sont archivés en `skills/@historique/prompts-maitres/` — byte-identité historique assumée (R2), non-cibles de resynchronisation. `scripts/sync-context-block.py` cible exactement les 2 fichiers du tableau (recalibré Task 16). Le PM CORRECT-WORK v2.7.0 porte le bloc figé hérité de v2.5.1 (reconstitution méthode B1) — non-cible (bloc gelé R2).
> **Rétro-compatibilité R2** : les versions antérieures (PM GEN-PLAN v3.6.1 → v3.19.0, PM CORRECT-WORK v2.4.0 → v2.6.0) sont archivées en `skills/@historique/prompts-maitres/` — byte-identité historique assumée (§11b) — elles ne sont PAS des cibles de resynchronisation. Les PMs CORRECT-WORK v2.6.0/v2.7.0 (reconstitués Task 16, méthode B1) portent le bloc figé hérité byte-identique de v2.5.1 — mêmes statut et traitement (non-cibles, bloc gelé R2, divergence documentée au §7 de chaque PM).

## Procédure étape par étape

### Étape 1 : Modifier la source de vérité
Éditer `PROMPT-MAITRE-SHARED.md` avec les nouvelles informations.

### Étape 2 : Incrémenter la version
Mettre à jour le champ `Version` dans l'en-tête du SHARED.
Exemple : `v1.5.2` → `v1.6.0` (si nouvelle convention), `v1.5.3` (si correction mineure).

### Étape 3 : Exécuter les scripts de synchronisation
```bash
python scripts/sync-context-block.py --level all   # bloc figé N1 (2 porteurs vivants)
python scripts/propagate-context.py                # N2 skills + N3 scripts
```

### Étape 4 : Resceller l'archive (unique voie de diffusion)
```bash
python3 scripts/task14-scan-doublons.py   # garde anti-doublons download/ (0 attendu)
```
Puis régénérer l'archive dès que le corpus lui-même a changé (round-trip v2.2 vérifié par l'arbitre integrity).

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
- **À chaque changement du corpus** (ajout/retrait de fichier, montée de version) : recalibrage L004 des arbitres (`CORPUS_ATTENDU`, garde anti-doublons) + mise à jour de la présente section « État du corpus ».
- **Audit trimestriel** : Vérifier que les blocs embarqués correspondent toujours à la version courante du SHARED.

## Commandes rapides

```bash
# Synchroniser uniquement les prompts maîtres (Niveau 1)
python scripts/sync-context-block.py --level all   # 2 porteurs vivants (Task 16)

# Synchroniser uniquement les skills (Niveau 2)
python scripts/propagate-context.py

# Garde anti-doublons du canal download/ (décision v2.2 — 0 doublon attendu)
python3 scripts/task14-scan-doublons.py
```

## En cas de conflit

Si la synchronisation automatique échoue :
1. Identifier le fichier problématique
2. Supprimer manuellement l'ancien bloc Contexte Système
3. Réexécuter le script de synchronisation
4. Vérifier avec `verify-cross.py`
5. Si le miroir diverge du corpus : `python scripts/restore-miroir.py` (sens corpus → miroir fait foi, invariant SHARED §1.2)
