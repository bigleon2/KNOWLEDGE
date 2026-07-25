# Skill : resume-chat

> **Version** : 1.0.0  
> **Catégorie** : Méta-Analyse & Archivage  
> **Date** : 24 juillet 2026  
> **Auteur** : PEK v4.1 Architect  

## Description

Le skill `resume-chat` est conçu pour générer des résumés détaillés et structurés d'une discussion ou d'un projet. Il assure un tracking précis des versions des artefacts générés, reconstruit la chronologie des interactions et produit un livrable Markdown avec une Table des Matières (TOC) interactive.

## Paramètres d'Entrée

| Paramètre | Type | Valeurs par défaut | Description |
|---|---|---|---|
| `context` | string | Conversation history | Historique de la conversation ou fichiers joints à analyser. |
| `format` | enum | `markdown` | Format de sortie (`markdown`, `json`, `text`). |
| `include_toc` | boolean | `true` | Inclure une Table des Matières avec liens ancres. |
| `track_versions` | boolean | `true` | Activer le suivi des versions des artefacts mentionnés. |

## Pipeline d'Exécution (5 Étapes)

1.  **COLLECTE** : Lecture intégrale du contexte, identification des artefacts (code, docs, scripts) et extraction des métadonnées (versions, dates).
2.  **CHRONOLOGIE** : Reconstruction de la timeline des interactions, regroupement par phases thématiques et identification des points de bascule.
3.  **TRACKING VERSIONS** : Listing des versions successives pour chaque artefact, description concise de l'évolution (≤ 3 lignes) et calcul des gains/métriques.
4.  **STRUCTURATION** : Génération de la TOC, organisation en sections (Vue d'ensemble, Historique, Optimisations) et application du formatage Markdown strict.
5.  **VALIDATION** : Vérification de la complétude, validation des liens TOC et respect de la concision des descriptions.

## Sortie Attendue

Un fichier `.md` téléchargeable contenant :
*   Un titre principal et une Table des Matières interactive.
*   Une vue d'ensemble chronologique sous forme de tableau.
*   Un historique détaillé des artefacts avec leurs évolutions.
*   Une analyse des optimisations clés apportées durant la discussion.
*   Les annexes techniques (skills générés, scripts, configurations).

## Règles Critiques

*   **Préservation** : Ne jamais inventer de versions ou d'évolutions non présentes dans le contexte.
*   **Concision** : Les descriptions d'évolution doivent tenir en 3 lignes maximum.
*   **Exhaustivité** : Couvrir tous les artefacts majeurs mentionnés ou générés.
*   **Formatage** : Utiliser un Markdown strict avec des liens ancres fonctionnels pour la TOC.
*   **Tracking** : Indiquer clairement les numéros de version et les dates associées.

## Intégration dans l'Écosystème

*   **Emplacement** : `KNOWLEDGE.md` section 3.7 (Skills Intégrés).
*   **Invocation** : Déclenché par les phrases clés "résumé chat", "historique versions", "archive discussion".
*   **Dépendances** : Utilise `gen-plan` pour la structure de base et `correct-work` pour la validation finale du résumé.

## Exemple d'Utilisation

**Input** : "Fais un résumé structuré de notre discussion sur le PEK v4.1 en suivant les versions."
**Output** : Génération de `RESUME-DISCUSSION-PEK-v4.1.md` avec TOC et tracking des 5 artefacts principaux.
