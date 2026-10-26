# Banque de questions techniques

Applicable : aux 1ère et 2ème entrevues (tours techniques) pour les postes R&D / Algorithme / Données / DevOps.

Organisé par niveau de compétence :
- **Débutant (0-3 ans)** : fondamentaux de base + algorithmes simples + détails du projet
- **Intermédiaire (3-5 ans)** : conception de systèmes + questions de scénarios complexes + approfondissement du projet
- **Avancé (5+ ans)** : compromis architecturaux + problèmes inter-équipes + compréhension métier

## I. Backend / Serveur

### Fondamentaux de base (posés par chaque entreprise)
1. Flux HTTP / HTTPS / TLS, session vs cookie vs token
2. Les trois poignées de main et quatre fermetures de TCP, pourquoi quatre fermetures
3. Fondamentaux des index MySQL (arbre B+), quand ils deviennent inefficaces, préfixe le plus à gauche
4. Niveaux d'isolation des transactions MySQL + problèmes que chacun résout
5. Persistance de Redis (RDB / AOF) + réplication maître-esclave + sentinel + cluster
6. Comment résoudre la panne de cache / la perforation de cache / l'effondrement de cache Redis
7. Trois implémentations de verrouillage distribué (Redis / Zookeeper / base de données) + leurs pièges respectifs
8. Comment Kafka garantit que les messages ne sont ni perdus, ni dupliqués, et ordonnés
9. Modèle mémoire JVM + GC (poste Java) / Ordonnancement Goroutine (poste Go)
10. Bref aperçu du hachage de consistence, CAP, BASE, Raft / Paxos

### Questions fréquentes de conception de systèmes
- Concevoir un système de vente flash (10k QPS)
- Concevoir un service de raccourcissement d'URL (génération / redirection / statistiques)
- Concevoir un générateur d'ID distribués
- Concevoir un flux de fil de Weibo (push / pull / push-pull combiné)
- Concevoir un limiteur de débit (seau de jetons / seufre d'écoulement / fenêtre glissante)

### Cadre de réponse pour la conception de systèmes
```
1. Clarifier les besoins (demander QPS, ratio lecture/écriture, volume de données, SLA)
2. Estimer la capacité (QPS × taille moyenne de requête = bande passante ; volume de données × temps = stockage)
3. Architecture de haut niveau (couche d'accès → couche métier → couche de stockage → flux de données)
4. Exploration approfondie des modules clés (expliquer pourquoi le choix a été fait)
5. Extensibilité / haute disponibilité / récupération de catastrophe
6. Mentionner activement les compromis (trade-offs)
```

## II. Frontend

1. Processus de rendu du navigateur (DNS → TCP → TLS → HTTP → analyse HTML → mise en page → dessin)
2. Boucle d'événements + micro-tâches / macro-tâches
3. Fermetures, chaîne de prototypes, liaison this
4. Principes de réactivité React / Vue
5. Optimisation des performances (indicateurs FCP / LCP / CLS + mise en pratique)
6. SSR vs CSR vs SSG, quand les utiliser
7. Solutions de cross-domain (CORS / JSONP / proxy inverse)
8. Différences webpack / vite + principes

## III. Algorithmes / Machine Learning

### Fondamentaux
1. Biais / variance, comment résoudre le surajustement
2. Différence entre régularisation L1 / L2
3. Forêt aléatoire vs GBDT vs XGBoost
4. Disparition / explosion de gradient + solutions (BatchNorm / résidus / fonctions d'activation)
5. Expliquer le mécanisme d'Attention, comparaison Transformer vs RNN
6. Gestion des déséquilibres d'échantillons (échantillonnage / poids de classe / Focal Loss)
7. Évaluation de modèle : précision, precision, rappel, AUC, F1, quand les utiliser

### Direction LLM / GenAI (tendu en 2024+)
1. SFT vs RLHF vs DPO, principes + quand les utiliser
2. Pipeline complet RAG : stratégie de segmentation, choix d'Embedding, fusion de recherche, Reranker
3. Utilisation d'outil / planification / mémoire d'Agent, différence avec un LLM unique
4. Long contexte (mise à l'échelle YARN / RoPE, extension de la fenêtre de contexte)
5. Optimisation d'inférence : cache KV, décodage spéculatif, quantification
6. Évaluation de grands modèles : benchmarks, évaluation humaine, pièges respectifs de LLM-as-Judge

### Approfondissement de projet (chaque intervieweur le demande obligatoirement)
- Pourquoi avez-vous choisi ___ plutôt que ___ pour ce modèle
- Les données ont-elles été étiquetées / nettoyées, quel volume
- Quels matériels ont été utilisés pour l'entraînement, combien de temps, comment les hyperparamètres ont été ajustés
- Comment l'efficacité a-t-elle été évaluée après la mise en ligne, comparaison avec la ligne de base
- Cas d'échec / bug, comment les debuguer

## IV. Données / Entrepôt de données / Analyse

### SQL (obligatoire)
- Ligne à colonne / colonne à ligne / tableau croisé dynamique
- Fonctions de fenêtre (rank / dense_rank / lead / lag)
- Calcul des utilisateurs actifs sur 7 jours / 30 jours
- Nombre de jours de connexion consécutifs pour le même utilisateur
- Taux de rétention / entonnoir / analyse de cohorte
- Optimisation des performances (index, explain, partitionnement, éviter les sous-requêtes)

### Questions métier
- Vous donnez un scénario métier, vous devez concevoir un système d'indicateurs
- DAU a baissé de 5%, comment investiguer
- Concevoir un A/B test (calcul de taille d'échantillon, signification, arrêt des pertes)
- Modèle de segmentation utilisateur (RFM / cycle de vie)

## V. Principes de réponse aux questions techniques

1. **Clarifier avant de répondre** : pour les questions floues, poser d'abord 1-2 questions de clarification
2. **Sortie structurée** : expliquer par points / modules, pas en flux de conscience
3. **Pensée des compromis** : quand on choisit A plutôt que B, dire activement "parce que ___"
4. **Honnêteté** : pour les questions qu'on ne connaît pas, dire "je n'ai pas étudié cela, mais selon ma compréhension de X, on pourrait penser ___"
5. **Dessiner / écrire du code** : pour les exercices au tableau, expliquer d'abord l'approche, puis écrire, et enfin exécuter des cas de test
