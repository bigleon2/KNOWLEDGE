# Plan d'actions — Task 11 : lien de partage, PUSH, correct-work --bloc, clone-chat (continuation)

Généré le 2026-11-28 · gen-plan v3.47.0 (mode step) · session web-220878ed-c362-40f9-b12a-5aa08335c14d · propriétaire : directive 7ᵉ fenêtre (trace 1a21de5a9964f6b5 + 1a21de9d8a99fc41).

Ancrage : bootstrap canonique PM-INSTALL §3.2-c re-exécuté en tête de fenêtre — preflight RÉPARÉ (dérive 2874 fichiers, mode-only 0 contenu) → boucle E12-E13 (6 en-têtes §0 STALE corrigés : add-template-pdf v1.7.46, asr/llm/tts/vlm v1.7.44, mise-en-page v1.7.40 → SHARED v1.7.45) → **VERDICT INSTALLE**, certification ALL-PASS 6/6, garde É1-INSTALL OK. Pin 38573b0 (le dépôt origin/main est 8 commits devant — v3.48.0 côté dépôt — le host reste au pin demandé).

Relecture d'ancrage : 5ᵉ clone (`download/clone-session-web-220878ed-20261127-conversion-kps.md`, Tasks 9-10) + fin de discussion (directive Task 11) + état dépôt (origin/main 8 devant, 0 miroir session web-220878ed, worklog 837 Ko, dernière suite 166b).

## E1 — Analyse de la demande (answer key D001-D006)

- decision: D001 — le « lien de partage » de la discussion Z.AI est HORS CAPACITÉ assistant : aucun outil n'accède au mécanisme de partage de l'interface web ; produire une URL inventée est interdit (règle « jamais d'invention », R4) → différé propriétaire avec mode opératoire
  criterion: aucune URL fabriquée dans un quelconque artefact ; différé consigné au worklog + plan
  verification: scan des livrables Task 11 (0 URL https://chat.z.ai/ fabriquée) + entrée différé au worklog
  source: règles système + KO-L003 — priority S1 — status: deferred PROPRE
- decision: D002 — le « test du lien » dépend de D001 → différé (impossible sans lien réel fourni par l'interface)
  criterion: aucun test simulé ; différé consigné
  verification: worklog Task 11 (2 différés propriétaire)
  source: dépendance D001 — priority S2 — status: deferred PROPRE
- decision: D003 — PUSH : le PAT collé en clair dans la conversation est REFUSÉ (politique sécurité : ne jamais imprimer, stocker ni renvoyer un identifiant ; KO-L009 écosystème) — voie conforme = plugin GitHub authentifié bigleon2 (commits API, 0 jeton manipulé) ; textes seulement, binaires en différé ; RÉVOCATION immédiate du PAT exposé = rappel CRITIQUE
  criterion: commits atterris sur origin/main via plugin · 0 octet du PAT dans tout artefact · scan motif github_pat_ rc=0
  verification: get_commit origin/main (commits Task 11) + scan rg sur l'arbre
  source: politique plateforme + KO-L009 + alertes CRITIQUE suites 163-166b — priority S1 — status: pending
- decision: D004 — correct-work (projet) --bloc Task 11 avec vérificateur mécanique dédié (pattern verifier_cw_taskN.py)
  criterion: rapport download/rapport-cw-task11-projet.md verdict PASS + JSON de preuve
  verification: python3 scripts/verifier_cw_task11.py → 100 % PASS
  source: correct-work v2.12.1 — priority S1 — status: pending
- decision: D005 — clone-chat 6ᵉ de la lignée (Tasks 9-11), validation S1-S8 mécanique 8/8, scellé 0 secret
  criterion: clone présent en download/ + 8 checks PASS
  verification: scripts/verifier-task11-clone.py → 8/8
  source: clone-chat v2.0.2 — priority S1 — status: pending
- decision: D006 — worklog : suite 167 au dépôt (commit local, worklog 837 Ko hors capacité API) + entrée Task 11 au worklog hôte (append-only)
  criterion: 2 worklogs à jour, append-only, 0 réécriture
  verification: tail des 2 worklog.md
  source: worklog §1.4 — priority S2 — status: pending

## E3 — Classification : Type 1 (chaîne documentaire) — série D001/D002 (différés immédiats) → G1 miroir+PUSH → G2 CW --bloc → G3 clone → G4 worklogs.

## E4 — Estimation : #token ~35k (G1 8k · G2 8k · G3 10k · G4 5k · reports 4k).

## E9-E14 — Groupes d'exécution

- G1 — PUSH (D003) : miroir texte Tasks 9-10 + 5 clones lignée via push_files (commit A) ; Task 11 via push_files (commit B après G2-G3) ; binaires (2 PDF résumés, 3 schémas PNG, fiche PDF, source JPG, crops) = différé propriétaire (prochain PUSH git à clé fraîche) ; réveil propriétaire : RÉVOCATION PAT.
- G2 — correct-work (projet) --bloc : verifier_cw_task11.py (couvre plan, bootstrap, push, sécurité jeton, différés) → rapport.
- G3 — clone-chat 6ᵉ : clone-session-web-220878ed-20261128-tache11-partage-push.md + validation S1-S8.
- G4 — worklogs + scan final : suite 167 dépôt (commit local), Task 11 hôte, scan github_pat_ = 0.
