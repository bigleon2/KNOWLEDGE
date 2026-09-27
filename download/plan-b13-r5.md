# PLAN D'ACTIONS B13-r6 — régénéré via gen-plan v3.16.0 (garde G-RES intégrée)

> **Version du plan** : B13-r6 (maintenance E13) | **Généré le** : 2026-09-27 | **Mode** : M1 (Planification)
> **Provenance** : régénération conforme à la **règle d'or n°2 §1.5** (gen-plan v3.16.0) et à la directive utilisateur trace `1a0dfe43940ae0c5` — « si mon skill gen-plan version 3.16.0 est fonctionnel alors génère à nouveau le plan d'actions actuel via la version 3.16.0 ». Le plan B12 précédent est perdu (incident B-17 + wipe inter-sessions) ; la régénération suit le pattern r29/r40 : le worklog fait foi.
> **Auto-suffisance** : ce plan est auto-portant — tout tour peut reprendre sans contexte hérité (bloc REPRISE en fin de plan).
> **Règle permanente (NOUVELLE, directive utilisateur)** : chaque fois que gen-plan est **modifié et jugé valide**, le plan d'actions actuel est **re-généré via la nouvelle version** — validité établie par arbitres mécaniques AVANT toute re-génération (jamais par présomption). Enregistrée comme leçon **L005** (knowledge-observer) ; cette exécution en est la première application.
> **Révision B13-r6** (trace `1a0e00ed957ff2d1`, maintenance E13 optimisée via gen-plan) : garde transversale **G-RES** (surveillance de la consommation des ressources + adaptation autonome en cas de blocage/ralentissement) intégrée additivement (R2) — ancrée sur le skill **`resource-monitor` v1.0.0** (détenteur de la fonction de surveillance permanente, gen-plan §1.14) ; règles R-RES1 à R-RES5 détaillées en E7 ; aucune phase existante supprimée (additivité R2).

---

## E1 — Analyse de la demande (hook answer key)

| Objet | Contenu | Traçabilité |
|-------|---------|-------------|
| (a) Validité gen-plan v3.16.0 | Exigée AVANT toute re-génération | n60-genplan-3160 **10/10 ALL PASS** + certification complète **5/5 ALL PASS** (verify-cross 47/47 ×2, verify-correct-work 16/16, integrity 42/42, interactions 42/45 PASS AVEC RÉSERVES) — rapport `tmp/b13r5-install/rapport-n60.json`, `scripts/certification-report.json` |
| (b) Re-génération du plan | Ce document (E1-E8) | règle d'or n°2 + directive trace `1a0dfe43940ae0c5` |
| (c) Règle permanente | Re-générer à chaque version modifiée et jugée valide | leçon L005 (journal knowledge-observer) + phase N23 |
| (d) Garde G-RES | Surveillance permanente des ressources + adaptation autonome aux blocages/ralentissements (conso, stagnation, timeouts, 429), mise à jour optimisée du plan via gen-plan si nécessaire — pour atteindre l'objectif final | demande trace `1a0e00ed957ff2d1` ; skill `resource-monitor` v1.0.0 (§1.14) ; garde R-RES1 à R-RES5 en E7 |

Décisions vérifiables : registre `tmp/b13r5-install/answer-key-b13.md` (D011-D017, extension R2 du registre b12 D001-D010).

## E2 — Inventaire des ressources

- **Corpus canonique** `skills/@mon-ecosysteme/` : 19 fichiers, restauration B13-r4 complétée B13-r5 (T1-T4 : snapshot 43 Mo, PM v3.16.0 assemblé 1348 L, observation-patterns.md v1.0.0, lessons-learned.json L001-L004 restitués).
- **3 emplacements PM v3.16.0** : corpus + miroir `skills/_prompts-maitres/` + racine `@mon-ecosysteme/` (diff SHA256 19/19 byte-identique).
- **Arbitres calibrés v3.16.0** : integrity (19 fichiers, ECO_SKILLS 3.16.0), SYNC_MAP (+v3.16.0), verify-correct-work (2.6.0), n60 (10 checks), answer-key-checker (16 checks).
- **Pile de directives en attente** : 5 directives antérieures (voir phases N24-N28) + directive courante.

## E3 — Classification

**Type 4** (orchestration / traitement local) avec livrable plan markdown — aucune interface web, aucun document bureautique demandé.

## E4 — Estimation #token

| Phase | Objet | Estimation |
|-------|-------|-----------|
| N22 | Clôture B13-r5 : idempotence ×2 arbitres + traçabilité T6 | 800 #token |
| N23 | Règle permanente : leçon L005 + application immédiate (ce plan) | 800 #token |
| N23-b | (armée) Montée v3.17.0 : extension règle d'or n°2 + re-certification + re-génération plan | 8000 #token |
| N24 | Cycle M1-M2 knowledge-observer sur la session | 1500 #token |
| N25 | Durcissement script-creator (4 sous-objectifs) | 12000 #token |
| N26 | Homologues archive + RÉVERDICT ×2 | 10000 #token |
| N27 | Audit de provenance : skill dédié + réécriture idempotente | 15000 #token |
| N28 | Convergences transverses (n67-1, PM par version, conventions) | 10000 #token |
| Maintenance | Worklog + re-validation E13 | 500 #token/tour |

## E5 — Sélection des skills

| Skill | Usage | Version plancher |
|-------|-------|-----------------|
| gen-plan | Méthode E1-E15, règles d'or, hooks | 3.16.0 |
| correct-work | Hook E8 + contrôle par phase (E9-E14) | 2.6.0 |
| knowledge-observer | E15 (M1-M2), journal leçons | 1.0.0 |
| Arbitres mécaniques | certification-complete.py, n60, answer-key-checker | — |

## E6 — Profilage ressource

**NORMAL** — signaux de pression : aucun (disque > 5 Go, 0 timeout consécutif, budget < 80 %).

**G-RES active** (révision B13-r6) : la collecte est rejouée en continu (hook E9-E14) via `python skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor-state.json` — à l'ouverture de chaque phase, à chaque signal (timeout, 429, échec d'arbitre, écriture lourde) et à la clôture du tour ; verdict OK / PRESSION / CRITIQUE → mode recommandé (PARALLELE / PARALLELE_REDUIT / SERIE / PAUSE) ; décision journalisée au worklog (règle d'or n°1).

---

## E7 — LE PLAN (phases N22-N28)

> Philosophie : exécution série par défaut (§1.4 #4) ; Graph Diamond uniquement si indépendance prouvée. Toute phase terminée → hook correct-work (§5.4). Idempotence R1-R6 sur chaque écriture.

### GARDE TRANSVERSALE G-RES — Surveillance des ressources + adaptation autonome (trace `1a0e00ed957ff2d1`, révision B13-r6)

> S'applique à TOUTES les phases du plan (N25→N28, N23-b, re-générations) — de l'ouverture à la clôture de chaque tour. Détenteur : skill `resource-monitor` v1.0.0 (gen-plan §1.14, fonction de surveillance permanente). La recommandation du monitor est un AVIS ; la décision de bascule est journalisée au worklog (règle d'or n°1).

- **R-RES1 — Collecte systématique** : à l'OUVERTURE de chaque phase, à chaque point de bascule (timeout, 429, échec d'arbitre, écriture lourde) et à la CLÔTURE du tour → `python skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor-state.json` (sortie JSON machine-à-machine ; le tour met à jour le fichier d'état : timeouts consécutifs, erreurs 429, dernière progression, tâche courante). Verdicts consignés au worklog (R3).
- **R-RES2 — Seuils & modes** : OK → exécution normale (série par défaut, philosophie E7) ; PRESSION → PARALLELE_REDUIT ou bascule série + décomposition des sous-étapes lourdes avec checkpoint intermédiaire (snapshot L002 AVANT écriture risquée) ; CRITIQUE → SERIE stricte ou PAUSE + mini-snapshot de sécurité (L002) AVANT toute action non terminée.
- **R-RES3 — Blocage & stagnation → adaptation autonome OBLIGATOIRE** : déclencheurs — ≥ 2 timeouts consécutifs sur le même appel, ≥ 2 échecs du même arbitre sur le même artefact, stagnation > 15 min sur la même sous-étape (`derniere_progression_epoch`), outil bloqué 2× de suite (règles 12/13 session). Adaptation en cascade R3 (un seul cycle par niveau — jamais de 3e tentative identique) : (a) CONTOURNER (outil/chemin alternatif équivalent) ; (b) SIMPLIFIER (réduire la sous-étape à un noyau vérifiable) ; (c) DÉCOMPOSER (sous-tâches plus petites, checkpoints entre chacune) ; (d) CHECKPOINT (snapshot + worklog + bloc REPRISE) puis re-planification optimisée. Chaque adaptation est tracée (worklog ; plan si structurel).
- **R-RES4 — Mise à jour optimisée du plan via gen-plan** : si l'adaptation change la STRUCTURE du plan (phase inapplicable, nouvelle phase, ordre modifié) → maintenance E13 (règle d'or n°3) : MultiEdit R2 atomique + version du plan incrémentée + E8 re-validation + B-14 ancres. Si gen-plan lui-même doit être modifié → boucle L005 (N23-b : arbitres → v3.17.0 → re-certification → re-génération du plan).
- **R-RES5 — Objectif intangible** : l'objectif final (N25→N28, puis correct-work(projet), puis clone-chat, puis installation — directive `1a0dffd2ae120851`) ne peut être ni abandonné ni substitué — seulement atteint par un chemin adapté. Honnêteté R3 : aucune adaptation simulée, aucun contournement fantôme.

### N22 — Clôture B13-r5 (ce tour)
1. Preuve d'idempotence **×2** : re-exécution `n60-genplan-3160.py` + `certification-complete.py` ×2 — verdicts identiques ALL PASS.
2. Traçabilité T6 : constater calibrages déjà en place (integrity 19/3.16.0, SYNC_MAP v3.16.0, verify-correct-work 2.6.0) — re-verdict honnête (L003/L004).
3. Mise à jour statuts answer key b13 (pending → verified si preuve).
4. Worklog Task 43 (append, R3).

### N23 — Règle permanente de re-génération (ce tour)
1. Journal knowledge-observer : leçon **L005** — « Toute version de gen-plan modifiée et jugée valide (arbitres) déclenche la re-génération du plan d'actions via cette version » — occurrences 2 (règle d'or n°2 lignée + directive trace `1a0dfe43940ae0c5`), statut `validé`, cible §1.5.
2. Application immédiate : ce plan en est la 1re exécution (D012 verified).
3. **N23-b armée** : matérialisation M4 — extension additive R2 de la règle d'or n°2 dans gen-plan §1.5 (bloc PATTERN:KO-L005-v1.0.0) → montée v3.17.0 + recalibrage croisé (L004) + re-certification + **re-génération du plan via v3.17.0** (démonstration boucle complète de la règle). À exécuter au prochain tour ou à la demande.

### N24 — Cycle M1-M2 knowledge-observer sur la session (directive `1a0dfa2dd2163ed5`, ce tour — version compacte)
- **M1 Observation** : collecte des événements de session B13-r5 (wipe, restauration, arbitres, plan) → journal worklog.
- **M2 Analyse** : patterns détectés → L005 (déjà capturée) ; confirmation statuts L002 (proposé — snapshot déjà appliqué 2× en pratique) ; proposition M3 : N23-b.
- Les modes M3-M4 complets exigent un verdict correct-work (hook E15) — armés en N23-b/N27.

### N25 — Durcissement script-creator (directive `1a0def365a639149`, ✅ FAIT B13-r6)
1. correct-work(script-creator) — mode cible sur le skill. → **PASS AVEC RÉSERVES round 1** (0 S1 ; 1 S2 + 3 S3) → corrections → **round 2 PASS** ; rapport tmp/b13r5-install/rapport-correct-work-script-creator.md.
2. Test simple de bout en bout du skill. → **PASS** (micro-arbitre tmp/test-script-creator/kb-entry-count.py, §1.2 ×2, idempotence sha16 ×2).
3. Champ `version` dans skill-creator (cohérence frontmatters). → Déjà présent (1.0.0) — constaté.
4. 4 evals + 7 trigger_evals en base réelle (historique 429 — travail local). → Déjà en base — constaté.
5. Corrections des réserves : KB 13 → **15 entrées** (script-creator + script-reviewer + réciproques skill-creator/correct-work + décision N25/N26) ; recalibrage croisé L004 (integrity 46/46 ×2, interactions 43/3/0 ×2, verify-cross 53/53).

### N26 — Homologues archive + RÉVERDICT (directive `1a0df0297431ea3d`, ✅ FAIT B13-r6)
1. Homologues archive agent-creator / script-reviewer (clone épinglé `d9ff9fb`). → En place (archive v2.1, PROVENANCE-homologues.md) — re-prouvé.
2. Régénération `mon-ecosysteme_archive.zip`. → v2.1 (29 fichiers : 19 corpus + 10 homologues) — re-prouvée (integrity + interactions round-trip v2.1).
3. correct-work(projet). → **REPORTÉ post-N28** (résolution de pile : directive la plus récente `1a0dffd2ae120851` — adaptation tracée G-RES-R4/R-RES5).
4. RÉVERDICT Global « Certification - Complète » via `certification-complete.py` ×2. → **5/5 ALL PASS ×2 identiques** (verify-cross 53/53 ×2 modes, verify-correct-work 16/16, integrity 46/46, interactions 43/46).

### N27 — Audit de provenance (directive `1a0df36f356c3add`, ✅ FAIT B13-r6)
1. Skill dédié audit de provenance (traçabilité des artefacts, lignage wipes/restaurations). → **audit-provenance v1.0.0** (SKILL.md + evals 4+7 + collecteur scripts/audit-provenance.py) — KB 16 entrées, réciproques, décision N27.
2. Réécriture idempotente des artefacts concernés. → **25 scripts documentés** (en-tête PROVENANCE, syntaxe-safe), idempotence ×2 no-op prouvée (sha16 ded19f62…), 33 orphelins résiduels assumés v1.0.0 ; adaptation R-RES3 (périmètre corrigé en vol 1057 → 214 artefacts).
3. Leçon L006 (audit de provenance) — application M3-M4 avec verdict correct-work. → **L006 au journal** (6 leçons, statut appliqué, occurrences 3) ; certification 5/5 ×2 (verify-cross 56/56).

### N28 — Convergences transverses (directive `1a0df4d7831e4f49`, ✅ FAIT B13-r6)
1. Hook n67-1 en E1 (gen-plan) — **FUSIONNÉ avec N23-b** (optimisation G-RES-R4 : UN SEUL cycle de version) : → **v3.17.0 EXÉCUTÉE** (§1.5 bloc PATTERN:KO-L005-v1.0.0 + §1.2bis hook E1-RES n67-1 reconstitué — provenance tracée) ; n60b **12/12 ALL PASS ×2** ; certification 5/5 ×2 ; **PM v3.17.0 assemblé 1362 L déployé ×3** (corpus + miroir + download) ; corpus 20 (archive v2.1 → 30 fichiers) ; **boucle L005 complète : plan B13-r7 re-généré via v3.17.0** (download/plan-b13-r7.md, E8 16/16).
2. Prompts maîtres par version — fraîcheur `mon-ecosysteme/` (diff 19/19 après v3.17.0). → PM v3.17.0 ×3 byte-identiques (copie shutil), SYNC_MAP +v3.17.0, check 3 sync PASS.
3. Conventions langage + skill correct-py (référence post-traitement §1.3 script-creator — vérifier/ajouter R2). → **CONSTAT** : script-creator §1.3 GF-6 + §2/§3 référencent correct-py (post-traitement obligatoire) ✓ ; convention langage appliquée dans les artefacts B13 (contenus FR, identifiants/noms de fichiers non traduits) — aucune édition requise.
4. Provenance script-creator + correct-work (blocs idempotents — couverts par audit-provenance N27). → verify-correct-work.py en-tête PROVENANCE (N27 fix) + KB correct-work Note N27/N28 + KB script-creator Dernière calibration N25.

---

## E8 — Validation du plan

- **Arbitre answer-key-checker** (16 checks) : exécuté après création du registre b13 — verdict requis PASS.
- **Validation mécanique** de la clé b13 : parse YAML-safe + comptage statuts (procédure answer-key-b12 §fin).
- **Hook correct-work E8** : à lever sur ce plan au prochain checkpoint (mode CIBLE) — non bloquant pour N22/N23 (phases locales déjà couvertes par arbitres mécaniques ×2).
- Critères S1/S2 : D011, D012, D016 — tous `verified` avant exécution des phases.

## Bloc REPRISE B13-r6 (auto-suffisant)

Au prochain « continue » (ordre de priorité) :
0. **G-RES réflexe 0** : collecte d'ouverture `python skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor-state.json` → verdict → mode (R-RES1/R-RES2) ; CRITIQUE → PAUSE + checkpoint AVANT toute écriture.
1. **N22/N23/N24 FAITES** (worklog Task 43) ; garde G-RES intégrée (B13-r6, trace `1a0e00ed957ff2d1`).
2. **N25** durcissement script-creator (directive `1a0def365a639149`) — puis **N26** homologues + RÉVERDICT ×2 (`1a0df0297431ea3d`), **N27** audit provenance (`1a0df36f356c3add`), **N28** convergences (`1a0df4d7831e4f49`) — chaque phase ouvre/ferme par une collecte G-RES (R-RES1) et applique R-RES3 en cas de blocage.
3. **N23-b FUSIONNÉE à N28** (G-RES-R4, un seul cycle de version) : §1.5 L005 + hook E1 (n67-1 reconstitué) → v3.17.0 → re-calibrage n60 → re-certification ×2 → PM ×3 → **re-génération du plan via v3.17.0** (règle L005).
4. Après construction complète : **correct-work(projet)** → **clone-chat** (clone intégral de la discussion) → **installation** (INSTALL-ECOSYSTEME.md) — directive `1a0dffd2ae120851`.
5. Tout tour ouvre par la lecture seule préalable (B-11 — D008) ; l'état des arbitres fait foi ; toute adaptation G-RES est tracée (R-RES3/R-RES5).
