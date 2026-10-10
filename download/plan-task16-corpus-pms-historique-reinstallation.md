# Plan Task 16 — corpus @mon-ecosysteme : déduplication des PMs vers @historique/, réinstallation profil local

## Métadonnées
- **Date** : 2026-10-11 (session web-b93f42fa)
- **Directive propriétaire** : « analyse la derniere version des fichiers de ce dossier [skills/@mon-ecosysteme @ b36f177], puis installe à nouveau mon écosystème dans mon profil local ; plusieurs versions des prompts maitres → ne garder que la dernière version, historique des versions (particularités, améliorations, avantages vs précédente) dans un nouveau dossier skills/@historique/ (format libre), sans augmenter la taille ni du prompt maitre, ni du dossier @mon-ecosysteme » + « intègre que tu devras effectuer un commit et un push avec ma clé [PAT fournie, non révoquée] »
- **gen-plan** : v3.21.0 (frontmatter installé `skills/gen-plan/SKILL.md` — source de vérité, contrat §1.5) ; règles d'or n°3 (intégration de la demande commit/push au plan courant — extension R2) et n°4 (dépôt = clone local work_knowledge, 0 lecture distante)
- **Hook É1-INSTALL frais** : rc0 INSTALLE (head b36f177, kb 28) — re-exécuté en A
- **Profil** : NORMAL
- **Estimation #token** : ~18 000 (grille §4)
- **Règle d'or n°2 — GO REÇU (2026-10-11)** : commit+push autorisés avec le PAT fourni — discipline : jeton en URL d'invocation UNIQUEMENT (jamais écrit dans un fichier, jamais en config), audit anti-persistance après CHAQUE push (grep VALEUR sur arbre suivi + arbre de travail + git config locale)

## E1 — Livrables + critères de succès
1. **D001 — GO commit/push + stratégie B5 étendue** : la couche Task 15 (D001-D006, staged non commitée, « prête pour commit/push » au worklog) est commitée et poussée EN PREMIER (séparation des couches — commits empilés linéaires), puis la couche Task 16, puis le journal — 3 commits / 3 pushes, audit anti-persistance après chaque push, `git update-ref refs/remotes/origin/main` après push par URL explicite. Succès : 3 commits distants, 0 occurrence de la VALEUR du jeton dans l'arbre suivi, l'arbre de travail et la config locale.
2. **D002 — analyse corpus à b36f177** : 27 fichiers canoniques = 22 PMs (GEN-PLAN ×16 : v3.6.1→v3.21.0 ; CORRECT-WORK ×5 : v2.4.0→v2.7.0 ; CLONE-CHAT ×1 : v2.0.0) + socle 5 fichiers (SHARED v1.6.7, INSTALL v1.6.0, ULTRA-ORCHESTRATION v1.0.0, README v2.1.0, SYNC-CONTEXT v1.4.1) ; 1 302 854 o. Dernières versions (dérivation dynamique KO-L003 + instantané §2ter PM-INSTALL v1.6.0) : GEN-PLAN v3.21.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0. Historique consolidé de chaque famille = table §7 du PM le plus récent (source primaire de la distillation). Succès : inventaire SHA-256 scellé au rapport.
3. **D003 — réinstallation profil local** : le dépôt fait foi (formes installées certifiées par les arbitres) — déploiement vers `/home/z/my-project/skills/` des pièces ABSENTES : `gen-plan/` (v3.21.0 : SKILL.md + references/ + evals/ + scripts/), `correct-work/` (v2.7.0 : SKILL.md + references/ + evals/ + scripts/), `KNOWLEDGE.md` (kb 28 entrées). Cas de wipe inter-sessions documenté (PM-INSTALL §3.4). Formes EXISTANTES du profil : diff-audit rapporté, 0 écrasement sans divergence de version (R2 — non-régression du runtime plateforme) ; à version égale avec octets divergents = drift documenté, alignement UNIQUEMENT si le dépôt est à la fois plus récent ET certifié vert. `@historique/` reste côté dépôt (R4 anti-duplication — le profil est la surface d'exécution, pas le corpus). Succès : gen-plan + correct-work + KB présents au profil ; rc0 des checks §6 PM gen-plan sur la forme déployée ; diff-audit consigné.
4. **D004 — création `skills/@historique/`** : convention `@` (SHARED §1.2 — ASCII 64, dossier non-skill en tête de listing, précédent @mon-ecosysteme). Structure : `README.md` (objet, provenance, règles de mise à jour, distinction archive ≠ doublon R4 : les fichiers y sont UNIQUES, retirés du corpus) ; `historique-versions-prompts-maitres.md` (DISTILLATION — par famille, par version : version, date, particularités du skill installé, améliorations implantées, avantages vs version précédente, renvoi au fichier source ; sources = §7 des PMs les plus récents + SYNC-CONTEXT v1.4.1 + PM-INSTALL §7 + entrées KB ; format Markdown canonique écosystème — lisible, diffable, sans dépendance) ; `prompts-maitres/gen-plan/` ×15 + `prompts-maitres/correct-work/` ×4 (anciens PMs déplacés `git mv` — byte-identité prouvée SHA-256 avant/après). Succès : 19+2+1 fichiers ; SHA-256 identiques avant/après ; 0 copie résiduelle.
5. **D005 — @mon-ecosysteme = dernières versions seules** : 27 → 8 fichiers (3 PMs sources + 5 socle), ~1 302 854 o → ~355 000 o (−73 %). Contrainte propriétaire satisfaite : l'historique n'augmente NI la taille des PMs (0 édition des 3 PMs sources) NI celle d'@mon-ecosysteme (déplacement hors dossier, R4 : pas de copie). Succès : listing = 8 fichiers ; les 3 PMs sources byte-identiques à b36f177 (SHA-256) ; 0 ancien PM restant.
6. **D006 — recalibrage croisé KO-L004** : CORPUS_ATTENDU 27→8 (commenté, précédent Task 15 D002) ; manifeste `scripts/ecosysteme-integrity.json` régénéré par l'arbitre ; archive re-scellée round-trip v2.2 (`task21-f2-rebuild-archive.py`) ; ULTRA-ORCHESTRATION régénéré (`gen-ultra-maitre.py` — idempotent ; état actuel STALE : annonce v3.18.0/25 fichiers) ; révisions documentaires SANS bump de version (précédent toilettage clone-chat 1.0.x) : README §2 (arborescence), SYNC-CONTEXT (table porteurs N1 + notes R2 → @historique), PM-INSTALL §2ter (les PMs antérieurs « demeurent » → « demeurent en skills/@historique/prompts-maitres/ ») ; SYNC_MAP/sync-context-block recalibré aux porteurs VIVANTS ; generer-pm --check 3/3. Succès : integrity 60/60 rc0 ; coherence PASS ; ULTRA régénéré cohérent au listing réel.
7. **D007 — sweep R2 final** : vcw 16/16 · integrity 60/60 · coherence PASS AVEC RÉSERVES · verify-cross 84/84 · generer-pm 3/3 · doublons download/ 0 · registry-sync ghosts 0 · replay 93/0 (15 dérives documentées, non forcées) · harnais task16 (16 checks) PASS rc0. Toute divergence = correction à la racine (KO-L003), jamais de fix instrument.
8. **D008 — journalisation** : rapport `download/rapport-task16-corpus-pms-historique-reinstallation.md` ; worklog interne + externe (entrée Task 16, format SHARED §1.4) ; réponse propriétaire avec état final + restant.

## E2 — Ressources (mesuré)
- Dépôt : HEAD b36f177 = origin/main ; arbre = couche Task 15 staged non commitée (19 renommages + 64 evals + worklog +402 L + 3 fichiers non suivis) — **ne pas mélanger** avec la couche Task 16 (add sélectif).
- Corpus : 27 fichiers (inventaire wc -c scellé) ; CORPUS_ATTENDU = 27 (check-ecosysteme-integrity l.122) ; ECO_SKILLS pins gen-plan 3.21.0.
- Profil local : 94 skills ; gen-plan/correct-work/KNOWLEDGE.md ABSENTS (wipe documenté) ; versions profil = versions dépôt (clone-chat 2.0.0, context-engineering 1.1.0, skills-inventory 1.1.0, prompt-engineering 2.2.0) ; clone-chat SKILL.md octets divergents à version égale (diff-audit en E).
- Scripts : gen-ultra-maitre.py (régénération idempotent) ; task21-f2-rebuild-archive.py (re-scellement, retraits sanctionnés) ; generer-pm-skill.py --check ; sync-context-block.py (SYNC_MAP à recalibrer) ; verify-registry-sync.py.
- GO commit/push : PAT fournie non révoquée (D001) — jeton JAMAIS persisté (precedents Task 8/14/15).

## E3 — Type 2 (ingénierie écosystème — protocole + scripts ; rapport .md secondaire)

## E5 — Skills mobilisés
gen-plan (plan, v3.21.0) · correct-work (hooks par phase) · arbitres : check-ecosysteme-integrity, test-coherence-interactions, verify-cross, verify-correct-work (shim), generer-pm-skill, verify-registry-sync, task14-scan-doublons · instruments : task21-f2-rebuild-archive.py, gen-ultra-maitre.py, sync-context-block.py · leçons KO-L003 (invariants dynamiques + anti-écho byte-level) et KO-L004 (recalibrage croisé) appliquées en continu.

## E7 — Séquence (série par défaut — philosophie #4)
| Phase | Contenu | #token |
|---|---|---|
| A | Hook É1 frais + écriture plan + harnais answer-key task16 (16 checks) | 2 000 |
| B | D001 : commit + push couche Task 15 (add sélectif) + audit anti-persistance + update-ref | 1 500 |
| C | D004 : SHA-256 avant ×19 → git mv vers @historique/prompts-maitres/ + README + distillation (§7 ×3 familles) | 4 000 |
| D | D005 : vérification corpus 8 fichiers + SHA des 3 PMs sources = b36f177 | 1 000 |
| E | D003 : réinstallation profil (gen-plan, correct-work, KNOWLEDGE.md) + diff-audit existants + checks §6 | 2 500 |
| F | D006 : recalibrage KO-L004 (CORPUS_ATTENDU, manifeste, archive, ULTRA, README/SYNC-CONTEXT/PM-INSTALL, SYNC_MAP) | 3 000 |
| G | D007 : sweep R2 arbitres + harnais 16/16 + rapport + D008 worklogs | 2 500 |
| H | D001 : commit + push couche Task 16 + audit ; commit + push journal + audit ; update-ref ; réponse | 1 500 |

## Answer key (hook E1 — décisions D001-D008)
| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|---|---|---|---|---|---|
| D001 | GO reçu : 3 commits / 3 pushes (Task 15, Task 16, journal), jeton URL seule, audit après chaque push | 3 sha distants ; grep VALEUR jeton = 0 (arbre suivi + travail + config) ; origin/main = HEAD après chaque push | directive propriétaire 2026-10-11 + pattern B5 (Tasks 13/14-push) | S1 | pending |
| D002 | Analyse corpus b36f177 : 27 fichiers, 22 PMs en 3 familles, dernières versions 3.21.0/2.7.0/2.0.0 | inventaire SHA-256 au rapport ; dérivation semver = §2ter PM-INSTALL v1.6.0 | listing réel + §2ter + KO-L003 | S2 | pending |
| D003 | Réinstallation profil = déploiement des formes certifiées du dépôt (gen-plan, correct-work, KB) ; diff-audit existants ; 0 écrasement à version égale | 3 cibles présentes au profil ; checks §6 PM gen-plan rc0 sur la forme déployée ; diff-audit au rapport | PM-INSTALL §2/§3.4 + R2 + arbitres verts dépôt | S2 | pending |
| D004 | skills/@historique/ : README + historique-versions-prompts-maitres.md (distillé §7) + git mv ×19 byte-identiques | 22 fichiers ; SHA-256 ×19 avant=après ; 0 doublon nom entre corpus et @historique | directive propriétaire (dossier + format libre) + SHARED §1.2 (convention @) | S2 | pending |
| D005 | @mon-ecosysteme = 8 fichiers (3 PMs + 5 socle), 0 édition des PMs sources, −73 % taille | listing = 8 ; SHA ×3 PMs = b36f177 ; wc -c consigné | directive propriétaire (ni PM ni dossier grossis) + R4 | S1 | pending |
| D006 | Recalibrage KO-L004 : CORPUS_ATTENDU 8, manifeste, archive re-scellée, ULTRA régénéré, révisions documentaires README/SYNC-CONTEXT/PM-INSTALL, SYNC_MAP vivants | integrity 60/60 rc0 ; coherence PASS ; ULTRA = listing réel ; generer-pm 3/3 | KO-L004 (gen-plan §1.12bis) + précédent Task 15 D002 | S2 | pending |
| D007 | Sweep R2 : 7 arbitres verts + harnais task16 16/16 ; divergence = correction racine (KO-L003) | verdicts consignés au rapport ; harnais rc0 | R-F2 + KO-L003 | S1 | pending |
| D008 | Rapport + worklog interne/externe entrée Task 16 + réponse propriétaire | 3 artefacts présents ; format SHARED §1.4 | règle d'or n°1 + SHARED §1.4 | S3 | pending |

## E8 — Validation du plan
`scripts/task16-answer-key-check.py` (16 checks mécaniques : structure answer key, critères exécutables, byte-proof @historique, corpus 8, profil déployé, arbitres, 0 jeton) exécuté après exécution ; verdict consigné au rapport ; fallback honnête journalisé si arbitre inopérant (règle d'or n°1).

## R2 — Baselines (HEAD b36f177 + couche Task 15 staged, mesuré fin Task 15)
vcw 16/16 · integrity 60/60 · coherence PASS AVEC RÉSERVES 48/3/0 · verify-cross 84/84 · generer-pm 3/3 · replay 93/0 (15 dérives documentées) · doublons 0 · registry-sync 28/28 ghosts 0 · hook rc0 INSTALLE kb 28. **Cibles Task 16** : mêmes verdicts aux nouvelles constantes (CORPUS_ATTENDU 8, manifeste + archive recalibrés, ULTRA régénéré, profil +2 skills + KB) — 0 régression des verdicts.
