# Lignage & changelogs — iphone17 (blocs archivés R4)

> **Provenance** : skill `iphone17` · sections « Lignage — projection skill ← prompt maître source », « PROMPT MAÎTRE — … » (intro), « Changelog v2.0 → v2.1 » et « Changelog v1.4 → v2.0 » (bloc historique cohérent regroupé — analogue Task 82 iphone18 changelogs-versions.md) · déplacées R4 byte-identité vers `references/` le 2026-11-09 (Task 85 G5, re-curation progressive disclosure — protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)) · **SHA-256 du bloc : `22e908eb009323be…`** · le PM source intégral demeure `skills/@photos/iphone17-photos.md` v2.1 [COURANT — R2 byte-identique, jamais édité] et le skill intégral demeure `skills/iphone17/SKILL.md`.

## Lignage — projection skill ← prompt maître source

> Skill métier projeté depuis le prompt maître `skills/@photos/iphone17-photos.md` **v2.1** (génération 17 — ARCHIVÉE au plan générationnel, supersédée par iphone18 [règle §6.10 activée, keynote 9/9/2026] ; le pipeline reste opérationnel pour un rendu génération 17 demandé explicitement ; v2.1 : extension 1944 — chemin argentique N&B années 1930-1950, grain préservé, aucune colorisation inventée ; v2.0 archivée @historique/photos/) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). Tests empiriques de référence : PA-TEST-003 (2 photos — sortie 1 QC 11/11) + PA-TEST-004 (nouvelle tentative « les potos » — QC arbitré haute confiance, zéro retouche). P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).

## PROMPT MAÎTRE — Pipeline d'amélioration photo « iPhone 17 Pro Max, qualité max » + rendus d'époques + posters
**Version 2.1 — Langue : français — Mode : data-driven (Analyse → Décision → Plan → Exécution → QC → Question utilisateur)**

> **Origine v2.1 (extension 1944 — directive propriétaire 2026-10-21) :** renforcement du chemin « restauration de photos anciennes » pour les **photographies argentiques N&B des années 1930-1950** (directive : « fais en sorte que mes skills puissent effectuer un traitement fonctionnel et optimisé sur les photos prises en 1944 ») — **ajout pur** : note d'analyse §1 (grain argentique ≠ bruit numérique, monochrome natif), ère **40s** dans la table §6.5, extension §6.6 (grain préservé par défaut, tonalité restaurée, dégâts d'époque, aucune colorisation inventée — G3). Aucune règle R1–R17, aucun garde-fou G1–G7, aucun critère QC 1–11 modifié.

### Changelog v2.0 → v2.1 (extension 1944)
| Zone | Modification | Fondement |
|---|---|---|
| En-tête | Version **2.1** + origine v2.1 (bloc ci-dessus) | Directive propriétaire 2026-10-21 (photos de 1944) |
| §0 | Rendus d'époque étendus « années 40 → 2010 » + restauration « photographies argentiques N&B années 1930-1950 — grain préservé, aucune colorisation inventée » | Ajout pur |
| §1 | Note années 1940 après l'axe contextuel (grain argentique authentique vs bruit, dégâts physiques, tonalité délavée, monochrome natif) | Ajout pur |
| §6.5 | Ère **40s** ajoutée en tête de la table (simulation + restauration argentiques N&B) | Ajout pur |
| §6.6 | Extension « années 1930-1950 » du chemin `restauration_scan` | Ajout pur |
| §8 | Avis grain/tonalité (sources argentiques N&B) dans les limites honnêtes | Propagation |
| §11 | Note rétroactive v2.1 | §11 |
| §12 | Présent PM v2.1 ; v2.0 archivée `@historique/photos/` | Hygiène R4 |

### Changelog v1.4 → v2.0
| Zone | Modification | Fondement |
|---|---|---|
| §0 | Cible explicite « iPhone 17 Pro Max » + contexte matériel (A19 Pro, chambre à vapeur) + simulation de focales | Keynote Apple — `confirmé` |
| §1 (C3) | Champ « focale équivalente demandée » | Propagation R17 |
| §2 | Nouvelle règle **R17** (focales équivalentes 13–200 mm) | `confirmé` |
| §3 | Champ YAML `focale_cible` + nouvelles valeurs `rendu_cible` | Propagation R17 |
| §4 (P8) | Vocabulaire des focales équivalentes | `confirmé` |
| §5 | Nouveau critère QC **11** (focale respectée) | Propagation R17 |
| §6.1 | Preset par défaut redéfini — ancrage matériel triple 48 MP Fusion + Photonic Engine NG | `confirmé` (détails ISP : `[INCERTAIN]`) |
| §6.8 | Nouveau preset `log2_cinema` (Apple Log 2 — mode SIMULATION) | `confirmé` |
| §6.9 | Nouveau preset `frontal_center_stage` (caméra frontale 18 MP) | `confirmé` |
| §6.10 | Squelette `iphone18` — **INACTIF, 100 % [SPÉCULATIF]**, activation conditionnelle | `rumeur` — consentement utilisateur (option H) |
| §8 | Rapport : mention focale + éléments spéculatifs éventuels | Propagation |
| §11 | Note rétroactive v2.0 | — |
| §12 | v2.0 ajoutée ; entrées PA-CLUB requalifiées « historiques projet » | Hygiène |

**Invariants garantis : aucune règle R1–R16 modifiée ni affaiblie ; garde-fous G1–G7 et inventaire B6 strictement intacts.**

---

