---
name: vr-canvas
description: Générer un site portfolio monofichier façon VR — les œuvres sont carrelées à l'intérieur d'un cylindre/sphère 3D (enveloppe concave, comme dans un casque immersif), inclinaison de tête contrôlée à la souris, appui long pour faire glisser et parcourir le canevas infini, clic pour ouvrir le détail d'une œuvre. Inclut des overlays À propos / CV / Contact / Filtre. Prend en entrée une description en langage naturel du studio et des œuvres (images + textes courts) ; produit UN fichier .html fonctionnel. Fonctionne AUSSI BIEN dans Claude Code (écrit dans ~/Desktop) que dans GLM / chat en ligne (sort le HTML en ligne). Phrases déclencheuses : « fais un portfolio VR », « fais un portfolio canevas infini », « fais un portfolio enveloppé en dôme », « vr-canvas-gen ... », ou quand l'utilisateur glisse ce dossier de skill dans le chat en demandant un portfolio enveloppant/immersif.
visibility: public
mode: template
carrier: web-page
scenario: portfolio
pattern_source: reference.html
source_priority: skill-first
triggers:
  - « fais un portfolio VR »
  - « fais un portfolio canevas infini »
  - « fais un portfolio enveloppé en dôme »
  - « portfolio écran incurvé »
  - « portfolio avec sensation d'enveloppement »
related_patterns: portfolio-detail, digital-eguide
legacy_gen: true
---

# vr-canvas — générateur de portfolio VR à écran incurvé

## Quand se déclencher
L'utilisateur dit « fais un portfolio VR » / « fais un portfolio dôme / écran incurvé / enveloppant » / « fais un portfolio canevas infini » / « vr-canvas-gen ... », et fournit :
- **des fichiers d'œuvres** (images, chemin de dossier ou plusieurs chemins de fichiers) — en mode GLM, une description peut suffire
- **une description en langage naturel** (présentation du studio + histoire de chaque œuvre — la prose libre convient, pas besoin de structure)

## Analyse de l'entrée
Extraire du message de l'utilisateur :
- **works_path** (requis en mode A) : chemin du dossier d'œuvres ou ensemble de chemins de fichiers
- **bio_text** (requis) : présentation du studio + contexte de chaque projet. Peut contenir : nom du studio, ville, domaine, année de création, équipe, types de clients, histoire de chaque œuvre
- **variante de style** (optionnel) : par défaut ambiance sombre « matériaux/studio » ; si l'utilisateur dit « clair / façon magazine / cyber / minimaliste », ajuster la palette `:root`

Si l'utilisateur dit juste « fais un portfolio VR » sans fournir d'œuvres → **demander une fois** les œuvres et le nom du studio.
Des œuvres sans description → **ne pas relancer**, inférer titres et catégories depuis les noms de fichiers/le contenu visuel.

## Environnements d'exécution (deux modes)

### A. Claude Code / local (avec système de fichiers)
- Utiliser `Bash` pour lister les fichiers, `sips` pour sonder les dimensions, `cp` pour copier les images
- Sortie vers `~/Desktop/{slug}-vr-canvas/index.html` + `images/`
- Images en chemins relatifs `images/work-NN.jpg`
- Le gabarit embarque `images/p-01-color-macro.jpg ... p-18-magazine.jpg`, 18 photographies réelles orientées design (≈2,2 Mo) : sans image fournie par l'utilisateur, ouvrir template.html suffit pour voir l'effet VR complet de la sphère

### B. GLM / dialogue en ligne (sans système de fichiers)
- Vous **produisez uniquement une chaîne HTML complète** (dans un bloc de code ```html)
- L'utilisateur a téléversé des images sans URL → utiliser `https://picsum.photos/seed/{description-index}/1080/1080` comme placeholder
- L'utilisateur a donné des URL → directement `<img src="https://...">`
- Ne pas tenter d'accéder aux fichiers locaux, ne pas suggérer d'opérations en ligne de commande (sauf « enregistre ce contenu en index.html »)

Décision : **impossible de lire les images locales avec Read** → mode B par défaut.

## Répartition des fichiers

| Fichier | Rôle | Usage |
|---|---|---|
| `reference.html` | **produit fini complet** (studio Xubai, 20 œuvres + textes about/cv/contact/filter entiers) | à regarder : ton des textes de tuiles, vocabulaire des tags, longueur des desc, densité about/cv, ambiance générale |
| `template.html` | **squelette vide** (mêmes CSS/JS, 2 exemples + tous les repères SWAP) | le modifier pour produire le HTML final |

**Règle cardinale** : toutes les modifications partent de `template.html` ; on apprend de `reference.html` **comment écrire dans le ton**, sans copier son contenu précis (Xubai, résidence Kyoto, pavillon de thé Aoki… tout cela appartient à quelqu'un d'autre).

## Étapes de travail

### 1. Lire les deux HTML
- D'abord `template.html`, repérer les marqueurs SWAP (12 au total)
- Puis parcourir `reference.html` du regard, saisir la densité et le rythme des textes d'œuvres et de about/cv

**Ne pas modifier le JS, ni le CSS de .work / .frame / .sphere / .viewport / .overlay, ni aucune logique #sphere / #viewport / .splash**.

### 2. (mode A seulement) Lister les œuvres + sonder les dimensions
```bash
ls -la "{works_path}"
sips -g pixelWidth -g pixelHeight "{works_path}/{file}" 2>/dev/null
```

Pour chaque œuvre, à partir du nom de fichier + jugement visuel (Read sur quelques représentatives) → (title, brand, year, tags, desc).

### 3. Analyser bio_text pour extraire les informations

**Niveau studio** (chaque valeur avec au moins un repli par défaut) :
- **STUDIO_NAME_CN / STUDIO_NAME_EN** (ex. « Xubai 虚白 / Xubai », « Mingchuan 明川 / Mingchuan »)
- **STUDIO_TYPE** (ex. « studio de design », « studio d'image », « agence d'architecture », « designer indépendant »)
- **TAGLINE** (deux lignes : phrase longue + conclusion courte, modèle : « Xubai est un studio de design chinois qui prend les matériaux et les scènes pour méthode, cherchant une position de repos entre marque, visuel et espace »)
- **LOCATION_PRIMARY / SECONDARY** (ex. « Chine · Shanghai », « Japon · Kyoto » ; une seule ville → supprimer la deuxième ligne)
- **TIMEZONE_PRIMARY / SECONDARY** (ex. « heure de Pékin UTC+8 », JST/EST pour la seconde ville)
- **YEAR_FOUNDED** (ex. 2017)
- **CTA_TEXT** (défaut « venons discuter. », remplaçable par « Let's Talk », « contact et collaborations », etc.)
- **TAB_LABELS** (défaut `Œuvres / À propos / Parcours`, modifiable)
- **CAPABILITIES** (4—5 compétences, pour l'overlay about)
- **TEAM** (3—5 membres, pour l'overlay about ; portfolio personnel → une seule ligne pour soi)
- **CV_YEARS** (chronologie de projets groupée par année)
- **AWARDS** (3—8 expositions/prix)
- **CONTACT_EMAILS** (trois boîtes : nouveau projet / presse / recrutement)
- **OFFICE_ADDRESSES** (1—2 adresses de bureaux)
- **SOCIAL** (IG / WeChat / Twitter / Behance etc.)
- **FILTER_CATEGORIES / YEARS** (cases à cocher de l'overlay filter, dérivées automatiquement de WORKS)

**Chaque œuvre** :
- **id** (chaîne de deux chiffres '01'—'NN')
- **brand** (nom du client ou « projet personnel », « création indépendante »)
- **title** (titre concis de 4—12 caractères)
- **year** (nombre YYYY)
- **tags** (tableau, 1—3 mots anglais, ex. Identity / Editorial / Web / Installation / Poster / Sound / Motion / Print / Type / Packaging / Exhibition / Light)
- **img** (image de couverture, carrée 1080×1080)
- **hero** (image d'en-tête du détail, paysage 1600×1000)
- **g1, g2** (deux images d'appoint du détail, 800×600)
- **desc** (une phrase ~20—50 caractères, sous-titre de la page de détail secondaire)
- **long** (corps du détail, 2—3 paragraphes de 60—120 caractères)
- **spec** (4 lignes clé-valeur : `[['Client','xxx'],['Year','xxx'],['Scope','xxx'],['Duration / Pages / Edition','xxx']]`)

Si bio_text ne contient que des notes éparses sans histoires précises → **composer** de brefs récits cohérents avec l'ambiance, mais **sans inventer de noms de clients** (écrire 'Personal' / « création indépendante » / « initiative du studio »).

### 4. Nombre de WORKS
- Minimum **8 œuvres** (sinon l'écran est vide) ; en dessous, remplir par répétition : laisser `workFor()` boucler via mod
- Maximum **30 œuvres** (au-delà, inutile — la sphère répète)
- Recommandé **15—25 œuvres**

### 5. Remplacer les 12 SWAP

| SWAP | Emplacement | Contenu |
|---|---|---|
| 1 | `<title>` | `{STUDIO_NAME_CN} — {STUDIO_TYPE} · Index {YEAR}` |
| 2 | `.brand-block` (logo + texte en haut à gauche) | logo SVG personnalisé ou changer l'icône + « son [off] » modifiable ou conservé |
| 3 | `.tagline` (deux lignes au centre du bandeau) | `{TAGLINE}` phrase longue + `<br>` + conclusion courte |
| 4 | `.col-meta` (localisation en haut à droite) | 1—2 `<div class="row"><span class="loc-dot live"></span>{LOCATION}</div>` |
| 5 | `.col-times` (fuseaux en haut à droite) | `heure de Pékin UTC+8` / `<div id="time1">` laissé vide pour le JS / deuxième ligne `<div id="time2">` également vide |
| 6 | bouton `.cta` | `{CTA_TEXT}` |
| 7 | `.bottombar .tabs` | les trois textes de `<button class="tab">` (défaut `Œuvres / À propos / Parcours`) |
| 8 | `#overlay-about` | contenu about complet : eyebrow + titre + corps + domaines de compétence + membres |
| 9 | `#overlay-cv` | chronologie de projets par année + expositions/prix |
| 10 | `#overlay-contact` | 6 contact-cell : emails / adresses / réseaux / recrutement |
| 11 | `#overlay-filter` | trois groupes de cases : catégories / années / types de clients (dérivées de vos WORKS finaux) |
| 12 | `const WORKS = [...]` | le tableau WORKS complet |

### 6. Variantes de style (optionnel)

Palette par défaut (ambiance sombre « matériaux / studio ») :
```css
--bg: #0d0c0b;
--ink: #f0e9df;
--ink-soft: #8a8278;
--accent: #c89a5a;
```

Si l'utilisateur demande :
- **clair / façon magazine** → bg `#f4f1ec`, ink `#1a1714`, accent `#8a4a1a`
- **blanc minimaliste** → bg `#ffffff`, ink `#0a0a0a`, accent `#666666`
- **violet cyber** → bg `#0a0612`, ink `#e8d8ff`, accent `#9b6dff`
- **brun chaud rétro** → bg `#1f1610`, ink `#e8d4b6`, accent `#c8895a`

Ne modifier que les quatre variables de `:root` ; pas le layout / ni le JS.

### 7. Écrire les fichiers / sortir le HTML

**Mode A (Claude Code)** :
```
~/Desktop/{slug}-vr-canvas/
├── index.html
└── images/
    ├── work-01.jpg ... work-NN.jpg
    └── (hero / g1 / g2 sous les mêmes noms avec -hero / -g1 / -g2)
```
Le slug en pinyin du nom du studio avec tirets (xubai / mingchuan / li-ming).

**Mode B (GLM)** :
Sortir directement un HTML complet dans la réponse, dans un bloc ```html. Tous les `<img src>` en placeholders picsum ou URL fournies par l'utilisateur.

Terminer la réponse par :
> Enregistre ce qui précède en `index.html` et double-clique pour ouvrir. Pour changer les images, remplace `img / hero / g1 / g2` dans le tableau WORKS par tes adresses d'images.

### 8. Rapport

**Mode A** : une phrase avec chemin + nombre d'œuvres + style.
> Généré ~/Desktop/xubai-vr-canvas/index.html — 18 œuvres, palette sombre « matériaux ». Double-clique pour ouvrir : en promenant la souris, l'effet de rotation de tête VR apparaît ; appui long + glisser pour parcourir les autres œuvres, clic pour le détail.

**Mode B** : le bloc de code HTML directement + une ligne d'instructions.

## À conserver impérativement (ne jamais modifier)

- Tout le JS (projection sphérique / inertie du glisser / zoom molette / routage par hash / splash / tick d'horloge / inclinaison souris)
- Le CSS de `.work / .frame / .cell-head / .cell-foot / .num / .brand / .proj`
- Le CSS et la structure DOM de `.viewport / .sphere`
- `SPHERE_R = 1700 / STEP_DEG = 11 / ROW_HALF = 6` (paramètres cardinaux de la projection sphérique ; ne toucher à R que pour renforcer l'effet VR)
- La structure de `.overlay / .overlay-close / .info-pane / .info-section` (texte seulement, jamais les classes)
- `mix-blend-mode: difference` sur la topbar (c'est le cœur du langage design)

## Aide-mémoire des pièges

- **Images** : `img` doit être un carré 1080×1080 (les cellules sphériques sont carrées) ; hero du détail en paysage 1600×1000
- **Trop peu de WORKS** : 8 minimum ; sinon composer quelques « créations indépendantes / projets expérimentaux » dans la bio
- **Ne pas** écrire des `long` interminables (300+ caractères) pour toutes les œuvres — le rythme des vides compte plus que la densité d'information
- **Ne pas** toucher aux polices serif chinoises type `font-family: "Noto Serif SC"` (source de la texture « studio »)
- **Les trois overlays about / cv / contact sont obligatoires** : même sans informations fournies, composer un contenu plausible depuis la bio ; ne jamais laisser d'overlay vide
- **Les cases de l'overlay filter** sont décoratives (sans JS) mais doivent refléter les catégories et années réelles de WORKS
- **Portfolio personnel** (pas un studio) : team sur une seule ligne ; adresses remplacées par « indépendant · ville de travail »
