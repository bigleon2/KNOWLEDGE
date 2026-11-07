# Rapport correct-work (projet) --bloc — Task 58

**Mode** : bloc par bloc (correct-work v2.11.0 §A/§1.7/§10.1bis) · **Date** : 2026-11-07 · **Session** : web-c30e6506 · **Périmètre** : chaîne Task 58 (branche compilation-windows K3 [requalifiée] + plancher dessin-technique v1.3.0 + clôture) · **Verdict global = pire des blocs**.

## Bloc B1 — G1 Branche compilation-windows (clé K3) — requalifiée done-documenté

| Check | Preuve mécanique | Verdict |
|---|---|---|
| Branche distante publiée | API GitHub (§0 plan) : `test/compilation-windows@04accb8` PRÉSENTE sur bigleon2/cmdr, master == 83d8c84 == pin manifeste | PASS |
| Fenêtre de compilation validée | Run WF 42303936370 **SUCCESS** (2026-11-06 22:18-22:23, artefact 1 758 544 o — plan-task59 §0, horodaté) ; le run 1 MSB3644 historique documenté et corrigé sans toucher au code | PASS |
| Requalification recyclage (règle d'or n°5) | 5ᵉ recyclage sandbox : ~/GitHub + journal volatils (L55-3) — reconstruction = travail jetable, D582-D584 **done-documenté** (preuves = documentation horodatée, pas le disque) — jamais de résultat fabriqué | PASS |
| Sécurité clé K3 | Jamais persistée (inline one-shot, scan 0 secret) — 13ᵉ+ exposition → RAPPEL rotation en clôture | PASS |

**Verdict B1 : PASS** (4/4). Finding : aucun nouveau — la fusion workflow → master reste décision propriétaire (§5).

## Bloc B2 — G2 Plancher dessin-technique v1.3.0 (D585/D586)

| Check | Preuve mécanique | Verdict |
|---|---|---|
| Nœud C++ selon contrat registre | `skills/dessin-technique/scripts/trigo-euler.cpp` (≈1500 L) + binaire — compilation EXACTE registre `g++ -O2 -std=c++17 -pthread -Wall` → **0 warning** ; 15 capacités + echo + daemon.stop ; modes one-shot/stdin/daemon ; NDJSON ; max_clients 8 | PASS |
| Selftest T7 | T01-T15 **15/15 PASS ×2, sorties byte-identiques** (`tmp/mission-task58/trigo-node/selftest-{1,2}.txt`) — valeurs contrôlées (Guldin 5000π exact, ratio cap ≈ sin 35,264° par valeurs singulières, ellipse 3/1,5/30° à 1e-6) | PASS |
| Preuves daemon T8 | Harnais `tmp/mission-task58/trigo-node/preuves.py` → **PASS 8/8 ×2, re-jeu identique** (`journal-preuves{,-run1}.json`) : 15 op via is_client, health-check echo, concurrence 4×25 = **100/100** (0,1-0,7 ms), saturation 8+1 → « daemon sature » non-bloquant, daemon.stop propre (socket supprimée), orchestrateur ×2 **sha16 identiques**, cas vivant joint 5c (44,9 × 35,2) | PASS |
| SKILL.md v1.3.0 | frontmatter `version: 1.3.0` + description F6 + §1.8 complet (nœud, capacités, lignage honnête R4, limites) + T7/T8 tableau §1.5 + §2 stack C++/exception N3 déclarée + §3 inter-scripts + tag #trigo-euler + read_when mathématiques | PASS |
| evals.json v1.3.0 | 8 tests (T1-T6 inchangés + T7/T8) — T8 vérifié en direct : `ok:true`, canal daemon-socket, arrêt propre, socket absente | PASS |
| Cascade KO-L004 5 touches | (1) SKILL.md ✓ (2) evals ✓ (3) KB `## dessin-technique v1.3.0` (Six fonctions + F6 + inter-scripts + calibration Task 58 — 7/7 checks) + skill-creator « Utilisé par » v1.3.0 ✓ (4) pin arbitre `"dessin-technique": "1.3.0"` commenté Task 58 ✓ (5) historiques-par-skill ligne v1.3.0 (4 versions) + sceaux v1.1.1 (git a988f51) ✓ ; ULTRA régénéré ×2 idempotent ; archive v2.3 rescellée ×2 (15/15 round-trip) | PASS |
| Plancher satisfait | frontmatter inter-scripts `dessin-technique >= 1.3.0` : installé 1.3.0 == déclaré 1.3.0 (registre v1.0.0 inchangé — contrat respecté) | PASS |
| Batterie certification | integrity **HÔTE 110/110 ×2 + MIROIR 110/110 ×2** · coherence **53 PASS / 29 WARN / 0 FAIL** · verify-correct-work **16/16** · miroir 3 commits (00f9ca6, e7d6bcb, 768bb3a) | PASS |

**Verdict B2 : PASS** (8/8). Findings corrigés en vol (max 2 rounds — conforme) : (1) T04 canonique.ellipse FAIL round 1 → cause racine double (matrice forme quadratique B/2 + second membre +1) → corrigé, 15/15 au round 2 ; (2) warning -Wall variable `degres` → intégrée en avertissement de réponse. Findings informatifs : (a) piège pipe subprocess (daemon enfant rémanent hérite stdout pipe → communicate() bloque — leçon consignée, redirection fichier) ; (b) **3 résorptions de dettes héritées** découvertes par les arbitres, jamais masquées : sync §0 gen-plan/certification-complete (propagation 00:57 non commitée), **70 étiquettes §0 → SHARED v1.7.28** (dette Task 60 G4, coherence FAIL → résorbée), **version-management 19ᵉ disparition** (incident volatilité n°7 — auto-restauré depuis miroir local, garde Task 56).

## Bloc B3 — G3 Clôture (D587/D588)

| Check | Preuve mécanique | Verdict |
|---|---|---|
| Rapport --bloc (ce document) | `download/rapport-correct-work-bloc-task58.md` — 3 blocs, verdict global = pire des blocs | PASS |
| Rapport final | `download/rapport-final-task58.md` (couverture 5/5 demandes, état final dérivé du disque, RAPPELS OBLIGATOIRES en tête) | PASS |
| Clone-chat scellé | `download/clone-discussion-2026-11-07-task58.md` (auto-suffisant, 8 checks clone-chat v2.0.2) | PASS |
| Answer key 8/8 | D581-D588 toutes done (D581-D584 done/documenté §0-bis, D585-D586 notes d'exécution, D587-D588 ce bloc) | PASS |
| Worklog R5 | Suites 10-14 : jalons G1 consigné, directives 8ᵉ-13ᵉ, inventaire E13-7, G2 terminé, clôture | PASS |

**Verdict B3 : PASS** (5/5). Finding : aucun.

---

## VERDICT GLOBAL : **PASS** (B1 PASS · B2 PASS · B3 PASS — 17/17 checks, 0 S1-S2, sources chemin:ligne)

Résorptions hors périmètre exécutées en vol (transparence) : dette §0 sync miroir, dette 70 étiquettes SHARED v1.7.28, version-management 19ᵉ — toutes documentées worklog suites 12-13 et commits miroir dédiés.
