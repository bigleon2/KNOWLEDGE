# Schéma JSON RAG-Ready — Référence complète

Ce fichier définit le schéma JSON universel utilisé par tous les modes du
skill pdf-llm. Il est conçu pour être directement indexable par un moteur
vectoriel (ChromaDB, FAISS, Pinecone, etc.).

---

## Structure racine

```json
{
  "title": "string — titre du document",
  "metadata": { /* objet Metadata (voir ci-dessous) */ },
  "toc": [ /* array de ToCEntry */ ],
  "extraction_method": "string — mode qwen | glm | multi | pipeline",
  "extraction_notes": "string — notes sur problèmes rencontrés (pipeline uniquement)",
  "normalization_applied": ["string — liste des normalisations (pipeline uniquement)"],
  "sections": [ /* array de Section */ ]
}
```

---

## Metadata

```json
{
  "authors": ["string"],
  "dates": {
    "created": "YYYY-MM-DD | NON PRÉSENT DANS LE DOCUMENT",
    "modified": "YYYY-MM-DD | NON PRÉSENT DANS LE DOCUMENT"
  },
  "version": "string | NON PRÉSENT DANS LE DOCUMENT",
  "page_count": 0,
  "language": "code ISO 639-1 | NON PRÉSENT DANS LE DOCUMENT",
  "source_type": "pdf | image | texte | mixed",
  "ocr": true | false,
  "ocr_quality": "excellente | bonne | moyenne | mauvaise | NON APPLICABLE",
  "ocr_notes": "string | NON APPLICABLE"
}
```

**Note importante** : `title` est au niveau **racine uniquement**, pas dans metadata.
Les champs `extraction_method`, `extraction_notes`, `normalization_applied`
sont au niveau **racine uniquement** (mode pipeline), pas dans metadata.

### Champs additionnels du script (non normalisés)

Le script `extract_pdf.py` peut ajouter ces champs supplémentaires dans
`document_metadata.json` (pour référence, mais ils ne font pas partie du
schéma JSON RAG final) :

| Champ | Type | Description |
|-------|------|-------------|
| `producer` | string | Outil de création du PDF |
| `creator` | string | Application de création |
| `encryption` | boolean | PDF chiffré |

Ces champs sont ignorés dans le JSON RAG final produit par le LLM.

### Champs conditionnels par mode

Ces champs s'ajoutent à l'objet racine ou metadata selon le mode :

| Champ | Type | Mode | Description |
|-------|------|------|-------------|
| `extraction_method` | string | pipeline | "pymupdf" \| "pdfplumber" \| "ocr" — origine de l'extraction |
| `extraction_notes` | string | pipeline | Notes sur les problèmes rencontrés lors de l'extraction |
| `normalization_applied` | string[] | pipeline | Liste des normalisations effectuées (ex: "pagination_artifacts_removed", "hyphenation_fixed") |
| `chunk_count` | int | glm | Nombre total de chunks générés |
| `avg_chunk_length` | int | glm | Longueur moyenne des chunks en mots |
| `type_hint` | string | glm | Annotation sémantique par section : "definition" \| "procedure" \| "example" \| "summary" \| "data" \| "background" |

---

## ToCEntry (entrée de table des matières)

```json
{
  "heading": "string — titre de la section",
  "level": 1 | 2 | 3 | 4,
  "page": 0
}
```

---

## Section (bloc de contenu)

```json
{
  "id": "sec-N — identifiant unique (sec-1, sec-2, sec-1-1, etc.)",
  "heading": "string — titre de la section",
  "level": 1 | 2 | 3 | 4,
  "page_start": 0,
  "page_end": 0,
  "content": "string — texte intégral de la section",
  "type_hint": "string — annotation sémantique (glm uniquement)",
  "tables": [ /* array de Table */ ],
  "images": [ /* array de ImageEntry */ ],
  "links": [ /* array de LinkEntry */ ],
  "children": [ /* array de Section (imbriqué, glm et pipeline) */ ]
}
```

---

## Table

```json
{
  "caption": "string — légende du tableau",
  "headers": ["Colonne A", "Colonne B", "Colonne C"],
  "rows": [
    ["Valeur A1", "Valeur B1", "Valeur C1"],
    ["Valeur A2", "Valeur B2", "Valeur C2"]
  ],
  "page": 0,
  "pages_source": [3, 4]  // si tableau fusionné sur plusieurs pages
}
```

---

## ImageEntry

```json
{
  "description": "string — description courte de l'image",
  "page": 0,
  "bbox": null | [x0, y0, x1, y1],
  "ocr_text": "string — texte extrait de l'image par OCR",
  "caption": "string — légende associée (si présente)"
}
```

---

## LinkEntry (nouveau — extraction fine)

```json
{
  "text": "string — texte d'ancre du lien",
  "url": "string — URL cible",
  "page": 0
}
```

---

## Différences par mode

| Champ | qwen | glm | multi | pipeline |
|-------|------|-----|-------|----------|
| `toc` | inclus | inclus | inclus | inclus |
| `sections[].tables` | inclus | inclus | inclus | inclus (enrichi) |
| `sections[].images` | inclus | inclus | inclus | inclus (enrichi) |
| `sections[].links` | inclus | inclus | inclus | inclus |
| `sections[].children` | omit | inclus (sous-chunks) | omit | inclus (hiérarchie) |
| `sections[].content` | texte brut | texte brut | texte brut | texte normalisé |
| `sections[].type_hint` | omit | inclus | omit | omit |
| `extraction_method` | omit | omit | omit | inclus |
| `normalization_applied` | omit | omit | omit | inclus |
| `chunk_count` | omit | inclus | omit | omit |
| `avg_chunk_length` | omit | inclus | omit | omit |

En mode **glm**, les `children` servent au sous-chunking des longues sections.
En mode **pipeline**, les `children` reflètent la hiérarchie complète du document.

---

## Bonnes pratiques pour l'indexation

1. Chaque `sections[].content` constitue un **chunk** naturel pour le RAG
2. Le champ `id` sert de clé de référence unique
3. Les `page_start` et `page_end` permettent le traçage source
4. Les tableaux sont structurés pour permettre des requêtes ciblées
5. Les images avec `ocr_text` sont traitées comme du contenu textuel
6. Les liens permettent le traçage des références externes
7. En mode glm, les `type_hint` améliorent la pertinence du retrieval sémantique
8. En mode pipeline, `normalization_applied` permet l'audit du traitement
