# Référentiel des signaux de parsing des JD (descriptions de poste chinoises)

## Signaux forts (must-have)

Dès que l'une de ces expressions apparaît dans une phrase du JD, la compétence / l'expérience qui suit est très probablement un seuil dur :

- 必须 / 必备 / 要求 / 应当
- 至少 X 年 / X+ years / 不少于
- "需要" / "需具备"
- "必要条件" / "硬性要求"
- 工科背景 / 985 / 211 / 硕士及以上 / 博士

En JD anglais :
- Required / Must have / Mandatory / Essential
- Minimum X years
- Strong proficiency in / Expert in
- Demonstrated experience with

## Signaux faibles (nice-to-have)

- 加分 / 优先 / 优先考虑
- 熟悉 ___ 者优先
- 有 ___ 经验者优先
- "了解 ___ 即可"
- 加分项

En anglais :
- Preferred / Nice to have / Plus / Bonus / Desirable
- Familiar with / Exposure to
- A plus / Would be a plus

## Verbes de responsabilité (à écrire dans les bullets pour faire écho au JD)

Chinois : 负责、主导、推动、设计、搭建、优化、规划、迭代、孵化、复盘、运营、管理、协调、执行
Anglais : Lead / Drive / Build / Design / Architect / Develop / Implement / Optimize / Manage / Coordinate / Execute / Own

## Exigences particulières

- **Diplôme** : 本科 (licence) / 硕士 (master) / 博士 (doctorat) et plus ; palier d'école
- **Années d'expérience** : X-Y ans (donner la fourchette ; ne pas la remplir laisse de la marge de négociation)
- **Langues** : anglais courant à l'oral / CET-6 / IELTS X / langue maternelle
- **Certifications** : CFA / CPA / PMP / AWS Solutions Architect etc.
- **Déplacements / détachement / heures supplémentaires** : "接受出差" (déplacements acceptés), "奇偶周末调休" (repos alterné week-ends pairs/impairs), "项目制 996" (996 par projet)
- **Lieu de travail** : ville + remote / hybride ou non

## Contre-signaux (être vigilant à la vue de ces mentions)

- "其他领导交办的任务" (tâches confiées par les autres dirigeants) → périmètre de travail flou
- "良好的抗压能力" (bonne résistance à la pression) → beaucoup d'heures supplémentaires
- "拥抱变化 / 快速迭代" (étreindre le changement / itération rapide) → direction métier instable
- "扁平化沟通 / 没有层级" (communication plate / sans hiérarchie) → en pratique souvent plus désordonné
- "5 险一金 + 节日福利" (5 assurances + fonds de logement + avantages de fête) mis en évidence dans le JD → les avantages s'arrêtent probablement là

## Format de sortie (présenté à l'utilisateur à l'étape 1)

```json
{
  "company": "XX 公司",
  "position": "XX 岗位",
  "must_have": [
    {"item": "5 年以上 C 端产品经验", "evidence": "JD 第 X 行"},
    {"item": "熟练 SQL", "evidence": "JD 第 Y 行"}
  ],
  "nice_to_have": [
    {"item": "海外业务经验", "evidence": "JD 第 Z 行"}
  ],
  "soft_skills": ["跨部门推动", "数据驱动决策"],
  "responsibilities": [
    "主导 ___ 业务线产品规划",
    "通过数据分析驱动迭代"
  ],
  "special_requirements": {
    "education": "本科及以上",
    "years": "5+",
    "language": "英语口语流利",
    "location": "上海，可接受短期出差"
  }
}
```
