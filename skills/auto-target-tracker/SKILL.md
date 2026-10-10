---
name: auto-target-tracker
version: "1.0.0"
category: "Autres"
tags:
  - auto
  - target
  - tracker
description: Traceur automatique de progression des objectifs. Lorsqu'une image liée à un objectif (notes, progression, captures d'écran, journaux) est détectée dans la conversation, appelle automatiquement le VLM pour en identifier les informations clés et les consigner dans le journal d'objectifs. S'applique à tous les scénarios de gestion d'objectifs : suivi d'apprentissage, fitness, avancement professionnel, habitudes, journal créatif, etc.
language: fr

read_when:
  - Déclencher quand la demande concerne : traceur automatique de progression des objectifs
  - Déclencher si la demande mentionne : objectifs, progression, journal
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Traceur automatique de progression des objectifs

## Conditions de déclenchement

Se déclenche automatiquement lorsque les conditions suivantes apparaissent dans la conversation :

1. **L'utilisateur envoie une image** (notamment notes d'étude, captures d'écran de progression, relevés de fitness, listes de tâches, réalisations créatives, etc.).
2. **L'utilisateur envoie une image pendant la plage horaire d'objectif définie** (par exemple 08:30, 10:00, 20:00).
3. **L'utilisateur le demande explicitement** : « note-le pour moi », « regarde ma progression », « je fais mon point », « mise à jour », etc.

---

## Workflow

### 1. Détecter l'image

Quand une image est détectée, vérifier :
- Le nom du fichier image contient-il des mots-clés d'objectif (progress, goal, task, workout, note, etc.) ?
- Le contenu de l'image contient-il des éléments d'objectif (barre de progression, texte, code, graphique, planning, etc.) ?
- Sommes-nous à proximité d'une heure de rappel d'objectif planifiée ?
- Le contexte récent de la conversation porte-t-il sur l'exécution d'un objectif ?

### 2. Appeler le VLM pour l'identification

Utiliser l'outil vlm pour analyser l'image :

**Template de prompt générique** :
```
"Identifie les informations clés de l'image et extrais, selon le type d'objectif, les éléments suivants :
- Tâche/contenu central
- Progression ou quantité réalisée
- Données clés (temps, poids, nombre de mots, etc.)
- Un bref retour sur l'exécution"
```

**Prompts dédiés par type d'objectif** :

| Type d'objectif | Prompt |
|---------|--------|
| Étude | "Identifie les notes d'étude, extrais les points de connaissances et le degré d'avancement" |
| Fitness | "Identifie le relevé de fitness, extrais le type d'exercice, les séries, les répétitions, la charge" |
| Travail | "Identifie la progression du travail, extrais les tâches réalisées et le taux d'achèvement" |
| Création | "Identifie la réalisation créative, extrais le type de création, la progression, les éléments clés" |
| Habitudes | "Identifie le relevé de pointage, extrais le contenu pointé et le nombre de jours consécutifs" |

### 3. Analyser les informations d'objectif

Extraire du résultat renvoyé par le VLM :
- **Liste des tâches/contenus** : les actions ou tâches concrètes identifiées
- **Degré d'achèvement** : estimation de la progression à partir du contenu de l'image
- **Données clés** : temps, quantité, charge, nombre de mots et autres indicateurs quantitatifs
- **Retour cognitif** : brève évaluation de l'état actuel de l'objectif

### 4. Consigner dans le journal d'objectifs

Appeler l'outil `edit_daily` pour enregistrer le résultat d'identification dans la note du jour.


### 5. Renvoyer un retour à l'utilisateur

Confirmer le résultat d'identification avec l'utilisateur :

```
Ton pointage d'objectif a été enregistré :

📝 Résultat d'identification :
Contenu central : tu as photographié la liste de vocabulaire anglais du jour, 15 nouveaux mots appris.
Estimation de progression : la tâche de vocabulaire du jour est bouclée, mieux que 80 % des apprenants.
Conseil : l'orthographe de deux mots est un peu floue, jette-y un second coup d'œil lors de la révision de demain.

L'enregistrement est-il correct ? Veux-tu que je l'ajoute au journal d'objectifs du jour ?
```

---

## Format d'enregistrement

### Exemple d'entrée du journal d'objectifs

```markdown
## 20:00 Relevé de pointage

**Type d'objectif**: 📚 Étude

**Image**: ![Image objectif](path/to/image.jpg)

**Résultat d'identification VLM**:

| Tâche/Contenu | Progression/Quantité | Statut |
|----------|----------|------|
| Vocabulaire anglais (Unit 1) | 15 mots | Terminé |
| Exercices de maths (chapitre 3) | 80% | En cours |

| **Total** | | **2/3 atteints aujourd'hui** |

**Données clés**:
- Temps d'étude : 2 heures
- Concentration : élevée

**Remarque**: Identification automatique, confirmée correcte par l'utilisateur

---

## 10:30 Pointage fitness

**Type d'objectif**: 🏃 Fitness

**Image**: ![Relevé fitness](path/to/gym.jpg)

**Résultat d'identification VLM**:

| Type d'exercice | Séries | Répétitions | Charge | Statut |
|---------|------|------|------|------|
| Développé couché | 4 | 12 | 60kg | ✅ Terminé |
| Squat | 4 | 10 | 80kg | ✅ Terminé |
| Tractions | 3 | 8 | Poids du corps | ⚠️ Une série manquante |

| **Total** | | | **Objectif du jour atteint** |

**Données clés**:
- Charge totale : 2640kg
- Durée de la séance : 45 minutes

**Remarque**: Une série de tractions en moins, à rattraper la prochaine fois
```

---

## Intégration avec le système d'objectifs

### Résumé quotidien

Le résumé de 22:00 chaque soir inclut :
- Tous les relevés de pointage du jour
- L'analyse du taux d'atteinte des objectifs
- La comparaison avec les objectifs (si des objectifs sont définis)

### Rapports hebdomadaires/mensuels

Le rapport hebdomadaire inclut :
- La durée d'exécution effective de la semaine
- Le périmètre des objectifs couverts
- Le nombre de jours de pointage consécutifs
- Les suggestions d'ajustement dynamique de la difficulté : si les objectifs sont atteints en continu, suggérer d'augmenter le volume de tâches de la semaine suivante

---

## Scénarios d'usage courants

### Scénario 1 : pointage d'étude

**Comportement utilisateur** : envoi d'une photo de notes manuscrites

**Identification automatique** :
- Extraction des points de connaissances
- Calcul de la progression d'apprentissage
- Enregistrement dans le journal d'étude

**Exemple de retour** :
```
📚 Notes d'étude identifiées :
- Algorithmes d'apprentissage supervisé (terminé)
- Optimiseur par descente de gradient (en cours)
- Régularisation anti-surapprentissage (non commencé)

Progression : 33 % | environ 2 heures restantes
```

### Scénario 2 : pointage fitness

**Comportement utilisateur** : envoi d'une photo de relevé de fitness

**Identification automatique** :
- Extraction du type d'exercice
- Comptage des séries, répétitions, charges
- Calcul du volume d'entraînement

**Exemple de retour** :
```
🏃 Relevé de fitness identifié :
- Développé couché 60kg × 12 × 4 séries ✅
- Squat 80kg × 10 × 4 séries ✅
- Tractions poids du corps × 8 × 3 séries ✅

Volume total : 2640kg | Durée : 45 minutes
```

### Scénario 3 : avancement professionnel

**Comportement utilisateur** : envoi d'une capture d'écran d'avancement de projet

**Identification automatique** :
- Extraction des tâches réalisées
- Calcul du pourcentage d'achèvement
- Identification des tâches restantes

**Exemple de retour** :
```
💼 Progression du travail identifiée :
- Cahier des charges (terminé) ✅
- Maquette (terminée) ✅
- Développement front (en cours) 🔄 80%
- Développement back (non commencé) ⏳

Avancement global du projet : 67 %
```

### Scénario 4 : pointage créatif

**Comportement utilisateur** : envoi d'une photo de réalisation créative

**Identification automatique** :
- Extraction du type de création
- Identification des éléments clés
- Estimation du degré d'achèvement

**Exemple de retour** :
```
🎨 Réalisation créative identifiée :
Type : illustration
Éléments : personnage, arrière-plan
Degré d'achèvement : line art 100 %, mise en couleur 60 %

Conseil : le line art du personnage est fini aujourd'hui, la mise en couleur de l'arrière-plan peut commencer demain
```

### Scénario 5 : pointage d'habitudes

**Comportement utilisateur** : envoi d'une capture d'écran du calendrier de pointage

**Identification automatique** :
- Extraction du nombre de jours consécutifs
- Identification du statut de pointage du jour
- Calcul du taux de pointage

**Exemple de retour** :
```
✅ Pointage d'habitudes identifié :
Lever tôt : 15 jours consécutifs | taux de pointage 100 %
Lecture : 8 jours consécutifs | taux de pointage 73 %
Sport : 21 jours consécutifs | taux de pointage 100 %

🎉 3 semaines de sport consécutives, continue comme ça !
```

---

## Périmètre

Ce skill fait UNIQUEMENT :
- Identifier les images liées aux objectifs et en extraire les informations clés
- Enregistrer les données de pointage dans les fichiers de notes du jour
- Fournir des retours de progression et des conseils

Ce skill ne fait JAMAIS :
- Exécuter automatiquement une action fondée sur le résultat d'identification
- Envoyer des images vers un service externe (hors API VLM)
- Accéder à des ressources images non autorisées par l'utilisateur
- Modifier le plan d'objectifs de l'utilisateur (enregistre uniquement la progression)

---

## Sécurité et confidentialité

**Données qui restent en local :**
- Le résultat structuré après identification
- Le contenu consigné dans les notes du jour ou la mémoire long terme et USER.md
- L'historique des données de pointage

**Ce skill ne fait PAS :**
- Partager la progression ou les données de pointage avec des tiers
- Publier automatiquement les pointages sur les réseaux sociaux
- Accéder aux autres ressources images de l'utilisateur

---

## Points d'attention

1. **Protection de la vie privée** : les images et les résultats d'identification sont stockés uniquement en local, sans envoi vers le cloud (hormis l'appel à l'API VLM pour l'identification)
2. **Exactitude** : le contenu identifié par le VLM n'est qu'indicatif ; des écarts sont possibles en raison d'une écriture floue, de la qualité de l'image, etc.
3. **Confirmation rapide** : il est recommandé à l'utilisateur de confirmer le résultat d'identification après enregistrement, et de le corriger manuellement en cas d'écart
4. **Type d'objectif** : le système détermine automatiquement le type d'objectif d'après le contenu de l'image ; ajustement manuel possible en cas d'erreur
5. **Estimation de progression** : le pourcentage de progression est estimé à partir de l'image et peut être imprécis ; une mise à jour manuelle régulière est conseillée

---

## Suggestions d'intégration

### En complément de SOUL.md

Intégrer le traceur automatique dans le workflow quotidien de gestion des objectifs :

```markdown
### 2. Enregistrement et estimation intelligents (Logging & Estimation)

- Quand l'utilisateur envoie une image liée à un objectif :
  1. Appeler automatiquement auto-target-tracker pour identifier le contenu
  2. Extraire les informations clés et estimer la progression
  3. Enregistrer immédiatement dans les notes du jour
  4. Synchroniser la progression des objectifs dans USER.md
```

### En complément de HEARTBEAT.md

Inclure dans les vérifications du heartbeat :

```markdown
## Résumé quotidien
- À 22:00, lecture automatique de tous les relevés de pointage du jour
- Génération du rapport de progression des objectifs
- Envoi à l'utilisateur
```
