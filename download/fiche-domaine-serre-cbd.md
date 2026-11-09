# Fiche domaine — Projet SERRE CBD (écoute acoustique de stress végétal)

> M5 ANALYSER — skill `cahier-des-charges` v2.0.1 (cycle Engineering Design complet)
> Session web-dd290b0d · 2026-10-25 · Sources compilées : 3 (dont 1 fondatrice) · **v1.2.0 — clôture J-M4 sans contenu Copilot** (v1.1.0 — consolidation S-C réelle, navigateur headless)

## 1. Sources compilées

| # | Source | Nature | Statut d'extraction |
|---|--------|--------|---------------------|
| S-A | **Science & Vie SV-238443** — « Les plantes crient quand elles sont en état de stress : pour la première fois, des chercheurs enregistrent les sons émis par les végétaux » (Auriane Polge, Science & Vie, publié le 05/07/26) | **Source d'inspiration fondatrice du projet** (directive propriétaire, répétée 3×) | Extraite intégralement (web-reader) — citations verbatim disponibles |
| S-B | **PDF « Résumé Global Des Références Serre CBD »** (propriétaire) | Référentiel technique consolidé du projet existant : architecture, modèles de données, API, services, Docker, CI/CD, sécurité, gouvernance | Extraite intégralement (pdftotext, 350 L) |
| S-C | Discussion chat.z.ai (s/aeec48ec) — « Serre CBD Automatisée » | Conversation d'origine du projet (10 messages, 5 paires) | **Extraite réellement (v1.1.0)** — navigateur headless agent-browser (rendu JS complet ; le lecteur web seul rendait 0 texte), transcript 22 598 octets archivé `upload/discussion-serre-cbd.md` ; la substitution par S-B (v1.0.0) est **levée** — S-C est désormais une source primaire tracée, dont les apports (A-1/A-2/A-3, §4) complètent sans contredire S-A/S-B |

## 2. Domaine technique détecté

**Domaine primaire : bioacoustique végétale (ingénierie du son appliquée à l'agronomie).**

Le cœur du système est la détection acoustique passive du stress des plantes dans la bande ultrasonore 40-80 kHz, fondée scientifiquement par l'étude Hadany & Yovel (université de Tel-Aviv, revue *Cell*) rapportée par la source fondatrice S-A. Les sons de stress y sont décrits comme des « craquements ou des bulles qui éclatent », de volume « 60 à 65 décibels, comparable à celui d'une conversation normale », détectables « jusqu'à cinq mètres de distance » (donnée Natural History Museum de Londres), avec une cadence discriminante : plante saine < 1 son/heure contre ≈ 35 clics/heure pour une tomate assoiffée ; deux protocoles de stress validés (privation d'eau 5 jours ; coupure de tige) ; mécanisme causal pressenti : **cavitation** — « formation et l'éclatement de bulles d'air dans le système vasculaire de la plante », hypothèse honnêtement non confirmée dans l'article (« rien ne prouve encore que ») — d'où l'hypothèse tracée [HYP-01].

**Domaines secondaires détectés (signaux lexicaux S-B) :**
1. **IoT / électronique embarquée** — signaux : « capteurs acoustiques », « sensor_id », « site_id », « sample_rate », « raw_audio_ref », chaîne « capteurs → acquisition → inférence → décision → orchestration → commandes PLC ».
2. **Informatique / ML d'inférence** — signaux : « inférence ML », « model_registry.json », « model_id », « confidence », « seuils utilisés », règles de décision chiffrées (n_peaks/mean_energy).
3. **Automatisation industrielle** — signaux : « commandes PLC », « PLCCommand », « target/action/parameters/duration_s/priority ».
4. **Génie logiciel & DevOps** — signaux : « OpenAPI », « JSON Schema », « Docker multi-stage », « Gunicorn », « GitLab CI », « Azure DevOps », « sanitisation », « SHA256 ».

**Espèces et contexte de culture** : serre de chanvre CBD (cadre réglementaire français/européen — variétés autorisées THC < 0,3 %) ; l'article S-A valide la généralité du phénomène sur tomate, tabac, maïs, blé, vigne et cactus — le chanvre n'y figure pas explicitement, d'où [HYP-02] (transposabilité de la signature acoustique).

## 4. Apports de la source S-C réelle (v1.1.0 — consolidation)

Le transcript extrait porte sur la gouvernance d'écosystème autour du projet, pas sur la technique du système lui-même — c'est précisément ce que S-A/S-B ne couvraient pas :

- **A-1 (apport contractuel)** : un **amendement M4 FAIRE ÉVOLUER du cahier des charges Serre CBD a été programmé en suspens** (« à réception du contenu Copilot », 2 occurrences au transcript, dont la suggestion ③ « fournir le contenu Copilot pour l'amendement M4 du CDC Serre CBD ») — le CDC documentait ce jalon d'évolution programmé (consigné §9 du CDC, jalon J-M4). **Clôture v1.2.0** : le contenu Copilot n'ayant pas été retrouvé par le propriétaire (directive du 2026-10-25), l'amendement est exécuté **sans ce contenu** — aucun apport contractuel à intégrer, aucune exigence EF/ENF ajoutée ou modifiée ; la promesse S-C reste tracée, jamais effacée.
- **A-2 (contrainte opérationnelle)** : le propriétaire exploite dans un **cadre de gouvernance discipliné** — worklog append-only, arbitres mécaniques rejoués (idempotence ×2), publication contrôlée au GO (règle d'or n°4 : jeton éphémère jamais persisté, audit anti-persistance), clone-chat de session, suggestion de republication des livrables vers `bigleon2/KNOWLEDGE` — cadre dans lequel les livrables Serre CBD s'inscrivent (consigné §7 du CDC).
- **A-3 (constat négatif, honnêteté R3)** : aucune exigence fonctionnelle système nouvelle (capteurs, seuils, PLC, API) n'émerge de S-C — la batterie de tests M7 reste valide telle quelle ; re-validation par re-run ×2 uniquement.

Profil SE : inchangé (**standard**). Hypothèses [HYP-01..05] : inchangées (A-3). Annexe D du CDC alignée sur cette section.

## 5. Normes et références techniques identifiées (recherche web, sonde unique)

- **[S1] ISO 9613-2** — « Acoustique — Atténuation du son lors de sa propagation en extérieur — Partie 2 : méthode d'ingénierie » : modèle d'atténuation (divergence géométrique Adiv, absorption atmosphérique Aatm fortement dépendante de la fréquence et de l'humidité, effet de sol Agr, écrans Abar) — directement mobilisable pour modéliser la propagation des clics 40-80 kHz dans l'air humide d'une serre et justifier la portée de détection cible (5 m).
- **[S2] IEC 61260** — filtres de bande de fraction d'octave (bande étroite ultrasonore 40-80 kHz : filtrage passe-bande normalisé avant détection de pics).
- **[S3] IEC 60529 (indices IP)** — protection des micros ultrasoniques en environnement de serre (humidité élevée, brumisation, condensation).
- Contexte d'architecture IoT de serre confirmé par la recherche (surveillance multi-capteurs temps réel, alertes) — cohérent avec l'architecture S-B.

## 4. Hypothèses tracées

| ID | Hypothèse | Fondement | Impact si invalidée |
|----|-----------|-----------|---------------------|
| [HYP-01] | Les clics 40-80 kHz sont causés par la cavitation du xylème | S-A (hypothèse des auteurs, non confirmée) | Faible pour le CDC : le système détecte le *corrélat* acoustique, pas le mécanisme causal |
| [HYP-02] | La signature acoustique établie sur tomate/tabac/maïs/blé/vigne/cactus se transpose au chanvre CBD | S-A espèces validées ≠ chanvre ; même mécanisme vasculaire pressenti | Moyenne : recalibrage des seuils sur données terrain chanvre (batterie M7 = contrat) |
| [HYP-03] | La portée effective ≤ 5 m par capteur est atteignable dans une serre (réflexions structurales, humidité) | S-A (NHM Londres) + [S1] absorption atmosphérique défavorable aux ultra-sons dans l'air humide | Haute : densité de capteurs ×2-3, coût |
| [HYP-04] | La discrimination sain/stress léger/stress sévère est fiable avec les seuls traits n_peaks et mean_energy (fenêtres d'acquisition) | S-B règles de décision existantes (8/20 pics ; 0,0005/0,001 énergie) | Moyenne : enrichissement des traits (median_freq, peak_list_summary) |
| [HYP-05] | L'action PLC déclenchée (irrigation/ventilation) résorbe le stress avant perte de rendement | S-B (chaîne décision → commandes) ; cadence 35 clics/h vs < 1/h | Faible pour la détection, moyenne pour l'ROI |

## 5. Doutes et zones d'ombre

- La valeur « ≈ 35 clics/h » de S-A concerne la tomate en stress hydrique ; l'extrapolation de seuils numériques au chanvre est une supposition (traitée par [HYP-02] et les critères mécaniques EF-03, recalibrables par configuration).
- S-A précise que « rien ne prouve encore que » la cavitation soit la cause — le CDC formule donc ses exigences sur le signal observable, jamais sur le mécanisme.
- Les seuils S-B (n_peaks ≥ 8/20, mean_energy 0,0005/0,001) ne précisent ni la durée de la fenêtre d'acquisition ni la bande de filtrage effective — exigences ENF/EF rédigées avec valeurs de contrat, modifiables en M4 FAIRE ÉVOLUER.

## 6. Calibration System Engineering

**Profil : STANDARD** — justification : multi-domaine (4 secteurs secondaires) mais périmètre borné (une serre, chaîne unique déjà prototypée S-B) ; contraintes de sûreté faibles (pas de risque humain direct — actions PLC d'irrigation/ventilation réversibles) ; contraintes réglementaires modérées (culture CBD légale, données sans caractère personnel) ; intensité de simulation moyenne (2 TH matériels simulés : capteur acoustique virtuel + propagation atténuée). Ni MINI (multi-domaine + contrat de tests exigé par le propriétaire), ni COMPLEXE (pas de sûreté critique, pas d'interopérabilité multi-sites imposée).
