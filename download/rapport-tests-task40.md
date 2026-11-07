# Rapport de tests $FACON $FACON2 — Task 40 : LEON TSI EDITEUR v11 (Extension React du studio v11)

> **Session** : web-6058b3ba · **Date** : 2026-11-02 · **Directive** : « effectue $FACON la batterie de tests $FACON2 fonctionnels et de performances, puis fais les correctifs les plus appropriés » + « effectue tous les correctifs »
> **Verdict global : PASS intégral** — 47 vérifications app + arbitres écosystème, 0 échec, 2 rounds de correctifs (2 bugs réels attrapés par les jalons).

## 1. Harnais app (persisté `scripts/leon/` — hôte + dépôt)

| Batterie | Résultat | Timing |
|---|---|---|
| API fonctionnelle 15 points (`test-api-fonctionnel.sh`) | **16/15 PASS** (15 points + contrôle de restauration d'état : 0 projet résiduel) | 0,92 s |
| Idempotence TSI round-trip (`test-idempotence.mjs`) | **12/12 PASS** | 0,091 s |
| ESLint `src/` | **0 erreur / 0 avertissement** | — |
| tsc --noEmit (`src/`) | **0 erreur** | — |
| Navigateur interactif (agent-browser, D1-D12) | **12/12 flux validés** | — |

### Détail idempotence (12/12)
Preset Freeze Mode 15 mappings byte-exact · DSL 5 lignes sans erreur · projet DSL (modifiers M1/M2) byte-exact · re-jeu ×2 byte-stable · échappement XML quotes/& · déséchappement intact · **rejet propre du format réel TraktorSettings → pont écosystème (R4)** · rejet propre racine inconnue · **modifiers M1-M8 round-trip (chiffres)** · détection de conflit (canal/note/couche) · spec LED OUT round-trip (canon NISYSTEM + MODE Output E6) · taille export réaliste.

### Détail navigateur (12/12)
Rendu intégral (vues, panneaux, footer) · vue Modes & Modules **8/8 modules** sourcés · chip commande → dialogue pré-rempli (commande + zone) · ajout → ligne tableau + note auto (anti-collision) + toast · **persistance au rechargement** (2 mappings testés) · preset Freeze Mode appliqué **+15 mappings** (source partagée toolchain) · DSL compilé +3 mappings · **verify → BYTE-EXACT** · vue Retours LED (220, groupée) · mass-edit : sélection + dupliquer (20→21, audit « duplication ») · audit auto-évolutif alimenté (ajout/preset/DSL/duplication avec conflits recalculés) · restauration propre de l'état projet (0 projet résiduel).

## 2. Arbitre écosystème R4 (preuves d'intégration app ↔ toolchain ↔ arbitre)

| Test | Résultat |
|---|---|
| Export app (4 mappings : IN + Modifier source + IN [M1] + LED Output) → `valider-tsi.py` v1.2.0 | **PASS (0 erreur)** rc=0 |
| **E2E preset Freeze Mode complet via l'API (15 mappings) → arbitre** | **PASS (0 erreur)** rc=0 — 3 212 octets |
| Toolkit suite (arbre dépôt, `tsi-toolkit/tests/`) | **20/20 PASS** + 7 subtests (0,58 s) |

## 3. Bugs réels attrapés et corrigés (2 rounds — jalons tsc/verify/arbitre)

| # | Bug | Détecté par | Correctif | Re-test |
|---|---|---|---|---|
| 1 | Regex blocs `<MAPPING[^>]*>` matchait `<MAPPINGS>` → parse vide (NAME/GROUP/CONTROL perdus) | jalon verify API (« DIVERGENT ») | `<MAPPING\s` + tête idem | Round-trip byte-exact ✓ |
| 2 | `ATTR_RE` `[A-Z_]+` ne capturait pas les modifiers **M1-M8** (chiffre) → `<MODIFIER/>` vide au re-parse | jalon verify sur projet réel (modifiers) | `[A-Z0-9_]+` | Round-trip ✓ |
| 3 | Sérialiseur NIXML → l'arbitre classait l'export « réel NIXML » (E1 FAIL) | Preuve R4 arbitre | Alignement canon **NISYSTEM** (VERSION=1, DEVICE conteneur, MAPPINGS COUNT, self-closing golden) | Arbitre **PASS** ✓ |
| 4 | Spec LED sans `MODE="Output"` (E6) | Preuve R4 arbitre | `MODE="Output"` émis + LedSpec.mode | E6 OK ✓ |
| 5 | Garde silencieuse : ajout sans note = impasse (retour vide, dialogue figé) | Test navigateur | **Note auto anti-collision + signal « note provisoire — capturez la vraie (Learn/Ctrl+L) »** | Flux complet ✓ |
| 6 | `e.data` `Uint8Array\|null` non narrant (TS2769) + icônes lucide inexistantes (`Audit`, `MidiIcon`) + setState-en-effet | Jalons tsc/ESLint | Garde `if (!e.data) return`, icônes `ScrollText`/`Radio`, pré-remplissage au montage par clé | 0/0 + 0 erreur ✓ |
| 7 | Étiquette MIDI `Ch000` ≠ convention discussion `Ch00.CC.013` | Revue convention | `pad2` canal | Cohérent ✓ |
| 8 | 9 lignes vivantes des disciplines citant gen-plan v3.30.0 (STALE v3.32.0) | test-coherence-interactions | Recalibrage mécanique ×9 (hôte+dépôt) | **COHÉRENCE 0 FAIL** ✓ |

## 4. Arbitres écosystème (post-correctifs — certification complète)

| Arbitre | Résultat |
|---|---|
| verify-cross (axes 1-6) | **141/141 ALL PASS** (les 2 avertissements hérités — trigger_evals manquants — résorbés par la sync dépôt→hôte des skills) |
| verify-correct-work v2.5.1 | **16/16 ALL PASS** |
| check-ecosysteme-integrity | **98/98 PASS, 0 FAIL** |
| test-coherence-interactions | **50 PASS / 24 WARN / 0 FAIL** — PASS AVEC RÉSERVES (warnings = baseline honnête inchangée) |
| check-tool-routing | **7/7 PASS** (N2 résorbé par le plan Task 40 citant les skills dédiés par type) |
| garde-plan-genplan | **PASS** (plus-récent) |
| **Certification consolidée** | **CERTIFICATION COMPLÈTE : PASS AVEC RÉSERVES (24 avertissement(s), 0 échec) — 6/6** |

## 5. Performances (timings médians, 3 runs — seuils CDC 10 s arbitre / 5 s unitaire)

| Cible | Médiane | Verdict |
|---|---|---|
| API 15 points (harnais complet) | 0,92 s | PASS |
| Idempotence 12 tests | 0,091 s | PASS |
| tsi-validator v1.2.0 — export app 15 mappings | <0,06 s | PASS |
| tsi-validator v1.2.0 — TSI DREW réel 623 Ko | 0,054 s | PASS |
| analyse-doc-s4mk2 — ZIP DJTT 1,8 Mo / DREW 1,3 Mo | 0,174 s / 0,153 s | PASS |
| tsi_toolkit nixml / convertisseurs / studio (DREW réel) | 0,037 s / 0,040 s / 0,039 s | PASS |
| Batterie analyse-doc-s4mk2 16 tests (fixtures DREW réimportées) | **16/16 PASS** 1,44 s | PASS |

## 6. Non-régressions

- Graph Diamond v1.0.0 **byte-identique — jamais touché** (aucun fichier de la chaîne diamant modifié dans cette mission) ;
- Garde R2 tenue : sync complète **dépôt→hôte** (l'état poussé certifié fait foi — 89/115 skills divergents résorbés) + montée v3.32.0 corpus (bundle/scellé Task 38 — jamais de rétrogradation) ;
- Preset et catalogue = sources scellées partagées (byte-parité toolkit : preset 15 mappings identique, catalogue généré mécaniquement 455 commandes, zéro valeur inventée) ;
- Le connecteur S4 MK2 réel (Web MIDI) reste la pendance matérielle honnête : le routage entrant est préservé par construction (handlePortMessage) mais aucune verification hardware n'est possible en sandbox.
