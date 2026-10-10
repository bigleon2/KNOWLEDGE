---
name: xlsx
version: "1.1.0"
category: "Documents & Contenu"
tags:
  - xlsx
metadata:
  author: Z.AI
  version: "1.1"
description: "Utilise ce skill chaque fois qu'un fichier tableur est l'entrée ou la sortie principale. Cela couvre toute tâche où l'utilisateur souhaite : ouvrir, lire, modifier ou réparer un fichier .xlsx, .xlsm, .csv ou .tsv existant ; créer un nouveau tableur de zéro ou à partir d'autres sources de données ; analyser des données et produire les résultats dans un fichier Excel avec graphiques ; convertir entre formats tabulaires (CSV/JSON/PDF → XLSX ou inversement) ; nettoyer, fusionner, pivoter ou transformer des données tabulaires. Déclenchement tout particulièrement lorsque l'utilisateur mentionne un fichier tableur par nom ou chemin, dit « fais un tableau/un rapport/un modèle », mentionne Excel/CSV/analyse de données/rapports/synthèse, ou souhaite une visualisation de données dans un tableur."
license: Proprietary. LICENSE.txt has complete terms
language: fr

read_when:
  - Déclencher quand la demande concerne : "Utilise ce skill chaque fois qu'un fichier tableur est l'entrée ou la sortie principale
  - Déclencher si la demande mentionne : données, fichier, tableur
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# XLSX — Atelier de tableurs piloté par scénarios

## Configuration rapide

```bash
bash "$XLSX_SKILL_DIR/setup.sh"    # Interactive environment check + install
```
## Pré-flight : filtre d'intention

Avant d'écrire la moindre ligne de code, confirmez que l'utilisateur a réellement besoin d'un tableur :

- Rapport / synthèse d'analyse (compte rendu, rapport d'étude) → **skill docx**
- Présentation (compte rendu, exposé, pitch deck) → **skill pptx**
- Document imprimé formel (contrat, certificat, « PDF ») → **skill pdf**
- Graphiques uniquement, sans tableau de données → **skill charts**
- L'utilisateur indique explicitement un format → le respecter

Si c'est bien du xlsx → passez au Scene Router ci-dessous.

**Décomposition de la demande** (à faire à chaque fois) :
- **Besoins explicites** : feuilles, colonnes, formules, métriques énoncées par l'utilisateur
- **Besoins implicites** : contexte métier, usage en aval (filtrer ? trier ? saisir ?)
- **Demandes en plusieurs parties** : générez TOUTES les parties — n'abandonnez jamais silencieusement un composant

**Détection multi-intentions** — certaines demandes combinent plusieurs scénarios :

```
"Create a financial model with charts and export a PDF summary"
 → scenes/finance.md + engines/chart.md + (hand off PDF to pdf skill)

"Analyze this CSV, build a dashboard, and make it look professional"
 → scenes/analyze.md + engines/chart.md + engines/design.md

"Edit this budget file, add a new quarter column, and create a pivot"
 → scenes/edit.md + quality/pipeline.md (pivot command)

"Convert these 5 CSVs into one xlsx with a summary sheet"
 → scenes/convert.md + scenes/create.md (for summary)
```

Lorsque plusieurs intentions sont détectées, chargez tous les fichiers correspondants et exécutez dans l'ordre logique : préparation des données → analyse → visualisation → style → QA.

---

## Complexity Gate (à évaluer AVANT le Scene Router)

Déterminez la complexité de la tâche pour contrôler la profondeur de chargement des fichiers :

```
User Request
│
├─ LITE (single aggregation, simple chart, direct conversion, QA-only)
│  → Load: SKILL.md + ONE scene file (lean version)
│  → Skip: engine files (use built-in knowledge for basic styles)
│  → QA: audit + validate only
│  → Target: ≤ 400 lines total context
│
└─ FULL (multi-dimensional analysis, financial model, dashboard, KANO, etc.)
   → Load: SKILL.md + scene + engines (chart.md / design.md) as needed
   → For code patterns: load recipes/templates files ON DEMAND (not upfront)
   → QA: full pipeline (recalc → audit → scan → chart-verify → validate)
   → Target: load recipes/templates only when stuck on implementation
```

**Déclencheurs LITE** : un seul groupby, un graphique, conversion de format, inspect/audit/validate, pivot simple
**Déclencheurs FULL** : matrice de corrélation, tableau de bord multi-feuilles, analyse statistique, modèle financier, KANO/funnel/cohort

---

## Scene Router

```
Demande de l'utilisateur
│
├─ Concerne un fichier existant ?
│  ├─ Oui → Modifier le contenu ou la structure ?
│  │         ├─ Oui ──────────────────── → scenes/edit.md
│  │         └─ Non (lecture/analyse seule) ─ → scenes/analyze.md
│  │
│  └─ Conversion de format (CSV↔XLSX, JSON, tableaux PDF) ?
│     └─ Oui ────────────────────────── → scenes/convert.md
│
├─ Créer de zéro ?
│  ├─ Financier / budget / prévisionnel / suivi de coûts ?
│  │  ├─ Complexe (DCF / LBO / trois états liés / sensitivity / modèle IB) ?
│  │  │  └─ Oui ─────────────────────── → scenes/finance.md
│  │  └─ Simple (tableau de budget / note de frais / recettes vs dépenses / coût de projet / comptabilité personnelle) ?
│  │     └─ Oui ─────────────────────── → scenes/finance_lite.md
│  └─ Tableau général / rapport / modèle
│     └─ ──────────────────────────── → scenes/create.md
│
├─ Traitement par lots / gros fichiers / protection / validation ?
│  └─ Oui ───────────────────────────── → scenes/advanced.md
│
├─ VBA / macros / automatisation dans Excel ?
│  └─ Oui ───────────────────────────── → scenes/vba.md + engines/vba-templates.md
│
├─ Besoin de graphiques ou de visualisation de données ?
│  └─ Oui ───────────── ajouter ────────→ engines/chart.md
│
└─ Besoin de style / design system ?
   └─ Oui ───────────── ajouter ────────→ engines/design.md
```

**Demandes mixtes** : chargez tous les fichiers correspondants. Les fichiers engine s'ajoutent toujours (**append**) à un scénario.

**Détection finance** :
- **finance.md** (complexe) : DCF, LBO, P&L, compte de résultat, bilan, valuation, valorisation, IRR, trois états financiers liés, sensitivity, scenario
- **finance_lite.md** (simple) : budget, prévisionnel, dépenses, expense, recettes/dépenses, comptabilité, coût de projet, cost tracking, notes de frais, ROI

**Détection VBA** : macro, VBA, automatisation, automation, .xlsm, bouton, button, auto-run, script de traitement par lots

---

## Principes de conception

### 1. Garantie de formules vivantes
Chaque valeur dérivée DEVRAIT être une formule Excel afin que le tableur reste dynamique.

**Exception — vérification programmatique** : lorsque le fichier de sortie sera vérifié par Python (sans être ouvert dans Excel), les lignes TOTAL/SUM doivent écrire des **valeurs calculées** au lieu de formules, car openpyxl ne peut pas évaluer les formules et `data_only=True` renvoie `None` pour les formules fraîchement écrites. Ajoutez éventuellement la formule en commentaire de cellule pour référence.

### 2. Tolérance zéro erreur
Les livrables ne doivent contenir aucune erreur de formule. Toutes les divisions enveloppées avec `IFERROR` ou `IF(denom=0,...)`. Références absolues (`$C$42`) pour les dénominateurs partagés.

### 3. Compatibilité d'abord
Pas de fonctions de tableaux dynamiques (`FILTER`, `UNIQUE`, `XLOOKUP`, `SORT`, `SORTBY`, `XMATCH`, `SEQUENCE`, `LET`, `LAMBDA`, `RANDARRAY`). Pas de formules de tableau implicites — utilisez des alternatives avec `SUMPRODUCT`.

### 4. Préserver et reproduire
Lors de la modification de fichiers existants : étudiez et reproduisez exactement le format, le style, les conventions. Les motifs existants l'emportent toujours sur les valeurs par défaut. Le texte commençant par `=` doit être préfixé par `'`.

### 5. Miroir de langue
La langue de sortie (noms de feuilles, en-têtes, libellés) correspond à la langue d'entrée de l'utilisateur.

### 6. Cohérence des données avant les instructions
Lorsque les instructions de l'utilisateur contredisent les motifs de données réels du fichier existant :
- **Priorité 1** : respecter le motif de données existant (ex. si les données existantes utilisent `0` pour vide, ne pas passer à `-`)
- **Priorité 2** : suivre littéralement les instructions de l'utilisateur
- Toujours signaler le conflit à l'utilisateur

Exemple : l'utilisateur dit « afficher un tiret pour zéro » mais les données existantes et la clé de réponse utilisent le numérique `0` → utilisez `0` et signalez l'écart à l'utilisateur.

---

## Chaîne d'outils

### Configuration du chemin des scripts (OBLIGATOIRE avant tout appel de script)

Tous les outils CLI se situent par rapport au répertoire de ce skill. Avant d'appeler un script, résolvez une fois pour toutes le chemin absolu :

```bash
XLSX_SKILL_DIR="<skill_directory>"   # ← parent directory of this SKILL.md

# Then all commands use absolute paths:
python3 "$XLSX_SKILL_DIR/xlsx.py" inspect data.xlsx --pretty
python3 "$XLSX_SKILL_DIR/xlsx.py" pivot data.xlsx output.xlsx --rows Region --values Revenue
python3 "$XLSX_SKILL_DIR/xlsx.py" validate output.xlsx
```

**Pour les imports Python** (lorsque le code de génération doit importer les modules du skill) :

```python
import sys, os
XLSX_SKILL_DIR = "<skill_directory>"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)
```

**⚠️ N'utilisez JAMAIS un `python3 xlsx.py ...` nu** — cela ne fonctionne que si le répertoire courant (cwd) se trouve être celui du skill. Utilisez toujours le chemin absolu.

### Référence des outils

| Outil | Usage |
|------|-----|
| **openpyxl** | Formules, formatage, graphiques, contrôle au niveau cellule |
| **pandas** | Analyse de données, opérations en masse, CSV/TSV |
| `load_workbook(read_only=True)` | Lectures de gros fichiers |
| `Workbook(write_only=True)` | Écritures de gros fichiers |
| **templates/base.py** | Design tokens, résolution des polices, fabriques de styles, utilitaires (source unique de vérité) |
| **xlsx.py** | Commandes QA (voir `quality/pipeline.md`) |

Métadonnées du classeur : `wb.properties.creator = "Z.ai"`

> **Tout le code doit importer depuis `templates/base.py`** pour les couleurs, les polices et les helpers de style. Ne codez jamais en dur de valeurs hexadécimales ni de noms de polices.

---

## Porte qualité

Chaque livrable doit passer le pipeline complet d'intégrité avant livraison.

→ **Chargez `quality/pipeline.md` pour le workflow d'intégrité basé sur les rôles.**

Référence rapide :
```
Blueprint → Build & Self-check (per-sheet) → Inspect → Pivot (if needed) → Release
```

---

## Matrice de capacités

| Capacité | Pris en charge | Scénario/Engine |
|-----------|-----------|-------------|
| Créer de zéro | ✅ | scenes/create |
| Modifier un fichier existant | ✅ | scenes/edit |
| Analyse de données et EDA | ✅ | scenes/analyze |
| Conversion de format | ✅ | scenes/convert |
| Modèles financiers (DCF/LBO/P&L) | ✅ | scenes/finance |
| Budgets et dépenses simples | ✅ | scenes/finance_lite |
| Macros VBA et automatisation | ✅ | scenes/vba + engines/vba-templates |
| Traitement par lots | ✅ | scenes/advanced |
| Graphiques intégrés | ✅ | engines/chart |
| Recommandation intelligente de graphiques | ✅ | engines/chart |
| Design system et style | ✅ | engines/design |
| Création de tableaux croisés (pivot) | ✅ | quality/pipeline (pivot cmd) |
| Validation des formules | ✅ | quality/pipeline |
| Validation structurelle | ✅ | quality/pipeline |
| Traçabilité de la provenance des données | ✅ | scenes/analyze |
| Gestion de gros fichiers | ✅ | scenes/advanced |
| Protection et verrouillage des données | ✅ | scenes/advanced |
