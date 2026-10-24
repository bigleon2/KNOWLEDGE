# Format `$<ALIAS>` et registre `aliases.json` — Conventions (alias-eco v1.2.0)

> Référence normative du système d'alias de l'écosystème Knowledge (directive propriétaire 2026-10-23).
> Source de vérité opérationnelle : `skills/@historique/@Alias/aliases.json` (une seule source, R4).

## 1. Format d'un alias

- Syntaxe : **`$` + nom** — regex `^[A-Z0-9][A-Z0-9-]*$` (majuscules, chiffres, tirets ; jamais d'accent ni d'espace).
- Exemples valides : `$ECO-LEON`, `$ECO-DEPOT`, `$FACON`.
- Exemples invalides (refusés par la garde `--add`) : `$eco-leon` (minuscules), `$ECO LEON` (espace), `$ÉCO` (accent).
- **Sémantique** : `$ALIAS` = la phrase complète qu'il abrège. « de $ECO-LEON » se lit « de mon écosystème personnel ».
- **Résolution à la lecture** : l'expansion se produit avant l'interprétation du message propriétaire (l'agent ou tout skill lit la forme expansée) ; l'alias est un raccourci d'ENTRÉE, jamais une transformation des livrables.
- Un alias non enregistré est signalé explicitement, jamais inventé ni expansé en aveugle.
- **Grammaire B (v1.2.0 — GO propriétaire 2026-10-24)** : déclencheur mécanique d'attribution
  `alias-eco "<texte récurrent>" --add <ALIAS>` (variantes : guillemets français `« … »`, préfixe `$`
  optionnel sur l'ALIAS). Le délimiteur GUILLAUME (jamais parenthèses) supporte parenthèses,
  virgules, deux-points et `--add` internes dans le texte ; l'ALIAS reste au format canonique
  `^[A-Z0-9][A-Z0-9-]*$` (un nom comme `façon()` est refusé — 3 violations : minuscules, accent,
  parenthèses). Exemple canonique : `alias-eco "de façon cohérente, optimisée et fonctionnelle"
  --add FACON`.

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

## 4. Limites connues (v1.1.0)

- Description v1.1.0 : la clause d'exclusion est formulée sans radicaux des périmètres sœurs
  (Description Optimization — la v1.0.0 émettait `inventair/skill/clon/sess/livr` et polluait
  le routage heuristique voie M : 3 faux positifs sur les cas négatifs du replay).
- Guillemets français « » et parenthèses en bordure de phrase ne sont pas tokénisés finement (la normalisation d'extrémité les retire) ; les phrases à cheval sur un saut de ligne sont détectées (les espaces regroupent).
- La détection est mécanique : elle propose des CANDIDATS ; la curation sémantique (fusion de variantes, choix des vraies phrases à aliaser) appartient à l'agent/propriétaire (`--add`, édition tracée).
- Seuil MIN_OCC = 3 : une phrase répétée 2 fois n'entre pas au registre par la mécanique (ajout manuel possible).
- **Décision de normalisation `$façon()` → `$FACON`** (2026-10-24, consentements propriétaires Task 27 « effectue l'option recommandée » puis « je préfère $FACON », session web-fdf5963c) : le nom `$façon()` demandé pour la phrase « de façon cohérente, optimisée et fonctionnelle » viole la garde canonique — 3 violations (minuscules, `ç` non-ASCII, parenthèses) : rejet rc=2, jamais expansé. L'alias de la phrase, initialement attribué sous `$OPT-TRIO` (Task 25ter, même mandat corrigé), est **renommé `$FACON`** — renommage tracé (registre état vivant via `--add`, références vivantes : présente référence §1/§4, eval 7 AE-facon, KB description, journal) ; les mentions OPT-TRIO des journaux et notes de révision antérieures demeurent (historique R2, jamais rétro-édité) ; `$façon()` demeure non expansé (comportement documenté, jamais inventé) — **écrire `$FACON`**.
