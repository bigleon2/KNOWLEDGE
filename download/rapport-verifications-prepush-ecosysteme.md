# Rapport de vérifications pré-push — écosystème Knowledge

**Session** : B13-r7-c · **Task ID** : 52 · **Date** : 2026-09-27
**Dépôt cible** : `github.com/bigleon2/KNOWLEDGE` · **Commit de référence** : `d9ff9fb5411985282bdb2bbc5ccaf284c18d971f`
**Statut : AUCUN PUSH EXÉCUTÉ** — ce rapport documente les vérifications A/B/C demandées, intégrées au plan d'actions gen-plan **avant** toute opération de push.

---

## 1. Position du commit de référence (préambule)

Le commit `d9ff9fb` a été vérifié par clone frais (`tmp/gh-check-d9ff9fb`) : il existe, et il est **à la fois HEAD et pointe de `main`** du dépôt distant, avec **0 commit en aval**. Conséquence directe : le push local → dépôt se fera en **fast-forward** possible, sans rebasage ni conflit de base. Le périmètre de comparaison ci-dessous a donc la valeur d'un état des lieux à jour de la pointe actuelle du dépôt.

## 2. Vérification A — dossier `skills/@mon-ecosysteme/`

**Tous les fichiers attendus sont présents localement (20/20), aucun manquant, aucun fichier du dépôt absent du local.** Le corpus local compte 20 fichiers contre 15 au dépôt : les 5 supplémentaires sont les versions créées localement depuis l'installation — `PROMPT-MAITRE-GEN-PLAN-v3.12.0.md`, `-v3.13.0.md`, `-v3.16.0.md`, `-v3.17.0.md` et `SYNC-CONTEXT.md` — destinées au push. Sur les 15 fichiers communs, 8 sont **byte-identiques** et 7 divergent : ces 7 divergences sont les fichiers dont les versions locales ont été supersedées (SHARED, INSTALL-ECOSYSTEME ×2, README, PM-CLONE-CHAT v2.0.0, PM-CORRECT-WORK v2.5.1, PM-GEN-PLAN v3.11.0). Chaque divergence correspond à une évolution locale versionnée et documentée (registre KB, worklog, archive v2.1) — aucune n'est une régression. Le miroir `skills/_prompts-maitres/` présente le même profil (8 identiques / 7 divergents / 5 à pousser), ce qui confirme la cohérence corpus ↔ miroir.

**À jour au sens local** : oui — la chaîne de propagation v3.17.0 est complète (10/10 porteurs vérifiés par l'arbitre d'interactions) et l'arbitre d'intégrité certifie le corpus à 49/49 PASS.

## 3. Vérification B — dossiers `skills/` et `scripts/`

### 3.1 Skills écosystème (16 canoniques `ECO_SKILLS`)

| État vs dépôt@d9ff9fb | Skills | Détail |
|---|---|---|
| Conformes (tous fichiers identiques) | — | aucun (tous ont évolué localement) |
| Présents et divergents (9) | gen-plan, correct-work, clone-chat, skills-inventory, skill-creator, context-engineering, loop-engineering, graph-engineering, harness-engineering | divergences = SKILL.md, evals, scripts, références supplémentaires locales (ex. gen-plan : +5 `references/`) |
| **Nouveaux, absents du dépôt (7)** | knowledge-observer, agent-creator, script-creator, script-reviewer, audit-provenance, prompt-engineering, script-mon-ecosysteme-infrastructure | à pousser intégralement |
| Registre `skills/KNOWLEDGE.md` | divergent | versions locales v3.12→v3.17, 15 entrées versionnées |

Faux positif levé au passage : `skills/clone-chat/références/clone-template.md` apparaissait « absent local » à cause du quottage UTF-8 de `git ls-tree` (`core.quotepath`) ; réintégré avec `quotepath=false`, il est **présent et byte-identique**.

### 3.2 Scripts

`scripts/` local compte **118 fichiers contre 23 au dépôt** : 4 byte-identiques (`_archive/generate-clone-genplan.py`, `_archive/generate-knowledge-v3.py`, `git-deploy.sh`, `lexique-domain.json`), **19 divergents** (les arbitres recalibrés : `verify-cross.py`, `check-ecosysteme-integrity.py`, `test-coherence-interactions.py`, `sync-download.py`, `verify-correct-work.py`, etc.), **95 absents du dépôt** (outillage créé localement : `n60b-genplan-3170.py`, suite `t50-*`/`t51-*`, arbitres d'arbitrage b10-b12, scripts d'installation et de restauration…) et **0 absent du local**. Rien du dépôt ne manque localement.

### 3.3 Fraîcheur mécanique (arbitres exécutés en fin de session)

| Arbitre | Résultat |
|---|---|
| `check-ecosysteme-integrity.py` | **49/49 PASS**, 0 FAIL — manifeste SHA-256 régénéré |
| `verify-cross.py` (6 axes) | **98,2 %** — 0 ERROR, 1 WARNING hérité (frontmatter plateforme, S3) |
| `verify-cross.py --mode correct-work` | **98,2 %** — 0 ERROR |
| `verify-correct-work.py` | **16/16 ALL PASS** |
| `test-coherence-interactions.py` | **43 PASS / 3 WARN stables P5 / 0 FAIL** — PASS AVEC RÉSERVES |

Les trois WARN résiduels sont les avertissements hérités déjà documentés (frontmatter des skills plateforme, regex KB format liste) — zéro échec introduit par les sessions locales.

## 4. Vérification C — compatibilité locale ↔ GitHub@d9ff9fb

**Verdict : COMPATIBLE — l'écosystème local est un sur-ensemble strict du dépôt.** Aucun fichier du dépôt n'est absent du local (vérification A : corpus 0 absent local ; vérification B : 0 absent local sur skills et scripts). Toutes les divergences vont dans le sens local → dépôt et correspondent à des évolutions versionnées, certifiées par les arbitres ci-dessus : nouvelles versions gen-plan v3.12→v3.17, correct-work v2.6.0, 7 nouveaux skills écosystème, registre KB à 15 entrées, outillage étendu. Le côté plateforme (74 répertoires métier comparés : 976 fichiers identiques, 73 divergents) relève d'une décision distincte : ces divergences proviennent des mises à jour Z.ai de la plateforme postérieures à l'installation et **ne font pas partie du périmètre écosystème** (héritage S3 documenté dès l'installation).

## 5. Recommandations avant push

1. **Périmètre écosystème (recommandé)** : `skills/@mon-ecosysteme/` (20), `skills/_prompts-maitres/` (20), `skills/KNOWLEDGE.md`, les 9 skills écosystème divergents, les 7 nouveaux skills, `scripts/` (118). Ce périmètre forme un état cohérent certifié 49/49 + 16/16 + 43/0.
2. **Périmètre plateforme (à décider explicitement)** : pousser ou non les 73 répertoires métier divergents. Recommandation : les exclure du push écosystème, ou faire un commit séparé clairement étiqueté, car leurs différences viennent de la plateforme et non de votre travail.
3. **Exclusions à confirmer** avant push : `__pycache__/`, `*.pyc`, `.next/`, `tmp/`, rapports d'exécution (`interactions-report.json`, `ecosysteme-integrity.json` — ou les pousser en tant qu'attestations, au choix).
4. **Aucune action de push n'a été exécutée** dans le cadre de cette task — le plan gen-plan positionne ce rapport comme garde A/B/C préalable ; le push reste à votre décision.

*Rapport mécanique complet : `rapport-verifications-prepush-ecosysteme.json` (comparaison SHA-256 fichier à fichier, corrections incluses). Outil persisté rejouable : `scripts/t52-prepush-compare.py`.*
