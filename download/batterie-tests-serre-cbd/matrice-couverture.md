# Matrice de couverture — batterie-tests-serre-cbd

> Batterie implémentée et exécutée (M7, 2026-10-25) — **verdict global : PASS — 8 PASS / 0 ECHEC / 0 NON_IMPLÉMENTÉ, code 0, ×2 (idempotence)**.
> Protocole STATUT respecté : aucun squelette résiduel ; chaque test passe `PRÊT` puis exécution réelle.
> Exécution : `python3 run_all.py` (verdicts par test + `journal/synthese.json`).

## Exigences ↔ tests fonctionnels

| Exigence | Test | Squelette | Verdict | Détail |
|----------|------|-----------|---------|--------|
| EF-03 | TF-01 | `tf_01_ef_03.py` | **PASS** | 10/10 cas borniers conformes ; strictitude des inégalités énergie (0,0005→healthy, 0,001→light) ; priorité severe |
| EF-04 | TF-02 | `tf_02_ef_04.py` | **PASS** | 4/4 schémas invalides rejetés (422 + détail) ; charge valide acceptée (202) |
| ENF-02 | TF-02 | `tf_02_ef_04.py` | **PASS** | sans en-tête→401, clé invalide→401, clé valide→200 (100 % rejets) |
| EF-06 | TF-03 | `tf_03_ef_06.py` | **PASS** | 1 commande complète par décision non-healthy ; healthy→0 commande ; priorité severe < light ; mapping déterministe |
| EF-01 | TF-04 | `tf_04_ef_01.py` | **PASS** | 12/12 champs obligatoires ; bornes ordonnées ; sample_rate ≥ 192 kS/s (Nyquist 80 kHz + 20 %) ; champ manquant détecté |
| EF-05 | TF-05 | `tf_05_ef_05.py` | **PASS** | model_id connu du registre ; model_id inconnu rejeté (0 orpheline) ; registre porte version + 4 seuils |
| EF-07 | TF-06 | `tf_06_ef_07.py` | **PASS** | 200 + 3 dépendances ; réponse < 1 s (mesurée, marge large) ; dépendance dégradée→503 |

## Sous-systèmes matériels ↔ tests TH

| TH | Sous-système | Exigences rattachées | Verdict |
|----|--------------|---------------------|---------|
| TH-01 | SS-02 Traitement de signal — capteur acoustique virtuel (porte 40-80 kHz + hystérésis, biais 0,5 dB, quantification 0,1 dB, graine 42) | EF-02, EF-08 (+ I-01) | **PASS** — 0 pic hors bande (20 kHz, 5000 essais) ; détection 100 % des clics bande (805/805) ; régime stress détecté ~35 clics/h (tolérance 20 %) ; régime sain ≤ 1/h ; déterminisme prouvé |
| TH-02 | SS-01 Acquisition — propagation ultrasonore atténuée (divergence + absorption f²/humidité, mécanismes ISO 9613-2 [S1] transposés — simplification documentée, graine 42) | ENF-08 (+ [HYP-03]) | **PASS** — ≥ 95 % des clics 40-60 kHz détectés à 5 m (mesuré 100 %) ; monotonie distance 4 m ≥ 5 m ≥ 6 m ; absorption décroissante en humidité ; 80 kHz plus atténué que 40 kHz (honnêteté haut de bande) |

## Non-couverture assumée

| Exigence | Raison NON VÉRIFIABLE | Levier pour la couvrir |
|----------|----------------------|------------------------|
| EF-08 (cadence discriminante sur espèce chanvre) | TH-01 simule la signature générique S-A (tomate) — la transposition chanvre est [HYP-02], hors simulation sans données terrain | Campagne terrain J-5 : capteurs réels, recalibrage registre, extension TH-01 aux données chanvre |
| ENF-01 (latence p95 ≤ 500 ms) | Nécessite le service API réel en charge (mock non instrumenté de latence dans cette batterie) | Benchmark sur mock puis prod (J-3) : 100 requêtes séquentielles, p95 mesuré |
| ENF-03 (sanitisation 0 motif) | Le scan opère sur l'archive finale produite par les scripts S-B, non présente dans ce sandbox | Exécuter checks_report.sh sur l'archive packagée (J-4) |
| ENF-04 (Dockerfile durci) | Le Dockerfile S-B n'est pas dans ce sandbox | Lint Dockerfile + build image en CI (J-4) |
| ENF-05 (trajectoire OAuth2/mTLS) | Vérification documentaire — présent au dossier de conception SS-04 (revue) | Revue propriétaire J-1 |
| ENF-06 (pipeline 5 étapes) | Les fichiers CI (.gitlab-ci.yml, azure-pipelines.yml) S-B ne sont pas dans ce sandbox | Vérification mécanique des fichiers de pipeline en J-4 |
| EF-04/API contractuelle complète (OpenAPI de bout en bout) | La batterie vérifie le contrat de validation/auth par référence ; le serveur réel n'est pas déployé ici | Brancher TF-02 sur le mock réel puis la prod (J-3) |

> Aucune cellule vide injustifiée : 7 PASS exécutés couvrent EF-01, EF-03..EF-07, ENF-02 et ENF-08 (par TH-02) ; les 6 non-couvertures restantes sont **assumées, motivées et assorties de leur levier** — conformément au protocole anti-couverture-alléguée (R3).
