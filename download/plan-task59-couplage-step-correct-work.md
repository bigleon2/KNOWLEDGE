# Plan d'actions Task 59 — Couplage correct-work v2.10.0 : plan d'actions des correctifs via gen-plan en mode STEP + re-plan Task 58 (mode STEP)

**Générateur** : skill `gen-plan` v3.35.2 (invocation **mode NULL** — `gen-plan : "…"` sans mode explicite : exécution classique sans portes de confirmation, clause mode NULL v3.21.0). **Session** : web-c30e6506 · **Date** : 2026-11-06 · **Position** : préalable « avant tout chose » à la continuation Task 58 (directive propriétaire : « continue mais avant tout chose fais gen-plan : "intègre dans mon skill correct-work qu'il génère le plan d'actions des correctifs via mon skill gen-plan en mode STEP, puis recommence gen-plan en mode STEP" »).

---

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5, 23:12Z)

| Vérification préalable | Résultat |
|---|---|
| É1-INSTALL (garde n°9) | **INSTALLE** — piliers présents (KB 52 entrées, PM SHARED v1.7.26, gen-plan v3.35.2), miroir `3ace5b5` porcelain 0, certification verte ce tour (verify-cross 100 %, integrity 108/108 ×2, coherence 53/23/0, verify-correct-work 16/16 — worklog suite 9) |
| correct-work (état disque) | **v2.9.0** installé — §1.5 couplage gen-plan OBLIGATOIRE à l'Étape 1 (plan de vérification, plancher >= v3.7.0) ; **aucune contractualisation du plan d'actions des CORRECTIFS** (les corrections Étapes 2-5 sont appliquées directement, max 2 rounds — c'est le vide que la directive comble) |
| gen-plan (état disque) | **v3.35.2** — mode step disponible depuis v3.22.0 (enchaînement autonome des groupes, correct-work(groupe) après chaque groupe, correct-work(projet) en fin de chaîne) ; v3.35.2 >= v3.22.0 ✓ |
| Task 58 (état disque) | **G1 EXÉCUTÉ** (22:18-22:23 : clone cmdr `83d8c84`/`04accb8` porcelain 0, run WF 42303936370 **success**, artefact 1 758 544 o, journal `~/GitHub/_outils/etat-ghorg-ecosysteme.json` 22:22:57Z — worklog G1 À CONSIGNER) · **G2 vide** (dessin-technique v1.1.1, dossier preuves vide 22:35) · **G3 absent** — plan v1 `plan-task58-…md` E8 PASS 22:15Z |
| G-RES | OK (disque 7,1 Go, mémoire 2,5 Go) — PARALLELE possible, séquentiel retenu : G_A2 dépend de G_A1 |

## §1 Objectif (éléments restants de la discussion — règle d'or n°7)

1. « intègre dans mon skill "correct-work" qu'il génère le plan d'actions des correctifs via mon skill "gen-plan" en mode STEP » → **G_A1** : montée correct-work **v2.9.0 → v2.10.0** (MINOR — nouveau contrat §1.5bis) + cascade KO-L004 complète.
2. « puis recommence "gen-plan" en mode STEP » → **G_A2** : régénération du plan d'actions actuel (Task 58 v2) via gen-plan v3.35.2 **mode STEP** (E8 + PLAN-AFFICHE), puis enchaînement autonome des groupes restants (G2 dessin-technique v1.3.0, G3 clôture) avec `correct-work(groupe)` après chaque groupe.
3. « continue … » → l'exécution Task 58 G2/G3 se poursuit sous le plan régénéré (v2.10.0 mobilisé pour la clôture `correct-work (projet) --bloc`).

## Answer key (hook E1)

```yaml
decisions:
  - id: "D591"
    libelle: "correct-work SKILL.md v2.10.0 — §1.5bis « Plan d'actions des correctifs via gen-plan en mode STEP » (contrat OBLIGATOIRE : tout lot de correctifs Étapes 2-5 planifié via gen-plan mode STEP avant application ; groupes + correct-work(groupe) max 2 rounds + correct-work(projet) en fin de chaîne ; plancher gen-plan >= v3.22.0 [version d'introduction du mode step, SHARED §3.2 règle 5] ; ARRÊT EXPLICITE si gen-plan indisponible) + §1.3/§1.5/§2.2/§3/§10.1 Phase 2 alignés + description frontmatter += couplage correctifs STEP"
    criterion: "SKILL.md version 2.10.0 ; §1.5bis présent avec les 5 points (obligation, mode STEP, plancher 3.22.0, arrêt explicite, compatibilité tous modes) ; plancher frontmatter gen-plan >=3.22.0 ; plage lignes 200-500 respectée"
    verification: "verify-correct-work.py recalibré 16/16 (version attendue 2.10.0, checks 11/15 → >=3.22.0)"
    source: "Directive propriétaire ce tour (verbatim §1.5bis)"
    priority: S1
    status: pending
  - id: "D592"
    libelle: "PM CORRECT-WORK v2.10.0 généré (corpus @mon-ecosysteme/ — renommé, 9 fichiers inchangés en compte) + v2.9.0 archivé R4 git mv byte-identité @historique/prompts-maitres/correct-work/ + delta verrouillé scripts/delta-correctwork-v2100.json"
    criterion: "Mêmes subs que SKILL.md (titre, §1.3, §1.5, §1.5bis, §2.2, §3, §4 YAML, §6 table arbiteur, §10.1, history += v2.10.0) ; SHA-256 v2.9.0 archivé == blob pré-déplacement"
    verification: "Round-trip corpus 9/9 byte-identique (integrity check 2) ; git mv miroir sans copie (R4)"
    source: "Mécanique KO-L004 v1.1.0 (génération mécanique du PM à toute montée)"
    priority: S1
    status: pending
  - id: "D593"
    libelle: "Cascade KO-L004 complète : KB (entrée ## correct-work v2.10.0 — description + Dépend de gen-plan >= v3.22.0 + calibration Task 59) · pin ECO_SKILLS 2.9.0 → 2.10.0 · historiques-par-skill ligne v2.10.0 (v2.9.0 supplantée) · SHARED v1.7.27 (§6.1 ligne CORRECT-WORK v2.10.0 + en-tête révision) · PM-INSTALL v1.9.4 (§2ter instantané + §A.3 + history) · corpus README + ULTRA recalibrés · archive v2.3 rescellée (piliers correct-work SKILL.md + KNOWLEDGE.md + check-ecosysteme-integrity.py)"
    criterion: "Toutes touches appliquées ; integrity 108/108 ×2 arbres (le bump sans cascade échouerait — L57-1 détecteur) ; coherence sans FAIL ; verify-correct-work 16/16"
    verification: "Re-certification ×2 arbres verte + commit miroir Task 59"
    source: "Cascade 5 touches (leçon L57-1) + recalibrage croisé SHARED/PM-INSTALL (précédent v2.9.0)"
    priority: S1
    status: pending
  - id: "D594"
    libelle: "Re-plan mode STEP : plan d'actions actuel (Task 58) RÉGÉNÉRÉ via gen-plan v3.35.2 mode STEP — G1 documenté fait (preuves §0), préalable Task 59 documenté fait, G2/G3 restants — E8 PASS + PLAN-AFFICHE, puis enchaînement autonome (correct-work(groupe) après chaque groupe)"
    criterion: "plan-task58 v2 horodaté frais ; answer key D581-D588 statuts recalés (D581-D584 FAIT, D585-D588 pending) ; E8 5/5"
    verification: "check_plan_protocol.py P1-P5 PASS ; worklog suite 10"
    source: "Directive « puis recommence gen-plan en mode STEP » + règle d'or n°2 (KO-L005 : gen-plan v3.35.2 inchangé = version génératrice)"
    priority: S1
    status: pending
```

## §2 Groupes et tâches

### G_A1 — Montée correct-work v2.10.0 (séquentiel, écritures concentrées écosystème)
- **SG1** SKILL.md v2.10.0 (§1.5bis + alignements §1.3/§1.5/§2.2/§3/§10.1 + frontmatter description/deps + note plancher gradué §3.2 règle 6).
- **SG2** PM v2.10.0 (copie + subs, delta verrouillé) + v2.9.0 archivé R4 + arbitre verify-correct-work.py recalibré (2.10.0, checks 11/15 → 3.22.0).
- **SG3** Cascade : KB + pin + historiques + SHARED v1.7.27 + PM-INSTALL v1.9.4 + README/ULTRA + archive piliers rescellée + sync miroir + commit + re-certification ×2 arbres.

### G_A2 — Re-plan mode STEP (après G_A1)
- **SG1** Régénération plan-task58 v2 (mode STEP) + E8 + PLAN-AFFICHE.
- **SG2** Bascule vers l'exécution du plan régénéré (mode step : G2 dessin-technique, G3 clôture — correct-work(groupe) après chaque groupe).

## §3 Budget #token et profil

~14 k#token (G_A1 ~10 k · G_A2 ~4 k) × 1,3 ≈ **18 k**. Profil NORMAL. Skills mobilisés : gen-plan v3.35.2 (porteur), correct-work v2.10.0 (auto-vérification post-montée), script-creator (conventions), clone-chat (clôture session).

## §4 Risques et adaptations (règle d'or n°1)

- Plage 200-500 lignes du check 2 : SKILL.md v2.9.0 = 466 lignes, §1.5bis ≈ +14 → ~482 ✓ (si dépassement : recalibrage plage documenté, précédent v2.9.0).
- verify-correct-work.py Check 11 exige « >= v3.7.0 » : la recalibration (3.22.0) et les éditions SKILL.md sont ATOMIQUES — l'arbitre n'est rejoué qu'après les deux.
- Drift §0 SHARED v1.7.26 dans les 116 skills : bump SHARED v1.7.27 (§6.1 seul) SANS re-propagation §0 (précédent v1.7.21→v1.7.26 : propagation seulement quand le contenu §0 change — KO-L003 dérivation dynamique).
- Recyclage sandbox en cours de chaîne → plan rejouable, preuves vivantes.

## §5 Hors périmètre (différés/propriétaire)

Push distant KNOWLEDGE (GO propriétaire — KO-L009 : commits 59a5805 + 1e7e541 + 2adbd7a + 3ace5b5 + Task 58/59) · rotation PAT K1/K2/K3 + GHORG_GITHUB_TOKEN (RAPPEL clôture Task 58) · fusion workflow compilation-windows → master · F1 import Traktor · F3 décision P1b.

---

## Hooks de validation (E8)

Horodatage plan : 2026-11-06T23:20:00Z

Verdict E8 : (à arbitrer — check_plan_protocol.py après exécution G_A1/G_A2)
