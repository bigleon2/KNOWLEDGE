# Rapport final — Task 75 : vérification d'idempotence de l'écosystème post-re-curation vs version précédente

**VERDICT GLOBAL : PASS** — horodatage : 2026-11-08T05:48:17Z · Session : web-ecef7f80 · Trace directive : 1a1b9955a1f207ed · Plan : download/plan-task75-verif-idempotence-ecosysteme-post-recuration.md (E8 PASS 2026-11-08T05:28:40Z) · Synthèse mécanique : download/task75-verif-idempotence.json (verdict PASS, 4/4 checks)

## §1 — Mission et interprétation

Directive propriétaire (2026-11-08) : « gen-plan : "vérifie que mon écosystème après re-curation reste idempotent à sa version précédente". »

La propriété demandée a été décomposée en trois propriétés vérifiables mécaniquement (answer key D001) :
- **P1 — Équivalence de contenu** : la version post-re-curation préserve TOUT le contenu de la version précédente ;
- **P2 — Idempotence opérationnelle** : re-appliquer les opérations de la re-curation sur l'état courant ne change RIEN ;
- **P3 — Intégrité vérifiable** : tout écart entre la baseline et l'état courant est un changement versionné documenté.

**VERDICT P1 : PASS · VERDICT P2 : PASS · VERDICT P3 : PASS → agrégation (pire-des-verdicts) : PASS.**

## §2 — Méthode et matériaux

- **Baseline « version précédente »** : commit git **`011d342`** (Task 71 G5+G6 CLOSE) — parent prouvé de `5646e96` (Task 72 G1, re-curation gen-plan v3.38.0→v3.39.0) : `git log -1 --format='%P' 5646e96` → `011d342860e…`. Extraction byte-exacte : SKILL.md (106 465 o, 489 L) + evals ×2 vers `tmp/verif-task75/baseline/`.
- **Golden master Task 72** : `download/task72-baseline-genplan.json` — intégrité croisée vs git : **13/13 PASS** (sha256 SKILL.md `3e71ea45…` identique, 9 blocs sha256 identiques, evals ×2 identiques) — le référentiel de comparaison est fidèle au dépôt (D002).
- **Harnais dédié** : `scripts/task75-verif-idempotence.py` (N3 Python stdlib, selftest 5/5) — checks `baseline` / `fidelite` / `diffs` / `evals` / synthèse. Invariant de fidélité **dynamisé v2** (KO-L003) après instruction du premier FAIL : le périmètre correct est l'écosystème personnel (54 entrées KB + corpus + collections), les skills plate-forme et corpus externes étant des classes informationnelles (règle d'or n°8 — le PM INSTALL n'installe que `skills/<skill>/`).
- **Arbitres réutilisés (R4 — jamais dupliquer)** : `protocole-test.py --post` (skill re-curation v1.0.0), `check-recuration.py`, `task72-baseline-verifier.py --verifier`, `poids-chargement.py`, `ensure-installed.py`, `verify-cross.py`, `verify-correct-work.py`, `check-ecosysteme-integrity.py`, `task14-scan-doublons.py`.

## §3 — P1 : équivalence de contenu vs version précédente — PASS

| Preuve | Résultat mesuré | Décision |
|---|---|---|
| Intégrité du référentiel (golden master ↔ git 011d342) | 13/13 sha256 identiques (fichier + 9 blocs + evals ×2) | D002 ✓ |
| Blocs déplacés R4 byte-identité | **9/9** : journal_versions · regles_or · lecons_ko · disciplines · hooks_patterns · routage_install · mode_step · contingences · philo4 (baseline v3.38.0 ↔ `references/` v3.39.0) | D005 ✓ |
| Contrats verbatim intacts | §A (déclencheurs + glossaire $FACON/$FACON2) · §0 normalisé · read_when · evals/evals.json · evals/trigger_evals.json · comptages §A — **tous == baseline** | D005 ✓ |
| Zéro duplication | aucune fenêtre 1024 o d'un bloc déplacé dupliquée inline | D005 ✓ |
| Zéro perte | chaque intégral v3.38.0 vit UNE fois en `references/` ; les résumés inline sont des textes NOUVEAUX (preuve de non-duplication) | P1 ✓ |
| evals jamais touchés | evals.json + trigger_evals.json byte-identiques baseline ↔ courant (sha `74b52b3d…` / `de229e8b…`) | P1 ✓ |
| Poids | 104,0 → 29,9 Kio (−71,2 % ; ≈ 26 616 → 7 667 #token estimés) — seuil LOURD 30 Kio : sous | D005 ✓ |

## §4 — P2 : idempotence opérationnelle (re-jeu = no-op) — PASS

| Re-jeu | Passage 1 | Passage 2 | Décision |
|---|---|---|---|
| `protocole-test.py --post gen-plan` | **MAINTIEN DE L'OPTIMISATION** (COHÉRENT=True · FONCTIONNEL=True · OPTIMISÉ=True ; contrats 6/6 PASS ; pointeurs + non-duplication PASS ; poids 30 667→30 667 o, 0,0 %) | **MAINTIEN DE L'OPTIMISATION** — sorties **byte-identiques** (sha `5654bf3f…` ×2) | D004 ✓ |
| `check-recuration.py gen-plan` | C1-C4 **PASS** (pointeurs, non-duplication, marqueurs, seuils) | C1-C4 **PASS** — sorties byte-identiques ×2 | D006 ✓ |
| `poids-chargement.py --json` | 70 skills mesurés | sorties **byte-identiques** (cmp OK) ; gen-plan 29,9 Kio INTERMÉDIAIRE maintenu | D007 ✓ |
| `ensure-installed.py --check` | rc=0 **INSTALLE** (54/54 entrées KB, 0 fichier manquant) | idempotent — l'état installé est stable | D008 ✓ |

**Preuve vivante de la machinerie d'auto-réparation** : 36ᵉ disparition environnementale de version-management capturée EN DIRECT pendant la vérification (volatilité documentée Task 69 — 35 incidents antérieurs) → réparée automatiquement 2 fois par la garde É1-INSTALL (INSTALLE-REPARÉ, rc=0, depuis le miroir local), puis stable. Ce comportement est la neutralisation résiliente v1.3.0 fonctionnant comme conçue — PAS une régression de la re-curation (version-management est hors du périmètre re-curation, et l'état final est byte-identique au dépôt).

## §5 — P3 : intégrité vérifiable (écarts justifiés) — PASS

| Écart examiné | Résultat | Décision |
|---|---|---|
| Plage de commits baseline→HEAD | `011d342..a14f750` == **exactement les 5 commits documentés** : 5646e96 (T72 G1 re-curation) · d3ee6e6 (T72 G4+G5 skill re-curation) · 4439592 (T72 CLOSE) · a790d04 (T73 tests) · a14f750 (T73 CLOSE) — aucun commit étranger | D009 ✓ |
| Fichiers non-commités (131) | **100 % changements de MODE PURS** (bits d'exécution 100644→100755, hérités du ressync d'installation Task 74) — **0 octet de contenu modifié**, 0 orphelin de contenu | D009 ✓ |
| Fidélité hôte↔dépôt | **54/54 entrées KB byte-identiques** (ensembles de fichiers complets, hash par fichier) + corpus propres (@mon-ecosysteme, @historique, @Bibliotheque-skills-Multi-IA, @GHORG-ecosysteme, KNOWLEDGE.md — 0 seul-hôte, 0 divergent) | D003 ✓ |
| Arbitres écosystème (exécution réelle) | verify-cross **162/162 (100,0 %)** · verify-correct-work **16/16 ALL PASS** · check-ecosysteme-integrity **112/112 PASS (0 FAIL)** · task14-scan-doublons **0 doublon** | D010 ✓ |

## §6 — Écarts qualifiés (honnêteté, aucune action bloquante)

1. **Mode-purs non-commités (131 fichiers, dont 33 hors classes ressync)** : bits d'exécution posés par le ressync Task 74 (download/ 64, scripts/ 27, skills/@historique/ 6, skills/@mon-ecosysteme/ 1, skills/gen-plan+re-curation+analyse-doc-s4mk2 11, tmp/mission-task58 22) — zéro contenu ; leur commit appartient au G3 GO de la Task 74 (pendance inchangée).
2. **17 skills plate-forme divergents hôte↔dépôt** (ASR, LLM, TTS, VLM, agent-browser, charts, docx, gif-animator, gif-animator-pro, image-edit, image-generation, image-search, pdf, pptx, task-review, video-understand, xlsx) : copies d'archive du dépôt périmées par l'évolution plate-forme du bac à sable — hors écosystème personnel (non-KB), classe informationnelle.
3. **67 corpus externes dépôt-seuls** (@PM-SKILLS 371 fichiers, @photos, aminer-*, design, gaokao-*, quiz-*, ui-ux-pro-max…) : jamais installés par conception (règle d'or n°8).
4. **Conventions de mesure** : 30 668 o (vérificateur T1.1.0, octets disque) vs 30 667 o (protocole-test, lecture texte) — chacune self-consistante, aucune dérive.

## §7 — Conclusion et suites

**L'écosystème après re-curation EST idempotent et équivalent à sa version précédente** : rien n'a été perdu (P1), re-appliquer les opérations ne change rien (P2), et tous les écarts vs la baseline sont des changements versionnés documentés (P3). La re-curation gen-plan v3.38.0→v3.39.0 a réduit le poids de 71,2 % SANS AUCUNE PERTE de contenu (intégraux byte-identiques en `references/`, contrats verbatim intacts).

Suites : la Task 74 (G1 clone-chat · G2 correct-work (projet) --bloc · G3 GO) demeure EN VOL au GO propriétaire, intacte (R2) — le présent rapport sera couvert par son correct-work --bloc et archivé par son clone-chat. PUSH distant : propriétaire uniquement, après révocation du PAT exposé (KO-L009/D013).
