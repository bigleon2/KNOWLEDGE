# Plan — Task 97 : mission dédiée arbitre V6.2 (écart cas 6 voie M) + check N1 calibré sur la KB (proposition VALIDÉE) + correct-work (projet) --bloc + clone-chat + PUSH

**Directive propriétaire** trace `1a1df48b3eb8fb9d` (gen-plan mode step — 5 items exécutés dans l'ordre) : (1) « PUSH avec ma clé <PAT frais fourni dans la discussion> » ; (2) « lance $FACON la mission dédiée à l'arbitre V » ; (3) « je valide la proposition future check N1 skill calibré sur le périmètre KB » ; (4) « correct-work (projet) --bloc » ; (5) « clone-chat ».
**Référentiel à l'ouverture** : HEAD `b49c072` (Task 96 SUIVI) · worklog dernière entrée suite 138 (parité hôte/dépôt 2 289 lignes) · cron cadence 531684 ACTIF (3 ticks/jour, prochain 15:00 CET — ré-armage de secours suite 138) · arbitres ×6 AU VERT (suite 138) · 2 commits en attente de PUSH.

---

## Enquête E1-E2 (read before planning — exécutée avant plan, mode step item par item)

- **Item 1 PUSH : EXÉCUTÉ AVANT PLAN (ordre directive)** : push `2d37797..b49c072` (commits Task 96 CLOSE `111e356` + Task 96 SUIVI `b49c072`), vérification ls-remote = HEAD `b49c072` — **0 unpushed, pendance PUSH ÉTEINTE** — E15 : 20ᵉ exposition (PAT frais trace 1a1df48b3eb8fb9d, 1ʳᵉ utilisation ; KO-L009 : jeton en mémoire de commande uniquement, jamais git config ni fichier).
- **Écart cas 6 voie M (la pendance, décision DONNÉE item 2)** : arbitre = `scripts/check-triggers-replay.py` V6.1 (voie M : réplique SHARED §7 v2 — `trig = ≥ 2 hits OU radical du nom ∈ strong` ; couches V6.1 : veto exclusifs → voie M → cache voie L). Baseline rejeu frais : **97/101** — 4 dérives : agent-engineering 6/7 [cas 6 « Lance une flotte d'agents en parallèle… » attendu False, hits {agent, flott} : strong « agent » + « flott » venu de la clause d'exclusion de la description A10/A14 — ironie structurelle : l'exclusion documentée alimente les keywords] ; correct-work 7/8 [cas 6 identique à une positive de gen-plan] ; midi-doc-expert 5/6 [cas 5, voisine tsi-validator jaccard 0,2] ; re-curation 9/12 [cas 1/7 : faux négatifs lexicaux « re-cure » vs nom « curation » ; cas 10 : sans voisine forte]. Diagnostic par simulation (harnais dédié, 101 skills équipés) : les requêtes POSITIVES des corpus des autres skills encodent le périmètre → règle candidate **V6.2 « réservation de corpus croisée »**.
- **Check N1 (proposition VALIDÉE item 3)** : `check-tool-routing.py` — périmètre N1 « skill » dérivé du registre KB `skills/KNOWLEDGE.md` (55 entrées, source de vérité) au lieu du scan du répertoire ; 65 skills miroirs plateforme hors registre (ASR, LLM, TTS, VLM, docx, pdf, pptx, xlsx, aminer-*, gaokao-*…) → exemption typée ; bénéfice : certification reproductible indépendante du périmètre de diffusion des cascades (échec N1 5/6 Task 95 résorbé).
- **Routage (N2)** : éléments touchés = arbitre [script → script-creator + correct-work en vérification] + plan/worklog [gen-plan] + rapports download/ [hors routage N1] ; aucun skill KB / agent / registre KB modifié.

## G1 — Mission arbitre V6.2 (item 2) : réservation de corpus croisée

1. SIMULATION PRÉALABLE (règle d'or n°5 — mesurer avant corriger) : harnais `scripts/task97-simulation-v62.py` (réplique exacte voie M, diagnostic S2 des voisines positives, balayage S3 de 7 seuils, reco S4) → rapport `scripts/task97-simulation-report.json`.
2. Implémentation V6.2 dans `check-triggers-replay.py` : couche 4 APPLIQUÉE EN DERNIER, uniquement sur les cas non résolus par (veto → voie M → cache voie L) — garde (a) : un cas résolu ne peut jamais régresser ; réservation si requête IDENTIQUE (normalisée) à une positive d'un autre skill OU Jaccard radical ≥ 0,7 avec ≥ 3 radicaux partagés — garde (b) : une requête aussi positive du corpus courant (corpus jumeaux aminer-*/gaokao-*) n'est jamais réservée ; source `v62-reservation-corpus`.
3. Rejeu global attendu : **99/101** — agent-engineering **7/7 (PENDANCE ÉTEINTE)**, correct-work 8/8 (bonus), 0 régression ; voie M brute inchangée (transparence).
4. $FACON2 : idempotence ×2 (rapport byte-identique) ; performance médiane ×3 vs V6.1 (garde < 30 %) ; adaptation autonome : chemin git mort `work_knowledge` → `str(BASE)` (date du rapport déterministe rétablie).
5. Résidus documentés (nouvelles pendances R5, hors périmètre pendance) : midi-doc-expert 5/6 (extinction : champ `exclusifs`) ; re-curation 9/12 (cas 1/7 : extinction par lexique description/tags ; cas 10 : extinction par champ `exclusifs`).

## G2 — Check N1 calibré sur le registre KB (item 3, proposition VALIDÉE)

1. `check-tool-routing.py` : `kb_registry_names()` (55 entrées « ## nom vX.Y.Z ») ; `classify` → « skill » (KB : check profond frontmatter skill-creator §2 INCHANGÉ) vs « skill hors KB » (exemption typée, comptée et signalée dans le rapport) ; routage N2 skill-creator non exigé pour les miroirs.
2. Tests : T1 couche courante PASS ; T2 miroir touché (rejeu du scénario Task 95) → PASS avec exemption typée ; T3 garde inverse : skill KB sans frontmatter → N1 FAIL (sévérité KB intacte) ; arbre skills restauré propre + re-jeu PASS final.

## G3 — correct-work (projet) --bloc (item 4)

Blocs explicites B1-B4 (B1 PUSH item 1 · B2 mission V6.2 · B3 check N1 KB · B4 worklog + arbitres + commit), Étapes 2-5 par bloc, verdict PAR BLOC, agrégation pire-des-verdicts, table « Blocs vérifiés » ; rapport `download/rapport-cw-task97-bloc.md` ; `verify-correct-work.py` 16/16 ; alias-eco Phase 2 (phrases récurrentes du tour).

## G4 — clone-chat (item 5)

16ᵉ clone, lignée Task 72→97, prédécesseur clone task95, suites 136-140 couvertes, scellé 8/8 S1-S8 (étape 11 PM-INSTALL).

## G5 — Worklog + miroirs + arbitres ×6 + commit + PUSH + résumé

Suites 139-140 parité hôte/dépôt ; miroirs download/ ×2 (plan + rapport CW + clone) ; arbitres ×6 AU VERT avant commit (certification-complete + tool-routing sur couche scripts N1) ; **COMMIT « Task 97 CLOSE » + PUSH** (E15 : 21ᵉ exposition — 2ᵉ utilisation PAT frais, rotation recommandée après) ; résumé concis au propriétaire TOUJOURS en français (règle d'or n°6).

---

## Answer key (preuves vérifiables par décision)

| ID | Décision | Preuve mécanique |
|----|----------|------------------|
| D001 | PUSH 2 commits effectué, 0 unpushed | push `2d37797..b49c072` + ls-remote = HEAD `b49c072` |
| D002 | Écart cas 6 voie M agent-engineering ÉTEINT | triggers-replay-report.json : agent-engineering 7/7, cas 6 source `v62-reservation-corpus` (fleet-engineering, jaccard 0,727, inter 8) |
| D003 | V6.2 : 0 régression | rejeu 99/101 (97 OK inchangés + correct-work 8/8 bonus — garde (a) : couche sur non-résolus seulement) |
| D004 | V6.2 idempotence + performance | 3 SHA byte-identiques du rapport + médiane ×3 : 0,121 s → 0,146 s (+20,7 % < garde 30 %) |
| D005 | Check N1 KB : miroirs exemptés, KB strict | T2 PASS (exemption typée) + T3 FAIL (garde inverse) + re-jeu final PASS arbre propre |
| D006 | Résidus triggers documentés avec voies d'extinction | plan G1.5 + worklog suite 139 (midi-doc-expert 5/6, re-curation 9/12) |
| D007 | correct-work --bloc PASS | rapport B1-B4 + verify-correct-work 16/16 + agrégation pire-des-verdicts |
| D008 | clone-chat scellé | clone 8/8 S1-S8, lignée Task 72→97 |
| D009 | Arbitres ×6 AU VERT avant commit | certification-complete ALL PASS + check-tool-routing PASS (couche = scripts, N1 compilable+docstring) |
| D010 | Commit + PUSH + E15 + résumé français | git log « Task 97 CLOSE » + ls-remote + worklog suites 139-140 + réponse finale |

*Plan Task 97 — gen-plan mode step v3.43.0, enquête E1-E2 terminée (baseline arbitre rejouée 97/101 · registre KB 55 entrées vs 65 miroirs · simulation V6.2 101 skills · PUSH exécuté item 1).*
