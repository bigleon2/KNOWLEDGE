# Plan Task 105 — Tests d'efficacité du système d'installation (3 axes) → stratégie d'optimisation → correct-work --bloc

> gen-plan mode **step** (v3.43.0 — enchaînement autonome des groupes séquentiels, correct-work(groupe) après chaque groupe, max 2 rounds de correction, correct-work(projet) en fin de chaîne) · Directive propriétaire trace `1a1efb513dfbc805` : ① installer l'écosystème personnel sur le profil local via le fichier PM-INSTALL (URL `aa3b99d` — identification de procédure ; exécution par dérivation dynamique KO-L003 sur le corpus vivant v1.9.16, garde R2 — précédents Task 1/102/103) ; ② lorsque l'installation sera terminée, prendre en compte le skill gen-plan fraîchement installé pour générer le plan d'actions des étapes suivantes : item A « génère $FACON et fais des tests $FACON2 sur le système d'installation de mon écosystème dans l'objectif d'optimiser son efficacité, trouve $FACON la meilleure stratégie pour faire cela » ; item B « correct-work ». Alias résolus (registre @Alias) : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) ».

## G0 — Installation (EXÉCUTÉE EN AMONT, ce tour)

- Préflight (récidive recyclage sandbox, 4ᵉ consécutive — pattern Task 102/103) : dérive 2741 fichiers (2681 mode-bits 0 octet + 42 binaires byte-identiques + **18 JPG à contenu altéré** — même dossier design que Task 103) + origin/main local stale (`aa855a2f`, HEAD `24441ed2` = pendance PUSH Task 104) → réparés `git reset --hard` LOCAL + `git fetch` ANONYME (0 exposition) → 0 porcelain.
- Pipeline canonique `scripts/eco_install_pipeline.py` : dry-run d'abord (RC mesuré sans pipe — leçon F2 Task 103) : fail-fast F3 attendu **55 divergences hôte** (gen-plan/correct-work absents — arbre hôte restauré ancien) → installation réelle **rc=0** : pin `a14f750` descendant-tolérant · garde R2 « 0 rétrogradation » · archive v2.3 rescellée **15/15** · manifeste **114/114 PASS** · post-install **55/55 SHA 0 divergence** (0,24 s) · certification-complete **ALL PASS 6/6** (verify-cross 165/165 ×2 · vcw 16/16 · integrity 114/114 · interactions 55/55 STRICT · tool-routing 5/5 — 0,71 s) · É1-INSTALL INSTALLE (gen-plan v3.43.0 · correct-work v2.11.0 · clone-chat v2.0.2 · version-management v1.3.0 · refactor-guard v1.8.1 · alias-eco v1.3.0 — SHA identiques hôte↔dépôt, 72 skills hôte).

## Contexte E2 (mesures réelles de session — règle d'or n°5)

- **Cible** : le « système d'installation » = PM-INSTALL v1.9.16 + exécutants canoniques (`eco_install_pipeline.py` · `task-f5-seal-archive-v23.py` · `check-ecosysteme-integrity.py` · `certification-complete.py` · `ensure-installed.py` É1-INSTALL · `auto-install-ecosysteme.py` D727) **+ le flux de bout en bout par session** (préflight git → dry-run → install → certification → É1-INSTALL).
- **État de l'art interne** : Task 70 (étude faisabilité, 2026-11-07) — pipeline 0,14 s, garde 0,04 s, **goulot réel = budget #token (contexte LLM), PAS l'entré-sortie** ; réécritures OOP intégrale et noyau compilé unique NON RECOMMANDÉES (mesures §3/§5 : zip 10× plus lent en lecture, 5,7× en installation) · Task 76 (tests C1/C2 + failles F1-F5 corrigées : contrat CLI, --dry-run, pin, scelleur v2.3 branché Task 100) · Task 95 (conventions mesure : baseline médiane ×3, tolérances) · le coût bootstrap de G0 CE TOUR = **6 tours agent** (état · préflight · dry-run · install · certification · É1) — donnée réelle de dérive, le cas sain est mesuré par le harnais.
- **Hypothèses à éprouver** : H1 le coût machine demeure négligeable malgré seal v2.3 + manifeste 2bis (aggravation à quantifier vs 0,14 s Task 70) ; H2 le levier d'efficacité réel est le **nombre de tours agent** du bootstrap (6 → 1 sans perte de garantie) ; H3 l'optimisation ne doit AUCUNEMENT casser les garanties (idempotence, 0 mutation dry-run, R2, arbitres).

## Groupes (mode step — exécution séquentielle autonome, CW(groupe) après chacun)

- **G1 (outillage — ~3500 #token)** Harnais + protocole : `scripts/task105-campagne-efficacite.py` (stdlib, self-test, **stratégie de test en 3 axes** — la réponse à « trouve la meilleure stratégie » : Axe A efficacité machine · Axe B efficacité du flux de bout en bout (le goulot réel, 3 voies d'entrée mesurées apples-to-apples) · Axe C garanties non négociables ; orchestration R4 des arbitres existants — zéro duplication de logique de verdict, AUCUNE écriture corrective) + `download/protocole-tests-efficacite-task105.json`. CW(groupe) : py_compile + selftest + protocole vérifiés.
- **G2 (campagne — ~3500 #token)** Exécution des 3 axes : **A** micro-durées médiane ×3 par composant (7 composants, perf_counter, comparaison baseline Task 70) → `download/rapport-efficacite-task105-machine.json` ; **B** 3 voies d'entrée — V1 manuelle canonique (6 tours, séquence G0 rejouée sur état sain) · V2 auto-install D727 (1 commande, couverture partielle : sans préflight git ni certification) · V3 **prototype consolidé** (1 commande : préflight git → dry-run → install → certification → É1 → verdict consolidé JSON) → `download/rapport-efficacite-task105-flux.json` + `download/rapport-efficacite-task105-bootstrap-consolide.json` ; **C** garanties : idempotence ×2 (verdicts normalisés byte-identiques) · dry-run 0 mutation (preuve mtime/SHA) · garde R2 · arbitres post-campagne ALL PASS → `download/rapport-efficacite-task105-garanties.json` + synthèse JSON `download/rapport-efficacite-task105-synthese.json`. CW(groupe) : answer key D002-D005 re-jouée.
- **G3 (stratégie — ~2500 #token)** Rapport final `download/rapport-tests-efficacite-task105.md` : verdicts par axe (chiffres des JSON) + **stratégie d'optimisation hiérarchisée S1-S4** fondée sur les mesures (H1/H2/H3 tranchées, gains attendus chiffrés en tours agent et octets de sortie, coûts, ce qu'il ne faut PAS faire — Task 70 réitéré) + feuille de route d'application (GO propriétaire requis pour toute montée canonique — R2/zéro-régression). CW(groupe) : D006 vérifié.
- **G4 (correct-work — ~2500 #token)** correct-work (projet) **--bloc** (item B de la directive + fin de chaîne mode step) : 4 blocs (B1 préflight+installation G0 · B2 harnais+campagne G1-G2 · B3 stratégie G3 · B4 clôture G5) × Étapes 2-5 → rapport `download/rapport-cw-task105-bloc.md` (agrégation = pire bloc ; answer key D001-D009 re-jouée).
- **G5 (clôture — ~2500 #token)** worklog suite 151 (hôte↔dépôt parité md5, marqueur PLAN-AFFICHE) + arbitres pré-commit (verify-correct-work 16/16 · certification-complete ALL PASS 6/6 · triggers-replay 0 dérive · doublons 0) + miroirs download/ hôte→dépôt (plan + protocole + 5 rapports JSON + rapport MD + rapport CW) + E8 final (answer-key-checker 16/16 ×2 byte-identiques · check_plan_protocol P1-P5) + COMMIT LOCAL SANS PUSH « Task 105 CLOSE » (0 PAT fourni — 0 exposition, E15 inchangé 31, **pendance PUSH 2 commits** consignée — leçon Task 98/101 : push immédiat dès PAT frais).

## Answer key (schéma E1 — arbitre answer-key-checker, vérifications Python N3 re-jouables)

- D001 :
    criterion: "Harnais de campagne $FACON2 généré et auto-vérifié : scripts/task105-campagne-efficacite.py (stdlib, selftest embarqué, modes --protocole/--axe/--bootstrap-consolide/--synthese, orchestration R4 des arbitres existants, aucune écriture corrective) + protocole download/protocole-tests-efficacite-task105.json (3 axes, critères de verdict, tolérances)"
    verification: "python3 -m py_compile scripts/task105-campagne-efficacite.py && python3 scripts/task105-campagne-efficacite.py --selftest && python3 scripts/task105-campagne-efficacite.py --protocole && python3 -c \"import json; d=json.load(open('download/protocole-tests-efficacite-task105.json')); assert len(d['axes'])==3 and d['cible']\""
    source: "directive trace 1a1efb513dfbc805 item A (génère $FACON... fais des tests $FACON2) ; précédents harnais Task 73/76 ; conventions mesure Task 95"
    priority: "S1"
    status: "verified"
- D002 :
    criterion: "Axe A — efficacité machine mesurée : 7 composants du système d'installation chronométrés médiane ×3 (perf_counter), comparés à la baseline Task 70 (pipeline 0,14 s / 53 entrées), verdict tracé dans download/rapport-efficacite-task105-machine.json"
    verification: "python3 scripts/task105-campagne-efficacite.py --axe machine && python3 -c \"import json; d=json.load(open('download/rapport-efficacite-task105-machine.json')); assert len(d['composants'])>=7 and all(c.get('mediane_ms') is not None for c in d['composants']) and d['verdict']\""
    source: "directive item A (optimiser son efficacité) ; étude Task 70 §3 (baseline) ; hypothèse H1"
    priority: "S2"
    status: "verified"
- D003 :
    criterion: "Axe B — efficacité du flux mesurée : 3 voies d'entrée du bootstrap comparées apples-to-apples (V1 manuelle canonique 6 tours · V2 auto-install D727 · V3 prototype consolidé 1 commande) sur métriques commandes/tours, durée, octets de sortie, verdict consolidé, garanties couvertes → download/rapport-efficacite-task105-flux.json"
    verification: "python3 scripts/task105-campagne-efficacite.py --axe flux && python3 -c \"import json; d=json.load(open('download/rapport-efficacite-task105-flux.json')); assert len(d['voies'])==3 and all('tours' in v and 'octets_sortie' in v for v in d['voies'])\""
    source: "directive item A ; étude Task 70 (goulot = #token) ; auto-install D727 ; hypothèse H2"
    priority: "S2"
    status: "verified"
- D004 :
    criterion: "Prototype de voie consolidée démontré : 1 commande unique couvre préflight git + dry-run + installation + certification + É1-INSTALL et émet un verdict consolidé JSON — gain mesuré vs voie manuelle (tours et octets de sortie) consigné dans download/rapport-efficacite-task105-bootstrap-consolide.json (prototype de preuve, PAS une promotion canonique — GO propriétaire requis)"
    verification: "python3 scripts/task105-campagne-efficacite.py --bootstrap-consolide && python3 -c \"import json; d=json.load(open('download/rapport-efficacite-task105-bootstrap-consolide.json')); assert d['verdict_global'] in ('INSTALLE','INSTALLE-REPARÉ') and d['tours']==1\""
    source: "directive item A (trouve la meilleure stratégie) ; pattern D727 auto-install ; R2 (aucune composante existante modifiée)"
    priority: "S2"
    status: "verified"
- D005 :
    criterion: "Axe C — garanties non négociables vérifiées : idempotence ×2 du prototype (verdicts normalisés byte-identiques) · dry-run 0 mutation prouvée (aucun fichier des zones cibles modifié) · garde R2 0 rétrogradation · arbitres post-campagne ALL PASS → download/rapport-efficacite-task105-garanties.json (agrégation pire-des-verdicts)"
    verification: "python3 scripts/task105-campagne-efficacite.py --axe garanties && python3 -c \"import json; d=json.load(open('download/rapport-efficacite-task105-garanties.json')); assert all(t['verdict']=='PASS' for t in d['tests']), [t['id'] for t in d['tests'] if t['verdict']!='PASS']\""
    source: "directive item A ; refactor-guard zéro-régression ; hypothèse H3 ; idempotence R6"
    priority: "S1"
    status: "verified"
- D006 :
    criterion: "Stratégie d'optimisation hiérarchisée livrée : download/rapport-tests-efficacite-task105.md — verdicts des 3 axes avec chiffres des rapports JSON + hiérarchie S1-S4 (gains attendus, coûts, conditions GO) + contre-recommandations (Task 70 : ni OOP intégrale ni noyau compilé) + feuille de route"
    verification: "python3 -c \"c=open('download/rapport-tests-efficacite-task105.md',encoding='utf-8').read(); assert all(m in c for m in ('Axe A','Axe B','Axe C','S1','feuille de route')) and len(c)>3000\""
    source: "directive item A (trouve la meilleure stratégie pour faire cela) — livrable central"
    priority: "S1"
    status: "verified"
- D007 :
    criterion: "Rapport correct-work (projet) --bloc livré (item B + fin de chaîne mode step) : 4 blocs B1-B4 × Étapes 2-5, verdict agrégé PASS 4/4, answer key D001-D009 vérifiée"
    verification: "python3 -c \"c=open('download/rapport-cw-task105-bloc.md',encoding='utf-8').read(); assert all(f'B{i}' in c for i in range(1,5)) and 'PASS 4/4' in c and 'D009' in c\""
    source: "directive trace 1a1efb513dfbc805 item B (correct-work) ; PM-INSTALL étape 9(b) — mode PROJET --bloc (pattern Task 102/103)"
    priority: "S2"
    status: "verified"
- D008 :
    criterion: "Clôture vérifiée : worklog suite 151 en parité byte hôte↔dépôt + arbitres pré-commit ALL PASS + commit local « Task 105 CLOSE » (exactement 2 commits en avance sur origin/main, aucun push — 0 PAT fourni, E15 inchangé 31)"
    verification: "python3 -c \"import hashlib; a=hashlib.md5(open('worklog.md','rb').read()).hexdigest(); b=hashlib.md5(open('KNOWLEDGE-repo/worklog.md','rb').read()).hexdigest(); assert a==b\" && python3 scripts/certification-complete.py && python3 -c \"import subprocess; r=subprocess.run(['git','-C','KNOWLEDGE-repo','rev-list','--count','origin/main..HEAD'],capture_output=True,text=True); assert int(r.stdout.strip())==2, r.stdout\""
    source: "SHARED §1.4 journalisation ; KO-L009 ; leçon Task 98/101 (pendance PUSH consignée, push immédiat dès PAT frais)"
    priority: "S2"
    status: "verified"
- D009 :
    criterion: "Chaîne E7-DISP complète : plan écrit + answer key + verdict E8 consigné aux horodatages couplés + worklog R5 PLAN-AFFICHE + bloc récapitulatif au chat + fenêtre native TodoWrite (check_plan_protocol P1-P5 PASS)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task105-tests-efficacite-installation-cw-bloc.md --worklog worklog.md"
    source: "gen-plan §1.2bis E7-DISP (v3.36.0/v3.39.0) — garde bloquante"
    priority: "S2"
    status: "verified"

## Estimation #token (E4) et routage (E5)

- Total estimé : ~14 500 #token (G1 3500 · G2 3500 · G3 2500 · G4 2500 · G5 2500) ; G0 déjà consommé (~6000, donnée réelle axe B cas dérive). Profil NORMAL (G-RES OK — disque > 7 Go libres, 0 signal pression).
- Routage : [gen-plan · correct-work · script-creator · correct-py · resource-monitor] · couches : scripts/ + download/ + worklog (0 skill KB / agent / registre KB modifié — le harnais est un artefact de test, les composants d'installation ne sont PAS modifiés) · règle d'or n°6 (français exclusif) · règle d'or n°5 (état vérifiable, KO-L003) · KO-L009 (0 jeton manipulé ce tour) · idempotence ×2 exigée du harnais (R6).

Horodatage plan : 2026-11-18T18:07:47Z (final — 9/9 décisions verified)

Verdict E8 : PASS (answer-key-checker 16/16 ALL PASS ×2 — idempotence, sorties byte-identiques ; check_plan_protocol P1-P5 PASS — Horodatage vérifié : 2026-11-18T18:07:47Z)
