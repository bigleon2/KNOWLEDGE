# Domaines techniques — grille de détection automatique (M5 ANALYSER)

> Compatibilité : skill `cahier-des-charges` v2.0.0 → v2.0.1 (reconnaissance discipline + tags — contenu de cette référence inchangé, R2).


> Skill cahier-des-charges v2.0.0 — reference de détection. Objectif : que la détection du
> domaine ne soit ni une supposition ni un choix arbitraire, mais la convergence mesurée de
> signaux lexicaux tirés DU PROJET, immédiatement suivie de l'instruction du domaine par
> recherche web. Le détecteur court sur les informations compilées (lien lu, fichiers, discussion)
> — jamais sur la seule intuition.

## §1 — Méthode de détection (5 étapes)

1. **Extraire le lexique du projet** : noms, verbes, unités, chiffres, composants cités dans les
   sources compilées (le texte du lien, les fichiers, la discussion). Un signal = un fragment
   lexique qui appartient à un domaine bien précis (ex : « asservir », « couple », « encoder » →
   mécatronique).
2. **Scorer les domaines du catalogue (§2)** : chaque domaine calcule son nombre de signaux
   observés. Un signal compte une fois par occurrence de famille (pas par répétition du même mot).
3. **Retenir** : domaine PRIMAIRE = score ≥ 2 ET non contredit ; domaines SECONDAIRES = score ≥ 1
   ou effet de bord évident. En cas d'égalité, le domaine le plus spécifique l'emporte (ex :
   « ingénierie du son » > « logiciel » si le projet est un DSP).
4. **Tracer** : la fiche domaine liste, pour chaque domaine retenu, les signaux observés (cités)
   et les doutes `[HYP-xx]`. Une détection à un seul signal est explicitement fragile.
5. **Instruire** (immédiatement, même phase) : lancer les requêtes web types du domaine (§2,
   colonne « recherches web ») et compléter normes/méthodes/état de l'art — sources datées.

**Domaine mixte** : tout système réel croise plusieurs familles (une serre automatisée =
mécatronique primaire + agronomie + domotique). Le PRIMAIRE gouverne le vocabulaire, les normes
et la posture de rédaction ; les SECONDAIRES fournissent contraintes et glossaire additionnels.
Si aucun domaine du catalogue ne converge, déclarer un domaine AD HOC (nommé) et appliquer la
même discipline : signaux, recherche web, glossaire métier.

## §2 — Catalogue des domaines

| Domaine | Signaux lexicaux typiques | Recherches web types (à lancer en M5) | Normes/méthodes souvent impliquées | Patrons TH pertinents |
|---------|---------------------------|----------------------------------------|------------------------------------|------------------------|
| **Mécatronique / robotique** | asservir, moteur, servomoteur, couple, capteur, encodeur, PID, asservissement, articulation, pompe, vérin, trame, MCU, Arduino, Raspberry, step, DC, PWM, CNC, drone, bras | « norme sécurité machine <objet> », « dimensionnement moteur <charge> », « asservissement PID <processus> », « capteurs <mesure> précision » | EN/ISO 12100 (sécurité machines), IEC 60204, méthodes de dimensionnement (moteur, structure), state of the art des solutions analogues | modèle moteur+charge, PID, capteur bruité |
| **Domotique / IoT** | maison connectée, capteur de température, zigbee, mqtt, scène, automation, hub, wifi, batterie, station, serre, arrosage | « protocole domotique <x> », « norme radio <x> », « supervision <processus> », « consommation veille capteur » | RGPD selon données, EN 62443 (si industriel), standards radio | modèle thermique/ambiance, réseau retardé |
| **Électronique** | PCB, schéma, alimentation, régulateur de tension, ADC, bus, I2C, SPI, impédance, solder, firmware | « norme EMC <environnement> », « sélection composant <fonction> », « datasheet <composant> » | EN 61000 (CEM), IPC-A-610, règles de conception PCB | capteur bruité, alimentation avec chute |
| **Ingénierie du son / audio** | microphone, haut-parleur, DSP, échantillonnage, latence, gain, filtrage, acoustique, mixage, dB, SPL, fréquence | « taux d'échantillonnage <usage> », « norme SPL <contexte> », « chaîne de traitement audio <application> » | ITU-R BS.1116 (qualité audio), EN 61672 (sonométrie), pratiques DSP | modèle de chaîne d'échantillonnage, filtrage |
| **Prompt engineering / IA (LLM)** | prompt, LLM, modèle de langage, chatbot, RAG, fine-tuning, tokens, agent, embedding, contexte, system prompt | « best practices <tâche LLM> », « évaluation qualité LLM <tâche> », « architecture RAG <domaine> » | grilles d'évaluation LLM, conventions de specs d'agents, limites de contexte | harness d'évaluation de prompts (TF surtout) |
| **Logiciel (web / API)** | application web, API, base de données, frontend, backend, authentification, utilisateurs, dashboard, websocket | « architecture <type d'app> », « OWASP <usage> », « stack <besoin> comparaison » | OWASP ASVS, RGPD (données perso), WCAG (accessibilité) | harness de charge, simulation de latence |
| **Énergie / thermique** | panneau solaire, batterie, charge, rendement, watt, kWh, thermique, chauffage, isolation, dissipation | « dimensionnement <source> <charge> », « rendement <conversion> », « norme sécurité <équipement> » | EN 62368 (sécurité), règles de dimensionnement énergétique | modèle thermique 1er ordre, bilan de puissance |
| **Agronomie / bioprocédés** | culture, serre, hydroponie, substrat, pH, EC, photopériode, humidité, croissance, rendement | « conditions optimales <culture> », « paramètres <bioprocédé> », « capteurs <grandeur> agronomie » | bonnes pratiques culturales, référentiels agronomiques | modèle climatique de serre (thermique+humidité) |
| **Mécanique / CAO** | pièce, tolérance, matériau, contrainte, usinage, imprimante 3D, assemblage, couple de serrage | « matériau <usage> propriétés », « tolérance ISO <ajustement> », « norme <pièce> » | ISO 2768 (tolérances générales), ISO 286 (ajustements) | modèle statique charge/déformation allégé |
| **Vidéo / image** | caméra, détection, frame, résolution, fps, encodage, flux, traitement d'image | « capteur caméra <usage> », « latence pipeline vidéo », « détection <objet> état de l'art » | pratiques de pipeline temps réel | modèle de latence de pipeline |

> Catalogue NON EXHAUSTIF — un projet hors catalogue déclare un domaine AD HOC et suit la même
> discipline (signaux cités, recherche web datée, glossaire métier).

## §3 — Requête web : discipline de collecte

- 3 à 8 sources retenues par phase P1 ; chaque source porte : URL, date de consultation, ce
  qu'elle fonde (norme, méthode, chiffre, glossaire).
- Privilégier les sources primaires (normes, datasheets, référentiels) aux agrégateurs.
- Un chiffre repris d'une source dans le CDC (ex : seuil de latence, précision capteur) cite la
  source — un chiffre sans source est `[HYP-xx]`.
- Si la recherche web est indisponible (quota, réseau) : la fiche domaine marque les sections
  « à instruire en re-passsage M5 » et le CDC marque les normes attendues `[HYP-xx]` — la phase
  reste honnête, elle ne s'invente pas (R3).

## §4 — Anti-pièges de la détection

- **Faux ami lexique** : « capteur » dans un projet logiciel peut désigner une donnée d'entrée —
  vérifier la réalité matérielle avant de scorer mécatronique/électronique.
- **Domaine de la solution vs du système** : le projet peut être écrit avec le lexique de sa
  solution (ex : « application mobile ») alors que le SYSTÈME est domotique — scorer le système,
  trancher le primaire par la fonction du système (ce qu'il pilote), pas par son habillage.
- **Primaire par défaut trompeur** : « logiciel » n'est pas un primaire par défaut ; s'il ne
  s'agit que de l'emballage, remonter au domaine métier du système piloté.
- **Détection ≠ verdict** : la fiche domaine expose les signaux et les doutes — le propriétaire
  peut corriger en tout temps (sa correction relance M5 puis l'aval impacté).
