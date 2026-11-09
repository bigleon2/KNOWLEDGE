# Référentiel G2 — format réel des TSI de mapping S4 MK2

**Provenance** : Task 7 G2 (2026-10-30, analyse ZIP DJTT v2.1.0) · **Erratum** : Task 33 (2026-11-01/02, diag-cmad2 + diag-illisibles, motifs BE/LE)
**Arbitre** : `scripts/analyser_tsi_mk2.py` v1.0.0 (self-test PASS ×2 byte-stable)

## 1. Encapsulation

```
NIXML (racine réelle Traktor — PAS NISYSTEM)
└── Entry Name="DeviceIO.Config.Controller"  ← le blob est dans l'ATTRIBUT Value (Base64), PAS dans le texte
    └─ Base64 → blob DIOM
```

Pièges : (a) racine `NIXML` contre `NISYSTEM` écosystème (cf. écart validator, doc approfondie §7) ; (b) `Value` est un **attribut** — `Entry.text` est vide.

## 2. Trames FourCC (big-endian intégral)

`DIOM → DIOI → DEVS → DEVI → DDAT → (DDDC → DDCI/DDCO × DCDT ; DDCB → DDCO/CMAS → CMAI × (CMAD embarqué) ; DCBM) → CMAI(CMAD) → DCBM`

- Chaque trame : FourCC (4 o) + u32 taille (4 o) + payload.
- Chaînes : `[u32 n][n × 2 octets]` UTF-16-BE.
- **CMAI** : payload = `[u32 ordinal][u32 drapeau][u32 ref-cid-DCBM]` puis trame **CMAD embarquée** à +12 (FourCC @+12, taille @+16, payload @+20). Le `ref` référence un **cid DCBM** (contrôle sollicité), PAS une condition.
- **CMAD** : layout validé : type @+0 (du payload), u32 @+4, u32 @+8, deck @+12, floats @+24/+28/+32, longueur nom @+48, nom UTF-16BE @+52 (localisation mécanique par scan 4-aligné fiable dans tous les cas).
- **DCBM** : 5 626 définitions, **cid tous distincts**, mais seulement **163 noms** — chaque contrôle est redéfini ~34× selon le contexte Traktor ; `controles_distincts` se compte par NOMS.

## 3. Comptes de référence (échantillon DJTT v2.1.0)

| Compte | Valeur | Erratum Task 33 |
| --- | ---: | --- |
| DEVI | 1 | — |
| DCDT in / out / total | 125 / 220 / 345 | — |
| CMAI = CMAD lus = DCBM | 5 626 | — |
| noms de commandes lisibles | 4 960 (88,17 %) | G2 publié 4 970 (88,3 %) : les 666 CMAD de 120 o n'ont AUCUN champ nom (vérifié à tous les offsets) — +10 non reproductibles (décodeur perdu) |
| CMAD illisibles | 666 (11,83 %) | — |
| commandes distinctes | 393 | G2 publié 394 : +1 non reproductible |
| refs résolues / non résolues | 5 136 / 490 | — |
| noms DCBM distincts | 163 | — |
| contrôles réellement sollicités | 49 | — |

## 4. Limites documentées

- Lien CMAI ↔ condition (quel DCDT conditionne quelle assignation) : **non décodé** ; candidat « index de condition » dans le payload CMAD autour des offsets @44 (31 valeurs) / @48 (42 valeurs) — hypothèse qualifiée, non conclusive.
- `Status.Effect 4 Select` absent du FX Settings.tsi (constat brut, interprétation refusée).
- Le validateur écosystème (`tsi-validator` E1) attend la racine `NISYSTEM` : il rejette les TSI réels — recommandation d'évolution consignée, non appliquée.
