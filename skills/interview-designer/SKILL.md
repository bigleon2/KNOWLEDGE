---
name: interview-designer
version: "1.0.0"
category: "Visualisation & Design"
tags:
  - interview
  - designer
description: Analyse des CV et conception de stratégies d'entretien selon une méthodologie fondée sur les preuves. Transforme la préparation d'entretien « lire le CV → poser des questions » en « définir un standard → investigation médico-légale → simulation du futur ». Combine le Topgrading de Geoff Smart, le recrutement basé sur la performance de Lou Adler et le contrôle des biais de Daniel Kahneman. À utiliser pour préparer des entretiens, créer des guides d'entretien structurés ou concevoir des questions de validation des compétences des candidats.
language: fr

---

# Skill Interview Designer

> **Mission centrale** : élever la planification des entretiens de « jeter un œil au CV et poser des questions » à « investigation fondée sur les preuves et projection ».
> **Mécanisme opératoire** : définir la grille d'évaluation (fixer les standards) → balayage médico-légal (collecte de preuves) → simulation du futur (prédiction de la performance).
> **Stratégie de prompt** : ce skill utilise \<Chain of Thought\>. Pendant l'exécution, conservez une perspective d'« évaluateur objectif », recherchant à la fois les signaux rouges et les signaux verts.

## 1. Salle de guerre dynamique (panel d'experts)

Invoquer dynamiquement dans la salle de guerre les **meilleurs esprits** correspondant le mieux aux **attributs du poste du candidat** :

*   **Geoff Smart (Qui)** : responsable de **Définir & Vérifier**.
    *   *Principe* : la grille d'évaluation d'abord. Avant de regarder un CV, clarifier ce qu'est un « A Player » pour ce poste.
*   **Lou Adler (basé sur la performance)** : responsable de **Prédire**.
    *   *Principe* : la performance passée ne prédit la performance future *que si* le contexte est similaire. Il faut concevoir des simulations de scénarios futurs.
*   **Daniel Kahneman (contrôle des biais)** : responsable de **Dé-biaiser**.
    *   *Principe* : se méfier du « biais de confirmation ». Si des préoccupations apparaissent, chercher aussi des contre-preuves ; si des points forts apparaissent, vérifier leur reproductibilité.
*   **Expert du domaine** : responsable de la **Profondeur**.

## 2. Workflow d'exécution central

### Étape 1 : définition de la grille d'évaluation - *priorité de Smart*
**Ne regardez pas le CV d'abord !** À partir de la fiche de poste (JD) ou des exigences du rôle, définir les standards « A Player » pour ce poste :
*   **Mission** : une phrase — pourquoi ce poste existe-t-il ?
*   **Résultats** : 3 à 5 résultats spécifiques et mesurables à atteindre en 12 mois.
*   **Compétences** : compétences techniques/comportementales requises pour atteindre les résultats ci-dessus.

### Étape 2 : balayage médico-légal du CV - *forensic de Smart*
Utiliser les standards de l'étape 1 pour balayer le CV, en cherchant les **Écarts (incohérences)** et les **Points hauts (atouts)** :
*   **L'heuristique « Trop beau pour être vrai »** : les trous logiques derrière des données parfaites.
*   **L'heuristique « Passager vs Pilote »** : la contribution réelle de la personne sous l'effet d'aube d'une grande entreprise.
*   **L'heuristique « Premiers principes »** : la compréhension des principes derrière le jargon technique.

### Étape 3 : test de pression et simulation du futur - *prédiction d'Adler*
Concevoir deux types de questions :
1.  **Scripts de test de pression (sur le passé)** : concevoir des relances STAR médico-légales ciblant les préoccupations de l'étape 2 (à l'origine « questions torpilles », mais plus objectives).
2.  **Simulation du futur (sur l'avenir)** : concevoir un Problème de Performance concret.
    *   *Exemple* : « Nous entrons sur ce nouveau marché l'année prochaine, et le plus grand obstacle est X. Si vous nous rejoignez, comment analyseriez-vous ce problème lors de votre première semaine ? »

## 3. Principes de conception des questions

1.  **Ne peut pas être appris par cœur** : forcer le candidat à réfléchir sur le moment (simulation) ou à se remémorer des souvenirs douloureux (test de pression).
2.  **Arbitrages forcés** : choisir entre deux options « correctes » pour tester les valeurs.
3.  **Granularité des détails** : il doit être possible de descendre jusqu'à « quel schéma avez-vous dessiné » ou « quels mots exacts avez-vous dits ».

## 4. Format de sortie

Appeler directement `templates/interview_guide_template.md` pour générer le rapport.
**Remarque** : lors de la génération du guide, inclure à la fois **[Signaux rouges] (préoccupations)** et **[Signaux verts] (vérification des atouts)** pour préserver l'objectivité de l'évaluation.
