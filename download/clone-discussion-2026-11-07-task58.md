# Clone de discussion — Task 58 (plancher dessin-technique v1.3.0 + compilation-windows) — 2026-11-07

> **Skill** : clone-chat v2.0.2 · **Session clonée** : web-c30e6506 (reprise de web-c30e6506 suites 9-11) · **Profil** : NORMAL · **Auto-suffisant** : ce document permet à une session héritière de reprendre sans le contexte de la discussion.

## §1 — Contexte et mission

**Task 58** (file d'attente §5 Task 60, directive « gen-plan (step): continue ») : exécution du plan `download/plan-task58-compilation-windows-plancher-dessin-technique.md` — 2 différés propriétaire : (G1) fenêtre de compilation Windows branche `test/compilation-windows` avec clé K3 ; (G2) plancher **dessin-technique ≥ 1.3.0** par évolution du skill (matérialisation du nœud C++ `trigo-euler` déclaré au registre inter-scripts v1.0.0, jamais installé depuis le recyclage) ; (G3) clôture canonique.

**Directives du tour** : 8ᵉ — exécution autonome du reste du plan (« gen-plan (step) » = TOUJOURS autonome, validation uniquement sur « gen-plan (step-ok) » — sémantique enregistrée) ; 9ᵉ — français exclusif (incident langue n°2, règle d'or n°6, jamais de dérive) ; 10ᵉ-13ᵉ — relire les **3 discussions d'origine** (VOSS COOLING `0d14e61c`, COOLING VOSS #2 `1de508c4`, Rasta Mouton `55afc1b5`) et intégrer **tout ce qui concerne les calculs mathématiques** que le skill dessin-technique doit intégrer, avec recherche dans les dossiers des projets.

**Généalogie reconstituée** : VOSS COOLING (07-13/10) = session d'origine DU SKILL (mission VOSS-C, v1.0.0 2026-10-13, croisée avec `skills/@historique/historiques-par-skill/dessin-technique.md`) → rendu joint 5c stochastique → COOLING VOSS #2 (22/10) = mission TRIGO-INTER-SCRIPTS (trigo-euler.cpp + inter-scripts v1.0.0 + bump v1.2.0→v1.3.0 — PERDUS au recyclage sandbox, inter-scripts seul survivant) → Rasta Mouton (25/10, livraison GIF — rien de mathématique) → Task 58 = reconstruction v1.3.0.

## §2 — Ce qui a été exécuté (chaîne G1→G3)

- **G1 (requalifié done-documenté)** : exécuté 2026-11-06 (run WF 42303936370 SUCCESS, branche 04accb8, artefact 1 758 544 o — plan-task59 §0) ; 5ᵉ recyclage sandbox a détruit les artefacts locaux volatils (L55-3) — D582-D584 done-documenté, jamais de travail jetable refabriqué.
- **G2-SG2.1** : `skills/dessin-technique/scripts/trigo-euler.cpp` (≈1500 L, C++17 std, 0 dépendance, mini-JSON ordonné) — 15 capacités + echo + daemon.stop ; modes one-shot/stdin/daemon ; NDJSON ; max_clients 8 saturation non-bloquante « daemon sature » ; déterminisme %.10g. Compilation registre EXACTE : `g++ -O2 -std=c++17 -pthread -Wall` → 0 warning. **2 rounds de correction** (T04 canonique.ellipse : matrice forme quadratique [[A,B/2],[B/2,C]], second membre +1 [F=−1], angle propre 0.5·atan2(B, A−C) ; warning degres).
- **G2-SG2.2** : preuves `tmp/mission-task58/trigo-node/` — selftest **15/15 ×2 byte-identique** ; harnais `preuves.py` **PASS 8/8 ×2** (P1-P8 : selftest, 15 op is_client, daemon+echo, concurrence 4×25=100/100 à 0,1-0,7 ms, saturation 8+1, daemon.stop propre, orchestrateur ×2 sha16 identiques, cas vivant joint 5c 44,9×35,2 profil+iso). **Piège découvert** : `subprocess.run(capture_output=True)` + daemon enfant rémanent → pipe stdout hérité jamais fermé → `communicate()` bloque — TOUJOURS redirection fichier pour lancer l'orchestrateur/harnais du nœud.
- **G2-SG2.3** : SKILL.md **v1.3.0** (description F6, §1.8, T7/T8, §2 stack C++ + exception N3, §3 inter-scripts, frontmatter complet) ; evals.json v1.3.0 **8 tests**.
- **G2-SG2.4** : cascade KO-L004 5 touches (KB v1.3.0 7/7, pin ECO_SKILLS 1.3.0, historiques 4 versions + sceaux v1.1.1 [git a988f51], ULTRA régénéré ×2 idempotent, archive v2.3 rescellée ×2) + résorptions de dettes héritées (sync §0 gen-plan/certification-complete ; **70 étiquettes §0 → SHARED v1.7.28** [dette Task 60 G4] ; version-management 19ᵉ disparition restauré).
- **G3** : correct-work (projet) **--bloc PASS 3/3** (17/17 checks) ; rapport final + RAPPELS OBLIGATOIRES ; présent clone.

## §3 — Décisions (D581-D588, 8/8 done)

D581 installation+plan (préalable) · D582-D584 compilation-windows done-documenté (requalification recyclage, preuves horodatées) · D585 nœud trigo-euler (contrat registre respecté à la lettre : 15 capacités, commande g++ exacte, preuves mécaniques) · D586 cascade 5 touches + certification ×2 arbres (110/110 hôte+miroir, coherence 53/29/0, vcw 16/16, plancher satisfait) · D587 --bloc PASS · D588 rapport final + rappels + clone.

## §4 — Bugs rencontrés et correctifs (4/4 cause+fix+résultat)

1. **T04 canonique.ellipse FAIL** (14/15 round 1) → cause : matrice de la forme quadratique passée avec B au lieu de B/2, second membre −1 au lieu de +1 (F=−1), angle propre avec 2B → fix : `eig2_sym(A, B/2, C)`, `Sv += ligne*1.0`, `0.5·atan2(B, A−C)` → 15/15 round 2 (même classe que les corrections d'origine T06/T13).
2. **Warning -Wall** (variable `degres` inutilisée) → intégrée en avertissement de réponse (« dérivée calculée en radians ») → compilation 0 warning.
3. **Blocage harnais P7** (timeout) → cause : pipe capture_output hérité par le daemon rémanent → fix : redirection fichier (`stdout=lf`) → harnais < 30 s, PASS 8/8.
4. **coherence FAIL ×2** (références vives 70 STALE + round-trip archive piliers) → causes : dette Task 60 G4 (étiquettes §0 jamais propagées à v1.7.28) + piliers touchés par la résorption → fix : 70 montées d'étiquette (R2) + archive re-rescellée → coherence 0 FAIL.

## §5 — Drifts (typés)

Langue : **0 drift** (français exclusif tenu toute la chaîne, 9ᵉ directive appliquée — le résumé de continuation chinois de la plateforme n'a pas dérivé la session). Périmètre : 3 résorptions de dettes héritées hors périmètre G2 (documentées, commits dédiés — jamais silencieuses). Version : registre inter-scripts v1.0.0 NON touché (contrat respecté — le nœud implémente, le registre déclare).

## §6 — Artefacts et état du disque (pour reprise)

- **Nœud** : `skills/dessin-technique/scripts/trigo-euler{.cpp,}` (source + binaire) — selftest `--selftest`, version `--version`.
- **Preuves** : `tmp/mission-task58/trigo-node/` (journal-preuves.json PASS 8/8 ×2, selftest-{1,2}.txt, run{1,2}/, joint-5c-{profil,modele-iso}.json, preuves.py, mini-plan.json).
- **Discussions d'origine extraites** : `tmp/mission-task58/discussions/discussion-{1,2,3}.{txt,json}`.
- **Skill** : `skills/dessin-technique/` v1.3.0 (SKILL.md 8 sections F1-F6, evals 8 tests, 5 scripts Python + nœud C++).
- **Livrables** : `download/rapport-final-task58.md`, `download/rapport-correct-work-bloc-task58.md`, le présent clone.
- **Miroir** : commits 00f9ca6 + e7d6bcb + 768bb3a + clôture (push distant = GO propriétaire, KO-L009).
- **Arbitres (état certifié ×2)** : integrity 110/110 hôte+miroir · coherence 53/29/0 · verify-correct-work 16/16.
- **Pendances §5** : rotation PAT (K1/K2/K3 + GHORG_GITHUB_TOKEN) · push miroir distant · ghorg/Go · F1 import Traktor · F3 P1b · fusion workflow → master.

## §7 — Reprise éventuelle (§ exécutable)

1. Lire SHARED §0 + règles d'or ; vérifier É1-INSTALL (`python3 scripts/ensure-installed.py`) — la volatilité snapshots UUID peut avoir recyclé (gardes Task 56).
2. Vérifier l'état : `python3 scripts/check-ecosysteme-integrity.py` (attendu 110/110) + `skills/dessin-technique/scripts/trigo-euler --selftest` (attendu 15/15).
3. Si G3 déjà consigné (worklog suite 14) : Task 58 CLOSE — ne pas y toucher ; file d'attente §5 du plan.
4. Voie --geo Python (suggestion ① d'origine : `geometry_from_cotes.py` + extension `generer_dessin.py --geo` + check T9) : NON reconstruite — hors contrat D585 (registre = nœud C++) ; suggestion documentée SKILL.md §1.8.

## §8 — Auto-clonage

Ce clone se référence lui-même comme artefact de clôture (D588) — toute session héritière le lit avant toute action sur la famille dessin-technique/inter-scripts (versions liées : dessin-technique v1.3.0, inter-scripts v1.0.0, registre contrat nœud).

**Validation 8 checks** : ① Auto-suffisance PASS (données clés in extenso) · ② Complétude worklog PASS (suites 9-14) · ③ Complétude skills PASS (versions + spécifications F1-F6) · ④ Complétude décisions PASS (D581-D588) · ⑤ Complétude bugs PASS (4/4) · ⑥ Complétude drifts PASS (3 typés) · ⑦ Exécutabilité PASS (§7) · ⑧ Auto-clonage PASS (§8) — **8/8 PASS**.
