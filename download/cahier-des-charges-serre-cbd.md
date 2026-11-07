# Cahier des charges — SERRE CBD : système d'écoute acoustique du stress des plantes

> **Version du livrable : v1.2.0** (clôture J-M4 sans contenu Copilot) · v1.0.0 (M6 initial) → v1.1.0 (M4/M2 consolidation — S-C réelle) → v1.2.0 (M4 clôture J-M4 — historique en annexe H)
> **Domaine** : bioacoustique végétale (primaire) + IoT/électronique, ML d'inférence, automatisation PLC, DevOps (secondaires — détecté M5, résumé Annexe D) · **Profil SE** : standard (calibré M5)
> Référence fondatrice : Science & Vie SV-238443 (Hadany & Yovel, université de Tel-Aviv, revue *Cell*) — voir section 12 et Annexe D.

## 1. Contexte et problématique

Les plantes réagissent au stress depuis toujours — changement de couleur, d'odeur, de forme — mais une dimension est restée inexplorée jusqu'à la publication de l'étude de l'université de Tel-Aviv menée par Lilach Hadany et Yossi Yovel, rapportée par Science & Vie (SV-238443, source d'inspiration fondatrice de ce projet) : pour la première fois, des chercheurs ont **capté dans l'air les sons émis par des plantes en état de stress**. Des microphones ultrasoniques, posés à proximité de plants de tomate et de tabac sans y être fixés, ont enregistré des « craquements » ressemblant « à des bulles qui éclatent », situés **entre 40 et 80 kilohertz** — bien au-delà du seuil de perception humaine (16 kHz) — dont le volume atteint **60 à 65 décibels**, comparable à une conversation normale. Les plantes privées d'eau pendant cinq jours comme celles soumises à une coupure de tige émettent ces clics en quantité massive (≈ 35 clics/heure pour une tomate assoiffée contre moins de 1 son/heure pour une plante saine), et le phénomène a été confirmé sur le maïs, le blé, la vigne et le cactus. La cause exacte reste incertaine — l'hypothèse avancée est la **cavitation**, c'est-à-dire la formation et l'éclatement de bulles d'air dans le système vasculaire de la plante — mais quelle que soit sa cause, cette signature acoustique porte « une information précise, lisible par une machine » et « pourrait transformer la surveillance agricole ».

C'est précisément cette promesse que le présent projet industrialise pour une **serre de chanvre CBD**. Le propriétaire a déjà construit un premier référentiel technique complet (source S-B) : une chaîne fonctionnelle capteurs acoustiques → acquisition (fenêtres `AcqWindow`) → inférence ML → décision de stress → orchestration → commandes PLC, outillée d'un schéma de données typé (`AcqWindow`, `StressDecision`, `PLCCommand`), d'une API OpenAPI authentifiée, d'un serveur de simulation, de tests, d'une CI/CD GitLab et Azure, d'un Dockerfile de production et de scripts de packaging avec sanitisation des secrets. Le problème n'est donc plus la faisabilité : c'est la **formalisation contractuelle** de ce que le système doit faire, avec des critères d'acceptation mécaniquement vérifiables, pour permettre l'implémentation, la validation terrain et l'évolution maîtrisée. Ce cahier des charges transforme l'état d'art scientifique (S-A) et le référentiel existant (S-B) en un contrat d'ingénierie System Engineering calibré « standard ».

La problématique tient en trois défis. D'abord un défi de **détection** : discriminer un fond de bruit de serre (équipements, ventilation, météo, insectes) d'une signature ultrasonore faible et rare (35 clics/h contre 0) dans une bande 40-80 kHz fortement atténuée par l'air humide. Ensuite un défi de **décision** : convertir un flux de fenêtres acoustiques en une décision de stress fiable (sain / stress léger / stress sévère) dont les seuils sont recalibrables par espèce. Enfin un défi d'**action** : orchestrer des commandes PLC (irrigation, ventilation) opportunes, priorisées et réversibles, avec une traçabilité complète du signal à la commande.

## 2. Objectifs et indicateurs de succès

**Objectif général** — Produire un système d'écoute acoustique opérationnel pour serre de chanvre CBD qui détecte le stress hydrique et mécanique des plantes par leur émission ultrasonore et déclenche des actions correctrices automatiques via PLC, avec une traçabilité de bout en bout.

Cet objectif se décline en quatre sous-objectifs mesurables. **O-1 — Détection** : capturer et caractériser les clics ultrasonores 40-80 kHz émis par les plantes, avec une cadence discriminante conforme à l'étude fondatrice (plante saine < 1 son/h, plante en stress hydrique ≈ 35 clics/h chez la tomate). **O-2 — Décision** : classer chaque fenêtre d'acquisition en trois états (healthy / stress_light / stress_severe) selon des seuils explicites, versionnés dans un registre de modèles. **O-3 — Action** : transformer chaque décision en commandes PLC paramétrées (cible, action, durée, priorité) exécutées sans intervention humaine. **O-4 — Industrialisation** : maintenir un socle logiciel vérifié automatiquement (API contractuelle, tests, CI/CD, packaging avec sanitisation), héritant du référentiel S-B.

| Indicateur de succès | Cible mécanique | Vérifié par |
|---|---|---|
| Taux de clics détectés dans la bande 40-80 kHz | ≥ 95 % des clics injectés dans une simulation de capteur | TH-01 (batterie M7) |
| Portée de détection par capteur | ≥ 5 m sur signal 60-65 dB en air humide simulé | TH-02 |
| Décision d'inférence sur fenêtres bornes | 100 % de correspondance aux seuils contractuels (EF-03) | TF-01 |
| Validation des fenêtres AcqWindow entrantes | 100 % des schémas invalides rejetés (HTTP 4xx) | TF-02 |
| Conversion décision → commande PLC | 100 % des décisions mappées, priorité respectée | TF-03 |
| Authentification API | 100 % des requêtes sans `x-api-key` rejetées (401) | TF-04 |

Le succès du projet est déclaré atteint lorsque tous les tests de la batterie M7 passent mécaniquement (verdict `PASS`, code 0) et que la matrice de couverture ne recouvre aucune non-couverture non assumée. Les indicateurs sont conçus pour rester vérifiables sans matériel spécialisé : les performances acoustiques sont prouvées par simulation matérielle (capteur virtuel, propagation atténuée) plutôt que par campagne terrain, la validation terrain restant une étape recommandée hors périmètre de ce contrat (section 4).

## 3. Parties prenantes et rôles

**Le propriétaire du projet** est le commanditaire et le décideur : il a fourni les trois sources du projet (l'article Science & Vie fondateur, le référentiel technique PDF, la discussion d'origine — S-C réellement extraite en v1.1.0), a déjà produit une première implémentation de référence (mock server, module métier, CI/CD), et valide les évolutions du contrat en mode M4 FAIRE ÉVOLUER. Il est aussi l'exploitant cible du système dans sa serre de chanvre CBD, ce qui impose que les livrables restent exploitables sans équipe dédiée (scripts automatisés, rapport de vérifications, archives prêtes à déployer). Le transcript de S-C documente en outre le **cadre de gouvernance discipliné** dans lequel il opère — journal de travail append-only, arbitres mécaniques rejoués (idempotence ×2), publication contrôlée au GO (jetons d'accès éphémères, jamais persistés, audités après usage) — et le présent CDC s'inscrit dans ce cadre : ses statuts, chiffres et verdicts sont dérivés d'artefacts vérifiables sur disque, jamais pré-écrits (leçon anti-aspirante du cadre propriétaire).

**Le concepteur System Engineering** (rôle tenu par l'exécution du skill `cahier-des-charges`) produit et maintient ce cahier des charges, la fiche domaine, le dossier de conception (sous-systèmes, interfaces, allocation) et la batterie de tests M7. Il garantit la cohérence croisée exigences ↔ sous-systèmes ↔ interfaces ↔ tests, et doit prouver mécaniquement chaque affirmation vérifiable : aucun critère d'acceptation n'est admis sans sa vérification associée.

**Le développeur/implémenteur** (pouvant être le propriétaire lui-même) implémente ou complète les sous-systèmes SS-01 à SS-06 pour satisfaire aux exigences ; la batterie de tests M7 fait office de contrat d'implémentation : un code est réputé conforme lorsque tous les tests `PRÊT` passent. **Le modèle ML et ses versions** sont traités comme une partie prenante technique à part entière : tout modèle (`model_id`) porte ses seuils dans `model_registry.json`, et le système doit refuser une décision orpheline de registre. **Les partenaires externes** incluent : la communauté scientifique (étude Cell/Tel-Aviv comme fondement, à citer), les outils CI (GitLab, Azure DevOps), l'hébergement Docker, et le cadre réglementaire CBD (variétés autorisées) qui borne les usages. Enfin **les plantes elles-mêmes** — cliché apparent, mais utile : elles définissent la « source primaire du signal » et leurs variabilités (espèce, âge, humidité du substrat) figurent dans les facteurs de risque de la calibration.

## 4. Périmètre

**Est inclus dans le périmètre** : (a) l'acquisition acoustique ultrasonore en serre (capteurs 40-80 kHz, fenêtrage temporel `AcqWindow`, stockage de référence audio brute `raw_audio_ref`) ; (b) le traitement de signal minimal (comptage de pics `n_peaks`, énergie moyenne `mean_energy`, fréquence médiane `median_freq`, résumé de pics `peak_list_summary`) ; (c) l'inférence de décision à seuils (healthy / stress_light / stress_severe) et son registre de modèles ; (d) l'API d'ingestion et d'inférence (`POST /ingest/acqwindow`, `POST /ml/infer`) avec authentification par clé `x-api-key` ; (e) l'orchestration des commandes PLC (`PLCCommand` : cible, action, paramètres, durée, priorité) ; (f) le socle d'exploitation : conteneur Docker multi-stage non-root, endpoint `/health`, CI/CD GitLab et Azure, scripts de packaging avec génération SHA256/Base64 et sanitisation automatique des secrets ; (g) la documentation contractuelle (ce CDC, dossier de conception, batterie de tests, rapport de couverture).

**Est exclu du périmètre** : la validation terrain multi-saisons sur chanvre (recommandée en conclusion de S-B mais hors contrat, faute de serre instrumentée à disposition dans cette phase) ; l'entraînement de modèles ML supervisés (le contrat impose des seuils explicites et un registre, pas un apprentissage) ; la gestion des utilisateurs et des rôles applicatifs (une seule clé API en phase 1, la migration OAuth2/mTLS est une exigence d'évolution ENF-05) ; la facturation, la multi-tenance, les applications mobiles ; la modification du cadre réglementaire. Les évolutions de seuils par espèce sont admises **par configuration** (registre), jamais par modification du code d'inférence — c'est une frontière contractuelle explicite.

**Frontières physiques** : la zone de détection nominale est la serre unitaire (surface couverte par la densité de capteurs nécessaire à la portée cible de 5 m) ; les bâtiments voisins, l'extérieur et les autres serres sont hors de responsabilité de détection, même si le filtrage doit y être robuste aux sources ultrasonores parasites (chauves-souris et insectes perçoivent et émettent aussi dans ces bandes — constat de S-A intégré en risque).

## 5. Exigences fonctionnelles (EF)

Format : `EF-xx` — exigence atomique ; critère d'acceptation mécanique en gras ; traçabilité source [S-A]/[S-B]/[HYP-xx] ; sous-système d'allocation SS-xx (Annexe T, dossier de conception).

| ID | Exigence | Critère d'acceptation mécanique | Alloc. | Source |
|----|----------|--------------------------------|--------|--------|
| EF-01 | Le système acquiert des fenêtres acoustiques ultrasonores dans la bande 40-80 kHz et les matérialise en objets `AcqWindow` complets | Un `AcqWindow` produit contient **tous les champs obligatoires** (sensor_id, site_id, timestamp_start, timestamp_end, sample_rate, n_peaks, mean_energy, median_freq, peak_list_summary, env, meta, raw_audio_ref) — validation de schéma passée | SS-01/SS-02 | [S-B], [S-A] |
| EF-02 | Le filtrage passe-bande 40-80 kHz est appliqué avant détection de pics | Un sinus hors bande (ex. 20 kHz) injecté dans le détecteur produit **0 pic détecté** ; un train de clics 40-80 kHz produit n_peaks ≥ n_injectés − tolérance 5 % | SS-02 | [S-A], [S2] |
| EF-03 | L'inférence classe chaque `AcqWindow` en trois états selon des seuils explicites et versionnés | Pour tout couple (n_peaks, mean_energy) bornier : n_peaks ≥ 20 ou mean_energy > 0,001 → **stress_severe** ; n_peaks ≥ 8 ou mean_energy > 0,0005 → **stress_light** ; sinon → **healthy** — 100 % des cas de test TF-01 conformes | SS-03 | [S-B] |
| EF-04 | L'API expose `POST /ingest/acqwindow` et `POST /ml/infer` conformes au contrat OpenAPI | Toute charge utile violant le schéma renvoie **HTTP 4xx avec détail de violation** ; toute charge valide renvoie 2xx et est persistée/répondue conformément au contrat | SS-04 | [S-B] |
| EF-05 | Toute décision `StressDecision` est traçable (decision_id, model_id, seuils, horodatage, notes) | Chaque décision produite référence un `model_id` présent dans `model_registry.json` — **0 décision orpheline de registre** | SS-03 | [S-B] |
| EF-06 | Les décisions de stress sont converties en commandes PLC paramétrées | Chaque `StressDecision` non-healthy génère **exactement une** `PLCCommand` (target, action, parameters, duration_s, priority) ; stress_severe → priorité supérieure à stress_light — vérifié TF-03 | SS-05 | [S-B], [HYP-05] |
| EF-07 | Le système expose son état de santé opérationnel | Un appel à `/health` renvoie **2xx avec l'état des dépendances** (API, registre, horloge) en < 1 s | SS-06 | [S-B] |
| EF-08 | Le taux de clics par fenêtre est comparable à la cadence de référence de l'étude fondatrice | Sur simulation TH-01 (35 clics/h vs < 1 son/h) : le système **sépare les deux régimes** avec la marge contractuelle (≥ 95 % de détection, ≤ 1 faux positif/h sur régime sain) | SS-02/SS-03 | [S-A], [HYP-02] |

## 6. Exigences non-fonctionnelles (ENF)

| ID | Exigence | Critère d'acceptation mécanique | Alloc. | Source |
|----|----------|--------------------------------|--------|--------|
| ENF-01 | Performance : la latence bout-en-bout ingestion → décision reste exploitable pour l'automatisation | En simulation (mock), p95 de latence `POST /ml/infer` ≤ **500 ms** sur 100 requêtes séquentielles | SS-03/SS-04 | [S-B] |
| ENF-02 | Sécurité : toute route API est authentifiée | Toute requête sans en-tête `x-api-key` (ou clé invalide) renvoie **HTTP 401** — 0 route anonyme au scan | SS-04 | [S-B] |
| ENF-03 | Confidentialité : aucun secret ne fuit dans les livrables | Le scan de sanitisation sur l'archive finale renvoie **0 motif détecté** (clés API, Bearer, JWT, e-mails, clés AWS, access_token) | SS-06 | [S-B] |
| ENF-04 | Robustesse d'exploitation : le conteneur est durci | Image multi-stage, **utilisateur non-root**, HEALTHCHECK défini, `/health` câblé — vérifications Dockerfile mécaniques | SS-06 | [S-B] |
| ENF-05 | Évolutivité sécurité : migration OAuth2 ou mTLS documentée comme trajectoire | Le dossier de conception contient la **trajectoire de migration** (pré-requis, étapes, régression à surveiller) — revue documentaire | SS-04 | [S-B] |
| ENF-06 | Traçabilité CI/CD : chaque commit passe les vérifications contractuelles | Pipeline : validation OpenAPI, validation JSON Schema, lint Dockerfile, build image, tests d'intégration — **5 étapes présentes** dans les fichiers de pipeline | SS-06 | [S-B] |
| ENF-07 | Portabilité : la batterie de tests s'exécute sans matériel spécialisé | `run_all.py` passe (code 0) sur environnement Python standard ≥ 3.10, **0 dépendance matérielle**, graine fixée | Batterie M7 | [S-B] |
| ENF-08 | Éco-attention ultrasonore : le système n'émet pas d'onde active dans la bande 40-80 kHz à puissance de gêne | Le système est **purement passif** en écoute (0 émetteur actif) — revue d'architecture ; justification : chauves-souris et insectes perçoivent la bande (S-A) | SS-01 | [S-A] |

## 7. Contraintes

**Contraintes physiques et acoustiques.** Le signal utile vit dans une bande ultrasonore (40-80 kHz) où l'absorption atmosphérique est forte et croissante avec la fréquence, amplifiée par l'humidité élevée d'une serre ; la modélisation de propagation s'appuie sur les mécanismes normalisés de l'ISO 9613-2 [S1] (divergence géométrique, absorption atmosphérique, effets de sol et d'écrans), transposés à une bande au-delà de son domaine nominal — d'où l'hypothèse de portée [HYP-03] et le choix de simuler plutôt que de promettre. La serre introduit par ailleurs des réflexions sur structures (verre, polycarbonate) et un bruit de fond équipements (ventilation, pompes) que le filtrage passe-bande et la fenêtrage doivent absorber. Le système doit rester passif en écoute [ENF-08] : chauves-souris et insectes perçoivent la bande (S-A), et toute émission active serait à la fois une gêne écologique et une source d'auto-parasitage.

**Contraintes réglementaires et éthiques.** La culture porte sur du chanvre CBD, dont la légalité est conditionnée aux variétés autorisées (THC < 0,3 % en France) — le système n'intervient que sur le pilotage cultural et ne traite aucune donnée personnelle ; la sanitisation des secrets [ENF-03] et l'authentification [ENF-02] découlent aussi du bon référentiel de sécurité logicielle hérité de S-B. Aucune exigence de ce CDC ne doit pousser à une intervention sur la plante qui ne serait pas réversible (irrigation, ventilation oui ; traitement chimique hors périmètre).

**Contraintes techniques et opérationnelles.** L'implémentation cible un environnement Python standard (≥ 3.10) conteneurisé (Docker multi-stage, non-root), CI GitLab et Azure DevOps — le propriétaire opère seul, donc tout doit rester automatisable et auditable sans expertise dédiée. La batterie de tests doit s'exécuter sans matériel spécialisé [ENF-07] : les performances acoustiques sont prouvées par simulation matérielle (capteur virtuel, propagation), jamais alléguées. Enfin, contrainte de continuité : le projet existe déjà (S-B) — ce CDC n'invalide pas l'existant, il le contractualise ; les incompatibilités éventuelles entre l'existant et ce contrat sont des écarts à lever en M4 FAIRE ÉVOLUER, pas des réécritures tacites.

**Contrainte de gouvernance documentaire (S-C, v1.1.0).** Les livrables de ce projet s'inscrivent dans le flux discipliné documenté par la discussion d'origine (S-C) : toute exécution est journalisée (worklog append-only — l'historique n'est jamais réécrit, les corrections s'y apposent), tout verdict est dérivé de vérifications mécaniques rejouables (idempotence ×2) et toute publication externe (dépôt GitHub) est un geste contrôlé au GO explicite du propriétaire avec un jeton d'accès éphémère, jamais persisté, révoqué et audité après usage. Conséquences contractuelles : (a) les statuts et chiffres de ce CDC et de ses livrables annexes sont dérivés de l'état vérifiable sur disque, jamais pré-écrits ; (b) la traçabilité des secrets (clés API, jetons) est déjà couverte par [ENF-03] et s'étend aux jetons d'accès aux dépôts ; (c) toute republication des livrables Serre CBD vers le dépôt distant de référence suit le même protocole GO + jeton éphémère + audit anti-persistance.

## 8. Livrables attendus

| Livrable | Nature | Format | Statut dans ce cycle |
|----------|--------|--------|----------------------|
| L-1 Cahier des charges (ce document) | Contrat d'exigences | Markdown (+ PDF en M3 VALIDER) | Produit (M6) |
| L-2 Fiche domaine | Analyse M5 | Markdown | Produit |
| L-3 Dossier de conception | Sous-systèmes SS-01..SS-06, interfaces I-01..I-05, allocation | Markdown | Produit (M6) |
| L-4 Batterie de tests M7 | Tests TF/TH exécutables + harnais `run_all.py` + matrice de couverture | Dossier Python idempotent | Produit (M7) |
| L-5 Rapport de couverture exigences ↔ tests | Traçabilité de vérification, non-couvertures assumées | Markdown | Produit (M7) |
| L-6 Implémentation système (héritée S-B : mock_ml_infer.py, serre_logic.py, Dockerfile, CI/CD, scripts) | Code source | Projet Python/Docker | Hérité — à aligner sur le contrat |

Le livrable L-4 fait office de **contrat d'implémentation** : un code réputé conforme fait passer l'intégralité des tests `PRÊT`. L'archive finale du projet (ZIP + SHA256) est produite par les scripts S-B (create_and_package_serre.sh) après passage de la batterie — le rapport de vérifications automatiques (checks_report.sh) s'ajoute alors au dossier de validation.

## 9. Jalons et planning indicatif

| Jalon | Contenu | Critère de franchissement |
|-------|---------|---------------------------|
| J-1 Contrat figé | CDC + fiche domaine + dossier de conception produits et validés (M5→M6) | Arbitre de structure du skill PASS ; revue propriétaire |
| J-2 Contrat vérifiable | Batterie M7 complète, tous tests `PRÊT`, verdict `PASS` (M7) | `run_all.py` code 0 ×2 (idempotence) ; rapport de couverture sans non-couverture non assumée |
| J-3 Alignement de l'existant | serre_logic.py/mock server alignés sur EF-03/EF-04, Dockerfile aligné sur ENF-04 | TF-01..TF-03 branchés sur le code réel : PASS inchangé |
| J-4 Socle d'exploitation | CI/CD complète (ENF-06), packaging avec sanitisation (ENF-03) | Pipeline vert ; scan secrets 0 motif |
| J-M4 Amendement contractuel (S-C, v1.1.0) — **CLÔTURÉ (v1.2.0)** | Amendement M4 FAIRE ÉVOLUER programmé en v1.1.0 « à réception du contenu Copilot » (décision tracée dans la discussion d'origine S-C, suggestion ③) — le contenu Copilot **n'ayant pas été retrouvé** par le propriétaire (directive du 2026-10-25 : « fais sans le contenu de Copilot »), l'amendement est **exécuté SANS ce contenu** : aucun apport contractuel à intégrer, aucune exigence EF/ENF ajoutée ou modifiée, le contrat reste auto-suffisant | Décision propriétaire journalisée (worklog R5) ; clôture tracée au présent jalon et à l'annexe H (bump MINOR v1.2.0) ; batterie M7 re-validée PASS ×2 ; PDF ré-exporté v1.2.0 |
| J-5 (hors contrat, recommandé) | Validation terrain chanvre : campagne capteurs en serre réelle, recalibrage registre | Taux de détection terrain ≥ cible contractuelle ; mise à jour M4 |

Le planning est indicatif : la méthode impose l'ordre (contrat → vérification → implémentation), pas les dates. Chaque jalon se franchit mécaniquement, jamais par présomption — c'est l'esprit du protocole STATUT de la batterie (un test non implémenté reste `NON_IMPLÉMENTÉ` et bloque le verdict, aucune couverture alléguée n'est admise).

## 10. Critères d'acceptation

Le système est **accepté** lorsque l'ensemble des conditions suivantes est mécaniquement vérifié : (1) la batterie M7 rend verdict `PASS` avec code de sortie 0, deux fois de suite (idempotence) ; (2) chaque exigence EF-01..EF-08 et ENF-01..ENF-08 est soit couverte par au moins un test `PRÊT` et passant, soit explicitement portée à la matrice de couverture comme non-couverture assumée avec justification (jamais silencieuse) ; (3) les deux TH matériels simulés (capteur acoustique virtuel TH-01, propagation atténuée TH-02) passent avec leurs marges contractuelles (≥ 95 % de clics détectés ; séparation des régimes sain/stress ; portée 5 m en air humide simulé) ; (4) les vérifications d'exploitation (Dockerfile durci, sanitisation 0 motif, pipeline 5 étapes) sont prouvées par scripts ; (5) l'arbitre de structure du skill (`verifier_structure.py`) et le rapport de couverture sont joints au dossier de validation. L'acceptation est réputée échouée si un seul test `PRÊT` échoue ou si une non-couverture apparaît sans traçabilité — en ce cas, retour au jalon concerné, correction, re-exécution complète.

## 11. Glossaire

| Terme | Définition |
|-------|------------|
| **AcqWindow** | Fenêtre d'acquisition acoustique typée (schéma JSON S-B) : métadonnées capteur, bornes temporelles, traits de signal (n_peaks, mean_energy, median_freq), référence audio brute |
| **StressDecision** | Décision de stress produite par l'inférence : score, label (healthy/stress_light/stress_severe), confidence, model_id, action recommandée |
| **PLCCommand** | Commande vers l'automate : cible (target), action, paramètres, durée, priorité |
| **Cavitation** | Formation et éclatement de bulles d'air dans le système vasculaire (xylème) — hypothèse causale des clics ultrasonores [S-A, non confirmée] |
| **Clic ultrasonore** | Émission brève 40-80 kHz (~60-65 dB), corrélat acoustique du stress végétal [S-A] |
| **Fenêtre bornier** | Couple (n_peaks, mean_energy) exactement aux seuils — cas de test qui fixe le sens de l'inégalité contractuelle |
| **model_registry.json** | Registre des versions de modèles : model_id, version, seuils utilisés [S-B] |
| **Protocole STATUT** | Convention de la batterie M7 : un test non implémenté reste `NON_IMPLÉMENTÉ` et n'est pas exécuté tant qu'il n'est pas passé `PRÊT` — anti-couverture-alléguée |
| **TH / TF** | Test matériel simulé (TH) / test fonctionnel (TF) — batterie M7 |
| **Serre CBD** | Serre de culture de chanvre industriel à CBD (variétés autorisées THC < 0,3 %) |

## 12. Annexes et sources

1. **[S-A] SV-238443 — Science & Vie (source d'inspiration fondatrice)** : Auriane Polge, « Les plantes « crient » quand elles sont en état de stress : pour la première fois, des chercheurs enregistrent les sons émis par les végétaux », science-et-vie.com, publié le 05/07/26. Données structurantes : Hadany & Yovel (université de Tel-Aviv), revue *Cell* ; microphones ultrasoniques non fixés aux plantes ; clics 40-80 kHz ; 60-65 dB ; détectables ≤ 5 m (Natural History Museum de Londres) ; tomate assoiffée ≈ 35 clics/h vs plante saine < 1 son/h ; stress sécheresse (5 jours) et coupure de tige ; hypothèse de cavitation (non confirmée) ; généralisation maïs, blé, vigne, cactus ; perception de la bande par chauves-souris et insectes ; promesse de « surveillance acoustique des cultures grâce à un algorithme avancé ».
2. **[S-B] PDF « Résumé Global Des Références Serre CBD »** (propriétaire) : chaîne fonctionnelle capteurs → AcqWindow → inférence → décision → orchestration → PLC ; schémas AcqWindow/StressDecision/PLCCommand ; OpenAPI (POST /ingest/acqwindow, POST /ml/infer) ; ApiKeyAuth x-api-key (reco OAuth2/mTLS) ; mock_ml_infer.py (seuils 8/20 pics, 0,0005/0,001 énergie) ; serre_logic.py ; Docker multi-stage non-root Gunicorn /health ; tests unitaires et API ; GitLab CI + Azure DevOps ; scripts de packaging (ZIP, SHA256, Base64, sanitisation) ; model_registry.json.
3. **[S-C] Discussion chat.z.ai (s/aeec48ec) — « Serre CBD Automatisée »** (source d'origine du projet) : extraite intégralement en v1.1.0 par navigateur headless (rendu JS — 10 messages, 5 paires, 22 598 octets, transcript archivé `upload/discussion-serre-cbd.md`) après échec des voies d'extraction directes. Contenu : gouvernance d'écosystème autour du projet (clone de session, vérifications mécaniques, publication contrôlée). Apports contractuels : **A-1** — amendement M4 FAIRE ÉVOLUER du présent CDC « à réception du contenu Copilot » (→ jalon J-M4, section 9) — **clôturé en v1.2.0 sans ce contenu** (introuvable, décision propriétaire du 2026-10-25) ; **A-2** — cadre de gouvernance discipliné du propriétaire (→ section 7, contrainte de gouvernance documentaire) ; **A-3** — aucune exigence fonctionnelle système nouvelle (batterie M7 inchangée, re-validée par re-run ×2). La substitution par S-B opérée en v1.0.0 (S-C alors indisponible) est **levée**.
4. **[S1] ISO 9613-2** — Acoustique : atténuation du son lors de sa propagation en extérieur, Partie 2 (méthode d'ingénierie) — modèle d'atténuation mobilisé pour la portée.
5. **[S2] IEC 61260** — Filtres de bande de fraction d'octave (filtrage passe-bande normalisé).
6. **[S3] IEC 60529** — Degrés de protection (IP) — capteurs en environnement humide de serre.

## Annexe D — Fiche domaine (résumé) — cycle Engineering Design (M5)

Domaine primaire : **bioacoustique végétale** ; secondaires : IoT/électronique, ML d'inférence, automatisation PLC, DevOps. Signaux lexicaux porteurs : « capteurs acoustiques », « 40-80 kHz », « cavitation », « serre de chanvre CBD », « inférence ML », « commandes PLC », « OpenAPI », « sanitisation ». Sources : S-A fondatrice (Science & Vie — Hadany & Yovel, Cell), S-B référentiel technique, S-C discussion d'origine (extraite réellement v1.1.0 — apports A-1 amendement M4, clôturé v1.2.0 sans contenu Copilot, A-2 cadre de gouvernance, A-3 aucune exigence nouvelle). Normes tracées [S1] ISO 9613-2, [S2] IEC 61260, [S3] IEC 60529. Méthodes mobilisées : exigences atomiques à critères mécaniques, simulation matérielle (capteur virtuel, propagation), registre de modèles. Doutes : [HYP-01] cavitation non confirmée, [HYP-02] transposabilité au chanvre, [HYP-03] portée 5 m en air humide, [HYP-04] suffisance des traits n_peaks/mean_energy, [HYP-05] résorption du stress par action PLC. Profil SE : **standard**.

## Annexe T — Stratégie de vérification — cycle Engineering Design (M7)

**Lot TF (fonctionnel)** — TF-01 seuils d'inférence (EF-03, borniers inclus), TF-02 validation schéma + auth API (EF-04, ENF-02), TF-03 mapping décision → PLCCommand (EF-06), TF-04 intégrité AcqWindow (EF-01), TF-05 registre de modèles (EF-05), TF-06 santé opérationnelle (EF-07). **Lot TH (matériel simulé)** — TH-01 capteur acoustique virtuel (spectre 40-80 kHz, régimes 35 clics/h vs < 1/h, bruit/biais/quantification, graine fixe 42) pour EF-02/EF-08 ; TH-02 propagation ultrasonore atténuée (absorption atmosphérique dépendante de la fréquence et de l'humidité, mécanismes ISO 9613-2 [S1] transposés, portée cible 5 m) pour ENF-08/[HYP-03]. **Exigences visées non couvertes par tests exécutables** : ENF-05 (revue documentaire), ENF-08 (revue d'architecture) — non-couvertures assumées, consignées au rapport de couverture. **Critère de succès global** : `run_all.py` PASS ×2, 0 test `NON_IMPLÉMENTÉ` dans le lot visé, matrice sans cellule vide injustifiée. *v1.1.0 : exigences inchangées (S-C, A-3) — batterie re-validée par re-run ×2 (idempotence).*

## Annexe H — Historique des révisions (v1.2.0)

| Version | Date | Nature | Motif et provenance |
|---------|------|--------|---------------------|
| v1.0.0 | 2026-10-25 | Création (cycle M5→M7) | Test fonctionnel du skill cahier-des-charges v2.0.1 — sources S-A (fondatrice) + S-B ; S-C indisponible à l'extraction, substituée par S-B (adaptation tracée) |
| v1.1.0 | 2026-10-25 | Consolidation M4/M2 (bump MINOR — contenu contractuel enrichi, aucune exigence EF/ENF modifiée) | Directive propriétaire « exécute avec les 3 sources » — S-C réellement extraite (navigateur headless) ; substitution levée ; apports : amendement M4 en suspens (J-M4, §9), cadre de gouvernance (§7), S-C/Annexe D réécrites, présente annexe |
| v1.2.0 | 2026-10-25 | Clôture J-M4 (bump MINOR — jalon contractuel résolu, aucune exigence EF/ENF modifiée) | Directive propriétaire « fais sans le contenu de Copilot, je n'arrive pas à le retrouver » — amendement M4 exécuté SANS le contenu Copilot (introuvable) ; J-M4 clôturé (§9), A-1/Annexe D alignés ; batterie re-validée PASS ×2 ; PDF v1.2.0 exporté ; publication GitHub au GO (règle d'or n°4) |

