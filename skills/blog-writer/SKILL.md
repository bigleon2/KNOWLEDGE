---
name: blog-writer
version: "1.0.0"
category: "Contenu & Marketing"
tags:
  - blog
  - writer
description: Ce skill doit être utilisé pour rédiger des articles de blog, des billets ou tout contenu long dans le style d'écriture distinctif de l'auteur. Il produit un contenu authentique et engagé, fidèle à la voix de l'auteur — directe, conversationnelle et ancrée dans l'expérience personnelle. Le skill couvre le workflow complet, de la revue de la recherche jusqu'à la publication sur Notion. Utilisez ce skill pour rédiger des articles de blog, des pièces de réflexion (thought leadership) ou tout texte censé refléter le point de vue de l'auteur sur l'IA, la productivité, la vente, le marketing ou la technologie.
language: fr

---

# Blog Writer

## Vue d'ensemble

Ce skill permet de rédiger des articles de blog et des billets qui capturent de façon authentique la voix et le style distinctifs de l'auteur. Il s'appuie sur des exemples du travail publié de l'auteur pour produire un contenu direct, engagé, conversationnel et ancré dans l'expérience pratique. Le skill inclut une intégration Notion automatique et maintient une bibliothèque croissante d'exemples finalisés.

## Quand utiliser ce skill

Déclenchez ce skill quand :
- L'utilisateur demande la rédaction d'un article de blog ou d'un billet « dans mon style » ou « comme mes autres articles »
- Il s'agit de rédiger un contenu de réflexion (thought leadership) sur l'IA, la productivité, le marketing ou la technologie
- Il faut créer un article qui ait la voix et la perspective authentiques de l'auteur
- L'utilisateur fournit des documents de recherche, des liens ou des notes à intégrer à la rédaction

## Responsabilités principales

1. **Respecter le style d'écriture de l'auteur** : calquer la voix, le choix des mots, la structure et la longueur des exemples d'articles dans `references/blog-examples/`
2. **Intégrer la recherche** : relire et intégrer toute information, tout document de recherche ou lien fourni par l'utilisateur
3. **Suivre les instructions de l'utilisateur** : se conformer strictement aux demandes spécifiques de l'utilisateur concernant le sujet, l'angle et l'accent
4. **Produire une écriture authentique** : créer un contenu qui sonne comme la vraie voix de l'auteur, pas comme un texte générique généré par IA

## Workflow

### Phase 1 : rassembler les informations

Demander à l'utilisateur :
- Le sujet ou la thématique
- Tout angle ou thèse spécifique à développer
- Les documents de recherche, liens ou notes (s'il y en a)
- La longueur cible souhaitée (défaut : 800-1500 mots)

Relire attentivement tous les documents fournis avant de commencer à écrire.

### Phase 2 : rédiger le contenu

S'appuyer sur le guide de style `references/style-guide.md` et les exemples de `references/blog-examples/` pour l'étalonnage.

Pendant la rédaction :
1. Commencer par une phrase d'ouverture forte qui pose la thèse
2. Utiliser une voix personnelle et le « je » là où c'est naturel
3. Inclure, si pertinent, des anecdotes personnelles ou une expérience professionnelle
4. Structurer avec des sous-titres clairs (###) tous les 2-3 paragraphes
5. Garder des paragraphes courts (2-4 phrases)
6. Tisser les documents de recherche naturellement, pas en blocs de citations
7. Terminer par une réflexion, un appel à l'action ou une ouverture tournée vers l'avenir

### Phase 3 : relire et itérer

Présenter le brouillon et recueillir les retours. Itérer jusqu'à ce que l'utilisateur se déclare satisfait.

### Phase 4 : publier sur Notion (OBLIGATOIRE)

Quand le brouillon est complet (même s'il n'est pas encore finalisé), le publier dans la base TS Notes.

**Détails de publication Notion :**
- Base de données : « TS Notes » (data source ID : `04a872be-8bed-4f43-a448-3dfeebc0df21`)
- **Propriété Type** : `Writing`
- **Propriété Project(s)** : lien vers le projet « My Writing » (URL de page : `https://www.notion.so/2a5b4629bb3780189199f3c496980c0c`)
- **Propriété Note** : le titre de l'article de blog
- **Contenu** : le contenu complet de l'article en Markdown façon Notion

**Exemple de propriétés d'un appel API Notion :**
```json
{
  "Note": "Blog Post Title Here",
  "Type": "Writing",
  "Project(s)": "[\"https://www.notion.so/2a5b4629bb3780189199f3c496980c0c\"]"
}
```

**CRITIQUE** : le résultat est considéré comme un **échec** si le contenu n'est pas ajouté à Notion. Publiez toujours sur Notion dans le cadre du workflow, même pour des brouillons.

### Phase 5 : finaliser dans la bibliothèque d'exemples (post-résultat)

Quand l'utilisateur confirme que le brouillon est **final** :

1. Enregistrer l'article finalisé dans `references/blog-examples/` avec un nom de fichier au format :
   ```
   YYYY-MM-DD-slug-title.md
   ```
   Exemple : `2025-11-25-why-ai-art-is-useless.md`

2. Vérifier le nombre d'articles dans la bibliothèque d'exemples :
   - Si elle dépasse 20 exemples, demander l'autorisation de l'utilisateur pour supprimer les 5 plus anciens
   - Trier par préfixe de date du nom de fichier pour identifier les plus anciens

Le post-résultat est considéré comme **réussi** quand le brouillon final est enregistré dans le dossier du skill.

## Critères de succès

| Résultat | Succès | Échec |
|---------|---------|---------|
| Primaire | L'utilisateur reçoit le contenu demandé ET il est ajouté à TS Notes avec Type=Writing et Project=My Writing | Contenu livré mais NON ajouté à Notion |
| Post-résultat | Brouillon final enregistré dans `references/blog-examples/` | Brouillon final non enregistré alors que l'utilisateur l'a confirmé comme final |

## Profil du style d'écriture de l'auteur

### Voix et ton
- **Direct et engagé** : énoncer clairement les positions, même contrariennes
- **Conversationnel** : écrire comme en parlant à un collègue — accessible sans être simpliste
- **Première personne pour partager l'expérience** : utiliser « je » naturellement pour les aperçus personnels
- **Scepticisme authentique** : prêt à critiquer les tendances quand c'est justifié

### Schémas de structure
- **Thèse d'ouverture forte** : ouvrir par une affirmation claire, souvent audacieuse
- **Sous-titres partout** : utiliser généreusement le format `###` pour aérer le contenu
- **Paragraphes courts** : rarement plus de 3-4 phrases
- **Anecdotes personnelles tissées dans le texte** : illustrer les propos par des exemples réels
- **Enseignements pratiques** : donner des pistes actionnables, pas seulement de la théorie
- **Conclusion réflexive** : finir par un appel à l'action ou une espérance tournée vers l'avenir

### Longueur et format
- Cible : 800-1500 mots
- Format Markdown avec titres et emphase
- Peu de puces dans la prose — préférer des phrases fluides

### Marqueurs de vocabulaire
- Emploie « tirer parti » (leverage) pour les outils/technologies
- Dit « cela dit » (that said) pour les transitions
- À l'aise avec des affirmations directes comme « c'est inutile » ou « j'ai eu tort, et alors »
- Utilise naturellement les contractions (I've, doesn't, won't)
- Évite le jargon d'entreprise tout en gardant le professionnalisme

### Éléments thématiques
- L'IA comme outil, pas comme remplacement
- Le pratique plutôt que le théorique
- Une technologie centrée sur l'humain
- Une évaluation honnête de ce qui marche et de ce qui ne marche pas

## Ressources

### references/style-guide.md
Référence rapide des schémas d'écriture de l'auteur, de ses préférences de vocabulaire et de ses conventions structurelles.

### references/blog-examples/
Contient des exemples d'articles de blog illustrant le style d'écriture de l'auteur. Ils servent de matériau de référence pour calibrer la voix et la structure. Les nouveaux articles finalisés enrichissent cette bibliothèque au fil du temps.

## Référence API Notion

Pour créer une page dans TS Notes :

```
Database data source ID: 04a872be-8bed-4f43-a448-3dfeebc0df21

Properties:
- "Note": (title) - The blog post title
- "Type": "Writing"
- "Project(s)": ["https://www.notion.so/2a5b4629bb3780189199f3c496980c0c"]

Content: Full blog post in Notion-flavored Markdown
```

L'ID de la page du projet « My Writing » est : `2a5b4629-bb37-8018-9199-f3c496980c0c`
