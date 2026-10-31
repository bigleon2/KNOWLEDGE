# Spécial entretien technique / R&D / data

Les questions généralistes d'algorithmique et de conception de systèmes sont dans `technical.md` ; ce fichier se concentre sur :
- les techniques d'approfondissement de projet
- les questions spécifiques aux postes algorithme / LLM / data
- les questions d'équipe / soft skills (à préparer aussi pour les postes techniques)

## Approfondissement de projet (systématique, partout)

Les intervieweurs adorent « creuser jusqu'au fond » — s'y préparer obligatoirement.

Pour chaque projet, savoir répondre au minimum à ces 8 questions :

1. **Contexte** — pourquoi ce projet ? quel problème métier ?
2. **Votre rôle** — quel était votre rôle dans l'équipe ? quels modules ___ avez-vous réalisés ?
3. **Choix techniques** — pourquoi X plutôt que Y ? quel était l'arbitrage ?
4. **Défis** — le problème technique le plus difficile rencontré ? comment résolu ?
5. **Données** — quels QPS / volume de données / latence / disponibilité ?
6. **Résultats** — quels effets après mise en production ? amélioration de ___ par rapport à la référence ?
7. **Échecs / pièges** — quels pièges rencontrés ? comment débuggé ? comment évités ensuite ?
8. **Améliorations** — si vous refaisiez ce projet aujourd'hui, que changeriez-vous ?

## Spécifique postes algorithme / machine learning

### Questions de compréhension métier
1. Avec un métier ___, comment formuleriez-vous un problème de ML
2. Comment travaillez-vous avec le métier / le produit / la data
3. Le modèle en production sous-performe, comment menez-vous l'investigation
4. Modèle vs règles, quand choisir quoi
5. Avez-vous déjà mis à la retraite / remplacé un de vos modèles ? pourquoi

### Questions révélatrices des « faux projets LLM sans profondeur »
- Vous dites maîtriser le RLHF : comment le terme KL du PPO est-il introduit ? pourquoi ainsi ?
- Vous avez fait du RAG : comment calculez-vous la précision du rappel ? avez-vous comparé les stratégies de découpage ?
- Vous dites avoir fait un Agent : votre module de planification est-il en ReAct / CoT / sur mesure ? comment gérez-vous la récupération d'erreur ?

Parade : **ne décrire que des projets réellement menés** — les projets LLM inventés sont les plus faciles à démasquer.

## Spécifique postes data / entrepôt de données / analyse

### Questions métier (très fréquentes)
1. Comment mesurez-vous la santé d'un métier ___
2. La DAU chute de 5 %, comment diagnostiquez-vous
3. Le projet d'analyse de données le plus valorisant que vous ayez mené
4. Comment communiquez-vous vos conclusions au métier / produit / direction
5. On vous donne une demande : « analyser pourquoi les utilisateurs partent », comment procédez-vous

### SQL sur le vif (incontournable)
- Écrire une requête SQL : jours de connexion consécutifs par utilisateur
- Écrire une requête SQL : taux de rachat par article
- Écrire une requête SQL : nouveaux utilisateurs de chaque jour sur les 7 derniers jours
- Écrire une requête SQL : comparaison des résultats d'un test A/B + significativité

Astuce : **en live, toujours écrire le SQL en expliquant sa démarche à voix haute**, jamais en silence.

### Modélisation d'entrepôt de données
- Comment concevoir le modèle de données d'un métier ___
- Modélisation dimensionnelle vs modélisation normalisée : comment choisir
- Listes à fermeture éclair / dimensions à évolution lente : comment les traiter
- Comment garantir la qualité des données (supervision / contrôle / analyse post-mortem)

## Soft skills (à préparer aussi côté technique)

Croire qu'un entretien technique ne teste que la technique = grosse erreur. À partir du niveau intermédiaire :

1. Désaccord avec une autre équipe / un PM / un designer, que faites-vous
2. Comment revoyez-vous le code / les documents des autres
3. Comment formez-vous les nouveaux arrivants
4. Une décision technique reste sans réponse, comment la faites-vous avancer
5. Vous héritez d'un code « champ de ruines », comment le retapez-vous
6. Comment gérez-vous votre progression technique

## Questions inverses (entretien technique / entretien manager)

Entretien technique :
- Quelle est la stack technique de l'équipe et ses évolutions prévues ?
- Quels sont les défis techniques récents de l'équipe ?
- Quelles sont les pratiques de code review / astreinte / réunion hebdomadaire ?

Entretien manager :
- Que pensez-vous de l'avenir de la technologie / de la direction métier ___ ?
- Comment se porte la dette technique de l'équipe ?
- Quel est le défi le plus stimulant au sein de cette équipe, selon vous ?
