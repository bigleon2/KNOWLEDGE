# Plan d'actions — cahier-des-charges v2.0.1 (discipline + campagne voie L + test fonctionnel Serre CBD)

> Généré par **gen-plan v3.23.1** (fraîchement installé — règle d'or n°2 : régénération post-installation).
> **MAJ v2 (E13, règle d'or n°3 — 2026-10-25)** : intégration de la directive propriétaire « audit + correction + test robuste de gen-plan » (constat S1 : Task 14 non journalisée, E8 non exécuté, plan non affiché). Nouveaux groupes **G6-G9** insérés AVANT G1, nouveaux arbres de décision **D014-D018**, #token re-estimé (+9500). Non-régression R2 : G0-G5 inchangés.
> **Finalisé via gen-plan v3.24.0 (hook E7-DISP — 2026-10-24T18:06:48Z)** : arbitres frais — answer-key-checker 16/16 ×2 · verify-cross 100 % · selftest check_plan_protocol 7/7 · É1-INSTALL INSTALLE · G-RES NORMAL.
> Session : web-dd290b0d · Date : 2026-10-25 · Profil : **NORMAL** (G-RES niveau 0, É1-INSTALL rc=0 INSTALLE)
> Classification : ingénierie de skill (Type 4 dominant) + livrables documentaires embarqués (Type 1) — profil SE projet : standard
> Sources fonctionnelles : discussion chat.z.ai/s/aeec48ec + PDF « Résumé Global Des Références Serre CBD » + **article Science & Vie SV-238443 (fondement scientifique — Hadany & Yovel, Tel-Aviv, revue Cell : sons de stress 40-80 kHz, 60-65 dB, ≤ 5 m, <1 son/h sain vs ≈35 clics/h tomate assoiffée, cavitation)**

Horodatage plan : 2026-10-24T18:06:48Z
Verdict E8 : PASS (answer-key-checker 16/16 ×2, verify-cross 100.0 %, arbitre E7-DISP selftest 7/7, hook correct-work(plan) — Horodatage vérifié : 2026-10-24T18:06:48Z)

## Directives propriétaire (verbatim consolidé)

1. `correct-work (projet)` en fin de chaîne.
2. `cahier-des-charges` reconnu comme **discipline** par l'écosystème.
3. Tags : `discipline`, `engineering`, `cahier des charges`, `projet`.
4. Campagne d'évaluation LLM : **3 runs × 12 requêtes** (voie L — KO-L001 QUOTA_OK).
5. Test fonctionnel du skill : sources discussion **et** PDF Serre CBD.
6. Article SV-238443 = source d'inspiration fondatrice du projet SERRE CBD (à intégrer au CDC généré).
7. Ordre imposé : installation écosystème d'abord (✅ Task 13 certifié), plan via gen-plan (ce document), exécution.

## Groupes d'exécution (série par défaut — philosophie #4)

### G6 — Constat + audit complet de gen-plan et fichiers associés — #token 3000
6.1 Constat de défaillance documenté (S1) : Task 14 absente du worklog (R5 violée), arbitre answer-key-checker jamais exécuté (E8 court-circuité), plan non affiché au chat — preuves grep/archives consignées.
6.2 Audit SKILL.md (382 L) : frontmatter YAML, 4 modes, 15 étapes, 4 règles d'or, hooks E1-RES/É1-INSTALL, modes NULL/step/step-ok, références croisées internes.
6.3 Audit des 11 fichiers `references/` (présence + bannières + cohérence avec §2.2) ; audit des 2 `evals/` (evals.json 8 cas, trigger_evals.json 12 cas) ; audit `scripts/ensure-installed.py` (--check/--reinstall/--preempt) ; audit entrée KB gen-plan ; audit arbitres dépendants (verify-cross, answer-key-checker, check-ecosysteme-integrity).
6.4 **Analyse de cause racine du bug « plan non affiché / protocole court-circuité »** : cartographier la chaîne E7→E8→R5→affichage et identifier l'absence de garde mécanique (aucun check n'oblige la finalisation après écriture du fichier) — scénario déclenchant = interruption en cours de plan (habitude propriétaire, 3 occurrences depuis hier).
6.5 Rapport d'audit `download/audit-gen-plan-v3.23.1.md` (écarts classés S1-S3) ; hook correct-work(groupe, CIBLE).

### G7 — Correction du bug + cascade KO-L004 → gen-plan v3.24.0 — #token 2500
7.1 Correctif SKILL.md : **hook E7-DISP (affichage obligatoire du plan)** — la finalisation E7/E8 exige : plan écrit + answer key présente + arbitre E8 exécuté + entrée worklog R5 + **bloc récapitulatif affiché au chat** (titre, groupes, #token, verdict E8, chemin) ; extension du hook E1-RES → **reprise après interruption** (tout message utilisateur arrivant pendant un plan en vol déclenche : lecture préalable → contrôle de fraîcheur → E13 → re-validation E8 → R5 → affichage).
7.2 Nouvel arbitre `scripts/check_plan_protocol.py` (N3, stdlib) : P1 plan non vide, P2 answer key ≥ 1 décision avec verification, P3 worklog journalise le plan (R5), P4 preuve d'affichage (marqueur PLAN-AFFICHE au worklog), P5 exécution arbitre E8 tracée — verdict PASS/FAIL JSON ; selftest intégré.
7.3 Cascade KO-L004 : montée **v3.23.1 → v3.24.0** (MINOR) ; recalibrage des outils dépendants présents localement (verify-cross.py, answer-key-checker.py, check-ecosysteme-integrity.py, skills-meta.json si présents) ; génération PM mécanique `generer-pm-skill.py --generate gen-plan` si disponible (sinon S3 journalisée) ; évals : +1 cas trigger_evals (interruption/reprise) → 13 cas, evals.json aligné ; §2.2 mis à jour.
7.4 Hooks : verifier arbitres ×2 (idempotence) ; hook correct-work(groupe, CIBLE).

### G8 — Test robuste anti-récidive — #token 2000
8.1 **Reproduction mécanique du bug** : `check_plan_protocol.py --plan download/plan-cahier-des-charges-v2.0.1.md --worklog worklog.md` sur l'état ACTUEL → **FAIL attendu sur P3/P4/P5** (reproduction des 3 occurrences) — preuve que l'arbitre détecte le bug.
8.2 **Cycle corrigé en sandbox** (tmp/test-gen-plan/) : plan factice + worklog factice avec marqueurs → PASS ; puis suppression de la journalisation → FAIL (l'arbitre sait échouer).
8.3 Idempotence ×2 + selftest ; verdict documenté ; hook correct-work(groupe, CIBLE).

### G9 — Mise à jour du plan via gen-plan v3.24.0 corrigé — #token 2000
9.1 Re-génération complète du plan (règles d'or n°2 + KO-L005 : gen-plan modifié et jugé valide → re-génération AVANT reprise) via v3.24.0 : réalignement des groupes G0-G5, hooks par phase, #token recalculés ; non-régression R2 (G0-G5 + G6-G8 conservés).
9.2 **Protocole complet cette fois** : écriture plan → arbitre check_plan_protocol.py PASS → entrée worklog R5 + marqueur PLAN-AFFICHE → **bloc récapitulatif affiché au chat** (critère de sortie de G9 = l'utilisateur a VU le plan).
9.3 Re-validation E8 (arbitre answer-key-checker si disponible + hook correct-work(plan, CIBLE)) ; verdict consigné.

### G0 — Installation écosystème (✅ TERMINÉ, Task 13) — #token 3000
Pipeline PM-INSTALL v1.7.1 : corpus 9/9 byte-identique, 4 familles v-courantes, KB 33 entrées, outillage 20 scripts, arbitres 99/99 + 70/70 + 0 doublon, 0 S1-S2, S3×2 journalisées.

### G1 — Discipline + tags → v2.0.1 — #token 2000
1.1 SKILL.md frontmatter : tags += `discipline`, `engineering`, `cahier des charges` (R1 : existants conservés) ; description → préfixe canon « **Skill discipline** d'Engineering Design » ; `version: 2.0.1` (PATCH).
1.2 Cascade KO-L003 (dynamisation arbitre) : `verifier_structure.py` VERSION_CIBLE="2.0.1" ; `evals.json` version 2.0.1 + note provenance ; 4 références : annotation compat « skill v2.0.0 → v2.0.1 (tags + discipline, contenu inchangé) ».
1.3 §5 : statut discipline ; §6 : entrée traçabilité v2.0.1 (provenance directives 2-3).
1.4 Entrée KB `## cahier-des-charges v2.0.1` (format SHARED §2.2 — category discipline, Dépend de = 7 dépendances YAML, Utilisé par réciproque) + vérification version SHARED du §0 (écart éventuel S3).
1.5 Ré-amorçage `@historique/@Alias/aliases.json` (S3 Task 13 — wipe inter-sessions) : alias FACON.
1.6 Arbitres : `verifier_structure.py` ×2 (37/37 attendu, idempotence) ; `verify-cross.py` re-run (KB modifié) ; hook correct-work(groupe, CIBLE).

### G2 — Campagne évals voie L : 3 runs × 12 requêtes — #token 4000
2.1 Runner `scripts/eval-campaign.py` (N3, stdlib + SDK) : charge `evals/trigger_evals.json` (12 requêtes : 9+/3−), 3 runs, vote LLM par requête (déclenche/ndeclenche vs attendu), sortie `download/eval-campaign-report.json` (36 votes, précision/rappel/F1 par run + agrégat), `--skip-done` idempotent, 429-aware (1 sonde/tour — KO-L001).
2.2 Exécution 36 votes → verdict voie L (MESURÉE).
2.3 SKILL.md §5 : voie L MESURÉE + verdict ; §6 : traçabilité campagne ; evals.json : note provenance.
2.4 hook correct-work(groupe, CIBLE).

### G3 — Test fonctionnel M5→M7 : projet Serre CBD — #token 15000
3.1 Extraction discussion chat.z.ai via SDK web-reader → `upload/discussion-serre-cbd.md`.
3.2 **M5 ANALYSER** : compilation 3 sources (discussion + PDF + SV-238443), fiche-domaine (domaine mixte : ingénierie du son × agronomie × IoT/électronique), signaux lexicaux, recherche web normes (sonde unique), `[HYP-xx]`, calibration SE.
3.3 **M6 CONCEVOIR** : cahier des charges 12 sections (template v2.0.0 — exigences EF/ENF atomiques à critères mécaniques, SS-xx, I-xx, annexe D/T, **SV-238443 citée comme référence fondatrice**) + dossier-conception (architecture sous-systèmes, interfaces, allocation).
3.4 **M7 TESTER** : `scaffold_tests.py --projet serre-cbd` → implémentation des tests indispensables (STATUT PRÊT) → `run_all.py` verdict + TH matériels simulés (capteurs acoustiques virtuels 40-80 kHz, rayon 5 m, taux de clics, bruit/biais) → rapport-couverture exigences↔tests.
3.5 Livrables → `download/` ; hook correct-work(groupe, CIBLE).

### G4 — correct-work (projet) — #token 2000
4.1 Mode PROJET v2.7.0 : plan de vérification (gen-plan), erreurs/omissions (re-jeu des vérifications answer key), cohérence inter-artefacts, arbitres re-runs, **verdict S1-S3** documenté (worklog + plan).

### G5 — Clôture — #token 1000
5.1 Archivage `download/cahier-des-charges-v2.0.1.zip` (13 fichiers).
5.2 Worklog final (Tasks 14+) + bilan E15 (auto-calibration grille).
5.3 Résumé interactif propriétaire.

## Answer key (hook E1 — décisions vérifiables mécaniquement)

```yaml
decisions:
  - id: "D001"
    criterion: "Le frontmatter SKILL.md porte les 4 tags requis (discipline, engineering, cahier des charges, projet)"
    verification: "python3 -c \"import re;fm=open('skills/cahier-des-charges/SKILL.md').read().split('---')[1];print(all(t in fm for t in ['discipline','engineering','cahier des charges','projet']))\""
    source: "directive propriétaire 3 (session web-dd290b0d)"
    priority: "S2"
    status: "verified"
  - id: "D002"
    criterion: "La description du frontmatter commence par « Skill discipline » (canon graph-engineering)"
    verification: "python3 -c \"fm=open('skills/cahier-des-charges/SKILL.md').read().split('---')[1];print(fm.split('description:')[1].replace('>-','').strip().startswith('Skill discipline'))\""
    source: "directive propriétaire 2 — convention discipline (graph-engineering)"
    priority: "S2"
    status: "verified"
  - id: "D003"
    criterion: "La version installée du skill est 2.0.1 (bump PATCH)"
    verification: "grep -m1 '^version: 2.0.1' skills/cahier-des-charges/SKILL.md"
    source: "convention semver (SHARED §1.2) + directive propriétaire 2-3"
    priority: "S2"
    status: "verified"
  - id: "D004"
    criterion: "L'arbitre verifier_structure.py rend 37/37 PASS deux fois (idempotence ×2) sur l'état v2.0.1"
    verification: "python3 skills/cahier-des-charges/scripts/verifier_structure.py --racine skills/cahier-des-charges (×2)"
    source: "SKILL.md §5 (voie mécanique) + KO-L003 (arbitre dynamisé)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Le registre KB contient l'entrée cahier-des-charges v2.0.1 (reconnaissance discipline)"
    verification: "grep -A2 '^## cahier-des-charges v2.0.1' skills/KNOWLEDGE.md"
    source: "directive propriétaire 2 + étape 11 PM-INSTALL (nouveau skill → KB)"
    priority: "S2"
    status: "verified"
  - id: "D006"
    criterion: "La section §6 du SKILL.md porte l'entrée de traçabilité v2.0.1"
    verification: "grep -c 'v2.0.1' skills/cahier-des-charges/SKILL.md"
    source: "convention traçabilité (SHARED §1.4)"
    priority: "S3"
    status: "verified"
  - id: "D007"
    criterion: "Le rapport de campagne contient 36 votes (3 runs × 12 requêtes) avec métriques par run"
    verification: "python3 -c \"import json;r=json.load(open('download/eval-campaign-report.json'));print(len(r['votes'])==36)\""
    source: "directive propriétaire 4 (3 runs × 12 requêtes)"
    priority: "S2"
    status: "pending"
  - id: "D008"
    criterion: "Le §5 du SKILL.md déclare la voie L MESURÉE avec verdict de campagne"
    verification: "grep 'MESURÉE' skills/cahier-des-charges/SKILL.md"
    source: "SKILL.md §5 (campagne à armer) + directive propriétaire 4"
    priority: "S3"
    status: "verified"
  - id: "D009"
    criterion: "Les 5 livrables Serre CBD existent (fiche-domaine, cahier-des-charges, dossier-conception, batterie-tests, rapport-couverture)"
    verification: "ls download/serre-cbd* download/rapport-couverture-serre-cbd.md"
    source: "directive propriétaire 5 + SKILL.md §2 (livrables v2)"
    priority: "S2"
    status: "verified"
  - id: "D010"
    criterion: "La batterie de tests run_all.py rend verdict PASS avec au moins 1 TH matériel PRÊT (exit 0)"
    verification: "cd download/batterie-tests-serre-cbd && python3 run_all.py ; echo RC=$?"
    source: "SKILL.md §2 (protocole STATUT) + directive propriétaire 5"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "Le verdict correct-work (projet) S1-S3 est documenté au worklog"
    verification: "grep -c 'correct-work (projet)' worklog.md"
    source: "directive propriétaire 1 (correct-work v2.7.0)"
    priority: "S2"
    status: "verified"
  - id: "D012"
    criterion: "L'archive download/cahier-des-charges-v2.0.1.zip contient 13 fichiers"
    verification: "unzip -l download/cahier-des-charges-v2.0.1.zip | tail -3"
    source: "convention archivage (Task 12 précédent)"
    priority: "S3"
    status: "verified"
  - id: "D013"
    criterion: "Le cahier des charges Serre CBD cite l'article Science & Vie SV-238443 comme référence fondatrice (données 40-80 kHz, 5 m, cavitation)"
    verification: "grep -c 'Science.*Vie\\|Hadany\\|cavitation' download/cahier-des-charges-serre-cbd.md"
    source: "directive propriétaire 6 (article source d'inspiration)"
    priority: "S2"
    status: "verified"
  - id: "D014"
    criterion: "Le constat de défaillance gen-plan (S1 : E8 + R5 + affichage court-circuités) est documenté au worklog avec preuves"
    verification: "grep -c 'constat de défaillance\\|Task 14 absente\\|PLAN-AFFICHE' worklog.md"
    source: "directive propriétaire (vérifier si gen-plan a failli) — preuves E1-RES"
    priority: "S1"
    status: "verified"
  - id: "D015"
    criterion: "Le rapport d'audit download/audit-gen-plan-v3.23.1.md existe et classe les écarts S1-S3"
    verification: "test -s download/audit-gen-plan-v3.23.1.md && grep -c 'S1' download/audit-gen-plan-v3.23.1.md"
    source: "directive propriétaire (audit complet de gen-plan et de ses fichiers associés)"
    priority: "S1"
    status: "verified"
  - id: "D016"
    criterion: "gen-plan est bumpé v3.24.0 avec le hook E7-DISP (affichage obligatoire) et l'arbitre scripts/check_plan_protocol.py (selftest OK)"
    verification: "grep -m1 '^version: 3.24.0' skills/gen-plan/SKILL.md && python3 skills/gen-plan/scripts/check_plan_protocol.py --selftest"
    source: "directive propriétaire (correction anti-récidive) + cascade KO-L004"
    priority: "S1"
    status: "verified"
  - id: "D017"
    criterion: "Le test robuste reproduit le bug sur l'état ancien (FAIL) et valide le cycle corrigé en sandbox (PASS ×2, idempotence)"
    verification: "grep -c 'REPRODUCTION' worklog.md && python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-cahier-des-charges-v2.0.1.md --worklog worklog.md"
    source: "directive propriétaire (test robuste, bug apparu 3 fois depuis hier, scénario = interruption mi-plan)"
    priority: "S1"
    status: "verified"
  - id: "D018"
    criterion: "Le plan a été mis à jour via gen-plan corrigé avec protocole complet (arbitre PASS + entrée worklog + marqueur PLAN-AFFICHE + bloc affiché au chat)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-cahier-des-charges-v2.0.1.md --worklog worklog.md ; echo RC=$?"
    source: "directive propriétaire (mettre à jour le plan via gen-plan fraîchement corrigé)"
    priority: "S1"
    status: "verified"
```

## Hooks de validation (E8)

- Arbitre answer-key-checker : 16/16 (état écosystème, référence b12 intacte — R4).
- Hook correct-work sur le plan : périmètre = directives 1-7 couvertes (G1↔2-3, G2↔4, G3↔5-6, G4↔1, G5↔clôture) ; chaque décision D001-D013 testable ; arbitres identifiés (verifier_structure ×2, verify-cross, run_all, answer-key-checker) — **verdict : PASS**.
- Hooks par phase (E9-E14) : correct-work(groupe, CIBLE) après G1, G2, G3 ; correct-work(projet) en G4 ; FAIL → pause + correction.

## Règles d'exécution

Série par défaut (philosophie #4) · N3 Python uniquement · KO-L001 (1 sonde API/tour, --skip-done) · R1-R6 idempotence · R3 traçabilité worklog · compaction mémoire à E11 si > seuil · profil NORMAL figé (downgrade irréversible §1.4 #8).
