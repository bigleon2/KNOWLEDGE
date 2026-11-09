# Rapport de campagne de tests — Task 81 (G3, D005)

**Directive** : trace 1a1bcf4fecbf5f29, item 4 — « génère $FACON, puis effectue des tests $FACON2 fonctionnels et performances des éléments de mon écosystème créés ou modifiés dans cette discussion hier et aujourd'hui […] en suivant la chronologie de création/modification (tous les éléments qui vont être POUSSER, ainsi que les éléments dont leur création ou modifications dépendent, doivent aussi être testés) ».
**Exécution** : session web-ecef7f80, 2026-11-09 — harnais `skills/re-curation/scripts/protocole-test.py` **v1.2.1** (3 familles F1/F2/F3) + arbitres écosystème. **Verdict global : 15/15 éléments testés — 15 PASS (dont 1 avec écart consigné) · 0 FAIL.**

---

## 1. Chronologie hier (2026-11-08) — 7 éléments

| # | Heure | Élément (création/modification) | Tests exécutés | Verdict |
|---|-------|--------------------------------|----------------|---------|
| T1 | 18:09 | **Task 78 — gen-plan v3.41.0** (règle de sondage borné + cascade PM v3.41.0/SHARED v1.7.36/PM-INSTALL v1.9.13) | `--verifier gen-plan` : pointeurs references/ 15/15 · non-duplication 1024 o · **F1** 2 scripts 2 evals 0,035 s PASS · **F3** SAINES (5 sortantes · 23 entrantes · KB=3.41.0) · **F2** 30 696 o / 30,0 Kio INTERMÉDIAIRE (< 30 Kio seuil LOURD) | **PASS** |
| T2 | 18:26 | **Task 79 G2 — version-management v1.3.0 re-curé** (46,1→25,2 Kio, −45,4 %, 7 blocs R4) | `--verifier version-management` : pointeurs 7/7 · non-duplication · **F1** 1 script 2 evals 0,1 s PASS · **F3** SAINES (0/0 · KB=1.3.0) · **F2** 25 782 o / 25,2 Kio INTERMÉDIAIRE | **PASS** |
| T2b | 18:35 | **Task 74 CLOSE — livrables** (clone-chat 74, rapports) | présence : `clone-chat-session-web-ecef7f80-20261108-task74.md` ✓ | **PASS** |
| T2c | 18:40 | **Task 79 CLOSE — livrables** (clone-chat 79, rapport final, plan statuts) | présence : `clone-chat-session-web-ecef7f80-20261109-task79.md` ✓ | **PASS** |
| T3 | 19:17 | **Pendances 79 — SYNC-CONTEXT v1.5.7** (recalibrage inert) | citations ↔ corpus réel : GEN-PLAN v3.41.0 ×2 ✓ · CORRECT-WORK v2.11.0 ✓ · CLONE-CHAT v2.0.2 ✓ · REFACTOR-GUARD v1.8.1 ✓ · SHARED v1.7.36 ✓ · PM-INSTALL v1.9.13 ✓ · README v2.1.21 ✓ · **119 porteurs §0 confirmés mécaniquement** (grep -l 119) ; lag Task 80/81 = inert documenté → resync v1.5.8 au G4 (faille F-a associée) | **PASS** (lag documenté → G4) |
| T4 | 19:17→22:00 | **Task 80 + Task 81 G2 — protocole-test.py v1.2.0→v1.2.1 + re-curation v1.2.0→v1.2.1** | `--selftest` **14/14 ×2 idempotent rc=0** (v1.2.1 — évolution 13/13 [v1.2.0, Task 80] → 14 cas après correctif idempotence POST posé sur preuves réelles iphone19 [Task 81 G2]) + `--verifier re-curation` : pointeurs · non-duplication · **F1** 3 scripts 2 evals 0,261 s PASS · **F3** SAINES (2 sortantes · KB=1.2.1) · **F2** 19 449 o / 19,0 Kio INTERMÉDIAIRE | **PASS** |
| T5 | 20:42 | **Task 80 — preuves baselines ×4** | `download/protocole-test-{gen-plan,version-management,iphone19,re-curation}.json` : structure complète (nature/protocole/baseline/contrats) · familles 3/3 partout · verdicts : gen-plan **GO** (v1.2.0) · version-management **GO** (v1.2.0) · iphone19 **POST MAINTIEN** (v1.2.1 — ré-ancrée Task 81 G2, runs 1-6) · re-curation **POST MAINTIEN** (v1.2.0, Task 80 G3) | **PASS** |
| T6 | 20:46 | **Task 80 CLOSE — livrables + secrets** | `clone-chat-session-web-ecef7f80-20261109-task80.md` ✓ + rapports CW --bloc présents ✓ + **scan jeton complet : 0 occurrence** (dépôt + profil + worklog — grep `github_pat_11AJSTJXQ0…` complet) | **PASS** |

## 2. Chronologie aujourd'hui (2026-11-09) — 6 éléments

| # | Élément (création/modification) | Tests exécutés | Verdict |
|---|--------------------------------|----------------|---------|
| T7 | **Task 81 G1 — iphone19 v0.12.0** (règle absolue 15 + QC 14, ajouts purs) | règle 15 en texte : SKILL.md ×4 · PM source ×5 ✓ · QC 14 ×5 ✓ · description frontmatter verbatim (« ne jamais inventer et rester fidèle à l'image d'origine (visage, …) ») ✓ · contrats intacts (ajouts purs : règles 1-14 · R1-R19 · G1-G7 · QC 1-13 — auto-audit §11) | **PASS** |
| T7b | **Task 81 G2 — re-curation progressive disclosure iphone19** (55 645 → 40 430 o, −27,3 %, 6 blocs R4 references/) | PRE GO v0.12.0 [journal v1.2.1 : run 1 avant=55 645] · POST ×2 **MAINTIEN ×2 rc=0** (runs 5-6 reprise : COHÉRENT · FONCTIONNEL · OPTIMISÉ · INTERACTIONS SAINES · PERF STABLE — empreinte interactions identique) · **R4-INTÈGRE 6/6** (`scripts/task81-verif-r4-iphone19.py` : SHA provenance == SHA references/ == SHA PM source byte-identité, 19 778 o) · `--verifier iphone19` **PASS** (pointeurs 6 · non-duplication · F1 2 evals · F3 SAINES 2 sortantes · KB=0.12.0) · check-recuration **C1-C3 PASS · C4 ÉCART CONSIGNÉ** | **PASS avec écart C4 consigné** |
| T8 | **Dépendances de tout ce qui est POUSSÉ** (5 arbitres + corpus + pipeline) | verify-cross **100,0 %** (0 WARN · 0 ERR) · answer-key-checker **16/16** · doublons **0** (281 uniques) · interactions **55/55 PASS STRICT** · integrity **112/112 PASS manifeste écrit** (pins re-curation 1.2.1 + iphone19 0.12.0 alignés) · corpus PM `--check` **4/4 COHERENT** (GEN-PLAN v3.41.0 · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1) · pipeline miroir **54/54 SHA-256, 0 divergence, garde R2** (même passe G2 — version-management présent, anti-disparition) | **PASS** |
| T8b | **Réinstallation locale** (directive reprise, ×2 rejouées) | eco_install_pipeline rc=0 ×2 — 54/54, 0 divergence, R2 OK, archive round-trip v2.2 ; volatilité profil résorbée (gen-plan vide + version-management absent à l'ouverture — récidive plateforme documentée Tasks 56/72/75/79/81) | **PASS** |
| T8c | **Archive d'intégrité dépôt** | rescellée v2.2 ×2 (hôte+dépôt) — corpus 9/9 byte-identique round-trip ; piliers retirés PAR CONCEPTION 2026-10-23 (RETRAITS_SANCTIONNES task21-f2, aucune perte — l'arbitre ne gate que sur n_pil_ko==0) | **PASS** |
| T9 | **Artefacts du jour + présent rapport** | présent rapport (chronologie tracée, verdicts par élément F1/F2/F3, métriques) + projection dépôt | **PASS** |

## 3. Failles détectées et corrections (max 2 rounds — 0 round consommé au-delà de l'intra-passe)

| Faille | Détection | Correction | Statut |
|--------|-----------|------------|--------|
| **F-a** — worklog DÉPÔT stale (1 806 lignes vs profil ; suites 72-75 non synchronisées) | E1-RES ouverture Task 81 | extinction G4 (worklog dépôt ← profil + suites du jour) avant PUSH | **→ G4 (planifiée)** |
| Idempotence verdicts POST (run 2 DÉRIVE fausse sur baseline ancrée) | preuves réelles iphone19, run 2 | harnais **v1.2.1** : re-jeu = NON-RÉGRESSION (`apres <= avant`), réduction stricte au 1er POST ; selftest 14/14 ×2 | **CORRIGÉE (intra-G2)** |
| Scellé archive hôte ≠ dépôt (le pipeline rescelle l'archive hôte, l'arbitre contrôle celle du dépôt) | integrity 111/112 (corpus 8/9) reprise | rescellage dépôt dédié `task21-f2-rebuild-archive.py` (côté dépôt) → 112/112 ; leçon consignée worklog suite 78 | **CORRIGÉE (intra-G2) — leçon consignée** |
| C4 seuil LOURD résiduel iphone19 (39,5 Kio > 30 Kio) | check-recuration P7 | **ÉCART CONSIGNÉ** (non-évitabilité mesurée : contrats ≈ 12,5 Kio + cœur par-mission ≈ 18 Kio ⇒ sub-LOURD = externaliser grille ANALYSE + moteur R1-R19 = dégradation par-mission refusée ; marge nulle ; re-ancrage v1.0.0 re-franchirait le seuil) — l'OPTIMISÉ du protocole P5 demeure satisfait (−27,3 % réel) | **CONSIGNÉE (écart D004, précédent écart D006 Task 78)** |
| Volatilité profil (gen-plan vide + version-management absent à l'ouverture — récidive) | garde n°9 ouverture | réinstallations ×2 rc=0 54/54 + garde anti-disparition pipeline | **Résorbée (plateforme — récidive documentée)** |

## 4. Métriques de performance (F2, mesurées)

- **gen-plan** : 30 696 o / 30,0 Kio (INTERMÉDIAIRE, sous seuil LOURD) — F1 0,035 s.
- **version-management** : 25 782 o / 25,2 Kio (INTERMÉDIAIRE) — F1 0,1 s.
- **re-curation v1.2.1** : 19 449 o / 19,0 Kio (INTERMÉDIAIRE) — F1 0,261 s (3 scripts exécutés).
- **iphone19** : 55 645 → **40 430 o (54,3 → 39,5 Kio, −27,3 %)** — LOURD assumé (écart C4) ; #token estimés 13 911 → **10 107** (convention octets/4 : 55 645/4 = 13 911 · 40 430/4 = 10 107 — **−3 804 par chargement**) ; F1 0 s (2 evals, 0 script embarqué) ; PERF STABLE PRE/POST (tolérance ×1,5 + 0,5 s).
- **R4 déplacé iphone19** : 19 778 o en 6 blocs byte-identiques (preuve R4-INTÈGRE 6/6).

## 5. Bilan

- **15/15 éléments PASS** (1 avec écart consigné) — 0 FAIL — 0 secret sur disque (jeton complet : 0 occurrence dépôt + profil).
- Chaîne PUSH prête : les 3 commits hérités + les commits du jour dépendent tous d'éléments testés PASS (T8 dépendances 5/5 arbitres + corpus 4/4 + miroir 54/54).
- Failles : 2 corrigées intra-passe (idempotence POST v1.2.1 ; scellé archive dépôt), 1 écart consigné (C4 — justification mesurée), 1 planifiée G4 (F-a worklog dépôt — extinction avant PUSH), 1 résorbée (volatilité profil, récidive plateforme).

*Généré par Task 81 G3 (D005) — harnais protocole-test v1.2.1, session web-ecef7f80, 2026-11-09.*
