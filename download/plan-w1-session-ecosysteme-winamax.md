# PLAN D'ACTIONS W1 — session web-59ca44d5 — re-généré via gen-plan v3.23.1 (règle d'or n°2)

> **Version du plan** : W1 | **Généré le** : 2026-10-16 | **Mode** : M1 (Planification) → exécution suite immédiate
> **Provenance** : re-génération conforme à la **règle d'or n°2 §1.5 + KO-L005** — écosystème réinstallé et certifié (worklog local Task 1 : arbitres 3/3 verts, verify-cross 96/96, verify-correct-work 16/16, integrity 68/68) → plan d'actions actuel re-généré via **gen-plan v3.23.1** installée (source : corpus @mon-ecosysteme, commit épinglé bc387a0, règle d'or n°4 du PM-INSTALL v1.7.1). Objectif final inchangé, **R2** : étapes A0-A1/W0 terminées conservées telles quelles (jamais réécriture destructrice).
> **Demandes intégrées** (règle d'or n°3 — E13) : (1) « réinstalle mon écosystème personnel » ; (2) « installe via PROMPT-MAITRE-INSTALL-ECOSYSTEME.md @ bc387a0 » ; (3) « utilise cette clé PAT GitHub » ; (4) « gen-plan : continue » ; (5) « gen-plan : génère à nouveau le plan d'actions actuel » ; (6) « génère à nouveau aussi le plan d'actions de la discussion partagée ».
> **Clause mode NULL (v3.22.1)** : invocations `gen-plan : <instructions>` sans mode explicite → exécution classique du plan, sans portes de confirmation.
> **Auto-suffisance** : ce plan est auto-portant — tout tour peut reprendre sans contexte hérité (bloc REPRISE en fin de plan).

---

## E1 — Analyse de la demande (hook answer key)

| Objet | Contenu | Traçabilité |
|-------|---------|-------------|
| (a) Tâche A — réinstallation écosystème | Installation via **PM-INSTALL v1.7.1** (pipeline 11 étapes), dépôt `bigleon2/KNOWLEDGE` **commit épinglé bc387a0** (règle d'or n°4 : cloner localement) | worklog local **Task 1** — ✅ FAITE et certifiée (étapes 0-10, 3/3 arbitres verts) |
| (b) PAT GitHub | Clé fine-grained fournie par le propriétaire — authentification des opérations git restantes (publication/push d'archive) — **déjà configurée sur origin du clone** (vérifiée `git ls-remote`, worklog Task 1) ; **jamais persistée dans un fichier** (anti-persistance Task 8/14) | directive propriétaire (message 3) |
| (c) Tâche B — gen-plan : « continue » | Reprise du travail de la discussion partagée `28b4adb7` : **fiches PDF Winamax VPIP/PFR/AF** — plan d'exécution opérationnel re-généré : **plan W2** | discussion 28b4adb7 (capture agent-browser) ; `download/plan-w2-discussion-28b4adb7-winamax.md` |
| (d) Demande — régénérations | « gen-plan : génère à nouveau le plan d'actions actuel » (règle d'or n°2/KO-L005) **+ « génère à nouveau le plan d'actions de la discussion partagée »** → deux plans : **W1 (ce document)** et **W2** | directives propriétaires (messages 4-5) — ✅ W0 FAITE (ce tour) |
| (e) Objectif final | Tâche A certifiée ✅ → Tâche B livrée (fiches PDF Winamax dans `download/`) → clôture de session : étape 11 PM-INSTALL (clone-chat archivage) | directive maîtresse de session |

Décisions vérifiables : D-W1-1 (Tâche A certifiée — rapport `scripts/rapport-installation-ecosysteme.json` verdict PASS) ; D-W1-2 (PAT sur origin — `git remote get-url origin` avec jeton, non persisté ailleurs) ; D-W1-3 (plans W1/W2 régénérés via v3.23.1 — présents dans `download/`) ; D-W1-4 (cahier des charges Winamax épinglé dans la discussion source — aucune re-clarification requise).

## E2 — Inventaire des ressources

- **Écosystème local certifié (Task 1)** : corpus `skills/@mon-ecosysteme/` **9/9 byte-identique** ; familles d'instantané §2ter — **gen-plan 3.23.1**, **correct-work 2.7.0**, **clone-chat 2.0.1**, **refactor-guard 1.7.0** ; registre KB `skills/KNOWLEDGE.md` (350 L, 26 entrées) ; outillage **68 scripts** ; archive scellée `download/mon-ecosysteme_archive.zip` (round-trip 9/9 PASS, 0 doublon download/).
- **Certification étape 9** : verify-cross 96/96 · verify-correct-work 16/16 · integrity 68/68 (manifeste `scripts/ecosysteme-integrity.json`) ; rapport `scripts/rapport-installation-ecosysteme.json` (PASS).
- **Clone local** : `/home/z/my-project/KNOWLEDGE` (HEAD **bc387a0** — Task 12-CORRECTIONS, batterie 100 % verte d'origine) ; origin authentifié PAT.
- **Artefacts de session** : `upload/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` (référence d'installation) ; `upload/shared_chat.json` + `upload/discussion-28b4adb7-texte.txt` (captures de la discussion partagée) ; `download/plan-w2-discussion-28b4adb7-winamax.md` (plan d'exécution Tâche B).
- **Restes Tâche A** : étape **11** (clôture : clone-chat archivage session + mise à jour KNOWLEDGE.md si nouveau skill — 8 checks S1-S8) — différée par Task 1 à la fin de session ; **publication archive via PAT** (push) — à exécuter (A2).
- **Tâche B** : cahier des charges verrouillé (30+ pages, intermédiaire, cash game + tournoi, bleu nuit + cyan, corrigés, HUD simulés, 4 modules, 5 exemples, 10 exercices) — plan W2 E1(b).

## E3 — Classification

**Type 4** (orchestration/locale) pour A2 (publication git) et A3 (clôture clone-chat) ; **Type 1** (création de document PDF) pour la Tâche B via plan W2. Aucun développement web.

## E4 — Estimation #token

| Phase | Objet | Estimation |
|-------|-------|-----------|
| A0-A1 | ✅ FAITES (Task 1) — réinstallation PM-INSTALL v1.7.1 étapes 0-10 + certification | 0 (restant) |
| W0 | ✅ FAITE (ce tour) — régénérations W1 + W2 via gen-plan v3.23.1 | ~1500 #token (consommé) |
| A2 | Publication archive + rapport via PAT (push vers bigleon2/KNOWLEDGE) + worklog | ~3000 #token |
| B1-B7 | Tâche B — exécution du plan W2 (outline, HTML 30+ pages, validation, conversion, QA, livraison) | ~17500 #token (détail : plan W2 §E4) |
| A3 | Clôture de session — étape 11 PM-INSTALL : clone-chat (8 checks S1-S8) + worklog final | ~3000 #token |
| Maintenance | worklog par tour | ~500 #token/tour |

## E5 — Sélection des skills

| Skill | Usage | Version plancher |
|-------|-------|-----------------|
| gen-plan | Méthode E1-E15, règles d'or n°1-4, clause mode NULL | 3.23.1 |
| correct-work | Hooks par phase (E8 final + mode CIBLE sur livrables) | 2.7.0 |
| clone-chat | Étape 11 — archivage de session (7+1 étapes, 8 checks S1-S8) | 2.0.1 |
| pdf (plateforme) | Tâche B — génération fiches PDF (plan W2 E5) | courante |
| agent-browser (plateforme) | Re-capture SPA de la discussion si re-vérification nécessaire | courante |
| resource-monitor | G-RES — collectes R-RES1 en continu | 1.0.0 |
| Git + PAT | Publication (push) — jeton non persisté hors origin | — |

## E6 — Profilage ressource

**NORMAL** — signaux de pression : aucun (disque OK, 0 timeout consécutif, budget < 80 %). **G-RES active** : collecte à l'ouverture/fermeture de chaque phase (R-RES1) ; adaptation en cascade au blocage (R-RES3) ; mise à jour optimisée du plan via gen-plan si dérive structurelle (R-RES4) ; objectif final intangible (R-RES5).

---

## E7 — LE PLAN (phases restantes)

> Philosophie : exécution série par défaut (§1.4 #4). Toute phase terminée → hook correct-work (§5.4). Idempotence R1-R6 sur chaque écriture. G-RES sur toutes les phases. Clause mode NULL : exécution sans portes de confirmation.

### A0-A1 — ✅ FAITES (Task 1)

- A0 lecture PM-INSTALL v1.7.1 + SHARED v1.7.7 ; règle d'or n°4 : clone bc387a0 ; PAT configuré sur origin (non persisté).
- A1 pipeline étapes 0-10 exécuté et certifié : corpus 9/9, familles gen-plan 3.23.1 / correct-work 2.7.0 / clone-chat 2.0.1 / refactor-guard 1.7.0, registre KB 26 entrées, 68 scripts, archive scellée round-trip 9/9, arbitres 3/3 verts (96/96, 16/16, 68/68), rapport PASS.

### W0 — ✅ FAITE (ce tour)

- W0 régénérations demandées : **plan W1** (session, ce document) + **plan W2** (discussion 28b4adb7, fiches Winamax) — via gen-plan v3.23.1, format canonique E1-E8 + bloc REPRISE, journalisées au worklog (Task 2).

### A2 — Publication archive via PAT — ⏳ À FAIRE

1. Pré-flight : collecte G-RES + vérification état git du clone (propre, HEAD bc387a0) + vérification accès distant (PAT, `git ls-remote`).
2. Déposer dans le clone les livrables de session à publier : `download/mon-ecosysteme_archive.zip` (archive d'intégrité scellée), `scripts/rapport-installation-ecosysteme.json`, plans W1/W2 (`download/plan-w1-session-ecosysteme-winamax.md`, `download/plan-w2-discussion-28b4adb7-winamax.md`).
3. Commit descriptif (convention dépôt) + push origin avec PAT configuré ; vérification post-push (`git log`, `git status`).
4. En cas de refus distant (permissions fine-grained manquantes) : reporter le verdict exact + conserver les livrables locaux (règle d'or n°1 — adaptation, jamais un arrêt).
5. Worklog : journaliser la publication (traces commit/push).

### B1-B7 — Tâche B : fiches PDF Winamax (plan W2) — ⏳ À FAIRE

- Exécution intégrale du **plan W2** (plan d'exécution opérationnel de la discussion 28b4adb7) : T3 outline détaillé → T4 HTML complet Template 07 « Crystal Blue » (30+ pages, HUD simulés, 4 modules, 5 exemples, 10 exercices corrigés) → T5 `poster_validate.py check-html` → T6 conversion `html2pdf-next.js` + QA `pdf_qa.py` → T7 numérotation pypdf + métadonnées + livraison `download/` + worklog.
- Cahier des charges déjà épinglé (discussion source) : aucune re-clarification — exécution directe.
- Statuts reportés dans W1 à chaque phase terminée (R2 : jamais de réécriture destructrice).

### A3 — Clôture de session (étape 11 PM-INSTALL) — ⏳ À FAIRE (fin de session)

1. Pré-requis : A2 ✅ et B1-B7 ✅ (livrables finalisés).
2. Exécuter clone-chat v2.0.1 (7+1 étapes, mode CIBLE, Context Drift §3.5) : clone intégral de la session courante — contexte, décisions, artefacts, worklog Tasks 1-N, plans W1/W2, directives (traces), nom descriptif du clone.
3. Vérification : 8 checks S1-S8 clone-chat PASS ; idempotence.
4. Mise à jour KNOWLEDGE.md si nouveau skill installé (aucun prévu — no-op attendu).
5. Worklog final : section de clôture + verdict Global de session.

---

## E8 — Validation du plan

- **W0** : validation mécanique — deux plans présents dans `download/` (W1, W2), format canonique E1-E8 + bloc REPRISE, journalisés au worklog Task 2 (règle d'or n°2/KO-L005).
- **A2** : publication vérifiée — push confirmé (`git log` distant) ou verdict d'incident documenté (règle d'or n°1).
- **B1-B7** : livrable vérifié — `poster_validate` PASS, `pdf_qa` PASS, PDF numéroté + métadonnées, fichier dans `download/`, worklog journalisé ; correct-work(mode CIBLE) final PASS.
- **A3** : clone-chat 8/8 checks S1-S8 PASS, clone scellé et idempotent.
- **Hook correct-work** : exécuté après chaque phase terminée (A2, B1-B7, A3) — verdicts PASS requis avant phase suivante.

## Bloc REPRISE W1 (auto-suffisant)

Au prochain « continue » (ordre de priorité, clause mode NULL — sans portes de confirmation) :
1. **A2** — publication archive + rapport + plans via PAT (pré-flight G-RES → dépôt dans clone → commit → push → vérification → worklog).
2. **B1-B7** — exécuter le plan W2 (T3 outline → T4 HTML → T5 validate → T6 convert+QA → T7 livraison) : fiches PDF Winamax VPIP/PFR/AF.
3. **A3** — clôture : clone-chat (8 checks) + worklog final + verdict Global.
4. Statuts maintenus dans ce plan (R2) ; toute nouvelle demande utilisateur → mise à jour E13 (règle d'or n°3) ; toute dérive structurelle → re-génération via gen-plan v3.23.1 (règle d'or n°2/KO-L005).
