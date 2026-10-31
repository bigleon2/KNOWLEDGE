# Modèle de CV technique / R&D / data

## Structure

```
Nom｜Téléphone｜E-mail｜GitHub｜Ville｜Poste visé

【Résumé / Summary】(facultatif, 1~2 lignes)
X ans d'expérience en ___, spécialisé ___ (back-end forte concurrence / système de recommandation / applications LLM / ...), maîtrise de la stack ___

【Compétences】(en tête pour les postes techniques, pour que le RH voie d'un coup d'œil si la stack correspond)
- Langages : Java (expert), Python (avancé), Go (notions)
- Back-end : Spring Boot, Spring Cloud, gRPC, Kafka, Redis, MySQL, ClickHouse
- Big data / algorithmes : Spark, Flink, Hive, PyTorch (si poste algorithme)
- Ingénierie : Docker, Kubernetes, Linux, Git, CI/CD
- Autres : TypeScript, AWS

【Expérience professionnelle】
Entreprise A | Niveau (ingénieur senior / ingénieur expert / Tech Lead) | Période
- Résultats au niveau système (avec chiffres : QPS, latence, disponibilité, échelle)
- Contributions d'architecture / conception (ce que vous avez conçu, pourquoi ce choix)
- Impact métier (quel résultat métier vous avez fait avancer)

【Projets】
Nom du projet | Rôle | Stack | Période
- Contexte : échelle métier / point de douleur (une phrase)
- Solution : votre conception centrale + décisions techniques clés (expliquer le pourquoi)
- Résultat : chiffres de performance / stabilité / coût

【Formation】

【Open source / publications / compétitions】(fort bonus)
- Projets GitHub (nombre d'étoiles / contributeur principal)
- Publications (préciser conférence / revue)
- Compétitions (Kaggle / ACM / Tianchi / hackathons, avec classement)
```

## Points de style

- **Peu d'adjectifs, beaucoup de chiffres + détails techniques**
  - Faible : « optimisé les performances du système »
  - Fort : « en introduisant un cache secondaire + réécriture SQL, fait passer le P99 de l'API fiche produit de 480 ms à 110 ms »
- **Distinguer clairement « ce que vous avez fait » de « ce que l'équipe a fait »** : utiliser « piloté » / « responsable de » pour délimiter le périmètre de responsabilité
- Poste algorithme : dans la liste de compétences, **mettre en avant les modèles / versions de frameworks précis** (éviter l'empilement de buzzwords)
- Poste LLM / Agent : préciser explicitement la part « entraînement / fine-tuning / inférence / application » qui est la vôtre, pour ne pas passer pour un profil prompt-only
- Longueur : 1~2 pages

## Pièges fréquents

- Écrire « expert » dans le CV et rester muet à la question en entretien → si la maîtrise est incertaine, écrire « avancé / notions »
- Lister 20+ compétences sans profondeur sur aucune → réduire à 8~12 réellement maîtrisées
- Présenter un travail de cours comme une expérience projet → l'étiqueter « projet de cours (Course Project) », ne pas le déguiser en projet industriel
- Description de projet limitée à « ce qu'est ___ », sans « ce que j'ai fait » → réécrire
