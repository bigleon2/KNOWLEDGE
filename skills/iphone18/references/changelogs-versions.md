# Origines + changelogs versionnés v2.0 → v1.1 — iphone18 (bloc archivé R4)

> **Provenance** : skill `iphone18` v1.1.0 · section « en-tête PROMPT MAÎTRE — origines, tables changelog + invariants » · déplacé R4 byte-identité vers `references/` le 2026-11-09 (Task 82 G6, re-curation progressive disclosure — protocole re-curation v1.2.2, méthode moves-r4-pur arbitrée --compare (P2)) · **SHA-256 du bloc : `ec0cd7fefe513dd250d1f790e5d8c3b23b2787a68f1376b0c002eb63e412c7fc`** · le PM intégral de référence demeure `skills/@photos/iphone18-photos.md` v1.1 [COURANT — génération iPhone 18 CONFIRMÉE] — jamais édité (R2).

> **Origine v1.0 (reset de version — prompt maître `iphone-photos-migration.md` §6-1) :** document généré par migration depuis `iphone17-photos.md` v2.0 le 2026-10-09, à l'activation de la règle §6.10 de cette dernière (génération iPhone 18 confirmée par Apple le 9/9/2026).

> **Origine v1.1 (extension 1944 — directive propriétaire 2026-10-21) :** renforcement du chemin « restauration de photos anciennes » pour les **photographies argentiques N&B des années 1930-1950** (directive : « fais en sorte que mes skills puissent effectuer un traitement fonctionnel et optimisé sur les photos prises en 1944 ») — **ajout pur** : note d'analyse §1 (grain argentique ≠ bruit numérique, monochrome natif), ère **40s** dans la table §6.5, extension §6.6 (grain préservé par défaut, tonalité restaurée, dégâts d'époque, aucune colorisation inventée — G3). Aucune règle R1–R18, aucun garde-fou G1–G7, aucun critère QC 1–12 modifié.

### Changelog `iphone18-photos.md` v1.0 → v1.1 (extension 1944)
| Zone | Modification | Fondement |
|---|---|---|
| En-tête | Version **1.1** + origine v1.1 (bloc ci-dessus) | Directive propriétaire 2026-10-21 (photos de 1944) |
| §0 | Rendus d'époque étendus « années 40 → 2010 » + restauration « photographies argentiques N&B années 1930-1950 — grain préservé, aucune colorisation inventée » | Ajout pur |
| §1 | Note années 1940 après l'axe contextuel (grain argentique authentique vs bruit, dégâts physiques, tonalité délavée, monochrome natif) | Ajout pur |
| §6.5 | Ère **40s** ajoutée en tête de la table (simulation + restauration argentiques N&B) | Ajout pur |
| §6.6 | Extension « années 1930-1950 » du chemin `restauration_scan` | Ajout pur |
| §8 | Avis grain/tonalité (sources argentiques N&B) dans les limites honnêtes | Propagation |
| §11 | Note rétroactive v1.1 | §11 |
| §12 | Présent PM v1.1 ; v1.0 archivée `@historique/photos/` | Hygiène R4 |

### Changelog `iphone17-photos.md` v2.0 → `iphone18-photos.md` v1.0
| Zone | Modification | Fondement |
|---|---|---|
| En-tête | Nouveau document `iphone18-photos.md` — titre + cible « iPhone 18 Pro Max » + version **1.0** (reset) | Prompt maître migration §6-1 ; keynote Apple — `confirmé` |
| §0 | Cible re-ancrée « iPhone 18 Pro Max » + contexte matériel (A20 Pro, Dual Neural Engine 32 cœurs, ouverture variable ƒ/1.48–ƒ/4.0, capteur/ISP nouveaux) + capacité texture-grain (Styles 3) + simulation d'ouverture | Apple Newsroom + Specs — `confirmé` |
| §1 (C3) | Défaut rendu cible → `iphone18_max` + champ « ouverture demandée » | Propagation preset + R18 |
| §2 | Nouvelle règle **R18** (ouverture variable simulée ƒ/1.48–ƒ/4.0) ; **R13** : renommage du preset référencé `iphone17_max` → `iphone18_max` (contrainte 5.2 — renommage global, logique inchangée) ; **R17** : correction de coquille typographique de la source (« pitié » → « piqué » source insuffisant — logique inchangée) | `confirmé` + propagation |
| §3 | Champ YAML `ouverture_cible` + `regles_declenchees` jusqu'à R18 + défaut `rendu_cible: iphone18_max` | Propagation R18 |
| §4 (P5/P6) | Note texture/grain — Photographic Styles 3 | Apple Newsroom + Specs — `confirmé` |
| §5 | Nouveau critère QC **12** (ouverture simulée) | Propagation R18 |
| §6.1 | Preset par défaut renommé **`iphone18_max`** — re-ancrage capteur/ISP + calibrage labo DXOMARK (172 pts, nuit 150) + limites honnêtes + périmètre images statiques | `confirmé` |
| §6.5 | Renommage preset de restauration `iphone17_max` → `iphone18_max` (propagation 5.2, logique inchangée) | Propagation |
| §6.9 | Référence génération → « caméra frontale iPhone 18 Pro Max » (caractéristiques inchangées : 18 MP, ƒ/1.9, Center Stage) | Apple Specs — `confirmé` |
| §6.10 | Squelette `iphone18` **archivé** (règle d'activation remplie le 9/9/2026) + nouveau squelette `iphone19` — **INACTIF, 100 % [SPÉCULATIF]** | `rumeur` — structure conditionnelle (règle 14) |
| §7 | Ligne d'expression opérationnelle de R18 dans l'instruction consolidée (ajout pur) | Propagation R18 |
| §8 | Rapport : mention `ouverture_cible` + avis R18 | Propagation |
| §11 | Note rétroactive v1.0 | — |
| §12 | Livrables actualisés : v1.0 présente, `iphone17-photos.md` v2.0 archivée | Hygiène |
| §13 | `preset:iphone18` / `preset:iphone18_max` acceptés (nouveau défaut) ; `preset:iphone19` → refus (règle 14) | Propagation |

**Invariants garantis : aucune règle R1–R17 modifiée ni affaiblie (ajout pur R18 ; renommages de preset propagés conformément à la contrainte 5.2 du prompt maître migration et correction de coquille typographique R17 documentée — logique inchangée) ; garde-fous G1–G7 et inventaire B6 strictement intacts ; critères QC 1–11 inchangés (ajout pur 12) ; règles absolues 1–13 inchangées, règle 14 maintenue et généralisée au squelette `iphone19`.**

---

