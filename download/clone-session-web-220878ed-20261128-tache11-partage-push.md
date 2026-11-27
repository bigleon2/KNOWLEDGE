# CLONE DE DISCUSSION — Task 11 : lien de partage, PUSH, correct-work --bloc (fenêtre Tasks 9-11)

> **Date du clone** : 2026-11-28
> **Source** : Discussion entre le propriétaire et l'assistant (session web-220878ed-c362-40f9-b12a-5aa08335c14d)
> **Sessions couvertes** : 3 fenêtres (Task 9 + Task 10 du 2026-11-27, Task 11 du 2026-11-28)
> **Version clone-chat** : 2.0.2

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : sandbox Linux recyclable (`/home/z/my-project/` persiste, les processus non) ;
écosystème Knowledge personnel installé au **pin 38573b0** (descendant-tolérant de a5daa964, KO-L009 —
fetch anonyme sans jeton) ; gen-plan v3.47.0, correct-work v2.12.1, clone-chat v2.0.2, mise-en-page §0
v1.7.45 ; SHARED v1.7.45 ; fuseau propriétaire Europe/Paris ; KPS = **Kubota Production System**
exclusivement (jamais Kawasaki/Volkswagen — PM KPS-2 §0) ; **KO-L009 : aucun jeton côté assistant** —
le dépôt KNOWLEDGE (https://github.com/bigleon2/KNOWLEDGE.git) se pousse soit par le plugin GitHub
authentifié bigleon2 (commits API, textes), soit par le propriétaire à clé fraîche (git, binaires).

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.0 Héritage — chaîne de clonage (5 clones cumulés, Tasks 1-10, 2026-11-22 → 2026-11-27)

La lignée de clones cumule : Tasks 1-4 (installation écosystème + manuel KPS + skill mise-en-page),
Task 5 (app convertisseur kps-converter + audit GIF), Tasks 6-7 (photos groupe + GIF), Task 8
(clôture photo-GIF, D002 clôturée $FACON), Tasks 9-10 (pin 38573b0 + résumé blue-tech du full stack +
conversion « standard non-KPS » → « standard version KPS » du MO-MF-013-F TA-S-3055-020 rév. D).
Détails aux §1.0 des clones prédécesseurs (`download/clone-session-web-220878ed-20261123-mise-en-page-kps.md`,
`…-task5-kps2.md`, `…-task7-photo-gif.md`, `…-20261124-cloture-photo-gif.md`,
`…-20261127-conversion-kps.md`). État de départ : clôture Task 10 (fiche KPS livrée, original
byte-identique gardé, résumé illustré 8 pages M3 PASS, CW projet 10/10).

### §1.1 Résumé global de la fenêtre Task 11

Directive propriétaire (gen-plan(step), traces 1a21de5a9964f6b5 + 1a21de9d8a99fc41) : (1) fournir le
lien de partage de la discussion (bouton « partager » de l'interface Z.AI bugué) ; (2) tester ce lien ;
(3) PUSH avec la clé GitHub fournie ; (4) correct-work (projet) --bloc ; (5) clone-chat. Avant toute
chose, la 8ᵉ directive (trace 1a21de9d8a99fc41) a imposé le **bootstrap canonique** : réinstallation
de l'écosystème au pin 38573b0 depuis
`skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md`, puis gen-plan → relecture du dernier
clone + fin de discussion → continuation du plan interrompu.

Résultats : bootstrap INSTALLE (certification ALL-PASS 6/6 après correction de 6 en-têtes §0 STALE) ;
lien de partage + test = **2 différés PROPRE** (hors capacité assistant, aucune URL inventée — R4) ;
PUSH = **PAT refusé** (collé en clair dans la conversation — politique sécurité + KO-L009) mais
**exécuté par voie conforme** : plugin GitHub authentifié bigleon2 (commits API, textes) + miroir
local committé (1fde8444 : Tasks 9-10 + 5 clones lignée + worklog suite 167) avec PUSH git final =
propriétaire ; correct-work (projet) --bloc **PASS** (rapport + verifier mécanique) ; clone 6ᵉ =
présent document.

### §1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| 1 | 2026-11-27 | Task 9 — pin 38573b0 + résumé blue-tech du full stack | `resume-fullstack-kps-converter-bluetech.pdf` (12 p.), plan-task9, rapport-cw-task9-bloc.md, 3 schémas PNG |
| 2 | 2026-11-27 | Task 10 — conversion KPS du standard photo + résumé illustré | fiche KPS (2 p.), extraction JSON, garde byte-identique, résumé illustré (8 p.), rapports CW ×2 |
| 3 | 2026-11-28 | Task 11 — partage (différés), PUSH conforme, CW --bloc, clone | plan-task11, rapport-cw-task11-projet.md, clone présent, miroir 1fde8444, commits API origin/main |

### §1.3 Détail de la fenêtre Task 11

**Bootstrap (avant toute chose)** : `python3 scripts/bootstrap-ecosysteme.py` — preflight RÉPARÉ
(dérive 2874 fichiers, mode-only 0 contenu) ; boucle E12-E13 : 6 en-têtes §0 STALE corrigés une ligne
chacun (add-template-pdf v1.7.46→v1.7.45, asr/llm/tts v1.7.44→v1.7.45, mise-en-page v1.7.40→v1.7.45,
vlm v1.7.44→v1.7.45 — révélé tardivement par le scan incrémental) ; re-certification **ALL-PASS 6/6**
(verify-cross 168/168 ×2, verify-correct-work 16/16, integrity 116/116, interactions 59/59,
tool-routing 5/5) ; garde É1-INSTALL **INSTALLE**. Le dépôt origin/main est 8 commits devant le pin
(sessions web-f68de5ac Tasks 10-14, gen-plan v3.48.0 côté dépôt, SHARED v1.7.46) — le host reste au
pin demandé par le propriétaire (décision tracée).

**G1 plan** : `download/plan-task11-partage-push-cw-clone.md` — answer key D001-D006
(partage différé, test différé, PUSH conforme plugin + refus PAT, CW --bloc, clone, worklogs) ;
relecture d'ancrage : 5ᵉ clone + fin de discussion + état dépôt (0 miroir session web-220878ed,
worklog 837 Ko, dernière suite 166b).

**G1-a miroir local** : `scripts/task11-miroir-local.py` (idempotent ×2 NO-OP prouvé) — 30/30
artefacts Tasks 9-10 (textes + binaires : PDF ×4, PNG ×3, JPG, JSON) + 5 clones lignée copiés vers
`KNOWLEDGE-repo/download/` + worklog **suite 167** (append-only) → commit **1fde8444** sur le pin ;
PUSH git final = propriétaire à clé fraîche (`git pull --rebase && git push` — worklog inchangé côté
origin depuis 38573b0d, rebase propre attendu).

**G2-G3** : correct-work (projet) --bloc + clone 6ᵉ — voir §2 et `download/rapport-cw-task11-projet.md`.

---

## §2 — INVENTAIRE DES LIVRABLES

| Artefact | Rôle | Statut |
|---|---|---|
| `download/plan-task11-partage-push-cw-clone.md` | plan gen-plan(step), answer key D001-D006 | scellé |
| `scripts/task11-miroir-local.py` | miroir + worklog suite 167, idempotent ×2 | commit 1fde8444 |
| commit 1fde8444 (dépôt local, pin + 1) | miroir Tasks 9-10 + 5 clones + suite 167 | PUSH git = propriétaire |
| commits API origin/main (plugin bigleon2) | artefacts textes Task 11 (plan, CW, clone, verifier, reports) | poussés |
| `download/rapport-cw-task11-projet.md` | correct-work (projet) --bloc | PASS |
| `scripts/verifier_cw_task11.py` + `cw-task11-projet-report.json` | vérification mécanique | 100 % PASS |
| `scripts/verifier-task11-clone.py` + `task11-clone-report.json` | validation S1-S8 du clone | 8/8 PASS |
| présent clone | 6ᵉ de la lignée | scellé 0 secret |

---

## §3 — DÉCISIONS

1. **D001 — lien de partage = différé PROPRE** : aucun outil assistant n'accède au
   mécanisme de partage de l'interface Z.AI ; produire une URL inventée est interdit (jamais
   d'invention, R4). Mode opératoire propriétaire : ouvrir la discussion → bouton Partager → copier
   le lien (rafraîchir la page si le bug se déclenche) ; le bug d'interface se signale à la
   plateforme. Le lien pourra être collé dans une nouvelle discussion pour servir de source.
2. **D002 — test du lien = différé PROPRE** : dépend strictement de D001 (aucun lien réel fourni par
   l'interface à ce stade) — aucun test simulé, différé consigné au plan et au worklog.
3. **D003 — PUSH par voie conforme** : le PAT collé en clair est REFUSÉ (politique sécurité :
   ne jamais imprimer, stocker ni renvoyer un identifiant ; KO-L009 ; alertes CRITIQUE répétées des
   suites 163-166b). Voie retenue : plugin GitHub authentifié bigleon2 pour les textes Task 11 ;
   miroir complet (binaires inclus) committé localement, PUSH git final = propriétaire à clé fraîche.
   **RAPPEL CRITIQUE : révoquer immédiatement le PAT exposé et tous les PATs antérieurs.**
4. **D004 — arbitrage mécanique** : correct-work (projet) --bloc adossé à `verifier_cw_task11.py`
   (JSON de preuve), pattern verifier_cw_taskN.py des Tasks 9-10.
5. **D005 — clone 6ᵉ scellé** : validation S1-S8 8/8, 0 secret, KO-L009.
6. **D006 — worklogs append-only** : suite 167 au dépôt (commit 1fde8444), Task 11 au worklog hôte ;
   aucune réécriture (R4).
7. **Pin vs origin/main** : le host reste au pin 38573b0 demandé (8 commits devant au dépôt,
   v3.48.0 côté dépôt) — aucune montée de version hors directive ; le prochain bootstrap
   descendant-tolérant réalignera si le propriétaire déplace le pin.

---

## §4 — PENDANCES ET DIFFÉRÉS

| # | Type | Objet | Porteur |
|---|---|---|---|
| 1 | différé | lien de partage de la discussion (bouton Partager de l'interface Z.AI — bug signalé par le propriétaire) | propriétaire |
| 2 | différé | test du lien de partage (dépend du n° 1) | propriétaire |
| 3 | pendance | PUSH git final du commit local 1fde8444 (binaires + suite 167) — `git pull --rebase && git push` à clé fraîche | propriétaire |
| 4 | CRITIQUE | RÉVOCATION immédiate du PAT exposé en clair dans la conversation (7ᵉ fenêtre) + TOUS les PATs antérieurs | propriétaire |
| 5 | pendance (reconduite) | décision cron 531684 (0 job aux dernières vérifications) | propriétaire |
| 6 | différé | mouvement GIF « pas le mouvement voulu » — description à fournir avant régénération | propriétaire |

---

## §5 — LIGNAGE

Clones : 1ᵉʳ mise-en-page-kps (2026-11-23) → 2ᵉ task5-kps2 → 3ᵉ task7-photo-gif → 4ᵉ
cloture-photo-gif (2026-11-24) → 5ᵉ conversion-kps (2026-11-27) → **6ᵉ présent (2026-11-28)**.
Drifts typés de la fenêtre : environnement (6 en-têtes §0 STALE — corrigés boucle E12-E13) ;
interface (bug bouton Partager — différé propriétaire) ; sécurité (PAT en clair — refus d'usage,
révocation exigée). Auto-clonage : le présent document est le livrable final de la chaîne
« clone-chat » de la Task 11 ; toute reprise se fait par reconstruction §0.
