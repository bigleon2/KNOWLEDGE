# Answer Key — Lignée B12 (registre des décisions vérifiables)

> **Premier registre réel du pattern Answer Key** (propositions-qwen.md §1.1,
> intégration N19 — demande n°33, session B12-r40). Idempotent, immuable après
> validation E8 (R2 : ne jamais rétrograder — extension uniquement).
> Priorités = sévérité correct-work (S1-S4). Statuts mis à jour à chaque E2/E5.

```yaml
answer_key:
  metadata:
    created: "2026-09-19"
    source_skill: "gen-plan"
    source_version: "3.12.0"
    source_session: "B12-r40"
    decisions_count: 10

  decisions:
    - id: "D001"
      criterion: "Aucune attente longue intra-tour (les sommeils sont annulés par la passerelle IM)"
      verification: "grep scripts/ : aucun sleep > 120 s hors garde démon ; probes = 1/message"
      source: "R3-A11 (r20-r24) — boucle d'adaptation documentée worklog"
      priority: "S2"
      status: "verified"

    - id: "D002"
      criterion: "La cadence 'continue' 2 h n'est JAMAIS simulée (honnêteté R3)"
      verification: "constat expérimental tracé (reaper sandbox) + log tmp/sonde-2h/loop.log"
      source: "R3-A17-bis (r38) — démon non persistant prouvé"
      priority: "S2"
      status: "verified"

    - id: "D003"
      criterion: "Toute restauration part des sources locales survivantes (filesystem fait foi)"
      verification: "journal restauration tmp/b17-restauration/ + SHA référence re-posée"
      source: "N13 (r29) + N18 (r40) — pattern éprouvé"
      priority: "S1"
      status: "verified"

    - id: "D004"
      criterion: "Purge du canal : uniquement les porteurs < version courante"
      verification: "SYNC_MAP canal = 8 courants byte-identiques ; idempotence ×2"
      source: "N14-c (r32) — adaptation R3-A15, pattern N6"
      priority: "S2"
      status: "verified"

    - id: "D005"
      criterion: "Les planchers de version sont directionnels (pas d'égalité stricte) pour artefacts vivants"
      verification: "verify-correct-work 16/16 (check planchers) PASS"
      source: "leçon E21 — correct-work §11"
      priority: "S3"
      status: "verified"

    - id: "D006"
      criterion: "Canal (SYNC_MAP 8) et corpus (CORPUS_ATTENDU 17) restent des compteurs séparés"
      verification: "integrity 38/38 = cible A7 exacte"
      source: "cible A7 (r32) — calibrage arbitres N14-c"
      priority: "S2"
      status: "verified"

    - id: "D007"
      criterion: "Le miroir _prompts-maitres est byte-identique au corpus (sens corpus → miroir fait foi)"
      verification: "restore-miroir.py no-op 17/17 (idempotence prouvée)"
      source: "invariant SHARED §1.2 — correction R3-A16 (r33)"
      priority: "S2"
      status: "verified"

    - id: "D008"
      criterion: "L'état réel du filesystem prime sur tout résumé de contexte hérité"
      verification: "chaque tour ouvre par la lecture seule préalable (B-11) — worklog"
      source: "leçon B-11 (r30) — appliquée à chaque reprise"
      priority: "S1"
      status: "verified"

    - id: "D009"
      criterion: "Ordre de restauration : réinstallation B9 (N13) PUIS montée v3.12.0 (N14-b) PUIS normalise-frontmatter"
      verification: "journal N18 : 3 contre-ordres ont produit régression/frontmatters cassés ; ordre corrigé → certification 5/5"
      source: "N18 (r40) — incident B-17, 3 échecs diagnostiqués"
      priority: "S1"
      status: "verified"

    - id: "D010"
      criterion: "Toute édition planaire multi-lots est suivie d'une vérification B-14 (grep marqueurs)"
      verification: "B-14 7/7 à 9/10 ancres OK documentées à chaque E13"
      source: "leçon MultiEdit atomicité partielle (r30-r39)"
      priority: "S3"
      status: "verified"
```

## Procédure de mise à jour (extension R2 uniquement)

1. Toute nouvelle décision E1 → entrée `D0NN` appendue (jamais éditée a posteriori)
2. `status` uniquement `pending → verified|failed` (jamais l'inverse)
3. À E8 : les critères S1/S2 `verified` conditionnent le verdict PASS
4. Vérification mécanique : `python3 -c` yaml-safe parse + comptage des statuts
