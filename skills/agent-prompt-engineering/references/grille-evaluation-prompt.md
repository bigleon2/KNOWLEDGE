# Grille d'évaluation de prompts — agent-prompt-engineering v1.0.0

> Source : SKILL.md §1.4. Ce fichier détaille l'usage opérationnel de la grille (mode M3) et la conduite de la boucle d'itération (§1.5).

## 1. Protocole d'évaluation M3

Pour chaque axe, le rapport M3 consigne : la note (PASS / PASS AVEC RÉSERVES / FAIL), la preuve (ligne ou section de l'artefact évalué), et — en cas de non-PASS — une recommandation classée par impact (fort / moyen / faible).

| Axe | Méthode de mesure | Preuve attendue |
|-----|-------------------|-----------------|
| Clarté | Relecture instruction par instruction ; détection des lectures alternatives possibles | Liste des ambiguïtés (vide = PASS) |
| Précision | Vérifier que chaque critère est mesurable : seuil chiffré, format, version minimale | Tableau critère → mesure |
| Structure | Comparer aux conventions SHARED §5 (structure type, tailles cibles) | Écarts de structure listés |
| Économie | Recherche de duplications intra et inter-fichiers (SHARED §6.3) ; verbiage | Occurrences dupliquées (0 = PASS) |
| Robustesse | Confronter le prompt aux cas limites : blocage, wipe inter-sessions, ressource dégradée | Couverture règle d'or n°1 |

Verdict global : le pire des verdicts par axe (convention correct-work).

## 2. Conduite de la boucle d'itération (§1.5)

1. **Itération k** : évaluation M3 → ajustements (un par axe sous seuil) → re-évaluation.
2. **Arrêt** : tous les axes PASS, ou k = 3. En cas d'arrêt sur dérive, journalisation au worklog (cause, axes restants, décision utilisateur requise).
3. **Traçabilité** : chaque itération produit un diff (artefact avant/après) — aucune édition silencieuse d'artefact PM-gouverné (révision de prompt uniquement, SHARED en-tête).

## 3. Mesures programmatiques

Quand un axe est mesurable par script (Python uniquement, N3), le script prime sur l'œil : comptage de duplications (économie), présence des sections obligatoires (structure), validité JSON/YAML (précision). Les scripts sont réutilisables entre itérations et leurs sorties archivées comme preuves.
