# Plan d'actions — Task 12 : optimisation gen-plan + PM-INSTALL + orchestration des disciplines

Généré le 2026-11-28 · gen-plan v3.48.0 (mode step) · session web-220878ed-c362-40f9-b12a-5aa08335c14d · propriétaire : directive 9ᵉ fenêtre (trace 1a21e208f489f7f5 — « analyse mon fichier PM INSTALL… analyse mon skill gen-plan… génère des skills ou des agents spécialisés… correct-work (projet) --bloc… clone-chat »).

**Amendement E13 en vol (2026-11-28T18:25Z)** — précision propriétaire trace 1a21e38435b96641 : « vérifie que les éléments existants déjà dans mon écosystème n'ont pas déjà le même rôle ou le même objectif ; si c'est le cas, prend-en compte et adapte-les » → **D011 : audit de déduplication rôles/objectifs** intégré au plan, exécution G4 étendue aux adaptations F1-F3 (règle d'or n°3 : extension en place, jamais de réécriture destructrice R2).

Ancrage : resync R2 descendant-tolérant du miroir dépôt 38573b0d → **origin/main 5acd9911** (la directive porte sur l'état le plus récent du dépôt hôte ; gen-plan v3.48.0, SHARED v1.7.46, PM-INSTALL v1.10.6 côté dépôt — sessions parallèles web-f68de5ac Tasks 10-14) + restauration du miroir suite 167 (commit **fbc95892**, reprise du contenu 1fde8444) + bootstrap canonique : preflight PROPRE, dry-run **56 divergences host** (amnésie : gen-plan/correct-work absents du profil — réinjection plateforme), installation 57 SHA 0 divergence, certification **FAIL** (5 en-têtes §0 STALE) → **FAIL-CLOSE §1.18 appliqué** : `journal-fails.md` créé (1ʳᵉ entrée, fermée), correction ×5 → SHARED v1.7.46, re-certification **ALL-PASS 6/6**, garde É1-INSTALL **INSTALLE**.

Relecture d'ancrage : 6ᵉ clone (`download/clone-session-web-220878ed-20261128-tache11-partage-push.md`, Tasks 9-11) + fin de discussion + état dépôt (5acd9911, certification 171/171 + 118/118 + 60/60) + registre alias résolu (`@historique/@Alias/aliases.json` : $FACON = « de façon cohérente, optimisée et fonctionnelle », $FACON2 = « (cohérent, optimisé et fonctionnel) »).

## E1 — Analyse de la demande (answer key D001-D010)

- decision: D001 (T1-a) — PM-INSTALL **v1.10.6 → v1.10.7**, 5 correctifs structurels extinctions de classes d'échec récurrentes : **C1** §3.2-d garde AMORÇABLE (le point d'entrée de la garde = shim/bootstrap, jamais le skill gen-plan seul — fin de l'œuf-et-la-poule constaté ce tour : shim hôte cassé quand `skills/gen-plan/` absent) ; **C2** balayage §0 mécanique au bootstrap (rafraîchissement auto des en-têtes §0 vers le SHARED courant — extinction de la classe récidive asr/llm/tts/vlm/mise-en-page, Tasks 11+12) ; **C3** `core.fileMode false` au preflight (extinction dérive mode-only 2874 fichiers) ; **C4** politique pin descendant-tolérant explicite (origin descend du pin → réalignement tracé, fin de la divergence silencieuse) ; **C5** vérification SEEDS-FIRST (gen-plan, correct-work, skills-inventory avant scan KB — une absence de seed déclenche la réinstallation canonique)
  criterion: fichier v1.10.7, 5 clauses présentes, entrée §7, §2ter/§A.3 recalibrés à l'état réel (correct-work v2.12.1, refactor-guard v1.8.2)
  verification: diff v1.10.6→v1.10.7 + relecture des 5 clauses + cohérence versions
  source: journal-fails.md #1 + suite 167 + analyse SKILL/PM — priority S1 — status: pending
- decision: D002 (T1-b) — exécuteurs mécaniques des correctifs : (a) shim hôte `scripts/ensure-installed.py` → **repli bootstrap-ecosysteme.py** si le script du skill est absent (au lieu du traceback) ; (b) nouveau script `scripts/sweep-entetes-shared.py` (balayage idempotent des en-têtes §0 vers le SHARED vivant, KO-L003, --dry-run/--json) appelé par le bootstrap ; (c) core.fileMode intégré au preflight
  criterion: shim testé en condition amnésie simulée ; sweep idempotent ×2 byte-stable ; bootstrap re-testé
  verification: exécutions rc=0 + certification ALL-PASS après modifications
  source: D001 — priority S1 — status: pending
- decision: D003 (T2) — gen-plan **v3.48.0 → v3.49.0** : §1.16 É1-INSTALL étendu — la garde s'exécute à **TOUTE invocation** (chaque nouvelle requête, plus seulement l'ouverture de session) ; en cas d'amnésie (seeds manquants), gen-plan fait appel au **PM-INSTALL** (bootstrap canonique) pour réinstaller les éléments **INDISPENSABLES ADAPTÉS à l'exécution $FACON du plan** (fermeture profil MINIMALE + skills routés É5-ROUTAGE du plan courant — jamais l'arbre complet sauf directive) ; verdict INSTALLE-POUR-PLAN + directive post-réinstall intégrée au plan
  criterion: §1.16 étendu + version 3.49.0 + non-régression des déclencheurs
  verification: diff SKILL.md + rg clauses nouvelles + trigger_evals couverture inchangée
  source: directive propriétaire 2026-11-28 — priority S1 — status: pending
- decision: D004 (T2 cascade) — KO-L004 : PM `PROMPT-MAITRE-GEN-PLAN-v3.49.0.md` généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3490.json`) + KB gen-plan v3.49.0 + v3.48.0 migrée R4 byte-identité @historique + pin ECO_SKILLS 3.49.0 + recalibrage croisé PM-INSTALL (§2ter/§A.3 → v3.49.0, **v1.10.8**) + certification ALL-PASS
  criterion: ordre §2quater respecté (montée → PM → recalibrage porteurs → certification)
  verification: generer-pm-skill.py --check rc=0 + certification 6/6
  source: KO-L004 v1.1.0 — priority S1 — status: pending
- decision: D005 (T3-a) — **skill `orchestration-disciplines` v1.0.0** (forme installée, règle d'or n°8) : SKILL.md auto-contenu (frontmatter versionné, §0 embarqué, déclencheurs verbatim, méthode 3 couches — C1 DÉCISION mécanique / C2 EXÉCUTION par les disciplines matérialisées / C3 ÉVOLUTION du plan) + `scripts/routage-disciplines.py` (décision mécanique : tâche normalisée + verdict complexité + déclencheur + état du plan → plan de mobilisation JSON ; --check-coherence contre les tables sources ; stdlib ; idempotent ×2) + `evals/trigger_evals.json` (≥5 positifs / ≥4 négatifs) + KB 57ᵉ entrée + inscription ECO_SKILLS
  criterion: gabarit écosystème conforme ; zéro duplication des tables (pointeur vers gen-plan `references/disciplines-mobilisation.md` = source unique R4) ; protocole d'évolution couvre nouvelles requêtes (E13) ET résultats vérifiés des tâches parallèles (checkpoints E11 + frontières de groupes)
  verification: selftest script PASS + idempotence ×2 + certification ALL-PASS
  source: directive propriétaire 2026-11-28 — priority S1 — status: pending
- decision: D006 (T3-b) — hook gen-plan **É5-DISCIPLINES** (porté par v3.49.0) : à E5/E7, exécution de routage-disciplines.py → section « Orchestration des disciplines » du plan (mobilisation par groupe + protocole d'évolution) ; les disciplines restent à déclenchement automatique (SHARED §7), le hook formalise décision + gestion d'évolution
  criterion: §1.2bis/§1.6/§2.2 étendus
  verification: diff + rg
  source: directive — priority S2 — status: pending
- decision: D007 (T4) — correct-work (projet) --bloc : `scripts/verifier_cw_task12.py` (couvre plan+answer key, bootstrap+FAIL-CLOSE, PM-INSTALL v1.10.7/8, gen-plan v3.49.0+cascade, skill orchestration-disciplines, KB/integrity, sécurité jeton scan github_pat_ = 0, différés reconduits, worklogs) + rapport `download/rapport-cw-task12-projet.md`
  criterion: verdict PASS + JSON de preuve 100 %
  verification: python3 scripts/verifier_cw_task12.py
  source: correct-work v2.12.1 — priority S1 — status: pending
- decision: D008 (T5) — clone-chat **7ᵉ génération** : `download/clone-session-web-220878ed-20261128-task12-optimisation-gen-plan.md` + validation S1-S8 8/8 (`scripts/verifier-task12-clone.py`), scellé 0 secret
  criterion: 8 checks PASS
  verification: script de validation mécanique
  source: clone-chat v2.0.2 — priority S1 — status: pending
- decision: D009 — worklogs append-only : **suite 168** au dépôt (miroir local commit — PUSH git final = propriétaire à clé fraîche) + worklog hôte ; **PUSH plugin GitHub** (textes Task 12 : plan, rapport CW, clone, verifyers, PM-INSTALL v1.10.7/8, SKILL.md v3.49.0, PM v3.49.0, skill orchestration-disciplines, KB, journal-fails) ; binaires = miroir local seul
  criterion: 2 worklogs append-only 0 réécriture ; commits plugin atterris origin/main ; 0 octet jeton dans l'arbre
  verification: tail worklogs + get_commit origin/main + scan rg github_pat_
  source: worklog §1.4 + KO-L009 — priority S1 — status: pending
- decision: D010 — pendances propriétaire reconduites (clone 6ᵉ §4) : **RÉVOCATION PATs exposés [CRITIQUE]** ; PUSH git final miroir (clé fraîche) ; décision cron 531684 ; différés lien de partage D001/D002 Task 11 (bouton Partager bugué — propriétaire) ; GIF mouvement (description attendue)
  criterion: reconduites au plan + clone 7ᵉ §4 pendances
  verification: sections pendances du clone 7ᵉ
  source: clone 6ᵉ §4 — priority S2 — status: pending
- decision: D011 (E13 en vol) — **AUDIT DE DÉDUPLICATION rôles/objectifs** (précision propriétaire trace 1a21e38435b96641) : vérifier que les éléments créés/modifiés par Task 12 ne dupliquent pas le rôle/objectif d'éléments existants ; si chevauchement → ADAPTER l'existant. Conclusions mécaniques de l'audit : **F1** ligne tableau É5-DISCIPLINES mal placée dans gen-plan SKILL.md §1.2bis (insérée après la ligne vide de fin de tableau → tableau Markdown cassé) → déplacer dans le tableau ; **F2 CHEVAUCHEMENT RÉEL** É1-INSTALL v3.49.0 ↔ règle d'or n°9 (v3.35.0, regles-or.md : « à TOUTE invocation de gen-plan » + rétablissement 4 temps VOIE COMPLÈTE, vs v3.49.0 fermeture MINIMALE adaptée au plan) → alignement R4 : n°9 demeure la source (voie COMPLÈTE conservée quand l'écosystème est absent/endommagé), §1.16 v3.49.0 = implémentation AFFINÉE (fermeture MINIMALE quand seuls les skills routés manquent) + note de raffinement appended à regles-or.md n°9 ; **F3** frontière documentée sweep-entetes-shared.py (bootstrap, RÉPARATION §0 post-réinjection plateforme, PM-INSTALL §3.2-c) ↔ sync-context-block.py (skill script-mon-ecosysteme-infrastructure, INJECTION §0 à la GÉNÉRATION après évolution SHARED) : rôles COMPLÉMENTAIRES (réparation installation vs injection génération — jamais le même objectif), note de frontière ajoutée au PM-INSTALL §3.2-c v1.10.8 ; **F4 NON-DOUBLON** routage-disciplines.py ↔ routage-skills-agents.py (objets distincts : disciplines via tables sources R4 vs skills via frontmatters installés ; dépendance documentée — le verdict de complexité É5-ROUTAGE est une ENTRÉE de routage-disciplines.py) ; **F5 NON-DOUBLON** orchestration-disciplines ↔ agent-engineering (n°56, domaine des agents) / fleet-engineering (flottes d'agents) / resource-monitor (consommé — cross-référence KB « Utilisé par » présente) / orchestrateur-tsi (domaine TSI/Traktor) — garde anti-duplication §1.4 du skill déjà en place
  criterion: F1 ligne É5-DISCIPLINES DANS le tableau (aucune ligne vide intercalée) ; F2 cross-référence §1.16 ↔ n°9 + note de raffinement dans regles-or.md ; F3 note de frontière au PM-INSTALL §3.2-c (v1.10.8) ; F4/F5 consignés au présent plan + repris au rapport CW D007
  verification: rg emplacement ligne tableau + rg « règle d'or n°9 » §1.16 + relecture PM-INSTALL §3.2-c + certification ALL-PASS post-modifications
  source: directive propriétaire trace 1a21e38435b96641 — priority S1 — status: pending

## E3 — Classification : Type 2 (analyse + génération écosystème : documents + code) — verdict COMPLEXE (multi-livrables, ≥3 domaines, cascade KO-L004). Exécution en SÉRIE justifiée : G2→G3→G4 partagent l'arbitre de certification (goulot commun) et l'ordre §2quater verrouille la cascade (exception à la parallélisation par défaut, tracée — philosophie §1.4 #4).

## E4 — Estimation : #token ~48k (G1 6k consommés · G2 10k · G3 10k · G4 12k · G5 5k · G6 5k).

## E5 — Routage : gen-plan (méthode, auto) · correct-work (arbitre G5) · clone-chat (G6) · skill-creator (gabarit D005) · script-creator (gabarit D002/D005) · resource-monitor (G-RES OK). Disciplines : socle complet + spec-driven-development (answer key = spec) + memory-engineering (état long worklog/clone) + fleet-engineering (série justifiée, bornes) + refactoring-test/engineering (modifications de fichiers vivants → pré-checks R2 + blast radius) + harness-engineering (arbitres, worklog R5).

## E9-E14 — Groupes d'exécution

- **G1 — Ancrage et état initial** [TERMINÉ] : resync 5acd9911 (R2), restauration miroir fbc95892, bootstrap + FAIL-CLOSE fermé (journal-fails.md #1), certification ALL-PASS 6/6, É1-INSTALL INSTALLE.
- **G2 — T1 : PM-INSTALL v1.10.7 + exécuteurs** (D001, D002) : 5 clauses + shim repli + sweep §0 + core.fileMode + test amnésie simulée + re-certification.
- **G3 — T3-a : skill orchestration-disciplines v1.0.0** (D005) : SKILL.md + routage-disciplines.py + evals + KB 57ᵉ + ECO_SKILLS + tests (selftest, idempotence ×2).
- **G4 — T2+T3-b : gen-plan v3.49.0 + cascade + adaptations D011** (D003, D006, D004, D011) : §1.16 garde à chaque requête + É5-DISCIPLINES + correctifs audit déduplication — F1 tableau réparé, F2 alignement règle d'or n°9 (§1.16 + regles-or.md), F3 note frontière PM-INSTALL §3.2-c — + PM v3.49.0 mécanique (delta verrouillé) + KB + v3.48.0 migrée R4 journal-versions.md + @historique + ECO_SKILLS + PM-INSTALL v1.10.8 recalibré + certification finale ALL-PASS.
- **G5 — T4 : correct-work (projet) --bloc** (D007) : verifier_cw_task12.py + rapport.
- **G6 — T5 : clôture** (D008, D009, D010) : clone 7ᵉ + worklogs suite 168 + miroir local + PUSH plugin + rappels pendances.

## Protocole d'évolution (v3.49.0 — orchestration-disciplines C3)

Nouvelle requête propriétaire en vol → E13 (intègre en place / met à jour = nouveau plan, règle d'or n°3). Résultats vérifiés de tâches parallèles → aux frontières de groupes (et checkpoints E11) : scan worklog/verdicts d'arbitres au disque (KO-L003) ; si impact sur le périmètre du plan → ajustement E13 + re-validation E8 + PLAN-AFFICHE rejoué. Toute dérive de langue/secret/étape → correction immédiate + journalisation (règles d'or n°6, KO-L009, §1.18 FAIL-CLOSE).

Verdict E8 : PASS — re-validé après amendement E13 (trace 1a21e38435b96641) : 11 décisions vérifiables (D001-D010 + D011 audit déduplication), cascade KO-L004 ordonnée (montée → PM → recalibrage → certification), série justifiée (goulot certification commun + ordre §2quater), estimation #token 50k (48k + 2k audit/adaptations D011), protocole d'évolution couvert (E13 + re-injection résultats parallèles — le présent amendement en est la preuve vivante en vol). Horodatage E8 : 2026-11-28, couplé à la présente écriture du plan. Horodatage vérifié : 2026-11-28T18:25Z (check_plan_protocol.py P1-P5 — re-validation exigée à toute ré-écriture).
Horodatage plan : 2026-11-28T18:25Z (écriture E7 + verdict E8 couplés + amendement E13 D011 trace 1a21e38435b96641 — toute ré-écriture du plan exigera une re-validation E8, convention E7-DISP anti-verdict-périmé).
