# CLONE DE DISCUSSION — Écosystème Knowledge : idempotence par élément, routage dédié, installation minimale, francisation, publication

> **Date du clone** : 2026-10-04
> **Source** : Discussion entre le Propriétaire (bigleon2) et l'Assistant (Super Z / GLM, gen-plan v3.18.0 → v3.19.0)
> **Sessions couvertes** : 11 sessions worklog racine (Tasks 22, 22-b2, 23, 24 détaillées ; lignée antérieure héritée)
> **Version clone-chat** : 2.0.0

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : écosystème personnel « Knowledge » installé localement à
`/home/z/my-project/ecosystem` (dépôt git `KNOWLEDGE`, remote `github.com/bigleon2/KNOWLEDGE`,
branche `main`). Racine de session : `/home/z/my-project/` (worklogs, `scripts/`, `download/`).
Skills root : `ecosystem/skills/` · Registre KB : `ecosystem/skills/KNOWLEDGE.md` (27 entrées
skills + décisions) · Corpus : 27 skills + familles PM `@mon-ecosysteme/` (ULTRA, SHARED v1.6.4,
gen-plan corpus, INSTALL, CORRECT-WORK, CLONE-CHAT) · Profil ressource : NORMAL · Conventions :
kebab-case, semver, tags neutres, dépendances YAML, cross-references bidirectionnelles,
arbitres de certification ×6, worklog format SHARED §1.4 (sections séparées par `---`).

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.0 Héritage — chaîne de clonage

La lignée de clones cumule les sessions Tasks 0 → 21 avant le présent document (détail aux §1.0
des prédécesseurs : `download/clone-discussion-2026-09-27-ecosysteme-knowledge-b13-r7.md` et
successeurs `-b/-c/-d/-e`, `@mon-ecosysteme/clone-discussion-2026-09-27-...-b13-r7-f.md`,
`download/clone-session-task19-analyse-triggers-2026-10-03.md`). L'état de départ connu de la
présente discussion : écosystème certifié 6/6 arbitres, Tasks 18-21 closes, push armé sans jeton.

### §1.1 Résumé global

La discussion porte sur la **fiabilisation et la publication de l'écosystème Knowledge**. Le
propriétaire exige d'abord la preuve d'idempotence **par élément** (octets, M0/M1/M2) de toute
modification non-skill avant tout push (Task 22-b2) ; puis l'automatisation du **routage des
outils dédiés**, d'une **installation minimale** économe en disque, de l'**auto-réinstallation**
et de la **francisation idempotente** du corpus (Task 23) ; enfin une séquence de clôture
ordonnée : re-certification → correct-work PROJET → clone-chat → push avec jeton fourni
(Task 24). La complexité croît du point de vue protocolaire : chaque faille trouvée (auto-
observation d'arbitre, artefact d'invocation N2, dates horloges) est corrigée **à la source**
(KO-L003 : jamais ajuster la réalité au verdict). L'état final : 107/107 éléments non-skill au
point-fixe, 6/6 arbitres verts, 3 commits Task 22 + 1 commit Task 23 + couche Task 24 poussés
sur GitHub en 2 pushes (pattern B5).

### §1.2 Table des sessions

| # | Task ID | Thème | Livrables principaux |
|---|---------|-------|---------------------|
| 1 | 0 | Amorçage écosystème | structure, corpus initial |
| 2 | 1-3 | Phases d'exécution fondatrices | corpus skills v1 |
| 3 | 18-a | correct-work PROJET + levée confirm LLM | 42/42 votes réels |
| 4 | 18-b | Baselines hors périmètre (c) | memory-engineering v1.1.0 |
| 5 | 19 | Push + clone-chat + analyse incohérences + déclencheurs | clone task19, rapport triggers |
| 6 | 20 | Mode tâches en parallèle | installation locale ∥ plan d'extension |
| 7 | 21 | correct-work → gen-plan parallèle → correct-work final | campagnes, rapports task21 |
| 8 | **22** | Installation + idempotence skills/agents + routage outils dédiés | commit `9afc540`, arbitre check-tool-routing (D006), 15/15 PASS |
| 9 | **22-b2** | Idempotence PAR ÉLÉMENT des non-skill (MD/PY/JSON/PDF) | commits `bdf3d59`, `a7ca9de`, protocole B2, 36/36 PASS |
| 10 | **23** | Routage découverte + installation minimale + auto-réinstallation + francisation | commit `b145fe6`, gen-plan v3.19.0, PM-INSTALL v1.4.0, 23 skills min, −60,8 Mo |
| 11 | **24** | Re-certification → correct-work PROJET → clone-chat → PUSH | harnais task24 (107 PASS), rapport task24, présent clone, push B5 |

### §1.3 Détail par session

**Sessions 1-7 (lignée, Tasks 0 → 21)** : construction progressive de l'écosystème (corpus,
KB, arbitrages, baselines API hors périmètre, modes parallèles). Detail inutile à la reprise :
les clones prédécesseurs (§1.0) et les worklogs font foi. Point d'entrée utile : Tasks 18-21
ont établi le régime « certification 6/6 avant commit, push conditionnel au jeton ».

**Session 8 — Task 22 (2026-10-03)** : directive « vérifie l'idempotence des skills/agents
modifiés + fais-le automatiquement à partir de maintenant ». Installation PASS 11/11 ; preuve
f(f(x))=f(x) 15/15 (installation + arbitres + ULTRA) ; dérive ULTRA KO-L004 corrigée
(régénérée, archive rescellée 26/26) ; NOUVEL ARBITRE `check-tool-routing.py` branché 6e
(routage automatique des outils dédiés par type : skill→skill-creator, agent/PM→agent-creator,
script→script-creator, infrastructure→script-mon-ecosysteme-infrastructure, KB→skills-inventory)
; tags neutres ×5 ; agrégateur réparé. Commit de couche `9afc540` (65 fichiers). Push BLOQUÉ
sur credentials (0 jeton — anti-persistance respectée).

**Session 9 — Task 22-b2 (2026-10-03)** : directive « as-tu vérifié l'idempotence de tous les
éléments non-skill (MD, PY, JSON, PDF) ? » — constat honnête : NON au niveau octets. Protocole
B2 bâti (M0 → cycle C1 → M1 → cycle C2 → M2, verdict par élément). Tour 1 : 1 FAIL réel
(tool-routing s'observait lui-même — exclusion CERT_ARTIFACTS à la source), 2 écarts
(provenance « mode/plan », interactions périmé). Corrections : dates dérivées du commit
(plus d'horloge figée), bug cwd du harnais. Commit `bdf3d59`. Re-preuve : 3 RE-STABILISÉ
analysés comme **rapports à état dépendant** (diff vs HEAD, compteur worklog) — mathématiquement
incommittables en point-fixe → décision 22-ter : dé-suivi des 3 sorties runtime (classe `.next`),
critère applicable M1=M2 acquis. Commit `a7ca9de`. PREUVE FINALE : 36 PASS / 0 FAIL, arbre
committé = point-fixe véritable. PUSH armé, conditionné au PAT éphémère.

**Session 10 — Task 23 (2026-10-03/04)** : directive autonome en 5 actions. (1) Fraîcheur
prouvée (HEAD a7ca9de, ensure-installed rc=0). (2) gen-plan v3.18.0→**v3.19.0** §1.16 :
skills-inventory PRIORITAIRE (scanner 73 skills/73 descriptions/14 catégories/zéro API,
comparaison performances vs natifs mémorisée au KB), fallback skill-finder-cn UNIQUEMENT sur
échec avec contrôle cybersécurité audit-provenance avant adoption. (3) PM-INSTALL
v1.3.1→**v1.4.0** §2bis : fermeture mécanique (seeds + dependencies YAML + KB « Dépend de »
transitif) = 23 skills, empreinte c6212e1e ×2, **gain 60,8 Mo (96,7 %)**, arbre
`ecosystem-minimale/` ; corpus et archive TOUJOURS complets. (4) `ensure-installed.py`
(--check/--reinstall, clone éphémère sans persistance de jeton) branché au hook É1-INSTALL.
(5) Francisation idempotente : audit corrigé (élisions FR → 26 cibles RÉELLES, 31 faux positifs),
noyau par skill-creator (v1.1.0 FR), 16 tiers par agents de masse, identifiants/structure/blocs
de code préservés (hashes vérifiés), V6 18/26 sans régression ; liés propagés (KB miroir ×3,
ECO_SKILLS, 67 frontmatters, 7 citations vives, ULTRA régénéré SHA 7774994a, archive 26/26).
3 défauts d'arbitres corrigés à la source (compte KB figé → len(ECO_SKILLS) ; résolution PM
famille ; regex semver). Certification 6/6 PASS AVEC RÉSERVES. Commit `b145fe6` (HEAD, avance 8).

**Session 11 — Task 24 (2026-10-04, présente)** : directive ordonnée « vérifie idempotence →
correct-work(projet) → clone-chat → push (PAT fourni) ». Re-certification B2 de `b145fe6` :
**107 PASS / 0 RE-STABILISÉ / 0 FAIL**, py_compile 26/26, C1≡C2 ; échec transitoire tool-routing
diagnostiqué = artefact d'invocation (`--plan` court-circuite le fallback worklog du N2),
corrigé dans le harnais uniquement (KO-L003). correct-work PROJET : verify-correct-work 16/16,
rapport `download/rapport-correct-work-projet-task24.md` (PASS AVEC RÉSERVES). clone-chat :
présent document (8/8 checks). PUSH : pattern B5 (2 commits / 2 pushes), jeton éphémère
x-access-token jamais persisté, audit anti-persistance post-push.

---

## §2 — ÉCOSYSTÈME DE SKILLS

### §2.1 Skills créés ou modifiés (discussion)

#### gen-plan v3.19.0

- **Description** : protocole de planification gen-plan ; gagne §1.16 « Routage découverte »
  et hook É1-INSTALL (auto-réinstallation).
- **Catégorie** : ecosystem | **Langue** : fr
- **Spécification fonctionnelle** : §1.16 — à toute recherche de skills/éléments : skills-inventory
  PRIORITAIRE (comparaison de performances éléments trouvés vs natifs, MÉMORISÉE au KB) ;
  fallback skill-finder-cn UNIQUEMENT sur échec, avec contrôle cybersécurité audit-provenance
  AVANT adoption ; bascule unidirectionnelle. Hook É1 : ensure-installed.py --check → no-op si
  installé, sinon réinstallation (PM-INSTALL).
- **Spécification technique** : SKILL.md ~frontmatter semver 3.19.0 ; 7 citations vives
  mises à jour (context/fleet/graph/harness/loop/memory/spec engineering).
- **Relations** : skills-inventory, skill-finder-cn, audit-provenance, ensure-installed (script),
  PM-INSTALL, KB.

#### PROMPT-MAITRE-INSTALL-ECOSYSTEME v1.4.0 (agent/PM)

- **Description** : pipeline d'installation ; gagne §2bis « profils COMPLET (défaut) / MINIMALE ».
- **Spécification fonctionnelle** : MINIMALE = {gen-plan, correct-work, skills-inventory} ∪ liés
  (dépendances YAML + KB transitif) ∪ {ULTRA, SHARED, SYNC-CONTEXT} ∪ outillage ∪ KB ;
  corpus et archive TOUJOURS complets.
- **Relations** : task23-install-minimale.py (matérialisation), gen-plan, KB.

#### skill-creator v1.1.0 · version-management v1.1.0 · skill-finder-cn (FR)

- **Description** : francisation idempotente EN→FR / ZH→FR (identifiants, structure, blocs de
  code préservés — hashes vérifiés) ; skill-finder-cn : version + §0 installés, inscrit
  ECO_SKILLS (n°27) et KB.
- **Relations** : V6 re-verdict maintenu (skill-creator 8/8 ; version-management 3/8 inchangé,
  C006 voie L armée QUOTA_OK).

#### check-tool-routing.py — NOUVEL ARBITRE (6e)

- **Description** : enforcement automatique du routage des outils dédiés (directive Task 22).
- **Spécification technique** : N1 preuves mécaniques par artefact (frontmatter skill-creator §2,
  traçabilité version agent/PM, docstring+compilable script, entrées KB parsables) ; N2 routage
  normatif par session (plan/worklog doit citer le skill dédié de chaque type touché) ;
  exclusion CERT_ARTIFACTS (ses propres sorties) ; provenance mode/plan ; date du commit.
- **Relations** : certification-complete.py (agrégateur, 6e position), plan/worklog de session.

#### KNOWLEDGE.md (KB) — 27 entrées skills + décisions

- Miroirs ×3 (gen-plan, skill-creator, version-management) + entrée skill-finder-cn + décisions
  Task 22 (D006 routage) et Task 23 (D004 mémoire comparaison, D005, D006, D007) + bullet
  Task 22 « PUSH exécuté » corrigé (armé-en-attente, KO-L003).

### §2.2 Scripts créés ou modifiés

| Script | Rôle | Signature clé |
|--------|------|---------------|
| `scripts/task22-phase-a-install.py` (session) | installation pipeline, 11/11 | empreinte installation |
| `scripts/task22-phase-b-idempotence.py` (session) | preuve f(f(x)) niveau stdout 15/15 | cycles arbitres |
| `scripts/task22-phase-b2-non-skill-idempotence.py` (session) | protocole B2 par élément (Task 22) | M0/C1/M1/C2/M2 |
| `scripts/task24-b2-idempotence.py` (session) | protocole B2 re-pointé b145fe6 (Task 24) | 107 éléments, --worklog N2 |
| `scripts/task22-canonical-pass.sh` (session) | passe canonique 10 étapes | 6 arbitres → agrégateur → ULTRA → install → harnais |
| `scripts/task23-install-minimale.py` (repo) | fermeture mécanique installation minimale | 23 skills, c6212e1e |
| `scripts/ensure-installed.py` (repo) | garde --check/--reinstall idempotente | hook É1 gen-plan |
| `scripts/task23-complete-frontmatters.py` (repo) | complétion 67 frontmatters (semver, catégorie, tags) | idempotent ×2 |
| `scripts/check-tool-routing.py` (repo) | 6e arbitre (voir §2.1) | N1+N2, --plan/--worklog |
| `scripts/check-triggers-replay.py` (repo) | V6 triggers, date du commit | rc=1 par design (8 consignés) |
| `scripts/test-coherence-interactions.py` (repo) | arbitre interactions, garde R2 dynamisée | PM famille |
| `scripts/check-ecosysteme-integrity.py` (repo) | intégrité, compte KB dynamisé | len(ECO_SKILLS) |
| `scripts/gen-ultra-maitre.py` (repo) | génération ULTRA + --check | SHA 7774994a |
| `skills/correct-work/scripts/verify-correct-work.py` (repo) | 16 checks post-install | ALL PASS |

### §2.3 Artefacts produits

| Fichier | Taille | Description |
|---------|--------|-------------|
| `download/plan-task22-idempotence-skills-agents.md` | plan | plan de session Task 22 |
| `download/plan-task23-routage-install-minimale-francisation.md` | 38 L | plan Task 23, answer key D001-D008 |
| `download/plan-task24-idempotence-correctwork-clone-push.md` | 43 L | plan Task 24, answer key D001-D008 |
| `download/rapport-correct-work-projet-task22.md` (repo) | rapport | PROJET Task 22, 16/16 |
| `download/rapport-correct-work-projet-task23.md` (repo) | 36 L | PROJET Task 23, PASS AVEC RÉSERVES |
| `download/rapport-correct-work-projet-task24.md` (repo) | rapport | PROJET Task 24, PASS AVEC RÉSERVES |
| `scripts/task22-phase-b2-results.json` (session) | résultats | preuve B2 Task 22 (36 PASS) |
| `scripts/task24-b2-results.json` (session) | 798 L | preuve B2 Task 24 (107 PASS) |
| `download/clone-discussion-task22-24-idempotence-publication-2026-10-04.md` (repo) | présent clone | archivage de la discussion |
| commits `9afc540` → `bdf3d59` → `a7ca9de` → `b145fe6` (+ couche 24) | git | couches certifiées poussées |

### §2.4 Historique des interactions (KB)

| Ordre | Skills/scripts invoqués | Résultat |
|-------|------------------------|----------|
| Task 22 | gen-plan (plan) → task22-phase-a-install → arbitres ×6 → skill-creator (tags) → script-creator (arbitre D006) → correct-work | 15/15 PASS, commit 9afc540 |
| Task 22-b2 | script-creator (harnais B2) → arbitres ×6 ×2 cycles → knowledge-observer (analyse point-fixe) → correct-work | 36/36 PASS, commits bdf3d59/a7ca9de |
| Task 23 | gen-plan (plan) → skills-inventory (scanner) → audit-provenance (cybersécurité fallback) → skill-creator + agents de masse (francisation) → agent-creator (PM-INSTALL v1.4.0) → script-creator (task23-*, ensure-installed) → prompt-engineering (descriptions) → knowledge-observer (leçon élisions) → correct-work | 6/6 PASS, commit b145fe6 |
| Task 24 | gen-plan (plan) → script-creator (harnais task24) → arbitres ×6 ×2 cycles → correct-work (PROJET, verify 16/16) → clone-chat (présent clone) → script-mon-ecosysteme-infrastructure (push B5) | 107/107 PASS, push |

---

## §3 — DÉCISIONS CLÉS

### §3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | Idempotence prouvée PAR ÉLÉMENT (octets) avant tout push — pas seulement au niveau stdout | directive Task 22-b2 : « tous les éléments (autres que les skills. ex : MD, PY, etc.) » | protocole B2 M0/C1/M1/C2/M2, harnais dédié, verdict par élément |
| 2 | Routage des outils dédiés AUTOMATIQUE à partir de maintenant | directive Task 22 (D006) | 6e arbitre check-tool-routing branché dans l'agrégateur — toute couche sans routage explicite échoue mécaniquement |
| 3 | gen-plan : skills-inventory PRIORITAIRE (comparaison performances mémorisée), fallback skill-finder-cn avec contrôle cybersécurité | directive Task 23 (D004) | §1.16 gen-plan v3.19.0, décision KB |
| 4 | Installation minimale économe en disque (gen-plan + correct-work + skills-inventory + liés ∪ ULTRA/SHARED/SYNC-CONTEXT) | directive Task 23 (D005) | PM-INSTALL v1.4.0 §2bis, 23 skills, −60,8 Mo (96,7 %) |
| 5 | Auto-réinstallation à l'invocation de gen-plan si écosystème absent | directive Task 23 (D006) | ensure-installed.py au hook É1 |
| 6 | Francisation idempotente de tous les skills/agents non-français, SANS traduire les noms de fonctions/skills/agents/scripts | directive Task 23 (D002/D003) | 26 cibles réelles réécrites, identifiants préservés, liés propagés |
| 7 | Séquence de clôture ordonnée : vérif idempotence → correct-work(projet) → clone-chat → push | directive Task 24 | ordonnancement exécuté tel quel ; PAT fourni pour le push |

### §3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | tool-routing FAIL M1≠M2 (Task 22-b2) | l'arbitre dérivait la couche de l'état sale du worktree et voyait ses propres sorties réécrites (auto-observation, f(f(x))≠f(x)) | exclusion CERT_ARTIFACTS (*-report.json) dans layer_files() | idempotent, rc stable |
| 2 | Rapports non comparables / périmés (Task 22-b2) | provenance d'invocation absente ; interactions généré avant ajout de section worklog | champs « mode »/« plan » ; rafraîchissement par passe canonique | comparabilité rétablie |
| 3 | Dates horloges figées/variables (Task 22-b2) | dates murales ou codées en dur dans 3 rédacteurs de rapports | date dérivée du commit audité (git log -1 --format=%cd) | classe de variance fermée |
| 4 | Sonde --help exécutait des one-shots (Task 22-b2) | scripts sans garde __main__ s'exécutent à toute invocation | analyse statique uniquement (grep, jamais d'exécution) | risque d'effet de bord éliminé |
| 5 | Harness cwd erroné (Task 22-b2) | match « my-project » dans l'ARGUMENT --plan | test cmd.startswith() | tool-routing exécuté au bon cwd |
| 6 | 3 rapports runtime jamais point-fixe (Task 22-ter) | rapports décrivant l'état vs HEAD = fonction de l'état | dé-suivi git (classe .next), critère M1=M2 acquis | arbre committé = point-fixe véritable |
| 7 | tool-routing rc=1 en re-certification (Task 24) | artefact d'invocation : --plan court-circuite le fallback worklog du N2 | correction HARNAIS seule (--worklog en complément), arbitre intact | rc=0 ×2 cycles, leçon consignée |
| 8 | Compte KB figé « 26 » (Task 23) | valeur littérale dans l'arbitre intégrité | dynamisé len(ECO_SKILLS) | garde pérenne |
| 9 | Résolution PM par nom exact (Task 23) | crash si l'installé devance le corpus (v3.19.0 > v3.18.0) | garde R2 dynamisée : PM famille le plus récent, antérieur toléré+journalisé, postérieur FAIL | interactions robustes |
| 10 | Regex semver avalant le point final (Task 23) | extraction non bornée (« 3.18.0. ») | regex bornée | parsing correct |
| 11 | Compteur langue surestimant l'anglais (Task 23) | élisions FR (l'utilisateur, d'entrée, s'active) comptées comme EN | parseur corrigé → 26 cibles réelles, 31 faux positifs | francisation ciblée, 0 régression V6 |
| 12 | ULTRA en dérive / KB bullet faux (Task 22/23) | montées de version non propagées ; « PUSH exécuté » affirmé alors qu'armé | ULTRA régénéré (SHA 7774994a, --check no-op) ; bullet corrigé (KO-L003) | cohérence documentaire |

### §3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| KO-L003 | Ne JAMAIS ajuster la réalité au verdict — diagnostiquer, corriger à la source | exclusion CERT_ARTIFACTS plutôt que figer le rapport |
| Anti-persistance | jeton PAT éphémère en URL d'invocation uniquement ; jamais dans un fichier suivi, la remote ou la config ; révocation recommandée après usage | push x-access-token, audit grep = 0 occurrence |
| Pattern B5 | après push : journalisation post-push (date dérivée du commit) → commit → second push (2 commits / 2 pushes) | Task 24 |
| Point-fixe committé | un rapport décrivant l'état courant ne peut être un point-fixe committé → dé-suivi (classe .next), critère applicable M1=M2 | 22-ter : 3 rapports runtime |
| Analyse statique des scripts inconnus | jamais exécuter un script sans garde __main__ ni autorisation (QUOTA_OK pour l'API) | classification classify_py |
| Identifiants protégés | noms de skills/fonctions/agents/scripts/chemins jamais traduits lors de la francisation | skill-creator, ensure-installed.py verbatim |
| Preuve avant affirmation | toute affirmation de rapport adossée à une empreinte/verdict consigné | EMPREINTES-NON-SKILL 184bdb85… |

### §3.4 Données de calibration

| Mesure | Valeur | Source |
|--------|--------|--------|
| Éléments non-skill suivis (b145fe6) | 107 (py_compile 26/26) | task24-b2-results.json |
| Verdict B2 Task 24 | 107 PASS / 0 RE-STABILISÉ / 0 FAIL, C1≡C2 | idem |
| EMPREINTES-NON-SKILL (Task 24) | sha256 184bdb85b2c1507e… | idem |
| Empreinte installation | fe1b6975… stable ×2 (Task 23/24) ; 255a8e2e (Task 22) | Phase A installer |
| ULTRA | SHA 7774994a, --check no-op | gen-ultra-maitre |
| Installation minimale | 23 skills, empreinte c6212e1e ×2, gain 60,8 Mo (96,7 %) | task23-install-minimale.py |
| KB | 27 entrées skills versionnées + décisions (28 H2) | skills-inventory |
| V6 triggers | 18/26 conformes, 8 dérivants consignés (0 régression post-francisation) | check-triggers-replay |
| verify-cross | 98,8 % (0 erreur) | arbitre cross |
| verify-correct-work | 16/16 ALL PASS | skill correct-work |
| Avance origin/main avant Task 24 | 8 commits (Task 15/16 → 23) | git log |

### §3.5 Évolutions de contexte (Context Drift)

**5 types de drift** : INVERSION (décision renversée) · MODIFICATION (ajustée) · CORRECTION
(erronée corrigée) · ENRICHISSEMENT (complétée) · RECALIBRAGE (paramètre ajusté).

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | INVERSION | 3 rapports runtime de certification suivis git | dé-suivis (gitignore + rm --cached) | 22-b2/22-ter | section 22-b2, addenda | un rapport à état dépendant ne peut être un point-fixe committé |
| 2 | ENRICHISSEMENT | preuve d'idempotence au niveau stdout (15/15) | preuve PAR ÉLÉMENT (protocole B2) | 22-b2 | section 22-b2 | exigence propriétaire : tous les éléments non-skill |
| 3 | ENRICHISSEMENT | 5 arbitres de certification | 6e arbitre check-tool-routing (routage automatique) | 22 | section 22 | directive D006 « automatiquement à partir de maintenant » |
| 4 | CORRECTION | KB bullet Task 22 « PUSH exécuté » | « armé-en-attente » | 23 | section 23 | KO-L003 : jamais affirmer sans preuve |
| 5 | RECALIBRAGE | compteur langue naïf : 70/103 non-FR | audit élisions : 26 cibles réelles | 23 | section 23 | leçon knowledge-observer : élisions FR masquent les articles |
| 6 | MODIFICATION | push « armé, en attente de jeton » (Tasks 22/23) | push exécuté avec PAT fourni (pattern B5) | 24 | section 24 | le propriétaire fournit le jeton et ordonne la publication |

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone

1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire

1. Lire §0 (Règle zéro) — tout est à reconstruire
2. Reconstruire les fichiers spécifiés en §2 (les clones/worklogs préexistants restent la
   source de vérité pour la lignée Tasks 0 → 21)
3. Appliquer les décisions et conventions de §3 (KO-L003, anti-persistance, B5, identifiants
   protégés)
4. Vérifier l'état réel par les empreintes de §3.4 avant toute affirmation
5. Se positionner à l'état exact de fin de discussion : écosystème certifié, couches Task
   22 → 24 poussées, aucune tâche ouverte hors réserves documentées

### Fichiers à reconstruire en priorité

1. **worklogs** (`/home/z/my-project/worklog.md`, `ecosystem/worklog.md`) — mémoire de toutes
   les sessions (11 + 22 sections)
2. **plans/rapports Task 22-24** (`download/plan-task2{2,3,4}*.md`,
   `download/rapport-correct-work-projet-task2{2,3,4}.md`) — contrats et verdicts
3. **scripts/session** (`scripts/task24-b2-idempotence.py`, `task22-phase-b2-*.py`,
   `task22-phase-a-install.py`, résultats JSON) — outillage de preuve
4. **gen-plan v3.19.0 §1.16 + PM-INSTALL v1.4.0 §2bis** — comportements nouveaux à connaître
5. **KB** (`skills/KNOWLEDGE.md`) — registre 27 skills + décisions

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :

1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra : tout le contexte du présent clone + le nouveau contexte
3. Le nouveau clone remplace ce fichier ; le clone « grandit » sans perdre l'historique

**Mécanisme** : les sections §1-§3 (incluant §3.5 Context Drift) sont enrichies avec les
nouvelles sessions ; §0, §4-§5 sont régénérés à l'identique (auto-référentiels).

---

## §6 — VALIDATION (8 checks, Étape 6 clone-chat)

| # | Check | Verdict | Preuve |
|---|-------|---------|--------|
| 1 | Auto-suffisance | PASS | aucun renvoi externe indispensable ; §0 fixe l'environnement ; §2 décrit fichiers et signatures |
| 2 | Complétude worklog | PASS | 11/11 sessions racine en §1.2 (détail Tasks 22-24, lignée héritée §1.0) ; sections écosystème 22/23/24 couvertes |
| 3 | Complétude skills | PASS | §2.1 : versions, descriptions, spécifications, relations pour chaque skill/PM modifié (gen-plan 3.19.0, PM-INSTALL 1.4.0, skill-creator 1.1.0, version-management 1.1.0, skill-finder-cn, check-tool-routing, KB) |
| 4 | Complétude décisions | PASS | §3.1 : 7 décisions avec contexte + conséquence |
| 5 | Complétude bugs | PASS | §3.2 : 12 bugs, chaque ligne = cause + fix + résultat |
| 6 | Complétude drifts | PASS | §3.5 : 6 drifts typés, Avant/Après, session + ligne worklog ; analyse effectuée et consignée |
| 7 | Exécutabilité | PASS | §4 : instructions + priorité de reconstruction + empreintes de vérification (§3.4) |
| 8 | Auto-clonage | PASS | §5 présent et auto-référentiel ; clone-chat référencé ; mécanisme §1-§3 enrichis / §0,§4-§5 régénérés |

**Résultat Étape 6 : 8/8 PASS** — clone valide (profil NORMAL, discussion longue).

