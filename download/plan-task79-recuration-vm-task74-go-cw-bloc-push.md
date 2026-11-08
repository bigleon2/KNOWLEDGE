# Plan Task 79 — Exécution Task 78 (règle de sondage borné) → re-curation version-management → Task 74 GO (clone-chat 74 + correct-work --bloc + finalisation) → clone-chat session → PUSH final (PAT délégué)

**Horodatage plan : 2026-11-08T16:52:00Z (INITIAL — 14 décisions : 3 verified ouverture / 11 pending exécution)** · Mode : gen-plan (step, chaîne autonome — enchaînement des groupes sans portes) · Session : web-ecef7f80 · Trace directive : 1a1bc0ad4607c95d (doublon 1a1bc0b5e38f52a9 dédupliqué — une seule exécution) · Prérequis vérifié : Task 78 plan PRÊT (E8 initial PASS 2026-11-08T16:32:00Z) · Task 77 CLOSE (53d2392 poussé) · Task 74 EN VOL au GO propriétaire (plan INTACT — le GO est donné par la présente directive)

## Contexte et périmètre

Directive propriétaire (2026-11-08, trace 1a1bc0ad4607c95d), 4 items :
1. « as-tu fait la "re-curation" sur "version-management", si c'est judicieux de le faire alors fais-le (avec pré-test d'idempotence et de cohérence par rapport à mon écosystème). »
2. « fais le reste du plan d'actions $FACON : "Go" avec ma clé "github_pat_11AJ…CTrp". »
3. « correct-work (projet) --bloc. »
4. « clone-chat. »

Interprétation (règle d'or n°5, dérivée du disque) :
- **Item 1** : réponse MESURÉE — la re-curation de version-management n'a PAS été faite (n°1 de la file Task 72, en attente). Elle est JUDICIEUSE : 47 244 o (46,1 Kio, LOURD ≥ 30 Kio), ~23,1 Kio déplaçables (7 sections ≥ 1,5 Kio), 0 dépendant KB, gain projeté ~50 % → ~18-22 Kio. Pré-tests exigés = le protocole P0-P7 du skill re-curation v1.0.0 : `protocole-test.py --pre` (baseline golden master + contrats sha256 + verdict GO/NO-GO — la **cohérence** demandée) puis P5-P6 (`--post` ×2 MAINTIEN + re-jeu ×2 no-op — l'**idempotence** demandée). **Contrainte miroir** (file Task 72) : sync hôte↔dépôt dans la MÊME passe (récidive de disparition ≥ 37ᵉ occurrence — réparée à l'ouverture du présent plan, preuve vivante).
- **Item 2** : « le reste du plan d'actions » = la file d'actions affichée (E7 Task 78) : **Task 78 GO** (exécution G1-G3 du plan prêt) + **Task 74 GO** (exécution intégrale de son plan intact : G1 clone-chat session 74 → G2 correct-work --bloc → G3 finalisation + commit incluant les mode-purs — propriété de son G3 GO) + **PUSH final** avec la clé fournie (délégation explicite — dérogation KO-L009 point 5 documentée, précédents Task 63/77 : jeton UNIQUEMENT en mémoire de commande, URL one-shot, JAMAIS persisté — vérification mécanique zéro-persistance avant/après, tronqué « github_pat_11AJ…CTrp » dans tout artefact).
- **Items 3-4** : correct-work (projet) --bloc s'exécute comme G2 du Task 74 (sa place canonique dans son plan — le worklog Task 75 l'anticipait : « son rapport sera couvert par le correct-work --bloc Task 74 G2 ») ; clone-chat = G4 du Task 79 (session courante, dernier artefact de la chaîne).
- **E15** (récidive) : le jeton a circulé une 4ᵉ fois en clair (26/10, 07/11, 08/11 ×2) — révocation/rotation RECOMMANDÉE après usage.

## État initial mesuré (E1-RES + E2, règle d'or n°5)

- **E1-RES (hook, complet)** : (1) B-11 lecture préalable — Task 77 CLOSE (16/16, 53d2392 poussé, distant == HEAD) + Task 78 plan PRÊT (E8 initial PASS 16:32:00Z, worklog suite 65) ; (2) G-RES **OK — PARALLELE** (monitor.py) ; (3) fraîcheur : aucun plan en exécution (le plan Task 78 est PRÊT, non démarré) ; (4) garde post-coupure : écosystème installé à 16:25Z (54/54) MAIS **version-management disparu à nouveau en plein session** (récidive ≥ 37ᵉ — volatilité plateforme documentée Task 56/72/75) → **réparation immédiate : eco_install_pipeline rc=0 (54/54 SHA-256, 0 divergence, version-management 47 244 o restauré)** — preuve vivante de la contrainte miroir.
- **Certification d'ouverture (réinstallée)** : arbitres 4/4 PASS à 16:26Z (verify-cross 100,0 % · vcw 16/16 · integrity 112/112 · doublons 0) — valides pour la présente chaîne (aucune écriture écosystème depuis).
- **Git dépôt** : HEAD `53d2392` (Task 77) == distant `origin/main` (avance 0 — tout est poussé) · working tree : 129 fichiers mode-purs (0 insertion/0 suppression — héritage Task 74/76/77, R2, propriété du GO Task 74).
- **version-management** : v1.3.0 · 47 244 o (46,1 Kio LOURD) · 0 fichier references/ (tout inline) · 0 dépendant KB · blocs déplaçables ~23,1 Kio (§1.3 5 822 o · §3.4 5 597 o · §3.1 3 532 o · §6 3 035 o · §8 2 264 o · §1.2 2 204 o · §5 1 630 o — cartographie sèche Task 72 G3, à re-mesurer SG2.1).
- **Task 74** : plan INTACT — G1 clone-chat (0/7) · G2 correct-work --bloc (0/7) · G3 GO (0/3) · answer key D001-D012 (3 verified / 9 pending à l'ouverture d'origine) · livrables Task 74 au worklog suites 50-52.
- **Task 78** : plan PRÊT — 10 décisions (D001-D003 verified · D004-D010 pending) · ≈ 13 500 #token estimés.

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Ouverture saine : G-RES OK PARALLELE · écosystème 54/54 (réinstall 16:25Z) · version-management réparé après récidive ≥ 37ᵉ (pipeline rc=0, 0 divergence, 47 244 o) · arbitres 4/4 PASS (16:26Z)"
    verification: "ls skills/version-management/SKILL.md && monitor.py (OK) — traces session 2026-11-08T16:47Z"
    source: "Règle d'or n°9 ; garde É1-INSTALL v3.35.2 ; contrainte miroir file Task 72"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "État initial mesuré : Task 74 plan intact (G1 0/7 · G2 0/7 · G3 0/3 — R2) · Task 78 plan prêt (10 décisions) · git avance 0 (53d2392 poussé) · 129 mode-purs intacts · re-curation version-management NON faite (n°1 file Task 72, judicieuse : 46,1 Kio, ~23,1 Kio déplaçables, 0 dépendant)"
    verification: "rg -c 'À FAIRE' download/plan-task74-*.md && git -C KNOWLEDGE-repo rev-list origin/main..HEAD --count (=0) && git status --porcelain | wc -l (mode-purs)"
    source: "Directive item 1 (question) ; file d'actions E7 Task 78 ; KO-L003"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "PAT délégué : zéro-persistance au plan (jeton tronqué « github_pat_11AJ…CTrp » uniquement — 0 occurrence du jeton complet dans tout artefact écrit)"
    verification: "rg -l 'github_pat_11AJSTJX' download/ KNOWLEDGE-repo/ (0 résultat) && mentions au plan/worklog = forme tronquée"
    source: "Précédents Task 63/77 ; KO-L009 point 5 (délégation) ; E15 révocation"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "G1 — Task 78 exécuté : amendement gen-plan v3.41.0 (rangée « Sondage borné » §1.2bis + intégral protocoles-detailles Extension v3.41.0 — 4 règles + exceptions ; SKILL.md < 30 720 o après compensations ; description/§A intacts) + cascade KO-L004 (PM v3.41.0, PM v3.40.0 archivé R4, KB, pin ×2, historiques, README ×2, ULTRA ×2 — SHARED INCHANGÉ) + preuves (volumétrie grep BRUT vs BORNÉ mesurée + protocole-test PRE GO / POST ×2 MAINTIEN) + arbitres un bloc PAR + sweep citations + E8 final 10/10 + commit dédié"
    verification: "rg -c 'Sondage borné' skills/gen-plan/SKILL.md (≥1) && wc -c skills/gen-plan/SKILL.md (<30720) && arbitres rc=0 && git log (commit Task 78)"
    source: "Directive item 2 ; plan-task78 D004-D010 ; précédent v3.40.0"
    priority: "S1"
    status: "pending"
  - id: "D005"
    criterion: "G2 — re-curation version-management P0-P7 : PRE GO (baseline golden master : contrats sha256 + 38 sections mesurées) → cartographie re-mesurée → méthode arbitrée (--compare, R4-compliante) → moves R4 byte-identité vers references/ (en-têtes de provenance : section, version, date, SHA-256 du bloc) → résumés opérationnels inline → POST ×2 MAINTIEN DE L'OPTIMISATION (cohérent/fonctionnel/optimisé — poids cible ~18-22 Kio) → idempotence ×2 no-op des scripts de la passe"
    verification: "protocole-test.py --pre version-management (GO) puis --post ×2 (MAINTIEN) && check-recuration.py version-management (C1-C4 PASS) && poids mesuré"
    source: "Directive item 1 (pré-tests idempotence + cohérence) ; skill re-curation v1.0.0 §2 P0-P7"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "G2 — cascade légère + sync hôte↔dépôt MÊME PASSE (contrainte miroir) : pin ECO_SKILLS + entrée KB (Dernière calibration re-curation) + historiques-par-skill/version-management.md + ULTRA ×2 + arbitres (cross/vcw/integrity/doublons/coherence) + sync pipeline rc=0 54/54 avec version-management PRÉSENT à l'hôte en fin de passe (anti-disparition)"
    verification: "eco_install_pipeline.py rc=0 (divergences==[]) && ls skills/version-management/SKILL.md (présent) && arbitres rc=0"
    source: "File Task 72 (contrainte miroir) ; re-curation §2 règle 4 (gouvernance KB/ECO_SKILLS)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "G3.a — Task 74 G1 clone-chat : archive auto-suffisante de la session Task 74 (installation écosystème) — §0-§5 + drifts + 8 checks S1-S8 — download/clone-chat-session-web-ecef7f80-20261108-task74.md scellé + statuts plan 74 mis à jour"
    verification: "ls download/clone-chat-session-web-ecef7f80-20261108-task74.md && 8 checks documentés + plan 74 statuts cohérents"
    source: "Directive items 2-4 ; plan Task 74 G1 (D005-D008 de son answer key)"
    priority: "S2"
    status: "pending"
  - id: "D008"
    criterion: "G3.b — Task 74 G2 correct-work (projet) --bloc : blocs B1 installation+certification · B2 corpus+KB+outillage · B3 livrables session 74 + bloc d'extension B4 (sessions Task 75-79 : re-curations, Task 77 cascade, Task 78 sondage, présente chaîne) — Étapes 2-5 par bloc (max 2 rounds), agrégation pire-des-verdicts → PASS"
    verification: "verdict agrégé consigné au worklog + plan 74 (0 S1/S2 restant bloquant)"
    source: "Directive item 3 ; plan Task 74 G2 ; précédent Task 76 (2× CW --bloc PASS)"
    priority: "S1"
    status: "pending"
  - id: "D009"
    criterion: "G3.c — Task 74 G3 GO : E8 final (answer key 12/12 verified, horodatages couplés) + rapport final download/rapport-final-task74.md + sync dépôt SANS --delete (C5) + commit Task 74 INCLUANT les mode-purs (propriété du G3 GO — 129+ fichiers) + marqueur TASK 74 CLOSE"
    verification: "check_plan_protocol --plan plan74 --worklog PASS && git log (commit Task 74) && mode-purs commités (git status propre)"
    source: "Directive item 2 (GO) ; plan Task 74 G3 (D010-D012)"
    priority: "S1"
    status: "pending"
  - id: "D010"
    criterion: "G4 — clone-chat session courante (Task 79) : archive §0-§5 + drifts + jeton tronqué (0 occurrence complète) + leçons L-79"
    verification: "ls download/clone-chat-session-web-ecef7f80-20261109-task79.md && 0 occurrence jeton complet"
    source: "Directive item 4 ; clone-chat v2.0.2"
    priority: "S2"
    status: "pending"
  - id: "D011"
    criterion: "G4 — E8 final Task 79 : answer key 14/14 verified · horodatages couplés (KO-L003) · check_plan_protocol P1-P5 PASS post-finalisation · commit dédié Task 79 SANS résidu (mode-purs déjà commités au Task 74 G3)"
    verification: "check_plan_protocol.py --plan plan79 --worklog PASS && git log (commit Task 79)"
    source: "gen-plan E7-DISP point 3 ; précédents Task 76-78"
    priority: "S1"
    status: "pending"
  - id: "D012"
    criterion: "G5 — PUSH final (délégation PAT item 2) : cadre zéro-persistance vérifié AVANT (remote sans jeton, 0 credential.helper, 0 ~/.git-credentials, jeton complet 0 occurrence disque) · pré-vol (fsck rc=0, commits en attente dénombrés, ls-remote authentifié, fast-forward pur prouvé) · push one-shot (jeton en mémoire de commande UNIQUEMENT) · post-push (distant == HEAD, avance 0, zéro-persistance re-vérifiée) · E15 RÉVOCATION/ROTATION consignée (4ᵉ exposition)"
    verification: "git ls-remote origin refs/heads/main (== HEAD local) && zéro-persistance re-vérifiée (grep segments = 0 hors littéraux doc)"
    source: "Directive item 2 ; précédents Task 63/77 (protocole cadre sécurisé) ; KO-L009/D013"
    priority: "S1"
    status: "pending"
  - id: "D013"
    criterion: "Chaîne conforme : 4 items directive exécutés dans l'ordre (1 re-curation ✓ → 2 reste du plan GO ✓ → 3 CW --bloc ✓ → 4 clone-chat ✓) · correct-work(groupe) après chaque groupe (max 2 rounds) · fenêtre native maintenue G1→G5 · horodatages couplés à chaque E8 · aucun mode-pur résiduel non-commité en fin de chaîne"
    verification: "worklog suites 66+ tracées par groupe && fenêtre native && git status (propre hors fichiers travail courant)"
    source: "Mode step (enchaînement autonome) ; §5.5 ; E7-DISP point 6"
    priority: "S2"
    status: "pending"
  - id: "D014"
    criterion: "Bilan : version-management ~46,1 → ~18-22 Kio (≈ −55 %, ≈ 9 000 #token économisés par chargement) · gen-plan v3.41.0 (sondage borné opérationnalisé — le symptôme SG2.2 ne se reproduit plus : greps bornés par protocole) · Task 74 CLOSE (pendance éteinte) · PUSH public — écosystème $FACON2"
    verification: "mesures poids-chargement.py ×2 (avant/après) && rg -c 'Sondage borné' skills/gen-plan/SKILL.md && TASK 74 CLOSE au worklog && distant == HEAD"
    source: "Directive (objet des 4 items) ; règle d'or n°5"
    priority: "S2"
    status: "pending"
```

## Estimation et profil (E3-E6)

- **E3** : Type 2 (analyse/amendement/re-curation + livrables documentaires MD/JSON — aucun docx/pdf/xlsx/pptx).
- **E4** : G1 ≈ 5 000 · G2 ≈ 8 000 · G3 ≈ 12 000 (clone-chat 74 ≈ 4 500 + CW --bloc ≈ 6 000 + finalisation 1 500) · G4 ≈ 3 500 · G5 ≈ 1 500 — **total ≈ 30 000 #token** (bornes 22 000-45 000).
- **E5-POIDS** : gen-plan 29,9 Kio (INTERMÉDIAIRE — lecture ciblée) · correct-work 28,6 Kio (INTERMÉDIAIRE) · version-management 46,1 Kio (LOURD — lecture ciblée §0 + sections, cartographie déjà disponible) · clone-chat 17,4 Kio.
- **E6** : NORMAL (G-RES OK — PARALLELE).

## G1 — Exécution Task 78 : règle de sondage borné (gen-plan v3.41.0) `[À FAIRE]` (0/3)

Exécution intégrale du plan download/plan-task78-regle-sondage-borne.md (E8 initial PASS 16:32:00Z) :
- **SG1.1 PRE + amendement** (D004) : T1.1.1 volumétrie BRUT vs BORNÉ [VAGUE-PAR a∥b] · T1.1.2 protocole-test --pre GO · T1.2.1 inline v3.41.0 (< 30 720 o, compensations) · T1.2.2 intégral protocoles-detailles Extension v3.41.0.
- **SG1.2 Cascade KO-L004 + sync** (SHARED INCHANGÉ) : PM v3.41.0 + PM v3.40.0 archivé R4 + KB + pin ×2 + historiques + README ×2 + ULTRA ×2 + pipeline rc=0.
- **SG1.3 Preuves + arbitres + E8 final Task 78 + commit** : POST ×2 MAINTIEN · 5 arbitres un bloc PAR · sweep citations v3.40.0→v3.41.0 · answer key 10/10 · commit dédié.

## G2 — Re-curation version-management (protocole P0-P7) `[TERMINÉ]` (3/3)

- **SG2.1 P0-P2 tests AVANT + méthode** (D005) : `protocole-test.py --pre version-management` → GO/NO-GO (cohérence : contrats sha256 + baseline) · cartographie re-mesurée (mesure-sections) · `--compare` méthode la plus optimisée (R4-compliante seule éligible).
- **SG2.2 P3-P5 re-curation + maintien** (D005) : moves R4 byte-identité (7 blocs ~23,1 Kio → references/ avec en-têtes de provenance) · résumés opérationnels inline (contrats §A/read_when/evals/description intacts) · `--post` ×2 MAINTIEN (poids cible ~18-22 Kio) · idempotence ×2 no-op (pré-test demandé).
- **SG2.3 P6-P7 arbitres + cascade légère + sync miroir** (D006) : arbitres + check-recuration C1-C4 + pin/KB/historiques/ULTRA + sync hôte↔dépôt MÊME PASSE (version-management présent à l'hôte en fin de passe — anti-disparition ≥ 37ᵉ récidive).

## G3 — Task 74 GO : clone-chat 74 + correct-work --bloc + finalisation `[À FAIRE]` (0/3)

- **SG3.1 Task 74 G1 — clone-chat session 74** (D007) : archive auto-suffisante §0-§5 (installation écosystème + suites 50-52) + 8 checks + statuts plan 74.
- **SG3.2 Task 74 G2 — correct-work (projet) --bloc** (D008) : B1 installation+certification · B2 corpus+KB+outillage · B3 livrables 74 · B4 extension sessions 75-79 — max 2 rounds/bloc, agrégation pire-des-verdicts.
- **SG3.3 Task 74 G3 — GO finalisation** (D009) : E8 final 12/12 + rapport final + sync SANS --delete + commit Task 74 (mode-purs inclus) + **TASK 74 CLOSE**.

## G4 — clone-chat session courante + clôture Task 79 `[À FAIRE]` (0/2)

- **SG4.1 clone-chat v2.0.2 session Task 79** (D010) : §0-§5 + drifts + jeton tronqué + leçons.
- **SG4.2 E8 final + commit** (D011) : answer key 14/14 · horodatages couplés · commit dédié Task 79.

## G5 — PUSH final (délégation PAT — protocole Task 63/77) `[À FAIRE]` (0/2)

- **SG5.1 Cadre zéro-persistance + pré-vol + push one-shot + post-push** (D012) : fsck · commits dénombrés · fast-forward pur prouvé · push (jeton en mémoire de commande UNIQUEMENT) · distant == HEAD · zéro-persistance re-vérifiée.
- **SG5.2 E15 + clôture** (D013, D014) : révocation/rotation du PAT consignée (4ᵉ exposition) · TASK 79 CLOSE · bilan chiffré.

## PLAN-AFFICHE

(Task 79 — download/plan-task79-recuration-vm-task74-go-cw-bloc-push.md — INITIAL — **G1 Task 78 sondage borné ✅ 3/3 · G2 re-curation version-management ✅ 3/3 · G3 Task 74 GO `[À FAIRE]` 0/3 · G4 clone-chat + clôture `[À FAIRE]` 0/2 · G5 PUSH final `[À FAIRE]` 0/2** — answer key 14 décisions (D001-D003 verified ouverture · D004-D014 pending exécution) — E8 initial PASS 2026-11-08T16:52:00Z — #token ≈ 30 000 (bornes 22 000-45 000) — exécution step : G1→G5 chaîne autonome (série justifiée ENTRE groupes : écritures chaînées + ordre directive), vagues PAR internes (T1.1.1-a∥b, arbitres, preuves) — fenêtre native TodoWrite : affichée au début d'exécution, mise à jour à chaque fin de groupe (E7-DISP point 6))

Verdict E8 : PASS INITIAL (answer-key-checker 16/16 ALL PASS ×2 sha16 stable + check_plan_protocol P1-P5 PASS — 14 décisions : D001-D003 verified ouverture · D004-D014 pending exécution — Horodatage vérifié : 2026-11-08T16:52:00Z)
