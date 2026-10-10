---
name: gaokao-collect-student-info
version: "1.0.0"
category: "Éducation"
tags:
  - gaokao
  - collect
  - student
  - info
description: >-
  Collecte d'informations pour le remplissage des vœux du Gaokao : à partir de l'expression
  native du candidat, recueillir les champs API obligatoires (province, score, matières, etc.)
  ainsi que les informations auxiliaires (centres d'intérêt, situation familiale, orientation
  professionnelle), en évitant au maximum toute reformulation ou sur-généralisation, et produire
  un student.json structuré. Convient pour l'ouverture d'une consultation Gaokao, l'enregistrement
  des informations du candidat et la collecte d'informations avant le remplissage des vœux.
language: fr

read_when:
  - Déclencher quand la demande concerne : >-
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Collecte des informations du candidat au Gaokao

Ce skill est la **première étape** du pipeline de recommandation de vœux : il se contente de dialoguer avec l'utilisateur pour produire `student.json`, sans appel d'API ni recommandation.

## Principe fondamental : restituer la formulation native

**Il ne fait que collecter, il ne transforme pas.** La recommandation de filières et d'établissements en aval dépend de ce que le candidat **dit lui-même** ; une réécriture excessive crée des pertes d'information.

| Pratique | Consigne |
|------|------|
| ✅ Conserver les mots du candidat | Pour les champs textuels `interests`, `family_situation`, `career_direction`, `notes`, etc., **utiliser autant que possible les phrases exactes du candidat ou des formulations complètes fidèles au sens**, sans polissage, sans enjolivement, sans résumer à sa place |
| ✅ Enregistrer fidèlement | Le langage oral, les répétitions et les formulations vagues du candidat peuvent être conservés ; compléter `notes` avec ses mots à lui plutôt que de réécrire une « réponse standard » |
| ✅ Structurer seulement si nécessaire | Pour les champs API obligatoires comme `province`, `score`, `classify`, `subjects`, ne faire qu'une normalisation de format (score en entier, matières séparées par des virgules) |
| ✅ N'enregistrer que l'explicite | `preferred_*` ne consigne que les établissements, villes, niveaux et familles de filières **explicitement mentionnés** par le candidat ; ne rien inventer à défaut |
| ❌ Interdiction de sur-intervenir | Ne pas transformer « je veux faire du code » en « orientation informatique » ; ne pas suppléer un projet professionnel que le candidat n'a pas exprimé ; ne pas faire de recommandation de filières/établissements ni d'inférence d'orientation à ce stade |

Pour reformuler à l'utilisateur afin de confirmer, **citer ses propres mots**, et non une version réécrite par vos soins.

## Amont / aval

- **Amont** : aucun
- **Aval** : [gaokao-fetch-volunteers](../gaokao-fetch-volunteers/SKILL.md) lit la sortie de ce skill et mappe les préférences vers les paramètres API optionnels

## Liste de collecte

### Champs API obligatoires (à écrire à la racine de `student.json`)

| Champ | Description | Exemple |
|------|------|------|
| `province` | Province du Gaokao | Shandong |
| `classify` | `文科` (littéraire) / `理科` (scientifique) / `物理` (physique) / `历史` (histoire) / `综合` (mixte) | `综合` |
| `score` | Score du Gaokao (entier) | 650 |
| `batch` | Lot de candidature | `本科批` |
| `subjects` | 3+1+2 : **les trois matières complètes** (matière principale + deux matières secondaires) ; 3+3 : trois matières complètes ; ancien régime : `null` | `物理,化学,生物` |
| `gradeType` | Uniquement Pékin/Shanghai/Tianjin : `本科` (licence) / `专科` (filière courte) | `本科` |
| `rank` | Classement, sinon `null` | 5000 |

### Profil auxiliaire (mots du candidat en priorité, pour l'analyse en aval)

| Champ | Description | Consignes de remplissage |
|------|------|----------|
| `interests` | Centres d'intérêt | **Mots du candidat**, en virgules ou en phrases naturelles, sans résumer |
| `family_situation` | Situation familiale | **Mots du candidat**, en conservant sa façon d'exprimer le contexte financier, géographique, l'attitude face aux études longues, etc. |
| `career_direction` | Orientation professionnelle/avenir | **Mots du candidat**, même flous, à recopier tels quels, sans conclure |
| `subject_scores` | Notes par matière | Champs numériques, selon ce que déclare le candidat |
| `preferred_cities` | Villes souhaitées | Ne lister que les villes **explicitement mentionnées** par le candidat |
| `preferred_provinces` | Provinces souhaitées | À enregistrer si le candidat les mentionne explicitement ; sinon laisser vide, l'aval les déduira des villes |
| `preferred_universities` | Établissements convoités | Utiliser le **nom complet ou l'appellation d'origine** utilisée par le candidat, sans remplacer par un raccourci |
| `preferred_tags` | Niveau d'établissement souhaité | Ne consigner que ce que le candidat **a dit lui-même** (p. ex. « je veux un 985 »), sans déduire de soi-même |
| `preferred_major_classes` | Familles de filières souhaitées | Ne consigner que les filières/orientations **explicitement mentionnées**, sans déduire ni réécrire à partir des centres d'intérêt |
| `notes` | Autres compléments | **Mots du candidat** ne rentrant pas dans les champs ci-dessus, tabous, demandes particulières |

Le mappage des champs de préférences vers l'API est géré en aval par [gaokao-fetch-volunteers](../gaokao-fetch-volunteers/SKILL.md) ; à ce stade, **inutile** de réécrire ou de compléter `preferred_*` pour satisfaire les paramètres de l'API.

## Flux de travail

1. Interroger l'utilisateur point par point en langage naturel : demander ce qui manque ; poser les questions en plusieurs fois si besoin.
2. **Déterminer le régime de matières selon la province et remplir correctement les champs API** (voir le tableau ci-dessous et [reference.md](reference.md)).
3. Saisir les réponses du candidat **en respectant leur sens d'origine** dans les champs correspondants ; ne normaliser le format que pour les champs API obligatoires.
4. Une fois les informations complètes, enregistrer `output/student.json`, **reformuler avec les mots du candidat** les points clés et lui demander de confirmer.

### Remplir classify / subjects / gradeType selon la province (SOP)

| Régime | Provinces | classify | subjects | gradeType |
|------|------|----------|----------|-----------|
| Ancien régime | Xinjiang | `文科` **ou** `理科` | `null` (ne pas transmettre les matières) | `null` |
| 3+1+2 | Guangdong, Jiangsu, Hebei, Hubei, Hunan, Fujian, Liaoning, Chongqing, Gansu, Heilongjiang, Jilin, Anhui, Jiangxi, Guizhou, Guangxi, Yunnan, Mongolie-Intérieure, Sichuan, Ningxia, Shanxi, Henan, Shaanxi, Qinghai | `物理` **ou** `历史` | **Les trois matières complètes** : `物理,化学,生物` (doivent inclure la matière principale ; ne pas écrire uniquement les deux matières secondaires) | `null` |
| 3+3 | Shanghai, Pékin, Tianjin, Shandong, Zhejiang, Hainan | `综合` (ne pas mettre `物理`/`历史`) | Trois matières ; le Zhejiang peut choisir `技术` | Uniquement Pékin/Shanghai/Tianjin : `本科` / `专科` |

**Points clés de collecte** :

- Demander clairement si le candidat est **littéraire ou scientifique** (Xinjiang), **physique ou histoire** (3+1+2), ou noter directement les matières (3+3 : mettre `classify=综合`).
- **Pour le 3+1+2, `subjects` doit contenir les trois matières complètes** (p. ex. physique-chimie-biologie), y compris la matière principale cohérente avec `classify` ; ne pas se limiter à chimie et biologie.
- Pour Pékin/Shanghai/Tianjin, confirmer s'il s'agit de **`本科` (licence) ou `专科` (filière courte)** (la filière courte n'évalue que chinois, maths et anglais sur 450 points).
- Pour le Xinjiang, la collecte du **score** est obligatoire ; le rang seul ne suffit pas.
- **Tibet** : l'environnement de test ne supporte pas l'API de vœux ; le dire à l'utilisateur lors de la collecte.
- `batch` peut reprendre la mention « 本科批 » telle que dite par l'utilisateur ; l'aval la résoudra automatiquement via batch/list.

## Format de sortie

Se référer à [examples/student_template.json](examples/student_template.json) et [examples/student_shandong.json](examples/student_shandong.json).

```json
{
  "province": "山东",
  "classify": "综合",
  "subjects": "物理,化学,生物",
  "score": 650,
  "batch": "本科批",
  "rank": null,
  "gradeType": null,
  "interests": "考生原话，勿改写",
  "career_direction": "考生原话，勿改写",
  "family_situation": "考生原话，勿改写",
  "preferred_cities": ["北京", "上海", "深圳"],
  "preferred_provinces": ["北京", "上海", "广东"],
  "preferred_universities": ["北京航空航天大学"],
  "preferred_tags": ["985", "211"],
  "preferred_major_classes": ["计算机类", "电子信息类"],
  "notes": "不接受偏远地区"
}
```

## Points d'attention

- `batch` sera résolu automatiquement en aval via batch/list ; ici on peut reprendre la mention « 本科批 » telle que dite par l'utilisateur.
- **`classify` doit être cohérent avec le régime de la province** (erreur la plus fréquente : saisir `物理` pour le Shandong). Voir tous les pièges dans [gaokao-fetch-volunteers/reference.md](../gaokao-fetch-volunteers/reference.md).
- Les préférences d'exclusion (p. ex. « pas de régions reculées ») sont à écrire avec les mots du candidat dans `notes`, **pas** dans `preferred_provinces`, et sans les réécrire en style formel.
- Lors de la reformulation de confirmation, présenter **l'expression du candidat lui-même**, pas une version polie par l'agent.
- Utiliser un chemin absolu pour livrer le fichier de sortie à l'utilisateur.

## Ressources annexes

- [reference.md](reference.md) — régimes de matières par province et correspondance des lots
- [preference_mapping.md](../gaokao-fetch-volunteers/preference_mapping.md) — mappage préférences → paramètres API
