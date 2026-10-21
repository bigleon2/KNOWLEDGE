# Rapport Task 48 — G4/S4 : test robuste des skills iphone17, iphone18 et iphone19 sur « libération après guerre »

> gen-plan v3.23.1 mode (step) — groupe G4. Mini-plan `scripts/task48-plan-PA-20261021-007.yaml` (persisté AVANT exécution — règle 3). Contrainte propriétaire §9 pré-décidée pour CHAQUE skill : **« sans modification, ni retouches »** — G1-G7 stricts, inventaire B6 verrouillé, extension 1944 §6.6 (monochrome natif, grain préservé, **aucune colorisation**).

## 📋 Analyse (grille ANALYSE-v2 — photo inédite, `scripts/task48-pa007-analyse.json`)

**Source** : `upload/libération après guerre.png` — 828×550 (3:2), tirage argentique N&B scanné (C1), **août 1944, Libération de Paris** (C2), monochrome neutre (A7=0, aucune dominante).

| Axe | Scores | Observation clé |
|---|---|---|
| Technique | A1=1 · A2=2 · **A3=1 (grain authentique ≠ bruit)** · A4=1 · A5=0 · A6=1 · A7=0 · A8=2 · A9=1 · A10=2 | Écrêtage ciel/chemises + ombres denses (R4) ; contraste dur de tirage ancien (R10) ; **grain argentique cohérent, à préserver** (note §1 v-bump : R5 NON déclenchée) ; taches/poussières d'âge (R2) ; piqué modéré assumé (R7 NON déclenchée) |
| Sémantique | B1 = foule nombreuse (camion + sol) · B2 = aucun texte lisible · B3 = fête de libération · B4 = lumière du jour · B5 = plan large | **Inventaire B6 verrouillé** : camion militaire sombre (calandre verticale, câbles, AUCUN marquage) ; homme casqué au sommet bras levé + drapeau ; **drapeau tricolore français + drapeau américain** ; jeune homme sourisant (pull col en V, carabine sur les genoux) ; jeune femme (robe claire à motifs, jambes pendantes) ; homme au pare-choc (costume sombre, cravate claire, casque posé) ; 3 pousseurs ; garçon qui court ; silhouette partielle ; immeuble haussmannien + bâtiment bas + arbres + rue pavée |
| Contextuel | C1 = tirage argentique scanné · C2 = années 1940 · C3 = défaut par skill | Règles déclenchées : **17 : [R2, R4, R10, R13]** · **18 : [R2, R4, R10, R13, R18]** · **19 : [R2, R4, R10, R13, R18, R19]** |

## 🗺️ Plan exécuté (par skill : P1-P6 [1 appel] → rendu conservateur [1 appel], ordre 17 → 18 → 19)

- **Sortie 1 — iphone17 v1.1.0 (d'époque)** : P1-P6 → intermédiaire → rendu 17_max conservateur (Photonic Engine NG), QC 11 critères.
- **Sortie 2 — iphone18 v1.1.0 (confirmée)** : P1-P6 → rendu 18_max (ƒ/4.0 netteté étendue + Styles 3), QC 12 critères.
- **Sortie 3 — iphone19 v0.11.0 (ANTICIPÉE)** : P1-P6 + expression R19 → rendu 19_max (ƒ/4.0 + binning « pixels fusionnés »), QC 13 critères.
- Canevas 1152×768 (×1,39 propre) ; candidats versionnés par tentative ; P0 sha256 `5818fa6a1aaa7ae9…` vérifié identique avant/après.

## ✅ Résultat QC (par sortie)

| Sortie | Verdict | Détail |
|---|---|---|
| **PA-TEST-007-1 (17_max)** | **11/11 OK — fidèle, zéro divergence** (candidat v1, zéro itération) | Monochrome ✓, grain préservé ✓, inventaire B6 ✓, aucun ajout ✓ — saturation mécanique 0.16 |
| **PA-TEST-007-2 (18_max)** | **12/12 OK — fidèle, zéro divergence** (après **itération 1/2**) | v1 rejetée : **colorisation complète** (drapeaux peints bleu-blanc-rouge, camion vert olive, grain écrasé, visages altérés — 4/12, divergences majeures) → it.1 : P1 renforcé anti-colorisation + rendu → v2 fidèle — saturation 0.10 |
| **PA-TEST-007-3 (19_max)** | **13/13 OK — fidèle, zéro divergence** (candidat v1, zéro itération) | Monochrome ✓, grain ✓, ƒ/4.0 ✓, **binning R19 ✓ (pixels fusionnés, SNR, micro-détail, sans écraser le grain)** — saturation 0.48 (monochrome confirmé critère 4) |

**Preuves** : `scripts/task48-pa007-qc-{1,2,2-it1,3}.json` · mesure PIL des saturations (original 0.01 ; finaux 0.16 / 0.10 / 0.48).

## 🖼️ Description des livrables

- `download/PA-TEST-007-1-iphone17-max.png` — rendu 17 d'époque (1152×768)
- `download/PA-TEST-007-2-iphone18-max.png` — rendu 18 confirmée (1152×768, candidat v2 promu)
- `download/PA-TEST-007-3-iphone19-max.png` — rendu 19 ANTICIPÉ + binning (1152×768)
- Intermédiaires P1-P6 versionnés (`*-amelioration-P1-P6*.png`) + candidats non promus conservés (v1 18) — traçabilité complète.
- Comparaison enrichie : `download/comparaison-liberation-apres-guerre-cote-a-cote.png` (rapport dédié : `rapport-comparaison-liberation.md`).

## ⚠️ Limites & enseignements honnêtes

1. **Biais de colorisation à l'étage P1-P6 (constat systématique)** : sur cette scène iconique, l'appel « amélioration technique » a produit un intermédiaire **colorisé** 3 fois sur 3 (saturation 23-29), y compris avec l'instruction renforcée interdisant toute couleur en tête. Le biais du modèle de génération (« Libération de Paris » → souvenir couleur) dépasse la force de la consigne à cet étage.
2. **Le rendu conservateur restaure le monochrome** : l'étage rendu (instructions « DEMEURE en noir et blanc strict ») a correctement re-monochromé l'image (17 : v1 finale fidèle dès la 1re passe ; 18 : v2 fidèle après itération ; 19 : v1 fidèle). **La recette éprouvée sur cette photo : P1-P6 (quoi qu'il produise) → rendu conservateur monochrome — le LIVRABLE final est conforme.**
3. Le panneau « amélioration technique » de la comparaison est une copie **désaturée mécaniquement (PIL)** de l'intermédiaire 19, présentée comme telle (étiquette honnête) — l'intermédiaire natif colorisé reste livré à côté pour traçabilité.
4. Piqué modéré de la source assumé (avis R16-style : agrandissement ×1,39 propre, aucun détail inventé — QC 10 OK ×3).
5. Rendu 19 : saturation résiduelle 0.48 (traces infimes) — validée monochrome par le QC (critère 4), à la limite du mesurable.

## ❓ Souhaitez-vous des modifications ? (question obligatoire — §9)

Le test robuste est livré : **les 3 skills (17 v1.1.0, 18 v1.1.0, 19 v0.11.0) traitent la photo de 1944 de façon fonctionnelle et optimisée — 11/11, 12/12 et 13/13, fidélité zéro divergence, monochrome et grain préservés** (réponse §9 déjà fixée par votre directive : « sans modification, ni retouches » — aucune retouche ne sera effectuée). **Souhaitez-vous autre chose — par exemple un poster A4 d'un des rendus, ou un zoom sur une zone ?** (Sans demande explicite, aucune retouche ne sera effectuée — G7.)
