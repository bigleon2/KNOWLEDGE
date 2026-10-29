---
nom: cheat-sheet
source: skills/cheat-sheet/SKILL.md
sha256_source: 2f816a0ee18b
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — cheat-sheet (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/cheat-sheet/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: cheat-sheet
description: Transformer des supports d'apprentissage PDF/Word/Markdown en fiches de synthèse condensée. Trois styles (fiches de repérage / carte mentale / questions-réponses), sortie PDF deux colonnes en petit corps. Se déclenche quand l'utilisateur dit « génère des fiches de synthèse », « génère une Cheatsheet », « fais-moi une table de repérage rapide », « condense ce document en une page », « fais des fiches de savoir ». **Ne traite pas** : la génération de quiz à partir d'un support (→ quiz-mastery), les projets d'apprentissage au long cours (→ study-buddy).
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Générateur de Cheatsheet

## Ce que vous faites

Compresser les supports d'apprentissage de l'utilisateur (PDF/Word/Markdown/texte) en une Cheatsheet **deux colonnes, petit corps, forte densité informationnelle** (format PDF).

**Principe fondamental : ne garder que l'essentiel, couper le remplissage.**

---

## ⚠️ Règle de fer : éviter les créations en doublon

Avant de générer une Cheatsheet, **scanner d'abord le répertoire de sortie** pour vérifier l'absence d'un fichier sur le même sujet :
- **Existant** → demander à l'utilisateur « il existe déjà un [nom de fichier], écraser / en créer un nouveau / passer ? » et attendre sa réponse avant d'agir
- **Inexistant** → générer directement
- **Jamais** d'écrasement sans avoir demandé

---

## Workflow

### Étape 1 : recevoir le support

L'utilisateur fournit un fichier de support, formats acceptés :
- `.pdf` — passer par la route process du skill PDF pour extraire le texte
- `.docx` — passer par la route process du skill PDF pour extraire le texte
- `.md` / `.txt` — lecture directe

**Commandes d'extraction de texte :**
```bash
# Extraire le texte d'un PDF
python3 "$PDF_SCRIPTS/pdf.py" extract.text <file_path>

# Convertir un Word en PDF puis extraire (si nécessaire)
python3 "$PDF_SCRIPTS/pdf.py" convert.office <file_path>
```

`$PDF_SCRIPTS` est le chemin du répertoire scripts du skill PDF, à déduire de l'emplacement du SKILL.md du skill PDF.

Si l'utilisateur colle directement le texte au lieu d'un fichier, sauter l'extraction et utiliser le texte tel quel.

---

### Étape 2 : choisir le style

**Demander obligatoirement à l'utilisateur** le style voulu (ne pas choisir à sa place) :

Présenter les options suivantes :
1. 📋 **Fiches de repérage** — concepts clés + définitions + formules/points essentiels, repérables d'un coup d'œil, idéal pour réviser à la dernière minute
2. 🌳 **Style carte mentale** — organisation hiérarchique (grand titre → sous-titres → points), vue d'ensemble structurée, idéal pour cartographier un domaine
3. ❓ **Style questions-réponses** — transformer les points de savoir en paires « question → réponse », idéal pour l'auto-évaluation

Une fois le choix fait, passer à l'étape 3.

---

### Étape 3 : distillation par LLM

Selon le style choisi, construire le prompt correspondant pour que le LLM distille le contenu de la cheatsheet à partir de l'original.

#### Style 1 : fiches de repérage

Règles de distillation :
- Extraire tous les concepts clés, définitions, formules, données essentielles
- Chaque point au format **terme : explication en une phrase**
- Regrouper les points liés, chaque groupe avec son sous-titre
- Conserver telles quelles les formules/extraits de code importants
- Couper tous les exemples, phrases de transition, mises en contexte

Structure de sortie :
```
## [titre de groupe]
- **Terme A** : définition en une phrase
- **Terme B** : définition en une phrase
- 📐 Formule : `contenu de la formule`

## [titre de groupe]
...
```

#### Style 2 : carte mentale

Règles de distillation :
- Extraire la structure hiérarchique du document (chapitre → section → point)
- Chaque nœud résumé dans la formulation la plus brève
- 3 niveaux de profondeur maximum (au-delà, tout ne tient plus sur une page)
- Exprimer la hiérarchie par indentation et symboles

Structure de sortie :
```
# Sujet

## Branche de niveau 1
  ├─ Point de niveau 2
  │   ├─ Détail 1
  │   └─ Détail 2
  └─ Point de niveau 2
      └─ Détail
```

#### Style 3 : questions-réponses

Règles de distillation :
- Transformer chaque point de savoir en une question
- Réponses tenues en 1 à 3 phrases
- Questions ordonnées du basique à l'avancé
- Les concepts confusables donnent des questions de discrimination

Structure de sortie :
```
## [groupe thématique]

**Q : Qu'est-ce que XXX ?**
A : réponse en une phrase.

**Q : Différence entre XXX et YYY ?**
A : comparaison brève.
```

---

### Étape 4 : validation et ajustements par l'utilisateur

Après la génération, **présenter d'abord le contenu sous forme de texte** et demander :

> « Le contenu est prêt, voulez-vous ajuster quelque chose ? Par exemple :
> - mettre en évidence certaines parties ?
> - supprimer ou compléter certains contenus ?
> - des préférences de mise en page ? (corps un peu plus petit, distinction par couleur de section, etc.) »

Après le « OK » de l'utilisateur, passer à l'étape 5.
Si l'utilisateur demande des modifications → ajuster → représenter → attendre la validation.

---

### Étape 5 : générer le PDF

Appeler la **route Report du skill PDF (ReportLab)** pour produire le PDF deux colonnes.

**Spécifications de mise en page (valeurs par défaut) :**

| Paramètre | Défaut | Description |
|------|--------|------|
| Format de page | A4 | ajustable à la demande |
| Colonnes | 2 | 2 par défaut, 1 possible à la demande |
| Corps du texte | 8pt | densité d'information d'abord, ajustable à la demande |
| Titres | 10pt (niveau 1) / 9pt (niveau 2) | |
| Interligne | 1.2 | compact mais lisible |
| Marges | 12 mm de chaque côté | maximiser la zone de contenu |
| Polices | UniSong/UniHei pour le chinois, Helvetica pour l'anglais | |

**Flux de génération :**

1. Convertir le Markdown distillé par le LLM en instructions de mise en page ReportLab
2. Appeler la route report du skill PDF pour générer le PDF
3. Communiquer à l'utilisateur le chemin du fichier produit

**En appelant le skill PDF, respecter toutes les règles de son SKILL.md**, y compris :
- contrôle des polices CJK
- protection contre le débordement des tableaux
- contrôle du taux de remplissage des pages
- réglage des métadonnées

---

### Étape 6 : livraison

Rendre à l'utilisateur :
- 📄 le chemin du fichier PDF
- la taille du fichier, le nombre de pages
- l'invitation à poursuivre les ajustements

---

## Points d'attention

### Qualité du contenu
- **Ne rien inventer** : tous les points de savoir doivent venir du texte d'origine, aucune improvisation
- **Ne rien oublier d'essentiel** : concepts clés, formules et définitions doivent être conservés
- **Garder la terminologie d'origine** : ne pas remplacer un terme technique de sa propre initiative

### Opérations sur les fichiers
- Le PDF produit va par défaut à la racine de l'espace de travail, nom de fichier : `fiches_[sujet]_[date].pdf`
- Pour la déduplication, voir plus haut « ⚠️ Règle de fer : éviter les créations en doublon »

---

## Relations avec les autres skills

| Skill | Relation |
|-------|------|
| skill PDF | appel de sa route process pour l'extraction de texte, de sa route report pour la génération du PDF |
| study-buddy | study-buddy peut recommander une cheatsheet quand l'utilisateur termine un projet d'apprentissage |
| quiz-mastery | pas de lien direct, mais le contenu d'une cheatsheet peut alimenter les points de savoir des quiz |

---

## Structure de fichiers

```
skills/cheat-sheet/
├── SKILL.md              ← ce fichier
```

Ce skill est un pur guide de flux, sans script propre. Toutes les opérations de fichiers et la génération du PDF passent par le skill PDF.


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
