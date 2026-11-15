# Plan Task 100 — mission F1 : brancher l'étape 2 du pipeline eco_install sur le scelleur canonique v2.3

> gen-plan mode step (v3.43.0) · GO propriétaire trace `1a1dfb31d58350d5` sur la pendance F1 du point d'état Task 99 (finding suite 142 : véhicule de rescellement du pipeline eco_install incompatible avec l'arbitre integrity v2.3)

## Groupes

- **G1 — Enquête E1-E2** : lecture des deux véhicules — étape 2 du pipeline appelle `task21-f2-rebuild-archive.py` (v2.2, préserve l'archive entrante, piliers dans ses `RETRAITS_SANCTIONNES`) ; arbitre integrity attend corpus + piliers (v2.3) ; baseline capture pré-implémentation (S1) : archives repo/host 9 entrées 0 piliers SHA `3d903db2…` identiques, integrity 114/114 PASS — défaut LATENT.
- **G2 — Simulation préalable (règle d'or n°5)** : harnais `scripts/task100-mission-f1.py` mode `baseline` — S2 réplique bac à sable : une archive v2.3 (15 entrées, 6 piliers) rescellée par le véhicule v2.2 → **rc=0 ET 9 entrées, 0 piliers** (désempilement SILENCIEUX prouvé mécaniquement) → S4 **GO**.
- **G3 — Implémentation** : (i) `eco_install_pipeline.py` étape 2 → `task-f5-seal-archive-v23.py` + **étape 2bis** régénération du manifeste par l'arbitre canonique (pense-bête du scelleur), rc propagés (anti-faux-succès F1 Task 22 conservé) ; (ii) `task-f5-seal-archive-v23.py` **byte-stable** (ZipInfo époque fixe 1980-01-01, politique Task 20 F3) — idempotence byte R6 + parité miroir repo↔hôte sans passe manuelle.
- **G4 — Rejeu réel** : pipeline réel rc=0 ×2 (étape 2 : 15 entrées piliers 6/6 ; 2bis : manifeste hôte 114/114 ; F3 : 0 divergence, garde R2 0 rétrogradation) ; harnais mode `rejeu` : idempotence ×2 (2 reseals SHA `26557e45…` byte-identiques) + parité miroir byte-identique repo/host + arbitres ×6 ALL PASS (tool-routing 6/6 — 2 scripts modifiés détectés et vérifiés frontmatter) + triggers 101/101.
- **G5 — Clôture** : rapport fusionné S1-S4 `scripts/task100-mission-f1-report.json` (+ miroirs hôte scripts et download) ; worklog suite 145 (parité) ; COMMIT « Task 100 CLOSE » + PUSH avec la clé de la session courante (leçon Task 98 — commit réel, E15 27ᵉ exposition) ; `ls-remote` de vérification.

## Answer key (vérifiables mécaniquement)

- **D001** : S1 capture pré-implémentation (9 entrées, 0 piliers, SHA `3d903db2…` parité) au rapport fusionné.
- **D002** : S2 rc=0 avec 6→0 piliers (désempilement silencieux) — deselement_silencieux=true.
- **D003** : pipeline réel rc=0, `etapes.2_archive` « 15 entrées (attendu 15) » piliers —.
- **D004** : pipeline réel `etapes.2_manifeste` « 114/114 PASS » + manifeste hôte écrit.
- **D005** : harnais rejeu — idempotence_x2_2_reseals_byte_identiques=true, parité SHA `26557e45…` repo=host.
- **D006** : certification-complete ALL PASS 6/6 AVANT commit (tool-routing 6/6) + triggers 101/101.
- **D007** : worklog parité hôte/dépôt (suite 145).
- **D008** : push vérifié `ls-remote` = SHA local ; E15 27ᵉ exposition consignée (rotation IMPÉRATIVE).

## Routage

[gen-plan] · scripts/ uniquement (0 skill KB / agent / registre KB modifié — couche script-creator, tool-routing N1/N2 rejoué 6/6) · KO-L009 (jeton mémoire de commande)
