# 3.1 Points d'entrée d'édition et détermination de la version — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 3.1 Points d'entrée d'édition et détermination de la version » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : 4e6435236ca92f2f33c861139982780d8b3c40bd2e70f97212bfdb0d35cd2792**

### 3.1 Points d'entrée d'édition et détermination de la version

| Point d'entrée d'édition | Projet | Version |
|---------|------|------|
| Édition par commentaire (instruction écrite sur l'élément sélectionné dans la zone d'aperçu) | l'instruction MD contient le nom du projet | l'instruction MD contient le numéro de version (celui de l'aperçu) |
| Éditeur de paramètres (bouton d'édition de la zone d'aperçu) | l'instruction MD contient le nom du projet | l'instruction MD contient le numéro de version (celui de l'aperçu) |
| Langage naturel (saisie dans la boîte de dialogue) | voir les règles ci-dessous | voir les règles ci-dessous |
| Carte du flux de conversation « Éditer à partir de cette version » | projet correspondant à la carte | version correspondant à la carte (passe par le flux de fusion §4) |

**Défaut en langage naturel : éditer la dernière version du projet le plus récent.**

Détermination du projet : selon les priorités du §2 (nom désigné par l'utilisateur > contexte front-end > dernière opération > question posée).

Détermination de la version :

| Scénario | Traitement |
|------|----------|
| L'utilisateur désigne explicitement une version (ex. « à partir de V2, modifier le titre », ou boîte de saisie préremplie « Éditer à partir de la version V2 de « {nom-projet} » ») | suivre la version désignée → flux de fusion §4 |
| L'utilisateur désigne un projet sans désigner de version | dernière version de ce projet |
| Autres cas | par défaut : dernière version du projet le plus récent |

Pas de question supplémentaire. Toutes les versions sont restaurables ; une édition par mégarde d'une version non prévue se corrige par une restauration.

#### Règles de traitement des éditions par commentaire et par l'éditeur de paramètres

Après une édition par commentaire ou par l'éditeur de paramètres dans la zone d'aperçu (y compris l'aperçu d'une version historique), le front-end génère une instruction MD envoyée à l'Agent. L'instruction MD contient le **nom du projet** et le **numéro de version** ; l'Agent applique les règles suivantes :

1. Extraire le nom du projet de l'instruction MD → localiser `mes-projets/{nom-projet}/`
2. Extraire le numéro de version de l'instruction MD → obtenir `V{n}`
3. Lire le `latest_version` du `meta.json` du projet et déterminer la relation entre versions :
   - **Version désignée = dernière version** → éditer directement dans le workspace courant → créer une nouvelle version selon §3.3
   - **Version désignée ≠ dernière version (version historique)** → **obligation** d'exécuter le flux de fusion §4.4 (restaurer d'abord la version désignée avec `git checkout v{n} -- .`, puis appliquer l'édition, enfin un seul commit en nouvelle version). **Interdit de sauter l'étape de restauration** ; aussi minime que l'Agent estime l'écart entre la version courante et la version cible, il doit restaurer strictement avant de modifier.
4. Rechercher les correspondances par ancres dans tous les fichiers HTML du répertoire projet, localiser l'élément cible et appliquer la modification
5. Une fois terminé : créer la version avec les commandes git du §3.3 / §4.4 + mettre à jour `meta.json` + `send_file`

> **Le template MD est maintenu par le front-end.** Ce Skill ne définit pas le format MD précis ; il suffit qu'il contienne le nom du projet, le numéro de version, les ancres et les modifications pour être parsable par l'Agent.
