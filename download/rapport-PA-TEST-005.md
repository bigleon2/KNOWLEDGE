# Rapport PA-TEST-005 — Test du skill `iphone19` v0.9.0 [ANTICIPÉE] (campagne série §10, 2 photos — contrainte propriétaire : zéro modification, zéro retouche)

> Pipeline exécuté selon `skills/iphone19/SKILL.md` (projection VERBATIM du PM `skills/@photos/iphone19-photos.md` v0.9.0 [ANTICIPÉE] — génération 19 non confirmée, calibration extrapolée) — Task 47, session web-38713acd. Mode SÉRIE §10 : sorties une par une, QC unitaire (grille 12 critères), rapport unifié, question unique finale. **Contrainte propriétaire respectée sur toute la chaîne : « je ne veux pas faire de modifications et de retouches à ces photos » — interprétation alignée sur la réponse §9 PA-TEST-004 (« aucune modification — uniquement l'amélioration de la qualité ») : pipeline qualité standard, rendu défaut `iphone19_max` (moteur R13/R18), AUCUNE retouche créative, garde-fous G1-G7 stricts, inventaires B6 verrouillés.**

## 📋 Analyse (grilles ANALYSE-v2 réutilisées des campagnes PA-TEST-002/003 — photo-intrinsèques identiques, économie API KO-L001 ; B6 verrouillés : `scripts/task45e-an-copines.json` / `task45e-an-potos.json`)

### Sortie 1 — PA-TEST-005-1 « musikalarue - les copines.jpg » (604×453 4:3, sha256:62cd2fac…)
A1=2 A2=**3** A3=**3** A4=2 A5=2 A6=2 A7=1 A8=**3** A9=1 A10=0 · B1=6 visages + homme partiel · B2=badge FESTIVAL · B3=fête nocturne sous tente · B4=flash direct · B5=plan moyen groupé · C1=compact 2000s · C2=2000s-début 2010 · **C3=rendu défaut `iphone19_max`**, écran, focale aucune, ouverture auto (→ ƒ/4.0, groupe).

### Sortie 2 — PA-TEST-005-2 « musikalarue - les potos.jpg » (604×453 4:3, sha256:1a5c04df…)
A1=2 A2=1 A3=**3** A4=2 A5=2 A6=2 A7=1 A8=2 A9=1 A10=0 · B1=6 visages en cercle (tête en bas au centre, chevauchement de visage) · B2=inscription graphique t-shirt · B3=soirée intérieure · B4=lumière artificielle dure · B5=plan rapproché collectif circulaire · C1=smartphone/compact bas de gamme · C2=2000s-2010 · **C3=`iphone19_max`**, écran, focale aucune, ouverture auto (→ ƒ/4.0, groupe).

## 🧠 Diagnostic & règles déclenchées (moteur R1-R18 — aucune règle R19 : aucune capacité fonctionnelle confirmée)

- **Sortie 1** : R1 (A5=2), R3 (A1=2), R4 (A2=3), R5 (A3=3), R6 (A4=2), R7 (A6=2), **R8** (6 visages prioritaires), R10 (A8=3), **R13** (ère 2000s + iphone19_max → mode restauration), **R18** (groupe → défaut ƒ/4.0). **Sortie 2** : R1, R3, R5 (A3=3), R6, R7, **R8**, R10, **R13**, **R18** (R4 non déclenchée, A2=1).
- Adaptation du traitement à chaque photo (directive propriétaire) : copines → priorité écrêtage flash (R4)/bruit (R5)/tone-mapping (R10), badge FESTIVAL strictement préservé (G2/B2) ; potos → priorité bruit (R5), composition circulaire atypique conservée telle quelle, chevauchement de visages préservé, inscription du t-shirt intacte (G2), zone de fragilité connue (échec rendu 17 documenté PA-TEST-003-2) → vigilance fidélité renforcée au QC.

## 🗺️ Plan d'actions exécuté (PA-20261020-005 — YAML : `scripts/task47-plan-PA-20261020-005.yaml`, persisté AVANT exécution — règle 3)

Chaîne 2 appels/sortie via `skills/iphone19/scripts/editer-image.mjs` (contournement SDK base64) : P1-P6 consolidé → rendu `iphone19_max` (ƒ/4.0), canevas 1152×864 (×1,9 propre). **Candidats VERSIONNÉS par tentative** (leçon PA-TEST-003-2 — jamais d'écrasement). Remède erreur SSE appliqué à tous les appels vision : `createVision` + `thinking: disabled` (pattern éprouvé — jamais de parsing JSON de flux stream). Estimation a posteriori : risque anticipé « dérive générationnelle sur composition atypique potos » CONFIRMÉ sur la v1 puis résorbé (voir QC) — le budget d'itération §5 (2/2) a suffi.

## ✅ Résultat QC (grille 12 critères, QC unitaire par sortie — `scripts/task47-pa005-qc.mjs`)

### Sortie 1 — `download/PA-TEST-005-1-iphone19-max.png` (1152×864, 4:3 natif) — candidat v1 PROMU
| # | Critère | Verdict |
|---|---------|---------|
| 1-6 | Visages/identité, expressions des 6 visages, B6 (coiffures/vêtements/accessoires dont badge FESTIVAL + collier perlé + boucles pendantes), zéro ajout/suppression, sources sans halo, bruit ≈ 0 sans plastique | **OK** |
| 7 | Rendu `iphone19_max` respecté (netteté zones utiles, nuit propre, groupe net ƒ/4.0, textures réalistes) | OK |
| 8-11 | Cadrage conservé, ratio 4:3 exact 1152×864, agrandissement ×1,9 propre, focale aucune — cadre conservé | OK |
| 12 | Ouverture ƒ/4.0 (défaut auto groupe) : netteté étendue avant-arrière, zéro altération des sujets | OK |

**→ 12/12 OK — verdict fidélité « fidèle », divergences : aucune. Itération : aucune (première tentative).** Intermédiaire P1-P6 livré : `download/PA-TEST-005-1-amelioration-P1-P6.png`.

### Sortie 2 — `download/PA-TEST-005-2-iphone19-max.png` (1152×864) — candidat v3 PROMU après itérations
Historique d'exécution (budget d'itération §5 = 2/2 utilisé, candidats versionnés) :

| # | Configuration | QC | Verdict |
|---|---------------|----|---------|
| v1 | Chaîne standard (P1-P6 → rendu iphone19_max) | **4/12** | Divergences majeures : lunettes rondes noires INVENTÉES + piercing septum DISPARU + expression changée sur la femme tête en bas (G1/G3/G6 — mêmes inventions que l'échec 17_max PA-TEST-003-2 récup.2) ; barbe inventée sur la femme au haut moutarde (G3) ; boucle d'oreille inventée (G3) ; moues ajoutées sur les hommes dégarnis (G1) ; lissage cutané agressif « peau de pêche » (G4) |
| it.1 | Rendu durci (prompt éprouvé PA-TEST-004 adapté + contre-mesures ciblées : anti-lunettes, anti-barbe, anti-boucle, conservation septum) | **5/12** | PROGRÈS : toutes les inventions G3 éliminées (plus de lunettes/barbe/boucle, septum conservé) — mais dérives persistantes : lèvres pincées sur l'homme de face (G1), léger sourire ajouté sur l'homme à lunettes (G1), sur-lissage G4 + altérations de forme nez/joues |
| it.2 | **Rendu conservateur à verrouillage facial** (visages = zones verrouillées copiées à l'identique, grain de peau préservé, intervention minimale : netteté homogène + lumière maîtrisée + tone-mapping doux) | **12/12** | **PASS — fidélité « fidèle », divergences : aucune. Tous les garde-fous respectés (expressions exactes, chevauchement conservé, inscription t-shirt intacte, 3 piercings présents, G4 respecté)** |

**→ Sortie 2 : PASS après itération contrôlée 2/2 — livrable final = candidat v3.** Intermédiaire P1-P6 livré : `download/PA-TEST-005-2-amelioration-P1-P6.png`.

### Bilan global de la campagne
| Sortie | QC final | Itérations | Livrable |
|--------|----------|------------|----------|
| PA-TEST-005-1 (copines) | **12/12 OK** — fidèle | 0 | final `iphone19_max` + intermédiaire P1-P6 |
| PA-TEST-005-2 (potos) | **12/12 OK** — fidèle | 2/2 (v1 4/12 → it.1 5/12 → it.2 12/12) | final `iphone19_max` (candidat v3) + intermédiaire P1-P6 |
| **Campagne PA-TEST-005** | **PASS** | — | contrainte propriétaire zéro modification/retouche respectée sur les 2 sorties ; originaux P0 intacts (sha256 vérifiés : 62cd2fac… / 1a5c04df…) |

## 🖼️ Description des résultats

- **PA-TEST-005-1 (copines)** : les six amies sous tente, nuit — rendu « iPhone 19 Pro Max qualité max » ANTICIPÉ : mode nuit propre, sourires/orientations inchangés, badge FESTIVAL révélé et intact, teintes chair naturelles, netteté étendue ƒ/4.0 sur le groupe. 1152×864 (4:3 natif).
- **PA-TEST-005-2 (potos)** : le cercle des six amis — même rendu ANTICIPÉ, obtenu après 2 itérations : expressions exactes (dont la tête inversée au centre et le chevauchement de visage), inscription du t-shirt intacte, grain de peau naturel.

## ⚠️ Limites & reconstructions honnêtes

- **Statut ANTICIPÉ du preset** : la calibration `iphone19_max` est une EXTRAPOLATION des rumeurs crédibles 2026 (A21 Pro — Macworld ; Photonic Engine NG+ ; Face ID sous écran — The Information/Kuo) — **aucune spécification officielle n'existe au 2026-10-20** (keynote attendu sept. 2027) ; aucun calibrage labo possible ; le rendu est une anticipation prudente de la baseline confirmée 18 ; bump v1.0.0 + re-ancrage prévus à la confirmation officielle (§6.10). Téléobjectif 200 MP [NON VÉRIFIÉ — rumeur unique] NON intégré. Incertitude de nommage (iPhone 19 vs 20, 20e anniversaire) documentée.
- **Zone de fragilité confirmée (sortie 2)** : la composition circulaire atypique (6 têtes chevauchées, tête inversée, source 604×453) déclenche une dérive générationnelle non déterministe sur la première tentative (inventions G3 identiques à l'échec 17_max documenté). **Leçon consignée** : sur compositions atypiques, la contre-mesure efficace est le rendu MINIMAL CONSERVATEUR à verrouillage facial (it.2) — à appliquer dès la première itération dans les prochaines campagnes.
- **Avis R18** : ouverture ƒ/4.0 simulée (défaut auto scène de groupe) — rendu tonal/profondeur perçue, computationnel et non optique (honnêteté règle 7).
- **Avis R7/R8** : sources 604×453 — reconstruction fidèle ×1,9, aucun texte/motif inventé (badge FESTIVAL et inscription t-shirt vérifiés intacts).
- **Éléments [SPÉCULATIF]** : squelette `iphone20` (§6.10) — INACTIF, jamais appliqué (règle 14).

## ❓ Souhaitez-vous des modifications ? (question OBLIGATOIRE — §9, posée UNE seule fois pour la campagne)

Les deux rendus `iphone19_max` (12/12 chacun, fidèles, zéro retouche conformément à votre contrainte) et leurs intermédiaires P1-P6 sont livrés. **Souhaitez-vous des modifications — par exemple une nouvelle tentative sans itération sur les potos, un autre preset (époque, poster), ou un traitement sur une autre photo ?** (Sans réponse explicite, aucune retouche ne sera effectuée — G7.)
