# @historique/ — Archive documentaire des versions des prompts maîtres et des skills

> **Version** : 1.0.0
> **Date** : 2026-10-11 (Task 16, session web-b93f42fa — directive propriétaire « plusieurs versions des prompts maitres → ne garder que la dernière version… crée un dossier @historique/ »)
> **Nature** : dossier d'infrastructure documentaire — **pas un skill, pas de SKILL.md** (convention SHARED §1.2 : préfixe `@` = ASCII 64, dossier non-skill en tête du listing `skills/`, précédent `@mon-ecosysteme/`)

## 1. Objet

Ce dossier conserve l'**historique des versions** des prompts maîtres de l'écosystème (3 familles : gen-plan, correct-work, clone-chat) et des skills, afin que le corpus canonique `skills/@mon-ecosysteme/` ne porte plus que la **dernière version** de chaque prompt maître. Il satisfait la contrainte propriétaire : l'historique n'augmente **ni la taille des prompts maîtres** (les PMs sources ne sont jamais édités — byte-identité prouvée), **ni celle du dossier `@mon-ecosysteme/`** (les versions antérieures y sont retirées, pas copiées).

## 2. Contenu

| Élément | Rôle |
|---------|------|
| `historique-versions-prompts-maitres.md` | Distillation consolidée : par famille, par version — particularités du skill installé, améliorations implantées, avantages par rapport à la version précédente. Sources primaire : tables §7 des PMs les plus récents, SYNC-CONTEXT, PM-INSTALL §7, registre KB. |
| `prompts-maitres/gen-plan/` | 15 PMs GEN-PLAN historiques (v3.6.1 → v3.19.0), déplacés du corpus `git mv` — byte-identité prouvée SHA-256 contre les blobs du commit de référence (b36f177, rapport Task 16). |
| `prompts-maitres/correct-work/` | 4 PMs CORRECT-WORK historiques (v2.4.0 → v2.6.0), mêmes garanties. |

## 3. Règles de conservation

1. **Byte-identité (R2)** : les fichiers archivés ici ne sont JAMAIS édités. Leurs blocs `CONTEXTE SYSTÈME` figés et leurs §7 d'époque restent intacts (statut « non-cibles de resynchronisation », SYNC-CONTEXT — rétro-compatibilité R2).
2. **Unicité (R4 anti-duplication)** : un fichier archivé ici est RETIRÉ du corpus `@mon-ecosysteme/` (déplacement, pas copie) — aucun homonyme ne peut exister des deux côtés. Ce dossier n'est pas un doublon du corpus : c'est l'archive des versions supprimées.
3. **Jamais source d'installation (garde R2 PM-INSTALL §3.2)** : les étapes 3-5 du pipeline d'installation ne mobilisent que le PM le plus récent du corpus (dérivation dynamique KO-L003). Les fichiers de ce dossier sont consultatifs.
4. **Différence avec l'historique vivant** : la table §7 de chaque PM le plus récent reste la source de vérité de l'historique de sa famille ; le fichier de distillation du présent dossier en est l'archive documentaire (instantané daté) — en cas de divergence, le §7 du PM vivant fait foi.

## 4. Procédure de mise à jour

À chaque montée de version d'une famille (règle KO-L004 — génération automatique du PM par `scripts/generer-pm-skill.py §2quater PM-INSTALL`) :

1. Le nouveau PM est généré dans `skills/@mon-ecosysteme/` (recalibrage croisé inclus) ;
2. Le PM supplanté est déplacé ici par `git mv` (`prompts-maitres/<famille>/`), byte-identité prouvée SHA-256 avant/après ;
3. Sa ligne est ajoutée à `historique-versions-prompts-maitres.md` (table de sa famille, sources : §7 du nouveau PM) ;
4. La présente table §2 et l'index §5 du fichier de distillation sont rafraîchis ;
5. Recalibrage croisé KO-L004 standard (CORPUS_ATTENDU, manifeste integrity, archive, orchestrateur ULTRA) et sweep arbitres avant tout commit.
