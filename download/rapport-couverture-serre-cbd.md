# Rapport de couverture exigences ↔ tests — SERRE CBD

> M7 TESTER (livrable L-5) · 2026-10-25 · Batterie : `download/batterie-tests-serre-cbd/` · Skill `cahier-des-charges` v2.0.1
> **Verdict global : PASS — 8 PASS / 0 ECHEC / 0 NON_IMPLÉMENTÉ — code 0, ×2 (idempotence prouvée)**

## 1. Résumé de vérification

La batterie de tests M7 du projet SERRE CBD (système d'écoute acoustique du stress des plantes en serre de chanvre CBD) a été générée par `scaffold_tests.py` v2.0.0, puis intégralement implémentée : **6 tests fonctionnels (TF-01 à TF-06) et 2 tests matériels simulés (TH-01, TH-02)**, tous passés au statut `PRÊT` et exécutés réellement. Le harnais `run_all.py` rend un verdict global **PASS** avec code de sortie 0, deux exécutions consécutives identiques (déterminisme : graines fixes 42, aucune horloge non contrôlée). Un défaut de données bornières détecté au premier passage (cas (0, 0,001) attendu à tort `stress_severe` alors que le contrat strict donne `stress_light`) a été corrigé dans le test — l'implémentation de référence était conforme au contrat — puis re-exécuté : PASS stable. C'est exactement le rôle du protocole STATUT : rien n'est allégué, tout est exécuté.

## 2. Couverture par exigence

| Exigence | Vérifiée par | Verdict | Mécanisme de preuve |
|----------|--------------|---------|---------------------|
| EF-01 (AcqWindow complète) | TF-04 | PASS | 12 champs obligatoires, bornes ordonnées, Nyquist 80 kHz + 20 % (≥ 192 kS/s), détection de champ manquant |
| EF-02 (filtrage 40-80 kHz) | TH-01 | PASS | 0 pic détecté sur 5000 essais hors bande (20 kHz) ; 100 % des clics in-bande détectés (805/805) |
| EF-03 (seuils d'inférence) | TF-01 | PASS | 10/10 cas borniers (frontières 8/20 pics, 0,0005/0,001 énergie, strictitude prouvée, priorité severe) |
| EF-04 (API contractuelle) | TF-02 | PASS | 4/4 schémas invalides → 422 avec détail ; charge valide → 202 |
| EF-05 (traçabilité registre) | TF-05 | PASS | model_id connu obligatoire ; 0 décision orpheline (rejet explicite) ; version + seuils au registre |
| EF-06 (mapping PLC) | TF-03 | PASS | exactement 1 commande complète par décision non-healthy ; 0 pour healthy ; priorité severe < light ; déterministe |
| EF-07 (santé /health) | TF-06 | PASS | 200 + 3 dépendances ; < 1 s mesuré ; dégradation → 503 |
| EF-08 (cadence discriminante) | TH-01 | PASS | régime stress détecté ≈ 35 clics/h (tolérance 20 %) vs régime sain ≤ 1/h — séparation prouvée sur 24 h simulées ×2 graines |
| ENF-02 (authentification) | TF-02 | PASS | sans en-tête → 401 ; clé invalide → 401 ; clé valide → 200 |
| ENF-08 (écoute passive) | TH-02 + revue | PASS | portée ≥ 5 m prouvée par simulation de propagation (mécanismes [S1] transposés) — le système n'émet rien (revue d'architecture, dossier de conception SS-01) |
| ENF-01, ENF-03..ENF-07 | **non couvertes exécutables** | — | **Non-couvertures assumées** (voir §3) |

## 3. Non-couvertures assumées (anti-couverture-alléguée)

Six exigences ne sont pas vérifiables par tests exécutables dans ce sandbox, et le sont **explicitement** : ENF-01 (latence p95 — requiert le service réel en charge : benchmark J-3), ENF-03 (sanitisation sur l'archive finale — scripts de packaging S-B, J-4), ENF-04 (Dockerfile durci — lint+build CI, J-4), ENF-05 (trajectoire OAuth2/mTLS — revue documentaire, dossier de conception SS-04), ENF-06 (pipeline 5 étapes — fichiers CI S-B, J-4), et le volet chanvre de EF-08 (transposition d'espèce [HYP-02] — campagne terrain J-5). Chaque non-couverture porte sa raison et son levier dans la matrice de couverture — aucune n'est silencieuse, conformément au protocole R3 du skill.

## 4. Fondements scientifiques vérifiés dans les tests

Les constantes de simulation proviennent de la source fondatrice **Science & Vie SV-238443** (Hadany & Yovel, université de Tel-Aviv, revue *Cell*) : bande de clics **40-80 kHz** (TH-01 : porte passe-bande ; TH-02 : absorption croissante en f²), niveau **60-65 dB** (TH-01/TH-02 : émissions 60-65 dB), cadence **≈ 35 clics/h en stress hydrique contre < 1 son/h en régime sain** (TH-01 : séparation des régimes), portée **≤ 5 m** (TH-02 : cible contractuelle à 5 m), robustesse au mécanisme causal non confirmé — **hypothèse de cavitation** traitée comme [HYP-01] : les tests portent sur le signal observable, jamais sur la cause. Le seuil de sévérité élevé (blessure/coupure de tige du protocole S-A) est reflété par la priorité `stress_severe` > `stress_light` (TF-03).

## 5. Conclusion de vérification

Le contrat d'implémentation est **tenable et vérifié** : toute implémentation conforme du système (y compris le référentiel existant S-B à aligner en J-3) doit faire passer ces 8 tests sans modification des assertions. Les deux tests matériels simulés prouvent, sans matériel spécialisé (ENF-07), la faisabilité contractuelle de la détection dans la bande fondatrice et de la portée cible. Le dossier de validation est complet : batterie exécutable + `journal/synthese.json` + matrice de couverture sans cellule vide injustifiée + ce rapport.
