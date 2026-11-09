# Rapport de livraison — Recalibrage triggers traduction-zh-fr v1.3.1 (F-2)

**Directive** : `gen-plan : "GO"` (trace 1a19749ed0a1575d, session web-4f989063, 2026-11-01) — application de la correction F-2 proposée par correct-work Task 28 (verdict PASS AVEC RÉSERVES).
**Périmètre GO** : F-2 uniquement — dérive triggers `traduction-zh-fr` v1.3.0 (replay 6/8).
**Mode** : gen-plan (mode NULL) — décisions D001-D009, cascade KO-L004, replay arbitres.

---

## 1. Défaut constaté (Task 28)

| Cas trigger_evals | Attendu | Constat replay | Nature |
|---|---|---|---|
| n°5 « Traduis la documentation chinoise du référentiel en anglais avec le même outil » | trigger | non-trigger (0 hit) | **faux négatif** — l'axe `--src zh --dest en` est pourtant supporté depuis v1.2.0 |
| n°7 « Résume ce vidéo YouTube en chinois sans traduction » | non-trigger | trigger (2 hits : chinois + traduction) | **faux positif** — « sans traduction » = hors périmètre |

Cause racine du faux négatif : l'inflexion `chinoise` → stem `chinois` ne matche pas le radical du tag `chinois` → `chinoi` (stemmer SHARED §7 v2 appliqué aux deux côtés, asymétrie d'inflexion) ; la requête ne partage alors aucun second radical avec les keywords du skill.

## 2. Corrections appliquées

| # | Décision | Détail |
|---|---|---|
| D001 | **Veto négatif** | case 7 : `exclusifs: ["sans traduction"]` — mécanisme V6.1 existant (Task 30), veto AVANT scoring, source `veto-exclusif` |
| D002 | **Keywords** | tags SKILL += `anglais`, `documentation`, `referentiel` — la requête n°5 atteint ≥ 2 radicaux partagés (`document`, `anglais`, `referent`) |
| D003 | **Version** | 1.3.0 → **1.3.1** (PATCH sémantique — zéro changement fonctionnel des scripts) + section « Recalibrage v1.3.1 » au SKILL |
| D004 | **KB** | en-tête `## traduction-zh-fr v1.3.1` + phrase de calibration v1.3.1 |
| D005 | **Pin** | `ECO_SKILLS["traduction-zh-fr"] = "1.3.1"` dans `check-ecosysteme-integrity.py` (hôte + dépôt byte-identiques `967c8887`) |
| D006 | **Replay ×2** | TZF 8/8 ×2 hôte + ×2 dépôt (voir §3) |
| D007 | **Cascade** | verify-cross 100 % ; integrity 86/86 ×2 ; archive v2.3 re-scellée + sync hôte→dépôt |
| D008 | **Non-régression** | description frontmatter INCHANGÉE (md5) ; cas négatifs n°6 (veto allemand) et n°8 re-vérifiés au replay |
| D009 | **Traçabilité** | worklog Task 29 + présent rapport + commit pathspec strict (push = propriétaire, KO-L009 point 5) |

## 3. Preuves mécaniques

| Arbitre | Dépôt (canonique) | Hôte |
|---|---|---|
| check-triggers-replay ×2 | **PASS 827/827** ×2 — TZF **8/8** | TZF **8/8** ×2 — global 478/483 (voir §4) |
| verify-cross | 100 %, 0 erreur | — |
| check-ecosysteme-integrity ×2 | **86/86 PASS** | **86/86 PASS** |
| Archive v2.3 | re-scellée, corpus 9/9 + piliers 6/6 byte-identiques, round-trip vérifié ; sync hôte→dépôt sha256 `c43659b41ce9` | idem |
| Byte-identité hôte↔dépôt | OK ×4 fichiers édités (`fa9e7c42`, `27fd7329`, `0b28037e`, `967c8887`) | idem |

## 4. Constats hérités (hors périmètre GO — consignés, non corrigés)

1. **5 dérives triggers famille TSI (hôte-seulement)** : `midi-doc-expert` ×1, `tsi-architect` ×2, `tsi-validator` ×2 — les `trigger_evals.json` de ces 3 skills existent sur l'hôte (variantes plateforme) et sont ABSENTS du dépôt canonique (d'où le dépôt PASS 827/827). Résorption possible sur GO ultérieur : recalibrage identique (vetos exclusifs / keywords) sur les copies hôte, ou décision de rapatrier ces evals au dépôt.
2. **F-1 matérialisé à nouveau** : `version-management` a disparu de l'hôte entre deux messages (réserve ① « volatilité skills/ hôte » de Task 28) — réinstallé depuis le dépôt, byte-identique. Le hook Règle 4 (`auto-install-ecosysteme.py`, commit 48f2298) reste la parade recommandée à chaque ouverture de session.
3. **Disque 86 % (1,4 Go libre)** — G-RES CRITIQUE récurrent, surveillance maintenue (F-3 Task 28).

## 5. État final

- `traduction-zh-fr` **v1.3.1** — triggers 8/8, fonctionnalité inchangée (PATCH).
- Dépôt : commit pathspec strict (SKILL TZF, trigger_evals TZF, KB, arbitre integrity, archive v2.3, rapport replay, manifeste integrity, worklog Task 29) — **push origin/main = propriétaire**.
- Chantier F-2 **clos** ; restent ouverts : dérives TSI (GO ultérieur), disque.
