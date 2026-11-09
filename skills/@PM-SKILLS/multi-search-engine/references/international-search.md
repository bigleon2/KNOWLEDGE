# Guide de recherche approfondie sur les moteurs internationaux

## 🔍 Recherche approfondie Google

### 1.1 Opérateurs avancés de base

| Opérateur | Fonction | Exemple | URL |
|--------|------|------|-----|
| `""` | correspondance exacte | `"machine learning"` | `https://www.google.com/search?q=%22machine+learning%22` |
| `-` | exclure un mot-clé | `python -snake` | `https://www.google.com/search?q=python+-snake` |
| `OR` | ou logique | `machine learning OR deep learning` | `https://www.google.com/search?q=machine+learning+OR+deep+learning` |
| `*` | joker | `machine * algorithms` | `https://www.google.com/search?q=machine+*+algorithms` |
| `()` | groupement | `(apple OR microsoft) phones` | `https://www.google.com/search?q=(apple+OR+microsoft)+phones` |
| `..` | plage numérique | `laptop $500..$1000` | `https://www.google.com/search?q=laptop+%24500..%241000` |

### 1.2 Recherche par site et par fichier

| Opérateur | Fonction | Exemple |
|--------|------|------|
| `site:` | recherche dans un site | `site:github.com python projects` |
| `filetype:` | type de fichier | `filetype:pdf annual report` |
| `inurl:` | contenu de l'URL | `inurl:login admin` |
| `intitle:` | contenu du titre | `intitle:"index of" mp3` |
| `intext:` | contenu du corps | `intext:password filetype:txt` |
| `cache:` | voir le cache | `cache:example.com` |
| `related:` | sites similaires | `related:github.com` |
| `info:` | informations sur un site | `info:example.com` |

### 1.3 Paramètres de filtrage temporel

| Paramètre | Signification | Exemple d'URL |
|------|------|---------|
| `tbs=qdr:h` | dernière heure | `https://www.google.com/search?q=news&tbs=qdr:h` |
| `tbs=qdr:d` | dernières 24 heures | `https://www.google.com/search?q=news&tbs=qdr:d` |
| `tbs=qdr:w` | dernière semaine | `https://www.google.com/search?q=news&tbs=qdr:w` |
| `tbs=qdr:m` | dernier mois | `https://www.google.com/search?q=news&tbs=qdr:m` |
| `tbs=qdr:y` | dernière année | `https://www.google.com/search?q=news&tbs=qdr:y` |
| `tbs=cdr:1,cd_min:1/1/2024,cd_max:12/31/2024` | plage de dates personnalisée | toute l'année 2024 |

### 1.4 Filtres de langue et de région

| Paramètre | Fonction | Exemple |
|------|------|------|
| `hl=en` | langue de l'interface | `https://www.google.com/search?q=test&hl=en` |
| `lr=lang_zh-CN` | langue des résultats | `https://www.google.com/search?q=test&lr=lang_zh-CN` |
| `cr=countryCN` | pays/région | `https://www.google.com/search?q=test&cr=countryCN` |
| `gl=us` | localisation | `https://www.google.com/search?q=test&gl=us` |

### 1.5 Types de recherche spéciaux

| Type | URL | Note |
|------|-----|------|
| Recherche d'images | `https://www.google.com/search?q={keyword}&tbm=isch` | `tbm=isch` pour les images |
| Recherche d'actualités | `https://www.google.com/search?q={keyword}&tbm=nws` | `tbm=nws` pour les actualités |
| Recherche de vidéos | `https://www.google.com/search?q={keyword}&tbm=vid` | `tbm=vid` pour les vidéos |
| Recherche cartographique | `https://www.google.com/search?q={keyword}&tbm=map` | `tbm=map` pour les cartes |
| Recherche shopping | `https://www.google.com/search?q={keyword}&tbm=shop` | `tbm=shop` pour le shopping |
| Recherche de livres | `https://www.google.com/search?q={keyword}&tbm=bks` | `tbm=bks` pour les livres |
| Recherche académique | `https://scholar.google.com/scholar?q={keyword}` | Google Scholar |

### 1.6 Exemples de recherche avancée Google

```javascript
// 1. Chercher des projets Python de machine learning sur GitHub
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+machine+learning"})

// 2. Chercher des tutos machine learning en PDF de 2024
web_fetch({"url": "https://www.google.com/search?q=machine+learning+tutorial+filetype:pdf&tbs=cdr:1,cd_min:1/1/2024"})

// 3. Chercher des pages Python dont le titre contient « tutorial »
web_fetch({"url": "https://www.google.com/search?q=intitle:tutorial+python"})

// 4. Chercher les actualités de la semaine
web_fetch({"url": "https://www.google.com/search?q=AI+breakthrough&tbs=qdr:w&tbm=nws"})

// 5. Chercher du contenu chinois (interface anglaise, résultats chinois)
web_fetch({"url": "https://www.google.com/search?q=人工智能&lr=lang_zh-CN&hl=en"})

// 6. Chercher des ordinateurs portables dans une fourchette de prix
web_fetch({"url": "https://www.google.com/search?q=laptop+%241000..%242000+best+rating"})

// 7. Exclure Wikipedia des résultats
web_fetch({"url": "https://www.google.com/search?q=python+programming+-wikipedia"})

// 8. Chercher de la littérature académique
web_fetch({"url": "https://scholar.google.com/scholar?q=deep+learning+optimization"})

// 9. Voir la page en cache (contenu supprimé)
web_fetch({"url": "https://webcache.googleusercontent.com/search?q=cache:example.com"})

// 10. Chercher des sites similaires
web_fetch({"url": "https://www.google.com/search?q=related:stackoverflow.com"})
```

---

## 🦆 Recherche approfondie DuckDuckGo

### 2.1 Fonctions phares de DuckDuckGo

| Fonction | Syntaxe | Exemple |
|------|------|------|
| **Bangs, raccourcis** | `!abbr` | `!g python` → recherche Google |
| **Génération de mot de passe** | `password` | `https://duckduckgo.com/?q=password+20` |
| **Conversion de couleur** | `color` | `https://duckduckgo.com/?q=+%23FF5733` |
| **Liens courts** | `shorten` | `https://duckduckgo.com/?q=shorten+example.com` |
| **Génération de QR code** | `qr` | `https://duckduckgo.com/?q=qr+hello+world` |
| **Génération d'UUID** | `uuid` | `https://duckduckgo.com/?q=uuid` |
| **Encodage/décodage Base64** | `base64` | `https://duckduckgo.com/?q=base64+hello` |

### 2.2 Liste complète des Bangs DuckDuckGo

#### Moteurs de recherche

| Bang | Destination | Exemple |
|------|---------|------|
| `!g` | Google | `!g python tutorial` |
| `!b` | Bing | `!b weather` |
| `!y` | Yahoo | `!y finance` |
| `!sp` | Startpage | `!sp privacy` |
| `!brave` | Brave Search | `!brave tech` |

#### Développement

| Bang | Destination | Exemple |
|------|---------|------|
| `!gh` | GitHub | `!gh tensorflow` |
| `!so` | Stack Overflow | `!so javascript error` |
| `!npm` | npmjs.com | `!npm express` |
| `!pypi` | PyPI | `!pypi requests` |
| `!mdn` | MDN Web Docs | `!mdn fetch api` |
| `!docs` | DevDocs | `!docs python` |
| `!docker` | Docker Hub | `!docker nginx` |

#### Encyclopédies et savoir

| Bang | Destination | Exemple |
|------|---------|------|
| `!w` | Wikipédia | `!w machine learning` |
| `!wen` | Wikipédia anglais | `!wen artificial intelligence` |
| `!wt` | Wiktionnaire | `!wt serendipity` |
| `!imdb` | IMDb | `!imdb inception` |

#### Achats et prix

| Bang | Destination | Exemple |
|------|---------|------|
| `!a` | Amazon | `!a wireless headphones` |
| `!e` | eBay | `!e vintage watch` |
| `!ali` | AliExpress | `!ali phone case` |

#### Cartes et lieux

| Bang | Destination | Exemple |
|------|---------|------|
| `!m` | Google Maps | `!m Beijing` |
| `!maps` | OpenStreetMap | `!maps Paris` |

### 2.3 Paramètres de recherche DuckDuckGo

| Paramètre | Fonction | Exemple |
|------|------|------|
| `kp=1` | recherche sécurisée stricte | `https://duckduckgo.com/html/?q=test&kp=1` |
| `kp=-1` | recherche sécurisée désactivée | `https://duckduckgo.com/html/?q=test&kp=-1` |
| `kl=cn` | région Chine | `https://duckduckgo.com/html/?q=news&kl=cn` |
| `kl=us-en` | États-Unis anglais | `https://duckduckgo.com/html/?q=news&kl=us-en` |
| `ia=web` | résultats web | `https://duckduckgo.com/?q=test&ia=web` |
| `ia=images` | résultats images | `https://duckduckgo.com/?q=test&ia=images` |
| `ia=news` | résultats actualités | `https://duckduckgo.com/?q=test&ia=news` |
| `ia=videos` | résultats vidéos | `https://duckduckgo.com/?q=test&ia=videos` |

### 2.4 Exemples de recherche avancée DuckDuckGo

```javascript
// 1. Utiliser un Bang pour sauter vers Google
web_fetch({"url": "https://duckduckgo.com/html/?q=!g+machine+learning"})

// 2. Chercher directement un projet sur GitHub
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+react"})

// 3. Trouver une réponse Stack Overflow
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+python+list+comprehension"})

// 4. Générer un mot de passe
web_fetch({"url": "https://duckduckgo.com/?q=password+16"})

// 5. Encoder en Base64
web_fetch({"url": "https://duckduckgo.com/?q=base64+hello+world"})

// 6. Convertir un code couleur
web_fetch({"url": "https://duckduckgo.com/?q=%23FF5733"})

// 7. Chercher des vidéos YouTube
web_fetch({"url": "https://duckduckgo.com/html/?q=!yt+python+tutorial"})

// 8. Consulter Wikipédia
web_fetch({"url": "https://duckduckgo.com/html/?q=!w+artificial+intelligence"})

// 9. Chercher un produit sur Amazon
web_fetch({"url": "https://duckduckgo.com/html/?q=!a+laptop"})

// 10. Générer un QR code
web_fetch({"url": "https://duckduckgo.com/?q=qr+https://github.com"})
```

---

## 🔎 Recherche approfondie Brave Search

### 3.1 Fonctions phares de Brave Search

| Fonction | Paramètre | Exemple |
|------|------|------|
| **Index indépendant** | sans dépendance Google/Bing | index de ses propres crawlers |
| **Goggles** | règles de recherche personnalisées | créer des filtres sur mesure |
| **Discussions** | recherche dans les forums | agrège Reddit et autres forums |
| **News** | agrégation d'actualités | index d'actualités indépendant |

### 3.2 Paramètres Brave Search

| Paramètre | Fonction | Exemple |
|------|------|------|
| `tf=pw` | cette semaine | `https://search.brave.com/search?q=news&tf=pw` |
| `tf=pm` | ce mois | `https://search.brave.com/search?q=tech&tf=pm` |
| `tf=py` | cette année | `https://search.brave.com/search?q=AI&tf=py` |
| `safesearch=strict` | sécurité stricte | `https://search.brave.com/search?q=test&safesearch=strict` |
| `source=web` | recherche web | par défaut |
| `source=news` | recherche actualités | `https://search.brave.com/search?q=tech&source=news` |
| `source=images` | recherche images | `https://search.brave.com/search?q=cat&source=images` |
| `source=videos` | recherche vidéos | `https://search.brave.com/search?q=music&source=videos` |

### 3.3 Brave Search Goggles (filtres personnalisés)

Les Goggles permettent de créer des règles de recherche sur mesure :

```
$discard  // tout rejeter
$boost,site=stackoverflow.com  // favoriser Stack Overflow
$boost,site=github.com  // favoriser GitHub
$boost,site=docs.python.org  // favoriser la documentation Python
```

### 3.4 Exemples de recherche avancée Brave Search

```javascript
// 1. Actualités tech de la semaine
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw&source=news"})

// 2. Progrès de l'IA ce mois-ci
web_fetch({"url": "https://search.brave.com/search?q=artificial+intelligence&tf=pm"})

// 3. Recherche d'images
web_fetch({"url": "https://search.brave.com/search?q=machine+learning&source=images"})

// 4. Tutoriels vidéo
web_fetch({"url": "https://search.brave.com/search?q=python+tutorial&source=videos"})

// 5. Recherche sur l'index indépendant
web_fetch({"url": "https://search.brave.com/search?q=privacy+tools"})
```

---

## 📊 WolframAlpha, recherche calculée sur les connaissances

### 4.1 Types de données WolframAlpha

| Type | Exemple de requête | URL |
|------|---------|-----|
| **Calcul mathématique** | `integrate x^2 dx` | `https://www.wolframalpha.com/input?i=integrate+x%5E2+dx` |
| **Conversion d'unités** | `100 miles to km` | `https://www.wolframalpha.com/input?i=100+miles+to+km` |
| **Conversion de devises** | `100 USD to CNY` | `https://www.wolframalpha.com/input?i=100+USD+to+CNY` |
| **Données boursières** | `AAPL stock` | `https://www.wolframalpha.com/input?i=AAPL+stock` |
| **Météo** | `weather in Beijing` | `https://www.wolframalpha.com/input?i=weather+in+Beijing` |
| **Données de population** | `population of China` | `https://www.wolframalpha.com/input?i=population+of+China` |
| **Éléments chimiques** | `properties of gold` | `https://www.wolframalpha.com/input?i=properties+of+gold` |
| **Valeurs nutritionnelles** | `nutrition of apple` | `https://www.wolframalpha.com/input?i=nutrition+of+apple` |
| **Calcul de dates** | `days between Jan 1 2020 and Dec 31 2024` | intervalle entre deux dates |
| **Fuseaux horaires** | `10am Beijing to New York` | conversion de fuseau |
| **Adresse IP** | `8.8.8.8` | informations IP |
| **Code-barres** | `scan barcode 123456789` | informations code-barres |
| **Vols aériens** | `flight AA123` | informations de vol |

### 4.2 Exemples de recherche avancée WolframAlpha

```javascript
// 1. Calculer une intégrale
web_fetch({"url": "https://www.wolframalpha.com/input?i=integrate+sin%28x%29+from+0+to+pi"})

// 2. Résoudre une équation
web_fetch({"url": "https://www.wolframalpha.com/input?i=solve+x%5E2-5x%2B6%3D0"})

// 3. Taux de change en temps réel
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})

// 4. Données boursières en temps réel
web_fetch({"url": "https://www.wolframalpha.com/input?i=Apple+stock+price"})

// 5. Météo d'une ville
web_fetch({"url": "https://www.wolframalpha.com/input?i=weather+in+Shanghai+tomorrow"})

// 6. Statistiques par pays
web_fetch({"url": "https://www.wolframalpha.com/input?i=GDP+of+China+vs+USA"})

// 7. Calcul chimique
web_fetch({"url": "https://www.wolframalpha.com/input?i=molar+mass+of+H2SO4"})

// 8. Constantes physiques
web_fetch({"url": "https://www.wolframalpha.com/input?i=speed+of+light"})

// 9. Informations nutritionnelles
web_fetch({"url": "https://www.wolframalpha.com/input?i=calories+in+banana"})

// 10. Dates historiques
web_fetch({"url": "https://www.wolframalpha.com/input?i=events+on+July+20+1969"})
```

---

## 🔧 Startpage, recherche orientée confidentialité

### 5.1 Fonctions phares de Startpage

| Fonction | Description | URL |
|------|------|-----|
| **Navigation par procuration** | accès anonyme aux résultats | cliquer « voir anonymement » |
| **Aucun pistage** | pas d'historique de recherche | activé par défaut |
| **Serveurs UE** | protégé par le droit européen | données en Europe |
| **Images par procuration** | chargement des images via proxy | masque l'IP |

### 5.2 Paramètres Startpage

| Paramètre | Fonction | Exemple |
|------|------|------|
| `cat=web` | recherche web | par défaut |
| `cat=images` | recherche images | `...&cat=images` |
| `cat=video` | recherche vidéos | `...&cat=video` |
| `cat=news` | recherche actualités | `...&cat=news` |
| `language=english` | résultats en anglais | `...&language=english` |
| `time=day` | dernières 24 heures | `...&time=day` |
| `time=week` | dernière semaine | `...&time=week` |
| `time=month` | dernier mois | `...&time=month` |
| `time=year` | dernière année | `...&time=year` |
| `nj=0` | désactiver le filtre famille | `...&nj=0` |

### 5.3 Exemples de recherche avancée Startpage

```javascript
// 1. Recherche privée
web_fetch({"url": "https://www.startpage.com/sp/search?query=privacy+tools"})

// 2. Recherche d'images privée
web_fetch({"url": "https://www.startpage.com/sp/search?query=nature&cat=images"})

// 3. Actualités de la semaine (mode privé)
web_fetch({"url": "https://www.startpage.com/sp/search?query=tech+news&time=week&cat=news"})

// 4. Recherche de résultats en anglais
web_fetch({"url": "https://www.startpage.com/sp/search?query=machine+learning&language=english"})
```

---

## 🌍 Stratégies de recherche combinées

### 6.1 Choisir le moteur selon l'objectif

| Objectif | Moteur principal | Alternatives | Raison |
|---------|---------|---------|------|
| **Recherche académique** | Google Scholar | Google, Brave | index de ressources académiques |
| **Développement** | Google | GitHub (bang DuckDuckGo) | documentation technique exhaustive |
| **Confidentialité** | DuckDuckGo | Startpage, Brave | aucun pistage |
| **Actualités en temps réel** | Brave News | Google News | index d'actualités indépendant |
| **Calcul de savoir** | WolframAlpha | Google | données structurées |
| **Contenu chinois** | Google HK | Bing | bonne optimisation chinois |
| **Regard européen** | Qwant | Startpage | conformité UE |
| **Soutien écologique** | Ecosia | DuckDuckGo | un arbre planté par recherche |
| **Sans filtrage** | Brave | Startpage | résultats sans biais |

### 6.2 Vérification croisée multi-moteurs

```javascript
// Stratégie : chercher le même mot-clé sur plusieurs moteurs et comparer
const keyword = "climate change 2024";

// Obtenir des perspectives différentes
const searches = [
  { engine: "Google", url: `https://www.google.com/search?q=${keyword}&tbs=qdr:m` },
  { engine: "Brave", url: `https://search.brave.com/search?q=${keyword}&tf=pm` },
  { engine: "DuckDuckGo", url: `https://duckduckgo.com/html/?q=${keyword}` },
  { engine: "Ecosia", url: `https://www.ecosia.org/search?q=${keyword}` }
];

// Analyser les différences de résultats entre moteurs
```

### 6.3 Stratégies de recherche selon la fraîcheur

| Exigence de fraîcheur | Choix de moteurs | Paramètres |
|-----------|---------|---------|
| **Temps réel (heure)** | Google News, Brave News | `tbs=qdr:h`, `tf=pw` |
| **Récent (jour)** | Google, Brave | `tbs=qdr:d`, `time=day` |
| **Cette semaine** | tous | `tbs=qdr:w`, `tf=pw` |
| **Ce mois** | tous | `tbs=qdr:m`, `tf=pm` |
| **Historique** | Google Scholar | archives académiques |

### 6.4 Recherche approfondie par domaine

#### Développement technique

```javascript
// Recherche de projets GitHub
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+tensorflow+stars:%3E1000"})

// Questions Stack Overflow
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+python+memory+leak"})

// Documentation MDN
web_fetch({"url": "https://duckduckgo.com/html/?q=!mdn+javascript+async+await"})

// Paquets PyPI
web_fetch({"url": "https://duckduckgo.com/html/?q=!pypi+requests"})

// Paquets npm
web_fetch({"url": "https://duckduckgo.com/html/?q=!npm+express"})
```

#### Recherche académique

```javascript
// Publications Google Scholar
web_fetch({"url": "https://scholar.google.com/scholar?q=deep+learning+2024"})

// Chercher des articles PDF
web_fetch({"url": "https://www.google.com/search?q=machine+learning+filetype:pdf+2024"})

// Articles arXiv
web_fetch({"url": "https://duckduckgo.com/html/?q=site:arxiv.org+quantum+computing"})
```

#### Finance et investissement

```javascript
// Données boursières en temps réel
web_fetch({"url": "https://www.wolframalpha.com/input?i=AAPL+stock"})

// Conversion de devises
web_fetch({"url": "https://www.wolframalpha.com/input?i=EUR+to+USD"})

// Chercher un rapport financier PDF
web_fetch({"url": "https://www.google.com/search?q=Apple+Q4+2024+earnings+filetype:pdf"})
```

#### Actualités

```javascript
// Google Actualités
web_fetch({"url": "https://www.google.com/search?q=breaking+news&tbm=nws&tbs=qdr:h"})

// Brave Actualités
web_fetch({"url": "https://search.brave.com/search?q=world+news&source=news"})

// DuckDuckGo Actualités
web_fetch({"url": "https://duckduckgo.com/html/?q=tech+news&ia=news"})
```

---

## 🛠️ Récapitulatif des techniques avancées

### Fonction utilitaire d'encodage URL

```javascript
// Encoder un mot-clé en URL
function encodeKeyword(keyword) {
  return encodeURIComponent(keyword);
}

// Exemple
const keyword = "machine learning";
const encoded = encodeKeyword(keyword); // "machine%20learning"
```

### Gabarit de recherche en lot

```javascript
// Fonction de génération d'URL multi-moteurs
function generateSearchUrls(keyword) {
  const encoded = encodeURIComponent(keyword);
  return {
    google: `https://www.google.com/search?q=${encoded}`,
    google_hk: `https://www.google.com.hk/search?q=${encoded}`,
    duckduckgo: `https://duckduckgo.com/html/?q=${encoded}`,
    brave: `https://search.brave.com/search?q=${encoded}`,
    startpage: `https://www.startpage.com/sp/search?query=${encoded}`,
    bing_intl: `https://cn.bing.com/search?q=${encoded}&ensearch=1`,
    yahoo: `https://search.yahoo.com/search?p=${encoded}`,
    ecosia: `https://www.ecosia.org/search?q=${encoded}`,
    qwant: `https://www.qwant.com/?q=${encoded}`
  };
}

// Exemple d'usage
const urls = generateSearchUrls("artificial intelligence");
```

### Fonction rapide de filtrage temporel

```javascript
// Générateur d'URL Google avec filtre temporel
function googleTimeSearch(keyword, period) {
  const periods = {
    hour: 'qdr:h',
    day: 'qdr:d',
    week: 'qdr:w',
    month: 'qdr:m',
    year: 'qdr:y'
  };
  return `https://www.google.com/search?q=${encodeURIComponent(keyword)}&tbs=${periods[period]}`;
}

// Exemple d'usage
const recentNews = googleTimeSearch("AI breakthrough", "week");
```

---

## 📝 Recueil complet d'exemples de recherche

```javascript
// ==================== Développement technique ====================

// 1. Chercher des projets Python très étoilés sur GitHub
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+stars:%3E1000"})

// 2. Meilleures réponses Stack Overflow
web_fetch({"url": "https://duckduckgo.com/html/?q=!so+best+way+to+learn+python"})

// 3. Requête documentation MDN
web_fetch({"url": "https://duckduckgo.com/html/?q=!mdn+promises"})

// 4. Chercher un paquet npm
web_fetch({"url": "https://duckduckgo.com/html/?q=!npm+axios"})

// ==================== Recherche académique ====================

// 5. Publications Google Scholar
web_fetch({"url": "https://scholar.google.com/scholar?q=transformer+architecture"})

// 6. Chercher un article PDF
web_fetch({"url": "https://www.google.com/search?q=attention+is+all+you+need+filetype:pdf"})

// 7. Derniers articles arXiv
web_fetch({"url": "https://duckduckgo.com/html/?q=site:arxiv.org+abs+quantum"})

// ==================== Actualités ====================

// 8. Dernières actualités Google (dernière heure)
web_fetch({"url": "https://www.google.com/search?q=breaking+news&tbs=qdr:h&tbm=nws"})

// 9. Actualités tech de la semaine sur Brave
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw&source=news"})

// 10. Actualités DuckDuckGo
web_fetch({"url": "https://duckduckgo.com/html/?q=world+news&ia=news"})

// ==================== Finance et investissement ====================

// 11. Données boursières en temps réel
web_fetch({"url": "https://www.wolframalpha.com/input?i=Tesla+stock"})

// 12. Taux de change
web_fetch({"url": "https://www.wolframalpha.com/input?i=1+BTC+to+USD"})

// 13. Rapport annuel PDF d'une société
web_fetch({"url": "https://www.google.com/search?q=Microsoft+annual+report+2024+filetype:pdf"})

// ==================== Calcul de savoir ====================

// 14. Calcul mathématique
web_fetch({"url": "https://www.wolframalpha.com/input?i=derivative+of+x%5E3+sin%28x%29"})

// 15. Conversion d'unités
web_fetch({"url": "https://www.wolframalpha.com/input?i=convert+100+miles+to+kilometers"})

// 16. Informations nutritionnelles
web_fetch({"url": "https://www.wolframalpha.com/input?i=protein+in+chicken+breast"})

// ==================== Recherche et confidentialité ====================

// 17. Recherche privée DuckDuckGo
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// 18. Recherche anonyme Startpage
web_fetch({"url": "https://www.startpage.com/sp/search?query=secure+messaging"})

// 19. Recherche sans pistage Brave
web_fetch({"url": "https://search.brave.com/search?q=encryption+software"})

// ==================== Recherches combinées avancées ====================

// 20. Recherche Google multi-conditions et exacte
web_fetch({"url": "https://www.google.com/search?q=%22machine+learning%22+site:github.com+filetype:pdf+2024"})

// 21. Recherche excluant des sites précis
web_fetch({"url": "https://www.google.com/search?q=python+tutorial+-wikipedia+-w3schools"})

// 22. Recherche par fourchette de prix
web_fetch({"url": "https://www.google.com/search?q=laptop+%24800..%241200+best+review"})

// 23. Saut rapide par Bangs
web_fetch({"url": "https://duckduckgo.com/html/?q=!g+site:medium.com+python"})

// 24. Recherche d'images (Google)
web_fetch({"url": "https://www.google.com/search?q=beautiful+landscape&tbm=isch"})

// 25. Recherche de citations académiques
web_fetch({"url": "https://scholar.google.com/scholar?q=author:%22Geoffrey+Hinton%22"})
```

---

## 🔐 Bonnes pratiques de confidentialité

### Niveau de confidentialité des moteurs

| Moteur | Niveau de pistage | Conservation des données | Chiffrement | Scénario recommandé |
|------|---------|---------|------|---------|
| **DuckDuckGo** | aucun pistage | aucune conservation | oui | recherche privée quotidienne |
| **Startpage** | aucun pistage | aucune conservation | oui | résultats Google sans compromettre sa vie privée |
| **Brave** | aucun pistage | aucune conservation | oui | index indépendant, sans biais |
| **Qwant** | aucun pistage | aucune conservation | oui | exigences de conformité UE |
| **Google** | pistage élevé | conservation longue | oui | résultats personnalisés |
| **Bing** | pistage modéré | conservation longue | oui | intégration aux services Microsoft |

### Conseils de recherche confidentielle

1. **Usage quotidien** : DuckDuckGo ou Brave
2. **Résultats Google sans compromettre sa vie privée** : Startpage
3. **Recherche académique** : Google Scholar (pistage réduit pour un usage académique)
4. **Requêtes sensibles** : navigateur Tor + service onion DuckDuckGo
5. **Synchronisation multi-appareils** : éviter de se connecter à son compte de moteur de recherche

---

## 📚 Références

- [Liste complète des opérateurs Google](https://support.google.com/websearch/answer/...)
- [Liste complète des Bangs DuckDuckGo](https://duckduckgo.com/bang)
- [Documentation Brave Search](https://search.brave.com/help/...)
- [Exemples WolframAlpha](https://www.wolframalpha.com/examples/)
