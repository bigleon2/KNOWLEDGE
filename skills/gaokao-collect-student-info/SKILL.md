---
name: gaokao-collect-student-info
description: >-
  Collecte d'informations pour la saisie des vœux du gaokao : les formulations natifs du candidat font foi ;
  on recueille province, note, matières choisies et autres champs requis par l'API, ainsi que les informations
  complémentaires (centres d'intérêt, famille, orientation professionnelle), sans réécrire ni sur-synthétiser,
  pour produire un student.json structuré.
  Conçu pour l'ouverture d'une consultation gaokao, l'enregistrement du dossier candidat, la collecte d'informations avant la saisie des vœux.
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Collecte des informations du candidat au gaokao

Ce skill est la **première étape** du pipeline de recommandation de vœux : il se limite au dialogue avec l'utilisateur et à la production de `student.json` — aucun appel d'API, aucune recommandation.

## Principe fondamental : restituer l'expression native

**Seulement collecter, jamais transformer.** Les recommandations de spécialités et d'établissements en aval dépendent de **ce que le candidat dit lui-même** ; toute réécriture excessive crée des écarts d'information.

| Pratique | Description |
|------|------|
| ✅ Conserver les propos originaux | pour les champs textuels `interests`, `family_situation`, `career_direction`, `notes`, **utiliser autant que possible les phrases du candidat ou une formulation complète proche de son intention**, sans fioritures, sans élévation, sans résumer à sa place |
| ✅ Enregistrer tel quel | le langage parlé, les répétitions et les formulations vagues peuvent être conservés ; ses propos peuvent être repris dans `notes` plutôt que réécrits en « réponse standard » |
| ✅ Structurer seulement le nécessaire | `province`, `score`, `classify`, `subjects` et autres champs requis par l'API : uniquement une normalisation de format (note en entier, matières séparées par virgules) |
| ✅ Ne verser que l'explicite | `preferred_*` n'enregistre que les établissements, villes, niveaux et catégories de spécialités **explicitement énoncés** par le candidat ; rien d'inventé s'il n'en a pas parlé |
| ❌ Interdiction de sur-interpréter | ne pas réécrire « je veux faire du code » en « orientation informatique » ; ne pas compléter son plan de carrière à sa place ; à cette étape, aucune recommandation de spécialité/établissement ni inférence de tendance |

Lors de la relecture de confirmation, **citer ses propres mots** plutôt que de substituer une version réécrite.

## Amont et aval

- **Amont** : aucun
- **Aval** : [gaokao-fetch-volunteers](../gaokao-fetch-volunteers/SKILL.md) lit la sortie de ce skill et mappe les préférences vers les paramètres optionnels de l'API

## Liste de collecte

### Champs requis par l'API (niveau supérieur de `student.json`)

| Champ | Description | Exemple |
|------|------|------|
| `province` | province du gaokao | Shandong (山东) |
| `classify` | 文科/理科/物理/历史/综合 | 综合 |
| `score` | note du gaokao (entier) | 650 |
| `batch` | batch de saisie | 本科批 |
| `subjects` | 3+1+2 : **les trois matières complètes** (principale + deux options) ; 3+3 : les trois matières ; ancien gaokao `null` | `物理,化学,生物` |
| `gradeType` | uniquement Pékin/Shanghai/Tianjin : 本科/专科 | 本科 |
| `rank` | classement, `null` si absent | 5000 |

### Portrait complémentaire (propos originaux d'abord, pour l'analyse en aval)

| Champ | Description | Exigence de saisie |
|------|------|----------|
| `interests` | centres d'intérêt | **propos du candidat**, virgules ou phrase naturelle acceptées, ne pas résumer |
| `family_situation` | situation familiale | **propos du candidat**, conserver ses expressions sur la situation économique, la région, l'attente vis-à-vis des études |
| `career_direction` | orientation professionnelle future | **propos du candidat**, enregistrer même flou, sans conclure |
| `subject_scores` | notes par matière | champ numérique, selon la saisie du candidat |
| `preferred_cities` | villes souhaitées | ne lister que les villes **explicitement mentionnées** |
| `preferred_provinces` | provinces souhaitées | saisir si explicitement mentionnées ; sinon laisser vide, l'aval déduira depuis les villes |
| `preferred_universities` | établissements visés | utiliser le **nom complet ou l'appellation du candidat**, sans substituer d'abréviation de sa propre initiative |
| `preferred_tags` | niveau d'établissement visé | ne saisir que ce que le candidat **a dit lui-même** (ex. « je veux du 985 »), sans inférence |
| `preferred_major_classes` | catégories de spécialités visées | ne saisir que les spécialités/orientations **explicitement mentionnées**, sans inférer depuis les intérêts |
| `notes` | autres compléments | **propos originaux**, interdits, demandes particulières ne rentrant dans aucun champ |

Le mapping des champs de préférence vers l'API est traité en aval par [gaokao-fetch-volunteers](../gaokao-fetch-volunteers/SKILL.md) ; à cette étape, **inutile** de réécrire ou compléter les `preferred_*` pour coller aux paramètres d'API.

## Workflow

1. Demander point par point en langage naturel, interroger ce qui manque ; les questions peuvent être groupées.
2. **Déterminer le mode de matières selon la province et remplir correctement les champs API** (voir la table et [reference.md](reference.md)).
3. Enregistrer les réponses du candidat **selon leur sens d'origine** dans les champs correspondants ; normaliser uniquement les champs requis par l'API.
4. Une fois les informations complètes, sauvegarder `output/student.json`, **relire les éléments clés avec les mots du candidat** et lui faire confirmer.

### Remplir classify / subjects / gradeType selon la province (SOP)

| Mode | Provinces | classify | subjects | gradeType |
|------|------|----------|----------|-----------|
| Ancien gaokao | Xinjiang (新疆) | 文科 **ou** 理科 | `null` (ne pas transmettre les matières) | `null` |
| 3+1+2 | 23 provinces (粤苏冀鄂湘闽辽渝甘黑吉皖赣贵桂云蒙川宁晋豫陕青) | 物理 **ou** 历史 | **les trois matières complètes** : `物理,化学,生物` (doit inclure la matière principale, pas seulement les deux options) | `null` |
| 3+3 | 沪京津鲁浙琼 (Shanghai, Pékin, Tianjin, Shandong, Zhejiang, Hainan) | **综合** (jamais 物理/历史) | trois matières ; le Zhejiang admet `技术` | uniquement Pékin/Shanghai/Tianjin : `本科`/`专科` |

**Points clés de la collecte** :

- Demander clairement si le candidat est en **littéraire ou scientifique** (Xinjiang), en **physique ou histoire** (3+1+2), ou noter directement les matières choisies (3+3, remplir `classify=综合`).
- **En 3+1+2, `subjects` doit contenir les trois matières complètes** (ex. physique-chimie-biologie), y compris la matière principale cohérente avec `classify`, pas seulement chimie et biologie.
- Pour Pékin/Shanghai/Tianjin, confirmer **licence ou professionnel** (le professionnel ne compte que chinois-maths-langues sur 450).
- Le Xinjiang exige obligatoirement le recueil du **score** ; le classement seul ne suffit pas.
- **Tibet (西藏)** : l'environnement de test ne supporte pas l'interface des vœux — en informer l'utilisateur pendant la collecte.
- `batch` peut recevoir le « 本科批 » tel que dit par le candidat ; l'aval le résoudra automatiquement via batch/list.

## Format de sortie

Voir [examples/student_template.json](examples/student_template.json), [examples/student_shandong.json](examples/student_shandong.json).

```json
{
  "province": "山东",
  "classify": "综合",
  "subjects": "物理,化学,生物",
  "score": 650,
  "batch": "本科批",
  "rank": null,
  "gradeType": null,
  "interests": "propos du candidat, ne pas réécrire",
  "career_direction": "propos du candidat, ne pas réécrire",
  "family_situation": "propos du candidat, ne pas réécrire",
  "preferred_cities": ["北京", "上海", "深圳"],
  "preferred_provinces": ["北京", "上海", "广东"],
  "preferred_universities": ["北京航空航天大学"],
  "preferred_tags": ["985", "211"],
  "preferred_major_classes": ["计算机类", "电子信息类"],
  "notes": "pas de régions reculées"
}
```

## Points d'attention

- `batch` sera résolu automatiquement en aval via batch/list ; ici, on peut saisir le « 本科批 » tel que dit par l'utilisateur.
- **classify doit être cohérent avec le mode de la province** (erreur la plus fréquente : 物理 saisi pour le Shandong). Le recueil complet des pièges est dans [gaokao-fetch-volunteers/reference.md](../gaokao-fetch-volunteers/reference.md).
- Les préférences d'exclusion (ex. pas de régions reculées) vont dans `notes` avec les mots du candidat, **jamais** dans `preferred_provinces`, et sans réécriture en style soutenu.
- La relecture de confirmation montre **la formulation du candidat lui-même**, pas une version lustrée par l'agent.
- Livrer le chemin de sortie en chemin absolu à l'utilisateur.

## Ressources complémentaires

- [reference.md](reference.md) — modes de matières par province et correspondance des batches
- [preference_mapping.md](../gaokao-fetch-volunteers/preference_mapping.md) — correspondance préférences → paramètres API
