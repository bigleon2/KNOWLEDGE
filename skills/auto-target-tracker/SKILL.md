---
name: auto-target-tracker
description: Traqueur automatique de progression des objectifs. Quand la conversation contient des images liées à un objectif (notes, progrès, captures, journaux), il appelle automatiquement le VLM pour reconnaître les informations clés et les consigner dans le journal d'objectif. Convient à tous les scénarios de gestion d'objectif : gestion des études, suivi sportif, avancement professionnel, installation d'habitudes, journal de création.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Traqueur automatique de progression des objectifs

## Conditions de déclenchement

Se déclenche automatiquement quand la conversation présente l'une des conditions suivantes :

1. **L'utilisateur envoie une image** (notamment notes d'étude, captures de progression, relevés sportifs, listes de tâches, travaux de création, etc.).
2. **L'utilisateur envoie une image dans un créneau horaire d'objectif défini** (ex. 08:30, 10:00, 20:00).
3. **L'utilisateur le demande explicitement** : « note ça pour moi », « regarde où j'en suis », « pointage », « mets à jour », etc.

---

## Workflow

### 1. Détecter l'image

À la détection d'une image, vérifier :
- si le nom de fichier contient des mots-clés d'objectif (progress, goal, task, workout, note, etc.)
- si le contenu de l'image comporte des éléments d'objectif (barres de progression, texte, code, graphiques, plannings, etc.)
- si l'on est proche d'un créneau de rappel d'objectif
- si le contexte récent de la conversation porte sur l'exécution de l'objectif

### 2. Appeler le VLM pour la reconnaissance

Utiliser l'outil vlm pour analyser l'image :

**Gabarit de prompt générique** :
```
« Reconnaître les informations clés de l'image et, selon le type d'objectif, en extraire :
- la tâche/le contenu principal
- la progression ou les quantités accomplies
- les données clés (durée, charge, nombre de mots, etc.)
- puis fournir un bref retour d'exécution »
```

**Prompts dédiés par type d'objectif** :

| Type d'objectif | Prompt |
|---------|--------|
| Étude | « Reconnaître des notes d'étude, extraire les points de savoir et le taux d'achèvement » |
| Sport | « Reconnaître un relevé d'entraînement, extraire le type d'exercice, les séries, les répétitions, la charge » |
| Travail | « Reconnaître une progression de travail, extraire les tâches accomplies et le taux d'achèvement » |
| Création | « Reconnaître un travail de création, extraire le type, l'avancement et les éléments clés » |
| Habitude | « Reconnaître un journal de pointage, extraire le contenu pointé et le nombre de jours consécutifs » |

### 3. Analyser les informations de l'objectif

Extraire du retour du VLM :
- **la liste des tâches/contenus** : actions ou tâches précises reconnues
- **le taux d'achèvement** : estimation de progression fondée sur le contenu de l'image
- **les données clés** : indicateurs quantifiés — durée, quantités, charges, nombre de mots…
- **le retour cognitif** : bref commentaire sur l'état courant de l'objectif

### 4. Consigner dans le journal d'objectif

Appeler l'outil `edit_daily` pour enregistrer le résultat de la reconnaissance dans la note quotidienne du jour


### 5. Retour à l'utilisateur

Faire confirmer le résultat de la reconnaissance à l'utilisateur :

```
Votre pointage d'objectif est enregistré :

📝 Résultat de la reconnaissance :
Contenu principal : la photo montre votre tableau de vocabulaire anglais du jour, 15 nouveaux mots appris.
Estimation de progression : la tâche de vocabulaire du jour est bouclée, vous faites mieux que 80 % des étudiants.
Conseil : l'orthographe de deux mots reste floue, repassez-y demain en révision.

L'enregistrement est-il exact ? Veux-tu que je le conserve dans le journal d'objectif du jour ?
```

---

## Format d'enregistrement

### Exemple d'entrée de journal d'objectif

```markdown
## 20:00 Pointage

**Type d'objectif** : 📚 Étude

**Image** : ![image d'objectif](path/to/image.jpg)

**Résultat VLM** :

| Tâche/contenu | Progression/quantité | Statut |
|----------|----------|------|
| Vocabulaire anglais (Unité 1) | 15 mots | accompli |
| Exercices de maths (chap. 3) | 80 % | en cours |

| **Total** | | **2/3 atteints aujourd'hui** |

**Données clés** :
- Durée d'étude : 2 heures
- Concentration : haute

**Note** : reconnaissance automatique, validée par l'utilisateur

---

## 10:30 Pointage sport

**Type d'objectif** : 🏃 Sport

**Image** : ![relevé d'entraînement](path/to/gym.jpg)

**Résultat VLM** :

| Exercice | Séries | Répétitions | Charge | Statut |
|---------|------|------|------|------|
| Développé couché | 4 | 12 | 60 kg | ✅ fait |
| Squat | 4 | 10 | 80 kg | ✅ fait |
| Tractions | 3 | 8 | poids du corps | ⚠️ une série en moins |

| **Total** | | | **objectif du jour atteint** |

**Données clés** :
- Charge totale : 2640 kg
- Durée d'entraînement : 45 minutes

**Note** : une série de tractions manquante, à rattraper la prochaine fois
```

---

## Intégration au système d'objectifs

### Récapitulatif quotidien

Dans le récapitulatif de 22:00 chaque soir, inclure :
- tous les pointages du jour
- l'analyse du taux d'atteinte des objectifs
- la comparaison aux cibles (si des cibles sont définies)

### Rapports hebdomadaires/mensuels

Dans le rapport hebdomadaire, inclure :
- la durée effective d'exécution de la semaine
- la couverture des objectifs
- le nombre de jours de pointage consécutifs
- des suggestions d'ajustement de difficulté : en cas de réussite consécutive, proposer d'augmenter la charge de la semaine suivante

---

## Scénarios d'usage courants

### Scénario 1 : pointage d'étude

**Comportement utilisateur** : envoi d'une photo de notes manuscrites

**Reconnaissance automatique** :
- extraction des points de savoir
- calcul de la progression d'étude
- enregistrement dans le journal d'étude

**Exemple de retour** :
```
📚 Notes d'étude reconnues :
- algorithmes supervisés du machine learning (accompli)
- optimiseurs à descente de gradient (en cours)
- régularisation contre le surapprentissage (non commencé)

Progression : 33 % | environ 2 heures restantes
```

### Scénario 2 : pointage sport

**Comportement utilisateur** : envoi d'une photo de relevé d'entraînement

**Reconnaissance automatique** :
- extraction du type d'exercice
- comptage des séries, répétitions, charges
- calcul du volume d'entraînement

**Exemple de retour** :
```
🏃 Relevé d'entraînement reconnu :
- Développé couché 60 kg × 12 × 4 séries ✅
- Squat 80 kg × 10 × 4 séries ✅
- Tractions poids du corps × 8 × 3 séries ✅

Volume total : 2640 kg | Durée : 45 minutes
```

### Scénario 3 : progression de travail

**Comportement utilisateur** : envoi d'une capture d'avancement de projet

**Reconnaissance automatique** :
- extraction des tâches accomplies
- calcul du pourcentage d'achèvement
- identification des tâches restantes

**Exemple de retour** :
```
💼 Avancement de travail reconnu :
- cahier des besoins (accompli) ✅
- conception des maquettes (accompli) ✅
- développement front-end (en cours) 🔄 80 %
- développement back-end (non commencé) ⏳

Progression globale du projet : 67 %
```

### Scénario 4 : pointage de création

**Comportement utilisateur** : envoi d'une photo d'un travail de création

**Reconnaissance automatique** :
- extraction du type de création
- identification des éléments clés
- estimation du taux d'achèvement

**Exemple de retour** :
```
🎨 Journal de création reconnu :
Type : illustration
Éléments : personnages, arrière-plans
Avancement : crayonné 100 %, colorisation 60 %

Conseil : le crayonné des personnages est terminé aujourd'hui, la colorisation des décors peut commencer demain
```

### Scénario 5 : pointage d'habitude

**Comportement utilisateur** : envoi d'une capture du calendrier de pointage

**Reconnaissance automatique** :
- extraction du nombre de jours consécutifs
- identification du statut du jour
- calcul du taux de pointage

**Exemple de retour** :
```
✅ Pointage d'habitude reconnu :
Lever tôt : 15 jours consécutifs | taux 100 %
Lecture : 8 jours consécutifs | taux 73 %
Sport : 21 jours consécutifs | taux 100 %

🎉 Sport pointé sans interruption depuis 3 semaines, continuez !
```

---

## Scope

This skill ONLY:
- reconnaît les images liées aux objectifs et en extrait les informations clés
- enregistre les données de pointage dans les fichiers de notes quotidiennes
- fournit retours et conseils sur la progression

This skill NEVER:
- n'exécute automatiquement aucune action fondée sur la reconnaissance
- ne téléverse pas les images vers des services externes (hors API VLM)
- n'accède pas aux images non autorisées par l'utilisateur
- ne modifie pas le plan d'objectif de l'utilisateur (enregistrement de la progression seulement)

---

## Security & Privacy

**Data that stays local:**
- les résultats structurés de la reconnaissance
- les contenus consignés dans les notes quotidiennes ou la mémoire longue et USER.md
- l'historique des pointages

**This skill does NOT:**
- partager la progression des objectifs ou les données de pointage avec des tiers
- publier automatiquement les pointages sur les réseaux sociaux
- accéder aux autres ressources d'images de l'utilisateur

---

## Points d'attention

1. **Protection de la vie privée** : les images et résultats de reconnaissance restent stockés localement, aucun téléversement cloud (hors appel de l'API VLM pour la reconnaissance)
2. **Exactitude** : les contenus reconnus par le VLM sont indicatifs ; des écarts sont possibles selon l'écriture ou la qualité de l'image
3. **Confirmation rapide** : inviter l'utilisateur à confirmer sans tarder le résultat et à corriger manuellement en cas d'écart
4. **Reconnaissance du type d'objectif** : le système déduit le type d'objectif du contenu de l'image ; ajustement manuel possible en cas d'erreur
5. **Estimation de progression** : les pourcentages sont estimés depuis l'image et peuvent être imprécis ; une mise à jour manuelle régulière est conseillée

---

## Suggestions d'intégration

### Avec SOUL.md

Intégrer le traqueur automatique au workflow quotidien de gestion des objectifs :

```markdown
### 2. Enregistrement et estimation intelligents (Logging & Estimation)

- Quand l'utilisateur envoie une image liée à un objectif :
  1. appeler automatiquement auto-target-tracker pour reconnaître le contenu
  2. extraire les informations clés et estimer la progression
  3. consigner immédiatement dans la note quotidienne
  4. mettre à jour en synchronisation la progression de l'objectif dans USER.md
```

### Avec HEARTBEAT.md

Inclure dans le contrôle de pulsation :

```markdown
## Récapitulatif quotidien
- 22:00 lecture automatique de tous les pointages du jour
- génération du rapport de progression des objectifs
- envoi à l'utilisateur
```
