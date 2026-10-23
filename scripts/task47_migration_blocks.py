"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 47 — D3 : blocs de contenu nouveau pour la migration ANTICIPÉE iphone18 → iphone19.
Chaque bloc remplace une section précise du PM source (assertion count==1 côté générateur)."""

TITRE_DOC = "# 📱 iphone19-photos.md"
TITRE_PM = ("## PROMPT MAÎTRE — Pipeline d'amélioration photo « iPhone 19 Pro Max, qualité max » "
            "(génération ANTICIPÉE 2027) + rendus d'époques + posters")
VERSION = ("**Version 0.9.0 [ANTICIPÉE] — Langue : français — Mode : data-driven "
           "(Analyse → Décision → Plan → Exécution → QC → Question utilisateur)**")

ORIGINE = ("> **Origine v0.9.0 (migration ANTICIPÉE — prompt maître `iphone-photos-migration.md`, "
           "déviation §6-1 documentée) :** document généré par migration depuis `iphone18-photos.md` v1.0 "
           "le 2026-10-20, sur **directive propriétaire explicite** (« fais cette migration de façon autonome ») "
           "— le squelette §6.10 de la source est consommé **avant la confirmation officielle Apple** "
           "(génération 19 non confirmée au 2026-10-20 ; keynote attendu sept. 2027). Version **0.9.0** "
           "(et non 1.0) : v1.0 est réservé à la génération confirmée — à la confirmation officielle, "
           "bump v1.0.0 + re-ancrage des spécifications (règle d'activation §6.10 du présent document).")

CHANGELOG = """### Changelog `iphone18-photos.md` v1.0 → `iphone19-photos.md` v0.9.0
| Zone | Modification | Fondement |
|---|---|---|
| En-tête | Nouveau document `iphone19-photos.md` — titre + cible « iPhone 19 Pro Max » (ANTICIPÉ 2027) + version **0.9.0 [ANTICIPÉE]** (déviation §6-1 : pas de reset 1.0 — génération non confirmée) | Directive propriétaire 2026-10-20 (migration autonome) — `rumeur` |
| §0 | Cible re-ancrée « iPhone 19 Pro Max (génération ANTICIPÉE) » + contexte matériel **extrapolé** (A21 Pro, Photonic Engine NG+, Face ID sous écran — tous [RUMEUR], aucun confirmé) | Macworld / MacRumors / AppleInsider / The Information / Kuo (2026) — `rumeur` |
| §1 (C3) | Défaut rendu cible → `iphone19_max` | Propagation preset (contrainte 5.2) |
| §2 | **Aucune nouvelle règle** — R1–R18 intacts ; R13 : renommage du preset référencé `iphone18_max` → `iphone19_max` (contrainte 5.2 — renommage global, logique inchangée) | Honnêteté (règle 14) + propagation |
| §3 | Défaut `rendu_cible: iphone19_max` | Propagation |
| §6.1 | Preset par défaut renommé **`iphone19_max`** — recalibrage **ANTICIPÉ** (extrapolation de la baseline confirmée 18 + delta rumeurs ; **aucun calibrage labo** — génération non sortie) + limites honnêtes renforcées | `rumeur` + extrapolation |
| §6.5 | Renommage preset de restauration `iphone18_max` → `iphone19_max` (propagation 5.2, logique inchangée) | Propagation |
| §6.9 | Référence génération → « caméra frontale iPhone 19 Pro Max » (caractéristiques anticipées inchangées : 18 MP, ƒ/1.9, Center Stage ; caméra sous écran [RUMEUR], sans effet rendu statique) | `rumeur` |
| §6.10 | Squelette `iphone19` **consommé** par la présente v0.9.0 (directive propriétaire — activation ANTICIPÉE documentée) + nouveau squelette `iphone20` — **INACTIF, 100 % [SPÉCULATIF]** + règle d'activation de la migration de CONFIRMATION (bump v1.0.0) | `rumeur` — structure conditionnelle (règle 14) |
| §11 | Note rétroactive v0.9.0 | — |
| §12 | Livrables actualisés : v0.9.0 présente ; `iphone18-photos.md` v1.0 **demeure le PM de la génération CONFIRMÉE** (référence de calibrage — archivage prévu à la confirmation génération 19, PAS avant) | Honnêteté |
| §13 | `preset:iphone19` / `preset:iphone19_max` acceptés (nouveau défaut) ; `preset:iphone20` → refus (règle 14) | Propagation |

**Invariants garantis : aucune règle R1–R18 modifiée ni affaiblie (aucune règle R19 — aucune capacité fonctionnelle confirmée) ; garde-fous G1–G7 et inventaire B6 strictement intacts ; critères QC 1–12 inchangés ; règles absolues 1–13 inchangées, règle 14 maintenue et généralisée au squelette `iphone20`. Écarts vs migration standard, tous documentés : versionnement 0.9.0 (anticipation), §12 sans archivage du PM génération 18, calibration §6.1 extrapolée (jamais mesurée labo).**"""

CIBLE_S0 = "(cible : **iPhone 19 Pro Max, réglages photo au maximum** — génération ANTICIPÉE 2027)"

CONTEXTE_MATERIEL = ("**Contexte matériel de référence** (ancrage v0.9.0 — **ANTICIPÉ, tous éléments "
 "[RUMEUR]/extrapolation, aucun confirmé au 2026-10-20**) : système photo **triple 48 MP Fusion** "
 "(structure génération 18 présumée conservée : principal 24 mm à ouverture variable ƒ/1.48–ƒ/4.0 ; "
 "ultra-grand-angle 13 mm ; téléobjectif jusqu'à 200 mm), **Photonic Engine nouvelle génération** "
 "[EXTRAPOLATION], **Photographic Styles 3** (contrôles texture et grain), puce **A21 Pro** "
 "[RUMEUR — Macworld, oct. 2026] à Neural Engine accru, **Face ID sous écran** "
 "[RUMEUR — The Information/Kuo, readiness 2027 incertaine selon Ross Young/DSCC], design tout-verre "
 "quad-courbe 20e anniversaire [RUMEUR — MacRumors 2026]. Ce contexte **extrapolé** calibre le rendu du "
 "preset par défaut (§6.1) comme une anticipation prudente de la baseline confirmée iPhone 18 Pro Max ; "
 "il ne déclenche aucune règle fonctionnelle propre, et sera **re-ancré à la confirmation officielle** "
 "(bump v1.0.0 — §6.10). *(Capacité d'authenticité « Apple Reference Image » — signature matérielle des "
 "pixels : non simulée, hors périmètre de rendu. Téléobjectif 200 MP [NON VÉRIFIÉ — rumeur unique, non "
 "intégré].)*")

REGLE14 = ("14. **ÉLÉMENTS SPÉCULATIFS** : toute section taggée `[SPÉCULATIF]` (ex. §6.10 — squelette "
           "`iphone20`) est **inactive** — elle ne déclenche jamais de traitement, ne fournit jamais de "
           "valeur par défaut, et n'est jamais appliquée aux images.")

SECTION_61 = """### 6.1 `iphone19_max` (défaut — ancrage matériel ANTICIPÉ iPhone 19 Pro Max [2027])
**Baseline de référence (v0.9.0 — ANTICIPÉE) :** structure photo génération 18 confirmée (triple 48 MP Fusion, principal 24 mm ouverture variable ƒ/1.48–ƒ/4.0 — 6 lames, 4 réglages auto/manuel ; télé 4x/8x 200 mm ; capteur sensor-shift 2e génération 100 % Focus Pixels ; Photographic Styles 3) **+ delta rumeuré génération 19** : puce **A21 Pro** [RUMEUR] à puissance neurale accrue pour la photo computationnelle, **Photonic Engine nouvelle génération** [EXTRAPOLATION]. Aucune spécification officielle n'existe au 2026-10-20 — la calibration est une **extrapolation**, jamais un calibrage labo.
**Rendu simulé (calibrage ANTICIPÉ — extrapolation de la baseline confirmée 18, cf. §6.1 de `iphone18-photos.md` v1.0) :** rendu `iphone18_max` poussé d'un cran cohérent avec le delta matériel rumeuré — netteté max sur les zones utiles (visages prioritaires), piqué accru, dynamique étendue sans HDR visible, colorimétrie naturelle et teintes chair fidèles, mode nuit encore plus propre (ouverture auto ƒ/1.48, bruit maîtrisé, sources lumineuses sans halo), texture/bruit équilibré (texture naturelle sans lissage excessif — jamais plastique, G4), groupes nets de l'avant à l'arrière (fermeture ƒ/4.0 — R18), textures réalistes (peau, tissu, matière).
**Limites honnêtes (statut ANTICIPÉ — renforcées) :** calibration extrapolée, **jamais mesurée en labo** (aucun calibrage DXOMARK possible sur génération non sortie) ; spécifications non confirmées (rumeurs 2026 — A21 Pro, Face ID sous écran, quad-courbe) ; rumeurs non-photo (écran, Face ID) sans effet sur le rendu d'image statique ; téléobjectif 200 MP [NON VÉRIFIÉ — rumeur unique Digital Chat Station, mars 2026] **non intégré** (PM migration §4.4 : source unique non qualifiée → citation en contexte seul, aucune règle fonctionnelle) ; le pipeline ne sur-promet pas — le rendu v0.9.0 est une anticipation prudente, à re-ancrer à la confirmation officielle.
*(Périmètre : images statiques — les capacités vidéo ne sont pas simulées.)*"""

SECTION_69 = """### 6.9 `frontal_center_stage` (caméra frontale 18 MP Center Stage)
- Simulation du rendu **caméra frontale iPhone 19 Pro Max** (18 MP, ƒ/1.9, Center Stage — caractéristiques anticipées inchangées vs génération 18 ; caméra frontale sous écran [RUMEUR — NON VÉRIFIÉ, sans effet sur le rendu statique]) : recadrage **carré 1:1** centré sur le(s) sujet(s) (bbox visages/corps, adaptatif façon Center Stage), rendu grand-angle frontal léger, piqué doux optimisé visage, exposition prioritaire aux visages."""

SECTION_610 = """### 6.10 `iphone20` — **[SPÉCULATIF] — SECTION INACTIVE**
> **Statut : génération non confirmée.** Cette section est un **squelette conditionnel** : elle ne contient volontairement **aucune spécification**, ne fournit **aucune valeur par défaut**, et ne déclenche **jamais** de traitement. Toute activation prématurée de son contenu violerait la règle 14.

- **Statut de la génération 19 (présent document) : ANTICIPÉE.** Le présent document v0.9.0 a été produit par migration ANTICIPÉE depuis `iphone18-photos.md` v1.0 (directive propriétaire 2026-10-20) — le squelette `iphone19` de la source est **consommé** sans que la règle d'activation officielle soit remplie (génération 19 non confirmée au 2026-10-20).
- **Règle d'activation (migration de CONFIRMATION génération 19) :** à la confirmation officielle par Apple (keynote / page produit — attendu sept. 2027), exécuter le prompt maître `iphone-photos-migration.md` (recherche web qualifiée, Phase 2) → **bump v1.0.0 (reset)** + re-ancrage §0/§6.1 des spécifications confirmées + nouvelles règles R19+ si capacités fonctionnelles confirmées (propagation §3/§5/§8) + archivage de `iphone18-photos.md` v1.0 (§12).
- **Squelette `iphone20` :** structure conditionnelle vide — INACTIVE (règle 14), même mécanique que les squelettes `iphone18`/`iphone19` avant elle.
- **En attendant :** la calibration v0.9.0 (extrapolation rumeurs 2026) demeure celle du preset par défaut `iphone19_max` (§6.1) — la génération 18 confirmée reste servie par `iphone18-photos.md` v1.0 (PM parallèle).
- **Archivage :** le squelette `iphone19` (§6.10 de `iphone18-photos.md` v1.0) est consommé par la présente v0.9.0 le 2026-10-20 (directive propriétaire — activation ANTICIPÉE documentée, déviation §6-1 assumée)."""

NOTE_RETRO_090 = ("**Note rétroactive v0.9.0 :** les intégrations (renommages de preset `iphone18_max` → "
 "`iphone19_max` — contrainte 5.2 ; re-ancrage ANTICIPÉ §0/§6.1 ; squelette §6.10 `iphone20` ; référence "
 "§6.9) sont des **ajouts purs ou renommages propagés** — aucune règle R1–R18, aucun critère QC 1–12, "
 "aucun garde-fou G1–G7 n'a été modifié ni affaibli ; aucun QC antérieur n'est requalifié. Aucune règle "
 "R19 : aucune capacité fonctionnelle confirmée (règle 14).")

SECTION_12 = """## §12 — LIVRABLES DU PROJET

- `iphone19-photos.md` — le présent prompt maître (**v0.9.0 [ANTICIPÉE]** — produit par migration ANTICIPÉE depuis la v1.0 génération 18, directive propriétaire 2026-10-20) ;
- `iphone18-photos.md` — prompt maître de la **génération CONFIRMÉE courante** (**v1.0** — demeure la référence de calibrage mesurée ; archivage prévu à la confirmation officielle de la génération 19, PAS avant) ;
- `iphone17-photos.md` — prompt maître **archivé (v2.0** — génération 17 ; ayant activé la migration génération 18 via sa §6.10) ;
- `crop_utils.py` — post-recadrage P8b (`crop_ratio`, `export_print`) — inchangé ;
- `iphone-photos-migration.md` — prompt maître de migration générationnelle (réutilisable — a produit la présente v0.9.0 en mode ANTICIPÉ, déviation §6-1 documentée) ;
- **Livrables historiques du projet CLUB** (générés sous v1.x/v2.0, non régénérés) : PA-CLUB-001 (`iphone17_max`), PA-CLUB-002/003 (1:1 gauche + 16:9), PA-CLUB-004/005 (1:1 droite + 16:9 gros plan), PA-CLUB-006 (poster A4 focalisé), PA-CLUB-007 (variante `chaud`, cible A4) ;
- Scripts PIL historiques consolidés dans `crop_utils.py`."""

LIGNE_PRESET_13 = ("| `preset:<nom> [params]` | Exécute un preset §6 sur l'image courante (mode série §10 "
 "si plusieurs sorties) — y compris `log2_cinema`, `frontal_center_stage` ; `preset:iphone19` / "
 "`preset:iphone19_max` → preset par défaut (§6.1) ; **`preset:iphone20` → refus, section inactive "
 "(règle 14)** ; `preset:iphone18` / `preset:iphone18_max` → servie par le PM génération 18 confirmé "
 "(`iphone18-photos.md` v1.0, PM parallèle) |")
