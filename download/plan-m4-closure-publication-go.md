# Plan d'actions — Clôture amendement M4 sans contenu Copilot + publication GitHub bigleon2/KNOWLEDGE (GO + jeton éphémère)

> Généré par **gen-plan v3.27.0** (fusion des lignées — hook E7-DISP, affichage REJOUABLE) · Directive propriétaire du jour (verbatim) :
> 1. *« pour l'amendement M4 du CDC, fais sans le contenu de COPILOT, je n'arrive pas à le retrouver. »*
> 2. *« go »* suivi du **jeton d'accès GitHub éphémère fourni en conversation** (règle d'or n°4 — le jeton n'est reproduit dans AUCUN artefact : ni plan, ni worklog, ni rapport, ni configuration git).
> Contexte : plan plan-serre-cbd-consolidation-s-c.md G10-G16 TERMINÉ (Tasks 21-24) — CDC v1.1.0 + PDF 12 pages + gen-plan v3.27.0 reconstruit (commits locaux 26d9846 + 2bb9beb). En suspens propriétaire levés par la présente directive : (1) jalon J-M4 attendait le contenu Copilot → clôture SANS ce contenu (introuvable) ; (2) publication GitHub attendait GO + jeton → GO fourni.
> Non-régression R2 : les plans clôturés (plan-cahier-des-charges-v2.0.1.md, plan-serre-cbd-consolidation-s-c.md) restent intacts — nouveaux groupes **G17-G21** dans ce fichier séparé.
> Session : web-dd290b0d · Date : 2026-10-25 · Profil : **NORMAL** · Skill exécuté : cahier-des-charges **v2.0.1** (M4 FAIRE ÉVOLUER) + protocole de publication (règle d'or n°4, précédent PUB-web-f90062ce).

## Découverte de cadrage (preuve mécanique — correctif RC2 intégré au plan)

Le **miroir hôte `skills/` a régressé** (restauration de sandbox) alors que le clone dépôt + download/ + upload/ + worklog sont intacts — le pattern **RC2 (double emplacement) / RC3** documenté dans analyse-causes-racines-gen-plan.md SE REPRODUIT : gen-plan et correct-work **absents** de `skills/`, KB `skills/KNOWLEDGE.md` absente, registre `skills/@historique/` absent, alias-eco hôte 1.0.0 vs dépôt 1.2.0, clone-chat hôte 2.0.1 vs dépôt 2.0.2, cahier-des-charges hôte **rétrogradé v1.0.0** (l'extension v2.0.0/v2.0.1 du host est annulée — la v2.0.1 canonique survit dans `download/cahier-des-charges-v2.0.1.zip`, 13 fichiers). Sens de réconciliation (KO-L003 — référentiel lu AVANT verdict) : **dépôt = source R4** ; exception cahier-des-charges où le zip canonique est la source (le dépôt lui-même est resté à v1.0.0 — trou de synchronisation, précédent da549af).

Horodatage plan : 2026-10-24T20:00:12Z
Verdict E8 : PASS (answer-key-checker 16/16 ×2 · verify-cross 100,0 % · selftest check_plan_protocol 7/7 ×2 instances · hook correct-work(plan) — Horodatage vérifié : 2026-10-24T20:00:12Z). Le verdict strict `check_plan_protocol --plan` (P1-P5) est dérivé en G21 après journalisation R5 (P3/P4 dépendent de l'entrée worklog — précédent Task 21).

## Sources de la directive

1. **Directive 1 (M4)** : clôture de l'amendement M4 FAIRE ÉVOLUER du CDC Serre CBD **sans le contenu Copilot** — le propriétaire ne retrouve pas ce contenu ; décision contractuelle tracée dans la discussion S-C (s/aeec48ec, suggestion ③ et 2 occurrences transcript).
2. **Directive 2 (publication)** : « go » + jeton éphémère → protocole de publication complet vers `bigleon2/KNOWLEDGE` (précédent PUB-web-f90062ce : push → vérification distale → journalisation → audit anti-persistance).

## Groupes d'exécution

### G17 — Ré-alignement miroir hôte (correctif RC2, découvert au cadrage) — #token 1500
- 17.1 Recensement mécanique des écarts dépôt→hôte (skills écosystème + KNOWLEDGE.md + @historique) — script persisté N3 stdlib.
- 17.2 Re-projection byte-identique : gen-plan, correct-work, alias-eco, clone-chat, skills-inventory, KNOWLEDGE.md, @historique/ — idempotent ×2 (diff -rq nul ×2).
- 17.3 cahier-des-charges : extraction v2.0.1 du zip canonique → **hôte ET dépôt** (commit dépôt dédié — trou de synchronisation résorbé).
- 17.4 Arbitres : selftest check_plan_protocol ×2 (dépôt + hôte), verify-cross, answer-key-checker.

### G18 — M4 FAIRE ÉVOLUER : clôture J-M4 sans Copilot (CDC v1.2.0 + fiche v1.2.0) — #token 2500
- 18.1 CDC → **v1.2.0** (bump MINOR — jalon contractuel résolu, **aucune exigence EF/ENF modifiée**) : en-tête versionné ; §9 jalon J-M4 passe de « en suspens » à **CLÔTURÉ** (décision propriétaire 2026-10-25 : contenu Copilot introuvable, amendement exécuté sans ce contenu, aucun apport contractuel à intégrer, aucune exigence nouvelle) ; §12 source [S-C] apports A-1 statut clôturé ; Annexe D alignée ; Annexe H ligne v1.2.0.
- 18.2 fiche-domaine → **v1.2.0** : A-1 passe de « en suspens » à « clôturé v1.2.0 sans contenu Copilot » — cohérence croisée fiche ↔ CDC.
- 18.3 Traçabilité : la promesse d'amendement S-C reste TRACÉE (aucun effacement d'historique — R2/R3) : la clôture documente POURQUOI le contenu Copilot n'entre pas (introuvable), pas son oubli.

### G19 — M3 VALIDER + export PDF v1.2.0 — #token 1500
- 19.1 Script persisté scripts/gen-cdc-serre-cbd-pdf.py édité (v1.2.0 : J-M4 clôturé, statuts L-1/L-2, A-1, Annexe H) → `download/cahier-des-charges-serre-cbd-v1.2.0.pdf` (pipeline Report ReportLab + couverture Template 01 inchangés).
- 19.2 Vérifications mécaniques : version v1.2.0 des trois côtés (md + PDF + fiche) ; « en suspens » résiduel absent sur J-M4/Copilot ; batterie M7 re-run **PASS ×2** (rc 0 ×2 — aucune exigence modifiée, idempotence).

### G20 — Publication GitHub bigleon2/KNOWLEDGE (GO + jeton éphémère) — #token 2000
- 20.1 Pré-pousse : `core.fileMode=false` (30 changements de mode 100644→100755 = artefact plateforme, 0 octet de contenu — JAMAIS committés) ; sonde ls-remote (KO-L001) ; recensement exact du delta (fast-forward attendu depuis e6a9595).
- 20.2 Artefacts Serre CBD v1.2.0 → repo/download/ (fiche, CDC, PDF v1.2.0, dossier-conception, rapport-couverture, batterie-tests-serre-cbd/, plan-serre-cbd-consolidation-s-c.md, plan-m4-closure-publication-go.md, analyse-causes-racines-gen-plan.md, plan-cahier-des-charges-v2.0.1.md, audit-gen-plan-v3.23.1.md, eval-campaign-report.json, cover-cdc-serre-cbd.html) ; projection worklog hôte→dépôt (Tasks 21-25, append-only).
- 20.3 Push : credential helper en ligne (jeton **jamais persisté** — ni remote.url, ni config, ni fichier) → vérification distale ls-remote + fetch → commit de journalisation final (tip = commit de journalisation, précédent respecté) → **audit anti-persistance 5 zones** (remote URL, arborescence, git log -S, ~/.git-credentials, historiques shell) → rappel de révocation propriétaire.

### G21 — correct-work (projet, équivalent mécanique) + clôture — #token 1500
- 21.1 Arbitres ×2 + cohérence inter-artefacts (fiche ↔ CDC ↔ PDF ↔ worklog : J-M4 clôturé identique des quatre côtés).
- 21.2 Worklog Task 25 (R5, append-only) ; résumé propriétaire.

## Answer key (hook E1 — décisions vérifiables mécaniquement)

```yaml
decisions:
  - id: "D015"
    criterion: "Le miroir hôte est ré-aligné : gen-plan, correct-work, KNOWLEDGE.md, alias-eco, clone-chat, skills-inventory, @historique byte-identiques au dépôt (×2)"
    verification: "diff -rq ecosysteme-install/repo/skills/gen-plan skills/gen-plan && diff -rq ecosysteme-install/repo/skills/correct-work skills/correct-work && diff -rq ecosysteme-install/repo/skills/KNOWLEDGE.md skills/KNOWLEDGE.md && echo PASS"
    source: "cadrage G17 (correctif RC2 — dépôt = source R4)"
    priority: "S1"
    status: "pending"
  - id: "D016"
    criterion: "cahier-des-charges v2.0.1 restaurée (13 fichiers, SKILL.md ~27 Ko) au miroir hôte ET committée au dépôt"
    verification: "test $(stat -c%s skills/cahier-des-charges/SKILL.md) -gt 25000 && git -C ecosysteme-install/repo log --oneline -1 -- skills/cahier-des-charges/SKILL.md"
    source: "G17.3 (zip canonique download/cahier-des-charges-v2.0.1.zip — trou de synchro résorbé)"
    priority: "S1"
    status: "pending"
  - id: "D017"
    criterion: "Le CDC v1.2.0 clôture J-M4 sans contenu Copilot (statut CLÔTURÉ, décision propriétaire tracée, aucune exigence nouvelle)"
    verification: "grep -c 'CLÔTURÉ' download/cahier-des-charges-serre-cbd.md && grep -c 'v1.2.0' download/cahier-des-charges-serre-cbd.md && ! grep -q 'en suspens.*Copilot' download/cahier-des-charges-serre-cbd.md && echo PASS"
    source: "directive propriétaire 1 (amendement M4 sans Copilot) + G18.1"
    priority: "S1"
    status: "pending"
  - id: "D018"
    criterion: "Aucune exigence EF/ENF modifiée — batterie M7 PASS ×2 (code 0, idempotence)"
    verification: "cd download/batterie-tests-serre-cbd && python3 run_all.py >/dev/null 2>&1 ; echo RC1=$? ; python3 run_all.py >/dev/null 2>&1 ; echo RC2=$?"
    source: "G19.2 (re-validation M3 — A-3 inchangé)"
    priority: "S1"
    status: "pending"
  - id: "D019"
    criterion: "Le PDF v1.2.0 existe, non vide, et porte le titre v1.2.0"
    verification: "test -s download/cahier-des-charges-serre-cbd-v1.2.0.pdf && pdftotext download/cahier-des-charges-serre-cbd-v1.2.0.pdf - 2>/dev/null | grep -c 'v1.2.0'"
    source: "G19.1 (export M3)"
    priority: "S2"
    status: "pending"
  - id: "D020"
    criterion: "La fiche-domaine v1.2.0 statue A-1 clôturé, cohérent avec le CDC"
    verification: "grep -c 'clôtur' download/fiche-domaine-serre-cbd.md && grep -m1 '^> .*v1.2.0' download/fiche-domaine-serre-cbd.md"
    source: "G18.2 (cohérence croisée)"
    priority: "S2"
    status: "pending"
  - id: "D021"
    criterion: "origin/main == main après push (vérification distale) — fast-forward depuis e6a9595"
    verification: "git -C ecosysteme-install/repo ls-remote origin refs/heads/main (SHA == git rev-parse main après push)"
    source: "directive propriétaire 2 (go + jeton) + G20.3"
    priority: "S1"
    status: "pending"
  - id: "D022"
    criterion: "Audit anti-persistance : 0 occurrence du jeton dans remote URL, arborescence, git log -S, ~/.git-credentials, historiques shell"
    verification: "grep -c 'github_pat' ecosysteme-install/repo/.git/config (attendu 0) + balayage zones"
    source: "G20.3 (règle d'or n°4 / A-2 — hygiène jetons)"
    priority: "S1"
    status: "pending"
  - id: "D023"
    criterion: "Le worklog du dépôt porte les entrées de session projetées (Tasks 21-25, append-only)"
    verification: "grep -c 'Task ID: 2[1-5]' ecosysteme-install/repo/worklog.md"
    source: "G20.2 (précédent 6cae154 — projection hôte→dépôt à la publication)"
    priority: "S2"
    status: "pending"
  - id: "D024"
    criterion: "Non-régression R2 : les plans clôturés restent intacts (v2.0.1 + consolidation-s-c)"
    verification: "git -C ecosysteme-install/repo status --porcelain -- download/plan-cahier-des-charges-v2.0.1.md download/plan-serre-cbd-consolidation-s-c.md (aucune modification hors copie ajoutée)"
    source: "R2 (plans clôturés intacts)"
    priority: "S2"
    status: "pending"
```

## Hooks de validation (E8) et règles d'exécution

- Arbitres frais : answer-key-checker **16/16** ×2 · verify-cross **100,0 %** · selftest check_plan_protocol 7/7 ×2 · check_plan_protocol --plan PASS (P1-P5) — à re-jouer en G21 (idempotence ×2).
- Règles : série par défaut · R1-R6 idempotence · R2 non-régression (plans clôturés intacts) · R3 traçabilité worklog · R4 dépôt = source · N3 scripts stdlib · KO-L001 (1 sonde/tour) · règle d'or n°4 (GO + jeton éphémère jamais persisté, audit anti-persistance) · File Output Rule (livrables → download/).
- FAIL à tout hook → pause + correction + re-validation E8 (horodatages couplés).
