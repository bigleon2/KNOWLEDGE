# Plan Task 102 — Installation + relecture intégrale + PUSH + continue + CW --bloc + clone-chat

> gen-plan mode step (v3.43.0) · Directive propriétaire trace `1a1e2bbb50baf7d1` : ① installer l'écosystème personnel sur le profil local via le PM installateur (URL `aa3b99d` — dérivation dynamique KO-L003 : corpus vivant v1.9.16, garde R2) ; ② une fois installé, générer le plan des étapes suivantes, puis les exécuter dans l'ordre : (a) relire l'intégralité de la discussion en mode bloc par bloc ou via les clones et les archives ; (b) PUSH avec la clé [PAT fourni] ; (c) continue ; (d) correct-work (projet) --bloc ; (e) clone-chat.

## G0 — Installation (EXÉCUTÉE EN AMONT, ce tour)

- Dérive mode-bits 2728 fichiers (0 octet de contenu, 59 binaires byte-identiques vérifiés par hash-object) réparée par `git reset --hard` LOCAL avant installation.
- Pipeline canonique `scripts/eco_install_pipeline.py` (forme installée, KO-L008) : rc=0 — préflight pin `a14f750` descendant-tolérant OK · garde R2 0 rétrogradation · archive v2.3 rescellée 15 entrées (attendu 15 — fix F1 Task 100 validé en réel) · manifeste integrity 114/114 PASS · post-install 55/55 SHA, 0 divergence · repo 0 porcelain (idempotence) · interactions 55/55 PASS STRICT.

## Groupes (items dans l'ordre de la directive)

- **G1 (item a)** Relecture intégrale bloc par bloc via worklog (146 suites) + clones (17 clôtures) + archives : extraction mécanique (`scripts/task102-extraction-blocs.py` — stdlib, découpage par suite, agrégation par blocs chronologiques, stats verdicts/E15/pendances) → note rédigée `download/note-relecture-blocs-task102.md` (un bloc par phase, points clés, incidents, leçons, table des clones).
- **G2 (item b)** PUSH avec la clé : à l'instant t post-installation = 0 unpushed (idempotence prouvée) → consignation no-op honnête SANS exposition ; le push final du commit du tour est exécuté en clôture avec la clé fraîche fournie ce tour (leçon Task 98 — jamais laisser un commit réel non poussé quand un PAT frais est disponible). E15 : 29ᵉ exposition consignée.
- **G3 (item c)** Continue : point d'état des pendances (rotation PAT [PROPRIÉTAIRE] · PMs §0 L2 [AUTO] · cron 531684 [AUTOMATIQUE]) + vérification cron actif + orientation suivante.
- **G4 (item d)** correct-work (projet) --bloc : 4 blocs (B1 préflight/installation · B2 relecture · B3 continue/état · B4 clôture clone/push) × Étapes 2-5 → rapport `download/rapport-cw-task102-bloc.md` (agrégation = pire bloc).
- **G5 (item e)** clone-chat 18ᵉ clôture : `download/clone-chat-session-web-ecef7f80-20261116-task102.md` — §0-§5, directives/leçons/reprise mécanique, scellement 8/8 S1-S8, 0 secret (KO-L009).
- **G6** Clôture : worklog suite 147 (hôte↔dépôt parité md5) + arbitres pré-commit (verify-correct-work 16/16 · certification-complete ALL PASS · triggers 101/101) + miroirs download/ + commit « Task 102 CLOSE » + PUSH avec la clé (KO-L009 mémoire de commande, sortie masquée, E15 29ᵉ) + ls-remote de vérification.

## Answer key (vérifiables mécaniquement)

- **D001** : pipeline installation rc=0 + 55/55 SHA + 114/114 + 55/55 STRICT + repo 0 porcelain.
- **D002** : extraction mécanique — 146 suites couvertes, 0 suite manquante, blocs chronologiques bornés.
- **D003** : note relecture livrée avec blocs, stats E15/verdicts, table des 17 clones, leçons.
- **D004** : no-op PUSH documenté à l'instant t (0 unpushed) + push final du commit du tour avec ls-remote = SHA local.
- **D005** : point d'état rendu (pendances par acteur + cron vérifié).
- **D006** : rapport CW --bloc 4 blocs, verdict agrégé.
- **D007** : clone 8/8 S1-S8, 0 occurrence de jeton.
- **D008** : worklog suite 147 parité md5 hôte↔dépôt.
- **D009** : arbitres ALL PASS avant commit.
- **D010** : push final vérifié `ls-remote` = HEAD ; E15 29ᵉ consignée (rotation IMPÉRATIVE).

## Routage

[gen-plan] · couches : scripts/ + download/ + worklog (0 skill KB modifié sauf besoin démontré) · KO-L009 (jeton mémoire de commande) · règle d'or n°6 (français exclusif) · règle d'or n°5 (jamais de re-jeu à l'identique sans adaptation).
