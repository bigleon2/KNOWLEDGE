---
name: cheat-sheet
version: "1.0.0"
category: "Documents & Contenu"
tags:
  - cheat
  - sheet
description: Convertit des supports d'étude (PDF/Word/Markdown) en documents de fiches de révision condensées. Prend en charge trois styles (cartes de révision / carte mentale / Q&R) et produit un PDF compact à deux colonnes en petits caractères. Se déclenche quand l'utilisateur dit « génère une fiche de révision », « génère un Cheatsheet », « fais-moi un anti-sèche », « mets ce support sur une page », « fais une carte de connaissances ». **Ne gère pas** : créer des questions à partir du support (→ quiz-mastery), les projets d'apprentissage longue durée (→ study-buddy).
language: fr

read_when:
  - Déclencher quand la demande concerne : convertit des supports d'étude (PDF/Word/Markdown) en documents de fiches de révision condensées
  - Déclencher si la demande mentionne : révision, carte, génère
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Générateur de Cheatsheet

## Ce que vous faites

Compresser les supports d'étude de l'utilisateur (PDF/Word/Markdown/texte) en un document Cheatsheet **à deux colonnes, petits caractères, forte densité d'information** (format PDF).

**Principe fondamental : ne garder que l'essentiel, couper le superflu.**

---

## ⚠️ Règle d'or : éviter les doublons

Avant de générer un Cheatsheet, **scannez d'abord le répertoire de sortie** pour vérifier qu'il n'existe pas déjà un fichier sur le même thème :
- **Présent** → demandez à l'utilisateur « il existe déjà [nom du fichier], écraser / en créer une nouvelle / passer ? » et attendez la réponse avant d'agir
- **Absent** → générez directement
- **Jamais** d'écrasement sans demander

---

## Workflow

### Étape 1 : recevoir le support

L'utilisateur fournit un fichier de support d'étude, formats pris en charge :
- `.pdf` — utilisez la route process du skill PDF pour extraire le texte
- `.docx` — utilisez la route process du skill PDF pour extraire le texte
- `.md` / `.txt` — lecture directe

**Commandes d'extraction de texte :**
```bash
# PDF 提取文本
python3 "$PDF_SCRIPTS/pdf.py" extract.text <file_path>

# Word 转 PDF 后提取（如需要）
python3 "$PDF_SCRIPTS/pdf.py" convert.office <file_path>
```

Où `$PDF_SCRIPTS` est le chemin du répertoire scripts du skill PDF, à déduire de l'emplacement du SKILL.md du skill PDF.

Si l'utilisateur n'a pas fourni de fichier mais a collé directement du texte, sautez l'étape d'extraction et utilisez le texte tel quel.

---

### Étape 2 : choisir le style

**Demandez obligatoirement à l'utilisateur** quel style il veut (ne choisissez pas à sa place) :

Présentez à l'utilisateur les options suivantes :
1. 📋 **Cartes de révision de connaissances** — concepts clés + définitions + formules/points essentiels, d'un coup d'œil, idéal pour un bachotage avant examen
2. 🌳 **Style carte mentale** — organisé par hiérarchie (grand titre → sous-titre → points), avec une vraie structure en plan, idéal pour cartographier un système
3. ❓ **Style Q&R** — transformer les points de connaissances en paires « question → réponse », idéal pour l'auto-évaluation

Une fois l'utilisateur decidé, passez à l'étape 3.

---

### Étape 3 : distillation du contenu par le LLM

Selon le style choisi, construisez un prompt différent pour que le LLM extraie de l'original le contenu du cheatsheet.

#### Style 1 : cartes de révision de connaissances

Règles de distillation :
- Extraire tous les concepts clés, définitions, formules, données importantes
- Chaque point de connaissance au format **terme : explication en une phrase**
- Regrouper les points liés, chaque groupe ayant un petit titre
- Conserver telles quelles les formules/fragments de code importants
- Couper tous les exemples, phrases de transition et mises en contexte

Structure de sortie :
```
## [分组标题]
- **术语A**：一句话定义
- **术语B**：一句话定义
- 📐 公式：`公式内容`

## [分组标题]
...
```

#### Style 2 : carte mentale

Règles de distillation :
- Extraire la structure hiérarchique du document (chapitre → section → points)
- Résumer chaque nœud dans la langue la plus courte possible
- 3 niveaux de profondeur maximum (au-delà, ça ne tient plus sur une page)
- Exprimer la hiérarchie par l'indentation et les symboles

Structure de sortie :
```
# 主题

## 一级分支
  ├─ 二级要点
  │   ├─ 细节 1
  │   └─ 细节 2
  └─ 二级要点
      └─ 细节
```

#### Style 3 : Q&R

Règles de distillation :
- Transformer chaque point de connaissance en une question
- Réponses limitées à 1-3 phrases
- Questions classées du basique à l'avancé
- Créer des questions de discrimination pour les concepts confusants

Structure de sortie :
```
## [主题分组]

**Q：什么是 XXX？**
A：一句话回答。

**Q：XXX 和 YYY 的区别？**
A：简短对比。
```

---

### Étape 4 : confirmation et ajustement par l'utilisateur

Après la génération par le LLM, **présentez d'abord le contenu sous forme de texte** et demandez :

> « Le contenu est prêt, y a-t-il des ajustements à faire ? Par exemple :
> - Marquer certaines parties en évidence ?
> - Supprimer ou compléter certains contenus ?
> - Des préférences de mise en page ? (police plus petite, couleurs par section, etc.) »

Si l'utilisateur confirme « c'est bon », passez à l'étape 5.
Si l'utilisateur demande des modifications → ajustez le contenu → représentez → attendez la confirmation.

---

### Étape 5 : générer le PDF

Appelez la **route Report (ReportLab)** du skill PDF pour générer le PDF à deux colonnes.

**Spécifications de mise en page (valeurs par défaut) :**

| Paramètre | Valeur par défaut | Commentaire |
|------|--------|------|
| Format de page | A4 | ajustable à la demande de l'utilisateur |
| Colonnes | deux | deux par défaut, une colonne possible sur demande |
| Corps du texte | 8pt | densité d'information prioritaire, ajustable à la demande |
| Taille des titres | 10pt (niveau 1) / 9pt (niveau 2) | |
| Interligne | 1.2 | compact mais lisible |
| Marges | 12mm en haut, en bas et sur les côtés | maximise la zone de contenu |
| Polices | UniSong/UniHei pour le chinois, Helvetica pour le latin | |

**Flux de génération :**

1. Convertir le contenu Markdown distillé par le LLM en instructions de mise en page ReportLab
2. Appeler la route report du skill PDF pour générer le PDF
3. Indiquer à l'utilisateur le chemin du fichier généré

**En appelant le skill PDF, respectez toutes les règles de son SKILL.md**, notamment :
- Vérification des polices CJK
- Protection contre le débordement des tableaux
- Contrôle du taux de remplissage de la page
- Réglage des métadonnées

---

### Étape 6 : livraison

Sortir pour l'utilisateur :
- 📄 Chemin du fichier PDF
- Taille du fichier, nombre de pages
- Rappel que l'utilisateur peut continuer à ajuster

---

## Points d'attention

### Qualité du contenu
- **N'inventez rien** : tous les points de connaissance doivent provenir de l'original, aucune libre création
- **N'omettez rien d'essentiel** : concepts clés, formules et définitions doivent être conservés
- **Conservez la terminologie d'origine** : ne remplacez pas les termes techniques de votre propre chef

### Opérations sur les fichiers
- Le PDF généré est enregistré par défaut à la racine de l'espace de travail, nom au format : `知识浓缩卡_[主题]_[日期].pdf`
- Le contrôle des doublons est décrit ci-dessus : « ⚠️ Règle d'or : éviter les doublons »

---

## Relations avec les autres skills

| Skill | Relation |
|-------|------|
| Skill PDF | appelle sa route process pour extraire le texte, sa route report pour générer le PDF |
| study-buddy | study-buddy peut suggérer de générer un cheatsheet une fois le projet d'apprentissage terminé |
| quiz-mastery | pas de lien direct, mais le contenu du cheatsheet peut servir de source de points de connaissances pour créer des questions |

---

## Structure des fichiers

```
skills/cheat-sheet/
├── SKILL.md              ← 当前文件
```

Ce skill est un pur guide de processus, sans script autonome. Toutes les opérations de fichiers et la génération du PDF passent par le skill PDF.
