---
name: docx
version: "1.1.0"
category: "Documents & Contenu"
tags:
  - docx
metadata:
  author: Z.AI
  version: "1.1"
description: "Création, édition et analyse complètes de documents, avec prise en charge du suivi des modifications, des commentaires, de la préservation de la mise en forme et de l'extraction de texte. Quand GLM doit travailler avec des documents professionnels (fichiers .docx) pour : (1) créer de nouveaux documents, (2) modifier ou éditer du contenu, (3) travailler avec le suivi des modifications, (4) ajouter des commentaires, ou toute autre tâche documentaire"
license: Proprietary. LICENSE.txt has complete terms
language: fr

read_when:
  - Déclencher quand la demande concerne : "Création, édition et analyse complètes de documents, avec prise en charge du suivi des modifications, des com…
  - Déclencher si la demande mentionne : documents, suivi, modifications
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Création, édition et analyse de documents DOCX

## Mise en route rapide

```bash
bash "$SKILL_DIR/setup.sh"    # Interactive environment check + install
```

## Vue d'ensemble

Un fichier .docx est une archive ZIP contenant des fichiers XML. Ce skill fournit des outils pour créer, éditer, lire et relire des documents Word.

## Route rapide — à lire d'abord

**Étape 1** : déterminer le type de tâche → charger le fichier de route correspondant
**Étape 2** : déterminer la scène métier → charger le fichier de scène correspondant (le cas échéant)
**Étape 3** : charger `references/design-system.md` pour les recettes de couverture, les palettes et les couleurs de graphiques
**Étape 4** : charger `references/common-rules.md` pour les règles partagées de mise en page, de police et de qualité
**Étape 5** : exécuter selon les instructions de la route
**Étape 6** : exécuter la checklist post-génération

⚠️ **OBLIGATOIRE — Application des recettes de couverture (étape 3) :**
Lors de la création d'un document nécessitant une page de couverture, vous DEVEZ utiliser l'une des 7 recettes de couverture validées (R1–R7) de `design-system.md`. **Le code de couverture libre est INTERDIT.** La recette fournit la table englobante, l'arrière-plan, la structure de mise en page, les réglages de bordures et les espacements — n'en réinventez aucun.

Flux : (1) appeler `selectCoverRecipe(docType, industry)` pour obtenir la recette + la palette → (2) utiliser le code de la fonction `buildCoverRX()` correspondante de `design-system.md` → (3) passer votre `config` (titre, sous-titre, metaLines, etc.) au constructeur de la recette. Si vous sautez cette étape et écrivez le code de couverture de zéro, la couverture AURA des problèmes de compatibilité (pages blanches dans MS Office, bordures manquantes, débordement, etc.).

### Configuration des chemins de scripts (OBLIGATOIRE avant tout appel de script)

Tous les outils CLI vivent dans `scripts/`, relativement au répertoire de ce skill. Avant d'appeler un script, résoudre une fois le chemin absolu :

```bash
DOCX_SCRIPTS="<skill_directory>/scripts"   # ← parent directory of this SKILL.md

# Then all commands use $DOCX_SCRIPTS:
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" output.docx --auto
```

**Pour les imports Python** (quand le code de génération doit importer les modules du skill) :

```python
import sys, os
DOCX_SCRIPTS = os.path.join("<skill_directory>", "scripts")
if DOCX_SCRIPTS not in sys.path:
    sys.path.insert(0, DOCX_SCRIPTS)
```

**⚠️ N'utilisez JAMAIS un `python3 scripts/...` nu** — cela ne fonctionne que si le cwd se trouve être le répertoire du skill. Utilisez toujours le chemin absolu `$DOCX_SCRIPTS`.

### Routeur de tâches

| Intention de l'utilisateur | Route | Fichiers à charger |
|-------------|-------|---------------|
| Créer/écrire/générer (sans pièce jointe) | **Create** | `routes/create.md` + `references/docx-js-core.md` |
| Éditer/modifier/réviser (avec pièce jointe) | **Edit** | `routes/edit.md` + `references/ooxml.md` |
| Mise en forme/disposition/police/marges | **Format** | `routes/format.md` |
| Commenter/annoter/relecture | **Comment** | `routes/comment.md` |
| Lire/analyser/extraire | **Read** | `routes/read.md` |

### Routeur de scènes (optionnel — à charger après la route)

| Mots-clés utilisateur | Scène | Fichier |
|---------------|-------|------|
| thesis, academic, research, paper, dissertation, abstract, journal | Academic | `scenes/academic.md` |
| report, analysis, experiment, testing, survey, review, summary, proposal, feasibility, competitor, industry, operations | Report | `scenes/report.md` |
| contract, agreement, terms, transfer, NDA, confidential, framework, cooperation, service terms, user agreement, procurement | Contract | `scenes/contract.md` |
| resume, CV, job application | Resume | `scenes/resume.md` |
| exam, test, quiz, paper (exam context), lesson plan | Exam | `scenes/exam.md` |
| official document, notice, letter, reply, minutes, red header, government, issuance | Official | `scenes/official-doc.md` |
| broadcast script, product copy, livestream, speech, presentation script, video script | Copywriting | `scenes/copywriting.md` |
| plan, proposal (if not report context) | Report | `scenes/report.md` |
| policy, regulation, standard, management rules | Official | `scenes/official-doc.md` |

**Si aucune scène ne correspond**, utiliser les règles de design par défaut de `references/design-system.md` et `references/common-rules.md`.

## Normes de mise en forme (toujours appliquer)

→ Voir `references/common-rules.md` pour les profils de police complets, les espacements, les retraits et les règles de mise en page.

**Règles clés (référence rapide) :**
- **Interligne** : 1,3x (`line: 312`) — OBLIGATOIRE. Exceptions : CV 1,15x, document officiel 28pt fixe, copywriting `400`, contrat 1,5x
- **Corps CJK** : justifié + retrait de 2 caractères (`firstLine: 480` SimSun / `420` YaHei)
- **Tableaux** : `margins` définies, `ShadingType.CLEAR`, `tableHeader: true`, `cantSplit: true`, titre `keepNext: true`
- **Images** : paramètre `type` requis, conserver le ratio via `image-size`, PageBreak à l'intérieur d'un Paragraph
- **Ligne de tableau pleine page** : `rule: "exact"` avec marge de sécurité de 1200 twips

## Aide-mémoire des unités

| Unité | Valeur |
|------|-------|
| 1 cm | 567 twips |
| 1 inch | 1440 twips |
| 1 pt | 20 half-points |
| A4 | 11906 × 16838 twips |

Pour la table des tailles de police chinoises et les marges courantes, voir `references/common-rules.md`.

## Post-génération — vérification en deux couches

### Couche 1 : checklist manuelle (autocontrôle pendant la génération)

#### Format de base
- [ ] L'interligne est de 1,3x (`line: 312`) ou surcharge propre à la scène
- [ ] Le corps CJK a un retrait de 2 caractères (`firstLine: 480` ou `420`)
- [ ] Les tableaux ont des marges définies
- [ ] Les images conservent leur ratio via `image-size` — ne JAMAIS coder en dur largeur ET hauteur
- [ ] PageBreak à l'intérieur d'un Paragraph
- [ ] ShadingType utilise CLEAR
- [ ] Chaque liste numérotée utilise une `reference` unique
- [ ] **⚠️ CRITIQUE — Guillemets dans les chaînes JS correctement échappés.** Les guillemets courbes chinois (`""` `''`) DOIVENT utiliser les échappements Unicode (`\u201c` `\u201d` `\u2018` `\u2019`) ; les guillemets droits (`"` `'`) utilisent `\"` `\'` ou des délimiteurs alternés. **C'est le bug de génération de code le plus fréquent.** Le texte chinois contient souvent `""` pour l'emphase ou les noms propres (p. ex. "双11", "前低后高", "618") — chaque occurrence DOIT être échappée. Un échappement manquant produit des erreurs de syntaxe JS qui cassent silencieusement la génération du document.
- [ ] ImageRun inclut le paramètre `type`
- [ ] En-tête/pied de page présents (sauf indication contraire de la scène)

#### Styles de titres
- [ ] Tous les titres de chapitres du corps utilisent `heading: HeadingLevel.HEADING_X` (jamais simulés par gras + grande police)
- [ ] Le titre de couverture peut ignorer le style Heading (absent de la table des matières), mais les titres du corps DOIVENT utiliser le style Heading

#### Sauts de page et prévention des pages blanches
- [ ] Couverture/contenu dans des sections séparées
- [ ] Trois règles pour prévenir les pages blanches :
  - ① avec section(NEXT_PAGE), la section précédente ne doit PAS se terminer par un PageBreak (double saut = page blanche)
  - ② le paragraphe avec PageBreak DEVRAIT contenir du texte visible — **exception** : paragraphe vide de fin de section + PageBreak autorisé (séparateur de section normal, p. ex. après la couverture)
  - ③ pas plus de 3 paragraphes vides consécutifs
- [ ] La hauteur de ligne des tableaux pleine page utilise `rule: "exact"` (jamais `"atLeast"` pour les grands tableaux)
- [ ] Aucune page blanche non désirée (vérifier la fin de chaque section)

#### TOC (table des matières)
→ Voir `references/toc.md` pour la référence TOC complète et la checklist.
- [ ] Si un titre de TOC existe → l'élément `TableOfContents` doit être présent
- [ ] **⚠️ OBLIGATOIRE PageBreak après TableOfContents** — un Paragraph contenant un PageBreak DOIT suivre immédiatement l'élément `TableOfContents` ; sinon la TOC et le corps s'afficheront sur la même page. C'est l'erreur de mise en forme TOC n°1 — ne jamais l'omettre
- [ ] `add_toc_placeholders.py --auto` s'exécute après la génération ; code de sortie = 0
- [ ] **La TOC DOIT être dans sa propre section** — la section du corps définit `page: { pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } }` pour que la numérotation commence à la première page du corps, et non aux pages de la TOC
- [ ] **Imbrication de l'API de numérotation de page** — `pageNumbers` DOIT être dans `page: {}`, PAS au niveau supérieur des propriétés (voir toc.md § Page Number API)
- [ ] **Numérotation sur 3 sections** — Couverture (pas de n°) → Pages liminaires (romains i, ii, iii, start=1) → Corps (arabes 1, 2, 3, start=1)
- [ ] **Post-traiter les pieds de page** — l'instrText du pied de page de la section romaine doit contenir `PAGE \* ROMAN \* MERGEFORMAT` ; celui de la section arabe `PAGE \* arabic \* MERGEFORMAT` (WPS ignore pgNumType fmt). **⚠️ Ne JAMAIS utiliser `\* decimal` dans instrText** — `decimal` est une valeur d'énum de l'API docx-js (`NumberFormat.DECIMAL`), PAS un commutateur de champ Word valide ; l'utiliser rend les numéros de page « 1decimal », « 2decimal ». Le commutateur de champ Word correct pour les chiffres arabes est `\* arabic`.
- [ ] **Supprimer pgNumType vide** — post-traiter pour retirer `<w:pgNumType/>` de la section de couverture (docx-js émet un élément vide qui perturbe WPS)
- [ ] **⚠️ Indication de rafraîchissement de la TOC OBLIGATOIRE** — entre l'élément `TableOfContents` et le PageBreak, DOIT figurer un paragraphe de note grise en italique invitant l'utilisateur à faire un clic droit sur la TOC → « Mettre à jour les champs » pour rafraîchir les numéros de page (voir toc.md § TOC Refresh Hint)

#### Tableaux multi-pages
- [ ] Lignes d'en-tête : `tableHeader: true`
- [ ] Toutes les lignes : `cantSplit: true`
- [ ] Paragraphe de titre : `keepNext: true`

#### Couverture
- [ ] **La couverture DOIT utiliser une recette validée (R1–R7)** de `design-system.md` — le code de couverture libre est interdit
- [ ] La recette de couverture correspond au type de document (selon `selectCoverRecipe()` dans `design-system.md`)
- [ ] La couverture utilise la table englobante externe 16838 avec `allNoBorders` (toutes les recettes la fournissent)
- [ ] Le titre de couverture utilise `calcTitleLayout()` — jamais de taille de police codée en dur au-delà de 40pt
- [ ] Les espacements de couverture utilisent `calcCoverSpacing()` — jamais de grandes valeurs d'espacement codées en dur
- [ ] Le contenu de couverture ne déborde pas (hauteur totale ≤ 15638 twips, la Table utilise `rule: "exact"`)
- [ ] Chaque TextRun sur fond sombre/coloré a une `color` explicite (Règle 9 — ne jamais se fier au noir par défaut)
- [ ] La section de couverture n'a pas de PageBreak final ni de paragraphes vides traînants
- [ ] Les lignes du titre sont coupées aux frontières sémantiques (pas de coupure en milieu de mot, pas de ligne orpheline d'un seul caractère)
- [ ] Pas de lignes décoratives en caractères (`───`, `━━━`) — uniquement des bordures de paragraphe

### Couche 2 : script de post-vérification automatisé

```bash
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
```

Vérifie automatiquement 14 règles métier : pages blanches, **débordement de couverture (taille de police/espacement/contenu traînant)**, cohérence de l'interligne, marges des tableaux, contrôle multi-pages des tableaux (cantSplit/tblHeader), débordement d'images, distorsion du ratio d'images, repli de police, retrait CJK, hiérarchie des titres, mauvais usage de ShadingType, qualité de la TOC, propreté du document (textes placeholder/résidus Markdown/HTML), qualité du contenu des rapports (présence de l'abstract/spécificité des titres/détection des conclusions vagues).

⚠️ **Après la génération de tout document, il faut impérativement exécuter postcheck.py et corriger toutes les erreurs ❌.**

## Formules mathématiques

La saisie des formules utilise la **syntaxe LaTeX**, convertie en interne en objets Math docx-js.

- **Formules simples** (fractions, indices/exposants, racines, sommations) → composants Math docx-js
- **Formules complexes** (imbrication ≥ 3, matrices, fonctions par morceaux) → repli PNG matplotlib

Voir `references/math-formulas.md`.

## Graphiques

Par défaut : **bibliothèque de templates matplotlib** qui génère des PNG à intégrer.

6 templates prêts à l'emploi : barres, lignes, secteurs, boîtes, radar, heatmap.
Les couleurs sont dérivées automatiquement de la palette.accent du document pour la cohérence stylistique.
Palette par défaut : Morandi basse saturation (voir design-system.md).

Voir `references/chart-templates.md`.

## Dépendances

- **pandoc** : extraction de texte
- **docx** : `bun add docx` ou `npm install docx` (création)
- **LibreOffice** : conversion PDF, support .doc
- **Poppler** : PDF vers image (`pdftoppm`)
- **defusedxml** : analyse XML sécurisée
- **python-docx** : opérations de commentaires simples
