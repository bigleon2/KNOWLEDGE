# Rapport Task 48 — G2/S2 : comparaison côte à côte enrichie du rendu 19 pour « Les Potos »

> gen-plan v3.23.1 mode (step) — groupe G2. Mini-plans persistés AVANT action (règle 3) : `scripts/task48-plan-PA-20261021-006.yaml` (campagne) et `scripts/task48-plan-directive.yaml` (directive). Composite PIL pur — zéro appel générationnel pour la comparaison, zéro modification des sources (sha256 des 5 fichiers vérifiés avant/après). **Adapté à la photo originale « les potos »** : 5 versions + guide de lecture propre à son contenu.

## 📋 Demande

« Effectue la même comparaison enrichie du rendu 19 pour la photo "Les Potos" (la réponse à la dernière question du skill sera "sans modification, ni retouches"). » — soit : (1) un rendu 19 de la **version courante v0.10.0** (émulation pixel binning R19, issue du groupe G1) sous contrainte zéro-retouche, puis (2) la même comparaison enrichie que celle livrée pour « les copines » (Task 47 D7 : 5 versions + guide de lecture + rapport).

## 🗺️ Plan exécuté

**Campagne PA-20261021-006** (skill iphone19 v0.10.0, série §10) — contrainte propriétaire §9 pré-décidée « sans modification, ni retouches » (G1-G7 stricts, inventaire B6 verrouillé, aucune retouche créative) :

1. **Appel 1 — P1-P6 consolidé avec expression R19** (§7 : « rendu capteur à pixels fusionnés — bruit maîtrisé, SNR accru, micro-détail fin préservé ») : original 604×453 → intermédiaire 1152×864 (`PA-TEST-006-1-amelioration-P1-P6.png`).
2. **Appel 2 — rendu conservateur à verrouillage facial + caractère binning** : la leçon PA-TEST-005 it.2 (composition atypique → rendu MINIMAL CONSERVATEUR avec visages verrouillés **dès la première passe**) est appliquée d'emblée — la recette it.2 éprouvée (12/12) est reprise intégralement, augmentée du caractère « pixels fusionnés » du binning 16-en-1 → candidat versionné v1, promu final après QC.
3. **Comparaison enrichie** : composite PIL 2×3 (task48-comparaison-potos.py).

## ✅ Résultat QC

| # | Vérification | Verdict |
|---|---|---|
| 1 | Rendu produit — chaîne 2 appels, canevas 1152×864 (×1,9 propre), candidat versionné jamais écrasé | OK |
| 2 | QC grille **13 critères v0.10.0** : 12/13 directs — critère 5 (inscription t-shirt) KO en grille globale → **arbitrage ciblé pleine image (confiance haute) : inscription identique, netteté excellente pour ×1,9, verdict INTACT** → requalifié (protocole variance-vision Groupe F / précédent PA-TEST-004) → **13/13** | OK |
| 3 | Fidélité : verdict « divergences mineures » — les 3 relevés sont tous des effets de rendu attendus (douceur d'upscale arbitrée intacte ; micro-lissage tissu = débruitage A3=3 ; courbe de contraste = caractère « nuit propre » demandé) — **aucune violation G1-G7, aucun contenu modifié** | OK |
| 4 | **Critère 13 (R19 binning) : OK** — caractère « pixels fusionnés » respecté sans lissage plastique ni altération des sujets | OK |
| 5 | Leçon PA-TEST-005 appliquée (rendu conservateur dès la 1re passe) : **zéro itération nécessaire**, budget 2/2 intact | OK |
| 6 | P0 intact — sha256 `1a5c04df6d3783ba…` identique avant/après | OK |
| 7 | Comparaison : 2208×1204, 6 panneaux 720×540 légendés, composite PIL pur, **5 sources sha256 intacts** avant/après (empreintes pré-vol vérifiées) | OK |
| 8 | Règle 3 : plans persistés AVANT action (mini-plan campagne + plan directive) | OK |

**→ 8/8 OK.** Preuves : `scripts/task48-pa006-qc-1.json` (grille 13), `scripts/task48-pa006-arbitrage-{1,2,3}.json` (arbitrages ciblés).

## 🖼️ Description du livrable

**`download/comparaison-les-potos-cote-a-cote-5-versions.png`** (2208×1204) — grille 2×3 :

| Haut gauche | Haut centre | Haut droite |
|---|---|---|
| **ORIGINAL** — 604×453, source P0 : soirée intérieure, lumière artificielle dure, bruit élevé, six têtes en cercle | **AMÉLIORATION QUALITÉ SEULE** — P1-P6 v0.10.0 avec binning R19 : exposition +0,7 EV, débruitage, déblocage JPEG, netteté ×1,9 — sans style (PA-TEST-006-1) | **RENDU iPhone 17 Pro Max** — iphone17_max, périmètre d'époque Photonic Engine NG (PA-TEST-004-1, QC arbitré haute confiance) |
| **Bas gauche** | **Bas centre** | **Bas droite** |
| **RENDU iPhone 18 Pro Max** — iphone18_max, génération confirmée, R18 ƒ/4.0 + Styles 3 (PA-TEST-002-2, QC 12/12) | **RENDU iPhone 19 Pro Max v0.10.0** — ANTICIPÉ 2027 + **émulation pixel binning R19** (capteur 200 MP, fusion 16-en-1 → 12,5 MP équivalente : SNR accru, nuit propre, micro-détail préservé — PA-TEST-006-1, QC 13/13) | **GUIDE DE LECTURE** — ordre de comparaison, repères potos (tête inversée au centre, chevauchement conservé, casquette à l'envers, 3 piercings, inscription t-shirt), lignée 17→18→19 + R19 |

Lecture conseillée : comparer d'abord l'original ↔ amélioration qualité (gain technique pur, binning inclus), puis l'amélioration ↔ les trois rendus générationnels (17 d'époque → 18 confirmée → 19 anticipée + binning : le traitement de la soirée dure progresse d'un cran à chaque génération, la v0.10.0 ajoutant le caractère « pixels fusionnés » du capteur 200 MP rumeuré).

## ⚠️ Limites honnêtes

- Panneaux affichés à 720×540 pour la vue d'ensemble — pour l'inspection fine (inscription du t-shirt, teintes chair, chevauchement), se reporter aux fichiers pleine résolution 1152×864 (`download/PA-TEST-00{2,4,6}-*.png`).
- Le panneau original est agrandi ×1,19 pour l'alignement de la grille (il reste le plus « doux » — réalité de la source 604×453).
- Le rendu 19 présenté est celui de la **version courante v0.10.0** ; le rendu v0.9.0 (PA-TEST-005-2, QC 12/12) demeure disponible — la différence attendue porte sur le caractère binning (finition SNR/micro-détail), subtile par construction (émulation de rendu, calibration [RUMEUR] jamais mesurée en labo).
- Intermédiaires P1-P6 historiques (PA-TEST-003-2 / 004-2 / 005-2) toujours disponibles ; c'est le plus récent (v0.10.0 avec R19) qui est présenté — précédent copines D7.
- 19_max reste une **ANTICIPATION** (génération non confirmée au 2026-10-21 ; pixel binning = [RUMEUR] Digital Chat Station via Frandroid 27/03/2026 — v1.0.0 à la confirmation officielle Apple).

## ❓ Souhaitez-vous des modifications ? (question obligatoire — §9)

La comparaison enrichie du rendu 19 pour « les potos » est livrée (rendu v0.10.0 QC 13/13 sous contrainte « sans modification, ni retouches » — réponse §9 déjà fixée par votre directive : aucune retouche ne sera effectuée). **Souhaitez-vous autre chose — par exemple une variante de mise en page (1×5, zoom sur un visage, poster A4), ou un ajustement du traitement ?** (Sans demande explicite, aucune retouche ne sera effectuée — G7.)
