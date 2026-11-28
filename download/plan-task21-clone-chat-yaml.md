# Plan d'actions gen-plan — Task 21 (fenêtre 17, suite 177)

**Session** : web-220878ed-c362-40f9-b12a-5aa08335c14d · **trace directive** : 1a221e5599452e2d · **date** : 2026-11-28

## Directive propriétaire (verbatim)

> gen-plan : "ne serait-ce pas judicieux que "clone-chat" génère des clones au format YALM, si c'est le cas alors fais sorte $FACON en que mon skill "clone-chat" le fasse."

Lecture : (1) analyser la judiciousité d'une sortie des clones de « clone-chat » au format « YALM » ; (2) si verdict positif, implémenter ($FACON) l'évolution dans le skill vivant `skills/clone-chat/SKILL.md` (référence canonique — jamais les PMs du corpus @mon-ecosysteme/).

## Ancrage (KO-L003)

- Parité git 0/0, HEAD = origin/main = 2ec35b6c (suite 176 Task 20 atterrie), arbre propre.
- clone-chat v2.2.0 identique live/dépôt (SHA 30531c12 ×2) avant édition.
- PyYAML 6.0.3 disponible (validation mécanique réelle possible).

## D001 — Terminologie « YALM »

« YALM » (formulation propriétaire) est interprété comme **YAML** (sérialisation structurée) : aucune norme publique « YALM » n'existe comme format documentaire. Garde de fidélité : l'alias `--yalm` est accepté au déclencheur (l'appel propriétaire fonctionne tel quel) et l'interprétation est tracée au SKILL §1.14 avec le trace_id. Évolution réversible (ajout de mode, aucune fonction retirée).

## D002 — Verdict : JUDICIEUSE (sous conditions R4)

| Argument | Détail |
|---|---|
| Utilité mécanique réelle | Le clone Markdown est auto-suffisant pour l'usage humain mais non parseable par les scripts ; un jumeau YAML alimente sessions héritières (lecture machine), arbitres et checkpoints (ancrage KO-L003, E11, État Long) |
| R4 respecté | Le YAML est une VUE DÉRIVÉE régénérable du clone canonique — jamais une seconde source d'information ; le Markdown demeure l'instantané canonique (§5 inchangé) |
| Cohérence écosystème | Les frontmatters des skills sont déjà YAML ; la sortie s'insère dans les chaînes de réingestion existantes |
| Coût marginal faible | Dérivation des sections déjà assemblées (Étape 5) — aucune re-analyse, surcoût ~15-20 % #token (grille §2.3) |
| Limites encadrées | YAML multi-lignes verbatim fragile → règles R-5 (sans tabs, blocs scalaires indentés, tableaux de lignes) ; validation obligatoire (check 10) |

## D003 — Implémentation ($FACON) : clone-chat v2.3.0 (MINOR)

15 éditions du SKILL.md vivant (557 lignes finales, SHA 1e3db637 hôte = dépôt ×2) :

1. Frontmatter : version 2.3.0, tags += yaml/yalm, description += sortie duale (alias `--yalm`, trace citée).
2. §A : +1 déclencheur `clone-chat --yaml` (alias `--yalm`, formulation propriétaire acceptée).
3. §1.1 : +1 phrase (jumeau YAML, Markdown seul canonique).
4. §1.9 : **check 10 — validité du jumeau YAML** (parse sans erreur, 9 clés racines, couverture §0-§5, idempotence bytes identiques) → 10/10 en mode `--yaml`.
5. §1.12 : intro + table +1 ligne « modificateur transversal » (combinable aux 4 modes thématiques).
6. **§1.14 « Jumeau YAML »** : terminologie (YALM→YAML, trace_id), principe de sortie duale, règles R-1 à R-6, schéma des 9 clés racines (`meta`/`rule_zero`/`chronologie`/`artefacts`/`decisions`/`drifts`/`instructions`/`autoclone`/`chain`), usage cible.
7. §2.1/§2.2 : production sans dépendance installée, validation parseur si dispo sinon garde structurelle ; jumeau optionnel non canonique.
8. §2.3 : grille +1 ligne « mode `--yaml` » (+325 NORMAL, +15-20 % du mode correspondant) + note v2.3.0.
9. §2.8 : logging Étape 7 mentionne le jumeau + check 10.
10. §6 : +1 puce conventions (jumeau DÉRIVÉ non canonique, idempotent, alias `--yalm`).

Cascade : KB ×2 (entrée v2.3.0 + calibration Task 21, SHA 000d81ca hôte = dépôt) — invariants dans le même commit (leçon flux C6 suite 175). Aucun PM régénéré requis (clone-chat n'est pas un PM famille, précédent v2.1.0/v2.2.0).

## D005 — Tests ($FANCON2) : 7/7 PASS ×2

`scripts/task21-clone-yaml-test.py` (T1-T6, deux passes internes, deux ré-invocations rc 0 ×2) :

| Test | Objet | Verdict ×2 |
|---|---|---|
| T1 | Parse PyYAML 6.0.3 sans erreur | PASS |
| T2 | 9 clés racines exactes (schéma §1.14) | PASS |
| T3 | Couverture §0-§5 + §1.0 | PASS |
| T4 + T4bis | Idempotence bytes identiques + round-trip stable | PASS |
| T5 | Provenance meta.source_md + sha256_source exacts (R-2) | PASS |
| T6 | Sans tabulations, indentation 2 (R-5) | PASS |
| Croisé | SHA passe 1 = SHA passe 2 | PASS |

Livrables : `download/echantillon-clone-jumeau-yaml-demo.yaml` (2 679 o), `download/echantillon-clone-jumeau-yaml-demo.source.md`, `download/rapport-task21-clone-yaml.json` (VERDICT GLOBAL PASS, règles R-1..R-6 tracées) + miroirs dépôt ×4.

## D006 — État et suivis

- Première invocation RÉELLE du mode non exécutée ce tour (aucune demande de clone dans la directive) — le premier jumeau réel sera produit à la prochaine invocation `clone-chat --yaml` (ou `clone-chat --yalm`).
- Consignation suite 177 append-only hôte+dépôt ; scan jetons (task15-scan-jetons.py) AVANT commit ; commit + push clé propriétaire [JETON masqué] ; parité vérifiée après push.
- Résiduels reconduits propriétaire-seul : n°1 révocation PATs (CRITIQUE — la clé a de nouveau servi ce tour), n°4 lien de partage (bloquée plateforme), n°5 GIF.

## Statut des groupes

| Groupe | Objet | Statut |
|---|---|---|
| G1 | Ancrage KO-L003 + terminologie D001 | TERMINÉ |
| G2 | Verdict judiciousité D002 | TERMINÉ |
| G3 | Implémentation v2.3.0 + KB D003-D004 | TERMINÉ |
| G4 | Tests $FANCON2 D005 | TERMINÉ |
| G5 | Consignation + scan + commit + push D006 | TERMINÉ |

Coût #token : ~45k (analyse + 15 éditions + batterie + clôture). — PLAN AFFICHÉ, 5/5 TERMINÉS.
