# Plan d'actions — Task 111 : installation écosystème (GO-1) + PUSH pendance + point d'état

> Directive propriétaire trace `1a1f7d3e607663f1` : « installe mon écosystème personnel en tant que mon écosystème personnel sur mon profil local grâce à mon fichier [PM-INSTALL commit a5daa964] et lorsque l'installation de mon écosystème sera terminée, prend en compte mon skill gen-plan fraichement installé pour générer le plan d'actions des étapes suivantes : gen-plan (step) — relecture intégrale de cette discussion grâce au dernier clone + effectue les dernières tâches en utilisant ma clé [KO-L009] ; puis correct-work (projet) --bloc ; puis clone-chat ». Session web-ecef7f80, suite worklog 157. Généré le 2026-11-20 par gen-plan v3.43.0 (E1-E8).

**Horodatage plan : 2026-11-20T00:00:00Z**

## E1 — Analyse de la demande (answer key ci-dessous)

File d'instructions propriétaire, 5 étapes ordonnées :
1. **GO-1** — installation de l'écosystème sur le profil local via PM-INSTALL v1.10.0 (entrée canonique `scripts/bootstrap-ecosysteme.py`).
2. **gen-plan (step)** — (a) relecture intégrale via le dernier clone (22ᵉ, task110) ; (b) exécution des dernières tâches avec la clé fournie.
3. **correct-work (projet) --bloc**.
4. **clone-chat**.

## E2 — Inventaire des ressources (mesuré au disque, 2026-11-20)

| Ressource | État mesuré |
|---|---|
| PM-INSTALL | byte-identique ×3 sources (upload téléchargé / `git show a5daa964` / `git show HEAD`) SHA-256 `b2fe8371…`, v1.10.0 |
| Dépôt git (avant push) | HEAD = `d4e228f4` (Task 110 CLOSE), origin/main = `a5daa964` — **1 commit en pendance PUSH** ; dérive recyclage : 2778 fichiers mode 644→755, 0 ligne modifiée |
| Installation hôte | ensure-installed : verdict INSTALLE, 55 entrées KB, 0 skill manquant, host_head = d4e228f4 |
| Clone de relecture | `download/clone-chat-session-web-ecef7f80-20261119-task110.md` (22ᵉ, 8/8 S1-S8) + `download/taches-restantes-task108.md` (fait foi) |
| Tâches restantes (livrable) | 1 révocation PAT [PROPRIÉTAIRE — CRITIQUE] · 3-4-5 ÉTEINTES (Task 110) · 6 décision cron [PROPRIÉTAIRE] · 7 surveillance F3 [AUTO] · 8 PMs §0 [AUTO] |
| G-RES | OK — profil NORMAL, 0 signal de pression |

## E3 — Classification : Type 4 (maintenance état écosystème — installation + push + suivi, livrables = plan + livrable mis à jour + CW + clone).

## E4 — Estimation #token

| Groupe | #token estimé |
|---|---|
| G0-G1 préflight + installation + relecture | 2 000 |
| G2 dernières tâches (push + cron) | 1 200 |
| G3 livrables (plan + tâches restantes + worklog) | 1 000 |
| G4 commit + push | 1 500 |
| G5 correct-work --bloc | 1 500 |
| G6 clone-chat | 1 000 |
| **Total** | **~8 200** (profil NORMAL, plage exécution standard) |

## E5 — Skills mobilisés : gen-plan (pilote, ce plan) · correct-work (E8 + G5 --bloc) · clone-chat (G6) · resource-monitor (E1-RES : OK). Arbitres : certification-complete, check-ecosysteme-integrity, verify-correct-work, check-triggers-replay, task14-scan-doublons, answer-key-checker, check_plan_protocol.

## E6 — Profil NORMAL (G-RES OK).

---

## Answer key (D001-D010)

| ID | Décision | Critère | Vérification | Source | Priorité | Statut |
|---|---|---|---|---|---|---|
| D001 | GO-1 par entrée canonique bootstrap-ecosysteme.py (1 commande) | verdict INSTALLE-REPARÉ rc=0 | sortie bootstrap : preflight RÉPARÉ 2778 · installation 55 SHA 0 divergence · certification ALL-PASS-6/6 · garde É1 INSTALLE | directive étape 1 + PM-INSTALL §3.2-c | P1 | **PASS** (mesuré) |
| D002 | PM-INSTALL = commit a5daa964 fourni par le propriétaire | byte-identité ×3 sources | sha256sum ×3 = `b2fe8371…` | directive (URL commit a5daa964) | P1 | **PASS** |
| D003 | Relecture intégrale via le DERNIER clone (22ᵉ task110) + livrable tâches restantes fait foi | 0 trou de continuité (suites 155-156) | clone 8/8 S1-S8 + livrable cohérent (3-4-5 ÉTEINTES avec preuves) | gen-plan(step) item a | P1 | **PASS** |
| D004 | Dernières tâches = pendance PUSH d4e228f4 (0 PAT au tour Task 110) + surveillance F3 (tâche 7) | extinction de la pendance + constat consigné | push rc=0 + ls-remote anonyme = HEAD ; bootstrap du tour SAIN (0 récidive) | clone 22ᵉ §5 « si un PAT frais est fourni, éteindre la pendance » + livrable tâche 7 | P1 | **PASS** |
| D005 | Manipulation clé KO-L009 (mémoire de commande, sortie masquée, 0 trace écrite) | 0 occurrence de clé dans tout livrable/clone/worklog | grep négatif ×4 arbres + clone S8 « 0 secret » | leçon Task 98/101, KO-L009 | P1 | **PASS** |
| D006 | Push = `d4e228f4:main` (fast-forward a5daa964..d4e228f4) puis commit du tour poussé immédiatement | ls-remote anonyme : refs/heads/main = HEAD final ; rev-list origin/main..HEAD = 0 | mesuré après chaque push | leçon Task 98/101 « push immédiat dès PAT frais » | P1 | **PASS** |
| D007 | cron 531684 : vérification état (cron list) SANS recréation | constat consigné (0 job = 4ᵉ dispositif perdu), escalade maintenue | cron list = 0 job mesuré | livrable tâche 6 + clause anti-boucle règle d'or n°5 | P3 | **PASS** (escalade maintenue) |
| D008 | Tâche 7 (surveillance F3) éteinte par constat : bootstrap du tour = injection v2.2.0 SAIN | constat consigné au tour d'installation (critère d'extinction verbatim) | worklog suite 157 + livrable mis à jour | livrable tâche 7 critère d'extinction | P3 | **PASS** |
| D009 | HORS PÉRIMÈTRE session : tâche 1 (révocation ancien PAT) — PROPRIÉTAIRE | (côté GitHub) | rapport $FACON au chat | livrable tâche 1 [PROPRIÉTAIRE — CRITIQUE] | P1 | OUVERTE [PROPRIÉTAIRE] |
| D010 | Clôture : correct-work (projet) --bloc PUIS clone-chat 23ᵉ (8/8 S1-S8, 0 secret) | verdicts mécaniques PASS / 8/8 | arbitres + checks clone-chat | directive étapes 3-4 | P1 | **À EXÉCUTER (G5-G6)** |

## Groupes d'exécution

### G0-G1 — Préflight + GO-1 + relecture — [TERMINÉ]

| Tâche | Description | Statut |
|---|---|---|
| T0.1 | Téléchargement PM-INSTALL (commit a5daa964) + byte-identité ×3 sources | [TERMINÉ] |
| T0.2 | État git : HEAD d4e228f4, 1 commit en pendance, dérive recyclage 2778 modes | [TERMINÉ] |
| T1.1 | GO-1 : bootstrap-ecosysteme.py → INSTALLE-REPARÉ (certification ALL-PASS-6/6, garde É1 INSTALLE, re-check ensure-installed rc=0) | [TERMINÉ] |
| T1.2 | Relecture : clone 22ᵉ + livrable tâches restantes + worklog suites 155-156 — 0 trou | [TERMINÉ] |

### G2 — Dernières tâches avec la clé — [TERMINÉ]

| Tâche | Description | Statut |
|---|---|---|
| T2.1 | PUSH pendance `d4e228f4:main` rc=0 (KO-L009) — E15 36ᵉ consignée au worklog | [TERMINÉ] |
| T2.2 | Atterrissage vérifié : ls-remote anonyme = d4e228f4, parité HEAD = origin, ref locale origin/main réalignée | [TERMINÉ] |
| T2.3 | cron list = 0 job — escalade maintenue (D007) | [TERMINÉ] |

### G3 — Livrables — #token 1 000

| Tâche | Description | Statut |
|---|---|---|
| T3.1 | Worklog suite 157 ouverte ×2 arbres (idempotence ×2, parité md5) | [TERMINÉ] |
| T3.2 | Présent plan écrit + PLAN-AFFICHE (E7-DISP 6 points) | [TERMINÉ] |
| T3.3 | `download/taches-restantes-task108.md` mis à jour : pendance PUSH Task 110 ÉTEINTE (preuves) + tâche 7 ÉTEINTE (constat bootstrap) + note cron 4ᵉ dispositif | [TERMINÉ] |

### G4 — Commit + push du tour — #token 1 500

| Tâche | Description | Statut |
|---|---|---|
| T4.1 | Commit Task 111 (livrables + worklog + script ouverture) + push immédiat (clé du tour) | [À FAIRE] |
| T4.2 | Parité finale HEAD = origin/main + arbitres pré-commit (certification 6/6, doublons 0, triggers) | [À FAIRE] |

### G5 — correct-work (projet) --bloc — #token 1 500

| Tâche | Description | Statut |
|---|---|---|
| T5.1 | CW PROJET Étapes 1-5 --bloc, rapport horodaté download/, verdict mécanique | [À FAIRE] |

### G6 — clone-chat — #token 1 000

| Tâche | Description | Statut |
|---|---|---|
| T6.1 | Clone 23ᵉ de la lignée (7+1 étapes, 8/8 S1-S8, 0 secret), worklog consigné | [À FAIRE] |
