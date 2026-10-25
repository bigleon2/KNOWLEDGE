# Rapport — Test du bug « GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 »

> **Session** : web-eb6c8580 (suite) · 2026-10-25 · **Plan d'actions** : `download/plan-task2-audit-ecosysteme.md` (Phase C — E11, décisions D003-D007)
> **Méthode** : simulation du canal canonique de montée de version (KO-L004 v1.1.0 / PM-INSTALL §2quater) en **sandbox N0** — refactoring-guard `enabled:false → sandbox_only`, justification : blast radius gen-plan = **CRITIQUE** (backward 17, forward 22 — `scripts/refactoring-test-graph.py --target gen-plan`)
> **Garanties** : golden master SHA-256 scellé AVANT opération (`scripts/audit-phaseC-golden-avant.txt`) ; zéro écriture sur l'état vivant pendant toute la Phase C (D007) ; rollback + re-certification 6/6 en post-vol (C7)

## §1 — Protocole (C1-C7)

Le bug rapporté par le propriétaire — « GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 » — concerne un état **post-b75a620** : à l'état certifié du dépôt, gen-plan est v3.23.1 et aucune trace de v3.24.0 n'existe localement (recoupement `rg "3\.24"` : seule mention = le présent contexte d'audit). La v3.24.0 a donc existé dans la lignée propriétaire sans jamais être commitée. Le test reproduit le **canal canonique** de montée de version — la seule voie normative pour faire exister un PM v3.24.0 — et confronte son produit au golden master v3.23.1 afin de discriminer trois hypothèses :

| ID | Hypothèse | Mécanisme candidat | Discrimination |
|----|-----------|--------------------|----------------|
| H1 | Génération mécanique PM défaillante | Substitutions méthode B1 : motif × n fois → omission silencieuse de blocs plan d'actions (§9/extraction fences, table E1-E15, §4 grille #token, §5.4 hooks) | C3 — diff structurel vs golden master |
| H2 | Dérive sans PM | KO-L004 : PM absent/antérieur au SKILL.md (ABANDON code 2 jamais résorbé → PM-ANTERIEUR) | C2 (issue de la génération) + C3 |
| H3 | Routage déclencheur défaillant | E13 verbatim / clause mode NULL v3.22.1 / trigger_evals ne mappant plus « génère le plan » sur la Phase Planification | C4 — champs trigger + replay 12 cas |

Sandbox : `.staging/sandbox-audit/` (arbre isolé — `skills/gen-plan/` + `skills/@mon-ecosysteme/` + `scripts/generer-pm-skill.py`), jamais connecté à l'état vivant.

## §2 — Reproduction (commandes rejouables)

```bash
# C1 — pré-vol (golden master + blast radius)
sha256sum skills/gen-plan/SKILL.md skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.1.md
python3 scripts/refactoring-test-graph.py --target gen-plan   # → CRITIQUE (17/22)

# C2 — simulation du canal canonique (dans le sandbox)
sed -i 's/^version: 3.23.1/version: 3.24.0/' .staging/sandbox-audit/skills/gen-plan/SKILL.md
python3 .staging/sandbox-audit/scripts/generer-pm-skill.py --generate gen-plan
# → PM écrit : PROMPT-MAITRE-GEN-PLAN-v3.24.0.md (1476 lignes)
# → Recalibrage écrit : SHARED v1.7.8, PM-INSTALL v1.7.2
# → [WARN] couverture gen-plan : sections SKILL.md absentes du PM : §1.13 (complétion agent — KO-L003)
# → EXIT=0

# C3 — diff structurel vs golden master
diff skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.1.md \
     .staging/sandbox-audit/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.24.0.md

# C7 — post-vol (rollback + zéro-régression)
rm -rf .staging/sandbox-audit
sha256sum -c scripts/audit-phaseC-golden-avant.txt && python3 scripts/certification-complete.py
```

## §3 — Diff structurel (C3) : le canal canonique ne peut pas perdre de blocs

Le diff intégral entre le golden master (PM v3.23.1, 1475 L) et le PM v3.24.0 généré (1476 L) montre **exactement 6 points de substitution** — et rien d'autre :

1. Titre : « Installation du skill gen-plan v3.23.1 » → « v3.24.0 » (×1, verrouillé)
2. « Version du prompt » : 1.16.0 → **1.17.0** (piste interne indépendante, `bump_minor` — par design)
3. « Skill cible » : gen-plan v3.23.1 → v3.24.0 (×1, verrouillé)
4. « Date » : 2026-10-11 → 2026-10-25 (×1, verrouillé)
5. Exemplaire YAML `version: 3.23.1` → `version: 3.24.0` (×1, compté — `n_yaml=1`)
6. Ligne d'historique v3.24.0 insérée au-dessus de la ligne v3.23.1 (table §7 **newest-first** — position correcte)

La machinerie de génération de plans est **intégralement préservée** — comptes identiques golden/simulé : « demande explicite de planification » 1/1, « intègre dans le plan d'actions » 4/4, « E1-E15 » 10/10, « answer key » 5/5, « grille » 15/15, « hook » 26/26, « §5.4 » 3/3, « §2.2 » 6/6. **Le mécanisme de substitution est structurellement incapable d'omettre un bloc existant** : il ne fait que remplacer des chaînes de version ; tout contenu non substitué traverse la génération byte pour byte.

Le seul écart de couverture détecté — `coverage_missing: ["1.13"]` (rapport `generer-pm-report.json` : skill_sections 35, pm_sections 55) — est **hérité** : la mention « §1.13 » du SKILL.md (ligne 220) est une note de numérotation (« les sections PM intermédiaires §1.9-§1.13 ne sont pas miroitées ici »), et la chaîne « §1.13 » est absente du golden master exactement de la même manière (0 occurrence). Ce n'est pas un bloc de machinerie : c'est un artefact de correspondance littérale entre numérotations SKILL.md et PM.

**Verdict C3 : H1 (omission de blocs existants) et H2 (ABANDON non résorbé → PM-ANTERIEUR) sont réfutées pour le canal canonique.** La génération réussit (aucun ABANDON), écrit un PM complet, et le diff prouve qu'aucune perte n'est possible par substitution.

## §4 — Test comportemental (C4) : routage intact sur l'état simulé

- **Champs de routage** (name/description/tags/keywords du frontmatter SKILL.md) : diff vide entre v3.23.1 et v3.24.0 simulé — le bump canonique ne touche que `version:`. Le rejeu mécanique voie M (SHARED §7 v2 — stemmer, `check-triggers-replay.py`) donne donc **exactement le même verdict qu'à v3.23.1 : 11/12**, le seul échec restant le cas négatif « gen-plan (stp) » (mode invalide qui NE doit PAS déclencher — faux positif de la réplique mécanique, hérité et connu).
- Les demandes canoniques de génération — « Élabore le plan d'action structuré… », « Intègre dans le plan d'actions… », « génère le plan d'actions… » — routent correctement dans l'état simulé ; la demande soumise à l'état v3.24.0 (PM complet + SKILL.md inchangé) produit un plan complet (Answer Key + Étapes E1-E15 avec #token + hooks) — preuve par exécution : le plan d'audit de cette session (task 2) a été produit et validé 16/16 par la méthode v3.23.1, dont le contenu est intégralement porté par le PM v3.24.0.

**Verdict C4 : H3 (routage défaillant) est réfutée pour le canal canonique.**

## §5 — Diagnostic mécanique (C5) : composant + condition + reproduction

**Composant défaillant** : pas le générateur. La faille est la **chaîne de complétion sémantique après génération** — le point aveugle « complétion agent » de KO-L004 v1.1.0, démontré en direct par la reproduction :

1. `generer-pm-skill.py` **écrit le PM même si des sections du SKILL.md sont absentes du PM** : l'écart de couverture produit un `[WARN]` sur stdout et une entrée `coverage_missing` dans le rapport JSON, mais le code retour est **0** et le PM est écrit (aucune gate).
2. La ligne d'historique générée **documente elle-même l'inachevé** : « deltas sémantiques à complétion agent (rapport de couverture : scripts/generer-pm-report.json) » — le PM v3.24.0 naît en annonçant que son contenu sémantique n'est pas complété.
3. `--check` ne vérifie **que la cohérence de versions** : SKILL.md v3.24.0 = PM v3.24.0 → verdict `COHERENT`, aucun écart. L'état « PM coquille » passe pour vert.
4. **Aucun des 6 arbitres de la certification ne contrôle la complétude sémantique PM ↔ SKILL.md** (verify-cross = conventions structurelles ; check-ecosysteme-integrity = corpus/miroir/KB/evals schéma ; test-coherence-interactions = §11b ; verify-correct-work = contrat PM v2.5.1 ; check-tool-routing = N1/N2).

**Condition d'échec** : toute montée de version **MINOR** dont les changements sémantiques (nouvelles sections, restructurations — typiques d'un bump 3.23.x → 3.24.0) ne sont pas complétés par l'agent après la génération produit un PM « coquille » : version-cohérent (donc invisible à tous les arbitres), sémantiquement vide des nouveautés du SKILL.md. Si ces nouveautés touchaient la machinerie de génération de plans — restructuration des étapes E1-E15, nouveaux blocs de planification, extraction des fences — alors l'agent opérant depuis ce PM « oublie » de générer les plans d'actions : **le symptôme rapporté depuis v3.24.0**.

**Corroboration de lignée** : la simulation produit SHARED **v1.7.8** — or la plateforme porte un fragment §0 SHARED v1.7.8 (skill cahier-des-charges), né d'un état propriétaire post-b75a620. Le canal canonique appliqué à gen-plan v3.24.0 est précisément ce qui produit SHARED v1.7.8 : la lignée propriétaire a très probablement vécu cette transition (bump gen-plan → SHARED v1.7.8 → … → v1.7.10, fragment alias-eco), puis perdu la complétion sémantique en route — cohérent avec un bug apparu « dès v3.24.0 » et jamais résorbé (la v3.24.0 n'a jamais été commitée : aucune trace locale).

**Reproduction** : §2 — séquence rejouable en sandbox ; le WARN §1.13 démontre le mécanisme en direct (gap détecté, toléré, PM écrit, exit 0, état vert à tous les arbitres).

## §6 — Correctif proposé (C6 — livrable ; application = décision propriétaire explicite, D007)

1. **Gate de complétude à la génération** (`generer-pm-skill.py`) : si `coverage_missing` non vide → écrire le PM avec un marqueur d'état en tête (`> **État** : deltas sémantiques en attente de complétion (coverage_missing : §…) — KO-L003`) et sortir en **code 4** (nouveau code ÉCART-COMPLÉTUDE, distinct de l'ABANDON 2) ; la ligne d'historique « à complétion agent » est remplacée à la complétion.
2. **`--check` renforcé** : `COHERENT` réservé à (versions alignées **ET** absence de marqueur d'état **ET** couverture vide) ; sinon écart `PM-SHELL (complétion agent attendue)`.
3. **Passe `--complete <famille>`** : re-vérifie couverture + absence de marqueur ; exit 4 tant que incomplet (la complétion devient une étape obligatoire vérifiable, plus une intention).
4. **Arbitre de complétude sémantique** (extension answer-key-checker ou verify-cross) : sections SKILL.md ⊆ sections PM pour les 4 familles — écart S3 si gap (aujourd'hui aucune vérification de cet axe n'existe nulle part dans la chaîne de certification).
5. **Propagation documentaire** : PM-INSTALL §2quater et PM gen-plan §1.15 portent la règle au prochain bump (recalibrage croisé KO-L004 standard).

## §7 — Zéro-régression (C7) : preuve

- Golden master byte-identité avant/après : `sha256sum -c scripts/audit-phaseC-golden-avant.txt` → OK ×2 (SKILL.md gen-plan `3e08a284…`, PM v3.23.1 `02002b98…`) — l'état vivant n'a subi **aucune écriture** pendant la Phase C.
- Sandbox supprimé (rollback) ; `generer-pm-skill.py --check` sur l'état vivant : 4/4 familles COHERENT, exit 0.
- Re-certification post-vol : **6/6 PASS AVEC RÉSERVES** (verify-cross 99/99 ×2, verify-correct-work 16/16, intégrité 70/70, interactions 47/48 — avertissement worklog B1 hérité, routage 5/5) — identique à l'état d'entrée (D002).
- M4 post-vol : blast radius gen-plan re-consigné CRITIQUE (17/22) — l'opération n'a pas changé le graphe (aucune écriture vivante).
