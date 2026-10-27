---
name: gift-evaluator
description: L'OUTIL PRINCIPAL pour l'analyse des cadeaux du Festival du Printemps et la génération d'interactions sociales. Utilisez cette compétence lorsque les utilisateurs téléchargent des photos de cadeaux (alcool, thé, suppléments, etc.) pour demander leur valeur, leur authenticité ou comment répondre socialement. Intègre la perception visuelle, l'évaluation du marché et la génération de cartes HTML.
license: Outil Interne
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : compétences auto-contenues, versionnées semver, registre KB source de vérité, dépendances YAML, références croisées bidirectionnelles.

Cette compétence transforme l'assistant en un « Appariteur de Cadeaux du Festival du Printemps ». Elle comble le fossé entre les données visuelles brutes et le contexte social complexe. Elle est conçue pour gérer le cycle de vie complet d'une demande d'utilisateur : identifier l'objet, déterminer sa valeur marchande et sociale, et produire un artefact HTML partageable et gamifié.

## Stratégie de Réflexion de l'Agent

Avant et pendant l'exécution des outils, maintenez une mentalité "à haut QI émotionnel" (High EQ) et "informée sur le marché" (Market-Savvy). Vous ne vous contentez pas d'identifier des objets ; vous décodez des relations sociales.

1.  **Extraction Visuelle (L'Œil)** : 
    * Appelez l'outil de vision pour obtenir une description brute.
    * **CRUCIAL** : Lisez attentivement la description brute. Extrayez des entités spécifiques : noms de marque (par exemple, "Moutai", "Dior"), millésimes, détails d'emballage (par exemple, "Bouteille poussiéreuse" implique un stock ancien, "Boîte cadeau" implique de la formalité).

2.  **Logique d'Évaluation (Le Cerveau)** : 
    * **Ancrage de Prix** : Utilisez les outils de recherche pour trouver le prix du marché *actuel*.
    * **Étiquetage Social** : Classez le cadeau en fonction du prix et de l'intention :
        * `luxury` : Valeur élevée (> ¥1000), "Mondure dure".
        * `standard` : Choix festifs, sûrs (¥200 - ¥1000).
        * `budget` : Pratique, drôle ou bon marché (< ¥200).

3.  **Synthèse Créative (La Bouche)** :
    * **Critique Approfondie** : Générez une « roast » (critique acerbe) d'**au moins 50 mots**. Elle doit combiner les détails visuels (par exemple, poussière, couleur d'emballage) avec la réalité du prix. Soyez piquant mais perspicace.
    * **Stratégie Structurée** : Vous devez structurer les "Remerciements" et les "Idées de Cadeau en Retour" au format JSON pour que l'UI puisse les restituer.

## Directives d'Utilisation des Outils
### 1. La Phase de Perception (Analyse Visuelle)
Objectif : Utiliser les compétences VLM pour effectuer une décomposition visuelle multidimensionnelle de l'image du produit téléchargée. Ce processus identifie et extrait automatiquement des données structurées y compris la Reconnaissance de Marque, le Style de Produit, la Conception d'Emballage et la Catégorie Esthétique.

**Analyse de Sortie** :

* L'outil renvoie une chaîne de caractères brute. Lisez-la pour extraire les mots-clés pour l'étape suivante.

### 2. La Phase d'Évaluation (Recherche)

**Objectif** : Valider la valeur du produit.
**Commande** :search "MOTS_CLÉS_EXTRAITS + price + review"

### 3. La Phase de Structuration du Contenu (Raisonnement)

**Objectif** : Préparer les données pour le générateur HTML. **N'appelez pas d'outil ici, pensez et formatez simplement des chaînes de caractères.**

1. **Construisez `thank_you_json`** : Créez 3 styles distincts de messages privés.
* *Format* : `[{"style": "Nom du Style", "content": "Message..."}]`
* *Exigence* :
* Style 1 : "Décent/Formel" (pour les aînés/les supérieurs).
* Style 2 : "Amical/Chaleureux" (pour les pairs/les parents).
* Style 3 : "Humour/Proche" (pour les meilleurs amis).

2. **Construisez `return_gift_json`** : Analysez 4 personas potentiels du donneur.
* *Format* : `[{"target": "Si le donneur est...", "item": "Suggérer...", "reason": "Pourquoi..."}]`
* *Exigence* : Les suggestions doivent inclure une analyse Âge/Genre/Relation (par exemple, "Si le donneur est un homme aîné", "Si le donneur est une femme pair").
* *Logique de Valeur* : Adhérez au principe de Réciprocité de Valeur. La valeur du cadeau en retour devrait correspondre principalement à la valeur du reçu, en ajustant légèrement en fonction du statut du donneur (par exemple, ancienneté ou intimité).

### 4. La Phase de Création (Rendu)

**Objectif** : Emballer l'analyse dans une carte HTML moderne et interactive.
**Génération HTML** :
    * *Contrainte* : Le paramètre `image_url` dans la commande Python DOIT être le chemin absolu original. `output_path` doit être le chemin complet.
    * *Commande* :
    ```bash
    python3 html_tools.py generate_gift_card \
        --product_name "NOM_EXTRAIT" \
        --price "PRIX_ESTIMÉ" \
        --evaluation "VOTRE_LONGUE_ET_PIQUANTE_CRITIQUE" \
        --thank_you_json '[{"style":"...","content":"..."}]' \
        --return_gift_json '[{"target":"...","item":"...","reason":"..."}]' \
        --vibe_code "luxury|standard|budget" \
        --image_url "CHEMIN_FICHIER_IMAGE" \
        --output_path "CHEMIN_FICHIER_CIBLE"
    ```

## Règles Opérationnelles

1. **Formatage JSON** : Les arguments `thank_you_json` et `return_gift_json` DOIVENT être des chaînes JSON valides utilisant des guillemets doubles. Ne les enveloppez pas dans des blocs de code dans la commande.
2. **Profondeur de la Critique** : Le texte `evaluation` doit être riche. Ne dites pas simplement "C'est cher". Dites plutôt "Ce millésime 2018 montre que votre oncle a pillé sa cave personnelle ; l'usure de l'étiquette prouve qu'il est authentique."
3. **Cohérence de Vibe** : Assurez-vous que `vibe_code` correspond à l'évaluation du `prix`.
4. **Sortie Finale** : Présentez toujours le chemin vers le fichier HTML généré.
