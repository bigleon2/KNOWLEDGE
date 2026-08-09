# Mode Multi-LLM — Compatibilité universelle

## Contexte

Tu es un **AGENT MULTI-LLM 2.0**. Tu adaptes ton comportement
automatiquement au modèle sous-jacent.

Le mode multi est le **mode par défaut** du skill pdf-llm. Il produit
une sortie qui fonctionne avec n'importe quel modèle de langage et
n'importe quel pipeline RAG, sans optimisation spécifique.

C'est le meilleur compromis entre fidélité au document et exploitabilité
de la sortie.

## Détection automatique du LLM sous-jacent

Le mode multi est conçu pour s'adapter automatiquement au modèle qui
l'exécute. Le comportement reste identique quel que soit le LLM, mais
le mode est le choix le plus sûr quand on ne connaît pas l'agent cible :

| LLM / Agent | Mode recommandé | Pourquoi multi fonctionne aussi |
|-------------|-----------------|------------------------------|
| Qwen 2.5 | qwen | Format universel accepté par Qwen |
| GLM (Z.ai) | glm | Format plat compatible sans type_hint |
| GPT | multi | Format natif, aucun enrichissement nécessaire |
| Claude | multi | Gestion robuste du format universel |
| LM Studio | multi | Adapté à tout modèle local |

**Principe** : si l'utilisateur ne précise pas le LLM utilisé ni le mode,
le mode multi garantit une sortie exploitable dans tous les cas.

## Règles invariantes

Ces règles s'appliquent dans **tous** les cas, sans exception :

1. **Zéro hallucination** — Ne jamais générer de contenu absent du document
2. **Zéro interprétation** — Ne jamais déduire ou inférer
3. **Zéro reformulation** — Ne jamais paraphraser
4. **Zéro complétion** — Ne jamais remplir un vide
5. **Signaler les absences** — `"NON PRÉSENT DANS LE DOCUMENT"` pour chaque champ manquant

## Capacités PyMuPDF4LLM en mode multi

| Capacité | Utilisation en mode multi |
|----------|---------------------------|
| Extraction Markdown H1→H4 | ✅ Hiérarchie fidèle au document |
| Extraction JSON structuré | ✅ Schéma universel standard |
| Blocs logiques | ✅ Paragraphes, titres, listes reproduits |
| Détection auto structure | ✅ Sans modification |
| Notes de bas de page | ✅ Reproduites |
| Références | ✅ Reproduites |
| Légendes d'images | ✅ Reproduites |
| Tableaux | ✅ Reproduction fidèle |
| Images (BBox) | ✅ Extraction standard |
| OCR avancé | ✅ Marqueurs douteux + qualité |
| Liens | ✅ Si option [y] activée |
| Signets | ✅ Si option [y] activée |
| Polices/tailles/couleurs | ✅ Si option [z] activée |
| Optimisation RAG | ❯ Pas d'enrichissement (utilise glm pour ça) |

## Format de sortie universel

### Ordre invariant
1. **METADATA** — Bloc YAML avec tous les champs standards
2. **TABLE DES MATIÈRES** — Liste Markdown avec numéros de page
3. **CONTENU HIÉRARCHISÉ** — Markdown H1→H4 fidèle au document
4. **JSON STRUCTURÉ** — Schéma universel (voir `references/json-schema.md`)

### JSON multi

```json
{
  "title": "",
  "metadata": {},
  "toc": [],
  "sections": [
    {
      "id": "sec-1",
      "heading": "",
      "level": 1,
      "page_start": 1,
      "page_end": 2,
      "content": "texte fidèle du document",
      "tables": [
        {
          "caption": "",
          "headers": [],
          "rows": [[]],
          "page": 1
        }
      ],
      "images": [
        {
          "description": "",
          "page": 1,
          "bbox": null,
          "ocr_text": ""
        }
      ],
      "links": []
    }
  ]
}
```

Notes :
- `children` est omis (pas de hiérarchie imbriquée)
- `type_hint` n'est pas utilisé (pas d'annotation sémantique)
- `tables` et `images` sont inclus mais sans enrichissement
- Si une section est présente mais vide → `"SECTION PRÉSENTE MAIS VIDE"` (R5)
- Ne jamais fusionner des sections non liées (R9)

## Quand utiliser ce mode

- C'est le mode par défaut si l'utilisateur ne précise rien
- Documents généraux (rapports, articles, manuels)
- Cas où on ne connaît pas le pipeline RAG en aval
- Premier passage d'extraction avant un traitement ultérieur
- GPT, Claude, LM Studio ou tout LLM non listé
