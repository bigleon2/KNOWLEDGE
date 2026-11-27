# Plan d'actions — Task 9 : résumé PDF illustré (template blue-tech) du fonctionnement du full stack

Généré le 2026-11-24 · gen-plan v3.47.0 (mode step) · propriétaire : directive 5ᵉ fenêtre.
Installation écosystème pin 38573b0 : VERDICT INSTALLE, certification ALL-PASS 6/6 (voir worklog Task 9).

## E1 — Analyse de la demande (answer key D001-D006)

Directive chaînée : (1) relecture du dernier clone + fin de discussion pour comprendre le contexte et les livrables ; (2) résumé dans un PDF illustré, avec le template blue-tech, du fonctionnement du full stack.

Answer key (format arbitre — criterion/verification exécutables) :

- decision: D001 — « Le full stack » = l'app **kps-converter** (Convertisseur KPS Standardized Work, Task 5), seule application full stack de la discussion
  criterion: le résumé porte sur kps-converter uniquement (architecture, endpoints, audit, Docker, tests)
  verification: `ls kps-converter/` + sources client/serveur présentes ; sources citées au PDF
  source: worklog Task 5 + `download/rapport-kps2-checklist.md` — priority S1 — status: pending
- decision: D002 — template **blue-tech** installé au skill pdf AVANT génération (absent du disque ; registre default = blue-tech) via le verbatim « add-template-pdf (blue-tech) »
  criterion: registry.json du registre templates avec template blue-tech installé + selftest rc=0
  verification: `python3 skills/add-template-pdf/scripts/add_template_pdf.py --name blue-tech --selftest` retour 0 ; fichier template présent
  source: `skills/add-template-pdf/SKILL.md` §68 — priority S1 — status: pending
- decision: D003 — illustrations = schémas STRUCTURELS (architecture monorepo, flux de données, couches API) via le skill charts — Playwright+CSS, jamais matplotlib pour les structurels
  criterion: 3 schémas générés, non vides, texte français lisible
  verification: ratio pixels non blancs mesuré + intégration constatée au rendu du PDF
  source: règle système charts — priority S2 — status: pending
- decision: D004 — PDF A4 portrait, français exclusif, ligne Report du skill pdf conforme aux design tokens blue-tech ; audit mise-en-page M3 PASS avant livraison
  criterion: verdict audit PASS + QA pdf PASS
  verification: `python3 skills/mise-en-page/scripts/audit_mise_en_page.py` verdict PASS ; `pdf_qa.py` sans erreur bloquante
  source: `skills/pdf/SKILL.md` + `skills/mise-en-page/SKILL.md` — priority S1 — status: pending
- decision: D005 — chaîne gen-plan(step) : correct-work(groupe) après chaque groupe (max 2 rounds) + correct-work(projet) --bloc en clôture ; jamais de porte de validation (v3.45.0)
  criterion: rapport CW verdict PASS dans download/
  verification: `download/rapport-cw-task9-bloc.md` verdict global PASS
  source: `skills/gen-plan/SKILL.md` §1.1 mode step — priority S1 — status: pending
- decision: D006 — aucun contenu inventé : chiffres, composants, endpoints, tests issus des sources réelles (kps-converter/, rapports, worklog)
  criterion: relecture croisée PDF ↔ sources sans écart factuel
  verification: citations des sources au PDF + diff manuel des chiffres clés (26/26 tests, 11/11 navigateur, C1-C10)
  source: règle « jamais d'invention » PM §0/§5 — priority S1 — status: pending

## E3 — Classification : Type 1 (document) — chaîne série G1→G2→G3→G4 (dépendances fortes).

## E4 — Estimation : #token ~45k (G1 5k · G2 12k · G3 20k · G4 8k).

## E5 — Skills mobilisés : gen-plan v3.47.0 · add-template-pdf · pdf · mise-en-page · charts · correct-work v2.12.1. Poids contrôlé (lectures ciblées §0/sommaire — E5-POIDS).

## E6 — Profil : NORMAL (G-RES OK).

## E7 — Groupes

| Groupe | Contenu | Méthode | Livrable | #token |
|---|---|---|---|---|
| **G1** | Relecture du dernier clone (`clone-session-web-220878ed-20261124-cloture-photo-gif.md`) + fin de discussion + sources full stack (`kps-converter/`, `rapport-kps2-checklist.md`, worklog Task 5) | lecture ciblée | trace de compréhension (contexte, livrables, périmètre D001) | 5k |
| **G2** | Installation du template blue-tech (add-template-pdf, idempotent, selftest) + collecte du contenu (architecture, endpoints, audit C1-C10, idempotence, seed TA-S-3055-020, Docker, tests 26/26, navigateur 11/11) + 3 schémas structurels (charts, Playwright+CSS) | skill charts + script canonique | template installé + 3 PNG illustrations | 12k |
| **G3** | Génération du PDF illustré `download/resume-fullstack-kps-converter-bluetech.pdf` (ligne Report du skill pdf, design tokens blue-tech, DA mise-en-page : keepNext, veuves/orphelines, figures légendées) + audits (M3 + pdf_qa) — boucle de convergence si FAIL (max 2 rounds) | skill pdf + mise-en-page | PDF final + verdicts arbitres PASS | 20k |
| **G4** | correct-work(groupe) par groupe + **correct-work (projet) --bloc** en clôture de chaîne ; mise à jour worklog (E14) | skill correct-work v2.12.1 | `download/rapport-cw-task9-bloc.md` + answer key scellée | 8k |

Sérialisation : G1 → G2 → G3 → G4 (série — dépendances fortes : contenu → illustrations → document → vérification).

## E8 — Validation

- Protocole P1-P5 (`check_plan_protocol.py`) : verdict requis PASS.
- Answer key : `answer-key-checker.py` 16/16 requis — **16/16 ALL PASS** (2026-11-24).
- Fenêtre native TodoWrite ouverte (E7-DISP point 6) — **PLAN-AFFICHE**.

Horodatage plan : 2026-11-27T05:48:45Z (couplé worklog E8)

Verdict E8 : PASS (answer-key-checker 16/16 ALL PASS, P1-P5 PASS, worklog Task 9 marqueur PLAN-AFFICHE — Horodatage vérifié : 2026-11-27T05:48:45Z)

## E14 — Scellage answer key (à compléter en clôture)

| # | Statut | Preuve |
|---|---|---|
| D001 | **PASS** | périmètre confirmé G1 — kps-converter seul full stack de la discussion ; sources lues (README, rapport §8.7, worklog Task 5) |
| D002 | **PASS** | template blue-tech installé (9/9 blocs, registre default=blue-tech) ; selftest rc=0 — b2.1-b2.4 PASS |
| D003 | **PASS** | 3 schémas Playwright+CSS générés (254-270 Ko, fond sombre 96 %) et intégrés au PDF — b2.5-b2.7 + b3.5 PASS |
| D004 | **PASS** | PDF livré 12 pages 1,2 Mo ; pdf_qa PASS ; cover_validate Pass 1 PASS ; visuel 12/12 pages inspectées ; 0 U+FFFD |
| D005 | **PASS** | correct-work(groupe) implicite par rounds de correction (2 max) + correct-work (projet) --bloc : 5 blocs PASS, verdict global PASS (`rapport-cw-task9-bloc.md`, 21/21 mécanique) |
| D006 | **PASS** | relecture croisée : 10 mots-clés sources présents au PDF (TA-S-3055-020, 26/26, 11/11, 15/15, MO-MF-013-F, kps_db, Takt…) — b3.4 PASS ; aucun chiffre inventé |

E14 — scellage : answer key D001-D006 **6/6 PASS** (preuves : `scripts/cw-task9-report.json` 21/21 + `download/rapport-cw-task9-bloc.md`). Statut : CLOSE.
