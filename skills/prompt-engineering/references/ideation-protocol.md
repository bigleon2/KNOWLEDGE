
<!-- PATTERN:IDEATION-PROTOCOL-v1.0.0 -->

# Protocole d'idéation — Tree of Thought (mode M5, prompt-engineering v2.1.0)

## Pre-check (3 questions) — l'idéation ToT est déclenchée si au moins 2 réponses sont OUI

1. Le problème est-il ouvert (plusieurs solutions plausibles, pas de recette unique) ?
2. Les enjeux sont-ils élevés (artefact durable, coût d'erreur élevé, forte visibilité) ?
3. La demande est-elle explicite (contraintes et formats exprimés, pas d'ambiguïté S1) ?

## Tree of Thought — 5 étapes

1. **Cadre** — énoncer le problème, les contraintes, le format de sortie attendu.
2. **Divergence** — produire N idées nouvelles, V variantes d'idées existantes,
   F idées folles (quota N + V + F >= 20 avant toute convergence).
3. **Exploration** — développer chaque branche prometteuse (prémisses → conséquences).
4. **Élagage** — noter chaque branche (grille §1.4) ; couper sous le seuil.
5. **Convergence** — fusionner les 2-3 meilleures branches en une solution documentée
   (les branches écartées restent tracées pour ré-audit).

## Les 6 frames de recadrage

utilisateur · système · contrainte · ressource · risque · temps — chaque idée candidate
est re-lue sous au moins 3 frames avant l'élagage.

Reconstitué session B12-r56 — l'original N20 (r41) est perdu (incident B-17-r56) ; re-ancré sur le worklog survivant (Tasks 33-42) et le PM gen-plan v3.13.0 survivant (corpus). Règle N1 auto-portance.

<!-- FIN-PATTERN:IDEATION-PROTOCOL-v1.0.0 -->
