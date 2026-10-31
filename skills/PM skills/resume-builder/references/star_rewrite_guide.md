# Guide de réécriture STAR

## Principe fondamental

STAR = Situation (contexte) + Task (mission) + Action (action) + Result (résultat)

Mais **une puce de CV ne consiste pas à empiler les quatre blocs STAR** : elle condense le tout en une seule phrase qui contient implicitement les signaux STAR :

```
[verbe d'action] + [objet / périmètre] + [méthode / outils] + [résultat quantifié]
```

Exemples :

❌ Faible : a participé au développement du système XX
✅ Fort : a piloté la conception et la mise en production du module de stockage du système de commandes XX, introduit des verrous distribués Redis pour éliminer les surventes, encaissé 800 000 commandes quotidiennes, réduit la latence P99 de 320 ms à 95 ms

❌ Faible : en charge des opérations d'événements promotionnels
✅ Fort : conçu la campagne « retour des clients fidèles 618 », couvrant 300 000 utilisateurs dormants, via push segmenté + combinaison de bons d'achat, taux de retour 11,4 % (référence 4,2 %), ROI 3,8

## Processus de réécriture

1. **Repérer le maillon faible STAR de la puce d'origine**
   - Pas de verbe d'action ? En ajouter un
   - Pas de résultat quantifié ? Interroger l'utilisateur
   - Action trop vague (« participé / assisté / appuyé / soutenu ») ? Remplacer par un verbe d'action concret
   - Pas de méthode / outil ? En ajouter

2. **Appliquer la bibliothèque de verbes** (voir ci-dessous)

3. **Quantifier** (chiffres / pourcentages / classements / délais / échelle, au choix)

4. **Maîtriser la longueur** : une puce ≤ 2 lignes

## Bibliothèque de verbes d'action forts (par fonction)

### Général
piloter, être responsable de, faire aboutir, initier, concevoir, construire, optimiser, faire le retour d'expérience, incubé, boucler

### Produit / opérations
planifier, itérer, étudier, définir (fonctionnalité), déploiement progressif, tests A/B, attribution data, mettre en ligne, roll back

### Technique
refactorer, concevoir l'architecture, régler finement, découpler, abstraire, modulariser, automatiser, superviser, plan de secours, dégradation gracieuse

### Data
modéliser, nettoyer, attribuer, visualiser, régresser, partitionner, ingénierie des caractéristiques, entraîner, mettre en production

### Ventes / business development
ouvrir des comptes, signer, renouveler, encaisser, négocier, gérer l'entonnoir, segmenter la clientèle

### Management
constituer (l'équipe), former, gérer la performance, décliner les objectifs, coordonner transversalement

## Table de remplacement des termes faibles

| Terme faible | Remplacement recommandé |
|------|---------|
| a participé à | a piloté / responsable du module ___ (préciser le périmètre) |
| a assisté | en collaboration avec ___, a réalisé ___ (préciser le partenaire et le résultat) |
| a appuyé | idem |
| a suivi | a fait aboutir / a piloté / drive |
| a aidé | via ___, a permis à ___ d'atteindre ___ |
| a appris | maîtrise et applique ___ pour réaliser ___ |
| a été exposé à | supprimer, ou transformer en projet concret |
| connaît / a connaissance de | supprimer le terme abstrait, citer le projet concret |

## Bibliothèque d'indices de quantification

Si l'utilisateur ne peut vraiment produire de chiffre, utiliser ces « quantifications souples » en guise d'appoint, marquées `[à compléter]` :

- Échelle utilisateurs / clients : dizaine de milliers / million / dizaine de millions
- Taille d'équipe : 3 personnes / 10 personnes / transverse
- Durée du projet : 2 semaines / 1 trimestre / 6 mois
- Impact métier : cœur de métier / critique / pilote
- Comparaison sectorielle : première du secteur / première de l'entreprise / client Tier 1

## Auto-contrôle : pour chaque puce, se demander

- Commence-t-elle par un verbe ?
- Contient-elle au moins 1 chiffre / un ordre de grandeur ?
- Si on la supprime, que perd le CV ? Si la réponse est « rien », la supprimer
- Quelle compétence concrète cette puce fait-elle venir à l'esprit du RH ?
