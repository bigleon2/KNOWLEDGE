---
name: xianying-tool
description: Modèle de page d'atterrissage d'outil de génération d'images IA axé sur le chinois — hero centré de style TwelveMei avec navigation d'île flottante d'icônes, titre d'affichage avec police FlyFlowerSong (Fei Hua Ge) serif, CTAs en forme de pilule texturée, maquette de toile de verre de l'outil lui-même, palette d'encre monochrome. Conçu pour les pages de produit d'outils créatifs / d'images génératives / AI-工具 (gong ju) destinés aux concepteurs et éditeurs, pas au marketing agressif.
visibility: public
mode: template
carrier: web-page
scenario: product-tool-landing
pattern_source: index.standalone.html
source_priority: skill-first
triggers:
- "créer une page d'atterrissage pour un outil IA"
  - "Générateur d'images landing" (page d'atterrissage pour un outil de génération d'images)
- "TwelveMei 风工具页" (page d'outil de style TwelveMei)
  - "玻璃画布 mockup" (maquette de toile de verre)
  - "<LIGNES À TRADUIRES> Outils d'IA (Zhongwen AI-tools) </LIGNES À TRADUIRES>" (page de produit d'outil IA en chinois)
- "Songti hero 工具页" (page d'outil hero avec police Song)
---

# Modèle Xianying Tool

Utilisez ce modèle lorsque l'artefact est une **page de produit d'outil créatif IA / d'images génératives en langue chinoise** qui doit donner l'impression d'un atelier éditorial tranquille, pas un argumentaire SaaS.

## À utiliser quand

- Le produit est un outil créatif (shēng tú / shè jì / biān jí / AI gōng jù - génération d'images / design / édition / outil IA) dont l'audience est des concepteurs, illustrateurs ou éditeurs chinois.
- Le hero doit **montrer l'outil lui-même** — une maquette de toile de verre avec onglets de cas, préréglages, carte de prompt, puces graine/style — plutôt qu'une métaphore ou une illustration générique.
- La navigation doit être une **île centrale flottante d'icônes** (Shouye / Anlanglang / Moxing / Dingjia / Wenzhang - accueil / galerie de cas / modèles / tarification / documentation), avec la marque à gauche et un CTA en pilule texturée à droite.
- L'apparence doit être monochrome encre — fond papier, typographie encre foncée, une accentuation mesurée — avec FlyFlowerSong (ou une autre serif moderne à fort contraste) pour le titre d'affichage et MiSans pour le texte de l'interface.
- La page est menée par un seul écran : hero + toile de verre + une courte bande de portfolio + pied de page. Les longs rouleaux de fonctionnalités sont hors de portée.

## À éviter quand

- Le produit est un **SaaS B2B** avec tarification par paliers comme surface principale — utilisez plutôt `pricing-page/` ou `saas-landing/`.
- La page est une **liste d'attente avant lancement** (pas de toile fonctionnelle, juste un formulaire d'email) — utilisez `waitlist-page/`.
- La marque veut du marketing agressif — dégradés vifs, vidéo hero, murs de preuves sociales. Ce modèle est discret et éditorial.
- L'audience est principalement anglophone — l'empilement de polices et le rythme sont réglés pour l'affichage CJK + support latin, et non l'inverse.
- L'artefact est un tableau de bord, une présentation, une carte sociale ou un rapport PDF — choisissez le modèle correspondant.

## Lecture obligatoire

Lisez d'abord ce `SKILL.md`. Ne lisez **pas** `index.standalone.html` par défaut — il fait ~11MB avec des polices web en base64 intégrées et inondera le contexte.

Lisez `index.standalone.html` seulement quand vous en avez besoin : la géométrie de la navigation d'île d'icônes, la composition de la maquette de toile de verre (canvas-frame / canvas-glass / canvas-row / case-tabs / preset chips), le traitement du CTA en pilule texturée, le verrouillage de la marque (`Xianying` + `XIANYING®`), ou la structure de colonne du pied de page. Extrayez les modèles ; ne copiez pas les noms de préréglages (Lingjing / Huan yi / Huan guang / Xia zhao / Chu fa xianying), les étiquettes de modèle (GEN-3 / GEN-2 / Xian gao mo xing), ou le dépôt ICP en bloc.

## Stratégie de design

Avant de placer les composants, décidez ce que le hero **vend** :

- l'**outil** (toile + préréglages dominent, le titre est une phrase sur l'audience)
- l'**esthétique** (une seule image générée domine, les contrôles sont suggérés)
- la **gamme de modèles** (onglets de cas / rangée de cartes de modèle dominent, la toile est secondaire)
- le **portfolio** (la bande de galerie apparaît, le hero se comprime)

Choisissez-en un. Mélanger les quatre aplatit la page en une liste de fonctionnalités.

Le modèle de titre ici est `显影 (Xianying) <LIGNES TRADUITES> est une destination pour </LIGNES TRADUITES>[Public]Outil de génération d'images.` — une seule phrase qui nomme l'audience en ligne. Gardez ce rythme : une phrase déclarative, audience en emphase serif, point à la fin. Ne le remplacez pas par un slogan marketing.

## Biais de mise en page

Préférer :

- FlyFlowerSong (ou une police Song moderne comparable avec fort contraste de trait) pour le titre d'affichage ; MiSans Heavy / Bold / Semibold pour les poids d'interface ; Inter pour les chiffres et les étiquettes latines.
- fond de ton papier (#F7F4EE / mǐ bái - blanc de riz) avec typographie encre foncée (#1A1A1A), une accentuation gris chaud ou à une seule couleur — jamais deux accents sur le même écran.
- boutons en forme de pilule texturés (bruit subtil / grain de papier), pas de remplissage plat uni.
- navigation d'île flottante d'icônes avec puces d'info-bulle au survol ; marque à gauche, unique CTA en pilule à droite.
- maquette de toile de verre avec un cadre fin, ombre interne légère et rangée de toile visible de puces de préréglages en bas — montrez l'outil en fonctionnement, ne le simulez pas avec une capture d'écran.
- pied de page en quatre courtes colonnes (chanpin / gongsi / ziyuan / tiaokuan - produit / entreprise / ressources / termes) plus une ligne bei'an xinxi - conformité internet chinoise, pas décorative.

Éviter :

- 黑金 (Heijin) / dégradés foncés / surcharges "premium exécutif" — ce modèle est de l'encre monochrome sur papier.
- polices monospace n'importe où (la note de direction dit explicitement pas de mono).
- séparateurs entre les éléments de nav (`首页 · 案例廊 · 模型`) — l'île d'icônes les remplace.
- emoji dans la nav, les CTAs ou les puces de préréglage.
- autocollants en 3D, reflets brillants ou illustrations hero générées par IA de la toile.
- forcer l'espacement négatif entre les caractères CJK d'affichage — FlyFlowerSong a besoin de son rythme natif.

## Plateforme / Taille

Priorité au bureau, largeur de conception ~ 1280–1440px. La navigation d'île d'icônes et la maquette de toile de verre sont les éléments porteurs — elles ont besoin d'espace horizontal. Sur tablette (~ 900px) la toile se replie en aperçu empilé ; sur mobile l'île d'icônes devient une bande d'onglets en haut et la toile passe en carte à seule image. Ne faites pas semblant que ce soit une application native mobile.
