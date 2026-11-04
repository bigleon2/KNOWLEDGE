# Plan Task 49 — Règle d'or n°8 « PM INSTALL installe les skills » · renommage `@PM-SKILLS` · rafraîchissement miroirs · test PM INSTALL

Session : web-c30e6506 · Date : 2026-11-04 · Générateur : gen-plan v3.34.0 (mode step — KO-L005 : généré via v3.33.1, re-stampé via v3.34.0 en SG5.3)
Horodatage plan : 2026-11-04T20:35:00+01:00

## Directives verbatim (recensement E1-E2 — règle d'or n°7, intégralité de la discussion)

1. « il a des incohérences dans mon écosystème. exemple pour mon skill "gen-plan", il a : { - mon skill "gen-plan" est à la version "v3.33.1". - PM GEN-PLAN dans "@mon-ecosysteme/" est la version "v3.33.1". - son prompt maitre dans "skills/PM skills/" est à la version "v3.28.1" alors qu'il devrait être aussi à la version "v3.33.1". } »
2. « fais en sorte que ceux soient toujours mes skills (avec le "skill.md") qui soient installés par PM INSTALL et non pas leur prompt maitre dans "PM skills/" qui soient installés (fais en une règle d'or de mon écosystème.) »
3. « renomme le dossier "PM skills/" en "@PM-SKILLS/", puis adapte mon écosystème à ce changement. »
4. « teste PM INSTALL. »

Contexte de mission (messages antérieurs de la session) : installation de l'écosystème sur le profil local (TERMINÉE en préalable — PM-INSTALL v1.8.15 MODE CLONE depuis clone certifié `main` @1e399ff + sync plein-arbre famille TSI/plateforme + `@historique`/`@photos` + rescellement archive v2.2 compat v2.3 ; arbitres : verify-cross **141/141**, integrity **98/98**, 0 dérive) ; mission GHORG/CMDR/MD **REPORTÉE** après Task 49 (directive « avant toute chose »).

## Constats d'état disque (E1-E2 — règle d'or n°5, tous vérifiés mécaniquement)

- `skills/gen-plan/SKILL.md` = v3.33.1 ; `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md` = v3.33.1 ; `skills/PM skills/gen-plan/.source.json` = **v3.28.1 (périmé)** — incohérence confirmée exactement comme décrite.
- `skills/PM skills/` = 348 fichiers, README marqueur D010 (« usage hors écosystème, non lu par l'orchestration, non indexé KB »), généré 2026-10-29 (phase P2, directive 10 tâches, tâche 2), idempotent par SHA-256 scellé (`.source.json` par dossier).
- Incohérence SYSTÉMIQUE (l'exemple gen-plan n'est pas isolé) : index README porte p.ex. `correct-work` v2.8.0 (courant v2.9.0).
- Générateur : `scripts/p2-prompt-maitre.py` — écrit dans `<racine>/skills/PM skills` (`--racine` paramétrable), état `scripts/p2-pm-etat.json`, sources = `skills/*/SKILL.md`, régénère un dossier seulement si le SHA source a changé.
- Références vivantes réelles au dossier : `p2-prompt-maitre.py` (chemins + docstring) et le README du dossier (régénéré). **Faux positifs écartés** (mot « PM » suivi du chemin `skills/@photos/…`) : `task45c-generer-skills-photo.py`, `task48-recalibrage-1944.py`, `skills/KNOWLEDGE.md` — aucune adaptation requise.
- `scripts/p2-etat.json` = journal de la campagne P2 traduction (clés `traitements`/`finition_p2`/`reprise_p2_lots`) — **journal historique d'époque, R2 append-only, NON réécrit** (décision D003).
- `worklog.md` + `download/*.md` mentionnent « PM skills » à titre **historique** — jamais réécrits (R2) ; la Task 49 s'y documente par nouvelles entrées.
- `install-ecosysteme-local.sh` (v1.8.15) : n'installe structurellement jamais `PM skills/` (sources = `$REPO/skills/<skill>/` uniquement) — la règle d'or formalise cette garantie et l'arme mécaniquement (D005).
- Cascade KO-L004 (précédent Task 48, correct-work v2.9.0) : delta verrouillé → `generer-pm-skill.py --generate` (PM mécanique + recalibrage AUTO SHARED §6.1 / PM-INSTALL §2ter+§A.3) → archivage PM précédent `@historique` R4 → pin arbitre (check-ecosysteme-integrity.py L73) + manifeste (seal = exécution sans `--check`) → KB + historiques-par-skill + lignes vives → propagation §0 → ULTRA + README sceaux → rescellement archive → arbitres ×2 → miroir hôte.
- Sémantique versions PM-INSTALL : v1.8.x = recalibrages automatiques ; v1.8.0/v1.9.0 = fonctionnalités (précédent v1.8.0 « mécanisme dual d'installation »).
- KO-L009 : la clé GitHub a été postée dans le canal par le propriétaire (6e exposition) — usage unique éphémère déjà effectué (lecture API `user` → bigleon2), jamais persistée ; **rotation PAT recommandée immédiatement** (guidance réitérée). Aucun push sans GO explicite.

## Groupes d'exécution (mode step — enchaînement séquentiel, correct-work(groupe) après chaque groupe)

### G1 — Règle d'or n°8 dans gen-plan + cascade v3.34.0 [~10 k#token]
- SG1.1 · Tâche 1.1 [À FAIRE] : éditer `skills/gen-plan/SKILL.md` — insérer la **règle d'or n°8** au §1.5 (après n°7, règles contiguës, avant le bloc PATTERN:KO-L009) : *PM INSTALL installe toujours les formes installées `skills/<skill>/` (SKILL.md + ressources) depuis le clone certifié ; les prompts maîtres — corpus `@mon-ecosysteme/` ET miroirs autonomes `@PM-SKILLS/` (ex-« PM skills/ », garde D010) — ne sont jamais installés comme formes installées ; garantie mécanique par garde dans l'installateur* ; monter `version: 3.33.1` → `3.34.0` (MINOR — précédent v3.330) ; entrée changelog v3.34.0 (§11) ; description frontmatter inchangée (non-régression triggers).
- SG1.2 · Tâche 1.2 [À FAIRE] : écrire `scripts/delta-genplan-v3340.json` (history + subs verrouillées : insertion règle n°8 + ligne historique).
- SG1.3 · Tâche 1.3 [À FAIRE] : exécuter `generer-pm-skill.py --generate gen-plan --delta scripts/delta-genplan-v3340.json` → PM v3.34.0 généré mécaniquement + SHARED v1.7.22 + PM-INSTALL v1.8.16 (recalibrage automatique) ; `--check` 4 familles COHERENT rc=0 ; `git mv` PM v3.33.1 → `skills/@historique/prompts-maitres/gen-plan/` (byte-identité R4, SHA consigné).
- SG1.4 · Tâche 1.4 [À FAIRE] : recalibrage — pin `check-ecosysteme-integrity.py` L73 gen-plan `3.33.1`→`3.34.0` (+ commentaire Task 49) ; entrée KB gen-plan v3.34.0 + calibration 2026-11-04 ; `@historique/historiques-par-skill/gen-plan.md` += v3.34.0 ; lignes vives (occurrences `v3.33.1` vivantes → v3.34.0, historiques exclus R2) ; ULTRA régénéré (`gen-ultra-maitre.py`) ; README `@mon-ecosysteme` sceaux §5 + arborescence ; propagation §0 v1.7.22 (`propagate-context.py`).

### G2 — Renommage `@PM-SKILLS` + adaptation écosystème [~7 k#token]
- SG2.1 · Tâche 2.1 [À FAIRE] : `git mv "skills/PM skills" "skills/@PM-SKILLS"` (clone — 348 fichiers, historique git préservé).
- SG2.2 · Tâche 2.2 [À FAIRE] : adapter `scripts/p2-prompt-maitre.py` — `PM_ROOT`/`pm_root` → `skills/@PM-SKILLS`, docstring (« sauvegardés UNIQUEMENT dans `skills/@PM-SKILLS/` »), titre README index `# « @PM-SKILLS » — …` ; `--seulement` et `--racine` inchangés.
- SG2.3 · Tâche 2.3 [À FAIRE] : PM-INSTALL **v1.9.0** (fonctionnalité) — codifier la règle d'or n°8 : note §2 (étape d'installation = formes installées uniquement) + contrôle §3.5 « Aucun PM installé comme forme installée » (garde D010 + règle d'or n°8) + renommage `@PM-SKILLS` dans §2bis/§2ter/§A le cas échéant + entrée §7 v1.9.0.
- SG2.4 · Tâche 2.4 [À FAIRE] : garde mécanique dans `install-ecosysteme-local.sh` — bloc final « Règle d'or n°8 » : scan `skills/*/` (hors `@mon-ecosysteme`, `@PM-SKILLS`, `@historique`, `@photos`) → **0** fichier `PROMPT-MAITRE-*` ET 0 dossier `PM skills`/`@PM-SKILLS` déployé sur le profil ; FAIL → exit 1.

### G3 — Rafraîchissement miroirs périmés [~4 k#token]
- SG3.1 · Tâche 3.1 [À FAIRE] : `p2-prompt-maitre.py --racine <clone>` — régénération idempotente (uniquement les dossiers dont le SHA source a changé depuis le 2026-10-29 : gen-plan v3.34.0, correct-work v2.9.0, etc.) ; index README régénéré ; re-jeu ×2 = no-op ; vérifier `.source.json` gen-plan = version 3.34.0.

### G4 — Rescellement + tests PM INSTALL + arbitres [~9 k#token]
- SG4.1 · Tâche 4.1 [À FAIRE] : miroir dépôt→profil des fichiers modifiés (corpus, gen-plan, SHARED, PM-INSTALL, KB, scripts, @historique, @PM-SKILLS non déployé — reste dépôt-seul) puis rescellement archive profil (`task21-f2-rebuild-archive.py`) + manifeste scellé (`check-ecosysteme-integrity.py` sans `--check`).
- SG4.2 · Tâche 4.2 [À FAIRE] : **test PM INSTALL ×2** (MODE CLONE) — 2e exécution = no-op idempotent (0 réécriture, piliers OK) ; garde règle d'or n°8 PASS ; `@PM-SKILLS` jamais déployé sur le profil (absence vérifiée).
- SG4.3 · Tâche 4.3 [À FAIRE] : arbitres ×2 — verify-cross **141/141**, integrity **98/98**, coherence (baseline 51 PASS/23 WARN/0 FAIL préservée), garde-plans PASS, doublons download/ 0.

### G5 — Worklog + commit local + KO-L005 [~5 k#token]
- SG5.1 · Tâche 5.1 [À FAIRE] : entrée worklog Task 49 (directives verbatim, décisions D001-D007, preuves mécaniques, statuts plan, PLAN-AFFICHE) + append des verdicts correct-work(groupe) G1→G4.
- SG5.2 · Tâche 5.2 [À FAIRE] : commit local clone, message conventionnel « Task 49 — … » ; **PUSH = GO propriétaire uniquement (KO-L009 point 5)** — aucun push effectué.
- SG5.3 · Tâche 5.3 [À FAIRE] : KO-L005 — re-stamp du présent plan via gen-plan v3.34.0 (horodatages couplés + verdict E8 re-validé) + bloc récapitulatif final au chat + rapport final.

**Budget total estimé : ~35 k#token** (G1 10 k · G2 7 k · G3 4 k · G4 9 k · G5 5 k) + contingence reprise ×2-3 (règle d'or n°1).

## Answer key (décisions D001-D007 — criterion + verification exécutable)

- **D001** — gen-plan **v3.34.0** (MINOR — ajout règle d'or n°8 ; précédent v3.33.0 règle n°7)
  - criterion: frontmatter `version: 3.34.0` + PM corpus v3.34.0 généré MÉCANIQUEMENT (zéro rédaction manuelle du PM)
  - verification: `rg -m1 '^version:' skills/gen-plan/SKILL.md` → 3.34.0 ; PM corpus `PROMPT-MAITRE-GEN-PLAN-v3.34.0.md` présent ; `generer-pm-skill.py --check` rc=0
- **D002** — PM-INSTALL **v1.9.0** (fonctionnalité : règle d'or n°8 codifiée + @PM-SKILLS) APRÈS v1.8.16 (auto-recalibrage cascade)
  - criterion: §7 porte v1.8.16 (auto) PUIS v1.9.0 (règle d'or n°8 + renommage) ; contrôle §3.5 ajouté
  - verification: `rg 'v1\.9\.0' skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` ; garde §3.5 présente
- **D003** — `p2-etat.json` **NON réécrit** (journal historique campagne P2 close — R2 append-only ; chemins d'époque)
  - criterion: SHA-256 identique avant/après
  - verification: `sha256sum scripts/p2-etat.json` avant == après
- **D004** — SHARED **v1.7.22** par recalibrage AUTOMATIQUE uniquement (§6.1 instantané gen-plan v3.34.0) — aucune édition manuelle
  - criterion: §6.1 porte gen-plan v3.34.0 ; §7 entrée v1.7.22 auto
  - verification: `rg 'v1\.7\.22' skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md`
- **D005** — Garde mécanique règle d'or n°8 dans l'installateur (scan post-install : 0 `PROMPT-MAITRE-*` hors corpus autorisés ; 0 déploiement `@PM-SKILLS`)
  - criterion: installateur contient le bloc garde + le test le déclenche PASS
  - verification: 2 exécutions `install-ecosysteme-local.sh` → garde PASS ×2 ; `ls skills/ | grep -c PM` → 0
- **D006** — Rafraîchissement miroirs par GÉNÉRATEUR idempotent (jamais d'édition manuelle des miroirs)
  - criterion: `.source.json` gen-plan = version 3.34.0 + sha_source = SHA SKILL.md v3.34.0 ; re-jeu ×2 no-op
  - verification: `cat "skills/@PM-SKILLS/gen-plan/.source.json"` ; 2e exécution générateur = 0 GENERE
- **D007** — **Aucun push** sans GO propriétaire (KO-L009 point 5) — commits locaux seulement
  - criterion: 0 push effectué ; branche locale en avance constatée
  - verification: `git status` clone : commits non poussés, rapport final le documente

## Statuts (état disque — règle d'or n°5, mis à jour à chaque groupe)

- G1 [TERMINÉ 4/4 SG] · G2 [TERMINÉ 4/4 SG] · G3 [TERMINÉ 1/1 SG] · G4 [TERMINÉ 3/3 SG] · G5 [EN COURS 1/3 SG — worklog ✓]

---

Verdict E8 : PASS (P1-P5 exécutés via `skills/gen-plan/scripts/check_plan_protocol.py` — 5/5 checks : plan présent, answer key 7 décisions vérifiables, worklog R5 cite le plan, PLAN-AFFICHE dans l'entrée, verdict + horodatages couplés — Horodatage vérifié : 2026-11-04T20:35:00+01:00)
