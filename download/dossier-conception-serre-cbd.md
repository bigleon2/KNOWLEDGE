# Dossier de conception — SERRE CBD (écoute acoustique du stress des plantes)

> M6 CONCEVOIR — skill `cahier-des-charges` v2.0.1 · 2026-10-25 · Complète le CDC (EF/ENF → SS/I) · Profil SE : standard

## 1. Architecture générale

L'architecture reprend la chaîne fonctionnelle du référentiel existant [S-B] et la découpe en six sous-systèmes à responsabilités disjointes, reliés par cinq interfaces typées : **capteurs acoustiques → SS-01 acquisition → SS-02 traitement de signal → SS-03 inférence → SS-04 API → SS-05 orchestration PLC**, sous la surveillance transverse de **SS-06 exploitation**. Ce découpage suit la logique du contrat : chaque exigence EF/ENF s'alloue à exactement un sous-système responsable (avec contributeurs), ce qui rend chaque échec de test directement attribuable. Les schémas de données (`AcqWindow`, `StressDecision`, `PLCCommand`) constituent la colonne vertébrale : ils sont les seuls objets qui circulent entre sous-systèmes, et leur validation de schéma est un mécanisme de défense en profondeur (un sous-système refuse toute entrée non conforme).

## 2. Sous-systèmes

| ID | Sous-système | Responsabilité | Exigences allouées | Conception retenue |
|----|--------------|----------------|--------------------|--------------------|
| SS-01 | **Acquisition acoustique** | Écoute passive ultrasonore 40-80 kHz, fenêtrage temporel, stockage audio brut (raw_audio_ref) | EF-01 (contributeur), ENF-08 | Micros ultrasoniques non fixés aux plantes (méthode S-A), échantillonnage suffisant pour la bande (≥ 192 kS/s), fenêtres AcqWindow périodiques ; passivité stricte (0 émetteur) |
| SS-02 | **Traitement de signal** | Filtrage passe-bande 40-80 kHz, détection de pics, extraction des traits n_peaks / mean_energy / median_freq / peak_list_summary | EF-01 (contributeur), EF-02, EF-08 | Filtre passe-bande normalisé [S2 IEC 61260], détecteur de crêtes avec hystérésis, traits agrégés par fenêtre ; robustesse au bruit (hystérésis + seuil d'énergie) |
| SS-03 | **Inférence de stress** | Classification healthy / stress_light / stress_severe à seuils explicites, registre de modèles, confiance | EF-03, EF-05, ENF-01 | Règles contractuelles sur (n_peaks, mean_energy) — seuils en configuration (`model_registry.json` : model_id, version, seuils) ; 0 décision sans model_id (contrat EF-05) ; extension ML supervisée possible sans changer le contrat |
| SS-04 | **API d'ingestion et d'inférence** | Contrat OpenAPI, authentification, validation de schémas, mock + production | EF-04, ENF-02, ENF-05 | Flask/Gunicorn (S-B), `POST /ingest/acqwindow`, `POST /ml/infer`, ApiKeyAuth `x-api-key` phase 1 ; trajectoire OAuth2/mTLS documentée (ENF-05) ; erreurs 4xx détaillées |
| SS-05 | **Orchestration PLC** | Conversion StressDecision → PLCCommand, priorisation, durées, idempotence des commandes | EF-06 | Mapper décision→action paramétrable ; stress_severe ⇒ priorité haute (préempte), stress_light ⇒ priorité normale ; journal des commandes ; sécurité : actions réversibles uniquement |
| SS-06 | **Exploitation & qualité** | Conteneur durci, santé, CI/CD, sanitisation des secrets, packaging (ZIP/SHA256/Base64), rapports | EF-07, ENF-03, ENF-04, ENF-06, ENF-07 | Docker multi-stage non-root + HEALTHCHECK [S-B] ; /health état dépendances ; pipelines GitLab + Azure (5 étapes contractuelles) ; sanitisation automatique (clés API, Bearer, JWT, e-mails, AWS, access_token) ; graine fixe pour la reproductibilité |

## 3. Interfaces

| ID | Interface | De → À | Contrat | Points de vérification |
|----|-----------|--------|---------|------------------------|
| I-01 | Signal acoustique → Acquisition | Physique → SS-01 | Bande 40-80 kHz, niveaux ~60-65 dB à ≤ 5 m (S-A) ; capteurs IP adaptés [S3] | TH-01 (régimes sain/stress), TH-02 (portée) |
| I-02 | Acquisition → Traitement | SS-01 → SS-02 | Flux audio fenêtré + métadonnées env | TF-04 (intégrité AcqWindow) |
| I-03 | Traitement → Inférence | SS-02 → SS-03 | `AcqWindow` validé par schéma JSON (champs obligatoires EF-01) | TF-01 (seuils borniers), TF-04 |
| I-04 | Inférence → API → Orchestration | SS-03 → SS-04 → SS-05 | `POST /ml/infer` → `StressDecision` → `PLCCommand` (target/action/parameters/duration_s/priority) | TF-02 (schéma+auth), TF-03 (mapping+priorité) |
| I-05 | Exploitation ↔ tous | SS-06 ↔ SS-01..05 | `/health` (2xx < 1 s), logs, journal de commandes, registre de modèles | TF-05 (registre), TF-06 (santé) |

## 4. Allocation et couverture exigences → sous-systèmes

- **EF-01** SS-01+SS-02 (I-02/I-03) · **EF-02** SS-02 (I-01, TH-01) · **EF-03** SS-03 (I-03, TF-01) · **EF-04** SS-04 (I-04, TF-02) · **EF-05** SS-03 (I-05, TF-05) · **EF-06** SS-05 (I-04, TF-03) · **EF-07** SS-06 (I-05, TF-06) · **EF-08** SS-02+SS-03 (TH-01)
- **ENF-01** SS-03+SS-04 · **ENF-02** SS-04 (TF-02) · **ENF-03** SS-06 · **ENF-04** SS-06 · **ENF-05** SS-04 (revue) · **ENF-06** SS-06 · **ENF-07** batterie M7 · **ENF-08** SS-01 (TH-02/revue)
- Toute exigence sans sous-système responsable est un défaut de conception : la matrice ci-dessus est exhaustive sur EF-01..EF-08 et ENF-01..ENF-08 (aucune cellule vide).

## 5. Risques de conception et parades

| Risque | Parade intégrée à la conception |
|--------|--------------------------------|
| Absorption ultrasonore en air humide ⇒ portée < 5 m [HYP-03] | TH-02 simule la dépendance fréquence/humidité ; densité de capteurs paramétrable ; marges contractuelles explicites |
| Faux clics (insectes, équipements) dans la bande (S-A : chauves-souris/insectes la perçoivent) | Filtrage passe-bande strict [S2], hystérésis de détection, cadence discriminante (35/h vs < 1/h) plutôt qu'un pic isolé [EF-08] |
| Seuils non transposables au chanvre [HYP-02] | Seuils en configuration (registre versionné), jamais codés en dur ; recalibrage terrain J-5 sans changement de code |
| Décision orpheline / non traçable | Contrat EF-05 : 0 décision sans model_id du registre ; journalisation complète |
| Commande PLC inappropriée | Mapper paramétrable + priorités + actions réversibles uniquement (contrainte section 7 CDC) |
| Fuite de secret dans les livrables | Sanitisation automatique en fin de chaîne + scan 0 motif (ENF-03) |
| Dérive mock ≠ production | Même contrat OpenAPI pour mock et prod ; la batterie M7 s'exécute sur le contrat, pas sur une implémentation particulière |
