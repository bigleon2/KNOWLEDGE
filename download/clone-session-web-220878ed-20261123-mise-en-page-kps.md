# Clone de discussion — session web-220878ed : optimisation éditoriale documents KPS + skill mise-en-page

> **Auto-clonage** : ce document est auto-suffisant — une session héritière peut reprendre le contexte sans fichier externe (règle zéro : les fichiers des sessions précédentes n'existent pas dans une nouvelle session, tout se reconstruit depuis la lignée). Généré le 2026-11-23 · gen-plan v3.43.0 / correct-work v2.11.0 / clone-chat v2.0.2 · PM-INSTALL v1.10.0 · propriétaire : Kubota (Farm Machinery Europe) — projet standards d'assemblage KPS.

## §0 — Contexte Système (SHARED v1.7.40)

Écosystème Knowledge : SKILLS_ROOT=skills/ | KB_PATH=skills/KNOWLEDGE.md | 55 entrées KB versionnées + collections @ · dépôt git local miroir `/home/z/my-project/KNOWLEDGE-repo` (github.com/bigleon2/KNOWLEDGE, pin a5daa964 — descendant-tolérant du pin pipeline a14f750) · conventions : kebab-case, semver, #token, français exclusif (règle d'or n°6) · référence canonique « mon skill X » = forme installée `skills/X/SKILL.md`, jamais le PM du corpus · KO-L009 : 0 jeton manipulé · R2 anti-rétrogradation · R4 une information une source · arbres : bootstrap canonique `scripts/bootstrap-ecosysteme.py` (entrée consolidée PM-INSTALL §3.2-c), certification 6 arbitres, garde É1-INSTALL · wipe inter-sessions = cas documenté (7ᵉ recyclage absorbé cette session — ré-exécuter le bootstrap).

## §1 — Worklog chronologique (fenêtre du clone : Tasks 1-4)

| Task | Date | Faits saillants |
|---|---|---|
| 1 | 2026-11-22/23 | Directive : installer l'écosystème personnel via PM-INSTALL (pin GitHub a5daa964) → clone au chemin canonique `KNOWLEDGE-repo` · voie (a) exécutant canonique `scripts/eco_install_pipeline.py` : corpus 9 PMs, 56 formes installées (gen-plan v3.43.0, correct-work v2.11.0, clone-chat v2.0.2, disciplines, alias-eco, collections @), outillage 376 scripts, archive rescellée v2.3, manifeste 114/114, post-install 55 SHA 0 divergence, garde R2 0 rétrogradation · bootstrap consolidé **INSTALLE** (certification ALL-PASS 6/6) après corrections E12-E13 : 6 en-têtes §0 STALE alignés (asr/llm/tts/vlm 1.7.44→1.7.40, rea-analysis 1.7.43→1.7.40, mise-en-page 1.7.8→1.7.40), doublon download/README.md supprimé, worklog créé · wipe inter-sessions intermédiaire absorbé par re-bootstrap |
| 2 | 2026-11-23 | gen-plan(step) : reprise du contexte (dernier clone lignée = clone-chat-session-web-ecef7f80-20261119-task108.md, 21ᵉ) + fin de discussion → plan `download/plan-task2-mise-en-page.md` (8 groupes G1-G8, answer key D001-D008, E8 PASS horodaté, PLAN-AFFICHE, fenêtre native TodoWrite) |
| 3 | 2026-11-23 | Exécution G1-G7 : audit documents (61 orphelines/67 sans keepNext) → recherche web méthodes (3 sources notées, API docx-js vérifiée) → skill mise-en-page v1.0.0 consolidé → tests (8/8 self-tests, perf ×12-33 sous seuils, idempotence ×3) → illustrations web (55 candidats, 4 rounds, scoring S1-S5 + VLM → 5 validées, 10 rejets documentés) → clones optimisés (générateur v2 DA-5 chaîné + boucle de convergence 2 passes + sommaire refolié → **arbitre PASS 6/6**, 104 pages) → correct-work (projet) -- bloc **PASS 9/9** |
| 4 | 2026-11-23 | Présent clone (archivage) — 8 checks de validation |

Chaque Task a son entrée intégrale au `worklog.md` (source de vérité — format SHARED §1.4) ; le présent tableau est la vue chronologique exigée par clone-chat Étape 1.

## §2 — Artefacts de la fenêtre (Étape 2)

| Catégorie | Fichiers |
|---|---|
| Plan | `download/plan-task2-mise-en-page.md` (G1-G8, answer key D001-D008 — D001-D007 PASS, D008 PASS à la clôture) |
| Rapports | `download/rapport-audit-mise-en-page.md` (G1) · `download/rapport-tests-mise-en-page.md` (G4) · `download/rapport-g6-clones-optimises.md` (G6) · `download/rapport-cw-task2-bloc.md` (G7 — 9/9 blocs PASS) |
| Livrable propriétaire | **`download/Manuel-KPS-Premium-optimise.docx`** (690 Ko, 104 p.) + **`download/Manuel-KPS-Premium-optimise.pdf`** (1,77 Mo) — version finale qualité expert magazine · originaux `Manuel-KPS-Premium.docx/.pdf` INTACTS (D002) |
| Illustrations | `download/illustrations-kps/` — 5 fichiers validés (muda_1, takt_4, kaizen_1, pdca_5, 5s_1) + `manifeste.json` (55 candidats scannés, 10 rejets VLM, DPI effectif 271-566) |
| Skill | `skills/mise-en-page/` v1.0.0 — SKILL.md (modes M1-M4, règles DA-1..DA-8, gardes-fous), references/ (méthode DA + maths recalibrées), scripts/ (audit_mise_en_page.py, integration_illustrations.py — self-tests embarqués), evals/ |
| Scripts session | `scripts/generate_manuel_kps_v2.js` (générateur cloné DA) · `scripts/calculer_sauts.py` (sauts ciblés occurrence-désambiguïsés) · `scripts/injecter_toc_cache.py` (reconstruction cache TOC + gardes) · `scripts/orchestrer_illustrations_m4.py` · `scripts/finaliser_manifeste_illustrations.py` · `scripts/patch_plan_task2.py` · `scripts/breaks-manuel.json` (9 sauts consignés) · `scripts/test_keep_chaine.js` (expérience LO) |
| Infrastructure | `KNOWLEDGE-repo/` (clone pin a5daa964) · worklog.md (5 Task IDs) · `download/bootstrap-ecosysteme-rapport.json` |
| Clôture | présent clone + worklog Task 4 |

## §3 — Décisions, bugs, conventions (Étape 3)

**Décisions propriétaire (directives)** : (D-220878-1) installer l'écosystème via le PM INSTALL au pin URL GitHub puis mobiliser gen-plan fraîchement installé pour le plan ; (D-220878-2) optimiser la mise en page des DEUX documents (PDF + DOCX) sur des CLONES (originaux intacts, pages ajoutées autorisées) ; (D-220878-3) règle : titres chapitres/paragraphes avec ≥ 5 lignes de leur contenu sur la même page, titres ni italiques ni soulignés ; (D-220878-4) chercher sur le web un skill/méthode de pagination puis faire un skill « mise-en-page » au rôle des experts en conception graphique magazine et DA éditoriale, orchestrateur décisionnaire des recherches web (pertinence/cohérence/adaptabilité + mathématiques) ; (D-220878-5) générer + tester le skill puis corriger/optimiser ; (D-220878-6) chercher des illustrations de taille cohérente (compréhension novice + exemples de normalisation KPS) ; (D-220878-7) version finale du Manuel-KPS-Premium.docx qualité expert ; (D-220878-8) clôture : correct-work (projet) -- bloc puis clone-chat.

**Décisions d'exécution** : installation par la voie (a) (formes certifiées du dépôt — règle d'or n°4 : clone local, jamais raw/API) ; travail KPS sur le générateur docx npm existant (reproductible — D005) plutôt que patch binaire ; politique éditoriale : parties (h1) et annexes en pages neuves, chapitres en flux dense (magazine) ; boucle M3→M2 pour les résidus moteur (sauts ciblés plutôt que combattre les bugs LO keep-with-next) ; calibration conservatrice de l'estimation de lignes (garantir ≥ 5 RÉELLES) ; classification honnête « section courte complète » (WARN) pour les rubriques < 5 lignes de contenu total ; réutilisation de la charte CM-2 et de la structure 3 sections de l'original (contenu inchangé — mise en page seule).

**Bugs corrigés (cause → fix → résultat)** :
1. **Écrasement de définition JS** : `bulletItem` défini deux fois dans le générateur v2 (brut hérité + descripteur nouveau) — la dernière déclaration gagnait → descripteurs sans `build` → TypeError. Fix : doublon supprimé. Résultat : génération OK (idempotence de la cause vérifiée).
2. **Calibration de l'estimation de lignes** : 75 car./ligne surestimait la densité réelle (82-85 mesurées sur Times 12 pt justifié) → « 5 lignes estimées » = 4 réelles → orphelins résiduels. Fix : 90/80 conservateur + recalibration documentée au référentiel du skill (F6). Résultat : garantie ≥ 5 réelles (0 orpheline finale).
3. **Chaînes keepNext non honorées par LibreOffice** (bugs LO connus keep-with-next sur chaînes longues/listes) → titres résiduels en bas de page malgré un XML correct. Fix : boucle M3→M2 — l'arbitre détecte les orphelines au rendu, `calculer_sauts.py` désambiguïse par occurrence, détecte le contexte (rubrique proche d'un titre → sauter le TITRE), élage les conflits ; le générateur pose des `pageBreakBefore` ciblés. Résultat : PASS (0 orpheline) atteint en 2 passes de convergence.
4. **Mesure R2 masquée par le folio** : le pied de page étendait le span de remplissage → pages creuses invisibles. Fix (F4) : zone pied exclue + zone en-tête exclue du calcul de section (F5). Résultat : R2 fiable.
5. **Sommaire sans numéros** : le cache du champ TOC du clone régénéré était vide (LibreOffice rend le cache sans mise à jour) — et la 1ʳᵉ injection a corrompu le XML (coupe hors bornes SDT, runs Word morcelés). Fix : `injecter_toc_cache.py` v2 — région = bloc `<w:sdt>` entier, entrées régénérées depuis les titres DOCX (libellés complets) + folios PDF, gardes de validation (ET.parse + python-docx + conversion test) avant engagement, double passe de convergence. Résultat : sommaire folié correct (67 entrées), audit toujours PASS.
6. **Wipe inter-sessions** (7ᵉ recyclage) : gen-plan/correct-work/KNOWLEDGE.md disparus entre deux messages, en-têtes §0 régressés. Fix : re-bootstrap canonique (INSTALLE) + ré-alignement des 5 en-têtes. Résultat : certification ALL-PASS 6/6 restaurée ; leçon opérationnelle : re-vérifier les artefacts critiques après chaque recyclage.

**Conventions établies/réaffirmées** : toute génération documentaire « soignée » charge mise-en-page (M2 règles + M4 maths + M3 arbitre = juge de livraison) ; la boucle M3→M2 (arbitre détecte → générateur corrige) est le protocole de correction de mise en page ; une section courte entièrement présente sous son titre satisfait l'intent de la règle ≥5 lignes (WARN, pas FAIL) ; les illustrations web passent TOUJOURS par scoring M4 + contrôle VLM + relances affinées (jamais d'insertion directe) ; toute écriture de fichier structuré passe par des gardes de validation avant engagement.

## §3.5 — Context Drift (Étape 3.5)

| Type | Avant → Après | Réf. |
|---|---|---|
| CRÉATION | pas de skill DA dédié → `skills/mise-en-page/` v1.0.0 (méthode + maths + arbitre + orchestrateur) consolidé, self-testé, amélioré en vol (F4-F6) | Task 3, G3 |
| MODIFICATION | documents KPS orphelinés (61 titres isolés) → clones optimisés 104 p. arbitre PASS 6/6, sommaire refolié, 5 figures légendées — originaux byte-intacts | Task 3, G6 |
| DÉGRADATION EXTERNE | 7ᵉ recyclage sandbox (wipe gen-plan/correct-work/KB) → auto-réparé par l'entrée canonique (bootstrap INSTALLE ×2) | Task 1, §0 |
| ENRICHISSEMENT | recherche illustration naïve → protocole orchestrateur (scoring M4 + VLM + relances affinées + maths de place) réutilisable pour tout document | Task 3, G5 |
| RECALIBRAGE | estimation de lignes théorique (75) → calibrée au rendu réel (90/80 conservateur, mesuré 82-85) | Task 3, G6 (F6) |

## §4 — Spécifications techniques (Étape 4 — fichiers prioritaires)

1. **`skills/mise-en-page/SKILL.md`** (v1.0.0, ~15 Ko) — 4 modes : M1 CONCEVOIR (design amont), M2 APPLIQUER (règles pendant génération), M3 AUDITER (arbitre mécanique — juge de livraison), M4 ORCHESTRER (décisionnaire des recherches web). Règles DA-1..DA-8 (hiérarchie sans italique/souligné, échelle modulaire 1,25, rythme vertical 2:1-3:1, keepNext, règle des N lignes, veuves ≥ 2, pages ≥ 25 %, illustration = bloc titré). Scripts : `audit_mise_en_page.py` (R1-R6 + self-test), `integration_illustrations.py` (scoring S1-S5 + maths de place + self-test). Interactions : docx, pdf, pptx, image-search, web-search, VLM, charts, gen-plan, correct-work, knowledge-observer, pm-skill, skills-inventory. Réserves : entrée KB différée (GO propriétaire) ; heuristique titre PDF à calibrer par document.
2. **`scripts/generate_manuel_kps_v2.js`** (~580 l.) — générateur cloné avec couche DA : composants descripteurs (h1/h2/body/bullet/fig/table — construits APRÈS chaînage), `chainer()` (DA-5 : titres traversés, contenu chaîné jusqu'à ≥ 5 lignes estimées, fig/table stoppeurs insécables), figures légendées (ImageRun + légende italique + crédit), sauts ciblés par `breaks-manuel.json` (texte+occurrence), Heading 4 non italique. Reproduire : `node scripts/generate_manuel_kps_v2.js` → `soffice --headless --convert-to pdf` → `python3 skills/mise-en-page/scripts/audit_mise_en_page.py --pdf … --docx …` (PASS attendu).
3. **`scripts/calculer_sauts.py`** — arbitre → breaks : mapping (page, y, texte) → occurrence PDF ; flux DOCX (h1/h2 par style, rub = runs gras courts) ; règle de contexte (rubrique ≤ 2 blocs après un titre → sauter le titre) ; élagage anti-conflit ; `--accumulate` pour stabiliser entre rounds. Boucle : audit → calculer_sauts → générateur → conversion → audit, ARRÊT AU PASS (leçon : ne jamais écraser des breaks qui ont produit un PASS).
4. **`scripts/injecter_toc_cache.py`** — reconstruction du cache TOC : région = bloc `<w:sdt>` entier ; entrées = titres DOCX (complets) × folios PDF (offset = page de « Partie I » − 1) ; gardes XML+python-docx ; double passe de convergence (le sommaire recomposé change de hauteur → re-mesurer).
5. **Chaîne de session héritière** : bootstrap canonique en OUVERTURE → gen-plan(step) pour toute directive → arbitres avant livraison → correct-work (projet) -- bloc → clone-chat. Pour re-mettre en page un document : G1 audit → corrections générateur → boucle jusqu'à PASS → injection TOC → re-audit.

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone — les sections §1-§3 sont ENRICHIES par le clone du tour, les sections §0/§4-§5 sont RÉGÉNÉRÉES (état courant du système). clone-chat référencé (skill v2.0.2, déclencheurs §A). La session héritière reprend : lire le présent clone + `worklog.md` (Tasks 1-4) + `download/plan-task2-mise-en-page.md` (answer key fait foi) + `download/rapport-cw-task2-bloc.md` (réserves) — puis exécuter le bootstrap canonique AVANT toute action. Pendants connus : (a) inscription du skill mise-en-page au registre KB à la prochaine poussée dépôt (GO propriétaire — R2) ; (b) révocation de l'ancien PAT (tâche P1 du clone Task 108 — toujours ouverte côté propriétaire).

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = Tasks 1-4, chacune ≥ 1 ligne) | PASS |
| S3 | Complétude skills (mise-en-page décrit avec version, specs, relations) | PASS |
| S4 | Complétude décisions (8 décisions propriétaire + exécution avec contexte/conséquence) | PASS |
| S5 | Complétude bugs (6 bugs : cause + fix + résultat vérifié) | PASS |
| S6 | Complétude drifts (5 drifts typés, avant/après explicites) | PASS |
| S7 | Exécutabilité (§4 instructions claires + chaîne héritière + fichiers prioritaires) | PASS |
| S8 | Auto-clonage (§5 croissance + clone-chat référencé + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — aucun PAT ni jeton manipulé cette session).

(Étape 7 — Sauvegarde : présent fichier `download/clone-session-web-220878ed-20261123-mise-en-page-kps.md`, enregistrement au worklog Task 4.)
