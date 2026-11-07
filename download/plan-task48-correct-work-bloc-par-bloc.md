# Plan d'actions — Task 48 : Mode « bloc par bloc » correct-work (projet --bloc) + chaîne + PAT PUSH (GO)

- **Généré par** : gen-plan v3.33.1 (dernière version installée — KO-L005) · mode **step**
- **Date** : 2026-11-04 · **Session** : web-6058b3ba · **Trace** : 1a1a4fb0b84786f5 · Horodatage plan : 2026-11-04T05:20:00+00:00

## Recensement E1-E2 (règle d'or n°7 — couverture vérifiable de TOUS les éléments de la discussion)

| # | Élément de la discussion (verbatim/synthèse) | Couverture |
|---|---|---|
| 1 | « correct-work (projet) en mode "bloc par bloc" $FACON2. intègre $FACON ce mode "bloc par bloc" dans mon skill "correct-work" avec "correct-work (projet) --bloc" en tant que déclencheur et intègre $FACON cette modification. » | G1 (intégration skill + cascade) + G2 (usage — preuve vivante) |
| 2 | « correct-work. » | G2 (correct-work (projet) standard en fin de chaîne) |
| 3 | « clone-chat. » | G3-SG3.1 |
| 4 | « GO avec ma clé "github_pat_…". » | G3-SG3.2 — PAT PUSH (pendance Tasks 46/47 résolue) |
| 5 | Lignée (worklog, 746 L) : pendances reportées — S4 MK2 matériel, grille #token contingence reprise ×3-4, N1 natifs 57 + gif-animator-pro (plateforme-gérés) | Pendances consignées G3-SG3.3 (aucune perdue) |
| 6 | KO-L009 : la clé a été postée DANS le canal par le propriétaire (précepte antérieur : « clé hors canal ») — écart consigné | G3-SG3.2 (jeton éphémère unique, jamais persisté/recopié, rotation recommandée immédiate) |

**Alias résolus** : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) ».

**État disque (règle d'or n°5, audit E1-RES)** : clone de travail `work/KNOWLEDGE-b75a620` HEAD `4569930`, remote `https://github.com/bigleon2/KNOWLEDGE.git`, working tree portant les modifications Tasks 41→47 non commitées (« commit Tasks 41→47 à créer sur HEAD 4569930 ») ; correct-work v2.8.0 (4 modes, §A 9 déclencheurs, pas d'option --bloc) ; écosystème certifié 2026-11-04 (integrity 98/98, verify-cross 141/141, coherence 51 PASS/23 WARN/0 FAIL, garde-plans PASS, doublons 0) ; cron **501529** actif (auto-suppression post-PUSH encodée dans son payload).

## Groupes d'exécution (mode step — correct-work(groupe) après chaque groupe, max 2 rounds)

### G1 — Intégration du mode « bloc par bloc » dans correct-work #9k

- **SG1.1 Audit des sources (vague parallèle)** — T1.1.1 lire PM CORRECT-WORK v2.8.0 (§A, §1.2, §7 history) · T1.1.2 lire SKILL.md correct-work v2.8.0 (§A, §1.2, §10.1) · T1.1.3 lire evals/trigger_evals.json + scripts/verify-correct-work.py (contraintes arbitres). *Indépendance : lectures pures, preuve triviale.*
- **SG1.2 Intégration SKILL.md (écriture unique)** — T1.2.1 déclencheur `correct-work (projet) --bloc` ajouté au §A + read_when ; T1.2.2 sémantique du mode : option du mode PROJET — décomposition en BLOCS explicites (groupes/sous-groupes du plan ou livrables), Étapes 2-5 appliquées PAR BLOC, verdict PAR BLOC (PASS / PASS AVEC RÉSERVES / FAIL), agrégation = pire des verdicts (alignée §1.4 multi-cibles) ; T1.2.3 checklist §10.1bis « Mode bloc par bloc » ; T1.2.4 version frontmatter 2.8.0 → **2.9.0** (MINOR, addition pure, description enrichie de l'option --bloc) ; T1.2.5 worklog.
- **SG1.3 Cascade KO-L004 ($FACON — cohérente, optimisée, fonctionnelle)** — T1.3.1 delta verrouillé `scripts/delta-correctwork-v290.json` + génération MÉCANIQUE PM CORRECT-WORK v2.9.0 (+ SHARED §6.1 + PM-INSTALL recalibrés si lignes correct-work) ; T1.3.2 archivage R4 PM v2.8.0 (git mv byte-identité) ; T1.3.3 recalibrage croisé : KB (entrée correct-work + calibration 2.9.0), pin ECO_SKILLS, `@historique/historiques-par-skill/correct-work.md`, evals/trigger_evals.json (nouveau cas --bloc) ; T1.3.4 propagation §0 + rescellement archive v2.3 (round-trip) ; T1.3.5 miroir hôte syncé.
- **SG1.4 Replay arbitres ×2 (GRAPH-DIAMOND)** — T1.4.1 verify-correct-work.py (16 checks) ; T1.4.2 verify-cross + integrity manifeste + coherence ; T1.4.3 trigger-evals replay (discovery du déclencheur --bloc). *Indépendance entre arbitres : preuve triviale (lectures indépendantes).*

### G2 — correct-work (projet) --bloc (preuve vivante) + correct-work (projet) standard #6k

- **SG2.1 correct-work (projet) --bloc sur la chaîne Task 48** — blocs : B1 = intégration skill (G1-SG1.2) ; B2 = cascade KO-L004 (G1-SG1.3/1.4) ; B3 = plan + recensement Task 48. Verdict PAR BLOC + agrégation. *Dépend de G1 (le mode doit exister pour être exercé — séquentiel justifié).*
- **SG2.2 correct-work (projet) standard (item 2)** — vérification complète Étapes 1-5 de l'ensemble, verdict final (attendu : PASS AVEC RÉSERVES au plus — réserves héritées N1/23 WARN balises connues), rapport `download/rapport-correct-work-projet-task48.md`.

### G3 — clone-chat + PAT PUSH (GO) + clôture #7k

- **SG3.1 clone-chat** — T3.1.1 clone de la discussion Task 48 (7+1 étapes) → `download/clone-discussion-2026-11-04-task48-correct-work-bloc.md`.
- **SG3.2 PAT PUSH sur GO (pendance Tasks 46/47 résolue)** — T3.2.1 contrôles pré-push : certification arbitres re-vérifiée (integrity 98/98, verify-cross 141/141, coherence, garde-plans, doublons 0) + **0 secret dans le diff** (scan PAT avant commit) + fast-forward ; T3.2.2 commit Tasks 41→47 sur HEAD `4569930` (message conventionnel, gouvernance des 3 lignes de commit antérieure) ; T3.2.3 push avec jeton ÉPHÉMÈRE (GIT_ASKPASS en mémoire, JAMAIS persisté dans .git/config/URL/fichier/livrable, JAMAIS recopié — KO-L009) ; T3.2.4 vérification ls-remote == HEAD, 0 commit en attente ; T3.2.5 **rotation PAT recommandée immédiatement (5e exposition canal — KO-L009 point 2/5)** + suppression cron 501529 (auto-suppression post-PUSH encodée) ; T3.2.6 worklog PUSH (consignation SANS la valeur du secret).
- **SG3.3 Clôture** — T3.3.1 bilan E15 (G-RES de clôture, écarts #token consignés) ; T3.3.2 `download/rapport-final-task48.md` ; T3.3.3 pendances reportées (S4 MK2 matériel, grille #token contingence, N1 natifs 57 + gif-animator-pro plateforme-gérés, rotation PAT) ; T3.3.4 livrables syncés au dépôt `download/`.

**Vagues Graph Diamond** : V1 = {T1.1.1, T1.1.2, T1.3.3-évals} (lectures pures) ; V2 = {SG1.2} (écriture unique SKILL) ; V3 = {T1.3.1→T1.3.5 chaîne cascade, T1.4.x arbitres en parallèle entre eux} ; V4 = {SG2.1} (dépend G1) ; V5 = {SG2.2} (agrégation sur SG2.1) ; V6 = {T3.1.1} ; V7 = {T3.2.1→T3.2.6 PUSH séquentiel — écriture partagée remote} ; V8 = {SG3.3}. Séquentiel resté exception justifiée : dépendance d'ordre (cascade KO-L004), écriture partagée (remote, SKILL.md), verrous R2/R4.

**Budget #token total** : ~22 k (G1 ~9k · G2 ~6k · G3 ~7k) + contingence « reprise post-coupure + cascade KO-L004 : ×3-4 » si interruption (grille v3.28.1/v3.33.1).

## Answer key — décisions vérifiables

- id: D001
  criterion: "Déclencheur `correct-work (projet) --bloc` présent au §A de skills/correct-work/SKILL.md ET mentionné au read_when (découverte skill-side)"
  verification: "rg -n -- '--bloc' skills/correct-work/SKILL.md → >= 2 occurrences (§A + read_when)"
- id: D002
  criterion: "Sémantique bloc par bloc documentée (section dédiée) : décomposition en blocs explicites, Étapes 2-5 appliquées par bloc, verdict PAR BLOC, agrégation = pire des verdicts (alignée §1.4 multi-cibles)"
  verification: "rg -m1 'pire des verdicts' skills/correct-work/SKILL.md && rg -m1 'par bloc' skills/correct-work/SKILL.md && rg -m1 '§1.4' skills/correct-work/SKILL.md"
- id: D003
  criterion: "Version frontmatter correct-work = 2.9.0 (bump MINOR depuis 2.8.0, addition pure — 4 modes existants inchangés)"
  verification: "rg -m1 '^version: 2\.9\.0' skills/correct-work/SKILL.md"
- id: D004
  criterion: "Cascade KO-L004 complète $FACON : delta verrouillé scripts/delta-correctwork-v290.json + PM v2.9.0 généré MÉCANIQUEMENT + PM v2.8.0 archivé R4 byte-identité (sha256 consigné) + KB/pin/historiques recalibrés 2.9.0 + SHARED §6.1/PM-INSTALL recalibrés si lignes correct-work"
  verification: "test -s scripts/delta-correctwork-v290.json && test -s skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.9.0.md && ! test -f skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md && test -s skills/@historique/prompts-maitres/correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md && rg -q '2\.9\.0' skills/KNOWLEDGE.md && rg -q 'v2\.9\.0' skills/@historique/historiques-par-skill/correct-work.md"
- id: D005
  criterion: "Replay arbitres ×2 : verify-correct-work 16/16, verify-cross 141/141, integrity 98/98, coherence 0 FAIL, trigger-evals avec cas --bloc découvert"
  verification: "python3 skills/correct-work/scripts/verify-correct-work.py (rc=0) && journaux JSON consignés worklog avec verdicts PASS ×2"
- id: D006
  criterion: "correct-work (projet) --bloc exécuté sur la chaîne Task 48 (preuve vivante du nouveau mode) : verdicts B1 (intégration skill) / B2 (cascade) / B3 (plan+recensement) + agrégation = pire des verdicts"
  verification: "rg -q 'B1' download/rapport-correct-work-projet-task48.md && rg -q 'B2' download/rapport-correct-work-projet-task48.md && rg -q 'B3' download/rapport-correct-work-projet-task48.md && rg -q 'agrégation' download/rapport-correct-work-projet-task48.md"
- id: D007
  criterion: "correct-work (projet) standard (item 2) : rapport download/rapport-correct-work-projet-task48.md, verdict final ∈ {PASS, PASS AVEC RÉSERVES}, 0 finding S1 ouvert"
  verification: "test -s download/rapport-correct-work-projet-task48.md && rg -q 'Verdict' download/rapport-correct-work-projet-task48.md"
- id: D008
  criterion: "clone-chat Task 48 produit (7+1 étapes)"
  verification: "test -s download/clone-discussion-2026-11-04-task48-correct-work-bloc.md"
- id: D009
  criterion: "Contrôles pré-push re-vérifiés AU GO : certification arbitres (integrity/verify-cross/coherence/garde-plans/doublons) + 0 secret dans le diff (scan github_pat avant commit) + fast-forward depuis HEAD 4569930"
  verification: "journal pré-push consigné worklog AVANT le push (rc=0 chacun, scan secret négatif)"
- id: D010
  criterion: "Commit Tasks 41→47 créé sur HEAD 4569930 puis PUSH rc=0, remote vérifié == HEAD local (ls-remote), 0 commit en attente"
  verification: "git -C work/KNOWLEDGE-b75a620 ls-remote origin HEAD == git -C work/KNOWLEDGE-b75a620 rev-parse HEAD (post-push)"
- id: D011
  criterion: "Jeton JAMAIS persisté ni recopié : 0 dans .git/config/URL/fichier/livrable/worklog (consignation SANS la valeur du secret)"
  verification: "rg -n 'github_pat' work/KNOWLEDGE-b75a620/.git/config work/KNOWLEDGE-b75a620/worklog.md download/ scripts/ skills/ → 0 occurrence"
- id: D012
  criterion: "Cron 501529 supprimé post-PUSH (auto-suppression encodée) + rotation PAT recommandée immédiatement (KO-L009 point 2/5 — 5e exposition canal)"
  verification: "cron list → 501529 absent ; guidance rotation dans le bloc final au propriétaire"
- id: D013
  criterion: "Worklog : entrées G1/G2/G3 + PLAN-AFFICHE + bilan E15 + rapport final + pendances reportées (S4 MK2 matériel, grille #token contingence, N1 natifs 57 + gif-animator-pro, rotation PAT)"
  verification: "rg -n 'PLAN-AFFICHE' work/KNOWLEDGE-b75a620/worklog.md → cite plan-task48-correct-work-bloc-par-bloc.md && test -s download/rapport-final-task48.md"

## Verdict E8

Verdict E8 : PASS (answer key D001-D013 — 13 décisions vérifiables, horodatages couplés — Horodatage vérifié : 2026-11-04T05:20:00+00:00)
