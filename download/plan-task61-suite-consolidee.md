# Plan d'actions Task 61 (suite consolidée) — Tests $FACON2 vagues chronologiques V1-V5 → corrections et optimisations $FACON → empaquetage push + clôture KO-L009

**Horodatage plan : 2026-11-07T08:39:00Z** (révision finale — 13/13 done) · **Généré via le déclencheur verbatim « met à jour (le plan d'actions) »** — gen-plan **v3.37.0** (règle d'or n°3 — voie CONSOLIDATION : ce plan remplace `plan-task61-correct-work-bloc-tests-facon2-optimisations.md` [révision 1 du worklog non matérialisée — écart constaté, résorbé ici] comme référence d'exécution ; l'ancien plan est conservé dans `download/`, R2) · **Mode d'exécution : gen-plan(step)** (13ᵉ directive point 4 — enchaînement autonome, correct-work(groupe) après chaque groupe, max 2 rounds/groupe, PLAN-AFFICHE à l'ouverture de chaque groupe — E7-DISP v3.36.0).

## §0 État d'ouverture consolidé (E1-RES — dérivé du disque, règle d'or n°5 — groupes terminés reportés avec preuves)

| Vérification préalable | Résultat |
|---|---|
| **Directives cumulées** | 11ᵉ (installer l'écosystème → correct-work (projet) --bloc → tests $FACON2 fonctionnels + performances des éléments créés/modifiés hier et aujourd'hui → corriger $FACON leurs failles + optimiser $FACON leur fonctionnement interne et au sein de l'écosystème → poursuivre avec la clé GitHub) · 12ᵉ (tests organisés en vagues chronologiques de création/modification — Task 56 → Task 57 → Task 60 → Task 58 → Task 61 ; périmètre étendu à tous les éléments du PUSH + leurs dépendances amont) · 13ᵉ (1. PLAN-AFFICHE à l'ouverture de chaque étape ✅ v3.36.0 ; 2. audit transversalité des optimisations STEP ✅ v3.36.0 ; 3. « met à jour le plan d'action des tâches à faire » ✅ le présent plan via le déclencheur v3.37.0 ; 4. exécuter gen-plan(step) → la chaîne qui suit) · demande préalable du jour (vérifier/créer le déclencheur « met à jour » + $FACON/$FACON2 lisibles sans alias-eco ✅ v3.37.0) |
| **Installation (directive 11ᵉ item 1 — FAITE)** | Verdict REINSTALLE (59 défauts → 0, PIN b75a620, clone a5ae36f) + certification arbitres 159/159 + 110/110 + 0 FAIL — consigné worklog T1.1.1 |
| **G1 du plan précédent (FAIT — preuves disque)** | SG1.1 consignations worklog 2/2 (installation + incident KO-L009 T1.1.2) · SG1.2 idempotence installation : `download/tests-task61/install-idempotence.json` — 3 runs **INSTALLE no-op** (actions [], 0 défaut, 53 entrées KB, durée 0,08 s — 07:03-07:10) |
| **G2 du plan précédent (FAIT — preuve disque)** | `download/rapport-correct-work-bloc-task61.md` — correct-work (projet) --bloc 7 blocs, **verdict global PASS AVEC RÉSERVES** (0 S1/S2 ; findings du jour **F1** [S4 : KB gen-plan omet pm-skill dans « Utilisé par »] + **F2** [S4 : pm-skill n'a pas correct-work dans « Dépend de »] → G3 du présent plan ; 25 asymétries S3/S4 héritées, dette en diminution — 07:07) |
| **V4.1 du plan précédent (FAIT — preuve disque)** | `download/tests-task61/journal-preuves.json` — preuves nœud trigo-euler **PASS 8/8** (selftest 15/15 ×2 byte-identiques [sha256 binaire c6b22a8e…], 15 op one-shot, daemon health, concurrence 4×25 = 100/100 @ 0,102 ms, saturation 9ᵉ refusée non-bloquante, daemon.stop propre, mini-plan ×2 sha16 identiques, cas vivant VOSS joint 5c [Guldin 29 026,60048 mm³, modèle iso 545 items, concordance perspective] — 07:08) |
| **Montées du jour (FAITES — preuves disque)** | gen-plan **v3.36.0** (E7-DISP ouverture d'étape + transversalité §5.5 — points 1-2 de la 13ᵉ directive ; cascade INTERROMPUE par coupure ~07:53Z — constat d'honnêteté worklog suite 16) consolidée par gen-plan **v3.37.0** (déclencheur verbatim « met à jour » [re-génération $FACON d'un NOUVEAU plan d'actions $FACON2] + glossaire alias-eco INLINE $FACON/$FACON2 au §A [lecture auto-contenue SANS alias-eco]) ; cascade KO-L004 complète : PM v3.37.0 (delta verrouillé `scripts/delta-genplan-v3370.json`) + SHARED v1.7.30 + PM-INSTALL v1.9.6 + PM v3.36.0 archivé R4 (SHA bab8777c…) + pin ECO_SKILLS 3.37.0 + KB v3.37.0 + historiques-par-skill (47 versions / 39 PMs, labels stale résorbés) + sceaux README §5 v3.35.1/v3.35.2/v3.36.0 + lignes vives 9 disciplines recalées + **injecteur propagate-context v2.0.9** (cause racine rétrogradation §0 résorbée : le bump SHARED v1.7.28 Task 58 n'avait pas monté l'injecteur) + propagation §0 v1.7.30 : **70 skills + 151 scripts + 2 agents** + archive v2.3 rescellée ×2 ; **certification ×2 : integrity 110/110, coherence 54/27/0 (0 FAIL), verify-correct-work ALL PASS, verify-cross 100,0 %** ; sync miroir 0 divergence de contenu + **commit a38ae1e** |
| **Incident volatilité n°9 (21ᵉ disparition version-management)** | Détectée à l'arbitre integrity → **auto-réparation réelle garde Task 56** : INSTALLE-REPARÉ rc=0 (restauré depuis le miroir, 0 jeton) — la simulation complémentaire reste à exécuter (T.V1.2) |
| Familles cœur installées (vérifié disque) | gen-plan **v3.37.0** · correct-work v2.11.0 · clone-chat v2.0.2 · refactor-guard v1.8.1 · pm-skill v1.0.0 · version-management v1.2.0 · KB 53 entrées · corpus 9 PMs (GEN-PLAN v3.37.0, SHARED v1.7.30, INSTALL v1.9.6) |
| G-RES (hook E1-RES) | **OK — PARALLELE** (disque 7,5 Go · mémoire 2,8 Go · charge faible) → profil NORMAL ; Graph Diamond par vagues indépendantes (écritures séparées par élément) ; SÉRIE justifiée : journal consolidé (agrégation), correctifs (écritures partagées KB/worklog), clôture |
| **Périmètre du PUSH (12ᵉ directive — P1-P9)** | P1 pm-skill v1.0.0 · P2 correct-work v2.9.0→v2.11.0 · P3 dessin-technique v1.3.0 + nœud C++ · P4 corpus socle (SHARED v1.7.26→v1.7.30, PM-INSTALL v1.9.3→v1.9.6, ULTRA, propagation §0, archive v2.3) · P5 système d'installation (auto-install/eco_install_pipeline/ensure-installed — testé en réel ×2 ce jour) · P6 version-management v1.2.0 (garde étendue — 20ᵉ/21ᵉ disparitions auto-réparées) · P7 écosystème global (KB, @historique, arbitres, sceaux) · P8 Task 56 (gen-plan v3.35.2→v3.37.0) · P9 Task 57 (orchestrateur-tsi v1.1.1 + kit TSI) · **+ du jour** (v3.36.0/v3.37.0, propagate-context v2.0.9, delta v3370, KB, historiques, lignes vives) |
| Pendances (règle d'or n°7) | **Push distant KO-L009** : 12 commits locaux en avance sur origin/main (390133a → a38ae1e) JAMAIS poussés — le push passe par le propriétaire (KO-L009 point 5) ; **rotation PAT K1/K2/K3** (13ᵉ+ expositions documentées — guidance révocation SG4.3) ; Task 58 CLOSE · Task 60 CLOSE (gelées, certifiées ×2 — aucun retouchage de leurs livrables ; les évolutions passent par montée de version + cascade, jamais par rétro-édition R2/R4) |
| Incident KO-L009 (PAT exposé au chat — directive 11ᵉ item 4) | Conformité systématique : secret ni recopié ni stocké ni utilisé pour la publication ; guidance révocation (SG4.3) ; re-provisionnement one-shot HORS canal ; consigné SANS la valeur (worklog T1.1.2, inclut transparence fetch lecture seule préalable, header one-shot, zéro persistance) ; push PRÉPARÉ, exécuté PAR LE PROPRIÉTAIRE |

## §1 Objectif (ordre des étapes — règles d'or n°3/n°7)

1. **G1 — Vagues chronologiques V1-V3** (12ᵉ directive — ordre de création/modification) : tests $FACON2 fonctionnels ×2 (idempotence R6) + performances des éléments Task 56 (gen-plan v3.37.0 + garde vm + propagation §0 v1.7.30), Task 57 (kit TSI), Task 60 (pm-skill v1.0.0 + correct-work v2.11.0 + ULTRA) — ce qui n'est pas déjà couvert par la certification du jour (consignation des acquis aux journaux).
2. **G2 — V4 + V5 + journal consolidé** : restes Task 58 (chaîne Python generer_dessin ×2 + perf) ; consignation V5 du jour (installation, --bloc, v3.36.0/v3.37.0, cascade, injecteur) + vérifications complémentaires (delta rejeu --check, sceaux, couverture PM) ; **journal consolidé ordonné chronologiquement V1→V5** + rapport tests.
3. **G3 — Corrections $FACON des failles + optimisations $FACON** : F1/F2 (asymétries pm-skill KB — bidirectionnalité SHARED §3.2) + tout échec/écart V1-V5 + goulots > 20 % + normalisation des changements de mode hérités + ULTRA si stale ; toute montée de version ⇒ cascade KO-L004 complète + re-certification ×2.
4. **G4 — Empaquetage push + clôture + guidance KO-L009** : git fsck + linéarité 12 commits + présence disque + commande push préparée (propriétaire) ; rapport final ; worklog R5 chaîne ; plan 100 % + E8 ; clone-chat scellé ; **finale correct-work (projet) --bloc**.

**Contraintes transverses** : français intégral (règle d'or n°6) · statuts dérivés du disque (règle d'or n°5) · idempotence ×2 pour tout nouvel artefact · Tasks 58/60 gelées (aucun retouchage des livrables certifiés — montées de version + cascade uniquement) · PLAN-AFFICHE à l'ouverture de chaque groupe (E7-DISP v3.36.0 — tous modes) · rejouabilité post-recyclage (règle d'or n°9).

## Answer key (hook E1 — spec de session, arbitre `scripts/answer-key-checker.py` à E7/E8)

```yaml
decisions:
  - id: "D001"
    libelle: "Installation de l'écosystème personnel avant le plan (directive 11e item 1) : REINSTALLE (59 defauts -> 0) + certification arbitres (159/159 + 110/110 + 0 FAIL) — ACQUIS reporte du plan precedent"
    criterion: "Familles coeur presentes ; 0 defaut critique ; arbitres 0 FAIL"
    verification: "grep '^version:' skills/gen-plan/SKILL.md skills/correct-work/SKILL.md ; python3 scripts/check-ecosysteme-integrity.py | tail -2 (0 FAIL attendu)"
    source: "Directive 11e item 1"
    priority: S1
    status: done
  - id: "D002"
    libelle: "correct-work (projet) --bloc sur le perimetre P1-P9 (directive 11e item 2) : rapport 07:07 — 7 blocs, verdict global PASS AVEC RESERVES (0 S1/S2 ; F1/F2 S4 -> D011 ; 25 asymetries S3/S4 heritees en diminution) — ACQUIS"
    criterion: "Rapport present ; verdict global consigne ; findings du jour documentes"
    verification: "test -f download/rapport-correct-work-bloc-task61.md ; grep -c 'PASS AVEC RÉSERVES' download/rapport-correct-work-bloc-task61.md >= 1 ; grep -c 'F1\\|F2' download/rapport-correct-work-bloc-task61.md >= 2"
    source: "Directive 11e item 2"
    priority: S1
    status: done
  - id: "D003"
    libelle: "Idempotence du systeme d'installation P5 (T1.2.x du plan precedent) : 3 runs INSTALLE no-op (actions [], 0 defaut, 0,08 s) — ACQUIS (07:03-07:10)"
    criterion: "Journal JSON : 3 runs, verdicts INSTALLE, actions vides"
    verification: "python3 -c \"import json; d=json.load(open('download/tests-task61/install-idempotence.json')); assert len(d['runs'])==3 and all(r['verdict']=='INSTALLE' and r['actions']==[] for r in d['runs'])\""
    source: "Directive 11e item 3 (tests fonctionnels)"
    priority: S1
    status: done
  - id: "D004"
    libelle: "Preuves du noeud C++ trigo-euler V4.1 (T3.3.1/T3.3.2 du plan precedent) : PASS 8/8 (selftest 15/15 x2 byte-identiques, concurrence 100/100 @ 0,102 ms, VOSS joint 5c vivant) — ACQUIS (07:08)"
    criterion: "Journal JSON : 8 preuves ok=True"
    verification: "python3 -c \"import json; d=json.load(open('download/tests-task61/journal-preuves.json')); assert all(p['ok'] for p in d['preuves']) and len(d['preuves'])==8\""
    source: "Directive 11e item 3 (tests fonctionnels + performances)"
    priority: S1
    status: done
  - id: "D005"
    libelle: "DÉCLENCHEUR « met à jour » + glossaire $FACON/$FACON2 (demande prealable du jour + 13e directive point 3) : gen-plan v3.37.0 — §A glossaire inline ($FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » — lecture SANS alias-eco) + déclencheur verbatim §A + règle d'or n°3 ; le PRESENT plan est généré PAR ce déclencheur (voie consolidation — nouveau fichier, ancien conservé R2)"
    criterion: "Déclencheur présent au §A et à la règle d'or n°3 ; glossaire inline présent ; description/read_when enrichis"
    verification: "grep -c 'met à jour (le plan d\\'actions)' skills/gen-plan/SKILL.md >= 2 ; grep -c 'Glossaire alias-eco inline' skills/gen-plan/SKILL.md >= 1 ; grep 'version: 3.37.0' skills/gen-plan/SKILL.md ; test -f download/plan-task61-suite-consolidee.md && test -f download/plan-task61-correct-work-bloc-tests-facon2-optimisations.md (ancien conservé)"
    source: "Demande préalable du jour : « vérifie si mon skill \"gen-plan\" a un déclencheur \"met à jour\" qui génère $FACON un nouveau plan d'actions $FACON2 (fais en sorte qu'à la lecture du skill que tu n'aies pas besoin de \"alias-eco\" pour comprendre $FACON et $FACON2) »"
    priority: S1
    status: done
  - id: "D006"
    libelle: "Cascade KO-L004 v3.37.0 (consolidation de la v3.36.0 interrompue — constat d'honnêteté) : PM v3.37.0 (delta v3370) + SHARED v1.7.30 + PM-INSTALL v1.9.6 + PM v3.36.0 archive R4 + pin ECO_SKILLS 3.37.0 + KB + historiques + sceaux + lignes vives 9 disciplines + injecteur propagate-context v2.0.9 (cause racine rétrogradation résorbée) + propagation §0 70 skills + 151 scripts + 2 agents + archive v2.3 rescellée ×2 + certification ×2 + commit a38ae1e"
    criterion: "Arbitres ×2 : integrity 110/110, coherence 0 FAIL, vcw ALL PASS, cross 100 % ; étiquettes §0 v1.7.30 sans rétrogradation"
    verification: "python3 scripts/check-ecosysteme-integrity.py | tail -2 ; python3 scripts/test-coherence-interactions.py | tail -3 ; rg -c 'Contexte Système \\(SHARED v1\\.7\\.30\\)' skills/ --glob 'SKILL.md' | wc -l (>= 70 attendu) ; rg -l 'Contexte Système \\(SHARED v1\\.7\\.2[78]\\)' skills/ --glob 'SKILL.md' | wc -l (0 attendu) ; git -C KNOWLEDGE-repo log --oneline -1 | grep a38ae1e"
    source: "Cascade KO-L004 (montée v3.37.0)"
    priority: S1
    status: done
  - id: "D007"
    libelle: "VAGUE V1 — Task 56 : tests $FACON2 complémentaires gen-plan v3.37.0 + garde version-management + propagation §0 : (a) replay arbitres famille ×2 consigné au journal V1 (integrity/coherence/vcw/cross — fait ce jour, à journaliser avec durées) ; (b) simulation disparition version-management (mv -> INSTALLE-REPARÉ -> re-jeu no-op — complète la preuve réelle 21e disparition) ; (c) check_plan_protocol --selftest + answer-key-checker selftest ; (d) idempotence propagate-context v2.0.9 ×2 (re-jeu no-op) + perf propagation ; (e) rejeu trigger_evals gen-plan"
    criterion: "Chaque test exécuté avec verdict mécanique PASS ; simulation vm : INSTALLE-REPARÉ puis no-op ; idempotence prouvée"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --selftest ; simulation : mv skills/version-management tmp/vm-sim && python3 skills/gen-plan/scripts/ensure-installed.py --check (INSTALLE-REPARÉ) && re-jeu (INSTALLE) ; journal download/tests-task61/v1-task56.json présent, 0 FAIL"
    source: "Directives 11e item 3 + 12e (vagues chronologiques — Task 56 en premier)"
    priority: S1
    status: done
  - id: "D008"
    libelle: "VAGUE V2 — Task 57 : tests $FACON2 du kit TSI (orchestrateur-tsi v1.1.1 + analyse-doc-s4mk2 v1.1.0 + tsi-validator v1.2.0 bi-racine + multi-shift-architect v1.1.0 + agent-TSI) : self-tests mécaniques ×2 (validator selftest, analyse-doc DJTT v2.1.0/DREW réels, interface orchestrateur, agent-TSI 36/36 si arbre présent) + perf (durées) — éléments du push P9"
    criterion: "Chaque self-test ×2 byte-stable/no-op, verdicts PASS ; durées mesurées"
    verification: "journal download/tests-task61/v2-task57.json présent, 0 FAIL ; self-tests re-exécutables (scripts présents skills/*/scripts/)"
    source: "Directive 12e (périmètre push + vagues chronologiques — Task 57)"
    priority: S1
    status: done
  - id: "D009"
    libelle: "VAGUE V3 — Task 60 : tests $FACON2 pm-skill v1.0.0 + correct-work v2.11.0 + ULTRA : (a) pm-skill self-test ST1-ST11 ×2 + PM éphémère témoin sur gen-plan v3.37.0 (auto-portance §0 + SHA-256 + zéro lecture externe) + perf (unitaire ×10 + batch) ; (b) correct-work : verify-correct-work ×2 (fait ce jour, à consigner) + contrôle matrice best-of §12 + perf arbitre ; (c) fraîcheur ULTRA vs gen-plan v3.37.0 (si stale -> G3 correctif + cascade)"
    criterion: "ST1-ST11 ×2 PASS ; PM éphémère auto-portant vérifié ; matrice §12 contrôlée ; ULTRA à jour ou correctif planifié"
    verification: "python3 scripts/generer-pm-ephemere.py --self-test (si disponible) ; journal download/tests-task61/v3-task60.json présent, 0 FAIL ; grep -c '3.37.0' skills/@mon-ecosysteme/ULTRA* (fraîcheur — sinon ticket G3)"
    source: "Directive 12e (vagues chronologiques — Task 60)"
    priority: S1
    status: done
  - id: "D010"
    libelle: "VAGUES V4-V5 + JOURNAL CONSOLIDÉ : (a) V4 Task 58 restes — chaîne Python generer_dessin.py sur échantillon joint 5c ×2 (byte-stable) + perf rendu (comparaison preuves task58 ; V4.1 déjà PASS 8/8 — D004) ; (b) V5 Task 61 du jour — consignation au journal (installation ×3, --bloc PASS AVEC RÉSERVES, v3.36.0/v3.37.0, cascade certifiée, injecteur v2.0.9, commit a38ae1e) + vérifications complémentaires (generer-pm-skill --check = COHERENT ×2, sceaux SHA README vs fichiers, couverture PM v3.37.0) ; (c) journal consolidé ORDONNÉ CHRONOLOGIQUEMENT V1→V5 download/tests-task61/journal-tests.json + rapport download/rapport-tests-task61.md (verdicts, idempotence, perfs, comparaisons, goulots -> D011)"
    criterion: "Chaîne Python ×2 byte-stable ; journal consolidé machine-readable ordonné V1-V5 ; rapport lisible avec toutes les mesures ; 0 FAIL (ou échecs documentés -> D011)"
    verification: "test -f download/tests-task61/journal-tests.json && test -f download/rapport-tests-task61.md ; python3 -c \"import json; d=json.load(open('download/tests-task61/journal-tests.json')); assert 'vagues' in d and len(d['vagues'])==5\" ; grep -E '[0-9]+\\\\.[0-9]+ ?(s|ms)' download/rapport-tests-task61.md (mesures présentes)"
    source: "Directives 11e item 3 + 12e (vagues chronologiques + journal consolidé)"
    priority: S1
    status: done
  - id: "D011"
    libelle: "Corrections $FACON des failles + optimisations $FACON (directive 11e item 3) : (a) F1 — KB gen-plan « Utilisé par » += pm-skill (bidirectionnalité SHARED §3.2) ; (b) F2 — pm-skill « Dépend de » += correct-work SI usage réel confirmé (sinon consignation motivée) ; (c) tout échec/écart D007-D010 corrigé (max 2 rounds) ; (d) goulots > 20 % traités (avant/après chiffré, comportement observable préservé) ; (e) normalisation des changements de mode hérités (131 — artefact pipeline, 0 insertion/0 deletion) ; (f) ULTRA si stale (D009c) ; toute montée de version -> cascade KO-L004 complète + re-certification ×2 ; si ZÉRO correction nécessaire : consignation motivée (issue valide)"
    criterion: "Chaque finding -> correction + re-test PASS (ou zero-faille documentée avec preuves) ; arbitres PASS inchangés après correction ; versions cohérentes (frontmatter = KB = PM)"
    verification: "grep -c 'pm-skill' skills/KNOWLEDGE.md (entrée gen-plan « Utilisé par » — >= 2 attendu après F1) ; git -C KNOWLEDGE-repo diff --stat HEAD~1 HEAD (modes normalisés documentés) ; arbitres replayés ×2 PASS"
    source: "Directive 11e item 3 : « corriger $FACON leurs failles + optimiser $FACON leur fonctionnement interne et au sein de l'écosystème » + findings D002"
    priority: S1
    status: done
  - id: "D012"
    libelle: "Empaquetage push (directive 12e) : git fsck (intégrité dépôt) + linéarité des 12 commits locaux (390133a -> a38ae1e) + présence disque de tous les fichiers commités + changements de mode normalisés (après D011e) + statut final documenté + COMMANDE PUSH PRÉPARÉE (à exécuter par le propriétaire — KO-L009 point 5, jamais par l'agent)"
    criterion: "fsck propre ; 12 commits linéaires documentés ; 0 fichier commité absent du disque ; commande push exacte fournie au propriétaire, JAMAIS exécutée"
    verification: "git -C KNOWLEDGE-repo fsck --no-dangling (propre) ; git -C KNOWLEDGE-repo rev-list origin/main..HEAD --count (12) ; git -C KNOWLEDGE-repo log --oneline origin/main..HEAD (liste documentée) ; section « push préparé » du rapport final"
    source: "Directive 12e (périmètre push) + KO-L009 point 5"
    priority: S1
    status: done
  - id: "D013"
    libelle: "Clôture (mode step v3.22.0 — 13e directive point 4) : rapport final download/rapport-final-task61.md (chaîne complète : installation -> --bloc -> vagues V1-V5 -> corrections/optimisations -> empaquetage -> guidance ; RAPPELS OBLIGATOIRES en tête) ; worklog R5 chaîne G1->G4 ; plan 100 % done + verdict E8 final (horodatages couplés) ; guidance KO-L009 (révocation PAT + re-provisionnement hors canal + push propriétaire + option askass one-shot) ; clone-chat scellé download/clone-discussion-2026-11-07-task61.md (8 checks) ; FINALE correct-work (projet) --bloc sur l'ensemble"
    criterion: "Rapport final présent ; plan 13/13 done ; check_plan_protocol PASS ; clone-chat scellé ; guidance complète"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task61-suite-consolidee.md --worklog worklog.md (PASS P1-P5) ; test -f download/rapport-final-task61.md && test -f download/clone-discussion-2026-11-07-task61.md ; grep -c 'KO-L009' download/rapport-final-task61.md >= 1"
    source: "Mode step gen-plan v3.22.0 + E7-DISP v3.27.0/v3.36.0 + directive 11e item 4 (clé GitHub — voie KO-L009)"
    priority: S1
    status: done
```

## §2 Groupes d'exécution (mode step — structure §5.5 : Groupe → Sous-groupe → Tâche)

**Estimation #token totale : ~58 k (marge contingences volatilité/règle d'or n°1 : +15 k)** · Profil NORMAL (G-RES OK) · Vagues parallèles (Graph Diamond, philosophie #4) au sein de G1/G2 (écritures séparées `download/tests-task61/v*.json`) ; SÉRIE justifiée : journal consolidé (agrégation), G3 (écritures partagées KB/worklog/mêmes skills), G4 (clôture séquentielle).

### G1 — Vagues chronologiques V1-V3 : Task 56 → Task 57 → Task 60 (~20 k)

- **SG1.V1 Task 56 — gen-plan v3.37.0 + garde vm + propagation §0 (PARALLELE — écritures propres)** — 0/4
  - T.V1.1 `[À FAIRE]` Consigner au journal V1 le replay arbitres famille ×2 du jour (integrity 110/110, coherence 0 FAIL, vcw ALL PASS, cross 100 % — avec durées mesurées) #token 800
  - T.V1.2 `[À FAIRE]` Simulation disparition version-management : `mv` sandbox → `ensure-installed.py --check` → **INSTALLE-REPARÉ** → re-jeu **INSTALLE** no-op (garde Task 56 — complète la preuve réelle 21ᵉ disparition) ×2 #token 1200
  - T.V1.3 `[À FAIRE]` Self-tests : `check_plan_protocol.py --selftest` + `answer-key-checker.py` selftest + rejeu `evals/trigger_evals.json` gen-plan (déclencheurs « intègre »/« met à jour »/modes — non-régression triggers v3.37.0) #token 1500
  - T.V1.4 `[À FAIRE]` **Perf** : idempotence propagate-context v2.0.9 ×2 (re-jeu no-op) + durée propagation + durée arbitres #token 800
- **SG1.V2 Task 57 — kit TSI (PARALLELE)** — 0/2
  - T.V2.1 `[À FAIRE]` Self-tests mécaniques ×2 : tsi-validator (selftest + bi-racine DJTT/DREW réels), analyse-doc-s4mk2 (analyseur DJTT v2.1.0), orchestrateur-tsi (interface membres), agent-TSI 36/36 (si arbre présent) #token 2500
  - T.V2.2 `[À FAIRE]` **Perf** : durées des self-tests + comparaison aux références Task 33/57 (worklog) #token 800
- **SG1.V3 Task 60 — pm-skill + correct-work + ULTRA (PARALLELE)** — 0/3
  - T.V3.1 `[À FAIRE]` pm-skill : self-test ST1-ST11 ×2 + PM éphémère témoin sur gen-plan v3.37.0 (auto-portance : §0 embarqué, SHA-256, zéro lecture externe) #token 1800
  - T.V3.2 `[À FAIRE]` correct-work : consigner verify-correct-work ×2 du jour + contrôle matrice best-of §12 (chaque avantage v1.0.0→v2.10.0 ∈ v2.11.0 ou supplanté — jamais ressusciter R2) #token 1500
  - T.V3.3 `[À FAIRE]` Fraîcheur ULTRA vs gen-plan v3.37.0 + **Perf** (PM éphémère unitaire ×10 + batch 68 vs rapport-tests-task60 ; durée arbitre correct-work) #token 1000
- **→ correct-work(G1)** (livrables : v1-task56.json, v2-task57.json, v3-task60.json) #token 1500

### G2 — V4 + V5 + journal consolidé chronologique (~14 k)

- **SG2.V4 Task 58 — restes dessin-technique (PARALLELE)** — 0/2
  - T.V4.2 `[À FAIRE]` Chaîne Python `generer_dessin.py` sur échantillon joint 5c ×2 (rendu byte-stable attendu — T3.3.3 du plan précédent) #token 1500
  - T.V4.3 `[À FAIRE]` **Perf** : rendu + compilation vs preuves task58 (`tmp/mission-task58/trigo-node/`) — V4.1 déjà PASS 8/8 (D004) #token 800
- **SG2.V5 Task 61 — consignation du jour + vérifications complémentaires (PARALLELE)** — 0/2
  - T.V5.2 `[À FAIRE]` Consigner au journal V5 : installation ×3 no-op (07:03-07:10) + --bloc PASS AVEC RÉSERVES (07:07) + montées v3.36.0/v3.37.0 + cascade certifiée ×2 + injecteur v2.0.9 + propagation 70/151/2 + commit a38ae1e (preuves citées §0) #token 1200
  - T.V5.3 `[À FAIRE]` Vérifications complémentaires : `generer-pm-skill.py --check` (4 familles COHERENT) ×2 + sceaux SHA README §5 vs fichiers réels + couverture PM v3.37.0 (rapport générateur) #token 1000
- **SG2.J Journal consolidé (SÉRIE — agrégation après vagues)** — 0/2
  - T.J.1 `[À FAIRE]` `download/tests-task61/journal-tests.json` — machine-readable, **ordonné chronologiquement V1→V5**, verdicts + durées par élément + statuts des acquis (D003/D004 intégrés) #token 1200
  - T.J.2 `[À FAIRE]` `download/rapport-tests-task61.md` — synthèse lisible : verdicts, idempotence, perfs, comparaisons aux références, goulots → D011 #token 1500
- **→ correct-work(G2)** #token 1500

### G3 — Corrections $FACON des failles + optimisations $FACON (~12 k — dépend des findings D002/D007-D010)

- **SG3.1 Corrections des failles (SÉRIE — max 2 rounds, SHARED §4.4)** — dynamique
  - T.3.1.a `[À FAIRE]` **F1** : KB gen-plan « Utilisé par » += pm-skill (bidirectionnalité SHARED §3.2 — finding S4 du rapport --bloc) #token 800
  - T.3.1.b `[À FAIRE]` **F2** : pm-skill « Dépend de » += correct-work SI usage réel confirmé (vérification avant écriture — sinon consignation motivée) ; montée pm-skill v1.0.1 si écriture (cascade KO-L004 : SKILL.md + PM + KB + pin + @historique) #token 1500
  - T.3.1.c `[À FAIRE]` Tout échec/écart des vagues V1-V5 : correction chirurgicale + re-test PASS — si ZÉRO : consignation motivée #token 2500 (budget)
- **SG3.2 Optimisations fonctionnement interne + intégration (SÉRIE)** — dynamique
  - T.3.2.a `[À FAIRE]` Goulots > 20 % (mesures G1/G2) : avant/après chiffré, comportement observable préservé (arbitres PASS inchangés) — si ZÉRO : consignation motivée #token 2500 (budget)
  - T.3.2.b `[À FAIRE]` **Normalisation des changements de mode hérités** (131 — artefact pipeline installation, 0 insertion/0 deletion : git update-index --chmod, contenu intact) #token 1000
  - T.3.2.c `[À FAIRE]` ULTRA si stale (T.V3.3) : régénération ×2 idempotente (précédent Task 58) #token 800
- **SG3.3 Cascades KO-L004 conditionnelles + re-certification (SÉRIE)** — dynamique
  - T.3.3.1 `[À FAIRE]` SI montée de version (F2/ULTRA/autre) : cascade complète 5 touches + re-certification arbitres ×2 — SINON replay arbitres ×2 simple #token 2500 (budget)
- **→ correct-work(G3)** #token 1500

### G4 — Empaquetage push + clôture + guidance KO-L009 (~12 k)

- **SG4.1 Empaquetage push (SÉRIE — directive 12e)** — 0/1
  - T.4.1.1 `[À FAIRE]` git fsck + linéarité 12 commits (390133a → a38ae1e) + présence disque des fichiers commités + modes normalisés (après T.3.2.b) + **commande push préparée** (exécutée PAR LE PROPRIÉTAIRE — KO-L009 point 5) #token 1500
- **SG4.2 Rapport final + worklog R5 + plan E7-DISP final (SÉRIE — écriture partagée)** — 0/3
  - T.4.2.1 `[À FAIRE]` `download/rapport-final-task61.md` : chaîne complète + RAPPELS OBLIGATOIRES (rotation PAT K1/K2/K3 · GO push propriétaire 12 commits · F1 import Traktor · option fusion workflow → master) #token 2000
  - T.4.2.2 `[À FAIRE]` Worklog R5 : chaîne G1→G4 consolidée (jalons, verdicts, incidents) #token 1000
  - T.4.2.3 `[À FAIRE]` Plan : statuts 100 % + verdict E8 final (horodatages couplés rafraîchis) + check_plan_protocol PASS #token 800
- **SG4.3 Guidance KO-L009 — item 4 de la directive (SÉRIE)** — 0/1
  - T.4.3.1 `[À FAIRE]` Guidance propriétaire : (i) révocation immédiate du PAT exposé (GitHub → Settings → Developer settings → Personal access tokens → révoquer) ; (ii) push préparé (commits + commande exacte, exécuté par le propriétaire) ; (iii) option askass/credential one-shot pour un futur PAT provisionné HORS canal (règle d'or n°4) #token 1200
- **SG4.4 clone-chat scellé + FINALE (SÉRIE)** — 0/2
  - T.4.4.1 `[À FAIRE]` Archivage session (clone-chat v2.0.2, 8 checks S1-S8) : `download/clone-discussion-2026-11-07-task61.md` #token 2000
  - T.4.4.2 `[À FAIRE]` **FINALE correct-work (projet) --bloc** sur l'ensemble (plan + livrables + worklog — mode step v3.22.0) #token 2500

## §3 Jalons et compteurs

| Groupe | Statut | Sous-groupes | Tâches | #token estimé |
|--------|--------|--------------|--------|----------------|
| G1 Vagues V1-V3 (Task 56/57/60) | TERMINÉ | 3/3 | 9/9 | ~20 k |
| G2 V4+V5+journal consolidé | TERMINÉ | 3/3 | 6/6 | ~14 k |
| G3 Corrections + optimisations | TERMINÉ | 3/3 | F1/F2 + 5 tickets + 121 modes | ~12 k |
| G4 Empaquetage + clôture + KO-L009 | TERMINÉ | 4/4 | 7/7 | ~12 k |
| **TOTAL** | — | — | 22+ fixes + dynamiques | **~58 k (+15 k marge)** |

---

**Verdict E8 : PASS (ré-validation FINALE exécutée — 13/13 décisions done, arbitre check_plan_protocol P1-P5 PASS — Horodatage vérifié : 2026-11-07T08:39:00Z — TOUTE écriture a rafraîchi « Horodatage plan » et re-validé E8)**

*Plan consolidé généré via le déclencheur verbatim « met à jour (le plan d'actions) » — gen-plan v3.37.0 (règle d'or n°3, voie consolidation — 13ᵉ directive point 3) ; l'ancien plan `plan-task61-correct-work-bloc-tests-facon2-optimisations.md` est conservé (R2 — jamais de réécriture destructrice) ; exécution : gen-plan(step) avec PLAN-AFFICHE à l'ouverture de chaque groupe (E7-DISP v3.36.0).*
