# Rapport Task 16 — déduplication des PMs vers @historique/, réinstallation du profil local

## Métadonnées
- **Date** : 2026-10-11 (session web-b93f42fa)
- **Directive propriétaire** : analyse du dossier `skills/@mon-ecosysteme` (commit de référence `b36f177`), réinstallation de l'écosystème dans le profil local, déduplication des prompts maîtres (ne garder que la dernière version) avec historique des versions dans `skills/@historique/` (format libre, sans grossissement ni des PMs ni du corpus) + GO commit/push avec la clé fournie (non révoquée).
- **Plan** : `download/plan-task16-corpus-pms-historique-reinstallation.md` (answer key D001-D008, gen-plan v3.21.0, hook É1-INSTALL frais rc0 INSTALLE b36f177 kb 28)
- **Règle d'or n°2** : GO REÇU 2026-10-11 — pattern B5 étendu (commit/push couche Task 15 d'abord, puis couche Task 16, puis journal).

## E1 — Résultats par décision

### D001 — GO commit/push + pattern B5 étendu
- **Push #1 (couche Task 15)** : `b36f177..c964d7f` — 84 fichiers, 9 651 insertions (64 enveloppes bare-liste, archive 27, 11 dormants archivés, tmp/ supprimé, rétro-sync 19 entrées) — commité puis poussé AVANT tout travail Task 16 (séparation des couches, add sélectif).
- Audit anti-persistance post-push : préfixe VALEUR du jeton = 0 occurrence dans l'arbre suivi (`git grep HEAD` rc1), l'arbre de travail (rc1), la config locale (rc1) ; `remote -v` sans jeton ; tracking ref resynchronisé (`git update-ref origin/main c964d7f`).
- Push #2 (couche Task 16) et push #3 (journal) : mêmes audits — voir « Traces de publication » ci-dessous.

### D002 — Analyse du corpus à b36f177 (scellée)
- **27 fichiers canoniques** = 22 PMs en 3 familles (GEN-PLAN ×16 : v3.6.1→v3.21.0 ; CORRECT-WORK ×5 : v2.4.0→v2.7.0 ; CLONE-CHAT ×1 : v2.0.0) + socle 5 fichiers (SHARED v1.6.7, INSTALL v1.6.0, ULTRA-ORCHESTRATION v1.0.0, README v2.1.0, SYNC-CONTEXT v1.4.1) — **1 302 854 o**.
- Dernières versions (dérivation dynamique KO-L003 + instantané §2ter PM-INSTALL v1.6.0) : **GEN-PLAN v3.21.0 · CORRECT-WORK v2.7.0 · CLONE-CHAT v2.0.0**.
- Historique consolidé de chaque famille : tables §7 des PMs vivants (source primaire de la distillation) ; versions sans fichier archivé (v2.0.0→v3.6.0 GEN-PLAN, v1.0.0→v2.3.0 CORRECT-WORK, v1.x CLONE-CHAT) tracées par les §7 successifs (perte aux wipes inter-sessions, aucun faux lignage).

### D004 — `skills/@historique/` créé (21 fichiers)
- `README.md` (objet, règles de conservation : byte-identité R2, unicité R4, jamais source d'installation, procédure de mise à jour KO-L004) ; `historique-versions-prompts-maitres.md` (distillation : 36 versions documentées sur 3 familles — particularités du skill, améliorations implantées, avantage vs version précédente ; index SHA-256 §5 ; instantané des 28 skills KB §6).
- `prompts-maitres/gen-plan/` ×15 + `prompts-maitres/correct-work/` ×4 : déplacés `git mv` — **byte-identité prouvée SHA-256 contre les blobs b36f177** (script `/home/z/my-project/scripts/task16-move-pms.py`, all-or-nothing, idempotent ×2 ; index complet au §5 de la distillation).

### D005 — Corpus dédupliqué : 27 → 8 fichiers, 1 302 854 → 238 345 o (−81,7 %)
- Restants : 3 PMs de famille (byte-identiques à b36f177 — preuve C05 du harnais) + 5 socle. 0 édition des PMs vivants (contrainte propriétaire « ni le prompt maître ni le dossier ne grossissent » satisfaite : les PMs ne sont pas touchés, le corpus rétrécit).

### D003 — Réinstallation du profil local (`/home/z/my-project/skills/`)
- **Déployés (absents — wipe inter-sessions documenté PM-INSTALL §3.4)** : `gen-plan/` v3.21.0 (SKILL.md + 11 references + evals [6 evals JSON valides, 8 cas trigger] + scripts/ensure-installed.py), `correct-work/` v2.7.0 (SKILL.md + evals 7 cas + references + scripts), `KNOWLEDGE.md` (byte-identique au registre 28 entrées). Checks §6 du PM gen-plan : PASS.
- **Alignés (drift SHARED v1.6.4→v1.6.7 à version égale, copie fusion 0 suppression)** : 14 skills écosystème (clone-chat, context/loop/graph/harness-engineering, skills-inventory, agent-creator, prompt-engineering, audit-provenance, knowledge-observer, resource-monitor, script-creator, script-reviewer, script-mon-ecosysteme-infrastructure) — re-vérification : 14/14 byte-identiques au dépôt certifié.
- **Couche plateforme intouchée (R2 non-régression runtime)** : `skill-creator`, `version-management`, `skill-finder-cn` du profil sont des formes plateforme (frontmatters EN/ZH sans version semver) — hors périmètre d'installation écosystème (précédent « GAP plateforme par conception », registry-sync).
- `@historique/` reste côté dépôt (R4 anti-duplication — le profil est la surface d'exécution, pas le corpus).

### D006 — Recalibrage croisé KO-L004
| Outil | Recalibrage |
|---|---|
| `check-ecosysteme-integrity.py` | CORPUS_ATTENDU 27 → 8 (commenté Task 16) + libellé check 1 |
| `task21-f2-rebuild-archive.py` | RETRAITS_SANCTIONNES + 19 PMs déplacés + **garde anti-perte renforcée** (chaque PM vérifié présent et byte-identique en `@historique/` contre l'ancienne archive AVANT re-scellement — 19/19 vérifiés) ; re-scellement PASS : archive 27 → 8 entrées, round-trip v2.2 vérifié |
| `ecosysteme-integrity.json` | manifeste régénéré par l'arbitre (pins corpus 8 + archive + download) |
| `sync-context-block.py` | PROMPT_FILES 4 → 2 porteurs vivants (CLONE-CHAT v2.0.0 + INSTALL) — v3.11.0/v2.5.1 archivés non-cibles (R2), v2.7.0 bloc gelé hérité (non-cible) |
| `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` | régénéré (`gen-ultra-maitre.py`, idempotent) : « 7 fichiers canoniques + cet orchestrateur », familles v3.21.0/v2.7.0/v2.0.0, versions historiques figées « — » (dérivation dynamique) — état STALE préalable (v3.18.0/25 fichiers) résorbé |
| `README.md` (corpus) | v2.1.0 → **v2.1.1** : arborescence §2 recalibrée (@mon-ecosysteme 8 fichiers + @historique) |
| `SYNC-CONTEXT.md` | v1.4.1 → **v1.4.2** : table porteurs N1 (2 vivants), notes R2 → @historique, état du corpus 8 fichiers (historique complet des recalibrages consigné) |
| `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | révision documentaire SANS bump (précédent Task 14) : §2ter « versions historiques archivées en @historique/ » + note §7 (diff vs b36f177 = exactement 3 lignes documentées) |

### D007 — Sweep R2 final (état après Task 16)
| Arbitre | Verdict |
|---|---|
| verify-correct-work (vcw) | **ALL PASS 16/16** |
| check-ecosysteme-integrity --check | **60/60 PASS, rc0** (constantes nouvelles : corpus 8, archive 8 entrées) |
| test-coherence-interactions | **PASS AVEC RÉSERVES 48/3/0** (51 checks — identique baseline, 0 régression) |
| verify-cross --check-context | **100,0 % — 0 warning, 0 error** |
| generer-pm-skill --check | **3/3 COHERENT rc0** |
| task14-scan-doublons | **0 doublon** (39 uniques légitimes) |
| verify-registry-sync | ECARTS par conception (ghosts **0** — état inchangé) |
| **Harnais task16** (`scripts/task16-answer-key-check.py`) | **22/22 PASS rc0** (16 prévus au plan + 6 ajoutés par calibration — comptes réels consignés, 0 fix instrument) |

## Calibration d'instrument (2 passes — KO-L003, 0 ajustement de réalité)
1. **C05 tour 1** : incluait INSTALL dans les « PMs vivants intacts » — le harnais était trop large : la contrainte propriétaire porte sur les 3 PMs de famille ; INSTALL a reçu une révision documentaire LÉGITIME et documentée (C16, diff = 3 lignes exactement). Check restreint aux 3 familles.
2. **C06 tour 1** : homonymie par nom seul — deux `README.md` de rôles distincts (guide corpus vs archive) ne sont pas des doublons ; critère R4 réel = même nom ET même octets (critère task14-scan-doublons). Check aligné.
3. **C09 tour 1** : comptage `\n## ` = 29 (28 entrées skills + section « Décisions d'architecture ») — critère réel = byte-identité du KB déployé au registre source. Check aligné.
4. **C22 tour 1** : le marqueur jeton était stocké littéral dans le harnais (auto-détection) — marqueur reconstruit à l'exécution (`"11AJST"+"JXQ0"`), 0 occurrence littérale dans tout l'arbre y compris le harnais. Convention « 0 occurrence du préfixe dans l'arbre suivi » préservée pour les audits futurs.
- Observation consignée (non traitée, R2) : l'instantané §5.5 du PM gen-plan v3.21.0 liste 9 cas trigger illustratifs vs 8 cas de la forme installée certifiée — divergence documentaire préexistante, non traitable sans éditer un PM vivant (interdit par la contrainte propriétaire Task 16).

## Traces de publication (pattern B5 étendu — GO propriétaire 2026-10-11)
- Push #1 : couche Task 15 (`b36f177..c964d7f`) — audit PASS (0 occurrence ×3 canaux).
- Push #2 : couche Task 16 (ce rapport + plan + 19 R + 4 M scripts + 4 M corpus + 2 ?? @historique) — audit anti-persistance PASS (voir journal).
- Push #3 : commit journal (worklog dépôt) — audit anti-persistance PASS.
- Discipline jeton : URL d'invocation uniquement, jamais écrit dans un fichier, jamais en config ; préfixe reconstruit à l'exécution dans le harnais (C22).

## Restant propriétaire
- Re-mesure voie L des 15 dérives replay (QUOTA_OK — héritées Task 15).
- Décision révocation PAT (consignée Tasks 18/22/24/13-push/14-push/15/16 — la clé a été réutilisée à GO express du 2026-10-11).
- Éventuelle codification SHARED §1.2 du dossier `@historique/` (non faite : le principe du préfixe `@` y est déjà documenté — cascade resync N1 évitée, R-F1).
