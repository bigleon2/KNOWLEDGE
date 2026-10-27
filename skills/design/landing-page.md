---
name: Landing Page Skill
description: Concevez des pages de destination à thème unique, des pages d'accueil SaaS, des listes d'attente avant lancement, des pages de service, des pages d'agence/studio, des pages de tarification et des pages marketing produit axées sur la conversion, en tant qu'artefacts HTML autonomes.
mode: artifact
platform: responsive-web
scenario: landing-page
preview:
  type: html
default_for:
  - landing page
  - product landing page
  - product homepage
  - SaaS homepage
  - SaaS landing
  - product website
  - marketing page
  - pre-launch waitlist
  - waitlist page
  - service page
  - agency homepage
  - studio homepage
  - pricing page
  - Page d'atterrissage produit
  - Site officiel produit
  - Accueil SaaS
  - Site officiel
  - Page de liste d'attente
  - Page de tarification
fidelity: high
---

# Landing Page Skill

Concevez une page de destination pour **un produit, service, offre ou sujet** qui permet à un visiteur de rapidement répondre à trois questions :

1. **Qu'est-ce que c'est ?**
2. **Pourquoi devrais-je m'en soucier ?**
3. **Que devrais-je faire ensuite ?**

Ce fichier donne des jugements sur les pages de destination, pas un manuel complet de règles. Il s'intègre au flux principal `SKILL.md` — il ne le remplace pas.

## Redirigez ailleurs si

person / body-of-work showcase → `portfolio.md` · product UI / dashboard / app flow / clickable demo / « faire une démo de XX » → `prototype.md` · single-task calculator/generator/checker → `web-tool.md` · linear reading / newsletter / editorial → `content-page.md` · information exploration / data story → `info-interactive.md` · social image / product brief image / report summary image / poster / cover / long-image → `social-card.md` · slides / pitch deck → `deck.md`

Les sites d'agence/studio peuvent être à la fois portfolio et page de destination — privilégiez l'intention dominante : vendre un service (offre claire, CTA de tarification/contact, cadre des compétences) → page de destination ; montrer le travail et la personnalité (grille menée par les études, profondeur des projets, voix distinctive) → `portfolio.md`.

## Les deux non-négociables

Tout le reste est flexible, mais ces deux doivent être vrais :

1. **Un public, une action.** La page sert un public principal et incite à une seule action principale. Chaque section soit fait avancer le visiteur vers cette action, soit construit la confiance pour celle-ci. Si deux CTA sont en compétition à poids égal, la page a déjà échoué.

2. **Valeur concrète dans la première écran.** L'hero doit dire ce que le produit est et fait — en termes de produit, pas de positionnement. "Plateforme alimentée par IA pour booster votre flux de travail" est un échec ; "transformez un CSV de commandes en rapport fiscal prêt en 30 secondes" est un hero. Si le visiteur ne peut pas reformuler l'offre après un écran, réécrivez l'hero avant de styliser quoi que ce soit.

## Choisissez une structure

Choisissez **une** structure en fonction de la mission de conversion de la page. Ne mélangez pas plusieurs structures en une bouillie.

### A. Défilement narratif classique
Hero → problème/valeur → preuve produit → comment ça marche → objections → CTA. Chaque section de défilement répond à la question suivante non posée du visiteur, dans l'ordre.
**Idéal pour :** les produits qui nécessitent une explication avant l'achat ; la plupart des pages SaaS et B2B.
**Le mouvement :** l'ordre des sections = l'ordre des objections. Cartographiez les questions du sceptique ("est-ce que ça fonctionne avec ma stack ?", "combien de temps pour mettre en place ?", "ça coûte combien ?") et laissez les sections y répondre dans l'ordre. Une section qui ne répond à aucune objection est supprimée.

### B. Mise en avant produit
L'interface produit est l'hero — montrée grande, réelle et annotée. Le texte soutient l'image, pas l'inverse.
**Idéal pour :** les produits visuellement forts : outils de design, tableaux de bord, outils de dev avec une UI qui vaut le coup d'être vue.
**Le mouvement :** interface réelle à pleine échelle avec annotations de pointage sur les fonctionnalités réelles. Jamais un mockup de portable flottant à 30° avec un effet glow — cela ajoute trois couches de distance et signale un modèle générique.

### C. Page de vente / tarification
Construite autour de la décision d'achat : forfaits, comparaison, gestion des objections, garantie.
**Idéal pour :** les visiteurs qui connaissent déjà le produit et décident s'ils l'achètent et quel forfait.
**Le mouvement :** répondez aux objections au moment du doute — FAQ à côté du tableau de tarification, conditions de remboursement/annulation à côté du bouton d'achat, lignes de comparaison de forfaits qui correspondent à des situations d'utilisation réelles ("vous avez besoin de ce forfait quand…"), pas une soupe de cases à cocher de noms de fonctionnalités.

### D. Page d'attente / lancement
Scarcité délibérée : une promesse, une visuelle, un champ. La tension vient de la retenue.
**Idéal pour :** les produits avant lancement qui collectent des inscriptions avant d'avoir une histoire complète à raconter.
**Le mouvement :** rendez la valeur de l'inscription explicite — ce que l'abonné obtient (accès anticipé ? prix fondateur ? mises à jour de construction ?) et environ quand. "Rejoignez la liste d'attente" sans récompense déclarée ne convertit personne. Un état de confirmation doit exister (message de succès en ligne au minimum).

### E. Page de service / agence
Cadre des compétences + processus nommé + preuve du travail + chemin de contact.
**Idéal pour :** les cabinets de conseil, studios, freelances qui vendent leur expertise plutôt qu'un produit.
**Le mouvement :** un processus nommé, numéroté ("Semaine 1 : audit → Semaine 2–3 : prototype → Semaine 4 : livraison") est le signal de confiance le plus fort qu'une page de service ait — cela prouve que le travail est systématisé, pas improvisé. Les paragraphes vagues "nous collaborons étroitement" ne prouvent rien.

### F. Lancement éditorial
Style manifeste, mené par la typographie. Le texte EST le design ; l'imagerie est minimale ou absente.
**Idéal pour :** les produits opinionnés, les lancements menés par la marque, les outils de développeurs avec un point de vue fort.
**Le mouvement :** typographie de déclaration surdimensionnée (clamp() jusqu'à ~10–14vw pour la ligne thèse), texte convaincant de longue forme avec vrai rythme de paragraphe, une couleur d'accentuation. Fonctionne seulement si le texte est vraiment percutant — un texte faible à l'échelle d'affichage est juste une faiblesse amplifiée.

### G. Hero à toile interactive
Le produit est utilisable à l'intérieur de l'hero — une démo en direct, une aire de jeu, ou une sortie générée.
**Idéal pour :** les outils et API dont la valeur est prouvable en moins de 10 secondes d'interaction.
**Le mouvement :** le visiteur utilise le produit avant de lire à son sujet. La démo doit vraiment fonctionner avec une logique réelle (`web-tool.md` s'applique strictement à ce composant) ; une fausse démo est pire que pas de démo.

**Anti-modèle : la page SaaS interchangeable.**
Hero avec dégradé doux → accroche vague → trois cartes de fonctionnalités égales → mur de logos en niveaux de gris → carrousel de témoignages → bannière CTA. Cachez le nom du produit et cela pourrait être n'importe quel concurrent. C'est un modèle vêtu des habits d'un produit — si un projet converge vers cela, revenez au choix de structure.

**Pages sensibles à la confiance / entreprise** (fintech, sécurité, santé, infrastructure) : la distinction vient de la hiérarchie, de la densité de preuves, de la clarté du produit et de la retenue — pas de mouvements visuels audacieux. Structure A ou C avec un système discipliné bat un concept expressif ici.## Stratégie de preuve

Décidez ce qui prétend la valeur du produit, puis concevez cette preuve comme une section de premier ordre — pas une après-thought avec bandeau logo.

- **Le produit lui-même est la meilleure preuve.** UI réelle, flux de travail réel, exemple d'entrée→sortie réel. Privilégiez-le à tout témoignage.
- **Choisissez une preuve que le produit peut réellement offrir :** parcours d'interface utilisateur/flux de travail/témoignage client/métrique/étude de cas/benchmark/presse/données de démo en direct. Une forme forte vaut mieux que quatre faibles.
- **N'inventez jamais de preuve.** Aucun faux logos, témoignages, nombres d'utilisateurs, récompenses, données marché ou citations. Les preuves d'espace réservé doivent être visiblement marquées comme telles. Règles détaillées : `horizontal-craft/link-and-proof.md`, `horizontal-craft/data-integrity.md`.

## Mouvements spécifiques aux pages d'atterrissage

### Niveaux de poids visuel, jamais un CSV avec CSS
Chaque section dense en informations a besoin d'au moins quatre niveaux de poids visibles : moment héroïque / modules primaires / modules secondaires / détails tertiaires. Une page de cartes de hauteur égale en colonne unique est un tableau avec padding. Donnez à l'affirmation la plus forte 2-3× l'espace des points de soutien ; laissez les fonctionnalités mineures se comprimer en une grille compacte ou une ligne chacune.

### Rythme de densité
Alternez des moments de déclaration pleine page avec des sections informationnelles plus denses. Un moment dominant par page (l'héroïque ou une section milieu de page), tout le reste le soutient. Une page où chaque section crie au même volume est perçue comme du bruit ; une page de densité moyenne uniforme est perçue comme un document.

### L'appel à l'action répété, avec retenue
CTA principal à l'héroïque, puis à chaque moment d'engagement naturel (après la section preuve, après les prix, en fin de page). Même formulation et style à chaque fois — la répétition crée la familiarité. Les actions secondaires ("lire docs", "regarder vidéo") reçoivent un traitement visuellement subordonné partout : lien texte ou bouton fantôme, jamais un deuxième bouton plein à côté du principal.

### Héroïque asymétrique, pas la sécurité centrée
Définissez par défaut une composition héroïque déséquilibrée — colonne de copie contre visuel produit à `1fr 1.2fr`, titre dépassant dans la marge, image produit déborderant sur un bord. Titre centré + sous-titre centré + bouton centré est le signal de modèle unique le plus fort. Centrez seulement quand la rareté de la structure D ou le manifeste de F l'exige vraiment.

### Échelle d'objections pour les prix
Là où un prix apparaît, les trois angoisses d'achat doivent être résolues dans un seul viewport : exactement quoi j'obtiens, que se passe-t-il si ça ne marche pas (conditions d'annulation/remboursement/essai), et quelle option est pour moi (niveau recommandé mis en évidence avec une raison, pas juste un badge "POPULAIRE").

### Les nombres comme matériau de design
Les métriques réelles (latence, précision, temps économisé, quantités) affichées à l'échelle d'affichage avec de petites étiquettes sont à la fois preuve et texture visuelle. Seulement des nombres réels ou clairement étiquetés comme démo — et respectez `horizontal-craft/data-integrity.md`.

## Liste de vérification de complétude

Une page d'atterrissage est terminée quand :

- [ ] L'héroïque répond à quoi/pourquoi/action-suivante en un écran, en termes concrets de produit
- [ ] Une structure (A-G) est reconnaissable ; la page n'est pas un mélange
- [ ] Chaque section dense en informations montre quatre niveaux de poids visuel — pas de murs de cartes égales
- [ ] Le CTA principal apparaît à l'héroïque et revient aux moments d'engagement naturels ; les actions secondaires ne concurrencent jamais
- [ ] Chaque CTA mène à une vraie étape suivante — formulaire fonctionnel avec état de succès, ancrage prix, mailto, ou vue de confirmation ; jamais `href="#"`
- [ ] Toutes les preuves sont réelles ou visiblement marquées comme espace réservé
- [ ] Les sections qui ne servent aucune objection ou objectif sont supprimées, pas remplies
- [ ] Les pages prix/ventes répondent aux trois angoisses d'achat ; les pages liste d'attente indiquent la récompense de l'inscription
- [ ] La page fonctionne sur mobile — la structure s'adapte, pas seulement se réduit
- [ ] Le test de distinction passe : cachez le nom du produit — la page ne fonctionnerait pas inchangée pour un concurrent arbitraire

## Comment cela s'intègre au flux de Design Skill

- **Type de scène.** Une page d'atterrissage est une scène **expressive** par défaut (selon `SKILL.md`) : concevez à partir des choix de structure de ce fichier + Contexte Créatif + horizontal craft. Ne la poussez pas vers un kit UI générique. Exception : les briefs sensibles à la confiance/entreprise peuvent aller volontairement sobre — c'est un jugement, pas un recours.
- **Modèles.** Si `design-templates/TEMPLATE-ROUTER.md` + `INDEX.md` a un motif correspondant (atterrissage SaaS, prix, liste d'attente, lancement, service), il peut fournir le squelette — mais le choix de structure et le moment signature déterminent encore le résultat ; ne livrez jamais une mise en page de modèle inchangée.

## Contexte Créatif (de SKILL.md)

Pour les demandes ouvertes, complétez silencieusement avant de générer :

- `creative_positioning` — de quoi le produit est vraiment au-delà de la liste des fonctionnalités (une ligne ; cela devient l'angle de l'héroïque).
- `first_impression` — ce que le visiteur devrait ressentir dans les 3 premières secondes (liez-le au choix de structure et au traitement de l'héroïque).
- `anti_default` — quel réflexe générique à éviter (généralement l'anti-modèle Page SaaS Interchangeable ; nommez le cliché spécifique dont ce produit est le plus à risque).

L'artefact doit refléter cela visiblement. N'imprimez pas le contexte sauf demande.

## Références — chargez seulement quand déclenché

Ne lisez pas ces éléments par défaut. Un premier brouillon a généralement besoin de ce fichier + d'une référence modèle/système de design sélectionnée si présente + seulement 1-3 fichiers craft déclenchés.

- `horizontal-craft/chinese-typography.md` — texte chinois substantiel. **Si la page a du chinois, ses règles de police sont obligatoires** : les polices nommées doivent vraiment se charger, `font-family` doit contenir un nom de police CJK, et les webfonts se chargent non-bloquantes (preload + fetchpriority / print-onload / unicode-range subset / fallback système) — pas de FOIT sur les lents réseaux.
- `horizontal-craft/color.md` — aucun système de design n'est fourni, ou la direction couleur est vague.
- `horizontal-craft/icon-system.md` — icônes fonctionnelles, pictogrammes, icônes de nav. Pas d'emoji comme icônes.
- `horizontal-craft/link-and-proof.md` — logos, témoignages, affirmations, récompenses, presse, citations, liens CTA, ou modules de preuve.
- `horizontal-craft/data-integrity.md` — métriques, ROI, taille du marché, benchmarks, graphiques, ou tableaux.
- `horizontal-craft/animation-discipline.md` — révélation au défilement, parallaxe, mouvement héroïque, micro-interactions. Pour une page d'atterrissage expressive, une page entièrement statique est généralement sous-délivrée ; prenez le CSS d'entrée prêt-à-coller d'ici.
- `horizontal-craft/technique-library.md` — effets avancés au-delà du CSS pur qui servent réellement la compréhension ou l'histoire produit (notamment la structure G).
- `design-system-reference.md` — un guide de marque, référence de style, modèle, ou `DESIGN.md` est fourni ou référencé.
- `canvas-and-device.md` — viewport spécial, cadre d'appareil, taille d'export, ou contraintes de breakpoint.## Porte finale

Exécutez `quality-gate.md` comme la liste de contrôle finale bloquante avant la livraison. Il contient les vérifications globales (accessibilité, liens morts, fausses preuves, logique de placeholder, anti-AI-slop, commentaires de Conformité Design) — ne les dupliquez pas ici.

Porte spécifique aux pages de destination, en plus de la Liste de Conformité ci-dessus :

- le hero explique l'offre réelle, pas le positionnement flou ;
- le "mouvement" de la structure choisie est présent, pas seulement son ordre de sections ;
- les pages de prix/ventes répondent aux objections d'achat au moment du doute ;
- les pages d'attente/lancement rendent le gain d'inscription explicite et confirment le succès ;
- la direction visuelle fait écho au produit et à l'audience — chaque choix majeur (palette, composition du hero, typographie, mouvement, ordre des modules) a une raison produit ;
- un haut niveau de finition ne cache pas une structure faible : retirez mentalement le style — la logique des sections doit encore tenir.

## Transmission

Utilisez le flux de livraison, d'exportation et de gestion de versions standard de Design Skill (`export.md`). Les pages de destination n'ont pas de processus de transmission séparé sauf si l'utilisateur demande une transmission/exportation/package d'actifs.
