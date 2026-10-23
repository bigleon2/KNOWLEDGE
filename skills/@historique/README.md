# @historique/ — Archive documentaire des versions des prompts maîtres et des skills

> **Version** : 1.2.0
> **Date** : 2026-10-11 (Task 17-B, session web-b93f42fa — directive propriétaire « je voulais qu'il ait un historique par skill et qu'il y ait un fichier historique pour les autres éléments de @mon-ecosysteme/ » ; structure initiale v1.0.0 Task 16)
> **Nature** : dossier d'infrastructure documentaire — **pas un skill, pas de SKILL.md** (convention SHARED §1.2 v1.6.8 : préfixe `@` = ASCII 64, dossier non-skill en tête du listing `skills/`, précédent `@mon-ecosysteme/`)

## 1. Objet

Ce dossier conserve l'**historique des versions** des prompts maîtres de l'écosystème et des skills, afin que le corpus canonique `skills/@mon-ecosysteme/` ne porte plus que la **dernière version** de chaque prompt maître. Il satisfait la contrainte propriétaire : l'historique n'augmente **ni la taille des prompts maîtres** (les PMs sources ne sont jamais édités — byte-identité prouvée), **ni celle du dossier `@mon-ecosysteme/`** (les versions antérieures y sont retirées, pas copiées).

Structure dirigée par le propriétaire (Task 17-B) : **un historique par skill** (`historiques-par-skill/` — un fichier dédié par famille à PM) et **un fichier historique pour les autres éléments** du socle `@mon-ecosysteme/` (`historique-autres-elements.md`).

## 2. Contenu

| Élément | Rôle |
|---------|------|
| `historiques-par-skill/gen-plan.md` | Historique dédié du skill gen-plan — 25 versions (v2.0.0 → v3.23.0), tables migrées verbatim de l'ex-distillation globale (Task 17-B) |
| `historiques-par-skill/correct-work.md` | Historique dédié du skill correct-work — 10 versions (v1.0.0 → v2.7.0) + révisions documentaires de la famille |
| `historiques-par-skill/clone-chat.md` | Historique dédié du skill clone-chat — 4 versions (v1.0.0 → v2.0.0) + révisions documentaires (PROMPT 1.0.1-1.0.3) |
| `historiques-par-skill/dessin-technique.md` | Historique dédié du skill dessin-technique — 2 versions (v1.0.0 → v1.1.0), créé Task 10 (2026-10-18, session web-da654199) ; v1.0.0 vit en git dépôt (b944a27 → 26de6c1), SHA-256 scellé au journal |
| `photos/` | 4 PMs @photos historiques (iphone17 v2.0, iphone18 v1.0, iphone19 v0.9.0/v0.10.0) — extraits git byte-identiques (e62f354, 29e2de1), scellés SHA-256 dans `photos/INDEX.md` (créé Task 48, 2026-10-21) |
| `@Alias/aliases.json` | **Registre VIVANT** du système d'alias `$<ALIAS>` (skill alias-eco v1.0.0, Task 18 2026-10-23) — phrases récurrentes triées alphabétiquement, dédupliquées ; ÉTAT VIVANT non scellé (mis à jour à chaque scan/analyse correct-work PROJET) — les règles de conservation R2/R4 du présent dossier ne s'y appliquent PAS (il n'est pas une archive scellée) |
| `historique-autres-elements.md` | Historique du socle sans famille à PM : SHARED (v1.4.0 → v1.7.2), SYNC-CONTEXT (v1.4.0 → v1.4.5), README (v2.1.0 → v2.1.3), ULTRA (généré), PM-INSTALL (v1.1.0 → v1.6.2), registre KB (instantané 28 skills) |
| `prompts-maitres/gen-plan/` | 18 PMs GEN-PLAN historiques (v3.6.1 → v3.22.1), déplacés du corpus `git mv` — byte-identité prouvée SHA-256 contre les blobs du commit de référence (b36f177, rapport Task 16) |
| `prompts-maitres/correct-work/` | 4 PMs CORRECT-WORK historiques (v2.4.0 → v2.6.0), mêmes garanties |

Vue d'ensemble des 3 familles (héritée de l'ex-distillation) :

| Famille | Skill installé | Versions documentées | Fichiers archivés ici | Version vivante (corpus) |
|---------|----------------|---------------------|----------------------|--------------------------|
| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 26 (v2.0.0 → v3.23.2) | 19 (v3.6.1 → v3.23.1) | v3.23.2 |
| CORRECT-WORK | correct-work — vérification/correction (5 étapes, 4 modes) | 11 (v1.0.0 → v2.8.0) | 5 (v2.4.0 → v2.7.0) | v2.8.0 |
| CLONE-CHAT | clone-chat — archivage de session (7+1 étapes, 8 checks) | 6 (v1.0.0 → v2.0.2) | 2 (v2.0.0, v2.0.1) | v2.0.2 |
| REFACTOR-GUARD | refactor-guard — garde-fous de refactoring (H01-H15, échelle rollout) | 4 (v1.7.0 → v1.8.1) | 3 (v1.7.0, v1.7.1, v1.8.0) | v1.8.1 |

Versions documentées SANS fichier archivé : GEN-PLAN v2.0.0 → v3.6.0 (antérieures à la matérialisation du corpus, perdues aux wipes inter-sessions — changements tracés par les §7 successifs) et v3.20.0 (remplacée le jour même par v3.21.0) ; CORRECT-WORK v1.0.0 → v2.3.0 (même cause) ; CLONE-CHAT v1.0.0 → v1.2.0 (même cause). Les PMs CORRECT-WORK v2.6.0/v2.7.0 sont des RECONSTITUTIONS par diffs chirurgicaux (méthode B1, Task 16 session web-8a7e5653 — provenance tracée en tête de chaque PM, aucun faux lignage).

## 3. Règles de conservation

1. **Byte-identité (R2)** : les fichiers archivés ici ne sont JAMAIS édités. Leurs blocs `CONTEXTE SYSTÈME` figés et leurs §7 d'époque restent intacts (statut « non-cibles de resynchronisation », SYNC-CONTEXT — rétro-compatibilité R2).
2. **Unicité (R4 anti-duplication)** : un fichier archivé ici est RETIRÉ du corpus `@mon-ecosysteme/` (déplacement, pas copie) — aucun homonyme ne peut exister des deux côtés. Ce dossier n'est pas un doublon du corpus : c'est l'archive des versions supprimées. Dans le même esprit, la distillation globale unique (`historique-versions-prompts-maitres.md`) a été RETIRÉE après migration verbatim de ses tables vers les historiques par skill (Task 17-B — une information, une source).
3. **Jamais source d'installation (garde R2 PM-INSTALL §3.2)** : les étapes 3-5 du pipeline d'installation ne mobilisent que le PM le plus récent du corpus (dérivation dynamique KO-L003). Les fichiers de ce dossier sont consultatifs.
4. **Source de foi** : la table §7 de chaque PM le plus récent reste la source de vérité de l'historique de sa famille ; les historiques par skill et le fichier des autres éléments sont les archives documentaires (instantanés datés) — en cas de divergence, les en-têtes vivants (§7 du PM, en-tête Révision du socle) font foi.

## 4. Procédure de mise à jour

À chaque montée de version d'une famille (règle KO-L004 — génération automatique du PM par `scripts/generer-pm-skill.py §2quater PM-INSTALL`) :

1. Le nouveau PM est généré dans `skills/@mon-ecosysteme/` (recalibrage croisé inclus) ;
2. Le PM supplanté est déplacé ici par `git mv` (`prompts-maitres/<famille>/`), byte-identité prouvée SHA-256 avant/après ;
3. Une ligne est ajoutée à la table de la famille dans `historiques-par-skill/<skill>.md` (source : §7 du nouveau PM) ;
4. À chaque révision d'un élément du socle (SHARED, SYNC-CONTEXT, README, PM-INSTALL, registre KB) : une ligne est ajoutée à la table correspondante de `historique-autres-elements.md` ;
5. La présente table §2 est rafraîchie et l'index §5 mis à jour ;
6. Recalibrage croisé KO-L004 standard (CORPUS_ATTENDU, manifeste integrity, archive, orchestrateur ULTRA) et sweep arbitres avant tout commit.

## 5. Index des fichiers sources archivés (27 PMs — sceau SHA-256)

Déplacés du corpus `skills/@mon-ecosysteme/` vers le présent dossier par `git mv` (Task 16, 2026-10-11) — byte-identité prouvée contre les blobs du commit de référence `b36f177` (script `/home/z/my-project/scripts/task16-move-pms.py`, all-or-nothing, garde anti-homonyme R4). Table complète au rapport `download/rapport-task16-corpus-pms-historique-reinstallation.md`. Complément cascade Task 24 (2026-10-23, session web-fdf5963c — directive « révisez les §1.9bis des 16 éléments ») : `PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md` archivé par `git mv` byte-identité (R4 — SHA-256 scellé ci-dessous ; fichier suivi au dépôt depuis le commit des couches 18/20/22). Complément cascade Task 22 (2026-10-23, session web-fdf5963c — directive « disciplines/techniques », veille 2025-2026) : `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md` archivé par `mv` byte-identité (fichier non suivi — jamais commité, adaptation règle d'or n°1 journalisée ; SHA-256 scellé ci-dessous ; provenance : le fichier corpus v1.7.1 était la source de l'archive scellée Task 20 — même octets). Complément cascade gen-plan v3.22.1 (2026-10-11, session web-b4d7dd19) : `PROMPT-MAITRE-GEN-PLAN-v3.22.0.md` archivé par `mv` byte-identité (fichier non suivi — jamais commité ; adaptation règle d'or n°1 journalisée, SHA-256 scellé ci-dessous).

| Fichier archivé | SHA-256 |
|-----------------|---------|
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.23.1.md | 02002b98586fbe38b45a760748b94a226846da527264fa3331c9dd31984ba59c |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md | dcecb4d62228cef38106e8770aeabf6b8ff5e33372f6992f1529575790196e01 |
| clone-chat/PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md | 1e8bcb65667a52a902d6010c210dcec9b3ac6c7c71e1b5d16101925992435c80 |
| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md | 74438d695d2fb7b4d7b406f576b16d7fa2706d0b4113183ea6e55fb84215e62e |
| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md | 8fceb8c1ac1dbb2848b87a8d154d9970a5b6418551898065caee56f9392de33e |
| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md | 907f899247ff5a087c781275223bfcacd779df3bc20a6734b9f34ef1dc1bbb54 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md | 6356ae3efe09522a8c6802147cfc88b0e0e58875b2dd3443d84a378395565ef6 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.7.0.md | e053f0ae7ccde425f7f15d84ab263738637a442e48c9e245824a9b32656b8880 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.8.0.md | 25ee244df6a790c02366a57617f2b5ee8ba80b2e3b931d963b7e06b53beef190 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.8.1.md | 69addcc9b1ef060ed348022b4753eccf2a160c6b66b38d946b8f5e49dd144ad9 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.9.0.md | a3c2fafaae6167b7a971a3120029349fca53f3d77c9eb9c3451108c597d82aee |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.10.0.md | aade3e718746827c4a0380d7e2a07bfa40cc4a07d989053f9c8b4696e485613d |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.11.0.md | bde9d5b5fab39647c78c020ef959640e17b52dd6d7a33d6844de1eda8e1c5a94 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.12.0.md | 55cb53dd8871a8bbfb2935976927d8232a79197610fcdae690d57869551f2a81 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.13.0.md | e9bdcfa56570a499a6ac35f0e40beb2b31d25db7ca5fa8c323137f48cdd08d97 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.16.0.md | 9baf0a2f10b4e0bf07d469ade7b9a23917974f3fb2b1d5c922e04787cf696aec |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.17.0.md | 1188c0ea067de8fbaa6e420268464f021014948a2cecfa1cb8ebdb1300d3b692 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.17.1.md | 31139a0738dcdc4faf513a28626d60a789dd2db88493e5931ccc99e645cda44d |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.17.2.md | 45f7e71989f44b85530a689580b969c78b6b33d009d9ab5e910c839f86d5dbe6 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.18.0.md | 65b68b2d7f423e280fa6353dd375e6d8b512043299166491a3cbbf8d44d32cc9 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.19.0.md | df6a59c04d02bc932ceb2d9bac48629ea073f8ca788df2e3af5fbf3a1db5103b |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.21.0.md | 0eab284a6c0a06d798856ff3300c09c6229ea898b19a55a503853e7a5fd64bec |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.22.0.md | 07118d824393b6464170f77669eabf5e262d2fbecd67fbe3ad136beab8300a4c |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.22.1.md | 45a01c3c90ec1eeb17bd602fa323b38c7e2c7804ec0796b5da539134959c0db5 |
| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.23.0.md | bba1b9c40dda47936fa9a1317897b99680c851f2cf4bf20e675a954da10e724b |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md | 16f82edb358ce36cfffbbfb9058ffda4d1d8a1e7d144791f11cbc82f67b60063 |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.5.0.md | 8dfc29a77633502609abc7a1d68a73cf53be40be7a7d5a6fd2670d1a40bfb8cf |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md | 9b3fad20a188aeb95a21cf251fb71a36a9a4b038bbb8a1fff96599f4adfba0b5 |
| correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.6.0.md | 45dfedb4812e74304310300947bfe2bca65b4da3f3c94c01d58c18b9a9c15209 |
