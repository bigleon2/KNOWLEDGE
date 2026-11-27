# Clone de discussion — session web-220878ed (4ᵉ fenêtre) : clôture photo-GIF — livraison photo seule + audit différés

> **Auto-clonage** : ce document est auto-suffisant — une session héritière peut reprendre le contexte sans fichier externe (règle zéro). Généré le 2026-11-24 · gen-plan v3.43.0 / correct-work v2.11.0 / clone-chat v2.0.2 · PM-INSTALL v1.10.0 · propriétaire : Kubota (Farm Machinery Europe) — lignée photo de groupe (Tasks 6-7, clôture Task 8).

## §0 — Contexte Système (SHARED v1.7.40)

Écosystème Knowledge : SKILLS_ROOT=skills/ | KB_PATH=skills/KNOWLEDGE.md | 55 entrées KB + collections @ · dépôt git local miroir `/home/z/my-project/KNOWLEDGE-repo` (github.com/bigleon2/KNOWLEDGE, pin a5daa964) · conventions : kebab-case, semver, #token, français exclusif (règle d'or n°6) · référence canonique « mon skill X » = forme installée `skills/X/SKILL.md`, jamais le PM du corpus · KO-L009 : 0 jeton manipulé · R2 anti-rétrogradation · R4 une information une source · bootstrap canonique `scripts/bootstrap-ecosysteme.py` (PM-INSTALL §3.2-c, 1 commande : preflight → dry-run → installation → certification 6 arbitres → garde É1-INSTALL) · attention récurrente : après TOUT reset git du dépôt miroir, re-vérifier les 5 en-têtes §0 v1.7.40 (asr/llm/tts/vlm/rea-analysis) et supprimer un éventuel `download/README.md` plateforme · wipe inter-sessions = cas documenté · clonages antérieurs : `clone-session-web-220878ed-20261123-mise-en-page-kps.md` (Tasks 1-4) → `clone-session-web-220878ed-20261123-task5-kps2.md` (Task 5) → `clone-session-web-220878ed-20261123-task7-photo-gif.md` (Tasks 6-7) → présent clone (Task 8, clôture).

## §1 — Worklog chronologique (fenêtres récentes ; Tasks 1-5 au worklog et aux clones antérieurs)

| Task | Date | Faits saillants |
|---|---|---|
| 6 | 2026-11-23 (3ᵉ fenêtre) | Photo de groupe fournie (`upload/maman fume 2~2.jpg`, scan 607×341, années 90) — levée de la pendance Task 5 (b) · pipeline iphone18 : `PA-GROUPE-001.png` (QC 12/12) · `PA-GROUPE-002.png` (défloutage) · `PA-GROUPE-003-groupe-vivant.gif` (spec anti-modifications v2 : warp déterministe sur masques featherés, fond pixel-identique, 1024×585, 6,94 Mo, QC Q1-Q8 8/8) |
| 7 | 2026-11-23 (3ᵉ fenêtre) | Insatisfaction propriétaire (rendu « trop transformé ») → `PA-GROUPE-004.png` **qualité seule** depuis le scan original (défloutage/denoise sobres, teintes & ambiance 90s verrouillées) · `PA-GROUPE-005-groupe-vivant-marque.gif` mouvement ×2,63 (9,61 px, 896×512, 8,77 Mo, QC 8/8, idempotence ×2) · correct-work --bloc **19/19 PASS** (1 réserve D002) · clone 8/8 |
| 8 | 2026-11-24 (4ᵉ fenêtre — présent clone) | **Retour propriétaire** : le mouvement « n'est pas ce qui était voulu » (mais non détaillé — à redéfinir par le propriétaire) ; **la qualité de la photo est validée** (« m'a l'air réussi ») · G1 livraison **`download/PA-GROUPE-004.png`** seule pour validation (vérifié mécaniquement : BASE du GIF, sha256 03ccd28276c573a7…, aucune régénération) · G2 audit des différés : réserve **D002 CLÔTURÉE $FACON par validation propriétaire**, pendance Task 5 (a) levée (T6), réécriture skill mise-en-page faite (T3), download/README.md absent ; réserves hors sandbox non corrigeables ici (Docker réel, vision 501, entrée KB + PAT — côté propriétaire) ; **nouveau différé entrant** : nature du mouvement GIF à détailler — aucune régénération tant que non décrit (« jamais d'invention ») · G3 présent clone scellé 8/8 |

Chaque Task a son entrée intégrale au `worklog.md` (source de vérité — format SHARED §1.4).

## §2 — Artefacts de la fenêtre (Étape 2)

| Catégorie | Fichiers |
|---|---|
| Livrable validé | **`download/PA-GROUPE-004.png`** (1344×768, qualité seule depuis le scan original — photo utilisée pour générer le GIF, livrée seule pour validation propriétaire) |
| Référence GIF (en attente de redéfinition du mouvement) | `download/PA-GROUPE-005-groupe-vivant-marque.gif` (896×512, 3,84 s, 8,77 Mo, QC 8/8) + `PA-GROUPE-005-contact-sheet.png` |
| Historique de lignée | PA-GROUPE-001/002/003 (+ contact sheet 003) — conservés pour comparaison |
| Traces session | `worklog.md` (Tasks 1-8) · plans `plan-task6-photo-groupe-vivant.md`, `plan-task7-photo-qualite-gif-marque.md` (answer keys scellées) · rapports CW `rapport-cw-task2/5/7-bloc.md` |
| Scripts clés | `scripts/restauration-pa-groupe-004.mjs` · `scripts/gif-groupe-vivant-t7.py` (AX/AY/W2 paramétrés, 2ᵉ harmonique k=2) · `scripts/verifier_cw_task7.py` (19 vérifs à froid) · `scripts/bootstrap-ecosysteme.py` |
| Spécification GIF | `download/PROMPT-GIF-anti-modifications-v2.md` (plafond amplitude 5 % ≈ 25 px, fond pixel-identique, boucle sans crossfade, dither NONE) |

## §3 — Décisions clés (Étape 3)

| # | Décision | Contexte | Conséquence |
|---|---|---|---|
| 1 | Livraison **limitée à la photo PA-GROUPE-004** (pas de nouveau GIF) | propriétaire : le mouvement ne correspond pas à son intention, mais il ne l'a pas encore détaillée ; la photo, elle, est validée | validation propriétaire recueillie sur la base statique ; toute régénération GIF attend une description explicite du mouvement souhaité (règle « jamais d'invention » — PM §0/§5) |
| 2 | Réserve **D002 clôturée $FACON par validation propriétaire** | le proxy pré-enregistré Δsat était un mauvais prédicteur ; le propriétaire confirme le rendu | proxy révoqué au profit du jugement propriétaire ; trace append-only au worklog (rapports scellés non réécrits — R4) |
| 3 | Différé entrant consigné : **mouvement GIF à redéfinir** | « ce n'est pas le mouvement que je voulais mais c'est moi qui ne te l'a pas détaillée » | nouvelle itération GIF dès que le propriétaire décrit le mouvement voulu (types possibles à qualifer : direction, rythme, quels personnages, durée) ; plafond spec v2 inchangé (≤ 5 % hauteur) |
| 4 | Technique GIF inchangée en attente (warp déterministe, fond pixel-identique, boucle parfaite) | moteur génératif vidéo absent du sandbox ; identité garantie par construction | toute nouvelle variante passe par `scripts/gif-groupe-vivant-t7.py` (paramètres AX/AY/W2) ou une extension de spec — idempotent ×2 |

## §3.5 — Évolutions de contexte (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|---|---|---|---|---|---|
| 1 | ENRICHISSEMENT | D002 = réserve ouverte (proxy Δsat échoue) | D002 = clôturée par validation propriétaire | Task 8 | Task 8, G2 | le propriétaire a validé la qualité de la photo — la substance de la décision prime sur le proxy |
| 2 | INVERSION (partielle) | priorité = régénérer le GIF avec mouvement plus marqué (Task 7) | priorité = livraison photo seule ; GIF en attente d'une description précise du mouvement | Task 8 | Task 8, directive propriétaire | le mouvement ×2,63 ne correspond pas à l'intention du propriétaire (non détaillée) |
| 3 | CORRECTION | download/README.md pouvait réapparaître (plateforme) | absent à l'instant T — rien à corriger | Task 8 | Task 8, G2 | re-vérification systématique après recyclage |

## §4 — Instructions d'utilisation (Étape 4)

1. **Livrable à valider** : `download/PA-GROUPE-004.png` — la photo exacte avec laquelle le GIF a été généré (BASE de `gif-groupe-vivant-t7.py`, byte-identique, sha256 03ccd28276c573a7…).
2. **Prochaine itération GIF** : attendre la description du mouvement voulu par le propriétaire (quels personnages, direction, amplitude, rythme) → soit paramétrer `scripts/gif-groupe-vivant-t7.py` (AX/AY/W2 — plafond ≤ 25 px), soit étendre `PROMPT-GIF-anti-modifications-v2.md` si le mouvement demandé sort du champ « respiration/micro-balancement » (ex. geste, objet) → QC Q1-Q8 + fond diff 0,0 obligatoires.
3. **Vérificateurs à froid** : `python3 scripts/verifier_cw_task7.py` (19 vérifs) · `python3 scripts/bootstrap-ecosysteme.py` (écosystème) · QC colorimétrie `scripts/task47-qc-pa004.json`.
4. **Chaîne de session héritière** : bootstrap canonique en OUVERTURE (après tout reset : re-vérifier les 5 en-têtes §0 + download/README.md) → gen-plan(step) pour toute directive → arbitres/QC avant livraison → correct-work (projet) --bloc → clone-chat. Pendants ouverts : (a) description du mouvement GIF par le propriétaire — BLOCANT pour toute nouvelle animation ; (b) clignements d'yeux si un moteur génératif fidèle devenait disponible ; (c) entrée KB du skill mise-en-page à la prochaine poussée dépôt + révocation de l'ancien PAT (GO propriétaire — KO-L009, côté propriétaire) ; (d) docker compose réel sur poste équipé (Task 5).

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone — §1-§3 ENRICHIES par le clone du tour, §0/§4-§5 RÉGÉNÉRÉES (état courant). La session héritière reprend : lire le présent clone + `worklog.md` (Tasks 1-8) + `download/plan-task7-photo-qualite-gif-marque.md` (answer key fait foi) + `download/rapport-cw-task7-bloc.md` (réserve D002, clôturée Task 8) — puis exécuter le bootstrap canonique AVANT toute action. Lignée : clone mise-en-page (Tasks 1-4) → clone task5-kps2 (Task 5) → clone task7-photo-gif (Tasks 6-7) → présent clone (Task 8, clôture photo-GIF).

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = Tasks 6-8, chacune ≥ 1 ligne ; Tasks 1-5 référencés) | PASS |
| S3 | Complétude livrables (photo validée + GIF en attente décrits avec paramètres, QC, preuves) | PASS |
| S4 | Complétude décisions (4 décisions avec contexte/conséquence) | PASS |
| S5 | Complétude bugs (D002 cause→lecture→clôture tracée ; réserves hors sandbox explicitées) | PASS |
| S6 | Complétude drifts (§3.5 : 3 drifts typés avant/après/session/raison) | PASS |
| S7 | Exécutabilité (§4 : prochaine itération GIF conditionnée, vérificateurs à froid, chaîne héritière, pendants) | PASS |
| S8 | Auto-clonage (§5 croissance + lignée 4 clones + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — aucun PAT ni jeton manipulé cette fenêtre).

(Étape 7 — Sauvegarde : présent fichier `download/clone-session-web-220878ed-20261124-cloture-photo-gif.md`, enregistrement au worklog Task 8.)
