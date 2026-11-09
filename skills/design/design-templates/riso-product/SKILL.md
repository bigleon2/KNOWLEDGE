---
name: riso-product
description: Gabarit de page produit / page de marque / landing à l'impression Risograph — fond papier crème + trame de demi-teintes + surimpression deux-trois couleurs + grands titres en écriture lishu / au pinceau avec ombre portée décalée + boutons et cartes Neobrutalism à ombre dure. 7 préréglages de palette (rose+bleu / menthe+corail / citron+violet électrique / olive+rose / nuit+fluorescent / bleu ciel+moutarde / terre cuite+bleu canard) × 4 squelettes de mise en page (landing monopage en long défilement / home+page détail unique / magazine indépendant / affiche plein écran). Déclencheurs : l'utilisateur réclame une vitrine de marque, une landing produit, une page de vente limitée ou une publication indépendante « à l'impression / façon riso / sérigraphie rétro / papier crème / magazine à la chinoise ». Ne pas l'utiliser si l'utilisateur dit juste « fais une page produit » sans préciser de style.
visibility: public
mode: template
carrier: web-page
scenario: brand-landing
pattern_source: reference.html
source_priority: skill-first
triggers:
  - « fais une page produit façon riso »
  - « page de marque à l'impression »
  - « landing papier crème »
  - « page produit sérigraphie rétro »
  - « page de marque façon magazine chinois »
  - « page de vente limitée »
  - « page de publication indépendante »
related_patterns: saas-landing
---

# riso-product — pages à l'impression riso

Traduire sur le web le « deux-trois couleurs en surimpression + demi-teintes + papier crème » du duplicateur risograph. Le squelette vient d'un prototype de design pour la marque d'acoustique domestique NOIRLAB (voir `reference.html`), mais **ce skill livre un tempérament et des briques, pas un gabarit**.

## Comment utiliser ce skill

1. **Saisir le ton** : d'abord Read `reference.html` pour comprendre la superposition des couleurs, la direction des ombres, la hiérarchie typographique, la densité des demi-teintes. **Cette étape sert uniquement à « savoir à quoi ressemble le juste résultat ».**
2. **Choisir la palette** : prendre l'un des 7 préréglages ci-dessous (ou ajuster librement selon la description de l'utilisateur), **ne pas prendre par défaut le rose+bleu de la référence**.
3. **Choisir le squelette** : prendre l'un des 4 prototypes de mise en page ci-dessous (ou les combiner) ; **interdiction de cloner intégralement la structure home + 4 pages détail + page histoire de la référence**.
4. **Copier les briques** : les fragments CSS (halftone, paper, ombre neobrutalism, riso shade, ombre décalée des titres) sont réutilisables tels quels.
5. **Passer la ligne rouge** : une fois écrit, s'auto-contrôler avec la liste « obligatoire / interdit ».

## ADN visuel — à ne jamais perdre

S'il manque un seul de ces éléments, ce n'est plus du riso :

1. **Fond papier crème** : le fond ne peut être ni blanc pur ni gris froid ; il doit tirer sur le beige chaude/avoine/lin chaud (luminosité 88–94, saturation 8–18)
2. **Demi-teintes en surimpression** : `body::after` global avec `radial-gradient(circle at 1px 1px, ...)` en grille 5–8px, `mix-blend-mode: multiply`, opacité 30–55 %. Sur les grandes zones en aplat, superposer une seconde couche de grains plus gros (8–12px) d'une autre couleur
3. **Hero deux-trois couleurs en surimpression** : le hero / grands aplats utilisent 2-3 `radial-gradient` ellipse, positions et couleurs différentes (rose + bleu + jaune est le trio classique, mais tout est remplaçable), `mix-blend-mode: multiply`, pour que les couleurs produisent naturellement une troisième teinte aux recouvrements
4. **Grands titres en lishu/pinceau** + **ombre décalée** : `text-shadow: 4px 4px 0 var(--accent-a), 8px 8px 0 var(--accent-b)`, pour simuler le défaut physique de mauvais repérage de la sérigraphie
5. **Ombres dures Neobrutalism** : boutons/cartes avec `box-shadow: Npx Npx 0 var(--ink)` (N=4–8), au survol l'ombre se réduit à 0, l'élément se déplace en `translate(Npx, Npx)`, bordures pleines 2px solid

## Obligatoire / Interdit (auto-contrôle après écriture)

**Obligatoire** :
- [ ] au moins 1 texte avec ombre décalée colorée
- [ ] une trame de demi-teintes visible à l'échelle de la page mais sans brouiller
- [ ] au moins 1 hero / grand aplat en superposition multiply de 2 radial gradients ou plus
- [ ] au moins 1 jeu de boutons/cartes en ombre dure + décalage au survol
- [ ] la police des titres en lishu/pinceau ou régulière kai (voir la pile `--hanli`), **pas PingFang / Source Han Sans**
- [ ] des couleurs saturées mais pas agressives ; le fond paper désacidule tout aplat criard

**Interdit** :
- [ ] ne pas recopier tels quels les `<section>` de reference.html (bandeau d'annonce → header → hero → USP 4 colonnes → feature → cat-grid → material → process → gallery → counters → testi → faq → news → footer + 4 pages détail + 1 page histoire)
- [ ] ne pas prendre par défaut rose #FF3F8E + bleu #2240FF — c'est l'empreinte de NOIRLAB
- [ ] pas de noir et or / glassmorphism / dégradés deep space / emoji / stickers plastiques 3D
- [ ] pas de calque gris lourd sur les images (les demi-teintes restent légères, l'encre doit transparaître)
- [ ] les demi-teintes ne doivent être ni monocolories ni de taille unique, sinon elles font bruit CSS ; au minimum deux couches de grains différents et colorés
- [ ] ne pas recopier les mentions propres à NOIRLAB : nom de marque / Lin Jian'an / Tongji / 28 dB

## Sept préréglages de palette (en choisir un, jamais par défaut)

Chacun respecte la structure « fond crème désaturé + deux couleurs fortes + une d'appoint (optionnelle) ». Copier dans `:root`.

```css
/* 1. Rose chaud + bleu fédéral (original NOIRLAB — prudent, risque de resemblance) */
--paper:#F1EBDA; --ink:#1B1A18;  --a:#FF3F8E; --b:#2240FF; --c:#FFD23A;

/* 2. Menthe + corail — frais, orienté féminin, soin/infusions/boxes d'abonnement */
--paper:#EFEEE5; --ink:#1F2A28;  --a:#FF6B5A; --b:#2BB7A1; --c:#FFC857;

/* 3. Citron + violet électrique — impact fort, tendance, baskets/électronique/marques jeunes */
--paper:#F4EFE4; --ink:#16151A;  --a:#F4E04D; --b:#6A2EE8; --c:#FF4D8D;

/* 4. Olive + rose — posé, introverti, thé/vin/maison/publications indépendantes */
--paper:#EFE9D8; --ink:#1E1C18;  --a:#C24A6C; --b:#5C6E2C; --c:#D9A24A;

/* 5. Nuit + fluorescent — riso sur fond sombre, logique inversée */
--paper:#1B1A18; --ink:#F1EBDA;  --a:#FF3F8E; --b:#4DE0C7; --c:#FFD23A;
/* attention : sur fond sombre, demi-teintes claires et mélange en screen */

/* 6. Bleu ciel + moutarde — plein air, café, slow life, papeterie */
--paper:#EDE8D8; --ink:#1B1B1B;  --a:#3D89C7; --b:#D6A92E; --c:#E0625E;

/* 7. Terre cuite + bleu canard — artisanat/fait main/poterie/arts populaires */
--paper:#F0E7D5; --ink:#1F1A16;  --a:#C25538; --b:#2F6B7D; --c:#E4B83B;
```

Principe de remplacement : dans reference.html, remplacer `var(--pink)` par le `var(--a)` choisi, `var(--blue)` par `var(--b)`, `var(--yellow)` par `var(--c)`. **Remplacement homogène sur tout le site** — pas de rose ici et de rouge là.

## Quatre squelettes de mise en page (en choisir un ; plus jamais le combo « home + 4 détails + histoire »)

Chacun porte le visuel riso mais avec des **structures radicalement différentes**, pour éviter les ressemblances.

### Squelette A — landing monopage en long défilement
```
[bandeau d'annonce défilant] → [hero avec titre décalé] → [USP 3 colonnes] → [grille aperçu produit 3-6 cartes]
→ [spotlight produit vedette avec photo mi-corps + fiche specs] → [citation du fondateur + compteurs]
→ [communauté/avis réels 3 cartes] → [FAQ 5–7 accordéons] → [bandeau d'inscription] → [footer]
```
**Pas de pages détail**. Tout se replie et se déploie dans la même page. Adapté aux marques resserrées à 1–4 SKU.

### Squelette B — deux pages : home + page détail unique (sans routage hash)
```
home : [hero plein écran image + titre décalé] → [grille 4 cartes produit] → [histoire de marque 2 colonnes] → [footer]
detail : detail.html autonome → [grande image hero + capsule prix] → [long texte à gauche + fiche specs sticky à droite]
        → [3 images de détail en galerie] → [3 cartes autres séries] → [retour home]
```
Adapté aux marques avec 1 produit phare + des SKU secondaires (ex. 1 parfum + 3 accessoires).

### Squelette C — mise en page magazine / publication indépendante
```
[page de couverture : un grand caractère + trame riso plein écran + numéro/date en mono]
[sommaire : numéros verticaux à gauche, à droite chaque titre + auteur + rubrique]
[pages intérieures : colonnes asymétriques, long format 6:4 / citation 7:3 / grande image 1:1 / mixte texte-image]
[pied de page façon dos de livre : petits caractères mono, nom de chapitre + pagination]
```
Adapté aux sites de contenu de marque / brand magazine / marques culturelles / projets éditoriaux. Peut se passer de tout bouton CTA.

### Squelette D — affiche plein écran (sans défilement)
```
Le premier écran occupe toute la page :
  haut : annonce + marque
  milieu : titre décalé surdimensionné (60 % de la hauteur d'écran) + sous-titre en une phrase
  bas : un CTA unique + une vignette de détail (ouvrable en lightbox)
Aucun défilement nécessaire. Adapté aux waitlist / drop / séries limitées / événements.
```

## Briques CSS à copier directement

### Grain papier global + demi-teintes (indispensable)
```css
body{
  background: var(--paper);
  color: var(--ink);
  position: relative;
}
/* grain bruité (fibres de papier) */
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9000;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .12 0 0 0 0 .10 0 0 0 0 .08 0 0 0 .35 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity:.45; mix-blend-mode:multiply;
}
/* trame de demi-teintes */
body::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:8990;
  background-image: radial-gradient(circle at 1px 1px, rgba(27,26,24,.08) 1px, transparent 1.4px);
  background-size: 5px 5px;
  mix-blend-mode: multiply; opacity:.55;
}
```

### Ombre décalée des titres
```css
.headline-riso{
  font-family: var(--hanli);  /* voir la pile ci-dessous */
  text-shadow: 4px 4px 0 var(--a), 8px 8px 0 var(--b);
  letter-spacing: .04em;
}
/* version inversée : fond sombre */
.headline-riso--invert{
  color: var(--paper);
  text-shadow: 3px 3px 0 var(--a), 6px 6px 0 var(--c);
}
```

### Pile de polices lishu/pinceau (titres chinois)
```css
:root{
  --hanli: "白舟隷書教漢", "HakushuReisho", "Yuji Mai", "Yuji Boku",
           "ZCOOL XiaoWei", "STLiti", "华文隶书", "LiSu", "SimLi", Georgia, serif;
}
/* repli CDN éventuel */
/* <link href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet"> */
/* détecter via local() la présence du 白舟隷書 sur le système */
@font-face{
  font-family:"HakushuReisho"; font-display:swap;
  src: local("HOT-ReishoR-K"), local("Hakushu Reisho R"), local("白舟隷書教漢");
}
```
**Interdit** d'utiliser PingFang / Source Han Sans / Microsoft YaHei pour les titres — la saveur riso disparaît immédiatement. Le corps de texte peut prendre Inter / sans système.

### Surimpression trois couleurs riso (pour grands aplats/hero)
```css
.riso-shade{
  position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 55% 65% at 18% 25%, rgba(255,63,142,.55) 0%, transparent 60%),
    radial-gradient(ellipse 50% 55% at 82% 75%, rgba(34,64,255,.50) 0%, transparent 60%),
    radial-gradient(ellipse 30% 35% at 65% 18%, rgba(255,210,58,.40) 0%, transparent 70%);
  mix-blend-mode: multiply;
}
```
**Point clé** : les 3 ellipses doivent être **décalées** (haut-gauche / bas-droite / milieu-droite) pour donner l'effet de mauvais repérage. Trois couleurs alignées au centre = échec.

### Bouton Neobrutalism
```css
.btn-riso{
  display:inline-flex; align-items:center; gap:14px;
  padding:16px 28px; font-weight:600; letter-spacing:.05em;
  border:2px solid var(--ink); border-radius:999px;
  background: var(--ink); color: var(--paper);
  box-shadow: 5px 5px 0 var(--a);
  transition: all .25s cubic-bezier(.2,.8,.2,1);
}
.btn-riso:hover{
  background: var(--a); color: var(--paper);
  box-shadow: 0 0 0 var(--a);
  transform: translate(5px, 5px);
}
```
4 variantes : `--ink` (fond noir plein) / `--paper` (fond clair, ombre bleue) / `--ghost` (transparent + bordure ink) / `--accent` (fond en couleur forte). **Au survol, l'ombre se réduit à 0 + translate** : c'est la clé du système — le survol fait « disparaître » l'ombre, pas l'épaissir.

### Carte Neobrutalism
```css
.card-riso{
  border: 2px solid var(--ink);
  box-shadow: 6px 6px 0 var(--ink);
  background: var(--paper-2);
  transition: transform .3s, box-shadow .3s;
}
.card-riso:hover{
  transform: translate(-3px, -3px);
  box-shadow: 9px 9px 0 var(--a);  /* l'ombre passe en couleur + s'agrandit */
}
```

### Demi-teintes sur image (sans noyer la photo)
```css
.img-riso{
  position: relative; overflow: hidden;
  border: 2px solid var(--ink); box-shadow: 5px 5px 0 var(--a);
}
.img-riso > img,
.img-riso > .img{
  width:100%; height:100%; object-fit: cover;
  filter: contrast(1.05) saturate(.9);  /* légère désaturation, vers l'encre */
}
.img-riso::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background-image: radial-gradient(circle at 1px 1px, rgba(34,64,255,.18) 1px, transparent 1.4px);
  background-size: 5px 5px;
  mix-blend-mode: multiply;
}
```
**Principe** : les demi-teintes couvrent l'image mais à 18 % d'opacité seulement, l'image reste nette ; le `filter: contrast(1.05) saturate(.9)` ramène le rendu numérique vers l'encre.

### Bandeau d'annonce défilant (optionnel)
```css
.announce{
  background: var(--a); color: var(--paper);
  border-bottom: 2px solid var(--ink); text-shadow: 1.5px 1.5px 0 var(--b);
  height:40px; display:flex; align-items:center; overflow:hidden;
}
.announce__track{ display:flex; gap:64px; white-space:nowrap; animation: marquee 38s linear infinite; }
@keyframes marquee{ from{transform:translateX(0)} to{transform:translateX(-50%)} }
```

## Chargement des webfonts chinoises (obligatoire)

Les Yuji Mai / ZCOOL XiaoWei de Google sont des webfonts chinois + japonais, volumineuses. Charger en « quatre pièces » :

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" fetchpriority="high"
  href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap">
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap"
  media="print" onload="this.media='all'">
<noscript><link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Yuji+Mai&family=ZCOOL+XiaoWei&display=swap"></noscript>
```
Puis `font-display: swap` + repli sur le lishu système (déjà dans `--hanli`).

## Aide-mémoire des anti-patterns (corriger dès qu'on les voit)

| Symptôme | Erreur | Correction |
|---|---|---|
| Titres en PingFang gras | pas de police pinceau/lishu | passer à `var(--hanli)` |
| Titres sans ombre / ombre noire | pas d'ombre décalée colorée | `text-shadow:4px 4px 0 var(--a),8px 8px 0 var(--b)` |
| Fond #FFFFFF / gris froid | couleur paper inadéquate | passer au crème chaud #F1EBDA / #EFE9D8 |
| Demi-teintes absentes ou en nappe | mauvaise opacité, grains trop gros ou trop denses | grille 5–8px, opacité 30–55 % |
| Images grisâtres et illisibles | overlay trop lourd | demi-teintes à 18 % seulement + `filter: contrast(1.05) saturate(.9)` |
| Au survol, l'ombre du bouton grossit | sens inversé | au survol, l'ombre doit se réduire à 0 + translate de l'élément |
| Tout en rose+bleu NOIRLAB | resemblance | choisir un des sept préréglages |
| 4 pages détail en routage hash | structure clonée de la référence | prendre un squelette A/B/C/D |

## À propos de reference.html

Placé dans le même répertoire que le skill, **toutes les images sont inlinées en base64** (dédupliquées via les variables CSS `:root` `--img-01..06`) — un fichier unique d'environ 2,6 Mo qui s'ouvre d'un double-clic pour voir l'effet complet. **N'en retenir que le tempérament, jamais la structure**. Pour « à quoi ressemble le juste résultat », le consulter ; pour « comment construire mon nouveau projet », suivre les squelettes A/B/C/D et les briques ci-dessus.

## Vérification des informations d'entrée

Faire rassembler ceci à l'utilisateur avant de commencer :
1. Nom de la marque + positionnement en une phrase
2. 1–6 produits / 1 produit phare / événement unique (influence le choix du squelette)
3. Préférence de palette (nom du préréglage ou description)
4. Images : fournies par l'utilisateur ou placeholders picsum
5. Dans la description du style, présence de zones « resemblance NOIRLAB » (l'utilisateur veut « discret et retenu » → éviter le bandeau défilant plein écran du squelette A)

## Exigences de sortie

- HTML monofichier (routage hash optionnel : pas en A/D, optionnel en B/C)
- Responsive mobile (au moins deux des trois paliers ≥1024 / 900 / 520)
- Webfonts chinoises chargées en quatre pièces comme ci-dessus
- Pas de commentaires expliquant le CSS ; le CSS parle de lui-même
