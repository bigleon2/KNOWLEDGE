# Rapport correct-work(aveugle) — PMs CORRECT-WORK v2.6.0 / v2.7.0 reconstitués

> **Session** : continuation web (Task 17) · 2026-10-02 · **Mode** : AVEUGLE (Second Opinion — verification-protocol.md v1.0.0)
> **Cibles** : `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.6.0.md` (SHA 45dfedb4812e7430) · `PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` (SHA dc52a5b5eaa808ae)
> **Motivation** : suggestion ③ de la clôture Task 16 — « re-vérification sans biais » des PMs reconstitués ; directive utilisateur « fais (3) ».

## 1. Inputs filtrés (ce que l'instance aveugle a vu)

| Voit | Ne voit PAS |
|---|---|
| Les 2 PMs livrés + la lignée corpus v2.4.0/v2.5.0/v2.5.1 | Le rapport d'application Task 16 et ses justifications |
| La forme installée certifiée (SKILL.md v2.7.0, evals/, references/verification-protocol.md) | Le worklog Task 16 et les messages de construction |
| Conventions de référence (SHARED v1.6.4 §3.2/§4.4, SYNC-CONTEXT v1.4.1 note N1, décision KB N20) | Les verdicts préliminaires de la vérification contextuelle |
| Arbitrages mécaniques (SHA-256, comptages, diffs) | |

## 2. Cadrage à froid — critères pré-écrits (étape 1 du protocole)

- C01 En-tête PM conforme à la lignée (titre, version prompt, skill cible, date, source, dépend CONTEXTE SYSTÈME, provenance)
- C02 Bloc CONTEXTE SYSTÈME embarqué byte-identique à celui de v2.5.1 (bloc figé hérité — SYNC-CONTEXT v1.4.1 note N1)
- C03 Carte des sections : surensemble de v2.5.1 (§A, §1-§10b toutes présentes)
- C04 §4 YAML PM v2.7.0 == frontmatter installé SKILL.md v2.7.0 (contrat d'assemblage PM → skill)
- C05 §4 YAML PM v2.6.0 : version 2.6.0, structure frontmatter conforme à la lignée
- C06 v2.6.0 : 4e mode AVEUGLE documenté (§1.2/§10) + déclencheur correct-work(aveugle) + hook 2nd opinion Étape 5 + max 2 rounds (SHARED §4.4)
- C07 v2.6.0 : protocole Second Opinion embarqué au §5.6 (4 étapes + inputs filtrés + garde anti-boucle)
- C08 v2.7.0 : couplage gen-plan OBLIGATOIRE Étape 1 + résolution dynamique frontmatter → KB + ARRÊT EXPLICITE
- C09 v2.7.0 : fin du mode autonome — directive propriétaire 2026-10-02 citée
- C10 Traçabilité N20 : marqueurs « phase N20 » / décision KB N20 présents dans v2.6.0
- C11 Planchers §3 RELATIONS inchangés vs v2.5.1 (SHARED §3.2 règle 5 — aucun changement de contrat d'intégration)
- C12 §5.4 trigger_evals : v2.5.1 = 8 cas, v2.6.0 = 8 cas (héritage), v2.7.0 = 7 cas (aligné forme installée — evals/trigger_evals.json)
- C13 Plage check 2 §6 du PM v2.7.0 contient le nombre de lignes réel de la forme installée (429)
- C14 §7 historique : lignée complète v2.4.0 → v2.5.0 → v2.5.1 (partie héritée byte-identique à v2.5.1) + lignes v2.6.0/v2.7.0 + révisions documentaires tracées (aucun faux lignage)
- C15 §8 historique des corrections inchangé vs v2.5.1
- C16 Diffs bornés : aucun hunk hors périmètre documenté (CONTEXTE SYSTÈME, §3, §8 intacts ; hunks classables en-tête/versions/modes/protocole/provenance/§9.5)
- C17 Provenance explicite en en-tête et §7 des deux PMs reconstitués (méthode B1, sources citées)

## 3. Vérification aveugle — résultats (étape 2)

| # | Critère | Verdict | Détail |
|---|---|---|---|
| 1 | C01[2.6.0] | PASS | titre='# PROMPT MAÎTRE — Installation du skill correct-work v2.6.0' |
| 2 | C01[2.7.0] | PASS | titre='# PROMPT MAÎTRE — Installation du skill correct-work v2.7.0' |
| 3 | C02[2.6.0] | PASS | bloc identique à v2.5.1 : True (len 579 vs 579) |
| 4 | C02[2.7.0] | PASS | bloc identique à v2.5.1 : True (len 579 vs 579) |
| 5 | C03[2.6.0] | PASS | sections manquantes : aucune — carte ['§0', '§1', '§10', '§10b', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§A'] |
| 6 | C03[2.7.0] | PASS | sections manquantes : aucune — carte ['§0', '§1', '§10', '§10b', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§A'] |
| 7 | C04[v2.7.0] | PASS | byte-aligné (délimiteurs --- du bloc §4 exclus — convention lignée) |
| 8 | C05[v2.6.0] | PASS | version déclarée : 2.6.0 |
| 9 | C06[v2.6.0] | PASS | marqueurs : AVEUGLE ✓  |
| 10 | C06[v2.6.0]-modes | PASS | énumération 4 modes ×2 |
| 11 | C07[v2.6.0] | PASS | §5.6 présent : True ; protocole (Second Opinion + inputs filtrés) présent |
| 12 | C07[v2.6.0]-bloc | PASS | bloc §5.6 localisé avant §6 |
| 13 | C08[v2.7.0] | PASS | OBLIGATOIRE=True ; ARRÊT EXPLICITE=True ; résolution dynamique frontmatter→KB |
| 14 | C09[v2.7.0] | PASS | directive propriétaire 2026-10-02 citée |
| 15 | C10[v2.6.0] | PASS | occurrences « N20 » : 10 |
| 16 | C11[2.6.0] | PASS | §3 byte-identique à v2.5.1 : True |
| 17 | C11[2.7.0] | PASS | plancher gen-plan préservé : >= v3.7.0 (v2.5.1 : >= v3.7.0) ; nature mise à jour « OBLIGATOIRE » : True |
| 18 | C12[v2.5.1] | PASS | cas = 8 (lignée) |
| 19 | C12[v2.6.0] | PASS | cas = 8 (héritage, aucun changement tracé) |
| 20 | C12[v2.7.0] | PASS | cas = 7 == forme installée (7) |
| 21 | C13[v2.7.0] | PASS | plage [200-450] vs installé 430 L |
| 22 | C14[2.6.0]-héritage | PASS | lignes v2.4.0/v2.5.0/v2.5.1 préservées |
| 23 | C14[2.6.0]-ligne propre | PASS | ligne v2.6.0 présente |
| 24 | C14[2.7.0]-héritage | PASS | lignes v2.4.0/v2.5.0/v2.5.1 préservées |
| 25 | C14[2.7.0]-ligne propre | PASS | ligne v2.7.0 présente |
| 26 | C14[provenance] | PASS | révisions documentaires de reconstitution tracées dans §7 |
| 27 | C15[2.6.0] | PASS | §8 identique à v2.5.1 : True |
| 28 | C15[2.7.0] | PASS | §8 identique à v2.5.1 : True |
| 29 | C16[2.5.1→2.6.0]-protégés | PASS | CONTEXTE SYSTÈME + §8 intacts (§3 classé au C11 — couplage v2.7.0 documenté) |
| 30 | C16[2.5.1→2.6.0]-delta | PASS | delta total ≈ 116 lignes modifiées/ajoutées |
| 31 | C16[2.6.0→2.7.0]-protégés | PASS | CONTEXTE SYSTÈME + §8 intacts (§3 classé au C11 — couplage v2.7.0 documenté) |
| 32 | C16[2.6.0→2.7.0]-delta | PASS | delta total ≈ 60 lignes modifiées/ajoutées |
| 33 | C17[2.6.0] | PASS | en-tête + §7 portent la provenance de reconstitution (méthode B1) |
| 34 | C17[2.7.0] | PASS | en-tête + §7 portent la provenance de reconstitution (méthode B1) |

**Bilan mécanique : 34 PASS / 0 FAIL sur 34 vérifications.**

## 4. Confrontation (étape 3) — matrice de divergence

**Divergences détectées au round 1 puis instruites (KO-L003 — la réalité d'abord) :**

| # | Divergence observée | Instruction | Classification |
|---|---|---|---|
| D1 | C04 FAIL initial : bloc §4 du PM inclut les délimiteurs `---` | Le bloc §4 de la lignée v2.5.1 embarque le frontmatter AVEC ses délimiteurs (convention corpus) — contenu byte-conforme hors délimiteurs | Calibration d'arbitre (faux positif) |
| D2 | C11[2.7.0] FAIL initial : §3 non byte-identique à v2.5.1 | Le hunk §3 = ligne gen-plan « Invocation à E1 (OBLIGATOIRE) — dernière version installée » : exactement le changement documenté v2.7.0 (couplage obligatoire) ; plancher >= v3.7.0 préservé (contrat SHARED §3.2 règle 5 intact) | Critère redéfini (changement documenté, pas une régression) |
| D3 | C16[2.6.0→2.7.0] FAIL initial : région « protégée » §3 modifiée | Même instruction que D2 — §3 sort du périmètre gelé pour v2.7.0 ; CONTEXTE SYSTÈME et §8 demeurent byte-identiques | Critère redéfini (même cause) |

| Verdict initial (contextuel, Task 16) | Critère aveugle correspondant | Convergence (post-instruction) |
|---|---|---|
| §4 byte-aligné frontmatter installé | C04 | CONVERGENCE |
| diffs bornés aux changements documentés (116 + 60 lignes) | C16 | CONVERGENCE |
| provenance tracée, aucun faux lignage | C17 | CONVERGENCE |
| protocole embarqué §5.6 | C07 | CONVERGENCE |

## 5. Verdict consolidé (étape 4)

**VERDICT : PASS** — 34/34 PASS, 0 divergence non résolue.

La re-vérification aveugle, menée à froid depuis les seuls inputs filtrés (lignée corpus, forme installée certifiée, conventions SHARED/SYNC-CONTEXT/KB), **converge** avec la certification contextuelle Task 16 : les deux PMs reconstitués portent les changements documentés (v2.6.0 : 4e mode AVEUGLE + hook 2nd opinion + protocole embarqué §5.6 ; v2.7.0 : couplage gen-plan obligatoire + résolution dynamique frontmatter → KB + ARRÊT EXPLICITE + fin du mode autonome), respectent le contrat d'assemblage (§4 byte-aligné sur le frontmatter installé), préservent les régions protégées de la lignée (CONTEXTE SYSTÈME figé, §3 planchers, §8) et tracent honnêtement leur provenance de reconstitution (aucun faux lignage).

## 6. Journalisation

Round 1 : inputs filtrés listés §1, critères pré-écrits §2, verdicts §3, confrontation §4 — 3 divergences détectées, instruites et documentées (2 calibrations d'arbitre, 1 critère redéfini sur changement documenté) ; re-verdict après instruction : convergence intégrale. Aucun round supplémentaire nécessaire (garde anti-boucle SHARED §4.4 respectée). Rapport JSON mécanique : `scripts/aveugle-pms-report.json`.

## 7. Artefact

Arbitre de session persistant : `scripts/task17-aveugle-pms.py` (rejouable, idempotent — les divergences du premier passage sont conservées dans la matrice §4 et l'historique git).