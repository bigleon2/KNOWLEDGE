# PLAN D'ACTIONS B13-r7 — re-généré via gen-plan v3.17.0 (boucle L005 complète)

> **Version du plan** : B13-r7 | **Généré le** : 2026-09-27 | **Mode** : M1 (Planification)
> **Provenance** : re-génération conforme à la **règle d'or n°2 §1.5 + règle KO-L005** (bloc PATTERN:KO-L005-v1.0.0, matérialisé v3.17.0) — la boucle complète est exécutée : extension §1.5 + hook E1-RES (n67-1 reconstitué) → montée v3.17.0 → recalibrage croisé (L004 : integrity 49/49, interactions 43/3/0, verify-cross 56/56, verify-correct-work 16/16) → re-certification ×2 (5/5 ALL PASS ×2) → arbitre n60b **12/12 ALL PASS ×2** → **ce plan re-généré via v3.17.0** (directive trace `1a0dff290e1cef55`, pile N23-b fusionnée N28 — session B13-r6).
> **Hook E1-RES appliqué** (n67-1 reconstitué — PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0) : (1) lecture seule B-11 exécutée (worklog Tasks 43-44 fait foi) ; (2) collecte G-RES exécutée (verdict OK/PARALLELE) ; (3) contrôle de fraîcheur → le plan B13-r6 est obsolète (gen-plan a changé) → ce plan le remplace (R2 : B13-r5/B13-r6 conservés en historique).
> **Auto-suffisance** : ce plan est auto-portant — tout tour peut reprendre sans contexte hérité (bloc REPRISE en fin de plan).
> **Statuts post-Task 47** (directive `1a0e03969df8da69`) : N29 ✅ (Tasks 46-47 — clones -a/-b, 8/8 checks ×2) ; correct-work(projet) ✅ (rounds 1-2 PASS) ; N30 ✅ (Task 47 — installation PM-INSTALL 11/11 ×2, snapshot L002, post-installation certifiée ×2).

---

## E1 — Analyse de la demande (hook answer key)

| Objet | Contenu | Traçabilité |
|-------|---------|-------------|
| (a) Montée gen-plan v3.17.0 | §1.5 bloc PATTERN:KO-L005-v1.0.0 + §1.2bis hook E1-RES (n67-1 reconstitué — provenance tracée, aucun faux lignage) + PM v3.17.0 assemblé 1362 L déployé ×3 (corpus + miroir + download) | N23-b fusionnée N28 (directives `1a0dff290e1cef55`, `1a0df36f356c3add`, `1a0df4d7831e4f49`) |
| (b) Boucle L005 exécutée | arbitres → v3.17.0 → recalibrages → certification 5/5 ×2 → n60b 12/12 ×2 → ce plan | leçon L005 (statut validé, première boucle complète) |
| (c) Garde G-RES | Surveillance des ressources + adaptation autonome (R-RES1 à R-RES5, ancrée resource-monitor v1.0.0 §1.14) — s'applique à toutes les phases | trace `1a0e00ed957ff2d1`, plan B13-r6 |
| (d) Objectif final | Construction complète → **correct-work(projet)** → **clone-chat** (clone intégral de la discussion) → **installation** (INSTALL-ECOSYSTEME.md) | directive maîtresse `1a0dffd2ae120851` |

Décisions vérifiables : registre `tmp/b13r5-install/answer-key-b13.md` (D011-D017) + D018 (boucle L005 exécutée — verified sur preuves n60b/certification de ce tour).

## E2 — Inventaire des ressources

- **Corpus canonique** `skills/@mon-ecosysteme/` : **20 fichiers** (19 + PM v3.17.0) ; archive v2.1 : 30 fichiers (20 corpus + 10 homologues) — round-trip PASS (integrity + interactions).
- **PM v3.17.0 ×3 emplacements** : corpus + miroir `skills/_prompts-maitres/` + `download/` (1362 L — plage interactions 1200-1400 respectée).
- **16 skills écosystème** (ECO_SKILLS) : gen-plan v3.17.0, correct-work 2.6.0, clone-chat 2.0.0, skills-inventory 1.0.0, skill-creator 1.0.0, agent-creator 2.0.0, script-creator 1.0.0, script-reviewer 1.0.0, audit-provenance 1.0.0, prompt-engineering 2.1.0, context-engineering 1.1.0, loop-engineering 1.0.1, graph-engineering 1.0.1, harness-engineering 1.0.1, script-mon-ecosysteme-infrastructure 1.1.0, knowledge-observer 1.0.0 — + 3 skills métier (audio-metadata, cpp-analysis, pdf-llm).
- **Journal knowledge-observer** : 6 leçons (L001-L006) — L005 validée (matérialisée), L006 appliquée (audit-provenance).
- **Arbitres recalibrés L004** : integrity 49/49, interactions 43 PASS/3 WARN/0 FAIL (WARN stables P5), verify-cross 56/56 ×2 modes, verify-correct-work 16/16, answer-key-checker 16/16, n60b 12/12.
- **Audit de provenance** : 214 artefacts écosystème scannés, 189 tracés, 25 scripts documentés (idempotence ×2 no-op), 33 orphelins résiduels assumés v1.0.0 (rapport `tmp/b13r5-install/rapport-audit-provenance-fix2.json`).

## E3 — Classification

**Type 4** (orchestration / traitement local) — livrable plan markdown ; aucune interface web, aucun document bureautique.

## E4 — Estimation #token

| Phase | Objet | Estimation |
|-------|-------|-----------|
| N22-N26 | ✅ FAITES (B13-r5/r6) — clôture, L005, M1-M2, script-creator, homologues + RÉVERDICT | 0 (restant) |
| N27 | ✅ FAITE (B13-r6) — audit-provenance v1.0.0 + L006 + fix 25 artefacts | 0 (restant) |
| N28 | ✅ FAITE (B13-r6) — v3.17.0 + n60b + PM ×3 + corpus 20 + boucle L005 | 0 (restant) |
| N29 | Clone intégral de la discussion via clone-chat (méthode 7+1 étapes, 8 checks §0-§5) | 12000 #token |
| N30 | Installation selon INSTALL-ECOSYSTEME.md (audit de provenance préalable L006, G-RES) | 10000 #token |
| Maintenance | Worklog + re-validation E13 | 500 #token/tour |

## E5 — Sélection des skills

| Skill | Usage | Version plancher |
|-------|-------|-----------------|
| gen-plan | Méthode E1-E15, règles d'or, hooks (E1-RES actif) | 3.17.0 |
| correct-work | Hook E8 + correct-work(projet) post-construction | 2.6.0 |
| clone-chat | Clone intégral de la discussion (N29) | 2.0.0 |
| audit-provenance | Pré-clone / pré-installation (L006) | 1.0.0 |
| resource-monitor | G-RES — collectes R-RES1 en continu | 1.0.0 |
| knowledge-observer | E15 (M1-M2), journal leçons | 1.0.0 |
| Arbitres mécaniques | certification-complete.py, n60b, answer-key-checker | — |

## E6 — Profilage ressource

**NORMAL** — signaux de pression : aucun (disque 8,7 Go > 5, 0 timeout consécutif, budget < 80 %). **G-RES active** : collecte à l'ouverture/fermeture de chaque phase et à chaque signal (R-RES1) ; adaptation autonome en cascade au blocage (R-RES3) ; mise à jour optimisée du plan via gen-plan si structurel (R-RES4) ; objectif final intangible (R-RES5).

---

## E7 — LE PLAN (phases restantes)

> Philosophie : exécution série par défaut (§1.4 #4). Toute phase terminée → hook correct-work (§5.4). Idempotence R1-R6 sur chaque écriture. G-RES sur toutes les phases.

### N22-N28 — ✅ FAITES (B13-r5 → B13-r6)

- N22 clôture, N23 règle L005, N24 M1-M2, N25 script-creator (verdict CIBLE round 2 PASS, test bout en bout, KB famille), N26 homologues v2.1 + RÉVERDICT 5/5 ×2, N27 audit-provenance + L006, N28 v3.17.0 (KO-L005 + E1-RES + n60b + PM ×3 + corpus 20) — détails : worklog Tasks 43-44-45, plan B13-r6 historisé.

### N29 — Clone intégral de la discussion (clone-chat, directive `1a0dffd2ae120851`) — ✅ FAITE (Tasks 46-47 : clones -a + -b, 8/8 checks ×2)

1. Pré-clone : audit de provenance (audit-provenance — L006 : l'audit est exécuté AVANT tout clone) + collecte G-RES (R-RES1).
2. Exécuter la méthode clone-chat v2.0.0 : 7+1 étapes, 8 checks, ordre imposé, §0-§5, Context Drift §3.5 (mode CIBLE), nom descriptif du clone.
3. Couverture : contexte, décisions, artefacts, worklog Tasks 1-45, plans B12/B13, directives (traces), lignage wipes/restaurations.
4. Vérification : 8 checks clone-chat + verdict correct-work (mode CIBLE sur le clone) + worklog.

### N30 — Installation de l'écosystème (INSTALL-ECOSYSTEME.md, directive `1a0dffd2ae120851`) — ✅ FAITE (Task 47 : PM-INSTALL 11/11 ×2, rapport download/rapport-installation-ecosysteme-b13-r7.json)

1. Pré-installation : collecte G-RES + snapshot de sécurité (L002) + re-vérification arbitres.
2. Suivre les protocoles INSTALL-ECOSYSTEME.md (pipeline PM-INSTALL) — corpus 20, ECO_SKILLS 16, PM v3.17.0.
3. Post-installation : integrity ×2 + certification ×2 + answer-key-checker + audit de provenance post-installation (L006).
4. Clôture : worklog final + verdict Global.

---

## E8 — Validation du plan

- **Arbitre answer-key-checker** (16 checks) : re-exécuté après génération — verdict requis PASS.
- **Validation mécanique** de la clé b13 : parse YAML-safe + comptage statuts (D011-D017 + D018).
- **Hook correct-work E8** : correct-work(projet) exécuté après N29 (couvre la construction complète + le clone) — conformément à la directive `1a0dffd2ae120851`.
- Critères S1/S2 : D011, D012, D016 — tous `verified` (D018 verified sur preuves n60b ×2 + certification ×2 de ce tour).

## Bloc REPRISE B13-r7 (auto-suffisant)

Au prochain « continue » (ordre de priorité) :
0. **Hook E1-RES** (reconstitué n67-1) : (1) lecture seule B-11 (worklog Task 45 fait foi) ; (2) collecte G-RES `python skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor/state.json` → verdict → mode ; (3) fraîcheur du plan : ce plan est généré via v3.17.0 (n60b 12/12 ×2) — frais, aucune re-génération requise tant que gen-plan n'est pas re-modifiée (L005).
1. **N29 ✅ FAITE** (Tasks 46-47) — clones `-a` (Task 46) et `-b` (Task 47, post-relecture intégrale), 8/8 checks ×2 ; relecture intégrale exécutée (Tasks 1-46, 1 189 L).
2. **N30 ✅ FAITE** (Task 47) — G-RES + snapshot L002 (43 Mo) → pipeline PM-INSTALL §2 **11/11 ALL PASS ×2** → post-installation : certification 5/5 ×2 + audit de provenance ×2 (sha16 stable) → clôture Task 47 + statuts plan.
3. Si gen-plan est re-modifiée et jugée valide : boucle **L005** automatique (arbitres → version → recalibrage → certification → re-génération du plan → E8).
4. G-RES en continu (R-RES1 à R-RES5) ; l'objectif final (clone → installation) est **ATTEINT** (Task 47, directive maîtresse `1a0dffd2ae120851`) ; clone -c post-installation ✅ FAIT (Task 48 — 8/8 checks ×2) ; **aucune phase armée restante** (mode maintenance : hook E1-RES + boucle L005 conditionnelle + auto-clonage §5) ; **maintenance exécutée** ✅ (Task 49, trace `1a0e0560cdac76a1` : hook E1-RES OK/G-RES PARALLELE, n60b 12/12 ×2 → L005 NON déclenchée, clone -d 8/8 ×2) ; **3 tests gen-plan + 3 rapports illustrés** ✅ (Task 50, trace `1a0e074494548cd9` : T1 disciplines × PARALLELE ×1,47 / T2 pipeline E1-E15 / T3 surcharge réelle + timer — ALL PASS ×2 chacun, harnais `scripts/t50-*` rejouable, clone -e 8/8 ×2).
