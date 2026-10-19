# Rapport PA-TEST-002 — Test robuste du skill `iphone18` v1.0.0 (campagne série §10, 2 photos)

> Pipeline exécuté selon `skills/iphone18/SKILL.md` (projection VERBATIM du PM `skills/@photos/iphone18-photos.md` v1.0) — Task 45 Groupe E, session web-38713acd. Mode SÉRIE §10 : sorties une par une, QC unitaire, rapport unifié, question unique finale.

## 📋 Analyse (grille ANALYSE-v2 — scores + inventaire B6 + cadrage/focale/ouverture demandés)

### Sortie 1 — PA-TEST-002-1 « musikalarue - les copines.jpg » (604×453 4:3, sans EXIF)
| A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | **3** | **3** | 2 | 2 | 2 | 1 | **3** | 1 | 0 |

- **B1** : 6 visages premier plan (femmes, groupe serré) + 1 homme partiel arrière-plan droit · **B2** : badge « FESTIVAL » (lanière verte, porté par la femme à la casquette) · **B3** : fête/festival extérieur nocturne sous tente · **B4** : flash intégré direct (dur) + ambiance nocturne faible · **B5** : plan moyen rapproché groupé serré, horizontal.
- **B6 (verrouillé)** : P1 queue-de-cheval châtain clair (sourire discret, tête penchée droite, débardeur noir, bracelets, verre brun, sac ethnique) · P2 brune mi-longue (large sourire dents, débardeur gris, collier ras-du-cou) · P3 châtaine courte (sourire très large yeux plissés, tête tournée à droite penchée, haut rouge + accessoire vert cou) · P4 casquette noire (sourire éclatant bouche ouverte, collier perlé blanc, badge FESTIVAL, verre rosé) · P5 blonde attachée (rire franc yeux fermés, tête rejetée arrière tournée à gauche, débardeur kaki, manchette) · P6 brune courte (grand sourire, tête penchée gauche, caraco blanc, boucles pendantes) · DÉCOR : tente blanche h.g., fond nocturne noir, homme torse nu partiel à droite.
- **C1** compact années 2000 (flash direct) · **C2** 2000s-début 2010 · **C3** rendu défaut `iphone18_max`, support écran, focale : aucune, ouverture : auto.

### Sortie 2 — PA-TEST-002-2 « musikalarue - les potos.jpg » (604×453 4:3, sans EXIF)
| A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 1 | **3** | 2 | 2 | 2 | 1 | 2 | 1 | 0 |

- **B1** : 6 visages en cercle serré, têtes réunies au centre (dont une tête en bas — composition inhabituelle conservée telle quelle) · **B2** : aucun texte lisible (inscription graphique partielle sur un t-shirt, à préserver) · **B3** : soirée intérieure · **B4** : lumière artificielle intérieure dure (ombres marquées) · **B5** : plan rapproché collectif circulaire centré.
- **B6 (verrouillé)** : P1 longue brune raie au milieu (sourire large bouche ouverte, tête en bas, piercing septum, objet vert en main, maquillage yeux) · P2 brune longue (moue/sourire timide, tête penchée, visage partiellement chevauché par les cheveux de P1 — chevauchement préservé) · P3 longue brune ondulée (sourire en coin, haut moutarde, casquette noire à l'envers, eye-liner, piercing nostril droit) · P4 dégarni dessus (neutre sérieux lèvres serrées, strictement de face) · P5 tempes dégarnies (neutre, lunettes fines métalliques, barbe plusieurs jours) · P6 châtains dégarnis (air surpris bouche entrouverte, t-shirt gris à inscription graphique rose/violette, piercing nostril) · DÉCOR : mur intérieur clair, ligne d'angle verticale.
- **C1** smartphone/compact bas de gamme · **C2** 2000s-2010 · **C3** rendu défaut `iphone18_max`, support écran, focale : aucune, ouverture : auto.

## 🧠 Diagnostic & règles déclenchées

- **Sortie 1** : R1 (A5=2 deblocking), R3 (A1=2 exposition), R4 (A2=3 ombres/HL), R5 (A3=3 débruitage), R6 (A4=2 défloutage), R7 (A6=2 super-résolution), **R8** (visages prioritaires), R10 (A8=3 tone-mapping), **R13** (ère 2000s + iphone18_max → mode restauration, authenticité préservée), **R18** (basse lumière + groupe → défaut auto).
- **Sortie 2** : R1, R3 (A1=2), R5 (A3=3), R6, R7, **R8**, R10 (A8=2), **R13**, **R18** — R4 non déclenchée (A2=1).
- Non déclenchées : R2 (A10=0), R9 (A7=1), R11-R12 (pas de preset d'époque/variation), R14-R16 (pas de print/poster), R15 (pas de terme ambigu), R17 (pas de focale demandée).

## 🗺️ Plan d'actions exécuté (PA-20261020-002 — YAML complet : `scripts/task45e-plan-PA-20261020-002.yaml`)

- **focale_cible** : aucune · **ouverture_cible** : auto → **ƒ/4.0** (R18 défaut : scène de groupe 6 sujets → netteté étendue avant-arrière ; basse lumière couverte par le pipeline nuit P2/P3 + rendu mode nuit — pondération documentée, précédent PA-TEST-001) · **rendu_cible** : `iphone18_max` · série : 2 sorties (ordre utilisateur copines → potos) · pipeline P0→P9 exécuté par sortie en chaîne 2 appels (P1-P6 consolidés → rendu iphone18_max + R18) via le script embarqué du skill `skills/iphone18/scripts/editer-image.mjs` (contournement SDK base64 — CLI z-ai image-edit erreur 1210). 4/4 appels réussis à la 1re tentative.
- **Estimation a posteriori** : risque principal anticipé (fidélité en flash dur + chevauchements de visages) — non matérialisé (QC 12/12 ×2).

## ✅ Résultat QC (grille §5 — QC unitaire par sortie, comparaison vision original↔sortie)

### Sortie 1 — `download/PA-TEST-002-1-iphone18-max.png` (1152×864, 4:3 natif)
| # | Critère | Verdict |
|---|---------|---------|
| 1 | Visages naturels, identité préservée (G1) | OK |
| 2 | Expressions strictement identiques (sourires, regards, orientations des 6 têtes) | OK |
| 3 | Coiffures/vêtements/accessoires/morphologie — inventaire B6 (G6) | OK |
| 4 | Aucun élément ajouté/supprimé (G3) | OK |
| 5 | Sources lumineuses sans halo, badge FESTIVAL intact (G2/G4) | OK |
| 6 | Bruit ≈ 0 sans effet plastique (G4) | OK |
| 7 | Rendu iphone18_max respecté | OK |
| 8 | Cadrage/plan conservé | OK |
| 9 | Ratio 4:3 exact — sortie 1152×864 native (pas de P8b requis) | OK |
| 10 | Adéquation résolution 604×453 → écran (×1,9 propre, pas de P8b/print) | OK |
| 11 | Focale : aucune demandée — cadre conservé | OK |
| 12 | Ouverture ƒ/4.0 simulée : netteté étendue du groupe, sujets intacts (R18) | OK |

**→ 12/12 OK — zéro divergence de fidélité détectée. Itération : aucune.**

### Sortie 2 — `download/PA-TEST-002-2-iphone18-max.png` (1152×864, 4:3 natif)
| # | Critère | Verdict |
|---|---------|---------|
| 1 | Visages naturels, identité préservée (G1) | OK |
| 2 | Expressions strictement identiques (y compris tête en bas + chevauchement de visage préservé) | OK |
| 3 | Coiffures/vêtements/accessoires — inventaire B6 (casquette à l'envers, 3 piercings nez, lunettes, barbe, inscription t-shirt) | OK |
| 4 | Aucun élément ajouté/supprimé (G3) | OK |
| 5 | Sources lumineuses sans halo, inscription graphique intacte (G2/G4) | OK |
| 6 | Bruit ≈ 0 sans effet plastique (G4) | OK |
| 7 | Rendu iphone18_max respecté | OK |
| 8 | Cadrage/plan conservé (cercle complet) | OK |
| 9 | Ratio 4:3 exact — 1152×864 native (pas de P8b requis) | OK |
| 10 | Adéquation résolution 604×453 → écran (×1,9 propre) | OK |
| 11 | Focale : aucune demandée — cadre conservé | OK |
| 12 | Ouverture ƒ/4.0 simulée : cercle uniformément net, sujets intacts (R18) | OK |

**→ 12/12 OK — verdict fidélité « fidèle » ; 3 notes de rendu mineures documentées ci-dessous. Itération : aucune.**

### Bilan global de la campagne
| Sortie | QC | Fidélité | Itérations |
|--------|----|----------|------------|
| PA-TEST-002-1 (copines) | **12/12 OK** | fidèle — 0 divergence | 0 |
| PA-TEST-002-2 (potos) | **12/12 OK** | fidèle — 3 notes mineures | 0 |
| **Campagne PA-TEST-002** | **PASS** | G1-G7 + B6 respectés | 0/2 max |

## 🖼️ Description du résultat

- **PA-TEST-002-1** : groupe de six amies sous la tente du festival, nuit — rendu « iPhone 18 Pro Max qualité max » : mode nuit propre (flash douci sans halo), teintes chair naturelles, sourires et orientations inchangés, badge FESTIVAL lisible, netteté uniforme du premier plan au fond (ƒ/4.0 simulé). Sortie écran 1152×864 (P8b non requis — 4:3 natif).
- **PA-TEST-002-2** : cercle de six amis en soirée — rendu nuit propre, peaux naturelles, piercings/lunettes/casquette à l'envers/inscription graphique préservés, cercle uniformément net (ƒ/4.0 simulé). Sortie écran 1152×864 (P8b non requis).
- Intermédiaires P1-P6 livrés : `download/PA-TEST-002-{1,2}-amelioration-P1-P6.png`.

## ⚠️ Limites & reconstructions honnêtes

- **Avis R18 (ouverture variable)** : la profondeur de champ perçue et la collecte de lumière ƒ/4.0 sont un **rendu computationnel, pas une optique physique** — les sujets ne sont jamais altérés (G1/G3/G6). Pondération auto documentée (groupe → ƒ/4.0, basse lumière → pipeline nuit).
- **Avis R7/R8 (super-résolution)** : sources 604×453 — les détails fins (maillage cutané, fines mèches) sont restitués par reconstruction IA fidèle, pas par interpolation ; tout détail non résoluble à cette résolution reste non inventé (aucun texte, aucun motif créé).
- **Sortie 2 — 3 notes de fidélité mineures (QC vision, verdict global « fidèle »)** : (1) très léger lissage du maillage cutané sur certains visages — jugé naturel, non plastique (critère 6 OK) ; (2) teinte globale légèrement plus chaude et contraste accru — effet attendu du rendu P5/iphone18_max (critère 7 OK) ; (3) détails fins de cheveux légèrement adoucis par le débruitage (A3=3 source). Aucune note sur les expressions, orientations, coiffures, vêtements, accessoires ou éléments de scène.
- **Éléments [SPÉCULATIF]** : aucun (squelette §6.10 iphone19 inactif — règle 14).

## ❓ Souhaitez-vous des modifications ? (question OBLIGATOIRE — §9, posée UNE seule fois pour la campagne)

Les deux sorties PA-TEST-002-1 et PA-TEST-002-2 sont livrées avec leur QC 12/12. **Souhaitez-vous des modifications sur l'une des sorties ?** (Sans réponse explicite, aucune retouche ne sera effectuée — G7.)
