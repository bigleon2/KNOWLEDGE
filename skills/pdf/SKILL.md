---
name: pdf
version: "1.1.0"
category: "Documents & Contenu"
tags:
  - pdf
metadata:
  author: Z.AI
  version: "1.1"
description: "Boîte à outils PDF professionnelle avec quatre lignes de production : (1) Report - documents structurés via ReportLab (rapports, propositions, contrats, livres blancs) ; (2) Creative - design visuel via JSON Blueprint → design_engine.py → capture Playwright (posters, infographies, invitations, dashboards). Le LLM agit comme directeur artistique et ne produit QUE des blueprints spatiaux JSON ; convert.blueprint compile en un PDF au pixel près. (3) Academic - travaux académiques via LaTeX/Tectonic (articles, thèses, documents très mathématiques) ; (4) Process - manipuler des PDFs existants (extraire, fusionner, découper, remplir des formulaires, convertir) ; routage automatique selon le type de document. Inclut des sous-chemins de CV ATS/creative/academic."
license: Proprietary. LICENSE.txt has complete terms
language: fr

read_when:
  - Déclencher quand la demande concerne : "Boîte à outils PDF professionnelle avec quatre lignes de production : (1) Report - documents structurés via R…
  - Déclencher si la demande mentionne : documents, creative, design
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# PDF - Atelier de production de documents

## Configuration des chemins de scripts (OBLIGATOIRE avant tout appel de script)

Tous les chemins sont relatifs à `$PDF_SKILL_DIR`. Résolvez-le une fois avant d'appeler tout script :

```bash
PDF_SKILL_DIR="<skill_directory>"   # ← parent directory of this SKILL.md
```

**Pour les imports Python** (quand le code de génération doit importer les modules du skill) :

```python
import sys, os
PDF_SKILL_DIR = "<skill_directory>"
_scripts = os.path.join(PDF_SKILL_DIR, "scripts")
if _scripts not in sys.path:
    sys.path.insert(0, _scripts)
```

## Tri

Déterminez le poids de la tâche pour contrôler la quantité de contexte à charger :

| Poids | Déclencheurs | À charger |
|--------|----------|--------------|
| **Léger** | Conversion de format, remplissage de formulaire, extraction de texte, fusion/découpe, certificat simple | SKILL.md + `briefs/process.md` uniquement |
| **Standard** | Rapport multi-pages, poster, article académique, CV, reformatage - tout document impliquant des décisions de design | SKILL.md + `configs/fonts.md` + brief correspondant + **TOUS les fichiers référencés par le brief** (typesetting, configs, etc.) |

### ⚠️ Vérifications pré-routage (à exécuter AVANT de choisir le brief)

1. **Vérification emoji** - Scannez le contenu de l'utilisateur à la recherche d'emojis intentionnels (décoratifs 📊🎯🔥, pas des emojis saisis au niveau OS). Si trouvés → **forcez le pipeline Creative** (Fixed-Canvas ou Flow selon le type de document) quel que soit le routage initial. ReportLab rend les emojis en carrés □ ; LaTeX les supprime purement et simplement.
2. **Vérification CJK** - Le contenu chinois/japonais/coréen nécessite une couverture de polices. Le brief Report doit enregistrer des polices CJK - **sondez d'abord** avec `ls /usr/share/fonts/truetype/chinese/` (Linux) ou vérifiez `$FONT_DIR` (macOS) pour confirmer quelles polices existent, puis enregistrez en conséquence (préférez NotoSerifSC > Noto Sans SC ; ne codez jamais en dur un nom de police sans vérifier son existence). Les briefs Creative Fixed-Canvas et Creative Flow doivent charger la police Google Fonts Noto Sans SC avec `font-display: swap` ; le brief Academic doit utiliser `\usepackage{ctex}`.
3. **Vérification des dimensions** - Tailles de page non standard (autres que A4/Letter/A3) → préférez le brief Creative (Playwright gère toute dimension). ReportLab peut faire des tailles personnalisées mais la pagination est manuelle.
4. **Vérification de sécurité des caractères** - Avant d'écrire toute chaîne de contenu, scannez les kana japonais (の、が、は etc.), les symboles Unicode inhabituels ou les caractères non-CJK susceptibles d'être corrompus pendant le transit d'encodage (surtout quand le code est écrit via heredoc/base64/sortie LLM). Remplacez par des équivalents chinois simples : `の`→`之/的/缔`, `々`→omis ou écrire le caractère complet. **Si le contenu doit préserver le japonais, utilisez uniquement les idéogrammes CJK unifiés standards (U+4E00-U+9FFF) et les kana courants ; évitez les points de code rares/à usage privé.**

---

## Briefing

Faites correspondre l'intention de l'utilisateur à un brief de production. Chaque brief contient le workflow complet, les spécificités de la pile technique et les références aux ressources de mise en page partagées.

```
User Request
│
├─ Work with existing PDF? ─────────────┬─ Extract/merge/split/fill/convert → briefs/process.md
│                                       ├─ Reformat/redesign → briefs/process.md (extract) → delegate to report or creative brief
│                                       └─ User provides a PDF template/reference to match style
│                                          → briefs/process.md "Template-Guided Reformat" → delegate to matched brief
│
├─ Report / proposal / white paper / contract / analysis?
│  └─ ────────────────────────────────── → briefs/report.md   (ReportLab)
│
├─ Poster / invitation / infographic / dashboard / creative layout?
│  └─ ────────────────────────────────── → briefs/creative-fixed-canvas.md  (Playwright, fixed-canvas)
│
├─ Guide / handbook / catalog / introduction / collection (text-heavy + design)?
│  └─ ────────────────────────────────── → briefs/creative-flow.md  (Playwright, flowing content)
│
├─ Academic paper / thesis / math / IEEE / ACM / LaTeX?
│  └─ ────────────────────────────────── → briefs/academic.md  (Tectonic)
│
├─ Math-heavy doc / TikZ diagram / algorithm pseudocode / Beamer slides?
│  └─ ────────────────────────────────── → briefs/academic.md  (Tectonic, Scenarios A-D)
│
├─ Document needs complex embedded diagrams (flowcharts, architecture, neural nets)?
│  └─ Route by target brief:
│     ├─ Report → Playwright+CSS → PNG → ReportLab Image() flowable
│     ├─ Creative → directly in HTML (CSS flexbox/grid + connectors)
│     └─ Academic → complexity-based:
│        ├─ Simple (≤6 nodes, linear/tree) → TikZ native (vector)
│        └─ Complex (>6 nodes, branches, annotations) → Playwright+CSS → PNG → \includegraphics
│
└─ Resume / CV?
   ├─ ATS-safe / corporate ─────────── → briefs/resume.md
   ├─ Creative / design industry ────── → briefs/creative-fixed-canvas.md   (resume sub-section)
   └─ Academic CV / publications ────── → briefs/academic.md   (resume sub-section)
```

### Mots-clés de détection

| Brief | Mots-clés |
|-------|----------|
| Report | rapport, report, analyse, analysis, livre blanc, white paper, proposition, proposal, contrat, contract, plan, planning, facture, invoice, reçu, receipt, examen, exam, quiz, test paper, exercice, exercise, feuille d'exercices, worksheet, test, interrogation |
| Creative Fixed-Canvas | poster, poster, invitation, invitation, infographie, infographic, tableau de bord, dashboard, flyer, flyer, certificat, certificate, menu, menu, carte de visite, business card, distinction, award, étiquette, label, enveloppe, envelope, carte de vœux, greeting card → `briefs/creative-fixed-canvas.md` |
| Creative (Poster) | poster, poster, flyer, flyer, prospectus, leaflet → charger en plus les règles de scène `briefs/poster.md` par-dessus creative-fixed-canvas.md |
| Creative Flow | guide, guide, manuel, handbook, catalogue, catalog, introduction, introduction, collection, collection → `briefs/creative-flow.md` |
| Academic | article, paper, académique, academic, LaTeX, mathématiques, math, IEEE, ACM, thèse, thesis, recherche, research, Beamer, slides, rapport de projet, diplôme, dissertation, proposal |
| Process | extraire, extract, fusionner, merge, découper, split, remplir, fill, convertir, convert, OCR, reformater, reformat, redesign, template, template, suis ce style, match this style, compresser, compress, filigrane, watermark, chiffrer, encrypt, signer, sign |

### Matrice complète de routage des scénarios

Voici une cartographie exhaustive de chaque type de demande PDF connue vers sa stratégie de traitement. Si un scénario n'est pas listé, routez vers la correspondance la plus proche ou demandez à l'utilisateur.

#### Création (Générer un PDF à partir de zéro)

| Scénario | Route | Notes |
|----------|-------|-------|
| Rapport / livre blanc / analyse | report.md | Document structuré ReportLab |
| Rapport avec emojis | **creative-fixed-canvas.md** | Priorité à la règle emoji |
| Proposition commerciale | report.md | Structuré + tableaux de données |
| Contrat / document juridique | report.md | Ajouter des emplacements de signature (ligne pointillée + libellé) |
| Facture / reçu | report.md | Lourd en tableaux, alignement précis |
| Examen / quiz / sujet de test / feuille d'exercices | report.md | Options en retrait, réservation d'espace réponse, numérotation structurée (voir Exam Paper Rules dans report.md) |
| Examen de maths / feuille de maths (avec formules/équations) | academic.md | LaTeX pour une composition mathématique correcte. Voir §Exam Paper Rules dans academic.md |
| Poster / flyer | creative-fixed-canvas.md + **poster.md** | Design visuel + règles de densité/dimensionnement poster |
| Invitation / carte de vœux | creative-fixed-canvas.md | Taille non standard, décoratif |
| Certificat / distinction | creative-fixed-canvas.md | Page unique, mise en page centrée, bordure décorative |
| Carte de visite | creative-fixed-canvas.md | Très petit format (90×54 mm), support natif Playwright |
| Enveloppe / étiquette | creative-fixed-canvas.md | Taille non standard, mise en page simple |
| Menu / liste de prix | creative-fixed-canvas.md | Mise en page visuelle + peut contenir des emojis |
| CV (ATS) | resume.md | Structure en texte brut |
| CV (créatif) | creative-fixed-canvas.md | Design visuel |
| CV (académique) | academic.md | Liste de publications + BibTeX |
| Article académique | academic.md | LaTeX/Tectonic |
| Document très mathématique | academic.md | Composition LaTeX |
| Présentation / style PPT | creative-fixed-canvas.md | Paysage (1280×720), un sujet par page |
| Livre / document long | report.md | Ajouter sommaire + numérotation des chapitres, valider avec toc_validate.py |
| Texte CJK vertical | creative-fixed-canvas.md | HTML `writing-mode: vertical-rl` + `text-orientation: upright` + `white-space: nowrap` + Playwright |
| Document RTL (arabe/hébreu) | creative-fixed-canvas.md | HTML `dir="rtl"` + Playwright |
| Génération par lot (fusion de courriers) | report.md | Boucle Python + substitution de variables de template |
| Infographie | creative-fixed-canvas.md | Visualisation de données + design |
| Calendrier / planning | creative-fixed-canvas.md | Mise en page en grille + dimensions personnalisées |
| Guide / manuel / catalogue / introduction / collection | creative-flow.md | Mode document fluide — riche en texte avec une touche de design, le contenu s'écoule naturellement sur les pages |

#### Traitement (Manipuler un PDF existant)

| Scénario | Route | Commande / Méthode |
|----------|-------|------------------|
| Fusionner plusieurs PDFs | process.md | `pages.merge a.pdf b.pdf -o out.pdf` |
| Découper un PDF | process.md | `pages.split input.pdf -o ./output/` |
| Extraire le texte | process.md | `extract.text input.pdf` |
| Extraire les tableaux | process.md | `extract.table input.pdf` |
| Extraire les images | process.md | `extract.image input.pdf` |
| Remplir des formulaires | process.md | `form.fill input.pdf` |
| Office → PDF | process.md | `convert.office input.docx` |
| HTML → PDF (documents) | process.md | `convert.html input.html` ou `node html2pdf-next.js` |
| HTML → PDF (posters) | poster.md | `node html2poster.js poster.html` |
| Image → PDF | process.md | pikepdf : une image par page, intégrée comme XObject |
| PDF → image | process.md | pypdfium2 rend chaque page en PNG |
| Chiffrer / déchiffrer | process.md | chiffrement qpdf / pypdf |
| Ajouter un filigrane | process.md | superposition pikepdf : créer la page filigrane → fusionner sur chaque page |
| Compresser un PDF | process.md | Ghostscript : `gs -sDEVICE=pdfwrite -dPDFSETTINGS=/screen` |
| OCR d'un PDF scanné | process.md | pytesseract + pdf2image |
| Pivoter des pages | process.md | `pages.rotate input.pdf 90 -o out.pdf` |
| Rogner des pages | process.md | `pages.crop input.pdf l,b,r,t -o out.pdf` |
| Supprimer les pages blanches | process.md | `pages.clean input.pdf` |
| Reformater selon un template | process.md → délégation | Extraire le contenu → régénérer via report/creative |
| Diff / comparaison de PDFs | process.md | CLI `diff-pdf` ou comparaison de texte page par page en Python |
| Signature numérique | process.md | bibliothèque `pyhanko` (installation supplémentaire requise) |
| Modifier les métadonnées | process.md | `meta.set input.pdf -o out.pdf -d '{...}'` |

### Règles de routage spéciales

** Règle emoji (CRITIQUE - à vérifier EN PREMIER)** : contenu avec emojis intentionnels (📊🎯🔥💡 etc.) → forcer le **pipeline Creative** (utilisez `briefs/creative-fixed-canvas.md` pour les designs visuels d'abord, `briefs/creative-flow.md` pour les documents riches en texte) quel que soit le routage initial. ReportLab rend les emojis en carrés □ ; LaTeX les supprime silencieusement. Cette règle prime sur le routage Report/Academic. Même si l'utilisateur dit « rapport » - si le contenu contient des emojis, utilisez un brief Creative.

**Règle des tailles de page non standard** : dimensions autres que A4/Letter/A3 → préférez fortement le **pipeline Creative** (`briefs/creative-fixed-canvas.md` ou `briefs/creative-flow.md`). Playwright gère nativement toute taille de page arbitraire. ReportLab exige des calculs de pagination manuels.

**Détection automatique Academic** : articles, thèses ou maths lourdes → **briefs/academic.md** même sans mention explicite de « LaTeX ».

**Règle guidée par template** : quand l'utilisateur téléverse un PDF et dit « suis ce template » / « suis ce style » / « reformate comme ça » → section Template-Guided Reformat de **briefs/process.md**. C'est un triage Standard (pas Léger), car cela implique des décisions de design.

**Routage CV** : par défaut, brief Resume (compatible ATS). Industrie créative → brief Creative. CV académique avec publications → brief Academic.

---

## Ressources partagées

Ces ressources sont référencées par plusieurs briefs. Chaque brief indique quand et quoi charger.

| Ressource | Chemin | Utilisé par | Objectif |
|-------|------|---------|---------|
| Palette & typographie | `typesetting/palette.md` | Report, Fixed-Canvas, Flow | Système de couleurs, règles de polices, anti-patterns, espacement |
| Système de mise en page de couverture V2.1 | `typesetting/cover.md` | **Report + Fixed-Canvas + Flow + Academic** | 5 templates de qualité industrielle avec grille d'ancrage absolue, couches Z-index, système de graisse typographique, Summary Block obligatoire, sécurité au niveau code (5 vérifications), unité de base `U = W*0.05`. **Système de couverture HTML/Playwright unifié pour toutes les routes.** |
| Style des graphiques & anti-superposition | `typesetting/charts.md` | Report, Fixed-Canvas, Flow, Academic | Valeurs par défaut des graphiques, prévention des collisions, règles axes/grille/légende |
| Prévention du débordement | `typesetting/overflow.md` | Report, Fixed-Canvas, Flow, Academic | Système de bounding box, prévention du débordement texte/image/tableau, stratégies de repli |
| **Fill Engine (Anti-Vide)** | `typesetting/fill-engine.md` | **Report, Fixed-Canvas, Academic** | **Anti-Void Engine V2.0 : respect du plancher de police, calcul du taux de remplissage, inflation de paragraphes, élévation de composants, ancrage Y au nombre d'or** |
| Pagination & contrôle du flux | `typesetting/pagination.md` | Report, Fixed-Canvas, Flow | Intégrité inter-pages, contrôle orphelines/veuves, règles de ponctuation CJK |
| Système typographique | `typesetting/typography.md` | Report, Fixed-Canvas, Flow | Échelle de tailles de police, interligne, hiérarchie d'espacement |
| Ancres géométriques | `typesetting/geometry.md` | Creative + Report | Éléments géométriques décoratifs, règles de placement des ancres |
| Fonds de couverture | `typesetting/cover-backgrounds.md` | **Report + Fixed-Canvas + Flow + Academic** | Rendu des fonds de couverture, contraintes de transparence |
| Framework visuel | `configs/visual_framework.md` | Fixed-Canvas | Mode palette, harmonie des couleurs, paramètres de fond SVG |
| Bibliothèque de composants | `configs/components.md` | Fixed-Canvas | Composants de composition hors grille (cartes flottantes, etc.) |
| Piles de polices | `configs/fonts.md` | Tous les pipelines | Familles de polices par pipeline (Google Fonts, ReportLab, LaTeX) |

---

## Règles de contenu

- **Langue** : répondez dans la langue de la requête de l'utilisateur. Requête en français → PDF en français.
- **Nombre de pages/mots** : respectez les contraintes explicites (±20 %). Non spécifié → privilégier la complétude plutôt que la concision.
- **Plan** : les plans fournis par l'utilisateur sont sacrés. Pas de réorganisation sans demander.
- **Citations** : aucune fabrication. Chinois → GB/T 7714, anglais → APA. Recherchez pour vérifier.
- **Demandes multi-parties** : générez TOUTES les parties - ne supprimez jamais silencieusement un composant.

### Normes de profondeur et de richesse du contenu (anti-rédaction superficielle)

**PROBLÈME À ÉVITER** : un contenu superficiel avec des paragraphes de 1-2 phrases seulement, ou des sections avec un texte minimal sous les titres.

#### Normes minimales de contenu

1. **Profondeur de paragraphe**
   - Chaque paragraphe DOIT contenir au moins 3 à 5 phrases
   - Les paragraphes d'une seule phrase sont INTERDITS (sauf phrases de transition)
   - Chaque paragraphe doit développer UNE idée complète avec des détails à l'appui

2. **Complétude des sections**
   - Chaque titre de section DOIT être suivi d'un contenu substantiel (minimum 150-200 mots)
   - Ne créez JAMAIS une section avec seulement 1-2 phrases courtes
   - Si une section ne peut pas atteindre la longueur minimale, fusionnez-la avec les sections liées

3. **Techniques d'enrichissement du contenu**
   - Incluez des exemples concrets, des points de données ou des études de cas
   - Fournissez le contexte et les informations d'arrière-plan
   - Expliquez le « pourquoi » et le « comment », pas seulement le « quoi »
   - Ajoutez des comparaisons, contrastes ou perspectives alternatives quand c'est pertinent
   - Incluez implications, conséquences ou recommandations

#### Liste de contrôle qualité de rédaction

Avant de finaliser TOUT document rédigé, vérifiez :
- [ ] Aucun paragraphe ne compte moins de 3 phrases
- [ ] Aucune section ne compte moins de 150 mots de corps de texte
- [ ] Chaque point principal est soutenu par des exemples ou des preuves
- [ ] Les termes techniques sont expliqués à leur première occurrence
- [ ] Des transitions relient les idées entre paragraphes et sections

#### Stratégies d'expansion du contenu

Quand la rédaction semble maigre, appliquez ces techniques :

**Pour analyses/rapports :**
- Ajoutez du contexte d'arrière-plan (histoire, état actuel, tendances)
- Incluez plusieurs perspectives ou points de vue des parties prenantes
- Fournissez des métriques, statistiques ou données quantitatives précises
- Discutez des limites, défis ou contre-arguments
- Proposez des recommandations actionnables avec leur justification

**Pour du contenu explicatif :**
- Utilisez des analogies pour clarifier les concepts complexes
- Fournissez des décompositions étape par étape quand c'est applicable
- Incluez des applications réelles ou des cas d'usage
- Traitez les questions fréquentes ou les idées reçues
- Ajoutez des descriptions visuelles ou des explications de diagrammes

**PATTERNS INTERDITS :**
- Section dont le titre n'est suivi que de 1 à 3 phrases
- Listes à puces sans contexte explicatif
- Conclusions qui se contentent de reformuler l'introduction
- Sections qui disent « comme mentionné ci-dessus » sans apporter de valeur nouvelle

### Règle de cohérence linguistique

Utilisez toujours la même langue que celle de l'utilisateur pour :
- La réponse et le contenu du document
- Tout rapport, PDF ou graphique/diagramme généré
- **Page de couverture** : tout texte de la couverture (titre, sous-titre, tags, auteur, pied de page) DOIT être dans la langue de la requête de l'utilisateur. Requête en français → couverture en français ; requête en anglais → couverture en anglais. Le mélange est interdit.
- **Graphiques et figures** : avant de générer tout graphique ou figure, déterminez la langue de l'utilisateur. Assurez-vous que le titre, la légende, les libellés et les autres éléments textuels sont cohérents avec la langue de l'utilisateur. Si un élément ne peut pas utiliser la langue de l'utilisateur, expliquez explicitement la raison.

### Règles de chemins pour les sources d'images HTML

Lors de l'intégration d'images dans des documents HTML (pipeline Creative, diagrammes rendus par Playwright, ou tout flux HTML→PDF) :

| Emplacement de l'image | Valeur `<img src>` | Exemple |
|---|---|---|
| **Fichier local** | **Chemin relatif** au répertoire du fichier HTML | `<img src="images/chart.png">` ou `<img src="./diagram.png">` |
| **URL distante** | URL complète (aucun changement nécessaire) | `<img src="https://example.com/photo.jpg">` |

**Règles de fer :**
1. **N'utilisez JAMAIS de chemins absolus** pour les fichiers locaux dans les `<img>` HTML, `<source>`, `url()` CSS ou toute autre référence de ressource (ex. `/Users/alice/project/img.png`). Les chemins absolus cassent la portabilité entre machines et environnements.
2. **Utilisez toujours des chemins relatifs** ancrés au répertoire propre du fichier HTML. Si l'image vit dans un sous-répertoire, utilisez `images/foo.png` ou `./images/foo.png`.
3. **Les URLs distantes (`http://` / `https://`) restent telles quelles** - ne les convertissez pas en chemins locaux.
4. Quand vous générez du HTML depuis un script ou un blueprint, assurez-vous que toutes les ressources référencées sont soit (a) dans le même répertoire que le HTML de sortie, soit (b) dans un sous-répertoire clairement nommé (ex. `assets/`, `images/`), et référencées avec des chemins relatifs.
5. Si un script de build doit résoudre des chemins par programme, calculez des chemins relatifs au moment de la génération (ex. `os.path.relpath(image_path, html_dir)`) plutôt que d'embarquer des chemins de système de fichiers absolus.

---

## Intégration de figures et diagrammes (tous les briefs)

### Règle de fer : les figures sont de niveau bloc

Les figures, diagrammes et graphiques DOIVENT être des éléments de bloc indépendants occupant toute la largeur. **Ne faites jamais** flotter/envelopper les figures avec le texte du corps - cela provoque le badcase de chevauchement texte-diagramme.

| Brief | Intégration correcte | Interdit |
|-------|-------------------|-----------|
| Report (ReportLab) | `story.append(Image(...))` comme Flowable autonome | Placer des images dans le texte d'un Paragraph, simuler un float |
| Creative (Playwright) | `<figure style="display:block; width:100%; margin:2em auto">` | `float:right`, `display:flex` avec le texte, CSS façon `wrapfigure` |
| Academic (LaTeX) | `\begin{figure}[t] ... \end{figure}` | `\includegraphics` nu dans le corps du texte (pas d'environnement figure), `tikzpicture` nu en multi-colonnes |

### Stratégie pour diagrammes complexes

Quand un diagramme compte **>12 nœuds, >3 sous-groupes ou des connexions complexes**, n'essayez PAS de le rendre comme une figure géante unique. À la place :

1. **Tableau pour les détails** - les données structurées (phases, composants, specs) vont dans un vrai tableau
2. **Diagramme d'ensemble simplifié** - un flowchart/Mermaid épuré ne montrant que le flux de haut niveau (≤8 nœuds)
3. **Références croisées** - la légende du tableau et celle du diagramme se référencent mutuellement

Ce pattern « tableau + diagramme simple » prévient :
- Les diagrammes débordant des limites de page
- Un texte devenant trop petit pour être lisible afin de tout faire tenir
- Les moteurs de mise en page maltraitant les graphiques surdimensionnés

### Règles de qualité du contenu des diagrammes (référence croisée : charts)

Les règles ci-dessus traitent **comment** intégrer des diagrammes dans un PDF. Pour **l'apparence du diagramme lui-même** (disposition des nœuds, routage des connecteurs, couleurs, lisibilité), suivez les règles du skill `charts` :

**Avant de générer TOUT flowchart/diagramme pour intégration PDF, vérifiez ceci :**

1. **Les connecteurs ne doivent pas traverser les nœuds** - S'il y a 3 couches ou plus, connectez uniquement les couches adjacentes (haut→milieu, milieu→bas). Ne tracez jamais de lignes haut→bas traversant les nœuds du milieu. Utilisez des chemins de détour si des liens inter-couches sont nécessaires.
2. **Plusieurs flèches vers un même nœud ne doivent pas s'empiler** - Répartissez les points d'entrée uniformément le long du bord cible, ou utilisez le pattern fusion-puis-entrée (les sources convergent vers une ligne de fusion verticale, puis une seule flèche vers la cible).
3. **Remplissages à faible saturation uniquement** - Les fonds des nœuds doivent être pâles (`#EFF6FF`, `#F0FDF4`). Les couleurs à haute saturation (`#3B82F6`, `#10B981`) uniquement pour les bordures ou petits accents. Pas de palettes dignes d'un dessin d'enfant.
4. **Titres de phase vs sous-étapes doivent être visuellement distincts** - Couleur de fond, taille de police et graisse différentes. Jamais le même style de boîtes pour les deux.
5. **Les tailles de police doivent rester lisibles à la taille finale de sortie** - Les tailles dépendent du contexte d'intégration :
   | Contexte de sortie | Titre de nœud min | Description min | Libellé min |
   |---------------|----------------|-----------------|-----------|
   | PNG autonome (web/présentation, ≥1200px de large) | 14px | 12px | 11px |
   | Intégré dans un PDF A4 (ReportLab/LaTeX, ~450pt de largeur de contenu) | 10pt | 8pt | 7pt |
   | Intégré dans un diaporama (paysage, ~720pt de large) | 12pt | 10pt | 9pt |

   **Principe** : après intégration, le plus petit texte du diagramme doit rester lisible quand le document est consulté à un zoom de 100 %. Si le diagramme est réduit pour tenir dans la largeur de page, recalculez : `effective_size = original_size × (display_width / canvas_width)`. Si la taille effective passe sous le minimum, augmentez la taille de police d'origine ou réduisez la complexité du diagramme.
6. **Légende/annotations ne doivent pas chevaucher le contenu** - Conteneur séparé, écart ≥ 40px du dernier nœud, entièrement dans les limites du canevas.

**Pour les diagrammes rendus par Playwright** : utilisez des remplissages à faible saturation (`#EFF6FF`, `#F0FDF4`), CSS flexbox/grid pour la disposition des nœuds, SVG `<line>`/`<path>` pour les connecteurs, et vérifiez l'absence de chevauchement à la taille de rendu finale.
**Pour les diagrammes dessinés par ReportLab** : mêmes principes - utilisez `Drawing()` avec des coordonnées explicites, vérifiez l'absence de chevauchement des bounding boxes des nœuds avant de finaliser.

### Stratégie de génération des diagrammes (par brief)

Le rendu des diagrammes dépend du brief cible - **PAS** un pipeline TikZ universel.

| Brief cible | Méthode de diagramme | Justification |
|---|---|---|
| **Report** (ReportLab) | Playwright+CSS → PNG → `Image()` | Pas de compilateur LaTeX dans cette route ; HTML/CSS gère nativement toute mise en page |
| **Creative** (Playwright) | Directement en HTML (CSS flexbox/grid + connecteurs JS) | Déjà en contexte navigateur |
| **Academic** (Tectonic) - simple (≤6 nœuds) | `tikzpicture` TikZ natif | Sortie vectorielle, cohérence des polices, natif LaTeX |
| **Academic** (Tectonic) - complexe (>6 nœuds) | Playwright+CSS → PNG @2× → `\includegraphics` | La logique de branches TikZ est source d'erreurs pour les modèles ; un PNG 300dpi est prêt pour publication |

**Pipeline diagramme Playwright+CSS (Report & Academic-complexe) :**

```bash
# 1. Write diagram HTML (CSS grid/flexbox + connectors)
cat > diagram.html << 'EOF'
<!-- LLM generates: nodes as divs, arrows as SVG/CSS -->
EOF

# 2. Screenshot at 2× for print quality (300dpi equivalent)
python3 "$PDF_SKILL_DIR/scripts/pdf.py" convert.blueprint diagram.html --device-scale-factor 2 --output diagram.png
# Or via Playwright directly:
# page.screenshot(path='diagram.png', scale='device', device_scale_factor=2)

# 3a. Embed in ReportLab (Report brief)
from reportlab.platypus import Image
img = Image('diagram.png', width=450)  # auto height via aspect ratio
story.append(img)

# 3b. Embed in LaTeX (Academic brief, complex diagrams only)
# \includegraphics[width=\columnwidth]{diagram.png}
```

**🚫 INTERDIT pour les briefs Report/Creative :** n'utilisez PAS le pipeline TikZ standalone → compilation → pdftoppm → PNG. Cette route n'a pas de compilateur LaTeX et les étapes de compilation supplémentaires sont sources d'erreurs.

**TikZ reste valide UNIQUEMENT pour :**
- Le brief Academic avec des diagrammes simples (≤6 nœuds, linéaire/hiérarchique)
- L'intégration directe de `tikzpicture` dans des documents LaTeX
- Les diagrammes annotés de maths où le rendu mathématique LaTeX compte

Voir le Scénario B de `briefs/academic.md` pour les templates TikZ (diagrammes simples uniquement).

---

## Règle de fer du rendu vectoriel

**Le PDF final DOIT être généré via `page.pdf()` (Playwright) ou la sortie native ReportLab/LaTeX - JAMAIS via screenshot-to-PDF.**

| Scénario | Méthode correcte | Interdit |
|----------|---------------|-----------|
| Pipeline Creative (mono/multi-pages) | `page.pdf()` via `convert.blueprint` ou `html2pdf-next.js` | `page.screenshot()` → image → empaquetage en PDF |
| Couverture Report (HTML/Playwright) | `page.pdf()` → fusion via pypdf | Capture d'écran de couverture → intégration en image |
| Couverture Academic | `page.pdf()` → fusion via pypdf | Capture d'écran → `\includegraphics` pour la couverture |
| Posters/infographies pleine page | `html2poster.js` (overflow:hidden auto + mesure de hauteur + `page.pdf()`) | Tout pipeline raster pour la sortie finale |

**Pourquoi :** `page.pdf()` produit du texte vectoriel + des formes vectorielles. Le texte reste sélectionnable, net à tout zoom, et la taille de fichier est plus petite. Les PDFs basés sur capture d'écran sont des images raster - flous au zoom, non cherchables, et 3 à 5 fois plus gros.

**Le SEUL endroit où l'intégration de capture d'écran/PNG est acceptable :**
- Les **diagrammes** intégrés comme sous-éléments dans un document plus grand (ex. flowcharts dans un Report). Ils utilisent `page.screenshot()` à un facteur d'échelle device de 2× pour une qualité d'impression 300dpi, puis s'intègrent via `Image()` (ReportLab) ou `\includegraphics` (LaTeX).
- Les **images de graphiques** générées par matplotlib/plotly, enregistrées en PNG puis intégrées.

Ce sont des sous-éléments, pas le document lui-même. La sortie PDF au niveau du document doit toujours être vectorielle.

**Test rapide :** ouvrez le PDF généré, zoomez à 400 %. Si le texte est flou, vous avez utilisé un pipeline de capture d'écran. Corrigez.

### Règles de sélection du moteur HTML→PDF

Il existe **deux scripts dédiés** pour HTML→PDF. Choisissez selon le type de document :

| Type de document | Script | Raison |
|---------------|--------|--------|
| **Posters, infographies, designs d'image longue en page unique** | `html2poster.js` | overflow:hidden auto, mesure de hauteur auto, marge zéro, sortie monopage |
| **Pages de couverture (routes Report/Academic)** | `html2poster.js` | Les couvertures sont des mises en page fixes monopages en positionnement absolu - même nature que les posters. `html2pdf-next.js` convertirait absolute→static et détruirait la mise en page |
| **Documents multi-pages, rapports, articles académiques, CV** | `html2pdf-next.js` | Pagination Paged.js, taille A4/personnalisée, métadonnées pdf-lib. `--nopaged` pour le repli natif Chromium |
| **Pipeline Creative (Blueprint → HTML → PDF)** | `html2pdf-next.js` via `convert.blueprint` | Appelé en interne par le pipeline design_engine |

#### Poster / image longue monopage → `html2poster.js`

```bash
node "$PDF_SKILL_DIR/scripts/html2poster.js" poster.html --output poster.pdf --width 720px
```

`html2poster.js` automatiquement :
- Force `overflow: hidden` sur les conteneurs `.poster` / `.page` (rognage du débordement décoratif)
- Injecte `@page { margin: 0 }` (marges zéro toujours)
- Synchronise le fond `html/body` avec la couleur de fond du poster
- Mesure le scrollHeight de `.poster` et l'utilise comme hauteur du PDF
- Génère un PDF vectoriel monopage aux dimensions exactes du contenu

**Utilisez ceci pour TOUT design monopage à largeur fixe et hauteur dynamique.**

#### Documents / multi-pages → `html2pdf-next.js`

```bash
node "$PDF_SKILL_DIR/scripts/html2pdf-next.js" input.html --output output.pdf --width 210mm --height 297mm
# Or via pdf.py wrapper:
python3 "$PDF_SKILL_DIR/scripts/pdf.py" convert.html input.html --output output.pdf
```

Les hooks de pré-rendu gèrent automatiquement le rendu Mermaid/KaTeX, la détection de débordement et le chargement des polices. Le **polyfill Paged.js** est injecté pour la pagination (break-inside/before/after, orphelines/veuves, pages nommées). Utilisez le drapeau `--nopaged` pour revenir à la pagination @page native de Chromium si nécessaire.

#### ⚠️ Règle de fer : pas de scripts Playwright écrits à la main

Problèmes courants avec un `page.pdf()` Python écrit à la main (les scripts dédiés les gèrent automatiquement) :
1. **Règle `@page` manquante** → la marge par défaut du navigateur provoque un débordement du contenu sur une seconde page ou des bords blancs
2. **Éléments surdimensionnés non corrigés** → les grands éléments avec `break-inside: avoid` bloquent la pagination, le contenu est tronqué
3. **Rendu avant le chargement des polices** → le texte chinois s'affiche en carrés ou retombe sur une mauvaise police
4. **Pas de détection de débordement** → le contenu dépasse les limites de page sans que personne ne s'en aperçoive
5. **Pas de métadonnées** → titre, auteur et autres infos du PDF manquants

**Règle de fer : les posters et pages de couverture utilisent `html2poster.js`, les documents multi-pages utilisent `html2pdf-next.js`. N'écrivez pas de scripts Python Playwright à la main.**

> **⚠️ Piège de la page de couverture :** le HTML de couverture utilise `position: absolute` pour la mise en page. Utilisez toujours `html2poster.js` pour les couvertures — `html2pdf-next.js` + Paged.js remettrait en flux les éléments en position absolue, détruisant le design de la couverture.

### Pas de overflow:hidden sur les pages à taille fixe

**Ne réglez JAMAIS `overflow: hidden` sur `html`, `body`, `.page` ou le conteneur principal** dans un HTML destiné à la conversion PDF. Paged.js gère nativement le découpage du contenu et la pagination — il n'a pas besoin de rognage par débordement.

> **Note :** cette règle ne s'applique PAS aux posters rendus via `html2poster.js` - ce script ajoute automatiquement `overflow: hidden` aux conteneurs `.poster`/`.page` pour rogner le débordement décoratif.

| Problème | Cause | Correctif |
|---------|-------|-----|
| Contenu rogné silencieusement aux limites de page | `overflow: hidden` sur le conteneur masque le contenu dépassant les limites | Retirez `overflow: hidden` ; Paged.js gère la pagination |
| Éléments décoratifs gonflant le scrollWidth | `width > 100%` ou décalages négatifs sur des éléments en position absolue | Contraindre dans les limites de page (voir creative-fixed-canvas.md §0.75) |

**Associez toujours les pages à taille fixe à une auto-échelle `@media screen`** pour que la page entière soit visible dans toute fenêtre de navigateur sans défilement. Voir le pattern CSS dans `briefs/creative-fixed-canvas.md` § 0.5.

### Règle full-bleed (aucune marge blanche)

Quand vous générez du HTML pour `page.pdf()` Playwright, le contenu **DOIT remplir toute la page** avec zéro marge. Des marges blanches latérales = mise en page cassée.

**CSS obligatoire pour tout HTML → PDF :**
```css
@page {
  size: <width> <height>;  /* e.g., 720px 960px, or A4 */
  margin: 0;
}
html, body {
  margin: 0;
  padding: 0;
}
```

**Causes courantes de marges blanches :**
1. `@page { margin: 0 }` manquant - les marges par défaut du navigateur s'appliquent (~1cm de chaque côté)
2. La largeur du contenu ne correspond pas à la largeur de page - ex. le canevas fait 720px mais la page est A4 (794px)
3. Déclaration `@page { size }` manquante dans le HTML
4. Le contenu a un `max-width` explicite plus étroit que la page

**Pour le pipeline blueprint :** `design_engine.py` injecte désormais automatiquement `@page { size: var(--canvas-w) var(--canvas-h); margin: 0; }`.
**Pour du HTML brut :** VOUS devez inclure la règle `@page`. Aucune exception.
**Pour Playwright direct :** passez `margin: { top: 0, right: 0, bottom: 0, left: 0 }` à `page.pdf()`.

### Cohérence de la couleur de fond (pas de décalage de couleur)

**La couleur de fond de `html` / `body` doit correspondre à la couleur de fond du canevas de contenu.**

`page.pdf({ printBackground: true })` de Playwright rend la couleur de fond du body. Si le body est blanc alors que la zone de contenu est grise/colorée, des bords/écarts aux couleurs incohérentes apparaîtront dans le PDF.

#### Documents monochromes (toutes les pages avec le même fond)

```css
/* MANDATORY: body background = content background */
html, body {
  margin: 0;
  padding: 0;
  background: var(--c-bg);  /* Same color as content canvas */
}
```

#### Documents multi-pages à fonds mixtes (ex. couverture sombre + pages du corps blanches)

**Cause racine :** Playwright résout `.page { width: 210mm }` et `@page { size: 210mm }` en valeurs sous-pixel légèrement différentes (ex. 793.688px vs 793.701px). Cela crée un écart <1px au bord droit/bas de chaque div `.page` où le fond du `body` transparaît. Sur les pages sombres, un fond `body` blanc rend cet écart visible sous forme de bord blanc.

**Correctif - réglez le fond du `body` sur la couleur sombre dominante du document :**

```css
:root {
  --primary: #0f172a;  /* darkest page background */
}
html, body {
  margin: 0;
  padding: 0;
  width: 210mm;  /* match @page size */
  background: var(--primary);  /* fallback for sub-pixel gaps */
}
```

**Pourquoi cela fonctionne sans casser les pages blanches :**
- Pages sombres : l'écart sous-pixel révèle un `body` sombre → écart invisible.
- Pages blanches : `.page-white { background: #ffffff }` couvre entièrement le `body` → le body sombre n'est jamais visible.
- L'écart est <1px - même sur les pages blanches, le body sombre au bord extrême du pixel est imperceptible après anticrénelage.

**Règle : en générant un HTML multi-pages à fonds mixtes, réglez toujours `html, body { background }` sur la couleur de fond de la page la plus sombre.** Si toutes les pages sont claires/blanches, utilisez le fond de contenu le plus clair (ex. `#f8fafc`). Ne laissez jamais le fond du `body` non défini (défaut navigateur = blanc = bords blancs garantis sur les pages sombres).
```

### Centrage du contenu (pas de décalage gauche/droite)

**Après la conversion HTML→PDF, le contenu doit être centré, aucun décalage gauche/droite toléré.**

Causes courantes de décalage :
1. `@page { margin }` différent de 0 - la marge par défaut du navigateur provoque un décalage
2. `.safe-zone` ou conteneur de contenu avec `inset` / `padding` asymétrique gauche-droite
3. Le conteneur de contenu a un `max-width` mais pas de `margin: 0 auto`
4. Les composants en grille n'occupent qu'une largeur de colonne partielle (ex. `1/1 → X/7` n'utilise que la moitié gauche)
5. **Éléments décoratifs débordant des limites de page** - les éléments avec `width > 100%` ou décalages négatifs (ex. cercles lumineux, superpositions de dégradé) gonflent le `scrollWidth` au-delà de la largeur de page. Playwright réduit tout le contenu pour l'ajuster, provoquant un décalage à gauche. **Correctif : contraindre les éléments décoratifs dans les limites de page** (`width` ≤ 100 %, pas de décalages `left`/`right` négatifs). Voir `briefs/creative-fixed-canvas.md` §0.75 et `typesetting/overflow.md` §3.5 pour les détails.

### Bords anti-vide (pas de grandes marges vides)

**Le contenu ne doit pas présenter de grands espaces blancs dénués de sens aux bords de page, en haut ou en bas.**

- Le contenu doit exploiter pleinement la zone de page ; ne tassez pas tout le contenu dans la moitié supérieure en laissant le bas vide
- Pour les documents multi-pages, le taux de remplissage de chaque page doit être ≥ 60 % (voir la règle dernière page ≥ 40 % de `pagination.md`)
- Pour les posters/infographies monopages, le taux de remplissage doit être ≥ 70 %

---

## Preflight (assurance qualité)

Chaque PDF doit passer les vérifications preflight avant livraison. Chaque brief précise les commandes exactes.

### Validation HTML pré-rendu (OBLIGATOIRE pour tous les chemins HTML→PDF)

**Avant** d'appeler `html2pdf-next.js`, `html2poster.js`, `convert.blueprint` ou tout `page.pdf()` Playwright, exécutez :

```bash
python3 "$PDF_SKILL_DIR/scripts/poster_validate.py" check-html <your_file>.html
```

| Résultat | Action |
|--------|--------|
| **PASS** (aucune erreur) | Passez à la génération du PDF |
| Éléments **ERROR** | À corriger avant de générer le PDF. Utilisez `--fix --output <file>.html` pour la réparation automatique |
| Éléments **WARNING** | À examiner ; non bloquant mais à traiter |

**Vérifications clés :**
- `OVERFLOW_HIDDEN_CONTAINER` (erreur) : `overflow:hidden` sur html/body/.page rogne le contenu et masque les bugs de mise en page. Paged.js gère la pagination sans avoir besoin de rognage par débordement
- `FIXED_SIZE_NO_SCREEN_ADAPT` (avertissement) : page à taille fixe sans auto-échelle `@media screen` - l'aperçu navigateur exige un défilement
- `SCREEN_ADAPT_NO_SCALE` (avertissement) : `@media screen` présent mais sans scale/transform/zoom
- `FONT_NO_FALLBACK` (erreur) : font-family sans repli générique
- `COLOR_CONTRAST` (avertissement) : rapport de contraste texte/fond < 3:1
- Plus : images distantes, chemins absolus, reset de marge manquant, polices minuscules, fond incohérent, etc.

Ceci s'applique aux **trois routes HTML** : pipeline blueprint Creative, couvertures HTML Report, et HTML personnalisé/bypass.

### Système de prévention du débordement

**→ Spécification complète : `typesetting/overflow.md`** - lisez-la pour tout document avec tableaux, images ou mises en page multi-colonnes.

Principes fondamentaux :
1. **Mesurer d'abord, dessiner ensuite** - ne rendez jamais le contenu sans avoir précalculé ses dimensions
2. **Contrainte de bounding box** - la largeur de chaque élément ≤ `Max_Width` de son conteneur parent
3. **Texte : utilisez les métriques de police**, pas le nombre de caractères, pour le calcul de largeur
4. **Images : mise à l'échelle proportionnelle** - n'insérez jamais à la taille d'origine
5. **Tableaux : largeur de colonne pondérée** + enveloppement `Paragraph()` (jamais de chaînes brutes)
6. **Échelle de repli** : envelopper → réduire la police (max -3pt) → réduire le padding → scinder l'élément → journaliser un avertissement
7. **Vertical : KeepTogether** pour titre+corps, graphique+légende ; `repeatRows=1` pour les longs tableaux

### Prévention du débordement de tableaux (ReportLab)
**Bug de mise en page le plus courant : les colonnes de tableau dépassent les marges de page.**

Avant de construire tout Table ReportLab :
1. Calculez `available_width = page_width - left_margin - right_margin`
2. Utilisez des colWidths proportionnels (`[0.25, 0.40, 0.20, 0.15]` × available_width) ou le pattern fixe+flex
3. `sum(colWidths)` doit être ≤ `available_width` - **vérifiez-le dans le code**
4. Les colonnes de texte long doivent utiliser l'enveloppement `Paragraph()`, pas des chaînes brutes (les chaînes brutes ne se replient pas)
5. Le texte CJK est plus large : prévoyez ~12pt par caractère à une taille de police de 10pt

Voir `briefs/report.md` § « Table Width Management » pour les patterns de code.

### Prévention du débordement de tableaux (LaTeX/Academic)
**Bug le plus courant dans les articles à double colonne : les tableaux larges débordent de la largeur de colonne.**

Avant d'écrire tout tableau LaTeX :
1. Comptez les colonnes de données - ≤ 4 tient en une colonne ; 5-6 exigent `\small` ; 7-8 exigent `\resizebox` ; ≥ 9 utilisez `table*` (pleine largeur)
2. Utilisez `tabular*{\columnwidth}` ou `tabularx{\columnwidth}` au lieu de `tabular` brut pour 5 colonnes ou plus
3. N'utilisez jamais `tabular` brut avec 8 colonnes ou plus en mise en page twocolumn - débordement garanti
4. `\resizebox{\columnwidth}{!}` en dernier recours - vérifiez que le plus petit texte reste ≥ 6pt après mise à l'échelle

Voir `briefs/academic.md` § « Table width management » pour les patterns LaTeX.

### Liste noire CSS du PDF Playwright
Ces propriétés CSS **cassent silencieusement** dans le moteur de rendu PDF de Playwright :
- `backdrop-filter` / `-webkit-backdrop-filter` - **supprime tout le contenu de l'élément**. Utilisez des fonds `rgba()` solides.
- `overflow: hidden` sur les conteneurs de contenu - rogne le contenu. Sûr uniquement sur les petits éléments décoratifs (< 200px).

Après avoir généré tout PDF Playwright, **vérifiez que chaque page a du contenu** (extraction de texte pypdf, vérification non vide).

### Métadonnées PDF (tous les briefs)
TOUS les PDFs doivent avoir : Title, Author (défaut « Z.ai »), Creator, Subject.

### Résumé de livraison (tous les briefs)
Rapportez à l'utilisateur : chemin du fichier, taille, nombre de pages. Academic ajoute le nombre de mots/images. Creative ajoute la vérification page par page.

**Livrables de la route HTML→PDF (OBLIGATOIRE - s'applique à TOUS les briefs qui utilisent Playwright/HTML pour générer un PDF) :**
Chaque fois que le pipeline HTML→PDF est utilisé (route Creative, bypass de couverture Report, posters Direct HTML Flow, ou tout chemin `page.pdf()` Playwright), vous DEVEZ livrer **les deux fichiers** à l'utilisateur :
1. **HTML** - le fichier HTML source, pour que l'utilisateur puisse modifier et réutiliser le design
2. **PDF** - le PDF vectoriel final (sortie de `page.pdf()`)

Fournissez aussi, en option :
3. **Image** - une capture d'écran/image d'aperçu pleine page (PNG ou JPG) pour un partage rapide sur messagerie/réseaux sociaux

Tous les chemins de fichiers doivent être rapportés à l'utilisateur. **Ne livrez jamais seulement le PDF sans la source HTML.**

---

## Référence des outils

### CLI : `python3 "$PDF_SKILL_DIR/scripts/pdf.py" <command>`

```bash
# Environment
env.check                    # Check deps
env.fix                      # Auto-install missing

# Quality
code.sanitize <script>       # Sanitize forbidden Unicode
content.sanitize <file> [--apply]  # Fix content issues (CJK, encoding)
meta.brand <pdf>             # Add Z.ai metadata
font.check <pdf>             # Scan for missing glyphs
toc.check <pdf>              # Validate TOC

# Conversion
convert.blueprint <llm_json_response.md> -o final.pdf  # CRITICAL FOR CREATIVE: Auto-extracts JSON, compiles, and renders PDF.
convert.html <html>          # HTML → PDF (Playwright)
convert.latex <tex>           # LaTeX → PDF (Tectonic). Bundled binary is macOS arm64 only; see academic.md for other-platform install.
convert.office <file>         # Office → PDF (LibreOffice)

# Processing
extract.text <pdf>            # Extract text
extract.table <pdf>           # Extract tables
extract.image <pdf>           # Extract images
pages.merge a.pdf b.pdf -o out.pdf
pages.split <pdf>
pages.clean <pdf>             # Remove blank pages
form.info <pdf>               # Inspect form fields
form.fill <pdf>               # Fill form
form.annotate <pdf>           # Fill via annotations
meta.get <pdf>
meta.set <pdf> -o out.pdf -d '{"Title": "..."}'
```

### Validateur Poster/HTML/LaTeX : `python3 "$PDF_SKILL_DIR/scripts/poster_validate.py"`
```bash
check-html <html>                              # Pre-render validation (overflow:hidden, @media screen, fonts, contrast, etc.)
check-html <html> --fix --output <fixed.html>  # Auto-fix errors (remove overflow:hidden, add font fallback)
check-pdf <pdf> --source-html <html>           # Post-render validation
check-pdf <pdf> --poster                       # Poster mode: suppress ORPHAN_PAGE warning
check-tex <tex>                                # LaTeX source validation (table overflow, image width, etc.)
```

**Les vérifications de check-html incluent :**
- `OVERFLOW_HIDDEN_CONTAINER` (erreur) : overflow:hidden sur html/body/.page/.poster - rogne le contenu
- `FIXED_SIZE_NO_SCREEN_ADAPT` (avertissement) : page à taille fixe sans auto-échelle @media screen
- `SCREEN_ADAPT_NO_SCALE` (avertissement) : @media screen présent mais sans scale/transform/zoom
- `FONT_NO_FALLBACK` (erreur) : font-family sans repli générique (sans-serif/serif)
- `COLOR_CONTRAST` (avertissement) : rapport de contraste texte/fond < 3:1
- `BG_COLOR_MISMATCH` (avertissement) : le fond du body diffère de celui de .canvas/.poster
- `SCREEN_BG_MISMATCH` (avertissement) : le fond html du @media screen diffère de celui du body/canevas
- `MULTIPAGE_BODY_BG_MISSING` (avertissement) : document multi-pages avec fonds `.page` sombres mais sans couleur de fond `html/body`. Les écarts sous-pixel aux bords de page révèlent un body blanc, provoquant des bords blancs visibles sur les pages sombres. Résout les références `var()` via les variables `:root`.
- `SCREEN_NO_BG` (avertissement) : le bloc @media screen d'une page à taille fixe n'a pas de couleur de fond html
- `OVERFLOW_DECORATION` (avertissement) : des valeurs de position négatives peuvent provoquer des bords noirs
- `NO_PAGE_SIZE` / `MISSING_MARGIN_RESET` / `WHITE_BACKGROUND` / `TINY_FONT` / etc.

**Les vérifications de check-tex incluent :**
- `BARE_TABULAR_OVERFLOW` (erreur) : `\begin{tabular}` avec 5 colonnes ou plus en mise en page double colonne, non enveloppé dans resizebox/adjustbox/table*
- `RESIZEBOX_TEXTWIDTH` (erreur) : `\resizebox{\textwidth}` utilisé dans un float à colonne unique en mise en page double colonne. `\textwidth` = pleine largeur de page, mais le float `table` est une colonne. Correctif : utiliser `\resizebox{\columnwidth}` ou `table*`
- `TABULAR_OVERFLOW_RISK` (avertissement) : tabular à 4 colonnes en double colonne sans contrainte de largeur
- `TABULAR_WIDE` (avertissement) : tabular à 7 colonnes ou plus en colonne unique sans contrainte de largeur
- `TABULAR_NO_FLOAT` (avertissement) : tabular hors environnement float table/table*
- `TABULARX_NOT_LOADED` (avertissement) : le document a du tabular mais le package tabularx n'est pas chargé
- `IMAGE_NO_WIDTH` (avertissement) : `\includegraphics` sans contrainte width/height/scale
- `EQUATION_DUAL_ON_LINE` (avertissement) : environnement `equation` avec 2 équations ou plus jointes par `\quad` sans sauts de ligne. Débordement garanti en double colonne
- `EQUATION_OVERFLOW_RISK` (avertissement) : corps d'équation de plus de 80 caractères mathématiques. Déborde probablement d'une colonne
- `ALGORITHM_NO_SMALL_FONT` (avertissement) : environnement `algorithm` en double colonne sans `\SetAlFnt{\small}`
- `ALGORITHM_LONG_IO` (avertissement) : ligne Input/Output d'algorithm de plus de 120 caractères. Débordera d'une colonne étroite
- `CJK_ASCII_QUOTES` (erreur) : guillemet ASCII `"` trouvé adjacent à des caractères CJK. LaTeX interprète `"` comme guillemet double fermant, donc `"北漂"` se rend incorrectement. Ignore les environnements verbatim/lstlisting/minted et les commandes en ligne `\texttt{}`/`\url{}`/`\href{}{}`/`\verb||`.

### Design Engine : `python3 "$PDF_SKILL_DIR/scripts/design_engine.py"`
```bash
compile --blueprint <json_file> --output poster.html  # CRITICAL: Compile JSON blueprint to HTML
derive "document title or description"         # Auto-derive intent from content
palette --intent calm --mode dark               # Generate HSL-locked palette
palette-cascade --intent cold --mode minimal    # Generate role-based cascade palette (V2, preferred)
svg --intent flow --dimensions 720x960         # Generate SVG background
full --intent energy --mode dark --dimensions 720x960 --output-dir ./assets/
audit --palette-json palette.json              # Check palette constraints
```

### Générateur de palette (pour la route Report) : `python3 "$PDF_SKILL_DIR/scripts/pdf.py" palette.generate`
```bash
palette.generate --title "document title" --mode minimal   # Output: ready-to-paste ReportLab Python code
palette.generate --title "..." --format json               # Output: raw JSON
palette.generate --title "..." --format css                # Output: CSS custom properties
palette.generate --title "..." --mode dark --harmony complementary --seed 42
```

### Palette cascade (V2 - préférée) : `python3 "$PDF_SKILL_DIR/scripts/pdf.py" palette.cascade`
```bash
palette.cascade --title "document title" --mode minimal    # Output: summary table with all 12 roles
palette.cascade --title "..." --format json                # Full structured JSON (roles + cover + body + charts + semantic)
palette.cascade --title "..." --format css                 # CSS custom properties by tier
palette.cascade --title "..." --format reportlab           # Ready-to-paste ReportLab Python code
```
**⚠️ La palette cascade est le système de palette préféré.** Elle impose aire ∝ 1/saturation (grandes aires = saturation plus faible) et produit des sous-ensembles de couleurs unifiés pour la couverture, le corps et les graphiques à partir d'une teinte de base. Utilisez `palette.cascade` plutôt que `palette.generate` pour les nouveaux documents.

**⚠️ La route Report DOIT appeler `palette.cascade` (ou `palette.generate`) avant d'écrire tout code ReportLab.** La sortie est prête à copier-coller - aucune sélection manuelle d'hex autorisée.

> **Note** : `design_engine.py compile` produit du **HTML** à partir d'un blueprint JSON. Pour obtenir un **PDF**, utilisez `pdf.py convert.blueprint` qui appelle en interne `compile` → rendu Playwright → sortie PDF. Dans le pipeline Creative, utilisez toujours `convert.blueprint` pour le PDF final.

### Pile technique par brief

| Brief | Outil principal | Secondaire | Support emoji | Taille de page personnalisée |
|-------|-------------|-----------|---------------|-----------------|
| Report | ReportLab + pypdf | **Playwright (couverture)** | ❌ (tofu □) | Pagination manuelle |
| Creative | Playwright | html2pdf-next.js (Paged.js + pdf-lib) | ✅ natif | ✅ toute taille |
| Academic | Tectonic + pypdf | **Playwright (couverture)** | ❌ (supprimés) | Dépend du template |
| Process | pikepdf, pdfplumber | LibreOffice (soffice) | N/A | N/A |

> **Système de couverture unifié** : toutes les routes génèrent les couvertures via HTML/Playwright. Report utilise le Template 01, Academic les Templates 03-04 (fonds sombres, typographie savante), Creative génère couverture + corps dans un seul document HTML. Les PDFs de couverture sont fusionnés avec les PDFs du corps via pypdf.
>
> **Repli** : si le contenu du brief Report contient des emojis → re-router vers Creative.

---

## Carte des fichiers

```
SKILL.md                            ← You are here
briefs/
  report.md                         ← Report production: ReportLab workflow + API
  resume.md                         ← Resume/CV production: ATS-friendly single-column template
  creative-fixed-canvas.md              ← Fixed-canvas: posters, infographics, certificates (5-phase blueprint design)
  creative-flow.md                       ← Flowing documents: guides, handbooks, catalogs, introductions (content flows across pages)
  poster.md                          ← Poster scene rules: density, font sizing, fill constraints (overlay on creative-fixed-canvas.md)
  academic.md                       ← Academic production: LaTeX workflow + templates + resume(CV)
  process.md                        ← PDF processing: extract/merge/split/form/convert/reformat/encrypt/OCR/batch
configs/
  visual_framework.md               ← Palette mode, color harmony, SVG background params
  components.md                     ← Non-grid composition components (floating cards, etc.)
  fonts.md                          ← Font stacks per pipeline (Creative/Report/Academic)
typesetting/
  palette.md                        ← Color system + typography + anti-patterns + spacing
  cover.md                          ← Cover page layout system (7 layouts × 2-3 variants) + typography scale + color rules
  cover-backgrounds.md              ← Cover background rendering rules + transparency constraints
  charts.md                         ← Chart styling + anti-stacking rules + axis/grid/legend treatment
  overflow.md                       ← Bounding box system, text/image/table overflow prevention
  pagination.md                     ← Cross-page integrity, orphan/widow control, CJK punctuation
  typography.md                     ← Font size scale, line-height, spacing system
  geometry.md                       ← Geometric anchor system (decorative elements, lines, shapes)
  fill-engine.md                    ← Adaptive anti-void layout engine V2.0
scripts/
  pdf.py                            ← CLI tool (30 subcommands)
  pdf_qa.py                         ← PDF quality checker (metadata, fonts, overflow, margins, tables, formulas)
  design_engine.py                  ← Generative SVG + palette engine (palette/svg/compile/derive/audit)
  poster_validate.py                ← HTML/PDF validator
  toc_validate.py                   ← TOC validator
  html2pdf-next.js                  ← Playwright + Paged.js + pdf-lib HTML→PDF converter for documents
  html2poster.js                    ← Playwright HTML→PDF converter for posters/single-page (auto overflow:hidden, dynamic height)
  cover_validate.js                 ← Cover-ONLY overlap detection (text vs decorative lines). Do NOT run on posters or documents - only on cover HTML in Report/Academic pipelines.
references/
  resume-altacv.tex                 ← AltaCV dual-column resume template (creative/tech)
  resume-academic.tex               ← Academic CV template (PhD/academic)
```

### Protocole de chargement

> **⚠️ NE SAUTEZ AUCUN FICHIER. NE LISEZ PAS EN DIAGONALE.**
>
> Chaque règle de ces fichiers existe parce qu'une génération précédente a échoué sans elle. « Je sais déjà faire un PDF » n'est pas une raison valable pour sauter la lecture. Vous ne le savez pas — ces fichiers contiennent des centaines de pièges spécifiques aux moteurs (ordre d'enregistrement des polices, restrictions overflow:hidden, outils de rendu de couverture, interactions de saut de page) que vous ne pouvez pas deviner correctement.

**Étape 1 — à lire TOUJOURS (chaque tâche) :**
- Ce fichier (SKILL.md) — routage + règles de fer
- `configs/fonts.md` — piles de polices par pipeline (mauvaise police = CJK illisible)

**Étape 2 — lire le brief correspondant (chaque tâche) :**
- UN fichier de brief dans `briefs/` selon le routage
- Lisez-le **entièrement, de haut en bas** — ne vous arrêtez pas au premier exemple de code

**Étape 3 — lire chaque fichier référencé par le brief (OBLIGATOIRE, pas optionnel) :**
- Quand le brief dit « voir `typesetting/cover.md` » ou « voir `typesetting/overflow.md` » → vous **DEVEZ** ouvrir et lire ce fichier avant d'écrire tout code
- Quand un fichier de typesetting référence un autre fichier → suivez ce lien aussi
- **Il n'y a pas de « à la demande » ni de « seulement si nécessaire ».** Si le brief mentionne un fichier, lisez-le. Point.

**Étape 4 — page de couverture ? Lisez ceci AVANT de générer le HTML de couverture :**
- `typesetting/cover.md` — système de templates, architecture en couches, règles anti-débordement
- Exécutez `cover_validate.js` après avoir généré le HTML de couverture (avant la conversion PDF)
- Utilisez `html2poster.js` pour le rendu de la couverture — **n'écrivez JAMAIS de scripts Playwright à la main**

**Point de contrôle avant d'écrire le code :** pouvez-vous nommer l'outil de rendu exact (html2poster.js vs html2pdf-next.js), la pile de polices, l'ID du template de couverture et les validateurs post-génération pour cette tâche ? Sinon, vous n'avez pas assez lu. Retournez en arrière.

---

## 8. Liste de contrôle qualité (obligatoire après chaque génération de PDF)

> ⚠️ **Le corps du texte constitue le premier chapitre.** Couverture/sommaire/résumé ne comptent pas dans la numérotation ; la numérotation du corps commence toujours à 1. Voir `report.md` étape 3.5.

> Les vérifications suivantes proviennent des fichiers de spécification `typesetting/` et constituent des **portes de qualité obligatoires**.

### Détection automatisée (à exécuter obligatoirement)

```bash
# 1. PDF quality check (all pipelines)
python3 "$PDF_SKILL_DIR/scripts/pdf_qa.py" <output.pdf>
python3 "$PDF_SKILL_DIR/scripts/pdf_qa.py" --poster <output.pdf>   # poster mode: skip content fill ratio, check all pages for full-bleed
python3 "$PDF_SKILL_DIR/scripts/pdf_qa.py" --skip-cover --formulas <output.pdf>   # academic mode: skip cover for margin check, enable formula overflow
python3 "$PDF_SKILL_DIR/scripts/pdf_qa.py" --no-tables <output.pdf>   # creative mode: skip table centering check

# 2. Cover overlap detection (Report/Academic with cover - MANDATORY)
#    Run on the cover HTML BEFORE rendering to PDF. Detects:
#    - Text vs decorative line overlap (minimum gap = 1U = 5% of page width)
#    - Layer 3 text vs text zone overflow (same-layer foreground text blocks overlapping)
#    Exit 0 = pass, Exit 1 = overlap found (must fix), Exit 2 = script error
node "$PDF_SKILL_DIR/scripts/cover_validate.js" cover.html
node "$PDF_SKILL_DIR/scripts/cover_validate.js" cover.html --min-gap 30   # custom min gap in px
```

> **Dépendances** : `pymupdf` (`pip install pymupdf`) pour pdf_qa.py ; `playwright` ou `playwright-core` pour cover_validate.js. Si non installées, sautez la vérification correspondante et utilisez la liste de contrôle manuelle ci-dessous.

Exécutez `pdf_qa.py` après avoir généré un PDF. Il détecte automatiquement : complétude des métadonnées, cohérence des tailles de page, pages blanches, placement de la ponctuation CJK, nombre de couleurs, statut d'incorporation des polices, débordement de contenu, taux de remplissage du contenu, full-bleed de la couverture, symétrie des marges, centrage des tableaux, débordement de formules.
- **Mode `--poster`** : saute la vérification du taux de remplissage du contenu (la dernière page d'un poster contient naturellement moins de contenu), vérifie le full-bleed sur TOUTES les pages (pas seulement la couverture)
- **`--skip-cover`** : saute la page 1 lors de la vérification de symétrie des marges (pour les documents à couverture générée séparément)
- **`--no-tables`** : désactive la vérification de centrage des tableaux (pour les documents créatifs/posters qui ont rarement des tableaux classiques)
- **`--formulas`** : active la détection de débordement de formules (vérifie si le contenu ressemblant à des formules dépasse la marge de contenu droite)
- Résultat PASS → livrez directement
- Résultat WARN → évaluez si un correctif est nécessaire, non bloquant
- Résultat FAIL → **corriger et régénérer obligatoirement**

### Listes de contrôle qualité spécifiques aux briefs

Les éléments détaillés de contrôle ont été déplacés dans chaque brief pour réduire la taille du contexte :

- **Report** → `briefs/report.md` § « Quality Checklist — Report-Specific Items » (pagination, débordement, couleur, couverture, graphiques, règles d'examen, mise en page, retenue de design)
- **Academic** → `briefs/academic.md` § « Quality Checklist — Academic-Specific Items » (pagination, spécifique LaTeX)
- **Creative Fixed-Canvas** → `briefs/creative-fixed-canvas.md` § « Quality Checklist — Creative-Specific Items » (couleur, ancres géométriques, mise en page, retenue de design)
- **Creative Flow** → `briefs/creative-flow.md` § « Quality Checklist — Creative Flow » (mise en page & pagination, full-bleed, qualité de design)

Après avoir chargé votre brief, relisez sa liste de contrôle qualité avant de livrer.

### Propreté de la sortie (tous les pipelines)

- [ ] **Aucun artefact de processus dans la sortie** : n'incluez JAMAIS de numéros de version (« V3 »), marqueurs d'itération, libellés de brouillon (« DRAFT »), tampons « CONFIDENTIAL »/« 机密 », « Generated by AI »/« 本文档由AI生成 », ni commentaires internes dans le PDF final, sauf demande explicite de l'utilisateur
- [ ] **Aucun libellé boilerplate auto-généré** : n'ajoutez AUCUN filigrane, avis de génération, numéro de version, horodatage ou nom d'outil non demandé par l'utilisateur
- [ ] **Aucune sortie de debug dans le contenu** : les logs console, chemins de fichiers, horodatages de génération, noms d'outils ou messages d'erreur ne doivent jamais apparaître dans le corps du PDF
- [ ] **Métadonnées propres uniquement** : les métadonnées PDF (auteur, titre, sujet) doivent refléter le contenu du document, pas le processus de génération
