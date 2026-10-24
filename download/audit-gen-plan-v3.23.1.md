# Audit complet de gen-plan v3.23.1 — bug « plan d'actions non affiché / protocole court-circuité »

> Task 15 (plan v2, G6) · Session web-dd290b0d · 2026-10-25 · Conformité : KO-L003 (arbitres à invariants dynamisés), KO-L004 (recalibrage croisé), R3 (traçabilité)
> Déclencheur : directive propriétaire — « vérifie s'il a bien failli à sa tâche » (bug apparu 3× depuis hier, scénario : interruption en cours de plan pour correction/clarification)

## 1. Constat de défaillance (preuves mécaniques)

| # | Fait établi | Preuve | Sévérité |
|---|-------------|--------|----------|
| 1 | Génération Task 14 jamais journalisée (R5 violée) | `grep -c "Task ID: 14" worklog.md` → **0** (dernier = Task 13) | S1 |
| 2 | E8 (validation du plan) jamais exécuté | 0 trace d'invocation `answer-key-checker`/hook correct-work sur le plan | S1 |
| 3 | Plan non affiché au chat | Témoignage propriétaire (« pas fait ou pas afficher comme d'habitude ») + aucun marqueur d'affichage conventionnalisé | S1 |
| 4 | Fichier plan écrit malgré tout | `download/plan-cahier-des-charges-v2.0.1.md` (10 282 octets, 17:34) | — |

**Verdict : gen-plan a failli à sa tâche — génération PARTIELLE.** La chaîne de finalisation E7 (écriture) → E8 (validation) → R5 (journalisation) → affichage a été **court-circuitée après l'étape d'écriture du fichier**, sans qu'aucun mécanisme ne détecte l'interruption. Le mode de défaillance se répète exactement dans le scénario signalé par le propriétaire (interruption mi-plan → message de correction → reprise sans finalisation).

## 2. Inventaire audité (16 fichiers, 1 854 lignes)

| Composant | État | Verdict |
|-----------|------|---------|
| SKILL.md v3.23.1 (381 L) | Frontmatter complet (5 dépendances, read_when), 4 modes, 15 étapes, 4 règles d'or, hooks §1.2bis (answer key E1, arbitre E7/E8, Graph Diamond, observer E15), E1-RES, É1-INSTALL, modes NULL/step/step-ok, KO-L001/L003/L004/L005/L007 | **Structurellement sain** — voir écarts §3 |
| references/ (11 fichiers) | Tous présents, bannières cohérentes avec §2.2 (11 références déclarées = 11 réelles) | OK |
| evals/trigger_evals.json | 12 cas (9+ / 3−) couvrant modes step/step-ok/step-confirm, verbatim « intègre dans le plan d'actions », contrôles négatifs | OK — **mais gap de couverture (E-5)** |
| evals/evals.json | 8 evals (id 1-8), version alignée | OK |
| scripts/ensure-installed.py (174 L) | --check/--reinstall/--preempt, idempotent, racine dérivée L008 | **Testé live : rc=0 INSTALLE** — OK |
| Entrée KB gen-plan v3.23.1 | Bidirectionnelle (Dépend de ×16, Utilisé par ×14), calibration à jour | OK |
| Arbitres écosystème | answer-key-checker 16/16 PASS (testé) ; verify-cross 99/99 (Task 13) | OK — mais **aucun n'oblige la finalisation du plan** (E-1) |

## 3. Écarts détectés (classés S1-S3)

**E-1 [S1 — CAUSE RACINE] Aucune garde mécanique sur la chaîne de finalisation du plan.** La philosophie #5 (« Visible progress ») et les étapes E7/E8/R5 sont déclaratives : aucune règle du SKILL.md n'exige qu'un plan écrit soit systématiquement suivi de (a) l'exécution de l'arbitre E8, (b) l'entrée worklog R5, (c) un bloc récapitulatif visible au chat. Aucun script ne vérifie l'état « plan écrit mais protocole incomplet ». Conséquence : toute interruption (fin de contexte, stop utilisateur, bug de session) après l'écriture du fichier laisse un plan invisible et non validé, sans détection à la reprise.

**E-2 [S1] Hook E1-RES borné à « l'ouverture de session ».** Le contrôle de fraîcheur du plan (re-génération si gen-plan modifié/validé — KO-L005/L005) ne se déclenche qu'à l'ouverture de session, AVANT E1. Une correction arrivant **pendant** un plan en vol (l'habitude déclarée du propriétaire) est routée par le mode NULL vers « intégration E13 ou exécution classique » sans ré-exiger la chaîne complète (re-validation E8 + R5 + affichage). C'est le trou protocolaire exact du scénario reproduit 3 fois.

**E-3 [S2] L'affichage du plan n'est opérationalisé nulle part.** E7 liste ses outputs (plan structuré, TODO, étapes parallélisables) et E8 ses critères (cohérence, complétude, faisabilité) — aucun des deux ne comporte un critère « le plan a été rendu visible au propriétaire » ni un format standard de récapitulatif. Le marqueur mécanique de preuve d'affichage n'existe pas.

**E-4 [S2] L'entrée worklog de génération de plan n'est pas vérifiable mécaniquement.** R5 est une convention ; aucun check ne confirme « le plan courant a bien une entrée worklog dédiée » — d'où le Task 14 perdu sans alerte.

**E-5 [S2] Gap de couverture evals.** Les 12 cas trigger_evals ne contiennent aucun cas « interruption mi-plan + correction → reprise conforme » ; les 8 evals ne contiennent aucun cas « protocole de finalisation complet ». Le bug était donc structurellement invisible pour la campagne d'évaluation.

**E-6 [S3] verify-cross.py ne porte aucun check gen-plan (grep vide)** — la cascade KO-L004 du correctif devra recalibrer les arbitres dépendants présents localement.

## 4. Correction décidée (→ G7 du plan)

1. **Hook E7-DISP** (nouveau, §1.2bis) : toute écriture/mise à jour du fichier plan (E7, E13, re-génération) exige la chaîne complète — plan + answer key + arbitre E8 exécuté + entrée worklog R5 + marqueur `PLAN-AFFICHE` + bloc récapitulatif visible au chat (titre, groupes, #token, verdict E8, chemin).
2. **Extension E1-RES** : le contrôle s'applique à TOUT message utilisateur arrivant pendant un plan en vol (reprise après interruption) : lecture préalable → contrôle de fraîcheur → E13 → re-validation E8 → R5 → affichage.
3. **Nouvel arbitre `scripts/check_plan_protocol.py`** (P1-P5 + selftest) : rend l'état « plan écrit / protocole incomplet » mécaniquement détectable et échec bloquant (KO-L003 : invariants dérivés de l'état courant).
4. **Cascade KO-L004** : bump v3.24.0 (MINOR), KB recalibrée, evals +1 cas trigger (+1 eval), arbitres dépendants re-vérifiés, PM régénéré mécaniquement si l'outil le permet.
5. **Test robuste (→ G8)** : reproduction du bug sur l'état actuel (FAIL attendu de l'arbitre = preuve de détection), cycle corrigé en sandbox (PASS), idempotence ×2.

## 5. Conclusion

gen-plan v3.23.1 est structurellement sain (16 fichiers cohérents, arbitres PASS, KB à jour) mais **incomplet sur un point de protocole critique : la finalisation du plan n'est ni exigée textuellement ni vérifiable mécaniquement**. La correction v3.24.0 (hook E7-DISP + extension E1-RES + arbitre check_plan_protocol.py + cascade KO-L004) transforme la chaîne E7→E8→R5→affichage en obligation vérifiable, fermant le scénario d'interruption qui a produit les 3 occurrences du bug.
