# Rapport de tests du skill re-curation — Task 72 G4+G5 (D009, D010)

**Date : 2026-11-08** · Session : web-ecef7f80 · Skill : **re-curation v1.0.0** (créé G4 — directive à 7 items item 4 + directive complémentaire 1a1b7b297b7b4975)
Méthode : tests $FACON [(cohérents, optimisés et fonctionnels)] — chaque verdict ci-dessous est une exécution mécanique réelle de la présente session.

## 1. T5.1 — Selftests embarqués + compilation

| Test | Verdict | Couverture |
|---|---|---|
| py_compile ×3 (protocole-test.py, mesure-sections.py, check-recuration.py) | **3/3 ✓** | syntaxe |
| protocole-test.py --selftest | **PASS 5/5** | PRE→GO · POST identité→MAINTIEN · contrat §A altéré→DÉRIVE (rc=1) · compare R4 (suppression disqualifiée) · pointeur manquant→FAIL (rc=1) |
| mesure-sections.py --selftest | **PASS 3/3** | sections détectées · **couverture exhaustive (somme sections == taille fichier)** · fichier introuvable→erreur explicite |
| check-recuration.py --selftest | **PASS 4/4** | état sain→PASS 4/4 · pointeur cassé→C1 FAIL · bloc dupliqué inline→C2 FAIL · skill introuvable→ABANDON |

Correction en round (classe « bug de harnais, jamais du système testé ») : la formule de mesure par section surcomptait les sauts de ligne (+[j−i] au lieu de +1 par section, et le frontmatter n'était pas mesuré depuis la ligne 0) — corrigée sur preuve du selftest « couverture exhaustive » (somme des sections == taille exacte du fichier — vérifié en réel sur gen-plan : 30 668 == 30 668 o). L'original Task 72 (task72-mesure-sections.py) sous-comptait de 1 octet/section — écart informationnel négligeable, aucune décision n'en dépendait.

## 2. T5.2 — Exécutions RÉELLES du protocole de test

### 2.1 Phase PRE sur la cible n°1 (version-management — baseline pour la FUTURE re-curation)

```
--pre version-management → download/protocole-test-version-management.json
nature : version 1.3.0 · §A=False · read_when=True · evals=2 · gouvernance KB=1.3.0 / ECO_SKILLS=True
baseline : 46.1 Kio ≈ 11 810 #token · 39 sections · 5 contrats sha256
VERDICT PRE : GO
```
→ La baseline golden master de la cible n°1 (G3) est **capturée et prête** — la future re-curation de version-management démarre par un GO documenté.

### 2.2 Paire PRE/POST réelle sur gen-plan v3.39.0 (post-re-curation G1)

```
--pre gen-plan   → GO (6 contrats sha256, 31 sections, 29,9 Kio)
--post gen-plan  → contrats evals ×2 PASS · description PASS · pointeurs PASS · non-duplication PASS
                   poids 30 667 → 30 667 o (identité) — seuil LOURD 30 Kio : sous
                   COHÉRENT=True · FONCTIONNEL=True · OPTIMISÉ=True
                   VERDICT POST : MAINTIEN DE L'OPTIMISATION
```
→ Le triplet maintien-de-l'optimisation (cohérent / fonctionnel / optimisé) est vérifié EN RÉEL sur le skill re-curé en G1.

### 2.3 Mode VÉRIFICATION réel sur gen-plan v3.39.0 (arbitre du nouveau skill validant la re-curation G1)

```
check-recuration.py gen-plan → C1 pointeurs PASS · C2 non-duplication PASS
                               C3 marqueurs PASS · C4 seuils PASS (29,9 Kio — INTERMÉDIAIRE)
                               VERDICT : PASS (rc=0, stable ×2)
```
→ L'arbitre C1-C4 du skill re-curation **valide mécaniquement la re-curation G1 de gen-plan**.

### 2.4 Mode --compare réel (arbitrage des méthodes, gen-plan — potentiel résiduel)

```
sections ≥ 1,5 Kio mobilisables : 10,9 Kio
moves-r4-resumes             → 20,4 Kio · R4 ✓
moves-r4-pur                 → 19,4 Kio · R4 ✓   ← la plus optimisée et performante (R4-compliantes)
append-references-existantes → 20,4 Kio · R4 ✓
suppression                  → 19,1 Kio · R4 ✗ DISQUALIFIÉE
```
→ Gains projetés calculés des sections MESURÉES (jamais inventés) ; les méthodes non-R4 sont disqualifiées d'office — la plus optimisée et performante est désignée parmi les R4-compliantes.

## 3. T5.3 — Idempotence ×2 (re-jeu no-op)

| Re-jeu | Preuve |
|---|---|
| --pre version-management ×2 | SHA-256 du protocole **b66f338a4a36… identique aux deux passages** — baseline stable |
| --verifier gen-plan ×2 (check-recuration) | VERDICT PASS stable |
| selftests ×3 | PASS stables (5/5 · 3/3 · 4/4) |

## 4. Cascade légère (G4/T4.4) — preuves

- **KB** : entrée `## re-curation v1.0.0` insérée (Description + Dépend de + Dernière calibration) + **réciprocités** « Utilisé par » ajoutées à gen-plan et correct-work (2 WARN d'asymétrie cohérence résorbées → 54/1/0).
- **Pin ECO_SKILLS** : `"re-curation": "1.0.0"` (check-ecosysteme-integrity.py) — integrity **112/112 PASS, 0 FAIL** (manifeste ré-écrit ; compteur passé 110→112 avec la nouvelle entrée KB).
- **Historiques** : `@historique/historiques-par-skill/re-curation.md` créé (famille 1 version).
- **§0 canonique** : bloc L2 propagé inséré (cross 100,0 % — l'écart initial « §0 incomplet » résorbé ; propagate-context re-jeu = 0 skills/0 scripts/0 agents no-op).
- **ULTRA** : régénéré (131 lignes, SHA f40ea21e…).
- **Arbitres finaux** : integrity **112/112** · coherence **54 PASS / 1 WARN B1 légitime / 0 FAIL — PASS AVEC RÉSERVES** · vcw **16/16 ALL PASS** · cross **100,0 %**.
- **Archive** : re-scellée ×2 (SHA final 31533516…, round-trip corpus 9/9 + piliers 6/6 byte-identiques — KB/pin/ULTRA pilier-fraîches).

## 5. Synthèse honnête

**Verdict des tests $FACON : PASS** — le skill re-curation v1.0.0 est cohérent (contrats/selftests/idempotence), optimisé (3 scripts ciblés, selftest < 1 s, stdlib), fonctionnel (executions réelles PRE/POST/VÉRIFICATION/--compare sur des éléments réels de l'écosystème, dont la validation rétroactive de la re-curation G1). Le protocole de test adapté (directive complémentaire 1) fonctionne : **baseline de la cible n°1 capturée, GO tracé — la prochaine re-curation (version-management) peut démarrer par un test, pas par une foi**.

Décisions couvertes : **D009 ✓** (skill créé, implémenté du script principal, 3 scripts selftestés, evals, cascade légère) · **D010 ✓** (présent rapport — PRE/POST/--compare réels tracés).

Pendance : PUSH propriétaire (D013/KO-L009 — inchangé).
