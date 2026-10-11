# Historique par skill — clone-chat

> **Version** : 1.0.0 — **Date** : 2026-10-11 (Task 17-B, session web-b93f42fa — directive propriétaire « un historique par skill »)
> **Version vivante (corpus)** : v2.0.1 — `skills/@mon-ecosysteme/PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md` (sa table §7 fait foi)
> **Versions archivées** : 1 PM (v2.0.0) dans `prompts-maitres/clone-chat/` — `git mv` byte-identité R4 (Task 12, 2026-10-12)
> **Provenance** : tables migrées verbatim de `historique-versions-prompts-maitres.md` §4 (fichier retiré après migration — R4 une information, une source ; Task 17-B)

## Famille CLONE-CHAT — 5 versions (skill : clone-chat)

**Particularité durable du skill** : archivage de session en document-cloné auto-suffisant — 7+1 étapes, intégralité du contexte (décisions, artefacts, worklog), format Markdown unique, propriété d'auto-clonage, reprise par session héritière.

| Version | Date | Améliorations implantées (source §7 du PM v2.0.0) | Avantage par rapport à la version précédente |
|---------|------|---------------------------------------------------|----------------------------------------------|
| v1.0.0 | 2026-07-29 | Version initiale : 7 étapes, template, auto-clonage | — (point de départ) |
| v1.1.0 | 2026-07-29 | 8 corrections correct-work (§0-§5, #token, chemins) | Conformité vérifiée par correct-work dès la première lignée (seuil in extenso, chemins relatifs, alignement SKILL.md ↔ template) |
| v1.2.0 | 2026-07-29 | Étape 3.5 Context Drift, 5 types de dérive, 8 checks, gen-plan KB | La dérive de contexte est détectée et typée à l'archivage au lieu d'être découverte à la reprise |
| v2.0.1 | 2026-10-12 | Task 12 (directive propriétaire « appliquer les corrections », session web-b4d7dd19 — gen-plan(step)) : dependencies += skill-creator >= v1.0.0 (conventions — alignement frontmatter sur KB « Dépend de »/SHARED §3.1, résorption F-c1 Task 12) ; §5.2 item 8 harmonisé au modèle PM-§7 (R4 une information une source — résorption F-c2) ; recalibrage croisé KO-L004 : SHARED v1.7.7 (§7 dé-figage pins n°53 + §6.1), PM-INSTALL v1.7.1 (§2ter/§A.3), @historique/prompts-maitres/clone-chat/ (git mv byte-identité R4), ECO_SKILLS arbitre, ULTRA régénéré (4 familles + routes refactoring + ECO_SKILLS dérivée KB + date non figée) | Le skill déclare ses conventions structurelles dans son frontmatter (cohérence FM/KB/SHARED ×3 niveaux) et son historique est porté par le PM vivant (R4 une information une source) — **VERSION VIVANTE (corpus)** |
| v2.0.0 | 2026-08-09 | Harmonisation écosystème maître : gen-plan v3.6.0, correct-work v2.3.0, 78 skills, variables SHARED, dependencies frontmatter, worklog SHARED §1.4, prompt maître | Le clone est aligné sur tout l'écosystème (variables, dépendances, worklog) — reprise par session héritière fiable — supplantée par v2.0.1 le 2026-10-12 — archivée |

Révisions documentaires de la famille (sans changement de version du skill) : révisions du PROMPT 1.0.1 / 1.0.2 / 1.0.3 (2026-09-05 → 2026-09-06 — toilettage de cohérence §6, correction de références internes, complétude du template §9.1 bloc « §1.0 Héritage — chaîne de clonage » ; Task 21 observation S4 ; la version du skill reste v2.0.0).
Fichiers archivés de la famille : aucun (v2.0.0 est la version vivante depuis sa création — la lignée v1.x n'a jamais été matérialisée au corpus).
