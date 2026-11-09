# Magazine Web PPT · Skill de PPT web façon magazine électronique

> 🌏 **English version: [README.en.md](./README.en.md)**

Un skill [Claude Code / Claude Agent Skills](https://agentskills.io/) pour générer des **PPT HTML monofichiers à défilement horizontal**, dont le ton visuel est « **magazine électronique × encre électronique** » — comme *Monocle* avec du code plaqué dessus.

> Distillé par [歸藏](https://x.com/op7418) lors de partages en présentiel comme « L'entreprise d'une seule personne : l'organisation pliée par l'IA » et « Une nouvelle façon de travailler » ; chaque piège rencontré est consigné dans `checklist.md`.

![Démonstration Magazine Web PPT](https://github.com/user-attachments/assets/5dc316a2-401c-4e37-9123-ea081b6ae470)

## Effets

- 🖋 **Grands titres serif + corps sans-serif + métadonnées monospace** : une répartition typographique à trois niveaux
- 🌊 **Fond WebGL fluides/dispersion**, visible sur la page héro, retenu sur les pages de contenu
- 📐 **Défilement horizontal gauche-droite** : clavier ← → / molette / glisser tactile / pastilles en bas / index ESC
- 🎨 **5 préréglages de thèmes** : Encre classique / Indigo porcelaine / Encre forêt / Papier kraft / Dune
- 🧩 **10 gabarits de pages** : couverture d'ouverture, volet de chapitre, grands chiffres, texte à gauche/image à droite, grille d'images, Pipeline, question en suspens, grande citation, comparaison Avant/Après, mixte texte-image
- 📄 **HTML monofichier** : ni build ni serveur, ouverture directe dans le navigateur

## Adapté / inadapté

**✅ Adapté** : partage en présentiel / discours internes au secteur / rencontres privées / lancement de produit IA / demo day / présentations à forte personnalité

**❌ Inadapté** : gros tableaux de données / supports de formation (densité d'information insuffisante) / édition collaborative à plusieurs (HTML statique)

## Installation

### Méthode 1 : envoyer directement ce texte à l'IA (recommandé)

> Aide-moi à installer le skill Claude Code `guizang-ppt-skill`. Suis ces étapes :
>
> 1. T'assurer que le répertoire `~/.claude/skills/` existe (le créer sinon)
> 2. Exécuter `git clone https://github.com/op7418/guizang-ppt-skill.git ~/.claude/skills/magazine-web-ppt`
> 3. Vérifier : `ls ~/.claude/skills/magazine-web-ppt/` doit montrer `SKILL.md`, `assets/`, `references/`
> 4. Me confirmer l'installation ; ensuite, quand je dirai « fais-moi un PPT façon magazine » le skill se déclenchera

Copier-coller ce texte dans Claude Code / Cursor / tout agent IA avec accès shell, l'installation se fera automatiquement.

### Méthode 2 : ligne de commande manuelle

```bash
git clone https://github.com/op7418/guizang-ppt-skill.git ~/.claude/skills/magazine-web-ppt
```

### Mode de déclenchement

Une fois installé, Claude Code découvre et invoque ce skill automatiquement dans la conversation. Mots-clés déclencheurs :

- « fais-moi un PPT façon magazine »
- « génère un horizontal swipe deck »
- « editorial magazine style presentation »
- « slides de présentation style encre électronique »

## Flux d'utilisation

Le skill est un workflow structuré en 6 étapes, que Claude guide pas à pas :

1. **Clarification du besoin** — liste de 6 questions : audience, durée, supports, images, thème, contraintes dures
2. **Copie du gabarit** — `assets/template.html` → répertoire projet, modifier `<title>`, changer le thème
3. **Remplissage du contenu** — choisir parmi les 10 gabarits de layout, coller, adapter les textes (avec pré-contrôle des classes + planification du rythme des thèmes)
4. **Auto-contrôle** — conformément à `references/checklist.md`, les problèmes de niveau P0 doivent tous passer
5. **Prévisualisation** — ouverture directe dans le navigateur
6. **Itération** — ajuster tailles/hauteurs/espacements via inline style

Description détaillée dans [`SKILL.md`](./SKILL.md).

## Structure du répertoire

```
magazine-web-ppt/
├── SKILL.md              ← fichier principal du skill : workflow, principes, erreurs courantes
├── README.md             ← ce fichier
├── assets/
│   └── template.html     ← HTML de départ complet et exécutable (CSS + WebGL + JS de pagination tout prêt)
└── references/
    ├── components.md     ← manuel des composants (typo, couleurs, grille, icônes, callout, stat, pipeline)
    ├── layouts.md        ← 10 gabarits de pages (collables directement)
    ├── themes.md         ← 5 préréglages de thème (à choisir, pas de personnalisation)
    └── checklist.md      ← liste de contrôle qualité (niveaux P0 / P1 / P2 / P3)
```

## Préréglages de thème

Choisir un ensemble dans `references/themes.md` — **les valeurs hex personnalisées sont interdites** : protéger l'esthétique compte plus que la liberté.

| Thème | Contextes adaptés |
|------|---------|
| 🖋 Encre classique | défaut universel, publication commerciale, quand on ne sait pas quoi choisir |
| 🌊 Indigo porcelaine | tech / recherche / IA / conférences techniques |
| 🌿 Encre forêt | nature / durabilité / culture / documentaire |
| 🍂 Papier kraft | nostalgie / humanités / littérature / magazine indépendant |
| 🌙 Dune | art / design / création / galerie |

Changer de thème = remplacer les 6 lignes de variables du `:root{}` en tête de `template.html` ; tout le reste du CSS passe par des `var(--...)`.

## Principes de design fondamentaux

1. **La retenue prime sur la démonstration technique** — le fond WebGL n'apparaît que sur la page héro
2. **La structure prime sur la décoration** — l'information repose sur les tailles + contrastes typographiques + grilles et blancs, pas sur les ombres et cartes flottantes
3. **L'image est citoyenne de première classe** — rogner seulement en bas, le haut et les côtés restent entiers
4. **Le rythme vient de la page héro** — alterner héro / non-héro, sinon l'œil se fatigue
5. **Terminologie stable** — Skills reste Skills, pas de traduction mi-chinoise mi-anglaise

## Références visuelles

- La mise en page du magazine [*Monocle*](https://monocle.com)
- YC Garry Tan « Thin Harness, Fat Skills »
- La série de PPT des partages en présentiel de 歸藏

## Contribuer

Bugs, problèmes de mise en page, demandes de nouveaux gabarits — Issues et PR bienvenus. Pour les modifications, privilégier :

- Ajouter les classes dans `template.html`, ne pas faire utiliser à layouts.md des classes non définies
- Consigner les pièges rencontrés dans `checklist.md` au niveau P0 / P1 / P2 / P3 correspondant
- Les nouveaux thèmes vont dans `themes.md` avec leurs contextes d'usage

## Licence

MIT © 2026 [op7418](https://github.com/op7418)
