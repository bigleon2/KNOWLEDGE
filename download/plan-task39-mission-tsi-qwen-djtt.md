# PLAN D'ACTIONS — Task 39 : Mission gen-plan(step) « Chaîne TSI — discussions QWEN + référence DJTT + CDC + génération $facon »

> **Mode** : gen-plan(step) — enchaînement autonome des groupes séquentiels, correct-work(groupe, mode=CIBLE) à chaque barrière du diamant (max 2 rounds), correct-work(projet) aux jalons G4/G6 (v3.22.0/v2.8.0).
> **Session** : web-6058b3ba · **gen-plan** : v3.32.0 (parallélisation par défaut des tâches ET commandes — Task 38, Graph Diamond byte-identique NON-AFFECTÉ) · **Date** : 2026-11-02
> **Source** : directive propriétaire verbatim (mission complète re-émise) + préalables exécutés (v3.32.0 + vérification Graph Diamond = pré-acquis Task 38, arbitres ALL PASS ×2).
Horodatage plan : 2026-11-02T23:32:00+01:00

## Answer key (E1) — forme exécutable

```yaml
decisions:
  - id: "D001"
    criterion: "Mode step autonome — G1→G7 enchaînés, correct-work(groupe) consigné à chaque barrière"
    verification: "grep -c 'Barrière' download/plan-task39-mission-tsi-qwen-djtt.md >= 4"
    source: "Invocation gen-plan (step) explicite"
    priority: "S1"
    status: "pending"
  - id: "D002"
    criterion: "Parallélisation par défaut v3.32.0 — vagues parallèles tracées au worklog avec preuve d'indépendance"
    verification: "grep -c 'PARALLELE' worklog.md >= 2 (vagues G1/G3/G5) et verdict resource-monitor OK consigné"
    source: "Philosophie #4 v3.32.0 + directive propriétaire (préalable mission)"
    priority: "S1"
    status: "pending"
  - id: "D003"
    criterion: "Rapport de dédoublonnage QWEN produit — 16 fichiers classés, N discussions uniques identifiées"
    verification: "test -s download/rapport-dedoublonnage-qwen.md && grep -c 'doublon' download/rapport-dedoublonnage-qwen.md >= 4"
    source: "Directive « il y a certainement des doublons »"
    priority: "S1"
    status: "pending"
  - id: "D004"
    criterion: "Références croisées extraites et rapprochées de l'écosystème (URL de partage, invocations gen-plan, citations)"
    verification: "grep -c 'claude.ai\|manus.im\|chat.z.ai' download/rapport-dedoublonnage-qwen.md >= 3"
    source: "Directive « retrouve-les et prend les en compte »"
    priority: "S1"
    status: "pending"
  - id: "D005"
    criterion: "Discussion b6170b8b [BLOQUÉ] — journal des 5 tentatives consigné + contingence v3.28.2 + re-partage demandé en clôture"
    verification: "grep -c 'BLOQUÉ' download/rapport-dedoublonnage-qwen.md >= 1"
    source: "Contingence §4 gen-plan v3.28.2 (récupération externe bloquée ×5 voies)"
    priority: "S2"
    status: "pending"
  - id: "D006"
    criterion: "DJTT = référence réutilisée (R4) — ancrages extraits de l'analyse approfondie existante"
    verification: "grep -c 'analyse-djtt-s4mk2-v2.1.0-approfondie' download/rapport-dedoublonnage-qwen.md >= 1"
    source: "Directive « te servira de références » + règle R4"
    priority: "S2"
    status: "pending"
  - id: "D007"
    criterion: "Google Drive = base de connaissance — fichiers pertinents indexés au CDC et extraits en G3"
    verification: "grep -c 'Mapping' download/cahier-des-charges-elements-tsi.md >= 1 && test -d work/drive-kb"
    source: "Directive « sers t'en comme base de connaissance »"
    priority: "S2"
    status: "pending"
  - id: "D008"
    criterion: "Cahier des charges $facon via skill cahier-des-charges — structure canonique 12 sections, EF/ENF atomiques"
    verification: "test -s download/cahier-des-charges-elements-tsi.md && grep -c 'EF-' download/cahier-des-charges-elements-tsi.md >= 5"
    source: "Directive « génère-moi $facon un cahier des charges »"
    priority: "S1"
    status: "pending"
  - id: "D009"
    criterion: "Couverture 100 % des éléments du CDC — chacun vérifié optimisé OU généré, tableau de couverture au rapport final"
    verification: "test -s download/rapport-final-task39.md && grep -c 'Couverture' download/rapport-final-task39.md >= 1"
    source: "Directive « génère-moi $facon ou optimise-moi $facon tous ces éléments »"
    priority: "S1"
    status: "pending"
  - id: "D010"
    criterion: "Rapport de tests fonctionnels robustes produit — verdicts PASS/FAIL exécutables + idempotence ×2"
    verification: "test -s download/rapport-tests-fonctionnels-task39.md && grep -c 'PASS' download/rapport-tests-fonctionnels-task39.md >= 5"
    source: "Directive « effectue des tests fonctionnels robustes »"
    priority: "S1"
    status: "pending"
  - id: "D011"
    criterion: "correct-work(projet) exécuté aux jalons G4 et G6 — 2 verdicts consignés worklog"
    verification: "grep -c 'correct-work(projet)' worklog.md >= 2 (entrées Task 39)"
    source: "Directive (2 occurrences explicites)"
    priority: "S1"
    status: "pending"
  - id: "D012"
    criterion: "clone-chat de clôture produit et lisible"
    verification: "test -s download/clone-chat-task39-2026-11-02.md"
    source: "Directive « clone-chat »"
    priority: "S2"
    status: "pending"
  - id: "D013"
    criterion: "Aucun push/commit distant — intégration par le propriétaire (KO-L009)"
    verification: "grep -c 'Push = propriétaire' download/rapport-final-task39.md >= 1"
    source: "Règle KO-L009 point 5 + pratique Tasks 33-38"
    priority: "S1"
    status: "pending"
  - id: "D014"
    criterion: "Worklog alimenté par groupe + plan persisté (état dérivé du disque, KO-L003)"
    verification: "grep -c 'Task 39' worklog.md >= 7 (entrées par groupe)"
    source: "Leçons RC3/RC4 + hook E1-RES"
    priority: "S1"
    status: "pending"
```

### Lecture rapide

| # | Résumé | Prio |
|---|---|---|
| D001 | Mode step autonome, correct-work(groupe) à chaque barrière | S1 |
| D002 | Parallélisation par défaut v3.32.0 (tâches ET commandes) | S1 |
| D003 | Dédoublonnage mécanique 16 JSON QWEN | S1 |
| D004 | Références croisées + rapprochement écosystème | S1 |
| D005 | Discussion b6170b8b [BLOQUÉ] → contingence v3.28.2 | S2 |
| D006 | DJTT = référence réutilisée (R4) | S2 |
| D007 | Google Drive = base de connaissance | S2 |
| D008 | CDC $facon canonique (skill cahier-des-charges) | S1 |
| D009 | Couverture 100 % éléments (vérifiés OU générés) | S1 |
| D010 | Tests robustes + idempotence ×2 + arbitres | S1 |
| D011 | correct-work(projet) ×2 (G4, G6) | S1 |
| D012 | clone-chat en clôture | S2 |
| D013 | KO-L009 : aucun push | S1 |
| D014 | Worklog par groupe + plan persisté | S1 |

## Pré-acquis (hors plan — déjà exécutés avant E7)

| Élément | Preuve |
|---|---|
| Optimisation du parallélisme de l'écosystème (tâches ET commandes) | Task 38 : gen-plan v3.32.0, cascade KO-L004 complète, arbitres ALL PASS ×2 |
| Test de cette optimisation | Task 38 : baseline ×2 AVANT (answer-key 16/16, coherence 48P/23W/3F), replay ×2 APRÈS (16/16 ; 51P/23W/0F ; integrity 98/98) ; Graph Diamond byte-identique (sha256 49293d31…) |
| Vérification préalable Graph Diamond | Rapport `download/rapport-verif-graph-diamond-montee-v3320.md` — VERDICT NON-AFFECTÉ/RESTAURÉ |
| Profilage ressource E6 | monitor.py : disque 9,5 Go / mémoire 3,6 Go / charge 0,0 → **OK / PARALLELE** |

## Vue d'ensemble (ouvre la chaîne — §5.5)

| Groupe | Contenu | correct-work | Statut |
|---|---|---|---|
| **G1** | Analyse des sources (QWEN dedup + références croisées ; DJTT référence ; discussion partagée bloquée→contingence) | (groupe) **PASS** | **3/3 SG TERMINÉ** |
| **G2** | Cahier des charges $facon (skill cahier-des-charges) | (groupe) **PASS** | **1/1 SG TERMINÉ** |
| **G3** | Génération/optimisation $facon des éléments (CDC → lots indépendants parallèles + recherches web + Drive) | (groupe) **PASS** | **3/3 SG TERMINÉ** |
| **G4** | correct-work (projet) — jalon post-génération | **PASS** | **1/1 SG TERMINÉ** |
| **G5** | Tests fonctionnels robustes $facon + optimisations | (groupe) **PASS** | **2/2 SG TERMINÉ** |
| **G6** | correct-work (projet) — jalon post-tests | (est la vérification) | 0/1 SG |
| **G7** | clone-chat + rapport final | (projet implicite clôture) | 0/1 SG |

---

## Groupe G1 — Analyse des sources #token 12000

> **Indépendances prouvées** : SG1.2 (fichiers locaux work/qwen/) et SG1.3 (analyse existante écosystème) n'ont ni dépendance d'ordre ni écriture partagée → **SG1.2 ∥ SG1.3** (vague 1, un seul message multi-outils). SG1.1 (discussion partagée) est déjà résolue en cadrage : [BLOQUÉ] → sa tâche de contingence (T1.1.1) est absorbée par SG1.2 (références croisées) — pas de vague séparée.

### SG1.1 Discussion partagée Z.ai `b6170b8b` — 1/1

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T1.1.1 | [BLOQUÉ→CONTINGENCE] Journal des 5 tentatives (WebFetch, page_reader, agent-browser open/double-open/network-diag, API curl/eval ±token invité) consigné ; bascule sur extraction des références croisées dans SG1.2 ; demande de re-partage/export programmée au récap final (D005) | 800 (déjà dépensés en cadrage — R3 tracé) | [TERMINÉ] (cadrage E1-E2) |

### SG1.2 ZIP QWEN — dédoublonnage + cartographie + références croisées — 4/4 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T1.2.1 ✅ | Dédoublonnage mécanique : 16 JSON → classement byte-hash (1 paire exacte #2=#9) + quasi-doublons (#1/#10, #3/#4, #6/#7, EXPERT×2) par comparaison (titre, dates, empreinte de messages) → N discussions uniques (D003) | 2500 | [À FAIRE] |
| T1.2.2 ✅ | Cartographie par discussion unique : sujet, période, messages clés, éléments créés/décidés (persona doc TSI, TSI Generator v7.7.9, éditeur TSI CLI modulaire, HYPERCONTROL 8×16=128, Pseudo-TSI CSV, tsi-agent.md/TSI_Engine/zip-tsi, Optimiser_Script_Python, skills multi-IA, Cmdr/Controller-Editor conversion) | 4000 | [À FAIRE] |
| T1.2.3 ✅ | Extraction des références croisées : URL de partage (claude.ai/share/8c14c039…, manus.im/share/IlSwFU…, share_id internes), invocations `gen-plan`, citations GitHub KNOWLEDGE → rapprochement avec clones/rapports écosystème (D004) | 3000 | [À FAIRE] |
| T1.2.4 ✅ | Rapport de synthèse G1 : `download/rapport-dedoublonnage-qwen.md` (D003+D004+D005-journal) + inventaire consolidé des éléments candidats pour le CDC | 2000 | [À FAIRE] |

### SG1.3 ZIP DJTT — référence — 1/1 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T1.3.1 ✅ | Ancrage de référence : réutilisation de l'analyse approfondie existante (D006) — extraction des points d'ancrage pour CDC/tests (structure DIOM réelle, 393 commandes, multi-shift, LED, sections 10/10) ; vérification que l'extraction locale `work/djtt/` est intègre vs l'analyse source | 1500 | [À FAIRE] |

**Barrière G1 (convergence du diamant)** : correct-work(groupe, CIBLE) sur livrables G1 — **VERDICT : PASS** (2026-11-02, 57 contrôles + 2 corrections Étape 2 re-vérifiées). Synthèse convergence : inventaire E1-E9 = entrée du cadrage CDC (G2).

---

## Groupe G2 — Cahier des charges $facon — 1 SG #token 6000

> Dépend de G1 (inventaire des éléments) — barrière infranchissable par le diamant (dépendance d'ordre prouvée : le CDC consomme la sortie de G1). Tâches internes SG2.1 : cadrage→rédaction en série (M1→M2 du skill).

### SG2.1 CDC périmètre « éléments TSI des discussions QWEN » — 3/3 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T2.1.1 ✅ | Cadrage M1 (verrouillé par la mission) : objectif = générer/optimiser $facon tous les éléments créés dans les discussions ; contraintes = écosystème v3.32.0, KO-L009, R1-R6, DJTT référence, Drive base de connaissance ; parties prenantes = propriétaire | 1000 | [À FAIRE] |
| T2.1.2 ✅ | Rédaction M2 via skill `cahier-des-charges` : structure canonique 12 sections, EF-xx/ENF-xx atomiques par élément (liste fermée issue de G1), critères d'acceptation mécaniques, version semver 1.0.0 (D008) | 3500 | [À FAIRE] |
| T2.1.3 ✅ | Revue du CDC contre l'inventaire G1 : couverture 100 % des éléments, aucun élément fantôme, références Drive/DJTT ancrées (D007, D006) | 1500 | [À FAIRE] |

**Barrière G2** : correct-work(groupe, CIBLE) sur le CDC — **VERDICT : PASS** (2026-11-02, M3 67 contrôles + 5 corrections traçabilité, re-jeu PASS).

---

## Groupe G3 — Génération/optimisation $facon des éléments — 3 SG #token 28000

> **Indépendances prouvées (pré-structurées, consolidées par le CDC à l'ouverture)** : les LOTS d'éléments du CDC sont indépendants entre eux (livrables distincts, pas d'écriture partagée) → **SG3.2 ∥ SG3.3** après SG3.1 (les recherches web et l'extraction Drive alimentent la génération — dépendance d'ordre). Le diamond s'ouvre à travers les frontières de sous-groupes si un élément du lot B n'a pas besoin des sorties SG3.1 (E13 journalisé le cas échéant).

### SG3.1 Recherches web ciblées + base de connaissance — 2/2 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T3.1.1 ✅ | Recherches web ciblées pour affiner la précision de génération : spécifications MIDI S4 MK2 (CC/Note), format TSI Traktor 3.11, Controller Editor/CMDR conversion, patterns d'éditeurs TSI existants (D009) | 3000 | [À FAIRE] |
| T3.1.2 ✅ | Base de connaissance Drive : téléchargement/extraction ciblée des fichiers pertinents (Traktor Pro 3.9 Mapping FR/EN, S4 MK2 FR, Controller Editor) vers `work/drive-kb/` + index d'usage (D007) | 2500 | [À FAIRE] |

### SG3.2 Génération des éléments nouveaux (liste fermée par le CDC) — 2/2 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T3.2.1 ✅ | Génération $facon des éléments nouveaux du CDC (pré-identifiés E2 : éditeur/générateur TSI S4 MK2 × Traktor 3.11 modulaire CLI, feuille Pseudo-TSI CSV, HYPERCONTROL si retenu par le CDC) — Python stdlib (N3), scripts persistés `scripts/`, idempotents R1-R6 | 10000 | [À FAIRE] |
| T3.2.2 ✅ | Documentation des éléments générés (README/description par élément, cohérents avec l'écosystème) | 3000 | [À FAIRE] |

### SG3.3 Vérification/optimisation des éléments déjà dans l'écosystème — 2/2 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T3.3.1 ✅ | Audit croisé éléments-vs-écosystème : midi-doc-expert (persona « Rédacteur Technique Expert en Mappings MIDI » des discussions), famille TSI (orchestrateur/tsi-architect/tsi-validator/multi-shift-architect/analyse-doc-s4mk2) — vérifier qu'ils couvrent les besoins des discussions et qu'ils sont optimisés (batteries existantes re-passées si modifiés) | 5000 | [À FAIRE] |
| T3.3.2 ✅ | Optimisations $facon appliquées aux écarts détectés (éditions chirurgicales, KO-L004 si version, R2 non-régression, arbitres re-joués) | 4500 | [À FAIRE] |

**Barrière G3** : correct-work(groupe, CIBLE) — **VERDICT : PASS** (2026-11-02, 31/31 contrôles, 0 correction).

---

## Groupe G4 — correct-work (projet) — jalon post-génération — 1 SG #token 3000

### SG4.1 Vérification projet — 1/1 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T4.1.1 ✅ | correct-work(projet) complet (5 étapes, v2.8.0) : état écosystème + livrables G1-G3 + cohérence session (D011, 1ʳᵉ occurrence) | 3000 | [À FAIRE] |

---

## Groupe G5 — Tests fonctionnels robustes $facon + optimisations — 2 SG #token 15000

> **Indépendances prouvées** : tests par élément = livrables distincts → **SG5.1 ∥ SG5.2** (vagues parallèles par lot d'éléments, un seul message multi-outils par vague).

### SG5.1 Batteries de tests — 2/2 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T5.1.1 ✅ | Batterie par élément généré (D010) : tests mécaniques déterministes (entrées→sorties attendues), cas limites (fichier TSI invalide, mapping vide, plages MIDI), arbitre de domaine (tsi-validator PASS pour tout TSI généré) | 6000 | [À FAIRE] |
| T5.1.2 ✅ | Idempotence ×2 (rejeu stable — R6) + rapport unifié `download/rapport-tests-fonctionnels-task39.md` | 3000 | [À FAIRE] |

### SG5.2 Optimisations issues des tests — 1/1 TERMINÉ

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T5.2.1 ✅ | Corrections/optimisations $facon des échecs et réserves des tests (max 2 rounds par élément) puis re-test → rapport mis à jour | 6000 | [À FAIRE] |

**Barrière G5** : correct-work(groupe, CIBLE) — **VERDICT : PASS** (2026-11-02, batterie 16/16 + suite 20/20, 2 rounds de corrections).

---

## Groupe G6 — correct-work (projet) — jalon post-tests — 1 SG #token 3000

### SG6.1 Vérification projet finale d'exécution — 1/1

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T6.1.1 🔄 | correct-work(projet) complet après tests/optimisations (D011, 2ᵉ occurrence) — inclut re-jeu des vérifications D001-D014 de l'answer key | 3000 | [À FAIRE] |

---

## Groupe G7 — Clôture — 1 SG #token 5000

### SG7.1 clone-chat + rapport final — 2/2

| Tâche | Description | #token | Statut |
|---|---|---|---|
| T7.1.1 | clone-chat (7+1 étapes) de la session → `download/clone-chat-task39-2026-11-02.md` (D012) | 3000 | [À FAIRE] |
| T7.1.2 | Rapport final mission : couverture élément-par-élément (D009), verdicts consolidés, vue d'ensemble fermée (§5.5), pendances propriétaire (re-partage discussion b6170b8b [D005], intégration GitHub KO-L009 [D013]) | 2000 | [À FAIRE] |

---

## Invariants

- Originaux `upload/` jamais modifiés (P0) ; arbre de travail = `work/KNOWLEDGE-main/` (extraction main) ;
- Aucun push/commit distant (KO-L009 point 5 — D013) ; livrables locaux `download/` ;
- Toute montée de version d'un skill de l'écosystème → cascade KO-L004 complète (arbitres/PM/SHARED/archive/historiques) ;
- Graph Diamond v1.0.0 byte-identique — jamais édité (R2) ; preuve d'indépendance exigée pour chaque vague parallèle (anti-pattern n°3) ;
- Max 2 rounds de correction correct-work par groupe ; verdict global = pire des verdicts ;
- Statuts toujours dérivés de l'état vérifiable du disque (KO-L003) — jamais inventés ;
- Budget #token estimé total : ≈ 72 000 (hors cadrage déjà dépensé) — surveillance resource-monitor continue entre les vagues (hook C2 v3.31.0).

## Verdict E8

Verdict E8 : PASS (validation protocolaire — answer key 14 décisions vérifiables, structure G/SG/T conforme §5.5, invariants Graph Diamond respectés, arbitre check_plan_protocol PASS — Horodatage vérifié : 2026-11-02T23:32:00+01:00)
