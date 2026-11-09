# CLONE DE DISCUSSION — Migration photo iphone17→iphone18 + intégration écosystème Knowledge

> **Date du clone** : 2026-10-20
> **Source** : Discussion entre le propriétaire (bigleon2) et l'assistant (session `web-38713acd`, canal zai-web)
> **Sessions couvertes** : 7 entrées worklog (Tasks 41→45, du 2026-10-08 au 2026-10-20) + mission en cours
> **Version clone-chat** : 2.0.1 · **Profil** : NORMAL (discussion moyenne) · **8/8 checks** : voir §6

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

**Contexte matériel cible** : conteneur sandbox `/home/z/my-project/` (l'écraseur local fauche les dossiers entre les tours — leçons Tasks 17/44 du dépôt) ; écosystème Knowledge **réinstallé à jour** sur l'hôte (`skills/` : gen-plan v3.23.1, correct-work v2.7.0, clone-chat v2.0.1, 23 familles syncées) ; clone canonique du dépôt `bigleon2/KNOWLEDGE` à `/home/z/my-project/tmp/KNOWLEDGE-repo` @ `1020518` (= origin/main, lecture publique sans jeton) ; registre KB `skills/KNOWLEDGE.md` 33 entrées ; PMs photo dans `skills/@photos/` du dépôt (source de vérité).

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.0 Héritage — chaîne de clonage

Lignée : **aucun prédécesseur direct** — premier clone de la session `web-38713acd`. Le dépôt distant contient par ailleurs des clones d'AUTRES sessions (`download/clone-discussion-2026-09-27-ecosysteme-knowledge-b13-r7*.md`, lignée B13) qui ne font pas partie de cette chaîne. L'état de départ connu de la présente session : dépôt `bigleon2/KNOWLEDGE` @ `3eebe65` (vérifié en Task 41), aucun fichier photo versionné.

### §1.1 Résumé global

La discussion a réalisé la **migration générationnelle du skill photo « iphone17-photos » → « iphone18-photos »** : le prompt maître de migration (`iphone-photos-migration.md`) a été exécuté de bout en bout (checkpoints humains G-M1/G-M3/G-M5), produisant `iphone18-photos.md` v1.0 (preset `iphone18_max`, règle R18 ouverture variable simulée ƒ/1.48–ƒ/4.0, squelette spéculatif iphone19), auto-audité 100 % (A1→A8, 11 blocs littéraux vs v2.0). Le skill a été **testé empiriquement** sur photo réelle (PA-TEST-001 : pipeline §1→§9 complet, QC 12/12 PASS, validation propriétaire sans réserve §9 = « non »), archivé (`iphone18.zip`, 9 fichiers) puis **poussé au dépôt distant** (`skills/@photos/`, commit `1020518`, byte-identité SHA-256). L'écosystème local, fauché par l'écraseur, a été **réinstallé à jour** via le pipeline d'installation du dépôt. La mission en cours (Task 45, gen-plan step) génère les **skills formels iphone18/iphone17** pour l'écosystème personnel puis les teste sur deux nouvelles photos.

### §1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | 2026-10-08 | Task 41 — Plan migration (gen-plan E1-E12, Phases 0-2, checkpoint G-M3) | `plan-task41-migration-iphone18-photos.md`, `plan-integration-task41-phase3.md`, `iphone17-photos.md` (v2.0 archivé), `iphone-photos-migration.md` |
| 2 | 2026-10-09 | Task 41 suite — GO propriétaire, Phases 4-6 | `iphone18-photos.md` v1.0, `rapport-final-task41-migration-iphone18.md`, `scripts/task41-audit-livrable.py` |
| 3 | 2026-10-09 | Task 42 — Test empirique PA-TEST-001 | `PA-TEST-001-amelioration-P1-P6.png`, `PA-TEST-001-iphone18-max.png`, `rapport-PA-TEST-001.md`, `iphone18.zip`, `scripts/task42-edit.mjs` |
| 4 | 2026-10-19 | Task 43 — Exécution vue-upload (portail livrables) | Fenêtre --hold 540 s, téléchargement_effectif `iphone18.zip` par le propriétaire |
| 5 | 2026-10-19/20 | Task 42 clôture §9 — réponse « non » | Fin de traitement (G7), PA-TEST-001 validé sans réserve |
| 6 | 2026-10-20 | Task 44 — Push skills photo au dépôt | `skills/@photos/` (3 PMs + README), commit `1020518`, entrées worklog dépôt |
| 7 | 2026-10-20 | Task 45 — Mission gen-plan(step) EN COURS | Pré-vol écosystème (réinstallation PASS), `plan-task45-mission-step.md`, Groupe A (ce clone) |

### §1.3 Détail par session

**T41 (plan)** : gen-plan v3.20.0 exécuté E1-E12, answer key D001-D011 PASS, sources web Task 41 (Apple Newsroom/Specs/DXOMARK — iPhone 18 Pro Max `confirmé`, keynote 9/9/2026, DXOMARK 172/nuit 150), 6 intégrations du plan Phase 3 validées, generation bloquée au checkpoint G-M3 jusqu'au GO.
**T41 suite** : GO reçu → Phase 4 (génération v1.0, reset de version §6-1 : nouveau document = v1.0, 16 changements vs v2.0 tracés), Phase 5 (auto-audit scripté 4 itérations — faux positif A5 corrigé, coquille source R17 « pitié »→« piqué » corrigée et tracée, regex gras normalisée → PASS 100 %), Phase 6 (rapport final, 3 suggestions). PAT utilisé en lecture éphémère pour vérifier le distant (vierge de fichiers photo).
**T42** : photo `Marjo, Lydie et tonyo.jpg` (2048×1536) — analyse grille ANALYSE-v2 (A1-A10, B1-B6 : 12 visages, scène after-show nocturne), moteur R1-R18 (R18 défaut auto → ƒ/4.0), plan YAML `PA-TEST-20261009-001` affiché avant exécution (règle 3), CLI z-ai image-edit KO (erreur 1210 transmission image locale) → **contournement SDK base64 via script .mjs** (appel 1 : P1-P6 ; appel 2 : rendu iphone18_max + R18) ; QC comparatif 12/12 PASS ; rapport + zip (248,6 Ko, 9 fichiers).
**T43** : skill vue-upload v1.2.0 exécuté selon son protocole §1.2 : garde E1-INSTALL, panel rapide --json (voie froide 0,004 s, edge :81 vivant), fenêtre --hold 540 s ; journal serveur : 5 chargements UI, ~26 GET /files, **GET /get/download/iphone18.zip → 200** (téléchargement effectif).
**T42 clôture** : réponse §9 = « non » → §9-2 du skill : fin de traitement, aucune retouche spontanée (G7) ; livrables laissés en l'état (stables vs zip téléchargé).
**T44** : constat wipes (KNOWLEDGE/ et ecosystem/ fauchés) → clone frais (distant passé à b75a620 — autre session dessin-technique Tasks 8-13) ; création `skills/@photos/` (convention @ SHARED §1.2, précédent @historique) ; 3 PMs byte-identiques (SHA-256 : `6b2846fd…`/`2887e9e3…`/`3a5e95d6…`) + README règles (R2 byte-identité, courante unique, hors registre KB, restauration par clone) ; **KB volontairement non modifié** (compteurs ECO_SKILLS 33 des arbitres préservés) ; commit `1020518` (+1017/-0) + push URL jetable PAT ; audit anti-persistance : 0 valeur de PAT dans l'arbre.
**T45 (en cours)** : pré-vol « écosystème à jour » — clone déplacé vers chemin canonique `tmp/KNOWLEDGE-repo`, pipeline `eco_install_pipeline.py` exécuté (preflight pin b944a27 descendant-tolérant OK, garde R2 0 rétrogradation, 23 familles syncées, KB 33, 123 scripts, 1 purge non-canonique) ; plan step D001-D010 persisté ; Groupe A = ce clone.

---

## §2 — ÉCOSYSTÈME DE SKILLS (fichiers, scripts, artefacts)

### §2.1 Artefacts de la session (par catégorie)

| Catégorie | Artefact | Taille | Rôle |
|-----------|----------|--------|------|
| documents | `download/iphone18-photos.md` | 31,8 Ko / 357 L | PM COURANT v1.0 — pipeline complet §0→§13 (preset iphone18_max, R18, QC 12, squelette iphone19 INACTIF) |
| documents | `download/iphone17-photos.md` | 25,2 Ko / 341 L | PM ARCHIVÉ v2.0 — génération précédente (source de la migration) |
| documents | `download/iphone-photos-migration.md` | 12,2 Ko / 271 L | PM migration v1.0 — Phases 0→6 + checkpoints G-M1/M3/M5 (réutilisable iphone18→iphone19) |
| documents | `download/rapport-final-task41-migration-iphone18.md` | 7,2 Ko | Rapport final migration (3 suggestions) |
| documents | `download/rapport-PA-TEST-001.md` | 7,0 Ko | Rapport test empirique (QC 12/12, limites honnêtes) |
| documents | `download/plan-task45-mission-step.md` | ~5 Ko | **Plan mission en cours** (answer key D001-D010, 6 groupes step) |
| plans | `plan-task41-*`, `plan-integration-task41-phase3.md`, `plan-post-reinstall-*.json` | 0,8-13 Ko | Plans Task 41 (answer key, intégrations) |
| images | `download/PA-TEST-001-amelioration-P1-P6.png` (105 Ko), `PA-TEST-001-iphone18-max.png` (99 Ko) | 204 Ko | Sorties test T42 (1152×864 natif 4:3) |
| archives | `download/iphone18.zip` | 248,6 Ko | Archive 9 fichiers finaux (remise via portail T43) |
| scripts | `scripts/task41-audit-livrable.py` | — | Auto-audit A1-A8 + comparaison littérale 11 blocs |
| scripts | `scripts/task42-edit.mjs` + `task42-prompt1/2.txt` | — | **Contournement SDK base64** (CLI défaillant) — prompts consolidés P1-P6 / rendu |
| scripts | `scripts/task42-zip.py` | — | Assemblage archive iphone18.zip |
| dépôt | `tmp/KNOWLEDGE-repo/skills/@photos/` | 4 fichiers | Source de vérité distante (3 PMs byte-identiques + README) |
| upload | `Marjo, Lydie et tonyo.jpg` (267,9 Ko, testé T42), `musikalarue - les copines.jpg` + `musikalarue - les potos.jpg` (36,7/34,5 Ko, 604×453 — **tests T45 en cours**) | — | Photos propriétaire |

### §2.2 Enrichissement KB (registre `skills/KNOWLEDGE.md`, 33 entrées — extraits)

- **gen-plan v3.23.1** (ecosystem) : planification 4 modes/15 étapes E1-E15 ; modes step/step-ok v3.22+ (step = enchaînement autonome + correct-work(groupe)/projet ; step-ok = confirmation par groupe) ; hook E1-RES, answer key E1, arbitre answer-key-checker E7/E8 ; garde É1-INSTALL préemptive.
- **correct-work v2.7.0** (ecosystem) : 5 étapes, 4 modes PROJET/CIBLE/DIRECT/AVEUGLE ; couplage gen-plan OBLIGATOIRE Étape 1 (dernière installée) ; multi-cibles ; verdict global = pire des verdicts.
- **clone-chat v2.0.1** (ecosystem) : clonage 7+1 étapes, Étape 3.5 Context Drift (5 types), 8 checks, intégration gen-plan v3.6.1+ KB ; clonage en DERNIER (leçon E23 — contourné sur ordre explicite propriétaire, D002).
- **vue-upload v1.2.0** (ecosystem) : portail livrables (panel --hold, share/push/doctor) — exécuté T43.
- **Précédent génération skill** : **dessin-technique v1.1.1** (métier, Tasks 8-13 dépôt) — skill répertoire SKILL.md + scripts + references + evals + entrée KB 6 champs + bidirectionnalité + recalibrage KO-L004 + journal @historique. **C'est le modèle du Groupe C.**

### §2.4 Historique des interactions (extrait)

| Interaction | Nature | Détail |
|---|---|---|
| gen-plan → correct-work | hooks E9-E14 | correct-work(groupe) CIBLE après chaque groupe step (max 2 rounds), correct-work(projet) fin de chaîne |
| gen-plan → clone-chat | E15 (contourné E23) | ordre propriétaire : clone en tête de mission (D002) |
| vue-upload → gen-plan | garde É1-INSTALL | exécutée T43 (PRIORITE-NONE) |
| correct-work → gen-plan | Étape 1 OBLIGATOIRE | dernière version installée v3.23.1 (résolue dynamiquement) |
| iphone18/iphone17 (futurs) → skill-creator | conventions | Groupe C : frontmatter, evals, §0 Contexte Système N2 |

---

## §3 — DÉCISIONS CLÉS

### §3.1 Décisions utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | « go » (2026-10-09) | Checkpoint G-M3 du prompt maître migration | Déblocage Phase 4 → génération v1.0 |
| 2 | §9 = « non » (post-PA-TEST-001) | Question obligatoire post-génération | Fin de traitement (G7), zéro retouche |
| 3 | Push explicite des skills photo (2026-10-20) | Décision en suspens depuis T41 + PAT fourni | `skills/@photos/` publié au dépôt (commit 1020518) |
| 4 | Mission gen-plan(step) 7 étapes (2026-10-20) | Suite logique : skills FORMELS pour l'écosystème + tests 2 photos | Task 45 (ce plan, Groupe A→F) |
| 5 | Pré-vol « vérifie que mon écosystème local est à jour » avant la mission | Wipes constatés | Réinstallation pipeline PASS (hôte = dépôt) |

### §3.2 Bugs corrigés

| Bug | Cause | Fix | Résultat |
|-----|-------|-----|----------|
| CLI z-ai image-edit erreur 1210 (T42) | Transmission d'image locale défaillante par le CLI | Bascule SDK base64 via script `.mjs` (retry ×3) | 2 appels OK, sorties générées |
| Faux positif audit A5 (T41) | Bornage changelog insuffisant dans le script | Tolérance zones documentaires ajoutée | Audit PASS 100 % |
| KeyError R17 (T41 it.2) | Regex ne gérait pas le gras `\| **R17** \|` | Regex corrigée | Comparaison littérale OK |
| Skills écosystème absents de l'hôte (T45) | Écraseur inter-tours (documenté au dépôt) | `eco_install_pipeline.py` (clone → pipeline → hôte) | 23 familles aux versions dépôt, gardes vertes |

### §3.3 Conventions établies

| Règle | Exemple |
|-------|---------|
| Byte-identité R2 : livrables audités jamais édités en place | PMs @photos/ SHA-256 prouvées au push |
| PAT jamais persisté (URL jetable, jamais fichier/config/script) | Push T44 + audit anti-persistance 0 occurrence |
| Dossier `@` = non-skill (SHARED §1.2) | `skills/@photos/` (précédent `@historique/`) |
| Compteurs KB/arbitres jamais modifiés unilatéralement | T44 : KB non touché ; T45 : inscription EXPLICITEMENT ordonnée (D005) — recalibrage KO-L004 requis |
| Sorties photo nommées `PA-<CAS>-<seq>` (règle 13) | PA-TEST-001-* ; prochains : PA-TEST-002/003 |
| Question §9 obligatoire en fin de rapport, retouche uniquement sur demande explicite (G7) | PA-TEST-001 clos par « non » |

### §3.4 Données de calibration

QC iphone18 = 12 critères (fidélité B6, décor, R18 netteté étendue…) ; grille ANALYSE-v2 (A1-A10 technique, B1-B6 contenu, C1-C3 rendu) ; DXOMARK 172 / nuit 150 (ancrage §6.1 honnête) ; R18 pondération auto basse lumière vs netteté groupe (défaut ƒ/4.0 si pipeline nuit couvert) ; grille #token clone-chat : discussion moyenne ≈ 4500, profil NORMAL.

---

## §3.5 — ÉVOLUTIONS DE CONTEXTE (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | RECALIBRAGE | Distant `3eebe65` (vérifié T41) | `b75a620` (autre session) puis `1020518` (T44) | T44 | Task 44 Work Log | Évolution forward du dépôt (dessin-technique Tasks 8-13) |
| 2 | CORRECTION | Clone local à `KNOWLEDGE/` (T44) | `tmp/KNOWLEDGE-repo` (chemin canonique du pipeline) | T45 | Task 45 pré-vol | `eco_install_pipeline.py` attend REPO=tmp/KNOWLEDGE-repo |
| 3 | MODIFICATION | gen-plan v3.20.0 (session) | gen-plan v3.23.1 (hôte réinstallé) | T45 | Task 45 pré-vol | Réinstallation écosystème à jour (modes step disponibles) |
| 4 | ENRICHISSEMENT | Hôte fragmenté (gen-plan/correct-work absents) | 23 familles syncées + KB 33 + 123 scripts | T45 | Task 45 pré-vol | Pipeline d'installation post-wipe |
| 5 | MODIFICATION | Skills photo = dossier non-skill `@photos/` hors registre (T44) | Skills FORMELS `iphone18`/`iphone17` + inscription KB (33→35) | T45 | Mission step D004/D005 | Ordre explicite propriétaire (« pour mon écosystème personnel ») |
| 6 | CORRECTION | PAT actif exposé au canal | **Révocation recommandée URGENTE** (reste à faire propriétaire) | T44 | Task 44 Stage Summary | Expositions multiples + fragment 18c dans l'historique `6af3e0a` |

Analyse effectuée et certifiée exhaustive à la date du clone (6 drifts).

---

## §4 — INSTRUCTIONS D'UTILISATION (reprise par session héritière)

1. **Première action** : exécuter `python3 skills/gen-plan/scripts/ensure-installed.py --preempt` (garde É1-INSTALL — si l'hôte a été fauché à nouveau : `--reinstall` puis reprendre).
2. **État de la mission Task 45** (gen-plan step, plan persisté `download/plan-task45-mission-step.md`, answer key D001-D010) : pré-vol PASS ; Groupe A (clone-chat) = ce document ; **Groupes B→F à exécuter** : B correct-work(projet) · C génération skills iphone18+iphone17 (modèle dessin-technique : répertoire SKILL.md + frontmatter + §0 CS N2 + evals + trigger_evals + entrées KB 6 champs + bidirectionnalité + recalibrage KO-L004 + PM via `scripts/generer-pm-skill.py --generate <skill>` + garde R2 + push) · D correct-work(projet) · E test robuste iphone18 sur `upload/musikalarue - les copines.jpg` + `les potos.jpg` (série §10, 2 sorties `PA-TEST-002-*`, QC unitaire, rapport unifié, question §9 unique) · F idem iphone17 (`PA-TEST-003-*`) · fin de chaîne correct-work(projet).
3. **Fichiers prioritaires** (ordre de lecture) : ce clone → `download/plan-task45-mission-step.md` → `tmp/KNOWLEDGE-repo/skills/@photos/iphone18-photos.md` + `iphone17-photos.md` (pipelines complets à exécuter pour les tests) → `tmp/KNOWLEDGE-repo/skills/dessin-technique/SKILL.md` (modèle Groupe C) → `scripts/task42-edit.mjs` (contournement SDK base64 pour tout traitement d'image).
4. **Traitement d'image** : JAMAIS le CLI z-ai image-edit en direct (erreur 1210) — passer par le SDK en base64 (script .mjs, retry ×3).
5. **Sécurité** : si un PAT est nécessaire pour pousser, usage URL jetable uniquement, jamais persisté ; rappeler la révocation.
6. **Mise à jour** : worklog `/home/z/my-project/worklog.md` après CHAQUE groupe (format SHARED §1.4).

---

## §5 — AUTO-CLONAGE

Ce clone est l'instantané d'une session en **mission en cours** (Groupe A de la Task 45). Mécanisme de croissance : lors du prochain clonage (fin de mission ou sur demande), les sections §1-§3 sont **enrichies** (nouvelles sessions worklog, nouveaux artefacts, décisions et drifts des Groupes B→F) tandis que §0, §4 et §5 sont **régénérés** (état cible, instructions de reprise, chaînage). Le clonage de clôture absorbera l'état final de la mission (leçon E23 appliquée en fin d'ordonnancement). Skill référencé : **clone-chat v2.0.1** (7+1 étapes, 8 checks — §1.9). Un assistant neuf lisant ce document peut reprendre la mission sans autre contexte.

---

## §6 — VALIDATION (8 checks)

| # | Check | Résultat | Preuve |
|---|-------|----------|--------|
| 1 | Auto-suffisance | PASS | Aucun « voir fichier X » pour le contenu essentiel ; décisions/drifts/état inline ; §4 liste les sources durables à LIRE pour agir (attendu check 7) |
| 2 | Complétude worklog | PASS | 7/7 sessions du worklog en §1.2 + détail §1.3 |
| 3 | Complétude skills | PASS | Skills impliqués décrits (versions, rôle, interactions §2.2/§2.4) |
| 4 | Complétude décisions | PASS | 5 décisions + contexte + conséquence (§3.1) |
| 5 | Complétude bugs | PASS | 4 bugs cause+fix+résultat (§3.2) |
| 6 | Complétude drifts | PASS | 6 drifts typés, avant/après, session, ligne worklog, raison (§3.5) — section non vide |
| 7 | Exécutabilité | PASS | §4 instructions pas-à-pas + fichiers prioritaires ordonnés + niveaux de détail par taille (§2.1 ; résumés structurés pour PMs >200 L, in extenso pour plans courts) |
| 8 | Auto-clonage | PASS | §5 présent, auto-référentiel, mécanisme croissance décrit |

**Verdict : 8/8 PASS — clone valide.**
