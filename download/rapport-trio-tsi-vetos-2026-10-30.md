# Rapport — Résorption des dérives voie M du trio TSI (vetos exclusifs doctrinaux)

> **Task 6 / G2** · Session web-eb6c8580 (continuation 4) · 2026-10-30 · gen-plan v3.28.1 (mode NULL)
> Décisions : D003-D006 du plan `download/plan-task6-publication-trio-tsi-voie-l.md`

## 1. Contexte

L'arbitre V6.1 (`scripts/check-triggers-replay.py`, rejeu 2026-10-30 pré-vol) constatait 3 skills en dérive voie M (5 cas `non-resorbe` : requêtes négatives marquant ≥ 2 radicaux partagés alors qu'elles doivent router vers le skill sœur) :

| Skill | Score avant | Cas dérivants |
|-------|-------------|---------------|
| midi-doc-expert | 5/6 | « Valide la conformité de ce TSI au schéma de référence. » |
| tsi-architect | 4/6 | « Valide ce fichier TSI et liste-moi toutes les erreurs. » · « Génère la documentation du Freeze Mode avec tableaux MIDI et états LED. » |
| tsi-validator | 4/6 | « Conçois l'architecture d'un nouveau mapping TSI complet. » · « Documente ce mapping avec un tableau de référence MIDI. » |

Le trio est **local à l'hôte** (créé 2026-10-26, session « TSI Agents » : spec-first EF-01→EF-12/ENF-01→ENF-06, 3 agents + 4 skills, batterie 8/8 ×2, certification 111/111 + 78/78) — jamais publié au dépôt, hors registre KB (état hérité, constat S4 sans action : la publication du trio est une décision propriétaire hors périmètre).

## 2. Doctrine (discussions intégrées au pré-vol)

Deux discussions partagées par le propriétaire ont été récupérées intégralement (adaptations journalisées règle d'or n°1 : WAF chat.z.ai contourné par z-ai function `page_reader` + agent-browser double-open) :

- **TSI Agents** (2026-10-26) : création du trio — doctrine **complémentaire par conception** : tsi-architect = méthode/SOURCE DE VÉRITÉ (délègue l'exécution à l'agent homonyme), tsi-validator = arbitre mécanique PASS/FAIL (E1-E8), midi-doc-expert = génération doc MD+JSON déterministe. Les descriptions se citent mutuellement (« La validation mécanique relève du skill tsi-validator (garde obligatoire : jamais de mapping livré sans verdict PASS) »).
- **LEON TSI EDITEUR** (2026-10-22) : le projet source — éditeur TSI full-stack S4 MK2 (format TSI rétro-ingénierié byte-exact, catalogue 388 commandes/39 catégories/62 enums, Web MIDI) — confirme la frontière historique conception / validation / documentation du périmètre TSI.

**Frontière des verbes directeurs** encodée dans les vetos :

| Verbe directeur (exclusif) | Skill sœur réservée |
|----------------------------|---------------------|
| « valide la conformité » / « valide ce fichier » | tsi-validator (verdict PASS/FAIL mécanique) |
| « génère la documentation » / « documente ce mapping » | midi-doc-expert (génération doc) |
| « conçois l'architecture » | tsi-architect (méthode d'architecture) |

## 3. Mécanisme appliqué (canon Task 30 — campagne A/B/C, commit af303cc)

Champ optionnel `exclusifs` ajouté aux 5 cas négatifs (champ doctrinal additif, **0 bump** — précédents : 14 vetos / 11 corpus, Task 30 ; Task 27-A) : si la requête contient un terme réservé (comparaison normalisée insensible casse/accents), l'arbitre V6.1 rend false immédiat (source `veto-exclusif`), avant tout scoring mots-clés.

Script `scripts/trio-tsi-vetos.py` : éditions protégées (assert count==1 par requête, garde doctrinale substring ⊂ requête normalisée, garde should_trigger=False) · **idempotent** (rejeu ×2 : 5 ajoutés → 0 ajouté/5 déjà présents, no-op).

## 4. Verdicts (rejeu arbitre V6.1 host)

| Mesure | Avant | Après |
|--------|-------|-------|
| midi-doc-expert | 5/6 (DÉRIVE) | **6/6** (1 veto-exclusif) |
| tsi-architect | 4/6 (DÉRIVE) | **6/6** (2 veto-exclusif) |
| tsi-validator | 4/6 (DÉRIVE) | **6/6** (2 veto-exclusif) |
| Verdict global | FAIL (3 dérives) | **PASS — 47/47 skills au score maximal, dérives : aucune** |
| Sources verdicts | voie-m + 14 veto + non-resorbe ×5 | voie-m 322 · **veto-exclusif 19** (14 + 5 nouveaux) · voie-l-cache 8 |
| cahier-des-charges (non-régression) | 12/12 | 12/12 (inchangé) |

Voie M seule (informatif, transparence Task 30) : 5 skills hérités résolus par cache/veto (agent-prompt-engineering, gen-plan, iphone19, refactor-guard, vue-upload) — FAIL informatif assumé, statu quo documenté Task 30 ; le trio quitte cette liste (résorbé par veto, plus aucun recours au cache).

## 5. Livrables et journalisation

- Corpus modifiés (hôte) : `skills/{midi-doc-expert,tsi-architect,tsi-validator}/evals/trigger_evals.json` (champ `exclusifs` ×5)
- Script : `scripts/trio-tsi-vetos.py` (idempotent ×2)
- Journal §6bis (worktree publish) : entrée campagne 2026-10-30 (append-only R2)
- Rapport replay régénéré : `scripts/triggers-replay-report.json` (47/47 PASS)
- Artefacts de pré-vol : `tmp/discussion-tsi-agents.txt` (21,8 Ko) + `tmp/discussion-leon-tsi-editeur.txt` (35,6 Ko)

## Verdict du groupe : **PASS**

D003 ✓ (5 vetos, substrings validés 5/5, 0 bump) · D004 ✓ (6/6 ×3, dérives [], verdict PASS) · D005 ✓ (idempotence no-op) · D006 ✓ (§6bis + présent rapport). Aucune positive touchée (les exclusifs sont par cas, les 13 positives du trio restent voie-m). Constat S4 journalisé : trio hors registre KB/dépôt (état hérité, publication = décision propriétaire).
