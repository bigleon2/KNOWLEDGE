# Clone de discussion — session web-220878ed (3ᵉ fenêtre) : photo de groupe vivante — qualité seule + GIF mouvement marqué

> **Auto-clonage** : ce document est auto-suffisant — une session héritière peut reprendre le contexte sans fichier externe (règle zéro). Généré le 2026-11-23 · gen-plan v3.43.0 / correct-work v2.11.0 / clone-chat v2.0.2 · PM-INSTALL v1.10.0 · propriétaire : Kubota (Farm Machinery Europe) — lignée photo de groupe (Tasks 6-7).

## §0 — Contexte Système (SHARED v1.7.40)

Écosystème Knowledge : SKILLS_ROOT=skills/ | KB_PATH=skills/KNOWLEDGE.md | 55 entrées KB + collections @ · dépôt git local miroir `/home/z/my-project/KNOWLEDGE-repo` (github.com/bigleon2/KNOWLEDGE, pin a5daa964) · conventions : kebab-case, semver, #token, français exclusif (règle d'or n°6) · référence canonique « mon skill X » = forme installée `skills/X/SKILL.md`, jamais le PM du corpus · KO-L009 : 0 jeton manipulé · R2 anti-rétrogradation · R4 une information une source · bootstrap canonique `scripts/bootstrap-ecosysteme.py` (PM-INSTALL §3.2-c, 1 commande : preflight → dry-run → installation → certification 6 arbitres → garde É1-INSTALL) · **9ᵉ recyclage absorbé cette fenêtre** : réparation dérive 2770 fichiers (reset --hard LOCAL) + ré-alignement 5 en-têtes §0 v1.7.44/43→v1.7.40 (asr/llm/tts/vlm/rea-analysis — récurrent après reset) ; re-vérifier ces 5 en-têtes après TOUT reset · wipe inter-sessions = cas documenté · clonages antérieurs : `download/clone-session-web-220878ed-20261123-mise-en-page-kps.md` (Tasks 1-4) et `download/clone-session-web-220878ed-20261123-task5-kps2.md` (Task 5).

## §1 — Worklog chronologique (fenêtre du clone : Tasks 6-7)

| Task | Date | Faits saillants |
|---|---|---|
| 6 | 2026-11-23 (3ᵉ fenêtre — présente discussion) | Photo de groupe fournie (`upload/maman fume 2~2.jpg`, scan 607×341, années 90) — levée de la pendance Task 5 (b) · pipeline iphone18 : `PA-GROUPE-001.png` restauration vive (QC 12/12) · demande propriétaire « version moins flou + GIF personnages en mouvement » → gen-plan `download/plan-task6-photo-groupe-vivant.md` (D001-D006 PASS) · `PA-GROUPE-002.png` (défloutage, QC fidélité) · `PA-GROUPE-003-groupe-vivant.gif` (spec anti-modifications v2 exécutée : champ de déplacement périodique déterministe sur masques featherés, fond pixel-identique, 1024×585, 6,94 Mo, QC Q1-Q8 8/8) |
| 7 | 2026-11-23 (3ᵉ fenêtre — présent clone) | Bootstrap ré-exécuté en ouverture (9ᵉ recyclage absorbé — INSTALLE 6/6) · **insatisfaction propriétaire sur le rendu trop transformé** → gen-plan `download/plan-task7-photo-qualite-gif-marque.md` (D001-D007) · `PA-GROUPE-004.png` **qualité seule** depuis le scan original (défloutage/denoise/lisibilité sobres, teintes & ambiance 90s verrouillées) · `PA-GROUPE-005-groupe-vivant-marque.gif` mouvement ×2,63 (9,61 px, 896×512, 8,77 Mo, QC 8/8, idempotence ×2) · correct-work --bloc **19/19 PASS** (`download/rapport-cw-task7-bloc.md`, 1 réserve) · clone présent scellé 8/8 |

Chaque Task a son entrée intégrale au `worklog.md` (source de vérité — format SHARED §1.4).

## §2 — Artefacts de la fenêtre (Étape 2)

| Catégorie | Fichiers |
|---|---|
| Livrables photo | **`download/PA-GROUPE-004.png`** (version « qualité seule » — référence courante) · PA-GROUPE-001/002/003 (lignée Task 6, conservés pour comparaison) |
| Livrable GIF | **`download/PA-GROUPE-005-groupe-vivant-marque.gif`** (boucle 3,84 s, 12,5 fps, 896×512 ratio 1,75 conservé, 8,77 Mo, loop infinie, fond pixel-identique) |
| Plans | `download/plan-task6-photo-groupe-vivant.md` (D001-D006 PASS) · `download/plan-task7-photo-qualite-gif-marque.md` (D001-D007 PASS, E14 scellé) |
| Rapports | `download/rapport-cw-task7-bloc.md` (correct-work 19/19 PASS, 1 réserve D002) |
| Scripts session | `scripts/restauration-pa-groupe-004.mjs` (SDK image_edit, import absolu bun) · `scripts/gif-groupe-vivant.py` (Task 6) · `scripts/gif-groupe-vivant-t7.py` (Task 7 — amplitudes paramétrées, 2ᵉ harmonique k=2 poids 0,25) · `scripts/verifier_cw_task7.py` (19 vérifs, importlib) |
| QC | `scripts/task47-qc-pa004.json` (colorimétrie originale/PA-004/PA-002) · contact sheets 003 & 005 · `scripts/cw-task7-report.json` |
| Spécification GIF | `download/PROMPT-GIF-anti-modifications-v2.md` (audité Task 5 — appliquée intégralement) |

## §3 — Décisions clés (Étape 3)

| # | Décision | Contexte | Conséquence |
|---|---|---|---|
| 1 | Technique GIF = **warp déterministe** (champ de déplacement périodique sur masques featherés) plutôt qu'un moteur génératif image→vidéo | aucun moteur vidéo disponible dans le sandbox ; les skills gif-animator* animent des sprites superposés, pas les personnages | identité garantie par construction (aucune régénération par frame), fond pixel-identique prouvé mécaniquement (diff 0,0), boucle parfaite sans crossfade — conforme à la règle de repli v2 « l'identité prime sur l'animation » ; limite assumée : pas de clignements d'yeux (inpainting génératif risquerait une dérive d'identité) |
| 2 | Task 7 : base photo = **scan original**, pas PA-002 | propriétaire insatisfait du rendu « trop transformé » de PA-GROUPE-002 (vif/contrasté) | PA-GROUPE-004 sobre : médiane 70,3→72,7, teintes fanées conservées ; réserve CW documentée : le proxy pré-enregistré Δsat était un mauvais prédicteur (minimes des deux côtés) — le ressenti portait sur la vivacité locale du rendu |
| 3 | Amplitude GIF ×2,63 (3,65 → 9,61 px) + 2ᵉ harmonique k=2 poids 0,25 | demande « mouvement un peu plus marqué » | plafond spec 5 % (≈25 px) respecté ; boucle toujours parfaite (sinusoïdes à k entiers) |
| 4 | Poids GIF : réduction de la résolution de SORTIE uniquement (1024→896 px), après validation identité | base plus sombre = entropie supérieure (11,5 Mo à 1024) | 8,77 Mo < 10 Mo — règle de poids spec v2 appliquée à la lettre |

## §4 — Instructions d'utilisation (Étape 4)

1. **Livrables courants** : `PA-GROUPE-004.png` (photo fidèle qualité-max) et `PA-GROUPE-005-groupe-vivant-marque.gif` (animation). La lignée PA-001→003 reste dans download/ pour comparaison.
2. **Régénérer le GIF** (variante d'amplitude) : éditer AX/AY/W2 dans `scripts/gif-groupe-vivant-t7.py` puis le re-exécuter (idempotent ×2 — sha256 stables à paramètres inchangés). Plafond : amplitude totale ≤ 25 px (5 % hauteur personne).
3. **Vérificateurs à froid** : `python3 scripts/verifier_cw_task7.py` (19 vérifs) · `python3 scripts/bootstrap-ecosysteme.py` (écosystème) · QC colorimétrie `scripts/task47-qc-pa004.json`.
4. **Chaîne de session héritière** : bootstrap canonique en OUVERTURE (re-vérifier les 5 en-têtes §0 après tout reset) → gen-plan(step) pour toute directive → arbitres/QC avant livraison → correct-work (projet) --bloc → clone-chat. Pendants connus : (a) retour propriétaire sur PA-GROUPE-004/005 (amplitude, durée, palette) ; (b) clignements d'yeux si un moteur génératif fidèle devenait disponible ; (c) inscription du skill mise-en-page au registre KB (GO propriétaire — reporté depuis Task 5) ; (d) docker compose config réel sur poste équipé (Task 5).

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone — §1-§3 ENRICHIES par le clone du tour, §0/§4-§5 RÉGÉNÉRÉES (état courant). La session héritière reprend : lire le présent clone + `worklog.md` (Tasks 1-7) + `download/plan-task7-photo-qualite-gif-marque.md` (answer key fait foi) + `download/rapport-cw-task7-bloc.md` (réserve) — puis exécuter le bootstrap canonique AVANT toute action. Lignée : clone mise-en-page (Tasks 1-4) → clone task5-kps2 (Task 5) → présent clone (Tasks 6-7).

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = Tasks 6-7, chacune ≥ 1 ligne ; Tasks 1-5 référencés) | PASS |
| S3 | Complétude livrables (photo + GIF décrits avec paramètres, QC, preuves) | PASS |
| S4 | Complétude décisions (4 décisions avec contexte/conséquence) | PASS |
| S5 | Complétude bugs (réserve D002 documentée cause→lecture→traitement ; réparation 9ᵉ recyclage) | PASS |
| S6 | Complétude drifts (dérive git 2770 fichiers réparée ; en-têtes §0 ré-alignés — avant/après explicites) | PASS |
| S7 | Exécutabilité (§4 : régénération GIF, vérificateurs à froid, chaîne héritière, pendants) | PASS |
| S8 | Auto-clonage (§5 croissance + lignée + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — aucun PAT ni jeton manipulé cette fenêtre).

(Étape 7 — Sauvegarde : présent fichier `download/clone-session-web-220878ed-20261123-task7-photo-gif.md`, enregistrement au worklog Task 7.)
