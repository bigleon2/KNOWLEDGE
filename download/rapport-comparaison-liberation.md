# Rapport Task 48 — G4/S5 : comparaison côte à côte enrichie des rendus iphone17 / iphone18 / iphone19 pour « libération après guerre »

> gen-plan v3.23.1 mode (step) — groupe G4. Mini-plans persistés AVANT action (règle 3) : `scripts/task48-plan-PA-20261021-007.yaml` + `scripts/task48-plan-directive.yaml`. Composite PIL pur — zéro appel générationnel pour la comparaison, zéro modification des sources (sha256 vérifiés avant/après). **Adapté à la photographie originale de 1944** : panneaux au ratio 3:2 de la source, guide de lecture propre au contenu historique.

## 📋 Demande

« Effectue la même comparaison enrichie que précédemment du rendu de mes skills iphone17, iphone18 et iphone19 pour la photo "libération après guerre" (la réponse à la dernière question de mes skills sera "sans modification, ni retouches"). » — même format que les comparaisons « les copines » (Task 47 D7) et « les potos » (Task 48 G2) : 5 versions + guide de lecture + rapport.

## 🗺️ Plan exécuté

Campagne PA-20261021-007 (test robuste × 3 skills, cf. `rapport-PA-TEST-007.md`) puis composite PIL 2×3 (task48-comparaison-liberation.py) : panneaux 720×480 (ratio 3:2 de la source 828×550 — aucun étirement), légendes dédiées, guide 1944.

## ✅ Résultat QC (structurel — composite déterministe)

| # | Vérification | Verdict |
|---|---|---|
| 1 | Sortie produite : `download/comparaison-liberation-apres-guerre-cote-a-cote.png` — 2208×1084, 6 panneaux 720×480 légendés | OK |
| 2 | Original P0 intact (sha256:5818fa6a…) | OK |
| 3 | Panneau P1-P6 = copie désaturée MÉCANIQUE (PIL L→RGB) de l'intermédiaire 19, étiquetée comme telle + intermédiaire natif conservé | OK |
| 4 | Rendus 17/18/19 intacts (sha256 f74f594e…, 9c3ae84d…, d21b39e4…) | OK |
| 5 | 6/6 panneaux distincts et valides (ratio 3:2 respecté — aucun étirement) | OK |
| 6 | Monochrome des 3 rendus vérifié mécaniquement (saturations 0.16 / 0.10 / 0.48) + QC campagnes 11/11, 12/12, 13/13 | OK |
| 7 | Règle 3 : mini-plans persistés AVANT action | OK |
| 8 | Rejeu idempotent du composite : sources intacts | OK |

**→ 8/8 OK.** QC vision non requis sur le composite : collage déterministe d'artefacts déjà certifiés par leurs QC de campagne.

## 🖼️ Description du livrable

**`download/comparaison-liberation-apres-guerre-cote-a-cote.png`** (2208×1084) — grille 2×3 :

| Haut gauche | Haut centre | Haut droite |
|---|---|---|
| **ORIGINAL** — 828×550, tirage argentique N&B, août 1944 (Libération) : grain marqué, contraste dur, écrêtage du ciel | **AMÉLIORATION TECHNIQUE SEULE** — P1-P6 v0.11.0 (désaturée pour la lecture : tonalité restaurée, taches nettoyées, netteté légère — grain préservé) | **RENDU iPhone 17 Pro Max** — d'époque, Photonic Engine NG (PA-TEST-007-1, QC 11/11) |
| **Bas gauche** | **Bas centre** | **Bas droite** |
| **RENDU iPhone 18 Pro Max** — confirmée, ƒ/4.0 netteté étendue + Styles 3 (PA-TEST-007-2, QC 12/12 après it. 1) | **RENDU iPhone 19 Pro Max v0.11.0** — ANTICIPÉ 2027 + binning R19 « pixels fusionnés » (PA-TEST-007-3, QC 13/13) | **GUIDE DE LECTURE** — ordre de comparaison, repères 1944 (drapeaux en gris, homme casqué, carabine, pousseurs, garçon), restauration ≠ colorisation |

Lecture conseillée : comparer d'abord l'original ↔ amélioration technique (gain pur : tonalité, propreté, netteté — le grain et le monochrome demeurent), puis l'amélioration ↔ les trois rendus générationnels (17 d'époque → 18 confirmée → 19 anticipée + binning : la finition affine à chaque génération, **sans jamais coloriser** — les drapeaux tricolore et américain restent en niveaux de gris, fidélité historique stricte).

## ⚠️ Limites honnêtes

- Panneaux affichés à 720×480 — pour l'inspection fine (visages de la foule, texture du grain, drapeaux), se reporter aux fichiers pleine résolution 1152×768 (`download/PA-TEST-007-{1,2,3}-*.png`).
- Le panneau « amélioration technique » est une **désaturation mécanique de présentation** : l'intermédiaire généré est systématiquement ressorti colorisé (constat documenté 3/3 — biais du modèle sur cette scène iconique) ; l'étage rendu restaure le monochrome et les rendus finaux sont certifiés N&B. L'intermédiaire natif colorisé est conservé à côté pour traçabilité complète.
- Rendu 19 : génération ANTICIPÉE 2027 (calibration [RUMEUR], jamais mesurée en labo — pixel binning : Digital Chat Station via Frandroid 27/03/2026) ; rendu 17 : périmètre d'époque supersédé au plan générationnel.
- La photographie demeure strictement monochrome dans toutes les versions — aucune colorisation n'a été appliquée (une colorisation éventuelle ne pourrait survenir QUE sur demande explicite, signalée « reconstruction réaliste » — règle 7/G3).

## ❓ Souhaitez-vous des modifications ? (question obligatoire — §9)

La comparaison enrichie des trois rendus pour « libération après guerre » est livrée (réponse §9 déjà fixée par votre directive : « sans modification, ni retouches » — aucune retouche ne sera effectuée). **Souhaitez-vous autre chose — par exemple une variante de mise en page, un zoom sur le camion ou un drapeau, ou un poster A4 d'un des rendus ?** (Sans demande explicite, aucune retouche ne sera effectuée — G7.)
