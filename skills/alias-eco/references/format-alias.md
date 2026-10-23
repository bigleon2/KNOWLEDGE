# Format `$<ALIAS>` et registre `aliases.json` — Conventions (alias-eco v1.0.0)

> Référence normative du système d'alias de l'écosystème Knowledge (directive propriétaire 2026-10-23).
> Source de vérité opérationnelle : `skills/@historique/@Alias/aliases.json` (une seule source, R4).

## 1. Format d'un alias

- Syntaxe : **`$` + nom** — regex `^[A-Z0-9][A-Z0-9-]*$` (majuscules, chiffres, tirets ; jamais d'accent ni d'espace).
- Exemples valides : `$ECO-LEON`, `$ECO-DEPOT`, `$OPT-TRIO`.
- Exemples invalides (refusés par la garde `--add`) : `$eco-leon` (minuscules), `$ECO LEON` (espace), `$ÉCO` (accent).
- **Sémantique** : `$ALIAS` = la phrase complète qu'il abrège. « de $ECO-LEON » se lit « de mon écosystème personnel ».
- **Résolution à la lecture** : l'expansion se produit avant l'interprétation du message propriétaire (l'agent ou tout skill lit la forme expansée) ; l'alias est un raccourci d'ENTRÉE, jamais une transformation des livrables.
- Un alias non enregistré est signalé explicitement, jamais inventé ni expansé en aveugle.

## 2. Détection des phrases récurrentes (mécanique, `alias-manager.py`)

- **Corpus d'entrée** : transcrit de la discussion (fichiers texte passés à `--scan`/`--chat`).
- **Candidats** : n-grammes de mots répétés **≥ 3 fois** (MIN_OCC), **≥ 3 mots** (MIN_WORDS), **≥ 12 caractères** normalisés (MIN_CHARS), fenêtres ≤ 10 mots (MAX_N).
- **Tokénisation** : par espaces, ponctuation attachée — une virgule reste INTRA-phrase (« de façon cohérente, optimisée et fonctionnelle » est UN n-gramme) ; un token final de phrase (`. ! ? …`) en position interne rejette le candidat (jamais de phrase à cheval sur deux phrases).
- **Maximalité** : un candidat sous-chaîne d'un candidat plus long répété est retiré (on garde la phrase maximale).
- **Clé de déduplication stricte** : phrase normalisée (espaces repliés, ponctuation d'extrémité retirée, casse repliée) — « pas de doublons strictement identiques ».
- **Représentant stocké** : première occurrence naturelle du texte (casse et ponctuation internes réelles), ponctuation d'extrémité retirée.

## 3. Registre `aliases.json`

- Emplacement : `skills/@historique/@Alias/aliases.json` — dossier `@` = infrastructure non-skill (SHARED §1.2) ; règles de conservation du dossier parent `@historique/` (byte-identité des archives, jamais source d'installation) ne s'appliquent pas au registre lui-même : c'est un ÉTAT VIVANT (mis à jour à chaque scan), pas une archive scellée.
- Champs par entrée : `phrase` (représentant), `alias` (ou `null` — jamais inventé par la détection), `occurrences` (dernier scan), `occurrences_cumulees`, `premiere_detection`, `derniere_detection`, `source` (traçabilité : amorçage/scan/attribution).
- Ordre : tri alphabétique par `phrase` (casse repliée) — garanti à chaque sauvegarde.
- Fusion au re-scan : même clé → mise à jour des compteurs et de `derniere_detection` ; l'`alias` existant est TOUJOURS préservé ; nouvelle phrase → ajout avec `alias: null`.
- Idempotence : re-scan d'une même entrée ne crée jamais de doublon ; sortie JSON déterministe.

## 4. Limites connues (v1.0.0)

- Guillemets français « » et parenthèses en bordure de phrase ne sont pas tokénisés finement (la normalisation d'extrémité les retire) ; les phrases à cheval sur un saut de ligne sont détectées (les espaces regroupent).
- La détection est mécanique : elle propose des CANDIDATS ; la curation sémantique (fusion de variantes, choix des vraies phrases à aliaser) appartient à l'agent/propriétaire (`--add`, édition tracée).
- Seuil MIN_OCC = 3 : une phrase répétée 2 fois n'entre pas au registre par la mécanique (ajout manuel possible).
