# Rapport correct-work — Task 10 (bloc 1) : conversion « standard non-KPS » → « standard version KPS »

## Métadonnées
- **Date** : 2026-11-27
- **Mode** : vérification de bloc (conversion) — correct-work v2.12.1
- **Cible** : analyse + conversion du standard photo `IMG_20261127_131943.jpg` (MO-MF-013-F, « Sous assemblage du tank fuel », TA-S-3055-020)

## Étape 1 — Plan d'actions
Directive propriétaire gen-plan(step) du 2026-11-27 : (1) analyse de la photo en tant que « standard non KPS » avec objectif de conversion « standard version KPS » en gardant le standard non-KPS ; (2) correct-work ; (3) résumé illustré PDF de la conversion mis en page avec le skill mise-en-page ; (4) correct-work (projet) ; (5) clone-chat. Exécution en chaînage step (fenêtre Task 10, gen-plan v3.47.0).

## Blocs vérifiés
| Bloc | Étapes couvertes | Findings | Verdict |
|---|---|---|---|
| B1 — Analyse du standard non-KPS | extraction structurée JSON (cartouche, 4 révisions A-D, nomenclature 7, 5 opérations, colonnes check), audit C1-C10 source = 40 %, 9 crops illustratifs + planche de contrôle | 1 (crop localisation — bande de fond à droite) — corrigé (coupe 0,558→0,545), 1 round | **PASS** |
| B2 — Conversion KPS | fiche Standardized Work A4 paysage 2 pages (palette PM §6, valeurs canoniques seed §4), garde de l'original (copie byte-identique sha256 3d4d5109…) | 2 (blanc panneau nomenclature p.1 ; vide avant jauge p.2) — corrigés (table révisions A-D intégrée ; flex:1 sur les 5 opérations), 1 round | **PASS** |
| B3 — Arbitres de la fiche | poster_validate 0 erreur · pdf_qa PASS (après meta.brand) · inspection visuelle 2/2 pages · 0 U+FFFD · 0 placeholder | 1 (métadonnée auteur manquante) — corrigée (meta.brand) | **PASS** |

**Verdict du bloc : PASS** — vérification mécanique `scripts/verifier_cw_task10_conversion.py` : **10/10 PASS** (`scripts/cw-task10-conversion-report.json`).

## Étape 2 — Erreurs et omissions (toutes corrigées, re-vérifiées)
| # | Sévérité | Description | Emplacement | Correction appliquée |
|---|----------|-------------|-------------|---------------------|
| 1 | S3 | crop `localisation-tank` capte une bande de fond hors photo centrale | scripts/task10-crops-source.py | fraction droite 0,558→0,545, re-génération idempotente |
| 2 | S2 | panneau nomenclature p.1 : blanc terminal ~40 % | fiche HTML | table « Historique des révisions » A-D intégrée sous la nomenclature (contenu réel du cartouche source) |
| 3 | S2 | page 2 : vide ~100 px entre les opérations et la jauge | fiche HTML | `.op { flex:1 }` — les 5 opérations se répartissent toute la hauteur utile |
| 4 | S3 | métadonnée auteur manquante (pdf_qa WARN) | PDF fiche | `meta.brand` appliqué → pdf_qa **PASS** |
| 5 | S2 | mauvais prédicteur du vérificateur C07 : l'extracteur PDF insère des espaces dans les libellés à `letter-spacing` (« S W I P ») — livrable intact, rendu correct (confirmé visuellement) | scripts/verifier_cw_task10_conversion.py | contrôles de libellés passés sur texte aplati (sans espaces, NFC) → 10/10 PASS |

## Étape 3 — Structure et conflits
| # | Type | Description | Résolution |
|---|------|-------------|------------|
| 1 | Choix de source | l'op. 2 imprimée dit « Assembler ③ JOINT dans ④ HOSE… » alors que « JOINT » n'existe pas dans la nomenclature ; annotation manuscrite « → 3J09900482 » | lecture canonique déjà validée Task 5 (seed §4) : ⑤ JOINT PIPE dans ③ HOSE avec ④ CLAMP — R4 : une information une source ; l'ambiguïté est tracée à l'extraction JSON et au résumé |
| 2 | Interdiction d'invention | temps, Takt, SWIP, règle d'anomalie absents du standard source | repris du seed §4 « valeurs de démonstration réalistes » avec mention explicite « à remplacer par chronométrage terrain » — aucune valeur inventée |

## Étape 4 — Interactions
| # | Skill A | Skill B | Type | Statut |
|---|---|---|---|---|
| 1 | pdf | mise-en-page | couche DA au-dessus du générateur (M2 appliquée, M3 réservé au résumé) | ✅ |
| 2 | VLM (lecture photo) | pdf | amont (extraction de contenu → fiche) | ✅ |
| 3 | gen-plan v3.47.0 | correct-work v2.12.1 | plan obligatoire (directive step) | ✅ |
| 4 | PM KPS-2 (seed §4) | pdf | source canonique des valeurs de conversion | ✅ |

## Réserves
- Flags QG1/QG2/Pré. : convention qualité du site à confirmer par Méthodes (hypothèse PM §0 — jamais inventée).
- Temps/Takt : valeurs de démonstration du seed — chronométrages terrain requis avant usage production.
- Nom complet du Vérificateur 2 (« Kazumi D. Fukushima », tronqué sur la photo) et référence manuscrite 3J09900482 : à confirmer.

## Résumé
- Livrables du bloc : `download/fiche-kps-standardized-work-TA-S-3055-020.pdf` (2 p. A4 paysage, vectoriel) · `download/extraction-standard-non-KPS-MO-MF-013-F.json` · `download/source-standard-non-KPS-MO-MF-013-F.jpg` (garde byte-identique) · 9 crops illustratifs (`assets_tmp/task10-crops/`).
- Preuves : `scripts/cw-task10-conversion-report.json` (10/10 PASS) · poster_validate 0 erreur · pdf_qa PASS · audit C1-C10 fiche = 100 % (mécanique) · somme temps 144 s / Takt 150 s = 96 % · 0 U+FFFD · inspection visuelle 2/2.
