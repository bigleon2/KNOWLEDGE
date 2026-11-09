# Plan d'actions — Task 55 : optimisation des pendances différées (tsi-validator F1/F2 + inscription KB des 4 skills hors registre)

**Généré via gen-plan v3.35.1** (invocation **mode STEP** — `gen-plan : « enchère $FACON en mode STEP sur les pendances différées… »`, clause §A : plan affiché, **GO propriétaire attendu avant exécution**) · Session web-c30e6506 · 2026-11-06
**Horodatage plan : 2026-11-06T19:35:00+00:00**

---

## Contexte (E1-E2 — recensement intégral, règle d'or n°7)

**Directive propriétaire couverte (verbatim, alias expansés au registre) :**
1. « gen-plan : "enchère $FACON en mode STEP sur les pendances différées (tsi-validator F1/F2, inscription KB des 4 skills hors registre) dans l'objectif d'optimiser $FACON mon écosystème" » — *$FACON = « de façon cohérente, optimisée et fonctionnelle »*. Enchère = nouvelle tâche séquencée après la Task 54 suite (correct-work --bloc PASS, main 3bb050e) ; mode STEP = plan affiché, attente GO.

**Garde préalable exécutée (règle d'or n°9 / É1-INSTALL / E1-RES) :**
- `ensure-installed.py --check` → **INSTALLE** (rc=0, 48 entrées KB, aucun fichier manquant) — piliers présents (gen-plan v3.35.1, SHARED v1.7.24, règle langue FR active).
- G-RES (resource-monitor) : verdict **OK** — profil NORMAL, exécution SÉQUENTIELLE adaptée (chaîne de dépendances linéaire : F1/F2 → superposition cmdr → inscription KB → re-certification).
- B-11 (lecture seule préalable) : worklog lu — Task 54 suite clos (fusions R4 vérifiées, GEN langue FR d387169, arbitres 10/10, correct-work --bloc PASS 6/6 blocs, clone scellé).
- Fraîcheur plan (KO-L005/D012) : gen-plan v3.35.1 = version génétrice du plan courant (le GEN d387169 est déjà intégré à l'état) — aucun plan en vol.

**Recensement des 2 pendances (état disque vérifié ce jour) :**

| # | Pendances | État constaté | Détail technique |
|---|-----------|---------------|------------------|
| **F1** | tsi-validator : verdict **PRÉFÉRENCES** | v1.2.0 — voie réelle NIXML : un TSI de préférences (Entry `DeviceIO.Config.Controller` absente) rend **FAIL E1** alors que la structure NIXML est saine | `scripts/valider-tsi.py` (const. `ENTRY_CTRL` ligne 41) : E1 échoue proprement mais verdict binaire PASS/FAIL — pas de tiers. Échantillon réel disponible : `~/GitHub/bigleon2/cmdr/tests/keyboard/keyboard__timecode_mode__1st_abs__2nd_rel___3rd___4th_hap.tsi` (TC4 Task 51 : 21 PASS/2 FAIL légitimes = F1/F2) |
| **F2** | tsi-validator : **multi-devices E3** | v1.2.0 — `DEVS déclare N devices (attendu 1)` : erreur E3 systématique dès que le DIOM embarque > 1 DEVI | `valider-tsi.py` ligne 108-111 : single `next(t for t …)` — un seul device attendu partout (E2, E3, stats). Aucune itération par device |
| **P3** | Inscription KB des **4 skills hors registre** | Les 4 skills **existent dépôt + profil**, versionnés, fonctionnels — seule l'entrée registre manque : `inter-scripts` v1.0.0 (Dépend de graph-engineering >=1.0.1) · `resume-youtube` v1.1.0 · `web-reader` v1.0.0 · `web-search` v1.0.0 | Registre `skills/KNOWLEDGE.md` : 48 sections versionnées (0 occurrence `## <skill> v` pour les 4) ; dictionnaire `ECO_SKILLS` (check-ecosysteme-integrity.py ligne 73) : 4 entrées absentes ; interactions : arête inter-scripts→graph-engineering NON déclarée bidirectionnelle (« Utilisé par » de graph-engineering) |

**Cascade identifiée (leçons L54-4/L54-5 + règle KO-L004) :**
1. F1/F2 modifient `tsi-validator` (famille TSI) → **superposition cmdr à re-jeu** (SHA-256) + PR + merge R4 + **re-pin manifeste** + sync profil.
2. Bump tsi-validator v1.2.0→**v1.3.0** (2 fonctionnalités = 1 minor) → ligne registre KB (ligne 496) à mettre à jour.
3. Inscription KB 4 skills → `ECO_SKILLS` += 4 → **baseline integrity 100→104/104** (recalage KO-L004) + arêtes interactions à créer bidirectionnelles (sinon WARN d'asymétrie — baseline coherence à recaler).
4. Les push distants utiliseront K1 → **exposition supplémentaire consignée** (rotation PAT toujours en attente propriétaire — rappel clôture).

---

## Answer key (E1 — décisions D551-D556, criterion + verification exécutable)

- **D551** (S1, pending) — **F1 : verdict PRÉFÉRENCES** — `valider-tsi.py` voie réelle : Entry contrôleur absente + NIXML structurellement sain → verdict **`PRÉFÉRENCES`** (exit code dédié **2**, JSON `"PREFERENCES"`), message « fichier de préférences — hors périmètre validation mapping » ; SKILL.md §E1 + interface (§2 : `PASS|FAIL|PRÉFÉRENCES`) + description mises à jour ; bump v1.3.0.
  - criterion : le TSI de préférences cmdr (tests/keyboard) rend PRÉFÉRENCES exit 2 (plus FAIL exit 1) ; `--self-test` étendu à 3 cas (valide PASS / invalide FAIL / préférences PRÉFÉRENCES) ; zéro régression (échantillons golden inchangés : valide → PASS, invalide → FAIL 8 catégories)
  - verification : `python3 skills/tsi-validator/scripts/valider-tsi.py --self-test` → PASS 3/3 ; `python3 …/valider-tsi.py ~/GitHub/bigleon2/cmdr/tests/keyboard/keyboard__timecode_mode*.tsi` → `VERDICT : PRÉFÉRENCES` + exit 2 ; re-jeu echantillon-valide.tsi → PASS exit 0 ; `--json` → `"verdict": "PREFERENCES"`
- **D552** (S1, pending) — **F2 : multi-devices E3** — `valider-tsi.py` : DEVS avec N>1 devices → **itération des DEVI** (E2 comptage par device, E3 par device, `stats.devices` = liste), suppression de l'erreur systématique « attendu 1 » ; SKILL.md §E3 + stats JSON mis à jour (même bump v1.3.0 que D551).
  - criterion : un DIOM multi-devices sain (2 devices, construit au self-test) rend **PASS** avec `stats.devices` == 2 ; un DIOM multi-devices avec un device fautif rend FAIL **sur le device concerné uniquement** (erreur E3 qualifiée `device i`) ; self-test 4 cas
  - verification : `--self-test` PASS 4/4 ; échantillon synthétique multi-devices (généré in-test, jamais sur disque) → PASS + stats.devices == 2 ; re-jeu échantillons golden → verdicts inchangés
- **D553** (S1, pending) — **P3 : inscription KB des 4 skills** — 4 sections registre `skills/KNOWLEDGE.md` au format modèle (## <skill> vX.Y.Z / Category / Description / Dernière calibration / Dépend de / Utilisé par / Statut), rédigées depuis les SKILL.md réels (aucune invention — périmètres exacts) ; `ECO_SKILLS` += 4 (check-ecosysteme-integrity.py) ; arête bidirectionnelle inter-scripts↔graph-engineering (« Utilisé par : inter-scripts » ajouté à l'entrée graph-engineering).
  - criterion : registre passe de 48 à **52 sections versionnées** ; integrity **104/104 PASS 0 FAIL** (baseline recalée KO-L004) ; coherence **0 FAIL** avec les 4 nouvelles entrées sans WARN d'asymétrie nouveau (arête inter-scripts déclarée des deux côtés) ; verify-cross 100 %
  - verification : `grep -c "^## " skills/KNOWLEDGE.md` → 52 (+en-têtes) ; `python3 scripts/check-ecosysteme-integrity.py` → 104/104 ; `python3 scripts/test-coherence-interactions.py` → 0 FAIL ; `python3 scripts/verify-cross.py` → 100 % ; `grep -c "inter-scripts" skills/KNOWLEDGE.md` ≥ 2 (entrée + Utilisé par graph-engineering)
- **D554** (S2, pending) — **Cascade cmdr (L54-5)** — superposition re-jeu (tsi-validator v1.3.0 → cmdr/ecosystem/ + SOURCE.md régénéré) → commit (identité bigleon2) → PR cmdr → **merge R4** (2 parents) → branche supprimée → **manifeste re-pinné** (bootstrap ×2 idempotent, commit_epingle = nouveau merge) → push KNOWLEDGE → sync profil (tsi-validator + manifeste + registre).
  - criterion : cmdr/ecosystem/skills/tsi-validator/SKILL.md == KNOWLEDGE (SHA-256 via SOURCE.md) ; merge commit 2 parents ; bootstrap run 2 = « déjà à jour » ; porcelain 0 ×2 ; profil byte-identique
  - verification : `git -C ~/GitHub/bigleon2/cmdr log -1 --format=%P | awk '{print NF}'` → 2 ; `python3 scripts/ecosystem/bootstrap.py` ×2 → erreurs None ; `cmp` dépôt↔profil ×3 fichiers ; `git status --porcelain | wc -l` → 0 ×2
- **D555** (S2, pending) — **Re-certification intégrale** — batterie 10 contrôles en exécution courante : ensure-installed (INSTALLE, 52 entrées) · verify-cross 100 % · integrity **104/104** · coherence ≥ 52/23/0 recalé (0 FAIL) · tool-routing PASS · verify-correct-work 16/16 · TG4 Karnaugh 20/20 · bootstrap ×2 idempotent · porcelain 0 ×2 · marqueur ghorg e05d9b5f + **self-tests tsi-validator ×2 arbres** (dépôt + profil, 4/4 chacun).
  - criterion : 10/10 verts + 2/2 self-tests — aucune régression, toutes baselines recalées explicitement (100→104 integrity, coherence nouvelle baseline documentée)
  - verification : sorties consignées au rapport final Task 55 (commandes + verdicts)
- **D556** (S2, pending) — **Clôture** — rapport `download/rapport-final-task55-optimisation-pendances-deferrees.md` (F1/F2/P3 : avant/après avec preuves) ; **correct-work (projet) --bloc** (3 blocs : B1 tsi-validator F1/F2, B2 inscription KB, B3 cascade+re-certification) ; worklog ×2 (profil + dépôt) ; clone-chat scellé (8 checks) ; push final ; **rappel révocation PAT K1/K2 + GHORG_GITHUB_TOKEN (exposition supplémentaire des push — rotation TOUJOURS en attente)**.
  - criterion : verdict correct-work --bloc consigné (pire des blocs), clone 8/8, pendances suivantes listées (différé restant : décision branche test/compilation-windows, normalisation indentation registre alias S4)
  - verification : `ls download/rapport-final-task55-*` ; `ls download/*task55*clone*` ; entrée worklog finale ; section rappel PAT présente au rapport ET au chat

---

## Groupes d'exécution (structure hiérarchique §5.5)

**Vue d'ensemble** : G1 (F1+F2 tsi-validator) → G2 (P3 inscription KB) → G3 (cascade cmdr + re-certification) → G4 (clôture). Chaîne strictement séquentielle : G3 dépend de G1 (superposition du v1.3.0) ET G2 (registre complet à certifier) ; G4 clôt l'ensemble.

### G1 — tsi-validator F1/F2 : verdict PRÉFÉRENCES + multi-devices (D551, D552)
- **SG1.1 F1 — verdict PRÉFÉRENCES** : `valider-tsi.py` — détection « Entry contrôleur absente + NIXML sain » → verdict `PRÉFÉRENCES` (exit 2, JSON "PREFERENCES") ; 3ᵉ cas golden au self-test (échantillon préférences réel cmdr, copie in-test jamais sur disque) ; SKILL.md §E1/§2/description. — *T1.1.1 code, T1.1.2 self-test, T1.1.3 SKILL.md*
- **SG1.2 F2 — multi-devices E3** : `valider-tsi.py` — itération DEVI (E2/E3 par device, stats.devices[]) ; 4ᵉ cas golden au self-test (DIOM 2 devices synthétique) ; SKILL.md §E3/stats. — *T1.2.1 code, T1.2.2 self-test, T1.2.3 SKILL.md*
- **SG1.3 Bump + validation** : frontmatter v1.2.0→v1.3.0, ligne registre KB 496, self-test 4/4, test réel cmdr (préférences → PRÉFÉRENCES exit 2), re-jeu golden (0 régression), arbitre integrity avant cascade. — *T1.3.1 bump, T1.3.2 tests, T1.3.3 registre*
- **correct-work(groupe) G1** (max 2 rounds).

### G2 — P3 : inscription KB des 4 skills (D553)
- **SG2.1 Rédaction 4 sections registre** : inter-scripts v1.0.0 (Dépend de : graph-engineering >=1.0.1) · resume-youtube v1.1.0 · web-reader v1.0.0 · web-search v1.0.0 — descriptions depuis les SKILL.md réels (règle d'or n°2 : aucun détail inventé, périmètres exacts). — *T2.1.1-T2.1.4 (une section par skill)*
- **SG2.2 Recalibrage mécanique** : ECO_SKILLS += 4 (check-ecosysteme-integrity.py) + arête bidirectionnelle graph-engineering (« Utilisé par » += inter-scripts). — *T2.2.1 ECO_SKILLS, T2.2.2 arête*
- **SG2.3 Arbitres recalés** : integrity 104/104 · coherence 0 FAIL (nouvelle baseline documentée) · verify-cross 100 %. — *T2.3.1-T2.3.3*
- **correct-work(groupe) G2** (max 2 rounds).

### G3 — Cascade cmdr + re-certification intégrale (D554, D555)
- **SG3.1 Superposition + PR + merge + re-pin** : bootstrap (D6 re-jeu overlay tsi-validator v1.3.0) → commit bigleon2 → PR cmdr → merge R4 (2 parents) → branche supprimée → manifeste re-pinné → push → sync profil. — *T3.1.1 overlay, T3.1.2 PR+merge, T3.1.3 re-pin+push+sync*
- **SG3.2 Batterie 10 + self-tests ×2 arbres** : 10 contrôles + tsi-validator --self-test dépôt ET profil (4/4 ×2). — *T3.2.1-T3.2.11*
- **correct-work(groupe) G3** (max 2 rounds).

### G4 — Clôture (D556)
- **SG4.1 Rapport final** : `download/rapport-final-task55-optimisation-pendances-deferrees.md` — avant/après F1/F2/P3 avec preuves, baselines recalées, pendances suivantes. — *T4.1.1*
- **SG4.2 correct-work (projet) --bloc** : 3 blocs (B1 F1/F2, B2 P3, B3 cascade) — verdict global = pire des blocs. — *T4.2.1*
- **SG4.3 Worklog + clone-chat + push final** : worklog ×2, clone scellé 8/8, push, **rappel révocation PAT** (chat + rapport). — *T4.3.1 worklog, T4.3.2 clone, T4.3.3 push+rappel*
- **correct-work(groupe) G4** (max 2 rounds).

---

## Budget & ressources (E6)

- **Budget estimé** : ~34 k#token (G1 ~12 k, G2 ~6 k, G3 ~10 k, G4 ~6 k) — profil NORMAL, contingence ×2 = ~68 k#token.
- **Ressources critiques** : clone cmdr propre (porcelain 0 ✓ ce jour), K1 valide (exposition supplémentaire à consigner), échantillon préférences cmdr disponible ✓, aucune dépendance bloquante.
- **Risques** : (R1) le fichier préférences cmdr pourrait contenir d'autres écarts NIXML → F1 teste « Entry absente » en priorité, verdict PRÉFÉRENCES seulement si structure saine (sinon FAIL documenté) ; (R2) multi-devices : sémantique E4-E8 reste déléguée à analyse-doc-s4mk2 (R4 — pas de duplication) ; (R3) baseline coherence pourrait bouger (nouvelles arêtes) → recalage documenté KO-L004, jamais silencieux.

## Verdict E8

**PASS** — la chaîne D551-D556 couvre intégralement la directive (les 2 pendances nommées + l'objectif d'optimisation $FACON) : F1 et F2 transforment les 2 FAIL légitimes du TC4 Task 51 en comportements corrects documentés (verdict tiers PRÉFÉRENCES + itération multi-devices, bump v1.3.0) ; P3 fait passer le registre de 48 à 52 entrées avec recalage mécanique complet (ECO_SKILLS, integrity 104/104, arêtes bidirectionnelles) ; la cascade cmdr (L54-5) et la re-certification 10+2 garantissent $FACON2 en fin de tâche ; la clôture --bloc + clone-chat + rappel PAT referment proprement. L'ordre respecte les dépendances (skill d'abord, registre ensuite, cascade en dernier, clôture finale) ; chaque décision porte criterion + verification exécutables.

---

**Mode STEP — sauvegarde KO-L005** : `download/plan-task55-optimisation-pendances-deferrees.md` (généré via gen-plan v3.35.1, horodatage ci-dessus).
**Statut : PLAN-AFFICHE — attente du GO propriétaire.**
