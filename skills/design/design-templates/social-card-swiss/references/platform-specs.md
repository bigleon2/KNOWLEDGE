# Spécifications de Plateforme

Utilisez des exports haute résolution. L'utilisateur pourra ensuite sous-échantillonner.

## Xiaohongshu / Rednote

Taille par défaut :

- `1080 x 1440`
- Ratio : `3:4`
- Export : PNG pour les images riches en texte, JPEG uniquement lorsque c'est une photo uniquement et que la taille du fichier compte.

Zone de sécurité :

- Marge latérale : 72-96px.
- Marge supérieure : 72-112px.
- Marge inférieure : 80-120px.
- Gardez tout le texte et les objets clés à l'intérieur de la zone de sécurité.

Ensemble recommandé :

- 1 couverture.
- 4-8 pages de contenu.
- 1 page de résumé ou de liste de vérification si l'article en bénéficie.

Nommage :

```text
output/xhs-01-cover.png
output/xhs-02-<topic>.png
output/xhs-03-<topic>.png
...
```

Structure de la couverture :

- Grand titre avec un accroche percutante.
- Une forte visuelle : image fournie, capture d'écran, photo générée ou objet produit.
- Ligne du bas avec 3-5 points clés ou une bande de problèmes compacte.
- Évitez les sous-titres longs. Mettez les nuances dans les pages suivantes.

Structure de la page de contenu :

- Une idée par page.
- 12-30 caractères chinois pour le titre lorsque c'est possible.
- 2-4 fragments de puces courts ou un paragraphe concis.
- Si une page a une capture d'écran, réduisez le texte et donnez à la capture d'écran assez d'espace.
- Si l'espace inférieur est vide à travers les pages, combinez les pages ou ajoutez un élément fonctionnel tel que liste de vérification, ligne de comparaison, citation ou image de preuve.

## Paire de Couvertures pour Compte Officiel WeChat

Générez une paire : une couverture principale `21:9` et une couverture carrée `1:1`. Construisez-les dans le même fichier HTML, et incluez une section d'aperçu combiné qui les place ensemble pour vérification visuelle.

### Couverture Principale 21:9

Taille par défaut :

- `2100 x 900`
- Ratio : `21:9`

Utilisation :

- Couverture principale de l'article.
- Titre complet ou presque complet, sous-titre et preuve visuelle.
- Gardez le titre lisible près du centre-gauche ou à l'intérieur d'une bande de sécurité claire.
- Évitez le centre vide. Augmentez l'échelle du titre, l'échelle de l'image ou l'espacement si le centre semble creux.

### Couverture 1:1

Taille par défaut :

- `1080 x 1080`
- Ratio : `1:1`

Style par défaut :

- Uniquement un court titre, simplifié à partir du long titre.
- Gros texte, centré.
- Pas d'image sauf si l'utilisateur le demande explicitement.
- Pas de sous-titre par défaut.
- Contraste fort et assez d'espace respiratoire.

Règle du titre court :

- Extrayez l'objet et l'action clés du long titre.
- Gardez-le à environ 4-10 caractères chinois, ou 2 lignes courtes si nécessaire.
- N'essayez pas de faire tenir le titre complet `21:9` dans le carré.

Exemple :

```text
Long: An open-sourced Skill that lets AI take over the sticky note at the edge of your screen
Square: AI takes over the sticky note
```

Nommage :

```text
output/wechat-21x9-cover.png
output/wechat-1x1-cover.png
output/wechat-cover-pair-preview.png
```

## Placement des Captures d'Écran et Photos

Pour les captures d'écran/photos fournies :

- Mettez les originaux dans `assets/`.
- Utilisez CSS `object-fit:cover` uniquement lorsque la recadrage est sûr.
- Utilisez CSS `object-fit:contain` pour les captures d'écran d'interface utilisateur, texte dense, code, tableaux ou fenêtres d'application.
- Réglez `object-position` intentionnellement : haut pour les longues interfaces utilisateur lorsque le haut compte, centre pour les objets, 35%-45% vertical pour les portraits.
- Ne pas agrafer les images au bord du canevas sauf si la conception utilise intentionnellement un débordement (bleed).

## Média de la Réponse Finale

Dans Codex desktop, les médias locaux peuvent être affichés avec des chemins absolus :

```markdown
![cover](/absolute/path/to/output/xhs-01-cover.png)
```

Faites cela pour les images les plus importantes, en particulier la couverture et toutes les pages que l'utilisateur a demandé inspecter.
