# CLONE DE DISCUSSION — Installation de l'écosystème personnel + plan d'actions d'audit (bug gen-plan v3.24.0)

> **Date du clone** : 2026-10-25
> **Source** : Discussion entre le propriétaire (bigleon2) et l'assistant (Z.ai — session web-eb6c8580)
> **Sessions couvertes** : 1 session (du 2026-10-25 au 2026-10-25)
> **Version clone-chat** : 2.0.1

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : profil local `/home/z/my-project` (assistanat IA, écosystème Knowledge installé) — `{{SKILLS_ROOT}}=skills/`, `{{KB_PATH}}=skills/KNOWLEDGE.md`, registre KB 33 entrées, corpus `skills/@mon-ecosysteme/` (9 fichiers), outillage `scripts/` (100 entrées), archive d'intégrité `download/mon-ecosysteme_archive.zip` (v2.3 — 9 corpus + 6 piliers, round-trip byte-identité).

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.0 Héritage — chaîne de clonage (1 session, 2026-10-25)

La lignée de clones cumule 0 session avant le présent document (premier clone de ce profil local — l'historique canonique pré-b75a620 vit dans `skills/@historique/` et le §7 des PMs, jamais dans les clones).
La présente session ajoute 4 entrées worklog (Tasks 1-4). L'état de l'écosystème à l'ouverture était : profil local SANS écosystème (skills plateforme seulement, pas de corpus, pas de gen-plan, pas de registre KB).

### §1.1 Résumé global

La session a installé l'écosystème personnel du propriétaire (dépôt GitHub bigleon2/KNOWLEDGE @ b75a62066791a8cce8c1ec5d1dbe7d976bae4244) sur le profil local, en suivant le pipeline PROMPT-MAITRE-INSTALL-ECOSYSTEME.md v1.7.1 (11 étapes). L'installation a été certifiée 6/6 arbitres verts (PASS AVEC RÉSERVES — 1 avertissement documenté), puis le skill gen-plan v3.23.1 fraîchement installé a généré le plan d'actions de la tâche d'audit demandée : « audit complet de l'écosystème, incluant un test pour comprendre le bug GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 ». Trois incidents d'installation ont été résolus par contournement conforme (règle d'or n°1 §3.4) et journalisés. Le plan d'audit est PRÊT, en attente de directive d'exécution.

### §1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | 2026-10-25 | Installation écosystème (étapes 0-10) + certification + plan d'actions d'audit | `skills/@mon-ecosysteme/` (corpus 9) + 33 skills écosystème + `skills/KNOWLEDGE.md` + `scripts/` (100) + `download/mon-ecosysteme_archive.zip` (v2.3) + `download/plan-task1-installation-ecosysteme.md` + `download/rapport-correct-work-projet-installation-2026-10-25.md` + `download/plan-task2-audit-ecosysteme.md` + `worklog.md` (Tasks 1-4) + présent clone |

### §1.3 Détail par session

**Session 1 (2026-10-25)** — une seule session, deux phases :
- **Phase installation** : directive propriétaire en deux étapes ordonnées. Étape 0 : lecture SHARED v1.7.7 + PM-INSTALL v1.7.1. Étapes 1-8 : corpus (9 fichiers) + @historique + 33 skills écosystème (4 familles version-matched aux PMs : gen-plan v3.23.1, correct-work v2.7.0, clone-chat v2.0.1, refactor-guard v1.7.0 — garde R2) + registre KB + outillage. Étape 2/10 : archive d'intégrité v2.3 rescellée (15 entrées). Étape 9 : verify-cross 99/99 ; correct-work Mode PROJET (plan via gen-plan — couplage §1.5) → rapport PASS AVEC RÉSERVES ; intégrité 70/70 ; certification consolidée 6/6. Étape 10 : 0 doublon download/. Incident critique écarté : bug « gen-plan v3.24.0 » NON reproductible à b75a620 (v3.23.1 = plus récent — dérivation KO-L003) → délégué au plan d'audit.
- **Phase planification (gen-plan v3.23.1, règle d'or n°2)** : plan d'actions de l'audit — answer key D001-D010, Phases A-D, hooks correct-work par phase, test du bug en sandbox (blast radius gen-plan CRITIQUE : 17 amont / 22 aval), discrimination d'hypothèses H1/H2/H3, zéro-régression R2/R4.

---

## §2 — ÉCOSYSTÈME DE SKILLS

### §2.1 Skills créés ou modifiés

Aucun skill créé. 33 skills écosystème **installés** (état certifié b75a620 — versions ECO_SKILLS exactes, registre `skills/KNOWLEDGE.md` = source de vérité). Skills **modifiés** (2, correction S3 — marqueurs §0 alignés sur SHARED v1.7.7, extrait byte-identique au corpus) :

#### alias-eco (skill plateforme)
- **Description** : gestionnaire du système d'alias $<ALIAS> de l'écosystème Knowledge (registre @historique/@Alias/ du dépôt KNOWLEDGE).
- **Modification** : en-tête §0 « SHARED v1.7.10 » → « SHARED v1.7.7 » (ligne 31) — résorption STALE arbitre interactions 11c ; lignée post-b75a620 documentée au worklog Task 1.

#### cahier-des-charges (skill plateforme)
- **Description** : conception de cahiers des charges (12 sections, EF/ENF, jalons, critères d'acceptation mécaniques).
- **Modification** : en-tête §0 « SHARED v1.7.8 » → « SHARED v1.7.7 » (ligne 36) — même correction S3.

### §2.2 Scripts créés ou modifiés

#### install-ecosysteme-session.sh (créé — script de session, conventions script-creator)
- **Description** : matérialisation des étapes 1-8 du PM-INSTALL v1.7.1 (corpus, 33 skills, registre, outillage) depuis .staging vers le profil local.
- **Chemin** : `scripts/install-ecosysteme-session.sh` (~1,5 Ko)

100 scripts **installés** depuis le dépôt (arbitres, certification-complete.py, réinstallateur install-ecosysteme-local.sh, generer-pm-skill.py, refactoring-test-graph.py, G-RES — pas créés).

### §2.3 Artefacts produits

| Fichier | Taille | Description |
|---------|--------|-------------|
| `download/mon-ecosysteme_archive.zip` | 174 Ko | Archive d'intégrité v2.3 — 9 corpus + 6 piliers, round-trip byte-identité (véhicule unique de diffusion du corpus) |
| `download/plan-task1-installation-ecosysteme.md` | ~4 Ko | Plan d'actions Task 1 (gen-plan v3.23.1 — couplage correct-work §1.5) : answer key D001-D009, E1-E15 |
| `download/rapport-correct-work-projet-installation-2026-10-25.md` | ~4 Ko | Rapport correct-work Mode PROJET — verdict PASS AVEC RÉSERVES (2 drifts hérités findings) |
| `download/plan-task2-audit-ecosysteme.md` | ~6 Ko | **Plan d'actions de l'audit** (gen-plan v3.23.1) : answer key D001-D010, Phases A-D, protocole test du bug v3.24.0 — PRÊT, exécution en attente |
| `worklog.md` | ~6 Ko | Journal de session — Tasks 1-4 (installation, certification, planification, clôture) |
| `download/clone-discussion-2026-10-25-…md` | présent fichier | Clone de session (étape 11 — archivage auto-suffisant) |

### §2.4 Historique des interactions

| Ordre | Interaction | Résultat |
|-------|-------------|----------|
| 1 | garde É1-INSTALL (gen-plan §1.16) → ensure-installed.py --check | rc=0 INSTALLE (33 entrées KB) |
| 2 | gen-plan v3.23.1 —invoque→ correct-work v2.7.0 (§1.5, E8 hook) | Mode PROJET : PASS AVEC RÉSERVES |
| 3 | correct-work —utilise→ gen-plan (plan de vérification Étape 1) | plan-task1 (couplage respecté) |
| 4 | gen-plan —garde-fous→ refactor-guard (n°55) | blast radius CRITIQUE → sandbox désigné pour le test v3.24.0 |
| 5 | gen-plan —utilise→ clone-chat (E15/étape 11) | présent clone |
| 6 | arbitres (verify-cross, verify-correct-work, intégrité, interactions, routage, answer-key-checker) | 6/6 verts + 16/16 — certification PASS AVEC RÉSERVES |

---

## §3 — DÉCISIONS CLÉS

### §3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | Installer l'écosystème personnel depuis le fichier PROMPT-MAITRE-INSTALL-ECOSYSTEME.md du dépôt @ b75a620 | Le profil local ne portait pas l'écosystème (skills plateforme seulement) | Pipeline PM-INSTALL v1.7.1 exécuté — écosystème installé et certifié 6/6 |
| 2 | Une fois l'installation terminée, mobiliser gen-plan fraîchement installé pour générer le plan d'actions de l'audit | gen-plan v3.23.1 doit planifier « audit complet + test du bug v3.24.0 » | Plan Task 2 créé (règle d'or n°2) — 4 phases, answer key D001-D010, PRÊT à exécuter |

### §3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | Archive d'intégrité absente (étape 2 impossible) | `*.zip` gitignoré — l'archive n'est jamais commitée | Rescellage v2.3 via task-f5-seal-archive-v23.py (règle d'or n°1 §3.4) | 15 entrées, round-trip ✓ |
| 2 | Garde anti-doublons FAIL (1/70) | Placeholder plateforme download/README.md en collision nominale avec le corpus README.md | Suppression du placeholder (état canonique) | 70/70 PASS |
| 3 | Arbitre interactions FAIL (STALE 11c) | Skills plateforme alias-eco/cahier-des-charges portaient SHARED v1.7.10/v1.7.8 (lignée post-b75a620) ≠ v1.7.7 installé | Marqueurs §0 alignés v1.7.7 (extrait identique) | PASS AVEC RÉSERVES 0 FAIL |
| 4 (ouvert) | « GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 » | Non reproductible à b75a620 (v3.23.1 = plus récent) — hypotheses H1 génération PM/H2 dérive sans PM/H3 routage déclencheur | Délégué au plan d'audit Phase C (sandbox, D003-D007) | EN ATTENTE D'EXÉCUTION |

### §3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| Périmètre d'installation | Écosystème = corpus + @historique + 33 ECO_SKILLS + KB + scripts + archive ; skills plateforme hors périmètre certifiable | alias-eco/cahier-des-charges conservés, marqueurs §0 seuls modifiés |
| Download/ de session | Rapports de l'auteur non importés (livrables ≠ composants) ; le rapport correct-work de la session est généré par la session | rapport-correct-work-projet-installation-2026-10-25.md |

### §3.4 Données de calibration

#token (grille gen-plan §4 — exécution complexe 4+ skills 10-20 k) : session ~30 k au total (installation ~22 k + certification/planification ~5 k + clôture ~3 k) ; plan d'audit estimé ~13,1 k (planification 2,6 k consommée + exécution 10,5 k en attente). Profil NORMAL (G-RES OK). Auto-calibration E15 à l'exécution de l'audit.

### §3.5 Évolutions de contexte (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | ENRICHISSEMENT | Directive = installation seule | Directive = installation PUIS plan d'actions d'audit via gen-plan fraîchement installé | 1 | Task 1 (directive) | demande propriétaire ordonnée en 2 étapes |
| 2 | CORRECTION | download/ contenait README.md (placeholder plateforme) | download/ sans README (état canonique, garde v2.2) | 1 | Task 1 (incident 2) | garde anti-doublons — collision nominale corpus |
| 3 | CORRECTION | alias-eco §0 = SHARED v1.7.10 ; cahier-des-charges §0 = SHARED v1.7.8 | les deux §0 = SHARED v1.7.7 (installé) | 1 | Task 1 (incident 3) | arbitre interactions 11c STALE → dérive résorbée |

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire

1. Lire §0 (Règle zéro) — tout est à reconstruire
2. Reconstruire l'état : exécuter `python3 skills/gen-plan/scripts/ensure-installed.py --check` (rc=0 attendu — si rc≠0 : PRÉEMPTION É1-INSTALL, réinstallation via `--reinstall` AVANT toute autre étape)
3. Appliquer les décisions et conventions de §3
4. Poursuivre au point d'arrêt : **exécution du plan d'audit** `download/plan-task2-audit-ecosysteme.md` (Phases A-D, hooks correct-work par phase — sur directive propriétaire uniquement)

### Fichiers à reconstruire en priorité

1. **`skills/@mon-ecosysteme/` + archive** — via ensure-installed --reinstall si dérive (le corpus est la source de vérité restaurable)
2. **`download/plan-task2-audit-ecosysteme.md`** — le travail en cours (plan d'audit PRÊT : Phase A structurel → B drifts → C test bug v3.24.0 sandbox → D rapports)
3. **`worklog.md`** — journal append-only (l'état fait foi, B-11)

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra :
   - Tout le contexte de ce clone (discussion originale)
   - Tout le nouveau contexte de la discussion en cours
3. Le nouveau clone remplace ce fichier
4. Le clone « grandit » à chaque session sans perdre l'historique

**Mécanisme** : les sections §1-§3 (incluant §3.5 Context Drift) sont enrichies avec les nouvelles sessions. Les sections §0, §4-§5 sont régénérées à l'identique (auto-référentielles).
