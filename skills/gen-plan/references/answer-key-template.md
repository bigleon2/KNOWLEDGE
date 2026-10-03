# Answer Key Template — décisions E1 vérifiables mécaniquement

Source : propositions-qwen.md §1.1 (pattern Answer Key), intégré phase N20 (gen-plan v3.13.0).
Hook gen-plan : **E1** (answer key obligatoire) et **E7/E8** (arbitre `scripts/answer-key-checker.py`).

<!-- PATTERN:ANSWER-KEY-TEMPLATE-v1.0.0 -->

## §1 — Objet

L'answer key transforme chaque décision prise à l'étape E1 en une entrée vérifiable
mécaniquement. À E8, l'arbitre `scripts/answer-key-checker.py` contrôle que chaque
décision porte un critère, une vérification exécutable, une source, une priorité et un
statut — la promesse du plan devient un contrat testable (héritage harness-engineering :
boucle de vérification avec graders et feedback exploitable).

## §2 — Schéma YAML d'une décision

```yaml
decisions:
  - id: "D001"
    criterion: "Le livrable X est produit au format Y"
    verification: "python3 scripts/arbitre-x.py && grep -c 'Y' <fichier> > 0"
    source: "demande utilisateur (trace <id>)"
    priority: "S2"
    status: "pending"
```

| Champ | Rôle | Contrainte |
|-------|------|------------|
| `id` | Identifiant séquentiel `D0NN` | Jamais réutilisé (R1-R6) |
| `criterion` | Ce que la décision promet | Phrase testable, une seule promesse par décision |
| `verification` | Commande exécutable qui prouve le critère | Python uniquement (N3), rejeu stable (idempotence) |
| `source` | Origine de la décision | Trace, demande, convention (SHARED §) |
| `priority` | Sévérité si violée | S1 (critique) à S4 (cosmétique) |
| `status` | État de la vérification | `pending` → `verified` \| `failed` — jamais inversé sans re-exécution |

## §3 — Les 5 règles d'écriture

1. **Une décision = une promesse testable** : si la vérification ne peut pas échouer,
   ce n'est pas un critère.
2. **Vérification exécutable d'abord** : chaque `verification` est une commande réelle
   (Python, N3) re-jouable sans état caché ; les artefacts textuels sont vérifiés par
   comptage/comparaison, pas par jugement.
3. **Provenance obligatoire** : toute décision cite sa source (demande utilisateur,
   convention SHARED, leçon knowledge-observer) — pas de décision orpheline.
4. **Priorité honnête** : S1-S4 reflètent l'impact réel ; un S1 faux crée des faux
   verdicts (leçon KO-L003 — arbitres à invariants dynamisés).
5. **Statut mis à jour par l'exécution, jamais à la main** : `status` bascule à
   `verified`/`failed` uniquement sur la sortie réelle de la commande de vérification ;
   l'intégration correct-work re-vérifie les statuts à chaque passage (hook Étape 2).

## §4 — Intégration correct-work

- Le plan d'actions (E7) référence l'answer key ; à E8, le verdict PASS requiert
  0 S1/S2 en échec (`scripts/answer-key-checker.py` — 16 checks, verdict ALL PASS ×2
  pour l'idempotence).
- En mode CIBLE, l'Étape 2 (Erreurs et omissions) re-joue les `verification` des
  décisions marquées `verified` ; une régression ramène le statut à `failed`
  (R2 : pas de statut fantôme).
- Les corrections appliquées après un FAIL font l'objet d'une nouvelle décision
  `D0NN` (jamais d'édition silencieuse de l'entrée initiale).

<!-- FIN-PATTERN:ANSWER-KEY-TEMPLATE-v1.0.0 -->

> Provenance : reconstituée post-wipe (B13-r4) d'après le schéma vérifié de
> `answer-key-b12.md` (N19, 10/10 verified) et les 16 checks de l'arbitre survivant
> `scripts/answer-key-checker.py` (N20) — le contenu exact de la version N20 originale
> reste perdu au wipe inter-sessions.
