---
name: pricing-page
description: Modèle de page de tarification SaaS pour le marché chinois — verre de bleu ciel doux avec effet glass-morphism, grille de 4 niveaux avec un niveau "recommandé" surélevé, bascule mensuelle/annuelle, accordéon FAQ, tarifs en ¥ avec chiffres Inter, saut de ligne CJK soigné, pied de page avec dépôt ICP.
visibility: public
mode: template
carrier: web-page
scenario: pricing
pattern_source: pricing-cn.html
source_priority: skill-first
triggers:
  - "Faire une page de tarification SaaS"
  - "Page de paiement en chinois"
  - "Bascule mensuelle/annuelle"
  - "Cartes de tarification à 4 niveaux"
  - "Tableau de prix en ¥"
  - "Tarification + FAQ"
---

# Modèle de page de tarification

Utilisez ce modèle lorsque l'artefact est une **page de tarification SaaS / produit pour le marché chinois** qui doit paraître premium, calme et pilotée par le design — pas une grille générique de 3 niveaux avec liste de fonctionnalités.

## Utiliser lorsque

- Le produit est vendu à un public chinois (¥, yuan/mois, dépôt ICP, WeChat/Alipay implicite).
- Le modèle de tarification correspond à des cartes de niveau (3-4 niveaux, bascule mensuelle/annuelle optionnelle).
- Un niveau doit être visiblement surélevé (early-bird, le plus populaire, recommandé).
- La marque peut supporter un effet glass-morphism doux en bleu ciel — ou vous avez l'intention de modifier la palette tout en conservant la structure.

## Éviter lorsque

- Le produit est mondial / principalement en anglais — modifiez fortement le thème ou utilisez un autre modèle.
- Le tarif est purement par siège / mesuré par utilisation sans niveaux — une grille de niveaux est inappropriée.
- La page nécessite une matrice de comparaison de fonctionnalités approfondie comme surface principale — partez plutôt d'un modèle axé sur le tableau de comparaison.
- C'est un produit OSS / gratuit / en liste d'attente — utilisez `waitlist-page/` ou `saas-landing/`.

## Lecture obligatoire

Lisez d'abord ce `SKILL.md`. Ne lisez **pas** `pricing-cn.html` par défaut.

Lisez `pricing-cn.html` uniquement lorsque vous avez besoin de la géométrie concrète des cartes de niveau, des valeurs de transformation du niveau surélevé, du comportement de la bascule mensuelle/annuelle, ou du modèle d'accordéon FAQ avec une seule ouverture. Extrayez les modèles ; ne copiez pas le DOM, les noms de classes, le texte de marque ou les prix d'espace réservé.

## Stratégie de design

Décidez avant de construire :

1. **Nombre de niveaux** — 3 (standard) ou 4 (avec un niveau Observateur / Gratuit).
2. **Niveau recommandé** — lequel se lève et s'inverse (CTA blanc sur fond sombre) ?
3. **Modèle de bascule** — mensuel / annuel avec remise en %, ou étiquettes par lot / cohorte (di N pi) pour l'accès anticipé.
4. **Nom des niveaux** — générique (Basic / Pro / Business) ou atmosphérique (Observer / Early Bird / Founder / Patron). La voix du modèle favorise l'atmosphérique.

## Biais de mise en page

Privilégiez :

- un niveau surélevé (élévation 3D + voile avec image arrière + CTA inversé), les autres cartes plates en verre
- ¥ + chiffres tabulaires Inter pour le prix ; PingFang / MiSans pour le texte environnant
- listes de fonctionnalités courtes (≤ 6 par niveau), chaque préfixée par une coche unique
- une "bande de valeur" sous les cartes (4 appels à l'action courts) plutôt qu'un grand tableau de comparaison
- FAQ comme accordéon avec une seule ouverture, pas développé par défaut
- dépôt ICP dans le pied de page (réel ou espace réservé)

Évitez :

- plusieurs badges "Recommandé" (tuījiàn) sur les niveaux — choisissez-en un
- dégradés 黑金 (hēijīn) (noir-or) ou accents néon (esthétique interdite)
- emojis génériques ou puces d'icônes 3D pour les fonctionnalités
- forcer les noms de niveau en anglais quand le public lit le chinois
- prétendre être Stripe / Linear avec une quasi-copie identique de leur page de tarification

## Plateforme / Taille

Page web responsive prioritaire desktop. Les cartes se réorganisent en 2 + 2 en largeur tablette et s'empilent sur mobile. Gardez le niveau surélevé proéminent à chaque point de rupture.

[INSTRUCTION COMPLÉMENTAIRE : il reste des caractères chinois dans ce document — traduis-les TOUS en français, y compris s'ils se trouvent dans des chaînes de caractères HTML/JS/CSS (attributs title, alt, placeholder, textes visibles, libellés d'interface), dans des tableaux ou des valeurs YAML. Ne garde du chinois que les noms propres (translittérés en pinyin). Renvoie le document intégral traduit, même structure, mêmes lignes.]
