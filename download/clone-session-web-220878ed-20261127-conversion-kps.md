# CLONE DE DISCUSSION — Conversion « standard non-KPS » → « standard version KPS » (fenêtre Tasks 9-10)

> **Date du clone** : 2026-11-27
> **Source** : Discussion entre le propriétaire et l'assistant (session web-220878ed-c362-40f9-b12a-5aa08335c14d)
> **Sessions couvertes** : 2 fenêtres (Task 9 du 2026-11-27 + Task 10 du 2026-11-27)
> **Version clone-chat** : 2.0.2

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : sandbox Linux recyclable (`/home/z/my-project/` persiste, les processus non) ;
écosystème Knowledge personnel installé au pin 38573b0 (descendant-tolérant de a5daa964, KO-L009 — fetch
anonyme sans jeton) ; gen-plan v3.47.0, correct-work v2.12.1, clone-chat v2.0.2, mise-en-page §0 v1.7.45 ;
SHARED v1.7.45 ; fuseau propriétaire Europe/Paris ; KPS = **Kubota Production System** exclusivement
(jamais Kawasaki/Volkswagen — PM KPS-2 §0).

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.0 Héritage — chaîne de clonage (4 clones cumulés, Tasks 1-8, 2026-11-22 → 2026-11-24)

La lignée de clones cumule les fenêtres Tasks 1-4 (installation écosystème + manuel KPS + skill
mise-en-page), Task 5 (app convertisseur kps-converter + audit GIF), Tasks 6-7 (photos groupe + GIF),
Task 8 (clôture photo-GIF, D002 clôturée $FACON). Détails aux §1.0 des clones prédécesseurs
(`download/clone-session-web-220878ed-20261123-mise-en-page-kps.md`,
`clone-session-web-220878ed-20261123-task5-kps2.md`,
`clone-session-web-220878ed-20261123-task7-photo-gif.md`,
`clone-session-web-220878ed-20261124-cloture-photo-gif.md`). La présente session ajoute 2 entrées
worklog (Tasks 9-10). État de départ connu : clôture Task 8 (photo PA-GROUPE-004 validée, mouvement
GIF différé en attente de description).

### §1.1 Résumé global

Fenêtre Task 9 : réinstallation de l'écosystème au nouveau pin 38573b0 (bootstrap canonique, boucle
E12-E13 sur 7 en-têtes §0, re-certification ALL PASS 6/6) puis résumé PDF blue-tech du fonctionnement
du full stack kps-converter (12 pages, arbitres PASS, CW projet 21/21). Fenêtre Task 10 (directive
gen-plan(step) du 2026-11-27) : analyse de la photo `IMG_20261127_131943.jpg` (le standard non-KPS
MO-MF-013-F « Sous assemblage du tank fuel », TA-S-3055-020, rév. D), conversion en « standard version
KPS » (fiche KPS Standardized Work A4 paysage 2 pages, seed §4 = source canonique, audit 40 % → 100 %)
avec garde byte-identique de l'original, correct-work sur la conversion (10/10), résumé illustré PDF de
la conversion mis en page avec le skill mise-en-page (8 pages, 6 figures, blue-tech, M3 PASS, CW
projet 10/10), et clonage (présent document).

### §1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | 2026-11-27 | Task 9 — pin 38573b0 + résumé blue-tech du full stack | `resume-fullstack-kps-converter-bluetech.pdf` (12 p.), plan-task9, rapport-cw-task9-bloc.md, 3 schémas PNG |
| 2 | 2026-11-27 | Task 10 — conversion KPS du standard photo + résumé illustré | fiche KPS (2 p.), extraction JSON, garde byte-identique, résumé illustré (8 p.), rapports CW ×2, 9 crops, présent clone |

### §1.3 Détail par session

**Task 9 (2026-11-27)** : bootstrap canonique PM-INSTALL §3.2-c (fetch anonyme, pin 38573b0 =
descendant de a5daa964, reset --hard d'une dérive 2770 fichiers) ; boucle E12-E13 : réinstallation de
version-management + ré-alignement de 7 en-têtes §0 (asr/llm/tts/vlm/mise-en-page/add-template-pdf ≠
SHARED v1.7.45) ; re-certification ALL PASS 6/6 ; gen-plan v3.43.0 → v3.47.0. G1-G4 : registre
templates/registry.json amorcé au profil (absent du pin), template blue-tech installé, 3 schémas
Playwright+CSS, PDF creative-flow 12 pages (boucle de convergence : cover_validate Pass 1, 5 pages
creuses densifiées), CW projet --bloc 21/21. Détail : worklog Task 9 + rapport-cw-task9-bloc.md.

**Task 10 (2026-11-27)** : G0 lecture des référentiels (pdf SKILL.md + brief creative-flow + overflow +
maths-integration + méthode DA) ; G1 analyse du standard non-KPS : lecture visuelle complète de la
photo (cartouche, 4 révisions A-D, nomenclature 7 pièces, 5 opérations, couples 13 Nm/10 Nm,
check sheet « Pré. »), extraction structurée JSON avec audit C1-C10 de la source = **40 %**, 9 crops
illustratifs + planche de contrôle (1 ajustement de crop) ; G2 conversion : fiche KPS Standardized Work
A4 paysage 2 pages (palette PM §6, chiffres cerclés CSS, photos recadrées de la source, jauge
Cycle/Takt 96 %), valeurs canoniques du seed §4 (Takt 150 s démonstration, SWIP 1, temps
57/36/14/27/10 = 144 s), garde de l'original (copie byte-identique sha256 3d4d5109847d9f51…) ;
G3 arbitres : poster_validate 0 erreur, pdf_qa PASS (après meta.brand), inspection visuelle 2/2 ;
G4 correct-work (conversion) : 10/10 PASS ; G5 résumé illustré creative-flow blue-tech 8 pages
(6 figures légendées, table d'audit source 40 %, mapping donnée par donnée, vignettes de la fiche,
preuves, réserves), mise-en-page M2 + M3 **PASS**, pdf_qa PASS, folios du sommaire vérifiés
mécaniquement ; G6 correct-work (projet) : 10/10 PASS ; G7 clone (présent fichier) ; G8 worklog.

---

## §2 — ÉCOSYSTÈME DE SKILLS

### §2.1 Skills créés ou modifiés

Aucun skill créé ni modifié dans cette fenêtre (conformité R4 — les formes installées du pin 38573b0
sont consommées telles quelles). Skills consommés : gen-plan v3.47.0 (mode step), correct-work
v2.12.1 (bloc + projet), pdf (creative-flow, html2pdf-next.js --nopaged, poster_validate, pdf_qa,
meta.brand), mise-en-page v1.x (M2 règles DA-1..DA-8 + M3 audit_mise_en_page.py), VLM (lecture
photo), clone-chat v2.0.2.

### §2.2 Scripts créés ou modifiés

#### task10-crops-source.py
- **Description** : découpe idempotente des 9 illustrations du standard non-KPS photographié + copie
  d'archive byte-identique + planche de contact de contrôle.
- **Chemin** : `scripts/task10-crops-source.py` (~100 lignes)

#### task10-build-fiche.py
- **Description** : générateur HTML de la fiche KPS Standardized Work (2 feuilles A4 paysage,
  palette PM §6, chiffres cerclés CSS, révisions A-D intégrées, jauge Cycle/Takt 96 %).
- **Chemin** : `scripts/task10-build-fiche.py` (~380 lignes)

#### task10-build-resume.py
- **Description** : générateur HTML du résumé illustré (creative-flow blue-tech 8 pages : cover, sommaire
  à folios réels, 6 sections, 6 figures légendées, 3 tables, ending) — règles DA appliquées (M2).
- **Chemin** : `scripts/task10-build-resume.py` (~370 lignes)

#### verifier_cw_task10_conversion.py / verifier_cw_task10_projet.py
- **Description** : vérificateurs mécaniques correct-work (10 contrôles C01-C10 conversion ; 10 contrôles
  P01-P10 projet : folios réels, M3, garde byte-identique, inventaire, KO-L009).
- **Sorties** : `scripts/cw-task10-conversion-report.json`, `scripts/cw-task10-projet-report.json`

### §2.3 Artefacts produits

| Fichier | Taille | Description |
|---------|--------|-------------|
| `download/fiche-kps-standardized-work-TA-S-3055-020.pdf` | 2,4 Mo | la conversion : fiche KPS Standardized Work, 2 p. A4 paysage, vectoriel |
| `download/resume-conversion-kps-bluetech.pdf` | ~6 Mo | résumé illustré de la conversion, 8 p., 6 figures |
| `download/resume-conversion-kps-bluetech.html` + `download/assets-resume-task10/` | HTML + 12 img | source HTML du résumé (chemins réécrits) |
| `download/extraction-standard-non-KPS-MO-MF-013-F.json` | ~9 Ko | analyse structurée de la source (audit 40 %, hypothèses tracées) |
| `download/source-standard-non-KPS-MO-MF-013-F.jpg` | 2,3 Mo | garde du standard non-KPS (byte-identique à upload/, sha256 3d4d5109…) |
| `download/rapport-cw-task10-conversion.md` / `rapport-cw-task10-projet.md` | — | rapports correct-work (bloc + projet) |
| `assets_tmp/task10-crops/` (9 PNG + planche + rapport JSON) | — | illustrations recadrées du standard source |
| `scripts/cw-task10-*-report.json`, `assets_tmp/task10/audit-m3.json` | — | preuves mécaniques |
| Task 9 : `download/resume-fullstack-kps-converter-bluetech.pdf` (12 p.) + HTML + 3 schémas + plan + CW | — | livrables Task 9 déjà scellés |

### §2.4 Historique des interactions

| Ordre | Skill/outil | Usage | Résultat |
|---|---|---|---|
| 1 | bootstrap-ecosysteme.py (Task 9) | pin 38573b0, reset dérive, boucle E12-E13 | INSTALLE, ALL PASS 6/6 |
| 2 | gen-plan v3.47.0 (mode step) | plan Task 9 puis exécution directe Task 10 | PLAN-AFFICHE / étapes enchaînées |
| 3 | VLM + lecture directe photo | extraction du contenu MO-MF-013-F | extraction JSON complète |
| 4 | pdf (html2pdf-next.js --nopaged + arbitres) | fiche 2 p. puis résumé 8 p. | 2 PDF vectoriels, pdf_qa PASS ×2 |
| 5 | mise-en-page (M2 + M3) | règles DA pendant génération + audit post-rendu | audit-m3.json **PASS** |
| 6 | correct-work v2.12.1 (bloc, puis projet) | 2 vérifications comme demandé | 10/10 + 10/10 PASS |
| 7 | clone-chat v2.0.2 | présent clone | 8/8 PASS |

---

## §3 — DÉCISIONS CLÉS

### §3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | Analyser la photo comme « standard non KPS », la convertir en « standard version KPS », **garder le standard non-KPS** | directive gen-plan(step) du 2026-11-27 | l'original n'est jamais altéré : copie d'archive byte-identique livrée + upload/ intact |
| 2 | Résumé illustré PDF de la conversion **avec le skill mise-en-page** | même directive | pipeline creative-flow + M2/M3 (audit PASS) au lieu d'un simple export |
| 3 | Deux correct-work (après conversion, puis projet) puis clone-chat | même directive | chaîne d'arbitrage exécutée dans cet ordre exact |
| 4 | KPS = Kubota Production System (décision Task 5, réaffirmée) | PM KPS-2 §0 interdit l'amalgame Kawasaki/VW | la conversion cible la fiche Standardized Work du projet (fusion 3 feuilles + dossier de poste) |

### §3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | crop `localisation-tank` avec bande de fond hors photo | fraction droite 0,558 trop large | coupe à 0,545, re-génération idempotente | crop propre (planche de contrôle) |
| 2 | fiche p.1 : blanc ~40 % sous la nomenclature | panneau plus haut que le contenu | table « Historique des révisions » A-D intégrée (contenu réel) | page 1 équilibrée |
| 3 | fiche p.2 : vide ~100 px avant la jauge | lignes d'opération à hauteur fixe | `.op { flex:1 }` — répartition sur toute la hauteur | page 2 pleine |
| 4 | C07 FAIL (audit fiche) : libellés « SWIP », « POINT CLÉ » introuvables | `letter-spacing` CSS fait insérer des espaces par l'extracteur PDF (« S W I P ») — mauvais prédicteur du vérificateur, rendu correct | contrôles sur texte aplati sans espaces + NFC (livrable intact) | 10/10 PASS |
| 5 | cover_validate Pass 1 : 8 chevauchements texte↔ligne | les divs `.rule` (2 px) classés lignes décoratives (seuil ~40 px, arbitre « ONLY for cover pages » appliqué au document entier) | règles remplacées par `border-bottom` portés par les titres | Pass 1 = 0 erreur |
| 6 | pdf_qa : 2 tirets cadratins en début de ligne (p. 6) | retour à la ligne devant « — » | insécables ` ` avant les tirets | warning disparu |
| 7 | pdf_qa : page 7 creuse (36 % < 40 %) | §6 trop courte | table « Inventaire des livrables du Task 10 » (contenu réel) | fill ratio OK |
| 8 | folios du sommaire faux (3,3,5,6,8,9) | estimation avant rendu | corrigés au rendu réel (2,3,4,5,6,6) + vérification mécanique par repères de titres | folios exacts |
| 9 | P02 FAIL : marqueurs « TODO/XXX » détectés dans le résumé | la cellule de preuve citait littéralement les noms des marqueurs (auto-référence) | cellule reformulée, vérificateur inchangé | 10/10 PASS |
| 10 | pagedjs non résolu au rendu | node_modules global effacé par le recyclage du sandbox | voie de repli documentée `--nopaged` (pagination native Chromium) | 2 PDF conformes |

### §3.3 Conventions établies

| Convention | Règle | Exemple |
|---|---|---|
| Fiche KPS imprimable | A4 paysage 1123×794 px, palette PM §6, chiffres cerclés en composant CSS dédié | `scripts/task10-build-fiche.py` |
| Séparateurs de titres | jamais de divs `.rule` (classés lignes par cover_validate) : `border-bottom` porté par le titre | `task10-build-resume.py` |
| Typographie française PDF | insécable avant les tirets cadratins et les % pour interdire tout début de ligne par « — » | cellules de preuve du résumé |
| Folios de sommaire | jamais estimés : corrigés après premier rendu puis revérifiés mécaniquement (repères de titres par page) | verifier P03 |
| Valeurs non présentes dans la source | jamais inventées : reprises du seed §4 avec mention « démonstration » ou tracées comme hypothèses Méthodes | Takt 150 s, temps par étape, flags QG |
| Garde de document source | copie byte-identique dans download/ + sha256 cité dans les livrables | `source-standard-non-KPS-MO-MF-013-F.jpg` |

### §3.4 Données de calibration

- Coûts #token fenêtre : Task 9 ~15k (installation) + ~43k (G1-G4) ; Task 10 ~45k estimés / ~40k réalisés
  (G0-G7, incluant 8+8 lectures d'images de contrôle sous le plafond de 20).
- Audit KPS : source MO-MF-013-F = 4/10 critères = 40 % ; fiche convertie = 10/10 = 100 % ;
  somme temps seed = 57+36+14+27+10 = 144 s ; Takt 150 s ; charge = 96 %.
- Vérificateurs : conversion 10/10, projet 10/10, M3 PASS, pdf_qa PASS ×2, poster_validate 0 erreur (Pass 1).

### §3.5 Évolutions de contexte (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|---|---|---|---|---|---|
| 1 | MODIFICATION | gen-plan v3.43.0 / SHARED v1.7.40 (pin a5daa964) | gen-plan v3.47.0 / SHARED v1.7.45 (pin 38573b0) | Task 9 | Task 9, E12-E13 | réinstallation demandée au nouveau pin |
| 2 | ENRICHISSEMENT | la conversion MO-MF-013-F n'existait qu'en données seed (app) | matérialisée en fiche KPS imprimable + résumé illustré | Task 10 | Task 10, G2/G5 | directive propriétaire « convertir (garde du standard non-KPS) » |
| 3 | CORRECTION | folios du sommaire estimés avant rendu | folios réels vérifiés mécaniquement | Task 10 | Task 10, G5 (finding 5) | leçon Task 2 réappliquée |
| 4 | MODIFICATION | pagedjs requis pour html2pdf-next.js | `--nopaged` = voie par défaut de la fenêtre (pagedjs non résolu) | Task 9-10 | Task 10, §3.2-10 | node_modules global éffacé au recyclage |

---

## §4 — INSTRUCTIONS D'UTILISATION (Étape 4)

1. **Chaîne de session héritière** : bootstrap canonique en OUVERTURE (après tout reset : re-vérifier les
   en-têtes §0 + download/README.md) → gen-plan(step) pour toute directive → arbitres avant livraison →
   correct-work → clone-chat.
2. **Vérificateurs à froid** : `python3 scripts/verifier_cw_task10_conversion.py`,
   `python3 scripts/verifier_cw_task10_projet.py`, `python3 scripts/verifier_cw_task9.py`,
   audit M3 : `python3 skills/mise-en-page/scripts/audit_mise_en_page.py --pdf
   download/resume-conversion-kps-bluetech.pdf --min-lines 5 --skip-pages 1`.
3. **Hypothèses à faire valider par le service Méthodes** (bloquantes pour un usage production, tracées
   au résumé §6 et à l'extraction JSON) : signification des flags QG1/QG2/Pré. ; source du Takt ;
   chronométrages terrain (les temps seed sont de la démonstration) ; nom complet du Vérificateur 2 +
   référence manuscrite 3J09900482.
4. **Pendants ouverts (hérités)** : description du mouvement GIF par le propriétaire (Task 8 — blocant
   pour toute nouvelle animation) ; Docker compose réel sur poste équipé (Task 5) ; vision 501 (Task 5) ;
   entrée KB du skill mise-en-page à la prochaine poussée dépôt + révocation de l'ancien PAT (KO-L009,
   côté propriétaire) ; correctif add_template_pdf.py (SameFileError depot==profil, Task 9).

## §5 — AUTO-CLONAGE (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone — §1-§3 ENRICHIES par le clone du tour,
§0/§4-§5 RÉGÉNÉRÉES (état courant). La session héritière reprend : lire le présent clone + `worklog.md`
(Tasks 1-10) + `download/rapport-cw-task10-projet.md` (preuves de clôture) — puis exécuter le bootstrap
canonique AVANT toute action. Lignée : clone mise-en-page (Tasks 1-4) → clone task5-kps2 (Task 5) →
clone task7-photo-gif (Tasks 6-7) → clone cloture-photo-gif (Task 8) → présent clone (Tasks 9-10).

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X » sans contenu, lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (§1.2 = Tasks 9-10, chacun détaillé §1.3 ; Tasks 1-8 référencés §1.0) | PASS |
| S3 | Complétude livrables (fiche, résumé, extraction, garde, crops, rapports — avec tailles et rôles) | PASS |
| S4 | Complétude décisions (4 décisions avec contexte/conséquence) | PASS |
| S5 | Complétude bugs (10 bugs, chacun cause → fix → résultat vérifié) | PASS |
| S6 | Complétude drifts (§3.5 : 4 drifts typés avant/après/session/raison) | PASS |
| S7 | Exécutabilité (§4 : chaîne héritière, vérificateurs à froid, hypothèses Méthodes, pendants) | PASS |
| S8 | Auto-clonage (§5 croissance + lignée 5 clones + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — aucun PAT ni jeton manipulé cette fenêtre).

(Étape 7 — Sauvegarde : présent fichier `download/clone-session-web-220878ed-20261127-conversion-kps.md`, enregistrement au worklog Task 10.)
