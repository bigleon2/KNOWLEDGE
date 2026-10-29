# Aide-mémoire de l'API du tableau de vœux à recommandation intelligente

## Flux d'appel en deux étapes

`fetch_volunteers.py` appelle d'abord l'interface des batches, puis celle de recommandation de vœux :

1. **Liste des batches** `GET /zp/volunteer/batch/list?province=山东&classify=综合&score=651`
2. **Recommandation de vœux** `POST /zp/volunteer/intelligenceVolunteer` (les champs `batch` et `volunteerType` du corps de requête proviennent de l'option choisie à l'étape 1)

Valeurs de `classify` : `文科` (littéraire), `理科` (scientifique), `物理` (physique), `历史` (histoire), `综合` (général), à renseigner selon la province et le mode de spécialités (voir ci-dessous).

Règle de sélection du batch : nom de batch exact → filtrage par `gradeType` / batch licence · batch professionnel → parmi les batches accessibles au score, prendre celui au seuil le plus élevé.

Le résultat analysé `parsed.json` contient un champ `batch_resolution` qui consigne l'origine du batch et les options possibles.

## Interface liste des batches

| Élément | Valeur |
|----|-----|
| Chemin | `GET /zp/volunteer/batch/list` |
| Paramètres | `province`, `classify`, `score` ; `gradeType` en plus pour Pékin/Shanghai/Tianjin |
| Réponse | `{ status, message, result: [{ batch, score, gradeType, type, ... }] }` |

`result[].type` correspond au `volunteerType` de l'interface des vœux (ex. `MAJOR_GROUP`). `gradeType` ne sert qu'au filtrage des batches ; il n'entre dans le corps de la requête de vœux **que pour Pékin/Shanghai/Tianjin**.

## Interface de recommandation de vœux

| Élément | Valeur |
|----|-----|
| Chemin | `POST /zp/volunteer/intelligenceVolunteer` |
| Content-Type | `application/json` |
| Authentification | aucune (interface skill-test publique) |
| BASE_URL par défaut | `https://publicapi.chatglm.cn/chatglm_public/skill-test` |
| Adresse complète | `{BASE_URL}/zp/volunteer/intelligenceVolunteer` |

## Champs du corps de requête

| Champ | Type | Requis | Description |
|------|------|------|------|
| province | string | ✓ | province du gaokao |
| classify | string | ✓ | 文科/理科/物理/历史/综合 |
| score | integer | ✓ | note du gaokao |
| batch | string | ✓ | batch de saisie (résolu automatiquement par batch/list) |
| subjects | string \| null | selon le mode | spécialités choisies, séparées par virgules |
| gradeType | string \| null | Pékin/Shanghai/Tianjin | 本科 (licence) / 专科 (professionnel) |
| rank | integer \| null | | classement |
| universitys | string \| null | | universités visées, séparées par `,` ; issu de `student.preferred_universities` |
| provinces | string \| null | | provinces souhaitées ; issu de `preferred_provinces` ou déduit de `preferred_cities` |
| tags | string \| null | | attributs d'établissements souhaités ; issu de `preferred_tags` (ex. 985,211) |
| majorClass | string \| null | | catégories de spécialités souhaitées ; issu de `preferred_major_classes` |
| universityNum | integer | | nombre d'établissements recommandés, défaut 30 |
| majorNum | integer | | nombre de spécialités par groupe, défaut 6 |
| isAdjust | boolean | | accepter la réaffectation |
| volunteerType | string | | ACADEMY_GROUP / ACADEMY_MAJOR / MAJOR_GROUP |
| returnUniversityNum | integer | | nombre de vœux déjà saisis |
| intentionNum | integer | | nombre d'intentions déjà saisies |

## Modes province/spécialités (règles constatées)

### Ancien gaokao (Xinjiang seul)

| Champ | Valeur |
|------|-----|
| classify | `文科` ou `理科` (l'un des deux, jamais 物理/历史/综合) |
| subjects | ne pas transmettre ou `null` (**ne pas** transmettre la chaîne `"null"`) |
| gradeType | ne pas transmettre |
| score | **obligatoire** (le Xinjiang n'a pas de table score/rang, le rang seul ne permet pas de retrouver la note) |

### Mode 3+1+2 (23 provinces)

Guangdong, Jiangsu, Hebei, Hubei, Hunan, Fujian, Liaoning, Chongqing, Gansu, Heilongjiang, Jilin, Anhui, Jiangxi, Guizhou, Guangxi, Yunnan, Mongolie-Intérieure, Sichuan, Ningxia, Shanxi, Henan, Shaanxi, Qinghai

| Champ | Valeur |
|------|-----|
| classify | `物理` ou `历史` (matière principale du 3+1+2) |
| subjects | **les trois matières complètes**, séparées par virgules : `matière principale,option 1,option 2`. Doit inclure la matière principale cohérente avec `classify`, **ne pas transmettre seulement les deux options** |

Exemple : `classify=物理`, `subjects=物理,化学,生物` (✓) ; `subjects= 化学,生物` (✗ il manque 物理)

Les matières optionnelles ne peuvent être que : 化学 (chimie), 生物 (biologie), 政治 (politique), 地理 (géographie).
| gradeType | ne pas transmettre |

### Mode 3+3 (6 provinces)

Shanghai, Pékin, Tianjin, Shandong, Zhejiang, Hainan

| Champ | Valeur |
|------|-----|
| classify | fixé à `综合` |
| subjects | trois matières séparées par virgules ; le Zhejiang admet `技术` (technologie) |
| gradeType | **uniquement pour Pékin/Shanghai/Tianjin** : `本科` (licence) / `专科` (professionnel) |

**Écarts de barème** : Shandong/Zhejiang 750 ; Hainan 900 ; licence Shanghai 660 ; licence Pékin/Tianjin 750 ; professionnel Pékin/Shanghai/Tianjin 450 (chinois, math, langues).

### Règle gradeType pour Pékin/Shanghai/Tianjin

L'interface des batches `batch/list` **et** celle des vœux exigent toutes deux `gradeType` :

```
GET .../batch/list?province=北京&classify=综合&score=650&gradeType=本科
```

Si absent, le script infère ainsi : `batch=专科批` → professionnel ; `score≤450` → professionnel ; sinon → licence.

| Scénario | subjects | gradeType |
|------|----------|-----------|
| Licence Pékin | `物理,化学,生物` | `本科` |
| Professionnel Pékin | chaîne `"null"` (exigé par l'API, pas un null JSON) | `专科` |
| Zhejiang/Shandong/Hainan | combinaison de trois matières | ne pas transmettre |

### Tibet

**Non intégré** dans l'environnement de test : tout classify renvoie `status=500`, ce n'est pas une erreur de paramètres. Le script le signale comme non supporté dès la phase de validation.

### Pièges courants (interface des batches)

| Symptôme | Cause | Traitement |
|------|------|------|
| `status=0` mais `result=[]` | classify incohérent avec le mode de la province (ex. `物理` pour le Shandong) | corriger classify selon les tables ci-dessus |
| Vœux 500 (Shandong etc.) | `gradeType` transmis par erreur | ne le transmettre que pour Pékin/Shanghai/Tianjin, le retirer ailleurs |
| Vœux 500 (Shandong etc.) | `subjects` absent ou limité à deux matières | en 3+1+2, transmettre les **trois matières complètes** (avec 物理/历史) |
| Vœux 500 (Xinjiang) | `subjects` est la chaîne `"null"` | ne pas transmettre le champ subjects |
| Professionnel Pékin 500 | subjects est un null JSON ou omis | utiliser la chaîne `"null"` |

`scripts/province_config.py` encapsule ces validations et la normalisation des paramètres ; `scripts/test_batch_api.py` permet une régression en lot sur les 31 provinces.

### Repli statique sur les batches (si batch/list échoue)

| Province | batch |
|------|-------|
| Tianjin | 本科批A段 |
| Zhejiang | 普通类一段 |
| Shandong | 普通类一段 |
| Sichuan, Yunnan | 本科批B段 |
| Gansu | 本科批 |
| Ningxia | 本科批B段 |
| Xinjiang | 本科一批 |
| Tibet | non supporté en environnement de test (erreur 2222010 province gaokao) |

## Structure de réponse

L'interface publique skill-test renvoie `{ status, message, result }` (`status=0` = succès) ; le script convertit automatiquement au format unifié.

```json
{
  "status": 0,
  "message": "success",
  "result": {
    "province": "...",
    "schoolList": [
      {
        "universityName": "",
        "universityCode": "",
        "universityMajorGroup": "",
        "enrollProbability": 20,
        "type": "CHONG",
        "majorList": [ { "majorName": "", "claim": "", "type": "CHONG" } ]
      }
    ]
  }
}
```

L'ancien format d'interface `{ code, msg, body }` (`code=200`) est également compatible.

Énumération de `type` : `CHONG` ambitieux, `WEN` stable, `BAO` garanti, `NAN` difficile, `YI` facile.

`score` / `parityScore` sont souvent des chaînes JSON, ex. `[{"2025":"660,2153,60"}]` (note, rang, nombre de places).
