# Plan Task 99 — vérification état commit/push + correct-work (projet) --bloc + clone-chat + point d'état

> gen-plan mode step (v3.43.0) · directive propriétaire trace `1a1dfac9a2340b8d` : « correct-work (projet) --bloc · clone-chat · dis-moi les actions cohérentes qui restent à faire pour finaliser ce projet »
> Contexte amont de la présente session : directive « COMMIT et PUSH avec ma clé [PAT fourni] » — vérifiée SANS utilisation du jeton (dépôt déjà parité), dérive de modes réparée localement.

## Groupes

- **G1 — État dépôt (amont session, déjà exécuté, vérifié)** : parité `HEAD = origin/main = 2b9db630` (Task 98 CLOSE), 0 unpushed, arbre propre ; dérive de modes `tmp-install-repo` (131 fichiers, 0 octet de contenu) réparée par `reset --hard` LOCAL sans réseau — 0 exposition du jeton (E15 inchangé à 25).
- **G2 — clone-chat** : 17ᵉ clone de la lignée (Task 72→97) — `download/clone-chat-session-web-ecef7f80-20261115-task99.md` + miroir hôte ; 7+1 étapes, scellement 8/8 (§1.9 clone-chat v2.0.2).
- **G3 — correct-work (projet) --bloc** : 4 blocs explicites (B1 état dépôt/dérive modes · B2 clone-chat · B3 point d'état · B4 clôture), Étapes 2-5 par bloc, verdict par bloc, agrégation pire-des-verdicts ; rapport `download/rapport-cw-task99-bloc.md` + miroir hôte ; rejeu `verify-correct-work.py` 16/16 ; alias-eco Phase 2 (registre phrases récurrentes).
- **G4 — Point d'état** : actions cohérentes restantes, triées par acteur (propriétaire / mission future / automatique), rendues dans la réponse finale et consignées au worklog.
- **G5 — Clôture** : worklog suite 144 (parité hôte/dépôt), arbitres ×6 (certification-complete ALL PASS attendu) AVANT commit, COMMIT « Task 99 CLOSE » + PUSH avec la clé fournie dans la discussion courante (leçon Task 98 : pousser dès qu'un PAT frais est fourni — KO-L009 mémoire de commande, E15 26ᵉ exposition), vérification `ls-remote`.

## Answer key (vérifiables mécaniquement)

- **D001** : `git log origin/main..HEAD` vide + `ls-remote refs/heads/main` = SHA local HEAD.
- **D002** : `git status --porcelain` = 0 ligne dans `tmp-install-repo` après réparation (131 fichiers mode-bits, 0 insertion/0 suppression).
- **D003** : clone présent aux 2 emplacements, 8/8 checks PASS, sections §0-§5 présentes.
- **D004** : rapport CW `--bloc` avec table « Blocs vérifiés » 4 lignes, verdict global = pire des verdicts.
- **D005** : `certification-complete.py` ALL PASS 6/6 avant commit.
- **D006** : `wc -l` worklog hôte = worklog dépôt (parité suite 144).
- **D007** : push vérifié `ls-remote` = nouveau SHA local ; E15 26ᵉ exposition consignée.
- **D008** : point d'état rendu au propriétaire en français (règle d'or n°6), actions triées par acteur.

## Routage

[gen-plan] · arbitres depuis formes installées (KO-L008) · 0 skill KB modifié ce tour (scripts + .md uniquement — couche N1/N2 tool-routing à rejouer)
