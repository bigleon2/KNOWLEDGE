# Arbitrage des 3 dérives replay iphone (héritées de l'amont) — Task 25 / G2

> **Date** : 2026-10-24 · **Session** : web-fdf5963c · **gen-plan** : v3.23.2 (mode step)
> **Plan** : download/plan-task25-suite-mode-step.md — G2 (armée par directive propriétaire) · décision D002.
> **Source des dérives** : session photos amont (web-38713acd, intégrée en Task 24 G-B) — trigger_evals iphone17/18/19 vs heuristique voie M locale.

## 1. Constat mécanique (re-mesure préalable)

Re-joue de l'arbitre `scripts/check-triggers-replay.py` (KNOWLEDGE-repo) le 2026-10-24 :
**idempotence confirmée** — 101 skills, 81/101 au score maximal, 20 dérives identiques au replay Task 24
(verdict FAIL informatif). Les 3 dérives objet de l'arbitrage sont les 3 skills iphone, portant
**6 cas négatifs échoués** au total :

| # | Skill | Version | Score replay | Cas échoués |
|---|-------|---------|--------------|-------------|
| D1 | iphone17 | 1.1.0 | 7/8 | 1 négatif : « Améliore cette photo au rendu **iPhone 18** Pro Max qualité max. » (attendu false, déclenché, 0.625) |
| D2 | iphone18 | 1.1.0 | 7/8 | 1 négatif : « Fais le rendu **iPhone 17** Pro Max de cette photo. » (attendu false, déclenché, 0.429) |
| D3 | iphone19 | 0.11.0 | 4/8 | 4 négatifs : « Améliore cette photo qualité max. » · « rendu **iPhone 18** Pro Max » · « Restaure ce scan… années 80 » · « Poster A4 300 DPI » (tous attendus false, déclenchés) |

Le cas positif canonique (isométrie CAO → dessin-technique) reste correctement rejeté sur les 3 skills,
et tous les cas positifs déclenchent : la dérive est **exclusivement concentrée sur les cas négatifs
de routage inter-générations/inter-fonctions**.

## 2. Arbitrage par dérive (verdict voie L)

### D1 — iphone17 (1 cas)

**Attendu eval** : un rendu « iPhone 18 Pro Max » ne doit pas déclencher iphone17.
**Référentiel** : description SKILL.md iphone17 v1.1.0 — PÉRIMÈTRE D'ÉPOQUE, « supersédée par le skill
iphone18 », pipeline opérationnel « pour un rendu génération 17 **demandé explicitement** ».
**Verdict : CONFIRME l'eval.** L'attendu est conforme au référentiel : un rendu 18 doit router vers
iphone18. La dérive provient de l'instrument : l'heuristique voie M (SHARED §7 v2, réplique harnais
Task 19, zéro API) compte des mots-clés **partagés** entre les 3 générations (iphon, photo, amelior,
qualit, rendu) — aucune discrimination générationnelle possible sans sémantique.

### D2 — iphone18 (1 cas)

**Attendu eval** : un rendu « iPhone 17 Pro Max » ne doit pas déclencher iphone18.
**Référentiel** : miroir exact de D1 — le rendu 17 appartient au périmètre d'époque d'iphone17.
**Verdict : CONFIRME l'eval.** Même limite instrument (mots-clés iphon/photo/rendu partagés).

### D3 — iphone19 (4 cas)

**Attendu eval** : les 4 requêtes (amélioration générique, rendu 18, restauration de scan ancien,
poster A4 300 DPI) ne doivent pas déclencher iphone19.
**Référentiel** : description SKILL.md iphone19 v0.11.0 — génération ANTICIPÉE 2027, déclenchement
« dès que l'utilisateur demande **explicitement** le rendu « iPhone 19 » ou la génération suivante,
ou le preset iphone19_max — **pour la génération CONFIRMÉE courante (iPhone 18), préférer le skill
iphone18** ». Les 4 requêtes relèvent donc canoniquement d'iphone18 (défaut, « même sans mentionner
« iPhone » »).
**Verdict : CONFIRME les 4 evals.** Même limite instrument : restauration, poster, mode série et
amélioration sont des capacités **partagées** par les 3 skills (mêmes sections descriptives), donc
non discriminables par mots-clés.

## 3. Verdict global d'arbitrage

| Décision | Valeur |
|----------|--------|
| Verdict par dérive | **3/3 CONFIRME-eval** (6/6 cas) — les trigger_evals sont conformes aux descriptions SKILL.md |
| Nature des dérives | **Limites documentées de l'heuristique voie M** : cas négatifs de routage inter-générations/fonctions, non discriminables par mots-clés partagés |
| Révision eval / SKILL.md | **0** — aucun correctif de livrable |
| Recalibrage KO-L004 | **Non requis** (0 bump semver, 0 cascade) |
| Verdict replay global | FAIL **informatif maintenu** (politique Task 22/24 : 0 fix instrument) — le FAIL ne masque aucune régression : 0 nouvelle dérive, idempotence ×2 |
| D002 | **executed** — 0 dérive iphone restante non arbitrée |

## 4. Résorption optionnelle (décision propriétaire, hors périmètre du présent arbitrage)

- **Option A — extension de schéma** : champ de mots-clés exclusifs dans `trigger_evals.json`
  (ex : « iphone18 » exclusif pour iphone17) — mécanisable dans l'heuristique voie M, mais impact
  cross-skills (schéma canonique skill-creator, harnais, certification) → campagne dédiée.
- **Option B — voie L sur les cas négatifs cross-skill** : routage sémantique par LLM pour les
  négatifs (coût API, sortie non déterministe à neutraliser).
- **Option C — statu quo documenté** : replay FAIL informatif assumé, arbitration tracée dans le
  présent rapport (état recommandé par défaut tant que la campagne A/B n'est pas armée).
