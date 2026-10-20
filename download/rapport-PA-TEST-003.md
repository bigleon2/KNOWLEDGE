# Rapport PA-TEST-003 — Test robuste du skill `iphone17` v1.0.0 (campagne série §10, 2 photos)

> Pipeline exécuté selon `skills/iphone17/SKILL.md` (projection VERBATIM du PM `skills/@photos/iphone17-photos.md` v2.0 ARCHIVÉ — périmètre d'époque R1-R17, sans R18) — Task 45 Groupe F, session web-38713acd. Mode SÉRIE §10 : sorties une par une, QC unitaire (grille v2.0 à 11 critères), rapport unifié, question unique finale.

## 📋 Analyse (grille ANALYSE-v2 — réutilisée de la campagne PA-TEST-002 : grille photo-intrinsèque identique, économie API KO-L001)

### Sortie 1 — PA-TEST-003-1 « musikalarue - les copines.jpg » (604×453 4:3)
A1=2 A2=**3** A3=**3** A4=2 A5=2 A6=2 A7=1 A8=**3** A9=1 A10=0 · B1=6 visages + homme partiel · B2=badge FESTIVAL · B3=fête nocturne sous tente · B4=flash direct · B5=plan moyen rapproché groupé · C1=compact 2000s · C2=2000s-début 2010 · **C3=rendu défaut `iphone17_max`**, écran, focale aucune.
Inventaire B6 verrouillé : cf. `scripts/task45e-an-copines.json` (6 femmes détaillées + tente blanche + homme torse nu partiel).

### Sortie 2 — PA-TEST-003-2 « musikalarue - les potos.jpg » (604×453 4:3)
A1=2 A2=1 A3=**3** A4=2 A5=2 A6=2 A7=1 A8=2 A9=1 A10=0 · B1=6 visages en cercle (tête en bas au centre, chevauchement de visage) · B2=aucun texte lisible · B3=soirée intérieure · B4=lumière artificielle dure · B5=plan rapproché collectif circulaire · C1=smartphone/compact bas de gamme · C2=2000s-2010 · **C3=`iphone17_max`**, écran, focale aucune.
Inventaire B6 verrouillé : cf. `scripts/task45e-an-potos.json` (6 personnes détaillées, 3 piercings nez, casquette à l'envers, lunettes fines, barbe, chevauchement à préserver).

## 🧠 Diagnostic & règles déclenchées (moteur R1-R17 d'époque)

- **Sortie 1** : R1 (A5=2), R3 (A1=2), R4 (A2=3), R5 (A3=3), R6 (A4=2), R7 (A6=2), **R8** (visages prioritaires), R10 (A8=3), **R13** (ère 2000s + iphone17_max → mode restauration). **Sortie 2** : R1, R3, R5, R6, R7, **R8**, R10 (A8=2), **R13** (R4 non déclenchée, A2=1).
- Non déclenchées : R2 (A10=0), R9 (A7=1), R11-R12, R14-R16, R15, R17 (pas de focale demandée). **R18 : ABSENTE du pipeline v2.0** (ouverture variable = ajout v1.0 iphone18) — aucune simulation d'ouverture dans cette campagne.

## 🗺️ Plan d'actions exécuté (PA-20261020-003 — YAML : `scripts/task45f-plan-PA-20261020-003.yaml`)

- **focale_cible** : aucune (schéma v2.0 sans champ ouverture) · **rendu_cible** : `iphone17_max` (§6.1 v2.0 : Photonic Engine NG, netteté max zones utiles/visages prioritaires, mode nuit propre, textures réalistes) · série 2 sorties (copines → potos) · chaîne 2 appels/sortie via `skills/iphone17/scripts/editer-image.mjs` (contournement SDK base64).
- **Estimation a posteriori** : le risque anticipé « différenciation rendu 17 vs 18 » s'est doublé d'un risque réel non anticipé : **dérive générationnelle sur la composition atypique de la sortie 2** (détails ci-dessous).

## ✅ Résultat QC (grille v2.0 — 11 critères, QC unitaire par sortie)

### Sortie 1 — `download/PA-TEST-003-1-iphone17-max.png` (1152×864, 4:3 natif)
| # | Critère | Verdict |
|---|---------|---------|
| 1 | Visages naturels, identité préservée (G1) | OK |
| 2 | Expressions strictement identiques (6 visages, orientations inchangées) | OK |
| 3 | Coiffures/vêtements/accessoires — inventaire B6 (G6) | OK |
| 4 | Aucun élément ajouté/supprimé (G3) | OK |
| 5 | Sources sans halo, badge FESTIVAL intact (G2/G4) | OK |
| 6 | Bruit ≈ 0 sans effet plastique (G4) | OK |
| 7 | Rendu iphone17_max respecté (Photonic Engine NG) | OK |
| 8 | Cadrage/plan conservé | OK |
| 9 | Ratio 4:3 exact — 1152×864 native (pas de P8b) | OK |
| 10 | Adéquation résolution 604×453 → écran (×1,9 propre) | OK |
| 11 | Focale : aucune demandée — cadre conservé | OK |

**→ 11/11 OK — verdict fidélité « fidèle » (les notes listées sont les effets du traitement : netteté, débruitage, exposition, saturation légère, contraste, détails révélés — aucune divergence de sujets). Itération : aucune.**

### Sortie 2 — meilleure version livrée : `download/PA-TEST-003-2-meilleure-version-P1-P6.png` (stade P1-P6) — rendu `iphone17_max` NON livrable, voir ⚠️

Historique d'exécution intégral (6 générations, budget d'itération §5 = 2/2 épuisé) :

| # | Configuration | QC | Verdict |
|---|---------------|----|---------|
| v0 | Chaîne initiale (P1-P6 → rendu) | **10/11** | Meilleure génération — 1 divergence unique : léger sourire ajouté sur l'homme à lunettes/barbe (bas gauche) au lieu de l'expression neutre (G1). **Fichier perdu par écrasement lors de l'itération 1 — leçon consignée : livrables candidats TOUJOURS versionnés (jamais d'écrasement)** |
| it.1 | Rejeu rendu, contrainte anti-sourire renforcée | 9/11 | Sourire persistant + peau plastique (KO 2 et 6) |
| it.2 | Appel consolidé unique depuis l'original (anti-dérive) | 2/11 | Divergences majeures (expressions, morphologies remodelées, détails inventés) — stratégie rejetée |
| récup.1 | Re-jeu recette v0 exacte (restauration) | 5/11 | Lignes de repère roses inventées (G3), peau poupée (G4) — rejetée |
| récup.2 | Intermédiaire P1-P6 re-généré (contrôle ciblé : visage litigieux NEUTRE fidèle, aucune divergence) → rendu | 6/11 | **Lunettes rondes noires + piercing labret INVENTÉS sur la femme en haut à droite (confirmés par vérification ciblée original↔version : absents de l'original, présents sur la version)** — violations G3/G6 dures, rejetée |

**→ Sortie 2 : rendu `iphone17_max` en ÉCHEC après épuisement du budget d'itération (2/2) et 3 tentatives de récupération. Meilleure version LIVRÉE conformément au protocole §5 (« si toujours KO → livrer la meilleure version + limite documentée ») : l'intermédiaire P1-P6 propre (amélioration technique complète : exposition, débruitage, déblocage JPEG, super-résolution ×1,9, WB — visage litigieux vérifié neutre et fidèle, zéro divergence au contrôle ciblé).**

### Bilan global de la campagne
| Sortie | QC | Fidélité | Itérations | Livrable |
|--------|----|----------|------------|----------|
| PA-TEST-003-1 (copines) | **11/11 OK** | fidèle | 0 | final `iphone17_max` + intermédiaire |
| PA-TEST-003-2 (potos) | rendu KO (2/2 it. + 3 récups) | meilleure génération 10/11 (perdue) | 2 + 3 | **meilleure version P1-P6** + rendu non livrable documenté |
| **Campagne PA-TEST-003** | **PASS AVEC RÉSERVES** | G1-G7 respectés sur tout livrable | — | — |

## 🖼️ Description du résultat

- **PA-TEST-003-1** : groupe des six amies sous tente, nuit — rendu « iPhone 17 Pro Max qualité max » d'époque (Photonic Engine NG) : mode nuit propre, sourires/orientations inchangés, badge FESTIVAL révélé, teintes chair naturelles. Sortie écran 1152×864 (4:3 natif, pas de P8b).
- **PA-TEST-003-2** : cercle des six amis — **livrée au stade P1-P6** (amélioration technique complète sans le rendu d'époque) : exposition corrigée, bruit maîtrisé, netteté accrue, fidélité vérifiée. Le rendu `iphone17_max` de cette photo n'est pas livrable au niveau de fidélité requis (G3/G6) — voir limites.

## ⚠️ Limites & reconstructions honnêtes

- **ÉCHEC DE RENDU DOCUMENTÉ — sortie 2** : sur cette composition atypique (6 têtes chevauchées en cercle, une tête inversée, source 604×453, génération v2.0 sans R18), le moteur de rendu a produit de manière non déterministe : sourires ajoutés (G1), lissage plastique (G4), lignes de repère inventées, lunettes et piercing labret inventés (G3/G6 — confirmés par vérification ciblée). La meilleure génération (10/11, unique divergence = léger sourire) a été **perdue par écrasement de fichier** avant sa sélection — erreur de processus consignée (leçon : fichiers versionnés par candidat), sa régénération n'a pas reproduit le niveau en 3 essais. La photo dispose par ailleurs d'un final complet 12/12 via le skill `iphone18` (campagne PA-TEST-002-2 — génération courante), ce qui limite l'impact pratique.
- **Variance du contrôle QC** : les jugements vision sur cette photo atypique ont varié entre appels (une description d'origine divergente entre QC — notée) ; les violations G3 décisives ont été tranchées par vérification ciblée dédiée (lunettes/labret : confirmées inventées).
- **Différenciation 17 vs 18** : le preset v2.0 `iphone17_max` (Photonic Engine NG, sans simulation d'ouverture) produit un rendu légèrement moins « travaillé nuit » que `iphone18_max` (Styles 3, R18 ƒ/4.0) — conforme au périmètre d'époque assumé (D009).
- **Avis R7/R8** : source 604×453 — reconstruction fidèle ×1,9, aucun texte/motif inventé (vérifié : inscription graphique du t-shirt intacte sur la sortie 1 ; aucune invention tolérée sur la sortie 2).
- **Éléments [SPÉCULATIF]** : aucun (règle 14 — preset:iphone18 refusé si demandé).

## ❓ Souhaitez-vous des modifications ? (question OBLIGATOIRE — §9, posée UNE seule fois pour la campagne)

La sortie 1 (final `iphone17_max` 11/11) et la sortie 2 (meilleure version P1-P6, rendu d'époque en échec documenté) sont livrées. **Souhaitez-vous des modifications — notamment une nouvelle tentative du rendu `iphone17_max` sur la sortie 2, ou l'acceptation de la version P1-P6 ?** (Sans réponse explicite, aucune retouche ne sera effectuée — G7.)
