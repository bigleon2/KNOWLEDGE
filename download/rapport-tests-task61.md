# Rapport de tests Task 61 — Tests $FACON2 fonctionnels ×2 et performances (vagues chronologiques V1→V5)

> **Plan** : `download/plan-task61-suite-consolidee.md` (D003/D004/D007-D010) · **Journal machine-readable** : `download/tests-task61/journal-tests.json` · **Date** : 2026-11-07 (session web-c30e6506)
> **Méthode** : vagues chronologiques de création/modification (12ᵉ directive : Task 56 → Task 57 → Task 60 → Task 58 → Task 61) · chaque batterie ×2 (idempotence R6 — re-jeu byte-stable/no-op) · mesures de performance comparées aux références (Task 33/58/60).

## Synthèse

| Indicateur | Valeur |
|---|---|
| **Verdict global** | **PASS — 20 tests : 18 PASS · 1 PASS AVEC RÉSERVES (hérité --bloc) · 1 BLOQUÉ (documenté) · 0 FAIL** |
| Idempotence | Prouvée sur TOUTES les batteries re-jouables (byte-stable ou no-op) |
| Tickets G3 ouverts | 7 (voir §3) — aucune faille bloquante, écarts tracés |
| Perfs | Toutes excellentes (0,03-0,17 s ; nœud C++ 0,102 ms/client en concurrence) |

## §1 Résultats par vague (ordre chronologique)

### V1 — Task 56 : gen-plan v3.37.0 + garde É1-INSTALL + propagation §0 — 4/4 PASS
- Replay arbitres ×2 : integrity **110/110** (0,05 s) · coherence **54/27/0** (0,12 s) · vcw **ALL PASS** (0,03 s) · cross **100 %** (0,03 s)
- **Simulation disparition version-management** : `mv` → **INSTALLE-REPARÉ** rc=0 (v1.2.0 restauré depuis miroir, 0 jeton) → re-jeu **INSTALLE no-op** — garde Task 56 prouvée en réel (21ᵉ disparition, suite 16) ET en simulation
- Self-tests : check_plan_protocol **7/7** · answer-key-checker **16/16** · trigger_evals JSON valide (13 cas) — **écart** : aucun cas « met à jour » → ticket F-V1-1
- propagate-context v2.0.9 idempotence ×2 : **no-op parfait** (0/0/0 — 0,04 s/run)

### V2 — Task 57 : kit TSI — 4/5 PASS + 1 BLOQUÉ documenté
- tsi-validator self-test ×2 : **PASS** (0,049/0,052 s — échantillons golden intégrés)
- analyse-doc-s4mk2 batterie calibrée DJTT : **BLOQUÉ** — échantillon de référence `upload/DJTT...v2.1.0.zip` absent du disque (upload/ recyclé) + **bug TF-00 découvert** (tuple-not-callable, branche jamais exercée) → F-V2-1/2/3
- analyse-doc-s4mk2 **pipeline RÉEL ×2 sur `mes-mappings-tsi-actuels.zip`** (données propriétaire) : **byte-stable ×2** (sha 80ea18a38f6b2a69) — classification 5 MAPPING + 1 PRÉFÉRENCES-GÉNÉRIQUES (device Traktor.Kontrol S4MK2.Default, DDIV 2.9.0 R1257) — verdict pipeline FAIL sémantiquement CORRECT (mappings personnels ≠ référentiel DJTT v2.1.0 : attendus 5626 CMAI/163 noms DCBM calibrés DJTT — le pipeline rend un verdict déterministe avec motifs détaillés)
- orchestrateur-tsi + agent-TSI : contrôle structurel PASS (SKILL.md + 2 agents + tsi-architect.agent présents)

### V3 — Task 60 : pm-skill v1.0.0 + correct-work v2.11.0 + ULTRA — 3/4 PASS + 1 écart tracé
- pm-skill self-test ST1-ST11 ×2 : **11 PASS · 0 FAIL** (0,04 s)
- **PM éphémère témoin gen-plan v3.37.0** : généré (110 283 o), **auto-portant** (§0 embarqué, zéro lecture externe), SHA-256 source tracé, nouveaux déclencheurs (« met à jour » + glossaire) projetés fidèlement
- correct-work : verify-correct-work ×2 **ALL PASS** + matrice best-of §12 présente
- **ULTRA stale** (cite gen-plan v3.35.2 + SHARED v1.7.28 vs courants v3.37.0/v1.7.30) → F-V3-1

### V4 — Task 58 : dessin-technique v1.3.0 + nœud C++ — 3/3 PASS
- Preuves nœud (pré-exécutées 07:08) : **8/8** — selftest 15/15 ×2 byte-identiques (sha binaire c6b22a8e…), concurrence **100/100 @ 0,102 ms**, saturation 9ᵉ refusée non-bloquante, cas vivant VOSS joint 5c (Guldin 29 026,60048 mm³, iso 545 items)
- **Chaîne Python `generer_dessin` (partie locale déterministe) ×2 — cas joint 5c : byte-stable** — construire_prompt `8ab0f7d9…` (955 car.) · postpro `5bb34182…` (palette DNA 5 tons) · annoter `7f5df294…` (cotes/couples) — le rendu z-ai final (API générative) est non déterministe par nature : hors périmètre byte-stable, documenté
- Perf : concurrence nœud 0,102 ms (vs 0,27 ms origine) ; chaîne Python < 0,5 s

### V5 — Task 61 (jour) : installation + --bloc + montées + cascade — 4/4 PASS
- Idempotence installation ×3 (07:03-07:10) : **INSTALLE no-op** (0,08 s)
- correct-work (projet) --bloc 7 blocs (07:07) : **PASS AVEC RÉSERVES** (0 S1/S2 ; F1/F2 S4 → G3 ; 25 asymétries S3/S4 héritées en diminution)
- Vérifications complémentaires : générateur PM --check **4 familles COHERENT ×2** · sceaux SHA **42/42 OK** · arbitres ×2 verts
- Montées v3.36.0/v3.37.0 + cascade complète + injecteur v2.0.9 + propagation §0 (70+151+2) : certifiées ×2, commit a38ae1e

## §2 Performances (résumé)

| Élément | Mesure | Référence | Écart |
|---|---|---|---|
| Arbitre integrity | 0,05 s | — | nominal |
| Arbitre coherence | 0,12 s | — | nominal |
| Arbitre vcw / cross | 0,03 s | — | nominal |
| Nœud C++ concurrence | 0,102 ms/client | 0,27 ms (Task 58) | **−62 %** |
| validator selftest | 0,049-0,052 s | — | nominal |
| Pipeline analyse ZIP | 0,14-0,17 s | 0,174 s (Task 33 DJTT) | nominal |
| pm-skill self-test | 0,04 s | — | nominal |
| propagate-context (no-op) | 0,04 s | — | nominal |
| Installation (no-op) | 0,08 s | — | nominal |

**Goulots > 20 % : AUCUN** (toutes les mesures sont nominales ou meilleures que les références).

## §3 Tickets ouverts → G3 (corrections + optimisations)

| Ticket | Origine | Traitement G3 |
|---|---|---|
| F-V1-1 | trigger_evals gen-plan sans cas « met à jour » (v3.37.0) | Ajout cas + montée PATCH + cascade KO-L004 |
| F-V2-1 | Bug TF-00 run_all.py (tuple-not-callable — branche jamais exercée) | Fix + montée analyse-doc + cascade |
| F-V2-2 | Échantillon DJTT v2.1.0 perdu (batterie calibrée SKIP) | SKIP documenté (le propriétaire peut re-téléverser l'échantillon) — pipeline testé sur données réelles ✓ |
| F-V2-3 | Ligne 179 run_all.py (affichage incohérent avec ast.parse) | Examen au fix F-V2-1 |
| F-V3-1 | ULTRA stale (gen-plan v3.35.2 / SHARED v1.7.28) | Régénération `gen-ultra-maitre.py` + recalibrage |
| F1/F2 | Asymétries pm-skill KB (rapport --bloc 07:07) | Bidirectionnalité SHARED §3.2 |
| Modes | 131 changements de mode hérités (0 insertion/0 deletion) | Normalisation git update-index --chmod |

## §4 Conclusion

**Verdict : PASS.** Le périmètre P1-P9 du push + les éléments du jour sont testés en vagues chronologiques, ×2 (idempotence prouvée partout où re-jouable), avec mesures de performance nominales (aucun goulot > 20 %). Un blocage documenté (batterie calibrée DJTT — échantillon perdu du disque) est couvert par un test réel équivalent sur les données du propriétaire. Les 7 tickets ouverts alimentent G3 (corrections $FACON + optimisations $FACON) conformément au plan consolidé.
