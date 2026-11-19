# Clone de discussion — session web-ecef7f80 (Tasks 109→110), 22ᵉ de la lignée

> Session : web-ecef7f80 · chat 891cbdaf-5243-420e-9c3a-50feb93ef417 · canal zai-web. Généré le 2026-11-19 par clone-chat v2.0.2 (7+1 étapes). Directive du tour : trace `1a1f2297d90c957d` « gen-plan : "GO futur + GO-3" ».

## §0 — Contexte Système (SHARED v1.7.40)

> Écosystème Knowledge : skills/ = racine | KB = skills/KNOWLEDGE.md (55 entrées) | @mon-ecosysteme/ (9 corpus) | @historique/ (archive R4). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot. Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md, jamais le PM du corpus. Versionnée : gen-plan v3.43.0 · correct-work v2.11.0 · clone-chat v2.0.2 · script-creator v1.2.0 · correct-py v1.2.0 · propagate-context v2.2.0 · scelleur v2.4 (task-f5-seal-archive-v24.py) · SHARED v1.7.40 · PM-INSTALL v1.10.0.

## §1 — Worklog chronologique (fenêtre du clone : suites 155-156)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 155 | 2026-11-19 | Task 109 SUIVI — pendance PUSH Task 108 ÉTEINTE : push 19eb34b1..f658e4c9 rc=0 (E15 34ᵉ) + commit SUIVI poussé (E15 35ᵉ), parité vérifiée ls-remote anonyme ; tâche 1 (révocation ancien PAT Task 107) maintenue OUVERTE [PROPRIÉTAIRE — CRITIQUE] |
| 156 | 2026-11-19 | Task 110 « GO futur + GO-3 » — GO propriétaire pour tâches 3-4-5 du livrable Task 108 : G1 F3 injecteur v2.2.0 (+durcissement mesuré en séance) + 5+2 scripts restaurés + 17 SKILL.md hôte resynchronisés ; G2 scelleur v2.4 NOUVEAU (discrimination PERTE/ÉVOLUTION git + drapeau) + harnais 9/9 + pipeline repointé + preuve byte-stable ; G3 canons v1.2.0 + cascade KO-L004 (KB, pins, rescellement mécanique, manifeste) ; G4 CW PASS + clone 22ᵉ + commit LOCAL SANS PUSH (0 PAT ce tour — pendance consignée) |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Nature | Détail |
|---|---|---|
| `scripts/propagate-context.py` | MODIFIÉ v2.1.1→v2.2.0 | 5 points : re.sub robuste (cause racine F3 : clé figée échouait silencieusement) · DRY L3 dérivé · injection docstring-aware (comment-form après docstring, canon GO-3) · remplacement 2 formes (docstring + commentée, préfixes stricts — forme enveloppée bootstrap stable R2) · durcissement : scoping ast + garde tokenize + garde de parse/délimiteurs |
| `scripts/task-f5-seal-archive-v24.py` | NOUVEAU (scelleur v2.4) | discrimination PERTE rc=2 (jamais contournable) / ÉVOLUTION LÉGITIME git (chaîne BASE→--depot-git, rescellage SANS ECHEC tracé) / divergence non commitée rc=3 + guidance / --autoriser-evolution ; EPOQUE_FIXE + round-trip + .bak hérités ; démontre la convention GO-3 par construction ; v2.3 conservé R4 |
| `scripts/task110-test-injecteur.py` | NOUVEAU (harnais) | matrice F3 a-k (15 verdicts) + idempotence ×2 ; fixtures à jetons {{VERSION}} (hygiène — leçon F1 du tour) ; bac à sable tempfile, lecture seule sur l'arbre réel |
| `scripts/task110-test-scelleur.py` | NOUVEAU (harnais) | T0-T5 (9 verdicts) sur mini-git-repo : T1 = critère d'extinction F2 (bump commité rescellé SANS ECHEC) · T5 parité v2.3/v2.4 |
| `scripts/task110-worklog-ouverture.py` | NOUVEAU | ouverture worklog suite 156 (idempotente, garde positionnelle de la note É1 — leçon F5) |
| `scripts/task110-rejeu-answer-key.py` | NOUVEAU | re-jeu mécanique D001-D010 (pattern task107) |
| `scripts/eco_install_pipeline.py` | MODIFIÉ (repointage) | étape 2 → v24 + `--depot-git REPO` (3 références, note Task 110, rc propagés inchangés) ×2 arbres |
| `skills/script-creator/SKILL.md` + `skills/correct-py/SKILL.md` | MONTÉS v1.1.0→v1.2.0 | convention « docstring d'abord, bloc CONTEXTE ensuite » (§2+§4 / §4+HISTORIQUE) — GO-3, feuille de route §8.3 Task 105 |
| `skills/KNOWLEDGE.md` + `scripts/check-ecosysteme-integrity.py` | MODIFIÉS (cascade) | 2 montées v1.2.0 + notes Dernière montée ; pins ECO_SKILLS recalibrés ×2 arbres (KO-L004) |
| `download/plan-task110-go-futur-f3-f2-go3-cw-clone.md` | LIVRABLE | plan G0-G4, answer key D001-D010, Verdict E8 PASS 2026-11-19T05:05:00Z |
| `download/rapport-cw-task110-projet.md` | LIVRABLE | CW PROJET Étapes 1-5, verdict PASS, 5 findings |
| `download/taches-restantes-task108.md` | MIS À JOUR | tâches 3-4-5 ÉTEINTES avec preuves (critères d'extinction satisfaits) |

## §3 — Décisions, bugs, conventions (Étape 3)

**Décisions d'exécution Task 110** : le message « gen-plan : "GO futur + GO-3" » interprété comme GO propriétaire (les tâches 3-4-5 étaient marquées « GO futur »/« GO propriétaire requis » dans le livrable Task 108) ; mode NULL de gen-plan (exécution classique sans portes, clause v3.21.0) ; véhicule scelleur = NOUVEAU fichier v2.4 (précédent Task 100 v2.2→v2.3) avec v2.3 conservé intact (R4) ; la comparaison git retenue pour la discrimination F2 (CW 107 proposait « drapeau OU comparaison git » — les DEUX implémentés : git = voie mécanique, drapeau = acceptation explicite) ; scoping de la substitution docstring-forme au span ast après mesure réelle de la classe de mutation (scan : 398 porteurs en docstring de module, gabarits de générateurs dynamiques v%s/v{version} jamais matchés — le scoping est un gain pur).

**Bugs (cause racine + fix + résultat vérifié)** :
1. Clé de dynamisation figée `.replace("(SHARED v1.7.31)")` (F3, héritée) : ne matchait plus dès qu'un littéral était bumpé manuellement (gabarit v1.7.39 injecté en Task 107) → re.sub sur `\(SHARED v[0-9.]+\)` → harnais cas e/f verts, 15/15.
2. Garde délimiteurs bloquait les INSERTIONS (delta 0 exigé alors qu'une insertion docstring-forme ajoute +2 `"""`) : invariant pensé pour les remplacements appliqué à tort aux insertions → delta paramétré (0 ou +2, compte `'''` invariant) → cas c/d verts.
3. Mutation de fixture par l'injecteur (leçon du tour) : la substitution textuelle matchait le TEXTE d'en-tête dans un littéral de chaîne (L37 du harnais) et avalait un délimiteur collé (SyntaxError) → durcissement 3 gardes (scoping ast, tokenize, parse+délimiteurs) + fixtures à jetons + cas j/k → 15/15, bootstrap inchangé (R2).
4. Montage bac à sable scelleur : chemins piliers doublés (`skills/skills/…` — le préfixe était déjà dans rel) → `base/rel` direct → T0 vert.

**Conventions (avec règle)** : « docstring d'abord, bloc CONTEXTE ensuite » (GO-3) — la docstring PEP 257 reste le PREMIER énoncé, le bloc §0 en lignes commentées APRÈS, jamais en second littéral (SyntaxError `from __future__`) ; inscrite aux canons script-creator/correct-py v1.2.0 + démontrée par les 3 nouveaux scripts du tour.

## §3.5 — Context Drift (Étape 3.5)

| Drift | Type | Avant → Après | Réf. |
|---|---|---|---|
| Injecteur de contexte | MODIFICATION | v2.1.1 (gabarits littéraux, injection cassante) → v2.2.0 (dynamisation robuste, injection comment-form scopée, 3 gardes) | suite 156, G1 |
| Scelleur d'archive | MODIFICATION | v2.3 (garde anti-perte sans discrimination — bloquait l'évolution légitime) → v2.4 (PERTE/ÉVOLUTION/drapeau, voie mécanique) + pipeline repointé | suite 156, G2 |
| Canons script-creator/correct-py | RECALIBRAGE | v1.1.0 → v1.2.0 (convention GO-3) + KB + pins ECO_SKILLS + manifeste | suite 156, G3 |
| Périmètre §0 | ENRICHISSEMENT | 5 scripts protégés sans bloc + 1 script orphelin (task107-rejeu) + 1 porteur stale (task105) → 7 restaurés ; 17 SKILL.md hôte stale → resynchronisés (parité 120/120) | suite 156, G1 |

## §4 — Spécifications techniques (Étape 4 — fichiers prioritaires)

Séquence héritière recommandée :
1. `download/taches-restantes-task108.md` — les tâches restantes font foi (3-4-5 éteintes ; restent : 1 révélation PAT [PROPRIÉTAIRE — CRITIQUE], 6 décision cron 531684, 7-8 AUTO).
2. `scripts/propagate-context.py` v2.2.0 + `scripts/task110-test-injecteur.py` — le couple correctif/preuve F3.
3. `scripts/task-f5-seal-archive-v24.py` + `scripts/eco_install_pipeline.py` (étape 2 v24 + --depot-git REPO) — la voie mécanique F2.
4. `skills/script-creator/SKILL.md` + `skills/correct-py/SKILL.md` v1.2.0 — la convention GO-3 (canons).
5. Bootstrap canonique : `scripts/bootstrap-ecosysteme.py` (inchangé ce tour — R2) à exécuter AVANT E1 à la reprise.

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone (lignée Task 72→110, 22ᵉ) — les sections §1-§3 sont ENRICHIES par le clone du tour, les sections §0/§4-§5 sont RÉGÉNÉRées (état courant). clone-chat référencé (skill v2.0.2, déclencheurs §A). La session héritière reprend : lire le présent clone + worklog.md (suites 155-156) + `download/taches-restantes-task108.md` (la liste fait foi) — puis exécuter le bootstrap canonique AVANT E1 ; si un PAT frais est fourni, éteindre la pendance PUSH (leçon Task 98/101).

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », dépendance externe nulle, lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = 2 sessions de la fenêtre, chacune ≥ 1 ligne) | PASS |
| S3 | Complétude skills (chaque système créé/modifié décrit §2/§4 avec version et relations) | PASS |
| S4 | Complétude décisions (décisions avec contexte+conséquence, conventions avec règle) | PASS |
| S5 | Complétude bugs (4 bugs : cause racine + fix + résultat vérifié) | PASS |
| S6 | Complétude drifts (4 drifts typés, avant/après explicites, réf. suite) | PASS |
| S7 | Exécutabilité (§4 instructions claires, fichiers prioritaires, séquence héritière) | PASS |
| S8 | Auto-clonage (§5 croissance + clone-chat référencé + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — aucun PAT n'a été fourni ni manipulé ce tour : 0 exposition, E15 inchangée à 35).

(Étape 7 — Sauvegarde : présent fichier `download/clone-chat-session-web-ecef7f80-20261119-task110.md`, enregistrement au worklog suite 156.)
