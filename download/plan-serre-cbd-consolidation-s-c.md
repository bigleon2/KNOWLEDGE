# Plan d'actions — Exécution cahier-des-charges SERRE CBD avec 3 sources réelles (consolidation S-C + export PDF)

> Généré par **gen-plan v3.24.0** (hook E7-DISP — protocole complet) · Directive propriétaire du jour :
> *« exécute mon skill « cahier-des-charges » avec comme sources « https://chat.z.ai/s/aeec48ec-09d9-4513-bd27-a3c49e1de7b2 », le PDF que je t'ai envoyé et l'article Science & Vie … qui m'a inspiré le projet "SERRE CBD" »*
> Contexte : le plan précédent (plan-cahier-des-charges-v2.0.1.md, G0-G9) est TERMINÉ (Tasks 14-20) — dont le test fonctionnel M5→M7 avait produit 5 livrables avec S-C (discussion) **indisponible** et substituée par le PDF. La présente directive reprend le point ouvert : extraire S-C RÉELLE, consolider les livrables, exporter le PDF promis (L-1 « Markdown (+ PDF en M3 VALIDER) »).
> Non-régression R2 : le plan clôturé et son verdict E8 ne sont pas modifiés — nouveaux groupes **G10-G14** dans un fichier séparé.
> Session : web-dd290b0d · Date : 2026-10-25 · Profil : **NORMAL** · Skill exécuté : cahier-des-charges **v2.0.1** (discipline)
> **MAJ v2 (E13 — 2026-10-24T19:09:47Z, règle d'or n°3 : extension, jamais réécriture destructrice)** : directive propriétaire additionnelle « analyse approfondie des causes du bug gen-plan (apparu à la génération de sa v3.24.0, discussion s/64c90144) + reconstruction éventuelle depuis la discussion et l'historique GitHub » — nouveaux groupes **G15 (analyse approfondie + rapport)** et **G16 (reconstruction gen-plan v3.27.0 : lignée canonique dépôt v3.26.0 + report apports E7-DISP du fork local)**, décisions **D009-D014**. Correction R3 apposée (Task 22) : l'entrée Task 21 affirmait « bloc récapitulatif affiché au chat » — FAUX à l'époque (tour coupé par erreur d'outil « context canceled » AVANT l'affichage) ; l'affichage est rejoué après cette MAJ. Preuves nouvelles : discussion 64c90144 extraite (upload/discussion-gen-plan-64c90144.md, 22 406 octets) + historique GitHub (clone e6a9595 : lignée canonique v3.24.0-parallélisation → v3.25.0-step → v3.26.0-leçons, remote = e6a9595).

Horodatage plan : 2026-10-24T19:23:33Z
Verdict E8 : PASS (answer-key-checker 16/16 ×2 · verify-cross 100,0 % · selftest check_plan_protocol 7/7 · hook correct-work(plan) — Horodatage vérifié : 2026-10-24T19:23:33Z)

## Sources de la directive (verbatim consolidé)

1. **S-C** Discussion https://chat.z.ai/s/aeec48ec-09d9-4513-bd27-a3c49e1de7b2 — **EXTRÄTE RÉELLE en cadrage pré-plan** (G10) : navigateur headless agent-browser (rendu JS — le SDK web-reader seul rendait 0 texte), transcript 22 598 octets / 10 messages archivé `upload/discussion-serre-cbd.md`.
2. **S-B** PDF « Résumé Global Des Références Serre CBD » — extrait intégralement (Task 19, inchangé).
3. **S-A** Article Science & Vie SV-238443 (source d'inspiration fondatrice) — extrait verbatim (Task 13/19, inchangé).

## Apports identifiés de S-C (cadrage — preuve transcript)

- **A-1 (contractuel)** : un **amendement M4 FAIRE ÉVOLUER du CDC Serre CBD est en suspens** « à réception du contenu Copilot » (2 occurrences au transcript) — le CDC doit documenter ce jalon d'évolution.
- **A-2 (contrainte opérationnelle)** : le propriétaire exploite dans un **cadre de gouvernance discipliné** — worklog append-only, arbitres mécaniques (idempotence ×2), publication contrôlée au GO (règle d'or n°4), audit anti-persistance des jetons, clone-chat — cadre dans lequel les livrables Serre CBD s'inscrivent.
- **A-3 (négatif, honnêteté R3)** : la discussion porte sur l'écosystème de skills (clone-chat, correct-work, vue-upload, publication GitHub) — **aucune exigence fonctionnelle système nouvelle** (capteurs, seuils, PLC) : la batterie M7 reste valide telle quelle, re-validation par re-run ×2 uniquement.

## Groupes d'exécution

### G10 — Extraction S-C réelle (cadrage pré-plan — DÉJÀ EXÉCUTÉ, tracé ici pour R3) — #token 1500
- 10.1 Sonde web-reader seule → 0 texte (app JS) — méthode remplacée par **agent-browser** (headless, rendu JS réel).
- 10.2 Ouverture + networkidle + titre « Serre CBD Automatisée » ✓ · sonde DOM : 10 messages (5×`.chat-user`, 5×`.chat-assistant`) · scroll ×3 → pas de lazy-loading (10 messages = totalité).
- 10.3 Transcript extrait, décodé JSON, archivé `upload/discussion-serre-cbd.md` (22 598 octets) ; apports A-1/A-2/A-3 catalogués.

### G11 — M5 ANALYSER (consolidation) : fiche-domaine v1.1.0 — #token 1500
- 11.1 fiche-domaine-serre-cbd.md : S-C passe de « indisponible, substituée » à **source réelle** (transcript, méthode, apports A-1/A-2/A-3) ; profil SE **standard inchangé** ; hypothèses [HYP-01..05] inchangées (A-3).
- 11.2 Cohérence croisée fiche ↔ CDC (S-C identique des deux côtés).

### G12 — M2/M4 consolidation CDC v1.1.0 (bump MINOR du livrable, R2 : v1.0 conservée en historique) — #token 3000
- 12.1 En-tête : version livrable **v1.1.0** + date + motif « consolidation S-C réelle ».
- 12.2 §3 parties prenantes : cadre de gouvernance discipliné du propriétaire (A-2) intégré au rôle exploitant.
- 12.3 §7 contraintes opérationnelles : contrainte de gouvernance (journalisation, arbitres, publication au GO, hygiène secrets — cohérente ENF-03).
- 12.4 §9 jalons : **J-M4** — amendement FAIRE ÉVOLUER en suspens (contenu Copilot attendu, trace S-C).
- 12.5 §12 sources : S-C réécrite (source réelle + contenu + archivage) — substitution S-B **levée** ; Annexe D alignée.
- 12.6 Annexe « Historique des révisions » (v1.0.0 → v1.1.0, provenance S-C).

### G13 — M3 VALIDER + export PDF promis (L-1) — #token 2500
- 13.1 Export PDF du CDC v1.1.0 (pipeline Report — ReportLab, polices enregistrées, sauts de page uniquement couverture→corps) → `download/cahier-des-charges-serre-cbd-v1.1.0.pdf`.
- 13.2 Vérifications mécaniques : version, sources S-A/S-B/S-C, absence de « indisponible à l'extraction », amendement M4 présent ; batterie M7 re-run **PASS ×2** (A-3 : aucune exigence modifiée, idempotence).

### G15 — Analyse approfondie causes racines du bug gen-plan (directive additionnelle — dédup vérifié) — #token 2500
- 15.1 Dédup : l'audit v3.23.1 (Task 15, rapport audit-gen-plan-v3.23.1.md) couvrait l'état v3.23.1 avec l'hypothèse « interruption utilisateur » — INVALIDÉE partiellement par les preuves nouvelles (bug sans interruption + coupures plateforme) → analyse nouvelle, non dupliquée.
- 15.2 Preuves : discussion 64c90144 extraite (5 paires — coupure au 1er « go », journal aspirant, réconciliation repo→hôte, constat « gen-plan vit côté dépôt ») ; historique GitHub (lignée canonique v3.24.0-parallélisation/v3.25.0-step/v3.26.0-leçons ; collision avec le fork local E7-DISP homonyme).
- 15.3 Causes racines qualifiées : **RC1** collision de lignée (2 gen-plan v3.24.0 indépendants — fork local ignorait les leçons v3.25.0/v3.26.0 dont la règle d'or n°5 anti-aspirant) ; **RC2** double emplacement (dépôt = source R4 vs miroir hôte — instances différentes chargées selon la session) ; **RC3** reprise post-coupure incomplète (E1-RES dépend de l'instance chargée) ; **RC4** interruption plateforme (« context canceled » — l'affichage, dernière maillon de la chaîne, n'était pas REJOUABLE) → contre-mesure v3.27.0 : affichage rejouable à toute reprise.
- 15.4 Rapport `download/analyse-causes-racines-gen-plan.md` (preuves, causes, contre-mesures) ; hook correct-work(groupe, CIBLE).

### G16 — Reconstruction gen-plan v3.27.0 (lignée canonique dépôt + report apports E7-DISP) — #token 3000
- 16.1 Base canonique = clone dépôt e6a9595 (v3.26.0 — philosophie #4, règle d'or n°5, §5.5 step, dégradation 429) ; report depuis le fork local : hook E7-DISP (table §1.2bis + paragraphe dédié), extension E1-RES (reprise après interruption + affichage rejouable — leçon Task 22), arbitre `check_plan_protocol.py` (P1-P5 + garde anti-verdict-périmé, selftest 7/7), §2.2 recalibré, évals fusionnées (13 cas).
- 16.2 Journal du SKILL : entrée v3.27.0 documentant la COLLISION v3.24.0 (fork local vs lignée dépôt) et la fusion.
- 16.3 Cascade KO-L004 : entrée KB gen-plan → v3.27.0 (dépôt + hôte si présent) ; PM régénéré si générateur disponible (sinon S3 journalisée) ; commit local du clone (publication au GO — jeton éphémère, règle d'or n°4).
- 16.4 Projection miroir hôte `skills/gen-plan/` = dépôt (byte-identité ×2) ; arbitres : selftest check_plan_protocol ×2, verify-cross, É1-INSTALLED ; hook correct-work(groupe, CIBLE).

### G14 — correct-work (projet, équivalent mécanique) + clôture — #token 1500
- 14.1 Arbitres : check_plan_protocol.py PASS sur ce plan · batterie ×2 · cohérence inter-artefacts (fiche ↔ CDC ↔ PDF ↔ worklog).
- 14.2 Worklog final (R5) ; résumé propriétaire : livrables consolidés + 2 rappels S-C (amendement M4 attend le contenu Copilot ; publication bigleon2/KNOWLEDGE au GO + jeton éphémère — suggestion ④ du transcript).

## Answer key (hook E1 — décisions vérifiables mécaniquement)

```yaml
decisions:
  - id: "D001"
    criterion: "La discussion S-C est extraite et archivée (transcript non vide, 5 messages utilisateur au moins)"
    verification: "test -s upload/discussion-serre-cbd.md && [ $(grep -c 'UTILISATEUR' upload/discussion-serre-cbd.md) -ge 5 ] && echo PASS"
    source: "directive propriétaire (S-C comme source explicite) + cadrage G10"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "La fiche-domaine v1.1.0 cite S-C comme source réelle extraite par navigateur headless"
    verification: "grep -c 'agent-browser' download/fiche-domaine-serre-cbd.md"
    source: "G11.1 (M5 consolidation)"
    priority: "S2"
    status: "verified"
  - id: "D003"
    criterion: "Le CDC v1.1.0 ne décrit plus S-C comme indisponible (substitution levée)"
    verification: "if grep -q 'indisponible à l.extraction' download/cahier-des-charges-serre-cbd.md; then echo FAIL; else echo PASS; fi"
    source: "G12.5 (levée de la substitution Task 19)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Le CDC documente l'amendement M4 en suspens (contenu Copilot, trace S-C)"
    verification: "grep -c 'Copilot' download/cahier-des-charges-serre-cbd.md"
    source: "A-1 (apport contractuel S-C) + G12.4"
    priority: "S2"
    status: "verified"
  - id: "D005"
    criterion: "Le PDF promis par L-1 existe et est non vide (v1.1.0)"
    verification: "test -s download/cahier-des-charges-serre-cbd-v1.1.0.pdf && echo PASS"
    source: "L-1 « Markdown (+ PDF en M3 VALIDER) » + G13.1"
    priority: "S2"
    status: "verified"
  - id: "D006"
    criterion: "La batterie M7 re-rend PASS ×2 (code 0, idempotence — A-3)"
    verification: "cd download/batterie-tests-serre-cbd && python3 run_all.py ; echo RC=$? (×2)"
    source: "G13.2 (re-validation, aucune exigence modifiée)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "L'arbitre check_plan_protocol.py rend PASS sur ce plan (P1-P5)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-serre-cbd-consolidation-s-c.md --worklog worklog.md ; echo RC=$?"
    source: "hook E7-DISP (gen-plan v3.24.0) — anti-récidive bug affichage"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Le CDC porte une section Historique des révisions (v1.0.0 → v1.1.0)"
    verification: "grep -c 'Historique des révisions' download/cahier-des-charges-serre-cbd.md"
    source: "G12.6 (traçabilité d'évolution du livrable)"
    priority: "S3"
    status: "verified"
  - id: "D009"
    criterion: "La discussion 64c90144 (génération v3.24.0) est extraite et archivée"
    verification: "test -s upload/discussion-gen-plan-64c90144.md && grep -c 'UTILISATEUR' upload/discussion-gen-plan-64c90144.md"
    source: "directive propriétaire (analyse depuis la discussion s/64c90144) + G15.2"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Le rapport d'analyse des causes racines existe (RC1-RC4 + contre-mesures)"
    verification: "test -s download/analyse-causes-racines-gen-plan.md && grep -c 'RC1\|RC2\|RC3\|RC4' download/analyse-causes-racines-gen-plan.md"
    source: "directive propriétaire (analyse approfondie des causes possibles) + G15.4"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "gen-plan reconstruit en v3.27.0 aux DEUX emplacements (dépôt + miroir hôte) avec le hook E7-DISP et la règle d'or n°5"
    verification: "grep -m1 '^version: 3.27.0' ecosysteme-install/repo/skills/gen-plan/SKILL.md skills/gen-plan/SKILL.md && diff -rq skills/gen-plan ecosysteme-install/repo/skills/gen-plan"
    source: "directive propriétaire (reconstruction depuis discussion + historique GitHub) + G16.1/16.4"
    priority: "S1"
    status: "verified"
  - id: "D012"
    criterion: "L'arbitre check_plan_protocol.py est présent dans l'instance reconstruite et son selftest passe ×2"
    verification: "python3 ecosysteme-install/repo/skills/gen-plan/scripts/check_plan_protocol.py --selftest"
    source: "G16.1 (report du garde mécanique) — anti-récidive bug affichage"
    priority: "S1"
    status: "verified"
  - id: "D013"
    criterion: "La collision de version v3.24.0 est documentée dans le journal du SKILL reconstruit"
    verification: "grep -c 'collision' ecosysteme-install/repo/skills/gen-plan/SKILL.md"
    source: "G16.2 (traçabilité fusion des lignées)"
    priority: "S2"
    status: "verified"
  - id: "D014"
    criterion: "Le KB du dépôt porte l'entrée gen-plan v3.27.0 (cascade KO-L004)"
    verification: "grep -c 'gen-plan v3.27.0' ecosysteme-install/repo/skills/KNOWLEDGE.md"
    source: "G16.3 (cascade KO-L004 — convention écosystème)"
    priority: "S2"
    status: "verified"
```

## Hooks de validation (E8) et règles d'exécution

- Arbitres frais : answer-key-checker **16/16** ×2 · verify-cross **100,0 %** — à re-jouer en G14 (idempotence ×2).
- Règles : série par défaut · R1-R6 idempotence · R2 non-régression (plan clôturé intact) · R3 traçabilité worklog · N3 scripts stdlib · KO-L001 (1 sonde/tour) · File Output Rule (livrables → download/).
- FAIL à tout hook → pause + correction + re-validation E8 (horodatages couplés).
