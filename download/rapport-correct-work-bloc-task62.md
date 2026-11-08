# Rapport correct-work — Task 62 (projet écosystème, post-Task 61)

## Métadonnées
- **Date** : 2026-11-07
- **Mode** : PROJET (option « bloc par bloc » — `--bloc`)
- **Version correct-work** : 2.11.0
- **Plan de vérification (Étape 1)** : `download/plan-task62-correct-work-projet-bloc.md` — généré via **gen-plan v3.37.1** (invocation `gen-plan : "correct-work"`, mode NULL), E8 PASS 09:12:00Z, answer key D001-D012
- **Cible** : écosystème Knowledge post-Task 61 (session web-c30e6506, suites 12-21) + état post-réinstallation du 22ᵉ recyclage sandbox + préparation push (15 commits)

## Étape 1 — Plan d'actions
Plan généré via gen-plan v3.37.1 (dernière version installée — §1.5 correct-work) : 4 groupes G1-G4, 12 décisions D001-D012, estimation ~49 k #token + 15 k marge — verdict E8 PASS (answer-key-checker 16/16 ALL PASS ; check_plan_protocol P1-P5 PASS).

## Étape 2 — Erreurs et omissions

| # | Sévérité | Description | Emplacement | Correction proposée |
|---|----------|-------------|-------------|---------------------|
| F-62-1 | S2 | PM GEN-PLAN v3.37.0 résiduel dans le corpus (10 fichiers vs 9 attendus — Architecture v2.0) : archivage R4 de la Task 61 G3 exécuté en COPIE vers @historique sans retrait du corpus côté dépôt ; divergence hôte/dépôt restée latente (rsync miroir sans `--delete`), scellée par les commits d15c0a9/ae24212, révélée par la réinstallation du 22ᵉ recyclage (sync dépôt→hôte delete=True) | `skills/@mon-ecosysteme/` (hôte+dépôt) | **RÉSORBÉE** : purge corpus ×2 arbres + retrait sanctionné (SHA d002ba40 byte-identité prouvée par la garde anti-perte) + re-scellement archive 9 entrées + arbitres 0 FAIL ×2 |
| F-62-2 | S3 | 23ᵉ disparition de version-management — INTRA-SESSION cette fois (entre les arbitres passe 1 à ~09:08 et le ls de ~09:16) : la volatilité snapshots ne frappe plus seulement entre les sessions | `skills/version-management/` | Auto-réparée par la garde (INSTALLE-REPARÉ, rc=0) — pattern nouveau documenté |
| F-62-3 | S3 | 24ᵉ disparition de version-management (~09:30, entre la certification intermédiaire et la re-certification C3) — volatilité CONTINUE pendant la session | `skills/version-management/` | Auto-réparée par la garde (INSTALLE-REPARÉ, rc=0) + re-certification 110/110 immédiate — pattern à surveiller (la garde absorbe structurellement) |
| F-62-4 | S4 | Libellés stale « archive v2.3 / 15 entrées / corpus 9/9 + piliers 6/6 » : worklog Task 61 (suites 16/20) et docstring du check 2 integrity citent le véhicule v2.3-piliers qui a été RETIRÉ au profit du v2.2 corpus-seul (PM-INSTALL v1.8.0 — commentaires explicites du rebuild-archive l.89-92) | worklog, `scripts/check-ecosysteme-integrity.py` (docstring) | Documentation (le véhicule réel v2.2 corpus-seul est celui scellé et vérifié ; les libellés seront recalés à la prochaine montée des scripts concernés) |
| F-62-5 | S4 | Sceaux SHA README §5 sans entrées v3.37.x (le dernier scellé documenté : v3.36.0 en suite 16 ; les 42/42 restent OK — le PM v3.37.0 archivé n'a pas de sceau dédié) | `skills/@historique/README.md` §5 (ou équivalent) | Lag de sceaux — à ajouter à la prochaine montée (non bloquant, check 42/42 OK) |
| F-62-6 | S4 | `eco_install_pipeline.py --help` DÉCLENCHE l'installation réelle (aucun parsing d'arguments) — comportement surprenant pour un opérateur (vécu ce jour : la première invocation « --help » a exécuté la réinstallation complète) | `scripts/eco_install_pipeline.py` | À documenter/garder en mémoire d'exécution ; proposition : parsing d'args à une future montée |
| F-62-7 | S4 | `ensure-installed.py` rapporte `head: ce22a14` = HEAD du repo HÔTE (`/home/z/my-project/.git`), pas du miroir KNOWLEDGE-repo (ae24212) — ambiguïté de traçabilité dans le rapport JSON | `skills/gen-plan/scripts/ensure-installed.py` | Documentation (le champ désigne le repo détecté à la racine hôte) |

## Étape 3 — Structure et conflits

| # | Type | Description | Fichiers concernés | Résolution |
|---|------|-------------|-------------------|------------|
| F-62-8 | Mode-changes | 55 fichiers en mode-change pur (`100644 => 100755`, 0 insertion/0 deletion) sur le miroir après les écritures G4 Task 61 + la réinstallation — réapparition du même artefact que les 121 normalisés en G3 Task 61 | `download/*.md`, `download/tests-task61/*.json`, `tmp/mission-task58/*`, … | **RÉSOLU** : modes HEAD restaurés (chmod -x) — git status réduit aux 2 changements réels du correctif Task 62 |
| — | Divergences hors-KB | 15 SKILL.md divergents hôte/dépôt (ASR, LLM, TTS, VLM, agent-browser, charts, docx, gif-animator(-pro), image-edit/generation/search, pdf, pptx, task-review) + 67 « Only in dépôt » | skills plateforme (hors registre KB) | **LÉGITIME** : le périmètre sync = écosystème KB uniquement ; les skills plateforme divergent par conception (copies de référence du dépôt) — aucune action |
| — | Retrait sanctionné | L'entrée `PROMPT-MAITRE-GEN-PLAN-v3.37.0.md` manquait à RETRAITS_SANCTIONNES (le re-scellement échouait proprement en « extra hors homologues » — garde anti-faux-succès F1 Task 22 CONFORME) | `scripts/task21-f2-rebuild-archive.py` | **RÉSOLU** : retrait sanctionné ajouté avec traçabilité complète (cascade v3.37.1, commit d15c0a9, finding F-62-1, SHA d002ba40…) — re-scellement 9 entrées round-trip OK |

## Étape 4 — Interactions

| # | Skill A | Skill B | Type d'interaction | Statut |
|---|--------|--------|-------------------|--------|
| 1 | correct-work v2.11.0 | gen-plan v3.37.1 | Couplage Étape 1 (§1.5) + correctifs mode STEP (§1.5bis) | OK — plan généré via la dernière version installée, lot correctifs structuré G3 |
| 2 | gen-plan v3.37.1 | pm-skill v1.0.1 | « Utilisé par » KB += pm-skill (F1 Task 61) | OK — bidirectionnalité vérifiée (pm-skill « Dépend de » : gen-plan >= 3.20.0 + correct-work >= 2.4.0) |
| 3 | correct-work v2.11.0 | pm-skill v1.0.1 | Certification post-intégration (F2 Task 61) | OK — dependencies += correct-work présent, réciproque KB présente |
| 4 | gen-plan | resource-monitor | Hook E1-RES (G-RES) | OK — verdict OK/PARALLELE collecté et consigné |
| 5 | gen-plan | version-management (garde Task 56) | É1-INSTALL auto-réparant | OK — 2 mobilisations réelles intra-session (INSTALLE-REPARÉ ×2, rc=0, 0 jeton) — 3ᵉ/4ᵉ preuves vivantes après les 20ᵉ/21ᵉ disparitions |
| 6 | rebuild-archive v2.2 | integrity (check 2) | Round-trip archive ↔ corpus | OK après re-scellement (9 entrées, 0 divergent, 0 extra) |

## Étape 5 — Cohérence des raisonnements

| # | Point vérifié | Résultat | Détail |
|---|---------------|----------|--------|
| 1 | Annonce « PM v3.37.0 archivé R4 (SHA d002ba40…) » (worklog suite 20) | VRAIE sur la copie, INCOMPLÈTE sur le retrait | Le SHA @historique == d002ba40 exactement (vérifié) ; le retrait du corpus côté dépôt manquait (F-62-1) — la relecture honest : l'integrity hôte 110/110 ×2 de l'époque restait légitime (l'arbitre vérifie l'hôte, la divergence vivait côté dépôt) |
| 2 | Annonce « 121 modes normalisés — 0 restant » (G3 Task 61) vs 55 M constatés | EXPLIQUÉ, pas un faux | Les 55 sont APPARUS APRÈS la normalisation (écritures G4 + réinstallation) — normalisés à nouveau en C4 |
| 3 | Chronologie Task 61 → recyclage → Task 62 | COHÉRENTE | Task 61 CLOSE 08:39 → recyclage (piliers absents au constat 09:07) → réinstallation → F-62-1 → correctifs |
| 4 | Comptages push | COHÉRENTS | 14 commits (G4 Task 61) + commit de clôture ae24212 = 15 en attente (rev-list vérifié) ; le push appartient au propriétaire (KO-L009) |
| 5 | Verdicts arbitres passe 1 (109/110 + FAIL coherence) | FIDÈLES au disque | Les FAIL reflétaient le corpus à 10 fichiers — cause racine traitée, re-certification 0 FAIL ×2 |

## Blocs vérifiés (option `--bloc` §1.7 — verdicts individuels, corrections re-vérifiées)

| Bloc | Contenu | Étapes couvertes | Findings | Verdict |
|------|---------|------------------|----------|---------|
| B1 | Incident 22ᵉ recyclage + réinstallation | 2-5 | F-62-2, F-62-3 (S3), F-62-6, F-62-7 (S4) | **PASS AVEC RÉSERVES** (volatilité intra-session — garde absorbante) |
| B2 | Montées gen-plan v3.37.0/v3.37.1 + cascade KO-L004 | 2-5 | F-62-1 (S2, **résorbé** : arbitres 0 FAIL ×2), F-62-4, F-62-5 (S4) | **PASS** (post-correction) |
| B3 | Correctifs Task 61 G3 (pm-skill v1.0.1, analyse-doc v1.3.1, trigger_evals 15, ULTRA, modes 121) | 2-4 | 0 | **PASS** |
| B4 | Livrables G4 Task 61 (rapport final + RAPPELS, clone-chat 8 sections, plan 13/13, E8 08:39) | 2-5 | 0 | **PASS** |
| B5 | Empaquetage push (fsck propre, 15 commits linéaires, fichiers critiques présents, commande push préparée) | 2-5 | F-62-8 (S3, **résolu** : modes normalisés, git status propre) | **PASS** (post-correction) |
| B6 | Worklog ↔ disque (règle d'or n°5) | 2-5 | F-62-4 (S4, libellés stale v2.3) | **PASS AVEC RÉSERVES** |
| B7 | Agrégation | — | — | cf. Résumé |

## Résumé
- **Problèmes trouvés** : 8 findings (0 S1 · 1 S2 · 3 S3 · 4 S4)
- **Corrections appliquées** : 5 (C1 purge corpus ×2 arbres · C2 retrait sanctionné + re-scellement archive 9 entrées round-trip OK · C3 re-certification 4 arbitres 0 FAIL ×2 [110/110 · 54/25/0 · 16/16 · 100 %] avec 2 réparations garde version-management · C4 normalisation 55 mode-changes + commit correctif · C5 leçon rsync `--delete` consignée au worklog)
- **Problèmes restants** : 5 S3/S4 documentés (volatilité intra-session ×2 — absorbée structurellement par la garde ; libellés stale v2.3 ; sceaux v3.37.x en lag ; --help pipeline ; head ambigu ensure-installed)
- **Verdict global (B7 — pire des verdicts de blocs, post-corrections)** : **PASS AVEC RÉSERVES**

---
*Rapport généré le 2026-11-07 par correct-work v2.11.0 — plan `plan-task62-correct-work-projet-bloc.md` (gen-plan v3.37.1, E8 PASS). Taux de correction S1/S2 : 100 % (1/1). Métriques §2.8 : findings_total = 8 ; findings par étape : E2 = 7, E3 = 2 (dont 1 légitime), E4 = 0, E5 = 0 ; taux_correction = 5/8 (S1/S2 : 100 %) ; temps_par_mode : PROJET --bloc ~35 min.*
