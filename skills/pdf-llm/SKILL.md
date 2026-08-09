---
name: pdf-llm
version: 1.0.0
category: metier
language: fr
description: >
  Extraction documentaire PDF vers Markdown + JSON structuré RAG-ready. Active ce skill chaque fois que l'utilisateur demande d'extraire, analyser, structurer, convertir en Markdown/JSON le contenu d'un PDF, d'un document scanné, ou de toute sortie OCR. Fonctionne en 4 modes : qwen (extraction littérale), glm (structuré RAG-friendly), multi (universel par défaut), ou pipeline (normalisation post-PyMuPDF). Zéro hallucination, fidélité totale au document. Aussi lorsque l'utilisateur parle de RAG, d'indexation de documents, de vectorisation de PDF, de chunking documentaire, d'extraction de tableaux/images, ou d'OCR.
  
tags: []
dependencies: []
license: MIT
---

# PDF-LLM — Extraction Documentaire RAG-Ready
### Compatible : Qwen 2.5 · GLM-5.2 · GPT · Claude · LM Studio

---

## Architecture : Script + LLM

Ce skill fonctionne en **deux étapes** avec des responsabilités clairement
séparées :

```
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 — SCRIPT (automatisée, mode-agnostic)              │
│  scripts/extract_pdf.py                                      │
│                                                             │
│  Responsabilité : extraction BRUTE des données PDF           │
│  - Texte page par page                                       │
│  - Métadonnées PDF natives                                   │
│  - Tableaux (via page.find_tables())                        │
│  - Images (métadonnées + BBox)                               │
│  - Liens, signets, polices                                   │
│  - Détection en-têtes/pieds                                 │
│  - Détection OCR heuristique                                 │
│                                                             │
│  Le script ne gère AUCUN mode. Il est mode-agnostic.        │
│  Il ne normalise pas, ne reformule pas, n'interprète pas.   │
├─────────────────────────────────────────────────────────────┤
│  ÉTAPE 2 — LLM (intelligence, mode-dépendant)               │
│                                                             │
│  Responsabilité : traitement et mise en forme                │
│  - Menu décisionnel (résolution du contexte)                 │
│  - Choix du mode (qwen/glm/multi/pipeline)                  │
│  - Normalisation du contenu (mode pipeline uniquement)       │
│  - Construction de la hiérarchie Markdown (H1→H4)            │
│  - Génération du JSON RAG-ready                              │
│  - Application des règles R1-R9                               │
│  - OCR avancé et marqueurs [[? mot]] (si applicable)        │
└─────────────────────────────────────────────────────────────┘
```

### Qui produit quoi ?

| Fichier | Producteur | Description |
|---------|-----------|-------------|
| `document_raw.txt` | Script | Texte brut page par page (dump intermédiaire) |
| `document_metadata.json` | Script | Métadonnées PDF natives |
| `document_pages.json` | Script | Détail page par page (texte, images, tableaux, blocs) |
| `document_links.json` | Script | Liens hypertexte |
| `document_bookmarks.json` | Script | Signets/TOC intégrés |
| `document_fonts.json` | Script | Polices, tailles et couleurs (données brutes pour LLM) |
| `document_headers_footers.json` | Script | Patterns en-têtes/pieds de page |
| `<nom>_extrait.md` | **LLM** | Markdown hiérarchisé final (H1→H4, tableaux, images) |
| `<nom>_rag.json` | **LLM** | JSON structuré RAG-ready (schéma universel) |
| `<nom>_brut.txt` | **LLM** | Texte brut nettoyé, segmenté (optionnel) |

---

## MENU DÉCISIONNEL — Point d'entrée obligatoire (LLM)

**Quand ce skill est activé, le LLM TOUJOURS commence par ce menu.**
Posez ces questions à l'utilisateur (ou déduisez les réponses du
contexte) avant toute action :

```
╔══════════════════════════════════════════════════════════════╗
║  PDF-LLM — Menu de démarrage                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ① SOURCE DU DOCUMENT                                       ║
║     [a] Fichier PDF (chemin ou upload)                       ║
║     [b] Texte collé dans le prompt                           ║
║     [c] Sortie PyMuPDF brute (pipeline)                     ║
║     [d] Document scanné (OCR)                                 ║
║                                                              ║
║  ② MODE D'EXTRACTION                                        ║
║     [1] qwen   — Extraction stricte, zéro hallucination     ║
║     [2] glm    — Structurée, RAG-friendly, annotations      ║
║     [3] multi  — Universel, compatibilité maximale (défaut)  ║
║     [4] pipeline— Normalisation post-PyMuPDF                ║
║                                                              ║
║  ③ SORTIES SOUHAITÉES                                       ║
║     [A] Markdown hiérarchisé (.md)                           ║
║     [B] JSON RAG-ready (.json)                               ║
║     [C] Texte brut propre (.txt)                             ║
║     [D] Tous les formats                                     ║
║                                                              ║
║  ④ OPTIONS SUPPLÉMENTAIRES                                   ║
║     [i] Extraction des images (BBox + OCR)                  ║
║     [l] Extraction des liens/signets                        ║
║     [f] Analyse des polices/tailles/couleurs                 ║
║     [r] Nettoyage en-têtes/pieds pour RAG                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Règles du menu

1. Si l'utilisateur a déjà fourni un PDF → **① = [a]** automatiquement
2. Si l'utilisateur ne précise pas le mode → **② = [3] multi** par défaut
3. Si l'utilisateur ne précise pas les sorties → **③ = [D]** tous les formats
4. Les options ④ sont activées automatiquement selon le contexte :
   - Mode **pipeline** → [i] et [r] activés par défaut
   - Mode **glm** → [i] et [l] activés par défaut
   - Mode **qwen** → [i] et [l] activés par défaut
   - Mode **multi** → [i] activé par défaut

### Alias de compatibilité (mapping LLM)

Les anciens noms de mode sont acceptés et redirigés silencieusement
par le LLM (pas par le script) :

| Ancien nom | Nouveau nom | Comportement |
|------------|-------------|--------------|
| strict | qwen | Identique |
| structuré | glm | Identique |

---

## Flux de travail

```
PDF source (upload / chemin / texte collé)
        │
        ▼
  [0] Menu décisionnel (LLM)
        │   → Résoudre : source, mode, sorties, options
        ▼
  [1] Extraction brute (Script)
        │   → python extract_pdf.py --full
        │   → 7 fichiers intermédiaires
        ▼
  [2] Traitement + Normalisation (LLM)
        │   → Mode choisi (qwen/glm/multi/pipeline)
        │   → Règles R1-R9
        │   → Construction hiérarchie Markdown
        │   → JSON RAG-ready
        ▼
  [3] Sortie finale (LLM)
        → <nom>_extrait.md + <nom>_rag.json (+ optionnel .txt)
        → Sauvegardés dans /home/z/my-project/download/
```

---

## Étape 1 — Extraction brute (Script)

### Si un fichier PDF est fourni — Source [a] ou [d]

Exécuter le script d'extraction PyMuPDF :

```bash
PDF_LLM_DIR="/home/z/my-project/skills/pdf-llm"
python "$PDF_LLM_DIR/scripts/extract_pdf.py" \
  --input "/chemin/du/document.pdf" \
  --output "/home/z/my-project/download/" \
  --full
```

Le flag `--full` active toutes les options d'extraction :
- `--links` : Extraction des liens hypertexte
- `--bookmarks` : Extraction des signets PDF (TOC intégré)
- `--fonts` : Analyse des polices/tailles/couleurs (données brutes pour le LLM)
- `--rag-cleanup` : Détection en-têtes/pieds de page
- `--extract-images` : Extraire les images sur disque (option supplémentaire)

Le script produit **7 fichiers intermédiaires** :

| Fichier | Contenu |
|---------|---------|
| `document_raw.txt` | Texte extrait page par page |
| `document_metadata.json` | Métadonnées PDF natives |
| `document_pages.json` | Détail page par page (texte, images, tableaux, blocs, flags OCR) |
| `document_links.json` | Liens hypertexte (URL + texte d'ancre + page) |
| `document_bookmarks.json` | Signets/TOC intégrés du PDF |
| `document_fonts.json` | Polices, tailles et couleurs (données brutes pour le LLM) |
| `document_headers_footers.json` | Patterns en-têtes/pieds de page |

**Tous les fichiers sont TOUJOURS créés** (même vides) quand `--full` est activé.
Cela garantit que le LLM peut les lire sans erreur.

### Si le texte est fourni directement — Source [b]

Utiliser le texte tel quel. Passer directement à l'étape 2.
Déterminer les métadonnées à partir du contenu ou les marquer
`"NON PRÉSENT DANS LE DOCUMENT"`.

### Si la sortie PyMuPDF est fournie — Source [c]

Utiliser les fichiers intermédiaires existants. Passer directement
à l'étape 2 en mode **pipeline**.

### Gestion des erreurs par le script

| Situation | Comportement du script |
|-----------|----------------------|
| PDF protégé/chiffré | Signale `"DOCUMENT PROTÉGÉ — extraction impossible"`, écrit un JSON d'erreur, quitte |
| PDF corrompu | Tente chaque page, signale les pages corrompues, continue pour les pages valides |
| PDF vide (0 page) | Signale `"DOCUMENT VIDE"`, écrit un JSON d'erreur, quitte |
| Fichier introuvable | Signale `"ERREUR: Fichier introuvable"`, quitte |

---

## Étape 2 — Traitement + Normalisation (LLM)

### Choisir le mode

Chaque mode a un fichier de référence dédié :

| Mode | Fichier de référence | Quand l'utiliser |
|------|----------------------|------------------|
| **qwen** | `references/mode-qwen.md` | Extraction littérale, fidélité absolue, Qwen 2.5 |
| **glm** | `references/mode-glm.md` | Structurée, RAG-friendly, annotations sémantiques, GLM |
| **multi** | `references/mode-multi.md` | Universel par défaut, compatibilité maximale |
| **pipeline** | `references/mode-pipeline.md` | Normalisation post-PyMuPDF, nettoyage artefacts |

### Compatibilité LLM recommandée

| LLM / Agent | Mode recommandé | Raison |
|-------------|-----------------|--------|
| Qwen 2.5 | **qwen** | Fidélité littérale, tolérance zéro, prompts courts |
| GLM (Z.ai) | **glm** | Annotations sémantiques natives, RAG-friendly |
| GPT / ChatGPT | **multi** | Compatibilité maximale, format universel |
| Claude | **multi** | Gestion robuste du format universel |
| LM Studio (local) | **multi** | Adapté à tout modèle local chargé |
| Pipeline automatisé | **pipeline** | Sortie PyMuPDF brute nécessite normalisation |

**Si l'utilisateur ne précise ni le LLM ni le mode → mode = multi par défaut.**

---

## Étape 3 — Sortie finale (LLM)

La sortie se fait **toujours** dans cet ordre précis et est sauvegardée
dans `/home/z/my-project/download/` :

### Ordre de sortie invariant

```
1. METADATA (bloc YAML)
2. TABLE DES MATIÈRES
3. CONTENU HIÉRARCHISÉ (Markdown)
4. JSON STRUCTURÉ (RAG-ready)
```

### Fichier 1 : `<nom>_extrait.md` (produit par le LLM)

```markdown
---
metadata:
  title: "titre du document"
  authors: ["auteur 1"]
  dates: { created: "YYYY-MM-DD", modified: "YYYY-MM-DD" }
  version: "x.y"
  page_count: 42
  language: "fr"
  source_type: "pdf"
  ocr: false
  ocr_quality: "NON APPLICABLE"
---

## Table des matières

1. Titre niveau 1 .......................................... page X
   1.1 Titre niveau 2 .................................... page Y

---

# 1. Titre de niveau 1

Contenu fidèle du document...

## 1.1 Titre de niveau 2

| Colonne A | Colonne B |
|-----------|-----------|
| Valeur 1  | Valeur 2  |

![description de l'image](page_X)
```

### Fichier 2 : `<nom>_rag.json` (produit par le LLM)

Le schéma JSON complet est détaillé dans `references/json-schema.md`.
Ce fichier est **directement indexable** par un moteur vectoriel.

**Règles de structure du JSON** :
- `title` est au niveau racine UNIQUEMENT (pas dupliqué dans metadata)
- `extraction_method`, `extraction_notes`, `normalization_applied` sont
  au niveau racine UNIQUEMENT (mode pipeline)
- Chaque section doit avoir un `page_end` cohérent avec ses tableaux/images
  (le page_end doit être >= page la plus élevée de tout contenu inclus)

### Fichier 3 (optionnel) : `<nom>_brut.txt` (produit par le LLM)

Texte brut nettoyé, segmenté par sections. C'est une sortie LLM, pas
le `document_raw.txt` du script (qui est un dump intermédiaire brut).

---

## RÈGLES STRICTES (TOUS MODES — INVARIABLES)

Ces règles sont **non négociables**, quel que soit le mode :

### R1 — Zéro hallucination
Ne jamais générer de contenu absent du document source.
Si une information manque : `"NON PRÉSENT DANS LE DOCUMENT"`.

### R2 — Zéro interprétation
Ne jamais déduire, inférer, extrapoler. Reproduire le texte tel qu'il
apparaît, y compris les erreurs du document original.

### R3 — Zéro reformulation
Ne jamais paraphraser, simplifier ou "améliorer" le texte.
Fidélité mot pour mot.

### R4 — Gestion OCR
- Caractère douteux → `[[? mot]]` (géré par le LLM, pas le script)
- Zone illisible → `"OCR INCERTAIN"`
- Toujours indiquer le score de qualité OCR dans les métadonnées
- Le script détecte uniquement si un OCR est probable (heuristique)
- L'OCR réel et les marqueurs sont gérés par le LLM en mode pipeline

### R5 — Gestion des absences
Un champ vide sans explication est une erreur.
Toujours utiliser `"NON PRÉSENT DANS LE DOCUMENT"` pour les valeurs manquantes.
Si une section est présente dans le document mais vide de contenu →
`"SECTION PRÉSENTE MAIS VIDE"`.

### R6 — Tableaux
Reproduire en Markdown dans le contenu ET structurer dans `sections[].tables`
du JSON (avec `headers` et `rows`). Fusionner les tableaux sur plusieurs
pages en un seul, indiquer les pages sources.

### R7 — Images
Pour chaque image : description courte + texte OCR + page + bbox.
Extraire les légendes associées quand elles existent.
Le script extrait les métadonnées ; utiliser `--extract-images` pour
les fichiers image sur disque.

### R8 — Langue
Reproduire dans la langue du document source. Ne jamais traduire sans
instruction explicite de l'utilisateur. Pour les documents multilingues,
taguer chaque section avec `[LANG: xx]`.
Si la langue n'est pas dans les métadonnées PDF, le LLM peut la détecter
mais doit le signaler : `"language_source": "inferred"` ou conserver
`"NON PRÉSENT DANS LE DOCUMENT"` strictement.

### R9 — Intégrité des sections
Ne jamais fusionner des sections non liées entre elles.
Chaque section du document doit correspondre à une et une seule entrée
dans le JSON. Ne pas regrouper des contenus distincts sous un même
heading, même s'ils sont visuellement adjacents.

---

## RÉSOLUTION DE PROBLÈMES

| Situation | Action |
|-----------|--------|
| PDF verrouillé / protégé | Signaler `"DOCUMENT PROTÉGÉ — extraction impossible"` et demander un PDF non protégé |
| PDF corrompu | Signaler `"DOCUMENT CORROMPU"` et lister les pages récupérables |
| PDF vide | Signaler `"DOCUMENT VIDE — 0 page"` |
| Document multilingue | Reproduire chaque section dans sa langue d'origine, taguer `[LANG: xx]` |
| Tableaux sur plusieurs pages | Fusionner en un seul tableau Markdown, indiquer les pages sources |
| En-têtes/pieds de page répétés | Mode pipeline : les supprimer. Autres modes : les inclure dans `sections[].headers_footers` du JSON |
| Formules mathématiques | Reproduire en LaTeX si possible, sinon en texte brut entre `$...$` |
| Annotations / commentaires | Inclure dans une section `annotations` dédiée du JSON |
| Liens hypertexte | Conserver les URLs dans le Markdown `[texte](url)` et dans le JSON `sections[].links` |
| Signets PDF | Utiliser pour reconstruire la table des matières quand elle existe |
| Pages sans texte (images pures) | Marquer `"PAGE IMAGE — contenu non textuel"`, extraire les images avec OCR |

---

## SCRIPTS DISPONIBLES

| Script | Fonction | Usage |
|--------|----------|-------|
| `scripts/extract_pdf.py` | Extraction PDF brute via PyMuPDF (mode-agnostic) | `python extract_pdf.py --input file.pdf --output dir/ --full` |

### Options du script

| Option | Description | Activé par défaut |
|--------|-------------|-------------------|
| `--full` | Active toutes les capacités d'extraction | Non |
| `--links` | Extraction des liens hypertexte | Avec `--full` |
| `--bookmarks` | Extraction des signets PDF | Avec `--full` |
| `--fonts` | Analyse des polices/tailles/couleurs | Avec `--full` |
| `--rag-cleanup` | Détection en-têtes/pieds pour nettoyage RAG | Avec `--full` |
| `--extract-images` | Extraire les images sur disque | Non |

Pour le chemin du skill, résoudre une seule fois en début de session :
```bash
PDF_LLM_DIR="/home/z/my-project/skills/pdf-llm"
```

---

## FICHIERS DE RÉFÉRENCE

Charger le fichier correspondant au mode choisi :

| Fichier | Contenu |
|---------|---------|
| `references/json-schema.md` | Schéma JSON complet avec tous les champs (universel) |
| `references/mode-qwen.md` | Règles spécifiques mode qwen (extraction stricte) |
| `references/mode-glm.md` | Règles spécifiques mode glm (RAG-friendly) |
| `references/mode-multi.md` | Règles spécifiques mode multi (universel) |
| `references/mode-pipeline.md` | Règles spécifiques mode pipeline (normalisation) |
