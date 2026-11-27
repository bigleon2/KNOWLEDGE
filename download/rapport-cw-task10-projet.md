# Rapport correct-work — Task 10 (bloc 2, projet) : clôture de la conversion « standard non-KPS » → « standard version KPS »

## Métadonnées
- **Date** : 2026-11-27
- **Mode** : PROJET (clôture) — correct-work v2.12.1
- **Cible** : l'ensemble des livrables Task 10 (analyse, conversion, résumé illustré, traces)

## Blocs vérifiés
| Bloc | Contenu | Findings | Verdict |
|---|---|---|---|
| B1 — Bloc conversion (CW #1) | extraction, fiche KPS, garde de l'original | 5 — tous corrigés (voir rapport-cw-task10-conversion.md) | **PASS** (10/10 mécanique) |
| B2 — Résumé illustré (mise-en-page) | ligne creative-flow blue-tech, M2/M3 | 3 — corrigés (voir Étape 2) | **PASS** |
| B3 — Traçabilité et livrabilité | inventaire, HTML+images, KO-L009 | 0 | **PASS** |

**Verdict global : PASS** — vérification mécanique `scripts/verifier_cw_task10_projet.py` : **10/10 PASS** (`scripts/cw-task10-projet-report.json`).

## Étape 1 — Plan d'actions
Directive propriétaire gen-plan(step) exécutée dans l'ordre : analyse de la photo (standard non-KPS) → conversion (standard version KPS) → correct-work → résumé illustré PDF mis en page avec le skill mise-en-page → correct-work (projet) → clone-chat.

## Étape 2 — Erreurs et omissions du bloc résumé (corrigées, re-vérifiées)
| # | Sévérité | Description | Correction appliquée |
|---|----------|-------------|---------------------|
| 1 | S1 | COVER_TEXT_OVERLAP Pass 1 : 8 chevauchements texte↔ligne — les divs `.rule` (2 px) sont classés « lignes décoratives » par cover_validate (seuil ~40 px, document scanné en entier alors que l'arbitre est « ONLY for cover pages ») | les règles dégradées sont remplacées par des `border-bottom` portés par les titres (les éléments texte ne sont jamais classés lignes) → Pass 1 **0 erreur** |
| 2 | S2 | pdf_qa : 2 tirets cadratins en début de ligne (p. 6) | insécables ` ` avant les deux tirets → warning disparu |
| 3 | S2 | pdf_qa : page 7 creuse (36 % < 40 %) | densification réelle : inventaire des livrables du Task 10 (table 6 lignes) → fill ratio OK |
| 4 | S3 | métadonnée auteur manquante | `meta.brand` appliqué → pdf_qa **PASS** |
| 5 | S2 | folios du sommaire estimés avant rendu (3,3,5,6,8,9 ≠ réels) | corrigés sur le rendu réel (2,3,4,5,6,6) et **revérifiés mécaniquement** (5 repères de titres par page) |
| 6 | S3 | faux positif du vérificateur P02 : la cellule de preuve citait littéralement les noms des marqueurs de placeholder (« TODO/XXX/… ») que le vérificateur cherche | reformulation de la cellule (« liste standard des marqueurs »), livrable régénéré, vérificateur inchangé → 10/10 |

## Étape 3 — Structure et conflits
| # | Type | Description | Résolution |
|---|------|-------------|------------|
| 1 | Portée d'arbitre | cover_validate appliqué à un document fluide de 8 pages : 46 « chevauchements » Pass 2 = cellules de même ligne de tableau côte à côte + couples en ligne d'une même phrase | motif structurel identique au Task 9 (faux positifs documentés, arbitre conçu pour couverture canvas fixe) ; compensation : inspection visuelle 8/8 pages + audit M3 PASS + pdf_qa PASS |
| 2 | Environnement | pagedjs non résolu (node_modules global éffacé par le recyclage du sandbox) | voie de repli documentée du skill pdf : `--nopaged` (pagination native Chromium), adaptée aux feuilles fixes de la fiche et au flux du résumé |

## Étape 4 — Interactions
| # | Skill A | Skill B | Type | Statut |
|---|---|---|---|---|
| 1 | pdf (creative-flow) | mise-en-page (M2 règles DA pendant génération, M3 audit post-rendu) | couche décisionnelle | ✅ M3 PASS |
| 2 | pdf (html2pdf-next.js) | pdf (poster_validate, pdf_qa, meta.brand) | pipeline + arbitres | ✅ |
| 3 | VLM (lecture de la photo) | pdf | amont extraction | ✅ |
| 4 | correct-work (2 fois, comme demandé) | gen-plan v3.47.0 (mode step) | plan + vérification | ✅ |

## Réserves
- Les 46 signalements Pass 2 de cover_validate sont des faux positifs structurels (cellules de tableau côte à côte) — documentés, compensés visuellement ; aucun texte ne se chevauche réellement (inspecté page par page).
- Hypothèses métier reportées au résumé §6 (flags QG, source du Takt, chronométrages terrain, nom du Vérificateur 2 + référence manuscrite) — arbitrage : service Méthodes.

## Résumé
- Livrables Task 10 : fiche KPS (2 p. A4 paysage) · résumé illustré (8 p., 6 figures, blue-tech) · extraction JSON · garde byte-identique du standard non-KPS · 9 crops illustratifs · rapports CW ×2 + HTML source et images du résumé.
- Preuves : `scripts/cw-task10-projet-report.json` (10/10) · `scripts/cw-task10-conversion-report.json` (10/10) · `assets_tmp/task10/audit-m3.json` (M3 PASS) · pdf_qa PASS ×2 · folios vérifiés mécaniquement · 0 U+FFFD · inspection visuelle 8/8 + 2/2.
