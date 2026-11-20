# Référentiel du kit REA — rea-analysis v1.0.0

> Référentiel factuel du kit (dérivé du disque et des mesures Task 8/9 — règle d'or n°5) : surface, moteurs, verdicts, politique d'épingles. Le présent document est la source inline du skill ; les Evidence brutes vivent sous `tools/rea/`.

## 1. Identité du kit

| Élément | Valeur (2026-11-21, Task ID 12) |
|---|---|
| Dépôt | fork bigleon2/REA_Reverse_All_Thing_Kit (clone anonyme lecture seule) |
| Épingle installée | HEAD 03a3fcbce (6701 commits, 7622 fichiers trackés, arbre propre) |
| Origine | morluto/rea v6.8.0 (npm `rea-agents`, MIT) — fork = miroir-épingle SANS commit propre |
| Amont | hyper-actif : 0 ahead / 2317 behind au 2026-11-21 (upstream/main 76585bc08) → **politique d'épingles datées** (`rea-install.py --pin <sha>`), jamais de suivi implicite |
| Coûts | acquisition ≈ 48 s / 1,2 Go (clone 18 s + npm ci 15 s + build 15 s ; 246 Mo repo + 883 Mo node_modules + 62 Mo dist) — disque à prévoir |

## 2. Surface du CLI (`node scripts/rea.mjs --help` — 215 lignes, ~180 commandes)

- **inspect-\*** : lecture déterministe d'artefacts — `inspect-binary-hardening` · `inspect-byte-entropy` · `inspect-elf-notes` · `inspect-native-exports` · `inspect-binary-layout` · `inspect-go-binary` (vcs.revision récupérée du binaire — preuve Task 8) · etc.
- **analyze-\*** : campagnes lourdes (moteurs natifs) — `analyze-binary` (Ghidra headless) · `analyze-javascript-application` (frontend) · `analyze-android-apk` · `analyze-apple-ipa` · etc.
- **capture / compare** : captures de comportement et comparaison d'artefacts.
- **doctor** : sonde moteurs (node/host sains ; moteurs natifs par classification).
- ZÉRO commande de clonage/reproduction depuis un dépôt (grep borné Task 8 : 0 occurrence — verdict : inapplicable comme mécanisme de reproduction).

## 3. Moteurs d'analyse (état sandbox — doctor)

| Moteur | État | Note |
|---|---|---|
| node v24.22.3 / host debian 13 | healthy | — |
| Ghidra 12.2 PUBLIC | healthy ×7 (plateforme, architecture, installation, version, headless `support/analyzeHeadless`, décompilateur elf) | via `GHIDRA_INSTALL_DIR=tools/rea/ghidra/ghidra_12.2_PUBLIC` ; JDK 25 requis au-delà du runtime (Task 9) |
| hopper / ida / jadx / kuna | missing_analysis_engine | absents du sandbox — état dégradé documenté (règle d'or n°1 : jamais un arrêt) |

## 4. Bornes et leçons mesurées (profil NORMAL, nproc=2, D7 ≤ 590 s)

- `analyze-binary` (Ghidra) sur binaire Go 41,2 Mio : **échec mécanique** — Go 1.27.4 non couvert par les analyseurs Go de Ghidra 12.2 (« Untested Go version ») + délai de démarrage écoulé → bascule branche frontend.
- `analyze-javascript-application` sur frontend SvelteKit 9 336 fichiers : **rc=124** (borne D7 atteinte), verdict REA `retryable: true` → reprise sur profil plus puissant.
- Batterie `inspect-*` sur `bin/holyarrs` : **5/5 rc=0** (hardening · entropy · elf-notes · exports · layout — après adaptation venv pwntools 4.15 + REA_PWNTOOLS_MAX_INPUT_BYTES 48 Mio, journalisée Task 9).
- Evidence conservées : `tools/rea/*.out`, `tools/rea/inspect-go-binary-holyarrs.json`.

## 5. Verdicts intégration ($FACON2 — battery T1/T2/T3)

- **Task 9 G1 — VERDICT FAVORABLE** : intégrable $FACON (complémentaire de ghorg-cmdr [clonage] : REA = analyse SANS source, MIT, KO-L009-compatible par clones anonymes) sous conditions : épingles datées (amont hyper-actif), disque ~2,7 Go stack complète, personnalisation à porter dans le fork si divergence voulue.
- **Task 8 — inapplicable à la reproduction** : REA ne produit AUCUN arbre source ; la reproduction d'applications = git clone + build (branche (b), branche maintenue).
- **Choix de forme (Task ID 12, matrice correct-work §6)** : SKILL (pas agent, pas agent autonome) — un CLI déterministe ~180 commandes n'exige ni boucle d'agent ni mémoire persistante ; précédent ghorg-cmdr Task 51 (forme installée = skill, règle d'or n°8) ; disciplines mobilisées : spec-driven-development (contrat D101-D107), harness-engineering (idempotence ×2 + bornes), memory-engineering (registre KB append).

## 6. Protocole réseau (GO + KO-L009)

- Clones ANONYMES lecture seule uniquement (dépôts publics — jamais de jeton, jamais d'écriture distante, remotes sans identifiant).
- Releases publiques en lecture seule tolérées (Ghidra, JDK) — précédents Task 9/10.
- Toute élévation (jeton fourni par le propriétaire) suit KO-L009 ONE-SHOT : valeur jamais échoée/persistée, env à l'appel, unset immédiat, sorties masquées, remotes sanitisés, rotation recommandée.
