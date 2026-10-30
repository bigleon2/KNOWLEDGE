---
nom: docx
version: 1.0
source: skills/docx/SKILL.md
sha256_source: a4f2fbeff3a0
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — docx (v1.0)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/docx/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: docx
metadata:
  author: Z.AI
  version: "1.0"
description: "Création, édition et analyse de documents complets avec prise en charge des modifications suivies, des commentaires, de la préservation du formatage et de l'extraction de texte. Lorsque GLM doit travailler avec des documents professionnels (fichiers .docx) pour : (1) Créer de nouveaux documents, (2) Modifier ou éditer du contenu, (3) Travailler avec des modifications suivies, (4) Ajouter des commentaires, ou toute autre tâche documentaire"
license: Propriétaire. LICENSE.txt contient les termes complets
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# DOCX Création, Édition et Analyse

## Installation Rapide

```bash
bash "$SKILL_DIR/setup.sh"    # Vérification interactive de l'environnement + installation
```

## Vue d'ensemble

Un fichier .docx est une archive ZIP contenant des fichiers XML. Cette compétence fournit des outils pour créer, éditer, lire et réviser des documents Word.

## Itinéraire Rapide — Lisez ceci d'abord

**Étape 1** : Déterminer le type de tâche → charger le fichier d'itinéraire correspondant
**Étape 2** : Déterminer le contexte métier → charger le fichier de scène correspondant (si applicable)
**Étape 3** : Charger `references/design-system.md` pour les modèles de couverture, palettes et couleurs de graphiques
**Étape 4** : Charger `references/common-rules.md` pour les règles de mise en page, police et qualité partagées
**Étape 5** : Exécuter les instructions par itinéraire
**Étape 6** : Exécuter la liste de contrôle post-génération

⚠️ **OBLIGATOIRE — Application du modèle de couverture (Étape 3) :**
Lors de la création d'un document nécessitant une page de couverture, vous DEVEZ utiliser l'un des 7 modèles de couverture validés (R1–R7) de `design-system.md`. **Le code de couverture libre est INTERDIT.** Le modèle fournit le tableau d'enveloppe, l'arrière-plan, la structure de mise en page, les paramètres de bordure et l'espacement — ne réinventez aucun de ces éléments.

Workflow : (1) Appeler `selectCoverRecipe(docType, industry)` pour obtenir le modèle + palette → (2) Utiliser le code de fonction correspondant `buildCoverRX()` de `design-system.md` → (3) Passer votre `config` (titre, sous-titre, metaLines, etc.) dans le constructeur de modèle. Si vous sautez cette étape et écrivez le code de couverture à partir de zéro, la couverture AURA des problèmes de compatibilité (pages blanches dans MS Office, bordures manquantes, débordement, etc.).

### Configuration du chemin de script (OBLIGATOIRE avant tout appel de script)

Tous les outils CLI résident dans `scripts/` par rapport au répertoire de cette compétence. Avant d'appeler un script, résoudre le chemin absolu une seule fois :

```bash
DOCX_SCRIPTS="<skill_directory>/scripts"   # ← répertoire parent de ce SKILL.md

# Ensuite, toutes les commandes utilisent $DOCX_SCRIPTS :
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" output.docx --auto
```

**Pour les imports Python** (lorsque le code de génération doit importer des modules de compétence) :

```python
import sys, os
DOCX_SCRIPTS = os.path.join("<skill_directory>", "scripts")
if DOCX_SCRIPTS not in sys.path:
    sys.path.insert(0, DOCX_SCRIPTS)
```

**⚠️ JAMAIS utiliser `python3 scripts/...` nu** — cela ne fonctionne que si le répertoire de travail courant est justement le répertoire de compétence. Utilisez toujours le chemin absolu `$DOCX_SCRIPTS`.

### Routeur de Tâche

| Intention Utilisateur | Itinéraire | Fichiers à Charger |
|-----------------------|------------|--------------------|
| Créer/écrire/générer (sans pièce jointe) | **Créer** | `routes/create.md` + `references/docx-js-core.md` |
| Modifier/réviser (avec pièce jointe) | **Modifier** | `routes/edit.md` + `references/ooxml.md` |
| Formatage/mise en page/police/marges | **Formater** | `routes/format.md` |
| Commenter/annoter/réviser | **Commenter** | `routes/comment.md` |
| Lire/analyser/extraire | **Lire** | `routes/read.md` |

### Routeur de Scène (Optionnel — charger après l'itinéraire)

| Mots-clés Utilisateur | Scène | Fichier |
|-----------------------|-------|---------|
| thesis, academic, research, paper, dissertation, abstract, journal | Académique | `scenes/academic.md` |
| report, analysis, experiment, testing, survey, review, summary, proposal, feasibility, competitor, industry, operations | Rapport | `scenes/report.md` |
| contract, agreement, terms, transfer, NDA, confidential, framework, cooperation, service terms, user agreement, procurement | Contrat | `scenes/contract.md` |
| resume, CV, job application | CV | `scenes/resume.md` |
| exam, test, quiz, paper (contexte examen), lesson plan | Examen | `scenes/exam.md` |
| official document, notice, letter, reply, minutes, red header, government, issuance | Officiel | `scenes/official-doc.md` |
| broadcast script, product copy, livestream, speech, presentation script, video script | Rédaction | `scenes/copywriting.md` |
| plan, proposal (si contexte rapport) | Rapport | `scenes/report.md` |
| policy, regulation, standard, management rules | Officiel | `scenes/official-doc.md` |

**Si aucune scène ne correspond**, utiliser les règles de conception par défaut de `references/design-system.md` et `references/common-rules.md`.

## Normes de Formatage (Toujours Appliquer)

→ Voir `references/common-rules.md` pour les profils de police complets, espacement, retrait et règles de mise en page.

**Règles clés (référence rapide) :**
- **Espacement des lignes** : 1.3x (`line: 312`) — OBLIGATOIRE. Exceptions : CV 1.15x, document officiel 28pt fixe, rédaction `400`, contrat 1.5x
- **Corps CJK** : Justifié + retrait de 2 caractères (`firstLine: 480` SimSun / `420` YaHei)
- **Tableaux** : `margins` définis, `ShadingType.CLEAR`, `tableHeader: true`, `cantSplit: true`, titre `keepNext: true`
- **Images** : paramètre `type` requis, préserver les proportions via `image-size`, saut de page dans le Paragraphe
- **Ligne de tableau pleine page** : `rule: "exact"` avec une marge de sécurité de 1200 twips

## Référence Rapide des Unités

| Unité | Valeur |
|-------|--------|
| 1 cm | 567 twips |
| 1 inch | 1440 twips |
| 1 pt | 20 half-points |
| A4 | 11906 × 16838 twips |

Pour le tableau de taille de police chinoise et les marges courantes, voir `references/common-rules.md`.## Post-Generation — Vérification en Deux Couches

### Couche 1 : Liste de contrôle manuelle (auto-vérification pendant la génération)

#### Format de base
- [ ] L'interligne est de 1.3x (`line: 312`) ou substitution spécifique à la scène
- [ ] Le corps CJK a une indentation de 2 caractères (`firstLine: 480` ou `420`)
- [ ] Les tableaux ont des marges définies
- [ ] Les images conservent leur ratio d'aspect via `image-size` — NE JAMAIS coder en dur la largeur et la hauteur en même temps
- [ ] PageBreak à l'intérieur d'un Paragraph
- [ ] ShadingType utilise CLEAR
- [ ] Chaque liste numérotée utilise un `reference` unique
- [ ] **⚠️ CRITIQUE — Les guillemets dans les chaînes JS sont correctement échappés.** Les guillemets courbes chinois (`""` `''`) DOIVENT utiliser des échappements Unicode (`\u201c` `\u201d` `\u2018` `\u2019`) ; les guillemets droits (`"` `'`) utilisent `\"` `\'` ou des délimiteurs alternatifs. **C'est le bug #1 le plus courant dans la génération de code.** Le texte chinois contient fréquemment `""` pour l'emphase ou les noms propres (par exemple, "shuang11", "qian di hou gao", "618") — chaque occurrence DOIT être échappée. L'échappement manquant produit des erreurs de syntaxe JS qui cassent silencieusement la génération de document.
- [ ] ImageRun inclut le paramètre `type`
- [ ] En-tête/pied de page présents (sauf indication contraire de la scène)

#### Styles de titre
- [ ] Tous les titres de chapitre du corps utilisent `heading: HeadingLevel.HEADING_X` (jamais simulé avec gras + grande police)
- [ ] Le titre de couverture peut ignorer le style Heading (pas dans la TOC), mais les titres du corps DOIVENT utiliser le style Heading

#### Saut de page et prévention des pages blanches
- [ ] Couverture/contenu dans des sections séparées
- [ ] Trois règles pour éviter les pages blanches :
  - ① Lors de l'utilisation de section(NEXT_PAGE), la section précédente NE DOIT PAS se terminer par PageBreak (double saut = page blanche)
  - ② Le paragraphe PageBreak DEVRAIT contenir du texte visible — **exception** : paragraphe vide de fin de section + PageBreak est autorisé (séparateur de section normal, par exemple après la page de couverture)
  - ③ Pas plus de 3 paragraphes vides consécutifs
- [ ] La hauteur de ligne de tableau pleine page utilise `rule: "exact"` (jamais `"atLeast"` pour les tableaux hauts)
- [ ] Pas de pages blanches indésirées (vérifier chaque fin de section)

#### TOC
→ Voir `references/toc.md` pour la référence et la checklist de la TOC complète.
- [ ] Si le titre de TOC existe → l'élément `TableOfContents` DOIT être présent
- [ ] **⚠️ OBLIGATOIRE PageBreak après TableOfContents** — un Paragraph contenant PageBreak DOIT suivre immédiatement l'élément `TableOfContents` ; sans cela, la TOC et le contenu du corps s'afficheront sur la même page. C'est l'échec de formatage TOC #1 — ne jamais l'omettre
- [ ] `add_toc_placeholders.py --auto` s'exécute après la génération ; code de sortie = 0
- [ ] **LA TOC DOIT être dans sa propre section** — la section corps définit `page: { pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } }` afin que les numéros de page commencent à partir de la première page du corps, pas des pages de la TOC
- [ ] **Imbrication de l'API de numérotation de page** — `pageNumbers` DOIT être à l'intérieur de `page: {}`, PAS au niveau supérieur des propriétés (voir toc.md § API de numérotation de page)
- [ ] **Numérotation de page en 3 sections** — Couverture (pas de #) → Matière frontale (romain i,ii,iii, start=1) → Corps (arabe 1,2,3, start=1)
- [ ] **Post-traitement des pieds de page** — Le pied de page de la section romaine DOIT contenir `PAGE \* ROMAN \* MERGEFORMAT` ; la section arabe `PAGE \* arabic \* MERGEFORMAT` (WPS ignore le format pgNumType). **⚠️ JAMAIS utiliser `\* decimal` dans instrText** — `decimal` est une valeur enum de l'API docx-js (`NumberFormat.DECIMAL`), PAS un commutateur de format de champ Word valide ; son utilisation fait que les numéros de page s'affichent comme "1decimal", "2decimal". Le commutateur de champ Word correct pour les chiffres arabes est `\* arabic`.
- [ ] **Supprimer pgNumType vide** — Post-traitement pour supprimer `<w:pgNumType/>` de la section de couverture (docx-js émet un élément vide qui perturbe WPS)
- [ ] **⚠️ ASTUCE DE RAFRAÎCHISSEMENT TOC OBLIGATOIRE** — entre l'élément `TableOfContents` et le PageBreak, DOIT ajouter un paragraphe de note en italique gris informant les utilisateurs de faire clic droit sur la TOC → "Update Field" pour rafraîchir les numéros de page (voir toc.md § Astuce de rafraîchissement TOC)

#### Tableau multi-page
- [ ] Lignes d'en-tête : `tableHeader: true`
- [ ] Toutes les lignes : `cantSplit: true`
- [ ] Paragraphe de titre : `keepNext: true`

#### Couverture
- [ ] **LA COUVERTURE DOIT utiliser une recette validée (R1–R7)** de `design-system.md` — le code de couverture libre est interdit
- [ ] La recette de couverture correspond au type de document (selon `selectCoverRecipe()` dans `design-system.md`)
- [ ] La couverture utilise le wrapper externe de table 16838 avec `allNoBorders` (toutes les recettes le fournissent)
- [ ] Le titre de couverture utilise `calcTitleLayout()` — jamais de taille de police codée en dur au-dessus de 40pt
- [ ] L'espacement de couverture utilise `calcCoverSpacing()` — jamais de grandes valeurs d'espacement codées en dur
- [ ] Le contenu de couverture ne déborde pas (hauteur totale ≤ 15638 twips, Table utilise `rule: "exact"`)
- [ ] Chaque TextRun sur un fond foncé/couleur a une `color` explicite définie (Règle 9 — ne jamais compter sur le noir par défaut)
- [ ] La section de couverture n'a pas de PageBreak ou de paragraphes vides en fin
- [ ] Les lignes de titre se divisent aux limites sémantiques (pas de coupure au milieu d'un mot, pas de lignes orphelines d'un seul caractère)
- [ ] Pas de lignes décoratives avec caractères de texte (`───`, `━━━`) — utiliser uniquement les bordures de paragraphe

### Couche 2 : Script de vérification post-génération automatisée

```bash
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
```

Vérifie automatiquement 14 règles métier : pages blanches, **débordement de couverture (taille de police/espacement/contenu de fin)**, cohérence de l'interligne, marges de tableau, contrôle de tableau multi-page (cantSplit/tblHeader), débordement d'image, distorsion du ratio d'aspect d'image, police de secours, indentation CJK, hiérarchie de titres, mauvais usage de ShadingType, qualité de TOC, propreté du document (texte d'espace réservé/Markdown/HTML résiduel), qualité du contenu du rapport (présence de résumé/spécificité de titre/détection de conclusion vague).

⚠️ **Après avoir généré n'importe quel document, DOIT exécuter postcheck.py et corriger toutes les erreurs ❌.**

## Formules mathématiques

L'entrée de formule utilise la syntaxe **LaTeX**, convertie internement en objets Math docx-js.

- **Formules de base** (fractions, indices/exposants, racines, sommes) → composants Math docx-js
- **Formules complexes** (imbrication 3+, matrices, fonctions par morceaux) → secours matplotlib PNG

Voir `references/math-formulas.md`.

## Graphiques

Par défaut : **bibliothèque de modèles matplotlib** génère un PNG pour l'intégration.

6 modèles prêts à l'emploi : barre, ligne, camembert, boîte, radar, heatmap.
Les couleurs sont dérivées automatiquement de palette.accent du document pour la cohérence de style.
Palette par défaut : basse saturation Morandi (voir design-system.md).

Voir `references/chart-templates.md`.## Dépendances

- **pandoc**: Extraction de texte
- **docx**: `bun add docx` or `npm install docx` (création)
- **LibreOffice**: Conversion PDF, support .doc
- **Poppler**: PDF vers image (`pdftoppm`)
- **defusedxml**: Analyse XML sécurisée
- **python-docx**: Opérations simples sur les commentaires


---

## Ressources locales du dossier

Ressources jointes (usage autonome — lire au besoin pendant l'application du prompt) :
- `references/chart-templates.md`
- `references/common-rules.md`
- `references/decorations.md`
- `references/design-system.md`
- `references/docx-js-advanced.md`
- `references/docx-js-core.md`
- `references/faq.md`
- `references/math-formulas.md`
- `references/ooxml.md`
- `references/toc.md`
