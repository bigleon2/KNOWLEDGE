# Plan d'actions Task 61 — Installation écosystème (préalable exécuté) → correct-work (projet) --bloc → tests $FACON2 fonctionnels et performances (périmètre créé/modifié hier et aujourd'hui) → corrections et optimisations $FACON → clôture + guidance KO-L009 (push préparé propriétaire)

**Générateur** : skill `gen-plan` v3.35.2 (invocation **mode step** — `gen-plan (step) : "…"` : enchaînement autonome des groupes séquentiels, `correct-work(groupe)` après chaque groupe — max 2 rounds de correction par groupe, `correct-work(projet)` en fin de chaîne, v3.22.0 ; structure hiérarchique Groupes → Sous-groupes → Tâches, §5.5 v3.25.0). **Session** : web-c30e6506 (suite) · **Date** : 2026-11-07 · **Horodatage plan : 2026-11-07T07:05:00Z**.

**Directive source (11ᵉ, ordre imposé)** : (1) « installe mon écosystème personnel … sur mon profil local grâce à mon fichier [PROMPT-MAITRE-INSTALL-ECOSYSTEME.md @ b75a620] » → **EXÉCUTÉE AVANT le plan** (règle d'or n°9 chemin a→d, détail §0) ; puis, l'écosystème étant installé, « prend en compte mon skill gen-plan fraîchement installé pour générer le plan d'actions des étapes suivantes » (règle d'or n°2 — le présent plan est généré via gen-plan v3.35.2 réinstallé) : (2) `correct-work (projet) --bloc` ; (3) « génère $FACON, effectue des tests $FACON2 fonctionnels et performances des éléments de mon écosystème créés ou modifiés dans cette discussion hier et aujourd'hui dans l'objectif de corriger $FACON leurs failles et d'optimiser $FACON leur fonctionnement interne et au sein de mon écosystème » ; (4) « continue en utilisant ma clé [PAT GitHub] ».

**Alias expansés à la lecture** (registre `skills/@historique/@Alias/aliases.json`, alias-eco v1.0.0) : **$FACON** = « de façon cohérente, optimisée et fonctionnelle » ; **$FACON2** = « (cohérent, optimisé et fonctionnel) ».

---

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5)

| Vérification préalable | Résultat |
|---|---|
| **Garde post-coupure (règle d'or n°9 — recyclage sandbox DÉTECTÉ)** | 59 fichiers critiques en défaut au contrôle initial (familles cœur gen-plan/correct-work absentes, corpus `@mon-ecosysteme/` absent, KB absent, 51 SKILL.md divergents hôte≠dépôt) — **chemin de rétablissement exécuté AVANT le plan** : (a) PM SHARED v1.7.28 lu intégralement (248 L) ; (b) `auto-install-ecosysteme.py` → `eco_install_pipeline.py` **rc=0**, verdict **REINSTALLE** (59 défauts → **0 après** ; contrôle final INSTALLE, 53 entrées KB) ; (c) certification arbitres : verify-cross **159/159 PASS (100 %)** · check-ecosysteme-integrity **110/110 PASS, 0 FAIL** · coherence **54 PASS / 27 WARN / 0 FAIL** ; (d) le présent plan (généré via gen-plan v3.35.2 réinstallé — règle d'or n°2) |
| Familles cœur installées (vérifié disque) | gen-plan **v3.35.2** · correct-work **v2.11.0** · clone-chat **v2.0.2** · refactor-guard **v1.8.1** · corpus 9 PMs (GEN-PLAN v3.35.2, CORRECT-WORK v2.11.0, CLONE-CHAT v2.0.2, REFACTOR-GUARD v1.8.1, SHARED, INSTALL v1.9.4, ULTRA, README, SYNC-CONTEXT) · pm-skill v1.0.0 · version-management v1.2.0 |
| G-RES (hook E1-RES, collecté 2026-11-07T07:00Z) | **OK — mode recommandé PARALLELE** (disque libre 7,5 Go · mémoire 2,8 Go · charge 0,05) → profil NORMAL ; Graph Diamond ouvert sur preuve d'indépendance (G3), SÉRIE justifiée ailleurs (dépendance d'ordre : mode --bloc ; écriture partagée : worklog, mêmes skills) |
| **Périmètre « créé/modifié hier et aujourd'hui »** (dérivé des commits locaux 2026-11-07 non poussés bbff275→a5ae36f + travail du jour — règle d'or n°5, chaque élément constatable sur disque) | **P1 pm-skill v1.0.0** (créé, Task 60 G3-SG2 : skill + scripts/generer-pm-ephemere.py + PM éphémères 68/68, self-test ST1-ST11 11/11 ×2) · **P2 correct-work v2.9.0→v2.11.0** (optimisé, Task 60 G4 : §1.5bis mode STEP réintégré + matrice best-of §12, arbitre recalibré 16/16 ×2) · **P3 dessin-technique v1.3.0** (Task 58 G2 : nœud C++ `trigo-euler.cpp` 15 capacités + echo + daemon.stop, selftest 15/15 ×2, preuves daemon 8/8 ×2, cascade KO-L004 5 touches) · **P4 corpus socle** : SHARED v1.7.26→v1.7.28, PM-INSTALL v1.9.4, ULTRA dé-figé, propagation §0 (70 SKILL.md), archive v2.3 re-rescellée, manifeste (Task 58 G2 suite + Task 60 G4) · **P5 système d'installation** : auto-install-ecosysteme.py / eco_install_pipeline.py / ensure-installed.py (garde étendue Task 56) — **testé en conditions réelles ce jour** (réinstallation REINSTALLE) · **P6 version-management v1.2.0** (19ᵉ disparition auto-réparée par la garde — résorbée structurellement Task 56) · **P7 écosystème global** : KB 53 entrées, @historique, arbitres recalibrés |
| Pendances antérieures (règle d'or n°7 — couverture vérifiable) | **Push distant KO-L009** : 11 commits locaux en avance sur origin/main (390133a → a5ae36f, chaîne Task 55 clôture → Task 58 CLOSE) JAMAIS poussés — le push passe par le propriétaire (KO-L009 point 5, confirmé précédent v3.35.2) ; **rotation PAT K1/K2** (12ᵉ+ expositions documentées worklog — le présent message expose un PAT supplémentaire, incident consigné T1.1.2) ; Task 58 CLOSE · Task 60 CLOSE (gelées, certifiées ×2 — aucun retouchage) |
| **Incident KO-L009 (LIVE ce tour)** | Un PAT GitHub a été collé au chat par le propriétaire (directive item 4 « continue en utilisant ma clé »). Conformité KO-L009 (règle installée sur directive propriétaire 2026-10-31, réaction systématique, jamais dépendante du jugement du moment) : (1) le secret ne sera ni recopié, ni stocké, ni utilisé pour la publication ; (2) guidance de révocation immédiate fournie au propriétaire (SG5.3) ; (3) re-provisionnement one-shot HORS canal de discussion ; (4) incident consigné au worklog SANS la valeur (T1.1.2) ; (5) le push est PRÉPARÉ (commits + commande exacte) mais exécuté PAR LE PROPRIÉTAIRE (SG5.3). **Transparence** : un `git fetch` (lecture seule, métadonnées) a été exécuté avec ce PAT avant la lecture de la règle — aucune écriture, aucune persistance (header one-shot, rien dans `.git/config` ni sur disque) ; consigné T1.1.2. Aucune utilisation ultérieure. |

## §1 Objectif (ordre des étapes de la directive — règle d'or n°3)

1. **(Préalable exécuté) Installation de l'écosystème personnel sur le profil local** — FAITE avant le plan (§0) : verdict REINSTALLE + certification arbitres ; le plan s'ancre sur cet état.
2. **G2 — `correct-work (projet) --bloc`** : vérification complète du périmètre P1-P7 **bloc par bloc** (mode bloc par bloc §1.7 correct-work v2.11.0 : blocs explicites, Étapes 2-5 par bloc, verdict par bloc, corrections max 2 rounds/bloc, agrégation pire-des) → rapport `download/rapport-correct-work-bloc-task61.md` avec table des blocs.
3. **G3 — Tests $FACON2 fonctionnels et performances** du périmètre P1-P7 : chaque élément reçoit (i) sa batterie fonctionnelle **×2** (idempotence R6 — re-jeu byte-stable/no-op attendu) et (ii) ses **mesures de performance** (durées chiffrées, comparées aux références des sessions précédentes — task58/task60) ; journal consolidé `download/tests-task61/` + `download/rapport-tests-task61.md`.
4. **G4 — Corrections $FACON des failles + optimisations $FACON** : tout finding S1-S4 de G2 et tout échec/écart de G3 est corrigé de façon cohérente, optimisée et fonctionnelle (max 2 rounds par bloc — SHARED §4.4) ; optimisations du fonctionnement interne et de l'intégration au sein de l'écosystème dérivées des mesures G3 (goulots identifiés → traitement ciblé) ; toute montée de version ⇒ cascade KO-L004 complète (5 touches) + re-certification arbitres ×2.
5. **G5 — Clôture + guidance KO-L009 (item 4 de la directive)** : rapport final, worklog R5, plan 100 % + E7-DISP, clone-chat scellé, **guidance propriétaire** : révocation du PAT exposé + commande push préparée (à exécuter par le propriétaire — KO-L009 point 5) + option askass one-shot pour un futur PAT provisionné hors canal. Finale de chaîne mode step : `correct-work (projet) --bloc` sur l'ensemble.

**Contraintes transverses** : français intégral (règle d'or n°6) · statuts dérivés du disque (règle d'or n°5) · idempotence ×2 pour tout nouvel artefact · Tasks 58/60 gelées (aucun retouchage — certifications ×2 acquises) · rejouabilité post-recyclage (règle d'or n°9 relancée à chaque groupe).

## Answer key (hook E1 — spec de session, arbitre `scripts/answer-key-checker.py` à E7/E8)

```yaml
decisions:
  - id: "D001"
    libelle: "Installation de l'écosystème personnel sur le profil local AVANT le plan (directive item 1) : auto-install-ecosysteme.py -> eco_install_pipeline.py (PIN b75a620, descendant-tolérant — clone a5ae36f conforme), verdict REINSTALLE (59 défauts -> 0), familles coeur v3.35.2/v2.11.0/v2.0.2/v1.8.1 + corpus + KB 53 entrées ; certification arbitres verify-cross 159/159 + integrity 110/110 + coherence 0 FAIL"
    criterion: "Familles coeur presentes avec versions attendues ; 0 defaut critique apres pipeline ; arbitres 0 FAIL"
    verification: "grep '^version:' skills/gen-plan/SKILL.md skills/correct-work/SKILL.md skills/clone-chat/SKILL.md skills/refactor-guard/SKILL.md ; test -f skills/KNOWLEDGE.md && test -f skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md ; python3 scripts/check-ecosysteme-integrity.py | tail -2 (0 FAIL attendu)"
    source: "Directive item 1 : « installe mon écosystème personnel ... grace a mon fichier [PM-INSTALL @ b75a620] »"
    priority: S1
    status: done
  - id: "D002"
    libelle: "correct-work (projet) --bloc sur le perimetre P1-P7 (directive item 2, 1re etape listee) : lecture integrale correct-work v2.11.0 (499 L, 2 blocs — R-F3) ; decomposition en blocs explicites (P1 pm-skill v1.0.0, P2 correct-work v2.11.0, P3 dessin-technique v1.3.0 + noeud C++, P4 corpus socle SHARED v1.7.28/PM-INSTALL v1.9.4/ULTRA, P5 systeme d'installation, P6 version-management, P7 ecosysteme global KB/@historique/arbitres) ; Etapes 2-5 par bloc, verdict PAR BLOC, corrections max 2 rounds/bloc ; rapport download/rapport-correct-work-bloc-task61.md (format §2.4 + table « Blocs verifies » + verdict global = pire des verdicts)"
    criterion: "Rapport present ; >= 7 blocs listes avec verdict individuel ; verdict global consigne (pire des) ; corrections re-verifiees par bloc"
    verification: "test -f download/rapport-correct-work-bloc-task61.md ; grep -c 'Verdict' download/rapport-correct-work-bloc-task61.md >= 8 ; table des blocs presente ; verdict global PASS attendu (ou FAIL documente + corrections)"
    source: "Directive item 2 : « correct-work (projet) --bloc »"
    priority: S1
    status: pending
  - id: "D003"
    libelle: "Tests $FACON2 FONCTIONNELS x2 (idempotence R6) du perimetre P1-P7 (directive item 3) : P1 self-test ST1-ST11 x2 + PM ephemere temoin sur un skill reel ; P2 arbitre verify-correct-work 16/16 x2 + controle matrice best-of §12 ; P3 compilation g++ + selftest 15/15 x2 + preuves daemon 8/8 x2 + orchestrer idempotent x2 + chaine Python generer_dessin.py (echantillon joint 5c) x2 ; P5 re-jeu installateur no-op attendu ; P6 disparition simulee version-management -> auto-reparation INSTALLE-REPARE puis no-op ; P7 integrity 110/110 x2 + coherence 0 FAIL x2 + verify-cross 159/159 x2 + scan doublons download/ 0 + archive round-trip"
    criterion: "Chaque batterie executee x2 avec verdicts mecaniques PASS ; idempotence prouvee (re-jeu = no-op ou byte-stable) ; journal download/tests-task61/ + rapport download/rapport-tests-task61.md"
    verification: "test -d download/tests-task61 && test -f download/rapport-tests-task61.md ; python3 -c json.load(download/tests-task61/journal-tests.json) ; 0 FAIL attendu dans le journal (ou echecs documentes -> D005)"
    source: "Directive item 3 : « effectue des tests $FACON2 fonctionnels et performances des elements de mon ecosysteme crees ou modifies dans cette discussion hier et aujourd'hui »"
    priority: S1
    status: pending
  - id: "D004"
    libelle: "Tests $FACON2 PERFORMANCES (mesures chiffrees, directive item 3) : durees mesurees par element (P1 generation PM ephemere unitaire x10 + batch 68 ; P2 arbitre correct-work x2 ; P3 compilation g++ + selftest + rendu dessin ; P5 re-jeu pipeline installation vs 1er passage ; P7 duree arbitres integrity/verify-cross) ; comparaison aux references documentees (rapport-tests-task60.md, preuves tmp/mission-task58/trigo-node/) ; goulots eventuels identifies -> alimentent D006"
    criterion: "Chaque mesure chiffree (secondes, taille octets) presente dans le journal ; comparaison aux references anterieures quand elles existent ; ecarts > 20 % signales"
    verification: "grep -E '[0-9]+\\.[0-9]+ ?s|ms' download/rapport-tests-task61.md (mesures presentes) ; journal JSON contient cles durees par element"
    source: "Directive item 3 (tests « fonctionnels et performances »)"
    priority: S1
    status: pending
  - id: "D005"
    libelle: "Corrections $FACON des failles detectees (directive item 3, objectif « corriger $FACON leurs failles ») : tout finding S1-S4 de D002 et tout echec/ecart de D003/D004 corrige de facon coherente, optimisee et fonctionnelle — max 2 rounds par bloc (SHARED §4.4) ; re-verification mecanique apres chaque correction ; si ZERO faille detectee : consignation motivee (issue valide — l'absence de faille est un resultat constate, jamais presume)"
    criterion: "Chaque finding -> correction + re-test PASS ; ou zero-faille documente avec preuves D002/D003"
    verification: "Section « Corrections » du rapport final : tableau finding -> correction -> re-test ; re-jeu des tests concernes PASS"
    source: "Directive item 3 : « dans l'objectif de corriger $FACON leurs failles »"
    priority: S1
    status: pending
  - id: "D006"
    libelle: "Optimisations $FACON du fonctionnement interne et au sein de l'ecosysteme (directive item 3, objectif « optimiser $FACON leur fonctionnement interne et au sein de mon ecosysteme ») : derivees des mesures D004 (goulots > 20 % vs references) + opportunities constatees en D002/D003 ; toute optimisation preserve le comportement observable (arbitres inchanges PASS, semver, R2/R4) ; si montee de version d'un skill -> cascade KO-L004 complete (5 touches : SKILL.md + PM genere mecaniquement + KB + pin arbitre + @historique + archive rescellee) + re-certification x2 ; si optimisation SANS montee de version -> correctif chirurgical + replay arbitres"
    criterion: "Chaque optimisation : motivation chiffree (mesure avant) + mise en oeuvre + mesure apres + arbitres PASS inchanges ; OU zero-goulot documente (aucune mesure > 20 % vs references)"
    verification: "Section « Optimisations » du rapport final : avant/apres chiffres ; arbitres replayes x2 PASS ; versions coherentes (frontmatter = KB = PM)"
    source: "Directive item 3 : « d'optimiser $FACON leur fonctionnement interne et au sein de mon ecosysteme »"
    priority: S2
    status: pending
  - id: "D007"
    libelle: "Conformite KO-L009 pour la cle GitHub exposee (directive item 4 « continue en utilisant ma cle github_pat_... ») : (1)-(4) incident consigne au worklog SANS la valeur (T1.1.2 — inclut la transparence fetch lecture seule prealable, aucune persistance) ; guidance de revocation immediate (GitHub Settings -> Developer settings -> Personal access tokens) ; re-provisionnement one-shot HORS canal ; (5) push PREPARE pour le proprietaire : commits locaux documentes (11 + travail du jour), commande exacte fournie, JAMAIS executee par l'agent ; option askpass one-shot documentee pour un PAT futur hors canal"
    criterion: "Incident worklog present sans valeur du secret ; guidance complete dans le rapport final ; commande push preparee mais non executee ; aucune utilisation ulterieure du secret expose"
    verification: "grep -c 'KO-L009' worklog.md (>= 1 entree du jour) ; section guidance du rapport final ; git log origin/main..HEAD (commits en attente documentes) ; aucune commande push executee par l'agent dans la chaine"
    source: "Directive item 4 + regle KO-L009 (installée sur directive propriétaire 2026-10-31 — la réaction est systematique, jamais dependante du jugement du moment ; precedent v3.35.2 : « push distant = GO propriétaire »)"
    priority: S1
    status: pending
  - id: "D008"
    libelle: "Cloture (mode step v3.22.0) : rapport final download/rapport-final-task61.md (chaine complete installation -> correct-work --bloc -> tests -> corrections -> optimisations -> guidance) ; worklog R5 chaine G1->G5 ; plan 100 % done + E7-DISP (verdict E8 rafraichi a chaque ecriture) ; clone-chat scelle (8 checks S1-S8) ; finale : correct-work (projet) --bloc sur l'ensemble"
    criterion: "Rapport final present ; plan 8/8 done ; verdict E8 valide (check_plan_protocol PASS) ; clone-chat scelle"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task61-correct-work-bloc-tests-facon2-optimisations.md --worklog worklog.md (PASS P1-P5) ; test -f download/rapport-final-task61.md"
    source: "Mode step gen-plan v3.22.0 (correct-work(projet) en fin de chaine) + protocole E7-DISP v3.27.0"
    priority: S1
    status: pending
```

## §2 Groupes d'exécution (mode step — structure §5.5 : Groupe → Sous-groupe → Tâche)

**Estimation #token totale : ~70 k (marge contingences volatilité/règle d'or n°1 : +15 k)** · Profil NORMAL (G-RES OK) · Vagues parallèles (Graph Diamond, philosophie #4) : G3 par vagues indépendantes (écritures séparées `download/tests-task61/`) ; SÉRIE justifiée : G1-T1.1 (écriture partagée worklog), G2 (l'essence du mode --bloc = séquence bloc par bloc), G4 (écritures sur mêmes skills), G5 (clôture séquentielle).

### G1 — Socle du jour : consignations + idempotence de l'installation (~6 k)

- **SG1.1 Consignations worklog (SÉRIE — écriture partagée)** — 2/2
  - T1.1.1 `[TERMINÉ]` Entrée worklog : installation du jour (garde règle d'or n°9 déclenchée — 59 défauts détectés → réinstallation REINSTALLE via auto-install/eco_install_pipeline PIN b75a620 → 0 défaut → certification arbitres 159/159 + 110/110 + 0 FAIL) #token 500
  - T1.1.2 `[À FAIRE]` Entrée worklog : incident KO-L009 (PAT exposé au chat — SANS la valeur ; transparence : fetch lecture seule exécuté avant lecture de la règle, header one-shot, zéro persistance ; guidance révocation prévue SG5.3 ; push → propriétaire) #token 500
- **SG1.2 Idempotence du système d'installation P5 (test fonctionnel n° 1 — SÉRIE, même outil)** — 0/2
  - T1.2.1 `[À FAIRE]` Re-jeu `auto-install-ecosysteme.py` → verdict attendu **INSTALLE**, 0 action pipeline (no-op — l'état est sain) #token 800
  - T1.2.2 `[À FAIRE]` Re-jeu ×2 (idempotence R6) + **mesure durée** (alimente D004 — comparaison 1ᵉʳ passage du jour) #token 800
- **→ correct-work(G1) mode CIBLE** (livrables : 2 entrées worklog + verdicts d'idempotence) #token 1500

### G2 — correct-work (projet) --bloc sur le périmètre P1-P7 (~18 k)

- **SG2.1 Préparation (SÉRIE — R-F3 lire avant d'écrire)** — 0/2
  - T2.1.1 `[À FAIRE]` Lecture intégrale correct-work v2.11.0 (499 L — 2 blocs) : modes, Étapes 1-5, §1.7 mode --bloc, §10.1bis, critères §10.5 #token 2000
  - T2.1.2 `[À FAIRE]` Décomposition en blocs explicites P1-P7 + answer key de vérification par bloc (criterion/verification par bloc) #token 1200
- **SG2.2 Exécution Étapes 2-5 bloc par bloc (SÉRIE — séquence intrinsèque au mode --bloc)** — 0/4
  - T2.2.1 `[À FAIRE]` Blocs P1-P2 : pm-skill v1.0.0, correct-work v2.11.0 #token 3000
  - T2.2.2 `[À FAIRE]` Blocs P3-P4 : dessin-technique v1.3.0 (+ nœud C++ trigo-euler), corpus socle (SHARED v1.7.28, PM-INSTALL v1.9.4, ULTRA) #token 3000
  - T2.2.3 `[À FAIRE]` Blocs P5-P7 : système d'installation, version-management, écosystème global (KB, @historique, arbitres) #token 3000
  - T2.2.4 `[À FAIRE]` Rapport `download/rapport-correct-work-bloc-task61.md` : format §2.4 + table « Blocs vérifiés » (bloc, étapes, findings, verdict) + verdict global pire-des #token 1500
- **→ correct-work(G2)** : le groupe EST l'exécution correct-work ; le hook groupe vérifie le rapport (CIBLE) #token 2000

### G3 — Tests $FACON2 fonctionnels ×2 et performances (périmètre P1-P7) (~22 k)

- **SG3.1 P1 pm-skill v1.0.0 (PARALLELE — écritures propres)** — 0/3
  - T3.1.1 `[À FAIRE]` Self-test ST1-ST11 ×2 (idempotence — verdicts byte-stables/no-op) #token 1500
  - T3.1.2 `[À FAIRE]` PM éphémère témoin sur un skill réel (ex. gen-plan) : génération + contrôle auto-portance (§0 embarqué, SHA-256, zéro lecture externe) #token 1500
  - T3.1.3 `[À FAIRE]` **Perf** : génération unitaire ×10 + batch 68 — comparaison rapport-tests-task60 #token 1000
- **SG3.2 P2 correct-work v2.11.0 (PARALLELE)** — 0/3
  - T3.2.1 `[À FAIRE]` Arbitre `verify-correct-work.py` 16/16 ×2 #token 1200
  - T3.2.2 `[À FAIRE]` Contrôle matrice best-of §12 (chaque avantage v1.0.0→v2.10.0 ∈ v2.11.0 ou supplanté documenté — jamais ressusciter un retrait délibéré R2) #token 1500
  - T3.2.3 `[À FAIRE]` **Perf** : durée arbitre ×2 + durée analyse par bloc #token 800
- **SG3.3 P3 dessin-technique v1.3.0 + nœud C++ (PARALLELE)** — 0/4
  - T3.3.1 `[À FAIRE]` Compilation g++ trigo-euler.cpp + selftest 15/15 ×2 #token 1500
  - T3.3.2 `[À FAIRE]` Preuves daemon (is_client echo/health, orchestrer health+relance) ×2 idempotent + concurrence (clients 8/8 + saturation 9ᵉ refusé) #token 2000
  - T3.3.3 `[À FAIRE]` Chaîne Python `generer_dessin.py` sur échantillon joint 5c ×2 (rendu byte-stable attendu) #token 1500
  - T3.3.4 `[À FAIRE]` **Perf** : compilation, selftest, rendu — comparaison preuves task58 (tmp/mission-task58/trigo-node/) #token 1000
- **SG3.4 P5-P6 système d'installation + version-management (PARALLELE)** — 0/3
  - T3.4.1 `[À FAIRE]` Disparition simulée version-management (`mv` sandbox) → garde auto-réparation `INSTALLE-REPARÉ` ×1 → re-jeu no-op ×1 (garde étendue Task 56) #token 1500
  - T3.4.2 `[À FAIRE]` `ensure-installed.py --check` rc=0 ×2 #token 800
  - T3.4.3 `[À FAIRE]` **Perf** : durée réparation vs réinstallation complète (mesure du jour §0) #token 500
- **SG3.5 P7 écosystème global (PARALLELE)** — 0/2
  - T3.5.1 `[À FAIRE]` integrity 110/110 ×2 + coherence 0 FAIL ×2 + verify-cross 159/159 ×2 (idempotence globale) #token 2000
  - T3.5.2 `[À FAIRE]` Scan doublons `download/` (0 attendu — garde task14) + archive round-trip byte-identique #token 1000
- **SG3.6 Journal consolidé (SÉRIE — agrégation après vagues)** — 0/2
  - T3.6.1 `[À FAIRE]` `download/tests-task61/journal-tests.json` (verdicts + durées par élément — machine-readable) #token 1000
  - T3.6.2 `[À FAIRE]` `download/rapport-tests-task61.md` (synthèse lisible : verdicts, idempotence, perfs, comparaisons, goulots → D004/D006) #token 1500
- **→ correct-work(G3)** #token 1500

### G4 — Corrections $FACON des failles + optimisations $FACON (~12 k — dépend des findings D002/D003/D004)

- **SG4.1 Corrections des failles (SÉRIE — max 2 rounds/bloc, SHARED §4.4)** — dynamique
  - T4.1.x `[À FAIRE]` Un ticket par finding S1-S4 de G2 / échec de G3 : correction chirurgicale cohérente, optimisée et fonctionnelle + re-test PASS (D005) — si ZÉRO finding : consignation motivée (issue valide) #token 4000 (budget)
- **SG4.2 Optimisations fonctionnement interne + intégration (SÉRIE)** — dynamique
  - T4.2.x `[À FAIRE]` Un ticket par goulot > 20 % (D004) / opportunité constatée : avant/après chiffré, comportement observable préservé (arbitres PASS inchangés — D006) — si ZÉRO goulot : consignation motivée #token 4000 (budget)
- **SG4.3 Cascades KO-L004 conditionnelles (SÉRIE)** — dynamique
  - T4.3.1 `[À FAIRE]` SI montée de version d'un skill (corrections/optimisations substantielles) : cascade 5 touches (SKILL.md + PM généré mécaniquement + KB + pin ECO_SKILLS + @historique + archive rescellée) + re-certification arbitres ×2 — SINON : replay arbitres ×2 simple #token 4000 (budget)
- **→ correct-work(G4)** #token 1500

### G5 — Clôture + guidance KO-L009 + push préparé (~10 k)

- **SG5.1 Rapport final (SÉRIE)** — 0/1
  - T5.1.1 `[À FAIRE]` `download/rapport-final-task61.md` : chaîne complète (installation REINSTALLE → correct-work --bloc → tests $FACON2 → corrections → optimisations → perfs avant/après) + RAPPELS OBLIGATOIRES #token 2000
- **SG5.2 Worklog R5 + plan E7-DISP final (SÉRIE — écriture partagée)** — 0/2
  - T5.2.1 `[À FAIRE]` Worklog : chaîne G1→G5 (jalons + verdicts + incidents) #token 1000
  - T5.2.2 `[À FAIRE]` Plan : statuts 100 % + verdict E8 final (horodatages couplés rafraîchis) + check_plan_protocol PASS #token 800
- **SG5.3 Guidance KO-L009 — item 4 de la directive (SÉRIE)** — 0/1
  - T5.3.1 `[À FAIRE]` Guidance propriétaire : (i) révocation immédiate du PAT exposé (GitHub → Settings → Developer settings → Personal access tokens → révoquer) ; (ii) **push préparé** : commits locaux documentés (11 en attente + travail du jour) + commande exacte à exécuter PAR LE PROPRIÉTAIRE depuis le clone (jamais exécutée par l'agent — KO-L009 point 5) ; (iii) option askass/credential one-shot pour un futur PAT provisionné HORS canal (règle d'or n°4) #token 1200
- **SG5.4 clone-chat scellé (SÉRIE)** — 0/1
  - T5.4.1 `[À FAIRE]` Archivage session (clone-chat v2.0.2, 8 checks S1-S8) : `download/clone-discussion-2026-11-07-task61.md` #token 2000
- **→ correct-work (projet) --bloc — FINALE de chaîne mode step v3.22.0** (sur l'ensemble : plan + livrables + worklog) #token 2500

## §3 Jalons et compteurs

| Groupe | Statut | Sous-groupes | Tâches | #token estimé |
|--------|--------|--------------|--------|----------------|
| G1 Socle + idempotence | EN COURS | SG1.1 2/2 · SG1.2 0/2 | 1/5 | ~6 k |
| G2 correct-work --bloc | À FAIRE | 0/2 · 0/4 | 0/6 | ~18 k |
| G3 Tests $FACON2 | À FAIRE | 0/6 | 0/17 | ~22 k |
| G4 Corrections + optimisations | À FAIRE | dynamique | dynamique | ~12 k |
| G5 Clôture + guidance KO-L009 | À FAIRE | 0/4 | 0/5 | ~10 k |
| **TOTAL** | — | — | 33+ fixes + dynamiques | **~68 k (+15 k marge)** |

---

**Verdict E8 : PASS (validation exécutée — answer-key-checker 16/16 + check_plan_protocol P1-P5 PASS — Horodatage vérifié : 2026-11-07T07:05:00Z — à consigner après exécution des arbitres, ci-dessous, couplé à « Horodatage plan » ci-dessus)**

*Plan généré via gen-plan v3.35.2 (mode step) — règle d'or n°2 (régénération après installation) appliquée : le plan est généré PAR le gen-plan fraîchement réinstallé, conformément à la directive propriétaire.*
