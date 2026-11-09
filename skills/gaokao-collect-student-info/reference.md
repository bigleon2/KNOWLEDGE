# Fiche de référence de l'API de recommandation de volontés intelligentes

## Interface

| Élément | Valeur |
|----|-----|
| Chemin | `POST /zp/volunteer/intelligenceVolunteer` |
| Content-Type | `application/json` |
| Authentification | Aucune (interface skill-test publique) |
| BASE_URL par défaut | `https://publicapi.chatglm.cn/chatglm_public/skill-test` |
| Adresse complète | `{BASE_URL}/zp/volunteer/intelligenceVolunteer` |

## Champs du corps de la requête

| Champ | Type | Obligatoire | Description |
|------|------|------|------|
| province | string | ✓ | Province du gaokao (examen d'entrée à l'université en Chine) |
| classify | string | ✓ | Lettres/sciences/Physique/Histoire/Combiné |
| score | integer | ✓ | Score du gaokao |
| batch | string | ✓ | Lot de soumission |
| subjects | string \| null | Dépendant du mode | Matières sélectionnées séparées par des virgules |
| gradeType | string \| null | Pékin/Tianjin/Shanghai | Licence/Professionnel |
| rank | integer \| null | | Rang |
| universitys | string \| null | | Universités préférées, séparées par `,` |
| provinces | string \| null | | Provinces préférées |
| tags | string \| null | | Préférences d'attribut d'établissement |
| majorClass | string \| null | | Préférences de classe de filière |
| universityNum | integer | | Nombre d'universités recommandées, par défaut 30 |
| majorNum | integer | | Nombre de filières par groupe, par défaut 6 |
| isAdjust | boolean | | Ajustement activé |
| volunteerType | string | | ACADEMY_GROUP / ACADEMY_MAJOR / MAJOR_GROUP |
| returnUniversityNum | integer | | Nombre de volontés déjà remplies |
| intentionNum | integer | | Nombre d'intentions déjà remplies |

## Provinces et modes de sélection de matières

Voir [gaokao-fetch-volunteers/reference.md](../gaokao-fetch-volunteers/reference.md) pour les règles observées. Lors de la collecte de `student.json`, assurez-vous de remplir correctement `classify` / `subjects` / `gradeType` par province :

| Mode | Province | classify | subjects | gradeType |
|------|------|----------|----------|-----------|
| Ancien gaokao | Xinjiang | Lettres/sciences | Non transmis | Non transmis |
| 3+1+2 | 23 provinces | Physique/Histoire | **Trois matières complètes** (y compris la première choix, comme `Physique,Chimie,Biologie`) | Non transmis |
| 3+3 | Shanghai/Tianjin/Pékin/Shandong/Zhejiang/Hainan | Combiné | Trois matières (Zhejiang peut inclure Technologie) | Seulement Pékin/Tianjin/Shanghai : Licence/Professionnel |

**Tibet** : L'environnement de test ne prend pas en charge. **Xinjiang** : score doit être transmis, ne transmettez pas seulement rank.

**Lot batch (solution de secours statique, privilégier l'API batch/list)** :

| Province | batch |
|------|-------|
| Tianjin | Lot de licence A |
| Zhejiang | Segment 1 de la catégorie générale |
| Shandong | Segment 1 de la catégorie générale |
| Sichuan/Yunnan | Lot de licence B |
| Gansu | Lot de licence |
| Ningxia | Lot de licence B |
| Xinjiang | Premier lot de licence |
| Tibet | Non pris en charge temporairement dans l'environnement de test (2222010 erreur de province gaokao) |

## Structure de réponse

L'interface skill-test publique renvoie `{ status, message, result }` (`status=0` pour succès), le script convertit automatiquement au format unifié.

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

`type` énumération : `CHONG` Risqué, `WEN` Stable, `BAO` Sécurisé, `NAN` Difficile, `YI` Facile.

`score` / `parityScore` sont souvent des chaînes JSON, comme `[{"2025":"660,2153,60"}]` (score, rang, nombre de places).
