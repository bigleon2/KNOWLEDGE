# Correspondance entre les préférences du candidat et les paramètres optionnels de l'API

Avant **l'étape 2 de récupération des vœux**, l'agent doit extraire les préférences des informations complémentaires de `student.json`, les écrire dans les champs structurés, puis construire la requête API.

## Table de correspondance générale

| Champ student.json | Champ API | Format | Description |
|-------------------|----------|------|------|
| `preferred_universities` | `universitys` | chaîne séparée par virgules | noms complets des universités visées, ex. `北京航空航天大学,华东师范大学` |
| `preferred_provinces` | `provinces` | chaîne séparée par virgules | provinces d'études souhaitées ; si vide, déduit automatiquement de `preferred_cities` |
| `preferred_cities` | `provinces` (déduit) | — | correspondance villes ci-dessous ; traité automatiquement par le script `build_api_request.py` |
| `preferred_tags` | `tags` | chaîne séparée par virgules | attributs des établissements, ex. `985,211,双一流` |
| `preferred_major_classes` | `majorClass` | chaîne séparée par virgules | catégories de spécialités du ministère de l'Éducation, ex. `计算机类,电子信息类` |

## Règles d'extraction par l'agent

Identifier les préférences à partir du langage naturel et **les écrire dans les champs correspondants de student.json** (possible dès la collecte de l'étape 1, ou en complément avant l'appel API de l'étape 2) :

### Préférence d'établissement → `preferred_universities`

Écoles précises mentionnées par l'utilisateur, « viser Tsinghua-Pékinard-Fudan-Jiaotong (清北复交) », « envisager l'Université de défense nationale (国防科大) », etc.

### Préférence de ville → `preferred_cities` + `preferred_provinces`

- Collecter la liste des villes dans `preferred_cities`
- En déduire les provinces et les écrire dans `preferred_provinces` (à fusionner et dédupliquer avec le résultat de la correspondance ville→province)

Correspondances ville→province usuelles : Shenzhen/Guangzhou → Guangdong, Wuhan → Hubei, Hangzhou → Zhejiang, Nanjing/Suzhou → Jiangsu, Chengdu → Sichuan, Xi'an → Shaanxi.

### Préférence de niveau d'établissement → `preferred_tags`

| Formulation utilisateur | Valeur tags |
|----------|---------|
| 985 / haut niveau | `985` |
| 211 | `211` |
| Double première classe (双一流) | `双一流` |
| Accès au master sans examen (保研) | `保研资格` |
| Enseignement (normal) | `师范` |
| Grande école de médecine | à combiner avec l'établissement précis, ou renseigner le tag `医学院` (si l'API le permet) |

### Préférence de spécialité → `preferred_major_classes`

Déduire à partir de `interests`, `career_direction`, `subject_scores` :

| Orientation intérêt/emploi | majorClass suggéré |
|--------------|-----------------|
| Programmation, internet, IA | `计算机类,软件工程,电子信息类` |
| Électronique, puces, télécoms | `电子信息类,微电子科学与工程,集成电路` |
| Médecine, clinique | `临床医学类,口腔医学类,药学类` |
| Mécanique, fabrication, aérospatial | `机械类,航空航天类,自动化类` |
| Économie, finance, gestion | `经济学类,金融学类,工商管理类` |
| Droit | `法学类` |
| Enseignement, éducation | `教育学类,中国语言文学类,数学类` |

> Utiliser les appellations standard des catégories de licence du ministère chinois de l'Éducation ; séparer plusieurs catégories par des virgules (format anglais), sans dépasser 5 entrées de préférence.

### Exclusions et interdits → `notes` + absence de paramètre

Les préférences **d'exclusion** comme « pas de régions reculées » vont dans `notes`, pour le Skill de recommandation en aval ; **ne surtout pas** mettre les provinces rejetées dans `provinces`.

## Workflow

```
student.json (avec champs de préférence)
    → l'agent vérifie/complète les champs preferred_*
    → build_api_request.py
    → api_request.json
    → fetch_volunteers.py
    → parsed.json
```

## Exemple Shandong

Candidat : intéressé par la programmation/l'IA, vise Pékin-Shanghai-Shenzhen, souhaite du 985, orientation informatique.

```json
{
  "preferred_cities": ["北京", "上海", "深圳"],
  "preferred_provinces": ["北京", "上海", "广东"],
  "preferred_universities": ["北京航空航天大学", "华东师范大学"],
  "preferred_tags": ["985", "211"],
  "preferred_major_classes": ["计算机类", "电子信息类", "自动化类"]
}
```

Fragment API généré :

```json
{
  "universitys": "北京航空航天大学,华东师范大学",
  "provinces": "北京,上海,广东",
  "tags": "985,211",
  "majorClass": "计算机类,电子信息类,自动化类"
}
```
