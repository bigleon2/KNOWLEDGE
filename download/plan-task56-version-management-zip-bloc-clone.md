# Plan d'actions Task 56 — version-management (cause racine) · ZIP S4 MK2 · correct-work --bloc · clone-chat

**Générateur** : skill `gen-plan` v3.35.1 (mode **step** — demande propriétaire : « recommence le plan d'actions actuel mais en le générant via mon skill gen-plan », relais de la demande d'origine « continue mais avant fait gen-plan (step) »).
**Session** : web-c30e6506 · **Date** : 2026-11-06 · **Exécution** : mode step (enchaînement autonome des groupes, `correct-work(groupe)` après chaque groupe — max 2 rounds — puis `correct-work (projet) --bloc` en fin de chaîne).

---

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5)

| Vérification préalable | Résultat |
|---|---|
| É1-INSTALL `ensure-installed.py --check` | **INSTALLE** (rc=0, git_repo d184c98, KB 52 entrées) |
| Garde post-coupure (règle d'or n°9 — arbitre integrity) | **107/108 PASS, 1 FAIL : `version-management` SKILL.md manquant** → **4ᵉ récidive** (Tasks 52, 54, 55, aujourd'hui — leçon **L55-3** : investiguer la cause racine, ne pas restaurer aveuglément) |
| Collecte G-RES (resource-monitor) | **OK → PARALLELE** (disque 7,5 Go, mémoire 2,7 Go, charge 0) |
| Fraîcheur plan (KO-L005) | gen-plan v3.35.1 = version génératrice ; plan Task 53-55 perdus au recyclage → **re-génération intégrale** (demande explicite propriétaire) |
| Recyclage sandbox | **5ᵉ** — `~/GitHub` DÉTRUIT ; livrables download/ des Tasks 53-55 perdus ; dépôt miroir local `KNOWLEDGE-repo/` **présent** (source locale de vérité — règle d'or n°4) ; `KNOWLEDGE-repo/skills/version-management/` **v1.2.0 EXISTE** |
| ZIP propriétaire | `upload/mes-mappings-tsi-actuels.zip` — **6 fichiers TSI** (4 mappings S4 MK2 : Aout 2023, Novembre 2023, Aout 2024, Juin 2024-2025 + 2 « Settings » volumineux 2/4 Mo attendus PRÉFÉRENCES) |
| correct-work `--bloc` | Mode **confirmé préexistant** (v2.9.0 : §A déclencheur, §1.7 mode, §10.1bis checklist — leçon L54-4) → tâche 3 = vérification en **exécution réelle** |
| État arbitres à l'ouverture | integrity 107/108 · coherence 53/23/0 (baseline Task 55) |

**Faits d'ancrage cause racine (à approfondir G1)** : version-management absent du profil ET du HEAD git du profil ; le snapshot profil (21:01) est **postérieur** à tsi-validator v1.3.0 (Task 55 G1) mais **antérieur à la restauration** de version-management (Task 55 G3) → piste : restauration par copie sans ancrage snapshot + garde légère aveugle (L54-1 : `ensure-installed` ne contrôle pas les répertoires des skills du registre KB).

---

## §1 Objectif (toutes les demandes de la discussion — règle d'or n°7)

Demande d'origine : « analyse $FACON et corrige $FACON les pendances signalées (mappings TSI actuels clavier + KONTROL S4 MK2 fournis) dans l'objectif de corriger $FACON les failles de mon écosystème afin de l'optimiser $FACON pour qu'il ait un fonctionnement $FACON2 » — expansions alias-eco : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) ».

Les 4 étapes ordonnées du plan d'actions actuel (demande « gen-plan (step) ») :
1. **Analyser pourquoi « version-management » disparaît tout le temps** de l'écosystème + optimiser pour que cela ne se reproduise plus (ni cette discussion, ni les futures).
2. **Analyser le ZIP** (plusieurs anciens mappings S4 MK2 ajoutés par le propriétaire).
3. **correct-work --bloc** : vérifier que c'est bien le mode bloc par bloc qui se lance ; si ce n'est pas le cas, faire les correctifs adaptés.
4. **clone-chat**.

Demande intégrée en cours de plan (E13 — règle d'or n°3, directive propriétaire 2026-11-06, « continue mais intègre gen-plan ») :
5. **Lecture SHARED à l'exécution** : « fais en sorte $FACON que lorsqu'un de mes skills, agents ou scripts est exécuté qu'il lise $FACON les parties de PM SHARED qui lui sont dédiées, ainsi que les règles d'or de mon écosystème » — mécanisme structurel : portage du protocole par le corpus (SHARED §nouveau + §0 propagé à tous les éléments) → G5.

---

## Answer key (hook E1)

```yaml
decisions:
  - id: "D001"
    libelle: "Plan régénéré via gen-plan v3.35.1 en mode step (structure G/SG/T §5.5)"
    criterion: "Le plan est écrit dans download/, validé E8 (P1-P5), affiché au chat (PLAN-AFFICHE)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task56-version-management-zip-bloc-clone.md --worklog worklog.md → PASS 5/5"
    source: "Demandes propriétaire (gen-plan (step) + « recommence le plan d'actions actuel via mon skill gen-plan »)"
    priority: S1
    status: pending
  - id: "D002"
    libelle: "Cause racine de la disparition récidivante de version-management INVESTIGUÉE (jamais de restauration aveugle — L55-3)"
    criterion: "Rapport d'analyse documentant la mécanique complète de la récidive (recyclage → snapshot carencé → absence de restauration automatique), chaque affirmation ancrée à un artefact vérifiable"
    verification: "Rapport G1 dans download/ ; worklog Task 56 cite les preuves (git, pipeline, timestamps, pin)"
    source: "Leçon L55-3 (worklog 2026-11-06) + arbitre 107/108 du 2026-11-06 21:04 UTC"
    priority: S1
    status: pending
  - id: "D003"
    libelle: "Correctif DURABLE appliqué : la disparition ne peut plus passer inaperçue ni persister"
    criterion: "Garde étendue ensure-installed (contrôle des répertoires des skills du registre KB — piste L54-1) avec réparation depuis le dépôt local ; version-management v1.2.0 restauré ; cascade conformité KO-L004 si le skill gen-plan est modifié"
    verification: "Test mécanique : absence simulée détectée + réparée par ensure-installed ; integrity 108/108 ×2 ; re-jeu idempotent"
    source: "Leçons L54-1 + L55-3 ; directive propriétaire « que cela ne se reproduise plus »"
    priority: S1
    status: pending
  - id: "D004"
    libelle: "ZIP analysé intégralement (6 TSI) — inventaire, classification, analyse mapping"
    criterion: "Chaque fichier reçoit un verdict tsi-validator v1.3.0 (PASS/FAIL/PRÉFÉRENCES) et une entrée au rapport d'analyse (pipeline analyse-doc-s4mk2 v1.3.0)"
    verification: "Rapport JSON + rapport Markdown dans download/ couvrant 6/6 fichiers"
    source: "Demande propriétaire « analyse le ZIP, j'y ai ajouté plusieurs de mes anciens mapping pour le S4 MK2 »"
    priority: S1
    status: pending
  - id: "D005"
    libelle: "Qualification honnête des 2 fichiers volumineux « Settings » (2/4 Mo)"
    criterion: "Verdict PRÉFÉRENCES attendu (F1 tsi-validator v1.3.0) — si divergent, analyse documentée de l'écart"
    verification: "Verdicts par fichier dans le rapport G2 ; classification TSI (mapping vs préférences) tracée"
    source: "Inventaire ZIP (Traktor - Setting NOVEMBRE 2024.tsi 2 Mo, Traktor Settings.tsi 4 Mo)"
    priority: S2
    status: pending
  - id: "D006"
    libelle: "correct-work (projet) --bloc VÉRIFIÉ en exécution réelle — c'est bien le mode bloc par bloc qui se lance"
    criterion: "Exécution réelle du mode --bloc (déclencheur §A, mode §1.7, checklist §10.1bis) produisant des verdicts PAR BLOC (B1…Bn) + verdict global ; si divergence constatée → correctifs adaptés appliqués"
    verification: "Rapport correct-work --bloc avec verdicts par bloc dans download/ ; structure de sortie prouve le mode bloc"
    source: "Demande propriétaire tâche 3 ; leçon L54-4 (mode = MODE D'EXÉCUTION préexistant, pas un artefact à créer)"
    priority: S1
    status: pending
  - id: "D007"
    libelle: "Failles et optimisation de la demande d'origine couvertes — rapport final $FACON2"
    criterion: "Rapport final : chaque pendance signalée ∈ {traitée, documentée} ; failles écosystème (vm) + failles mappings (ZIP) synthétisées ; état de fonctionnement décrit (cohérent, optimisé, fonctionnel)"
    verification: "Tableau de couverture pendances ↔ actions dans le rapport final"
    source: "Demande d'origine (analyse $FACON et corrige $FACON les pendances)"
    priority: S1
    status: pending
  - id: "D008"
    libelle: "clone-chat scellé en fin de chaîne"
    criterion: "Clone de la discussion écrit dans download/ + entrée worklog"
    verification: "Fichier clone présent ; entrée worklog R5"
    source: "Demande propriétaire tâche 4"
    priority: S1
    status: pending
  - id: "D009"
    libelle: "RAPPEL OBLIGATOIRE rotation PAT K1/K2 + GHORG_GITHUB_TOKEN (12ᵉ+ expositions — KO-L009)"
    criterion: "Rappel présent au bloc récapitulatif final ET au rapport final"
    verification: "Chaîne « rotation » présente dans le rapport final"
    source: "Worklog Task 55 état final (pendances propriétaire)"
    priority: S1
    status: pending
  - id: "D010"
    libelle: "Français intégral (règle d'or n°6 renforcée v3.35.1 — dès le premier mot, jamais dérivé)"
    criterion: "Plan, rapports, livrables et échanges en français ; artefacts techniques verbatim exceptés"
    verification: "Relecture des livrables G4"
    source: "Règle d'or n°6 gen-plan v3.35.1"
    priority: S1
    status: pending
  - id: "D011"
    libelle: "Lecture SHARED à l'exécution (directive propriétaire E13 2026-11-06) — tout skill/agent/script exécuté lit les parties du PM SHARED qui lui sont dédiées + les règles d'or de l'écosystème"
    criterion: "Mécanisme structurel porté par le corpus : SHARED v1.7.26 (section « Règles d'or de l'écosystème & protocole de lecture à l'exécution » — résumé des 9 règles d'or + renvoi canonique gen-plan §1.5, R4 jamais dupliquer) + propagateur v2.0.7 (bloc §0 v1.7.26 enrichi de la ligne protocole) + propagation à TOUS les éléments (skills + scripts + agents)"
    verification: "Propagation exécutée (compteur d'éléments mis à jour) ; idempotence ×2 ; coherence baseline (§0 == SHARED réel partout) ; présence de la ligne protocole dans un échantillon de SKILL.md/scripts/agents"
    source: "Directive propriétaire : « fais en sorte $FACON que lorsqu'un de mes skills, agents ou scripts est exécuté qu'il lise $FACON les parties de PM SHARED qui lui sont dédiées, ainsi que les règles d'or de mon écosystème »"
    priority: S1
    status: pending
  - id: "D012"
    libelle: "Les règles d'or de l'écosystème deviennent accessibles à tout élément exécuté (portage corpus, pas seulement gen-plan)"
    criterion: "Le SHARED porte le résumé des 9 règles d'or (n°1-9) avec renvoi canonique gen-plan §1.5 ; le §0 propagé cite les règles d'or et le protocole de lecture"
    verification: "Contenu de la section SHARED vérifié ligne à ligne vs gen-plan §1.5 (9 règles présentes) ; ligne §0 présente dans l'échantillon"
    source: "Directive propriétaire (même message — « ainsi que les règles d'or de mon écosystème »)"
    priority: S1
    status: pending
```

---

## §2 Plan d'actions (mode step — structure hiérarchique §5.5)

### Groupe G1 — version-management : cause racine + correctif durable (tâche 1)

**Sous-groupe SG1.1 — Diagnostic mécanique** `[À FAIRE] 0/3`
- T1.1.1 `[À FAIRE]` Reconstituer la chronologie des 4 récidives (worklog Tasks 52/54/55 + aujourd'hui) et la mécanique de snapshot/recyclage du profil (HEAD git UUID 21:01, fenêtres de carence, ordre G1/G3 Task 55). `#token 3k`
- T1.1.2 `[À FAIRE]` Auditer le chemin de restauration : `ensure-installed.py` (garde légère — quels piliers ?), `eco_install_pipeline.py` (que restaure-t-il ? pin/liste), dépôt miroir `KNOWLEDGE-repo/` (vm v1.2.0 présent). Identifier POURQUOI vm seul échappe à la restauration automatique. `#token 4k`
- T1.1.3 `[À FAIRE]` Rédiger la synthèse cause racine avec preuves mécaniques (chaque affirmation ancrée — règle d'or n°5). `#token 2k`

**Sous-groupe SG1.2 — Correctif durable** `[À FAIRE] 0/3`
- T1.2.1 `[À FAIRE]` Étendre la garde `ensure-installed.py` : contrôle des répertoires des skills du registre KB (piste L54-1) + réparation automatique depuis le dépôt local (miroir KNOWLEDGE-repo — règle d'or n°4) ; conformité cascade KO-L004 si gen-plan est modifié (bump + PM + recalibrage). `#token 5k`
- T1.2.2 `[À FAIRE]` Tester le correctif : absence simulée détectée + réparée ; re-jeu idempotent (2ᵉ passage no-op). `#token 2k`
- T1.2.3 `[À FAIRE]` Restaurer `skills/version-management/` v1.2.0 (forme certifiée dépôt→profil) + vérifier `grep ^version SKILL.md` = 1.2.0. `#token 1k`

**Sous-groupe SG1.3 — Re-certification G1** `[À FAIRE] 0/2`
- T1.3.1 `[À FAIRE]` Batterie arbitres : integrity **108/108** attendu + coherence ≥ 53/23/0 + verify-cross 100 %. `#token 2k`
- T1.3.2 `[À FAIRE]` `correct-work(groupe G1)` — verdict consigné worklog. `#token 2k`

### Groupe G2 — Analyse du ZIP : 6 TSI S4 MK2 (tâche 2 + demande d'origine)

**Sous-groupe SG2.1 — Inventaire + classification** `[À FAIRE] 0/3`
- T2.1.1 `[À FAIRE]` Extraction sûre du ZIP vers `tmp/` (vérification intégrité, 6 fichiers attendus). `#token 1k`
- T2.1.2 `[À FAIRE]` Verdicts `tsi-validator` v1.3.0 ×6 (vague parallèle — Graph Diamond, fichiers indépendants) : mapping (PASS/FAIL) vs PRÉFÉRENCES (exit 2 — F1). `#token 3k`
- T2.1.3 `[À FAIRE]` Classification `analyse-doc-s4mk2` (pipeline 7 étapes, référentiel G2) : DeviceIO.Config.Controller vs préférences-FX/préférences-layouts. `#token 4k`

**Sous-groupe SG2.2 — Analyse des mappings** `[À FAIRE] 0/3`
- T2.2.1 `[À FAIRE]` Analyse DIOM des 4 mappings (commandes, modifiers, LED, couches — script `analyser-zip-mk2.py` / `analyser_tsi_mk2.py`). `#token 6k`
- T2.2.2 `[À FAIRE]` Lecture croisée chronologique Aout 2023 → Juin 2024-2025 : évolution, régressions, invariants du mapping propriétaire. `#token 3k`
- T2.2.3 `[À FAIRE]` Détection des failles mappings + recommandations $FACON2 (orchestrateur-tsi : arbitrage famille TSI si besoin). `#token 3k`

**Sous-groupe SG2.3 — Synthèse G2** `[À FAIRE] 0/2`
- T2.3.1 `[À FAIRE]` Rapport d'analyse ZIP (Markdown + JSON) dans download/. `#token 3k`
- T2.3.2 `[À FAIRE]` `correct-work(groupe G2)`. `#token 2k`

### Groupe G3 — correct-work --bloc : vérification du mode (tâche 3)

**Sous-groupe SG3.1 — Vérification en exécution réelle** `[À FAIRE] 0/3`
- T3.1.1 `[À FAIRE]` Re-contrôle statique : déclencheur §A + mode §1.7 + checklist §10.1bis du SKILL.md correct-work v2.9.0. `#token 1k`
- T3.1.2 `[À FAIRE]` Exécution réelle `correct-work (projet) --bloc` sur le périmètre Task 56 (blocs = G1, G2, G3, G4) — verdicts PAR BLOC attendus. `#token 4k`
- T3.1.3 `[À FAIRE]` Verdict du mode : conforme (verdicts par bloc produits) OU divergent → correctifs adaptés (§1.7/§10.1bis) documentés worklog. `#token 2k`

### Groupe G5 — Lecture SHARED à l'exécution : portage corpus (directive propriétaire E13)

**Sous-groupe SG5.1 — Corpus SHARED + propagateur** `[À FAIRE] 0/3`
- T5.1.1 `[À FAIRE]` SHARED v1.7.25 → **v1.7.26** : nouvelle section « Règles d'or de l'écosystème & protocole de lecture à l'exécution » (résumé des 9 règles d'or n°1-9 + renvoi canonique gen-plan §1.5 — R4 jamais dupliquer ; protocole : tout skill/agent/script à l'exécution lit §0 + sa section dédiée §7 + règles d'or). `#token 3k`
- T5.1.2 `[À FAIRE]` Propagateur **v2.0.7** : bloc §0 v1.7.26 enrichi de la ligne « Règles d'or & lecture SHARED à l'exécution ». `#token 2k`
- T5.1.3 `[À FAIRE]` Propagation complète (skills + scripts + agents) + idempotence ×2. `#token 3k`

**Sous-groupe SG5.2 — Recalibrage + certification G5** `[À FAIRE] 0/2`
- T5.2.1 `[À FAIRE]` Recalibrage croisé (PM-INSTALL §2ter/A.3 si citation SHARED, rescellement archive corpus, sync miroir) + arbitres ×2 (integrity 108/108, coherence baseline §0==v1.7.26, verify-correct-work 16/16). `#token 3k`
- T5.2.2 `[À FAIRE]` `correct-work(groupe G5)` — verdict consigné worklog. `#token 2k`

### Groupe G6 — Clôture $FACON2 (ex-G4, réordonné après G5 — le clone-chat scelle APRÈS le chantier SHARED)

**Sous-groupe SG6.1 — Rapport final + E15** `[À FAIRE] 0/2`
- T6.1.1 `[À FAIRE]` Rapport final : couverture pendances (tableau), failles corrigées (vm + mappings), optimisation, fonctionnement $FACON2, **RAPPEL rotation PAT K1/K2 + GHORG_GITHUB_TOKEN (D009)**. `#token 3k`
- T6.1.2 `[À FAIRE]` knowledge-observer E15 (modes M1-M2) : leçons L56-x — dont clôture officielle de L55-3 (cause racine résolue + preuve vivante 10ᵉ matérialisation auto-réparée). `#token 2k`

**Sous-groupe SG6.2 — Scellement** `[À FAIRE] 0/3`
- T6.2.1 `[À FAIRE]` `correct-work (projet) --bloc` FINAL — verdicts par bloc B1-Bn + global (preuve D006). `#token 3k`
- T6.2.2 `[À FAIRE]` clone-chat scellé dans download/ + worklog R5. `#token 2k`
- T6.2.3 `[À FAIRE]` Bloc récapitulatif final affiché au chat (E7-DISP). `#token 1k`

---

## §3 Protocole d'exécution (mode step)

- Enchaînement **G1 → G2 → G3 → G5 → G6** (ordre demandé par le propriétaire + G5 inséré avant la clôture G6 — E13 ; le clone-chat scelle toujours en dernier) ; la boucle coherence §0 (reliquat G1) se résout via G5 (§0 → v1.7.26).
- `correct-work(groupe)` après chaque groupe (max 2 rounds de correction par groupe — §5.4).
- `correct-work (projet) --bloc` en fin de chaîne (double rôle : clôture + vérification D006).
- **Graph Diamond** (philosophie #4) : parallélisation par défaut des tâches ET commandes prouvées indépendantes (ex : verdicts tsi-validator ×6, arbitres) ; série justifié tracé (dépendances d'ordre, écritures partagées) ; re-verdict resource-monitor entre vagues.
- Statuts dérivés du disque (KO-L003) : `[À FAIRE]` · `[EN COURS]` · `[TERMINÉ]` · `[BLOQUÉ]` · `[REPORTÉ]` + compteurs n/m par sous-groupe/groupe.

## §4 Budget #token (E4) et profil (E6)

| Groupe | Estimation |
|---|---|
| G1 | ~14 k (dont cascade conformité correctif — EXÉCUTÉ : voir statuts) |
| G2 | ~25 k (6 TSI dont 2 volumineux, DIOM ×4) |
| G3 | ~7 k |
| G5 | ~13 k (portage corpus + propagation + recalibrage — ajout E13) |
| G6 | ~11 k |
| **Total** | **~70 k #token** (contingence ×1.3 → ~91 k pire cas) |

**Profil** : NORMAL (G-RES OK) · exécution PARALLELE par défaut.

## §5 Hors périmètre (différés documentés Task 55 — inchangés)

Branche test/compilation-windows@04accb8 · plancher inter-scripts→dessin-technique ≥1.3.0 · précision verdicts orchestrateur-tsi · indentation registre alias — reportés (E13 possible sur demande propriétaire).

## §6 Risques et adaptations (règle d'or n°1)

- Recyclage sandbox en cours de chaîne → reprise E1-RES (état dérivé du disque) ; le correctif G1 rend la reprise auto-réparante.
- Fichiers TSI volumineux (4 Mo) : lecture bloc par bloc (philosophie #7), parsing Python stdlib.
- Si divergence mode --bloc constatée en T3.1.3 : correctifs adaptés AVANT le correct-work final (le plan n'est pas re-généré — extension E13 si besoin).

---

## Hooks de validation (E8)

Horodatage plan : 2026-11-06T21:35:00Z

Verdict E8 : PASS (P1 plan présent · P2 answer key 12 décisions/12 vérifications · P3 worklog R5 · P4 PLAN-AFFICHE · P5 frais — Horodatage vérifié : 2026-11-06T21:35:00Z)
